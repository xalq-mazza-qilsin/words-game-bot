from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.buttons import by_text, by_inline_keyboard, by_image
from loader import dp, db
from random import choices
from states.states import ByText


@dp.message_handler(text=by_text, state='*')
async def selected_by_text(message: types.Message):
    user = await db.select_user(telegram_id=message.from_user.id)
    words = await db.select_all_words()
    word = choices(words)[0]
    pattern = f"{len(word[-1]) * '*'}"
    game = await db.add_game(
        user=user.get('id'),
        status='active',
        chat_type='private',
        word=word.get('id')
    )
    await db.add_guessed_letter(game_id=game.get('id'), guessed_letters=pattern)
    await message.answer(f"{pattern}({word[-1]})\n\nSo'zning harflarini taxmin qiling.")
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
    guessed_letters = guessed_letters.get('guessed_letters')
    for index, letter in enumerate(word[-1]):
        if letter in letters and guessed_letters[index] == '*':
            guessed_letters[index] = letter
        else:
            guessed_letters[index] = '*'
    await db.update_guessed_letter(guessed_letters=guessed_letters, game_id=game_id)
    await message.answer(guessed_letters)
