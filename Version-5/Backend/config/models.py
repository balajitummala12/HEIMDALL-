import os


# ============================================================
# HEIMDALL AI MODELS
# ============================================================

# FAST BRAIN
# ------------------------------------------------------------
# Used for:
# - Normal conversation
# - Simple questions
# - Translations
# - Short explanations
# - Simple coding
#
# Groq currently lists GPT-OSS 20B at ~1000 tokens/sec.
# ------------------------------------------------------------

FAST_MODEL = os.getenv(
    "FAST_MODEL",
    "openai/gpt-oss-20b"
)


# DEEP BRAIN
# ------------------------------------------------------------
# Used for:
# - Complex coding
# - Debugging
# - Advanced reasoning
# - Mathematics
# - Architecture
# - Difficult analysis
#
# Groq currently lists GPT-OSS 120B at ~500 tokens/sec.
# ------------------------------------------------------------

DEEP_MODEL = os.getenv(
    "DEEP_MODEL",
    "openai/gpt-oss-120b"
)


# DEFAULT MODEL
# ------------------------------------------------------------
# Kept for compatibility with existing HEIMDALL modules.
# Normal requests use the Fast Brain unless the router
# selects the Deep Brain.
# ------------------------------------------------------------

MODEL_NAME = FAST_MODEL