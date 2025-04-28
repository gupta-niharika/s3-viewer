from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QLineEdit,
    QVBoxLayout, QGridLayout, QSpacerItem, QSizePolicy, QPushButton
)
from PyQt6.QtCore import Qt, QSettings
from .s3_client import S3Client 
from .file_browser import FileBrowserPage

S3_CREDENTIALS = [
    "Access Key ID",
    "Secret Access Key",
    "Bucket Name",
    "Region",
    "Service Name"
]

class LoginPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("S3 Client Login")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Form layout
        form_layout = QGridLayout()
        form_layout.setVerticalSpacing(20)
        form_layout.setHorizontalSpacing(10)

        self.textboxes = {}

        for i, label_text in enumerate(S3_CREDENTIALS):
            label = QLabel(label_text)
            textbox = QLineEdit()
            textbox.setObjectName("inputField")
            self.textboxes[label_text] = textbox 

            form_layout.addWidget(label, i, 0, alignment=Qt.AlignmentFlag.AlignLeft)
            form_layout.addWidget(textbox, i, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        form_widget = QWidget()
        form_widget.setLayout(form_layout)

        main_layout.addWidget(form_widget, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Submit button
        submit_button = QPushButton("Submit")
        submit_button.setObjectName("submitButton")
        submit_button.setFixedWidth(200)
        submit_button.clicked.connect(self.on_submit)
        main_layout.addWidget(submit_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        self.load_credentials()

    def on_submit(self):
        keys = {field: self.textboxes[field].text() for field in 
                ["Access Key ID", "Secret Access Key", "Bucket Name", "Region", "Service Name"]}
        access_key, secret_key, bucket_name, region, service_name = keys.values()

        self.save_credentials()

        s3_client = S3Client.login_to_s3(access_key, secret_key, region, service_name)

        if s3_client:
            self.file_browser_page = FileBrowserPage(s3_client, bucket_name)
            self.setCentralWidget(self.file_browser_page)
        else:
            print("Login failed. Please check your credentials.")

    def save_credentials(self):
        settings = QSettings("MyCompany", "S3ClientApp")
        for field in S3_CREDENTIALS:
            settings.setValue(field, self.textboxes[field].text())

    def load_credentials(self):
        settings = QSettings("MyCompany", "S3ClientApp")
        for field in S3_CREDENTIALS:
            saved_value = settings.value(field, "")
            self.textboxes[field].setText(saved_value)
