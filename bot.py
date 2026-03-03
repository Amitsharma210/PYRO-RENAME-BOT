from datetime import datetime
from pytz import timezone
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from config import Config
from aiohttp import web
import os


class Bot(Client):
    def __init__(self):
        super().__init__(
            name="renamer",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,

            # 🔥 Optimized for Koyeb Free (512MB RAM)
            workers=4,

            plugins={"root": "plugins"},
            sleep_threshold=15,

            # 🔥 Keep only 1 transmission for stability
            max_concurrent_transmissions=1,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username
        self.uptime = Config.BOT_UPTIME

        # ✅ WEB SERVER FOR KOYEB
        if Config.WEB_SUPPORT:
            port = int(os.environ.get("PORT", 8000))

            async def handle(request):
                return web.Response(text="Bot is running!")

            app = web.Application()
            app.router.add_get("/", handle)

            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, "0.0.0.0", port)
            await site.start()

        print(f"\033[1;96m @{me.username} Sᴛᴀʀᴛᴇᴅ......⚡️⚡️⚡️\033[0m")

        try:
            for id in Config.ADMIN:
                await self.send_message(id, f"**__{me.first_name} Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**")
        except:
            pass

        if Config.LOG_CHANNEL:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')

                await self.send_message(
                    Config.LOG_CHANNEL,
                    f"**__{me.mention} Iꜱ Rᴇsᴛᴀʀᴛᴇᴅ !!__**\n\n"
                    f"📅 Date : `{date}`\n"
                    f"⏰ Time : `{time}`\n"
                    f"🌐 Timezone : `Asia/Kolkata`\n\n"
                    f"🉐 Version : `v{__version__} (Layer {layer})`"
                )
            except:
                print("Please make this bot admin in your log channel")


Bot().run()
