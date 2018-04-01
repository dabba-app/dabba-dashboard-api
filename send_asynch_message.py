from pymongo import MongoClient

from telegram_api import telegram as t


def getMongoClient():
    #return MongoClient(host=os.environ['HOST'], port=int(os.environ['PORT']),
    #                   username=os.environ['USER'], password=os.environ['PASS']) #add params
    return MongoClient()

def send_message(user_name, message):
    client = getMongoClient()
    telegram = client.telegram_db.posts
    chat_id = telegram.find_one({"USER_NAME": str(user_name)})['C_ID']
    out = t()
    out.send_message(chat_id, str(message))