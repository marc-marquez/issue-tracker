queue()
    .defer(d3.json,"/rest/work/log/custom/?format=json")
    .await(makeWorkGraphs);

/*function zoom(svg){
    const extent = [[margin.left, margin.top],[width-margin.right,height-margin.top]];

    svg.call(d3.zoom()
        .scaleExtent([1,8])
        .translateExtent(extent)
        .extent(extent)
        .on("zoom",zoomed));

    function zoomed(){
        x.range([margin.left,width-margin.right].map(d=> d3.event.transform.applyX(d)));
        svg.selectAll(".bars rect").attr("x",d=>x(d.date)).attr("width",x.bandwidth());
        svg.selectAll(".x-axis").call(xAxis);
    }
}

function zoomableBarChart(chart){
    var width = chart.effectiveWidth() - chart.margin.left - chart.margin.right;
    var height = chart.effectiveHeight() - chart.margin.top - chart.margin.bottom;
    var marginOv = {top:500,right:chart.margin.right,bottom:20,left:chart.margin.left};
    var heightOv = 500 - marginOv.top - marginOv.bottom;

    var x = d3.time.scale().range([0,width]);
    var y = d3.scale.linear().range([height,0]);
    var xOv = d3.time.scale().range([0,width]);
    var yOv = d3.scale.linear().range([heightOv,0]);

    var xAxis = d3.svg.axis().scale(x).orient("bottom");
    var yAxis = d3.svg.axis().scale(y).orient("left");
    var xAxisOv = d3.svg.axis().scale(xOv).orient("bottom");

    var chartBody = chart.select("g");
}*/

function makeWorkGraphs(error,workdata) {

    if (error) {
        console.error("makeGraphs in bug_graph error on receiving dataset:", error.statusText);
        throw error;
    }

    var ndx = crossfilter(workdata);

    //console.log(workdata);

    //var dateFormatSpecifier = "%Y-%m-%d";
    var dateFormat = d3.time.format("%Y-%m-%d").parse;
    /*var dateFormatParser = d3.timeParse(dateFormatSpecifier);*/

    workdata.forEach(function (d) {
        d.dd = dateFormat(d.date);
        //d.month = d3.time.month(d.dd);
        d.day = d3.time.day(d.dd);
        //d.year = d3.time.year(d.dd);
        //d.week = d3.time.week(d.dd);
    });

    var dateDim = ndx.dimension(function(d){
        //return d3.time.day(dateFormat(d.date));
        return d.day;
    });

    /*var weekDim = ndx.dimension(function(d){
        //return d3.time.week(dateFormat(d.date));
        return d.week;
    });

    var monthDim = ndx.dimension(function(d){
        //return d3.time.month(dateFormat(d.date));
        return d.month;
    });*/

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

    /*var bugsPerMonthGroup = monthDim.group().reduceSum(function(d){
        return d.ticket_type=="Bug";
    });*/

    var bugsPerDayGroup = dateDim.group().reduceSum(function(d){
        return d.ticket_type=="Bug";
    });

    /*var featuresPerMonthGroup = monthDim.group().reduceSum(function(d){
        return d.ticket_type=="Feature";
    });*/

    var featuresPerDayGroup = dateDim.group().reduceSum(function(d){
        return d.ticket_type=="Feature";
    });

    /*var bugsPerWeekGroup = weekDim.group().reduceSum(function(d){
        return d.ticket_type=="Bug";
    });

    var featuresPerWeekGroup = weekDim.group().reduceSum(function(d){
        return d.ticket_type=="Feature";
    });*/

    var ticketStatusGroup = ticketStatusDim.group();
    var ticketTypeGroup = ticketTypeDim.group();

    focusChart = dc.barChart("#focusChart");
    overviewChart = dc.barChart("#overviewChart");
    //weekChart = dc.barChart("#weekChart");
    statusChart = dc.rowChart("#statusChart");
    ticketTypeChart = dc.rowChart("#ticketTypeChart");
    ticketHoursChart = dc.rowChart("#ticketHoursChart");

    var minDate = new Date(dateDim.bottom(1)[0]["date"]);
    var maxDate = new Date();
    //console.log("min: "+minDate+",max: "+maxDate);

    //var minWeekDate = new Date(2018,10,01);
    //var maxWeekDate = new Date(2018,10,31);


    //var colorSchemeS = ["#013369","#D50A0A","#008000","#FFA500","#FFFF00"];
    //var colorScheme = ["#79CED7", "#C96A23","#66AFB2", "#D3D1C5", "#F5821F"];
    //var colorScheme = ["#A07A19", "#AC30C0", "#EB9A72", "#BA86F5", "#EA22A8"];

    /*var colorScheme = d3.scale.ordinal().domain(["Bug","Feature"])
                                        .range(["#79CED7", "#C96A23"]);*/

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
        //.xAxisLabel("Number of Tickets")
        .xAxis().ticks(4);

    ticketTypeChart
        .ordinalColors(colorSchemeBF)
        //.width(300)
        .height(250)
        .dimension(ticketTypeDim)
        .group(ticketTypeGroup)
        .useViewBoxResizing(true)
        .elasticX(true)
        //.xAxisLabel("Number of Tickets")
        .xAxis().ticks(4);

    ticketHoursChart
        .ordinalColors(colorSchemeS)
        .dimension(ticketDim)
        .group(ticketHoursGroup)
        /*.colorAccessor(function(d){
            console.log(d);
        }
        .colors(d3.scale.ordinal().domain([0,1])
            .range(["#79CED7", "#C96A23"]))*/
        //.width(300)
        .height(600)
        .useViewBoxResizing(true)
        .elasticX(true)
        //.xAxisLabel("Hours")
        .xAxis().ticks(4);


    dc.renderAll();
    showPage();
}