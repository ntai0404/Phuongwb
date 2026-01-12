# Class Diagrams

This document contains the analysis class diagram and general class diagram for the news aggregation system.

## Analysis Class Diagram

The analysis class diagram shows the main domain concepts and their relationships identified during the analysis phase.

```plantuml
@startuml Analysis Class Diagram

class User {
    +id: int
    +username: string
    +email: string
    +hashed_password: string
    +role: string
    +created_at: datetime
    +updated_at: datetime
    --
    +register()
    +login()
    +updateProfile()
}

class RSSSource {
    +id: int
    +name: string
    +url: string
    +category: string
    +is_active: boolean
    +created_at: datetime
    +updated_at: datetime
    --
    +addSource()
    +updateSource()
    +deactivateSource()
}

class Article {
    +id: int
    +title: string
    +link: string
    +content: string
    +published: string
    +summary: string
    +image_url: string
    +source_id: int
    +fetched_at: datetime
    --
    +fetchContent()
    +summarize()
    +categorize()
}

class SavedArticle {
    +id: int
    +user_id: int
    +article_id: int
    +saved_at: datetime
    --
    +saveArticle()
    +removeFromSaved()
}

class ReadingHistory {
    +id: int
    +user_id: int
    +article_id: int
    +read_at: datetime
    --
    +markAsRead()
    +getReadingHistory()
}

class CrawlerConfig {
    +id: int
    +cron_schedule: string
    +is_enabled: boolean
    +updated_at: datetime
    --
    +updateSchedule()
    +enableCrawler()
    +disableCrawler()
}

User ||--o{ SavedArticle : saves
User ||--o{ ReadingHistory : reads
RSSSource ||--o{ Article : provides
Article ||--o{ SavedArticle : saved by
Article ||--o{ ReadingHistory : read by

@enduml
```

## General Class Diagram

The general class diagram shows the main implementation classes and their relationships in the system architecture.

```plantuml
@startuml General Class Diagram

package "Core API Service" {
    class ArticleRoutes {
        +get_articles()
        +get_article_by_id()
        +save_article()
        +get_saved_articles()
        +mark_as_read()
        +get_reading_history()
    }

    class AuthRoutes {
        +register()
        +login()
        +refresh_token()
        +get_current_user()
    }

    class SourceRoutes {
        +get_sources()
        +create_source()
        +update_source()
        +delete_source()
    }

    class AdminRoutes {
        +get_users()
        +update_user_role()
        +get_system_stats()
    }

    class ArticleService {
        +fetch_articles_from_sources()
        +process_article_content()
        +store_articles()
    }

    class AuthService {
        +authenticate_user()
        +generate_tokens()
        +verify_token()
    }
}

package "Crawler Service" {
    class CrawlerService {
        +crawl_rss_sources()
        +extract_article_data()
        +send_to_core_api()
    }
}

package "Recommendation Service" {
    class RecommendationEngine {
        +analyze_user_preferences()
        +generate_recommendations()
        +rank_articles()
    }
}

package "Summary Service" {
    class SummarizationEngine {
        +summarize_article()
        +extract_key_points()
        +generate_summary()
    }
}

package "Frontend" {
    class NewsCard {
        +article: Article
        +onClick()
        +markAsRead()
        +saveArticle()
    }

    class NewsGrid {
        +articles: Article[]
        +renderArticles()
        +handlePagination()
    }

    class AuthProvider {
        +user: User
        +login()
        +logout()
        +refreshToken()
    }

    class ApiClient {
        +get()
        +post()
        +put()
        +delete()
    }
}

ArticleRoutes --> ArticleService : uses
AuthRoutes --> AuthService : uses
CrawlerService --> ArticleService : sends articles
RecommendationEngine --> ArticleService : analyzes articles
SummarizationEngine --> ArticleService : summarizes articles
NewsCard --> ApiClient : calls
NewsGrid --> ApiClient : calls
AuthProvider --> ApiClient : calls

@enduml
```

## Diagram Explanations

### Analysis Class Diagram
- **User**: Represents system users with authentication and profile management capabilities
- **RSSSource**: Represents RSS feed sources that provide articles
- **Article**: Core entity representing news articles with content and metadata
- **SavedArticle**: Junction entity for user's saved articles
- **ReadingHistory**: Tracks user's reading activity
- **CrawlerConfig**: Configuration for the crawling system

### General Class Diagram
- **Core API Service**: Main backend service with route handlers and business logic
- **Crawler Service**: Handles RSS feed crawling and article extraction
- **Recommendation Service**: Provides personalized article recommendations
- **Summary Service**: Generates article summaries
- **Frontend**: React components and utilities for user interface

The relationships show the dependencies and data flow between different components of the system.