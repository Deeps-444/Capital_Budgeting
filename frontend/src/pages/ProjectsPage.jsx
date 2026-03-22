import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import DashboardLayout from "../components/layout/DashboardLayout";

function ProjectsPage() {
  const navigate = useNavigate();

  const [projects, setProjects] = useState([]);
  const [loadingId, setLoadingId] = useState(null);

  useEffect(() => {
    const storedUser = sessionStorage.getItem("user");

    //  If not logged in → redirect
    if (!storedUser) {
      navigate("/login", { replace: true });
      return;
    }

    const user = JSON.parse(storedUser);

    // 📡 Fetch projects
    const fetchProjects = async () => {
      try {
        const res = await axios.get(
          `http://localhost:8080/projects/user/${user.userId}`,
        );
        setProjects(res.data);
      } catch (err) {
        console.error(err);
        alert("Error fetching projects");
      }
    };

    fetchProjects();
  }, [navigate]); // ✅ safe dependency

  return (
    <DashboardLayout>
      <div className="p-6 space-y-6">
        {/* Title */}
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold">My Projects</h1>

          <button
            onClick={() => navigate("/new-project")}
            className="bg-green-500 text-white px-4 py-2 rounded"
          >
            + New Project
          </button>
        </div>

        {/* Projects */}
        {projects.length === 0 ? (
          <p className="text-gray-500">No projects found</p>
        ) : (
          <div className="grid grid-cols-3 gap-4">
            {projects.map((proj) => (
              <div
                key={proj.projectId}
                className="bg-white p-4 rounded shadow cursor-pointer hover:shadow-lg transition"
                onClick={async () => {
                  setLoadingId(proj.projectId);

                  try {
                    const res = await axios.get(
                      `http://localhost:8080/projects/${proj.projectId}`,
                    );

                    navigate("/dashboard", { state: res.data });
                  } catch (err) {
                    console.error(err);
                    alert("Error loading project");
                  } finally {
                    setLoadingId(null);
                  }
                }}
              >
                <h2 className="font-semibold">
                  {loadingId === proj.projectId
                    ? "Loading..."
                    : proj.projectName}
                </h2>

                <p className="text-sm text-gray-500 mt-2">
                  NPV: ₹{proj.meanNPV?.toFixed(0)}
                </p>

                <p className="text-sm text-gray-500">
                  Risk: {(proj.riskProbability * 100).toFixed(1)}%
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

export default ProjectsPage;
