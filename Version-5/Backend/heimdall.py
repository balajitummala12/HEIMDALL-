# ============================================================
# HEIMDALL 5.0.0
# Smart Windows Console Input
# ============================================================

import sys
import time
import msvcrt

from core.services.chat_service import chat
from core.version import VERSION


# ============================================================
# SETTINGS
# ============================================================

# How long HEIMDALL waits after pressing Enter to see whether
# more pasted characters/lines are already waiting.
PASTE_WAIT = 0.12


# ============================================================
# CONSOLE INPUT
# ============================================================

def read_line():
    """
    Read one line manually from the Windows console.

    Unlike input(), this lets us inspect whether more pasted
    characters are already waiting after Enter.
    """

    chars = []

    while True:

        ch = msvcrt.getwch()

        # ----------------------------------------------------
        # ENTER
        # ----------------------------------------------------

        if ch in ("\r", "\n"):

            print()

            return "".join(chars)

        # ----------------------------------------------------
        # BACKSPACE
        # ----------------------------------------------------

        elif ch == "\b":

            if chars:
                chars.pop()

                # Remove character visually
                sys.stdout.write("\b \b")
                sys.stdout.flush()

        # ----------------------------------------------------
        # CTRL+C
        # ----------------------------------------------------

        elif ch == "\x03":

            raise KeyboardInterrupt

        # ----------------------------------------------------
        # NORMAL CHARACTER
        # ----------------------------------------------------

        else:

            chars.append(ch)

            sys.stdout.write(ch)
            sys.stdout.flush()


def more_input_available():

    """
    Wait briefly to determine whether additional characters
    are already waiting in the console input buffer.

    This is what allows pasted multiline text to be detected
    without requiring END or /send.
    """

    start = time.time()

    while time.time() - start < PASTE_WAIT:

        if msvcrt.kbhit():
            return True

        time.sleep(0.01)

    return False


def read_message():

    """
    Read a complete user message.

    Normal question:

        What is RAM?

    Multiline paste:

        Debug this code:

        x = 10

        print(y)

    Both become ONE message.
    """

    lines = []

    # --------------------------------------------------------
    # FIRST LINE
    # --------------------------------------------------------

    first_line = read_line()

    # Ignore completely empty input
    if not first_line.strip():
        return ""

    lines.append(first_line)

    # --------------------------------------------------------
    # CHECK FOR MORE PASTED INPUT
    # --------------------------------------------------------

    while more_input_available():

        line = read_line()

        # Keep blank lines.
        # They are important for code and paragraphs.
        lines.append(line)

    # --------------------------------------------------------
    # COMBINE MESSAGE
    # --------------------------------------------------------

    return "\n".join(lines).strip()


# ============================================================
# HEIMDALL STARTUP
# ============================================================

print("=" * 60)
print(f"⚔️ HEIMDALL {VERSION}")
print("=" * 60)

print("")


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    try:

        # ----------------------------------------------------
        # USER INPUT
        # ----------------------------------------------------

        print("You : ", end="")
        sys.stdout.flush()

        query = read_message()

        # ----------------------------------------------------
        # IGNORE EMPTY INPUT
        # ----------------------------------------------------

        if not query:
            continue

        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        if query.lower() in ["exit", "quit"]:

            print("\nHEIMDALL : Goodbye!")

            break

        # ----------------------------------------------------
        # SEND TO AI
        # ----------------------------------------------------

        try:

            reply = chat(query)

            if reply:

                print(f"\nHEIMDALL : {reply}")

        except Exception as e:

            print(f"\nERROR : {e}")

    # --------------------------------------------------------
    # CTRL+C
    # --------------------------------------------------------

    except KeyboardInterrupt:

        print("\n\nHEIMDALL : Goodbye!")

        break

    except Exception as e:

        print(f"\nERROR : {e}")