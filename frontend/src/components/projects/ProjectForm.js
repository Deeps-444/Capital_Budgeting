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

    if (formData.marketGrowthIndex < 0 || formData.marketGrowthIndex > 1) {
      newErrors.marketGrowthIndex = "Value must be between 0 and 1";
    }

    if (formData.sectorRiskIndex < 0 || formData.sectorRiskIndex > 1) {
      newErrors.sectorRiskIndex = "Value must be between 0 and 1";
    }

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
        marketGrowthIndex: Number(formData.marketGrowthIndex),
        sectorRiskIndex: Number(formData.sectorRiskIndex),
        discountRate: Number(formData.discountRate),
      };

      const res = await axios.post(
        "http://localhost:8080/projects",
        payload,
      );
      sessionStorage.setItem("projectResult", JSON.stringify(res.data));
      navigate("/dashboard", { state: res.data });
    } catch (err) {
      console.error(err);
      alert("Error evaluating project");
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Project Info */}
      <div className="bg-white p-4 rounded shadow">
        <h2 className="font-semibold mb-3">Project Info</h2>

        <input
          type="text"
          name="projectName"
          placeholder="Project Name"
          className="w-full p-2 border rounded"
          onChange={handleChange}
        />
        {errors.projectName && (
          <p className="text-red-500 text-sm">{errors.projectName}</p>
        )}
      </div>

      {/* Financial Inputs */}
      <div className="bg-white p-4 rounded shadow space-y-3">
        <h2 className="font-semibold">Financial Inputs</h2>

        <input
          type="number"
          name="initialInvestment"
          placeholder="Initial Investment"
          className="w-full p-2 border rounded"
          onChange={handleChange}
        />
        {errors.initialInvestment && (
          <p className="text-red-500 text-sm">{errors.initialInvestment}</p>
        )}

        <input
          type="number"
          name="revenueGrowthRate"
          placeholder="Revenue Growth Rate (%)"
          className="w-full p-2 border rounded"
          onChange={handleChange}
        />
        {errors.revenueGrowthRate && (
          <p className="text-red-500 text-sm">{errors.revenueGrowthRate}</p>
        )}

        <input
          type="number"
          name="inflationRate"
          placeholder="Inflation Rate (%)"
          className="w-full p-2 border rounded"
          onChange={handleChange}
        />
        {errors.inflationRate && (
          <p className="text-red-500 text-sm">{errors.inflationRate}</p>
        )}

        <input
          type="number"
          name="discountRate"
          placeholder="Discount Rate (%)"
          className="w-full p-2 border rounded"
          onChange={handleChange}
        />
        {errors.discountRate && (
          <p className="text-red-500 text-sm">{errors.discountRate}</p>
        )}
      </div>

      {/* Market & Risk */}
      <div className="bg-white p-4 rounded shadow space-y-3">
        <h2 className="font-semibold">Market & Risk</h2>

        <input
          type="number"
          step="0.01"
          name="marketGrowthIndex"
          placeholder="Market Growth Index (0–1)"
          className="w-full p-2 border rounded"
          onChange={handleChange}
        />
        {errors.marketGrowthIndex && (
          <p className="text-red-500 text-sm">{errors.marketGrowthIndex}</p>
        )}

        <input
          type="number"
          step="0.01"
          name="sectorRiskIndex"
          placeholder="Sector Risk Index (0–1)"
          className="w-full p-2 border rounded"
          onChange={handleChange}
        />
        {errors.sectorRiskIndex && (
          <p className="text-red-500 text-sm">{errors.sectorRiskIndex}</p>
        )}
      </div>

      {/* Submit */}
      <button
        onClick={evaluateProject}
        className="bg-green-500 text-white px-4 py-3 rounded w-full"
      >
        Evaluate Project
      </button>
    </div>
  );
}

export default ProjectForm;
