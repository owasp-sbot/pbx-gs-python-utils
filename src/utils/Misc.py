import random
import string
import textwrap


class Misc:

    @staticmethod
    def random_string_and_numbers(length=6,prefix=''):
        return prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    @staticmethod
    def word_wrap(text,length = 40):
        return '\n'.join(textwrap.wrap(text, length))

    def word_wrap_escaped(text,length = 40):
        return '\\n'.join(textwrap.wrap(text, length))