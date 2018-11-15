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
    def pprint(data):
        print()                                 # add a line before
        pprint.pprint(data, indent=2)           # use a pprint to format
        return data

    @staticmethod
    def print(data):
        print()                                 # add a line before
        print(data)
        return data


