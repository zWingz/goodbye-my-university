$(function(){
    var hash = location.hash;
    new bingUserTabs(".usercenter-nav",".usercenter-content");
    $("a[href*='"+hash+"']").click();
    new changeAvatar("#uploadImg","/users/updateImage",".user-avatar");
    new changeAvatar("#uploadLogo","/team/changeLogo",".team-avatar");

    //  个人信息编辑
    new bindEditFnc("#editUserInfoBtn",{});
    //  球员信息编辑
    new bindEditFnc("#editPlayerInfoBtn",{
        saveCb:function($target){
            var postData = {}
            $target.parents(".content-bd").find(".my-form-input").each(function(index,input){
                postData[$(this).attr("name")] = $(this).val();
            });
            console.log(postData);
            $.ajax({
                    url: '/team/editPlayer',
                    type: 'post',
                    dataType: 'json',
                    data: postData
                })
                .done(function(data) {
                    // console.log(data);
                    location.reload();
                });
        }
    });
    //  球队信息编辑
    new bindEditFnc("#editTeamInfoBtn",{
        saveCb:function($target){
            var postData = {}
            $target.parents(".content-bd").find(".my-form-input").each(function(index,input){
                postData[$(this).attr("name")] = $(this).val();
            });
            console.log(postData);
            $.ajax({
                    url: '/team/editTeam',
                    type: 'post',
                    dataType: 'json',
                    data: postData
                })
                .done(function(data) {
                    // console.log(data);
                    location.reload();
                });
        }
    });

    new bindEditFnc("#edit-player-btn",{
        editCb:function($target){
            var container = $target.parents(".playerDetailContainer");
            var number = container.find(".detail-number");
            var position = container.find(".detail-position");
            var select = $("<select name='position'></select>");
            select.append("<option value='PG'>控卫</option>")
            .append("<option value='SG'>分位</option>")
            .append("<option value='C'>中锋</option>")
            .append("<option value='PF'>大前</option>")
            .append("<option value='SF'>小前</option>");
            select.val(position.text());
            var input = $("<input name='number' type='text'>").val(number.text());
            position.after(select);
            number.after(input);
            position.hide()
            number.hide();
        },
        saveCb:function($target){
            var postData = {}
            postData.id_code = $target.parents(".playerDetailContainer").find(".playerDetail").data('id_code');
            postData.number = $target.parents(".playerDetailContainer").find("[name='number']").val();
            postData.position = $target.parents(".playerDetailContainer").find("[name='position']").val();
            console.log(postData);
            $.ajax({
                    url: '/team/changeNumAndPos',
                    type: 'post',
                    dataType: 'json',
                    data: postData
                })
                .done(function(data) {
                    console.log(data);
                    location.reload();
                });
            }
        });

    //  msg 弹出框
    $(".message-action").on("click",function(e){
        var $target = $(e.target);
        var index = $target.index();
        var container = $target.parents(".message-item");
        if(index === 0) {
            var player_id_code = container.find(".sender-name").data("id-code");
            var msg_id_code = container.data('id-code')
            $("#applyModal").data("player-id-code",player_id_code).data("msg-id-code",msg_id_code);
            $("#applyModal").modal("open");
        }else {

        }
    });
    //  提交同意申请
    $("#agreeApplyJoin").on("click",function(){
        var postData = {};
        var container = $("#applyModal");
        postData.player_id_code = container.data("player-id-code");
        postData.msg_id_code = container.data("msg-id-code");
        postData['r-position']= container.find("[name='r-position']").val();
        postData['r-number'] = container.find("[name='r-number']").val();
        console.log(postData)
        $.post("/team/joinTeam",postData,function(data){
            console.log(data);
        });
    });

    $(document.body).on("click",function(e){
        var $target = $(e.target);
        if($target.hasClass("players-item")){
            var id_code = $target.data("idcode");
            $.post("/team/getPlayerDetail",{id_code:id_code},function(data){
                // console.log(data.players);
                bindPlayerTmpl(data.players[0]);
                $(".playerDetailContainer").css("transform","scale(1)");
            });
        }else if($target.parents(".playerDetailContainer").length === 0 && e.target !== $(".playerDetailContainer").get(0)){
            $(".playerDetailContainer").css("transform","scale(0)")
        }
    });
});


