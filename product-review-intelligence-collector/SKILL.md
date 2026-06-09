---
name: product-review-intelligence-collector
description: "Automated product review collection and intelligence gathering from major e-commerce platforms (Amazon, TikTok, Walmart, etc.). Use this skill when the user wants to collect, analyze, and synthesize customer feedback for market research, competitor benchmarking, or identifying product improvement opportunities. It focuses on extraction strategies, data cleaning, and multi-dimensional analysis (pros/cons, scenarios, unmet needs)."
category: market-research
risk: safe
source: curated
date_added: "2026-04-08"
tags: [reviews, sentiment-analysis, competitor-analysis, market-research, customer-voice, data-extraction]
triggers: ["collect product reviews", "analyze competitor reviews", "review sentiment analysis", "customer pain points", "market research reviews", "scrape amazon reviews", "gather customer feedback", "review mining"]
---

# Product Review Intelligence Collector

## Overview

This skill transforms raw customer feedback from e-commerce platforms into actionable market intelligence. Instead of just "listing" reviews, it focuses on **automated collection** and **strategic synthesis** to help product managers and researchers identify market gaps, competitive advantages, and customer pain points.

## Core Workflow

### Step 1: Target Identification & Scoping
1.  **Identify Platforms**: Determine where the target audience leaves the most honest feedback (e.g., Amazon for utility, TikTok for trends, Specialized forums for enthusiasts).
2.  **Define Scope**: 
    *   **Direct Competitors**: Top-selling ASINs or URLs.
    *   **Quantity**: Determine the sample size (e.g., "latest 50 reviews" or "all 1-3 star reviews from the last 6 months").
    *   **Segments**: Focus on specific variations (colors, sizes) if relevant.

### Step 2: Collection Strategy
Use the most efficient tool based on the platform:
- **Amazon**: Prefer `apify` actors (like `junglee/amazon-reviews-scraper`) or `browser` sessions for authenticated/localized results.
- **Social Media (TikTok/Instagram)**: Use `browser` to scroll comments or `apify` social media scrapers.
- **Generic Sites**: Use `web_fetch` for static pages or `browser` for JS-heavy review widgets.

### Step 3: Data Extraction & Cleaning
For each review, extract:
- **Metadata**: Star rating, Date, Verified Purchase status, Helpful votes.
- **Content**: Review title and body text.
- **Rich Media**: Note if photos or videos are attached (indicates high engagement).
- **Cleaning**: Filter out "vine customer reviews" (incentivized) or one-word reviews (e.g., "Good") to focus on high-signal content.

### Step 4: Multi-Dimensional Analysis
Analyze the collected data across these 4 dimensions:
1.  **Pros (High-Value Hooks)**: What do users love? (e.g., "The handle stays cool in the microwave").
2.  **Cons (Critical Flaws)**: What are the recurring complaints? (e.g., "The bottom is not flat, it wobbles").
3.  **Scenario Mapping**: Where and how are they using it? (e.g., "Used in a camper van," "Office desk companion").
4.  **Unmet Needs**: What do users wish the product had? (e.g., "Wish it came with a lid").

## Deliverable Formats

### 1. Raw Data (`reviews_ASIN.json`)
Store structured data for further processing:
```json
[
  {
    "rating": 5,
    "title": "Best mug ever",
    "text": "...",
    "is_verified": true,
    "has_images": true,
    "date": "2024-03-15"
  }
]
```

### 2. Intelligence Report (`review_analysis_report.md`)
ALWAYS include a summary table and a "Product Opportunity" section:
# [Product Name] Review Analysis
## Executive Summary
- **Overall Sentiment**: Positive/Mixed/Negative
- **Key Pivot Point**: The one thing that defines this product's success or failure.

## Deep Dive Analysis
- **Top 3 Pros**: ...
- **Top 3 Cons**: ...
- **Common Use Scenarios**: ...

## Market Gaps & Opportunities
- [Insight 1]: "Users complain about X; a version with Y would dominate."
- [Insight 2]: "Scenario Z is underserved by current designs."

## Best Practices
- **Focus on the "Middle"**: 3-star reviews often contain the most balanced and detailed technical feedback.
- **Watch the Velocity**: A sudden spike in negative reviews often points to a recent manufacturing/QC issue.
- **Analyze Images**: Users often post photos of broken parts; these are "smoking guns" for product improvement.
