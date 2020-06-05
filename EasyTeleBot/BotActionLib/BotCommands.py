import random
from abc import ABC

import StringCalculator

from ..BotAction import GetBotActionById
from ..BotActionLib import ActionType
from ..BotActionLib.BotActionClass import BotAction
from ..GenericFunctions import RemoveUnreachableFormats


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
        save_text_format = RemoveUnreachableFormats(save_text_format, chat)
        save_text = save_text_format.format(data=chat.data)

        if self.eval:
            try:
                data = chat.data
                eval_result = eval(save_text)  # very risky move , can be hacked in a second , suck as "()"*8**5
                # [i for i in range(10**100)] crashes the app
                chat.data[self.save_to_data_name] = eval_result
            except:
                print("eval '{}' cannot be evaluated chat_id={} ".format(save_text, chat.id))
                bot.sendMessage(chat_id=chat.id,
                                text="eval '{}' cannot be evaluated".format(save_text),
                                reply_to_message_id=message.message_id)
                return
        else:
            chat.data[self.save_to_data_name] = save_text

        print("data has been changed  ,,,  chat_id - {} , data_name - {} , value={}"
              .format(chat.id, self.save_to_data_name, chat.data[self.save_to_data_name]))
        return super(SaveCommand, self).PerformAction(bot, chat, message)


class CalculateCommand(Command):
    def __init__(self, act: dict):
        super(CalculateCommand, self).__init__(act)

    def PerformAction(self, bot, chat, message):
        calculate_text_format = self.data
        calculate_text_format = RemoveUnreachableFormats(calculate_text_format, chat)
        calculate_text = calculate_text_format.format(data=chat.data)

        calculate_result = StringCalculator.SolveMathProblem(calculate_text)
        chat.data['calculate_result'] = calculate_result

        print("data has been calculated  ,,,  chat_id - {} , value={}"
              .format(chat.id, calculate_result))
        return super(CalculateCommand, self).PerformAction(bot, chat, message)


class RandomCommand(Command):
    def __init__(self, act: dict):
        super(RandomCommand, self).__init__(act)

    def PerformAction(self, bot, chat, message):
        random_data_format = self.data
        random_data_format = RemoveUnreachableFormats(random_data_format, chat)
        random_data = random_data_format.format(data=chat.data)

        random_list = random_data.split(',')
        empties_index_list = []

        for i in range(len(random_list)):
            if random_list[i] is None or random_list[i] == "":
                empties_index_list.append(i)

        for i in reversed(empties_index_list):
            del random_list[i]

        if len(random_list) > 0:
            random_result = random_list[random.randint(0, len(random_list)-1)]
            chat.data['random_result'] = random_result
            print("data has been randomised  ,,,  chat_id - {} , value={}"
                  .format(chat.id, random_result))
        return super(RandomCommand, self).PerformAction(bot, chat, message)


class RedirectCommand(Command):
    def __init__(self, act: dict):
        super(RedirectCommand, self).__init__(act)

    def PerformAction(self, bot, chat, message):
        redirect_text_format = self.data
        redirect_text_format = RemoveUnreachableFormats(redirect_text_format, chat)
        redirect_text = redirect_text_format.format(data=chat.data)

        redirect_id = None
        try:
            redirect_id = int(redirect_text)
        finally:
            if type(redirect_id) is int:
                if redirect_id == self.id:
                    print("tried to redirect to the same redirect action (endless recursion)")
                else:
                    next_action = GetBotActionById(chat.bot_actions, redirect_id)
                    if type(next_action) is BotAction:
                        next_action.Perform(bot, chat, message)
                        print("data has been redirected  ,,,  chat_id - {} , value={}"
                              .format(chat.id, self.next_action_id))
                    else:
                        print("performing redirect command , no action id '{}'".format(redirect_id))
        return super(RedirectCommand, self).PerformAction(bot, chat, message)


CommandTypeReferenceDictionary = {
    ActionType.SaveCommand: SaveCommand,
    ActionType.CalculateCommand: CalculateCommand,
    ActionType.RandomCommand: RandomCommand,
    ActionType.RedirectCommand: RedirectCommand
}
