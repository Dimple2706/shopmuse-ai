class ClarificationAgent:

    def run(self, intent):

        # -------------------------
        # Missing Category
        # -------------------------

        if not intent.get("category"):

            return {
                "needed": True,
                "question": (
                    "What kind of product are you looking for? "
                    "For example, hiking, fitness, yoga, or something else?"
                )
            }

        # -------------------------
        # Very Low Confidence
        # -------------------------

        if intent.get("confidence", 0) < 0.65:

            return {
                "needed": True,
                "question": (
                    "Could you tell me a little more about "
                    "what you're looking for so I can find a better match?"
                )
            }

        # -------------------------
        # Enough Information
        # -------------------------

        return {
            "needed": False,
            "question": None
        }