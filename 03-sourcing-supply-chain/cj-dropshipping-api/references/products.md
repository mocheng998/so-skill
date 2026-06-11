# Product API (Verified)

Source: `https://developers.cjdropshipping.cn/en/api/api2/api/product.html`

This file covers the product-related endpoints documented on CJ Dropshipping's Product API page only. All endpoints below require the `CJ-Access-Token` request header unless noted otherwise.

## 1. Product catalog and search

### 1.1 Get Category List
- **Method**: `GET`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/product/getCategory`
- **Purpose**: Return CJ's category tree.
- **Query parameters**: none.

### 1.2 Product List V2
- **Method**: `GET`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/product/listV2`
- **Purpose**: Main high-performance product search/list endpoint. Uses Elasticsearch according to CJ docs.
- **Documented notes**:
  1. Supports keyword search.
  2. Supports multiple filters such as price range, category, and country.
  3. Supports sorting.
  4. `features` can expand returned product/category details.
  5. `page` min `1`, max `1000`; `size` min `1`, max `100`.
- **Query parameters**:
  - `keyWord` `string` optional, length `200`: search keyword; matches product name or SKU.
  - `page` `int` optional, length `20`: page number; default `1`, minimum `1`, maximum `1000`.
  - `size` `int` optional, length `20`: results per page; docs state default `10`, minimum `1`, maximum `100`.
  - `categoryId` `string` optional, length `200`: filter by third-level category ID.
  - `lv2categoryList` `array` optional: filter by second-level category ID list.
  - `lv3categoryList` `array` optional: filter by third-level category ID list.
  - `countryCode` `string` optional, length `200`: ISO-like country code such as `CN`, `US`, `GB`, `FR`; returns products with inventory in the specified countries.
  - `startSellPrice` `decimal` optional: minimum sell price.
  - `endSellPrice` `decimal` optional: maximum sell price.
  - `addMarkStatus` `int` optional, length `1`: free-shipping filter; `0` = not free shipping, `1` = free shipping.
  - `productType` `int` optional, length `15`: product type filter; documented values include `4` = supplier product, `10` = video product, `11` = non-video product.
  - `productFlag` `int` optional, length `1`: product flag; `0` = trending, `1` = new, `2` = video, `3` = slow-moving.
  - `startWarehouseInventory` `int` optional: minimum warehouse inventory.
  - `endWarehouseInventory` `int` optional: maximum warehouse inventory.
  - `verifiedWarehouse` `int` optional, length `1`: warehouse verification filter; `0` or null = all, `1` = verified inventory, `2` = unverified inventory.
  - `timeStart` `long` optional: listing start timestamp in milliseconds.
  - `timeEnd` `long` optional: listing end timestamp in milliseconds.
  - `zonePlatform` `string` optional, length `200`: platform recommendation hint such as `shopify`, `ebay`, `amazon`, `tiktok`, `etsy`.
  - `isWarehouse` `boolean` optional, length `1`: whether to search global warehouse products; `true` or `false`.
  - `sort` `string` optional, length `4`: sort direction; `desc` default, or `asc`.
  - `orderBy` `int` optional, length `20`: sort field; `0` = best match, `1` = listing count, `2` = sell price, `3` = create time, `4` = inventory.
  - `features` `array` optional, length `200`: supported values are `enable_description`, `enable_category`, `enable_combine`, `enable_video`.
  - `supplierId` `string` optional, length `200`: supplier ID filter.
  - `hasCertification` `int` optional, length `1`: certification filter; `0` = no, `1` = yes.
  - `isSelfPickup` `int` optional, length `1`: self-pickup filter; `0` = no, `1` = yes.
  - `customization` `int` optional, length `1`: customization product filter; `0` = no, `1` = yes.
- **Use when**: catalog browsing, keyword search, filtered discovery.


## 2. Product details and My Products

### 2.1 Product Details
- **Method**: `GET`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/product/query`
- **Purpose**: Fetch a single product plus variants and optional expansions.
- **Query parameters**:
  - `pid` `string` conditional, length `200`: product ID. Choose one of `pid`, `productSku`, or `variantSku`.
  - `productSku` `string` conditional, length `200`: product SPU code. Choose one of `pid`, `productSku`, or `variantSku`.
  - `variantSku` `string` conditional, length `200`: variant SKU code. Choose one of `pid`, `productSku`, or `variantSku`.
  - `features` `List` optional, length `200`: optional expansion list.
    - `enable_combine`: include combination variants and combination product info.
    - `enable_video`: include product video info.
    - `enable_inventory`: include variant inventory info, including storage ID.
  - `countryCode` `string` optional, length `2`: country code such as `CN` or `US`; when passed, only returns variants with inventory in that country.

### 2.2 Add to My Product
- **Method**: `POST`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/product/addToMyProduct`
- **Purpose**: Save a CJ product into the authenticated account's My Products.
- **JSON body parameters**:
  - `productId` `string` required, length `100`: CJ product ID to add into My Products.
