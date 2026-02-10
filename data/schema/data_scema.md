# Capital Budgeting Dataset Schema

## Description
This dataset is used for a Decision Support System for Capital Budgeting.
It combines company financial indicators with simulated project-level data.

## Features

| Column Name | Data Type | Description |
|------------|----------|-------------|
| company_name | String | Name of the company |
| sector | String | Industry sector |
| revenue | Float | Latest annual revenue |
| operating_income | Float | Operating income |
| net_income | Float | Net income |
| ebitda | Float | EBITDA |
| initial_investment | Float | Initial project cost |
| cashflow_y1 | Float | Cash flow year 1 |
| cashflow_y2 | Float | Cash flow year 2 |
| cashflow_y3 | Float | Cash flow year 3 |
| discount_rate | Float | Cost of capital |
| risk_score | Integer | Risk level (1–10) |
| npv | Float | Net Present Value |
| irr | Float | Internal Rate of Return |
| payback_period | Float | Payback period (years) |
| decision | String | Accept / Reject |

## Target Variable
- decision
