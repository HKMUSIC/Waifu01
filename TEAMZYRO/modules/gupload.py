import httpx
from pyrogram import filters
from TEAMZYRO import (
    app,
    CHARA_CHANNEL_ID,
    collection,
    rarity_map,
    require_power
)

# ---------------- ID GENERATOR ----------------
async def find_available_id():
    cursor = collection.find().sort("id", 1)
    ids = []
    async for doc in cursor:
        if "id" in doc:
            try:
                ids.append(int(doc["id"]))
            except:
                pass

    ids.sort()
    for i in range(1, len(ids) + 2):
        if i not in ids:
            return str(i).zfill(2)

    return str(len(ids) + 1).zfill(2)


# ---------------- HYBRID FETCH SYSTEM ----------------
async def fetch_waifu_image(query):
    query_clean = query.lower().replace(" ", "%20")

    async with httpx.AsyncClient(timeout=15) as client:

        # 1️⃣ Try NekosAPI (character specific)
        try:
            url1 = f"https://nekosapi.com/api/v3/images/random?tags={query_clean}"
            r1 = await client.get(url1)
            data1 = r1.json()

            if "items" in data1 and len(data1["items"]) > 0:
                return data1["items"][0]["image_url"]
        except:
            pass

        # 2️⃣ Try Nekos.best (random HD)
        try:
            url2 = f"https://nekos.best/api/v2/waifu"
            r2 = await client.get(url2)
            data2 = r2.json()

            if "results" in data2 and len(data2["results"]) > 0:
                return data2["results"][0]["url"]
        except:
            pass

        # 3️⃣ Try Waifu.im (backup)
        try:
            url3 = f"https://api.waifu.im/search?included_tags={query_clean}"
            r3 = await client.get(url3)
            data3 = r3.json()

            if "images" in data3 and len(data3["images"]) > 0:
                return data3["images"][0]["url"]
        except:
            pass

    # ❌ All failed
    return None


# ---------------- MAIN COMMAND ----------------
@app.on_message(filters.command("gupload"))
@require_power("add_character")
async def auto_upload(_, message):
    args = message.text.split()

    if len(args) != 4:
        return await message.reply_text(
            "Use: `/gupload character-name anime-name rarity-number`"
        )

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

    image_url = await fetch_waifu_image(query)

    if not image_url:
        return await waiting.edit("❌ No HD image found.")

    waifu_id = await find_available_id()

    character = {
        "name": character_name,
        "anime": anime_name,
        "rarity": rarity_text,
        "rarity_number": rarity_number,
        "id": waifu_id,
        "img_url": image_url,
    }

    await collection.insert_one(character)

    caption = (
        f"Character Name: {character_name}\n"
        f"Anime: {anime_name}\n"
        f"Rarity: {rarity_text}\n"
        f"ID: {waifu_id}\n"
        f"Added By: [{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    )

    try:
        await app.send_photo(
            CHARA_CHANNEL_ID,
            photo=image_url,
            caption=caption
        )
    except:
        await waiting.edit("⚠️ Image could not be sent to channel.\nBut character saved.")
        return

    await waiting.delete()

    await message.reply_text(
        f"✅ Character Added!\n"
        f"**Name:** {character_name}\n"
        f"**Rarity:** {rarity_text}\n"
        f"**ID:** {waifu_id}"
    )
