from java.awt.event import ItemListener
from java.awt import  Checkbox, GridBagConstraints, GridBagLayout, GridLayout, Panel
from ohsu.config.foci_config import FociConfig
from ohsu.gui.ohsu_panel import OHSUPanel
from ohsu.gui.checkbox import OHSUCheckbox
from ohsu.gui.config.channel_panel import ChannelListener

class FociPanel(OHSUPanel):

    def __init__(self, gd, channelPanel):
        OHSUPanel.__init__(self, gd)
        self.channelPanel = channelPanel
        self.channelPanel.addListener(ChannelChangeHandler(self))
        self.options = None

        isEnabled = FociConfig.getChannels() is not None
        self.checkbox = Checkbox('Enable foci analysis', isEnabled)
        self.checkbox.addItemListener(self.ToggleHandler(self))
        
        self.regenerateOptions()
        
        self.setLayout(GridBagLayout())
        self.c = GridBagConstraints()
        self.c.anchor = GridBagConstraints.CENTER

        checkboxConstraint = GridBagConstraints()
        checkboxConstraint.gridwidth = GridBagConstraints.REMAINDER
        self.add(self.checkbox, checkboxConstraint)
        self.handleToggleChange()

    def getOptions(self):
        choicesPanel = Panel()
        choicesPanel.setLayout(GridLayout(0, 1))
        for channelNum, channelName in self.channelPanel.getChannels().items():
            checkbox = OHSUCheckbox(channelNum, channelName, channelNum in (FociConfig.getChannels() or []))
            choicesPanel.add(checkbox)
        return choicesPanel

    def regenerateOptions(self):
        if self.options is not None: 
            self.remove(self.options)
        self.options = self.getOptions()
        self.handleToggleChange()


    def getChannels(self):
        if not self.checkbox.getState():
            return None
        chosenBoxes = filter(lambda checkbox: checkbox.getState(), self.options.getComponents())
        return map(lambda checkbox: checkbox.getValue(), chosenBoxes)

    def handleToggleChange(self):
        if self.checkbox.getState():
            self.add(self.options, self.c)
        else:
            self.remove(self.options)
        self.repaintDialog()

    class ToggleHandler(ItemListener):
        
        def __init__(self, fociPanel):
            super(ItemListener, self).__init__()
            self.fociPanel = fociPanel

        def itemStateChanged(self, event):
            self.fociPanel.handleToggleChange()

class ChannelChangeHandler(ChannelListener):
    
    def __init__(self, fociPanel):
        self.fociPanel = fociPanel

    def onChannelsChanged(self, channels):
        self.fociPanel.regenerateOptions()
        self.fociPanel.repaintDialog()
