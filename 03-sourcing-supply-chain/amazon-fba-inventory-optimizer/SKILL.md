---
name: amazon-fba-inventory-optimizer
description: >
  Manage Amazon FBA inventory health, IPI score, restock limits, and storage fees. 
  Trigger this skill for questions about improving IPI scores, managing FBA storage/capacity limits, 
  avoiding long-term storage fees or aged inventory surcharges, calculating restock quantities, 
  balancing in-stock rates vs. excess inventory, and peak season inventory planning.
---

# Amazon FBA Inventory Optimizer

## IPI Score Explained

The **Inventory Performance Index (IPI)** is Amazon's health metric for FBA sellers.
It determines your monthly storage capacity limit.

**IPI Threshold: 400**

- IPI ≥ 400: No storage capacity restrictions
- IPI < 400: Amazon may impose storage limits and charge overage fees

**IPI Score Components:**


| Factor                 | Weight  | How to Improve                                        |
| ---------------------- | ------- | ----------------------------------------------------- |
| **Excess Inventory**   | Highest | Remove or liquidate slow-moving stock                 |
| **Sell-through Rate**  | High    | Increase sales velocity through PPC or promotions     |
| **Stranded Inventory** | Medium  | Fix listing issues causing inventory to go unsellable |
| **In-Stock Rate**      | Medium  | Restock bestsellers before they hit zero              |


**Check your IPI score:** Seller Central → Inventory → Inventory Performance Dashboard

---

## FBA Capacity Management (Post-2024 System)

Amazon moved from weekly restock limits to **monthly capacity limits** in 2024.
Capacity is assigned in cubic feet per product type (standard, oversize, apparel, etc.)

**Capacity allocation formula factors:**

- Your IPI score (primary driver)
- Historical sales velocity of your ASINs
- Available warehouse space in Amazon's network
- Reservations made via Capacity Manager

**Capacity Manager (Reservation System):**

- Request additional capacity in advance (up to 3 months ahead)
- Pay a reservation fee (refunded as credit if you use ≥100% of reserved capacity)
- Best for: Peak season pre-loading, new product launches requiring high initial stock

---

## Restock Quantity Calculation

**Step 1: Calculate daily sales velocity**
Daily velocity = Units sold in last 30 days ÷ 30

**Step 2: Determine restock lead time**
Lead time = Manufacturing days + Freight days + FBA check-in days
(Typical: 14-45 days for China to Amazon US)

**Step 3: Set safety stock**
Safety stock = (Max daily velocity − Average daily velocity) × Lead time days

**Step 4: Calculate reorder point**
Reorder point = (Average daily velocity × Lead time) + Safety stock

**Step 5: Calculate restock quantity**
Restock quantity = (Daily velocity × Target days of supply) − Current FBA inventory − Inbound units

**Target days of supply guidelines:**

- Standard products: 45-60 days
- Seasonal peak periods: 90-120 days
- Slow-moving products: 30-45 days maximum

---

## FBA Fee Structure (Key Fees to Manage)


| Fee Type                     | When Charged                                                        | How to Minimize                                          |
| ---------------------------- | ------------------------------------------------------------------- | -------------------------------------------------------- |
| **Fulfillment Fee**          | Per unit shipped                                                    | Optimize packaging to reduce dimensional weight          |
| **Monthly Storage Fee**      | Per cubic foot/month                                                | Keep inventory lean; liquidate excess                    |
| **Aged Inventory Surcharge** | 181-270 days: $0.50/unit; 271-365: $1.00/unit; 365+: $1.50/unit     | Set 150-day sell-through target as hard limit            |
| **Removal/Disposal Fee**     | Per unit removed                                                    | Use liquidations for slow stock vs. paying LTSF          |
| **Inbound Placement Fee**    | Per unit, based on how many fulfillment centers Amazon places stock | Ship to Amazon Optimized Placement (if lower total cost) |


---

## Aged Inventory Prevention Protocol

**At 90 days**: Flag any ASIN with >60 days of supply remaining at current velocity
**At 120 days**: Run a targeted promotion (5-10% price reduction) or Amazon Coupon
**At 150 days**: Create a removal order for slowest-moving units
**At 180 days**: Liquidate all remaining units before aged inventory surcharge kicks in

**Liquidation options (in order of preference):**

1. Amazon Outlet (discounted listing in Amazon's liquidation channel)
2. Amazon Liquidations program (Amazon buys at ~5-10% of recovery value)
3. Removal order to your warehouse → sell on other channels

---

## Peak Season Inventory Planning


| Peak Event                  | Prep Start | Stock Target    | Key Action              |
| --------------------------- | ---------- | --------------- | ----------------------- |
| Prime Day (July)            | May 1      | 90 days supply  | Submit inbound April 15 |
| Back to School (Aug)        | June 15    | 60 days supply  | FBA check-in by July 15 |
| Black Friday / Cyber Monday | September  | 120 days supply | FBA check-in by Oct 1   |
| Holiday Season (Dec)        | October    | 90 days supply  | FBA check-in by Nov 1   |


**FBA receiving lead times during peak:** Allow 2-3 weeks extra check-in time from October through December.

---

## Stranded Inventory Fix Protocol

Stranded inventory = Units in FBA that are not buyable due to listing issues.

**Common causes and fixes:**


| Cause                                            | Fix                                                 |
| ------------------------------------------------ | --------------------------------------------------- |
| Listing closed or deleted                        | Relist the product; re-associate FNSKU              |
| Price alert (price too high/low)                 | Update pricing within Amazon's allowed range        |
| Safety complaint                                 | Submit appeal with test reports and compliance docs |
| Listing suppression (missing required attribute) | Add missing attribute in Manage Inventory           |


**Check stranded inventory:** Seller Central → Inventory → Fix Stranded Inventory

---

## Inventory Health KPIs to Monitor Weekly


| KPI                         | Target               | Alert Threshold       |
| --------------------------- | -------------------- | --------------------- |
| IPI Score                   | ≥ 450                | < 400 (capacity risk) |
| In-Stock Rate (bestsellers) | > 95%                | < 85%                 |
| Excess Inventory %          | < 15% of total units | > 30%                 |
| Aged Inventory (>180 days)  | 0 units              | Any units at 150 days |
| Sell-through Rate           | > 7 (last 90 days)   | < 3 (flag for review) |
| Stranded Inventory          | 0 units              | Any                   |


