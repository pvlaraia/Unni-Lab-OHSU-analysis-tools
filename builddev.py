import sys
import os
import shutil

print("Starting...")

if len(sys.argv) < 2:
    print('''
    Usage: python test.py <path/to/Fiji.app>
    ''')
    exit(-1)

fiji_path = sys.argv[1];  

# Delete existing Lib & Script
lib_path = '{}/jars/Lib/ohsu'.format(fiji_path)
script_path = '{}/scripts/OHSU'.format(fiji_path)
if (os.path.exists(lib_path)):
    print("Removing existing lib...")
    shutil.rmtree(lib_path)

if (os.path.exists(script_path)):
    print("Remove existing scripts...")
    shutil.rmtree(script_path)
    

# Copy over lib from project
if not os.path.exists('{}/jars/Lib'.format(fiji_path)):
    print("Create Lib folder...")
    os.mkdir('{}/jars/Lib'.format(fiji_path))


print("Copy files...")
shutil.copytree('./Fiji.app', fiji_path, dirs_exist_ok=True)