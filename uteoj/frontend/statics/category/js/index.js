var triggerTabList = [].slice.call(document.querySelectorAll('#list-tab a'))
var triggerDivList = [].slice.call(document.querySelectorAll('#nav-tabContent div'))

var listActive = document.getElementsByClassName("active");
var oldInputName=null;

triggerTabList[0].classList.add("active")
triggerDivList[0].classList.add("show", "active")

function showProblem(){
  var value = listActive[1].id;
  console.log(value);
  window.location= "http://127.0.0.1:8000/admin/problems/?category="+value;
}

function getCategoryInfo(){
  oldName = listActive[1].textContent;
  var oldDescription = listActive[2].textContent;
  document.getElementById("inputEditName").value = oldName;
  document.getElementById("editDescription").value = oldDescription;
  console.log(oldName);
  console.log(oldDescription);
}

triggerTabList.forEach(function (triggerEl) {
  var tabTrigger = new bootstrap.Tab(triggerEl)

  triggerEl.addEventListener('click', function (event) {
    event.preventDefault()
    tabTrigger.show()
  })
})

function addNewCategory() {
  var inputName = document.getElementById("inputName").value;
  var description = document.getElementById("description").value;

  $.ajax({
    url: '/admin/categories/',
    type: 'POST',
    data: {
      method: 'add', //method là add
      name: inputName, //cái tên mới
      description: description, //thông tin phụ
      csrfmiddlewaretoken: CSRF_TOKEN, ///phải có (ở trên)
    },
    success: function (data) {
      if (data.status == 'success') {
        ///xử lý message khi thành công - có thể alert ra, có thể cập nhật vào label trong modal (đổi thành màu xanh)
        alert("Add Success");
        console.log("SUCCESS: " + data.message);
        location.reload();
      } else {
        ///xử lý message khi lỗi (như trên)
        console.log("ERROR: " + data.message);
      }
    }
  })
}

function editCategory(){
  var newName = document.getElementById("inputEditName").value;
  var newDescripttion = document.getElementById("editDescription").value;

  $.ajax({
    url: '/admin/categories/',
    type: 'POST',
    data: {
      method : 'edit', 
      old_name : oldName,
      new_name : newName,
      description: newDescripttion,
      csrfmiddlewaretoken: CSRF_TOKEN, ///phải có (ở trên)
    },
    success: function(data) {
        if (data.status=='success') {
            ///xử lý message khi thành công - có thể alert ra, có thể cập nhật vào label trong modal (đổi thành màu xanh)
            alert("Update Success");
            console.log("SUCCESS: " + data.message);
            location.reload();
        }
        else {
            ///xử lý message khi lỗi (như trên)
            console.log("ERROR: " + data.message);
        }
    }
});
}