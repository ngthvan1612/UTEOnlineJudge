updatePage();

function updatePage() {
    var pageArray = [];
    var pagination = document.getElementById("Pagination");
    var pageCurrent = parseInt(document.getElementById("page_current").value);
    var totalPage = parseInt(document.getElementById("page_total").value);
    var base = pageCurrent;

    if (base > totalPage) base = totalPage;

    if (pageCurrent == 1) {
        document.getElementById("first").style.display = "none";
        document.getElementById("previous").style.display = "none";
    }
    if (base == totalPage) {
        document.getElementById("next").style.display = "none";
        document.getElementById("end").style.display = "none";
    }

    if (base > 4) pageArray.push(createBtn("...", totalPage));

    for (var i = Math.max(pageCurrent - 3, 1); i <= Math.min(pageCurrent + 3, totalPage); i++)
        pageArray.push(createBtn(i, base));

    if (base + 3 < totalPage) pageArray.push(createBtn("...", totalPage));

    for (var i = 0; i < pageArray.length; i++)
        pagination.insertBefore(pageArray[i], pagination.children[i + 2]);
}

function createBtn(id, Max) {
    var aElement;
    if (id != "...") {
        aElement = document.createElement('a');
    } else aElement = document.createElement('span');
    aElement.textContent = id.toString();
    aElement.classList.add("page-link");


    var liElement = document.createElement("li");
    liElement.classList.add("page-item");
    if (id == Max) liElement.classList.add("active");
    if (id != "...") {
        liElement.onclick = function () {
            element = this.children[0];
            window.location = "/submissions?page=" + element.textContent.toString();
            //goNewPage(parseInt(element.textContent), '');
        }
    }
    else{
        liElement.classList.add("disabled");
    }
    liElement.appendChild(aElement);
    return liElement;
}

function previous() {
    var page = parseInt(document.getElementsByClassName("active")[1].children[0].textContent);
    window.location = "/submissions?page=" + (page-1).toString();
}

function next() {
    var page = parseInt(document.getElementsByClassName("active")[1].children[0].textContent);
    window.location = "/submissions?page=" + (page+1).toString();
}

function goFirst() {
    window.location = "/submissions?page=1" ;
}

function goEnd() {
    var totalPage = parseInt(document.getElementById("page_total").value);
    window.location = "/submissions?page=" + (totalPage).toString();
}