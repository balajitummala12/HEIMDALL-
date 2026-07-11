from openai import OpenAI
from config.settings import GROQ_API_KEY
if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found in .env"
    )
class GroqProvider:

    def __init__(self):

        self.client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )

    def chat(self, messages, model):

        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.6
        )

        return response.choices[0].message.content.strip()