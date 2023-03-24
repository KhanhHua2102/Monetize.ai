// Generate random colors as HexCode
function randomColor() {
    let letters = "0123456789ABCDEF";
    let color = "#";
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

// Convert portfolioData to CSV
function convertToCSV(data) {
    let csv = "Stock,Date,Quantity,Bought Price,Current Price,Returns Percent,Returns Dollar,Totals";
    data.forEach(function(row) {
        csv += row.stocks + ',' + row.dates + ',' + row.quantities + ',' + row.bougthPrice + ',' + row.currentPrice + ',' + row.returnsPercent + ',' + row.returnsDollar + ',' + row.totals + "\r";
    });
    return csv;
}

// Download CSV file
function downloadCSV(data) {
    let csv = convertToCSV(data);
    let blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    let link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = 'portfolio.csv';
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Export CSV file when button is clicked
function exportCSV() {
    let exportButton = document.getElementById("export-button");
    exportButton.addEventListener("click", function() {
        downloadCSV(portfolioData);
    });
}

// Get the canvas element
let ctx = document.getElementById("portfolio-chart").getContext("2d");

let portfolioData = {
    stocks: [],
    dates: [],
    quantities: [],
    bougthPrice: [],
    currentPrice: [],
    returnsPercent: [],
    returnsDollar: [],
    totals: []
}

// Get table data for portfolioData
let table = document.getElementById("portfolio-table");
let rows = table.getElementsByTagName("tr");
for (let i = 1; i < rows.length; i++) {
    let cells = rows[i].getElementsByTagName("td");
    portfolioData.stocks.push(cells[0].innerHTML);
    portfolioData.dates.push(cells[1].innerHTML);
    portfolioData.quantities.push(cells[2].innerHTML);
    portfolioData.bougthPrice.push(cells[3].innerHTML);
    portfolioData.currentPrice.push(cells[4].innerHTML);
    portfolioData.returnsPercent.push(cells[5].innerHTML);
    portfolioData.returnsDollar.push(cells[6].innerHTML);
    portfolioData.totals.push(cells[7].innerHTML);
}

// Default colors for piechart
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

// Create the pie chart
let myChart = new Chart(ctx, {
	type: "pie",
	data: {
		labels: portfolioData.stocks,
		datasets: [
			{
				label: " totals",
				data: portfolioData.totals,
				backgroundColor: defaultColors,
			},
		],
	},
});
