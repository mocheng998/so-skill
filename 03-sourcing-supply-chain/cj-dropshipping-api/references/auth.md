# Authentication & Token Management

CJ Dropshipping API V2.0 uses an access-token plus refresh-token model. Authenticated requests must send `CJ-Access-Token` in the request header.

## Endpoints

### 1. Get Access Token
**Endpoint**: `POST /api2.0/v1/authentication/getAccessToken`

**Body**:
```json
{"apiKey": "YOUR_API_KEY"}
```

### 2. Refresh Access Token
**Endpoint**: `POST /api2.0/v1/authentication/refreshAccessToken`

**Body**:
```json
{"refreshToken": "YOUR_REFRESH_TOKEN"}
```

### 3. Logout Token
**Endpoint**: `POST /api2.0/v1/authentication/logout`

## Token lifecycle rules

- Access token lifetime is generally **15 days**.
- Refresh token lifetime is generally **180 days**.
- Store both tokens on the backend only.
- Check token expiry before API calls.
- If the access token is near expiry, refresh proactively.
- If both access and refresh tokens are expired, reauthorize and obtain a new token pair.
- CJ explicitly recommends using a delay queue or similar mechanism to avoid concurrent refresh races.
