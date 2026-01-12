# Kịch Bản Mô Tả Chi Tiết Use Cases - Phuong Web

## UC đăng ký tài khoản

| Thông tin | Chi tiết |
|----------|----------|
| **Use case** | Đăng ký tài khoản |
| **Actor** | Người dùng |
| **Tiền điều kiện** | Người dùng truy cập vào ứng dụng và chưa có tài khoản |
| **Hậu điều kiện** | Tài khoản người dùng được tạo thành công và có thể sử dụng các chức năng |

**Kịch bản chính:**
1. Người dùng chọn chức năng "Đăng ký" trên giao diện ứng dụng
2. Hệ thống hiển thị giao diện đăng ký với: ô nhập email, ô nhập mật khẩu, ô xác nhận mật khẩu và nút đăng ký
3. Người dùng nhập thông tin email hợp lệ, mật khẩu mạnh và xác nhận mật khẩu khớp
4. Người dùng click nút "Đăng ký"
5. Hệ thống kiểm tra tính hợp lệ của thông tin và tạo tài khoản mới
6. Hệ thống gửi email xác nhận (nếu có) và chuyển hướng người dùng đến trang đăng nhập

**Ngoại lệ:**
- Email đã tồn tại: Hệ thống hiển thị thông báo "Email đã được sử dụng"
- Mật khẩu yếu: Hệ thống hiển thị thông báo "Mật khẩu phải có ít nhất 8 ký tự"
- Xác nhận mật khẩu không khớp: Hệ thống hiển thị thông báo "Mật khẩu xác nhận không khớp"

---

## UC đăng nhập hệ thống

| Thông tin | Chi tiết |
|----------|----------|
| **Use case** | Đăng nhập hệ thống |
| **Actor** | Người dùng |
| **Tiền điều kiện** | Người dùng đã có tài khoản và truy cập vào ứng dụng |
| **Hậu điều kiện** | Người dùng đăng nhập thành công và truy cập được các chức năng cá nhân hóa |

**Kịch bản chính:**
1. Người dùng chọn chức năng đăng nhập trên giao diện ứng dụng
2. Hệ thống hiển thị giao diện đăng nhập với: một ô nhập email, một ô nhập password và nút login
3. Người dùng nhập email bằng abc@gmail.com, password bằng ***** và click login
4. Hệ thống xác thực thông tin đăng nhập
5. Hệ thống chuyển hướng người dùng vào giao diện chính ứng dụng

**Ngoại lệ:**
- Email hoặc mật khẩu không chính xác: Hệ thống hiện thông báo "Email hoặc mật khẩu không chính xác"
- Tài khoản bị khóa: Hệ thống hiển thị thông báo "Tài khoản đã bị khóa"

---

## UC xem danh sách tin tức

| Thông tin | Chi tiết |
|----------|----------|
| **Use case** | Xem danh sách tin tức |
| **Actor** | Người dùng |
| **Tiền điều kiện** | Người dùng truy cập vào ứng dụng |
| **Hậu điều kiện** | Người dùng xem được danh sách tin tức với phân trang |

**Kịch bản chính:**
1. Người dùng truy cập trang chủ hoặc trang tin tức
2. Hệ thống lấy danh sách tin tức từ cơ sở dữ liệu
3. Hệ thống hiển thị danh sách tin tức với tiêu đề, hình ảnh và tóm tắt
4. Người dùng có thể điều hướng qua các trang phân trang
5. Người dùng có thể sử dụng bộ lọc theo nguồn, ngày, danh mục

**Ngoại lệ:**
- Không có tin tức: Hệ thống hiển thị thông báo "Không có tin tức nào"
- Lỗi kết nối database: Hệ thống hiển thị thông báo lỗi hệ thống

---

## UC đọc chi tiết tin tức

| Thông tin | Chi tiết |
|----------|----------|
| **Use case** | Đọc chi tiết tin tức |
| **Actor** | Người dùng |
| **Tiền điều kiện** | Người dùng đã xem danh sách tin tức |
| **Hậu điều kiện** | Người dùng đọc được nội dung đầy đủ và được ghi nhận vào lịch sử |

**Kịch bản chính:**
1. Người dùng click vào tiêu đề hoặc hình ảnh của bài viết trong danh sách
2. Hệ thống hiển thị modal hoặc trang chi tiết với nội dung đầy đủ
3. Người dùng đọc nội dung bài viết
4. Hệ thống tự động ghi nhận bài viết vào lịch sử đọc
5. Người dùng có thể lưu bài viết hoặc đóng modal

