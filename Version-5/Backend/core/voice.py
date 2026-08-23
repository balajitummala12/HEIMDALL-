import pyttsx3
import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from pathlib import Path


# ============================================================
# TEXT TO SPEECH
# ============================================================

engine = pyttsx3.init()
engine.setProperty("rate", 185)


def speak(text):
    print(f"⚡ HEIMDALL: {text}")

    try:
        engine.say(text)
        engine.runAndWait()

    except Exception:
        pass


# ============================================================
# VOICE INPUT
# ============================================================

audio_queue = queue.Queue()


# Find the HEIMDALL Version-3 root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Vosk model location
MODEL_PATH = BASE_DIR / "models" / "vosk-model-small-en-us-0.15"


# Load Vosk model
model = Model(str(MODEL_PATH))


# ============================================================
# AUDIO CALLBACK
# ============================================================

def audio_callback(indata, frames, time_info, status):
    audio_queue.put(bytes(indata))


# ============================================================
# LISTEN TO VOICE
# ============================================================

def listen_voice():

    with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=audio_callback
    ):

        recognizer = KaldiRecognizer(model, 16000)

        print("🎤 Listening...")

        while True:

            data = audio_queue.get()

            if recognizer.AcceptWaveform(data):

                result = json.loads(
                    recognizer.Result()
                )

                text = result.get(
                    "text",
                    ""
                ).strip()

                if text:
                    print("You:", text)
                    return text.lower()


# ============================================================
# TEXT INPUT
# ============================================================

def listen_text():
    return input("You: ").lower()