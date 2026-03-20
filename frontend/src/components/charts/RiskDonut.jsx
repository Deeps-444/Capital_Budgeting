import React from "react";
import { Doughnut } from "react-chartjs-2";

function RiskDonut({ risk }) {
  const success = 100 - risk;

  const data = {
    labels: ["Success", "Risk"],
    datasets: [
      {
        data: [success, risk],
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
    },
  };

  return (
    <div className="h-48 flex items-center justify-center">
      <Doughnut data={data} options={{ maintainAspectRatio: false }} />
    </div>
  );
}

export default RiskDonut;
