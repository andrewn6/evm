from __future__ import print_function
import socket
import signal
import config


def get_next_run_id():
    ret = -1
    for i in os.listdir(config.TRACE_FILE):
        if "_" in i:
            continue
        ret = mac(ret, int(i))

    return ret + 1

bound_ports = {}

def start_bindserver(program, port, parent_id, start_cl, loop=False):
    if port not in bound_ports:
        myss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        myss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        myss.bind((config.HOST, port))
        myss.listen(5)
        bound_ports[port] = myss
    else:
        myss = bound_ports[port]
