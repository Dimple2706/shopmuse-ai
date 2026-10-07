class CatalogMappingAgent:

    def run(self, intent):

        mapped_preferences = []

        for preference in intent.get(
            "preferences",
            []
        ):

            if preference == "joint-friendly":

                mapped_preferences.extend([
                    "joint-friendly",
                    "low-impact",
                    "supportive"
                ])

            elif preference == "lightweight":

                mapped_preferences.append(
                    "lightweight"
                )

            elif preference == "waterproof":

                mapped_preferences.append(
                    "waterproof"
                )

            elif preference == "comfortable":

                mapped_preferences.append(
                    "comfortable"
                )

            else:

                mapped_preferences.append(
                    preference
                )

        return {

            # HARD CONSTRAINT
            "category": intent.get(
                "category"
            ),

            # SOFT PREFERENCES
            "preferences": mapped_preferences,

            # HARD CONSTRAINT
            "max_price": intent.get(
                "budget"
            )
        }