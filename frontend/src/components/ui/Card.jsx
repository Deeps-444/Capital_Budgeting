import React from "react";

function Card({ children, className = "" }) {
  return (
    <div
      className={`bg-white rounded-2xl border border-slate-200 shadow-sm p-5 hover:shadow-md transition ${className}`}
    >
      {children}
    </div>
  );
}

export default Card;
