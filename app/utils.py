import time
import base64
from io import BytesIO
from PIL import Image

from flask import url_for as _url_for, current_app, _request_ctx_stack


def timestamp():
    """Return the current timestamp as an integer."""
    return int(time.time())


def url_for(*args, **kwargs):
    """
    url_for replacement that works even when there is no request context.
    """
    if '_external' not in kwargs:
        kwargs['_external'] = False
    reqctx = _request_ctx_stack.top
    if reqctx is None:
        if kwargs['_external']:
            raise RuntimeError('Cannot generate external URLs without a '
                               'request context.')
        with current_app.test_request_context():
            return _url_for(*args, **kwargs)
    return _url_for(*args, **kwargs)


def decode_base64(base64_str):
    """decodes a base64 image string"""
    starter = base64_str.find(',')
    image_data = base64_str[starter + 1:]
    image_data = bytes(image_data, encoding="ascii")
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    if image.mode != "RGB":
        image = image.convert("RGB")
    return image
