# Upgrade database                          (DONE)
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

# Fix                                       (DONE)
## Fix các pagination                       (DONE)

Thiết kế lại pagination như sau

> {{page_obj.paginator.num_pages}} là số lượng trang đang phân

Nếu trang hiện tại là k, và tổng số trang là n
- In ra như sau: 1 ... k-1 k k+1...n
- Ví dụ:
-- 1 ... 8 9 10 ... 103 //đang ở trang 9
-- 1 2 ... 103 //đang ở trang 1
-- 1 2 3 ...103 //đang ở trang 2

## Trang listtestcase                       (DONE)
- Làm mỗi hàng nhỏ lại (height)
- Hiện tại backend không đưa ra categories nữa (tức là không show ra nhưng filter không đổi) - bỏ div categories trong table là được.

## Trang problem details                    (DONE)
- Edit lại toàn bộ textarea - test lỗi. Xóa bỏ khoảng trắng thừa ví dụ
```html
<tag> {{variable}} </tag>
thành
<tag>{{variable}}</tag>
```

## Trang list testcase                      (DONE)
- Thêm cột is sample để biết test có dùng làm mẫu hay không (boolean - giống is_admin)
- 
## Trang edit testcase                      (DONE)
- Thêm trường is_sample (type=checkbox, name="is_sample") để gửi thông tin về server

## Trang settings                           (DONE)
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

# Upgrade
## Fix lại models                           (DONE)
```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```
## Cài đặt máy chủ redis (dùng để chạy nền) (DONE)
```bash
sudo apt-get install redis
```
## Chạy nền celery (trên terminal khác)     (DONE)
```
celery -A uteoj worker -Ofair
```
> Note: Số lượng luồng celery chạy = số lượng bài chấm cùng một lúc = Số cores của máy tính hiện t
> Nên chỉ định số luồng chạy bằng cách thêm -c=<số luồng chạy> vào sau lệnh trên để tiện quan sát

## Chỉnh sửa:

### List problem (trong admin):

Chỉnh lại problemlikename thành name

## Thêm trang phía user:

### Danh sách bài tập

url:/problems
template:user-template/problem/listproblem.html

#### Backend:

Truyền xuống:

- page_obj: danh sách bài tập, mỗi phần tử gồm giá trị sau:
-- shortname: tên ngắn của bài, (này dùng để href)
-- fullname: tên đầy đủ của bài
-- difficult: độ khó
-- problem.categories.all: dạng bài

- Dùng phân trang như trong admin

- list_categories: danh sách tên dạng bài (như trong admin)

#### Frontend:

Gửi lên (nếu người dùng cần filter, method='GET', làm giống admin):
- category: dạng bài
- problem_type: acm hay oi
- name: tên bài (tìm những bài chứa chuỗi name)
- orderby: hiện tại chỉ dùng được difficult
-- orderby=difficult là xếp tăng,
-- orderby=-difficult là xếp giảm

### Trạng thái

url=/status
template: user-template/status.html

#### Backend

Gửi xuống client
- submissions: danh sách trạng thái hiện tại, mỗi trạng thái gồm
-- id: chỉ số bài nộp
-- username: tên người dùng,
-- problem.shortname: tên ngắn của bài
-- problem.fullname: tên đầy đủ của bài
-- submission_date: thời điểm gửi lên,
-- judge_date: thời điểm chấm,
-- language: tên ngôn ngữ,
-- status: trạng thái,
-- result: kết quả,
-- testid: đang chạy test nào

#### Frontend xử lý gần xuống như này

https://ideone.com/q3aFGp

### Submit bài

url: /problem/{{shortname}}/submit
template: user-template/problem/submit.html

#### Backend

Gửi xuống client:
- languages: danh sách ngôn ngữ, mỗi thành phần gồm:
-- value: giá trị để gửi lên server
-- display: tên ngôn ngữ


#### Frontend

> Phần langauges dùng select, option

Gửi về server (method=post, url=/):

- language: tên value nảy backend gửi xuống và người dùng chọn
- source: source code
