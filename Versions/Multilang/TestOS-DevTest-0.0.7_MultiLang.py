import os
import sys
import datetime
import random
import time
import shutil
from cmd import Cmd
import builtins
import platform
import ctypes
import math
from colorama import init, Fore, Back, Style
import pyfiglet

# Инициализация colorama
init()

version = "0.0.7 MiltiLang"
DATA_ROOT = os.path.join(os.path.expanduser("~"), "TestOS_data")

# Языковые настройки
LANGUAGES = {
    'ru': {
        'welcome': "Добро пожаловать в TestOS!",
        'select_lang': "Выберите язык (ru/en): ",
        'invalid_lang': "Неверный выбор языка, используется русский по умолчанию.",
        'help_title': "Справка по командам",
        'help_page': "Страница {}",
        'help_next': "Следующая страница: HELP {}",
        'ver_title': "О системе",
        'ver_content': "TestOS Версия {}\n\nНовые возможности в этой версии:\n- Поддержка псевдографики\n- Цветное оформление\n- Анимация загрузки\n- Упрощенный ввод для игр",
        'current_dir': "Текущий каталог: {}",
        'dir_title': "Содержимое каталога",
        'dir_content': "\n Содержимое каталога {}\n\n{:<12} {:<8} {:>10} {:>12}\n{}\n",
        'dir_footer': "\n Файлов: {}\n Каталогов: {}",
        'file_not_found': "Файл {} не найден!",
        'color_usage': "Использование:\n  COLOR #AABBCC  - HEX-цвет\n  COLOR RED      - именованные цвета (RED, GREEN, BLUE, WHITE)",
        'color_changed': "Цвет изменен на {}",
        'color_error': "Неверный цвет! Доступно:\n- HEX: #AABBCC или #ABC\n- Именованные: RED, GREEN, BLUE, WHITE",
        'calc_usage': "Использование: CALC <число> <операция> <число>\nДоступные операции: + - * /",
        'calc_result': "Результат: {}",
        'calc_error': "Ошибка: {}\nИспользование: CALC <число> <операция> <число>",
        'ttt_usage': "Использование: TICTACTOE START\nИли просто введите координаты (A1, B2 и т.д.)",
        'ttt_start': "Игра началась! Ходят крестики (X)\nВводите координаты (например: A1)",
        'ttt_invalid': "Неверный ход. Используйте формат A1, B2, C3 и т.д.",
        'ttt_taken': "Эта клетка уже занята!",
        'ttt_win': "Игрок {} победил!",
        'ttt_draw': "Ничья!",
        'ttt_turn': "Ход игрока {}",
        'cf_usage': "Использование: CF Имя_файла \"Содержимое\" Расширение\nПример для Python: CF SCRIPT \"print('Hello')\" PY\nСпецсимволы: /n - перенос строки, /t - табуляция\nДля записи кавычек внутри текста используйте \\\"\nФайл будет создан в: {}",
        'cf_created': "Файл создан: {}{}",
        'cf_exists': "Ошибка: Файл {} уже существует!",
        'cf_error': "Ошибка: {}\nПравильный формат: CF Имя \"Содержимое\" Расширение\nПример с кавычками: CF TEST \"print(\\\"Hello\\\")\" PY",
        'run_usage': "Использование: RUN Имя_файла.PY или RUN Имя_файла.BAT",
        'run_error': "Ошибка: Можно выполнять только .PY или .BAT файлы!",
        'type_usage': "Использование: TYPE Имя_файла\nПоказывает содержимое файла из текущей директории: {}",
        'type_error': "Ошибка: Файл {} не найден!",
        'type_binary': "Ошибка: Файл содержит бинарные данные и не может быть прочитан как текст!",
        'type_content': "Содержимое файла {}{}:\n{}\n{}\n{}\nРазмер: {} байт",
        'time_current': "Текущее время: {}",
        'time_set': "Время установлено (эмуляция)",
        'date_current': "Текущая дата: {}",
        'date_set': "Дата установлена (эмуляция)",
        'copy_success': "1 файл(ов) скопирован(о)",
        'del_success': "Файл удален:\n{}",
        'md_success': "Каталог создан:\n{}",
        'rd_success': "Каталог удален:\n{}",
        'bsod_title': "ПРОИЗОШЛА КРИТИЧЕСКАЯ ОШИБКА",
        'bsod_message': "TestOS обнаружила проблему и будет перезагружена",
        'bsod_code': "Код ошибки: {}",
        'bsod_restart': "Нажмите Enter для перезагрузки...",
        'prompt': "{}> ",
        'boot': "Загрузка системы...",
        'intro': "TestOS Версия {}\n© Тимофей Якубов 2025\n\nФайловая система: {}\nДля первого тестового запуска введите: RUN HELLO_WORLD.BAT\n\nВведите HELP для списка команд"
    },
    'en': {
        'welcome': "Welcome to TestOS!",
        'select_lang': "Choose language (ru/en): ",
        'invalid_lang': "Invalid language choice, using English by default.",
        'help_title': "Command Help",
        'help_page': "Page {}",
        'help_next': "Next page: HELP {}",
        'ver_title': "About System",
        'ver_content': "TestOS Version {}\n\nNew features in this version:\n- Pseudographics support\n- Color scheme\n- Boot animation\n- Simplified input for games",
        'current_dir': "Current directory: {}",
        'dir_title': "Directory Content",
        'dir_content': "\n Content of directory {}\n\n{:<12} {:<8} {:>10} {:>12}\n{}\n",
        'dir_footer': "\n Files: {}\n Directories: {}",
        'file_not_found': "File {} not found!",
        'color_usage': "Usage:\n  COLOR #AABBCC  - HEX color\n  COLOR RED      - named colors (RED, GREEN, BLUE, WHITE)",
        'color_changed': "Color changed to {}",
        'color_error': "Invalid color! Available:\n- HEX: #AABBCC or #ABC\n- Named: RED, GREEN, BLUE, WHITE",
        'calc_usage': "Usage: CALC <number> <operation> <number>\nAvailable operations: + - * /",
        'calc_result': "Result: {}",
        'calc_error': "Error: {}\nUsage: CALC <number> <operation> <number>",
        'ttt_usage': "Usage: TICTACTOE START\nOr just enter coordinates (A1, B2 etc.)",
        'ttt_start': "Game started! X's turn\nEnter coordinates (e.g. A1)",
        'ttt_invalid': "Invalid move. Use format A1, B2, C3 etc.",
        'ttt_taken': "This cell is already taken!",
        'ttt_win': "Player {} wins!",
        'ttt_draw': "Draw!",
        'ttt_turn': "Player {}'s turn",
        'cf_usage': "Usage: CF Filename \"Content\" Extension\nPython example: CF SCRIPT \"print('Hello')\" PY\nSpecial chars: /n - new line, /t - tab\nTo use quotes inside text use \\\"\nFile will be created in: {}",
        'cf_created': "File created: {}{}",
        'cf_exists': "Error: File {} already exists!",
        'cf_error': "Error: {}\nCorrect format: CF Name \"Content\" Extension\nExample with quotes: CF TEST \"print(\\\"Hello\\\")\" PY",
        'run_usage': "Usage: RUN Filename.PY or RUN Filename.BAT",
        'run_error': "Error: Only .PY or .BAT files can be executed!",
        'type_usage': "Usage: TYPE Filename\nShows file content from current directory: {}",
        'type_error': "Error: File {} not found!",
        'type_binary': "Error: File contains binary data and cannot be read as text!",
        'type_content': "Content of file {}{}:\n{}\n{}\n{}\nSize: {} bytes",
        'time_current': "Current time: {}",
        'time_set': "Time set (emulation)",
        'date_current': "Current date: {}",
        'date_set': "Date set (emulation)",
        'copy_success': "1 file(s) copied",
        'del_success': "File deleted:\n{}",
        'md_success': "Directory created:\n{}",
        'rd_success': "Directory deleted:\n{}",
        'bsod_title': "A CRITICAL ERROR OCCURRED",
        'bsod_message': "TestOS has encountered a problem and will be restarted",
        'bsod_code': "Error code: {}",
        'bsod_restart': "Press Enter to restart...",
        'prompt': "{}> ",
        'boot': "Loading system...",
        'intro': "TestOS Version {}\n© Timofey Yakubov 2025\n\nFile system: {}\nFor first test run enter: RUN HELLO_WORLD.BAT\n\nType HELP for command list"
    }
}

