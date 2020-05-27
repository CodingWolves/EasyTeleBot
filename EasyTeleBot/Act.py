from abc import ABC, abstractmethod
from telegram.bot import Bot
from telegram.replykeyboardremove import ReplyKeyboardRemove
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup

from EasyTeleBot.ActionTypes import *
from EasyTeleBot.Generic import GetFormatNames, Object


def InitializeActs(acts_list: []):
    acts: []
    if acts_list is None and issubclass(type(acts_list), list):
        raise Exception('could not initialize acts - {}'.format(acts_list))
    print("<<<<<<<<<<!!!Acts Created!!!>>>>>>>>>>")
    acts = [Act.CreateAct(act_dict) for act_dict in acts_list]
    return acts


class Act(ABC):
    @classmethod
    def CreateAct(cls, act: dict):
        print("Creating Act {}".format(act['id']))
        if act['type'] == ActType.Text:
            return TextResponse(act)
        elif act['type'] == ActType.Animation:
            return AnimationResponse(act)
        elif act['type'] == ActType.SaveCommand:
            return SaveCommand(act)

    @classmethod
    def getActByTrigger(cls, acts: list, trigger: str):
        for act in acts:
            if act.isTriggeredBy(trigger):
                return act
        print("did not find an Act for trigger {trigger}".format(trigger=trigger))

    @classmethod
    def getActById(cls, acts: list, act_id: int):
        for act in acts:
            if act.id == act_id:
                act: Act
                return act

    def __init__(self, act: dict):
        self.original_dict = act
        self.id = act['id']
        self.triggers = act['triggers']
        self.data = act['data']
        self.markup = None

        self.follow_up_act_id = None
        if 'follow_up_act_id' in act:
            self.follow_up_act_id = act['follow_up_act_id']

        self.next_act_id = None
        if 'next_act_id' in act:
            self.next_act_id = act['next_act_id']

        if 'markup_type' in act:
            markup_type = act['markup_type']

            if 'markup_data' in act:
                markup_string = act['markup_data']
                options = [[item for item in row.split(",")] for row in
                           markup_string.split(":")]  # convert it to lists in list

                if markup_type == MarkupType.OneTimeReply:
                    self.markup = ReplyKeyboardMarkup(options, one_time_keyboard=True)
                if markup_type == MarkupType.StaticReply:
                    self.markup = ReplyKeyboardMarkup(options)

            elif act['markup_type'] == MarkupType.Remove:
                self.markup = ReplyKeyboardRemove()
            else:
                print('error 15')  # act is not correct , markup_type exist and not 'Remove' but no markup_data
                pass
        pass

    def isTriggeredBy(self, text_message: str) -> bool:
        return text_message in self.triggers

    @abstractmethod
    def doAct(self, bot: Bot, chat, message):
        result = None
        print("doing super() in act - {}".format(self.id))
        if self.follow_up_act_id:
            print("follow_up_act_id has been sent - {follow_up_act_id} from act - {act_id}".format(
                follow_up_act_id=self.follow_up_act_id, act_id=self.id))
            result = Act.getActById(chat.acts, self.follow_up_act_id)
        if self.next_act_id:
            print("next_act has been sent - {next_act_id} from act - {act_id}".format(next_act_id=self.next_act_id,
                                                                                      act_id=self.id))
            result = Act.getActById(chat.acts, self.next_act_id).doAct(bot, chat, message)
        print("sending")
        print(result)
        print("sent")
        return result


class TextResponse(Act):
    def doAct(self, bot: Bot, chat, message):
        format_names = GetFormatNames(self.data)
        print('found formant_name ')
        print(format_names)
        print("chat.data")
        print(chat.data)
        for name in format_names:
            if not Object.hasAttrNested(chat, name):
                print("error - trying to find {format_name} in chat.data but not found , chat_id={chat_id}".format(
                    format_name=name.split('.', 1)[1], chat_id=chat.id))
                bot.sendMessage(chat_id=chat.id, text='error - {} not found in Chat'.format(name),
                                reply_to_message_id=message.message_id)
                return
        text = self.data.format(data=chat.data)
        if text == "":
            print("error - act id {} tried sending a null text".format(self.id))
            return
        bot.sendMessage(chat_id=chat.id, text=text,
                        reply_to_message_id=message.message_id, reply_markup=self.markup)
        return super(TextResponse, self).doAct(bot, chat, message)

    pass


class AnimationResponse(Act):
    def doAct(self, bot: Bot, chat, message):
        url = self.data.format(URL=URL, data=chat.data)
        if url == "":
            print("act id {} tried sending a null url animation".format(self.id))
            return
        bot.sendAnimation(chat_id=chat.id, animation=url,
                          reply_to_message_id=message.message_id, reply_markup=self.markup)
        return super(AnimationResponse, self).doAct(bot, chat, message)
        pass

    pass


class PhotoResponse(Act):
    def doAct(self, bot: Bot, chat, message):
        return super(PhotoResponse, self).doAct(bot, chat, message)
        pass

    pass


class Command(Act, ABC):
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

    def doAct(self, bot: Bot, chat, message):
        text_message = GetTextFromMessage(message)
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
        return super(SaveCommand, self).doAct(bot, chat, message)


def GetTextFromMessage(message):
    return message.text.encode('utf-8').decode()
