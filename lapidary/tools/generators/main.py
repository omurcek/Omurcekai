import requests, string, random, toml

from util.terminal import *
from colorama      import Fore
from time          import sleep

t = terminal

settings = toml.load('./util/settings.toml')
name = settings['general']['name']

class generator():
    class nitro():
        def random_string(length):
            characters = string.ascii_letters + string.digits
            random_string = ''.join(random.choice(characters) for _ in range(length))
            return random_string
        
        successful_requests = 0
        total_requests = 0
            
        def update_title():
            t.setTitle(f"{name.lower()}@generator - Unvalid Codes: {generator.nitro.total_requests - generator.nitro.successful_requests} | Valid Codes: {generator.nitro.successful_requests}")
        
    def menu():
        print(Center.XCenter(f"""
{Fore.MAGENTA}01 »{Fore.RESET} Nitro Generator
              """))
    
    def main():
        t.clear()
        t.print.logo("Generator")
        t.setTitle(f"{name.lower()}@generator:menu")
        generator.menu()
        # t.print.info("You can exit generator tool by typing 'exit'.")
        
        while True:
            try:
                choice = input(Colorate.Horizontal(Colors.red_to_purple, f"{name.lower()}@generators:menu → select~ ", 1))
                
                if (choice == "1" or choice == "01"):
                    t.setTitle(f"{name.lower()}@generator:nitro")
                    t.clear()
                    t.print.logo("Generator")
                    t.print.info("You can exit nitro generator tool by pressing CTRL + C.")
                    
                    webhook = input(Colorate.Horizontal(Colors.red_to_purple, f"{name.lower()}@generator:nitro → webhook~ ", 1))
                    timeout = int(input(Colorate.Horizontal(Colors.red_to_purple, f"{name.lower()}@generator:nitro → timeout~ ", 1)))
                    
                    while True:
                        try:
                            code = generator.nitro.random_string(24)
                            url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
                            generator.nitro.total_requests += 1
                            
                            response = requests.get(url)
                            if response.status_code == 200:
                                generator.nitro.successful_requests += 1
                                t.print.success(f"VALID NITRO CODE FOUND: {code}")
                                
                                try:
                                    response = requests.post(webhook, json={"content": f"**@everyone :white_check_mark: VALID NITRO CODE FOUND:** discord.gift/{code}"})
                                    response.raise_for_status()
                                            
                                except Exception:
                                    with open("valid_nitro_codes.txt", "a") as file:
                                        file.write(f"{code}\n")
                                    
                            elif response.status_code == 429:
                                t.print.fail(f"Code invalid: {code}")
                                t.print.warn(f"Rate limit hit, waiting {timeout} seconds")
                                sleep(timeout)
                            else:
                                t.print.fail(f"Code invalid: {code}")
                            
                            generator.nitro.update_title()
                        except KeyboardInterrupt:
                            t.print.warn(f"Exiting the {name.capitalize()} nitro generator...")
                            sleep(0.8)
                            generator.main()
                            break
                elif (choice == "exit" or choice == "x"):
                    import lapidary
                    t.print.warn(f"Exiting the {name.capitalize()} generators...")
                    sleep(0.7)
                    lapidary.core.main()
            except KeyboardInterrupt:
                import lapidary
                print()
                t.print.warn(f"Exiting the {name.capitalize()} generators...")
                sleep(0.7)
                lapidary.core.main()