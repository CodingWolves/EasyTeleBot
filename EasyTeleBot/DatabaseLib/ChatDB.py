import json
import os

import numpy
from pandas import DataFrame

from EasyTeleBot.Chat import Chat
from EasyTeleBot.GenericFunctions import Object
from EasyTeleBot.DatabaseLib.pandasDB import DB


chat_db_path = os.environ['PYTHONPATH'].split(';')[0]+'/database/db.csv'


def LoadChat(chat: Chat):
    if 'db_row' in chat and chat.db_row is not None:
        chat_row = DB.GetChatOnlyRow(chat_db_path, chat)
    else:
        db = DB(chat_db_path)
        chat_row = db.GetRowByColumnValue('id', chat.id)
    chat_row: DataFrame
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
            elif type(value) is numpy.float64:
                value = int(value)
            elif value == "False":
                value = False
            elif value == "True":
                value = True
            chat[key] = value
        data_dict = json.loads(chat_str)
        chat.data = Object.ConvertDictToObject(data_dict)
        if 'db_row' not in chat or chat.db_row is None:
            chat.db_row = chat_row.name


def SaveChat(chat: Chat):
    chat_dict = chat.GetAsDict()
    chat_dict['data'] = str(chat_dict['data']).replace('\'', '\"')
    del chat_dict['bot_actions']
    del chat_dict['url']
    del chat_dict['db_row']
    db = DB(chat_db_path)
    db.data: DataFrame

    db.AddRow(chat_dict, important_column='id')
    db.__save__()
    # db.data.to_json(os.environ['PYTHONPATH'].split(';')[0]+'/database/db.json')
    print(chat_dict)
