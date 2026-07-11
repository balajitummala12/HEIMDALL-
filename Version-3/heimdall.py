from core.services.chat_service import chat
from core.version import VERSION

print("=" * 60)
print(f"⚔️ HEIMDALL {VERSION}")
print("=" * 60)

while True:
    query = input("\nYou : ").strip()

    if query.lower() in ["exit", "quit"]:
        print("\nHEIMDALL : Goodbye!")
        break

    try:
        reply = chat(query)
        print(f"\nHEIMDALL : {reply}")

    except Exception as e:
        print(f"\nERROR : {e}")