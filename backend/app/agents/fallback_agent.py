class FallbackAgent:

    def __init__(self, catalog):
        self.catalog = catalog

    def run(self, intent):

        budget = intent.get("budget")
        category = intent.get("category")
        preferences = intent.get("preferences", [])

        products = [
            product
            for product in self.catalog.products
            if product["stock"]
        ]

        # -------------------------
        # Strategy 1:
        # Relax Budget
        # -------------------------

        if budget:

            alternatives = [
                product
                for product in products
                if product["price"] > budget
            ]

            if category:

                same_category = [
                    product
                    for product in alternatives
                    if product["category"] == category
                ]

                if same_category:
                    alternatives = same_category

            alternatives.sort(
                key=lambda product:
                product["price"] - budget
            )

            alternatives = alternatives[:3]

            if alternatives:

                lowest_price = alternatives[0]["price"]

                return {
                    "type": "fallback",
                    "fallback_used": True,
                    "strategy": "budget_relaxation",
                    "message": (
                        f"I couldn't find an exact "
                        f"{category or ''} match under "
                        f"${budget:.0f}. "
                        f"The closest options start at "
                        f"${lowest_price:.0f}. "
                        f"Would you like to relax your "
                        f"budget slightly?"
                    ),
                    "products": alternatives
                }

        # -------------------------
        # Strategy 2:
        # Relax Preferences
        # -------------------------

        if category:

            alternatives = [
                product
                for product in products
                if product["category"] == category
            ]

            if budget:

                alternatives = [
                    product
                    for product in alternatives
                    if product["price"] <= budget
                ]

            # Prefer products matching at least
            # one preference
            if preferences:

                matching = [
                    product
                    for product in alternatives
                    if any(
                        preference in product["tags"]
                        for preference in preferences
                    )
                ]

                if matching:
                    alternatives = matching

            alternatives.sort(
                key=lambda product:
                product["rating"],
                reverse=True
            )

            alternatives = alternatives[:3]

            if alternatives:

                return {
                    "type": "fallback",
                    "fallback_used": True,
                    "strategy": "preference_relaxation",
                    "message": (
                        "I couldn't find an exact match "
                        "with all your requirements. "
                        "Here are the closest options "
                        "while keeping your main category "
                        "and budget."
                    ),
                    "products": alternatives
                }

        # -------------------------
        # Strategy 3:
        # General Fallback
        # -------------------------

        products.sort(
            key=lambda product:
            product["rating"],
            reverse=True
        )

        return {
            "type": "fallback",
            "fallback_used": True,
            "strategy": "general",
            "message": (
                "I couldn't find an exact match. "
                "Here are some popular alternatives "
                "you may want to consider."
            ),
            "products": products[:3]
        }