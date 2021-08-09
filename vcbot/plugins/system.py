from vcbot import app
from pyrogram import filters
from pyrogram.types import Message
import os
import logging


@app.on_message(filters.regex("/cc"))
async def clear(client, message : Message):
    for f in os.listdir("songs/"):
        os.remove(os.path.join(dir, f))
    logging.info("Cleared files from songs/")
    await message.reply("Cleared unnecessary files")

@app.on_message(filters.regex("/logs"))
async def clear(client, message : Message):
    await message.reply_document("vcbot.logs", caption="Here are the Logs")


@app.on_message(filters.regex("/restaartbot"))
async def restart(client, message : Message):
    await message.reply("Restarting...")
