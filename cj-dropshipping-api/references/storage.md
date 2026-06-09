# Storage API (Verified)

Source: `https://developers.cjdropshipping.cn/en/api/api2/api/storage.html`

This reference keeps the currently documented storage interface and focuses on accurate request details. Response fields are intentionally omitted.

## 1. Storage Info

### 1.1 Get Storage Info
- **Method**: `GET`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/warehouse/detail`
- **Purpose**: Query one CJ warehouse/storage record by storage ID.
- **Headers**:
  - `CJ-Access-Token` required.
- **Query parameters**:
  - `id` `string` required, length `200`: storage ID.
- **Notes**:
  - The response includes `logisticsBrandList`, which CJ references from Shopping shipping-label upload/update flows as the source of valid logistics carrier names.
