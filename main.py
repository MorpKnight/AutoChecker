from UnitTest import UnitTest as UT
from Extractor import Extractor as EX

def read_input(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        f.close()
    return lines

if __name__ == '__main__':
    input_test = read_input("input.txt")
    # for i in input_test remove \n
    for i in range(len(input_test)):
        input_test[i] = input_test[i].replace("\n", "")
    expected_output = read_input("output.txt")
    # for i in expected_output remove \n
    for i in range(len(expected_output)):
        expected_output[i] = expected_output[i].replace("\n", "")

    filePath = r"D:\DigiLab\Progdas2023\Modul7\PT\PT"

    checker = UT(filePath, input_test=input_test, output_test=expected_output, regex=True)
    checker.run()
    # checker.generate_output()

    # extractor = EX(filePath, folderName=["PT"])
    # extractor.run()