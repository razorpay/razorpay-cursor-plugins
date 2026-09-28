# Security

## Reporting a vulnerability

Please do **not** open a public GitHub issue for security problems.
Report them privately to Razorpay's security team through Razorpay's responsible disclosure channel.

<!-- TODO(security team): confirm the official disclosure contact / URL to publish here before the repo goes public. -->

## What this repo holds

Configuration only: plugin manifests, public MCP server URLs, READMEs and logos.
No source code, credentials, internal hostnames or customer data are ever committed here.

## Controls

- Every change goes through a pull request reviewed by `@razorpay/payments-ai-devs` (CODEOWNERS).
- `master` is protected: no direct pushes, at least one approving review, CI must pass.
- CI runs `scripts/validate.py` (https-only, allowlisted MCP hosts, no inline auth headers) and a gitleaks scan of the full history on every PR and push.
- GitHub secret scanning and push protection are enabled on the repository.
- Adding a new MCP host to the allowlist requires security review.
