---
name: create-website
description: |
  Website creation capabilities. Use when the user wants to create a new website from scratch.
  
  **Capabilities**:
  1. **Create Website** - Generate a complete HTML website directly from requirements
  
  **When to use**:
  - User requests to create a new website (e.g., "create a website for my business", "build a landing page")
  - Keywords: "create website", "build website", "design webpage", "创建网站"
enabled: true
---

# Create Website

This skill provides **creating new websites** capability by directly generating HTML files.

## ⚠️ Important Rules

1. **Direct HTML Generation**: Generate the complete HTML file directly without running any external scripts.

2. **Single File Output**: The output should be a single, self-contained HTML file with inline CSS and JavaScript.

3. **Modern and Responsive**: Use modern HTML5, CSS3, and ensure the website is responsive across different devices.

## Workflow

**Step 1: Analyze Requirements**

Understand the user's website requirements, including:
- Purpose (business, portfolio, landing page, etc.)
- Target audience
- Style preferences (modern, minimalist, colorful, professional, etc.)
- Content sections needed

**Step 2: Generate HTML File**

Create a complete, self-contained HTML file with:
- Semantic HTML5 structure
- Inline CSS for styling (or embedded `<style>` block)
- Responsive design (mobile-friendly)
- Modern UI/UX design
- Any necessary JavaScript (embedded `<script>` block)

**Step 3: Save and Deliver**

Save the generated HTML file to the workspace and provide the file path to the user.

## Output Format

The final deliverable is a **single HTML file** containing the complete website.

| Capability | Output |
|------------|--------|
| Create Website | Single `index.html` file with inline CSS/JS |

The HTML file should be:
- Self-contained (no external dependencies except CDN resources if needed)
- Well-commented and organized
- Ready to open in any browser

