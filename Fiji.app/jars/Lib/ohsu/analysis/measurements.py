from ij import IJ
from ohsu.config.core_config import CoreConfig
from ohsu.constants import HEADER_KEY
from ohsu.helpers.roi_manager import RoiManager

class Measurements:
    def __init__(self, img, outputDir):
        self.img = img
        self.outputDir = outputDir
        self.roiMeasurements = {}
        channels = CoreConfig.getChannels()
        for channel in channels.keys():
            self.roiMeasurements[channel] = {}

    def run(self):
        slices = self.img.getSlices()
        channels = CoreConfig.getChannels()
        core_mask_channel = CoreConfig.getMaskChannel()
        main_threshold = self.img.getThreshold(channels[core_mask_channel])
        # routine to create ROIs for each nucleus using a set threshold, saves a nuclear mask image and then closes it, saves nuclei properties and the nuclear ROIs
        self.analyzeParticlesAndCreateROIs(slices[core_mask_channel], main_threshold)
        for channel, channel_img in slices.items():
            headings, measurements = channel_img.getRoiMeasurements()
            self.roiMeasurements[channel][HEADER_KEY] = headings
            self.roiMeasurements[channel][self.img.getName()] = measurements
        return self.roiMeasurements

    def analyzeParticlesAndCreateROIs(self, slice, threshold):
        slice.select()
        imgName = self.img.getName()
        IJ.setThreshold(threshold, 65535)

        RoiManager().get().runCommand('Show All with labels')
        IJ.run("Analyze Particles...", "size=500-Infinity show=Outlines add slice")
        drawing = IJ.getImage()
        tif_name = 'Drawing of {}.tif'.format(imgName)
        IJ.saveAsTiff(drawing, '{}/{}'.format(self.outputDir.path, tif_name))
        drawing.close()

        RoiManager().get().runCommand('Save', '{}/{}_RoiSet.zip'.format(self.outputDir.path, imgName))

