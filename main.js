const async = require("async");
const axios = require("axios");
const fs = require("fs");
const { Parser } = require("json2csv");
const path = require('path');

// example: https://ftx.com/api/funding_rates?start_time=1577854800&end_time=1580580752&future=BTC-PERP
const fundingRatesUrl = "https://ftx.com/api/funding_rates"
// example: https://ftx.com/api/markets/BTC-PERP/candles?resolution=3600&limit=5000&start_time=1546300800&end_time=1580580752
const futuresPricesUrl = "https://ftx.com/api/markets"

/**
 * Downloads the funding rates
 * @param {*} ticker 
 * @param {*} startDate 
 * @param {*} endDate 
 */
function getFundingRates(ticker, startDate, endDate) {
    let startTimestamp = (new Date(startDate)).getTime() / 1000;
    let endTimestamp = (new Date(endDate)).getTime() / 1000;

    // We need to fetch data in batches of 500, so we fetch every 500 hours
    const timestep = 500 * 60 * 60;
    let timestamp = startTimestamp;
    let nextTimestamp;
    let rates = [];
    let nbrOfBatches = Math.ceil((endTimestamp - startTimestamp) / 60 / 60 / 500) + 1;
    let batch = 0;

    async.whilst(
        function test(cb) {
            cb(null, batch < nbrOfBatches);
        },
        function iter(callback) {
            nextTimestamp = timestamp + timestep;
            if (nextTimestamp > endTimestamp && endTimestamp - timestamp > 0) {
                nextTimestamp = timestamp + endTimestamp - timestamp;
            }

            let url = fundingRatesUrl + "?start_time=" + timestamp + "&end_time=" + nextTimestamp + "&future=" + ticker;
            axios.get(url)
                .then(function (response) {
                    rates = rates.concat(response.data.result);
                    batch++;
                    timestamp = nextTimestamp
                    console.log("Batch " + batch + " of " + nbrOfBatches);
                    callback(null, rates);
                });
        },
        function end(err, fundingRates) {
            if (err) {
                console.log(err);
            } else {
                // Save rates as CSV
                exportCsv(ticker + "_rates", fundingRates);
                console.log("Saved to CSV");
            }
        }
    )

}

function getPrices(ticker, startDate, endDate, resolution, limit) {
    resolution = parseInt(resolution);
    limit = parseInt(limit);
    let startTimestamp = (new Date(startDate)).getTime() / 1000;
    let endTimestamp = (new Date(endDate)).getTime() / 1000;

    // Execute in batches
    const timestep = limit * resolution;
    let timestamp = startTimestamp;
    let nextTimestamp;
    let prices = [];
    let nbrOfBatches = Math.ceil((endTimestamp - startTimestamp) / resolution / limit) + 1;
    let batch = 0;

    async.whilst(
        function test(cb) {
            cb(null, batch < nbrOfBatches);
        },
        function iter(callback) {
            nextTimestamp = timestamp + timestep;
            if (nextTimestamp > endTimestamp && endTimestamp - timestamp > 0) {
                nextTimestamp = timestamp + endTimestamp - timestamp;
            }

            let url = futuresPricesUrl + "/" + ticker + "/candles?resolution=" + resolution + "&limit=" + limit + "&start_time=" + timestamp + "&end_time=" + nextTimestamp;
            axios.get(url)
                .then(function (response) {
                    prices = prices.concat(response.data.result);
                    batch++;
                    timestamp = nextTimestamp
                    console.log("Batch " + batch + " of " + nbrOfBatches);
                    callback(null, prices);
                });
        },
        function end(err, prices) {
            if (err) {
                console.log(err);
            } else {
                // Save rates as CSV
                if (prices.length > 0) {
                    exportCsv(ticker + "_prices", prices);
                    console.log("Saved to CSV");
                } else {
                    console.log("No data found");
                }
            }
        }
    )
}

function exportCsv(filename, data) {
    const filepath = path.join(__dirname, filename + ".csv");
    const parser = new Parser();
    const csv = parser.parse(data);
    fs.writeFileSync(filepath, csv);
}

// Main
let args = process.argv.slice(2);
switch (args[0]) {
    case "funding":
        getFundingRates(args[1], args[2], args[3]);
        break
    case "prices":
        getPrices(args[1], args[2], args[3], args[4], args[5]);
}

