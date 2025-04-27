import sys
from PyQt6.QtWidgets import QApplication
from ui.login import LoginPage


def main():
    app = QApplication(sys.argv)
    window = LoginPage()

    with open("ui/style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window.showMaximized()
    window.setWindowTitle("S3 Client")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
