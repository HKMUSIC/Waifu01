import httpx
from pyrogram import filters
from TEAMZYRO import (
    app,
    CHARA_CHANNEL_ID,
    collection,
    rarity_map,
    require_power
)

# ---------------- FIND NEXT AVAILABLE ID ----------------
async def find_available_id():
    cursor = collection.find({}, {"id": 1}).sort("id", 1)
    ids = []

    async for doc in cursor:
        try:
            ids.append(int(doc["id"]))
        except:
            pass

    ids.sort()
    for i in range(1, len(ids) + 2):
        if i not in ids:
            return str(i).zfill(2)

    return str(len(ids) + 1).zfill(2)


# ---------------- FETCH IMAGE FROM WAIFU.IM --------------
async def fetch_character_image(character_name):
    url = "https://graphql.anilist.co"

    query = """
    query ($name: String) {
      Character(search: $name) {
        image {
          large
        }
      }
    }
    """

    variables = {"name": character_name}

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            resp = await client.post(url, json={"query": query, "variables": variables})
            data = resp.json()

            img = data["data"]["Character"]["image"]["large"]

            return img
        except:
            return None


# --------------------- MAIN COMMAND ----------------------
@app.on_message(filters.command("gupload"))
@require_power("add_character")
async def auto_upload(_, message):
    args = message.text.split()

    if len(args) != 4:
        return await message.reply_text(
            "❗ Use:\n`/gupload character-name anime-name rarity-number`"
        )

    character_name = args[1].replace("-", " ").title()
    anime_name = args[2].replace("-", " ").title()

    # rarity check
    try:
        rarity_number = int(args[3])
    except:
        return await message.reply_text("❌ Rarity must be a number.")

    if rarity_number not in rarity_map:
        return await message.reply_text("❌ Invalid rarity number.")

    rarity_text = rarity_map[rarity_number]

    # fetching image
    waiting = await message.reply_text("⏳ Fetching HD image from waifu.im...")

    query = character_name.lower().replace(" ", "%20")
    image_url = await fetch_waifu_image(query)

    if not image_url:
        return await waiting.edit("❌ No HD image found for this character.")

    # ID generate
    waifu_id = await find_available_id()

    # save in DB
    character = {
        "name": character_name,
        "anime": anime_name,
        "rarity": rarity_text,
        "rarity_number": rarity_number,
        "id": waifu_id,
        "img_url": image_url,
    }

    await collection.insert_one(character)

    # Send to channel
    caption = (
        f"✨ **New Character Added!**\n\n"
        f"**Name:** {character_name}\n"
        f"**Anime:** {anime_name}\n"
        f"**Rarity:** {rarity_text}\n"
        f"**ID:** `{waifu_id}`\n"
        f"**Added By:** [{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    )

    try:
        await app.send_photo(
            CHARA_CHANNEL_ID,
            photo=image_url,
            caption=caption
        )
    except:
        await waiting.edit("⚠️ Character saved but image failed to send to channel.")
        return

    await waiting.delete()

    await message.reply_text(
        f"✅ **Character Added Successfully!**\n"
        f"**Name:** {character_name}\n"
        f"**ID:** `{waifu_id}`\n"
        f"**Rarity:** {rarity_text}"
    )
