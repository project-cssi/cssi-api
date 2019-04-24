import time
import logging
from datetime import datetime

from . import celery, cssi, db
from app.models import Session

logger = logging.getLogger('cssi.api')


@celery.task
def calculate_latency(pre_frames, curr_head_frame, curr_scene_frame, session_id):
    from .wsgi_aux import app
    with app.app_context():
        pre_head_frame, prev_scene_frame = pre_frames

        _, phf_pitch, phf_yaw, phf_roll = cssi.latency.calculate_head_pose(frame=pre_head_frame)
        _, chf_pitch, chf_yaw, chf_roll = cssi.latency.calculate_head_pose(frame=curr_head_frame)
        _, _, sf_pitch, sf_yaw, sf_roll = cssi.latency.calculate_camera_pose(first_frame=prev_scene_frame,
                                                                             second_frame=curr_scene_frame, crop=True,
                                                                             crop_direction='horizontal')

        head_angles = [[phf_pitch, phf_yaw, phf_roll], [chf_pitch, chf_yaw, chf_roll]]
        camera_angles = [sf_pitch, sf_yaw, sf_roll]

        latency_score = cssi.latency.generate_score(head_angles=head_angles, camera_angles=camera_angles)

        session = Session.query.filter_by(id=session_id).first()
        if session is not None:
            new_score = {'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'score': latency_score}
            session.latency_scores.append(new_score)
            db.session.commit()


@celery.task
def record_sentiment(head_frame, session_id):
    """Sample celery task that posts a message."""
    from .wsgi_aux import app
    with app.app_context():
        sentiment = cssi.sentiment.detect_emotions(frame=head_frame)
        session = Session.query.filter_by(id=session_id).first()
        if session is not None:
            if sentiment is not None:
                new_score = {'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'sentiment': sentiment}
                session.sentiment_scores.append(new_score)
                db.session.commit()


@celery.task
def persist_prev_frames(head_frame, scene_frame, interval):
    time.sleep(interval)
    return head_frame, scene_frame
