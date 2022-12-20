import os, cv2, numpy as np
from classes.ImageHandler import ImageHandler

class DatasetHandler:
    '''
    This class is responsible for maintaining the noisy and non-noisy
    image states. Given a directory, it processes generators for images
    or videos contained within the directory (sub-folder with a particular 
    naming convention).
    '''
    def __init__(self, rel_path:str) -> None:
        self.path = os.path.join(os.getcwd(), rel_path)
        self.files:dict = {}
        self.sort_files()

    def sort_files(self) -> None:
        files_dict = {
            'bnw_images':[],
            'clr_images':[],
            'video':[]
        }
        for (root,dirs,files) in os.walk(self.path, topdown=True):
            for file in files:
                file_path = os.path.join(os.path.join(self.path, root, file))
                if root .endswith('Black and White'):
                    files_dict['bnw_images'].append(file_path)
                elif root.endswith('Colored'):
                    files_dict['clr_images'].append(file_path)
                elif root.endswith('Video'):
                    files_dict['video'].append(file_path)

        self.files = files_dict

    def bnw_image_handler(self) -> None:
        '''
        Yields an ImageHandler object
        '''
        for file in self.files['bnw_images']:
            yield file, ImageHandler(cv2.imread(file, 0))

    def clr_image_handler(self) -> None:
        '''
        Yields three ImageHandler objects, one for each
        R, G, and B channels
        '''
        for file in self.files['clr_images']:
            clr_img = cv2.imread(file, 1)
            yield file, ImageHandler(clr_img[:,:,0]), ImageHandler(clr_img[:,:,1]), ImageHandler(clr_img[:,:,2])


    def video_frame_handler(self) -> None:
        '''
        Reads a video from file as images (frame)
        Yields three ImageHandler objects, one for each
        R, G, and B channels
        '''
        for file in self.files['video']:
            cap = cv2.VideoCapture(file)
            if (cap.isOpened() == False): 
                print(f"Unable to read video feed for {file}")
            size = (int(cap.get(3)), int(cap.get(4)))
            yield True, file, size
            while(True):
                ret, frame = cap.read()
                if ret == True:
                    yield False, file, size, ImageHandler(frame[:,:,0]), ImageHandler(frame[:,:,1]), ImageHandler(frame[:,:,2])
                else:
                    break
            cap.release()
        
    def __del__(self):
        cv2.destroyAllWindows()

if __name__ == '__main__':
    dataset_handler = DatasetHandler(
        os.path.join(
            os.curdir, 
            'Test Data'
        )
    )