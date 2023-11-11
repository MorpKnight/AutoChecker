import os, subprocess, threading, mosspy
from bs4 import BeautifulSoup
from time import sleep
import re

import requests

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
        self.regex:bool = kwargs.get("regex")
        self.actual_output = None
        self.actual_output_list = []
        self.student:Student = []
        self.mossURL = None

    def compileC(self):
        """
        The function renames a C file, compiles it using gcc, and checks if the compilation was
        successful.
        :return: a boolean value. It returns True if the compilation is successful and False if there is
        a compile error.
        """
        
        if os.path.exists(self.filename.replace(".c", ".exe")):
            self.filename = self.filename.replace(".c", "")
            return True
        
        os.rename(self.filename, self.filename.replace(" ", ""))
        sleep(1)
        compile_cmd = f"gcc {self.filename.replace(' ', '')} -o {self.filename.replace(' ', '').replace('.c', '')}"
        # compileSuccess = False
        # while(not compileSuccess):
        #     try:
        #         os.system(compile_cmd)
        #         compileSuccess = True
        #     except:
        #         os.rename(self.filename.replace(" ", ""), self.filename)
        #         print("\nCompile Error")
        #         return False
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
        try:
            stdout, stderr = process.communicate(input=input_test.encode("utf-8"), timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            return "Timeout", "Timeout"
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

    def compare_output_regex(self):
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
            try:
                count += 1
                pat = re.compile(expected_line)
                if pat.findall(actual_line):
                    matching_lines += 1
                else:
                    message += f"Test {count}: Expected {expected_line} but got {actual_line}\n"
            except:
                print(f"Error while checking {self.filename}\n")

        percentage = matching_lines / total_lines * 100

        if percentage == 0:
            message += "Need to re-check the program\n"
        return percentage, message

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
            try:
                count += 1
                # message += f"{re.search(expected_line, actual_line)}"
                if expected_line in actual_line:
                    matching_lines += 1
                else:
                    message += f"Test {count}: Expected {expected_line} but got {actual_line}\n"
            except:
                print(f"Error while checking {self.filename}\n")

        percentage = matching_lines / total_lines * 100

        if percentage == 0:
            message += "Need to re-check the program\n"
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
        # regex_pattern = r'(for\s*\(.*\)\s*\{)|(while\s*\(.*\)\s*\{)|(do\s*\{.*\}\s*while\s*\(.*\);)|(if\s*\(.*\)\s*\{.*\}\s*else\s*\{)|(switch\s*\(.*\)\s*\{)'
        regex_pattern = r'for\s*\(.*\)\s*\{.*for\s*\(.*\)\s*\{'
        with open(f"{self.filename}.c", "r") as f:
            content = f.read()
            matches = re.findall(regex_pattern, content)
            if len(matches) > 0:
                return True
            else:
                return False
    
    def check_kode_aslab(self):
        pass
    
    def check_plagiarism(self):
        moss = mosspy.Moss(220418487, "C")
        mossDir = self.folder_name
        moss.addFilesByWildcard(os.path.join(mossDir, "*.c"))
        url = moss.send()
        self.mossURL = url
        print("Report Url: " + url)

    def hydrate_plagiat(self):
        response = requests.get(self.mossURL)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table')
            high_plagiarism_names = []

            for row in table.find_all('tr')[1:]:
                cells = row.find_all('td')
                cell1 = cells[0].find('a')
                cell2 = cells[1].find('a')
                list_name_cell1 = cell1.text.split('/')
                list_name_cell2 = cell2.text.split('/')

                for name1, name2 in zip(list_name_cell1, list_name_cell2):
                    try:
                        plagiarisme_checker1 = int(name1[-4:-2])
                        plagiarisme_checker2 = int(name2[-4:-2])
                    except:
                        continue

                    if plagiarisme_checker1 >= 85 and plagiarisme_checker2 >= 85:
                        high_plagiarism_names.append(name1.split("_")[3])
                        high_plagiarism_names.append(name2.split("_")[3])
            for i in self.student:
                if i.name in high_plagiarism_names:
                    i.score = 0
                    i.message = "Plagiarism detected"

        else:
            print("Failed to retrieve the HTML content")
            

    def run(self):
        """
        The function iterates through all ".c" files in a specified folder, compiles and tests each
        file, compares the output, and generates a result CSV file.
        """

        count = len(list(filter(lambda file:file.endswith(".c") or file.endswith(".C"), os.listdir(self.folder_name))))
        print(f"\rTesting {0}/{count} files", end="")
        
        count_rn = 0
        for file in os.listdir(self.folder_name):
            if file.endswith(".c"):
                count_rn += 1
                print(f"\rTesting {count_rn}/{count} files - {self.filename}", end="")
                self.filename = os.path.join(self.folder_name, file)
                boolCheck = self.compileC()
                try:
                    student_name = self.filename.split("_")[3]
                except:
                    student_name = self.filename

                if not boolCheck:
                    self.student.append(Student(student_name, 0, "Compile Error\n", self.kode_aslab, False))
                    continue
                self.test()
                print(f"Done testing {self.filename}")

                if self.regex:
                    perc, msg = self.compare_output_regex()
                else:
                    perc, msg = self.compare_output()
                
                perc = round(perc, 2)
                
                try:
                    self.student.append(Student(student_name, perc, msg, self.kode_aslab, self.checkProgram()))
                except:
                    self.student.append(Student(student_name, perc, msg, self.kode_aslab, False))
                sleep(1)
                self.actual_output_list = []
                os.system("cls")
        self.check_plagiarism()
        self.hydrate_plagiat()
        self.result_csv()
        self.result_txt()
        print("\nDone")