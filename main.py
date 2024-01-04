from UnitTest import UnitTest as UT
from Extractor import Extractor as EX

if __name__ == '__main__':
    input_test = []
    expected_output = []

    # fill with folder path
    filePath = r"D:\DigiLab\Progdas2023\Modul8\CS2\CS2"
    checker = UT(filePath, regex=True)