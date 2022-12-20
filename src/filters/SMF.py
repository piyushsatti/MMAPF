import numpy as np
from PIL import Image, ImageFilter

def SMF(nImg:np.array):
    nImg_object = Image.fromarray(nImg)
    out_img = nImg_object.filter(ImageFilter.MedianFilter(size=3))
    return np.asarray(out_img)