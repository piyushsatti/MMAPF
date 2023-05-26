import os, sys, time
import numpy as np, multiprocessing as mp

# Project module imports
from gambit.user_menu.user_menu import userOptionsMenu
from gambit.image.color.color import color_image_dataset_process_handler
from gambit.image.grayscale.grayscale import grayscale_image_dataset_process_handler
from gambit.video.color.color import color_video_dataset_process_handler
from gambit.video.grayscale.grayscale import color_video_dataset_process_handler

# Filters
from filters.SMF import SMF
from filters.MMAPF import MMAPF

def main():

    (
        selected_input_media_type, 
        selected_input_media_color, 
        input_data_abs_path, 
        output_data_abs_path,
        max_number_of_processes
    ) = userOptionsMenu()
    
    color_video_dataset_process_handler(
        input_data_abs_path,
        output_data_abs_path,
        max_number_of_processes,
        0.3,
        SMF, MMAPF
    )

if __name__ == "__main__": 
    main()