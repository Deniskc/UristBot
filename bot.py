import logging
import asyncio
import re

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from html import escape

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота
with open("token.txt", "r") as f:
    TOKEN = f.read()

API_TOKEN = TOKEN
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

with open("chat_id.txt", "r") as f:
    TARGET_CHAT_ID = f.read()

# TARGET_CHAT_ID = -4956226056
RATING_PATTERN = re.compile(r'\bоцен(?:к[ауеи]|щик|ист|ивать|ять|ю|ил|ят)\b', re.IGNORECASE)

def highlight_matches(text, pattern):
    """Выделяет все совпадения с регулярным выражением жирным шрифтом"""
    if not text:
        return text
    
    def bold_match(match):
        return f'<b><u>{escape(match.group(0))}</u></b>'
    
    return pattern.sub(bold_match, text)

# Start command
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer('Бот успешно запущен!')

# Перехват всех сообщений из групп/чатов
@dp.message(F.chat.type.in_({"group", "supergroup"}))
async def handle_group_message(message: types.Message):

    chat_link = None
    try:
        if message.chat.username:
            chat_link = f"https://t.me/{message.chat.username}"
        else:
            # Если чат приватный, пробуем получить инвайт-ссылку
            chat_link = await bot.export_chat_invite_link(chat_id=message.chat.id)
    except:
        pass

    if not message.text:
        return
    
    date = message.date.astimezone()
    
    matches = RATING_PATTERN.findall(message.text)
    if matches:
        highlighted_text = highlight_matches(message.text, RATING_PATTERN)
        await bot.send_message(
            chat_id=TARGET_CHAT_ID,
            text=
                f"<a href='{chat_link}'>Ссылка на чат</a> \n"
                f"<b>{date.strftime('%d.%m.%Y в %H:%M, %A')}</b> \n"
                f"<i>{escape(message.from_user.full_name)} (@{escape(message.from_user.username)})</i>:\n\n"
                f"{highlighted_text}"
                # f"</b>"
            ,parse_mode='HTML'
        )

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
