#!/usr/bin/env python3
"""
Script to add sample articles to the database for testing different categories.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'core-api-service'))

from src.models.database import SessionLocal
from src.models.models import Article, RSSSource
from datetime import datetime, timedelta
import random

def create_sample_sources():
    """Create sample RSS sources if they don't exist"""
    db = SessionLocal()
    try:
        # Check if sources already exist
        existing_sources = db.query(RSSSource).count()
        if existing_sources > 0:
            print("Sources already exist, skipping creation")
            return

        sources_data = [
            {"name": "VNExpress Kinh Doanh", "url": "https://vnexpress.net/rss/kinh-doanh.rss", "category": "business"},
            {"name": "VNExpress Công Nghệ", "url": "https://vnexpress.net/rss/so-hoa.rss", "category": "technology"},
            {"name": "VNExpress Thể Thao", "url": "https://vnexpress.net/rss/the-thao.rss", "category": "sports"},
            {"name": "VNExpress Giải Trí", "url": "https://vnexpress.net/rss/giai-tri.rss", "category": "entertainment"},
            {"name": "VNExpress Chính Trị", "url": "https://vnexpress.net/rss/chinh-tri.rss", "category": "politics"},
            {"name": "VNExpress Sức Khỏe", "url": "https://vnexpress.net/rss/suc-khoe.rss", "category": "health"},
            {"name": "VNExpress Giáo Dục", "url": "https://vnexpress.net/rss/giao-duc.rss", "category": "education"},
            {"name": "VNExpress Pháp Luật", "url": "https://vnexpress.net/rss/phap-luat.rss", "category": "law"},
        ]

        for source_data in sources_data:
            source = RSSSource(
                name=source_data["name"],
                url=source_data["url"],
                category=source_data["category"],
                is_active=True
            )
            db.add(source)

        db.commit()
        print(f"Created {len(sources_data)} sample sources")

    except Exception as e:
        db.rollback()
        print(f"Error creating sources: {e}")
    finally:
        db.close()

