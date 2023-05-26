from helpers.DatasetHandler import DatasetHandler

class GrayscaleImageHandler (DatasetHandler(abs_path)):
    
    def __init__(self, abs_path:str):
        super().__init__(abs_path)
    
    def grayscale_image_handler(self) -> None:
        '''
        Yields an ImageHandler object
        '''
        for file in self.files['bnw_images']:
            yield file, ImageHandler(cv2.imread(file, 0))