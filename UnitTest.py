from operator import indexOf
import os, subprocess
import threading
from time import sleep

class UnitTest:
    def __init__(self, filename, inputTest, expectedOutput):
        self.filename = filename
        self.input = inputTest
        self.expectedOutput = expectedOutput
        self.actualOutput = None
        self.actualOutputList = []
        self.count_event = threading.Event()
        self.assert_event = threading.Event()

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
        sleep(10)
        return True

    def executeProgram(self, inputString:str):
        process = subprocess.Popen(self.filename, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input=inputString.encode("utf-8"))
        self.actualOutput = stdout.decode("utf-8")
        return stdout.decode("utf-8"), stderr.decode("utf-8")
    
    def assertInputProgram(self):
        for i in self.input:
            stdout, stderr = self.executeProgram(i)
            stdout = stdout.replace("\r", "").replace("\n", "").replace(" ", "")
            if stdout is not None:
                self.actualOutputList.append(stdout.upper())
            else:
                self.actualOutputList.append(stderr)

    def multiThreadAssert(self):
        count = threading.Thread(target=self.count5Seconds)
        assertFunction = threading.Thread(target=self.assertInputProgram)
        count.start()
        assertFunction.start()

        if count.join():
            assertFunction.join()
            return True
    
    def compareOutput(self):
        print(f"{self.filename} is comparing")
        message = ""
        try:
            expectedLines = self.expectedOutput
            actualLines = self.actualOutputList
        except:
            expectedLines = self.expectedOutput.splitlines()
            actualLines = self.actualOutput.splitlines()
        matchingLines = 0
        totalLines = max(len(expectedLines), len(actualLines))
        if len(expectedLines) != len(actualLines):
            print("Test case is not equal")

        for expected, actual in zip(expectedLines, actualLines):
            if expected in actual:
                matchingLines += 1
                # print test number is passed
                print(f"Test {indexOf(actualLines, actual) + 1}: AC")
            else:
                message += f"Expected: {expected}\nActual: {actual}\n"
                print(f"Test {indexOf(actualLines, actual) + 1}: WA")

        percentage = matchingLines / totalLines * 100

        return percentage, message
    
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
            f.write(message)
            f.write("\n")

    def printResultToCSV(self):
        if not os.path.exists("result.csv"):
            open("result.csv", "w").close()

        with open("result.csv", "a") as f:
            student = self.filename.split("_")
            try:
                student = student[3]
            except:
                student = student
            percentage, message = self.compareOutput()
            f.write(f"{student};{percentage}\n")