from pyrogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from youtubesearchpython.__future__ import VideosSearch
from vcbot import app


@app.on_inline_query()
async def search(client, InlineQuery : InlineQuery):
    ans = []
    blank = InlineQueryResultArticle(
                    title="Dynamic VC Player",
                    description="Enter any Song name to search and download",
                    input_message_content=InputTextMessageContent(
                        ("**This is Dynamic Vc Player Bot**\n\n"
                        "Enter any song name to search")
                        ),
                    thumb_url="https://telegra.ph/file/5a451086a26b8eff9f201.jpg"
                )
    query = InlineQuery.query
    if query == "":
        await app.answer_inline_query(
            InlineQuery.id,
            results=[blank],
            switch_pm_text=("Search a youtube video"),
            switch_pm_parameter="help",
            cache_time=0
        )
    else:
        string = query.lower()
        src = VideosSearch(string)
        vidoes = await src.next()
        for v in vidoes["result"]:
        #for v in vidoes:
            ans.append(
                InlineQueryResultArticle(
                    title=v["title"],
                    description=("Duration: {} Views: {}").format(
                        v["duration"],
                        v["viewCount"]["short"]
                    ),
                    input_message_content=InputTextMessageContent(
                        "/play https://www.youtube.com/watch?v={} ".format(
                            v["id"]
                        )
                    ),
                    thumb_url=v["thumbnails"][0]["url"]
                )
            )
        await app.answer_inline_query(
        InlineQuery.id,
        results=ans,
        switch_pm_text=("Search Results"),
        switch_pm_parameter="help",
        cache_time=0
        )