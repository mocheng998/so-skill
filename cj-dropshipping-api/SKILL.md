---
name: cj-dropshipping-api
description: >
  Use when integrating CJ Dropshipping API V2.0 — products, orders (Shopping API), logistics, webhooks,
  Shopify delivery profiles. Business calls are REST against `developers.cjdropshipping.com`; use `accio-mcp-cli`
  only to obtain OAuth tokens (`start_cj_auth`, `get_cj_access_token`), not for product or order APIs.
tool_triggers:
  - tool: bash
    args:
      command: /accio-mcp-cli\s+call\s+(?:start_cj_auth|get_cj_access_token)\b/i
---

# CJ Dropshipping API V2.0

**accio-mcp-cli** is used **only for CJ OAuth and reading the stored token** (`start_cj_auth`, `get_cj_access_token`). Everything else — product search, orders, logistics, webhooks, partner listing — follows the **REST API** in sections 2 onward: call `https://developers.cjdropshipping.com/api2.0/v1/...` with header **`CJ-Access-Token`** from `get_cj_access_token`.

For CLI flags such as `--port`, `--raw`, or `--refresh` on those two auth calls, see the **accio-mcp-cli** skill.

## 1. Authentication (accio-mcp-cli only)

Run OAuth once, then read the token before any REST request.

```bash
accio-mcp-cli call start_cj_auth
accio-mcp-cli call get_cj_access_token
```

| Step | Command |
|------|---------|
| Start OAuth (user completes link in browser) | `accio-mcp-cli call start_cj_auth` |
| Read stored token pair | `accio-mcp-cli call get_cj_access_token` |

Use the returned `accessToken` as **`CJ-Access-Token`** on all REST calls below. Add `--raw` on `get_cj_access_token` if you need the full gateway JSON.

**Example payload shape** (fields may vary; use `--raw` for the exact MCP result):

```json
{
  "provider": "cj",
  "accessToken": "...",
  "accessTokenExpiryDate": "...",
  "refreshToken": "...",
  "refreshTokenExpiryDate": "..."
}
```

## 2. Product Management & Listing

All product endpoints require:
- `CJ-Access-Token: YOUR_ACCESS_TOKEN`

### 2.1 Get Category List
**Endpoint:** `GET https://developers.cjdropshipping.com/api2.0/v1/product/getCategory`

Returns the CJ category tree.

### 2.2 Get Product List (V2)
**Endpoint:** `GET https://developers.cjdropshipping.com/api2.0/v1/product/listV2`

Primary product search/list endpoint for new integrations.

**Query Parameters:**
- `page`: Page number, default `1`, min `1`, max `1000`
- `size`: Page size, default `20`, min `1`, max `100`
- `keyWord`: Search keyword for product name or SKU
- `categoryId`: Category ID filter
- `countryCode`: Only return products with inventory in the specified country
- `minPrice`: Minimum price
- `maxPrice`: Maximum price
- `features`: Optional expansion parameter for product/category details

### 2.3 Get Product Detail
**Endpoint:** `GET https://developers.cjdropshipping.com/api2.0/v1/product/query`

Get a single product with variants.

**Query Parameters:**
- `pid`: Product ID. Use one of `pid`, `productSku`, or `variantSku`
- `productSku`: Product SKU. Use one of `pid`, `productSku`, or `variantSku`
- `variantSku`: Variant SKU. Use one of `pid`, `productSku`, or `variantSku`
- `countryCode`: Optional inventory country filter
- `features`: Optional. Supported documented values:
  - `enable_combine`
  - `enable_video`
  - `enable_inventory`

**Important note:** do not use undocumented query parameters such as `productId` or `variantId` for this endpoint.

### 2.4 Get All Variants
**Endpoint:** `GET https://developers.cjdropshipping.com/api2.0/v1/product/variant/query`

**Query Parameters:**
- `pid`: Use one of `pid`, `productSku`, or `variantSku`
- `productSku`: Use one of `pid`, `productSku`, or `variantSku`
- `variantSku`: Use one of `pid`, `productSku`, or `variantSku`
- `countryCode`: Optional inventory country filter

### 2.5 Get Variant Detail
**Endpoint:** `GET https://developers.cjdropshipping.com/api2.0/v1/product/variant/queryByVid`

