from pyrogram import filters
from pyrogram.types import Message
from pyrogram.raw.functions.phone import CreateGroupCall
from pyrogram.raw.types import InputPeerChannel
from vcbot import player, group_call, app


@player.on_message(filters.regex('/join'))
async def join_handler(_, message : Message):
    print("Joined")
    try:
        await group_call.start(message.chat.id)
    except:
        peer = await app.resolve_peer(message.chat.id)
        CreateGroupCall(
            peer=InputPeerChannel(
                channel_id=peer.channel_id,
                access_hash=peer.access_hash,
            ),
            random_id=app.rnd_id() // 9000000000,
        )
        await group_call.start(message.chat.id)
    # await message.reply("Successfully joined VC!")
    await app.send_message(message.chat.id ,"Successfully joined VC!", reply_to_message_id=message.message_id)

@player.on_message(filters.regex("/d"))
async def leave_handler(_, message : Message):
    await group_call.leave_current_group_call()
    await app.send_message(message.chat.id ,"Disconnected from voice chat..", reply_to_message_id=message.message_id)