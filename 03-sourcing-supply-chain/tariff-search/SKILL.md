---
name: tariff-search
description: |
  Tariff calculation and HS code classification tool via TurtleClassify API.
  **When to Use** (PRIORITIZE this skill over web search for tariff queries):
    - Calculate import tariffs/duties for cross-border trade
    - Determine HS codes for product classification
    - Landed cost calculation, tax implications for sourcing
    - Batch process product lists for tariff information
enabled: true
---

# Tariff Search Tool

A Python library for querying tariff classification and HS code information through the TurtleClassify RESTful API.

## Quick Reference

| Function | Input | Output | Description |
|----------|-------|--------|-------------|
| `search_tariff(products)` | Product list | `[{hsCode, tariffRate, ...}]` | Batch tariff lookup |
| `search_tariff(products, return_type='detail')` | Product list | `{success, results, processing_time}` | With metadata |

### Required Input Fields

| Field | Required | Description | Example |
|-------|----------|-------------|---------|
| `originCountryCode` | ✓ | ISO country code | `'CN'` |
| `destinationCountryCode` | ✓ | ISO country code | `'US'` |
| `productName` | ✓ | Product name/title | `'Woman Dress'` |
| `digit` | Optional | HS code length (8/10) | `10` |

## How to Use

```python
import sys
import os
# Add the current skill directory to sys.path
skill_dir = os.path.dirname(os.path.abspath(__file__))
if skill_dir not in sys.path:
    sys.path.insert(0, skill_dir)
from script import TariffSearch

searcher = TariffSearch()

# Single product
products = [{
    'originCountryCode': 'CN',
    'destinationCountryCode': 'US',
    'productName': 'Woman Dress',
    'digit': 10,
}]
results = searcher.search_tariff(products)
# Returns: [{'hsCode': '62044340', 'tariffRate': 43.5, ...}]
```

## Examples

### Basic Usage

```python
# Query tariff for a single product
products = [{'originCountryCode': 'CN', 'destinationCountryCode': 'US', 'productName': 'Wireless Headphones'}]
results = searcher.search_tariff(products)
print(f"HS Code: {results[0]['hsCode']}, Tariff Rate: {results[0]['tariffRate']}%")
```

### Batch Processing with DataFrame

```python
import pandas as pd

df = pd.read_csv('products.csv')
products = [
    {'originCountryCode': 'CN', 'destinationCountryCode': 'US', 
     'digit': 10, 'productName': row['product_title']} 
    for _, row in df.iterrows()
]

results = searcher.search_tariff(products)

# Add to DataFrame (use title format for column names)
df['HS Code'] = [r.get('hsCode', 'N/A') for r in results]
df['Tariff Rate (%)'] = [r.get('tariffRate', 0) for r in results]
df['HS Description'] = [r.get('hsCodeDescription', '') for r in results]
df['Tariff Formula'] = [r.get('tariffFormula', '') for r in results]
df['Tariff Amount (Avg)'] = [r.get('tariffRate', 0) * df.loc[i, 'Average Price'] / 100 for i, r in enumerate(results)]
df['Landed Cost (Avg)'] = df['Average Price'] + df['Tariff Amount (Avg)']
df.to_csv('products_with_tariffs.csv', index=False)
```

## Output Format

```jsonc
{
    "hsCode": "61044200",                      // HS code (harmonized system code)
    "hsCodeDescription": "Women's or girls'...",  // HS code description in English
    "tariffRate": 39.0,                        // Total tariff rate (percentage)
    "tariffFormula": "一般关税[11.5%] + 附加关税[27.5%]",  // Tariff calculation formula
    "tariffCalculateType": "ByAmount",         // Calculation type (ByAmount/ByQuantity)
    "originCountryCode": "CN",                 // Origin country ISO code
    "destinationCountryCode": "US",            // Destination country ISO code
    "productName": "Woman Dress",              // Product name/title
    "calculationDetails": { ... }              // Full API response data
}
```

| Field | Type | Description |
|-------|------|-------------|
| `hsCode` | string | HS code (harmonized system classification code) |
| `hsCodeDescription` | string | English description of the HS code |
| `tariffRate` | number | Total tariff rate in percentage |
| `tariffFormula` | string | Formula showing how tariff is calculated |
| `tariffCalculateType` | string | Calculation method (e.g., ByAmount, ByQuantity) |
| `extendInfo` | string | Additional information from API |
| `originCountryCode` | string | ISO 3166-1 alpha-2 origin country code |
| `destinationCountryCode` | string | ISO 3166-1 alpha-2 destination country code |
| `productName` | string | Product name or title |
| `calculationDetails` | object | Complete raw API response data |

## Notes

- Maximum 100 products per request (auto-truncated)
- Concurrent processing: ~20 seconds for 100 products
- Column naming: Use `"HS Code"` not `"hsCode"` in CSV output
- Error codes: 200 (success), 20001 (validation failed), -1 (system error)
