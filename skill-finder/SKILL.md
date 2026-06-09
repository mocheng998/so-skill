---
name: skill-finder
description: Find, search, recommend, and install agent skills from the internal catalog, skills.sh, ClawHub, and SkillsMP — all in one place. **Install routing:** when the user gives an **exact skill name** (e.g., "装 pdf", "install image-prompt-guide", "帮我加 yuque 技能") AND the `skill` tool is in your available_tools, call `skill({action:"install", skill_id:"<name>"})` directly — no need to read this skill. Consult this skill when (a) the user's query is **fuzzy/descriptive** ("我需要一个发邮件的技能", "find me something for PDFs", "有没有能剪视频的"), so you must search the catalog first to resolve the query into a concrete skill_id; (b) the `skill` tool is NOT in your available_tools (use the bash fallback for internal install); (c) the `skill` tool returns SKILL_NOT_FOUND (skill is from an external source — skills.sh / ClawHub / SkillsMP); or (d) the user explicitly asks for discovery/search across platforms. Trigger phrases: "how do I do X", "find a skill for X", "is there a skill that can...", "search all platforms", "best skill for X", "what skill should I use for X", "该用什么skill", "有没有XX的skill", "帮我找skill", "推荐一个skill", or any expression of interest in discovering/choosing the right skill for a task.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["clawhub"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "clawhub",
              "bins": ["clawhub"],
              "label": "Install ClawHub CLI (npm)",
            },
          ],
      },
  }
always_apply: true
---

# Skill Finder

When a user asks to **find**, **search**, **discover**, or **install** agent skills — or says things like "how do I do X", "is there a skill for X", "can you do X" — use this skill to search across platforms, evaluate results, and install the best match.

## Available Platforms

| Platform | Best For | Search Method | Speed | Catalog Size | Auth |
|----------|----------|---------------|-------|-------------|------|
| **Internal Catalog** | Official/first-party skills, already vetted, instant install | Local file read | ⚡ Instant | ~60 | ❌ Not required |
| **skills.sh** | Open-source, workflow automation, quick install | CLI: `npx skills find` | ⚡ Fast | ~Thousands | ❌ Not required |
| **ClawHub** | Community-driven, version management, publishing | CLI: `clawhub search` | ⚡ Fast | Community | ⚠️ Optional |
| **SkillsMP** | Largest database, AI semantic search, niche/research | REST API | 🐢 5–15s | 283K+ | ✅ Required |

## Install Workflow (Read First)

The `skill` tool is the **preferred installer**. It handles internal-catalog
skills atomically, registers via the official pipeline, and writes
`skills.jsonc` correctly. This skill (skill-finder) is the **fallback** for
when `skill` is unavailable or the target isn't in the internal catalog.

### Decision flow when the user wants to install a skill

```
Step 0: Resolve user query → exact skill_id
  ├─ User gave a name that looks like a catalog id
  │  (single noun / kebab-case / matches the form of a skill name,
  │   e.g., "pdf", "image-prompt-guide", "yuque", "gmail-assistant")
  │  → use it directly as skill_id, go to Step A
  │
  └─ User gave a fuzzy / descriptive query
     (sentence with verb, vague need, e.g., "能处理 PDF 的", "发邮件的技能",
      "帮我找个能剪视频的")
     → search the internal catalog first (see Step 1.5 below), present
       candidates, let user pick → then proceed to Step A with the chosen id

Step A: Is `skill` listed in <available_tools>?
  ├─ YES → try: skill({ action: "install", skill_id: "<resolved-name>" })
  │           ├─ success → done. No need to read further.
  │           ├─ SKILL_NOT_FOUND → skill is not in internal catalog;
  │           │                    proceed to Step B for cross-source install
  │           └─ other error    → report to user; do NOT bypass with bash
  │
  └─ NO  → `skill` tool is not registered for this agent.
           Skip to Step B and use the bash flow even for internal skills.
           (See Method 5 below: "Internal Catalog Optimized ZIP — Fallback".)

Step B: Cross-source / fallback install via bash
  ├─ Internal catalog (Method 5)              ← when `skill` tool unavailable
  ├─ skills.sh           (Method 1 / 2)
  ├─ ClawHub             (Method 3)
  └─ SkillsMP → GitHub   (Method 4)
```

