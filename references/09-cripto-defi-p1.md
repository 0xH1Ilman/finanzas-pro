# 09-cripto-defi — parte 1

Skills de terceros agrupadas por tema. Cada sección indica fuente, licencia y dónde está su código.



---

## SKILL: crypto-tax-export

- Fuente: `agiprolabs/claude-trading-skills` → `skills/crypto-tax-export` (MIT)
- Cuándo usarla: Export trade history and tax calculations in formats compatible with Koinly, CoinTracker, CoinLedger, TokenTax, and IRS Form 8949
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/crypto-tax-export/` (demo_cointracker_export.csv, demo_form_8949.csv, demo_koinly_export.csv, tax_exporter.py)

# Crypto Tax Export

Export trade history and tax calculations for tax software and IRS filing. Handles Solana-specific transaction types (Jupiter swaps, LP operations, staking rewards, airdrops) and generates CSVs compatible with Koinly, CoinTracker, CoinLedger, TokenTax, TurboTax/TaxAct, and IRS Form 8949.

> **Disclaimer:** This skill provides data formatting and calculation tools only. It does not constitute tax advice. Consult a qualified tax professional for guidance on reporting cryptocurrency transactions. Tax laws vary by jurisdiction and change frequently.

## Prerequisites

- Python 3.10+
- Trade history data (from internal trade journal, on-chain history, or exchange exports)
- For on-chain reconciliation: Solana RPC or Helius API access (see `helius-api` skill)
- For cost basis: historical price data (see `birdeye-api` or `coingecko-api` skills)

## Capabilities

| Capability | Description |
|---|---|
| Multi-format CSV export | Koinly, CoinTracker, CoinLedger, TokenTax, TurboTax, TaxAct |
| IRS Form 8949 generation | Part I (short-term) and Part II (long-term), columns a through h |
| Solana tx classification | Jupiter swaps, multi-hop routes, LP deposits/withdrawals, staking, airdrops |
| Cost basis methods | FIFO, LIFO, HIFO, Specific Identification |
| Reconciliation | Match on-chain history against internal trade journal |
| Failed tx handling | Identify and exclude failed transactions (no taxable event) |

## Supported Export Formats

### Koinly CSV

Koinly expects a universal import format with these columns:

```
Date,Sent Amount,Sent Currency,Received Amount,Received Currency,Fee Amount,Fee Currency,Net Worth Amount,Net Worth Currency,Label,Description,TxHash
```

Labels: `swap`, `staking`, `airdrop`, `liquidity_in`, `liquidity_out`, `cost`, `gift`, `lost`.

### CoinTracker CSV

```
Date,Received Quantity,Received Currency,Sent Quantity,Sent Currency,Fee Amount,Fee Currency,Tag
```

Tags: `trade`, `staking_reward`, `airdrop`, `lp_deposit`, `lp_withdrawal`.

### CoinLedger CSV

```
Date (UTC),Type,Received Currency,Received Amount,Sent Currency,Sent Amount,Fee Currency,Fee Amount,Exchange/Wallet
```

Types: `Trade`, `Income`, `Gift Received`, `Mining`, `Staking Reward`, `Airdrop`.

### TokenTax CSV

```
Type,BuyAmount,BuyCurrency,SellAmount,SellCurrency,FeeAmount,FeeCurrency,Exchange,Group,Comment,Date
```

Types: `Trade`, `Income`, `Staking`, `Airdrop`, `Spending`.

### TurboTax / TaxAct CSV

Both accept a simplified Form 8949 format:

```
Description of Property,Date Acquired,Date Sold,Proceeds,Cost Basis,Gain or Loss
```

### IRS Form 8949

Part I — Short-term (held one year or less). Part II — Long-term (held more than one year).

Columns:
- **(a)** Description of property (e.g., "2.5 SOL")
- **(b)** Date acquired (MM/DD/YYYY)
- **(c)** Date sold or disposed of (MM/DD/YYYY)
- **(d)** Proceeds (sale price in USD)
- **(e)** Cost or other basis (purchase price in USD + fees)
- **(f)** Code, if any (per IRS instructions)
- **(g)** Adjustment amount
- **(h)** Gain or loss (d minus e, adjusted by g)

Check box: **(A)** if basis reported to IRS, **(B)** if not, **(C)** if Form 1099-B not received.

## Solana Transaction Classification

### Jupiter Swaps (Single-Hop)

A direct token-to-token swap. Classified as a **disposal** of the sent token and **acquisition** of the received token. Each side is a taxable event.

```python
tx = {
    "type": "swap",
    "sent": {"amount": 1.5, "currency": "SOL", "usd_value": 225.00},
    "received": {"amount": 50000, "currency": "BONK", "usd_value": 224.50},
    "fee": {"amount": 0.000005, "currency": "SOL", "usd_value": 0.00075},
    "timestamp": "2025-03-15T14:30:00Z",
    "tx_hash": "5abc...def",
}
```

### Jupiter Swaps (Multi-Hop)

A routed swap through intermediate tokens (e.g., SOL -> USDC -> BONK). Only the **initial send** and **final receive** matter for tax purposes. Intermediate hops are not separate taxable events.

### LP Deposits / Withdrawals

- **Deposit**: Sending tokens to an LP is generally treated as a disposal at fair market value.
- **Withdrawal**: Receiving tokens from an LP is an acquisition at fair market value.
- LP tokens received/burned may be tracked for cost basis continuity.

### Staking Rewards

Staking rewards (SOL validator rewards, liquid staking yield) are **income** at fair market value when received. Cost basis equals the FMV at receipt.

### Airdrops

Airdrops are **income** at fair market value when the recipient gains dominion and control. Some jurisdictions differ on when dominion is established.

### Token Migrations

A 1:1 token migration (e.g., protocol upgrade) is generally **not** a taxable event. The new token inherits the cost basis and holding period of the old token.

### Failed Transactions

Failed Solana transactions (status: failed, or inner instruction errors) are **not** taxable events. The transaction fee (SOL) may still be deductible as a cost of doing business in some jurisdictions. Always exclude failed txs from trade export.

## Cost Basis Methods

```python
from enum import Enum

class CostBasisMethod(Enum):
    FIFO = "fifo"      # First In, First Out (IRS default)
    LIFO = "lifo"      # Last In, First Out
    HIFO = "hifo"      # Highest In, First Out (minimizes gains)
    SPEC_ID = "spec_id" # Specific Identification (requires lot tracking)

def compute_gain(
    proceeds: float,
    cost_basis: float,
    adjustments: float = 0.0,
) -> float:
    """Compute gain or loss for Form 8949 column (h)."""
    return proceeds - cost_basis + adjustments
```

## Reconciliation

Reconciling on-chain history with an internal trade journal catches:

1. **Missing trades** — on-chain tx not in journal (manual entry missed)
2. **Phantom trades** — journal entry with no matching on-chain tx
3. **Amount mismatches** — journal amount differs from on-chain amount
4. **Duplicate entries** — same tx recorded twice

Reconciliation workflow:

```python
def reconcile(
    journal_trades: list[dict],
    onchain_txs: list[dict],
    tolerance: float = 0.001,
) -> dict:
    """Match journal entries to on-chain transactions.

    Args:
        journal_trades: Internal trade records with tx_hash field.
        onchain_txs: Parsed on-chain transactions.
        tolerance: Relative tolerance for amount matching.

    Returns:
        Dict with matched, missing_onchain, missing_journal,
        mismatched lists.
    """
    onchain_by_hash = {tx["tx_hash"]: tx for tx in onchain_txs}
    matched, missing_onchain, missing_journal, mismatched = [], [], [], []

    for trade in journal_trades:
        tx = onchain_by_hash.pop(trade.get("tx_hash", ""), None)
        if tx is None:
            missing_onchain.append(trade)
        elif abs(trade["amount"] - tx["amount"]) / max(tx["amount"], 1e-9) > tolerance:
            mismatched.append({"journal": trade, "onchain": tx})
        else:
            matched.append({"journal": trade, "onchain": tx})

    missing_journal = list(onchain_by_hash.values())

    return {
        "matched": matched,
        "missing_onchain": missing_onchain,
        "missing_journal": missing_journal,
        "mismatched": mismatched,
        "summary": {
            "total_journal": len(journal_trades),
            "total_onchain": len(onchain_txs),
            "matched": len(matched),
            "missing_onchain": len(missing_onchain),
            "missing_journal": len(missing_journal),
            "mismatched": len(mismatched),
        },
    }
```

## Quick Start

```python
from scripts.tax_exporter import (
    generate_demo_trades,
    export_koinly_csv,
    export_form_8949_csv,
)

# Generate sample trades
trades = generate_demo_trades()

# Export to Koinly format
export_koinly_csv(trades, "koinly_import.csv")

# Export to Form 8949 format
export_form_8949_csv(trades, "form_8949.csv")
```

Run the demo directly:

```bash
python scripts/tax_exporter.py --demo
```

## Use Cases

### End-of-Year Tax Filing
Export all trades from your journal, reconcile with on-chain history, generate Form 8949 line items, and import into TurboTax or hand to your CPA.

### Tax-Loss Harvesting Review
Export with HIFO cost basis method to identify positions with unrealized losses that could offset gains before year-end.

### Multi-Platform Consolidation
Combine trades from multiple wallets and DEXs into a single Koinly or CoinTracker import file for unified portfolio tax reporting.

### Audit Preparation
Use reconciliation to verify completeness of your trade records against on-chain history. Produce a clean Form 8949 with supporting transaction hashes.

## Files

| File | Description |
|---|---|
| `references/planned_features.md` | Export format specs, Form 8949 mapping, Solana tx classification, reconciliation methodology |
| `scripts/tax_exporter.py` | Demo script: generate trades, export to Koinly CSV and Form 8949 CSV, show format differences |

## Related Skills

- `helius-api` — Fetch and parse Solana transaction history for reconciliation
- `birdeye-api` / `coingecko-api` — Historical price data for cost basis lookups
- `solana-onchain` — Wallet transaction analysis and classification
- `trade-journal` — Internal trade record keeping

### Referencia: references/planned_features.md

# Crypto Tax Export — Planned Features Reference

## Export Format Specifications

### Koinly Universal CSV

Koinly accepts a universal CSV format for importing transactions from any source.

**Required columns:**
- `Date` — ISO 8601 or `YYYY-MM-DD HH:MM:SS UTC`
- `Sent Amount` — quantity sent (blank for income)
- `Sent Currency` — ticker symbol
- `Received Amount` — quantity received (blank for disposal-only)
- `Received Currency` — ticker symbol

**Optional columns:**
- `Fee Amount` / `Fee Currency` — transaction fee
- `Net Worth Amount` / `Net Worth Currency` — USD value at time of tx (helps Koinly price lookups)
- `Label` — transaction classification
- `Description` — free text note
- `TxHash` — on-chain transaction signature

**Koinly labels:** `swap`, `staking`, `airdrop`, `liquidity_in`, `liquidity_out`, `cost`, `gift`, `lost`, `fork`, `margin_fee`, `realized_gain`.

**Notes:**
- For swaps, populate both Sent and Received columns.
- For income (staking, airdrops), populate only Received columns.
- For expenses/losses, populate only Sent columns.
- Koinly auto-detects duplicates by TxHash.

### CoinTracker CSV

**Columns:** `Date`, `Received Quantity`, `Received Currency`, `Sent Quantity`, `Sent Currency`, `Fee Amount`, `Fee Currency`, `Tag`.

**Tags:** `trade`, `staking_reward`, `airdrop`, `lp_deposit`, `lp_withdrawal`, `payment`, `gift`.

**Date format:** `MM/DD/YYYY HH:MM:SS` (US format).

**Notes:**
- CoinTracker uses tags to classify income vs trades.
- Fees should be in the same currency as the sent side when possible.

### CoinLedger CSV

**Columns:** `Date (UTC)`, `Type`, `Received Currency`, `Received Amount`, `Sent Currency`, `Sent Amount`, `Fee Currency`, `Fee Amount`, `Exchange/Wallet`.

**Types:** `Trade`, `Income`, `Gift Received`, `Mining`, `Staking Reward`, `Airdrop`, `Spending`, `Lost/Stolen`.

**Date format:** `YYYY-MM-DD HH:MM:SS`.

**Notes:**
- The `Exchange/Wallet` field should identify the source (e.g., "Jupiter", "Raydium", "Phantom Wallet").
- CoinLedger pairs each trade row into buy/sell internally.

### TokenTax CSV

**Columns:** `Type`, `BuyAmount`, `BuyCurrency`, `SellAmount`, `SellCurrency`, `FeeAmount`, `FeeCurrency`, `Exchange`, `Group`, `Comment`, `Date`.

**Types:** `Trade`, `Income`, `Staking`, `Airdrop`, `Spending`, `Gift`, `Lost`, `Mining`.

**Date format:** `YYYY-MM-DD HH:MM:SS UTC`.

**Group field:** Optional grouping label for related transactions.

### TurboTax / TaxAct CSV

Both accept a simplified Form 8949-style CSV.

**Columns:** `Description of Property`, `Date Acquired`, `Date Sold`, `Proceeds`, `Cost Basis`, `Gain or Loss`.

**Date format:** `MM/DD/YYYY`.

**Notes:**
- Proceeds and Cost Basis are in USD.
- Gain or Loss = Proceeds - Cost Basis.
- Short-term and long-term should be in separate sections or files.

## Form 8949 Field Mapping

### Column Definitions

| Column | Field | Source | Notes |
|---|---|---|---|
| (a) | Description of property | `"{amount} {currency}"` | e.g., "2.5 SOL" |
| (b) | Date acquired | Trade journal / on-chain timestamp | MM/DD/YYYY |
| (c) | Date sold or disposed of | Disposal timestamp | MM/DD/YYYY |
| (d) | Proceeds | USD value at disposal | Sale price minus exchange fees |
| (e) | Cost or other basis | USD value at acquisition | Purchase price plus fees |
| (f) | Code | IRS code if applicable | Usually blank for crypto |
| (g) | Adjustment amount | Wash sale or other adjustments | Usually 0 |
| (h) | Gain or loss | `(d) - (e) + (g)` | Negative = loss |

### Check Box Rules

- **(A)** Basis reported to IRS — Rarely applies to crypto (no 1099-B from DEXs).
- **(B)** Basis NOT reported to IRS — Most common for DEX trades.
- **(C)** Form 1099-B not received — Use when no 1099-B was issued.

### Part I vs Part II

- **Part I** — Short-term: acquired and disposed within 365 days.
- **Part II** — Long-term: held for more than 365 days.
- Holding period starts the day after acquisition.

## Solana Transaction Type Classification

### Classification Rules

| Tx Pattern | Tax Type | Sent | Received | Label |
|---|---|---|---|---|
| Jupiter swap (single-hop) | Trade | Input token | Output token | swap |
| Jupiter swap (multi-hop) | Trade | First input | Final output | swap |
| LP deposit (add liquidity) | Disposal | Token A + Token B | LP token | liquidity_in |
| LP withdrawal (remove liquidity) | Acquisition | LP token | Token A + Token B | liquidity_out |
| Staking reward claim | Income | — | Reward token | staking |
| Airdrop receipt | Income | — | Airdrop token | airdrop |
| Token migration (1:1) | Non-taxable | Old token | New token | migration |
| Failed transaction | Non-taxable | — | — | (exclude) |
| NFT purchase | Trade | SOL/token | NFT | swap |
| Rent recovery (account close) | Non-taxable | — | SOL (rent) | cost |

### Multi-Hop Swap Handling

Jupiter routes through intermediate tokens for better pricing. For tax:
1. Parse the swap instruction to find the initial input and final output.
2. Ignore intermediate token transfers within the same transaction.
3. Record as a single trade: input token -> output token.
4. Transaction fee is the SOL fee on the outer transaction.

### Identifying Failed Transactions

A Solana transaction is failed if:
- `meta.err` is not `null` in the transaction response.
- The transaction status is `Err`.
- Inner instructions may have executed partially but the overall tx reverted.

Failed transactions still consume SOL for fees. The fee is **not** automatically deductible but may be claimed as a business expense if trading is a business activity.

## Reconciliation Methodology

### Step 1: Collect Sources

- **Journal trades**: Internal records with timestamps, amounts, tx hashes.
- **On-chain history**: Fetched via Helius `getSignaturesForAddress` + parsed transactions.

### Step 2: Primary Match (by tx hash)

Match journal entries to on-chain transactions by `tx_hash` / signature. This is the strongest match.

### Step 3: Secondary Match (by timestamp + amount)

For journal entries without tx hashes, attempt fuzzy matching:
- Timestamp within 60-second window.
- Amount within 0.1% relative tolerance.
- Same token pair.

### Step 4: Classify Unmatched

- **Journal-only entries**: Potentially from off-chain venues (CEX) or manual errors.
- **On-chain-only entries**: Missed journal entries — need to be added.
- **Amount mismatches**: Possible slippage discrepancies or partial fills.

### Step 5: Generate Report

Output a reconciliation report with:
- Match rate percentage.
- List of unmatched entries with suggested actions.
- List of mismatched amounts with differences.
- Summary statistics (total trades, total volume, date range).

## Planned Enhancements

- **Wash sale detection**: Flag disposals where the same or substantially identical asset was repurchased within 30 days (note: IRS has not issued definitive guidance on wash sale rules for crypto as of 2025, but proposed regulations may apply starting 2026).
- **Multi-wallet aggregation**: Combine exports across multiple Solana wallets into a single tax report.
- **CEX import parsing**: Ingest CSVs from Coinbase, Kraken, Binance and merge with on-chain data.
- **Lot tracking UI**: Visual tool for specific identification lot selection.
- **Schedule D summary**: Auto-generate Schedule D totals from Form 8949 line items.
- **International formats**: Support for HMRC (UK), ATO (Australia), CRA (Canada) reporting requirements.


---

## SKILL: defillama-api

- Fuente: `agiprolabs/claude-trading-skills` → `skills/defillama-api` (MIT)
- Cuándo usarla: Free DeFi analytics across all chains — TVL, token prices, DEX volumes, fees/revenue, stablecoins, and bridges
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/defillama-api/` (defi_snapshot.py, price_lookup.py)

# DeFiLlama API — DeFi Macro Analytics

DeFiLlama is the largest DeFi TVL aggregator. Its API is **free with no authentication** for most endpoints — covering TVL, token prices, DEX volumes, fees/revenue, stablecoins, and bridges across all chains.

## Quick Start

```python
import httpx

# No auth required for free endpoints
BASE = "https://api.llama.fi"
COINS = "https://coins.llama.fi"

# Current TVL for a protocol
tvl = httpx.get(f"{BASE}/tvl/raydium").json()
print(f"Raydium TVL: ${tvl:,.0f}")

# Token prices (multi-chain)
resp = httpx.get(f"{COINS}/prices/current/solana:So11111111111111111111111111111111111111112")
sol_price = resp.json()["coins"]["solana:So11111111111111111111111111111111111111112"]["price"]
```

## Base URLs

| Service | Base URL | Auth |
|---------|----------|------|
| TVL / Protocols | `https://api.llama.fi` | Free |
| Coin Prices | `https://coins.llama.fi` | Free |
| Stablecoins | `https://stablecoins.llama.fi` | Free |
| Yields | `https://yields.llama.fi` | Pro ($300/mo) |
| Bridges | `https://bridges.llama.fi` | Free (list) / Pro (detail) |
| Pro API | `https://pro-api.llama.fi/{KEY}/api/...` | Pro key in URL path |

**Rate limits**: ~500 requests per 5 minutes (free). Pro: 1,000 req/min, 1M calls/mo.

## TVL & Protocol Data

```python
# List all protocols with TVL
GET /protocols
# Returns: [{name, slug, tvl, chainTvls, change_1h, change_1d, change_7d, category, chains, ...}]

# Detailed protocol data with historical TVL
GET /protocol/{slug}
# Returns: Full object with tvl[], tokensInUsd{}, currentChainTvls{}, ...

# Simple current TVL number
GET /tvl/{slug}
# Returns: plain number (e.g., 150977324562.40)

# TVL for all chains
GET /v2/chains
# Returns: [{name, tvl, tokenSymbol, chainId, gecko_id}]

# Historical chain TVL
GET /v2/historicalChainTvl/{chain}
# chain: "Ethereum", "Solana", "Arbitrum", etc.
# Returns: [{date, tvl}] — date is unix timestamp (seconds)
```

## Token Prices

Coin identifiers use `{chain}:{address}` format:
- `solana:So11111111111111111111111111111111111111112` (SOL)
- `ethereum:0xdac17f958d2ee523a2206206994597c13d831ec7` (USDT)
- `coingecko:bitcoin` (non-chain lookups)

```python
# Current prices (batch)
GET /prices/current/{coins}
# coins: comma-separated identifiers
# Optional: searchWidth (default 4h)
# Returns: {coins: {id: {price, decimals, symbol, timestamp, confidence}}}

# Historical price at timestamp
GET /prices/historical/{timestamp}/{coins}
# timestamp: unix seconds

# Price chart
GET /chart/{coins}?period=1d&span=30
# period: 1d, 4h, 1h
# Returns: {coins: {id: {prices: [{timestamp, price}]}}}

# Price change percentage
GET /percentage/{coins}

# First recorded price
GET /prices/first/{coins}

# Block number at timestamp
GET /block/{chain}/{timestamp}
```

### Batch Historical Prices

```python
# POST for multiple timestamps per coin
POST /batchHistorical
Body: {"coins": {"solana:So11...": [1709251200, 1709337600]}}
```

## DEX Volumes

```python
# All DEXes aggregated
GET /overview/dexs
# Optional: excludeTotalDataChart=true, dataType=dailyVolume

# Chain-specific
GET /overview/dexs/{chain}
# chain: "Solana", "Ethereum", etc.

# Specific DEX
GET /summary/dexs/{protocol}
# Returns: {total24h, total7d, total30d, totalAllTime, totalDataChart, ...}
```

## Fees & Revenue

```python
# All protocols
GET /overview/fees
# Optional: dataType=dailyFees|dailyRevenue|dailyUserFees

# Chain-specific
GET /overview/fees/{chain}

# Specific protocol
GET /summary/fees/{protocol}
# Returns: {total24h, total7d, methodology{}, totalDataChart[], ...}
```

## Stablecoins

```python
# All stablecoins with supply data
GET https://stablecoins.llama.fi/stablecoins
# Returns: [{name, symbol, pegType, circulating, chainCirculating, price}]

# Historical market cap
GET https://stablecoins.llama.fi/stablecoincharts/all

# Chain-specific stablecoin data
GET https://stablecoins.llama.fi/stablecoincharts/{chain}

# Stablecoin prices (deviation tracking)
GET https://stablecoins.llama.fi/stablecoinprices
```

## Bridges

```python
# List all bridges
GET https://bridges.llama.fi/bridges
# Optional: includeChains=true
# Returns: {bridges: [{name, volume stats, chains, ...}]}
```

## Common Patterns

### Protocol TVL Comparison

```python
def compare_protocol_tvl(slugs: list[str]) -> list[dict]:
    """Compare TVL across protocols."""
    results = []
    for slug in slugs:
        resp = httpx.get(f"https://api.llama.fi/tvl/{slug}", timeout=15.0)
        if resp.status_code == 200:
            results.append({"protocol": slug, "tvl": resp.json()})
    return sorted(results, key=lambda x: x["tvl"], reverse=True)
```

### Multi-Token Price Lookup

```python
def get_solana_prices(mints: list[str]) -> dict[str, float]:
    """Get USD prices for Solana tokens via DeFiLlama."""
    coins = ",".join(f"solana:{m}" for m in mints)
    resp = httpx.get(f"https://coins.llama.fi/prices/current/{coins}")
    data = resp.json().get("coins", {})
    return {
        mint: data[f"solana:{mint}"]["price"]
        for mint in mints
        if f"solana:{mint}" in data
    }
```

### Solana DeFi Overview

```python
def solana_defi_snapshot() -> dict:
    """Get a snapshot of Solana DeFi activity."""
    chain_tvl = httpx.get("https://api.llama.fi/v2/chains").json()
    sol_tvl = next((c["tvl"] for c in chain_tvl if c["name"] == "Solana"), 0)

    dex_vol = httpx.get("https://api.llama.fi/overview/dexs/Solana").json()
    fees = httpx.get("https://api.llama.fi/overview/fees/Solana").json()

    return {
        "tvl": sol_tvl,
        "dex_volume_24h": dex_vol.get("total24h", 0),
        "fees_24h": fees.get("total24h", 0),
    }
```

### Historical Price Analysis

```python
def price_at_date(coin: str, date_str: str) -> float:
    """Get token price at a specific date.

    Args:
        coin: DeFiLlama coin ID (e.g., 'solana:So11...')
        date_str: Date string 'YYYY-MM-DD'
    """
    from datetime import datetime, timezone
    dt = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    ts = int(dt.timestamp())
    resp = httpx.get(f"https://coins.llama.fi/prices/historical/{ts}/{coin}")
    data = resp.json().get("coins", {})
    return data.get(coin, {}).get("price", 0)
```

## Free vs Pro Endpoints

| Category | Free | Pro ($300/mo) |
|----------|------|---------------|
| TVL / Protocols | Yes | Yes |
| Coin Prices | Yes | Yes |
| DEX Volumes (overview) | Yes | Yes |
| Fees/Revenue (overview) | Yes | Yes |
| Stablecoins | Yes | Yes |
| Bridges (list) | Yes | Yes |
| Yields / Pools | No | Yes |
| Bridge detail | No | Yes |
| Derivatives | No | Yes |
| Emissions/Unlocks | No | Yes |
| Treasuries | No | Yes |
| Hacks database | No | Yes |

## When to Use DeFiLlama vs Alternatives

| Need | Use |
|------|-----|
| Protocol TVL comparison | **DeFiLlama** |
| Multi-chain token prices | **DeFiLlama** (free batch) |
| Historical prices at specific timestamps | **DeFiLlama** |
| DeFi macro analysis | **DeFiLlama** |
| Solana token OHLCV | Birdeye or SolanaTracker |
| Real-time token data | DexScreener or Birdeye |
| Wallet PnL | SolanaTracker |
| On-chain transaction data | Helius |

## Files

### References
- `references/endpoints.md` — Complete endpoint listing with parameters and response schemas
- `references/coin_identifiers.md` — Chain prefixes, address formats, and batch lookup patterns
- `references/error_handling.md` — Rate limits, error codes, retry strategies, large response handling

### Scripts
- `scripts/defi_snapshot.py` — Solana DeFi overview: TVL, volumes, fees, top protocols
- `scripts/price_lookup.py` — Multi-token price lookup with historical comparison

### Referencia: references/coin_identifiers.md

# DeFiLlama — Coin Identifier Reference

## Format

All coin price endpoints use the format `{chain}:{address}`.

## Supported Chain Prefixes

| Prefix | Chain | Example Address |
|--------|-------|----------------|
| `solana` | Solana | `So11111111111111111111111111111111111111112` |
| `ethereum` | Ethereum | `0xdAC17F958D2ee523a2206206994597C13D831ec7` |
| `bsc` | BNB Smart Chain | `0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c` |
| `polygon` | Polygon | `0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270` |
| `arbitrum` | Arbitrum | `0x912CE59144191C1204E64559FE8253a0e49E6548` |
| `optimism` | Optimism | `0x4200000000000000000000000000000000000042` |
| `avalanche` | Avalanche | `0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7` |
| `base` | Base | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| `fantom` | Fantom | `0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83` |
| `coingecko` | CoinGecko ID | `bitcoin`, `ethereum`, `solana` |

## Common Solana Tokens

```python
SOLANA_COINS = {
    "SOL":  "solana:So11111111111111111111111111111111111111112",
    "USDC": "solana:EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    "USDT": "solana:Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
    "JUP":  "solana:JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
    "BONK": "solana:DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
    "WIF":  "solana:EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm",
    "RAY":  "solana:4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R",
    "ORCA": "solana:orcaEKTdK7LKz57vaAYr9QeNsVEPfiu6QeMU1kektZE",
}
```

## Batch Lookup Patterns

### Current Prices (up to 50+ coins)

```python
coins = ",".join(SOLANA_COINS.values())
resp = httpx.get(f"https://coins.llama.fi/prices/current/{coins}")
prices = resp.json()["coins"]
for name, coin_id in SOLANA_COINS.items():
    if coin_id in prices:
        print(f"{name}: ${prices[coin_id]['price']:.4f}")
```

### Historical Comparison

```python
from datetime import datetime, timezone, timedelta

now = int(datetime.now(tz=timezone.utc).timestamp())
week_ago = int((datetime.now(tz=timezone.utc) - timedelta(days=7)).timestamp())

# Current vs 7 days ago
current = httpx.get(f"https://coins.llama.fi/prices/current/{coin}").json()
historical = httpx.get(f"https://coins.llama.fi/prices/historical/{week_ago}/{coin}").json()
```

### Using coingecko: prefix for non-chain lookups

For tokens without a specific chain address (BTC, or when you don't know the address):

```python
# Use CoinGecko IDs
resp = httpx.get("https://coins.llama.fi/prices/current/coingecko:bitcoin,coingecko:ethereum,coingecko:solana")
```

## Confidence Score

Price responses include a `confidence` field (0-1):
- **0.99**: High confidence, multiple sources agree
- **0.90-0.98**: Good confidence
- **< 0.90**: Low confidence, price may be stale or unreliable

Filter out low-confidence prices for reliable data:

```python
def get_reliable_price(coin: str) -> float | None:
    resp = httpx.get(f"https://coins.llama.fi/prices/current/{coin}")
    data = resp.json().get("coins", {}).get(coin, {})
    if data.get("confidence", 0) < 0.9:
        return None
    return data.get("price")
```

## searchWidth Parameter

Controls how far back to look for a valid price (default: `4h`):

```python
# For illiquid tokens, increase searchWidth
resp = httpx.get(f"https://coins.llama.fi/prices/current/{coin}?searchWidth=24h")
```

Values: `4h`, `12h`, `24h`, `48h`, `1w`

### Referencia: references/endpoints.md

# DeFiLlama API — Endpoints Reference

All free endpoints require no authentication. Pro endpoints use key in URL path.

---

## TVL & Protocols (`https://api.llama.fi`)

### GET /protocols
All protocols with current TVL. Returns array of objects with: `name`, `slug`, `tvl`, `chainTvls`, `change_1h`, `change_1d`, `change_7d`, `category`, `chains`, `symbol`, `twitter`, `url`.

### GET /protocol/{slug}
Detailed protocol data with historical TVL arrays, token breakdowns, chain-specific TVL.

### GET /tvl/{slug}
Simple number — current TVL in USD.

### GET /v2/chains
All chains with TVL. Returns: `[{name, tvl, tokenSymbol, chainId, gecko_id}]`

### GET /v2/historicalChainTvl
Historical TVL summed across all chains. Returns: `[{date, tvl}]`

### GET /v2/historicalChainTvl/{chain}
Historical TVL for specific chain. Chain names: `Ethereum`, `Solana`, `Arbitrum`, etc.

---

## Coin Prices (`https://coins.llama.fi`)

**Coin ID format**: `{chain}:{address}` — e.g., `solana:So11111111111111111111111111111111111111112`

Supported chains: `ethereum`, `solana`, `bsc`, `polygon`, `arbitrum`, `optimism`, `avalanche`, `base`, `fantom`, `coingecko` (for non-chain lookups).

### GET /prices/current/{coins}
Current prices. Comma-separated coin IDs. Optional: `searchWidth` (default `4h`).

```json
{"coins": {"solana:So11...": {"price": 147.23, "decimals": 9, "symbol": "SOL", "timestamp": 1709251200, "confidence": 0.99}}}
```

### GET /prices/historical/{timestamp}/{coins}
Prices at unix timestamp. Same response schema.

### POST /batchHistorical
Batch multiple timestamps: `{"coins": {"solana:So11...": [ts1, ts2]}}`

### GET /chart/{coins}
Price chart. Query params: `period` (1d, 4h, 1h), `span` (number of periods).

### GET /percentage/{coins}
Price change percentage. Optional: `timestamp`, `lookForward`.

### GET /prices/first/{coins}
First recorded price for tokens.

### GET /block/{chain}/{timestamp}
Block number closest to timestamp.

---

## DEX Volumes (`https://api.llama.fi`)

### GET /overview/dexs
Aggregated DEX volumes. Optional: `excludeTotalDataChart=true`, `dataType=dailyVolume`.

### GET /overview/dexs/{chain}
Chain-specific DEX volumes.

### GET /summary/dexs/{protocol}
Specific DEX detail: `total24h`, `total7d`, `total30d`, `totalAllTime`, `totalDataChart[]`.

---

## Fees & Revenue (`https://api.llama.fi`)

### GET /overview/fees
All protocol fees. Optional: `dataType` = `dailyFees`, `dailyRevenue`, `dailyUserFees`.

### GET /overview/fees/{chain}
Chain-specific fees.

### GET /summary/fees/{protocol}
Specific protocol with methodology: `{total24h, methodology{UserFees, Fees, Revenue, ProtocolRevenue}, totalDataChart[]}`.

---

## Stablecoins (`https://stablecoins.llama.fi`)

### GET /stablecoins
All stablecoins: `{name, symbol, pegType, circulating, chainCirculating, price}`.

### GET /stablecoincharts/all
Historical aggregated stablecoin market cap.

### GET /stablecoincharts/{chain}
Chain-specific. Optional: `stablecoin` (filter by stablecoin ID).

### GET /stablecoinprices
Historical stablecoin price deviations.

### GET /stablecoinchains
All chains with stablecoin data.

---

## Bridges (`https://bridges.llama.fi`)

### GET /bridges
List all bridges. Optional: `includeChains=true`.
Returns: `{bridges: [{name, last24hVolume, weeklyVolume, monthlyVolume, chains}]}`

---

## Options (`https://api.llama.fi`)

### GET /overview/options
Options trading volumes. Optional: `excludeTotalDataChart`.

### GET /overview/options/{chain}
Chain-specific options.

### GET /summary/options/{protocol}
Specific protocol detail.

---

## Pro-Only Endpoints

All require API key in URL path: `https://pro-api.llama.fi/{KEY}/api/...`

| Endpoint | Description |
|----------|-------------|
| `/pools` | All yield pools with APY |
| `/chart/{pool}` | Historical APY/TVL for pool |
| `/poolsBorrow` | Borrowing rates |
| `/perps` | Perpetual funding rates |
| `/lsdRates` | Liquid staking rates |
| `/bridge/{id}` | Bridge detail |
| `/bridgevolume/{chain}` | Bridge volume by chain |
| `/api/categories` | TVL by category |
| `/api/treasuries` | Protocol treasuries |
| `/api/hacks` | Exploit database |
| `/api/raises` | Funding rounds |
| `/api/emissions` | Token unlock schedules |
| `/api/emission/{protocol}` | Specific vesting |
| `/etfs/overview` | Crypto ETF data |
| `/usage/APIKEY` | API usage stats |

---

## Response Size Warning

`/protocols`, `/overview/dexs`, and `/overview/fees` return very large payloads (10MB+). Always use `excludeTotalDataChart=true` and `excludeTotalDataChartBreakdown=true` to reduce response size.

### Referencia: references/error_handling.md

# DeFiLlama API — Error Handling

## Rate Limits

| Tier | Limit | Monthly |
|------|-------|---------|
| Free | ~500 req / 5 min | Unlimited |
| API ($300/mo) | 1,000 req/min | 1M calls |

No rate limit headers are returned. HTTP 429 means you're rate limited.

## HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Process response |
| 400 | Bad request | Check coin IDs, parameters |
| 429 | Rate limited | Wait 30-60 seconds |
| 502 | Upstream error | Retry after 5 seconds |
| 504 | Gateway timeout | Response too large, use exclude params |

## Retry Strategy

```python
import time
import httpx

def llama_get(url: str, max_retries: int = 3) -> dict | list:
    """GET with retry for DeFiLlama endpoints."""
    for attempt in range(max_retries):
        try:
            resp = httpx.get(url, timeout=30.0)

            if resp.status_code == 200:
                return resp.json()

            if resp.status_code == 429:
                wait = 30.0 * (attempt + 1)
                print(f"Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue

            if resp.status_code >= 500:
                time.sleep(5.0 * (attempt + 1))
                continue

            resp.raise_for_status()
        except httpx.TimeoutException:
            if attempt < max_retries - 1:
                time.sleep(5.0)
                continue
            raise

    raise RuntimeError(f"Failed after {max_retries} retries: {url}")
```

## Common Issues

### 1. Large response payloads
`/protocols` and volume/fee overviews can return 10MB+. Always use filter params:
```python
resp = httpx.get("https://api.llama.fi/overview/dexs", params={
    "excludeTotalDataChart": "true",
    "excludeTotalDataChartBreakdown": "true",
})
```

### 2. Timestamps are seconds, not milliseconds
All DeFiLlama timestamps are unix seconds. Don't multiply by 1000.

### 3. Missing coin data
If a coin ID returns no data, check:
- Address format (lowercase for EVM, base58 for Solana)
- Chain prefix is correct
- Token has on-chain liquidity
- Try `searchWidth=24h` for illiquid tokens

### 4. Stale prices
Check the `timestamp` and `confidence` fields:
```python
import time

data = resp.json()["coins"].get(coin_id, {})
age = time.time() - data.get("timestamp", 0)
if age > 3600:  # older than 1 hour
    print("Warning: stale price data")
if data.get("confidence", 0) < 0.9:
    print("Warning: low confidence price")
```

### 5. Protocol slugs
Protocol slugs don't always match the display name:
- "Raydium" → `raydium`
- "Aave V3" → `aave-v3`
- "Uniswap V3" → `uniswap`

Use `/protocols` to find the correct `slug` field.

### 6. Chain name casing
Chain names in URLs are case-sensitive:
- Correct: `Solana`, `Ethereum`, `Arbitrum`
- Wrong: `solana`, `SOLANA`

This applies to `/overview/dexs/{chain}`, `/overview/fees/{chain}`, `/v2/historicalChainTvl/{chain}`.

## Caching Recommendations

| Data | Cache TTL | Reason |
|------|-----------|--------|
| Protocol list | 15-30 min | Changes slowly |
| TVL (current) | 5-15 min | Updates periodically |
| Historical TVL | 1 hour+ | Immutable history |
| Prices (current) | 1-5 min | Changes constantly |
| Prices (historical) | Forever | Immutable |
| Volume/Fee overviews | 15-30 min | Daily aggregation |


---

## SKILL: dex-execution

- Fuente: `agiprolabs/claude-trading-skills` → `skills/dex-execution` (MIT)
- Cuándo usarla: Solana DEX swap execution via Jupiter aggregator including quoting, transaction building, signing, and confirmation
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/dex-execution/` (get_quote.py, simulate_swap.py)

# DEX Execution — Solana Swap Execution via Jupiter

Execute token swaps on Solana through Jupiter, the dominant DEX aggregator routing across Raydium, Orca, Meteora, Phoenix, Lifinity, and 20+ other venues.

## Overview

Jupiter aggregates liquidity across all major Solana DEXes to find optimal swap routes. A single swap may split across multiple pools and hop through intermediate tokens to minimize price impact. The Jupiter v6 API handles route discovery, transaction building, and fee optimization — your code handles quoting, user confirmation, signing, and submission.

**Base URL**: `https://quote-api.jup.ag/v6`

## Execution Pipeline

Every swap follows this seven-step pipeline. Never skip steps 2-3 (display and confirm).

### Step 1 — Get Quote

```python
import httpx

params = {
    "inputMint": "So11111111111111111111111111111111111111112",   # SOL
    "outputMint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", # USDC
    "amount": 1_000_000_000,  # 1 SOL in lamports
    "slippageBps": 50,        # 0.5%
}
resp = httpx.get("https://quote-api.jup.ag/v6/quote", params=params)
quote = resp.json()
```

### Step 2 — Display Quote to User

Always show these fields before proceeding:

| Field | Source |
|---|---|
| Input amount | `quote["inAmount"]` (in token decimals) |
| Output amount | `quote["outAmount"]` |
| Minimum received | `quote["otherAmountThreshold"]` |
| Price impact | `quote["priceImpactPct"]` |
| Route | `quote["routePlan"]` — DEXes used |
| Slippage | The `slippageBps` you requested |

### Step 3 — Require User Confirmation

```
⚠️  SWAP PREVIEW
    Selling:   1.000 SOL
    Buying:    ~142.50 USDC
    Min recv:  141.79 USDC (0.5% slippage)
    Impact:    0.01%
    Route:     Raydium V4 → USDC

    Proceed? [y/N]
```

**NEVER proceed without explicit "yes" from the user.**

### Step 4 — Build Transaction

```python
swap_body = {
    "quoteResponse": quote,
    "userPublicKey": "YourPubkeyBase58...",
    "wrapAndUnwrapSol": True,
    "dynamicComputeUnitLimit": True,
    "prioritizationFeeLamports": "auto",
}
resp = httpx.post("https://quote-api.jup.ag/v6/swap", json=swap_body)
swap_data = resp.json()
swap_tx = swap_data["swapTransaction"]  # base64-encoded transaction
```

### Step 5 — Sign Transaction

```python
import base64
from solders.transaction import VersionedTransaction
from solders.keypair import Keypair

raw_tx = base64.b64decode(swap_tx)
tx = VersionedTransaction.from_bytes(raw_tx)
keypair = Keypair.from_base58_string(os.environ["WALLET_PRIVATE_KEY"])
tx.sign([keypair])
```

### Step 6 — Submit Transaction

```python
rpc_url = os.environ.get("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
signed_bytes = bytes(tx)
payload = {
    "jsonrpc": "2.0", "id": 1,
    "method": "sendTransaction",
    "params": [
        base64.b64encode(signed_bytes).decode(),
        {"encoding": "base64", "skipPreflight": False,
         "maxRetries": 3, "preflightCommitment": "confirmed"}
    ],
}
resp = httpx.post(rpc_url, json=payload)
sig = resp.json()["result"]
print(f"Submitted: https://solscan.io/tx/{sig}")
```

### Step 7 — Confirm Transaction

```python
import time

for attempt in range(30):
    payload = {
        "jsonrpc": "2.0", "id": 1,
        "method": "getSignatureStatuses",
        "params": [[sig], {"searchTransactionHistory": False}],
    }
    resp = httpx.post(rpc_url, json=payload)
    status = resp.json()["result"]["value"][0]
    if status and status.get("confirmationStatus") in ("confirmed", "finalized"):
        print(f"Confirmed at slot {status['slot']}")
        break
    time.sleep(2)
else:
    print("Transaction not confirmed within 60s — check explorer")
```

## Jupiter API v6 Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/quote` | GET | Get best-price quote with routing |
| `/swap` | POST | Build a swap transaction from a quote |
| `/swap-instructions` | POST | Get individual instructions (advanced) |
| `/price?ids=token1,token2` | GET | Simple price lookup (v2) |
| `/tokens` | GET | List all supported tokens |

See `references/jupiter_api.md` for full parameter and response documentation.

## Key Parameters

### Slippage (`slippageBps`)

| Token Type | Recommended Range | Notes |
|---|---|---|
| SOL, USDC, major tokens | 50-100 (0.5-1%) | Stable liquidity |
| Mid-cap tokens | 100-300 (1-3%) | Variable liquidity |
| PumpFun / meme tokens | 500-2000 (5-20%) | Thin books, high volatility |
| New launches (<1h old) | 1000-3000 (10-30%) | Extreme volatility |

### Dynamic Slippage

Set `dynamicSlippage: true` in the swap request to let Jupiter auto-adjust slippage based on current market conditions. Preferred for most use cases.

### Priority Fees (`prioritizationFeeLamports`)

Priority fees determine transaction ordering within a block.

| Level | microLamports | When to Use |
|---|---|---|
| Low | 10,000-50,000 | Normal conditions |
| Medium | 50,000-200,000 | Moderate congestion |
| High | 200,000-1,000,000 | High congestion / time-sensitive |
| Urgent | 1,000,000-5,000,000 | Meme coin launches, NFT mints |
| Auto | `"auto"` | Jupiter estimates for you |

Use `"auto"` for most cases. For fine-grained control, query Helius `getPriorityFeeEstimate`.

### Other Parameters

- **`onlyDirectRoutes`**: Skip multi-hop routing. Faster but may get worse price.
- **`asLegacyTransaction`**: Use legacy format instead of versioned transactions. Required for some older wallets.
- **`maxAccounts`**: Limit accounts in transaction (default 64). Lower values reduce route options but improve confirmation reliability.
- **`platformFeeBps`**: Integrator fee in basis points. Taken from output amount.
- **`wrapAndUnwrapSol`**: Auto wrap/unwrap SOL ↔ wSOL (default true).
- **`dynamicComputeUnitLimit`**: Auto-set compute budget based on simulation.

## Priority Fee Estimation

```python
# Using Helius getPriorityFeeEstimate
helius_url = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_KEY}"
payload = {
    "jsonrpc": "2.0", "id": 1,
    "method": "getPriorityFeeEstimate",
    "params": [{"accountKeys": [input_mint, output_mint],
                "options": {"recommended": True}}],
}
resp = httpx.post(helius_url, json=payload)
fee = resp.json()["result"]["priorityFeeEstimate"]
```

## Transaction Confirmation Strategy

See `references/transaction_lifecycle.md` for the full Solana transaction lifecycle.

1. **Submit** with `skipPreflight: False` to catch obvious errors
2. **Poll** `getSignatureStatuses` every 2 seconds for up to 60 seconds
3. **If not confirmed**: rebuild transaction with fresh blockhash and retry (max 3 attempts)
4. **Blockhash expiry**: transactions expire ~60 seconds after blockhash was fetched
5. **Final check**: verify token balance changed as expected

## Error Handling

| Error | Cause | Recovery |
|---|---|---|
| `"Slippage tolerance exceeded"` | Price moved beyond slippageBps | Increase slippage or retry |
| `"Insufficient funds"` | Not enough input token or SOL for fees | Check balance before quoting |
| `"Transaction expired"` | Blockhash too old | Rebuild with fresh blockhash |
| `"Transaction simulation failed"` | Various — check logs | Parse simulation logs for root cause |
| `"Too many accounts"` | Route uses too many accounts | Set `maxAccounts` lower or use `onlyDirectRoutes` |
| HTTP 429 | Rate limited | Back off and retry with exponential delay |
| HTTP 400 `"No route found"` | No liquidity path exists | Check token mints are correct, try larger slippage |

## Safety Requirements

> **These are non-negotiable requirements for any execution code.**

1. **ALWAYS show quote details** (amounts, price impact, route) before execution
2. **ALWAYS require explicit user confirmation** — never auto-execute
3. **Default to simulation mode** — do not sign or submit unless explicitly enabled
4. **Never store or log private keys** — load from env vars, use immediately, discard
5. **Never use 100% slippage** — this is a common scam/exploit vector
6. **Verify token addresses** — confirm mints match expected tokens before swapping
7. **Check price impact** — warn if >2%, block if >10% unless user overrides
8. **Maintain SOL reserve** — keep 0.05 SOL minimum for rent and future fees

See `references/safety_checklist.md` for the complete pre/during/post execution checklist.

## Integration with Other Skills

| Skill | Integration |
|---|---|
| `slippage-modeling` | Estimate optimal slippageBps based on token liquidity profile |
| `liquidity-analysis` | Verify pool depth supports trade size before quoting |
| `position-sizing` | Calculate trade amount based on risk parameters |
| `risk-management` | Enforce portfolio-level exposure limits before execution |
| `jupiter-api` | Underlying API documentation for Jupiter endpoints |
| `helius-api` | Priority fee estimation and transaction monitoring |

## Files

### References
- `references/jupiter_api.md` — Complete Jupiter v6 API parameter and response reference
- `references/transaction_lifecycle.md` — Solana transaction lifecycle, priority fees, retry strategies
- `references/safety_checklist.md` — Pre/during/post execution verification checklist

### Scripts
- `scripts/get_quote.py` — Fetch and display Jupiter swap quotes with route analysis
- `scripts/simulate_swap.py` — Build and simulate swap transactions without submitting

### Referencia: references/jupiter_api.md

# Jupiter v6 API Reference

Base URL: `https://quote-api.jup.ag/v6`

No authentication required. Rate limits apply per IP.

## Rate Limits

| Endpoint | Limit |
|---|---|
| GET /quote | 600 requests/minute |
| POST /swap | 300 requests/minute |
| POST /swap-instructions | 300 requests/minute |
| GET /price | 600 requests/minute |
| GET /tokens | 60 requests/minute |

## GET /quote

Get the best-price quote for a token swap.

### Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `inputMint` | string | Yes | — | Input token mint address |
| `outputMint` | string | Yes | — | Output token mint address |
| `amount` | integer | Yes | — | Input amount in smallest unit (lamports for SOL) |
| `slippageBps` | integer | No | 50 | Maximum slippage in basis points |
| `platformFeeBps` | integer | No | 0 | Integrator fee in basis points |
| `onlyDirectRoutes` | boolean | No | false | Skip multi-hop routes |
| `asLegacyTransaction` | boolean | No | false | Return legacy transaction format |
| `maxAccounts` | integer | No | 64 | Maximum accounts in transaction |
| `excludeDexes` | string | No | — | Comma-separated DEX names to exclude |
| `restrictIntermediateTokens` | boolean | No | false | Only use high-liquidity intermediate tokens |

### Response

```json
{
  "inputMint": "So11111111111111111111111111111111111111112",
  "inAmount": "1000000000",
  "outputMint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
  "outAmount": "14250000",
  "otherAmountThreshold": "14178750",
  "swapMode": "ExactIn",
  "slippageBps": 50,
  "priceImpactPct": "0.01",
  "routePlan": [
    {
      "swapInfo": {
        "ammKey": "...",
        "label": "Raydium",
        "inputMint": "So111...",
        "outputMint": "EPjFW...",
        "inAmount": "1000000000",
        "outAmount": "14250000",
        "feeAmount": "25000",
        "feeMint": "So111..."
      },
      "percent": 100
    }
  ],
  "contextSlot": 250000000,
  "timeTaken": 0.05
}
```

### Key Response Fields

- **`outAmount`**: Expected output in smallest units
- **`otherAmountThreshold`**: Minimum output after slippage (for ExactIn mode)
- **`priceImpactPct`**: Price impact as a percentage string
- **`routePlan`**: Array of swap steps with DEX labels and amounts
- **`timeTaken`**: Quote computation time in seconds

### Example

```bash
curl "https://quote-api.jup.ag/v6/quote?\
inputMint=So11111111111111111111111111111111111111112&\
outputMint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v&\
amount=1000000000&\
slippageBps=50"
```

## POST /swap

Build a swap transaction from a quote response.

### Request Body

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `quoteResponse` | object | Yes | — | Full quote response from GET /quote |
| `userPublicKey` | string | Yes | — | Signer's public key (base58) |
| `wrapAndUnwrapSol` | boolean | No | true | Auto wrap/unwrap SOL |
| `useSharedAccounts` | boolean | No | true | Use shared intermediate token accounts |
| `dynamicComputeUnitLimit` | boolean | No | false | Auto-set compute unit limit from simulation |
| `skipUserAccountsRpcCalls` | boolean | No | false | Skip RPC calls for user account checks |
| `prioritizationFeeLamports` | int/string | No | 0 | Priority fee; use `"auto"` for Jupiter estimate |
| `dynamicSlippage` | boolean | No | false | Auto-adjust slippage based on conditions |
| `computeUnitPriceMicroLamports` | integer | No | — | Explicit compute unit price (overrides prioritizationFeeLamports) |

### Response

```json
{
  "swapTransaction": "AQAAAA...base64...",
  "lastValidBlockHeight": 250000100,
  "prioritizationFeeLamports": 50000,
  "computeUnitLimit": 200000,
  "dynamicSlippageReport": {
    "slippageBps": 75,
    "otherAmount": 14143125,
    "simulatedIncurredSlippageBps": 12
  }
}
```

- **`swapTransaction`**: Base64-encoded versioned transaction (or legacy if requested)
- **`lastValidBlockHeight`**: Transaction expires after this block height
- **`dynamicSlippageReport`**: Present when `dynamicSlippage: true`; shows actual slippage used

### Example

```bash
curl -X POST "https://quote-api.jup.ag/v6/swap" \
  -H "Content-Type: application/json" \
  -d '{
    "quoteResponse": { ... },
    "userPublicKey": "YourPubkeyHere",
    "wrapAndUnwrapSol": true,
    "dynamicComputeUnitLimit": true,
    "prioritizationFeeLamports": "auto"
  }'
```

## POST /swap-instructions

Returns individual instructions instead of a serialized transaction. Use this for advanced cases where you need to add custom instructions.

### Request Body

Same as POST /swap.

### Response

```json
{
  "tokenLedgerInstruction": null,
  "computeBudgetInstructions": [...],
  "setupInstructions": [...],
  "swapInstruction": { ... },
  "cleanupInstruction": { ... },
  "addressLookupTableAddresses": [...]
}
```

Each instruction contains `programId`, `accounts` (array of `{pubkey, isSigner, isWritable}`), and `data` (base58).

## GET /price

Simple price lookup for one or more tokens (Jupiter Price API v2).

**URL**: `https://price.jup.ag/v2/price`

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `ids` | string | Yes | Comma-separated token mint addresses |
| `vsToken` | string | No | Quote token (default: USDC) |

### Response

```json
{
  "data": {
    "So11111111111111111111111111111111111111112": {
      "id": "So11111111111111111111111111111111111111112",
      "mintSymbol": "SOL",
      "vsToken": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
      "vsTokenSymbol": "USDC",
      "price": 142.50
    }
  },
  "timeTaken": 0.002
}
```

## GET /tokens

Returns all tokens Jupiter supports for swapping.

### Response

Array of token objects:

```json
[
  {
    "address": "So11111111111111111111111111111111111111112",
    "chainId": 101,
    "decimals": 9,
    "name": "Wrapped SOL",
    "symbol": "SOL",
    "logoURI": "https://...",
    "tags": ["old-registry"],
    "extensions": {}
  }
]
```

## Common Token Mints

| Token | Mint Address |
|---|---|
| SOL (wrapped) | `So11111111111111111111111111111111111111112` |
| USDC | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |
| USDT | `Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB` |
| BONK | `DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263` |
| JUP | `JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN` |
| RAY | `4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R` |
| ORCA | `orcaEKTdK7LKz57vaAYr9QeNsVEPfiu6QeMU1kektZE` |

## Error Responses

| Status | Body | Meaning |
|---|---|---|
| 400 | `{"error": "No route found"}` | No swap path exists for this pair/amount |
| 400 | `{"error": "Amount too small"}` | Input amount below minimum |
| 429 | — | Rate limit exceeded |
| 500 | — | Internal server error; retry |

### Referencia: references/safety_checklist.md

# DEX Execution Safety Checklist

## Pre-Execution Checks

Run all checks before requesting user confirmation. Block execution if any critical check fails.

### 1. Token Validation (Critical)

```python
def validate_token(mint: str, expected_symbol: str) -> bool:
    """Verify mint address matches expected token."""
    resp = httpx.get(f"https://quote-api.jup.ag/v6/tokens")
    tokens = {t["address"]: t for t in resp.json()}
    if mint not in tokens:
        print(f"WARNING: {mint} not in Jupiter token list")
        return False
    actual = tokens[mint]["symbol"]
    if actual != expected_symbol:
        print(f"MISMATCH: expected {expected_symbol}, got {actual}")
        return False
    return True
```

- Verify mint address is correct (copy-paste errors are common)
- Cross-reference symbol with known token list
- Watch for fake tokens that mimic real token names

### 2. Liquidity Check (Critical)

- Query pool depth before quoting
- Minimum liquidity threshold: trade size should be < 2% of total pool TVL
- For tokens with < $10K liquidity, warn the user explicitly
- See the `liquidity-analysis` skill for detailed pool assessment

### 3. Price Impact Assessment (Critical)

| Impact | Action |
|---|---|
| < 1% | Proceed normally |
| 1-2% | Show warning, proceed if user confirms |
| 2-5% | Strong warning — suggest smaller trade or limit order |
| 5-10% | Block by default — require explicit override |
| > 10% | Block — almost certainly a mistake or scam token |

```python
impact = float(quote["priceImpactPct"])
if impact > 10.0:
    print("BLOCKED: Price impact exceeds 10%. This is likely an error.")
    return False
elif impact > 5.0:
    print(f"WARNING: {impact:.2f}% price impact. Requires explicit override.")
    return confirm_with_user("Proceed despite high impact?")
elif impact > 2.0:
    print(f"CAUTION: {impact:.2f}% price impact. Consider reducing trade size.")
```

### 4. Slippage Validation (Critical)

- Never accept slippage >= 50% (5000 bps) — almost always a mistake or exploit
- Warn if slippage > 10% (1000 bps) for non-meme tokens
- For meme tokens, cap at 30% (3000 bps) with explicit user acknowledgment

```python
MAX_SLIPPAGE_BPS = 5000  # absolute max, never exceed

def validate_slippage(slippage_bps: int, is_meme: bool = False) -> bool:
    if slippage_bps >= MAX_SLIPPAGE_BPS:
        print("BLOCKED: Slippage >= 50% is never acceptable")
        return False
    if not is_meme and slippage_bps > 1000:
        print(f"WARNING: {slippage_bps/100:.1f}% slippage is high for this token")
    return True
```

### 5. Balance Verification (Critical)

```python
def check_balance(rpc_url: str, pubkey: str, input_mint: str,
                  amount: int, is_sol: bool) -> bool:
    """Verify sufficient balance for trade + fees."""
    SOL_RESERVE = 50_000_000  # 0.05 SOL for rent + fees

    if is_sol:
        # Need amount + reserve for fees
        sol_balance = get_sol_balance(rpc_url, pubkey)
        required = amount + SOL_RESERVE
        if sol_balance < required:
            print(f"Insufficient SOL: have {sol_balance}, need {required}")
            return False
    else:
        # Need token amount + SOL for fees
        token_balance = get_token_balance(rpc_url, pubkey, input_mint)
        sol_balance = get_sol_balance(rpc_url, pubkey)
        if token_balance < amount:
            print(f"Insufficient token balance: have {token_balance}, need {amount}")
            return False
        if sol_balance < SOL_RESERVE:
            print(f"Insufficient SOL for fees: have {sol_balance}, need {SOL_RESERVE}")
            return False
    return True
```

### 6. Quote Freshness

- Quotes are valid for approximately 30 seconds
- If more than 30 seconds have elapsed since the quote, fetch a new one
- In volatile markets, re-quote even more frequently (10-15 seconds)

### 7. User Confirmation (Critical)

Display all of the following before asking for confirmation:

```
╔══════════════════════════════════════╗
║         SWAP CONFIRMATION            ║
╠══════════════════════════════════════╣
║  Sell:     1.000 SOL                 ║
║  Buy:      ~142.50 USDC             ║
║  Min recv: 141.79 USDC              ║
║  Impact:   0.01%                     ║
║  Slippage: 0.5%                      ║
║  Route:    SOL → Raydium → USDC     ║
║  Fee:      ~0.00005 SOL             ║
╠══════════════════════════════════════╣
║  Proceed? Type YES to confirm        ║
╚══════════════════════════════════════╝
```

## During Execution

### 8. Simulate Before Sending

- Always call `simulateTransaction` before `sendTransaction`
- Check `result.value.err` — if not null, do not proceed
- Parse simulation logs for warnings
- Note compute units consumed for fee estimation

### 9. Monitor Confirmation

- Poll `getSignatureStatuses` every 2 seconds
- Set a timeout of 60 seconds maximum
- If timeout: do NOT assume failure — the transaction may still land
- Check the explorer before retrying to avoid double-execution

### 10. Handle Timeout Gracefully

```python
def handle_timeout(rpc_url: str, signature: str) -> str:
    """Determine transaction fate after timeout."""
    # Check one more time with history search
    payload = {
        "jsonrpc": "2.0", "id": 1,
        "method": "getSignatureStatuses",
        "params": [[signature], {"searchTransactionHistory": True}],
    }
    resp = httpx.post(rpc_url, json=payload)
    status = resp.json()["result"]["value"][0]

    if status is None:
        return "dropped"  # Transaction was never processed — safe to retry
    elif status.get("err"):
        return "failed"   # Transaction failed on-chain — safe to retry
    else:
        return "pending"  # Still processing — DO NOT retry yet
```

## Post-Execution

### 11. Verify Balance Change

After confirmation, verify the expected token was received:

```python
def verify_execution(rpc_url: str, pubkey: str, output_mint: str,
                     pre_balance: int, expected_min: int) -> dict:
    """Verify swap executed correctly."""
    post_balance = get_token_balance(rpc_url, pubkey, output_mint)
    received = post_balance - pre_balance

    return {
        "received": received,
        "expected_min": expected_min,
        "within_slippage": received >= expected_min,
        "execution_quality": received / expected_min if expected_min > 0 else 0,
    }
```

### 12. Log Transaction

Record for analysis (never log private keys):

```python
execution_log = {
    "timestamp": datetime.utcnow().isoformat(),
    "signature": sig,
    "input_mint": input_mint,
    "output_mint": output_mint,
    "input_amount": in_amount,
    "quoted_output": quoted_output,
    "actual_output": actual_output,
    "price_impact_pct": price_impact,
    "slippage_bps": slippage_bps,
    "priority_fee_lamports": priority_fee,
    "route": route_labels,
}
```

### 13. Calculate Execution Quality

```python
quoted_price = float(quoted_output) / float(in_amount)
actual_price = float(actual_output) / float(in_amount)
execution_cost_bps = (1 - actual_price / quoted_price) * 10000
print(f"Execution cost: {execution_cost_bps:.1f} bps vs quoted price")
```

## What NOT to Do

1. **Never auto-execute** — always require explicit user confirmation
2. **Never hardcode private keys** — environment variables only
3. **Never log private keys** — not to console, files, or remote services
4. **Never ignore simulation errors** — if simulation fails, do not send
5. **Never set slippage to 100%** — this is a common attack vector
6. **Never retry without checking** — verify the first tx didn't land before retrying
7. **Never skip balance checks** — insufficient balance errors waste fees
8. **Never trust token symbols alone** — always verify by mint address
9. **Never execute on behalf of user** without showing full trade details first
10. **Never assume a timeout means failure** — always check transaction status

### Referencia: references/transaction_lifecycle.md

# Solana Transaction Lifecycle

## Overview

Every Solana swap follows a strict lifecycle: build, simulate, sign, send, confirm. Understanding each step prevents lost funds and failed transactions.

## 1. Build Transaction

Jupiter's POST /swap returns a base64-encoded versioned transaction. To work with it:

```python
import base64
from solders.transaction import VersionedTransaction

raw_tx = base64.b64decode(swap_response["swapTransaction"])
tx = VersionedTransaction.from_bytes(raw_tx)
```

**Versioned vs Legacy Transactions**:
- Versioned transactions (v0) support address lookup tables, reducing account size
- Legacy transactions have a 35-account hard limit
- Use `asLegacyTransaction: true` only if the signing wallet requires it
- Jupiter defaults to versioned transactions

## 2. Simulate Transaction

Always simulate before signing to catch errors without spending fees.

```python
import base64, httpx

rpc_url = "https://api.mainnet-beta.solana.com"
raw_bytes = bytes(tx)  # unsigned transaction bytes
payload = {
    "jsonrpc": "2.0", "id": 1,
    "method": "simulateTransaction",
    "params": [
        base64.b64encode(raw_bytes).decode(),
        {
            "encoding": "base64",
            "commitment": "confirmed",
            "sigVerify": False,
            "replaceRecentBlockhash": True,
        }
    ],
}
resp = httpx.post(rpc_url, json=payload)
result = resp.json()["result"]["value"]

if result["err"]:
    print(f"Simulation failed: {result['err']}")
    print(f"Logs: {result['logs']}")
else:
    print(f"Simulation OK — {result['unitsConsumed']} compute units")
```

Key simulation parameters:
- **`sigVerify: False`**: Skip signature verification (transaction isn't signed yet)
- **`replaceRecentBlockhash: True`**: Use a fresh blockhash so simulation doesn't fail on expiry

## 3. Sign Transaction

```python
from solders.keypair import Keypair

keypair = Keypair.from_base58_string(private_key)
tx.sign([keypair])
```

**Security rules**:
- Load private key from environment variable only
- Never log, print, or persist the private key
- Never sign without user confirmation
- Clear the keypair from memory after signing (Python GC handles this)

## 4. Send Transaction

```python
signed_bytes = bytes(tx)
payload = {
    "jsonrpc": "2.0", "id": 1,
    "method": "sendTransaction",
    "params": [
        base64.b64encode(signed_bytes).decode(),
        {
            "encoding": "base64",
            "skipPreflight": False,
            "preflightCommitment": "confirmed",
            "maxRetries": 3,
        }
    ],
}
resp = httpx.post(rpc_url, json=payload)
sig = resp.json()["result"]
```

**`skipPreflight` options**:
- `False` (default): RPC simulates before forwarding. Catches errors early.
- `True`: Skip simulation, send directly. Use only when you already simulated and need speed.

## 5. Confirm Transaction

```python
import time

def confirm_transaction(rpc_url: str, signature: str,
                        timeout: int = 60, interval: int = 2) -> dict:
    """Poll for transaction confirmation."""
    start = time.time()
    while time.time() - start < timeout:
        payload = {
            "jsonrpc": "2.0", "id": 1,
            "method": "getSignatureStatuses",
            "params": [[signature], {"searchTransactionHistory": False}],
        }
        resp = httpx.post(rpc_url, json=payload)
        statuses = resp.json()["result"]["value"]
        if statuses[0]:
            status = statuses[0]
            if status.get("err"):
                return {"confirmed": False, "error": status["err"]}
            if status["confirmationStatus"] in ("confirmed", "finalized"):
                return {"confirmed": True, "slot": status["slot"],
                        "status": status["confirmationStatus"]}
        time.sleep(interval)
    return {"confirmed": False, "error": "timeout"}
```

**Commitment levels**:
- **`processed`**: Seen by the leader, not yet voted on (~400ms)
- **`confirmed`**: Voted on by supermajority (~5-10s) — sufficient for most swaps
- **`finalized`**: Rooted, irreversible (~15-30s) — use for high-value transactions

## Priority Fees

Solana uses a fee market based on compute unit price. Higher fees = higher priority in block scheduling.

### How Priority Fees Work

Total fee = `base_fee (5000 lamports)` + `compute_units * compute_unit_price`

```python
# compute_unit_price is in microLamports (1 lamport = 1_000_000 microLamports)
# Example: 100,000 microLamports * 200,000 CU = 20,000 lamports = 0.00002 SOL
```

### Estimating Priority Fees

**Option A — Jupiter auto**:
Set `prioritizationFeeLamports: "auto"` in the /swap request. Jupiter estimates based on recent blocks.

**Option B — Helius API**:
```python
payload = {
    "jsonrpc": "2.0", "id": 1,
    "method": "getPriorityFeeEstimate",
    "params": [{
        "accountKeys": [input_mint, output_mint],
        "options": {"recommended": True}
    }],
}
resp = httpx.post(helius_rpc_url, json=payload)
estimate = resp.json()["result"]
# Returns: {"priorityFeeEstimate": 50000}
```

**Option C — Fixed tiers**:

| Tier | microLamports | Typical Cost (200K CU) |
|---|---|---|
| Economy | 10,000 | 0.000002 SOL |
| Standard | 50,000 | 0.00001 SOL |
| Fast | 200,000 | 0.00004 SOL |
| Turbo | 1,000,000 | 0.0002 SOL |
| Emergency | 5,000,000 | 0.001 SOL |

### When to Increase Priority Fees

- Token launches (first minutes): Turbo/Emergency
- High market volatility: Fast/Turbo
- Normal trading: Standard
- Non-urgent rebalancing: Economy

## Blockhash Expiry and Retries

Transactions include a `recentBlockhash` that expires after ~60 seconds (~150 slots).

### Retry Strategy

```
1. Get quote → Build tx → Simulate → Sign → Send
2. Poll for 30 seconds
3. If not confirmed:
   a. Get fresh quote (prices may have changed)
   b. Build new tx with new blockhash
   c. Simulate → Sign → Send
4. Repeat up to 3 total attempts
5. If still not confirmed, abort and alert user
```

Never resubmit a signed transaction with an expired blockhash — it will be rejected.

## Common Failure Modes

| Failure | Cause | Solution |
|---|---|---|
| `BlockhashNotFound` | Blockhash expired | Rebuild transaction with fresh blockhash |
| `InsufficientFundsForRent` | Account needs rent-exempt minimum | Ensure 0.05 SOL reserve |
| `SlippageToleranceExceeded` | Price moved beyond limit | Increase slippage or retry quickly |
| `AccountNotFound` | Token account doesn't exist | Enable `wrapAndUnwrapSol`, check ATAs |
| `ProgramError` | AMM-specific error | Check simulation logs for details |
| Transaction dropped | Leader didn't include it | Resubmit with higher priority fee |

## Verifying Execution

After confirmation, verify the swap executed correctly:

```python
# Check token balance changed
payload = {
    "jsonrpc": "2.0", "id": 1,
    "method": "getTokenAccountsByOwner",
    "params": [
        user_pubkey,
        {"mint": output_mint},
        {"encoding": "jsonParsed"}
    ],
}
```

Compare post-swap balance with pre-swap balance to calculate actual execution price.


---

## SKILL: dex-pool-analysis

- Fuente: `agiprolabs/claude-trading-skills` → `skills/dex-pool-analysis` (MIT)
- Cuándo usarla: AMM pool mechanics comparison across Raydium, Orca, and Meteora including fee structures, pool types, creation patterns, and volume efficiency
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/dex-pool-analysis/` (analyze_pools.py, pool_monitor.py)

# DEX Pool Analysis — Solana AMM Pool Mechanics & Comparison

Solana's DEX ecosystem spans multiple AMM designs: constant-product pools (Raydium V4), concentrated liquidity (Raydium CLMM, Orca Whirlpool), and bin-based liquidity (Meteora DLMM). Each pool type has distinct fee structures, capital efficiency characteristics, and risk profiles. Understanding these differences is essential for selecting the best execution venue, evaluating liquidity quality, and identifying pool-level risks.

This skill covers:
- Pool type mechanics and fee structures across Solana DEXes
- Pool health metrics (TVL, volume efficiency, fee APR, LP count)
- Pool creation patterns (PumpFun graduation, manual creation)
- Best pool selection for trade execution
- Pool age and risk assessment

**Related skills**: See `lp-math` for AMM formulas, `liquidity-analysis` for depth assessment, `impermanent-loss` for LP risk, `slippage-modeling` for execution cost.

---

## 1. Pool Types on Solana

### Raydium V4 (Constant Product)

The most common pool type for newly launched tokens. Uses the classic `xy = k` invariant with a fixed 0.25% swap fee. Integrated with OpenBook (formerly Serum) for combined AMM + orderbook liquidity.

```
Program ID: 675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8
Fee: 0.25% per swap (0.22% to LPs, 0.03% to RAY buyback)
```

**Key characteristics**:
- Full-range liquidity (infinite price range)
- Simple LP provisioning — deposit both tokens in equal value
- Lower capital efficiency than concentrated liquidity
- OpenBook market ID required for pool creation

### Raydium CLMM (Concentrated Liquidity)

Concentrated Liquidity Market Maker pools allow LPs to specify price ranges, improving capital efficiency by 10-100x compared to V4.

```
Program ID: CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK
Fee tiers: 0.01%, 0.05%, 0.25%, 1%, 2%
Tick spacing: 1, 10, 60, 120, 240 (corresponding to fee tiers)
```

**Key characteristics**:
- LPs choose min/max price for their position
- Positions represented as NFTs
- Higher fee income per dollar deposited (when in range)
- Risk of position going out of range (no fees earned)
- Multiple fee tiers for different volatility profiles

### Orca Whirlpool (Concentrated Liquidity)

Orca's concentrated liquidity implementation, dominant for major token pairs (SOL/USDC, SOL/USDT).

```
Program ID: whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc
Fee tiers: 0.01%, 0.02%, 0.04%, 0.05%, 0.16%, 0.30%, 0.65%, 1%, 2%
Tick spacing: 1, 2, 4, 8, 16, 64, 128, 256, 512 (varies by fee)
```

**Key characteristics**:
- Positions as NFTs (similar to Uniswap V3)
- Wide fee tier selection for granular control
- Strong SDK and developer tooling
- Dominant for blue-chip Solana pairs

### Meteora DLMM (Dynamic Liquidity Market Maker)

Bin-based liquidity where each bin holds a fixed price. LPs distribute liquidity across bins using strategy modes.

```
Program ID: LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo
Fee: Dynamic (base fee + variable fee based on volatility)
Bin step: 1-100 basis points per bin
```

**Key characteristics**:
- Discrete price bins instead of continuous ticks
- Dynamic fees that increase during high volatility
- Strategy modes: Spot, Curve, Bid-Ask
- Zero slippage within a single bin
- Extremely capital efficient for stablecoin pairs

### Meteora Dynamic Pools

Multi-token pools with single-sided deposit capability and volatility-adjusted fees.

```
Program ID: Eo7WjKq67rjJQSZxS6z3YkapzY3eMj6Xy8X5EQVn5UaB
Fee: Volatility-based dynamic fee
```

**Key characteristics**:
- Single-sided deposits allowed
- Dynamic fee based on recent price volatility
- Multi-token pool support
- Simpler LP experience than concentrated liquidity

### PumpSwap (PumpFun AMM)

PumpFun's native AMM for tokens that graduate from the bonding curve.

```
Program ID: PSwapMdSai8tjrEXcxFeQth87xC4rRsa4VA5mhGhXkP
Fee: 0.25% per swap (0.20% to LPs, 0.05% protocol)
Migration fee: 0 SOL (post-March 2025)
```

**Key characteristics**:
- Constant-product (`xy = k`) mechanics
- Automatic migration from PumpFun bonding curve at ~$69K market cap
- Creator coin rewards (10% of protocol fees to coin creators)

---

## 2. Fee Structure Comparison

| DEX | Pool Type | Fee Range | LP Share | Protocol Share |
|-----|-----------|-----------|----------|----------------|
| Raydium V4 | Constant Product | 0.25% fixed | 0.22% | 0.03% (RAY) |
| Raydium CLMM | Concentrated | 0.01%–2% | ~84% | ~16% |
| Orca Whirlpool | Concentrated | 0.01%–2% | 87% | 13% |
| Meteora DLMM | Bin-based | Dynamic | 80% | 20% |
| Meteora Dynamic | Dynamic | Variable | ~80% | ~20% |
| PumpSwap | Constant Product | 0.25% fixed | 0.20% | 0.05% |

**Fee tier selection guidance**:
- **0.01%**: Stablecoin pairs (USDC/USDT) — minimal price movement
- **0.05%**: Correlated assets (mSOL/SOL, jitoSOL/SOL) — low volatility
- **0.25%–0.30%**: Standard pairs (SOL/USDC) — moderate volatility
- **1%–2%**: Volatile/meme tokens — high impermanent loss risk

---

## 3. Pool Creation Patterns

### PumpFun Graduation Flow

Most new Solana meme tokens follow this lifecycle:

```
PumpFun Bonding Curve → ~$69K market cap → Migration → Raydium V4 or PumpSwap
```

1. Token launches on PumpFun bonding curve
2. As buys push market cap to ~$69K, the bonding curve completes
3. Liquidity migrates automatically to either Raydium V4 or PumpSwap
4. Since March 2025, PumpFun defaults migration to PumpSwap (their own AMM)
5. Post-migration, additional pools may be created on other DEXes

**Analysis implications**:
- Pools created via PumpFun graduation have known initial liquidity (~$12K)
- Very new graduated pools carry higher rug risk
- Check if creator LP tokens are locked or burnable

### Manual Pool Creation

Tokens not launched via PumpFun have pools created manually:
- Raydium V4 requires an OpenBook market + pool initialization
- Raydium CLMM, Orca, and Meteora allow direct pool creation
- Manual creation allows arbitrary initial liquidity amounts

---

## 4. Volume Efficiency (Volume/TVL Ratio)

Volume efficiency measures how actively a pool's liquidity is utilized:

```python
volume_efficiency = volume_24h / tvl
```

| V/TVL Ratio | Interpretation |
|-------------|---------------|
| > 5.0 | Very high turnover — likely wash trading or bot activity |
| 1.0–5.0 | Active trading — healthy, well-utilized pool |
| 0.1–1.0 | Moderate activity — normal for mid-cap tokens |
| < 0.1 | Low activity — stale or abandoned pool |
| 0.0 | No trades — dead pool |

**Fee APR estimation from volume efficiency**:

```python
fee_apr = volume_efficiency * fee_rate * 365
# Example: V/TVL of 2.0 at 0.25% fee = 2.0 * 0.0025 * 365 = 182.5% APR
```

This is a theoretical maximum — actual LP returns depend on impermanent loss, position range (for concentrated liquidity), and fee share.

---

## 5. Pool Health Metrics

### Core Metrics

```python
pool_health = {
    "tvl_usd": 150_000,          # Total value locked
    "volume_24h_usd": 300_000,   # 24-hour trading volume
    "volume_tvl_ratio": 2.0,     # Volume efficiency
    "fee_apr_estimate": 182.5,   # Annualized fee rate (%)
    "pool_age_hours": 720,       # Time since creation
    "lp_count_estimate": 45,     # Number of LP positions
    "tvl_trend_24h": -0.05,      # TVL change (-5%)
    "price_change_24h": 0.12,    # Price change (+12%)
}
```

### Red Flags

Watch for these warning signs when evaluating pools:

| Red Flag | Threshold | Risk |
|----------|-----------|------|
| Very new pool | < 24 hours old | Rug pull, unvetted token |
| Single LP | LP count = 1 | Creator can pull all liquidity |
| Declining TVL | > 20% drop in 24h | Liquidity flight |
| Zero volume | No trades in 6h+ | Dead or abandoned |
| Extreme V/TVL | > 10x | Wash trading, bot manipulation |
| Tiny TVL | < $1,000 | Massive slippage on any trade |

### Health Score Algorithm

```python
def compute_health_score(
    tvl_usd: float,
    volume_24h: float,
    pool_age_hours: float,
    lp_count: int,
    tvl_change_24h: float,
) -> float:
    """Score from 0-100 indicating pool health.

    Components (each 0-20):
    - TVL adequacy: Is there enough liquidity?
    - Volume efficiency: Is the pool actively traded?
    - Maturity: How long has the pool existed?
    - LP diversity: How many independent LPs?
    - TVL stability: Is liquidity growing or shrinking?
    """
    # TVL score (0-20): logarithmic scale, peaks at $1M+
    tvl_score = min(20, max(0, 5 * math.log10(max(tvl_usd, 1)) - 10))

    # Volume score (0-20): V/TVL ratio, sweet spot 0.5-3.0
    v_tvl = volume_24h / max(tvl_usd, 1)
    volume_score = min(20, max(0, v_tvl * 10)) if v_tvl < 5 else max(0, 20 - (v_tvl - 5) * 4)

    # Age score (0-20): older = more trusted
    age_score = min(20, pool_age_hours / 72 * 20)  # Max at 72h

    # LP diversity score (0-20)
    lp_score = min(20, lp_count * 2)  # Max at 10 LPs

    # Stability score (0-20): penalize large negative TVL changes
    stability_score = max(0, 20 + tvl_change_24h * 40)  # -50% → 0, 0% → 20

    return tvl_score + volume_score + age_score + lp_score + stability_score
```

---

## 6. Best Pool Selection for Execution

When multiple pools exist for a token pair, select the best one for trade execution:

```python
def rank_pools_for_execution(pools: list[dict], trade_size_usd: float) -> list[dict]:
    """Rank pools by execution quality for a given trade size.

    Factors:
    1. Sufficient TVL (trade size < 2% of TVL for acceptable slippage)
    2. Active volume (recent trades confirm the pool is live)
    3. Lowest fee tier (when liquidity is sufficient)
    4. Pool type efficiency (concentrated > constant product for same TVL)
    5. Pool health score (age, LP count, stability)
    """
    for pool in pools:
        size_ratio = trade_size_usd / max(pool["tvl_usd"], 1)
        pool["estimated_slippage"] = size_ratio * 100  # Rough % estimate

        # Prefer pools where trade is < 2% of TVL
        pool["size_ok"] = size_ratio < 0.02

        # Concentrated liquidity is more efficient
        efficiency_mult = 1.0
        if pool["pool_type"] in ("clmm", "whirlpool", "dlmm"):
            efficiency_mult = 0.3  # ~3x less slippage per TVL dollar

        pool["adjusted_slippage"] = pool["estimated_slippage"] * efficiency_mult
        pool["execution_score"] = (
            (1.0 / max(pool["adjusted_slippage"], 0.001)) * 0.5
            + pool.get("health_score", 50) * 0.3
            + (1.0 / max(pool["fee_rate"], 0.0001)) * 0.2
        )

    return sorted(pools, key=lambda p: p["execution_score"], reverse=True)
```

---

## 7. Program IDs Quick Reference

```python
PROGRAM_IDS = {
    "raydium_v4": "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8",
    "raydium_clmm": "CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK",
    "orca_whirlpool": "whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc",
    "meteora_dlmm": "LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo",
    "meteora_dynamic": "Eo7WjKq67rjJQSZxS6z3YkapzY3eMj6Xy8X5EQVn5UaB",
    "pumpswap": "PSwapMdSai8tjrEXcxFeQth87xC4rRsa4VA5mhGhXkP",
    "pumpfun_bonding": "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P",
}
```

---

## 8. Integration Points

### With `liquidity-analysis`
Use pool analysis to feed liquidity depth assessment. Pool type determines which liquidity model applies (constant product vs concentrated vs bin-based).

### With `lp-math`
Pool type determines which math formulas apply. Raydium V4 uses `xy = k`, CLMM/Whirlpool use tick-based math, DLMM uses bin math. See `lp-math` for full derivations.

### With `slippage-modeling`
Best pool selection directly feeds slippage estimation. Concentrated liquidity pools have different slippage curves than constant-product pools.

### With `jupiter-api`
Jupiter aggregates across all pool types automatically. Pool analysis helps understand *why* Jupiter routes through specific pools and validate route quality.

---

## 9. Workflow Example

```python
import httpx

# Step 1: Fetch all pools for a token from DexScreener
async def analyze_token_pools(token_mint: str) -> dict:
    url = f"https://api.dexscreener.com/tokens/v1/solana/{token_mint}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        pools = resp.json()

    results = []
    for pool in pools:
        dex = pool.get("dexId", "unknown")
        pool_info = {
            "dex": dex,
            "pool_address": pool.get("pairAddress"),
            "tvl_usd": pool.get("liquidity", {}).get("usd", 0),
            "volume_24h": pool.get("volume", {}).get("h24", 0),
            "age_hours": pool.get("pairCreatedAt", 0),
            "fee_rate": estimate_fee_rate(dex),
            "pool_type": classify_pool_type(dex),
        }
        pool_info["volume_efficiency"] = (
            pool_info["volume_24h"] / max(pool_info["tvl_usd"], 1)
        )
        results.append(pool_info)

    return {"token": token_mint, "pool_count": len(results), "pools": results}
```

---

## Files

### References
- `references/pool_mechanics.md` — Detailed mechanics for each pool type with program IDs and formulas
- `references/pool_analysis_guide.md` — Pool health metrics, red flags, volume efficiency, and best pool selection

### Scripts
- `scripts/analyze_pools.py` — Fetch and analyze all pools for a token, rank by execution quality
- `scripts/pool_monitor.py` — Monitor pool metrics over time, detect liquidity events

---

*This skill provides analysis tools and information for evaluating DEX pool characteristics. It does not provide financial advice or trading recommendations.*

### Referencia: references/pool_analysis_guide.md

# Pool Analysis Guide — Health Metrics, Red Flags & Best Pool Selection

Practical guide for evaluating DEX pool quality, detecting risks, and selecting optimal execution venues.

---

## Pool Health Metrics

### TVL (Total Value Locked)

Minimum TVL thresholds by trade size:

| Trade Size | Minimum TVL | Rationale |
|-----------|-------------|-----------|
| < $100 | $5,000 | < 2% impact |
| $100–$1K | $50,000 | Acceptable slippage |
| $1K–$10K | $250,000 | Professional execution |
| $10K–$100K | $1,000,000 | Institutional quality |
| > $100K | $5,000,000 | Deep liquidity required |

For concentrated liquidity pools, the relevant metric is **liquidity at the current price**, not total TVL. A $100K CLMM pool concentrated in a tight range can handle larger trades than a $500K constant-product pool.

### Volume/TVL Ratio (Volume Efficiency)

```python
volume_efficiency = volume_24h / tvl
```

| Ratio | Classification | Interpretation |
|-------|---------------|----------------|
| > 10.0 | Extreme | Almost certainly wash trading or bot loops |
| 5.0–10.0 | Very high | Suspicious — verify with tx analysis |
| 1.0–5.0 | High | Active, healthy pool |
| 0.3–1.0 | Moderate | Normal for mid-cap tokens |
| 0.05–0.3 | Low | Light trading, may have wide spreads |
| < 0.05 | Very low | Stale pool — check if still active |

### Fee APR Estimate

```python
# For constant-product pools
fee_apr = (volume_24h * fee_rate * 365) / tvl * 100

# For concentrated liquidity (position-specific)
fee_apr = (volume_24h * fee_rate * 365) / position_value * concentration_factor * 100
```

Note: Fee APR does not account for impermanent loss. Net LP return = Fee APR - IL.

### Pool Age

```python
pool_age_hours = (current_time - pool_created_at) / 3600
```

| Age | Risk Level | Notes |
|-----|-----------|-------|
| < 1 hour | Very high | Sniper bots active, volatile |
| 1–6 hours | High | Initial price discovery ongoing |
| 6–24 hours | Elevated | Settling but still risky |
| 1–7 days | Moderate | Established but young |
| > 7 days | Lower | Track record available |
| > 30 days | Base | Enough history for analysis |

### LP Count

Number of distinct liquidity providers. Higher LP count indicates more distributed (safer) liquidity.

| LP Count | Risk |
|----------|------|
| 1 | Critical — single entity controls all liquidity |
| 2–5 | High — few LPs, easy to rug |
| 5–20 | Moderate — reasonable distribution |
| 20–100 | Low — well distributed |
| > 100 | Very low — organic, mature pool |

---

## Red Flags Checklist

### Critical (Do Not Trade)

1. **Single LP with > 90% of liquidity**: Creator can rug by removing liquidity
2. **Pool age < 5 minutes with > $50K TVL**: Likely still in sniper phase
3. **TVL dropped > 50% in last hour**: Active liquidity removal in progress
4. **Zero volume for 24+ hours on a token with market cap > $100K**: Possible frozen/broken pool

### Warning (Proceed with Caution)

5. **V/TVL > 10**: Probable wash trading — real liquidity may be much lower
6. **Pool age < 24 hours**: Limited price history, higher manipulation risk
7. **TVL < $10,000**: High slippage even on small trades
8. **Only one pool exists**: No alternative venue if pool is compromised
9. **LP tokens not burned/locked**: Creator can remove liquidity at any time

### Informational

10. **Multiple pools on different DEXes**: Normal — compare for best execution
11. **V/TVL < 0.1**: Low activity but not necessarily dangerous
12. **Fee tier mismatch** (e.g., 0.01% fee on a meme token): Pool may not attract LPs

---

## Pool Creation Patterns

### PumpFun Graduation Flow

```
Bonding Curve Phase → ~$69K Market Cap → Migration → AMM Pool
```

**Timeline analysis**:
1. **T=0**: Token deploys on PumpFun bonding curve
2. **T=minutes to hours**: Trading on bonding curve (no traditional LP)
3. **T=graduation**: Market cap hits ~$69K, migration triggered
4. **T=graduation+seconds**: Pool created on Raydium V4 or PumpSwap
5. **T=graduation+minutes**: Sniper bots front-run organic traders
6. **T=graduation+1h**: Initial volatility settling

**Key checks after graduation**:
- Was the migration to Raydium V4 or PumpSwap?
- Is initial LP burned? (Check burn transaction)
- How many unique wallets traded in first hour?
- Did creator wallets sell in first 10 minutes?

### Organic Pool Creation

Non-PumpFun tokens may have pools created manually on any DEX:
- Check who created the pool (team wallet vs random)
- Verify initial liquidity amount is reasonable
- Look for simultaneous pool creation on multiple DEXes (professional launch)

---

## Best Pool Selection Algorithm

When a token has multiple pools across DEXes, use this ranking process:

### Step 1: Filter by Minimum Requirements

```python
def passes_minimum(pool: dict, trade_size_usd: float) -> bool:
    """Check if pool meets minimum requirements for execution."""
    min_tvl = trade_size_usd * 50  # Trade must be < 2% of TVL
    return (
        pool["tvl_usd"] >= min_tvl
        and pool["volume_24h"] > 0  # Must have recent activity
        and pool["pool_age_hours"] > 1  # Not brand new
    )
```

### Step 2: Estimate Execution Cost

```python
def estimate_execution_cost(pool: dict, trade_size_usd: float) -> float:
    """Estimate total cost: fee + slippage."""
    fee_cost = trade_size_usd * pool["fee_rate"]

    # Slippage depends on pool type
    if pool["pool_type"] in ("clmm", "whirlpool", "dlmm"):
        # Concentrated liquidity — lower slippage per TVL
        slippage_pct = (trade_size_usd / pool["tvl_usd"]) * 0.3
    else:
        # Constant product — standard slippage
        slippage_pct = trade_size_usd / pool["tvl_usd"]

    slippage_cost = trade_size_usd * slippage_pct
    return fee_cost + slippage_cost
```

### Step 3: Score and Rank

```python
def rank_pools(pools: list[dict], trade_size_usd: float) -> list[dict]:
    """Rank pools by total execution quality."""
    valid = [p for p in pools if passes_minimum(p, trade_size_usd)]

    for pool in valid:
        cost = estimate_execution_cost(pool, trade_size_usd)
        health = compute_health_score(pool)

        # Lower cost is better (invert for scoring)
        pool["cost_score"] = 1.0 / max(cost, 0.01)
        pool["health_score"] = health
        pool["total_score"] = pool["cost_score"] * 0.6 + health * 0.4

    return sorted(valid, key=lambda p: p["total_score"], reverse=True)
```

### Step 4: Verify Route

For the top-ranked pool, verify:
- Pool has had a trade in the last 30 minutes (still active)
- Current price in pool matches other pools within 2% (no stale pricing)
- Sufficient balance in the pool for the quote token you want to receive

---

## Practical Workflow: Token Pool Analysis

```python
# 1. Fetch all pools for a token
pools = fetch_pools_from_dexscreener(token_mint)

# 2. Classify each pool
for pool in pools:
    pool["pool_type"] = classify_by_dex(pool["dex_id"])
    pool["health"] = compute_health_score(pool)
    pool["flags"] = check_red_flags(pool)

# 3. Filter out critical-flag pools
safe_pools = [p for p in pools if not p["flags"]["critical"]]

# 4. Rank for execution
ranked = rank_pools(safe_pools, trade_size_usd=500)

# 5. Select best pool
best = ranked[0] if ranked else None
```

---

*This guide provides analytical frameworks for pool evaluation. It does not constitute financial advice or trading recommendations.*

### Referencia: references/pool_mechanics.md

# DEX Pool Mechanics — Solana AMM Comparison

Detailed mechanics for each major AMM pool type on Solana, including formulas, fee structures, and program IDs.

---

## Raydium V4 (Constant Product)

**Program ID**: `675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8`

### Mechanics
- Uses the constant-product invariant: `x * y = k`
- Full-range liquidity — every LP position covers price 0 to infinity
- Integrated with OpenBook (Serum successor) for hybrid AMM + orderbook routing

### Fee Structure
- **Swap fee**: 0.25% per trade
- **LP share**: 0.22% (88% of fee)
- **Protocol share**: 0.03% used for RAY token buyback

### Pool Creation
- Requires an OpenBook market ID
- Initial liquidity set by creator (both tokens deposited in equal USD value)
- Pool creation fee: ~0.4 SOL (for OpenBook market + pool accounts)

### Swap Formula
```
output = (reserve_out * amount_in * 9975) / (reserve_in * 10000 + amount_in * 9975)
```

The `9975/10000` factor encodes the 0.25% fee.

### Price Impact
```
price_impact = amount_in / (reserve_in + amount_in)
```

For a $1,000 trade against a pool with $100,000 in reserves: ~1% price impact.

---

## Raydium CLMM (Concentrated Liquidity)

**Program ID**: `CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK`

### Mechanics
- Concentrated liquidity (Uniswap V3-style) on Solana
- LPs choose a price range [P_low, P_high] for their position
- Liquidity only active when current price is within range
- Position represented as an NFT

### Fee Tiers and Tick Spacing

| Fee Tier | Tick Spacing | Use Case |
|----------|-------------|----------|
| 0.01% | 1 | Stablecoin pairs |
| 0.05% | 10 | Correlated assets (LSTs) |
| 0.25% | 60 | Standard pairs |
| 1.00% | 120 | Volatile pairs |
| 2.00% | 240 | Very volatile / meme tokens |

### Price-Tick Relationship
```
price = 1.0001^tick
tick = log(price) / log(1.0001)
```

### Liquidity Concentration Factor
```
concentration = sqrt(P_high / P_low) / (sqrt(P_high / P_low) - 1)
```

A position covering a +/-5% range has ~10x concentration vs full range. A +/-1% range has ~50x.

### Capital Efficiency
For a given TVL, concentrated positions provide more liquidity depth at the current price:
```
effective_liquidity = tvl * concentration_factor
```

---

## Orca Whirlpool (Concentrated Liquidity)

**Program ID**: `whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc`

### Mechanics
- Concentrated liquidity similar to Raydium CLMM
- Positions as NFTs with per-position fee tracking
- Mature SDK with strong TypeScript and Rust support

### Fee Tiers

| Fee Tier | Tick Spacing | Typical Use |
|----------|-------------|-------------|
| 0.01% | 1 | Stable pairs |
| 0.02% | 2 | Tightly correlated |
| 0.04% | 4 | LST pairs |
| 0.05% | 8 | Correlated assets |
| 0.16% | 16 | Mid-vol pairs |
| 0.30% | 64 | Standard pairs |
| 0.65% | 128 | Higher vol |
| 1.00% | 256 | Volatile pairs |
| 2.00% | 512 | Meme / high vol |

### Fee Distribution
- **LP share**: ~87% of swap fees
- **Protocol share**: ~13% to Orca treasury

### Key Differences from Raydium CLMM
- More fee tier options (9 vs 5)
- Different tick spacing mapping
- Separate reward mechanism for liquidity mining
- Generally higher TVL for major pairs (SOL/USDC, SOL/USDT)

---

## Meteora DLMM (Dynamic Liquidity Market Maker)

**Program ID**: `LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo`

### Mechanics
- **Bin-based** liquidity: each bin holds liquidity at a single discrete price
- Current active bin determines the current price
- LPs distribute tokens across multiple bins using strategy modes
- Zero slippage for trades that fit within a single bin

### Bin System
```
bin_price = (1 + bin_step / 10000) ^ (bin_id - 8388608)
```
- `bin_step`: 1-100 basis points between adjacent bins
- `bin_id`: integer index, 8388608 is the "zero" bin (price = 1.0)

### Strategy Modes

| Mode | Distribution | Best For |
|------|-------------|----------|
| **Spot** | Uniform across bins | General purpose, balanced exposure |
| **Curve** | Gaussian/bell curve around current price | Concentrated around expected price |
| **Bid-Ask** | Heavy on outer bins | Market-making, earning on mean reversion |

### Dynamic Fee
```
total_fee = base_fee + variable_fee
variable_fee = bin_step * volatility_accumulator
```

The variable fee increases during high-volatility periods (many bin crossings in recent swaps) and decays over time. This protects LPs from adverse selection during volatile moves.

### Fee Distribution
- **LP share**: ~80% of total fee
- **Protocol share**: ~20% to Meteora treasury

---

## Meteora Dynamic Pools

**Program ID**: `Eo7WjKq67rjJQSZxS6z3YkapzY3eMj6Xy8X5EQVn5UaB`

### Mechanics
- Constant-product base with dynamic fee adjustment
- Single-sided deposits permitted (the protocol rebalances internally)
- Fees adjust based on recent price volatility

### Key Features
- Lower barrier for LPs (no price range selection required)
- Volatility-based fee: higher fees during volatile periods, lower during calm
- Virtual price mechanism for fair LP token valuation

---

## PumpSwap

**Program ID**: `PSwapMdSai8tjrEXcxFeQth87xC4rRsa4VA5mhGhXkP`

### Mechanics
- Standard constant-product AMM (`xy = k`)
- Designed as the destination for PumpFun bonding curve graduations
- Launched March 2025, replacing Raydium V4 as default migration target

### Fee Structure
- **Swap fee**: 0.25% per trade
- **LP share**: 0.20% (80%)
- **Protocol share**: 0.05% (20%), with 10% of protocol fees going to coin creators

### Migration Details
- Migration from bonding curve is automatic at ~$69K market cap
- Migration fee: 0 SOL (reduced from 6 SOL in original Raydium migration)
- Initial pool liquidity: ~85 SOL + all remaining tokens from bonding curve

---

## Program ID Quick Reference

| DEX | Program ID |
|-----|-----------|
| Raydium V4 | `675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8` |
| Raydium CLMM | `CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK` |
| Orca Whirlpool | `whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc` |
| Meteora DLMM | `LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo` |
| Meteora Dynamic | `Eo7WjKq67rjJQSZxS6z3YkapzY3eMj6Xy8X5EQVn5UaB` |
| PumpSwap | `PSwapMdSai8tjrEXcxFeQth87xC4rRsa4VA5mhGhXkP` |
| PumpFun Bonding | `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P` |

---

## Comparison Summary

| Feature | Raydium V4 | Raydium CLMM | Orca Whirlpool | Meteora DLMM | PumpSwap |
|---------|-----------|-------------|----------------|-------------|----------|
| Model | xy=k | Concentrated | Concentrated | Bin-based | xy=k |
| Fee | 0.25% fixed | 0.01-2% | 0.01-2% | Dynamic | 0.25% fixed |
| Capital efficiency | 1x | 10-100x | 10-100x | 10-50x | 1x |
| LP complexity | Low | High | High | Medium | Low |
| Slippage model | Continuous | Tick-based | Tick-based | Bin-based | Continuous |
| Position type | LP tokens | NFT | NFT | NFT | LP tokens |
| Dynamic fee | No | No | No | Yes | No |

*This reference provides technical information about pool mechanics. It does not constitute financial advice.*


---

## SKILL: digital-assets

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/digital-assets` (MIT)
- Cuándo usarla: Analyze digital assets including cryptocurrency fundamentals, blockchain mechanics, DeFi protocols, and on-chain metrics. Use when the user asks about crypto investing, Bitcoin, Ethereum, staking yields, DeFi lending, impermanent loss, or on-chain valuation metrics. Also trigger when users mention 'blockchain', 'proof of stake', 'proof of work', 'smart contracts', 'NFTs', 'stablecoins', 'NVT ratio', 'TVL', 'crypto portfolio allocation', 'halving', or ask about risks and returns of cryptocurrency.

# Digital Assets

## Core Concepts

### Blockchain Fundamentals
A distributed ledger maintained by a network of nodes. Transactions are grouped into blocks, cryptographically linked in sequence. Immutability comes from the chain structure — altering any block requires recomputing all subsequent blocks. Consensus mechanisms determine how the network agrees on the valid state of the ledger.

### Consensus Mechanisms
**Proof of Work (PoW):** Miners compete to solve computational puzzles. The winner adds the next block and earns a reward. High energy consumption but battle-tested security (Bitcoin). Security scales with hash rate.

**Proof of Stake (PoS):** Validators lock up tokens as collateral ("stake"). Block proposers are selected based on stake weight. Slashing penalizes malicious behavior. Far more energy-efficient than PoW. Ethereum transitioned to PoS in September 2022.

### Bitcoin
Fixed supply of 21 million coins, enforced by protocol rules. Block reward halves approximately every 4 years (halving cycle), reducing new supply issuance. The block reward is 3.125 BTC following the April 2024 halving (next halving expected ~2028, dropping to 1.5625 BTC). Mining reward = block reward + transaction fees. Scarcity narrative drives the "digital gold" thesis.

### Ethereum
The leading smart contract platform. The Ethereum Virtual Machine (EVM) executes arbitrary programs (smart contracts). Gas fees compensate validators for computation. EIP-1559 introduced a base fee that is burned (destroyed), making ETH potentially deflationary when network usage is high. The merge to PoS (Sept 2022) reduced energy usage by ~99.95%.

### Staking Yield
For Proof of Stake networks:

Staking Yield = (Rewards + MEV Tips - Validator Costs) / Staked Amount

Rewards come from new token issuance and transaction fees. MEV (Maximal Extractable Value) provides additional income from transaction ordering. Validator costs include hardware, bandwidth, and the risk of slashing. Real yield (after accounting for inflation of token supply) can be significantly lower than nominal yield.

### DeFi (Decentralized Finance)
- **Lending protocols (Aave, Compound):** Users deposit assets to earn interest; borrowers post collateral to borrow. Interest rates are algorithmically determined by supply/demand (utilization rate).
- **DEXs (Uniswap, Curve):** Decentralized exchanges using automated market makers instead of order books. Liquidity providers deposit token pairs and earn trading fees.
- **Yield farming:** Deploying capital across DeFi protocols to maximize yield, often involving multiple protocol interactions and leverage.

### Automated Market Maker (AMM)
The constant product formula: x * y = k

where x and y are the reserves of two tokens in a liquidity pool. Price is determined by the ratio of reserves. Large trades cause slippage (price impact proportional to trade size relative to pool depth).

### Impermanent Loss
The loss that liquidity providers experience relative to simply holding the tokens when prices change:

IL = 2 * sqrt(p_ratio) / (1 + p_ratio) - 1

where p_ratio = new_price / old_price for one token relative to the other. At a 2x price change, IL is approximately 5.7%. At a 5x change, IL is approximately 25.5%. "Impermanent" because the loss reverses if prices return to original levels — but it becomes permanent if the LP withdraws at diverged prices.

### On-Chain Metrics
- **NVT Ratio (Network Value to Transactions):** Market cap / daily transaction volume (on-chain). Analogous to P/E for equities. Higher NVT suggests overvaluation relative to network usage.
- **Active addresses:** Number of unique addresses transacting daily. Proxy for network adoption.
- **Hash rate (PoW):** Total computational power securing the network. Higher hash rate = more security.
- **TVL (Total Value Locked):** Total value of assets deposited in DeFi protocols. Measure of DeFi ecosystem size.

### Stablecoin Types
- **Fiat-backed (USDC, USDT):** Each token backed by reserves of fiat currency or equivalents. Centralized issuance and custody.
- **Crypto-backed (DAI):** Overcollateralized with cryptocurrency. Decentralized but capital-inefficient.
- **Algorithmic:** Maintain peg through minting/burning mechanisms without full collateral backing. Higher risk of de-peg (e.g., UST/Luna collapse in 2022).

### Token Valuation
No universally accepted model. Approaches include:
- NVT ratio (compare to peers and historical range)
- Fees/revenue analysis (protocol revenue as proxy for earnings)
- TVL multiples (market cap / TVL)
- Fully diluted valuation (FDV) vs circulating supply market cap
- Discounted cash flow on protocol fee revenue (experimental)

### Custody
**Self-custody:** Hardware wallets (Ledger, Trezor) or software wallets. User controls private keys. "Not your keys, not your coins." Risk of loss if keys are lost.

**Custodial:** Exchanges (Coinbase, Kraken) or qualified custodians hold assets on behalf of users. Convenience but counterparty risk (e.g., FTX collapse).

### Regulatory Considerations
Regulatory treatment is evolving. In the US, crypto is generally treated as property for tax purposes — each sale, exchange, or use is a taxable event. Securities classification (Howey test) remains contentious for many tokens. Regulatory clarity is improving but varies significantly by jurisdiction.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Staking Yield | (Rewards + MEV - Costs) / Staked Amount | Validator return |
| Impermanent Loss | 2*sqrt(p_ratio)/(1+p_ratio) - 1 | LP loss from price divergence |
| AMM Price | Price_x = y/x (for token x in terms of y) | DEX pricing |
| NVT Ratio | Market Cap / Daily On-Chain Tx Volume | Network valuation metric |
| Real Staking Yield | Nominal Yield - Token Inflation Rate | Inflation-adjusted return |

## Worked Examples

### Example 1: Staking Yield on Ethereum
**Given:** 32 ETH staked (one validator), 4.5% APR nominal yield, ETH price = $3,000
**Calculate:** Annual rewards in ETH and USD
**Solution:**
Annual ETH rewards = 32 ETH × 4.5% = 1.44 ETH
Annual USD value = 1.44 ETH × $3,000 = $4,320
Total staked value = 32 × $3,000 = $96,000

If ETH supply inflation is approximately 0.5% per year (net of EIP-1559 burns), the real staking yield is roughly 4.5% - 0.5% = 4.0%. Note that the USD return depends entirely on ETH price changes — a 10% decline in ETH price would far exceed the 4.5% staking yield.

### Example 2: Impermanent Loss Calculation
**Given:** A liquidity provider deposits equal value of ETH and USDC into a Uniswap pool. ETH price doubles from $2,000 to $4,000.
**Calculate:** Impermanent loss
**Solution:**
p_ratio = $4,000 / $2,000 = 2.0
IL = 2 × sqrt(2.0) / (1 + 2.0) - 1
IL = 2 × 1.4142 / 3.0 - 1
IL = 2.8284 / 3.0 - 1
IL = 0.9428 - 1 = -0.0572 = -5.72%

The LP's position is worth 5.72% less than if they had simply held the tokens. If the pool earned 8% in trading fees over the period, the net return is 8% - 5.72% = 2.28% — still positive but substantially reduced. If ETH had tripled (p_ratio = 3), IL would be approximately 13.4%, potentially exceeding fee income.

## Common Pitfalls
- Confusing APR with APY — compounding matters significantly at high yield rates (100% APR ≈ 171.8% APY)
- Impermanent loss can exceed trading fee income — LPs can have negative returns even in active pools if price divergence is large
- Smart contract risk in DeFi protocols — bugs, exploits, and rug pulls can result in total loss of deposited funds
- Comparing crypto "yields" to traditional fixed income — very different risk profiles; crypto yields compensate for smart contract risk, impermanent loss, token price volatility, and regulatory uncertainty

## Cross-References
- **historical-risk** (wealth-management plugin): volatility and risk measurement (crypto exhibits extreme volatility)
- **currencies-and-fx** (wealth-management plugin): stablecoin and crypto-fiat exchange dynamics
- **alternatives** (wealth-management plugin): crypto as an alternative asset class
- **tax-efficiency** (wealth-management plugin): cryptocurrency tax reporting and optimization


---

## SKILL: funding-digest

- Fuente: `anthropics/financial-services` → `plugins/partner-built/spglobal/skills/funding-digest` (Apache-2.0)
- Cuándo usarla: Generate a polished one-page PowerPoint slide summarizing key takeaways from recent funding rounds and notable capital markets activity across a user's watched sectors or companies. Use this skill when the user asks for a deal flow summary, weekly recap, funding digest, transaction roundup, or capital markets briefing. Triggers on: 'deal flow digest', 'weekly funding recap', 'deal roundup', 'transaction summary this week', 'what happened in [sector] this week', 'capital markets update', or any request to compile recent funding activity into a briefing slide. Produces a professional single-slide PPTX with key takeaways, valuation data, and Capital IQ deal links.

**AI DISCLAIMER (MANDATORY):**
You MUST include the following disclaimer text in the powerpoint footer. This is not optional — the report is incomplete without it:

> **"Analysis is AI-generated — please confirm all outputs"**

**Footer** — At the bottom of the generated slide, as a prominent yellow banner: "Analysis is AI-generated — please confirm all outputs"

---

# Weekly Deal Flow Digest

Generate an analyst-quality **single-slide PowerPoint** that summarizes key takeaways from recent funding rounds across watched sectors or companies, using S&P Global Capital IQ data. Each deal links back to its Capital IQ profile for quick drill-down.

## When to Use

Trigger on any of these patterns:
- "Give me a deal flow digest for this week"
- "Weekly funding recap for [sector]"
- "What deals closed in [sector/companies] recently?"
- "Transaction roundup" or "deal roundup"
- "Capital markets update for my coverage universe"
- "Summarize recent funding activity"
- Any periodic briefing request about deals, raises, or rounds

## Nested Skills

This skill produces a one-slide PPTX briefing:
- **Read** `/mnt/skills/public/pptx/SKILL.md` before generating the PowerPoint (and its sub-reference `pptxgenjs.md` for creating from scratch)

## Entity Resolution & Tool Robustness

S&P Global's identifier system resolves company names to legal entities. This works well for most companies but has known failure modes that cause empty results. **Apply these rules throughout the workflow to avoid silent data loss.**

### Rule 0: Pre-validate ALL identifiers before querying funding

**Before** calling any funding tools, run every identifier through `get_info_from_identifiers`. This is the cheapest and most reliable way to catch problems early. Check two things in the response:

1. **Did it resolve at all?** If the identifier returns empty/error, the name doesn't exist in S&P Global. Try the alias from `references/sector-seeds.md`, the legal entity name, or the `company_id` directly.
2. **What is the `status` field?** 
   - `"Operating"` → Safe to query for funding rounds.
   - `"Operating Subsidiary"` → The company exists but is owned by a parent. It will return **zero funding rounds**. Note this in the digest as context (e.g., "acquired by [Parent]") but do not query for funding.
   - Any other status (e.g., closed, inactive) → The company is no longer operating. Historical data may exist but no new activity.

**This single pre-validation step prevents the majority of empty-result issues.** Batch all candidates into a single `get_info_from_identifiers` call (it handles large batches well) and triage before proceeding.

### Rule 1: Never trust empty results without a fallback

If `get_rounds_of_funding_from_identifiers` returns empty for a company you expect to have data:
1. **Try the legal entity name or company_id.** Brand names usually work, but some don't. See the alias table in `references/sector-seeds.md` for known mismatches. Common pattern: "[Brand] AI" → "[Legal Name], Inc." (e.g., Together AI → "Together Computer, Inc.", Character.ai → "Character Technologies, Inc.", Runway ML → "Runway AI, Inc.").
2. **Verify the company exists in S&P.** If you skipped Rule 0, call `get_info_from_identifiers(identifiers=["Company"])` now — if this also returns empty, the company may be too early-stage or not yet indexed.

### Rule 2: Subsidiaries have no funding rounds

Companies that are divisions or wholly-owned subsidiaries of larger companies (e.g., DeepMind under Alphabet, GitHub under Microsoft, BeReal under Voodoo) will return **zero funding rounds**. Their capital events are tracked at the parent level.

**How to detect:** The `status` field from `get_info_from_identifiers` will show `"Operating Subsidiary"`. The `references/sector-seeds.md` file also flags known subsidiaries with ⚠️ warnings. Skip these for funding queries.

### Rule 3: Use `get_rounds_of_funding_from_identifiers` as the primary tool, not `get_funding_summary_from_identifiers`

The summary tool is faster but less reliable — it can return errors or incomplete data even when detailed rounds exist. Always use the detailed rounds tool as the primary data source. The summary tool is acceptable only for quick aggregate checks (total raised, round count) and should be verified against the rounds tool if results seem low.

### Rule 4: Batch carefully and validate

When processing large company universes (50+ companies), batch in groups of 15–20. After each batch, check for companies that returned empty results and run them through the fallback steps in Rule 1 before moving on.

### Rule 5: The `role` parameter is critical

- `company_raising_funds` → "What rounds did X raise?" (company perspective)
- `company_investing_in_round_of_funding` → "What did investor Y invest in?" (investor perspective)

Using the wrong role returns empty results silently. For deal flow digests, you almost always want `company_raising_funds`. Only use the investor role when specifically analyzing an investor's portfolio activity.

### Rule 6: Identifier resolution is case-insensitive but spelling-sensitive

S&P Global handles case variations ("openai" = "OpenAI") but is strict on spelling and punctuation. "Character AI" may fail where "Character.ai" succeeds. When in doubt, use the `company_id` (e.g., `C_1829047235`) which is guaranteed to resolve.

## Workflow

### Step 1: Establish Coverage & Period

Determine what the digest should cover. There are two setups:

**Returning user (has a watchlist):**
If the user has previously defined sectors or companies to track, use that list. Check conversation history for prior watchlists.

**New user:**
Ask for:

| Parameter | Default | Notes |
|-----------|---------|-------|
| **Sectors** | *(at least one)* | e.g., "AI, Fintech, Biotech" |
| **Specific companies** | Optional | Supplement sector-level coverage |
| **Time period** | Last 7 days | "This week", "last 2 weeks", "this month" |

Calculate the exact `start_date` and `end_date` from the time period.

### Step 2: Build the Company Universe

For each sector specified, build a company universe using a validated bootstrapping approach:

1. **Seed companies** from domain knowledge (see `references/sector-seeds.md`)
   - Pay attention to the ⚠️ warnings and alias notes in the seeds file — some well-known companies are subsidiaries, have been acquired, or require a specific legal name to resolve.
   - The seeds file includes `company_id` values for known alias mismatches. Use these directly if the brand name fails.

2. **Pre-validate all seeds immediately** (Rule 0):
   ```
   get_info_from_identifiers(identifiers=[all_seeds_for_this_sector])
   ```
   Triage the results into two buckets:
   - ✅ **Resolved & Operating** (`status` = "Operating") → proceed to competitor expansion
   - ❌ **Unresolved or Subsidiary** → retry with alias/legal name from seeds file; subsidiaries are noted for context but excluded from funding queries

3. **Expand via competitors** (using only the ✅ resolved seeds):
   ```
   get_competitors_from_identifiers(identifiers=[resolved_seeds], competitor_source="all")
   ```

4. **Validate expanded universe:**
   ```
   get_info_from_identifiers(identifiers=[new_competitors])
   ```
   Apply the same triage. Filter by `simple_industry` matching the target sector. Drop any unresolved names or subsidiaries.

If the user provides specific companies, add those directly but still run them through the pre-validation triage. Never skip validation — even well-known brand names can fail silently.

Keep the universe manageable — aim for 15–40 **resolved, operating** companies per sector. For a multi-sector digest, this might total 50–100+ companies.

### Step 3: Pull Funding Rounds

For all companies in the universe:

```
get_rounds_of_funding_from_identifiers(
    identifiers=[batch],
    role="company_raising_funds",
    start_date="YYYY-MM-DD",
    end_date="YYYY-MM-DD"
)
```

Process in batches of 15–20 if the universe is large.

**After each batch, identify companies with empty results.** For any company expected to have activity:
1. Retry with the legal entity name or alternate identifier (see Entity Resolution rules above).
2. Log the company as "no data" only after exhausting fallbacks.

Collect all `transaction_id` values from successful results, then enrich with detailed round info:

```
get_rounds_of_funding_info_from_transaction_ids(
    transaction_ids=[all_funding_ids]
)
```

Pass ALL transaction IDs in a single call (or small number of calls) rather than one per transaction — the tool handles batches efficiently.

**Extract the following from each round (critical for the slide):**
- `transaction_id` — needed for the Capital IQ deal link
- **Announcement date** — when the round was publicly announced
- **Close date** — when the round officially closed
- Amount raised
- **Pre-money valuation** (if disclosed)
- **Post-money valuation** (if disclosed)
- Lead investors
- Round type (Series A, B, C, etc.)
- Security terms
- Advisors
- Pricing trend (up-round / down-round / flat)

> **Dates are required.** The announcement and close dates must always appear in the final slide's deal table. If only one date is available, show it and mark the other as "—".

### Step 4: Pull Company Context for Notable Deals

For any company involved in a significant deal (large round, notable valuation shift), get a brief description:

```
get_company_summary_from_identifiers(identifiers=[notable_companies])
```

This adds context to the narrative (e.g., "The company, an AI infrastructure startup founded in 2021, is expanding into...").

### Step 5: Identify Highlights & Trends

Before designing the slide, analyze the data to surface the story:

**Flag as "Notable":**
- Rounds ≥ $100M
- Down rounds (pricing trend = down)
- New unicorns (post-money valuation crossing $1B)
- Significant valuation jumps (post-money ≥ 2x the last known valuation)
- Repeat raisers (same company raising again within 6 months)
- Unusually large investor syndicates

**Identify Trends:**
- Total capital deployed this period vs. typical (if historical data available)
- Which sub-sectors are hottest (most rounds, most capital)
- Round stage distribution (is early-stage or late-stage dominating?)
- Most active investors across the digest
- Geographic concentration
- Valuation trends (are pre-money valuations compressing or expanding?)

**Select Key Takeaways (3–5):**
Distill the most important signals into 3–5 concise bullet-style takeaways. These are the centerpiece of the slide. Each takeaway should be one sentence, punchy, and data-backed.

Examples:
- "AI sector raised $2.4B across 8 rounds — 3x the prior week, led by a $800M mega-round from [Company] at a $12B post-money valuation."
- "[Company] closed a $200M Series D at $3.5B pre-money, up from $1.8B in its Series C — signaling strong demand for AI developer tools."
- "Down-round activity ticked up: 2 of 6 late-stage rounds priced below prior valuations."

### Step 6: Generate Company Logos

For each company featured in the key takeaways or notable deals, generate a logo using a two-tier local pipeline. **Do not use Clearbit** (`logo.clearbit.com`) — it is deprecated and consistently fails. External logo CDNs (Brandfetch, logo.dev, Google Favicons) require API keys or are blocked by network restrictions. Instead, use the following approach:

#### Tier 1: `simple-icons` npm Package (3,300+ Brand SVGs, No Network Required)

The `simple-icons` package bundles high-quality SVG icons for thousands of well-known brands. It works entirely offline — no API keys, no network calls. Install it alongside `sharp` for SVG → PNG conversion:

```bash
npm install simple-icons sharp
```

**Lookup strategy:**

```javascript
const si = require('simple-icons');
const sharp = require('sharp');

// Find an icon by exact title match (case-insensitive)
function findSimpleIcon(companyName) {
    // Try exact match first
    for (const [key, val] of Object.entries(si)) {
        if (!key.startsWith('si') || !val || !val.title) continue;
        if (val.title.toLowerCase() === companyName.toLowerCase()) return val;
    }
    // Try without common suffixes (AI, Inc., Corp.)
    const stripped = companyName.replace(/\s*(AI|Inc\.?|Corp\.?|Ltd\.?)$/i, '').trim();
    if (stripped !== companyName) {
        for (const [key, val] of Object.entries(si)) {
            if (!key.startsWith('si') || !val || !val.title) continue;
            if (val.title.toLowerCase() === stripped.toLowerCase()) return val;
        }
    }
    return null;
}

// Convert SVG to PNG with the brand's official color
async function simpleIconToPng(icon, outputPath) {
    const coloredSvg = icon.svg.replace('<svg', `<svg fill="#${icon.hex}"`);
    await sharp(Buffer.from(coloredSvg))
        .resize(128, 128, { fit: 'contain', background: { r: 255, g: 255, b: 255, alpha: 0 } })
        .png()
        .toFile(outputPath);
}
```

**Coverage:** ~43% of typical deal flow companies (strong for major tech brands like Stripe, Anthropic, Databricks, Snowflake, Discord, Shopify, SpaceX, Mistral AI, Hugging Face; weaker for niche fintech, biotech, or early-stage companies).

#### Tier 2: Initial-Based Fallback via `sharp` (100% Coverage)

For companies not found in `simple-icons`, generate a clean initial-based logo as a PNG:

```javascript
async function generateInitialLogo(companyName, outputPath) {
    const initial = companyName.charAt(0).toUpperCase();
    const svg = `
    <svg width="128" height="128" xmlns="http://www.w3.org/2000/svg">
        <circle cx="64" cy="64" r="64" fill="#BDBDBD"/>
        <text x="64" y="64" font-family="Arial, Helvetica, sans-serif"
              font-size="56" font-weight="bold" fill="#FFFFFF"
              text-anchor="middle" dominant-baseline="central">${initial}</text>
    </svg>`;
    await sharp(Buffer.from(svg)).png().toFile(outputPath);
}
```

#### Complete Pipeline

```javascript
async function fetchLogo(companyName, outputDir) {
    const fileName = companyName.toLowerCase().replace(/[\s.]+/g, '-') + '.png';
    const outPath = path.join(outputDir, fileName);

    // Tier 1: Try simple-icons
    const icon = findSimpleIcon(companyName);
    if (icon) {
        await simpleIconToPng(icon, outPath);
        return { path: outPath, source: 'simple-icons' };
    }

    // Tier 2: Generate initial-based fallback
    await generateInitialLogo(companyName, outPath);
    return { path: outPath, source: 'initial-fallback' };
}
```

**Logo guidelines:**
- Save all logos to `/home/claude/logos/[company-name].png`
- All logos are 128×128 PNG with transparent backgrounds
- On the slide, display logos at 0.35"–0.5" tall — they're accents, not focal points
- Initial-fallback circles use gray (`BDBDBD`) fill with white text — consistent with the monochrome palette
- Never mix logo styles randomly — if most companies resolve to brand icons, the few fallbacks should blend in naturally

### Step 7: Generate the One-Page PPTX

Read `/mnt/skills/public/pptx/SKILL.md` and `/mnt/skills/public/pptx/pptxgenjs.md` before creating the slide.

Create a **single-slide** PowerPoint using `pptxgenjs`. The slide should be information-dense but visually clean — think "executive dashboard" not "wall of text."

#### Slide Layout

```
┌─────────────────────────────────────────────────────────────┐
│  DEAL FLOW DIGEST                                           │
│  [Period] · [Sectors]                           [Date]      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│  │  $X.XB  │  │  N      │  │  $X.XB  │  │  $X.XB  │       │
│  │ Raised  │  │ Rounds  │  │ Avg Pre │  │ Largest │       │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘       │
│                                                             │
│  KEY TAKEAWAYS                                              │
│  ─────────────────────────────────────────────────          │
│  [Logo] Takeaway 1 text goes here...                        │
│  [Logo] Takeaway 2 text goes here...                        │
│  [Logo] Takeaway 3 text goes here...                        │
│  [Logo] Takeaway 4 text goes here...                        │
│                                                             │
│  TOP DEALS                                                  │
│  ┌──────────────────────────────────────────────────────────┐│
│  │Company│Type │Announced│Closed│Amount│Pre-$│Post-$│Lead│🔗││
│  │───────│─────│─────────│──────│──────│─────│──────│────│──││
│  │ ...   │ ... │  ...    │ ...  │ ...  │ ... │ ...  │... │🔗││
│  └──────────────────────────────────────────────────────────┘│
│                                                             │
│  [Footer: Deal Flow Digest · Sources: S&P Global Capital IQ]│
│  [Footer: AI Disclaimer]                                    │
└─────────────────────────────────────────────────────────────┘
```

#### Design Specifications

**Color philosophy: Minimal, monochrome-first.** The slide should feel like a high-end financial brief — black, white, and gray dominate. Color is used **only** where it carries meaning (e.g., a red indicator for a down round, a green indicator for a standout metric) or where the reader would naturally expect it (company logos). Never use color for purely decorative purposes like background fills, accent bars, or gradient effects.

**Color palette — Monochrome Executive:**
- Primary background: `FFFFFF` (white) — clean, open slide background
- Header bar: `1A1A1A` (near-black) — strong contrast for the title region
- Primary text: `1A1A1A` (near-black) — all body text, stat numbers, takeaways
- Secondary text: `6B6B6B` (medium gray) — labels, captions, footer, date stamps
- Borders & dividers: `D0D0D0` (light gray) — subtle structural lines, card outlines, table borders
- Card backgrounds: `F5F5F5` (off-white / very light gray) — stat card fills, alternating table rows
- Link text: `2B5797` (muted blue) — Capital IQ deal links in the table (the only blue on the slide)
- **Semantic color (sparingly):**
  - Down rounds or negative signals: `C0392B` (muted red) — use only as a small dot, tag, or single-word highlight, never as a fill or background
  - Standout positive metrics (new unicorn, outsized round): `2E7D32` (muted green) — same minimal usage: a dot, a small tag, or a single highlighted number
  - If no data points warrant a color indicator, **use no color at all**. A fully monochrome slide is perfectly correct.

**Typography:**
- Title: 28–32pt, bold, white on near-black header bar
- Stat numbers: 36–44pt, bold, near-black
- Stat labels: 10–12pt, medium gray (`6B6B6B`)
- Takeaway text: 12–14pt, near-black, left-aligned
- Table text: 9–11pt, near-black with gray (`6B6B6B`) for secondary columns
- Link text: 9–10pt, muted blue (`2B5797`)
- Footer: 8pt, medium gray

**Stat Cards (top row):**
- 4 key metrics as large-number callouts: Total Raised, # Rounds, Avg Pre-Money Valuation, Largest Round
- Each in a card with `F5F5F5` fill and a thin `D0D0D0` border — no shadow, no color fills
- If a stat is surprising or extreme (e.g., 3x normal volume, a record deal), a small colored dot or underline may be placed next to that single number — otherwise keep fully monochrome
- If pre-money valuations are mostly undisclosed, substitute with a different metric (e.g., Median Round Size, # New Unicorns)

**Key Takeaways (middle section):**
- 3–5 one-line takeaways, each prefixed with the relevant company logo (small, ~0.35" tall)
- If no logo available, use a **gray circle** with the company initial in white — not a colored circle
- Left-aligned, with enough spacing to breathe
- Down-round or negative takeaways may use a small red dot prefix; otherwise no color
- Include valuation context where available (e.g., "at a $5B post-money valuation")

**Top Deals Table (bottom section):**
- Compact table showing the 4–6 most notable deals
- Columns: Company, Type (Series X), Announced (date), Closed (date), Amount ($M), Pre-Money ($M), Post-Money ($M), Lead Investor, Deal Link
- **Announced** and **Closed** columns show dates in `MMM DD` format (e.g., "Jan 15"). These columns are required and must always be present. If a date is not available, show "—".
- The **Deal Link** column contains a clickable "View →" text linking to Capital IQ:
  ```
  https://www.capitaliq.spglobal.com/web/client?#offering/capitalOfferingProfile?id=<transaction_id>
  ```
  where `<transaction_id>` is the `transaction_id` from `get_rounds_of_funding_from_identifiers`.
- If pre-money or post-money valuation is not disclosed, show "—" in that cell
- Header row with near-black (`1A1A1A`) fill and white text; alternating rows in `F5F5F5` and `FFFFFF`
- **Center the table horizontally** on the slide. Calculate the table's total width, then set `x` so it is centered within the slide width: `x = (slideWidth - tableWidth) / 2`. For a 16:9 layout (13.33" wide), if the table is 12" wide, use `x = 0.67`. Never left-align the table to the slide edge.
- Keep it tight — this is a reference, not the focal point
- No colored fills in table cells. If a deal is a down round, a small red text tag "(↓ down)" may appear next to the amount — that is the only permitted color in the table.

**Deal Link Implementation (pptxgenjs):**
In pptxgenjs, hyperlinks are added to table cells using the `options.hyperlink` property on the cell object:
```javascript
// Table cell with Capital IQ deal link
{
  text: "View →",
  options: {
    hyperlink: {
      url: `https://www.capitaliq.spglobal.com/web/client?#offering/capitalOfferingProfile?id=${transactionId}`
    },
    color: "2B5797",
    fontSize: 9,
    fontFace: "Arial"
  }
}
```

**Table Centering (pptxgenjs):**
Always center the deal table on the slide. Calculate the x position dynamically:
```javascript
const SLIDE_W = 13.33; // 16:9 slide width
const TABLE_W = 12.5;  // total table width (sum of all column widths)
const TABLE_X = (SLIDE_W - TABLE_W) / 2; // ≈ 0.42"

slide.addTable(tableRows, {
  x: TABLE_X,
  y: tableY,
  w: TABLE_W,
  colW: [1.8, 0.9, 0.9, 0.9, 1.0, 1.1, 1.2, 1.6, 0.7], // Company, Type, Announced, Closed, Amount, Pre-$, Post-$, Lead, Link
  // ... other options
});
```
Adjust `colW` values as needed, but always recompute `TABLE_X` from `(SLIDE_W - sum(colW)) / 2` to keep the table centered.

**Footer:**
- Small text in medium gray: "Deal Flow Digest · [Period] · Sources: S&P Global Capital IQ · Generated [Date]"

**General color rules (enforce strictly):**
- Company logos are the only "full color" elements on the slide — they appear as-is from the source.
- Deal links use muted blue (`2B5797`) — this is the only non-monochrome text color besides semantic red/green.
- Outside of logos and links, the slide should look correct printed on a black-and-white printer.
- Never apply color to backgrounds, accent bars, decorative shapes, or section dividers.
- When in doubt, leave it gray.

#### Code Structure

```javascript
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "Deal Flow Digest";

const slide = pres.addSlide();
const SLIDE_W = 13.33; // 16:9 slide width in inches

// 1. Dark header bar with title and period
// 2. Stat cards row (4 cards: Total Raised, # Rounds, Avg Pre-Money, Largest Round)
// 3. Key takeaways section with logos (include valuation context)
// 4. Top deals table with Announced, Closed, Pre-Money, Post-Money columns and Capital IQ deal links
//    - Center the table: x = (SLIDE_W - tableWidth) / 2
// 5. Footer

pres.writeFile({ fileName: "/home/claude/deal-flow-digest.pptx" });
```

Use factory functions (not shared objects) for shadows and repeated styles per the pptxgenjs pitfalls guidance.

### Step 8: QA the Slide

Follow the QA process from the PPTX skill:

1. **Content QA:** `python -m markitdown deal-flow-digest.pptx` — verify all text, numbers, company names, valuation figures, and deal links are correct
2. **Visual QA:** Convert to image and inspect:
   ```bash
   python /mnt/skills/public/pptx/scripts/office/soffice.py --headless --convert-to pdf deal-flow-digest.pptx
   pdftoppm -jpeg -r 200 deal-flow-digest.pdf slide
   ```
   Check for overlapping elements, text overflow, alignment issues, low-contrast text, logo sizing problems, and that deal link text is visible.
3. **Link QA:** Verify that the Capital IQ URLs in the table are correctly formatted with the right transaction IDs.
4. **Fix and re-verify** — at least one fix-and-verify cycle before declaring done.

### Step 9: Present Results

1. Copy the final `.pptx` to `/mnt/user-data/outputs/`
2. Use `present_files` to share the slide
3. Provide a 2–3 sentence verbal summary:
   - "Your digest covers X rounds totaling $Y raised across [sectors]."
   - Call out the single most notable deal and its valuation
   - Flag any concerning trends (down rounds, valuation compression, etc.)

## Error Handling

### Entity Resolution Failures
- **Empty results for a known company:** First check `get_info_from_identifiers` — if that fails, try the alias from `references/sector-seeds.md` or the `company_id` directly. Common brand→legal mismatches: Together AI → "Together Computer, Inc.", Character.ai → "Character Technologies, Inc.", Runway ML → "Runway AI, Inc.".
- **Subsidiary companies:** DeepMind, GitHub, Instagram, WhatsApp, YouTube, BeReal, etc. are subsidiaries — they have zero independent funding rounds. Note these as "acquired/subsidiary" in context but do not report them as "no activity."
- **Defunct companies:** Companies like Convoy (shut down Oct 2023) still resolve in S&P Global but will never have new activity. The `references/sector-seeds.md` file flags these — check it before including a company.
- **`get_funding_summary_from_identifiers` errors or returns zeros:** Fall back to `get_rounds_of_funding_from_identifiers` — the summary tool is less reliable. Never rely on the summary tool as the sole data source.
- **Wrong `role` parameter:** If investor-perspective queries return empty, verify you're using `company_investing_in_round_of_funding`, not `company_raising_funds` (and vice versa).

### Data Quality Issues
- **No activity in period:** If a sector had zero funding rounds, note this explicitly on the slide ("No transactions recorded in [Sector] during the period") — absence of activity is itself informative.
- **Sparse valuation data:** If pre-money and post-money valuations are undisclosed for most transactions, note the data limitation in a footer annotation and use "—" in the table. Adjust the stat card to show a different metric (e.g., Median Round Size) instead of Avg Pre-Money.
- **Logo retrieval failures:** The `simple-icons` npm package provides ~43% coverage for typical deal flow companies. For the remainder, use the `sharp`-generated initial-based fallback. Keep a consistent icon style — don't mix random approaches. If `simple-icons` or `sharp` fail to install, fall back to pptxgenjs shape-based initials (gray ellipse + white text overlay) which require no external dependencies.
- **Too many deals for one slide:** If there are more than 6 notable deals, show the top 6 in the table and add a footnote: "+N additional deals not shown." Prioritize by deal size.
- **Large universes:** For multi-sector digests with 100+ companies, batch all API calls in groups of 15–20. Prioritize depth on notable deals over completeness on minor ones.
- **Stale seeds:** If competitor expansion returns very few results for a sector, the seed companies may be too niche. Broaden by adding 2–3 more well-known names and re-expanding.
- **Invalid transaction IDs for links:** If a `transaction_id` from the funding tool doesn't produce a valid Capital IQ URL, omit the link cell for that row rather than including a broken link.

## Example Prompts

- "Give me a weekly deal flow digest for AI and fintech"
- "Summarize this week's funding in biotech"
- "Deal roundup for my coverage — cybersecurity, cloud infrastructure, and dev tools — last 2 weeks"
- "What happened in venture this week across all sectors I follow?"
- "Quick deal flow slide for climate tech this month"

### Referencia: references/sector-seeds.md

# Sector Seed Companies Reference

When the user specifies a sector but not specific companies, use these seed lists to bootstrap the company universe. These are starting points — always expand via `get_competitors_from_identifiers` and validate with `get_info_from_identifiers`.

> **All seeds below have been validated against S&P Global's identifier system.** If a seed fails to resolve, try the alias listed in parentheses before dropping it.

## Technology / Software

### AI / Machine Learning
Seeds: OpenAI, Anthropic, Databricks, Scale AI, Cohere, Hugging Face, Mistral AI, xAI, Perplexity AI, Runway ML (alias: "Runway AI, Inc."), Together AI (alias: "Together Computer, Inc."), Character.ai (alias: "Character Technologies, Inc."), Groq, Stability AI, Aleph Alpha, Magic AI

⚠️ **Excluded (do not use as seeds):**
- *Inflection AI* — Core team absorbed by Microsoft (Mar 2024). Historical rounds exist but no new activity.
- *Adept AI* — Largely absorbed by Amazon (2024). Same as above.
- *DeepMind* — Subsidiary of Alphabet. No independent funding rounds.

### Cybersecurity
Seeds: CrowdStrike, Palo Alto Networks, Wiz, Snyk, SentinelOne, Abnormal Security, Netskope

### Cloud Infrastructure / DevTools
Seeds: Snowflake, HashiCorp, Datadog, Confluent, Vercel, Supabase, PlanetScale

### Fintech
Seeds: Stripe, Plaid, Brex, Ramp, Mercury, Affirm, Marqeta, Navan

### Vertical SaaS
Seeds: ServiceTitan, Toast, Procore, Veeva Systems, Blend Labs

## Healthcare / Life Sciences

### Biotech / Pharma
Seeds: Moderna, BioNTech, Recursion Pharmaceuticals, Tempus AI, Insitro, AbCellera

### Digital Health
Seeds: Teladoc, Hims & Hers, Ro, Noom, Color Health

⚠️ **Excluded (do not use as seeds):**
- *Cerebral* — Still operating but has faced significant regulatory issues; include only if the user specifically requests it.

### Medical Devices
Seeds: Intuitive Surgical, Butterfly Network, Outset Medical

⚠️ **Excluded (do not use as seeds):**
- *Shockwave Medical* — Acquired by Johnson & Johnson (May 2024). Now a subsidiary with no independent funding rounds.

## Energy / Climate

### Climate Tech
Seeds: Redwood Materials, Form Energy, Commonwealth Fusion, Sila Nanotechnologies, Climeworks

### Clean Energy
Seeds: Enphase Energy, First Solar, Rivian, QuantumScape, Sunnova

## Consumer

### E-Commerce / Marketplace
Seeds: Shopify, Faire, Whatnot, Fanatics

⚠️ **Excluded (do not use as seeds):**
- *Temu (PDD Holdings)* — PDD Holdings is a massive public conglomerate; its funding activity is captured via equity markets, not venture rounds.

### Consumer Social / Media
Seeds: Discord, Reddit, Substack

⚠️ **Excluded (do not use as seeds):**
- *BeReal* — Acquired by Voodoo (Jun 2024). Now a subsidiary.
- *Lemon8* — The brand name "Lemon8" resolves in S&P Global to a small Dutch company (Lemon8 B.V.), **not** the ByteDance social media app. ByteDance's apps are subsidiaries and do not have independent funding rounds. Do not use.

## Industrials / Logistics

### Logistics / Supply Chain
Seeds: Flexport, Samsara, Project44, FourKites

⚠️ **Excluded (do not use as seeds):**
- *Convoy* — Shut down operations (Oct 2023). The identifier still resolves and historical rounds are available, but no new activity will appear.

### Robotics / Automation
Seeds: Figure AI, Agility Robotics, Locus Robotics, Symbotic, Covariant

### Space / Aerospace
Seeds: SpaceX, Relativity Space, Rocket Lab, Planet Labs, Astra

## Identifier Alias Reference

Some well-known brand names don't match S&P Global's legal entity names. If a brand name returns empty results from `get_info_from_identifiers`, try the alias:

| Brand Name | S&P Global Legal Name | company_id |
|---|---|---|
| Together AI | Together Computer, Inc. | C_1860042219 |
| Character.ai | Character Technologies, Inc. | C_1829047235 |
| Runway ML | Runway AI, Inc. | C_633706980 |
| Adept AI | Adept AI Labs Inc. | C_1780739313 |
| xAI | X.AI LLC | C_1863863313 |

> **Tip:** When a brand name fails, try `get_info_from_identifiers` with the legal name. If that also fails, the company may not be indexed yet. As a last resort, use the `company_id` directly as the identifier.

## Notes

- These lists skew toward US-based companies. For geographic filtering (Europe, Asia, etc.), the competitor expansion step is especially important.
- For niche sub-sectors not listed here, ask the user for 2–3 example companies to use as seeds.
- Always validate seeds are still active/relevant — companies pivot, merge, or shut down.
- **Refresh cadence:** These seeds should be reviewed quarterly. AI sector seeds in particular change rapidly due to acquisitions and new entrants.
- Seeds marked as subsidiaries or acquired will still resolve in `get_info_from_identifiers` (status = "Operating Subsidiary") but will return zero funding rounds. Skip these for funding queries.


---

## SKILL: hyperliquid-reader

- Fuente: `himself65/finance-skills` → `plugins/data-providers/skills/hyperliquid-reader` (MIT)
- Cuándo usarla: >

# Hyperliquid Reader (Read-Only)

If your host has not already executed the shell probes below (for example, in Codex), run the commands inside the `!` wrappers with its shell tool before choosing a setup path. Use the actual output; if shell access is unavailable, report that limitation.

Reads [Hyperliquid](https://app.hyperliquid.xyz) — the on-chain perps/spot DEX — for market data via [opencli](https://github.com/jackwener/opencli) and the `hyperliquid` plugin in this repo's [`opencli-plugins/hyperliquid`](https://github.com/himself65/finance-skills/tree/main/opencli-plugins/hyperliquid) tree (a separate plugin from opencli's built-in adapters, installed via opencli's monorepo subpath syntax).

**This skill is read-only and market-data only.** It reads Hyperliquid's fully public info API for analysis: market tables, funding, order book, and candles. It does NOT read individual accounts, place/modify/cancel orders, or move funds. There is no trading path in the plugin — order placement requires wallet-signed actions on a separate endpoint this adapter never calls.

**How it works**: every command issues a single `POST https://api.hyperliquid.xyz/info` with a `{ "type": "..." }` body and normalizes the response. **No API key, no wallet, no login, no running app** — the info API is public.

---

## Step 1: Ensure opencli + Plugin Are Installed and Ready

**Current environment status:**

```
!`(command -v opencli && opencli hyperliquid markets --coin BTC -f json 2>&1 | head -3 && echo "READY" || echo "SETUP_NEEDED") 2>/dev/null || echo "NOT_INSTALLED"`
```

If the status above shows `READY`, skip to Step 2. Otherwise:

### NOT_INSTALLED — Install opencli

```bash
npm install -g @jackwener/opencli
```

Requires Node.js >= 24 — the `hyperliquid` plugin declares `engines.node >= 24`.

### SETUP_NEEDED — Install the Hyperliquid plugin

The Hyperliquid adapter is **not** built into opencli — it's a separate plugin:

```bash
opencli plugin install github:himself65/finance-skills/hyperliquid
```

That's the entire setup — no auth, no launch step. Verify with `opencli hyperliquid markets --coin BTC`.

### Common setup issues

| Symptom | Fix |
|---|---|
| `opencli: command not found` | `npm install -g @jackwener/opencli` (Node ≥ 24) |
| `Unknown command: hyperliquid` | `opencli plugin install github:himself65/finance-skills/hyperliquid` |
| `hyperliquid info 429` | Rate limited — wait a few seconds and retry |

---

## Step 2: Identify What the User Needs

| User Request | Command | Key Flags |
|---|---|---|
| Perp markets overview / top by volume | `opencli hyperliquid markets` | `--sort`, `--limit`, `--coin` |
| One perp's price + funding + OI | `opencli hyperliquid markets --coin BTC` | — |
| Spot pairs overview | `opencli hyperliquid spot-markets` | `--sort`, `--limit`, `--pair`, `--canonical-only` |
| All current mid prices | `opencli hyperliquid mids` | `--coin <substring>` |
| Order book for a coin | `opencli hyperliquid book --coin ETH` | `--depth`, `--n-sig-figs` |
| OHLCV candles | `opencli hyperliquid candles --coin BTC --interval 1h` | `--limit` |
| Historical funding for a coin | `opencli hyperliquid funding-history --coin BTC` | `--hours`, `--limit` |
| Funding arb: HL vs Binance vs Bybit | `opencli hyperliquid funding-compare` | `--coin`, `--sort`, `--limit` |

---

## Step 3: Execute the Command

### General pattern

```bash
# Use -f json or -f yaml for structured output
opencli hyperliquid markets --sort fundingAprPct --limit 15 -f json
opencli hyperliquid funding-compare --sort hlVsBinancePct --limit 20 -f md
opencli hyperliquid candles --coin BTC --interval 4h --limit 50 -f csv
opencli hyperliquid book --coin ETH --depth 5 -f json
```

### Key rules

1. **Coin symbols are bare perp names** — `BTC`, `ETH`, `SOL`, `HYPE` (no exchange prefix). Spot pairs are `BASE/USDC` (e.g. `PURR/USDC`); for `book`/`candles` you can pass either a perp coin or a spot pair.
2. **`markets` is the default lens for "how is X / the market doing"** — it carries mark/oracle/mid price, 24h change, hourly funding + APR, open interest (coins and notional), and 24h volume in one row per perp. Filter with `--coin` for a single asset.
3. **Funding is reported two ways** — `fundingHrPct` is the raw hourly rate as a percent; `fundingAprPct` annualizes it (`hourly × 24 × 365`). Lead with APR when comparing carry across assets; use the hourly figure for "what will I pay next hour".
4. **`funding-compare` is the funding-arb screen** — it annualizes each venue with its own interval (HL hourly, Binance/Bybit usually 4h) and reports `hlVsBinancePct` / `hlVsBybitPct` spreads. Default sort ranks by **absolute** HL-vs-Binance spread (widest dislocations first). A positive `hlVsBinancePct` means HL longs pay more than Binance longs.
5. **`book` defaults to 10 levels per side** — raise `--depth` (max 20) for more, or `--n-sig-figs 2..5` to aggregate price levels. Compute the spread/mid from the top bid and ask.
6. **`candles` pulls the most recent `--limit` candles** of `--interval` (default `1h`, 100 candles). Valid intervals: `1m 3m 5m 15m 30m 1h 2h 4h 8h 12h 1d 3d 1w 1M`. Max 5000.
7. **`-f json`** for programmatic processing / feeding other skills; `-f md` or `-f table` for human-readable output.
8. **Read-only market data.** No account reads, no order placement, modification, or cancellation, and no transfers — the plugin intentionally exposes no write endpoints, so don't look for workarounds.

### Output format flag (`-f`)

| Format | Flag | Best for |
|---|---|---|
| Table | `-f table` (default) | Human-readable terminal output |
| JSON | `-f json` | Programmatic processing, LLM context |
| YAML | `-f yaml` | Structured, readable |
| Markdown | `-f md` | Reports |
| CSV | `-f csv` | Spreadsheet export |

### Output columns

- `markets` — `coin`, `markPx`, `midPx`, `oraclePx`, `change24hPct`, `fundingHrPct`, `fundingAprPct`, `openInterest`, `oiNotional`, `dayNtlVlm`, `premiumPct`, `maxLeverage`
- `spot-markets` — `pair`, `base`, `markPx`, `midPx`, `change24hPct`, `dayNtlVlm`, `circulatingSupply`, `marketCap`, `canonical`
- `mids` — `coin`, `mid`
- `book` — `side`, `level`, `px`, `sz`, `orders`
- `candles` — `time`, `open`, `high`, `low`, `close`, `volume`, `trades`
- `funding-history` — `coin`, `fundingRatePct`, `fundingAprPct`, `premiumPct`, `time`
- `funding-compare` — `coin`, `hlAprPct`, `binanceAprPct`, `bybitAprPct`, `hlVsBinancePct`, `hlVsBybitPct`, `nextHlFunding`

---

## Step 4: Present the Results

1. **Lead with the headline number, then the table.** For `markets --coin BTC`: state mark price, 24h change, funding APR, and open interest in prose first. For a full `markets` dump: lead with the count and the top movers / highest-funding names.
2. **Frame funding in carry terms** — e.g. "BTC perp funding is +10.9% APR (longs pay shorts)". Positive funding ⇒ longs pay shorts; negative ⇒ shorts pay longs.
3. **For `funding-compare`, surface the widest dislocations first** — name the coin, both venues' APRs, and the spread, and remember the spread is annualized; a real arb also pays exchange/withdrawal frictions, so present it as a screen, not a guaranteed edge.
4. **For `book`, report the spread** — best bid, best ask, mid, and spread in bps before (or instead of) dumping every level. Don't paste 20 levels unless asked.
5. **For `candles`, describe the move** — first/last close, high/low, and direction; only show the full OHLCV table when the user wants the series.
6. **Filter aggressively before showing** — `markets` has ~180 perps and `mids` ~700 markets; cap to top 15-20 by the relevant sort unless the user asks for the full list.
7. **Cross-reference for trade decisions** — Hyperliquid is the on-chain venue; for equities/options context pair it with the `tradingview-reader` skill. For funding/basis trades, `funding-compare` plus `markets` (premium, OI) is the core view.

---

## Step 5: Diagnostics

```bash
opencli hyperliquid markets --coin BTC
```

A successful BTC row confirms opencli, the plugin, and the public API are all reachable. If it errors with `Unknown command: hyperliquid`, reinstall the plugin (Step 1). A `hyperliquid info 4xx/5xx` is an upstream API issue — retry after a short wait.

---

## Error Reference

| Error | Cause | Fix |
|---|---|---|
| `Unknown command: hyperliquid` | Plugin not installed | `opencli plugin install github:himself65/finance-skills/hyperliquid` |
| `hyperliquid info 429` | Rate limited | Wait a few seconds, then retry |
| `hyperliquid info 422/500` | Malformed body or upstream issue | Re-check the coin/interval; retry after a wait |
| `No perp market for coin "X"` | Wrong/unlisted symbol | Run `opencli hyperliquid markets` (or `mids`) to find the exact symbol |

---

## Reference Files

- `references/commands.md` — Every command with all flags, output schemas, and analyst workflows (funding carry, basis/arb, spot snapshot)

### Referencia: README.md

# hyperliquid-reader

Read-only Hyperliquid market-data reader via [opencli](https://github.com/jackwener/opencli) + the [`hyperliquid`](../../../../opencli-plugins/hyperliquid/) opencli plugin shipped alongside this skill.

## What it does

Reads [Hyperliquid](https://app.hyperliquid.xyz)'s **public info API** — no API key, no wallet, no login, no scraping. Capabilities:

- **Perp markets** — mark/oracle/mid price, 24h change, hourly funding + annualized APR, open interest (coins + notional), and 24h volume for every perpetual
- **Spot markets** — pair price, 24h change, volume, circulating supply, market cap
- **Mids** — current mid price for every perp + spot market in one call
- **Order book** — L2 snapshot, top N levels per side, with spread
- **Candles** — OHLCV history for any interval (1m … 1M)
- **Funding history** — historical hourly funding (rate, APR, premium) per coin
- **Funding compare** — cross-venue predicted funding (Hyperliquid vs Binance vs Bybit), annualized, with spreads — a funding-arbitrage screen

**This skill is read-only and market-data only.** It does NOT read individual accounts, place/modify/cancel orders, or move funds.

## Authentication

None. Hyperliquid's `info` market-data endpoints are fully public — nothing to authenticate.

## Triggers

- "Hyperliquid funding for X", "what's the funding on BTC perp", "HL open interest"
- "Hyperliquid order book for ETH", "HL perp markets", "Hyperliquid spot markets"
- "funding arb Hyperliquid vs Binance", "Hyperliquid candles for SOL"
- "PURR price on Hyperliquid", "Hyperliquid mid prices"
- Any mention of Hyperliquid / app.hyperliquid.xyz / HL DEX in context of reading market data or funding

## Platform

Works on **Claude Code** and other CLI-based agents (any OS with Node ≥ 24). Does **not** work on Claude.ai — the sandbox restricts the network access opencli needs. Unlike the TradingView reader, there is no desktop-app or macOS dependency — it's a plain HTTP API.

## Setup

```bash
# Choose finance-data-providers when prompted.
npx plugins add himself65/finance-skills

# Or install just this skill
npx skills add himself65/finance-skills --skill hyperliquid-reader
```

See the [main README](../../../../README.md) for more installation options.

## Prerequisites

- Node.js >= 24 — for `npm install -g @jackwener/opencli`, and required by the plugin's `engines.node`
- The `hyperliquid` opencli plugin: `opencli plugin install github:himself65/finance-skills/hyperliquid` (installs from this repo's monorepo subpath)

No API key, no wallet, no launch step.

## Reference files

- `references/commands.md` — Complete market-data command reference with all flags, output schemas, and analyst workflows

### Referencia: references/commands.md

# Hyperliquid Reader — Command Reference

Every command issues a single `POST https://api.hyperliquid.xyz/info` and prints normalized rows. All are **read-only market data**, need no auth, and accept `-f json|yaml|md|csv|table`.

> Symbols: perps are bare names (`BTC`, `ETH`, `HYPE`); spot pairs are `BASE/USDC` (`PURR/USDC`). `book` and `candles` accept either.

---

## Market data

### `markets` — perpetual markets table

`metaAndAssetCtxs` → one row per perp.

| Flag | Default | Notes |
|---|---|---|
| `--coin` | (all) | Filter to one coin (exact, case-insensitive) |
| `--sort` | `dayNtlVlm` | One of `dayNtlVlm`, `change24hPct`, `fundingAprPct`, `fundingHrPct`, `openInterest`, `oiNotional`, `markPx`, `coin` (desc; `coin` asc). `null` sorts last |
| `--limit` | (all) | Max rows after sort |
| `--include-delisted` | `false` | Include delisted markets |

Columns: `coin`, `markPx`, `midPx`, `oraclePx`, `change24hPct`, `fundingHrPct`, `fundingAprPct`, `openInterest`, `oiNotional`, `dayNtlVlm`, `premiumPct`, `maxLeverage`.

- `fundingHrPct` — raw hourly funding rate as a percent.
- `fundingAprPct` — `hourly × 24 × 365` (annualized).
- `openInterest` — in coins; `oiNotional` — `openInterest × markPx` (USD).
- `premiumPct` — perp premium/discount vs oracle (mark-implied).

```bash
opencli hyperliquid markets --sort dayNtlVlm --limit 15
opencli hyperliquid markets --coin HYPE -f json
opencli hyperliquid markets --sort fundingAprPct --limit 20   # highest carry
```

### `spot-markets` — spot pairs table

`spotMetaAndAssetCtxs` → one row per spot pair.

| Flag | Default | Notes |
|---|---|---|
| `--pair` | (all) | Filter by pair or base token (e.g. `PURR` or `PURR/USDC`) |
| `--sort` | `dayNtlVlm` | One of `dayNtlVlm`, `change24hPct`, `marketCap`, `markPx`, `pair` |
| `--limit` | (all) | Max rows after sort |
| `--canonical-only` | `false` | Only named pairs (hide `@index` pairs) |

Columns: `pair`, `base`, `markPx`, `midPx`, `change24hPct`, `dayNtlVlm`, `circulatingSupply`, `marketCap`, `canonical`.

```bash
opencli hyperliquid spot-markets --canonical-only --sort dayNtlVlm --limit 20
opencli hyperliquid spot-markets --pair PURR -f json
```

### `mids` — all mid prices

`allMids` (+ `spotMeta` to resolve names) → `coin`, `mid` for every market.

| Flag | Default | Notes |
|---|---|---|
| `--coin` | (all) | Case-insensitive **substring** filter |

Non-canonical spot keys (`@<index>`) resolve to `BASE/QUOTE`; perp names and canonical pairs pass through; builder perp-dex keys (`#<n>`) are shown as-is.

```bash
opencli hyperliquid mids --coin BTC      # BTC, plus any pair containing "BTC"
opencli hyperliquid mids -f json | jq '.[] | select(.coin=="ETH")'
```

### `book` — L2 order book snapshot

`l2Book` → up to `--depth` levels per side, bids first then asks.

| Flag | Default | Notes |
|---|---|---|
| `--coin` | (required) | Coin or spot pair |
| `--depth` | `10` | Levels per side (1-20) |
| `--n-sig-figs` | (full) | Price aggregation, 2-5 |

Columns: `side` (`bid`/`ask`), `level`, `px`, `sz`, `orders`.

Spread = best ask − best bid; mid = their average. Top-of-book is `level: 1` on each side.

```bash
opencli hyperliquid book --coin ETH --depth 5
opencli hyperliquid book --coin BTC --n-sig-figs 3 -f json
```

### `candles` — OHLCV history

`candleSnapshot` → most recent `--limit` candles of `--interval`.

| Flag | Default | Notes |
|---|---|---|
| `--coin` | (required) | Coin or spot pair |
| `--interval` | `1h` | `1m 3m 5m 15m 30m 1h 2h 4h 8h 12h 1d 3d 1w 1M` |
| `--limit` | `100` | Number of candles (max 5000) |

Columns: `time` (ISO, candle open), `open`, `high`, `low`, `close`, `volume`, `trades`.

```bash
opencli hyperliquid candles --coin BTC --interval 4h --limit 60
opencli hyperliquid candles --coin SOL --interval 1d --limit 30 -f csv
```

### `funding-history` — historical funding for a coin

`fundingHistory` → hourly prints within the lookback window, newest first.

| Flag | Default | Notes |
|---|---|---|
| `--coin` | (required) | Coin (e.g. `BTC`) |
| `--hours` | `24` | Lookback window in hours |
| `--limit` | (all) | Cap to most recent N |

Columns: `coin`, `fundingRatePct`, `fundingAprPct`, `premiumPct`, `time`.

```bash
opencli hyperliquid funding-history --coin BTC --hours 72
opencli hyperliquid funding-history --coin ETH --hours 168 --limit 24 -f json
```

### `funding-compare` — cross-venue funding (arb screen)

`predictedFundings` → per coin, each venue's predicted funding annualized to APR, plus HL-vs-venue spreads.

| Flag | Default | Notes |
|---|---|---|
| `--coin` | (all) | Filter to one coin (exact) |
| `--sort` | `hlVsBinancePct` | `hlVsBinancePct`, `hlVsBybitPct` (by absolute spread), or `hlAprPct`, `binanceAprPct`, `bybitAprPct`, `coin` (signed) |
| `--limit` | (all) | Max rows after sort |

Columns: `coin`, `hlAprPct`, `binanceAprPct`, `bybitAprPct`, `hlVsBinancePct`, `hlVsBybitPct`, `nextHlFunding`.

Each venue is annualized with its own interval (HL hourly, Binance/Bybit usually 4h). `hlVsBinancePct = hlAprPct − binanceAprPct`; positive ⇒ HL longs pay more. Default sort surfaces the widest dislocations first. Treat as a screen — a real arb also pays exchange and transfer frictions.

```bash
opencli hyperliquid funding-compare --limit 20            # widest HL/Binance gaps
opencli hyperliquid funding-compare --coin BTC -f json
opencli hyperliquid funding-compare --sort hlAprPct --limit 15   # highest HL carry
```

---

## Analyst workflows

### Funding carry scan
1. `markets --sort fundingAprPct --limit 20` — highest (and, reversed mentally, lowest) annualized funding.
2. `funding-history --coin <X> --hours 168` — confirm the rate is persistent, not a one-hour spike.
3. `markets --coin <X>` — check open interest and premium to size whether the carry is tradeable.

### Cross-venue funding arbitrage
1. `funding-compare --limit 25` — widest HL-vs-Binance/Bybit dislocations.
2. For a candidate `<X>`: `funding-compare --coin <X>` for all three venues' APRs and the next HL funding time.
3. `book --coin <X>` and `markets --coin <X>` — verify depth and OI can support the size before treating the spread as real (it's annualized and ignores frictions).

### Basis / premium check
1. `markets --coin <X>` — `premiumPct` shows perp rich/cheap vs oracle; `markPx` vs `oraclePx` is the absolute basis.
2. `candles --coin <X> --interval 1h` — recent price action around the basis.

### Spot token snapshot
1. `spot-markets --canonical-only --sort dayNtlVlm` — most active named pairs.
2. `spot-markets --pair <BASE>` — price, 24h change, market cap for one token.
3. `book --coin <BASE>/USDC` — liquidity at top of book.


---

## SKILL: kalshi-crypto-index-markets

- Fuente: `agiprolabs/claude-trading-skills` → `skills/kalshi-crypto-index-markets` (MIT)
- Cuándo usarla: Kalshi daily and hourly range markets on crypto prices (BTC, ETH) and equity indices (S&P 500, Nasdaq-100) — bracket structure, Gaussian P(YES) modeling on price/vol, close-offset decision timing, longshot-sell edge with honest evidence bounds

# Kalshi Crypto & Index Range Markets

Kalshi lists daily (and for crypto, hourly) **range bracket markets** on the level of four liquid underlyings: S&P 500, Nasdaq-100, Bitcoin, and Ethereum. The math is the same partition-and-Gaussian framework as weather brackets — the variable is just price/return and σ comes from the underlying's realized or implied volatility, not a temperature model.

> Cross-references: for Kalshi API mechanics see `kalshi-api`; for the strategy, sizing, and backtesting framework see `prediction-market-strategy`; for the temperature counterpart see `kalshi-weather-markets`; for the shared bracket/overround formulas see `prediction-markets/references/brackets-and-settlement.md`.

---

## Series & Market-Type Mapping

```python
SERIES_MARKET = {
    "KXINX":       "index",   # S&P 500 index level
    "KXNASDAQ100": "index",   # Nasdaq-100 index level
    "KXBTC":       "crypto",  # Bitcoin price (USD)
    "KXETH":       "crypto",  # Ethereum price (USD)
}
```

- `market_type = "index"` — daily range only; underlying is the index points level at the official market close.
- `market_type = "crypto"` — daily **and hourly** range markets; BTC and ETH each have multiple hourly events running in parallel with the daily.

Cadence is higher than weather: crypto hourlies open and settle throughout the day; daily markets open the prior session and settle at the reference close.

---

## Bracket Structure

Each event is a **mutually exclusive, collectively exhaustive** partition of the underlying's possible values at settlement:

- An interior bracket `B<center>` covers a contiguous price band (floor to cap, both-ends-inclusive). Bracket widths are set per-market — read the event's market list; do not assume a fixed width.
- Two open-tail markets anchor the partition: a `less-than` (below the lowest bracket floor) and a `greater-than` (above the highest bracket cap).
- At settlement exactly **one** bracket is YES; all others are NO.

The overround (sum of all YES prices) is typically > 1.0. The excess is concentrated in the cheap tails — the same favorite–longshot bias seen in weather markets. See `prediction-markets/references/brackets-and-settlement.md` for the overround formula.

---

## Gaussian P(YES) on Price/Vol

Given a price forecast distribution `N(μ, σ)` for the underlying at settlement, with bracket covering `[floor, cap]`:

```
# interior bracket
P(YES) = Φ((cap − μ) / σ) − Φ((floor − μ) / σ)

# open-tail, "greater than cap"
P(YES) = 1 − Φ((cap − μ) / σ)

# open-tail, "less than floor"
P(YES) = Φ((floor − μ) / σ)
```

`Φ` is the standard normal CDF. Unlike temperature brackets (which settle on integers), price brackets settle on a continuous reference price — the half-integer continuity correction used for weather is **not applicable here**. Do not add ±0.5.

### Sourcing σ

- **Realized vol:** rolling 5- or 20-day realized volatility of the underlying, scaled to the settlement horizon.
- **Implied vol:** the ATM IV from listed options (SPX/NDX for index, CME/Deribit for crypto) is a forward-looking σ that already embeds the market's distributional view for the horizon.
- **Hourly markets:** for BTC/ETH hourlies, σ is the 1-hour IV or intraday realized vol. Σ shrinks rapidly — even small absolute moves land in a different bracket. Sensitivity is high; prefer IV-derived σ.

For daily markets, a simple log-return diffusion gives `σ_daily ≈ σ_annual / √252` for index, or the equivalent annualized vol / √365 for crypto. Express in price units (not %) before inserting into the formula.

---

## Decision Timing — Close-Offset, Not a City Hour

**This is the key difference from weather markets.**

Weather settles on a daily extreme that occurs at some unknown intraday time. The decision book is read near the likely peak/trough (a city-local hour).

Crypto and index markets settle at a **fixed reference close**:

- Daily S&P 500 / Nasdaq-100: the official market close (4:00 PM ET).
- Daily BTC/ETH: a defined reference close published in the market's rulebook.
- Hourly BTC/ETH: the close of each hour interval per the rulebook.

The practical convention used in production:

```python
DECISION_OFFSET_MINUTES = 120   # read book ~2h before settlement close
decision_ts = settlement_close_ts - timedelta(minutes=DECISION_OFFSET_MINUTES)
```

This offset balances information freshness (IV and order-book signal) against the risk of being front-run by news that drops in the final window. Tune per-series based on your fill-rate observations.

---

## Settlement — Verify the Rulebook Reference

Settlement is on Kalshi's own `result` field. **Do not re-derive from an external feed.** The exact reference price for each series (e.g., official SPX close vs. a crypto composite) is specified per-market in the Kalshi rulebook.

Honest caveat: the exact reference price spec was not pinned for every series during development. Before trading any new series, read the market's rulebook and confirm:
1. The settlement price source (exchange, composite, or Kalshi-computed).
2. The settlement time and timezone.
3. Whether the bracket is inclusive/exclusive at the boundary.

Backtesting against a price feed that differs from the true settlement source is the primary way to manufacture fake edge in these markets.

---

## Edge: Longshot-Sell Generalization

The **favorite–longshot bias** generalizes from weather to index and crypto brackets. Tail brackets are systematically overpriced relative to a Gaussian model calibrated to realized/implied vol; interior brackets near the current underlying level are fairly priced or underpriced.

### Evidence (be precise about depth)

From production testing with a rotating CV approach, Kalshi-settled outcomes, fee-inclusive:

| Market type | Sweet band | Edge direction | Sample | Result |
|-------------|-----------|----------------|--------|--------|
| **Index** | Market-implied P ∈ [0.05, 0.20] | Longshot-sell (short tail brackets) | ~50 trades | ~+1.7% taker / ~+9% maker |
| **Crypto daily** | — | — | Too sparse | Inconclusive |
| **Crypto hourly** | — | — | Too sparse | Inconclusive |

**Interpret conservatively.** ~50 trades is not a stable estimate; confidence intervals are wide. The index result is directionally consistent with the weather finding and prior literature on longshot bias, but treat it as a hypothesis to validate forward, not a confirmed edge.

### The HFT Caveat (critical for hourlies)

Crypto and index markets settle on public, real-time price ticks. The underlying is continuously quoted on liquid venues with sub-millisecond latency. This means:

- The information content of any bracket price is rapidly arbitraged by HFT and market-maker algos watching the same tick.
- **Latency front-running** — buying or selling brackets based on price moves — is a colocation/HFT game. From a retail connection you will be consistently on the wrong side of news-driven bracket repricing.
- The retail-feasible angle is the **structural longshot-sell** (exploiting the persistent overpricing in cheap tails that is stable across market regimes), not speed-based positioning.
- Hourly crypto markets are the most HFT-contested of all Kalshi markets. Maker fills on tail brackets may be scarce precisely when the edge is largest.

---

## Market Microstructure Notes

- **Overround** is the primary microstructure signal. For a partition of N brackets, `overround = Σ P_yes`. When overround > 1.10 in the tails, the aggregate tail sell has positive expected value before fees; after Kalshi taker fees (~7 cents/$1 per leg) the bar is higher. Maker rebates change the math substantially.
- **Thin books:** individual bracket markets on hourly crypto may show wide spreads and low depth. Model a realistic fill at a depth level before sizing.
- **Basket dutch:** selling the complete set of tail brackets is not trivially an arb even when overround > 1.0; fees per leg plus execution uncertainty can eliminate the overround advantage. See `prediction-market-strategy` for the dutch/portfolio treatment.

---

## Files

### References
- `references/structure-and-modeling.md` — Series details, bracket structure, σ-from-vol modeling, decision timing, settlement

### Referencia: references/structure-and-modeling.md

# Structure & Modeling — Kalshi Crypto & Index Range Markets

Detailed reference for series definitions, bracket anatomy, volatility-derived σ, decision timing, and settlement. Read `SKILL.md` first for context.

---

## Series Definitions

| Series ticker | Underlying | Market type | Cadence |
|--------------|------------|-------------|---------|
| `KXINX` | S&P 500 index (INX) | `index` | Daily only |
| `KXNASDAQ100` | Nasdaq-100 (NDX) | `index` | Daily only |
| `KXBTC` | Bitcoin / USD | `crypto` | Daily + hourly |
| `KXETH` | Ethereum / USD | `crypto` | Daily + hourly |

Code convention:

```python
SERIES_MARKET = {
    "KXINX":       "index",
    "KXNASDAQ100": "index",
    "KXBTC":       "crypto",
    "KXETH":       "crypto",
}
```

---

## Bracket Anatomy

Each event `E` at settlement time `T` is a price-level partition:

```
  … | tail_low | B_1 | B_2 | … | B_n | tail_high | …
  (−∞, floor_1)  [floor_1, cap_1]  …  [floor_n, cap_n]  (cap_n, +∞)
```

- **Interior bracket** `B_k`: covers the closed interval `[floor_k, cap_k]`. Settlement YES iff the reference price `∈ [floor_k, cap_k]`.
- **Low tail**: YES iff reference price `< floor_1`.
- **High tail**: YES iff reference price `> cap_n`.
- Exactly one market is YES at settlement.
- Bracket width is set per-event; do not assume a fixed width — read the market list from the API.

### Overround

```python
overround = sum(p_yes for all brackets in event)
# fair = 1.0; typical live overround = 1.05–1.20
```

Overround is concentrated in the cheap tails. The interior brackets near the current underlying level tend to be fairly priced.

---

## Modeling: σ from Underlying Volatility

### Daily markets

Use the log-return diffusion approximation to express annual volatility in price-level units:

```python
import numpy as np
from scipy.stats import norm

def price_sigma_daily(underlying_price: float, annual_vol: float) -> float:
    """
    Convert annualized % vol to 1-day price-unit sigma.
    annual_vol: e.g. 0.20 for 20% annualized
    Returns sigma in the same units as the price.
    """
    daily_log_sigma = annual_vol / np.sqrt(252)          # index (trading days)
    # For crypto (24/7), use 365:
    # daily_log_sigma = annual_vol / np.sqrt(365)
    return underlying_price * daily_log_sigma


def p_yes_bracket(mu: float, sigma: float, floor: float, cap: float) -> float:
    """
    P(YES) for an interior bracket [floor, cap] under N(mu, sigma).
    mu: forecast mean price at settlement
    sigma: price-unit standard deviation
    NO half-integer correction (continuous settlement price).
    """
    return norm.cdf((cap - mu) / sigma) - norm.cdf((floor - mu) / sigma)


def p_yes_low_tail(mu: float, sigma: float, floor: float) -> float:
    return norm.cdf((floor - mu) / sigma)


def p_yes_high_tail(mu: float, sigma: float, cap: float) -> float:
    return 1.0 - norm.cdf((cap - mu) / sigma)
```

### Hourly markets (BTC/ETH)

For a 1-hour horizon, scale from daily:

```python
def price_sigma_hourly(underlying_price: float, daily_vol_pct: float) -> float:
    hourly_log_sigma = daily_vol_pct / np.sqrt(24)
    return underlying_price * hourly_log_sigma
```

IV-derived σ is preferable to realized-vol for hourlies because the market's own distributional expectation for the next hour is embedded in the options surface. Use the ATM 1-hour or shortest-dated expiry.

### σ sources (preferred order)

| Source | Notes |
|--------|-------|
| ATM IV from listed options | Forward-looking; preferred. SPX/NDX options for index; CME BTC/ETH or Deribit for crypto |
| Realized vol (5-day rolling) | Backward-looking; more stable, slower to adapt to vol regime changes |
| Realized vol (1-day) | Noisy; useful for fast-adapting hourly estimates |

Always verify that the vol source is in the same units (annualized %) before converting.

---

## Decision Timing

### Index daily

| Event | Time (ET) |
|-------|-----------|
| Market open | 9:30 AM |
| Decision book read | ~2:00 PM (2h before close) |
| Settlement close | 4:00 PM |

```python
from datetime import time
DECISION_OFFSET_MINUTES = 120
# decision_ts = settlement_close_ts - timedelta(minutes=DECISION_OFFSET_MINUTES)
```

### Crypto daily

Settlement close time is defined in the market's rulebook (varies; often midnight UTC or a Kalshi-specified time). Apply the same 120-min default offset and adjust based on fill observations.

### Crypto hourly

Each hourly market settles at the top of the hour. The decision window is short — on the order of 10–30 minutes before the close. The offset should be tighter:

```python
HOURLY_DECISION_OFFSET_MINUTES = 15  # indicative; tune per fill data
```

At this frequency, the dominant risk is not model error but HFT front-running in the final minutes. See the HFT caveat in `SKILL.md`.

---

## Settlement

**Always use Kalshi's own `result` field.** Do not re-derive settlement from an external price feed.

Key questions to answer per-series before backtesting or trading:

1. **Settlement price source:** Exchange official close? A composite of multiple exchanges? A Kalshi-computed VWAP? Read the per-market rulebook.
2. **Settlement time:** The exact UTC timestamp. For S&P 500 this is the 4:00 PM ET official close; for crypto it is market-specified.
3. **Bracket boundary condition:** Is the boundary inclusive or exclusive? (Kalshi temperature brackets use both-ends-inclusive; price brackets should be checked per-market.)
4. **Corporate actions / index rebalances:** For index markets, large rebalance events (Russell reconstitution, S&P additions) can cause out-of-distribution moves. Flag these dates in any backtest.

### Common backtest error

Substituting Yahoo Finance or Binance closing prices for the Kalshi-defined settlement reference will produce small but systematic settlement mismatches that corrupt P&L attribution. The mismatch is usually < 0.5% on price but can shift a bracket outcome at the boundary.

---

## Sizing and Risk

Use the same sizing framework as weather markets (Kelly/SLSQP under EV threshold). Key differences to account for:

- **Correlation:** BTC and ETH daily returns are highly correlated (~0.85). Treat them as a correlated pair, not independent bets, when sizing simultaneously.
- **Index–crypto correlation:** BTC/ETH daily returns correlate with equity risk-on/off at ~0.4–0.6 in high-volatility regimes. Portfolio-level risk is higher than the individual-market EV suggests.
- **Tail risk:** Price distributions have fat tails relative to Gaussian. The Gaussian model will underestimate the probability of extreme brackets. Apply a tail-inflation factor (e.g., model with a Student-t ν=5) or add a vol-of-vol buffer to σ.

See `prediction-market-strategy` for the full Kelly/SLSQP optimizer and EV-threshold filter.

---

## Related Files

- `SKILL.md` — Strategy overview, edge evidence, HFT caveat
- `../prediction-markets/references/brackets-and-settlement.md` — Shared bracket/overround formulas


---

## SKILL: mev-analysis

- Fuente: `agiprolabs/claude-trading-skills` → `skills/mev-analysis` (MIT)
- Cuándo usarla: MEV exposure assessment, sandwich attack detection, and protection strategies for Solana DEX trading
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/mev-analysis/` (mev_risk_estimator.py, sandwich_detector.py)

# MEV Analysis for Solana DEX Trading

Maximal Extractable Value (MEV) is the profit that validators and searchers can extract by reordering, inserting, or censoring transactions within a block. On Solana DEXes, MEV primarily manifests as sandwich attacks against swaps, cross-DEX arbitrage, and liquidation extraction. This skill covers detection, estimation, and protection strategies.

## What Is MEV on Solana?

MEV occurs when someone with transaction ordering power profits at other traders' expense. On Solana, the MEV supply chain works as follows:

1. **You submit a swap** through an RPC endpoint
2. **Searchers observe** your transaction (via RPC forwarding, block engine access, or leader TPU sniffing)
3. **Searcher constructs a profitable bundle** (e.g., sandwich your swap)
4. **Bundle submitted to Jito block engine** with a tip to the validator
5. **Validator includes the bundle** in the block, earning the tip
6. **You receive worse execution**; the searcher profits the difference

### How Solana MEV Differs from Ethereum

| Aspect | Ethereum | Solana |
|--------|----------|--------|
| Block time | 12 seconds | ~400ms slots |
| Mempool | Public mempool | No mempool (but tx visible in transit) |
| Ordering | Proposer-builder separation (PBS) | Jito block engine (~85%+ validators) |
| Bundle system | Flashbots bundles | Jito bundles with tips |
| MEV cost | Gas priority fees | Jito tips (SOL) |
| Latency pressure | Moderate | Extreme (sub-100ms decisions) |

Key Solana-specific factors:
- **No public mempool**: Transactions flow RPC → TPU → Leader, but searchers tap into this flow via Jito's block engine and modified validators
- **Known leader schedule**: The leader (block producer) schedule is known ~2 epochs ahead, letting searchers target specific leaders
- **Jito dominance**: ~85%+ of validators run the Jito-modified client, making Jito bundles the primary MEV vector
- **Speed**: 400ms slots mean MEV bots must operate in microseconds, favoring co-located infrastructure

## MEV Types on Solana

### 1. Sandwich Attacks

The most common MEV attack against retail traders.

**Mechanics:**
```
1. Attacker sees your pending swap: Buy 10 SOL worth of TOKEN_X
2. Front-run:  Attacker buys TOKEN_X first  → price rises
3. Your swap:  You buy TOKEN_X at higher price → worse execution
4. Back-run:   Attacker sells TOKEN_X         → profits the difference
```

**Your loss** = price impact from front-run + attacker's profit margin
**Attacker profit** = your_loss - jito_tip - transaction_fees

**Risk factors:**
- Trade size: Larger trades = more profitable to sandwich
- Token liquidity: Illiquid tokens = easier price manipulation
- Slippage setting: Wide slippage = more room for the attacker
- Pool type: CPMM pools more vulnerable than CLMM pools at concentrated ranges

### 2. Arbitrage (Cross-DEX)

Searchers capture price discrepancies between DEXes.

```
Pool A: TOKEN_X = 1.00 USDC
Pool B: TOKEN_X = 1.02 USDC
→ Buy on A, sell on B, profit 0.02 USDC per token (minus fees)
```

This is generally **beneficial** to the market — it equalizes prices across venues. However, your trade may trigger the arbitrage opportunity that the searcher captures.

### 3. Liquidation Extraction

When DeFi positions (Solend, Marginfi, Kamino) become undercollateralized, searchers race to liquidate them and claim the liquidation bonus (typically 5-10%).

### 4. JIT (Just-In-Time) Liquidity

Searchers add concentrated liquidity to a CLMM pool just before a large swap and remove it immediately after, earning swap fees without sustained impermanent loss exposure. This is a sophisticated MEV form that can actually **improve** execution for the swapper.

### 5. Back-Running

Trading immediately after a large swap that moved the price, capturing the reversion. Less harmful than sandwiching because it does not worsen your execution — it profits from the market response to your trade.

## Estimating MEV Exposure

Estimate your MEV risk before executing a trade:

```python
import httpx

def estimate_mev_risk(
    trade_size_sol: float,
    pool_liquidity_usd: float,
    slippage_bps: int,
    token_daily_volume_usd: float,
) -> dict:
    """Estimate sandwich attack profitability for a given trade.

    Returns risk assessment with estimated cost and recommendations.
    """
    # Trade as percentage of pool liquidity
    sol_price = 150.0  # approximate; fetch live price in production
    trade_usd = trade_size_sol * sol_price
    trade_pct_of_pool = (trade_usd / pool_liquidity_usd) * 100

    # Estimated price impact from constant-product AMM
    # price_impact ≈ trade_size / pool_liquidity (simplified)
    price_impact_bps = int(trade_pct_of_pool * 100)

    # Sandwich profitability: attacker captures portion of slippage headroom
    # Rough model: sandwich_profit ≈ 0.5 * slippage_headroom * trade_size
    slippage_headroom_bps = slippage_bps - price_impact_bps
    if slippage_headroom_bps < 0:
        slippage_headroom_bps = 0

    sandwich_profit_usd = (slippage_headroom_bps / 10000) * trade_usd * 0.5
    jito_tip_cost = 0.001 * sol_price  # ~0.001 SOL typical tip
    tx_fees = 0.000015 * sol_price * 2  # two transactions for sandwich

    net_mev_profit = sandwich_profit_usd - jito_tip_cost - tx_fees
    is_profitable_to_sandwich = net_mev_profit > 0.10  # $0.10 minimum

    # Volume ratio indicates MEV bot attention level
    volume_ratio = trade_usd / max(token_daily_volume_usd, 1)

    risk_level = "LOW"
    if is_profitable_to_sandwich and trade_pct_of_pool > 1.0:
        risk_level = "HIGH"
    elif is_profitable_to_sandwich or trade_pct_of_pool > 0.5:
        risk_level = "MEDIUM"

    return {
        "risk_level": risk_level,
        "trade_pct_of_pool": round(trade_pct_of_pool, 2),
        "estimated_price_impact_bps": price_impact_bps,
        "slippage_headroom_bps": slippage_headroom_bps,
        "estimated_sandwich_cost_usd": round(max(net_mev_profit, 0), 2),
        "is_profitable_to_sandwich": is_profitable_to_sandwich,
        "recommendations": _get_recommendations(
            risk_level, trade_size_sol, slippage_bps, trade_pct_of_pool
        ),
    }


def _get_recommendations(
    risk_level: str,
    trade_size_sol: float,
    slippage_bps: int,
    trade_pct_of_pool: float,
) -> list[str]:
    """Generate protection recommendations based on risk assessment."""
    recs = []
    if risk_level == "HIGH":
        recs.append("Use Jito bundle with 0.001-0.005 SOL tip")
        recs.append("Use private/protected RPC endpoint")
    if trade_pct_of_pool > 2.0:
        n_splits = max(2, int(trade_pct_of_pool))
        recs.append(f"Split into {n_splits} trades over 2-5 minutes")
    if slippage_bps > 100:
        recs.append(f"Reduce slippage from {slippage_bps}bps to 50-100bps")
    if risk_level in ("MEDIUM", "HIGH"):
        recs.append("Enable Jupiter dynamic slippage / MEV protection")
    if not recs:
        recs.append("Standard execution is likely safe for this trade size")
    return recs
```

## MEV Protection Strategies

### Strategy 1: Tight Slippage Settings

Set `slippageBps` as low as feasible. Sandwich profit is bounded by your slippage tolerance.

| Token Liquidity | Recommended Slippage |
|----------------|---------------------|
| > $5M pool | 50 bps (0.5%) |
| $1M - $5M pool | 100 bps (1%) |
| $100K - $1M pool | 150-200 bps |
| < $100K pool | 200-500 bps (high risk) |

**Trade-off:** Too-tight slippage causes failed transactions, costing you fees with no execution.

### Strategy 2: Jito Bundles

Submit your swap as a Jito bundle with a priority tip:

```python
import httpx

JITO_BLOCK_ENGINE = "https://mainnet.block-engine.jito.wtf"

async def submit_jito_bundle(
    signed_transactions: list[str],
    tip_lamports: int = 1_000_000,  # 0.001 SOL
) -> str:
    """Submit a transaction bundle to Jito block engine.

    Args:
        signed_transactions: Base64-encoded signed transactions.
        tip_lamports: Tip amount in lamports (1 SOL = 1e9 lamports).

    Returns:
        Bundle ID for tracking.
    """
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{JITO_BLOCK_ENGINE}/api/v1/bundles",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "sendBundle",
                "params": [signed_transactions],
            },
            timeout=10.0,
        )
        resp.raise_for_status()
        result = resp.json()
        return result.get("result", "")
```

**Tip guidelines:**
- Normal priority: 0.0001 - 0.001 SOL
- High priority: 0.001 - 0.01 SOL
- Urgent (volatile market): 0.01 - 0.05 SOL

### Strategy 3: Private/Protected RPCs

Send transactions through endpoints that do not expose them to searchers:

- **Jito bundles** (described above)
- **Helius priority fee API** with staked connections
- **QuickNode** private transaction submission
- **Direct TPU forwarding** (requires infrastructure)

### Strategy 4: Trade Splitting

For large trades (> 1% of pool liquidity), split execution:

```python
def compute_split_plan(
    total_sol: float,
    pool_liquidity_usd: float,
    sol_price: float = 150.0,
    max_pct_per_trade: float = 0.5,
) -> list[dict]:
    """Compute a trade splitting plan to minimize MEV exposure."""
    total_usd = total_sol * sol_price
    trade_pct = (total_usd / pool_liquidity_usd) * 100

    if trade_pct <= max_pct_per_trade:
        return [{"sol_amount": total_sol, "delay_seconds": 0}]

    n_splits = max(2, int(trade_pct / max_pct_per_trade) + 1)
    per_trade = total_sol / n_splits
    delay = 30  # seconds between trades

    return [
        {"sol_amount": round(per_trade, 4), "delay_seconds": i * delay}
        for i in range(n_splits)
    ]
```

### Strategy 5: Jupiter MEV Protection

Jupiter v6 includes built-in MEV protection features:
- **Dynamic slippage**: Automatically adjusts slippage to minimize sandwich window
- **Priority fee estimation**: Sets appropriate compute unit price
- **Transaction landing optimization**: Retry logic with increasing priority

Enable via Jupiter API:
```python
params = {
    "inputMint": "So11111111111111111111111111111111111111112",
    "outputMint": token_mint,
    "amount": str(amount_lamports),
    "slippageBps": "50",
    "dynamicSlippage": "true",        # Auto-adjust slippage
    "prioritizationFeeLamports": "auto",  # Auto priority fee
}
```

## Detecting Sandwich Attacks

After a trade, check whether you were sandwiched:

1. **Fetch your transaction** and identify the slot
2. **Fetch all transactions in that slot** involving the same token
3. **Look for the pattern**:
   - Transaction A: Buy TOKEN_X (before your tx in slot ordering)
   - Your transaction: Buy TOKEN_X (worse price than expected)
   - Transaction B: Sell TOKEN_X (after your tx, same signer as A)
4. **Verify**: Signer of A and B is the same wallet (the attacker)
5. **Estimate cost**: Difference between your expected and actual execution price

See `scripts/sandwich_detector.py` for a working implementation.

**Known MEV indicators:**
- Transaction signer has thousands of transactions per day
- Same-slot buy-then-sell of the same token around your swap
- Signer interacts with Jito tip program frequently
- Wallet has no token holdings (just in-and-out)

## Integration with Other Skills

- **`slippage-modeling`**: Use slippage estimates to set protective limits
- **`liquidity-analysis`**: Pool liquidity determines MEV vulnerability
- **`jupiter-api`**: Jupiter's MEV protection features and swap execution
- **`solana-onchain`**: On-chain transaction analysis for sandwich detection
- **`helius-api`**: Transaction parsing and historical analysis

## Files

### References
- `references/solana_mev_mechanics.md` — Solana block production, Jito block engine, MEV supply chain, and transaction flow paths
- `references/protection_strategies.md` — Detailed protection strategies with implementation guidance, cost-benefit analysis, and decision matrix

### Scripts
- `scripts/sandwich_detector.py` — Detects sandwich attacks around a given transaction signature using on-chain data
- `scripts/mev_risk_estimator.py` — Estimates MEV exposure for a planned trade based on token liquidity, trade size, and slippage settings

### Referencia: references/protection_strategies.md

# MEV Protection Strategies

## Strategy 1: Tight Slippage Settings

### Rationale

Sandwich attack profit is bounded by your slippage tolerance. If you set slippage to 50bps, the attacker can extract at most ~50bps of your trade value (minus their costs). Tighter slippage makes sandwiching less profitable or unprofitable.

### Implementation

```python
# Jupiter API quote with tight slippage
params = {
    "inputMint": "So11111111111111111111111111111111111111112",
    "outputMint": token_mint,
    "amount": str(amount_lamports),
    "slippageBps": "50",  # 0.5% — tight for liquid tokens
}
```

### Recommended Settings by Pool Liquidity

| Pool Liquidity (USD) | Slippage (bps) | Rationale |
|-----------------------|-----------------|-----------|
| > $10M | 30-50 | Deep liquidity, minimal natural slippage |
| $1M - $10M | 50-100 | Moderate liquidity, need some buffer |
| $100K - $1M | 100-200 | Thinner books, more natural price impact |
| < $100K | 200-500 | Very thin, high natural slippage, high MEV risk |

### Trade-offs

- **Too tight**: Transaction fails (you still pay base fee, get no execution)
- **Too loose**: Sandwich bots extract maximum value
- **Sweet spot**: Set slippage to ~1.5x your expected price impact

### Dynamic Approach

Monitor recent price volatility and adjust:
```python
def compute_safe_slippage(
    expected_impact_bps: float,
    recent_volatility_bps: float,
    safety_margin: float = 1.5,
) -> int:
    """Compute slippage that covers natural movement but limits MEV."""
    base = expected_impact_bps + recent_volatility_bps
    return max(30, int(base * safety_margin))
```

## Strategy 2: Jito Bundles

### Rationale

By submitting your transaction as a Jito bundle, you control the execution context. No searcher can insert transactions before or after yours within your bundle. You pay a tip for priority inclusion.

### When to Use

- Trade size > 5 SOL
- Trading illiquid tokens (< $1M pool)
- During high-MEV periods (meme coin launches, volatile markets)
- When you need guaranteed execution ordering

### Implementation

```python
import httpx
import base64

JITO_BLOCK_ENGINE = "https://mainnet.block-engine.jito.wtf"

async def get_tip_accounts() -> list[str]:
    """Fetch current Jito tip accounts."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{JITO_BLOCK_ENGINE}/api/v1/bundles",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getTipAccounts",
                "params": [],
            },
            timeout=10.0,
        )
        resp.raise_for_status()
        return resp.json().get("result", [])

async def send_bundle(
    serialized_txs: list[bytes],
    tip_lamports: int = 100_000,
) -> str:
    """Submit a bundle to Jito block engine.

    Args:
        serialized_txs: List of serialized, signed transactions.
        tip_lamports: Tip amount (1 SOL = 1_000_000_000 lamports).

    Returns:
        Bundle ID string.
    """
    encoded = [base64.b64encode(tx).decode() for tx in serialized_txs]
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{JITO_BLOCK_ENGINE}/api/v1/bundles",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "sendBundle",
                "params": [encoded],
            },
            timeout=10.0,
        )
        resp.raise_for_status()
        return resp.json().get("result", "")
```

### Tip Sizing Guide

| Scenario | Tip (SOL) | Tip (Lamports) |
|----------|-----------|----------------|
| Low priority, small trade | 0.0001 | 100,000 |
| Normal priority | 0.001 | 1,000,000 |
| High priority, large trade | 0.005 | 5,000,000 |
| Urgent (volatile market) | 0.01-0.05 | 10,000,000-50,000,000 |

**Rule of thumb**: Tip should be < 0.1% of trade value. If tip exceeds MEV risk, skip the bundle.

### Bundle Status Checking

```python
async def check_bundle_status(bundle_id: str) -> dict:
    """Check if a bundle was included."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{JITO_BLOCK_ENGINE}/api/v1/bundles",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getBundleStatuses",
                "params": [[bundle_id]],
            },
            timeout=10.0,
        )
        resp.raise_for_status()
        return resp.json().get("result", {})
```

## Strategy 3: Private / Protected RPCs

### Rationale

Standard public RPCs forward your transaction to multiple validators, increasing the number of parties that can observe it. Private RPCs minimize this exposure.

### Providers

| Provider | Feature | Endpoint |
|----------|---------|----------|
| Jito | Bundle submission | `mainnet.block-engine.jito.wtf` |
| Helius | Staked connections, priority fees | `mainnet.helius-rpc.com/?api-key=KEY` |
| QuickNode | Private transaction submission | Via QuickNode endpoint |
| Triton | Dedicated RPC with staked connections | Custom endpoint |

### How Staked Connections Help

Validators prioritize transactions from staked connections. With a staked RPC:
- Your transaction goes directly to the leader via a trusted channel
- Less forwarding through intermediary nodes
- Faster inclusion (competitive advantage over public RPC users)

### Implementation

```python
# Use Helius with staked connection for reduced MEV exposure
HELIUS_RPC = f"https://mainnet.helius-rpc.com/?api-key={os.getenv('HELIUS_API_KEY')}"

async def send_protected_transaction(signed_tx_base64: str) -> str:
    """Send transaction via Helius staked connection."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            HELIUS_RPC,
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "sendTransaction",
                "params": [
                    signed_tx_base64,
                    {"skipPreflight": False, "maxRetries": 3},
                ],
            },
            timeout=30.0,
        )
        resp.raise_for_status()
        return resp.json().get("result", "")
```

## Strategy 4: Trade Splitting

### Rationale

MEV profitability scales with trade size. Splitting a large trade into smaller pieces makes each individual piece less attractive to sandwich.

### When to Split

- Trade is > 1% of pool liquidity
- Estimated sandwich cost > $5
- Token is actively targeted by MEV bots (high volume micro-cap)

### Implementation

```python
import asyncio

async def execute_split_trades(
    total_sol: float,
    pool_liquidity_usd: float,
    max_pct_per_trade: float = 0.5,
    delay_seconds: int = 30,
    sol_price: float = 150.0,
) -> list[dict]:
    """Execute a trade in smaller pieces to reduce MEV exposure.

    Note: This is a framework. In production, each piece requires
    building, signing, and submitting a real transaction.
    """
    total_usd = total_sol * sol_price
    trade_pct = (total_usd / pool_liquidity_usd) * 100

    if trade_pct <= max_pct_per_trade:
        return [{"piece": 1, "sol": total_sol, "status": "single_trade"}]

    n = max(2, int(trade_pct / max_pct_per_trade) + 1)
    per_trade = total_sol / n
    results = []

    for i in range(n):
        if i > 0:
            await asyncio.sleep(delay_seconds)
        results.append({
            "piece": i + 1,
            "sol": round(per_trade, 4),
            "status": "submitted",
        })
    return results
```

### Trade-offs

- **Pro**: Each piece has lower MEV risk
- **Con**: Total execution takes longer; price may move against you
- **Con**: More transaction fees (base fee per trade)
- **Con**: Potential information leakage if pattern is detected

## Strategy 5: Jupiter MEV Protection

### Dynamic Slippage

Jupiter's dynamic slippage mode adjusts the slippage parameter based on:
- Current market volatility
- Historical fill rates at different slippage levels
- Pool depth and expected price impact

```python
params = {
    "inputMint": input_mint,
    "outputMint": output_mint,
    "amount": str(amount_lamports),
    "dynamicSlippage": "true",
    "prioritizationFeeLamports": "auto",
}
```

### Transaction Landing Improvements

Jupiter v6 includes retry logic and priority fee optimization that reduces the chance of failed transactions when using tight slippage.

## Decision Matrix

Use this matrix to select protection level:

| Trade Size | Liquid Token (>$5M pool) | Mid Liquidity ($500K-$5M) | Low Liquidity (<$500K) |
|-----------|--------------------------|---------------------------|------------------------|
| < 1 SOL | No protection needed | Tight slippage (50-100bps) | Tight slippage (100-200bps) |
| 1-10 SOL | Tight slippage (50bps) | Jito bundle + tight slippage | Jito bundle + split |
| 10-50 SOL | Tight slippage + private RPC | Jito bundle + split (2-3x) | Split (5x+) + Jito bundles |
| > 50 SOL | Split (2-3x) + Jito | Split (5x+) + Jito + private RPC | Avoid or OTC |

## Cost-Benefit Analysis

Only protect when MEV risk exceeds protection cost (tip + extra fees + delay).

**Rule of thumb:** Under 0.5 SOL in liquid pools: skip protection. 0.5-5 SOL: tight slippage. 5-50 SOL: Jito bundle + tight slippage. Over 50 SOL: full stack (split + Jito + private RPC).

### Referencia: references/solana_mev_mechanics.md

# Solana MEV Mechanics

## Solana Block Production

### Leader Schedule

Solana uses a rotating leader schedule. One validator is the "leader" for each slot (~400ms). The leader:
- Receives transactions from the network
- Orders them into a block
- Streams the block to the cluster via Turbine

The leader schedule is deterministic and known **2 epochs ahead** (~4 days). This means searchers know exactly which validator will produce each block, enabling targeted strategies.

### Slot Timing

- **Slot duration**: ~400ms (target)
- **Actual slot time**: 400-600ms depending on network load
- **Transactions per slot**: ~2,000-4,000 (theoretical max much higher)
- **Finality**: ~6.4 seconds (2/3 stake confirmation), but for MEV purposes, slot inclusion is what matters

### Transaction Flow (Standard)

```
User Wallet → RPC Node → TPU (Transaction Processing Unit) → Leader Validator → Block
                ↓
        (Forwarded to other validators for redundancy)
```

The TPU accepts transactions via UDP (QUIC since v1.15). There is no public mempool — transactions are forwarded directly to the current and upcoming leaders.

**However**, transactions are observable:
- RPC nodes forward to multiple leaders for reliability
- Jito block engine receives transactions from RPC infrastructure
- Validators can inspect incoming transactions before ordering

## Jito Block Engine

### Overview

Jito Labs operates a modified Solana validator client that adds an auction mechanism for transaction ordering. As of early 2025, approximately 85-90% of Solana validators run the Jito-modified client.

### How It Works

```
Searcher → Jito Block Engine → Jito-Modified Validator → Block

1. Searcher identifies MEV opportunity
2. Searcher constructs a "bundle" (ordered list of transactions)
3. Searcher submits bundle to Jito block engine with a SOL tip
4. Block engine validates the bundle (simulates execution)
5. Block engine forwards bundle to the current leader (if running Jito client)
6. Leader includes the bundle atomically in the block
7. Validator receives the tip
```

### Bundle Properties

- **Atomic execution**: All transactions in a bundle execute or none do
- **Ordered**: Transactions execute in the specified order within the bundle
- **Priority**: Higher tips get priority placement in the block
- **Size limit**: Up to 5 transactions per bundle
- **Simulation**: Block engine simulates before forwarding; reverted bundles are discarded

### Tip Mechanics

Tips are paid via a special Jito tip program. The tip transaction is included in the bundle:

```
Bundle = [
    tx_1 (front-run),
    tx_2 (victim's transaction),  # or reference to it
    tx_3 (back-run),
    tx_4 (tip to Jito: sendSOL to tip account)
]
```

**Tip distribution:**
- 100% of the tip goes to the validator producing the block
- Jito Labs charges no fee on tips (revenue from other services)

**Typical tip amounts (as of 2025):**
- Low priority: 1,000 - 10,000 lamports (0.000001 - 0.00001 SOL)
- Normal: 100,000 - 1,000,000 lamports (0.0001 - 0.001 SOL)
- High priority: 1,000,000 - 10,000,000 lamports (0.001 - 0.01 SOL)
- Competitive MEV: 10,000,000+ lamports (0.01+ SOL)

### Jito Endpoints

- **Mainnet block engine**: `https://mainnet.block-engine.jito.wtf`
- **Bundle submission**: `POST /api/v1/bundles` with `sendBundle` JSON-RPC method
- **Bundle status**: `POST /api/v1/bundles` with `getBundleStatuses` method
- **Tip accounts**: Rotate periodically; fetch via `getTipAccounts` method

## MEV Supply Chain on Solana

### Participants

1. **Users**: Submit swaps, provide liquidity, borrow/lend
2. **Searchers**: Identify and capture MEV opportunities. Run co-located infrastructure with sub-millisecond latency
3. **Block Engine (Jito)**: Auction platform connecting searchers to validators
4. **Validators**: Produce blocks, earn tips from MEV bundles
5. **Protocols**: DEXes, lending platforms — where MEV opportunities originate

### Value Flow

```
MEV Opportunity (user's swap creates arbitrage or sandwich opportunity)
    ↓
Searcher extracts value:
    gross_profit = extracted_value
    net_profit   = extracted_value - jito_tip - tx_fees - infrastructure_cost
    ↓
Jito tip to validator:
    validator_revenue = jito_tip
    ↓
Cost to user:
    user_cost = worse execution price (implicit cost, not a visible fee)
```

### MEV Extraction Economics

For a sandwich attack to be profitable:

```
sandwich_profit = victim_slippage_captured - (2 * tx_fee) - jito_tip - capital_cost

Where:
    victim_slippage_captured ≈ victim_trade_size * (slippage_bps / 10000) * capture_rate
    capture_rate ≈ 0.3 to 0.7 (depends on pool depth and attacker's capital)
    tx_fee ≈ 0.000005 SOL per transaction (5000 lamports base fee)
    jito_tip ≈ 0.0001 to 0.01 SOL (depends on competition)
    capital_cost ≈ minimal for atomic bundles (no holding risk)
```

**Minimum viable sandwich** (rough estimate):
- Trade size: > 0.5 SOL with > 100bps slippage in an illiquid pool
- Or: > 5 SOL with > 50bps slippage in a moderately liquid pool
- Below these thresholds, gas + tips exceed potential profit

## Transaction Flow Paths and MEV Visibility

### Path 1: Public RPC (Most Vulnerable)

```
User → Public RPC → Multiple Leaders (via QUIC)
                  → Jito Block Engine (intercepted)
```

Transactions are visible to the Jito block engine and any searcher connected to it. This is the most MEV-exposed path.

### Path 2: Private/Staked RPC (Less Visible)

```
User → Private RPC (Helius/QuickNode) → Current Leader Only
```

Staked connections can send directly to the leader. Fewer intermediaries see the transaction. Not immune to MEV but reduces the observation window.

### Path 3: Jito Bundle (User-Controlled Ordering)

```
User → Jito Block Engine → Leader
     (user IS the searcher, controlling tx order)
```

By submitting your own bundle, you control the ordering. A searcher cannot insert transactions into your bundle. This is the strongest MEV protection available.

### Path 4: Direct TPU (Requires Infrastructure)

```
User → Leader's TPU directly (UDP/QUIC)
```

Requires knowing the leader's TPU address and having network proximity. Used by professional trading firms. Minimizes intermediary visibility.

## Historical MEV on Solana

MEV on Solana has grown significantly:

- **2022-2023**: Early MEV, mostly arbitrage. Limited sandwich attacks due to lower DEX volume
- **2024**: Explosive growth with meme coin trading surge. Sandwich attacks became routine on Jupiter and Raydium swaps. Jito tips exceeded $1M/day during peak periods
- **2025**: MEV infrastructure matured. Protection mechanisms improved (Jupiter dynamic slippage, private RPCs). MEV remains significant but users have more tools to mitigate it

**Key metrics to track:**
- Jito bundle volume (indicates MEV activity level)
- Average Jito tip (indicates MEV competition/profitability)
- Sandwich attack frequency (via on-chain analysis)
- Protected vs unprotected transaction ratio


---

## SKILL: raptor-dex

- Fuente: `agiprolabs/claude-trading-skills` → `skills/raptor-dex` (MIT)
- Cuándo usarla: Self-hosted Solana DEX aggregator by SolanaTracker — multi-hop routing across 25+ DEXes, WebSocket streaming, Yellowstone Jet TPU submission, no rate limits
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/raptor-dex/` (raptor_quote.py, raptor_swap.py)

# Raptor — Self-Hosted Solana DEX Aggregator

Raptor is a self-hosted Rust binary that aggregates swap quotes across 25+ Solana DEXes. Unlike Jupiter, Raptor runs on your own infrastructure with **no rate limits**, **no API key**, and **no dependency on external API availability**. Free during public beta.

- **Program ID (Mainnet)**: `RaptorD5ojtsqDDtJeRsunPLg6GvLYNnwKJWxYE4m87`
- **GitHub**: [solanatracker/raptor-binary](https://github.com/solanatracker/raptor-binary)
- **Docs**: [docs.solanatracker.io/raptor/overview](https://docs.solanatracker.io/raptor/overview)

## Quick Start

```bash
# Clone the binary repo (includes required signature file)
git clone https://github.com/solanatracker/raptor-binary
cd raptor-binary

# Run with required environment variables
export RPC_URL="https://your-solana-rpc.com"
export YELLOWSTONE_ENDPOINT="https://your-yellowstone-grpc.com"
export YELLOWSTONE_TOKEN="your-token"  # if required by provider
./raptor
# Listens on 0.0.0.0:8080 by default
```

**Requirements**: Solana RPC endpoint + Yellowstone gRPC endpoint (for pool indexing). Raptor uses very few RPC calls during normal operation since pool state is streamed via Yellowstone.

**Signature file**: The `signature` file must be in the same directory as the Raptor binary. It authenticates your instance and is included in the repo clone. If you move the binary, copy the signature file with it.

## Execution Flow

```
1. GET  /quote              → Best route across 25+ DEXes
2. POST /swap               → Unsigned versioned transaction
3. Sign locally              → Your private key never leaves your machine
4. POST /send-transaction   → Submit via Yellowstone Jet TPU
5. GET  /transaction/{sig}  → Confirm status (pending/confirmed/failed/expired)
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/quote` | Get swap quote with multi-hop routing |
| `POST` | `/swap` | Build swap transaction from quote |
| `POST` | `/swap-instructions` | Get swap instructions only (no tx wrapper) |
| `POST` | `/quote-and-swap` | Quote + transaction in one request |
| `POST` | `/send-transaction` | Submit via Yellowstone Jet TPU with auto-retry |
| `GET` | `/transaction/:signature` | Track transaction status and parsed events |
| `GET` | `/health` | Health check (pools, cache, Yellowstone connection) |

## Get a Quote

```python
import httpx

RAPTOR = "http://localhost:8080"

resp = httpx.get(f"{RAPTOR}/quote", params={
    "inputMint": "So11111111111111111111111111111111111111112",   # SOL
    "outputMint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",  # USDC
    "amount": 1_000_000_000,  # 1 SOL in lamports
    "slippageBps": 50,
})
quote = resp.json()
print(f"Output: {quote['amountOut']} lamports")
print(f"Price impact: {quote['priceImpact']}%")
print(f"Route: {len(quote['routePlan'])} hops")
```

### Quote Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `inputMint` | string | Yes | Input token mint address |
| `outputMint` | string | Yes | Output token mint address |
| `amount` | integer | Yes | Amount in smallest unit (lamports) |
| `slippageBps` | string | No | Basis points or `"dynamic"` (default: 50) |
| `dexes` | string | No | Comma-separated DEX filter |
| `excludeDexes` | string | No | DEXes to exclude |
| `maxHops` | integer | No | 1-4 hops (default: 4) |
| `directRouteOnly` | boolean | No | Only single-hop routes |
| `pools` | string | No | Comma-separated pool address filter |
| `feeBps` | integer | No | Platform fee 0-1000 bps |
| `feeAccount` | string | No | Fee recipient wallet |

## Build and Sign a Swap

```python
import base64
import os

# Step 2: Build transaction from quote
resp = httpx.post(f"{RAPTOR}/swap", json={
    "quoteResponse": quote,
    "userPublicKey": "YOUR_WALLET_PUBKEY",
    "wrapUnwrapSol": True,
    "txVersion": "v0",
    "priorityFee": "auto",       # min|low|auto|medium|high|veryHigh|turbo|unsafeMax
    "maxPriorityFee": 100_000,    # cap in lamports
})
swap = resp.json()
# swap["swapTransaction"] is base64-encoded unsigned transaction

# Step 3: Sign locally (private key never sent to Raptor)
from solders.transaction import VersionedTransaction
from solders.keypair import Keypair

tx_bytes = base64.b64decode(swap["swapTransaction"])
tx = VersionedTransaction.from_bytes(tx_bytes)
keypair = Keypair.from_base58_string(os.getenv("PRIVATE_KEY"))
signed_tx = VersionedTransaction(tx.message, [keypair])
signed_b64 = base64.b64encode(bytes(signed_tx)).decode()

# Step 4: Submit via Yellowstone Jet TPU
resp = httpx.post(f"{RAPTOR}/send-transaction", json={
    "transaction": signed_b64,
})
result = resp.json()
print(f"Signature: {result['signature']}")

# Step 5: Track status
resp = httpx.get(f"{RAPTOR}/transaction/{result['signature']}")
status = resp.json()
# status: pending | confirmed | failed | expired
print(f"Status: {status['status']}, Latency: {status.get('latency_ms')}ms")
```

## WebSocket Streaming

Real-time quote streaming with slot-based updates when pool state changes:

```python
import asyncio, websockets, json

async def stream_quotes():
    async with websockets.connect("ws://localhost:8080/stream") as ws:
        await ws.send(json.dumps({
            "type": "subscribe",
            "inputMint": "So11111111111111111111111111111111111111112",
            "outputMint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
            "amount": 1_000_000_000,
            "slippageBps": "50",
        }))
        async for msg in ws:
            data = json.loads(msg)
            if data.get("type") == "quote":
                print(f"Out: {data['data']['amountOut']} (slot {data['data']['contextSlot']})")
```

`/stream/swap` variant pre-builds transactions ready for signing, with automatic resend every 10 slots to prevent expiry.

## Supported DEXes (25+)

**Raydium**: AMM, CLMM, CPMM, LaunchLab | **Meteora**: DLMM, Dynamic AMM, DAMM V2, Curve, DBC | **Orca**: Whirlpool v1/v2 | **Bonding Curves**: Pump.fun, Pumpswap, Heaven, MoonIt, Boopfun | **PropAMM**: Humidifi, Tessera, Solfi V1/V2, AlphaQ, ZeroFi, BisonFi, GoonFi V2 | **Other**: FluxBeam, PancakeSwap V3

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `RPC_URL` | Yes | — | Solana RPC endpoint |
| `YELLOWSTONE_ENDPOINT` | Yes | — | Yellowstone gRPC endpoint |
| `YELLOWSTONE_TOKEN` | No | — | Auth token (if provider requires) |
| `BIND_ADDR` | No | `0.0.0.0:8080` | Listen address |
| `INCLUDE_DEXES` | No | all | Comma-separated DEX filter |
| `EXCLUDE_DEXES` | No | none | DEXes to exclude |
| `WORKER_THREADS` | No | CPU cores | Worker thread count |
| `ENABLE_WEBSOCKET` | No | false | Enable `/stream` endpoints |
| `ENABLE_YELLOWSTONE_JET` | No | false | Enable Jet TPU for `/send-transaction` |
| `ENABLE_ARBITRAGE` | No | false | Enable circular arbitrage routes |

### CLI Flags

```bash
./raptor --include-dexes raydium,orca,meteora \
         --enable-websocket \
         --enable-yellowstone-jet \
         --workers 4
```

### DEX Filtering Examples

```bash
# Only bonding curve DEXes (for PumpFun sniping)
INCLUDE_DEXES="pumpfun,pumpswap,heaven,moonit,boopfun" ./raptor

# Only major AMMs
INCLUDE_DEXES="raydium,orca,meteora" ./raptor
```

## Priority Fee Levels

| Level | Use Case |
|-------|----------|
| `min` / `low` | Cost-saving, non-urgent |
| `auto` / `medium` | Recommended default |
| `high` / `veryHigh` | Faster confirmation |
| `turbo` / `unsafeMax` | Maximum speed, competitive scenarios |

## Raptor vs Jupiter

| Feature | Raptor | Jupiter |
|---------|--------|---------|
| Self-hosted | Yes | No |
| Rate limits | None (your hardware) | API rate limits |
| DEX coverage | 25+ | 30+ |
| Latency | Network-local | Remote API |
| Cost | Free (beta) | Free (hosted) |
| Tx submission | Yellowstone Jet TPU | Standard RPC |
| On-chain program | `RaptorD5o...` | `JUP...` |
| API key required | No | No |

## Deployment

See `references/deployment.md` for Docker, Fly.io, and bare metal setup.

## Files

### References
- `references/api_reference.md` — Complete HTTP and WebSocket API with request/response schemas
- `references/deployment.md` — Docker, Fly.io, bare metal deployment with signature file handling
- [docs.solanatracker.io/raptor/overview](https://docs.solanatracker.io/raptor/overview) — Official Raptor documentation
- [github.com/solanatracker/raptor-binary](https://github.com/solanatracker/raptor-binary) — Binary releases and README

### Scripts
- `scripts/raptor_quote.py` — Get and compare swap quotes with --demo mode
- `scripts/raptor_swap.py` — Full swap flow: quote → build → sign → submit → confirm (simulation only in --demo)

### Referencia: references/api_reference.md

# Raptor API Reference

Complete HTTP and WebSocket API for the Raptor DEX aggregator.

## HTTP Endpoints

### GET /quote

Get the best swap quote across all supported DEXes.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `inputMint` | string | Yes | Input token mint address |
| `outputMint` | string | Yes | Output token mint address |
| `amount` | integer | Yes | Amount in smallest unit (lamports for SOL) |
| `slippageBps` | string | No | Basis points (e.g. `50`) or `"dynamic"` |
| `dexes` | string | No | Comma-separated DEX whitelist |
| `excludeDexes` | string | No | Comma-separated DEX blacklist |
| `maxHops` | integer | No | Max routing hops 1-4 (default: 4) |
| `directRouteOnly` | boolean | No | Only single-hop routes |
| `pools` | string | No | Comma-separated pool address filter |
| `mints` | string | No | Comma-separated intermediate mint allowlist |
| `feeBps` | integer | No | Platform fee 0-1000 bps |
| `feeAccount` | string | No | Fee recipient wallet |

**Response**:
```json
{
  "amountIn": 1000000000,
  "amountOut": 156234567,
  "otherAmountThreshold": 155453000,
  "priceImpact": 0.12,
  "slippageBps": 50,
  "routePlan": [
    {
      "inputMint": "So11...",
      "outputMint": "EPjF...",
      "amountIn": 1000000000,
      "amountOut": 156234567,
      "dex": "raydium_clmm",
      "pool": "pool_address..."
    }
  ],
  "contextSlot": 298765432
}
```

### POST /swap

Build a complete swap transaction from a quote.

**Request body**:
```json
{
  "quoteResponse": { /* from GET /quote */ },
  "userPublicKey": "wallet_pubkey",
  "wrapUnwrapSol": true,
  "txVersion": "v0",
  "priorityFee": "auto",
  "maxPriorityFee": 100000,
  "computeUnitLimit": null,
  "tip": null,
  "destinationTokenAccount": null
}
```

**Response**:
```json
{
  "swapTransaction": "base64_encoded_unsigned_transaction"
}
```

### POST /swap-instructions

Same as `/swap` but returns instructions only (no transaction wrapper). Useful for composing with other instructions.

### POST /quote-and-swap

Combined quote + transaction build in a single request. Accepts all `/quote` params plus `/swap` body fields.

### POST /send-transaction

Submit a signed transaction via Yellowstone Jet TPU. Requires `--enable-yellowstone-jet`.

**Request body**:
```json
{
  "transaction": "base64_encoded_signed_transaction"
}
```

**Response**:
```json
{
  "signature": "5abc..."
}
```

Raptor automatically retries submission for ~30 seconds or until confirmed.

### GET /transaction/:signature

Track a submitted transaction's status.

**Response**:
```json
{
  "signature": "5abc...",
  "status": "confirmed",
  "latency_ms": 450,
  "slot": 298765433,
  "events": [
    {
      "name": "SwapEvent",
      "parsed": {
        "amountIn": 1000000000,
        "amountOut": 156234567,
        "inputMint": "So11...",
        "outputMint": "EPjF..."
      }
    }
  ]
}
```

Status values: `pending`, `confirmed`, `failed`, `expired`

### GET /health

Returns pool count, cache status, and Yellowstone connection health.

---

## WebSocket API

### /stream — Real-time Quote Streaming

Connect and subscribe to receive updated quotes whenever pool state changes.

**Subscribe**:
```json
{
  "type": "subscribe",
  "inputMint": "So11...",
  "outputMint": "EPjF...",
  "amount": 1000000000,
  "slippageBps": "50"
}
```

**Quote update message**:
```json
{
  "type": "quote",
  "data": {
    "amountIn": 1000000000,
    "amountOut": 156234567,
    "priceImpact": 0.12,
    "routePlan": [...],
    "contextSlot": 298765432
  }
}
```

**Unsubscribe**: `{"type": "unsubscribe", "inputMint": "...", "outputMint": "..."}`

### /stream/swap — Streaming Swap Transactions

Same as `/stream` but returns pre-built transactions ready to sign. Automatically resends after 10 slots without an update to prevent transaction expiry.

**Subscribe** (additional fields):
```json
{
  "type": "subscribe",
  "inputMint": "So11...",
  "outputMint": "EPjF...",
  "amount": 1000000000,
  "slippageBps": "50",
  "userPublicKey": "wallet_pubkey",
  "priorityFee": "auto",
  "tip": null
}
```

**Swap update message**:
```json
{
  "type": "swap",
  "data": {
    "swapTransaction": "base64_unsigned_tx",
    "quote": { /* full quote data */ }
  }
}
```

---

## Error Codes

| Code | Meaning |
|------|---------|
| 400 | Invalid parameters or transaction |
| 404 | Transaction not tracked / token not found |
| 503 | Service unavailable (pool indexer still loading, Yellowstone disconnected) |

## Priority Fee Levels

| Level | Description |
|-------|-------------|
| `min` / `low` | Lowest fees, may take longer |
| `auto` / `medium` | Recommended — balances cost and speed |
| `high` / `veryHigh` | Higher fees for faster landing |
| `turbo` / `unsafeMax` | Maximum priority, use for competitive scenarios |

Fees are calculated per-route and per-DEX based on recent fee data.

### Referencia: references/deployment.md

# Raptor Deployment Guide

## Prerequisites

- **Solana RPC endpoint** — Any RPC provider (Helius, Triton, QuickNode, etc.)
- **Yellowstone gRPC endpoint** — Required for pool state streaming (Helius, Triton, Shyft)
- **Signature file** — Must be in the same working directory as the binary (included in repo clone)

Raptor uses very few RPC calls during normal operation since pool state is streamed via Yellowstone gRPC.

## Signature File

The `signature` file authenticates your Raptor instance. It is **required** and must be in the same directory where the binary runs.

```bash
# After cloning, both files are present:
ls raptor-binary/
# raptor          ← the binary
# signature       ← required auth file

# If you move the binary, ALWAYS copy the signature file too
cp raptor /opt/raptor/
cp signature /opt/raptor/
cd /opt/raptor && ./raptor   # signature must be in working directory
```

Without the signature file, Raptor will fail to start.

## Bare Metal / VPS

```bash
# Option A: Clone from GitHub
git clone https://github.com/solanatracker/raptor-binary
cd raptor-binary

# Option B: Download binary directly
curl -L https://github.com/solanatracker/raptor/releases/latest/download/raptor-linux-amd64 -o raptor
chmod +x raptor
# You still need the signature file from the repo

# Set environment and run
export RPC_URL="https://your-rpc.com"
export YELLOWSTONE_ENDPOINT="https://your-yellowstone.com"
export YELLOWSTONE_TOKEN="your-token"
./raptor
```

### Recommended: systemd Service

```ini
# /etc/systemd/system/raptor.service
[Unit]
Description=Raptor DEX Aggregator
After=network.target

[Service]
Type=simple
User=raptor
WorkingDirectory=/opt/raptor
ExecStart=/opt/raptor/raptor
Environment=RPC_URL=https://your-rpc.com
Environment=YELLOWSTONE_ENDPOINT=https://your-yellowstone.com
Environment=YELLOWSTONE_TOKEN=your-token
Environment=ENABLE_WEBSOCKET=true
Environment=ENABLE_YELLOWSTONE_JET=true
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now raptor
sudo journalctl -u raptor -f  # watch logs
```

## Docker

```dockerfile
FROM ubuntu:22.04
COPY raptor /usr/local/bin/raptor
COPY signature /usr/local/bin/signature
RUN chmod +x /usr/local/bin/raptor
WORKDIR /usr/local/bin
CMD ["raptor"]
```

```bash
docker build -t raptor .
docker run -d \
  -e RPC_URL="https://your-rpc.com" \
  -e YELLOWSTONE_ENDPOINT="https://your-yellowstone.com" \
  -e YELLOWSTONE_TOKEN="your-token" \
  -e ENABLE_WEBSOCKET=true \
  -p 8080:8080 \
  raptor
```

## Fly.io

```toml
# fly.toml
app = "my-raptor"
primary_region = "ewr"  # East US — pick closest to your RPC

[build]
  dockerfile = "Dockerfile"

[env]
  RPC_URL = "https://your-rpc.com"
  YELLOWSTONE_ENDPOINT = "https://your-yellowstone.com"
  INCLUDE_DEXES = "raydium,orca,meteora,pumpfun,pumpswap"
  ENABLE_WEBSOCKET = "true"
  ENABLE_YELLOWSTONE_JET = "true"

[[services]]
  internal_port = 8080
  protocol = "tcp"
  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]

[[vm]]
  size = "shared-cpu-2x"
  memory = "4gb"
```

```bash
fly secrets set YELLOWSTONE_TOKEN="your-token"
fly deploy
```

## DEX Filter Presets

```bash
# PumpFun sniping — only bonding curves
INCLUDE_DEXES="pumpfun,pumpswap,heaven,moonit,boopfun" ./raptor

# Major AMMs only
INCLUDE_DEXES="raydium,orca,meteora" ./raptor

# Everything except bonding curves
EXCLUDE_DEXES="pumpfun,pumpswap,heaven,moonit,boopfun" ./raptor
```

## Performance Tuning

| Setting | Recommendation |
|---------|---------------|
| `WORKER_THREADS` | Match CPU cores (default). For quote-heavy loads, try 2x cores |
| `RPC_RATE_LIMIT` | Set to your RPC provider's limit to avoid 429s |
| Region | Co-locate with your RPC and Yellowstone providers |
| Memory | 4GB minimum recommended for full DEX indexing |

## Health Check

```bash
curl http://localhost:8080/health
# Returns: pool count, cache status, Yellowstone connection state
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Slow startup (1-2 min) | Normal — pool indexing via Yellowstone. Use `--no-pool-indexer` to skip (quotes may be incomplete) |
| Quote returns 0 output | Token has no liquidity on included DEXes. Check `INCLUDE_DEXES` |
| Transaction fails | Check slippage, priority fee, and blockhash freshness |
| Signature file missing | Copy from repo clone to working directory |
| WebSocket not connecting | Set `ENABLE_WEBSOCKET=true` or `--enable-websocket` |
| `/send-transaction` 503 | Set `ENABLE_YELLOWSTONE_JET=true` and verify Yellowstone endpoint |


---

## SKILL: shredstream

- Fuente: `agiprolabs/claude-trading-skills` → `skills/shredstream` (MIT)
- Cuándo usarla: Pre-execution Solana transaction streaming via Jito ShredStream, Shyft RabbitStream, and Triton Deshred
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/shredstream/` (parse_shredstream_entries.py, rabbitstream_monitor.py)

# ShredStream — Pre-Execution Solana Data

ShredStream gives you transaction data **before the validator executes the block** — typically 100-500ms earlier than standard Yellowstone gRPC. You see transaction *intent*, not confirmed results.

This is the fastest path to Solana data for time-critical trading strategies.

## How It Works

Solana validators produce blocks by serializing transactions into **shreds** (~1,228 bytes each, sized for UDP MTU). Shreds propagate through Turbine (Solana's fanout protocol, 2-3 hops). ShredStream bypasses Turbine by receiving shreds **directly from leader validators** via Jito's Block Engine.

```
Leader Validator
     │
     ├── Turbine (standard, 2-3 hops, 200-500ms)
     │       └── Your RPC Node → Yellowstone gRPC (post-execution)
     │
     └── Jito Block Engine (direct)
              └── ShredStream Proxy (your server)
                   ├── UDP shreds → Your RPC/Validator (faster block building)
                   └── gRPC entries → Your Trading Bot (decoded transactions)
```

### What You Get vs. What You Don't

| Available (Pre-Execution) | NOT Available (Needs Execution) |
|---------------------------|--------------------------------|
| Transaction signatures | Success/failure status |
| Account keys (pubkeys) | Balance changes (pre/post) |
| Instructions (program, accounts, data) | Log messages |
| Address lookup table references | Inner instructions (CPI) |
| Slot number | Token balance changes |
| | Compute units consumed |

**Key tradeoff**: Speed for completeness. You see what's *about to happen* but can't confirm it actually succeeded. Some transactions you see will ultimately fail.

## Three Ways to Get Pre-Execution Data

| Provider | Product | Latency | Access | Cost |
|----------|---------|---------|--------|------|
| **Jito** | ShredStream Proxy | ~10-50ms from leader | Apply + auth keypair | Free (beta) |
| **Shyft** | RabbitStream | ~15-100ms faster than gRPC | Shyft gRPC plan | From $199/mo |
| **Triton** | Deshred (`SubscribeDeshred`) | ~6.3ms p50 from shred | Triton customer | ~$2,900+/mo |

See `references/providers_compared.md` for detailed comparison.

## Option 1: Jito ShredStream Proxy

The most direct approach — run Jito's open-source proxy on your own server.

### Get Access

1. Generate a Solana keypair: `solana-keygen new -o shred_auth.json`
2. Apply at [Jito's form](https://web.miniextensions.com/WV3gZjFwqNqITsMufIEp) with your public key
3. Wait for approval (your keypair gets whitelisted)
4. No staking requirement, free during beta

### Run the Proxy

```bash
# Clone and build
git clone https://github.com/jito-labs/shredstream-proxy.git --recurse-submodules
cd shredstream-proxy

# Run with gRPC enabled (key flag: --grpc-service-port)
RUST_LOG=info cargo run --release --bin jito-shredstream-proxy -- shredstream \
    --block-engine-url https://mainnet.block-engine.jito.wtf \
    --auth-keypair /path/to/shred_auth.json \
    --desired-regions ny,amsterdam \
    --dest-ip-ports 127.0.0.1:8001 \
    --grpc-service-port 7777
```

Docker (host networking required for UDP):

```bash
docker run -d --name shredstream-proxy --rm \
  --network host \
  -e RUST_LOG=info \
  -e BLOCK_ENGINE_URL=https://mainnet.block-engine.jito.wtf \
  -e AUTH_KEYPAIR=/app/shred_auth.json \
  -e DESIRED_REGIONS=ny,amsterdam \
  -e DEST_IP_PORTS=127.0.0.1:8001 \
  -e GRPC_SERVICE_PORT=7777 \
  -v /path/to/shred_auth.json:/app/shred_auth.json \
  jitolabs/jito-shredstream-proxy shredstream
```

### Configuration

| Parameter | Description | Example |
|-----------|-------------|---------|
| `BLOCK_ENGINE_URL` | Jito block engine endpoint | `https://mainnet.block-engine.jito.wtf` |
| `AUTH_KEYPAIR` | Path to whitelisted Solana keypair | `shred_auth.json` |
| `DESIRED_REGIONS` | Max 2, comma-separated | `ny,amsterdam` |
| `DEST_IP_PORTS` | Where to forward raw shreds (UDP) | `127.0.0.1:8001` |
| `GRPC_SERVICE_PORT` | Enable gRPC entry streaming | `7777` |
| `SRC_BIND_PORT` | Incoming shred UDP port | `20000` |

Available regions: `amsterdam`, `dublin`, `frankfurt`, `london`, `ny`, `salt-lake-city`, `singapore`, `tokyo`

### Verify It's Working

```bash
# Check shreds are arriving via UDP
sudo tcpdump 'udp and dst port 20000'
# Should see many ~1200-byte packets continuously
```

### Consume via gRPC

```rust
use jito_protos::shredstream::{
    shredstream_proxy_client::ShredstreamProxyClient,
    SubscribeEntriesRequest,
};

let mut client = ShredstreamProxyClient::connect("http://127.0.0.1:7777").await?;
let mut stream = client
    .subscribe_entries(SubscribeEntriesRequest {})
    .await?
    .into_inner();

while let Some(entry) = stream.message().await? {
    let entries: Vec<solana_entry::entry::Entry> =
        bincode::deserialize(&entry.entries)?;

    for e in &entries {
        for tx in &e.transactions {
            let sig = tx.signatures[0];
            let msg = tx.message();
            // Parse instructions, accounts, etc.
        }
    }

    println!("Slot {}: {} entries, {} transactions",
        entry.slot,
        entries.len(),
        entries.iter().map(|e| e.transactions.len()).sum::<usize>()
    );
}
```

## Option 2: Shyft RabbitStream

**Drop-in replacement** for Yellowstone gRPC — same `SubscribeRequest` format, just a different endpoint. Easiest way to get pre-execution data without running infrastructure.

```bash
export GRPC_ENDPOINT="https://rabbitstream.ny.shyft.to"
export GRPC_TOKEN="your-shyft-x-token"
```

```python
# Same code as yellowstone-grpc, just different endpoint
import grpc

endpoint = "rabbitstream.ny.shyft.to"
token = os.environ["GRPC_TOKEN"]

# ... standard Yellowstone connection code ...
# Subscribe to transactions — same filter format
request = SubscribeRequest(
    transactions={
        "pumpfun": SubscribeRequestFilterTransactions(
            account_include=["6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"],
            vote=False,
            failed=False,
        )
    },
    commitment=CommitmentLevel.PROCESSED,
)
```

**Limitations**: Only transaction filters work. No account, slot, or block subscriptions. The `meta` field is empty (no execution results).

Regional endpoints: `rabbitstream.{ny,va,ams,fra}.shyft.to`

## Option 3: Triton Deshred

Lowest latency (~6.3ms p50) via Triton's `SubscribeDeshred` RPC. Same Yellowstone client, different method.

```rust
// Requires yellowstone-grpc-client with Deshred support
let (mut tx, mut stream) = client.subscribe_deshred().await?;

tx.send(SubscribeDeshredRequest {
    deshred_transactions: hashmap!{
        "pumpfun".to_string() => SubscribeRequestFilterDeshredTransactions {
            vote: Some(false),
            account_include: vec!["6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P".into()],
            ..Default::default()
        }
    },
    ..Default::default()
}).await?;
```

**Access**: Triton customers only, paid beta, requires their custom Agave validator fork.

## Parsing Pre-Execution Transactions

Without execution metadata, parsing is simpler but requires program-specific knowledge.

### Identify the Program

```python
# From a raw VersionedTransaction (post-deserialization)
account_keys = [str(k) for k in tx.message.account_keys]
for ix in tx.message.instructions:
    program_id = account_keys[ix.program_id_index]
    if program_id == "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P":
        # This is a PumpFun instruction
        discriminator = ix.data[:8]
        # Decode instruction data per PumpFun IDL
```

### Instruction Discriminators

Most Solana programs use 8-byte discriminators (Anchor SHA256 hash of the instruction name). Match `instruction.data[:8]` against known values for each program.

```python
# Common approach
PUMPFUN_CREATE = bytes.fromhex("181ec828051c0777")
PUMPFUN_BUY = bytes.fromhex("66063d1201daebea")
PUMPFUN_SELL = bytes.fromhex("33e685a4017f83ad")

disc = ix.data[:8]
if disc == PUMPFUN_BUY:
    # Parse buy parameters from remaining bytes
    ...
```

**Warning**: Discriminator values are program-specific and can change between program versions. Always verify against the current program IDL. See the `pumpfun-mechanics` skill for PumpFun-specific parsing.

## Common Architecture: ShredStream + Yellowstone

Most production systems use both:

```
ShredStream (pre-execution)          Yellowstone gRPC (post-execution)
         │                                      │
         ▼                                      ▼
  Intent Detection                    Confirmation + Reconciliation
  "Wallet X is buying token Y"       "Buy succeeded, wallet now holds Z"
         │                                      │
         ▼                                      ▼
  Pre-compute Response                Execute / Update State
  (route, sign, prepare bundle)       (record PnL, update positions)
```

This gives you the speed advantage of ShredStream for signal detection while using Yellowstone for reliable state management.

## Deployment Requirements

- **Public IP required** — NAT breaks UDP shred delivery
- **Host networking** — Docker bridge mode drops shred packets
- **UDP port 20000** open for incoming shreds
- **Co-locate near validators** — Frankfurt, NY, Amsterdam, London, Tokyo recommended
- **Bare metal preferred** — Cloud VMs add 1-5ms jitter from shared NICs

See `references/deployment.md` for full infrastructure guide.

## Files

### References
- `references/providers_compared.md` — Jito ShredStream vs Shyft RabbitStream vs Triton Deshred
- `references/deployment.md` — Infrastructure requirements, region selection, firewall configuration
- `references/proto_reference.md` — ShredStream protobuf definitions and Entry parsing

### Scripts
- `scripts/parse_shredstream_entries.py` — Decode and analyze ShredStream gRPC entries
- `scripts/rabbitstream_monitor.py` — Connect to Shyft RabbitStream for pre-execution transaction monitoring

### Referencia: references/deployment.md

# ShredStream — Deployment & Infrastructure Guide

## Requirements

### Network
- **Public IP** — Required. NAT is not supported (shreds arrive via UDP)
- **UDP port 20000** — Open for incoming shreds (configurable via `SRC_BIND_PORT`)
- **Host networking** — Docker bridge mode drops UDP multicast. Use `--network host`
- **Low-jitter connection** — Bare metal preferred over cloud VMs

### Hardware (Recommended for HFT)
- **CPU**: Modern AMD (EPYC 9354/9005 series) or Intel Xeon
- **RAM**: 32GB+ (proxy itself is lightweight, but co-located services need more)
- **NIC**: 10Gbps+ with kernel bypass (DPDK/AF_XDP) for lowest latency
- **Storage**: NVMe SSD (for any logging/persistence)

### Software
- **Rust toolchain** (for building from source) or Docker
- **Solana CLI** (for keypair generation): `sh -c "$(curl -sSfL https://release.anza.xyz/stable/install)"`

## Region Selection

Choose regions closest to your server and to major validator clusters.

| Region | Code | Best For |
|--------|------|----------|
| New York | `ny` | US East coast, most Solana validators |
| Amsterdam | `amsterdam` | Europe, good validator density |
| Frankfurt | `frankfurt` | Europe, major datacenter hub |
| London | `london` | Europe |
| Salt Lake City | `salt-lake-city` | US West |
| Singapore | `singapore` | Asia-Pacific |
| Tokyo | `tokyo` | Asia-Pacific |
| Dublin | `dublin` | Europe |

**Max 2 regions per proxy instance.** Run multiple instances for more regions.

### Recommended Co-Location
For lowest latency, co-locate in datacenters near Solana validator clusters:
- **Frankfurt**: OVH, Equinix FR5
- **New York**: Equinix NY, TeraSwitch
- **Amsterdam**: Equinix AM, Interxion
- **Tokyo**: Equinix TY

Co-location trims 20-50ms vs. random cloud placement.

## Firewall Configuration

Each Jito region uses specific IP ranges for shred delivery. You must allow UDP traffic from these IPs on your shred receive port (default 20000).

Check the current IP allowlist at: https://docs.jito.wtf/lowlatencytxnfeed/

General rule:
```bash
# Allow UDP from Jito Block Engine IPs (example, verify current IPs in docs)
sudo ufw allow proto udp from <JITO_IP> to any port 20000
```

Also allow outbound HTTPS (443) for gRPC connection to the Block Engine.

## Running the Proxy

### Build from Source

```bash
git clone https://github.com/jito-labs/shredstream-proxy.git --recurse-submodules
cd shredstream-proxy
cargo build --release
```

### Systemd Service (Production)

```ini
[Unit]
Description=Jito ShredStream Proxy
After=network.target

[Service]
Type=simple
User=solana
Environment=RUST_LOG=info
ExecStart=/opt/shredstream/target/release/jito-shredstream-proxy shredstream \
    --block-engine-url https://mainnet.block-engine.jito.wtf \
    --auth-keypair /opt/shredstream/shred_auth.json \
    --desired-regions ny,amsterdam \
    --dest-ip-ports 127.0.0.1:8001 \
    --grpc-service-port 7777
Restart=always
RestartSec=5
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
```

```bash
sudo cp shredstream.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now shredstream
sudo journalctl -u shredstream -f  # monitor logs
```

### Docker (Host Networking)

```bash
docker run -d --name shredstream \
  --network host \
  --restart unless-stopped \
  -e RUST_LOG=info \
  -e BLOCK_ENGINE_URL=https://mainnet.block-engine.jito.wtf \
  -e AUTH_KEYPAIR=/app/shred_auth.json \
  -e DESIRED_REGIONS=ny,amsterdam \
  -e DEST_IP_PORTS=127.0.0.1:8001 \
  -e GRPC_SERVICE_PORT=7777 \
  -v /opt/shredstream/shred_auth.json:/app/shred_auth.json:ro \
  jitolabs/jito-shredstream-proxy shredstream
```

### Fly.io Deployment

For distributed setups, run the proxy on Fly.io near your target region:

```toml
# fly.toml
app = "my-shredstream"
primary_region = "ewr"  # Newark (close to NY)

[build]
image = "jitolabs/jito-shredstream-proxy"

[env]
RUST_LOG = "info"
BLOCK_ENGINE_URL = "https://mainnet.block-engine.jito.wtf"
DESIRED_REGIONS = "ny"
GRPC_SERVICE_PORT = "7777"

[[services]]
internal_port = 7777
protocol = "tcp"
[[services.ports]]
port = 7777

[[services]]
internal_port = 20000
protocol = "udp"
[[services.ports]]
port = 20000
```

**Note**: Fly.io may not support raw UDP well on all regions. Test thoroughly.

## Verification

### Check Shred Receipt
```bash
# Should see continuous stream of ~1200-byte UDP packets
sudo tcpdump -i any 'udp and dst port 20000' -c 10

# Count packets per second
sudo tcpdump -i any 'udp and dst port 20000' -w /dev/null 2>&1 | head -1
```

### Check gRPC Output
```bash
# If you have grpcurl installed
grpcurl -plaintext localhost:7777 shredstream.ShredstreamProxy/SubscribeEntries
```

### Check Proxy Logs
```bash
# Look for successful heartbeat responses and shred counts
journalctl -u shredstream --since "5 minutes ago" | grep -E "heartbeat|shred|entries"
```

## Monitoring

| Metric | How to Check | Alert On |
|--------|-------------|----------|
| Shreds/second | `tcpdump` packet count | < 100/sec (stream may be dead) |
| Heartbeat TTL | Proxy logs | Missed heartbeats (reconnection needed) |
| gRPC clients connected | Proxy logs | Unexpected disconnections |
| Entry deserialization errors | Proxy logs | Non-zero error rate |
| Slot gaps | Compare slots in entries | Gaps > 2 consecutive slots |

## Common Issues

### No Shreds Arriving
1. Check keypair is whitelisted (re-apply if needed)
2. Verify UDP port is open: `sudo ufw status | grep 20000`
3. Check Block Engine URL is reachable: `curl -s https://mainnet.block-engine.jito.wtf`
4. Ensure no NAT between you and the internet
5. Try different regions

### High Latency
1. Move closer to validators (Frankfurt/NY/Amsterdam)
2. Switch from cloud VM to bare metal
3. Check for CPU contention: `htop`
4. Verify NIC is not saturated

### Docker Shred Loss
- **Use host networking** (`--network host`), not bridge mode
- Bridge mode fragments UDP multicast and drops packets
- If host networking is unavailable, use `SRC_BIND_PORT` and explicit port mapping

### Referencia: references/proto_reference.md

# ShredStream — Protobuf & Data Reference

Source: [jito-labs/mev-protos](https://github.com/jito-labs/mev-protos/blob/master/shredstream.proto)

## Proto Definitions

### ShredStream Service (Block Engine ↔ Proxy)

```protobuf
service Shredstream {
  rpc SendHeartbeat(Heartbeat) returns (HeartbeatResponse) {}
}

message Heartbeat {
  shared.Socket socket = 1;   // IP must match incoming packet (anti-spoofing)
  repeated string regions = 2; // desired regions, max 2
}

message HeartbeatResponse {
  uint32 ttl_ms = 1;  // must send next heartbeat within this window
}
```

The proxy sends heartbeats to the Block Engine to maintain the shred stream. If a heartbeat is missed (exceeds `ttl_ms`), the stream stops.

### ShredStream Proxy Service (Proxy ↔ Your Code)

```protobuf
service ShredstreamProxy {
  rpc SubscribeEntries(SubscribeEntriesRequest) returns (stream Entry) {}
}

message SubscribeEntriesRequest {
  // Currently no filters — you get everything
}

message Entry {
  uint64 slot = 1;
  bytes entries = 2;  // bincode-serialized Vec<solana_entry::entry::Entry>
}
```

### Shared Types

```protobuf
message Socket {
  string ip = 1;
  int64 port = 2;
}
```

### Trace Shred (Debugging)

```protobuf
message TraceShred {
  string region = 1;
  google.protobuf.Timestamp created_at = 2;
  uint32 seq_num = 3;  // monotonically increases, resets on restart
}
```

## Solana Entry Structure

The `Entry.entries` field contains bincode-serialized `Vec<solana_entry::entry::Entry>`:

```rust
/// A Solana entry — a batch of transactions with a PoH hash
pub struct Entry {
    pub num_hashes: u64,                    // PoH hashes since previous entry
    pub hash: Hash,                         // resulting PoH hash (32 bytes)
    pub transactions: Vec<VersionedTransaction>,
}

/// A versioned transaction (v0 or legacy)
pub struct VersionedTransaction {
    pub signatures: Vec<Signature>,         // first is the tx signature
    pub message: VersionedMessage,          // legacy or v0
}

/// Transaction message (v0 with ALT support)
pub struct v0::Message {
    pub header: MessageHeader,
    pub account_keys: Vec<Pubkey>,          // static account keys
    pub recent_blockhash: Hash,
    pub instructions: Vec<CompiledInstruction>,
    pub address_table_lookups: Vec<MessageAddressTableLookup>,
}

pub struct CompiledInstruction {
    pub program_id_index: u8,               // index into account_keys
    pub accounts: Vec<u8>,                  // indices into account_keys
    pub data: Vec<u8>,                      // instruction data (program-specific)
}
```

## Parsing Flow

### Step 1: Receive Entry from gRPC

```rust
let entry_msg: Entry = stream.message().await?.unwrap();
let slot = entry_msg.slot;
```

### Step 2: Deserialize Entries

```rust
let entries: Vec<solana_entry::entry::Entry> =
    bincode::deserialize(&entry_msg.entries)
        .expect("failed to deserialize entries");
```

### Step 3: Extract Transactions

```rust
for entry in &entries {
    for tx in &entry.transactions {
        let signature = tx.signatures[0];
        let message = tx.message();

        // Static account keys
        let account_keys = message.static_account_keys();

        // Instructions
        for ix in message.instructions() {
            let program_id = account_keys[ix.program_id_index as usize];
            let accounts: Vec<Pubkey> = ix.accounts
                .iter()
                .map(|&i| account_keys[i as usize])
                .collect();
            let data = &ix.data;

            // Match by program ID
            if program_id == pumpfun_program_id {
                let discriminator = &data[..8];
                // Parse instruction-specific data
            }
        }
    }
}
```

### Step 4: Handle Address Lookup Tables (v0 Transactions)

v0 transactions may reference accounts via Address Lookup Tables (ALTs). These accounts are NOT in `static_account_keys()`. To resolve them:

```rust
// Check if transaction uses ALTs
if let VersionedMessage::V0(msg) = &tx.message {
    for lookup in &msg.address_table_lookups {
        // lookup.account_key = the ALT address
        // lookup.writable_indexes = indices into ALT for writable accounts
        // lookup.readonly_indexes = indices into ALT for readonly accounts

        // To resolve: fetch the ALT account data via RPC
        // let alt_data = rpc.get_account(&lookup.account_key).await?;
        // Parse addresses from ALT data at the specified indices
    }
}
```

**Important**: Without resolving ALTs, you may miss some accounts referenced in instructions. For pre-execution use cases where speed matters, you can:
1. Pre-cache frequently used ALTs (Jupiter, Raydium, etc.)
2. Skip ALT resolution and work only with static keys (misses some accounts)
3. Resolve lazily after initial signal detection

## What You Can Extract (Without Execution)

| Data | Available? | How |
|------|-----------|-----|
| Transaction signature | Yes | `tx.signatures[0]` |
| Signer (fee payer) | Yes | `account_keys[0]` |
| Programs called | Yes | `account_keys[ix.program_id_index]` |
| Instruction data | Yes | `ix.data` (decode per program IDL) |
| Static account keys | Yes | `message.static_account_keys()` |
| ALT-referenced accounts | Partial | Need ALT data to resolve indices |
| Success/failure | No | Transaction hasn't executed yet |
| Balance changes | No | Need execution results |
| Log messages | No | Need execution results |
| Inner instructions (CPI) | No | Need execution results |
| Token balance changes | No | Need execution results |
| Compute units | No | Need execution results |

## Comparison with Yellowstone gRPC Data

| Field | ShredStream Entry | Yellowstone SubscribeUpdateTransaction |
|-------|-------------------|---------------------------------------|
| Signature | `tx.signatures[0]` | `info.signature` |
| Slot | `entry.slot` | `tx_update.slot` |
| Account keys | `msg.static_account_keys()` | `msg.account_keys` (all resolved) |
| Instructions | `msg.instructions()` | `msg.instructions` |
| ALT resolution | Manual (need ALT data) | Automatic (loaded addresses in meta) |
| Execution status | Not available | `meta.err` |
| Balances | Not available | `meta.pre_balances`, `meta.post_balances` |
| Token balances | Not available | `meta.pre_token_balances`, `meta.post_token_balances` |
| Logs | Not available | `meta.log_messages` |
| Inner instructions | Not available | `meta.inner_instructions` |
| Compute units | Not available | `meta.compute_units_consumed` |
| Block position | Entry order within slot | `info.index` |

### Referencia: references/providers_compared.md

# Pre-Execution Streaming — Provider Comparison

## Overview

Three products offer pre-execution Solana data (transactions before block confirmation):

| | Jito ShredStream | Shyft RabbitStream | Triton Deshred |
|---|---|---|---|
| **How it works** | Raw shreds from Block Engine via UDP proxy | Shred-level extraction, Yellowstone-compatible format | Blockstore tap before Replay stage |
| **Latency** | 10-50ms from leader | 15-100ms faster than standard gRPC | ~6.3ms p50, ~20ms p90 |
| **Self-hosted?** | Yes (run proxy yourself) | No (managed service) | No (Triton infrastructure) |
| **API format** | Custom gRPC (`SubscribeEntries`) | Yellowstone gRPC (`Subscribe`) | Yellowstone gRPC (`SubscribeDeshred`) |
| **Filtering** | None (all entries) | Transaction filters only | Transaction filters (vote, accounts) |
| **Cost** | Free (beta) + server costs | From $199/mo (Shyft plan) | ~$2,900+/mo (Triton dedicated) |
| **ALT resolution** | No (raw transactions) | Yes | Yes |

## Jito ShredStream (Direct)

**Best for**: Teams running their own infrastructure who want maximum control and lowest cost.

### Pros
- Free during beta (no Jito fees)
- Open-source proxy ([jito-labs/shredstream-proxy](https://github.com/jito-labs/shredstream-proxy))
- Direct from Block Engine — no intermediary
- Can also feed shreds to your own RPC node for faster block building
- gRPC mode eliminates need for a full Solana node

### Cons
- Requires public IP with UDP access (no NAT)
- Must run and maintain the proxy yourself
- No server-side filtering — you get everything, must filter client-side
- Approval process required (keypair whitelisting)
- Entry deserialization is bincode, not protobuf (slightly more work)
- Limited to 2 regions per proxy instance

### Access
1. Generate keypair: `solana-keygen new -o shred_auth.json`
2. Submit public key at: https://web.miniextensions.com/WV3gZjFwqNqITsMufIEp
3. Wait for approval
4. Run proxy with `--grpc-service-port` to enable gRPC streaming

### Regions
amsterdam, dublin, frankfurt, london, ny, salt-lake-city, singapore, tokyo

## Shyft RabbitStream

**Best for**: Teams already using Shyft who want pre-execution data with minimal code changes.

### Pros
- **Drop-in replacement** for Yellowstone gRPC — same `SubscribeRequest` format
- No infrastructure to run — managed service
- Same x-token auth as regular Shyft gRPC
- Server-side transaction filtering (account_include, account_exclude, etc.)
- ALT resolution included
- Multiple regions available

### Cons
- Only transaction filters work (no account/slot/block subscriptions)
- No `meta` field (no execution results, as expected for pre-execution)
- Requires Shyft Build plan or higher ($199+/mo)
- Slightly higher latency than direct ShredStream (goes through Shyft infrastructure)

### Endpoints
- `rabbitstream.ny.shyft.to` (New York)
- `rabbitstream.va.shyft.to` (Virginia)
- `rabbitstream.ams.shyft.to` (Amsterdam)
- `rabbitstream.fra.shyft.to` (Frankfurt)

### Connection
Same as Yellowstone gRPC — just change the endpoint URL:
```python
endpoint = "rabbitstream.ny.shyft.to"  # instead of grpc.ny.shyft.to
# Everything else identical
```

## Triton Deshred

**Best for**: HFT teams who need absolute lowest latency and can afford Triton pricing.

### Pros
- Lowest measured latency: ~6.3ms p50, ~20ms p90
- Integrated into Yellowstone client (same library, different RPC method)
- Server-side filtering: vote, account_include, account_exclude, account_required
- ALT resolution included
- Historical data via Old Faithful

### Cons
- Paid beta, limited availability (waitlist)
- Requires Triton dedicated node (~$2,900+/mo)
- Requires Triton's custom Agave validator fork (not stock Agave)
- New API surface (`SubscribeDeshred` vs `Subscribe`)

### RPC Method
```protobuf
rpc SubscribeDeshred(stream SubscribeDeshredRequest) returns (stream SubscribeUpdateDeshred) {}
```

### Filter Definition
```protobuf
message SubscribeRequestFilterDeshredTransactions {
  optional bool vote = 1;
  repeated string account_include = 2;
  repeated string account_exclude = 3;
  repeated string account_required = 4;
}
```

## Decision Matrix

| If you need... | Use... |
|---|---|
| Lowest cost, willing to run infra | Jito ShredStream (free + server) |
| Minimal code changes from Yellowstone | Shyft RabbitStream |
| Absolute lowest latency | Triton Deshred |
| No self-hosted infrastructure | Shyft RabbitStream or Triton Deshred |
| Server-side filtering | Shyft RabbitStream or Triton Deshred |
| Feed shreds to your own validator | Jito ShredStream |

## Bundled Provider Access

Some RPC providers include ShredStream automatically:
- **Chainstack** — ShredStream on all Solana nodes
- **RPC Fast** — ShredStream gRPC as free add-on to dedicated nodes
- **Everstake** — Connect ($199/mo), Pro ($499/mo), Enterprise (custom)
- **QuickNode** — gRPC products on ShredStream-enabled leader nodes


---

## SKILL: solana-rpc

- Fuente: `agiprolabs/claude-trading-skills` → `skills/solana-rpc` (MIT)
- Cuándo usarla: Direct Solana blockchain interaction via JSON-RPC — account lookups, token balances, transaction submission, and program queries
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/solana-rpc/` (token_holders.py, wallet_scanner.py)

# Solana RPC — Direct Blockchain Interaction

The Solana JSON-RPC API provides direct read/write access to the blockchain. Use it for account state queries, token balance lookups, transaction building and submission, and program account enumeration. This is the low-level foundation when higher-level APIs (Birdeye, Helius, SolanaTracker) don't have the data you need.

## Quick Start

```python
import httpx

RPC = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")

def rpc_call(method: str, params: list = None) -> dict:
    resp = httpx.post(RPC, json={
        "jsonrpc": "2.0", "id": 1,
        "method": method, "params": params or [],
    }, timeout=30.0)
    return resp.json()

# Get SOL balance
result = rpc_call("getBalance", ["WALLET_PUBKEY"])
sol_balance = result["result"]["value"] / 1e9

# Get latest blockhash
result = rpc_call("getLatestBlockhash")
blockhash = result["result"]["value"]["blockhash"]
```

## RPC Providers

| Provider | Free Tier | Paid | Notes |
|----------|-----------|------|-------|
| Helius | 50K credits/day | $49+/mo | Enhanced RPCs, DAS API |
| QuickNode | Limited | $49+/mo | Multi-chain, WebSocket |
| Triton | No free tier | ~$300+/mo | Yellowstone gRPC bundled |
| Shyft | Limited | $49+/mo | Yellowstone gRPC bundled |
| Alchemy | 300M CU/mo | Scaling | Good free tier |
| Public (mainnet-beta) | Free | — | Rate limited, unreliable |

**Recommendation**: Use Helius or QuickNode for development. Never use public RPC for production trading.

## Core Read Methods

### Account & Balance

```python
# SOL balance (in lamports, divide by 1e9 for SOL)
getBalance(pubkey, {commitment: "confirmed"})

# Full account info (data, owner, lamports, executable)
getAccountInfo(pubkey, {encoding: "jsonParsed"})

# Multiple accounts in one call
getMultipleAccounts([pubkey1, pubkey2], {encoding: "jsonParsed"})
```

### Token Accounts

```python
# All SPL token accounts owned by a wallet
getTokenAccountsByOwner(wallet_pubkey, {
    "programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
}, {"encoding": "jsonParsed"})

# Token balance for a specific token account
getTokenAccountBalance(token_account_pubkey)

# Largest token accounts (top holders)
getTokenLargestAccounts(mint_pubkey)

# Total supply of a token
getTokenSupply(mint_pubkey)
```

### Transaction Data

```python
# Get parsed transaction by signature
getTransaction(signature, {
    "encoding": "jsonParsed",
    "maxSupportedTransactionVersion": 0,
})

# Recent transaction signatures for an address
getSignaturesForAddress(pubkey, {
    "limit": 20,
    "before": "optional_signature",  # pagination cursor
})

# Transaction status
getSignatureStatuses([sig1, sig2])
```

### Block & Slot

```python
# Current slot
getSlot({commitment: "confirmed"})

# Block data
getBlock(slot, {
    "encoding": "jsonParsed",
    "transactionDetails": "full",
    "maxSupportedTransactionVersion": 0,
})

# Latest blockhash (needed for tx building)
getLatestBlockhash({commitment: "confirmed"})

# Slot leader schedule
getLeaderSchedule()
```

### Program Accounts

```python
# All accounts owned by a program (with filters)
getProgramAccounts(program_pubkey, {
    "encoding": "jsonParsed",
    "filters": [
        {"dataSize": 165},  # Filter by account data size
        {"memcmp": {         # Filter by data content
            "offset": 32,
            "bytes": "base58_encoded_value",
        }},
    ],
})
```

**Warning**: `getProgramAccounts` without filters can return millions of results and timeout. Always use `dataSize` and/or `memcmp` filters.

### Priority Fees

```python
# Recent priority fee estimates
getRecentPrioritizationFees([account_pubkey])
# Returns array of { slot, prioritizationFee } for recent slots

# Minimum rent for account
getMinimumBalanceForRentExemption(data_length)
```

## Write Methods

### Send Transaction

```python
# Send a signed, serialized transaction
sendTransaction(base64_tx, {
    "encoding": "base64",
    "skipPreflight": False,
    "preflightCommitment": "confirmed",
    "maxRetries": 3,
})

# Simulate before sending
simulateTransaction(base64_tx, {
    "encoding": "base64",
    "sigVerify": False,
    "commitment": "confirmed",
})
```

### Transaction Confirmation

```python
import time

def confirm_transaction(rpc_url: str, signature: str, timeout: float = 30.0) -> bool:
    """Poll for transaction confirmation."""
    start = time.time()
    while time.time() - start < timeout:
        result = rpc_call("getSignatureStatuses", [[signature]])
        statuses = result.get("result", {}).get("value", [None])
        if statuses[0] is not None:
            status = statuses[0]
            if status.get("err"):
                return False
            if status.get("confirmationStatus") in ("confirmed", "finalized"):
                return True
        time.sleep(0.5)
    return False
```

## Commitment Levels

| Level | Description | Use When |
|-------|-------------|----------|
| `processed` | Single node confirmation | Speed over safety |
| `confirmed` | Supermajority (2/3+) | **Default for trading** |
| `finalized` | Maximum supermajority + 31 slots | Critical operations |

Always specify commitment explicitly. Default varies by provider.

## Common Patterns

### Get All Token Holdings for a Wallet

```python
def get_wallet_tokens(wallet: str) -> list[dict]:
    """Get all SPL token holdings with metadata."""
    result = rpc_call("getTokenAccountsByOwner", [
        wallet,
        {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"},
        {"encoding": "jsonParsed"},
    ])
    tokens = []
    for acct in result["result"]["value"]:
        info = acct["account"]["data"]["parsed"]["info"]
        tokens.append({
            "mint": info["mint"],
            "amount": int(info["tokenAmount"]["amount"]),
            "decimals": info["tokenAmount"]["decimals"],
            "ui_amount": info["tokenAmount"]["uiAmount"],
        })
    return [t for t in tokens if t["amount"] > 0]
```

### Get Top Holders of a Token

```python
def get_top_holders(mint: str) -> list[dict]:
    """Get the 20 largest holders of a token."""
    result = rpc_call("getTokenLargestAccounts", [mint])
    supply_result = rpc_call("getTokenSupply", [mint])
    total_supply = int(supply_result["result"]["value"]["amount"])

    holders = []
    for acct in result["result"]["value"]:
        amount = int(acct["amount"])
        holders.append({
            "address": acct["address"],
            "amount": amount,
            "decimals": acct["decimals"],
            "ui_amount": acct["uiAmount"],
            "percentage": amount / total_supply * 100 if total_supply > 0 else 0,
        })
    return holders
```

### Batch RPC Calls

```python
def rpc_batch(calls: list[tuple[str, list]]) -> list[dict]:
    """Execute multiple RPC calls in a single HTTP request."""
    payload = [
        {"jsonrpc": "2.0", "id": i, "method": method, "params": params}
        for i, (method, params) in enumerate(calls)
    ]
    resp = httpx.post(RPC, json=payload, timeout=30.0)
    results = resp.json()
    results.sort(key=lambda r: r["id"])
    return [r.get("result") for r in results]
```

## Key Program IDs

| Program | ID |
|---------|-----|
| System | `11111111111111111111111111111111` |
| SPL Token | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` |
| Token-2022 | `TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb` |
| Associated Token | `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL` |
| Raydium AMM | `675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8` |
| Raydium CLMM | `CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK` |
| Orca Whirlpool | `whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc` |
| Meteora DLMM | `LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo` |
| PumpFun | `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P` |
| Jupiter v6 | `JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4` |
| Compute Budget | `ComputeBudget111111111111111111111111111111` |

## When to Use Direct RPC vs Higher-Level APIs

| Need | Use |
|------|-----|
| Token balance check | **Direct RPC** (`getTokenAccountsByOwner`) |
| Top 20 holders | **Direct RPC** (`getTokenLargestAccounts`) |
| Historical OHLCV | Birdeye or SolanaTracker |
| Parsed transaction history | Helius Enhanced Transactions |
| Token metadata (name, image) | Helius DAS API |
| Real-time streaming | Yellowstone gRPC |
| Wallet PnL tracking | SolanaTracker |
| Token risk scoring | SolanaTracker |
| Cross-chain data | DexScreener or CoinGecko |

## Files

### References
- `references/methods.md` — Complete RPC method reference with parameters and response schemas
- `references/error_handling.md` — Error codes, rate limits, timeout handling, retry strategies
- `references/providers.md` — RPC provider comparison with pricing and features

### Scripts
- `scripts/wallet_scanner.py` — Scan wallet for all token holdings with balances
- `scripts/token_holders.py` — Get top holders and concentration metrics for any token

### Referencia: references/error_handling.md

# Solana RPC — Error Handling & Rate Limits

## JSON-RPC Error Codes

| Code | Message | Cause | Action |
|------|---------|-------|--------|
| -32600 | Invalid request | Malformed JSON | Fix request format |
| -32601 | Method not found | Typo in method name | Check method name |
| -32602 | Invalid params | Wrong parameter types | Check param format |
| -32003 | Transaction simulation failed | Tx would fail on-chain | Check simulation logs |
| -32004 | Block not available | Slot was skipped | Try adjacent slot |
| -32005 | Node is behind | Node not synced | Use different node or retry |
| -32007 | Transaction precompile verification failure | Bad signature | Re-sign transaction |
| -32009 | Transaction has already been processed | Duplicate submission | Tx already landed |
| -32010 | Transaction version unsupported | Missing version param | Add `maxSupportedTransactionVersion: 0` |
| -32014 | Slot was skipped | Leader didn't produce block | Normal, try next slot |
| -32015 | No snapshot | Node doesn't have snapshot | Use different node |

## Rate Limits by Provider

| Provider | Requests/sec | Daily Limit | Batch Size |
|----------|-------------|-------------|------------|
| Public mainnet-beta | ~10-40 | Unlimited | 10 |
| Helius Free | ~50 | 50K credits | 100 |
| Helius Paid | ~500+ | By plan | 100 |
| QuickNode | By plan | By plan | 100 |
| Alchemy | ~25 CU/s free | 300M CU/mo | 100 |

## Retry Strategy

```python
import time
import httpx
from typing import Any

def rpc_call_with_retry(
    rpc_url: str,
    method: str,
    params: list,
    max_retries: int = 3,
    timeout: float = 30.0,
) -> dict[str, Any]:
    """Make an RPC call with exponential backoff retry.

    Args:
        rpc_url: RPC endpoint URL.
        method: RPC method name.
        params: Method parameters.
        max_retries: Maximum retry attempts.
        timeout: Request timeout in seconds.

    Returns:
        The 'result' field from the response.

    Raises:
        RuntimeError: On persistent failure or RPC error.
    """
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}

    for attempt in range(max_retries):
        try:
            resp = httpx.post(rpc_url, json=payload, timeout=timeout)

            if resp.status_code == 429:
                wait = 2.0 * (attempt + 1)
                time.sleep(wait)
                continue

            if resp.status_code >= 500:
                time.sleep(1.0 * (attempt + 1))
                continue

            resp.raise_for_status()
            data = resp.json()

            if "error" in data:
                err = data["error"]
                code = err.get("code", 0)

                # Retriable errors
                if code in (-32005, -32014):
                    time.sleep(1.0)
                    continue

                raise RuntimeError(f"RPC error {code}: {err.get('message')}")

            return data.get("result", {})

        except httpx.TimeoutException:
            if attempt < max_retries - 1:
                time.sleep(2.0 * (attempt + 1))
                continue
            raise

    raise RuntimeError(f"RPC call {method} failed after {max_retries} retries")
```

## Common Pitfalls

### 1. Versioned transactions require explicit opt-in
```python
# Wrong — will fail on versioned (v0) transactions
rpc_call("getTransaction", [sig])

# Right
rpc_call("getTransaction", [sig, {
    "encoding": "jsonParsed",
    "maxSupportedTransactionVersion": 0,
}])
```

### 2. getProgramAccounts without filters
This can return millions of accounts and timeout or OOM:
```python
# Wrong — returns ALL token accounts
rpc_call("getProgramAccounts", ["TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"])

# Right — filter by data size and/or memcmp
rpc_call("getProgramAccounts", ["TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA", {
    "filters": [{"dataSize": 165}],
    "encoding": "jsonParsed",
}])
```

### 3. Lamport vs SOL confusion
All RPC values are in lamports (1 SOL = 1,000,000,000 lamports).
All token amounts are in raw units (check decimals).

```python
sol = lamports / 1e9
token_amount = raw_amount / (10 ** decimals)
```

### 4. Commitment level defaults
Different providers may default to different commitment levels. Always specify explicitly:
```python
rpc_call("getBalance", [pubkey, {"commitment": "confirmed"}])
```

### 5. Blockhash expiration
Blockhashes expire after ~60-90 seconds. If building transactions:
- Fetch blockhash right before signing
- Submit immediately after signing
- Monitor `lastValidBlockHeight` to know when to retry

### 6. Null results
Many methods return `null` for accounts/transactions that don't exist:
```python
result = rpc_call("getAccountInfo", [pubkey])
if result["value"] is None:
    print("Account does not exist")
```

### Referencia: references/methods.md

# Solana RPC — Method Reference

All methods use POST to the RPC endpoint with JSON-RPC 2.0 format.

## Request Format

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "METHOD_NAME",
  "params": [/* method-specific */]
}
```

## Response Format

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": { /* method-specific */ }
}
```

On error:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": { "code": -32600, "message": "Invalid request" }
}
```

---

## Account Methods

### getBalance
Returns SOL balance in lamports (1 SOL = 1,000,000,000 lamports).
- **Params**: `[pubkey, {commitment}]`
- **Result**: `{ context: { slot }, value: lamports }`

### getAccountInfo
Returns all account data including owner program, data, and executable flag.
- **Params**: `[pubkey, {encoding, commitment, dataSlice}]`
- **Encodings**: `base58` (slow), `base64`, `base64+zstd`, `jsonParsed`
- **Result**: `{ context, value: { data, executable, lamports, owner, rentEpoch } }`
- **Note**: `jsonParsed` only works for known programs (Token, System, etc.)

### getMultipleAccounts
Batch lookup for up to 100 accounts.
- **Params**: `[[pubkey1, pubkey2, ...], {encoding, commitment}]`
- **Result**: `{ context, value: [account1, account2, ...] }`

---

## Token Methods

### getTokenAccountsByOwner
All SPL token accounts owned by a wallet.
- **Params**: `[owner_pubkey, {mint | programId}, {encoding, commitment}]`
- **Filter by mint**: `{"mint": "TOKEN_MINT"}` — accounts for a specific token
- **Filter by program**: `{"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"}` — all SPL tokens

### getTokenLargestAccounts
Top 20 largest holders of a token.
- **Params**: `[mint_pubkey, {commitment}]`
- **Result**: `{ value: [{ address, amount, decimals, uiAmount, uiAmountString }] }`

### getTokenSupply
Total supply of a token.
- **Params**: `[mint_pubkey, {commitment}]`
- **Result**: `{ value: { amount, decimals, uiAmount, uiAmountString } }`

### getTokenAccountBalance
Balance of a specific token account.
- **Params**: `[token_account_pubkey, {commitment}]`
- **Result**: `{ value: { amount, decimals, uiAmount } }`

---

## Transaction Methods

### getTransaction
Full transaction data by signature.
- **Params**: `[signature, {encoding, commitment, maxSupportedTransactionVersion}]`
- **Note**: Must set `maxSupportedTransactionVersion: 0` for versioned transactions.

### getSignaturesForAddress
Recent signatures involving an address.
- **Params**: `[pubkey, {limit, before, until, commitment}]`
- **Result**: `[{ signature, slot, err, memo, blockTime, confirmationStatus }]`
- **Limit**: Max 1000 per call. Use `before` for pagination.

### getSignatureStatuses
Check confirmation status of transactions.
- **Params**: `[[sig1, sig2, ...], {searchTransactionHistory}]`
- **Result**: `{ value: [{ slot, confirmations, err, confirmationStatus } | null] }`

### sendTransaction
Submit a signed transaction.
- **Params**: `[base64_tx, {encoding, skipPreflight, preflightCommitment, maxRetries, minContextSlot}]`
- **Result**: Transaction signature string
- **Note**: `skipPreflight: true` skips simulation (faster but riskier).

### simulateTransaction
Simulate without submitting.
- **Params**: `[base64_tx, {encoding, sigVerify, commitment, replaceRecentBlockhash}]`
- **Result**: `{ err, logs, accounts, unitsConsumed, returnData }`

---

## Block & Slot Methods

### getSlot
Current slot number.
- **Params**: `[{commitment}]`

### getBlock
Full block data.
- **Params**: `[slot, {encoding, transactionDetails, rewards, commitment, maxSupportedTransactionVersion}]`
- **transactionDetails**: `full`, `signatures`, `accounts`, `none`

### getLatestBlockhash
Current blockhash for transaction building.
- **Params**: `[{commitment}]`
- **Result**: `{ value: { blockhash, lastValidBlockHeight } }`

### isBlockhashValid
Check if a blockhash is still valid.
- **Params**: `[blockhash, {commitment}]`

### getBlockHeight
Current block height.
- **Params**: `[{commitment}]`

---

## Program Methods

### getProgramAccounts
All accounts owned by a program.
- **Params**: `[program_pubkey, {encoding, commitment, filters, dataSlice, withContext}]`
- **Filters**: `[{ dataSize: N }, { memcmp: { offset, bytes } }]`
- **Warning**: Without filters, this can return millions of accounts. Always filter.

### getRecentPrioritizationFees
Priority fee estimates from recent blocks.
- **Params**: `[[account_pubkey1, ...]]`
- **Result**: `[{ slot, prioritizationFee }]` — fee in micro-lamports per compute unit

### getMinimumBalanceForRentExemption
SOL needed to keep an account alive.
- **Params**: `[data_length_bytes]`
- **Result**: Lamports required

---

## Subscription Methods (WebSocket)

Connect via WebSocket (`wss://` version of RPC URL).

### accountSubscribe / accountUnsubscribe
Watch for account data changes.
- **Params**: `[pubkey, {encoding, commitment}]`

### logsSubscribe / logsUnsubscribe
Watch for transaction logs.
- **Params**: `[{mentions: [pubkey]} | "all" | "allWithVotes", {commitment}]`

### signatureSubscribe / signatureUnsubscribe
Watch for transaction confirmation.
- **Params**: `[signature, {commitment}]`

### slotSubscribe / slotUnsubscribe
Watch for slot changes.
- **Params**: `[]`

---

## Batch Requests

Send multiple calls in one HTTP request:

```json
[
  {"jsonrpc":"2.0","id":0,"method":"getBalance","params":["ADDR1"]},
  {"jsonrpc":"2.0","id":1,"method":"getBalance","params":["ADDR2"]},
  {"jsonrpc":"2.0","id":2,"method":"getBalance","params":["ADDR3"]}
]
```

Response is an array in the same order. Most providers support up to 100 calls per batch.

### Referencia: references/providers.md

# Solana RPC — Provider Comparison

## Provider Overview

| Provider | Free Tier | Entry Paid | Best For |
|----------|-----------|------------|----------|
| **Helius** | 50K credits/day | $49/mo (500K) | Best all-around, DAS API included |
| **QuickNode** | 50 req/s | $49/mo | Multi-chain, marketplace add-ons |
| **Triton** | No free | ~$300/mo | Yellowstone bundled, low latency |
| **Shyft** | Limited | $49/mo | Yellowstone + RabbitStream |
| **Alchemy** | 300M CU/mo | Scaling | Large free tier, enterprise |
| **Chainstack** | 3M req/mo | $29/mo | Budget option |
| **Public** | Free | — | Testing only |

## Detailed Comparison

### Helius
- **URL format**: `https://mainnet.helius-rpc.com/?api-key=YOUR_KEY`
- **Strengths**: DAS API, Enhanced Transactions, Webhooks, Priority Fee API
- **Free tier**: 50K credits/day (most calls = 1 credit)
- **Paid**: Developer $49/mo (500K), Business $199/mo (2M), Professional $999/mo (10M)
- **WebSocket**: Included
- **Yellowstone**: LaserStream on Professional tier ($999/mo)

### QuickNode
- **URL format**: `https://YOUR_ENDPOINT.solana-mainnet.quiknode.pro/YOUR_KEY`
- **Strengths**: Multi-chain (100+ chains), marketplace add-ons
- **Free tier**: 50 req/s, 10M API credits/mo
- **Paid**: Build $49/mo, Scale $299/mo
- **WebSocket**: Included
- **Yellowstone**: Available as add-on

### Triton (by Triton One)
- **URL format**: Custom endpoint provided
- **Strengths**: Lowest latency, Yellowstone (Dragon's Mouth) bundled, DeShed
- **Free tier**: None
- **Paid**: ~$300/mo+ (contact sales)
- **Yellowstone**: Dragon's Mouth gRPC included
- **Best for**: Professional/HFT operations

### Shyft
- **URL format**: `https://rpc.shyft.to?api_key=YOUR_KEY`
- **Strengths**: Yellowstone + RabbitStream (pre-exec streaming)
- **Free tier**: Limited
- **Paid**: $49/mo (Growth), $199/mo (Premium)
- **Yellowstone**: Included on paid tiers
- **RabbitStream**: Pre-execution data streaming

### Alchemy
- **URL format**: `https://solana-mainnet.g.alchemy.com/v2/YOUR_KEY`
- **Strengths**: Large free tier, auto-scaling, analytics dashboard
- **Free tier**: 300M compute units/mo
- **Paid**: Growth (scaling), Enterprise
- **Note**: CU-based pricing, different methods cost different CUs

## Choosing a Provider

### For development / research
Use **Helius** free tier — best DX, DAS API, and Enhanced Transactions included.

### For production trading
Use **Helius** paid or **Triton** — low latency, reliable, Yellowstone available.

### For multi-chain projects
Use **QuickNode** or **Alchemy** — both support 100+ chains.

### For HFT / latency-sensitive
Use **Triton** — lowest latency, Yellowstone bundled, bare-metal options.

## Public RPC Endpoints

For testing only — rate limited, unreliable, no SLA:
- `https://api.mainnet-beta.solana.com`
- `https://api.devnet.solana.com`
- `https://api.testnet.solana.com`

**Never use public endpoints for trading.** They are rate limited (10-40 req/s), may drop requests under load, and provide no uptime guarantees.

## Environment Setup

```bash
# Add to your shell profile (~/.zshrc or ~/.bashrc)
export SOLANA_RPC_URL="https://mainnet.helius-rpc.com/?api-key=YOUR_KEY"

# For development, also set devnet
export SOLANA_DEVNET_URL="https://api.devnet.solana.com"
```

```python
import os
RPC = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
```


---

## SKILL: solana-tx-building

- Fuente: `agiprolabs/claude-trading-skills` → `skills/solana-tx-building` (MIT)
- Cuándo usarla: Solana transaction construction including instruction building, account resolution, compute budget, priority fees, and versioned transactions
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/solana-tx-building/` (build_transfer.py, decode_transaction.py)

# Solana Transaction Building

This skill covers how to construct, simulate, and inspect Solana transactions programmatically. It addresses the full anatomy of a Solana transaction — from raw instruction encoding to versioned transaction formats, compute budget management, priority fees, and address lookup tables.

**Safety**: This skill is for transaction *construction* and *analysis* only. Scripts in this skill NEVER sign or submit real transactions. Always simulate before sending. Never auto-sign.

## Transaction Anatomy

A Solana transaction consists of:

1. **Signatures**: One or more Ed25519 signatures (64 bytes each)
2. **Message**: The serializable payload containing:
   - **Header**: Counts of required signers, read-only signers, read-only non-signers
   - **Account keys**: Array of all pubkeys referenced by instructions
   - **Recent blockhash**: 32-byte hash for replay protection (expires ~60-90 seconds)
   - **Instructions**: Array of program calls

### Transaction Size Limit

The hard limit is **1232 bytes** for the entire serialized transaction. This constrains how many instructions and accounts you can include. Strategies to stay within the limit:

- Use versioned transactions with Address Lookup Tables (ALTs)
- Minimize the number of accounts per instruction
- Combine related operations into single instructions where supported
- Split complex operations across multiple transactions

### Instruction Format

Each instruction contains three fields:

```
Instruction {
    program_id_index: u8,      // Index into the account keys array
    accounts: [u8],            // Indices into account keys array
    data: [u8],                // Opaque byte array interpreted by the program
}
```

### Account Meta

Every account referenced in an instruction has metadata:

```
AccountMeta {
    pubkey: Pubkey,            // 32-byte public key
    is_signer: bool,           // Must sign the transaction
    is_writable: bool,         // Will be written to by this instruction
}
```

The four combinations determine the account's role:

| is_signer | is_writable | Role |
|-----------|-------------|------|
| true | true | Fee payer, token owner performing transfer |
| true | false | Multisig co-signer, read-only authority |
| false | true | Destination account, PDA being written |
| false | false | Program ID, sysvar, clock |

## Legacy vs Versioned Transactions

### Legacy Transactions

The original format. All accounts must be listed in the account keys array. With the 1232-byte limit, you can fit roughly 20-35 accounts depending on instruction data size.

### Versioned Transactions (v0)

Introduced to support **Address Lookup Tables (ALTs)**. A v0 transaction includes:

- A version prefix byte (`0x80` for v0)
- The same message structure as legacy
- An additional `address_table_lookups` array

ALTs let you reference accounts by a compact index into an on-chain table rather than including the full 32-byte pubkey. This dramatically increases the number of accounts a transaction can reference.

```
AddressTableLookup {
    account_key: Pubkey,           // The ALT account address
    writable_indexes: [u8],        // Indices for writable accounts
    readonly_indexes: [u8],        // Indices for read-only accounts
}
```

**When to use v0**: Any transaction referencing more than ~20 accounts, Jupiter swaps with multi-hop routes, complex DeFi interactions.

## Compute Budget

Every transaction has a compute budget that determines how many compute units (CUs) it can consume and what priority fee to pay.

### Compute Budget Instructions

Two key instructions from the Compute Budget Program (`ComputeBudget111111111111111111111111111111`):

**1. Set Compute Unit Limit**
```
Instruction data: [0x02, <units as u32 LE>]
```
Sets the maximum CUs this transaction can consume. Default is 200,000 per instruction (max 1,400,000 per transaction). Setting this lower than needed causes the transaction to fail. Setting it higher wastes budget but does not cost more (you only pay for requested, not consumed).

**2. Set Compute Unit Price**
```
Instruction data: [0x03, <micro_lamports as u64 LE>]
```
Sets the price per CU in micro-lamports. This is the priority fee mechanism. The total priority fee is:

```
priority_fee = compute_unit_limit * compute_unit_price / 1_000_000
```

### Priority Fee Estimation

To estimate an appropriate priority fee:

1. Call `getRecentPrioritizationFees` RPC method with the accounts your transaction touches
2. Look at the median or 75th percentile fee from recent slots
3. During congestion, fees spike — monitor and adjust dynamically

```python
import httpx

def get_priority_fees(rpc_url: str, accounts: list[str]) -> list[dict]:
    """Fetch recent prioritization fees for given accounts."""
    resp = httpx.post(rpc_url, json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getRecentPrioritizationFees",
        "params": [accounts]
    })
    return resp.json()["result"]
```

## Common Transaction Patterns

### 1. SOL Transfer

The simplest transaction: a System Program transfer.

```python
# System Program transfer instruction data layout:
# [2, 0, 0, 0]  (u32 LE = instruction index 2 = Transfer)
# + amount as u64 LE (lamports)
import struct

def build_sol_transfer_data(lamports: int) -> bytes:
    """Build instruction data for a SOL transfer."""
    return struct.pack("<I", 2) + struct.pack("<Q", lamports)
```

Accounts required:
1. Sender (signer, writable)
2. Recipient (writable)

### 2. SPL Token Transfer

Transferring SPL tokens requires the Token Program.

```python
# Token Program transfer instruction:
# [3]  (instruction index 3 = Transfer)
# + amount as u64 LE
def build_token_transfer_data(amount: int) -> bytes:
    """Build instruction data for an SPL token transfer."""
    return bytes([3]) + struct.pack("<Q", amount)
```

Accounts required:
1. Source token account (writable)
2. Destination token account (writable)
3. Owner/delegate (signer)

### 3. Create Associated Token Account (ATA)

Before transferring tokens, the recipient must have an Associated Token Account.

```python
# ATA Program: instruction index 0 = Create
# No instruction data needed (empty bytes)
ATA_PROGRAM_ID = "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"
```

Accounts required (in order):
1. Payer (signer, writable) — pays rent
2. Associated token account (writable) — the ATA to create
3. Wallet address — owner of the new ATA
4. Token mint
5. System Program
6. Token Program

### 4. Jupiter Swap

Jupiter provides a `/swap-instructions` endpoint that returns pre-built instructions. See the `jupiter-api` skill for full details.

General flow:
1. Get a quote from `/quote`
2. Get swap instructions from `/swap-instructions`
3. Build transaction with setup instructions + swap instruction + cleanup instructions
4. Add compute budget instructions
5. Simulate, then sign and send

## Simulation

Always simulate before sending. Use the `simulateTransaction` RPC method:

```python
def simulate_transaction(rpc_url: str, tx_base64: str) -> dict:
    """Simulate a transaction without submitting it.

    Args:
        rpc_url: Solana RPC endpoint URL.
        tx_base64: Base64-encoded serialized transaction.

    Returns:
        Simulation result with logs and compute units consumed.
    """
    resp = httpx.post(rpc_url, json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "simulateTransaction",
        "params": [
            tx_base64,
            {"encoding": "base64", "replaceRecentBlockhash": True}
        ]
    })
    result = resp.json()["result"]
    if result["value"]["err"]:
        print(f"Simulation failed: {result['value']['err']}")
        for log in result["value"].get("logs", []):
            print(f"  {log}")
    else:
        cu = result["value"].get("unitsConsumed", 0)
        print(f"Simulation OK — {cu} compute units consumed")
    return result
```

The `replaceRecentBlockhash: True` flag lets you simulate even if your blockhash has expired, which is useful for testing transaction construction without timing pressure.

## Error Handling

Common transaction errors and their causes:

| Error | Cause | Fix |
|-------|-------|-----|
| `BlockhashNotFound` | Blockhash expired (~60-90s) | Fetch new blockhash and rebuild |
| `InsufficientFunds` | Not enough SOL for fees + transfer | Check balance before building |
| `AccountNotFound` | Token account doesn't exist | Create ATA first |
| `ProgramFailedToComplete` | Exceeded compute budget | Increase compute unit limit |
| `TransactionTooLarge` | Over 1232 bytes | Use ALTs or split into multiple txs |
| `InvalidAccountData` | Wrong account passed to instruction | Verify account derivation |
| `SignatureVerificationFailed` | Missing or wrong signer | Check all `is_signer` accounts signed |

### Retry Strategy

```python
import time

def send_with_retry(
    rpc_url: str,
    build_fn,
    max_retries: int = 3,
    base_delay: float = 0.5
) -> dict:
    """Build and send a transaction with blockhash refresh on expiry.

    Args:
        rpc_url: Solana RPC endpoint.
        build_fn: Callable that takes a blockhash and returns a signed tx.
        max_retries: Maximum retry attempts.
        base_delay: Base delay between retries in seconds.

    Returns:
        Send result from RPC.
    """
    for attempt in range(max_retries):
        blockhash = get_latest_blockhash(rpc_url)
        tx = build_fn(blockhash)
        result = send_transaction(rpc_url, tx)
        if "error" not in result:
            return result
        err = result["error"]
        if "BlockhashNotFound" in str(err):
            time.sleep(base_delay * (attempt + 1))
            continue
        raise RuntimeError(f"Transaction failed: {err}")
    raise RuntimeError("Max retries exceeded")
```

## Transaction Decoding

To decode an existing transaction from the chain:

```python
def decode_transaction(rpc_url: str, signature: str) -> dict:
    """Fetch and return a parsed transaction.

    Args:
        rpc_url: Solana RPC endpoint.
        signature: Transaction signature (base58).

    Returns:
        Parsed transaction data.
    """
    resp = httpx.post(rpc_url, json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTransaction",
        "params": [
            signature,
            {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}
        ]
    })
    return resp.json()["result"]
```

## Integration with Other Skills

- **`solana-rpc`**: Provides the RPC connection layer for submitting and querying transactions
- **`jupiter-api`**: Supplies swap instructions that this skill assembles into transactions
- **`dex-execution`**: Orchestrates the full execution flow using transactions built by this skill
- **`mev-analysis`**: Evaluates MEV risk of constructed transactions before submission
- **`helius-api`**: Enhanced transaction parsing and webhook-based confirmation tracking

## Safety Checklist

Before submitting any transaction to mainnet:

1. **Simulate first** — always call `simulateTransaction` before `sendTransaction`
2. **Verify accounts** — confirm all account addresses are correct (especially for token transfers)
3. **Check balances** — ensure sufficient SOL for fees and any transfers
4. **Review compute budget** — set appropriate CU limit based on simulation
5. **Confirm priority fee** — check current network fees, do not overpay
6. **Never auto-sign** — require explicit user confirmation before signing
7. **Use devnet for testing** — build and test on devnet before mainnet
8. **Log everything** — record transaction signatures, simulation results, and errors

## Files

### References
- `references/transaction_anatomy.md` — Message format, versioned transactions, compute budget, blockhash management
- `references/common_instructions.md` — Instruction layouts for System, Token, ATA, Compute Budget, Memo, and Jupiter programs

### Scripts
- `scripts/build_transfer.py` — Build and simulate a SOL transfer transaction (demo mode, never signs)
- `scripts/decode_transaction.py` — Fetch and decode on-chain transactions with program identification

### Referencia: references/common_instructions.md

# Common Solana Instructions Reference

## Program IDs

| Program | Address |
|---------|---------|
| System Program | `11111111111111111111111111111111` |
| Token Program | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` |
| Token-2022 | `TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb` |
| Associated Token Account | `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL` |
| Compute Budget | `ComputeBudget111111111111111111111111111111` |
| Memo Program | `MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr` |
| Memo Program (v1) | `Memo1UhkJBfCR6MNhJeXukzT2hbXzgnQ8e7MY1WDvN8` |
| Address Lookup Table | `AddressLookupTab1e1111111111111111111111111` |
| Jupiter v6 | `JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4` |

## System Program Instructions

### Transfer SOL

- **Instruction index**: 2 (u32 LE)
- **Data**: `[02 00 00 00] + [amount as u64 LE]`

```python
import struct

def system_transfer_data(lamports: int) -> bytes:
    """Build System Program transfer instruction data."""
    return struct.pack("<I", 2) + struct.pack("<Q", lamports)
```

**Accounts** (in order):
1. Source (signer, writable)
2. Destination (writable)

### Create Account

- **Instruction index**: 0 (u32 LE)
- **Data**: `[00 00 00 00] + [lamports u64 LE] + [space u64 LE] + [owner Pubkey 32 bytes]`

```python
def system_create_account_data(
    lamports: int, space: int, owner: bytes
) -> bytes:
    """Build System Program createAccount instruction data."""
    return (
        struct.pack("<I", 0)
        + struct.pack("<Q", lamports)
        + struct.pack("<Q", space)
        + owner  # 32 bytes
    )
```

**Accounts**:
1. Payer (signer, writable)
2. New account (signer, writable)

### Allocate

- **Instruction index**: 8 (u32 LE)
- **Data**: `[08 00 00 00] + [space u64 LE]`

**Accounts**:
1. Account to allocate (signer, writable)

## Token Program Instructions

### Transfer

- **Instruction index**: 3
- **Data**: `[03] + [amount u64 LE]`

```python
def token_transfer_data(amount: int) -> bytes:
    """Build Token Program transfer instruction data."""
    return bytes([3]) + struct.pack("<Q", amount)
```

**Accounts**:
1. Source token account (writable)
2. Destination token account (writable)
3. Owner (signer)

### Transfer Checked

- **Instruction index**: 12
- **Data**: `[0c] + [amount u64 LE] + [decimals u8]`

```python
def token_transfer_checked_data(amount: int, decimals: int) -> bytes:
    """Build Token Program transferChecked instruction data."""
    return bytes([12]) + struct.pack("<Q", amount) + bytes([decimals])
```

**Accounts**:
1. Source token account (writable)
2. Token mint (read-only)
3. Destination token account (writable)
4. Owner (signer)

Preferred over plain `transfer` because it validates the mint and decimals.

### Approve

- **Instruction index**: 4
- **Data**: `[04] + [amount u64 LE]`

**Accounts**:
1. Source token account (writable)
2. Delegate (read-only)
3. Owner (signer)

### Mint To

- **Instruction index**: 7
- **Data**: `[07] + [amount u64 LE]`

**Accounts**:
1. Mint (writable)
2. Destination token account (writable)
3. Mint authority (signer)

### Burn

- **Instruction index**: 8
- **Data**: `[08] + [amount u64 LE]`

**Accounts**:
1. Source token account (writable)
2. Mint (writable)
3. Owner (signer)

## Associated Token Account Program

### Create ATA

- **Instruction index**: 0 (implicit — no instruction data)
- **Data**: empty (`b""`)

```python
def ata_create_data() -> bytes:
    """ATA create instruction has no data."""
    return b""
```

**Accounts** (in order):
1. Payer (signer, writable) — pays rent for new account
2. Associated token account (writable) — the ATA to create
3. Wallet address (read-only) — owner of the ATA
4. Token mint (read-only)
5. System Program (read-only)
6. Token Program (read-only)

### Create Idempotent

- **Instruction index**: 1
- **Data**: `[01]`

Same accounts as Create ATA. Does not error if the ATA already exists. Preferred for transaction builders since you don't need to check existence first.

### ATA Derivation

The ATA address is a PDA derived from:
```
seeds = [wallet_address, token_program_id, mint_address]
program_id = ATA_PROGRAM_ID
```

```python
import hashlib

def derive_ata(wallet: bytes, mint: bytes) -> bytes:
    """Derive Associated Token Account address (simplified).

    Note: This is illustrative. Production code should use
    a proper PDA derivation with bump seed search.
    """
    TOKEN_PROGRAM = bytes.fromhex(
        "06ddf6e1d765a193d9cbe146ceeb79ac1cb485ed5f5b37913a8cf5857eff00a9"
    )
    ATA_PROGRAM = bytes.fromhex(
        "8c97258f4e2489f1bb3d1029148e0d830b5a1399daff1084048e7bd8dbe9f859"
    )
    # findProgramAddress searches for bump 255..0
    for bump in range(255, -1, -1):
        seed = wallet + TOKEN_PROGRAM + mint + bytes([bump])
        candidate = hashlib.sha256(seed + ATA_PROGRAM + b"ProgramDerivedAddress").digest()
        # Valid PDA must not be on the ed25519 curve (simplified check omitted)
        return candidate
    raise ValueError("Could not derive ATA")
```

## Compute Budget Program

### Set Compute Unit Limit

- **Discriminator**: `0x02`
- **Data**: `[02] + [units u32 LE]`

```python
def compute_budget_set_units(units: int) -> bytes:
    """Set compute unit limit for the transaction."""
    return bytes([2]) + struct.pack("<I", units)
```

**Accounts**: None required.

### Set Compute Unit Price

- **Discriminator**: `0x03`
- **Data**: `[03] + [micro_lamports u64 LE]`

```python
def compute_budget_set_price(micro_lamports: int) -> bytes:
    """Set compute unit price (priority fee) in micro-lamports."""
    return bytes([3]) + struct.pack("<Q", micro_lamports)
```

**Accounts**: None required.

### Request Heap Frame

- **Discriminator**: `0x01`
- **Data**: `[01] + [bytes u32 LE]`

Must be a multiple of 1024. Maximum 262,144 (256 KB).

**Accounts**: None required.

## Memo Program

### Add Memo

- **Data**: UTF-8 encoded memo string (arbitrary bytes)

```python
def memo_data(message: str) -> bytes:
    """Build memo instruction data."""
    return message.encode("utf-8")
```

**Accounts**: At least one signer (optional, but recommended for attribution).

The memo is stored in the transaction log and is visible in explorers. Maximum length is constrained by transaction size.

## Jupiter Swap Instructions

Jupiter provides swap instructions via the `/swap-instructions` API endpoint rather than requiring manual construction.

### API Flow

```python
import httpx

def get_jupiter_swap_instructions(
    quote: dict,
    user_pubkey: str,
) -> dict:
    """Get swap instructions from Jupiter API.

    Args:
        quote: Quote response from /quote endpoint.
        user_pubkey: The user's wallet public key.

    Returns:
        Dict with setupInstructions, swapInstruction,
        cleanupInstruction, and addressLookupTableAddresses.
    """
    resp = httpx.post(
        "https://quote-api.jup.ag/v6/swap-instructions",
        json={
            "quoteResponse": quote,
            "userPublicKey": user_pubkey,
            "dynamicComputeUnitLimit": True,
            "prioritizationFeeLamports": "auto",
        },
    )
    resp.raise_for_status()
    return resp.json()
```

The response contains pre-encoded instructions that you deserialize and include in your transaction. See the `jupiter-api` skill for full endpoint documentation.

### Referencia: references/transaction_anatomy.md

# Solana Transaction Anatomy

## Message Format

A Solana transaction message contains four sections:

### 1. Header (3 bytes)

```
MessageHeader {
    num_required_signatures: u8,          // Total signers required
    num_readonly_signed_accounts: u8,     // Signers that are read-only
    num_readonly_unsigned_accounts: u8,   // Non-signers that are read-only
}
```

The header determines how accounts in the account keys array are categorized:

```
Account keys array layout:
[0..num_required_signatures)                          → writable signers
[num_required_signatures - num_readonly_signed..num_required_signatures)  → read-only signers
[num_required_signatures..len - num_readonly_unsigned) → writable non-signers
[len - num_readonly_unsigned..len)                     → read-only non-signers
```

The first account in the writable signers section is always the **fee payer**.

### 2. Account Keys

A compact array of 32-byte public keys. Every account referenced by any instruction must appear here exactly once. The order matters because instructions reference accounts by index.

Deduplication rules:
- If an account is both writable and read-only across instructions, it is listed as writable
- If an account is both a signer and non-signer across instructions, it is listed as a signer
- The most permissive role wins

### 3. Recent Blockhash

A 32-byte hash that:
- Prevents replay attacks (same transaction cannot be submitted twice)
- Expires after ~60-90 seconds (~150 slots)
- Must be fetched fresh before building each transaction

### 4. Instructions

A compact array of compiled instructions:

```
CompiledInstruction {
    program_id_index: u8,    // Index of the program in account keys
    accounts: [u8],          // Indices of accounts in account keys
    data: [u8],              // Program-specific instruction data
}
```

## Versioned Transactions

### Legacy Format

```
[signatures_length, ...signatures, message_bytes]
```

Where `message_bytes` is:
```
[header(3), account_keys_length, ...account_keys(32 each),
 recent_blockhash(32), instructions_length, ...compiled_instructions]
```

### V0 Format

V0 transactions add a version prefix and address table lookups:

```
[0x80,  // version prefix (0x80 = v0)
 signatures_length, ...signatures,
 message_bytes,
 address_table_lookups_length, ...address_table_lookups]
```

Each address table lookup:
```
AddressTableLookup {
    account_key: Pubkey,           // 32 bytes — the ALT account
    writable_indexes: [u8],        // Compact array of writable indices
    readonly_indexes: [u8],        // Compact array of read-only indices
}
```

### Address Lookup Tables (ALTs)

ALTs are on-chain accounts that store up to 256 public keys. Instead of including a full 32-byte pubkey in the transaction, you reference it with a 1-byte index into the ALT.

**Space savings**: Each ALT reference saves 31 bytes per account (32-byte pubkey replaced by 1-byte index, plus the 32-byte ALT address amortized across lookups).

**Creating an ALT**:
```python
# AddressLookupTable program: AddressLookupTab1e1111111111111111111111111
# Instruction 0: CreateLookupTable
# Instruction 1: ExtendLookupTable (add addresses)
# Instruction 2: FreezeLookupTable
# Instruction 3: DeactivateLookupTable
# Instruction 4: CloseLookupTable
```

**Lookup flow**:
1. Transaction includes ALT account key + indices
2. Runtime loads the ALT account data
3. Resolves each index to the stored pubkey
4. Passes resolved accounts to the program

**Restrictions**:
- ALT accounts must be active (not deactivated)
- Newly added addresses require one slot to become usable
- Maximum 256 addresses per ALT
- Multiple ALTs can be used in a single transaction

## Compute Budget

### Default Limits

| Parameter | Default | Maximum |
|-----------|---------|---------|
| Compute units per instruction | 200,000 | — |
| Compute units per transaction | 200,000 * num_instructions | 1,400,000 |
| Heap size | 32 KB | 256 KB |
| Call depth | — | 4 |
| Stack frame size | — | 4 KB |

### Compute Budget Instructions

Program ID: `ComputeBudget111111111111111111111111111111`

**Set Compute Unit Limit** (instruction discriminator: `0x02`):
```
Data layout: [0x02, units: u32 LE]
Example: Set 300,000 CUs → [0x02, 0xe0, 0x93, 0x04, 0x00]
```

**Set Compute Unit Price** (instruction discriminator: `0x03`):
```
Data layout: [0x03, micro_lamports: u64 LE]
Example: Set 1000 micro-lamports → [0x03, 0xe8, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
```

**Request Heap Frame** (instruction discriminator: `0x01`):
```
Data layout: [0x01, bytes: u32 LE]
Must be multiple of 1024, max 256 KB (262144)
```

### Priority Fee Calculation

```
priority_fee_lamports = compute_unit_limit * compute_unit_price_micro_lamports / 1_000_000
```

Example: 300,000 CU limit at 5,000 micro-lamports/CU:
```
300,000 * 5,000 / 1,000,000 = 1,500 lamports = 0.0000015 SOL
```

The base transaction fee (5,000 lamports per signature) is always charged in addition to the priority fee.

## Transaction Size: 1232 Bytes

The maximum transaction size is 1232 bytes. This is a hard network limit (MTU-derived). Here is how the bytes break down for a typical transaction:

| Component | Size |
|-----------|------|
| Signatures length (compact-u16) | 1 byte |
| Each signature | 64 bytes |
| Header | 3 bytes |
| Account keys length (compact-u16) | 1-2 bytes |
| Each account key | 32 bytes |
| Recent blockhash | 32 bytes |
| Instructions length (compact-u16) | 1-2 bytes |
| Each instruction (variable) | ~5-100+ bytes |

**Budget estimation for a single-signer transaction**:
```
Fixed overhead: 64 (sig) + 1 (sig count) + 3 (header) + 32 (blockhash)
              + 2 (account count) + 2 (instruction count) = 104 bytes
Remaining for accounts + instructions: 1232 - 104 = 1128 bytes
Each account key: 32 bytes → ~35 accounts max with minimal instruction data
```

### Strategies to Fit Within 1232 Bytes

1. **Use v0 transactions with ALTs** — compress account references
2. **Minimize accounts** — only include necessary accounts
3. **Batch wisely** — split large operations across transactions
4. **Use compact instruction data** — avoid unnecessary padding

## Blockhash Management

### Fetching a Blockhash

```python
import httpx

def get_latest_blockhash(rpc_url: str) -> dict:
    """Get latest blockhash and its last valid block height.

    Returns:
        Dict with 'blockhash' (str) and 'lastValidBlockHeight' (int).
    """
    resp = httpx.post(rpc_url, json={
        "jsonrpc": "2.0", "id": 1,
        "method": "getLatestBlockhash",
        "params": [{"commitment": "finalized"}]
    })
    return resp.json()["result"]["value"]
```

### Blockhash Expiry and Retry

- A blockhash is valid for ~150 slots (~60-90 seconds)
- `lastValidBlockHeight` tells you the exact block height after which the blockhash expires
- If a transaction fails with `BlockhashNotFound`, fetch a new blockhash and rebuild
- For time-sensitive operations, use `commitment: "confirmed"` for faster (but slightly less safe) blockhashes
- For high-value operations, use `commitment: "finalized"` and accept the latency

### Durable Nonces (Advanced)

For transactions that need to remain valid longer than ~90 seconds:

1. Create a nonce account with `SystemProgram.createNonceAccount`
2. Use the nonce value as the "blockhash" in your transaction
3. Include an `AdvanceNonce` instruction as the first instruction
4. The transaction remains valid until the nonce is advanced

Use cases: offline signing, multi-party signatures, scheduled transactions.


---

## SKILL: solanatracker-api

- Fuente: `agiprolabs/claude-trading-skills` → `skills/solanatracker-api` (MIT)
- Cuándo usarla: Solana token data, PnL, risk scores, 1-second OHLCV, wallet analytics, and self-hosted swap execution via Raptor
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/solanatracker-api/` (token_analysis.py, wallet_pnl.py)

# SolanaTracker API — Token Data, Analytics & Raptor DEX Aggregator

SolanaTracker provides comprehensive Solana token data with unique features: **1-second OHLCV resolution**, **wallet PnL tracking**, **risk scoring**, **bundler/sniper detection**, and a **self-hosted DEX aggregator (Raptor)** supporting 25+ DEXes with no rate limits.

## Quick Start

```python
import httpx

API_KEY = os.getenv("SOLANATRACKER_API_KEY", "")
BASE = "https://data.solanatracker.io"
HEADERS = {"x-api-key": API_KEY}

# Token info with risk score, pools, holders
resp = httpx.get(f"{BASE}/tokens/{mint}", headers=HEADERS)
token = resp.json()
print(f"Risk: {token['risk']['score']}/10, Pools: {len(token['pools'])}")

# Wallet PnL
resp = httpx.get(f"{BASE}/pnl/{wallet}", headers=HEADERS)
pnl = resp.json()
print(f"Win rate: {pnl['summary']['winPercentage']}%")
```

## Authentication & Pricing

- **API Key**: From your SolanaTracker dashboard, passed as `x-api-key` header
- **Plans**: Starting ~€50/mo (200K requests), €200/mo (higher volume), Enterprise custom
- **Raptor**: Free during public beta (self-hosted, no rate limits)

## Core Data Endpoints

### Token Data

```python
# Full token info (metadata, pools, risk, events, holders summary)
GET /tokens/{tokenAddress}

# New tokens (paginated, pages 1-10)
GET /tokens/latest?page=1

# Trending by volume (default: past hour)
GET /tokens/trending
GET /tokens/trending/{timeframe}  # 5m, 15m, 30m, 1h, 4h, 12h, 24h

# Top performers
GET /tokens/top

# Graduated from bonding curves (pump.fun → Raydium)
GET /tokens/graduated
GET /tokens/graduating

# Multiple tokens in one request
GET /tokens/multi?tokens=ADDR1,ADDR2

# Deployer's tokens
GET /tokens/deployer/{deployerAddress}

# Token by pool address
GET /tokens/pool/{poolAddress}

# All-time high
GET /tokens/{token}/ath
```

### Price Data

```python
# Current price with liquidity and market cap
GET /price?token={address}

# Price with change percentages
GET /price?token={address}&priceChanges=true

# Historic prices (3d, 5d, 7d, 14d, 30d snapshots)
GET /price/history?token={address}

# Multiple token prices
GET /price/multi?tokens=ADDR1,ADDR2
```

### OHLCV Charts (1-second resolution)

```python
# Candle data — supports 1s resolution (unique to SolanaTracker)
GET /chart/{token}?type=1s&time_from=UNIX&time_to=UNIX

# Timeframes: 1s, 5s, 15s, 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1mn
# Optional: currency=usd|sol|eur, removeOutliers=true, marketCap=true

# Specialized charts
GET /chart/{token}/bundlers   # Bundler activity overlay
GET /chart/{token}/holders    # Holder count overlay
GET /chart/{token}/insiders   # Insider activity overlay
GET /chart/{token}/snipers    # Sniper activity overlay
```

### Wallet PnL

```python
# Full wallet PnL across all tokens
GET /pnl/{wallet}

# Token-specific PnL
GET /pnl/{wallet}/{token}

# First buyers with PnL
GET /first-buyers/{token}

# Optional params: showHistoricPnL=true (1d/7d/30d), holdingCheck=true
```

**PnL response summary fields**: `realized`, `unrealized`, `total`, `totalInvested`, `averageBuyAmount`, `totalWins`, `totalLosses`, `winPercentage`, `lossPercentage`

### Wallet Data

```python
# All tokens held by wallet
GET /wallet/{owner}

# Paginated wallet tokens
GET /wallet/{owner}/paginated

# Trade history
GET /wallet/{owner}/trades

# Portfolio chart over time
GET /wallet/{owner}/chart
```

### Holder Analysis

```python
# Paginated holder list
GET /tokens/{token}/holders?page=1

# Top 100 holders
GET /tokens/{token}/holders/top

# Top 20 holders (lighter)
GET /tokens/{token}/holders/top20

# Bundler detection
GET /tokens/{token}/bundlers
```

### Top Traders

```python
# Global top traders
GET /top-traders/all
GET /top-traders/all/paginated?page=1

# Token-specific top traders
GET /top-traders/{token}

# Optional: expandPnl=true, sortBy=total|winPercentage
```

### Risk Assessment

Risk is included in the `/tokens/{token}` response:

```json
{
  "risk": {
    "score": 7,        // 1-10 (10 = safest)
    "rugged": false,
    "jupiterVerified": true,
    "risks": [
      { "name": "Top 10 holders own 45%", "level": "warn" },
      { "name": "Freeze authority enabled", "level": "danger" }
    ]
  }
}
```

**Risk factors**: sniper/insider concentration, developer holdings, bundler activity, top 10 holder %, mint/freeze authority, social presence, metadata completeness, liquidity.

### Search (30+ filters)

```python
GET /search?query=BONK&minLiquidity=10000&minRiskScore=5&market=raydium&sortBy=volume&limit=50

# Key filters: query, symbol, minLiquidity, maxLiquidity, minMarketCap, maxMarketCap,
# minVolume, maxVolume, hasImage, hasSocials, minHolders, maxHolders, minRiskScore,
# freezeAuthority, mintAuthority, deployer, market, sortBy, sortOrder, limit (max 500), page
```

## Raptor — Self-Hosted DEX Aggregator

> **See the dedicated `raptor-dex` skill** for complete Raptor documentation including setup, API reference, deployment guides, WebSocket streaming, and execution scripts.

Raptor is SolanaTracker's self-hosted DEX aggregator: 25+ DEXes, no rate limits, no API key, Yellowstone Jet TPU submission. [GitHub](https://github.com/solanatracker/raptor-binary) | [Docs](https://docs.solanatracker.io/raptor/overview)

## DataStream WebSocket

Real-time streaming via WebSocket for 30+ event types:

```python
import websockets, json

async def stream():
    uri = f"wss://datastream.solanatracker.io/{DATASTREAM_KEY}"
    async with websockets.connect(uri) as ws:
        # Subscribe to token trades
        await ws.send(json.dumps({"type": "join", "room": f"transaction:{token_addr}"}))
        # Also: price:{token}, holders:{token}, latest_tokens, graduated, etc.
        async for msg in ws:
            data = json.loads(msg)
            if data.get("type") != "joined":
                print(data)
```

**Key channels**: `transaction:{token}`, `price:{token}`, `holders:{token}`, `latest_tokens`, `graduated`, `graduating`, `bundlers:{token}`, `insiders:{token}`, `snipers:{token}`, `wallet_transaction:{wallet}`

## When to Use SolanaTracker vs Alternatives

| Need | Use |
|------|-----|
| 1-second OHLCV candles | **SolanaTracker** |
| Wallet PnL tracking | **SolanaTracker** |
| Token risk scoring | **SolanaTracker** |
| Bundler/sniper detection | **SolanaTracker** |
| Self-hosted swap execution | **Raptor** |
| Free no-auth quick lookup | DexScreener |
| Real-time gRPC streaming | Yellowstone |
| Parsed transaction history | Helius |
| Cross-chain data | DexScreener or CoinGecko |

## Files

### References
- `references/data_api_endpoints.md` — Complete Data API endpoint reference with parameters and response schemas
- `references/raptor_setup.md` — Raptor quick-start reference (full docs in the `raptor-dex` skill)
- `references/risk_and_pnl.md` — Risk scoring methodology and PnL calculation details
- [docs.solanatracker.io/llms-full.txt](https://docs.solanatracker.io/llms-full.txt) — Complete SolanaTracker documentation (13K+ lines, LLM-optimized) covering Data API, Swap API, Datastream WebSocket, Solana RPC, Yellowstone gRPC, SDK libraries, and all endpoint schemas. Fetch on demand rather than embedding.

### Scripts
- `scripts/token_analysis.py` — Fetch token data, risk score, holders, and trades
- `scripts/wallet_pnl.py` — Wallet PnL analysis with win rate and trade breakdown

### Referencia: references/data_api_endpoints.md

# SolanaTracker Data API — Endpoints Reference

Base URL: `https://data.solanatracker.io`
Authentication: `x-api-key` header

---

## Token Endpoints

### Get Token Info
- **Endpoint**: `GET /tokens/{tokenAddress}`
- **Response**: Full token object with metadata, pools, risk, events, holder summary
- **Notes**: Most comprehensive single-call endpoint. Includes risk score, all pools, and recent events.

```bash
curl -H "x-api-key: $KEY" "https://data.solanatracker.io/tokens/So11111111111111111111111111111111111111112"
```

### Latest Tokens
- **Endpoint**: `GET /tokens/latest`
- **Parameters**: `page` (1-10)
- **Response**: Array of newly created tokens
- **Notes**: Useful for monitoring new launches. Updates frequently.

### Trending Tokens
- **Endpoint**: `GET /tokens/trending` or `GET /tokens/trending/{timeframe}`
- **Timeframes**: `5m`, `15m`, `30m`, `1h`, `4h`, `12h`, `24h`
- **Response**: Top 100 tokens by volume for the timeframe

### Graduated / Graduating
- **Endpoint**: `GET /tokens/graduated`, `GET /tokens/graduating`
- **Response**: Tokens that graduated from bonding curves (e.g., pump.fun → Raydium)
- **Notes**: Key signal for tokens transitioning to real liquidity pools.

### Multiple Tokens
- **Endpoint**: `GET /tokens/multi`
- **Parameters**: `tokens` — comma-separated addresses
- **Response**: Array of token objects

### Tokens by Deployer
- **Endpoint**: `GET /tokens/deployer/{deployerAddress}`
- **Response**: All tokens deployed by a specific wallet

---

## Price Endpoints

### Current Price
- **Endpoint**: `GET /price`
- **Parameters**: `token` (required), `priceChanges` (optional, boolean)
- **Response**: `{ price, liquidity, marketCap, priceChange5m, priceChange1h, ... }`

### Historic Prices
- **Endpoint**: `GET /price/history`
- **Parameters**: `token` (required)
- **Response**: Current price + snapshots at 3d, 5d, 7d, 14d, 30d intervals

### Price at Timestamp
- **Endpoint**: `GET /price/history/timestamp`
- **Parameters**: `token`, `timestamp` (unix seconds)

### Price Range
- **Endpoint**: `GET /price/history/range`
- **Parameters**: `token`, `time_from`, `time_to`
- **Response**: Lowest and highest price in the range

### Multi-Token Prices
- **Endpoint**: `GET /price/multi` (GET) or `POST /price/multi` (POST)
- **Parameters**: `tokens` — comma-separated addresses

---

## Chart / OHLCV Endpoints

### OHLCV Candles
- **Endpoint**: `GET /chart/{token}`
- **Parameters**:
  - `type` — Timeframe: `1s`, `5s`, `15s`, `1m`, `3m`, `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `6h`, `8h`, `12h`, `1d`, `3d`, `1w`, `1mn`
  - `time_from` — Start unix timestamp
  - `time_to` — End unix timestamp
  - `currency` — `usd` (default), `sol`, `eur`
  - `removeOutliers` — Boolean, filter anomalous candles
  - `marketCap` — Boolean, return market cap instead of price
  - `dynamicPools` — Boolean, aggregate across pools
  - `fastCache` — Boolean, use cache for faster response

```bash
curl -H "x-api-key: $KEY" \
  "https://data.solanatracker.io/chart/TOKEN?type=1m&time_from=1700000000&time_to=1700003600"
```

### Specialized Charts
- `GET /chart/{token}/bundlers` — Bundler activity overlay
- `GET /chart/{token}/holders` — Holder count overlay
- `GET /chart/{token}/insiders` — Insider activity overlay
- `GET /chart/{token}/snipers` — Sniper activity overlay

---

## PnL Endpoints

### Wallet PnL
- **Endpoint**: `GET /pnl/{wallet}`
- **Parameters**: `showHistoricPnL` (bool), `holdingCheck` (bool), `hideDetails` (bool)
- **Response**: Summary + per-token breakdown

```json
{
  "summary": {
    "realized": 1234.56,
    "unrealized": 567.89,
    "total": 1802.45,
    "totalInvested": 5000.00,
    "averageBuyAmount": 50.00,
    "totalWins": 42,
    "totalLosses": 18,
    "winPercentage": 70.0,
    "lossPercentage": 30.0
  },
  "tokens": [ /* per-token PnL details */ ]
}
```

### Token-Specific PnL
- **Endpoint**: `GET /pnl/{wallet}/{token}`
- **Response**: PnL for a specific token position

### First Buyers
- **Endpoint**: `GET /first-buyers/{token}`
- **Response**: First buyers of a token with full PnL data
- **Notes**: Useful for identifying early-entry wallets and their current P&L.

---

## Wallet Endpoints

### Wallet Holdings
- **Endpoint**: `GET /wallet/{owner}`
- **Response**: All tokens held with pool, risk, and event data

### Wallet Trades
- **Endpoint**: `GET /wallet/{owner}/trades`
- **Response**: Trade history with buy/sell amounts, prices, timestamps

### Portfolio Chart
- **Endpoint**: `GET /wallet/{owner}/chart`
- **Response**: Portfolio value over time

---

## Top Traders

### Global Top Traders
- **Endpoint**: `GET /top-traders/all` or `GET /top-traders/all/paginated?page=1`
- **Parameters**: `expandPnl` (bool), `sortBy` (`total` or `winPercentage`)

### Token Top Traders
- **Endpoint**: `GET /top-traders/{token}`
- **Parameters**: Same as global

---

## Holder Endpoints

### Paginated Holders
- **Endpoint**: `GET /tokens/{token}/holders?page=1`

### Top Holders
- **Endpoint**: `GET /tokens/{token}/holders/top` — Top 100
- **Endpoint**: `GET /tokens/{token}/holders/top20` — Top 20

### Bundler Detection
- **Endpoint**: `GET /tokens/{token}/bundlers`
- **Response**: Wallets identified as bundlers (batch transaction senders)

---

## Search

- **Endpoint**: `GET /search`
- **Key parameters**: `query`, `symbol`, `minLiquidity`, `maxLiquidity`, `minMarketCap`, `maxMarketCap`, `minVolume`, `maxVolume`, `hasImage`, `hasSocials`, `minHolders`, `maxHolders`, `minRiskScore`, `freezeAuthority`, `mintAuthority`, `deployer`, `market`, `sortBy`, `sortOrder`, `limit` (max 500), `page`, `cursor`

```bash
curl -H "x-api-key: $KEY" \
  "https://data.solanatracker.io/search?minLiquidity=50000&minRiskScore=5&market=raydium&sortBy=volume&limit=20"
```

---

## Trade / Event Endpoints

### Token Trades
- `GET /trades/{token}` — All trades
- `GET /trades/{token}/{wallet}` — Wallet-specific trades
- `GET /trades/pool/{pool}` — Pool-specific trades

### Token Events
- `GET /events/{token}` — Price change events by timeframe
- `GET /events/pool/{pool}` — Pool-specific events

---

## Account Management

- `GET /credits` — Remaining API credits
- `GET /subscription` — Current subscription info

### Referencia: references/raptor_setup.md

# Raptor DEX Aggregator — Setup & Deployment

Raptor is a self-hosted Rust binary by SolanaTracker that aggregates swap quotes across 25+ Solana DEXes. Free during public beta.

## Quick Start

```bash
# Clone the binary repo
git clone https://github.com/solanatracker/raptor-binary
cd raptor-binary

# Run with minimum required config
RPC_URL="https://your-solana-rpc.com" \
YELLOWSTONE_ENDPOINT="https://your-yellowstone-grpc.com" \
./raptor

# Default: listens on 0.0.0.0:8080
```

**Requirements**: Solana RPC endpoint + Yellowstone gRPC endpoint (for pool indexing and Jet TPU transaction submission) + signature file in the working directory.

## Signature File

Raptor requires a `signature` file in the same directory where the binary runs. This file authenticates your instance with the SolanaTracker backend.

```bash
# The signature file must be present alongside the raptor binary
ls raptor-binary/
# raptor          ← the binary
# signature       ← required auth file (provided by SolanaTracker)

# If you move the binary, copy the signature file too
cp raptor /opt/raptor/
cp signature /opt/raptor/
cd /opt/raptor && ./raptor
```

Without the signature file, Raptor will fail to start or fail to submit transactions. The file is included in the `raptor-binary` repo clone.

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `RPC_URL` | Yes | — | Solana RPC endpoint |
| `YELLOWSTONE_ENDPOINT` | Yes | — | Yellowstone gRPC endpoint |
| `BIND_ADDR` | No | `0.0.0.0:8080` | Listen address |
| `INCLUDE_DEXES` | No | All | Comma-separated DEX filter |
| `SKIP_POOL_INDEXER_WAIT` | No | false | Skip initial pool index sync |

## Execution Flow

```
1. GET /quote → Best route across DEXes
2. POST /swap → Unsigned transaction
3. Sign transaction locally (your key, never sent to Raptor)
4. POST /send-transaction → Submit via Yellowstone Jet TPU
5. GET /transaction/{sig} → Confirm status
```

### Step 1: Get Quote

```python
import httpx

RAPTOR = "http://localhost:8080"

resp = httpx.get(f"{RAPTOR}/quote", params={
    "inputMint": "So11111111111111111111111111111111111111112",  # SOL
    "outputMint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",  # USDC
    "amount": 1_000_000_000,  # 1 SOL in lamports
    "slippageBps": 50,
})
quote = resp.json()
print(f"Output: {quote['amountOut']} lamports")
print(f"Price impact: {quote['priceImpact']}%")
print(f"Route: {len(quote['routePlan'])} hops")
```

### Step 2: Build Swap Transaction

```python
resp = httpx.post(f"{RAPTOR}/swap", json={
    "userPublicKey": "YOUR_WALLET_PUBKEY",
    "quoteResponse": quote,
    "wrapUnwrapSol": True,
    "txVersion": "v0",
    "priorityFee": "auto",
    "maxPriorityFee": 100_000,  # max priority fee in lamports
})
swap = resp.json()
# swap["swapTransaction"] is base64-encoded unsigned transaction
```

### Step 3: Sign Locally

```python
from solders.transaction import VersionedTransaction
from solders.keypair import Keypair
import base64

tx_bytes = base64.b64decode(swap["swapTransaction"])
tx = VersionedTransaction.from_bytes(tx_bytes)
keypair = Keypair.from_base58_string(os.getenv("PRIVATE_KEY"))
signed_tx = tx.sign([keypair])
signed_b64 = base64.b64encode(bytes(signed_tx)).decode()
```

### Step 4: Submit Transaction

```python
resp = httpx.post(f"{RAPTOR}/send-transaction", json={
    "transaction": signed_b64,
})
result = resp.json()
print(f"Signature: {result['signature']}")
# Raptor retries for up to 30 seconds or until confirmed
```

### Step 5: Check Status

```python
resp = httpx.get(f"{RAPTOR}/transaction/{result['signature']}")
status = resp.json()
# status: pending | confirmed | failed | expired
```

## DEX Filter Configuration

Limit which DEXes Raptor queries. Useful for targeting specific pool types:

```bash
# Only bonding curve DEXes
INCLUDE_DEXES="pumpfun,moonit,heaven,raydium-launchlab,meteora-curve" ./raptor

# Only major AMMs
INCLUDE_DEXES="raydium,orca,meteora" ./raptor
```

**All supported DEXes**: `raydium` (AMM/CLMM/CPMM), `meteora` (DLMM/Dynamic), `orca` (Whirlpool v1/v2), `pancakeswap`, `pumpfun`, `pumpswap`, `heaven`, `moonit`, `boopfun`, `humidifi`, `tessera`, `solfi`, `alphaq`, `zerofi`, `bisonfi`, `goonfi`, `fluxbeam`, and more.

## Deployment Options

### Bare Metal / VPS

```bash
# Ensure signature file is in the same directory as the binary
ls ./raptor ./signature  # both must exist
chmod +x raptor
RPC_URL="..." YELLOWSTONE_ENDPOINT="..." ./raptor
```

### Docker

```dockerfile
FROM ubuntu:22.04
COPY raptor /usr/local/bin/raptor
COPY signature /usr/local/bin/signature
RUN chmod +x /usr/local/bin/raptor
WORKDIR /usr/local/bin
CMD ["raptor"]
```

```bash
docker run -e RPC_URL="..." -e YELLOWSTONE_ENDPOINT="..." -p 8080:8080 raptor
```

### Fly.io

```toml
# fly.toml
app = "my-raptor"
primary_region = "ewr"  # East US for low latency

[build]
  dockerfile = "Dockerfile"

[env]
  RPC_URL = "https://your-rpc.com"
  YELLOWSTONE_ENDPOINT = "https://your-yellowstone.com"
  INCLUDE_DEXES = "raydium,orca,meteora,pumpfun"

[[services]]
  internal_port = 8080
  protocol = "tcp"
  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]

[[vm]]
  size = "shared-cpu-2x"
  memory = "4gb"
```

```bash
fly deploy
```

## Key Differences from Jupiter

1. **Self-hosted**: Runs on your infrastructure, no external API dependency
2. **No rate limits**: Limited only by your hardware
3. **Separate on-chain program**: Uses `RaptorD5o...` program, not Jupiter's
4. **Jet TPU submission**: Transactions submitted via Yellowstone, not standard RPC
5. **Private key stays local**: Signing happens on your machine, never sent to Raptor
6. **DEX filtering**: Choose exactly which DEXes to include

## Troubleshooting

- **Slow startup**: Initial pool indexing can take 1-2 minutes. Use `SKIP_POOL_INDEXER_WAIT=true` to serve requests during indexing (quotes may be incomplete).
- **Quote returns 0 output**: Token may not have liquidity on any included DEX. Check `INCLUDE_DEXES` filter.
- **Transaction fails**: Check slippage, priority fee, and block height. Raptor retries automatically for 30 seconds.
- **Health check fails**: Verify RPC and Yellowstone endpoints are reachable.

### Referencia: references/risk_and_pnl.md

# SolanaTracker — Risk Scoring & PnL Calculation

## Risk Score

SolanaTracker assigns each token a risk score from **1 (highest risk) to 10 (safest)**, evaluating multiple on-chain and metadata factors.

### Risk Factors Evaluated

| Factor | Level | Description |
|--------|-------|-------------|
| Mint authority enabled | `danger` | Token supply can be increased |
| Freeze authority enabled | `danger` | Tokens can be frozen in wallets |
| Top 10 holders own >50% | `warn` | High concentration risk |
| Top 10 holders own >80% | `danger` | Extreme concentration |
| Low holder count (<100) | `warn` | Limited distribution |
| No social media links | `warn` | Possible low-effort token |
| Incomplete metadata | `warn` | Missing name, symbol, or image |
| Bundler activity detected | `warn` | Coordinated buy patterns |
| High sniper concentration | `warn` | Early buyers hold large % |
| Developer holds >10% | `warn` | Creator retention risk |
| Low liquidity (<$10K) | `danger` | Difficult to exit |
| Not Jupiter verified | `info` | Not vetted by Jupiter |

### Risk Response Schema

```json
{
  "risk": {
    "score": 7,
    "rugged": false,
    "jupiterVerified": true,
    "risks": [
      {
        "name": "Top 10 holders own 45%",
        "description": "High holder concentration",
        "level": "warn",
        "score": -1
      },
      {
        "name": "Freeze authority enabled",
        "description": "Token accounts can be frozen",
        "level": "danger",
        "score": -2
      }
    ]
  }
}
```

### Using Risk Scores

```python
def assess_risk(token_data: dict) -> str:
    """Classify token risk level from SolanaTracker data."""
    risk = token_data.get("risk", {})
    score = risk.get("score", 0)
    rugged = risk.get("rugged", False)

    if rugged:
        return "RUGGED — avoid"
    if score >= 8:
        return "LOW RISK"
    if score >= 5:
        return "MODERATE RISK"
    if score >= 3:
        return "HIGH RISK"
    return "EXTREME RISK"

def has_danger_flags(token_data: dict) -> list[str]:
    """Extract danger-level risk flags."""
    risks = token_data.get("risk", {}).get("risks", [])
    return [r["name"] for r in risks if r.get("level") == "danger"]
```

## PnL Calculation

SolanaTracker tracks realized and unrealized PnL per wallet across all Solana tokens.

### PnL Summary Fields

| Field | Type | Description |
|-------|------|-------------|
| `realized` | float | Profit/loss from closed positions (SOL) |
| `unrealized` | float | Open position value vs. cost basis (SOL) |
| `total` | float | realized + unrealized |
| `totalInvested` | float | Total SOL spent on buys |
| `averageBuyAmount` | float | Mean buy transaction size |
| `totalWins` | int | Positions closed in profit |
| `totalLosses` | int | Positions closed at a loss |
| `winPercentage` | float | Win rate (0-100) |
| `lossPercentage` | float | Loss rate (0-100) |

### Token-Level PnL

Each token in the breakdown includes:

| Field | Type | Description |
|-------|------|-------------|
| `tokenAddress` | string | Token mint |
| `totalBought` | float | Total tokens bought |
| `totalSold` | float | Total tokens sold |
| `totalBuyValue` | float | Total SOL spent buying |
| `totalSellValue` | float | Total SOL received selling |
| `realized` | float | Sell value - buy value for sold tokens |
| `unrealized` | float | Current value of held tokens - cost basis |
| `holdingAmount` | float | Currently held tokens |
| `holdingValue` | float | Current value of holdings |

### PnL Analysis Patterns

```python
def classify_trader(pnl_summary: dict) -> str:
    """Classify trader skill level from PnL data."""
    win_pct = pnl_summary.get("winPercentage", 0)
    total = pnl_summary.get("total", 0)
    invested = pnl_summary.get("totalInvested", 0)
    trades = pnl_summary.get("totalWins", 0) + pnl_summary.get("totalLosses", 0)

    if trades < 10:
        return "INSUFFICIENT DATA"

    roi = total / invested if invested > 0 else 0

    if win_pct >= 60 and roi > 0.5:
        return "STRONG PERFORMER"
    if win_pct >= 50 and roi > 0:
        return "PROFITABLE"
    if win_pct >= 40:
        return "MARGINAL"
    return "UNPROFITABLE"
```

### Historical PnL

With `showHistoricPnL=true`, the response includes:
- `pnl_1d` — Last 24 hours
- `pnl_7d` — Last 7 days
- `pnl_30d` — Last 30 days

Each interval has the same summary structure, enabling trend analysis:

```python
def pnl_trend(pnl: dict) -> str:
    """Check if trader is improving or declining."""
    d1 = pnl.get("pnl_1d", {}).get("total", 0)
    d7 = pnl.get("pnl_7d", {}).get("total", 0)
    d30 = pnl.get("pnl_30d", {}).get("total", 0)

    if d1 > 0 and d7 > 0 and d30 > 0:
        return "CONSISTENTLY PROFITABLE"
    if d1 > 0 and d7 > 0:
        return "RECENTLY PROFITABLE"
    if d1 < 0 and d7 < 0:
        return "DECLINING"
    return "MIXED"
```

## First Buyers Analysis

The `/first-buyers/{token}` endpoint combines early entry detection with PnL:

```python
def analyze_first_buyers(token: str, api_key: str) -> dict:
    """Analyze first buyers and their outcomes."""
    resp = httpx.get(
        f"https://data.solanatracker.io/first-buyers/{token}",
        headers={"x-api-key": api_key},
    )
    buyers = resp.json()

    profitable = sum(1 for b in buyers if b.get("realized", 0) > 0)
    total = len(buyers)

    return {
        "total_first_buyers": total,
        "profitable_count": profitable,
        "profitable_pct": round(profitable / total * 100, 1) if total > 0 else 0,
        "still_holding": sum(1 for b in buyers if b.get("holdingAmount", 0) > 0),
        "total_realized": sum(b.get("realized", 0) for b in buyers),
    }
```

## Bundler Detection

Bundlers are wallets that use atomic bundles to execute coordinated buys (often at launch). The `/tokens/{token}/bundlers` endpoint identifies these:

```json
[
  {
    "wallet": "ADDR...",
    "bundleCount": 5,
    "totalBought": 15000000,
    "holdingAmount": 12000000,
    "holdingPercentage": 2.4
  }
]
```

High bundler concentration at launch is a risk signal — it suggests coordinated buying that may precede a dump.


---

## SKILL: token-holder-analysis

- Fuente: `agiprolabs/claude-trading-skills` → `skills/token-holder-analysis` (MIT)
- Cuándo usarla: Token holder distribution, concentration metrics, insider detection, and supply analysis for Solana tokens
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/token-holder-analysis/` (analyze_holders.py, concentration_scanner.py)

# Token Holder Analysis — Concentration, Distribution & Risk

Analyze who holds a token, how concentrated ownership is, and whether insider patterns suggest risk. This is a critical pre-trade safety check — high concentration means a few wallets can crash the price.

## Quick Start

```python
import httpx
import math

# Using Helius DAS API for holder data
HELIUS_KEY = os.getenv("HELIUS_API_KEY", "")
HELIUS = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_KEY}"

# Or using SolanaTracker for holder + risk data
ST_KEY = os.getenv("SOLANATRACKER_API_KEY", "")
ST = "https://data.solanatracker.io"

# Get top holders via RPC
def get_top_holders(mint: str) -> list[dict]:
    resp = httpx.post(HELIUS, json={
        "jsonrpc": "2.0", "id": 1,
        "method": "getTokenLargestAccounts",
        "params": [mint],
    })
    return resp.json()["result"]["value"]

holders = get_top_holders("TOKEN_MINT")
```

## Data Sources

| Source | What It Provides | Auth |
|--------|-----------------|------|
| **Solana RPC** (`getTokenLargestAccounts`) | Top 20 holders, supply | RPC key |
| **Helius DAS** (`getAsset`, token accounts) | Parsed holder data, metadata | API key |
| **SolanaTracker** (`/tokens/{t}/holders/top`) | Top 100 holders, bundler detection | API key |
| **Birdeye** (`/defi/token_security`) | Top 10 %, creator balance, freeze/mint auth | API key |

## Concentration Metrics

### Top-N Holder Percentage

The simplest measure — what % of supply do the top N holders control?

```python
def top_n_percentage(holders: list[dict], supply: int, n: int = 10) -> float:
    """Calculate percentage held by top N holders.

    Args:
        holders: Sorted list of holders (largest first).
        supply: Total token supply.
        n: Number of top holders.

    Returns:
        Percentage (0-100) held by top N.
    """
    top_n_amount = sum(int(h.get("amount", 0)) for h in holders[:n])
    return top_n_amount / supply * 100 if supply > 0 else 0
```

**Risk thresholds**:
- Top 10 < 30%: Well distributed
- Top 10 30-50%: Moderate concentration
- Top 10 50-80%: High concentration — significant dump risk
- Top 10 > 80%: Extreme — likely controlled by a few wallets

### Gini Coefficient

Measures inequality of token distribution (0 = perfectly equal, 1 = one holder owns everything).

```python
def gini_coefficient(amounts: list[float]) -> float:
    """Calculate Gini coefficient for holder distribution.

    Args:
        amounts: List of holder amounts (any order).

    Returns:
        Gini coefficient between 0 and 1.
    """
    if not amounts or all(a == 0 for a in amounts):
        return 0.0
    sorted_amounts = sorted(amounts)
    n = len(sorted_amounts)
    cumsum = sum((i + 1) * a for i, a in enumerate(sorted_amounts))
    total = sum(sorted_amounts)
    return (2 * cumsum) / (n * total) - (n + 1) / n
```

**Interpretation for crypto tokens**:
- Gini < 0.6: Unusual, very well distributed
- Gini 0.6-0.8: Typical for established tokens
- Gini 0.8-0.95: Common for newer tokens
- Gini > 0.95: Extreme concentration, high risk

### Herfindahl-Hirschman Index (HHI)

Measures market concentration — sum of squared market shares.

```python
def hhi(amounts: list[float]) -> float:
    """Calculate HHI for holder concentration.

    Args:
        amounts: List of holder amounts.

    Returns:
        HHI value (0-10000). Higher = more concentrated.
    """
    total = sum(amounts)
    if total == 0:
        return 0.0
    shares = [a / total * 100 for a in amounts]
    return sum(s ** 2 for s in shares)
```

**Interpretation**:
- HHI < 1500: Competitive (unconcentrated)
- HHI 1500-2500: Moderately concentrated
- HHI > 2500: Highly concentrated

### Nakamoto Coefficient

Minimum number of holders needed to control >50% of supply.

```python
def nakamoto_coefficient(amounts: list[float]) -> int:
    """Calculate Nakamoto coefficient (holders needed for 51%).

    Args:
        amounts: Sorted list of holder amounts (largest first).

    Returns:
        Number of holders needed for majority control.
    """
    total = sum(amounts)
    if total == 0:
        return 0
    threshold = total * 0.51
    cumulative = 0
    for i, amount in enumerate(sorted(amounts, reverse=True)):
        cumulative += amount
        if cumulative >= threshold:
            return i + 1
    return len(amounts)
```

## Insider Detection Patterns

### Bundler Detection

Bundlers use atomic transaction bundles (via Jito) to execute coordinated buys at token launch. Detection signals:

```python
def detect_bundler_patterns(holders: list[dict], first_buyers: list[dict]) -> dict:
    """Identify potential bundler activity.

    Args:
        holders: Current top holders.
        first_buyers: Early buyers from SolanaTracker /first-buyers endpoint.

    Returns:
        Bundler risk analysis.
    """
    early_still_holding = [
        b for b in first_buyers
        if b.get("holdingAmount", 0) > 0
    ]
    early_holder_pct = sum(
        b.get("holdingPercentage", 0) for b in early_still_holding
    )

    return {
        "early_buyers_count": len(first_buyers),
        "still_holding_count": len(early_still_holding),
        "early_holder_pct": round(early_holder_pct, 2),
        "risk": "HIGH" if early_holder_pct > 20 else
                "MODERATE" if early_holder_pct > 10 else "LOW",
    }
```

### Developer Holdings

Creator wallet retention is a risk signal:

```python
def check_developer_risk(token_data: dict) -> dict:
    """Check developer wallet holdings and authority.

    Args:
        token_data: Token info from SolanaTracker or Birdeye.

    Returns:
        Developer risk assessment.
    """
    risk = token_data.get("risk", {})
    flags = []

    # Check creator balance (from Birdeye security endpoint)
    creator_balance = token_data.get("creatorBalance", 0)
    if creator_balance > 10:
        flags.append(f"Creator holds {creator_balance:.1f}% of supply")

    # Check mint authority
    if token_data.get("mintAuthority") or token_data.get("ownerAddress"):
        flags.append("Mint authority NOT renounced — supply can increase")

    # Check freeze authority
    if token_data.get("freezeAuthority") or token_data.get("freezeable"):
        flags.append("Freeze authority enabled — tokens can be frozen")

    return {
        "flags": flags,
        "risk_level": "HIGH" if len(flags) >= 2 else
                      "MODERATE" if len(flags) == 1 else "LOW",
    }
```

### Sniper Detection

Snipers buy in the first few seconds/blocks after token creation:

```python
def analyze_sniper_concentration(first_buyers: list[dict], total_supply: float) -> dict:
    """Analyze sniper impact on holder distribution.

    Args:
        first_buyers: First buyers data from SolanaTracker.
        total_supply: Total token supply.

    Returns:
        Sniper concentration analysis.
    """
    # Snipers typically buy in first 10 seconds
    snipers = first_buyers[:10]  # first N buyers are potential snipers
    sniper_holding = sum(b.get("holdingAmount", 0) for b in snipers)
    sniper_pct = sniper_holding / total_supply * 100 if total_supply > 0 else 0

    return {
        "sniper_count": len(snipers),
        "sniper_holding_pct": round(sniper_pct, 2),
        "sniper_still_holding": sum(1 for s in snipers if s.get("holdingAmount", 0) > 0),
        "risk": "HIGH" if sniper_pct > 15 else
                "MODERATE" if sniper_pct > 5 else "LOW",
    }
```

## Complete Analysis Pipeline

```python
def full_holder_analysis(mint: str) -> dict:
    """Run complete holder analysis for a token.

    Combines RPC, SolanaTracker, and computed metrics.
    """
    # 1. Get supply and top holders via RPC
    supply_result = rpc_call("getTokenSupply", [mint])
    total_supply = int(supply_result["result"]["value"]["amount"])

    holders = get_top_holders(mint)
    amounts = [int(h["amount"]) for h in holders]

    # 2. Compute concentration metrics
    metrics = {
        "total_supply": total_supply,
        "holder_count": len(holders),
        "top_1_pct": top_n_percentage(holders, total_supply, 1),
        "top_5_pct": top_n_percentage(holders, total_supply, 5),
        "top_10_pct": top_n_percentage(holders, total_supply, 10),
        "top_20_pct": top_n_percentage(holders, total_supply, 20),
        "gini": round(gini_coefficient(amounts), 4),
        "hhi": round(hhi(amounts), 1),
        "nakamoto": nakamoto_coefficient(amounts),
    }

    # 3. Risk classification
    t10 = metrics["top_10_pct"]
    if t10 > 80:
        metrics["risk"] = "EXTREME"
    elif t10 > 50:
        metrics["risk"] = "HIGH"
    elif t10 > 30:
        metrics["risk"] = "MODERATE"
    else:
        metrics["risk"] = "LOW"

    return metrics
```

## Risk Classification Summary

| Metric | Low Risk | Moderate | High | Extreme |
|--------|----------|----------|------|---------|
| Top 10 % | <30% | 30-50% | 50-80% | >80% |
| Gini | <0.7 | 0.7-0.85 | 0.85-0.95 | >0.95 |
| HHI | <1500 | 1500-2500 | 2500-5000 | >5000 |
| Nakamoto | >10 | 5-10 | 2-4 | 1 |
| Mint Auth | Renounced | — | Active | Active + high dev % |
| Freeze Auth | Disabled | — | Enabled | Enabled + low liq |

## Known Exclusions

When computing holder concentration, exclude these addresses which are programs/pools, not individual holders:

- DEX pool addresses (Raydium, Orca, Meteora pools)
- Token program vaults
- Bridge escrow accounts
- Known burn addresses

```python
KNOWN_PROGRAMS = {
    "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1",  # Raydium authority
    "GThUX1Atko4tqhN2NaiTazWSeFWMuiUvfFnyJyUghFMJ",  # Orca authority
    # Add more as needed
}

def filter_real_holders(holders: list[dict]) -> list[dict]:
    """Remove known program/pool accounts from holder list."""
    return [h for h in holders if h.get("address") not in KNOWN_PROGRAMS]
```

## Files

### References
- `references/concentration_metrics.md` — Mathematical formulas and derivations for Gini, HHI, Nakamoto
- `references/insider_patterns.md` — Bundler, sniper, and developer detection methodology
- `references/data_sources.md` — How to fetch holder data from each API source

### Scripts
- `scripts/analyze_holders.py` — Full holder analysis: fetch holders, compute metrics, generate risk report
- `scripts/concentration_scanner.py` — Scan multiple tokens for concentration risk

### Referencia: references/concentration_metrics.md

# Concentration Metrics — Formulas & Interpretation

## Top-N Holder Percentage

The simplest concentration measure. Sums the holdings of the N largest holders as a percentage of total supply.

**Formula**:
```
Top_N% = (Σ holdings[i] for i=1..N) / total_supply × 100
```

**Thresholds for Solana tokens**:

| Top 10 % | Risk Level | Interpretation |
|----------|------------|----------------|
| < 20% | Very Low | Exceptionally well distributed |
| 20-30% | Low | Good distribution |
| 30-50% | Moderate | Typical for mid-cap tokens |
| 50-80% | High | Significant dump risk |
| > 80% | Extreme | Likely controlled by a few actors |

**Important**: Always exclude known program accounts (DEX pools, bridge escrows, burn addresses) from holder counts. Including pool liquidity as a "holder" skews the metric.

---

## Gini Coefficient

Measures inequality of distribution. Originally from economics (income inequality), applied here to token holdings.

**Formula**:
```
G = (2 × Σ(i × x_i)) / (n × Σ(x_i)) - (n + 1) / n

where x_i are amounts sorted ascending, i is 1-indexed position, n is holder count
```

**Equivalent formula** (via mean absolute difference):
```
G = Σ_i Σ_j |x_i - x_j| / (2 × n² × μ)

where μ is the mean holding
```

**Range**: 0 to 1
- 0 = perfectly equal (every holder has the same amount)
- 1 = maximally unequal (one holder owns everything)

**Crypto-specific thresholds**:

| Gini | Interpretation |
|------|---------------|
| < 0.5 | Rare — very egalitarian distribution |
| 0.5-0.7 | Well distributed for crypto |
| 0.7-0.85 | Typical for established tokens |
| 0.85-0.95 | Common for newer/smaller tokens |
| > 0.95 | Extreme concentration |

**Limitations**:
- Gini is sensitive to the number of holders included. Computing over top 20 holders (RPC limit) vs. all holders gives different values.
- For meaningful comparison, always compute over the same sample size.
- Gini doesn't distinguish between distributions with the same inequality but different shapes (e.g., one whale vs. several large holders).

---

## Herfindahl-Hirschman Index (HHI)

Sum of squared market shares. Originally used for antitrust analysis (market concentration). More sensitive to large holders than Gini.

**Formula**:
```
HHI = Σ(s_i²)

where s_i = (holding_i / total_supply) × 100  (percentage share)
```

**Range**: 0 to 10,000
- Minimum (n equal holders): HHI = 10000/n
- Maximum (one holder): HHI = 10,000

**Thresholds** (adapted from DOJ antitrust guidelines):

| HHI | Interpretation |
|-----|---------------|
| < 1,500 | Unconcentrated (competitive) |
| 1,500-2,500 | Moderately concentrated |
| 2,500-5,000 | Highly concentrated |
| > 5,000 | Extremely concentrated |

**Advantage over Gini**: HHI is more sensitive to the presence of dominant holders. A distribution with one 50% holder and many small holders will have a much higher HHI than a distribution with several 10% holders, even if both have similar Gini values.

---

## Nakamoto Coefficient

Minimum number of entities needed to control >50% of the system. Named after Satoshi Nakamoto.

**Formula**:
```
N = min k such that Σ(holding_i for top k holders) > 0.51 × total_supply
```

**Interpretation**:

| Nakamoto | Meaning |
|----------|---------|
| 1 | Single entity controls majority — maximum centralization |
| 2-3 | Small cartel can control the token |
| 4-10 | Moderate decentralization |
| > 10 | Good decentralization |

**Notes**:
- Lower bound for Nakamoto is 1. If the largest holder owns >50%, Nakamoto = 1.
- The 51% threshold can be adjusted (e.g., 33% for tokens where 1/3 can block governance).
- Nakamoto coefficient is particularly useful for governance tokens where voting power matters.

---

## Shannon Entropy

Information-theoretic measure of distribution randomness. Not commonly used but provides additional perspective.

**Formula**:
```
H = -Σ(p_i × log2(p_i))

where p_i = holding_i / total_supply
```

**Range**: 0 to log2(n)
- 0 = one holder owns everything
- log2(n) = perfectly equal distribution

Higher entropy = more decentralized.

---

## Combining Metrics

No single metric tells the full story. Use them together:

```python
def comprehensive_risk(top_10_pct, gini, hhi, nakamoto):
    """Combine metrics into a single risk score."""
    scores = {
        "top10": 3 if top_10_pct > 80 else 2 if top_10_pct > 50 else 1 if top_10_pct > 30 else 0,
        "gini": 3 if gini > 0.95 else 2 if gini > 0.85 else 1 if gini > 0.7 else 0,
        "hhi": 3 if hhi > 5000 else 2 if hhi > 2500 else 1 if hhi > 1500 else 0,
        "nakamoto": 3 if nakamoto <= 1 else 2 if nakamoto <= 3 else 1 if nakamoto <= 5 else 0,
    }
    total = sum(scores.values())
    if total >= 9: return "EXTREME"
    if total >= 6: return "HIGH"
    if total >= 3: return "MODERATE"
    return "LOW"
```

### Referencia: references/data_sources.md

# Holder Analysis — Data Sources

## Source Comparison

| Data Point | Solana RPC | Helius DAS | SolanaTracker | Birdeye |
|-----------|-----------|------------|---------------|---------|
| Top holders | Top 20 | Via token accts | Top 100 | Top 10 % |
| Total supply | Yes | Yes | Yes | Partial |
| Holder count | No | No | Yes | No |
| Mint authority | Via getAccountInfo | Via getAsset | In risk score | Yes |
| Freeze authority | Via getAccountInfo | Via getAsset | In risk score | Yes |
| Creator balance | No | No | Yes | Yes |
| Bundler detection | No | No | Yes | No |
| Sniper detection | No | No | Yes | No |
| Risk score | No | No | Yes (1-10) | Partial |
| Auth required | RPC key | API key | API key | API key |
| Cost | Free (public) | 50K/day free | €50/mo | Free tier |

## Method 1: Solana RPC (Free, Basic)

Best for: Quick top-20 check, total supply, mint/freeze authority status.

```python
# Top 20 holders
result = rpc_call("getTokenLargestAccounts", [mint])
holders = result["value"]  # [{address, amount, decimals, uiAmount}]

# Total supply
result = rpc_call("getTokenSupply", [mint])
supply = result["value"]  # {amount, decimals, uiAmount}

# Mint/freeze authority (from mint account data)
result = rpc_call("getAccountInfo", [mint, {"encoding": "jsonParsed"}])
mint_info = result["value"]["data"]["parsed"]["info"]
# mint_info["mintAuthority"] — None if renounced
# mint_info["freezeAuthority"] — None if disabled
```

**Limitations**: Only top 20 holders. No holder count. No insider detection.

## Method 2: Helius DAS API

Best for: Token metadata, parsed account data, fungible token details.

```python
# Token metadata via DAS
resp = httpx.post(f"https://mainnet.helius-rpc.com/?api-key={KEY}", json={
    "jsonrpc": "2.0", "id": 1,
    "method": "getAsset",
    "params": {"id": mint},
})
asset = resp.json()["result"]
# asset["authorities"] — mint/freeze authority info
# asset["token_info"]["supply"] — total supply
# asset["content"]["metadata"] — name, symbol, image
```

**Limitations**: Doesn't directly provide holder lists. Use with RPC for complete picture.

## Method 3: SolanaTracker API (Most Complete)

Best for: Full holder analysis including bundlers, snipers, risk scoring.

```python
HEADERS = {"x-api-key": ST_KEY}

# Top 100 holders
resp = httpx.get(f"https://data.solanatracker.io/tokens/{mint}/holders/top", headers=HEADERS)
holders = resp.json()

# Top 20 (lighter call)
resp = httpx.get(f"https://data.solanatracker.io/tokens/{mint}/holders/top20", headers=HEADERS)

# Bundler detection
resp = httpx.get(f"https://data.solanatracker.io/tokens/{mint}/bundlers", headers=HEADERS)
bundlers = resp.json()

# First buyers with PnL
resp = httpx.get(f"https://data.solanatracker.io/first-buyers/{mint}", headers=HEADERS)
first_buyers = resp.json()

# Full token info with risk score
resp = httpx.get(f"https://data.solanatracker.io/tokens/{mint}", headers=HEADERS)
token = resp.json()
risk_score = token["risk"]["score"]  # 1-10
```

## Method 4: Birdeye API

Best for: Quick security check (mint/freeze authority, top 10 concentration).

```python
# Token security info
resp = httpx.get("https://public-api.birdeye.so/defi/token_security",
    headers={"X-API-KEY": BE_KEY, "x-chain": "solana"},
    params={"address": mint})
security = resp.json()["data"]
# security["top10HolderPercent"]
# security["ownerAddress"] — mint authority (None if renounced)
# security["freezeable"]
# security["mutableMetadata"]
# security["creatorBalance"]
```

## Recommended Pipeline

For a thorough pre-trade holder analysis:

```python
def full_holder_check(mint: str) -> dict:
    """Complete holder analysis using best available data sources."""

    # 1. Quick check via RPC (free, always available)
    supply = get_token_supply(mint)
    top_20 = get_largest_accounts(mint)

    # 2. Risk score from SolanaTracker (if key available)
    if ST_KEY:
        token_data = st_get(f"/tokens/{mint}")
        risk_score = token_data.get("risk", {}).get("score", 0)
        bundlers = st_get(f"/tokens/{mint}/bundlers")

    # 3. Security check from Birdeye (if key available)
    if BE_KEY:
        security = birdeye_get("/defi/token_security", {"address": mint})

    # 4. Compute concentration metrics from RPC data
    amounts = [int(h["amount"]) for h in top_20]
    metrics = compute_concentration(amounts, int(supply["amount"]))

    return {
        "supply": supply,
        "top_holders": top_20,
        "concentration": metrics,
        "risk_score": risk_score,
        "bundlers": bundlers,
        "security": security,
    }
```

## Caching Considerations

Holder data changes slowly compared to price data. Reasonable cache TTLs:

| Data | Cache TTL | Reason |
|------|-----------|--------|
| Top holders | 5-15 minutes | Positions change via trades |
| Total supply | 1 hour | Rarely changes (unless mintable) |
| Mint/freeze authority | 1 hour | Almost never changes |
| Risk score | 15-30 minutes | Recalculated periodically |
| Bundler data | 1 hour | Historical, doesn't change |

### Referencia: references/insider_patterns.md

# Insider Detection Patterns

## Overview

"Insider" in Solana token trading refers to wallets that have an unfair advantage — they bought before public availability, used transaction bundles for guaranteed early execution, or are connected to the token creator. Detecting these patterns is a critical pre-trade safety check.

## Pattern 1: Bundler Detection

### What is bundling?
Bundlers use Jito or similar services to submit multiple transactions atomically in a single block. This guarantees execution order, allowing coordinated buys at token launch.

### Detection signals
1. **Multiple buys in the same block/slot as token creation**
2. **Multiple wallets buying the exact same amount** in the first slots
3. **Wallets that share funding sources** (funded from the same parent wallet)
4. **High holding percentage from first-block buyers**

### Data sources
- **SolanaTracker** `/tokens/{token}/bundlers` — pre-computed bundler detection
- **SolanaTracker** `/first-buyers/{token}` — first buyers with PnL
- **Helius** Enhanced Transactions — parse early transactions for patterns

### Risk interpretation

| Bundler Holding % | Risk |
|-------------------|------|
| < 5% | Low — bundlers exited or hold small amounts |
| 5-15% | Moderate — some coordinated buying |
| 15-30% | High — significant coordinated control |
| > 30% | Extreme — likely orchestrated launch |

## Pattern 2: Sniper Detection

### What is sniping?
Snipers use automated bots to buy tokens within the first few seconds of liquidity being added. They achieve near-zero entry prices on bonding curves or DEX launches.

### Detection signals
1. **Buy transactions within first 1-10 seconds** of pool creation
2. **Wallet has many "first buy" patterns** across different tokens
3. **Bot-like transaction patterns** (fixed amounts, consistent timing)
4. **Currently holding large % of supply** from initial snipe

### Analysis approach
```python
def is_sniper_wallet(wallet_trades: list[dict], token_created_at: int) -> bool:
    """Check if wallet sniped the token launch."""
    first_buy = next(
        (t for t in wallet_trades if t["type"] == "buy"),
        None
    )
    if first_buy is None:
        return False
    # Bought within 10 seconds of creation
    return first_buy["timestamp"] - token_created_at < 10
```

## Pattern 3: Developer / Creator Analysis

### Risk factors
1. **Creator still holds tokens** — can dump at any time
2. **Mint authority not renounced** — creator can mint more tokens
3. **Freeze authority active** — creator can freeze token accounts
4. **Creator wallet funded by known rug accounts**
5. **Creator deployed multiple tokens** that failed (serial deployer)

### Data sources
- **Birdeye** `/defi/token_security` — mint authority, freeze authority, creator balance
- **SolanaTracker** `/tokens/{token}` — risk score includes these checks
- **SolanaTracker** `/tokens/deployer/{addr}` — all tokens by the same deployer
- **Direct RPC** — check mint account for authority fields

### Serial deployer detection
```python
def check_deployer_history(deployer: str, api_key: str) -> dict:
    """Check deployer's track record."""
    resp = httpx.get(
        f"https://data.solanatracker.io/tokens/deployer/{deployer}",
        headers={"x-api-key": api_key},
    )
    tokens = resp.json()

    rugged = sum(1 for t in tokens if t.get("risk", {}).get("rugged"))
    low_risk = sum(1 for t in tokens if t.get("risk", {}).get("score", 0) >= 7)

    return {
        "total_deployments": len(tokens),
        "rugged_count": rugged,
        "low_risk_count": low_risk,
        "serial_rug": rugged > 3,
    }
```

## Pattern 4: Connected Wallet Clusters

### What to look for
- Wallets funded from the same source around token launch
- Wallets that only ever trade the same tokens
- Wallets that buy and sell in coordinated timing patterns

### Analysis approach
This requires transaction history analysis:
1. For each top holder, trace their funding source (SOL origin)
2. Cluster wallets that share the same funding source
3. Flag clusters that collectively hold >10% of supply

```python
def trace_funding_source(wallet: str, depth: int = 2) -> list[str]:
    """Trace SOL funding sources for a wallet.

    Use Helius Enhanced Transactions to find incoming SOL transfers.
    Returns list of funding source addresses.
    """
    sources = []
    resp = httpx.get(
        f"https://api.helius.xyz/v0/addresses/{wallet}/transactions",
        params={"api-key": HELIUS_KEY, "type": "TRANSFER"},
    )
    for tx in resp.json()[:20]:
        for transfer in tx.get("nativeTransfers", []):
            if transfer.get("toUserAccount") == wallet:
                sources.append(transfer["fromUserAccount"])
    return sources
```

## Pattern 5: Wash Trading Detection

### Signals
- Same wallet appearing as both buyer and seller (self-trades)
- High volume but low unique wallet count
- Volume spikes with no corresponding price movement
- Buy/sell ratio extremely close to 1.0 across many time periods

### Quick check
```python
def wash_trading_check(pair_data: dict) -> dict:
    """Quick wash trading heuristic from DexScreener data."""
    txns = pair_data.get("txns", {}).get("h24", {})
    buys = txns.get("buys", 0)
    sells = txns.get("sells", 0)
    total = buys + sells

    volume = pair_data.get("volume", {}).get("h24", 0)
    liquidity = pair_data.get("liquidity", {}).get("usd", 0)

    flags = []
    if total > 0 and abs(buys - sells) / total < 0.05:
        flags.append("Buy/sell count suspiciously balanced")
    if liquidity > 0 and volume / liquidity > 50:
        flags.append(f"Volume/liquidity ratio extremely high ({volume/liquidity:.0f}x)")

    return {"flags": flags, "suspicious": len(flags) > 0}
```

## Combining Insider Signals

Weight multiple signals for a composite insider risk score:

| Signal | Weight | Max Score |
|--------|--------|-----------|
| Bundler holding > 15% | High | 3 |
| Sniper holding > 10% | High | 3 |
| Creator holds > 10% | Medium | 2 |
| Mint authority active | High | 3 |
| Freeze authority active | Medium | 2 |
| Serial deployer (3+ rugs) | Critical | 4 |
| Connected wallet cluster | Medium | 2 |
| Wash trading signals | Low | 1 |

Score 0-3: Low insider risk
Score 4-7: Moderate — proceed with caution
Score 8-12: High — small positions only
Score 13+: Extreme — avoid


---

## SKILL: wallet-profiling

- Fuente: `agiprolabs/claude-trading-skills` → `skills/wallet-profiling` (MIT)
- Cuándo usarla: Behavioral classification, performance analysis, and trading style detection for Solana wallets
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/wallet-profiling/` (compare_wallets.py, profile_wallet.py)

# Wallet Profiling

Behavioral classification, performance analysis, and trading style detection for Solana wallets. Profile any wallet to understand how it trades, how well it performs, and whether it is worth following.

## Why Wallet Profiling Matters

### Copy-Trade Evaluation
Before mirroring another wallet's trades, you need evidence that its historical performance is genuine, consistent, and not the result of a single lucky hit. Profiling quantifies win rate, profit factor, hold time, and consistency so you can make informed decisions about which wallets merit attention.

### Smart Money Identification
Wallets that consistently buy tokens early and exit profitably are signal sources. Profiling separates genuinely skilled traders from lucky gamblers and wash-trading bots. Key differentiators: sustained profit factor above 2.0, win rates above 45% across 100+ trades, and diversified token selection.

### Counterparty Analysis
When a large wallet enters a position you hold, understanding its historical behavior (sniper vs. holder, bot vs. human) helps you anticipate what will happen next. A sniper wallet buying suggests a quick dump is coming; a swing trader buying suggests multi-day conviction.

### Risk Assessment
Token holder analysis benefits from knowing whether top holders are bots, snipers, or genuine investors. A token where 60% of holders are classified as snipers has very different risk characteristics than one held primarily by swing traders.

## Wallet Classification

### By Trading Style

Classification is based on the **median hold time** across all closed trades:

| Style | Median Hold Time | Characteristics |
|-------|-----------------|-----------------|
| Sniper | < 5 minutes | First-block buyers, MEV-adjacent, extremely fast exits |
| Scalper | 5 min – 1 hour | Quick momentum trades, high frequency |
| Day Trader | 1 – 24 hours | Intraday positions, moderate frequency |
| Swing Trader | 1 – 7 days | Multi-day conviction holds |
| Position Holder | > 7 days | Long-term accumulation, low frequency |

See `references/classification_methods.md` for the full classification algorithm.

### By Trade Size

Based on **median trade size in SOL**:

| Tier | Median Trade Size | Typical Behavior |
|------|------------------|-----------------|
| Whale | > 100 SOL | Market-moving entries, often front-run |
| Large | 10 – 100 SOL | Significant but not dominant |
| Medium | 1 – 10 SOL | Active retail traders |
| Small | < 1 SOL | Micro-cap gamblers, new wallets |

### By Behavior Type

| Type | Detection Method |
|------|-----------------|
| Bot | Low inter-trade timing variance (CV < 0.3), uniform sizing |
| Human | Variable timing, variable sizing, session-based activity |
| MEV | Sandwich patterns, consistent small profits, high frequency |

### By Focus Area

| Focus | Detection Criteria |
|-------|-------------------|
| PumpFun Specialist | > 70% of trades on PumpFun-launched tokens |
| DEX Trader | Primarily swaps on Raydium/Orca/Meteora |
| DeFi Farmer | Frequent LP add/remove, staking operations |
| NFT Trader | Significant NFT marketplace interactions |
| Multi-Strategy | No single category exceeds 50% |

## Performance Metrics

### Core Metrics

**Win Rate** — Percentage of trades that are profitable.
```
win_rate = count(pnl > 0) / count(all_closed_trades)
```
Minimum 30 trades for statistical significance. A 60% win rate across 200 trades is far more meaningful than 80% across 10 trades.

**Average ROI Per Trade** — Mean return across all closed positions.
```
avg_roi = mean((exit_value - entry_value) / entry_value)
```
Include all fees: platform fees, priority fees, and estimated slippage.

**Profit Factor** — Ratio of gross profits to gross losses.
```
profit_factor = sum(winning_pnl) / abs(sum(losing_pnl))
```
Interpretation: > 2.0 excellent, 1.5–2.0 good, 1.0–1.5 marginal, < 1.0 losing.

**Total PnL** — Cumulative profit/loss in SOL.
```
total_pnl = sum(all_trade_pnl)
```

**Maximum Drawdown** — Largest peak-to-trough decline in cumulative PnL curve.
```
drawdown = (peak_equity - trough_equity) / peak_equity
```

**Sharpe-Like Ratio** — Risk-adjusted return metric.
```
sharpe = mean(trade_returns) / std(trade_returns) * sqrt(trades_per_year)
```

See `references/performance_metrics.md` for detailed formulas, edge cases, and interpretation guidelines.

### Activity Metrics

| Metric | Calculation | What It Reveals |
|--------|------------|-----------------|
| Trades per day | total_trades / active_days | Activity level and capacity |
| Average hold time | mean(exit_time - entry_time) | Trading style confirmation |
| Token diversity | unique_tokens / total_trades | Specialization vs. diversification |
| Peak hours | mode(hour_of_trade) | Session patterns, timezone hints |
| Activity streaks | consecutive active days | Dedication and consistency |

## Data Sources

### SolanaTracker PnL API (Primary)

The SolanaTracker API provides pre-computed PnL data per wallet per token.

```python
import httpx

url = f"https://data.solanatracker.io/pnl/{wallet_address}"
headers = {"x-api-key": os.getenv("ST_API_KEY")}
resp = httpx.get(url, headers=headers)
pnl_data = resp.json()
```

Response includes per-token: `realized`, `unrealized`, `total_invested`, `total_sold`, `num_buys`, `num_sells`, `last_trade_time`.

### Helius Parsed Transactions (Detailed)

For granular transaction-level analysis, use the `helius-api` skill to fetch parsed transaction history. This provides exact timestamps, amounts, and program interactions.

### Birdeye Trader Data

Birdeye's trader endpoints provide wallet-level analytics. See the `birdeye-api` skill for endpoint details.

### DexScreener (Free Fallback)

DexScreener does not provide wallet-level PnL but can be used to validate token prices at trade timestamps.

## Copy-Trade Evaluation Framework

Before following a wallet's trades, verify these criteria:

### Minimum Requirements
- **Trade history**: At least 50 closed trades (100+ preferred)
- **Time span**: Active for at least 30 days
- **Consistent performance**: Rolling 7-day win rate standard deviation < 15%
- **Reasonable sizing**: No single trade > 20% of observed portfolio
- **Diverse tokens**: At least 10 unique tokens traded

### Green Flags
- Profit factor > 1.8 sustained over 60+ days
- Win rate 45–65% (unrealistically high rates suggest wash trading)
- Moderate trade frequency (2–20 trades/day)
- Mixed hold times indicating adaptive strategy
- Gradual equity curve growth (not step-function jumps)

### Red Flags
- **New wallet** (< 14 days old): Possible sybil or one-hit-wonder
- **Single big win**: One trade accounts for > 50% of total PnL
- **Declining performance**: Last-30-day metrics significantly below all-time
- **Bot-like patterns**: Uniform timing/sizing without proportional edge
- **Extreme win rate**: > 80% often indicates small wins with catastrophic losses
- **Concentration**: > 50% of PnL from a single token
- **Wash trading signals**: Repeated buy/sell of same token with minimal price movement

### Risk Score Calculation

```python
risk_score = 0  # 0 = low risk, 100 = high risk

if wallet_age_days < 14:
    risk_score += 25
if top_trade_pnl_pct > 0.5:
    risk_score += 20
if recent_pf < historical_pf * 0.7:
    risk_score += 15
if bot_probability > 0.7:
    risk_score += 15
if win_rate > 0.8:
    risk_score += 10
if unique_tokens < 5:
    risk_score += 15
```

## Integration with Other Skills

- **`whale-tracking`**: Identify large wallets, then profile them here for behavioral context
- **`token-holder-analysis`**: Profile top holders of a token to assess holder quality
- **`solana-onchain`**: Fetch raw transaction data for deep-dive analysis
- **`helius-api`**: Parsed transaction history for granular trade reconstruction
- **`birdeye-api`**: Token price data for PnL validation

## Quick Start

### Profile a Single Wallet

```python
# Set environment variables
# export WALLET_ADDRESS=YourTargetWallet...
# export ST_API_KEY=your_solanatracker_key  (optional)

python scripts/profile_wallet.py
# Or use demo mode:
python scripts/profile_wallet.py --demo
```

### Compare Multiple Wallets

```python
# export WALLET_ADDRESSES=Wallet1...,Wallet2...,Wallet3...
# export ST_API_KEY=your_solanatracker_key  (optional)

python scripts/compare_wallets.py
# Or use demo mode:
python scripts/compare_wallets.py --demo
```

## Files

| File | Description |
|------|-------------|
| `references/classification_methods.md` | Hold time, size, bot detection, and focus classification algorithms |
| `references/performance_metrics.md` | Detailed metric formulas, interpretation, edge cases, and decay detection |
| `scripts/profile_wallet.py` | Profile a single wallet: fetch data, compute metrics, classify, report |
| `scripts/compare_wallets.py` | Compare multiple wallets side-by-side with ranking |

## Dependencies

```bash
uv pip install httpx
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `WALLET_ADDRESS` | For profile_wallet.py | Solana wallet address to profile |
| `WALLET_ADDRESSES` | For compare_wallets.py | Comma-separated wallet addresses |
| `ST_API_KEY` | No | SolanaTracker API key for PnL data |

### Referencia: references/classification_methods.md

# Wallet Classification Methods

Algorithms for categorizing Solana wallets by trading style, size, behavior type, and focus area.

## Style Classification (Hold Time)

Classify based on the **median hold time** of all closed trades. Use median rather than mean to avoid skew from forgotten positions.

### Algorithm

```python
def classify_style(hold_times_minutes: list[float]) -> str:
    """Classify wallet trading style from hold time distribution.

    Args:
        hold_times_minutes: List of hold durations in minutes for closed trades.

    Returns:
        Style label: sniper, scalper, day_trader, swing, or holder.
    """
    if not hold_times_minutes:
        return "unknown"

    import statistics
    median = statistics.median(hold_times_minutes)

    if median < 5:
        return "sniper"
    elif median < 60:
        return "scalper"
    elif median < 1440:       # 24 hours
        return "day_trader"
    elif median < 10080:      # 7 days
        return "swing"
    else:
        return "holder"
```

### Hold Time Distribution Analysis

Beyond the median, examine the full distribution shape:

| Distribution Shape | Interpretation |
|-------------------|----------------|
| Tight unimodal (low std) | Consistent strategy, single style |
| Bimodal | Two distinct strategies (e.g., scalp + swing) |
| Right-skewed | Primarily fast trades with occasional holds |
| Uniform/flat | No clear strategy, opportunistic |

```python
def analyze_hold_distribution(hold_times: list[float]) -> dict:
    """Analyze the shape of hold time distribution."""
    import statistics
    if len(hold_times) < 5:
        return {"shape": "insufficient_data"}

    median = statistics.median(hold_times)
    mean = statistics.mean(hold_times)
    stdev = statistics.stdev(hold_times)
    cv = stdev / mean if mean > 0 else 0

    return {
        "median_minutes": round(median, 1),
        "mean_minutes": round(mean, 1),
        "stdev_minutes": round(stdev, 1),
        "cv": round(cv, 2),
        "skew_direction": "right" if mean > median * 1.5 else "left" if mean < median * 0.67 else "symmetric",
        "consistency": "high" if cv < 0.5 else "medium" if cv < 1.0 else "low",
    }
```

## Size Classification (Trade Size)

Based on **median trade size in SOL** across all buy transactions.

```python
def classify_size(trade_sizes_sol: list[float]) -> str:
    """Classify wallet by typical trade size.

    Args:
        trade_sizes_sol: List of trade sizes in SOL.

    Returns:
        Size tier: whale, large, medium, or small.
    """
    if not trade_sizes_sol:
        return "unknown"

    import statistics
    median = statistics.median(trade_sizes_sol)

    if median > 100:
        return "whale"
    elif median > 10:
        return "large"
    elif median > 1:
        return "medium"
    else:
        return "small"
```

### Size Consistency

Check whether the wallet uses consistent sizing or varies dramatically:

```python
def sizing_consistency(trade_sizes: list[float]) -> str:
    """Assess how consistent trade sizing is."""
    import statistics
    if len(trade_sizes) < 5:
        return "insufficient_data"
    cv = statistics.stdev(trade_sizes) / statistics.mean(trade_sizes)
    if cv < 0.3:
        return "very_uniform"     # Likely bot or fixed-size strategy
    elif cv < 0.6:
        return "moderate"         # Adaptive but disciplined
    elif cv < 1.0:
        return "variable"         # Opportunistic sizing
    else:
        return "highly_variable"  # Erratic or conviction-based
```

## Bot vs. Human Detection

### Inter-Trade Interval Analysis

The primary signal for bot detection is the **coefficient of variation (CV)** of time gaps between consecutive trades.

```python
def bot_probability(trade_timestamps: list[float]) -> float:
    """Estimate probability that a wallet is operated by a bot.

    Uses inter-trade interval regularity as the primary signal.
    CV < 0.3 is highly suggestive of automated execution.

    Args:
        trade_timestamps: Unix timestamps of trades, sorted ascending.

    Returns:
        Probability from 0.0 (definitely human) to 1.0 (definitely bot).
    """
    if len(trade_timestamps) < 10:
        return 0.0  # Insufficient data

    import statistics

    intervals = [
        trade_timestamps[i + 1] - trade_timestamps[i]
        for i in range(len(trade_timestamps) - 1)
    ]
    intervals = [i for i in intervals if i > 0]  # Remove duplicates
    if len(intervals) < 5:
        return 0.0

    mean_interval = statistics.mean(intervals)
    std_interval = statistics.stdev(intervals)
    cv = std_interval / mean_interval if mean_interval > 0 else 999

    # Score components
    timing_score = max(0, 1.0 - cv / 0.5)  # Low CV = more bot-like

    # Check for round-number intervals (e.g., exactly 60s, 300s)
    round_count = sum(1 for i in intervals if i % 10 < 1 or i % 10 > 9)
    round_pct = round_count / len(intervals)
    round_score = round_pct  # Higher = more bot-like

    # 24/7 activity (humans sleep, bots don't)
    from datetime import datetime, timezone
    hours = [datetime.fromtimestamp(t, tz=timezone.utc).hour for t in trade_timestamps]
    unique_hours = len(set(hours))
    hour_coverage = unique_hours / 24
    hour_score = hour_coverage  # Trading across all hours = more bot-like

    # Weighted combination
    probability = (timing_score * 0.5 + round_score * 0.25 + hour_score * 0.25)
    return round(min(1.0, max(0.0, probability)), 2)
```

### Additional Bot Indicators

| Indicator | Bot Signal | Human Signal |
|-----------|-----------|-------------|
| Trade timing CV | < 0.3 | > 0.8 |
| Active hours per day | > 20 | 8–16 |
| Weekend activity | Same as weekday | Reduced |
| Size variance | Very low (CV < 0.2) | Moderate (CV 0.4–1.0) |
| Response to price moves | Immediate (< 2 blocks) | Delayed (minutes) |

## Focus Area Detection

Classify wallets by which protocols and token types they interact with most.

```python
def classify_focus(
    token_types: list[str],
    programs_used: list[str],
) -> str:
    """Classify wallet focus area based on interaction patterns.

    Args:
        token_types: List like ["pumpfun", "raydium", "pumpfun", "orca", ...].
        programs_used: List of program IDs or labels interacted with.

    Returns:
        Focus label: pumpfun_specialist, dex_trader, defi_farmer,
                     nft_trader, or multi_strategy.
    """
    if not token_types:
        return "unknown"

    total = len(token_types)
    from collections import Counter
    type_counts = Counter(token_types)

    pumpfun_pct = type_counts.get("pumpfun", 0) / total

    program_counts = Counter(programs_used)
    lp_programs = {"raydium_amm", "orca_whirlpool", "meteora_dlmm"}
    lp_interactions = sum(program_counts.get(p, 0) for p in lp_programs)
    lp_pct = lp_interactions / max(len(programs_used), 1)

    nft_programs = {"metaplex", "tensor", "magic_eden"}
    nft_interactions = sum(program_counts.get(p, 0) for p in nft_programs)
    nft_pct = nft_interactions / max(len(programs_used), 1)

    if pumpfun_pct > 0.7:
        return "pumpfun_specialist"
    elif nft_pct > 0.5:
        return "nft_trader"
    elif lp_pct > 0.4:
        return "defi_farmer"
    elif pumpfun_pct < 0.3:
        return "dex_trader"
    else:
        return "multi_strategy"
```

## Composite Classification

Combine all classifiers into a single wallet profile:

```python
def build_profile(
    hold_times: list[float],
    trade_sizes: list[float],
    timestamps: list[float],
    token_types: list[str],
    programs: list[str],
) -> dict:
    """Build a complete wallet classification profile."""
    return {
        "style": classify_style(hold_times),
        "size_tier": classify_size(trade_sizes),
        "bot_probability": bot_probability(timestamps),
        "focus": classify_focus(token_types, programs),
        "hold_distribution": analyze_hold_distribution(hold_times),
        "sizing_consistency": sizing_consistency(trade_sizes),
        "trade_count": len(hold_times),
    }
```

## Confidence Levels

| Trade Count | Confidence | Recommendation |
|-------------|-----------|----------------|
| < 10 | Very Low | Do not classify |
| 10–29 | Low | Tentative classification only |
| 30–99 | Moderate | Reasonable classification |
| 100–499 | High | Reliable classification |
| 500+ | Very High | Strong statistical basis |

### Referencia: references/performance_metrics.md

# Performance Metrics Reference

Detailed formulas, interpretation guidelines, and edge case handling for wallet performance analysis.

## Win Rate

**Formula:**
```
win_rate = count(trades where pnl > 0) / count(all_closed_trades)
```

**Requirements:**
- Minimum 30 closed trades for statistical significance
- Only count fully closed positions (all tokens sold)
- Include fees in PnL calculation (a trade that made 0.01 SOL but cost 0.005 SOL in fees is still a win at 0.005 SOL net)

**Interpretation:**
| Win Rate | Assessment | Context |
|----------|-----------|---------|
| > 80% | Suspicious | Possible wash trading or tiny wins with large losses |
| 60–80% | Excellent | Sustainable if profit factor also high |
| 45–60% | Good | Standard for profitable traders with good R:R |
| 30–45% | Acceptable | Can be profitable with high avg win / avg loss ratio |
| < 30% | Poor | Rarely sustainable regardless of win size |

**By token type:**
Separate win rates for PumpFun tokens vs. established tokens. PumpFun win rates are typically lower (30–40%) but winners can be 10x+, while established token trading shows higher win rates (50–60%) with smaller moves.

## ROI Per Trade

**Formula:**
```
roi = (exit_value - entry_value - total_fees) / entry_value
```

Where:
- `entry_value` = total SOL spent buying the token (sum of all buys)
- `exit_value` = total SOL received selling the token (sum of all sells)
- `total_fees` = platform fees + priority fees + estimated slippage

**Handling Partial Exits (FIFO):**
```python
def compute_roi_fifo(buys: list[dict], sells: list[dict]) -> float:
    """Compute ROI using FIFO cost basis.

    Args:
        buys: [{"amount": token_qty, "cost_sol": sol_spent}, ...]
        sells: [{"amount": token_qty, "proceeds_sol": sol_received}, ...]

    Returns:
        ROI as a decimal (0.5 = 50% gain).
    """
    buy_queue = list(buys)  # FIFO queue
    total_cost = 0.0
    total_proceeds = 0.0

    for sell in sells:
        remaining = sell["amount"]
        total_proceeds += sell["proceeds_sol"]

        while remaining > 0 and buy_queue:
            buy = buy_queue[0]
            if buy["amount"] <= remaining:
                total_cost += buy["cost_sol"]
                remaining -= buy["amount"]
                buy_queue.pop(0)
            else:
                fraction = remaining / buy["amount"]
                total_cost += buy["cost_sol"] * fraction
                buy["amount"] -= remaining
                buy["cost_sol"] *= (1 - fraction)
                remaining = 0

    if total_cost == 0:
        return 0.0
    return (total_proceeds - total_cost) / total_cost
```

**Fee Estimation:**
- Solana base fee: 0.000005 SOL per transaction
- Priority fee: variable, typically 0.0001–0.01 SOL
- Jupiter platform fee: 0 (no fee) for basic swaps
- Slippage: estimate from trade size vs. pool liquidity

## Profit Factor

**Formula:**
```
profit_factor = sum(pnl for trades where pnl > 0) / abs(sum(pnl for trades where pnl < 0))
```

**Edge Cases:**
- No losing trades: profit_factor = infinity (use a cap of 99.9)
- No winning trades: profit_factor = 0
- No closed trades: undefined (return None)

**Interpretation:**
| Profit Factor | Rating | Meaning |
|--------------|--------|---------|
| > 3.0 | Exceptional | Very high edge, verify not cherry-picked |
| 2.0–3.0 | Excellent | Strong, sustainable edge |
| 1.5–2.0 | Good | Solid performance |
| 1.0–1.5 | Marginal | Small edge, vulnerable to costs |
| 0.7–1.0 | Poor | Losing after costs |
| < 0.7 | Very Poor | Significant negative edge |

**Rolling Profit Factor:**
Calculate profit factor over rolling windows to detect performance trends:
```python
def rolling_profit_factor(pnl_series: list[float], window: int = 20) -> list[float]:
    """Compute rolling profit factor over a sliding window."""
    results = []
    for i in range(window, len(pnl_series) + 1):
        window_pnl = pnl_series[i - window:i]
        wins = sum(p for p in window_pnl if p > 0)
        losses = abs(sum(p for p in window_pnl if p < 0))
        pf = wins / losses if losses > 0 else 99.9
        results.append(round(pf, 2))
    return results
```

## Sharpe-Like Ratio

**Formula:**
```
sharpe = mean(trade_returns) / std(trade_returns) * sqrt(trades_per_year)
```

**Annualization:**
- Estimate `trades_per_year` from observed frequency
- `trades_per_year = trades_per_day * 365`
- If trading for < 30 days, annualization is unreliable

**Interpretation:**
| Annualized Sharpe | Rating |
|-------------------|--------|
| > 3.0 | Exceptional (verify data quality) |
| 2.0–3.0 | Excellent |
| 1.0–2.0 | Good |
| 0.5–1.0 | Mediocre |
| < 0.5 | Poor |

**Note:** This is an approximation. True Sharpe uses continuous returns and a risk-free rate. For crypto trading with discrete trade-level returns, this metric provides directional guidance rather than precise comparison with traditional finance Sharpe ratios.

## Maximum Drawdown

**Formula:**
```python
def max_drawdown(cumulative_pnl: list[float]) -> tuple[float, int, int]:
    """Compute maximum drawdown from cumulative PnL series.

    Returns:
        (max_dd_pct, peak_index, trough_index)
    """
    peak = cumulative_pnl[0]
    peak_idx = 0
    max_dd = 0.0
    max_dd_peak = 0
    max_dd_trough = 0

    for i, value in enumerate(cumulative_pnl):
        if value > peak:
            peak = value
            peak_idx = i

        if peak > 0:
            dd = (peak - value) / peak
        else:
            dd = 0

        if dd > max_dd:
            max_dd = dd
            max_dd_peak = peak_idx
            max_dd_trough = i

    return (round(max_dd, 4), max_dd_peak, max_dd_trough)
```

**Interpretation:**
| Max Drawdown | Assessment |
|-------------|-----------|
| < 10% | Very conservative |
| 10–25% | Disciplined risk management |
| 25–50% | Moderate risk, common in crypto |
| 50–75% | High risk tolerance |
| > 75% | Extremely aggressive or poor risk management |

## Performance Decay Detection

Compare recent performance to historical performance to detect declining edge.

```python
def detect_decay(
    trade_pnls: list[float],
    recent_window: int = 30,
) -> dict:
    """Detect performance decay by comparing recent vs. historical metrics.

    Args:
        trade_pnls: Chronological list of trade PnLs.
        recent_window: Number of recent trades to compare.

    Returns:
        Decay assessment with metrics comparison.
    """
    if len(trade_pnls) < recent_window * 2:
        return {"status": "insufficient_data"}

    recent = trade_pnls[-recent_window:]
    historical = trade_pnls[:-recent_window]

    recent_wr = sum(1 for p in recent if p > 0) / len(recent)
    hist_wr = sum(1 for p in historical if p > 0) / len(historical)

    recent_avg = sum(recent) / len(recent)
    hist_avg = sum(historical) / len(historical)

    r_wins = sum(p for p in recent if p > 0)
    r_losses = abs(sum(p for p in recent if p < 0))
    recent_pf = r_wins / r_losses if r_losses > 0 else 99.9

    h_wins = sum(p for p in historical if p > 0)
    h_losses = abs(sum(p for p in historical if p < 0))
    hist_pf = h_wins / h_losses if h_losses > 0 else 99.9

    wr_change = recent_wr - hist_wr
    pf_change = recent_pf - hist_pf

    if wr_change < -0.1 and pf_change < -0.5:
        status = "significant_decay"
    elif wr_change < -0.05 or pf_change < -0.3:
        status = "moderate_decay"
    elif wr_change > 0.05 and pf_change > 0.3:
        status = "improving"
    else:
        status = "stable"

    return {
        "status": status,
        "recent_win_rate": round(recent_wr, 3),
        "historical_win_rate": round(hist_wr, 3),
        "win_rate_delta": round(wr_change, 3),
        "recent_profit_factor": round(recent_pf, 2),
        "historical_profit_factor": round(hist_pf, 2),
        "profit_factor_delta": round(pf_change, 2),
        "recent_avg_pnl": round(recent_avg, 4),
        "historical_avg_pnl": round(hist_avg, 4),
    }
```

## Consistency Metrics

### Rolling Win Rate Stability

```python
def win_rate_stability(trade_pnls: list[float], window: int = 20) -> float:
    """Compute standard deviation of rolling win rate.

    Lower values indicate more consistent performance.
    """
    import statistics
    if len(trade_pnls) < window * 2:
        return -1.0

    rolling_wrs = []
    for i in range(window, len(trade_pnls) + 1):
        chunk = trade_pnls[i - window:i]
        wr = sum(1 for p in chunk if p > 0) / len(chunk)
        rolling_wrs.append(wr)

    return round(statistics.stdev(rolling_wrs), 3)
```

### Consistency Score

Combine stability measures into a composite 0–100 score by summing contributions from win rate stability (lower std = better), drawdown control (lower = better), profit factor sustainability (higher = better), and sample size (more trades = more reliable). Start from a base of 50 and add/subtract up to 20 points per factor.
