import logging
import asyncio
import re

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

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
# TARGET_USER_ID = 1208126125
TAGS = [
    'оценк',
    'оценщик',
    'оценку', 
    'оценить', 
    'оценит', 
    'оцените', 
    'оценщ', 
    'оцен', 
    'оценка', 
]


# Start command
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer('Бот успешно запущен!')

# Перехват всех сообщений из групп/чатов
@dp.message(F.chat.type.in_({"group", "supergroup"}))
async def handle_group_message(message: types.Message):
    chat_id = message.chat.id
    print(chat_id)
    text_lower = message.text
    found_tags = [tag for tag in TAGS if tag in text_lower]
    RATING_PATTERN = re.compile(r'оцен[кщ]?', re.IGNORECASE)
    if found_tags or RATING_PATTERN.search(message.text):
        try:
            await bot.forward_message(
                chat_id=TARGET_USER_ID,
                from_chat_id=message.chat.id,
                message_id=message.message_id,
                # disble_notification=True
            )
        except:
            # Альтернатива: можно отправлять текст + информацию о чате
            await bot.send_message(
                chat_id=TARGET_USER_ID,
                text=
                    f"<i>{message.from_user.full_name} (@{message.from_user.username})</i>:\n"
                    f"{message.text}",
                    parse_mode='HTML',
                    # disble_notification=True
            )

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
