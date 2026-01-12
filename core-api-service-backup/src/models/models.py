from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="user")  # user or admin
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class RSSSource(Base):
    __tablename__ = "rss_sources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    url = Column(String(500), unique=True, nullable=False)
    category = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    articles = relationship("Article", back_populates="source")

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    link = Column(Text, unique=True, nullable=False)
    content = Column(Text)
    published = Column(String(100))
    summary = Column(Text)
    image_url = Column(Text)
    source_id = Column(Integer, ForeignKey("rss_sources.id"))
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())
    
    source = relationship("RSSSource", back_populates="articles")

class SavedArticle(Base):
    __tablename__ = "saved_articles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    saved_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User")
    article = relationship("Article")

class ReadingHistory(Base):
    __tablename__ = "reading_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    read_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User")
    article = relationship("Article")
    
    __table_args__ = (UniqueConstraint('user_id', 'article_id', name='unique_user_article_read'),)

class CrawlerConfig(Base):
    __tablename__ = "crawler_config"
    
    id = Column(Integer, primary_key=True, index=True)
    cron_schedule = Column(String(100), default="0 */6 * * *")  # Every 6 hours by default
    is_enabled = Column(Boolean, default=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
