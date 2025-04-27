from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTreeView, QPushButton
from .s3_client import S3FileModel
from PyQt6.QtCore import QDir


class FileBrowserPage(QWidget):
    def __init__(self, s3_client, bucket_name):
        super().__init__()

        layout = QVBoxLayout(self)

        # Initialize the S3FileModel with the s3_client and bucket_name
        self.model = S3FileModel(s3_client, bucket_name)

        # Set up TreeView to show file system
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        layout.addWidget(self.tree)

        # Add a back button to return to the login page (optional)
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.on_back)
        layout.addWidget(back_button)

    def on_back(self):
        self.close()  # Close current page to go back (or can trigger stack navigation here)
