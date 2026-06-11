# CJ Dropshipping API V2.0 Verified Endpoints Index

This list is verified against the account quota limits and live testing.

## Authentication
| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/api2.0/v1/authentication/getAccessToken` | Exchange API Key for tokens. |
| POST | `/api2.0/v1/authentication/refreshAccessToken` | Refresh access token. |
| POST | `/api2.0/v1/authentication/logout` | Invalidate tokens. |

## Settings
| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api2.0/v1/setting/get` | Get account info, QPS, and quota limits. |

## Products
| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api2.0/v1/product/getCategory` | Hierarchical category tree. |
| GET | `/api2.0/v1/product/listV2` | Search products (ES engine). |
| GET | `/api2.0/v1/product/query` | Product details (by pid). |
| GET | `/api2.0/v1/product/variant/query` | List variants for a product (by pid). |
| GET | `/api2.0/v1/product/variant/queryByVid` | Specific variant details (by vid). |
| GET | `/api2.0/v1/product/stock/queryByVid` | Real-time stock for a variant (by vid). |
| GET | `/api2.0/v1/product/comments` | Product reviews. |
| POST | `/api2.0/v1/product/sourcing/create` | Request product sourcing. |
| POST | `/api2.0/v1/product/sourcing/query` | Check sourcing status. |

## Shopping & Orders
| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/api2.0/v1/shopping/order/createOrderV2` | Place dropshipping order. |
| POST | `/api2.0/v1/shopping/order/confirmOrder` | Confirm order. |
| GET | `/api2.0/v1/shopping/order/getOrderDetail` | Get specific order info. |
| GET | `/api2.0/v1/shopping/order/list` | Paginated order list. |
| POST | `/api2.0/v1/shopping/order/deleteOrder` | Delete order. |
| GET | `/api2.0/v1/shopping/pay/getBalance` | Check CJ wallet balance. |
| POST | `/api2.0/v1/shopping/pay/payBalance` | Pay order using balance. |

## Logistics
| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/api2.0/v1/logistic/freightCalculate` | Shipping cost calculation. |
| POST | `/api2.0/v1/logistic/freightCalculateTip` | Advanced cost calculation. |
| GET | `/api2.0/v1/logistic/trackInfo` | Real-time tracking. |
| GET | `/api2.0/v1/logistic/getTrackInfo` | Detailed tracking info. |

## Disputes
| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api2.0/v1/disputes/getDisputeList` | List all disputes. |
| GET | `/api2.0/v1/disputes/disputeProducts` | List products for dispute. |
| POST | `/api2.0/v1/disputes/create` | Open a dispute. |
| POST | `/api2.0/v1/disputes/cancel` | Cancel a dispute. |
| POST | `/api2.0/v1/disputes/disputeConfirmInfo` | Confirm dispute info. |
