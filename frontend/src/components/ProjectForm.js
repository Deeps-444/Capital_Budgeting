import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function ProjectForm() {
  const navigate = useNavigate();

  const user = JSON.parse(sessionStorage.getItem("user"));

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

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value === "" ? "" : parseFloat(e.target.value),
    });
  };

  const evaluateProject = async () => {
    if (!user || !user.userId) {
      alert("User not logged in");
      return;
    }

    const isValid = Object.values(formData).every(
      (val) => val !== "" && !isNaN(val),
    );

    if (!isValid) {
      alert("Fill all fields");
      return;
    }

    try {
      const payload = {
        ...formData,
        userId: user.userId,
      };
      console.log("Payload:", payload);
      console.log("User from session:", user);
      const response = await axios.post(
        "http://localhost:8080/projects",
        payload,
      );
      console.log(formData);
      // move to result page with data
      navigate("/result", { state: response.data });
    } catch (error) {
      console.error("Error:", error);
      alert("Error calling backend");
    }
  };

  return (
    <div>
      {Object.keys(formData)
        .filter((key) => key !== "userId")
        .map((key) => (
          <div key={key}>
            <label>{key.replace(/([A-Z])/g, " $1")}</label>
            <input type="number" name={key} onChange={handleChange} />
          </div>
        ))}
      {/* // to evaluate the project */}
      <button onClick={evaluateProject}>Evaluate Project</button>
      {/* to logout */}
      <button
        onClick={() => {
          localStorage.removeItem("user");
          window.location.href = "/login";
        }}
      >
        Logout
      </button>
    </div>
  );
}

export default ProjectForm;
