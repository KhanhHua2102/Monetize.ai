/*
  This is the Portfolio.js file, which contains JavaScript code for handling portfolio-related functionality.
  It uses jQuery and Chart.js to interact with the DOM and create charts.
  The code includes functions for exporting portfolio data as a CSV file and creating a pie chart using Chart.js.
*/
$(document).ready(function () {
	// Event handler for export CSV button click
	$('.download-csv button').click(function () {
	  console.log("export csv button clicked");
	  exportCSV();
	});
  });
  
  // Define table data for the portfolio
  let portfolioData = {
	stocks: [],
	dates: [],
	quantities: [],
	bougthPrice: [],
	currentPrice: [],
	returnsPercent: [],
	returnsDollar: [],
	totals: []
  };
  
  // Get table data for portfolioData
  let table = $("#portfolio-table");
  let rows = table.find("tr");
  for (let i = 1; i < rows.length; i++) {
	let cells = $(rows[i]).find("td");
	portfolioData.stocks.push(cells[0].innerHTML);
	portfolioData.dates.push(cells[1].innerHTML);
	portfolioData.quantities.push(cells[2].innerHTML);
	portfolioData.bougthPrice.push(cells[3].innerHTML);
	portfolioData.currentPrice.push(cells[4].innerHTML);
	portfolioData.returnsPercent.push(cells[5].innerHTML);
	portfolioData.returnsDollar.push(cells[6].innerHTML);
	portfolioData.totals.push(cells[7].innerHTML);
  }
  
  // Default colors for the pie chart
  let defaultColors = [
	"rgb(54, 162, 235)",
	"rgb(75, 192, 192)",
	"rgb(255, 205, 86)",
	"rgb(255, 99, 132)",
	"rgb(201, 203, 207)",
	"rgb(255, 159, 64)",
	"rgb(30, 144, 255)",
	"rgb(0, 128, 0)",
	"rgb(255, 215, 0)",
	"rgb(128, 0, 0)",
  ];
  
  // Get the canvas element for the pie chart
  let ctx = $("#portfolio-chart")[0].getContext("2d");
  
  // Remove the $ symbol from return ($) and totals
  let totals = [];
  for (let i = 0; i < portfolioData.stocks.length; i++) {
	totals[i] = portfolioData.totals[i].substring(1);
  }
  
  // Create the pie chart using Chart.js
  let myChart = new Chart(ctx, {
	type: "pie",
	data: {
	  labels: portfolioData.stocks,
	  datasets: [
		{
		  label: "totals",
		  data: totals,
		  backgroundColor: defaultColors,
		},
	  ],
	},
});

/**
 * Export portfolioData to CSV file
 */
function exportCSV() {
    let csv = convertToCSV(portfolioData);
    let blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
	let link = $('<a>').attr({
	  href: URL.createObjectURL(blob),
	  download: "portfolio.csv",
	  style: "display: none",
	});
	$().append(link);
	link[0].click();
	$().remove(link);
}

/**
 * Convert portfolioData to CSV format
 * @param data 
 * @returns csv
 */
function convertToCSV(data) {
    let csv = "Stock,Date,Quantity,Bought Price,Current Price,Returns Percent,Returns Dollar,Totals\r";
    for (let i = 0; i < data.stocks.length; i++) {
        csv +=
					data.stocks[i] +
					"," +
					data.dates[i] +
					"," +
					data.quantities[i] +
					"," +
					data.bougthPrice[i] +
					"," +
					data.currentPrice[i] +
					"," +
					data.returnsPercent[i] +
					"," +
					data.returnsDollar[i] +
					"," +
					data.totals[i] +
					"\r";
    }
    return csv;
}
