import os

from ij import IJ, WindowManager
from ij.gui import NonBlockingGenericDialog
from ohsu.config.core_config import CoreConfig
from ohsu.helpers.roi_manager import RoiManager
from ohsu.results.results import Results

class Image:
    '''
    ImagePlus img - the image for which we're retrieving DAPI threshold
    '''
    def __init__(self, img):
         self.img = img
         self.slices = None

    '''
    Open a CZI image with default Bio-Formats settings

    string imgpath - path of the image

    return Image - instance of this class
    '''
    @classmethod
    def fromCZI(cls, imgpath):
        filename = os.path.basename(imgpath)
        IJ.run("Bio-Formats", "open=["+imgpath+"] autoscale color_mode=Default rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT")
        img = WindowManager.getImage(filename)
        return cls(img)

    '''
    Close this image
    '''
    def close(self):
        self.img.changes = False
        self.img.close()

    '''
    Select/focus this image
    '''
    def select(self):
        IJ.selectWindow(self.img.getTitle())

    '''
    Ask the user to determine a threshold to use for this image

    string label - The type of threshold being retrieved, eg DAPI

    return int - the threshold as set by the user
    '''
    def getThreshold(self, label):
        self.select()
        IJ.run('Threshold...')
        threshold_window = WindowManager.getWindow('Threshold')

        gd = NonBlockingGenericDialog('Get {} Threshold'.format(label))
        gd.addMessage('Tweak the threshold slider until it looks right, then enter that number below as the {} Threshold to use for this image'.format(label))
        gd.addNumericField('{} Threshold'.format(label), 0)
        gd.hideCancelButton()
        gd.showDialog()
        dapi_threshold = int(gd.getNumericFields()[0].getText())

        threshold_window.close()
        return dapi_threshold

    '''
    For this image, get ROI measurements

    return tuple([headers], [[roi measurements]])
    '''
    def getRoiMeasurements(self):
        roiM = RoiManager().get()
        roiM.deselect()
        self.select()
        roiM.runCommand('Measure')
        results = Results()
        data = results.getResultsArray()
        results.close()
        return data

    '''
    return slices for this image based on the channels in the provided channel configuration

    return array of image slices
    '''
    def getSlices(self):
        if self.slices is None:
            self.makeSlices()
        print(self.slices)
        return self.slices
    
    '''
    Close all our channel img slices

    return void
    '''
    def closeSlices(self):
        for s in self.slices.values():
            s.close()
        self.slices = None

    '''
    Generate slices for the channels in our program configuration

    return void
    '''
    def makeSlices(self):
        channels = CoreConfig.getChannels()
        self.slices = {}
        for channel, label in channels.items():
            self.slices[channel] = self.createStackedImage(label, int(channel))

    '''
    Create a new image from a specific channel of the image in this class

    string name - name of the new image
    int channel - the channel from which to build this new image

    return Image - new instance of this class wrapping the created stacked image
    '''
    def createStackedImage(self, name, channel):
        IJ.newImage(name, '16-bit black', 1908, 1908, 1)
        copy = Image(WindowManager.getImage(name))
        self.select()
        initialSlice = self.img.getSlice()
        initialChannel = self.img.getC()
        self.img.setSlice(0)
        self.img.setC(channel)

        self.img.copy()
        copy.img.paste()

        self.img.setSlice(initialSlice)
        self.img.setC(initialChannel)
        return copy