updatePage();
updateFilter();

function showSelect() {
    var item = document.getElementById("addCatetory");
    var selectItem = document.getElementById("selectCategory");

    item.style.display = "none";
    selectItem.style.display = "block";
}

function createNewCategory(selectedValue) {
    var categoryBoxes = document.getElementsByClassName("listCatgories")[0];

    var newBox = document.createElement("div");
    var icon = document.createElement("i");
    var h5 = document.createElement("span");

    newBox.id = selectedValue;

    h5.textContent = selectedValue;
    h5.style.fontSize = "14px";

    icon.classList.add("fa", "fa-times");
    icon.style.marginLeft = "6px";
    icon.style.fontSize = "14px";
    icon.id = selectedValue;
    icon.onclick = function () {
        var element = document.getElementById(this.id);
        categoryBoxes.removeChild(element);
    }

    newBox.classList.add("btn", "btn-secondary", "categoryAdd");
    newBox.name = selectedValue;
    newBox.appendChild(h5);
    newBox.appendChild(icon);
    newBox.style.display = "flexbox";
    newBox.style.marginRight = "3px";
    newBox.style.marginTop = "3px";

    return newBox;
}

function chooseCategory() {
    var checkExist = false;
    var categoryBoxes = document.getElementsByClassName("listCatgories")[0];
    var categoryAdds = document.getElementsByClassName("categoryAdd");
    var selectBox = document.getElementById("selectCategory");

    var selectedValue = selectBox.options[selectBox.selectedIndex].value;

    var newBox = createNewCategory(selectedValue);

    for (var i = 0; i < categoryAdds.length; i++)
        if (categoryAdds[i].name == selectedValue) checkExist = true;

    if (!checkExist && selectedValue != "") categoryBoxes.appendChild(newBox);
}

function createBtn(id, Max) {
    var aElement;
    if (id != "...") {
        aElement = document.createElement('a');
        aElement.setAttribute('href', "javascript:;");
    } else aElement = document.createElement('span');
    aElement.textContent = id.toString();
    aElement.classList.add("page-link");


    var liElement = document.createElement("li");
    liElement.classList.add("page-item");
    if (id == Max) liElement.classList.add("active");
    if (id != "...") {
        liElement.onclick = function () {
            element = this.children[0];
            goNewPage(parseInt(element.textContent), '');
        }
    }
    else{
        liElement.classList.add("disabled");
    }
    liElement.appendChild(aElement);
    return liElement;
}

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

function updateFilter() {
    var categoryBoxes = document.getElementsByClassName("listCatgories")[0];
    var selectType = document.getElementById("selectType");
    var searchBox = document.getElementById("search");
    var minBox = document.getElementById("minDifficult");
    var maxBox = document.getElementById("maxDifficult");

    var urlSearchParams = new URLSearchParams(window.location.search);
    var params = Object.fromEntries(urlSearchParams.entries())

    console.log(params);

    if (params["category"] != null) {
        var categories = params["category"].split(',');

        for (var item of categories)
            categoryBoxes.appendChild(createNewCategory(item));
    }

    if (params["problem_type"] != null) {
        var problem_type = params["problem_type"];
        if (problem_type == "ACM") selectType.selectedIndex = 1;
        else selectType.selectedIndex = 2;
    }

    if (params["name"] != null) {
        searchBox.value = params["name"];
    }

    if (params["difficult"] != null) {
        var minMax = (params["difficult"]).split(',');
        var min = new Number(minMax[0]);
        var max = new Number(minMax[1]);
        
        if (min == 0) minBox.value = '';
        else minBox.value = minMax[0];
        if (max == 10) maxBox.value = '';
        else maxBox.value = minMax[1];

        console.log(min, max);
    }
}

function previous() {
    var page = parseInt(document.getElementsByClassName("active")[1].children[0].textContent);
    goNewPage(page - 1, '');
}

function next() {
    var page = parseInt(document.getElementsByClassName("active")[1].children[0].textContent);
    goNewPage(page + 1, '');
}

function goFirst() {
    goNewPage(1, '');
}

function goEnd() {
    var totalPage = parseInt(document.getElementById("page_total").value);
    goNewPage(totalPage, '');
}

function difficultFilter() {
    var urlSearchParams = new URLSearchParams(window.location.search);
    var params = Object.fromEntries(urlSearchParams.entries())

    var orderString = "";
    if (params["orderby"] == null || params["orderby"] == "-difficult") {
        orderString = "orderby=difficult"
    } else orderString = "orderby=-difficult"
    goNewPage(1, orderString);
}

function goNewPage(page, orderString) {
    var searchBox = document.getElementById("search");
    var selectedBox = document.getElementById("selectType");
    var categoryAdds = document.getElementsByClassName("categoryAdd");
    var minBox = document.getElementById("minDifficult");
    var maxBox = document.getElementById("maxDifficult");

    var urlSearchParams = new URLSearchParams(window.location.search);
    var params = Object.fromEntries(urlSearchParams.entries())

    /*Cagetory*/
    var category = ""
    if (categoryAdds.length != 0) category = "category=";
    for (var i = 0; i < categoryAdds.length; i++) {
        if (i == 0) category += categoryAdds[i].name
        else category += "," + categoryAdds[i].name
    }

    /*Problem Type*/
    var problem_type = "";
    if (selectedBox.selectedIndex != 0)
        problem_type = "problem_type=" + selectedBox[selectedBox.selectedIndex].value;

    /*Problem Name*/
    var problem_name = "";
    if (searchBox.value != "") problem_name = "name=" + searchBox.value;

    /*Order*/
    var order = "";
    if (params["orderby"] != null) {
        if (params["orderby"] == "difficult") order = "orderby=difficult"
        else order = "orderby=-difficult"
    }

    /*Difficult*/
    var difficult = "";
    if (minBox.value != "") difficult = "difficult="+minBox.value;
    if (maxBox.value != ""){
        if (difficult == "") difficult = "difficult=0,"+maxBox.value;
        else difficult += ","+maxBox.value;
    }
    else if (difficult != "") difficult += ","+maxBox.value;

    var listQuery = [];
    var query = "";

    if (page != 1) listQuery.push("page=" + page.toString());
    if (orderString != "") listQuery.push(orderString);
    else if (order != "") listQuery.push(order);
    if (category != "") listQuery.push(category);
    if (problem_type != "") listQuery.push(problem_type);
    if (problem_name != "") listQuery.push(problem_name);
    if (difficult != "") listQuery.push(difficult);

    for (var i = 0; i < listQuery.length; i++) {
        if (i == 0) query += listQuery[i];
        else query += "&" + listQuery[i];
    }

    window.location = "/admin/problems/?" + query;
}