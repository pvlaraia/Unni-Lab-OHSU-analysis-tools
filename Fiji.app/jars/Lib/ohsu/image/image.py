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
        IJ.log(img.getTitle())
        return cls(img)

    '''
    Close this image
    '''
    def close(self):
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