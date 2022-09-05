
class Nucleolus:
    def __init__(self, mainChannelImg, secondaryChannelImg, threshold, shouldInvertROI):
        self.threshold = threshold
        self.mainChannelImg = mainChannelImg
        self.secondaryChannelImg= secondaryChannelImg
        self.shouldInvertROI= shouldInvertROI

    def run():
        threshold = 1