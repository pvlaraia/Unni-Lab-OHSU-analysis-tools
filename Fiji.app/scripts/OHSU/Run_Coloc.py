from ohsu.file_manager.directory import IJDirectory
from ij import IJ
from ij.gui import GenericDialog


def run():
    gd = GenericDialog('Instructions')
    gd.addMessage('1. When prompted, choose the input folder (Where are the files we want to analyze?)')
    gd.addMessage('2. When prompted, choose the output folder (Where should we put the results?)')
    gd.addMessage('3. Start processing images from the input folder. For each image, you will be asked to select a DAPI Threshold.')
    gd.showDialog()
    if (gd.wasCanceled()):
        return 0



    inDir = IJDirectory('Input')
    outDir = IJDirectory('Output')

    IJ.log(inDir.path)
    IJ.log(outDir.path)

run()