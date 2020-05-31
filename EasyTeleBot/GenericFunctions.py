class Object(object):
    def __init__(self):
        super(Object, self).__setattr__('_attributes', [])

    def __setattr__(self, key, value):
        super(Object, self).__setattr__(key, value)
        if key not in self._attributes:
            self._attributes.append(key)

    def __setitem__(self, key, value):
        if issubclass(type(key), str):
            if key not in self._attributes:
                self._attributes.append(key)
            super(Object, self).__setattr__(key, value)
        elif issubclass(type(key), int):
            key: int
            if 'list' not in self._attributes or not issubclass(type(self.list), list):
                self.__setattr__('list', [])
            self.list: list
            while len(self.list) <= key:
                self.list.append(None)
            self.list[key] = value

    def __getitem__(self, item):
        if issubclass(type(item), str):
            return super(Object, self).__getattribute__(item)
        elif issubclass(type(item), int):
            if 'list' in self._attributes and issubclass(type(self.list), list):
                if item < len(self.list):
                    return self.list[item]
                else:
                    return None
            else:
                raise KeyError("list has not been set")
        else:
            raise KeyError("'{}' is not string nor int ".format(item))

    def __iter__(self):
        for item in self._attributes:
            yield item

    def __str__(self):
        result = "{"
        for attr_name in self._attributes:
            value_format = "{value}"
            attr_value = self.__getattribute__(attr_name)
            if issubclass(type(attr_value), str):
                value_format = "'{value}'"
            elif issubclass(type(attr_value), int) or issubclass(type(attr_value), dict)\
                    or issubclass(type(attr_value), Object):
                value_format = "{value}"
            result += (" '{key}': " + value_format + ", ").format(key=attr_name, value=attr_value)
        result = result[0:-2] + result[-1] + "}"
        return result

    def GetAsDict(self):
        result = dict()
        for attr in self._attributes:
            attr_value = self.__getattribute__(attr)
            if type(attr_value) is Object:
                result[attr] = attr_value.GetAsDict()
            result[attr] = attr_value
        return result

    @classmethod
    def ConvertDictToObject(cls, d: dict):
        result = cls()
        for key in d.keys():
            value = d[key]
            if type(value) is dict:
                value = cls.ConvertDictToObject(value)
            result.__setattr__(key, value)
        return result

    @classmethod
    def hasAttrNested(cls, var, attrs: str) -> bool:
        attr = attrs.split('.', 1)
        if hasattr(var, attr[0]):
            if len(attr) > 1:
                return Object.hasAttrNested(var.__getattribute__(attr[0]), attr[1])
            return True
        return False


def DecodeUTF8(text: str):
    return text.encode('utf-8').decode()


def RemoveFormatName(text, format_name) -> str:
    remove_from_index = text.find('{' + format_name + '}')
    return text[:remove_from_index] + text[text.find('}', remove_from_index) + 1:]


def GetFormatNames(text) -> list:
    names = []
    start_index = text.find('{')
    end_index = text.find('}', start_index)
    while start_index != -1 and end_index != -1:
        names.append(text[start_index + 1:end_index])
        text = text[:start_index] + text[end_index + 1:]
        start_index = text.find('{')
        end_index = text.find('}', start_index)
    return names


def IsFormatNameInText(text: str, format_name: str) -> bool:
    names = GetFormatNames(text)
    return format_name in names


# format of this function is "'1','2':'3','4'" to [['1','2']['3','4']]
def ConvertStringToListsInList(text):
    # Formats text in this order "'1','2':'3','4'" to [['1','2']['3','4']]
    # ',' separates between items in list and ':' separates between lists

    return [(item for item in row.split(',')) for row in text.split(":")]


def RemoveUnreachableFormats(text_format: str, obj: Object):
    new_text_format = text_format
    format_names = GetFormatNames(text_format)
    for format_name in format_names:
        if not Object.hasAttrNested(obj, format_name):
            new_text_format = RemoveFormatName(new_text_format, format_name)
    return new_text_format
