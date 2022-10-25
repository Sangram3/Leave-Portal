import json

class JsonReader:
    """
        This class is used to perform Json file parsing.
        Takes path of the file.
    """

    def __init__(self, file_name) -> None:
        self.file_name = file_name
        
    def read(self):
        """
            Returns the dictionary containing all the fields in the 
            Json file.
        """
        f = open(self.file_name)
        data = json.load(f)
        f.close()        
        return data

key_path = 'keys.json'
jsonReader = JsonReader(key_path)


