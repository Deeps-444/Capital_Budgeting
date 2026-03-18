import React, { useState } from "react";
import axios from "axios";
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
import "./App.css";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const FIELDS = [
  { key: "initialInvestment",    label: "Initial Investment",      placeholder: "e.g. 1000000" },
  { key: "revenueGrowthRate",    label: "Revenue Growth Rate",     placeholder: "e.g. 0.12" },
  { key: "operatingCostRatio",   label: "Operating Cost Ratio",    placeholder: "e.g. 0.45" },
  { key: "workingCapitalRatio",  label: "Working Capital Ratio",   placeholder: "e.g. 0.10" },
  { key: "capexRatio",           label: "CapEx Ratio",             placeholder: "e.g. 0.08" },
  { key: "inflationRate",        label: "Inflation Rate",          placeholder: "e.g. 0.03" },
  { key: "marketGrowthIndex",    label: "Market Growth Index",     placeholder: "e.g. 1.05" },
  { key: "sectorRiskIndex",      label: "Sector Risk Index",       placeholder: "e.g. 0.75" },
  { key: "discountRate",         label: "Discount Rate (WACC)",    placeholder: "e.g. 0.09" },
];

const fmt = (val) =>
  typeof val === "number"
    ? val.toLocaleString("en-US", { maximumFractionDigits: 2 })
    : val;

const getRiskLevel = (prob) => {
  if (prob === null || prob === undefined) return null;
  if (prob > 0.6) return { label: "HIGH RISK", cls: "high" };
  if (prob > 0.3) return { label: "MODERATE RISK", cls: "med" };
  return { label: "LOW RISK", cls: "low" };
};

