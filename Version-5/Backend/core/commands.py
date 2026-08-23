from core.database import (
    save_profile,
    get_profile,
    save_topic,
    load_topics,
    get_memory_count
)

from core.voice import speak


class CommandHandler:

    def execute(self, command):

        command = command.lower().strip()

        if command == "memory stats":

            count = get_memory_count()

            speak(f"I currently remember {count} messages.")

            return True

        if command == "who am i":

            name = get_profile("name")

            if name:
                speak(f"You are {name}")
            else:
                speak("I don't know your name yet.")

            return True

        if command.startswith("set name "):

            name = command.replace(
                "set name ",
                ""
            )

            save_profile(
                "name",
                name
            )

            speak("Name saved.")

            return True

        if command.startswith("set college "):

            college = command.replace(
                "set college ",
                ""
            )

            save_profile(
                "college",
                college
            )

            speak("College saved.")

            return True

        if command.startswith("set goal "):

            goal = command.replace(
                "set goal ",
                ""
            )

            save_profile(
                "goal",
                goal
            )

            speak("Goal saved.")

            return True

        if command.startswith("completed "):

            topic = command.replace(
                "completed ",
                ""
            )

            save_topic(
                "General",
                topic
            )

            speak("Topic saved.")

            return True

        if command == "show topics":

            topics = load_topics()

            if not topics:

                speak("No topics saved.")

                return True

            result = ""

            for _, topic in topics:

                result += topic + ". "

            speak(result)

            return True

        return False


command_handler = CommandHandler()