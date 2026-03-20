import React from "react";
import { useNavigate } from "react-router-dom";

function Topbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    sessionStorage.removeItem("user"); // clear login
    navigate("/login"); // redirect
  };

  return (
    <div className="w-full bg-white shadow px-6 py-4 flex justify-between items-center">
      {/* Left */}
      <div>
        <h2 className="text-lg font-semibold text-gray-800">
          Project Dashboard
        </h2>
        <p className="text-sm text-gray-500">Scenario: Base Case</p>
      </div>

      {/* Right */}
      <div className="flex items-center gap-4">
        {/* Date */}
        <div className="text-sm text-gray-600">March 2026</div>

        {/* Logout Button */}
        <button
          onClick={handleLogout}
          className="text-sm text-red-500 hover:text-red-600 font-medium"
        >
          Logout
        </button>

        {/* Avatar */}
        <div className="w-8 h-8 bg-green-500 text-white flex items-center justify-center rounded-full">
          U
        </div>
      </div>
    </div>
  );
}

export default Topbar;
