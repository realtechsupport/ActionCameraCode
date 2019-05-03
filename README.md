# ActionCameraCode
ART350 video experience toolkit - Department of ART - University of Buffalo, Spring 2019  

------------------------------------------------------------------------------------------------------------------------------
**Overview**

This course is an introduction to computational thinking in code integrated into a survey of great video art. 

Students are exposed to the opportunities of time based image capture along two vectors. First, with repeated field experiments with GoPro cameras. Second with exposure to film/video classics including Dziga Vertov's 'Man with a Move Camera' 1929, Luis Buñuel's 'Un chien andalou' 1929, Chris Marker's 'La Jetée' 1962, Michael Snow's 'La Région Centrale' 1971, Dara Birnbaum's 'Technology/Transformation: Wonder Woman' 1978, Douglas Gordon's 'Psycho' 1993, Pipilotti Rist's 'Ever is overall' 1997 and others. 

After several weeks of field recordings and screenings, the course moves to coding, on an introductory level in python(3). The course produced a large collection of functions that operate on individual images and video segments, ranging from basic color management to video overlay, optical character recognition and template matching. Technically, the functions offered below are mostly wrappers of ffmpeg and opencv funcionalities. But they allow coding novices to concentrate on desiging video experiences and wasting less time fiddling with code.

While many programming ideas are not covered in this course, those that do pertain to video management are addressed, and contextualized in code such that beginners can use the examples developed here to perform computationally based video experiments on their own.

More importantly, experimentation with these code artifacts allows students to explore the shifting locus of creative practice as traditional media intersect with computational methods.


**Acknowledgements**  
Supported in part by a Google Cloud Platform Education Grant  

**Dependencies**    
python3, ffmpeg, pillow, opencv, tesseract, datetime, psutil

**Files**    
av_helper.py, image_helper.py, utilities.py, combine_segments.py, extract_process_make.py

**Comments**  
platform: developed and tested on ubuntu 18.04 LTS, google cloud (1vCPU, 3.75GB memory, 10GB storage)  
gopro input: HD 1920x1080@30fps; H264 MP4


**Example usage**  
from av_helper import * 
datapath = 'where you keep your gopro data'  
videofile = 'yourgoprofile.mp4'  
start = 1; end = 4  #start and end time in seconds  
time_s = time.strftime("%H:%M:%S", time.gmtime(start))  
time_e = time.strftime("%H:%M:%S", time.gmtime(end))  
info = videofile.split('.')  
segmentname = info[0] + '_' + str(start) + '_' + str(end) + '.' + info[1]  

1) *extract a segment with the specified start and end times in seconds*   
extract_segment (datapath, videofile, time_s, time_e, segmentname)

2) *operate on all images (here blur via convolution with specified kernel) in that segment*   
kernel = (11,11)  
type = process_images_blur (datapath+'temp/', datapath, kernel)

3) *overlay two video segments in a given proportion*  
segment1 = 'mv1.mp4'  
segment2 = 'mv1_edgedetect.mp4'  
seg1_contrib = 0.3; seg2_contrib = 1-seg1_contrib  
type = process_images_videooverlay (datapath, 'temp/', 'temp2/', segment1, segment2, seg1_contrib, seg2_contrib)

4) *create a new .mp4 from the images created in any of the previous steps*  
create_video_from_images (datapath, 'temp/', framerate, reverse, output)

**Detailed examples**  
see *extract_process_make.py* for the complete pipeline of extraction, manipulation and video segment creation.  
see *combine_segments.py* to see how the individual segments are placed into a final video product.

**Results**  
see video folder

**Known issues**  
H265 encoded files are currently not supported (on the todo list)


