import os
from functools import wraps
from flask import request, jsonify


def auth_interceptor(f):
    @wraps(f)
    def auth_decorator(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if auth_header == os.environ['SECRET_KEY']:
            return f(*args, **kwargs)
        return jsonify({'error': 'Pass Authorization in Request Header'})

    return auth_decorator
