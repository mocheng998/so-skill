# Shopping API (Verified)

Source: `https://developers.cjdropshipping.cn/en/api/api2/api/shopping.html`

This reference keeps the current/newer shopping interfaces and omits older superseded ones where the official Shopping page provides a newer equivalent. Response fields are intentionally omitted; request parameters are kept detailed.

## 1. Order APIs

### 1.1 Create Order V3
- **Method**: `POST`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/shopping/order/createOrderV3`
- **Purpose**: Create a CJ order using the newer documented order-creation endpoint.
- **Headers**:
  - `CJ-Access-Token` required.
  - `platformToken` optional. CJ documents that it is obtained the same way as `CJ-Access-Token`; if not required, it may be empty.
  - `Content-Type: application/json` required.
- **JSON body parameters**:
  - `orderNumber` `string` required, length `50`: unique partner order identifier.
  - `shippingZip` `string` optional, length `20`: destination ZIP/postal code.
  - `shippingCountryCode` `string` required, length `20`: two-letter destination country code.
  - `shippingCountry` `string` required, length `50`: destination country name.
  - `shippingProvince` `string` required, length `50`: destination province/state.
  - `shippingCity` `string` required, length `50`: destination city.
  - `shippingCounty` `string` optional, length `50`: destination county/district.
  - `shippingPhone` `string` optional, length `20`: destination phone number.
  - `shippingCustomerName` `string` required, length `50`: recipient name.
  - `shippingAddress` `string` required, length `200`: destination address line 1.
  - `shippingAddress2` `string` optional, length `200`: destination address line 2.
  - `houseNumber` `string` optional, length `20`: house number.
  - `email` `string` optional, length `50`: recipient email.
  - `taxId` `string` optional, length `20`: tax ID.
  - `remark` `string` optional, length `500`: order remark.
  - `consigneeID` `string` optional, length `20`: consignee ID.
  - `shopAmount` `BigDecimal` optional, length `20`: order amount.
  - `logisticName` `string` required, length `50`: logistics name. CJ points to freight-calculation APIs for valid values.
  - `fromCountryCode` `string` required, length `20`: two-letter origin country code.
  - `platform` `string` optional, length `20`: platform name. If omitted, CJ uses default platform `Api`.
  - `iossType` `int` optional, length `20`: IOSS mode.
    - `1`: no IOSS
    - `2`: declare with your own IOSS
    - `3`: declare with CJ's IOSS
  - `iossNumber` `string` optional, length `10`: IOSS number. If `iossType=3`, CJ documents fixed value `CJ-IOSS`.
  - `shopLogisticsType` `int` optional, length `20`, default `2`: shipping mode.
    - `1`: platform logistics, `storageId` specified by you
    - `2`: seller logistics
    - `3`: platform logistics, `storageId` specified by CJ
  - `storageId` `string` optional, length `40`: CJ warehouse ID. Valid when `shopLogisticsType=1`.
  - `products` `object[]` required, length `20`: order item list.
    - `vid` `string` conditional, length `50`: CJ variant ID. `vid` and `sku` cannot both be null. If non-CJ SKU submission permission is enabled, `vid` is required.
    - `sku` `string` conditional, length `50`: CJ variant SKU. Used for lookup when `vid` is absent. If both `vid` and `sku` are provided, they must map to the same variant.
    - `quantity` `int` required, length `50`: ordered quantity.
    - `unitPrice` `BigDecimal` optional, length `20`: item pricing.
    - `storeLineItemId` `string` optional, length `125`: your store order lineItem ID.
    - `podProperties` `string` optional, length `500`: POD customization info. CJ documents two formats:
      - POD 2.0 example: `[{"areaName":"LogoArea","links":["..."],"type":"1"}]`
      - POD 3.0 example: `[{"links":["Production image URL"],"effectImgs":["Rendering image URL"]}]`
- **Notes**:
  - `createOrderV2` is intentionally omitted because `createOrderV3` is the newer same-purpose interface on the official page.
  - `shopLogisticsType` and `storageId` are documented as added/launched on `2025-11-18`.

### 1.2 Add Cart
- **Method**: `POST`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/shopping/order/addCart`
- **Purpose**: Add one or more CJ orders into cart/confirmation flow.
- **Headers**:
  - `CJ-Access-Token` required.
  - `Content-Type: application/json` required.
- **JSON body parameters**:
  - `cjOrderIdList` `string[]` required, length `200`: CJ order ID list.

### 1.3 Add Cart Confirm
- **Method**: `POST`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/shopping/order/addCartConfirm`
- **Purpose**: Confirm cart items after add-to-cart.
- **Headers**:
  - `CJ-Access-Token` required.
  - `Content-Type: application/json` required.
- **JSON body parameters**:
  - `cjOrderIdList` `string[]` required, length `200`: CJ order ID list to confirm.

### 1.4 Save Generate Parent Order
- **Method**: `POST`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/shopping/order/saveGenerateParentOrder`
- **Purpose**: Save and generate the parent/shipment order in the shopping flow.
- **Headers**:
  - `CJ-Access-Token` required.
  - `Content-Type: application/json` required.
- **JSON body parameters**:
  - `shipmentOrderId` `string` required, length `200`: shipment order ID.

