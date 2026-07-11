from core.ai.providers import GroqProvider
from config.prompts import SYSTEM_PROMPT
from config.models import MODEL_NAME

class AIEngine:

    def __init__(self):

        self.provider = GroqProvider()

    def chat(self, prompt):

        messages = [

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": prompt
            }

        ]

        return self.provider.chat(
            messages,
            MODEL_NAME
        )


ai_engine = AIEngine()