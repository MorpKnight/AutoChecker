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
        self.main()

    def compileC(self):
        os.rename(self.filename, self.filename.replace(" ", ""))
        sleep(1)

        if os.path.exists(self.filename + ".exe"):
            return True
        compileCmd = f"gcc {self.filename} -o {self.filename.replace('.c', '')}"
        try:
            os.system(compileCmd)
        except:
            print("Compile Error")
            return False
        self.filename = self.filename.replace(".c", "")
        sleep(3)
        return True
    
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

        count = 0
        for expected, actual in zip(expectedLines, actualLines):
            count += 1
            message += f"Expected: {expected} | Actual: {actual}\n"
            if expected in actual:
                matchingLines += 1
                print(f"Test {count}: ✅")
            else:
                print(f"Test {count}: ❌")

        percentage = matchingLines / totalLines * 100

        return percentage, message

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

    def main(self):
        self.compileC()
        self.assertInputProgram()
        self.printResultToCSV()
        self.printResultToTXT()