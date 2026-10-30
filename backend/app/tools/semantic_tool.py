
"""Optional ChromaDB semantic search for ShopMuse AI."""

import os
from pathlib import Path


class SemanticSearchTool:
    def __init__(self):
        self.enabled = os.getenv(
            "ENABLE_SEMANTIC_SEARCH", "true"
        ).lower() == "true"

        self.client = None
        self.collection = None

        if not self.enabled:
            return

        import chromadb
        from chromadb.utils.embedding_functions import (
            SentenceTransformerEmbeddingFunction,
        )

        path = os.getenv(
            "CHROMA_PATH",
            str(Path(__file__).resolve().parents[2] / "chroma_data"),
        )

        self.client = chromadb.PersistentClient(path=path)

        model = os.getenv(
            "EMBEDDING_MODEL", "all-MiniLM-L6-v2"
        )

        embedding_function = SentenceTransformerEmbeddingFunction(
            model_name=model
        )

        self.collection = self.client.get_or_create_collection(
            "shopmuse_products",
            embedding_function=embedding_function,
        )

    @staticmethod
    def document(p):
        return (
            f"Product: {p['name']}. "
            f"Category: {p['category']}. "
            f"Features: {', '.join(p.get('tags', []))}."
        )

    def index(self, products):
        if not self.enabled or self.collection is None:
            return 0

        if not products:
            return 0

        for i in range(0, len(products), 100):
            batch = products[i:i + 100]

            self.collection.upsert(
                ids=[str(p["id"]) for p in batch],
                documents=[self.document(p) for p in batch],
                metadatas=[
                    {"category": str(p["category"])}
                    for p in batch
                ],
            )

        return len(products)

    def search(self, query, category=None, limit=30):
        if not self.enabled or self.collection is None:
            return []

        if not query.strip() or self.collection.count() == 0:
            return []

        args = {
            "query_texts": [query[:1000]],
            "n_results": min(limit, self.collection.count()),
        }

        if category:
            args["where"] = {"category": category}

        try:
            result = self.collection.query(**args)
        except Exception:
            return []

        return [
            {
                "id": product_id,
                "distance": distance,
                "context": doc,
            }
            for product_id, distance, doc in zip(
                result["ids"][0],
                result["distances"][0],
                result["documents"][0],
            )
        ]
