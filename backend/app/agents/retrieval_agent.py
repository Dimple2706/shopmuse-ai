from app.tools.product_tools import ProductTools
class CandidateRetrievalAgent:
    def __init__(self,tools=None):
        self.tools=tools or ProductTools()
        self.catalog=self.tools.catalog # backward-compatible reference; use tools in new code
        self.last_context={}
        self.last_mode='structured_fallback'
    def run(self,attributes,query=''):
        result=self.tools.hybrid_search(query,category=attributes.get('category'),max_price=attributes.get('max_price'))
        self.last_context=result['contexts']
        self.last_mode=result['retrieval_mode']
        return result['products']
