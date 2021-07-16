# Fix & update
## Quạn trọng
# 1. Đổi dbms
Vào file dbutils.py cấu hình lại database với các hằng sau:
> Hiện tại sẽ dùng mysql
DATABASE_NAME = 'tên csdl'
DATABASE_USER = 'tên người dùng'
DATABASE_PASSWORD = 'mật khẩu'
DATABASE_HOST = 'host của mysql, localhost hoặc 127.0.0.1'
DATABASE_PORT = 'cổng mysql, mặc định 3306'

> Lưu ý trong quá trình comit, push sẽ không có file dbutils.py tham gia vào, vì đã ignore rồi

Sau khi đổi, làm 3 việc
1. Update lại thư viên
```bash
pip install -r requirements.txt # ở trong thư mục gốc
```
2. Update lại csdl
```bash
python manage.py makemigrations
python manage.py migrate
```
3. Tạo người dùng admin
```bash
python manage.py createsuperuser
# bắt đầu nhập vào username
admin
# email bỏ cũng được
qwert@gmail.com
# password, mật khẩu khác cũng được
1234567890
# nhập lại
1234567890
#django có hỏi gì thì chọn y ---> OK
```
# nếu có lỗi xảy ra, xem lại cấu hình dbutils.py
```

## 2. Update toàn bộ thông báo lỗi
1. Tạo trong thư mục admin-template/\_layout/ file **errort\_handle.html** (giống nav.html, ...) gồm nội dung sau (mẫu):
```html
<div class="row">
    <div class="col-12">
        {% if messages %}
            <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                <symbol id="check-circle-fill" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
                </symbol>
                <symbol id="info-fill" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/>
                </symbol>
                <symbol id="exclamation-triangle-fill" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
                </symbol>
            </svg>
            <div class="message">
                {% for message in messages %}
                    <div>
                        {% if message.level == DEFAULT_MESSAGE_LEVELS.ERROR %}
                            <div class="alert alert-danger fade show">
                                <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg>
                                {{message}}
                                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                </button>
                            </div>
                        {% elif message.level == DEFAULT_MESSAGE_LEVELS.WARNING %}
                            <div class="alert alert-warning fade show" role="alert">
                                <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Warning:"><use xlink:href="#exclamation-triangle-fill"/></svg>
                                {{message}}
                                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                </button>
                            </div>
                        {% elif message.level == DEFAULT_MESSAGE_LEVELS.INFO %}
                            <div class="alert alert-primary fade show" role="alert">
                                <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Info:"><use xlink:href="#info-fill"/></svg>
                                {{message}}
                                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                </button>
                            </div>
                        {% else %}
                            <div class="alert alert-success" role="alert">
                                <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:"><use xlink:href="#check-circle-fill"/></svg>
                                {{message}}
                                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                    <span style="color:black;">&times;</span>
                                </button>
                            </div>
                        {% endif %}
                    </div>
                {% endfor %}
            </div>
        {% endif %}
    </div>
</div>
```
> Kết quả
![image](https://i.ibb.co/93gFrH5/u1.png)

![image](https://i.ibb.co/pbPnqnV/u2.png)
2. Chỉnh sửa lại login.html bằng cách thay các {% login_error %} thành dòng sau:
```html
{% include 'admin-template/_layout/error_handle.html' %}
```
> Làm tương tự với **signup.html**
> Còn các trang khác, trước khi bắt đầu code nội dung thì để cái include đó ở trên đầu
```html
	<!-- Content Header (Page header) -->
	<div class="content-header">
		<div class="container-fluid">
			<div class="row">
				<div class="col-12 mb-3">
					{% include 'admin-template/_layout/error_handle.html' %}
				</div>
				<div class="col-12 mb-3">...
```
## 3. Các page mới
### 3.1.Thêm menu ngôn ngữ code (language) giống category:
#### 3.1.1 Tạo ngôn ngữ mới:

**a) Frontend**
- Template: admin-template/language/createNewLanguage.html
- Address: /admin/language/create/
- Gửi về backend (method=post, url="", nhảy vào trang này luôn, không dùng ajax - nếu dùng thì reload lại trang này) (_url="" tức là action="", gửi tại chỗ_) gồm:
-- csrf_token
-- lang_name: tên của ngôn ngữ mới (C++ 14, Java 1.8, ..) - không được trống
-- lang_ext: đuôi file của ngôn ngữ đó (.cpp, .py, .java, ... bla bla) - không được trống
-- lang_description: miêu, tả, thông tin, ... của ngôn ngữ đó (giống bên category) - không được trống
-- lang_compile_command: lệnh biên dịch - có thể trống (ex: python khỏi biên dịch)
-- lang_run_command: lệnh chạy - không được trống (biên dịch hay không gì cũng phải chạy)

#### 3.1.2 Chỉnh sửa ngôn ngữ:
**a)Frontend**
- Template: admin-template/language/editLanguage.html, thiết kế khá giống
- Address: /admin/language/edit/{{lang\_id}}/ (lang\_id xem ở mục 3.1.3)
- createLanguage, nhưng sẽ có 2 nút "save" và "delete"
- Đối với save, nội dung gửi về backend giống như createLanguage
- Đối với delete, chỉ cần dùng form gửi csrf\_token vào địa chỉ này /admin/language/delete/{{lang_id}}/ sau đó chuyển hướng vào danh sách ngôn ngữ
-- Ví dụ (có thể hide form rồi sau đó nếu click nút delete thì document.getElementById('#delete-lang').submit()) - form không lồng nhau được
```html
<form hidden id="delete-lang" action="/admin/language/delete/{{lang_id}}/" method="post">
    {% csrf_token %}
    <input type="submit">
</form>
```
**b)Backend**
- Gửi về frontend (giống tên khi frontend gửi về backend):
-- lang_id: PK của ngôn ngữ (PK, mục đích để delete), ***lang_id khác hoàn toàn id***
-- lang_name: tên ngôn ngữ
-- lang_ext: đuôi file
-- lang_description: miêu tả cái ngôn ngữ
-- lang\_compile\_command: lệnh biên dịch
-- lang\_run\_command: lệnh chạy

#### 3.1.3 Danh sách ngôn ngữ
**a)Frontend**
- Template: admin-template/language/listLanguage.html
- Address: /admin/language/
- Thiết kế show ra từng ngôn ngữ theo từng hàng, cuối hàng có nút edit/xóa (không được thêm nút delete vô đây :))), phải để admin vào chỉnh sửa mới delete được, vì có khả năng ấn nhầm delete thì xong - cái này quan trong hợn categories nhiều), tức là chuyển vào trang /admin/language/edit/{{lang_id}}/
**b)Backend**
- Gửi về frontend list_language: một mảng ngôn ngữ, mà mỗi phần tử đều có dạng sau:
-- id: số thứ tự, ***lang_id khác hoàn toàn id***
-- lang_name: tên ngôn ngữ
-- lang_ext: đuôi file
-- lang_description: miêu tả cái ngôn ngữ
-- lang\_compile\_command: lệnh biên dịch
-- lang\_run\_command: lệnh chạy
