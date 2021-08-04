from pyrogram import filters
from pyrogram import emoji
from pyrogram.types import Message
from vcbot import group_call, app, vcstatus, player
import pafy
import wget
from youtubesearchpython import VideosSearch
from pyrogram.utils import MAX_CHANNEL_ID
import ffmpeg
import os
from gtts import gTTS
from io import BytesIO
import pydub
from vcbot import transcode, download_and_transcode, download_song
from config import Config
from youtubesearchpython import VideosSearch



playlist = ["input.raw"]


@group_call.on_network_status_changed
async def on_network_changed(context, is_connected):
    if is_connected:
        # try:
        group_call.input_filename = playlist[0]
        print("Ended : ", )
        playlist.pop(0)
        # except:
        #     group_call.input_filename = "input.raw"


@group_call.on_playout_ended
async def on_network_changed(context, is_connected):
    if len(playlist) > 0:
        playlist.pop(0)
        group_call.input_filename = playlist[0]
        print("playing : ", playlist[0])
        
    else:
        await app.send_message(Config.CHAT_ID, "No song to play in the playlist")


@app.on_message(filters.regex("/pause"))
async def play(client, message : Message):
    if vcstatus['call'] == "paused":
        await message.reply("VC is already paused. Send /resume to resume")
    else:
        group_call.pause_playout()
        vcstatus['call'] = "paused"
        await message.reply("Paused current song. Send /resume to resume")

@app.on_message(filters.regex("/resume"))
async def play(client, message : Message):
    if vcstatus['call'] == "playing":
        await message.reply("VC is already playing. Send /resume to resume")
    else:
        group_call.resume_playout()
        vcstatus['call'] = "playing"
        await message.reply("Resumed current song. Send /pause to pause")\


# @group_call.on_network_status_changed
# async def on_network_changed(context, is_connected):
#     chat_id = MAX_CHANNEL_ID - context.full_chat.id
#     if is_connected:
#         group_call

@app.on_message(filters.regex("^/playlist$"))
async def radio(client, message : Message):
    if len(playlist) == 0:
        await message.reply("There are no song in the playlist")
        return

    msg = "The following songs are added in the playlist\n\n"
    count = 0
    for song in playlist:
        count += 1
        msg += f"{count}. {song}\n" 

    await message.reply(msg)


@app.on_message(filters.regex("^/play"))
async def play(client, message : Message):
    if message.reply_to_message:
        service = "telegram"
    else:
        service = "youtube"
    if service == "youtube":
        msg = await message.reply("Searching...")
        try:
            link = message.text.replace("/play", "")
        except:
            await message.edit("Provide a valid url or song name to play or reply to a file")
            return

        if "youtube" in link:
            await msg.edit("Downloading...")
            file, title, length = download_and_transcode(link)
            if len(playlist) > 0:
                playlist.append(file)
                print(file)
            elif len(playlist) == 0:
                playlist.append(file)
                group_call.input_filename = file
                print("playing : ", file)

            pos = playlist.index(file)
            await msg.edit(f"Added to playlist at no. {pos}!")
            print("\n" + file)
        else:
            src = VideosSearch(link, limit=1)
            await msg.edit("Downloading...")
            u = "https://www.youtube.com/watch?v=" + src.result()['result'][0]['id']
            file, title, length = download_and_transcode(u)
            if len(playlist) > 0:
                playlist.append(file)
                print(file)
            elif len(playlist) == 0:
                playlist.append(file)
                group_call.input_filename = file
                print("\nplaying : ", file)
                
            pos = playlist.index(file)
            await msg.edit(f"Added to playlist at no. {pos}!")
            print("\n" + file)

            
            
    # if message.reply_to_message:
    #     if message.reply_to_message.audio:
    #         path = await message.download()
    #         playlist.append(path)
    #         return
    #     else:
    #         await message.reply("Please reply to a audio file to play")
    #         return
    
    # to_play = message.text.replace("/play", "")
    # msg = await message.reply("Searching...")

    # search = VideosSearch(to_play, limit=1)
    # link = "https://www.youtube.com/watch?v=" + search.result()['result'][0]['id']
    # print(link)
    # video = pafy.new(link)
    # audio = video.getbestaudio()
    # await msg.edit("Downloading...")
    # path = wget.download(audio.url, out = "song" + ".webm")
    # playlist.append(path)
    # await msg.edit("Added to queue...")
    # print(playlist)
    # # print(search.result())
    # # for vid in search.result()['results']:
        
    # #print(search)


@app.on_message(filters.regex("/skip"))
async def skip(client, message : Message):
    """Skip the currently playing song"""
    playlist.pop(0)
    group_call.input_filename = playlist[1]
    await message.reply("Skipped the current song")

