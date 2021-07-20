## Note: Không commit file dbutil.py
> Note: Các Address dưới đây đều không có dấu / ở phía sau link để tiện cho việc chuyển qua lại giữa các trang, ví dụ đang ở trang details muốn qua testcases của cùng một bài thì chỉ cần gắn thẻ a với href="testcases" là đủ
# Edit problem:
## 1. Details
Template: ***admin-template/problem/editProblemDetails.html***

Address: ***/admin/problems/edit/{{shortname}}/details***
### a) Backend:
Gửi xuống client:
- problem.shortname: Tên ngắn của bài
- problem.fullname: Tên đầy đủ của bài
- problem.difficult: Độ khó
- problem.categories: Danh sách tên của các categories của bài
- problem.points_per_test: Điểm của mỗi test,
- problem.statement: Đề bài (viết bằng markdown)
- problem.input_statement: Phần input của bài (markdown)
- problem.constraints_statement: Phần ràng buộc của bài (markdown)
- problem.output_statement: Phần output của bài (markdown)
> 
- list_categories: Danh sách toàn bộ categories
### b) Frontend:
#### + Thiết kế categories dùng check box giống như này
```html
{%for cate in list_categories %}
        <div class="form-check">
            <input type="checkbox" 
                   value="{{cate}}" 
                   name="list_categories[]"
{% if cate in problem.categories%}checked{%endif%}>
            <label class="form-check-label">{{cate}}</label>
        </div>
{%endfor%}
```
#### + Gửi lên server: (method=post, url="")
- Toàn bộ những gì server gửi xuống (giống tên)
- Với categories chỉ cần đặt tên của mỗi checkbox là name="list_categories[]" là được.
#### + Yêu cầu thêm (nếu cần): Dùng plugin JS edit cho markdown (statement, input_statement,...)

## 2. Problemsetter
Template: ***../problem/editProblemProblemSetter.html***

Address: ***admin/problems/edit/{{shortname}}/problemsetter***

### a) Backend:
Gửi xuống client:
- list_authors: Danh sách những user tạo ra bài này.
### b) Frontend:
Gửi lên server (method="post", url="")
- Với mỗi author trong list_author, tạo một input vớiname="list_author[]" là đủ, sau đỏ submit toàn bộ form gửi lên.
- Edit, delete làm dưới frontend, không cần kiểm tra có người dùng đó hay không, chỉ cần gửi lên server là được (tham khảo trên admin - hackerank)

## 3. Testcase
Template: ***../problem/editProblemTestcases.html***

Address: ***/admin/problems/edit/{{shortname}}/testcases***

### a) Backend:
#### Gửi xuống client:
1. problem.shortname: Tên ngắn của bài (cho việc delete)
2. list_testcases: Danh sách test, mỗi test gồm:
- input_file: Đường link tới file input, href trỏ vô đây là được
- output_file: Đường link tới file output, tương tự input_file
- pk: primary key của test (khác id)
- id: id của test (STT)
- tag: Tag của test
- time_limit: Thời gian chạy 
- memory_limit: Giới hạn bộ nhớ
- points: Điểm của test
### b) Frontend:
#### Gửi lên server:
Không có
#### Thiết kế một nút edit, một nút delete ở cuối hàng trỏ về:
- Edit: testcases/edit/{{testcase.pk}} // Lưu ý không có / ở đầu (xem đầu file readme.md này)
- Delete: HỎi lại user + dùng ajax gửi csrf_token về địa chỉ này: ***'/admin/problems/edit/{{shortname}}/testcases/delete/{{testcase.pk}}/'***

## 4. Testcase edit
> To be Continue