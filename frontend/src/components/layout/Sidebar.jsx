import React from "react";
import { Home, PlusCircle, History, BarChart3, Settings } from "lucide-react";
import { useLocation } from "react-router-dom";

function Sidebar() {
  const location = useLocation();
  return (
    <div className="w-64 h-screen bg-[#0F172A] text-white flex flex-col p-5">
      {/* Logo */}
      <h1 className="text-2xl font-bold mb-10 text-green-400">FinAI</h1>

      {/* Menu */}
      <nav className="flex flex-col gap-4">
        <div
          className={`flex items-center gap-3 p-2 rounded-lg cursor-pointer ${
            location.pathname === "/"
              ? "bg-gray-800 text-green-400"
              : "hover:bg-gray-800"
          }`}
        >
          <Home size={18} />
          Dashboard
        </div>

        <div className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-800 cursor-pointer">
          <PlusCircle size={18} />
          <span>New Project</span>
        </div>

        <div className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-800 cursor-pointer">
          <History size={18} />
          <span>History</span>
        </div>

        <div className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-800 cursor-pointer">
          <BarChart3 size={18} />
          <span>Reports</span>
        </div>

        <div className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-800 cursor-pointer mt-auto">
          <Settings size={18} />
          <span>Settings</span>
        </div>
      </nav>
    </div>
  );
}

export default Sidebar;
