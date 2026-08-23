from openai import OpenAI
from config.settings import GROQ_API_KEY


class GroqProvider:

    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in .env")

        self.client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )

    def chat(self, messages, model):

        # ----------------------------------------------------
        # FAST BRAIN
        # ----------------------------------------------------

        if model == "openai/gpt-oss-20b":

            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.4,
                reasoning_effort="low",
                max_completion_tokens=500
            )

        # ----------------------------------------------------
        # DEEP BRAIN
        # ----------------------------------------------------

        else:

            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.5,
                reasoning_effort="medium",
                max_completion_tokens=1200
            )

        content = response.choices[0].message.content

        if not content:
            return "I couldn't generate a response."

        return content.strip()