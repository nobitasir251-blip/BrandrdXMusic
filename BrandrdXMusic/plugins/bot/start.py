```python id="j9d3la"
import os
import time
import asyncio

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from BrandrdXMusic import app
from BrandrdXMusic.misc import _boot_
from BrandrdXMusic.plugins.sudo.sudoers import sudoers_list
from BrandrdXMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from BrandrdXMusic.utils.decorators.language import LanguageStart
from BrandrdXMusic.utils.formatters import get_readable_time
from BrandrdXMusic.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string


@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)

    try:
        await message.react("❤")
    except:
        pass

    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]

        if name.startswith("help"):
            keyboard = help_pannel(_)

            try:
                await message.reply_sticker(
                    "CAACAgUAAxkBAAEQI1RlTLnRAy4h9lOS6jgS5FYsQoruOAAC1gMAAg6ryVcldUr_lhPexzME"
                )
            except:
                pass

            return await message.reply_photo(
                photo=config.START_IMG_URL,
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )

        if name.startswith("sud"):
            await sudoers_list(client=client, message=message, _=_)

            if await is_on_off(2):
                await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"""
{message.from_user.mention} checked sudo list.

User ID : {message.from_user.id}
Username : @{message.from_user.username}
""",
                )
            return

        if name.startswith("inf"):
            m = await message.reply_text("🔎")

            try:
                query = name.replace("info_", "", 1)
                query = f"https://www.youtube.com/watch?v={query}"

                results = VideosSearch(query, limit=1)

                for result in (await results.next())["result"]:
                    title = result["title"]
                    duration = result["duration"]
                    views = result["viewCount"]["short"]
                    thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                    channellink = result["channel"]["link"]
                    channel = result["channel"]["name"]
                    link = result["link"]
                    published = result["publishedTime"]

                searched_text = _["start_6"].format(
                    title,
                    duration,
                    views,
                    published,
                    channellink,
                    channel,
                    app.mention,
                )

                key = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text=_["S_B_8"],
                                url=link,
                            ),
                            InlineKeyboardButton(
                                text=_["S_B_9"],
                                url=config.SUPPORT_CHAT,
                            ),
                        ]
                    ]
                )

                await m.delete()

                await app.send_photo(
                    chat_id=message.chat.id,
                    photo=thumbnail,
                    caption=searched_text,
                    reply_markup=key,
                )

            except Exception as e:
                await m.edit_text(f"Error : {e}")

            return

    out = private_panel(_)

    try:
        lol = await message.reply_text(
            f"Welcome Baby {message.from_user.mention} ❣️"
        )

        texts = [
            "🥳",
            "💥",
            "🤩",
            "💌",
            "💞",
        ]

        for emoji in texts:
            await asyncio.sleep(0.3)
            await lol.edit_text(
                f"Welcome Baby {message.from_user.mention} {emoji}"
            )

        await asyncio.sleep(0.5)
        await lol.delete()

    except:
        pass

    try:
        lols = await message.reply_text("⚡")

        for txt in [
            "⚡s",
            "⚡st",
            "⚡sta",
            "⚡star",
            "⚡start",
            "⚡starti",
            "⚡startin",
            "⚡starting",
        ]:
            await asyncio.sleep(0.1)
            await lols.edit_text(txt)

    except:
        pass

    try:
        m = await message.reply_sticker(
            "CAACAgUAAxkBAAEQI1BlTLmx7PtOO3aPNshEU2gCy7iAFgACNQUAApqMuVeA6eJ50VbvmDME"
        )
    except:
        m = None

    try:
        if message.chat.photo:
            userss_photo = await app.download_media(
                message.chat.photo.big_file_id
            )

            if userss_photo and os.path.exists(userss_photo):
                chat_photo = userss_photo
            else:
                chat_photo = config.START_IMG_URL
        else:
            chat_photo = config.START_IMG_URL

    except:
        chat_photo = config.START_IMG_URL

    try:
        await lols.delete()
    except:
        pass

    try:
        if m:
            await m.delete()
    except:
        pass

    await message.reply_photo(
        photo=chat_photo,
        caption=_["start_2"].format(
            message.from_user.mention,
            app.mention,
        ),
        reply_markup=InlineKeyboardMarkup(out),
    )

    if await is_on_off(config.LOG):
        sender_id = message.from_user.id
        sender_name = message.from_user.first_name

        await app.send_message(
            config.LOG_GROUP_ID,
            f"""
{message.from_user.mention} has started bot.

User ID : {sender_id}
User Name : {sender_name}
""",
        )


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)

    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=_["start_1"].format(
            app.mention,
            get_readable_time(uptime),
        ),
        reply_markup=InlineKeyboardMarkup(out),
    )

    return await add_served_chat(message.chat.id)


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)

            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass

            if member.id == app.id:

                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)

                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )

                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)

                await message.reply_photo(
                    photo=config.START_IMG_URL,
                    caption=_["start_3"].format(
                        message.from_user.first_name,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )

                await add_served_chat(message.chat.id)

                await message.stop_propagation()

        except Exception as ex:
            print(ex)
```
