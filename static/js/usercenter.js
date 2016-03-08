$(function(){
    var hash = location.hash;
    new bingUserTabs(".usercenter-nav",".usercenter-content")
    $("a[href*='"+hash+"']").click();
});


function bingUserTabs(nav,content){
    this.nav = $(nav);
    this.content = $(content);
    this.items = this.nav.find("[my-role='nav-item']");
    this.contents = this.content.find("[my-role='content-item']");
    var self = this;
    this.items.on("click",function(e){
        // e.preventDefault();
        var nav_index = $(this).attr("nav-index");
        self.items.removeClass("active");
        $(this).addClass("active");
        var content ;
        self.contents.each(function(index, el) {
            if( nav_index == index){
                content = $(el);
            }    
            $(el).removeClass("active");
        });
        content.addClass('active');
    });
}