---
name: shopify-ads-roas-optimizer
description: "Audit and optimize Shopify ad performance across Meta, Google, and TikTok by diagnosing tracking health, ROAS volatility, and funnel leaks."
---

# Shopify Ads & ROAS Optimizer

## Overview
Maximizing ROAS (Return on Ad Spend) on Shopify requires perfect alignment between store events, ad platform algorithms, and the checkout funnel. This framework provides a professional diagnostic path to identify whether performance issues stem from tracking gaps, creative fatigue, poor site conversion, or attribution lag.

---

## 1. Data Input Contract
To perform an accurate audit, the following data points are required:
- **Shopify Store Context:** URL, primary niche, and average order value (AOV).
- **Tracking Stack:** Status of Meta Pixel/CAPI, Google Tag Manager, and TikTok Events API.
- **Performance Snapshot:** Spend, Impressions, CTR, CPC, and Platform-reported ROAS.
- **Backend Metrics:** Blended ROAS (MER), Checkout Initiation Rate, and Purchase Conversion Rate.
- **Contextual Changes:** Recent theme updates, shipping policy shifts, or discount launches.

---

## 2. Core Diagnostic Framework

### Pillar 1: Tracking & Event Integrity
- **Event Mapping:** Verify that `ViewContent`, `AddToCart`, `InitiateCheckout`, and `Purchase` events are firing with correct currency and value parameters.
- **CAPI Match Quality:** Ensure server-side events (Meta Conversions API) have high match scores to mitigate iOS 14+ tracking loss.
- **Deduplication:** Check for double-counting of purchases caused by multiple pixels or app conflicts.

### Pillar 2: Channel & Account Structure
- **Account Hierarchy:** Audit for over-segmentation. Are there too many small ad sets competing for the same audience?
- **Advantage+ & PMax:** Evaluate the use of automated campaign types (Meta Advantage+ / Google PMax) vs. manual controls.
- **Creative Refresh Cycle:** Identify high-spend assets with declining CTR—a primary signal for creative fatigue.

### Pillar 3: ROAS & Margin Analysis
- **Blended ROAS (MER):** Calculate total revenue / total ad spend to account for attribution "dark matter."
- **Margin-Based Bidding:** Do not optimize for ROAS alone. A 2.0 ROAS on a 70% margin product is healthier than a 4.0 ROAS on a 15% margin product.
- **Attribution Windows:** Compare 1-day vs. 7-day click data to understand the customer consideration cycle.

### Pillar 4: The Checkout Funnel Leak Detection
- **Micro-Conversion Rates:**
    - *Add-to-Cart (ATC) Rate:* Target > 5%
    - *Initiate Checkout (IC) Rate:* Target > 40% of ATCs
    - *Purchase Rate:* Target > 50% of ICs
- **Friction Points:** If IC-to-Purchase is low, audit shipping costs, payment gateways, and guest checkout options.

---

## 3. Strategic Decision Rules

| Scenario | Primary Action | Secondary Action |
| :--- | :--- | :--- |
| **High ATC, Low Purchase** | Audit shipping/taxes in checkout. | Implement "Abandoned Cart" SMS/Email. |
| **High Spend, Low CTR** | Immediate Creative Refresh. | Test new "Hook" variations. |
| **Stable ROAS, High Margin** | Scale budget by 15-20% daily. | Expand to Lookalike audiences. |
| **Volatile ROAS (Post-Update)** | Isolate pre/post change data. | Verify tracking pixel status. |

---

## 4. Scaling Thresholds (Logic Example)
A campaign is "Scale-Ready" only if it clears these three hurdles:
1. **Efficiency:** Blended ROAS > Break-even ROAS + 1.0.
2. **Stability:** Performance has been consistent for 7 consecutive days.
3. **Infrastructure:** Checkout Conversion Rate (CVR) > 2.2% (to ensure the traffic isn't being wasted).

**Action:** Increase daily budget by 15% every 48 hours until the ROAS drops to the target floor.

---

## 5. Deliverables & Output Contract
The optimizer will generate a report containing:
1. **Health Score:** A summary of tracking and attribution reliability.
2. **Channel Diagnosis:** Specific critiques of Meta, Google, and TikTok account structures.
3. **The "Scale vs. Fix" Verdict:** A clear decision on whether to increase spend or pause and fix the site.
4. **Prioritized Action Plan:** 3-5 high-impact tasks (e.g., "Fix CAPI deduplication," "Launch 3 new video hooks").
5. **Funnel Benchmarking:** Comparison of your store's funnel metrics against industry standards.

---

## 6. Constraints & Safety
- **Never Scale on "Empty" ROAS:** If platform ROAS is high but bank account revenue isn't moving, do not increase budget.
- **Gradual Changes:** Avoid budget jumps larger than 30% to prevent the ad platforms from re-entering the "Learning Phase."
- **SKU Isolation:** Always separate high-performance "Hero" products from testing/new arrivals.
