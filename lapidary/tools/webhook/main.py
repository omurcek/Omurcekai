import requests, base64, os, toml

from util.terminal import *
from colorama      import Fore
from tkinter       import filedialog as fd
from time          import sleep

t = terminal

settings = toml.load('./util/settings.toml')
name = settings['general']['name']

class webhook:    
    def menu():
        print(Center.XCenter(f"""
                    {Fore.MAGENTA}01 »{Fore.RESET} Send Message               {Fore.MAGENTA}04 »{Fore.RESET} Webhook Information        {Fore.MAGENTA}07 »{Fore.RESET} Log Out 
                    {Fore.MAGENTA}02 »{Fore.RESET} Spam Message               {Fore.MAGENTA}05 »{Fore.RESET} Delete Webhook             {Fore.MAGENTA}08 »{Fore.RESET} Menu 
                    {Fore.MAGENTA}03 »{Fore.RESET} Rename Webhook             {Fore.MAGENTA}06 »{Fore.RESET} Change PFP                 {Fore.MAGENTA}09 »{Fore.RESET} Exit 
              """))
    
    def main():
        t.clear()
        t.print.logo("Webhook")
        t.print.info("You can exit webhook tool by typing 'exit'.")
        t.setTitle(f"{name.lower()}@webhooktool:login")
        
        while True:
            while True:
                try:
                    url = input(Colorate.Horizontal(Colors.red_to_purple, f"{name.lower()}@webhook:login → webhook~ "))
                    
                    if (url.lower() == "exit" or url.lower() == "x"):
                        import lapidary
                        return lapidary.core.main()
                    
                    response = requests.get(url)
                    if response.status_code == 200:
                        hook = response.json()
                        t.clear()
                        t.print.logo("Webhook")
                        webhook.menu()
                        webhook_name = hook["name"]
                        t.print.success(f"Logged into webhook: {webhook_name}")
                        break
                    else:
                        t.print.negv(f"Invalid Webhook. ({response.status_code})")
                except KeyboardInterrupt:
                    print("")
                    t.print.warn(f"Exiting the {name.capitalize()} Webhook.")
                    sleep(0.6)
                    import lapidary
                    return lapidary.core.main()
                except Exception:
                    t.print.fail("Invalid Webhook.")
                    
            while True:
                try:
                    t.setTitle(f"{name.lower()}@webhooktool:menu")
                    choice = input(Colorate.Horizontal(Colors.red_to_purple, f'{name.lower()}@webhook:menu → select~ ', 1))
                    
                    if (choice == "1" or choice == "01"):
                        t.setTitle("{name.lower()}@webhooktool:sendmessage")
                        webhook.sendMessage(url)
                    elif (choice == "2" or choice == "02"):
                        t.setTitle("{name.lower()}@webhooktool:spammessage")
                        webhook.spamMessage(url)
                    elif (choice == "3" or choice == "03"):
                        t.setTitle("{name.lower()}@webhooktool:sendmessage")
                        webhook.rename(url)
                    elif (choice == "4" or choice == "04"):
                        t.setTitle("{name.lower()}@webhooktool:webhookinfo")
                        t.clear()
                        t.print.logo("Webhook")
                        webhook.menu()
                        
                        if hook["application_id"]:
                            print(f"{Colorate.Horizontal(Colors.red_to_white, 'Application ID: ', 1)} {format(webhook['application_id'])}\n\n")
                            
                        print(f"""
    {Colorate.Horizontal(Colors.red_to_white, 'Server Information', 1)}
        {Fore.YELLOW}Guild ID:{Fore.RESET} {hook["guild_id"]}
        {Fore.YELLOW}Channel ID:{Fore.RESET} {hook["channel_id"]}

    {Colorate.Horizontal(Colors.red_to_white, 'Webhook Information', 1)}
        {Fore.YELLOW}Token:{Fore.RESET} {hook["token"][:-18] + Colorate.Horizontal(Colors.green_to_white, "****", 1)}
        {Fore.YELLOW}Webhook ID:{Fore.RESET} {hook["id"]}
        {Fore.YELLOW}Name:{Fore.RESET} {hook["name"]}
        {Fore.YELLOW}Type:{Fore.RESET} {hook["type"]}
                            """)
                    elif (choice == "5" or choice == "05"):
                        t.setTitle("discord@webhooktool:deletewebhook")
                        webhook.delete(url)
                        break
                    elif (choice == "6" or choice == "06"):
                        t.setTitle("discord@webhooktool:changepfp")
                        webhook.changePFP(url)
                    elif (choice == "7" or choice == "07"):
                        t.clear()
                        t.print.logo("Webhook")
                        t.print.success("Logged out from the webhook.")
                        break
                    elif (choice == "8" or choice == "08" or choice == "menu"):
                        t.clear()
                        t.print.logo("Webhook")
                        webhook.menu()
                    elif (choice == "exit" or choice == "x" or choice == "9" or choice == "09"):
                        print("")
                        t.print.warn(f"Exiting the {name.capitalize()} Webhook.")
                        sleep(0.7)
                        import lapidary
                        return lapidary.core.main()
                        
                except KeyboardInterrupt:
                    print("")
                    t.print.warn(f"Exiting the {name.capitalize()} Webhook.")
                    sleep(0.7)
                    import lapidary
                    return lapidary.core.main()
                
    def sendMessage(url):
        message = input(Colorate.Horizontal(Colors.red_to_purple, f"{name.lower()}@webhook:sendmessage → message~ ", 1))
        
        try:
            response = requests.post(url, json={"content": message})
            response.raise_for_status()
                
            if (response.status_code == 200 or response.status_code == 204):
                t.clear()
                t.print.logo("Webhook")
                webhook.menu()
                t.print.success(f"Message sent successfully: {message}")
            else:
                t.print.fail(f"An error occured. ({response.status_code})")
                    
        except requests.exceptions.HTTPError as errh:
            t.print.fail(f"HTTP Error: {errh}")

        except requests.exceptions.ConnectionError as errc:
            t.print.fail(f"Error Connecting: {errc}")

        except requests.exceptions.Timeout as errt:
            t.print.fail(f"Timeout Error: {errt}")

        except requests.exceptions.RequestException as err:
            t.print.fail(f"Request Exception: {err}")
            
    def spamMessage(url):
        message = input(Colorate.Horizontal(Colors.red_to_purple, f"{name.lower()}@spammessage → message~ ", 1))
        ratelimit = int(input(Colorate.Horizontal(Colors.red_to_purple, f"{name.lower()}@rename → timeout~ ")))
        
        while True:                            
            try:
                response = requests.post(url, json={"content": message})
                response.raise_for_status()
                    
                if (response.status_code == 200 or response.status_code == 204):
                    t.print.success(f"Message sent successfully: {message}")
                elif (response.status_code == 429):
                    t.print.warn(f"Recieved ratelimit, waiting {ratelimit} seconds.")
                    sleep(ratelimit)
                else:
                    t.print.fail(f"An error occured. ({response.status_code})")
                        
            except requests.exceptions.HTTPError as errh:
                t.print.warn(f"Recieved ratelimit, waiting {ratelimit} seconds.")
                sleep(ratelimit)
                # negv(f"HTTP Error: {errh}")

            except requests.exceptions.ConnectionError as errc:
                t.print.fail(f"Error Connecting: {errc}")

            except requests.exceptions.Timeout as errt:
                t.print.fail(f"Timeout Error: {errt}")

            except requests.exceptions.RequestException as err:
                t.print.fail(f"Request Exception: {err}")
                
            except KeyboardInterrupt:
                print("")
                t.print.warn(f"Exiting the {name.capitalize()} webhook spammer...")
                sleep(0.7)
                return webhook.main()
            
    def rename(url):
        name = input(Colorate.Horizontal(Colors.red_to_purple, f"{name.lower()}@webhook:rename → name~ "))
        
        try:
            response = requests.patch(url, json={"name": name})
            response.raise_for_status()
            
            if (response.status_code == 200):
                t.clear()
                t.print.logo("Webhook")
                webhook.menu()
                t.print.success(f"Webhook name changed successfully: {name}")
            else:
                t.print.fail(f"An error occured. ({response.status_code})")

        except requests.exceptions.HTTPError as errh:
            t.print.fail(f"HTTP Error: {errh}")

        except requests.exceptions.ConnectionError as errc:
            t.print.fail(f"Error Connecting: {errc}")

        except requests.exceptions.Timeout as errt:
            t.print.fail(f"Timeout Error: {errt}")

        except requests.exceptions.RequestException as err:
            t.print.fail(f"Request Exception: {err}")
            
    def delete(url):    
        try:
            response = requests.delete(url)
            response.raise_for_status()
                
            if (response.status_code == 200 or response.status_code == 204):
                t.clear()
                t.print.logo("Webhook")
                t.print.success(f"Webhook deleted successfully.")
            else:
                t.print.fail(f"An error occured. ({response.status_code})")
            
        except requests.exceptions.HTTPError as errh:
            t.print.fail(f"HTTP Error: {errh}")

        except requests.exceptions.ConnectionError as errc:
            t.print.fail(f"Error Connecting: {errc}")

        except requests.exceptions.Timeout as errt:
            t.print.fail(f"Timeout Error: {errt}")

        except requests.exceptions.RequestException as err:
            t.print.fail(f"Request Exception: {err}")
    
    def changePFP(url):
        t.print.warn(f"Press enter to select file or skip this to input the PATH/URL")
        image_path = fd.askopenfilename(filetypes=[("Profile Pictures", "*.png;*.jpg;*.jpeg")])
        if image_path is None or image_path == "":
            image_path = input(Colorate.Horizontal(Colors.red_to_purple, f"{name.lower()}@changepfp → path/url~ "))
        
        try:
            if image_path.startswith(('http://', 'https://')):
                response = requests.get(image_path)
                response.raise_for_status()
                encoded_image = base64.b64encode(response.content).decode('utf-8')
            else:
                if not os.path.exists(image_path):
                    t.clear()
                    t.print.logo("Webhook")
                    webhook.menu()
                    return t.print.fail("No such a file or directory.")
                
                with open(image_path, "rb") as image_file:
                    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

            data = {
                "avatar": f"data:image/jpeg;base64,{encoded_image}"
            }
            
            response = requests.patch(url, json=data)
            response.raise_for_status()
            
            if (response.status_code == 200):
                t.clear()
                t.print.logo("Webhook")
                webhook.menu()
                t.print.success(f"Profile picture changed successfully.")
            else:
                t.print.fail(f"An error occured. ({response.status_code})")
            
        except requests.exceptions.HTTPError as errh:
            t.print.fail(f"HTTP Error: {errh}")

        except requests.exceptions.ConnectionError as errc:
            t.print.fail(f"Error Connecting: {errc}")

        except requests.exceptions.Timeout as errt:
            t.print.fail(f"Timeout Error: {errt}")

        except requests.exceptions.RequestException as err:
            t.print.fail(f"Request Exception: {err}")