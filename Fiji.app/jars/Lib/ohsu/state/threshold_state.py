
class ThresholdState(object):
    def init(self):
        self.state = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ThresholdState, cls).__new__(cls)
            cls.instance.init()
        return cls.instance

    '''
    get a previously set threshold for a given image

    return int threshold
    '''
    def get(self, image):
        return self.state[image] if image in self.state else None


    '''
    set the threshold used for a image in program state

    return void
    '''
    def set(self, image, threshold):
        self.state[image] = threshold