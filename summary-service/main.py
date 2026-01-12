from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import logging

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Summary Service",
    description="LLM-based text summarization service",
    version="1.0.0"
)

class SummaryRequest(BaseModel):
    text: str
    url: str = None

class SummaryResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int

# Initialize summarization pipeline
logger.info("Loading summarization model...")
summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
logger.info("Model loaded successfully!")

@app.get("/")
def root():
    return {
        "service": "Summary Service",
        "version": "1.0.0",
        "model": "facebook/bart-large-cnn"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "summary-service",
        "model": "facebook/bart-large-cnn"
    }

@app.post("/api/v1/summary/generate", response_model=SummaryResponse)
def generate_summary(request: SummaryRequest):
    """Generate summary for article text"""
    if not request.text or len(request.text.strip()) < 50:
        raise HTTPException(
            status_code=400,
            detail="Text is too short for summarization (minimum 50 characters)"
        )
    
    try:
        # Limit input text length for the model
        max_input_length = 1024
        text = request.text[:max_input_length] if len(request.text) > max_input_length else request.text
        
        # Generate summary
        summary_result = summarizer(
            text,
            max_length=150,
            min_length=40,
            do_sample=False
        )
        
        summary_text = summary_result[0]['summary_text']
        
        logger.info(f"Generated summary for text (length: {len(request.text)})")
        
        return {
            "summary": summary_text,
            "original_length": len(request.text),
            "summary_length": len(summary_text)
        }
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8002)
