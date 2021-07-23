> Note: Có thay đổi models, thực hiện makemigrations & migrate lại

> Nếu chạy lỗi có thể cần phải drop cả database và tạo lại 

# Fix & update  
## 1. Trang signup:                             (DONE)
- Link trỏ về /signup/ không phải /signup   (DONE)
- Thêm phần xử lý message

## 2. Trang login:                              (DONE)
- Thêm phần xử lý message

## 3. Trang list testcases                      (DONE)
- input{{x.id}} không phải pk
- output tương tự
- Cho link đi trang trang khác
- chỉnh lại menu cho giống mấy trang kia

## 4. Trang problem details                     (DONE)
- Lỗi khi editmarkdown: Khi nhấn nút Toggle Full Screen ở trên thanh công cụ thì bị tràn phía bên trái - không thấy gì hết

## 5. Link ở các trang editproblem:             (DONE)
- Trỏ về settings không phải setting

## 6. Điều chỉnh lại thư mục frontend:          (DONE)
- Trang details: ../admin-template/problem/edit/details.html
- Trang problemsetter: ../../problemsetter.html
- Trang list testcase: ../../listtestcase.html
- Trang edit testcase: ../../editestcase.html
- Trang languages: ../../languages.html
- Trang settings: ../../settings.html
- Trang custom checker: ../../checker.html

## 7. Thêm trang checker                        (DONE)
### a) Backend:
Gửi xuống client:
- use_checker: Có sử dụng checker ngoài hay không (dưới client dùng giống is_admin, is_active)
- checker_source: Mã nguồn của checker (c++)
### b) Frontend:
Gửi lên lại server (method=post, url=""):
- use_checker: (giống is_admin, nếu có tick thì gửi, không thì thôi)
- checker_source

