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

font = cv2.FONT_HERSHEY_SIMPLEX

# funcja przetwarzajaca zdjecia i znajdujaca charakterystyczne punkty na zdjeciach
def preprocess_image(image):

    # ladowanie zdjecia
    im = cv2.imread(image)
    imag = cv2.imread(image)

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

    return imag, extLeft, extRight, extTop, extBot


# funkcja obliczajaca charakterystyki pukntow charakterystycznych

def predict(left, right, top, bot):
    width = right[0] - left[0]
    heigth = bot[1] - top[1]
    x_shift = right[1] - left[1]
    y_shift = top[0] - left[0]
    return width, heigth, x_shift, y_shift

imag, l, r, t, b = preprocess_image(f"images/V3.jpg")

width, heigth, x_shift, y_shift = predict(l, r, t, b)


# na podstawie charekterystyk przewidywanie znaku

if width < 430 and width > 394 and heigth < 560 and heigth > 502 and x_shift < -120 and x_shift > -150 and y_shift < 366 and y_shift > 320:
    cv2.putText(imag, 'A', (100,100), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
elif width < 340 and width > 294 and heigth < 710 and heigth > 600 and x_shift < 20 and x_shift > -66 and y_shift < 200 and y_shift > 144:
    cv2.putText(imag, 'B', (100,100), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
elif width < 582 and width > 520 and heigth < 710 and heigth > 660 and x_shift < -110 and x_shift > -170 and y_shift < 300 and y_shift > 244:
    cv2.putText(imag, 'L', (100,100), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
elif width < 350 and width > 290 and heigth < 674 and heigth > 580 and x_shift < -70 and x_shift > -200 and y_shift < 130 and y_shift > 80:
    cv2.putText(imag, 'V', (100,100), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
elif width < 600 and width > 560 and heigth < 640 and heigth > 600 and x_shift < 240 and x_shift > 200 and y_shift < 30 and y_shift > 0:
    cv2.putText(imag, 'Y', (100,100), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
else:
    print("can't recognise")

cv2.imshow("PREDICT", imag)
cv2.waitKey(0)
