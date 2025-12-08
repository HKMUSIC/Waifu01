import os
import importlib.util
import random
import time
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from TEAMZYRO import *
from TEAMZYRO.unit.zyro_help import HELP_DATA  

# 🔹 Bot Uptime
START_TIME = time.time()

def get_uptime():
    uptime_seconds = int(time.time() - START_TIME)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"

# -------------------------------------------------------------------------
# 🔹 Generate Private Start Message
# -------------------------------------------------------------------------
async def generate_start_message(client, ctx):
    # ctx may be message or query
    if hasattr(ctx, "message"):
        msg = ctx.message
    else:
        msg = ctx

    bot = await client.get_me()
    bot_name = bot.first_name

    # Handling ping (fallback if ctx has no date)
    try:
        ping = round(time.time() - msg.date.timestamp(), 2)
    except:
        ping = "0.00"

    uptime = get_uptime()

    caption = f"""
🍃 ɢʀᴇᴇᴛɪɴɢs, ɪ'ᴍ <b>{bot_name}</b> 🫧, ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ!
╭━━━━━━━╾❁✦❁╼━━━━━━━╮
⟡ ɪ ᴀᴍ ʏᴏᴜʀ ᴡᴀɪғᴜ ɢᴇɴɪᴇ!  
    sᴜᴍᴍᴏɴ ᴄᴜᴛᴇ ᴡᴀɪғᴜs  
    ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴄʜᴀᴛ ✧

⟡ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ  
    & ᴛᴀᴘ /help ғᴏʀ ᴄᴏᴍᴍᴀɴᴅs
╰━━━━━━━╾❁✦❁╼━━━━━━━╯

➺ <b>Ping:</b> <code>{ping}</code> ms
➺ <b>Uptime:</b> <code>{uptime}</code>
"""

    buttons = [
        [InlineKeyboardButton("⋆ᴀᴅᴅ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ⋆", url=f"https://t.me/{bot.username}?startgroup=true")],
        [
            InlineKeyboardButton("❍sᴜᴘᴘᴏʀᴛ❍", url="https://t.me/GOJO_NOBITA_II"),
            InlineKeyboardButton("❍ᴄʜᴀɴɴᴇʟ❍", url="https://t.me/thedrxnet")
        ],
        [InlineKeyboardButton("⋆ʜᴇʟᴘ⋆", callback_data="open_help")],
        [InlineKeyboardButton("✦ʟᴏʀᴅ✦", url="http://t.me/II_YOUR_GOJO_ll")]
    ]

    return caption, buttons

# -------------------------------------------------------------------------
# 🔹 Generate Group Start Message
# -------------------------------------------------------------------------
async def generate_group_start_message(client):
    bot = await client.get_me()
    caption = f"""🍃 ɪ'ᴍ <b>{bot.first_name}</b> 🫧
ɪ sᴘᴀᴡɴ ᴡᴀɪғᴜs ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ғᴏʀ ᴜsᴇʀs ᴛᴏ ɢʀᴀʙ.
ᴜsᴇ /help ғᴏʀ ᴍᴏʀᴇ ɪɴғᴏ."""

    buttons = [
        [
            InlineKeyboardButton("◦ᴀᴅᴅ ᴍᴇ◦", url=f"https://t.me/{bot.username}?startgroup=true"),
            InlineKeyboardButton("◦sᴜᴘᴘᴏʀᴛ◦", url="https://t.me/+8KU5ZDxvZyw0N2U1"),
        ]
    ]
    return caption, buttons

# -------------------------------------------------------------------------
# 🔹 Start Command — Private Chat
# -------------------------------------------------------------------------
@app.on_message(filters.command("start") & filters.private)
async def start_private(client, message):
    # Save user if new
    existing = await user_collection.find_one({"id": message.from_user.id})
    if not existing:
        await user_collection.insert_one({
            "id": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "start_time": time.time()
        })

    # Send log to GLOG group
    await app.send_message(
        chat_id=GLOG,
        text=f"{message.from_user.mention} Started The Bot.\n"
             f"<b>User ID:</b> <code>{message.from_user.id}</code>\n"
             f"<b>Username:</b> @{message.from_user.username}",
        parse_mode="html"
    )

    caption, buttons = await generate_start_message(client, message)
    media = random.choice(START_MEDIA)

    if media.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        await message.reply_photo(
            photo=media,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="html"
        )
    else:
        await message.reply_video(
            video=media,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="html"
        )

# -------------------------------------------------------------------------
# 🔹 Start Command — Group Chat
# -------------------------------------------------------------------------
@app.on_message(filters.command("start") & filters.group)
async def start_group(client, message):
    caption, buttons = await generate_group_start_message(client)
    media = random.choice(START_MEDIA)

    if media.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        await message.reply_photo(
            photo=media,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="html"
        )
    else:
        await message.reply_video(
            video=media,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="html"
        )

# -------------------------------------------------------------------------
# 🔹 Build Help Menu
# -------------------------------------------------------------------------
def build_help_buttons():
    rows = []
    row = []

    for module_name, data in HELP_DATA.items():
        row.append(InlineKeyboardButton(data.get("HELP_NAME", module_name), callback_data=f"help_{module_name}"))
        if len(row) == 3:
            rows.append(row)
            row = []

    if row:
        rows.append(row)

    return rows

# -------------------------------------------------------------------------
# 🔹 Open Help Menu
# -------------------------------------------------------------------------
@app.on_callback_query(filters.regex("^open_help$"))
async def open_help(client, query):
    await asyncio.sleep(0.3)

    buttons = build_help_buttons()
    buttons.append([InlineKeyboardButton("⬅ Back", callback_data="back_to_home")])

    await query.message.edit_caption(
        "<b>Choose a module to view commands:</b>\n\nAll commands work with: <code>/</code>",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="html"
    )

# -------------------------------------------------------------------------
# 🔹 Individual Help Pages
# -------------------------------------------------------------------------
@app.on_callback_query(filters.regex(r"^help_(.+)"))
async def help_page(client, query):
    await asyncio.sleep(0.3)
    module_name = query.data.split("_", 1)[1]

    data = HELP_DATA.get(module_name, {})
    help_text = data.get("HELP", "No help available for this module.")

    await query.message.edit_caption(
        f"<b>{module_name} Help:</b>\n\n{help_text}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="open_help")]]),
        parse_mode="html"
    )

# -------------------------------------------------------------------------
# 🔹 Back to Home Menu
# -------------------------------------------------------------------------
@app.on_callback_query(filters.regex("^back_to_home$"))
async def back_to_home(client, query):
    await asyncio.sleep(0.3)

    caption, buttons = await generate_start_message(client, query)

    await query.message.edit_caption(
        caption,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="html"
        )
