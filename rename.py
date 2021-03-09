# coding:utf-8
import glob
import os
for filepath in glob.glob("./png/*/*.png"):
    comic_num = filepath.split("_")[1][0:3]
    file_name = filepath.split("/")[-1]
    file_directory = filepath[0:-len(file_name)]
    new_filepath = file_directory+comic_num+"_"+file_name
    print(new_filepath)
    os.rename(filepath, new_filepath)
