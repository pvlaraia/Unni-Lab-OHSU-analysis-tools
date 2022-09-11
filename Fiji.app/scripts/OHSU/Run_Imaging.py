import codecs
import csv
import os

from ohsu.analysis.measurements import Measurements
from ohsu.analysis.nucleolus import Nucleolus
from ohsu.config.colocalisation_config import ColocalisationConfig
from ohsu.config.config import Config
from ohsu.config.core_config import CoreConfig
from ohsu.config.foci_config import FociConfig
from ohsu.file_manager.directory import IJDirectory
from ohsu.helpers.roi_manager import RoiManager
from ohsu.image.image import Image
from ohsu.results.results import Results
from ij import IJ, WindowManager
from ij.gui import GenericDialog

HEADER_KEY = '__HEADER__'

def run():

    validateConfig()

    gd = GenericDialog('Instructions')
    gd.addMessage('1. When prompted, choose the input folder (Where are the files we want to analyze?)')
    gd.addMessage('2. When prompted, choose the output folder (Where should we put the results?)')
    gd.addMessage('3. Start processing images from the input folder. For each image, you will be asked to select a Threshold.')
    gd.addMessage('Channels:')
    for channel, label in CoreConfig.getChannels().items():
        gd.addMessage('{} - {}'.format(channel, label))
    gd.showDialog()
    if (gd.wasCanceled()):
        return 0

    inDir = IJDirectory('Input')
    outDir = IJDirectory('Output')

    ImageProcessor(inDir, outDir).run()
    Config.close()

def validateConfig():
    CoreConfig.validate()
    ColocalisationConfig.validate()


class ImageProcessor:
    def __init__(self, inputDir, outputDir):
        self.inputDir = inputDir
        self.outputDir = outputDir
        self.roiMeasurements = None
        self.fociMeasurements = {}
        for channel in (FociConfig.getChannels() or []):
            self.fociMeasurements[channel] = {}
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
        channels = CoreConfig.getChannels()
        for channel, cellData in self.roiMeasurements.items():
            self.saveCollection(cellData, '{}_cells.csv'.format(channels[channel]))
        
        if ColocalisationConfig.getChannel() is not None:
            self.saveCollection(self.colocalisation, 'colocalisation.csv')

        for channel, fociData in self.fociMeasurements.items():
            self.saveCollection(fociData, '{}_foci.csv'.format(channels[channel]))

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

        # Cell Measurements
        self.roiMeasurements = Measurements(img, imgName, self.outputDir).run()

        slices = img.getSlices()
        # Colocalisation
        coloc_channel = ColocalisationConfig.getChannel()
        if (coloc_channel is not None and CoreConfig.getChannels().has_key(coloc_channel)):
            headings, coloc_measurements = self.getColocalisationForImg(slices[coloc_channel])
            self.colocalisation[HEADER_KEY] = headings
            self.colocalisation[imgName] = coloc_measurements

        # Foci
        foci_channels = FociConfig.getChannels() or []
        if foci_channels:
            for foci_channel in foci_channels:
                headings, measurements = self.getFociForImg(slices[foci_channel])
                self.fociMeasurements[foci_channel][HEADER_KEY] = headings
                for roiIndex, measurement in measurements.items():
                    self.fociMeasurements[foci_channel][imgName + '_ROI_' + roiIndex] = measurement

        # close everything
        RoiManager().dispose()
        img.closeSlices()
        img.close()
        Results().close()
        # Nucleolus(images.values()[3], images.values()[1], True).run()


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


    '''
    Given an image, run Colocalisation Test plugin

    @img Image - the image to run Coloc on

    return tuple([headers], [[roi measurements]])
    '''
    def getColocalisationForImg(self, img):
        roiM = RoiManager().get()
        headers = None
        collection = []
        channels = CoreConfig.getChannels()
        colocChannel = ColocalisationConfig.getChannel()
        for i in range(0, roiM.getCount()):
            img.select()
            roiM.select(i)
            IJ.run('Colocalization Test', 'channel_1={} channel_2={} roi=[ROI in channel {} ] randomization=[Fay (x,y,z translation)] current_slice'.format(channels["1"], channels["2"], colocChannel))
            resultsTextWindow = WindowManager.getWindow('Results')
            textPanel = resultsTextWindow.getTextPanel()
            headings = textPanel.getOrCreateResultsTable().getColumnHeadings().split("\t")
            data = textPanel.getLine(0).split("\t")
            headers = headings if headers is None else headers
            collection.append(data)
        return (headers, collection)

    '''
    Given an img, the channel, and original imgName, run Foci analysis and collect data

    @img Image - the image to run foci on
    @channel string - the channel number
    @imgName string - name of the original image

    return tuple([headers], {roi, [measurements]}) - measurements grouped by ROI
    '''
    def getFociForImg(self, img):
        headers = None
        collection = {}
        img.select()
        IJ.setThreshold(img.getThreshold(img.img.getTitle()), 65535)
        roiM = RoiManager().get()
        for i in range(0, roiM.getCount()):
            img.select()
            roiM.select(i)
            IJ.run("Analyze Particles...", "size=3-Infinity pixel display clear")
            results = Results()
            headings, measurements = results.getResultsArray()
            headers = headers or headings
            collection[str(i+1)] = measurements
            results.close()
        return (headers, collection)

run()