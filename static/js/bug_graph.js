/*queue()
    .defer(d3.json,"/ticket_serial/ticket/?format=json")
    .await(makeTicketGraphs);*/

/*queue()
    .defer(d3.json,"/polls/votes/?format=json")
    .await(makeVoteGraphs);*/

/*queue()
    .defer(d3.json,"/rest/polls/option/custom/?format=json")
    .await(makeOptionGraphs);*/

queue()
    .defer(d3.json,"/rest/work/log/custom/?format=json")
    .await(makeWorkGraphs);


/*queue()
    .defer(d3.json,"/rest/tickets/ticket/custom/?format=json")
    .await(makeWorkGraphs);*/

/*function makeTicketGraphs(error,ticketdata){
    if (error){
        console.error("makeGraphs in bug_graph error on receiving dataset:", error.statusText);
        throw error;
    }

    var ndx = crossfilter(ticketdata);
    console.log(ticketdata);

    var ticketDim = ndx.dimension(function (d) {
        return d.options.vote_count;
    })
}*/

/*function makeVoteGraphs(error,votedata){
    if (error){
        console.error("makeGraphs in bug_graph error on receiving dataset:", error.statusText);
        throw error;
    }

    var ndx = crossfilter(votedata);

    //console.log(votedata);

    var ticketVotesDim = ndx.dimension(function(d){
            return d.ticket_name;
    });

    var bugVotesDim = ndx.dimension(function(d){
        if(d.poll_id == 1){
            return d.ticket_name;
        }
    });

    var featureVotesDim = ndx.dimension(function(d){
        if(d.poll_id == 2) {
            return d.ticket_name;
        }
    });

    var pollDim = ndx.dimension(function(d){
        if (d.poll_id == 1) {
            return "Bug";
        }  else if (d.poll_id == 2) {
            return "Feature";
        }
    });

    var statusDim = ndx.dimension(function(d){
        return d.status;
    });

    var ticketVotesGroup = ticketVotesDim.group();

    var bugVotesGroup = bugVotesDim.group().reduceSum(function(d){return d.poll_id==1});
    var featureVotesGroup = featureVotesDim.group().reduceSum(function(d){return d.poll_id==2});
    var statusGroup = statusDim.group();
    var pollGroup = pollDim.group();


    var colorScheme = ["#013369","#D50A0A","#008000","#FFA500","#FFFF00"];


    ticketVotesChart = dc.rowChart("#ticketVotesChart");
    bugVotesChart = dc.rowChart("#bugVotesChart");
    featureVotesChart = dc.rowChart("#featureVotesChart");
    statusChart = dc.rowChart("#statusChart");
    pollChart = dc.rowChart("#pollChart");

    ticketVotesChart
        .ordinalColors(colorScheme)
        .width(300)
        .height(300)
        .dimension(ticketVotesDim)
        .group(ticketVotesGroup)
        .elasticX(true)
        .xAxis().ticks(4);

    bugVotesChart
        .ordinalColors(colorScheme)
        .width(300)
        .height(300)
        .dimension(bugVotesDim)
        .group(bugVotesGroup)
        .elasticX(true)
        .xAxis().ticks(4);

    featureVotesChart
        .ordinalColors(colorScheme)
        .width(300)
        .height(300)
        .dimension(featureVotesDim)
        .group(featureVotesGroup)
        .elasticX(true)
        .xAxis().ticks(4);

    pollChart
        .ordinalColors(colorScheme)
        .width(300)
        .height(300)
        .dimension(pollDim)
        .group(pollGroup)
        .elasticX(true)
        .xAxis().ticks(4);

    statusChart
        .ordinalColors(colorScheme)
        .width(300)
        .height(300)
        .dimension(statusDim)
        .group(statusGroup)
        .elasticX(true)
        .xAxis().ticks(4);

    dc.renderAll();
}*/

/*function makeOptionGraphs(error,optiondata){
    const BUG = 1;
    const FEATURE = 2;

    if (error){
        console.error("makeGraphs in bug_graph error on receiving dataset:", error.statusText);
        throw error;
    }

    var ndx = crossfilter(optiondata);

    var ticketTypeDim = ndx.dimension(function(d){
        if (d.poll_id == BUG){
            return "Bug";
        } else if (d.poll_id == FEATURE){
            return "Feature"
        } else {}

    });

    var ticketDim = ndx.dimension(function(d){
        return d.ticket_name;
    });

    var votesDim = ndx.dimension(function(d){
       return d.vote_count;
    });

    var statusDim = ndx.dimension(function(d){
        return d.ticket_status;
    });

    var ticketTypeGroup = ticketTypeDim.group();
    var ticketGroup = ticketDim.group();

    //pollDim.filter("Bug");
    var ticketVotesGroup = ticketDim.group().reduceSum(function (d) {
        return d.vote_count;
    });

    var votesGroup = votesDim.group();
    var statusGroup = statusDim.group();


    //var colorScheme = ["#013369","#D50A0A","#008000","#FFA500","#FFFF00"];
    var colorScheme = ["#79CED7", "#66AFB2", "#C96A23", "#D3D1C5", "#F5821F"];

    ticketTypeChart = dc.rowChart("#ticketTypeChart");
    ticketChart = dc.rowChart("#ticketChart");
    votesChart = dc.rowChart("#votesChart");
    statusChart = dc.rowChart("#statusChart");

    ticketTypeChart
        .ordinalColors(colorScheme)
        .width(300)
        .height(300)
        .dimension(ticketTypeDim)
        .group(ticketTypeGroup)
        //.useViewBoxResizing(true)
        .elasticX(true)
        .xAxis().ticks(4);

    ticketChart
        .ordinalColors(colorScheme)
        .width(300)
        .height(300)
        .dimension(ticketDim)
        .group(ticketGroup)
        //.useViewBoxResizing(true)
        .elasticX(true)
        .xAxis().ticks(4);

    votesChart
        .ordinalColors(colorScheme)
        .width(300)
        .height(300)
        .dimension(ticketDim)
        .group(ticketVotesGroup)
        //.useViewBoxResizing(true)
        .elasticX(true)
        .xAxis().ticks(4);

    statusChart
        .ordinalColors(colorScheme)
        .width(300)
        .height(300)
        .dimension(statusDim)
        .group(statusGroup)
        //.useViewBoxResizing(true)
        .elasticX(true)
        .xAxis().ticks(4);

    dc.renderAll();
}*/

