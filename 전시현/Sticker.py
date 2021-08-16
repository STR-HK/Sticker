from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from PIL import Image
from PIL.ImageQt import ImageQt

from os import path


class Sticker(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout()

        self.img = QLabel()
        self.image = Image.open(
            path.abspath(path.join(path.dirname(__file__), "Sakura Miko.png"))
        )
        layout.addWidget(self.img)

        # sizegrip = QSizeGrip(self)
        # layout.addWidget(sizegrip, 0, Qt.AlignBottom | Qt.AlignRight)
        self.setLayout(layout)

        self.setGeometry(0, 0, 300 * 1, 300 * (self.image.height / self.image.width))
        self.show()

        self.img.resize(self.width(), self.height())
        pixmap = QPixmap.fromImage(
            ImageQt(self.image.resize((self.width(), self.height())))
        )

        self.img.setPixmap(pixmap)

        print(self.img.width(), self.img.height())
        print(self.width(), self.height())

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        # newAct = contextMenu.addAction("New")
        openAct = contextMenu.addAction("Open")
        quitAct = contextMenu.addAction("Quit")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAct:
            self.close()

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        try:
            if self.offset:
                x = event.globalX()
                y = event.globalY()
                x_w = self.offset.x()
                y_w = self.offset.y()
                self.move(x - x_w, y - y_w)
        except:
            print("error")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Sticker()

    # palatte = window.palette()
    # trs = QColor("transparent")
    # trs.setAlpha(100)
    # palatte.setColor(window.backgroundRole(), trs)
    # window.setPalette(palatte)

    window.show()
    sys.exit(app.exec())
