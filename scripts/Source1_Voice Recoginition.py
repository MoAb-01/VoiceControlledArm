import sounddevice as sd
import numpy as np
from scipy.signal import resample
from vosk import Model, KaldiRecognizer
from fuzzywuzzy import process
import json
import sys

# Allow UTF-8 printing on some systems
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Predefined voice commands for each language
COMMANDS = {
    "english": ["open", "close", "stop", "Peace"],
    ##"arabic": ["افتح", "أغلق", "توقف", "ابدأ"],
    ##"turkish": ["aç", "kapat", "başlat", "durdur"]
}

def match_command(text, language):
    """
    Match the recognized text to the closest known command using fuzzy matching.
    """
    commands = COMMANDS.get(language, [])
    if not text or not commands:
        return None, 0
    match, score = process.extractOne(text, commands)
    return match, score

def main():
    model_paths = {
        'english': '/home/pi5g/Downloads/vosk-model-small-en-us-0.15',
        ## 'arabic':  '/home/pi5g/Downloads/vosk-model-ar-0.22-linto-1.1.0',
        ##'turkish': '/home/pi5g/Downloads/vosk-model-small-tr-0.3'
    }

    # Ask user for language choice
    choice = input("Which language would you like to speak? (English/Arabic/Turkish): ").strip().lower()
    if choice not in model_paths:
        print("Invalid choice. Please run again and pick English, Arabic, or Turkish.")
        return

    print(f"Loading {choice.capitalize()} model...")
    model = Model(model_paths[choice])
    rec = KaldiRecognizer(model, 16000)

    DURATION = 6  # seconds
    print(f"Please speak now in {choice.capitalize()} (recording {DURATION} seconds)...")
    audio = sd.rec(int(DURATION * 48000), samplerate=48000, channels=1, dtype='int16')
    sd.wait()

    # Resample to 16kHz
    audio_resampled = resample(audio.flatten(), int(DURATION * 16000)).astype(np.int16)
    data = audio_resampled.tobytes()

    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
    else:
        result = json.loads(rec.FinalResult())

    recognized_text = result.get("text", "").strip()
    print("\n=== Raw Recognition ===")
    print("You said (raw):", recognized_text)

    # Try to match against known commands
    matched_command, confidence = match_command(recognized_text, choice)

    if confidence > 75:
        print(f"\n✅ Matched Command: {matched_command} (Confidence: {confidence}%)")
        # You can now trigger robotic arm actions here based on `matched_command`
    else:
        print("\n⚠️ Could not confidently understand the command.")

if __name__ == "__main__":
    main()
