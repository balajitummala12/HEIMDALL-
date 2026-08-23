# ============================================================
# HEIMDALL RESPONSE CONTROLLER
# ============================================================


class ResponseController:

    def __init__(self):
        pass

    def control(self, response, intent, prompt):

        if not response:
            return ""

        response = response.strip()

        # ----------------------------------------------------
        # TRANSLATION
        # ----------------------------------------------------

        if intent == "translation":
            return response

        # ----------------------------------------------------
        # CASUAL CHAT
        # ----------------------------------------------------

        if intent == "casual":
            return response

        # ----------------------------------------------------
        # DEBUGGING
        # ----------------------------------------------------

        if intent == "debugging":
            return response

        # ----------------------------------------------------
        # CODING
        # ----------------------------------------------------

        if intent == "coding":
            return response

        # ----------------------------------------------------
        # USER EXPLICITLY REQUESTED SHORT ANSWER
        # ----------------------------------------------------

        short_words = [
            "short",
            "brief",
            "quick",
            "one line",
            "just tell me"
        ]

        prompt_lower = prompt.lower()

        if any(word in prompt_lower for word in short_words):
            return response

        # ----------------------------------------------------
        # DEFAULT
        # ----------------------------------------------------

        return response


# ============================================================
# GLOBAL RESPONSE CONTROLLER
# ============================================================

response_controller = ResponseController()