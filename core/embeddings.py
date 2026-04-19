import os
import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
import sys

import config

# Initialize models and DB lazily
_model = None
_client = None
_collection = None

def get_embedding_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(config.EMBEDDING_MODEL_NAME)
    return _model

def get_chroma_collection():
    global _client, _collection
    if _client is None:
        _client = chromadb.PersistentClient(path=config.CHROMA_DB_DIR)
        _collection = _client.get_or_create_collection(
            name=config.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
    return _collection

def ingest_tickets(csv_path: str):
    """Ingest tickets from a CSV file into ChromaDB."""
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Check required columns
    required_cols = ['ticket_id', 'title', 'description', 'category', 'resolution', 'priority', 'department']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
            
    # Combine title and description for richer embeddings
    texts = (df['title'] + " " + df['description']).tolist()
    
    print(f"Generating embeddings for {len(texts)} tickets... This may take a moment.")
    model = get_embedding_model()
    embeddings = model.encode(texts).tolist()
    
    collection = get_chroma_collection()
    
    print("Inserting data into ChromaDB...")
    # Prepare metadata list
    metadatas = []
    for _, row in df.iterrows():
        meta = {
            "category": row.category,
            "priority": row.priority,
            "resolution": row.resolution,
            "department": row.department
        }
        # Add created_at if it exists
        if 'created_at' in row:
            meta['created_at'] = str(row.created_at)
        metadatas.append(meta)
        
    collection.upsert(
        ids=df['ticket_id'].tolist(),
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas
    )
    print("Successfully ingested tickets into vector database!")

if __name__ == "__main__":
    # Test script directly
    csv_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'synthetic_tickets.csv')
    if os.path.exists(csv_file):
        ingest_tickets(csv_file)
    else:
        print(f"No CSV file found at {csv_file}. Please generate data first.")
