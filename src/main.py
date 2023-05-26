import os, sys, time
import numpy as np, multiprocessing as mp

# Project module imports
from gambit.image.color.color import color_dataset_process_handler
from gambit.user_menu.user_menu import userOptionsMenu

# Filters
from filters.SMF import SMF
from filters.MMAPF import MMAPF

def main(data_set_dir:str='Test Images'):

    (
        selected_input_media_type, 
        selected_input_media_color, 
        input_data_abs_path, 
        output_data_abs_path,
        max_number_of_processes
    ) = userOptionsMenu()
    
    color_dataset_process_handler(
        input_data_abs_path, 
        output_data_abs_path,
        max_number_of_processes,
        0.3,
        SMF, MMAPF
    )
    
    # video_test = video_processing(dataset, 30, SMF, MMAPF)

if __name__ == "__main__": 
    main()