from datetime import datetime

from EasyTeleBot.DatabaseLib.ChatDB import LoadChat, SaveChat
from EasyTeleBot.DatabaseLib.pandasDB import DB
from EasyTeleBot.GenericFunctions import Object

chat = Object()
chat.id = 2

time = datetime.now()
LoadChat(chat)
print(chat)
time = datetime.now() - time
print(time)

chat.bot_actions = ""
chat.url = ""

time = datetime.now()
SaveChat(chat)
time = datetime.now() - time
print(time)


print("load2")
time = datetime.now()
LoadChat(chat)
print(chat)
time = datetime.now() - time
print(time)
