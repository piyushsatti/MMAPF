import os, cv2

class DatasetHandler:
    '''
    This class is responsible for maintaining the noisy and non-noisy
    image states. Given a directory, it processes generators for images
    or videos contained within the directory (sub-folder with a particular 
    naming convention).
    '''
    def __init__(self, abs_path:str) -> None:
        self.abs_path = abs_path
        self.file_paths:set = self.load_file_names()

    def load_file_names(self) -> set:
        file_paths = set()
        for (root,dirs,files) in os.walk(
            self.abs_path, 
            topdown=True
        ):
            for file in files:
                file_paths.add(os.path.join(root, file))

        return file_paths
    
    def __del__(self):
        cv2.destroyAllWindows()
        
if __name__ == '__main__':
    test_image_paths = DatasetHandler('''C:\\Users\\piyus\\Documents\\GitHub\\MMAPF\\sample_data''')
    print(test_image_paths.file_paths)