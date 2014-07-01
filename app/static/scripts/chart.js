function generateChart(ticker,company_name,importData){
  var dataset = {"Price" : [],
                 "Volume" : [],
                 "SMA20" : [],
                 "SMA50" : [],
                 "SMA200" : [],
                };
  for (var i=0; i < importData.length; i++){
    dataset["Price"].push([importData[i]["Date"], importData[i]["Adj Close"]]);
    dataset["Volume"].push([importData[i]["Date"], importData[i]["Volume"]]);
    dataset["SMA20"].push([importData[i]["Date"], importData[i]["sma20"]]);
    dataset["SMA50"].push([importData[i]["Date"], importData[i]["sma50"]]);
    dataset["SMA200"].push([importData[i]["Date"], importData[i]["sma200"]]);
  }
  $(function(){
    $('#chart').highcharts('StockChart', {
          rangeSelector : { selected : 1, inputEnabled: $('#chart').width() > 480 },
        //	chart : { height: "70%", width: "70%" },
          title : { text : company_name },
          yAxis: [{
                    labels: { align: 'right', x: -3 },
                    title: { text: ticker },
                    height: '80%',
                  },
                  {
                    labels: { align: 'right', x: -3 },
                    title: { text: 'Volume' },
                    top: '85%',
                    height: '15%',
                    offset: 0,
                    lineWidth: 2
                  }],
          series: [{
                    type: 'spline',
                    name: ticker,
                    data: dataset["Price"],
                    lineWidth: 3,
                    yAxis: 0,
                    zIndex: 3,
                  },
                  {
                    type: 'spline',
                    name: 'SMA 20',
                    data: dataset["SMA20"],
                    lineWidth: 1,
                    yAxis: 0,
                    zIndex: 2,
                  },
                  {
                    type: 'spline',
                    name: 'SMA 50',
                    data: dataset["SMA50"],
                    lineWidth: 1,
                    yAxis: 0,
                    zIndex: 1,
                  },
                  {
                    type: 'spline',
                    name: 'SMA 200',
                    data: dataset["SMA200"],
                    lineWidth: 1,
                    yAxis: 0,
                    zIndex: 0,
                  },
                  {
                    type: 'column',
                    name: 'Volume',
                    data: dataset["Volume"],
                    yAxis: 1,
                  }]
          });
    });
};
