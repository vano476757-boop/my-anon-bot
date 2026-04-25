import asyncio
import os
from aiogram import Bot, Dispatcher, types

# Эти данные мы впишем потом в самом Koyeb
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def forward_to_channel(message: types.Message):
    if message.text:
        try:
            await bot.send_message(CHANNEL_ID, f"📩 Анонимка:\n\n{message.text}")
            await message.answer("✅ Отправлено в канал!")
        except Exception as e:
            await message.answer("❌ Ошибка. Проверь, админ ли бот в канале.")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
