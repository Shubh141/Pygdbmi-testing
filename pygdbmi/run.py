from pygdbmi.gdbcontroller import GdbController
from pygdbmi import gdbmiparser
from pprint import pprint

gdbmi = GdbController()
#print(gdbmi.get_subprocess_cmd())

gdbmi.write("-file-exec-and-symbols basic")
gdbmi.write("-break-insert main")
gdbmi.write("-break-insert 17")
response = gdbmi.write("-break-list")
pprint(response)
print("---")
response = gdbmi.write("-exec-run")
pprint(response)
print("---")
response = gdbmi.write("-exec-continue")
pprint(response)
print("---")
response = gdbmi.write("-stack-list-variables --all-values")
pprint(response)
print("---")