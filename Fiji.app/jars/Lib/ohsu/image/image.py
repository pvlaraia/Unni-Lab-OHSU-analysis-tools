import os
from ij import IJ, WindowManager
from ij.gui import NonBlockingGenericDialog

class Image:
    '''
    ImagePlus img - the image for which we're retrieving DAPI threshold
    '''
    def __init__(self, img):
         self.img = img

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
    Ask the user to determine a threshold to use for this image

    string label - The type of threshold being retrieved, eg DAPI

    return int - the threshold as set by the user
    '''
    def getThreshold(self, label):
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
    Create a new image from a specific channel of the image in this class

    string name - name of the new image
    int channel - the channel from which to build this new image

    return Image - new instance of this class wrapping the created stacked image
    '''
    def createStackedImage(self, name, channel):
        IJ.newImage(name, '16-bit black', 1908, 1908, 1)
        copy = Image(WindowManager.getImage(name))
        IJ.selectWindow(self.img.getTitle())
        initialSlice = self.img.getSlice()
        initialChannel = self.img.getC()
        self.img.setSlice(0)
        self.img.setC(channel)

        self.img.copy()
        copy.img.paste()

        self.img.setSlice(initialSlice)
        self.img.setC(initialChannel)
        return copy

