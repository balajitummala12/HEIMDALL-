# ============================================================
# HEIMDALL SMART CONTEXT MANAGER
# ============================================================


class ContextManager:

    def __init__(self, max_messages=10, max_chars=12000):
        self.max_messages = max_messages
        self.max_chars = max_chars

    def build_context(self, conversation):

        # ----------------------------------------------------
        # No conversation
        # ----------------------------------------------------

        if not conversation:
            return []

        # ----------------------------------------------------
        # Get the most recent messages
        # ----------------------------------------------------

        recent = conversation[-self.max_messages:]

        selected = []
        total_chars = 0

        # ----------------------------------------------------
        # Add messages from newest to oldest
        # ----------------------------------------------------

        for message in reversed(recent):

            content = message.get("content", "")

            # Ignore empty messages
            if not content:
                continue

            message_size = len(content)

            # Stop if the context becomes too large
            if total_chars + message_size > self.max_chars:
                break

            # Insert at the beginning so the original order
            # of the conversation is preserved
            selected.insert(0, message)

            total_chars += message_size

        return selected


# ============================================================
# GLOBAL CONTEXT MANAGER
# ============================================================

context_manager = ContextManager()