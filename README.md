# ftx-data-fetcher
Download historical data for perps, futures and funding rates

Written quickly, this is mainly a tool for me.

Usage:
  - Arguments : 
        - type (prices, funding)
        - contract name
        - start date
        - end date
        - timeframe in seconds
        - batch size (limit of 5000 from ftx api)
        
      example:
        - download prices data:
              node .\main.js "prices" "DEFI-0326" "2019-01-01 00:00:00" "2021-02-17 00:00:00" "3600" "5000"
        - download funding rate data:
              node .\main.js "funding" "DEFI-PERP" "2019-01-01 00:00:00" "2021-02-20 00:00:00"
      
      
