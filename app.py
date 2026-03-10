#!/usr/bin/env python3
"""
Semantic Search Engine
Search engine using TF-IDF vectorization and cosine similarity.
Author: Gabriel Demetrios Lafis
"""

import re
import math
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Tuple
from flask import Flask, request, jsonify


class TFIDFVectorizer:
    """TF-IDF vectorizer for document representation."""

    def __init__(self):
        self.vocabulary: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}
        self.doc_count = 0

    @staticmethod
    def tokenize(text: str) -> List[str]:
        """Tokenize and normalize text."""
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", "", text)
        tokens = text.split()
        stop_words = {
            "the", "a", "an", "is", "are", "was", "were", "in", "on", "at",
            "to", "for", "of", "and", "or", "but", "not", "with", "this",
            "that", "it", "be", "as", "by", "from", "has", "have", "had",
        }
        return [t for t in tokens if t not in stop_words and len(t) > 1]

    def fit(self, documents: List[str]) -> None:
        """Build vocabulary and compute IDF from document corpus."""
        self.doc_count = len(documents)
        doc_freq: Dict[str, int] = defaultdict(int)

        for doc in documents:
            tokens = set(self.tokenize(doc))
            for token in tokens:
                doc_freq[token] += 1

        self.vocabulary = {
            word: idx for idx, word in enumerate(sorted(doc_freq.keys()))
        }
        self.idf = {
            word: math.log((self.doc_count + 1) / (freq + 1)) + 1
            for word, freq in doc_freq.items()
        }

    def transform(self, text: str) -> Dict[str, float]:
        """Transform text into a TF-IDF vector."""
        tokens = self.tokenize(text)
        if not tokens:
            return {}

        tf = Counter(tokens)
        max_tf = max(tf.values())
        vector = {}

        for word, count in tf.items():
            if word in self.idf:
                normalized_tf = 0.5 + 0.5 * (count / max_tf)
                vector[word] = normalized_tf * self.idf[word]

        return vector


class SemanticSearchEngine:
    """Search engine with TF-IDF indexing and cosine similarity ranking."""

    def __init__(self):
        self.vectorizer = TFIDFVectorizer()
        self.documents: List[Dict] = []
        self.vectors: List[Dict[str, float]] = []
        self.indexed = False

    def index_documents(self, documents: List[Dict]) -> int:
        """Index a list of documents. Each must have 'id', 'title', 'content'."""
        self.documents = documents
        texts = [f"{doc.get('title', '')} {doc.get('content', '')}" for doc in documents]
        self.vectorizer.fit(texts)
        self.vectors = [self.vectorizer.transform(text) for text in texts]
        self.indexed = True
        return len(documents)

    def add_document(self, doc: Dict) -> None:
        """Add a single document to the index."""
        self.documents.append(doc)
        text = f"{doc.get('title', '')} {doc.get('content', '')}"
        texts = [f"{d.get('title', '')} {d.get('content', '')}" for d in self.documents]
        self.vectorizer.fit(texts)
        self.vectors = [self.vectorizer.transform(t) for t in texts]
        self.indexed = True

    @staticmethod
    def _cosine_similarity(vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
        """Compute cosine similarity between two sparse vectors."""
        common = set(vec_a.keys()) & set(vec_b.keys())
        if not common:
            return 0.0

        dot = sum(vec_a[k] * vec_b[k] for k in common)
        norm_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
        norm_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))

        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    def search(self, query: str, k: int = 10, threshold: float = 0.0) -> List[Dict]:
        """Search documents by query. Returns ranked results."""
        if not self.indexed:
            return []

        query_vector = self.vectorizer.transform(query)
        if not query_vector:
            return []

        results = []
        for i, doc_vector in enumerate(self.vectors):
            score = self._cosine_similarity(query_vector, doc_vector)
            if score > threshold:
                results.append({
                    "document": self.documents[i],
                    "score": round(score, 4),
                    "rank": 0,
                })

        results.sort(key=lambda x: x["score"], reverse=True)
        for rank, result in enumerate(results[:k], 1):
            result["rank"] = rank

        return results[:k]

    def find_similar(self, doc_id: str, k: int = 5) -> List[Dict]:
        """Find documents similar to a given document."""
        target_idx = None
        for i, doc in enumerate(self.documents):
            if doc.get("id") == doc_id:
                target_idx = i
                break

        if target_idx is None:
            return []

        target_vector = self.vectors[target_idx]
        results = []

        for i, doc_vector in enumerate(self.vectors):
            if i != target_idx:
                score = self._cosine_similarity(target_vector, doc_vector)
                if score > 0:
                    results.append({
                        "document": self.documents[i],
                        "similarity": round(score, 4),
                    })

        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:k]

    def get_stats(self) -> Dict:
        """Return engine statistics."""
        return {
            "total_documents": len(self.documents),
            "vocabulary_size": len(self.vectorizer.vocabulary),
            "indexed": self.indexed,
        }


