import asyncio
import importlib
import threading
from TEAMZYRO import ZYRO, application, LOGGER
from TEAMZYRO.modules import ALL_MODULES


OWNER_ID = 7553434931
LOG_CHAT = -1002792716047


def start_ptb():
    """Run PTB in a separate thread (safe)."""
    application.run_polling(drop_pending_updates=True)


async def send_start_message():
    try:
        await ZYRO.send_message(
            OWNER_ID,
            "✅ Bot Started Successfully!"
        )
        await ZYRO.send_message(
            LOG_CHAT,
            "🚀 TEAMZYRO Started!"
        )
        LOGGER("TEAMZYRO").info("Start messages sent.")
    except Exception as e:
        LOGGER("TEAMZYRO").error(e)


async def start_all():
    # Load modules
    for module_name in ALL_MODULES:
        importlib.import_module("TEAMZYRO.modules." + module_name)

    LOGGER("TEAMZYRO.modules").info("🔥 All Features Loaded Successfully!")

    # Start PTB in another thread
    threading.Thread(target=start_ptb, daemon=True).start()

    # Start Pyrogram
    await ZYRO.start()

    # Send start messages
    await send_start_message()

    LOGGER("TEAMZYRO").info(
        "╔═════ஜ۩۞۩ஜ════╗\n"
        "  ☠︎︎ MADE BY GOJOXNETWORK ☠︎︎\n"
        "╚═════ஜ۩۞۩ஜ════╝"
    )


def main():
    asyncio.run(start_all())


if __name__ == "__main__":
    main()
