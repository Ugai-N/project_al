from aiogram import types, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.settings import SessionLocal
from crud.contest import get_contests_info, find_contests_with_rating, find_contests_with_rating_and_tag
from crud.problem import search_problem_by_search_code

router = Router()
# @dp.message(CommandStart())
# async def handle_start(message: types.Message):
#     contests_data = get_contests_info()
#
#     contest_tags_list = contests_data[1]
#     qty_of_contests = len(contests_data[2])
#
#     text = f"Hello, {message.from_user.full_name}!\n" \
#            f"We have {qty_of_contests} contests in our database for {len(contest_tags_list)} topics\n" \
#            f"Let's start!"
#
#     await message.answer(text=text)
#     await choose_rating(message, contests_data)

@router.message(CommandStart())
async def handle_start(message: types.Message):
    contests_data = get_contests_info()

    contest_tags_list = contests_data[1]
    qty_of_contests = len(contests_data[2])

    text = f"Hello, {message.from_user.full_name}!\n" \
           f"We have {qty_of_contests} contests in our database for {len(contest_tags_list)} topics\n" \
           f"Let's start! Send any command from below:\n\n" \
           f"/choose - to choose the rating and tag for a contest of 10 problems\n" \
           f"/find - find a problem via search code\n"

    await message.answer(text=text)


@router.message(Command('help'))
async def handle_help(message: types.Message):
    text = f"I am a bot, that will provide you the info on 10 problems from CodeForces, " \
           f"grouped by the rating and topics upon your request\n\n" \
           f"Send any command from below:\n\n" \
           f"/choose - to choose the rating and tag for a contest of 10 problems\n" \
           f"/find - find a problem via search code\n"
    await message.answer(text=text)


@router.message(Command('find'))
async def handle_find(message: types.Message):
    text = f"Please enter the search code of the problem, eg: 1912-D"
    await message.answer(text=text)


@router.message(Command('choose'))
async def choose_rating(message: types.Message):
    contests_data = get_contests_info()
    contest_rating_list = contests_data[0]

    builder = InlineKeyboardBuilder()
    for rating in sorted(contest_rating_list):
        builder.button(text=f"{rating} - {rating + 300 - 1 if rating != 0 else 799}",
                       callback_data=f"rating:{rating}")
    builder.adjust(2, 2)

    await message.answer(
        "Choose the rating level of the problems to solve\n",
        reply_markup=builder.as_markup())


# async def choose_rating(message: types.Message, contests_data):
#     contest_rating_list = contests_data[0]
#
#     builder = InlineKeyboardBuilder()
#     for rating in sorted(contest_rating_list):
#         builder.button(text=f"{rating} - {rating + 300 - 1 if rating != 0 else 799}",
#                        callback_data=f"rating:{rating}")
#     builder.adjust(2, 2)
#
#     await message.answer(
#         "Choose the rating level of the problems to solve\n",
#         reply_markup=builder.as_markup())


@router.callback_query(lambda call: call.data.startswith('rating'))
async def choose_tag(callback: CallbackQuery):
    rate_str = callback.data.split(':')[1]
    rate_int = int(rate_str)
    tags = find_contests_with_rating(rate_int)

    tags_builder = InlineKeyboardBuilder()
    for tag in tags:
        tags_builder.button(text=f"{tag}",
                            callback_data=f"tag:{tag}_rating:{rate_int}")
    tags_builder.adjust(2, 2)

    await callback.answer(text=f"rating {rate_int} was chosen")
    await callback.message.answer(
        f'for the rating "{rate_int} - {rate_int + 300 - 1 if rate_int != 0 else 799}" we have {len(tags)} topics.\n'
        f'Choose the desirable topic of the problems to solve',
        reply_markup=tags_builder.as_markup())


@router.callback_query(lambda call: call.data.startswith('tag'))
async def deliver_problem(callback: CallbackQuery):
    rate_int = int(callback.data.split('_')[1].replace('rating:', ''))
    tags_str = callback.data.split('_')[0].replace('tag:', '')
    contest_data = find_contests_with_rating_and_tag(tags_str, rate_int)
    contest = contest_data[0]
    qty_of_set_contests = contest_data[2]
    await callback.answer(text=f"tag {tags_str} was chosen")
    await callback.message.answer(
        text=f'<b><i>There are {qty_of_set_contests} contests with rating "{contest.rating}" '
             f'for topic "{contest.tag}"</i></b>\n'
             f'We have randomly chosen <b>"{contest}"</b>.\n'
             f'It has the following problems:\n')
    problems = contest_data[1]  # list
    count = 1
    for pro in problems:
        text = f'{count}. <b>{pro}</b>\n' \
               f'rating: {pro.rating}\n' \
               f'times solved: {pro.solvedCount}'
        await callback.message.answer(text=text)
        count += 1
    await callback.message.answer(text="to check the available commands --> /help")


@router.callback_query(lambda call: call.data.startswith('search'))
async def perform_searching(callback: CallbackQuery):
    answer = callback.data.split(':')[1]
    search_text = callback.data.split(':')[2]
    if answer == 'YES':
        with SessionLocal() as user_db:
            db_data = search_problem_by_search_code(user_db, search_text)
            if db_data is not None:
                problem = db_data[0]
                text = f'<b>{problem}</b>\n' \
                       f'<b>rating:</b> {problem.rating}\n' \
                       f'<b>times solved:</b> {problem.solvedCount}\n' \
                       f'<b>contest:</b> {db_data[1]}\n' \
                       f'<b>tags:</b>'
                tags_text = "\n".join([f'   -- {tag.tag}' for tag in problem.tags])
            else:
                text = f'Sorry! There is no such problem in our data base\n\n' \
                       f'You can always check the available commands here --> /help'
                tags_text = ''
            await callback.message.answer(text='\n'.join([text, tags_text]))
    else:
        await callback.message.answer(
            text=f'OK, but just to remind you:\n'
                 f'You can always check the available commands here --> /help')


@router.message()
async def start_searching(message: types.Message):
    yes_button = InlineKeyboardButton(text=f"YES",
                                      callback_data=f"search:YES:{message.text}")
    no_button = InlineKeyboardButton(text=f"NO",
                                     callback_data=f"search:NO:{message.text}")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[yes_button], [no_button]])
    if message.text:
        await message.reply(text='Do you want me to search for the problem by this search code?\n\n'
                                 'To check the available commands --> /help', reply_markup=keyboard)
    else:
        await message.answer(text='I can search the problem only by its search code, e.g 1912-D\n\n'
                                  'To check the available commands --> /help')