**Ngoại lệ:**
- Bài viết không tồn tại: Hệ thống hiển thị thông báo "Bài viết không tồn tại"
- Lỗi tải nội dung: Hệ thống hiển thị thông báo lỗi

---

## UC lưu trữ tin tức

| Thông tin | Chi tiết |
|----------|----------|
| **Use case** | Lưu trữ tin tức |
| **Actor** | Người dùng |
| **Tiền điều kiện** | Người dùng đã đăng nhập và đang đọc tin tức |
| **Hậu điều kiện** | Bài viết được lưu vào danh sách đã lưu của người dùng |

**Kịch bản chính:**
1. Người dùng click nút "Lưu" trên bài viết
2. Hệ thống kiểm tra trạng thái hiện tại của bài viết
3. Nếu chưa lưu: Hệ thống thêm bài viết vào danh sách đã lưu
4. Nếu đã lưu: Hệ thống xóa bài viết khỏi danh sách đã lưu
5. Hệ thống cập nhật giao diện và hiển thị trạng thái mới

**Ngoại lệ:**
- Chưa đăng nhập: Hệ thống chuyển hướng đến trang đăng nhập
- Lỗi lưu trữ: Hệ thống hiển thị thông báo lỗi

---

## UC xem tin tức đã lưu

| Thông tin | Chi tiết |
|----------|----------|
| **Use case** | Xem tin tức đã lưu |
| **Actor** | Người dùng |
| **Tiền điều kiện** | Người dùng đã đăng nhập |
| **Hậu điều kiện** | Người dùng xem được danh sách bài viết đã lưu |

**Kịch bản chính:**
1. Người dùng truy cập trang "Đã lưu"
2. Hệ thống lấy danh sách bài viết đã lưu của người dùng
3. Hệ thống hiển thị danh sách với tùy chọn tìm kiếm và lọc
4. Người dùng có thể xóa bài viết khỏi danh sách đã lưu
5. Người dùng có thể click vào bài viết để đọc chi tiết

**Ngoại lệ:**
- Chưa đăng nhập: Hệ thống chuyển hướng đến trang đăng nhập
- Không có bài viết đã lưu: Hệ thống hiển thị thông báo "Chưa có bài viết nào được lưu"

---

## UC xem lịch sử đọc

| Thông tin | Chi tiết |
|----------|----------|
| **Use case** | Xem lịch sử đọc |
| **Actor** | Người dùng |
| **Tiền điều kiện** | Người dùng đã đăng nhập |
| **Hậu điều kiện** | Người dùng xem được lịch sử đọc tin tức |

**Kịch bản chính:**
1. Người dùng truy cập trang "Lịch sử"
2. Hệ thống lấy danh sách bài viết đã đọc theo thời gian giảm dần
3. Hệ thống hiển thị danh sách với ngày giờ đọc
4. Người dùng có thể tìm kiếm trong lịch sử
5. Người dùng có thể xóa mục khỏi lịch sử

**Ngoại lệ:**
- Chưa đăng nhập: Hệ thống chuyển hướng đến trang đăng nhập
- Không có lịch sử: Hệ thống hiển thị thông báo "Chưa có lịch sử đọc"

---

## UC tìm kiếm tin tức

| Thông tin | Chi tiết |
|----------|----------|
| **Use case** | Tìm kiếm tin tức |
| **Actor** | Người dùng |
| **Tiền điều kiện** | Người dùng truy cập vào ứng dụng |
| **Hậu điều kiện** | Người dùng tìm thấy kết quả phù hợp với từ khóa |

**Kịch bản chính:**
1. Người dùng nhập từ khóa vào thanh tìm kiếm
2. Người dùng có thể chọn bộ lọc theo danh mục, nguồn, ngày
3. Người dùng click nút tìm kiếm
4. Hệ thống tìm kiếm trong tiêu đề, tóm tắt và nội dung
5. Hệ thống hiển thị kết quả với highlighting từ khóa

**Ngoại lệ:**
- Không tìm thấy kết quả: Hệ thống hiển thị "Không tìm thấy kết quả phù hợp"
- Từ khóa quá ngắn: Hệ thống hiển thị "Vui lòng nhập ít nhất 3 ký tự"

---

## UC nhận gợi ý tin tức cá nhân hóa

| Thông tin | Chi tiết |
|----------|----------|
| **Use case** | Nhận gợi ý tin tức cá nhân hóa |
| **Actor** | Người dùng |
| **Tiền điều kiện** | Người dùng đã có lịch sử đọc |
| **Hậu điều kiện** | Người dùng nhận được gợi ý tin tức phù hợp |

