"""Run python -m app.scripts.seed_catalog from backend/ after setting MONGODB_URI."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(
    Path(__file__).resolve().parents[2] / ".env"
)
import json,os
from pathlib import Path
from pymongo import MongoClient,UpdateOne
from app.tools.semantic_tool import SemanticSearchTool

def main():
    products=json.loads((Path(__file__).resolve().parents[1]/'data/products.json').read_text())
    client=MongoClient(os.environ['MONGODB_URI'],serverSelectionTimeoutMS=5000)
    col=client[os.getenv('MONGODB_DB','shopmuse')]['products']
    col.create_index('id',unique=True)
    col.bulk_write([UpdateOne({'id':p['id']},{'$set':p},upsert=True) for p in products])
    count=SemanticSearchTool().index(products)
    print(f'Seeded {len(products)} MongoDB products and {count} ChromaDB vectors')
if __name__=='__main__':main()
