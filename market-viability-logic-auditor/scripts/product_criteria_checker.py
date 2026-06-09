#!/usr/bin/env python3
"""
Product Market Viability Criteria Checker

Validates whether a product meets the recommended criteria for e-commerce sellers.
"""

import sys
import json


def check_product_criteria(
    monthly_sales: int,
    price: float,
    competition_level: str,
    category: str,
    is_electronic: bool = False,
    is_bulky: bool = False,
    is_fragile: bool = False,
    has_major_brand: bool = False
) -> dict:
    """
    Check if a product meets the criteria for e-commerce market entry.
    
    Args:
        monthly_sales: Average monthly sales per seller
        price: Product price in USD
        competition_level: "low", "medium", or "high"
        category: Product category
        is_electronic: Whether the product is electronic
        is_bulky: Whether the product is large/bulky
        is_fragile: Whether the product is fragile
        has_major_brand: Whether the market is dominated by major brands
    
    Returns:
        dict with 'passed', 'score', 'issues', and 'recommendations'
    """
    issues = []
    recommendations = []
    score = 100
    
    # Check monthly sales (ideal: 100-300)
    if monthly_sales < 100:
        issues.append(f"Monthly sales ({monthly_sales}) below recommended minimum (100)")
        score -= 20
        recommendations.append("Look for products with higher demand")
    elif monthly_sales > 300:
        issues.append(f"Monthly sales ({monthly_sales}) above recommended range (100-300)")
        score -= 10
        recommendations.append("Higher sales may indicate more competition")
    
    # Check price (minimum: $20)
    if price < 20:
        issues.append(f"Price (${price}) below recommended minimum ($20)")
        score -= 25
        recommendations.append("Higher-priced products offer better profit margins")
    
    # Check competition level
    if competition_level.lower() == "high":
        issues.append("Competition level is high")
        score -= 20
        recommendations.append("Consider products with medium or low competition")
    
    # Check product type restrictions
    if is_electronic:
        issues.append("Product is electronic (high return rates and support overhead)")
        score -= 15
        recommendations.append("Avoid electronics due to higher return rates and complexity")
    
    if is_bulky:
        issues.append("Product is bulky/large (not recommended)")
        score -= 15
        recommendations.append("Avoid bulky items due to higher shipping and storage costs")
    
    if is_fragile:
        issues.append("Product is fragile (not recommended)")
        score -= 15
        recommendations.append("Avoid fragile items due to higher damage and return rates")
    
    if has_major_brand:
        issues.append("Market dominated by major brands")
        score -= 20
        recommendations.append("Look for markets with more opportunities for private label")
    
    # Determine pass/fail
    passed = score >= 60 and not (is_electronic or is_bulky or is_fragile or has_major_brand)
    
    return {
        "passed": passed,
        "score": max(0, score),
        "issues": issues,
        "recommendations": recommendations,
        "summary": "PASS - Good candidate for market entry" if passed else "FAIL - Does not meet criteria"
    }


def main():
    """CLI interface for the product criteria checker."""
    if len(sys.argv) < 2:
        print("Usage: python3 product_criteria_checker.py <json_file>")
        print("\nJSON format:")
        print(json.dumps({
            "monthly_sales": 200,
            "price": 25.99,
            "competition_level": "medium",
            "category": "Home & Kitchen",
            "is_electronic": False,
            "is_bulky": False,
            "is_fragile": False,
            "has_major_brand": False
        }, indent=2))
        sys.exit(1)
    
    # Load product data from JSON file
    with open(sys.argv[1], 'r') as f:
        product_data = json.load(f)
    
    # Check criteria
    result = check_product_criteria(**product_data)
    
    # Print results
    print("\n" + "="*60)
    print("PRODUCT MARKET VIABILITY CHECK")
    print("="*60)
    print(f"\nResult: {result['summary']}")
    print(f"Score: {result['score']}/100")
    
    if result['issues']:
        print(f"\n⚠️  Issues Found ({len(result['issues'])}):")
        for i, issue in enumerate(result['issues'], 1):
            print(f"  {i}. {issue}")
    
    if result['recommendations']:
        print(f"\n💡 Recommendations ({len(result['recommendations'])}):")
        for i, rec in enumerate(result['recommendations'], 1):
            print(f"  {i}. {rec}")
    
    print("\n" + "="*60)
    
    # Exit with appropriate code
    sys.exit(0 if result['passed'] else 1)


if __name__ == "__main__":
    main()
