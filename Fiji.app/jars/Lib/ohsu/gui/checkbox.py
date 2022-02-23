from java.awt import Checkbox

class OHSUCheckbox(Checkbox):

    def __init__(self, value, label, check):
        super(Checkbox, self).__init__(label, check)
        self.value = value

    def getValue(self):
        return self.value