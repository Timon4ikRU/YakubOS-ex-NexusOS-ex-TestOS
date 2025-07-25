import os
import sys
import datetime
import random
import time
from cmd import Cmd

version = "DevTest 0.0.2"

def is_idle():
    """Проверяем, запущен ли код в IDLE"""
    return 'idlelib.run' in sys.modules

def show_bsod(error_code="0x00000001"):
    """Функция для отображения синего экрана смерти (BSOD)"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n"*5)
    print(" "*20 + "="*60)
    print(" "*20 + "|" + " "*58 + "|")
    print(" "*20 + f"|{'ПРОИЗОШЛА КРИТИЧЕСКАЯ ОШИБКА':^58}|")
    print(" "*20 + "|" + " "*58 + "|")
    print(" "*20 + f"|{'TestOS обнаружила проблему и будет перезагружена':^58}|")
    print(" "*20 + "|" + " "*58 + "|")
    print(" "*20 + f"| Код ошибки: {error_code:<45}|")
    print(" "*20 + "|" + " "*58 + "|")
    print(" "*20 + "| Нажмите любую клавишу для перезагрузки...          |")
    print(" "*20 + "|" + " "*58 + "|")
    print(" "*20 + "="*60)
    print("\n"*5)
    input()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\nПерезагрузка...\n")
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')

class TestOS(Cmd):
    intro = f"""
GercogRybron(R) TestOS(R) Версия {version}
(C)Тимофей Якубов 2025 - Наше время.
Введите HELP для списка команд.

