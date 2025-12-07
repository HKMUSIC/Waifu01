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

# ----- Find next available ID -----
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


# ----- Fetch HD image from waifu.im -----
async def fetch_waifu_image(query):
    url = f"https://api.waifu.im/search?included_tags={query}"

    async with httpx.AsyncClient() as client:
        r = await client.get(url, timeout=30)
        data = r.json()
        return data["images"][0]["url"]


@ZYRO.on_message(filters.command("gupload"))
@require_power("add_character")
async def auto_upload(client, message):

    args = message.text.split()
    if len(args) != 4:
        return await message.reply_text(
            "Use: `/gupload character-name anime-name rarity-number`"
        )

    # ----- Parse inputs -----
    character_name = args[1].replace("-", " ").title()
    anime_name = args[2].replace("-", " ").title()

    try:
        rarity_number = int(args[3])
    except:
        return await message.reply_text("Rarity must be a number.")

    if rarity_number not in rarity_map:
        return await message.reply_text("Invalid rarity number.")

    rarity_text = rarity_map[rarity_number]

    waiting = await message.reply_text("Fetching HD image from waifu.im...")

    # ---- Create query keyword for image search ----
    query = character_name.lower().replace(" ", "%20")

    try:
        # Fetch HD image
        image_url = await fetch_waifu_image(query)
    except:
        await waiting.edit("❌ No image found on waifu.im")
        return

    # Generate ID
    waifu_id = await find_available_id()

    # Create DB object
    character = {
        "name": character_name,
        "anime": anime_name,
        "rarity": rarity_text,
        "rarity_number": rarity_number,
        "id": waifu_id,
        "img_url": image_url,
    }

    # Save to MongoDB
    await collection.insert_one(character)

    # Send to channel
    caption = (
        f"Character Name: {character_name}\n"
        f"Anime: {anime_name}\n"
        f"Rarity: {rarity_text}\n"
        f"ID: {waifu_id}\n"
        f"Added by: [{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    )

    await client.send_photo(
        CHARA_CHANNEL_ID,
        image_url,
        caption=caption,
    )

    await waiting.delete()

    # Final confirmation
    await message.reply_text(
        f"✅ **Character Added Successfully!**\n\n"
        f"**Name:** {character_name}\n"
        f"**Rarity:** {rarity_text}\n"
        f"**ID:** {waifu_id}"
  )
