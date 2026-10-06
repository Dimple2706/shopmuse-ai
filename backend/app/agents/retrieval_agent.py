from app.tools.catalog_tool import CatalogTool


class CandidateRetrievalAgent:

    def __init__(self):
        self.catalog = CatalogTool()

    def run(self, attributes):

        return self.catalog.search(
            category=attributes.get("category"),
            tags=attributes.get("tags"),
            max_price=attributes.get("max_price")
        )