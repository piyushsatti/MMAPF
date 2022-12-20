import numpy as np, cv2
from skimage.util import random_noise

class ImageHandler:
    
    def __init__(self, img) -> None:
        self.Img = img

    def add_noise(self, noise_type:str='s&p', noise_factor=0.3) -> None:
        nImg = random_noise(self.Img, mode=noise_type, amount=noise_factor)
        self.nImg = np.array(255*nImg, dtype = 'uint8')