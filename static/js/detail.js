

function showPlayer(id_code,event){
    event.preventDefault();
    $.post('/team/playerDetail', {id_code: id_code}, function(data, textStatus, xhr) {
        $(".detail-right").removeClass("opacity")
            setTimeout(function(){
                $(".detail-right").hide();
                bindPlayerTmpl(data)
                $(".detail-right").show();
                $(".detail-right").addClass("opacity")
            },500);
    });
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