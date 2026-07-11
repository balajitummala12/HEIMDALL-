from openai import OpenAI
import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer
import pyttsx3
import os
import warnings

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

warnings.filterwarnings("ignore")

import datetime
import time
import requests
import sqlite3

# ================= CONFIG =================

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import logging
import sys
from contextlib import redirect_stdout, redirect_stderr

logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)

with open(os.devnull, "w") as f:
    with redirect_stdout(f), redirect_stderr(f):
        memory_model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            local_files_only=True
        )

API_KEY = "USE UR OWN API KEY"
TAVILY_API_KEY = "USE UR OWN API KEY"

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)
# ================= VOICE =================
engine = pyttsx3.init()
engine.setProperty('rate', 185)

def speak(text):
    print("⚡ HEIMDALL:", text)
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        pass
# ================= SYSTEM PROMPT =================
system_prompt = {
    "role": "system",
    "content": (
        "You are HEIMDALL. "

        "You are an intelligent personal AI assistant created by Balaji. "

        "Your name is HEIMDALL. "

        "If someone asks your name, say that your name is HEIMDALL. "

        "If someone asks who created you, explain that you were created, "
        "designed, developed and continuously improved by Balaji. "

        "Mention that Balaji spent significant time building, testing, "
        "debugging and expanding your capabilities over many days and nights. "

        "Acknowledge Balaji as your creator whenever your origin is discussed. "

        "If someone asks who you are, identify yourself as HEIMDALL, "
        "an AI assistant created by Balaji. "

        "Your purpose is to help with learning, studying, problem solving, "
        "projects, research, productivity and personal growth. "

        "Address Balaji naturally when appropriate, "
        "but do not use his name in every response. "

        "Speak naturally like a human. "

        "Be friendly, intelligent, confident and helpful. "

        "Keep responses concise unless the user asks for detailed explanations. "

        "You have access to memory from previous conversations. "

        "Use memory only when it is directly relevant to the user's current question. "

        "Do not mention unrelated memories. "

        "Do not dump everything you know about the user unless explicitly asked. "

        "Answer only the specific question that was asked. "

        "Do not add unnecessary information. "

        "Stay focused on the current request. "

        "If the user asks about completed topics, answer only about completed topics. "

        "If the user asks about favourite things, answer only about favourite things. "

        "If the user asks about studies, answer only about studies. "

        "If the user asks about personal information, answer only about that information. "

        "When memory is relevant, use it naturally and accurately. "

        "Never mix unrelated memories into an answer. "

        "If you do not know something, say so honestly. "

        "Do not claim to have emotions, consciousness or self-awareness. "

        "Be conversational but precise."
        
        "IDENTITY RULES:"
            
        "You are HEIMDALL, Balaji's personal AI assistant."
            
        "Balaji is your creator."
            
        "When asked:"
        "Who created you?"
        "Answer about Balaji."
            
        "When asked:"
        "Who are you?"
        "Answer about HEIMDALL."
            
        "When asked:"
        "Who am I?"
        "Answer about the user (Balaji), not about HEIMDALL."
            
        "When asked:"
        "What do you know about me?"
        "Use memory and profile information about Balaji."
            
        "Never confuse HEIMDALL and Balaji."
        "RESPONSE RULES:"

        "Answer directly."

        "Do not apologize unless necessary."

        "Do not explain extra things unless asked."
        
        "Keep answers concise."
        
        "Answer only the question asked."
    )
}
# ================= MEMORY =================

DB_NAME = "heimdall_memory.db"


