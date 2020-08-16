# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import math

from centroidtracker import CentroidTracker
from trackableobject import TrackableObject

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
ap.add_argument("-c", "--color", default="green",
    help="color to track")
ap.add_argument("-r", "--radius", default=10,
    help="minimum radius to be tracked")
ap.add_argument("-n", "--numpoint", default=3,
    help="maximum number of objects to be plotted in a frame")
args = vars(ap.parse_args())

# Set the trackable object
ct = CentroidTracker(maxDisappeared=5, maxDistance=70)
trackableObjects = {}

# define the lower and upper boundaries of the several colors
# in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
red1Lower = (0, 20, 6)
red1Upper = (20, 255, 230)
red2Lower = (160, 20, 6)
red2Upper = (179, 255, 230)
blueLower = (95, 100, 80)
blueUpper = (125, 255, 170)

colormap = {
    'green': (greenLower, greenUpper),
    'red': (red1Lower, red1Upper, red2Lower, red2Upper),
    'blue': (blueLower, blueUpper)
}

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	vs = VideoStream(src=0).start()
# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])
# allow the camera or video file to warm up
time.sleep(2.0)

maxnumpoint = args["numpoint"]

# keep looping
while True:
    # grab the current frame
    frame = vs.read()
    # handle the frame from VideoCapture or VideoStream
    frame = frame[1] if args.get("video", False) else frame
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break
    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    if args["color"] is not 'red':
        mask = cv2.inRange(hsv, colormap[args["color"]][0], colormap[args["color"]][1])
    else:
        mask1 = cv2.inRange(hsv, colormap[args["color"]][0], colormap[args["color"]][1])
        mask2 = cv2.inRange(hsv, colormap[args["color"]][2], colormap[args["color"]][3])
        mask = mask1 | mask2
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = []
    rects = []
    # only proceed if at least one contour was found
    if len(cnts) > 0:
	    # find the largest contour in the mask, then use
	    # it to compute the minimum enclosing circle and
	    # centroid
        contour_area = np.array([cv2.contourArea(contour) for contour in cnts])
        contour_arg = contour_area.argsort()[-(maxnumpoint):][::-1]
        cs = []
        for arg in contour_arg:
            cs.append(cnts[arg])
        for c in cs:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center.append((int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])))
            # only proceed if the radius meets a minimum size
            if radius > args["radius"]:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center[-1], 5, (0, 0, 255), -1)
                rects.append((x - radius, y - radius, x + radius, y + radius))
        # use centroidtracker to associate detected objects with objects in previous frame
        objects = ct.update(rects)
        # use trackable object to plot object trail
        for (objectID, centroid) in objects.items():
            print(objectID)
            to = trackableObjects.get(objectID, None)

            if to is None:
                to = TrackableObject(objectID, centroid, args["buffer"])
                to.deque.appendleft(centroid)
            else:
                to.centroids.append(centroid)
                to.deque.appendleft(centroid)

            trackableObjects[objectID] = to
            for j in range(1, len(to.deque)):
                if to.deque[j-1] is None or to.deque[j] is None:
                    continue
                thickness = int(np.sqrt(args["buffer"] / float(j + 1)) * 2.5)
                cv2.line(frame, (to.deque[j - 1][0], to.deque[j-1][1]), (to.deque[j][0], to.deque[j][1]), (0, 0, 255), thickness)
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
	vs.stop()
# otherwise, release the camera
else:
	vs.release()
# close all windows
cv2.destroyAllWindows()