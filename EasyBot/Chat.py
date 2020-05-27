from EasyBot.Act import Act
from EasyBot.Generic import Object


class Chat:
    def __init__(self, easy_bot, message):
        self.id = message.chat.id
        self.url = easy_bot.base_url
        self.acts = easy_bot.acts
        self.data = Object()
        self.data.user = Object()
        self.data.user.first_name = message.chat.first_name
        self.data.user.last_name = message.chat.last_name
        self.follow_up_act = False
        self.unhandled_messages = []

    def GotMessage(self, bot, message):
        text = message.text.encode('utf-8').decode()
        print("chat - {chat_id} got text_message = {text_message}".format(chat_id=self.id, text_message=text))
        print("chat continue , follow_up_act={follow_up_act}".format(follow_up_act=self.follow_up_act))
        if self.follow_up_act:
            print("found previous follow_up_act {id} , now acting".format(id=self.follow_up_act.id))
            self.follow_up_act = self.follow_up_act.doAct(bot, self, message)
            return
            pass

        print("after follow_up_act")

        act = Act.getActByTrigger(self.acts, text)
        if issubclass(type(act), Act):
            print("doing act - {id} after text = {text}".format(id=act.id, text=text))
            follow_up_act = act.doAct(bot, self, message)
            if follow_up_act:
                print("got follow_up_act - {act_id}".format(act_id=follow_up_act.id))
                self.follow_up_act = follow_up_act
                print("setting as Chat.follow_up_act - now follow up id is {}".format(self.follow_up_act.id))

        print("end GotMessage")
