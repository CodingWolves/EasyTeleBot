from abc import ABC

from EasyTeleBot.BotActionLib import BotActionType
from EasyTeleBot.BotActionLib.BotActionClass import BotAction
from EasyTeleBot.Generic import DecodeUTF8


class Command(BotAction, ABC):
    def __init__(self, act: dict):
        super(Command, self).__init__(act)
        pass

    pass


class SaveCommand(Command):
    def __init__(self, act: dict):
        super(SaveCommand, self).__init__(act)
        self.data_name = act['save_to_data_name']
        self.eval = False
        if 'evaluate' in act:
            self.eval = act['evaluate']

    def PerformAction(self, bot, chat, message):
        text_message = DecodeUTF8(message.text)
        save_text = self.data.format(text_message=text_message, data=chat.data)

        if self.eval:
            try:
                data = chat.data
                eval_result = eval(save_text)  # very risky move , can be hacked in a second , suck as "()"*8**5
                # [i for i in range(10**100)] crashes the app
                chat.data[self.data_name] = eval_result
            except:
                print("eval '{}' cannot be evaluated chat_id={} ".format(save_text, chat.id))
                bot.sendMessage(chat_id=chat.id,
                                text="eval '{}' cannot be evaluated".format(save_text),
                                reply_to_message_id=message.message_id)
                return
        else:
            chat.data[self.data_name] = save_text

        print("data has been changed  ,,,  chat_id - {} , data_name - {} , value={}"
              .format(chat.id, self.data_name, chat.data[self.data_name]))
        return super(SaveCommand, self).PerformAction(bot, chat, message)


CommandTypeReferenceDictionary = {
    BotActionType.SaveCommand: SaveCommand,
}