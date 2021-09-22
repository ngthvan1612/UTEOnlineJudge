var triggerTabList = [].slice.call(document.querySelectorAll('#list-tab a'))
var triggerDivList = [].slice.call(document.querySelectorAll('#nav-tabContent div'))

var listActive = document.getElementsByClassName("active list-group-item");
var oldInputName = null;

triggerTabList[0].classList.add("active")
triggerDivList[0].classList.add("show", "active")

function showProblem() {
  var value = listActive[0].id;
  console.log(value);
  window.location = "/admin/problems/?category=" + value;
}

function getCategoryInfo(value) {
  oldName = listActive[1].textContent;
  var oldDescription = listActive[2].textContent;
  if (value === 0) {
    console.log("+++++");
    document.getElementById("inputEditName").value = oldName;
    document.getElementById("editDescription").value = oldDescription;
  } 
  else {
    console.log("+++++");
    document.getElementById("inputDeleteName").value = oldName;
    document.getElementById("deleteDescription").value = oldDescription;
  }
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

function editCategory() {
  var newName = document.getElementById("inputEditName").value;
  var newDescripttion = document.getElementById("editDescription").value;

  $.ajax({
    url: '/admin/categories/',
    type: 'POST',
    data: {
      method: 'edit',
      old_name: oldName,
      new_name: newName,
      description: newDescripttion,
      csrfmiddlewaretoken: CSRF_TOKEN, ///phải có (ở trên)
    },
    success: function (data) {
      if (data.status == 'success') {
        ///xử lý message khi thành công - có thể alert ra, có thể cập nhật vào label trong modal (đổi thành màu xanh)
        alert("Update Success");
        console.log("SUCCESS: " + data.message);
        location.reload();
      } else {
        ///xử lý message khi lỗi (như trên)
        console.log("ERROR: " + data.message);
      }
    }
  });
}

function deleteCategory() {
  var name = document.getElementById("inputDeleteName").value;

  $.ajax({
    url: '/admin/categories/',
    type: 'POST',
    data: {
      method: 'delete',
      name: name,
      csrfmiddlewaretoken: CSRF_TOKEN, ///phải có (ở trên)
    },
    success: function (data) {
      if (data.status == 'success') {
        ///xử lý message khi thành công - có thể alert ra, có thể cập nhật vào label trong modal (đổi thành màu xanh)
        alert("Delete Success");
        console.log("SUCCESS: " + data.message);
        location.reload();
      } else {
        ///xử lý message khi lỗi (như trên)
        console.log("ERRRRRORR: " + data);
      }
    }
  });
}