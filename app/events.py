from . import socketio, celery

@celery.task
def calculate_latency():
    """Sample celery task that posts a message."""
    from .wsgi_aux import app
    with app.app_context():
        print('hi from celery')


@socketio.on('post_message')
def on_post_message():
    """Sample post message."""
    calculate_latency.apply_async()
    print('post message')


@socketio.on('disconnect')
def on_disconnect():
    """A Socket.IO client has disconnected."""
    print('connection hi disconnected')