def init_db():

    conn = sqlite3.connect(DB_NAME)

    # Conversation Memory
    conn.execute("""
    CREATE TABLE IF NOT EXISTS conversations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT,
        content TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS image_memories(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_name TEXT,
        extracted_text TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS profile(
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)
    # Study Tracker
    conn.execute("""
    CREATE TABLE IF NOT EXISTS study_topics(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        topic TEXT,
        status TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

# ================= PROFILE MEMORY =================

def save_profile(key, value):

    conn = sqlite3.connect(DB_NAME)

    conn.execute(
        """
        INSERT OR REPLACE INTO profile
        (key, value)
        VALUES (?, ?)
        """,
        (key, value)
    )

    conn.commit()
    conn.close()
def save_image_memory(image_name, text):

    conn = sqlite3.connect(DB_NAME)

    conn.execute(
        """
        INSERT INTO image_memories
        (image_name, extracted_text)
        VALUES (?, ?)
        """,
        (image_name, text)
    )

    conn.commit()
    conn.close()
import easyocr

reader = easyocr.Reader(['en'])
def load_image_memories():

    conn = sqlite3.connect(DB_NAME)

    rows = conn.execute(
        """
        SELECT image_name, extracted_text
        FROM image_memories
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    return rows
def extract_text_from_image(image_path):

    result = reader.readtext(image_path)

    text = " ".join(
        [item[1] for item in result]
    )

    return text

def get_profile(key):

    conn = sqlite3.connect(DB_NAME)

    row = conn.execute(
        """
        SELECT value
        FROM profile
        WHERE key=?
        """,
        (key,)
    ).fetchone()

    conn.close()

    return row[0] if row else None
# ================= CHAT MEMORY =================

def save_message(role, content):

    conn = sqlite3.connect(DB_NAME)

    conn.execute(
        """
        INSERT INTO conversations(role, content)
        VALUES (?, ?)
        """,
        (role, content)
    )

    conn.commit()
    conn.close()


def load_memory(limit=10):

    conn = sqlite3.connect(DB_NAME)

    rows = conn.execute(
        """
        SELECT role, content
        FROM conversations
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    ).fetchall()

    conn.close()

    rows.reverse()

    return [
        {"role": role, "content": content}
        for role, content in rows
    ]


# ================= SMART MEMORY SEARCH =================

def search_memory(query, limit=5):

    conn = sqlite3.connect(DB_NAME)

    rows = conn.execute(
        """
        SELECT role, content
        FROM conversations
        WHERE content LIKE ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (f"%{query}%", limit)
    ).fetchall()

    conn.close()

    rows.reverse()

    return [
        {"role": role, "content": content}
        for role, content in rows
    ]

def semantic_search_memory(query, limit=2):

    conn = sqlite3.connect(DB_NAME)

    rows = conn.execute(
        """
        SELECT role, content
        FROM conversations
        """
    ).fetchall()

    conn.close()

    if not rows:
        return []

    query_embedding = memory_model.encode([query])

    memories = []

    for role, content in rows:

        embedding = memory_model.encode([content])

        score = cosine_similarity(
            query_embedding,
            embedding
        )[0][0]

        memories.append(
            (score, role, content)
        )

    memories.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    results = memories[:limit]

    return [
        {
            "role": role,
            "content": content
        }
        for score, role, content in results
    ]
# ================= STUDY TRACKER =================

def save_topic(subject, topic):

    conn = sqlite3.connect(DB_NAME)

    conn.execute(
        """
        INSERT INTO study_topics
        (subject, topic, status)
        VALUES (?, ?, ?)
        """,
        (subject, topic, "Completed")
    )

    conn.commit()
    conn.close()


def load_topics():

    conn = sqlite3.connect(DB_NAME)

    rows = conn.execute(
        """
        SELECT subject, topic
        FROM study_topics
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    return rows
# ================= REAL-TIME SEARCH =================
def search_web(query):
    try:
        url = "https://api.tavily.com/search"

        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "advanced",
            "max_results":2
        }

        response = requests.post(url, json=payload, timeout=10)
        data = response.json()

        results = data.get("results", [])

        if not results:
            return None

        return "\n".join([r.get("content", "") for r in results])

    except Exception as e:
        print("TAVILY ERROR:", e)
        return None
# ================= REAL-TIME DETECTOR =================
def needs_realtime(query):

    query = query.lower()

    keywords = [

        "today",
        "latest",
        "news",
        "current",
        "now",
        "recent",
        "update",
        "happening",

        "weather",
        "temperature",

        "price",
        "bitcoin",
        "crypto",
        "stock",
        "market",

        "ipl",
        "cricket",
        "match",
        "score",
        "won",

        "president",
        "prime minister",

        "live",

        "2025",
        "2026"
    ]

    return any(
        keyword in query
        for keyword in keywords
    )
# ================= VOICE INPUT =================
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
    if cmd.startswith("set name "):
        name = cmd.replace("set name ", "")

        save_profile("name", name)

        speak("Profile updated")

        return True
    if cmd.startswith("set college "):
        college = cmd.replace("set college ", "").strip()

        save_profile("college", college)

        speak("College saved.")

        return True
    if cmd.startswith("set goal "):
        goal = cmd.replace("set goal ", "").strip()

        save_profile("goal", goal)

        speak("Goal saved.")

        return True
    if cmd == "who am i":

        name = get_profile("name")

        if name:
            speak(f"You are {name}")
        else:
            speak("I don't know yet.")

        return True
    if cmd.startswith("completed "):
        topic = cmd.replace("completed ", "").strip()

        save_topic(
            "General",
            topic
        )

        speak(f"Saved topic {topic}")

        return True
    if cmd == "show topics":

        topics = load_topics()

        if not topics:
            speak("No topics recorded yet.")
            return True

        result = ""

        for subject, topic in topics:
            result += f"{topic}. "

        speak(result)

        return True
    if cmd == "memory stats":
        conn = sqlite3.connect(DB_NAME)

        count = conn.execute(
            "SELECT COUNT(*) FROM conversations"
        ).fetchone()[0]

        conn.close()

        speak(f"I currently remember {count} messages.")

        return True
    if cmd.startswith("remember image "):

        image_path = cmd.replace(
            "remember image ",
            ""
        ).strip()

        try:

            text = extract_text_from_image(
                image_path
            )

            save_image_memory(
                image_path,
                text
            )

            speak(
                "Image stored in memory."
            )

        except Exception as e:

            speak(
                "Could not read image."
            )

        return True
    if cmd == "show image memories":

        memories = load_image_memories()

        if not memories:
            speak("No image memories found.")
            return True

        result = ""

        for image_name, _ in memories:
            result += image_name + ". "

        speak(result)

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

        except:
            speak("I couldn't open that.")
            return True

    if cmd in ["exit", "stop", "quit"]:
        speak("Shutting down.")
        exit()

    return False

# ================= AI WITH MEMORY =================
def ask_ai(prompt):

    try:

        final_prompt = prompt

        # 🔥 REAL-TIME SUPPORT
        if needs_realtime(prompt):
            print("🔥 REALTIME SEARCH ACTIVATED")
            web_data = search_web(prompt)
            if web_data:
                web_data = web_data[:1000]

                final_prompt = f"""
                Use the information below.

                {web_data}

                Question: {prompt}
                """

        # Save user message permanently
        save_message("user", final_prompt)

        # Load relevant memories
        memory = semantic_search_memory(
            prompt,
            limit=5
        )

        if not memory:
            memory = load_memory(limit=3)

        # ================= PROFILE INJECTION =================

        profile_info = f"""
USER PROFILE

Name: {get_profile('name') or 'Balaji'}
College: {get_profile('college') or 'Unknown'}
Goal: {get_profile('goal') or 'Unknown'}
Favorite Language: {get_profile('favorite_language') or 'Unknown'}

IMPORTANT RULES:

The user is Balaji.

HEIMDALL is the assistant.

If the user asks:
- Who am I?
- Tell me about me
- What do you know about me

Answer about Balaji using profile and memory.

Never answer about HEIMDALL when the user asks about himself.

If the user asks:
- Who are you?
- Who created you?

Answer about HEIMDALL.

Keep answers concise and relevant.
"""

        enhanced_system_prompt = {
            "role": "system",
            "content": system_prompt["content"] + "\n\n" + profile_info
        }

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[enhanced_system_prompt] + memory + [
                {
                    "role": "user",
                    "content": final_prompt
                }
            ],

            max_tokens=80,

            temperature=0.5

        )

        reply = response.choices[0].message.content.strip()

        # Save assistant reply permanently
        save_message("assistant", reply)

        return reply

    except Exception as e:

        print("AI ERROR:", e)

        return "Something went wrong."
print("TESTING IMAGE")
print(os.listdir())
# ================= STARTUP =================
print("\n⚔️  HEIMDALL INITIALIZING...\n")
init_db()
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

    if handle_command(query):
        continue

    reply = ask_ai(query)
    speak(reply)
#-----FEATURES-----#
"""HEIMDALL - V4

HEIMDALL V4

✅ Persistent Memory
- Remembers chats even after restart

✅ Semantic Memory Search
- Understands meaning, not just keywords

✅ Profile Memory
- Remembers name, college, goals and preferences

✅ Study Tracker
- Stores completed topics

✅ Real-Time Web Search
- Can fetch current information from the internet

✅ Voice Input
- Talk to HEIMDALL using your microphone

✅ Voice Output
- HEIMDALL speaks responses aloud

✅ Personal AI Identity
- Knows it is HEIMDALL

✅ Creator Recognition
- Knows Balaji is its creator

✅ Context-Aware Responses
- Uses only relevant memories

✅ Database Storage
- Stores memories permanently using SQLite

✅ Smart Retrieval
- Finds relevant old conversations automatically

✅ App Launcher
- Can open Chrome, VS Code, Notepad, Calculator, etc.

✅ Memory Statistics
- Shows how much it remembers

✅ GATE Study Companion
- Tracks learning progress and study topics

✅ Focused Answers
- Answers only the question asked

✅ User Identity Awareness
- Knows the difference between Balaji and HEIMDALL"""