//  绑定team中球员信息面板
function bindPlayerTmpl(player){
    var container = $(".playerDetail");
    container.data('id_code', player.id_code);
    container.find(".player-logo").attr("src","/static/upload/"+player.img_path);
    container.find(".detail-name").html(player.name);
    container.find(".detail-number").html(player.number);
    container.find(".detail-position").html(player.position);
    container.find(".detail-height").html(player.height);
    container.find(".detail-weight").html(player.weight);
    container.find(".detail-join-time").html(new Date(player.create_time).toLocaleDateString());
    container.find(".detail-desc").html(player.desc);
}

//  左侧兰tabs事件
function bingUserTabs(nav,content){
    this.nav = $(nav);
    this.content = $(content);
    this.items = this.nav.find("[my-role='nav-item']");
    this.contents = this.content.find("[my-role='content-item']");
    var self = this;
    this.items.on("click",function(e){
        e.preventDefault();
        var nav_index = $(this).attr("nav-index");
        self.items.removeClass("active");
        $(this).addClass("active");
        var content ;
        self.contents.each(function(index, el) {
            if( nav_index == index){
                content = $(el);
            }    
            $(el).removeClass("active").removeClass("opacity");
        });
        content.addClass('active');
        setTimeout(function(){
            content.addClass("opacity")
        },200);
    });
}

// 个人,team头像修改
function changeAvatar(fileInput,url,img){
    this.ele = $(fileInput);
    this.ele.on('change', function(event) {
        event.preventDefault();
        var formData = new FormData();
        formData.append("file",this.files[0]);
        console.log(this.files[0]);
        $.ajax({
            url: url,
            type: 'post',
            dataType: 'json',
            data: formData,
            processData:false,
            contentType:false,
        })
        .done(function(data) {
            var fileInfo = data.fileInfo;
            $(img).attr("src",fileInfo.url).attr("filename",fileInfo.uname);
        });
        
    });
}

//  编辑按钮事件绑定
function bindEditFnc(ele,cbObj){
    var self = this;
    this.ele = $(ele);
    this.editCb = cbObj.editCb || function($target){
        var $editabel = $target.parents(".content-bd").find("[editable]");
        $editabel.each(function(){
            var $el = $(this);
            var name = $el.attr("editable");
            var text = $el.text();
            var $input = $("<input>").attr("name",name).addClass("my-form-input").val(text);
            $el.hide();
            $el.parent().append($input);
        });
    };
    this.saveCb = cbObj.saveCb || function($target){
        var postData = {}
        $target.parents(".content-bd").find(".my-form-input").each(function(index,input){
            postData[$(this).attr("name")] = $(this).val();
        });
        $.ajax({
                url: '/users/editUserInfo',
                type: 'post',
                dataType: 'json',
                data: postData
            })
            .done(function(data) {
                // console.log(data);
                location.reload();
            });
    };
    this.cancelCb = cbObj.cancelCb || function($target){
        var $editabel = $target.parents(".content-bd").find("[editable]");
        $editabel.show();
        $editabel.parent().find('.my-form-input').remove();
    };
    this.ele.on('click', function(event) {
        event.preventDefault();
        var $target = $(event.target);
        if($target.hasClass("edit")){
            self.editCb($target);
            $target.hide();
            $target.siblings().show();
            return;
        }else if($target.hasClass('save')){
            self.saveCb($target);
        }else {
            self.cancelCb($target);
        }
        $target.parent().children().hide();
        $target.parent().children().eq(0).show();
    });
}



