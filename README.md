# Market Fiyatı MCP Server

[![PyPI version](https://img.shields.io/pypi/v/market-fiyati-mcp-server.svg)](https://pypi.org/project/market-fiyati-mcp-server/)
[![MCP Specification](https://img.shields.io/badge/spec-modelcontextprotocol.io-blue.svg)](https://spec.modelcontextprotocol.io)

An MCP server for [marketfiyati.org.tr](https://marketfiyati.org.tr/), a price comparison website for groceries in Turkey.

This server exposes the search functionality of the website as tools for MCP-compatible clients.

## Features

- **Search Products**: Find products using keywords.
- **Search by ID**: Look up products by their unique ID or barcode.
- **Find Similar Products**: Discover products similar to a given item.

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended for project and virtual environment management)

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/mtcnbzks/market-fiyati-mcp-server.git
    cd market-fiyati-mcp-server
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    uv venv
    uv sync
    ```

## Usage

You can run this server and connect to it from any MCP-compatible client.

### Running the Server

To start the server, run the following command in your terminal:

```bash
uv run python -m market_fiyati_mcp_server.server
```

The server will start and listen for connections from MCP clients.

### Connecting from a Client

You can use the MCP development tools to inspect and interact with the server.

- **Install in an MCP Client (e.g., Claude Desktop):**
  To make the server available in a client like the Claude Desktop App, you can install it using:

  ```bash
  uv run mcp install src/market_fiyati_mcp_server/server.py
  ```

- **Manual Configuration (e.g., VS Code):**
  To add the server to a client that uses a `mcp.json` configuration file (like VS Code), add the following to the `servers` object in your `mcp.json`.

  ```json
  {
    "servers": {
      "market-fiyati": {
        "command": "uvx",
        "args": ["market-fiyati-mcp-server"]
      }
    }
  }
  ```

## Tools

This server provides the following tools:

### `search_product`

Search for products matching given keywords.

- **Parameters:**
  - `keywords` (str): The search terms.
  - `latitude` (float, optional): Latitude for location-based search.
  - `longitude` (float, optional): Longitude for location-based search.
  - `distance` (int, optional): Radius in km for location-based search.
- **Returns:** A human-readable summary and the full structured API response.

### `search_product_by_identity`

Retrieve product information by a unique identity (e.g., barcode or internal ID).

- **Parameters:**
  - `identity` (str): The product's unique ID or barcode.
  - `identityType` (str, optional): The type of identity (`id` or `barcode`). Defaults to `id`.
  - `keywords` (str, optional): Optional keywords to refine the search.
  - `latitude` (float, optional): Latitude for location-based search.
  - `longitude` (float, optional): Longitude for location-based search.
  - `distance` (int, optional): Radius in km for location-based search.
- **Returns:** A summary of the found product and the full structured API response.

### `search_similar_products`

Find products similar to a reference item ID.

- **Parameters:**
  - `id` (str): The ID of the reference product.
  - `keywords` (str): Keywords to find similar products.
  - `latitude` (float, optional): Latitude for location-based search.
  - `longitude` (float, optional): Longitude for location-based search.
  - `distance` (int, optional): Radius in km for location-based search.
- **Returns:** A summary of the most similar product and the full structured API response.
