---
name: org-structure-research
description: |
  Systematically research a company's organizational structure, build org charts,
  and create employee profiles per business line. Use when the user asks to
  "调研组织架构", "org chart", "组织架构图", "员工画像", "业务线/部门结构", or
  "research [company] team structure and key people".
triggers:
  - org structure
  - organizational structure
  - org chart
  - 组织架构
  - 员工画像
  - business line
  - team structure
  - company hierarchy
  - who works at
  - key people at
---

# Org Structure Research

Orchestrate end-to-end research of a company's organizational structure: company overview, leadership discovery, department identification, employee discovery, profile building, optional social-network mapping, and org-chart visualization.

## When to Use This Skill

- User asks to research a company's **org structure** or **org chart**
- User wants **employee profiles** per **business line** or department
- User asks "who are the key people at [company]" or "调研 [company] 的组织架构"
- Output should include: **company overview + department breakdown + key people + (optional) social graph + org chart diagram**

## Sub-Skills and Tools to Invoke

| Phase | Sub-Skill / Tool | Purpose |
|-------|------------------|---------|
| Company overview | `company-research` | Exa search: company metadata, funding, headcount, product lines |
| Leadership discovery | `people-search` | Exa `category: "people"`: CEO, CTO, VP, Director |
| Department identification | Web search + careers/job pages | Infer departments from job listings, About page, news |
| Employee discovery | `people-search`, Bright Data LinkedIn tools, browser-use | List employees by department/title |
| Employee profiling | Bright Data `web_data_linkedin_person_profile`, Twitter tools | Build per-person profile (role, background, social) |
| Social relationships | **`social-network-mapper`** | Mutual follows, interactions, graph visualization |
| Org chart | `excalidraw-diagram-generator` or `draw-io` | Visual org chart from hierarchy data |
| Report synthesis | `deep-research` methodology | Citations, confidence levels, structured report |

## Research SOP (Standard Operating Procedure)

### Phase 1: Clarify Scope

Before heavy tool use:

1. **Confirm company**: Legal name, common name, parent entity (e.g. Cursor → Anysphere).
2. **Confirm depth**: Overview only vs. full employee list vs. key people + profiles.
3. **Confirm outputs**: Org chart (yes/no), employee profiles (per department?), social graph (yes/no).
4. **Confirm constraints**: Public sources only; no auth-required LinkedIn unless user has browser/session.

### Phase 2: Company Overview

1. Run **company-research** (or equivalent Exa) with:
   - `query`: "[Company legal name] company overview funding employees"
   - `category`: "company" for discovery; then "news" for recent announcements.
2. Extract: company name, legal entity, estimated headcount, funding stage, main product lines, headquarters.
3. Note official careers/job URL and About/Team URL for later.

### Phase 3: Leadership & Department Discovery

1. **Leadership**:
   - **people-search** (Exa `category: "people"`): "[Company] CEO", "[Company] CTO", "[Company] VP Engineering", etc.
   - If available: Bright Data `web_data_linkedin_people_search` with company name + title filters (C-level, VP, Director).
2. **Departments / business lines**:
   - Infer from job listings (careers page or `web_data_linkedin_job_listings` for the company).
   - Infer from titles in people-search results (Engineering, Product, Research, Growth, G&A, etc.).
   - Cross-check with company blog, press, "team" or "about" pages.
3. Produce a **department list** and **leadership table** (name, title, department, source).

### Phase 4: Employee Discovery by Department

For each department (or for "key people" only if scope is limited):

1. **people-search**: "[Company] [Department] engineer" / "[Company] [Role]" with Exa `category: "people"`.
2. If available: Bright Data LinkedIn people search constrained by company + title keywords.
3. Optional: Twitter/X user search for "[Company]" or "[Product]" to find employees who mention the company.
4. Deduplicate by name/linkedin_id; attach department from title heuristics.

Output: **Employee list** with columns: name, inferred department, title, LinkedIn/Twitter/GitHub if found.

### Phase 5: Employee Profile Building

For each key person (or a sampled set per department):

