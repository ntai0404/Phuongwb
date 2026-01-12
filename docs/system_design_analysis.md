# Phân Tích Thiết Kế Hệ Thống - Phuong Web

## 1. Tổng Quan Hệ Thống

Phuong Web là một hệ thống ứng dụng tin tức hiện đại được xây dựng theo kiến trúc microservices. Hệ thống cho phép người dùng đọc, lưu trữ và quản lý tin tức từ nhiều nguồn RSS khác nhau, với khả năng gợi ý tin tức cá nhân hóa và tóm tắt nội dung.

### Kiến Trúc Tổng Quan
- **Frontend**: Ứng dụng web React/Next.js chạy trên port 3000
- **Core API Service**: API chính (FastAPI) trên port 8080
- **Crawler Service**: Dịch vụ thu thập tin tức
- **Recommendation Service**: Dịch vụ gợi ý tin tức trên port 8001
- **Summary Service**: Dịch vụ tóm tắt tin tức trên port 8002
- **Cơ sở dữ liệu**: PostgreSQL, Redis cache, RabbitMQ message queue, Qdrant vector database

## 2. Sơ Đồ Use Case Tổng Quát

### Các Actor của Ứng dụng

1. **Người dùng (User)**: Người dùng cuối của hệ thống tin tức
   - Có thể là người dùng đã đăng ký hoặc khách vãng lai
   - Sử dụng ứng dụng để đọc và quản lý tin tức

2. **Quản trị viên (Administrator)**: Người quản lý hệ thống
   - Quản lý các nguồn tin RSS
   - Giám sát hoạt động của hệ thống
   - Quản lý crawler và các tác vụ nền

3. **Hệ thống bên ngoài (External Systems)**:
   - Các nguồn RSS feeds
   - Dịch vụ AI cho gợi ý và tóm tắt

### Các Use Case của Ứng dụng

#### Với Người dùng:
1. **UC đăng ký tài khoản**: Cho phép người dùng tạo tài khoản mới trong hệ thống thông qua việc cung cấp thông tin đăng ký cơ bản như email và mật khẩu, từ đó có thể sử dụng đầy đủ các chức năng của hệ thống.
2. **UC đăng nhập hệ thống**: Cho phép người dùng xác thực danh tính để truy cập vào hệ thống, sử dụng các chức năng cá nhân hóa và quản lý dữ liệu người dùng.
3. **UC xem danh sách tin tức**: Người dùng có thể xem danh sách các tin tức được hệ thống tổng hợp từ nhiều nguồn khác nhau, có hỗ trợ phân trang và bộ lọc theo tiêu chí.
4. **UC đọc chi tiết tin tức**: Người dùng có thể xem nội dung đầy đủ của một bài viết, bao gồm tiêu đề, nội dung chi tiết và các thông tin liên quan.
5. **UC lưu trữ tin tức**: Cho phép người dùng lưu các bài viết quan tâm để đọc lại sau, giúp quản lý và theo dõi những tin tức quan trọng.
6. **UC xem tin tức đã lưu**: Người dùng có thể xem lại danh sách các bài viết đã được lưu trữ trước đó và quản lý danh sách này.
7. **UC xem lịch sử đọc**: Cho phép người dùng xem lại các bài viết đã từng đọc, giúp theo dõi thói quen đọc tin và dễ dàng truy cập lại nội dung đã xem.
8. **UC tìm kiếm tin tức**: Người dùng có thể tìm kiếm tin tức theo từ khóa, danh mục hoặc tiêu chí liên quan để nhanh chóng tiếp cận thông tin mong muốn.
9. **UC nhận gợi ý tin tức cá nhân hóa**: Hệ thống đề xuất các bài viết phù hợp dựa trên lịch sử đọc và hành vi sử dụng của người dùng nhằm nâng cao trải nghiệm cá nhân hóa.
10. **UC xem tóm tắt tin tức**: Người dùng có thể xem nội dung tóm tắt của bài viết để nhanh chóng nắm bắt thông tin chính mà không cần đọc toàn bộ nội dung.

#### Với Quản trị viên:
1. **UC quản lý nguồn RSS**: Quản trị viên có thể thêm, chỉnh sửa hoặc xóa các nguồn RSS nhằm đảm bảo hệ thống luôn cập nhật tin tức từ những nguồn phù hợp.
2. **UC quản lý tác vụ crawler**: Quản trị viên có thể quản lý và giám sát các tác vụ thu thập tin tức tự động từ các nguồn RSS.
3. **UC quản lý người dùng**: Quản trị viên có thể quản lý tài khoản người dùng, bao gồm xem thông tin, khóa hoặc mở khóa tài khoản khi cần thiết.

## 3. Mô Tả Chi Tiết Use Case

