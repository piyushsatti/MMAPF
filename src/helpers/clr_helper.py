import os, time, numpy as np, multiprocessing as mp
from classes.DatasetHandler import DatasetHandler

def clr_processing(dataset:DatasetHandler, *args):
    '''
    Takes the dataset object and uses the clr
    generator to create and store the images
    '''
    dataset_output = {}
    for file_path, *img_channels in dataset.clr_image_handler():
        file_name = os.path.split(file_path)[-1]
        assert img_channels[0].Img.shape == img_channels[1].Img.shape == img_channels[2].Img.shape, f"{file_name} Image Shape mismatch."
        shape = img_channels[0].Img.shape + (3,)
        Img = np.zeros(shape, dtype=np.uint8)
        nImg = np.zeros(shape, dtype=np.uint8)
        for id in range(3):
            Img[..., id] = img_channels[id].Img
            img_channels[id].add_noise()
            nImg[..., id] = img_channels[id].nImg
        outImg = {
            f'true_image': Img,
            f'noisy_image': nImg
        }
        for arg in args:
            outImg[f'{arg.__name__}'] = np.zeros(shape, dtype=np.uint8)
            start_time = time.time()
            procs = []
            for id in range(3):
                proc = mp.Process(target=arg, args=(img_channels[id].nImg,))
                procs.append(proc)
                proc.start()
            for proc in procs:
                proc.join()
            print(f"--- {arg.__name__} took {time.time() - start_time} seconds to denoise {file_name} ---")
        dataset_output[f"{file_name}"] = outImg
    return dataset_output