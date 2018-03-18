from flask import request, Response, Blueprint, jsonify
from flask_cors import cross_origin

import logging
import json
import time
from api import controller

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')


def register_bin_endpoints(app):
    bins = Blueprint('bins', __name__, template_folder='templates')

    @cross_origin()
    @bins.route('/', methods=['GET', 'PUT', 'POST'])
    def bins_route():
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
    def all_bins_route(bin_usr):
        if request.method == 'GET':
            try:
                data = controller.get_bin_data(bin_usr)
                return Response(response=json.dumps(data), mimetype='application/json')
            except Exception, e:
                logging.error(e)
                return Response(response={'error': 'Server Error, see logs'}, mimetype='application/json')

    @cross_origin()
    @bins.route('/<bin_usr>/chart', methods=['GET'])
    def bin_chart_all_timestamps_route(bin_usr):
        if request.method == 'GET':
            try:
                data = controller.get_bin_data(bin_usr)
                dlist = []
                for d in data:
                    # Remove milliseconds
                    d['TIMESTAMP'] = d['TIMESTAMP'][:d['TIMESTAMP'].rfind('.')]

                    dlist.append({'TIMESTAMP': d['TIMESTAMP'], 'LEVEL': d['LEVEL']})

                dlist.sort(key=lambda x: time.mktime(time.strptime(x['TIMESTAMP'], '%Y-%m-%d %H:%M:%S')))

                date_list = ['x']
                level_list = ['data1']

                for data in dlist:
                    date_list.append(data['TIMESTAMP'])
                    level_list.append(data['LEVEL'])

                chart_data = dict(
                    x='x',
                    xFormat='%Y-%m-%d %H:%M:%S',
                    columns=[
                        date_list,
                        level_list
                    ]
                )

                chart_axis = dict(
                    x=dict(
                        type='timeseries',
                        tick=dict(
                            format='%Y-%m-%d %H:%M:%S'
                        )
                    )
                )
                return jsonify(dict(data=chart_data, axis=chart_axis))

            except Exception, e:
                logging.error(e)
                return Response(response={'error': 'Server Error, see logs'}, mimetype='application/json')

    @cross_origin()
    @bins.route('/<bin_usr>/chart/<date>', methods=['GET'])
    def bin_chart_for_day_as_time_route(bin_usr, date):
        if request.method == 'GET':
            try:
                data = controller.get_bin_data(bin_usr)
                dlist = []
                for d in data:
                    # Split into date and time
                    d['TIMESTAMP'] = d['TIMESTAMP'].split(" ")

                    if d['TIMESTAMP'][0] == date:
                        # Remove milliseconds
                        d['TIMESTAMP'][1] = d['TIMESTAMP'][1][:d['TIMESTAMP'][1].rfind('.')]

                        dlist.append({'TIMESTAMP': d['TIMESTAMP'][1], 'LEVEL': d['LEVEL']})

                dlist.sort(key=lambda x: time.mktime(time.strptime(x['TIMESTAMP'], '%H:%M:%S')))

                date_list = ['x']
                level_list = ['data1']

                for data in dlist:
                    date_list.append(data['TIMESTAMP'])
                    level_list.append(data['LEVEL'])

                chart_data = dict(
                    x='x',
                    xFormat='%H:%M:%S',
                    columns=[
                        date_list,
                        level_list
                    ]
                )

                chart_axis = dict(
                    x=dict(
                        type='timeseries',
                        tick=dict(
                            format='%H:%M:%S'
                        )
                    )
                )
                return jsonify(dict(data=chart_data, axis=chart_axis))

            except Exception, e:
                logging.error(e)
                return Response(response={'error': 'Server Error, see logs'}, mimetype='application/json')

    app.register_blueprint(bins, url_prefix='/bins')
