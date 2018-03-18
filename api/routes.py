from flask import request, Response, Blueprint, jsonify
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
    @bins.route('/<bin_usr>', methods=['GET', 'PUT', 'POST'])
    def get_all_bins(bin_usr):
        if request.method == 'GET':
            try:
                data = controller.get_bin_data(bin_usr)
                return Response(response=json.dumps(data), mimetype='application/json')
            except Exception, e:
                logging.error(e)
                return Response(response={'error': 'Server Error, see logs'}, mimetype='application/json')

    @cross_origin()
    @bins.route('/<bin_usr>/chart', methods=['GET', 'PUT', 'POST'])
    def get_bin_w_usr(bin_usr):
        if request.method == 'GET':
            try:
                data = controller.get_bin_data(bin_usr)
                return Response(response=json.dumps(data), mimetype='application/json')
            except Exception, e:
                logging.error(e)
                return Response(response={'error': 'Server Error, see logs'}, mimetype='application/json')

    # @cross_origin()
    # @app.route('/c3ts')
    # def c3ts():
    #     data = dict(
    #         x='x',
    #         xFormat='%Y%m%d',
    #         columns=[
    #             ['x', '20130101', '20130102', '20130103', '20130104', '20130105', '20130106'],
    #             ['data1', 30, 200, 100, 400, 150, 2],
    #             ['data2', 130, 340, 200, 500, 250, 350]
    #         ]
    #     )
    #     return jsonify(dict(data=data))

    app.register_blueprint(bins, url_prefix='/bins')
