from collections import OrderedDict

class PlayerInfo:
    def __init__(self, name):
        self.name = name
        self.info = OrderedDict()

    def addInformation(self, info_type, value):
        self.info[info_type] = value

    def returnInfo(self):
        values = []
        for key, value in self.info.items():
            values.append(key + ": " + str(value))

        return values

    def __str__(self):
        stats = self.name
        stats += "\n".join(self.returnInfo())
        return stats
