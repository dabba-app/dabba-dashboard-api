"""This is an example app, demonstrating usage."""

import os
from random import randrange as rr

from flask import (
    Flask,
    request,
    jsonify,
    redirect
)
from flask_cors import CORS
from flask_cors import cross_origin
from flask_jsondash.charts_builder import charts

"""ENV VARIABLES. No need to change now as all defaults created"""
# CHARTS_DB_HOST - The DB server hostname (defaults to 'localhost')
# CHARTS_DB_PORT - The DB server port (defaults to 27017)
# CHARTS_DB_NAME - The DB database name (defaults to 'charts')
# CHARTS_DB_TABLE The DB collection name (defaults to 'views')
# CHARTS_ACTIVE_DB The DB backend to use - options: 'mongo' (default)

app = Flask(__name__)
CORS(app)
app.debug = True
app.register_blueprint(charts)

# Config
app.config['SECRET_KEY'] = '14BCE'
app.config.update(
    JSONDASH_FILTERUSERS=False,
    JSONDASH_GLOBALDASH=True,
    JSONDASH_GLOBAL_USER='global',
)


def _can_edit_global():
    return True


def _can_delete():
    return True


def _can_clone():
    return True


def _get_username():
    return 'anonymous'


# Config examples.
app.config['JSONDASH'] = dict(
    metadata=dict(
        created_by=_get_username,
        username=_get_username,
    ),
    static=dict(
        js_path='js/vendor/',
        css_path='css/vendor/',
    ),
    auth=dict(
        edit_global=_can_edit_global,
        clone=_can_clone,
        delete=_can_delete,
    )
)


@cross_origin()
@app.route('/line')
def linechart():
    """Fake endpoint."""

    def rr_list(max_range=10):
        """Generate a list of random integers."""
        return [rr(0, 100) for i in range(max_range)]

    STRESS_MAX_POINTS = 300

    if 'stress' in request.args:
        return jsonify({
            'bar-{}'.format(k): rr_list(max_range=STRESS_MAX_POINTS)
            for k in range(STRESS_MAX_POINTS)
        })
    return jsonify({
        "line1": [1, 4, 3, 10, 12, 14, 18, 10],
        "line2": [1, 2, 10, 20, 30, 6, 10, 12, 18, 2],
        "line3": rr_list(),
    })


@app.route('/', methods=['GET'])
def index():
    return redirect(request.base_url + 'charts')


if __name__ == '__main__':
    PORT = int(os.getenv('PORT', 8080))
    HOST = os.getenv('HOST', '0.0.0.0')
    app.run(debug=True, host=HOST, port=PORT)
