---
name: people-research
description: People research using Exa search. Finds LinkedIn profiles, professional backgrounds, experts, team members, and public bios across the web. Use when searching for people, finding experts, or looking up professional profiles.
context: fork
always_apply: true
---

# People Research

## Tool Selection (Critical)

Exa search is available via **MCP tools** — no API key needed. Use **`accio-mcp-cli`** to invoke them (see **mcp-tools** / **accio-mcp-cli** skills). To discover or verify tool names, run `accio-mcp-cli search exa` (or `accio-mcp-cli toolkit`) before `call`.

**Preferred tools (in order):**

1. **`exa_web_search_exa`** (via `accio-mcp-cli call`) — supports `category`, `livecrawl`, `type`, `numResults`. Best for people discovery with `category: "people"`.
2. **`web_search_exa`** (via `accio-mcp-cli call`) — supports `num_results`, `include_domains`, `exclude_domains`, `start_published_date`, `end_published_date`, `include_text`, `type`. Best for filtered/domain-scoped searches.
3. **`get_page_contents_exa`** — extract text/summary from profile URLs.
4. **`exa_answer`** — get a direct answer with source citations.

**Fallback:** If Exa tools are unavailable (e.g. connection error, tool not found), ask the user to provide an `EXA_API_KEY` environment variable and use the Exa REST API directly via `bash`/`curl`.

### Calling Convention

All Exa MCP tools are invoked with `accio-mcp-cli call`. Prefer `--json` for nested or camelCase parameters:

```bash
accio-mcp-cli call exa_web_search_exa \
  --json '{"query":"...","numResults":20,"type":"auto","category":"people"}'
```

## Token Isolation (Critical)

Never run Exa searches in main context. Always spawn Task agents:
- Agent runs Exa search internally
- Agent processes results using LLM intelligence
- Agent returns only distilled output (compact JSON or brief markdown)
- Main context stays clean regardless of search volume

## Dynamic Tuning

No hardcoded numResults. Tune to user intent:
- User says "a few" → 10-20
- User says "comprehensive" → 50-100
- User specifies number → match it
- Ambiguous? Ask: "How many profiles would you like?"

## Query Variation

Exa returns different results for different phrasings. For coverage:
- Generate 2-3 query variations
- Run in parallel
- Merge and deduplicate

## Categories

Use appropriate Exa `category` (via `exa_web_search_exa`) depending on what you need:
- `people` → LinkedIn profiles, public bios (primary for discovery)
- `personal site` → personal blogs, portfolio sites, about pages
- `news` → press mentions, interviews, speaker bios
- No category (`type: "auto"`) → general web results, broader context

Start with `category: "people"` for profile discovery, then use other categories or no category with `livecrawl: "fallback"` for deeper research on specific individuals.

### Category-Specific Filter Restrictions

When using `category: "people"`, these parameters cause errors:
- `startPublishedDate` / `endPublishedDate`
- `startCrawlDate` / `endCrawlDate`
- `includeText` / `excludeText`
- `excludeDomains`
- `includeDomains` — **LinkedIn domains only** (e.g., "linkedin.com")

When searching without a category, all parameters are available (but `includeText`/`excludeText` still only support single-item arrays).

## LinkedIn

Public LinkedIn via Exa: `category: "people"`, no other filters.
Auth-required LinkedIn → use browser automation fallback.

## Browser Fallback

Auto-fallback to browser automation when:
- Exa returns insufficient results
- Content is auth-gated
- Dynamic pages need JavaScript

## Examples

### Discovery: find people by role
```bash
accio-mcp-cli call exa_web_search_exa \
  --json '{"query":"VP Engineering AI infrastructure","category":"people","numResults":20,"type":"auto"}'
```

### Deep dive: research a specific person
```bash
accio-mcp-cli call web_search_exa \
  --json '{"query":"Dario Amodei Anthropic CEO background","type":"auto","num_results":15}'
```

### News mentions
```bash
accio-mcp-cli call web_search_exa \
  --json '{"query":"Dario Amodei interview","num_results":10,"start_published_date":"2024-01-01"}'
```

### Extract profile content
```bash
accio-mcp-cli call get_page_contents_exa \
  --json '{"urls":["https://linkedin.com/in/example"],"text":true,"summary":true}'
```

### Direct answer about a person
```bash
accio-mcp-cli call exa_answer \
  --json '{"query":"Who is Dario Amodei and what is his background?","text":true}'
```

## Output Format

Return:
1) Results (name, title, company, location if available)
2) Sources (Profile URLs)
3) Notes (profile completeness, verification status)
