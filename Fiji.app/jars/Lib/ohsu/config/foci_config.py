
from ohsu.config.config import Config
from ohsu.config.core_config import CoreConfig

class FociConfig:

    @staticmethod
    def getChannel():
        config = FociConfig.get()
        return config['channel'] if config is not None and config.has_key('channel') else None
    
    @staticmethod
    def setChannel(channel):
        config = FociConfig.get()
        if channel is None:
            config.pop('channel', None)
        else:
            config['channel'] = channel
        Config.set('foci', config)

    @staticmethod
    def get():
        config = Config.get()
        return config['foci'] if config.has_key('foci') else {}

    @staticmethod
    def validate():
        channel = FociConfig.getChannel()
        if channel is not None and channel not in CoreConfig.getChannels().keys():
            raise Exception('fociChannel "{}" is not a valid channel, does not exist'.format(channel))