**Query Parameters:**
- `vid`: Variant ID
- `features`: Optional. Use `enable_inventory` to include inventory details

### 2.6 Get Product Stock by Variant ID
**Endpoint:** `GET https://developers.cjdropshipping.com/api2.0/v1/product/stock/queryByVid`

**Query Parameters:**
- `vid`: Variant ID

### 2.7 Get Product Stock by SKU
**Endpoint:** `GET https://developers.cjdropshipping.com/api2.0/v1/product/stock/queryBySku`

**Query Parameters:**
- `sku`: SKU or SPU

### 2.8 Get Product Stock by Product ID
**Endpoint:** `GET https://developers.cjdropshipping.com/api2.0/v1/product/stock/getInventoryByPid`

**Query Parameters:**
- `pid`: Product ID

### 2.9 Add to My Products
**Endpoint:** `POST https://developers.cjdropshipping.com/api2.0/v1/product/addToMyProduct`

**JSON Body:**
```json
{
  "productId": "CJ_PRODUCT_ID"
}
```

### 2.10 Query My Products
**Endpoint:** `GET https://developers.cjdropshipping.com/api2.0/v1/product/myProduct/query`

**Query Parameters:**
- `keyword`: SKU/SPU/product name
- `categoryId`: Category filter
- `startAt`: Start time
- `endAt`: End time
- `isListed`: Listing status filter
- `visiable`: Visibility filter
- `hasPacked`: Packing filter
- `hasVirPacked`: Virtual packing filter

### 2.11 Product Reviews
**Endpoint:** `GET https://developers.cjdropshipping.com/api2.0/v1/product/productComments`

**Query Parameters:**
- `pid`: Product ID
- `score`: Optional score filter
- `pageNum`: Page number, default `1`
- `pageSize`: Page size, default `20`

### 2.12 Batch Listing (刊登)
**Endpoint:** `POST https://developers.cjdropshipping.com/api2.0/v1/product/listed/listedByPids`

Lists CJ products to a third-party store (e.g., Shopify).

**Headers:**
- `CJ-Access-Token: USER_TOKEN`

**Body:**
```json
{
  "shopIds": ["..."],
  "productIds": ["..."],
  "formula": {
    "formulaType": 1,
    "formulaNumber": 15,
    "shippingFrom": "CN",
    "shippingTo": "US",
    "isLogistics": 1
  },
  "templateShopCategoryVOList": [
    {
      "shopId": "...",
      "deliveryProfileId": "..."
    }
  ]
}
```
*Note: For Shopify, `deliveryProfileId` is often mandatory to avoid 7001001 errors.*

### 2.13 Query Platform Category Tree
**Endpoint:** `POST https://developers.cjdropshipping.com/api2.0/v1/product/listed/getPlatformCategoryTree`

Gets categories/collections from the target platform (e.g., Shopify Collections).

### 2.14 Query Vendors
**Endpoint:** `POST https://developers.cjdropshipping.com/api2.0/v1/product/listed/queryVendors`

Gets the list of available vendors for a specific shop.

### 2.15 Get CJ Default Delivery Profile
**Endpoint:** `POST https://developers.cjdropshipping.com/api2.0/v1/product/listed/getCjDefaultDeliveryProfile`

Returns a default shipping profile template that can be used as a base for `createDeliveryProfile`.

### 2.16 Create Delivery Profile
**Endpoint:** `POST https://developers.cjdropshipping.com/api2.0/v1/product/listed/createDeliveryProfile`

Creates a new shipping profile in the target Shopify store. Requires a list of `locationIds` and `zones` (including countries and provinces).

### 2.17 Update Delivery Profile
**Endpoint:** `POST https://developers.cjdropshipping.com/api2.0/v1/product/listed/updateDeliveryProfile`

Updates an existing shipping profile.

### 2.18 Remove Delivery Profile
**Endpoint:** `POST https://developers.cjdropshipping.com/api2.0/v1/product/listed/removeDeliveryProfile`

Deletes a shipping profile.

### 2.19 Query Shop Locations
**Endpoint:** `POST https://developers.cjdropshipping.com/api2.0/v1/shop/location/queryList`

Lists all fulfillment locations for a shop. Essential for identifying the "CJ Dropshipping" location ID (where `fromCj: true`).

