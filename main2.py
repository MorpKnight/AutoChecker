import contextlib
import os, subprocess
import threading
from time import sleep
import time

class UnitTest:
    def __init__(self, filename, input, expectedOutput):
        self.filename = filename
        self.input = input
        self.expectedOutput = expectedOutput
        self.actualOutput = None
        self.actualOutputList = []

    def compileC(self):
        if os.path.exists(self.filename + ".exe"):
            return True
        compileCmd = f"gcc {self.filename} -o {self.filename.replace('.c', '')}"
        try:
            result = os.system(compileCmd)
        except:
            print(f"Compile {self.filename} failed")
            exit(1)
        self.filename = self.filename.replace(".c", "")
    
    def count5Seconds(self):
        for i in range(3):
            sleep(1)
        
        return True

    def executeProgram(self, inputString:str):
        process = subprocess.Popen(self.filename, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input=inputString.encode("utf-8"))
        self.actualOutput = stdout.decode("utf-8")
        return stdout.decode("utf-8"), stderr.decode("utf-8")
    
    def assertInputProgram(self):
        for i in self.input:
            stdout, stderr = self.executeProgram(i)
            self.actualOutputList.append(stdout)

        self.removeMultipleOutput()

    def multiThreadAssert(self):
        count = threading.Thread(target=self.count5Seconds)
        assertFunction = threading.Thread(target=self.assertInputProgram)
        count.start()
        assertFunction.start()

        # if count already finish, then stop assertFunction
        if count.join():
            assertFunction.join()
            return True
    
    def compareOutput(self):
        message = ""
        try:
            expectedLines = self.expectedOutput
            actualLines = self.actualOutputList
        except:
            expectedLines = self.expectedOutput.splitlines()
            actualLines = self.actualOutput.splitlines()
        matchingLines = 0
        totalLines = max(len(expectedLines), len(actualLines))

        for expected, actual in zip(expectedLines, actualLines):
            # if expected == actual:
            #     matchingLines += 1
            if expected in actual:
                matchingLines += 1
            else:
                message += f"Expected: {expected}\nActual: {actual}\n"

        percentage = matchingLines / totalLines * 100

        return percentage, message
    
    def removeMultipleOutput(self):
        for output in self.actualOutputList:
            output = output.replace("\r", "")
            output = output.replace("\n", "")
    
    def collectOutputFormToTXT(self):
        if not os.path.exists("output.txt"):
            open("output.txt", "w").close()

        with open("output.txt", "a") as f:
            for output in self.actualOutputList:
                f.write(output)
                f.write("\n")
            f.write("\n")

    def removeSpaceNameFile(self):
        if " " in self.filename:
            self.filename = self.filename.replace(" ", "")

    def printResultToTXT(self):
        if not os.path.exists("result.txt"):
            open("result.txt", "w").close()

        with open("result.txt", "a") as f:
            student = self.filename.split("_")
            student = student[3]
            percentage, message = self.compareOutput()
            f.write(f"{student}: {percentage}\n")
            # f.write(message)
            # f.write("\n\n")

if __name__ == '__main__':
    # inputTest = ["7 2 3 3 4 4 5 5 6 1 1 2 2 9 1"]
    # outputTest = ["5\r\n7\r\n9\r\n11\r\n2\r\n4\r\n0\r\n"]

    inputTest = ["10 1 2 3 4 5", "25 10 10 10", "1 2", "10 10 0 0 0 0 1", "0 0 1"]
    outputTest = ["4", "2", "0", "5", "1"]

    for file in os.listdir("code"):
        if file.endswith(".c"):
            filename = os.path.join("code", file)
            student = filename.split("_")
            student_name = student[3]

            checker = UnitTest(filename, inputTest, outputTest)
            checker.removeSpaceNameFile()
            checker.compileC()
            sleep(1)
            # checker.assertInputProgram()
            checker.multiThreadAssert()
            # print(checker.actualOutputList)
            # checker.collectOutputFormToTXT()
            # res = checker.compareOutput()
            # print(f"{student_name}: {res}")
            checker.printResultToTXT()