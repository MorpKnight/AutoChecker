import re


pattern = re.compile(r"(?i)ada.*ada.*ada.*ada")
ouputTest = ["disini ada tapi ADA, tidak Ada tapi ADA", "Disana tidak ada tapi ada tidak ADA tidak"]
for i in ouputTest:
    if pattern.findall(i):
        print("Matched")
    else:
        print("Not matched")
