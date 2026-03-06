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

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
);

function App() {
  const [formData, setFormData] = useState({
    initialInvestment: "",
    revenueGrowthRate: "",
    operatingCostRatio: "",
    workingCapitalRatio: "",
    capexRatio: "",
    inflationRate: "",
    marketGrowthIndex: "",
    sectorRiskIndex: "",
    discountRate: "",
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: parseFloat(e.target.value),
    });
  };

  const evaluateProject = async () => {
    try {
      const response = await axios.post(
        "http://localhost:8080/api/evaluate",
        formData,
      );

      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert("Error calling backend");
    }
  };

  const chartData = result
    ? {
        labels: result.npvDistribution.slice(0, 50).map((_, i) => i),
        datasets: [
          {
            label: "NPV Distribution",
            data: result.npvDistribution.slice(0, 50),
          },
        ],
      }
    : null;

  return (
    <div style={{ padding: "30px", fontFamily: "Arial" }}>
      <h1>Capital Budgeting Decision Support System</h1>

      <h2>Project Inputs</h2>

      {Object.keys(formData).map((key) => (
        <div key={key}>
          <label>{key}</label>
          <input type="number" name={key} onChange={handleChange} />
        </div>
      ))}

      <br />

      <button onClick={evaluateProject}>Evaluate Project</button>

      {result && (
        <div style={{ marginTop: "40px" }}>
          <h2>Results</h2>

          <p>
            <b>Mean NPV:</b> {result.meanNPV}
          </p>

          <p>
            <b>Risk Probability:</b> {result.riskProbability}
          </p>

          <h3>Predicted Cashflows</h3>

          <ul>
            {result.predictedCashflows.map((cf, index) => (
              <li key={index}>
                Year {index + 1}: {cf}
              </li>
            ))}
          </ul>

          <h3>NPV Distribution</h3>

          {chartData && <Bar data={chartData} />}
        </div>
      )}
    </div>
  );
}

export default App;
