# Dispute API (Verified)

Source: `https://developers.cjdropshipping.cn/en/api/api2/api/dispute.html`

This reference follows the currently documented dispute interfaces and focuses on accurate request details. Response fields are intentionally omitted.

## 1. Dispute APIs

### 1.1 Select the list of disputed products
- **Method**: `GET`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/disputes/disputeProducts`
- **Purpose**: List order items eligible for dispute.
- **Query parameters**:
  - `orderId` `string` required, length `100`: CJ order ID.

### 1.2 Confirm the dispute
- **Method**: `POST`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/disputes/disputeConfirmInfo`
- **Purpose**: Confirm amount/item scope before creating a dispute.
- **Headers**:
  - `CJ-Access-Token` required.
  - `Content-Type: application/json` recommended for implementation.
- **JSON body parameters**:
  - `orderId` `string` required, length `100`: CJ order ID.
  - `productInfoList` `object[]` required: product information list.
    - `lineItemId` `string` optional: line item ID.
    - `quantity` `integer` required: quantity.
    - `price` `BigDecimal` required, precision `(18,2)`: price in USD.

### 1.3 Create dispute
- **Method**: `POST`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/disputes/create`
- **Purpose**: Submit a dispute.
- **Headers**:
  - `CJ-Access-Token` required.
  - `Content-Type: application/json` recommended for implementation.
- **JSON body parameters**:
  - `businessDisputeId` `string` required, length `100`: customer business ID. CJ notes it must be unique.
  - `orderId` `string` required, length `100`: CJ order ID.
  - `disputeReasonId` `integer` required, length `10`: dispute reason ID.
  - `expectType` `integer` required, length `20`: expected result.
    - `1`: refund
    - `2`: reissue
  - `refundType` `integer` required, length `20`: refund type.
    - `1`: balance
    - `2`: platform
  - `messageText` `string` required, length `500`: text message / dispute description.
  - `imageUrl` `string[]` optional, length `200`: evidence image URLs.
  - `videoUrl` `string[]` optional, length `200`: evidence video URLs.
  - `productInfoList` `object[]` required: disputed product list.
    - `price` `BigDecimal` required, precision `(18,2)`: price in USD.
    - `lineItemId` `string` optional, length `100`: line item ID.
    - `quantity` `integer` required, length `10`: disputed quantity.

### 1.4 Cancel dispute
- **Method**: `POST`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/disputes/cancel`
- **Purpose**: Cancel an existing dispute.
- **Headers**:
  - `CJ-Access-Token` required.
  - `Content-Type: application/json` recommended for implementation.
- **JSON body parameters**:
  - `orderId` `string` required, length `100`: CJ order ID.
  - `disputeId` `string` required, length `100`: CJ dispute ID.

### 1.5 Query the list of disputes
- **Method**: `GET`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/disputes/getDisputeList`
- **Purpose**: Query disputes with filters and pagination.
- **Query parameters**:
  - `orderId` `string` optional, length `100`: CJ order ID.
  - `disputeId` `integer` optional, length `10`: dispute ID.
  - `orderNumber` `string` optional, length `100`: customer order number.
  - `pageNum` `integer` optional, length `10`, default `1`: page number.
  - `pageSize` `integer` optional, length `10`, default `10`: page size.

### 1.6 Get dispute detail
- **Method**: `GET`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/disputes/getDisputeDetail`
- **Purpose**: Query a single dispute in detail.
- **Query parameters**:
  - `disputeId` `integer` optional, length `10`: dispute ID.