### 2.20 Query Countries & Provinces
**Endpoint:** `POST https://developers.cjdropshipping.com/api2.0/v1/shop/property/queryCountries`

Returns a list of supported countries and their provinces/states. Mandatory for constructing the `zones` object in delivery profiles.

## 3. Order Processing (Shopping)

### 3.1 Create Order V2
**Endpoint:** `POST https://developers.cjdropshipping.com/api2.0/v1/shopping/order/createOrderV2`

**Headers:**
- `CJ-Access-Token: YOUR_ACCESS_TOKEN`

**Body:**
```json
{
  "orderNumber": "YOUR_ORDER_ID_123",
  "shippingZip": "10001",
  "shippingCountryCode": "US",
  "shippingCountry": "United States",
  "shippingProvince": "New York",
  "shippingCity": "New York",
  "shippingAddress": "123 Main St",
  "shippingCustomerName": "John Doe",
  "shippingPhone": "1234567890",
  "remark": "Dropshipping order",
  "fromCountryCode": "CN",
  "logisticName": "CJPacket Sensitive",
  "payType": "1", 
  "products": [
    {
      "vid": "CJ_VARIANT_ID",
      "quantity": 1
    }
  ]
}
```
*`payType`: 1 (URL payment), 2 (Balance payment), 3 (Create only)*

### 3.2 Get Order Details / List
**Endpoint:** `GET https://developers.cjdropshipping.com/api2.0/v1/shopping/order/list`
*(Note: Use `list` to search or `queryById` for specific details depending on needs, check documentation for exact path if `list` is not standard, traditionally `list` or `get` with params)*

**Correct Endpoint for List:** `GET https://developers.cjdropshipping.com/api2.0/v1/shopping/order/list` (Standard V2 pattern, verify if `list` exists or use `get` with params)
*Actually, strictly checked docs say:* `GET https://developers.cjdropshipping.com/api2.0/v1/shopping/order/list` allows filtering by `orderNumber`, `cjOrderCode`, `status`, etc.

**Query Parameters:**
- `page`: 1
- `size`: 20
- `orderNumber`: Your order ID
- `cjOrderCode`: CJ Order ID
- `status`: Order status (e.g., '10' for Paid)

### 3.3 Confirm Order (Payment)
If `payType=3` was used, confirm/pay using:
**Endpoint:** `POST https://developers.cjdropshipping.com/api2.0/v1/shopping/pay/payBalance`

**Body:**
```json
{
  "orderIdList": ["CJ_ORDER_ID_1", "CJ_ORDER_ID_2"]
}
```

## 4. Logistics

### 4.1 Freight Calculator
**Endpoint:** `POST https://developers.cjdropshipping.com/api2.0/v1/logistic/freightCalculate`

**Body:**
```json
{
  "startCountryCode": "CN",
  "countryCode": "US",
  "products": [
    {
      "vid": "CJ_VARIANT_ID",
      "quantity": 1
    }
  ]
}
```

### 4.2 Track Info
**Endpoint:** `GET https://developers.cjdropshipping.com/api2.0/v1/logistic/trackInfo`

**Query Parameters:**
- `trackNumber`: Tracking number (can be repeated for batch: `?trackNumber=A&trackNumber=B`)

### 4.3 Query Delivery Profile (Partner)
**Endpoint:** `POST https://developers.cjdropshipping.com/api2.0/v1/product/listed/queryDeliveryProfiles`

Gets Shopify Delivery Profiles to bind during listing.

### 4.4 Query Receiver Country Info
**Endpoint:** `POST https://developers.cjdropshipping.com/api2.0/v1/product/listed/getReceiverCountryInfo`

## 5. Webhooks

Configure webhooks to receive real-time updates.

**Endpoint:** `POST https://developers.cjdropshipping.com/api2.0/v1/webhook/set`

**Body:**
```json
{
  "product": { "type": "ENABLE", "callbackUrls": ["https://your-domain.com/webhook/product"] },
  "stock": { "type": "ENABLE", "callbackUrls": ["https://your-domain.com/webhook/stock"] },
  "order": { "type": "ENABLE", "callbackUrls": ["https://your-domain.com/webhook/order"] },
  "logistics": { "type": "ENABLE", "callbackUrls": ["https://your-domain.com/webhook/logistics"] }
}
```

