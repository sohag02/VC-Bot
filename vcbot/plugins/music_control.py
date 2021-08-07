from pyrogram import filters
from pyrogram.types import Message
from vcbot import group_call, app, vcstatus
from youtubesearchpython import VideosSearch
from vcbot import is_admin
from vcbot.helpers import *
from config import Config
from youtubesearchpython import VideosSearch



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
        
    else:
        if vcstatus["call"] == "radio":
            pass
        else:
            await app.send_message(Config.CHAT_ID, "No song to play in the playlist")



@app.on_message(filters.regex("/pause"))
@is_admin()
async def play(client, message : Message):
    if vcstatus['call'] == "paused":
        await message.reply("VC is already paused. Send /resume to resume")
    elif vcstatus['call'] == "not started":
        await message.reply("VC not started yet")
    else:
        group_call.pause_playout()
        vcstatus['call'] = "paused"
        await message.reply("Paused current song. Send /resume to resume")


@app.on_message(filters.regex("/resume"))
@is_admin()
async def play(client, message : Message):
    if vcstatus['call'] == "playing":
        await message.reply("VC is already playing. Send /resume to resume")
    elif vcstatus['call'] == "not started":
        await message.reply("VC not started yet")
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
        msg += f"{count}. {song}\n\n" 

    await message.reply(msg)


@app.on_message(filters.regex("^/play"))
@is_admin()
async def play(client, message : Message):
    if vcstatus["call"] == "radio":
        group_call.stop_playout()
        await message.reply("Radio Stoped!")

    # if vcstatus["call"] == "not started":
    #     await group_call.start(Config.CHAT_ID)
        
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

        if "www.youtube.com" in link:
            await msg.edit("Downloading...")
            file, title, length = await run_async(download_and_transcode, link) #download_and_transcode(link)
            if len(playlist) > 0:
                playlist.append(file)
                print(file)
            elif len(playlist) == 0:
                playlist.append(file)
                group_call.input_filename = file
                print("playing : ", file)

            pos = playlist.index(file)
            await msg.delete()
            await message.reply(f"Added to playlist at no. {pos + 1}!")
            print("\n" + file)
        else:
            src = VideosSearch(link, limit=1)
            await msg.edit("Downloading...")
            u = "https://www.youtube.com/watch?v=" + src.result()['result'][0]['id']
            file, title, length = await run_async(download_and_transcode, u, message)
            if len(playlist) > 0:
                playlist.append(file)
                print(file)
            elif len(playlist) == 0:
                playlist.append(file)
                group_call.input_filename = file
                print("\nplaying : ", file)
                
            pos = playlist.index(file)
            await msg.delete()
            await message.reply(f"Added to playlist at no. {pos + 1}!")
            print("\n" + file)

    else:
        msg = await message.reply("Downloading...")
        path = message.reply_to_message.download("song.mp3")

        file = run_async(transcode, path)
        if len(playlist) > 0:
                playlist.append(file)
                print(file)
        elif len(playlist) == 0:
            playlist.append(file)
            group_call.input_filename = file
            print("\nplaying : ", file)
                
        pos = playlist.index(file)
        await msg.edit(f"Added to playlist at no. {pos + 1}!")
        print("\n" + file)


@app.on_message(filters.regex("/skip"))
@is_admin()
async def skip(client, message : Message):
    playlist.pop(0)
    group_call.input_filename = playlist[0]
    await message.reply("Skipped the current song")

