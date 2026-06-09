---
name: loyalty-points-designer
description: "Implement a tiered reward system to increase customer retention and lifetime value through points-based incentives and VIP benefits"
category: pricing-promotions
risk: safe
source: curated
date_added: "2026-03-12"
tags: [loyalty, points, rewards, tiers, redemption, expiration, customer-retention]
triggers: ["loyalty program", "points system", "rewards program", "earn points", "redeem points", "customer loyalty", "tier system"]
tools: [claude-code, cursor, gemini-cli, copilot, codex-cli, kiro, opencode]
platforms: [shopify, woocommerce, bigcommerce, custom]
difficulty: intermediate
---

# Design and Launch Loyalty Points Program

## Overview

A loyalty points program rewards repeat customers with points earned on purchases and specific actions, which can be redeemed for discounts. Effective programs use tiered progression (e.g., Bronze → Silver → Gold) to unlock escalating benefits, driving higher lifetime value (LTV). While most merchants use platform-native apps or plugins, the underlying architecture relies on a ledger-based system for financial accuracy and auditability.

## When to Use This Skill

- When aiming to increase repeat purchase rate and reduce customer acquisition cost (CAC) dependency.
- When launching a tiered VIP program to reward high-value customers with exclusive perks.
- When replacing generic discounts with a structured value-exchange system.
- When integrating rewards into a mobile app or headless storefront.

## Core Instructions

### Step 1: Configure Platform-Native Loyalty Settings

#### Shopify
1. In **Shopify Admin**, navigate to **Settings → Apps and sales channels**.
2. For loyalty functionality, merchants typically install a specialized loyalty app. Configure the following universal settings within your chosen app:
   - **Earning Rules**: Set the base ratio (e.g., 5 points per $1 spent).
   - **Redemption Options**: Define the point-to-dollar value (e.g., 500 points = $5 discount).
   - **Tier Thresholds**: Set spend-based or point-based entry requirements for VIP levels.
3. Ensure the app is integrated with **Shopify Checkout** to allow seamless redemption.

