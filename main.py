from ast import List
from multiprocessing import process
import os, subprocess
from time import sleep

class UnitTest:
    def __init__(self, filename, input, expectedOutput):
        self.filename = filename
        self.input = input
        self.expectedOutput = expectedOutput
        self.actualOutput = None
        self.actualOutputList = []

    def compileC(self):
        compileCmd = f"gcc {self.filename} -o {self.filename.replace('.c', '')}"
        result = os.system(compileCmd)
        if result != 0:
            print(f"Compile {self.filename} failed")
            exit(1)
        self.filename = self.filename.replace(".c", "")

    def executeProgram(self, inputString:str):
        process = subprocess.Popen(self.filename, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input=inputString.encode("utf-8"))
        self.actualOutput = stdout.decode("utf-8")
        return stdout.decode("utf-8"), stderr.decode("utf-8")
    
    def assertInputProgram(self):
        for i in self.input:
            stdout, stderr = self.executeProgram(i)
            self.actualOutputList.append(stdout)
    
    def compareOutput(self):
        try:
            expectedLines = self.expectedOutput
            actualLines = self.actualOutputList
        except:
            expectedLines = self.expectedOutput.splitlines()
            actualLines = self.actualOutput.splitlines()
        matchingLines = 0
        totalLines = max(len(expectedLines), len(actualLines))

        for expected, actual in zip(expectedLines, actualLines):
            if expected == actual:
                matchingLines += 1

        percentage = matchingLines / totalLines * 100

        return percentage

if __name__ == '__main__':
    # inputTest = ["7 2 3 3 4 4 5 5 6 1 1 2 2 9 1"]
    # outputTest = ["5\r\n7\r\n9\r\n11\r\n2\r\n4\r\n0\r\n"]

    inputTest = ["5", "10"]
    outputTest = ["Masukkan angka :     *****\r\n   *   * *\r\n  *   *  *\r\n *   *   *\r\n*****    *\r\n*   *   *\r\n*   *  *\r\n*   * *\r\n*****\r\n", 'Masukkan angka :          **********\r\n        *        * *\r\n       *        *  *\r\n      *        *   *\r\n     *        *    *\r\n    *        *     *\r\n   *        *      *\r\n  *        *       *\r\n *        *        *\r\n**********         *\r\n*        *        *\r\n*        *       *\r\n*        *      *\r\n*        *     *\r\n*        *    *\r\n*        *   *\r\n*        *  *\r\n*        * *\r\n**********\r\n']

    for file in os.listdir("code"):
        if file.endswith(".c"):
            filename = os.path.join("code", file)
            student = filename.split("_")
            student_name = student[3]

            checker = UnitTest(filename, inputTest, outputTest)
            checker.compileC()
            sleep(1)
            checker.assertInputProgram()
            # print(checker.actualOutputList)
            res = checker.compareOutput()
            print(f"{student_name}: {res}")