class RankingAgent:

    def run(self, products, intent):

        ranked = []

        preferences = intent.get(
            "preferences",
            []
        )

        budget = intent.get(
            "budget"
        )

        category = intent.get(
            "category"
        )

        # Number of meaningful preferences
        meaningful_preferences = [
            preference
            for preference in preferences
            if preference not in [
                "cheaper",
                "premium"
            ]
        ]

        for product in products:

            score = 0
            reasons = []

            # -------------------------
            # 1. Category Match
            # -------------------------

            if category == product["category"]:

                score += 25

                reasons.append(
                    "matches your activity"
                )

            # -------------------------
            # 2. Preference Match
            # -------------------------

            matched_preferences = 0

            for preference in meaningful_preferences:

                if preference in product["tags"]:

                    matched_preferences += 1

                    reasons.append(
                        f"matches your "
                        f"{preference} preference"
                    )

            # Give preference points
            # based on how many match.
            if meaningful_preferences:

                preference_score = (
                    matched_preferences
                    / len(meaningful_preferences)
                ) * 45

                score += preference_score

            # -------------------------
            # 3. Budget Fit
            # -------------------------

            if budget:

                if product["price"] <= budget:

                    # Higher score when price is
                    # comfortably within budget.
                    budget_ratio = (
                        product["price"]
                        / budget
                    )

                    budget_score = (
                        20
                        * (1 - budget_ratio)
                    )

                    score += budget_score

                    reasons.append(
                        "within your budget"
                    )

                else:

                    # This normally won't happen
                    # because retrieval filters it.
                    score -= 20

            # -------------------------
            # 4. Rating
            # -------------------------

            rating_score = (
                product["rating"] / 5
            ) * 10

            score += rating_score

            # -------------------------
            # 5. Cheaper Preference
            # -------------------------

            if "cheaper" in preferences:

                if budget:

                    if product["price"] <= budget * 0.75:

                        score += 10

                        reasons.append(
                            "especially affordable"
                        )

            # -------------------------
            # 6. Premium Preference
            # -------------------------

            if "premium" in preferences:

                if budget:

                    if product["price"] >= budget * 0.75:

                        score += 10

                        reasons.append(
                            "premium option"
                        )

            # -------------------------
            # Final Score
            # -------------------------

            score = max(
                0,
                min(score, 100)
            )

            ranked.append({

                "product": product,

                "fit_score": round(
                    score,
                    1
                ),

                "reasons": reasons

            })

        # Highest fit first
        ranked.sort(
            key=lambda item: item["fit_score"],
            reverse=True
        )

        return ranked

