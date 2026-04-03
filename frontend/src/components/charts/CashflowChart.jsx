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
        borderRadius: 6,
        barThickness: 30,
      },
      {
        type: "line",
        label: "Cumulative Cashflow",
        data: cumulative,
        borderColor: "#1E293B",
        borderWidth: 2,
        tension: 0.4,
        pointRadius: 3,
        pointBackgroundColor: "#1E293B",
        yAxisID: "y",
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
        labels: {
          color: "#475569", // slate-600
          font: {
            size: 12,
          },
        },
      },
    },
    scales: {
      x: {
        grid: {
          display: false, // cleaner UI
        },
        ticks: {
          color: "#64748B", // slate-500
        },
      },
      y: {
        beginAtZero: true,
        grid: {
          color: "#E2E8F0", // subtle grid
        },
        ticks: {
          color: "#64748B",
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
