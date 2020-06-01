import json

from EasyTeleBot.DatabaseLib.ChatDB import LoadChat, SaveChat
from tests.messageTester import MessageClass, getCustomizedSequence, getSequenceFromActDict, getRandomSequenceFromActDict
from EasyTeleBot.Chat import Chat
from EasyTeleBot import EasyTelegramBot, CreateEasyTelegramBot
import random
from random import randint
import datetime

GarbageTexts = ['bot', 'ok', 'hi', '/start', 'help', 'q1', 'money money money', 'heroku', 'nadav', 'shish kabab']

global actions_currently_testing
actions_currently_testing = []


def getRandText():
    return GarbageTexts[randint(0, len(GarbageTexts) - 1)]


def StartTester():
    smart_seq_total_time = datetime.timedelta()
    garbage_total_time = datetime.timedelta()
    custom_seq_total_time = datetime.timedelta()

    print(random.random())

    config_file = [open('json_file.json'), open('json_file2.json')]

    easy_bot = CreateEasyTelegramBot(config_file, testing=True)

    bot_actions_list = easy_bot.bot_actions
    easy_bot.bot = BotClass()

    chats_count = 1000
    garbage_count = 10
    customized_sequences_count = 1
    smart_sequences_count = 1

    first_messages = [(MessageClass(message_id=randint(10000, 99999), text=getRandText(),
                                    chat_id=randint(1000, 9999999), chat_first_name='ido', chat_last_name='zany'))
                      for _ in range(chats_count)]
    chats = [Chat(easy_bot, msg) for msg in first_messages]
    for chat in chats:
        assert issubclass(type(chat), Chat)
        msg_time = datetime.datetime.now()
        GarbageSender(easy_bot.bot, chat, garbage_count)
        garbage_total_time += datetime.datetime.now() - msg_time

        GarbageSender(easy_bot.bot, chat, 10, text="abiding")  # resets the chat follow_up because of previous garbage

        custom_seq_time = datetime.datetime.now()
        for _ in range(customized_sequences_count):
            LoadChat(chat)
            actions_currently_testing.clear()
            sequence = getCustomizedSequence(random.randint(0, 10000))
            print('new customized sequence - {}'.format(sequence))
            SequenceSender(easy_bot.bot, chat, sequence)
            SaveChat(chat)
        custom_seq_total_time += datetime.datetime.now() - custom_seq_time

        smart_seq_time = datetime.datetime.now()
        for _ in range(smart_sequences_count):
            LoadChat(chat)
            sequence = getRandomSequenceFromActDict(actions_list=bot_actions_list, chat=chat)
            SequenceSender(easy_bot.bot, chat, sequence)
            SaveChat(chat)
        smart_seq_total_time += datetime.datetime.now() - smart_seq_time

    print('chats count {}'.format(chats_count))
    print('garbage msg count {} , time {}'.format(garbage_count, garbage_total_time))
    print('custom seq count {} , time {}'.format(customized_sequences_count, custom_seq_total_time))
    print('smart seq count {} , time {}'.format(smart_sequences_count, smart_seq_total_time))


def GarbageSender(bot, chat: Chat, count: int, text=None):
    messages = None
    if text:
        messages = [MessageClass(message_id=random.randint(10000, 99999), text=text,
                                 chat_id=chat.id, chat_first_name='ido', chat_last_name='zany')
                    for i in range(count)]
    else:
        messages = [MessageClass(message_id=random.randint(10000, 99999), text=getRandText(),
                                 chat_id=chat.id, chat_first_name='ido', chat_last_name='zany')
                    for i in range(count)]
    for msg in messages:
        actions_currently_testing.clear()
        chat.GotTextMessage(bot=bot, message=msg)
        for action in actions_currently_testing:
            print('action by server - {}'.format(action))


def SequenceSender(bot, chat: Chat, sequence):
    global actions_currently_testing
    print('new random sequence formed - {}'.format(sequence))
    actions_currently_testing.clear()
    for text in sequence['texts']:
        print(chat.data.user.first_name)
        chat.GotTextMessage(bot=bot, message=MessageClass(message_id=random.randint(10000, 99999), text=text,
                                                      chat_id=chat.id, chat_first_name='ido',
                                                      chat_last_name='zany'))
    CheckResponseActions(sequence)


def CheckResponseActions(sequence):
    for i in range(len(sequence['responses'])):
        response = sequence['responses'][i]
        if len(actions_currently_testing) > i:
            if 'text' in actions_currently_testing[i] and actions_currently_testing[i]['text'] == response:
                print('checked action for server - {}'.format(actions_currently_testing[i]))
            elif 'animation' in actions_currently_testing[i] and actions_currently_testing[i]['animation'] == response:
                print('checked action for server - {}'.format(actions_currently_testing[i]))
            else:
                print(actions_currently_testing)
                raise Exception("response was not correct '{}' , needed '{}'".format(actions_currently_testing[i], response))
        else:
            raise Exception('fewer actions by server than expected'.format())
    if len(actions_currently_testing) > len(sequence['responses']):
        print('Unexpected Actions ---')
        for i in range(len(sequence['responses']), len(actions_currently_testing), 1):
            print('action by server - {}'.format(actions_currently_testing[i]))
        raise Exception("more responses than expected".format())


class BotClass:
    def sendMessage(self, chat_id=0, text='null', reply_to_message_id=0, reply_markup=[]):
        if not self:
            return
        global actions_currently_testing
        actions_currently_testing.append({
            'action': 'sendMessage',
            'chat_id': chat_id,
            'text': text,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': reply_markup
        })

    def sendAnimation(self, chat_id=0, animation='null', reply_to_message_id=0, reply_markup=[]):
        if not self:
            return
        global actions_currently_testing
        actions_currently_testing.append({
            'action': 'sendAnimation',
            'chat_id': chat_id,
            'animation': animation,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': reply_markup
        })


StartTester()
