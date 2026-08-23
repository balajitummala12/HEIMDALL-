# ============================================================
# HEIMDALL AI ROUTER
# ============================================================

class AIRouter:

    def __init__(self):
        pass

    def select_model(self, prompt):

        text = prompt.lower().strip()

        # ----------------------------------------------------
        # EMPTY INPUT
        # ----------------------------------------------------

        if not text:
            return "fast"

        # ----------------------------------------------------
        # DEEP REASONING / ANALYSIS
        # ----------------------------------------------------

        deep_keywords = [
            "deep dive",
            "deeply",
            "in depth",
            "analyze deeply",
            "detailed analysis",
            "reason through",
            "think through",
            "complex reasoning",
            "advanced reasoning",
            "architecture",
            "system design",
            "design an architecture",
            "optimize this architecture"
        ]

        if any(keyword in text for keyword in deep_keywords):
            return "deep"

        # ----------------------------------------------------
        # DEBUGGING
        # ----------------------------------------------------

        debugging_keywords = [
            "debug",
            "debugging",
            "find the bug",
            "find the error",
            "fix this error",
            "why is this code not working",
            "why doesn't this work",
            "what is wrong with this code",
            "error in my code",
            "fix my code"
        ]

        if any(keyword in text for keyword in debugging_keywords):
            return "deep"

        # ----------------------------------------------------
        # ADVANCED PROGRAMMING
        # ----------------------------------------------------

        programming_keywords = [
            "optimize this code",
            "optimize my code",
            "refactor this",
            "refactor my code",
            "improve this architecture",
            "memory leak",
            "race condition",
            "multithreading",
            "concurrency",
            "complex algorithm",
            "advanced algorithm",
            "time complexity",
            "space complexity",
            "design pattern",
            "distributed system"
        ]

        if any(keyword in text for keyword in programming_keywords):
            return "deep"

        # ----------------------------------------------------
        # COMPLEX MATH / REASONING
        # ----------------------------------------------------

        reasoning_keywords = [
            "prove that",
            "derive",
            "solve step by step",
            "mathematical proof",
            "proof",
            "complex calculation",
            "advanced mathematics",
            "probability problem",
            "linear algebra problem",
            "discrete mathematics problem"
        ]

        if any(keyword in text for keyword in reasoning_keywords):
            return "deep"

        # ----------------------------------------------------
        # LONG CODE INPUT
        # ----------------------------------------------------

        # If the user gives a large amount of code/text,
        # assume deeper analysis may be required.

        if len(text) > 4000:
            return "deep"

        # ----------------------------------------------------
        # EVERYTHING ELSE
        # ----------------------------------------------------

        # Normal conversation, translation, simple questions,
        # definitions, short explanations, etc.

        return "fast"


# Global router instance
router = AIRouter()