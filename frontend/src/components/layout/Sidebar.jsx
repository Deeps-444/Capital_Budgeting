import React from "react";
import { Home, PlusCircle, History, Settings } from "lucide-react";
import { useLocation, useNavigate } from "react-router-dom";

function Sidebar() {
  const location = useLocation();
  const navigate = useNavigate();

  const menuItems = [
    { name: "Dashboard", icon: <Home size={18} />, path: "/dashboard" },
    {
      name: "New Project",
      icon: <PlusCircle size={18} />,
      path: "/new-project",
    },
    { name: "Projects", icon: <History size={18} />, path: "/projects" },
  ];

  return (
    <div className="w-64 h-screen bg-[#0F172A] text-slate-300 flex flex-col px-5 py-6">
      {/* Logo */}
      <h1
        className="text-2xl font-semibold mb-10 text-white tracking-tight cursor-pointer"
        onClick={() => {
          const stored = sessionStorage.getItem("projectResult");

          if (stored) {
            const parsed = JSON.parse(stored);
            navigate(`/dashboard/${parsed.projectId}`);
          } else {
            navigate("/projects");
          }
        }}
      >
        Cap<span className="text-green-400">Wise</span>
      </h1>

      {/* Menu */}
      <nav className="flex flex-col gap-2">
        {menuItems.map((item) => {
          const isActive = location.pathname === item.path;

          return (
            <div
              key={item.name}
              onClick={() => {
                if (item.name === "Dashboard") {
                  const stored = sessionStorage.getItem("projectResult");

                  if (stored) {
                    const parsed = JSON.parse(stored);
                    navigate(`/dashboard/${parsed.projectId}`);
                  } else {
                    navigate("/projects");
                  }
                } else {
                  if (!isActive) navigate(item.path);
                }
              }}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-xl cursor-pointer transition-all
              ${
                isActive
                  ? "bg-slate-800 text-white"
                  : "hover:bg-slate-800 hover:text-white"
              }`}
            >
              {item.icon}
              <span className="text-sm font-medium">{item.name}</span>
            </div>
          );
        })}

        {/* Spacer */}
        <div className="flex-1" />

        {/* Settings */}
        <div className="flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-slate-800 hover:text-white cursor-pointer transition">
          <Settings size={18} />
          <span className="text-sm font-medium">Settings</span>
        </div>
      </nav>
    </div>
  );
}

export default Sidebar;
