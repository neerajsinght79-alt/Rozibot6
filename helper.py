user_steps = {}

def save_user_step(user_id, results):
    user_steps[user_id] = results

def get_user_step(user_id):
    return user_steps.get(user_id)

def clear_user_step(user_id):
    user_steps.pop(user_id, None)
