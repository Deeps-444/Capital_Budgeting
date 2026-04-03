import React from "react";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

function DashboardLayout({ children }) {
  return (
    <div className="flex h-screen bg-slate-100">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Section */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Topbar */}
        <Topbar />

        {/* Content */}
        <div className="flex-1 p-6 overflow-auto">{children}</div>
      </div>
    </div>
  );
}

export default DashboardLayout;