def create_sample_articles():
    """Create sample articles for different categories"""
    db = SessionLocal()
    try:
        # Check if articles already exist
        existing_articles = db.query(Article).count()
        if existing_articles > 0:
            print("Articles already exist, skipping creation")
            return

        # Get sources
        sources = db.query(RSSSource).all()
        if not sources:
            print("No sources found, creating sources first")
            create_sample_sources()
            sources = db.query(RSSSource).all()

        # Sample articles data
        articles_data = [
            # Business articles
            {
                "title": "Cổ phiếu công nghệ tăng mạnh nhờ AI",
                "summary": "Các công ty công nghệ lớn báo cáo lợi nhuận kỷ lục nhờ vào các ứng dụng trí tuệ nhân tạo.",
                "content": "Thị trường chứng khoán ghi nhận sự tăng trưởng mạnh mẽ từ các cổ phiếu công nghệ...",
                "url": "https://vnexpress.net/ai-boosts-tech-stocks",
                "category": "business",
                "published": datetime.now() - timedelta(hours=2)
            },
            {
                "title": "Ngân hàng trung ương hạ lãi suất",
                "summary": "Quyết định hạ lãi suất nhằm kích thích nền kinh tế sau thời kỳ suy thoái.",
                "content": "Ngân hàng trung ương đã thông báo hạ lãi suất cơ bản xuống mức thấp kỷ lục...",
                "url": "https://vnexpress.net/central-bank-cuts-rates",
                "category": "business",
                "published": datetime.now() - timedelta(hours=4)
            },
            {
                "title": "Doanh nghiệp xuất khẩu tăng trưởng 15%",
                "summary": "Số liệu mới nhất cho thấy xuất khẩu tăng mạnh trong quý vừa qua.",
                "content": "Theo số liệu từ Bộ Công Thương, xuất khẩu đã tăng 15% so với cùng kỳ...",
                "url": "https://vnexpress.net/export-growth-15-percent",
                "category": "business",
                "published": datetime.now() - timedelta(hours=6)
            },

            # Technology articles
            {
                "title": "ChatGPT đạt 100 triệu người dùng",
                "summary": "Mô hình AI phổ biến nhất thế giới vừa đạt mốc người dùng mới.",
                "content": "OpenAI thông báo ChatGPT đã đạt 100 triệu người dùng hoạt động...",
                "url": "https://vnexpress.net/chatgpt-100-million-users",
                "category": "technology",
                "published": datetime.now() - timedelta(hours=1)
            },
            {
                "title": "iPhone 16 ra mắt với camera mới",
                "summary": "Apple giới thiệu thế hệ iPhone mới với công nghệ camera tiên tiến.",
                "content": "Tại sự kiện ra mắt, Apple đã công bố iPhone 16 với hệ thống camera 48MP...",
                "url": "https://vnexpress.net/iphone-16-new-camera",
                "category": "technology",
                "published": datetime.now() - timedelta(hours=3)
            },
            {
                "title": "Meta ra mắt AI tạo video",
                "summary": "Mạng xã hội lớn nhất thế giới tung ra công cụ AI tạo video tự động.",
                "content": "Meta vừa công bố công cụ AI mới có khả năng tạo video từ văn bản...",
                "url": "https://vnexpress.net/meta-ai-video-generator",
                "category": "technology",
                "published": datetime.now() - timedelta(hours=5)
            },

            # Sports articles
            {
                "title": "Việt Nam vô địch AFF Cup 2023",
                "summary": "Đội tuyển Việt Nam giành chức vô địch AFF Cup sau chiến thắng kịch tính.",
                "content": "Trong trận chung kết đầy kịch tính, đội tuyển Việt Nam đã vượt qua Thái Lan...",
                "url": "https://vnexpress.net/vietnam-aff-cup-champion",
                "category": "sports",
                "published": datetime.now() - timedelta(hours=8)
            },
            {
                "title": "Messi gia nhập Inter Miami",
                "summary": "Siêu sao bóng đá Lionel Messi chính thức ký hợp đồng với Inter Miami.",
                "content": "Sau khi hết hợp đồng với PSG, Messi đã chọn Inter Miami làm bến đỗ tiếp theo...",
                "url": "https://vnexpress.net/messi-joins-inter-miami",
                "category": "sports",
                "published": datetime.now() - timedelta(hours=10)
            },
            {
                "title": "Olympic Paris 2024: Việt Nam giành 1 HCV",
                "summary": "Vận động viên Việt Nam giành huy chương vàng đầu tiên tại Olympic.",
                "content": "Trong môn thể dục dụng cụ, vận động viên Việt Nam đã xuất sắc giành HCV...",
                "url": "https://vnexpress.net/olympic-vietnam-gold-medal",
                "category": "sports",
                "published": datetime.now() - timedelta(hours=12)
            },

            # Entertainment articles
            {
                "title": "Black Panther 2 phá kỷ lục phòng vé",
                "summary": "Phim siêu anh hùng mới nhất phá vỡ kỷ lục doanh thu cuối tuần.",
                "content": "Black Panther: Wakanda Forever đã thu về hơn 300 triệu USD trong tuần đầu...",
                "url": "https://vnexpress.net/black-panther-2-box-office",
                "category": "entertainment",
                "published": datetime.now() - timedelta(hours=7)
            },
            {
                "title": "Taylor Swift phát hành album mới",
                "summary": "Ca sĩ nổi tiếng nhất thế giới tung ra album phòng thu thứ 10.",
                "content": "Taylor Swift vừa phát hành album 'Midnights' với 13 bài hát mới...",
                "url": "https://vnexpress.net/taylor-swift-new-album",
                "category": "entertainment",
                "published": datetime.now() - timedelta(hours=9)
            },
            {
                "title": "Oscar 2024: Danh sách đề cử công bố",
                "summary": "Học viện Khoa học và Nghệ thuật Điện ảnh công bố đề cử Oscar 2024.",
                "content": "Phim 'Oppenheimer' dẫn đầu với 13 đề cử, tiếp theo là 'Poor Things' với 11 đề cử...",
                "url": "https://vnexpress.net/oscar-2024-nominations",
                "category": "entertainment",
                "published": datetime.now() - timedelta(hours=11)
            },

            # Politics articles
            {
                "title": "Chính phủ thông qua ngân sách 2024",
                "summary": "Quốc hội thông qua dự toán ngân sách nhà nước năm 2024.",
                "content": "Sau nhiều phiên thảo luận, Quốc hội đã thông qua ngân sách với tổng chi 2.500 tỷ...",
                "url": "https://vnexpress.net/government-budget-2024",
                "category": "politics",
                "published": datetime.now() - timedelta(hours=13)
            },
            {
                "title": "Hội nghị thượng đỉnh APEC thành công",
                "summary": "Các lãnh đạo APEC cam kết tăng cường hợp tác kinh tế.",
                "content": "Hội nghị thượng đỉnh APEC 2023 đã kết thúc thành công với nhiều thỏa thuận quan trọng...",
                "url": "https://vnexpress.net/apec-summit-success",
                "category": "politics",
                "published": datetime.now() - timedelta(hours=15)
            },
            {
                "title": "Bầu cử giữa nhiệm kỳ Mỹ kết thúc",
                "summary": "Đảng Dân chủ giành quyền kiểm soát Thượng viện.",
                "content": "Kết quả bầu cử giữa nhiệm kỳ cho thấy sự thay đổi lớn trong cán cân quyền lực...",
                "url": "https://vnexpress.net/us-midterm-elections-results",
                "category": "politics",
                "published": datetime.now() - timedelta(hours=17)
            },

            # Health articles
            {
                "title": "Khám phá vaccine COVID-19 mới",
                "summary": "Các nhà khoa học phát triển vaccine thế hệ mới chống lại biến thể mới.",
                "content": "Vaccine mới có khả năng chống lại tất cả biến thể hiện tại và tương lai...",
                "url": "https://vnexpress.net/new-covid-vaccine-discovery",
                "category": "health",
                "published": datetime.now() - timedelta(hours=14)
            },
            {
                "title": "Cách phòng ngừa bệnh tim mạch",
                "summary": "Các chuyên gia đưa ra lời khuyên phòng ngừa bệnh tim mạch hiệu quả.",
                "content": "Bệnh tim mạch là nguyên nhân gây tử vong hàng đầu trên thế giới...",
                "url": "https://vnexpress.net/heart-disease-prevention",
                "category": "health",
                "published": datetime.now() - timedelta(hours=16)
            },
            {
                "title": "Công nghệ mới trong phẫu thuật não",
                "summary": "Robot phẫu thuật giúp thực hiện các ca mổ não chính xác hơn.",
                "content": "Công nghệ robot mới cho phép phẫu thuật não với độ chính xác micromet...",
                "url": "https://vnexpress.net/brain-surgery-robot",
                "category": "health",
                "published": datetime.now() - timedelta(hours=18)
            },

            # Education articles
            {
                "title": "Đổi mới chương trình giáo dục phổ thông",
                "summary": "Bộ Giáo dục công bố chương trình học mới cho bậc phổ thông.",
                "content": "Chương trình mới nhấn mạnh phát triển kỹ năng và tư duy phản biện...",
                "url": "https://vnexpress.net/education-curriculum-reform",
                "category": "education",
                "published": datetime.now() - timedelta(hours=19)
            },
            {
                "title": "Học trực tuyến tăng trưởng mạnh",
                "summary": "Số lượng học viên tham gia các khóa học online tăng 200%.",
                "content": "Theo khảo sát, học trực tuyến đã trở thành xu hướng chính trong giáo dục...",
                "url": "https://vnexpress.net/online-learning-growth",
                "category": "education",
                "published": datetime.now() - timedelta(hours=21)
            },
            {
                "title": "Đại học Việt Nam trong bảng xếp hạng",
                "summary": "Một số trường đại học Việt Nam lọt top 1000 thế giới.",
                "content": "Theo bảng xếp hạng QS World University Rankings 2024...",
                "url": "https://vnexpress.net/vietnamese-universities-ranking",
                "category": "education",
                "published": datetime.now() - timedelta(hours=23)
            },

            # Law articles
            {
                "title": "Luật An toàn giao thông sửa đổi",
                "summary": "Quốc hội thông qua luật mới tăng cường xử phạt vi phạm giao thông.",
                "content": "Luật mới quy định mức phạt cao hơn cho các hành vi nguy hiểm...",
                "url": "https://vnexpress.net/traffic-safety-law-amendment",
                "category": "law",
                "published": datetime.now() - timedelta(hours=20)
            },
            {
                "title": "Tòa án xử vụ tham nhũng lớn",
                "summary": "Các bị cáo nhận án tù chung thân trong vụ tham nhũng nghìn tỷ.",
                "content": "Tòa án nhân dân tối cao đã tuyên án trong vụ tham nhũng lớn nhất từ trước đến nay...",
                "url": "https://vnexpress.net/major-corruption-case-verdict",
                "category": "law",
                "published": datetime.now() - timedelta(hours=22)
            },
            {
                "title": "Luật Bảo vệ dữ liệu cá nhân",
                "summary": "Việt Nam thông qua luật bảo vệ dữ liệu cá nhân theo chuẩn EU.",
                "content": "Luật mới quy định quyền của cá nhân đối với dữ liệu của mình...",
                "url": "https://vnexpress.net/personal-data-protection-law",
                "category": "law",
                "published": datetime.now() - timedelta(hours=24)
            },
        ]

        # Create articles
        for article_data in articles_data:
            # Find matching source
            source = None
            for s in sources:
                if s.category == article_data["category"]:
                    source = s
                    break

            if not source:
                # Use first source as fallback
                source = sources[0]

            article = Article(
                title=article_data["title"],
                summary=article_data["summary"],
                content=article_data["content"],
                url=article_data["url"],
                published=article_data["published"],
                source_id=source.id,
                fetched_at=datetime.now()
            )
            db.add(article)

        db.commit()
        print(f"Created {len(articles_data)} sample articles")

    except Exception as e:
        db.rollback()
        print(f"Error creating articles: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating sample data...")
    create_sample_sources()
    create_sample_articles()
    print("Sample data creation completed!")