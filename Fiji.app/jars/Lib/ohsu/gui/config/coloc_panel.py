from java.awt.event import ItemListener
from java.awt import Checkbox, GridLayout, Label, Panel, TextField
from ohsu.config.colocalisation_config import ColocalisationConfig
from ohsu.gui.ohsu_panel import OHSUPanel

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