from tools.webhook.main          import *
from tools.generators.main       import *
from tools.misc.main             import *
from tools.nuker.main            import *

from util.terminal               import *
from os                          import _exit

t = terminal

class core:
    def menu():
        print(Center.XCenter(f"""
            {Fore.MAGENTA}01 »{Fore.RESET} Webhook Tool         {Fore.MAGENTA}04 »{Fore.RESET} Misc
            {Fore.MAGENTA}02 »{Fore.RESET} Generators
            {Fore.MAGENTA}03 »{Fore.RESET} Nuker
              """))
    
    def main():
        t.clear()
        t.setTitle("ALL-IN-ONE")
        t.print.logo("Lapidary")
        core.menu()
        
        while True:
            try:
                choice = input(Colorate.Horizontal(Colors.red_to_purple, "lapidary@main → select~ ", 1))
                
                if choice in ["1", "01"]:
                    webhook.main()
                elif choice in ["2", "02"]:
                    generator.main()
                elif choice in ["3", "03"]:
                    nuker.main()
                elif choice in ["4", "04"]:
                    misc.main()
                elif choice in ["exit", "x"]:
                    t.print.warn("Exiting the Lapidary...")
                    sleep(0.35)
                    _exit(0)
            except KeyboardInterrupt:
                print()
                t.print.warn("Exiting the Lapidary...")
                sleep(0.35)
                _exit(0)

if __name__ == "__main__":
    core.main()