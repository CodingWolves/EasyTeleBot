from abc import ABC

import StringCalculator

from EasyTeleBot.BotActionLib import ActionType
from EasyTeleBot.BotActionLib.BotActionClass import BotAction
from EasyTeleBot.GenericFunctions import DecodeUTF8, RemoveUnreachableFormats


class Command(BotAction, ABC):
    def __init__(self, act: dict):
        super(Command, self).__init__(act)
        pass

    pass


class SaveCommand(Command):
    def __init__(self, act: dict):
        super(SaveCommand, self).__init__(act)
        self.save_to_data_name = act['save_to_data_name']
        self.eval = False
        if 'evaluate' in act:
            self.eval = act['evaluate']

    def PerformAction(self, bot, chat, message):
        text_message = DecodeUTF8(message.text)
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
        text_message = DecodeUTF8(message.text)
        calculate_text_format = self.data
        calculate_text_format = RemoveUnreachableFormats(calculate_text_format, chat)
        calculate_text = calculate_text_format.format(data=chat.data)

        calculate_result = StringCalculator.SolveMathProblem(calculate_text)
        chat.data['calculate_result'] = calculate_result

        print("data has been calculated  ,,,  chat_id - {} , value={}"
              .format(chat.id, chat.data['calculate_result']))
        return super(CalculateCommand, self).PerformAction(bot, chat, message)


CommandTypeReferenceDictionary = {
    ActionType.SaveCommand: SaveCommand,
    ActionType.CalculateCommand: CalculateCommand,
}