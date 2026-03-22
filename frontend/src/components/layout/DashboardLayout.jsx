import React from "react";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

function DashboardLayout({ children }) {
  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Section */}
      <div className="flex-1 flex flex-col bg-[#F8FAFC]">
        {/* Topbar */}
        <Topbar />

        {/* Content */}
        <div className="flex-1 p-4 overflow-auto">{children}</div>
      </div>
    </div>
  );
}

export default DashboardLayout;
