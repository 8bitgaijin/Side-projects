import pyttsx3

# Initialize the TTS engine
engine = pyttsx3.init()

# Set the voice to Japanese if available
for voice in engine.getProperty('voices'):
    if "japanese" in voice.languages or "Haruka" in voice.name:
        engine.setProperty('voice', voice.id)
        break
else:
    print("Japanese voice not found. Ensure you have a Japanese TTS voice installed.")

# Set properties like rate and volume if desired
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

# Sample text in Japanese
text = "こんにちは、ようこそ！お元気ですか？"  # "Hello, welcome! How are you?"

# Save the audio output directly to a WAV file
output_file = "output_greeting.wav"
engine.save_to_file(text, output_file)

# Run the engine to complete saving
engine.runAndWait()

print(f"Audio saved as '{output_file}'")
