import os
from classes.DatasetHandler import DatasetHandler

def bnw_processing(dataset:DatasetHandler, *args) -> None:
    '''
    Takes the dataset object and uses the bnw
    generator to process and store the images
    '''
    dataset_output = {}
    for file_path, img in dataset.bnw_image_handler():
        file_name = os.path.split(file_path)[-1]
        img.add_noise()
        outImg = {
            f'true_image': img.Img,
            f'noisy_image': img.nImg
        }
        for arg in args:
            outImg[f'{arg.__name__}'] = arg(img.nImg)
        
        dataset_output[f"{file_name}"] = outImg
    return dataset_output