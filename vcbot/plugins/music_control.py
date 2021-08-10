from re import S
from pyrogram import filters, emoji
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from vcbot import group_call, app, vcstatus
from vcbot import is_admin
from helpers import change_vc_title



playlist = ["input.raw"]


@group_call.on_network_status_changed
async def on_network_changed(context, is_connected):
    if is_connected:
        # try:
        group_call.input_filename = playlist[0]
        print("Ended : ", playlist[0])
        playlist.pop(0)
        # except:
        #     group_call.input_filename = "input.raw"


@group_call.on_playout_ended
async def on_network_changed(context, is_connected):
    if len(playlist) > 0:
        playlist.pop(0)
        group_call.input_filename = playlist[0]
        print("E playing : ", playlist[0])
        await change_vc_title(group_call.input_filename.replace("songs/", ""))
        
    else:
        if vcstatus["call"] == "radio":
            pass
        # else:
        #     await app.send_message(Config.CHAT_ID, "No song to play in the playlist")


@app.on_message(filters.regex("^/stop$"))
@is_admin()
async def play(client, message : Message):
    group_call.stop_playout()
    await message.reply("Stopped Music!")



@app.on_message(filters.regex("/pause"))
@is_admin()
async def play(client, message : Message):
    if vcstatus['call'] == "paused":
        await message.reply("VC is already paused. Send /resume to resume")
    else:
        group_call.pause_playout()
        vcstatus['call'] = "paused"
        await message.reply("Paused current song. Send /resume to resume")


@app.on_message(filters.regex("/resume"))
@is_admin()
async def play(client, message : Message):
    if vcstatus['call'] == "playing":
        await message.reply("VC is already playing. Send /resume to resume")
    else:
        group_call.resume_playout()
        vcstatus['call'] = "playing"
        await message.reply("Resumed current song. Send /pause to pause")\


@app.on_message(filters.regex("^/playlist$"))
@is_admin()
async def radio(client, message : Message):
    if len(playlist) == 0:
        await message.reply("There are no song in the playlist")
        return

    msg = "The following songs are added in the playlist\n\n"
    count = 0
    for song in playlist:
        count += 1
        s = song.replace("songs/","")
        if song == group_call.input_filename:
            msg += f"{emoji.PLAY_BUTTON}**{count}. {s}**\n\n"
        else:
            msg += f"  **{count}. {s}**\n\n"

    btns = InlineKeyboardMarkup([
        [InlineKeyboardButton(emoji.REPEAT_BUTTON, "repeat"), InlineKeyboardButton(emoji.PLAY_OR_PAUSE_BUTTON, "play_pause"),
        InlineKeyboardButton(emoji.NEXT_TRACK_BUTTON, "skip")]
    ])

    await message.reply(msg, reply_markup=btns)


@app.on_message(filters.regex("^/reload"))
@is_admin()
async def reload(client, message : Message):
    group_call.restart_playout()
    await message.reply("Reloaded File")


@app.on_message(filters.regex("/skip"))
# @app.on_callback_query(filters.regex(emoji.NEXT_TRACK_BUTTON))
@is_admin()
async def skip(client, message : Message):
    playlist.pop(0)
    group_call.input_filename = playlist[0]
    await message.reply("Skipped the current song")

