# Summary Service

LLM-based text summarization service using Facebook's BART model.

## Features

- **Text Summarization**: Generate concise summaries of long articles
- **BART Model**: Uses facebook/bart-large-cnn for high-quality summaries

## Technology Stack

- FastAPI
- Transformers (HuggingFace)
- PyTorch

## API Endpoints

- `POST /api/v1/summary/generate` - Generate article summary
- `GET /health` - Health check

## Request Format

```json
{
  "text": "Your long article text here...",
  "url": "https://example.com/article"  // optional
}
```

## Response Format

```json
{
  "summary": "Generated summary text",
  "original_length": 1024,
  "summary_length": 150
}
```

## Running

```bash
# Install dependencies
pip install -r requirements.txt

# Run the service
uvicorn main:app --host 0.0.0.0 --port 8002
```

## Docker

```bash
docker build -t summary-service .
docker run -p 8002:8002 summary-service
```

## Notes

- First run will download the BART model (~1.6GB)
- Minimum text length: 50 characters
- Maximum input length: 1024 characters (automatically truncated)
- Summary length: 40-150 characters
