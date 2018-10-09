/*queue()
    .defer(d3.json,"/ticket_serial/ticket/?format=json")
    .await(makeTicketGraphs);*/

/*queue()
    .defer(d3.json,"/polls/votes/?format=json")
    .await(makeVoteGraphs);*/

queue()
    .defer(d3.json,"/polls/options/?format=json")
    .await(makeOptionGraphs);

/*function makeTicketGraphs(error,ticketdata){
    if (error){
        console.error("makeGraphs in bug_graph error on receiving dataset:", error.statusText);
        throw error;
    }

    var ndx = crossfilter(ticketdata);

    var statusDim = ndx.dimension(function(d){
        return d.status;
    });

    var userDim = ndx.dimension(function(d){
        return d.user;
    });

    var statusGroup = statusDim.group();
    var userGroup = userDim.group();

    var colorScheme = ["#013369","#D50A0A","#008000","#FFA500","#FFFF00"];

    statusChart = dc.rowChart("#statusChart");
    userChart = dc.rowChart("#userChart");

    statusChart
        .ordinalColors(colorScheme)
        .width(300)
        .height(300)
        .dimension(statusDim)
        .group(statusGroup)
        .elasticX(true)
        .xAxis().ticks(4);

    userChart
        .ordinalColors(colorScheme)
        .width(300)
        .height(300)
        .dimension(userDim)
        .group(userGroup)
        .elasticX(true)
        .xAxis().ticks(4);

    dc.renderAll();
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

function makeOptionGraphs(error,optiondata){
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


    var colorScheme = ["#013369","#D50A0A","#008000","#FFA500","#FFFF00"];

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
}