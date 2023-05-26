from helpers.DatasetHandler import DatasetHandler

class ColorImageHandler (DatasetHandler(abs_path)):
    
    def __init__(self, abs_path:str):
        super().__init__(abs_path)
    
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