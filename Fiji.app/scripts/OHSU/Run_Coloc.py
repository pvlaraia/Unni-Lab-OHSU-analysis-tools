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

    for root, _dirs, files in os.walk(inDir.path):
        for filename in files:
            imgpath = os.path.join(root, filename)
            processor = ImageProcessor(imgpath, outDir)
            processor.run()


class ImageProcessor:
    def __init__(self, imgpath, outDir):
        self.outDir = outDir
        self.roiManager = None
        self.filename = os.path.basename(imgpath)
        self.filenameNoExtension = os.path.splitext(self.filename)[0]
        self.img = Image.fromCZI(imgpath)
    
    def run(self):
        dapi_threshold = self.img.getThreshold('DAPI')

        # routine to select and create single images of the Syn1, gH2AX and DAPI channels and then close the parent z-stack
        syn1 = self.img.createStackedImage('Syn1', 1)
        gh2ax = self.img.createStackedImage('gH2AX', 2)
        dapi = self.img.createStackedImage('DAPI', 3)
        self.img.close()

        # routine to create ROIs for each nucleus using a set threshold, saves a nuclear mask image and then closes it, saves nuclei properties and the nuclear ROIs
        # save DAPI TIFF
        dapi.select()
        IJ.setThreshold(dapi_threshold, 65535)

        self.getRoiManager().runCommand('Show All with labels')
        IJ.run("Analyze Particles...", "size=500-Infinity show=Outlines add slice")
        drawing = IJ.getImage()
        tif_name = 'Drawing of {}.tif'.format(self.filenameNoExtension)
        IJ.saveAsTiff(drawing, '{}/{}'.format(self.outDir.path, tif_name))
        drawing.close()

        self.saveDapiMultiMeasure(dapi)

        self.getRoiManager().runCommand('Save', '{}/{}_RoiSet.zip'.format(self.outDir.path, self.filenameNoExtension))


        # close everything
        self.disposeRoiManager()
        syn1.close()
        gh2ax.close()
        dapi.close() 


    def saveDapiMultiMeasure(self, dapi):
        dapi.select()
        nRoi = self.getRoiManager().getCount()
        for i in range(0, nRoi):
            self.getRoiManager().select(i)
            self.getRoiManager().runCommand('Measure')
        IJ.saveAs('Results', '{}/{}_nuclei_mask_properties.csv'.format(self.outDir.path, self.filenameNoExtension))
        self.closeResults()
        
    
    def getRoiManager(self):
        if self.roiManager is None:
            IJ.log('new roimanager')
            self.roiManager = RoiManager()
        return self.roiManager
    
    def disposeRoiManager(self):
        if (self.roiManager is not None):
            self.roiManager.reset()
            self.roiManager.close()
            self.roiManager = None
    
    def closeResults(self):
        results = WindowManager.getWindow('Results')
        results.close()

run()