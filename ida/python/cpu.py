import idc
import idaapi
from idaapi import *
import idautils

import hashes

class EVMAsm(object):
    pass

    class Instruction(object):
        def __init__(self, opcode, name, operand_size, pops, pushes, fee,
                description, operand=None, offset=0):

