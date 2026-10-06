class CatalogMappingAgent:

    def run(self, intent):

        tags = []

        for preference in intent.get(
            "preferences",
            []
        ):

            if preference == "joint-friendly":
                tags.extend([
                    "joint-friendly",
                    "low-impact",
                    "supportive"
                ])

            elif preference == "lightweight":
                tags.append("lightweight")

            elif preference == "waterproof":
                tags.append("waterproof")

            elif preference == "comfortable":
                tags.append("comfortable")

        return {
            "category": intent.get("category"),
            "tags": tags,
            "max_price": intent.get("budget")
        }