import random

def generate_message():
    messages = [
        "🌞 Good morning! Hope today brings you calm and clarity.",
        "🧘 A small check-in goes a long way. How are you feeling today?",
        "💬 Feel free to share anything on your mind today!",
        "✨ You're doing great. Wishing you a smooth day ahead!",
        "🎯 A new day, a new chance to grow. You've got this!"
    ]
    return random.choice(messages)