from UnitTest import UnitTest as UT
from Extractor import Extractor as EX

if __name__ == '__main__':
    input_test = ["3 1 0 0 0 1 0 0 0 1", "4 1 2 3 4 2 5 6 7 3 6 8 9 4 7 9 10", "5 1 2 3 4 5 0 6 7 8 9 0 0 10 11 12 0 0 0 13 14 0 0 0 0 15",
                  "4 1 2 3 4 2 5 6 7 3 6 8 94 7 8 10", "2 1 2 2 1", "5 1 2 3 4 5 2 6 7 8 9 3 7 10 11 12 4 8 11 14 15 5 9 12 14 16",
                  "6 1 2 3 4 5 6 2 7 8 9 10 11 3 8 12 13 14 15 4 9 13 16 17 18 5 10 14 17 19 20 6 11 15 18 20 21",
                  "6 1 2 3 4 5 6 2 7 8 9 10 11 3 8 12 13 14 15 4 9 13 16 17 18 5 10 11 17 19 20 6 11 15 18 20 21",
                  "7 1 2 3 4 5 6 7 2 8 9 10 11 12 13 3 9 14 15 16 17 18 4 10 15 19 20 21 22 5 11 16 20 23 24 25 6 12 17 21 24 26 27 7 13 18 22 25 27 28"]
    expected_output = ["(?i)ya", "(?i)ya", "(?i)tidak", "(?i)tidak", "(?i)ya", "(?i)ya", "(?i)tidak", "(?i)ya", 
                       "(?i)tidak", "(?i)ya"]

    filePath = r"D:\DigiLab\Progdas2023\Modul7\CS2\CS1"

    checker = UT(filePath, input_test=input_test, output_test=expected_output, regex=True)
    checker.run()
    # checkee2 = UT("code\\CS1", input_test=input_test, output_test=expected_output)
    # checkee2.run()

    # extractor = EX("code")
    # extractor.check_plagiarism()