class Reviewer:

    def review(self, products, intent):

        if not products:

            return {
                "approved": False,
                "needs_replan": True,
                "reason": "No products found",
                "suggestion": "Relax preferences or budget"
            }

        budget = intent.get("budget")

        preferences = [
            preference
            for preference in intent.get(
                "preferences",
                []
            )
            if preference not in [
                "cheaper",
                "premium"
            ]
        ]

        # --------------------------------
        # 1. HARD CONSTRAINT CHECK
        # --------------------------------

        hard_violations = []

        for item in products:

            product = item["product"]

            if budget and product["price"] > budget:

                hard_violations.append(
                    f"{product['name']} exceeds budget"
                )

        if hard_violations:

            return {
                "approved": False,
                "needs_replan": True,
                "reason": (
                    "Some recommendations violate "
                    "hard constraints"
                ),
                "violations": hard_violations,
                "suggestion": (
                    "Retrieve products again "
                    "while respecting the budget"
                )
            }

        # --------------------------------
        # 2. CHECK PREFERENCE COVERAGE
        # --------------------------------

        missing_preferences = []

        for preference in preferences:

            matched = False

            for item in products:

                product = item["product"]

                if preference in product["tags"]:

                    matched = True
                    break

            if not matched:

                missing_preferences.append(
                    preference
                )

        # --------------------------------
        # 3. REPLAN IF A PREFERENCE
        #    HAS ZERO REPRESENTATION
        # --------------------------------

        if missing_preferences:

            return {
                "approved": False,
                "needs_replan": True,
                "reason": (
                    "Some requested preferences "
                    "are not represented in the "
                    "recommendations"
                ),
                "missing_preferences":
                    missing_preferences,
                "suggestion": (
                    "Relax the least achievable "
                    "preference and search again"
                )
            }

        # --------------------------------
        # 4. APPROVED
        # --------------------------------

        return {
            "approved": True,
            "needs_replan": False,
            "reason": (
                "Recommendations satisfy "
                "the available constraints "
                "and represent the requested "
                "preferences"
            )
        }