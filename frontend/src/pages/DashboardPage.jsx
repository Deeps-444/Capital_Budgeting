import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import DashboardLayout from "../components/layout/DashboardLayout";
import CashflowChart from "../components/charts/CashflowChart";
import RiskDonut from "../components/charts/RiskDonut";
import NPVDistribution from "../components/charts/NPVDistribution";
import "../chartConfig";

function DashboardPage() {
  const { state } = useLocation();
  const navigate = useNavigate();

  const storedData = sessionStorage.getItem("projectResult");
  const projectData = state || (storedData ? JSON.parse(storedData) : null);

  // No project case
  if (!projectData) {
    return (
      <DashboardLayout>
        <div className="flex flex-col items-center justify-center h-[60vh] gap-4">
          <h2 className="text-2xl font-semibold">No Project Selected</h2>
          <button
            onClick={() => navigate("/new-project")}
            className="bg-green-500 text-white px-4 py-2 rounded"
          >
            Create New Project
          </button>
        </div>
      </DashboardLayout>
    );
  }

  // Extract data
  const {
    projectName,
    cashflows,
    meanNPV,
    stdNPV,
    riskProbability,
    p10,
    p50,
    p90,
  } = projectData;

  return (
    <DashboardLayout>
      <div className="p-6 space-y-6">
        {/* Title */}
        <h1 className="text-2xl font-bold">{projectName}</h1>

        {/* KPI CARDS */}
        <div className="grid grid-cols-4 gap-4">
          <div className="bg-white p-4 rounded shadow">
            <p className="text-gray-500">Mean NPV</p>
            <h2 className="text-xl font-bold">₹{meanNPV.toFixed(0)}</h2>
          </div>

          <div className="bg-white p-4 rounded shadow">
            <p className="text-gray-500">Risk</p>
            <h2 className="text-xl font-bold">
              {(riskProbability * 100).toFixed(1)}%
            </h2>
          </div>

          <div className="bg-white p-4 rounded shadow">
            <p className="text-gray-500">Worst Case (P10)</p>
            <h2 className="text-xl font-bold">₹{p10.toFixed(0)}</h2>
          </div>

          <div className="bg-white p-4 rounded shadow">
            <p className="text-gray-500">Best Case (P90)</p>
            <h2 className="text-xl font-bold">₹{p90.toFixed(0)}</h2>
          </div>
        </div>

        {/* Charts */}
        <div className="grid grid-cols-2 gap-6">
          {/* Cashflow */}
          <div className="bg-white p-4 rounded shadow">
            <h3 className="font-semibold mb-2">Cashflow Analysis</h3>
            <CashflowChart cashflows={cashflows} />
          </div>

          {/* Risk */}
          <div className="bg-white p-4 rounded shadow">
            <h3 className="font-semibold mb-2">Risk Analysis</h3>
            <RiskDonut risk={riskProbability} />
          </div>
        </div>

        {/* NPV Distribution */}
        <div className="bg-white p-4 rounded shadow">
          <h3 className="font-semibold mb-2">NPV Distribution</h3>
          <NPVDistribution mean={meanNPV} std={stdNPV} />
        </div>
      </div>
    </DashboardLayout>
  );
}

export default DashboardPage;
