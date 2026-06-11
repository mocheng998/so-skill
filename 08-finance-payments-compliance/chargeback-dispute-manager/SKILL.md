---
name: chargeback-dispute-manager
description: "Prevent and manage ecommerce chargebacks using fraud scoring, compelling evidence automation, and card network compliance standards."
---

# Manage Chargeback Disputes and Prevention

## Overview

A chargeback occurs when a cardholder disputes a transaction with their bank, forcing an immediate reversal of funds and a non-refundable fee ($15–$100 per dispute) charged to the merchant. Maintaining a low dispute ratio is critical for business continuity:
- **0.65% Early Warning**: Visa begins monitoring your account.
- **0.90% Critical**: High risk of being placed in a formal monitoring program.
- **1.00%+ Visa/Mastercard Monitoring**: Triggers monthly fines and potential termination of your merchant account.

Effective management requires a dual-track strategy: preventing fraudulent transactions before they ship and winning legitimate disputes through automated evidence submission.

## When to Use This Skill

- When your chargeback ratio exceeds 0.5% or fluctuates seasonally.
- When your team is manually compiling evidence and missing strict 7–21 day response windows.
- When "friendly fraud" (legitimate customers claiming non-receipt or unauthorized use) impacts margins.
- When expanding into international markets with higher fraud profiles.

## Core Framework

### 1. Dispute Management Infrastructure

Regardless of your ecommerce platform (Shopify, WooCommerce, BigCommerce), your dispute handling is determined by your payment processor.

| Integration Type | Dispute Visibility | Evidence Submission Method |
|------------------|--------------------|----------------------------|
| **Platform-Native** (e.g., Shopify Payments) | Integrated in Store Admin | Form-based submission within the order or payment settings. |
| **Gateway Dashboard** (e.g., Stripe, PayPal) | Payment Provider Portal | Manual upload or API-driven evidence packages in the provider's dashboard. |
| **Custom / API** | Webhook-driven (`charge.dispute.created`) | Programmatic evidence assembly using stored order, shipping, and IP data. |

### 2. Proactive Fraud Prevention (Pre-Shipment)

Prevention is the most effective way to protect your merchant health.

- **Enable Fraud Scoring**: Use rules-based engines to evaluate every transaction. High-risk orders should be automatically held for manual review or canceled before fulfillment.
- **Address Verification Service (AVS) & CVV**: Require an exact match for the billing zip code and the 3-digit security code. Discrepancies are the leading indicator of stolen card usage.
- **3D Secure (3DS)**: Implement 3DS for high-value or international transactions. This shifts the liability for "unauthorized" chargebacks from the merchant to the card issuer.
- **Velocity Limits**: Block multiple rapid-fire attempts from the same IP, email, or device fingerprint.
- **Chargeback Guarantees**: For high-risk categories, consider services that assume financial liability for fraud-related disputes in exchange for a percentage of transaction volume.

### 3. Understanding Chargeback Reason Codes

Banks categorize disputes into reason codes. Your response strategy depends on the code:

| Category | Typical Codes (Visa/MC) | Win Strategy |
|----------|-------------------------|--------------|
| **Fraud** | 10.4, 83 | Provide proof of 3DS, prior undisputed history, or IP/billing match. |
| **Item Not Received** | 13.1, 30 | Provide carrier tracking showing "Delivered" to the specific address. |
| **Not as Described** | 13.3, 53 | Provide proof the customer accepted your terms, or that they haven't returned the item. |
| **Canceled Subscription** | 13.5, 41 | Provide proof of the cancellation policy and the date the customer agreed to it. |

### 4. The "Fight vs. Concede" Decision Logic

Not all disputes should be fought. Every dispute—won or lost—counts against your ratio, but fighting takes time.

- **Fight if**: You have clear tracking showing delivery; the customer has a history of successful orders; the value is high enough to justify the labor.
- **Concede if**: You missed the shipping deadline; the product was genuinely defective; you lack the required evidence (e.g., no tracking number).
- **Nuance**: Conceding does not remove the "mark" from your ratio, but it stops further fees or escalations. Use it to preserve team resources.

### 5. Compelling Evidence Framework

When responding to a dispute, your "Evidence Package" should include:

1.  **Transaction Details**: Date, amount, and authorization code.
2.  **Proof of Delivery**: Carrier name, tracking number, and a screenshot of the delivery confirmation (including the destination city).
3.  **Customer Context**: IP address, device fingerprint, and billing vs. shipping address comparison.
4.  **Communication Logs**: Any emails or chat transcripts showing the customer was satisfied or acknowledged receipt.
5.  **Policy Acceptance**: A timestamped record showing the customer checked a box agreeing to your "Terms of Service" or "Refund Policy" at checkout.

### 6. Visa Compelling Evidence 3.0 (CE 3.0)

For "Unauthorized" fraud disputes, Visa allows you to shift liability back to the bank if you can prove a "Qualified Business Relationship."
- **Requirement**: Provide 2 prior undisputed transactions from the same cardholder within the last 120 days.
- **Data Points**: You must include the IP address, device ID, and shipping address used in those prior orders to prove the current order is consistent with established behavior.

## Industry Benchmarks & Monitoring

Monitor these thresholds monthly to avoid catastrophic account loss:

- **Response Window**: 7–21 days (non-negotiable). Missing this is an automatic loss.
- **Win Rate Target**: 40%–60% for Physical Goods; 20%–30% for Digital Goods.
- **Fee Impact**: Budget $15–$100 per dispute. High ratios increase your per-transaction processing costs.

## Handling Friendly Fraud Trends

"Friendly fraud" (first-party fraud) occurs when a legitimate customer disputes a valid charge.
- **Trend**: Customers using "Item Not Received" as a way to get a refund while keeping the product.
- **Countermeasure**: Require signature confirmation for orders over $250. This is often the only evidence banks accept to overturn a high-value dispute.
- **Trend**: "Digital Goods" fraud where customers claim they didn't receive access.
- **Countermeasure**: Provide server logs showing the customer logged in or downloaded the file after the purchase timestamp.