1. **LinkedIn**: Bright Data `web_data_linkedin_person_profile` (or people-search summary) → experience, education, skills.
2. **Twitter/X**: If handle known, get profile + recent posts (via twitter-command-center or equivalent) → interests, public stance.
3. **GitHub**: If handle/name matches, optional scrape or search for repos/contributions.
4. **Merge** into a single **profile object** per person:

```yaml
name: "Full Name"
title: "Title at Company"
department: "Engineering | Product | ..."
sources:
  linkedin: "url or summary"
  twitter: "handle"
  github: "handle"
experience_highlights: []
education: []
skills_or_focus: []
social_summary: "1-2 lines from Twitter/bio"
```

### Phase 6: Social Relationship Mapping (Optional)

If user asked for "社交关系", "互关", "谁和谁互动", or "social graph":

1. Invoke **`social-network-mapper`** skill with:
   - **Seed people**: List of names + Twitter handles (and optionally GitHub) for key people.
   - **Goal**: "Map mutual follows and interactions among these people; identify clusters."
2. Use the mapper’s output (graph + clusters + summary) in the final report.

### Phase 7: Org Chart Visualization

1. Build **hierarchy data** from leadership + department structure:
   - Root: company name
   - Level 2: departments or top-level leads (e.g. CEO → CTO, VP Eng, VP Product)
   - Level 3: sub-teams or key individuals under each lead
2. Invoke **excalidraw-diagram-generator** (or draw-io) with a clear description:
   - "Organization chart: root [Company], children [Dept1], [Dept2], ...; under [Dept1] list [Person A], [Person B]..."
3. Save diagram as `[company]-org-chart-[date].excalidraw` (or .drawio) and reference in report.

### Phase 8: Synthesis & Report

1. **Structure**:
   - Executive summary (company + org at a glance)
   - Company overview (funding, size, product lines)
   - Organization structure (departments + key leads)
   - Employee profiles per business line (tables or cards)
   - Optional: Social graph summary (from social-network-mapper)
   - Org chart diagram (file link or embed)
   - Sources and limitations
2. **Quality**: Use **deep-research** style: cite sources, note confidence [HIGH/MEDIUM/LOW], state gaps (e.g. "LinkedIn auth-required data not used").

## Data Model Conventions

- **Company**: name, legal_name, headcount_estimate, funding_stage, product_lines, careers_url, about_url.
- **Department**: name, inferred_from (job_listings | titles | about_page), key_lead_name.
- **Person**: name, title, department, linkedin_url, twitter_handle, github_handle, profile_summary (from Phase 5).
- **Org chart**: tree of (node_name, node_type: company | department | person, children[]).

## Information Source Priority

1. **Official**: Company website (about, team, careers), press releases.
2. **Structured**: LinkedIn (public or Bright Data), Crunchbase.
3. **Social**: Twitter/X (profiles, mutual follows, interactions).
4. **Secondary**: News, blogs, GitHub — use for cross-check and enrichment.

When sources conflict (e.g. title or department), state both and label confidence.

## Cross-Validation and Inference Rules

- **Department from title**: "Software Engineer" → Engineering; "Product Manager" → Product; "Head of Growth" → Growth/Marketing; "Researcher" / "Research Scientist" → Research.
- **Deduplication**: Match by normalized name + company; prefer LinkedIn as canonical if present.
- **Missing data**: Clearly mark "unknown" or "inferred"; do not invent data.

## Error Handling

- **No company results**: Broaden query (legal name, parent company, product name).
- **No people results**: Try product name + "team", or company + "LinkedIn".
- **Auth-required LinkedIn**: Offer browser-use or manual export; otherwise rely on Exa/Bright Data public data only.
- **Rate limits**: Batch requests; use sub-agents/tasks for large people sets to keep main context small.

## Output Checklist

- [ ] Company overview with sources
- [ ] Department list and key leads
- [ ] Employee list (and optionally full profiles) per business line
- [ ] Optional: social graph summary + cluster description
- [ ] Org chart diagram file
- [ ] Final report with citations and confidence notes

## Related Skills

- **social-network-mapper** — Use for mutual follows, interactions, and graph visualization.
- **company-research** — Company-level Exa search.
- **people-search** — People discovery via Exa.
- **excalidraw-diagram-generator** — Org chart and diagram output.
- **deep-research** / **academic-deep-research** — Methodology for rigorous, cited reports.
