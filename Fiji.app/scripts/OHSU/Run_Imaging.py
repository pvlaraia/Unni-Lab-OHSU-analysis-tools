import codecs
import csv
import json
import os
from ohsu.config.config import Config
from ohsu.file_manager.directory import IJDirectory
from ohsu.image.image import Image
from ohsu.results.results import Results
from ij import IJ, WindowManager
from ij.gui import GenericDialog
from ij.plugin.frame import RoiManager

HEADER_KEY = '__HEADER__'

def run():

    config = Config.getConfig()
    channel1 = config["channels"]["1"]
    channel2 = config["channels"]["2"]
    channel3 = config["channels"]["3"]

    gd = GenericDialog('Instructions')
    gd.addMessage('1. When prompted, choose the input folder (Where are the files we want to analyze?)')
    gd.addMessage('2. When prompted, choose the output folder (Where should we put the results?)')
    gd.addMessage('3. Start processing images from the input folder. For each image, you will be asked to select a Threshold.')
    gd.addMessage('Channels:')
    gd.addMessage('Channel 1 - ' + channel1)
    gd.addMessage('Channel 2 - ' + channel2)
    gd.addMessage('Channel 3 - ' + channel3)
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
        self.channel1Cells = {}
        self.channel2Cells = {}
        self.channel3Cells = {}
        self.colocalisation = {}

    '''
    Main entrypoint, run the program. walk all the images in inputDir and process in sequence

    return void
    '''
    def run(self):
        for root, _dirs, files in os.walk(self.inputDir.path):
            for filename in files:
                imgpath = os.path.join(root, filename)
                self.processImage(imgpath)
        self.postProcessData()

    '''
    Over the course of running each image, we've aggregated the data in ImageProcessor, and after processing
    all images we want to save the aggregated data into individual csv files
    
    return void
    ''' 
    def postProcessData(self):
        channels = Config.getConfig()["channels"]
        self.saveCollection(self.channel1Cells, '{}_cells.csv'.format(channels["1"]))
        self.saveCollection(self.channel2Cells, '{}_cells.csv'.format(channels["2"]))
        self.saveCollection(self.channel3Cells, '{}_cells.csv'.format(channels["3"]))
        self.saveCollection(self.colocalisation, 'colocalisation.csv')

    '''
    Save a collection to a file
    
    @collection dict -  of type 
    {
        '__HEADER__' => ['header', 'columns'],
        'imgFileName' => [[measurements, for, roi1], [measurements, for, roi2], [measurements, for, roi3]]
    }

    @name str - name of the file

    return void
    '''
    def saveCollection(self, collection, name):
        with open('{}/{}'.format(self.outputDir.path, name), 'wb') as csvfile:
            csvfile.write(codecs.BOM_UTF8)
            writer = csv.writer(csvfile)
            headers = [header.encode('utf-8') for header in collection[HEADER_KEY]]
            writer.writerow([''] + headers)
            for imgName, measurements in sorted(collection.items()):
                if (imgName == HEADER_KEY):
                    continue
                writer.writerow([imgName])
                writer.writerows(map(lambda measurement_row: [''] + [entry.encode('utf-8') for entry in measurement_row], measurements))
        

    '''
    Process a single image by running the various ROI analyses/measurements

    @imgpath str - file path to the image being processed

    return void
    '''
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

        # DAPI
        headings, dapi_measurements = self.getRoiMeasurements(dapi)
        self.channel3Cells[HEADER_KEY] = headings
        self.channel3Cells[imgName] = dapi_measurements
        self.getRoiManager().runCommand('Save', '{}/{}_RoiSet.zip'.format(self.outputDir.path, imgName))

        # SYN1
        headings, syn1_measurements = self.getRoiMeasurements(syn1)
        self.channel1Cells[HEADER_KEY] = headings
        self.channel1Cells[imgName] = syn1_measurements

        # GH2AX
        headings, gh2ax_measurements = self.getRoiMeasurements(gh2ax)
        self.channel2Cells[HEADER_KEY] = headings
        self.channel2Cells[imgName] = gh2ax_measurements

        # Colocalisation
        headings, coloc_measurements = self.getColocalisationForImg(syn1)
        self.colocalisation[HEADER_KEY] = headings
        self.colocalisation[imgName] = coloc_measurements

        # close everything
        self.disposeRoiManager()
        syn1.close()
        gh2ax.close()
        dapi.close()
        Results().close()


    '''
    Given an image, run Colocalisation Test plugin

    @img Image - the image to run Coloc on

    return tuple([headers], [[roi measurements]])
    '''
    def getColocalisationForImg(self, img):
        roiM = self.getRoiManager()
        headers = None
        collection = []
        for i in range(0, roiM.getCount()):
            img.select()
            roiM.select(i)
            IJ.run('Colocalization Test', 'channel_1=Syn1 channel_2=gH2AX roi=[ROI in channel 1 ] randomization=[Fay (x,y,z translation)] current_slice')
            resultsTextWindow = WindowManager.getWindow('Results')
            textPanel = resultsTextWindow.getTextPanel()
            headings = textPanel.getOrCreateResultsTable().getColumnHeadings().split("\t")
            data = textPanel.getLine(0).split("\t")
            headers = headings if headers is None else headers
            collection.append(data)

        return (headers, collection)


    '''
    Get a reference to our roiManager, create if non exists

    return RoiManager
    '''
    def getRoiManager(self):
        if self.roiManager is None:
            self.roiManager = RoiManager()
        return self.roiManager
    
    '''
    Get rid of our RoiManager

    return void
    '''
    def disposeRoiManager(self):
        if (self.roiManager is not None):
            self.roiManager.reset()
            self.roiManager.close()
            self.roiManager = None


    '''
    Given an image, get ROI measurements

    @img Image - the image to run Coloc on

    return tuple([headers], [[roi measurements]])
    '''
    def getRoiMeasurements(self, img):
        roiM = self.getRoiManager()
        roiM.deselect()
        img.select()
        roiM.runCommand('Measure')
        results = Results()
        data = results.getResultsArray()
        results.close()
        return data

run()