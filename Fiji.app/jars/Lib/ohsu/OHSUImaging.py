import sys
from ij import IJ;

from ohsu.file_manager.directory import IJDirectory

def run_coloc():
    for path in sys.path:
        IJ.log(path)
    inDir = IJDirectory('Input')
    outDir = IJDirectory('Output')

    IJ.log(inDir.path)
    IJ.log(outDir.path)