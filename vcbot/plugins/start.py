from vcbot import app
from pyrogram import filters
from pyrogram.types import Message


@app.on_message(filters.regex("/start"))
async def start(client, message : Message):
    await message.reply("""
**🎶 Dynamic VC Player Bot 🎶
▬▬▬▬▬▬▬▬▬▬▬▬▬▬
Coded in Pyrogram & pytgcalls. 
It will itself search Your Req. 
Music & Play it on Voice Chat.
You Can Even Go inline mode
to get your own desired song.
▬▬▬▬▬▬▬▬▬▬▬▬▬▬
To Get To Know About The Bot
Commands & Description:- /help
[To Be Accessed By Grp Admins]
▬▬▬▬▬▬▬▬▬▬▬▬▬▬
💝Join: @TheDynamicSupport
🤖Bot By: @TheDynamicNetwork**""")


@app.on_message(filters.regex("/help"))
async def start(client, message : Message):
    await message.reply("""**🎶 Dynamic VC Player Bot 🎶
▬▬▬▬▬▬▬▬▬▬▬▬▬▬
🌀Bot Help & Commands:-
👉🏻 `/Start` 
- Starts Or Restarts The Bot

👉🏻 `/join`
- Bot Joins The Voice Chat 

👉🏻 `/play` <Song Name / YouTube link / Reply To File>
- Plays The Requested Song

👉🏻 `/playlist` 
- Sends The Current Playlist

👉🏻 `/skip` 
- Skips A Song In Playlist 

👉🏻 `/disconnectvc`
- Bot gets Disconnects from VC

👉🏻 `/radio`
- Plays Random Songs 

👉🏻 `/stopradio`
- Stops Playing Random Songs
▬▬▬▬▬▬▬▬▬▬▬▬▬▬
💝Join: @TheDynamicSupport
🤖Bot By: @TheDynamicNetwork**""")
