from UnitTest import UnitTest as UT
from Extractor import Extractor as EX

if __name__ == '__main__':
    input_test = ["1 5", "2 5", "3 5", "1 6", "2 6", "3 6", "1 7", "2 7", "3 7"]
    expected_output = ["29", "8", "8", "866", "32", "16", "750797", "256", "32"]

    checker = UT("code\\CS1", input_test=input_test, output_test=expected_output, regex=True)
    checker.run()

    # checkee2 = UT("code\\CS1", input_test=input_test, output_test=expected_output)
    # checkee2.run()

    # extractor = EX("code", folderName=["CS1"])
    # extractor.run()