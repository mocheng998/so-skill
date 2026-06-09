---
name: marketing-roas-analyzer
description: "Track and analyze marketing spend across all channels with ROAS calculation, incrementality testing, and budget reallocation based on true profitability."
category: data-analytics
risk: safe
source: curated
date_added: "2026-03-12"
tags: [marketing-spend, roas, budget-optimization, analytics, attribution]
triggers: ["analyze marketing spend", "ROAS analysis", "marketing budget allocation", "channel efficiency", "diminishing returns", "ad spend optimization", "blended ROAS"]
tools: [claude-code, cursor, gemini-cli, copilot, codex-cli]
platforms: [shopify, woocommerce, bigcommerce, meta-ads, google-ads, tiktok-ads, google-analytics]
difficulty: intermediate
---

# Analyze Marketing Spend and Channel ROAS

## Overview

Marketing spend is typically the largest variable cost in a DTC ecommerce business—often 15–40% of revenue. Unlike most costs, marketing spend is directly controllable in near-real-time. The core goal is to maximize total contribution profit from your marketing investment, not just top-line revenue. This requires moving beyond platform-reported metrics to a unified view of efficiency and incrementality.

## When to Use This Skill

- When managing marketing budgets across multiple platforms (Meta, Google, TikTok, Amazon Ads).
- When wanting to identify which channels generate the most profitable customers.
- When platform-reported ROAS seems inflated compared to actual bank deposits.
- When hitting diminishing returns on a key channel and deciding where to reallocate the next $1,000.
- When comparing "Blended" efficiency (MER) against individual channel performance.

## Core Metric Definitions

| Metric | Calculation | Why It Matters |
|--------|-------------|---------------|
| **Platform ROAS** | `Platform Revenue / Platform Spend` | What the ad platform claims (typically inflated by view-throughs). |
| **1P (First-Party) ROAS** | `Attributed Revenue (GA4) / Platform Spend` | De-duplicated revenue based on your own tracking logic. |
| **Blended MER** | `Total Revenue / Total Marketing Spend` | The "North Star" for overall marketing health; harder to game. |
| **True ROAS** | `(Revenue * Gross Margin %) / Spend` | Accounts for COGS; shows if you are actually making profit. |
| **CAC (New Customer)** | `Prospecting Spend / New Customers Acquired` | Measures the efficiency of growing the customer base. |
| **Break-even ROAS** | `1 / (1 - COGS% - Variable Cost%)` | The minimum ROAS needed to result in $0 profit (net of ads). |

## Core Instructions

### Step 1: Calculate Your ROAS Break-Even

Before deciding if a channel is "good," you must know the point at which it becomes "profitable."

**Break-even ROAS formula:**
```text
Break-even ROAS = 1 / (1 - COGS rate - Variable cost rate)

Example:
  COGS rate: 45% (Product cost is 45% of price)
  Variable costs: 12% (Shipping + Payment fees + Packaging)
  
  Calculation: 1 / (1 - 0.45 - 0.12) = 1 / 0.43 = 2.33x
```
*Any channel with a 1P ROAS below 2.33x in this example is losing money on every sale.*

### Step 2: Set Target ROAS by Channel Type

Not all ROAS is created equal. A 5x on Retargeting might be less valuable than a 2x on Prospecting.

| Channel Type | Target ROAS Multiplier | Rationale |
|-------------|-------------------------|-----------|
| **Prospecting (Cold)** | 1.2x - 1.5x Break-even | Acquires new LTV; higher risk but high long-term value. |
| **Retargeting (Warm)** | 2x - 3x Break-even | Lower cost, but lower incrementality (they might buy anyway). |
| **Branded Search** | 5x+ | High ROAS but very low incrementality; defensive spend. |
| **Generic Search** | 1.5x - 2x Break-even | High intent; excellent for new customer acquisition. |
| **Email / SMS** | 10x+ | Retention tool; very low direct cost. |

### Step 3: Build a Weekly Channel Performance Scorecard

Use a unified reporting tool like **Google Looker Studio** or a structured spreadsheet to pull data from **Google Analytics 4**, **Meta Ads Manager**, and **Google Ads**.

