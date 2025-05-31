# RustAdminBans

## Better Battlemetrics Bans to Discord
This bot gives you the ability to send different types of Battlemetrics ban information to select Discord channels over a web hook. This “bot” does not require a physical bot to be in any Discord, it’s solely operated through web hooks.

This bot uses the Battlemetrics bans API to send newly added bans to Discord through a staff and public embed format. It uses Battlemetrics server IDs to separate each type of ban and where it goes. It also allows you to send specific server bans to specific Discord communities for example.

## Below is a complete setup guide and a showcase:
- https://www.youtube.com/watch?v=ifv9CUJVIzw

### Automatic dependencies installation (recommended)
In a terminal navigate to the install directory and run pip install -r requirements.txt

### Manual dependencies installation
The dependencies needed to get your bot online are stated in the main.py. You can install them using pip install <name>. Here they are now:
- discord.py==2.1.0
- requests==2.25.1
- aiohttp==3.9.5

### Servers.json "useSteamID" variable
This variable is responsible for changing the final embed that is handled in messageHandler.py
Specifically for games like Arma Reforger, we're unable to get any Steam data from the Battlemetrics ban. This means were unable to use the standard embed format that links their Steam profile, and Steam 64 ID.

Setting this variable to False, will mean you will change the "banned_player_profile" variable in your messageHandler.py file.

### For any further support or enquires join:
- [discord.lone.design](https://discord.lone.design/)
- [discord.platformsync.io](https://discord.platformsync.io/)
