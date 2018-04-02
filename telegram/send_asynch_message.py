from pymongo import MongoClient
import os
from telegram import telegram_obj


def __fetch_mongo_client():
    mongo_host = os.environ.get('CHARTS_DB_HOST')
    mongo_port = 27017
    return MongoClient(mongo_host, mongo_port, maxPoolSize=50)


def send_message(user_name, message):
    client = __fetch_mongo_client()
    telegram = client.telegram_db.posts
    chat_id = telegram.find_one({"USER_NAME": str(user_name)})['C_ID']
    out = telegram_obj.fetch_singleton()
    out.send_message(chat_id, str(message))
