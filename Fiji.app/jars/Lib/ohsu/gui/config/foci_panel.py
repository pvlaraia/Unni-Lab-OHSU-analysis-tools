from java.awt.event import ItemListener
from java.awt import  Checkbox, GridBagConstraints, GridBagLayout, GridLayout, Panel
from ohsu.config.foci_config import FociConfig
from ohsu.gui.ohsu_panel import OHSUPanel
from ohsu.gui.checkbox import OHSUCheckbox

class FociPanel(OHSUPanel):

    def __init__(self, gd, channelPanel):
        OHSUPanel.__init__(self, gd)
        self.channelPanel = channelPanel
        isEnabled = FociConfig.getChannels() is not None
        self.checkbox = Checkbox('Enable foci analysis', isEnabled)
        self.checkbox.addItemListener(self.ToggleHandler(self))
        
        self.options = self.getOptions()
        
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


    def getChannel(self):
        if not self.checkbox.getState():
            return None
        return self.textField.getText()

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