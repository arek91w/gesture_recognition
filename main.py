from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt,QObject
import sys
import cv2
from process import preprocess_image, predict
from os import walk
import random


# odczytywanie katalogu 'images'
filenames = next(walk('./images'), (None, None, []))[2]
num_of_pics = len(filenames)

font = cv2.FONT_HERSHEY_SIMPLEX
path = 'images/A1.jpg'






class App(QWidget):
    def __init__(self):
        super().__init__()

        # ustawienia atrybutow interfejsu
        self.setWindowTitle("Gesture recognition")
        self.disply_width = 640
        self.display_height = 480
        self.x = 0
        self.image_label = QLabel(self)
        self.textLabel = QLabel('Polecat')
        self.reco_btn = QPushButton('PREDICT', self)
        self.back_btn = QPushButton('CHANGE IMAGE', self)
        self.reco_btn.setStyleSheet("QPushButton"
                             "{"
                             "background-color : lightblue;"
                             "font-size: 18pt;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : white;"
                             "}"
                             )
        self.back_btn.setStyleSheet("QPushButton"
                             "{"
                             "background-color : lightblue;"
                             "font-size: 18pt;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : white;"
                             "}"
                             )

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.back_btn)
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        vbox.addWidget(self.back_btn)
        vbox.addWidget(self.reco_btn)
        self.setLayout(vbox)
        self.cv_img = cv2.imread('images/'+filenames[0])
        self.qt_img = self.convert_cv_qt(self.cv_img)
        self.image_label.setPixmap(self.qt_img)
        
        # polaczenie przyciskow z metodami
        self.reco_btn.clicked.connect(lambda: self.reco_sign(filenames[self.x]))
        self.back_btn.clicked.connect(self.backward)

    # metoda przetwarzajaca zdjecie, aby wyswietlilo sie w interfejsie
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    # metoda rozpoznajaca dana literke

    def reco_sign(self, path_1):
        imag, l, r, t, b = preprocess_image('images/'+path_1)
        width, heigth, x_shift, y_shift = predict(l, r, t, b)
        t_ratio, z_ratio = width/heigth, x_shift/y_shift
        print(t_ratio, z_ratio)
        if t_ratio < 0.9 and t_ratio > 0.7 and z_ratio < -0.3 and z_ratio > -0.45:
            cv2.putText(imag, 'Predicted letter: A', (100,100), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
        elif t_ratio < 0.6 and t_ratio > 0.4 and z_ratio < 0.15 and z_ratio > -0.4:
            cv2.putText(imag, 'Predicted letter: B', (100,100), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
        elif t_ratio < 0.9 and t_ratio > 0.7 and z_ratio < -0.4 and z_ratio > -0.6:
            cv2.putText(imag, 'Predicted letter: L', (100,100), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
        elif t_ratio < 0.7 and t_ratio > 0.4 and z_ratio < 7 and z_ratio > -1.6:
            cv2.putText(imag, 'Predicted letter: V', (100,100), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
        elif t_ratio < 1 and t_ratio > 0.8 and z_ratio < 18 and z_ratio > 9:
            cv2.putText(imag, 'Predicted letter: Y', (100,100), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
        elif t_ratio < 1.1 and t_ratio > 0.82 and z_ratio < -0.35 and z_ratio > -0.5:
            cv2.putText(imag, 'Predicted letter: P', (100,100), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
        elif t_ratio < 1.3 and t_ratio > 0.76 and z_ratio < 1.55 and z_ratio > 0.5:
            cv2.putText(imag, 'Predicted letter: 0', (100,100), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
        elif t_ratio < 0.92 and t_ratio > 0.55 and z_ratio < 40 and z_ratio > 16:
            cv2.putText(imag, 'Predicted letter: I', (100,100), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
        else:
            print("can't recognise")
            cv2.putText(imag, 'CANT RECOGNIZE', (100,100), font, 2, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("PREDICT", imag)
        cv2.waitKey(0)
        print("klicker")


    # metoda zmieniajaca wyswietlane zdjecie

    def backward(self):
        self.x = random.randint(0,num_of_pics-1)
        print(filenames[self.x])
        self.cv_img = cv2.imread('images/'+filenames[self.x])
        self.qt_img = self.convert_cv_qt(self.cv_img)
        self.image_label.setPixmap(self.qt_img)


# glowny watek programu
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())