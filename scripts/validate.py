#!/usr/bin/env python3
"""Validate the Cursor plugin marketplace in this repo.

Checks (fails CI on any error):
  * every JSON file parses
  * marketplace entries point to real plugin folders with a plugin.json
  * plugin names are unique, kebab-case, and match their folder
  * manifest paths are relative and stay inside the plugin folder
  * MCP servers use https and only hosts in ALLOWED_MCP_HOSTS
  * mcp.json carries no inline headers/env secrets; any ${VAR} is declared in `variables`
  * referenced logos exist
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
VAR_RE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")
ALLOWED_MCP_HOSTS = frozenset({"merchants.agent.razorpay.com", "mcp.razorpay.com"})
SECRET_HEADER_RE = re.compile(r"(authorization|token|secret|key|password|cookie)", re.I)


def load(path: Path, errors: list) -> dict:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: cannot parse JSON ({exc})")
        return {}


def safe_rel(value: str) -> bool:
    return not (value.startswith("/") or "://" in value or ".." in Path(value).parts)


def check_mcp(plugin_dir: Path, manifest: dict, errors: list) -> None:
    rel = manifest.get("mcpServers", "mcp.json")
    if not isinstance(rel, str):
        errors.append(f"{plugin_dir.name}: mcpServers must reference a file, not inline config")
        return
    cfg = load(plugin_dir / rel, errors)
    declared = set((manifest.get("variables") or {}).get("properties", {}))
    servers = cfg.get("mcpServers", {})
    if not servers:
        errors.append(f"{plugin_dir.name}/{rel}: no mcpServers defined")
    for sname, server in servers.items():
        url = server.get("url", "")
        parsed = urlparse(url)
        if parsed.scheme != "https":
            errors.append(f"{plugin_dir.name}/{sname}: url must be https ({url!r})")
        if parsed.hostname not in ALLOWED_MCP_HOSTS:
            errors.append(f"{plugin_dir.name}/{sname}: host {parsed.hostname!r} not in allowlist")
        for hname, hval in (server.get("headers") or {}).items():
            if SECRET_HEADER_RE.search(hname) and not VAR_RE.fullmatch(str(hval).replace("Bearer ", "")):
                errors.append(f"{plugin_dir.name}/{sname}: header {hname!r} looks like an inline secret")
        for var in VAR_RE.findall(json.dumps(server)):
            if var not in declared:
                errors.append(f"{plugin_dir.name}/{sname}: ${{{var}}} not declared in plugin variables")


def check_plugin(entry: dict, seen: set, errors: list) -> None:
    name, source = entry.get("name", ""), entry.get("source", "")
    if not NAME_RE.match(name):
        errors.append(f"marketplace: plugin name {name!r} is not kebab-case")
    if name in seen:
        errors.append(f"marketplace: duplicate plugin name {name!r}")
    seen.add(name)
    if not isinstance(source, str) or not safe_rel(source):
        errors.append(f"marketplace: {name}: source must be a relative path inside the repo")
        return
    plugin_dir = ROOT / source
    manifest_path = plugin_dir / ".cursor-plugin" / "plugin.json"
    if not manifest_path.is_file():
        errors.append(f"marketplace: {name}: missing {source}/.cursor-plugin/plugin.json")
        return
    manifest = load(manifest_path, errors)
    if manifest.get("name") != name:
        errors.append(f"{source}: plugin.json name {manifest.get('name')!r} != marketplace name {name!r}")
    if not manifest.get("description"):
        errors.append(f"{source}: plugin.json needs a description")
    for key in ("logo", "mcpServers", "rules", "skills", "agents", "commands", "hooks"):
        val = manifest.get(key)
        vals = val if isinstance(val, list) else [val]
        for v in vals:
            if isinstance(v, str) and not safe_rel(v):
                errors.append(f"{source}: {key} path {v!r} must be relative and inside the plugin")
    logo = manifest.get("logo")
    if isinstance(logo, str) and not (plugin_dir / logo).is_file():
        errors.append(f"{source}: logo {logo!r} not found")
    if not (plugin_dir / "README.md").is_file():
        errors.append(f"{source}: missing README.md")
    check_mcp(plugin_dir, manifest, errors)


def main() -> int:
    errors: list = []
    for path in ROOT.rglob("*.json"):
        if ".git" not in path.parts:
            load(path, errors)
    market = load(ROOT / ".cursor-plugin" / "marketplace.json", errors)
    if not NAME_RE.match(market.get("name", "")):
        errors.append("marketplace: name must be kebab-case")
    seen: set = set()
    for entry in market.get("plugins", []):
        check_plugin(entry, seen, errors)
    if errors:
        print("Validation failed:\n  - " + "\n  - ".join(errors))
        return 1
    print(f"OK: {len(seen)} plugins valid ({', '.join(sorted(seen))})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
