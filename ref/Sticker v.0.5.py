from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from PIL import Image
from PIL.ImageQt import ImageQt
import os


class Sticker(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout()

        self.img = QLabel()

        layout.addWidget(self.img)

        self.imgsize = 400

        self.setLayout(layout)

        self.show()

        self.setPixmap(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "67669539.png"))
        )

    def setPixmap(self, path=None, pixmap=None):
        if pixmap:
            self.setGeometry(
                self.x(),
                self.y(),
                self.imgsize * 1,
                int(self.imgsize * (pixmap.height() / pixmap.width())),
            )

            self.img.setPixmap(pixmap)
            return

        try:
            self.movie.stop()
        except:
            print("움짤기록없음")

        self.image = Image.open(path)

        self.setGeometry(
            self.x(),
            self.y(),
            self.imgsize * 1,
            int(self.imgsize * (self.image.height / self.image.width)),
        )

        pixmap = QPixmap.fromImage(
            ImageQt(
                self.image.resize(
                    (
                        self.imgsize * 1,
                        int(self.imgsize * (self.image.height / self.image.width)),
                    )
                )
            )
        )
        self.img.setPixmap(pixmap)

    def setMovie(self, path):
        self.movie = QMovie(path)
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()

    def repaint(self):
        self.setPixmap(pixmap=self.movie.currentPixmap())

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        # newAct = contextMenu.addAction("New")
        openAct = contextMenu.addAction("Open")
        quitAct = contextMenu.addAction("Quit")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))

        if action == openAct:
            dialog = QFileDialog()
            dialog.setFileMode(QFileDialog.AnyFile)

            filename = dialog.getOpenFileName(
                caption="Open Image file",
                filter="Image files (*.png *.gif)",
                directory=".",
            )

            if filename:
                if filename[0] == "":
                    return

                print(filename[0])

                if filename[0].split(".")[-1] == "gif":
                    print("움짤")
                    self.setMovie(filename[0])

                else:
                    self.setPixmap(filename[0])

        if action == quitAct:
            self.close()

    def mouseDoubleClickEvent(self, event):
        print(event.pos())

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
    window.show()
    sys.exit(app.exec())
