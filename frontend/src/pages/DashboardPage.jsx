import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import DashboardLayout from "../components/layout/DashboardLayout";
import CashflowChart from "../components/charts/CashflowChart";
import RiskDonut from "../components/charts/RiskDonut";
import NPVDistribution from "../components/charts/NPVDistribution";
import "../chartConfig";
import KPIBox from "../components/ui/KPIBox";
import Card from "../components/ui/Card";
import { useParams } from "react-router-dom";
import Loader from "../components/ui/Loader";
import axios from "axios";

function DashboardPage() {
  // const { state } = useLocation();
  const navigate = useNavigate();
  const { projectId } = useParams();

  // const storedData = sessionStorage.getItem("projectResult");
  // const projectData = state || (storedData ? JSON.parse(storedData) : null);

  const [projectData, setProjectData] = React.useState(null);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    if (!projectId) {
      const stored = sessionStorage.getItem("projectResult");

      if (stored) {
        const parsed = JSON.parse(stored);
        navigate(`/dashboard/${parsed.projectId}`);
      } else {
        navigate("/projects"); // or "/new-project"
      }
      return;
    }
    const fetchProject = async () => {
      try {
        const res = await axios.get(
          `http://localhost:8080/projects/${projectId}`,
        );
        setProjectData(res.data);
        console.log("Dashboard Data Loaded:", res.data);
        // optional: store for fallback
        sessionStorage.setItem("projectResult", JSON.stringify(res.data));
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchProject();
  }, [projectId]);

  if (loading) {
    return (
      <DashboardLayout>
        <Loader />
      </DashboardLayout>
    );
  }
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
    irr,
    npv,
  } = projectData;

  // for explanability
  const generateInsights = () => {
    if (!projectData) return [];

    const insights = [];

    // IRR insight
    if (irr > 0.15) {
      insights.push("Strong return potential with high IRR.");
    } else if (irr > 0.08) {
      insights.push("Moderate return project.");
    } else {
      insights.push("Low return potential.");
    }

    // Risk insight
    if (riskProbability > 0.5) {
      insights.push("High risk: significant probability of loss.");
    } else if (riskProbability > 0.25) {
      insights.push("Moderate risk involved.");
    } else {
      insights.push("Relatively low risk project.");
    }

    // NPV comparison
    if (p10 < 0 && meanNPV > 0) {
      insights.push(
        "Positive expected value, but downside risk exists (possible losses in worst-case scenarios).",
      );
    }

    // Spread insight
    if (p90 - p10 > meanNPV) {
      insights.push("High variability in outcomes (uncertain project).");
    }

    return insights;
  };

  const insights = generateInsights();

  return (
    <DashboardLayout>
      <div className="p-8 space-y-8 bg-gradient-to-br from-slate-50 to-slate-100 min-h-screen">
        {/* Title */}
        <h1 className="text-3xl font-semibold text-slate-800">{projectName}</h1>

        {/* KPI CARDS */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
          <KPIBox
            title="Expected NPV (Mean)"
            value={`₹${meanNPV.toFixed(0)}`}
            border="border-green-500"
          />

          <KPIBox
            title="Baseline NPV"
            value={
              npv !== null && npv !== undefined ? `₹${npv.toFixed(0)}` : "N/A"
            }
            border="border-slate-500"
          />

          <KPIBox
            title="IRR"
            value={
              irr !== null && irr !== undefined
                ? `${(irr * 100).toFixed(1)}%`
                : "N/A"
            }
            border="border-purple-500"
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

        <Card>
          <h3 className="text-lg font-semibold text-slate-800 mb-3">
            Key Insights
          </h3>

          <ul className="space-y-2 text-sm text-slate-600">
            {insights.map((insight, index) => (
              <li key={index} className="flex items-start gap-2">
                <span className="text-green-500 mt-1">•</span>
                <span>{insight}</span>
              </li>
            ))}
          </ul>
        </Card>

        {/* Charts */}
        <h2 className="text-lg font-semibold text-slate-700">
          Analysis Overview
        </h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
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
