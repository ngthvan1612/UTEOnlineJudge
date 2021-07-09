const triggerTabList = [].slice.call(document.querySelectorAll('#list-tab a'))
const triggerDivList = [].slice.call(document.querySelectorAll('#nav-tabContent div'))
triggerTabList[0].classList.add("active")
triggerDivList[0].classList.add("show", "active")

triggerTabList.forEach(function (triggerEl) {
  var tabTrigger = new bootstrap.Tab(triggerEl)

  triggerEl.addEventListener('click', function (event) {
    event.preventDefault()
    tabTrigger.show()
  })
})