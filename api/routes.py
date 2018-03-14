from flask import request, Response, Blueprint
from flask_cors import cross_origin

import logging
import json

from api import controller

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')


def register_bin_endpoints(app):
    bins = Blueprint('bins', __name__, template_folder='templates')

    @cross_origin()
    @bins.route('/', methods=['GET', 'PUT', 'POST'])
    def get_bins():
        if request.method == 'GET':
            try:
                data = controller.get_all_bins_data()
                return Response(response=json.dumps(data), mimetype='application/json')
            except Exception, e:
                logging.error(e)
                return Response(response={'error': 'Server Error, see logs'}, mimetype='application/json')
        elif request.method == 'PUT' or request.method == 'POST':
            try:
                data = controller.insert_bin_data(json.loads(request.data))
                return Response(response=json.dumps(data), mimetype='application/json')
            except Exception, e:
                logging.error(e)
                return Response(response={'error': 'Server Error, see logs'}, status=201, mimetype='application/json')

    @cross_origin()
    @bins.route('/<bin_uid>', methods=['GET', 'PUT', 'POST'])
    def get_bin(bin_uid):
        if request.method == 'GET':
            try:
                data = controller.get_bin_data(int(bin_uid))
                return Response(response=json.dumps(data), mimetype='application/json')
            except Exception, e:
                logging.error(e)
                return Response(response={'error': 'Server Error, see logs'}, mimetype='application/json')

    app.register_blueprint(bins, url_prefix='/bins')
