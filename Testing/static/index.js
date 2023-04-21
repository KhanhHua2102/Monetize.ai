
       function addStock() {
  
        const inputElement = document.createElement("input");
        inputElement.setAttribute("type", "text");
        inputElement.setAttribute("name", "myInput"); 
        inputElement.required = true;
       
        inputElement.required = true;
        const myDiv = document.getElementById("message");
           myDiv.appendChild(inputElement); 
        
    var table = document.querySelector("table");
    var row = table.insertRow(-1);
    var tickerSymbol = row.insertCell(0);
    var selectedDate = row.insertCell(1);
    var endDate = row.insertCell(2);
    var companyName = row.insertCell(3);
    var startClosePrice = row.insertCell(4);
    var endClosePrice = row.insertCell(5);
    var shares = row.insertCell(6);
    var profit = row.insertCell(7);
   
   
   

    tickerSymbol.innerHTML = '<input type="text" name="ticker_symbol" required>';
    selectedDate.innerHTML = '<input type="date" name="selected_date" required>';
    endDate.innerHTML = '<input type="date" name="end_date" required>';
    companyName.innerHTML = '';
    startClosePrice.innerHTML = '';
    endClosePrice.innerHTML = '';
    shares.innerHTML = '<input type="number" name="Shares" required>';
    profit.innerHTML = '';
    message.innerHTML ='<input type="text">';

    // add event listener for the new row's submit button
    var submitButton = document.createElement("button");
    submitButton.textContent = "Result";
    submitButton.onclick = function() {
        // get input values from the new row
        var tickerSymbolValue = tickerSymbol.querySelector("input").value;
        var selectedDateValue = selectedDate.querySelector("input").value;
        var endDateValue = endDate.querySelector("input").value;
        var sharesValue = shares.querySelector("input").value;

        tickerSymbol.querySelector("input").disabled = true;
        selectedDate.querySelector("input").disabled = true;
        endDate.querySelector("input").disabled = true;

        // make API call to get stock data
        fetch(`/get_stock_data?ticker_symbol=${tickerSymbolValue}&selected_date=${selectedDateValue}&end_date=${endDateValue}`)
        .then(response => response.json())
        .then(data => {
            // fill in the missing values for the new row
            companyName.textContent = data.company_name;
            startClosePrice.textContent = data.start_close_price.toFixed(2);
            endClosePrice.textContent = data.end_close_price.toFixed(2);
            shares.textContent = sharesValue;
            profit.textContent = ((data.end_close_price - data.start_close_price) * sharesValue).toFixed(2);
        })
        .catch(error => console.log(error));
    }

    profit.appendChild(submitButton);

    // attach event listener to the new button
    submitButton.addEventListener('click', function(e) {
        e.preventDefault();
        submitButton.click();
    });

}
function calculateTotalProfit() {
  var totalProfit = 0;
  var profitCells = document.querySelectorAll("td:nth-child(8)");

  for (var i = 0; i < profitCells.length; i++) {
    totalProfit += parseFloat(profitCells[i].textContent);
  }

  document.getElementById("total-profit").textContent = totalProfit.toFixed(2);
}

