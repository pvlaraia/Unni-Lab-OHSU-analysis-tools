from ohsu.config.colocalisation_config import ColocalisationConfig
from ohsu.config.core_config import CoreConfig
from ohsu.constants import HEADER_KEY
from ohsu.helpers.roi_manager import RoiManager
from ij import IJ, WindowManager

class Colocalisation:
    def __init__(self, img, channel):
        self.img = img
        self.channel = channel

    def run(self):
        headings, measurements = self.getColocalisation()
        return {HEADER_KEY: headings, self.img.getName(): measurements}


    '''
    Given an image, run Colocalisation Test plugin

    @img Image - the image to run Coloc on

    return tuple([headers], [[roi measurements]])
    '''
    def getColocalisation(self):
        slice = self.img.getSlices()[self.channel]
        roiM = RoiManager().get()
        headers = None
        collection = []
        channels = CoreConfig.getChannels()
        colocChannel = ColocalisationConfig.getChannel()
        for i in range(0, roiM.getCount()):
            slice.select()
            roiM.select(i)
            IJ.run('Colocalization Test', 'channel_1={} channel_2={} roi=[ROI in channel {} ] randomization=[Fay (x,y,z translation)] current_slice'.format(channels["1"], channels["2"], colocChannel))
            resultsTextWindow = WindowManager.getWindow('Results')
            textPanel = resultsTextWindow.getTextPanel()
            headings = textPanel.getOrCreateResultsTable().getColumnHeadings().split("\t")
            data = textPanel.getLine(0).split("\t")
            headers = headings if headers is None else headers
            collection.append(data)
        return (headers, collection)
