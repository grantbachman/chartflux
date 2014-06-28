function printChart(ticker, dataset){
var margin = {top: 20, bottom: 50, left: 50, right: 20}
var svgWidth = (window.innerWidth > 0 && window.innerWidth < 750) ? window.innerWidth : screen.width;
var svgWidth = svgWidth - margin.left - margin.right;
var svgHeight = svgWidth*.75 - margin.top - margin.bottom;
var parseDate = d3.time.format.iso.parse;
//var ticker = '{{ stock.ticker }}'
//var dataset = JSON.parse('{{ data }}');

var minDate = parseDate(dataset[0]['Date']);
var maxDate = parseDate(dataset[dataset.length - 1]['Date']);
var minPrice = d3.min(dataset, function(obj) { return d3.min([obj['Adj Close'],obj['sma20'],obj['sma50'],obj['sma200']]);});
var maxPrice = d3.max(dataset, function(obj) { return d3.max([obj['Adj Close'],obj['sma20'],obj['sma50'],obj['sma200']]);});

var xScale = d3.time.scale().domain([minDate,maxDate]).range([0, svgWidth]);
var xAxis = d3.svg.axis().scale(xScale).orient("bottom");

var yScale = d3.scale.linear()
               .domain([minPrice, maxPrice]).range([svgHeight, 0]).nice();
var yAxis = d3.svg.axis().scale(yScale).orient("left");

var svg = d3.select("#chart").append("svg")
            .attr("width", svgWidth + margin.left + margin.right)
            .attr("height", svgHeight + margin.left + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + ","
                                            + margin.right + ")")

svg.append("g")
   .attr("class", "x axis")
   .attr("transform", "translate(0," + svgHeight + ")")
   .call(xAxis)
   .selectAll("text")
   .style("text-anchor", "end")
   .attr("transform", "rotate(-65)");

var xGrid = svg.append("g")
   .attr("class", "x grid")
   .call(xAxis.tickSize(svgHeight,0,0).tickFormat(""))


function currencyFormat(d){
if (d < 10) { return d3.format("$.2f")(d) }
else { return d3.format("$.0f")(d) }
}
svg.append("g")
   .attr("class", "y axis")
   .call(yAxis.tickFormat(function(d) { return currencyFormat(d); }));


var yGrid = svg.append("g")
   .attr("class", "y grid")
   .call(yAxis.tickSize(-svgWidth,0,0).tickFormat(""));

// Hide the first grid line on each axis.
-   // They were covering up the axis lines
xGrid.select(".tick").attr("visibility", "hidden");
yGrid.select(".tick").attr("visibility", "hidden");

function createAndAppendLine(column, legendName, lineClass, linePos){
  if (typeof dataset[0][column] === 'undefined') {
      return;
  } else {
      var line = d3.svg.line()
             .x(function(d) { return xScale(parseDate(d['Date'])); })
             .y(function(d) { return yScale(d[column]); })
             .interpolate("linear");
      svg.append("path").attr("class", lineClass)
                        .attr("data-legend", legendName)
                        .attr("data-legend-pos", linePos)
                        .attr("d",line(dataset))

  }
}

createAndAppendLine('Adj Close', ticker, 'priceline', 1);
createAndAppendLine('sma20', '20 Day SMA', 'sma20line', 2);
createAndAppendLine('sma50', '50 Day SMA', 'sma50line', 3);
createAndAppendLine('sma200', '200 Day SMA', 'sma200line', 4);

svg.append("g").attr("class", "legend")
               .attr("transform", "translate(50,30)")
               .call(d3.legend)
}
