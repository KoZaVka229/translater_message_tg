import os

from telegram.client import Telegram
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

load_dotenv()


TRIGGER = os.getevn('TRIGGER', '!!!')
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
PHONE = os.getenv('PHONE')
LIB_PATH = os.getenv('LIB_PATH')
DATA_KEY = LIB_PATH
CODES_COUNT = int(os.getenv('CODES_COUNT')) or None


codes = [v for k, v in GoogleTranslator('ru', 'en').get_supported_languages(as_dict=True).items()]
codes.remove('ru')
codes = codes[:CODES_COUNT]


tg = Telegram(API_ID, API_HASH, DATA_KEY, PHONE, library_path=LIB_PATH)
tg.login()


def new_message_handler(update):
    chat_id = update['message']['chat_id']
    text = update['message']['content'].get('text', {}).get('text', '').lower()

    if TRIGGER not in text:
        return

    text = text.replace(TRIGGER, '')
    for code in codes:
        translator = GoogleTranslator('ru', code)
        tg.send_message(chat_id=chat_id, text=translator.translate(text))


tg.add_message_handler(new_message_handler)
tg.idle()
