# Min-Max Average Pooling Filter for Impulse Noise Removal
[Piyush Satti](https://scholar.google.com/citations?user=eR10c10AAAAJ&hl=en&oi=ao), [Nikhil Sharma](https://scholar.google.com/citations?user=wVlxsrsAAAAJ&hl=en), [Bharat Garg](https://scholar.google.com/citations?user=M_NAbSkAAAAJ&hl=en)
---
*The source paper[^1] to this implementation can be found [here.](https://ieeexplore.ieee.org/abstract/document/9169792)and the output can be accessed using [this](https://drive.google.com/drive/folders/1fY4z9iJNKcULx3sQ-NiPTcknWT21KHPh?usp=sharing) link.* If one wishes to fork and run the demo for oneself, one may directly jump to [here.](#How-to-Run-the-Demo?) A [task list](#task-list) details the steps taken to arrive to the current state of this repo.

[^1]: DOI:10.1109/LSP.2020.3016868

### Problem Statement: Why this problem matters?
### Market Solutions: What are the available solutions?
### Proposed Work: What is my solution and how is it different?
### Results and Comparisons: On what basis is the comparison made?
#### Black and White Images
#### Colored Images
| Noise % | True Image | Noisy Image | SMF Filter | MMAPF Image |
| --- | --- | --- | --- | --- |
| ![Noisy 20%](/Sample-Images/house_50/MMAPF.tiff) |  |  |  | |
#### Colored Video
# How to Run the Demo?
The code is developed and tested in [python 3.10](https://www.python.org/downloads/release/python-3100/), and the various modules imported have been version locked in the [requirements.txt](requirements.txt) file. To run the demo, it is not required but recommended to use virtual enviornments and steps to do the same has been touched upon below. **It is also recommended to** ***not*** **run the video processing** unless you are willing to commit a couple of hours to the processing (someone please optimize that [kek](https://en.wiktionary.org/wiki/kek#:~:text=Rhymes%3A%20%2D%C9%9Bk-,Interjection,to%20indicate%20laughter%20or%20humour.)).

*This demo assumes that the reader is able to install python, and has basic familiarity with the terminal. To check if the correct python version is installed run `python3 --version`* 

## Step 1: Setting and Switching to a .venv
This is the local instance of the enviornment in which python is run, and is independent of the modules available to the global instance. It is the recommended option to avoid installing bloat. In the terminal, where you have forked this repo to, please type:
<pre><code>
python3 -m venv .venv
</code></pre>
It should create a hidden folder by the name of `.venv`. The next step is to connect to the virtual environment whose steps differ for different OS. For windows, and unix based system this should be sufficient.

For Windows: `.\.venv\Scripts\activate`
For Unix(MacOS): `source ./.venv/Scripts/activate` 

Double check that the ***venv*** (virtual environment) is active. One way to check this is to type: `pip -V`. The path provided should have the `.venv` inside it. If it does, all good! If it doesn't, you might need a rechecking of the above steps.

## Step 2: Installing the required modules
The modules required are standard python modules. These go in the `.venv` folder, inside `.venv/lib/site-packages`. Once your virtual environment is situated:
<pre><code>
pip install -r requirements.txt
</code></pre>

While that installs, let me inform you of the amazing

## Step 3: Running!
I would recommend, only running the image processing helpers, and avoiding the video processing unless you REALLY want to. The video processing is slow, and prone to... hiccups on lower end computers... The forked code comes with the video processing function commented out to avoid any hassels, so all should be good!

Another point to note is that, to change the noise density you can navigate to [src/classes/ImageHandler.py](src/classes/ImageHandler.py) and change the `noise_factor` default value in the `add_noise` function to whatever desired. It should be noted that the images are overwritten, so save the previous images in a folder if you like! Yet another point may be that the number of processes that are active at a time is given as the first argument in the various functions. Change that as appropriate as well.

To start the program you need to:
<pre><code>
python main.py
</code></pre>

That's, about it. A folder by the name of `Test Data Out` should be created in the main project folder (give no error occur and write permissions are enabled), inside of which should be the true, noisy, and denoised images!

## Step 4: Once you are done.
Delete the folder. Everything was saved and operated upon locally so there is no bloatware that persists. Also, would love to hear feedback and merge changes if someone spends the time to make this better (:3)[https://opensource.org/].

# Task List

## General Tasks
- [ ] Flow of the README
  - [ ] Problem statement
  - [ ] How widespread is the problem + Affected domains
  - [ ] Usual solutions
  - [ ] Proposed Solution
    - [ ] Along with diagram of the concept and source idea
  - [ ] Dataset used and backlinks to the source files for the datasets
  - [x] Demonstration
    - [x] Improvement images (colored and gray), and video
  - [x] Metrics that are reproducable by forking
- [x] Code - cleanup
  - [x] Code for running testing
  - [x] MMAPF Implementation
  - [x] Code for running colored images
  - [x] Code for running videos
  - [x] Error for colored images
  - [x] Speeding up algo for video processing
    - [x] Sub-divide video processing generator to handle batches of frames
    - [x] Parrallize the batch process into mp.Process objects
  - [x] Save colored images and bnw images in respective folders
- [ ] Posting to Social Media
  - [ ] LinkedIn post with the research paper, GitHub link and an example
  - [ ] Twitter Post tweeting the implementation and the paper link
  - [ ] Making a YouTube video for the implementation

## Bugs and Issues
- [x] Video Processor Not Working
  - [x] Video Processor needs OS specific file format and encoder additions
  - [x] Video Processor needs file process updates like a bar that fills according to how much progress made
- [x] Format the code with a goal specific architecture
  - [x] Use folders for bnw, clr, and video processing and its classes
- [x] Output Formatting
  - [x] Output Files need better formatting and clarity
    - [x] Output files should add to the `data` folder
      - [x] Better I/O organisation
        - [x] Option for selecting a `input` folder should be provided with auto-sorting of the input data into types
        - [x] Option for a destination folder should be provided and should be separated from `sample_data`
      - [x] test_input should contain sample testing data (should be limited to 1-2 image of each kind)
      - [x] test_output should contain a subset of outputs ideally processed from test_input
    - [x] <image_name>_<size>_<bnw | clr>_<true | noisy>_<0 for true image | 1 for noisy image | noise_density between 0 and 1 for filtered image>_<filter_used>

## Ideas
- [x] Videos are intensive processes. The Video section should be converted to handle Gifs instead. Provides better GitHub README.md integration as well.