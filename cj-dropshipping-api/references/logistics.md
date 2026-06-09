# Logistics API (Verified)

Source: `https://developers.cjdropshipping.cn/en/api/api2/api/logistic.html`

This reference keeps the current/newer logistics interfaces and omits deprecated ones where the official page marks a replacement. Response fields are intentionally omitted.

## 1. Logistics APIs

### 1.1 Freight Calculation
- **Method**: `POST`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/logistic/freightCalculate`
- **Purpose**: Simple logistics trial calculation. CJ explicitly recommends `freightCalculateTip` for more accurate calculation.
- **Headers**:
  - `CJ-Access-Token` required.
  - `Content-Type: application/json` required.
- **JSON body parameters**:
  - `startCountryCode` `string` required, length `200`: origin country code.
  - `endCountryCode` `string` required, length `200`: destination country code.
  - `zip` `string` optional, length `200`: destination ZIP/postal code.
  - `taxId` `string` optional, length `200`: tax ID.
  - `houseNumber` `string` optional, length `200`: house number.
  - `iossNumber` `string` optional, length `200`: IOSS number.
  - `products` `object[]` required: product list.
    - `quantity` `int` required, length `10`: quantity.
    - `vid` `string` required, length `200`: variant ID.

### 1.2 Freight Calculation Tip
- **Method**: `POST`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/logistic/freightCalculateTip`
- **Purpose**: More accurate freight trial calculation.
- **Headers**:
  - `CJ-Access-Token` required.
  - `Content-Type: application/json` required.
- **JSON body parameters**:
  - `reqDTOS` `object[]` required: freight trial request list.
    - `srcAreaCode` `string` required, length `200`: origin country code.
    - `destAreaCode` `string` required, length `200`: destination country code.
    - `customerCode` `string` optional, length `200`: customer code.
    - `zip` `string` optional, length `200`: ZIP/postal code.
    - `houseNumber` `string` optional, length `100`: house number.
    - `iossNumber` `string` optional, length `200`: IOSS number.
    - `storageIdList` `string[]` optional, length `100`: storage ID list.
    - `recipientAddress` `string` optional, length `200`: recipient address.
    - `city` `string` optional, length `50`: city.
    - `recipientName` `string` optional, length `200`: recipient name.
    - `skuList` `string[]` required, length `200`: SKU list.
    - `town` `string` optional, length `100`: town.
    - `phone` `string` optional, length `50`: phone.
    - `wrapWeight` `int` required, length `200`: wrap weight in grams.
    - `volume` `BigDecimal` required, length `200`: volume in `cm^3`.
    - `station` `string` optional, length `200`: station.
    - `platforms` `string[]` optional, length `200`: platform list. CJ refers to the Platforms appendix.
    - `dutyNo` `string` optional, length `200`: duty number.
    - `email` `string` optional, length `100`: email.
    - `province` `string` optional, length `100`: province/state.
    - `recipientAddress1` `string` optional, length `200`: address line 1.
    - `uid` `string` optional, length `200`: UID.
    - `recipientId` `string` optional, length `200`: recipient ID.
    - `recipientAddress2` `string` optional, length `200`: address line 2.
    - `amount` `BigDecimal` optional, length `50`: amount.
    - `productTypes` `string[]` optional: product type list. Documented values: `0` normal goods, `1` service goods, `3` packaged goods, `4` supplier goods, `5` supplier self-delivered goods, `6` virtual goods, `7` POD personalized goods.
    - `weight` `int` required, length `100`: weight in grams.
    - `productProp` `string` required, length `100`: product property.
    - `optionName` `string` optional, length `200`: option name.
    - `volumeWeight` `BigDecimal` optional, length `100`: volumetric weight in grams.
    - `orderType` `string` optional, length `100`: order type.
    - `totalGoodsAmount` `BigDecimal` optional, length `100`: total value of goods.
    - `freightTrialSkuList` `object[]` required: SKU-level trial list.
      - `productCode` `string` optional, length `100`: product code.
      - `sku` `string` optional, length `100`: SKU.
      - `productPropList` `string[]` optional, length `100`: product attributes.
      - `productTypeList` `string[]` optional: same enumeration as `productTypes`.
      - `vid` `string` optional, length `100`: variant ID.
      - `skuQuantity` `int` optional, length `50`: SKU quantity.
      - `skuWeight` `BigDecimal` optional, length `100`: SKU weight in grams.
      - `skuVolume` `BigDecimal` optional, length `100`: SKU volume in `cm^3`.
      - `combinationType` `int` optional, length `50`: combination type.
      - `parentVid` `string` optional, length `50`: parent variant ID.
      - `unsalable` `int` optional, length `10`: unsalable flag.
      - `tailCostQuantity` `int` optional, length `10`: tail-cost quantity.
      - `privateDeductionQuantity` `int` optional, length `10`: private-deduction quantity.

### 1.3 Partner Freight Calculation
- **Method**: `POST`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/logistic/partnerFreightCalculate`
- **Purpose**: Freight calculation for merchant partner orders.
- **Headers**:
  - `CJ-Access-Token` required.
  - `Content-Type: application/json` required.
- **JSON body parameters**:
  - `orderNumber` `string` required, length `40`: order number.
  - `shippingCountryCode` `string` required, length `200`: destination country code.
  - `shippingCountry` `string` required, length `200`: destination country.
  - `shippingProvince` `string` required, length `200`: province/state.
  - `shippingCity` `string` required, length `200`: city.
  - `shippingAddress` `string` optional, length `200`: address.
  - `shippingCustomerName` `string` optional, length `200`: recipient name.
  - `shippingZip` `string` required, length `200`: ZIP/postal code.
  - `shippingPhone` `string` optional, length `200`: phone. CJ notes it should be accurate.
  - `houseNumber` `string` optional, length `20`: house number.
  - `remark` `string` optional, length `500`: order remark.
  - `logisticName` `string` optional, length `200`: logistics name.
  - `fromCountryCode` `string` required, length `200`: origin/warehouse country code.
  - `email` `string` optional, length `200`: email.
  - `consigneeID` `string` optional, length `200`: consignee ID.
  - `iossType` `int` optional, length `20`: IOSS type.
    - `1`: do not use IOSS
    - `2`: use your own IOSS number
    - `3`: use CJ's IOSS number
  - `iossNumber` `string` optional, length `20`: IOSS number.
  - `products` `object[]` required, length `200`: product list.
    - `vid` `string` required, length `200`: variant ID.
    - `quantity` `int` required, length `200`: quantity.

### 1.4 Supplier self-shipment logistics trial calculation
- **Method**: `POST`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/logistic/getSupplierLogisticsTemplate`
- **Purpose**: Query supplier self-shipment logistics templates.
- **Headers**:
  - `CJ-Access-Token` required.
  - `Content-Type: application/json` required.
- **JSON body parameters**:
  - `skuList` `string[]` required, length `200`: product SPU list.

## 2. Tracking APIs

### 2.1 Get Tracking Information
- **Method**: `GET`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/logistic/getTrackInfo`
- **Purpose**: Current tracking-information endpoint.
- **Notes**:
  - The deprecated tracking endpoint is intentionally omitted.
  - Keep the exact current query parameter set from the official Logistic page when implementing this call. The extracted text available in this workspace does not include the parameter table for this subsection, so no undocumented fields are added here.
