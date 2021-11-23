import sys
import os
import capstone
from evm import EVM
# import convert_bytecode

def get_list_with_prefix(prefix, len):
    return ["{}{}".format(prefix, i) for i in range(len)]

if __name__ == "__main__":
    evm = EVM(bytes.fromhex(input('>> ')))
    insts, func_list, blocks = evm.disassemble()
    
    with open("output", "w") as output:
        output.write("FUNCTIONS:\n")
        for addr, infpo in sorted(func_list.items()):
            output.write('test')


