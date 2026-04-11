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

    //  Fetch projects
    const fetchProjects = async () => {
      try {
        const res = await axios.get(
          `http://localhost:8080/projects/user/${user.userId}`,
        );
        setProjects(res.data);
        console.log("Fetched Projects List:", res.data);
      } catch (err) {
        console.error(err);
        alert("Error fetching projects");
      }
    };

    fetchProjects();
  }, [navigate]); // safe dependency

  return (
    <DashboardLayout>
      <div className="p-8 bg-slate-50 min-h-screen space-y-8">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-semibold text-slate-800">
              My Projects
            </h1>
            <p className="text-sm text-slate-500 mt-1">
              View and manage your saved project analyses
            </p>
          </div>

          <button
            onClick={() => navigate("/new-project")}
            className="bg-slate-800 text-white px-5 py-2.5 rounded-xl text-sm font-medium hover:bg-slate-700 transition"
          >
            + New Project
          </button>
        </div>

        {/* Projects */}
        {projects.length === 0 ? (
          <div className="text-slate-500 text-sm">No projects found</div>
        ) : (
          <div className="grid grid-cols-3 gap-6">
            {projects.map((proj) => (
              <div
                key={proj.projectId}
                onClick={async () => {
                  setLoadingId(proj.projectId);

                  try {
                    const res = await axios.get(
                      `http://localhost:8080/projects/${proj.projectId}`,
                    );

                    navigate(`/dashboard/${proj.projectId}`, {
                      state: res.data,
                    });
                  } catch (err) {
                    console.error(err);
                    alert("Error loading project");
                  } finally {
                    setLoadingId(null);
                  }
                }}
                className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition cursor-pointer"
              >
                {/* Title */}
                <h2 className="font-semibold text-slate-800">
                  {loadingId === proj.projectId ? (
                    <span className="text-slate-400">Opening...</span>
                  ) : (
                    proj.projectName
                  )}
                </h2>

                {/* Info */}
                <div className="mt-3 space-y-1 text-sm text-slate-500">
                  <p>
                    NPV:{" "}
                    <span className="text-slate-700 font-medium">
                      ₹{proj.meanNPV?.toFixed(0)}
                    </span>
                  </p>

                  <p>
                    Risk:{" "}
                    <span className="text-red-500 font-medium">
                      {(proj.riskProbability * 100).toFixed(1)}%
                    </span>
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

export default ProjectsPage;
