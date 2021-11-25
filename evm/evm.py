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

        self._func_list = {0x0: [0, 0]}

        self.deferred_analysis = {}

        with open('../opcode.json', 'r') as opcode:
            self._table = {
                    int(k): v for k, v in json.load(opcode).items()}
        self._terminal_ops = ['*STOP', '*RETURN', '*REVERT', '*BALANCE']
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
            18: self._slt,
            19: self._sgt,
            20: self._eq,
            21: self._iszero,
            22: self._evm_and,
            23: self._evm_or,
            24: self._xor,
            25: self._evm_not,
            26: self._byte,
            27: self._shl,
            28: self.shr,
            29: self._sar,
            30: self._address,
            31: self._balance,
            32: self._sha3,
            48: self._address,
            49: self._balance,
            50: self._origin,
            51: self._caller,
            52: self._callvalue,
            53: self._calldataload,
            54: self._calldatasize,
            55: self._calldatacopy,
            56: self._codesize,
            57: self._codecopy,
            58: self._gasprice,
            59: self._extcodesize,
            60: self._extcodecopy,
            61: self._returndatasize,
            62: self._returndatacopy,
            63: self._extcodehash,
            64: self._blockhash,
            65: self._coinbase,
            66: self._timestamp,
            67: self._number,
            68: self._difficulty,
            69: self._gaslimit,
            80: self._pop,
            81: self._mload,
            82: self._mstore,
            83: self._mstore8,
            84: self._sload,
            85: self._sstore,
            86: self._jump,
            87: self._jumpi,
            88: self._evm_pc,
            89: self._msize,
            90: self._gas,
            91: self._jumpdest,
            96: self._push,
            97: self._push,
            98: self._push,
            99: self._push,
            100: self._push,
            101: self._push,
            102: self._push,
            103: self._push,
            104: self._push,
            105: self._push,
            106: self._push,
            107: self._push,
            108: self._push,
            109: self._push,
            110: self._push,
            111: self._push,
            112: self._push,
            113: self._push,
            114: self._push,
            115: self._push,
            116: self._push,
            117: self._push,
            118: self._push,
            119: self._push,
            120: self._push,
            121: self._push,
            122: self._push,
            123: self._push,
            124: self._push,
            125: self._push,
            126: self._push,
            127: self._push,
            128: self._dup,
            129: self._dup,
            130: self._dup,
            131: self._dup,
            132: self._dup,
            133: self._dup,
            134: self._dup,
            135: self._dup,
            136: self._dup,
            137: self._dup,
            138: self._dup,
            139: self._dup,
            140: self._dup,
            141: self._dup,
            142: self._dup,
            143: self._dup,
            144: self._swap,
            145: self._swap,
            146: self._swap,
            147: self._swap,
            148: self._swap,
            149: self._swap,
            150: self._swap,
            151: self._swap,
            152: self._swap,
            153: self._swap,
            154: self._swap,
            155: self._swap,
            156: self._swap,
            157: self._swap,
            158: self._swap,
            159: self._swap,
            160: self._log,
            161: self._log,
            162: self._log,
            163: self._log,
            164: self._log,
            176: self._push,
            177: self._dup,
            178: self._swap,
            240: self._create,
            241: self._call,
            242: self._callcode,
            243: self._evm_return,
            244: self._delegatecall,
            245: self._create2,
            250: self._staticcall,
            253: self._revert,
            255: self._selfdestruct,
        }
    
    def _insert_entry_list_dic(self, dict, k, v):
        if k not in dict:
            dict[k] = []
        if v not in dict[k]:
            dict[k].append(v)

    def _check_visited(self):
        if self._pc not in self._visited:
            return True
        
        if self._visited[self._pc][1] < self.MAX_DISASSEMBLE_TRIES: 
            return True
        
        else:
            return False

    def _mark_visited(self, inst):  
        if self._pc not in self._visited:   
            self._visited[self._pc] = [inst, 0]
        else:
            self._visited[self._pc][1] += 1

    def _is_function(self, addr):
        if self._pc not in self._stack: 
            return False
        
        if addr not in self._func_list: 
            self._queue.put((addr, deepcopy(self._stack)))
    
            self._func_list[addr] = {
                (len(self._stack) - self._stack.index(self._pc) - 1),
                self.FUNC_NOT_ANALYSED,
            }

        self._insert_entry_list_dict(
            self._blocks,
            addr,
            self._annotation_call()
        )
        self._insert_entry_list_dict(
            self._blocks,
            self._pc,
            self._annotation_return(addr)
        )

        if self._func_list[addr][1] == self.FUNC_NOT_ANALYSED:
            self._insert_entry_list_dict(
                self._deferred_analyis,
                addr,
                [
                    self._pc,
                 deepcopy(self._stack)[:-(self._func_list[addr][0] + 1)]
                ]
            )

        else:
            for i in range(self._func_list[addr][0] + 1):
                self._stack.pop()
                
            self._stack += self._get_func_ret_vals(addr)
            self._queue.put((self._pc, deepcopy(self._stack)))

        return True

    def _process_deferred(self, addr):
        for k, b in self._deferred_analysis.items():
            for ret, stack in b:
                if ret == addr:
                    # Get length of stack then subtract it
                    self._func_list[k][1] = \
                        len(self._stack) - len(stack)

                    if addr in self._stack:
                        self._func_list[k][1] -= 1

                    for e in b:
                        e[1] += self._get_func_ret_vals(k)
                        self._queue.put(e)

                    del self._deferred_analysis[k]
                    return True

            return False

    def _get_func_ret_vals(self, addr):
        return [
            'FUNC_{:04X}_{}'.format(addr, i)
            for i in range(self._func_list[addr][1])
        ]


    def _annotation_jump(self, addr, cond):
        return '// Incoming jump from 0x{:04X}'.format(addr),
        cond

    def _annotation_call(self):
        return (
            '// Incoming call from 0x{:04X}, returns to 0x{:04X}'.format(
            self._pc,
            self._pc - 1
        ),
        None
    )
   
    def _annotation_return(self, addr):
        return (
            '// Incoming return from call to 0x{:04X} at 0x{:04X}'.format(
                addr,
                self._pc - 1
            ),
            None
        )
    def disassemble(self):
        self._recursive_run()
        self.linear_run()
        return self._visited, self._blocks, self._func_list
    
    def _recursive_run(self):
        self._queue.put((0, []))
    
        # while queue is not empty do recursive traversal disassemble
        while not self._queue.empty():
            self.get_new_analysis_entry()

            while self._pc < len(self._data) and self._check_visited():
                cur_op = self._data[self._pc]
                if cur_op not in self._table:
                    self._mark_visited['INVALID']
                    break
                else:
                    inst = self._table[cur_op]
                    self._mark_visited(inst)
                    self._pc += 1
                if inst not in self.jump_ops:
                    self._stack_func(cur_op)

                    if inst in self._terminal_ops:
                        self._fin_addrs.append(self._pc)
                        break
                elif inst == "*JUMPI":
                    jump_addr, cond = self._jumpi()

                    if self._data[self._pc - 0xb] == 0x63 or \
                        self._data[self._pc - 0xa] == 0x63:
                            self._finc_list[jump_addr] = [0, 1]

                    self._insert_entry_list_dict(
                        self._blocks,
                        self._pc,
                        # might have to concatenate not into cond 
                        self._annotation_jump(self._pc - 1, "not" + str(cond))
                    )

                    if type(jump_addr) != int:
                        continue
                    
                    self._queue.put((jump_addr, deepcopy(self._stack)))
                    self._insert_entry_list_dict(
                        self._blocks,
                        jump_addr,
                        self._annotation_call(self._pc, - 1, cond)
                    )

                else:
                    jump_addr = self._jump()
                    if self._is_function(jump_addr):
                        break;

                    self._fin_addrs.append(self._pc)

                    if type(jump_addr) != int:
                        break;

                    if self._process_deferred(jump_addr):
                        break;

                    self._queue.put((jump_addr, deepcopy(self._stack)))
                    self._insert_entry_list_dict(
                        self._blocks,
                        jump_addr,
                        self._annotation_jump(self._pc - 1, None)
                    )
                    break;

    def _linear_run(self):
        # check for dead blocks
        for fin_addr in self._fin_addrs:
            if fin_addr not in self._visited:
                self._blocks[fin_addr] = [('// DEAD BL0CK', None)]

            self._pc = fin_addr
            while self._pc < len(self._data) and self._check_visited():
                cur_op =  self._data[self._pc]

                if cur_op not in self._table:
                    self._mark_visited['INVALID']
                    self._pc += 1
                    continue

                inst = self._table[self._data[self._pc]]
                self._mark_visited(inst)
                self._pc += 1

                if inst.startswith("PUSH"):
                    imm_width= int(width[4:])
                    imm_val = self._data[self._pc:self._pc
                            + imm_width].hex().str()

                    if len(self._visited[self._pc -1][0]) <= 6:
                        '0x{}'.format(imm_val)
                    self._pc += imm_width

    def _stack_pop(self):
        return self._stack.pop()

    def _stack_func(self, op):
        self._opcodes_func[op]()

    def _stop(self):
        return 0
        # sys.quit()
    
    def _add(self):
        operand_1 = self._stack_pop()
        operand_2 = self._stack_pop()
        if type(operand_1) == int:
            operand_1 = hex(operand_1)
        if type(operand_2) == int:
            operand_2 = hex(operand_2)

        self._stack.append('{} + {}'.format(operand_1, operand_2))
    
    def _mul(self):
        operand_1 = self._stack_pop()
        operand_2 = self._stack_pop()

        if type(operand_1) == int:
            operand_1 = hex(operand_1)

        if type(operand_2) == int:
             operand_2 = hex(operand_2)

        self._stack.append('{} * {}'.format(operand_1, operand_2))
    
    def _sub(self):
        operand_1 = self._stack_pop()
        operand_2 = self._stack_pop()

        if type(operand_1) == int:
            operand_1 = hex(operand_1)

        if type(operand_2) == int:
            operand_2 = hex(operand_2)
     
        self._stack.append('{} - {}'.format(operand_1, operand_2))

    def _div(self):
        operand_1 = self._stack_pop()
        operand_2 = self._stack_pop()

        if type(operand_1) == int:
            operand_1 = hex(operand_1)
      
        if type(operand_2) == int:
            operand_2 = hex(operand_2)
        
        self._stack.append('{} / {}'.format(operand_1, operand_2))

    def _sdiv(self):
        operand_1 = self._stack_pop()
        operand_2 = self._stack_pop()

        if type(operand_1) == int:
            operand_1 = hex(operand_1)
       
        if type(operand_2) == int:
            operand_2 = hex(operand_2)
        
        self._stack.append('{} / {}'.format(operand_1, operand_2))

    def _smod(self):
        operand_1 = self._stack_pop()
        operand_2 = self._stack_pop()

        if type(operand_1) == int:
            operand_1 = hex(operand_1)

        if type(operand_2) == int:
            operand_2 = hex(operand_2)
        
        self._stack.append('{} % {}'.format(operand_1, operand_2))

    def _smod(self):
        operand_1 = self._stack_pop()
        operand_2 = self._stack_pop()

        if type(operand_1) == int:
            operand_1 = hex(operand_1)

        if type(operand_2) == int:
            operand_2 = hex(operand_2)
        
        self._stack.append('{} % {}'.format(operand_1, operand_2))
    
    def _addmod(self):
        operand_1 = self._stack_pop()
        operand_2 = self._stack_pop()
        operand_3 = self._stack_pop()
        if type(operand_1) == int:
            operand_1 = hex(operand_1)
        if type(operand_2) == int:
            operand_2 = hex(operand_2)
        if type(operand_3) == int:
            operand_3 = hex(operand_3)
        
        # chad
        self._stack.append('({} + {}) % {}'.format(operand_1, operand_2, operand_3)) 
    
    def _mulmod(self):
        operand_1 = self._stack_pop()
        operand_2 = self._stack_pop()
        operand_3 = self._stack_pop()

        if type(operand_1) == int:
            operand_1 == hex(operand_1)

        if type(operand_2) == int:
            operand_2 = hex(operand_2)

        if type(operand_3) == int:
            operand_3 = hex(operand_3)

        self._stack.append('({} * {}) % {}'.format(operand_1, operand_2,
            operand_3))

    
    def _exp(self):
        operand_1 = self._stack_pop()
        operand_2 = self._stack_pop()

        if type(operand_1) == int:
            operand_1 = hex(operand_1)

        if type(operand_2) == int:
            operand_2 = hex(operand_2)

        self._stack.append('{} ** {}'.format(operand_1, operand_2))
    
    def _signextend(self):
        operand_1 = self._stack_pop()
        operand_2 = self._stack_pop()

        if type(operand_2) == int:
            operand_2 = hex(operand_2)

        self._stack.append('SIGNEXTEND({}, {})'.format(operand_1, operand_2))

    def _lt(self):
        operand_1 = self._stack_pop()
        operand_2 = self._stack.pop()

        if type(operand_1) == int:
            operand_1 = hex(operand_1)

        if type(operand_2) == int:
            operand_2 = hex(operand_2)

        self._stack.append("{} < {}".format(operand_1, operand_2))
                
    def _gt(self):
        operand_1 = self._stack_pop()
        operand_2 = self._stack_pop()
        if type(operand_1) == int:
            operand_1 = hex(operand_1)

        if type(operand_2) == int:
            operand_2 == hex(operand_2)

        self._stack.append('{} > {}'.format(operand_1, operand_2))

    def _slt(self):
        operand_1 = self._stack_pop()
        operand_2 = self._stack_pop()
        if type(operand_1) == int:
            operand_1 = hex(operand_1)

        if type(operand_2) == int:
            operand_2 = hex(operand_2)

        self._stack.append('{} < {}'.format(operand_1, operand_2))

    def _sgt(self):
        operand_1 = self._stack_pop()
        operand_2 = self._stack_pop()

        if type(operand_1) == int:
            operand_1 = hex(operand_1)

        if type(operand_2) == int:
            operand_2 = hex(operand_2)

        self._stack.append('{} > {}'.format(operand_1, operand_2))
    
    def _eq(self):
        operand_1 = self._stack_pop()
        operand_2 = self._stack_pop()

        if type(operand_1) == int:
            operand_1 = hex(operand_1)

        if type(operand_2) == int:
            operand_2 = hex(operand_2)

        self._stack.append('{} == {}'.format(operand_1, operand_2))

    def _iszero(self):
        operand_1 = self._stack_pop()
        
        if type(operand_1) == int:
            operand_1 == hex(operand_1)

        self._stack.append("{} == 0".format(operand_1))

    def _evm_and(self):
        operand_1 = self._stack_pop()
        operand_2 = self._stack_pop()

        if type(operand_1) == int:
            operand_1 = hex(operand_1)
        if type(operand_2) == int:
            operand_2 = hex(operand_2)
        
        self._stack.append("{} & {}".format(operand_1, operand_2))
    
    def _evm_or(self):
        operand_1 = self._stack_pop()
        operand_2 = self._stack_pop()

        if type(operand_1) == int:
            operand_1 = hex(operand_1)
        
        if type(operand_2) == int:
            operand_2 = hex(operand_2)
    
        self._stack.append("{} | {}".format(operand_1, operand_2))
    
    def _xor(self):
        operand_1 = self._stack_pop()
        operand_2 = self._stack_pop()

        if type(operand_1) == int:
            operand_1 = hex(operand_1)
        
        if type(operand_2) == int:
            operand_2 = hex(operand_2)
        
        self._stack.append("{} ^ {}".format(operand_1, operand_2))
    
    def _evm_not(self):
        operand_1 = self._stack_pop()

        if type(operand_1) == int:
            operand_1 = hex(operand_1)
        
        self._stack.append("~{}".format(operand_1))

    def _byte(self):
        operand_1 = self._stack_pop()
        operand_2 = self._stack_pop()

        if type(operand_2) == int:
            operand_2 = hex(operand_2)
        
        self._stack.append("({} >> (248 - {} * 8)) & 0xFF".format(operand_1, operand_2))
    
    def _shl(self):
        operand_1 = self._stack_pop()
        operand_2 = self._stack_pop()

        if type(operand_2) == int:
            operand_2 = hex(operand_2)

        self._stack.append("{} << {}".format(operand_2, operand_1))
    
    def _shr(self):
        operand_1 = self._stack_pop()
        operand_2 = self._stack_pop()

        if type(operand_2) == int:
            operand_2 = hex(operand_2)
        
        self._stack.append("{} >> {}".format(operand_2, operand_1))
    
    def _sar(self):
        # pass
        operand_1 = self._stack_pop()
        operand_2 = self._stack_pop()
        # do we need 3 operands?
        operand_3 = self._stack_pop()

        if type(operand_2) == int:
            operand_2 = hex(operand_2)

        if type(operand_3) == int:
            operand_3 = hex(operand_3)

        self._stack.append("{} >> {}".format(operand_2, operand_3, operand_1))

    def _sha3(self):
        operand_1 = self._stack_pop()
        operand_2 = self._stack_pop()

        if type(operand_1) == int and type(operand_2) == int:
            operand_2 = hex(operand_1 + operand_2)
            operand_1 = hex(operand_1)

        elif type(operand_1) == int:
            operand_1 = hex(operand_1)
            operand_2 = operand_1 + " + " + operand_2

        elif type(operand_2) == int:
            operand_2 = operand_1 + " + " + hex(operand_2)
        
        else:
            pass 
            
        self._stack.append("hash(memory[{}:{}])".format(operand_1, operand_2))
    
    def _address(self):
        self._stack.append("address(\n' T: \n')")
    
    def _balance(self):
        operand_1 = self._stack_pop()

        if type(operand_1) == int:
            operand_1 = hex(operand_1)
        
        self._stack.append('address(' + operand_1 + ').balance')

    def _origin(self):
        self._stack.append("tx.origin")
    
    def _caller_(self):
        self._stack.append("msg.caller")
    
    def _callvalue(self):
        self._stack.append("msg.value")
    
    def _calldataload(self):
        operand_1 = self._stack_pop()

        if type(operand_1) == int:
            operand_2 = hex(operand_1 + 0x30) # or 0x20
            operand_1 = hex(operand_1)
        else:
            operand_2 = operand_1 + " + 0x30"
        
        self._stack.append("msg.data[{}:{}]".format(operand_1, operand_2))
    
    def _calldatasize(self):
        self._stack.append("msg.data.size")
    
    def _calldatacopy(self):
        for _ in range(3):
            self._stack_pop()
    
    def _codesize(self):
        self._stack.append("address(this).code.size")
    
    def _codecopy(self):
        for _ in range(3):
            self._stack_pop()
    
    def _gasprice(self):
        self._stack.append("tx.gasprice")
    
    def _extcodesize(self):
        operand_1 = self._stack_pop()
        if type(operand_1) == int:
            operand_1 = hex(operand_1)
        
        self._stack.append("address({}).code.size".format(operand_1))

    def _extcodecopy(self):
        for _ in range(4):
            self._stack_pop()
    
    def _returndatasize(self):
        self._stack.append("RETURNDATA_SIZE()")
    
    def _returndatacopy(self):
        for _ in range(3):
            self._stack_pop()
    
    def _extcodehash(self):
        operand_1 = self._stack_pop()
        
        if type(operand_1) == int:
            operand_1 = hex(operand_1)

        self._stack.append("extcodehash(}".format(operand_1))
    
    def _blockhash(self):
        operand_1 = self._stack_pop()
        if type(operand_1) == int:
            operand_1 = hex(operand_1)

        self._stack.append('block.blockHash({})'.format(operand_1))
    
    # could be renamed to coinbase!???
    def _coin(self):
        self._stack.append("block.coin")

    def _timestamp(self):
        self._stack.append("block.timestamp")

    def _number(self):
        self._stack.append("block.number")

    def _difficulty(self):
        self._stack.append("block.difficulty")

    def _gaslimit(self):
        self._stack.append("block.gaslimit")

    def _balance(self):
        self._stack.append("block.balance")
    
    def _address(self):
        self._stack.append("block.address")

    def _pop(self):
        self._stack_pop()

    def _mload():
        operand_1 = self._stack_pop()
        if type(operand_1) == int:
            operand_2 = hex(operand_1 + 0x20)
            operand_1 = hex(operand_1)

        #elif:
            #operand_2 = operand_1 + ' + 0x20'

        else:
            operand_2 == operand_1 + " + 0x20"

print("**PASSED*")
