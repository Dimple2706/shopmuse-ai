"""Minimal privacy-preserving audit trail. No raw queries or customer IDs."""
import logging,hashlib,os
logger=logging.getLogger('shopmuse.audit')
def audit(event,session_id,**details):
    digest=hashlib.sha256((os.getenv('AUDIT_SALT','local-dev')+session_id).encode()).hexdigest()[:12]
    logger.info('event=%s session=%s details=%s',event,digest,{k:v for k,v in details.items() if k in ('mode','count','status')})