### 3.1 UC đăng ký tài khoản
**Actor**: Người dùng  
**Mô tả**: Cho phép người dùng tạo tài khoản mới trong hệ thống thông qua việc cung cấp thông tin đăng ký cơ bản như email và mật khẩu, từ đó có thể sử dụng đầy đủ các chức năng của hệ thống.  
**Điều kiện tiên quyết**: Người dùng chưa có tài khoản  
**Luồng chính**:
1. Người dùng nhập thông tin đăng ký (email, mật khẩu)
2. Hệ thống kiểm tra tính hợp lệ của thông tin
3. Hệ thống tạo tài khoản mới
4. Hệ thống gửi email xác nhận (nếu có)
5. Người dùng được chuyển đến trang đăng nhập

### 3.2 UC đăng nhập hệ thống
**Actor**: Người dùng  
**Mô tả**: Cho phép người dùng xác thực danh tính để truy cập vào hệ thống, sử dụng các chức năng cá nhân hóa và quản lý dữ liệu người dùng.  
**Điều kiện tiên quyết**: Người dùng đã có tài khoản  
**Luồng chính**:
1. Người dùng nhập email và mật khẩu
2. Hệ thống kiểm tra thông tin đăng nhập
3. Hệ thống tạo JWT token
4. Token được lưu trữ trong localStorage
5. Người dùng được chuyển đến trang chủ

### 3.3 UC xem danh sách tin tức
**Actor**: Người dùng  
**Mô tả**: Người dùng có thể xem danh sách các tin tức được hệ thống tổng hợp từ nhiều nguồn khác nhau, có hỗ trợ phân trang và bộ lọc theo tiêu chí.  
**Luồng chính**:
1. Người dùng truy cập trang chủ hoặc trang tin tức
2. Hệ thống lấy danh sách tin tức từ database
3. Hệ thống áp dụng bộ lọc (theo nguồn, ngày, từ khóa)
4. Hệ thống trả về danh sách tin tức với phân trang
5. Người dùng có thể điều hướng qua các trang

### 3.4 UC đọc chi tiết tin tức
**Actor**: Người dùng  
**Mô tả**: Người dùng có thể xem nội dung đầy đủ của một bài viết, bao gồm tiêu đề, nội dung chi tiết và các thông tin liên quan.  
**Luồng chính**:
1. Người dùng click vào tiêu đề tin tức
2. Hệ thống lấy thông tin chi tiết bài viết
3. Hệ thống hiển thị modal với nội dung đầy đủ
4. Hệ thống tự động đánh dấu bài viết đã đọc
5. Người dùng có thể lưu bài viết hoặc đóng modal

### 3.5 UC lưu trữ tin tức
**Actor**: Người dùng  
**Mô tả**: Cho phép người dùng lưu các bài viết quan tâm để đọc lại sau, giúp quản lý và theo dõi những tin tức quan trọng.  
**Điều kiện tiên quyết**: Người dùng đã đăng nhập  
**Luồng chính**:
1. Người dùng click nút "Lưu" trên bài viết
2. Hệ thống kiểm tra trạng thái hiện tại
3. Nếu chưa lưu: Thêm vào danh sách đã lưu
4. Nếu đã lưu: Xóa khỏi danh sách đã lưu
5. Hệ thống cập nhật giao diện

### 3.6 UC xem tin tức đã lưu
**Actor**: Người dùng  
**Mô tả**: Người dùng có thể xem lại danh sách các bài viết đã được lưu trữ trước đó và quản lý danh sách này.  
**Điều kiện tiên quyết**: Người dùng đã đăng nhập  
**Luồng chính**:
1. Người dùng truy cập trang "Đã lưu"
2. Hệ thống lấy danh sách bài viết đã lưu
3. Hệ thống hiển thị danh sách với tùy chọn tìm kiếm
4. Người dùng có thể xóa bài viết khỏi danh sách đã lưu

### 3.7 UC xem lịch sử đọc
**Actor**: Người dùng  
**Mô tả**: Cho phép người dùng xem lại các bài viết đã từng đọc, giúp theo dõi thói quen đọc tin và dễ dàng truy cập lại nội dung đã xem.  
**Điều kiện tiên quyết**: Người dùng đã đăng nhập  
**Luồng chính**:
1. Người dùng truy cập trang "Lịch sử"
2. Hệ thống lấy danh sách bài viết đã đọc theo thời gian
3. Hệ thống hiển thị danh sách với tùy chọn tìm kiếm
4. Người dùng có thể xóa mục khỏi lịch sử

### 3.8 UC tìm kiếm tin tức
**Actor**: Người dùng  
**Mô tả**: Người dùng có thể tìm kiếm tin tức theo từ khóa, danh mục hoặc tiêu chí liên quan để nhanh chóng tiếp cận thông tin mong muốn.  
**Luồng chính**:
1. Người dùng nhập từ khóa vào thanh tìm kiếm
2. Hệ thống tìm kiếm trong tiêu đề và tóm tắt
3. Hệ thống trả về kết quả phù hợp
4. Người dùng có thể lọc kết quả theo danh mục

