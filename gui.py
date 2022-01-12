#!/usr/bin/python



import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPixmap
import cv2

def convert_cv_qt(self, cv_img):
    """Convert from an opencv image to QPixmap"""
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
    p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
    return QPixmap.fromImage(p)

def main():

    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(550, 350)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()