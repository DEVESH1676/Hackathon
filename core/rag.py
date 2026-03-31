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
    
    def _generate_ollama(self, prompt: str) -> str:
        """Call Ollama via REST API directly to avoid LangChain timeouts/hanging."""
        print(f"  [LLM] Calling Ollama model: {config.OLLAMA_MODEL}...")
        url = f"{config.OLLAMA_BASE_URL}/api/chat"
        payload = {
            "model": config.OLLAMA_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"temperature": 0.2} # Low temp for factual IT resolutions
        }
        
        try:
            response = requests.post(url, json=payload, timeout=60)
            if response.status_code == 200:
                result = response.json()
                return result.get('message', {}).get('content', "Error: No content returned").strip()
            else:
                return f"Error: Ollama API returned HTTP {response.status_code}\n{response.text}"
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}"

    def suggest_resolution(self, title: str, description: str, k: int = 3) -> Dict[str, Any]:
        """
        Retrieve K similar tickets and formulate a resolution via AI.
        """
        ticket_text = f"{title} {description}"
        query_embedding = self.embedding_model.encode(ticket_text).tolist()
        
        # 1. Retrieve similar past tickets
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=["documents", "metadatas", "distances"]
        )
        
        past_resolutions = []
        similar_ticket_ids = []
        
        if results['ids'] and results['ids'][0]:
            for i, (doc, meta, dist) in enumerate(zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            )):
                similarity = 1 - dist
                similar_ticket_ids.append(results['ids'][0][i])
                past_resolutions.append(
                    f"--- PAST TICKET {i+1} (ID: {results['ids'][0][i]}, Similarity: {similarity:.2f}) ---\n"
                    f"Issue: {doc[:200]}...\n"
                    f"Past Resolution: {meta.get('resolution', 'N/A')}\n"
                )
        
        context = "\n".join(past_resolutions) if past_resolutions else "No similar past tickets found."
        
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
        resolution_text = self._generate_ollama(prompt)
        
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
