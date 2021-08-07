import os
import ffmpeg
from pyrogram.types import Message
from pyrogram import filters
from config import Config
from vcbot import vcstatus, app, group_call
import signal




FFMPEG_PROCESSES = {}


@app.on_message(filters.regex("/radio"))
async def radio(client, message : Message):
    msg = await message.reply("Processing...")
    vcstatus["call"] = "radio"

    process = ffmpeg.input(Config.RADIO_URL).output(
            "radio.raw",
            format='s16le',
            acodec='pcm_s16le',
            ac=2,
            ar='48k'
        ).overwrite_output().run_async()

    FFMPEG_PROCESSES[Config.CHAT_ID] = process

    group_call.input_filename = "radio.raw"

    await msg.edit("Radio Started")

@app.on_message(filters.regex("/stopradio"))
async def radio(client, message : Message):
    vcstatus["call"] = "not started"
    process = FFMPEG_PROCESSES.get(Config.CHAT_ID)

    if process:
        process.send_signal(signal.SIGTERM)
    print("FFMPEG")
    group_call.stop_playout()
    #group_call.input_filename = "input.raw"

    await message.reply("Stoped Radio")

