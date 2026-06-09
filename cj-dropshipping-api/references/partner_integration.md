# CJ Dropshipping Partner Integration Guide (ERP/Platform)

This guide is specifically for Partner/ERP platforms that integrate with CJ Dropshipping for product listing, shop management, and order synchronization.

## 1. Authorization Process

### 1.1 Partner Redirect Flow
Partners should redirect users to the CJ authorization page:
`https://www.cjdropshipping.com/mine/authorize/erpAuthorization?clientId={CLIENT_ID}&parnterName={NAME}&clientAccountId={ID}&clientAccountName={NAME}&clientRedirectUrl={URL}`

### 1.2 Get Access Token
**Endpoint:** `POST /authentication/getAccessToken`

**Body:**
```json
{
  "apiKey": "REQUIRED_API_KEY_FROM_CALLBACK"
}
```

**Response Data (`data`):**
- `accessToken`: The token for `CJ-Access-Token` header.
- `accessTokenExpiryDate`: Expiry timestamp.
- `refreshToken`: Used to refresh access token.
- `openId`: User's unique identifier.

---

## 2. Product Listing API (刊登)

### 2.1 Batch Listing (listedByPids)
**Endpoint:** `POST /product/listed/listedByPids`

**Description:** Lists products from CJ to a third-party shop (e.g., Shopify).

**Request Body:**
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `shopIds` | Set<String> | Yes | Target shop IDs. |
| `productIds` | List<String> | Yes | CJ product IDs to list. |
| `formula` | Object | Yes | Price calculation formula. |
| `formula.formulaType` | Integer | No | 0: Fixed, 1: Add, 2: Percentage, 3: Recommended. |
| `formula.formulaNumber` | BigDecimal | No | Value for the formula. |
| `formula.shippingFrom` | String | Yes | Origin (e.g., "CN"). |
| `formula.shippingTo` | String | Yes | Destination (e.g., "US"). |
| `formula.isLogistics` | Integer | Yes | 1: Include logistics fee in price, 0: Exclude. |

### 2.2 Query Listing Status
**Endpoint:** `POST /product/listed/queryListedStatus`

**Request Body:**
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `batchIds` | List<String> | Yes | Batch IDs returned by `listedByPids`. |

### 2.3 Get Platform Category Tree
**Endpoint:** `POST /product/listed/getPlatformCategoryTree`

**Description:** Retrieves collections/categories from the third-party shop.
- For Shopify: `categoryLevel 0` = Custom Collections; `categoryLevel 1` = Smart Collections.

---

## 3. Shop & Settings API

### 3.1 Get Authorized Shops
**Endpoint:** `GET /shop/getShops`

**Success Code:** `0`

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
      "platformLogoUrl": "...",
      "currencyCode": "USD"
    }
  ]
}
```

### 3.2 Query Shop Vendors
**Endpoint:** `POST /product/listed/queryVendors`

**Request Body:** `{"shopId": "..."}`

---

## 4. Logistics & Delivery

### 4.1 Query Delivery Profiles (Shopify)
**Endpoint:** `POST /product/listed/queryDeliveryProfiles`

**Description:** Retrieves Shopify Delivery Profiles to be assigned during listing.

### 4.2 Get Receiver Country Info
**Endpoint:** `POST /product/listed/getReceiverCountryInfo`

---

## 5. Implementation Notes

- **Success Codes:** Authentication and standard V2.0 APIs use `200`. Listing and Shop APIs (Partner system) use `0`.
