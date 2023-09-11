import os, subprocess

def compileCProgram(sourceFiles, executeableFiles):
    for sourceFile, executeableFile in zip(sourceFiles, executeableFiles):
        compileCmd = f"gcc -o {executeableFile} {sourceFile}"
        result = os.system(compileCmd)
        if result == 0:
            print(f"Compile {sourceFile} success")
        else:
            print(f"Compile {sourceFile} failed")

    # compileCmd = f"gcc -o {executeableFile} {sourceFiles}"
    # result = os.system(compileCmd)
    # if result == 0:
    #     print("Compile success")
    # else:
    #     print("Compile failed")

def executeCProgram(executeableFiles, inputFile):
    for executeableFile in executeableFiles:
        # with open(inputFile, "r") as file:
        #     inputFile = file.read()
        process = subprocess.Popen(executeableFile, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input=inputFile.encode("utf-8"))
        return stdout.decode("utf-8"), stderr.decode("utf-8")
    # with open(inputFile, "r") as file:
    #     inputText = file.read()

    # process = subprocess.Popen(executeableFile, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # stdout, stderr = process.communicate(input=inputText.encode("utf-8"))
    # return stdout.decode("utf-8"), stderr.decode("utf-8")

def compareOuput(expectedOutput, actualOutput):
    expectedLines = expectedOutput.splitlines()
    actualLines = actualOutput.splitlines()

    matchingLines = sum([1 for expected, actual in zip(expectedLines, actualLines) if expected == actual])
    totalLines = max(len(expectedLines), len(actualLines))
    percentage = matchingLines / totalLines * 100

    return percentage

def getAllCFiles():
    return [file for file in os.listdir() if file.endswith(".c")]

def readExpectedOutput(filename):
    with open(filename, "r") as file:
        return file.read().strip()
    
if __name__ == "__main__":
    sourceFiles = getAllCFiles()

    inputFile = "input.txt"
    expectedOutput = "output.txt"

    expectedOutput = readExpectedOutput(expectedOutput)
    # expectedOutput to list
    expectedOutput = expectedOutput.split("\n")

    # read inputFile and split to list
    with open(inputFile, "r") as file:
        inputFile = file.read()
    inputFile = inputFile.split("\n")
    
    print("Compiling...")

    executeableFiles = [file.replace(".c", "") for file in sourceFiles]
    for outputPrint, insertInput in zip(expectedOutput, inputFile):
        compileCProgram(sourceFiles, executeableFiles)
        for executeableFile in executeableFiles:
            actualOutput, stderr = executeCProgram([executeableFile], insertInput)
            print("Comparing...")
            percentage = compareOuput(outputPrint, actualOutput)
            print(f"Matching percentage: {percentage}%")
    # for output in expectedOutput:
    #     compileCProgram(sourceFiles, executeableFiles)
    #     for executeableFile in executeableFiles:
    #         actualOutput, stderr = executeCProgram([executeableFile], inputFile)
    #         print("Comparing...")
    #         percentage = compareOuput(output, actualOutput)
    #         print(f"Matching percentage: {percentage}%")

    # compileCProgram(sourceFiles, executeableFiles)

    # print("Executing...")
    # for executeableFile in executeableFiles:
    #     actualOutput, stderr = executeCProgram([executeableFile], inputFile)
    #     print("Comparing...")
    #     percentage = compareOuput(expectedOutput, actualOutput)
    #     print(f"Matching percentage: {percentage}%")