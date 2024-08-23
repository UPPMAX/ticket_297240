import sys
sys.path.append('/sw/bioinfo/Chromium-cellranger/7.1.0/bianca/lib/python/')
from cellranger import *



import sys
sys.path.append('/sw/bioinfo/Chromium-cellranger/7.1.0/bianca/lib/python/')
# sys.path.append('/home/richel/GitHubs/cellranger/lib/python')
from cellranger import *

exit()


# From https://stackoverflow.com/a/54956419
import importlib

pkg = importlib.import_module('~/GitHubs/cellranger/lib/python/cellranger')

# check if it's all there..
print(dir(pkg))


sys.modules[module_name] = module

import cellranger.matrix as cr_matrix

exit()
quit()

# from ../cellranger/lib/python import cellranger

# # From https://stackoverflow.com/a/55187291
# import os

# cwd = os.getcwd()

# new_dir = '/sw/bioinfo/Chromium-cellranger/7.1.0/bianca/lib/python/cellranger/'
# list_dir = os.listdir(new_dir) # Find all matching

# os.chdir(new_dir)
# for i in range(len(list_dir)): # Import all of them (or index them in some way)
#     module = list_dir[i][0:-3] # Filter off the '.py' file extension
#     from module import *
# os.chdir(cwd)

# Back to what the user needs
import cellranger
import cellranger.matrix as cr_matrix
