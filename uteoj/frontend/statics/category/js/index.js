var triggerTabList = [].slice.call(document.querySelectorAll('#list-tab a'))
var triggerDivList = [].slice.call(document.querySelectorAll('#nav-tabContent div'))
var test = document.getElementsByClassName("active");
var inputName = document.getElementById("inputName");
var description = document.getElementById("description");

triggerTabList[0].classList.add("active")
triggerDivList[0].classList.add("show", "active")

triggerTabList.forEach(function (triggerEl) {
  var tabTrigger = new bootstrap.Tab(triggerEl)

  triggerEl.addEventListener('click', function (event) {
    event.preventDefault()
    tabTrigger.show()
  })
})

function addNewCategory() {
  $.ajax({
    url: '/admin/categories/',
    type: 'POST',
    data: {
      method: 'add', //method là add
      name: inputName.value, //cái tên mới
      description: description.value, //thông tin phụ
      csrfmiddlewaretoken: CSRF_TOKEN, ///phải có (ở trên)
    },
    success: function (data) {
      if (data.status == 'success') {
        ///xử lý message khi thành công - có thể alert ra, có thể cập nhật vào label trong modal (đổi thành màu xanh)
        console.log("SUCCESS: " + data.message);
        reloadCurrentSource();
      } else {
        ///xử lý message khi lỗi (như trên)
        console.log("ERROR: " + data.message);
      }
    }
  })
}

function showProblem(){
  var value = test[1].id;
  console.log(value);
  window.location= "http://127.0.0.1:8000/admin/problems/?category="+value;
}