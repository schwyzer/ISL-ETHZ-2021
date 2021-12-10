import subprocess
import time
import os

COMMAND_MANAGER = "sh /home/isl/t1/run_manager.sh"
COMMAND_PERIPHERAL = "sh /home/isl/t1/run_peripheral.sh"
COMMAND_RUN = "nohup sh /home/isl/t1/run.sh"
COMMAND_START = "sh /home/isl/t1/start.sh"
flag_1_gdb_command = "screen -dmS string_parser gdb /home/isl/t1/string_parser -ex 'set pagination off' -ex 'set follow-fork-mode child' -ex 'b *0x00403545' -ex 'run' -ex 'set combinedResponse = \"de2c6a4b54d2506bc8e013a54e4f8ec397f9c5c52575318a035e1f2f3e61b09663c197a654aa3531c4a019e041395b8037cbe6daf9358e337354e61658e186b5ca6198d8ae31e469dabebe0d6ba2bcb1f8fbe352963c124562247f798ed99e2c5d356bd691a37f2bb2655d5baa01f03b3ecb6b520d4a714298b608cc22ab9ade6a4dc1cfd37cd7879cb9823210a7f987fa0a8ebbc80b3eb5b2e1a2beb9297377092a43cae019e4bdaa2b7627209674714eff53aa121c2b6aaf5e5bf4c56c9922c103ef3ce4f68169b695370e5783c53bcc633fd741381782c78bc397ef6c2924ec51fa0987e857216e7eb365ff1debeb69bc4d4502182700ad7bf62bbc4254f090df0b5fa114bac8d662afe83c1c9f6b45c84af86ba7bf6cf597501c\"' -ex 'c'"

flag_2_gdb_command = "screen -dmS string_parser gdb /home/isl/t1/string_parser -ex 'set pagination off' -ex 'set follow-fork-mode child' -ex 'b *0x0040339a' -ex 'b *0x004033e8' -ex 'b *0x004033fb' -ex 'run' -ex 'jump +1' -ex 'c' -ex 'jump +1' -ex 'c' -ex 'jump +1' -ex 'c'"


def get_first_flag():
    # start ./run.sh
    # start gdb command
    # instructions
    # b *0x00403545
    # set combinedResponse = "de2c6a4b54d2506bc8e013a54e4f8ec397f9c5c52575318a035e1f2f3e61b09663c197a654aa3531c4a019e041395b8037cbe6daf9358e337354e61658e186b5ca6198d8ae31e469dabebe0d6ba2bcb1f8fbe352963c124562247f798ed99e2c5d356bd691a37f2bb2655d5baa01f03b3ecb6b520d4a714298b608cc22ab9ade6a4dc1cfd37cd7879cb9823210a7f987fa0a8ebbc80b3eb5b2e1a2beb9297377092a43cae019e4bdaa2b7627209674714eff53aa121c2b6aaf5e5bf4c56c9922c103ef3ce4f68169b695370e5783c53bcc633fd741381782c78bc397ef6c2924ec51fa0987e857216e7eb365ff1debeb69bc4d4502182700ad7bf62bbc4254f090df0b5fa114bac8d662afe83c1c9f6b45c84af86ba7bf6cf597501c"
    # c
    os.system("pkill -9 node")
    os.system("pkill -9 node")
    os.system("pkill -9 string_pa")
    os.system('screen -wipe')
    os.system('screen -S string_parser -X quit')
    manager = subprocess.Popen(COMMAND_MANAGER, shell=True, stdin=subprocess.PIPE)
    peripheral = subprocess.Popen(COMMAND_PERIPHERAL, shell=True, stdin=subprocess.PIPE)
    string_parser = subprocess.Popen(
        flag_1_gdb_command, shell=True, stdin=subprocess.PIPE
    )

    time.sleep(2)

    subprocess.run(COMMAND_START, shell=True)

    while not os.path.isfile("/home/isl/scripts/flag1-1"):
        continue

    time.sleep(1)
    os.system("pkill -9 string_pa")
    os.system('screen -wipe')
    os.system('screen -S string_parser -X quit')

    return manager, peripheral


def get_second_flag():
    # restart
    # instructions
    # set follow-fork-mode child
    # b *0x0040339a
    # b *0x004033e8
    # b *0x004033fb
    # jump +1 on each breakpoint
    os.system("pkill -9 node")
    os.system("pkill -9 node")
    manager = subprocess.Popen(COMMAND_MANAGER, shell=True, stdin=subprocess.PIPE)
    peripheral = subprocess.Popen(COMMAND_PERIPHERAL, shell=True, stdin=subprocess.PIPE)
    string_parser = subprocess.Popen(
        flag_2_gdb_command, shell=True, stdin=subprocess.PIPE
    )
    time.sleep(2)
    subprocess.run(COMMAND_START, shell=True)

    while not os.path.isfile("/home/isl/scripts/flag1-2"):
        continue

    os.system("pkill -9 string_pa")
    os.system('screen -wipe')
    os.system('screen -S string_parser -X quit')


if __name__ == "__main__":
    get_first_flag()
    get_second_flag()
    time.sleep(1)
    os.chdir("/home/isl/t1/")
    subprocess.run(COMMAND_RUN, shell=True)


