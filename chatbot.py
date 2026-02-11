import subprocess

def chatbot_reply(user_text):
    prompt = f"""
You are a warm, caring mental health companion.
Talk like a close friend.
Give emotional support, small advice, and encouragement.
Do NOT repeat responses.
User says: {user_text}
"""

    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt,
        text=True,
        capture_output=True
    )

    reply = result.stdout.strip()

    # Simple emotion detection
    emotion = "positive"
    if any(word in user_text.lower() for word in ["sad","tired","depressed","lonely","anxious","angry","stressed"]):
        emotion = "negative"

    return reply, emotion
