"""
Resolution Engine (RAG) - Retrieves similar past tickets and uses LLM to generate resolutions.
Uses direct REST calls to Ollama to avoid Langchain hanging issues.
"""
import os
import sys
import json
import requests
from typing import Dict, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from core.embeddings import get_chroma_collection, get_embedding_model


class ResolutionEngine:
    """Retrieves similar tickets and generates an AI resolution."""
    
    def __init__(self):
        self.collection = get_chroma_collection()
        self.embedding_model = get_embedding_model()
    
    def _call_llm(self, prompt: str) -> str:
        """Call Groq or Ollama via REST API directly to avoid LangChain timeouts/hanging."""
        try:
            if config.USE_GROQ and config.GROQ_API_KEY:
                print(f"  [LLM] Calling Groq model: {config.GROQ_MODEL}...")
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {config.GROQ_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": config.GROQ_MODEL,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.2,
                        "max_tokens": 1000,
                    },
                    timeout=15,
                )
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"].strip()
            else:
                print(f"  [LLM] Calling Ollama model: {config.OLLAMA_MODEL}...")
                url = f"{config.OLLAMA_BASE_URL}/api/chat"
                payload = {
                    "model": config.OLLAMA_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                    "options": {"temperature": 0.2} # Low temp for factual IT resolutions
                }
                response = requests.post(url, json=payload, timeout=60)
                if response.status_code == 200:
                    result = response.json()
                    return result.get('message', {}).get('content', "Error: No content returned").strip()
                else:
                    return f"Error: Ollama API returned HTTP {response.status_code}\n{response.text}"
        except Exception as e:
            return f"Error connecting to LLM: {str(e)}"

    def _rank_retrieved_chunks(self, results) -> list:
        """Rank chunks based on semantic (60%), recency (20%), and outcome (20%)."""
        from datetime import datetime
        chunks = []
        if not results['ids'] or not results['ids'][0]:
            return chunks

        for i, (doc, meta, dist) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )):
            # 1. Semantic Score (60%)
            semantic_score = 1.0 - dist
            
            # 2. Recency Score (20%)
            recency_score = 0.5
            if 'created_at' in meta:
                try:
                    ticket_date = datetime.strptime(meta['created_at'].split()[0], "%Y-%m-%d")
                    current_date = datetime(2026, 4, 8)
                    days_old = (current_date - ticket_date).days
                    recency_score = max(0.0, 1.0 - (days_old / 730.0)) # Normalize over 2 years
                except:
                    pass
            
            # 3. Outcome Score (20%)
            outcome_score = 0.5
            res_text = meta.get('resolution', '').lower()
            positive_words = ['success', 'resolved', 'fixed', 'restored', 'completed', 'corrected']
            if any(w in res_text for w in positive_words):
                outcome_score = 1.0
            elif len(res_text) > 10:
                outcome_score = 0.8
                
            final_score = (semantic_score * 0.6) + (recency_score * 0.2) + (outcome_score * 0.2)
            
            chunks.append({
                "id": results['ids'][0][i],
                "document": doc,
                "metadata": meta,
                "semantic": semantic_score,
                "recency": recency_score,
                "outcome": outcome_score,
                "final_score": final_score
            })
            
        # Sort descending by final combined score
        return sorted(chunks, key=lambda x: x['final_score'], reverse=True)

    def suggest_resolution(self, title: str, description: str, k: int = 3) -> Dict[str, Any]:
        """
        Retrieve K similar tickets, rank them, fetch category KB (multi-hop), and formulate prediction.
        """
        ticket_text = f"{title} {description}"
        query_embedding = self.embedding_model.encode(ticket_text).tolist()
        
        # --- HOP 1: Primary Retrieval ---
        # Fetch a larger pool to allow ranking to surface the best
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k * 2,
            include=["documents", "metadatas", "distances"]
        )
        
        ranked_chunks = self._rank_retrieved_chunks(results)[:k]
        
        past_resolutions = []
        similar_ticket_ids = []
        top_category = "Unknown"
        
        if ranked_chunks:
            # Determine top category for second hop
            top_category = ranked_chunks[0]['metadata'].get('category', 'Unknown')
            
            for i, chunk in enumerate(ranked_chunks):
                similar_ticket_ids.append(chunk['id'])
                past_resolutions.append(
                    f"--- PAST TICKET {i+1} (ID: {chunk['id']}, Final Score: {chunk['final_score']:.2f}) ---\n"
                    f"[Scores: Semantic={chunk['semantic']:.2f}, Recency={chunk['recency']:.2f}, Outcome={chunk['outcome']:.2f}]\n"
                    f"Issue: {chunk['document'][:200]}...\n"
                    f"Past Resolution: {chunk['metadata'].get('resolution', 'N/A')}\n"
                )
                
        # --- HOP 2: Category KB Context ---
        kb_context = []
        if top_category != "Unknown":
            kb_results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=2,
                where={"category": top_category},
                include=["documents", "metadatas", "distances"]
            )
            if kb_results['ids'] and kb_results['ids'][0]:
                for doc, meta, t_id in zip(kb_results['documents'][0], kb_results['metadatas'][0], kb_results['ids'][0]):
                    if t_id not in similar_ticket_ids:
                        kb_context.append(f"- [KB Category '{top_category}'] (ID: {t_id}): {meta.get('resolution', doc[:150])}")
        
        hop1_text = "\n".join(past_resolutions) if past_resolutions else "No similar past tickets found."
        hop2_text = "\n".join(kb_context) if kb_context else "No additional category KB linked."
        
        context = f"## Primary Ranked Tickets (Hop 1):\n{hop1_text}\n\n## Linked Category DB Insight (Hop 2):\n{hop2_text}"
        
        # 2. Build the LLM Prompt
        prompt = f"""You are an Expert L3 IT Support Engineer AI. 
Based on these similar past tickets and their successful resolutions, suggest a detailed, step-by-step resolution for the new ticket.

## Past Similar Tickets (Context):
{context}

## New Ticket to Resolve:
Title: {title}
Description: {description}

## Instructions:
1. Synthesize the most relevant solution steps from the past tickets.
2. Adapt them to the specific details of the New Ticket (use the specific server names, users, or errors mentioned).
3. Be highly technical, concise, and provide actionable resolution steps (commands, tools to check, etc.).
4. Do NOT just copy-paste the past resolution; formulate a specific response for the new ticket.
5. Provide ONLY the suggested resolution text, formatted nicely.
"""

        # 3. Request generation
        resolution_text = self._call_llm(prompt)
        
        return {
            "suggested_resolution": resolution_text,
            "similar_ticket_ids": similar_ticket_ids,
            "context_used": context
        }


# --- CLI Test ---
if __name__ == "__main__":
    print("Initializing RAG Engine...")
    rag = ResolutionEngine()
    
    test_title = "VPN connection drops after 5 minutes"
    test_desc = "User jdoe is complaining that their VPN connects but drops exactly 5 minutes later with error 619. Checked Splunk, logs show active session timeout."
    
    print(f"\n=============================================")
    print(f"Testing RAG Engine for Ticket:")
    print(f"Title: {test_title}")
    print(f"Description: {test_desc}")
    print(f"=============================================\n")
    
    result = rag.suggest_resolution(test_title, test_desc)
    
    print("✓ Retrieved Context from Vector DB:")
    print(result['context_used'])
    
    print("\n✓ AI Suggested Resolution:")
    print("-" * 50)
    print(result['suggested_resolution'])
    print("-" * 50)