**Events:**
- `product`: Price/Inventory changes? (Check specific payload types in docs)
- `stock`: Inventory updates
- `order`: Status changes (Paid, Shipped, Completed)
- `logistics`: Tracking updates

## 6. Settings

### 6.1 Get Account Settings
**Endpoint:** `GET https://developers.cjdropshipping.com/api2.0/v1/setting/get`

Returns account info, API quotas, and current webhook configurations.

### 6.2 Set Webhook Callback
**Endpoint:** `POST https://developers.cjdropshipping.com/api2.0/v1/setting/setCallback`

**Body:**
```json
{
  "product": {"type": "ENABLE", "urls": ["..."]},
  "stock": {"type": "ENABLE", "urls": ["..."]},
  "order": {"type": "ENABLE", "urls": ["..."]},
  "logistic": {"type": "ENABLE", "urls": ["..."]}
}
```

## 7. Shop API (Partner Mode)

These endpoints manage store connections and settings.

### 7.1 Query Shop List
**Endpoint:** `GET /shop/getShops`

**Description:** Returns the list of shops authorized by the user. Success code is `0`.
**Note:** Relative path; base URL must be confirmed with the partner system.

---

## 8. API Reference (Detailed)

Detailed documentation for Partner/ERP integration is available in:
- [Partner Integration Guide (ERP/Platform)](references/partner_integration.md)

This section provides a summary of the Partner/Listing API endpoints.

### 8.1 Batch Product Listing (listedByPids)
**Endpoint:** `POST /product/listed/listedByPids`

**Request Body (JSON):**
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `shopIds` | Set<String> | Yes | Shop IDs to list on (e.g., `["shop_id"]`). |
| `productIds` | List<String> | Yes | CJ product IDs to list. |
| `formula` | Object | Yes | Listing price formula. |
| `formula.formulaType` | Integer | Yes | 0-Fixed, 1-Add, 2-Percentage, 3-Recommended. |
| `formula.formulaNumber` | BigDecimal | Yes | Multiplier/Value for the formula (required if type is not 3). |
| `formula.shippingFrom` | String | Yes | Origin country code (e.g., `"CN"`). |
| `formula.shippingFromName` | String | Yes | Origin country name (e.g., `"China"`). |
| `formula.shippingTo` | String | Yes | Destination country code (e.g., `"US"`). |
| `formula.shippingToName` | String | Yes | Destination country name (e.g., `"United States"`). |
| `formula.logisticsMaxDay` | Integer | Yes | Max delivery days (e.g., `30`). |
| `formula.logisticsMaxPrice` | BigDecimal | Yes | Max logistics cost (e.g., `100.00`). |
| `formula.logisticsType` | Integer | Yes | Logistics type (e.g., `0`). |
| `formula.isLogistics` | Integer | Yes | 1: Enable logistics fee, 0: Disable. |
| `templateShopCategoryVOList` | List<Object> | No | Required for Shopify stores. |
| `templateShopCategoryVOList[].shopId` | String | Yes | Shop ID. |
| `templateShopCategoryVOList[].deliveryProfileId` | String | Yes | Shopify Delivery Profile ID. |

**Example Request:**
```json
{
  "shopIds": ["2603221653513529700"],
  "productIds": ["1772614144538193920"],
  "formula": {
    "formulaType": 3,
    "shippingFrom": "CN",
    "shippingFromName": "China",
    "shippingTo": "US",
    "shippingToName": "United States",
    "logisticsMaxDay": 30,
    "logisticsMaxPrice": 100.00,
    "logisticsType": 0,
    "isLogistics": 1
  },
  "templateShopCategoryVOList": [
    {
      "shopId": "2603221653513529700",
      "deliveryProfileId": "112235774194"
    }
  ]
}
```

### 8.2 Query Platform Category Tree
**Endpoint:** `POST /product/listed/getPlatformCategoryTree`

**Request Body (JSON):**
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `shopId` | String | Yes | Target shop ID. |
| `countryCode` | String | No | Filter by country site. |
| `pageNum` | Integer | No | Default 1. |

