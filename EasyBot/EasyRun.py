from flask import Flask, request
import telegram
from EasyBot.Chat import Chat
from EasyBot import Act

import io
import json


class EasyBot:

    def __init__(self, config_file, token=None, url=None, bot_name=None):
        config_text = None
        if issubclass(type(config_file), str):
            config_file = open(config_file)
        if issubclass(type(config_file), io.IOBase):
            config_text = json.load(config_file)

        print("read config file - {}".format(config_text))

        if not config_text:
            raise Exception("could not initialize EasyBot from config file")

        self.acts = Act.InitializeActs(config_text['actions'])

        self.token = config_text['token']
        if token:
            self.token = token

        self.url = config_text['url']
        if url:
            self.url = url

        self.bot_name = config_text['bot_name']
        if bot_name:
            self.bot_name = bot_name

        self.bot = telegram.Bot(token=self.token)
        self.chats = []
        self.print_updates = False

        if not self.token or not self.acts or not self.url or not self.bot_name:
            raise Exception("could not initialize EasyBot , missing parameter token={} acts={} url={}"
                            .format(self.token, self.acts, self.url))

        self.set_webhook()
        self.app = Flask(__name__)

        print("EasyBot created bot '{}' successfully".format(config_text['bot_name']))

        @self.app.route('/{}'.format(self.token), methods=['POST'])
        def respond():
            print('Got Respond')
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
            print('set_webhook function')
            webhook_ok = self.set_webhook()
            return "webhook setup - {webhook}".format(webhook='ok' if webhook_ok else 'failed')

    def setPrintAllUpdates(self, print_updates: bool):
        self.print_updates = print_updates

    def set_webhook(self):
        return self.bot.setWebhook('{URL}{HOOK}'.format(URL=self.url, HOOK=self.token))

    def run(self, host=None, port=None, debug=None, load_dotenv=None):
        print("host={}, port={}, debug={}, load_dotenv={}".format(host=host, port=port, debug=debug, load_dotenv=load_dotenv))
        self.app.run(host=host, port=port, debug=debug, load_dotenv=load_dotenv)
