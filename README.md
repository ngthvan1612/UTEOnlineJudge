## Filter
### 1. Yêu cầu chung
- Khi có tham số GET sẵn thì tự động update vào form (khi vừa mở web)
 > Khi truy cập vào http://127.0.0.1:8000/admin/problems/?category=dp,greedy,flows&problem_type=Oi tự động form điền vào categories=dp,greedy,flows và problem_type là OI
- Khi gửi filter lên server phải gửi luôn cả thông tin đã gửi lần trước (trừ tham số page)
> Khi truy cập vào http://127.0.0.1:8000/admin/problems/?page=3&category=dp,greedy,flows&problem_type=Oi thì nếu filter lần nữa, ví dụ chọn lại problem_type=ACM thì phải gửi lại category=dp,greedy,flows (page bỏ)
### 2. Dữ liệu gửi lên SERVER
- problem_type: ACM hoặc OI (in hoa thường đều được)
- category: một dãy các category, nếu có nhiều thì nối nhau bởi dấu chấm phẩy (comma)  - Không cần combine giống CF
- problemnamelike: tên của bài cần search
- orderby: sắp xếp theo
1. orderby=difficult: độ khó tăng dần
2. orderby=-difficult: độ khó giảm dần
- page: số trang hiện tại
### 3. Dữ liệu từ SERVER xuống
- list_categories: danh sách categories
- page_obj: danh sách bài tập (thay thế cho list_problems cũ)
- page_obj.number: thứ tự trang hiện tại (mặc định 1)
- page_obj.paginator.num_pages: tổng số trang
> Thứ tự được đánh số từ 1 (1-indexed) và 1<=page_obj.number<=page_obj.paginator.num_pages (*)

> Dưới frontend xử lý khúc này bằng javascript (tạo link + function), mỗi lần chuyển sang trang mới (trang cũ +-1 & check khoảng (*)) phải giữ lại filter cũ (category, problemnamelike, problem_type,...) (1)
## Base (fix)
- Button logout nhỏ lại (kể cả khi co menu lại), đúng mẫu menu chứa Manage 
Problem, Manage Users
## Dashboard (fix)
- Bài mới chỉ cần hiện lên (shortname, fullname, author) + làm gọn gọn.
## List problem (fix)
- Tính cả toàn base.html, sửa lại tránh tràn dữ liệu xuống chân web, set height thành auto.
- Khi nhấp vào tiêu đề difficult (table) thì tự động sort lại, nếu đang tăng thì giảm (check giống phần (1), mặc định lần đầu là tăng dần.
- Chỉ cần đưa problemnamelike lên server, không xử lý dưới client, mỗi trang có khoảng 10 bài nên không cần thiết.
## List category (fix)
- Thông báo người dùng khi lỗi từ server xuống (bất kì lỗi gì).
- Edit, delete tag chứ không phải edit, delete description.
- Delete description chỉ hiện nội dung xác nhận, không hiện ra bất kì điều gì 
khác.
- Dùng icon thay cho chữ edit, delete.
- Xóa "Update 1 hour ago", không cần thiết vì tag dạng bài chỉ quan tâm đến dạng tên gì, admin cũng không quan tâm đến tag đó update khi nào.
