import re


pattern = re.compile(r"29")
ouputTest = ["29", "8", "8", "866", "32", "16", "750797", "256", "32"]
for i in ouputTest:
    if re.match(pattern, i):
        print("Matched")
    else:
        print("Not matched")