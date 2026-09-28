# Add a plugin

Plugins live under `plugins/` and are registered in `.cursor-plugin/marketplace.json`.

## 1. Create the plugin folder

```text
plugins/<plugin-name>/
  .cursor-plugin/plugin.json
  mcp.json
  assets/logo.svg
  README.md
```

`<plugin-name>` is lowercase kebab-case and must match `name` in `plugin.json`.

Example manifest:

```json
{
  "name": "razorpay-example",
  "displayName": "Razorpay Example",
  "version": "0.1.0",
  "description": "What this plugin does, in one or two sentences.",
  "author": { "name": "Razorpay" },
  "repository": "https://github.com/razorpay/razorpay-cursor-plugins",
  "license": "MIT",
  "keywords": ["Razorpay"],
  "logo": "assets/logo.svg"
}
```

## 2. Point it at a hosted MCP server

`mcp.json` holds only the public https URL of the server:

```json
{
  "mcpServers": {
    "razorpay-example": { "url": "https://mcp.razorpay.com/mcp" }
  }
}
```

Do not put API keys, tokens or auth headers here. Servers handle sign-in themselves (OAuth). If a new host is needed, add it to `ALLOWED_MCP_HOSTS` in `scripts/validate.py`. That change needs security review.

## 3. Register it

Append to `.cursor-plugin/marketplace.json`:

```json
{
  "name": "razorpay-example",
  "source": "./plugins/razorpay-example",
  "description": "Short description"
}
```

## 4. Validate and open a PR

```bash
node scripts/validate-template.mjs
python3 scripts/validate.py
```

CI runs both, plus a gitleaks secret scan. CODEOWNERS requests review from `@razorpay/payments-ai-devs`.
