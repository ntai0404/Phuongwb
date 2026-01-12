from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


from .models import init_db
from .auth.routes import router as auth_router
from .sources.routes import router as sources_router
from .articles.routes import router as articles_router
from .crawler.routes import router as crawler_router
from .admin.routes import router as admin_router
from .worker import start_background_worker

app = FastAPI(
    title="Core API Service",
    description="Central backend service for Phuong Web",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
def startup_event():
    init_db()
    start_background_worker()

# Include routers
app.include_router(auth_router)
app.include_router(sources_router)
app.include_router(articles_router)
app.include_router(crawler_router)
app.include_router(admin_router)

@app.get("/")
def root():
    return {
        "service": "Core API Service",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "core-api"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
