"""Grounded explanation: generated from validated catalog facts and retrieval context."""
class ExplanationAgent:
    def run(self,ranked_products,intent,contexts=None):
        contexts=contexts or {}
        for item in ranked_products:
            p=item['product']; tags=set(p.get('tags',[])); prefs=[x for x in intent.get('preferences',[]) if x in tags]
            # RAG context is passed in, but claims are grounded exclusively in current catalog facts.
            item['retrieved_context']=contexts.get(str(p['id']), '')[:500]
            parts=[f"{p['name']} is a {p['category']} option"]
            if prefs:parts.append('matching your '+', '.join(prefs[:3])+' preference'+('s' if len(prefs)>1 else ''))
            parts.append(f"priced at ${p['price']}")
            item['explanation']='; '.join(parts)+'.'
        return ranked_products
