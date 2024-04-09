import tojson
import notused.standardize as standardize
import Recognition
import tensorflow
import keras
import threading
import time
import cv2

running = True
video = cv2.VideoCapture(0)
frame_rate = 4
prev = 0

# run in a loop
while running:
# take a picture or video of a car butt, (taking video at 4 frames a second)
    time_elapsed = time.time() - prev
    res, image = video.read()

    if time_elapsed > 1./frame_rate:
        prev = time.time()

# focus on the license plate, 

# parse each letter,

# use ai to determine what each letter and number really is, 

# compare to history text file and see if the plate is already in there, or

# store the plaintext license plate in history text file.

# repeat.
    time.sleep(5)

video.release()
cv2.destroyAllWindows()