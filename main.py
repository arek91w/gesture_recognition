# Imports

import cv2
import imutils
import numpy as np



# tabela znakow do rozpoznania

characters = ["A", "B", "L", "V", "Y"]

im = cv2.imread("images/Y1.jpg")
cv2.imshow("Image", im)
cv2.waitKey(0)


gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
cv2.imshow("Gray", gray)
cv2.waitKey(0)

lower = np.array(68)
upper = np.array(255)

frame_threshold = cv2.inRange(gray, lower, upper)

cv2.imshow("Threshold", frame_threshold)
cv2.waitKey(0)


# funcja przetwarzajaca zdjecia i znajdujaca charakterystyczne punkty na zdjeciach
def preprocess_image(image):

    # ladowanie zdjecia
    im = cv2.imread(image)

    # konwersja na zdjecie czarno-biale oraz dadanie rozmycia Gaussa
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # ustalenie granic thresholdu aby wykryc granice dloni
    lower = np.array(68)
    upper = np.array(255)

    frame_threshold = cv2.inRange(gray, lower, upper)

    #znalezienie kontur oraz wybranie najdluzszej (obrys dloni)
    cnts = cv2.findContours(frame_threshold.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)

    # punkty charakterystyczne (maxLeft, maxRight, extTop, extBot)
    extLeft = tuple(c[c[:, :, 0].argmin()][0])
    extRight = tuple(c[c[:, :, 0].argmax()][0])
    extTop = tuple(c[c[:, :, 1].argmin()][0])
    extBot = tuple(c[c[:, :, 1].argmax()][0])

    # dorysowanie punktow do zdjecia
    cv2.drawContours(im, [c], -1, (0, 255, 255), 2)
    cv2.circle(im, extLeft, 8, (0, 0, 255), -1)
    cv2.circle(im, extRight, 8, (0, 255, 0), -1)
    cv2.circle(im, extTop, 8, (255, 0, 0), -1)
    cv2.circle(im, extBot, 8, (255, 255, 0), -1)


    # show the output image
    cv2.imshow(image, im)
    cv2.waitKey(0)

for ch in characters:
    preprocess_image(f"images/{ch}1.jpg")


