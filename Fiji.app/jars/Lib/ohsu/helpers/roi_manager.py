from ij.plugin.frame import RoiManager as IJRoiManager

class RoiManager(object):
    def init(self):
        self.roiManager = IJRoiManager()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(RoiManager, cls).__new__(cls)
            cls.instance.init()
        return cls.instance

    '''
    Get a reference to our roiManager, create if non exists

    return RoiManager
    '''
    def get(self):
        if self.roiManager is None:
            self.roiManager = IJRoiManager()
        return self.roiManager
    
    '''
    Get rid of our RoiManager

    return void
    '''
    def dispose(self):
        if (self.roiManager is not None):
            self.roiManager.reset()
            self.roiManager.close()
            self.roiManager = None
