import React from "react";
import "../../../chartConfig"
import Card from "../../../components/ui/Card";
import KPIBox from "../../../components/ui/KPIBox";
import CashflowChart from "../../../components/charts/CashflowChart";
import RiskDonut from "../../../components/charts/RiskDonut";
function safeNumber(value, fallback = 0) {
  const n = Number(value);
  return Number.isFinite(n) ? n : fallback;
}

function getPosition(value, min, max) {
  if (max === min) return 50;
  return ((value - min) / (max - min)) * 100;
}

function ProbabilityBar({ label, value }) {
  const probability = Math.max(0, Math.min(1, safeNumber(value)));

  return (
    <div className="v2-probability-row">
      <div className="v2-probability-label">
        <span>{label}</span>
        <strong>{formatPercent(probability)}</strong>
      </div>

      <div className="v2-probability-track">
        <div
          className="v2-probability-fill"
          style={{ width: `${probability * 100}%` }}
        />
      </div>
    </div>
  );
}
function formatCurrency(value) {
  if (
    value === null ||
    value === undefined ||
    !Number.isFinite(Number(value))
  ) {
    return "N/A";
  }

  return `₹${Number(value).toLocaleString("en-IN", {
    maximumFractionDigits: 0,
  })}`;
}

function formatPercent(value) {
  if (
    value === null ||
    value === undefined ||
    !Number.isFinite(Number(value))
  ) {
    return "N/A";
  }

  return `${(Number(value) * 100).toFixed(1)}%`;
}

