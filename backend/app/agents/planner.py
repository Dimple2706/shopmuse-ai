class Planner:

    def create_plan(self, intent):

        return [
            "intent_extraction",
            "catalog_mapping",
            "candidate_retrieval",
            "product_ranking",
            "explanation"
        ]