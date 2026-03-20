import React from "react";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

function DashboardLayout({ children }) {
  return (
    <div className="flex">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Section */}
      <div className="p-3 bg-[#F8FAFC] h-screen overflow-hidden">
        {/* Topbar */}
        <Topbar />

        {/* Content */}
        <div className="p-6">{children}</div>
      </div>
    </div>
  );
}

export default DashboardLayout;