function V2ResultsDashboard({ prediction }) {
  if (!prediction) return null;

  const monteCarlo = prediction.monteCarlo || {};
  const percentiles = monteCarlo.percentiles || {};
  const forecast = prediction.forecast || {};
  const risk = prediction.risk || {};
  const complexity = prediction.complexity || {};
  const bbnPredictions = prediction.bbn?.yearlyPredictions || [];
  const comparables = prediction.cbr?.comparables || [];
  const explainability = prediction.explainability || {};
  const financialExplanation = explainability.financial || {};
  const assumptions = prediction.futureAssumptions || {};

  const cashflows = (forecast.predictedCashFlows || []).map(
    (cashflow, index) => ({
      year: index + 1,
      cashflow,
    }),
  );

  const probabilityNegative = Number(monteCarlo.probabilityNPVNegative || 0);

  const decisionIsNegative = Number(monteCarlo.meanNPV) < 0;

  return (
    <div className="v2-results-dashboard">
      {/* ===================================================== */}
      {/* HEADER */}
      {/* ===================================================== */}

      <div className="v2-dashboard-header">
        <div>
          <div className="v2-dashboard-eyebrow">CAPITAL BUDGETING DSS</div>

          <h2>Project Investment Analysis</h2>

          <p>
            Forecast, risk and financial decision support generated from the
            project inputs and approved assumptions.
          </p>
        </div>

        <div className="v2-method-badge">
          <span>Forecasting Method</span>
          <strong>{forecast.method || "Not available"}</strong>
        </div>
      </div>

      {/* ===================================================== */}
      {/* PROJECT SNAPSHOT */}
      {/* ===================================================== */}

      <div className="v2-project-snapshot">
        <div>
          <span>Project Type</span>
          <strong>{prediction.project?.project_type || "—"}</strong>
        </div>

        <div>
          <span>Scale</span>
          <strong>{prediction.project?.project_scale || "—"}</strong>
        </div>

        <div>
          <span>Duration</span>
          <strong>
            {prediction.project?.project_duration_years || "—"} years
          </strong>
        </div>

        <div>
          <span>Initial Investment</span>
          <strong>
            {formatCurrency(prediction.project?.initial_investment)}
          </strong>
        </div>
      </div>

      {/* ===================================================== */}
      {/* DECISION SUMMARY */}
      {/* ===================================================== */}

      <section className="v2-dashboard-section">
        <div className="v2-section-heading">
          <div>
            <h3>Investment Decision Summary</h3>
            <p>The key financial indicators from the simulation.</p>
          </div>

          <div
            className={`v2-decision-badge ${
              decisionIsNegative
                ? "v2-decision-negative"
                : "v2-decision-positive"
            }`}
          >
            {decisionIsNegative
              ? "Higher financial concern"
              : "Positive expected outcome"}
          </div>
        </div>

        <div className="v2-dashboard-kpis">
          <KPIBox
            title="Expected NPV"
            value={formatCurrency(monteCarlo.meanNPV)}
            border={
              decisionIsNegative ? "border-red-500" : "border-emerald-500"
            }
          />

          <KPIBox
            title="Median NPV"
            value={formatCurrency(monteCarlo.medianNPV)}
            border="border-slate-500"
          />

          <KPIBox
            title="Probability of Loss"
            value={formatPercent(probabilityNegative)}
            border="border-red-500"
          />

          <KPIBox
            title="Forecast Horizon"
            value={`${forecast.horizonYears || cashflows.length} Years`}
            border="border-blue-500"
          />
        </div>

        <div
          className={`v2-decision-summary ${
            decisionIsNegative ? "v2-summary-negative" : "v2-summary-positive"
          }`}
        >
          <div className="v2-summary-icon">
            {decisionIsNegative ? "!" : "✓"}
          </div>

          <div>
            <strong>
              {decisionIsNegative
                ? "The simulated expected NPV is negative."
                : "The simulated expected NPV is positive."}
            </strong>

            <p>
              {decisionIsNegative
                ? "The project shows financial downside under the current assumptions. Review the risk exposure and assumptions before making an investment decision."
                : "Under the current assumptions, the project has a positive expected financial outcome. The probability of loss should still be considered alongside the expected NPV."}
            </p>
          </div>
        </div>
      </section>

      {/* ===================================================== */}
      {/* CASH FLOW + RISK */}
      {/* ===================================================== */}

      <div className="v2-dashboard-two-col">
        <Card>
          <div className="v2-card-heading">
            <div>
              <h3>Predicted Project Cash Flows</h3>
              <p>Forecasted cash flow trajectory over the project horizon.</p>
            </div>
          </div>

          <div className="v2-chart-container">
            <CashflowChart cashflows={cashflows} />
          </div>
        </Card>

        <Card>
          <div className="v2-card-heading">
            <div>
              <h3>Probability of Financial Loss</h3>
              <p>Probability that simulated NPV falls below zero.</p>
            </div>
          </div>

          <div className="v2-risk-visual">
            <RiskDonut risk={probabilityNegative} />

            <div className="v2-risk-number">
              <strong>{formatPercent(probabilityNegative)}</strong>

              <span>Probability of negative NPV</span>
            </div>
          </div>

          <div className="v2-risk-interpretation">
            {probabilityNegative < 0.2
              ? "Relatively low simulated downside probability."
              : probabilityNegative < 0.5
                ? "The project has a meaningful level of financial uncertainty."
                : "The project has substantial simulated downside risk."}
          </div>
        </Card>
      </div>

      {/* ===================================================== */}
      {/* MONTE CARLO */}
      {/* ===================================================== */}

      <section className="v2-dashboard-section">
        <div className="v2-section-heading">
          <div>
            <h3>Monte Carlo Financial Risk Simulation</h3>

            <p>
              The simulation evaluates how uncertainty in project cash flows
              affects the resulting NPV.
            </p>
          </div>

          <span className="v2-section-tag">
            {monteCarlo.simulations
              ? `${monteCarlo.simulations.toLocaleString()} simulations`
              : "Simulation"}
          </span>
        </div>

        <div className="v2-dashboard-kpis v2-mc-kpis">
          <KPIBox
            title="Mean NPV"
            value={formatCurrency(monteCarlo.meanNPV)}
            border="border-blue-500"
          />

          <KPIBox
            title="Median NPV"
            value={formatCurrency(monteCarlo.medianNPV)}
            border="border-slate-500"
          />

          <KPIBox
            title="Standard Deviation"
            value={formatCurrency(monteCarlo.stdNPV)}
            border="border-yellow-500"
          />

          <KPIBox
            title="Probability of Loss"
            value={formatPercent(probabilityNegative)}
            border="border-red-500"
          />
        </div>

        {/* Monte Carlo range visualization */}

        <div className="v2-monte-carlo-visual">
          <div className="v2-mc-visual-header">
            <div>
              <strong>Simulated NPV Outcome Range</strong>
              <span>
                P10 → P90 represents the central simulation outcome range.
              </span>
            </div>
          </div>

          {(() => {
            const p10 = safeNumber(percentiles.p10);
            const p25 = safeNumber(percentiles.p25);
            const median = safeNumber(monteCarlo.medianNPV);
            const p75 = safeNumber(percentiles.p75);
            const p90 = safeNumber(percentiles.p90);

            const values = [p10, p25, median, p75, p90];

            const min = Math.min(...values);
            const max = Math.max(...values);

            const zeroVisible = min < 0 && max > 0;

            return (
              <>
                <div className="v2-mc-range">
                  <div className="v2-mc-track" />

                  <div
                    className="v2-mc-iqr"
                    style={{
                      left: `${getPosition(p25, min, max)}%`,
                      width: `${
                        getPosition(p75, min, max) - getPosition(p25, min, max)
                      }%`,
                    }}
                  />

                  {zeroVisible && (
                    <div
                      className="v2-mc-zero"
                      style={{
                        left: `${getPosition(0, min, max)}%`,
                      }}
                    >
                      <span>₹0</span>
                    </div>
                  )}

                  {[
                    ["P10", p10],
                    ["P25", p25],
                    ["Median", median],
                    ["P75", p75],
                    ["P90", p90],
                  ].map(([label, value]) => (
                    <div
                      key={label}
                      className={`v2-mc-marker ${
                        label === "Median" ? "v2-mc-marker-main" : ""
                      }`}
                      style={{
                        left: `${getPosition(value, min, max)}%`,
                      }}
                    >
                      <div className="v2-mc-marker-dot" />

                      <div className="v2-mc-marker-label">
                        <strong>{label}</strong>
                        <span>{formatCurrency(value)}</span>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="v2-mc-legend">
                  <span>
                    <i className="v2-legend-dot" />
                    P25–P75: central 50% of outcomes
                  </span>

                  <span>
                    <i className="v2-legend-line" />
                    ₹0: break-even
                  </span>
                </div>
              </>
            );
          })()}
        </div>

        {/* Percentile cards */}

        <div className="v2-percentile-grid">
          {[
            ["P10", percentiles.p10, "Downside"],
            ["P25", percentiles.p25, "Lower range"],
            ["Median", monteCarlo.medianNPV, "Typical outcome"],
            ["P75", percentiles.p75, "Upper range"],
            ["P90", percentiles.p90, "Upside"],
          ].map(([label, value, description]) => (
            <div
              className={`v2-percentile-item ${
                label === "Median" ? "v2-percentile-highlight" : ""
              }`}
              key={label}
            >
              <span>{label}</span>
              <strong>{formatCurrency(value)}</strong>
              <small>{description}</small>
            </div>
          ))}
        </div>
      </section>

      {/* ===================================================== */}
      {/* BAYESIAN RISK */}
      {/* ===================================================== */}

      <section className="v2-dashboard-section">
        <div className="v2-section-heading">
          <div>
            <h3>Bayesian Cash-Flow Risk Analysis</h3>

            <p>
              Probability of each cash-flow deviation state for every forecast
              year.
            </p>
          </div>

          <span className="v2-section-tag">Year-wise risk</span>
        </div>

        <div className="v2-bbn-visual">
          {bbnPredictions.map((item) => {
            const better = safeNumber(item.probabilities?.Better);

            const expected = safeNumber(item.probabilities?.["Near Expected"]);

            const worse = safeNumber(item.probabilities?.Worse);

            return (
              <div className="v2-bbn-visual-row" key={item.year}>
                <div className="v2-bbn-year">
                  <strong>Year {item.year}</strong>

                  <span>
                    Most likely: <b>{item.most_likely_state}</b>
                  </span>
                </div>

                <div className="v2-bbn-bars">
                  <ProbabilityBar label="Better" value={better} />

                  <ProbabilityBar label="Near Expected" value={expected} />

                  <ProbabilityBar label="Worse" value={worse} />
                </div>
              </div>
            );
          })}
        </div>

        <div className="v2-notice">
          <strong>How to read this</strong>

          <p>
            These probabilities describe possible cash-flow deviation states for
            each year. They are not the probability of positive or negative NPV.
          </p>
        </div>
      </section>

      {/* ===================================================== */}
      {/* CBR */}
      {/* ===================================================== */}

      {comparables.length > 0 && (
        <section className="v2-dashboard-section">
          <div className="v2-section-heading">
            <div>
              <h3>Comparable Project Analysis</h3>

              <p>
                Historical projects used to construct the forecasting context
                for the current project.
              </p>
            </div>

            <span className="v2-section-tag">
              {comparables.length} comparables
            </span>
          </div>

          <div className="v2-comparables-grid">
            {comparables.map((item, index) => {
              const similarity = Math.max(
                0,
                Math.min(
                  1,
                  safeNumber(
                    item.similarity ?? item.similarity_score ?? item.score,
                  ),
                ),
              );

              return (
                <div
                  className="v2-comparable-card"
                  key={item.project_id || index}
                >
                  <div className="v2-comparable-header">
                    <strong>
                      {item.project_name ||
                        item.project_id ||
                        `Comparable ${index + 1}`}
                    </strong>

                    <span>{formatPercent(similarity)}</span>
                  </div>

                  <div className="v2-similarity-track">
                    <div
                      className="v2-similarity-fill"
                      style={{
                        width: `${similarity * 100}%`,
                      }}
                    />
                  </div>

                  <div className="v2-comparable-meta">
                    <span>Similarity</span>

                    {item.distance !== undefined && (
                      <span>Distance: {Number(item.distance).toFixed(3)}</span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>

          {prediction.cbr?.summary && (
            <div className="v2-cbr-summary">
              <strong>CBR contribution</strong>
              <p>{prediction.cbr.summary}</p>
            </div>
          )}
        </section>
      )}

      {/* ===================================================== */}
      {/* PROJECT ASSESSMENT */}
      {/* ===================================================== */}

      <div className="v2-dashboard-two-col">
        <Card>
          <div className="v2-card-heading">
            <div>
              <h3>Project Complexity</h3>
              <p>Deterministic assessment of project complexity.</p>
            </div>
          </div>

          <div className="v2-assessment-score">
            <strong>{safeNumber(complexity.index).toFixed(2)}</strong>

            <span>Complexity Index</span>
          </div>

          <div className="v2-assessment-list">
            <div>
              <span>Scale</span>
              <strong>{safeNumber(complexity.scaleScore).toFixed(2)}</strong>
            </div>

            <div>
              <span>Duration</span>
              <strong>{safeNumber(complexity.durationScore).toFixed(2)}</strong>
            </div>

            <div>
              <span>Investment</span>
              <strong>
                {safeNumber(complexity.investmentScore).toFixed(2)}
              </strong>
            </div>
          </div>
        </Card>

        <Card>
          <div className="v2-card-heading">
            <div>
              <h3>Project Risk Exposure</h3>
              <p>Aggregate exposure derived from probability × impact.</p>
            </div>
          </div>

          <div className="v2-assessment-score">
            <strong>{formatPercent(safeNumber(risk.risk_index))}</strong>

            <span>Overall Risk Index</span>
          </div>

          <div className="v2-risk-list">
            {(risk.risks || []).map((riskItem, index) => (
              <div className="v2-risk-item" key={index}>
                <div>
                  <strong>{riskItem.category}</strong>

                  <span>
                    P {formatPercent(riskItem.probability)}
                    {" · "}
                    Impact {formatPercent(riskItem.impact)}
                  </span>
                </div>

                <strong>{formatPercent(riskItem.exposure)}</strong>
              </div>
            ))}
          </div>
        </Card>
      </div>

      {/* ===================================================== */}
      {/* EXPLAINABILITY */}
      {/* ===================================================== */}

      <section className="v2-dashboard-section">
        <div className="v2-section-heading">
          <div>
            <h3>Why did the system make this forecast?</h3>

            <p>
              A concise explanation of the model choice and financial
              interpretation.
            </p>
          </div>

          <span className="v2-section-tag">Explainability</span>
        </div>

        <div className="v2-explain-grid">
          {/* Model selection */}

          <div className="v2-explain-card">
            <div className="v2-explain-number">01</div>

            <div>
              <span className="v2-explain-label">MODEL SELECTION</span>

              <h4>{forecast.method || "Forecasting model"}</h4>

              <p>
                The forecasting method was selected according to the available
                project information and historical context.
              </p>
            </div>
          </div>

          {/* Financial interpretation */}

          <div className="v2-explain-card">
            <div className="v2-explain-number">02</div>

            <div>
              <span className="v2-explain-label">FINANCIAL INTERPRETATION</span>

              <h4>
                {decisionIsNegative
                  ? "Downside requires attention"
                  : "Expected outcome is financially positive"}
              </h4>

              <p>
                Expected NPV is{" "}
                <strong>{formatCurrency(monteCarlo.meanNPV)}</strong> with a{" "}
                <strong>{formatPercent(probabilityNegative)}</strong>{" "}
                probability of negative NPV in the simulation.
              </p>
            </div>
          </div>

          {/* Model notes */}

          <div className="v2-explain-card">
            <div className="v2-explain-number">03</div>

            <div>
              <span className="v2-explain-label">MODEL NOTES</span>

              {Array.isArray(explainability.notes) &&
              explainability.notes.length > 0 ? (
                <ul className="v2-explain-notes">
                  {explainability.notes.map((note, index) => (
                    <li key={index}>{note}</li>
                  ))}
                </ul>
              ) : (
                <p>No additional model notes were returned.</p>
              )}
            </div>
          </div>
        </div>

        {financialExplanation &&
          Object.keys(financialExplanation).length > 0 && (
            <div className="v2-financial-explanation">
              <strong>Financial explanation</strong>

              <div className="v2-financial-explanation-grid">
                {Object.entries(financialExplanation).map(([key, value]) => (
                  <div key={key}>
                    <span>
                      {key
                        .replaceAll("_", " ")
                        .replace(/\b\w/g, (c) => c.toUpperCase())}
                    </span>

                    <p>{String(value)}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
      </section>

      {/* ===================================================== */}
      {/* ASSUMPTIONS */}
      {/* ===================================================== */}

      <section className="v2-dashboard-section">
        <div className="v2-section-heading">
          <div>
            <h3>Approved Forecast Assumptions</h3>

            <p>External assumptions used by the forecasting pipeline.</p>
          </div>
        </div>

        <div className="v2-assumptions-table">
          <div className="v2-assumption-header">
            <span>Year</span>
            <span>Inflation</span>
            <span>Market Growth</span>
          </div>

          {(assumptions.inflation || []).map((_, index) => (
            <div className="v2-assumption-row" key={index}>
              <strong>Year {index + 1}</strong>

              <span>{formatPercent(assumptions.inflation?.[index])}</span>

              <span>
                {formatPercent(
                  assumptions.market_growth?.[index] ??
                    assumptions.marketGrowth?.[index],
                )}
              </span>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

export default V2ResultsDashboard;
