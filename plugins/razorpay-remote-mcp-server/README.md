# Razorpay (Remote MCP Server)

Razorpay's official hosted MCP server. Work with your Razorpay account from Cursor: create and track payments, orders, refunds, payment links, QR codes and settlements.

- **MCP endpoint:** `https://mcp.razorpay.com/mcp`
- **Sign-in:** Cursor opens Razorpay's OAuth sign-in when you first connect. Access is limited to what your Razorpay account allows. No API keys are stored in this plugin.
- **Source:** the server is open source at [razorpay/razorpay-mcp-server](https://github.com/razorpay/razorpay-mcp-server), which also lists the full set of tools.

## Configuration

`mcp.json` holds only the public endpoint above. There are no keys, tokens or variables to set in this plugin.
