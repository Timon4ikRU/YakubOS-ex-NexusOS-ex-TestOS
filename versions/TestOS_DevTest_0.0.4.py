import os
import sys
import datetime
import random
import time
import shutil
from cmd import Cmd
import builtins

version = "DevTest 0.0.4"
DATA_ROOT = "D:\\TestOS_data"

def is_idle():
    """Проверяем, запущен ли код в IDLE"""
    return 'idlelib.run' in sys.modules

def show_bsod(error_code="0x00000001"):
    """Функция для отображения синего экрана смерти (BSOD)"""
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        sys.__stdout__.write("\n"*5)
        sys.__stdout__.write(" "*20 + "="*60 + "\n")
        sys.__stdout__.write(" "*20 + f"|{'ПРОИЗОШЛА КРИТИЧЕСКАЯ ОШИБКА':^58}|\n")
        sys.__stdout__.write(" "*20 + f"|{'TestOS обнаружила проблему и будет перезагружена':^58}|\n")
        sys.__stdout__.write(" "*20 + f"| Код ошибки: {error_code:<45}|\n")
        sys.__stdout__.write(" "*20 + "| Нажмите Enter для перезагрузки...          |\n")
        sys.__stdout__.write(" "*20 + "="*60 + "\n")
        sys.__stdout__.write("\n"*5)
        input()
    except:
        pass
    finally:
        os.system('cls' if os.name == 'nt' else 'clear')
        
def ensure_data_dir():
    """Создает базовую структуру папок, если их нет"""
    os.makedirs(os.path.join(DATA_ROOT, "C", "WINDOWS", "SYSTEM"), exist_ok=True)
    os.makedirs(os.path.join(DATA_ROOT, "C", "DOS"), exist_ok=True)
    os.makedirs(os.path.join(DATA_ROOT, "C", "TEMP"), exist_ok=True)
    os.makedirs(os.path.join(DATA_ROOT, "C", "GAMES"), exist_ok=True)
    
    # Создаем несколько тестовых файлов
    for path, content in [
        ("C\\AUTOEXEC.BAT", "@echo off"),
        ("C\\CONFIG.SYS", "DEVICE=C:\\DOS\\HIMEM.SYS"),
        ("C\\WINDOWS\\WIN.INI", "[windows]"),
        ("C\\DOS\\MEM.EXE", "MEM" * 1000)
    ]:
        full_path = os.path.join(DATA_ROOT, path)
        if not os.path.exists(full_path):
            with open(full_path, 'w') as f:
                f.write(content)

