from fiji.util.gui import GenericDialogPlus
from ij import IJ
from java.awt.event import ActionListener, ItemListener
from java.awt import Button, Checkbox, GridBagConstraints, GridBagLayout, GridLayout, Label, Panel, TextField
from ohsu.config.colocalisation_config import ColocalisationConfig
from ohsu.config.config import Config
from ohsu.config.core_config import CoreConfig
from ohsu.gui.ohsu_panel import OHSUPanel

def run():
    gd = GenericDialogPlus('Configure Parameters')

    channelPanel = ChannelPanel(gd)
    colocPanel = ColocalisationPanel(gd)

    gd.addMessage('Core Configuration')
    gd.addComponent(channelPanel)
    gd.addComponent(colocPanel)
   
    gd.showDialog()
    if (gd.wasCanceled()):
        return 0

    channels = channelPanel.getChannels()
    maskChannel = channelPanel.getMaskChannel()
    CoreConfig.setChannels(channels)
    CoreConfig.setMaskChannel(maskChannel)

    colocChannel = colocPanel.getChannel()
    ColocalisationConfig.setChannel(colocChannel)
    
    Config.save()

'''
CHANNELS
'''
class ChannelPanel(OHSUPanel):

    def __init__(self, gd):
        OHSUPanel.__init__(self, gd)
        self.setLayout(GridBagLayout())
        c = GridBagConstraints()
        self.channels = Panel()
        self.channels.setLayout(GridLayout(0, 1))
        for channel, channelName in CoreConfig.getChannels().items():
            self.addChannel(channel, channelName)

        c.gridwidth = GridBagConstraints.REMAINDER
        self.add(self.channels, c)

        addButton = Button('Add Channel')
        addButton.addActionListener(AddChannelHandler(self))
        self.add(addButton, c)

        self.maskTextField = TextField(CoreConfig.getMaskChannel(), 35)
        maskPanel = Panel()
        maskPanel.add(Label('Mask Channel'))
        maskPanel.add(self.maskTextField)
        self.add(maskPanel, c)

    def getMaskChannel(self):
        return self.maskTextField.getText()

    def getChannels(self):
        components = self.channels.getComponents()
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
        self.channels.add(panelRow)
        self.repaintDialog()

    def removeChannel(self, channelNumber):
        self.channels.remove(self.getComponentForChannel(channelNumber))
        self.regenerateChannelComponents()
        self.repaintDialog()

    def regenerateChannelComponents(self):
        components = self.channels.getComponents()
        for idx, component in enumerate(components):
            newChannelNum = str(idx + 1)
            channelNumLabel = component.getComponent(0)
            channelButton = component.getComponent(2)

            channelNumLabel.setText(newChannelNum)
            [channelButton.removeActionListener(listener) for listener in channelButton.getActionListeners()]
            channelButton.addActionListener(RemoveChannelHandler(self, newChannelNum))


    def getComponentForChannel(self, channelNumber):
        components = self.channels.getComponents()
        return components[int(channelNumber) - 1]

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


'''
COLOCALISATION
'''
class ColocalisationPanel(OHSUPanel):

    def __init__(self, gd):
        OHSUPanel.__init__(self, gd)
        isEnabled = ColocalisationConfig.getChannel() is not None
        self.checkbox = Checkbox('Enable colocalisation', isEnabled)
        self.checkbox.addItemListener(self.ToggleHandler(self))
        self.textField = TextField(ColocalisationConfig.getChannel(), 35)
        self.textPanel = Panel()
        self.textPanel.add(Label('Colocalisation Channel'))
        self.textPanel.add(self.textField)
        self.buildInitial()

    def getChannel(self):
        if not self.checkbox.getState():
            return None
        return self.textField.getText()

    def buildInitial(self):
        self.setLayout(GridLayout(0, 1))
        self.add(self.checkbox)
        self.handleToggleChange()

    def handleToggleChange(self):
        if self.checkbox.getState():
            self.add(self.textPanel)
        else:
            self.remove(self.textPanel)
        self.repaintDialog()

    class ToggleHandler(ItemListener):
        
        def __init__(self, colocPanel):
            super(ItemListener, self).__init__()
            self.colocPanel = colocPanel

        def itemStateChanged(self, event):
            self.colocPanel.handleToggleChange()

run()