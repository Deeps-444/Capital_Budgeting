import React from "react";
import Card from "./Card";

function KPIBox({ title, value, color = "text-gray-800" }) {
  return (
    <Card>
      <p className="text-xs text-gray-500">{title}</p>
      <h2 className={`text-xl font-bold mt-1 ${color}`}>{value}</h2>
    </Card>
  );
}

export default KPIBox;
