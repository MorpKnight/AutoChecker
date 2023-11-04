import re

output = ["YA", "YA", "TIDAK"]
inputtest = ["IYA", "YA", "TIDAK"]

for i in range(max(len(output), len(inputtest))):
    if re.match(output[i], inputtest[i]):
        print("True")
    else:
        print("False")