current_lang = 'en'  # По умолчанию английский

# Проверка доступности звука
sound_enabled = False
if sys.platform == 'win32':
    try:
        import winsound
        sound_enabled = True
    except ImportError:
        sound_enabled = False

def is_idle():
    return 'idlelib.run' in sys.modules

def play_sound(frequency, duration):
    if not sound_enabled or is_idle():
        return
    try:
        winsound.Beep(frequency, int(duration * 1000))
    except:
        pass

def show_bsod(error_code="0x00000001"):
    try:
        play_sound(2000, 2.0)
        print("\n"*5)
        print(" "*20 + "="*60)
        print(" "*20 + f"|{LANGUAGES[current_lang]['bsod_title']:^58}|")
        print(" "*20 + f"|{LANGUAGES[current_lang]['bsod_message']:^58}|")
        print(" "*20 + f"| {LANGUAGES[current_lang]['bsod_code'].format(error_code):<45}|")
        print(" "*20 + f"| {LANGUAGES[current_lang]['bsod_restart']:^36} |")
        print(" "*20 + "="*60)
        print("\n"*5)
        input()
    except:
        pass
    finally:
        play_sound(300, 0.8)
        os.system('cls' if os.name == 'nt' else 'clear')
        main()

def draw_window(title, content, width=60, height=10):
    """Рисует окно в стиле Windows 11"""
    # Верхняя граница
    border_top = "╔" + "═" * (width - 2) + "╗"
    
    # Линия заголовка
    title_line = f"║ {Fore.CYAN}{title.center(width-3)}{Style.RESET_ALL}║"
    
    # Разделитель
    separator = "╟" + "─" * (width - 2) + "╢"
    
    # Содержимое
    content_lines = []
    for line in content.split('\n'):
        while len(line) > width-3:
            content_lines.append(line[:width-3])
            line = line[width-3:]
        content_lines.append(line)
    
    # Нижняя граница
    border_bottom = "╚" + "═" * (width - 2) + "╝"
    
    # Отрисовка окна
    print(Fore.WHITE + Back.BLUE + border_top + Style.RESET_ALL)
    print(Fore.WHITE + Back.BLUE + title_line + Style.RESET_ALL)
    print(Fore.WHITE + Back.BLUE + separator + Style.RESET_ALL)
    
    for i in range(min(height, len(content_lines))):
        line = content_lines[i].ljust(width-3)
        print(Fore.WHITE + Back.BLUE + f"║ {line}║" + Style.RESET_ALL)
    
    # Заполнение пустых строк
    for _ in range(height - len(content_lines)):
        print(Fore.WHITE + Back.BLUE + f"║ {' '*(width-3)}║" + Style.RESET_ALL)
    
    print(Fore.WHITE + Back.BLUE + border_bottom + Style.RESET_ALL)

def ensure_data_dir():
    os.makedirs(os.path.join(DATA_ROOT, "C", "WINDOWS", "SYSTEM"), exist_ok=True)
    os.makedirs(os.path.join(DATA_ROOT, "C", "DOS"), exist_ok=True)
    os.makedirs(os.path.join(DATA_ROOT, "C", "TEMP"), exist_ok=True)
    os.makedirs(os.path.join(DATA_ROOT, "C", "GAMES"), exist_ok=True)
    
    for path, content in [
        ("C\\AUTOEXEC.BAT", "@echo off"),
        ("C\\CONFIG.SYS", "DEVICE=C:\\DOS\\HIMEM.SYS"),
        ("C\\WINDOWS\\WIN.INI", "[windows]"),
        ("C\\DOS\\MEM.EXE", "MEM" * 1000),
        ("C\\HELLO_WORLD.BAT", 
         "@echo off\n"
         "echo ============================\n"
         "echo Привет, мир от TestOS!\n"
         "echo Это демонстрационный BAT-файл\n"
         "echo ============================\n"
         "echo.\n"
         "echo Текущая дата: %date%\n"
         "echo Текущее время: %time%\n"
         "echo.\n"
         "echo Список файлов в текущей папке:\n"
         "dir\n"
         "pause\n"
         "cls\n"
         "echo Спасибо за использование TestOS!\n"
         "pause")
   ]:
        full_path = os.path.join(DATA_ROOT, path)
        if not os.path.exists(full_path):
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)