Новые возможности:
- Калькулятор (CALC)
- Крестики-нолики (TICTACTOE)
\n"""
    
    def __init__(self):
        super().__init__()
        self.current_dir = "C:\\"
        self.update_prompt()
        self.fs = {
            "C:\\": {
                "dirs": ["DOS", "WINDOWS", "TEMP", "GAMES"],
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
            },
            "C:\\GAMES\\": {
                "dirs": [],
                "files": {
                    "TICTACTOE.EXE": 10240,
                    "CALC.EXE": 8192
                }
            }
        }
        self.tictactoe_board = None
        self.tictactoe_turn = 'X'
    
    def update_prompt(self):
        self.prompt = f"{self.current_dir}>"
    
    def emptyline(self):
        pass
    
    def precmd(self, line):
        if random.random() < 0.05:
            show_bsod("0x0000007B")
            return ""
        return line.upper()
    
    def do_BSOD(self, arg):
        """Имитировать синий экран смерти"""
        show_bsod("0x000000ED")
    
    def do_VER(self, arg):
        """Показать версию системы"""
        print(f"\nTestOS версия {version}\n")
    
    def do_CLS(self, arg):
        """Очистить экран"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def do_DIR(self, arg):
        """Показать содержимое каталога"""
        path = os.path.join(self.current_dir, arg) if arg else self.current_dir
        path = path.replace("/", "\\")
        
        if not path.endswith("\\"):
            path += "\\"
        
        if path not in self.fs:
            show_bsod("0x00000024")
            return
        
        print(f"\n Содержимое каталога {path}\n")
        print(f"{'Имя':<12} {'Тип':<8} {'Размер':>10} {'Дата':>12}")
        print("-" * 45)
        
        for dir_name in self.fs[path]["dirs"]:
            print(f"{dir_name:<12} {'<DIR>':<8} {'':>10} {datetime.date.today().strftime('%d-%m-%y'):>12}")
        
        for file_name, size in self.fs[path]["files"].items():
            print(f"{file_name:<12} {'Файл':<8} {size:>10} {datetime.date.today().strftime('%d-%m-%y'):>12}")
        
        total_files = len(self.fs[path]["files"])
        total_dirs = len(self.fs[path]["dirs"])
        print(f"\n Файлов: {total_files}\n Каталогов: {total_dirs}\n")
    
    def do_CD(self, arg):
        """Сменить текущий каталог"""
        if not arg:
            print(f"\nТекущий каталог: {self.current_dir}\n")
            return
        
        new_path = os.path.join(self.current_dir, arg)
        new_path = new_path.replace("/", "\\")
        
        if arg == "\\":
            new_path = "C:\\"
        elif arg == "..":
            if self.current_dir == "C:\\":
                print("\nУже в корневом каталоге\n")
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
        """Создать каталог"""
        if not arg:
            show_bsod("0x0000001E")
            return
        
        new_dir = os.path.join(self.current_dir, arg)
        new_dir = new_dir.replace("/", "\\")
        
        if not new_dir.endswith("\\"):
            new_dir += "\\"
        
        if new_dir in self.fs:
            print("\nКаталог уже существует\n")
        else:
            self.fs[self.current_dir]["dirs"].append(arg)
            self.fs[new_dir] = {"dirs": [], "files": {}}
            print(f"\nКаталог создан: {new_dir}\n")
    
    def do_RD(self, arg):
        """Удалить каталог"""
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
            print("\nКаталог не пуст\n")
        else:
            self.fs[self.current_dir]["dirs"].remove(arg)
            del self.fs[target_dir]
            print(f"\nКаталог удален: {target_dir}\n")
    
    def do_COPY(self, arg):
        """Копировать файл"""
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
        print("\n1 файл(ов) скопирован(о)\n")
    
    def do_DEL(self, arg):
        """Удалить файл"""
        if not arg:
            show_bsod("0x00000026")
            return
        
        if "WINDOWS" in self.current_dir.upper():
            show_bsod("0x80070091")
            return
        
        deleted = False
        for path in self.fs:
            if arg in self.fs[path]["files"]:
                del self.fs[path]["files"][arg]
                deleted = True
                break
        
        if deleted:
            print(f"\nФайл удален: {arg}\n")
        else:
            show_bsod("0x00000027")
    
    def do_TIME(self, arg):
        """Показать/установить время"""
        now = datetime.datetime.now()
        print(f"\nТекущее время: {now.strftime('%H:%M:%S')}")
        print("Введите новое время (ЧЧ:ММ:СС): ", end="")
        try:
            new_time = input()
            if new_time:
                print("\nВремя установлено (эмуляция)\n")
        except:
            pass
    
    def do_DATE(self, arg):
        """Показать/установить дату"""
        now = datetime.datetime.now()
        print(f"\nТекущая дата: {now.strftime('%d-%m-%Y')}")
        print("Введите новую дату (ДД-ММ-ГГГГ): ", end="")
        try:
            new_date = input()
            if new_date:
                print("\nДата установлена (эмуляция)\n")
        except:
            pass
    
    def do_CALC(self, arg):
        """Калькулятор: CALC <число> <операция> <число>"""
        if not arg:
            print("\nИспользование: CALC <число> <операция> <число>")
            print("Доступные операции: + - * /")
            return
        
        try:
            parts = arg.split()
            if len(parts) != 3:
                raise ValueError("Неверный формат")
            
            a = float(parts[0])
            op = parts[1]
            b = float(parts[2])
            
            if op == '+':
                res = a + b
            elif op == '-':
                res = a - b
            elif op == '*':
                res = a * b
            elif op == '/':
                res = a / b
            else:
                raise ValueError("Неверная операция")
            
            print(f"\nРезультат: {res}\n")
        except ZeroDivisionError:
            print("\nОшибка: деление на ноль!\n")
        except Exception as e:
            print(f"\nОшибка: {e}\nИспользование: CALC <число> <операция> <число>\n")
    
    def _print_tictactoe_board(self):
        """Печать доски крестиков-ноликов"""
        print("\n   A   B   C")
        print(f"1  {self.tictactoe_board['A1']} | {self.tictactoe_board['B1']} | {self.tictactoe_board['C1']} ")
        print("  ---+---+---")
        print(f"2  {self.tictactoe_board['A2']} | {self.tictactoe_board['B2']} | {self.tictactoe_board['C2']} ")
        print("  ---+---+---")
        print(f"3  {self.tictactoe_board['A3']} | {self.tictactoe_board['B3']} | {self.tictactoe_board['C3']} \n")
    
    def _check_tictactoe_win(self):
        """Проверка победы в крестиках-ноликах"""
        # Горизонтали
        for row in ['1', '2', '3']:
            if (self.tictactoe_board[f'A{row}'] == self.tictactoe_board[f'B{row}'] == self.tictactoe_board[f'C{row}'] != ' '):
                return True
        
        # Вертикали
        for col in ['A', 'B', 'C']:
            if (self.tictactoe_board[f'{col}1'] == self.tictactoe_board[f'{col}2'] == self.tictactoe_board[f'{col}3'] != ' '):
                return True
        
        # Диагонали
        if (self.tictactoe_board['A1'] == self.tictactoe_board['B2'] == self.tictactoe_board['C3'] != ' '):
            return True
        if (self.tictactoe_board['A3'] == self.tictactoe_board['B2'] == self.tictactoe_board['C1'] != ' '):
            return True
        
        return False
    
    def do_TICTACTOE(self, arg):
        """Крестики-нолики: TICTACTOE START для начала игры"""
        if arg.upper() == "START":
            self.tictactoe_board = {
                'A1': ' ', 'B1': ' ', 'C1': ' ',
                'A2': ' ', 'B2': ' ', 'C2': ' ',
                'A3': ' ', 'B3': ' ', 'C3': ' '
            }
            self.tictactoe_turn = 'X'
            print("\nИгра началась! Ходят крестики (X)")
            print("Вводите координаты (например: A1)")
            self._print_tictactoe_board()
            return
        
        if not self.tictactoe_board:
            print("\nИгра не начата. Введите TICTACTOE START")
            return
        
        move = arg.upper()
        if move not in self.tictactoe_board:
            print("\nНеверный ход. Используйте формат A1, B2, C3 и т.д.")
            return
        
        if self.tictactoe_board[move] != ' ':
            print("\nЭта клетка уже занята!")
            return
        
        self.tictactoe_board[move] = self.tictactoe_turn
        self._print_tictactoe_board()
        
        if self._check_tictactoe_win():
            print(f"\nИгрок {self.tictactoe_turn} победил!\n")
            self.tictactoe_board = None
            return
        
        if all(cell != ' ' for cell in self.tictactoe_board.values()):
            print("\nНичья!\n")
            self.tictactoe_board = None
            return
        
        self.tictactoe_turn = 'O' if self.tictactoe_turn == 'X' else 'X'
        print(f"\nХод игрока {self.tictactoe_turn}\n")
    
    def do_HELP(self, arg):
        """Показать справку по командам"""
        commands = {
            "VER": "Показать версию TestOS",
            "CLS": "Очистить экран",
            "DIR": "Показать содержимое каталога",
            "CD": "Сменить текущий каталог",
            "MD": "Создать каталог",
            "RD": "Удалить каталог",
            "COPY": "Копировать файл(ы)",
            "DEL": "Удалить файл(ы)",
            "TIME": "Показать/установить время",
            "DATE": "Показать/установить дату",
            "CALC": "Калькулятор",
            "TICTACTOE": "Игра в крестики-нолики",
            "HELP": "Показать эту справку",
            "EXIT": "Выйти из эмулятора",
            "BSOD": "Имитировать синий экран смерти (тест)"
        }
        
        if not arg:
            print("\nДоступные команды:\n")
            for cmd, desc in commands.items():
                print(f"{cmd:12} - {desc}")
            print("\nДля подробной справки введите HELP имя_команды\n")
        else:
            cmd = arg.upper()
            if cmd in commands:
                print(f"\n{cmd} - {commands[cmd]}\n")
            else:
                print("\nКоманда не найдена\n")
    
    def do_EXIT(self, arg):
        """Выйти из TestOS"""
        print(f"\nСпасибо за использование TestOS версии {version}\n")
        return True
    
    do_QUIT = do_EXIT

if __name__ == "__main__":
    try:
        TestOS().cmdloop()
    except KeyboardInterrupt:
        print("\n^C\n")
        sys.exit(0)
    except Exception as e:
        show_bsod(f"0x{random.randint(0, 0xFFFF):04X}")
        sys.exit(1)