### How to tell whether the user gave a name or a fuzzy query

| User said | Branch | Reason |
|---|---|---|
| "帮我装 pdf 技能" | name | "pdf" matches a catalog id form |
| "install image-prompt-guide" | name | kebab-case skill id |
| "把 yuque 装上" | name | single noun, looks like a skill name |
| "我需要一个能处理 PDF 的技能" | fuzzy | descriptive, has verb "处理" |
| "找个发邮件的 skill" | fuzzy | "发邮件" is a behavior, not a name |
| "best skill for testing" | fuzzy | discovery query |
| "帮我找个能剪视频的" | fuzzy | descriptive need |

**When in doubt, do the catalog lookup first** — it's cheap (a single
`cat` + python parse) and avoids guessing wrong skill_id.

### Key rules

- **Never bypass `skill` with bash when `skill` is available** — bash flows
  duplicate logic and risk drifting from the official install pipeline.
- **External sources (skills.sh / ClawHub / SkillsMP) always go through
  the bash flow** — `skill` tool only knows the internal catalog.
- **Discovery (search) is independent of install** — even when the user only
  asks to "find" a skill, use the search strategies below; install only
  after they pick one.

## Decision Tree

### Step 1: Analyze User Query

**Specific platform requested:**
- "from internal" / "internal catalog" / "our skills" → search Internal Catalog only
- "from skills.sh" → search skills.sh only
- "from clawhub" → search ClawHub only
- "from skillsmp" → search SkillsMP only

**Otherwise → ALWAYS start with Internal Catalog (Step 1.5), then escalate if needed.**

### Step 1.5: Search Internal Skill Catalog (ALWAYS do this first)

The internal catalog contains all official/first-party skills — both installed and uninstalled. This is the fastest and most reliable source.

**How to search:**

```bash
# Read the local skills cache and search by keyword
cat ~/.accio/accounts/ACCOUNT_ID/skills/remote_skills_cache.json | \
  python3 -c "
import json, sys
query = 'USER_QUERY_KEYWORDS'.lower().split()
data = json.load(sys.stdin)
for s in data['skills']:
    text = (s['name'] + ' ' + s.get('description', '')).lower()
    if any(q in text for q in query):
        print(f\"  {s['name']}\")
        print(f\"    {s.get('description', 'No description')[:150]}\")
        print()
"
```

Replace `ACCOUNT_ID` with the actual account ID from the agent's skill directory path, and `USER_QUERY_KEYWORDS` with space-separated search terms derived from the user's query.

**After finding a match in the internal catalog:**

1. Check if the skill is already in `<available_skills>` in the system prompt:
   - If YES → tell the user it's already installed and enabled, and offer to use it directly
   - If NO → the skill needs to be installed. Tell the user you found a matching internal skill and what it does, then offer to install it

**To determine install status**, check if the skill directory exists locally:
```bash
# Check account-level skills
ls ~/.accio/accounts/ACCOUNT_ID/skills/SKILL_NAME/SKILL.md 2>/dev/null && echo "installed" || echo "not installed"

# Check agent-level skills
ls ~/.accio/accounts/ACCOUNT_ID/agents/AGENT_ID/agent-core/skills/SKILL_NAME/SKILL.md 2>/dev/null && echo "installed" || echo "not installed"
```

If the skill is not installed, **install it via the Install Workflow above**:

1. **Step A (preferred):** if `skill` is in `<available_tools>`, call:
   ```
   skill({ action: "install", skill_id: "SKILL_NAME" })
   ```
