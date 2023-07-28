from aiogram.types import ReplyKeyboardMarkup


by_text = "Oddiy matn orqali"
by_inline_keyboard = "Tugmalar orqali"
by_image = "Rasm orqali"

game_types_markup = ReplyKeyboardMarkup(resize_keyboard=True)
game_types_markup.add(by_text, by_inline_keyboard)
game_types_markup.add(by_image)

