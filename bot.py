import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton
from thinker import RuT5SmallModel

API_TOKEN = '...'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

current_thinker = RuT5SmallModel()


@dp.message_handler(commands=['start'])
async def greetings(message: types.Message):
    await message.reply('Привет, я Думатель. Сыграем?')

@dp.message_handler(commands=['config'])
async def configuration(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    rut5_button = KeyboardButton('rut5-small')
    keyboard.add(rut5_button)
    await message.answer("Выберите модель с которой хотите сыграть",\
         reply_markup=keyboard)

@dp.message_handler()
async def guess_the_ridlde(message: types.Message):
    riddle = message.text
    if riddle == 'rut5-small':
        global current_thinker
        current_thinker = RuT5SmallModel()
        await message.reply('Вы играете в загадки с rut5-small!')
    else:
        try:
            answer = current_thinker.guess_the_riddle(riddle)
            await message.reply(answer)
        except Exception as error:
            await message.reply(f'Ошибка: {error}')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)