import codecs
import csv
import os

from ohsu.analysis.colocalisation import Colocalisation
from ohsu.analysis.foci import Foci
from ohsu.analysis.measurements import Measurements
from ohsu.analysis.nucleolus import Nucleolus
from ohsu.config.colocalisation_config import ColocalisationConfig
from ohsu.config.config import Config
from ohsu.config.core_config import CoreConfig
from ohsu.config.foci_config import FociConfig
from ohsu.config.nucleolus_config import NucleolusConfig
from ohsu.file_manager.directory import IJDirectory
from ohsu.helpers.roi_manager import RoiManager
from ohsu.image.image import Image
from ohsu.results.results import Results
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
        self.nucleolusMeasurements = None

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
        if self.roiMeasurements is not None:
            for channel, cellData in self.roiMeasurements.items():
                self.saveCollection(cellData, '{}_cells.csv'.format(channels[channel]))
        
        if ColocalisationConfig.getChannel() is not None:
            self.saveCollection(self.colocalisation, 'colocalisation.csv')

        for channel, fociData in self.fociMeasurements.items():
            self.saveCollection(fociData, '{}_foci.csv'.format(channels[channel]))

        if self.nucleolusMeasurements is not None:
            self.saveCollection(self.nucleolusMeasurements, 'nucleolus.csv')

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

        if CoreConfig.getShouldRunCellMeasurements():
            self.roiMeasurements = Measurements(img, self.outputDir).run()
        
        coloc_channel = ColocalisationConfig.getChannel()
        if (coloc_channel is not None and CoreConfig.getChannels().has_key(coloc_channel)):
            self.colocalisation = Colocalisation(img, coloc_channel).run()
            
        foci_channels = FociConfig.getChannels() or []
        if foci_channels:
            self.fociMeasurements = Foci(img, foci_channels).run()
            
        nucleolus_target_channel = NucleolusConfig.getTargetChannel()
        if nucleolus_target_channel is not None:
            self.nucleolusMeasurements = Nucleolus(img, True).run()

        # close everything
        RoiManager().dispose()
        img.closeSlices()
        img.close()
        Results().close()

run()