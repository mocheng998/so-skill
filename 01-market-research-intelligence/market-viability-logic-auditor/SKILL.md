---
name: market-viability-logic-auditor
description: |
  Evaluates cross-platform product/market feasibility using a risk-first framework — screens for exclusion filters, validates market thresholds, and audits profitability. Use when making go/no-go decisions on product ideas, assessing product viability, risk, and market entry feasibility across e-commerce channels (Amazon, Shopify, Etsy, TikTok Shop, independent DTC, etc.).
workflow: |
  Complete this in five steps:
    0. Query Triage (if query is vague, recommend 3 niche categories)
    1. Risk Screening (exclusion filters for high-risk categories)
    2. Market Threshold Validation (pricing, competition, demand)
    3. Profitability Audit (cost structure, margin calculation)
    4. Verdict (Go / Further Research / Reject)
enabled: true
---

# Market Viability Logic Auditor

Evaluate the market viability of $ARGUMENTS using a systematic, data-driven approach: screen for deal-breaker risks first, then validate market data and profitability before rendering a verdict.

> **Scope:** For Etsy/POD product discovery, use `scenario-driven-product-scout`. For trend timing analysis, use `trend-stage-timing-analyzer`. For Amazon listing optimization, use `amazon-listing-expert`.

**Template Compliance:** Before generating the product research report, read the template at `${CLAUDE_SKILL_DIR}/templates/product_research_template.md` using `read_file` and follow its structure exactly. Include every section, fill all placeholders with actual data, and do not skip, reorder, or add sections.

---

## Step 0 — Query Triage (Vague-Query Handler)

Before starting research, assess whether the user's query is specific enough to proceed.

**Trigger condition:** The user provides no specific product/category, or uses overly broad terms like "help me find a product", "what should I sell", "recommend something profitable", or a single generic word (e.g., "electronics", "home").

**When triggered, do the following instead of proceeding to Step 1:**

1. Acknowledge the broad scope and explain why narrowing down is necessary.
2. Based on current market signals (trending searches, seasonal timing, emerging niches), recommend **exactly 3 niche sub-categories** using this format:

| # | Niche Sub-Category | Why Now | Estimated Demand | Entry Difficulty |
|---|-------------------|---------|-----------------|-----------------|
| 1 | [specific niche] | [market signal / trend rationale] | [High / Medium / Low] | [Low / Medium / High] |
| 2 | [specific niche] | [market signal / trend rationale] | [High / Medium / Low] | [Low / Medium / High] |
| 3 | [specific niche] | [market signal / trend rationale] | [High / Medium / Low] | [Low / Medium / High] |

3. Ask the user to pick one (or refine further), then proceed to the full research workflow.

