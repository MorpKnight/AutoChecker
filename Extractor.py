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

    def extract(self):
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith('.zip'):
                    zipPath = os.path.join(root, file)
                    try:
                        with zipfile.ZipFile(zipPath, 'r') as zip_ref:
                            zip_ref.extractall(root)
                    except zipfile.BadZipFile:
                        continue
                    except FileExistsError:
                        continue
    
    def remove_zip(self):
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith('.zip'):
                    try:
                        os.remove(os.path.join(root, file))
                    except:
                        print('Failed to remove: ' + os.path.join(root, file))

    def uppercase_filename(self):
        for root, dirs, files in os.walk(self.path):
            for file in files:
                os.rename(os.path.join(root, file), os.path.join(root, file.upper()))
                os.rename(os.path.join(root, file.upper()), os.path.join(root, file.upper().replace('.C', '.c')))

    def remove_picture(self):
        self.uppercase_filename()
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith('.JPG') or file.endswith('.PNG') or file.endswith('.JPEG'):
                    os.remove(os.path.join(root, file))

    def remove_empty_folder(self):
        for root, dirs, files in os.walk(self.path):
            if len(dirs) == 0 and len(files) == 0:
                os.rmdir(root)

    def separate_file_by_name(self):
        try:
            for folder in self.folderName:
                if not os.path.exists(os.path.join(self.path, folder)):
                    os.makedirs(os.path.join(self.path, folder))

            sleep(1)
            for root, dirs, files in os.walk(self.path):
                for file in files:
                    for folder in self.folderName:
                        if folder in file:
                            os.rename(os.path.join(root, file), os.path.join(self.path, folder, file))
                            print('Moved: ' + os.path.join(root, file) + ' to ' + os.path.join(self.path, folder, file))
        except:
            print('Failed to separate')

    def check_plagiarism(self):
        moss = mosspy.Moss(self.userid_moss, "C")
        mossDir = ["CS1", "CS2"]
        for mossPath in mossDir:
            moss.addFilesByWildcard(os.path.join(self.path, mossPath, "*.c"))
            url = moss.send()
            print(f"Report Url {mossPath}: " + url)

    def run(self):
        pass