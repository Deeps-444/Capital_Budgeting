import React from "react";

function Button({ children, onClick, className = "" }) {
  return (
    <button
      onClick={onClick}
      className={`bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition ${className}`}
    >
      {children}
    </button>
  );
}

export default Button;
