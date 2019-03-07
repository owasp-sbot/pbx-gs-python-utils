import hashlib
import pprint
import random
import string
import textwrap
import re

from utils.Dev import Dev


class Misc:

    @staticmethod
    def chunks(items, split):
        for i in range(0, len(items), split):
            yield items[i:i + split]

    @staticmethod
    def class_name(target):
        if target:
            return type(target).__name__
        return None

    @staticmethod
    def object_data(target):
        #fields = [field for field in dir(target) if not callable(getattr(target, field)) and not field.startswith("a__")]
        return target.__dict__ # this one seems to do the trick (if not look at the code sample above)

    @staticmethod
    def random_filename(extension='.tmp', length=10):
        if len(extension) > 0 and  extension[0] != '.' : extension = '.' + extension
        return '{0}{1}'.format(''.join(random.choices(string.ascii_lowercase + string.digits, k=length)) ,  extension)

    @staticmethod
    def random_number(min=1,max=65000):
        return random.randint(min, max)

    @staticmethod
    def random_string_and_numbers(length=6,prefix=''):
        return prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    @staticmethod
    def md5(target):
        if target:
            return hashlib.md5('{0}'.format(target).encode()).hexdigest()
        return None

    @staticmethod
    def word_wrap(text,length = 40):
        return '\n'.join(textwrap.wrap(text, length))

    @staticmethod
    def word_wrap_escaped(text,length = 40):
        return '\\n'.join(textwrap.wrap(text, length))

    @staticmethod
    def convert_to_number(value):
        if value != '':
            try:
                if value[0] == '£':
                    return float(re.sub(r'[^\d.]', '', value))
                else:
                    return float(value)
            except:
              return 0
        else:
            return 0

    @staticmethod
    def remove_html_tags(html):
        if html:
            TAG_RE = re.compile(r'<[^>]+>')
            return TAG_RE.sub('', html).replace('&nbsp;', ' ')
