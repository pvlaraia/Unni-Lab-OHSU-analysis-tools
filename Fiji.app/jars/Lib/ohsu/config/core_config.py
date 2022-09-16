
from ohsu.config.config import Config

class CoreConfig:

    @staticmethod
    def getMaskChannel():
        config = CoreConfig.get()
        return config['maskChannel'] if config is not None and config.has_key('maskChannel') else None
    
    @staticmethod
    def setMaskChannel(num):
        config = CoreConfig.get()
        config['maskChannel'] = num
        Config.set('core', config)

    @staticmethod
    def getShouldRunCellMeasurements():
        config = CoreConfig.get()
        return config['shouldRunMeasurements'] if config is not None and config.has_key('shouldRunMeasurements') else False

    @staticmethod
    def setShouldRunCellMeasurements(flag):
        config = CoreConfig.get()
        config['shouldRunMeasurements'] = flag
        Config.set('core', config)

    @staticmethod
    def getChannels():
        config = CoreConfig.get()
        return config['channels'] if config is not None and config.has_key('channels') else None

    @staticmethod
    def setChannels(channels):
        config = CoreConfig.get()
        config['channels'] = channels
        Config.set('core', config)

    @staticmethod
    def addChannel(num, label):
        channels = CoreConfig.getChannels()
        channels[str(num)] = label
        CoreConfig.setChannels(channels)

    @staticmethod
    def removeChannel(num):
        channels = CoreConfig.getChannels()
        del channels[str(num)]
        CoreConfig.setChannels(channels)

    @staticmethod
    def get():
        config = Config.get()
        return config['core'] if config.has_key('core') else {}

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
