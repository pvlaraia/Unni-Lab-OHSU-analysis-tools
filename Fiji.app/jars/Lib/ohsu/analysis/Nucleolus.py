from ij import IJ
from ohsu.constants import HEADER_KEY
from ohsu.config.core_config import CoreConfig
from ohsu.config.nucleolus_config import NucleolusConfig
from ohsu.helpers.roi_manager import RoiManager
from ohsu.results.results import Results

class Nucleolus:
    def __init__(self, img, shouldInvertROI):
        slices = img.getSlices()
        nucleolus_target_channel = NucleolusConfig.getTargetChannel()
        main_mask_channel = CoreConfig.getMaskChannel()
        self.mainChannelImg = slices[main_mask_channel]
        self.secondaryChannelImg= slices[nucleolus_target_channel]
        self.shouldInvertROI= shouldInvertROI

    def run(self):
        self.mainChannelImg.select()
        IJ.setThreshold(self.mainChannelImg.getThreshold(self.mainChannelImg.img.getTitle()), 65535)
        roiM = RoiManager().get()
        IJ.run("Analyze Particles...", "size=500-Infinity add")
        if self.shouldInvertROI:
            for i in range(0, roiM.getCount()):
                self.secondaryChannelImg.select()
                roiM.select(i)
                IJ.run("Invert")

        headers = None
        collection = {}
        for i in range(0, roiM.getCount()):
            self.secondaryChannelImg.select()
            roiM.select(i)
            IJ.setThreshold(self.secondaryChannelImg.getThreshold(self.secondaryChannelImg.img.getTitle()), 65535)
            IJ.run("Analyze Particles...", "size=300-Infinity display exclude clear")
            results = Results()
            headings, measurements = results.getResultsArray()
            headers = headers or headings
            collection[str(i+1)] = measurements
            results.close()
        collection[HEADER_KEY] = headers
        return collection