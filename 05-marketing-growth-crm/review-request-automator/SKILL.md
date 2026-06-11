---
name: review-request-automator
description: "Design and automate post-purchase review collection workflows. Implement timed request sequences, multi-media incentives, and moderation logic to maximize social proof and conversion rates."
category: marketing-growth
risk: safe
source: curated
date_added: "2026-03-12"
tags: [social-proof, product-reviews, customer-feedback, reputation-management, conversion-optimization]
triggers: ["automate review requests", "generate product reviews", "setup review incentives", "social proof automation"]
platforms: [shopify, woocommerce, amazon-seller-central, bigcommerce]
difficulty: intermediate
---

# Review Request Automator

## Overview

Product reviews are the most critical form of social proof in ecommerce. A single review can increase a product's conversion rate by up to 10%, while 50+ reviews can drive a 40% lift. This skill focuses on building an automated "Review Engine" that captures feedback at the peak of customer satisfaction, incentivizes high-value content (photos/videos), and manages negative feedback constructively.

## Strategic Timing Framework

| Milestone | Timing | Objective | Strategy |
|-----------|--------|-----------|----------|
| **Delivery** | T+0 | Satisfaction Check | Ensure the item arrived intact. No review ask yet. |
| **First Use** | T+7 to T+14 | The Request | Ask for a star rating. Timing depends on product type (e.g., 3 days for apparel, 21 days for supplements). |
| **Nudge** | T+21 | Content Incentive | Follow-up with non-respondents. Offer a "Photo/Video Incentive." |
| **Moderation** | Continuous | Quality Control | Filter for profanity/fraud and respond to low ratings. |

### Decision Criteria: Review vs. NPS
- **Product Review:** Best for SKU-level social proof. Ask "How do you like the [Product Name]?"
- **Net Promoter Score (NPS):** Best for brand-level loyalty. Ask "How likely are you to recommend [Brand] to a friend?" 
- **Rule of Thumb:** Send Product Review requests for *every* order. Send NPS surveys only once every 90 days per customer to avoid survey fatigue.

---

## Execution Steps

### Step 1: Automated Request Configuration

#### Shopify Admin
1.  **Native Integration:** Ensure "Product Reviews" are enabled in your theme settings.
2.  **Trigger Logic:** Use **Shopify Flow** to trigger an "External Action" (e.g., Email Send) only when the `Order.fulfillment_status` is `delivered`.
3.  **Conditions:** Exclude orders that have been `Refunded` or have an active `Return` request to avoid asking for a review from an unhappy customer.

#### WooCommerce Admin
1.  Navigate to **Settings > Products > General**. Enable "Product Reviews" and "Show 'verified owner' label."
2.  **AutomateWoo:** Create a workflow where the trigger is `Order Status Changed to Completed`. Add a `Time Delay` of 7 days before sending the "Review Request" email.

#### Amazon Seller Central
1.  Use the **"Request a Review"** button in Manage Orders (must be done between 5 and 30 days after delivery).
2.  **Automation:** Use an Amazon-approved "Request a Review" automation tool that utilizes the official Amazon API to trigger these requests based on delivery dates.

### Step 2: High-Value Content Incentives

Photo and Video reviews convert 3-4x better than text-only reviews. 

1.  **Incentive Design:** Offer a discount (e.g., 15% off next order) or "Loyalty Points" specifically for **media uploads**, not for the rating itself.
2.  **Compliance Note:** Under FTC guidelines (US) and similar regulations globally, you must disclose if a review was incentivized. Ensure your review widget automatically adds a "Received a discount/gift for this review" badge.

### Step 3: Technical Customization (Headless/Custom)

For maximum conversion, use "Tokenized/Signed" links in your emails so customers can submit a review with one click without logging in.

```typescript
import jwt from 'jsonwebtoken';

// Generate a one-click review URL
function createReviewLink(orderId: string, sku: string, rating: number) {
  const token = jwt.sign({ orderId, sku, rating }, process.env.SECRET_KEY, { expiresIn: '14d' });
  return `https://yourstore.com/submit-review?token=${token}&prefill_rating=${rating}`;
}
```

### Step 4: Negative Feedback Loop

A 1-star review is a "Customer Service Signal."
- **Auto-Quarantine:** Route all reviews <= 2 stars to a "Pending" folder.
- **The "Service Recovery" Protocol:** Reach out to the customer within 24 hours of a negative review. If you resolve their issue (e.g., send a replacement), you may politely ask them to update their review. **Never** offer a refund *in exchange* for deleting a review (Review Gating), as this is illegal in many regions (EU/UK/US).

---

## Benchmarks & Performance Targets

| Metric | Target (Good) | Target (Elite) |
|--------|---------------|----------------|
| **Review Response Rate** | 3% - 7% | > 12% |
| **Media Review % (Photos)** | 15% | > 30% |
| **Average Rating** | 4.2 Stars | 4.7 Stars |
| **Response Rate to Negative Reviews** | 50% | 100% |

---

## Troubleshooting & Common Pitfalls

- **Review Gating:** Only publishing positive reviews. This is a major compliance risk. Search engines and platforms may penalize or ban stores found "Gating" reviews.
- **The "Early Ask":** Requesting a review before the product arrives due to shipping delays. **Solution:** Use "Carrier Integration" to trigger the email only on the `DELIVERED` event, not the `SHIPPED` event.
- **Fake Review Detection:** Monitor for spikes in reviews from the same IP address or reviews containing generic "AI-generated" text.
- **Amazon Policy Violations:** Never include a link to your Shopify store or a request for a "5-star" review in an Amazon insert or message. Amazon only allows neutral requests for "honest feedback."
