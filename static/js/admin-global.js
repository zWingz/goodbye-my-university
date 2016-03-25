(function(){
    var href = location.pathname;
    var arr = href.split("/");
    var arg = arr[arr.length-1];
    $("li[data-nav-type='"+arg+"']").addClass("active");
})();