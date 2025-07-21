from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def build_movie_keyboard(movies):
    keyboard = []
    for idx, movie in enumerate(movies, start=1):
        button = [InlineKeyboardButton(
            text=f"{idx}. {movie['title']} ({movie['quality']})",
            callback_data=f"getlink_{idx}"
        )]
        keyboard.append(button)
    return InlineKeyboardMarkup(keyboard)

def build_verification_keyboard(link):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ Verify & Get Movie", url=link)
    ]])
