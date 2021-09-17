let value = document.getElementById("checkerSource").textContent;
var editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
editor.session.setMode("ace/mode/c_cpp");
editor.setValue(value);

function changeLanguage() {

    let language = $("#languages").val();

    if(language == 'c' || language == 'c++')editor.session.setMode("ace/mode/c_cpp");
    else if(language == 'php')editor.session.setMode("ace/mode/php");
    else if(language == 'python')editor.session.setMode("ace/mode/python");
    else if(language == 'node')editor.session.setMode("ace/mode/javascript");
}

function changeCheck(){
    document.getElementById("use_checker").checked = document.getElementById("checker").checked;
}

function getInfo(){
    document.getElementById("checker_source").value=editor.session.getValue();
    document.getElementById("form").submit();
    //console.log(document.getElementById("checker_source").value);
}