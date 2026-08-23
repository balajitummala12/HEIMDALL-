from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import logging
import os
from contextlib import redirect_stdout, redirect_stderr

from core.database import load_memory

logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)

with open(os.devnull, "w") as f:
    with redirect_stdout(f), redirect_stderr(f):
        memory_model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            local_files_only=True
        )
def semantic_search(query, limit=5):

    memories = load_memory(limit=200)

    if not memories:
        return []

    query_embedding = memory_model.encode([query])

    scored = []

    for memory in memories:

        embedding = memory_model.encode(
            [memory["content"]]
        )

        score = cosine_similarity(
            query_embedding,
            embedding
        )[0][0]

        scored.append(
            (score, memory)
        )

    scored.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    return [
        memory
        for score, memory in scored[:limit]
    ]