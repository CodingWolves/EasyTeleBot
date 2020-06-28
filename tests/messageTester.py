from string import Template

from EasyTeleBot.GenericFunctions import Data, RemoveUnreachableTemplateFormats
from EasyTeleBot.BotAction import *
from EasyTeleBot.BotActionLib.BotActionClass import BotAction
from random import randint


class MessageClass:
    def __init__(self, message_id: int, text: str, chat_id: int, chat_first_name: str, chat_last_name: str):
        super(MessageClass, self).__init__()
        self.message_id = message_id
        self.text = text
        self.chat = Data()
        self.chat.id = chat_id
        self.chat.first_name = chat_first_name
        self.chat.last_name = chat_last_name


def getCustomizedSequence(index: int):
    return message_sequences[index % len(message_sequences)]
    pass


def getRandomSequenceFromActDict(actions_list, chat=Data()):
    index = randint(0, len(actions_list) - 1)
    while len(actions_list[index].triggers) == 0:
        index = randint(0, len(actions_list) - 1)
    return getSequenceFromActDict(actions_list, actions_list[index].id, chat=chat)


def getSequenceFromActDict(actions_list, action_id: int, chat=Data(), is_follow_up=False, is_next_act=False):
    action_class = None
    action_class: BotAction
    for act in actions_list:
        if act.id == action_id:
            action_class = act
            break
    if not action_class:
        raise Exception('cant find id - {}'.format(action_id))
    print('action_id - {} , is_follow_up - {} , chat - {}'.format(action_id, is_follow_up, chat))

    user_messages = []
    server_messages = []
    if not is_follow_up:
        if type(action_class) is TextResponse or type(action_class) is AnimationResponse:
            user_msg = None
            if len(action_class.triggers) > 0:
                user_msg = action_class.triggers[randint(0, len(action_class.triggers) - 1)]
                user_messages.append(user_msg)
            chat.data.last_text_received = user_msg
            data_formatted = RemoveUnreachableTemplateFormats(action_class.data, chat.data)
            server_msg = Template(data_formatted).substitute(chat.data.__dict__)
            if server_msg != "":
                server_messages.append(server_msg)
        elif type(action_class) == SaveCommand:
            action_class: SaveCommand
            save_text = Template(action_class.data).substitute(chat.data.__dict__)
            data_name = action_class.save_to_data_name
            chat.data.set_attribute(data_name, save_text)
        elif isinstance(action_class, CalculateCommand):
            pass
        elif isinstance(action_class, RandomCommand):
            pass
        elif isinstance(action_class, RedirectCommand):
            pass
        else:
            raise Exception('101')
    else:
        if type(action_class) is SaveCommand:
            action_class: SaveCommand
            chat.data.last_text_received = getRandomInput()
            user_msg = Template(action_class.data).substitute(chat.data.__dict__)
            user_messages.append(user_msg)
            data_name = action_class.save_to_data_name
            chat.data.set_attribute(data_name, Template(user_msg).substitute(chat.data.__dict__))
        elif type(action_class) is CalculateCommand:
            return {'texts': [], 'responses': []}
        else:
            raise Exception('102')

    if is_next_act:
        user_messages.clear()

    if action_class.next_action_id:
        next_action_message = getSequenceFromActDict(actions_list, action_class.next_action_id, chat=chat,
                                                     is_next_act=True)
        for user_msg in next_action_message['texts']:
            user_messages.append(user_msg)
        for server_msg in next_action_message['responses']:
            server_messages.append(server_msg)

    elif action_class.follow_up_action_id:
        follow_up_action_message = getSequenceFromActDict(actions_list, action_class.follow_up_action_id,
                                                          chat=chat, is_follow_up=True)
        for user_msg in follow_up_action_message['texts']:
            user_messages.append(user_msg)
        for server_msg in follow_up_action_message['responses']:
            server_messages.append(server_msg)

    return {'texts': user_messages, 'responses': server_messages}


def getRandomInput():
    return NamesTemplates[randint(0, len(NamesTemplates) - 1)]


NamesTemplates = ['ido', 'nadav', 'gal', 'ben', 'alon', 'adi', 'omer', 'inbal', 'shir', 'dor']

message_sequences = [
    {'texts': ['ask me my name', 'cookie'],
     'responses': ['what is your name?', 'your name is cookie']
     },
    {'texts': ['fuck', 'hello'],
     'responses': ['hello to you too', 'server says hello back', 'server got to this action right after action id 1, '
                                                                 'now you got markup options']
     },
    {'texts': ["ok", "okay", "OK", "Ok"],
     'responses': ['OK', 'OK', 'OK', 'OK']
     },
    {'texts': ["math", "1+1"],
     'responses': ['enter math expression', '2.0']
     },
    {'texts': ["123456"],
     'responses': ['hello to you too']
     },

]
