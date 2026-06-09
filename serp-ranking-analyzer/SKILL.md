---
name: serp-ranking-analyzer
description: Conduct deep SERP analysis to identify ranking factors, intent signals, and feature opportunities for competitive search queries.
---

## When to Use
Trigger this skill when a user wants to understand why certain websites are ranking for a specific keyword and what it will take to outrank them. Use it for competitive research, content planning, and identifying SERP feature opportunities.

## Core Capabilities
- **SERP Composition Mapping**: Breaking down the page into Organic, Paid, and Feature elements.
- **Intent Signal Detection**: Identifying if the search is Informational, Transactional, Navigational, or Commercial.
- **Ranking Factor Identification**: Pinpointing the specific "weights" (Backlinks, Content Depth, Domain Authority) that Google is prioritizing for this specific query.
- **AI Overview (SGE) Analysis**: Analyzing how AI-generated summaries are impacting click-through rates and source attribution.
- **Content Format Recommendations**: Determining if the user needs a "How-to" guide, a "Listicle," a "Product Page," or a "Video."

## 8-Step Analysis Framework
1. **Understand the Query**: Identify the primary keyword and its semantic variations.
2. **Map SERP Composition**: Count the number of Ads, Featured Snippets, "People Also Ask" boxes, and Video carousels.
3. **Analyze the Top 10**: Audit the top-ranking URLs for:
    - **Content Type**: (e.g., Blog vs. Landing Page)
    - **Content Length**: Word count benchmarks.
    - **Freshness**: When was the content last updated?
4. **Identify Ranking Patterns**: Is every top result a "Big Brand" (High DA)? Is every result a "Comparison Table"?
5. **Analyze SERP Features**: Which features can be "stolen" via Schema markup (e.g., FAQ Schema for the FAQ feature)?
6. **Determine Search Intent**: If 9/10 results are e-commerce categories, do not try to rank with a 5,000-word blog post.
7. **Calculate True Difficulty**: Beyond a 0-100 score, look at the "Volatility" and "Brand Dominance."
8. **Generate Recommendations**: Create a checklist of technical and content requirements to compete.

## Key Metrics & Benchmarks
- **Domain Authority (DA/DR)**: Is there a "floor" (e.g., no site below 60 DR ranks)?
- **Backlink Profile**: Number of unique referring domains to the specific URL.
- **On-Page Optimization**: Presence of keyword in H1, URL, and Subheaders.
- **User Experience**: Mobile-friendliness, HTTPS status, and Core Web Vitals (LCP, FID, CLS).

## SERP Feature Taxonomy
Common features to monitor and optimize for:
- **Featured Snippet**: Target by answering questions directly in 40-60 words.
- **People Also Ask (PAA)**: Target by adding a dedicated FAQ section with H3 headers.
- **Local Pack**: Target via Google Business Profile optimization.
- **Knowledge Panel**: Target via entity-based Schema and Wikipedia/Wikidata presence.
- **Video Carousel**: Target by creating YouTube content with timestamped chapters.

## Validation Checkpoints
### Input Validation:
- Is the keyword specific enough? (e.g., "best running shoes" vs "running shoes")
- Is the target geography defined? (SERPs vary significantly by country).

### Output Validation:
- Does the report identify the "Content Gap" (what the top 10 are missing)?
- Does it provide a clear "Go/No-Go" recommendation based on the user's current site authority?
- Are the recommendations actionable (e.g., "Add a comparison table" vs "Make it better")?
