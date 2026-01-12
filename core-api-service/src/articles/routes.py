from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime, timezone

from sqlalchemy import text
from ..models.database import get_db
from ..models import Article
from ..auth.security import get_current_admin, get_current_user
from ..models.models import User, SavedArticle, ReadingHistory
from .schemas import ArticleResponse, SavedArticleResponse, ReadingHistoryResponse

router = APIRouter(prefix="/api/v1/articles", tags=["Articles"])

@router.get("", response_model=List[ArticleResponse])
def list_articles(
    source_id: Optional[int] = Query(None, description="Filter by source ID"),
    ids: Optional[List[int]] = Query(None, description="Filter by article IDs"),
    date_from: Optional[str] = Query(None, description="Filter from date (ISO format)"),
    date_to: Optional[str] = Query(None, description="Filter to date (ISO format)"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Get list of articles with pagination and filters (Public access)"""
    query = db.query(Article)
    
    # Apply filters
    if source_id:
        query = query.filter(Article.source_id == source_id)
    
    if ids:
        query = query.filter(Article.id.in_(ids))
    
    # For date filtering, we'd need to parse and compare properly
    # This is a simplified version
    if date_from:
        query = query.filter(Article.published >= date_from)
    if date_to:
        query = query.filter(Article.published <= date_to)
    
    # Order by fetched_at descending
    query = query.order_by(Article.fetched_at.desc())
    
    # Apply pagination
    offset = (page - 1) * per_page
    articles = query.offset(offset).limit(per_page).all()
    
    return articles

@router.get("/saved", response_model=List[SavedArticleResponse])
def get_saved_articles(
    user_id: int = Query(1, description="User ID"),
    db: Session = Depends(get_db)
):
    """Get user's saved articles"""
    saved = db.query(SavedArticle).options(
        joinedload(SavedArticle.article).joinedload(Article.source)
    ).filter(SavedArticle.user_id == user_id).all()
    return saved

@router.get("/history", response_model=List[ReadingHistoryResponse])
def get_reading_history(
    user_id: int = Query(1, description="User ID"),
    db: Session = Depends(get_db)
):
    """Get user's reading history"""
    history = db.query(ReadingHistory).options(
        joinedload(ReadingHistory.article).joinedload(Article.source)
    ).filter(ReadingHistory.user_id == user_id).order_by(ReadingHistory.read_at.desc()).all()
    return history

@router.get("/{article_id}", response_model=ArticleResponse)
def get_article(article_id: int, db: Session = Depends(get_db)):
    """Get article details (Public access)"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    return article

@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(
    article_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete article (Admin only)"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    db.delete(article)
    db.commit()
    
    return None

@router.post("/save/{article_id}", status_code=status.HTTP_201_CREATED)
def save_article(
    article_id: int,
    user_id: int = Query(1, description="User ID"),
    db: Session = Depends(get_db)
):
    """Save article for user"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    # Check if already saved
    existing = db.query(SavedArticle).filter(
        SavedArticle.user_id == user_id,
        SavedArticle.article_id == article_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Article already saved"
        )
    
    saved = SavedArticle(user_id=user_id, article_id=article_id)
    db.add(saved)
    db.commit()
    
    return {"message": "Article saved"}

@router.delete("/save/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def unsave_article(
    article_id: int,
    user_id: int = Query(1, description="User ID"),
    db: Session = Depends(get_db)
):
    """Unsave article for user"""
    saved = db.query(SavedArticle).filter(
        SavedArticle.user_id == user_id,
        SavedArticle.article_id == article_id
    ).first()
    if not saved:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not saved"
        )
    
    db.delete(saved)
    db.commit()
    
    return None

@router.get("/saved/{article_id}")
def check_article_saved(
    article_id: int,
    user_id: int = Query(1, description="User ID"),
    db: Session = Depends(get_db)
):
    """Check if article is saved by user"""
    saved = db.query(SavedArticle).filter(
        SavedArticle.user_id == user_id,
        SavedArticle.article_id == article_id
    ).first()
    return {"is_saved": saved is not None}

@router.post("/read/{article_id}", status_code=status.HTTP_201_CREATED)
def mark_as_read(
    article_id: int,
    user_id: int = Query(1, description="User ID"),
    db: Session = Depends(get_db)
):
    """Mark article as read for user"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    # Upsert reading history
    db.execute(text("""
        INSERT INTO reading_history (user_id, article_id, read_at)
        VALUES (:user_id, :article_id, NOW())
        ON CONFLICT ON CONSTRAINT unique_user_article_read
        DO UPDATE SET read_at = NOW()
    """), {"user_id": user_id, "article_id": article_id})
    db.commit()
    
    return {"message": "Article marked as read"}
