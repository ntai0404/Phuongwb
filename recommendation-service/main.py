from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import os
import logging

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
QDRANT_HOST = os.getenv('QDRANT_HOST', 'qdrant')
QDRANT_PORT = int(os.getenv('QDRANT_PORT', '6333'))
MODEL_NAME = os.getenv('MODEL_NAME', 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
COLLECTION_NAME = "articles"

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Recommendation Service",
    description="AI-powered article recommendation using vector search",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model and Qdrant client
logger.info(f"Loading embedding model: {MODEL_NAME}")
model = SentenceTransformer(MODEL_NAME)
logger.info("Model loaded successfully")

qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# Pydantic models
class ArticleUpsert(BaseModel):
    id: int
    title: str
    content: str

class SemanticSearchRequest(BaseModel):
    query: str
    top_k: int = 10

class RecommendationResponse(BaseModel):
    id: int
    score: float

@app.on_event("startup")
def startup_event():
    """Initialize Qdrant collection on startup"""
    try:
        # Check if collection exists
        collections = qdrant_client.get_collections().collections
        collection_names = [c.name for c in collections]
        
        if COLLECTION_NAME not in collection_names:
            # Create collection
            qdrant_client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=model.get_sentence_embedding_dimension(),
                    distance=Distance.COSINE
                )
            )
            logger.info(f"Created collection: {COLLECTION_NAME}")
        else:
            logger.info(f"Collection {COLLECTION_NAME} already exists")
    except Exception as e:
        logger.error(f"Error initializing Qdrant collection: {e}")

@app.get("/")
def root():
    return {
        "service": "Recommendation Service",
        "version": "1.0.0",
        "model": MODEL_NAME
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "recommendation-service",
        "model": MODEL_NAME
    }

@app.post("/api/v1/vectors/upsert")
def upsert_article(article: ArticleUpsert):
    """Create embedding for article and store in Qdrant"""
    try:
        # Create combined text for embedding
        text = f"{article.title} {article.content}".strip()
        
        if not text:
            logger.warning(f"Skipping article {article.id}: no content to embed")
            return {
                "status": "skipped",
                "id": article.id,
                "message": "No content to embed"
            }
        
        # Generate embedding
        embedding = model.encode(text).tolist()
        
        # Upsert to Qdrant
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                PointStruct(
                    id=article.id,
                    vector=embedding,
                    payload={
                        "title": article.title,
                        "content": article.content[:500] if article.content else ""  # Store first 500 chars
                    }
                )
            ]
        )
        
        logger.info(f"Upserted article {article.id}: {article.title}")
        
        return {
            "status": "success",
            "id": article.id,
            "message": "Article indexed successfully"
        }
    except Exception as e:
        logger.error(f"Error upserting article: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/search/semantic")
def semantic_search(request: SemanticSearchRequest):
    """Search articles using natural language query"""
    try:
        # Generate query embedding
        query_embedding = model.encode(request.query).tolist()
        
        # Search in Qdrant
        search_results = qdrant_client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_embedding,
            limit=request.top_k
        ).points
        
        results = []
        for hit in search_results:
            results.append({
                "id": hit.id,
                "score": hit.score,
                "title": hit.payload.get("title"),
                "content": hit.payload.get("content")
            })
        
        logger.info(f"Semantic search for '{request.query}' returned {len(results)} results")
        
        return {
            "query": request.query,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        logger.error(f"Error in semantic search: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/recommend/{article_id}")
def recommend_similar(article_id: int, top_k: int = 10):
    """Get similar articles based on article ID"""
    try:
        # Retrieve the article's vector
        article = qdrant_client.retrieve(
            collection_name=COLLECTION_NAME,
            ids=[article_id],
            with_vectors=True
        )
        
        if not article or len(article) == 0:
            logger.warning(f"Article {article_id} not found in vector database, returning empty recommendations")
            return {
                "article_id": article_id,
                "recommendations": [],
                "count": 0
            }
        
        # Search for similar articles
        search_results = qdrant_client.query_points(
            collection_name=COLLECTION_NAME,
            query=article[0].vector,
            limit=top_k + 1  # +1 to exclude the article itself
        ).points
        
        # Filter out the original article
        results = []
        for hit in search_results:
            if hit.id != article_id:
                results.append({
                    "id": hit.id,
                    "score": hit.score,
                    "title": hit.payload.get("title"),
                    "content": hit.payload.get("content")
                })
        
        # Limit to top_k results
        results = results[:top_k]
        
        logger.info(f"Recommendations for article {article_id}: {len(results)} results")
        
        return {
            "article_id": article_id,
            "recommendations": results,
            "count": len(results)
        }
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        return {
            "article_id": article_id,
            "recommendations": [],
            "count": 0,
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