2. **Step B (fallback):** if `skill` is not available, or returns
   `SKILL_NOT_FOUND`, use Method 5 (Internal Catalog Optimized ZIP) at
   the bottom of this skill.

**If a good internal match is found → use it. Only proceed to external platforms if no suitable internal skill exists.**

### Step 2: Choose Search Strategy (External Platforms)

Only reach this step if the Internal Catalog search in Step 1.5 found no suitable match.

#### Environment Check (IMPORTANT)

Before searching external platforms, check if the required CLIs are installed. If missing, install them first:

```bash
# Check if clawhub is installed
clawhub -h >/dev/null 2>&1 || npm i -g clawhub
```

#### Strategy A: Single Platform (Fast — Default)

1. Run `npx skills find <query>`
2. If a good match is found → **pick the best match and install it directly** (do not ask for user confirmation; prefer official/popular packages)
3. If not found or poor match → proceed to Strategy B

**Example output from `npx skills find`:**
```
Install with npx skills add <owner/repo@skill>

vercel-labs/agent-skills@vercel-react-best-practices
└ https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
```

#### Strategy B: Multi-Platform Search (Comprehensive)

Use when Strategy A yields no/poor results, or user asks for "best" / "any" / "comprehensive" search, or query is specialized/niche.

Search all three platforms in parallel:

```bash
# Platform 1: skills.sh
npx skills find <query>

# Platform 2: ClawHub
clawhub search <query>

# Platform 3: SkillsMP (API)
SKILLSMP_API_KEY=$(grep SKILLSMP_API_KEY .env | cut -d '=' -f2 | tr -d '"')
curl -X GET "https://skillsmp.com/api/v1/skills/ai-search?q=<url-encoded-query>&limit=5" \
  -H "Authorization: Bearer $SKILLSMP_API_KEY" \
  -H "Accept: application/json"
```

Aggregate and deduplicate results by GitHub URL. Score by relevance, stars, and recent updates. Present:

```
Found X skills across 3 platforms:

From skills.sh (Y results):
- skill-name by author — description
  https://skills.sh/owner/repo/skill-name

From ClawHub (Z results):
- skill-name by author — description

From SkillsMP (W results):
- skill-name by author (score: 0.95, ⭐ 29)
  https://github.com/owner/repo
```

#### Strategy C: Retry with Alternative Keywords

If the first search returns no suitable results, try **alternative queries** — synonyms, broader/narrower terms. Retry up to **3 times total** with different queries per platform.

**Example:** if `npx skills find deploy` has no good match, try:
1. `npx skills find deployment`
2. `npx skills find ci-cd`

After 3 attempts across platforms with no suitable result:
1. Inform the user no existing skill was found
2. Offer to help with the task directly using general capabilities
3. Suggest creating a custom skill: `npx skills init my-skill`

## Common Skill Categories

When choosing search terms, consider these common categories:

| Category | Example Queries |
|----------|----------------|
| Web Development | react, nextjs, typescript, css, tailwind |
| Testing | testing, jest, playwright, e2e |
| DevOps | deploy, docker, kubernetes, ci-cd |
| Documentation | docs, readme, changelog, api-docs |
| Code Quality | review, lint, refactor, best-practices |
| Design | ui, ux, design-system, accessibility |
| Productivity | workflow, automation, git |
| Research | arxiv, papers, academic, analysis |
| E-commerce | shopify, product, marketing, sourcing |

**Tips:**
- Use specific keywords: "react testing" > "testing"
- Try alternative terms: "deploy" → "deployment" → "ci-cd"
- Check popular sources: `vercel-labs/agent-skills`, community agent skill repositories

## SkillsMP API Reference

### AI Semantic Search (recommended)

**Endpoint:** `GET https://skillsmp.com/api/v1/skills/ai-search`

