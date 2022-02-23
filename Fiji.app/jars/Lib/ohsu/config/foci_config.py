
from ohsu.config.config import Config
from ohsu.config.core_config import CoreConfig

class FociConfig:

    @staticmethod
    def getChannels():
        config = FociConfig.get()
        return config['channels'] if config is not None and config.has_key('channels') else None
    
    @staticmethod
    def setChannels(channels):
        config = FociConfig.get()
        if channels is None:
            config.pop('channels', None)
        else:
            config['channels'] = channels
        Config.set('foci', config)

    @staticmethod
    def get():
        config = Config.get()
        return config['foci'] if config.has_key('foci') else {}

    @staticmethod
    def validate():
        channels = FociConfig.getChannels()
        if channels is not None and all(c in channels for c in CoreConfig.getChannels().keys()):
            raise Exception('One of the foci channels is not a valid channel')