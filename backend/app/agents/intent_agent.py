import json
import re
import os

from groq import Groq
from dotenv import load_dotenv


load_dotenv()


class IntentExtractionAgent:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.model = "openai/gpt-oss-120b"

    def run(self, query):

        prompt = f"""
You are the intent extraction agent for ShopMuse,
an AI-powered conversational shopping assistant.

Analyze the user's shopping request and return ONLY valid JSON.

Extract:

- purchase_type
- recipient
- occasion
- category
- budget
- preferences
- confidence

Rules:

1. category should be one of:
   hiking, fitness, yoga, footwear, beauty, electronics, bags, gifts, or null

2. budget should be a number if the user gives a budget.
   Otherwise use null.

3. preferences should contain concise shopping requirements
   such as:
   joint-friendly
   lightweight
   waterproof
   comfortable
   cheaper
   premium

4. Understand natural language.
   For example:
   "something easy on his knees"
   should become:
   "joint-friendly"

5. If the user is refining a previous request,
   extract only the new information.

6. confidence must be between 0 and 1.

Return exactly this structure:

{{
    "purchase_type": null,
    "recipient": null,
    "occasion": null,
    "category": null,
    "budget": null,
    "preferences": [],
    "confidence": 0.0
}}

User request:

{query}
"""

        try:

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0
            )

            content = response.choices[0].message.content

            # Remove accidental markdown fences
            content = re.sub(
                r"```json|```",
                "",
                content
            ).strip()

            intent = json.loads(content)

            # Safety defaults
            intent.setdefault(
                "purchase_type",
                None
            )

            intent.setdefault(
                "recipient",
                None
            )

            intent.setdefault(
                "occasion",
                None
            )

            intent.setdefault(
                "category",
                None
            )

            intent.setdefault(
                "budget",
                None
            )

            intent.setdefault(
                "preferences",
                []
            )

            intent.setdefault(
                "confidence",
                0.5
            )

            return intent

        except Exception as error:

            print(
                "Groq intent extraction failed:",
                error
            )

            # Safe fallback
            return {
                "purchase_type": None,
                "recipient": None,
                "occasion": None,
                "category": None,
                "budget": None,
                "preferences": [],
                "confidence": 0.0
            }