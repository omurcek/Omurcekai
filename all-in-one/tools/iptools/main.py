import requests, random, sys, socket, toml

from util.terminal import *
from datetime      import datetime
from colorama      import Fore
from time          import sleep

t = terminal

settings = toml.load('./util/settings.toml')
name = settings['general']['name']

class iptools:    
    class tools:
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
        
        def portscanner(ip):
            t.print.info(f"Target IP: {ip}")
            t.print.info(f"Scanning started at: {str(datetime.now())}")
            print("")
            
            try:
                for port in range (1, 65535):
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socket.setdefaulttimeout(0.5)
                    
                    result = s.connect_ex((ip, port))
                    if result == 0:
                        t.print.success(f"Port {port} is open.")
                    s.close()
            except KeyboardInterrupt:
                t.print.warn("Exiting port scanner.")
                return iptools.main()
            except socket.error:
                t.print.fail("Host not responding, exiting port scanner.")
                return iptools.main()
        
    def menu():
        print(Center.XCenter(f"""
                {Fore.MAGENTA}01 »{Fore.RESET} IP Info          {Fore.MAGENTA}04 »{Fore.RESET} Port Scanner
                {Fore.MAGENTA}02 »{Fore.RESET} My IP
                {Fore.MAGENTA}03 »{Fore.RESET} Random IP
              """))
    
    def main():
        t.clear()
        t.print.logo("IP TOOLS")
        t.setTitle(f"{name.lower()}@iptools:menu")
        iptools.menu()
        
        while True:
            try: 
                choice = input(Colorate.Horizontal(Colors.red_to_purple, f"{name.lower()}@iptools:menu → select~ ", 1))
                
                if choice in ["1", "01"]:
                    ip = input(Colorate.Horizontal(Colors.red_to_purple, f"{name.lower()}@iptools:ipinfo → ip~ ", 1))
                    
                    try:
                        info = iptools.tools.ipinfo(ip)
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
                elif choice in ["2", "02"]:
                    iptools.tools.myip()
                elif choice in ["3", "03"]:
                    iptools.tools.randomip()
                elif choice in ["4", "04"]:
                    ip = input(Colorate.Horizontal(Colors.red_to_purple, f"{name.lower()}@iptools:portscanner → ip~ ", 1))
                    
                    iptools.tools.portscanner(ip)
                elif choice in ["exit", "x"]:
                    t.print.warn(f"Exiting the {name.capitalize()} IP tools...")
                    sleep(0.6)
                    import lapidary
                    return lapidary.core.main()
                            
            except KeyboardInterrupt:
                import lapidary
                            
                print("")
                t.print.warn(f"Exiting the {name.capitalize()} IP tools...")
                sleep(0.6)
                lapidary.core.main()