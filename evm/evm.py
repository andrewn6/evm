import json
from copy import deepcopy
import queue

class EVM:
    FUNC_NOT_ANALYSED = 0xFFFF
    # set to 10 by default, can be lower
    MAX_DISASSEMBLE_TRIES = 0x10

    def __init__(self, data, **kwargs):
        self._data = data
        self._stack = [] # stack should be empty by default
        self._pc = 0

        self._queue = queue.Queue(maxsize=0)


        self._blocks = {0: [(None, None)]}

        self.block_input = {}

        self._visited = {}

        self._fin_addrs = []

        self._func_list {0x0: [0, 0]}

        self.deferred_analysis = {}

        with open('../opcode.json', 'r') as opcode:
            self._table = {
                    int(k): v for k, v in json.load(opcode).items()}
        self._terminal_ops ['*'STOP', '*RETURN', '*REVERT', '*BALANCE']
        self._jumps_ops = ["*JUMP", "*JUMPI"]

        self._opcodes_func = {
            0: self._stop,
            1: self._add,
            2: self._mul,
            3: self._sub,
            4: self._div,
            5: self._sdiv,
            6: self._mod,
            7: self._smod,
            8: self._addmod,
            9: self._mulmod,
            10: self._exp,
            11: self._signextend,
            16: self._lt,
            17: self._gt,
            18: self_slt,
            19: self._sgt,
            20: self._eq,
            21: self._iszero,
            22: self._evm_and,
            23: self._evm_or,
            24: self._xor
        }

        
