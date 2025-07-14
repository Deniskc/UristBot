import logging
import asyncio
import re

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.markdown import bold

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
TARGET_USER_ID = -4956226056
RATING_PATTERN = re.compile(r'оцен[кщиаует]*', re.IGNORECASE)

def highlight_matches(text, pattern):
    """Выделяет все совпадения с регулярным выражением жирным шрифтом"""
    if not text:
        return text
    
    def bold_match(match):
        return bold(match.group(0))
    
    return pattern.sub(bold_match, text)

# Start command
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer('Бот успешно запущен!')

# Перехват всех сообщений из групп/чатов
@dp.message(F.chat.type.in_({"group", "supergroup"}))
async def handle_group_message(message: types.Message):

    matches = RATING_PATTERN.findall(message.text.lower())
    if matches:
        highlighted_text = highlight_matches(message.text, RATING_PATTERN)
        await bot.send_message(
            chat_id=TARGET_USER_ID,
            text=f"<i>{message.from_user.full_name} (@{message.from_user.username})</i>:\n"
                f"{highlighted_text}",
            parse_mode='HTML'
        )

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
