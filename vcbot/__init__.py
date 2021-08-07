from pyrogram import Client
from pyrogram.types import Message
from config import Config
from pytgcalls import GroupCallFactory
import os

vcstatus = {"call" : "Not started"}

if os.path.exists("songs/") == True:
    print("Download Path Exist")
else:
    os.mkdir("songs")
    print("Download Path Created")


def is_admin():
    
    def decorator(func):

        async def wrapped(client, message : Message):
            
            user = await app.get_chat_member(Config.CHAT_ID, message.from_user.id)
            if user.status in ['creator', 'administrator'] and message.chat.type not in ["private"]:
                await func(client, message)
            else:
                await message.reply("You are not a Admin")

        return wrapped
    return decorator

app = Client(
    'vc-bot',
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

player = Client('pytgcalls', api_id=Config.PLAYER_API_ID, api_hash=Config.PLAYER_API_HASH)

group_call = GroupCallFactory(player).get_file_group_call('input.raw')

