# Razorpay Cursor Plugins

Official Razorpay plugins for the [Cursor](https://cursor.com) plugin marketplace.
Each plugin connects Cursor to one of Razorpay's hosted MCP servers.

| Plugin | What it does | MCP endpoint |
|---|---|---|
| [Razorpay ACE Marketplace](plugins/razorpay-ace-marketplace/) | Shop across Indian D2C brands (Shopify, Fynd and more) and check out via Razorpay hosted checkout | `https://merchants.agent.razorpay.com/mcp` |
| [Razorpay](plugins/razorpay-remote-mcp-server/) | Work with your Razorpay account: payments, orders, refunds, payment links, settlements | `https://mcp.razorpay.com/mcp` |

## Repository layout

```
.cursor-plugin/marketplace.json       # lists every plugin in this repo
plugins/
  razorpay-ace-marketplace/
    .cursor-plugin/plugin.json        # plugin manifest
    mcp.json                          # MCP server URL
    assets/logo.svg
    README.md
  razorpay-remote-mcp-server/
    (same layout)
docs/add-a-plugin.md                  # how to add another plugin
scripts/validate-template.mjs         # Cursor's plugin-template validator (unchanged)
scripts/validate.py                   # extra MCP config checks: https, host allowlist, no inline secrets
.github/workflows/validate.yml        # both validators + gitleaks secret scan on every PR
.github/workflows/central_security_checks.yml  # Razorpay central security scan (PRs, master, nightly)
.github/workflows/rcore-integration.yml         # Razorpay code review integration
.github/CODEOWNERS                    # @razorpay/payments-ai-devs reviews every change
```

This follows Cursor's official multi-plugin template, [cursor/plugin-template](https://github.com/cursor/plugin-template).

## What this repo contains, and what it never contains

This repo is **configuration only**.

- **Contains:** plugin manifests, the public URLs of Razorpay's hosted MCP servers, READMEs and logos.
- **Never contains:** service source code, API keys, tokens, OAuth client secrets or any other credentials, internal hostnames, or customer and merchant data.

Authentication happens on the MCP servers themselves. The ACE Marketplace browsing and cart tools work without sign-in. Account-level actions sign the user in through Razorpay's OAuth flow at connect time. Nothing in these files carries a credential.

`scripts/validate.py` enforces this in CI. It rejects non-https URLs, any MCP host outside the allowlist (`merchants.agent.razorpay.com`, `mcp.razorpay.com`), inline auth headers, and undeclared `${VAR}` placeholders. Gitleaks scans the full git history on every PR and push.

## Adding a plugin

See [docs/add-a-plugin.md](docs/add-a-plugin.md). Before opening a PR, run:

```bash
node scripts/validate-template.mjs
python3 scripts/validate.py
```

## Install in Cursor

Once the plugins are listed, install them from the Cursor marketplace. To test locally before listing, point Cursor at a plugin folder, or add the server from the plugin's `mcp.json` under **Cursor Settings → MCP**.

## Security

See [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE)
