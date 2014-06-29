function generateChart(ticker, importData){
  var parseDate = d3.time.format.iso.parse;
  var dataset = []
  // As COLIN[], COLOUT[], and colors[] are all related, I should turn this into
  // an object. But not today. I'm tired and going to bed.

  // COLIN are the possible columns that can exist
  var COLIN = ["Adj Close","Volume","sma20","sma50","sma200"]
  // COLOUT are the display names of the possible columns
  var COLOUT = [ticker,"Volume","SMA 20","SMA 50","SMA 200"]
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
    if (key=="Volume") { dataset[i]['bar'] = true }
    for (var j = 0; j < importData.length; j++){
      var date = importData[j]['Date'];
      var price = importData[j][lineLabelsIn[i]];
      dataset[i]['values'][j] = {};
      dataset[i]['values'][j]['x'] = parseDate(date);
      dataset[i]['values'][j]['y'] = price;
    };
  };

  nv.addGraph(function(){
    var colors = ['royalblue','lightgrey', 'green', 'orange', 'red'];
    var datasetLen = dataset[0]['values'].length
    var focusEnd = dataset[0]['values'][datasetLen - 1]['x']
    var focusStart = deltaMonth(focusEnd, -12) // 1 year ago

    var chart = nv.models.linePlusBarWithFocusChart()
                  .color(colors)
                  .interpolate("basis")
                  .brushExtent([focusStart,focusEnd])
                  /*
                  Due to a bug in NVD3 (I think), when formatting the right side
                  of the main chart(price) with a $ and adding two decimal
                  points, it gets applied to the tooltipContent for the left
                  side of the main chart(Volume). I might look into this
                  further to see what the real issue is, but until then, I'm
                  just hacking around it.
                  */
                  .tooltipContent(function(key, x, y, e, graph) {
                                    if (key.indexOf("Volume") > -1) {
                                        y = y.slice(1,-3)
                                    }
                                    return '<h3>' + key + '</h3>'
                                            + '<p>' +  y + ' on ' + x + '</p>'
                                  });
    chart.xAxis.tickFormat(function(d){ return d3.time.format('%b %e, %Y')(new Date(d))});
    chart.x2Axis.tickFormat(function(d){ return d3.time.format('%B %Y')(new Date(d))});
    chart.y2Axis.tickFormat(d3.format('$,.2f')); // Price on main chart, use $
    chart.y4Axis.tickFormat(d3.format('$,.2f')); // Price on focus chart, use $
    chart.y1Axis.tickFormat(d3.format('s')); // Volume on main chart, use SI-prefix
    chart.y3Axis.tickFormat(d3.format('s')); // Volume on focus chart, use SI-prefix

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
