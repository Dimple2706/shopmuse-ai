"""Structured catalog API. MongoDB is authoritative; local JSON is opt-in demo mode."""
import json, os
from pathlib import Path
from functools import lru_cache
from pymongo import MongoClient

class CatalogTool:
    def __init__(self):
        self.demo = os.getenv('CATALOG_BACKEND', 'mongodb').lower() == 'json'
        if self.demo:
            self.products = json.loads((Path(__file__).resolve().parents[1] / 'data/products.json').read_text())
        else:
            uri = os.getenv('MONGODB_URI')
            if not uri: raise RuntimeError('Set MONGODB_URI or CATALOG_BACKEND=json for demo mode')
            self.client = MongoClient(uri, serverSelectionTimeoutMS=4000)
            self.collection = self.client[os.getenv('MONGODB_DB','shopmuse')]['products']
            self.client.admin.command('ping')
    def _clean(self, doc):
        if not doc: return None
        return {k:v for k,v in doc.items() if k != '_id'}
    def all_products(self, limit=500):
        if self.demo: return self.products[:limit]
        return [self._clean(p) for p in self.collection.find({}, {'_id':0}).limit(limit)]
    def get_product(self, product_id):
        if self.demo: return next((p for p in self.products if str(p['id'])==str(product_id)),None)
        return self._clean(self.collection.find_one({'id':str(product_id)}, {'_id':0}))
    def search(self,category=None,tags=None,max_price=None,include_out_of_stock=False,limit=100):
        if self.demo:
            products=self.products
        else:
            query={}
            if category: query['category']=category
            if max_price is not None: query['price']={'$lte':float(max_price)}
            if not include_out_of_stock: query['stock']=True
            if tags: query['tags']={'$in':tags}
            return [self._clean(p) for p in self.collection.find(query,{'_id':0}).limit(limit)]
        return [p for p in products if (not category or p['category']==category) and (max_price is None or p['price']<=max_price) and (include_out_of_stock or p['stock']) and (not tags or any(t in p['tags'] for t in tags))][:limit]
    def availability_price(self,product_id):
        p=self.get_product(product_id)
        return {'id':product_id,'available':bool(p and p.get('stock')),'price':p.get('price') if p else None}
