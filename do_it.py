
# From https://stackoverflow.com/a/55187291
import os

cwd = os.getcwd()

new_dir = '/sw/bioinfo/Chromium-cellranger/7.1.0/bianca/lib/python/cellranger/'
list_dir = os.listdir(new_dir) # Find all matching

os.chdir(new_dir)
for i in range(len(list_dir)): # Import all of them (or index them in some way)
    module = list_dir[i][0:-3] # Filter off the '.py' file extension
    from module import *
os.chdir(cwd)

# Back to what the user needs
import cellranger
import cellranger.matrix as cr_matrix
