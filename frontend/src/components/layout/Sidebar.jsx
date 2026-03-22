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
    <div className="w-64 h-screen bg-[#0F172A] text-white flex flex-col p-5">
      {/* Logo */}
      <h1
        className="text-2xl font-bold mb-10 text-green-400 cursor-pointer"
        onClick={() => navigate("/dashboard")}
      >
        FinAI
      </h1>

      {/* Menu */}
      <nav className="flex flex-col gap-4">
        {menuItems.map((item) => (
          <div
            key={item.name}
            onClick={() => {
              if (location.pathname !== item.path) {
                navigate(item.path);
              }
            }}
            className={`flex items-center gap-3 p-2 rounded-lg cursor-pointer transition ${
              location.pathname === item.path
                ? "bg-gray-800 text-green-400"
                : "hover:bg-gray-800"
            }`}
          >
            {item.icon}
            <span>{item.name}</span>
          </div>
        ))}

        {/* Settings (optional) */}
        <div className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-800 cursor-pointer mt-auto">
          <Settings size={18} />
          <span>Settings</span>
        </div>
      </nav>
    </div>
  );
}

export default Sidebar;
