
import os
from .llm import chat
from .search_client import retrieve

STRICT = os.getenv("RAG_STRICT_MODE","true").lower()=="true"

SYSTEM = """You are a company policy assistant. Always base your answer STRICTLY on the provided context.
- If the answer is not in the context, say you don't have that information.
- Output one concise answer with steps if relevant.
- Include a 'Sources:' line with the document IDs you used.
"""

def build_messages(user_q, passages):
    context = "\n\n".join([f"[{i+1}] (id={p['id']})\n{p['content']}" for i,p in enumerate(passages)])
    user_msg = f"User question:\n{user_q}\n\nContext:\n{context}\n\nInstructions: Provide one consistent, definitive answer grounded in the context. If ambiguous, state the policy precedence and ask for the exact case detail needed."
    return [{"role":"system","content":SYSTEM},{"role":"user","content":user_msg}]

def answer(user_q):
    passages = retrieve(user_q, top=5)
    msgs = build_messages(user_q, passages)
    out = chat(msgs)
    if STRICT and ("Sources:" not in out):
        srcs = ", ".join([p["id"] for p in passages[:3]])
        out = out + f"\n\nSources: {srcs}"
    return out
