var editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
editor.getSession().setMode("ace/mode/c_cpp");

function check(){
    document.getElementById("source").value = editor.getValue();
    console.log(data);
}