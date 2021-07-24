# Upgrade database
> Có thay đổi toàn bộ cơ sở dữ liệu nên cần drop toàn bộ database và create lại
```sql
drop database <ten>
create database <ten>
```
Sau khi tạo lại thực hiện các lệnh sau:
```bash
python manage.py makemigrations
python manage.py migrate # tạo lại các bảng
python manage.py initadmin # tạo 2 người dùng admin và root
# mật khẩu của admin là 1234567890
# mật khẩu của root là 92ad5d248d6da148092419b836ce16c1
```

# Fix

## Fix các pagination

Thiết kế lại pagination như sau

> {{page_obj.paginator.num_pages}} là số lượng trang đang phân

Nếu trang hiện tại là k, và tổng số trang là n
- In ra như sau: 1 ... k-1 k k+1...n
- Ví dụ:
-- 1 ... 8 9 10 ... 103 //đang ở trang 9
-- 1 2 ... 103 //đang ở trang 1
-- 1 2 3 ...103 //đang ở trang 2

## Trang listtestcase
- Làm mỗi hàng nhỏ lại (height)
- Hiện tại backend không đưa ra categories nữa (tức là không show ra nhưng filter không đổi) - bỏ div categories trong table là được.

## Trang problem details
- Edit lại toàn bộ textarea - test lỗi. Xóa bỏ khoảng trắng thừa ví dụ
```html
<tag> {{variable}} </tag>
thành
<tag>{{variable}}</tag>
```

## Trang list testcase
- Thêm cột is sample để biết test có dùng làm mẫu hay không (boolean - giống is_admin)
- 
## Trang edit testcase
- Thêm trường is_sample (type=checkbox, name="is_sample") để gửi thông tin về server

## Trang settings
### a) Backend
Gửi xuống client:
- input_filename: tên file input
- output_filename: tên file output
- use_stdin: có dùng stdin hay không (boolean) - dùng giống is_admin, is_active, ...
- use_stdout: có dùng stdout hay không (boolean)
- time_limit: time limit của bài
- memory_limit: memory limit của bàii
- submission_visible_mode: các chế độ xem bài giải (số nguyên)
- submission_visible_mode_choices: list các chế độ xem bài (giống tùy chọn khi gửi filezip lên - themis, ...), mỗi cái gồm:
-- value:
-- display:
### b) Frontend
- mẫu submission_visible_mode_choices
```html
<select  name="submission_visible_mode">

{%for  x  in  submission_visible_mode_choices%}

<option  value="{{x.value}}"  {%if  submission_visible_mode  ==  x.value%}selected{%endif%}>{{x.display}}</option>

{%endfor%}

</select>
```
- Gửi lên server (method=post, url="")
-- input_filename
-- output_filename
-- use_stdin (cách gửi lên giống is_admin, is_active, ...)
-- use_stdout (giống use_stdin)
-- submission_visible_mode
-- time_limit
-- memory_limit
|