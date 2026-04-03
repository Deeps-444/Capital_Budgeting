import React from "react";
import { useNavigate } from "react-router-dom";

function Topbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    sessionStorage.removeItem("user");
    navigate("/login");
  };

  return (
    <div className="w-full bg-white border-b border-slate-200 px-6 py-4 flex justify-between items-center">
      {/* Left */}
      <div>
        <h2 className="text-lg font-semibold text-slate-800">
          Project Dashboard
        </h2>
        <p className="text-sm text-slate-500">Scenario: Base Case</p>
      </div>

      {/* Right */}
      <div className="flex items-center gap-5">
        {/* Date */}
        <div className="text-sm text-slate-500">March 2026</div>

        {/* Logout */}
        <button
          onClick={handleLogout}
          className="text-sm font-medium text-red-500 hover:text-red-600 transition"
        >
          Logout
        </button>

        {/* Avatar */}
        <div className="w-9 h-9 bg-slate-800 text-white flex items-center justify-center rounded-full text-sm font-semibold">
          U
        </div>
      </div>
    </div>
  );
}

export default Topbar;
