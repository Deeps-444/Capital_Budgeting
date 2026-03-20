import React from "react";
import { Bar } from "react-chartjs-2";

function CashflowChart({ cashflows }) {
  // cumulative cashflow
  let cumulative = [];
  cashflows.reduce((acc, curr, i) => {
    cumulative[i] = acc + curr;
    return cumulative[i];
  }, 0);

  const data = {
    labels: cashflows.map((_, i) => `Year ${i + 1}`),
    datasets: [
      {
        type: "bar",
        label: "Yearly Cashflow",
        data: cashflows,
        backgroundColor: "#22C55E",
      },
      {
        type: "line",
        label: "Cumulative Cashflow",
        data: cumulative,
        borderColor: "#0F172A",
        borderWidth: 2,
        tension: 0.4,
      },
    ],
  };

  return <Bar key={JSON.stringify(cashflows)} data={data} />;
}

export default CashflowChart;
