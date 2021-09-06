import os
from ohsu.file_manager.directory import IJDirectory
from ij import IJ, WindowManager
from ij.gui import GenericDialog, NonBlockingGenericDialog

SliceNumber = 0
Syn1Threshold = 2580
PARThreshold = 1800



def run():
    gd = GenericDialog('Instructions')
    gd.addMessage('1. When prompted, choose the input folder (Where are the files we want to analyze?)')
    gd.addMessage('2. When prompted, choose the output folder (Where should we put the results?)')
    gd.addMessage('3. Start processing images from the input folder. For each image, you will be asked to select a DAPI Threshold.')
    gd.showDialog()
    if (gd.wasCanceled()):
        return 0

    inDir = IJDirectory('Input')

    for root, _dirs, files in os.walk(inDir.path):
        for filename in files:
            imgpath = os.path.join(root, filename)
            processImage(imgpath)

'''
ImagePlus img - ImagePlus img that we're gonna process
'''
def processImage(imgpath):
    IJ.run("Bio-Formats", "open=["+imgpath+"] autoscale color_mode=Default rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT")
    img = IJ.getImage()
    IJ.log(img.getTitle())
    dapi_threshold = getDAPIThreshold()
    img.close()

'''
Get the user to input the DAPI threshold to use for the currently open image. 
Open the threshold tool to assist in finding the correct value
'''
def getDAPIThreshold():
    IJ.run('Threshold...')
    threshold_window = WindowManager.getWindow('Threshold')

    gd = NonBlockingGenericDialog('Get DAPI Threshold')
    gd.addMessage('Tweak the threshold slider until it looks right, then enter that number below as the DAPI Threshold to use for this image')
    gd.addNumericField('DAPI Threshold', 0)
    gd.hideCancelButton()
    gd.showDialog()
    dapi_threshold = int(gd.getNumericFields()[0].getText())

    threshold_window.close()
    IJ.log(str(dapi_threshold))
    return dapi_threshold

run()