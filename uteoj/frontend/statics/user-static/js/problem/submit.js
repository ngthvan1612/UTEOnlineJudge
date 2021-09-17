var editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
editor.getSession().setMode("ace/mode/c_cpp");

function check(){
    var valueIn = document.getElementsByClassName("ace_text-input")[0].value;
    document.getElementById("source").value = valueIn;
}