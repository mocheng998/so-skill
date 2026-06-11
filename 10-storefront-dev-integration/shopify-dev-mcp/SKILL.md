---
name: shopify-dev-mcp
description: >
  Search Shopify documentation, explore GraphQL schemas, and validate code for Admin/Storefront APIs, Liquid, and Polaris.
  Use when asked about Shopify API calls, schema details, webhook examples, or theme validation.
allowed-tools: [Bash]
---

# Shopify Dev MCP (@shopify/dev-mcp)

Connect to Shopify's development resources to search docs, explore API schemas, and build extensions. This skill prevents "hallucinations" by verifying code against live Shopify schemas and best practices.

## Supported APIs & Technologies
- **APIs**: Admin GraphQL, Storefront, Customer Account, Partner, Payment Apps.
- **Logic & UI**: Liquid, Functions, Polaris (Web Components), POS UI Extensions.

## Setup & Connection
If the `shopify-dev` MCP server is not yet connected or configured, call the `mcporter` skill to list, authenticate, or configure it using `mcporter list shopify-dev` or `mcporter auth shopify-dev`.

**🔧 Connection Best Practices (Based on Real-world Experience):**
1. **Prefer Manual Path over npx**: In restricted or server environments, `npx` may fail. It is safer to `npm install @shopify/dev-mcp` locally and point directly to the JS entry point.
2. **Absolute Pathing**: Use the absolute path to `node_modules/@shopify/dev-mcp/dist/index.js` in your MCP configuration to ensure the server starts reliably.
3. **Shell Quoting**: When calling tools via `mcporter call`, **always wrap the entire command in single quotes** (e.g., `'shopify-dev.tool(arg: "val")'`) to prevent the shell from misinterpreting parentheses or special characters.

**MCP Config (Reliable Template):**
```json
{
  "mcpServers": {
    "shopify-dev": {
      "command": "node",
      "args": ["/absolute/path/to/node_modules/@shopify/dev-mcp/dist/index.js"],
      "env": {
        "LIQUID_VALIDATION_MODE": "full"
      }
    }
  }
}
```
*Note: Use `LIQUID_VALIDATION_MODE: "full"` for entire theme directories or `"partial"` for self-contained Liquid codeblocks.*

## Detailed Capabilities

### 1. Learning & Context (`learn_shopify_api`)
**MANDATORY FIRST STEP**: Always start here. This tool "teaches" the agent how to use specific Shopify APIs (e.g., "admin", "storefront-graphql", "liquid", "polaris") and returns a `conversationId`. 
* **Critical Context**: You **must** provide this `conversationId` in every subsequent tool call (introspection, validation, search). Without it, the tools will lose their API version and technology context.

### 2. Documentation Search (`search_docs_chunks`, `fetch_full_docs`)
- Use **`search_docs_chunks`** for semantic search across all of `shopify.dev`.
- Use **`fetch_full_docs`** to retrieve complete documentation for a specific path.

### 3. Schema Introspection (`introspect_graphql_schema`)
Before writing any GraphQL query or mutation, use this tool to find valid types, fields, and arguments. 
* **Tip**: If a specific term (e.g., `captureSession`) returns no results, try broader terms like `capture` or `session`. The schema introspection is keyword-sensitive.

### 4. Real-time Validation
- **`validate_graphql_codeblocks`**: Checks your generated GraphQL against the live Shopify schema. 
  * **Note**: Pass parameters as objects (e.g., `codeblocks: [{content: "..."}]`) rather than simple string arrays if required by the tool schema.
- **`validate_component_codeblocks`**: Validates Polaris components and props.
- **`validate_theme`**: Runs a full "Theme Check" on a local directory to identify Liquid errors.

## Best Practices
1. **Initialize & Persist**: Call `learn_shopify_api` at the start and reuse the `conversationId` religiously.
2. **Single Quotes for CLI**: Always use `'shopify-dev.tool(...)'` syntax in shell environments.
3. **Schema over Memory**: Even if you think you know the schema, use `introspect_graphql_schema` to verify against the "latest" version.
4. **Validate Before Presenting**: Always run the relevant `validate_*` tool on any code block before presenting it to the user.

## Example Triggers
- "How do I create a product using the Admin API?"
- "What fields are available on the Order object?"
- "Show me an example of a webhook subscription."
- "How do I authenticate my Shopify app?"
- "What's the difference between Admin API and Storefront API?"
- "Build a new POS UI extension that shows product SKUs in the order details screen."
- "Debug this 'Field not found' error in Shopify GraphQL."
