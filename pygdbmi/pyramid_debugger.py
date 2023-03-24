import os
import tempfile
from pygdbmi.gdbcontroller import GdbController

def main():
    # Initialize GDB
    gdb = GdbController()

    # Load the executable
    gdb.write('-file-exec-and-symbols pyramid')

    # Start the program
    gdb.write("-break-insert main")
    gdb.write('-exec-run')
    

    while True:
        # Execute one step
        response = gdb.write('-exec-next')[0]
        print(response)

        if 'reason' in response and response['reason'] in ['exited', 'exited-normally', 'signal-received']:
            print("Program finished.")
            break

        # Print local variables
        locals_response = gdb.write('-stack-list-locals 0')[0]['payload']
        if 'locals' in locals_response:
            locals_data = locals_response['locals']

            print("Local variables at step:")
            for local in locals_data:
                print(f"{local['name']} = {local['value']}")

    # Exit GDB
    gdb.exit()

if __name__ == '__main__':
    main()