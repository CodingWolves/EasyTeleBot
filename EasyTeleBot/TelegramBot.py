from flask import Flask, request
import telegram

from .BotAction import CreateBotActionsList
from .Chat import Chat

import io
import json
from urllib import parse

from .DatabaseLib.ChatDB import LoadChat, SaveChat
from .GenericFunctions import JoinDictionariesLists


class EasyTelegramBot:
    def __init__(self):
        self.telegram_token = None
        self.webhook_url = None
        self.webhook_base_url = None
        self.webhook_url_path = None
        self.base_url = None
        self.bot = None
        self.bot_name = None
        self.bot_actions = None
        self.chats = None
        self.default_action_id = None
        self.print_updates = None
        self.flask_app = None

    def Initialize(self, config_text, telegram_token=None, webhook_url=None, bot_name=None, default_action_id=None,print_updates=None, testing=False):
        if type(config_text) is list:
            config_texts = config_text
            config_text = {}
            for text in config_texts:
                config_text = JoinDictionariesLists(config_text, text)

        if 'actions' not in config_text:
            raise Exception("actions not found")
        self.bot_actions = CreateBotActionsList(config_text['actions'])

        if 'telegram_token' in config_text:
            self.telegram_token = config_text['telegram_token']
        if telegram_token:
            self.telegram_token = telegram_token
        if self.telegram_token is None:
            raise Exception("telegram_token not found")

        if 'webhook_url' in config_text:
            self.webhook_url = config_text['webhook_url']
        if webhook_url:
            self.webhook_url = webhook_url
        if self.webhook_url is None:
            raise Exception("webhook_url not found")

        url = parse.urlparse(self.webhook_url)
        if not url.scheme or not url.netloc:
            raise Exception(
                'EasyTeleBot need to get webhook with http:// or https:// , got {}'.format(
                    self.webhook_url))
        self.webhook_base_url = url.scheme + "//" + url.netloc + "/"
        self.base_url = self.webhook_base_url
        self.webhook_url_path = url.path
        print('webhook path is = {}'.format(self.webhook_url_path))

        if 'bot_name' in config_text:
            self.bot_name = config_text['bot_name']
        if bot_name:
            self.bot_name = bot_name
        if self.bot_name is None:
            raise Exception("bot_name not found")

        self.chats = []

        if 'default_action_id' in config_text:
            self.default_action_id = config_text['default_action_id']
        if default_action_id is not None:
            self.default_action_id = default_action_id

        self.print_updates = False
        if print_updates:
            self.print_updates = print_updates

        self.flask_app = Flask(self.bot_name)

        if not testing:
            self.bot = telegram.Bot(token=self.telegram_token)
            self.bot.setWebhook(self.webhook_url)


def CreateEasyTelegramBot(config_file, telegram_token=None, webhook_url=None, bot_name=None, print_updates=None, testing=False):
    config_text = None
    if type(config_file) is str:
        config_file = open(config_file)
    if issubclass(type(config_file), io.IOBase):
        config_text = json.load(config_file)
    if type(config_file) is list:
        config_files = config_file
        if len(config_files) > 1:
            if type(config_files[0]) is str:
                config_files = [open(file) for file in config_files]
            if issubclass(type(config_files[0]), io.IOBase):
                config_text = [json.load(file) for file in config_files]

    print("read config file - {}".format(config_text))

    if not config_text:
        raise Exception("could not initialize EasyTeleBot from config file")

    easy_telegram_bot = EasyTelegramBot()
    easy_telegram_bot.Initialize(config_text, telegram_token=telegram_token, webhook_url=webhook_url,
                                 bot_name=bot_name, print_updates=print_updates, testing=testing)

    print("EasyTeleBot created bot '{}' successfully".format(easy_telegram_bot.bot_name))

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
        LoadChat(current_chat)
        current_chat.GotTextMessage(easy_telegram_bot.bot, update.message)
        SaveChat(current_chat)
        return 'ok'

    @easy_telegram_bot.flask_app.route('/set_webhook', methods=['GET', 'POST'])
    def set_webhook():
        print('webhook set')
        webhook_ok = easy_telegram_bot.bot.setWebhook(easy_telegram_bot.webhook_url)
        return "webhook setup - {webhook}".format(webhook='ok' if webhook_ok else 'failed')

    return easy_telegram_bot

