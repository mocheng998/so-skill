---
name: discount-promotion-engine
description: "Configure and manage complex ecommerce promotions including tiered quantity pricing, BOGO, and cart-level rules while ensuring margin protection and stacking governance."
category: pricing-promotions
risk: critical
source: curated
date_added: "2026-03-12"
tags: [discounts, promotions, pricing, coupons, bogo, tiered-pricing, rules-engine]
triggers: ["build discount system", "implement promo codes", "create discount engine", "add coupon support", "tier pricing", "BOGO rules"]
platforms: [shopify, woocommerce, bigcommerce, custom]
difficulty: intermediate
---

# Build Flexible Discount and Promotion Rules

## Overview

A discount engine evaluates promotions against a cart and applies the right discounts in the right order. Every major ecommerce platform has a native system for managing percentage off, fixed amounts, BOGO (Buy One Get One), and tiered thresholds. Success requires not just technical configuration, but strict governance to prevent "discount stacking" from eroding profit margins.

## When to Use This Skill

- When implementing tiered pricing (e.g., Buy 3+ get 10% off, Buy 10+ get 20% off).
- When creating automatic discounts that apply based on cart subtotal or customer segment.
- When launching BOGO, bundle, or "Gift with Purchase" (GWP) promotions.
- When configuring complex stacking rules (e.g., "Product discount can combine with Free Shipping, but not with another Order discount").
- When auditing promotion ROI to ensure discounts drive incremental value.

## Core Instructions

### Step 1: Platform-Native Configuration

| Platform | Native Capabilities | Advanced Customization |
|----------|---------------------|------------------------|
| **Shopify** | Automatic discounts, BOGO, Buy X Get Y, amount off products/order. | Use **Shopify Functions** (JavaScript) for custom stacking logic or unique eligibility rules. |
| **WooCommerce** | Core Coupons: fixed amount, percentage, free shipping. | Use WooCommerce core "Individual use only" to prevent stacking; use "Usage limits" to control velocity. |
| **BigCommerce** | Promotions Engine: Cart-level, Item-level, Free items, BOGO. | Use **Price Lists** for customer-group specific or wholesale tiered pricing. |
| **Custom / Headless** | Requires a custom evaluation engine. | See the technical pattern in Step 3. |

### Step 2: Configure Common Promotion Types

#### Automatic Discounts & BOGO
- **Automatic (No Code)**: In Shopify/BigCommerce, create a discount and select "Automatic" or "No Code Required". These apply to all eligible carts during the active window.
- **BOGO (Buy X Get Y)**:
    1. Define **Buy X**: Minimum quantity or subtotal of specific products/collections.
    2. Define **Get Y**: Quantity of items at a discounted rate (e.g., 100% off for free).
    3. Set **Usage Limits**: Cap the number of times a customer can trigger the BOGO in a single order.

#### Tiered Quantity Pricing
1. Define the tiers:
   - Tier 1: 1–4 units (0% discount)
   - Tier 2: 5–9 units (10% discount)
   - Tier 3: 10+ units (20% discount)
2. In **Shopify**, use "Quantity Breaks" logic via Shopify Functions.
3. In **BigCommerce**, create a **Price List** with explicit unit prices per quantity bracket and assign it to the relevant customer group.

### Step 3: Technical Standard for Discount Evaluation (TypeScript)

For custom storefronts or headless architectures, the evaluation engine must be idempotent and strictly server-side.

```typescript
interface Discount {
  id: string;
  type: 'percentage' | 'fixed_amount' | 'bogo';
  value: number;        // percentage (0-100) or cents
  isStackable: boolean;
  minCartCents?: number;
  minQuantity?: number;
  entitledProductIds?: string[];
  excludedProductIds?: string[];
}

function evaluateDiscounts(
  cart: { lines: CartLine[]; subtotalCents: number },
  discounts: Discount[]
): { discountId: string; amountCents: number }[] {
  // 1. Filter active and eligible discounts
  const eligible = discounts.filter(d => 
    (!d.minCartCents || cart.subtotalCents >= d.minCartCents)
  );

  // 2. Sort: apply non-stackable first to establish "exclusive" logic
  const sorted = [...eligible].sort((a, b) => (a.isStackable ? 1 : -1));

  const applications: { discountId: string; amountCents: number }[] = [];
  let exclusiveApplied = false;

  for (const discount of sorted) {
    if (exclusiveApplied) break;

    const eligibleLines = cart.lines.filter(l => 
      (!discount.entitledProductIds || discount.entitledProductIds.includes(l.productId))
    );

    let amount = 0;
    if (discount.type === 'percentage') {
      amount = Math.round(eligibleLines.reduce((s, l) => s + (l.price * l.qty), 0) * (discount.value / 100));
    } else if (discount.type === 'bogo') {
      // Logic for Buy X Get Y free
      for (const line of eligibleLines) {
        const freeItems = Math.floor(line.qty / (discount.minQuantity + 1));
        amount += freeItems * line.price;
      }
    }

    if (amount > 0) {
      applications.push({ discountId: discount.id, amountCents: amount });
      if (!discount.isStackable) exclusiveApplied = true;
    }
  }
  return applications;
}
```

## Best Practices & Stacking Rules

- **Always Calculate Server-Side**: Never trust discount amounts passed from the frontend. Recalculate the entire cart total and discount allocation at the moment of checkout/payment.
- **Strict Stacking Governance**: 
    - Rule: Product-level discounts (e.g., "10% off shirts") should generally not stack with Order-level discounts (e.g., "$20 off your total order").
    - Rule: Automatic discounts should always be evaluated before coupon codes.
- **Exclude Sale Items**: Ensure that items already marked down (compare-at price) are excluded from additional percentage-off promotions to protect margins.
- **Discount Caps**: For percentage discounts (e.g., 50% off), always set a "Max Discount Amount" (e.g., "$100 max") to prevent abuse on high-ticket orders.

## Deepening: ROI & Governance

### Promotion ROI Calculation
Measure the incremental impact, not just the total revenue associated with a code:
- **Formula**: `Incremental Margin = (Total Promo Revenue - Promo Discount Cost) - (Baseline Expected Revenue * Baseline Margin)`.
- If the incremental margin is negative, the promotion is simply "cannibalizing" full-price sales.

### Discount Velocity Monitoring
Monitor "coupon leakage" using your analytics platform:
- **Trigger**: If a specific code (e.g., `WELCOME10`) suddenly accounts for >30% of all orders, check deal/coupon aggregator sites.
- **Solution**: Switch to unique, single-use codes generated via API for welcome flows rather than generic strings.

### Promotional Calendar Governance
Maintain a centralized calendar that lists:
- **Campaign Name**: (e.g., Black Friday 2026)
- **Priority**: (1-10)
- **Stacking Permissions**: (Can stack with Free Shipping? Yes/No)
- **Approval Signature**: Merchandising + Finance.

## Common Pitfalls

| Problem | Root Cause / Solution |
|---------|----------|
| **Negative Order Total** | Caused by fixed-amount discounts exceeding the subtotal. Always `Math.max(0, subtotal - discount)`. |
| **BOGO "Loophole"** | Customer adds 1 item, gets 1 free, then removes the paid item. **Solution**: Link items in the cart so the free item is removed if the paid item quantity drops below the threshold. |
| **Double Dipping** | Customer uses a 10% auto-discount AND a 10% coupon. **Solution**: Set all discounts to "Non-stackable" by default in your platform settings. |
| **Price Flickering** | Prices change on the cart page after a delay. **Solution**: Ensure discount evaluation happens in the initial page load/SSR, not just via client-side JS. |
