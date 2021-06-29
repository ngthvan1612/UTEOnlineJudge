# UTE ONLINE JUDGE
Trình chấm bài online - ute
# Setup

## 1 Tạo virtualenv
```bash
virtualenv env-ubuntu # Nếu có rồi thì bỏ qua
source env-ubuntu/bin/activate # Lệnh này phải có
```

## 2 Cài đặt requirements (cho python)
```bash
pip install -r requirements.txt # Cập nhật, cài đặt các thư viện cho python
```

## 3 Chạy project
```bash
cd uteoj
make static #lệnh này để cập nhật các file CSS, JS, ... vào static của web
make migrate # Lệnh này cần thiết khi bên backend vừa có thay đổi models hoặc mới clone git về, các trường hợp còn lại có thể không dùng cũng được.
make run # chạy, vào trình duyệt truy cập vào địa chỉ 127.0.0.1:8000
```

## 4 Note
Hiện tại chỉ truy cập vào 127.0.0.1:8000/admin