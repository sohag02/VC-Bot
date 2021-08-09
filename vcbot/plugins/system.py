from vcbot import app
from pyrogram import filters
from pyrogram.types import Message
import os
import logging


@app.on_message(filters.regex("/cc"))
async def clear(client, message : Message):
    if message.from_user.username == "Sohag02":
        for f in os.listdir("songs/"):
            os.remove(f"songs/{f}")
        logging.info("Cleared files from songs/")
        await message.reply("Cleared unnecessary files")
    else:
        await message.reply("This command is not for You")

@app.on_message(filters.regex("/logs"))
async def clear(client, message : Message):
    if message.from_user.username == "Sohag02":
        await message.reply_document("vcbot.logs", caption="Here are the Logs")
    else:
        await message.reply("This command is not for You")
        await app.send_message("Sohag02", f"#StrangerLogRequest\n@{message.chat.username}, @{message.from_user.username}")

def restart():
        import sys
        print("argv was",sys.argv)
        print("sys.executable was", sys.executable)
        print("restart now")

        import os
        os.execv(sys.executable, ['python'] + sys.argv)

@app.on_message(filters.regex("/restaartbot"))
async def restart(client, message : Message):
    if message.from_user.username == "Sohag02":
        await message.reply("Restarting...")
        os.system("python3 -m vcbot")
        print("Restarting...")
        logging.info("Restarting...")
        app.edit_message_text()
        exit()
    else:
        await message.reply("This command is not for You")