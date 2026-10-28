"""Boundaries for untrusted queries, tool parameters and output claims."""
import re
from pydantic import BaseModel, Field
class GuardrailError(ValueError):pass
class SafeInput(BaseModel):
    session_id:str=Field(min_length=1,max_length=128)
    message:str=Field(min_length=1,max_length=2000)
class Guardrails:
    PATTERNS=[r'ignore (all |previous |prior )?instructions',r'reveal (your |the )?(system|developer) prompt',r'override (the )?(system|safety|rules)',r'execute (this |the )?(command|code)',r'drop (table|database)']
    def validate_input(self,session_id,message):
        try: obj=SafeInput(session_id=session_id,message=message.strip())
        except Exception as e:raise GuardrailError('Invalid message or session ID') from e
        if any(re.search(p,obj.message,re.I) for p in self.PATTERNS):raise GuardrailError('Request contains disallowed instructions')
        return obj.message
    def validate_intent(self,intent):
        if not isinstance(intent,dict):raise GuardrailError('Invalid intent')
        budget=intent.get('budget')
        if budget is not None and (not isinstance(budget,(int,float)) or isinstance(budget,bool) or not 0<=budget<=1000000):raise GuardrailError('Invalid budget')
        if not isinstance(intent.get('preferences',[]),list):raise GuardrailError('Invalid preferences')
        return intent
    def validate_products(self,ranked,intent,tools):
        valid=[]
        for item in ranked:
            product=tools.product_details(item['product']['id'])
            if not product or not product.get('stock'):continue
            if intent.get('category') and product.get('category')!=intent['category']:continue
            if intent.get('budget') is not None and product['price']>intent['budget']:continue
            item['product']=product
            item['reasons']=[r for r in item.get('reasons',[]) if isinstance(r,str)]
            valid.append(item)
        return valid