| Parameter | Required | Description |
|-----------|----------|-------------|
| `q` | Yes | Natural language query (URL-encoded) |
| `limit` | No | Results to return (default 20, max 100) |

> **Note:** Keyword Search (`/skills/search`) is currently unstable (returns `INTERNAL_ERROR`). Always use AI search.

**Response format:**

```json
{
  "success": true,
  "data": {
    "data": [
      {
        "score": 0.9956,
        "skill": {
          "name": "arxiv-search",
          "author": "DeevsDeevs",
          "description": "Search arXiv preprints...",
          "githubUrl": "https://github.com/...",
          "skillUrl": "https://skillsmp.com/skills/...",
          "stars": 29,
          "updatedAt": 1770255689
        }
      }
    ]
  }
}
```

**Parse results with jq:**

```bash
curl -s "https://skillsmp.com/api/v1/skills/ai-search?q=arxiv+papers&limit=5" \
  -H "Authorization: Bearer $SKILLSMP_API_KEY" -H "Accept: application/json" \
  | jq -r '.data.data[] | "\(.skill.name) by \(.skill.author)\n  \(.skill.description[0:100])...\n  ⭐ \(.skill.stars) | \(.skill.githubUrl)\n"'
```

**Score interpretation:** > 0.95 excellent · 0.90–0.95 good · 0.85–0.90 fair · < 0.85 weak

**Rate limits:** 500 requests/day per key. Resets at midnight UTC. Headers: `X-RateLimit-Daily-Limit`, `X-RateLimit-Daily-Remaining`.

**Common errors:**

| Code | Status | Fix |
|------|--------|-----|
| `INVALID_API_KEY` | 401 | Check `.env` for correct key |
| `MISSING_QUERY` | 400 | Add `q` parameter |
| `DAILY_QUOTA_EXCEEDED` | 429 | Wait until midnight UTC |
| `INTERNAL_ERROR` | 500 | Use AI search instead of keyword search |

**API key setup:**
- Get key at: https://skillsmp.com/docs/api (format: `sk_live_skillsmp_xxx...`)
- Configure: `echo 'SKILLSMP_API_KEY="sk_live_skillsmp_xxx..."' >> .env`

**Troubleshooting:**
- Empty results → use descriptive natural language, try broader terms, combine multiple keywords
- No API key → guide user to https://skillsmp.com/docs/api to generate a free key

## Installation Guidelines

After finding a skill, install it to the **correct directory**.

### ⚠️ DO NOT manually edit skills.jsonc

The `skills.jsonc` file is managed automatically by the PC runtime.
To install a skill, only place the skill directory under the correct path.
The runtime will auto-discover and register it. Manual edits to `skills.jsonc`
will be overwritten and may corrupt the skill registry.

### Directory Structure

| Level | Path | Scope |
|-------|------|-------|
| **Agent-specific** (default) | `~/.accio/accounts/{accountId}/agents/{agentId}/agent-core/skills/` | Only this agent |
| **Account-shared** | `~/.accio/accounts/{accountId}/skills/` | All agents in the account |

**Default: Always install to the agent's own directory** unless the user explicitly asks for account-level/global installation.

### ⚠️ CRITICAL: npx skills add Creates Subdirectory

`npx skills add` will ALWAYS create a `.agents/skills/` subdirectory in the current directory. The loader expects skills exactly one level below `skills/`, so this nested path will fail to load. Always use the "Install + Move" method below.

### Recommended Installation Methods

#### Method 1: git clone (DEFAULT — Safest)

Best for repositories that represent a single skill.

```bash
cd ~/.accio/accounts/{accountId}/agents/{agentId}/agent-core/skills/
git clone --depth 1 https://github.com/<owner>/<repo>.git <skill-name>
```

#### Method 2: "Install + Move" (Best for Monorepos/Sub-skills)

Use when installing a specific sub-skill from a large monorepo via `npx skills add`.

