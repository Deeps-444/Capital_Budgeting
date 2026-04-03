import React from "react";
import Card from "./Card";

function KPIBox({ title, value, color = "text-slate-800", border = "" }) {
  return (
    <Card className={`border-l-4 ${border}`}>
      <p className="text-xs text-slate-500">{title}</p>
      <h2 className={`text-2xl font-semibold mt-1 ${color}`}>{value}</h2>
    </Card>
  );
}

export default KPIBox;
