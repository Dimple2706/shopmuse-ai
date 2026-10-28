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
from app.security.guardrails import Guardrails
from app.governance.audit import audit


class Orchestrator:

    def __init__(self):

        self.guardrails = Guardrails()
        self.ingestion = QueryIngestionAgent()
        self.intent = IntentExtractionAgent()
        self.clarification = ClarificationAgent()
        self.mapping = CatalogMappingAgent()
        self.retrieval = CandidateRetrievalAgent()
        self.ranking = RankingAgent()
        self.explanation = ExplanationAgent()

        self.fallback = FallbackAgent(
            self.retrieval.tools
        )

        self.memory = SessionMemoryAgent()
        self.planner = Planner()
        self.reviewer = Reviewer()

    def run(self, session_id, query):

        # --------------------------------
        # 1. INGESTION
        # --------------------------------

        query = self.guardrails.validate_input(session_id, query)
        audit("request", session_id, status="received")
        normalized = self.ingestion.run(query)

        # --------------------------------
        # 2. INTENT EXTRACTION
        # --------------------------------

        new_intent = self.intent.run(
            normalized
        )

        # --------------------------------
        # 3. SESSION MEMORY
        # --------------------------------

        self.guardrails.validate_intent(new_intent)
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

        candidates = self.retrieval.run(attributes, normalized)

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

        ranked = self.guardrails.validate_products(ranked[:3], intent, self.retrieval.tools)

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

            replan_candidates = self.retrieval.run(replan_attributes, normalized)

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

        ranked = self.guardrails.validate_products(ranked, intent, self.retrieval.tools)
        ranked = self.explanation.run(ranked, intent, self.retrieval.last_context)
        audit("recommendation", session_id, count=len(ranked), mode=self.retrieval.last_mode)

        # --------------------------------
        # 11. FINAL RESPONSE
        # --------------------------------

        return {
            "type": "recommendation",
            "intent": intent,
            "plan": plan,
            "review": review,
            "products": ranked,
            "retrieval_mode": self.retrieval.last_mode
        }