import copy


class Data(object):
    def has_attribute(self, attr):
        return hasattr(self, attr)

    def __str__(self):
        return str(self.__dict__)

    def set_dictionary(self, dictionary: dict):
        self.__dict__ = dictionary

    def set_attribute(self, name, value):
        self.__setattr__(name, value)

    def get_attribute(self, name):
        return self.__getattribute__(name)


def DecodeUTF8(text: str):
    return text.encode('utf-8').decode()


def RemoveTemplateFormatName(text, format_name) -> str:
    remove_from_index = text.find('${' + format_name + '}')
    return text[:remove_from_index] + text[text.find('}', remove_from_index) + 1:]


def GetTemplateFormatNames(text) -> list:
    names = []
    start_index = text.find('${')
    end_index = text.find('}', start_index)
    while start_index != -1 and end_index != -1:
        names.append(text[start_index + 2:end_index])
        text = text[:start_index] + text[end_index + 1:]
        start_index = text.find('${')
        end_index = text.find('}', start_index)
    return names


def RemoveUnreachableTemplateFormats(text_format: str, dat: Data):
    new_text_format = text_format
    format_names = GetTemplateFormatNames(text_format)
    for format_name in format_names:
        if not dat.has_attribute(format_name):
            new_text_format = RemoveTemplateFormatName(new_text_format, format_name)
    return new_text_format


def JoinDictionariesLists(starting_dict, dominant_dict):
    """ takes the starting_dict and add to it the dominant_dict items
    if values types are different, it saves the dominant value.
    list values are combined.
    dict values are recursive joined by this function.
    :param starting_dict: the starting dict
    :param dominant_dict: the dominant dictionary, if values types are different it saves this dictionary value.
    :return: A combined dictionary of the two.
    """
    result_dic = copy.deepcopy(starting_dict)
    for key in dominant_dict:
        value2 = dominant_dict[key]
        if key in result_dic:
            value1 = result_dic[key]
            type_value1 = type(value1)
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
            result_dic[key] = value2
    return result_dic
