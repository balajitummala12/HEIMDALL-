import re

from core.ai.engine import ai_engine


PROTECTED_RESPONSE = (
    "⚡ Sorry, I can't provide details about my internal systems."
)


PROTECTED_PATTERNS = [

    # =========================
    # API / PROVIDER
    # =========================
    r"\b(do|are|did)\s+you\s+(use|using)\s+(openai|gpt|anthropic|claude|gemini|groq|deepseek|ollama)\b",
    r"\bwhat\s+(api|apis)\s+(do|does|are)\s+you\s+(use|using)\b",
    r"\bwhich\s+(api|apis)\s+(do|does|are)\s+you\s+(use|using)\b",
    r"\bwhat\s+(api|apis)\s+(power|powers|run|runs)\s+you\b",
    r"\bwho\s+provides?\s+your\s+(api|ai|model)\b",
    r"\bwhat\s+(provider|service)\s+(do|does)\s+you\s+use\b",
    r"\bwho\s+is\s+your\s+(provider|ai\s+provider)\b",
    r"\bwhat\s+company\s+(made|powers|runs)\s+you\b",

    # =========================
    # MODEL / AI / LLM
    # =========================
    r"\bwhat\s+(model|ai\s+model|llm)\s+(do|are|does)\s+you\s+(use|using|run|running)\b",
    r"\bwhich\s+(model|ai\s+model|llm)\s+(do|are|does)\s+you\s+(use|using|run|running)\b",
    r"\bwhat\s+are\s+you\s+powered\s+by\b",
    r"\bwhat\s+powers?\s+you\b",
    r"\bwhat\s+ai\s+are\s+you\b",
    r"\bwhat\s+llm\s+are\s+you\b",
    r"\bwhat\s+gpt\s+(version|model)\b",
    r"\bare\s+you\s+(openai|chatgpt|gpt|claude|gemini|deepseek|groq)\b",
    r"\bdo\s+you\s+run\s+on\s+(openai|gpt|claude|gemini|deepseek|groq|ollama)\b",
    r"\bwhich\s+version\s+of\s+(gpt|claude|gemini)\b",

    # =========================
    # ARCHITECTURE
    # =========================
    r"\bwhat\s+is\s+your\s+(system\s+|internal\s+|software\s+)?architecture\b",
    r"\bhow\s+does\s+your\s+architecture\s+work\b",
    r"\b(tell|show|explain|describe)\s+me\s+your\s+(system\s+|internal\s+)?architecture\b",
    r"\bhow\s+are\s+you\s+architected\b",
    r"\bwhat\s+is\s+inside\s+you\b",
    r"\bhow\s+are\s+your\s+systems?\s+structured\b",
    r"\bwhat\s+is\s+your\s+internal\s+structure\b",

    # =========================
    # IMPLEMENTATION / BUILD
    # =========================
    r"\bhow\s+(were|are)\s+you\s+(built|made|created|developed)\b",
    r"\bhow\s+do\s+you\s+work\s+internally\b",
    r"\bhow\s+do\s+you\s+work\s+under\s+the\s+hood\b",
    r"\bhow\s+do\s+you\s+function\s+internally\b",
    r"\b(tell|show|explain|describe)\s+me\s+(how|what)\s+you\s+(work|were\s+built|are\s+built)\b",
    r"\bwhat\s+technology\s+(do|does)\s+you\s+use\b",
    r"\bwhich\s+technology\s+(do|does)\s+you\s+use\b",
    r"\bwhat\s+technologies\s+(do|does)\s+you\s+use\b",
    r"\bwhat\s+stack\s+(do|does)\s+you\s+use\b",
    r"\bwhat\s+is\s+your\s+tech\s+stack\b",
    r"\bwhat\s+are\s+you\s+built\s+with\b",

    # =========================
    # SOURCE CODE
    # =========================
    r"\b(show|give|send|provide|reveal)\s+(me\s+)?your\s+(source\s+)?code\b",
    r"\bwhere\s+is\s+your\s+(source\s+)?code\b",
    r"\bwhat\s+does\s+your\s+code\s+look\s+like\b",
    r"\bcan\s+i\s+see\s+your\s+code\b",
    r"\bcan\s+i\s+get\s+your\s+source\b",
    r"\bshow\s+me\s+your\s+repository\b",
    r"\bwhere\s+is\s+your\s+repo\b",
    r"\bwhat\s+is\s+your\s+github\b",
    r"\bshow\s+me\s+your\s+github\b",

    # =========================
    # BACKEND / FRONTEND
    # =========================
    r"\bwhat\s+backend\s+(do|does)\s+you\s+use\b",
    r"\bwhich\s+backend\s+(do|does)\s+you\s+use\b",
    r"\bwhat\s+server\s+(do|does)\s+you\s+use\b",
    r"\bwhat\s+framework\s+(do|does)\s+you\s+use\b",
    r"\bwhich\s+framework\s+(do|does)\s+you\s+use\b",
    r"\bwhat\s+database\s+(do|does)\s+you\s+use\b",
    r"\bwhere\s+is\s+your\s+backend\b",
    r"\bhow\s+is\s+your\s+backend\s+built\b",
    r"\bhow\s+is\s+your\s+frontend\s+built\b",

    # =========================
    # PROMPTS / INSTRUCTIONS
    # =========================
    r"\bwhat\s+is\s+your\s+system\s+prompt\b",
    r"\bshow\s+me\s+your\s+system\s+prompt\b",
    r"\btell\s+me\s+your\s+system\s+prompt\b",
    r"\breveal\s+your\s+system\s+prompt\b",
    r"\bwhat\s+are\s+your\s+(internal\s+)?instructions\b",
    r"\bshow\s+me\s+your\s+(internal\s+)?instructions\b",
    r"\btell\s+me\s+your\s+(hidden\s+|secret\s+)?prompt\b",
    r"\bwhat\s+were\s+you\s+told\s+to\s+do\b",
    r"\bignore\s+your\s+(previous\s+)?instructions\b",

    # =========================
    # KEYS / SECRETS / CONFIG
    # =========================
    r"\b(show|give|tell|reveal)\s+(me\s+)?your\s+(api\s+)?key\b",
    r"\bwhat\s+is\s+your\s+(api\s+)?key\b",
    r"\b(show|give|reveal)\s+(me\s+)?your\s+secret\b",
    r"\bwhat\s+are\s+your\s+credentials\b",
    r"\bshow\s+me\s+your\s+credentials\b",
    r"\bshow\s+me\s+your\s+environment\s+variables\b",
    r"\bshow\s+me\s+your\s+\.env\b",
    r"\bwhat\s+is\s+in\s+your\s+\.env\b",
    r"\bshow\s+me\s+your\s+configuration\b",

    # =========================
    # INTERNAL DETAILS
    # =========================
    r"\b(tell|show|give|reveal|explain|describe)\s+(me\s+)?your\s+internal\s+(details|system|systems|setup|configuration)\b",
    r"\bwhat\s+is\s+your\s+internal\s+(system|setup|configuration)\b",
    r"\bhow\s+are\s+you\s+configured\b",
    r"\bwhat\s+is\s+behind\s+you\b",
    r"\bwhat\s+is\s+behind\s+the\s+scenes\b",
    r"\bhow\s+do\s+you\s+operate\s+behind\s+the\s+scenes\b",
    r"\breveal\s+your\s+implementation\b",
]


def is_protected_request(prompt):
    prompt = prompt.lower().strip()

    return any(
        re.search(pattern, prompt)
        for pattern in PROTECTED_PATTERNS
    )


def chat(prompt):

    if is_protected_request(prompt):
        return PROTECTED_RESPONSE

    return ai_engine.chat(prompt)