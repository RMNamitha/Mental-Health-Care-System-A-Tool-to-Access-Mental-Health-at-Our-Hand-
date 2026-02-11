from transformers import pipeline

emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base"
)

def detect_text_emotion(text):
    result = emotion_classifier(text)[0]
    emotion = result["label"]
    score = round(result["score"], 2)
    return emotion, score
