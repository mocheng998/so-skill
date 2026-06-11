---
name: ecommerce-sales-dashboard
description: "Design and implement comprehensive sales dashboards to track revenue, AOV, conversion rates, and channel performance. Establish a single source of truth for daily, weekly, and monthly executive reporting."
category: data-analytics
risk: safe
source: curated
date_added: "2026-03-12"
tags: [analytics, reporting, sales-performance, kpi, dashboard-design]
triggers: ["build sales dashboard", "revenue reporting setup", "ecommerce kpi tracking", "conversion rate analysis"]
platforms: [shopify, woocommerce, bigcommerce, amazon-seller-central]
difficulty: intermediate
---

# Ecommerce Sales Dashboard

## Overview

A high-performance sales dashboard transforms raw transactional data into actionable business intelligence. It serves as the "cockpit" for ecommerce operators, providing real-time visibility into revenue velocity, customer behavior, and channel efficiency. This skill focuses on building these dashboards using native platform analytics and standard BI frameworks (like Looker Studio or GA4), emphasizing data accuracy and period-over-period (PoP) context.

## The Core KPI Framework

Every executive dashboard must answer three fundamental questions:
1.  **Velocity:** How much are we selling right now vs. yesterday/last week?
2.  **Efficiency:** How much does it cost to acquire these sales (Conversion Rate & AOV)?
3.  **Retention:** Are these new or returning customers?

### Essential Metrics & Formulas

| Metric | Formula | Benchmark (DTC) |
|--------|---------|-----------------|
| **Gross Merchandise Value (GMV)** | Sum of All Order Totals (incl. Tax/Shipping) | N/A |
| **Net Sales** | GMV - Discounts - Refunds | > 85% of GMV |
| **Conversion Rate (CR)** | (Total Conversions / Total Sessions) × 100 | 2.5% - 4.0% |
| **Average Order Value (AOV)** | Net Sales / Total Orders | Industry Dependent |
| **Returning Customer Rate** | (Returning Customers / Total Customers) × 100 | 20% - 30% |

---

## Execution Steps

### Step 1: Establish the Single Source of Truth

Discrepancies between platforms (e.g., Shopify vs. GA4 vs. Stripe) are common due to attribution windows, timezones, and tax inclusion. 

- **Primary Source (Financial):** Use your Ecommerce Admin (Shopify/WooCommerce/Amazon) for revenue and order counts.
- **Secondary Source (Behavioral):** Use GA4 for conversion funnels, session-based metrics, and traffic attribution.

### Step 2: Native Platform Configuration

#### Shopify Admin
1.  Navigate to **Analytics > Dashboards**.
2.  **Customization:** Click "Manage" to add/remove tiles. Ensure "Total Sales," "Online Store Conversion Rate," and "Average Order Value" are prominent.
3.  **Comparisons:** Always enable the "Compare to" toggle in the date picker. Use "Prior Period" for daily checks and "Prior Year" for seasonal planning.

#### WooCommerce Admin
1.  Go to **Analytics > Overview**. 
2.  **Report Customization:** Use the "Revenue" and "Orders" sections to filter by order status. Always exclude "Cancelled" or "Failed" orders to avoid inflating revenue.

#### Amazon Seller Central
1.  Go to **Reports > Business Reports**.
2.  Focus on **Sales and Traffic by Date** to track "Ordered Product Sales" and "Unit Session Percentage" (Conversion Rate).

### Step 3: Advanced Visualization (Looker Studio)

For a unified view, connect your platform data to Google Looker Studio.

1.  **Data Source:** Connect Google Analytics 4 (Native) or export Shopify/WooCommerce data via Google Sheets.
2.  **SQL Reference (BigQuery/Generic SQL):** Use this logic for custom AOV calculation:
    ```sql
    SELECT 
      DATE(order_created_at) AS date,
      SUM(total_price) / COUNT(DISTINCT order_id) AS aov,
      SUM(total_price) AS total_revenue
    FROM `your_project.ecommerce_data.orders`
    WHERE status NOT IN ('cancelled', 'refunded')
    GROUP BY 1
    ORDER BY 1 DESC;
    ```
3.  **Visuals:** Use Scorecards for current KPIs and Time-Series charts for PoP trends.

### Step 4: Multi-Currency & Timezone Alignment

- **Multi-Currency:** If selling globally, convert all revenue to your base currency using the *exchange rate at the time of transaction*. Avoid using current "live" rates for historical data.
- **Timezones:** Set all reporting to the store's "Legal Entity" timezone. Ensure GA4 and Shopify timezones match exactly.

---

## Decision Criteria: Signal vs. Noise

- **The 20% Rule:** Don't panic over daily fluctuations within +/- 20% of the 30-day average. This is usually "noise."
- **The Conversion Drop:** A >30% drop in conversion rate over a 24-hour period (without a traffic spike) is a **signal** of a technical issue (e.g., checkout bug, broken discount code).
- **AOV Spikes:** A sudden 50% increase in AOV often indicates a "Wholesale" or "Fraudulent" order. Audit any order >10x your average.

---

## Benchmarks & Performance Targets

| Metric | Danger Zone | Healthy | Elite |
|-----------|-------------|---------|-------|
| **Conversion Rate** | < 1.0% | 2.5% | > 5.0% |
| **Refund Rate** | > 15% | 3% - 8% | < 2% |
| **New vs. Returning** | < 10% Returning | 25% Returning | > 40% Returning |
| **AOV Growth** | Declining YoY | Flat/Stable | +10% YoY |

---

## Troubleshooting & Common Pitfalls

- **Bot Traffic:** High session counts with 0% conversion rate can skew CR. Filter out non-residential IP ranges in GA4.
- **Refund Lag:** Refunds often happen 7-14 days after a sale. Your "Real-time" revenue will always look higher than your "Settled" revenue at the end of the month.
- **Inconsistent Definitions:** Ensure everyone agrees on whether "Revenue" includes shipping and tax. Standardize on **Net Sales** (Revenue minus discounts/refunds, excluding tax/shipping) for operational decisions.
