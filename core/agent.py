"""
Agentic Layer - Makes higher-level decisions on tickets.

1. Escalation detection: Identifies low-confidence classifications that need human review.
2. Automation suggestion: Detects when a pattern of similar issues occurs frequently
   and suggests creating a runbook or automation.
"""
import os
import sys
from datetime import datetime, timedelta
from collections import Counter

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from core.embeddings import get_chroma_collection, get_embedding_model


class AgenticLayer:
    def __init__(self):
        self.collection = get_chroma_collection()
        self.model = get_embedding_model()
        
    def process(self, title: str, description: str, classification_result: dict) -> dict:
        """Process a ticket to determine if it needs escalation or automation."""
        ticket_text = f"{title} {description}"
        actions = []
        
        # --- 1. Confidence Escalation ---
        if classification_result.get('confidence', 1.0) < config.CONFIDENCE_THRESHOLD:
            actions.append({
                "type": "ESCALATE",
                "reason": f"Classification confidence ({classification_result['confidence']:.1%}) is below threshold ({config.CONFIDENCE_THRESHOLD:.1%}).",
                "action": f"Route to Human L2 Triage for review. Predicted: {classification_result.get('category')}."
            })
            
        # --- 2. Repeat Detection / Automation Suggestion ---
        repeat_info = self._detect_repeats(ticket_text)
        if repeat_info["is_repeated"]:
            actions.append({
                "type": "SUGGEST_AUTOMATION",
                "reason": f"Detected {repeat_info['count']} highly similar tickets (similarity >= {config.SIMILARITY_THRESHOLD}).",
                "action": "Generate automated runbook or proactive script for this issue.",
                "pattern_preview": repeat_info['pattern_preview']
            })
            
        return {
            "requires_human": any(a['type'] == 'ESCALATE' for a in actions),
            "suggests_automation": any(a['type'] == 'SUGGEST_AUTOMATION' for a in actions),
            "agent_actions": actions,
            "repeat_info": repeat_info
        }
        
    def _detect_repeats(self, ticket_text: str) -> dict:
        """Find how many highly similar tickets exist to detect patterns."""
        embedding = self.model.encode(ticket_text).tolist()
        
        # Querying vector store for up to 10 nearest neighbors
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=10,
            include=["documents", "metadatas", "distances"]
        )
        
        similar_count = 0
        pattern_preview = ""
        
        if results['ids'] and results['ids'][0]:
            for doc, dist in zip(results['documents'][0], results['distances'][0]):
                similarity = 1 - dist
                if similarity >= config.SIMILARITY_THRESHOLD:
                    similar_count += 1
                    if not pattern_preview:
                        pattern_preview = doc[:80] + "..."
                        
        return {
            "is_repeated": similar_count >= config.REPEAT_THRESHOLD,
            "count": similar_count,
            "pattern_preview": pattern_preview
        }

# --- CLI Test ---
if __name__ == "__main__":
    print("Initializing Agentic Layer...")
    agent = AgenticLayer()
    
    # Test 1: High confidence, NO repeats
    res_1 = agent.process(
        title="Printer on floor 3 is out of toner",
        description="We need cyan toner for the HP laserjet on floor 3 breakroom.",
        classification_result={"confidence": 0.88, "category": "Infrastructure"}
    )
    
    # Test 2: Low confidence
    res_2 = agent.process(
        title="I can't do my job",
        description="The thing is broken and I have a meeting in 5 minutes please fix.",
        classification_result={"confidence": 0.42, "category": "Application"}
    )
    
    # Test 3: High repeats (using an issue we know is in the DB)
    res_3 = agent.process(
        title="VPN connection fails for remote users",
        description="Users are unable to establish VPN connections, receiving error 619. This is affecting the remote sales team.",
        classification_result={"confidence": 0.95, "category": "Network"}
    )
    
    print("\n--- Test 1 (Standard Ticket) ---")
    print(res_1['agent_actions'] or "No agent intervention needed. Proceed normally.")
    
    print("\n--- Test 2 (Low Confidence Vague Ticket) ---")
    print(res_2['agent_actions'])
    
    print("\n--- Test 3 (Recurring Issue) ---")
    print(res_3['agent_actions'])
