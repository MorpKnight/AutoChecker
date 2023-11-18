from UnitTest import UnitTest as UT
from Extractor import Extractor as EX

if __name__ == '__main__':
    input_test = []
    expected_output = []

    filePath = r"your file path"
    checker = UT(filePath, regex=True)