from app.agents.ingestion_agent import QueryIngestionAgent
from app.agents.intent_agent import IntentExtractionAgent
from app.agents.clarification_agent import ClarificationAgent
from app.agents.mapping_agent import CatalogMappingAgent
from app.agents.retrieval_agent import CandidateRetrievalAgent
from app.agents.ranking_agent import RankingAgent
from app.agents.explanation_agent import ExplanationAgent
from app.agents.fallback_agent import FallbackAgent
from app.agents.memory_agent import SessionMemoryAgent
from app.agents.planner import Planner
from app.agents.reviewer import Reviewer


class Orchestrator:

    def __init__(self):

        self.ingestion = QueryIngestionAgent()
        self.intent = IntentExtractionAgent()
        self.clarification = ClarificationAgent()
        self.mapping = CatalogMappingAgent()
        self.retrieval = CandidateRetrievalAgent()
        self.ranking = RankingAgent()
        self.explanation = ExplanationAgent()

        self.fallback = FallbackAgent(
            self.retrieval.catalog
        )

        self.memory = SessionMemoryAgent()
        self.planner = Planner()
        self.reviewer = Reviewer()

    def run(self, session_id, query):

        # --------------------------------
        # 1. INGESTION
        # --------------------------------

        normalized = self.ingestion.run(
            query
        )

        # --------------------------------
        # 2. INTENT EXTRACTION
        # --------------------------------

        new_intent = self.intent.run(
            normalized
        )

        # --------------------------------
        # 3. SESSION MEMORY
        # --------------------------------

        previous_intent = self.memory.get(
            session_id
        )

        intent = self.memory.merge(
            previous_intent,
            new_intent
        )

        self.memory.update(
            session_id,
            intent
        )

        # --------------------------------
        # 4. CLARIFICATION
        # --------------------------------

        clarification = self.clarification.run(
            intent
        )

        if clarification["needed"]:

            return {
                "type": "clarification",
                "question": clarification["question"],
                "intent": intent
            }

        # --------------------------------
        # 5. INITIAL PLAN
        # --------------------------------

        plan = self.planner.create_plan(
            intent
        )

        # --------------------------------
        # 6. FIRST RETRIEVAL + RANKING
        # --------------------------------

        attributes = self.mapping.run(
            intent
        )

        candidates = self.retrieval.run(
            attributes
        )

        # --------------------------------
        # 7. ZERO RESULT
        # --------------------------------

        if not candidates:

            fallback = self.fallback.run(
                intent
            )

            fallback["intent"] = intent
            fallback["plan"] = plan

            return fallback

        ranked = self.ranking.run(
            candidates,
            intent
        )

        ranked = ranked[:3]

        # --------------------------------
        # 8. REVIEW
        # --------------------------------

        review = self.reviewer.review(
            ranked,
            intent
        )

        # --------------------------------
        # 9. RE-PLAN IF NEEDED
        # --------------------------------

        if review.get("needs_replan"):

            replan = self.planner.create_replan(
                intent,
                review
            )

            # Create a modified intent
            replanned_intent = intent.copy()

            replanned_intent["preferences"] = (
                replan["preferences"]
            )

            # Run retrieval again
            replan_attributes = (
                self.mapping.run(
                    replanned_intent
                )
            )

            replan_candidates = (
                self.retrieval.run(
                    replan_attributes
                )
            )

            if replan_candidates:

                replan_ranked = (
                    self.ranking.run(
                        replan_candidates,
                        replanned_intent
                    )
                )

                replan_ranked = (
                    replan_ranked[:3]
                )

                replan_review = (
                    self.reviewer.review(
                        replan_ranked,
                        replanned_intent
                    )
                )

                # Use the replanned results
                # if they are approved.
                if replan_review.get(
                    "approved"
                ):

                    intent = replanned_intent

                    ranked = replan_ranked

                    review = replan_review

                    plan.append(
                        "replanning"
                    )

        # --------------------------------
        # 10. EXPLANATION
        # --------------------------------

        ranked = self.explanation.run(
            ranked,
            intent
        )

        # --------------------------------
        # 11. FINAL RESPONSE
        # --------------------------------

        return {
            "type": "recommendation",
            "intent": intent,
            "plan": plan,
            "review": review,
            "products": ranked
        }