from ij import IJ
from ohsu.constants import HEADER_KEY
from ohsu.config.core_config import CoreConfig
from ohsu.config.nucleolus_config import NucleolusConfig
from ohsu.helpers.roi_manager import RoiManager
from ohsu.results.results import Results

class Nucleolus:
    def __init__(self, img, shouldInvertROI):
        slices = img.getSlices()
        self.img = img
        self.cellMaskImg = slices[CoreConfig.getMaskChannel()]
        self.nucleolusMaskImg= slices[NucleolusConfig.getMaskChannel()]
        self.nucleolusMeasureImg = slices[NucleolusConfig.getNucleolusChannel()]
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

        roiGroups = {}
        roiCountSoFar = cellRoiCount
        for i in range(0, cellRoiCount):
            self.nucleolusMaskImg.select()
            roiM.select(i)
            IJ.setThreshold(self.nucleolusMaskImg.getThreshold(), 65535)
            IJ.run("Analyze Particles...", "size=300-Infinity exclude add")
            countAfterAnalyze = roiM.getCount()
            roiGroups[i] = range(roiCountSoFar, countAfterAnalyze)
            roiCountSoFar = countAfterAnalyze

        headers = None
        collection = {}
        for cellI, roiIndices in roiGroups.items():
            roiM.deselect()
            roiM.setSelectedIndexes(roiIndices)
            self.nucleolusMeasureImg.select()
            roiM.runCommand('Measure')
            results = Results()
            headings, measurements = results.getResultsArray()
            headers = headers or headings
            collection[cellI] = measurements
            results.close()
        RoiManager().dispose()

        return {HEADER_KEY: headers, self.img.getName(): collection}