---
name: coupon-discount-manager
description: "Trigger: Create and manage a coupon system with percentage and fixed discounts, usage limits, and expiration dates."
category: pricing-promotions
risk: critical
source: curated
date_added: "2026-03-12"
tags: [coupons, discounts, promotions, validation, bulk-generation, promo-codes]
platforms: [shopify, woocommerce, bigcommerce, custom]
difficulty: intermediate
---

# Create and Manage Discount Coupon System

## Overview

Coupon systems allow merchants to offer promotional codes with specific rules, such as percentage or fixed-amount discounts, minimum order requirements, usage limits, and expiration dates. Efficient coupon management is critical for running marketing campaigns, tracking performance, and protecting profit margins.

## When to Use This Skill

- When launching promotional codes for the first time.
- When migrating from simple discounts to complex, rule-based coupon engines.
- When needing to distribute unique, single-use codes for email or influencer campaigns.
- When creating restricted coupons (e.g., for specific customer segments or collections).
- When planning a seasonal promotional calendar.

## Core Instructions

### Step 1: Platform-Native Implementation

#### Shopify
1.  **Creation:** Go to **Discounts** in the Shopify sidebar.
2.  **Types:** Click **Create discount** and choose from:
    *   **Amount off products:** Percentage or fixed amount for specific SKUs.
    *   **Amount off order:** Percentage or fixed amount off the total cart.
    *   **Buy X get Y:** BOGO and bundle offers.
    *   **Free shipping:** Removes shipping costs when the code is applied.
3.  **Config:** Set **Minimum purchase requirements**, **Customer eligibility** (all, segments, or individuals), and **Usage limits** (total count and per-customer limit).
4.  **Shopify Scripts (Shopify Plus):** Use **Shopify Scripts** for advanced stacking logic or auto-applying discounts based on cart items without requiring a code.

#### WooCommerce
1.  **General:** Go to **WooCommerce → Coupons → Add coupon**.
2.  **Settings:** Under the **General** tab, set the **Discount type**, **Coupon amount**, and **Expiry date**.
3.  **Restrictions:** Use the **Usage restriction** tab to set **Minimum/Maximum spend**, **Exclude sale items**, and **Restrict to specific products/categories**.
4.  **Limits:** Under **Usage limits**, define the total uses per coupon and per customer.

#### BigCommerce
1.  **Creation:** Go to **Marketing → Coupon Codes → Create Coupon Code**.
2.  **Config:** Set the code, type (Percentage vs. Fixed), and what it applies to (all, category, or product).
3.  **Restrictions:** Set **Minimum order**, **Max uses**, and **Max uses per customer**.

### Step 2: Custom / Technical Standards (Headless)

For headless storefronts, use atomic redemption logic to prevent over-use during high-traffic events:

```typescript
// Atomic redemption logic inside the order creation transaction
async function redeemCoupon(tx: Tx, couponId: string, customerId: string, orderId: string) {
  const result = await tx.raw(
    `UPDATE coupons SET usage_count = usage_count + 1
     WHERE id = ? AND (usage_limit IS NULL OR usage_count < usage_limit)
     RETURNING id`,
    [couponId]
  );
  if (result.rowCount === 0) throw new Error('COUPON_EXHAUSTED');
  
  await tx.couponRedemptions.insert({ coupon_id: couponId, customer_id: customerId, order_id: orderId });
}
```

### Step 3: Decision Criteria & Deepening

#### Coupon Abuse Prevention Strategies
Protect your margins by preventing serial discount seekers:
1.  **Unique Code Generation:** Use unique, single-use codes instead of generic ones (e.g., `SUMMER10`) for email marketing.
2.  **Email Locking:** Restrict a coupon to a specific customer email address.
3.  **Honeypot Monitoring:** Monitor orders where multiple coupons are attempted.
4.  **IP/Device Fingerprinting:** For high-value offers, prevent the same user from using multiple accounts to redeem the same code.

#### Campaign Tracking Methodology
Measure the true ROI of each discount campaign:
*   **UTM Parameters:** Always append UTM tags to coupon links (e.g., `?utm_source=facebook&utm_campaign=summer_sale&promo=SUMMER10`).
*   **Segment Performance:** Compare the AOV and Customer Lifetime Value (CLV) of "coupon users" vs. "non-coupon users."
*   **Incremental Revenue:** Determine if the coupon drove a sale that wouldn't have happened otherwise, or if it just subsidized an existing customer.

#### Promotional Calendar Planning
Plan discounts at least one quarter in advance:
*   **Inventory Clearing:** Use deep discounts (30-50%) for end-of-season Class C inventory.
*   **Customer Acquisition:** Use 10-15% "Welcome" codes.
*   **Loyalty Retention:** Send "Birthday" or "VIP Anniversary" codes to high-CLV segments.

#### Discount Impact on Brand Perception
Frequent discounting can devalue your brand.
*   **Premium Positioning:** Luxury brands should focus on "Gift with Purchase" or "Free Shipping" rather than percentage discounts.
*   **Expectation Management:** Avoid running a sale every weekend, as customers will wait for the next discount rather than buying at full price.

## Best Practices

- **Normalize Codes to Uppercase:** Always store and compare codes in uppercase to avoid "code not found" errors due to case sensitivity.
- **Set Minimum Order Value (MOV):** Use MOV to ensure the discount doesn't result in a negative gross margin for the order.
- **Expiry Urgency:** Set short expiry windows (24-48 hours) for recovery coupons to drive immediate action.
- **Limit Stacking:** Unless explicitly desired, disable coupon stacking so customers cannot use multiple codes on one order.

## Common Pitfalls

| Problem | Solution |
|---------|----------|
| Stacking Errors | Clearly define in settings if a coupon can be combined with other discounts or free shipping. |
| Coupon Leaked to Sites | Use unique codes with 1-use limits for influencer campaigns to prevent codes from appearing on "RetailMeNot" or "Honey." |
| Forgotten Expiry | Set end dates for all promotional coupons to prevent customers from using a "Black Friday" code in May. |
| Margin Erosion | Calculate the impact on net margin *after* shipping and discount costs before activating any code. |
