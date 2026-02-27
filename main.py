import os, asyncio
from telegram.ext import ApplicationBuilder, CommandHandler
from telegram import Update
from aiohttp import web

async def start(update: Update, context):
    await update.message.reply_text("I'm alive!")

async def run_bot():
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    print("✅ Bot polling started")
    # Keep running
    await asyncio.Event().wait()

async def run_web():
    async def health(request):
        return web.Response(text="Bot is running")
    app = web.Application()
    app.router.add_get('/', health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get('PORT', 10000)))
    await site.start()
    print("✅ Web server running")
    await asyncio.Event().wait()

async def main():
    await asyncio.gather(run_bot(), run_web())

if __name__ == "__main__":
    asyncio.run(main())