```bash
cd ~/.accio/accounts/{accountId}/agents/{agentId}/agent-core/skills/
npx skills add <repo> --skill <name> -y
mv .agents/skills/<name> ./
rm -rf .agents
```

#### Method 3: clawhub install

Always use `--force` for non-interactive installations (e.g., in agents) to bypass "suspicious skill" prompts.

```bash
clawhub install <slug> --dir ~/.accio/accounts/{accountId}/agents/{agentId}/agent-core/skills/ --force
```

#### Method 4: SkillsMP → GitHub clone

Extract `githubUrl` from the SkillsMP API response, then use Method 1.

#### Method 5: Internal Catalog (Optimized ZIP) — FALLBACK only

> ⚠️ **Only use this when the `skill` tool is NOT available** in the
> agent's `<available_tools>`. When `skill` is available, always prefer:
>
>     skill({ action: "install", skill_id: "<bare-name>" })
>
> which is faster, atomic, and uses the official registration pipeline.
> See the "Install Workflow (Read First)" section near the top.

Bash flow for installing an internal-catalog skill when the `skill` tool
is not registered for this agent. Handles nested directory extraction in
a single command.

```bash
DIR="~/.accio/accounts/{accountId}/agents/{agentId}/agent-core/skills/{skillName}"
URL="OSS_URL_FROM_CACHE"
mkdir -p "$DIR" && curl -sL "$URL" -o /tmp/skill.zip && \
  unzip -q -o /tmp/skill.zip -d "$DIR" && \
  mv "$DIR"/{skillName}/* "$DIR"/ 2>/dev/null; \
  rmdir "$DIR"/{skillName} 2>/dev/null; \
  rm /tmp/skill.zip
```

### Account-Level Skills (Shared)

Only when user explicitly requests global/shared installation:
`~/.accio/accounts/{accountId}/skills/`

### Verification After Installation

```bash
# Verify skill directory exists directly under skills/
ls ~/.accio/accounts/{accountId}/agents/{agentId}/agent-core/skills/<skill-name>/

# Verify SKILL.md exists
cat ~/.accio/accounts/{accountId}/agents/{agentId}/agent-core/skills/<skill-name>/SKILL.md
```

## Platform CLI Quick Reference

### skills.sh (`npx skills`)

The Skills CLI is the package manager for the open agent skills ecosystem.

| Command | Description |
|---------|-------------|
| `npx skills find <query>` | Search for skills by keyword |
| `npx skills add <owner/repo@skill> -y` | Install a skill (requires move, see Method 2) |
| `npx skills check` | Check for skill updates |
| `npx skills update` | Update all installed skills |

Browse: https://skills.sh/

### ClawHub (`clawhub`)

| Command | Description |
|---------|-------------|
| `npm i -g clawhub` | Install ClawHub CLI (if missing) |
| `clawhub search <query>` | Search for skills |
| `clawhub install <slug> --force` | Install a skill (use --force for agents) |
| `clawhub install <slug> --version 1.2.3 --force` | Install a specific version |
| `clawhub update <skill> --force` | Update a single skill |
| `clawhub update --all --force` | Update all skills |
| `clawhub update --all --no-input --force` | Force update all skills (agent-safe) |
| `clawhub list` | List installed skills |
| `clawhub login` | Auth (needed for publishing or rate-limited ops) |
| `clawhub publish ./skill --slug my-skill --name "My Skill" --version 1.0.0` | Publish a skill |

- Default registry: https://clawhub.com (override with `CLAWHUB_REGISTRY` or `--registry`)
- Default workdir: cwd; install dir: `./skills` (override with `--workdir` / `--dir` / `CLAWHUB_WORKDIR`)

### SkillsMP (REST API)

- **Search**: See SkillsMP API Reference above
- **Auth**: Requires `SKILLSMP_API_KEY` — get from https://skillsmp.com/docs/api
- **Install**: Extract `githubUrl` from search results, then `git clone`
