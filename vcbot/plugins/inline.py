from pyrogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from pyrogram.types.inline_mode.inline_query_result import InlineQueryResult
from youtubesearchpython import VideosSearch
from vcbot import app

@app.on_inline_query()
async def search(client, InlineQuery : InlineQuery):
    ans = []
    query = InlineQuery.query
    if query == "":
        ans.append(
             InlineQueryResultArticle("Search Song", InputTextMessageContent("Search any song"))
         )
        await app.answer_inline_query(
            InlineQuery.id,
            results=ans,
            switch_pm_text=("Search a youtube video"),
            switch_pm_parameter="help",
            cache_time=0
        )
    else:
        string = query.lower()
        src = VideosSearch(string)
        for v in src.result()["result"]:
            ans.append(
                InlineQueryResultArticle(
                    title=v["title"],
                    description=("Duration: {} Views: {}").format(
                        v["duration"],
                        v["viewCount"]["short"]
                    ),
                    input_message_content=InputTextMessageContent(
                        "/song https://www.youtube.com/watch?v={} ".format(
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