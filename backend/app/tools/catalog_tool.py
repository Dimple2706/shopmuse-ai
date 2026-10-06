import json
import os


class CatalogTool:

    def __init__(self):

        path = os.path.join(
            os.path.dirname(__file__),
            "../data/products.json"
        )

        with open(path, "r") as file:
            self.products = json.load(file)

    def search(
        self,
        category=None,
        tags=None,
        max_price=None
    ):

        results = []

        for product in self.products:

            # Ignore out-of-stock products
            if not product["stock"]:
                continue

            # Category filter
            if category:
                if product["category"] != category:
                    continue

            # Budget filter
            if max_price:
                if product["price"] > max_price:
                    continue

            # Tag filter
            if tags:
                matches = any(
                    tag in product["tags"]
                    for tag in tags
                )

                if not matches:
                    continue

            results.append(product)

        return results