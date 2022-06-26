from zipfile import ZipFile
import requests
import io

etymwn_url = "http://etym.org/etymwn-20130208.zip"

# Download Etymwn
r = requests.get(etymwn_url, stream=True)
zip_as_bytes_io = io.BytesIO(r.content)
zip_file = ZipFile(zip_as_bytes_io)
zip_file.extractall("import/")
