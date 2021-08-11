from vcbot import app, group_call, is_admin
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters, emoji


@app.on_message(filters.regex("^/volume"))
@is_admin()
async def volume(client, message : Message):
    try:
        v = message.text.replace("/volume ", "")
    except:
        await message.reply("Provide a value b/w 1-200")
        return
    group_call.set_my_volume(v)
    await message.reply(f"Volume set to {v}")
#     await message.reply("**Volume Control**",
#                             reply_markup=InlineKeyboardMarkup([
#                                 [InlineKeyboardButton(emoji.PLUS, "volume_increase"), InlineKeyboardButton(emoji.MINUS), "volume_decrease"]
#                             ])
#                         )


# @app.on_callback_query(filters.regex("volume_increase"))
# async def vol(client, message : Message):
#     group_call.set_my_volume()
