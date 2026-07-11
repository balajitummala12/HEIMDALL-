import requests
from core.config import TAVILY_API_KEY


class WebSearch:

    def __init__(self):
        self.url = "https://api.tavily.com/search"

    def search(self, query, max_results=2):

        try:

            payload = {
                "api_key": TAVILY_API_KEY,
                "query": query,
                "search_depth": "advanced",
                "max_results": max_results
            }

            response = requests.post(
                self.url,
                json=payload,
                timeout=10
            )

            data = response.json()

            results = data.get("results", [])

            if not results:
                return None

            return "\n".join(
                r.get("content", "")
                for r in results
            )

        except Exception as e:
            print("Search Error:", e)
            return None
search_engine = WebSearch()
def needs_realtime(query):

    query = query.lower()

    keywords = [

        "today",
        "latest",
        "news",
        "current",
        "now",
        "recent",
        "update",
        "happening",

        "weather",
        "temperature",

        "price",
        "bitcoin",
        "crypto",
        "stock",
        "market",

        "ipl",
        "cricket",
        "match",
        "score",

        "president",
        "prime minister",

        "live",

        "2025",
        "2026",
        "2027"
    ]

    return any(
        keyword in query
        for keyword in keywords
    )