import json

class Config:
    __conf = None

    @staticmethod
    def get():
        return Config.__getConfig()

    @staticmethod
    def close():
        Config.__conf = None

    @staticmethod
    def __getConfig():
        if (Config.__conf is None):
            with open('./scripts/OHSU/config.json') as stream:
                Config.__conf = json.load(stream)
        return Config.__conf
