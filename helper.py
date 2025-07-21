# helper.py

user_steps = {}

def save_user_step(user_id, step):
    user_steps[user_id] = step

def get_user_step(user_id):
    return user_steps.get(user_id, None)

def clear_user_step(user_id):
    if user_id in user_steps:
        del user_steps[user_id]
