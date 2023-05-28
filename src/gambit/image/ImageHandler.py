import cv2
from gambit.helpers.DatasetHandler import DatasetHandler

class ImageHandler (DatasetHandler):
    
    def __init__(self, abs_path:str):
        super().__init__(abs_path)
        self.load_file_names()
    
    def color_image_handler(self):
        for file_path in self.file_paths:
            yield file_path, cv2.imread(file_path, 1)
    
    def grayscale_image_handler(self):
        for file_path in self.file_paths:
            yield file_path, cv2.imread(file_path, 0)