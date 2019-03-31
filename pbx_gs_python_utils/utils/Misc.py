import hashlib
import json
import pprint
import random
import string
import textwrap
import re
from time import sleep

class Misc:


    @staticmethod
    def array_add(array, value):
        array.append(value)
        return value

    @staticmethod
    def array_find(array, item):
        try:
            return array.index(item)
        except:
            return None

    @staticmethod
    def array_get(array, position=None):
        if array and len(array) > 0:
            if (position is not None) and len(array) > position:
                return array[position]

    @staticmethod
    def array_pop(array, position=None):
        if array and len(array) >0:
            if (position is not None) and len(array) > position:
                return array.pop(position)
            else:
                return array.pop()

    @staticmethod
    def array_pop_and_trim(array, position=None):
        value = Misc.array_pop(array,position)
        return Misc.trim(value)


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
    def get_value(target, key, default=None):
        if target is not None:
            try:
                value = target.get(key)
                if value is not None:
                    return value
            except:
                pass
        return default

    @staticmethod
    def get_random_color(max=5):
        if max > 5: max = 5                                                             # add support for more than 5 colors
        colors = ['skyblue', 'darkseagreen', 'palevioletred', 'coral', 'darkgray']
        return colors[Misc.random_number(0, max-1)]

    @staticmethod
    def is_number(value):
        try:
            int(value)
            return True
        except:
            pass
        return False

    @staticmethod
    def json_dumps(target, message=None):
        if target:
            return json.dumps(target, indent=4)
        return message

    @staticmethod
    def json_format(target, message=None):
        if target:
            return json.dumps(target, indent=4)
        return message

    @staticmethod
    def json_load(target):
        if target:
            try:
                return json.loads(target)
            except:
                pass
        return None

    @staticmethod
    def none_or_empty(target,field):
        if target:
            value = target.get(field)
            return (value is None) or value == ''
        return True

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
    def trim(target):
        if target:
            return target.strip()
        return target

    @staticmethod
    def to_int(value):
        try:
            return int(value)
        except:
            return None
    @staticmethod
    def wait(seconds):
        sleep(seconds)

    @staticmethod
    def word_wrap(text,length = 40):
        return '\n'.join(textwrap.wrap(text, length))

    @staticmethod
    def word_wrap_escaped(text,length = 40):
        if text:
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
