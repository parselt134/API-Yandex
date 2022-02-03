import sys
import requests
from io import BytesIO
from PIL import Image
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPixmap


class YandexAPI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("design.ui", self)
        self.search.clicked.connect(self.run)

    def run(self):
        coordinates = self.coordinates.text()
        scale = str(self.scale.value())
        scale = f"{scale},{scale}"
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={coordinates}&spn={scale}&l=map"
        response = requests.get(map_request)
        if not map_request:
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        im = Image.open(BytesIO(response.content))
        im.save("temp.png")
        self.pixmap = QPixmap("temp.png")
        self.map.setPixmap(self.pixmap)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = YandexAPI()
    widget.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
