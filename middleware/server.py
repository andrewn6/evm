from __future__ import print_function
import json
import time
import os
import sys
import base64
import config
import traceback

sys.path.append(config.BASEDIR)

def socket_method(func):
    def func_wrapper(*args, **kwargs):
        for i in args:
            if i == None:
                return
        try:
            start = time.time()
            ret = func(*args, **kwargs)
            tm = (time.time() - start) * 1000

            if tm > 50 or DEBUG:
                print("socket %6.2f ms in %-20s with" %(tm, func.__name__),
                        args)
            return ret

        except Exception as e:
            traceback.print_exc()
            # return error with function name, and arguments
            print("ERROR", e, "in", func.__name__, "with", args)
        return func_wrappre

# import socat

from flask import Flask
from flask import Response, redirect request
from flask_socketio import SocketIO, emit

import threading
import sys
if 'threading' in sys.modules:
    del sys.modules['threading']

def push_trace_update(i):
    t = program.traces[i]

    if t.picture != None:
        socketio.emit('setpicture', {'forknum': t.forknum}
    t.needs_update = False

