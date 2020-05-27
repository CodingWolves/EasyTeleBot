from flask import Flask, request
import telegram
from EasyBot.Chat import Chat
from EasyBot import Act

import io
import json


class EasyBot:

    def __init__(self, actions_file, token=str, url=str):
        if issubclass(type(actions_file), str):
            actions_file = open(actions_file)
        if issubclass(type(actions_file), io):
            actions_text = json.load(actions_file)
        self.acts = Act.InitializeActs(actions_text.actions)

        self.token = actions_text.token
        if token:
            self.token = token

        self.token = actions_text.url
        if url:
            self.url = url

        self.bot = telegram.Bot(token=self.token)
        self.chats = []
        self.print_updates = False

        self.app = Flask(__name__)

        @self.app.route('/{}'.format(self.token), methods=['POST'])
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
            print('set_webhook function')
            webhook_ok = self.bot.setWebhook('{URL}{HOOK}'.format(URL=self.url, HOOK=self.token))
            return "webhook setup - {webhook}".format(webhook='ok' if webhook_ok else 'failed')

    def setPrintAllUpdates(self, print_updates: bool):
        self.print_updates = print_updates
