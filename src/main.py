import os, sys, cv2, numpy as np, time
import multiprocessing as mp

# Project module imports
from helpers.bnw_helper import bnw_processing
from helpers.clr_helper import clr_processing
from helpers.video_helper import video_processing
from classes.DatasetHandler import DatasetHandler

# Filters
from filters.SMF import SMF
from filters.MMAPF import MMAPF

def main(data_set_dir:str='Test Images'):
    dataset = DatasetHandler(data_set_dir)

    # Should be able to recreate the folder structure and save file to that
    
    
    bnw_test = bnw_processing(dataset, SMF, MMAPF)
    clr_test = clr_processing(dataset, SMF, MMAPF)
    video_test = video_processing(dataset, SMF, MMAPF)

if __name__ == "__main__": 
    main('Test Data') 