class TestOS(Cmd):
    def __init__(self):
        super().__init__()
        self.current_dir = "C:\\"
        self.update_prompt()
        self.tictactoe_board = None
        self.tictactoe_turn = 'X'
        self.boot_screen()
        ensure_data_dir()
        self.intro = self.get_intro()
    
    def boot_screen(self):
        """Улучшенный экран загрузки"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # ASCII-арт логотипа
        try:
            logo = pyfiglet.figlet_format("TestOS", font="small")
            print(Fore.BLUE + logo + Style.RESET_ALL)
        except:
            print(Fore.BLUE + "TestOS" + Style.RESET_ALL)
            print("=" * 40)
        
        # Анимация загрузки
        print(Fore.CYAN + LANGUAGES[current_lang]['boot'] + Style.RESET_ALL)
        for i in range(1, 101):
            time.sleep(0.01)
            bar = "[" + "█" * (i//2) + " " * (50 - i//2) + "]"
            print(f"\r{Fore.YELLOW}{bar}{Style.RESET_ALL} {i}%", end='', flush=True)
        
        play_sound(300, 0.8)
        print("\n\n")
        time.sleep(0.5)
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_intro(self):
        """Генерирует интро в стиле Windows 11"""
        intro_text = LANGUAGES[current_lang]['intro'].format(version, DATA_ROOT)
        return f"""
{Fore.CYAN}╔══════════════════════════════════════════════════╗
║{Fore.WHITE}{'TestOS ' + ('Версия' if current_lang == 'ru' else 'Version') + ' ' + version:^50}{Fore.CYAN}║
║{Fore.WHITE}{'© Тимофей Якубов 2025' if current_lang == 'ru' else '© Timofey Yakubov 2025':^50}{Fore.CYAN}║
╚══════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.YELLOW}{'Файловая система' if current_lang == 'ru' else 'File system'}: {DATA_ROOT}{Style.RESET_ALL}
{Fore.GREEN}{'Для первого тестового запуска введите' if current_lang == 'ru' else 'For first test run enter'}: RUN HELLO_WORLD.BAT{Style.RESET_ALL}

