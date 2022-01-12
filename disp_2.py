from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt,QObject
import sys
import cv2
from main import preprocess_image, predict
from os import walk


filenames = next(walk('C:/Users\Arkadiusz Woloszyn/Desktop/gests_repo/gesture_recognition/gesture_recognition/images'), (None, None, []))[2]

print(filenames)

font = cv2.FONT_HERSHEY_SIMPLEX
path = 'images/A1.jpg'

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gesture recognition")
        self.disply_width = 640
        self.display_height = 480
        # create the label that holds the image
        self.image_label = QLabel(self)
        #self.image_label.resize(self.disply_width, self.display_height)
        # create a text label
        self.textLabel = QLabel('Polecat')
        self.reco_btn = QPushButton('RECO', self)
        self.back_btn = QPushButton('PREVIOUS', self)
        self.next_btn = QPushButton('NEXT', self)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.back_btn)
        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        vbox.addWidget(self.back_btn)
        vbox.addWidget(self.next_btn)
        vbox.addWidget(self.reco_btn)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)
        # don't need the grey image now
        #grey = QPixmap(self.disply_width, self.display_height)
        #grey.fill(QColor('darkGray'))
        #self.image_label.setPixmap(grey)

        # load the test image - we really should have checked that this worked!
        self.cv_img = cv2.imread(path)
        # convert the image to Qt format
        self.qt_img = self.convert_cv_qt(self.cv_img)
        # display it
        self.image_label.setPixmap(self.qt_img)
        self.reco_btn.clicked.connect(self.reco_sign)


    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def reco_sign(self):
        imag, l, r, t, b = preprocess_image(path)
        width, heigth, x_shift, y_shift = predict(l, r, t, b)
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
        print("klicker")
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())