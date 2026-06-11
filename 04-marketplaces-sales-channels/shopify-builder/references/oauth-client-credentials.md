# Getting API Credentials — Client Credentials OAuth

The user needs **three values** — store domain (e.g. `31vbs5-ae.myshopify.com`), Client ID, and Client Secret (starts with `shpss_`) — to exchange for an Access Token.

> **Important**: Shopify no longer supports creating legacy Custom Apps from Admin. All new apps must be created via the [Dev Dashboard](https://dev.shopify.com/dashboard).

## Step 1: Create a new app

1. Open the [Shopify Dev Dashboard](https://dev.shopify.com/dashboard) and log in with the store owner account.
2. Make sure **Apps** is selected in the left-panel navigation, then click **"Create app"** in the top-right corner.
3. Select **"Start from Dev Dashboard"**.
4. Enter an App name (e.g. `My Store API`), click **"Create"**.

## Step 2: Create a version (configure & release)

A **version** is a snapshot of your app's configuration, URLs, and scopes. Your app must have at least one released version before it can be installed.

1. From the **Versions** tab of your app, complete the following:
   - **App URL** — if your app is not embedded in Admin, use the default `https://shopify.dev/apps/default-app-home` or any valid URL (e.g. `https://example.com`).
   - **Webhooks API Version** — select the latest (e.g. `2026-01`).
   - **Scopes** — click **"Select scopes"** and choose: `write_products, read_products, write_themes, read_themes, write_files, read_files, write_orders, read_orders` (or select **all scopes** to avoid permission issues). Note: access to protected customer data requires separate approval.
2. Click **"Release"** to publish this version. **The app cannot be installed until a version is released.**

> When you update scopes in a new version, merchants need to manually approve the new scopes in their Admin.

## Step 3: Install your app (CRITICAL — do not skip)

**An uninstalled app cannot exchange credentials for an Access Token.** All API calls will fail with `shop_not_permitted` if this step is skipped.

1. From your app in the Dev Dashboard, select **"Home"** in the left panel.
2. Scroll down and click **"Install app"**.
3. Select or create the target store.
4. Click **"Install"**.

Your app is now installed on the store.

## Step 4: Get your credentials

1. From your app in the Dev Dashboard, select **"Settings"** in the left panel.
2. Find the **"Credentials"** section:
   - **Client ID** — a hex string (e.g. `c29b7d62f235b242380653713f39232c`). Click copy to copy.
   - **Client Secret** — hidden by default; click reveal to show (starts with `shpss_`). Click copy to copy.

> **Security**: Keep your Client Secret secure. Store credentials in a `.env` file and add it to `.gitignore`. Never commit secrets to version control.

## Step 5: Exchange credentials for an Access Token

Use the Client ID and Client Secret to programmatically request an access token from Shopify's OAuth endpoint. You will NOT copy a token from a browser page — your code requests a token when it needs one.

**Token exchange — execute via bash (`curl`):**

```bash
curl -s -X POST "https://{STORE_NAME}.myshopify.com/admin/oauth/access_token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}"
```

**Token response format:**

```json
{
  "access_token": "shpat_...",
  "scope": "write_products,read_products,write_themes,...",
  "expires_in": 86399
}
```

| Field | Description |
|---|---|
| `access_token` | The `shpat_*` token to include in API requests |
| `scope` | The access scopes granted to your app |
| `expires_in` | Seconds until expiration — always **86399** (24 hours) |

**Critical details:**
- Content-Type MUST be `application/x-www-form-urlencoded` (not JSON).
- Use `data=` (form-encoded), NOT `json=` (JSON body) — Shopify rejects JSON for this endpoint.
- The returned `shpat_` token is used in `X-Shopify-Access-Token` headers for all subsequent API calls.
- Token expires after **24 hours** — your code should request a new one when needed.

**Validation — always run after token exchange:**

```bash
curl -s "https://{STORE_NAME}.myshopify.com/admin/api/2026-01/shop.json" \
  -H "X-Shopify-Access-Token: {ACCESS_TOKEN}" \
  -H "Content-Type: application/json"
```

Confirm the response includes `shop.name`, `shop.domain`, and `shop.myshopify_domain`. Check `password_enabled` to know if the storefront is locked.

## Troubleshooting

| Error | Cause | Solution |
|---|---|---|
| `shop_not_permitted: Client credentials cannot be performed on this shop` | App is not installed on the store, or app and store are not in the same organization | Go back to **Step 3** and install the app. Client credentials only works within your organization. |
| External tool asks you to "copy a token" | The tool expects the older authentication flow | Use this Client Credentials method instead; contact the tool vendor about updating their integration to use OAuth. |
| `Invalid API key or access token` | Sending `client_id` or `client_secret` directly to the Admin API instead of an access token | First exchange credentials for an `access_token` using the token endpoint (Step 5), then use that token in API requests. |
