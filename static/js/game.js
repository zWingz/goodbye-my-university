



$(function(){
    var fixtures = [];
    var weekday = getWeekDate();
    var timeArr = ["09:30","11:00","02:00","03:30","05:00","08:00"];
    $("#fixtures-week").html(weekday[0]+" 至 "+weekday[6]);
    $(".fixtures-item").each(function(){
        var $this = $(this);
        var $tr = $this.parent();
        var colIndex = $tr.index();
        var rowIndex = $this.index();
        $this.attr('colIndex', colIndex).attr("rowIndex",rowIndex-1);
    });

    // 新建赛程
    $("#createFixtures-btn").on("click",function(){
        var postData = [];
        $("#createFixtures-table tbody tr").each(function(){
            var trArr = [];
            $(this).find("td").each(function(){
                if($(this).hasClass("active")){
                    var colIndex = $(this).attr("colIndex");
                    var rowIndex = $(this).attr("rowIndex");
                    var obj = {};
                    obj.time = {};
                    obj.time.date = weekday[colIndex];
                    obj.time.time = timeArr[rowIndex];
                    obj.index = {col:colIndex,row:rowIndex}
                    trArr.push(obj)
                }
            });
            postData.push(trArr);
        });
        $.post('/game/createFixtures',{"fixtures":JSON.stringify(postData)}, function(data, textStatus, xhr) {
            /*optional stuff to do after success */
            // console.log(data);
            fixtures = data;
            var timeLen = data.length;
            for (var i = 0; i < timeLen; i++) {
                var gameLen = data[i].length;
                for (var j= 0; j < gameLen; j++) {
                    var game = data[i][j];
                    if(typeof game.location !== "undefined"){
                        var $td = $("#createFixtures-table tbody tr").eq(game.index.col).find("td").eq(+game.index.row+1);
                        $td.addClass('game-item');
                        var locationDiv = $("<div>").addClass("game-item-location").append(game.location);
                        var $team = $("<div>").append($("<div>").append(game.team_one.name).attr("id_code",game.team_one.id_code))
                                                                    .append($("<i>").addClass('iconfont').append("&#xe607;"))
                                                                    .append($("<div>").append(game.team_two.name).attr("id_code",game.team_two.id_code))
                        $td.append(locationDiv).append($team).removeClass('active');
                    }
                }
            }
        });
    });

    //  选择比赛时间
    $(".fixtures-item").on("click",function(e){
        var $target = $(this);
        $target.addClass("active");
    });

    // 保存赛程
    $("#saveFixtures-btn").on("click",function(){
        console.log(fixtures);
        $.post('/game/saveFixtures', {fixtures: JSON.stringify(fixtures)}, function(data, textStatus, xhr) {
            /*optional stuff to do after success */
            console.log(data)
        });
    });
});



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