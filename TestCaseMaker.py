import random, os

# check if input.txt exists, if not, create it
if not os.path.exists("input.txt"):
    f = open("input.txt", "w")
    f.close()

def generate_random_header():
    random_number = [random.randint(0, 1) for i in range(3)]
    for i in range(8):
        random_number.append(random.randint(0, 999))
    return random_number

# write to input.txt
with open("input.txt", "a") as f:
    for i in range(100):
        random_header = generate_random_header()
        random_header = [str(i) for i in random_header]
        random_header = " ".join(random_header)
        f.write(random_header + "\n")
    f.close()

def read_input():
    with open("input.txt", "r") as f:
        lines = f.readlines()
        f.close()
    return lines

print(read_input())