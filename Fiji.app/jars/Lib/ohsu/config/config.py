import json

class Config:
    __conf = None

    @staticmethod
    def get():
        return Config.__getConfig()

    @staticmethod
    def set(key, content):
        Config.__conf[key] = content

    @staticmethod
    def close():
        Config.__conf = None

    @staticmethod
    def save():
        with open('./scripts/OHSU/config.json', 'w') as outfile:
            json.dump(Config.__conf, outfile)

    @staticmethod
    def __getConfig():
        if (Config.__conf is None):
            try:
                with open('./scripts/OHSU/config.json') as stream:
                    Config.__conf = json.load(stream)
            except Exception:
                Config.__conf = {}
        return Config.__conf

