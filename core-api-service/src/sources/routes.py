from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..models import get_db, RSSSource
from ..auth.security import get_current_user, get_current_admin
from ..models.models import User
from .schemas import RSSSourceCreate, RSSSourceUpdate, RSSSourceResponse

router = APIRouter(prefix="/api/v1/sources", tags=["RSS Sources"])

@router.get("", response_model=List[RSSSourceResponse])
def list_sources(db: Session = Depends(get_db)):
    """Get list of RSS sources (Public/User access)"""
    sources = db.query(RSSSource).filter(RSSSource.is_active == True).all()
    return sources

@router.post("", response_model=RSSSourceResponse, status_code=status.HTTP_201_CREATED)
def create_source(
    source_data: RSSSourceCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Add new RSS source (Admin only)"""
    # Check if URL already exists
    existing = db.query(RSSSource).filter(RSSSource.url == source_data.url).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="RSS source with this URL already exists"
        )
    
    new_source = RSSSource(
        name=source_data.name,
        url=source_data.url,
        category=source_data.category
    )
    
    db.add(new_source)
    db.commit()
    db.refresh(new_source)
    
    return new_source

@router.put("/{source_id}", response_model=RSSSourceResponse)
def update_source(
    source_id: int,
    source_data: RSSSourceUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update RSS source information (Admin only)"""
    source = db.query(RSSSource).filter(RSSSource.id == source_id).first()
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="RSS source not found"
        )
    
    # Update fields if provided
    if source_data.name is not None:
        source.name = source_data.name
    if source_data.url is not None:
        # Check if new URL conflicts with another source
        existing = db.query(RSSSource).filter(
            RSSSource.url == source_data.url,
            RSSSource.id != source_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Another RSS source with this URL already exists"
            )
        source.url = source_data.url
    if source_data.category is not None:
        source.category = source_data.category
    if source_data.is_active is not None:
        source.is_active = source_data.is_active
    
    db.commit()
    db.refresh(source)
    
    return source

@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_source(
    source_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete RSS source (Admin only)"""
    source = db.query(RSSSource).filter(RSSSource.id == source_id).first()
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="RSS source not found"
        )
    
    db.delete(source)
    db.commit()
    
    return None
