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

        # These are preferences, not hard requirements.
        soft_preferences = [
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

            # --------------------------------
            # 1. CATEGORY MATCH - 25 POINTS
            # --------------------------------

            if category == product["category"]:

                score += 25

                reasons.append(
                    "matches your activity"
                )

            # --------------------------------
            # 2. PREFERENCE MATCH - 40 POINTS
            # --------------------------------

            if soft_preferences:

                matched_preferences = []

                for preference in soft_preferences:

                    if preference in product["tags"]:

                        matched_preferences.append(
                            preference
                        )

                preference_ratio = (
                    len(matched_preferences)
                    / len(soft_preferences)
                )

                score += preference_ratio * 40

                for preference in matched_preferences:

                    reasons.append(
                        f"matches your "
                        f"{preference} preference"
                    )

            # --------------------------------
            # 3. BUDGET FIT - 20 POINTS
            # --------------------------------

            if budget:

                if product["price"] <= budget:

                    # Products comfortably below budget
                    # receive a slightly better score.
                    budget_ratio = (
                        product["price"] / budget
                    )

                    budget_score = (
                        20 * (1 - budget_ratio * 0.5)
                    )

                    score += budget_score

                    reasons.append(
                        "within your budget"
                    )

                else:

                    # Being over budget is a penalty,
                    # but not an automatic rejection.
                    score -= 15

                    reasons.append(
                        "slightly above your budget"
                    )

            # --------------------------------
            # 4. PRODUCT QUALITY - 10 POINTS
            # --------------------------------

            rating_score = (
                product["rating"] / 5
            ) * 10

            score += rating_score

            # --------------------------------
            # 5. CHEAPER PREFERENCE
            # --------------------------------

            if "cheaper" in preferences:

                if budget:

                    if product["price"] <= budget * 0.75:

                        score += 8

                        reasons.append(
                            "especially affordable"
                        )

            # --------------------------------
            # 6. PREMIUM PREFERENCE
            # --------------------------------

            if "premium" in preferences:

                if product["rating"] >= 4.7:

                    score += 8

                    reasons.append(
                        "highly rated premium option"
                    )

            # --------------------------------
            # 7. FINAL SCORE
            # --------------------------------

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
            key=lambda item:
            item["fit_score"],
            reverse=True
        )

        return ranked