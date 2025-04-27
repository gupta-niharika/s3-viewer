import boto3
from PyQt6.QtCore import Qt, QAbstractItemModel, QModelIndex, QVariant


class S3Client:
    def login_to_s3(access_key, secret_key, region, endpoint_url):
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region,
                endpoint_url=endpoint_url
            )
            return s3_client 
        except Exception as e:
            print(f"Login failed: {e}")
            return None


class S3FileModel(QAbstractItemModel):
    def __init__(self, s3_client, bucket_name, parent=None):
        super().__init__(parent)
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.objects = self._list_files_in_bucket()

    def _list_files_in_bucket(self):
        """
        List files in the S3 bucket and return a list of file names.
        """
        files = []
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            if 'Contents' in response:
                files = response['Contents']
        except Exception as e:
            print(f"Error retrieving S3 files: {e}")
        return files

    def rowCount(self, parent: QModelIndex = QModelIndex()):
        """
        Return the number of rows (files) in the current directory (bucket).
        """
        if parent.isValid():
            return 0
        return len(self.objects)

    def columnCount(self, parent: QModelIndex = QModelIndex()):
        """
        Return the number of columns (1 column for file names).
        """
        return 1

    def data(self, index: QModelIndex, role: int):
        """
        Return the file name for a given row and column.
        """
        if not index.isValid():
            return QVariant()

        if role == Qt.ItemDataRole.DisplayRole:
            return self.objects[index.row()]['Key']
        return QVariant()

    def index(self, row: int, column: int, parent: QModelIndex = QModelIndex()):
        """
        Return the index for a given row and column.
        """
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        return self.createIndex(row, column)

    def parent(self, index: QModelIndex) -> QModelIndex:
        """
        This is a flat structure, so no parent index exists.
        """
        return QModelIndex()
