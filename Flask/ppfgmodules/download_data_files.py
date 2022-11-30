from io import BytesIO
from zipfile import ZipFile
import os

class DownloadFiles:
    
    def __init__(self):
        pass

    def getDownlodStream(self, filePaths):
        stream = BytesIO()
        with ZipFile(stream, 'w') as zf:
            for file in filePaths:
                zf.write(file, os.path.basename(file))
        return stream