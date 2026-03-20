import React from "react";
import { useLocation } from "react-router-dom";
import { Bar } from "react-chartjs-2";

import CashflowChart from "../components/charts/CashflowChart";
import RiskDonut from "../components/charts/RiskDonut";
import NPVGauge from "../components/charts/NPVGauge";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

import annotationPlugin from "chartjs-plugin-annotation";

import DashboardLayout from "../components/layout/DashboardLayout";
import KPIBox from "../components/ui/KPIBox";
import Card from "../components/ui/Card";

// ✅ Register ALL required elements
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
  annotationPlugin,
);

function ResultPage() {
  const location = useLocation();
  const result = location.state;

  if (!result) return <h2 className="p-6">No data</h2>;

  // 💰 Currency formatter
  const formatCurrency = (num) =>
    new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 0,
    }).format(num);

  // 🎲 Monte Carlo Histogram
  const npvData = result.npvDistribution || [];

  const sortedData = [...npvData].sort((a, b) => a - b);
  const varIndex = Math.floor(0.05 * sortedData.length);
  const varValue = sortedData[varIndex];

  const bins = 20;
  const min = Math.min(...npvData);
  const max = Math.max(...npvData);
  const binSize = (max - min) / bins;

  const histogram = new Array(bins).fill(0);

  npvData.forEach((val) => {
    const index = Math.min(Math.floor((val - min) / binSize), bins - 1);
    histogram[index]++;
  });

  const histogramLabels = histogram.map((_, i) => {
    const start = (min + i * binSize).toFixed(0);
    const end = (min + (i + 1) * binSize).toFixed(0);
    return `${start} - ${end}`;
  });

  const histogramData = {
    labels: histogramLabels,
    datasets: [
      {
        label: "NPV Distribution",
        data: histogram,
        backgroundColor: "#0F172A",
        borderRadius: 4,
      },
    ],
  };

  const histogramOptions = {
    responsive: true,
    maintainAspectRatio: false, // ✅ IMPORTANT
    plugins: {
      legend: { position: "top" },
      title: {
        display: false,
      },
      annotation: {
        annotations: {
          line1: {
            type: "line",
            xMin: Math.floor((varValue - min) / binSize),
            xMax: Math.floor((varValue - min) / binSize),
            borderColor: "#EF4444",
            borderWidth: 2,
            label: {
              content: "VaR (5%)",
              enabled: true,
            },
          },
        },
      },
    },
  };

  return (
    <DashboardLayout>
      <div className="h-[calc(100vh-80px)] overflow-y-auto flex flex-col">
        {/* 🔷 Header */}
        <div className="mb-3">
          <h1 className="text-xl font-semibold text-gray-800">
            {result.projectName}
          </h1>
          <p className="text-sm text-gray-500">Financial Analysis Summary</p>
        </div>

        {/* 🟢 KPI SECTION */}
        <div className="grid grid-cols-3 gap-4 mb-4">
          <KPIBox
            title="Initial Investment"
            value={formatCurrency(result.initialInvestment)}
          />

          <Card className="flex items-center justify-center">
            <NPVGauge value={result.meanNPV} />
          </Card>

          <KPIBox
            title="Risk Probability"
            value={`${result.riskProbability}%`}
            color="text-red-500"
          />
        </div>

        {/* 📊 MAIN VISUALS */}
        <div className="grid grid-cols-2 gap-4 flex-1">
          {/* 💸 Cashflow */}
          <Card>
            <h3 className="text-sm font-semibold mb-2 text-gray-700">
              Cashflow Analysis
            </h3>
            <div className="h-48">
              <CashflowChart cashflows={result.predictedCashflows} />
            </div>
          </Card>

          {/* 🍩 Risk */}
          <Card>
            <h3 className="text-sm font-semibold mb-2 text-gray-700">
              Risk Analysis
            </h3>
            <div className="h-48">
              <RiskDonut risk={result.riskProbability} />
            </div>
          </Card>
        </div>

        {/* 🎲 MONTE CARLO */}
        <div className="mt-4">
          <Card>
            <h3 className="text-sm font-semibold mb-2 text-gray-700">
              Monte Carlo Simulation
            </h3>
            <div className="h-52">
              <Bar
                key={JSON.stringify(histogramData)} // ✅ prevents canvas reuse error
                data={histogramData}
                options={histogramOptions}
              />
            </div>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
}

export default ResultPage;
