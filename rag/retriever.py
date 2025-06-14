# rag/retriever.py

import os

# ✅ Set Hugging Face cache directories to avoid /.cache permission errors
os.environ["TRANSFORMERS_CACHE"] = "/tmp/hf_cache"
os.environ["HF_HOME"] = "/tmp/hf_home"

import json
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict
from rag.config import settings

class Retriever:
    def __init__(self, embeddings_path: str = "embeddings.json"):
        self.embedder = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.embeddings, self.metadata = self._load_embeddings(embeddings_path)
        self.content_lookup = self._build_content_lookup()

    def _load_embeddings(self, path: str) -> tuple[np.ndarray, List[Dict]]:
        """Load embeddings and metadata from file"""
        try:
            with open(path) as f:
                data = json.load(f)
            
            embeddings = np.array(data["embeddings"])
            metadata = data["metadata"]
            
            if len(embeddings) != len(metadata):
                raise ValueError("Mismatch between embeddings and metadata counts")
                
            return embeddings, metadata
            
        except Exception as e:
            raise RuntimeError(f"Failed to load embeddings: {str(e)}")

    def _build_content_lookup(self) -> Dict[str, str]:
        """Build a mapping from URLs to full content (lazy-loaded)"""
        try:
            with open("processed/combined.json") as f:
                combined_data = json.load(f)
            return {item["url"]: item["text"] for item in combined_data}
        except Exception as e:
            raise RuntimeError(f"Failed to build content lookup: {str(e)}")

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """Retrieve most relevant documents for a query"""
        query_embedding = self.embedder.encode([query])
        
        scores = np.dot(self.embeddings, query_embedding.T).flatten()
        top_indices = np.argsort(scores)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            item_meta = self.metadata[idx]
            results.append({
                "content": self.content_lookup.get(item_meta["url"], "Content not available"),
                "score": float(scores[idx]),
                "metadata": {
                    "title": item_meta.get("title", "Untitled"),
                    "url": item_meta.get("url", "#"),
                    "source": item_meta.get("source", "unknown"),
                    **item_meta.get("metadata", {})
                }
            })
        
        return results

    def retrieve_with_threshold(self, query: str, top_k: int = 3, min_score: float = 0.5) -> List[Dict]:
        """Retrieve documents with similarity score above threshold"""
        results = self.retrieve(query, top_k)
        return [r for r in results if r["score"] >= min_score]
