
document.addEventListener("DOMContentLoaded", () => {
  new ApexCharts(document.querySelector("#barChart"), {
    series: [{
      data: [400, 430, 300, 470, 400, 430, 448, 470, 400, 430, 448, 470,]
    }],
    chart: {
      type: 'bar',
      height: "437px"
    },
    plotOptions: {
      bar: {
        borderRadius: 4,
        vertical: true,
      }
    },
    dataLabels: {
      enabled: false
    },
    xaxis: {
      categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
        'Aug', 'Sept', 'Oct', 'Nov', 'Dec'
      ],
    }
  }).render();
});




document.addEventListener("DOMContentLoaded", () => {
  var budgetChart = echarts
    .init(document.querySelector("#budgetChart"))
    .setOption({
      legend: {
        data: ["Allocated Budget", "Actual Spending"],
      },
      radar: {
        // shape: 'circle',
        indicator: [
          {
            name: "Sales",
            max: 6500,
          },
          {
            name: "Administration",
            max: 16000,
          },
          {
            name: "Information Technology",
            max: 30000,
          },
          {
            name: "Customer Support",
            max: 38000,
          },
          {
            name: "Development",
            max: 52000,
          },
          {
            name: "Marketing",
            max: 25000,
          },
        ],
      },
      series: [
        {
          name: "Budget vs spending",
          type: "radar",
          data: [
            {
              value: [4200, 3000, 20000, 35000, 50000, 18000],
              name: "Allocated Budget",
            },
            {
              value: [
                5000, 14000, 28000, 26000, 42000, 21000,
              ],
              name: "Actual Spending",
            },
          ],
        },
      ],
    });
});
