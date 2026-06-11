"""
Tariff Search Library - TurtleClassify RESTful API Client for Tariff Classification

This library provides functions to query tariff classification and HS code information
through the TurtleClassify RESTful API (https://www.accio.com/api/turtle/classify).
It supports single and batch product classification.

API Documentation:
    Endpoint: POST /api/turtle/classify
    Base URL: https://www.accio.com (default)
    
    Response Structure:
        {
            "success": true,
            "msgCode": "200",
            "msgInfo": "ok",
            "data": "{\"success\":true,\"code\":\"200\",\"message\":\"success\",\"data\":{\"hscodeStr\":\"85171200\",\"hscodeDesc\":\"...\",\"tariffRate\":\"0\",\"extendInfo\":\"\"}}"
        }

IMPORTANT - Column Naming Convention:
    When adding results to CSV/DataFrame, ALWAYS use space-separated title format for column names:
    - Use "HS Code" (NOT "hs_code" or "hsCode")
    - Use "Tariff Rate (%)" (NOT "tariff_rate" or "tariffRate")
    - Use "HS Description" (NOT "hs_description" or "hsCodeDescription")
    - Use "Tariff Formula" (NOT "tariff_formula" or "tariffFormula")
    
    The returned dictionary uses camelCase field names ('hsCode', 'tariffRate', 'hsCodeDescription'), 
    but CSV columns should use title format ("HS Code", "Tariff Rate (%)", "HS Description") 
    for better readability.

Usage Examples:
    import sys
    import os
    # Add the current skill directory to sys.path
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    if skill_dir not in sys.path:
        sys.path.insert(0, skill_dir)
    from script import TariffSearch
    
    searcher = TariffSearch()
    
    # Products list with required fields
    products = [{
        'originCountryCode': 'CN',      # Required: ISO country code
        'destinationCountryCode': 'US', # Required: ISO country code
        'productName': 'Woman Dress',   # Required: Product name/title
        'digit': 10,                    # Optional: HS code digit length (8 or 10)
    }]
    
    # Default: Returns flattened list (recommended for DataFrame/CSV)
    results = searcher.search_tariff(products)
    # Returns: [{'hsCode': '62044340', 'tariffRate': 43.5, ...}, ...]
    
    # With metadata: Returns dict with processing details
    results = searcher.search_tariff(products, return_type='detail')
    # Returns: {'success': True, 'results': [...], 'processing_time': 1.5, ...}
    
    # Example: Processing CSV data
    import pandas as pd
    df = pd.read_csv('products.csv')
    products = [{'originCountryCode': 'CN', 'destinationCountryCode': 'US', 
                 'digit': 10, 'productName': row['product_title']} 
                for _, row in df.iterrows()]
    
    results = searcher.search_tariff(products)
    
    # Add results to DataFrame (use title format for column names)
    df['HS Code'] = [r.get('hsCode', 'N/A') for r in results]
    df['Tariff Rate (%)'] = [r.get('tariffRate', 0) for r in results]
    df['HS Description'] = [r.get('hsCodeDescription', '') for r in results]
    df['Tariff Formula'] = [r.get('tariffFormula', '') for r in results]
    df.to_csv('products_with_tariffs.csv', index=False)

Tool Description:
    TurtleClassify Tariff Calculation and HS Code Classification via RESTful API: This tool classifies 
    products and retrieves detailed HS code and tariff information for international trade through 
    the TurtleClassify RESTful API. It provides tariff rates based on product information, origin 
    country, and destination country. Use this tool when you need to calculate import tariffs,
    determine HS codes, or analyze tax implications for cross-border product sourcing.

Parameters (TurtleClassifyDTO):
    products (required, array): A list of product objects to classify. Each product object should contain:
        1) source (required, string): Product source info (defaults to 'alibaba').
        2) originCountryCode (required, string): Origin country code (ISO 3166-1 alpha-2, e.g., 'CN' for China).
        3) destinationCountryCode (required, string): Destination country code (ISO 3166-1 alpha-2, e.g., 'US' for United States).
        4) productName (required, string): Name or title of the product.
        5) digit (optional, integer): Expected HS code digit length (8 or 10).
        6) productId (optional, integer): Unique product identifier.
        7) productSource (optional, string): Source of product data (e.g., 'alibaba').
        8) productCategoryId (optional, integer): Product category identifier.
        9) productCategoryName (optional, string): Product category name.
        10) productProperties (optional, object): Dictionary of product attributes (e.g., {'brand': 'Apple', 'model': 'iPhone 15'}).
        11) productKeywords (optional, array): List of product keywords or search terms.
        12) channel (optional, string): Channel (e.g., 'web').
    
    base_url (optional, string): Base URL for the RESTful API endpoint.
        Defaults to 'https://www.accio.com'.

Batch Processing:
    - Maximum 100 products per request (will truncate if exceeded)
    - Concurrent processing with 50 workers + rate limiting (QPS < 10)
    - 100 products typically complete in ~20 seconds

Error Codes:
    - 200: Success
    - 20001: Parameter validation failed
    - -1: System error
"""

