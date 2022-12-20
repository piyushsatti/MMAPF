# Min-Max Average Pooling Filter for Impulse Noise Removal
[Piyush Satti](https://scholar.google.com/citations?user=eR10c10AAAAJ&hl=en&oi=ao), [Nikhil Sharma](https://scholar.google.com/citations?user=wVlxsrsAAAAJ&hl=en), [Bharat Garg](https://scholar.google.com/citations?user=M_NAbSkAAAAJ&hl=en)
---
*The source paper[^1] to this implementation can be found [here.](https://ieeexplore.ieee.org/abstract/document/9169792)*

[^1]: DOI:10.1109/LSP.2020.3016868



### Task List
- [ ] Flow of the README
  - [ ] Problem statement
  - [ ] How widespread is the problem + Affected domains
  - [ ] Usual solutions
  - [ ] Proposed Solution
    - [ ] Along with diagram of the concept and source idea
  - [ ] Demonstration
    - [ ] Improvement images (colored and gray), and video
  - [ ] Metrics that are reproducable by forking
- [ ] Code - cleanup
  - [x] Code for running testing
  - [x] MMAPF Implementation
  - [x] Code for running colored images
  - [x] Code for running videos
  - [z] Error for clred images
  - [x] Speeding up algo for video processing
    - [x] Sub-divide video processing generator to handle batches of frames
    - [x] Parrallize the batch process into mp.Process objects
  - [ ] Save colored images and bnw images in respective folders
- [ ] Posting to Social Media
  - [ ] LinkedIn post with the research paper, GitHub link and an example
  - [ ] Twitter Post tweeting the implementation and the paper link
  - [ ] Making a YouTube video for the implementation