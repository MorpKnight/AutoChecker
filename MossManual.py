from bs4 import BeautifulSoup
import mosspy
from requests import request

class Student:
    def __init__(self, studentName:str, studentScore:float):
        self.studentName = studentName
        self.studentScore = studentScore
    
class MossChecker:
    def __init__(self, mossURL:str):
        self.mossURL = mossURL
        self.students = []
    
    def obtainStudent(self):
        with open(".txt/result.csv", "r") as f:
            lines = f.readlines()
            for i in range(len(lines)):
                lines[i] = lines[i].replace("\n", "")
            for line in lines:
                line = line.split(", ")
                self.students.append(Student(line[0], line[1]))
    
    def checkPlagiarism(self):
        response = request.get(self.mossURL)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table")
            rows = table.find_all("tr")

MossChecker("http://moss.stanford.edu/results/5/4140649420182/")
