from fiji.util.gui import GenericDialogPlus
from ij import IJ
from java.awt.event import ActionListener
from java.awt import Button, GridLayout, Label, Panel, TextField
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
    

    gd.addButton('Add Channel', AddChannelHandler(channelPanel))


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

    def addChannel(self, channelNumber, name):
        panelRow = Panel()
        channelNumber = str(channelNumber)
        removeButton = Button('Remove')
        removeButton.addActionListener(RemoveChannelHandler(self, channelNumber))
        panelRow.add(Label(channelNumber))
        panelRow.add(TextField(name, 35))
        panelRow.add(removeButton)
        self.add(panelRow)
        self.repaintDialog()

    def removeChannel(self, channelNumber):
        self.remove(self.getComponentForChannel(channelNumber))
        self.regenerateChannelComponents()
        self.repaintDialog()

    def regenerateChannelComponents(self):
        components = self.getComponents()
        for idx, component in enumerate(components):
            newChannelNum = str(idx + 1)
            channelNumLabel = component.getComponent(0)
            channelButton = component.getComponent(2)
            
            channelNumLabel.setText(newChannelNum)
            [channelButton.removeActionListener(listener) for listener in channelButton.getActionListeners()]
            channelButton.addActionListener(RemoveChannelHandler(self, newChannelNum))


    def getComponentForChannel(self, channelNumber):
        components = self.getComponents()
        IJ.log('remove ' + channelNumber)
        return components[int(channelNumber) - 1]
        

    def repaintDialog(self):
        self.gd.validate()
        self.gd.pack()
        self.gd.repaint()

class AddChannelHandler(ActionListener):

    def __init__(self, channelPanel):
        self.channelPanel = channelPanel
        super(ActionListener, self).__init__()

    def actionPerformed(self, event):
        existingChannels = self.channelPanel.getChannels()
        self.channelPanel.addChannel(len(existingChannels) + 1, '')

class RemoveChannelHandler(ActionListener):
    
    def __init__(self, channelPanel, channelNumber):
        self.channelPanel = channelPanel
        self.channelNumber = channelNumber
        super(ActionListener, self).__init__()

    def actionPerformed(self, event):
        self.channelPanel.removeChannel(self.channelNumber)


class State(ActionListener):
    def actionPerformed(self, event):
        IJ.log('done')

run()