**Response Data (`data` field):**
Contains a `categoryVOS` list. For Shopify:
- `categoryLevel 0`: Custom Collections.
- `categoryLevel 1`: Smart Collections.

### 8.3 Query Shop Delivery Profile
**Endpoint:** `POST /product/listed/queryDeliveryProfiles`

**Request Body (JSON):**
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `shopId` | String | No | Target shop ID. |
| `forceRefresh` | Boolean | No | Force cache refresh. |

### 8.4 Get Access Token (Partner Mode)
**Endpoint:** `POST /authentication/getAccessToken`

**Success Response (`data` field):**
- `accessToken`: The token for `CJ-Access-Token` header.
- `accessTokenExpiryDate`: Token expiry timestamp.
- `refreshToken`: Token used to refresh the session.
- `openId`: User's unique identifier in the platform.

### 8.5 Shop API - Get Shops
**Endpoint:** `GET /shop/getShops`

**Response Example:**
```json
{
  "success": true,
  "code": 0,
  "data": [
    {
      "shopId": "...",
      "shopName": "...",
      "platformName": "Shopify",
      "currencyCode": "USD"
    }
  ]
}
```

---

## Common Error Codes
- `200`: Success
- `1600100`: Parameter error
- `1601000`: User not found
- `500`: System error (Retry later)

## 9. Troubleshooting & Common Errors

### 9.1 Error Code 400: Wrong request parameter
- **Cause**: Missing mandatory fields in `formula` (e.g., `shippingFrom`, `shippingTo`) or missing `templateShopCategoryVOList` for Shopify stores.
- **Fix**: Ensure all required fields are present. For Shopify, provide a valid `deliveryProfileId`.

### 9.2 Error Code 7001001: Template lacks Delivery Profile
- **Cause**: Shopify store requires a Delivery Profile assignment for products, but `deliveryProfileId` was not passed.
- **Fix**: Query available profiles using `/product/listed/queryDeliveryProfiles` and pass the ID in `templateShopCategoryVOList`.

### 9.3 Error Code 7001003: Delivery Profile does not include the location of application creation
- **Cause**: The Shopify Delivery Profile does not have the "CJ Dropshipping" location enabled.
- **Automated Fix (API)**:
    1. Query all locations via `/api/shop/location/queryList`. Identify the one where `fromCj: true`.
    2. Create a new Delivery Profile via `/api/product/listed/createDeliveryProfile` or update an existing one to include this location ID in `locationIds`.
    3. Ensure for countries with states (e.g., US), all provinces are explicitly provided in the `zones.countries` array.
- **Manual Fix**: Ask the user to go to **Shopify Admin > Settings > Shipping and delivery**, edit the profile, and add the "CJ Dropshipping" location to it.

## 10. Best Practices
1. **Check `deliveryProfileOpen`**: When querying shops via `getShops`, if `deliveryProfileOpen=1`, you MUST provide a `deliveryProfileId` during listing.
2. **Cache Access Tokens**: Do not request a new token for every call. Store it until near expiry.
3. **Handle Rate Limits**: Respect the QPS limits returned in the `setting/get` endpoint.
4. **Use Webhooks**: Prefer webhooks over polling for order status updates.
5. **Log Request IDs**: Log the `requestId` from responses for debugging with CJ support.

## 11. Shopify Shipping Profile Automation Workflow

When listing products on Shopify, follow this automated workflow to handle shipping profiles:

1. **Check Requirement**: Get the shop list via `/shop/getShops`. If the target shop has `deliveryProfileOpen: 1`, proceed to manage profiles.
2. **Identify CJ Location**: Call `/shop/location/queryList`. Find the location where `fromCj: true`. Save this `id` (this is the CJ app location ID).
3. **Query Provinces (If needed)**: If shipping to the US or other countries with mandatory provinces, call `/shop/property/queryCountries` to get the list of province codes.
4. **Setup Delivery Profile**:
   - Call `/product/listed/queryDeliveryProfiles` to see existing profiles.
   - If a valid profile exists and contains the CJ location, use its ID.
   - Otherwise, call `/product/listed/createDeliveryProfile` using the CJ location ID and the required country/province zones.
5. **Execute Listing**: Pass the resulting `deliveryProfileId` inside `templateShopCategoryVOList` when calling `/product/listed/listedByPids`.