import json
import sys
import time
import random
from typing import List, Dict, Any, Tuple, Union
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

# Auto-add skills directory to Python path if not already present
import os
_SKILLS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _SKILLS_DIR not in sys.path:
    sys.path.insert(0, _SKILLS_DIR)


class TariffSearch:
    """
    Tariff Search Client for querying tariff classification and HS code information.
    
    This class provides methods to classify products and retrieve tariff information
    through RESTful API calls.
    """
    
    # Default base URL for TurtleClassify API
    DEFAULT_BASE_URL = 'https://www.accio.com'
    
    # Maximum number of products per batch query (increased for better concurrency)
    MAX_BATCH_SIZE = 50
    
    # Maximum total number of products to process (will truncate if exceeded)
    MAX_TOTAL_PRODUCTS = 100
    
    def __init__(self, base_url: str = '', timeout: int = 300):
        """
        Initialize TariffSearch client
        
        Args:
            base_url: Base URL for the RESTful API endpoint. 
                      If empty string, uses default 'https://www.accio.com'.
            timeout: Request timeout in seconds
        """
        self.base_url = base_url if base_url else self.DEFAULT_BASE_URL
        self.timeout = timeout
    
    def search_tariff(self, products: List[Dict[str, Any]], return_type: str = 'list') -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Search tariff information for products (unified interface)
        
        Args:
            products: List of product dictionaries. Each dictionary MUST contain:
                - 'originCountryCode' (str, required): Origin country code (ISO 3166-1 alpha-2, e.g., 'CN')
                - 'destinationCountryCode' (str, required): Destination country code (ISO 3166-1 alpha-2, e.g., 'US')
                - 'productName' (str, required): Product name or title
                - 'digit' (int, optional): HS code digit length (8 or 10)
                Example: [{'originCountryCode': 'CN', 'destinationCountryCode': 'US', 'digit': 10, 'productName': 'Woman Dress'}]
            
            return_type: 'list' (default) or 'detail'
                - 'list': Returns List[Dict] - flattened results, ideal for DataFrame/CSV processing
                - 'detail': Returns Dict with metadata (success, processing_time, formatted_output, etc.)
            
        Returns:
            If return_type='list' (default):
                List of flattened result dicts: [{'hsCode': '62044340', 'tariffRate': 43.5, ...}, ...]
                
            If return_type='detail':
                Dict with metadata: {'success': True, 'results': [...], 'processing_time': 1.5, ...}
            
            CSV Column Naming (when return_type='list'):
                df['HS Code'] = [r.get('hsCode', 'N/A') for r in results]
                df['Tariff Rate (%)'] = [r.get('tariffRate', 0) for r in results]
                df['HS Description'] = [r.get('hsCodeDescription', '') for r in results]
                df['Tariff Formula'] = [r.get('tariffFormula', '') for r in results]
        """
        start_time = time.time()
        
        # Validate products
        validated_products = []
        for idx, product in enumerate(products):
            is_valid, error_msg = self._validate_product(product)
            if not is_valid:
                if return_type == 'detail':
                    return {
                        'success': False,
                        'error': f"Error in product {idx + 1}: {error_msg}",
                        'results': []
                    }
                else:
                    print(f"[WARNING] Product {idx + 1} validation failed: {error_msg}")
            validated_products.append(product)
        
        # Process products
        try:
            results = self._process_products(validated_products)
            processing_time = time.time() - start_time
            
            # Return based on return_type
            if return_type == 'detail':
                # Return detailed response with metadata
                if len(results) == 1:
                    response = results[0]
                else:
                    response = {'data': results}
                
                formatted_output = self._format_output(response)
                
                return {
                    'success': True,
                    'results': results,
                    'formatted_output': formatted_output,
                    'raw_response': response,
                    'processing_time': processing_time,
                    'products_count': len(validated_products),
                    'base_url': self.base_url
                }
            else:
                # Default: return flattened list for easy DataFrame usage
                flattened_results = []
                for idx, result in enumerate(results):
                    product = validated_products[idx] if idx < len(validated_products) else {}
                    
                    if not result or 'data' not in result:
                        flattened_results.append({
                            'hsCode': '',
                            'tariffRate': 0,
                            'tariffFormula': '',
                            'tariffCalculateType': '',
                            'originCountryCode': product.get('originCountryCode', ''),
                            'destinationCountryCode': product.get('destinationCountryCode', ''),
                            'productName': product.get('productName', ''),
                            'calculationDetails': {}
                        })
                    else:
                        flattened = self._extract_flattened_result(result['data'], product)
                        flattened_results.append(flattened)
                
                return flattened_results
                
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            if return_type == 'detail':
                return {
                    'success': False,
                    'error': f"Failed to get tariff classification: {str(e)}",
                    'error_trace': error_trace,
                    'results': []
                }
            else:
                print(f"[ERROR] Tariff search failed: {str(e)}")
                return []
    
    def get_tariff_classification_batch(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        [DEPRECATED] Use search_tariff(products) instead.
        Kept for backward compatibility.
        """
        return self.search_tariff(products, return_type='list')

    def _extract_flattened_result(self, data: Dict[str, Any], product: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract and flatten a single result with fallback values.
        
        Handles both TurtleClassify API response format and legacy format:
        
        TurtleClassify format (new):
            {
                "hscodeStr": "85171200",
                "hscodeDesc": "Other apparatus for transmission...",
                "tariffRate": "0",  # Note: string type
                "extendInfo": ""
            }
        
        Legacy format:
            {
                "hscodeInfo": {"hscode": "...", "descriptionEn": "..."},
                "tariffRate": 12.5,  # Note: float type
                "tariffFormula": "...",
                "tariffCalculateType": "..."
            }
        """
        # Handle TurtleClassify API response format (hscodeStr) or legacy format (hscodeInfo.hscode)
        hscode = data.get('hscodeStr', '')
        hscode_desc = data.get('hscodeDesc', '')
        
        # Fallback to legacy format if new fields not present
        if not hscode:
            hscode_info = data.get('hscodeInfo', {})
            hscode = hscode_info.get('hscode', '')
        
        # Always check hscodeInfo.descriptionEn if hscode_desc is empty
        if not hscode_desc:
            hscode_info = data.get('hscodeInfo', {})
            hscode_desc = hscode_info.get('descriptionEn', '')
        
        # Parse tariff rate - TurtleClassify returns string, legacy returns float
        tariff_rate_raw = data.get('tariffRate', 0)
        if isinstance(tariff_rate_raw, str):
            try:
                tariff_rate = float(tariff_rate_raw) if tariff_rate_raw else 0
            except ValueError:
                tariff_rate = 0
        else:
            tariff_rate = tariff_rate_raw if tariff_rate_raw else 0
        
        # Build tariff formula (not directly provided by TurtleClassify, construct from rate)
        tariff_formula = data.get('tariffFormula', '')
        if not tariff_formula:
            tariff_formula = f"Base Rate: {tariff_rate}%"
        
        # Ensure calculation type has a value (not provided by TurtleClassify)
        tariff_calc_type = data.get('tariffCalculateType', '')
        if not tariff_calc_type:
            tariff_calc_type = 'AD_VALOREM'
        
        # Get extend info from TurtleClassify response
        extend_info = data.get('extendInfo', '')
        
        return {
            'hsCode': hscode,
            'hsCodeDescription': hscode_desc,
            'tariffRate': tariff_rate,
            'tariffFormula': tariff_formula,
            'tariffCalculateType': tariff_calc_type,
            'extendInfo': extend_info,
            'originCountryCode': data.get('originCountryCode', product.get('originCountryCode', 'CN')),
            'destinationCountryCode': data.get('destinationCountryCode', product.get('destinationCountryCode', 'US')),
            'productName': data.get('productName', product.get('productName', 'Unknown Product')),
            'calculationDetails': data
        }
    
    def _validate_product(self, product: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate a single product object for TurtleClassify API.
        
        Required fields per TurtleClassifyDTO:
            - source: Product source info (defaults to 'alibaba')
            - originCountryCode: Origin country code
            - destinationCountryCode: Destination country code
            - productName: Product name
            
        Optional fields:
            - digit: HS code digit length (8 or 10)
            - productId, productSource, productCategoryId, productCategoryName
            - productProperties, productKeywords, channel
        """
        required_fields = {
            'originCountryCode': 'Origin country code',
            'destinationCountryCode': 'Destination country code',
            'productName': 'Product name'
        }
        
        for field, display_name in required_fields.items():
            if field not in product or not product[field]:
                return False, f"Missing required field: {display_name} ({field})"
        
        # digit is optional but if provided, must be 8 or 10
        digit = product.get('digit')
        if digit is not None:
            if not isinstance(digit, int) or digit not in [8, 10]:
                return False, f"digit must be 8 or 10, got: {digit}"
        
        # Set default source if not provided (required by TurtleClassify API)
        if 'source' not in product or not product['source']:
            product['source'] = 'alibaba'
        
        return True, ""
    
    def _call_restful_api(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call TurtleClassify RESTful API to get tariff classification
        
        API Endpoint: POST /api/turtle/classify
        
        Request payload (TurtleClassifyDTO):
            - source (required): Product source info, e.g., "alibaba"
            - originCountryCode (required): Origin country code, e.g., "CN"
            - destinationCountryCode (required): Destination country code, e.g., "US"
            - digit (optional): Expected HS code digit length (8 or 10)
            - productName (required): Product name
            - productId (optional): Product ID
            - productSource (optional): Product source
            - productCategoryId (optional): Product category ID
            - productCategoryName (optional): Product category name
            - productProperties (optional): Product properties dict
            - productKeywords (optional): Product keywords list
            - channel (optional): Channel
        
        Response structure:
            {
                "success": true,
                "msgCode": "200",
                "msgInfo": "ok",
                "data": "{\"success\":true,\"code\":\"200\",\"message\":\"success\",\"data\":{\"hscodeStr\":\"85171200\",\"hscodeDesc\":\"...\",\"tariffRate\":\"0\",\"extendInfo\":\"\"}}"
            }
        """
        endpoint = f"{self.base_url.rstrip('/')}/api/turtle/classify"
        
        # Build TurtleClassifyDTO payload (flat structure, not nested)
        payload = {
            'source': product.get('source', 'alibaba'),
            'originCountryCode': product.get('originCountryCode', 'CN'),
            'destinationCountryCode': product.get('destinationCountryCode', 'US'),
            'productName': product.get('productName', ''),
        }
        
        # Add optional fields if present
        if 'digit' in product and product['digit']:
            payload['digit'] = product['digit']
        if 'productId' in product and product['productId']:
            payload['productId'] = product['productId']
        if 'productSource' in product and product['productSource']:
            payload['productSource'] = product['productSource']
        if 'productCategoryId' in product and product['productCategoryId']:
            payload['productCategoryId'] = product['productCategoryId']
        if 'productCategoryName' in product and product['productCategoryName']:
            payload['productCategoryName'] = product['productCategoryName']
        if 'productProperties' in product and product['productProperties']:
            payload['productProperties'] = product['productProperties']
        if 'productKeywords' in product and product['productKeywords']:
            payload['productKeywords'] = product['productKeywords']
        if 'channel' in product and product['channel']:
            payload['channel'] = product['channel']
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(
                url=endpoint,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()
            
            # Check if the API call was successful
            if not result.get('success', False):
                error_code = result.get('msgCode', 'unknown')
                error_msg = result.get('msgInfo', 'Unknown error')
                print(f"[ERROR] TurtleClassify API returned error: {error_code} - {error_msg}")
                return {}
            
            # Parse the nested JSON in 'data' field
            # Note: API may return 'data' as either a JSON string or a dict object
            data_field = result.get('data', '')
            if data_field:
                try:
                    # Handle both string and dict formats
                    if isinstance(data_field, str):
                        inner_result = json.loads(data_field)
                    elif isinstance(data_field, dict):
                        inner_result = data_field
                    else:
                        print(f"[ERROR] Unexpected data field type: {type(data_field)}")
                        return {}
                    
                    if inner_result.get('success', False):
                        # Return in the expected format with 'data' key containing the classification result
                        return {
                            'data': inner_result.get('data', {}),
                            'raw_inner_response': inner_result
                        }
                    else:
                        inner_code = inner_result.get('code', 'unknown')
                        inner_msg = inner_result.get('message', 'Unknown error')
                        print(f"[ERROR] Inner API response error: {inner_code} - {inner_msg}")
                        return {}
                except json.JSONDecodeError as e:
                    print(f"[ERROR] Failed to parse inner JSON response: {e}")
                    return {}
            
            return {}
            
        except requests.exceptions.Timeout:
            print(f"[ERROR] TurtleClassify API call timed out after {self.timeout} seconds")
            return {}
        except requests.exceptions.ConnectionError as e:
            print(f"[ERROR] TurtleClassify API connection error: {e}")
            return {}
        except requests.exceptions.HTTPError as e:
            print(f"[ERROR] TurtleClassify API HTTP error: {e}")
            return {}
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] TurtleClassify API call failed: {e}")
            return {}
    
    def _format_single_result(self, data: Dict[str, Any], index: int = 1) -> str:
        """
        Format a single classification result.
        
        Handles both TurtleClassify API response format and legacy format.
        """
        output_lines = [f"Product {index} Classification Result:"]
        
        # Handle TurtleClassify format (hscodeStr, hscodeDesc) or legacy format (hscodeInfo)
        hscode = data.get('hscodeStr', '')
        hscode_desc = data.get('hscodeDesc', '')
        
        if not hscode:
            hscode_info = data.get('hscodeInfo', {})
            if hscode_info:
                hscode = hscode_info.get('hscode', 'N/A')
                hscode_desc = hscode_info.get('descriptionEn', 'N/A')
        
        if hscode:
            output_lines.append(f"  HS Code: {hscode}")
        if hscode_desc:
            output_lines.append(f"  Description: {hscode_desc}")
        
        tariff_rate = data.get('tariffRate', 'N/A')
        output_lines.append(f"  Total Tariff Rate: {tariff_rate}%")
        
        tariff_formula = data.get('tariffFormula', '')
        if tariff_formula:
            output_lines.append(f"  Tariff Formula: {tariff_formula}")
        
        tariff_type = data.get('tariffCalculateType', '')
        if tariff_type:
            output_lines.append(f"  Calculation Type: {tariff_type}")
        
        # Handle extend info from TurtleClassify
        extend_info = data.get('extendInfo', '')
        if extend_info:
            output_lines.append(f"  Extended Info: {extend_info}")
        
        # Handle legacy tariff details
        tariff_details = data.get('tariffCalRuleDetailList', [])
        if tariff_details:
            output_lines.append("  Tariff Breakdown:")
            for detail in tariff_details:
                tariff_desc = detail.get('tariffTypeDesc', 'Unknown')
                rate = detail.get('fixedRate', 0)
                hts_code = detail.get('htsCode', '')
                output_lines.append(f"    - {tariff_desc}: {rate}% (HTS: {hts_code})")
        
        return "\n".join(output_lines)
    
    def _format_output(self, response: Dict[str, Any]) -> str:
        """Format the response for consumption"""
        if not response:
            return "No tariff classification results returned."
        
        results = []
        data = response.get('data', {})
        
        if isinstance(data, list):
            for idx, item in enumerate(data):
                results.append(self._format_single_result(item, idx + 1))
        elif isinstance(data, dict):
            results.append(self._format_single_result(data, 1))
        
        return "\n\n".join(results) if results else json.dumps(response, ensure_ascii=False)
    
    def _process_single_product(self, product: Dict[str, Any], silent: bool = False) -> Dict[str, Any]:
        """
        Process a single product for tariff classification
        
        Args:
            product: Single product dictionary
            silent: If True, suppress info messages (useful for batch processing)
            
        Returns:
            Classification result dictionary
        """
        try:
            return self._call_restful_api(product)
        except Exception as e:
            import traceback
            print(f"[ERROR] Single product processing failed: {e}")
            traceback.print_exc()
            return {}
    
    def _process_single_product_with_delay(self, product: Dict[str, Any], delay: float, silent: bool = True) -> Dict[str, Any]:
        """Process single product with random delay to smooth QPS"""
        if delay > 0:
            time.sleep(delay)
        return self._process_single_product(product, silent)
    
    def _process_batch(self, products: List[Dict[str, Any]], batch_offset: int = 0, 
                       max_workers: int = 50, target_qps: float = 10.0) -> List[Dict[str, Any]]:
        """
        Process a single batch of products CONCURRENTLY with rate limiting
        
        Args:
            products: List of product dictionaries (should be <= MAX_BATCH_SIZE)
            batch_offset: Offset for logging purposes (index of first product in original list)
            max_workers: Maximum number of concurrent workers (default 50)
            target_qps: Target QPS limit (default 10), requests are spread with random delay
            
        Returns:
            List of classification results in the same order as input products
        """
        if not products:
            return []
        
        # 计算随机延迟范围，确保统计上 QPS 不超过 target_qps
        # 如果有 N 个请求要在 N/target_qps 秒内均匀分布发送
        # 每个请求的随机延迟范围是 [0, N/target_qps)
        n_products = len(products)
        max_delay = n_products / target_qps  # 例如 50 个请求, QPS=10, 则延迟范围 0-5 秒
        
        # 使用并发处理提升性能
        results = [None] * n_products  # 预分配结果列表，保持顺序
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任务，每个任务带随机延迟
            future_to_index = {}
            for i, product in enumerate(products):
                delay = random.uniform(0, max_delay)
                future = executor.submit(self._process_single_product_with_delay, product, delay, True)
                future_to_index[future] = i
            
            # 收集结果
            for future in as_completed(future_to_index):
                idx = future_to_index[future]
                try:
                    result = future.result()
                    results[idx] = result
                except Exception as e:
                    print(f"[ERROR] Product {batch_offset + idx + 1} failed: {e}")
                    results[idx] = {}
        
        return results
    
    def _process_products(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process multiple products with batch size limit (max MAX_BATCH_SIZE per batch)
        
        Args:
            products: List of product dictionaries
            
        Returns:
            List of classification results in the same order as input products
            (truncated to MAX_TOTAL_PRODUCTS if input exceeds limit)
        """
        if not products:
            return []
        
        total_count = len(products)
        
        # Truncate if exceeds maximum total products limit
        if total_count > self.MAX_TOTAL_PRODUCTS:
            print(f"[WARNING] Input contains {total_count} products, exceeding limit of {self.MAX_TOTAL_PRODUCTS}. Only processing first {self.MAX_TOTAL_PRODUCTS} products.")
            products = products[:self.MAX_TOTAL_PRODUCTS]
            total_count = self.MAX_TOTAL_PRODUCTS
        
        # If within batch limit, process directly
        if total_count <= self.MAX_BATCH_SIZE:
            return self._process_batch(products, batch_offset=0)
        
        # Process in batches of MAX_BATCH_SIZE
        all_results = []
        batch_count = (total_count + self.MAX_BATCH_SIZE - 1) // self.MAX_BATCH_SIZE
        
        print(f"[INFO] Processing {total_count} products in {batch_count} batches (max {self.MAX_BATCH_SIZE} per batch)")
        
        for batch_idx in range(batch_count):
            start_idx = batch_idx * self.MAX_BATCH_SIZE
            end_idx = min(start_idx + self.MAX_BATCH_SIZE, total_count)
            batch_products = products[start_idx:end_idx]
            
            print(f"[INFO] Processing batch {batch_idx + 1}/{batch_count} (products {start_idx + 1}-{end_idx})")
            
            batch_results = self._process_batch(batch_products, batch_offset=start_idx)
            all_results.extend(batch_results)
        
        return all_results
