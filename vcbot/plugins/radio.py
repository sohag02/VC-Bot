import ffmpeg
from pyrogram.types import Message
from pyrogram import filters, emoji
from config import Config
from vcbot import vcstatus, app, group_call, is_admin
from helpers import change_vc_title
import signal




FFMPEG_PROCESSES = {}


@app.on_message(filters.regex("/radio"))
@is_admin()
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

    FFMPEG_PROCESSES[message.chat.id] = process

    group_call.input_filename = "radio.raw"
    await change_vc_title(f"Radio | Music 24/7 {emoji.MUSICAL_NOTE}")

    await msg.edit("Radio Started")

@app.on_message(filters.regex("/stopradio"))
@is_admin()
async def radio(client, message : Message):
    if vcstatus["call"] == "radio":
        vcstatus["call"] = "not started"
        process = FFMPEG_PROCESSES.get(message.chat.id)

        if process:
            process.send_signal(signal.SIGTERM)
        print("FFMPEG")
        group_call.stop_playout()

        await message.reply("Stoped Radio")
        await change_vc_title("Dynamic VC Player")
    else:
        await message.reply("Radio is not running")

