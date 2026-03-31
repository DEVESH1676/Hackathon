"""
Ticket Classifier - Classifies incoming IT tickets using embedding similarity.

Uses ChromaDB vector store + category centroids for fast, accurate classification.
Falls back to direct similarity search when centroid confidence is low.
"""
import os
import sys
import numpy as np
from collections import defaultdict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from core.embeddings import get_embedding_model, get_chroma_collection


class TicketClassifier:
    """Classifies tickets by computing similarity to category centroids."""
    
    def __init__(self):
        self.model = get_embedding_model()
        self.collection = get_chroma_collection()
        self.centroids = {}
        self._build_centroids()
    
    def _build_centroids(self):
        """Compute average embedding per category from stored tickets."""
        all_data = self.collection.get(include=["embeddings", "metadatas"])
        
        if not all_data["ids"]:
            print("⚠ No tickets in vector store. Run embeddings.py first.")
            return
        
        # Group embeddings by category
        category_embeddings = defaultdict(list)
        for emb, meta in zip(all_data["embeddings"], all_data["metadatas"]):
            cat = meta.get("category", "Unknown")
            category_embeddings[cat].append(emb)
        
        # Compute centroid (mean embedding) per category
        for cat, embs in category_embeddings.items():
            self.centroids[cat] = np.mean(embs, axis=0)
            
        print(f"✓ Built centroids for {len(self.centroids)} categories: {list(self.centroids.keys())}")
    
    def _cosine_similarity(self, a, b):
        """Compute cosine similarity between two vectors."""
        a, b = np.array(a), np.array(b)
        dot = np.dot(a, b)
        norm = np.linalg.norm(a) * np.linalg.norm(b)
        return dot / norm if norm > 0 else 0.0
    
    def classify(self, title: str, description: str) -> dict:
        """
        Classify a ticket and return category, department, confidence, and similar tickets.
        
        Returns:
            dict with keys: category, department, confidence, priority_suggestion,
                           similar_tickets, method
        """
        text = f"{title} {description}"
        embedding = self.model.encode(text).tolist()
        
        # --- Method 1: Centroid similarity ---
        scores = {}
        for cat, centroid in self.centroids.items():
            scores[cat] = self._cosine_similarity(embedding, centroid)
        
        best_category = max(scores, key=scores.get)
        best_score = scores[best_category]
        
        # --- Method 2: Direct similarity search for validation + similar tickets ---
        search_results = self.collection.query(
            query_embeddings=[embedding],
            n_results=5,
            include=["documents", "metadatas", "distances"]
        )
        
        similar_tickets = []
        top_categories_from_search = []
        
        if search_results["ids"][0]:
            for i, (doc, meta, dist) in enumerate(zip(
                search_results["documents"][0],
                search_results["metadatas"][0],
                search_results["distances"][0]
            )):
                # ChromaDB cosine distance = 1 - similarity
                similarity = 1 - dist
                similar_tickets.append({
                    "document": doc[:150],
                    "category": meta.get("category", "Unknown"),
                    "priority": meta.get("priority", "Unknown"),
                    "resolution": meta.get("resolution", "")[:200],
                    "department": meta.get("department", "Unknown"),
                    "similarity": round(similarity, 4)
                })
                top_categories_from_search.append(meta.get("category", "Unknown"))
        
        # --- Confidence adjustment ---
        # If top search results disagree with centroid, reduce confidence
        if top_categories_from_search:
            search_agreement = sum(1 for c in top_categories_from_search[:3] if c == best_category) / min(3, len(top_categories_from_search))
            adjusted_confidence = (best_score * 0.6) + (search_agreement * 0.4)
        else:
            adjusted_confidence = best_score
        
        # --- Priority suggestion based on similar tickets ---
        priority_counts = defaultdict(int)
        for t in similar_tickets[:3]:
            priority_counts[t["priority"]] += 1
        suggested_priority = max(priority_counts, key=priority_counts.get) if priority_counts else "P3 Medium"
        
        # --- Department routing ---
        department = config.ROUTING.get(best_category, config.ROUTING["Unknown"])
        
        # --- Determine classification method ---
        method = "centroid"
        if adjusted_confidence < config.CONFIDENCE_THRESHOLD and similar_tickets:
            # Fall back to search-based classification
            best_category = top_categories_from_search[0]
            department = config.ROUTING.get(best_category, config.ROUTING["Unknown"])
            method = "similarity_search"
        
        return {
            "category": best_category,
            "department": department,
            "confidence": round(adjusted_confidence, 4),
            "priority_suggestion": suggested_priority,
            "similar_tickets": similar_tickets,
            "all_scores": {k: round(v, 4) for k, v in sorted(scores.items(), key=lambda x: -x[1])},
            "method": method
        }
    
    def find_repeats(self, title: str, description: str) -> list:
        """Find potentially recurring/duplicate tickets."""
        text = f"{title} {description}"
        embedding = self.model.encode(text).tolist()
        
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=10,
            include=["documents", "metadatas", "distances"]
        )
        
        repeats = []
        if results["ids"][0]:
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0]
            ):
                similarity = 1 - dist
                if similarity >= config.SIMILARITY_THRESHOLD:
                    repeats.append({
                        "document": doc[:150],
                        "category": meta.get("category"),
                        "resolution": meta.get("resolution", "")[:300],
                        "similarity": round(similarity, 4)
                    })
        
        return repeats


# --- CLI Test ---
if __name__ == "__main__":
    print("Initializing classifier...")
    clf = TicketClassifier()
    
    test_cases = [
        ("VPN not working", "Multiple users cannot connect to VPN. Getting error 619. Remote team is affected."),
        ("Cannot access SharePoint", "Getting access denied when trying to open the project site in SharePoint."),
        ("Database slow", "PROD-DB-02 queries are taking 30+ seconds. Application is timing out."),
        ("Suspicious email received", "Got a phishing email pretending to be from HR. Contains a suspicious link."),
        ("Kubernetes pods crashing", "Payment service pods keep getting OOMKilled in the production cluster."),
        ("Need new service account", "DevOps needs a service account with S3 access for the backup automation."),
    ]
    
    print(f"\n{'='*70}")
    print(f"  Testing classifier on {len(test_cases)} tickets")
    print(f"{'='*70}")
    
    for title, desc in test_cases:
        result = clf.classify(title, desc)
        print(f"\n  📝 \"{title}\"")
        print(f"     Category:   {result['category']} (via {result['method']})")
        print(f"     Department: {result['department']}")
        print(f"     Confidence: {result['confidence']:.1%}")
        print(f"     Priority:   {result['priority_suggestion']}")
        print(f"     Top scores: {result['all_scores']}")
