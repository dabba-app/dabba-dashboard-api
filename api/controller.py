import os
from pymongo import MongoClient
import validator
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')


def __fetch_mongo_client():
    mongo_host = os.environ.get('CHARTS_DB_HOST')
    mongo_port = 27017
    return MongoClient(mongo_host, mongo_port, maxPoolSize=50)


def __close_mongo_client(client):
    client.close()


def insert_dropbox_url(data):
    telegram_client = __fetch_mongo_client()
    db = telegram_client.telegram_db
    posts = db.posts
    posts.update_one({'C_ID': str(data["U_ID"])}, {"$set": {"LAT": str(data["URL"])}})
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

    validation_msg = validator.validate_bin_data(data)
    data['success'] = validation_msg['success']
    data['segregation'] = validation_msg['segregation']
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
        return data


def delete_bin_data(u_id):
    client = __fetch_mongo_client()
    db = client.admin

    del_data = db['bin_data'].delete_many({'U_ID': u_id})

    __close_mongo_client(client=client)

    return del_data.raw_result


def get_garbage_type(name):
    client = __fetch_mongo_client()
    db = client.admin

    document = db['garbage'].find_one({"NAME": name})
    if isinstance(document, dict) and '_id' in document:
        document.pop('_id')
    elif not document:
        document = {}

    __close_mongo_client(client=client)

    return document


def insert_garbage_type(data):
    client = __fetch_mongo_client()
    db = client.admin

    validation_msg = validator.validate_garbage_type(data)
    if 'success' in validation_msg:
        logging.info('Data validation successful')

        db['garbage'].insert_one(data)

        logging.info('Data inserted into DB')

        __close_mongo_client(client=client)

        data.pop('_id')
        return data
    else:
        logging.warning('Data validation failed', )
        return validation_msg


def get_all_garbage_types():
    client = __fetch_mongo_client()
    db = client.admin

    documents = []

    cursor = db['garbage'].find({})
    for document in cursor:
        document.pop('_id')
        documents.append(document)

    __close_mongo_client(client=client)

    return documents
