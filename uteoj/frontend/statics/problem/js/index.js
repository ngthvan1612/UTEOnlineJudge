$("#search").keyup(function () {
    search_table();
})

function search_table() {
    // Declare variables 
    var input, filter, table, tr, td, i;
    input = document.getElementById("search");
    filter = input.value.toUpperCase();
    table = document.getElementById("table_id");
    tr = table.getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td");
        //console.log(td[1].innerHTML);
        for (j = 0; j < td.length; j++){
            let tdata = td[0].id;
            if (tdata) {
                if (tdata.toLowerCase().indexOf(filter.toLowerCase()) > -1) {
                    tr[i].style.display = "";
                    break;
                } else {
                    tr[i].style.display = "none";
                }
            }
        }
    }
}

function showSelect(){
    var item = document.getElementById("addCatetory");
    var selectItem = document.getElementById("selectCategory");
    console.log(selectItem);
    item.style.display="none";
    selectItem.style.display="block";
}

function chooseCategory(){
    var checkExist = false;
    var categoryBoxes = document.getElementsByClassName("listCatgories")[0];
    var categoryAdds = document.getElementsByClassName("categoryAdd");
    var selectBox = document.getElementById("selectCategory");

    var selectedValue = selectBox.options[selectBox.selectedIndex].value;

    var newBox = document.createElement("div");
    var icon = document.createElement("i");
    var h5 = document.createElement("span");

    newBox.id = selectedValue;

    h5.textContent = selectedValue;
    h5.style.fontSize = "14px";

    icon.classList.add("fa","fa-times");
    icon.style.marginLeft = "6px";
    icon.style.fontSize = "14px";
    icon.id = selectedValue;
    icon.onclick=function(){
        var element = document.getElementById(this.id);
        categoryBoxes.removeChild(element);
    }

    newBox.classList.add("btn", "btn-secondary","categoryAdd");
    newBox.name = selectedValue;
    newBox.appendChild(h5);
    newBox.appendChild(icon);
    newBox.style.display = "flexbox";
    newBox.style.marginRight = "3px";
    newBox.style.marginTop = "3px";

    for (var i=0;i<categoryAdds.length;i++) 
        if (categoryAdds[i].name == selectedValue) checkExist=true;
    
    if (!checkExist && selectedValue!="") categoryBoxes.appendChild(newBox);
}