import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Upload, FileText, Loader2, CheckCircle2 } from "lucide-react";

function ProjectForm() {
  const navigate = useNavigate();
  const storedUser = sessionStorage.getItem("user");
  const user = storedUser ? JSON.parse(storedUser) : null;

  const [step, setStep] = useState("upload"); // upload | review
  const [file, setFile] = useState(null);
  const [extracting, setExtracting] = useState(false);
  const [extractError, setExtractError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const [formData, setFormData] = useState({
    projectName: "",
    initialInvestment: "",
    revenueGrowthRate: "",
    inflationRate: "",
    discountRate: "",
    marketGrowthIndex: "",
    sectorRiskIndex: "",
  });

  const [errors, setErrors] = useState({});

  const handleFileChange = (e) => {
    const selected = e.target.files?.[0];
    if (selected) {
      setFile(selected);
      setExtractError("");
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  // Convert decimal rates from Gemini (0.10) → percentage for the form (10)
  const toPercent = (val) => {
    if (val === null || val === undefined || val === "") return "";
    const n = Number(val);
    if (Number.isNaN(n)) return "";
    // If already looks like a percentage (> 1), leave it; else treat as decimal
    return n <= 1 ? (n * 100).toFixed(2) : n.toFixed(2);
  };

  const handleExtract = async () => {
    if (!file) {
      setExtractError("Please select a file first");
      return;
    }

    setExtracting(true);
    setExtractError("");

    try {
      const body = new FormData();
      body.append("file", file);

      const res = await axios.post("http://localhost:8001/extract", body, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const data = res.data;

      setFormData((prev) => ({
        ...prev,
        projectName: data.projectName || "",
        initialInvestment:
            data.initialInvestment != null
                ? String(Math.round(data.initialInvestment))
                : "",
        revenueGrowthRate: toPercent(data.revenueGrowthRate),
        inflationRate: toPercent(data.inflationRate),
        discountRate: toPercent(data.discountRate),
      }));

      setStep("review");
    } catch (err) {
      console.error(err);
      setExtractError(
          err.response?.data?.detail ||
          "Failed to extract project details. Check the extraction service is running."
      );
    } finally {
      setExtracting(false);
    }
  };

  const validate = () => {
    const newErrors = {};

    if (!formData.projectName.trim()) {
      newErrors.projectName = "Project name is required";
    }
    if (Number(formData.initialInvestment) <= 0) {
      newErrors.initialInvestment = "Must be greater than 0";
    }
    if (
        formData.revenueGrowthRate === "" ||
        Number(formData.revenueGrowthRate) < 0 ||
        Number(formData.revenueGrowthRate) > 100
    ) {
      newErrors.revenueGrowthRate = "Enter % between 0–100";
    }
    if (
        formData.inflationRate === "" ||
        Number(formData.inflationRate) < 0 ||
        Number(formData.inflationRate) > 100
    ) {
      newErrors.inflationRate = "Enter % between 0–100";
    }
    if (
        formData.discountRate === "" ||
        Number(formData.discountRate) <= 0 ||
        Number(formData.discountRate) > 100
    ) {
      newErrors.discountRate = "Enter % between 0–100";
    }
    if (!formData.marketGrowthIndex) {
      newErrors.marketGrowthIndex = "Select market growth";
    }
    if (!formData.sectorRiskIndex) {
      newErrors.sectorRiskIndex = "Select sector risk";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const evaluateProject = async () => {
    if (!user || !user.userId) {
      alert("User not logged in");
      return;
    }
    if (!validate()) return;

    setSubmitting(true);
    try {
      const payload = {
        projectName: formData.projectName,
        userId: user.userId,
        initialInvestment: Number(formData.initialInvestment),
        revenueGrowthRate: Number(formData.revenueGrowthRate),
        inflationRate: Number(formData.inflationRate),
        discountRate: Number(formData.discountRate),
        marketGrowthIndex: formData.marketGrowthIndex,
        sectorRiskIndex: formData.sectorRiskIndex,
      };

      const res = await axios.post("http://localhost:8080/projects", payload);
      sessionStorage.setItem("projectResult", JSON.stringify(res.data));
      navigate(`/dashboard/${res.data.projectId}`, { state: res.data });
    } catch (err) {
      console.error(err);
      alert("Error evaluating project");
    } finally {
      setSubmitting(false);
    }
  };

  // ---------- UPLOAD STEP ----------
  if (step === "upload") {
    return (
        <div className="max-w-2xl mx-auto">
          <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-200 text-center space-y-6">
            <div className="mx-auto w-16 h-16 rounded-2xl bg-slate-100 flex items-center justify-center">
              <FileText className="w-8 h-8 text-slate-600" />
            </div>

            <div>
              <h2 className="text-xl font-semibold text-slate-800">
                Start a New Project
              </h2>
              <p className="text-sm text-slate-500 mt-2">
                Upload your business report and we’ll extract the financial
                inputs for you.
              </p>
            </div>

            <label className="block cursor-pointer">
              <div className="border-2 border-dashed border-slate-200 rounded-2xl p-10 hover:border-slate-400 transition">
                <Upload className="w-8 h-8 text-slate-400 mx-auto mb-3" />
                <p className="text-sm font-medium text-slate-700">
                  {file ? file.name : "Upload Report"}
                </p>
                <p className="text-xs text-slate-400 mt-1">PDF • DOCX • TXT</p>
              </div>
              <input
                  type="file"
                  accept=".pdf,.docx,.txt"
                  className="hidden"
                  onChange={handleFileChange}
              />
            </label>

            {extractError && (
                <p className="text-sm text-red-500">{extractError}</p>
            )}

            <button
                onClick={handleExtract}
                disabled={!file || extracting}
                className="w-full bg-slate-800 text-white py-3 rounded-2xl font-medium hover:bg-slate-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {extracting ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    Analyzing document...
                  </>
              ) : (
                  "Analyze Document"
              )}
            </button>

            <button
                type="button"
                onClick={() => setStep("review")}
                className="text-sm text-slate-500 hover:text-slate-700 underline"
            >
              Skip upload — enter details manually
            </button>
          </div>
        </div>
    );
  }

  // ---------- REVIEW STEP ----------
  return (
      <div className="max-w-4xl mx-auto space-y-8">
        {file && (
            <div className="flex items-center gap-2 text-sm text-emerald-700 bg-emerald-50 border border-emerald-100 rounded-xl px-4 py-3">
              <CheckCircle2 className="w-4 h-4" />
              Extracted from <span className="font-medium">{file.name}</span>. You
              can edit any value before running the analysis.
            </div>
        )}

        {/* Project Info */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
          <h2 className="text-lg font-semibold text-slate-800 mb-4">
            Project Info
          </h2>
          <input
              type="text"
              name="projectName"
              value={formData.projectName}
              placeholder="Project Name"
              className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-300 text-sm"
              onChange={handleChange}
          />
          {errors.projectName && (
              <p className="text-red-500 text-sm mt-1">{errors.projectName}</p>
          )}
        </div>

        {/* Financial Inputs */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 space-y-4">
          <h2 className="text-lg font-semibold text-slate-800">
            Financial Inputs
          </h2>

          <div>
            <label className="text-xs text-slate-500 mb-1 block">
              Initial Investment (₹)
            </label>
            <input
                type="number"
                name="initialInvestment"
                value={formData.initialInvestment}
                placeholder="Initial Investment"
                className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-300 text-sm"
                onChange={handleChange}
            />
            {errors.initialInvestment && (
                <p className="text-red-500 text-sm">{errors.initialInvestment}</p>
            )}
          </div>

          <div>
            <label className="text-xs text-slate-500 mb-1 block">
              Revenue Growth Rate (%)
            </label>
            <input
                type="number"
                name="revenueGrowthRate"
                value={formData.revenueGrowthRate}
                placeholder="Revenue Growth Rate (%)"
                className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-300 text-sm"
                onChange={handleChange}
            />
            {errors.revenueGrowthRate && (
                <p className="text-red-500 text-sm">{errors.revenueGrowthRate}</p>
            )}
          </div>

          <div>
            <label className="text-xs text-slate-500 mb-1 block">
              Inflation Rate (%)
            </label>
            <input
                type="number"
                name="inflationRate"
                value={formData.inflationRate}
                placeholder="Inflation Rate (%)"
                className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-300 text-sm"
                onChange={handleChange}
            />
            {errors.inflationRate && (
                <p className="text-red-500 text-sm">{errors.inflationRate}</p>
            )}
          </div>

          <div>
            <label className="text-xs text-slate-500 mb-1 block">
              Discount Rate (%)
            </label>
            <input
                type="number"
                name="discountRate"
                value={formData.discountRate}
                placeholder="Discount Rate (%)"
                className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-300 text-sm"
                onChange={handleChange}
            />
            {errors.discountRate && (
                <p className="text-red-500 text-sm">{errors.discountRate}</p>
            )}
          </div>
        </div>

        {/* Market & Risk */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 space-y-4">
          <h2 className="text-lg font-semibold text-slate-800">Market & Risk</h2>
          <p className="text-xs text-slate-500">
            These are not extracted from the document — choose based on your
            research.
          </p>

          <div>
            <label className="text-xs text-slate-500 mb-1 block">
              Market Growth
            </label>
            <select
                value={formData.marketGrowthIndex}
                onChange={(e) =>
                    setFormData({ ...formData, marketGrowthIndex: e.target.value })
                }
                className="w-full px-4 py-3 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-slate-300"
            >
              <option value="">Select Market Growth</option>
              <option value="LOW">Low Growth</option>
              <option value="MEDIUM">Moderate Growth</option>
              <option value="HIGH">High Growth</option>
            </select>
            {errors.marketGrowthIndex && (
                <p className="text-red-500 text-sm">{errors.marketGrowthIndex}</p>
            )}
          </div>

          <div>
            <label className="text-xs text-slate-500 mb-1 block">
              Sector Risk
            </label>
            <select
                value={formData.sectorRiskIndex}
                onChange={(e) =>
                    setFormData({ ...formData, sectorRiskIndex: e.target.value })
                }
                className="w-full px-4 py-3 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-slate-300"
            >
              <option value="">Select Sector Risk</option>
              <option value="LOW">Low Risk</option>
              <option value="MEDIUM">Moderate Risk</option>
              <option value="HIGH">High Risk</option>
            </select>
            {errors.sectorRiskIndex && (
                <p className="text-red-500 text-sm">{errors.sectorRiskIndex}</p>
            )}
          </div>
        </div>

        <div className="flex gap-3">
          <button
              type="button"
              onClick={() => setStep("upload")}
              className="px-6 py-3 rounded-2xl border border-slate-200 text-slate-700 font-medium hover:bg-slate-50 transition"
          >
            Back
          </button>
          <button
              onClick={evaluateProject}
              disabled={submitting}
              className="flex-1 bg-slate-800 text-white py-3 rounded-2xl font-medium hover:bg-slate-700 transition disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {submitting ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Evaluating...
                </>
            ) : (
                "Run Analysis →"
            )}
          </button>
        </div>
      </div>
  );
}

export default ProjectForm;