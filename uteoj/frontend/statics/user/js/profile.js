function updateImage() {
    $('#user_avatar_preview').attr('src', URL.createObjectURL(event.target.files[0]));
}

function deleteUser(user_name) {
    if (confirm('Are you sure?')) {
        document.getElementById('delete-user').submit();
    }
}
