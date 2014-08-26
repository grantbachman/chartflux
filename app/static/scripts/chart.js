function priceChart(ticker,company_name,importData){
  var ohlc = [],
      volume = [],
      sma = {
              'SMA50':[],
              'SMA200': []
            };
  for (var i=0; i < importData.length; i++){
    ohlc.push([
                importData[i]['Date'],
                importData[i]['Open'],
                importData[i]['High'],
                importData[i]['Low'],
                importData[i]['Close'],
    ]);
    volume.push([
                importData[i]['Date'],
                importData[i]['Volume'],
      ]);
    sma['SMA50'].push([importData[i]['Date'], importData[i]['sma50']])
    sma['SMA200'].push([importData[i]['Date'], importData[i]['sma200']])
  }
  $(function () {
    $('#chart').highcharts('StockChart', {
      rangeSelector: {
        selected: 1
      },
      chart: { zoomType: 'xy' },
      title: { text: company_name },
      legend: { enabled: true },
      xAxis: { type: 'datetime' },
      yAxis: [
          { // Primary yAxis
              title: {
                  text: ticker,
              },
              labels: {
                  format: '${value}',
              },
              height: '70%'
          },
          { // Secondary yAxis
              title: {
                  text: 'Volume',
              },
              top: '75%',
              height: '25%'
          }
        ],
        tooltip: { shared: true },
        series: [
        {
            name: ticker,
            type: 'candlestick',
            lineWidth: 1,
            data: ohlc,
            color: Highcharts.getOptions().colors[0]
        },
        {
            name: 'SMA 50',
            type: 'spline',
            data: sma['SMA50'],
            color: Highcharts.getOptions().colors[2]
        },
        {
            name: 'SMA 200',
            type: 'spline',
            data: sma['SMA200'],
            color: Highcharts.getOptions().colors[3]
        },
        {
            name: 'Volume',
            type: 'column',
            lineWidth: 1,
            yAxis: 1,
            data: volume,
            color: Highcharts.getOptions().colors[1]
        }
        ]
    });
    });
}

function rsiChart(ticker,company_name,importData){
  rsi = [];
  for (var i=0; i < importData.length; i++){
    rsi.push([
                importData[i]['Date'],
                importData[i]['RSI']
      ]);
  }
  $(function () {
          $('#chart').highcharts('StockChart', {
            rangeSelector: {
              selected: 1
            },
            chart: { zoomType: 'xy' },
            title: { text: company_name },
            legend: { enabled: true },
            xAxis: { type: 'datetime' },
            yAxis: [
                { // Primary yAxis
                    title: {
                        text: ticker + ' RSI'
                    },
                    labels: {
                        format: '{value}',
                    },
                    height: '100%',
                    min: 0,
                    max: 100,
                    plotLines : [
                      {
                        value : 70,
                        color : 'black',
                        dashStyle : 'shortdash',
                        width : 1,
                        label : { text : 'Approaching Overbought' }
                      },
                      {
                            value : 30,
                            color : 'black',
                            dashStyle : 'shortdash',
                            width : 1,
                        label : { text : 'Approaching Oversold' }
                        }
                    ]
                }
              ],
              tooltip: { shared: true },
              series: [
              {
                  name: 'RSI',
                  type: 'spline',
                  data: rsi,
                  color: Highcharts.getOptions().colors[0]
              }
              ]
          });
      });
}
function macdChart(ticker,company_name,importData){
  var macd = {
          'MACD': [],
          'MACD-Signal': [],
          'Histogram': []
  };
  for (var i=0; i < importData.length; i++){
          macd['MACD'].push([importData[i]['Date'], importData[i]['MACD']])
          macd['MACD-Signal'].push([importData[i]['Date'], importData[i]['MACD-Signal']])
          macd['Histogram'].push([importData[i]['Date'], importData[i]['MACD'] - importData[i]['MACD-Signal']])
  }
  $(function () {
          $('#chart').highcharts('StockChart', {
            rangeSelector: {
              selected: 1
            },
            chart: { zoomType: 'xy' },
            title: { text: company_name },
            legend: { enabled: true },
            xAxis: { type: 'datetime' },
            yAxis: [
                { // Primary yAxis
                    title: {
                        text: ticker + ' MACD'
                    },
                    labels: {
                        format: '{value}',
                    },
                    height: '100%'
                }
              ],
              tooltip: { shared: true },
              series: [
              {
                  name: 'MACD',
                  type: 'spline',
                  data: macd['MACD'],
                  color: 'black'
              },
              {
                  name: 'MACD-Signal',
                  type: 'spline',
                  data: macd['MACD-Signal'],
                  color: 'red'
              },
              {
                  name: 'Histogram',
                  type: 'column',
                  data: macd['Histogram']
              }
              ]
          });
      });
}
