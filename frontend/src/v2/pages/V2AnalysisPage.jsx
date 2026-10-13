import { useState } from "react";
import DocumentUpload from "../components/DocumentUpload";
import {
    researchProjectAssumptions,
    predictProject,
  } from "../services/v2Api";
import "../V2App.css";
import V2ResultsDashboard from "../components/results/V2ResultsDashboard";

const fieldDefinitions = [
  { key: "project_name", label: "Project name", type: "text" },
  { key: "project_type", label: "Project type", type: "text" },
  { key: "project_scale", label: "Project scale", type: "text" },
  { key: "location", label: "Location", type: "text" },
  {
    key: "project_duration_years",
    label: "Duration (years)",
    type: "number",
  },
  {
    key: "initial_investment",
    label: "Initial investment (₹)",
    type: "number",
  },
  {
    key: "annual_revenue",
    label: "Annual revenue (₹)",
    type: "number",
  },
  {
    key: "annual_operating_cost",
    label: "Annual operating cost (₹)",
    type: "number",
  },
  { key: "tax_rate", label: "Tax rate (decimal)", type: "number" },
  {
    key: "discount_rate",
    label: "Discount rate (decimal)",
    type: "number",
  },
];

export default function V2AnalysisPage() {
  const [details, setDetails] = useState(null);
  const [notice, setNotice] = useState("");
  const [reviewed, setReviewed] = useState(false);
  const [research, setResearch] = useState(null);
  const [researchLoading, setResearchLoading] = useState(false);
  const [researchError, setResearchError] = useState("");
  const [assumptionsApproved, setAssumptionsApproved] = useState(false);

  const [inflation, setInflation] = useState(Array(5).fill(""));

  const [marketGrowth, setMarketGrowth] = useState(Array(5).fill(""));

  const [prediction, setPrediction] = useState(null);
  const [predictionLoading, setPredictionLoading] = useState(false);
  const [predictionError, setPredictionError] = useState("");

  const [risks, setRisks] = useState([
    {
      category: "",
      probability: "",
      impact: "",
    },
  ]);

  function handleExtracted(extractedDetails) {
    setDetails({ ...extractedDetails });
    setNotice(
      "Extraction complete. Review and correct every field before continuing.",
    );
  }

  function handleFieldChange(key, value) {
    setDetails((current) => ({
      ...current,
      [key]: value === "" ? null : value,
    }));

    setReviewed(false);
    setResearch(null);
    setResearchError("");
    setAssumptionsApproved(false);
  }

  function handleReviewSubmit(event) {
    event.preventDefault();

    const requiredFields = [
      "project_type",
      "project_scale",
      "project_duration_years",
      "initial_investment",
      "tax_rate",
      "discount_rate",
    ];

    const missing = requiredFields.filter((key) => {
      const value = details[key];
      return value === null || value === undefined || value === "";
    });

    if (missing.length) {
      setNotice(`Please complete the required fields: ${missing.join(", ")}`);
      return;
    }

    const numericFields = [
      "project_duration_years",
      "initial_investment",
      "annual_revenue",
      "annual_operating_cost",
      "tax_rate",
      "discount_rate",
    ];

    const reviewedDetails = { ...details };

    for (const key of numericFields) {
      if (
        reviewedDetails[key] !== null &&
        reviewedDetails[key] !== undefined &&
        reviewedDetails[key] !== ""
      ) {
        reviewedDetails[key] = Number(reviewedDetails[key]);
      }
    }

    if (
      reviewedDetails.project_duration_years <= 0 ||
      reviewedDetails.initial_investment <= 0 ||
      reviewedDetails.tax_rate < 0 ||
      reviewedDetails.tax_rate > 1 ||
      reviewedDetails.discount_rate < 0 ||
      reviewedDetails.discount_rate > 1
    ) {
      setNotice(
        "Check your values. Duration and investment must be positive; tax and discount rates must be between 0 and 1.",
      );
      return;
    }

    setReviewed(true);
    setResearch(null);
    setResearchError("");
    setAssumptionsApproved(false);

    setDetails(reviewedDetails);
    setNotice(
      "Details reviewed in this page. Forecasting has not started yet.",
    );

    // The next step will connect this reviewed data to the
    // assumptions and risk forms before calling /predict.
  }

  
async function handleResearch() {
  if (!details || !reviewed || researchLoading) return;

  setResearchLoading(true);
  setResearchError("");
  setResearch(null);
  setAssumptionsApproved(false);

  try {
    const result = await researchProjectAssumptions({
      project_type: details.project_type,
      project_scale: details.project_scale,
      project_duration_years: Number(details.project_duration_years),
      initial_investment: Number(details.initial_investment),
      location: details.location || "",
    });

    setResearch(result);
    console.log("FULL RESEARCH RESPONSE:", result);
    console.log("ANNUAL PROPOSALS:", result.annual_proposals);
    
    const proposals = result.proposals?.annual_proposals;

    const toFiveRates = (items = []) =>
      Array.from({ length: 5 }, (_, index) => {
        const item = items[index];
        return item?.rate_decimal != null ? String(item.rate_decimal) : "";
      });

    if (proposals) {
      setInflation(toFiveRates(proposals.inflation?.annual_proposals));

      setMarketGrowth(toFiveRates(proposals.market_growth?.annual_proposals));
    }
    } catch (err) {
      setResearchError(
        err.response?.data?.detail ||
          err.message ||
          "Web research failed. Please try again.",
      );
    } finally {
      setResearchLoading(false);
    }
}

function handleAssumptionChange(type, index, value) {
  const setter = type === "inflation" ? setInflation : setMarketGrowth;

  setter((current) => current.map((item, i) => (i === index ? value : item)));

  setAssumptionsApproved(false);
}

function handleRiskChange(index, field, value) {
  setRisks((current) =>
    current.map((risk, i) =>
      i === index
        ? {
            ...risk,
            [field]: value,
          }
        : risk,
    ),
  );

  setPrediction(null);
  setPredictionError("");
}

function addRisk() {
  setRisks((current) => [
    ...current,
    {
      category: "",
      probability: "",
      impact: "",
    },
  ]);
}

function removeRisk(index) {
  setRisks((current) => current.filter((_, i) => i !== index));
}

function approveAssumptions(event) {
  event.preventDefault();

  const values = [...inflation, ...marketGrowth];

  if (values.some((value) => value === "" || !Number.isFinite(Number(value)))) {
    setAssumptionsApproved(false);
    setResearchError(
      "Enter a numeric value for all five years in both assumption groups.",
    );
    return;
  }

  setResearchError("");
  setAssumptionsApproved(true);
}

async function handlePredict() {
  if (!details || !reviewed || !assumptionsApproved) return;

  setPredictionLoading(true);
  setPredictionError("");
  setPrediction(null);

  if (!risks.length) {
    setPredictionError(
      "Add at least one project risk before running the forecast.",
    );
    return;
  }

  const invalidRisk = risks.some((risk) => {
    const probability = Number(risk.probability);
    const impact = Number(risk.impact);

    return (
      !risk.category.trim() ||
      !Number.isFinite(probability) ||
      !Number.isFinite(impact) ||
      probability < 0 ||
      probability > 100 ||
      impact < 0 ||
      impact > 100
    );
  });

  if (invalidRisk) {
    setPredictionError(
      "Complete every risk category and enter probability and impact between 0% and 100%.",
    );
    return;
  }

  try {
    const payload = {
      project: {
        project_type: details.project_type,
        project_scale: details.project_scale,
        project_duration_years: Number(details.project_duration_years),
        initial_investment: Number(details.initial_investment),
        tax_rate: Number(details.tax_rate),
        discount_rate: Number(details.discount_rate),
      },

      risks: risks.map((risk) => ({
        category: risk.category.trim(),
        probability: Number(risk.probability) / 100,
        impact: Number(risk.impact) / 100,
      })),

      historical_cash_flows: null,

      future_assumptions: {
        inflation: inflation.map(Number),
        market_growth: marketGrowth.map(Number),
      },
    };

    console.log("PREDICTION PAYLOAD:", payload);

    const result = await predictProject(payload);

    console.log("PREDICTION RESPONSE:", result);

    setPrediction(result);
  } catch (err) {
    console.error("PREDICTION ERROR:", err);

    setPredictionError(
      err.response?.data?.detail ||
        err.message ||
        "Prediction failed. Please try again.",
    );
  } finally {
    setPredictionLoading(false);
  }
}

  return (
    <main className="v2-page">
      <header className="v2-header">
        <div className="v2-brand-mark">CB</div>
        <div>
          <p className="v2-eyebrow">CAPITAL BUDGETING DSS</p>
          <h1>Project Analysis</h1>
        </div>
        <span className="v2-version">V2 · ML Pipeline</span>
      </header>

      <section className="v2-intro">
        <p className="v2-eyebrow">INVESTMENT DECISION WORKSPACE</p>
        <h2>Turn your project proposal into a financial analysis.</h2>
        <p>
          Start with a project document. Review the extracted information before
          supplying assumptions and running the forecasting pipeline.
        </p>
      </section>

      <DocumentUpload onExtracted={handleExtracted} />

      {details && (
        <section className="v2-review-card">
          <div className="v2-section-heading">
            <span className="v2-step-number">02</span>
            <div>
              <h2>Review project details</h2>
              <p>
                Verify the extracted values and fill in anything missing. Rates
                are decimals: 0.12 means 12%.
              </p>
            </div>
          </div>

          <form onSubmit={handleReviewSubmit}>
            <div className="v2-fields-grid">
              {fieldDefinitions.map((field) => (
                <label className="v2-field" key={field.key}>
                  <span>{field.label}</span>
                  <input
                    type={field.type}
                    step={field.type === "number" ? "any" : undefined}
                    value={details[field.key] ?? ""}
                    onChange={(event) =>
                      handleFieldChange(field.key, event.target.value)
                    }
                  />
                </label>
              ))}
            </div>

            <p className="v2-helper-text">
              Required for forecasting: project type, scale, duration,
              investment, tax rate, and discount rate.
            </p>

            <button type="submit" className="v2-primary-button">
              Save reviewed details
            </button>
          </form>

          {notice && (
            <div className="v2-notice" role="status">
              {notice}
            </div>
          )}
        </section>
      )}

      {details && (
        <section className="v2-review-card">
          <div className="v2-section-header">
            <div className="v2-step-number">03</div>

            <div>
              <h2>Research future assumptions</h2>
              <p>
                Retrieve evidence for inflation and market growth, then decide
                which yearly rates to use.
              </p>
            </div>
          </div>

          <button
            type="button"
            className="v2-primary-button"
            onClick={handleResearch}
            disabled={!reviewed || researchLoading}
          >
            {researchLoading
              ? "Researching sources…"
              : "Research assumptions on the web"}
          </button>

          {!reviewed && (
            <p className="v2-helper-text">
              Save the reviewed project details first to enable research.
            </p>
          )}

          {researchError && (
            <div className="v2-error" role="alert">
              {researchError}
            </div>
          )}

          {research && (
            <div className="v2-research-results">
              <h3>Research status</h3>
              <p className="v2-helper-text">
                {research.research?.message ||
                  "Review the retrieved evidence before choosing your assumptions."}
              </p>

              {[
                {
                  key: "inflation",
                  label: "Inflation sources",
                },
                {
                  key: "market_growth",
                  label: "Market-growth sources",
                },
              ].map((topic) => {
                const sources = research.research?.sources?.[topic.key] || [];

                return (
                  <div key={topic.key} className="v2-source-group">
                    <h3>{topic.label}</h3>

                    {sources.length === 0 ? (
                      <p className="v2-helper-text">
                        No sources were returned for this topic.
                      </p>
                    ) : (
                      sources.map((source, index) => (
                        <article
                          className="v2-source-card"
                          key={`${source.url || source.title || topic.key}-${index}`}
                        >
                          <a href={source.url} target="_blank" rel="noreferrer">
                            {source.title || "Open research source"}
                          </a>

                          {source.domain && (
                            <span className="v2-source-domain">
                              {source.domain}
                            </span>
                          )}

                          {source.snippet && <p>{source.snippet}</p>}

                          {source.published_date && (
                            <span className="v2-source-domain">
                              Published: {source.published_date}
                            </span>
                          )}
                        </article>
                      ))
                    )}
                  </div>
                );
              })}

              <div className="v2-notice">
                Web sources provide evidence, not automatically approved
                forecasts. Enter the rates you want to use below.
              </div>

              <form onSubmit={approveAssumptions}>
                <h3>Five-year assumptions</h3>
                <p className="v2-helper-text">
                  Use decimals: 0.05 means 5%. These values will be supplied to
                  the model for each forecast year.
                </p>

                <div className="v2-fields-grid">
                  {Array.from({ length: 5 }, (_, index) => (
                    <label className="v2-field" key={`inflation-${index}`}>
                      <span>Year {index + 1} — Inflation rate</span>
                      <input
                        type="number"
                        step="any"
                        value={inflation[index]}
                        onChange={(event) =>
                          handleAssumptionChange(
                            "inflation",
                            index,
                            event.target.value,
                          )
                        }
                        required
                      />
                    </label>
                  ))}

                  {Array.from({ length: 5 }, (_, index) => (
                    <label className="v2-field" key={`growth-${index}`}>
                      <span>Year {index + 1} — Market-growth rate</span>
                      <input
                        type="number"
                        step="any"
                        value={marketGrowth[index]}
                        onChange={(event) =>
                          handleAssumptionChange(
                            "marketGrowth",
                            index,
                            event.target.value,
                          )
                        }
                        required
                      />
                    </label>
                  ))}
                </div>

                <button type="submit" className="v2-primary-button">
                  Approve five-year assumptions
                </button>
              </form>

              {assumptionsApproved && (
                <section className="v2-risk-section">
                  <div className="v2-notice" role="status">
                    Assumptions approved for this session.
                  </div>

                  <div className="v2-section-heading">
                    <span className="v2-step-number">04</span>

                    <div>
                      <p className="v2-eyebrow">PROJECT RISK INPUTS</p>
                      <h2>Identify project risks</h2>

                      <p>
                        Add the major risks that could affect project
                        performance. Probability and impact should be entered as
                        percentages.
                      </p>
                    </div>
                  </div>

                  <div className="v2-risk-list">
                    {risks.map((risk, index) => {
                      const probability = Number(risk.probability);
                      const impact = Number(risk.impact);

                      const exposure =
                        Number.isFinite(probability) && Number.isFinite(impact)
                          ? (probability * impact) / 100
                          : null;

                      return (
                        <div className="v2-risk-card" key={index}>
                          <div className="v2-risk-card-header">
                            <h3>Risk {index + 1}</h3>

                            {risks.length > 1 && (
                              <button
                                type="button"
                                className="v2-remove-risk-button"
                                onClick={() => removeRisk(index)}
                              >
                                Remove
                              </button>
                            )}
                          </div>

                          <label className="v2-field">
                            <span>Risk category</span>

                            <input
                              type="text"
                              placeholder="e.g. Construction delay"
                              value={risk.category}
                              onChange={(event) =>
                                handleRiskChange(
                                  index,
                                  "category",
                                  event.target.value,
                                )
                              }
                            />
                          </label>

                          <div className="v2-risk-input-grid">
                            <label className="v2-field">
                              <span>Probability (%)</span>

                              <input
                                type="number"
                                min="0"
                                max="100"
                                step="any"
                                placeholder="e.g. 40"
                                value={risk.probability}
                                onChange={(event) =>
                                  handleRiskChange(
                                    index,
                                    "probability",
                                    event.target.value,
                                  )
                                }
                              />
                            </label>

                            <label className="v2-field">
                              <span>Impact (%)</span>

                              <input
                                type="number"
                                min="0"
                                max="100"
                                step="any"
                                placeholder="e.g. 60"
                                value={risk.impact}
                                onChange={(event) =>
                                  handleRiskChange(
                                    index,
                                    "impact",
                                    event.target.value,
                                  )
                                }
                              />
                            </label>
                          </div>

                          {exposure !== null && (
                            <div className="v2-risk-exposure">
                              <span>Risk exposure</span>

                              <strong>{exposure.toFixed(1)}%</strong>

                              <small>Probability × Impact</small>
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>

                  <button
                    type="button"
                    className="v2-secondary-button"
                    onClick={addRisk}
                  >
                    + Add another risk
                  </button>

                  <div className="v2-risk-action">
                    <button
                      type="button"
                      className="v2-primary-button"
                      onClick={handlePredict}
                      disabled={predictionLoading}
                    >
                      {predictionLoading
                        ? "Running forecasting pipeline…"
                        : "Run financial forecast"}
                    </button>
                  </div>
                </section>
              )}
            </div>
          )}
        </section>
      )}

      {prediction && <V2ResultsDashboard prediction={prediction} />}
      {predictionError && (
        <div className="v2-error" role="alert">
          {predictionError}
        </div>
      )}
    </main>
  );
}
