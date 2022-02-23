from fiji.util.gui import GenericDialogPlus
from ohsu.config.colocalisation_config import ColocalisationConfig
from ohsu.config.config import Config
from ohsu.config.core_config import CoreConfig
from ohsu.config.foci_config import FociConfig
from ohsu.gui.config.channel_panel import ChannelPanel
from ohsu.gui.config.coloc_panel import ColocalisationPanel
from ohsu.gui.config.foci_panel import FociPanel

def run():
    gd = GenericDialogPlus('Configure Parameters')

    channelPanel = ChannelPanel(gd)
    colocPanel = ColocalisationPanel(gd)
    fociPanel = FociPanel(gd, channelPanel)

    gd.addMessage('Core Configuration')
    gd.addComponent(channelPanel)
    gd.addComponent(colocPanel)
    gd.addComponent(fociPanel)
   
    gd.showDialog()
    if (gd.wasCanceled()):
        return 0

    CoreConfig.setChannels(channelPanel.getChannels())
    CoreConfig.setMaskChannel(channelPanel.getMaskChannel())
    ColocalisationConfig.setChannel(colocPanel.getChannel())
    FociConfig.setChannels(fociPanel.getChannels())
    
    Config.save()

run()