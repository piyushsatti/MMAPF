import os, cv2, numpy as np
from skimage.util import random_noise

def add_noise_to_image(img, noise_type:str='s&p', noise_factor=0.7):
    return np.array(
        255*(
            random_noise(img, mode=noise_type, amount=noise_factor)
        ), 
        dtype = 'uint8'
    )

def write_output_image(abs_path, output_image):
    '''
        Writes Output Image to abs_path
    '''
    cv2.imwrite(abs_path, output_image)