from java.awt.event import ItemListener
from java.awt import  Checkbox, Choice, GridBagConstraints, GridBagLayout, GridLayout, Label, Panel
from ohsu.config.nucleolus_config import NucleolusConfig
from ohsu.gui.ohsu_panel import OHSUPanel
from ohsu.gui.config.channel_panel import ChannelListener

class NucleolusPanel(OHSUPanel):

    def __init__(self, gd, channelPanel):
        OHSUPanel.__init__(self, gd)
        self.channelPanel = channelPanel
        self.channelPanel.addListener(ChannelChangeHandler(self))
        self.options = None
        self.targetChoiceDropdown = None
        self.selectedTargetChannel = NucleolusConfig.getTargetChannel()
        self.setLayout(GridBagLayout())
        self.c = GridBagConstraints()
        self.c.anchor = GridBagConstraints.CENTER

        isEnabled = NucleolusConfig.getTargetChannel() is not None
        self.checkbox = Checkbox('Enable nucleolus analysis', isEnabled)
        self.checkbox.addItemListener(self.ToggleHandler(self))
        checkboxConstraint = GridBagConstraints()
        checkboxConstraint.gridwidth = GridBagConstraints.REMAINDER
        self.add(self.checkbox, checkboxConstraint)
        
        self.regenerateOptions()

    def getTargetChannel(self):
        if not self.checkbox.getState():
            return None
        return self.selectedTargetChannel

    def getOptions(self):
        targetPanel = Panel()
        targetPanel.setLayout(GridLayout(0, 1))
        targetPanel.add(Label('Target channel'))
        choice = Choice()
        [choice.add(channel) for channel in self.channelPanel.getChannels().keys()]
        if (self.selectedTargetChannel in self.channelPanel.getChannels().keys()):
            choice.select(self.selectedTargetChannel)
        choice.addItemListener(self.TargetChoiceHandler(self))
        targetPanel.add(choice)
        self.targetChoiceDropdown = choice
        return targetPanel

    def regenerateOptions(self):
        self.removeOptions()
        if self.checkbox.getState():
            self.options = self.getOptions()
            self.add(self.options, self.c)
        self.repaintDialog()

    def removeOptions(self):
        if (self.options is not None):
            self.targetChoiceDropdown = None
            self.remove(self.options)

    class ToggleHandler(ItemListener):
        
        def __init__(self, nucleolusPanel):
            super(ItemListener, self).__init__()
            self.nucleolusPanel = nucleolusPanel

        def itemStateChanged(self, event):
            self.nucleolusPanel.regenerateOptions()

    class TargetChoiceHandler(ItemListener):
        def __init__(self, nucleolusPanel):
            super(ItemListener, self).__init__()
            self.nucleolusPanel = nucleolusPanel

        def itemStateChanged(self, event):
            self.nucleolusPanel.selectedTargetChannel = self.nucleolusPanel.targetChoiceDropdown.getSelectedItem()

class ChannelChangeHandler(ChannelListener):
    
    def __init__(self, nucleolusPanel):
        self.nucleolusPanel = nucleolusPanel

    def onChannelsChanged(self, channels):
        self.nucleolusPanel.regenerateOptions()
