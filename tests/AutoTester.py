from threading import Thread

from EasyTeleBot.DatabaseLib.ChatDB import LoadChat, SaveChat
from tests.messageTester import MessageClass, getCustomizedSequence, getRandomSequenceFromActDict
from EasyTeleBot.Chat import Chat
from EasyTeleBot.TelegramBot import EasyTelegramBot
import random
from random import randint
import datetime

GarbageTexts = ['bot', 'ok', 'hi', '/start', 'help', 'q1', 'money money money', 'heroku', 'nadav', 'shish kabab']


def getRandText():
    return GarbageTexts[randint(0, len(GarbageTexts) - 1)]


def StartTester(name):
    smart_seq_total_time = datetime.timedelta()
    garbage_total_time = datetime.timedelta()
    custom_seq_total_time = datetime.timedelta()

    print(random.random())

    config_file = [open('json_file.json'), open('json_file2.json')]

    easy_bot = EasyTelegramBot(config_file, testing=True)

    bot_actions_list = easy_bot.bot_actions
    easy_bot.bot = BotClass()

    chats_count = 100
    garbage_count = 10
    customized_sequences_count = 10
    smart_sequences_count = 0

    first_messages = [(MessageClass(message_id=randint(10000, 99999), text=getRandText(),
                                    chat_id=randint(1000, 9999999), chat_first_name='ido', chat_last_name='zany'))
                      for _ in range(chats_count)]
    chats = [Chat(easy_bot, msg) for msg in first_messages]

    file = None
    try:
        file = open("../junk/StartTester_" + name + ".txt", mode="x")
    except:
        file = open("../junk/StartTester_" + name + ".txt", mode="w")

    for chat in chats:
        assert issubclass(type(chat), Chat)
        msg_time = datetime.datetime.now()
        GarbageSender(easy_bot.bot, chat, garbage_count)
        garbage_total_time += datetime.datetime.now() - msg_time

        GarbageSender(easy_bot.bot, chat, 10, text="abiding")  # resets the chat follow_up because of previous garbage

        custom_seq_time = datetime.datetime.now()
        for _ in range(customized_sequences_count):
            LoadChat(chat)
            easy_bot.bot.clear()
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
    file.write('chats count {}'.format(chats_count))
    file.write("\n")
    file.write('garbage msg count {} , time {}'.format(garbage_count, garbage_total_time))
    file.write("\n")
    file.write('custom seq count {} , time {}'.format(customized_sequences_count, custom_seq_total_time))
    file.write("\n")
    file.write('smart seq count {} , time {}'.format(smart_sequences_count, smart_seq_total_time))
    file.write("\n")
    file.write("bot sent " + str(easy_bot.bot.sent_count) + " messages")
    file.write("\n")
    file.close()


def GarbageSender(bot, chat: Chat, count: int, text=None):
    messages = [MessageClass(message_id=random.randint(10000, 99999), text=text if text else getRandText(),
                             chat_id=chat.id, chat_first_name='ido', chat_last_name='zany')
                for _ in range(count)]
    for msg in messages:
        bot.clear()
        chat.GotTextMessage(bot=bot, message=msg)
        for action in bot.sent_list:
            print('action by server - {}'.format(action))


def SequenceSender(bot, chat: Chat, sequence):
    print('new random sequence formed - {}'.format(sequence))
    bot.clear()
    for text in sequence['texts']:
        chat.GotTextMessage(bot=bot, message=MessageClass(message_id=random.randint(10000, 99999), text=text,
                                                          chat_id=chat.id, chat_first_name='ido',
                                                          chat_last_name='zany'))
    CheckResponseActions(bot, sequence)


def CheckResponseActions(bot, sequence):
    for i in range(len(sequence['responses'])):
        response = sequence['responses'][i]
        if len(bot.sent_list) > i:
            if 'text' in bot.sent_list[i] and bot.sent_list[i]['text'] == response:
                print('checked action for server - {}'.format(bot.sent_list[i]))
            elif 'animation' in bot.sent_list[i] and bot.sent_list[i]['animation'] == response:
                print('checked action for server - {}'.format(bot.sent_list[i]))
            else:
                print(bot.sent_list)
                raise Exception(
                    "response was not correct '{}' , needed '{}'".format(bot.sent_list[i], response))
        else:
            raise Exception('fewer actions by server than expected'.format())
    if len(bot.sent_list) > len(sequence['responses']):
        print('Unexpected Actions ---')
        for i in range(len(sequence['responses']), len(bot.sent_list), 1):
            print('action by server - {}'.format(bot.sent_list[i]))
        raise Exception("more responses than expected".format())


class BotClass:
    def __init__(self):
        self.sent_list = []
        self.sent_count = 0

    def clear(self):
        self.sent_list = []

    def sendMessage(self, chat_id=0, text='null', reply_to_message_id=0, reply_markup=[]):
        if not self:
            return
        self.sent_list.append({
            'action': 'sendMessage',
            'chat_id': chat_id,
            'text': text,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': reply_markup
        })
        self.sent_count += 1

    def sendAnimation(self, chat_id=0, animation='null', reply_to_message_id=0, reply_markup=[]):
        if not self:
            return
        self.sent_list.append({
            'action': 'sendAnimation',
            'chat_id': chat_id,
            'animation': animation,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': reply_markup
        })
        self.sent_count += 1


thread_list = []
number_of_threads = 2
for i in range(number_of_threads):
    thread_list.append(Thread(target=StartTester, args=(str(i),), name="StartTester_" + str(i)))

for thread in thread_list:
    thread.start()

for thread in thread_list:
    thread.join()
    print(thread.name + " finished")

# StartTester()
