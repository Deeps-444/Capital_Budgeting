import React from "react";
import { Doughnut } from "react-chartjs-2";

function NPVGauge({ value }) {
  const isPositive = value >= 0;

  const data = {
    datasets: [
      {
        data: [Math.abs(value), 1000000],
        backgroundColor: [isPositive ? "#22C55E" : "#EF4444", "#E5E7EB"],
        borderWidth: 0,
      },
    ],
  };

  const options = {
    cutout: "80%",
    rotation: -90,
    circumference: 180,
    plugins: {
      tooltip: { enabled: false },
      legend: { display: false },
    },
    maintainAspectRatio: false, // ✅ IMPORTANT
  };

  return (
    <div className="flex flex-col items-center justify-center h-40">
      {/* 👇 CONTROL HEIGHT */}
      <div className="w-full h-28">
        <Doughnut data={data} options={options} />
      </div>

      <p
        className={`text-lg font-bold mt-1 ${
          isPositive ? "text-green-500" : "text-red-500"
        }`}
      >
        ₹{Math.round(value)}
      </p>

      <p className="text-xs text-gray-500">Expected NPV</p>
    </div>
  );
}
export default NPVGauge;
