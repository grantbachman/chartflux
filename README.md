# Chartflux
### Yahoo/Google Finance, but better.

Things it currently does:
* Graphs a stock's chart along with it's 20/50/200 Day SMA (Simple Moving Average). It only displays a static view of the chart (~2 year chart).

Things it _could_ ultimately do:
* On individual company pages:
  * List out news articles that deal with the company via webscraping Google/Yahoo sites.
  * List out Positive/Negative indicators related to the stock. Write about what each indicator represents, how it's calculated, and why people see it as important. This could lead to a potential tutorial on technical analysis or overall stock market introduction tutorial.
* On the home page:
  * Show 'Hot Stocks' by checking the number of news articles written about a company or by it's percentage movement from the past couple days (or both). Checking the number of news articles will be tricky as I'll have to strike a balance with how often I check the sites.
  * Show 'Recommended Stocks'. I'll have to save off the number of Positive/Negative indicators for each stock each day (cron), and those with the highest positive/negative indicator ratio win out.
  * Perhaps an 'On the Verge' section, showing stocks that are about to trigger a major positive/negative indicator, like crossing above/below the 200 day moving average.
  * Chart pattern recognition. This would require delving into machine learning to identify chart patterns like the Head and Shoulders, Double Top/Bottom, Wedge, Triangle, etc.
