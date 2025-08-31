import os, sys, ctypes, pyfiglet

from pystyle        import Colors, Colorate, Center
from fade           import pinkred

class terminal:
    class print:        
        def success(text):
            print(f"{Colorate.Horizontal(Colors.green_to_white, '[ SUCCESS ]', 1)} {text}")
    
        def fail(text):
            print(f"{Colorate.Horizontal(Colors.red_to_white, '[ FAILURE ]', 1)} {text}")
            
        def warn(text):
            print(f"{Colorate.Horizontal(Colors.red_to_yellow, '[ WARNING ]', 1)} {text}")
            
        def info(text):
            print(f"{Colorate.Horizontal(Colors.blue_to_white, '[  INFO.  ]', 1)} {text}")
            
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
            terminal.print.warn("Unsupported operating system, Lapidary may not work properly.")
        return

    def setTitle(title):
        system = os.name
        
        if system == "nt":
            ctypes.windll.kernel32.SetConsoleTitleW(f"Lapidary ~ {title}")
        elif system == 'posix':
            sys.stdout.write(f"\x1b]0;Lapidary ~ {title}\x07")
        else:
            terminal.print.warn("Unsupported operating system, Lapidary may not work properly.")