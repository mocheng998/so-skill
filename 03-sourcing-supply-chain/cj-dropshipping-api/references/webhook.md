# Webhook API (Verified)

Source: `https://developers.cjdropshipping.cn/en/api/api2/api/webhook.html`

This reference keeps the currently documented webhook configuration interface and focuses on accurate request details. Response fields are intentionally omitted.

## 1. Webhook Setting

### 1.1 Message Setting
- **Method**: `POST`
- **Endpoint**: `https://developers.cjdropshipping.com/api2.0/v1/webhook/set`
- **Purpose**: Configure CJ webhook callbacks for product, stock, order, and logistics events.
- **Headers**:
  - `CJ-Access-Token` required.
  - `Content-Type: application/json` required.
- **JSON body parameters**:
  - `product` `object` required, length `200`: product-message setting.
    - `type` `string` required, length `200`: `ENABLE` or `CANCEL`.
    - `callbackUrls` `string[]` required, length `1`: only one callback URL is supported; it must be a reachable public HTTPS URL.
  - `stock` `object` required, length `200`: stock-message setting.
    - `type` `string` required, length `200`: `ENABLE` or `CANCEL`.
    - `callbackUrls` `string[]` required, length `1`: only one callback URL is supported; it must be a reachable public HTTPS URL.
  - `order` `object` required, length `200`: order-message setting.
    - `type` `string` required, length `200`: `ENABLE` or `CANCEL`.
    - `callbackUrls` `string[]` required, length `1`: only one callback URL is supported; it must be a reachable public HTTPS URL.
  - `logistics` `object` required, length `200`: logistics-message setting.
    - `type` `string` required, length `200`: `ENABLE` or `CANCEL`.
    - `callbackUrls` `string[]` required, length `1`: only one callback URL is supported; it must be a reachable public HTTPS URL.
- **Operational requirements from the page**:
  - Callback URL must be public `HTTPS`; `localhost` and `127.0.0.1` are not supported.
  - CJ sends webhook requests as `POST` with `Content-Type: application/json`.
  - Your endpoint should return `200 OK` within `3 seconds`.
