import React from "react";

function Button({ children, onClick, className = "" }) {
  return (
    <button
      onClick={onClick}
      className={`bg-slate-800 hover:bg-slate-700 text-white px-5 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 shadow-sm hover:shadow-md ${className}`}
    >
      {children}
    </button>
  );
}

export default Button;
