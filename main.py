import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import CommandStart

from core import settings
from crud.contest import find_all_contests_tags

mybot = Bot(token=settings.TELEGRAM_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    data = find_all_contests_tags()

    contest_tags_list = data[1]
    qty_of_contests = len(data[2])

    text = f"Hello, {message.from_user.full_name}!\n" \
           f"We have {qty_of_contests} contests in our database for {len(contest_tags_list)} topics\n" \
           f"Let's start!"

    await message.answer(text=text)
    await choose_tag(message, data)


async def choose_tag(message: types.Message, data):
    contest_tags_list = data[1]

    tags_dict = {}
    for index, tag in enumerate(contest_tags_list):
        tags_dict[index + 1] = tag
    # sorted_tags_dict = dict(sorted(tags_dict.items()))
    # print(tags_dict)
    # print(sorted_tags_dict)

    text = f'Choose the desirable topic of the problems to solve, by sending the corresponding number to this chat\n'
    text2 = "\n".join([f'{k} --> "{v}"' for k, v in tags_dict.items()])
    await message.answer(text='\n'.join([text, text2]))
    await choose_rating(message, data)


async def choose_rating(message: types.Message, data):
    contest_levels_list = data[0]

    rating_dict = {}
    for index, level in enumerate(sorted(contest_levels_list)):
        rating_dict[index + 1] = level

    text = f'Choose the rating level of the problems to solve, by sending the corresponding number to this chat\n'
    text2 = "\n".join([f'{k} --> "{v} - {v + 300 - 1 if v != 0 else 799}"' for k, v in rating_dict.items()])

    await message.answer(text='\n'.join([text, text2]))


@dp.message()
async def echo_message(message: types.Message): #входящий аргумент - айди сообщения
    # await message.reply(text=message.text) #отвечаем, в аргументы передаем текст самого изнач.сообщения
    if message.text == '1':
        await message.answer(text='1 - wait a sec')
    else:
        await message.answer(text='2 - wait a sec')


async def main():
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(mybot)

if __name__ == '__main__':
    asyncio.run(main())
