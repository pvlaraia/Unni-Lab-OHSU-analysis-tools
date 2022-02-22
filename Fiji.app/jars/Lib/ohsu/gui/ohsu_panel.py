from java.awt import Panel

class OHSUPanel(Panel):

    def __init__(self, gd):
        self.gd = gd
        super(Panel, self).__init__()
        
    def repaintDialog(self):
        self.gd.validate()
        self.gd.pack()
        self.gd.repaint()