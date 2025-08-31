import requests, random

from util.terminal import *
from colorama      import Fore
from time          import sleep

t = terminal

class misc:    
    class iptools:
        def ipinfo(ip):
            # IP info API'den bilgi al
            url = f"https://ipinfo.io/{ip}/json"
            try:
                response = requests.get(url)
                response.raise_for_status()  # HTTPError varsa istisna fırlatır
                data = response.json()
            except requests.exceptions.RequestException as e:
                t.print.fail(f"Error fetching IP information.")
                return None
            except Exception:
                return t.print.fail("An error occured while fetching IP information.")
            
            return data
        
        def myip():
            try:
                response = requests.get("https://ipinfo.io/ip")
                response.raise_for_status()  # HTTPError varsa istisna fırlatır
                ip = response.text.strip()  # Yanıtı al ve boşlukları kaldır
                return t.print.success(f"Your IP adress is: {ip}")
            except requests.exceptions.RequestException as e:
                t.print.fail(f"Error fetching IP information.")
                return None
            except Exception:
                return t.print.fail("An error occured while fetching IP information.")
        
        def randomip():
            return t.print.success(f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}")
        
    def menu():
        print(Center.XCenter(f"""
{Fore.MAGENTA}01 »{Fore.RESET} IP Info
{Fore.MAGENTA}02 »{Fore.RESET} My IP
{Fore.MAGENTA}03 »{Fore.RESET} Random IP
              """))
    
    def main():
        t.clear()
        t.print.logo("MISC")
        t.setTitle("discord@misc:menu")
        misc.menu()
        
        while True:
            try: 
                choice = input(Colorate.Horizontal(Colors.red_to_purple, "lapidary@misc:menu → select~ ", 1))
                
                if (choice == "1" or choice == "01"):
                    ip = input(Colorate.Horizontal(Colors.red_to_purple, "lapidary@misc:ipinfo → ip~ ", 1))
                    
                    try:
                        info = misc.iptools.ipinfo(ip)
                        if info:
                            print(f"""
    {Colorate.Horizontal(Colors.red_to_white, 'Connection Information', 1)}
        {Fore.YELLOW}IP:{Fore.RESET} {info["ip"]}
        {Fore.YELLOW}Hostname (DNS):{Fore.RESET} {info["hostname"]}
        {Fore.YELLOW}ORG:{Fore.RESET} {info["org"]}

    {Colorate.Horizontal(Colors.red_to_white, 'Location Information', 1)}
        {Fore.YELLOW}City:{Fore.RESET} {info["city"]}
        {Fore.YELLOW}Country:{Fore.RESET} {info["country"]}
        {Fore.YELLOW}Location:{Fore.RESET} {info["loc"]}
        {Fore.YELLOW}Postal:{Fore.RESET} {info["postal"]}
        {Fore.YELLOW}Timezone:{Fore.RESET} {info["timezone"]}
                            """)
                    except Exception:
                        t.print.fail("Unknown IP address.")
                elif (choice == "2" or choice == "02"):
                    misc.iptools.myip()
                elif (choice == "3" or choice == "03"):
                    misc.iptools.randomip()
                elif (choice == "exit" or choice == "x"):
                    t.print.warn("Exiting the Lapidary misc tools...")
                    sleep(0.6)
                    import lapidary
                    return lapidary.core.main()
                            
            except KeyboardInterrupt:
                import lapidary
                            
                print("")
                t.print.warn("Exiting the Lapidary misc tools...")
                sleep(0.6)
                lapidary.core.main()