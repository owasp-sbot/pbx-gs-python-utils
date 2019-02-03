import random
import string
import textwrap
import re


class Misc:

    @staticmethod
    def random_string_and_numbers(length=6,prefix=''):
        return prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    @staticmethod
    def word_wrap(text,length = 40):
        return '\n'.join(textwrap.wrap(text, length))

    @staticmethod
    def word_wrap_escaped(text,length = 40):
        return '\\n'.join(textwrap.wrap(text, length))

    @staticmethod
    def convert_to_number(value):
        if value != '':
            if value[0] == '£':
                return float(re.sub(r'[^\d.]', '', value))
            else:
                return float(value)
        else:
            return 0