from pygdbmi.gdbcontroller import GdbController
from pprint import pprint

# Start gdb process
gdbmi = GdbController()
print(gdbmi.command)  # print actual command run as subprocess
# Load binary a.out and get structured response
response = gdbmi.write('-file-exec-file a.out')
pprint(response)
# Prints:
# [{'message': 'thread-group-added',
#   'payload': {'id': 'i1'},
#   'stream': 'stdout',
#   'token': None,
#   'type': 'notify'},
#  {'message': 'done',
#   'payload': None,
#   'stream': 'stdout',
#   'token': None,
#   'type': 'result'}]