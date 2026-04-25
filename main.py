import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import web

# Настройки (Берем из переменных или вписываем)
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1003739715047  # ID твоего канала
ADMIN_ID =  8281562805        # ID СЕСТРЫ (модератора)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 1. Получение сообщения от юзера и отправка модератору
@dp.message(F.chat.type == "private")
async def handle_user_message(message: types.Message):
    if message.text:
        # Создаем кнопки для сестры
        builder = InlineKeyboardBuilder()
        builder.row(
            types.InlineKeyboardButton(text="✅ Одобрить", callback_data="approve"),
            types.InlineKeyboardButton(text="❌ Отклонить", callback_data="decline")
        )
        
        await bot.send_message(
            ADMIN_ID, 
            f"📩 Новое сообщение на проверку:\n\n{message.text}",
            reply_markup=builder.as_markup()
        )
        await message.answer("🚀 Твое сообщение отправлено на модерацию!")

# 2. Обработка кнопок (только для сестры)
@dp.callback_query(F.data.in_({"approve", "decline"}))
async def process_moderation(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return await callback.answer("Ты не модератор! 😎")

    if callback.data == "approve":
        # Вырезаем текст из сообщения модератора (убираем заголовок)
        original_text = callback.message.text.replace("📩 Новое сообщение на проверку:\n\n", "")
        await bot.send_message(CHANNEL_ID, f"📩 Анонимно:\n\n{original_text}")
        await callback.message.edit_text(f"✅ Одобрено и отправлено в канал!\n\n{original_text}")
    else:
        await callback.message.edit_text("❌ Сообщение отклонено.")
    
    await callback.answer()

# --- Тот самый костыль для Render (чтобы не спал) ---
async def handle(request):
    return web.Response(text="Бот живой!")

async def main():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await asyncio.gather(site.start(), dp.start_polling(bot))

if __name__ == "__main__":
    asyncio.run(main())
    
