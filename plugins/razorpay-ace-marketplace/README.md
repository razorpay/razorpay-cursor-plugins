# Razorpay ACE Marketplace

Shop across thousands of Indian D2C brands in one integration, across Shopify, Fynd and other commerce-platform stores. Browse, compare, add to cart, and check out via Razorpay's secure hosted checkout pages.

- **MCP endpoint:** `https://merchants.agent.razorpay.com/mcp`
- **Sign-in:** not needed to browse, build a cart or check out. Payment happens on Razorpay's hosted checkout page, not inside the agent.

## Tools

| Tool | Purpose |
|---|---|
| `search_products` | Search products across participating brands |
| `get_filter_options` | List the filters available for a search |
| `get_product_details` | Full details for one product |
| `add_to_cart` | Add an item to the cart |
| `remove_from_cart` | Remove an item |
| `update_cart_item` | Change quantity or variant |
| `view_cart` | Show the current cart |
| `clear_cart` | Empty the cart |
| `create_checkout` | Create a Razorpay hosted checkout link for the cart |
| `get_order_status` | Check the status of an order |

## Checkout flow

`search_products` → cart tools → `create_checkout` returns a hosted Razorpay checkout URL → the user pays on that page → `get_order_status`.

## Configuration

`mcp.json` holds only the public endpoint above. There are no keys, tokens or variables to set.
