function generatePriceChart(ticker,company_name,importData){
  var dataset = {"Price" : [],
                 "Volume" : [],
                 "SMA20" : [],
                 "SMA50" : [],
                 "SMA200" : [],
                 "RSI" : [],
                 "MACD": [],
                 "MACD-Signal": []
                };
  for (var i=0; i < importData.length; i++){
    dataset["Price"].push([importData[i]["Date"], importData[i]["Adj Close"]]);
    dataset["Volume"].push([importData[i]["Date"], importData[i]["Volume"]]);
    dataset["SMA20"].push([importData[i]["Date"], importData[i]["sma20"]]);
    dataset["SMA50"].push([importData[i]["Date"], importData[i]["sma50"]]);
    dataset["SMA200"].push([importData[i]["Date"], importData[i]["sma200"]]);
    dataset["RSI"].push([importData[i]["Date"], importData[i]["RSI"]]);
    dataset["MACD"].push([importData[i]["Date"], importData[i]["MACD"]]);
    dataset["MACD-Signal"].push([importData[i]["Date"], importData[i]["MACD-Signal"]]);

  }
  $(function(){
    $('#chart').highcharts('StockChart', {
          rangeSelector : { selected : 1, inputEnabled: $('#chart').width() > 480 },
        //	chart : { height: "70%", width: "70%" },
          title : { text : company_name },
          rangeSelector : { selected: 4 }, // Default to 1 year view
          tooltip : {
                    },
          yAxis: [{
                    labels: { align: 'right', x: -3 },
                    title: { text: ticker },
                    height: '40%',
                  },
                  {
                    labels: { align: 'right', x: -3 },
                    title: { text: 'RSI' },
                    top : '40%',
                    height: '20%',
                  },
                  {
                    labels: { align: 'right', x: -3 },
                    title: { text: 'MACD' },
                    top: '60%',
                    height: '20%',
                    offset: 0,
                    lineWidth: 1
                  },
                  {
                    labels: { align: 'right', x: -3 },
                    title: { text: 'Volume' },
                    top: '80%',
                    height: '20%',
                    offset: 0,
                    lineWidth: 2
                  }],
          series: [{
                    name: ticker,
                    data: dataset["Price"],
                    lineWidth: 3,
                    yAxis: 0,
                    zIndex: 3,
                  },
                  {
                    name: 'SMA 20',
                    data: dataset["SMA20"],
                    lineWidth: 1,
                    yAxis: 0,
                    zIndex: 2,
                  },
                  {
                    name: 'SMA 50',
                    data: dataset["SMA50"],
                    lineWidth: 1,
                    yAxis: 0,
                    zIndex: 1,
                  },
                  {
                    name: 'SMA 200',
                    data: dataset["SMA200"],
                    lineWidth: 1,
                    yAxis: 0,
                    zIndex: 0,
                  },
                  {
                    name: 'RSI',
                    data: dataset["RSI"],
                    lineWidth: 1,
                    yAxis: 1
                  },
                  {
                    name: 'MACD',
                    data: dataset['MACD'],
                    lineWidth: 1,
                    yAxis: 2
                  },
                  {
                    name: 'MACD-Signal',
                    data: dataset['MACD-Signal'],
                    lineWidth: 1,
                    yAxis: 2
                  },
                  {
                    type: 'column',
                    name: 'Volume',
                    data: dataset["Volume"],
                    yAxis: 3,
                  }]
          });
    });
};
