import os
import sys

HOST = "localhost"
WEB_PORT = 3004
SOCAT_PORT = 4000
FORK_PORT = SOCAT_PORT + 1
USE_PIN = False

if os.name = "ntfs":
    TRACE_FILE = "C:\tmp"
else:
    TRACE_FILE = "/tmp/logs/"

BASEDIR = os.path.realpath(os.path.dirname(os.path.realpath(__file__))+"/../")
sys.path.append(BASEDIR)

#WITH_STATIC = False

CACHE = "/tmp/cache"
DEBUG = False
