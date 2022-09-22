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
        self.cellMaskImg = slices[main_mask_channel]
        self.nucleolusMaskImg= slices[nucleolus_target_channel]
        self.nucleolusMeasureImg = slices['2'] # @nocommit
        self.shouldInvertROI= shouldInvertROI

    def run(self):
        self.cellMaskImg.select()
        IJ.setThreshold(self.cellMaskImg.getThreshold(), 65535)
        roiM = RoiManager().get()
        IJ.run("Analyze Particles...", "size=500-Infinity add")
        cellRoiCount = roiM.getCount()
        if self.shouldInvertROI:
            for i in range(0, cellRoiCount):
                self.nucleolusMaskImg.select()
                roiM.select(i)
                IJ.run("Invert")

        for i in range(0, cellRoiCount):
            self.nucleolusMaskImg.select()
            roiM.select(i)
            IJ.setThreshold(self.nucleolusMaskImg.getThreshold(), 65535)
            IJ.run("Analyze Particles...", "size=300-Infinity exclude add")

        headers = None
        collection = {}
        for i in range(cellRoiCount, roiM.getCount()):
            self.nucleolusMeasureImg.select()
            roiM.select(i)
            roiM.runCommand('Measure')
            results = Results()
            headings, measurements = results.getResultsArray()
            headers = headers or headings
            collection[str(i+1)] = measurements
            results.close()
        collection[HEADER_KEY] = headers
        return collection