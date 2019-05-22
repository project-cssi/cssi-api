import logging

from app.models import Session
from . import socketio, celery, db
from .tasks import calculate_latency, persist_frames, record_sentiment, calculate_plugin_unit_scores
from .utils import decode_base64

logger = logging.getLogger("cssi.api")


@socketio.on("test/init")
def on_test_init(session_id):
    from .wsgi_aux import app
    with app.app_context():
        session = Session.query.filter_by(id=session_id).first()
        if session is not None:
            if session.status == "initialised":
                session.status = "started"
                db.session.commit()
                socketio.send({"status": "success", "message": "The test session started successfully."}, json=True)
                logger.info("Successfully initialized the test session. ID: {0}".format(session_id))


@socketio.on("test/start")
def on_test_start(head_frame, scene_frame, session_id, latency_interval=2):
    _head_frame = head_frame["head_frame"]
    _scene_frame = scene_frame["scene_frame"]
    latency_frame_count = 10

    # decoding head-frame image(base64) string to OpenCV compatible format
    _head_frame_decoded = decode_base64(_head_frame)

    # decoding scene-frame image(base64) string to OpenCV compatible format
    _scene_frame_decoded = decode_base64(_scene_frame)

    # chain the two tasks which persist the frames and pass them to
    # the latency worker after the specified time interval.
    result = persist_frames.delay(head_frame=_head_frame, scene_frame=_scene_frame, limit=latency_frame_count)

    if result:
        calculate_latency.delay(session_id["session_id"], limit=latency_frame_count)

    record_sentiment.apply_async(args=[_head_frame_decoded, session_id["session_id"]], expires=10)

    calculate_plugin_unit_scores.apply_async(args=[_head_frame_decoded, _scene_frame_decoded, session_id["session_id"]], expires=10)


@socketio.on("test/stop")
def on_test_stop(session_id):
    from .wsgi_aux import app
    with app.app_context():
        session = Session.query.filter_by(id=session_id).first()
        if session is not None:
            if session.status == "started":
                session.status = "completed"
                db.session.commit()
                socketio.send({"status": "success", "message": "The test session completed successfully."}, json=True)
                celery.control.purge()  # stop all celery workers
                logger.info("The test session was terminated successfully. ID: {0}".format(session_id))


@socketio.on("disconnect")
def on_disconnect():
    """A Socket.IO client has disconnected."""
    celery.control.purge()  # stop all celery workers
    logger.info("The Socket.IO client disconnected.")
