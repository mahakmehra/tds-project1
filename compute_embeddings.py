import json
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path
from app.config import settings

def compute_embeddings():
    # Load model
    model = SentenceTransformer(settings.EMBEDDING_MODEL)
    
    # Load and validate data
    data_path = Path("data/processed/combined.json")
    if not data_path.exists():
        raise FileNotFoundError(f"Processed data not found at {data_path}")
    
    with open(data_path) as f:
        data = json.load(f)
    
    # Process texts and collect metadata
    texts = []
    metadata_records = []
    
    for item in data:
        if not isinstance(item, dict):
            print(f"Warning: Skipping invalid item (not a dict): {item}")
            continue
        
        text = item.get("text", "").strip()
        if not text:
            print(f"Warning: Empty text in item: {item.get('title', 'Untitled')}")
            continue
            
        texts.append(text)
        metadata_records.append({
            "title": item.get("title", "Untitled"),
            "url": item.get("url", "#"),
            "source": item.get("source", "unknown"),
            **item.get("metadata", {})
        })
    
    if not texts:
        raise ValueError("No valid text content found to embed")
    
    # Compute embeddings
    print(f"Computing embeddings for {len(texts)} items...")
    embeddings = model.encode(texts, show_progress_bar=True)
    
    # Prepare output structure
    output = {
        "embeddings": embeddings.tolist(),
        "metadata": metadata_records,
        "version": "1.0",
        "embedding_model": settings.EMBEDDING_MODEL
    }
    
    # Save results
    output_path = Path("data/embeddings.json")
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"Successfully saved embeddings to {output_path}")

if __name__ == "__main__":
    compute_embeddings()