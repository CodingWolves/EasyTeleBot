import json


def JoinDictionariesLists(dic1, dic2):
    result_dic = dic1
    for key in dic2:
        if key in dic1:
            value1 = dic1[key]
            type_value1 = type(value1)
            value2 = dic2[key]
            type_value2 = type(value2)
            if type_value1 == type_value2:
                if type_value1 is list:
                    result_dic[key] = value1 + value2
                if type_value1 is str:
                    result_dic[key] = value2
                if type_value1 is dict:
                    result_dic[key] = JoinDictionariesLists(value1, value2)
            else:
                result_dic[key] = value2
        else:
            result_dic[key] = dic2[key]
    return result_dic


file_dict = open('json_file.json').read()
file2_dict = open('json_file2.json').read()

file1 = json.loads(file_dict)
file1: dict
file2 = json.loads(file2_dict)
file2: dict

file_joined = JoinDictionariesLists(file1, file2)

actions1 = file1['actions']
actions2 = file2['actions']

actions = actions1 + actions2

print(file_joined)
