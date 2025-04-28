from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTreeView, QPushButton
from .s3_client import S3FileModel
from PyQt6.QtCore import QDir


class FileBrowserPage(QWidget):
    def __init__(self, s3_client, bucket_name):
        super().__init__()

        layout = QVBoxLayout(self)

        self.model = S3FileModel(s3_client, bucket_name)

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        layout.addWidget(self.tree)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.on_back)
        layout.addWidget(back_button)

    def on_back(self):
        from .login import LoginPage

        self.hide()
        
        self.login_page = LoginPage()
        self.login_page.show()

