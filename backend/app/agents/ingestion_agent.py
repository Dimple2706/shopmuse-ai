class QueryIngestionAgent:

    def run(self, query: str) -> str:
        fillers = ["hey", "hello", "hi", "um", "uh", "so"]

        words = query.lower().split()

        cleaned = [
            word for word in words
            if word not in fillers
        ]

        return " ".join(cleaned)