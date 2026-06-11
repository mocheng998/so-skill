---
name: ecommerce-budget-forecaster
description: "Build rolling operating budgets for revenue, marketing, and inventory with seasonal adjustments, variance analysis, and performance benchmarks."
---

# Build Ecommerce Operating Budget and Forecast

## Overview

A rolling operating budget is the financial backbone of an ecommerce business. Unlike a static annual budget, a rolling budget advances one month with each passing period, typically maintaining a 12-month forward view. This methodology allows operators to adjust marketing spend and inventory procurement based on real-time performance and shifting market conditions.

The three critical pillars of ecommerce budgeting are **Revenue Forecasting**, **Marketing Allocation**, and **Inventory Open-to-Buy (OTB)**.

## When to Use This Skill

- When building the annual operating plan (AOP) for an ecommerce brand.
- When allocating monthly marketing budgets across performance channels (Google, Meta, TikTok, Amazon).
- When managing cash flow by timing inventory purchases based on lead times and sales velocity.
- When producing monthly variance reports (Budget vs. Actuals) to identify operational inefficiencies.
- When re-forecasting the remainder of the year after a significant peak (e.g., Q4) or a supply chain disruption.

## 1. Revenue Budgeting Methodology

The revenue budget is the primary driver for all other expense lines. A "Bottom-Up" approach using historical seasonality is the most accurate method.

### Calculating Seasonal Indices
Seasonality accounts for the natural peaks and valleys of your business (e.g., Black Friday, Summer Slowdown).
- **Formula**: `Seasonal Index = Monthly Revenue / Annual Average Monthly Revenue`
- *Example*: If average monthly revenue is $100K and December is $250K, December's seasonal index is 2.5.

### Building the Forecast
1.  **Baseline**: Pull the last 12–24 months of revenue by channel (Web, Amazon, Wholesale).
2.  **Growth Assumptions**: Apply a percentage growth target based on planned marketing investment and new product launches.
3.  **Monthly Allocation**: Multiply the total annual target by the seasonal index for each month.

## 2. Marketing Budget Framework

Marketing spend should be categorized into **Variable** (Performance) and **Fixed** (Brand/Operations).

### Performance Marketing Targets
Set these as a percentage of the attributed revenue for each channel. Industry benchmarks for healthy ecommerce operations:

| Channel | % of Revenue (Target) | Logic |
|---------|-----------------------|-------|
| **Google Search/Shopping** | 6% – 10% | High-intent capture; lower funnel. |
| **Meta (FB/IG) Ads** | 8% – 15% | Top-of-funnel discovery; includes creative testing. |
| **TikTok Ads** | 5% – 12% | Highly volatile; requires frequent creative refresh. |
| **Amazon Ads (TACOS)** | 8% – 12% | Total Ad Cost of Sale; essential for visibility. |
| **Affiliate / Influencer** | 5% – 8% | Commission-based; low risk, variable scale. |

### Fixed Marketing Costs
Include non-variable expenses like email/SMS platform subscriptions, agency retainers, and content production. These should remain stable regardless of monthly revenue fluctuations unless a major strategy shift occurs.

## 3. Inventory Open-to-Buy (OTB) Budget

OTB is the dollar amount of new inventory you are authorized to purchase in each period to meet your sales goals without overstocking.

- **Formula**: `OTB = Planned Sales (at cost) + Planned End-of-Month (EOM) Inventory - Beginning-of-Month (BOM) Inventory`

### Inventory Planning Nuance
- **Weeks of Cover**: Aim for 8–12 weeks of stock for standard items.
- **Lead Time Adjustment**: Purchases must be budgeted 1–3 months *before* the planned sales month based on supplier lead times.
- **Safety Stock**: Increase the EOM target for high-velocity SKUs or items with volatile supply chains.

## 4. Variance Analysis and Materiality

By the 3rd business day of each month, compare your actual financial results (from your accounting system) against the budget.

### Variance Structure
| Category | Budget | Actual | Variance (%) | Status |
|----------|--------|--------|--------------|--------|
| Web Revenue | $100,000 | $112,000 | +12% | Favorable |
| Meta Ad Spend | $15,000 | $18,500 | +23% | Unfavorable ⚠ |
| COGS | $40,000 | $46,000 | +15% | Watch |

### Materiality Thresholds for Action
Not every discrepancy requires a meeting. Set strict triggers for management commentary:
1.  **Absolute Threshold**: Any variance > $5,000.
2.  **Percentage Threshold**: Any variance > 10% of the line item budget.
3.  **Critical Threshold**: Any variance > 20% requires a written "Root Cause Analysis" and a remediation plan for the following month.

## 5. The Rolling Forecast Update

Each month, the "Budget" becomes the "Plan," and the "Forecast" is updated with "Actuals."

1.  **Lock the Month**: Replace the past month's budget with actual figures.
2.  **Adjust Forward**: If revenue is 15% above plan for two consecutive months, increase the variable marketing and OTB budgets for the next quarter to capitalize on the momentum.
3.  **Resource Reallocation**: If one channel (e.g., Google) is underperforming by 20% while another (e.g., TikTok) is overperforming, reallocate the "Unfavorable" variance from the weak channel to the strong one mid-period.

## Best Practices

- **Zero-Based Overhead**: Every 12 months, rebuild your software and payroll budget from zero. Identify "zombie" subscriptions that are no longer driving value.
- **Revenue Recognition**: Ensure your actuals match your accounting system's revenue recognition (accrual basis) rather than just cash-in-hand to ensure the budget correctly aligns with cost of goods sold.
- **Sensitivity Analysis**: Create "Best Case" and "Worst Case" versions of the budget. What happens to cash runway if revenue is 20% lower than the "Base Case"?
- **Weekly Pacing**: Don't wait for month-end. Track performance marketing spend weekly against the monthly cap to avoid surprise overages.
