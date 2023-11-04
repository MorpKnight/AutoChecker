import re

output = ["YA", "YA", "TIDAK", "ya", "iYa", "tidakbisaya"]
inputtest = ["IYA", "YA", "TIDAK"]

pattern = re.compile("(?i)YA")

for i in range(len(output)):
    if pattern.findall(output[i]):
        print("YA")
    else:
        print("TIDAK")