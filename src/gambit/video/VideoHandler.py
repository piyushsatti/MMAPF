import os, cv2
from gambit.helpers.DatasetHandler import DatasetHandler

class VideoHandler (DatasetHandler):
    
    def __init__(self, abs_path:str):
        super().__init__(abs_path)
    
    def frame_handler(self, video_capture_object_pointer):
        '''
        Takes the capture object and
        yields the frame for the
        video capture object
        '''
        while(True):
                ret, frame = video_capture_object_pointer.read()
                if ret == True:
                    yield frame
                else:
                    break
        video_capture_object_pointer.release()
    
    def video_handlers(self):
        '''
        For each file in the file paths
        creates a video handler object
        and yields the path, video 
        dimensions and capture object
        '''
        for file_path in self.file_paths:
            video_capture_object_pointer = cv2.VideoCapture(file_path)
            if (video_capture_object_pointer.isOpened() == False):
                print(f"Unable to read video feed for {os.path.split(file_path)[-1]}")
            video_fps = video_capture_object_pointer.get(cv2.CAP_PROP_FPS)
            video_size = (
                int(video_capture_object_pointer.get(3)), 
                int(video_capture_object_pointer.get(4))
            )
            yield file_path, video_fps, video_size, video_capture_object_pointer