from fiji.util.gui import GenericDialogPlus
from ij import IJ
from java.awt.event import ActionListener
from java.awt import GridLayout, Label, Panel, TextField
from ohsu.config.core_config import CoreConfig

def run():
    coreConfig = CoreConfig.get()
    gd = GenericDialogPlus('Instructions')

    state = State()
    channelVerticalLayout = GridLayout(0,1)
    channelPanel = ChannelPanel(gd)
    channelPanel.setLayout(channelVerticalLayout)

    gd.addMessage('Core Configuration')

    for channel, channelName in coreConfig['channels'].items():
        channelPanel.addChannel(channel, channelName)

    gd.addComponent(channelPanel)
    

    gd.addButton('Add Channel', ChannelHandler(channelPanel))


    gd.addMessage('Colocalisation')

    gd.addButton('Save', state)
   
    gd.showDialog()
    if (gd.wasCanceled()):
        return 0

class ChannelPanel(Panel):

    def __init__(self, gd):
        self.gd = gd
        super(Panel, self).__init__()

    def getChannels(self):
        components = self.getComponents()
        channels = {}
        for component in components:
            idx = component.getComponent(0).getText()
            name = component.getComponent(1).getText()
            channels[idx] =  name
        return channels

    def addChannel(self, index, name):
        panelRow = Panel()
        field = TextField(name, 35)
        panelRow.add(Label(str(index)))
        panelRow.add(field)
        panelRow.add(Label('X'))
        self.add(panelRow)
        self.gd.validate()
        self.gd.pack()
        self.gd.repaint()

class ChannelHandler(ActionListener):

    def __init__(self, channelPanel):
        self.channelPanel = channelPanel
        super(ActionListener, self).__init__()

    def actionPerformed(self, event):
        existingChannels = self.channelPanel.getChannels()
        self.channelPanel.addChannel(len(existingChannels) + 1, '')

class State(ActionListener):
    def actionPerformed(self, event):
        IJ.log('done')

run()