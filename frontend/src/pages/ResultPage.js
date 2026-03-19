import React from "react";
import { useLocation } from "react-router-dom";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
);

function ResultPage() {
  const location = useLocation();
  const result = location.state;

  console.log("Result reeived: ", result);

  if (!result) return <h2>No data</h2>;

  const chartData = {
    labels: result.predictedCashflows.map((_, i) => `Year ${i + 1}`),
    datasets: [
      {
        label: "Cashflows",
        data: result.predictedCashflows,
      },
    ],
  };

  if (!result.npvDistribution) return <h2>No Simulation Data</h2>;
  //Monte Carlo Histogram
  const npvData = result.npvDistribution?.slice(0, 500); // limit for performance

  const bins = 20;
  const min = Math.min(...npvData);
  const max = Math.max(...npvData);
  const binSize = (max - min) / bins;

  const histogram = new Array(bins).fill(0);

  npvData.forEach((val) => {
    const index = Math.min(Math.floor((val - min) / binSize), bins - 1);
    histogram[index]++;
  });

  // labels for bins
  const histogramLabels = histogram.map((_, i) => {
    const start = (min + i * binSize).toFixed(0);
    const end = (min + (i + 1) * binSize).toFixed(0);
    return `${start} to ${end}`;
  });

  const histogramData = {
    labels: histogramLabels,
    datasets: [
      {
        label: "NPV Distribution",
        data: histogram,
      },
    ],
  };

  return (
    <div style={{ padding: "30px" }}>
      <h1>Results</h1>

      <p>
        <b>Project:</b> {result.projectName}
      </p>
      <p>
        <b>Initial Investment:</b> {result.initialInvestment}
      </p>
      <p>
        <b>Mean NPV:</b> {result.meanNPV}
      </p>
      <p>
        <b>Risk Probability:</b> {result.riskProbability}
      </p>

      <h3>Cashflows</h3>
      <ul>
        {result.predictedCashflows.map((cf, i) => (
          <li key={i}>
            Year {i + 1}: {cf}
          </li>
        ))}
      </ul>

      <Bar key={JSON.stringify(result.predictedCashflows)} data={chartData} />

      <h3>Monte Carlo NPV Distribution</h3>

      <Bar key={JSON.stringify(histogram)} data={histogramData} />
    </div>
  );
}
export default ResultPage;
