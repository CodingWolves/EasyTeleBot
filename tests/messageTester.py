from EasyTeleBot.GenericFunctions import Object, RemoveUnreachableFormats
from EasyTeleBot.BotActionLib import ActionType, TextResponse, AnimationResponse, SaveCommand, CalculateCommand
from EasyTeleBot.BotActionLib.BotActionClass import BotAction
from random import randint


class MessageClass(Object):
    def __init__(self, message_id: int, text: str, chat_id: int, chat_first_name: str, chat_last_name: str):
        super(MessageClass, self).__init__()
        self.message_id = message_id
        self.text = text
        self.chat = Object()
        self.chat.id = chat_id
        self.chat.first_name = chat_first_name
        self.chat.last_name = chat_last_name


def getCustomizedSequence(index: int):
    return message_sequences[index % len(message_sequences)]
    pass


def getRandomSequenceFromActDict(actions_list, chat=Object()):
    index = randint(0, len(actions_list) - 1)
    while len(actions_list[index].triggers) == 0:
        index = randint(0, len(actions_list) - 1)
    return getSequenceFromActDict(actions_list, actions_list[index].id, chat=chat)


def getSequenceFromActDict(actions_list, action_id: int, chat=Object(), is_follow_up=False, is_next_act=False):
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
                user_msg = action_class.triggers[randint(0, len(action_class.triggers)-1)]
                user_messages.append(user_msg)
            chat.data.last_text_received = user_msg
            data_formatted = RemoveUnreachableFormats(action_class.data, chat)
            server_msg = data_formatted.format(data=chat.data)
            if server_msg != "":
                server_messages.append(server_msg)
        elif type(action_class) == SaveCommand:
            action_class: SaveCommand
            save_text = action_class.data.format(data=chat.data)
            if 'evaluate' in action_class:
                try:
                    eval_result = eval(save_text)  # very risky move , can be hacked in a second
                    data_name = action_class.save_to_data_name
                    chat.data[data_name] = eval_result
                except:
                    server_messages.append("eval '{}' cannot be evaluated".format(save_text))
                    return {'texts': user_messages, 'responses': server_messages}
            else:
                data_name = action_class.save_to_data_name
                chat.data[data_name] = save_text
        else:
            raise Exception('101')
    else:
        if type(action_class) is SaveCommand:
            action_class: SaveCommand
            chat.data.last_text_received = getRandomInput()
            user_msg = action_class.data.format(data=chat.data)
            user_messages.append(user_msg)
            data_name = action_class.save_to_data_name
            chat.data[data_name] = user_msg.format(data=chat.data)
        elif type(action_class) is CalculateCommand:
            return {'texts': [], 'responses': []}
        else:
            raise Exception('102')

    if is_next_act:
        user_messages.clear()

    if action_class.next_action_id:
        next_act_message = getSequenceFromActDict(actions_list, action_class.next_action_id, chat=chat, is_next_act=True)
        for user_msg in next_act_message['texts']:
            user_messages.append(user_msg)
        for server_msg in next_act_message['responses']:
            server_messages.append(server_msg)

    elif action_class.follow_up_action_id:
        follow_up_act_message = getSequenceFromActDict(actions_list, action_class.follow_up_action_id,
                                                       chat=chat, is_follow_up=True)
        for user_msg in follow_up_act_message['texts']:
            user_messages.append(user_msg)
        for server_msg in follow_up_act_message['responses']:
            server_messages.append(server_msg)

    return {'texts': user_messages, 'responses': server_messages}


def getRandomInput():
    return NamesTemplates[randint(0, len(NamesTemplates)-1)]


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
