---
name: b2b-payment-terms-optimizer
description: "Establish and manage B2B trade credit, net-terms, and automated invoicing to accelerate sales cycles while mitigating credit risk"
category: payments-checkout
risk: safe
source: curated
date_added: "2026-03-12"
tags: [payment-terms, b2b, credit-management]
triggers: ["payment terms", "net-30 billing", "net-60", "credit terms", "B2B credit", "early payment discount", "credit limit", "trade credit", "payment terms management"]
tools: [claude-code, cursor, gemini-cli, copilot, codex-cli, kiro, opencode]
platforms: [shopify, woocommerce, bigcommerce, custom]
difficulty: intermediate
---

# Configure B2B Payment Terms and Credit Limits

## Overview

Payment terms allow B2B customers to purchase goods on "Trade Credit," paying at a later date (e.g., Net 30, Net 60). This is a critical lever for increasing average order value (AOV) and conversion in wholesale environments. Managing this requires a balance between offering competitive terms and enforcing strict credit limits to prevent bad debt.

## When to Use This Skill

- When transitioning from a retail (B2C) model to a wholesale (B2B) or distribution model.
- When high-value customers request "Pay on Invoice" options to align with their own cash flow cycles.
- When you need to automate the collection of accounts receivable (AR) via automated dunning emails.
- When credit losses or late payments are impacting the business's operating cash flow.

## Core Instructions

### Step 1: Configure Platform-Native B2B Features

#### Shopify Plus (B2B Native)
1. In **Shopify Admin**, go to **Customers → Companies**.
2. Create or select a company. Under **Locations**, click a location and navigate to **Payment terms**.
3. Select from presets (Net 7, 15, 30, 60, 90) or define a custom duration.
4. **Credit Limit**: Set the maximum outstanding balance for the company. Shopify will automatically block or flag orders that exceed this threshold.
5. When the buyer checkouts, they can select "Pay on Invoice" as their payment method. Shopify generates an invoice with the due date calculated from the order date.

#### BigCommerce B2B Edition
1. Navigate to **B2B Edition → Company Management**.
2. Under the **Company** profile, go to the **Credit** tab.
3. Set the **Credit Limit** and **Payment Terms** (e.g., Net 30).
4. Set the **Credit Status** to "Approved."
5. The buyer's portal will now show "Pay on Account" at checkout, and they can view their "Credit Balance" in real-time.

#### WooCommerce
1. Use a B2B-specific extension to enable "Customer Groups" with assigned payment methods.
2. Assign the "Invoice" or "Check/Bank Transfer" method specifically to the "Wholesale" group.
3. Manually set a "Credit Limit" attribute on the customer profile and use a hook to validate the cart total against the customer's open invoice balance during checkout.

### Step 2: Implement Technical Credit Checks (Custom/Stripe)

For headless or custom platforms, use Stripe Invoicing for automated lifecycle management.

#### Stripe Invoicing Implementation
```javascript
// 1. Create a customer with credit metadata
const customer = await stripe.customers.create({
  email: 'procurement@client-corp.com',
  name: 'Client Corp',
  metadata: { credit_limit_cents: '5000000', terms: 'net_30' }
});

// 2. Check credit availability before finalizing order
async function checkCreditAvailability(customerId, orderAmountCents) {
  const customer = await stripe.customers.retrieve(customerId);
  const creditLimit = parseInt(customer.metadata.credit_limit_cents);

  // Calculate open balance from 'open' and 'uncollectible' invoices
  const invoices = await stripe.invoices.list({ customer: customerId, status: 'open' });
  const openBalance = invoices.data.reduce((sum, inv) => sum + inv.amount_remaining, 0);

  const availableCredit = creditLimit - openBalance;
  return orderAmountCents <= availableCredit;
}

// 3. Create a Net-30 invoice
const invoice = await stripe.invoices.create({
  customer: customer.id,
  collection_method: 'send_invoice',
  days_until_due: 30,
  auto_advance: true // Automatically finalize and send
});
```

## Decision Criteria & Industry Benchmarks

### Customer Tiering × Payment Terms
| Tier | Terms | Rationale |
|------|-------|-----------|
| **New Accounts** | Prepay / Net 15 | No historical data. Limit initial credit to <$5,000. |
| **Established** | Net 30 | Standard industry terms. Increase limit based on 6 months of on-time pay. |
| **Strategic** | 2/10 Net 30 | Offer 2% discount for payment in 10 days. Incentivizes cash flow. |
| **High Risk** | Prepay Only | Accounts with >2 late payments in a rolling 12-month period. |

### DSO (Days Sales Outstanding) Interpretation
`DSO = (Average Accounts Receivable / Total Credit Sales) × 365 days`
- **Target**: 30–40 days for Net 30 terms.
- **Warning**: If DSO exceeds 45 days, it indicates that your "Net 30" customers are actually taking 45+ days to pay, signifying poor collection efficiency or deteriorating customer credit.

### Early Warning Indicators for Credit Risk
Red flags that suggest a customer's credit limit should be reduced or revoked:
1. **Rounded Payments**: Paying $10,000 against a $10,432.15 invoice suggests cash flow strain.
2. **Broken Promises**: Failing to pay on a "re-promised" date (e.g., "Check is in the mail by Friday").
3. **Limit Maxing**: Consistently hovering at 95%+ of their credit limit without paying down existing balances.

## Deep Analysis: Advanced Credit Strategies

### Trade Credit Insurance
For high-limit accounts (>$100,000), merchants should consider **Trade Credit Insurance** (e.g., Allianz Trade). This protects the merchant's balance sheet if a major customer goes insolvent. The insurer provides the credit limit recommendation based on their proprietary data.

### The "2/10 Net 30" Formula
This term means: "2% discount if paid in 10 days, otherwise the full balance is due in 30."
- **Financial Equivalent**: This is an annualized interest rate of **~36.7%** for the customer.
- **Strategy**: It is almost always better for the merchant to pay 2% to receive cash 20 days early than to rely on bank financing for working capital.

## Best Practices

- **Never ship to accounts on "Credit Hold"**: Once goods leave the warehouse, you lose 90% of your leverage. Ensure the OMS blocks shipping for any customer with an "Overdue" status.
- **Annual Credit Review**: Set a calendar reminder to review every credit account's limit and terms every 12 months.
- **Automated Dunning**: Use a "3-2-1" reminder strategy: 3 days before due, 2 days after due, 1 week after due.
- **Separation of Duties**: The salesperson who wants the commission should *not* be the one who approves the credit limit. Credit approval should be a finance function.

## Common Pitfalls & Edge Cases

| Problem | Solution |
|---------|----------|
| **Early discount taken late** | Ensure the system automatically rejects the 2% discount if the payment date is Day 11 or later. |
| **Partial Payments** | Clearly state in your terms that partial payments do not stop the "overdue" clock for the remaining balance. |
| **Parent/Child Accounts** | For franchises, determine if the credit limit is at the individual store level or the corporate parent level. |
| **Stale Credit Limits** | If a customer hasn't ordered in 24 months, revert their status to "Prepay" until a fresh credit review is completed. |
