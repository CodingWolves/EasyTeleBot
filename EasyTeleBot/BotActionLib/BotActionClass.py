from abc import ABC, abstractmethod
from telegram.bot import Bot
from telegram.replykeyboardremove import ReplyKeyboardRemove
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup

from ..BotActionLib import MarkupType


class BotAction(ABC):
    def __init__(self, act: dict):
        self.original_dict = act
        self.id = act['id']
        self.triggers = act['triggers']
        self.data = act['data']

        self.follow_up_action_id = None
        if 'follow_up_action_id' in act:
            self.follow_up_action_id = act['follow_up_action_id']
        self.follow_up_act = None

        self.next_action_id = None
        if 'next_action_id' in act:
            self.next_action_id = act['next_action_id']
        self.next_act = None

        self.markup = None
        if 'markup_type' in act:
            markup_type = act['markup_type']

            if 'markup_data' in act:
                markup_string = act['markup_data']
                # convert it to lists in list
                options = [[item for item in row.split(",")] for row in markup_string.split(":")]

                if markup_type == MarkupType.OneTimeReply:
                    self.markup = ReplyKeyboardMarkup(options, one_time_keyboard=True)
                if markup_type == MarkupType.StaticReply:
                    self.markup = ReplyKeyboardMarkup(options)

            elif act['markup_type'] == MarkupType.Remove:
                self.markup = ReplyKeyboardRemove()
            else:
                print('error 15')  # act is not correct , markup_type exist and not 'Remove' but no markup_data

    def isTriggeredBy(self, text_message: str) -> bool:
        return text_message in self.triggers

    @abstractmethod
    def PerformAction(self, bot: Bot, chat, message):
        result = None
        print("doing super() in act - {}".format(self.id))
        if self.follow_up_act:
            print("follow_up_act has been sent - {} from act - {}".format(self.follow_up_action_id, self.id))
            result = self.follow_up_act
        if self.next_action:
            print("next_act has been sent - {} from act - {}".format(self.next_action_id, self.id))
            result = self.next_act.PerformAction(bot, chat, message)
        print("sending")
        print(result)
        print("sent")
        return result
