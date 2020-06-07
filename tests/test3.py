import random
from datetime import datetime

from EasyTeleBot.DatabaseLib.ChatDB import LoadChat, SaveChat
from EasyTeleBot.DatabaseLib.pandasDB import DB
from EasyTeleBot.GenericFunctions import Data

chat = Data()
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

random_data = ",,,,1,,,2,3,,4,5,,,"

random_list = random_data.split(',')
random_result = None

empties_index_list = []

for i in range(len(random_list)):
    if random_list[i] is None or random_list[i] == "":
        empties_index_list.append(i)

for i in reversed(empties_index_list):
    del random_list[i]

print(random_list)
random_result = random_list[random.randint(0, len(random_list)-1)]
print(random_result)
