import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ProjectForm from "../components/ProjectForm";

function InputPage() {
  const navigate = useNavigate();

  useEffect(() => {
    const user = localStorage.getItem("user");

    if (!user) {
      navigate("/login");
    }
  }, [navigate]);

  return (
    <div style={{ padding: "30px" }}>
      <h1>Capital Budgeting System</h1>
      <h2>Enter Project Details</h2>
      <ProjectForm />
    </div>
  );
}

export default InputPage;
