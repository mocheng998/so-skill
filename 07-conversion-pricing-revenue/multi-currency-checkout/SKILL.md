---
name: multi-currency-checkout
description: "Configure multi-currency support to allow international customers to browse and pay in their local currency with automated exchange rates and localized rounding"
category: payments-checkout
risk: critical
source: curated
date_added: "2026-03-12"
tags: [multi-currency, forex, localization, exchange-rates, formatting, i18n, checkout]
triggers: ["multi currency", "currency conversion", "international pricing", "exchange rate", "currency selector", "localize prices"]
tools: [claude-code, cursor, gemini-cli, copilot, codex-cli, kiro, opencode]
platforms: [shopify, woocommerce, bigcommerce, custom]
difficulty: intermediate
---

# Enable Multi-Currency Pricing and Checkout

## Overview

Multi-currency support allows international shoppers to view prices and complete transactions in their local currency. This significantly improves conversion rates by removing the "mental math" and foreign transaction fee uncertainty for customers. Implementation involves three layers: localized display (UI), exchange rate management (FX), and multi-currency settlement (Payment Gateway).

## When to Use This Skill

- When expanding to international markets where customers expect localized pricing.
- When analytics show high "Add to Cart" rates from foreign countries but low "Checkout Completion."
- When implementing a global storefront where the merchant wants to control regional margins via fixed price overrides.
- When integrating mainstream gateways like Stripe or PayPal that support multi-currency settlement.

## Core Instructions

### Step 1: Configure Platform-Native Multi-Currency

#### Shopify Admin (Shopify Markets)
1. Navigate to **Settings → Markets**.
2. Click **Add market** or manage an existing one (e.g., "European Union").
3. Under **Currencies and pricing**:
   - Enable local currencies (e.g., EUR, GBP, JPY).
   - **Exchange Rates**: Set to "Automatic" for daily updates or "Manual" for stable seasonal pricing.
   - **Price Adjustment**: Add a percentage markup (e.g., 2%) to cover FX conversion fees.
   - **Rounding**: Enable rounding to ensure prices look natural (e.g., €19.99 instead of €19.84).
4. In **Online Store → Themes → Customize**, enable the **Country/Region selector** in the header or footer.

#### WooCommerce Admin (WooCommerce Payments)
1. Ensure **WooCommerce Payments** is active.
2. Go to **Payments → Settings → Multi-currency**.
3. Click **Add Currencies** and select target markets.
4. For each currency:
   - Configure **Rounding Rules** (e.g., round to the nearest 0.99).
   - Set the **Exchange Rate** source (WooCommerce provides a daily feed).
5. Add the "Currency Switcher" block or widget to your storefront for customer selection.

#### BigCommerce Admin
1. Go to **Settings → Store Setup → Currencies**.
2. Click **Add a Currency** and choose the desired currency code.
3. Configure the **Exchange Rate** (Manual or Automatic via BigCommerce's feed).
4. Set the **Default Currency** (used for reporting) and ensure the new currency is "Enabled."
5. In **Storefront → My Themes → Customize**, verify the currency selector is visible in the header.

### Step 2: Implement Technical Logic (Custom/Headless)

For headless storefronts, use server-side currency detection and Stripe's multi-currency Payment Intents.

#### Exchange Rate Caching
```javascript
// Fetch and cache daily exchange rates from a reliable provider
async function getExchangeRates() {
  const cached = await redis.get('exchange_rates');
  if (cached) return JSON.parse(cached);

  const res = await fetch(`https://api.exchangerate.host/latest?base=USD`);
  const { rates } = await res.json();

  // Cache for 24 hours to ensure stable pricing during a user session
  await redis.setex('exchange_rates', 86400, JSON.stringify(rates));
  return rates;
}
```

#### Stripe Multi-Currency Charge
```javascript
// Charge in customer's currency — Stripe handles settlement in your payout currency
const paymentIntent = await stripe.paymentIntents.create({
  // Use displayPrice * 100 for cents-based currencies
  amount: isZeroDecimalCurrency(currency) ? Math.round(price) : Math.round(price * 100),
  currency: customerCurrency.toLowerCase(), 
  automatic_payment_methods: { enabled: true },
  metadata: { base_currency_amount: String(originalUSDAmount) },
});

function isZeroDecimalCurrency(currency) {
  return ['JPY', 'KRW', 'VND'].includes(currency.toUpperCase());
}
```

## Decision Criteria & Industry Benchmarks

### Currency Risk Management (FX Hedging)
Currency values fluctuate intraday. To protect margins:
- **Conversion Markup**: Add a **1.5% to 3% buffer** to the exchange rate. This covers the spread charged by payment gateways (Stripe/Shopify Payments usually charge 1.5%–2% for conversion) and protects against sudden rate drops.
- **Fixed Regional Pricing**: For high-volume markets, use fixed prices (e.g., always €49.00) rather than dynamic conversion to maintain consistent brand positioning.

### Reporting & Accounting
- **Base vs. Transaction Currency**: Always store the `base_currency_amount` and `exchange_rate` alongside the `transaction_amount` in your database.
- **Consolidated Reporting**: Your accounting software should fetch the base currency value for tax reporting, regardless of what the customer paid.

### When NOT to Implement Multi-Currency
- **Low Margin Products**: If your net margin is <5%, FX volatility can easily turn a profit into a loss.
- **High Shipping Complexity**: If international shipping costs vary wildly, dynamic currency conversion might not be enough. Consider regional sub-domains (e.g., .co.uk) with dedicated inventory and pricing instead.

## Best Practices

- **Zero-Decimal Verification**: **JPY (Yen)** and **KRW (Won)** do not use decimals. A common bug is charging ¥2,999 as ¥29.99. Always use a helper function to determine the correct minor units for the gateway.
- **Daily Rate Refresh**: Refresh rates at a specific time daily (e.g., 00:00 UTC) rather than per-request to ensure price stability while the user is browsing.
- **Persistent Selection**: Store the user's currency choice in a server-side cookie or local storage to prevent the price from "flashing" or reverting to the base currency during navigation.
- **Rounding Rules**: Apply natural rounding (e.g., $19.99, £14.95). In some cultures (like Japan), whole numbers are preferred (¥3,000 instead of ¥2,999.50).

## Verification Test Scenarios

1. **Locale Detection**: Use a VPN/Proxy to visit from the UK; prices should automatically show in GBP.
2. **Checkout Consistency**: Verify that the price shown on the Product Page matches exactly in the Cart and the final Payment Gateway modal.
3. **Refund Integrity**: Ensure that refunding an order in the base currency correctly calculates the equivalent amount in the transaction currency based on the *original* exchange rate.
4. **Rounding Accuracy**: Test a price that converts to a messy decimal (e.g., $10.00 → €9.234) and ensure it rounds according to your configured rules.
5. **Zero-Decimal Checkout**: Place a test order in JPY and verify the Stripe/Gateway dashboard shows the correct integer amount.
