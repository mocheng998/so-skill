---
name: multi-location-order-router
description: "Design and implement a robust order lifecycle engine that manages multi-warehouse routing, split shipments, and backorder queues across complex fulfillment networks"
category: business-operations
risk: critical
source: curated
date_added: "2026-03-12"
tags: [OMS, order-management, split-orders, backorders, distributed-fulfillment, fulfillment-routing]
triggers: ["order management system", "OMS", "split orders", "backorder handling", "fulfillment routing", "distributed fulfillment", "order routing"]
tools: [claude-code, cursor, gemini-cli, copilot, codex-cli, kiro, opencode]
platforms: [shopify, woocommerce, bigcommerce, custom]
difficulty: advanced
---

# Build Multi-Location Order Management System

## Overview

An Order Management System (OMS) is the central "brain" of e-commerce operations. It manages the lifecycle of an order from the moment of payment until it reaches the customer's doorstep. A high-performance OMS must intelligently route orders to the optimal fulfillment location, manage inventory reservations across multiple warehouses, handle backorders without blocking the entire queue, and provide a tamper-proof audit trail for every status change.

## When to Use This Skill

- When scaling from a single warehouse to a distributed fulfillment network (Multiple 3PLs or own warehouses).
- When implementing "Ship from Store" or "BOPIS" (Buy Online, Pick Up In Store) strategies.
- When managing high-volume flash sales where thousands of orders compete for limited inventory.
- When you need to automate complex routing logic (e.g., "Route to Warehouse A unless shipping to West Coast, then route to Warehouse B").

## Core Instructions

### Step 1: Configure Multi-Location Inventory

#### Shopify Admin
1. Navigate to **Settings → Locations**.
2. Click **Add location** for each physical warehouse, retail store, or 3PL node.
3. In **Settings → Shipping and delivery**, under **Fulfillment priority**, drag locations to set the order in which Shopify should attempt to fulfill.
4. For each product, ensure **Track quantity** is enabled and stock levels are distributed across the relevant locations.

#### BigCommerce Admin
1. Go to **Inventory → Locations**.
2. Create locations for each fulfillment source.
3. Assign products to locations and set stock levels. BigCommerce will automatically route orders based on the "closest location with stock" principle or your custom priority list.

#### WooCommerce Admin
1. While basic WooCommerce is single-location, enable multi-location support using platform-native inventory extensions.
2. Define "Fulfillment Zones" and assign specific warehouses to each zone to minimize shipping distance and cost.

### Step 2: Implement Order Routing and State Logic (Custom/API)

For custom builds, use a formal state machine to prevent invalid transitions and ensure data integrity.

#### Order State Machine
```typescript
type OrderStatus = 'pending' | 'paid' | 'awaiting_fulfillment' | 'partially_fulfilled' | 'fulfilled' | 'cancelled';

const VALID_TRANSITIONS: Record<OrderStatus, OrderStatus[]> = {
  pending: ['paid', 'cancelled'],
  paid: ['awaiting_fulfillment', 'cancelled'],
  awaiting_fulfillment: ['partially_fulfilled', 'fulfilled', 'cancelled'],
  partially_fulfilled: ['fulfilled', 'cancelled'],
  fulfilled: [],
  cancelled: []
};

async function transitionOrder(orderId: string, newStatus: OrderStatus, actor: string): Promise<void> {
  const order = await db.orders.findById(orderId);
  if (!VALID_TRANSITIONS[order.status].includes(newStatus)) {
    throw new Error(`Invalid state transition: ${order.status} to ${newStatus}`);
  }

  await db.transaction(async tx => {
    await tx.orders.update(orderId, { status: newStatus });
    // Mandatory Audit Trail Entry
    await tx.order_events.insert({
      order_id: orderId,
      old_status: order.status,
      new_status: newStatus,
      actor: actor,
      created_at: new Date()
    });
  });
}
```

#### Inventory Routing Logic
```typescript
async function routeOrder(orderId: string): Promise<void> {
  const lines = await db.order_lines.findByOrderId(orderId);
  
  for (const line of lines) {
    // 1. Find optimal location using 'Nearest Neighbor' + 'In Stock' logic
    const bestLocation = await db.inventory.findOptimalSource(line.sku, line.quantity);
    
    if (bestLocation) {
      await db.fulfillment_requests.insert({
        order_id: orderId,
        location_id: bestLocation.id,
        sku: line.sku,
        quantity: line.quantity
      });
    } else {
      // 2. Fallback to Backorder Queue (FIFO)
      await db.backorders.insert({ order_id: orderId, sku: line.sku, status: 'pending' });
    }
  }
}
```

## Decision Criteria & Deep Analysis

### Order Cancellation Cascade
Cancelling an order is not just a status change. It requires a coordinated "cascade" of actions:
1. **Inventory Release**: Immediately move "Reserved" inventory back to "Available" for that SKU at the specific location.
2. **Fulfillment Void**: If a request was sent to a 3PL or warehouse WMS (but not yet shipped), send a `VOID_SHIPMENT` API call or EDI 945 message.
3. **Financial Reversal**: Trigger a `refund` or `void_authorization` on the payment gateway (Stripe/PayPal).
4. **Communication**: Notify the customer and updating the "Order Timeline" with the reason (e.g., "Customer requested," "Fraud detected").

### High-Volume Concurrency Considerations
When thousands of orders hit the same SKU simultaneously:
- **Lock Contention**: Standard `UPDATE inventory SET qty = qty - 1` can lead to deadlocks or slow performance.
- **Solution**: Use **Pessimistic Locking** (`SELECT ... FOR UPDATE`) in short transactions, or a distributed locking mechanism like **Redis Redlock** to ensure inventory is never over-allocated.
- **Buffer Stock**: Maintain a "Buffer" of 5-10% for high-velocity SKUs to account for sync lag between the OMS and the storefront.

### Backorder Fulfillment (FIFO)
Implement a First-In-First-Out (FIFO) queue for backorders. When new inventory is received (via a Purchase Order or Return):
- The system should automatically scan the `backorders` table.
- Allocate the new stock to the oldest pending order first.
- Re-trigger the fulfillment routing logic for that specific order.

## Best Practices

- **Split Shipment Communication**: If an order is split across two warehouses, send two distinct tracking emails. The first should clearly state "Part of your order is on the way," and list exactly which items are in that box.
- **24-Hour Stuck Alert**: Set an automated monitor for orders in `awaiting_fulfillment` status for >24 hours. These often indicate a stockout that wasn't properly synced or a 3PL API failure.
- **Idempotent Ingestion**: Ensure the order ingestion endpoint can handle duplicate webhooks from the storefront using the `storefront_order_id` as a unique idempotency key.
- **Audit Everything**: Every manual note or system-automated change must be logged. This is critical for resolving customer disputes and accounting audits.

## Common Pitfalls & Edge Cases

| Problem | Solution |
|---------|----------|
| **"Ghost" Inventory** | Inventory shows in stock in the OMS but isn't on the shelf. Trigger an immediate "Cycle Count" request to the warehouse when a "Short Pick" occurs. |
| **Address Sync Failure** | 3PLs often have stricter address validation than storefronts. Implement a "Fix Required" status in the OMS for orders that fail carrier validation. |
| **Partial Refunds** | If one item in a multi-item order is cancelled, ensure the tax and shipping portions are recalculated correctly before issuing the refund. |
| **Stale 3PL Status** | Don't rely solely on webhooks from 3PLs. Implement a "Heartbeat" task that polls for status updates on open fulfillments every 4 hours. |
