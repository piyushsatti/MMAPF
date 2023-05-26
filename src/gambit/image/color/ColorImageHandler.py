import cv2
from gambit.helpers.DatasetHandler import DatasetHandler

class ColorImageHandler (DatasetHandler):
    
    def __init__(self, abs_path:str):
        super().__init__(abs_path)
        self.load_file_names()
    
    def color_image_handler(self) -> None:
        '''
        Yields three ImageHandler objects, one for each
        R, G, and B channels
        '''
        for file_path in self.file_paths:
            yield file_path, cv2.imread(file_path, 1)