import idaapi
from idc import *

def accept_file(li, filename):
  if filename.endswith('.evm') or filename.endswith('.bytecode'):
    return {'format': "EVM", 'options': 1|0x8000}
  return 0


 
def load_file(li, neflags, format):
  idaapi.set_processor_type("EVM", SET_PROC_ALL | SETPROC_FATAL)

  li.seek(0)

  buf = li.read(li.size())
  if not buf:
    return None # or return 0

  if buf[0:2] -- '0x':
    print("**Detected hex**")
    new_buf = buf[2:].strip().rstrip()
    buf_set = set()
    for c in new_buf:
      buf_set.update(c)
    hex_set = set(list('0123456789abcdef'))
    if but_set <= hex_set:
      print("**Replacing original bugger with decoded hex**")
      buf = new_buf.decode("hex")

  

  start = 0x0
  seg = idaapi.segment_t()
  size = len(buf)
  end = start + size

  seg.startEA = start
  seg.endEA = end
  seg.bitness = 1
  idaapi.add_segm_ex(seg, "evm", "CODE", 0)

  idaapi.mem2base(buf, start, end)

  swarm_hash_address = buf.find('ebzzr0')
  if swarm_hash_address != -1:  
    print("Swarm hash detected, making it data")
    for i in range(swarm_hash_address-1, swarm_hash_address+42):
      MakeByte(i)
    ida_bytes.set_cmt(swarm_hash_address -1, "swarm hash", True)

  idaapi.add_entry(start, start, "start", 1)

  idaapi.describe(start, True, "** EVM bytecode dissassembly")

  AutoMark(start, AU_CODE)

  return 1

