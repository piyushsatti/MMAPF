import os, time, datetime, cv2
import numpy as np, multiprocessing as mp
from gambit.helpers.noise_helper import add_noise_to_color_image, add_noise_to_grayscale_image
from gambit.video.VideoHandler import VideoHandler

def write_output_video(
    abs_path, 
    output_frame_rate, 
    size
):
    return cv2.VideoWriter(
        abs_path, 
        cv2.VideoWriter_fourcc(*'mp4v'), 
        output_frame_rate,
        size
    )

def video_dataset_writer_initialization(
    file_path,
    video_fps,
    video_size,
    noise_factor,
    denoising_functions,
    output_data_abs_path
):
    # Vars defining the naming convention
    video_name, video_extension = (os.path.split(file_path)[-1]).split('.')
    video_color = 'color'
    output_video_name_true = f'{video_name}_{video_size[0]}_{video_size[1]}_{video_color}_true_0.' + video_extension
    output_video_name_noisy = f'{video_name}_{video_size[0]}_{video_size[1]}_{video_color}_noisy_1.' + video_extension
    output_writers = {
        'true': write_output_video(
            os.path.join(
                output_data_abs_path, 
                output_video_name_true
            ),
            video_fps, 
            video_size
        ),
        'noisy': write_output_video(
            os.path.join(
                output_data_abs_path, 
                output_video_name_noisy
            ), 
            video_fps, 
            video_size
        )
    }
    for func in denoising_functions:
        output_video_name_filter = f'{video_name}_{video_size[0]}_{video_size[1]}_{video_color}_noisy_{noise_factor}_{func.__name__}.' + video_extension
        output_writers[func.__name__] = write_output_video(
            os.path.join(
                output_data_abs_path, 
                output_video_name_filter
            ), 
            video_fps, 
            video_size
        )
    return output_writers

def process_color_frame(
    selected_input_media_color,
    frame, 
    noise_factor, 
    denoising_functions, 
    video_output_dataset_writers
):
    # Generating the noisy image
    n_img = add_noise_to_color_image(
        img=frame,
        noise_type='s&p',
        noise_factor=noise_factor
    )
    # Writing the true and noisy image
    video_output_dataset_writers['true'].write(frame)
    video_output_dataset_writers['noisy'].write(n_img)
    # denoising and writing the filtered images
    for denoising_function in denoising_functions:
        filter_output_frame = np.zeros(frame.shape, dtype=np.uint8)
        for layer in range(3):
            filter_output_frame[..., layer] = denoising_function(n_img[..., layer])
        video_output_dataset_writers[denoising_function.__name__].write(filter_output_frame)
        

def process_grayscale_frame(
    selected_input_media_color,
    frame, 
    noise_factor, 
    denoising_functions, 
    video_output_dataset_writers
):
    # Generating the noisy image
    n_img = add_noise_to_grayscale_image(
        img=frame,
        noise_type='s&p',
        noise_factor=noise_factor
    )
    # Writing the true and noisy image
    video_output_dataset_writers['true'].write(frame)
    video_output_dataset_writers['noisy'].write(n_img)
    # denoising and writing the filtered images
    for denoising_function in denoising_functions:
        video_output_dataset_writers[denoising_function.__name__].write(denoising_function(n_img))

def video_dataset_process_handler(
    selected_input_media_color,
    input_data_abs_path,
    output_data_abs_path,
    max_number_of_processes,
    noise_factor,
    *denoising_functions
):
    '''
    Takes the dataset object and uses the video
    processing to create and store the video
    '''
    input_video_dataset = VideoHandler(input_data_abs_path)
    for (
            file_path,
            video_fps,
            video_size,
            video_capture_object_pointer
        ) in input_video_dataset.video_handlers():
        procs = []
        process_start_time = time.time()
        # Initiating the Writer Objects for a video
        video_output_dataset_writers = video_dataset_writer_initialization(
            file_path,
            video_fps,
            video_size,
            noise_factor,
            denoising_functions,
            output_data_abs_path
        )
        # Handling the Frames
        for frame in input_video_dataset.frame_handler(video_capture_object_pointer):
            if selected_input_media_color == 'color':
                target = process_color_frame
            elif selected_input_media_color == 'grayscale':
                target = process_grayscale_frame
            else:
                raise
            target(
                selected_input_media_color,
                frame, 
                noise_factor, 
                denoising_functions, 
                video_output_dataset_writers
            )
        #     proc = mp.Process(
        #         target = target, 
        #         args=(
        #             selected_input_media_color,
        #             frame, 
        #             noise_factor, 
        #             denoising_functions, 
        #             video_output_dataset_writers
        #         )
        #     )
        #     procs.append(proc)
        #     proc.start()
        #     while [proc.is_alive() for proc in procs].count(True) >= max_number_of_processes:
        #         time.sleep(1)
        #         continue
        
        # [proc.join() for proc in procs]
        process_end_time = time.time()
        process_start_date = datetime.datetime.fromtimestamp(process_start_time)
        process_end_date = datetime.datetime.fromtimestamp(process_end_time)
        time_taken = time.strftime(
            "%H:%M:%S", 
            time.gmtime(
                process_end_time - process_start_time
        ))
        print(f'<{os.path.split(file_path)[-1]}>\nStart Date: {process_start_date}\nEnd Date: {process_end_date}\nTime Taken: {time_taken}')