{Fore.WHITE}{'Введите' if current_lang == 'ru' else 'Type'} {Fore.CYAN}HELP{Fore.WHITE} {'для списка команд' if current_lang == 'ru' else 'for command list'}{Style.RESET_ALL}
"""
    
    def update_prompt(self):
        """Стилизованный prompt в стиле Windows 11"""
        self.prompt = f"{Fore.BLUE}{self.current_dir}{Style.RESET_ALL}{Fore.CYAN}>{Style.RESET_ALL} "
    
    def emptyline(self):
        pass
    
    def precmd(self, line):
        """Обработка команды перед выполнением"""
        if not line:
            return line
            
        # Упрощённый ввод для крестиков-ноликов
        if self.tictactoe_board and len(line) == 2 and line[0].upper() in 'ABC' and line[1] in '123':
            return f"TICTACTOE {line}"
            
        # Обычная обработка команд
        parts = line.split(maxsplit=1)
        cmd = parts[0].upper()
        args = parts[1] if len(parts) > 1 else ""
        
        return f"{cmd} {args}".strip()

    def do_COLOR(self, arg):
        """Изменить цвет текста: COLOR [#HEX] или [RED|GREEN|BLUE|WHITE]"""
        content = ""
        if not arg:
            content = LANGUAGES[current_lang]['color_usage']
            draw_window("Смена цвета текста", content)
            return
        
        arg = arg.upper().strip()
        
        # Обработка HEX-цветов (#AABBCC или #ABC)
        if arg.startswith('#'):
            hex_color = arg[1:]
            
            # Проверка формата
            if len(hex_color) not in (3, 6):
                content = "Ошибка: HEX-цвет должен быть в формате #ABC или #AABBCC"
                draw_window("Ошибка смены цвета", content)
                return
                
            # Конвертация #ABC в #AABBCC
            if len(hex_color) == 3:
                hex_color = ''.join([c*2 for c in hex_color])
            
            try:
                # Конвертация HEX в RGB
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                
                # Формирование ANSI-кода (True Color)
                print(f"\033[38;2;{r};{g};{b}m")
                content = LANGUAGES[current_lang]['color_changed'].format(f"HEX #{hex_color}")
                draw_window("Смена цвета текста", content)
            except ValueError:
                content = "Ошибка: неверный HEX-формат"
                draw_window("Ошибка смены цвета", content)
            return
        
        # Стандартные цвета (обратная совместимость)
        color_map = {
            'RED': '\033[91m',
            'GREEN': '\033[92m',
            'BLUE': '\033[94m',
            'WHITE': '\033[0m',
        }
        
        if arg in color_map:
            print(color_map[arg], end='')
            content = LANGUAGES[current_lang]['color_changed'].format(arg)
            draw_window("Смена цвета текста", content)
        else:
            content = LANGUAGES[current_lang]['color_error']
            draw_window("Ошибка смены цвета", content)
            
    def do_VER(self, arg):
        """Показать версию системы"""
        content = LANGUAGES[current_lang]['ver_content'].format(version)
        draw_window(LANGUAGES[current_lang]['ver_title'], content)
    
    def do_CLS(self, arg):
        """Очистить экран"""
        os.system('cls' if os.name == 'nt' else 'clear')
        # Перерисовываем интро после очистки
        print(self.get_intro())
    
    def do_DIR(self, arg):
        """Показать содержимое каталога"""
        target_path = os.path.join(self.current_dir, arg) if arg else self.current_dir
        target_path = target_path.replace("/", "\\")
        
        if not target_path.endswith("\\"):
            target_path += "\\"
        
        real_path = os.path.join(DATA_ROOT, "C", target_path[3:])
        
        if not os.path.isdir(real_path):
            show_bsod("0x00000024")
            return
        
        content = LANGUAGES[current_lang]['dir_content'].format(
            target_path,
            'Name' if current_lang == 'en' else 'Имя',
            'Type' if current_lang == 'en' else 'Тип',
            'Size' if current_lang == 'en' else 'Размер',
            'Date' if current_lang == 'en' else 'Дата',
            Fore.YELLOW + "-" * 45 + Style.RESET_ALL
        )
        
        total_files = 0
        total_dirs = 0
        
        try:
            for entry in os.listdir(real_path):
                full_path = os.path.join(real_path, entry)
                if os.path.isdir(full_path):
                    content += f"{Fore.BLUE}{entry:<12}{Style.RESET_ALL} {'<DIR>':<8} {'':>10} {datetime.date.fromtimestamp(os.path.getmtime(full_path)).strftime('%d-%m-%y'):>12}\n"
                    total_dirs += 1
                else:
                    size = os.path.getsize(full_path)
                    content += f"{Fore.GREEN}{entry:<12}{Style.RESET_ALL} {'File' if current_lang == 'en' else 'Файл':<8} {size:>10} {datetime.date.fromtimestamp(os.path.getmtime(full_path)).strftime('%d-%m-%y'):>12}\n"
                    total_files += 1
        except Exception as e:
            show_bsod("0x00000025")
            return
        
        content += LANGUAGES[current_lang]['dir_footer'].format(total_files, total_dirs)
        draw_window(LANGUAGES[current_lang]['dir_title'], content)
    
    def do_CD(self, arg):
        """Сменить текущий каталог"""
        if not arg:
            content = LANGUAGES[current_lang]['current_dir'].format(self.current_dir)
            draw_window("Текущая директория", content)
            return
        
        new_path = os.path.join(self.current_dir, arg)
        new_path = new_path.replace("/", "\\")
        
        if arg == "\\":
            new_path = "C:\\"
        elif arg == "..":
            if self.current_dir == "C:\\":
                content = "Уже в корневом каталоге" if current_lang == 'ru' else "Already at root directory"
                draw_window("Смена директории", content)
                return
            parts = self.current_dir.split("\\")
            new_path = "\\".join(parts[:-2]) + "\\"
        
        if not new_path.endswith("\\"):
            new_path += "\\"
        
        real_path = os.path.join(DATA_ROOT, "C", new_path[3:])
        if os.path.isdir(real_path):
            self.current_dir = new_path
            self.update_prompt()
            content = f"Текущая директория изменена на:\n{self.current_dir}" if current_lang == 'ru' else f"Current directory changed to:\n{self.current_dir}"
            draw_window("Смена директории", content)
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
        
        real_path = os.path.join(DATA_ROOT, "C", new_dir[3:])
        if os.path.exists(real_path):
            content = "Каталог уже существует" if current_lang == 'ru' else "Directory already exists"
            draw_window("Ошибка создания", content)
        else:
            try:
                os.makedirs(real_path)
                content = LANGUAGES[current_lang]['md_success'].format(new_dir)
                draw_window("Создание каталога", content)
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
        
        real_path = os.path.join(DATA_ROOT, "C", target_dir[3:])
        if not os.path.isdir(real_path):
            show_bsod("0x0000002B")
        elif os.listdir(real_path):
            content = "Каталог не пуст" if current_lang == 'ru' else "Directory not empty"
            draw_window("Ошибка удаления", content)
        else:
            try:
                os.rmdir(real_path)
                content = LANGUAGES[current_lang]['rd_success'].format(target_dir)
                draw_window("Удаление каталога", content)
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
        
        real_src = os.path.join(DATA_ROOT, "C", src[3:])
        real_dst = os.path.join(DATA_ROOT, "C", dst[3:])
        
        if not os.path.isfile(real_src):
            show_bsod("0x0000007B")
            return
        
        try:
            if os.path.isdir(real_dst):
                real_dst = os.path.join(real_dst, os.path.basename(real_src))
            shutil.copy2(real_src, real_dst)
            content = LANGUAGES[current_lang]['copy_success']
            draw_window("Копирование файла", content)
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
        
        real_path = os.path.join(DATA_ROOT, "C", self.current_dir[3:], arg)
        if os.path.isfile(real_path):
            try:
                os.remove(real_path)
                content = LANGUAGES[current_lang]['del_success'].format(arg)
                draw_window("Удаление файла", content)
            except:
                show_bsod("0x00000027")
        else:
            show_bsod("0x00000027")
    
    def do_TIME(self, arg):
        """Показать/установить время"""
        now = datetime.datetime.now()
        content = LANGUAGES[current_lang]['time_current'].format(Fore.CYAN + now.strftime('%H:%M:%S') + Style.RESET_ALL) + "\n"
        content += "Введите новое время (ЧЧ:ММ:СС): " if current_lang == 'ru' else "Enter new time (HH:MM:SS): "
        draw_window("Системное время", content)
        
        try:
            new_time = input()
            if new_time:
                content = LANGUAGES[current_lang]['time_set']
                draw_window("Установка времени", content)
        except:
            pass
    
    def do_DATE(self, arg):
        """Показать/установить дату"""
        now = datetime.datetime.now()
        content = LANGUAGES[current_lang]['date_current'].format(Fore.CYAN + now.strftime('%d-%m-%Y') + Style.RESET_ALL) + "\n"
        content += "Введите новую дату (ДД-ММ-ГГГГ): " if current_lang == 'ru' else "Enter new date (DD-MM-YYYY): "
        draw_window("Системная дата", content)
        
        try:
            new_date = input()
            if new_date:
                content = LANGUAGES[current_lang]['date_set']
                draw_window("Установка даты", content)
        except:
            pass
    
    def do_CALC(self, arg):
        """Калькулятор: CALC <число> <операция> <число>"""
        if not arg:
            content = LANGUAGES[current_lang]['calc_usage']
            draw_window("Калькулятор", content)
            return
        
        try:
            parts = arg.split()
            if len(parts) != 3:
                raise ValueError("Неверный формат" if current_lang == 'ru' else "Invalid format")
            
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
                raise ValueError("Неверная операция" if current_lang == 'ru' else "Invalid operation")
            
            content = LANGUAGES[current_lang]['calc_result'].format(Fore.CYAN + str(res) + Style.RESET_ALL)
            draw_window("Калькулятор", content)
        except ZeroDivisionError:
            content = "Ошибка: деление на ноль!" if current_lang == 'ru' else "Error: division by zero!"
            draw_window("Ошибка калькулятора", content)
        except Exception as e:
            content = LANGUAGES[current_lang]['calc_error'].format(e)
            draw_window("Ошибка калькулятора", content)
    
    def _print_tictactoe_board(self):
        print("\n   A   B   C")
        print(f"1  {self._get_cell('A1')} | {self._get_cell('B1')} | {self._get_cell('C1')} ")
        print("  ---+---+---")
        print(f"2  {self._get_cell('A2')} | {self._get_cell('B2')} | {self._get_cell('C2')} ")
        print("  ---+---+---")
        print(f"3  {self._get_cell('A3')} | {self._get_cell('B3')} | {self._get_cell('C3')} \n")
    
    def _get_cell(self, cell):
        """Возвращает содержимое клетки с цветом"""
        value = self.tictactoe_board[cell]
        if value == 'X':
            return Fore.RED + 'X' + Style.RESET_ALL
        elif value == 'O':
            return Fore.BLUE + 'O' + Style.RESET_ALL
        return ' '

    def _check_tictactoe_win(self):
        for row in ['1', '2', '3']:
            if (self.tictactoe_board[f'A{row}'] == self.tictactoe_board[f'B{row}'] == self.tictactoe_board[f'C{row}'] != ' '):
                return True
        
        for col in ['A', 'B', 'C']:
            if (self.tictactoe_board[f'{col}1'] == self.tictactoe_board[f'{col}2'] == self.tictactoe_board[f'{col}3'] != ' '):
                return True
        
        if (self.tictactoe_board['A1'] == self.tictactoe_board['B2'] == self.tictactoe_board['C3'] != ' '):
            return True
        if (self.tictactoe_board['A3'] == self.tictactoe_board['B2'] == self.tictactoe_board['C1'] != ' '):
            return True
        
        return False
    
    def do_TICTACTOE(self, arg):
        """Крестики-нолики: TICTACTOE START для начала игры"""
        if not arg:
            content = LANGUAGES[current_lang]['ttt_usage']
            draw_window("Крестики-нолики", content)
            return
        
        # Нормализуем ввод (удаляем лишние пробелы и переводим в верхний регистр)
        args = arg.upper().strip().split()
        
        # Обработка команды START
        if args[0] == "START":
            self.tictactoe_board = {
                'A1': ' ', 'B1': ' ', 'C1': ' ',
                'A2': ' ', 'B2': ' ', 'C2': ' ',
                'A3': ' ', 'B3': ' ', 'C3': ' '
            }
            self.tictactoe_turn = 'X'
            content = "\n" + LANGUAGES[current_lang]['ttt_start'] + "\n"
            self._print_tictactoe_board()
            return
        
        # Проверка, что игра начата
        if not self.tictactoe_board:
            content = "Игра не начата. Введите TICTACTOE START" if current_lang == 'ru' else "Game not started. Type TICTACTOE START"
            draw_window("Ошибка", content)
            return
        
        # Обработка хода
        move = args[0] if args else ""
        if len(move) != 2 or move[0] not in 'ABC' or move[1] not in '123':
            content = LANGUAGES[current_lang]['ttt_invalid']
            draw_window("Ошибка", content)
            return
        
        if self.tictactoe_board[move] != ' ':
            content = LANGUAGES[current_lang]['ttt_taken']
            draw_window("Ошибка", content)
            return
        
        self.tictactoe_board[move] = self.tictactoe_turn
        self._print_tictactoe_board()
        
        if self._check_tictactoe_win():
            content = LANGUAGES[current_lang]['ttt_win'].format(self.tictactoe_turn)
            draw_window("Победа!", content)
            self.tictactoe_board = None
            return
        
        if all(cell != ' ' for cell in self.tictactoe_board.values()):
            content = LANGUAGES[current_lang]['ttt_draw']
            draw_window("Ничья", content)
            self.tictactoe_board = None
            return
        
        self.tictactoe_turn = 'O' if self.tictactoe_turn == 'X' else 'X'
        content = LANGUAGES[current_lang]['ttt_turn'].format(self.tictactoe_turn)
        draw_window("Крестики-нолики", content)
        
    def do_CF(self, arg):
        """Создать файл с кодом: CF Имя "Содержимое" PY"""
        if not arg:
            content = LANGUAGES[current_lang]['cf_usage'].format(self.current_dir)
            draw_window("Создание файла", content)
            return
        
        try:
            parts = arg.split('"')
            if len(parts) < 3:
                raise ValueError("Неверный формат" if current_lang == 'ru' else "Invalid format")
            
            name_part = parts[0].strip()
            content = parts[1].replace("/n", "\n").replace("/t", "\t")
            ext_part = parts[2].strip().upper()
            
            filename = f"{name_part}.{ext_part}" if ext_part else name_part
            filename = filename.replace(" ", "_")
            
            full_path = os.path.join(DATA_ROOT, "C", self.current_dir[3:], filename)
            
            if os.path.exists(full_path):
                content = LANGUAGES[current_lang]['cf_exists'].format(filename)
                draw_window("Ошибка создания файла", content)
                return
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            content = LANGUAGES[current_lang]['cf_created'].format(self.current_dir, filename)
            if ext_part == 'PY':
                content += "\nЭто Python-скрипт. Вы можете выполнить его командой RUN" if current_lang == 'ru' else "\nThis is a Python script. You can run it with RUN command"
            elif ext_part == 'BAT':
                content += "\nЭто BAT-файл. Вы можете выполнить его командой RUN" if current_lang == 'ru' else "\nThis is a BAT file. You can run it with RUN command"
            
            draw_window("Файл создан", content)
            
        except Exception as e:
            content = LANGUAGES[current_lang]['cf_error'].format(e)
            draw_window("Ошибка создания файла", content)

    def do_RUN(self, arg):
        """Выполнить Python-скрипт или BAT-файл: RUN Имя_файла.PY или RUN Имя_файла.BAT"""
        if not arg:
            content = LANGUAGES[current_lang]['run_usage']
            draw_window("Выполнение файла", content)
            return
        
        if not (arg.upper().endswith('.PY') or arg.upper().endswith('.BAT')):
            content = LANGUAGES[current_lang]['run_error']
            draw_window("Ошибка выполнения", content)
            if sound_enabled:
                play_sound(80, 1.0)
            return
        
        try:
            full_path = os.path.join(DATA_ROOT, "C", self.current_dir[3:], arg)
            
            if not os.path.isfile(full_path):
                content = LANGUAGES[current_lang]['file_not_found'].format(arg)
                draw_window("Ошибка выполнения", content)
                if sound_enabled:
                    play_sound(80, 1.0)
                return
            
            content = f"Выполняю {arg}..." if current_lang == 'ru' else f"Executing {arg}..."
            content += "\n" + "-"*40 + "\n"
            draw_window("Выполнение файла", content)
            
            if arg.upper().endswith('.PY'):
                with open(full_path, 'r', encoding='utf-8') as f:
                    script = f.read()
                
                safe_globals = {
                    '__name__': '__main__',
                    '__file__': full_path,
                    'print': print,
                    'os': os,
                    'sys': sys,
                    'time': time,
                    'datetime': datetime
                }
                
                for name in dir(builtins):
                    if not name.startswith('_'):
                        safe_globals[name] = getattr(builtins, name)
                
                exec(script, safe_globals)
            else:  # .BAT файл
                with open(full_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('@') and not line.startswith('REM'):
                            print(f"> {line}")
                            # Обработка переменных среды
                            line = line.replace('%date%', datetime.datetime.now().strftime('%d-%m-%Y'))
                            line = line.replace('%time%', datetime.datetime.now().strftime('%H:%M:%S'))
                            
                            # Эмулируем выполнение команд BAT
                            if line.upper().startswith('ECHO'):
                                print(line[4:].strip())
                            elif line.upper().startswith('PAUSE'):
                                input("Нажмите Enter для продолжения..." if current_lang == 'ru' else "Press Enter to continue...")
                            elif line.upper().startswith('CLS'):
                                self.do_CLS('')
                            elif line.upper().startswith('DIR'):
                                self.do_DIR(line[3:].strip() if len(line) > 3 else '')
                            else:
                                print(f"(эмуляция) {line}" if current_lang == 'ru' else f"(emulation) {line}")
                                
            print("-"*40 + "\nВыполнение завершено.\n" if current_lang == 'ru' else "-"*40 + "\nExecution completed.\n")
            if sound_enabled:
                play_sound(120, 1.0)
            
        except Exception as e:
            content = f"Ошибка выполнения: {type(e).__name__}: {e}" if current_lang == 'ru' else f"Execution error: {type(e).__name__}: {e}"
            draw_window("Ошибка выполнения", content)
            if sound_enabled:
                play_sound(80, 1.0)
                
    def do_TYPE(self, arg):
        """Вывести содержимое файла: TYPE Имя.Расширение"""
        if not arg:
            content = LANGUAGES[current_lang]['type_usage'].format(self.current_dir)
            draw_window("Просмотр файла", content)
            return
        
        try:
            full_path = os.path.join(DATA_ROOT, "C", self.current_dir[3:], arg)
            
            if not os.path.isfile(full_path):
                content = LANGUAGES[current_lang]['type_error'].format(arg)
                draw_window("Ошибка", content)
                return
            
            file_size = os.path.getsize(full_path)
            if file_size > 1024*1024:
                content = "Ошибка: Файл слишком большой для отображения!" if current_lang == 'ru' else "Error: File is too large to display!"
                draw_window("Ошибка", content)
                return
            
            with open(full_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
            
            output = LANGUAGES[current_lang]['type_content'].format(
                self.current_dir,
                arg,
                "-"*60,
                file_content,
                "-"*60,
                file_size
            )
            
            draw_window("Просмотр файла", output)
            
        except UnicodeDecodeError:
            content = LANGUAGES[current_lang]['type_binary']
            draw_window("Ошибка", content)
        except Exception as e:
            content = f"Ошибка при чтении файла: {e}" if current_lang == 'ru' else f"Error reading file: {e}"
            draw_window("Ошибка", content)
    
    def do_HELP(self, arg):
        """Показать справку по командам"""
        commands = [
            ("VER", "Показать версию TestOS", "Show TestOS version"),
            ("CLS", "Очистить экран", "Clear screen"),
            ("DIR", "Показать содержимое каталога", "Show directory content"),
            ("CD", "Сменить текущий каталог", "Change current directory"),
            ("MD", "Создать каталог", "Make directory"),
            ("RD", "Удалить каталог", "Remove directory"),
            ("COLOR", "Изменить цвет текста", "Change text color"),
            ("COPY", "Копировать файл(ы)", "Copy file(s)"),
            ("DEL", "Удалить файл(ы)", "Delete file(s)"),
            ("TIME", "Показать/установить время", "Show/set time"),
            ("DATE", "Показать/установить дату", "Show/set date"),
            ("FIRSTTEST", "Запустить тестирование системы", "Run system test"),
            ("DRVINFO", "Показать список драйверов", "Show drivers list"),
            ("DRVLOAD", "Загрузить драйвер", "Load driver"),
            ("DRVUNLOAD", "Выгрузить драйвер", "Unload driver"),
            ("CALC", "Калькулятор", "Calculator"),
            ("TICTACTOE", "Игра в крестики-нолики", "Tic-tac-toe game"),
            ("HELP", "Показать эту справку", "Show this help"),
            ("EXIT", "Выйти из эмулятора", "Exit emulator"),
            ("BSOD", "Имитировать синий экран смерти", "Simulate BSOD"),
            ("CF", "Создать файл с кодом", "Create file with code"),
            ("TYPE", "Вывести содержимое файла", "Show file content"),
            ("RUN", "Выполнить Python-скрипт или BAT-файл", "Run Python script or BAT file"),
            ("RELOAD", "Перезагрузить систему", "Reload system")
        ]
        
        # Разбиваем команды на страницы по 8 команд на страницу
        pages = []
        for i in range(0, len(commands), 8):
            pages.append(commands[i:i+8])
        
        # Если аргумент пустой, показываем первую страницу
        if not arg:
            page_num = 1
        else:
            try:
                page_num = int(arg)
                if page_num < 1 or page_num > len(pages):
                    raise ValueError
            except ValueError:
                content = "Неверный номер страницы" if current_lang == 'ru' else "Invalid page number"
                draw_window("Ошибка", content)
                return
        
        # Показываем запрошенную страницу
        content = f"{LANGUAGES[current_lang]['help_title']}\n\n"
        content += f"{LANGUAGES[current_lang]['help_page'].format(page_num)}\n\n"
        
        for cmd in pages[page_num-1]:
            content += f"{Fore.CYAN}{cmd[0]:12}{Style.RESET_ALL} - {cmd[1] if current_lang == 'ru' else cmd[2]}\n"
        
        # Добавляем подсказку о следующей странице, если она есть
        if page_num < len(pages):
            content += f"\n{LANGUAGES[current_lang]['help_next'].format(page_num+1)}"
        
        draw_window(LANGUAGES[current_lang]['help_title'], content)
    
    def do_BSOD(self, arg):
        """Имитировать синий экран смерти"""
        show_bsod("0x000000ED")
    
    def do_FIRSTTEST(self, arg):
        """Запустить тестирование системы: FIRSTTEST [--FORCE]"""
        if not arg or arg.upper() != "--FORCE":
            content = "Этот тест проверит основные функции системы.\n" if current_lang == 'ru' else "This test will check basic system functions.\n"
            content += "Вы уверены, что хотите продолжить? (Y/N): " if current_lang == 'ru' else "Are you sure you want to continue? (Y/N): "
            draw_window("Тестирование системы", content)
            
            answer = input().upper()
            if answer != 'Y':
                content = "Тестирование отменено." if current_lang == 'ru' else "Test canceled."
                draw_window("Тестирование системы", content)
                return
        
        content = "Запуск комплексного тестирования TestOS..." if current_lang == 'ru' else "Starting comprehensive TestOS testing..."
        draw_window("Тестирование системы", content)
        time.sleep(1)
        
        test_results = {
            'Файловая система' if current_lang == 'ru' else 'File system': False,
            'Команды' if current_lang == 'ru' else 'Commands': False,
            'Игры' if current_lang == 'ru' else 'Games': False,
            'Скрипты' if current_lang == 'ru' else 'Scripts': False,
            'Системные функции' if current_lang == 'ru' else 'System functions': False
        }
        
        try:
            # Тест файловой системы
            content = "=== Тест файловой системы ===" if current_lang == 'ru' else "=== File system test ==="
            draw_window("Тестирование системы", content)
            self.do_MD("TEST_DIR")
            self.do_CD("TEST_DIR")
            self.do_CF("TEST_FILE \"Тестовое содержимое\" TXT" if current_lang == 'ru' else "TEST_FILE \"Test content\" TXT")
            self.do_TYPE("TEST_FILE.TXT")
            self.do_COPY("TEST_FILE.TXT TEST_COPY.TXT")
            self.do_DEL("TEST_FILE.TXT")
            self.do_CD("..")
            self.do_RD("TEST_DIR")
            test_results['Файловая система' if current_lang == 'ru' else 'File system'] = True
            content = "Файловая система: OK" if current_lang == 'ru' else "File system: OK"
            draw_window("Тестирование системы", content)
            
            # Тест основных команд
            content = "=== Тест основных команд ===" if current_lang == 'ru' else "=== Basic commands test ==="
            draw_window("Тестирование системы", content)
            self.do_VER("")
            self.do_TIME("")
            self.do_DATE("")
            self.do_CALC("2 + 3 * 4")
            test_results['Команды' if current_lang == 'ru' else 'Commands'] = True
            content = "Основные команды: OK" if current_lang == 'ru' else "Basic commands: OK"
            draw_window("Тестирование системы", content)
            
            # Тест игр
            content = "=== Тест игр ===" if current_lang == 'ru' else "=== Games test ==="
            draw_window("Тестирование системы", content)
            self.do_TICTACTOE("START")
            content = "(Эмуляция игры в крестики-нолики)" if current_lang == 'ru' else "(Tic-tac-toe game emulation)"
            draw_window("Тестирование системы", content)
            test_results['Игры' if current_lang == 'ru' else 'Games'] = True
            content = "Игры: OK" if current_lang == 'ru' else "Games: OK"
            draw_window("Тестирование системы", content)
            
            # Тест скриптов
            content = "=== Тест скриптов ===" if current_lang == 'ru' else "=== Scripts test ==="
            draw_window("Тестирование системы", content)
            content = "Запуск HELLO_WORLD.BAT..." if current_lang == 'ru' else "Running HELLO_WORLD.BAT..."
            draw_window("Тестирование системы", content)
            self.do_RUN("HELLO_WORLD.BAT")
            test_results['Скрипты' if current_lang == 'ru' else 'Scripts'] = True
            content = "Скрипты: OK" if current_lang == 'ru' else "Scripts: OK"
            draw_window("Тестирование системы", content)
            
            # Тест системных функций
            content = "=== Тест системных функций ===" if current_lang == 'ru' else "=== System functions test ==="
            draw_window("Тестирование системы", content)
            self.do_COLOR("GREEN")
            content = "Цвет текста изменен (должен быть зеленым)" if current_lang == 'ru' else "Text color changed (should be green)"
            draw_window("Тестирование системы", content)
            self.do_COLOR("WHITE")
            content = "Цвет текста восстановлен" if current_lang == 'ru' else "Text color restored"
            draw_window("Тестирование системы", content)
            test_results['Системные функции' if current_lang == 'ru' else 'System functions'] = True
            content = "Системные функции: OK" if current_lang == 'ru' else "System functions: OK"
            draw_window("Тестирование системы", content)
            
            # Итоговый отчет
            content = "\n=== Результаты тестирования ===\n" if current_lang == 'ru' else "\n=== Test results ===\n"
            for test, result in test_results.items():
                status = f"{Fore.GREEN}УСПЕШНО{Style.RESET_ALL}" if result else f"{Fore.RED}ОШИБКА{Style.RESET_ALL}" if current_lang == 'ru' else f"{Fore.GREEN}SUCCESS{Style.RESET_ALL}" if result else f"{Fore.RED}ERROR{Style.RESET_ALL}"
                content += f"{test:20}: {status}\n"
            
            if all(test_results.values()):
                content += "\nВсе тесты пройдены успешно! Система работает корректно." if current_lang == 'ru' else "\nAll tests passed successfully! System is working correctly."
                draw_window("Результаты тестирования", content)
                if sound_enabled:
                    play_sound(1000, 0.5)
                    play_sound(1500, 0.5)
            else:
                content += "\nОбнаружены проблемы в работе системы!" if current_lang == 'ru' else "\nProblems detected in system operation!"
                draw_window("Результаты тестирования", content)
                if sound_enabled:
                    play_sound(200, 1.0)
            
        except Exception as e:
            content = f"Ошибка во время тестирования: {e}" if current_lang == 'ru' else f"Error during testing: {e}"
            draw_window("Ошибка тестирования", content)
            if sound_enabled:
                play_sound(200, 1.0)

    def do_RELOAD(self, arg):
        """Перезагрузить систему"""
        content = "Перезагрузка TestOS..." if current_lang == 'ru' else "Reloading TestOS..."
        draw_window("Перезагрузка", content)
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        main()
    
    def do_EXIT(self, arg):
        """Выйти из TestOS"""
        print(f"\nСпасибо за использование TestOS версии {version}\n" if current_lang == 'ru' else f"\nThank you for using TestOS version {version}\n")
        return True

    def do_DRVINFO(self, arg):
        """Показать информацию о драйверах основной системы"""
        if platform.system() != "Windows":
            content = "Эта команда доступна только в Windows" if current_lang == 'ru' else "This command is available only in Windows"
            draw_window("Ошибка", content)
            return
            
        try:
            import winreg
            content = "Список драйверов Windows (из реестра):\n\n" if current_lang == 'ru' else "Windows drivers list (from registry):\n\n"
            
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                              r"SYSTEM\CurrentControlSet\Services") as key:
                i = 0
                while True:
                    try:
                        name = winreg.EnumKey(key, i)
                        try:
                            with winreg.OpenKey(key, name) as subkey:
                                type_val = winreg.QueryValueEx(subkey, "Type")[0]
                                if type_val == 1:  # SERVICE_KERNEL_DRIVER
                                    image_path = winreg.QueryValueEx(subkey, "ImagePath")[0]
                                    state = "Загружен" if winreg.QueryValueEx(subkey, "Start")[0] == 0 else "Не загружен" if current_lang == 'ru' else "Loaded" if winreg.QueryValueEx(subkey, "Start")[0] == 0 else "Not loaded"
                                    content += f"{Fore.CYAN}{name:<30}{Style.RESET_ALL} {image_path:<50} {state:<10}\n"
                        except:
                            pass
                        i += 1
                    except OSError:
                        break
            draw_window("Драйверы системы", content)
        except Exception as e:
            content = f"Ошибка: {e}" if current_lang == 'ru' else f"Error: {e}"
            draw_window("Ошибка", content)

    def do_DRVLOAD(self, arg):
        """Загрузить драйвер в основной системе (требует прав админа)"""
        if not arg:
            content = "Использование: DRVLOAD путь_к_драйверу\n" if current_lang == 'ru' else "Usage: DRVLOAD driver_path\n"
            content += "Пример: DRVLOAD C:\\drivers\\example.sys" if current_lang == 'ru' else "Example: DRVLOAD C:\\drivers\\example.sys"
            draw_window("Загрузка драйвера", content)
            return
        
        if platform.system() == "Windows":
            try:
                # Проверяем существование файла
                if not os.path.exists(arg):
                    content = f"Файл драйвера {arg} не найден!" if current_lang == 'ru' else f"Driver file {arg} not found!"
                    draw_window("Ошибка", content)
                    return
                
                # Загружаем драйвер через Service Control Manager
                advapi32 = ctypes.windll.advapi32
                SC_MANAGER_ALL_ACCESS = 0xF003F
                
                sc_handle = advapi32.OpenSCManagerW(
                    None, None, SC_MANAGER_ALL_ACCESS)
                if not sc_handle:
                    content = "Ошибка доступа к Service Manager. Требуются права администратора." if current_lang == 'ru' else "Error accessing Service Manager. Administrator rights required."
                    draw_window("Ошибка", content)
                    return
                
                # Создаем временное имя службы
                service_name = "TestOS_" + os.path.basename(arg).split('.')[0]
                service_name = service_name[:32]
                
                # Создаем службу для драйвера
                service_handle = advapi32.CreateServiceW(
                    sc_handle,
                    service_name,
                    service_name,
                    0xF01FF,  # SERVICE_ALL_ACCESS
                    1,        # SERVICE_KERNEL_DRIVER
                    3,        # SERVICE_DEMAND_START
                    1,        # SERVICE_ERROR_NORMAL
                    arg,
                    None, None, None, None, None)
                
                if not service_handle:
                    content = f"Ошибка создания службы: {ctypes.get_last_error()}" if current_lang == 'ru' else f"Error creating service: {ctypes.get_last_error()}"
                    draw_window("Ошибка", content)
                    advapi32.CloseServiceHandle(sc_handle)
                    return
                
                # Запускаем службу
                if advapi32.StartServiceW(service_handle, 0, None):
                    content = f"Драйвер {os.path.basename(arg)} успешно загружен!" if current_lang == 'ru' else f"Driver {os.path.basename(arg)} loaded successfully!"
                    draw_window("Успех", content)
                else:
                    content = f"Ошибка загрузки драйвера: {ctypes.get_last_error()}" if current_lang == 'ru' else f"Error loading driver: {ctypes.get_last_error()}"
                    draw_window("Ошибка", content)
                
                advapi32.CloseServiceHandle(service_handle)
                advapi32.CloseServiceHandle(sc_handle)
                
            except Exception as e:
                content = f"Ошибка: {e}" if current_lang == 'ru' else f"Error: {e}"
                draw_window("Ошибка", content)
        
        else:
            content = "Эта команда доступна только в Windows" if current_lang == 'ru' else "This command is available only in Windows"
            draw_window("Ошибка", content)

    def do_DRVUNLOAD(self, arg):
        """Выгрузить драйвер из основной системы (требует прав админа)"""
        if not arg:
            content = "Использование: DRVUNLOAD имя_драйвера\n" if current_lang == 'ru' else "Usage: DRVUNLOAD driver_name\n"
            content += "Пример: DRVUNLOAD example.sys" if current_lang == 'ru' else "Example: DRVUNLOAD example.sys"
            draw_window("Выгрузка драйвера", content)
            return
        
        if platform.system() == "Windows":
            try:
                advapi32 = ctypes.windll.advapi32
                SC_MANAGER_ALL_ACCESS = 0xF003F
                
                sc_handle = advapi32.OpenSCManagerW(
                    None, None, SC_MANAGER_ALL_ACCESS)
                if not sc_handle:
                    content = "Ошибка доступа к Service Manager. Требуются права администратора." if current_lang == 'ru' else "Error accessing Service Manager. Administrator rights required."
                    draw_window("Ошибка", content)
                    return
                
                service_name = "TestOS_" + arg.split('.')[0]
                service_handle = advapi32.OpenServiceW(
                    sc_handle,
                    service_name,
                    0xF01FF)  # SERVICE_ALL_ACCESS
                
                if not service_handle:
                    content = f"Служба для драйвера {arg} не найдена!" if current_lang == 'ru' else f"Service for driver {arg} not found!"
                    draw_window("Ошибка", content)
                    advapi32.CloseServiceHandle(sc_handle)
                    return
                
                # Останавливаем службу
                SERVICE_STATUS = ctypes.c_uint32
                status = SERVICE_STATUS()
                if advapi32.ControlService(service_handle, 1, ctypes.byref(status)):
                    content = f"Драйвер {arg} успешно выгружен!" if current_lang == 'ru' else f"Driver {arg} unloaded successfully!"
                    draw_window("Успех", content)
                else:
                    content = f"Ошибка выгрузки драйвера: {ctypes.get_last_error()}" if current_lang == 'ru' else f"Error unloading driver: {ctypes.get_last_error()}"
                    draw_window("Ошибка", content)
                
                advapi32.DeleteService(service_handle)
                advapi32.CloseServiceHandle(service_handle)
                advapi32.CloseServiceHandle(sc_handle)
                
            except Exception as e:
                content = f"Ошибка: {e}" if current_lang == 'ru' else f"Error: {e}"
                draw_window("Ошибка", content)
        
        else:
            content = "Эта команда доступна только в Windows" if current_lang == 'ru' else "This command is available only in Windows"
            draw_window("Ошибка", content)
    
    do_QUIT = do_EXIT

def select_language():
    """Функция выбора языка при запуске"""
    global current_lang
    
    print(LANGUAGES['en']['welcome'])
    lang = input(LANGUAGES['en']['select_lang']).strip().lower()
    
    if lang in ('ru', 'en'):
        current_lang = lang
    else:
        print(LANGUAGES['en']['invalid_lang'])
        current_lang = 'en'

def main():
    try:
        select_language()  # Выбор языка при запуске
        
        if not os.path.exists(DATA_ROOT):
            print(f"Создаю корневую папку {DATA_ROOT}..." if current_lang == 'ru' else f"Creating root directory {DATA_ROOT}...")
            os.makedirs(DATA_ROOT)
        TestOS().cmdloop()
    except KeyboardInterrupt:
        print("\nЗавершение работы..." if current_lang == 'ru' else "\nShutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"\nОшибка запуска: {e}" if current_lang == 'ru' else f"\nStartup error: {e}")
        show_bsod(f"0x{random.randint(0, 0xFFFF):04X}")

if __name__ == "__main__":
    main()
