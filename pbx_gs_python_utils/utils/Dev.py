import json
import pprint


class Dev:
    @staticmethod
    def jformat(data):
        return json.dumps(data, indent=4)       # use json.dumps to format

    @staticmethod
    def jprint(data):
        print()                                 # add a line before
        print(json.dumps(data, indent=4))       # use json.dumps to format
        return data

    @staticmethod
    def pformat(data):
        return pprint.pformat(data, indent=2)  # use a pprint to format

    @staticmethod
    def pprint(*args):
        print()                                 # add a line before
        for arg in args:
            pprint.pprint(arg, indent=2)  # use a pprint to format
        if len(args) == 1:
            return args[0]
        return args

    @staticmethod
    def print(data):
        print()                                 # add a line before
        print(data)
        return data


