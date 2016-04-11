// var team_data = {};
$(function(){

    $(window).on("scroll",function(e){
        var top = getScrollTop();
        if(top > 110){
            $(".flex-right").css("top",top-110+"px")
        }else{
            $(".flex-right").css("top","0px")
        }
    });

    var codeTypeMap = {
            'team':{
                url:'/team/teamDetail',
                bindTmpl:bindTeamTmpl
            },
            'player':{
                url:'/team/playerDetail',
                bindTmpl:bindPlayerTmpl
            }
        };

    //  事件委托至content
    $(".teamList-content").on("click",function(e){
        var target = $(e.target);
        if( target.hasClass('apply-join-team')){  //  请求加入队伍
            var id_code = target.parent().data("code");
            $("#applyModal").find(".am-modal-bd").attr("team-id-code",id_code).attr("join-type","apply");
            $("#applyModal").modal("open");
        }else if(target.hasClass("invite-join-team")){ // 邀请加入队伍
            var id_code = target.parent().data("code");
            $("#applyModal").find(".am-modal-bd").attr("team-id-code",id_code).attr("join-type","invite");
            $("#applyModal").modal("open");
        }else if(target.hasClass("invite-game")){ // 邀请比赛
            var id_code = target.parent().data("code");
            $("#inviteGameModal").find(".am-modal-bd").attr("team-id-code",id_code);
            $("#inviteGameModal").modal("open");
        }else if(typeof target.parents(".team-item").attr("data-code") !== 'undefined'){
            var id_code = target.parents(".team-item").data("code");
            var code_type = target.parents(".team-item").data("code-type");
            var map = codeTypeMap[code_type];
            $.post(map.url,{id_code:id_code},function(data){
                $(".flex-right").show();
                setTimeout(function(){
                    $(".flex-right").css("width","400px");
                    $(".flex-right").removeClass("opacity")
                    setTimeout(function(){
                        $(".flex-right").hide();
                        map.bindTmpl(data)
                        $(".flex-right").show();
                        $(".flex-right").addClass("opacity")
                    },500);
                },100);
            });
        }
    });

    // 邀请,申请加入的提交btn
    $("#saveApplyJoin").on('click',function(){
        var postData = {},url = '';
        var container = $(this).parent();
        var type = container.attr('join-type');
        postData.id_code = container.attr("team-id-code");
        var position = container.find("[name='r-position']").val();
        var number = container.find("[name='r-number']").val();
        var desc =container.find("[name='r-saysomething']").val();
        var tmp = $("<div>").append(
            $("<div class='msg-content-label'>").append("位置:").append($("<span class='msg-content-position'>").append(position))
            .append("号码:").append($("<span class='msg-content-number'>").append(number)))
            .append($("<div class='msg-content-label'>").append("留言:").append($("<span>").append(desc))
            );
        postData.content= tmp.html();
        if(type === 'apply'){
            url = '/msg/applyJoinTeam';
        }else if(type === 'invite') {
            url = '/msg/inviteJoinTeam';
        }
        $.post(url,postData,function(data){
            msgPopup(data.message);
            if (data.success === 1) {
                reload();
            }
        });
    });

    // 邀请比赛btn
    $("#invite-game-btn").on('click',function(){
        var postData = {},url = '/msg/inviteGame';
        var container = $(this).parent().parent();
        postData.id_code = container.attr("team-id-code");
        var game_date = container.find("[name='game-date']").val();
        postData.game_date = game_date
        var game_time = container.find("[name='game-time']").val();
        var desc =container.find("[name='saysomething']").val();
        var location = container.find("[name='location']").val();
        var tmp = $("<div>").append(
            $("<div class='msg-content-label'>").append("日期:").append($("<span class='msg-content-game-date'>").append(game_date))
            .append("时间:").append($("<span class='msg-content-game-time'>").append(game_time)))
            .append($("<div class='msg-content-label'>").append("地点:").append($("<span class='msg-content-location'>").append(location)))
            .append($("<div class='msg-content-label'>").append("留言:").append($("<span>").append(desc))
            );
        postData.content= tmp.html();
        $.post(url,postData,function(data){
            msgPopup(data.message);
            if (data.success === 1) {
                reload();
            }
        });
    });

    // 加载更多
    new loadMore("#load-more-btn");

});



function bindTeamTmpl(data){
    // team_data = data;
    var container = $(".teamDetail");
    var team = data.team[0];
    var players = data.players;
    var data_profile = data.team_data;
    var players_container = container.find('.detail-players');
    container.prev().find(".into-detail").attr("href","/team/teamDetail?id_code="+team.id_code);
    container.find(".team-logo").attr("src","/static/files/teamLogo/"+team.logo);
    container.find(".detail-name").html(team.name);
    container.find(".detail-desc").html(team.desc);
    players_container.html("");
    for (var i = 0; i < players.length; i++) {
        var player = players[i];
        var $div = $("<a>").addClass("player").data('playerIndex', i).attr('href', "/team/playerDetail?id_code="+player.id_code).attr('target', '_blank');;
        var $img = $("<img>").attr("src","/static/files/userImg/"+player.img_path);
        var $name = $("<div>").html(player.name);
        var $position = $("<div>").html(player.position);
        $div.append($img).append($name).append($position);
        players_container.append($div)
    }
    var table = container.find(".detail-data");
    var keys = Object.keys(data_profile);
    var game = data_profile['game'];
    for (var i = 0; i < keys.length; i++) {
        var key = keys[i];
        if(game !== 0){
            table.find('[data-type="'+key+'"]').text((data_profile[key]/game).toFixed(2));
        }else {
            table.find('[data-type="'+key+'"]').text(data_profile[key]);
        }
    }
}


