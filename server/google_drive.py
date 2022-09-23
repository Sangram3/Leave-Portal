import json
import requests

class GoogleDrive:
    def __init__(self,access_token):
        self.headers = {"Authorization": "Bearer {}".format(access_token)}
    def uploadFile(self,file_path, filename):
        para = {"name": filename, "parents": ["1utY7GpylYINB6Zb1jie0Qbzrtrn_l-NV"]} # name of the file after upoading
        files = {
            'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
            'file': open(file_path, "rb")
        }
        r = requests.post("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",headers=self.headers,files=files)
 
        file_link = "https://drive.google.com/file/d/"+r.json()['id']+"/view?usp=sharing"
        return file_link