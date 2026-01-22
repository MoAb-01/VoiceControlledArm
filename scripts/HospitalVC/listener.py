import pyaudio
import json
import sys
import os
from vosk import Model, KaldiRecognizer
from fuzzywuzzy import process
from metaphone import doublemetaphone

# Ensure UTF-8 encoding for output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

#########################
# Active Listener Class
#########################
class ActiveListener:
    def __init__(self, model_path, commands, sensitivity=60):
        self.model_path = model_path
        self.commands = commands
        self.sensitivity = sensitivity
        self.sample_rate = 16000
        self.chunk_size = 4096
        self.p = None
        self.stream = None
        self.rec = None

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model not found at {self.model_path}. Please download it from https://alphacephei.com/vosk/models")

        print(f"Loading Vosk Model from '{self.model_path}'...")
        model = Model(self.model_path)
        self.rec = KaldiRecognizer(model, self.sample_rate)

    def _get_respeaker_index(self):
        """Internal method to find the Seeed ReSpeaker hardware index."""
        # If PyAudio hasn't been initialized yet, return default
        if not self.p:
            return None
            
        for i in range(self.p.get_device_count()):
            try:
                info = self.p.get_device_info_by_index(i)
                if "seeed" in info.get("name", "").lower():
                    print(f" Found! ReSpeaker at index {i}")
                    return i
            except Exception:
                continue
        print("ReSpeaker not found. Using default microphone.")
        return None

    def start(self):
        self.p = pyaudio.PyAudio()
        device_index = self._get_respeaker_index()

        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            input_device_index=device_index,
            frames_per_buffer=self.chunk_size
        )
        self.stream.start_stream()
        print("\nActiveListener Started. Speak now...")

    def stop(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.p:
            self.p.terminate()
        print("ActiveListener Stopped.")

    def _match_command(self, text):
        if not text:
            return None, 0

        # 1. Fuzzy Match
        match, score = process.extractOne(text, self.commands)
        if score >= self.sensitivity:
            return match, score

        # 2. Phonetic Match (fallback)
        words = text.split()
        for word in words:
            word_meta = doublemetaphone(word)[0]
            for cmd in self.commands:
                cmd_meta = doublemetaphone(cmd)[0]
                # Check if metaphone keys exist and match
                if word_meta and cmd_meta and word_meta == cmd_meta:
                    return cmd, "Phonetic"

        return None, 0

    def listen(self):
        if not self.stream:
            raise RuntimeError("Stream not started. Call start() first.")

        while True:
            try:
                data = self.stream.read(self.chunk_size, exception_on_overflow=False)

                if self.rec.AcceptWaveform(data):
                    result = json.loads(self.rec.Result())
                    text = result.get("text", "").strip()

                    if text:
                        print(f"Heard: '{text}'") # Debug print to see what it hears
                        cmd, score = self._match_command(text)
                        if cmd:
                            yield cmd, score
                        
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error in listener: {e}")
                break
