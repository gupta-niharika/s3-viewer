import boto3
from PyQt6.QtCore import Qt, QAbstractItemModel, QModelIndex, QVariant
from ui.treeview import TreeItem


class S3Client:
    def login_to_s3(access_key, secret_key, region, service_name):
        try:
            s3_client = boto3.client(
                service_name=service_name,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region,
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
        self.root_item = TreeItem("root")

        self._build_tree()

    def _list_files_in_bucket(self):
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            return [obj['Key'] for obj in response.get('Contents', [])]
        except Exception as e:
            print(f"Error retrieving S3 files: {e}")
            return []

    def _build_tree(self):
        keys = self._list_files_in_bucket()

        for key in keys:
            parts = key.split('/')
            current = self.root_item

            for part in parts:
                match = next((c for c in current.children if c.name == part), None)
                if not match:
                    match = TreeItem(part, current)
                    current.add_child(match)
                current = match

    def rowCount(self, parent):
        parent_item = self._item_from_index(parent)
        return parent_item.child_count()

    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        if not index.isValid():
            return QVariant()

        item = index.internalPointer()
        if role == Qt.ItemDataRole.DisplayRole:
            return item.name
        return QVariant()

    def index(self, row, column, parent):
        parent_item = self._item_from_index(parent)
        child_item = parent_item.child(row)
        return self.createIndex(row, column, child_item)

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        child_item = index.internalPointer()
        parent_item = child_item.parent

        if parent_item == self.root_item or parent_item is None:
            return QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def _item_from_index(self, index):
        if index.isValid():
            return index.internalPointer()
        return self.root_item
