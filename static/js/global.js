(function(){
    var href = location.pathname;
    var arr = href.split("/");
    var arg = arr[arr.length-1];
    $("li[data-nav-type='"+arg+"']").addClass("tabactive");
})();

$(function(){
    $(".my-tabs").each(function(index,ele){
        var $ele = $(this);
        var type = $ele.attr('changeType');
        $ele.children(".my-tabs-nav").find("li").on(type, function(event) {
            event.preventDefault();
            var i = $(this).index();
            $(this).siblings().removeClass("my-tabs-active");
            $(this).addClass("my-tabs-active");
            $ele.children(".my-tabs-bd").find('.my-tabs-panel').removeClass("my-tabs-active")
            $ele.children(".my-tabs-bd").find('.my-tabs-panel').eq(i).addClass('my-tabs-active')
        });
    });


});


function msgPopup(str,time) {
    var dialog = $("#my-popup");
    if(dialog.length === 0) {
        var $div = $("<div>").addClass("am-modal am-modal-alert am-modal-no-btn").attr("tabindex","-1").attr("id","my-popup");
        var $dialog = $("<div>").addClass("am-modal-dialog");
        var $bd = $("<div>").addClass("am-modal-bd");
        $div.append($dialog.append($bd));
        $(document.body).append($div);
        dialog = $div;
    }
    var popup = function(str,time){
        dialog.find(".am-modal-bd").html("").append(str);
        dialog.modal("open");
        setTimeout(function(){
            dialog.modal("close")
        },time|1000);
    }
    msgPopup = popup;
    popup(str,time);
}

function reload(time){
    setTimeout(function(){
        location.reload();
    },time | 1000)
}