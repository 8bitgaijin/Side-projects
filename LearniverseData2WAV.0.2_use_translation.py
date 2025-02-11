# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 12:17:52 2024

@author: Shane
"""

import os
import pyttsx3
from unidecode import unidecode

numbers_quiz = {
    "quiz_title": "Japanese Numbers 1 to 30",
    "questions": [
        {"furigana": "いち", "kanji": "一", "translation": "1"},
        {"furigana": "に", "kanji": "二", "translation": "2"},
        {"furigana": "さん", "kanji": "三", "translation": "3"},
        {"furigana": "よん", "kanji": "四", "translation": "4"},
        {"furigana": "ご", "kanji": "五", "translation": "5"},
        {"furigana": "ろく", "kanji": "六", "translation": "6"},
        {"furigana": "なな", "kanji": "七", "translation": "7"},
        {"furigana": "はち", "kanji": "八", "translation": "8"},
        {"furigana": "きゅう", "kanji": "九", "translation": "9"},
        {"furigana": "じゅう", "kanji": "十", "translation": "10"},
        {"furigana": "じゅういち", "kanji": "十一", "translation": "11"},
        {"furigana": "じゅうに", "kanji": "十二", "translation": "12"},
        {"furigana": "じゅうさん", "kanji": "十三", "translation": "13"},
        {"furigana": "じゅうよん", "kanji": "十四", "translation": "14"},
        {"furigana": "じゅうご", "kanji": "十五", "translation": "15"},
        {"furigana": "じゅうろく", "kanji": "十六", "translation": "16"},
        {"furigana": "じゅうなな", "kanji": "十七", "translation": "17"},
        {"furigana": "じゅうはち", "kanji": "十八", "translation": "18"},
        {"furigana": "じゅうきゅう", "kanji": "十九", "translation": "19"},
        {"furigana": "にじゅう", "kanji": "二十", "translation": "20"},
        {"furigana": "にじゅういち", "kanji": "二十一", "translation": "21"},
        {"furigana": "にじゅうに", "kanji": "二十二", "translation": "22"},
        {"furigana": "にじゅうさん", "kanji": "二十三", "translation": "23"},
        {"furigana": "にじゅうよん", "kanji": "二十四", "translation": "24"},
        {"furigana": "にじゅうご", "kanji": "二十五", "translation": "25"},
        {"furigana": "にじゅうろく", "kanji": "二十六", "translation": "26"},
        {"furigana": "にじゅうなな", "kanji": "二十七", "translation": "27"},
        {"furigana": "にじゅうはち", "kanji": "二十八", "translation": "28"},
        {"furigana": "にじゅうきゅう", "kanji": "二十九", "translation": "29"},
        {"furigana": "さんじゅう", "kanji": "三十", "translation": "30"}
    ]
}

# Initialize the TTS engine
engine = pyttsx3.init()

# Set the voice to Ayumi if available
for voice in engine.getProperty('voices'):
    if "Ayumi" in voice.name:
        engine.setProperty('voice', voice.id)
        break
else:
    print("Ayumi voice not found. Ensure you have the Japanese language pack installed.")

# Set desired speech properties
engine.setProperty('rate', 120)  # Slower rate
engine.setProperty('volume', 0.9)  # Volume

# Function to create WAV file for each question
def save_audio(question, output_folder="audio"):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Use the 'translation' field to name the file with the numeric value
    filename = f"{output_folder}/{question['translation']}.wav"

    # Choose either 'furigana' or 'kanji' text for audio content
    text = question.get("furigana") or question.get("kanji")

    # Save the text to a WAV file with the numeric filename
    engine.save_to_file(text, filename)
    engine.runAndWait()
    
    # Return the file path for reference
    return filename

# Function to process a single quiz
def process_quiz(quiz):
    for question in quiz["questions"]:
        audio_path = save_audio(question)
        question["audio"] = audio_path

# Automatically find and process all quiz variables in the global scope
for var_name, var_value in list(globals().items()):
    if isinstance(var_value, dict) and "quiz_title" in var_value and "questions" in var_value:
        print(f"Processing quiz: {var_name}")
        process_quiz(var_value)

print("All quizzes processed.")
