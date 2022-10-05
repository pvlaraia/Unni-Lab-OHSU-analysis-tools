from ohsu.constants import HEADER_KEY
from ohsu.helpers.roi_manager import RoiManager
from ohsu.results.results import Results
from ij import IJ


class Foci:
    def __init__(self, img, channels):
        self.img = img
        self.channels = channels

    def run(self):
        foci_measurements = {}
        slices = self.img.getSlices()
        for foci_channel in self.channels:
                headings, measurements = self.getFociForChannel(slices[foci_channel])
                foci_measurements[foci_channel] = {HEADER_KEY: headings}
                for roiIndex, measurement in measurements.items():
                    foci_measurements[foci_channel][self.img.getName() + '_ROI_' + roiIndex] = measurement
        RoiManager().dispose()
        return foci_measurements

    '''
    Given an img, the channel, and original imgName, run Foci analysis and collect data

    @img Image - the image to run foci on
    @channel string - the channel number
    @imgName string - name of the original image

    return tuple([headers], {roi, [measurements]}) - measurements grouped by ROI
    '''
    def getFociForChannel(self, img):
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