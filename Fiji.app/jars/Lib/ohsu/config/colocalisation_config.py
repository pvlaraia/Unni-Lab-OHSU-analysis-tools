
from ohsu.config.config import Config
from ohsu.config.core_config import CoreConfig

class ColocalisationConfig:

    @staticmethod
    def getChannel():
        config = ColocalisationConfig.get()
        return config['channel'] if config.has_key('channel') else None
    
    @staticmethod
    def setChannel(channel):
        config = ColocalisationConfig.get()
        if channel is None:
            config.pop('channel', None)
        else:
            config['channel'] = channel

    @staticmethod
    def get():
        config = Config.get()
        return config['colocalisation'] if config.has_key('colocalisation') else None

    @staticmethod
    def validate():
        channel = ColocalisationConfig.getChannel()
        if channel is not None and channel not in CoreConfig.getChannels().keys():
            raise Exception('colocChannel "{}" is not a valid channel, does not exist'.format(channel))