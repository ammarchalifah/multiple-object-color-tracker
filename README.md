![banner](https://github.com/ammarchalifah/multiple-object-color-tracker/blob/master/assets/banner.jpg)
# Multiple Object Color Tracker
Multiple object tracker based on color implemented with Python and OpenCV. This program may help in analysing body part movement (or any other objects' movement) using color
marker (e.g. gait analysis, 2D velocity analysis, etc.). This program is inspired by Adrian Rosebrock's tutorial: color tracking tutorial [here](https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/) and multiple object tracking tutorial [here](https://www.pyimagesearch.com/2018/07/23/simple-object-tracking-with-opencv/).
## Requirements
- imutils 0.5.3
- numpy
- opencv 3.4.2
## How to Use
<p align="center">
<img width=600 height=470 src="https://github.com/ammarchalifah/multiple-object-color-tracker/blob/master/assets/track.gif">
</p>
<br>

Clone this repository by typing this line of code in terminal
```
git clone https://github.com/ammarchalifah/multiple-object-color-tracker.git
```
Change working directory by typing
```
cd multiple-object-color-tracker
```
To track 2 green markers from your webcam, call the program by using
```
python color_tracking.py
```
For more customization, you can specify:
- video input file **[-v or --video]**
- max buffer size (the length of tracking length to be displayed on the screen, default is 64) **[-b or --buffer]**
- color to detect (red, green, or blue. the default color is green. for adding new color or changing the HSV values of each color, edit the source code in `color_tracking.py`) **[-c or --color]**
- minimum radius of masked object to be identified as object (default is 20 pixels) **[-r or --radius]**
- number of object(s) to be detected (default: 2) **[-n or --numpoint]**

For example,
```
python color_tracking.py -v INPUT_PATH -b 512 -c blue -r 30 -n 5
```
## References
- [Simple Object Tracking with OpenCV by Adrian Rosebrock](https://www.pyimagesearch.com/2018/07/23/simple-object-tracking-with-opencv/)
- [Ball Tracking with OpenCV by Adrian Rosebrock](https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/)
