import os
import sys
import datetime
import random
import time
from cmd import Cmd

version = "DevTest 0.0.1"

def show_bsod(error_code="0x00000001"):
    """Function for showing blue screen of death (BSOD)"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n"*5)
    print(" "*20 + "="*60)
    print(" "*20 + "|" + " "*58 + "|")
    print(" "*20 + f"|{'CR1T1C4L 3RR0R!':^58}|")
    print(" "*20 + "|" + " "*58 + "|")
    print(" "*20 + f"|{'Test0S experienced a pr0blem and will be restarted s00n':^58}|")
    print(" "*20 + "|" + " "*58 + "|")
    print(" "*20 + f"| Error code:: {error_code:<45} |")
    print(" "*20 + "|" + " "*58 + "|")
    print(" "*20 + "| Collect information about this error:            |")
    print(" "*20 + "| Failed to perform an operation                  |")
    print(" "*20 + "|" + " "*58 + "|")
    print(" "*20 + "| Press any key to continue...        |")
    print(" "*20 + "|" + " "*58 + "|")
    print(" "*20 + "="*60)
    print("\n"*5)
    input()
    # "Reloading" the system
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n"*3)
    print(" "*30 + "="*20)
    print(" "*30 + "|" + " "*18 + "|")
    print(" "*30 + f"|{'Loading...':^18}|")
    print(" "*30 + "|" + " "*18 + "|")
    print(" "*30 + "="*20)
    print("\n"*3)
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')

class TestOS(Cmd):
    intro = """
