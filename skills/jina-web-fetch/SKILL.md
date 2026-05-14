---
name: jina-web-fetch
description: Fetches web page content or searches keywords via curl using the Jina Reader API. Triggered when the user provides a URL to read web content, extract article text, or retrieve page information. Also supports keyword search to get relevant web summaries. Not suitable for scenarios requiring login, interactive operations, or binary file downloads.
---

# Jina Web Fetch

Converts web page content into clean Markdown text via curl using the Jina Reader API. Supports two modes: reading web content from a specified URL, and searching the web by keywords. Lightweight with no dependencies — only curl is required.

## When to Use

- User provides a URL and needs to read or summarize web content
- Need to extract article body, online documentation, or product page information
- Need to search keywords and get relevant web summaries
- Researching online articles or technical documentation

## When NOT to Use

- Requires login, clicking, form filling, or other interactive operations (consider browser automation)
- Downloading binary files (images, PDFs, etc.)
- API calls requiring complex authentication

## Environment Setup

Search mode (`s.jina.ai`) requires a Jina API Key. Ensure the environment variable is configured before use:

```bash
export JINA_API_KEY="jina_xxxxxxxxxxxx"
```

You can register at https://jina.ai/ to get a free API Key. Read mode (`r.jina.ai`) can be used without an API Key.

## Quick Reference

| Mode | Command | Description |
|------|---------|-------------|
| Read | `curl -s --max-time 30 "https://r.jina.ai/<URL>"` | Get web page Markdown content, no API Key required |
| Search | `curl -s -G --max-time 30 -H "X-Respond-With: no-content" -H "Authorization: Bearer $JINA_API_KEY" --data-urlencode "q=<keywords>" "https://s.jina.ai/"` | Search keywords, API Key required |

## Usage

### Reading Web Content

```bash
curl -s --max-time 30 "https://r.jina.ai/https://example.com/page"
```

The target URL must be a complete address (including `https://` or `http://`). Returns clean Markdown with navigation bars, ads, and other irrelevant content removed.

### Searching Keywords

Search keywords may contain special characters such as spaces or non-ASCII characters. You must use `--data-urlencode` to let curl handle URL encoding automatically, avoiding exit code 3 errors.

```bash
curl -s -G --max-time 30 \
  -H "X-Respond-With: no-content" \
  -H "Authorization: Bearer $JINA_API_KEY" \
  --data-urlencode "q=latest AI news 2025" \
  "https://s.jina.ai/"
```

Search uses `X-Respond-With: no-content` to strip the full web content from each result. It returns Markdown format by default, keeping only the title, URL, and description summary, significantly reducing the response size (from hundreds of KB down to a few KB).

To learn more about a specific result, use read mode to fetch its full content.

Before use, check whether the `JINA_API_KEY` environment variable is set. If not configured, prompt the user to set it first.

## Optional Parameters

Output behavior can be controlled via HTTP headers:

```bash
# JSON structured output (includes title, content, links fields)
curl -s -H "Accept: application/json" --max-time 30 "https://r.jina.ai/https://example.com"

# Preserve all hyperlinks on the page
curl -s -H "X-With-Links: true" --max-time 30 "https://r.jina.ai/https://example.com"

# Extract content from a specific CSS selector only
curl -s -H "X-Target-Selector: .article-body" --max-time 30 "https://r.jina.ai/https://example.com"
```

## Error Handling

If the returned content is empty, visibly incomplete, or curl returns a non-zero exit code, possible causes include:

- The target website requires login or relies on JavaScript rendering
- Jina service is temporarily unavailable
- Blocked by the target website's anti-scraping measures
- Search mode API Key is not configured or has expired

In such cases, inform the user that the fetch was unsuccessful and suggest: verifying the URL is correct, confirming the API Key configuration (for search mode), trying other available web reading methods, or considering browser automation tools when interaction is required.
