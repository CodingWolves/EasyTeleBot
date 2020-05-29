from EasyTeleBot.BotActionLib.BotActionClass import BotAction
from EasyTeleBot.BotActionLib.BotActionTypes import *
from EasyTeleBot.BotActionLib.BotResponses import *
from EasyTeleBot.BotActionLib.BotCommands import *


def CreateBotActionsList(actions_list: []):
    bot_actions: []
    if actions_list is None and issubclass(type(actions_list), list):
        raise Exception("could not initialize bot actions - '{}' need to be a list".format(actions_list))
    print("<<<<<<<<<<!!!Acts Creation Started!!!>>>>>>>>>>")
    bot_actions = [CreateBotActionFromDict(act_dict) for act_dict in actions_list]
    return bot_actions


def CreateBotActionFromDict(action_dict: dict):
    print("Creating BotAction with id - {}".format(action_dict['id']))

    action_type = action_dict['type']

    # searches action_type in the commands list, if found use the command type to create a new action
    if action_type in CommandTypeReferenceDictionary:
        command_class = CommandTypeReferenceDictionary[action_type]
        return command_class(action_dict)

    # searches action_type in the responses list, if found use the command type to create a new action
    if action_type in ResponseTypeReferenceDictionary:
        command_class = ResponseTypeReferenceDictionary[action_type]
        return command_class(action_dict)


def GetBotActionByTrigger(actions_list: list, trigger: str):
    for action in actions_list:
        if action.isTriggeredBy(trigger):
            return action
    print("did not find an Act by trigger - '{}'".format(trigger))


def GetBotActionById(actions_list: list, action_id: int):
    for action in actions_list:
        if action.id == action_id:
            return action
    print("did not find an Act by id - '{}'".format(action_id))
