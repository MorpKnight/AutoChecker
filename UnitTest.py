import os, subprocess
from time import sleep
import re

class Student:
    def __init__(self, name, score, message, kode_aslab, regex_output):
        """
        The function initializes an object with attributes such as name, score, message, kode_aslab, and
        regex_output.
        
        :param name: The name parameter is a string that represents the name of the object being
        initialized
        :param score: The `score` parameter is a float that represents the score of a student. It is
        used to store and manipulate the score value
        :param message: The `message` parameter is a string that represents a message or description
        associated with an object. It can be used to provide additional information or context about the
        object
        :param kode_aslab: The parameter "kode_aslab" is a variable that represents the code or
        identification of the assistant lab. It could be a string or any other data type that is used to
        uniquely identify the lab assistant
        :param regex_output: The `regex_output` parameter is a boolean value that indicates whether the
        output of a regular expression match is expected or not. If `regex_output` is `True`, it means
        that the output of the regular expression match is expected. If `regex_output` is `False`, it
        means that the
        """
        self.name = name
        self.score:float = score
        self.message = message
        self.kode_aslab = kode_aslab
        self.regex_output:bool = regex_output

class UnitTest:
    def __init__(self, folder_name, **kwargs):
        """
        The function initializes various attributes of an object, including a folder name, filename,
        input test, expected output, actual output, actual output list, and a student object.
        
        :param folder_name: The `folder_name` parameter is used to specify the name of the folder where
        the files will be stored or retrieved from
        """
        self.folder_name = folder_name
        self.filename = None
        self.input_test = kwargs.get("input_test")
        self.expected_output = kwargs.get("output_test")
        self.kode_aslab = kwargs.get("kode_aslab")
        self.actual_output = None
        self.actual_output_list = []
        self.student:Student = []

    def compileC(self):
        """
        The function renames a C file, compiles it using gcc, and checks if the compilation was
        successful.
        :return: a boolean value. It returns True if the compilation is successful and False if there is
        a compile error.
        """
        os.rename(self.filename, self.filename.replace(" ", ""))
        sleep(1)

        compile_cmd = f"gcc -w {self.filename} -o {self.filename.replace('.c', '')}"
        try:
            os.system(compile_cmd)
        except:
            print("Compile Error")
            return False
        if not os.path.exists(self.filename.replace(".c", ".exe")):
            print("Compile Error")
            return False

        self.filename = self.filename.replace(".c", "")
        sleep(3)
        return True
    
    def executeProgram(self, input_test:str):
        """
        The function executes a program and returns the standard output and standard error.
        
        :param input_test: The `input_test` parameter is a string that represents the input that will be
        passed to the program being executed. It is encoded as UTF-8 before being passed to the program
        :type input_test: str
        :return: The function `executeProgram` returns two values: `stdout.decode("utf-8")` and
        `stderr.decode("utf-8")`.
        """
        process = subprocess.Popen(self.filename, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input=input_test.encode("utf-8"))
        self.actual_output = stdout.decode("utf-8")
        return stdout.decode("utf-8"), stderr.decode("utf-8")
    
    def test(self):
        """
        The function takes a list of input tests, executes a program with each input, and appends the
        resulting output (if any) to a list after converting it to uppercase.
        """
        for i in self.input_test:
            stdout, stderr = self.executeProgram(i)
            stdout = stdout.replace("\r", "").replace("\n", "").replace(" ", "")
            if stdout is not None:
                self.actual_output_list.append(stdout.upper())
            else:
                self.actual_output_list.append(stderr)

    def compare_output(self):
        """
        The function `compare_output` compares the expected output with the actual output and returns
        the percentage of matching lines and a message indicating any differences.
        :return: a tuple containing the percentage of matching lines between the expected output and
        actual output, and a message string that lists any differences between the expected and actual
        output.
        """
        message = ""
        
        try:
            expected_lines = self.expected_output
            actual_lines = self.actual_output_list
        except:
            expected_lines = self.expected_output.splitlines()
            actual_lines = self.actual_output.splitlines()
        matching_lines = 0
        total_lines = max(len(expected_lines), len(actual_lines))
        if len(expected_lines) != len(actual_lines):
            print(f"Expected {len(expected_lines)} lines but got {len(actual_lines)} lines")
            
        count = 0
        for expected_line, actual_line in zip(expected_lines, actual_lines):
            count += 1
            # message += f"{re.search(expected_line, actual_line)}"
            if expected_line == actual_line:
                matching_lines += 1
            else:
                message += f"Test {count}: Expected {expected_line} but got {actual_line}\n"

        percentage = matching_lines / total_lines * 100
        return percentage, message
    
    def get_student(self):
        """
        The function returns the value of the "student" attribute.
        :return: The method is returning the value of the "student" attribute.
        """
        return self.student
    
    def result_csv(self):
        """
        The function `result_csv` writes the names and scores of students to a CSV file called
        "result.csv".
        """
        with open("result.csv", "a") as f:
            f.write("Name, Score\n")
            for i in self.student:
                f.write(f"{i.name}, {i.score}\n")

    def result_txt(self):
        """
        The function writes the name, score, and message of each student in a list to a text file called
        "result.txt".
        """
        with open("result.txt", "w") as f:
            for i in self.student:
                if i.message == "":
                    f.write(f"Name: {i.name}\nScore: {i.score}\nCheck program: {i.regex_output}\n\n")
                else:
                    f.write(f"Name: {i.name}\nScore: {i.score}\nCheck program: {i.regex_output}\nMessage:\n{i.message}\n\n")

    def checkProgram(self):
        """
        The function checks if a C program contains any loops, conditional statements, or switch
        statements.
        :return: a boolean value. If there are any matches found in the content of the file that match
        the specified regular expression pattern, it will return True. Otherwise, it will return False.
        """
        regex_pattern = r'(for\s*\(.*\)\s*\{)|(while\s*\(.*\)\s*\{)|(do\s*\{.*\}\s*while\s*\(.*\);)|(if\s*\(.*\)\s*\{.*\}\s*else\s*\{)|(switch\s*\(.*\)\s*\{)'
        with open(f"{self.filename}.c", "r") as f:
            content = f.read()
            matches = re.findall(regex_pattern, content)
            if len(matches) > 0:
                return True
            else:
                return False
    
    def check_kode_aslab(self):
        pass

    def run(self):
        """
        The function iterates through all ".c" files in a specified folder, compiles and tests each
        file, compares the output, and generates a result CSV file.
        """
        count = 0
        for file in os.listdir(self.folder_name):
            if file.endswith(".c"):
                count += 1
        print(f"\rTesting {0}/{count} files", end="")
        
        count_rn = 0
        for file in os.listdir(self.folder_name):
            if file.endswith(".c"):
                count_rn += 1
                print(f"\rTesting {count_rn}/{count} files", end="")
                self.filename = os.path.join(self.folder_name, file)
                boolCheck = self.compileC()
                if not boolCheck:
                    self.student.append(Student(self.filename.split("_")[3], 0, "Compile Error", self.kode_aslab, False))
                    continue
                self.test()
                perc, msg = self.compare_output()
                student_name = self.filename.split("_")[3]
                perc = round(perc, 2)
                try:
                    self.student.append(Student(student_name, perc, msg, self.kode_aslab, self.checkProgram()))
                except:
                    self.student.append(Student(student_name, perc, msg, self.kode_aslab, False))
                # print(f"\r{self.filename} {self.checkProgram()}", end="")
                sleep(1)
                self.actual_output_list = []
                os.system("cls")
        self.result_csv()
        self.result_txt()
        print("\nDone")