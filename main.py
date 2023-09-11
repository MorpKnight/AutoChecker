import os, subprocess

def changeFormatName(filename):
    # replace space with underscore
    filename = filename.replace(" ", "_")
    # replace [] with ""
    filename = filename.replace("[", "")
    filename = filename.replace("]", "")

    # return filename

def compileCProgram(sourceFiles, executeableFiles):
    for sourceFile, executeableFile in zip(sourceFiles, executeableFiles):
        compileCmd = f"gcc -o {executeableFile} {sourceFile}"
        result = os.system(compileCmd)
        if result != 0:
            print(f"Compile {sourceFile} failed")
            exit(1)
    print("Compile success")

def executeCProgram(executeableFiles, inputFile):
    for executeableFile in executeableFiles:
        process = subprocess.Popen(executeableFile, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input=inputFile.encode("utf-8"))
        return stdout.decode("utf-8"), stderr.decode("utf-8")

def compareOuput(expectedOutput, actualOutput):
    expectedLines = expectedOutput.splitlines()
    actualLines = actualOutput.splitlines()

    matchingLines = sum([1 for expected, actual in zip(expectedLines, actualLines) if expected == actual])
    totalLines = max(len(expectedLines), len(actualLines))
    percentage = matchingLines / totalLines * 100

    return percentage

def getAllCFiles():
    # return [file for file in os.listdir() if file.endswith(".c")]
    
    # return all file .c in "code" folder
    return [os.path.join("code", file) for file in os.listdir("code") if file.endswith(".c")]

def readExpectedOutput(filename):
    with open(filename, "r") as file:
        return file.read().strip()
    
if __name__ == "__main__":
    sourceFiles = getAllCFiles()

    # change format name
    for sourceFile in sourceFiles:
        os.rename(sourceFile, sourceFile.replace(" ", "").replace("[", "").replace("]", ""))
    
    sourceFiles = getAllCFiles()

    inputFile = "input.txt"
    expectedOutput = "output.txt"

    expectedOutput = readExpectedOutput(expectedOutput)
    expectedOutput = expectedOutput.split("\n")

    with open(inputFile, "r") as file:
        inputFile = file.read()
    inputFile = inputFile.split("\n")

    executeableFiles = [file.replace(".c", "") for file in sourceFiles]
    compileCProgram(sourceFiles, executeableFiles)

    # for outputPrint, insertInput in zip(expectedOutput, inputFile):
    #     for executeableFile in executeableFiles:
    #         actualOutput, stderr = executeCProgram([executeableFile], insertInput)
    #         print(f"Actual output: {actualOutput}")
    #         print(f"Expected output: {outputPrint}")
    #         print("Comparing...")
    #         percentage = compareOuput(outputPrint, actualOutput)
    #         print(f"Matching percentage: {percentage}%")

    for executeableFile in executeableFiles:
        percentage = 0
        for outputPrint, insertInput in zip(expectedOutput, inputFile):
            actualOutput, stderr = executeCProgram([executeableFile], insertInput)
            # print(f"Actual output: {actualOutput}")
            # print(f"Expected output: {outputPrint}")
            percentage += compareOuput(outputPrint, actualOutput)
        percentage /= len(expectedOutput)
        print(f"{executeableFile}: {percentage}%")