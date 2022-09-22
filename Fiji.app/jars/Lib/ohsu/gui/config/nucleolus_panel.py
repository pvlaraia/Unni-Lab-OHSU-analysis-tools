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

        self.maskOptions = None
        self.maskChoiceDropdown = None
        self.selectedMaskChannel = NucleolusConfig.getMaskChannel()

        self.nucOptions = None
        self.nucChoiceDropdown = None
        self.selectedNucChannel = NucleolusConfig.getNucleolusChannel()

        self.setLayout(GridBagLayout())
        self.c = GridBagConstraints()
        self.c.anchor = GridBagConstraints.CENTER

        isEnabled = NucleolusConfig.getMaskChannel() is not None
        self.checkbox = Checkbox('Enable nucleolus analysis', isEnabled)
        self.checkbox.addItemListener(self.ToggleHandler(self))
        checkboxConstraint = GridBagConstraints()
        checkboxConstraint.gridwidth = GridBagConstraints.REMAINDER
        self.add(self.checkbox, checkboxConstraint)
        
        self.regenerateOptions()

    def getMaskChannel(self):
        if not self.checkbox.getState():
            return None
        return self.selectedMaskChannel
    
    def getNucleolusChannel(self):
        if not self.checkbox.getState():
            return None
        return self.selectedNucChannel

    def getMaskOptions(self):
        maskPanel = Panel()
        maskPanel.setLayout(GridLayout(0, 1))
        maskPanel.add(Label('Inverted mask channel'))
        choice = self.getChannelChoices(self.selectedMaskChannel)
        choice.addItemListener(self.MaskChoiceHandler(self))
        maskPanel.add(choice)
        self.maskChoiceDropdown = choice
        return maskPanel
    
    def getNucOptions(self):
        nucPanel = Panel()
        nucPanel.setLayout(GridLayout(0, 1))
        nucPanel.add(Label('Nucleolus channel'))
        choice = self.getChannelChoices(self.selectedNucChannel)
        choice.addItemListener(self.NucChoiceHandler(self))
        nucPanel.add(choice)
        self.nucChoiceDropdown = choice
        return nucPanel

    def getChannelChoices(self, selectedChannel):
        choice = Choice()
        [choice.add(channel) for channel in self.channelPanel.getChannels().keys()]
        if (selectedChannel in self.channelPanel.getChannels().keys()):
            choice.select(selectedChannel)
        return choice


    def regenerateOptions(self):
        self.removeOptions()
        if self.checkbox.getState():
            self.maskOptions = self.getMaskOptions()
            self.add(self.maskOptions, self.c)
            self.nucOptions = self.getNucOptions()
            self.add(self.nucOptions, self.c)
        self.repaintDialog()

    def removeOptions(self):
        if (self.maskOptions is not None):
            self.maskChoiceDropdown = None
            self.remove(self.maskOptions)

        if self.nucOptions is not None:
            self.nucChoiceDropdown = None
            self.remove(self.nucOptions)

    class ToggleHandler(ItemListener):
        
        def __init__(self, nucleolusPanel):
            super(ItemListener, self).__init__()
            self.nucleolusPanel = nucleolusPanel

        def itemStateChanged(self, event):
            self.nucleolusPanel.regenerateOptions()

    class MaskChoiceHandler(ItemListener):
        def __init__(self, nucleolusPanel):
            super(ItemListener, self).__init__()
            self.nucleolusPanel = nucleolusPanel

        def itemStateChanged(self, event):
            self.nucleolusPanel.selectedMaskChannel = self.nucleolusPanel.maskChoiceDropdown.getSelectedItem()

    class NucChoiceHandler(ItemListener):
        def __init__(self, nucleolusPanel):
            super(ItemListener, self).__init__()
            self.nucleolusPanel = nucleolusPanel

        def itemStateChanged(self, event):
            self.nucleolusPanel.selectedNucChannel = self.nucleolusPanel.nucChoiceDropdown.getSelectedItem()


class ChannelChangeHandler(ChannelListener):
    
    def __init__(self, nucleolusPanel):
        self.nucleolusPanel = nucleolusPanel

    def onChannelsChanged(self, channels):
        self.nucleolusPanel.regenerateOptions()
