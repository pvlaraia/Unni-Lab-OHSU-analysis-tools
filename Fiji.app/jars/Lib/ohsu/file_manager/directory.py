
from ij import IJ

class IJDirectory:
    def __init__(self, label):
        self.label = label
        self.path = IJ.getDirectory('{} Folder'.format(self.label))