function makeWorkGraphs(error,workdata) {

    if (error) {
        console.error("makeGraphs in bug_graph error on receiving dataset:", error.statusText);
        throw error;
    }

    var ndx = crossfilter(workdata);

    //console.log(workdata);

    var dateFormat = d3.time.format("%Y-%m-%d").parse;

    var dateDim = ndx.dimension(function(d){
        return d3.time.day(dateFormat(d.date));
    });

    var weekDim = ndx.dimension(function(d){
        return d3.time.week(dateFormat(d.date));
    });

    var monthDim = ndx.dimension(function(d){
        return d3.time.month(dateFormat(d.date));
    });

    var ticketStatusDim = ndx.dimension(function(d){
       return d.ticket_status;
    });

    var ticketTypeDim = ndx.dimension(function(d){
       return d.ticket_type;
    });

    var ticketDim = ndx.dimension(function(d){
       return d.ticket_name;
    });

    var dateGroup = dateDim.group();

    var ticketHoursGroup = ticketDim.group().reduceSum(function(d){
        return d.hours;
    });

    var bugsPerMonthGroup = monthDim.group().reduceSum(function(d){
        return d.ticket_type=="Bug";
    });

    var bugsPerDayGroup = dateDim.group().reduceSum(function(d){
        return d.ticket_type=="Bug";
    });

    var featuresPerMonthGroup = monthDim.group().reduceSum(function(d){
        return d.ticket_type=="Feature";
    });

    var featuresPerDayGroup = dateDim.group().reduceSum(function(d){
        return d.ticket_type=="Feature";
    });

    var bugsPerWeekGroup = weekDim.group().reduceSum(function(d){
        return d.ticket_type=="Bug";
    });

    var featuresPerWeekGroup = weekDim.group().reduceSum(function(d){
        return d.ticket_type=="Feature";
    });

    var ticketStatusGroup = ticketStatusDim.group();
    var ticketTypeGroup = ticketTypeDim.group();

    monthChart = dc.barChart("#monthChart");
    dayChart = dc.barChart("#dayChart");
    weekChart = dc.barChart("#weekChart");
    statusChart = dc.rowChart("#statusChart");
    ticketTypeChart = dc.rowChart("#ticketTypeChart");
    ticketHoursChart = dc.rowChart("#ticketHoursChart");

    var minDate = new Date(dateDim.bottom(1)[0]["date"]);
    var maxDate = new Date();


    //var colorScheme = ["#013369","#D50A0A","#008000","#FFA500","#FFFF00"];
    var colorScheme = ["#79CED7", "#C96A23","#66AFB2", "#D3D1C5", "#F5821F"];

    monthChart
        .ordinalColors(colorScheme)
        .height(300)
        .width(1000)
        //.useViewBoxResizing(true)
        .dimension(monthDim)
        .x(d3.time.scale().domain([minDate, maxDate]))
        .xUnits(d3.time.months)
        .xAxisPadding(500)
        .group(bugsPerMonthGroup,"Bug")
        .stack(featuresPerMonthGroup,"Feature")
        .elasticX(true)
        .centerBar(true)
        .brushOn(true)
        .elasticY(true);

    monthChart
        .legend(dc.legend())
        .yAxis().ticks(4);

    dayChart
        .ordinalColors(colorScheme)
        .height(100)
        .width(1000)
        .dimension(dateDim)
        .x(d3.time.scale().domain([minDate, maxDate]))
        .xUnits(d3.time.days)
        .xAxisPadding(40)
        .group(bugsPerDayGroup,"Bug")
        .stack(featuresPerDayGroup,"Feature")
        .elasticX(true)
        .centerBar(true)
        .brushOn(false)
        .elasticY(true);

    dayChart.yAxis().ticks(2);

    weekChart
        .ordinalColors(colorScheme)
        .height(100)
        .width(1000)
        .dimension(dateDim)
        .x(d3.time.scale().domain([minDate, maxDate]))
        .xUnits(d3.time.weeks)
        .xAxisPadding(40)
        .group(bugsPerWeekGroup,"Bug")
        .stack(featuresPerWeekGroup,"Feature")
        .elasticX(true)
        .centerBar(true)
        .brushOn(false)
        .elasticY(true);

    weekChart.yAxis().ticks(2);


    statusChart
        .ordinalColors(colorScheme)
        .width(300)
        .height(300)
        .dimension(ticketStatusDim)
        .group(ticketStatusGroup)
        .elasticX(true)
        .xAxis().ticks(4);

    ticketTypeChart
        .ordinalColors(colorScheme)
        .width(300)
        .height(250)
        .dimension(ticketTypeDim)
        .group(ticketTypeGroup)
        .elasticX(true)
        .xAxis().ticks(4);

    ticketHoursChart
        .ordinalColors(colorScheme)
        .width(300)
        .height(300)
        .dimension(ticketDim)
        .group(ticketHoursGroup)
        .elasticX(true)
        .xAxis().ticks(4);

    dc.renderAll();
}