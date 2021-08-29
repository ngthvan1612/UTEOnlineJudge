function openMessage(){
    $('.offcanvas-overlay')[0].parentNode.removeChild($('.offcanvas-overlay')[0]);
    $('#kt_quick_panel').hide([force = false]);
}

function closeMessage(){
    $('#kt_quick_panel').css({display:""});
    $('#kt_quick_panel').removeClass("offcanvas-on");
}

function showManage(){
    $('#kt_quick_panel').show();
}