**Selection criteria for the 3 recommendations:**
- Favor niches with medium demand + low entry difficulty for beginners
- Diversify across different parent categories (e.g., don't suggest 3 kitchen niches)
- Prefer niches with evidence of rising search interest or underserved gaps
- Consider the current season/timing when suggesting

---

## Core Methodology

### 1. Product Discovery

Identify potential product opportunities using multiple discovery methods.

**Marketplace Trending Method:**
Browse trending/deal pages on target platforms (e.g., Amazon Today's Deals, Etsy Trending, TikTok Shop trending products) to identify products with current market traction. Products appearing in curated deal sections often indicate strong demand and can serve as starting points for niche exploration.

**Store Scanning Method:**
Analyze successful seller stores on the target platform to discover their product portfolio. Identify stores with multiple successful products and examine their entire catalog for patterns and opportunities.

**Keyword Extension Method:**
Start with a known product or keyword and use tools to discover related products and adjacent niches. This method helps uncover less obvious opportunities in related categories.

### 2. Market Data Analysis

For each potential product, gather and analyze comprehensive market data across relevant sales channels.

**Data source:** All figures (search volume, sales estimates, pricing, competition metrics) must come from verifiable tools or platform data — e.g. Helium 10 / Jungle Scout for Amazon, eRank / Etsy search for Etsy, Google Trends for broader demand — or from explicit user-provided data. Do not invent or assume numbers; when a value is unavailable, state "N/A" or "not available" and note the source used. **If key data (e.g. search volume or sales data) is N/A, do not write a full "data analysis" or viability conclusion as if it were data-backed** — instead state clearly that analysis is limited or cannot be completed without data, and recommend the user supply data or run the relevant tools first.

**Output requirement:** In every report, the section "Market Data Analysis" **must** begin with an explicit **Data source** statement (1–2 sentences), e.g. *"Data in this section from: [tool name, e.g. Helium 10 / eRank], [platform searched, e.g. Amazon US], [date or period if relevant]."* or *"Data from user-provided [description]."* Do not present analysis tables or metrics without this statement first.

**Search Volume Analysis:**
Use platform-specific tools (e.g., Helium 10 for Amazon, eRank for Etsy, Google Trends for DTC) to determine monthly search volume for main keywords. Target products with 5,000+ monthly searches for the primary keyword, indicating sufficient demand without oversaturation.

**Sales Performance Analysis:**
Analyze sales data for top 10 sellers in the niche on the target platform. Calculate average monthly sales for sellers ranked 5-10 to understand realistic performance expectations. Ideal range for beginners: 100-300 units per month per seller.

**Pricing Analysis:**
Review pricing across top sellers to identify the market price range. Target products with average prices above $20 to ensure adequate profit margins after platform fees and fulfillment costs.

**Competition Assessment:**
Evaluate competition level by examining number of sellers, review counts, and presence of major brands. Look for markets where top sellers have under 500 reviews and no dominant brand presence.

**Multi-Channel Opportunity Check:**
Assess whether the product has potential across multiple channels (e.g., Amazon + Shopify DTC, or Etsy + TikTok Shop). Multi-channel viability increases overall opportunity but also adds operational complexity.

### 3. Product Validation

Apply systematic criteria to validate product opportunities.

**Essential Criteria:**
- Monthly sales per seller: 100-300 units
- Selling price: $20 minimum
- Competition level: Low to medium
- Market trend: Stable or growing

**Exclusion Criteria — auto-reject if any apply:**

| Filter | Risk Rationale |
|--------|----------------|
| Electronics | High return rates (15-30%), certification requirements, technical support burden |
| Bulky items (>20 lbs or >18"×14"×8") | Excessive storage/shipping fees across all fulfillment channels |
| Fragile products | Damage in transit → high return rates and negative reviews |
| Major-brand-dominated market | Prohibitive ad costs; suppressed organic visibility |
| Restricted/gated categories | Requires platform approval; unpredictable timeline |
| Highly seasonal (as first product) | Inventory cash-flow risk; dead stock in off-season |
| Compliance-heavy (FDA, CPSC, etc.) | Regulatory barriers; liability exposure for new sellers |

**Validation Process:**
1. Compile market data into structured format
2. Run `${CLAUDE_SKILL_DIR}/scripts/product_criteria_checker.py` for automated validation
3. Review automated results and apply judgment
4. Document decision with supporting data

### 4. Profit Estimation

Calculate estimated profitability before final decision.

**Cost Components:**
- Product cost (target: under 30% of selling price)
- Shipping / fulfillment (warehouse, 3PL, or platform fulfillment fees)
- Platform fees (e.g., Amazon referral 15%, Etsy transaction 6.5%, Shopify subscription + payment processing)
- Advertising costs (estimate 10-15% of revenue initially)
- Returns / customer service overhead

**Platform Fee Quick Reference:**

| Platform | Typical Fee Structure |
|----------|----------------------|
| Amazon FBA | Referral fee (~15%) + FBA fulfillment fee + storage fee |
| Amazon FBM | Referral fee (~15%) + self-managed shipping |
| Etsy | Listing ($0.20) + transaction (6.5%) + payment processing (3%+$0.25) |
| Shopify | Subscription ($39+/mo) + payment processing (2.9%+$0.30) |
| TikTok Shop | Commission (varies 2-8%) + payment processing |
| DTC (own site) | Payment processing + hosting + fulfillment |

**Profit Targets:**

| Metric | Minimum | Target |
|--------|---------|--------|
| Profit margin | 25% | 30-40% |
| Profit per unit | $5 | $8+ |

---

## Research Tools

### Platform-Specific Tools

| Platform | Recommended Tools |
|----------|-------------------|
| Amazon | Helium 10 (X-Ray, Cerebro, Black Box, Trendster), Jungle Scout |
| Etsy | eRank, Marmalead |
| General / DTC | Google Trends, SEMrush, Ahrefs |
| TikTok Shop | TikTok Creative Center, Kalodata |
| Cross-platform | Google Trends, SimilarWeb |

For Helium 10 detailed usage instructions, see [helium10_guide.md](references/helium10_guide.md).

### Product Criteria Checker

Automate validation using the provided script:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/product_criteria_checker.py product_data.json
```

Input format:
```json
{
  "monthly_sales": 200,
  "price": 25.99,
  "competition_level": "medium",
  "category": "Home & Kitchen",
  "is_electronic": false,
  "is_bulky": false,
  "is_fragile": false,
  "has_major_brand": false
}
```

---

## Workflow

### Standard Research Process

1. **Discovery Phase**
   - Use one or more discovery methods to generate product ideas
   - Create list of 10-20 candidate products
   - Document source and initial observations

2. **Data Collection Phase**
   - For each candidate, gather market data using platform-appropriate tools
   - Record search volume, sales estimates, pricing, competition
   - Use product research template to organize data

3. **Validation Phase**
   - Apply essential and exclusion criteria
   - Run automated validation script
   - Calculate estimated profitability
   - Narrow list to top 3-5 candidates

4. **Deep Analysis Phase**
   - Conduct detailed competitor analysis
   - Review customer feedback and pain points
   - Assess improvement opportunities
   - Identify potential suppliers

5. **Decision Phase**
   - Compare final candidates using structured criteria
   - Make Go / Further Research / Reject decision based on data
   - Document reasoning and next steps

**Decision Matrix:**

| Verdict | Criteria |
|---------|----------|
| **Go** | Passes all exclusion filters + all market metrics PASS + margin ≥25% + profit ≥$5/unit + stable/growing trend |
| **Further Research** | Passes exclusion filters + most metrics PASS but 1-2 need deeper investigation |
| **Reject** | Triggers any exclusion filter, OR margin <25%, OR declining trend, OR ≥3 market metrics FAIL |

### Iteration and Refinement

Product research is iterative. Expect to evaluate 50-100 products before finding a strong candidate.

**Common Refinement Patterns:**
- If all products have too much competition, explore more specific niches
- If products don't meet price criteria, shift to different categories
- If sales volume is consistently too low, target broader keywords
- If major brands dominate, look for underserved sub-niches

---

## Category Guidance

**Recommended Categories:**
- Home & Kitchen (gadgets, organization, non-fragile décor)
- Pet Supplies (grooming tools, accessories, toys)
- Sports & Outdoors (fitness accessories, camping gear)
- Office Products (desk organization, accessories)
- Arts, Crafts & Sewing (craft tools, DIY kits)

**Categories to Avoid:**
- Electronics and technology
- Large or bulky items
- Fragile products
- Major brand dominated markets
- Restricted/gated categories
- Highly seasonal products (for first product)

For detailed category analysis, see [product_categories_guide.md](references/product_categories_guide.md).

---

## Common Mistakes to Avoid

| Mistake | Solution |
|---------|----------|
| Insufficient market research | Complete the full validation process before committing resources |
| Ignoring trends | Verify demand is stable or growing via Google Trends |
| Underestimating costs | Include ALL costs: platform fees, fulfillment, shipping, advertising, returns |
| Overestimating sales | Base estimates on sellers ranked 5-10, not #1 |
| Choosing difficult categories | Always run exclusion filters first |
| Following trends blindly | Check category return benchmarks; high returns destroy margins |
| Neglecting profit margins | Calculate full cost structure including all platform and fulfillment fees |
| Entering branded markets | Look for markets with no dominant brand presence |
| Single-platform thinking | Evaluate cross-channel potential to diversify revenue risk |

---

## Quick Reference

**Key Thresholds:**

| Metric | Threshold |
|--------|-----------|
| Search volume | ≥5,000/month |
| Monthly sales (per seller) | 100-300 units |
| Selling price | ≥$20 |
| Profit margin | ≥25% (target 30-40%) |
| Profit per unit | ≥$5 |
| Competitor reviews (page 1) | <500 |
| Category return rate | <10% |

---

## Additional Resources

- [helium10_guide.md](references/helium10_guide.md) — Helium 10 tool usage guide (Amazon-focused)
- [product_categories_guide.md](references/product_categories_guide.md) — Category guidance for beginners
- `${CLAUDE_SKILL_DIR}/templates/product_research_template.md` — Product research report template (read via `read_file`)
- `${CLAUDE_SKILL_DIR}/scripts/product_criteria_checker.py` — Automated criteria checker
- [Amazon FBA Calculator](https://sellercentral.amazon.com/fba/profitabilitycalculator/index)
- [Etsy Fee Calculator](https://www.etsy.com/seller-handbook/article/fees-and-payments-policy/27551923533)
- [Shopify Pricing](https://www.shopify.com/pricing)
