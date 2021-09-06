from ohsu.OHSUImaging import run_coloc
from ij import IJ

def run():
    IJ.log('Starting...')
    run_coloc()

run()