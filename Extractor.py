import zipfile, os, mosspy
from time import sleep

class Extractor:
    def __init__(self, path):
        """
        The function initializes an object with a given path and assigns a user ID to a variable.
        
        :param path: The `path` parameter is a string that represents the file path where the code files
        are located. It is used to specify the directory or folder where the code files will be read
        from or written to
        """
        self.path = path
        self.userid_moss = 220418487

    def extract(self):
        """
        The function extracts all .zip files found in a given directory and its subdirectories.
        """
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith('.zip'):
                    zipPath = os.path.join(root, file)
                    try:
                        with zipfile.ZipFile(zipPath, 'r') as zip_ref:
                            zip_ref.extractall(root)
                            print('Extracted: ' + zipPath)
                    except zipfile.BadZipFile:
                        print('Bad zip file: ' + zipPath)
                        continue
                    except FileExistsError:
                        print('File exists: ' + zipPath)
                        continue
    
    def remove_zip(self):
        """
        The function removes all zip files from a given directory and its subdirectories.
        """
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith('.zip'):
                    os.remove(os.path.join(root, file))

    def remove_space(self):
        """
        The function removes spaces from file names in a given directory and its subdirectories.
        """
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if ' ' in files:
                    os.rename(os.path.join(root, file), os.path.join(root, file.replace(' ', '')))
    
    def uppercase_filename(self):
        """
        The function `uppercase_filename` recursively renames all files in a given directory and its
        subdirectories to uppercase.
        """
        for root, dirs, files in os.walk(self.path):
            for file in files:
                os.rename(os.path.join(root, file), os.path.join(root, file.upper()))

    def remove_picture(self):
        """
        The function removes all picture files (JPG, PNG, JPEG) from a given directory and its
        subdirectories.
        """
        self.uppercase_filename()
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith('.JPG') or file.endswith('.PNG') or file.endswith('.JPEG'):
                    os.remove(os.path.join(root, file))

    def remove_empty_folder(self):
        """
        The function removes empty folders from a given directory.
        """
        for root, dirs, files in os.walk(self.path):
            if len(dirs) == 0 and len(files) == 0:
                os.rmdir(root)

    def separate_file_by_name(self):
        """
        The function separates files in a given directory into two separate directories based on the
        name of the file.
        """
        if not os.path.exists('SESI1'):
            os.makedirs('SESI1')
        if not os.path.exists('SESI2'):
            os.makedirs('SESI2')

        for root, dirs, files in os.walk(self.path):
            for file in files:
                fileName = os.path.join(root, file).split('_')[1]
                if 'SESI1' in fileName.upper():
                    os.rename(fileName, 'SESI1/' + file)
                elif 'SESI2' in fileName.upper():
                    os.rename(fileName, 'SESI2/' + file)

    def check_plagiarism(self):
        moss = mosspy.Moss(self.userid_moss, "C")
        mossDir = ["SESI1", "SESI2"]
        for mossPath in mossDir:
            moss.addFilesByWildcard(os.path.join(self.path, mossPath, "*.c"))
            url = moss.send()
            print(f"Report Url {mossPath}: " + url)

    def run(self):
        self.extract()
        sleep(2)
        self.remove_zip()
        sleep(2)
        self.separate_file_by_name()
        sleep(2)
        self.remove_space()
        sleep(2)
        self.remove_picture()
        sleep(2)
        self.remove_empty_folder()
        sleep(2)
        self.check_plagiarism()