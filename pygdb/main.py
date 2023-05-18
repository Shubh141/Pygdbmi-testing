import subprocess
import argparse
from pygdbmi.gdbcontroller import GdbController

COMMAND_TIMEOUT_SEC = 0.1


def main():
    """
    Main function
    """
    args = parse_args()
    compile_code(args.files)
    debug_code(args.breakpoints)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Runs GDB on C code and prints stack locals and frames"
    )
    parser.add_argument("files", nargs="+", help="the filename(s) of C code")
    parser.add_argument(
        "-b",
        "--breakpoints",
        default=[],
        nargs="*",
        help="the breakpoints (lines or functions) to be placed for debugging",
    )
    return parser.parse_args()


def compile_code(files):
    """
    Compiles code_file into executable
    Note: -ggdb option produces debugging information for use by GDB
    """
    subprocess.run(["gcc", "-ggdb", *files])


def debug_code(breakpoints):
    """
    Run GDB on the compiled executable
    Print out all stack args and locals at each frame where breakpoint is added
    """
    gdbmi = GdbController()

    gdbmi.write("-file-exec-and-symbols a.out")
    gdbmi.write("-break-insert main")
    for breakpoint in breakpoints:
        gdbmi.write(f"-break-insert {breakpoint}")
    gdbmi.write("-exec-run")

    # Continue executing GDB commands until execution ends
    while True:
        response = gdbmi.write("-exec-next", timeout_sec=COMMAND_TIMEOUT_SEC)[-1]["payload"]

        if "reason" in response and response["reason"] in [
            "exited",
            "exited-normally",
            "exited-signalled",
        ]:
            break

        frame_info = response["frame"]

        # Get the address of the linked list head
        gdbmi.write("-stack-select-frame 0")
        linked_list_head_addr = gdbmi.write(
            "-print &head", timeout_sec=COMMAND_TIMEOUT_SEC
        )[0].get("payload", {}).get("value")

        if linked_list_head_addr is not None:
            print(f"Memory address of the head: {linked_list_head_addr}")

            # Print the value stored at the head
            linked_list_head_value = gdbmi.write(
                f"-print *head",
                timeout_sec=COMMAND_TIMEOUT_SEC,
            )[0].get("payload", {}).get("value")
            if linked_list_head_value is not None:
                print(f"Value stored at the head: {linked_list_head_value}")

            # Iterate through the linked list
            node = linked_list_head_value
            while node:
                node_address = gdbmi.write(f"-print (void*){node}", timeout_sec=COMMAND_TIMEOUT_SEC)[-1]["payload"]["value"]
                node_value = gdbmi.write(f"-print *(int*){node}->data", timeout_sec=COMMAND_TIMEOUT_SEC)[-1]["payload"]["value"]
                if node_address is not None and node_value is not None:
                    print(f"Node at address {node_address}: data = {node_value}")

                # Move to the next node
                node = gdbmi.write(f"-print (void*){node}->next", timeout_sec=COMMAND_TIMEOUT_SEC)[-1]["payload"]["value"]

        print(f"In function {frame_info.get('func', '')}, {frame_info.get('file', '')}:{frame_info.get('line', '')}")


if __name__ == "__main__":
    main
