import json


class Blockchain():
    def __init__(self):
        self._blocks = []

    def append(self, block):
        self._blocks.append(block)

    def get_last(self):
        if len(self._blocks) <= 0:
            return None
        return self._blocks[-1]

    def get_length(self):
        return len(self._blocks)

    def json_dict(self):
        ret_val = []
        for block in self._blocks:
            ret_val.append(block.json_dict())
        return ret_val