# --- Initialize with sample documents ---
app = Flask(__name__)
engine = SemanticSearchEngine()

SAMPLE_DOCS = [
    {"id": "1", "title": "Introduction to Machine Learning",
     "content": "Machine learning is a subset of computer science that gives computers the ability to learn from data without being explicitly programmed."},
    {"id": "2", "title": "Deep Learning Fundamentals",
     "content": "Deep learning uses neural networks with many layers to model complex patterns in data. Convolutional and recurrent networks are common architectures."},
    {"id": "3", "title": "Natural Language Processing",
     "content": "NLP combines computational linguistics with statistical and machine learning models to process and analyze human language data."},
    {"id": "4", "title": "Data Science with Python",
     "content": "Python is widely used in data science for data analysis, visualization, and building machine learning models using libraries like pandas and scikit-learn."},
    {"id": "5", "title": "Web Development Basics",
     "content": "Web development involves building websites and applications using HTML, CSS, JavaScript, and backend frameworks like Flask and Django."},
    {"id": "6", "title": "Database Systems",
     "content": "Database management systems store, retrieve, and manage data. SQL databases use structured query language while NoSQL databases offer flexible schemas."},
    {"id": "7", "title": "Cloud Computing",
     "content": "Cloud computing delivers computing services over the internet including servers, storage, databases, networking, and software."},
    {"id": "8", "title": "Computer Vision",
     "content": "Computer vision enables machines to interpret visual information from images and videos using deep learning and convolutional neural networks."},
]
engine.index_documents(SAMPLE_DOCS)


@app.route("/")
def index():
    return jsonify({
        "name": "Semantic Search Engine",
        "version": "1.0.0",
        "endpoints": {
            "POST /api/search": "Search documents by query",
            "POST /api/index": "Index new documents",
            "GET /api/similar/<doc_id>": "Find similar documents",
            "GET /api/stats": "Engine statistics",
        },
    })


@app.route("/api/search", methods=["POST"])
def search():
    data = request.get_json() or {}
    query = data.get("query", "")
    k = data.get("k", 10)
    threshold = data.get("threshold", 0.0)

    if not query:
        return jsonify({"error": "query is required"}), 400

    results = engine.search(query, k=k, threshold=threshold)
    return jsonify({"query": query, "results": results, "total": len(results)})


@app.route("/api/index", methods=["POST"])
def index_docs():
    data = request.get_json() or {}
    documents = data.get("documents", [])

    if not documents:
        return jsonify({"error": "documents array is required"}), 400

    for doc in documents:
        if "id" not in doc or "content" not in doc:
            return jsonify({"error": "Each document needs 'id' and 'content'"}), 400

    count = engine.index_documents(engine.documents + documents)
    return jsonify({"message": f"Indexed {len(documents)} new documents", "total": count})


@app.route("/api/similar/<doc_id>")
def similar(doc_id):
    k = request.args.get("k", 5, type=int)
    results = engine.find_similar(doc_id, k=k)
    return jsonify({"doc_id": doc_id, "similar": results})


@app.route("/api/stats")
def stats():
    return jsonify(engine.get_stats())


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
