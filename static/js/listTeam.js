$(function(){
    var teamData = {}
    $("[data-code]").on("click",function(){
        var id_code = $(this).data("code");
        $.post("/team/getTeamDetail",{id_code:id_code},function(data){
            teamData = data;
            $(".teamList-right").removeClass("opacity")
            setTimeout(function(){
                $(".teamList-right").hide();
                bindTmpl(data);
                $(".teamList-right").show();
                $(".teamList-right").addClass("opacity")
            },500)
        });
    });
    $(".into-detail").on("click",function(e){
        var id_code = $(".teamDetail").data("id_code");
        $(".teamList-container").eq(0).removeClass("active");
        $(".teamList-container").eq(1).addClass("active");
    });
    $(".out-detail").on("click",function(e){
        $(".teamList-container").eq(1).removeClass("active");
        $(".teamList-container").eq(0).addClass("active");
    });

    $(".detail-players").on("click",function(e){
        var $target = $(e.target).parent('.player');
        if($target.length === 0){
            return;
        }
        var index = $target.data("playerIndex");
        var player_data = teamData.players[index];
        console.log(player_data)
        bindPlayerTmpl(player_data);
        $(".into-detail").click();
    });
});



function bindTmpl(data){
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