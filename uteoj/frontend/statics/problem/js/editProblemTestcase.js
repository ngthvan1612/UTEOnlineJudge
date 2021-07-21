var probName = null;
var idTest = null;

$('.custom-file-input').on('change', function () {
    let fileName = $(this).val().split('\\').pop();
    $(this).next('.custom-file-label').addClass("selected").html(fileName);
});

function updateInfo(prob, id) {
    probName = prob;
    idTest = id;
    console.log(probName, idTest);
}


function deleteTestCase() {
    $.ajax({
        url: '/admin/problems/edit/' + probName + '/testcases/delete/' + idTest.toString() + '/',
        method: 'POST',
        data: {
            method: 'delete',
            csrfmiddlewaretoken: CSRF_TOKEN
        },
        success: function(data) {
            location.reload();
        }
    });
}