### 1.5 List Orders
- **Method**: `GET`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/shopping/order/list`
- **Purpose**: Query a paginated order list.
- **Query parameters**:
  - `pageNum` `int` optional, length `20`, default `1`: page number.
  - `pageSize` `int` optional, length `20`, default `20`: page size.
  - `orderIds` `string[]` optional, length `100`: order ID list filter.
  - `shipmentOrderId` `string` optional, length `100`: shipment order ID filter.
  - `status` `string` optional, length `200`: order status filter. Documented values: `CREATED`, `IN_CART`, `UNPAID`, `UNSHIPPED`, `SHIPPED`, `DELIVERED`, `CANCELLED`, `OTHER`.
- **Notes**:
  - The page notes default status example as `CANCELLED`; keep explicit filters rather than assuming a server default in code.

### 1.6 Query Order
- **Method**: `GET`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/shopping/order/getOrderDetail`
- **Purpose**: Query a single order in detail.
- **Query parameters**:
  - `orderId` `string` required, length `200`: order ID. CJ documents support for custom order ID and CJ order ID.
  - `features` `string[]` optional, length `20`: feature flags. Pass multiple `features` params if multiple features are needed.
- **Feature enumeration**:
  - `LOGISTICS_TIMELINESS`: include logistics timeliness info (`logisticTimelines`) in the response.

### 1.7 Order Delete
- **Method**: `DELETE`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/shopping/order/deleteOrder`
- **Purpose**: Delete an order.
- **Notes**:
  - Keep the exact request parameter set from the official Shopping page when implementing this call. The current extracted text in this workspace did not include the parameter table for this section, so no undocumented fields are added here.

### 1.8 Confirm Order
- **Method**: `PATCH`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/shopping/order/confirmOrder`
- **Purpose**: Confirm an order in the shopping flow.
- **Notes**:
  - Keep the exact request parameter set from the official Shopping page when implementing this call. The current extracted text in this workspace did not include the parameter table for this section, so no undocumented fields are added here.

### 1.9 Change Order Warehouse
- **Method**: use the exact method documented on the Shopping page
- **Endpoint**: keep the exact current endpoint from the Shopping page when implementing.
- **Purpose**: Change an order's warehouse in supported scenarios.
- **Notes**:
  - The current extracted text in this workspace did not include the parameter table for this section, so no undocumented fields are added here.

## 2. Payment APIs

### 2.1 Get Balance
- **Method**: `GET`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/shopping/pay/getBalance`
- **Purpose**: Read CJ balance information.
- **Query parameters**: none documented.

### 2.2 Pay Balance V2
- **Method**: `POST`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/shopping/pay/payBalanceV2`
- **Purpose**: Pay a shipment order using the newer balance-payment interface.
- **Headers**:
  - `CJ-Access-Token` required.
  - `Content-Type: application/json` required.
- **JSON body parameters**:
  - `shipmentOrderId` `string` required, length `200`: shipment order ID.
  - `payId` `string` required, length `200`: pay ID.
- **Notes**:
  - Older `payBalance` is intentionally omitted because `payBalanceV2` is the newer same-purpose payment endpoint on the official page.

## 3. Shipping Info APIs

### 3.1 Upload Shipping Info
- **Method**: `POST`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/shopping/order/uploadWaybillInfo`
- **Purpose**: Upload seller/platform-logistics waybill information after order payment.
- **Headers**:
  - `CJ-Access-Token` required.
  - Use `multipart/form-data`.
- **Form-data parameters**:
  - `orderId` `string` required, length `200`: order ID.
  - `cjOrderId` `string` required, length `200`: CJ order ID.
  - `cjShippingCompanyName` `string` required, length `200`: CJ shipping company name. CJ points to Storage Info `logisticsBrandList` as the source of valid values.
  - `trackNumber` `string` required, length `200`: tracking number.
  - `waybillFile` `MultipartFile` required, length `200`: waybill document file.
- **Notes**:
  - CJ explicitly says this interface can only be called after CJ order payment.

### 3.2 Update Shipping Info
- **Method**: `POST`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/shopping/order/updateWaybillInfo`
- **Purpose**: Update previously uploaded waybill information.
- **Headers**:
  - `CJ-Access-Token` required.
  - Use `multipart/form-data`.
- **Form-data parameters**:
  - `orderId` `string` required, length `200`: order ID.
  - `cjOrderId` `string` required, length `200`: CJ order ID.
  - `cjShippingCompanyName` `string` required, length `200`: CJ shipping company name. CJ points to Storage Info `logisticsBrandList` as the source of valid values.
  - `trackNumber` `string` required, length `200`: tracking number.
  - `waybillFile` `MultipartFile` required, length `200`: waybill document file.

### 3.3 Update POD Pictures
- **Method**: `POST`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/shopping/order/podProductCustomPicturesEdit`
- **Purpose**: Update POD production/rendering pictures for order items.
- **Headers**:
  - `CJ-Access-Token` required.
  - `platformToken` optional as documented by CJ.
  - `Content-Type: application/json` required.
- **JSON body parameters**:
  - `podPicturesEditParams` `object[]` required: item-level update list.
    - `orderCode` `string` required, length `200`: CJ order ID.
    - `lineItemId` `string` required, length `200`: unique CJ order item ID.
    - `effectImgList` `string[]` required, length `200`: product rendering images.
    - `productionImgList` `string[]` required, length `200`: production images.
