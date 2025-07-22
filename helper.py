
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import UPDATES_CHANNEL

user_steps = {}

def save_user_step(user_id, data):
    user_steps[user_id] = data

def get_user_step(user_id):
    return user_steps.get(user_id)

def force_join_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔔 Join Update Channel", url=f"https://t.me/{UPDATES_CHANNEL.strip('@')}")],
        [InlineKeyboardButton("✅ Joined", callback_data="verify_join")]
    ])
