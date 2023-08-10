const renderChart = (data, labels) => {
    var ctx = document.getElementById("myChartExpensesMonthly").getContext("2d");
    var myChartMonthly = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Monthly",
            data: data,
            backgroundColor: [
              "rgba(31, 45, 87, 1)",

            ],
            borderColor: [
              "rgba(31, 45, 87, 1)",
   
            ],
            borderWidth: 1,
          },
        ],
      },
      options: {
        title: {
          display: true,
          text: "Income per Expenses",
        },
      },
    });
  };
  
  const getChartData = () => {
    console.log("fetching");
    fetch("expenses_monthly_summary")
      .then((res) => res.json())
      .then((results) => {
        console.log("results", results);
        const source_data = results.expenses_monthly_data;
        const [labels, data] = [
          Object.keys(source_data),
          Object.values(source_data),
        ];
          renderChart(data, labels);
      });
  };
  

  document.onload = getChartData();



const renderChart2 = (data, labels) => {
  var ctx = document.getElementById("myChartexpensesLastweek").getContext("2d");
  var myChartLastweek = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Expense",
          data: data,
          backgroundColor: [
            "rgba(255,240,0,0.8",
            
          ],
          borderColor: [
            "rgba(31, 45, 87, 0.1)",
           
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      title: {
        display: true,
        text: "Expenses last week",
      },
    },
  });
};

const getChartData2 = () => {
  console.log("fetching");
  fetch("expenses_lastweek_summary")
    .then((res) => res.json())
    .then((results) => {
      console.log("results", results);
      const source_data = results.expenses_lastweek_data;
      const [labels, data] = [
        Object.keys(source_data),
        Object.values(source_data),
      ];
        renderChart2(data, labels);
    });
};
  
document.onload = getChartData2();