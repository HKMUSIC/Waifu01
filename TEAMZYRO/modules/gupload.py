import os
import httpx
import asyncio
from pyrogram import filters
from TEAMZYRO import (
    CHARA_CHANNEL_ID,
    collection,
    rarity_map,
    ZYRO,
    require_power
)


# ------- Find next available ID -------
async def find_available_id():
    cursor = collection.find().sort("id", 1)
    ids = []
    async for doc in cursor:
        if "id" in doc:
            try:
                ids.append(int(doc["id"]))
            except:
                continue
    ids.sort()
    for i in range(1, len(ids) + 2):
        if i not in ids:
            return str(i).zfill(2)
    return str(len(ids) + 1).zfill(2)


# ------- Fetch waifu.im image safely -------
async def fetch_waifu_image(query):
    url = f"https://api.waifu.im/search?included_tags={query}"

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.get(url)
            data = r.json()

            if "images" not in data or len(data["images"]) == 0:
                return None

            return data["images"][0]["url"]

    except Exception as e:
        return None


@ZYRO.on_message(filters.command("gupload"))
@require_power("add_character")
async def auto_upload(client, message):

    args = message.text.split()
    if len(args) != 4:
        return await message.reply_text(
            "Use: `/gupload character-name anime-name rarity-number`"
        )

    # Inputs
    character_name = args[1].replace("-", " ").title()
    anime_name = args[2].replace("-", " ").title()

    try:
        rarity_number = int(args[3])
    except:
        return await message.reply_text("Rarity must be a number.")

    if rarity_number not in rarity_map:
        return await message.reply_text("Invalid rarity number.")

    rarity_text = rarity_map[rarity_number]

    waiting = await message.reply_text("⏳ Fetching HD image from waifu.im...")

    query = character_name.lower().replace(" ", "%20")

    # Fetch HD image
    image_url = await fetch_waifu_image(query)

    if not image_url:
        return await waiting.edit("❌ No HD image found for this character.")

    # Create ID
    waifu_id = await find_available_id()

    character = {
        "name": character_name,
        "anime": anime_name,
        "rarity": rarity_text,
        "rarity_number": rarity_number,
        "id": waifu_id,
        "img_url": image_url,
    }

    # Save to DB
    await collection.insert_one(character)

    caption = (
        f"Character Name: {character_name}\n"
        f"Anime: {anime_name}\n"
        f"Rarity: {rarity_text}\n"
        f"ID: {waifu_id}\n"
        f"Added by: [{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    )

    # ---- Safe image send (NO CRASH) ----
    try:
        await client.send_photo(
            CHARA_CHANNEL_ID,
            photo=image_url,
            caption=caption
        )
    except Exception as e:
        await waiting.edit("⚠️ Image could not be sent to channel.\nBut character is saved in DB.")
        return

    await waiting.delete()

    await message.reply_text(
        f"✅ **Character Added Successfully!**\n\n"
        f"**Name:** {character_name}\n"
        f"**Rarity:** {rarity_text}\n"
        f"**ID:** {waifu_id}"
        )
