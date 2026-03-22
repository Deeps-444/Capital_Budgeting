import React from "react";
import { Bar } from "react-chartjs-2";

function CashflowChart({ cashflows }) {
  if (!cashflows || cashflows.length === 0) return null;

  // extracting values
  const labels = cashflows.map((c) => `Year ${c.year}`);
  const yearly = cashflows.map((c) => c.cashflow);

  // Calculating cumulative
  const cumulative = [];
  yearly.reduce((acc, curr, i) => {
    cumulative[i] = acc + curr;
    return cumulative[i];
  }, 0);

  const data = {
    labels,
    datasets: [
      {
        type: "bar",
        label: "Yearly Cashflow",
        data: yearly,
        backgroundColor: "#22C55E",
      },
      {
        type: "line",
        label: "Cumulative Cashflow",
        data: cumulative,
        borderColor: "#0F172A",
        borderWidth: 2,
        tension: 0.4,
        yAxisID: "y",
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: function (value) {
            return `₹${value}`;
          },
        },
      },
    },
  };

  return <Bar data={data} options={options} />;
}

export default CashflowChart;
