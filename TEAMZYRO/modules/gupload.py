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


# ---------------- SAFE HYBRID FETCH SYSTEM ----------------
async def fetch_waifu_image(query):
    query_clean = query.lower().replace(" ", "%20")
    TIMEOUT = httpx.Timeout(2.0)

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:

        # 1️⃣ NekosAPI (HD models)
        try:
            r1 = await client.get(
                f"https://nekosapi.com/api/v3/images/random?tags={query_clean}"
            )
            d1 = r1.json()

            if d1.get("items"):
                return d1["items"][0]["image_url"]
        except:
            pass

        # 2️⃣ Waifu.pics (super fast + HD)
        try:
            r2 = await client.get(f"https://api.waifu.pics/sfw/{query_clean}")
            d2 = r2.json()

            if d2.get("url"):
                return d2["url"]
        except:
            pass

        # 3️⃣ Waifu.im (updated modern endpoint)
        try:
            r3 = await client.get(
                f"https://api.waifu.im/search?included_tags={query_clean}"
            )
            d3 = r3.json()

            if d3.get("images"):
                return d3["images"][0]["url"]
        except:
            pass

        # 4️⃣ Fallback: Nekos.best random HD
        try:
            r4 = await client.get("https://nekos.best/api/v2/waifu")
            d4 = r4.json()

            if d4.get("results"):
                return d4["results"][0]["url"]
        except:
            pass

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

    waiting = await message.reply_text("⏳ Fetching HD image...")
    
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
