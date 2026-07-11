from openai import OpenAI
import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer
import pyttsx3
import os
import datetime
import time
import requests


# ================= CONFIG =================
API_KEY = "YOUR GROQ API KEY HERE(I ABSTRACTED MINE)"
TAVILY_API_KEY = "YOUR TAVILY API KEY"

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


# ================= VOICE =================
engine = pyttsx3.init()
engine.setProperty('rate', 190)

def speak(text):
    print("⚡ HEIMDALL:", text)
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        pass


# ================= CLEAN RESPONSE =================
def clean_response(text):
    text = text.strip()
    if len(text) > 250:
        text = text[:250] + "..."
    return text


# ================= SYSTEM PROMPT =================
system_prompt = {
    "role": "system",
    "content": "You are HEIMDALL. Speak naturally, short and clear."
}


# ================= REAL-TIME SEARCH =================
def search_web(query):
    try:
        print("🌐 Searching Tavily...")

        url = "https://api.tavily.com/search"

        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "advanced",   # 🔥 important upgrade
            "max_results": 3
        }

        response = requests.post(url, json=payload, timeout=10)
        data = response.json()

        results = data.get("results", [])

        if not results:
            return None

        content = "\n".join([r["content"] for r in results])

        return content

    except Exception as e:
        print("TAVILY ERROR:", e)
        return None


# ================= REAL-TIME DETECTOR =================
def needs_realtime(query):
    keywords = [
        "today", "latest", "news", "current",
        "now", "recent", "update", "happening",
        "headlines", "live"
    ]
    return any(word in query.lower() for word in keywords)


# ================= VOSK =================
model = Model("vosk-model-small-en-us-0.15")
audio_queue = queue.Queue()

def audio_callback(indata, frames, time_info, status):
    audio_queue.put(bytes(indata))


def listen_voice():
    with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype='int16',
        channels=1,
        callback=audio_callback
    ):
        recognizer = KaldiRecognizer(model, 16000)
        print("🎤 Listening...")

        while True:
            data = audio_queue.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").strip()

                if text:
                    print("You:", text)
                    return text.lower()


def listen_text():
    return input("You: ").lower()


# ================= COMMANDS =================
def handle_command(cmd):

    if "time" in cmd:
        now = datetime.datetime.now().strftime("%H:%M")
        speak(f"It's {now}")
        return True

    if cmd.startswith("open "):
        app = cmd.replace("open ", "").strip()

        app_map = {
            "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "cmd": "cmd.exe",
            "vscode": r"C:\Users\balaji\AppData\Local\Programs\Microsoft VS Code\Code.exe",
            "whatsapp": "explorer shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App"
        }

        try:
            if app in app_map:
                os.startfile(app_map[app])
            else:
                os.system(f"start {app}")

            speak(f"Opening {app}")
            return True

        except Exception as e:
            print("APP ERROR:", e)
            speak("I couldn't open that.")
            return True

    if cmd.strip() in ["exit", "stop", "quit"]:
        speak("Shutting down. See you.")
        exit()

    return False


# ================= AI (HYBRID BRAIN) =================
def ask_ai(prompt):
    try:
        final_prompt = prompt

        if needs_realtime(prompt):
            print("🔥 USING REAL-TIME SEARCH")

            web_data = search_web(prompt)
            print("WEB DATA:", web_data[:200] if web_data else "None")

            if web_data:
                final_prompt = f"""
You are HEIMDALL.

You have LIVE internet data below.
IGNORE your old knowledge completely.

STRICT RULES:
- ONLY use the data below
- NEVER say you lack real-time info
- DO NOT use outdated knowledge

LIVE DATA:
{web_data}

QUESTION:
{prompt}

Give a short, clear answer:
"""
            else:
                print("⚠️ No real-time data found")

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": final_prompt}
            ],
            max_tokens=120,
            temperature=0.3   # 🔥 makes model obey instructions
        )

        return clean_response(response.choices[0].message.content)

    except Exception as e:
        print("AI ERROR:", e)
        return "Something went wrong."


# ================= STARTUP =================
print("\n⚔️  HEIMDALL INITIALIZING...\n")

speak("Initializing systems")
time.sleep(0.5)

speak("HEIMDALL is online")
time.sleep(0.5)

print("🧠 HEIMDALL is ready for the hunt.")


# ================= MODE =================
print("\nChoose mode:")
print("1. Voice 🎤")
print("2. Text ⌨️")

mode = input("Enter 1 or 2: ")


# ================= MAIN LOOP =================
while True:

    query = listen_voice() if mode == "1" else listen_text()

    if not query:
        continue

    print("🧠 Processing:", query)

    if handle_command(query):
        continue

    reply = ask_ai(query)
    speak(reply)
#-----FEATURES-----#
#what heimdall can do :#
#>listen, understand, and respond
#>answer questions instantly
#>execute commands on my system
#>open apps when asked
#>handle small tasks
#>act as a basic personal AI assistant#
