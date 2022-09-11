from ij import IJ
from ohsu.config.core_config import CoreConfig
from ohsu.constants import HEADER_KEY
from ohsu.helpers.roi_manager import RoiManager
from ohsu.results.results import Results

class Measurements:
    def __init__(self, img, slices, imgName, outputDir):
        self.img = img
        self.slices = slices
        self.imgName = imgName
        self.outputDir = outputDir
        self.roiMeasurements = {}
        channels = CoreConfig.getChannels()
        for channel in channels.keys():
            self.roiMeasurements[channel] = {}

    def run(self):
        '''
        channels = CoreConfig.getChannels()
        core_mask_channel = CoreConfig.getMaskChannel()
        # routine to select and create single images of the channels and then close the parent z-stack
        images = {}
        for channel, label in channels.items():
            images[channel] = self.img.createStackedImage(label, int(channel))
            '''
        channels = CoreConfig.getChannels()
        core_mask_channel = CoreConfig.getMaskChannel()
        main_threshold = self.img.getThreshold(channels[core_mask_channel])
        # routine to create ROIs for each nucleus using a set threshold, saves a nuclear mask image and then closes it, saves nuclei properties and the nuclear ROIs
        self.analyzeParticlesAndCreateROIs(self.slices[core_mask_channel], self.imgName, main_threshold)
        for channel, channel_img in self.slices.items():
            headings, measurements = channel_img.getRoiMeasurements()
            self.roiMeasurements[channel][HEADER_KEY] = headings
            self.roiMeasurements[channel][self.imgName] = measurements
        return self.roiMeasurements

    def analyzeParticlesAndCreateROIs(self, img, imgName, threshold):
        img.select()
        IJ.setThreshold(threshold, 65535)

        RoiManager().get().runCommand('Show All with labels')
        IJ.run("Analyze Particles...", "size=500-Infinity show=Outlines add slice")
        drawing = IJ.getImage()
        tif_name = 'Drawing of {}.tif'.format(imgName)
        IJ.saveAsTiff(drawing, '{}/{}'.format(self.outputDir.path, tif_name))
        drawing.close()

        RoiManager().get().runCommand('Save', '{}/{}_RoiSet.zip'.format(self.outputDir.path, imgName))

