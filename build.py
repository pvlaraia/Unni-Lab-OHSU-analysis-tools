import sys
import os
import shutil

if len(sys.argv) < 2:
    print('''
    Usage: python build.py <path/to/Fiji.app>
    ''')
    exit(-1)

fiji_path = sys.argv[1];  

# Delete existing Lib & Script
lib_path = '{}/jars/Lib/ohsu'.format(fiji_path)
script_path = '{}/scripts/OHSU'.format(fiji_path)
if (os.path.exists(lib_path)):
    shutil.rmtree(lib_path)

if (os.path.exists(script_path)):
    shutil.rmtree(script_path)
    

# Copy over lib from project
if not os.path.exists('{}/jars/Lib'.format(fiji_path)):
    os.mkdir('{}/jars/Lib'.format(fiji_path))


shutil.copytree('./Fiji.app', fiji_path, dirs_exist_ok=True)