**Kịch bản chính:**
1. Hệ thống phân tích lịch sử đọc và hành vi của người dùng
2. Hệ thống gửi yêu cầu đến recommendation service
3. Recommendation service tính toán độ tương đồng
4. Hệ thống hiển thị danh sách tin tức gợi ý
5. Người dùng có thể tương tác với tin tức gợi ý

**Ngoại lệ:**
- Không đủ dữ liệu lịch sử: Hệ thống hiển thị tin tức phổ biến
- Lỗi recommendation service: Hệ thống hiển thị tin tức ngẫu nhiên

---

## UC xem tóm tắt tin tức

| Thông tin | Chi tiết |
|----------|----------|
| **Use case** | Xem tóm tắt tin tức |
| **Actor** | Người dùng |
| **Tiền điều kiện** | Người dùng đang đọc tin tức |
| **Hậu điều kiện** | Người dùng xem được tóm tắt nội dung |

**Kịch bản chính:**
1. Người dùng chọn tùy chọn "Xem tóm tắt" trên bài viết
2. Hệ thống gửi yêu cầu đến summary service
3. Summary service tạo tóm tắt nội dung bài viết
4. Hệ thống hiển thị tóm tắt trong modal hoặc tooltip
5. Người dùng có thể đóng tóm tắt hoặc đọc đầy đủ

**Ngoại lệ:**
- Lỗi summary service: Hệ thống hiển thị thông báo "Không thể tạo tóm tắt"
- Nội dung quá ngắn: Hệ thống hiển thị nội dung gốc

---

## UC quản lý nguồn RSS

| Thông tin | Chi tiết |
|----------|----------|
| **Use case** | Quản lý nguồn RSS |
| **Actor** | Quản trị viên |
| **Tiền điều kiện** | Quản trị viên đã đăng nhập với quyền admin |
| **Hậu điều kiện** | Nguồn RSS được cập nhật thành công |

**Kịch bản chính:**
1. Quản trị viên truy cập trang quản lý sources
2. Quản trị viên chọn thao tác: thêm, sửa hoặc xóa nguồn RSS
3. Quản trị viên nhập thông tin nguồn RSS (tên, URL, danh mục)
4. Quản trị viên lưu thay đổi
5. Hệ thống cập nhật database và kích hoạt crawler

**Ngoại lệ:**
- Không có quyền admin: Hệ thống từ chối truy cập
- URL không hợp lệ: Hệ thống hiển thị "URL RSS không hợp lệ"
- Lỗi lưu trữ: Hệ thống hiển thị thông báo lỗi

---

## UC quản lý tác vụ crawler

| Thông tin | Chi tiết |
|----------|----------|
| **Use case** | Quản lý tác vụ crawler |
| **Actor** | Quản trị viên |
| **Tiền điều kiện** | Quản trị viên đã đăng nhập với quyền admin |
| **Hậu điều kiện** | Tác vụ crawler được quản lý thành công |

**Kịch bản chính:**
1. Quản trị viên truy cập trang quản lý crawler
2. Hệ thống hiển thị trạng thái các tác vụ crawler
3. Quản trị viên chọn tác vụ và hành động (bắt đầu, dừng, restart)
4. Hệ thống thực hiện hành động tương ứng
5. Hệ thống cập nhật trạng thái và logs

**Ngoại lệ:**
- Không có quyền admin: Hệ thống từ chối truy cập
- Tác vụ đang chạy: Hệ thống hiển thị "Tác vụ đang thực hiện"
- Lỗi kết nối: Hệ thống hiển thị lỗi hệ thống

---

## UC quản lý người dùng

| Thông tin | Chi tiết |
|----------|----------|
| **Use case** | Quản lý người dùng |
| **Actor** | Quản trị viên |
| **Tiền điều kiện** | Quản trị viên đã đăng nhập với quyền admin |
| **Hậu điều kiện** | Tài khoản người dùng được quản lý thành công |

**Kịch bản chính:**
1. Quản trị viên truy cập trang quản lý người dùng
2. Hệ thống hiển thị danh sách người dùng với thông tin chi tiết
3. Quản trị viên chọn người dùng và hành động (xem thông tin, khóa/mở khóa)
4. Quản trị viên xác nhận hành động
5. Hệ thống cập nhật trạng thái tài khoản

**Ngoại lệ:**
- Không có quyền admin: Hệ thống từ chối truy cập
- Người dùng không tồn tại: Hệ thống hiển thị "Người dùng không tồn tại"
- Lỗi cập nhật: Hệ thống hiển thị thông báo lỗi