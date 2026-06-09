---
name: product-launch-planner
description: "Orchestrate multi-phase product launches using pre-launch waitlists, tiered early access, and coordinated multi-channel marketing to maximize day-one velocity and long-term momentum."
category: marketing-growth
risk: safe
source: curated
date_added: "2026-03-12"
tags: [product-launch, go-to-market, campaign-planning]
triggers: ["launch new product", "product launch campaign", "new collection release"]
platforms: [shopify, woocommerce, amazon, bigcommerce]
difficulty: intermediate
---

# Product Launch Planner

## Overview

A successful product launch is a high-velocity event that transforms months of development into concentrated market demand. The objective is to coordinate email, SMS, paid social, and organic content into a synchronized sequence that builds anticipation, captures high-intent leads via waitlists, and converts them through tiered access. 

This skill provides a framework for planning the T-21 (Pre-launch) to T+30 (Post-launch) phases, focusing on native platform configurations and cross-channel orchestration.

## When to Use This Skill

- **New Category Entry:** When launching a product in a category where you have no existing customers.
- **Line Extension:** When adding a new variant or model to a successful existing line.
- **Limited Drops:** When inventory is constrained and you need to prioritize high-value customers.
- **Re-branding/Re-launch:** When significant updates require a "fresh start" in the market.

## Strategic Framework: The 3-Phase Launch

| Phase | Timing | Objective | Key Metrics |
|-------|--------|-----------|-------------|
| **Pre-launch** | T-21 to T-1 | Demand Signaling & List Building | Waitlist Size, Opt-in Rate, CPA per Lead |
| **Launch Day** | T-0 | Conversion Velocity | Sell-through Rate, Hourly Revenue, CAC |
| **Post-launch** | T+1 to T+30 | Momentum & Social Proof | Review Velocity, Repeat Purchase Rate |

### Decision Criteria: Hard Launch vs. Soft Launch

- **Hard Launch:** Use when you have significant inventory and a high marketing budget. Focus on mass awareness and simultaneous channel activation.
- **Soft Launch (Early Access):** Use for high-ticket items or when testing market fit. Focus on "VIP-only" periods to gather early feedback and create exclusivity.

---

## Execution Steps

### Step 1: Establish the Demand Capture Mechanic

Before any promotion begins, you must have a way to capture interest.

#### Shopify Admin
1. **Create a Landing Page:** Navigate to **Online Store > Pages**. Build a "Coming Soon" page.
2. **Password Protection:** For high-hype launches, use **Online Store > Preferences > Password protection**. Enable the password page and customize the message to include a signup form.
3. **Draft Products:** Create the product in **Products**, but keep it as **Draft** or set the **Published on** date to the launch time. This allows you to generate URLs for marketing without allowing premature checkout.

#### WooCommerce Admin
1. **Product Visibility:** Set the product status to "Hidden" or "Private" during the pre-launch phase.
2. **Catalog Visibility:** Set to "Hidden" so it doesn't appear in shop searches but remains accessible via a direct link for influencers or VIPs.

### Step 2: Tiered Access Orchestration

Maximize "Fear Of Missing Out" (FOMO) by rewarding your most loyal customers.

1. **VIP Tier (T-24h):** Grant access to the top 5-10% of customers (by Lifetime Value) 24 hours before the public.
2. **Waitlist Tier (T-2h):** Grant access to those who signed up for the "Notify Me" list 2 hours before the public.
3. **Public Launch (T-0):** Open the store to all traffic.

**Edge Case: High Traffic Spikes**
If you expect 10x your normal traffic, ensure your platform's checkout is ready. On Shopify, use the "Launchpad" app (if on Plus) to automate theme changes and inventory releases. On WooCommerce, ensure object caching (Redis/Memcached) is active to prevent database lockups during concurrent checkouts.

### Step 3: Multi-Channel Campaign Setup

#### Meta & TikTok Ads Manager
Build three distinct campaign sets:
- **Teaser (T-14 to T-1):** Objective: Lead Generation. Target: Lookalikes of existing buyers. Creative: "Coming Soon" video.
- **Launch (T-0 to T+3):** Objective: Conversions. Target: Waitlist (Custom Audience) + Site Visitors (Last 30 days). Creative: "Now Available" + Hero shots.
- **Momentum (T+4 to T+14):** Objective: Conversions/Retargeting. Creative: User Generated Content (UGC) + "Selling Fast" messaging.

#### Email/SMS Sequence Logic
- **T-14:** Reveal email to full list.
- **T-7:** Deep dive into features/benefits.
- **T-1:** "The countdown is on" reminder.
- **T-0 (8 AM):** VIP Early Access link.
- **T-0 (10 AM):** Waitlist Early Access link.
- **T-0 (12 PM):** Public Launch announcement.

### Step 4: Post-Launch Social Proof Loop

1. **Review Requests:** Automate a request 7–10 days after the estimated delivery date. 
2. **UGC Curation:** Monitor social tags. Re-post customer "unboxing" videos to your main feed during the first week to validate the purchase for "on-the-fence" buyers.

---

## Benchmarks & Performance Targets

| Metric | Benchmark (Good) | Benchmark (Great) |
|--------|------------------|-------------------|
| **Waitlist Conversion** | 10% - 15% | > 25% |
| **Launch Day Revenue** | 3x Avg. Daily Rev | > 10x Avg. Daily Rev |
| **Day 1 Sell-through** | 20% | > 50% |
| **Review Rate** | 2% - 5% | > 8% |

---

## Troubleshooting & Edge Cases

| Issue | Detection | Mitigation |
|-------|-----------|------------|
| **Inventory Oversell** | Negative inventory levels in Admin | Set "Track Quantity" and ensure "Continue selling when out of stock" is **Disabled**. |
| **Low Waitlist Growth** | < 1% click-through on teaser ads | Change creative to focus on a "Waitlist-only discount" or "Exclusive gift" for first 100 buyers. |
| **Checkout Crashes** | High bounce rate at /checkout | Disable non-essential scripts (tracking pixels, chat bots) during the first 2 hours of launch to reduce server load. |
| **Viral Outliers** | Traffic 100x higher than forecast | Implement a queueing system or a "Waitlist for Restock" button immediately once inventory hits 0. |
