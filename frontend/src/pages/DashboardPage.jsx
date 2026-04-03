import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import DashboardLayout from "../components/layout/DashboardLayout";
import CashflowChart from "../components/charts/CashflowChart";
import RiskDonut from "../components/charts/RiskDonut";
import NPVDistribution from "../components/charts/NPVDistribution";
import "../chartConfig";
import KPIBox from "../components/ui/KPIBox";
import Card from "../components/ui/Card";

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
          <h2 className="text-2xl font-semibold text-slate-700">
            No Project Selected
          </h2>
          <button
            onClick={() => navigate("/new-project")}
            className="bg-slate-800 text-white px-5 py-2 rounded-xl hover:bg-slate-700 transition"
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
      <div className="p-8 space-y-8 bg-slate-50 min-h-screen">
        {/* Title */}
        <h1 className="text-3xl font-semibold text-slate-800">{projectName}</h1>

        {/* KPI CARDS */}
        <div className="grid grid-cols-4 gap-6">
          <KPIBox
            title="Mean NPV"
            value={`₹${meanNPV.toFixed(0)}`}
            border="border-green-500"
          />

          <KPIBox
            title="Risk"
            value={`${(riskProbability * 100).toFixed(1)}%`}
            border="border-red-500"
          />

          <KPIBox
            title="Worst Case (P10)"
            value={`₹${p10.toFixed(0)}`}
            border="border-yellow-500"
          />

          <KPIBox
            title="Best Case (P90)"
            value={`₹${p90.toFixed(0)}`}
            border="border-blue-500"
          />
        </div>

        {/* Charts */}
        <div className="grid grid-cols-2 gap-6">
          {/* Cashflow */}
          <Card>
            <h3 className="font-semibold text-slate-700 mb-4">
              Cashflow Analysis
            </h3>
            <CashflowChart cashflows={cashflows} />
          </Card>

          {/* Risk */}
          <Card>
            <h3 className="font-semibold text-slate-700 mb-4">Risk Analysis</h3>
            <RiskDonut risk={riskProbability} />
          </Card>
        </div>

        {/* NPV Distribution */}
        <Card>
          <h3 className="font-semibold text-slate-700 mb-4">
            NPV Distribution
          </h3>
          <NPVDistribution mean={meanNPV} std={stdNPV} />
        </Card>
      </div>
    </DashboardLayout>
  );
}

export default DashboardPage;
