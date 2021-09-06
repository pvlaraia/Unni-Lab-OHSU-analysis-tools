import sys
import os
import inspect
from ij import IJ;

'''
Add current path to sys path so that python knows it can look for modules
(like file_manager) in subdirectories of this plugin
'''
current_filename = inspect.getframeinfo(inspect.currentframe()).filename
current_path = os.path.dirname(os.path.abspath(current_filename))
# If running directly from Fiji plugin bar, it gets the path wrong because it leaves out the scripts folder, idk why
sys.path.append(os.getcwd() + '\scripts' + current_path.split(os.getcwd())[1])
sys.path.append(current_path)
for path in sys.path:
    IJ.log(path)

from file_manager.directory import IJDirectory

def run():
    IJ.log('Starting...')
    for path in sys.path:
        IJ.log(path)
    inDir = IJDirectory('Input')
    outDir = IJDirectory('Output')

    IJ.log(inDir.path)
    IJ.log(outDir.path)

run()