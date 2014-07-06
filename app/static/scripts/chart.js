function generatePriceChart(ticker,company_name,importData){
  var dataset = {"Price" : [],
                 "Volume" : [],
                 "SMA50" : [],
                 "SMA200" : [],
                 "RSI" : [],
                 "MACD": [],
                 "MACD-Signal": []
                };
  for (var i=0; i < importData.length; i++){
    dataset["Price"].push([importData[i]["Date"], importData[i]["Adj Close"]]);
    dataset["Volume"].push([importData[i]["Date"], importData[i]["Volume"]]);
    dataset["SMA50"].push([importData[i]["Date"], importData[i]["sma50"]]);
    dataset["SMA200"].push([importData[i]["Date"], importData[i]["sma200"]]);
    dataset["RSI"].push([importData[i]["Date"], importData[i]["RSI"]]);
    dataset["MACD"].push([importData[i]["Date"], importData[i]["MACD"]]);
    dataset["MACD-Signal"].push([importData[i]["Date"], importData[i]["MACD-Signal"]]);
  }
$(function () {
        $('#chart').highcharts({
            chart: {
                zoomType: 'xy'
            },
            title: { text: company_name  },
          xAxis: { type: 'datetime' },
            yAxis: [
              { // Primary yAxis
                  title: {
                      text: ticker,
                      style: { color: Highcharts.getOptions().colors[0] }
                  },
                  labels: {
                      format: '${value}',
                      style: { color: Highcharts.getOptions().colors[0] }
                  },
                  opposite: true
              },
              { // Secondary yAxis
                  labels: { style: { color: Highcharts.getOptions().colors[1] } },
                  title: {
                      text: 'Volume',
                      style: { color: Highcharts.getOptions().colors[1] }
                  }
              }
            ],
            tooltip: { shared: true },
            series: [
            {
                name: 'Price',
                type: 'spline',
                data: dataset['Price']
            },
            {
                name: 'Volume',
                type: 'column',
                yAxis: 1,
                data: dataset['Volume'],
            }
            ]
        });
    });
}