### 3.9 UC nhận gợi ý tin tức cá nhân hóa
**Actor**: Người dùng  
**Mô tả**: Hệ thống đề xuất các bài viết phù hợp dựa trên lịch sử đọc và hành vi sử dụng của người dùng nhằm nâng cao trải nghiệm cá nhân hóa.  
**Luồng chính**:
1. Hệ thống phân tích lịch sử đọc của người dùng
2. Hệ thống gửi yêu cầu đến recommendation service
3. Recommendation service tính toán độ tương đồng
4. Hệ thống hiển thị tin tức gợi ý

### 3.10 Use Case: Quản lý nguồn RSS
**Actor**: Quản trị viên  
**Mô tả**: Quản trị viên thêm/sửa/xóa nguồn RSS  
**Điều kiện tiên quyết**: Quản trị viên đã đăng nhập  
**Luồng chính**:
1. Quản trị viên truy cập trang quản lý sources
2. Quản trị viên chọn thao tác (thêm/sửa/xóa)
3. Hệ thống cập nhật database
4. Hệ thống kích hoạt crawler để thu thập tin mới

### 3.11 UC quản lý nguồn RSS
**Actor**: Quản trị viên  
**Mô tả**: Quản trị viên có thể thêm, chỉnh sửa hoặc xóa các nguồn RSS nhằm đảm bảo hệ thống luôn cập nhật tin tức từ những nguồn phù hợp.  
**Điều kiện tiên quyết**: Quản trị viên đã đăng nhập  
**Luồng chính**:
1. Quản trị viên truy cập trang quản lý sources
2. Quản trị viên chọn thao tác (thêm/sửa/xóa)
3. Hệ thống cập nhật database
4. Hệ thống kích hoạt crawler để thu thập tin mới

### 3.12 UC quản lý tác vụ crawler
**Actor**: Quản trị viên  
**Mô tả**: Quản trị viên có thể quản lý và giám sát các tác vụ thu thập tin tức tự động từ các nguồn RSS.  
**Luồng chính**:
1. Quản trị viên truy cập trang quản lý crawler
2. Hệ thống hiển thị trạng thái các tác vụ crawler
3. Quản trị viên có thể bắt đầu/dừng tác vụ
4. Hệ thống cập nhật trạng thái và logs

### 3.13 UC quản lý người dùng
**Actor**: Quản trị viên  
**Mô tả**: Quản trị viên có thể quản lý tài khoản người dùng, bao gồm xem thông tin, khóa hoặc mở khóa tài khoản khi cần thiết.  
**Luồng chính**:
1. Quản trị viên truy cập trang quản lý người dùng
2. Hệ thống hiển thị danh sách người dùng
3. Quản trị viên chọn hành động (xem thông tin, khóa/mở khóa)
4. Hệ thống cập nhật trạng thái tài khoản

## 4. Kiến Trúc Hệ Thống

### 4.1 Kiến trúc Microservices
Hệ thống được chia thành các microservice độc lập:
- **Core API**: Xử lý logic chính, authentication, CRUD operations
- **Crawler Service**: Thu thập tin tức từ RSS feeds
- **Recommendation Service**: Xử lý gợi ý tin tức
- **Summary Service**: Tóm tắt nội dung tin tức

### 4.2 Công nghệ sử dụng
- **Backend**: Python FastAPI
- **Frontend**: React/Next.js với TypeScript
- **Database**: PostgreSQL
- **Cache**: Redis
- **Message Queue**: RabbitMQ
- **Vector Database**: Qdrant cho semantic search
- **Container**: Docker và Docker Compose

### 4.3 Bảo mật
- JWT authentication cho API
- CORS configuration
- Input validation
- SQL injection prevention qua ORM

## 5. Cơ Sở Dữ Liệu

### Các bảng chính:
- **users**: Thông tin người dùng
- **articles**: Bài viết tin tức
- **rss_sources**: Nguồn RSS feeds
- **saved_articles**: Bài viết đã lưu
- **reading_history**: Lịch sử đọc
- **user_sessions**: Sessions người dùng

## 6. API Endpoints

### Authentication
- POST /api/v1/auth/login
- POST /api/v1/auth/register
- GET /api/v1/auth/users/me

### Articles
- GET /api/v1/articles
- GET /api/v1/articles/{id}
- GET /api/v1/articles/saved
- POST /api/v1/articles/save/{id}
- DELETE /api/v1/articles/save/{id}
- GET /api/v1/articles/history

### Sources
- GET /api/v1/sources
- POST /api/v1/sources
- PUT /api/v1/sources/{id}
- DELETE /api/v1/sources/{id}

### Admin
- GET /api/v1/admin/stats
- GET /api/v1/admin/logs