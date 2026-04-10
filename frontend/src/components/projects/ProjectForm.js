import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function ProjectForm() {
  const navigate = useNavigate();
  const storedUser = sessionStorage.getItem("user");
  const user = storedUser ? JSON.parse(storedUser) : null;

  const [formData, setFormData] = useState({
    projectName: "",
    initialInvestment: "",
    revenueGrowthRate: "",
    inflationRate: "",
    marketGrowthIndex: "",
    sectorRiskIndex: "",
    discountRate: "",
  });

  const [errors, setErrors] = useState({});

  // 🔧 Handle input
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  // Validation
  const validate = () => {
    let newErrors = {};

    if (!formData.projectName.trim()) {
      newErrors.projectName = "Project name is required";
    }

    if (Number(formData.initialInvestment) <= 0) {
      newErrors.initialInvestment = "Must be greater than 0";
    }

    if (formData.revenueGrowthRate < 0 || formData.revenueGrowthRate > 100) {
      newErrors.revenueGrowthRate = "Enter % between 0–100";
    }

    if (formData.inflationRate < 0 || formData.inflationRate > 100) {
      newErrors.inflationRate = "Enter % between 0–100";
    }

    if (formData.discountRate <= 0 || formData.discountRate > 100) {
      newErrors.discountRate = "Enter % between 0–100";
    }

    // if (formData.marketGrowthIndex < 0 || formData.marketGrowthIndex > 1) {
    //   newErrors.marketGrowthIndex = "Value must be between 0 and 1";
    // }

    // if (formData.sectorRiskIndex < 0 || formData.sectorRiskIndex > 1) {
    //   newErrors.sectorRiskIndex = "Value must be between 0 and 1";
    // }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Submit
  const evaluateProject = async () => {
    if (!user || !user.userId) {
      alert("User not logged in");
      return;
    }

    if (!validate()) return;

    try {
      const payload = {
        ...formData,
        userId: user.userId,
        initialInvestment: Number(formData.initialInvestment),
        revenueGrowthRate: Number(formData.revenueGrowthRate),
        inflationRate: Number(formData.inflationRate),
        marketGrowthIndex: formData.marketGrowthIndex,
        sectorRiskIndex: formData.sectorRiskIndex,
        discountRate: Number(formData.discountRate),
      };

      const res = await axios.post("http://localhost:8080/projects", payload);
      sessionStorage.setItem("projectResult", JSON.stringify(res.data));
      navigate(`/dashboard/${res.data.projectId}`, { state: res.data });
    } catch (err) {
      console.error(err);
      alert("Error evaluating project");
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Project Info */}
      <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
        <h2 className="text-lg font-semibold text-slate-800 mb-4">
          Project Info
        </h2>

        <input
          type="text"
          name="projectName"
          placeholder="Project Name"
          className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-300 text-sm"
          onChange={handleChange}
        />
        {errors.projectName && (
          <p className="text-red-500 text-sm mt-1">{errors.projectName}</p>
        )}
      </div>

      {/* Financial Inputs */}
      <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 space-y-4">
        <h2 className="text-lg font-semibold text-slate-800">
          Financial Inputs
        </h2>

        <input
          type="number"
          name="initialInvestment"
          placeholder="Initial Investment"
          className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-300 text-sm"
          onChange={handleChange}
        />
        {errors.initialInvestment && (
          <p className="text-red-500 text-sm">{errors.initialInvestment}</p>
        )}

        <input
          type="number"
          name="revenueGrowthRate"
          placeholder="Revenue Growth Rate (%)"
          className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-300 text-sm"
          onChange={handleChange}
        />
        {errors.revenueGrowthRate && (
          <p className="text-red-500 text-sm">{errors.revenueGrowthRate}</p>
        )}

        <input
          type="number"
          name="inflationRate"
          placeholder="Inflation Rate (%)"
          className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-300 text-sm"
          onChange={handleChange}
        />
        {errors.inflationRate && (
          <p className="text-red-500 text-sm">{errors.inflationRate}</p>
        )}

        <input
          type="number"
          name="discountRate"
          placeholder="Discount Rate (%)"
          className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-300 text-sm"
          onChange={handleChange}
        />
        {errors.discountRate && (
          <p className="text-red-500 text-sm">{errors.discountRate}</p>
        )}
      </div>

      {/* Market & Risk */}
      <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 space-y-4">
        <h2 className="text-lg font-semibold text-slate-800">Market & Risk</h2>

        <select
          value={formData.marketGrowthIndex}
          onChange={(e) =>
            setFormData({ ...formData, marketGrowthIndex: e.target.value })
          }
          className="w-full px-4 py-3 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-slate-300"
        >
          <option value="">Select Market Growth</option>
          <option value="LOW">Low Growth</option>
          <option value="MEDIUM">Moderate Growth</option>
          <option value="HIGH">High Growth</option>
        </select>

        <select
          value={formData.sectorRiskIndex}
          onChange={(e) =>
            setFormData({ ...formData, sectorRiskIndex: e.target.value })
          }
          className="w-full px-4 py-3 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-slate-300"
        >
          <option value="">Select Sector Risk</option>
          <option value="LOW">Low Risk</option>
          <option value="MEDIUM">Moderate Risk</option>
          <option value="HIGH">High Risk</option>
        </select>
        {errors.sectorRiskIndex && (
          <p className="text-red-500 text-sm">{errors.sectorRiskIndex}</p>
        )}
      </div>

      {/* Submit */}
      <button
        onClick={evaluateProject}
        className="w-full bg-slate-800 text-white py-3 rounded-2xl font-medium hover:bg-slate-700 transition"
      >
        Evaluate Project
      </button>
    </div>
  );
}

export default ProjectForm;
