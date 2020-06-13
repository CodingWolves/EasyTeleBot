import copy
import json
import os
from threading import Lock

import numpy
from pandas import DataFrame

from ..Chat import Chat
from ..GenericFunctions import Data
from ..DatabaseLib.pandasDB import DB


chat_db_path = os.environ['PYTHONPATH'].split(';')[0]+'/database/db.csv'

chat_db_lock = Lock()


def LoadChat(chat: Chat):
    chat_db_lock.acquire()
    if hasattr(chat, 'db_row') and chat.db_row is not None:
        chat_row = DB.GetChatOnlyRow(chat_db_path, chat)
    else:
        db = DB(chat_db_path)
        chat_row = db.GetRowByColumnValue('id', chat.id)
    chat_db_lock.release()
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
            chat.__setattr__(key, value)
        data_dict = json.loads(chat_str)
        chat.data = Data()
        chat.data.set_dictionary(data_dict)
        if not hasattr(chat, 'db_row') or chat.db_row is None:
            chat.db_row = chat_row.name


def SaveChat(chat: Chat):
    chat_dict = copy.deepcopy(chat.__dict__)
    chat_dict['data'] = str(chat_dict['data']).replace('\'', '\"')
    del chat_dict['bot_actions']
    del chat_dict['url']
    del chat_dict['db_row']

    chat_db_lock.acquire()
    db = DB(chat_db_path)
    db.AddRow(chat_dict, important_column='id')
    db.__save__()
    # db.data.to_json(os.environ['PYTHONPATH'].split(';')[0]+'/database/db.json')
    chat_db_lock.release()

    # print(chat_dict)