function App() {
  const [formData, setFormData] = useState(
    Object.fromEntries(FIELDS.map((f) => [f.key, ""]))
  );
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const evaluateProject = async () => {
    setLoading(true);
    setResult(null);
    try {
      const payload = Object.fromEntries(
        Object.entries(formData).map(([k, v]) => [k, parseFloat(v)])
      );
      const response = await axios.post("http://localhost:8080/api/evaluate", payload);
      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert("Error calling backend. Make sure the server is running.");
    } finally {
      setLoading(false);
    }
  };

  const isFormFilled = FIELDS.every((f) => formData[f.key] !== "");
  const risk = result ? getRiskLevel(result.riskProbability) : null;

  const chartData = result
    ? {
        labels: result.npvDistribution.slice(0, 50).map((_, i) => `S${i + 1}`),
        datasets: [
          {
            label: "NPV",
            data: result.npvDistribution.slice(0, 50),
            backgroundColor: result.npvDistribution
              .slice(0, 50)
              .map((v) =>
                v >= 0 ? "rgba(52, 211, 153, 0.55)" : "rgba(248, 113, 113, 0.55)"
              ),
            borderColor: result.npvDistribution
              .slice(0, 50)
              .map((v) =>
                v >= 0 ? "rgba(52, 211, 153, 0.9)" : "rgba(248, 113, 113, 0.9)"
              ),
            borderWidth: 1,
            borderRadius: 2,
          },
        ],
      }
    : null;

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: "#111318",
        borderColor: "#1f2535",
        borderWidth: 1,
        titleColor: "#6b7280",
        bodyColor: "#e8eaf0",
        titleFont: { family: "DM Mono", size: 10 },
        bodyFont: { family: "DM Mono", size: 11 },
      },
    },
    scales: {
      x: {
        grid: { color: "rgba(31,37,53,0.8)" },
        ticks: {
          color: "#6b7280",
          font: { family: "DM Mono", size: 9 },
          maxTicksLimit: 10,
        },
      },
      y: {
        grid: { color: "rgba(31,37,53,0.8)" },
        ticks: {
          color: "#6b7280",
          font: { family: "DM Mono", size: 9 },
          callback: (v) => (v >= 1000 ? `${(v / 1000).toFixed(0)}k` : v),
        },
      },
    },
  };

  return (
    <div className="app-wrapper">
      {/* Header */}
      <header className="app-header">
        <div className="header-left">
          <h1>
            Capital <span>Budgeting</span>
            <br />Decision Support
          </h1>
        </div>
        <div className="header-badge">Monte Carlo · DCF Analysis</div>
      </header>

      {/* Main Grid */}
      <div className="main-grid">
        {/* ── Left: Inputs ── */}
        <div className="panel">
          <div className="panel-header">
            <div className="panel-dot" />
            <h2>Project Parameters</h2>
          </div>
          <div className="panel-body">
            <div className="field-list">
              {FIELDS.map((f) => (
                <div className="field-row" key={f.key}>
                  <label className="field-label" htmlFor={f.key}>
                    {f.label}
                  </label>
                  <input
                    id={f.key}
                    className="field-input"
                    type="number"
                    name={f.key}
                    placeholder={f.placeholder}
                    value={formData[f.key]}
                    onChange={handleChange}
                  />
                </div>
              ))}
            </div>

            <button
              className="evaluate-btn"
              onClick={evaluateProject}
              disabled={loading || !isFormFilled}
            >
              {loading ? "Running Analysis…" : "Evaluate Project"}
            </button>
          </div>
        </div>

        {/* ── Right: Results ── */}
        <div className="results-col">
          {/* Key Metrics */}
          <div className="panel">
            <div className="panel-header">
              <div className="panel-dot" />
              <h2>Key Metrics</h2>
            </div>
            <div className="panel-body">
              {loading && (
                <div className="loading-overlay">
                  <div className="loading-bar">
                    <div className="loading-fill" />
                  </div>
                  <span className="loading-text">Running Monte Carlo simulation…</span>
                </div>
              )}

              {!loading && !result && (
                <div className="empty-state">
                  <div className="empty-icon">◈</div>
                  <p>Fill in parameters and<br />run the evaluation</p>
                </div>
              )}

              {!loading && result && (
                <>
                  <div className="metric-grid">
                    <div className="metric-card">
                      <div className="metric-label">Mean NPV</div>
                      <div
                        className={`metric-value ${
                          result.meanNPV >= 0 ? "positive" : "negative"
                        }`}
                      >
                        {fmt(result.meanNPV)}
                      </div>
                    </div>
                    <div className="metric-card">
                      <div className="metric-label">Risk Probability</div>
                      <div className="metric-value">
                        {(result.riskProbability * 100).toFixed(1)}%
                      </div>
                    </div>
                  </div>
                  {risk && (
                    <div style={{ marginTop: 16 }}>
                      <span className={`risk-pill ${risk.cls}`}>
                        ● {risk.label}
                      </span>
                    </div>
                  )}
                </>
              )}
            </div>
          </div>

          {/* Cashflows */}
          <div className="panel">
            <div className="panel-header">
              <div className="panel-dot" />
              <h2>Predicted Cashflows</h2>
            </div>
            <div className="panel-body" style={{ padding: "0" }}>
              {!result && (
                <div className="empty-state" style={{ padding: "32px" }}>
                  <p>No cashflow data yet</p>
                </div>
              )}
              {result && (
                <table className="cashflow-table">
                  <thead>
                    <tr>
                      <th>Year</th>
                      <th>Cashflow</th>
                      <th>Δ Prior</th>
                    </tr>
                  </thead>
                  <tbody>
                    {result.predictedCashflows.map((cf, i) => {
                      const prev = i > 0 ? result.predictedCashflows[i - 1] : null;
                      const delta = prev !== null ? cf - prev : null;
                      return (
                        <tr key={i}>
                          <td>Y{i + 1}</td>
                          <td className={cf >= 0 ? "cf-positive" : "cf-negative"}>
                            {fmt(cf)}
                          </td>
                          <td
                            className={
                              delta === null
                                ? ""
                                : delta >= 0
                                ? "cf-positive"
                                : "cf-negative"
                            }
                          >
                            {delta !== null
                              ? `${delta >= 0 ? "+" : ""}${fmt(delta)}`
                              : "—"}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              )}
            </div>
          </div>

          {/* NPV Distribution */}
          <div className="panel">
            <div className="panel-header">
              <div className="panel-dot" />
              <h2>NPV Distribution</h2>
            </div>
            <div className="panel-body">
              {!result && (
                <div className="empty-state">
                  <p>Chart will appear after evaluation</p>
                </div>
              )}
              {result && chartData && (
                <div className="chart-container">
                  <Bar data={chartData} options={chartOptions} />
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      <footer className="app-footer">
        <span>Capital Budgeting DSS</span>
        <span>Monte Carlo Simulation Engine</span>
      </footer>
    </div>
  );
}

export default App;