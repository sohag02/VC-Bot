from vcbot import app, group_call, vcstatus
from .music_control import playlist
from pyrogram.types import CallbackQuery
from pyrogram import filters, emoji



@app.on_callback_query(filters.regex("skip"))
async def controls(client, query : CallbackQuery):
    playlist.pop(0)
    group_call.input_filename = playlist[0]
    await query.answer("Skipped the current song")


@app.on_callback_query(filters.regex("play_pause"))
async def controls(client, query : CallbackQuery):
    if vcstatus["call"] == "paused":
        msg = query.message.text.markdown
        await query.edit_message_caption(msg.replace(emoji.PAUSE_BUTTON, emoji.PLAY_BUTTON))
        await group_call.resume_playout()
        vcstatus["call"] = "playing"
        await query.answer("Resumed")
    elif vcstatus["call"] == "playing":
        msg = query.message.text.markdown
        await query.edit_message_caption(msg.replace(emoji.PLAY_BUTTON, emoji.PAUSE_BUTTON))
        await group_call.pause_playout()
        vcstatus["call"] = "paused"
        await query.answer("Paused")

@app.on_callback_query(filters.regex("repeat"))
async def controls(client, query : CallbackQuery):
    await group_call.restart_playout()
    await query.answer("Reapeating the current song")
