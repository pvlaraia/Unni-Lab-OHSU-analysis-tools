from java.awt import  Checkbox, GridBagConstraints, GridBagLayout
from ohsu.config.core_config import CoreConfig
from ohsu.gui.ohsu_panel import OHSUPanel

class MeasurementsPanel(OHSUPanel):

    def __init__(self, gd):
        OHSUPanel.__init__(self, gd)
        self.setLayout(GridBagLayout())
        self.c = GridBagConstraints()
        self.c.anchor = GridBagConstraints.CENTER
        isEnabled = CoreConfig.getShouldRunCellMeasurements() or False
        self.checkbox = Checkbox('Enable default cell measurements', isEnabled)
        checkboxConstraint = GridBagConstraints()
        checkboxConstraint.gridwidth = GridBagConstraints.REMAINDER
        self.add(self.checkbox, checkboxConstraint)

    def getRunCellMeasurementsFlag(self):
        return self.checkbox.getState()