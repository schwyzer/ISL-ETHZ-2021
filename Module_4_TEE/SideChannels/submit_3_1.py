import os
import sys
import string
from pathlib import Path

ADDRESS_EQUAL_LESS = "0x4011d0"
ADDRESS_KPP = "0x401211"
ADDRESS_POW = "0x401217"
ADDRESS_DIREC = "0x40126f"
ADDRESS_SUB = "0x40127e"
ADDRESS_END = "0x401288"
ADDRESS_EQUAL = "0x4012a8"
COMPLETENESS = "complete"
PARTIAL = "partial"
char_int = dict(zip(string.ascii_lowercase, range(0, 26)))
int_char = dict(zip(range(0, 26), string.ascii_lowercase))


def get_password(filename):
    guess = filename.split(".")[0]
    complete = False
    equal_or_less = False
    equal = False
    password = ""
    character = 0
    with open(filename, "r") as f:
        line = f.readline()
        while line:
            code = line.split(":")[1]
            if code == ADDRESS_EQUAL_LESS:
                line = f.readline()
                if line[0] == "R":
                    equal_or_less = True
            elif code == ADDRESS_KPP:
                # right char
                password += guess[character]
                character += 1
            elif code == ADDRESS_POW:
                # pow address
                line = f.readline()
                code = line.split(":")[1]
                substracting = 0
                while line:
                    code = line.split(":")[1]
                    if code == ADDRESS_SUB:
                        substracting += 1
                    elif code == ADDRESS_END:
                        break
                    line = f.readline()
                    # code = line.split(':')[1]
                # guess password
                guessed = (char_int[guess[character]] + substracting) % 26
                password += int_char[guessed]
                character += 1
            elif code == ADDRESS_EQUAL:
                equal = True
            line = f.readline()
        # TODO check completeness and other stuff
        if (equal and equal_or_less) or (not equal_or_less):
            complete = True
        return password, complete


def attack(dir):
    os.chdir(dir)
    # real_password = list()
    # crossreference = list()
    prefix = ""
    for f in os.listdir():
        password, complete = get_password(f)
        if complete:
            # if len(password) != real_password:
            # 	real_password = real_password[
            return password, COMPLETENESS
        elif password.startswith(prefix):
            prefix = password
    return prefix, PARTIAL


if __name__ == "__main__":
    folder_traces = sys.argv[1]
    id = sys.argv[2]
    folder_file = "/home/sgx/isl/t1/output/oput_" + id
    Path("/home/sgx/isl/t1/output").mkdir(parents=True, exist_ok=True)
    password, complete = attack(folder_traces)
    open(folder_file, "w").write(password + "," + complete)

