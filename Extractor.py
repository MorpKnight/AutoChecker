import zipfile, os, mosspy
from time import sleep

class FileStudent:
    def __init__(self):
        self.filename:str = None
        self.extracted:bool = False
        self.remove_zip:bool = False
        self.remove_picture:bool = False
        self.remove_space:bool = False
        self.remove_empty_folder:bool = False
        self.separate_file_by_name:bool = False
class Extractor:
    def __init__(self, path, **kwargs):
        self.path = path
        self.folderName:list = kwargs.get('folderName', [])
        self.userid_moss = 220418487
        self.run()

    def extract_zip(self):
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(".zip"):
                    file_path = os.path.join(root, file)
                    try:
                        with zipfile.ZipFile(file_path, 'r') as zip_ref:
                            zip_ref.extractall(root)
                        os.remove(file_path)
                        print(f"Extracted {file_path}")
                    except:
                        print(f"Error extracting {file_path}")
                        pass

    def remove(self):
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if ' ' in file:
                    os.rename(os.path.join(root, file), os.path.join(root, file.replace(' ', '')))
                if '._' in file:
                    os.rename(os.path.join(root, file), os.path.join(root, file.replace('._', '')))
                if file.upper().endswith(".JPG") or file.upper().endswith(".PNG") or file.upper().endswith(".JPEG"):
                    file_path = os.path.join(root, file)
                    os.remove(file_path)

            if len(dirs) == 0 and len(files) == 0:
                os.rmdir(root)

    def separate(self):
        try:
            for folder in self.folderName:
                if not os.path.exists(os.path.join(self.path, folder)):
                    os.makedirs(os.path.join(self.path, folder))
                for root, dirs, files in os.walk(self.path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if folder.upper() in file_path.upper():
                            os.rename(file_path, os.path.join(self.path, folder, file))
        except:
            pass
    
    def run(self):
        self.extract_zip()
        self.remove()
        self.separate()