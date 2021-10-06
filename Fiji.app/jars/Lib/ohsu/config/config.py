import json

class Config:
    __conf = None

    @staticmethod
    def getConfig():
        return Config.__getConfig()

    @staticmethod
    def __getConfig():
        if (Config.__conf is None):
            with open('./scripts/OHSU/config.json') as stream:
                Config.__conf = json.load(stream)
        return Config.__conf
