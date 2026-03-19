import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function ProjectForm() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    userId: 1,
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

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: parseFloat(e.target.value),
    });
  };

  const evaluateProject = async () => {
    try {
      const response = await axios.post(
        "http://localhost:8080/projects",
        formData,
      );
      console.log(response.data);
      // move to result page with data
      navigate("/result", { state: response.data });
    } catch (error) {
      console.error("Error:", error);
      alert("Error calling backend");
    }
  };

  return (
    <div>
      {Object.keys(formData).map((key) => (
        <div key={key}>
          <label>{key}</label>
          <input type="number" name={key} onChange={handleChange} />
        </div>
      ))}

      <button onClick={evaluateProject}>Evaluate Project</button>
    </div>
  );
}

export default ProjectForm;
