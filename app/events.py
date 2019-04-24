import logging
import base64
import numpy as np
from io import BytesIO
from PIL import Image
from celery import chain

from app.models import Session
from . import socketio, celery, db
from .tasks import calculate_latency, persist_prev_frames, record_sentiment

logger = logging.getLogger('cssi.api')


@socketio.on("test/init")
def on_test_init(session_id):
    from .wsgi_aux import app
    with app.app_context():
        session = Session.query.filter_by(id=session_id).first()
        if session is not None:
            if session.status == 'initialized':
                session.status = 'started'
                db.session.commit()
                socketio.send({"status": "success", "message": "The test session started successfully."}, json=True)
                logger.info("Successfully initialized the test session. ID: {0}".format(session_id))


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

    chain(
        persist_prev_frames.s(_head_frame_decoded, _scene_frame_decoded, latency_interval),
        calculate_latency.s(_head_frame_decoded, _scene_frame_decoded, session_id["session_id"])
    ).apply_async(expires=10)

    record_sentiment.apply_async(args=[_head_frame_decoded, session_id["session_id"]], expires=10)


@socketio.on("test/stop")
def on_test_stop(session_id):
    from .wsgi_aux import app
    with app.app_context():
        session = Session.query.filter_by(id=session_id).first()
        if session is not None:
            if session.status == 'started':
                session.status = 'completed'
                db.session.commit()
                socketio.send({"status": "success", "message": "The test session completed successfully."}, json=True)
                celery.control.purge()  # stop all celery workers
                logger.info("The test session was terminated successfully. ID: {0}".format(session_id))


@socketio.on("disconnect")
def on_disconnect():
    """A Socket.IO client has disconnected."""
    celery.control.purge()  # stop all celery workers
    logger.info("The Socket.IO client disconnected.")
