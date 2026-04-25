import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiohttp import web

# Берем токен из настроек хостинга
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1003739715047  # Замени на свой ID!

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Код самого бота
@dp.message()
async def forward_to_channel(message: types.Message):
    if message.text:
        try:
            await bot.send_message(CHANNEL_ID, f"📩 Анонимно:\n\n{message.text}")
            await message.answer("✅ Отправлено!")
        except Exception as e:
            print(f"Ошибка: {e}")

# Костыль для "прожарки" (чтобы не спал)
async def handle(request):
    return web.Response(text="Бот живой!")

async def main():
    # Запускаем веб-сервер на порту 8080
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    
    # Запускаем и сервер, и бота одновременно
    await asyncio.gather(site.start(), dp.start_polling(bot))

if __name__ == "__main__":
    asyncio.run(main())
  
