# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 10:05:45 2024

@author: Shane
"""

import os
import pyttsx3
from unidecode import unidecode


numbers_quiz = {
    "quiz_title": "Japanese Numbers 1 to 30",
    "questions": [
        {"furigana": "おつかれさまでした。", "kanji": "お疲れ様でした。", "translation": "Great job"},
    ]
}



# Example quiz data in the required format
# Quiz data in the required format
# greetings_quiz = {
#     "quiz_title": "Japanese Greetings",
#     "questions": [
#         {
#             "furigana": "おはようございます。",
#             "kanji": None,  # Optional if not available
#             "translation": "Good morning"
#         },
#         {
#             "furigana": "こんにちは。",
#             "kanji": None,
#             "translation": "Hello"
#         },
#         {
#             "furigana": "こんばんは。",
#             "kanji": None,
#             "translation": "Good evening"
#         }
#     ]
# }


# # Quiz for Days of the Week
# days_of_week_quiz = {
#     "quiz_title": "Days of the Week",
#     "questions": [
#         {"furigana": "今日は 月曜日 です。", "kanji": None, "translation": "Today is Monday."},
#         {"furigana": "今日は 火曜日 です。", "kanji": None, "translation": "Today is Tuesday."},
#         {"furigana": "今日は 水曜日 です。", "kanji": None, "translation": "Today is Wednesday."},
#         {"furigana": "今日は 木曜日 です。", "kanji": None, "translation": "Today is Thursday."},
#         {"furigana": "今日は 金曜日 です。", "kanji": None, "translation": "Today is Friday."},
#         {"furigana": "今日は 土曜日 です。", "kanji": None, "translation": "Today is Saturday."},
#         {"furigana": "今日は 日曜日 です。", "kanji": None, "translation": "Today is Sunday."}
#     ]
# }

# # Quiz for Months of the Year
# months_of_year_quiz = {
#     "quiz_title": "Months of the Year",
#     "questions": [
#         {"furigana": "今月は 1月 です。", "kanji": None, "translation": "This month is January."},
#         {"furigana": "今月は 2月 です。", "kanji": None, "translation": "This month is February."},
#         {"furigana": "今月は 3月 です。", "kanji": None, "translation": "This month is March."},
#         {"furigana": "今月は 4月 です。", "kanji": None, "translation": "This month is April."},
#         {"furigana": "今月は 5月 です。", "kanji": None, "translation": "This month is May."},
#         {"furigana": "今月は 6月 です。", "kanji": None, "translation": "This month is June."},
#         {"furigana": "今月は 7月 です。", "kanji": None, "translation": "This month is July."},
#         {"furigana": "今月は 8月 です。", "kanji": None, "translation": "This month is August."},
#         {"furigana": "今月は 9月 です。", "kanji": None, "translation": "This month is September."},
#         {"furigana": "今月は 10月 です。", "kanji": None, "translation": "This month is October."},
#         {"furigana": "今月は 11月 です。", "kanji": None, "translation": "This month is November."},
#         {"furigana": "今月は 12月 です。", "kanji": None, "translation": "This month is December."}
#     ]
# }

# # Hiragana Quiz
# # Hiragana Quiz with Voiced and Semi-Voiced Sounds
# hiragana_quiz = {
#     "quiz_title": "Hiragana Characters with Voiced Sounds",
#     "questions": [
#         # Basic Hiragana
#         {"furigana": "あ", "kanji": None, "translation": "A"},
#         {"furigana": "い", "kanji": None, "translation": "I"},
#         {"furigana": "う", "kanji": None, "translation": "U"},
#         {"furigana": "え", "kanji": None, "translation": "E"},
#         {"furigana": "お", "kanji": None, "translation": "O"},
#         {"furigana": "か", "kanji": None, "translation": "Ka"},
#         {"furigana": "き", "kanji": None, "translation": "Ki"},
#         {"furigana": "く", "kanji": None, "translation": "Ku"},
#         {"furigana": "け", "kanji": None, "translation": "Ke"},
#         {"furigana": "こ", "kanji": None, "translation": "Ko"},
#         {"furigana": "さ", "kanji": None, "translation": "Sa"},
#         {"furigana": "し", "kanji": None, "translation": "Shi"},
#         {"furigana": "す", "kanji": None, "translation": "Su"},
#         {"furigana": "せ", "kanji": None, "translation": "Se"},
#         {"furigana": "そ", "kanji": None, "translation": "So"},
#         {"furigana": "た", "kanji": None, "translation": "Ta"},
#         {"furigana": "ち", "kanji": None, "translation": "Chi"},
#         {"furigana": "つ", "kanji": None, "translation": "Tsu"},
#         {"furigana": "て", "kanji": None, "translation": "Te"},
#         {"furigana": "と", "kanji": None, "translation": "To"},
#         {"furigana": "な", "kanji": None, "translation": "Na"},
#         {"furigana": "に", "kanji": None, "translation": "Ni"},
#         {"furigana": "ぬ", "kanji": None, "translation": "Nu"},
#         {"furigana": "ね", "kanji": None, "translation": "Ne"},
#         {"furigana": "の", "kanji": None, "translation": "No"},
#         {"furigana": "は", "kanji": None, "translation": "Ha"},
#         {"furigana": "ひ", "kanji": None, "translation": "Hi"},
#         {"furigana": "ふ", "kanji": None, "translation": "Fu"},
#         {"furigana": "へ", "kanji": None, "translation": "He"},
#         {"furigana": "ほ", "kanji": None, "translation": "Ho"},
#         {"furigana": "ま", "kanji": None, "translation": "Ma"},
#         {"furigana": "み", "kanji": None, "translation": "Mi"},
#         {"furigana": "む", "kanji": None, "translation": "Mu"},
#         {"furigana": "め", "kanji": None, "translation": "Me"},
#         {"furigana": "も", "kanji": None, "translation": "Mo"},
#         {"furigana": "や", "kanji": None, "translation": "Ya"},
#         {"furigana": "ゆ", "kanji": None, "translation": "Yu"},
#         {"furigana": "よ", "kanji": None, "translation": "Yo"},
#         {"furigana": "ら", "kanji": None, "translation": "Ra"},
#         {"furigana": "り", "kanji": None, "translation": "Ri"},
#         {"furigana": "る", "kanji": None, "translation": "Ru"},
#         {"furigana": "れ", "kanji": None, "translation": "Re"},
#         {"furigana": "ろ", "kanji": None, "translation": "Ro"},
#         {"furigana": "わ", "kanji": None, "translation": "Wa"},
#         {"furigana": "を", "kanji": None, "translation": "Wo"},
#         {"furigana": "ん", "kanji": None, "translation": "N"},

#         # Voiced Hiragana (Dakuten)
#         {"furigana": "が", "kanji": None, "translation": "Ga"},
#         {"furigana": "ぎ", "kanji": None, "translation": "Gi"},
#         {"furigana": "ぐ", "kanji": None, "translation": "Gu"},
#         {"furigana": "げ", "kanji": None, "translation": "Ge"},
#         {"furigana": "ご", "kanji": None, "translation": "Go"},
#         {"furigana": "ざ", "kanji": None, "translation": "Za"},
#         {"furigana": "じ", "kanji": None, "translation": "Ji"},
#         {"furigana": "ず", "kanji": None, "translation": "Zu"},
#         {"furigana": "ぜ", "kanji": None, "translation": "Ze"},
#         {"furigana": "ぞ", "kanji": None, "translation": "Zo"},
#         {"furigana": "だ", "kanji": None, "translation": "Da"},
#         {"furigana": "ぢ", "kanji": None, "translation": "Ji"},
#         {"furigana": "づ", "kanji": None, "translation": "Zu"},
#         {"furigana": "で", "kanji": None, "translation": "De"},
#         {"furigana": "ど", "kanji": None, "translation": "Do"},
#         {"furigana": "ば", "kanji": None, "translation": "Ba"},
#         {"furigana": "び", "kanji": None, "translation": "Bi"},
#         {"furigana": "ぶ", "kanji": None, "translation": "Bu"},
#         {"furigana": "べ", "kanji": None, "translation": "Be"},
#         {"furigana": "ぼ", "kanji": None, "translation": "Bo"},

#         # Semi-Voiced Hiragana (Handakuten)
#         {"furigana": "ぱ", "kanji": None, "translation": "Pa"},
#         {"furigana": "ぴ", "kanji": None, "translation": "Pi"},
#         {"furigana": "ぷ", "kanji": None, "translation": "Pu"},
#         {"furigana": "ぺ", "kanji": None, "translation": "Pe"},
#         {"furigana": "ぽ", "kanji": None, "translation": "Po"}
#     ]
# }

# # Complete Hiragana Quiz with Basic, Voiced, Semi-Voiced, and Yōon Sounds
# hiragana_quiz2 = {
#     "quiz_title": "Complete Hiragana Characters with Long Vowels",
#     "questions": [
        
#         # Yōon (Contracted Sounds)
#         {"furigana": "きゃ", "kanji": None, "translation": "Kya"},
#         {"furigana": "きゅ", "kanji": None, "translation": "Kyu"},
#         {"furigana": "きょ", "kanji": None, "translation": "Kyo"},
        
#         # Long Vowel Yōon
#         {"furigana": "きゃあ", "kanji": None, "translation": "Kyaa"},
#         {"furigana": "きゅう", "kanji": None, "translation": "Kyuu"},
#         {"furigana": "きょう", "kanji": None, "translation": "Kyou"},
        
#         {"furigana": "しゃ", "kanji": None, "translation": "Sha"},
#         {"furigana": "しゅ", "kanji": None, "translation": "Shu"},
#         {"furigana": "しょ", "kanji": None, "translation": "Sho"},
        
#         {"furigana": "しゃあ", "kanji": None, "translation": "Shaa"},
#         {"furigana": "しゅう", "kanji": None, "translation": "Shuu"},
#         {"furigana": "しょう", "kanji": None, "translation": "Shou"},
        
#         {"furigana": "ちゃ", "kanji": None, "translation": "Cha"},
#         {"furigana": "ちゅ", "kanji": None, "translation": "Chu"},
#         {"furigana": "ちょ", "kanji": None, "translation": "Cho"},
        
#         {"furigana": "ちゃあ", "kanji": None, "translation": "Chaa"},
#         {"furigana": "ちゅう", "kanji": None, "translation": "Chuu"},
#         {"furigana": "ちょう", "kanji": None, "translation": "Chou"},
        
#         {"furigana": "にゃ", "kanji": None, "translation": "Nya"},
#         {"furigana": "にゅ", "kanji": None, "translation": "Nyu"},
#         {"furigana": "にょ", "kanji": None, "translation": "Nyo"},
        
#         {"furigana": "にゃあ", "kanji": None, "translation": "Nyaa"},
#         {"furigana": "にゅう", "kanji": None, "translation": "Nyuu"},
#         {"furigana": "にょう", "kanji": None, "translation": "Nyou"},
        
#         {"furigana": "ひゃ", "kanji": None, "translation": "Hya"},
#         {"furigana": "ひゅ", "kanji": None, "translation": "Hyu"},
#         {"furigana": "ひょ", "kanji": None, "translation": "Hyo"},
        
#         {"furigana": "ひゃあ", "kanji": None, "translation": "Hyaa"},
#         {"furigana": "ひゅう", "kanji": None, "translation": "Hyuu"},
#         {"furigana": "ひょう", "kanji": None, "translation": "Hyou"},
        
#         {"furigana": "みゃ", "kanji": None, "translation": "Mya"},
#         {"furigana": "みゅ", "kanji": None, "translation": "Myu"},
#         {"furigana": "みょ", "kanji": None, "translation": "Myo"},
        
#         {"furigana": "みゃあ", "kanji": None, "translation": "Myaa"},
#         {"furigana": "みゅう", "kanji": None, "translation": "Myuu"},
#         {"furigana": "みょう", "kanji": None, "translation": "Myou"},
        
#         {"furigana": "りゃ", "kanji": None, "translation": "Rya"},
#         {"furigana": "りゅ", "kanji": None, "translation": "Ryu"},
#         {"furigana": "りょ", "kanji": None, "translation": "Ryo"},
        
#         {"furigana": "りゃあ", "kanji": None, "translation": "Ryaa"},
#         {"furigana": "りゅう", "kanji": None, "translation": "Ryuu"},
#         {"furigana": "りょう", "kanji": None, "translation": "Ryou"},
        
#         # Voiced Yōon
#         {"furigana": "ぎゃ", "kanji": None, "translation": "Gya"},
#         {"furigana": "ぎゅ", "kanji": None, "translation": "Gyu"},
#         {"furigana": "ぎょ", "kanji": None, "translation": "Gyo"},
        
#         {"furigana": "ぎゃあ", "kanji": None, "translation": "Gyaa"},
#         {"furigana": "ぎゅう", "kanji": None, "translation": "Gyuu"},
#         {"furigana": "ぎょう", "kanji": None, "translation": "Gyou"},
        
#         {"furigana": "じゃ", "kanji": None, "translation": "Ja"},
#         {"furigana": "じゅ", "kanji": None, "translation": "Ju"},
#         {"furigana": "じょ", "kanji": None, "translation": "Jo"},
        
#         {"furigana": "じゃあ", "kanji": None, "translation": "Jaa"},
#         {"furigana": "じゅう", "kanji": None, "translation": "Juu"},
#         {"furigana": "じょう", "kanji": None, "translation": "Jou"},
        
#         {"furigana": "びゃ", "kanji": None, "translation": "Bya"},
#         {"furigana": "びゅ", "kanji": None, "translation": "Byu"},
#         {"furigana": "びょ", "kanji": None, "translation": "Byo"},
        
#         {"furigana": "びゃあ", "kanji": None, "translation": "Byaa"},
#         {"furigana": "びゅう", "kanji": None, "translation": "Byuu"},
#         {"furigana": "びょう", "kanji": None, "translation": "Byou"},
        
#         # Semi-Voiced Yōon
#         {"furigana": "ぴゃ", "kanji": None, "translation": "Pya"},
#         {"furigana": "ぴゅ", "kanji": None, "translation": "Pyu"},
#         {"furigana": "ぴょ", "kanji": None, "translation": "Pyo"},
        
#         {"furigana": "ぴゃあ", "kanji": None, "translation": "Pyaa"},
#         {"furigana": "ぴゅう", "kanji": None, "translation": "Pyuu"},
#         {"furigana": "ぴょう", "kanji": None, "translation": "Pyou"}
#     ]
# }




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

def text_to_romaji(text):
    # Convert Japanese text to a basic Romaji using unidecode
    return unidecode(text)

# Function to create WAV file for each question
def save_audio(question, output_folder="audio"):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Choose either 'furigana' or 'kanji' text for audio content
    text = question.get("kanji") or question.get("furigana")
    
    # Convert to a standardized Romaji filename and truncate if necessary
    romaji_filename = text_to_romaji(text)[:50]  # Truncate for length safety
    filename = f"{output_folder}/{romaji_filename}.wav"

    # Save the text to a WAV file
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
