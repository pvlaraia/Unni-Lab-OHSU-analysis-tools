
from ij import IJ, ImagePlus

class IJDirectory:
    def __init__(self, label):
        self.path = None
        self.label = label

    def initialize(self):
        self.path = IJ.getDirectory('{} Directory'.format(self.label))