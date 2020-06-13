from string import Template


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


SECRET = 'blop'

st = "{error.__init__.__globals__[SECRET]}"
st = Template("${error.__init__.__globals__[SECRET]}")
st2 = Template("${a} ${b}")
err = Data()
err.a = 1
err.b = 'a'
print(st2.substitute(err.__dict__))

random_list = ["", "1", "", "", "", None, "2", None, "", "3", "4"]

for i in reversed(range(len(random_list) - 1)):
    if random_list[i] is None or random_list[i] == "":
        del random_list[i]

print(random_list)
