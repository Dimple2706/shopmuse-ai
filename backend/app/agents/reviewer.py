class Reviewer:

    def review(self, products, intent):

        if not products:
            return {
                "approved": False,
                "reason": "No products found"
            }

        for item in products:

            product = item["product"]

            if intent["budget"]:

                if product["price"] > intent["budget"]:
                    return {
                        "approved": False,
                        "reason": "Product exceeds budget"
                    }

        return {
            "approved": True,
            "reason": (
                "Recommendations satisfy "
                "the available constraints"
            )
        }