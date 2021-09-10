# OHSU Unni Lab Scripting

Repository with python scripts for Fiji used in OHSU Unni Lab. 

# Getting started

## Prereq: Fiji

Download Fiji from https://imagej.net/software/fiji/downloads

Move/Unzip Fiji wherever you want

You should now have a Fiji.app folder on your system, within which is the ImageJ executable file (to run the ImageJ program), and folders like `scripts` and `jars`

![Image](./readme/images/fiji_fresh_install.PNG)

## Adding UnniImaging

Download the latest release by going to https://github.com/pvlaraia/ohsu_lab/releases and downloading the UnniImaging.zip file from the most recent release
Place the UnniImaging.zip file inside of the Fiji.app folder (see pre-reqs) ie place UnniImaging.zip alongside the ImageJ exe file. 

![Image](./readme/images/fiji_with_unni_zip.PNG)

Now unzip/extract the contents of UnniImaging.zip. That's going to add files to the existing `scripts` & `jars` folders. To confirm that this worked, you should see an ohsu folder in both `scripts` and `jars/Lib`

![](./readme/gifs/unni_extracting.gif)

# Run Imaging

After going through the above steps, open ImageJ, and you should see a new option in the title bar labeled 'OHSU' (next to 'Window' and 'Help'). Select `OHSU -> Run Imaging` to run the test, and follow the prompts. It'll ask for an input folder (The folder containing the images you intend to procss), and an output folder (where the results will be saved)

![](./readme/gifs/running_imaging.gif)

# Colocalisation Test "Results Window" bugfix

If you try to run the script on multiple images, and on the attempt to process the 2nd of n images, you see an error that says 'Results window not found' or something along those lines, you've encountered a bug in the default Colocalisation Test plugin. 

![Image](./readme/images/unni_results_window_bug.png)

In order to fix that, you can go to https://github.com/pvlaraia/Colocalisation_Analysis/releases

Download the .jar file in the most recent release, and follow the instructions to replace the existing Colocalisation Test jar file in the `plugins` folder

![](./readme/gifs/coloc_plugin.gif)
