from UnitTest import UnitTest as UT
from Extractor import Extractor as EX

if __name__ == '__main__':
    input_test = []
    expected_output = []

    filePath = r"D:\DigiLab\Progdas2023\Modul7\CS1"
    # checker = UT(filePath, regex=True)
    extractor = EX(filePath, folderName=["CS1"])