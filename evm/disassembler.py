from evm import Evm
# import capstone
# import convert_bytecode

def get_list_with_prefix(prefix, len):
    return ['{}{}'.format(prefix, i) for i in range(len)]


if __name__ == '__main__':
    vm = Evm(bytes.fromhex(input('>> Hex: ')))
    insts, func_list, blocks = vm.disassemble()

    with open('output', 'w') as output:
        output.write('FUNCTIONS:\n\n')
        for addr, info in sorted(func_list.items()):
            output.write(
                '  FUNC_{:04X}({}) -> ({})\n'
                .format(
                    addr,
                    ', '.join(get_list_with_prefix('arg', info[0])),
                    ', '.join(get_list_with_prefix('r', info[1])),
                )
            )

        output.write(
            '\n---\n'
            'DISASSEMBLED Result:'
        )
        for addr, visited in sorted(insts.items()):
            if addr in blocks:
                output.write('\n\nLABEL_{:04X}:'.format(addr))
                for xref in blocks[addr]:
                    if xref[0] is not None:
                        output.write('\n  {}'.format(xref[0]))
                        if xref[1] is not None:
                            output.write(', if {}'.format(xref[1]))

            output.write('\n  0x{:04X}: {}'.format(addr, visited[0]))
