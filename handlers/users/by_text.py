from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.buttons import by_text, by_inline_keyboard, by_image, game_types_markup
from loader import dp, db
from random import choices
from states.states import ByText
import asyncpg


@dp.message_handler(text=by_text, state='*')
async def selected_by_text(message: types.Message):
    user = await db.select_user(telegram_id=message.from_user.id)
    words = await db.select_all_words()
    while True:
        random_word = choices(words)[0]
        game = await db.select_user_games(user.get('id'))
        if game:
            word = game[-1].get('word')
            if random_word != word:
                break
        else:
            break
    pattern = f"{len(random_word[-1]) * '*'}"
    try:
        game = await db.add_game(
            user=user.get('id'),
            status='active',
            chat_type='private',
            word=random_word.get('id')
        )
    except asyncpg.exceptions.UniqueViolationError:
        games = await db.select_user_games(user_id=user.get('id'))
        game = games[-1]
    await db.add_guessed_letter(game_id=game.get('id'), guessed_letters=pattern)
    await message.answer(f"{pattern}({random_word[-1]})\n\nSo'zning harflarini taxmin qiling.", reply_markup=types.ReplyKeyboardRemove())
    await ByText.guess_letters.set()


@dp.message_handler(state=ByText.guess_letters)
async def get_letters(message: types.Message):
    user = await db.select_user(telegram_id=message.from_user.id)
    game = await db.select_user_games(user.get('id'))
    game_id = game[-1].get('id')
    guessed_letters = await db.get_guessed_letter(game_id=game_id)
    word_id = game[-1].get('word_id')
    word = await db.get_word(id=word_id)
    letters = [letter for letter in message.text]
    guessed_letters_list = [letter for letter in guessed_letters.get('guessed_letters')]
    for index, letter in enumerate(word[-1]):
        if letter in letters and guessed_letters_list[index] == '*':
            guessed_letters_list[index] = letter
        else:
            continue
    result = ''
    for letter in guessed_letters_list:
        result += letter
    await db.update_guessed_letter(guessed_letters=result, game_id=game_id)
    if result == word[-1]:
        await message.answer(f"<code>{word[-1]}</code> - Butun so'z topib bo'ldingiz!", reply_markup=game_types_markup)
    else:
        await message.answer(result)