- **Notes**:
  - Re-adding the same product returns the documented business error `1600000` with message `The product has been added to My Products.`

### 2.3 My Product List
- **Method**: `GET`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/product/myProduct/query`
- **Purpose**: Query products already added into My Products.
- **Query parameters**:
  - `keyword` `string` optional, length `200`: search by SKU, SPU, or product name.
  - `categoryId` `string` optional, length `200`: category ID filter.
  - `startAt` `string` optional, length `200`: start time filter.
  - `endAt` `string` optional, length `200`: end time filter. The CJ table labels this as `ent time`, clearly meaning end time.
  - `isListed` `int` optional, length `200`: listing-state filter.
  - `visiable` `int` optional: visibility filter. Keep CJ's original misspelling `visiable` when calling the API.
  - `hasPacked` `int` optional: packing-state filter.
  - `hasVirPacked` `int` optional: virtual-packing-state filter.

## 3. Variant APIs

### 3.1 Inquiry Of All Variants
- **Method**: `GET`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/product/variant/query`
- **Purpose**: Return variants for a product or SKU.
- **Query parameters**:
  - `pid` `string` conditional, length `200`: product ID. Choose one of `pid`, `productSku`, or `variantSku`.
  - `productSku` `string` conditional, length `200`: product SKU/SPU. Choose one of `pid`, `productSku`, or `variantSku`.
  - `variantSku` `string` conditional, length `200`: variant SKU. Choose one of `pid`, `productSku`, or `variantSku`.
  - `countryCode` `string` optional, length `2`: country code; if provided, only variants with inventory in that country are returned.

### 3.2 Variant Id Inquiry
- **Method**: `GET`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/product/variant/queryByVid`
- **Purpose**: Return one variant by `vid`.
- **Query parameters**:
  - `vid` `string` required, length `200`: variant ID.
  - `features` `string` optional, length `200`: supported value is `enable_inventory`, which includes variant inventory info including storage ID.

## 4. Inventory APIs

### 4.1 Inventory Inquiry by Variant ID
- **Method**: `GET`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/product/stock/queryByVid`
- **Purpose**: Query warehouse inventory for a single variant.
- **Query parameters**:
  - `vid` `string` required, length `200`: unique variant identifier.

### 4.2 Query Inventory by SKU
- **Method**: `GET`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/product/stock/queryBySku`
- **Purpose**: Query inventory by SKU or SPU.
- **Query parameters**:
  - `sku` `string` required, length `200`: SKU or SPU.

### 4.3 Query Inventory by Product ID
- **Method**: `GET`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/product/stock/getInventoryByPid`
- **Purpose**: Return both product-level and variant-level inventory by product ID.
- **Query parameters**:
  - `pid` `string` required, length `40`: product ID.

## 5. Reviews and sourcing endpoints on the same page

The Product page also documents review and sourcing endpoints. They are product-adjacent but not catalog/detail endpoints:
- `GET /api2.0/v1/product/productComments`
  - `pid` `string` required: product ID.
  - `score` `int` optional: review-score filter.
  - `pageNum` `int` optional: page number.
  - `pageSize` `int` optional: page size.
- `POST /api2.0/v1/product/sourcing/create`
  - `thirdProductId` `string` optional, length `200`: third-party product ID.
  - `thirdVariantId` `string` optional, length `200`: third-party variant ID.
  - `thirdProductSku` `string` optional, length `200`: third-party product SKU.
  - `productName` `string` required, length `200`: product name.
  - `productImage` `string` required, length `200`: product image URL.
  - `productUrl` `string` optional, length `200`: product page URL.
  - `remark` `string` optional, length `200`: sourcing remark.
  - `price` `BigDecimal` optional, length `200`: unit price in USD.
- `POST /api2.0/v1/product/sourcing/query`
  - `sourceIds` `string[]` required, length `200`: list of CJ sourcing IDs.

If this reference is later extended, document those in separate sections rather than mixing them into core catalog APIs.

## 6. Accuracy notes for implementers

- Use `product/query` with `pid`, `productSku`, or `variantSku`; do not invent a `productId` query parameter for this endpoint.
- Use `product/listV2` as the catalog listing/search endpoint in new integrations; the legacy `product/list` endpoint has been intentionally omitted from this reference.
- `product/variant/queryByVid` is the documented variant-detail endpoint; inventory expansion is optional via `features=enable_inventory`.
- `product/stock/queryByVid`, `product/stock/queryBySku`, and `product/stock/getInventoryByPid` are separate inventory endpoints and should not be collapsed into one abstraction without preserving their response differences.
- CJ's docs contain some inconsistent naming in examples vs field tables, such as `packingWeight` in payload examples vs `packWeight` in the field table. Preserve the documented field names your integration actually receives.
