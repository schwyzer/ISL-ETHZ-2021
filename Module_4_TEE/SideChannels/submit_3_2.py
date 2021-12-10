import os
import sys
import string
from pathlib import Path

# import subprocess
# import shlex

ADDRESS_KPP = "0x4011b6"
ADDRESS_JPP = "0x4011bc"
ADDRESS_RET = "0x40129b"
command = "/home/sgx/pin-3.11-97998-g7ecce2dac-gcc-linux-master/pin -t /home/sgx/pin-3.11-97998-g7ecce2dac-gcc-linux-master/source/tools/SGXTrace/obj-intel64/SGXTrace.so -o /home/sgx/isl/t2/out.txt -trace 1 -- /home/sgx/isl/t2/password_checker_2 {} > /dev/null 2>/dev/null"
pwd = "/home/sgx/pin-3.11-97998-g7ecce2dac-gcc-linux-master/source/tools/SGXTrace"
test_file = "/home/sgx/isl/t2/out.txt"
output_file = "/home/sgx/isl/t2/output/oput_{}"
COMPLETENESS = "complete"
PARTIAL = "partial"


def get_password(guess, password):
    character = 0
    k = 0
    os.system(command.format(guess))
    with open(test_file, "r") as f:
        line = f.readline()
        while line:
            code = line.split(":")[1]
            if code == ADDRESS_KPP:
                if password[character][1] == False:
                    password[character] = (guess[character], True)
                character += 1
                k += 1
            elif code == ADDRESS_JPP:
                character += 1
            elif code == ADDRESS_RET:
                break
            line = f.readline()
    return password, k == character


def get_length(guess, password):
    character = 0
    os.system(command.format(guess))
    with open(test_file, "r") as f:
        line = f.readline()
        while line:
            code = line.split(":")[1]
            if code == ADDRESS_KPP:
                if password[character][1] == False:
                    password[character] = (guess[character], True)
                character += 1
            elif code == ADDRESS_JPP:
                character += 1
            elif code == ADDRESS_RET:
                break
            line = f.readline()
    return password, character


def attack():
    max = 31
    equal = False
    guess = "a" * max
    password = [("a", False) for i in range(max)]
    password, size = get_length(guess, password)
    password = password[:size]
    if size < max:
        max = size
    for character in string.ascii_lowercase[1:]:
        # guess = character*max
        guess = "".join([i[0] if i[1] else character for i in password])
        password, equal = get_password(guess, password)
        if equal:
            return "".join([i[0] for i in password]), COMPLETENESS
    return "".join([i[0] for i in password]), PARTIAL


if __name__ == "__main__":
    id = sys.argv[1]
    Path("/home/sgx/isl/t2/output/").mkdir(parents=True, exist_ok=True)
    password, completeness = attack()
    open(output_file.format(id), "w").write(password + "," + completeness)

