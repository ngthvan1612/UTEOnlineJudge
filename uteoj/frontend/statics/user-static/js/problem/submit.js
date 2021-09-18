var editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
editor.getSession().setMode("ace/mode/c_cpp");

function check(){
    var valueIn = document.getElementsByClassName("ace_line");
    var data = "";
    for (var i=0; i<valueIn.length; i++){
        data+=(valueIn[i].children[0].textContent + "\n")
    }


    document.getElementById("source").value = data;
}