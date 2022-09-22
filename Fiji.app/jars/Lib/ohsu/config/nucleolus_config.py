from ohsu.config.config import Config
from ohsu.config.core_config import CoreConfig

class NucleolusConfig:

    @staticmethod
    def getMaskChannel():
        config = NucleolusConfig.get()
        return config['maskChannel'] if config is not None and config.has_key('maskChannel') else None
    
    @staticmethod
    def setMaskChannel(channel):
        config = NucleolusConfig.get()
        if channel is None:
            config.pop('maskChannel', None)
        else:
            config['maskChannel'] = channel
        Config.set('nucleolus', config)

    @staticmethod
    def getNucleolusChannel():
        config = NucleolusConfig.get()
        return config['nucleolusChannel'] if config is not None and config.has_key('nucleolusChannel') else None
    
    @staticmethod
    def setNucleolusChannel(channel):
        config = NucleolusConfig.get()
        if channel is None:
            config.pop('nucleolusChannel', None)
        else:
            config['nucleolusChannel'] = channel
        Config.set('nucleolus', config)


    @staticmethod
    def get():
        config = Config.get()
        return config['nucleolus'] if config.has_key('nucleolus') else {}

    @staticmethod
    def validate():
        pass