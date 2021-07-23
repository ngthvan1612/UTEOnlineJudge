function createNewListItem(newName){
    var listAuthor = document.getElementById("list-group-author");
    var newBox = document.createElement("div");
    var icon = document.createElement("i");
    var h5 = document.createElement("input");

    newBox.id = newName;
    newBox.classList.add("list-group-item");
    newBox.style.display = "flexbox";
    newBox.onclick = function () {};

    h5.value = newName;
    h5.style.marginBottom = "0";
    h5.style.cursor = "hand";
    h5.style.border = "transparent";
    h5.name = "list_author[]"

    icon.classList.add("fa", "fa-times");
    icon.style.fontSize = "20px";
    icon.style.float = "right";
    icon.onclick = function () {
        listAuthor.removeChild(document.getElementById(newName));
    }

    newBox.appendChild(h5);
    newBox.appendChild(icon);
    
    return newBox;
}

function checkNameExist(newName){
    console.log("*");
    var listItem = document.getElementsByClassName("list-group-item");
    //console.log(listItem);
    for (var item=0;item<listItem.length;item++)
        if (listItem[item].tagName!="A"){
            if (newName == listItem[item].id) return true;
        }
    return false;
}

function addAuthor() {
    var listAuthor = document.getElementById("list-group-author");
    var newName = document.getElementById("input-username").value;

    if (newName == "") return;
    console.log(newName);
    
    if (!checkNameExist(newName)){
        var newBox = createNewListItem(newName);    
        listAuthor.appendChild(newBox);
    }
}

function deleteAuthor(name) {
    var listAuthor = document.getElementById("list-group-author");
    listAuthor.removeChild(document.getElementById(name));
}