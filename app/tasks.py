from io import BytesIO
from flask import Blueprint, abort, g
from werkzeug.exceptions import InternalServerError
from celery import states

from . import celery
from .utils import url_for

text_types = (str, bytes)
try:
    text_types += (unicode,)
except NameError:
    # no unicode on Python 3
    pass

tasks = Blueprint('tasks', __name__)


@celery.task
def run_flask_request(environ):
    from .wsgi_aux import app

    if '_wsgi.input' in environ:
        environ['wsgi.input'] = BytesIO(environ['_wsgi.input'])

    # Create a request context similar to that of the original request
    # so that the task can have access to flask.g, flask.request, etc.
    with app.request_context(environ):
        # Record the fact that we are running in the Celery worker now
        g.in_celery = True

        # Run the route function and record the response
        try:
            rv = app.full_dispatch_request()
        except:
            # If we are in debug mode we want to see the exception
            # Else, return a 500 error
            if app.debug:
                raise
            rv = app.make_response(InternalServerError())
        return (rv.get_data(), rv.status_code, rv.headers)


@tasks.route('/status/<id>', methods=['GET'])
def get_status(id):
    """
    Return status about an asynchronous task. If this request returns a 202
    status code, it means that task hasn't finished yet. Else, the response
    from the task is returned.
    """
    task = run_flask_request.AsyncResult(id)
    if task.state == states.PENDING:
        abort(404)
    if task.state == states.RECEIVED or task.state == states.STARTED:
        return '', 202, {'Location': url_for('tasks.get_status', id=id)}
    return task.info
