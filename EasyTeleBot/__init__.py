from flask import Flask, request
import telegram
from EasyTeleBot.Chat import Chat
from EasyTeleBot import BotActionLib

import io
import json
from urllib import parse


class EasyTelegramBot:
    def __init__(self):
        return


def CreateEasyTelegramBot(config_file, telegram_token=None, webhook_url=None, bot_name=None, print_updates=None):
    config_text = None
    if type(config_file) is str:
        config_file = open(config_file)
    if issubclass(type(config_file), io.IOBase):
        config_text = json.load(config_file)

    easy_telegram_bot = EasyTelegramBot()

    print("read config file - {}".format(config_text))

    if not config_text:
        raise Exception("could not initialize EasyTeleBot from config file")

    easy_telegram_bot.bot_actions = BotActionLib.CreateBotActionsList(config_text['actions'])

    easy_telegram_bot.telegram_token = config_text['telegram_token']
    if telegram_token:
        easy_telegram_bot.telegram_token = telegram_token

    easy_telegram_bot.webhook_url = config_text['webhook_url']
    if webhook_url:
        easy_telegram_bot.webhook_url = webhook_url

    url = parse.urlparse(easy_telegram_bot.webhook_url)
    if not url.scheme or not url.netloc:
        raise Exception('EasyTeleBot need to get webhook with http:// or https:// , got {}'.format(easy_telegram_bot.webhook_url))
    easy_telegram_bot.webhook_base_url = url.scheme + "//" + url.netloc + "/"
    easy_telegram_bot.base_url = easy_telegram_bot.webhook_base_url
    easy_telegram_bot.webhook_url_path = url.path
    print('webhook path is = {}'.format(easy_telegram_bot.webhook_url_path))

    easy_telegram_bot.bot_name = config_text['bot_name']
    if bot_name:
        easy_telegram_bot.bot_name = bot_name

    easy_telegram_bot.bot = telegram.Bot(token=easy_telegram_bot.telegram_token)
    easy_telegram_bot.chats = []
    easy_telegram_bot.print_updates = False
    if print_updates:
        easy_telegram_bot.print_updates = print_updates

    if not easy_telegram_bot.telegram_token or not easy_telegram_bot.bot_actions or not easy_telegram_bot.webhook_url or not easy_telegram_bot.bot_name:
        raise Exception("could not initialize EasyTeleBot , missing parameter token={} acts={} url={}"
                        .format(easy_telegram_bot.telegram_token, easy_telegram_bot.bot_actions, easy_telegram_bot.webhook_url))

    easy_telegram_bot.bot.setWebhook(easy_telegram_bot.webhook_url)
    easy_telegram_bot.flask_app = Flask(easy_telegram_bot.bot_name)

    print("EasyTeleBot created bot '{}' successfully".format(config_text['bot_name']))

    @easy_telegram_bot.flask_app.route(easy_telegram_bot.webhook_url_path, methods=['POST'])
    def respond():
        update = telegram.Update.de_json(request.get_json(force=True), easy_telegram_bot.bot)
        if easy_telegram_bot.print_updates:
            print(update)
        if update.callback_query:  # button menu pressed
            return 'ok'
        if update.edited_message:
            return 'ok'
        if update.message and update.message.document:
            return 'ok'
        current_chat = False
        for chat in easy_telegram_bot.chats:  # searches if chat has previous records
            if chat.id == update.message.chat.id:
                current_chat = chat
                break
        if not current_chat:
            current_chat = Chat(easy_telegram_bot, update.message)  # creates a new chat
            print("New chat added id = {}".format(update.message.chat.id))
            easy_telegram_bot.chats.append(current_chat)
        current_chat.GotMessage(easy_telegram_bot.bot, update.message)
        return 'ok'

    @easy_telegram_bot.flask_app.route('/set_webhook', methods=['GET', 'POST'])
    def set_webhook():
        print('webhook set')
        webhook_ok = easy_telegram_bot.bot.setWebhook(easy_telegram_bot.webhook_url)
        return "webhook setup - {webhook}".format(webhook='ok' if webhook_ok else 'failed')

    return easy_telegram_bot
