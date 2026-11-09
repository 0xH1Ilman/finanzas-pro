# 14-datos-herramientas — parte 2

Skills de terceros agrupadas por tema. Cada sección indica fuente, licencia y dónde está su código.



---

## SKILL: tradingview-reader

- Fuente: `himself65/finance-skills` → `plugins/data-providers/skills/tradingview-reader` (MIT)
- Cuándo usarla: >

# TradingView Reader (Read-Only)

If your host has not already executed the shell probes below (for example, in Codex), run the commands inside the `!` wrappers with its shell tool before choosing a setup path. Use the actual output; if shell access is unavailable, report that limitation.

Reads TradingView's desktop macOS app for quotes, options chains, and chart state via [opencli](https://github.com/jackwener/opencli) and a CDP attach to the running TradingView.app process. Powered by the `tradingview` plugin in this repo's [`opencli-plugins/tradingview`](https://github.com/himself65/finance-skills/tree/main/opencli-plugins/tradingview) tree (a separate plugin from opencli's built-in adapters, installed via opencli's monorepo subpath syntax).

**This skill is read-only.** Designed for analysis: pulling options chains, checking IV/greeks, capturing chart state. It does NOT place trades, post ideas, modify watchlists, or change chart layouts.

> **Headless alternative**: for plain quotes, TA readouts, screeners, futures, or a greeks-free options chain, prefer the sibling `tradingview-mcp` skill (bundled MCP server, no desktop app, no CDP relaunch). Use *this* skill when you need greeks / per-strike IV skew, expiries with contract counts, or account-bound data (watchlists, alerts, charts, TV news).

**Important**: Unlike browser-based opencli readers (twitter, linkedin), this one talks directly to a running TradingView desktop app over Chrome DevTools Protocol. The user must (a) have `TradingView.app` installed, and (b) be logged in inside that app. The plugin handles relaunching with the debug port.

**How it works**: data commands read the app's session cookies over CDP and call TradingView's HTTP APIs from Node directly, so no Browser Bridge extension or `apps.yaml` registration is needed.

---

## Step 1: Ensure opencli + Plugin Are Installed and Ready

**Current environment status:**

```
!`(command -v opencli && opencli tradingview status 2>&1 | head -5 && echo "READY" || echo "SETUP_NEEDED") 2>/dev/null || echo "NOT_INSTALLED"`
```

If the status above shows `READY`, skip to Step 2. Otherwise:

### NOT_INSTALLED — Install opencli

```bash
npm install -g @jackwener/opencli
```

Requires Node.js >= 24 — the `tradingview` plugin installed in the next step declares `engines.node >= 24`.

### SETUP_NEEDED — Install the TradingView plugin and launch with CDP

The TradingView adapter is **not** built into opencli — it's a separate plugin:

```bash
# Install the plugin
opencli plugin install github:himself65/finance-skills/tradingview

# Relaunch TradingView.app with CDP enabled (one-time per session)
opencli tradingview launch
```

The `launch` step quits the running TradingView and reopens it with `--remote-debugging-port=9222`. **Warn the user to save chart layouts first** if they have unsaved drawings.

### Common setup issues

| Symptom | Fix |
|---|---|
| `opencli: command not found` | `npm install -g @jackwener/opencli` (Node ≥ 24) |
| `Unknown command: tradingview` | `opencli plugin install github:himself65/finance-skills/tradingview` |
| `Cannot reach CDP at http://127.0.0.1:9222` | App not launched with debug port — run `opencli tradingview launch` |
| `No tradingview.com cookies found` | App is open but logged out — log in inside the desktop app |
| `No TradingView tab found` | Open any chart or symbol page in TradingView, then retry |
| Empty chain / 0 contracts | Subscription tier on the logged-in account doesn't include options for this symbol |

---

## Step 2: Identify What the User Needs

### Setup / chart inspection

| User Request | Command | Key Flags |
|---|---|---|
| Setup / connection check | `opencli tradingview status` | — |
| Relaunch app with CDP | `opencli tradingview launch` | `--port 9222` |
| What's on the chart | `opencli tradingview chart-state` | `--tab <id>` |
| Screenshot a chart | `opencli tradingview screenshot --output ~/charts/nvda.png` | `--tab <id>` |

### Quotes + options

| User Request | Command | Key Flags |
|---|---|---|
| Spot quote | `opencli tradingview quote --ticker X` | `--exchange NASDAQ` |
| Options chain (full) | `opencli tradingview options-chain --ticker X` | `--exchange` |
| Options chain (one expiry, ATM band) | `opencli tradingview options-chain --ticker X --expiry YYYY-MM-DD` | `--type call\|put`, `--strikes-around-spot N` |
| List expiries | `opencli tradingview options-expiries --ticker X` | — |

### Screener

| User Request | Command | Key Flags |
|---|---|---|
| Generic screener (stocks/crypto/forex/futures/bonds) | `opencli tradingview screener --market america --columns ...` | `--filter <json>`, `--sort field:desc`, `--limit N`, `--label-product` |
| US stocks with RSI < 30, sorted by volume | `opencli tradingview screener --market america --columns "name,close,RSI\|60,volume" --filter '[{"left":"RSI\|60","operation":"less","right":30}]' --sort volume:desc` | — |
| Top crypto by market cap | `opencli tradingview screener --market coin --columns "name,close,change,market_cap_calc" --sort market_cap_calc:desc --limit 50` | — |
| Symbol search / autocomplete | `opencli tradingview search --query "nvidia"` | `--type stock\|funds\|crypto\|...`, `--exchange`, `--country` |

### News

| User Request | Command | Key Flags |
|---|---|---|
| Global news headlines | `opencli tradingview news --limit 25` | `--category`, `--area`, `--section`, `--provider` |
| News for a specific ticker | `opencli tradingview news --symbol NASDAQ:AAPL` | `--limit`, `--section analysis\|press_release\|...` |
| Full story by id | `opencli tradingview news --id <story-id>` | `--lang en` |

### Watchlists + alerts

| User Request | Command | Key Flags |
|---|---|---|
| List all watchlists | `opencli tradingview watchlists` | — |
| Symbols in one watchlist | `opencli tradingview watchlists --id <wl-id>` | — |
| Colored-flag list (red/orange/yellow/green/blue/purple) | `opencli tradingview watchlists --color red` | — |
| List all alerts | `opencli tradingview alerts --type list` | — |
| Active alerts | `opencli tradingview alerts --type active` | — |
| Recently triggered alerts | `opencli tradingview alerts --type triggered` | — |
| Alerts that fired while offline | `opencli tradingview alerts --type offline` | — |
| Full alert log | `opencli tradingview alerts --type log` | — |

---

## Step 3: Execute the Command

### General pattern

```bash
# Use -f json or -f yaml for structured output
opencli tradingview options-chain --ticker SNDK --expiry 2026-05-22 -f json
opencli tradingview options-chain --ticker NVDA --strikes-around-spot 8 -f csv
opencli tradingview quote --ticker SPY --exchange NYSEARCA -f json
```

### Key rules

1. **Run `opencli tradingview status` first** if connectivity is uncertain — it reports CDP connection state and active TradingView tabs.
2. **Use `-f json`** for programmatic processing (LLM context, downstream skills).
3. **Filter by expiry and `--strikes-around-spot`** — full chains can be 3,000+ rows; an unfiltered dump is rarely what the user wants.
4. **Default `--exchange NASDAQ`** for US equities; require explicit `--exchange` for ETFs (e.g. SPY = NYSEARCA, QQQ = NASDAQ) or non-US listings.
5. **For `screener`, choose `--columns` deliberately** — it controls both the request and the output table. Include `name` and any field used in `--filter` or `--sort`. Append `|TF` for an indicator's timeframe, e.g. `RSI|60` for 1-hour RSI. The default columns are sensible for stocks but should be replaced for crypto / forex / futures (different field catalogs).
6. **For `screener`, `--filter` is JSON** — array of `{left, operation, right}` clauses. Always single-quote the JSON in shell to avoid escaping issues. See `references/commands.md` for the operations cheat sheet.
7. **For `news`, narrow the feed early** — the global feed is firehose-level. Use `--symbol`, `--category`, `--section`, or `--provider` before raising `--limit`.
8. **For `search`, prefer it over guessing** — when the user gives an ambiguous ticker (e.g. "SPY" without exchange), run `search --query SPY` first to confirm the listing, then pass `--exchange` to subsequent commands.
9. **For `watchlists` and `alerts`, default to summary** — a user asking "what's in my watchlists?" wants list names + counts, not every symbol.
10. **Read-only.** No trades, no watchlist edits, no alert creation/deletion, no chart writes — the plugin intentionally does not expose write endpoints (`/append`, `/replace`, `/create_alert`, etc.), so don't look for workarounds.

### Output format flag (`-f`)

| Format | Flag | Best for |
|---|---|---|
| Table | `-f table` (default) | Human-readable terminal output |
| JSON | `-f json` | Programmatic processing, LLM context |
| YAML | `-f yaml` | Structured output, readable |
| Markdown | `-f md` | Documentation, reports |
| CSV | `-f csv` | Spreadsheet export |

### Output columns

- `quote` — `symbol`, `close`, `change`, `change_abs`, `currency`, `time`
- `options-chain` — `expiry`, `dte`, `strike`, `type`, `bid`, `ask`, `mid`, `iv`, `delta`, `gamma`, `theta`, `vega`, `rho`, `theo`, `bid_iv`, `ask_iv`, `symbol`
- `options-expiries` — `expiry`, `dte`, `contracts_count`
- `screener` — dynamic; one column per `--columns` entry, plus `symbol`. (Default: `name`, `close`, `change`, `volume`, `market_cap_basic`, `sector.tr`.)
- `search` — `symbol`, `description`, `type`, `exchange`, `country`, `currency`
- `news` (list mode) — `id`, `published`, `provider`, `title`, `urgency`, `related_symbols`, `link`
- `news` (story mode, `--id` set) — `id`, `published`, `provider`, `title`, `body`, `tags`, `link`
- `watchlists` — `id`, `name`, `symbol_count`, `symbols`
- `alerts` — `id`, `name`, `symbol`, `type`, `condition`, `value`, `active`, `status`, `fired_at`
- `chart-state` — `layout_id`, `symbol`, `interval`, `url`
- `screenshot` — `path`, `bytes`

---

## Step 4: Present the Results

1. **Lead with the structure summary** — for an options chain, state spot price, expiry being shown, ATM strike, and IV regime first; then the table. For a screener, lead with the count of matches and the filters applied.
2. **Filter aggressively before showing** — never paste a 3,000-row chain or a 500-row screener. Default to ATM ± 6 strikes per expiry for chains; for screeners cap to top 20 unless the user asks for more.
3. **Highlight skew** — when showing both calls and puts, note IV skew direction if material.
4. **For chart-state**, report layout id + symbol + interval + URL succinctly; offer to screenshot.
5. **For news (list mode)**, group by provider and lead with timestamps in the user's likely timezone (or always UTC ISO if uncertain). Include the link so the user can open the story. For story mode (`--id` set), the body is plain text — present it as-is, optionally trimmed.
6. **For watchlists**, summarize counts before listing symbols (e.g. "3 watchlists: Earnings (24 syms), AI plays (12 syms), Hedges (8 syms)"). Don't dump 100-symbol watchlist contents unless asked.
7. **For alerts**, group by status (active vs triggered/fired) and order recent firings by `fired_at` desc. Don't expose alert ids unless the user explicitly asks.
8. **For screener results**, surface the top movers / extreme values in plain prose first (e.g. "highest market cap NVDA at $4.2T, 12 names below the RSI<30 threshold"), then the table.
9. **Treat sessions as private** — never expose CDP target IDs, cookies, or layout IDs unless the user asks.

---

## Step 5: Diagnostics

```bash
opencli tradingview status
```

Returns CDP connection state and active TradingView tabs. If CDP is down, run `opencli tradingview launch` to relaunch with the debug port.

---

## Error Reference

| Error | Cause | Fix |
|---|---|---|
| `Unknown command: tradingview` | Plugin not installed | `opencli plugin install github:himself65/finance-skills/tradingview` |
| `Cannot reach CDP at http://127.0.0.1:9222` | App launched without debug port | `opencli tradingview launch` |
| `No tradingview.com cookies found` | Logged out of TradingView | Log in inside the desktop app |
| `No TradingView tab found` | App open but no TradingView page loaded | Open any chart or symbol page, then retry |
| `scanner 400 / Empty chain / totalCount=0` | Subscription tier doesn't cover this symbol's options | Check account tier in the desktop app |
| `Symbol not found` | Wrong exchange | Pass `--exchange` explicitly, or run `opencli tradingview search --query <name>` first |
| Rate limited | Too many requests | Wait a few seconds, then retry |

---

## Reference Files

- `references/commands.md` — Every command with all flags, output examples, and analyst workflows

### Referencia: README.md

# tradingview-reader

Read-only TradingView desktop reader for market data via [opencli](https://github.com/jackwener/opencli) + the [`tradingview`](../../../../opencli-plugins/tradingview/) opencli plugin shipped alongside this skill.

## What it does

Reads TradingView's macOS desktop app for market data via Chrome DevTools Protocol — no API keys, no cookie extraction, no scraping. Capabilities include:

- **Quote** — spot quote for any symbol (close, change, currency)
- **Options chain** — full chain or filtered by expiry / type / ATM band, with full greeks (delta, gamma, theta, vega, rho), IV, bid/ask IVs, and theoretical price
- **Options expiries** — list available expirations with DTE and contracts count
- **Screener and search** — stocks, crypto, forex, futures, bonds, and symbol lookup
- **News** — TradingView news feed and full story lookup
- **Watchlists and alerts** — read the signed-in account's existing lists and alert states
- **Chart state** — current symbol, interval, and layout of an active chart tab
- **Screenshot** — PNG capture of a chart tab
- **Status / launch** — CDP connection diagnostics and one-shot relaunch helper

**This skill is read-only.** It does NOT place trades, modify watchlists, post ideas, or change chart layouts.

## Authentication

No API key, no token. The adapter attaches to the user's already-logged-in TradingView desktop app over CDP. Just have `TradingView.app` installed and logged in.

## How it works

Data commands harvest session cookies via CDP `Storage.getCookies`, then fire HTTP requests from Node directly. Page-context fetch is blocked by browser CORS preflight even from TradingView's own pages — the desktop app uses Electron's main process (Node network stack) to bypass this, and the adapter replicates that path. No Browser Bridge extension or `apps.yaml` registration is required.

## Triggers

- "options chain for X", "what's the IV on Y", "show me SNDK puts"
- "what's the bid/ask on AAPL options", "TradingView IV skew"
- "what symbol is on my TradingView chart", "screenshot my NVDA chart"
- "read my TradingView watchlist", "show active TV alerts", "TradingView news for NVDA"
- "screen US stocks on TradingView", "find the TradingView symbol for gold futures"
- "TradingView quote for", "TV options for", "what expiries does X have"
- Any mention of TradingView in context of reading market data, options data, or charts

## Platform

Works on **Claude Code** and other CLI-based agents on macOS. Does **not** work on Claude.ai — the sandbox restricts network access and binaries required by opencli + CDP.

The plugin is currently macOS-only (relies on `open -a TradingView --args`).

## Setup

```bash
# Choose finance-data-providers when prompted.
npx plugins add himself65/finance-skills

# Or install just this skill
npx skills add himself65/finance-skills --skill tradingview-reader
```

See the [main README](../../../../README.md) for more installation options.

## Prerequisites

- Node.js >= 24 — for `npm install -g @jackwener/opencli`
- `TradingView.app` installed on macOS, logged in
- The `tradingview` opencli plugin: `opencli plugin install github:himself65/finance-skills/tradingview` (installs from this repo's monorepo subpath)
- Relaunch with CDP enabled: `opencli tradingview launch` (one-time per session — warn the user to save chart layouts first)

## Reference files

- `references/commands.md` — Complete read command reference with all flags, output schemas, and analyst workflows

### Referencia: references/commands.md

# opencli TradingView Command Reference (Read-Only)

Complete read-only reference for the `tradingview` opencli adapter that lives in this repo's [`opencli-plugins/tradingview`](../../../../../opencli-plugins/tradingview/) tree, scoped to financial research use cases.

Install: `npm install -g @jackwener/opencli && opencli plugin install github:himself65/finance-skills/tradingview`

**This skill is read-only.** No write operations, no trade execution.

---

## Setup

The adapter connects to a running `TradingView.app` over Chrome DevTools Protocol (CDP) — no bot account, no API key, no Browser Bridge extension.

**Requirements:**
1. Node.js >= 24 (the `tradingview` plugin declares `engines.node >= 24`)
2. `TradingView.app` installed on macOS, logged in
3. App launched with `--remote-debugging-port=9222` (the `launch` command handles this)

**Launch with CDP:**

```bash
opencli tradingview launch              # default port 9222
opencli tradingview launch --port 9333  # custom port
```

The `launch` step quits any running TradingView and reopens it with the debug port. Warn the user to save chart layouts first.

**Verify connectivity:**

```bash
opencli tradingview status
```

---

## Read Operations

### launch

Quits any running TradingView and re-launches it with `--remote-debugging-port` enabled. Polls `/json/version` until the app is reachable.

```bash
opencli tradingview launch
opencli tradingview launch --port 9333
opencli tradingview launch -f json
```

| Flag | Required | Default | Notes |
|---|---|---|---|
| `--port` | no | `9222` | CDP port |
| `-f, --format` | no | `table` | `table\|json\|yaml\|md\|csv` |

**Output columns:** `port`, `pid`, `ready`

---

### status

Reports CDP connection state and lists active TradingView tabs (chart, symbol page, options page).

```bash
opencli tradingview status
opencli tradingview status -f json
```

**Output columns:** `connected`, `tabs[]` (each tab has `id`, `type`, `url`, `title`)

Use `OPENCLI_CDP_TARGET=tradingview.com` to disambiguate when multiple Electron CDP sessions are running on the host.

---

### quote

Single-symbol spot quote, backed by `scanner.tradingview.com/global/scan2`.

```bash
opencli tradingview quote --ticker AAPL
opencli tradingview quote --ticker SPY --exchange NYSEARCA -f json
opencli tradingview quote --ticker BABA --exchange NYSE
```

| Flag | Required | Default | Notes |
|---|---|---|---|
| `--ticker` | yes | — | Symbol (e.g. `AAPL`) |
| `--exchange` | no | `NASDAQ` | TradingView exchange code (`NASDAQ`, `NYSE`, `NYSEARCA`, ...) |
| `-f, --format` | no | `table` | `table\|json\|yaml\|md\|csv` |

**Output columns:** `symbol`, `close`, `change`, `change_abs`, `currency`, `time`

---

### options-chain

Full options chain or filtered slice. Backed by `scanner.tradingview.com/options/scan2`. Returns one row per (expiry × strike × type) tuple — the response is the entire chain in one request, not paginated.

```bash
# Full chain (every expiry, every strike, calls + puts) — can be 3,000+ rows
opencli tradingview options-chain --ticker SNDK -f json

# One expiry, ATM ± 6 strikes, both call and put
opencli tradingview options-chain --ticker SNDK --expiry 2026-05-22 \
    --strikes-around-spot 6 -f json

# Calls only, full strike list, single expiry
opencli tradingview options-chain --ticker NVDA --expiry 2026-06-19 \
    --type call --strikes-around-spot 0 -f json

# CSV export for spreadsheet analysis
opencli tradingview options-chain --ticker AAPL --expiry 2026-05-15 -f csv
```

| Flag | Required | Default | Notes |
|---|---|---|---|
| `--ticker` | yes | — | Underlying ticker |
| `--exchange` | no | `NASDAQ` | TradingView exchange code |
| `--expiry` | no | all | ISO date (`YYYY-MM-DD`) |
| `--type` | no | both | `call` or `put` |
| `--strikes-around-spot` | no | `6` | Half-band; total strikes = 2N+1. `0` = full strike list. |
| `-f, --format` | no | `table` | `table\|json\|yaml\|md\|csv` |

**Output columns:** `expiry`, `dte`, `strike`, `type`, `bid`, `ask`, `mid`, `iv`, `delta`, `gamma`, `theta`, `vega`, `rho`, `theo`, `bid_iv`, `ask_iv`, `symbol`

**Symbol format:** `OPRA:<ROOT><YY><MM><DD><C|P><STRIKE>` (OCC-style, e.g. `OPRA:SNDK260522C2090.0`).

**Sample row (JSON):**

```json
{
  "expiry": "2026-05-22", "dte": 12, "strike": 2090, "type": "call",
  "bid": 12.9, "ask": 18.4, "mid": 15.65, "iv": 1.0953,
  "delta": 0.1035, "gamma": 0.000542, "theta": -2.177, "vega": 0.5456, "rho": 0.0552,
  "theo": 15.0, "bid_iv": 1.0546, "ask_iv": 1.1540,
  "symbol": "OPRA:SNDK260522C2090.0"
}
```

#### Common analyst workflows

- **IV regime check:** `--strikes-around-spot 0 --expiry <next-monthly>` → look at ATM IV vs IV at ±20%.
- **Skew measurement:** filter calls and puts at equidistant OTM strikes (e.g. ±10% from spot), compare IVs to quantify put skew.
- **Liquidity scan before structure:** sort by `(ask - bid)/mid` to flag wide spreads before placing a multi-leg order.
- **Theoretical edge:** compare `mid` to `theo` per row — large positive `theo - mid` suggests a market mispricing (or stale data — verify with the bid IV / ask IV envelope).

---

### options-expiries

Lists every available expiration for a ticker with DTE and contract counts. Useful before pulling a full chain to know what's available.

```bash
opencli tradingview options-expiries --ticker SNDK
opencli tradingview options-expiries --ticker SPY --exchange NYSEARCA -f json
```

| Flag | Required | Default | Notes |
|---|---|---|---|
| `--ticker` | yes | — | Underlying ticker |
| `--exchange` | no | `NASDAQ` | TradingView exchange code |
| `-f, --format` | no | `table` | `table\|json\|yaml\|md\|csv` |

**Output columns:** `expiry`, `dte`, `contracts_count`

---

### chart-state

Returns the current symbol/interval/layout of an active chart tab via CDP `Runtime.evaluate`.

```bash
opencli tradingview chart-state               # picks the first chart tab
opencli tradingview chart-state --tab abc123  # specific tab id (from `status`)
opencli tradingview chart-state -f json
```

| Flag | Required | Default | Notes |
|---|---|---|---|
| `--tab` | no | first chart tab | Tab id from `opencli tradingview status` |
| `-f, --format` | no | `table` | `table\|json\|yaml\|md\|csv` |

**Output columns:** `layout_id`, `symbol`, `interval`, `url`

---

### screenshot

Captures a PNG of a chart tab via CDP `Page.captureScreenshot`.

```bash
opencli tradingview screenshot --output ~/charts/nvda.png
opencli tradingview screenshot --tab abc123 --output ./snap.png
```

| Flag | Required | Default | Notes |
|---|---|---|---|
| `--tab` | no | first chart tab | Tab id from `opencli tradingview status` |
| `--output` | no | autogenerated | Output path (PNG) |
| `-f, --format` | no | `table` | `table\|json\|yaml\|md\|csv` |

**Output columns:** `path`, `bytes`

---

## Output Formats

All commands support the `-f` / `--format` flag:

| Format | Flag | Description |
|---|---|---|
| Table | `-f table` (default) | Rich CLI table |
| JSON | `-f json` | Pretty-printed JSON (2-space indent) |
| YAML | `-f yaml` | Structured YAML |
| Markdown | `-f md` | Pipe-delimited markdown tables |
| CSV | `-f csv` | Comma-separated values |

---

## Financial Research Workflows

### Quick IV / skew check on a single ticker

```bash
# 1. List expiries, pick the front month
opencli tradingview options-expiries --ticker NVDA -f json

# 2. Pull ATM band for that expiry, both call and put
opencli tradingview options-chain --ticker NVDA --expiry 2026-05-15 \
    --strikes-around-spot 6 -f json

# 3. Compare ATM call IV vs ATM put IV → skew direction
```

### Liquidity check before a multi-leg structure

```bash
# Pull the legs you plan to trade
opencli tradingview options-chain --ticker AAPL --expiry 2026-06-19 \
    --strikes-around-spot 8 -f csv > aapl_chain.csv

# In the CSV: sort by (ask-bid)/mid descending → widest spreads at the top
# Avoid legs with > 5–10% relative spread on liquid names
```

### Capture a chart for research notes

```bash
# 1. Identify what's currently shown
opencli tradingview chart-state -f json

# 2. Snapshot it
opencli tradingview screenshot --output ~/research/sndk-2026-05-10.png
```

---

## Error Reference

| Error | Cause | Fix |
|---|---|---|
| `Unknown command: tradingview` | Plugin not installed | `opencli plugin install github:himself65/finance-skills/tradingview` |
| `CDP not reachable on :9222` | App launched without debug port | `opencli tradingview launch` |
| `No tab matches tradingview.com` | App open but no TradingView page loaded | Open any chart in TradingView, then retry |
| `Empty chain / totalCount=0` | Subscription tier doesn't cover this symbol's options | Check account tier in the desktop app |
| `Symbol not found` | Wrong exchange | Pass `--exchange` explicitly |
| Multiple Electron CDP targets | Other Electron apps on the same port | Set `OPENCLI_CDP_TARGET=tradingview.com` |
| Rate limited / stale data | Too many requests | Wait a few seconds; the plugin caches `options/scan2` for ~5–10 s per ticker |

---

---

### screener

Generic stock / crypto / forex / futures / bond screener via `scanner.tradingview.com/{market}/scan2`. Same backend powers all of TradingView's screener, movers, and heatmap pages.

```bash
# US stocks with RSI(1h) below 30, sorted by volume
opencli tradingview screener \
    --market america \
    --columns "name,close,RSI|60,volume,market_cap_basic,sector.tr" \
    --filter '[{"left":"RSI|60","operation":"less","right":30}]' \
    --sort volume:desc \
    --limit 25 -f json

# Top 50 crypto by market cap
opencli tradingview screener \
    --market coin \
    --columns "name,close,change,market_cap_calc,total_volume_calc" \
    --sort market_cap_calc:desc --limit 50 -f json

# Specific ticker subset (skip filter, supply tickers explicitly)
opencli tradingview screener \
    --market america \
    --tickers "NASDAQ:AAPL,NASDAQ:MSFT,NASDAQ:NVDA" \
    --columns "name,close,change,market_cap_basic,price_earnings_ttm" -f json
```

| Flag | Required | Default | Notes |
|---|---|---|---|
| `--market` | no | `america` | Market path segment (see "Market codes" below) |
| `--columns` | no | `name,close,change,volume,market_cap_basic,sector.tr` | CSV. Append `|TF` for indicator timeframe, e.g. `RSI|60` for 1h RSI |
| `--filter` | no | — | JSON array of `{left, operation, right}` clauses |
| `--sort` | no | `volume:desc` | `field:asc` or `field:desc` |
| `--tickers` | no | — | Comma-separated `EXCH:SYM` list. Bypasses filter when set. |
| `--label-product` | no | `screener-stock` | Server-side analytics tag (`screener-stock`, `screener-crypto`, ...) |
| `--limit` | no | `50` | Max rows; clamped to `[1, 500]` |
| `--offset` | no | `0` | Pagination start |

**Market codes**

- Stocks (per country): `america`, `uk`, `germany`, `france`, `japan`, `india`, `china`, `hongkong`, `korea`, `taiwan`, `singapore`, `australia`, `canada`, `brazil`, `mexico`, `israel`, `saudi`, etc. (~70 codes)
- Cross-class: `crypto` (CEX pairs), `coin` (crypto coins, different schema), `forex`, `futures`, `bond`, `cfd`, `economics2`, `options`, `global`

**Filter operations**

`equal`, `nequal`, `greater`, `egreater`, `less`, `eless`, `in_range`, `not_in_range`, `empty`, `nempty`, `match` (substring), `nmatch`, `crosses`, `crosses_above`, `crosses_below`, `above%`, `below%`, `in_range%`. For boolean composition use the `filter2: {operator, operands}` field directly via the page-context API (not currently exposed via `--filter`).

**Field catalog**

3,000+ stock fields (1,018 deduplicated). See [TradingView-Screener fields reference](https://shner-elmo.github.io/TradingView-Screener/fields/stocks.html) for the full list. Common ones:

- Price: `close`, `open`, `high`, `low`, `change`, `change_abs`, `gap`, `volume`, `volume_change`
- Fundamentals: `market_cap_basic`, `price_earnings_ttm`, `price_book_fq`, `dividend_yield_recent`, `earnings_per_share_basic_ttm`, `revenue_ttm`, `total_debt`, `return_on_equity_fy`
- Technicals: `RSI`, `RSI|<tf>`, `MACD.macd`, `MACD.signal`, `BB.upper`, `BB.lower`, `ATR`, `ADX`, `Aroon.Up`, `Aroon.Down`, `MOM`, `Mom`, `Stoch.K`, `Stoch.D`
- Recommendation: `Recommend.All`, `Recommend.MA`, `Recommend.Other` (range -1..1)
- Categorical: `type`, `subtype`, `sector`, `sector.tr` (translated), `industry`, `industry.tr`, `country`, `exchange`

#### Common analyst workflows

- **Oversold scan:** `--filter '[{"left":"RSI|60","operation":"less","right":30}]' --sort volume:desc` → high-volume names with 1h RSI < 30.
- **Earnings beats:** `--filter '[{"left":"earnings_per_share_basic_ttm","operation":"egreater","right":0},{"left":"eps_surprise_percent_fq","operation":"greater","right":5}]'`.
- **Sector rotation:** group results by `sector.tr` after pulling top 200 by `change`.
- **Index constituents:** use `--tickers` with the SP500 / Nasdaq100 list to pull the same row set across multiple metrics in one call.

---

### search

Symbol / instrument autocomplete. Backed by `symbol-search.tradingview.com/symbol_search/v3/`. Use this whenever the user's ticker is ambiguous (e.g. "SPY" matches multiple listings) or to discover available exchanges for a name.

```bash
opencli tradingview search --query "nvidia" -f json
opencli tradingview search --query "BTC" --type crypto --exchange BINANCE -f json
opencli tradingview search --query "9988" --country HK
```

| Flag | Required | Default | Notes |
|---|---|---|---|
| `--query` | yes | — | Search text; supports `EXCH:SYM` parsing |
| `--type` | no | all | `stock`, `funds`, `index`, `futures`, `forex`, `crypto`, `bond`, `economic`, `dr`, `cfd`, `option`, `structured` |
| `--exchange` | no | — | `NASDAQ`, `NYSE`, `NYSEARCA`, `BINANCE`, `OANDA`, ... |
| `--country` | no | — | ISO-2 (`US`, `GB`, `JP`, `HK`, `DE`, ...) |
| `--lang` | no | `en` | Description language |
| `--limit` | no | `20` | Max results |
| `--offset` | no | `0` | Pagination start |

**Output columns:** `symbol` (full `EXCH:SYM`), `description`, `type`, `exchange`, `country`, `currency`.

---

### news

TradingView's news headlines feed (or full story). Backed by `news-headlines.tradingview.com/v2/`. Two modes:

- **List** (default): paginated headlines, filterable by symbol / category / area / section / provider.
- **Story** (`--id <story-id>`): one row with the full story body flattened to plain text.

```bash
# Global news feed
opencli tradingview news --limit 25 -f json

# Ticker-specific news
opencli tradingview news --symbol NASDAQ:AAPL --limit 10 -f json

# Analyst notes only, on Reuters
opencli tradingview news --section analysis --provider reuters -f json

# Full story by id
opencli tradingview news --id "tag:reuters.com,2026:newsml_..." -f json
```

| Flag | Required | Default | Notes |
|---|---|---|---|
| `--id` | no | — | When set, fetch full story instead of list |
| `--symbol` | no | — | `EXCH:SYM` filter (omit for global feed) |
| `--category` | no | — | `base`, `stock`, `etf`, `futures`, `forex`, `crypto`, `index`, `bond`, `economic` |
| `--area` | no | — | `WLD`, `AME`, `EUR`, `ASI`, `OCN`, `AFR` |
| `--section` | no | — | `press_release`, `financial_statement`, `insider_trading`, `esg`, `corp_activity`, `analysis`, `recommendation`, `prediction`, `markets_today`, `survey` |
| `--provider` | no | — | Single source (`reuters`, `dow_jones`, `cointelegraph`, ...) |
| `--lang` | no | `en` | Story language |
| `--limit` | no | `25` | Max headlines |

**Output columns (list mode):** `id`, `published`, `provider`, `title`, `urgency`, `related_symbols`, `link`.

**Output columns (story mode):** `id`, `published`, `provider`, `title`, `body` (plain-text rendering of the AST), `tags`, `link`.

#### Common analyst workflows

- **Pre-market scan:** `news --section markets_today --area AME --limit 20` for the morning brief.
- **Earnings call follow-up:** `news --symbol <S> --section press_release` → original release text via `news --id <id>` for AI summarization.
- **Recommendation tracking:** `news --section recommendation --symbol <S>` for upgrades/downgrades.

---

### watchlists

Read-only access to the user's watchlists.

```bash
# List all custom watchlists (id, name, count, symbols)
opencli tradingview watchlists -f json

# Symbols in one watchlist
opencli tradingview watchlists --id rRwIJoVm -f json

# Colored-flag list (red, orange, yellow, green, blue, purple)
opencli tradingview watchlists --color red -f json
```

| Flag | Required | Default | Notes |
|---|---|---|---|
| `--id` | no | — | 8-char watchlist id (mutually exclusive with `--color`) |
| `--color` | no | — | One of: red, orange, yellow, green, blue, purple |

**Output columns:** `id`, `name`, `symbol_count`, `symbols` (comma-separated for table; array in JSON).

**Note:** This skill does **not** expose write endpoints (`/append/`, `/replace/`). Modifying watchlists must be done through the TradingView UI.

---

### alerts

Read-only access to `pricealerts.tradingview.com`. One command, multiple modes via `--type`.

```bash
opencli tradingview alerts --type list      # all alerts (active + paused)
opencli tradingview alerts --type active    # currently armed
opencli tradingview alerts --type triggered # recently fired
opencli tradingview alerts --type offline   # fired while user was offline
opencli tradingview alerts --type log       # full historical fire log
```

| Flag | Required | Default | Notes |
|---|---|---|---|
| `--type` | no | `list` | One of: `list`, `active`, `triggered`, `offline`, `log` |

**Output columns:** `id`, `name`, `symbol`, `type`, `condition`, `value`, `active`, `status`, `fired_at`.

**Tier sensitivity:** TradingView caps the number of saved alerts by tier (Free=1, Essential=10, Plus=20, Premium=400, Ultimate=unlimited). The API surface is identical; only the saved set changes.

**Note:** Write endpoints (`/create_alert`, `/edit_alert`, `/remove_alert`, `/restart_alert`) are intentionally NOT exposed.

---

## Limitations

- **macOS only** — the `launch` helper relies on `open -a TradingView --args`. Linux / Windows desktop apps are not supported by this plugin.
- **Logged-in app required** — no auth bypass; data tier matches what the user sees in the app.
- **Read-only in this skill** — even if the plugin grows write commands later (alerts, watchlists), this skill forbids them.
- **Single attached app at a time** — if multiple Electron CDP sessions exist, set `OPENCLI_CDP_TARGET`.
- **Field positions are read from the response** — never hard-code field indices; if the plugin breaks because TradingView changes the wire format, file an issue at the plugin repo.

---

## Best Practices

- **Filter aggressively** — full chains are 3,000+ rows. Default to ATM ± 6 strikes per expiry.
- **Use `-f json`** for programmatic processing and LLM context.
- **Use `-f csv`** for spreadsheet analysis of chains.
- **Run `status` before `options-chain`** if you suspect connectivity issues.
- **Treat CDP endpoints as private** — never log or display debug URLs, target ids, or layout ids.
- **Spot self-consistency check** — `quote.close` should fall within `[min_strike, max_strike]` of the chain. If not, suspect stale data or wrong exchange.


---

## SKILL: twitter-reader

- Fuente: `himself65/finance-skills` → `plugins/social-readers/skills/twitter-reader` (MIT)
- Cuándo usarla: >

# Twitter Skill (Read-Only)

If your host has not already executed the shell probes below (for example, in Codex), run the commands inside the `!` wrappers with its shell tool before choosing a setup path. Use the actual output; if shell access is unavailable, report that limitation.

Reads Twitter/X for financial research using [opencli](https://github.com/jackwener/opencli), a universal CLI tool that bridges web services to the terminal via browser session reuse.

**This skill is read-only.** It is designed for financial research: searching market discussions, reading analyst tweets, tracking sentiment, and monitoring financial news on Twitter/X. It does NOT support posting, liking, retweeting, replying, or any write operations.

**Important**: opencli reuses your existing Chrome login session — no API keys or cookie extraction needed. Just be logged into x.com in Chrome and have the Browser Bridge extension installed.

---

## Step 1: Ensure opencli Is Installed and Ready

**Current environment status:**

```
!`(command -v opencli && opencli doctor 2>&1 | head -5 && echo "READY" || echo "SETUP_NEEDED") 2>/dev/null || echo "NOT_INSTALLED"`
```

If the status above shows `READY`, skip to Step 2. If `NOT_INSTALLED`, install first:

```bash
# Install opencli globally
npm install -g @jackwener/opencli
```

If `SETUP_NEEDED`, guide the user through setup:

### Setup

opencli requires Node.js >= 20 and a Chrome browser with the Browser Bridge extension:

1. **Install the Browser Bridge extension:**
   - Download the latest `opencli-extension-v{version}.zip` from the [GitHub Releases page](https://github.com/jackwener/opencli/releases)
   - Unzip it, open `chrome://extensions` in Chrome, and enable **Developer mode**
   - Click **Load unpacked** and select the unzipped folder
2. **Login to x.com** in Chrome — opencli reuses your existing browser session
3. **Verify connectivity:**

```bash
opencli doctor
```

This auto-starts the daemon, verifies the extension is connected, and checks session health.

### Common setup issues

| Symptom | Fix |
|---------|-----|
| `Extension not connected` | Install Browser Bridge extension in Chrome and ensure it's enabled |
| `Daemon not running` | Run `opencli doctor` — it auto-starts the daemon |
| `No session for twitter.com` | Login to x.com in Chrome, then retry |
| `CSRF token missing` | Refresh x.com in Chrome to regenerate the ct0 cookie |

---

## Step 2: Identify What the User Needs

Match the user's request to one of the read commands below, then use the corresponding command from `references/commands.md`.

| User Request | Command | Key Flags |
|---|---|---|
| Setup check | `opencli doctor` | — |
| Home feed / timeline | `opencli twitter timeline` | `--type for-you\|following`, `--limit N` (default 20) |
| Search tweets | `opencli twitter search "QUERY"` | `--filter top\|live`, `--limit N` (default 15) |
| Trending topics | `opencli twitter trending` | `--limit N` (default 20) |
| Bookmarks | `opencli twitter bookmarks` | `--limit N` (default 20) |
| Recent tweets from a user | `opencli twitter tweets USERNAME` | `--limit N` (default 20) |
| View a specific thread | `opencli twitter thread TWEET_ID` | `--limit N` (default 50) |
| Twitter article | `opencli twitter article TWEET_ID` | — |
| User profile | `opencli twitter profile USERNAME` | — (defaults to logged-in user) |
| Followers | `opencli twitter followers USERNAME` | `--limit N` (default 50) |
| Following | `opencli twitter following USERNAME` | `--limit N` (default 50) |
| Notifications | `opencli twitter notifications` | `--limit N` (default 20) |

---

## Step 3: Execute the Command

### General pattern

```bash
# Use -f json or -f yaml for structured output
opencli twitter timeline -f json --limit 20
opencli twitter timeline --type following --limit 20

# Recent tweets from a specific user
opencli twitter tweets elonmusk --limit 20 -f json

# Searching for financial topics
opencli twitter search "$AAPL earnings" --filter live --limit 10 -f json
opencli twitter search "Fed rate decision" --limit 20 -f yaml

# Trending topics
opencli twitter trending --limit 20 -f json
```

### Key rules

1. **Check setup first** — run `opencli doctor` before any other command if unsure about connectivity
2. **Use `-f json` or `-f yaml`** for structured output when processing data programmatically
3. **Use `-f csv`** when the user wants spreadsheet-compatible output
4. **Use `--limit N`** to control result count — start with 10-20 unless the user asks for more
5. **For search, use `--filter`** — `top` (default) for relevance, `live` for latest tweets
6. **Read-only** — don't post, like, retweet, reply, quote, follow, or delete, even though opencli exposes some of these commands

### Output format flag (`-f`)

| Format | Flag | Best for |
|---|---|---|
| Table | `-f table` (default) | Human-readable terminal output |
| JSON | `-f json` | Programmatic processing, LLM context |
| YAML | `-f yaml` | Structured output, readable |
| Markdown | `-f md` | Documentation, reports |
| CSV | `-f csv` | Spreadsheet export |

### Output columns

Tweet-listing commands (`timeline`, `search`, `thread`) include: `id`, `author`, `text`, `created_at`, `likes`, `retweets`, `replies`, `views`, `url`, `has_media`, `media_urls`.

`tweets` (per-user posts) also includes `is_retweet`.

`bookmarks` columns: `author`, `text`, `likes`, `retweets`, `bookmarks`, `url`.

`trending` columns: `rank`, `topic`, `tweets`, `category`.

Profile (`profile`) columns: `screen_name`, `name`, `bio`, `location`, `url`, `followers`, `following`, `tweets`, `likes`, `verified`, `created_at`.

`followers` / `following` columns: `screen_name`, `name`, `bio`, `followers`.

`notifications` columns: `id`, `action`, `author`, `text`, `url`.

---

## Step 4: Present the Results

Lead with what matters for the user's research question rather than a raw dump. Attribute each tweet (@handle, text, engagement such as likes and views, and the URL when the user may want the full thread), group search results by theme, and note the bullish or bearish lean and where views are consensus or contrarian. For profiles, give follower count, bio, and notable recent activity. Keep browser session details private.

---

## Step 5: Diagnostics

If something isn't working, run:

```bash
opencli doctor
```

This checks daemon status, extension connectivity, and browser session health.

---

## Error Reference

| Error | Cause | Fix |
|-------|-------|-----|
| `Extension not connected` | Browser Bridge not installed/enabled | Install extension and enable it in Chrome |
| `No session` | Not logged into x.com | Login to x.com in Chrome |
| `CSRF token missing` | Cookie expired or page needs refresh | Refresh x.com in Chrome |
| Rate limited | Too many requests | Wait a few minutes, then retry |

---

## Reference Files

- `references/commands.md` — Complete read command reference with all flags, research workflows, and usage examples
- `references/schema.md` — Output format documentation and column definitions

Read the reference files when you need exact command syntax, research workflow patterns, or output details.

### Referencia: README.md

# twitter-reader

Read-only Twitter/X skill for financial research using [opencli](https://github.com/jackwener/opencli).

## What it does

Reads Twitter/X for financial research — searching market discussions, reading analyst tweets, tracking sentiment, and monitoring financial news. Capabilities include:

- **Home feed / timeline** — read your feed ("For You" or "Following")
- **Search** — find tweets by keyword with relevance or recency filters
- **Trending** — view trending topics for market themes
- **Bookmarks** — view your saved tweets
- **User tweets** — fetch a user's recent posts (chronological)
- **User profiles** — look up users, their followers, and following
- **Tweet threads & articles** — view specific threads and long-form articles
- **Notifications** — read your Twitter notifications

**This skill is read-only.** It does NOT support posting, liking, retweeting, replying, or any write operations.

## Authentication

No API keys needed — opencli reuses your existing Chrome browser session via the Browser Bridge extension. Just be logged into x.com in Chrome.

## Triggers

- "check my feed", "search Twitter for", "show my bookmarks"
- "what are people saying about AAPL", "market sentiment on Twitter"
- "look up @user", "who follows", "fintwit", "what's trending"
- Any mention of Twitter/X in context of financial news or market research

## Platform

Works on **Claude Code** and other CLI-based agents. Does **not** work on Claude.ai — the sandbox restricts network access and binaries required by opencli.

## Setup

```bash
# Choose finance-social-readers when prompted.
npx plugins add himself65/finance-skills

# Or install just this skill
npx skills add himself65/finance-skills --skill twitter-reader
```

See the [main README](../../../../README.md) for more installation options.

## Prerequisites

- Node.js >= 20 (for `npm install -g @jackwener/opencli`)
- Chrome with the [Browser Bridge extension](https://github.com/jackwener/opencli/releases) installed (load unpacked from `chrome://extensions` in Developer mode)
- Logged into x.com in Chrome

## Reference files

- `references/commands.md` — Complete read command reference with all flags, research workflows, and usage examples
- `references/schema.md` — Output format documentation and column definitions

### Referencia: references/commands.md

# opencli Twitter Command Reference (Read-Only)

Complete read-only reference for Twitter commands in [opencli](https://github.com/jackwener/opencli), scoped to financial research use cases.

Install: `npm install -g @jackwener/opencli`

**This skill is read-only.** Write operations (post, like, retweet, reply, quote, follow, delete) are NOT supported in this finance skill.

---

## Setup

opencli authenticates via your existing Chrome browser session — no API keys or credentials needed.

**Requirements:**
1. Node.js >= 20 (or Bun >= 1.0)
2. Chrome with the Browser Bridge extension installed
3. Logged into x.com in Chrome

**Install the Browser Bridge extension:**
1. Download `opencli-extension-v{version}.zip` from the [GitHub Releases page](https://github.com/jackwener/opencli/releases)
2. Unzip it, open `chrome://extensions`, enable **Developer mode**
3. Click **Load unpacked** and select the unzipped folder

**Verify setup:**
```bash
opencli doctor
```

This auto-starts the daemon, verifies extension connectivity, and checks browser session health.

---

## Read Operations

### Timeline (Home Feed)

```bash
opencli twitter timeline                          # "For You" feed (default, limit 20)
opencli twitter timeline --type following         # "Following" tab (chronological)
opencli twitter timeline --type for-you           # "For You" tab (algorithmic, explicit)
opencli twitter timeline --limit 50               # Limit count
opencli twitter timeline -f json                  # JSON output
opencli twitter timeline -f yaml                  # YAML output
```

**Flags:** `--type` (`for-you` | `following`, default `for-you`), `--limit` (default 20).

### Search

```bash
opencli twitter search "keyword"                  # Basic search (top results, limit 15)
opencli twitter search "AI agent" --filter live --limit 50    # Latest tweets
opencli twitter search "topic" -f json            # JSON output
opencli twitter search "topic" -f csv             # CSV output

# Financial research examples
opencli twitter search "$AAPL earnings" --filter live --limit 20 -f json
opencli twitter search "Fed rate decision" --limit 20 -f yaml
opencli twitter search "market crash" --filter live --limit 15 -f json
```

**Flags:** `--filter` (`top` | `live`, default `top`), `--limit` (default 15).

### Trending Topics

```bash
opencli twitter trending                          # Top 20 trending topics (default)
opencli twitter trending --limit 10               # Limit count
opencli twitter trending -f json                  # JSON output
```

### Bookmarks

```bash
opencli twitter bookmarks                         # View bookmarked tweets
opencli twitter bookmarks --limit 30              # Limit count
opencli twitter bookmarks -f json                 # JSON output
```

### Thread / Tweet Detail

```bash
opencli twitter thread TWEET_ID                   # View tweet thread (default limit 50)
opencli twitter thread TWEET_ID --limit 20        # Limit replies
opencli twitter thread TWEET_ID -f json           # JSON output
```

### Twitter Articles

```bash
opencli twitter article TWEET_ID                  # View long-form article
opencli twitter article TWEET_ID -f json          # JSON output
```

### User Data

```bash
opencli twitter profile                           # Defaults to logged-in user
opencli twitter profile elonmusk                  # Look up a specific user
opencli twitter profile elonmusk -f json          # JSON output
opencli twitter followers elonmusk                # List followers (default limit 50)
opencli twitter followers elonmusk --limit 100    # Custom limit
opencli twitter following elonmusk                # List following (default limit 50)
```

### Recent Tweets from a User

Fetches a user's most recent posts (chronological, excludes pinned). Added in opencli 1.7.6.

```bash
opencli twitter tweets elonmusk                   # Most recent tweets (default limit 20)
opencli twitter tweets elonmusk --limit 50        # More tweets
opencli twitter tweets jimcramer -f json          # JSON output
```

**Columns:** `author`, `created_at`, `is_retweet`, `text`, `likes`, `retweets`, `replies`, `views`, `url`, `has_media`, `media_urls`.

### Notifications

```bash
opencli twitter notifications                     # View notifications
opencli twitter notifications -f json             # JSON output
```

---

## Output Formats

All commands support the `-f` / `--format` flag:

| Format | Flag | Description |
|---|---|---|
| Table | `-f table` (default) | Rich CLI table with bold headers, word wrapping, footer with count/elapsed time |
| JSON | `-f json` | Pretty-printed JSON (2-space indent) |
| YAML | `-f yaml` | Structured YAML |
| Markdown | `-f md` | Pipe-delimited markdown tables |
| CSV | `-f csv` | Comma-separated values with proper quoting/escaping |

### Output columns by command

| Command | Columns |
|---|---|
| `timeline`, `search`, `thread` | `id`, `author`, `text`, `likes`, `retweets`, `replies`, `views`, `created_at`, `url`, `has_media`, `media_urls` |
| `tweets` | `author`, `created_at`, `is_retweet`, `text`, `likes`, `retweets`, `replies`, `views`, `url`, `has_media`, `media_urls` |
| `bookmarks` | `author`, `text`, `likes`, `retweets`, `bookmarks`, `url` |
| `trending` | `rank`, `topic`, `tweets`, `category` |
| `profile` | `screen_name`, `name`, `bio`, `location`, `url`, `followers`, `following`, `tweets`, `likes`, `verified`, `created_at` |
| `followers`, `following` | `screen_name`, `name`, `bio`, `followers` |
| `notifications` | `id`, `action`, `author`, `text`, `url` |

**Note:** The `has_media` and `media_urls` columns were added in opencli 1.7.7.

---

## Financial Research Workflows

### Search for earnings sentiment

```bash
opencli twitter search "$AAPL earnings" --filter live --limit 20 -f json
opencli twitter search "$TSLA delivery numbers" --filter live --limit 15 -f json
```

### Monitor fintwit for a ticker

```bash
opencli twitter search "$NVDA" --filter live --limit 30 -f json
opencli twitter search "$SPY puts" --filter live --limit 20 -f json
```

### Track analyst commentary

```bash
# Check trending topics for market themes
opencli twitter trending --limit 20 -f json

# Search for specific analyst takes
opencli twitter search "price target AAPL" --filter live --limit 15 -f json

# Read recent tweets from a specific analyst or fintwit account
opencli twitter tweets jimcramer --limit 30 -f json
opencli twitter tweets elerianm --limit 20 -f json
```

### Macro / Fed watching

```bash
opencli twitter search "Fed rate decision" --filter live --limit 20 -f json
opencli twitter search "CPI report" --filter live --limit 15 -f json
opencli twitter search "inflation data" --filter live --limit 20 -f yaml
```

### Daily market reading workflow

```bash
# Check trending topics
opencli twitter trending --limit 10 -f json

# Read your feed
opencli twitter timeline --type following --limit 30 -f json

# Check bookmarks
opencli twitter bookmarks --limit 20 -f json

# Search for market outlook
opencli twitter search "market outlook" --filter live --limit 30 -f json
```

### Export for analysis

```bash
# CSV for spreadsheet analysis
opencli twitter search "AI stocks" --limit 50 -f csv > ai_stocks.csv

# JSON for programmatic processing
opencli twitter search "earnings beat" --limit 30 -f json > earnings.json
```

---

## Error Reference

| Error | Cause | Fix |
|-------|-------|-----|
| `Extension not connected` | Browser Bridge not installed | Install the Browser Bridge Chrome extension |
| `Daemon not running` | opencli daemon not started | Run `opencli doctor` to auto-start |
| `No session for twitter.com` | Not logged into x.com | Login to x.com in Chrome |
| `CSRF token missing` | Cookie expired | Refresh x.com in Chrome |
| Rate limited | Too many requests | Wait a few minutes, then retry |

---

## Limitations

- **Read-only in this skill** — write operations are not supported for finance use
- **No DMs** — direct messages are not exposed via read commands in this skill
- **Requires Chrome** — opencli uses Chrome's Browser Bridge; other browsers are not supported
- **Single browser profile** — uses the active Chrome profile's session

---

## Best Practices

- **Keep request volumes low** — use `--limit 20` instead of `--limit 500`
- **Use `opencli doctor`** before your first command in a session to verify connectivity
- **Use `-f json`** for programmatic processing and LLM context
- **Use `-f csv`** when the user wants to analyze data in a spreadsheet
- **Prefer `--filter live`** for time-sensitive financial searches (earnings, breaking news)

### Referencia: references/schema.md

# Output Format Reference

opencli supports multiple output formats for all Twitter commands via the `-f` / `--format` flag.

## Formats

| Format | Flag | Description |
|---|---|---|
| Table | `-f table` | Default in a TTY. Rich CLI table with bold headers, word wrapping, and a footer showing row count and elapsed time |
| JSON | `-f json` | Pretty-printed JSON array with 2-space indent — preferred for agents |
| YAML | `-f yaml` | Default in non-TTY. Structured YAML with 120-char line width |
| Plain | `-f plain` | Prints a single primary field (for chat-style commands) |
| Markdown | `-f md` | Pipe-delimited markdown table |
| CSV | `-f csv` | Comma-separated values with proper quoting and escaping |

## Column Definitions

### Tweet list columns (`timeline`, `search`, `thread`)

| Column | Type | Description |
|---|---|---|
| `id` | string | Tweet ID |
| `author` | string | @handle of the tweet author |
| `text` | string | Tweet text content |
| `likes` | number | Like count |
| `retweets` | number | Retweet count |
| `replies` | number | Reply count |
| `views` | number | View count |
| `created_at` | string | Timestamp of the tweet |
| `url` | string | Direct URL to the tweet |
| `has_media` | boolean | Whether the tweet contains media (images/video) — added in 1.7.7 |
| `media_urls` | string[] | URLs of attached media — added in 1.7.7 |

### Per-user tweets columns (`tweets`)

Same as tweet-list columns above, plus:

| Column | Type | Description |
|---|---|---|
| `is_retweet` | boolean | Whether the post is a retweet of another author |

`tweets` command returns a user's most recent posts in chronological order, excluding the pinned tweet. Added in opencli 1.7.6.

### Bookmark columns (`bookmarks`)

| Column | Type | Description |
|---|---|---|
| `author` | string | @handle of the tweet author |
| `text` | string | Tweet text content |
| `likes` | number | Like count |
| `retweets` | number | Retweet count |
| `bookmarks` | number | Bookmark count |
| `url` | string | Direct URL to the tweet |

### Trending columns (`trending`)

| Column | Type | Description |
|---|---|---|
| `rank` | number | Trending rank position |
| `topic` | string | Trending topic or hashtag |
| `tweets` | number | Number of tweets about the topic |
| `category` | string | Category label from X (e.g., "Business", "Sports") |

### Profile columns (`profile`)

| Column | Type | Description |
|---|---|---|
| `screen_name` | string | @handle |
| `name` | string | Display name |
| `bio` | string | Profile bio/description |
| `location` | string | User-provided location |
| `url` | string | User's linked website |
| `followers` | number | Follower count |
| `following` | number | Following count |
| `tweets` | number | Total tweets |
| `likes` | number | Total likes |
| `verified` | boolean | Verification status |
| `created_at` | string | Account creation timestamp |

### User list columns (`followers`, `following`)

| Column | Type | Description |
|---|---|---|
| `screen_name` | string | @handle |
| `name` | string | Display name |
| `bio` | string | Profile bio/description |
| `followers` | number | Follower count |

### Notification columns (`notifications`)

| Column | Type | Description |
|---|---|---|
| `id` | string | Notification ID |
| `action` | string | Action type (like, retweet, follow, reply, mention, etc.) |
| `author` | string | @handle of the account that triggered the notification |
| `text` | string | Notification text / related tweet text |
| `url` | string | Direct URL to the notification's source |

## JSON Example

```json
[
  {
    "id": "1234567890",
    "author": "@exampleuser",
    "text": "Breaking: $AAPL earnings beat expectations...",
    "likes": 1523,
    "retweets": 240,
    "replies": 88,
    "views": 89000,
    "created_at": "2026-03-26T14:30:00Z",
    "url": "https://x.com/exampleuser/status/1234567890",
    "has_media": true,
    "media_urls": ["https://pbs.twimg.com/media/abc123.jpg"]
  }
]
```

## Notes

- Table format includes a footer with total row count and elapsed time
- JSON output is a flat array (no envelope wrapper)
- CSV properly escapes commas and quotes within fields
- Markdown format is suitable for pasting into documents or LLM context
- For programmatic use by agents, prefer `-f json`


---

## SKILL: xlsx-author

- Fuente: `anthropics/financial-services` → `plugins/agent-plugins/earnings-reviewer/skills/xlsx-author` (Apache-2.0)
- Cuándo usarla: Produce a .xlsx file on disk (headless) instead of driving a live Excel workbook — for managed-agent sessions with no open Office app.

# xlsx-author

Use this skill when running **headless** (managed-agent / CMA mode) and you need to deliver an Excel workbook as a **file artifact** rather than editing a live workbook via `mcp__office__excel_*`.

## Output contract

- Write to `./out/<name>.xlsx`. Create `./out/` if it does not exist.
- Return the relative path in your final message so the orchestration layer can collect it.

## How to build the workbook

Write a short Python script and run it with Bash. Use `openpyxl`:

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

wb = Workbook()
ws = wb.active; ws.title = "Inputs"
ws["B2"] = "Revenue"; ws["C2"] = 1_250_000_000
ws["C2"].font = Font(color="0000FF")           # blue = hardcoded input
calc = wb.create_sheet("DCF")
calc["C5"] = "=Inputs!C2*(1+Inputs!C3)"        # black = formula
wb.save("./out/model.xlsx")
```

## Conventions (mirror `audit-xls`)

- **Blue / black / green.** Blue = hardcoded input, black = formula, green = link to another sheet/file.
- **No hardcodes in calc cells.** Every calculation cell is a formula; every input lives on an Inputs tab.
- **Named ranges** for any value referenced from a deck or memo.
- **Balance checks.** Include a Checks tab that ties (BS balances, CF ties to cash, etc.) and surfaces TRUE/FALSE.
- **One model per file.** Do not append to an existing workbook unless explicitly asked.

## When NOT to use

If `mcp__office__excel_*` tools are available (Cowork plugin mode), use those instead — they drive the user's live workbook with review checkpoints. This skill is the file-producing fallback for headless runs.


---

## SKILL: yc-reader

- Fuente: `himself65/finance-skills` → `plugins/social-readers/skills/yc-reader` (MIT)
- Cuándo usarla: >

# Y Combinator Reader (Read-Only)

If your host has not already executed the shell probes below (for example, in Codex), run the commands inside the `!` wrappers with its shell tool before choosing a setup path. Use the actual output; if shell access is unavailable, report that limitation.

Fetches Y Combinator company data from the [yc-oss/api](https://github.com/yc-oss/api), an unofficial open-source API that indexes all publicly launched YC companies. The data is sourced from YC's Algolia search index and updated daily via GitHub Actions.

**This is a read-only data source.** It provides company profiles, batch listings, industry/tag breakdowns, hiring status, and diversity data. No write operations exist — the API serves static JSON files.

**No authentication required.** The API is public and free. Just use `curl` to fetch JSON endpoints.

---

## Step 1: Verify Prerequisites

This skill only needs `curl` (to fetch data) and `jq` (to parse/filter JSON). Both are pre-installed on most systems.

```
!`(command -v curl > /dev/null && echo "CURL_OK" || echo "CURL_MISSING") && (command -v jq > /dev/null && echo "JQ_OK" || echo "JQ_MISSING")`
```

If `JQ_MISSING`, install it:

```bash
# macOS
brew install jq

# Linux (Debian/Ubuntu)
sudo apt-get install jq
```

If `jq` is unavailable, you can still fetch raw JSON with `curl` and parse it inline with Python or other tools — but `jq` makes filtering much easier.

---

## Step 2: Identify What the User Needs

Match the user's request to the appropriate endpoint. See `references/api_reference.md` for full details.

| User Request | Endpoint | Notes |
|---|---|---|
| Overall YC stats | `meta.json` | Company count, batch list, industry/tag lists |
| All companies | `companies/all.json` | Full dataset (~5,700 companies) — large response |
| Top companies | `companies/top.json` | ~91 top-performing YC companies |
| Companies hiring | `companies/hiring.json` | ~1,400 currently hiring |
| Non-profit companies | `companies/nonprofit.json` | YC-backed non-profits |
| Diversity data | `companies/black-founded.json`, `hispanic-latino-founded.json`, `women-founded.json` | Founder diversity |
| Specific batch | `batches/{batch-name}.json` | e.g., `winter-2026.json`, `spring-2026.json`, `fall-2025.json` |
| Single company profile | `batches/{batch-name}/{slug}.json` | e.g., `batches/summer-2009/stripe.json`, `batches/winter-2009/airbnb.json` |
| By industry | `industries/{industry}.json` | e.g., `fintech.json`, `healthcare.json` |
| By tag | `tags/{tag}.json` | e.g., `ai.json`, `developer-tools.json` |

### Batch name format

Batches use `{season}-{year}` format: `winter-2026`, `spring-2026`, `summer-2026`, `fall-2025`. Older batches follow the same pattern back to `summer-2005`. The short form (`w09`, `s21`) also works for the per-company endpoint.

### Industry and tag name format

Use lowercase with hyphens for multi-word names: `real-estate`, `developer-tools`, `machine-learning`.

---

## Step 3: Execute the Request

### Base URL

```
https://yc-oss.github.io/api/
```

### General pattern

```bash
# Fetch and pretty-print
curl -s https://yc-oss.github.io/api/companies/top.json | jq .

# Count companies in a result
curl -s https://yc-oss.github.io/api/batches/winter-2025.json | jq length

# Filter by field (e.g., hiring companies in a batch)
curl -s https://yc-oss.github.io/api/batches/winter-2025.json | jq '[.[] | select(.isHiring == true)]'

# Extract specific fields
curl -s https://yc-oss.github.io/api/companies/top.json | jq '.[] | {name, one_liner, batch, team_size, website}'

# Search by name (case-insensitive)
curl -s https://yc-oss.github.io/api/companies/all.json | jq '[.[] | select(.name | test("stripe"; "i"))]'
```

### Key rules

1. **Use `-s` flag** with curl to suppress progress output
2. **Pipe through `jq`** for readable output and filtering
3. **Avoid fetching `companies/all.json` unless necessary** — it's a large response (~5,700 companies). Prefer more specific endpoints (batches, industries, tags) when possible
4. **Use `jq` select/filter** to narrow results client-side when the API doesn't have a specific endpoint for what the user wants
5. **Batch names are lowercase with hyphens** — `winter-2025` not `Winter 2025` or `W25`
6. **Tag and industry names are lowercase with hyphens** — `developer-tools` not `Developer Tools`

### Common jq filters

| Filter | Purpose |
|---|---|
| `jq length` | Count results |
| `jq '.[0]'` | First company |
| `jq '.[:10]'` | First 10 companies |
| `jq '[.[] \| select(.isHiring == true)]'` | Only hiring companies |
| `jq '[.[] \| select(.status == "Active")]'` | Only active companies |
| `jq '[.[] \| select(.team_size > 100)]'` | Companies with 100+ employees |
| `jq '.[] \| {name, one_liner, batch, website}'` | Select specific fields |
| `jq '[.[] \| select(.name \| test("query"; "i"))]'` | Search by name |
| `jq 'sort_by(-.team_size) \| .[:10]'` | Top 10 by team size |

---

## Step 4: Present the Results

Summarize rather than dump JSON. For each company, give the name, one-liner, batch, team size, status, hiring status (a growth signal), and website. For a batch, lead with its size and notable companies; for an industry or tag, the count and which companies are top or hiring; for research questions, aggregate stats such as counts, common industries, and team-size distribution. Mention that the dataset refreshes daily.

---

## Step 5: Diagnostics

If a request fails:

| Error | Cause | Fix |
|-------|-------|-----|
| `404 Not Found` | Invalid batch, industry, or tag name | Check `meta.json` for valid names |
| Empty array `[]` | No companies match the query | Broaden the search or check spelling |
| `curl: Could not resolve host` | No internet connection | Check network connectivity |
| Large/slow response | Fetching `companies/all.json` (5,700+ entries) | Use a more specific endpoint or add `jq` filters |

To discover valid batch, industry, and tag names:

```bash
# List all batches
curl -s https://yc-oss.github.io/api/meta.json | jq '.batches[].name'

# List all industries
curl -s https://yc-oss.github.io/api/meta.json | jq '.industries[].name'

# List all tags (there are 333+)
curl -s https://yc-oss.github.io/api/meta.json | jq '.tags[].name'
```

---

## Reference Files

- `references/api_reference.md` — Complete endpoint reference with company schema, all endpoint URLs, and research workflow examples

Read the reference file when you need the exact company field schema, valid batch/industry/tag names, or detailed research workflow patterns.

### Referencia: README.md

# yc-reader

Read-only Y Combinator company data skill using the [yc-oss/api](https://github.com/yc-oss/api).

## What it does

Fetches Y Combinator company data for startup and venture research — company profiles, batch listings, industry/tag breakdowns, hiring status, and diversity data. Capabilities include:

- **Company collections** — top companies, all companies, currently hiring, non-profits, diversity data
- **Batch lookup** — companies by YC batch (e.g., Winter 2025, Summer 2024)
- **Industry filter** — companies by industry (fintech, healthcare, B2B, etc.)
- **Tag filter** — companies by tag (AI, developer tools, SaaS, climate, etc.)
- **Metadata** — overall YC stats, valid batch/industry/tag names
- **Client-side search** — find companies by name or description via jq filters

**This is a read-only data source.** The API serves static JSON files — no write operations exist.

## Authentication

None required. The API is public and free — just `curl` the endpoints.

## Triggers

- "YC companies in fintech", "top Y Combinator companies", "latest YC batch"
- "YC startups hiring", "find YC companies tagged AI", "W25 batch"
- "Y Combinator portfolio", "startup research", "which YC companies do X"
- Any mention of Y Combinator or YC in context of startup/venture research

## Platform

Works on **Claude Code** and other CLI-based agents. Does **not** work on Claude.ai — the sandbox restricts network access required for API calls.

## Setup

```bash
# Choose finance-social-readers when prompted.
npx plugins add himself65/finance-skills

# Or install just this skill
npx skills add himself65/finance-skills --skill yc-reader
```

See the [main README](../../../../README.md) for more installation options.

## Prerequisites

- `curl` (pre-installed on macOS and most Linux)
- `jq` (for JSON filtering — `brew install jq` or `apt-get install jq`)

## Reference files

- `references/api_reference.md` — Complete endpoint reference with company schema, all URLs, and research workflow examples

### Referencia: references/api_reference.md

# yc-oss API Reference

Complete reference for the [yc-oss/api](https://github.com/yc-oss/api), an unofficial open-source API indexing all publicly launched Y Combinator companies.

**Base URL:** `https://yc-oss.github.io/api/`

**Authentication:** None required — all endpoints are public.

**Format:** Static JSON files, updated daily via GitHub Actions.

---

## Company Schema

Each company object contains:

| Field | Type | Description |
|---|---|---|
| `id` | number | Internal ID |
| `name` | string | Company name |
| `slug` | string | URL-safe identifier |
| `former_names` | string[] | Previous company names |
| `small_logo_thumb_url` | string | Logo thumbnail URL |
| `website` | string | Company website URL |
| `all_locations` | string | Comma-separated locations |
| `long_description` | string | Full company description |
| `one_liner` | string | One-line summary |
| `team_size` | number | Current team size |
| `industry` | string | Primary industry |
| `subindustry` | string | Sub-industry classification |
| `launched_at` | number | Unix timestamp of YC launch |
| `tags` | string[] | Category tags |
| `tags_highlighted` | string[] | Featured tags |
| `top_company` | boolean | Whether it's a top YC company |
| `isHiring` | boolean | Currently hiring |
| `nonprofit` | boolean | Non-profit organization |
| `batch` | string | YC batch (e.g., "Winter 2026", "Summer 2009") |
| `status` | string | Company status ("Active", "Acquired", "Inactive", "Public") |
| `industries` | string[] | All industry classifications |
| `regions` | string[] | Geographic regions |
| `stage` | string | Company stage |
| `url` | string | YC profile URL (ycombinator.com) |
| `api` | string | API endpoint URL for this company |

---

## Endpoints

### Metadata

```bash
curl -s https://yc-oss.github.io/api/meta.json | jq .
```

Returns overall statistics: total company count, list of all batches (with counts), all industries (with counts), and all tags (with counts). Use this to discover valid batch/industry/tag names.

### Company Collections

| Endpoint | Description | Approx. Count |
|---|---|---|
| `companies/all.json` | All launched companies | ~5,700 |
| `companies/top.json` | Top-performing companies | ~91 |
| `companies/hiring.json` | Currently hiring | ~1,400 |
| `companies/nonprofit.json` | Non-profit organizations | ~42 |
| `companies/black-founded.json` | Black-founded companies | varies |
| `companies/hispanic-latino-founded.json` | Hispanic/Latino-founded | varies |
| `companies/women-founded.json` | Women-founded companies | varies |

```bash
# Top YC companies
curl -s https://yc-oss.github.io/api/companies/top.json | jq '.[:5] | .[] | {name, one_liner, batch, team_size}'

# Currently hiring
curl -s https://yc-oss.github.io/api/companies/hiring.json | jq length
```

### Batches

Pattern: `batches/{season}-{year}.json`

Seasons: `winter`, `spring`, `summer`, `fall`

```bash
# Winter 2026 batch
curl -s https://yc-oss.github.io/api/batches/winter-2026.json | jq length

# Spring 2026 batch
curl -s https://yc-oss.github.io/api/batches/spring-2026.json | jq '.[:5] | .[] | {name, one_liner}'

# Fall 2025 batch
curl -s https://yc-oss.github.io/api/batches/fall-2025.json | jq .
```

Historical batches go back to `summer-2005`.

### Single company profile

Pattern: `batches/{batch-slug}/{company-slug}.json`

Both long (`winter-2009`) and short (`w09`) batch slugs work. Company slug is the same lowercase-hyphenated form used in the `slug` field.

```bash
# Airbnb profile
curl -s https://yc-oss.github.io/api/batches/winter-2009/airbnb.json | jq .

# Stripe profile
curl -s https://yc-oss.github.io/api/batches/summer-2009/stripe.json | jq '{name, one_liner, team_size, status}'
```

### Industries

Pattern: `industries/{industry-name}.json`

Use lowercase with hyphens for multi-word names.

**Notable industries:**

| Industry | Endpoint | Approx. Count |
|---|---|---|
| B2B | `industries/b2b.json` | ~2,876 |
| Consumer | `industries/consumer.json` | ~866 |
| Healthcare | `industries/healthcare.json` | ~656 |
| Fintech | `industries/fintech.json` | ~607 |
| Engineering/Product/Design | `industries/engineering-product-and-design.json` | ~585 |
| Real Estate & Construction | `industries/real-estate-and-construction.json` | ~138 |
| Government | `industries/government.json` | ~75 |
| Education | `industries/education.json` | ~240 |
| Infrastructure | `industries/infrastructure.json` | ~261 |

```bash
# Fintech companies
curl -s https://yc-oss.github.io/api/industries/fintech.json | jq '.[:10] | .[] | {name, one_liner, batch, isHiring}'

# Healthcare companies hiring
curl -s https://yc-oss.github.io/api/industries/healthcare.json | jq '[.[] | select(.isHiring == true)] | length'
```

### Tags

Pattern: `tags/{tag-name}.json`

Use lowercase with hyphens for multi-word names.

**Notable tags:**

| Tag | Endpoint | Approx. Count |
|---|---|---|
| SaaS | `tags/saas.json` | ~1,127 |
| Artificial Intelligence | `tags/artificial-intelligence.json` | ~908 |
| AI | `tags/ai.json` | ~772 |
| Developer Tools | `tags/developer-tools.json` | ~537 |
| Marketplace | `tags/marketplace.json` | ~347 |
| Open Source | `tags/open-source.json` | ~179 |
| Climate | `tags/climate.json` | ~142 |
| Crypto/Web3 | `tags/crypto-web3.json` | ~119 |
| Robotics | `tags/robotics.json` | ~78 |
| Automation | `tags/automation.json` | ~85 |

```bash
# AI-tagged companies
curl -s https://yc-oss.github.io/api/tags/ai.json | jq '.[:10] | .[] | {name, one_liner, batch}'

# Developer tools that are hiring
curl -s https://yc-oss.github.io/api/tags/developer-tools.json | jq '[.[] | select(.isHiring == true)] | .[:10] | .[] | {name, one_liner, website}'
```

---

## Research Workflows

### Analyze the latest YC batch

```bash
# Get batch companies
curl -s https://yc-oss.github.io/api/batches/winter-2026.json | jq length

# Summarize by industry
curl -s https://yc-oss.github.io/api/batches/winter-2026.json | jq 'group_by(.industry) | map({industry: .[0].industry, count: length}) | sort_by(-.count)'

# Find hiring companies in the batch
curl -s https://yc-oss.github.io/api/batches/winter-2026.json | jq '[.[] | select(.isHiring == true)] | .[] | {name, one_liner, website}'
```

### Find fintech/finance startups

```bash
# All fintech companies
curl -s https://yc-oss.github.io/api/industries/fintech.json | jq '.[:20] | .[] | {name, one_liner, batch, team_size, status}'

# Active fintech companies that are hiring
curl -s https://yc-oss.github.io/api/industries/fintech.json | jq '[.[] | select(.isHiring == true and .status == "Active")] | .[:15] | .[] | {name, one_liner, batch, team_size, website}'
```

### Track hiring trends (growth signal)

```bash
# Largest hiring companies
curl -s https://yc-oss.github.io/api/companies/hiring.json | jq 'sort_by(-.team_size) | .[:20] | .[] | {name, team_size, industry, batch}'

# Hiring companies in AI
curl -s https://yc-oss.github.io/api/tags/ai.json | jq '[.[] | select(.isHiring == true)] | sort_by(-.team_size) | .[:15] | .[] | {name, team_size, one_liner}'
```

### Search for a specific company

```bash
# Search by name (case-insensitive)
curl -s https://yc-oss.github.io/api/companies/all.json | jq '[.[] | select(.name | test("stripe"; "i"))]'

# Search in one-liners
curl -s https://yc-oss.github.io/api/companies/all.json | jq '[.[] | select(.one_liner | test("payment"; "i"))] | .[:10] | .[] | {name, one_liner, batch}'
```

### Top companies analysis

```bash
# Top companies with details
curl -s https://yc-oss.github.io/api/companies/top.json | jq '.[] | {name, one_liner, batch, team_size, status, industry}'

# Top companies by team size
curl -s https://yc-oss.github.io/api/companies/top.json | jq 'sort_by(-.team_size) | .[:10] | .[] | {name, team_size, batch}'
```

### Diversity data

```bash
# Women-founded companies in latest batch
curl -s https://yc-oss.github.io/api/companies/women-founded.json | jq '[.[] | select(.batch == "Winter 2026")] | .[] | {name, one_liner}'

# Count by diversity category
curl -s https://yc-oss.github.io/api/companies/black-founded.json | jq length
curl -s https://yc-oss.github.io/api/companies/women-founded.json | jq length
```

### Export for analysis

```bash
# CSV export (name, batch, industry, team_size, status)
curl -s https://yc-oss.github.io/api/companies/top.json | jq -r '.[] | [.name, .batch, .industry, .team_size, .status] | @csv' > yc_top.csv

# JSON subset for processing
curl -s https://yc-oss.github.io/api/industries/fintech.json | jq '[.[] | {name, one_liner, batch, team_size, website, isHiring}]' > fintech_yc.json
```

---

## Discovering Valid Names

When the user asks for a batch, industry, or tag that you're not sure about, query `meta.json`:

```bash
# List all batch names
curl -s https://yc-oss.github.io/api/meta.json | jq '[.batches[] | .name]'

# List all industry names
curl -s https://yc-oss.github.io/api/meta.json | jq '[.industries[] | .name]'

# List all tag names (333+)
curl -s https://yc-oss.github.io/api/meta.json | jq '[.tags[] | .name]'

# Search for a tag name
curl -s https://yc-oss.github.io/api/meta.json | jq '[.tags[] | select(.name | test("fintech"; "i"))]'
```

---

## Error Reference

| Error | Cause | Fix |
|-------|-------|-----|
| `404 Not Found` | Invalid endpoint name | Check `meta.json` for valid batch/industry/tag names |
| Empty array `[]` | No companies match filter | Broaden the jq filter or check spelling |
| Network error | No internet connection | Check connectivity |
| Large/slow response | `companies/all.json` is ~5,700 entries | Use specific endpoints (batch, industry, tag) or pipe through `jq '.[:N]'` to limit |

---

## Limitations

- **Read-only** — Static JSON files, no search API or query parameters
- **No founder details** — Company profiles don't include individual founder names or bios
- **No funding data** — Funding amounts, valuations, and investor details are not included
- **No revenue/financial data** — Only public metadata (team size, hiring status, industry)
- **Updated daily** — Data may be up to 24 hours behind YC's live directory
- **Publicly launched only** — Stealth companies not yet launched on YC are excluded


---

## SKILL: yfinance-data

- Fuente: `himself65/finance-skills` → `plugins/market-analysis/skills/yfinance-data` (MIT)
- Cuándo usarla: >

# yfinance Data Skill

If your host has not already executed the shell probes below (for example, in Codex), run the commands inside the `!` wrappers with its shell tool before choosing a setup path. Use the actual output; if shell access is unavailable, report that limitation.

Fetches financial and market data from Yahoo Finance using the [yfinance](https://github.com/ranaroussi/yfinance) Python library.

**Important**: yfinance is not affiliated with Yahoo, Inc. Data is for research and educational purposes.

---

## Step 1: Ensure yfinance Is Available

**Current environment status:**

```
!`python3 -c "exec('try:\n import yfinance\n print(\'yfinance \' + yfinance.__version__ + \' installed\')\nexcept Exception:\n print(\'YFINANCE_NOT_INSTALLED\')')"`
```

If `YFINANCE_NOT_INSTALLED`, install it before running any code:

```python
import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "yfinance"])
```

If yfinance is already installed, skip the install step and proceed directly.

---

## Step 2: Identify What the User Needs

Match the user's request to one or more data categories below, then use the corresponding code from `references/api_reference.md`.

| User Request | Data Category | Primary Method |
|---|---|---|
| Stock price, quote | Current price | `ticker.info` or `ticker.fast_info` |
| Price history, chart data | Historical OHLCV | `ticker.history()` or `yf.download()` |
| Balance sheet | Financial statements | `ticker.balance_sheet` |
| Income statement, revenue | Financial statements | `ticker.income_stmt` |
| Cash flow | Financial statements | `ticker.cashflow` |
| Dividends | Corporate actions | `ticker.dividends` |
| Stock splits | Corporate actions | `ticker.splits` |
| Options chain, calls, puts | Options data | `ticker.option_chain()` |
| Earnings, EPS | Analysis | `ticker.earnings_history` |
| Analyst price targets | Analysis | `ticker.analyst_price_targets` |
| Recommendations, ratings | Analysis | `ticker.recommendations` |
| Upgrades/downgrades | Analysis | `ticker.upgrades_downgrades` |
| Institutional holders | Ownership | `ticker.institutional_holders` |
| Insider transactions | Ownership | `ticker.insider_transactions` |
| Company overview, sector | General info | `ticker.info` |
| Compare multiple stocks | Bulk download | `yf.download()` |
| Screen/filter stocks | Screener | `yf.screen()` + `yf.EquityQuery` |
| Sector/industry data | Market data | `yf.Sector` / `yf.Industry` |
| News | News | `ticker.news` |

---

## Step 3: Write and Execute the Code

### General pattern

```python
import yfinance as yf

ticker = yf.Ticker("AAPL")
# ... use the appropriate method from the reference
```

### Key rules

1. **Always wrap in try/except** — Yahoo Finance may rate-limit or return empty data
2. **Use `yf.download()` for multi-ticker comparisons** — it's faster with multi-threading
3. **For options, list expiration dates first** with `ticker.options` before calling `ticker.option_chain(date)`
4. **For quarterly data**, use `quarterly_` prefix: `ticker.quarterly_income_stmt`, `ticker.quarterly_balance_sheet`, `ticker.quarterly_cashflow`
5. **For large date ranges**, be mindful of intraday limits — 1m data only goes back ~7 days, 1h data ~730 days
6. **Print DataFrames clearly** — use `.to_string()` or `.to_markdown()` for readability, or select key columns
7. **Timezone handling** — yfinance returns tz-aware datetime indices (e.g., `America/New_York`). When comparing dates, always use `pd.Timestamp(..., tz=...)` or strip timezones with `.tz_localize(None)`. See the reference file for details.

### Valid periods and intervals

| Periods | `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max` |
|---|---|
| **Intervals** | `1m`, `2m`, `5m`, `15m`, `30m`, `60m`, `90m`, `1h`, `1d`, `5d`, `1wk`, `1mo`, `3mo` |

---

## Step 4: Present the Data

Answer with the numbers the user asked for first, then the supporting table (markdown, or a trimmed DataFrame with the key columns). Call out anything notable in the data — an earnings beat or miss, unusual volume, a dividend change — and add context such as sector averages, historical ranges, or analyst consensus where it changes how the numbers read. If the user wants a chart, pair the data with a visualization.

---

## Reference Files

- `references/api_reference.md` — Complete yfinance API reference with code examples for every data category

Read the reference file when you need exact method signatures or edge case handling.

### Referencia: README.md

# yfinance-data

Fetch financial and market data using the [yfinance](https://github.com/ranaroussi/yfinance) Python library.

## What it does

Retrieves a wide range of financial data from Yahoo Finance, including:

- **Current prices & quotes** — real-time stock prices, market cap, P/E
- **Historical OHLCV** — price history with configurable period and interval
- **Financial statements** — balance sheet, income statement, cash flow (annual & quarterly)
- **Corporate actions** — dividends, stock splits
- **Options data** — full options chains with greeks
- **Analysis** — earnings history, analyst price targets, recommendations, upgrades/downgrades
- **Ownership** — institutional holders, insider transactions
- **Screener** — filter stocks using `yf.screen()` and `yf.EquityQuery`

> **Note**: yfinance is not affiliated with Yahoo, Inc. Data is for research and educational purposes.

## Triggers

- Any mention of a ticker symbol (AAPL, MSFT, TSLA, etc.)
- "what's the price of", "get me the financials", "show earnings"
- "options chain", "dividend history", "balance sheet", "income statement"
- "analyst targets", "compare stocks", "screen for stocks"

## Prerequisites

- Python 3.8+
- The skill auto-installs `yfinance` via pip if not already present

## Platform

Works on **all platforms** (Claude Code, Claude.ai with code execution, etc.).

## Setup

```bash
# Choose finance-market-analysis when prompted.
npx plugins add himself65/finance-skills

# Or install just this skill
npx skills add himself65/finance-skills --skill yfinance-data
```

See the [main README](../../../../README.md) for more installation options.

## Reference files

- `references/api_reference.md` — Complete yfinance API reference with code examples for every data category

### Referencia: references/api_reference.md

# yfinance API Reference

Complete reference for all yfinance data access methods.

## Installation

```python
pip install yfinance
```

Requires Python 3.8+. Dependencies (pandas, requests, etc.) are installed automatically.

---

## Ticker Object

The primary interface for single-stock data.

```python
import yfinance as yf
ticker = yf.Ticker("AAPL")
```

---

## Historical Price Data

### `ticker.history()`

Returns a DataFrame with columns: Open, High, Low, Close, Volume, Dividends, Stock Splits.

```python
# Default: 1 month of daily data
hist = ticker.history(period="1mo")

# Specific date range
hist = ticker.history(start="2023-01-01", end="2023-12-31")

# Weekly data for 1 year
hist = ticker.history(period="1y", interval="1wk")

# Intraday 5-minute bars for last 5 days
hist = ticker.history(period="5d", interval="5m")

# Include pre/post market data
hist = ticker.history(period="5d", prepost=True)

# Repair price anomalies
hist = ticker.history(period="1mo", repair=True)
```

**Valid periods**: `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`
**Valid intervals**: `1m`, `2m`, `5m`, `15m`, `30m`, `60m`, `90m`, `1h`, `1d`, `5d`, `1wk`, `1mo`, `3mo`

**Intraday limits**:
- 1m: last ~7 days
- 2m/5m/15m/30m: last ~60 days
- 60m/90m/1h: last ~730 days

### `yf.download()` — Bulk Download

Efficient multi-threaded download for multiple tickers.

```python
data = yf.download(
    tickers="AAPL MSFT GOOGL AMZN",  # space or comma separated
    start="2023-01-01",
    end="2024-01-01",
    interval="1d",
    group_by="ticker",    # or "column" (default)
    auto_adjust=True,     # adjust for splits and dividends
    threads=True,         # multi-threading
    progress=True         # show progress bar
)

# Access a specific ticker
apple_close = data["AAPL"]["Close"]

# Download with dividends and splits
data = yf.download(["AAPL", "MSFT"], period="1y", actions=True)

# Additional options
data = yf.download(
    tickers=["TSLA", "NVDA"],
    period="6mo",
    interval="1h",
    repair=True,       # fix price anomalies
    keepna=False,      # remove NaN rows
    rounding=True,     # round to 2 decimals
    timeout=10         # request timeout seconds
)
```

---

## Company Info

### `ticker.info`

Returns a dictionary with company details, financials, and market data.

```python
info = ticker.info

# Common fields
info['shortName']          # Company name
info['sector']             # e.g., "Technology"
info['industry']           # e.g., "Consumer Electronics"
info['marketCap']          # Market capitalization
info['currentPrice']       # Current stock price
info['previousClose']      # Previous close price
info['trailingPE']         # Trailing P/E ratio
info['forwardPE']          # Forward P/E ratio
info['dividendYield']      # Dividend yield
info['beta']               # Beta
info['fiftyTwoWeekHigh']   # 52-week high
info['fiftyTwoWeekLow']    # 52-week low
info['averageVolume']      # Average volume
info['longBusinessSummary'] # Company description
```

### `ticker.fast_info`

Lightweight subset for quick price lookups (faster than `.info`).

```python
fi = ticker.fast_info
fi['lastPrice']
fi['marketCap']
fi['fiftyDayAverage']
fi['twoHundredDayAverage']
```

---

## Financial Statements

All return pandas DataFrames. Use `quarterly_` prefix for quarterly data.

```python
# Annual
ticker.income_stmt          # Income statement
ticker.balance_sheet        # Balance sheet
ticker.cashflow             # Cash flow statement

# Quarterly
ticker.quarterly_income_stmt
ticker.quarterly_balance_sheet
ticker.quarterly_cashflow
```

---

## Corporate Actions

```python
ticker.dividends            # Series of dividend payments
ticker.splits               # Series of stock splits
ticker.actions              # DataFrame with both dividends and splits
ticker.capital_gains        # Capital gains (for mutual funds/ETFs)
```

---

## Options

```python
# List available expiration dates
expirations = ticker.options   # tuple of date strings

# Get option chain for a specific expiration
opt = ticker.option_chain("2024-06-21")

# Calls and puts are separate DataFrames
calls = opt.calls
puts = opt.puts

# Key columns:
# strike, lastPrice, bid, ask, volume, openInterest, impliedVolatility,
# inTheMoney, contractSymbol, lastTradeDate, change, percentChange
```

---

## Analysis & Estimates

```python
# Analyst price targets
ticker.analyst_price_targets
# Returns dict: current, low, high, mean, median

# Recommendations (buy/hold/sell counts by period)
ticker.recommendations

# Upgrades and downgrades history
ticker.upgrades_downgrades
# Columns: firm, toGrade, fromGrade, action

# Earnings estimates
ticker.earnings_estimate
# Columns: numberOfAnalysts, avg, low, high, yearAgoEps, growth
# Index: 0q (current quarter), +1q, 0y, +1y

# Revenue estimates
ticker.revenue_estimate

# EPS trend
ticker.eps_trend

# EPS revisions
ticker.eps_revisions

# Growth estimates
ticker.growth_estimates

# Earnings history (actual vs estimate)
ticker.earnings_history
# Columns: epsEstimate, epsActual, epsDifference, surprisePercent

# Sustainability / ESG scores
ticker.sustainability
```

---

## Ownership

```python
# Major holders summary
ticker.major_holders

# Top institutional holders
ticker.institutional_holders
# Columns: Holder, Shares, Date Reported, % Out, Value

# Mutual fund holders
ticker.mutualfund_holders

# Insider transactions
ticker.insider_transactions

# Insider roster
ticker.insider_roster_holders

# Shares outstanding over time
ticker.get_shares_full(start="2023-01-01", end="2023-12-31")
```

---

## Calendar & Events

```python
ticker.calendar
# Returns dict with upcoming earnings dates, dividends, etc.
```

---

## News

```python
ticker.news
# Returns list of dicts with: title, link, publisher, providerPublishTime, type
```

---

## Multiple Tickers

```python
tickers = yf.Tickers("AAPL MSFT GOOGL")

# Access individual tickers
tickers.tickers["AAPL"].info
tickers.tickers["MSFT"].history(period="1mo")
```

---

## Screener & Equity Query

Build custom stock screens.

```python
import yfinance as yf
from yfinance import EquityQuery

# Create a query
query = EquityQuery('and', [
    EquityQuery('gt', ['intradaymarketcap', 1_000_000_000]),   # market cap > $1B
    EquityQuery('lt', ['peratio.lasttwelvemonths', 20]),       # trailing P/E < 20
    EquityQuery('eq', ['sector', 'Technology']),               # tech sector
    EquityQuery('eq', ['region', 'us']),
])

# Run the screen — returns a dict; matches are in result["quotes"]
result = yf.screen(query, size=25, sortField='intradaymarketcap', sortAsc=False)
symbols = [q['symbol'] for q in result.get('quotes', [])]

# Operators: eq, gt, lt, gte, lte, btwn, is_in
# EquityQuery validates field names and raises ValueError on unknown ones
# (e.g. 'marketcap' and 'peratio' are invalid; use 'intradaymarketcap' and
# 'peratio.lasttwelvemonths'). yf.screen also accepts predefined screen names
# such as 'day_gainers'.
```

---

## Sector & Industry

```python
# Sector data
tech = yf.Sector("technology")
tech.overview
tech.industries    # DataFrame of industries in this sector

# Industry data
semiconductors = yf.Industry("semiconductors")
semiconductors.overview
semiconductors.top_companies

# Valid sector keys:
# basic-materials, communication-services, consumer-cyclical,
# consumer-defensive, energy, financial-services, healthcare,
# industrials, real-estate, technology, utilities
```

---

## Search

```python
search = yf.Search("Tesla")
search.quotes    # matching ticker quotes
search.news      # related news articles
```

---

## Timezone Handling

yfinance returns tz-aware datetime indices (typically `America/New_York`). When filtering or comparing dates, you **must** match timezone awareness to avoid `TypeError: Cannot compare tz-naive and tz-aware datetime-like objects`.

```python
import yfinance as yf
import pandas as pd

hist = yf.Ticker("AAPL").history(period="1y")

# WRONG — tz-naive timestamp vs tz-aware index:
# filtered = hist[hist.index >= pd.Timestamp("2025-01-01")]  # TypeError!

# Option A (recommended): make the comparison timestamp tz-aware
start = pd.Timestamp("2025-01-01", tz="America/New_York")
filtered = hist[hist.index >= start]

# Option B: strip timezone from index first
hist.index = hist.index.tz_localize(None)
filtered = hist[hist.index >= pd.Timestamp("2025-01-01")]
```

Always use **Option A** when you need to preserve timezone info for accurate date boundaries. Use **Option B** when timezone doesn't matter (e.g., daily data aggregation).

---

## Error Handling

```python
import yfinance as yf

try:
    ticker = yf.Ticker("AAPL")
    hist = ticker.history(period="1mo")
    if hist.empty:
        print("No data returned — check ticker symbol or date range")
    else:
        print(hist)
except Exception as e:
    print(f"Error fetching data: {e}")
```

Common issues:
- **Empty DataFrame**: Invalid ticker, delisted stock, or date range outside available data
- **Rate limiting**: Too many requests in short time — add delays between calls
- **Missing fields in `.info`**: Not all fields are available for all tickers (ETFs, mutual funds, foreign stocks may differ)
- **Intraday data limits**: 1m data only available for last ~7 days
- **Timezone mismatch**: See "Timezone Handling" section above — always match tz-awareness when comparing dates
