telegram_obj = None


def fetch_singleton():
    global telegram_obj
    if telegram_obj is None:
        from telegram.telegram_api import Telegram
        telegram_obj = Telegram()
    return telegram_obj
