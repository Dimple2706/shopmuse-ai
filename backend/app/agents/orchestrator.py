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

        # Initialize all agents
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

        # -------------------------
        # 1. Clean user query
        # -------------------------

        normalized = self.ingestion.run(
            query
        )

        # -------------------------
        # 2. Extract new intent
        # -------------------------

        new_intent = self.intent.run(
            normalized
        )

        # -------------------------
        # 3. Retrieve previous memory
        # -------------------------

        previous_intent = self.memory.get(
            session_id
        )

        # -------------------------
        # 4. Merge conversation memory
        # -------------------------

        intent = self.memory.merge(
            previous_intent,
            new_intent
        )

        # Save the merged intent immediately.
        # This allows the assistant to remember
        # information even during clarification.
        self.memory.update(
            session_id,
            intent
        )

        # -------------------------
        # 5. Check for clarification
        # -------------------------

        clarification = self.clarification.run(
            intent
        )

        if clarification["needed"]:

            return {
                "type": "clarification",
                "question": clarification["question"],
                "intent": intent
            }

        # -------------------------
        # 6. Create execution plan
        # -------------------------

        plan = self.planner.create_plan(
            intent
        )

        # -------------------------
        # 7. Map intent to catalog
        # -------------------------

        attributes = self.mapping.run(
            intent
        )

        # -------------------------
        # 8. Retrieve candidates
        # -------------------------

        candidates = self.retrieval.run(
            attributes
        )

        # -------------------------
        # 9. Zero-result fallback
        # -------------------------

        if not candidates:

            fallback = self.fallback.run(
                intent
            )

            # Include intent and plan
            # for transparency/debugging.
            fallback["intent"] = intent
            fallback["plan"] = plan

            return fallback

        # -------------------------
        # 10. Rank candidates
        # -------------------------

        ranked = self.ranking.run(
            candidates,
            intent
        )

        # -------------------------
        # 11. Take top 3
        # -------------------------

        ranked = ranked[:3]

        # -------------------------
        # 12. Generate explanations
        # -------------------------

        ranked = self.explanation.run(
            ranked,
            intent
        )

        # -------------------------
        # 13. Review recommendations
        # -------------------------

        review = self.reviewer.review(
            ranked,
            intent
        )

        # -------------------------
        # 14. Return final response
        # -------------------------

        return {
            "type": "recommendation",
            "intent": intent,
            "plan": plan,
            "review": review,
            "products": ranked
        }

