# 1. API
## Sinh random user
- http://127.0.0.1:8000/random/user?startwith=<tên bắt đầu>&count=<số lượng>&isadmin=<True nếu là admin>   (pass mặc định là 12345678)
- Tạo ra **count** user với tên bắt đầ với **startwith** có pass là **12345678**, first name là **startwith** còn last name là số thứ tự (tính từ 0)
> Ex http://127.0.0.1:8000/random/user?startwith=abc&count=4&isadmin=True
Tạo 10 user lần lượt là abc0, abc1, abc2, abc3 với mật khẩu là 12345678, là mặc định là quyền admin
# 2. Page
## 1. List admin
Address: /admin/users/administrators/
### a) Backend:
Gửi xuống client:
- page_obj: danh sách các user, mỗi user gồm: id (số thứ tự), first_name (tên), last_name (họ), date_joined (thời điểm signup), is_active (còn hoạt động không hay bị admin block cmnr)
- page_obj giống bên listproblem, có phân trang
### b) Frontend:
Gửi lên server (mục đích chỉ để filter):
- rows_per_page: số dòng trong một trang (không gửi phía backend mặc định là 10)
- search: tên của user (giống filter problem name)
- page: thứ tự trang hiện tại (giống list problem)
Yêu cầu cuối mỗi hàng có link edit user (hoặc link ngay user) có trỏ đến ***/admin/users/edit/{{u.username}}*** (u là tên biến chạy)
## 2. List contestants
Address: /admin/users/contestants/
- Làm giống y như list admin
## 3. Tạo user mới
Address: /admin/users/create/
### a) Frontend:
Gửi lên server: **(method=post, url="")**
- first_name: Họ
- last_name: Tên
- user_name: Tên người dùng
- passowrd: Mật khẩu
- email: email
- make_user_admin: Có tạo user này thành admin không, chỉ cần có tên biến gửi lên server là coi như có (<input ... type="checkbox" ... name="make_user_admin">)
- job: công việc
Yêu cầu: xử lý luôn messages (giống như mọi trang khác, include 1 dòng error_handle ở đầu)
## 4. Chỉnh sửa user
Address: /admin/users/edit/{user name nao do}/
### a) Backend:
Gửi xuống client:
- username: tên người dùng
- first_name
- last_name
- email
- is_admin: có phải là admin hay không
- is_active: có còn hoạt động không
- date_joined: ngày tham signup
- job: công việc
- avatar: đường link tới avatar (nếu có avt thì server mới gửi biến này xuống, ngược lại thì không có biến này)
phần is_admin, is_active, xử lý dưới client: (dùng checkbox để tiện gửi lên lại)
```html
<input class="form-check-input" type="checkbox" {%if is_admin%}checked{%endif%} name="is_admin"/>
```
(is_active tương tự)
### b) Frontend:
Gửi lên server: **(method=post,url="",enctype="multipart/form-data")**

> enctype để gửi hình lên

> Yêu cầu dưới client block **username** và **date_joined** lại vì 2 biến này không thay đổi được)
- first_name
- last_name
- user_job
- email
- is_admin (làm giống như make_user_admin, dùng checkbox)
- is_active (làm giống is_admin)
- **user_avatar** file ảnh, dùng <input type="file"..>, mỗi khi up ảnh lên (vừa chọn xong) thì phải show ra cho người dùng thấy trước khi up lên server
