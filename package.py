import sys
import shutil

if len(sys.argv) < 2:
    print('''
    Usage: python package.py <version>
    ''')
    exit(-1)  

version = sys.argv[1]; 

shutil.make_archive('UnniImaging-{}'.format(version), 'zip', './Fiji.app')
