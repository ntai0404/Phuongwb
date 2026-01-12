"""
Script to classify existing articles in database
Run this once to add categories to existing articles
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import SessionLocal, Article
from src.classifier import classify_article

def classify_existing_articles():
    db = SessionLocal()
    try:
        # Get all articles without category
        articles = db.query(Article).filter(
            (Article.category == None) | (Article.category == '')
        ).all()
        
        print(f"Found {len(articles)} articles to classify")
        
        for i, article in enumerate(articles, 1):
            category = classify_article(
                title=article.title,
                summary=article.summary,
                content=article.content
            )
            
            article.category = category
            
            if i % 10 == 0:
                db.commit()
                print(f"Classified {i}/{len(articles)} articles...")
        
        db.commit()
        print(f"\n✅ Successfully classified {len(articles)} articles!")
        
        # Show category distribution
        from sqlalchemy import func
        stats = db.query(
            Article.category, 
            func.count(Article.id).label('count')
        ).group_by(Article.category).all()
        
        print("\n📊 Category distribution:")
        for category, count in stats:
            print(f"  {category or 'None'}: {count} articles")
            
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    classify_existing_articles()
