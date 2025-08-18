import sounddevice as sd
import numpy as np
from scipy.signal import resample
from vosk import Model, KaldiRecognizer
import json
import sys


# Predefined voice commands for each language
COMMANDS = {
    "english": ["open", "close", "stop", "peace"],
    "turkish": ["aÃ§mak"]
}

# Paths to Vosk models (adjust according to your system)
MODEL_PATHS = {
    "english": "/home/pi/Downloads/vosk-model-small-en-us-0.15",
    # "arabic": "/home/pi5g/Downloads/vosk-model-ar-0.22-linto-1.1.0",
     "turkish": "/home/pi/Downloads/vosk-model-small-tr-0.3"
}

def main():
    # Ask user to select a language
    choice = input("Which language would you like to speak? (English): ").strip().lower()
    if choice not in MODEL_PATHS:
        print("Invalid choice. Please run again with a valid language.")
        return

    # Load the appropriate model
    print(f"Loading {choice.capitalize()} model...")
    model = Model(MODEL_PATHS[choice])

    # Use grammar mode: only recognize defined commands
    grammar = json.dumps(COMMANDS[choice], ensure_ascii=False )
    rec = KaldiRecognizer(model, 16000, grammar)

    # Record audio from microphone
    DURATION = 6  # seconds
    print(f"Please speak now in {choice.capitalize()} (recording {DURATION} seconds)...")
    audio = sd.rec(int(DURATION * 48000), samplerate=48000, channels=1, dtype='int16')
    sd.wait()

    # Resample to 16kHz (Vosk expects 16kHz)
    audio_resampled = resample(audio.flatten(), int(DURATION * 16000)).astype(np.int16)
    data = audio_resampled.tobytes()

    # Process the audio
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
    else:
        result = json.loads(rec.FinalResult())

    recognized_text = result.get("text", "").strip()
    print("\n=== Recognized ===")
    if recognized_text:
        print(f"? You said: {recognized_text}")
        # You can act on the command here (like move robotic arm)
    else:
        print("?? No recognizable command detected.")

if __name__ == "__main__":
    main()

