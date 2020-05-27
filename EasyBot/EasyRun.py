from flask import Flask, request
import telegram
from EasyBot.Chat import Chat
from EasyBot import Act

import io
import json
from urllib import parse


class EasyBot:

    def __init__(self, config_file, telegram_token=None, webhook_url=None, bot_name=None):
        config_text = None
        if issubclass(type(config_file), str):
            config_file = open(config_file)
        if issubclass(type(config_file), io.IOBase):
            config_text = json.load(config_file)

        print("read config file - {}".format(config_text))

        if not config_text:
            raise Exception("could not initialize EasyBot from config file")

        self.acts = Act.InitializeActs(config_text['actions'])

        self.telegram_token = config_text['telegram_token']
        if telegram_token:
            self.telegram_token = telegram_token

        self.webhook_url = config_text['webhook_url']
        if webhook_url:
            self.webhook_url = webhook_url

        url = parse.urlparse(self.webhook_url)
        if not url.scheme or not url.netloc:
            raise Exception('EasyBot need to get webhook with http:// or https:// , got {}'.format(self.webhook_url))
        self.webhook_base_url = url.scheme + "//" + url.netloc + "/"
        self.webhook_url_path = url.path
        print(self.webhook_url_path)

        self.bot_name = config_text['bot_name']
        if bot_name:
            self.bot_name = bot_name

        self.bot = telegram.Bot(token=self.telegram_token)
        self.chats = []
        self.print_updates = False

        if not self.telegram_token or not self.acts or not self.webhook_url or not self.bot_name:
            raise Exception("could not initialize EasyBot , missing parameter token={} acts={} url={}"
                            .format(self.telegram_token, self.acts, self.webhook_url))

        self.set_webhook()
        self.app = Flask(__name__)

        print("EasyBot created bot '{}' successfully".format(config_text['bot_name']))

        @self.app.route(self.webhook_url_path, methods=['POST'])
        def respond():
            update = telegram.Update.de_json(request.get_json(force=True), self.bot)
            if self.print_updates:
                print(update)
            if update.callback_query:  # button menu pressed
                return 'ok'
            if update.edited_message:
                return 'ok'
            if update.message and update.message.document:
                return 'ok'
            current_chat = False
            for chat in self.chats:  # searches if chat has previous records
                if chat.id == update.message.chat.id:
                    current_chat = chat
                    break
            if not current_chat:
                current_chat = Chat(self, update.message)  # creates a new chat
                print("New chat added id = {}".format(update.message.chat.id))
                self.chats.append(current_chat)
            current_chat.GotMessage(self.bot, update.message)
            return 'ok'

        @self.app.route('/set_webhook', methods=['GET', 'POST'])
        def set_webhook():
            print('webhook set')
            webhook_ok = self.set_webhook()
            return "webhook setup - {webhook}".format(webhook='ok' if webhook_ok else 'failed')

    def setPrintAllUpdates(self, print_updates: bool):
        self.print_updates = print_updates

    def set_webhook(self):
        return self.bot.setWebhook(self.webhook_url)
