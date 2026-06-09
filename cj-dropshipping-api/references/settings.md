# Settings API (Verified)

Source: `https://developers.cjdropshipping.cn/en/api/api2/api/setting.html`

This reference keeps the currently documented settings interface only and focuses on accurate request details.

## 1. Settings

### 1.1 Get Settings
- **Method**: `GET`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/setting/get`
- **Purpose**: Read account-level settings, including quota limits, callback configuration, account role, and sandbox status.
- **Headers**:
  - `CJ-Access-Token` required.
- **Query parameters**: none.
- **Notes**:
  - Use this endpoint as the source of truth for account capabilities and throttling-related settings.
