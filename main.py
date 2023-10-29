from UnitTest import UnitTest as UT
from Extractor import Extractor as EX

if __name__ == '__main__':
    input_test = ["1 -2 1", "1 0 -1", "1 -1 6", "2 -5 2", "6 1 -35", "1 1 -1", "1 1 -5", "3 6 -9", "2.5 -9 6.8", "28.2 41.15 -33.6"]
    expected_output = ["1.001.00", "1.00-1.00", "3.00-2.00", "2.000.50", "2.33-2.50", "0.62-1.62", "1.79-2.79", "1.00-3.00", "2.521.08", "0.58-2.04"]

    checker = UT("code\\Unprak1", input_test=input_test, output_test=expected_output)
    checker.run()