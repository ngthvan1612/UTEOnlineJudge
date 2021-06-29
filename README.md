# UTE ONLINE JUDGE
Trình chấm bài online - ute
# Các account hiện tại
1. user: admin, password: admin123 (admin)
2. user: abcdef, password: 12345678 (thường)
3. user: xyz123, password: 1234567890 (thường)
4. user: hello, password: xinchao123 (thường)

# 1 Setup

## 1.1 Tạo virtualenv
```bash
virtualenv env-ubuntu # Nếu có rồi thì bỏ qua
source env-ubuntu/bin/activate # Lệnh này phải có
```

## 1.2 Cài đặt requirements (cho python)
```bash
pip install -r requirements.txt # Cập nhật, cài đặt các thư viện cho python
```

## 1.3 Chạy project
```bash
cd uteoj
make static #lệnh này để cập nhật các file CSS, JS, ... vào static của web
make migrate # Lệnh này cần thiết khi bên backend vừa có thay đổi models hoặc mới clone git về, các trường hợp còn lại có thể không dùng cũng được.
make run # chạy, vào trình duyệt truy cập vào địa chỉ 127.0.0.1:8000
```

## 1.4 Note
Hiện tại chỉ truy cập vào 127.0.0.1:8000/admin

# 2 Frontend & Backend (Address, variable, ...)

## 2.1  Trang đăng nhập: /login
1. File
* ***Template: /frontend/auth-template/login.html***
2. Từ backend gửi qua frontend (nếu đã vào trang login và đăng nhập lỗi mới gửi qua):
* login_error: lỗi đăng nhập
3. Từ frontend gửi qua backend:
* ***cstf_token (thêm dòng {% csrf_token %} vào chung với các thẻ input)***
* username: tên người dùng
* password: mật khẩu
```html
<form action="/login/" method="POST">
    {% csrf_token %}
    {% if login_error %}
        <script type="text/javascript">
            alert('{{login_error}}');
        </script>
    {% endif %}
    <label>User name: </label>
    <input type="text" name="username">
    <label>Password: </label>
    <input type="password" name="password">
    <input type="submit" text="Login">
</form>
```
> Nếu đăng nhập thành công, tự động nhảy qua trang /who để test xem đang đăng nhập với tên gì
## 2.2 Trang đăng ký: /signup
1. File
* ***Template: /frontend/auth-template/signup.html***
2. Từ backend gửi qua frontend:
* signup_error: Lỗi khi đăng ký (màu đỏ)
* signup_success: Khi đăng ký thành công (màu xanh)
* Note: 2 biến này không thể xuất hiện đồng thời, lỗi thì không thành công, thành công thì không lỗi.
3. Từ frontend gửi qua backend
* cstf_token
* username: tên người dùng
* email: email đăng ký
* password1: mật khẩu 1
* password1: mật khẩu 2
```html
{% if signup_error %}
        <label style="color:red;">{{signup_error}}</label>
        </br>
    {% endif %}
{% if signup_success %}
        <label style="color:green;">{{signup_success}}</label>
        </br>
{%endif %}
```