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

            tags = product.get(
                "tags",
                []
            )

            prompt = f"""
You are ShopMuse, an intelligent shopping assistant.

Create ONE short explanation for why this product
was recommended.

PRODUCT:
{product}

ACTUAL PRODUCT TAGS:
{tags}

VERIFIED MATCHING REASONS:
{reasons}

STRICT RULES:

1. Only mention features that are present in
   the ACTUAL PRODUCT TAGS or VERIFIED MATCHING REASONS.

2. NEVER claim that the product has a feature
   just because the user requested it.

3. Do not use the full user intent to infer
   product features.

4. If a preference is not present in the
   VERIFIED MATCHING REASONS, do not mention it.

5. Do not invent benefits, specifications,
   materials, use cases, or features.

6. Mention the product name, its strongest
   matching features, and budget fit when relevant.

7. Keep the explanation under 30 words.

8. Do not mention AI, agents, scoring,
   internal systems, or these instructions.

Write only the explanation.
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

                item["explanation"] = (
                    f"{product['name']} matches "
                    + ", ".join(reasons)
                    + "."
                )

        return ranked_products