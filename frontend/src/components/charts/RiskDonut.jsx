import React from "react";
import { Doughnut } from "react-chartjs-2";

function RiskDonut({ risk }) {
  if (risk === undefined) return null;

  // Convert to percentage
  const riskPercent = risk * 100;
  const success = 100 - riskPercent;

  const data = {
    labels: ["Success", "Risk"],
    datasets: [
      {
        data: [success, riskPercent],
        backgroundColor: ["#22C55E", "#EF4444"],
        borderWidth: 0,
      },
    ],
  };

  const options = {
    cutout: "70%",
    plugins: {
      legend: {
        position: "bottom",
      },
      tooltip: {
        callbacks: {
          label: function (context) {
            return `${context.label}: ${context.raw.toFixed(1)}%`;
          },
        },
      },
    },
  };

  return (
    <div className="relative h-48 flex items-center justify-center">
      {/* Chart */}
      <Doughnut data={data} options={options} />

      {/* Center Text */}
      <div className="absolute text-center">
        <p className="text-sm text-gray-500">Risk</p>
        <p className="text-lg font-bold text-red-500">
          {riskPercent.toFixed(1)}%
        </p>
      </div>
    </div>
  );
}

export default RiskDonut;
