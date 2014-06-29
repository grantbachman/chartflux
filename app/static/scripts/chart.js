function generateChart(ticker, importData){
  var parseDate = d3.time.format.iso.parse;
  var dataset = []
  // COLIN are the possible columns that can exist
  var COLIN = ["Adj Close","sma20","sma50","sma200"]
  // COLOUT are the display names of the possible columns
  var COLOUT = [ticker,"SMA 20","SMA 50","SMA 200"]
  // lineLabelsIn/Out are arrays containing the LINESPACEIN/OUT columns
  // that actually exist in the data
  var lineLabelsIn = [], lineLabelsOut = [];
  for (var i = 0; i < COLIN.length; i++){
    if (COLIN[i] in importData[0]){
      lineLabelsIn.push(COLIN[i])
      lineLabelsOut.push(COLOUT[i])
    };
  };

  // Mold data into a shape that NVD3 can interpret
  for (var i = 0; i < lineLabelsIn.length; i++){
    var key = lineLabelsOut[i]
    dataset[i] = {};
    dataset[i]['key'] = key;
    dataset[i]['values'] = [];
    for (var j = 0; j < importData.length; j++){
      var date = importData[j]['Date'];
      var price = importData[j][lineLabelsIn[i]];
      dataset[i]['values'][j] = {};
      dataset[i]['values'][j]['x'] = parseDate(date);
      dataset[i]['values'][j]['y'] = price;
    };
  };

  nv.addGraph(function(){
    var colors = ['royalblue', 'green', 'orange', 'red'];
    var datasetLen = dataset[0]['values'].length
    var focusEnd = dataset[0]['values'][datasetLen - 1]['x']
    var focusStart = deltaMonth(focusEnd, -12) // 1 year ago

    var chart = nv.models.lineWithFocusChart()
                  .color(colors)
                  .interpolate("basis")
                  .brushExtent([focusStart,focusEnd])
                  .tooltipContent(function(key, x, y, e, graph) {
                                    return '<h3>' + key + '</h3>'
                                            + '<p>$' +  y + ' on ' + x + '</p>'
                                  });

    chart.xAxis.tickFormat(function(d){ return d3.time.format('%b %e, %Y')(new Date(d))});
    chart.yAxis.tickFormat(d3.format(',.2f'));
    chart.x2Axis.tickFormat(function(d){ return d3.time.format('%B %Y')(new Date(d))});
    chart.y2Axis.tickFormat(d3.format('0f'));

    d3.select('#chart svg').datum(dataset).call(chart);
    nv.utils.windowResize(chart.update);
    return chart;
  });

  return dataset;
};

function deltaMonth(date, months){
  var returnDate = new Date();
  returnDate.setMonth(date.getMonth() + months);
  return returnDate;
};
