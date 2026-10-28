class SessionMemoryAgent:

    def __init__(self):
        self.sessions = {}

    def get(self, session_id):
        return self.sessions.get(
            session_id,
            {}
        )

    def update(self, session_id, intent):
        self.sessions[session_id] = intent
        return intent

    def merge(self, old_intent, new_intent):

        if not old_intent:
            return new_intent

        merged = old_intent.copy()

        # -------------------------
        # Preferences
        # -------------------------

        old_preferences = merged.get(
            "preferences",
            []
        ).copy()

        new_preferences = new_intent.get(
            "preferences",
            []
        )

        for preference in new_preferences:

            if preference not in old_preferences and preference not in ["cheaper", "premium"]:
                old_preferences.append(
                    preference
                )

        # An explicit change like "not waterproof" removes the old requirement.
        for preference in new_intent.get("remove_preferences", []):
            if preference in old_preferences: old_preferences.remove(preference)
        merged["preferences"] = old_preferences

        # -------------------------
        # Budget
        # -------------------------

        if new_intent.get("budget") is not None:

            merged["budget"] = (
                new_intent["budget"]
            )

        # -------------------------
        # Cheaper
        # -------------------------

        if "cheaper" in new_preferences:

            old_budget = old_intent.get(
                "budget"
            )

            if old_budget:

                merged["budget"] = round(
                    old_budget * 0.8,
                    2
                )

        # -------------------------
        # Premium
        # -------------------------

        if "premium" in new_preferences:

            old_budget = old_intent.get(
                "budget"
            )

            if old_budget:

                merged["budget"] = round(
                    old_budget * 1.2,
                    2
                )

        # -------------------------
        # Other Information
        # -------------------------

        for key, value in new_intent.items():

            if key in [
                "preferences",
                "confidence",
                "budget"
            ]:
                continue

            if value is not None:

                merged[key] = value

        # -------------------------
        # Confidence
        # -------------------------

        merged["confidence"] = max(
            old_intent.get(
                "confidence",
                0
            ),
            new_intent.get(
                "confidence",
                0
            )
        )

        return merged