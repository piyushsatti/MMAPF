import os, time, datetime, cv2, numpy as np, multiprocessing as mp
from gambit.image.color.ColorImageHandler import ColorImageHandler
from gambit.helpers.image_functions import add_noise_to_image, write_output_image

def process_color_image(file_path, output_data_abs_path, color_img, noise_factor, denoising_functions):
    complete_path_as_list = os.path.split(file_path)
    file_name = complete_path_as_list[-1]
    file_extension = '.tif'
    shape = color_img.shape
    # Generating the noisy image
    n_img = np.zeros(shape, dtype=np.uint8)
    for layer in range(3):
        n_img[..., layer] = add_noise_to_image(
            img=color_img[..., layer],
            noise_type='s&p',
            noise_factor=noise_factor
        )
    # Writing the true and noisy image
    write_output_image(
        os.path.join(
            output_data_abs_path, 
            f'{file_name.split("_")[0]}_{color_img.shape[0]}_{color_img.shape[1]}_color_true_0' + file_extension
        ), 
        color_img
    )
    write_output_image(
        os.path.join(
            output_data_abs_path, 
            f'{file_name.split("_")[0]}_{color_img.shape[0]}_{color_img.shape[1]}_color_noisy_1'  + file_extension
        ), 
        n_img
    )
    # denoising and writing the filtered images
    for denoising_function in denoising_functions:
        filter_output_image = np.zeros(shape, dtype=np.uint8)
        for layer in range(3):
            filter_output_image[..., layer] = denoising_function(n_img[..., layer])
        write_output_image(
            os.path.join(
                output_data_abs_path, 
                f'{file_name.split("_")[0]}_{color_img.shape[0]}_{color_img.shape[1]}_color_noisy_{noise_factor}_{denoising_function.__name__}'  + file_extension
            ), 
            filter_output_image
        )

def color_dataset_process_handler(
    input_data_abs_path, 
    output_data_abs_path,
    max_number_of_processes, 
    noise_factor, 
    *denoising_functions
):
    '''
    Takes the dataset object and uses the color
    generator to create and store the images
    using multiprocessing python module
    '''
    procs = []
    process_start_time = time.time()
    color_image_handler_instance = ColorImageHandler(input_data_abs_path)
    for file_path, color_img in color_image_handler_instance.color_image_handler():
        proc = mp.Process(
            target=process_color_image, 
            args=(file_path, output_data_abs_path, color_img, noise_factor, denoising_functions)
        )
        proc.start()
        procs.append(proc)
        while [proc.is_alive() for proc in procs].count(True) >= max_number_of_processes:
            time.sleep(1)
            continue
    [proc.join() for proc in procs]
    process_end_time = time.time()
    process_start_date = datetime.datetime.fromtimestamp(process_start_time)
    process_end_date = datetime.datetime.fromtimestamp(process_end_time)
    time_taken = time.strftime(
        "%H:%M:%S", 
        time.gmtime(
            process_end_time - process_start_time
    ))
    print(f'Start Date: {process_start_date}\nEnd Date: {process_end_date}\nTime Taken: {time_taken}')