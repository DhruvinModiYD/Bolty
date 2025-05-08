import random

polls = [
    {
        "question": "How are you feeling today?",
        "options": {
            "smiley": "Feeling good",
            "cloud": "A little stressed",
            "tornado": "Everything feels messy"
        },
        "results": {
            "smiley": "😄 Glad to see many of you are feeling good!",
            "cloud": "🌧️ A bit of stress is in the air. Let's take a breath together.",
            "tornado": "🌪️ It's a rough patch — reach out if you need support. We're here."
        },
        "low_energy_emojis": ["cloud", "tornado"]
    },
    {
        "question": "What’s draining your energy this week?",
        "options": {
            "brain": "Overthinking",
            "email": "Too many messages",
            "person_juggling": "Doing too many things at once"
        },
        "results": {
            "brain": "🧠 Take a moment to pause and write down what’s looping.",
            "email": "📩 Maybe it's time to silence the inbox for an hour.",
            "person_juggling": "🤹 Don’t forget: saying no is an energy-saving skill."
        },
        "low_energy_emojis": ["brain", "email", "person_juggling"]
    },
    {
        "question": "What helps you when you're feeling low?",
        "options": {
            "musical_note": "Music",
            "bed": "Lying down",
            "ramen": "Comfort food"
        },
        "results": {
            "musical_note": "🎶 Let’s start a music thread! Share your go-to feel-good track.",
            "bed": "🛏️ Sometimes doing nothing is doing something. Rest counts.",
            "ramen": "🍜 Comfort in a bowl — self-kindness comes in many forms."
        },
        "low_energy_emojis": []
    },
    {
        "question": "What wellness habit did you actually try this week?",
        "options": {
            "deciduous_tree": "Went outside",
            "person_in_lotus_position": "Sat quietly",
            "thinking_face": "Reflected on my feelings"
        },
        "results": {
            "deciduous_tree": "🌳 Nature is the best therapy. Keep walking.",
            "person_in_lotus_position": "🧘 Stillness is underrated. Good job.",
            "thinking_face": "🤔 Awareness is the first step to change. Keep going."
        },
        "low_energy_emojis": []
    }
]

affirmations = [
    "💛 You're doing better than you think.",
    "🌱 Healing is not linear — one deep breath at a time.",
    "🌟 It's okay to slow down. Energy isn't always constant.",
    "💬 You're not alone. Someone is always rooting for you.",
    "🎯 Progress, not perfection. Tiny wins matter."
]

def generate_affirmation():
    return random.choice(affirmations)