import os
from pymongo import MongoClient
from validator import validate_bin_data
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')


def __fetch_mongo_client():
    mongo_host = os.environ['CHARTS_DB_HOST']
    mongo_port = 27017
    return MongoClient(mongo_host, mongo_port, maxPoolSize=50)


def __close_mongo_client(client):
    client.close()

def insert_dropbox_url(data):
    telegram_client = __fetch_mongo_client()
    db = telegram_client.telegram_db
    posts = db.posts
    posts.update_one({'C_ID': str(data.U_ID)}, {"$set": {"LAT": str(data.URL)}})
    __close_mongo_client(telegram_client)


def get_all_bins_data():
    client = __fetch_mongo_client()
    db = client.admin

    documents = []

    cursor = db['bin_data'].find({})
    for document in cursor:
        document.pop('_id')
        documents.append(document)

    __close_mongo_client(client=client)

    return documents


def get_bin_data(bin_usr):
    client = __fetch_mongo_client()
    db = client.admin

    documents = []

    cursor = db['bin_data'].find({"USER_NAME": bin_usr})
    for document in cursor:
        document.pop('_id')
        documents.append(document)

    __close_mongo_client(client=client)

    return documents


def insert_bin_data(data):
    client = __fetch_mongo_client()
    db = client.admin

    validation_msg = validate_bin_data(data)
    if 'success' in validation_msg:
        logging.info('Data validation successful')

        db['bin_data'].insert_one(data)
        insert_dropbox_url(data)

        logging.info('Data inserted into DB')

        __close_mongo_client(client=client)

        data.pop('_id')
        return data
    else:
        logging.warning('Data validation failed', )
        return validation_msg
