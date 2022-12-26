import os, cv2, multiprocessing as mp, time
from classes.DatasetHandler import DatasetHandler

def write_output_images(rel_path, file_name, outImgs):
    folder_name = os.path.split(rel_path)[-1]
    new_folder_name = folder_name + ' Out'
    file_to_folder_name = file_name.split('.')[0]
    path = os.path.join(os.getcwd(), new_folder_name, 'Black and White', file_to_folder_name)
    if ~os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception as e:
            print(f"--- Exception in {file_name} ---\n{e}")
    for key in outImgs.keys():
        cv2.imwrite(
            os.path.join(path, f'{key}.tif'),
            outImgs[key]
        )

def process_bnw_dataset_instance(rel_path, file_path, img, args) -> None:
    '''
    Takes the dataset object and uses the bnw
    generator to process and store the images
    '''
    file_name = os.path.split(file_path)[-1]
    start_time = time.time()
    img.add_noise()
    outImg = {
        f'true_image': img.Img,
        f'noisy_image': img.nImg
    }
    for arg in args:
        outImg[f'{arg.__name__}'] = arg(img.nImg)
    print(f"--- Took {time.time() - start_time} seconds to denoise {file_name} ---")
    write_output_images(rel_path, file_name, outImg)

def process_bnw_dataset(max_num_proc, dataset:DatasetHandler, *denoising_functions):
    '''
    Takes the dataset object and uses the clr
    generator to create and store the images
    using multiprocessing python module
    '''
    procs = []
    for file_path, img in dataset.bnw_image_handler():
        rel_path = dataset.rel_path
        # process_clr_dataset_instance(dataset=dataset, file_path=file_path, img_channels=img_channels, denoising_functions=denoising_functions)
        proc = mp.Process(
            target=process_bnw_dataset_instance, 
            args=(rel_path, file_path, img, denoising_functions)
        )
        # start the process, a non-daemon process auto-joins at the end implicitly
        proc.start()
        # add process to the processes list
        procs.append(proc)
        # a foreverloop until the number of processes fall below the maximum allowed number of processes
        while [proc.is_alive() for proc in procs].count(True) >= max_num_proc:
            # sleep for 1 second for a process to auto-join
            time.sleep(1)
            # continue after 1 second
            continue
    
    [proc.join() for proc in procs]