#### WooCommerce
1. If using a points and rewards plugin, go to **WooCommerce → Settings → Products → Points and Rewards** (or the plugin's specific menu).
2. Configure **Points Settings**:
   - **Earn Points**: Define points awarded per currency unit spent.
   - **Redemption**: Set the discount value per point.
   - **Maximum Discount**: Cap the discount per order (e.g., max 50% of subtotal).
3. Use **WooCommerce → Customers** to view and manually adjust individual balances for support cases.

#### BigCommerce
1. Navigate to the **Channel Manager** or **Apps** section to manage loyalty integrations.
2. Ensure the loyalty program is synced with **BigCommerce Customer Groups** to automate tier-based pricing or exclusive category access.

### Step 2: Implement Technical Architecture (Custom/Headless)

For custom builds or deep integrations, use an append-only ledger pattern. This ensures points cannot be "lost" and provides a clear audit trail for accounting.

#### Database Schema
```sql
CREATE TABLE loyalty_accounts (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id  UUID NOT NULL UNIQUE,
  tier         VARCHAR(16) NOT NULL DEFAULT 'bronze',
  lifetime_spend_cents INTEGER NOT NULL DEFAULT 0,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE loyalty_ledger (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id   UUID NOT NULL REFERENCES loyalty_accounts(id),
  points       INTEGER NOT NULL,  -- positive = earned, negative = redeemed/expired
  type         VARCHAR(32) NOT NULL CHECK (type IN ('purchase', 'bonus', 'referral', 'redemption', 'expiration', 'adjustment')),
  reference_id UUID,              -- order_id, review_id, etc.
  description  TEXT NOT NULL,
  expires_at   TIMESTAMPTZ,       -- NULL = never expires
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

#### Points Calculation Logic
```typescript
async function getPointsBalance(accountId: string): Promise<number> {
  const result = await db.raw(`
    SELECT COALESCE(SUM(points), 0) AS balance
    FROM loyalty_ledger
    WHERE account_id = ?
      AND (expires_at IS NULL OR expires_at > NOW())
  `, [accountId]);
  return Math.max(0, parseInt(result.rows[0].balance, 10));
}

async function awardPurchasePoints(customerId: string, orderId: string, subtotalCents: number) {
  const account = await getOrCreateAccount(customerId);
  const TIER_MULTIPLIERS = { bronze: 1, silver: 1.2, gold: 1.5 };
  const multiplier = TIER_MULTIPLIERS[account.tier] || 1;
  const points = Math.round((subtotalCents / 100) * multiplier);
  
  const expiresAt = new Date();
  expiresAt.setMonth(expiresAt.getMonth() + 12); // 1-year expiration

  await db.loyaltyLedger.insert({
    account_id: account.id, points, type: 'purchase',
    reference_id: orderId, description: `Points for order ${orderId}`, expires_at: expiresAt,
  });

  await db.loyaltyAccounts.update(account.id, {
    lifetime_spend_cents: account.lifetime_spend_cents + subtotalCents,
  });
  await recalculateTier(account.id);
}

async function redeemPoints(customerId: string, orderId: string, pointsToRedeem: number): Promise<{ discountCents: number }> {
  const account = await db.loyaltyAccounts.findByCustomerId(customerId);
  const balance = await getPointsBalance(account.id);
  if (pointsToRedeem > balance) throw new Error('Insufficient points');

  const REDEMPTION_RATE = 0.01; // 100 points = $1
  const discountCents = Math.floor(pointsToRedeem * REDEMPTION_RATE * 100);
  
  await db.loyaltyLedger.insert({
    account_id: account.id, points: -pointsToRedeem, type: 'redemption',
    reference_id: orderId, description: `Redeemed for order ${orderId}`,
  });
  return { discountCents };
}
```

## Decision Criteria & Industry Benchmarks

### Loyalty Program ROI Calculation
Calculate the success of the program using this formula:
`ROI = (Incremental Profit from Rewards Members - Cost of Points Redeemed - Program Operating Fees) / Program Operating Fees`
- **Target Benchmark**: A healthy program should deliver a **3x to 7x ROI**.
- **Redemption Rate Benchmark**: 15%–25% for small stores; 30%–50% for established brands. Low rates suggest the program isn't compelling; extremely high rates may erode margins.

### Points Liability Accounting
Points are a financial liability on the balance sheet (Deferred Revenue).
- **Calculation**: `Total Outstanding Points × Point Value × Expected Redemption Rate (Breakage)`.
- **Edge Case**: If 1,000,000 points are outstanding at $0.01 value, but historically only 20% are ever redeemed, the liability is $2,000, not $10,000. Review this quarterly with finance teams.

### Sunsetting a Program
If a program is failing (low engagement or negative margin), follow this "sunset" protocol:
1. **Notice Period**: Provide at least 60–90 days notice via email and site banners.
2. **Final Redemption**: Allow a "last call" where points can be used with no minimum order value.
3. **Conversion**: Optionally convert remaining points into fixed-value discount codes (e.g., "We've converted your 500 points into a $5 coupon valid for 3 months").

## Best Practices

- **Award points after fulfillment**: Prevent "points-churning" where customers buy items to earn points and then return the goods.
- **Display dollar value, not just points**: "You have $10 in rewards" is more psychologically compelling than "You have 1,000 points."
- **Expiration Trigger**: Automated emails 30 days and 7 days before points expire are high-converting re-engagement tools.
- **Redemption Cap**: Limit point usage to **max 50% of order value** to ensure every transaction remains cash-flow positive.
- **Tier Downgrade Policy**: Use a fixed calendar date (e.g., Jan 1st) for tier resets rather than rolling periods to simplify customer support and communication.

## Common Pitfalls & Edge Cases

| Problem | Solution |
|---------|----------|
| **Referral Fraud** | Implement checks for shared IP addresses, matching billing addresses, or "same-device" cookies between referrer and referee. |
| **Points on Sale Items** | Decide if points should be earned on discounted items. Best practice: Award points on the *paid subtotal* only. |
| **Rounding Bugs** | In multi-currency environments, always calculate points in the base currency first, then convert, to avoid decimal discrepancies. |
| **Negative Balances** | If a customer redeems points and then returns the original order that earned them, their balance may go negative. Allow this to prevent fraud. |
