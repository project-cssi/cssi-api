import json
import logging
import redis
from datetime import datetime

from . import celery, cssi, db
from app.models import Session
from .utils import decode_base64

logger = logging.getLogger('cssi.api')


@celery.task
def calculate_latency(session_id, limit):
    """Celery task which handles latency score generation and persistence"""
    from .wsgi_aux import app
    with app.app_context():
        head_key = "head-frames"
        scene_key = "scene-frames"

        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        head_frames_raw = get_frames_from_redis(r=r, key=head_key, limit=limit)
        scene_frames_raw = get_frames_from_redis(r=r, key=scene_key, limit=limit)

        head_stream = []
        scene_stream = []

        for data in head_frames_raw:
            head_stream.append(decode_base64(data))

        for data in scene_frames_raw:
            scene_stream.append(decode_base64(data))

        _, phf_pitch, phf_yaw, phf_roll = cssi.latency.calculate_head_pose(frame=head_stream[0])
        _, chf_pitch, chf_yaw, chf_roll = cssi.latency.calculate_head_pose(frame=head_stream[1])
        _, _, ff_angles, sf_angles = cssi.latency.calculate_camera_pose(first_frame=scene_stream[0],
                                                                        second_frame=scene_stream[1], crop=True,
                                                                        crop_direction='horizontal')

        head_angles = [[phf_pitch, phf_yaw, phf_roll], [chf_pitch, chf_yaw, chf_roll]]
        camera_angles = [ff_angles, sf_angles]

        latency_score = cssi.latency.generate_rotation_latency_score(head_angles=head_angles,
                                                                     camera_angles=camera_angles)

        # head_movement = cssi.latency.check_for_head_movement(head_stream)
        # logger.debug("Head movement detected: {0}".format(head_movement))

        # pst = cssi.latency.calculate_pst(scene_stream, 10)
        # logger.debug("Pixel switching time: {0}".format(pst))

        session = Session.query.filter_by(id=session_id).first()
        if session is not None:
            new_score = {'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'score': latency_score}
            session.latency_scores.append(new_score)
            db.session.commit()


@celery.task
def record_sentiment(head_frame, session_id):
    """Celery task which handles sentiment score generation and persistence"""
    from .wsgi_aux import app
    with app.app_context():
        sentiment = cssi.sentiment.generate_sentiment_score(frame=head_frame)
        session = Session.query.filter_by(id=session_id).first()
        if session is not None:
            if sentiment is not None:
                new_score = {'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'sentiment': sentiment}
                session.sentiment_scores.append(new_score)
                db.session.commit()


@celery.task
def calculate_plugin_unit_scores(head_frame, scene_frame, session_id):
    """Celery task which handles plugin unit score generation and persistence"""
    from .wsgi_aux import app
    with app.app_context():
        unit_scores = cssi.generate_contributor_plugin_unit_scores(head_frame=head_frame, scene_frame=scene_frame)
        session = Session.query.filter_by(id=session_id).first()
        if session is not None:
            for value in unit_scores:
                new_score = {"timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "score": value["score"]}
                if value["name"] in session.plugin_scores:
                    logger.debug("{0} Appending plugin unit score: {1}".format(value["name"], value["score"]))
                    session.plugin_scores.setdefault(value["name"], []).append(new_score)
                else:
                    logger.debug("{0} Adding new plugin unit score: {1}".format(value["name"], value["score"]))
                    session.plugin_scores[value["name"]] = [new_score]
            db.session.commit()


@celery.task
def persist_frames(head_frame, scene_frame, limit):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    is_complete = save_frames_on_redis(r=r, head_frame=head_frame, scene_frame=scene_frame, limit=limit)
    return is_complete


def save_frames_on_redis(r, head_frame, scene_frame, limit):
    """Store dictionary on redis"""
    head_key = "head-frames"
    scene_key = "scene-frames"
    head_frame_count = 0
    scene_frame_count = 0
    if r.exists(head_key) and r.exists(scene_key):
        head_values = json.loads(r.get(head_key))
        head_values.append(head_frame)
        head_frame_count = len(head_values)

        scene_values = json.loads(r.get(scene_key))
        scene_values.append(scene_frame)
        scene_frame_count = len(scene_values)
    else:
        head_values = [head_frame]
        scene_values = [scene_frame]

    r = redis.StrictRedis(host='localhost')

    r.set(head_key, json.dumps(head_values))
    r.set(scene_key, json.dumps(scene_values))

    if head_frame_count and scene_frame_count >= limit:
        return True

    return False


def get_frames_from_redis(r, key, limit):
    count = 0
    frames = []
    if r.exists(key):
        frames = json.loads(r.get(key))
        count = len(frames)

    if count >= limit:
        r.delete(key)
        # logger.debug("Cleaning frame stream - key: {0}".format(key))

    return frames
