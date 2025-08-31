import os, sys, ctypes, pyfiglet, datetime, toml

from pystyle        import Colors, Colorate, Center
from fade           import pinkred
from colorama       import Fore

settings = toml.load('./util/settings.toml')
name = settings['general']['name']

class terminal:
    class print:        
        def success(text):
            current_time = datetime.datetime.now()
            current_time_str = current_time.strftime("%H:%M:%S")
            print(f"{Fore.LIGHTBLACK_EX}{current_time_str}{Fore.RESET} {Colorate.Horizontal(Colors.green_to_white, '[ SUCCESS ]', 1)} {text}")
    
        def fail(text):
            current_time = datetime.datetime.now()
            current_time_str = current_time.strftime("%H:%M:%S")
            print(f"{Fore.LIGHTBLACK_EX}{current_time_str}{Fore.RESET} {Colorate.Horizontal(Colors.red_to_white, '[ FAILURE ]', 1)} {text}")
            
        def warn(text):
            current_time = datetime.datetime.now()
            current_time_str = current_time.strftime("%H:%M:%S")
            print(f"{Fore.LIGHTBLACK_EX}{current_time_str}{Fore.RESET} {Colorate.Horizontal(Colors.red_to_yellow, '[ WARNING ]', 1)} {text}")
            
        def info(text):
            current_time = datetime.datetime.now()
            current_time_str = current_time.strftime("%H:%M:%S")
            print(f"{Fore.LIGHTBLACK_EX}{current_time_str}{Fore.RESET} {Colorate.Horizontal(Colors.blue_to_white, '[  INFO.  ]', 1)} {text}")
            
        def logo(text):
            logo = Center.XCenter(pyfiglet.figlet_format(text.capitalize(), font="ansi_shadow"))
            
            print("\n")
            print(pinkred(logo))
            
    def clear():
        system = os.name
        
        if system == 'nt':
            os.system('cls')
        elif system == 'posix':
            os.system('clear')
        else:
            print('\n'*120)
            terminal.print.warn(f"Unsupported operating system, {name.capitalize()} may not work properly.")
        return

    def setTitle(title):
        system = os.name
        
        if system == "nt":
            ctypes.windll.kernel32.SetConsoleTitleW(f"{name.capitalize()} ~ {title}")
        elif system == 'posix':
            sys.stdout.write(f"\x1b]0;{name.capitalize()} ~ {title}\x07")
        else:
            terminal.print.warn(f"Unsupported operating system, {name.capitalize()} may not work properly.")