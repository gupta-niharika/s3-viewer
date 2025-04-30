from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeView, QPushButton,
    QLineEdit
)
from .s3_client import S3FileModel


class FileBrowserPage(QWidget):
    def __init__(self, s3_client, bucket_name):
        super().__init__()

        self.s3_client = s3_client
        self.bucket_name = bucket_name

        # Main layout
        main_layout = QVBoxLayout(self)

        # --- Top row layout with buttons and search ---
        top_row = QHBoxLayout()

        self.refresh_button = QPushButton("🔄")
        self.add_button = QPushButton("➕")
        self.remove_button = QPushButton("➖")
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search files...")
        self.search_button = QPushButton("🔍")

        top_row.addWidget(self.refresh_button)
        top_row.addWidget(self.add_button)
        top_row.addWidget(self.remove_button)
        top_row.addStretch()
        top_row.addWidget(self.search_bar)
        top_row.addWidget(self.search_button)

        main_layout.addLayout(top_row)

        # --- Tree view for folder structure ---
        self.tree = QTreeView()
        self.model = S3FileModel(self.s3_client, self.bucket_name)
        self.tree.setModel(self.model)
        self.tree.setHeaderHidden(True)
        self.tree.expandAll()  # Optional: expands all items initially
        main_layout.addWidget(self.tree)

        # --- Back Button ---
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.on_back)
        main_layout.addWidget(back_button)

        # --- Hook up button events ---
        self.refresh_button.clicked.connect(self.refresh_files)
        # You can later hook up: self.add_button.clicked.connect(...)
        # You can later hook up: self.search_button.clicked.connect(...)

    def on_back(self):
        from .login import LoginPage
        self.hide()
        self.login_page = LoginPage()
        self.login_page.show()

    def refresh_files(self):
        self.model = S3FileModel(self.s3_client, self.bucket_name)
        self.tree.setModel(self.model)
        self.tree.expandAll() 
