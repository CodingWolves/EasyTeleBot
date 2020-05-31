import json
import os

import numpy

from EasyTeleBot.Chat import Chat
from EasyTeleBot.GenericFunctions import Object
from EasyTeleBot.DatabaseLib.pandasDB import DB


chat_db_path = os.environ['PYTHONPATH'].split(';')[0]+'/database/db.csv'


def LoadChat(chat: Chat):
    db = DB(chat_db_path)

    chat_row = db.GetRowByColumnValue('id', chat.id)
    if chat_row is None:
        return
    chat_str = chat_row['data']
    if type(chat_str) is str:
        for key in chat_row.index:
            value = chat_row[key]
            if value != value:
                continue
            if type(value) is numpy.int64:
                value = int(value)
            if type(value) is numpy.float64:
                value = int(value)
            chat[key] = value
        data_dict = json.loads(chat_str)
        chat.data = Object.ConvertDictToObject(data_dict)


def SaveChat(chat: Chat):
    chat_dict = chat.GetAsDict()
    chat_dict['data'] = str(chat_dict['data']).replace('\'', '\"')
    del chat_dict['bot_actions']
    del chat_dict['url']
    db = DB(chat_db_path)

    db.AddRow(chat_dict, important_column='id')
    db.__save__()
    print(chat_dict)
