import os
from ohsu.file_manager.directory import IJDirectory
from ohsu.image.image import Image
from ij import IJ, WindowManager
from ij.gui import GenericDialog
from ij.plugin.frame import RoiManager
from time import sleep

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

    ImageProcessor(inDir, outDir).run()


class ImageProcessor:
    def __init__(self, inputDir, outputDir):
        self.inputDir = inputDir
        self.outputDir = outputDir
        self.roiManager = None

    def run(self):
        for root, _dirs, files in os.walk(self.inputDir.path):
            for filename in files:
                imgpath = os.path.join(root, filename)
                self.processImage(imgpath)

    def processImage(self, imgpath):
        img = Image.fromCZI(imgpath)
        filename = os.path.basename(imgpath)
        imgName = os.path.splitext(filename)[0]

        dapi_threshold = img.getThreshold('DAPI')
        # routine to select and create single images of the Syn1, gH2AX and DAPI channels and then close the parent z-stack
        syn1 = img.createStackedImage('Syn1', 1)
        gh2ax = img.createStackedImage('gH2AX', 2)
        dapi = img.createStackedImage('DAPI', 3)
        img.close()

        # routine to create ROIs for each nucleus using a set threshold, saves a nuclear mask image and then closes it, saves nuclei properties and the nuclear ROIs
        # save DAPI TIFF
        dapi.select()
        IJ.setThreshold(dapi_threshold, 65535)

        self.getRoiManager().runCommand('Show All with labels')
        IJ.run("Analyze Particles...", "size=500-Infinity show=Outlines add slice")
        drawing = IJ.getImage()
        tif_name = 'Drawing of {}.tif'.format(imgName)
        IJ.saveAsTiff(drawing, '{}/{}'.format(self.outputDir.path, tif_name))
        drawing.close()

        self.measureRoiAndSave(dapi, imgName, 'nuclei_mask_properties.csv')
        self.getRoiManager().runCommand('Save', '{}/{}_RoiSet.zip'.format(self.outputDir.path, imgName))
        self.measureRoiAndSave(syn1, imgName, 'syn1_cell.csv')
        self.measureRoiAndSave(gh2ax, imgName, 'gh2ax_cell.csv')

        # close everything
        self.disposeRoiManager()
        syn1.close()
        gh2ax.close()
        dapi.close() 

    def getRoiManager(self):
        if self.roiManager is None:
            self.roiManager = RoiManager()
        return self.roiManager
    
    def disposeRoiManager(self):
        if (self.roiManager is not None):
            self.roiManager.reset()
            self.roiManager.close()
            self.roiManager = None

    def measureRoiAndSave(self, img, imgName, file_suffix):
        roiM = self.getRoiManager()
        roiM.deselect()
        img.select()
        roiM.runCommand('Measure')
        IJ.saveAs('Results', '{}/{}_{}'.format(self.outputDir.path, imgName, file_suffix))
        self.closeResults()

    def closeResults(self):
        results = WindowManager.getWindow('Results')
        results.close()

run()