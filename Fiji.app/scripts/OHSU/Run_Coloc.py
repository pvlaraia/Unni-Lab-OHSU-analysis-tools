import os
from ohsu.file_manager.directory import IJDirectory
from ohsu.image.image import Image
from ij import IJ
from ij.gui import GenericDialog

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
    main = Image.fromCZI(imgpath)
    main.getThreshold('DAPI')
    syn1 = main.createStackedImage('Syn1', 1)
    gh2ax = main.createStackedImage('gH2AX', 2)
    dapi = main.createStackedImage('DAPI', 3)
    main.close()

    syn1.close()
    gh2ax.close()
    dapi.close()

run()