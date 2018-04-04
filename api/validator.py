import requests
import os
import logging
from pymongo import MongoClient

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')


def __fetch_mongo_client():
    mongo_host = os.environ.get('CHARTS_DB_HOST')
    mongo_port = 27017
    return MongoClient(mongo_host, mongo_port, maxPoolSize=50)


def validate_bin_data(data):
    if not isinstance(data, dict):
        return {'error': 'Data must be a dict'}
    if 'U_ID' not in data or not isinstance(data.get('U_ID', None), basestring):
        return {'error': 'key U_ID of type string must be present'}
    if 'USER_NAME' not in data or not isinstance(data.get('USER_NAME', None), basestring):
        return {'error': 'key USER_NAME of type string must be present'}
    if 'URL' not in data or not isinstance(data.get('URL', None), basestring):
        return {'error': 'key URL of type string must be present'}
    if 'LEVEL' not in data or not isinstance(data.get('LEVEL', None), int):
        return {'error': 'key LEVEL of type int must be present'}
    if 'LAT' not in data or not isinstance(data.get('LAT', None), basestring):
        return {'error': 'key LAT of type string is required'}
    if 'LONG' not in data or not isinstance(data.get('LONG', None), basestring):
        return {'error': 'key LONG of type string is required'}
    if 'TIMESTAMP' not in data or not isinstance(data.get('TIMESTAMP', None), basestring):
        return {'error': 'key TIMESTAMP of type string is required'}
    if 'TAGS' not in data or not isinstance(data.get('TAGS', None), list):
        return {'error': 'key TAGS of type list is required'}
    if 'TYPE' not in data or not isinstance(data.get('TYPE', None), basestring):
        return {'error': 'key TYPE of type basestring either "0" or "1" is required'}

    # Get garbage from DB
    client = __fetch_mongo_client()
    db = client.admin

    classifier = dict()
    cursor = db['garbage'].find({})
    for document in cursor:
        classifier.update({document['NAME']: document['TYPE']})
    client.close()

    bio = 0
    nonbio = 0
    stag = ""
    for tag in data['TAGS']:
        if tag in classifier.keys() and classifier.get(tag) == "biodegradable":
            bio += 1
            stag = tag
        if tag in classifier.keys() and classifier.get(tag) == "non-biodegradable":
            nonbio += 1
            stag = tag

    async_msg_url = os.environ.get('TELEGRAM_URL', 'http://dabba-telegram.us-west-2.elasticbeanstalk.com') + '/sendasync/'
    user = data.get('USER_NAME', 'piyush9620')

    if bio > nonbio and 'TYPE' in data and data['TYPE'] == "1":
        msg = stag + " : Dear user, you have put the waste in the wrong dustbin, please put it in the biodegradable waste bin as " + stag + " is classified as biodegradable"
        data_to_send = "{\"USER\":\"" + user + "\",\"MSG\":\"" + msg + "\"}"
        try:
            r = requests.post(url=async_msg_url, data=data_to_send)
            logging.debug('Telegram Response msg {}'.format(r.text))
        except Exception as e:
            logging.error(e)
            return {'error': 'wrongly classified waste, not able to send notification for the same'}

    elif bio < nonbio and 'TYPE' in data and data['TYPE'] == "0":
        msg = stag + " : Dear user, you have put the waste in the wrong dustbin, please put it in the non-biodegradable waste bin as " + stag + " is classified as non-biodegradable"
        data_to_send = "{\"USER\":\"" + user + "\",\"MSG\":\"" + msg + "\"}"
        try:
            r = requests.post(url=async_msg_url, data=data_to_send)
            logging.debug('Telegram Response msg {}'.format(r.text))
        except Exception as e:
            logging.error(e)
            return {'error': 'wrongly classified waste, not able to send notification for the same'}

    return {'success': 'data validation successful'}


def validate_garbage_type(data):
    if not isinstance(data, dict):
        return {'error': 'Data must be a dict'}
    print (data.get('TYPE'))
    if 'TYPE' in data and data['TYPE'] != 'biodegradable' and data['TYPE'] != 'non-biodegradable':
        return {'error': 'key TYPE of type string must be present of type biodegradable or non-biodegradable'}
    if 'TYPE' not in data or not isinstance(data.get('TYPE', None), basestring):
        return {'error': 'key TYPE of type string must be present of type biodegradable or non-biodegradable'}
    if 'NAME' not in data or not isinstance(data.get('NAME', None), basestring):
        return {'error': 'key NAME of type string must be present'}
    return {'success': 'data validation successful'}