GercogRybron(R) TestOS(R) Version %s
(C)Timofey Yakubov 2025 - Our time.
Type HELP for list of commands.\n
"""%(version)
    
    def __init__(self):
        super().__init__()
        self.current_dir = "C:\\"
        self.update_prompt()
        self.fs = {
            "C:\\": {
                "dirs": ["DOS", "WINDOWS", "TEMP"],
                "files": {
                    "AUTOEXEC.BAT": 256,
                    "CONFIG.SYS": 128,
                    "COMMAND.COM": 94784
                }
            },
            "C:\\DOS\\": {
                "dirs": [],
                "files": {
                    "EDIT.COM": 41312,
                    "FORMAT.COM": 32911,
                    "FDISK.EXE": 64216,
                    "MEM.EXE": 39848
                }
            },
            "C:\\WINDOWS\\": {
                "dirs": ["SYSTEM"],
                "files": {
                    "WIN.COM": 102912,
                    "SYSTEM.INI": 2048,
                    "WIN.INI": 1024
                }
            },
            "C:\\TEMP\\": {
                "dirs": [],
                "files": {}
            },
            "C:\\WINDOWS\\SYSTEM\\": {
                "dirs": [],
                "files": {
                    "KERNEL.DLL": 456320,
                    "USER.EXE": 389120
                }
            }
        }
    
    def update_prompt(self):
        self.prompt = f"{self.current_dir}>"
    
    def emptyline(self):
        pass
    
    def precmd(self, line):
        # Random BSOD for demonstration
        if random.random() < 0.05:  # 5% chance for BSOD
            show_bsod("0x0000007B")
            return ""
        return line.upper()
    
    def do_BSOD(self, arg):
        """Imitate a BSOD for testing"""
        show_bsod("0x000000ED")
    
    def do_VER(self, arg):
        print("\nTestOS version %s.\n"%(version))
    
    def do_CLS(self, arg):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def do_DIR(self, arg):
        path = os.path.join(self.current_dir, arg) if arg else self.current_dir
        path = path.replace("/", "\\")
        
        if not path.endswith("\\"):
            path += "\\"
        
        if path not in self.fs:
            show_bsod("0x00000024")
            return
        
        print(f"\n Contents: {path}\n")
        print(f"{'Name':<12} {'Type':<8} {'Size':>10} {'Date':>12}")
        print("-" * 45)
        
        for dir_name in self.fs[path]["dirs"]:
            print(f"{dir_name:<12} {'<DIR>':<8} {'':>10} {datetime.date.today().strftime('%d-%m-%y'):>12}")
        
        for file_name, size in self.fs[path]["files"].items():
            print(f"{file_name:<12} {'File':<8} {size:>10} {datetime.date.today().strftime('%d-%m-%y'):>12}")
        
        total_files = len(self.fs[path]["files"])
        total_dirs = len(self.fs[path]["dirs"])
        print(f"\n Total files: {total_files}\n Total dirs: {total_dirs}\n")
    
    def do_CD(self, arg):
        if not arg:
            print(f"\n Current dir: {self.current_dir}\n")
            return
        
        new_path = os.path.join(self.current_dir, arg)
        new_path = new_path.replace("/", "\\")
        
        if arg == "\\":
            new_path = "C:\\"
        elif arg == "..":
            if self.current_dir == "C:\\":
                print("\nAlready in head dir\n")
                return
            parts = self.current_dir.split("\\")
            new_path = "\\".join(parts[:-2]) + "\\"
        
        if not new_path.endswith("\\"):
            new_path += "\\"
        
        if new_path in self.fs:
            self.current_dir = new_path
            self.update_prompt()
        else:
            show_bsod("0x00000003")
    
    def do_MD(self, arg):
        if not arg:
            show_bsod("0x0000001E")
            return
        
        new_dir = os.path.join(self.current_dir, arg)
        new_dir = new_dir.replace("/", "\\")
        
        if not new_dir.endswith("\\"):
            new_dir += "\\"
        
        if new_dir in self.fs:
            print("\nDirectory already exists\n")
        else:
            self.fs[self.current_dir]["dirs"].append(arg)
            self.fs[new_dir] = {"dirs": [], "files": {}}
            print(f"\nDirectory created: {new_dir}\n")
    
    def do_RD(self, arg):
        if not arg:
            show_bsod("0x0000002A")
            return
        
        target_dir = os.path.join(self.current_dir, arg)
        target_dir = target_dir.replace("/", "\\")
        
        if not target_dir.endswith("\\"):
            target_dir += "\\"
        
        if target_dir not in self.fs:
            show_bsod("0x0000002B")
        elif self.fs[target_dir]["dirs"] or self.fs[target_dir]["files"]:
            print("\nDirectory not empty!\n")
        else:
            self.fs[self.current_dir]["dirs"].remove(arg)
            del self.fs[target_dir]
            print(f"\nDirectory deleted: {target_dir}\n")
    
    def do_COPY(self, arg):
        if not arg:
            show_bsod("0x00000021")
            return
        
        args = arg.split()
        if len(args) < 2:
            show_bsod("0x0000007A")
            return
        
        src = os.path.join(self.current_dir, args[0])
        dst = os.path.join(self.current_dir, args[1])
        
        src_found = False
        for path in self.fs:
            if args[0] in self.fs[path]["files"]:
                src_found = True
                src_path = path
                break
        
        if not src_found:
            show_bsod("0x0000007B")
            return
        
        dst_dir = os.path.dirname(dst)
        if not dst_dir.endswith("\\"):
            dst_dir += "\\"
        
        if dst_dir not in self.fs:
            show_bsod("0x0000007C")
            return
        
        dst_file = os.path.basename(dst) if "." in os.path.basename(dst) else args[0]
        self.fs[dst_dir]["files"][dst_file] = self.fs[src_path]["files"][args[0]]
        print("\n1 file(s) copied\n")
    
    def do_DEL(self, arg):
        if not arg:
            show_bsod("0x00000026")
            return
        
        deleted = False
        for path in self.fs:
            if arg in self.fs[path]["files"]:
                del self.fs[path]["files"][arg]
                deleted = True
                break
        
        if deleted:
            print(f"\nFile deleted: {arg}\n")
        else:
            show_bsod("0x00000027")
    
    def do_TIME(self, arg):
        now = datetime.datetime.now()
        print(f"\nCurrent time: {now.strftime('%H:%M:%S')}")
        print("Enter new time (HH:MM:SS): ", end="")
        try:
            new_time = input()
            if new_time:
                print("\nTime set (emulation)\n")
        except:
            pass
    
    def do_DATE(self, arg):
        now = datetime.datetime.now()
        print(f"\nCurrent date: {now.strftime('%d-%m-%Y')}")
        print("Enter new date: (DD-MM-YYYY): ", end="")
        try:
            new_date = input()
            if new_date:
                print("\nDate set! (emulation)\n")
        except:
            pass
    
    def do_HELP(self, arg):
        commands = {
            "VER": "Show the TestOS version",
            "CLS": "Clear the screen",
            "DIR": "Show the contents of directory",
            "CD": "Change current directory",
            "MD": "Create directory",
            "RD": "Remove directory",
            "COPY": "Copy file",
            "DEL": "Remove file",
            "TIME": "Show/set the time",
            "DATE": "Show/set the date",
            "HELP": "Show this hint",
            "EXIT": "Leave the emulator",
            "BSOD": "Imitate BSOD (test)"
        }
        
        if not arg:
            print("\nAvailable commands:\n")
            for cmd, desc in commands.items():
                print(f"{cmd:8} - {desc}")
            print("\nFor more info, type HELP Command_name\n")
        else:
            cmd = arg.upper()
            if cmd in commands:
                print(f"\n{cmd} - {commands[cmd]}\n")
            else:
                print("\nCommand not found!\n")
    
    def do_EXIT(self, arg):
        print("\nThank you for using TestOS version %s\n"%(version))
        return True

    do_QUIT = do_EXIT
    
if __name__ == "__main__":
    try:
        TestOS().cmdloop()
    except KeyboardInterrupt:
        print("\n^C\n")
        sys.exit(0)
