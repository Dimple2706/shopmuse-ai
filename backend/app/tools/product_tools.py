"""Approved tool gateway: no agent needs DB internals."""
import logging
from app.tools.catalog_tool import CatalogTool
from app.tools.semantic_tool import SemanticSearchTool
log=logging.getLogger('shopmuse.tools')
class ProductTools:
    def __init__(self):
        self.catalog=CatalogTool()
        try: self.semantic=SemanticSearchTool()
        except Exception as e:
            log.warning('Semantic search unavailable: %s',type(e).__name__)
            self.semantic=None
    def catalog_access(self,limit=500):return self.catalog.all_products(min(max(int(limit),1),500))
    def product_search(self,category=None,tags=None,max_price=None,limit=100,include_out_of_stock=False):
        return self.catalog.search(category,tags,max_price,include_out_of_stock,min(max(int(limit),1),100))
    def product_details(self,product_id):return self.catalog.get_product(product_id)
    def availability_price(self,product_id):return self.catalog.availability_price(product_id)
    def semantic_search(self,query,category=None,limit=30):
        if not self.semantic:return []
        return self.semantic.search(query,category,min(max(int(limit),1),30))
    def hybrid_search(self,query,category=None,max_price=None,limit=60):
        # MongoDB hard constraints ALWAYS win. Semantic results only reorder eligible products.
        eligible=self.product_search(category=category,max_price=max_price,limit=100)
        by_id={str(p['id']):p for p in eligible}
        semantic=self.semantic_search(query,category)
        ordered=[]; seen=set(); contexts={}
        for hit in semantic:
            id=hit['id']
            if id in by_id and id not in seen:
                ordered.append(by_id[id]);seen.add(id);contexts[id]=hit['context']
        ordered.extend(p for p in eligible if str(p['id']) not in seen)
        return {'products':ordered[:limit], 'contexts':contexts, 'retrieval_mode':'hybrid' if semantic else 'structured_fallback'}
