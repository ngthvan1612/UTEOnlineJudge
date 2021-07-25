updatePage();
updateSelected();
getNumber();

function updatePage() {
    var pagination = document.getElementById("Pagination");

    var pageCurrent = parseInt(document.getElementById("page_current").value);
    var totalPage = parseInt(document.getElementById("page_total").value);
    var base = pageCurrent;

    if (base > totalPage) base = totalPage;
    if (totalPage - pageCurrent <= 1) pageCurrent = totalPage - 1;
    if (pageCurrent <= 0) pageCurrent = 1;

    if (pageCurrent == 1) {
        document.getElementById("previous").classList.add("disabled");
    }
    if (base >= totalPage) {
        document.getElementById("next").classList.add("disabled");
    }

    for (var i = Math.max(pageCurrent - 1, 1); i <= Math.min(pageCurrent + 1, totalPage); i++) {
        var aElement = document.createElement('a');
        aElement.classList.add("page-link");
        aElement.setAttribute('href', "javascript:;");
        aElement.textContent = i.toString();

        var liElement = document.createElement("li");
        liElement.classList.add("page-item");
        if (i == base) liElement.classList.add("active");
        liElement.onclick = function () {
            element = this.children[0];
            goNewPage(parseInt(element.textContent),);
        }
        liElement.appendChild(aElement);

        if (base == 2 && totalPage == 2) pagination.insertBefore(liElement, pagination.children[i - pageCurrent + 1]);
        else if (base != 1) pagination.insertBefore(liElement, pagination.children[i - pageCurrent + 2]);
        else pagination.insertBefore(liElement, pagination.children[i - pageCurrent + 1]);
    }
}

function updateSelected(){
    var selectBox = document.getElementById("listNumber").children[1];

    var urlSearchParams = new URLSearchParams(window.location.search);
    var params = Object.fromEntries(urlSearchParams.entries())

    if (params["rows_per_page"]!=null){
        value = parseInt(params["rows_per_page"]);
        selectBox.selectedIndex = (value-10)/5;
    }

    if (params["search"]!=null){
        document.getElementById("search").value = params["search"];
    }
}

function getNumber() {
    var selectBox = document.getElementById("listNumber").children[1];
    var value = parseInt(selectBox[selectBox.selectedIndex].value) * 5 + 10;
    return value;
}

function getName(){
    return (document.getElementById("search").value);
}

function previous() {
    var page = parseInt(document.getElementsByClassName("active")[2].children[0].textContent);
    goNewPage(page - 1);
}

function next() {
    var page = parseInt(document.getElementsByClassName("active")[2].children[0].textContent);
    goNewPage(page + 1);
}

function goNewPage(page) {
    console.log("*");
    var query = "";
    var listQuery =["page="+page.toString()];
    
    var numberOfUser=getNumber();
    listQuery.push("rows_per_page="+numberOfUser.toString());

    var searchName=getName();
    console.log(searchName);
    if (searchName !="") listQuery.push("search="+searchName.toString());

    for (var i = 0; i < listQuery.length; i++) {
        if (i == 0) query += listQuery[i];
        else query += "&" + listQuery[i];
    }
    
    console.log(query);
    window.location = "/admin/users/administrators/?" + query;
}