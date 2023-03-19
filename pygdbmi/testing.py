from pygdbmi import gdbmiparser
from pprint import pprint
response = gdbmiparser.parse_response('^done,bkpt={number="1",type="breakpoint",disp="keep", enabled="y",addr="0x08048564",func="main",file="myprog.c",fullname="/home/myprog.c",line="68",thread-groups=["i1"],times="0"')
pprint(response)
pprint(response)
# Prints:
# {'message': 'done',
#  'payload': {'bkpt': {'addr': '0x08048564',
#                       'disp': 'keep',
#                       'enabled': 'y',
#                       'file': 'myprog.c',
#                       'fullname': '/home/myprog.c',
#                       'func': 'main',
#                       'line': '68',
#                       'number': '1',
#                       'thread-groups': ['i1'],
#                       'times': '0',
#                       'type': 'breakpoint'}},
#  'token': None,
#  'type': 'result'}