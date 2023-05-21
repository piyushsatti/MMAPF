import os, sys, time
import numpy as np, multiprocessing as mp

# Project module imports
from helpers.bnw_helper import process_bnw_dataset
from helpers.clr_helper import process_clr_dataset
from helpers.video_helper import video_processing
from classes.DatasetHandler import DatasetHandler

# Filters
from filters.SMF import SMF
from filters.MMAPF import MMAPF

def main(data_set_dir:str='Test Images'):
    dataset = DatasetHandler(data_set_dir)
    # process_bnw_dataset(8, dataset, SMF, MMAPF)
    # process_clr_dataset(8, dataset, SMF, MMAPF)
    video_test = video_processing(dataset, 30, SMF, MMAPF)

if __name__ == "__main__": 
    main('data\\test_data')