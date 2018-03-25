import os
import json
import logging
from flask import (
    Flask,
    request,
    redirect,
)
from flask_cors import CORS
from flask_cors import cross_origin

from api import routes
from api import charts_dashboard

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

"""
CHARTS ENV VARIABLES

CHARTS_DB_HOST - The DB server hostname (defaults to 'localhost')
CHARTS_DB_PORT - The DB server port (defaults to 27017)
CHARTS_DB_NAME - The DB database name (defaults to 'charts')
CHARTS_DB_TABLE The DB collection name (defaults to 'views')
CHARTS_ACTIVE_DB The DB backend to use - options: 'mongo' (default)
"""

# Prod override
try:
    with open(os.path.dirname(__file__) + '/config.json') as json_config_file:
        config = json.load(json_config_file)

    for k, v in config.iteritems():
        os.environ[k] = v

# Config file not passed! Using defaults in local
except Exception as e:
    logging.warning('Config file not found. Using defaults with CHARTS_DB_HOST as %s' % (os.environ.get('CHARTS_DB_HOST', None)))
    pass

# Init App
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '14BCE')

app.debug = True
CORS(app)

# Init charts dashboard
charts_dashboard.init(app)

# Register bin endpoints
routes.register_bin_endpoints(app)


# Redirect root to dashboard
@cross_origin()
@app.route('/', methods=['GET'])
def index():
    return redirect(request.base_url + 'charts')


# start app
if __name__ == '__main__':
    PORT = int(os.getenv('PORT', 8000))
    HOST = os.getenv('HOST', '0.0.0.0')
    app.run(debug=True, host=HOST, port=PORT)
