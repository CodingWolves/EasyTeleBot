from EasyTeleBot.BotActionLib import GetBotActionByTrigger, GetBotActionById
from EasyTeleBot.GenericFunctions import Object, DecodeUTF8


class Chat(Object):
    def __init__(self, easy_bot, message):
        super(Chat, self).__init__()
        self.id = message.chat.id
        self.url = easy_bot.base_url
        self.bot_actions = easy_bot.bot_actions
        self.data = Object()
        self.data.user = Object()
        self.data.user.first_name = message.chat.first_name
        self.data.user.last_name = message.chat.last_name
        self.follow_up_bot_action_id = False

    def GotTextMessage(self, bot, message):
        text_received = DecodeUTF8(message.text)
        self.data.last_text_received = text_received
        print("chat - {} got text_message = {}".format(self.id, text_received))
        print("follow_up_act={}".format(self.follow_up_bot_action_id))
        if self.follow_up_bot_action_id:
            print("found previous follow_up_act {id} , now acting".format(id=self.follow_up_bot_action_id))
            current_action = GetBotActionById(self.bot_actions, self.follow_up_bot_action_id)
            follow_up_action = current_action.PerformAction(bot, self, message)
            if follow_up_action:
                self.follow_up_bot_action_id = follow_up_action.id
                print("got another follow_up_act - {}".format(self.follow_up_bot_action_id))
            else:
                self.follow_up_bot_action_id = False
            return

        print("searching for action by trigger")

        bot_action = GetBotActionByTrigger(self.bot_actions, text_received)
        if bot_action is not None:
            print("doing act - {id} after text = {text}".format(id=bot_action.id, text=text_received))
            follow_up_action = bot_action.PerformAction(bot, self, message)
            if follow_up_action:
                self.follow_up_bot_action_id = follow_up_action.id
                print("got follow_up_act - {}".format(self.follow_up_bot_action_id))
            else:
                self.follow_up_bot_action_id = False

        print("end GotMessage")
