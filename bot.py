import logging
import asyncio

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types
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

# Start command
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer('Бот успешно запущен!')

@dp.message()
async def save_message(message: types.Message):

    print(f'Бот получил сообщение в чате с id: {message.chat.id}')

    

    send_chat = message.chat.id

    if not message.reply_to_message:
        # await message.answer("Невозможно переслать сообщение")
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        username = message.from_user.username
        text = f'{first_name} { last_name if last_name else "" }(@{ username }): { message.text }'
        await bot.send_message(
            chat_id=-4694473266,
            text=text,
            disable_notification=True
        )
    else:
        await bot.forward_message(
            chat_id=-4694473266,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )



# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
