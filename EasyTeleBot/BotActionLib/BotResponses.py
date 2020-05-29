from EasyTeleBot.BotActionLib import BotActionType
from EasyTeleBot.BotActionLib.BotActionClass import BotAction
from EasyTeleBot.Generic import GetFormatNames, Object


class TextResponse(BotAction):
    def PerformAction(self, bot, chat, message):
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
        return super(TextResponse, self).PerformAction(bot, chat, message)

    pass


class AnimationResponse(BotAction):
    def PerformAction(self, bot, chat, message):
        url = self.data.format(data=chat.data)
        if url == "":
            print("act id {} tried sending a null url animation".format(self.id))
            return
        bot.sendAnimation(chat_id=chat.id, animation=url,
                          reply_to_message_id=message.message_id, reply_markup=self.markup)
        return super(AnimationResponse, self).PerformAction(bot, chat, message)


class PhotoResponse(BotAction):
    def PerformAction(self, bot, chat, message):
        return super(PhotoResponse, self).PerformAction(bot, chat, message)
        pass

    pass


ResponseTypeReferenceDictionary = {
    BotActionType.Text: TextResponse,
    BotActionType.Animation: AnimationResponse,
}