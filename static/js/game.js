

$(function(){
    $("#weeknum").data('date', moment().format("YYYY-MM-DD")).text(getWeekDate()[0]+" 至 "+getWeekDate()[6]);
    $("#next-week").on("click",function(){
        var date = moment($("#weeknum").data("date")).add(7,"d");
        $("#weeknum").data('date', date.format("YYYY-MM-DD")).text(getWeekDate(date.toDate())[0]+" 至 "+getWeekDate(date.toDate())[6]);
        $.ajax({
            url: '/game/fixtures',
            type: 'post',
            dataType: 'json',
            data: {weeknum: ""+date.year()+(""+date.week()-1)},
        })
        .done(function(data) {
            bindGmaeTmpl(data.fixtures);
        });
    });
    //  上一周
    $("#prev-week").on("click",function(){
        var date = moment($("#weeknum").data("date")).subtract(7,"d");
        $("#weeknum").data('date', date.format("YYYY-MM-DD")).text(getWeekDate(date.toDate())[0]+" 至 "+getWeekDate(date.toDate())[6]);
        $.ajax({
            url: '/game/fixtures',
            type: 'post',
            dataType: 'json',
            data: {weeknum: ""+date.year()+(""+date.week()-1)},
        })
        .done(function(data) {
            bindGmaeTmpl(data.fixtures);
        });
    });
});

//  渲染赛程
function bindGmaeTmpl(data){
    console.log(data)
    var table = $(".fixtures .data-table");
    if (data.length === 0) {
        table.hide();
        $(".none-data").show();
    }else {
        var tbody = table.find("tbody");
        tbody.html("");
        data.forEach(function(item,index){
            var tr = $("<tr>");
            var game_time = $("<td class='game-time'>").append($("<div>").append(item['game-date']))
                                                                                                    .append($("<div>").append(item['game-time']));
            var location = $("<td class='location'>").append(item.location);
            var status = $("<td class='status'>");
            var point = $("<td class='point'>");
            var game_data = $("<td class='game-data'>");
            if(item.status === 0 ){
                status.append('未赛');
                point.append(' --- ')
            }else {
                status.append('已完结');
                point.append(item.point)
                game_data.append($("<a>").attr("href","/game/getGame?id_code="+item.id_code).attr("target","_blank").append("查看"));
            }
            var team_one = $("<td class='team-td'>").append(
                $("<a>").attr("href","/team/teamDetail?id_code="+item.team_one.id_code).attr("target","_blank")
                    .append($("<img>").attr("src","/static/files/teamLogo/"+item.team_one.logo))
                    .append(item.team_one.name)
            );
            var team_two = $("<td class='team-td'>").append(
                $("<a>").attr("href","/team/teamDetail?id_code="+item.team_two.id_code).attr("target","_blank")
                    .append($("<img>").attr("src","/static/files/teamLogo/"+item.team_two.logo))
                    .append(item.team_two.name)
            );
            tr.append(game_time).append(location).append(status).append(team_one)
                .append(point).append(team_two).append(game_data);
            tbody.append(tr);
        });
        table.show();
        $(".none-data").hide();
    }
}

//返回本周的日期
function getWeekDate(currentdate){
    var date = typeof currentdate === 'undefined' ? new Date():new Date(currentdate);
    var week_day = date.getDay();
    if(week_day === 0){
        week_day = 7;
    }
    var result = [];
    var result_date; 
    for(var i=0;i<7;i++){
        result_date = new Date();
        result_date.setFullYear(date.getFullYear());
        result_date.setMonth(date.getMonth());
        result_date.setDate(date.getDate() + (i-week_day+1));
        result.push(dateFormat(result_date));
    }
    return result;
}


//格式化日期为 YYYY-mm-dd
function dateFormat(date){
    var year = date.getFullYear();
    var month = date.getMonth()+1;
    var day = date.getDate();
    return year+"-"+(+month<10?"0"+month:month)+"-"+(+day<10?"0"+day:day);
}