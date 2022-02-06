
from ohsu.config.config import Config

class CoreConfig:

    @staticmethod
    def getMaskChannel():
        config = CoreConfig.get()
        return config['maskChannel'] if config.has_key('maskChannel') else None

    @staticmethod
    def getChannels():
        config = CoreConfig.get()
        return config['channels'] if config.has_key('channels') else None

    @staticmethod
    def get():
        config = Config.get()
        return config['core'] if config.has_key('core') else None

    @staticmethod
    def validate():
        channels = CoreConfig.getChannels()
        maskChannel = CoreConfig.getMaskChannel()
        if channels is None:
            raise Exception('"channels" must be defined in config.json')
        
        if maskChannel is None:
            raise Exception('"maskChannel" must be defined in config.json')

        if maskChannel not in channels.keys():
            raise Exception('maskChannel "{}" is not a valid channel, does not exist'.format(maskChannel))
