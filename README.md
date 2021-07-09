# UTE ONLINE JUDGE
Trình chấm bài online - ute
# Các account hiện tại
1. user: admin, password: 1234567890 (admin)
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

# 2 Frontend & Backend (Address, variable, ...)

## 2.1 Categories
> Trước khi gửi mọi POST, yêu cầu phải có hằng CSRF_TOKEN trước khi import js
```html
<!-- just exmplate -->
<script>
   var CSRF_TOKEN = '{{ csrf_token }}';
</script>
...
<script type="text/javascript" src="{% static 'admin-static/js/category.js' %}"></script>
```
### 2.1.1 Add
Dùng ajax gửi lên server (method=POST, url=/admin/categories/), thông tin data như sau:
```js
data: {
            method : 'add', //method là add
            name : 'fftz', //cái tên mới
            description : '12.fft', //thông tin phụ
            csrfmiddlewaretoken: CSRF_TOKEN, ///phải có (ở trên)
},
```
Khi gửi thành công
```js
$.ajax({
        url: '/admin/categories/',
        type: 'POST',
        data: {
              .......
        },
        success: function(data) {
            if (data.status=='success') {
                ///xử lý message khi thành công - có thể alert ra, có thể cập nhật vào label trong modal (đổi thành màu xanh)
                console.log("SUCCESS: " + data.message);
                reloadCurrentSource();
            }
            else {
                ///xử lý message khi lỗi (như trên)
                console.log("ERROR: " + data.message);
            }
        }
    });
```
>> Note: tên không được đặt là 'All'

### 2.1.2 Edit
Gửi lên server (method=POST, url=/admin/categories/), thông tin data như sau:
- method: 'edit'
- old_name: //tên cũ
- new_name: //tên mới
- description: //thông tin phụ mới
> Sau khi thành công, xử lý như Add
### 2.1.3 Delete
Gửi lên server (method=POST, url=/admin/categories/), thông tin data như sau:
- method: 'delete'
- name: //tên của categories
> Note: Xác nhận trước khi xóa