function bindPlayerTmpl(data){
    var player = data;

    if(data.players !== undefined){
        player = data.players[0];
    }
    var container = $(".playerDetail");
    container.prev().find(".into-detail").attr("href","/team/playerDetail?id_code="+player.id_code);
    container.data('id_code', player.id_code);
    container.find(".player-logo").attr("src","/static/files/userImg/"+player.img_path);
    container.find(".detail-name").html(player.name);
    container.find(".detail-number").html(player.number);
    container.find(".detail-position").html(player.position);
    container.find(".detail-height").html(player.height);
    container.find(".detail-weight").html(player.weight);
    container.find(".detail-join-time").html(new Date(player.create_time).toLocaleDateString());
    container.find(".detail-desc").html(player.desc);
    var table = container.find(".detail-data");
    var data_profile = player.player_data;
    var keys = Object.keys(data_profile);
    var game = data_profile.game;
    for (var i = 0; i < keys.length; i++) {
        var key = keys[i];
        if(game !== 0){
            table.find('[data-type="'+key+'"]').text((data_profile[key]/game));
        }else {
            table.find('[data-type="'+key+'"]').text((data_profile[key]));
        }
    }
}


function getScrollTop()
{
    var scrollTop=0;
    if(document.documentElement&&document.documentElement.scrollTop)
    {
        scrollTop=document.documentElement.scrollTop;
    }
    else if(document.body)
    {
        scrollTop=document.body.scrollTop;
    }
    return scrollTop;
}

function loadMore(ele){
    this.ele = $(ele);
    this.page = 1;
    var self = this;
    if(this.ele.attr('load-type') === "team"){
        this.url = "listTeam";
        this.render = function(data,cb){
            var is_free_player = data.is_free_player;
            data = data.teams
            var $df = $(document.createDocumentFragment());
            data.forEach(function(ele,index){
                var $item = $("<div>").addClass("team-item").attr("data-code-type","team").attr("data-code",ele.id_code)
                var $img = $("<img>").addClass('team-logo').attr("src","/static/files/teamLogo/"+ele.logo);
                var $info = $("<div>").addClass("team-info");
                var can_inivite = ele.can_inivite;
                $info.append($("<span>").append($("<label>球队名:</label>")).append(ele.name))
                            .append($("<span>").append($("<label>学校:</label>")).append(ele.school))
                            .append($("<span>").append($("<label>管理员:</label>")).append(ele.manager))
                            .append($("<span>").append($("<label>创建时间:</label>")).append(ele.create_time));
                $item.append($img).append($info);
                if(is_free_player){
                    $item.append($("<button type='button' class='apply-join-team am-btn am-btn-default'>申请加入</button>"))
                }
                if(can_inivite){
                    $item.append($("<button type='button' class='invite-team am-btn am-btn-default'>邀请比赛</button>"))
                }
                $df.append($item);
            });
            self.ele.prev().before($df);
            cb();
        };
    }else {
        this.url = "listPlayer";
        this.render = function(data,cb){
            var is_manager = data.is_manager;
            data = data.players;
            var $df = $(document.createDocumentFragment());
            data.forEach(function(ele,index){
                var $item = $("<div>").addClass("team-item").attr("data-code-type","player").attr("data-code",ele.id_code)
                var $img = $("<img>").addClass('team-logo').attr("src","/static/files/userImg/"+ele.img_path);
                var $info = $("<div>").addClass("team-info");
                $info.append($("<span>").append($("<label>姓名:</label>")).append(ele.name))
                            .append($("<span>").append($("<label>球队:</label>")).append(ele.team))
                            .append($("<span>").append($("<label>学校:</label>")).append(ele.school))
                            .append($("<span>").append($("<label>位置:</label>")).append(ele.position));
                $item.append($img).append($info);
                if(is_manager && ele.team === '无'){
                    $item.append($("<button type='button' class='invite-join-team am-btn am-btn-default'>邀请加入</button>"))
                }
                $df.append($item);
            });
            self.ele.prev().before($df);
            cb();
        };
    }
    this.load = function(data){
        self.ele.hide();
        self.ele.prev().show();
        setTimeout(function(){
            self.render(data,function(){
                self.ele.prev().hide();
                self.ele.show();
            });
        },500);
    };
    this.ele.on("click",function(){
        self.page ++;
        $.post(self.url, {page: self.page}, function(data, textStatus, xhr) {
            self.load(data);
        });
    });
}


// 时间选择器禁止今天以及之前的选择
(function(){
    var nowTemp = new Date();
    $(".game-date-picker").datepicker({
          onRender: function(date, viewMode) {
            // 默认 days 视图，与当前日期比较
            var viewDate = nowTemp;
            return date.valueOf() < viewDate.valueOf() ? 'am-disabled' : '';
          }
        })
})();