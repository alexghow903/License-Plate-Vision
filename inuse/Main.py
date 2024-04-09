import cv2
import time
from ultralytics import YOLO
import json
import geocoder
from datetime import datetime
from geopy.geocoders import Nominatim
import imutils
import pytesseract
import time
import tkinter as tk

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'



class car:

    def __init__(self, number, location, timestamp):
        self.number = number
        self.location = location
        self.timestamp = timestamp

carlist = []

class display:
    def __init__(self):
        self.window = tk.Tk()


def create(text, file):
    # add to database and add to session history
    g = geocoder.ip('me')
    date = str(datetime.now())

    dictionary = { text: {
        "Geolocation": {
            "Latitude": g.lat,
            "Longitude": g.lng
            },
        "Timestamp": date
        }
    }
    f = open("recognized.json", "w")
    file.update(dictionary)
    json.dump(file, f, indent=4)
    f.close()
    geolocator = Nominatim()
    location = geolocator.reverse(g.lat, g.lng)
    cab = car(text, location.address, date)
    carlist.append(cab)

def check(text):
    # checks to see if i've seen it today
    for x in carlist:
        # if i have then return
        if x.number == text:
            return
        
    # checks to see if i've seen it ever
    f = open("recognized.json", "r+")
    file = json.load(f)
    f.close()
    print(file.get(text))

    # if not then add to database
    if file.get(text) == None:
        create(text, file)
    # if i have seen it before but not today, then display and and to session history
    else:
        lat = file[text]["Geolocation"]["Latitude"]
        lng = file[text]["Geolocation"]["Longitude"]
        time = file[text]["Timestamp"]
        geolocator = Nominatim()
        location = geolocator.reverse(lat, lng)
        cab = car(text, location.address, time)
        cab.display()
        carlist.append(cab)




def contour(frame):
    
    original_image = imutils.resize(frame, width=500 )
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY) 
    gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)

    edged_image = cv2.Canny(gray_image, 30, 200)

    contours, new = cv2.findContours(edged_image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    img1 = original_image.copy()
    cv2.drawContours(img1, contours, -1, (0, 255, 0), 3)
    # cv2.imshow("img1", img1)
    # time.sleep(2)
    # cv2.destroyWindow("img1")

    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:30]

    # stores the license plate contour
    screenCnt = None
    img2 = original_image.copy()

    # draws top 30 contours
    cv2.drawContours(img2, contours, -1, (0, 255, 0), 3)


    for c in contours:
        # approximate the license plate contour
        contour_perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * contour_perimeter, True)

        # Look for contours with 4 corners
        if len(approx) == 4:

            # find the coordinates of the license plate contour
            x, y, w, h = cv2.boundingRect(c)
            new_img = original_image [ y: y + h, x: x + w]

            # converts the license plate characters to string
            text = pytesseract.image_to_string(new_img, lang='eng')

            return text
        
    return "null"
    # print("License plate is:", text)
    # cv2.waitKey(0)

CONFIDENCE_THRESHOLD = 0.65
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)
frame_rate = 4
prev = 0
while True:
	time_elapsed = time.time() - prev
	ret, frame = cap.read()
	if time_elapsed > 1./frame_rate:
		if not ret:
			break
		
		# run the YOLO model on the frame
		detections = model(frame)[0]

		results = []

		for data in detections.boxes.data.tolist():
			# extract the confidence (i.e., probability) associated with the prediction
			confidence = data[4]

			# filter out weak detections by ensuring the 
			# confidence is greater than the minimum confidence
			if float(confidence) < CONFIDENCE_THRESHOLD:
				continue

			# if the confidence is greater than the minimum confidence,
			# get the bounding box and the class id
			xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
			class_id = int(data[5])
			# add the bounding box (x, y, w, h), confidence and class id to the results list
			if class_id == 2:
				results.append([[xmin, ymin, xmax - xmin, ymax - ymin], confidence, class_id])
		for i in results:
			cropped_frame = frame[i[0][1]:(i[0][1]+i[0][3]), i[0][0]:(i[0][0]+i[0][2])]
			# cv2.imshow('madam', cropped_frame)
			# cv2.waitKey(0)
			text = contour(cropped_frame)
			if text != "null":
				check(text)
	
	prev = time.time()

