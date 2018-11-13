queue()
    .defer(d3.json,"/rest/work/log/custom/?format=json")
    .await(makeWorkGraphs);

/* Creates all the graphs in the work dashboard */
function makeWorkGraphs(error,workdata) {

    if (error) {
        console.error("makeGraphs in bug_graph error on receiving dataset:", error.statusText);
        throw error;
    }

    var ndx = crossfilter(workdata);
    var dateFormat = d3.time.format("%Y-%m-%d").parse;

    workdata.forEach(function (d) {
        d.dd = dateFormat(d.date);
        d.day = d3.time.day(d.dd);
    });

    var dateDim = ndx.dimension(function(d){
        return d.day;
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

    var bugsPerDayGroup = dateDim.group().reduceSum(function(d){
        return d.ticket_type=="Bug";
    });

    var featuresPerDayGroup = dateDim.group().reduceSum(function(d){
        return d.ticket_type=="Feature";
    });

    var ticketStatusGroup = ticketStatusDim.group();
    var ticketTypeGroup = ticketTypeDim.group();

    focusChart = dc.barChart("#focusChart");
    overviewChart = dc.barChart("#overviewChart");
    statusChart = dc.rowChart("#statusChart");
    ticketTypeChart = dc.rowChart("#ticketTypeChart");
    ticketHoursChart = dc.rowChart("#ticketHoursChart");

    var minDate = new Date(dateDim.bottom(1)[0]["date"]);
    var maxDate = new Date();

    var colorScheme = d3.scale.ordinal().domain(["Bug","Feature"])
                                        .range(["#C96A23","#79CED7"]);

    var colorSchemeS = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628'];
    var colorSchemeBF = ["#C96A23","#79CED7"];

    overviewChart
        .ordinalColors(colorSchemeBF)
        .height(50)
        .dimension(dateDim)
        .group(bugsPerDayGroup,"Bug")
        .stack(featuresPerDayGroup,"Feature")
        .margins({top: 5, right: 20, bottom: 20, left: 20})
        .useViewBoxResizing(true)
        .x(d3.time.scale()
            .domain([minDate, maxDate])
        )
        .xUnits(d3.time.days)
        .elasticX(true)
        .centerBar(false)
        .brushOn(true)
        .elasticY(true);

    overviewChart
        .yAxis().ticks(1);

    focusChart
        .ordinalColors(colorSchemeBF)
        .dimension(dateDim)
        .group(bugsPerDayGroup,"Bug")
        .stack(featuresPerDayGroup,"Feature")
        .height(300)
        .margins({top: 50, right: 20, bottom: 30, left: 20})
        .mouseZoomable(true)
        .rangeChart(overviewChart)
        .transitionDuration(500)
        .useViewBoxResizing(true)
        .x(d3.time.scale()
            .domain([minDate, maxDate])
        )
        .xUnits(d3.time.days)
        .yAxisLabel("Tickets")

        .centerBar(true)
        .brushOn(false)
        .elasticY(true);

    focusChart
        .legend(dc.legend()
            .legendText(function (d) {return d.name;})
            .x(20)
            .y(5)
            .horizontal(true)
            .itemHeight(20)
        )
        .yAxis().ticks(4);

    statusChart
        .ordinalColors(colorSchemeS)
        .height(250)
        .dimension(ticketStatusDim)
        .group(ticketStatusGroup)
        .useViewBoxResizing(true)
        .elasticX(true)
        .xAxis().ticks(4);

    ticketTypeChart
        .colors(colorScheme)
        .height(250)
        .dimension(ticketTypeDim)
        .group(ticketTypeGroup)
        .useViewBoxResizing(true)
        .elasticX(true)
        .xAxis().ticks(4);

    ticketHoursChart
        .ordinalColors(colorSchemeS)
        .dimension(ticketDim)
        .group(ticketHoursGroup)
        .height(600)
        .useViewBoxResizing(true)
        .elasticX(true)
        .xAxis().ticks(4);

    dc.renderAll();
    showPage(false);
}