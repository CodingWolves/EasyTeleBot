from EasyTeleBot.BotActionLib import GetBotActionByTrigger
from EasyTeleBot.Generic import Object


class Chat:
    def __init__(self, easy_bot, message):
        self.id = message.chat.id
        self.url = easy_bot.base_url
        self.bot_actions = easy_bot.bot_actions
        self.data = Object()
        self.data.user = Object()
        self.data.user.first_name = message.chat.first_name
        self.data.user.last_name = message.chat.last_name
        self.follow_up_bot_action = False
        self.unhandled_messages = []

    def GotMessage(self, bot, message):
        text = message.text.encode('utf-8').decode()
        print("chat - {chat_id} got text_message = {text_message}".format(chat_id=self.id, text_message=text))
        print("chat continue , follow_up_act={follow_up_act}".format(follow_up_act=self.follow_up_bot_action))
        if self.follow_up_bot_action:
            print("found previous follow_up_act {id} , now acting".format(id=self.follow_up_bot_action.id))
            self.follow_up_bot_action = self.follow_up_bot_action.PerformAction(bot, self, message)
            return

        print("after follow_up_act")

        act = GetBotActionByTrigger(self.bot_actions, text)
        if act is not None:
            print("doing act - {id} after text = {text}".format(id=act.id, text=text))
            self.follow_up_bot_action = act.PerformAction(bot, self, message)
            if self.follow_up_bot_action:
                print("got follow_up_act - {}".format(self.follow_up_bot_action.id))

        print("end GotMessage")
