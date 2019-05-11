from pbx_gs_python_utils.utils.Dev import Dev


class Lists:

    @staticmethod
    def first(list, strip=False):
        if Lists.not_empty(list):
            value = list[0]
            if strip:
                value = value.strip()
            return value

    @staticmethod
    def not_empty(list):
        if list and type(list).__name__ == 'list' and len(list) >0:
            return True
        return False

    @staticmethod
    def empty(list):
        return not Lists.not_empty(list)
