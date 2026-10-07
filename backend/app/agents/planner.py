class Planner:

    def create_plan(self, intent):

        plan = [
            "intent_extraction",
            "catalog_mapping",
            "candidate_retrieval",
            "product_ranking"
        ]

        preferences = intent.get(
            "preferences",
            []
        )

        if preferences:

            plan.append(
                "preference_validation"
            )

        plan.extend([
            "reviewer",
            "explanation"
        ])

        return plan

    def create_replan(
        self,
        intent,
        review
    ):

        current_preferences = (
            intent.get(
                "preferences",
                []
            ).copy()
        )

        missing_preferences = review.get(
            "missing_preferences",
            []
        )

        # First remove a preference that
        # has zero representation.
        for preference in missing_preferences:

            if preference in current_preferences:

                current_preferences.remove(
                    preference
                )

                return {
                    "strategy":
                        "relax_unavailable_preference",

                    "removed_preference":
                        preference,

                    "preferences":
                        current_preferences
                }

        # Fallback if the reviewer did not
        # identify a specific missing preference.
        removable = [
            preference
            for preference in current_preferences
            if preference not in [
                "cheaper",
                "premium"
            ]
        ]

        if removable:

            removed = removable[-1]

            current_preferences.remove(
                removed
            )

            return {
                "strategy":
                    "relax_preference",

                "removed_preference":
                    removed,

                "preferences":
                    current_preferences
            }

        return {
            "strategy":
                "broaden_search",

            "preferences":
                current_preferences
        }