```text
WEEKLY PERFORMANCE SCORECARD (Mon-Sun)
─────────────────────────────────────────────────────────────
Channel    | Spend  | 1P Revenue | 1P ROAS | Status | Action
Meta Ads   | $5,000 | $16,500    | 3.3x    | GOOD   | Scale +10%
Google Ads | $3,000 | $10,200    | 3.4x    | GOOD   | Maintain
TikTok Ads | $1,500 | $2,100     | 1.4x    | POOR   | Audit Creative
Email/SMS  | $200   | $12,000    | 60.0x   | GREAT  | Increase Freq
─────────────────────────────────────────────────────────────
TOTAL      | $9,700 | $40,800    | MER: 4.2x | BE ROAS: 2.33x
```

### Step 4: Budget Pacing Calculation

Avoid mid-month budget depletion or end-of-month "spend-ups" that waste margin.

**Daily Pacing Formula:**
`Target Daily Spend = (Monthly Budget - Spend to Date) / Days Remaining`

**Pacing Percentage:**
`Pacing % = (Actual Spend to Date / (Monthly Budget * (% of month passed)))`
- **> 110%:** Overspending. Immediate budget cap required.
- **< 90%:** Underspending. Check for rejected ads or high CPMs.

### Step 5: Decision Framework for Budget Reallocation

- **Scale Up (+20% budget):** If 1P ROAS is > 20% above target for 7 consecutive days AND creative is fresh.
- **Scale Down (-20% budget):** If 1P ROAS is < Break-even for 3 days.
- **Pause:** If 1P ROAS is < 50% of Break-even OR if the associated landing page has a conversion rate drop of > 50%.

## Deepening: Advanced Spend Analysis

### Incrementality Testing Guidance (Holdout Tests)
To find the "True" value of a channel, run a holdout test:
1.  **Define a "Geo-Holdout":** Select 2-3 similar regions (e.g., similar population/income).
2.  **Turn off ads in "Test" region:** Keep them on in the "Control" region.
3.  **Measure Lift:** `Lift % = (Sales in Control - Sales in Test) / Sales in Control`.
4.  **Calculate iROAS (Incremental ROAS):** `iROAS = (Incremental Sales) / Spend`. 
    *If iROAS is significantly lower than Platform ROAS, your ads are "claiming credit" for sales that would have happened anyway.*

### Cross-Channel Attribution Conflict Resolution
When Meta and Google both claim the same order:
- **Last-Click (GA4 Standard):** Simple but ignores the "Top of Funnel" (Meta).
- **Data-Driven (GA4 Recommended):** Uses machine learning to distribute credit.
- **Rule of Thumb:** If 1P ROAS (Last-Click) is > 1.0x on a prospecting channel, and the Blended MER is healthy, the channel is likely contributing effectively even if it doesn't hit its "Target" on a last-click basis.

## Best Practices

- **Connect Inventory to Ads:** Never run ads for out-of-stock products. Use "Pause" rules in Meta/Google when stock levels hit zero.
- **De-duplicate Manually:** If you don't use an attribution tool, assume a 20-30% overlap between platforms and adjust your targets upward to compensate.
- **Monitor CPM Spikes:** A sudden ROAS drop is often a CPM spike (competition) rather than a creative failure. Check the "Frequency" metric; if it's > 2.0 in a 7-day window, you are over-saturating your audience.

## Common Pitfalls

| Problem | Solution |
|---------|----------|
| **Trusting Platform ROAS** | Always verify against 1P data (GA4) and Blended MER. |
| **Ignoring Branded Search** | Separate Branded from Generic Google Ads to see true acquisition costs. |
| **Over-scaling too fast** | Never increase budget by more than 20% every 48-72 hours to avoid resetting the "Learning Phase." |
| **Creative Fatigue** | If ROAS drops but CPM/CPC is stable, your creative is likely stale. Refresh assets before cutting budget. |
| **Attribution Lag** | Don't judge yesterday's Meta performance today. Allow 24-48 hours for data to "settle" due to API delays. |
