import os, sys, time
import numpy as np, multiprocessing as mp

# Project module imports
from gambit.helpers.user_menu import userOptionsMenu
from gambit.image.image_processor import image_dataset_process_handler
from gambit.video.video_processor import video_dataset_process_handler

# Filters
from filters.SMF import SMF
from filters.MMAPF import MMAPF

def main():
    # (
    #     selected_input_media_type, 
    #     selected_input_media_color, 
    #     input_data_abs_path, 
    #     output_data_abs_path,
    #     max_number_of_processes
    # ) = userOptionsMenu()
    
    selected_input_media_type = 'video'
    
    match (
        selected_input_media_type
    ):
        case 'image':
            image_dataset_process_handler(
                'grayscale',
                'C:\\Users\\piyus\\Documents\\GitHub\\MMAPF\\sample_data\\test_input\\Black_and_white',
                'C:\\Users\\piyus\\Documents\\GitHub\\MMAPF\\sample_data\\test_output',
                1,
                0.3,
                SMF, MMAPF
                 
            )
        case 'video':
            video_dataset_process_handler(
                'color',
                'C:\\Users\\piyus\\Documents\\GitHub\\MMAPF\\sample_data\\test_input\\Video',
                'C:\\Users\\piyus\\Documents\\GitHub\\MMAPF\\sample_data\\test_output',
                8,
                0.3,
                SMF, MMAPF
            )

if __name__ == "__main__": 
    main()