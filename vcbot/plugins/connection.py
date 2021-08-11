from pyrogram import filters
from pyrogram.types import Message
from pyrogram.raw.functions.phone import CreateGroupCall
from pyrogram.raw.types import InputPeerChannel
from vcbot import group_call, app, vcstatus, is_admin, player
from vcbot.plugins.radio import FFMPEG_PROCESSES
import signal
import logging


@app.on_message(filters.regex('^/join$'))
@is_admin()
async def join_handler(_, message : Message):
    print("Joined")
    try:
        await group_call.start(message.chat.id)
    except:
        try:
            peer = await player.resolve_peer(message.chat.id)
            data = CreateGroupCall(
                peer=InputPeerChannel(
                    channel_id=peer.channel_id,
                    access_hash=peer.access_hash,
                ),
                random_id=app.rnd_id() // 9000000000,
            )
            await player.send(data)
            await group_call.start(message.chat.id)
        except Exception as e:
            await message.reply(e)
            await message.reply("Please make me admin with manage voice chat permissions "
                                "or start voice chat manually and then use /join")
            return
    
    await app.send_message(message.chat.id ,"Successfully joined VC!", reply_to_message_id=message.message_id)
    logging.info(f"Joined VC : @{message.chat.username}")

@app.on_message(filters.regex("/disconectvc"))
@is_admin()
async def leave_handler(_, message : Message):
    await group_call.leave_current_group_call()
    if vcstatus["call"] == "radio":
        process = FFMPEG_PROCESSES.get(message.chat.id)
        if process:
            process.send_signal(signal.SIGTERM)

    await message.reply("Disconnected from voice chat..")
    logging.info(f"Disconected VC : @{message.chat.username}")