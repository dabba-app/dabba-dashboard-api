import os
import json
import logging
from pickle import load

import telebot
from pymongo import MongoClient
from telebot import types

with open(os.path.dirname(os.path.realpath(__file__)) + '/../config.json') as json_config_file:
    config = json.load(json_config_file)

for k, v in config.iteritems():
    os.environ[k] = v

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

host = os.environ.get('CHARTS_DB_HOST')
port = 27017
client = MongoClient(host, port)
db = client.telegram_db
text = load(open(os.path.dirname(os.path.realpath(__file__)) + '/text.txt', 'rb'))

markup = types.ReplyKeyboardMarkup()
start = types.KeyboardButton('/start')
location = types.KeyboardButton('/location')
reset = types.KeyboardButton('/reset')
status = types.KeyboardButton('/status')
markup.row(start, location)
markup.row(reset, status)

# token = "506400947:AAFaKrX-EFVhM-O1e6rV5XyWMzVWtMB1Wdo"
token = os.environ.get('TELEGRAM_KEY')
bot = telebot.TeleBot(token)
async_bot = telebot.AsyncTeleBot(token)
config_dict = dict()


class Telegram:  # ADD PI-CLIENT VALIDATION TO EACH!

    def __init__(self):  # add Boolean variable, MAC ID of Pi, OR SERVER SIDE CODE???
        if os.path.isfile('config.p'):
            config_dict = load(open('config.p', 'rb'))

    @bot.message_handler(commands=['start'])
    def first_start(message):
        print (message)
        posts = db.posts
        if posts.find_one({"C_ID": str(message.from_user.id)}) is None:
            config_dict.update({"C_ID": message.from_user.id})
            post = {"C_ID": str(message.from_user.id),
                    "USER_NAME": str(message.from_user.username),
                    "U_ID": None,
                    "LAT": None,
                    "LONG": None,
                    "URL": None,
                    "TYPE": None}
            posts.insert_one(post)
            bot.reply_to(message, text['start'], reply_markup=markup)
        else:
            bot.reply_to(message, "Hello", reply_markup=markup)
            # dump(message, open('message.p', 'wb'))

    def send_message(self, chat_id, message):
        async_bot.send_message(chat_id, message)

    @bot.message_handler(commands=['location'])
    def location_request(message):
        bot.reply_to(message, text['location_request'])

    @bot.message_handler(commands=['reset'])
    def reset(message):
        try:
            posts = db.posts
            posts.delete_many({"C_ID": str(message.from_user.id)})
            bot.reply_to(message, "Reset successfully")
        except:
            bot.reply_to(message, "Error")

    @bot.message_handler(commands=['status'])
    def status(message):
        try:
            posts = db.posts
            print (posts.find_one({"C_ID": str(message.from_user.id)}))
            url = posts.find_one({"C_ID": str(message.from_user.id)})['URL']
            bot.reply_to(message, str(url))
        except:
            bot.reply_to(message, "Error")

    @bot.message_handler(content_types=['text'])
    def mac_ID(message):
        try:
            [mac_id, bin_type] = message.text.split(' ')
            if int(bin_type) not in [0, 1]:
                raise ValueError
            if db.posts.find_one({"C_ID": str(message.from_user.id), "U_ID": str(int(mac_id))}) is None \
                    and db.posts.find_one({"U_ID": str(int(mac_id))}) is None \
                    and db.posts.find_one({"C_ID": str(message.from_user.id)})["U_ID"] is None:
                posts = db.posts
                posts.update_one({"C_ID": str(message.from_user.id), "U_ID": None},
                                 {"$set": {"U_ID": str(int(mac_id)), "TYPE": int(bin_type)}})
                bot.reply_to(message,
                             "MAC ID {} and bin type {} successfully set! Be sure to send your location again!".format(
                                 mac_id, 'non biodegradable' if int(bin_type) else 'biodegradable'))

            elif db.posts.find_one({"C_ID": str(message.from_user.id), "U_ID": str(int(mac_id))}) is None \
                    and db.posts.find_one({"U_ID": str(int(mac_id))}) is None:
                posts = db.posts
                post = {"C_ID": str(message.from_user.id),
                        "USER_NAME": str(message.from_user.username),
                        "U_ID": str(int(mac_id)),
                        "LAT": None,
                        "LONG": None,
                        "URL": None,
                        "TYPE": int(bin_type)}
                posts.insert_one(post)
                bot.reply_to(message,
                             "MAC ID {} and bin type {} successfully set! Be sure to send your location again!".format(
                                 mac_id, 'non biodegradable' if int(bin_type) else 'biodegradable'))

                for x in db.posts.find({"C_ID": str(message.from_user.id)}):
                    print (x)

            elif not db.posts.find_one({"C_ID": str(message.from_user.id), "U_ID": str(int(mac_id))}) is None:
                posts = db.posts
                posts.update_one({'C_ID': str(message.from_user.id), 'U_ID': str(int(mac_id))},
                                 {"$set": {'TYPE': int(bin_type)}})
                for x in db.posts.find({"C_ID": str(message.from_user.id)}):
                    print (x)

                if int(bin_type) == 0:
                    bin_type = 'biodegradable'
                else:
                    bin_type = 'non-biodegradable'
                bot.reply_to(message, 'Bin type {} successfully set!'.format(bin_type))

            else:
                bot.reply_to(message, "Error")
                print (db.posts.find_one({"C_ID": str(message.from_user.id)}))
        except Exception as e:
            bot.reply_to(message, e)

    @bot.message_handler(content_types=['location'])
    def get_location(message):
        try:
            if not db.posts.find_one({"C_ID": str(message.from_user.id)}) is None:
                posts = db.posts
                location_lat, location_long = message.location.latitude, message.location.longitude
                posts.update_many({'C_ID': str(message.from_user.id)}, {"$set": {"LAT": location_lat}})
                posts.update_many({'C_ID': str(message.from_user.id)}, {"$set": {"LONG": location_long}})
                # dump(config_dict, open('config.p', 'wb'))
                bot.reply_to(message, text['location_received'].format(location_lat, location_long))
            else:
                bot.reply_to(message, "Error")

        except:
            bot.reply_to(message, "Error")

    def poll(self):
        logging.info("Telegram API Running in background")
        bot.polling(none_stop=True)
