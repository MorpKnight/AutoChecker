from UnitTest import UnitTest as UT
from Extractor import Extractor as EX

if __name__ == '__main__':
    input_test = ["8", "5", "2", "32", "0", "1", "16", "256", "9"]
    expected_output = ["(?i)ada.*tidak.*ada.*ada", "(?i)ada.*ada.*tidak.*tidak", "(?i)ada.*ada.*ada.*ada", "(?i)tidak.*tidak.*ada.*ada", "(?i)ada.*ada.*ada.*ada", "(?i)ada.*ada.*ada.*ada", "(?i)tidak.*tidak.*tidak.*ada", "(?i)tidak.*tidak.*ada.*ada", 
                       "(?i)tidak.*tidak.*tidak.*tidak"]

    filePath = r"D:\DigiLab\Progdas2023\Modul6\CS2\CS2"

    checker = UT(filePath, input_test=input_test, output_test=expected_output, regex=True)
    checker.run()
    # checkee2 = UT("code\\CS1", input_test=input_test, output_test=expected_output)
    # checkee2.run()

    # extractor = EX("code")
    # extractor.check_plagiarism()