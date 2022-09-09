from ij import IJ
from ohsu.helpers.roi_manager import RoiManager

class Nucleolus:
    def __init__(self, mainChannelImg, secondaryChannelImg, shouldInvertROI):
        self.mainChannelImg = mainChannelImg
        self.secondaryChannelImg= secondaryChannelImg
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

        for i in range(0, roiM.getCount()):
            self.secondaryChannelImg.select()
            IJ.setThreshold(self.secondaryChannelImg.getThreshold(self.secondaryChannelImg.img.getTitle()), 65535)
            roiM.select()
            IJ.run("Analyze Particles...", "size=300-Infinity display exclude clear")

