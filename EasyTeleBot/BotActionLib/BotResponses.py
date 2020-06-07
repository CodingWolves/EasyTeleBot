from string import Template

from ..BotActionLib import ActionType
from ..BotActionLib.BotActionClass import BotAction
from ..GenericFunctions import RemoveUnreachableTemplateFormats


class TextResponse(BotAction):
    def PerformAction(self, bot, chat, message):
        text_response_format = self.data
        text_response_format = RemoveUnreachableTemplateFormats(text_response_format, chat.data)
        text_response = Template(text_response_format).substitute(chat.data.__dict__)
        if text_response == "":
            print("error - act id {} tried sending an empty text".format(self.id))
        else:
            bot.sendMessage(chat_id=chat.id, text=text_response,
                            reply_to_message_id=message.message_id, reply_markup=self.markup)
        return super(TextResponse, self).PerformAction(bot, chat, message)

    pass


class AnimationResponse(BotAction):
    def PerformAction(self, bot, chat, message):
        url_format = self.data
        url_format = RemoveUnreachableTemplateFormats(url_format, chat.data)
        url = Template(url_format).substitute(chat.data.__dict__)
        if url == "":
            print("act id {} tried sending an empty url animation".format(self.id))
        else:
            bot.sendAnimation(chat_id=chat.id, animation=url,
                              reply_to_message_id=message.message_id, reply_markup=self.markup)
        return super(AnimationResponse, self).PerformAction(bot, chat, message)


class PhotoResponse(BotAction):
    def PerformAction(self, bot, chat, message):
        return super(PhotoResponse, self).PerformAction(bot, chat, message)
        pass

    pass


ResponseTypeReferenceDictionary = {
    ActionType.TextResponse: TextResponse,
    ActionType.AnimationResponse: AnimationResponse,
}
