import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 185)


def speak(text):
    print(f"⚡ HEIMDALL: {text}")

    try:
        engine.say(text)
        engine.runAndWait()

    except Exception:
        pass
import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer

audio_queue = queue.Queue()

model = Model("models/vosk-model-small-en-us-0.15")
def audio_callback(indata, frames, time_info, status):
    audio_queue.put(bytes(indata))
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
def listen_text():
    return input("You: ").lower()