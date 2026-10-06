import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class ExplanationAgent:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.model = "openai/gpt-oss-120b"

    def run(self, ranked_products, intent):

        for item in ranked_products:

            product = item["product"]
            reasons = item["reasons"]

            prompt = f"""
You are ShopMuse, an intelligent shopping assistant.

Explain why this product is a good recommendation
for the user's request.

User intent:
{intent}

Product:
{product}

Matching reasons:
{reasons}

Write ONE short, natural explanation.
Mention the most important matching features.
Do not invent product features.
Do not mention AI, agents, scoring, or internal systems.
Keep it under 35 words.
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
                    temperature=0.3
                )

                explanation = (
                    response
                    .choices[0]
                    .message
                    .content
                    .strip()
                )

                item["explanation"] = explanation

            except Exception as error:

                print(
                    "Groq explanation failed:",
                    error
                )

                # Safe fallback
                item["explanation"] = (
                    f"{product['name']} matches "
                    + ", ".join(reasons)
                    + "."
                )

        return ranked_products