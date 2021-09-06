
from ij import IJ, ImagePlus

class IJDirectory:
    def __init__(self, label):
        self.label = label
        self.path = IJ.getDirectory('{} Directory'.format(self.label))