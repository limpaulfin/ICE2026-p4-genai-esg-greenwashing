"""Evidence database and retrieval for real RAG experiment."""
import csv
import re

def tokenize(text):
    """Simple word tokenization."""
    return [w.lower() for w in re.findall(r'\b\w{3,}\b', text)]


def jaccard(set_a, set_b):
    """Jaccard similarity between two token sets."""
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


def load_evidence_db(src_path):
    """Load ALL GreenClaims records as evidence knowledge base."""
    with open(src_path) as f:
        rows = list(csv.DictReader(f))
    db = []
    for r in rows:
        company = (r.get("Company") or "").strip()
        claim = (r.get("Claim") or "").strip()
        accusation = (r.get("Accusation") or "").strip()
        gw_type = (r.get("Type") or "").strip()
        if company and claim:
            db.append({
                "company": company, "claim": claim,
                "accusation": accusation, "type": gw_type,
                "tokens": set(tokenize(claim + " " + accusation)),
            })
    return db


def retrieve_evidence(query_text, query_company, db, top_k=3):
    """Retrieve top-K similar cases (exclude self)."""
    q_tokens = set(tokenize(query_text))
    scored = []
    for doc in db:
        if doc["company"].lower() == query_company.lower() and \
           doc["claim"][:50].lower() in query_text[:100].lower():
            continue
        sim = jaccard(q_tokens, doc["tokens"])
        scored.append((sim, doc))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]


def load_corpus(src_path):
    """Load 35-report test corpus."""
    with open(src_path) as f:
        return list(csv.DictReader(f))
