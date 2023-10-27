from email import message
import time
from UnitTest import UnitTest
import os
from time import sleep

if __name__ == '__main__':
    inputTest = ["1 5", "2 5", "3 5", "1 6", "2 6", "3 6", "1 7", "2 7", "3 7"]
    outputTest = ["29", "8", "8", "866", "32", "16", "750797", "256", "32"]

    for file in os.listdir("code"):
        if file.endswith(".c"):
            filename = os.path.join("code", file)
            checker = UnitTest(filename, inputTest, outputTest)

    # checker = UnitTest("code\CS1_GI_PROGDAS6_MuhammadNadzhifFikri_2306210102.c", inputTest, outputTest)
    # checker.compileC()
    # sleep(1)
    # checker.assertInputProgram()
    # # checker.multiThreadAssert()
    # res, message = checker.compareOutput()
    # print(res)
    # print(message)
