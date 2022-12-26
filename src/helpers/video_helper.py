import os, time, cv2, numpy as np, multiprocessing as mp
from classes.DatasetHandler import DatasetHandler

def video_single_frame_processing(args, img_channels):
    shape = img_channels[0].Img.shape + (3,)
    Img = np.zeros(shape, dtype=np.uint8)
    nImg = np.zeros(shape, dtype=np.uint8)
    for id in range(3):
        Img[..., id] = img_channels[id].Img
        # Adding Noise
        img_channels[id].add_noise()
        # Creating a variable for the noist image
        nImg[..., id] = img_channels[id].nImg
    
    frame = {
        'true_res': Img,
        'noisy_res': nImg
    }
    # Denoising
    for arg in args:
        outFrame = np.zeros(shape, dtype=np.uint8)
        for id in range(3):
            outFrame[..., id] = arg(img_channels[id].nImg)
        frame[f'{arg.__name__}'] = outFrame

    return frame

def video_multi_frame_processing(task_number, q, args:list, frame_data_list:list):
    out_frames = []
    for frame in frame_data_list:
        out_frames.append(video_single_frame_processing(args, frame))
    q.put((task_number,out_frames))

def video_writer_init(file_name, size, args, clear=False):
    if ~clear:
        outVideo_writer = {
            f'true_res' : cv2.VideoWriter(
                f'{file_name}_true.mp4', 
                cv2.VideoWriter_fourcc(*'H264'), 
                30,
                size
                ),
            f'noisy_res' : cv2.VideoWriter(
                f'{file_name}_noisy.mp4', 
                cv2.VideoWriter_fourcc(*'H264'), 
                30,
                size
                )
        }
        for arg in args:
            outVideo_writer[f'{file_name}_{arg.__name__}'] = cv2.VideoWriter(
                f'{file_name}_{arg.__name__}.mp4', 
                cv2.VideoWriter_fourcc(*'H264'), 
                30,
                size
            )
        return outVideo_writer
    else:
        for key in outVideo_writer.keys():
            outVideo_writer[key].release()

def video_processing(dataset:DatasetHandler, frame_segment_length=30, *denoising_functions):
    '''
    Takes the dataset object and uses the video
    processing to create and store the video
    '''
    inVideo = {}
    outVideo_writer = {}
    for flag, file_path, size, *img_channels in dataset.video_frame_handler():
        if flag:
            file_name = os.path.split(file_path)[-1]
            outVideo_writer[f'{file_name}'] = video_writer_init(file_name, size, denoising_functions)
            frame_number = 1
            inVideo[f'{file_name}'] = {}
            continue
        else:
            inVideo[f'{file_name}'][frame_number] = img_channels
            frame_number += 1

    for file_name in outVideo_writer.keys():
        frame_data_list = []
        procs = []
        q = mp.Manager().Queue()
        for frame_number in range(1, len(inVideo[file_name].keys())+1):
            frame_data_list.append(inVideo[file_name][frame_number])
            task_number = frame_number // frame_segment_length
            if frame_number % frame_segment_length == 0:
                procs.append(mp.Process(target=video_multi_frame_processing, args=(task_number, q, denoising_functions, frame_data_list)))
                frame_data_list = []
        procs.append(mp.Process(target=video_multi_frame_processing, args=(task_number+1, q, denoising_functions, frame_data_list)))
    
    task_length = len(procs)
    start_time = time.time()
    for proc in procs:
        proc.start()

    current_task = 1
    while current_task != task_length:
        task_number, out_frames = q.get()
        if task_number == current_task:
            for frame in out_frames:
                outVideo_writer[f'{file_name}']['true_res'].write(frame['true_res'])
                outVideo_writer[f'{file_name}']['noisy_res'].write(frame['noisy_res'])
                for arg in args:
                    outVideo_writer[f'{file_name}'][f'{file_name}_{arg.__name__}'].write(frame[f'{arg.__name__}'])
            current_task += 1
        else:
            q.put((task_number, out_frames))

    for proc in procs:
        proc.join()

    print(f"--- It took {time.time()-start_time} seconds to run.")