class TestOS(Cmd):
    intro = f"""
GercogRybron(R) TestOS(R) Версия {version}
(C)Тимофей Якубов 2025 - Наше время.
Введите HELP для списка команд.

Файловая система: {DATA_ROOT}
Новые возможности:
- Создание и вывод файлов
- Запуск python-файлов прямо в ОС
\n"""
    
    def __init__(self):
        super().__init__()
        ensure_data_dir()
        self.current_dir = "C:\\"
        self.update_prompt()
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
    
    def get_real_path(self, path=None):
        """Преобразует виртуальный путь в реальный"""
        if path is None:
            path = self.current_dir
        rel_path = path[3:]  # Убираем "C:\"
        return os.path.join(DATA_ROOT, "C", rel_path.replace("\\", os.sep))
    
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
        target_path = os.path.join(self.current_dir, arg) if arg else self.current_dir
        target_path = target_path.replace("/", "\\")
        
        if not target_path.endswith("\\"):
            target_path += "\\"
        
        real_path = self.get_real_path(target_path)
        
        if not os.path.isdir(real_path):
            show_bsod("0x00000024")
            return
        
        print(f"\n Содержимое каталога {target_path}\n")
        print(f"{'Имя':<12} {'Тип':<8} {'Размер':>10} {'Дата':>12}")
        print("-" * 45)
        
        total_files = 0
        total_dirs = 0
        
        try:
            for entry in os.listdir(real_path):
                full_path = os.path.join(real_path, entry)
                if os.path.isdir(full_path):
                    print(f"{entry:<12} {'<DIR>':<8} {'':>10} {datetime.date.fromtimestamp(os.path.getmtime(full_path)).strftime('%d-%m-%y'):>12}")
                    total_dirs += 1
                else:
                    size = os.path.getsize(full_path)
                    print(f"{entry:<12} {'Файл':<8} {size:>10} {datetime.date.fromtimestamp(os.path.getmtime(full_path)).strftime('%d-%m-%y'):>12}")
                    total_files += 1
        except Exception as e:
            show_bsod("0x00000025")
            return
        
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
        
        real_path = self.get_real_path(new_path)
        if os.path.isdir(real_path):
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
        
        real_path = self.get_real_path(new_dir)
        if os.path.exists(real_path):
            print("\nКаталог уже существует\n")
        else:
            try:
                os.makedirs(real_path)
                print(f"\nКаталог создан: {new_dir}\n")
            except:
                show_bsod("0x0000001F")
    
    def do_RD(self, arg):
        """Удалить каталог"""
        if not arg:
            show_bsod("0x0000002A")
            return
        
        target_dir = os.path.join(self.current_dir, arg)
        target_dir = target_dir.replace("/", "\\")
        
        if not target_dir.endswith("\\"):
            target_dir += "\\"
        
        real_path = self.get_real_path(target_dir)
        if not os.path.isdir(real_path):
            show_bsod("0x0000002B")
        elif os.listdir(real_path):
            print("\nКаталог не пуст\n")
        else:
            try:
                os.rmdir(real_path)
                print(f"\nКаталог удален: {target_dir}\n")
            except:
                show_bsod("0x0000002C")
    
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
        
        real_src = self.get_real_path(src)
        real_dst = self.get_real_path(dst)
        
        if not os.path.isfile(real_src):
            show_bsod("0x0000007B")
            return
        
        try:
            if os.path.isdir(real_dst):
                real_dst = os.path.join(real_dst, os.path.basename(real_src))
            shutil.copy2(real_src, real_dst)
            print("\n1 файл(ов) скопирован(о)\n")
        except:
            show_bsod("0x0000007C")
    
    def do_DEL(self, arg):
        """Удалить файл"""
        if not arg:
            show_bsod("0x00000026")
            return
        
        if "WINDOWS" in self.current_dir.upper():
            show_bsod("0x80070091")
            return
        
        real_path = self.get_real_path(os.path.join(self.current_dir, arg))
        if os.path.isfile(real_path):
            try:
                os.remove(real_path)
                print(f"\nФайл удален: {arg}\n")
            except:
                show_bsod("0x00000027")
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
    
    def do_CF(self, arg):
        """Создать файл с кодом: CF Имя "Содержимое" PY
        Для записи кавычек используйте двойные кавычки: \" """
        if not arg:
            print("\nИспользование: CF Имя_файла \"Содержимое\" Расширение")
            print("Пример для Python: CF SCRIPT \"print('Hello')\" PY")
            print("Спецсимволы: /n - перенос строки, /t - табуляция")
            print("Для записи кавычек внутри текста используйте \\\"")
            print(f"Файл будет создан в: {self.current_dir}")
            return
        
        try:
            parts = arg.split('"')
            if len(parts) < 3:
                raise ValueError("Неверный формат")
            
            name_part = parts[0].strip()
            content = parts[1].replace("/n", "\n").replace("/t", "\t")
            ext_part = parts[2].strip().upper()
            
            filename = f"{name_part}.{ext_part}" if ext_part else name_part
            filename = filename.replace(" ", "_")
            
            full_path = os.path.join(self.get_real_path(), filename)
            
            if os.path.exists(full_path):
                print(f"\nОшибка: Файл {filename} уже существует!\n")
                return
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"\nФайл создан: {self.current_dir}{filename}\n")
            
            if ext_part == 'PY':
                print("Это Python-скрипт. Вы можете выполнить его командой RUN")
            
        except Exception as e:
            print(f"\nОшибка: {e}")
            print("\nПравильный формат: CF Имя \"Содержимое\" Расширение")
            print('Пример с кавычками: CF TEST "print(\\\"Hello\\\")" PY\n')

    def do_RUN(self, arg):
        """Выполнить Python-скрипт: RUN Имя_файла.PY"""
        if not arg:
            print("\nИспользование: RUN Имя_файла.PY")
            return
        
        if not arg.upper().endswith('.PY'):
            print("\nОшибка: Можно выполнять только .PY файлы!")
            return
        
        try:
            full_path = os.path.join(self.get_real_path(), arg)
            
            if not os.path.isfile(full_path):
                print(f"\nФайл {arg} не найден!")
                return
            
            print(f"\nВыполняю {arg}...\n" + "-"*40)
            
            # Читаем скрипт
            with open(full_path, 'r', encoding='utf-8') as f:
                script = f.read()
            
            # Создаем безопасное пространство имен
            safe_globals = {
                '__name__': '__main__',
                '__file__': full_path,
                'print': print,
                'os': os,
                'sys': sys,
                'time': time,
                'datetime': datetime
            }
            
            # Добавляем встроенные функции
            for name in dir(builtins):
                if not name.startswith('_'):
                    safe_globals[name] = getattr(builtins, name)
            
            # Выполняем скрипт
            exec(script, safe_globals)
            
            print("-"*40 + "\nВыполнение завершено.\n")
            
        except Exception as e:
            print(f"\nОшибка выполнения: {type(e).__name__}: {e}\n")

            
    def do_TYPE(self, arg):
        """Вывести содержимое файла: TYPE Имя.Расширение"""
        if not arg:
            print("\nИспользование: TYPE Имя_файла")
            print(f"Показывает содержимое файла из текущей директории: {self.current_dir}")
            return
        
        try:
            # Полный путь к файлу
            full_path = os.path.join(self.get_real_path(), arg)
            
            if not os.path.isfile(full_path):
                print(f"\nОшибка: Файл {arg} не найден!\n")
                return
            
            # Проверяем размер файла (чтобы не выводить гигантские файлы)
            file_size = os.path.getsize(full_path)
            if file_size > 1024*1024:  # 1MB
                print("\nОшибка: Файл слишком большой для отображения!\n")
                return
            
            # Читаем и выводим содержимое
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"\nСодержимое файла {self.current_dir}{arg}:\n")
            print("-"*60)
            print(content)
            print("-"*60)
            print(f"\nРазмер: {file_size} байт\n")
            
        except UnicodeDecodeError:
            print("\nОшибка: Файл содержит бинарные данные и не может быть прочитан как текст!\n")
        except Exception as e:
            print(f"\nОшибка при чтении файла: {e}\n")
            
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
            "BSOD": "Имитировать синий экран смерти (тест)",
            "CF": "Создать файл (формат команды: CF Название Содержание_в_кавычках_двойных Фромат_файла)",
            "TYPE": "Вывести содержимое файла до 1 МБ"
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
        if not os.path.exists(DATA_ROOT):
            os.makedirs(DATA_ROOT)
        TestOS().cmdloop()
    except Exception as e:
        show_bsod(f"0x{random.randint(0, 0xFFFF):04X}")
        sys.exit(1)
