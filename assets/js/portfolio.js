// Generate random colors as HexCode
function randomColor() {
    let letters = "0123456789ABCDEF";
    let color = "#";
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

// Get the canvas element
let ctx = document.getElementById("portfolio-chart").getContext("2d");

// Store portfolio data from table
let portfolioData = {
    stocks: [],
    Dates: [],
    quantities: [],
    bougthPrice: [],
    currentPrice: [],
    returnsPercent: [],
    returnsDollar: [],
    totals: []
}

// Get table data from html
let table = document.getElementById("portfolio-table");
let rows = table.getElementsByTagName("tr");
let stocks = [];
let quantities = [];
let totals = [];
let colors = [];
for (let i = 1; i < rows.length; i++) {
    let cells = rows[i].getElementsByTagName("td");
    stocks.push(cells[0].innerHTML);
    totals.push(cells[7].innerHTML);
    colors.push(randomColor());
}

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

// Create the chart data
let data = {
	labels: stocks,
	datasets: [
		{
			label: " totals",
			data: totals,
			backgroundColor: defaultColors,
		},
	],
};

// Create the pie chart
let myChart = new Chart(ctx, {
	type: "pie",
	data: data,
});
