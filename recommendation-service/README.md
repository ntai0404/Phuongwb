# Recommendation Service

AI-powered article recommendation service using vector search with Qdrant.

## Features

- **Vector Embeddings**: Generate embeddings for articles using Sentence Transformers
- **Semantic Search**: Natural language search across articles
- **Article Recommendations**: Find similar articles based on content

## Technology Stack

- FastAPI
- Sentence Transformers (HuggingFace)
- Qdrant Vector Database Client
- PyTorch

## API Endpoints

- `POST /api/v1/vectors/upsert` - Index article in vector database
- `POST /api/v1/search/semantic` - Semantic search with natural language
- `GET /api/v1/recommend/{id}` - Get similar articles
- `GET /health` - Health check

## Environment Variables

- `QDRANT_HOST` - Qdrant host (default: qdrant)
- `QDRANT_PORT` - Qdrant port (default: 6333)
- `MODEL_NAME` - Sentence transformer model (default: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)

## Running

```bash
# Install dependencies
pip install -r requirements.txt

# Run the service
uvicorn main:app --host 0.0.0.0 --port 8001
```

## Docker

```bash
docker build -t recommendation-service .
docker run -p 8001:8001 recommendation-service
```

## Model

The service uses `paraphrase-multilingual-MiniLM-L12-v2` by default, which supports:
- Vietnamese
- English
- And 50+ other languages

For better performance, consider using GPU-enabled deployment.
