import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ProjectForm from "../components/ProjectForm";
import DashboardLayout from "../components/layout/DashboardLayout";

function InputPage() {
  const navigate = useNavigate();

  useEffect(() => {
    const user = sessionStorage.getItem("user");

    if (!user) {
      navigate("/login");
    }
  }, [navigate]);

  console.log("InputPage loaded");

  return (
    <DashboardLayout>
      <div className="text-gray-700 text-lg mb-4">
        <h1>Capital Budgeting System</h1>
        <h2>Enter Project Details</h2>
        <ProjectForm />
      </div>
    </DashboardLayout>
  );
}

export default InputPage;
