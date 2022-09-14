from ohsu.config.config import Config
from ohsu.config.core_config import CoreConfig

class NucleolusConfig:

    @staticmethod
    def getTargetChannel():
        config = NucleolusConfig.get()
        return config['targetChannel'] if config is not None and config.has_key('targetChannel') else None
    
    @staticmethod
    def setTargetChannel(channel):
        config = NucleolusConfig.get()
        if channel is None:
            config.pop('targetChannel', None)
        else:
            config['targetChannel'] = channel
        Config.set('nucleolus', config)

    @staticmethod
    def get():
        config = Config.get()
        return config['nucleolus'] if config.has_key('nucleolus') else {}

    @staticmethod
    def validate():
        pass