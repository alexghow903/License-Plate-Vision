import cv2
import imutils
import pytesseract

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

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