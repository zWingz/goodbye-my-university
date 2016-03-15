var teamData = {}
$(function(){
    //  获取球队信息
    var codeTypeMap = {
        'team':{
            url:'/team/getTeamDetail',
            bindTmpl:bindTeamTmpl
        },
        'player':{
            url:'/team/getPlayerDetail',
            bindTmpl:bindPlayerTmpl
        }
    };
    $("[data-code]").on("click",function(){
        var id_code = $(this).data("code");
        var code_type = $(this).data("code-type");
        var map = codeTypeMap[code_type];
        $.post(map.url,{id_code:id_code},function(data){
            $(".teamList-right").removeClass("opacity")
            setTimeout(function(){
                $(".teamList-right").hide();
                map.bindTmpl(data)
                $(".teamList-right").show();
                $(".teamList-right").addClass("opacity")
            },500)
        });
    });

    //  页面切换
    $(".into-detail").on("click",function(e){
        var id_code = $(".teamDetail").data("id_code");
        $(".teamList-container").eq(0).removeClass("active");
        $(".teamList-container").eq(1).addClass("active");
    });
    $(".out-detail").on("click",function(e){
        $(".teamList-container").eq(1).removeClass("active");
        $(".teamList-container").eq(0).addClass("active");
    });

    //  查看某个球员
    $(".detail-players").on("click",function(e){
        var $target = $(e.target).parent('.player');
        if($target.length === 0){
            return;
        }
        var index = $target.data("playerIndex");
        var player_data = teamData.players[index];
        bindPlayerTmpl(player_data);
        $(".into-detail").click();
    });

    //  申请加入
    $(".apply-join-team").on("click",function(){
        var id_code = $(this).parent().data("code");
        $("#applyModal").find(".am-modal-bd").attr("team-id-code",id_code).attr("join-type","apply");
        $("#applyModal").modal("open");
    });
    $(".invite-join-team").on("click",function(){
        var id_code = $(this).parent().data("code");
        $("#applyModal").find(".am-modal-bd").attr("team-id-code",id_code).attr("join-type","invite");
        $("#applyModal").modal("open");
    });
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
            console.log(data);
        });
    });
});



function bindTeamTmpl(data){
    teamData = data;
    var container = $(".teamDetail");
    container.data("id_code",data.team.id_code);
    var team = data.team;
    var players = data.players;
    var data_profile = data.team_data;
    var players_container = container.find('.detail-players');
    container.find(".team-logo").attr("src","/static/upload/"+team.logo);
    container.find(".detail-name").html(team.name);
    container.find(".detail-desc").html(team.desc);
    players_container.html("");
    for (var i = 0; i < players.length; i++) {
        var player = players[i];
        var $div = $("<div>").addClass("player").data('playerIndex', i);
        var $img = $("<img>").attr("src","/static/upload/"+player.img_path);
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
        table.find('[data-type="'+key+'"]').text((data_profile[key]/game).toFixed(2));
    }
}


function bindPlayerTmpl(data){
    var player = data;
    if(data.players !== undefined){
        player = data.players[0];
    }
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
    var table = container.find(".detail-data");
    var data_profile = player.player_data;
    var keys = Object.keys(data_profile);
    var game = data_profile.game;
    if(game == 0){
        return;
    }
    for (var i = 0; i < keys.length; i++) {
        var key = keys[i];
        table.find('[data-type="'+key+'"]').text((data_profile[key]/game));
    }
}