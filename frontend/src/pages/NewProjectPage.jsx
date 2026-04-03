import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ProjectForm from "../components/projects/ProjectForm";
import DashboardLayout from "../components/layout/DashboardLayout";

function NewProjectPage() {
  const navigate = useNavigate();

  useEffect(() => {
    const storedUser = sessionStorage.getItem("user");

    if (!storedUser) {
      navigate("/login", { replace: true });
    }
    // eslint-disable-next-line
  }, []);

  console.log("InputPage loaded");

  return (
    <DashboardLayout>
      <div className="p-8 bg-slate-50 min-h-screen space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-semibold text-slate-800">New Project</h1>
          <p className="text-sm text-slate-500 mt-1">
            Enter financial and market details to evaluate your project
          </p>
        </div>

        {/* Form */}
        <ProjectForm />
      </div>
    </DashboardLayout>
  );
}

export default NewProjectPage;
