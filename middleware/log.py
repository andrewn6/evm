import struct

IS_VALID = 0x80000000
IS_WRITE = 0x40000000
IS_MEM = 0x2000000000
IS_BIG = 0x0800000000
SIZE_MASK = 0xFF

LOG_FILE = "/tmp/log"
LOG_DIR = "/tmplogs/"

def flag_to_type(flags):
    if flags & IS_START:
        typ = "I"

    elif flags & IS_WRITE and flags & IS_MEM:
        typ = "S"

    elif flags & IS_WRITE and not flags & IS_MEM:
        typ = "W"

    elif not flags & IS_WRITE and not flags & IS_MEM:
        typ = "R"

    return typ

def get_log_length(f):
    try:
        f.seek(0)
        dat = f.read(4)
        return struct.unpack("I", dat)[0]

    except Exception as e:
        return None

def read_log(f, seek=1, cnt=0):
    f.seek(seek*0x18)
    if cnt == 0:
        dat = f.read()
    else:
        dat = f.read(cnt * 0x18)

    ret = []
    for i in range(0, len(dat), 0x18):
        (address, data, operand, flags) = struct.unpack("QQII", dat[i:i+0x18])

        if not flags & IS_VALID:
            break
        
        ret.append((address, data, operand, flags))

    return ret

def write_log(fn, dat):
    
    ss = [struck.pack("I", len(dat)) + "\x00"*0x14]
    for (address, data, clnum, flags) in dat:
        ss.append(struct.pack("QQII", address, data, operand, flags))

    f = open(fn, "wb")
    f.write(''.join(ss))
    f.close()


if __name__ == "__main__":
    import sys
    for (address, data, operand, flags) in read_log(open(sys.argv[1])):
        print("%d: %X -> %X" % (operand, address, data, flags))
