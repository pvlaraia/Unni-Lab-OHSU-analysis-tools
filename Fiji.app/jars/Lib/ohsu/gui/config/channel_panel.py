from java.awt.event import ActionListener, KeyListener
from java.awt import Button, GridBagConstraints, GridBagLayout, GridLayout, Label, Panel, TextField
from ohsu.config.core_config import CoreConfig
from ohsu.gui.ohsu_panel import OHSUPanel
from ij import IJ

class ChannelPanel(OHSUPanel):

    def __init__(self, gd):
        OHSUPanel.__init__(self, gd)
        self.listeners = []
        self.setLayout(GridBagLayout())
        c = GridBagConstraints()
        self.channels = Panel()
        self.channels.setLayout(GridLayout(0, 1))
        for channel, channelName in (CoreConfig.getChannels().items() if CoreConfig.getChannels() is not None else range(0)):
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
        field = TextField(name, 35)
        field.addKeyListener(ChannelTextChangeHandler(self))
        panelRow.add(Label(channelNumber))
        panelRow.add(field)
        panelRow.add(removeButton)
        self.channels.add(panelRow)
        self.runListeners()
        self.repaintDialog()

    def removeChannel(self, channelNumber):
        self.channels.remove(self.getComponentForChannel(channelNumber))
        self.regenerateChannelComponents()
        self.runListeners()
        self.repaintDialog()

    def runListeners(self):
        for listener in self.listeners:
            listener.onChannelsChanged(self.getChannels())

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

    def addListener(self, listener):
        self.listeners.append(listener)

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

class ChannelTextChangeHandler(KeyListener):

    def __init__(self, channelPanel):
        self.channelPanel = channelPanel
        super(KeyListener, self).__init__()

    def keyTyped(self, event):
        pass

    def keyPressed(self, event):
        pass

    def keyReleased(self, event):
        self.channelPanel.runListeners()

class ChannelListener():

    def onChannelsChanged(self, channels):
        pass