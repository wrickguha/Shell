import sys
import os
import shutil
import platform
import subprocess
import argparse


def change_directory(path):
    try:
        if path == "":
            path = os.path.expanduser("~")
        os.chdir(path)
    except FileNotFoundError:
        print(f"cd: {path}: No such file or directory")
    except PermissionError:
        print(f"cd: {path}: Permission denied")
    except Exception as e:
        print(f"cd: {path}: {e}")


def list_files():
    for file in os.listdir():
        print(file)


def pwd():
    print(os.getcwd())


def copy_file(src, dest):
    try:
        shutil.copy(src, dest)
        print(f"Copied {src} to {dest}")
    except FileNotFoundError:
        print(f"cp: {src}: No such file or directory")
    except PermissionError:
        print(f"cp: {src}: Permission denied")


def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"Deleted {file_path}")
    except FileNotFoundError:
        print(f"rm: {file_path}: No such file or directory")
    except PermissionError:
        print(f"rm: {file_path}: Permission denied")


def make_directory(directory_name):
    try:
        os.mkdir(directory_name)
    except PermissionError:
        print(f"mkdir: cannot create directory '{directory_name}': Permission Denied")
    except FileExistsError:
        print(f"mkdir: cannot create directory '{directory_name}': File exists")
    except FileNotFoundError:
        print(f"mkdir: cannot create directory '{directory_name}': No such file or directory")


def remove_directory(directory_name):
    try:
        os.rmdir(directory_name)
    except PermissionError:
        print(f"rmdir: cannot remove directory '{directory_name}': Permission Denied")
    except FileNotFoundError:
        print(f"rmdir: cannot remove directory '{directory_name}': No such file or directory")


def remove_file(files):
    for file in files:
        if os.path.isfile(file):
            os.remove(file)
        else:
            print(f"rm: cannot remove '{file}': No such file or directory")


def touch_file(file_name):
    try:
        with open(file_name, "a"):
            os.utime(file_name, None)
    except PermissionError:
        print(f"touch: cannot touch '{file_name}': Permission denied")
    except Exception as e:
        print(f"touch: {e}")


def uname_command(options):
    system = platform.system()
    node = platform.node()
    release = platform.release()
    version = platform.version()
    machine = platform.machine()
    processor = platform.processor()

    output = []

    if options.all or options.kernel_name:
        output.append(system)
    if options.all or options.nodename:
        output.append(node)
    if options.all or options.kernel_release:
        output.append(release)
    if options.all or options.kernel_version:
        output.append(version)
    if options.all or options.machine:
        output.append(machine)
    if options.all or options.processor:
        output.append(processor)

    print(" ".join(output))


def locate_file(pattern):
    try:
        result = subprocess.run(["locate", pattern], capture_output=True, text=True)
        print(result.stdout)
    except FileNotFoundError:
        print("locate: command not found (install 'mlocate' or 'locate' package)")


def create_link(source, link_name):
    try:
        os.symlink(source, link_name)
        print(f"Created symlink '{link_name}' -> '{source}'")
    except FileExistsError:
        print(f"ln: cannot create link '{link_name}': File exists")
    except PermissionError:
        print(f"ln: cannot create link '{link_name}': Permission denied")
    except Exception as e:
        print(f"ln: {e}")


def cat_file(file_name):
    try:
        with open(file_name, "r") as file:
            print(file.read())
    except FileNotFoundError:
        print(f"cat: {file_name}: No such file or directory")
    except PermissionError:
        print(f"cat: {file_name}: Permission denied")
    except Exception as e:
        print(f"cat: {e}")


def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input().strip()
        parts = command.split()
        if not parts:
            continue
        cmd = parts[0]

        if cmd == "exit":
            if len(parts) > 1 and parts[1].isdigit():
                sys.exit(int(parts[1]))
            else:
                print("Exiting MyShell...")
                sys.exit()

        elif cmd.startswith("echo"):
            sys.stdout.write(" ".join(parts[1:]) + "\n")

        elif cmd == "ls":
            list_files()

        elif cmd == "pwd":
            pwd()

        elif cmd == "cp":
            if len(parts) < 3:
                print("cp: missing arguments (usage: cp source destination)")
            else:
                copy_file(parts[1], parts[2])

        elif cmd == "rm":
            if len(parts) < 2:
                print("rm: missing argument (usage: rm filename)")
            else:
                delete_file(parts[1])

        elif cmd == "mkdir":
            if len(parts) > 1:
                make_directory(parts[1])
            else:
                print("mkdir: missing argument (usage: mkdir directory_name)")

        elif cmd == "type":
            for i in parts[1:]:
                if i in ["echo", "exit", "type", "ls", "pwd", "cp", "rm", "mkdir", "cd", "rmdir", "touch", "uname", "locate", "ln", "cat", "clear"]:
                    print(f"{i} is a shell builtin")
                else:
                    print(f"{i}: not found")

        elif cmd == "cd":
            if len(parts) > 1:
                change_directory(parts[1])
            else:
                change_directory("")

        elif cmd == "rmdir":
            if len(parts) < 2:
                print("rmdir: missing argument")
            else:
                remove_directory(parts[1])

        elif cmd == "touch":
            if len(parts) < 2:
                print("touch: missing argument (usage: touch filename)")
            else:
                touch_file(parts[1])

        elif cmd == "uname":
            parser = argparse.ArgumentParser(description="Python implementation of the uname command.")
            parser.add_argument("-a", "--all", action="store_true", help="print all information")
            parser.add_argument("-s", "--kernel-name", action="store_true", help="print the kernel name")
            parser.add_argument("-n", "--nodename", action="store_true", help="print the network node hostname")
            parser.add_argument("-r", "--kernel-release", action="store_true", help="print the kernel release")
            parser.add_argument("-v", "--kernel-version", action="store_true", help="print the kernel version")
            parser.add_argument("-m", "--machine", action="store_true", help="print the machine hardware name")
            parser.add_argument("-p", "--processor", action="store_true", help="print the processor type")
            args = parser.parse_args(parts[1:])
            uname_command(args)

        elif cmd == "locate":
            if len(parts) < 2:
                print("locate: missing argument (usage: locate pattern)")
            else:
                locate_file(parts[1])

        elif cmd == "ln":
            if len(parts) < 3:
                print("ln: missing arguments (usage: ln source link_name)")
            else:
                create_link(parts[1], parts[2])

        elif cmd == "cat":
            if len(parts) < 2:
                print("cat: missing argument (usage: cat filename)")
            else:
                cat_file(parts[1])

        elif cmd == "clear":
            clear_screen()

        else:
            print(f"{cmd}: command not found")


if __name__ == "__main__":
    main()