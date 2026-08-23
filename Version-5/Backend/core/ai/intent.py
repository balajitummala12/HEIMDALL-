# ============================================================
# HEIMDALL INTENT DETECTOR
# ============================================================


class IntentDetector:

    def detect(self, prompt):

        text = prompt.lower().strip()

        # ----------------------------------------------------
        # EMPTY INPUT
        # ----------------------------------------------------

        if not text:
            return "empty"

        # ----------------------------------------------------
        # TRANSLATION
        # ----------------------------------------------------

        translation_keywords = [
            "translate",
            "translation",
            "translate this",
            "translate it",
            "in telugu",
            "in hindi",
            "in tamil",
            "in kannada",
            "in malayalam",
            "in bengali",
            "in english"
        ]

        if any(keyword in text for keyword in translation_keywords):
            return "translation"

        # ----------------------------------------------------
        # DEBUGGING
        # ----------------------------------------------------

        debugging_keywords = [
            "debug",
            "debugging",
            "find the bug",
            "find the error",
            "fix this error",
            "fix my code",
            "why is this code",
            "why does this code",
            "why doesn't this code",
            "what is wrong with this code",
            "error in my code",
            "code is not working",
            "code isn't working"
        ]

        if any(keyword in text for keyword in debugging_keywords):
            return "debugging"

        # ----------------------------------------------------
        # CODE MODIFICATION
        # ----------------------------------------------------

        modification_keywords = [
            "make it shorter",
            "make this shorter",
            "shorten this",
            "optimize this",
            "modify this",
            "modify the code",
            "change this",
            "change the code",
            "add a function",
            "add functions",
            "add functionality",
            "remove this",
            "remove the function",
            "convert this",
            "convert it",
            "rewrite this",
            "refactor this"
        ]

        if any(keyword in text for keyword in modification_keywords):
            return "modification"

        # ----------------------------------------------------
        # CODE REQUEST
        # ----------------------------------------------------

        coding_keywords = [
            "write a program",
            "write code",
            "give me code",
            "give me a program",
            "create a program",
            "create code",
            "python program",
            "python code",
            "c program",
            "c code",
            "c++ program",
            "c++ code",
            "java program",
            "java code",
            "javascript code",
            "html code",
            "sql query"
        ]

        if any(keyword in text for keyword in coding_keywords):
            return "coding"

        # ----------------------------------------------------
        # EXPLANATION
        # ----------------------------------------------------

        explanation_keywords = [
            "explain",
            "explain this",
            "explain it",
            "how does",
            "how do",
            "why does",
            "why do",
            "what is",
            "what are",
            "difference between",
            "compare",
            "teach me",
            "help me understand"
        ]

        if any(keyword in text for keyword in explanation_keywords):
            return "explanation"

        # ----------------------------------------------------
        # CASUAL CONVERSATION
        # ----------------------------------------------------

        casual_keywords = [
            "hello",
            "hi",
            "hey",
            "yo",
            "bro",
            "how are you",
            "good morning",
            "good afternoon",
            "good evening",
            "thanks",
            "thank you",
            "lol",
            "haha"
        ]

        if any(keyword in text for keyword in casual_keywords):
            return "casual"

        # ----------------------------------------------------
        # DEFAULT
        # ----------------------------------------------------

        return "general"


# ============================================================
# GLOBAL INTENT DETECTOR
# ============================================================

intent_detector = IntentDetector()