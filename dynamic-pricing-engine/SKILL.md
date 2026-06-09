---
name: dynamic-pricing-engine
description: "Trigger: Automatically adjust prices based on demand signals, competitor prices, and inventory levels to maximize revenue."
category: pricing-promotions
risk: critical
source: curated
date_added: "2026-03-12"
tags: [dynamic-pricing, demand-pricing, price-optimization, competitor-monitoring, repricing, algorithmic-pricing]
platforms: [shopify, woocommerce, bigcommerce, custom]
difficulty: advanced
---

# Implement Dynamic Pricing Engine

## Overview

Dynamic pricing automatically adjusts product prices based on real-time data: demand signals, inventory levels, competitor pricing, and business rules. The objective is to maximize revenue per unit sold by raising prices when demand is strong or supply is limited, and lowering them to clear slow-moving inventory.

## When to Use This Skill

- When high-velocity SKUs lose revenue because fixed prices don't respond to market shifts.
- When liquidating slow-moving inventory through automated markdown schedules.
- When managing a marketplace where seller prices must respond to competitive pressure.
- When building a revenue management system for perishable or time-sensitive stock.
- When A/B testing price elasticity at scale to find optimal price points.

## Core Instructions

### Step 1: Define Pricing Rules and Guardrails

Before implementing any automated pricing, establish hard guardrails to protect margins and customer trust:

| Rule | Example |
|------|---------|
| **Floor price** | Never go below cost × 1.15 (15% gross margin minimum). |
| **Ceiling price** | Never exceed MSRP or a defined maximum cap. |
| **Max change per cycle** | Limit price movement to ±20% in a single repricing run. |
| **Change threshold** | Only update if the new price differs by >2% to avoid micro-oscillations. |
| **Lock-out periods** | Suspend dynamic pricing during flash sales or active promotions. |
| **Human review trigger** | Queue any change >10% for manual approval before applying. |

### Step 2: Demand Signal Identification

Incorporate multiple data points to drive price adjustments:
*   **Sales Velocity:** Units sold per hour/day relative to historical averages.
*   **Page Views:** High traffic with low conversion may indicate a price that is too high.
*   **Add-to-Cart (ATC) Rate:** A drop in ATC rate following a price increase indicates reaching the ceiling of price elasticity.
*   **Inventory Level:** "Inventory-aware" pricing raises prices as stock nears zero to slow demand and avoid stockouts.

### Step 3: Platform-Native Implementation

#### Shopify (Shopify Plus)
Use **Shopify Flow** for inventory or demand-based pricing adjustments:
1.  **Trigger:** Create a new workflow triggered by **Inventory level changed** or a custom webhook (e.g., from an analytics tool).
2.  **Condition:** Example: "Inventory quantity is less than 10".
3.  **Action:** **Update product variant** and set the price to a higher value.
4.  **Restore:** Add a separate workflow for when inventory recovers to restore the original price.
5.  **Best Practice:** Store original prices in a product metafield (`product.metafields.pricing.original_price`) for reliable rollbacks.

#### WooCommerce (REST API)
Use the WooCommerce REST API for automated updates from an external pricing engine:
*   **Endpoint:** `PUT /wp-json/wc/v3/products/{id}/variations/{id}`
*   **Payload Example:**
    ```json
    {
      "regular_price": "29.99",
      "sale_price": "24.99"
    }
    ```
*   **Scheduling:** Use server-side cron jobs to trigger the pricing logic every 1-4 hours.

#### Amazon Repricing
For marketplace sellers, automated repricing is standard. Mentioning Amazon repricing context is critical as the Buy Box algorithm reacts to price changes in real-time.

### Step 4: Competitor Price Monitoring Methodology

Monitor competitor pricing without naming specific tools using these steps:
1.  **URL Mapping:** Map your product SKUs to specific competitor product URLs.
2.  **Scraping/API Polling:** Regularly poll competitor pages (on a 4-24 hour cycle) for current price and availability.
3.  **Hysteresis Band:** Do not match a competitor if they are only $0.01 lower; use a 1-2% buffer to prevent "race to the bottom" scenarios.
4.  **Data Freshness:** Skip repricing if the competitor data is older than 4-6 hours to avoid reacting to stale promotions.

### Step 5: Price Elasticity Testing Framework

Test the impact of price changes using this structured approach:
1.  **Selection:** Choose 5-10 high-volume SKUs.
2.  **Control/Test groups:** If the platform allows, split traffic (50/50). If not, use temporal testing (7 days at Price A, 7 days at Price B).
3.  **Metric:** Measure **Gross Profit per Session** rather than just conversion rate.
4.  **Iteration:** Gradually increase/decrease prices by 5% increments until Gross Profit per Session peaks.

## Best Practices

- **Enforce Absolute Floors:** The margin-based floor must be hard-coded into the algorithm, overriding all other logic.
- **Store Full History:** Log every change with: `timestamp`, `old_price`, `new_price`, and `reason_code` (e.g., `low_inventory`, `competitor_undercut`).
- **Dry-Run Mode:** Run the pricing engine in "recommendation-only" mode for 7 days before allowing it to update live site prices.
- **Cache Management:** Purge product page caches and update search indexes immediately after a price change to prevent price discrepancies.

## Common Pitfalls

| Problem | Solution |
|---------|----------|
| Price oscillation | Add a minimum 2-hour "cooldown" period between changes for any single SKU. |
| Price drops during competitor war | Implement a `Stop-Loss` rule that freezes price updates if a competitor drops >30% below MSRP. |
| Discrepancy between feed and site | Ensure your Google Shopping feed or Meta catalog is updated within 1 hour of any price change. |
