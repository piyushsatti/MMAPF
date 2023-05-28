import numpy as np
from skimage.util import random_noise

def add_noise_to_color_image(img, noise_type:str='s&p', noise_factor=0.7):
    n_img = np.zeros(img.shape, dtype = 'uint8')
    for layer in range(3):
        n_img[..., layer] = np.array(
            255*(
                random_noise(img[..., layer], mode=noise_type, amount=noise_factor)
            ), 
            dtype = 'uint8'
        ) 
    return n_img

def add_noise_to_grayscale_image(img, noise_type:str='s&p', noise_factor=0.7):
    return np.array(
        255*(
            random_noise(img, mode=noise_type, amount=noise_factor)
        ), 
        dtype = 'uint8'
    )