import re, os
from pathlib import Path
import fitz
from django.conf import settings
from .models import Manual,Passage

def ingest_manual(manual):
    try:
        manual.status='processing'; manual.save(update_fields=['status'])
        manual.passages.all().delete()
        doc=fitz.open(manual.pdf.path); count=0
        for page_no,page in enumerate(doc,1):
            text=page.get_text('text').strip()
            words=re.findall(r'\S+',text)
            for start in range(0,len(words),120):
                chunk=' '.join(words[start:start+160]).strip()
                if chunk:
                    Passage.objects.create(manual=manual,page_number=page_no,text=chunk,chunk_index=count,embedding_text=chunk.lower()); count+=1
        manual.status='ready'; manual.error=''; manual.save(update_fields=['status','error']); return count
    except Exception as e:
        manual.status='failed'; manual.error=str(e); manual.save(update_fields=['status','error']); raise

def tokenize(s): return set(re.findall(r'[a-z0-9]+',s.lower()))
def retrieve(machine, query, limit=6):
    q=tokenize(query); scored=[]
    for p in Passage.objects.filter(manual__machine=machine,manual__status='ready').select_related('manual'):
        t=tokenize(p.text); score=len(q&t)/(len(q|t) or 1)
        if score>0: scored.append((score,p))
    scored.sort(key=lambda x:x[0],reverse=True)
    return scored[:limit]

def answer_from_evidence(query, hits):
    unsupported = ('price','cost','supplier','wiring diagram','tightening torque','remaining useful life','repair time','rewinding','circuit drawing')
    if any(term in query.lower() for term in unsupported) or not hits or hits[0][0] < 0.035:
        return 'INSUFFICIENT EVIDENCE: The uploaded manuals do not contain enough information to answer this question.', 'insufficient'
    # Safe extractive fallback: return the most relevant complete passages, without inventing values.
    selected=[]; seen=set()
    for score,p in hits:
        key=(p.manual_id,p.page_number)
        if key not in seen: selected.append(p.text); seen.add(key)
        if len(selected)>=3: break
    return 'Based on the selected machine manuals:\n\n'+'\n\n'.join(selected), 'answered'
