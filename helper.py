from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_keyboard():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Search Movie 🍿", switch_inline_query_current_chat="")],
            [InlineKeyboardButton("Join Updates Channel 🔔", url="https://t.me/Bollyhollyhub")]
        ]
    )

def movie_result_keyboard(movie_list):
    buttons = []
    for index, movie in enumerate(movie_list, start=1):
        buttons.append([
            InlineKeyboardButton(f"{index}. {movie['title']} ({movie['size']}, {movie['quality']})", 
                                 callback_data=f"getlink_{index}")
        ])
    return InlineKeyboardMarkup(buttons)

def verify_keyboard(shortlink):
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🔗 Verify to Get Link", url=shortlink)]
        ]
    )
