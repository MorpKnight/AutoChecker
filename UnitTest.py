import os, subprocess, threading, mosspy
from bs4 import BeautifulSoup
from time import sleep
import re

import requests

class Student:
    def __init__(self, name, score, message, kode_aslab, regex_output):
        self.name = name
        self.score:float = score
        self.message = message
        self.kode_aslab = kode_aslab
        self.regex_output:bool = regex_output

class UnitTest:
    def __init__(self, folder_name, **kwargs):
        self.folder_name = folder_name
        self.filename = None
        self.input_test = kwargs.get("input_test")
        self.expected_output = kwargs.get("output_test")
        self.kode_aslab = kwargs.get("kode_aslab")
        self.regex:bool = kwargs.get("regex")
        self.regex_pattern = kwargs.get("regex_pattern")
        self.actual_output = None
        self.actual_output_list = []
        self.student:Student = []
        self.mossURL = None
        self.run()

    def read_input(self):
        with open(".txt/input.txt", "r") as f:
            lines = f.readlines()
            f.close()
        for i in range(len(lines)):
            lines[i] = lines[i].replace("\n", "")
        return lines
    
    def read_output(self):
        with open(".txt/output.txt", "r") as f:
            lines = f.readlines()
            f.close()
        for i in range(len(lines)):
            lines[i] = lines[i].replace("\n", "")
        return lines

    def compileC(self):
        if os.path.exists(self.filename.replace(".c", ".exe")):
            self.filename = self.filename.replace(".c", "")
            return True
        
        os.rename(self.filename, self.filename.replace(" ", ""))
        sleep(1)
        compile_cmd = f"gcc {self.filename.replace(' ', '')} -o {self.filename.replace(' ', '').replace('.c', '')}"
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
        process = subprocess.Popen(self.filename, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            stdout, stderr = process.communicate(input=input_test.encode("utf-8"), timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            return "Timeout", "Timeout"
        self.actual_output = stdout.decode("utf-8")
        return stdout.decode("utf-8"), stderr.decode("utf-8")
    
    def test(self):
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
                pat = re.compile(f'(?i){expected_line}')
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
        return self.student
    
    def generate_result(self):
        if not os.path.exists(".txt"):
            os.mkdir(".txt")
        with open(".txt/result.txt", "w") as f:
            f.write("Name: Score\n")
            for i in self.student:
                if i.message == "":
                    f.write(f"Name: {i.name}\nScore: {i.score}\nCheck program: {i.regex_output}\n\n")
                else:
                    f.write(f"Name: {i.name}\nScore: {i.score}\nCheck program: {i.regex_output}\nMessage:\n{i.message}\n\n")
        with open(".txt/result.csv", "w") as f:
            f.write("Name, Score\n")
            for i in self.student:
                f.write(f"{i.name}, {i.score}\n")

    def checkProgram(self):
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
        self.check_plagiarism()
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
        self.input_test = self.input_test if self.input_test else self.read_input()
        self.expected_output = self.expected_output if self.expected_output else self.read_output()
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
        try:
            self.hydrate_plagiat()
        except:
            pass
        self.generate_result()
        print("\nDone")