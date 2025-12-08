import asyncio
import importlib
import threading

from TEAMZYRO import ZYRO, application, LOGGER
from TEAMZYRO.modules import ALL_MODULES

OWNER_ID = 7553434931
LOG_CHAT = -1002891249230


def start_ptb_thread():
    """Run PTB with its own event loop inside thread."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        application.run_polling(drop_pending_updates=True)
    except Exception as e:
        LOGGER("PTB").error(f"PTB Error: {e}")


async def send_start_message():
    try:
        await ZYRO.send_message(OWNER_ID, "✅ Bot started successfully!")
    except Exception as e:
        LOGGER("TEAMZYRO").error(f"Owner message error: {e}")

    try:
        await ZYRO.send_message(LOG_CHAT, "🚀 Bot started in group!")
    except Exception as e:
        LOGGER("TEAMZYRO").error(f"Group message error: {e}")


async def start_all():
    # Load all modules
    for module_name in ALL_MODULES:
        importlib.import_module("TEAMZYRO.modules." + module_name)
    LOGGER("TEAMZYRO.modules").info("🔥 All Features Loaded Successfully!")

    # Start PTB in its own thread + loop
    threading.Thread(target=start_ptb_thread, daemon=True).start()
    LOGGER("TEAMZYRO").info("PTB thread started ✔")

    # Start Pyrogram Client
    await ZYRO.start()
    LOGGER("TEAMZYRO").info("Pyrogram started ✔")

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
