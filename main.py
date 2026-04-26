import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from akinator import AsyncAkinator
from aiohttp import web

# Настройки
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Словарь для хранения активных игр
games = {}

# Кнопки для ответов
def get_kb():
    buttons = [
        [types.InlineKeyboardButton(text="Да", callback_data="0"),
         types.InlineKeyboardButton(text="Нет", callback_data="1")],
        [types.InlineKeyboardButton(text="Я не знаю", callback_data="2")],
        [types.InlineKeyboardButton(text="Скорее да", callback_data="3"),
         types.InlineKeyboardButton(text="Скорее нет", callback_data="4")],
        [types.InlineKeyboardButton(text="Назад", callback_data="back")]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)

# Команда /start
@dp.message(Command("start"))
async def start_game(message: types.Message):
    aki.language = "ru"
q = await aki.start_game()

    games[message.from_user.id] = aki
    await message.answer(f"Загадай персонажа! 🤔\n\nВопрос №1: {q}", reply_markup=get_kb())

# Обработка ответов
@dp.callback_query()
async def process_answer(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    
    if user_id not in games:
        return await callback.answer("Начни игру заново через /start")
    
    aki = games[user_id]
    
    try:
        if callback.data == "back":
            try:
                q = await aki.back()
            except:
                return await callback.answer("Назад нельзя!")
        else:
            # Отправляем ответ Акинатору
            q = await aki.answer(callback.data)

        # Если Акинатор уверен (больше 80% прогресса), он предлагает угадать
        if aki.progression >= 80:
            guess = await aki.win()
            if guess:
                await callback.message.edit_text(
                    f"Это {guess.name} ({guess.description})?\n"
                    f"Я уверен на {int(float(guess.ranking)*100)}%!",
                    reply_markup=None
                )
                del games[user_id] # Конец игры
                return
        
        # Иначе задаем следующий вопрос
        await callback.message.edit_text(
            f"Вопрос №{aki.step + 1}: {q}", 
            reply_markup=get_kb()
        )
    except Exception as e:
        await callback.message.answer("Ой, сервер Акинатора тупит. Попробуй позже!")
        print(f"Ошибка: {e}")

# Костыль для Render (чтобы не спал)
async def handle(request):
    return web.Response(text="Акинатор живой!")

async def main():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await asyncio.gather(site.start(), dp.start_polling(bot))

if __name__ == "__main__":
    asyncio.run(main())
