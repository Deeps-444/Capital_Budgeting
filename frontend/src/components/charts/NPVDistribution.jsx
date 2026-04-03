import React from "react";
import { Line } from "react-chartjs-2";

function NPVDistribution({ mean, std }) {
  if (!mean || !std) return null;

  const points = [];
  const negativePoints = [];
  const positivePoints = [];

  const min = mean - 3 * std;
  const max = mean + 3 * std;
  const step = (max - min) / 80;

  for (let x = min; x <= max; x += step) {
    const y =
      (1 / (std * Math.sqrt(2 * Math.PI))) *
      Math.exp(-((x - mean) ** 2) / (2 * std ** 2));

    points.push({ x, y });

    if (x < 0) {
      negativePoints.push({ x, y });
      positivePoints.push({ x, y: null });
    } else {
      positivePoints.push({ x, y });
      negativePoints.push({ x, y: null });
    }
  }

  const data = {
    datasets: [
      {
        label: "Loss Region",
        data: negativePoints,
        parsing: false,
        borderColor: "rgba(239,68,68,0.9)",
        backgroundColor: "rgba(239,68,68,0.15)", // softer fill
        fill: true,
        tension: 0.4,
        pointRadius: 0, // cleaner
      },
      {
        label: "Profit Region",
        data: positivePoints,
        parsing: false,
        borderColor: "rgba(34,197,94,0.9)",
        backgroundColor: "rgba(34,197,94,0.15)", // softer fill
        fill: true,
        tension: 0.4,
        pointRadius: 0,
      },
      {
        label: "Mean",
        data: [
          { x: mean, y: 0 },
          { x: mean, y: Math.max(...points.map((p) => p.y)) },
        ],
        parsing: false,
        borderColor: "#1E293B",
        borderWidth: 2,
        borderDash: [5, 5], // 🔥 dashed line = premium feel
        pointRadius: 0,
      },
    ],
  };
  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
        labels: {
          color: "#475569",
          font: {
            size: 12,
          },
        },
      },
      tooltip: {
        backgroundColor: "#0F172A",
        titleColor: "#fff",
        bodyColor: "#fff",
        callbacks: {
          label: function (context) {
            return `NPV: ₹${Math.round(context.raw.x)}`;
          },
        },
      },
    },
    scales: {
      x: {
        type: "linear",
        grid: {
          color: "#E2E8F0", // subtle grid
        },
        title: {
          display: true,
          text: "NPV (₹)",
          color: "#64748B",
          font: {
            size: 12,
          },
        },
        ticks: {
          color: "#64748B",
          callback: (value) => `₹${Math.round(value)}`,
        },
      },
      y: {
        display: false,
      },
    },
  };

  return <Line data={data} options={options} />;
}

export default NPVDistribution;
