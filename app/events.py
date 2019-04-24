import time
import logging
import base64
import numpy as np
from datetime import datetime
from io import BytesIO
from PIL import Image
from celery import chain
from app.models import Session
from . import socketio, celery, cssi, db

logger = logging.getLogger('cssi.api')


@socketio.on("test/start")
def on_test_start(head_frame, scene_frame, session_id, latency_interval=2):
    _head_frame = head_frame["head_frame"]
    _scene_frame = scene_frame["scene_frame"]

    # decoding base64 string to opencv compatible format
    _head_frame_starter = _head_frame.find(',')
    _head_frame_image_data = _head_frame[_head_frame_starter + 1:]
    _head_frame_image_data = bytes(_head_frame_image_data, encoding="ascii")
    _head_frame_decoded = np.array(Image.open(BytesIO(base64.b64decode(_head_frame_image_data))))

    _scene_frame_starter = _scene_frame.find(',')
    _scene_frame_image_data = _scene_frame[_scene_frame_starter + 1:]
    _scene_frame_image_data = bytes(_scene_frame_image_data, encoding="ascii")
    _scene_frame_decoded = np.array(Image.open(BytesIO(base64.b64decode(_scene_frame_image_data))))

    latency_workflow = chain(persist_prev_frames.s(_head_frame_decoded, _scene_frame_decoded, latency_interval), calculate_latency.s(_head_frame_decoded, _scene_frame_decoded, session_id["session_id"])).apply_async(expires=10)

    sentiment_workflow = record_sentiment.apply_async(args=[_head_frame_decoded], expires=10)


@socketio.on("disconnect")
def on_disconnect():
    """A Socket.IO client has disconnected."""
    print("Socket.IO Client Disconnected")


@celery.task
def calculate_latency(pre_frames, curr_head_frame, curr_scene_frame, session_id):
    print('Session id: {}'.format(session_id))
    from .wsgi_aux import app
    with app.app_context():
        pre_head_frame, prev_scene_frame = pre_frames

        _, phf_pitch, phf_yaw, phf_roll = cssi.latency.calculate_head_pose(frame=pre_head_frame)
        _, chf_pitch, chf_yaw, chf_roll = cssi.latency.calculate_head_pose(frame=curr_head_frame)
        _, _, sf_pitch, sf_yaw, sf_roll = cssi.latency.calculate_camera_pose(first_frame=prev_scene_frame, second_frame=curr_scene_frame, crop=True, crop_direction='horizontal')

        head_angles = [[phf_pitch, phf_yaw, phf_roll], [chf_pitch, chf_yaw, chf_roll]]
        camera_angles = [sf_pitch, sf_yaw, sf_roll]

        latency_score = cssi.latency.generate_score(head_angles=head_angles, camera_angles=camera_angles)

        print(
            'Celery calculate_latency Task - Previous Head Frame : {0}, {1}, {2}'.format(phf_pitch, phf_yaw, phf_roll))
        print('Celery calculate_latency Task - Current Head Frame : {0}, {1}, {2}'.format(chf_pitch, chf_yaw, chf_roll))
        print('Celery calculate_latency Task - Scene Frame : {0}, {1}, {2}'.format(sf_pitch, sf_yaw, sf_roll))
        print('Celery calculate_latency Task - Latency Score : {0}'.format(latency_score))

        new_score = {'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'score': latency_score}

        session = Session.query.filter_by(id=session_id).first()
        if session is not None:
            session.latency_scores.append(new_score)
            print('New Scores: {}'.format(session.latency_scores))
            db.session.commit()


@celery.task
def record_sentiment(head_frame):
    """Sample celery task that posts a message."""
    sentiment = cssi.sentiment.detect_emotions(frame=head_frame)
    print('From celery evaluate_sentiment: {0}'.format(sentiment))


@celery.task
def persist_prev_frames(head_frame, scene_frame, interval):
    time.sleep(interval)
    return head_frame, scene_frame

