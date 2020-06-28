import random
from abc import ABC
from string import Template

import StringCalculator

from ..BotActionLib import ActionType
from ..BotActionLib.BotActionClass import BotAction
from ..GenericFunctions import RemoveUnreachableTemplateFormats, Data


class Command(BotAction, ABC):
    def __init__(self, act: dict):
        super(Command, self).__init__(act)


class SaveCommand(Command):
    def __init__(self, act: dict):
        super(SaveCommand, self).__init__(act)
        self.save_to_data_name = act['save_to_data_name']
        self.eval = False
        if 'evaluate' in act:
            self.eval = act['evaluate']

    def PerformAction(self, bot, chat, message):
        save_text_format = self.data
        save_text_format = RemoveUnreachableTemplateFormats(save_text_format, chat.data)
        save_text = Template(save_text_format).substitute(chat.data.__dict__)

        chat.data.set_attribute(self.save_to_data_name, save_text)

        # print("data has been changed  ,,,  chat_id - {} , data_name - {} , value={}"
        #       .format(chat.id, self.save_to_data_name, chat.data.get_attribute(self.save_to_data_name)))
        return super(SaveCommand, self).PerformAction(bot, chat, message)


class CalculateCommand(Command):
    def __init__(self, act: dict):
        super(CalculateCommand, self).__init__(act)

    def PerformAction(self, bot, chat, message):
        calculate_text_format = self.data
        calculate_text_format = RemoveUnreachableTemplateFormats(calculate_text_format, chat.data)
        calculate_text = Template(calculate_text_format).substitute(chat.data.__dict__)

        calculate_result = StringCalculator.SolveMathProblem(calculate_text)
        chat.data.set_attribute('calculate_result', calculate_result)

        # print("data has been calculated  ,,,  chat_id - {} , value={}"
        #       .format(chat.id, calculate_result))
        return super(CalculateCommand, self).PerformAction(bot, chat, message)


class RandomCommand(Command):
    def __init__(self, act: dict):
        super(RandomCommand, self).__init__(act)

    def PerformAction(self, bot, chat, message):
        random_data_format = self.data
        random_data_format = RemoveUnreachableTemplateFormats(random_data_format, chat.data)
        random_data = Template(random_data_format).substitute(chat.data.__dict__)

        random_list = random_data.split(',')

        for i in reversed(range(len(random_list)-1)):
            if random_list[i] is None or random_list[i] == "":
                del random_list[i]

        if len(random_list) > 0:
            random_result = random_list[random.randint(0, len(random_list)-1)]
            chat.data.set_attribute('random_result', random_result)
            # print("data has been randomised  ,,,  chat_id - {} , value={}"
            #       .format(chat.id, random_result))
        return super(RandomCommand, self).PerformAction(bot, chat, message)


class RedirectCommand(Command):
    def __init__(self, act: dict):
        super(RedirectCommand, self).__init__(act)

    def PerformAction(self, bot, chat, message):
        redirect_text_format = self.data
        redirect_text_format = RemoveUnreachableTemplateFormats(redirect_text_format, chat.data)
        redirect_text = Template(redirect_text_format).substitute(chat.data.__dict__)
        redirect_text: str

        redirect_id = None
        if redirect_text.isnumeric():
            redirect_id = int(redirect_text)
            if redirect_id == self.id:
                print("tried to redirect to the same redirect action (endless recursion)")
            else:
                redirect_action = None
                for action in chat.bot_actions:
                    if action.id == redirect_id:
                        redirect_action = action
                if isinstance(redirect_action, BotAction):
                    return redirect_action.PerformAction(bot, chat, message)
                    # print("data has been redirected  ,,,  chat_id - {} , redirect_id={}"
                    #       .format(chat.id, redirect_id))
                else:
                    print("performing redirect command , no action id '{}'".format(redirect_id))
        return super(RedirectCommand, self).PerformAction(bot, chat, message)


class IfCommand(Command):
    def __init__(self, act: dict):
        super(IfCommand, self).__init__(act)
        self.true_action_id = int(act["true_action_id"])
        self.false_action_id = int(act["false_action_id"])

    def PerformAction(self, bot, chat, message):
        if_text_format = self.data
        if_text_format = RemoveUnreachableTemplateFormats(if_text_format, chat.data)
        if_text = Template(if_text_format).substitute(chat.data.__dict__)
        if_text: str
        try:
            if_result = eval(if_text, {"builtins": None})
            if isinstance(if_result, bool):
                next_action_id = self.true_action_id if if_result else self.false_action_id
                next_action = None
                for action in chat.bot_actions:
                    if action.id == next_action_id:
                        next_action = action
                if isinstance(next_action, BotAction):
                    next_action.PerformAction(bot, chat, message)
                else:
                    print("performing redirect command , no action id '{}'".format(next_action_id))
            else:
                print("if result is not boolean '{}'".format(if_result))
        except:
            print("could not resolve if data '{}'".format(if_text))
        return super(IfCommand, self).PerformAction(bot, chat, message)


CommandTypeReferenceDictionary = {
    ActionType.SaveCommand: SaveCommand,
    ActionType.CalculateCommand: CalculateCommand,
    ActionType.RandomCommand: RandomCommand,
    ActionType.RedirectCommand: RedirectCommand,
    ActionType.IfCommand: IfCommand,
}
