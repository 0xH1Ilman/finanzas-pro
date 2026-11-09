# 05-screeners-swing — parte 2

Skills de terceros agrupadas por tema. Cada sección indica fuente, licencia y dónde está su código.



---

## SKILL: parabolic-short-trade-planner

- Fuente: `tradermonty/claude-trading-skills` → `skills/parabolic-short-trade-planner` (MIT)
- Cuándo usarla: Screen US equities for parabolic exhaustion patterns and generate conditional pre-market short plans, then evaluate intraday trigger fires from live 5-min bars. Phase 1 daily 5-factor scorer (MA extension / acceleration / volume climax / range expansion / liquidity), Phase 2 per-candidate plans for ORL break / first-red 5-min / VWAP fail with explicit borrow / SSR / manual-confirmation gating, Phase 3 one-shot intraday FSM that detects trigger fires and resolves concrete share counts. Covers Phase 1 + Phase 2 + Phase 3.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/parabolic-short-trade-planner/` (smoke_universe_diverse.csv, smoke_universe_relaxed.csv, requirements.txt, _fmp_compat.py, _market_calendar.py, __init__.py, alpaca_inventory_adapter.py, alpaca_market_data_adapter.py, fixture_market_data_adapter.py, market_data_adapter.py, bar_normalizer.py, broker_short_inventory_adapter.py …)

## Overview

Generate Qullamaggie-style Parabolic Short watchlists and conditional
pre-market plans for US equities. The skill never sends orders. It emits
JSON + Markdown that a human reviews against their broker before entry.

Three phases:

- **Phase 1 (`screen_parabolic.py`)**: pulls EOD bars + company profile
  from FMP, applies hard invalidation rules (mode-aware), scores
  survivors on 5 factors (weights 30/25/20/15/10), and assigns A/B/C/D
  grades.
- **Phase 2 (`generate_pre_market_plan.py`)**: takes the Phase 1 JSON,
  filters by `--tradable-min-grade` (default `B`), checks Alpaca short
  inventory (or `ManualBrokerAdapter`), evaluates SEC Rule 201 SSR
  state from the inherited prior-day close, and renders three trigger
  plans per candidate.
- **Phase 3 (`monitor_intraday_trigger.py`)**: reads the Phase 2 plan,
  fetches 5-min bars (Alpaca live or fixture), walks each plan's FSM
  forward by one step, persists per-plan state, and writes an
  `intraday_monitor` JSON with `state`, `entry_actual`, `stop_actual`,
  and `shares_actual` (when triggered). One-shot — trader runs it
  every 1–5 min via `watch` or cron; replay-deterministic so re-runs
  are byte-identical.

## When to Use

Invoke this skill when the user wants to:

- Build a daily Parabolic Short watchlist from S&P 500 (or a custom CSV).
- Translate a watchlist into pre-market trade plans with explicit
  borrow / SSR / state-cap gating.
- Audit a candidate's blocking vs advisory manual-confirmation reasons
  before placing an order at Alpaca.

Do NOT invoke for:

- Long-side momentum screening — use vcp-screener or canslim-screener.
- 1-minute / sub-minute intraday signals — Phase 3 evaluates 5-min
  bars only.
- Live order routing — this skill is detection-only by design;
  Phase 3 emits a `triggered` state with concrete entry/stop/share
  count, but the trader fires the order manually.

## Workflow

### Phase 1 — daily screener

1. Confirm `FMP_API_KEY` is set (env var or `--api-key`).
2. Run with the safer-by-default mode:
   ```bash
   python3 skills/parabolic-short-trade-planner/scripts/screen_parabolic.py \
     --mode safe_largecap --as-of 2026-04-30 --output-dir reports/
   ```
3. Inspect `reports/parabolic_short_<date>.md` — the watchlist is grouped
   by grade (A→D).
4. Promote interesting names to Phase 2.

For small-cap blow-offs, switch to `--mode classic_qm` (looser market
cap and ADV floors, higher 5-day ROC threshold).

For testing without the API, run `--dry-run --fixture <path>` against a
JSON fixture (one is shipped at `scripts/tests/fixtures/dry_run_minimal.json`).

### Phase 2 — pre-market plan generator

1. Optional: set `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` for live borrow
   checks. Without them the planner falls back to `ManualBrokerAdapter`,
   which marks every candidate as `borrow_inventory_unavailable` /
   `plan_status: watch_only`.
2. Run:
   ```bash
   python3 skills/parabolic-short-trade-planner/scripts/generate_pre_market_plan.py \
     --candidates-json reports/parabolic_short_2026-04-30.json \
     --account-size 100000 --risk-bps 50 --output-dir reports/
   ```
3. Output: `reports/parabolic_short_plan_<date>.json`. Each plan contains
   three entry plans (5min ORL break, first red 5-min, VWAP fail) with
   `entry_hint` / `stop_hint` formula strings (no baked-in shares — the
   trader computes shares at trigger time from the `shares_formula`).

### Phase 3 — intraday trigger monitor

1. Confirm `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` are set (Phase 3
   uses Alpaca market data; `data.alpaca.markets` works for both
   paper and live accounts).
2. During US regular session, run one-shot per cadence — typical is
   every 60 s during the first 30 min, then every 5 min:
   ```bash
   python3 skills/parabolic-short-trade-planner/scripts/monitor_intraday_trigger.py \
     --plans-json reports/parabolic_short_plan_2026-05-05.json \
     --bars-source alpaca \
     --state-dir state/parabolic_short/ \
     --output-dir reports/
   ```
   Or wrap in `watch -n 60 'python3 ...'` / cron.
3. Output: `reports/parabolic_short_intraday_<date>.json` lists every
   monitored plan with `state` (`armed` / `triggered` / `invalidated`
   / FSM-specific), bar-derived transition timestamps, and
   `size_recipe_resolved` (concrete `shares_actual`) when triggered.
4. For testing without the API, use `--bars-source fixture
   --bars-fixture <path>` against a JSON fixture
   (`scripts/tests/fixtures/intraday_bars/`).

Phase 3 trigger detection is not an order instruction. Before any manual
short entry, confirm borrow/locate availability, SEC Rule 201 SSR state,
broker short-sale controls, and the broker's current intraday margin or
day-trading controls. FINRA replaced the old pattern-day-trader day-count
and $25,000 minimum-equity requirements with intraday margin standards
effective 2026-06-04, with broker phase-in allowed through 2027-10-20.

Phase 3 is **idempotent**: each run replays the full session bars
from open up to `now_et` (or `--now-et` override), so re-running
during the same minute produces the same state. `prior_state` is
used only for diff/notification display; it never advances the FSM.

### Reviewing a plan before entry

Read three top-level fields per ticker:

- `plan_status`: `actionable` (manual gates can be cleared) or
  `watch_only` (hard blockers — borrow unavailable or SSR active).
- `blocking_manual_reasons`: must all be resolved before pulling the
  trigger.
- `advisory_manual_reasons`: heads-up only, e.g.
  `manual_locate_required` (always set), `warning:too_early_to_short`,
  `warning:recent_earnings_catalyst` (last earnings within
  `--earnings-catalyst-window-days`, default 10 trading days — flag the
  move as event-driven rather than pure technical blow-off).

### Earnings-aware screening

Phase 1 fetches the FMP earnings calendar once per run (single call,
not per-symbol) and emits two earnings-aware checks:

- `--exclude-earnings-within-days` (default 2 calendar days, forward) —
  hard invalidation when next earnings is within the window. Matches
  the legacy `earnings_blackout_days` semantic.
- `--earnings-catalyst-window-days` (default 10 trading days, backward)
  — soft warning `recent_earnings_catalyst` when last earnings is
  within the window. Routes to Phase 2 as an advisory manual reason
  without forcing `trade_allowed_without_manual: false`.

Per-candidate output exposes `last_earnings_date`, `next_earnings_date`,
`trading_days_since_earnings` (TRADING days), `earnings_within_days`
(CALENDAR days, forward), `earnings_blackout_days` (configured threshold),
and `earnings_in_blackout_window`. The legacy `earnings_within_2d` is
kept for backward compatibility.

Top-level dates: `as_of` is the planning date (Phase 2 contract — never
mutate); `run_date` mirrors it; `market_data_as_of` is the latest bar
date used for technical metrics (differs from `as_of` on weekend runs).

## Exchange Calendar and Replay

Install `requirements.txt` before running the planner. Phase 1 `--as-of` uses
strict `YYYY-MM-DD`, filters bars beyond that ceiling, and counts earnings age
with XNYS sessions. Phase 3 uses actual holidays and early closes; the close
boundary is exclusive. Historical dates are accepted only with Phase 1
`--dry-run` fixture data; live universe and profile endpoints are not PIT and
therefore fail closed for a non-current `--as-of`.

## Output Format

Phase 1 JSON: `parabolic_short_<as_of>.json` (schema_version 1.0).
Phase 2 JSON: `parabolic_short_plan_<as_of>.json` (schema_version 1.0).
Phase 3 JSON: `parabolic_short_intraday_<as_of>.json` (schema_version 1.0,
phase = `intraday_monitor`).
The contract is pinned by `tests/test_schema_contract.py` plus
`tests/test_monitor_intraday_smoke.py` for Phase 3.

## Resources

- `references/parabolic_short_methodology.md` — Qullamaggie's 3-trigger
  framework and exhaustion signals.
- `references/short_invalidation_rules.md` — mode-aware exclusion rules.
- `references/short_risk_management.md` — Rule 201, ETB vs HTB, locate.
- `references/intraday_trigger_playbook.md` — detail on each trigger
  type, the FSM transitions Phase 3 implements, and same-bar tie-break
  semantics.
- `references/broker_capability_matrix.md` — what each broker exposes
  through its API for short inventory.

### Referencia: references/broker_capability_matrix.md

# Broker Capability Matrix

What each broker exposes through its API for short inventory, and how
it maps onto this skill's `BrokerShortInventoryAdapter` contract.

| Field | Alpaca (paper + live) | Interactive Brokers | Manual |
|---|---|---|---|
| `shortable` | ✅ (`/v2/assets/{symbol}.shortable`) | ✅ via TWS API | n/a |
| `easy_to_borrow` | ✅ (`easy_to_borrow`) | ⚠️ inferred from rate sheet | n/a |
| `can_open_new_short` | shortable AND ETB | locate-dependent | always False (default-deny) |
| `borrow_fee_apr` | 0.0 for ETB; None for HTB | quoted per-symbol | None |
| `borrow_fee_manual_check_required` | True only for HTB | False (rate is quoted) | always True |
| `manual_locate_required` | always True (broker confirms) | False after locate succeeds | always True |
| New short on HTB? | ❌ rejected at submit | ✅ after locate | n/a |

## Why the contract sets `manual_locate_required` to True even for ETB

ETB names can lose ETB status mid-day if borrow demand spikes. Marking
the field always True keeps the human in the loop: the trader sees
`advisory_manual_reasons: [manual_locate_required]` on every plan and
re-checks at the broker before submitting. The flag is *advisory*, so
it does not gate `trade_allowed_without_manual` on its own.

## How to add another broker

1. Subclass `BrokerShortInventoryAdapter` in
   `scripts/adapters/<broker>_inventory_adapter.py`.
2. Implement `get_inventory_status(symbol) -> dict` returning the
   contract dict.
3. Raise `BrokerNotConfiguredError` if the broker's credentials are
   missing — `generate_pre_market_plan.py` falls back to
   `ManualBrokerAdapter` when this fires.
4. Add the broker name to the `--broker` CLI choices in
   `generate_pre_market_plan.py::build_arg_parser`.
5. Add an adapter test that mocks the broker's HTTP layer with
   `unittest.mock.patch`.

## Why no SDK dependency

Alpaca publishes `alpaca-py` but each broker SDK pulls in additional
transitive dependencies and increases the skill bundle size. This skill
talks HTTP via `requests` directly, the same pattern the existing
`portfolio-manager` skill uses for its account checks. Keeps the
.skill bundle deployable as-is.

### Referencia: references/intraday_trigger_playbook.md

# Intraday Trigger Playbook

> **Status (v0.5 — implemented)**: this reference describes the
> trigger semantics that `monitor_intraday_trigger.py` evaluates as a
> one-shot FSM. Phase 2 plans (`generate_pre_market_plan.py`) emit
> `entry_hint` / `stop_hint` formula strings that map to these
> triggers; Phase 3 reads bars (Alpaca live or fixture), walks the
> FSM, and writes `intraday_monitor` JSON with concrete
> `entry_actual` / `stop_actual` / `shares_actual`.
>
> **FSM contracts implemented in Phase 3**:
> - `triggered` is **not** terminal — post-trigger bars are still
>   evaluated for invalidation predicates so a reclaim flips the plan
>   to `invalidated`.
> - `invalidated` **is** terminal/absorbing — no further transitions
>   for that `plan_id` on that session date.
> - First Red same-bar tie-break: when a single bar both takes out
>   `red_high` (would invalidate) AND prints below `red_low` (would
>   trigger), invalidation wins. Short-side conservatism.
> - ORL post-trigger invalidation requires `close > orl_low` AND
>   `close > current_vwap` (BOTH reclaimed, not just one).
> - Idempotency: every Phase 3 run replays the full session bars; the
>   FSM is a pure function of `(plan, bars, atr_14)`. `prior_state`
>   is consulted only for display continuity / notification diffs.
> - Bar timing (v0.5d): `ts_et` on each bar is the **bar-open**
>   instant (matches Alpaca wire). A bar with `ts_et = T` covers
>   `[T, T+5min)` and is *confirmed* at `T+5min`. The Phase 3
>   adapters only return confirmed bars (`bar_open + 5min <=
>   until_et`); the FSM never sees an in-progress current bar.
> - ORL anchoring: the Opening Range bar must be the 09:30 ET bar.
>   When Alpaca skips that interval (no trades / halt at the open),
>   the ORL evaluator emits `evaluation_status="skipped"` +
>   `skip_reason="opening_range_bar_unavailable"` rather than
>   anchoring on a later bar.

## 5-min Opening Range Low (ORL) break

```
plan_id template:   <TICKER>-<YYYYMMDD>-ORL5
trigger_type:       orl_5min_break
condition (ja):     5min ORL を出来高 1.2x 以上で下抜け
entry_hint:         5min_orl_low - 0.05
stop_hint:          session_HOD + 0.25 * ATR
structural_targets: dma_10, dma_20
```

**Phase 3 evaluator**:

1. Wait for the first 5-minute bar to close. Mark its high (ORH) and
   low (ORL).
2. After 9:35 ET, watch every 5-minute close. If a bar closes below
   ORL AND its volume ≥ 1.2× the ORL bar's volume, fire the trigger.
3. Stop is `session_HOD + stop_buffer_atr * ATR(14)`.
4. Invalidates if a subsequent 5-minute close prints back above ORL
   AND VWAP (sign of failed breakdown).

## First Red 5-minute candle

```
plan_id template:   <TICKER>-<YYYYMMDD>-FR5
trigger_type:       first_red_5min
condition (ja):     寄付後最初の赤 5min の安値割れ
entry_hint:         first_red_5min_low - 0.05
stop_hint:          first_red_5min_high
```

**Phase 3 evaluator**:

1. Track every 5-minute bar from 9:30 ET. Mark the first bar where
   `close < open` (a red candle).
2. After that bar closes, fire the trigger when a later 5-minute bar
   prints below the red candle's low.
3. Stop is the red candle's high.
4. Invalidates if any subsequent 5-minute bar takes out the red
   candle's high before the trigger fires.

## VWAP fail

```
plan_id template:   <TICKER>-<YYYYMMDD>-VWF
trigger_type:       vwap_fail
condition (ja):     First crack 後 VWAP retest で 5min 終値拒否 + lower-high 下抜け
entry_hint:         lower_high_low - 0.05
stop_hint:          vwap_reclaim_5min_close
```

**Phase 3 evaluator** (FSM):

State machine has six states:
`armed → first_crack_seen → vwap_retest_seen → rejection_confirmed → triggered → invalidated`

1. `armed`: market open, watching for first VWAP loss.
2. `first_crack_seen`: 5-minute close prints below VWAP for the first
   time, AND price comes from session HOD (filters open-print VWAP
   noise).
3. `vwap_retest_seen`: subsequent bar closes back at or above VWAP
   (the "retest").
4. `rejection_confirmed`: next 5-minute bar prints a lower high than
   the retest bar AND closes back below VWAP.
5. `triggered`: fire on the break of the rejection bar's low.
6. `invalidated`: any 5-minute close back above VWAP after `triggered`
   OR a clean uptrend line break before `triggered`.

## Common evaluator concerns

- **Time zone**: all timestamps `America/New_York`.
- **Halt handling**: bars during halt are skipped; the FSM resumes
  from its last state when trading resumes.
- **Bar close vs touch**: triggers fire on bar close, not intra-bar.
  Reduces wick noise.
- **No re-entry**: once a plan is `triggered` or `invalidated`, the
  FSM does not re-arm for the day.

### Referencia: references/parabolic_short_methodology.md

# Parabolic Short Methodology

Adapted from Qullamaggie's three "timeless" short setups. The thesis:
parabolic moves end in mean-reverting blow-offs, but shorting too
early — while the move is still climbing — is the single fastest way
to lose money. The setup framework below exists to *delay* entry until
exhaustion is visibly confirmed.

## When a stock qualifies as parabolic

Daily-chart preconditions, all of which must be true:

- 5-day return ≥ +30% (`safe_largecap`) or ≥ +100% (`classic_qm`).
- Latest close ≥ +25% above the 20-day SMA, AND ≥ 4 ATR-units above it
  (volatility-normalized — small-caps with high ATR aren't penalized).
- Three or more consecutive green daily candles AND an acceleration
  ratio (3-day mean return / 10-day mean return) > 1.0.
- Latest-bar volume ratio (vs 20-day average) ≥ 1.5×.
- Liquidity floor: 20-day average dollar volume ≥ $20M
  (`safe_largecap`) or $5M (`classic_qm`).

These aren't a trade trigger — they're a watchlist filter. Entries are
intraday on one of the three trigger types below.

## The three trigger types

### 1. 5-min Opening Range Low (ORL) break

The cleanest setup when the open prints a wide first 5-minute bar.
Mark its low. If a subsequent 5-minute bar prints below ORL on
≥1.2× the ORL bar's volume, short the break. Stop above session HOD
plus 0.25 ATR.

### 2. First Red 5-minute candle

When the open is straight up — a series of green 5-minute bars
extending the parabola — wait for the first red 5-minute candle.
Short the break of *its* low. Stop above its high. This is the safest
variant when the open gaps into resistance.

### 3. VWAP fail

After a "first crack" — price collapsing off session HOD toward VWAP —
let it retest VWAP. A 5-minute close back below VWAP plus a lower-high
break is the entry. Invalidates instantly on a 5-minute close back
above VWAP (the "VWAP reclaim").

## Invalidation rules

Hard skips, applied before scoring. See `short_invalidation_rules.md`
for the full list.

## Why state caps matter

Parabolic candidates are by definition hitting fresh highs with strong
closes and expanding volume — exactly the metrics that, in a trend
template, would qualify them as bullish. The skill flags candidates
that closed near their session high at a fresh 52-week high as
`state_cap: still_in_markup` so Phase 2 can mark them
`plan_status: watch_only` until intraday weakness shows up.

### Referencia: references/short_invalidation_rules.md

# Short Invalidation Rules

Hard-rejects in `invalidation_rules.py`. These run before any scoring,
so they're cheap and binary. Soft signals (state caps / warnings) live
in `state_caps.py` instead.

## Rules (mode-aware)

| Rule | safe_largecap | classic_qm | Source |
|---|---|---|---|
| Earnings within N trading days | ≤ 2 days → reject | ≤ 2 days → reject | FMP earnings calendar |
| Market cap floor | < $2B → reject | < $300M → reject | FMP profile `mktCap` |
| 20-day average dollar volume | < $20M → reject | < $5M → reject | Computed from EOD bars |
| Latest close | < $5.00 → reject | < $5.00 → reject | EOD close |
| Days since IPO | < 60 trading days → reject | < 60 trading days → reject | FMP profile `days_listed_actual` |
| User CSV catalyst flag | flagged → reject | flagged → reject | Optional input |

## Why earnings within 2 days is hard-rejected

Earnings risk is binary and asymmetric. Even a deeply parabolic chart
can gap +30% on a beat-and-raise overnight, blowing through any stop.
The screener does not enable a "trade through earnings" override —
post-earnings setups belong to a different skill (earnings-trade-analyzer
or pead-screener).

## Why classic_qm tolerates smaller caps

Qullamaggie's archetypal Parabolic Short targets — small-cap meme
runners up 300-1000% in a few weeks — wouldn't pass `safe_largecap`.
Switching to `classic_qm` lowers the cap floor to $300M and the ADV
floor to $5M so those names enter the universe. The trade-off:
classic_qm names are far more likely to be `borrow_inventory_unavailable`
on Alpaca and end up `plan_status: watch_only`.

## What's NOT a hard reject

- Recent 52-week high — that's a state cap, not a kill.
- Strong closing print near session high — also a state cap.
- Premarket gap — turns into the "wait for first crack" advisory warning.

The reasoning: this is a Parabolic SHORT planner. Bullish-looking daily
patterns are the *target*. Filtering them out leaves no candidates.

### Referencia: references/short_risk_management.md

# Short Risk Management

## SEC Rule 201 (Short Sale Restriction)

Triggered when a security's regular-session intraday price drops 10%
or more from the prior day's regular-session close. While active:

- New short sales are restricted to prices ABOVE the national best bid
  (the "uptick rule").
- The restriction holds for the rest of the trading day **and** the
  full next trading day.

**Implementation note**: this skill inherits `prior_regular_close` from
Phase 1's `key_levels.prior_close` (sourced from FMP's
`historical-price-eod/full`, which is the regular-session 4:00 PM ET
close). It does NOT use FMP's quote endpoint `previousClose`, which
can drift to the aftermarket print.

`ssr_state_tracker.py` persists per-symbol state to
`state/parabolic_short/ssr_state_<ticker>_<date>.json` so today's
`ssr_triggered_today` rolls forward to tomorrow's
`ssr_carryover_from_prior_day`.

## Borrow inventory: Alpaca specifics

Alpaca only allows new short opens on Easy-To-Borrow (ETB) names. The
adapter encodes this exactly:

```
can_open_new_short = shortable AND easy_to_borrow
borrow_fee_apr     = 0.0 if easy_to_borrow else None
manual_locate_required = True   # always
```

A name that is `shortable=True` but `easy_to_borrow=False` (HTB) cannot
be opened on Alpaca regardless of locate. Phase 2 marks these as
`borrow_inventory_unavailable` (a hard blocker) and renders the plan
as `plan_status: watch_only`.

`manual_locate_required` is True even on ETB names. The trader still
confirms locate at the broker before entry — it's an advisory reason,
not blocking, so plans for ETB names stay actionable.

## Position sizing

The `size_recipe_builder.py` outputs:

- `risk_usd` — per-trade risk in USD (account_size × risk_bps/10000).
- `max_position_value_usd` — per-symbol position cap (account_size ×
  max_position_pct/100), tightened if `current_short_exposure` is high.
- `shares_formula` — string form of the formula. Phase 3 evaluates it
  at trigger fire when actual entry/stop are known.
- `exposure_cap_applied` — True if the per-symbol cap was tightened
  because the aggregate short-book budget was already mostly used.
- `remaining_short_exposure_capacity_usd` — how much short-book
  headroom is left.

This deliberately excludes a fixed share count. ORL / first-red /
VWAP-fail entries only have known prices intraday, so committing to a
share count pre-market would be inaccurate.

## Daily loss limits

Not enforced in this MVP. The trader is responsible for honoring
account-level circuit breakers. A future revision can add a `state/`
file recording realized P&L and reject new plans when the daily loss
limit is hit.

### Referencia: references/smoke_test_runbook.md

# Parabolic Short — Live API Smoke Test Runbook

This runbook is the manual verification procedure for the
`parabolic-short-trade-planner` skill against **live** FMP and Alpaca
APIs. The Phase 1 + Phase 2 unit-test suite (137 tests on dry-run
fixtures) cannot prove that the wire shapes upstream still match the
contract Phase 1 was built against, nor that the Alpaca paper account
is reachable with the configured credentials. This runbook closes that
gap.

Run it on any non-trivial change to:

- `fmp_client.py` (especially the EOD / profile normalizers)
- `adapters/alpaca_inventory_adapter.py`
- the Phase 1 → Phase 2 schema (any field rename in `parabolic_short_*`
  output JSON)
- new Alpaca account / API key rotation

It is also the one-time validation expected after merging the Phase 1+2
implementation, since the original PR shipped without any live
execution.

## 1. Prerequisites

Set the following environment variables before running anything:

```bash
export FMP_API_KEY=...           # Free tier (250 calls/day) is enough
export ALPACA_API_KEY=...
export ALPACA_SECRET_KEY=...
export ALPACA_PAPER=true         # Paper trading account; recommended
```

Other requirements:

- Python 3.10+
- `requests` available (`pip install requests` or use the repo's venv)
- Run all commands from the repository root; `screen_parabolic.py` and
  `generate_pre_market_plan.py` resolve `--ssr-state-dir` and
  `--output-dir` relative to the current working directory.

> **Cwd matters for SSR carryover.** Mixing relative and absolute
> paths across runs can leave orphan state files. The runbook below
> always passes `"$(pwd)/state/parabolic_short"` as the SSR state dir.

## 2. Connectivity check (~90 s, 5 checks / 6 HTTP calls)

```bash
python3 skills/parabolic-short-trade-planner/scripts/check_live_apis.py
```

The script runs **5 logical checks** (4 required gates + 1 optional
warning) against FMP + Alpaca. The fifth check (`alpaca_404_graceful`)
issues two HTTP requests against the same Alpaca endpoint — one raw
probe to confirm the 404 status, one through
`AlpacaInventoryAdapter.get_inventory_status()` to confirm the adapter
handles that response without raising — so the script makes
**6 HTTP calls** per run total (3 FMP + 3 Alpaca). Cost remains
trivial under both API rate limits.

Expected output (order may vary):

```
PASS fmp.historical_price_eod_full — N bars; Issue #64 shape verified
PASS fmp.profile — mktCap=...
WARN fmp.sp500_constituent — HTTP 403 — likely entitlement (skip on Free)
PASS alpaca.assets_aapl — shortable=True easy_to_borrow=True (paper=True)
PASS alpaca.assets_404_graceful — raw HTTP 404 mapped to asset_not_found dict
Required gates: 4/4 passed (sp500 is optional warning)
```

Exit code 0 means all four required gates passed. The sp500 line is a
warning, not a gate — it can be PASS or WARN depending on FMP tier.

If any gate fails, the script prints `FAIL <name> — HTTP <code> — <body
truncated>`. Common failure causes are documented in the
**Troubleshooting matrix** at the end.

### 2a. FMP-only mode (no Alpaca credentials)

Contributors who only have an FMP key configured can validate the
FMP wire shape without needing Alpaca paper credentials:

```bash
python3 skills/parabolic-short-trade-planner/scripts/check_live_apis.py --fmp-only
```

Expected output:

```
Mode: --fmp-only (Alpaca gates will be skipped)
PASS fmp.historical_price_eod_full — N bars; Issue #64 shape verified
PASS fmp.profile — mktCap=...
PASS fmp.sp500_constituent — N constituents
SKIP alpaca.assets_aapl — explicitly skipped via --fmp-only
SKIP alpaca.assets_404_graceful — explicitly skipped via --fmp-only
Required gates: 2/2 passed (FMP only; Alpaca gates skipped, sp500 is optional warning)
```

Exit code is 0 when the FMP required gates pass. The Alpaca gates
print as `SKIP` and never count toward the exit code in this mode.

If you forget the flag and Alpaca creds are unset, the script still
runs the FMP gates, prints `SKIP` for the Alpaca gates, and tells you
to either pass `--fmp-only` or set the Alpaca env vars. This avoids
the previous behaviour of aborting at setup.

The Alpaca gates (`alpaca.assets_aapl`, `alpaca.assets_404_graceful`)
are **maintainer-only** verification when FMP is the only API the
contributor has access to. Production deployment of Phase 2 / Phase 3
still requires Alpaca credentials — `--fmp-only` is for runbook
validation, not production use.

## 3. Phase 1 — Tier 1 rejection smoke (`smoke_universe_diverse.csv`)

```bash
mkdir -p reports/smoke
python3 skills/parabolic-short-trade-planner/scripts/screen_parabolic.py \
  --universe finviz-csv \
  --universe-csv skills/parabolic-short-trade-planner/references/smoke_universe_diverse.csv \
  --max-api-calls 50 --top 25 \
  --output-dir reports/smoke/ \
  --verbose
```

The diverse CSV is rejection-biased (mega-cap defensives + thin
mid-caps), so most or all tickers will reject at the soft thresholds
(`min_roc_5d`, `min_ma20_extension_pct`). **Zero candidates is a PASS
for this tier** provided `--verbose` shows at least one rejection
reason, which proves the invalidation path is live.

Expected `--verbose` rejection log (one line per rejected ticker,
under `INFO parabolic_short.screen Universe size: ...`):

```
DEBUG parabolic_short.screen Rejected JNJ: min_roc_5d threshold not met (got -0.13%, need >=30.00%)
DEBUG parabolic_short.screen Rejected PG: min_roc_5d threshold not met (got -0.62%, need >=30.00%)
DEBUG parabolic_short.screen Rejected KO: min_roc_5d threshold not met (got 2.54%, need >=30.00%)
...
```

Other rejection reasons that may appear depending on the CSV /
market state:

- `Rejected <T>: insufficient_history (<N> bars; need >=21)` — recent
  IPO or post-split; the screener cannot compute its 20-bar metrics.
- `Rejected <T>: invalidation (<reasons>)` — hard-gate rejection
  (market cap below mode floor, ADV below floor, earnings within
  window, IPO too recent, catalyst blackout).
- `Rejected <T>: min_ma20_extension_pct threshold not met (got <X>%, need >=<Y>%)`
- `Rejected <T>: min_atr_extension threshold not met (got <X>, need >=<Y>)`

Tier 1 PASS requires at least one such rejection line — that proves
the rejection path is live, not silently swallowed.

Output:

- `reports/smoke/parabolic_short_<as_of>.json` — v1.0 schema; `candidates`
  may be `[]`.
- `reports/smoke/parabolic_short_<as_of>.md` — human-readable report.

If candidates **is** non-empty, you can additionally run Phase 2 with
`--broker none` against this report and confirm every plan comes out
as `plan_status: watch_only` with `borrow_inventory_unavailable` in
`blocking_manual_reasons` — same checks as Tier 2 below.

## 4. Phase 1 — Tier 2 end-to-end smoke (`smoke_universe_relaxed.csv`)

```bash
python3 skills/parabolic-short-trade-planner/scripts/screen_parabolic.py \
  --universe finviz-csv \
  --universe-csv skills/parabolic-short-trade-planner/references/smoke_universe_relaxed.csv \
  --min-roc-5d 0 --min-ma20-extension-pct 0 --min-atr-extension 0 \
  --watch-min-grade D \
  --exclude-earnings-within-days 0 --min-adv-usd 0 \
  --min-price 0 --min-market-cap 0 \
  --max-api-calls 50 --top 25 \
  --output-dir reports/smoke/ \
  --output-prefix parabolic_short_relaxed \
  --verbose
```

Two flag groups:

- **Soft** (`--min-roc-5d`, `--min-ma20-extension-pct`,
  `--min-atr-extension`): set to 0 so score components don't gate.
- **Hard** (`--exclude-earnings-within-days`, `--min-adv-usd`,
  `--min-price`, `--min-market-cap`): set to 0 so a single
  earnings-tomorrow ticker (or recent IPO) doesn't drop the whole
  CSV. All four flags already exist on `screen_parabolic.py` —
  the runbook does not need a source patch.

> Earnings-aware behavior: in addition to the forward-looking hard
> blackout above, `--earnings-catalyst-window-days` (default 10 trading
> days) attaches a **soft** `recent_earnings_catalyst` warning to any
> candidate that reported earnings within the window. Smoke runs leave
> this at the default — the warning is informational and does not gate
> survival. To suppress it for a regression diff against pre-earnings-fix
> output, set a **negative value** (e.g. `-1`): the screener compares
> `trading_days_since_earnings <= window`, so `0` still fires for same-day
> earnings while a negative window can never match.

Expected: `candidates` length ≥ 1 (near-certain on 8–10 mega-caps with
all gates relaxed). If 0, the rejection logic itself is buggy or the
relaxed CSV is stale (re-curate the CSV — see Pitfall #5).

Output:

- `reports/smoke/parabolic_short_relaxed_<as_of>.json` — feeds Phase 2.

## 5. Phase 2 — Alpaca + manual paths

> **Important**: Steps 5a and 5b both write to `reports/smoke/` but
> with **different `--output-prefix` values**. The default prefix
> (`parabolic_short_plan`) would have the manual run silently
> overwrite the Alpaca run.

### 5a. Alpaca path

```bash
mkdir -p state/parabolic_short
PHASE1_RELAXED=reports/smoke/parabolic_short_relaxed_<as_of>.json
python3 skills/parabolic-short-trade-planner/scripts/generate_pre_market_plan.py \
  --candidates-json "$PHASE1_RELAXED" \
  --broker alpaca \
  --tradable-min-grade D \
  --account-size 100000 --risk-bps 50 \
  --ssr-state-dir "$(pwd)/state/parabolic_short" \
  --output-dir reports/smoke/ \
  --output-prefix parabolic_short_plan_alpaca
```

Expected:

- ≥1 plan emitted in `parabolic_short_plan_alpaca_<as_of>.json`.
- ≥1 plan ideally has `plan_status: actionable` (ETB happy path).
  If all plans come out `watch_only`, document in the smoke report
  ("all relaxed-CSV candidates HTB today — not a code bug, log only").
- `entry_plans[*].size_recipe.shares_formula` is a **string formula**,
  not a numeric `shares` field.
- Per-ticker SSR state files written under
  `state/parabolic_short/ssr_state_<ticker>_<as_of>.json`.

### 5b. Manual fallback path

```bash
python3 skills/parabolic-short-trade-planner/scripts/generate_pre_market_plan.py \
  --candidates-json "$PHASE1_RELAXED" \
  --broker none \
  --tradable-min-grade D \
  --account-size 100000 --risk-bps 50 \
  --ssr-state-dir "$(pwd)/state/parabolic_short" \
  --output-dir reports/smoke/ \
  --output-prefix parabolic_short_plan_manual
```

Expected (regression check on the manual fallback):

- Every plan has `plan_status: watch_only`.
- Every plan's `blocking_manual_reasons` contains
  `borrow_inventory_unavailable`.

## 6. Day-2 SSR carryover determinism

```bash
PHASE2_PLAN=reports/smoke/parabolic_short_plan_alpaca_<as_of>.json

# Guard: Tier 2 must have produced at least one plan.
PLAN_COUNT=$(python3 -c "import json; print(len(json.load(open('$PHASE2_PLAN'))['plans']))")
if [ "$PLAN_COUNT" -lt 1 ]; then
  echo "Step 6 skipped: Tier 2 produced 0 plans; carryover test cannot run."
  exit 1
fi

TICKER=$(python3 -c "import json; print(json.load(open('$PHASE2_PLAN'))['plans'][0]['ticker'])")
TODAY=$(python3 -c "import json; print(json.load(open('$PHASE1_RELAXED'))['as_of'])")
TOMORROW=$(python3 -c "from datetime import date,timedelta; print((date.fromisoformat('$TODAY')+timedelta(days=1)).isoformat())")
STATE_FILE="state/parabolic_short/ssr_state_${TICKER}_${TODAY}.json"

# Force the trigger flag in yesterday's state file (the MVP can't detect
# Rule 201 fires on its own because aftermarket data isn't wired in).
python3 -c "import json,pathlib; p=pathlib.Path('$STATE_FILE'); \
  d=json.loads(p.read_text()); d['ssr_triggered_today']=True; \
  p.write_text(json.dumps(d))"

python3 skills/parabolic-short-trade-planner/scripts/generate_pre_market_plan.py \
  --candidates-json "$PHASE1_RELAXED" \
  --broker none \
  --tradable-min-grade D \
  --as-of "$TOMORROW" \
  --ssr-state-dir "$(pwd)/state/parabolic_short" \
  --output-dir reports/smoke/ \
  --output-prefix parabolic_short_plan_day2
```

Expected: in `reports/smoke/parabolic_short_plan_day2_<TOMORROW>.json`,
the plan for `$TICKER` has:

```json
"ssr_state": {
  "ssr_carryover_from_prior_day": true,
  "uptick_rule_active": true,
  ...
}
```

The new `test_as_of_override_advances_carryover` test in
`tests/test_generate_pre_market_plan.py` covers the same behaviour at
the CLI/main() level, so this manual step is a regression check, not
the only verification.

## 7. Phase 3 — intraday trigger monitor smoke (added in Phase 3 v0.5)

Phase 3 evaluates 5-min bars during the US regular session and
walks each plan's FSM forward. v0.5 ships two data sources — a
fixture (offline, used in tests) and live Alpaca. Both are smoke-tested
here.

### 7a. Fixture-driven dry-run (no network)

```bash
python3 skills/parabolic-short-trade-planner/scripts/monitor_intraday_trigger.py \
  --plans-json skills/parabolic-short-trade-planner/scripts/tests/fixtures/phase2_plan_smoke.json \
  --bars-source fixture \
  --bars-fixture \
    skills/parabolic-short-trade-planner/scripts/tests/fixtures/intraday_bars/orl_clean_break.json \
  --state-dir /tmp/parabolic_intraday_smoke \
  --output-dir /tmp/parabolic_intraday_smoke \
  --as-of 2026-05-05 \
  --now-et 2026-05-05T10:00:00-04:00 \
  --verbose
```

Expected (from `parabolic_short_intraday_2026-05-05.json`):
- `phase: "intraday_monitor"`, `data_source: "fixture"`,
  `market_status: "regular_session"`.
- `monitored_plans` contains the AAPL ORL plan with
  `state: "triggered"`, `entry_actual: 148.45`,
  `stop_actual: 150.35`, and a `size_recipe_resolved` block with
  a positive integer `shares_actual`.

### 7b. Alpaca live integration check (paper account)

```bash
PHASE2_PLAN=reports/smoke/parabolic_short_plan_alpaca_<as_of>.json
mkdir -p state/parabolic_short
python3 skills/parabolic-short-trade-planner/scripts/monitor_intraday_trigger.py \
  --plans-json "$PHASE2_PLAN" \
  --bars-source alpaca \
  --state-dir "$(pwd)/state/parabolic_short" \
  --output-dir reports/smoke/ \
  --verbose
```

Expected during regular session:
- `monitored_plans` is non-empty (one entry per actionable plan
  in the Phase 2 report).
- Each plan with bars has `last_bar_ts` within ~20 min of now
  (15-min IEX feed delay + 5-min bar close).
- Outside session / on holidays: every plan emits
  `evaluation_status: "no_bars"` with `state` carried forward
  from any prior state file (defaults to `armed`). The
  `monitored_plans` list is **never empty** when input plans
  exist — this distinguishes "filtered out" from "no bars".

### 7c. Idempotency spot-check

Run Phase 3 twice in a row with `--bars-source fixture` and the
same `--now-et`; the output JSON files MUST be byte-identical
after stripping wall-clock fields (`evaluated_at`,
`last_evaluated_at`, `written_at`). If they diverge, the FSM is
reading `prior_state` — a regression against the v0.5
idempotency contract. The
`tests/test_one_shot_idempotency.py` test enforces the same
property in CI.

### 7d. Phase 3 PASS criteria (one-tier)

PASS if all of:

- 7a returns exit 0; the AAPL ORL plan reaches `state="triggered"`
  with the expected `entry_actual` / `stop_actual` and a positive
  `shares_actual`.
- 7b returns exit 0; either monitored_plans contain bars (regular
  session) OR every plan has `evaluation_status: "no_bars"`
  (closed / pre-9:30).
- 7c shows byte-identical output across two consecutive runs.

## 8. Success criteria — three-tier (with Phase 3)

A **FULL PASS** requires both tiers green; report a **PARTIAL PASS**
when one tier passes and the other is incomplete (e.g. "rejection tier
passed; end-to-end incomplete due to live Alpaca outage").

### Tier 1: rejection smoke (Section 3)

PASS if all of:

- `check_live_apis.py` exits 0 on the four required gates.
- Phase 1 produces a v1.0 schema JSON. Candidates may be empty.
- `--verbose` documents at least one rejection reason for at least one
  ticker.
- (If candidates non-empty) Phase 2 with `--broker none` returns every
  plan as `plan_status: watch_only` with
  `borrow_inventory_unavailable` in `blocking_manual_reasons`.

Zero Phase 1 candidates is **NOT a fail** for Tier 1 — the diverse
CSV is rejection-biased by design.

### Tier 2: minimum-one-plan smoke (Sections 4–6)

PASS if all of:

- Phase 1 produces ≥1 candidate against the relaxed CSV.
- Phase 2 with `--broker alpaca` produces ≥1 plan whose schema
  validates against `tests/test_schema_contract.py`.
- ≥1 plan has `plan_status: actionable` — if none, document in the
  smoke report ("all relaxed-CSV candidates HTB today; not a code bug").
- Phase 2 with `--broker none` flips every plan to `plan_status:
  watch_only`.
- Day-2 carryover step (Section 6) flips `ssr_carryover_from_prior_day`
  to `true`.

This tier is **incomplete, not pass** if Phase 1 returns zero
candidates against the relaxed CSV — investigate (rejection logic
buggy, CSV stale, or FMP transient error).

## 9. Pitfalls

1. **FMP `quote.previousClose` aftermarket drift** — the screener
   uses `historical-price-eod/full` for `prior_close`. Never read
   `quote.previousClose`; it returns aftermarket-adjusted values and
   breaks SSR Rule 201 math. Verify by picking a ticker with a > 5%
   post-4 PM move and confirming Phase 1 stored the regular-session
   number in `key_levels.prior_close`.
2. **Alpaca paper symbol absence** — paper accounts have a smaller
   asset universe than live. After the 404 fix (in this PR),
   missing tickers map to `error: asset_not_found` and Phase 2
   continues with that symbol marked `borrow_inventory_unavailable`.
   `--verbose` shows the per-ticker map.
3. **SSR state file path drift** — `--ssr-state-dir` defaults to
   `state/parabolic_short/` **relative to cwd**. Different cwds produce
   orphan state files and silently break carryover. Always pass
   `"$(pwd)/state/parabolic_short"` for absolute clarity. The repo's
   `.gitignore` excludes `state/` so production state cannot
   accidentally be committed; note that already-tracked files would
   need a separate `git rm --cached`, and `git add -f` can still
   force-add. Treat the ignore line as a default, not a hard guarantee.
4. **Universe selection bias is split across two CSVs** —
   `smoke_universe_diverse.csv` is intentionally rejection-biased to
   exercise the invalidation path; `smoke_universe_relaxed.csv` is
   intentionally pass-biased to exercise Phase 2 wiring. Invalid
   tickers are **not** in either CSV — that path is covered by
   `check_live_apis.py` step 5 + the `tests/test_broker_inventory.py`
   404 test. Cherry-picking only parabolic-today names is forbidden
   because it masks rejection-path bugs.
5. **Both smoke CSVs age by construction** — current high-fliers,
   ETB liquidity, and mega-cap composition all rotate. Re-curate
   both CSVs quarterly. For the diverse CSV, Tier 1 still passes
   on staleness (zero candidates is OK). For the relaxed CSV,
   staleness drops Tier 2 to "incomplete" (zero candidates) — the
   known failure mode for stale CSV maintenance, distinct from a
   real code bug.
6. **Lookback < 21 bars silent skip** — `screen_one_candidate`
   returns `None` when fewer than 21 bars are available, logged only
   at DEBUG. Recently-IPO'd or post-split tickers can produce empty
   `candidates[]` and look like an API failure. Always use
   `--verbose` for the first smoke run; empty output is not the same
   as a broken pipeline.

## 10. Troubleshooting matrix

| Symptom | Likely cause | Action |
|---|---|---|
| `check_live_apis.py` FAIL on `fmp.historical_price_eod_full` HTTP 401 | `FMP_API_KEY` invalid / expired | Re-issue key on https://site.financialmodelingprep.com/developer/docs |
| `check_live_apis.py` FAIL on `fmp.historical_price_eod_full` shape mismatch | FMP changed the EOD response shape (Issue #64 regression) | Read the body excerpt, then re-check `fmp_client._normalize_eod_flat_list` |
| `check_live_apis.py` WARN on `fmp.sp500_constituent` | FMP tier doesn't include the constituent endpoint | Ignore — not a gate. Phase 1 only uses sp500 when `--universe sp500`; finviz-csv path doesn't need it. |
| `check_live_apis.py` FAIL on `alpaca.assets_aapl` HTTP 401/403 | `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` mismatch with `ALPACA_PAPER` | Confirm the key was issued for the same account class (paper vs live) as `ALPACA_PAPER` |
| `check_live_apis.py` FAIL on `alpaca.assets_404_graceful` ("raised on 404") | Adapter regression — `raise_for_status()` triggered | Re-apply the 404 → asset_not_found mapping in `adapters/alpaca_inventory_adapter.py` |
| Phase 1 emits empty `candidates[]` against the **diverse** CSV | Expected — diverse CSV is rejection-biased | Confirm `--verbose` shows rejection reasons; **PASS** for Tier 1 |
| Phase 1 emits empty `candidates[]` against the **relaxed** CSV | (a) Rejection logic buggy, (b) CSV stale, (c) FMP transient error | Re-run with another ticker; check `--verbose`; re-curate the CSV if needed |
| Phase 2 errors on `KeyError: 'as_of'` from a custom Phase 1 JSON | Hand-edited Phase 1 JSON missing `as_of` | Pass `--as-of YYYY-MM-DD` explicitly |
| Phase 2 alpaca-step output disappears between steps 5a and 5b | `--output-prefix` defaulted to the same value in both runs | Always pass distinct `--output-prefix` per step |
| Day-2 carryover does NOT flip `ssr_carryover_from_prior_day` | (a) Wrong cwd between runs (state file in a different `state/` dir), (b) `--as-of` not advanced by exactly +1 calendar day | Run `ls state/parabolic_short/` and confirm the Day-1 state file uses the expected date and ticker |
| `state-dir permission denied` | The `state/` directory is owned by another user (e.g. root from a Docker run) | `sudo chown -R "$USER" state/` |

---

This runbook is the executable definition of "smoke passed". When in
doubt, prefer running the runbook over reasoning about whether the
upstream APIs still match the contract.


---

## SKILL: price-history

- Fuente: `staskh/trading_skills` → `.claude/skills/price-history` (MIT)
- Cuándo usarla: Get historical price data (OHLCV) for a stock. Use when user asks about price history, historical data, past performance, price over time, or needs data for chart analysis.
- Código: extraer `code/staskh_trading_skills.tar` y usar `.claude/skills/price-history/` (history.py)

# Price History

Fetch historical OHLCV data from Yahoo Finance.

## Instructions

> **Note:** If `uv` is not installed or `pyproject.toml` is not found, replace `uv run python` with `python` in all commands below.

```bash
uv run python scripts/history.py SYMBOL [--period PERIOD] [--interval INTERVAL]
```

## Arguments

- `SYMBOL` - Ticker symbol
- `--period` - Time period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max (default: 1mo)
- `--interval` - Data interval: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo (default: 1d)

## Output

Returns JSON with:
- `symbol` - Ticker
- `period` - Requested period
- `interval` - Data interval
- `data` - Array of {date, open, high, low, close, volume}

Summarize key price movements, highs/lows, and trends.

## Dependencies

- `yfinance`


## Timezone

All timestamps and time-based calculations must use the `America/New_York` timezone. All JSON output must include `generated_at` (NY time string) and `data_delay` fields.


---

## SKILL: scanner-bullish

- Fuente: `staskh/trading_skills` → `.claude/skills/scanner-bullish` (MIT)
- Cuándo usarla: Scan stocks for bullish trends using technical indicators (SMA, RSI, MACD, ADX). Use when user asks to scan for bullish stocks, find trending stocks, or rank symbols by momentum.
- Código: extraer `code/staskh_trading_skills.tar` y usar `.claude/skills/scanner-bullish/` (scan.py)

# Bullish Scanner

Scans symbols for bullish trends and ranks them by composite score.

## Instructions

> **Note:** If `uv` is not installed or `pyproject.toml` is not found, replace `uv run python` with `python` in all commands below.

```bash
uv run python scripts/scan.py SYMBOLS [--top N] [--period PERIOD]
```

## Arguments

- `SYMBOLS` - Comma-separated ticker symbols (e.g., `AAPL,MSFT,GOOGL,NVDA`)
- `--top` - Number of top results to return (default: 30)
- `--period` - Historical period for analysis: 1mo, 3mo, 6mo (default: 3mo)

## Scoring System (max ~9.5 points)

| Indicator | Condition | Points |
|-----------|-----------|--------|
| SMA20 | Price > SMA20 | +1.0 |
| SMA50 | Price > SMA50 | +1.0 |
| RSI | 50-70 (bullish) | +1.0 |
| | 30-50 (neutral) | +0.5 |
| | <30 (oversold) | +0.25 |
| MACD | MACD > Signal | +1.0 |
| | Histogram rising | +0.5 |
| EMA9/21 | EMA9 > EMA21 (golden cross) | +0.5 |
| | EMA9 < EMA21 (death cross) | -0.25 |
| Dual crossover | Both up, both ≤10 days | +1.0 |
| | Both up, any age | +0.5 |
| | Both down, both ≤10 days | -1.0 |
| | Both down, any age | -0.5 |
| | Directions conflict | -0.5 |
| ADX | >25 with +DI > -DI | +1.5 |
| | +DI > -DI only | +0.5 |
| Momentum | period return / 20 | -1 to +2 |

## Output

Returns JSON with:
- `scan_date` - Timestamp of scan
- `symbols_scanned` - Total symbols analyzed
- `results` - Array sorted by score (highest first):
  - `symbol`, `score`, `price`
  - `next_earnings`, `earnings_timing` (BMO/AMC)
  - `period_return_pct`, `pct_from_sma20`, `pct_from_sma50`
  - `rsi`, `macd`, `macd_signal`, `macd_hist`, `adx`, `dmp`, `dmn`
  - `ema9`, `ema21` — current EMA9 and EMA21 values
  - `ema_crossover` - Most recent EMA9/EMA21 crossover (or `null` if none found):
    - `direction` - `"up"` (EMA9 crossed above EMA21 = bullish) or `"down"` (crossed below = bearish)
    - `days_ago` - Trading days since the crossover bar (0 = happened in the most recent bar)
  - `macd_crossover` - Most recent MACD crossover (or `null` if none found):
    - `direction` - `"up"` (MACD crossed above signal = bullish) or `"down"` (crossed below = bearish)
    - `days_ago` - Trading days since the crossover bar (0 = happened in the most recent bar)
  - `signals` - List of triggered conditions

## EMA Crossover Interpretation

- EMA9 > EMA21 with small `days_ago` (0-5): fresh golden cross — short-term momentum confirmed
- EMA9 just crossed below EMA21: death cross — short-term momentum turning negative
- EMA9 crossover lagging MACD crossover by days: normal — MACD leads, EMA confirms
- `null`: EMA9/21 relationship unchanged throughout the period

## MACD Crossover Interpretation

- `direction: "up"` with small `days_ago` (0-5): fresh bullish crossover — early entry signal
- `direction: "up"` from a deeply negative signal: recovery from correction
- `direction: "down"`: momentum has turned bearish regardless of score
- `null`: no sign change found in the period — trend has been consistently one-directional

## Examples

```bash
# Scan a few symbols
uv run python scripts/scan.py AAPL,MSFT,GOOGL,NVDA,TSLA

# Get top 10 from larger list
uv run python scripts/scan.py AAPL,MSFT,GOOGL,NVDA,TSLA,AMD,AMZN,META --top 10

# Use 6-month lookback
uv run python scripts/scan.py AAPL,MSFT,GOOGL --period 6mo
```

## Interpretation

- Score > 6: Strong bullish trend
- Score 4-6: Moderate bullish
- Score 2-4: Neutral/weak
- Score < 2: Bearish or no trend

## Dependencies

- `pandas`
- `pandas-ta`
- `yfinance`


## Timezone

All timestamps and time-based calculations must use the `America/New_York` timezone. All JSON output must include `generated_at` (NY time string) and `data_delay` fields.


---

## SKILL: sepa-strategy

- Fuente: `himself65/finance-skills` → `plugins/market-analysis/skills/sepa-strategy` (MIT)
- Cuándo usarla: >

# SEPA Strategy Analysis

Analyze stocks using Mark Minervini's SEPA (Specific Entry Point Analysis) framework — a complete system for identifying high-probability growth stock entries with strict risk management.

**Core philosophy:** Buy the right stock, in the right stage, at a precise entry point, with strict risk controls. Win rate is ~50-55% — profitability comes from asymmetric risk/reward (small losses, large gains), not from predicting direction.

> This skill is for educational/analytical purposes only. It does not constitute investment advice. Never execute trades based solely on this analysis.

---

## Step 1: Gather Stock Data

Collect the following data for the stock. Use yfinance or any available market data tool.

| Data needed | Purpose |
|---|---|
| Current price | Trend template check |
| 50-day, 150-day, 200-day moving averages | MA alignment verification |
| 52-week high and low | Price position check |
| 200MA value from 1 month ago and 4-5 months ago | MA200 slope direction |
| 20-day average volume + today's volume | Volume ratio analysis |
| Recent quarterly EPS (last 3-4 quarters) | EPS growth & acceleration |
| Annual EPS (last 3 years) | Long-term growth trend |
| Recent quarterly revenue (last 3-4 quarters) | Revenue growth check |
| Gross margin and net margin trend | Margin health |
| Institutional ownership changes (if available) | Smart money signal |
| RS rating or 12-month relative performance vs S&P 500 | Relative strength |
| Price history for pattern recognition | VCP / chart pattern analysis |

Compute the moving averages, 200MA slope, 52-week range, volume ratio, and relative performance from daily price history in code rather than estimating them — two years of history covers the 200-day MA and its 5-month slope.

If certain data is unavailable, note it and proceed with what you have. Missing RS rating is a significant gap — flag it.

---

## Step 2: Stage Analysis — Identify the Current Stage

Every stock cycles through four stages. Read `references/stage-analysis.md` for full details.

Determine which stage the stock is in:

| Stage | Characteristics | Action |
|---|---|---|
| **Stage 1** — Basing | Price near 200MA, MA flat/declining, MAs tangled, low volume | Do nothing, wait |
| **Stage 2** — Advancing | Making higher highs/lows, bullish MA alignment, volume on up days | **Only stage to buy** |
| **Stage 3** — Topping | Wide swings at highs, frequent false breakouts, heavy volume without progress | Reduce, no new positions |
| **Stage 4** — Declining | Below all MAs, bearish alignment, bounces are selling opportunities | Full cash, stay away |

If the stock is NOT in Stage 2, stop here and tell the user. No further analysis needed.

Within Stage 2, count the base number (how many consolidation-then-breakout cycles have occurred):
- **Base 1-2**: Safest, most upside potential — full position
- **Base 3-4**: Still valid but reduce position size
- **Base 5-6**: Late stage — half position at most
- **Base 7+**: Avoid — likely transitioning to Stage 3

---

## Step 3: Trend Template — 8 Mandatory Conditions

All 8 conditions must be met simultaneously. If any fails, the stock does not qualify. Read `references/trend-template.md` for detailed explanations.

Present results as a checklist:

| # | Condition | Status | Value |
|---|---|---|---|
| 1 | Price > 150MA and Price > 200MA | Pass/Fail | [actual values] |
| 2 | 150MA > 200MA | Pass/Fail | [actual values] |
| 3 | 200MA trending up for ≥1 month (ideally 4-5 months) | Pass/Fail | [slope data] |
| 4 | 50MA > 150MA and 50MA > 200MA | Pass/Fail | [actual values] |
| 5 | Price > 50MA | Pass/Fail | [actual values] |
| 6 | Price ≥ 30% above 52-week low | Pass/Fail | [% above low] |
| 7 | Price within 25% of 52-week high | Pass/Fail | [% from high] |
| 8 | Relative Strength > 70th percentile (prefer 85-90+) | Pass/Fail/Unknown | [RS if available] |

**Memory aid:** Conditions 1-5 = "MA staircase" (Price > 50MA > 150MA > 200MA, 200MA rising). Conditions 6-7 = "Price position" (far from low, near high). Condition 8 = "Relative strength" (market leader).

---

## Step 4: Fundamental Check

Strong fundamentals separate real leaders from momentum-only stocks. Read `references/fundamentals.md` for thresholds and rating criteria.

Check these in order of importance:

1. **Quarterly EPS growth ≥ 20%** (prefer 25-50%+). Below 20% = disqualify.
2. **EPS acceleration**: Current quarter growth > prior quarter growth. Deceleration (even with positive growth) is a warning.
3. **Annual EPS growth ≥ 25%** for each of the past 3 years.
4. **Revenue growth ≥ 15%** annually, ≥ 20-25% quarterly preferred. If EPS grows but revenue doesn't, the growth is likely from cost-cutting (unsustainable).
5. **Margin trend**: Gross and net margins stable or expanding = healthy. Contracting margins even with EPS growth = red flag.
6. **Institutional ownership increasing**: Smart money accumulating = fuel for Stage 2 move.
7. **Catalyst**: New product, FDA approval, major contract, market expansion, etc. Stocks with catalysts can run 50-100%+; without, typically 15-25%.

Rate fundamentals: **A** (EPS >30%, positive, revenue growing) / **B** (15-30%) / **C** (0-15%) / **D** (negative — skip).

---

## Step 5: Pattern Recognition

Identify which consolidation pattern is forming (if any). Read `references/patterns.md` for detailed identification rules for each pattern.

### VCP (Volatility Contraction Pattern) — The Core Pattern

The signature SEPA pattern. Look for these 7 characteristics:

1. Stock must be in Stage 2 uptrend (prerequisite)
2. **Pullback depths decrease** in sequence (e.g., 20% → 12% → 6% → 3%). Minimum 3 contractions, 4-5 ideal.
3. **Volume shrinks** with each contraction. Final contraction shows "Volume Dry-Up" (VDU) — multi-week low volume.
4. **Higher lows** — each pullback bottom is higher than the previous one.
5. **Clear pivot point** — the consolidation range high = resistance level to break.
6. RS > 70 (preferably 85-90+)
7. Market in bull or neutral environment

### Other Valid Patterns

| Pattern | Depth | Duration | Key Feature |
|---|---|---|---|
| Cup with Handle | Cup 12-35%, handle ≤12% | 7-65 weeks | U-shaped base + small handle |
| Flat Base | ≤ 15% | 5-10 weeks | Tight range near prior highs |
| Bull Flag | ≤ 50% of flagpole | 1-5 weeks | Sharp advance + tight drift down |
| High Tight Flag | ≤ 25% after 100%+ advance | 1-4 weeks | Rarest but most powerful |

**All patterns share the same entry rule**: breakout above the pivot point with volume ≥ 1.5x the 20-day average.

---

## Step 6: Entry Point Analysis

Read `references/entry-rules.md` for detailed entry mechanics, true vs false breakout identification, and the pocket pivot alternative.

### Primary Entry: Pivot Point Breakout

- **Pivot point** = the highest price in the consolidation range. This is the supply/demand inflection point.
- **Buy zone** = pivot price to +5% above pivot. This is the only valid entry window.
- **Beyond +5%**: Do NOT chase. Wait for the next setup.
- **Breakout volume**: Must be ≥ 1.5x the 20-day average volume (≥ 2x is strong confirmation).
- **Earnings proximity**: Avoid entering within 2 weeks of an earnings report.

### Breakout Quality Check

| Signal | True Breakout | False Breakout |
|---|---|---|
| Volume | ≥ 1.5x average, big spike | Below average, weak |
| Close | Near the day's high | Falls back below pivot |
| Follow-through | Continues higher next day | Drops back into range |
| Context | VDU preceded breakout | No volume dry-up before |

### Risk/Reward Validation

Before entering, verify:
- **Stop loss distance**: Entry price to stop ≤ 7-8%
- **Reward/risk ratio**: Target profit / stop distance ≥ 2:1 (prefer 3:1)
- If ratio < 2:1, the entry is too risky — skip it.

---

## Step 7: Market Environment Check

Read `references/market-environment.md` for detailed criteria.

The market environment is the master switch for position sizing — it sets the risk per trade used in Step 8:

| Environment | Criteria | Risk Per Trade | Max Positions |
|---|---|---|---|
| **Bull** | S&P 500/Nasdaq above 200MA, breadth expanding, new highs > new lows | 1-2% | 6-8 |
| **Choppy** | Sideways indices, frequent failed breakouts | 0.5-1% | 2-3 |
| **Bear** | Indices below 200MA, >50% of stocks below 200MA | 0% (no new positions) | 0 (all cash) |

Even the best setups fail in bear markets. Holding cash during bear markets IS a winning strategy — preserving capital for the next bull run.

---

## Step 8: Position Sizing & Stop Loss Plan

Read `references/position-sizing.md` for the full formula, examples, stop loss evolution, and pyramiding rules.

### Position Size Formula

```
Shares = (Account Value × Risk Per Trade %) ÷ (Entry Price − Stop Price)
```

**Example**: $100,000 account, 1% risk, buy at $50, stop at $46.50:
- Max loss = $100,000 × 1% = $1,000
- Stop distance = $50 − $46.50 = $3.50
- Shares = $1,000 ÷ $3.50 = **285 shares** ($14,250 = 14.25% of account)

### Stop Loss Evolution (3 phases)

| Phase | Trigger | Action |
|---|---|---|
| Phase 1: Initial | At entry | Hard stop at entry price −7-8%. Non-negotiable. |
| Phase 2: Breakeven | Stock reaches +8% | Sell half, move stop to entry price (breakeven). Trade can no longer lose money. |
| Phase 3: Trailing | Stock reaches +15% | Sell another 25%, trail remaining stop along 20MA. Close below 20MA = exit all. |

**Iron rules**: Stop losses only move UP, never down. Never average down on a losing position. After 3-4 consecutive losses, reduce risk per trade to 0.5%.

### Pyramiding (Adding to Winners)

Only add to winning positions, with decreasing size: 50% initial → 30% at +8% → 20% at next base breakout. Never add to losers.

---

## Step 9: Respond to the User

Present a structured analysis report with these sections:

### Report Structure

1. **Stock & Stage**: Ticker, current price, identified stage, base count if Stage 2
2. **Trend Template Scorecard**: 8-condition checklist with pass/fail and actual values
3. **Fundamental Grade**: A/B/C/D with EPS growth, acceleration status, revenue, margins
4. **Pattern Identified**: Which pattern (VCP, cup-handle, flat base, flag, HTF, or none), with key measurements (contraction depths, volume behavior)
5. **Entry Assessment**:
   - If a valid pattern exists: pivot price, buy zone, breakout volume requirement
   - If not yet formed: what to watch for
   - If already extended: "This has moved beyond the buy zone — wait for the next consolidation"
6. **Market Environment**: Current assessment and the risk per trade it implies
7. **Position Sizing**: Using the formula, show exact shares, stop price, first target, second target, and reward/risk ratio. Ask the user for their account size and risk tolerance if not provided.
8. **Overall Verdict**: One of:
   - **Strong Buy Setup** — all criteria met, actionable now
   - **Watch List** — promising but pattern not yet complete or one condition marginal
   - **Pass** — fails trend template, wrong stage, or poor fundamentals

Always end with the disclaimer that this is educational analysis, not investment advice.

---

## Reference Files

- `references/stage-analysis.md` — Four-stage theory, transition signals, base counting
- `references/trend-template.md` — Detailed 8-condition explanations and memory aids
- `references/fundamentals.md` — EPS, revenue, margins, institutional holdings, catalysts
- `references/patterns.md` — VCP 7 rules, cup-with-handle, flat base, flag, high tight flag, quality vs fake signals
- `references/entry-rules.md` — Pivot point mechanics, buy zone, pocket pivot, true vs false breakout identification
- `references/position-sizing.md` — Formula, stop loss 3-phase evolution, pyramiding, loss handling
- `references/market-environment.md` — Bull/choppy/bear criteria and position adjustment rules

### Referencia: README.md

# SEPA Strategy Analysis

Analyze stocks using Mark Minervini's SEPA (Specific Entry Point Analysis) methodology — a complete framework for identifying high-probability growth stock entries with strict risk management.

## Triggers

- Mentions of SEPA, Minervini, superperformance, trend template
- VCP (Volatility Contraction Pattern), stage analysis, Stage 2 uptrend
- Pivot point breakout, growth stock screening
- Moving average alignment checks (bullish stacking)
- Consolidation pattern analysis (cup-with-handle, flat base, flag, high tight flag)
- Position sizing with risk-based calculations
- "Should I buy this stock?" or "Is this a good setup?" in growth/momentum context

## What It Does

1. **Stage Analysis** — determines if a stock is in Stage 2 (the only buyable stage) and counts bases
2. **Trend Template** — evaluates 8 mandatory conditions (MA hierarchy, price position, relative strength)
3. **Fundamental Check** — grades EPS growth/acceleration, revenue, margins, institutional ownership
4. **Pattern Recognition** — identifies VCP, cup-with-handle, flat base, flag, and high tight flag patterns
5. **Entry Assessment** — calculates pivot point, buy zone (0-5% above pivot), breakout volume requirement
6. **Position Sizing** — risk-based share calculation, 3-phase stop loss plan, pyramiding rules
7. **Market Environment** — adjusts strategy based on bull/choppy/bear conditions

## Platform

All (works on Claude Code, Claude.ai, and other agents)

## Setup

No special setup required. Works best with access to market data tools (yfinance) for real-time prices and fundamentals.

## Reference Files

| File | Contents |
|---|---|
| `references/stage-analysis.md` | Four-stage theory, transition signals, base counting |
| `references/trend-template.md` | 8 mandatory conditions with detailed explanations |
| `references/fundamentals.md` | EPS, revenue, margins, institutional holdings, catalysts |
| `references/patterns.md` | VCP 7 rules, cup-with-handle, flat base, flag, high tight flag |
| `references/entry-rules.md` | Pivot point mechanics, buy zone, pocket pivot, true vs false breakout |
| `references/position-sizing.md` | Position formula, stop loss phases, pyramiding, loss management |
| `references/market-environment.md` | Bull/choppy/bear criteria and position adjustment |

## Disclaimer

This skill is for educational and informational purposes only. It does not constitute financial advice. Stock investing involves risk. Always do your own research and consult a qualified financial advisor before making investment decisions.

### Referencia: references/entry-rules.md

# Entry Point Rules

"Specific Entry Point" is the core of the SEPA name. This isn't about "looks roughly good, let's buy" — it's about entering at a very specific price level with defined risk.

## The Pivot Point

**Minervini's definition**: Below the pivot, supply equals or exceeds demand. Above the pivot, demand overwhelms remaining supply. The pivot is not just a technical resistance level — it is the true supply/demand inflection point.

The pivot point = the highest price within the consolidation pattern (VCP, cup-handle, flat base, etc.).

## Buy Zone: Pivot to +5%

- **Valid entry window**: From the pivot price to 5% above the pivot
- **Beyond +5%**: Do NOT enter. Minervini calls this "buying someone else's profit." The stop distance stays the same but profit potential shrinks — the risk/reward ratio deteriorates.
- **Missed it?** Wait for the next consolidation and breakout. There will be another opportunity.

## Volume Confirmation

| Breakout Volume vs 20-Day Average | Interpretation |
|---|---|
| ≥ 2.0x | Strong institutional buying — high confidence |
| ≥ 1.5x | Standard confirmation — normal entry |
| 1.2x – 1.5x | Marginal — enter with caution, tight stop |
| < 1.2x | Insufficient — high probability of false breakout, avoid |

## True Breakout vs False Breakout

### True Breakout Characteristics
- Breakout-day volume is a significant spike (≥ 1.5x average)
- Stock closes near the day's high (strong buying into the close)
- Volume Dry-Up preceded the breakout (supply was exhausted)
- Follow-through: stock continues higher the next day/week
- The breakout candle is decisive — large body, small upper wick

### False Breakout Characteristics
- Volume is weak (below or barely at average)
- Stock touches the pivot but closes back below it
- No VDU preceded the attempt (sellers still present)
- Stock falls back into the consolidation range within days
- Long upper wick on the breakout candle (rejection at resistance)

## Alternative Entry: Pocket Pivot (Advanced)

For experienced traders, the pocket pivot allows earlier entry during the consolidation phase:

- **Trigger**: On an up day during consolidation, the day's volume exceeds the volume of any down day in the previous 10 sessions
- **Entry point**: Near the 10MA or 20MA within the consolidation
- **Stop**: 1-2% below the pocket pivot day's low (tighter than standard)
- **Risk**: Higher skill requirement, more subjective judgment
- **Benefit**: Earlier entry = lower cost basis = better risk/reward if the breakout subsequently succeeds

Pocket pivots are appropriate for traders with experience reading volume patterns. Beginners should stick with the standard pivot point breakout.

## Five Entry Rules (Iron Laws)

1. **Buy within 0-5% of the pivot point** — the only reasonable entry window
2. **Never chase beyond 5% above the pivot** — missed opportunity, wait for next one
3. **Never enter during consolidation without a pocket pivot signal** — you'll likely get stopped out during the next contraction
4. **Be cautious if breakout volume is below 1.5x average** — the biggest warning sign for false breakouts
5. **Avoid entering within 2 weeks of an earnings report** — earnings are binary events; even perfect setups can gap down on a miss

## Risk/Reward Validation

Before placing any trade, calculate:

```
Reward/Risk Ratio = (Target Price − Entry Price) / (Entry Price − Stop Price)
```

- **Minimum**: 2:1 (e.g., risk $3.50 to make $7.00)
- **Preferred**: 3:1 or better
- **If < 2:1**: Do not take the trade. The math doesn't work even with 50% win rate.

Example: Buy at $50, stop at $46.50, target at $57.50
- Risk = $50 − $46.50 = $3.50
- Reward = $57.50 − $50 = $7.50
- Ratio = $7.50 / $3.50 = **2.14:1** (meets minimum)

### Referencia: references/fundamentals.md

# Fundamental Requirements

SEPA is not purely technical. Historical data shows 75% of superperformer stocks had quarterly EPS growth exceeding 20% before their largest advance. Fundamentals separate real leaders from momentum-only plays.

## EPS (Earnings Per Share) Growth

### Quarterly EPS

| Tier | Growth Rate | Significance |
|---|---|---|
| Minimum threshold | ≥ 20% | Below this = disqualify |
| Preferred range | 25% – 50% | Most successful cases cluster here |
| Superperformers | 50%+ | Seen in the biggest winners |

### EPS Acceleration — The Most Critical Factor

Raw growth isn't enough. The growth rate must be **accelerating**: this quarter's EPS growth rate > last quarter's EPS growth rate.

- Last quarter +20% → this quarter +28% = **accelerating** (bullish)
- Last quarter +30% → this quarter +22% = **decelerating** (warning signal, even though +22% looks decent)

Deceleration often precedes price peaks. The market prices in future expectations, so slowing growth can trigger selling even if absolute numbers look fine.

### Annual EPS

- Past 3 years: each year ≥ 25% growth
- Most recent year's growth rate > prior year's rate (annual acceleration)
- Avoid one-off spikes (1-2 quarters of high growth that isn't sustained)

## Revenue Growth

| Tier | Growth Rate | Notes |
|---|---|---|
| Minimum | Annual ≥ 15% | Below this, growth sustainability is questionable |
| Preferred | Quarterly ≥ 20-25% | Strong real demand signal |
| Red flag | EPS growing but revenue flat/declining | "Fake growth" — driven by cost-cutting, layoffs, or buybacks, not real business expansion |

**Why revenue and EPS must both grow**: If EPS grows 30% but revenue only grows 2%, the growth comes from cost optimization rather than genuine business expansion. This is unsustainable and Minervini calls it "fake growth."

## Profit Margins

Margins are often overlooked but critically important:

**Healthy signs:**
- Gross margin stable or expanding quarter-over-quarter
- Net margin stable or expanding
- Indicates pricing power and strengthening competitive advantage

**Danger signs:**
- Gross margin contracting quarter-over-quarter
- Even if EPS is still growing, be cautious
- Indicates intensifying competition or loss of pricing power
- Growth sustained by scale rather than efficiency — may collapse suddenly

## Institutional Ownership

Institutional buying is the fuel that drives sustained Stage 2 advances. Retail money alone cannot push a stock through a multi-month uptrend.

**What to look for:**
- Number of institutional holders increasing quarter-over-quarter
- Top-tier funds and hedge funds initiating positions
- Check 13F filings (quarterly institutional disclosure in the US)
- Tools: Finviz, Whalewisdom, WhalePortfolio

**Institutional ownership increasing = real demand. Decreasing = distribution warning.**

## Catalysts (Bonus Factor)

Catalysts can dramatically amplify a move:

- New product achieving major success
- New CEO bringing transformational strategy
- FDA drug approval
- Winning large government or enterprise contracts
- Entering entirely new markets
- Disruptive technology breakthrough

**With catalyst**: potential 50-100%+ advance
**Without catalyst**: typically 15-25% before stalling

## Fundamental Rating Summary

| Grade | EPS Growth | EPS Status | Revenue | Recommendation |
|---|---|---|---|---|
| **A** | > 30% | Positive, accelerating | Growing in sync | Top-tier growth stock — prioritize |
| **B** | 15-30% | Positive | Growing | Solid growth stock |
| **C** | 0-15% | Positive | Modest growth | Ordinary — lower priority |
| **D** | Negative | Losing money | Declining | Does not meet SEPA criteria — skip |

### Referencia: references/market-environment.md

# Market Environment Assessment

The market environment is the master switch for all SEPA activity. Even the best individual stock setups fail at high rates in bear markets. Assessing the environment determines whether to trade at all, and how aggressively.

## Three Market Environments

### Bull Market (Indices Strong)

**Identification criteria:**
- S&P 500 and Nasdaq above their 200-day moving averages
- Market breadth expanding (more stocks advancing than declining)
- New 52-week highs consistently outnumber new 52-week lows
- Breakouts generally follow through (success rate high)

**SEPA parameters:**
- Risk per trade: 1-2% of account
- Position size: S-tier setups get 10-15%, A-tier get 5-10%
- Maximum concurrent positions: 6-8
- Strategy: Aggressive offense — actively seek and enter quality setups

### Choppy / Sideways Market (Direction Unclear)

**Identification criteria:**
- Indices oscillating without clear direction
- Frequent failed breakouts — stocks break out then reverse
- Roughly equal numbers of advancing and declining stocks
- Mixed signals: some sectors strong, others weak

**SEPA parameters:**
- Risk per trade: 0.5-1% of account
- Position size: Only take A+ grade setups, enter at half normal size
- Maximum concurrent positions: 2-3
- Strategy: Cautious observation — trade only the best of the best, smaller

### Bear Market (Sustained Decline)

**Identification criteria:**
- Major indices below their 200-day moving averages
- More than 50% of stocks trading below their 200-day MAs
- New 52-week lows consistently > new 52-week highs
- Even quality breakouts fail or reverse quickly
- Defensive sectors (utilities, staples) outperforming growth

**SEPA parameters:**
- Risk per trade: 0% (no new positions)
- Position size: Gradually exit to 100% cash
- Maximum concurrent positions: 0
- Strategy: Full cash. Preserve capital. Wait for the next bull market.

## Key Principle

**Holding cash during a bear market IS a profitable strategy.** While others lose 30-50% trying to "find the bottom," cash preservation means you have full ammunition when the bull market returns.

Minervini's rule: "Wait for the market to offer opportunity, then strike with full force."

## Quick Environment Check

When assessing the market, check these indicators:

1. **S&P 500 position relative to 200MA** — above = bullish, below = bearish
2. **Nasdaq Composite position relative to 200MA** — tech sector health
3. **Advance/Decline line** — broadening participation = healthy; narrowing = deteriorating
4. **New Highs vs New Lows** — consistent new highs > new lows = bull; vice versa = bear
5. **VIX level** — sustained above 25-30 suggests elevated fear/uncertainty
6. **Recent breakout success rate** — if your last 5 breakouts all failed, the market is likely the problem, not your stock selection

## Adjusting From Bull to Bear (Gradual Process)

The transition from bull to bear rarely happens overnight. Watch for these progression signals:

1. Leading stocks start failing on breakouts
2. More stocks hitting 52-week lows
3. Indices start spending more time below 50MA
4. Former leaders break below 50MA, then 200MA
5. Market rallies on decreasing volume
6. Indices breach 200MA

**Response**: At each step, gradually reduce exposure. Don't wait for a full bear confirmation to start protecting capital. By the time everyone agrees it's a bear market, the damage is already done.

### Referencia: references/patterns.md

# Consolidation Patterns

All SEPA patterns share the same entry logic: **breakout above the pivot point + volume confirmation ≥ 1.5x 20-day average**.

## Pattern 1: VCP (Volatility Contraction Pattern) — The Core Pattern

VCP is Minervini's signature and most important pattern. Think of price as a spring being compressed: each pullback compresses it tighter (smaller amplitude). When the spring reaches maximum compression (supply exhaustion), it releases forcefully — that's the VCP breakout.

### 7 Identification Rules

**Rule 1: Stage 2 uptrend (prerequisite)**
Price above 50MA/150MA/200MA with bullish alignment. Without this, any contraction is just a bounce in a downtrend, not a VCP.

**Rule 2: Pullback depths decrease in sequence (core feature)**
Typical example: 20% → 12% → 6% → 3%. Each contraction is roughly 20-30% smaller than the previous one. Minimum 3 contractions; 4-5 is ideal. If the second pullback is deeper than the first, it's NOT a VCP.

**Rule 3: Volume shrinks in sync, ending with "Volume Dry-Up" (VDU)**
Volume decreases with each successive pullback. During the final contraction, volume drops to a multi-week low — this is the VDU signal, indicating supply exhaustion (sellers are nearly depleted).

**Rule 4: Higher lows**
Each pullback bottom is higher than the previous one. This proves buyers are stepping in at progressively higher prices — institutions accumulating at each dip.

**Rule 5: Clear pivot point**
The high of the consolidation range = the pivot point = resistance. The VCP breakout occurs when price crosses this level.

**Rule 6: RS > 70 (preferably 85-90+)**
Ensures the stock is a genuine market leader. Leader VCPs have far higher breakout success rates than laggard VCPs.

**Rule 7: Market in bull or neutral environment**
Major indices above their MAs, market breadth expanding. VCP breakout failure rates spike in bear markets.

### Volume + Price Interpretation

Volume shrinkage alone doesn't prove selling pressure is diminishing. The correct interpretation requires both price and volume:

| Price Action | Volume | True Meaning | Implication |
|---|---|---|---|
| Shallower pullbacks + higher lows | Shrinking | Supply exhausting, shares locked up | Ideal VCP — prepare to enter |
| Continued decline | Shrinking | Buyers retreating, stock bleeding | Dangerous — NOT a VCP |
| Sideways | Shrinking | Both sides waiting, direction unclear | Watch and wait |
| Breakout above pivot | Large spike ≥ 1.5x average | Demand surging, institutions buying | Confirmed signal — enter |

### Quality VCP vs Fake VCP

**Quality VCP:**
- Pullback depths strictly decreasing (20% → 12% → 6% → 3%)
- Each low higher than the previous
- Volume decreasing with each pullback
- Clear VDU in the final contraction
- Overall in a clear uptrend
- RS ranking near the top
- Breakout with strong volume (≥ 1.5x average)

**Fake VCP (common traps):**
- Irregular pullback depths (sometimes bigger, sometimes smaller)
- Lows not progressively higher (or moving lower)
- Volume not shrinking, or actually expanding on declines
- Stock in a downtrend overall
- Only 2 contractions (insufficient structure)
- Breakout with weak volume (below average)
- Price quickly falls back below the pivot after "breaking out"

---

## Pattern 2: Cup with Handle

- **Cup**: U-shaped price recovery, depth 12-35% from peak to trough
- **Handle**: Small pullback after the cup completes, ≤ 1/3 of cup depth (typically ≤ 12%)
- **Volume**: Low at cup bottom, even lower during handle, large on breakout
- **Duration**: 7-65 weeks total
- **Pivot**: Top of the handle's range
- **Strength**: 4/5 — works well for stocks in mature uptrends

The cup should be U-shaped (rounded bottom), not V-shaped (too sharp, no proper basing).

---

## Pattern 3: Flat Base (Platform Consolidation)

- **Depth**: ≤ 15% from high to low (very tight range)
- **Duration**: 5-10 weeks
- **Volume**: Contracts during the consolidation, expands on breakout
- **Pivot**: Top of the flat range
- **Strength**: 3/5 — represents a strong stock taking a brief rest near highs

Flat bases often appear in stocks that are too strong to pull back much. The tighter the range, the better.

---

## Pattern 4: Bull Flag

- **Flagpole**: Sharp advance of 25%+ (steep, fast move up)
- **Flag**: Slight downward drift or tight consolidation, pullback ≤ 50% of flagpole
- **Volume**: Flag portion shows shrinking volume; breakout shows volume expansion
- **Duration**: 1-5 weeks for the flag portion
- **Pivot**: Top of the flag range
- **Strength**: 4/5 — good continuation pattern after strong initial moves

---

## Pattern 5: High Tight Flag (The Rarest and Most Powerful)

- **Prerequisite**: Stock must have already advanced 100%+ in 4-8 weeks
- **Flag**: Pullback ≤ 25% from the peak, extremely tight
- **Volume**: Extremely dry during the flag; massive on breakout
- **Duration**: 1-4 weeks for the flag
- **Strength**: 5/5 — rare but highest success rate
- **Note**: These are uncommon. When they appear, they often lead to further massive advances.

---

## Universal Entry Rules for All Patterns

1. Price breaks above the pivot point (consolidation range high)
2. Breakout-day volume ≥ 1.5x the 20-day average volume (the bigger the better)
3. Stop loss at 5-10% below entry price (specific level depends on pattern structure)

### Referencia: references/position-sizing.md

# Position Sizing, Stop Loss & Pyramiding

This is the most critical part of the entire SEPA system. Minervini: "Not losing big is the only prerequisite for winning big." You cannot control how much a stock goes up, but you can fully control how much you lose.

**Key insight**: Minervini discovered that if he had tightened his stop from 15% to 10% early in his career, a losing account would have been profitable (+72%). This discovery made the 7-8% stop loss a sacred, inviolable rule.

## Position Size Formula

The logic: first determine the maximum dollar amount you're willing to lose, then work backward to determine how many shares to buy. **Don't decide position size by looking at the stock — decide it by fixing your risk first.**

```
Shares = (Account Value × Risk Per Trade %) ÷ (Entry Price − Stop Price)
```

### Complete Calculation Example ($100,000 account, 1% risk per trade)

1. **Maximum loss amount** = $100,000 × 1% = **$1,000** (the most this trade can lose)
2. **Entry price**: $50.00. Stop at −7% = $46.50. Stop distance = $50 − $46.50 = **$3.50/share**
3. **Shares** = $1,000 ÷ $3.50 = **285 shares**
4. **Total position** = 285 × $50 = **$14,250** (14.25% of account — reasonable)
5. **Stop price**: $46.50 (exit immediately if touched)
6. **Target 1**: $50 × 1.08 = $54.00 (+8%, sell half)
7. **Target 2**: $50 × 1.15 = $57.50 (+15%, sell another 25%)
8. **Reward/Risk** (to target 2): ($57.50 − $50) / ($50 − $46.50) = 7.5 / 3.5 ≈ **2.14:1** (meets minimum)

## Stop Loss Three-Phase Evolution

### Phase 1: Initial Hard Stop (At Entry)

- Set stop loss order immediately upon entry: **entry price minus 7-8%**
- Non-negotiable. No "let's see how it goes." Entry = stop is set.
- If triggered, exit immediately. Don't ask why, don't hesitate.
- The stop being hit doesn't mean you failed — it means this trade's premise didn't hold. That's normal probability.

### Phase 2: Move to Breakeven (At +8% Profit)

- Sell half the position to lock in profit
- Move stop loss from −7% up to the **entry price (breakeven)**
- After this point, this trade cannot lose money — capital is safe
- The remaining half is now a "free trade" — playing with house money

### Phase 3: Trailing Stop (At +15% Profit)

- Sell another 25% of the original position
- Trail the remaining 25% using the **20-day moving average**
- Update stop weekly to 1-2% below the current 20MA
- When price closes below 20MA, exit all remaining shares — let profits run as long as the trend holds

### Special Case: Rapid Advance

If the stock surges 20-25% in a short period (obvious acceleration), tighten the stop to below the **10MA** instead of the 20MA. This prevents large profit give-back in overextended moves.

### Stop Level Summary

| Scenario | Stop Placement |
|---|---|
| At entry | Entry price − 7-8% |
| Stock at +8% (after selling half) | Entry price (breakeven) |
| Stock at +15% (after selling 25% more) | 1-2% below 20MA, updated weekly |
| Rapid surge (+20-25% quickly) | Tighten to below 10MA |
| Close below 50MA | Serious warning — consider exiting everything |

## Iron Rules

1. **Stop losses only move UP, never down.** Moving a stop down "to give it more room" is how small losses become catastrophic ones.
2. **Never average down on a losing position.** Adding to a loser is the fastest path to account destruction.
3. **After 3-4 consecutive losses**, reduce risk per trade from 1% to 0.5% and cut the number of positions. Determine whether the issue is your execution or the market environment before resuming normal size.
4. **Average loss should be 4-5%, hard cap at 10%.** VCP's precise entry often allows exits at 3-5% loss. The smaller the average loss, the fewer winning trades needed to recover.

## Pyramiding (Adding to Winners)

Pyramiding = adding to a winning position with decreasing size. This is the opposite of averaging down.

### How to Pyramid

| Tranche | Timing | Size | Price (Example) | Shares | Amount |
|---|---|---|---|---|---|
| 1st (Main) | VCP breakout at pivot | 50% of target | $50.00 | 100 | $5,000 |
| 2nd (Add) | +8%, pullback to 20MA | 30% of target | $54.00 | 60 | $3,240 |
| 3rd (Add) | Next base breakout | 20% of target | $58.00 | 35 | $2,030 |
| **Total** | — | 100% | Avg ≈ $53.20 | 195 | $10,270 |

### Why Pyramiding Works

- The largest position (100 shares) is at the lowest cost ($50) — minimum risk, maximum cushion
- Even if tranches 2 and 3 both hit stops (combined loss ~$263), tranche 1's locked profit from the +8% partial sell ($400) covers the loss
- You only add more money when the market proves you right — each addition has a new breakout signal confirming the trend

### Why Averaging Down Fails

- Each addition is at a lower price = the market is proving you wrong
- "$60 → $40, that's down a lot, must be near the bottom" — then it goes to $20, then $5
- "My average cost went from $60 to $52" is an illusion — your real total loss is expanding exponentially
- You're doubling down on a failed thesis
- This is the single fastest way to destroy a trading account

## Handling Losing Trades

SEPA wins only ~50-55% of the time. Nearly half of all trades lose money. This is expected and by design.

### Loss Review Framework (Three Questions)

**Q1: Was it an execution problem or a strategy problem?**
- Execution problem (chased above +5%, didn't set stop, entered with weak volume, entered before earnings) → fix the habit, the strategy isn't wrong
- Strategy problem (misidentified the pattern, entered without trend template confirmation) → study more historical examples to improve recognition

**Q2: Was it a "good loss" or a "bad loss"?**
- Good loss: Followed all rules, market just didn't cooperate, exited at stop — **this is a normal cost of doing business, change nothing**
- Bad loss: Broke rules (no stop, averaged down, chased) — **this is what must be eliminated**

**Q3: Was it the individual stock or the overall market?**
- If recent breakouts are frequently failing, check the market first: indices below MAs? Breadth deteriorating?
- If the market environment has changed, pause trading and wait for improvement rather than forcing more trades

### The Casino Analogy

A casino doesn't win every hand — it wins through mathematical edge (favorable odds) over thousands of hands. SEPA works the same way:
- Win trades average +15-30%
- Lose trades average −5-7%
- Over 10 trades at 50% win rate: 5 × 15% − 5 × 6% = **+45% net**
- A retail trader with 55% win rate but no discipline: 5.5 × 5% − 4.5 × 12% = **−26.5% net**

The win rate matters less than the win/loss size ratio.

### Referencia: references/stage-analysis.md

# Stage Analysis — The Four Stages of Stock Price Cycles

Stan Weinstein's 4-stage theory (1988), integrated into SEPA by Minervini. Every stock continuously cycles through these four stages. Identifying the current stage is the starting point for all decisions.

## Stage 1: Basing / Accumulation

- Price oscillates sideways around the 200MA
- 200MA is flat or declining
- Moving averages are tangled (no clear order)
- Volume dries up — the market has forgotten this stock
- Institutions quietly accumulate shares
- **Duration**: Can last 1-3 years
- **Action**: Do nothing. Wait for transition signals.

## Stage 2: Advancing / Markup (The Only Buy Stage)

- Stock makes consistently higher highs and higher lows
- Perfect bullish MA alignment: Price > 50MA > 150MA > 200MA
- Volume expands on up moves, contracts on pullbacks
- VCP and other consolidation patterns appear repeatedly
- Typically goes through 3-6 consolidation bases
- **This is where 100% of SEPA trades occur**
- **Action**: Actively look for entry points on each base breakout

### Counting Bases Within Stage 2

Each completed "consolidation → breakout" cycle = one base. This tracks how far along Stage 2 has progressed:

| Base # | Safety | Position Size | Notes |
|---|---|---|---|
| 1-2 | Highest | Full position | Early Stage 2, maximum upside |
| 3-4 | Moderate | Reduce slightly | Trend still valid, more caution needed |
| 5-6 | Low | Half position max | Stage 2 maturing, topping risk rising |
| 7+ | Dangerous | Avoid | Likely transitioning to Stage 3 |

**How to count**: The first consolidation breakout after transitioning from Stage 1 to Stage 2 = Base 1 (the safest).

## Stage 3: Topping / Distribution

- High-level wide swings, increased volatility
- Frequent false breakouts
- Heavy volume at highs without upward progress (institutions distributing)
- Media attention peaks, retail sentiment most euphoric
- **Action**: Gradually reduce positions. Do not open new ones.

## Stage 4: Declining / Markdown

- Sustained decline, bearish MA alignment
- Bounces are selling opportunities, not buying opportunities
- "It's down 60%, must be near the bottom" — the most dangerous thought. A stock at $40 (from $100) can still go to $10.
- **Action**: Fully exit. Hold cash. Wait for the next Stage 1→2 transition.

## Stage 1 → Stage 2 Transition Signals (Precursors to the Best Buy Points)

1. **200MA shifts from declining → flat → starting to slope upward**
2. **Price breaks above the consolidation range on increased volume**
3. **50MA crosses above 150MA or 200MA (golden cross)**

These signals don't guarantee a Stage 2 move, but they're necessary preconditions. The first VCP breakout after these signals appear is typically the highest-probability entry.

### Referencia: references/trend-template.md

# Trend Template — 8 Mandatory Conditions

The trend template is a pre-entry qualification filter. All 8 conditions must be satisfied simultaneously. If any condition fails, skip the stock entirely — don't waste time on deeper analysis.

## The 8 Conditions

### MA Staircase (Conditions 1-5)

These five conditions establish that the stock has a healthy, stacked bullish moving average alignment.

**Condition 1: Price > 150MA AND Price > 200MA**
The stock must be trading above both its 150-day and 200-day moving averages. This confirms it is in a long-term uptrend, not struggling below key support levels.

**Condition 2: 150MA > 200MA**
The 150-day MA must be above the 200-day MA. This is a critical component of the bullish MA hierarchy.

**Condition 3: 200MA trending up for at least 1 month (ideally 4-5 months)**
The 200MA slope must be positive and sustained. This confirms the long-term trend is healthy and not just a temporary bounce. To check: compare today's 200MA value with the value from 1 month ago (and ideally 4-5 months ago). It should be higher now.

**Condition 4: 50MA > 150MA AND 50MA > 200MA**
The short-term moving average leads the pack. This shows strong recent momentum.

**Condition 5: Price > 50MA**
The stock is above its short-term trend line. This confirms even near-term momentum is positive.

**Summary**: The complete MA hierarchy is: **Price > 50MA > 150MA > 200MA**, with 200MA sloping upward.

### Price Position (Conditions 6-7)

**Condition 6: Price ≥ 30% above 52-week low (the more the better)**
This proves the stock has truly left its bottom and is in a genuine uptrend — not just a minor bounce off lows. Calculate as: (Current Price / 52-Week Low − 1) × 100%.

**Condition 7: Price within 25% of 52-week high (the closer the better)**
The stock should be trading near its highs, not 50% off a peak. Ideally it's near or making new 52-week highs. Calculate as: (1 − Current Price / 52-Week High) × 100%. Must be ≤ 25%.

### Relative Strength (Condition 8)

**Condition 8: Relative Strength ranking > 70th percentile (prefer 85-90+)**
Only trade true market leaders. RS measures how a stock's 12-month price performance ranks against the entire market. Stocks in the top 15% (RS > 85) are real leaders; those below the 70th percentile are laggards.

**Sources for RS**: IBD RS Rating, MarketSmith, TradingView "Relative Strength" indicator, or calculate manually by comparing 12-month return to S&P 500.

This is one of the conditions most commonly missing from screenings, yet it is one of Minervini's most emphasized filters.

## Memory Aid

Three sentences to remember all 8 conditions:

1. **MA Staircase** (Conditions 1-5): Price > 50MA > 150MA > 200MA, with 200MA rising
2. **Price Position** (Conditions 6-7): Far from the low (≥30%), near the high (≤25% away)
3. **Relative Strength** (Condition 8): Market leader, RS > 70th percentile

## Common Gaps in Screening Tools

Many stock screeners implement conditions 1-5 well but miss:
- **200MA uptrend duration** (Condition 3) — most screeners only check if MA200 is rising today, not for sustained periods
- **Relative Strength** (Condition 8) — the single most commonly missing condition; without it, you may trade mediocre stocks with good chart patterns but weak relative performance


---

## SKILL: stock-quote

- Fuente: `staskh/trading_skills` → `.claude/skills/stock-quote` (MIT)
- Cuándo usarla: Get real-time stock quote with price, volume, change, market cap, and 52-week range for any ticker symbol. Use when user asks about current stock price, quote, or basic stock info.
- Código: extraer `code/staskh_trading_skills.tar` y usar `.claude/skills/stock-quote/` (quote.py)

# Stock Quote

Fetch current stock data from Yahoo Finance.

## Instructions

> **Note:** If `uv` is not installed or `pyproject.toml` is not found, replace `uv run python` with `python` in all commands below.

Run the quote script with the ticker symbol:

```bash
uv run python scripts/quote.py SYMBOL
```

Replace SYMBOL with the requested ticker (e.g., AAPL, MSFT, TSLA, SPY).

## Output

The script outputs JSON with:
- symbol, name, price, change, change_percent
- as_of_session - the trading date `price`/`change` belong to (YYYY-MM-DD, from Yahoo's regular-session timestamp; null if Yahoo omits it)
- market_open_now - whether the NYSE regular session is open right now
- market_state - Yahoo's session state: `PRE`, `REGULAR`, `POST`, `CLOSED` (also `PREPRE`/`POSTPOST`)
- pre_market, post_market - `{price, change, change_percent, time}` for extended-hours trading, or null. `change` is measured from the last regular close; `time` is the ET timestamp of that print
- volume, avg_volume, market_cap
- high_52w, low_52w, pe_ratio, forward_pe, dividend_yield, beta

Present the data in a readable format. Highlight significant moves (>2% change).

**Before presenting `change`/`change_percent` as "today's move", check `as_of_session` against today's NY calendar date.** Before the regular session opens (`market_open_now: false` and `as_of_session` is a prior date), Yahoo's change fields still describe the *last completed session* (yesterday's close vs. the day before) — not intraday movement in the still-unopened current session. In that case, label it as "as of `<as_of_session>` close", not "today". Once `as_of_session` equals today's date, `change`/`change_percent` are genuinely intraday.

**Report the extended-hours move when there is one.** Pre-market (`market_state: PRE`), lead with `pre_market` as the current move, then give the regular `change` as the prior session's close. After the close (`POST`), show `post_market` alongside the day's regular move. Check each block's `time`: a `post_market` print from the previous evening seen during pre-market is last night's move, not this morning's.

## Dependencies

- `yfinance`


## Timezone

All timestamps and time-based calculations must use the `America/New_York` timezone. All JSON output must include `generated_at` (NY time string) and `data_delay` fields.


---

## SKILL: stockbee-20pct-study

- Fuente: `tradermonty/claude-trading-skills` → `skills/stockbee-20pct-study` (MIT)
- Cuándo usarla: Build and maintain a Stockbee-style daily 20% mover study for US equities by scanning +20%/-20% movers, classifying catalysts and setup context, updating forward outcomes, and summarizing cohort patterns. Use when the user asks to run a daily 20% study, backfill historical 20% movers, find recurring edge patterns, or build a model book of explosive market moves.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/stockbee-20pct-study/` (requirements.txt, fmp_client.py, run_20pct_study.py)

# Stockbee 20% Study

Build a daily event study of US equities that moved +20% or -20% over a defined window. Convert large movers into structured study records, classify the catalyst and chart context, update forward outcomes, and summarize recurring patterns for research.

This skill is a research, model-book, and setup-fluency workflow. It does not generate buy/sell signals, place orders, or output broker execution instructions.

## When to Use

- User wants to run a Stockbee-style daily 20% mover study
- User asks which stocks moved +20% or -20% today, this week, or over a configurable lookback window
- User wants to backfill historical 20% movers and study what happened next
- User wants to identify continuation, reversal, exhaustion, or theme-cluster patterns
- User wants to build a model book of explosive winners, major failures, and failed low-quality pops
- User wants edge hints for downstream strategy research rather than immediate trade signals

## Prerequisites

- Python 3.9+
- FMP API key for live US universe scans, or offline OHLCV JSON via `--prices-json`
- Optional structured news/catalyst JSON for higher-quality catalyst classification
- Recommended market regime artifact from `market-regime-daily`
- Recommended local state path: `state/stockbee/20pct_study_events.jsonl`

## Workflow

### Step 1: Scan for 20% Movers

Run after the US market close, or against the latest complete daily bar in an offline OHLCV file.

```bash
python3 skills/stockbee-20pct-study/scripts/run_20pct_study.py scan \
  --fmp-universe \
  --max-symbols 300 \
  --as-of 2026-06-28 \
  --lookback-days 5 \
  --min-abs-return-pct 20 \
  --min-price 5 \
  --min-dollar-volume 20000000 \
  --include-down-movers \
  --state-file state/stockbee/20pct_study_events.jsonl \
  --output-dir reports/
```

Use offline data instead of FMP:

```bash
python3 skills/stockbee-20pct-study/scripts/run_20pct_study.py scan \
  --prices-json data/us_daily_ohlcv.json \
  --as-of 2026-06-28 \
  --lookback-days 5 \
  --include-down-movers \
  --state-file state/stockbee/20pct_study_events.jsonl \
  --output-dir reports/
```

### Step 2: Enrich and Classify Events

Use structured catalyst data when available. The enrichment step is best-effort: if no news record is found, the event remains a price-only `NO_CLEAR_NEWS` study record.

```bash
python3 skills/stockbee-20pct-study/scripts/run_20pct_study.py enrich \
  --events-json reports/stockbee_20pct_events_YYYY-MM-DD_HHMMSS.json \
  --news-json data/catalysts_YYYY-MM-DD.json \
  --market-regime reports/market_regime_latest.json \
  --state-file state/stockbee/20pct_study_events.jsonl \
  --output-dir reports/
```

### Step 3: Update Matured Forward Outcomes

Update 1-day, 3-day, 5-day, 10-day, and 20-day forward outcomes after enough future bars exist.

```bash
python3 skills/stockbee-20pct-study/scripts/run_20pct_study.py update-outcomes \
  --prices-json data/us_daily_ohlcv.json \
  --state-file state/stockbee/20pct_study_events.jsonl \
  --horizons 1,3,5,10,20 \
  --output-dir reports/
```

The update records close return, MFE, MAE, direction-adjusted continuation return, and outcome tags.

### Step 4: Summarize Cohorts

```bash
python3 skills/stockbee-20pct-study/scripts/run_20pct_study.py summarize \
  --state-file state/stockbee/20pct_study_events.jsonl \
  --group-by direction,catalyst.label,technical_context.pattern_label,technical_context.close_quality \
  --min-sample 10 \
  --output-dir reports/
```

Treat `rule_candidates` and exported edge hints as research prompts. Require representative chart review, sample-size thresholds, and out-of-sample validation before changing trade rules.

### Step 5: Historical Backfill

```bash
python3 skills/stockbee-20pct-study/scripts/run_20pct_study.py backfill \
  --from 2020-01-01 \
  --to 2026-06-28 \
  --prices-json data/us_daily_ohlcv.json \
  --min-abs-return-pct 20 \
  --include-down-movers \
  --state-file state/stockbee/20pct_study_events.jsonl \
  --output-dir reports/
```

Backfill records are marked `CURRENT_UNIVERSE_BACKFILL_SURVIVORSHIP_BIAS` by default. Add `--survivorship-complete` only when the supplied OHLCV includes delisted symbols and historical universe coverage.

## Output Format

- `stockbee_20pct_events_YYYY-MM-DD_HHMMSS.json` — scan metadata and event records
- `stockbee_20pct_daily_report_YYYY-MM-DD_HHMMSS.md` — human-readable daily 20% study report
- `stockbee_20pct_enriched_YYYY-MM-DD_HHMMSS.json` — enriched event records
- `stockbee_20pct_outcome_update_YYYY-MM-DD_HHMMSS.json/md` — matured forward outcome update
- `stockbee_20pct_cohort_summary_YYYY-MM-DD_HHMMSS.json/md` — cohort statistics and rule candidates
- `stockbee_20pct_edge_hints_YYYY-MM-DD_HHMMSS.yaml` — edge-hint export for downstream research skills
- `state/stockbee/20pct_study_events.jsonl` — durable 20% mover model book

## Resources

- `references/methodology.md` — 20% study methodology and review checklist
- `references/event_schema.md` — JSONL event record schema
- `references/catalyst_taxonomy.md` — catalyst and risk label definitions
- `references/scoring_system.md` — event quality and study priority scoring
- `references/cohort_mining_rules.md` — overfitting controls and sample-size rules
- `scripts/run_20pct_study.py` — CLI for scan, enrich, update-outcomes, summarize, and backfill

## Shared FMP client

Live FMP access uses the bundled generated `scripts/fmp_client.py`, loaded only
when an FMP run starts, so offline modes still work without `requests`. CLI
key/environment precedence, the API-call budget and successful output shapes are
preserved. Requests use stable endpoints only; a denied, empty or failed stable
request does not fall back to retired v3 URLs. The shared client masks raw and
URL-encoded key echoes, retries malformed JSON once, and retries a 429 at most once,
after a 60-second wait, before stopping on a repeated rate limit.

### Referencia: assets/cohort_summary_template.md

# Stockbee 20% Study Cohort Summary — {{date}}

## Summary

## Cohorts

## Rule Candidates

## Data Quality Notes

## Accepted / Rejected / Pending Lessons

### Referencia: assets/daily_report_template.md

# Stockbee 20% Study — {{date}}

## Scan Summary

## +20% Movers

## -20% Movers

## Theme Clusters

## High-Value Study Cases

## Matured Outcome Updates

## Edge Hints

## Manual Review Notes

### Referencia: references/catalyst_taxonomy.md

# Catalyst Taxonomy

## Upside and Downside Catalyst Labels

| Label | Use when |
|---|---|
| `EARNINGS_REVALUATION` | Earnings, revenue, EPS, margin, or business results triggered a major repricing |
| `GUIDANCE_RAISE` | Management raised outlook, forecast, or long-term targets |
| `M&A` | Acquisition, merger, takeover, buyout, strategic alternative, or asset sale |
| `FDA_CLINICAL` | FDA, clinical trial, PDUFA, approval, rejection, or biotech study data |
| `CONTRACT_ORDER` | Large contract, government award, partnership, supply agreement, or major customer win |
| `ANALYST_UPGRADE` | Analyst upgrade, initiation, or material target-price change |
| `SHORT_SQUEEZE` | Short-interest, low float, borrow stress, squeeze narrative, or forced covering appears central |
| `THEME_SYMPATHY` | Move is primarily linked to a broader sector or theme cluster |
| `CAPITAL_STRUCTURE` | Offering, warrant, reverse split, convertible, ATM, recapitalization, or dilution issue |
| `LOW_FLOAT_SPECULATION` | Low-float / low-liquidity speculative burst without durable fundamental evidence |
| `NO_CLEAR_NEWS` | No structured catalyst is available or the move is price-only at the time of classification |

## Classification Rules

- Prefer structured catalyst data over price-only inference.
- Use `NO_CLEAR_NEWS` rather than hallucinating a catalyst.
- Keep `confidence` low when the text source is weak, vague, or stale.
- Classify the first-order catalyst, not every related news item.
- Allow human override in `human_review.label_override` when manual research finds a better label.

## Theme Context

Theme fields are separate from catalyst labels. A stock can be `EARNINGS_REVALUATION` and still belong to an AI infrastructure cluster. Use `THEME_SYMPATHY` only when the theme itself appears to be the primary driver.

## Risk Flags Often Associated With Catalysts

| Catalyst | Common risk |
|---|---|
| `FDA_CLINICAL` | Binary-event reversal after data details are digested |
| `SHORT_SQUEEZE` | Violent reversal and borrow/locate constraints |
| `CAPITAL_STRUCTURE` | Dilution, warrant overhang, reverse-split distortions |
| `LOW_FLOAT_SPECULATION` | Low liquidity, wide spreads, gap risk |
| `NO_CLEAR_NEWS` | Unexplained move, rumor risk, poor repeatability |

### Referencia: references/cohort_mining_rules.md

# Cohort Mining Rules

## Purpose

Cohort summaries convert many 20% mover observations into evidence prompts. They should reduce hindsight bias, not create overfit rules.

## Minimum Evidence Rules

- Require `min_sample` before promoting any rule candidate. Default: 10 matured records.
- Treat samples below 30 as preliminary unless the pattern is very stable and explainable.
- Split by market regime before increasing risk based on a cohort.
- Review representative charts from both winners and failures.
- Prefer simple groupings before adding more filters.

## Default Cohort Dimensions

```text
direction,catalyst.label,technical_context.pattern_label,technical_context.close_quality
```

Useful alternate groupings:

```text
direction,technical_context.pattern_label,technical_context.extension_risk
catalyst.label,technical_context.close_quality,liquidity.volume_ratio_20d
direction,data_quality.flags,technical_context.pattern_label
```

## Rule Candidate Thresholds

A continuation-favorable cohort can become `candidate_for_review` when:

- Sample size is at or above `min_sample`
- Direction-adjusted win rate is at least 58%
- Median direction-adjusted return is at least +2%

A weak cohort can become `avoid_or_fade_study` when:

- Sample size is at or above `min_sample`
- Direction-adjusted win rate is 42% or lower
- Median direction-adjusted return is -2% or worse

## Overfitting Controls

- Do not add filters solely because they improved one backtest.
- Do not mine hundreds of tag combinations without recording the number of trials.
- Do not use future catalyst knowledge during historical classification.
- Do not count records with `PENDING` outcomes as matured.
- Do not mix current-universe-only and survivorship-complete backfills without a data-quality split.

## Promotion Path

1. `stockbee-20pct-study` produces a rule candidate.
2. Human reviews charts and data-quality notes.
3. `edge-hint-extractor` or `edge-candidate-agent` converts it into an explicit research ticket.
4. `backtest-expert` validates the hypothesis with realistic execution assumptions.
5. `monthly-performance-review` decides whether to accept, reject, or keep monitoring.

### Referencia: references/event_schema.md

# Event Schema

The durable model book is stored as JSONL at `state/stockbee/20pct_study_events.jsonl`. Each line is one event record. Records are upserted by `record_id`.

## Identity Fields

```json
{
  "schema_version": "1.0",
  "source_skill": "stockbee-20pct-study",
  "record_id": "AAPL:2026-06-28:UP:5D",
  "episode_id": "AAPL:2026-06-24:UP",
  "symbol": "AAPL",
  "event_date": "2026-06-28",
  "direction": "UP",
  "window_days": 5,
  "event_day_index": 1
}
```

`record_id` identifies a single detection window. `episode_id` groups consecutive detections for the same symbol and direction into the same market episode.

## Price Snapshot

```json
{
  "price_snapshot": {
    "open": 100.0,
    "high": 126.0,
    "low": 98.0,
    "close": 124.0,
    "previous_close": 100.0,
    "lookback_close": 100.0,
    "return_pct": 24.0,
    "day_return_pct": 18.0,
    "gap_pct": 5.0,
    "range_pct": 28.0,
    "close_location_pct": 92.8
  }
}
```

`return_pct` is measured from the lookback close to the event close. `close_location_pct` is 0 at the low of the event-day range and 100 at the high.

## Liquidity

```json
{
  "liquidity": {
    "volume": 50000000,
    "avg_volume_20d": 12000000,
    "volume_ratio_20d": 4.17,
    "dollar_volume": 6200000000,
    "avg_dollar_volume_20d": 1500000000,
    "price_pass": true,
    "liquidity_pass": true
  }
}
```

## Technical Context

```json
{
  "technical_context": {
    "distance_to_52w_high_pct": -2.1,
    "distance_to_52w_low_pct": 88.0,
    "prior_20d_return_pct": 8.5,
    "prior_50d_return_pct": 22.0,
    "base_length_days": 25,
    "base_depth_pct": 14.0,
    "pattern_label": "BASE_BREAKOUT",
    "close_quality": "STRONG_CLOSE",
    "extension_risk": "MODERATE"
  }
}
```

## Catalyst

```json
{
  "catalyst": {
    "label": "EARNINGS_REVALUATION",
    "confidence": 0.82,
    "source_type": "news_events_json",
    "summary": "Large gap after earnings and guidance raise."
  }
}
```

If no catalyst source is provided, records default to `NO_CLEAR_NEWS` with `source_type=price_only`.

## Scores and Handoffs

```json
{
  "scores": {
    "continuation_quality_score": 78,
    "reversal_risk_score": 31,
    "study_priority_score": 91,
    "data_quality_score": 86
  },
  "labels": ["UP", "BASE_BREAKOUT", "STRONG_CLOSE", "A_REVALUATION_OR_HIGH_QUALITY_EVENT"],
  "handoffs": {
    "stockbee_episodic_pivot": true,
    "pead_screener": true,
    "theme_detector": true,
    "edge_candidate_agent": false,
    "parabolic_short_watch": false
  }
}
```

## Outcomes

```json
{
  "outcomes": {
    "1d": {
      "status": "MATURED",
      "horizon_days": 1,
      "entry_close": 124.0,
      "close_date": "2026-06-29",
      "close": 130.0,
      "close_return_pct": 4.84,
      "mfe_pct": 6.45,
      "mae_pct": -2.1,
      "directional_close_return_pct": 4.84,
      "directional_mfe_pct": 6.45,
      "directional_mae_pct": -2.1,
      "outcome_tag": "CONTINUED"
    },
    "5d": {
      "status": "PENDING",
      "reason": "insufficient_future_bars"
    }
  }
}
```

For `DOWN` events, direction-adjusted returns treat further downside as positive continuation. Raw `close_return_pct`, `mfe_pct`, and `mae_pct` remain long-side price movement from the event close.

## Data Quality

```json
{
  "data_quality": {
    "flags": ["SHORT_HISTORY_LT_260_BARS", "LOW_AVG_DOLLAR_VOLUME"],
    "data_quality_score": 70
  }
}
```

Common flags include:

- `SHORT_HISTORY_LT_260_BARS`
- `LOW_AVG_DOLLAR_VOLUME`
- `MISSING_VOLUME`
- `EXTREME_MOVE_CHECK_SPLIT_OR_CORPORATE_ACTION`
- `POSSIBLE_SPLIT_OR_SPECIAL_DISTRIBUTION`
- `CURRENT_UNIVERSE_BACKFILL_SURVIVORSHIP_BIAS`

### Referencia: references/methodology.md

# Stockbee 20% Study Methodology

## Purpose

The 20% study is a daily market observation routine. Its goal is to build a durable model book of unusual price moves, not to convert every mover into a trade.

The workflow answers three research questions:

1. Which stocks moved at least +20% or -20% over the selected window?
2. What catalyst, chart context, liquidity context, and market regime were present?
3. What happened 1, 3, 5, 10, and 20 trading days later?

## Operating Principles

- Record both winners and failures. Negative examples are necessary for setup fluency.
- Separate observation, hypothesis, and execution. A 20% mover is an event, not a signal.
- Classify before optimizing. The first pass should label catalyst and setup context; strategy design comes later.
- Preserve data-quality flags. Missing bars, current-universe-only backfills, possible splits, and low liquidity change interpretation.
- Prefer broad, stable cohorts over clever one-off rules.

## Daily Review Checklist

For each high-priority mover, review:

- Catalyst: earnings, guidance, M&A, FDA/clinical, contract, analyst action, short squeeze, theme sympathy, low-float speculation, capital structure, or no clear news
- Direction: +20% upside event or -20% downside event
- Window: 1-day, 5-day, or custom lookback
- Close quality: strong close, midpoint close, weak close, reversal close
- Volume shock: current volume versus 20-day average volume
- Liquidity: current dollar volume and 20-day average dollar volume
- Position in trend: near 52-week high, extended, breaking down, or attempting reversal
- Setup type: base breakout, gap-and-go, episodic-pivot-like, climax extension, failed breakout, breakdown, or reversal candidate
- Theme clustering: whether multiple related symbols moved together
- Follow-up plan: which future horizons should be updated

## Daily Cadence

1. Run `scan` after the daily bar is complete.
2. Run `enrich` when structured catalyst data is available.
3. Run `update-outcomes` to mature prior records.
4. Run `summarize` after enough records have matured.
5. Promote only evidence-backed findings into downstream research.

## Historical Backfill Cadence

Backfills are useful for initial model-book seeding, but they require stronger data-quality notes. A current listed-symbol universe excludes delisted failures and can materially overstate continuation quality.

The CLI marks backfill records with `CURRENT_UNIVERSE_BACKFILL_SURVIVORSHIP_BIAS` by default. Use `--survivorship-complete` only when the supplied OHLCV includes delisted symbols and historical universe coverage.

Minimum backfill notes:

- Universe source
- Whether delisted symbols are included
- Split and corporate-action adjustment source
- Liquidity filter
- Date range
- Lookback window
- Forward outcome horizons

## Interpretation Boundaries

The output is valid as:

- Study material
- Event history
- Cohort evidence
- Edge-hint input
- Manual chart-review queue

The output is not valid as:

- A buy/sell signal
- A broker order template
- A guarantee of continuation or reversal
- A substitute for position sizing, stop design, or regime gating

### Referencia: references/scoring_system.md

# Scoring System

The initial implementation uses deterministic scores. Scores are research triage aids, not trade signals.

## Continuation Quality Score

`continuation_quality_score` ranges from 0 to 100.

| Component | Intent |
|---|---|
| Catalyst quality | Durable revaluation catalysts score higher than no-news pops |
| Liquidity | Higher dollar volume improves execution realism and institutional relevance |
| Volume shock | Volume expansion indicates unusual attention and participation |
| Close quality | Strong closes receive higher continuation score for upside events |
| Setup context | Base breakout and gap-and-go patterns score higher than weak or failed moves |
| 52-week context | Upside events near 52-week highs receive additional score |
| Data quality | Missing history, missing volume, and split-like moves reduce confidence |
| Extension risk | Extreme prior extension reduces quality score |

## Reversal Risk Score

`reversal_risk_score` ranges from 0 to 100.

Risk increases when:

- Catalyst is `NO_CLEAR_NEWS`, `LOW_FLOAT_SPECULATION`, or `CAPITAL_STRUCTURE`
- The event is extremely extended
- Upside event closes weakly
- Dollar volume is below the liquidity floor
- Data quality flags are present

## Study Priority Score

`study_priority_score` ranks which events deserve manual review. A high-priority event is not necessarily a trade; it may be a high-quality example, a dangerous failure, or a useful negative case.

## Suggested Human Ratings

| Condition | Human-facing label |
|---|---|
| Quality >= 75 and catalyst is durable | `A_REVALUATION_OR_HIGH_QUALITY_EVENT` |
| Quality >= 60 | `B_MOMENTUM_EVENT` |
| Reversal risk >= 65 | `D_LOW_QUALITY_OR_REVERSAL_RISK` |
| Otherwise | `C_STUDY_ONLY` |

## Handoff Flags

| Flag | Meaning |
|---|---|
| `stockbee_episodic_pivot` | Event resembles a Day 1 EP / gap-and-go / base breakout candidate |
| `pead_screener` | Earnings or guidance catalyst may warrant PEAD-style research |
| `theme_detector` | Theme or high-priority event may deserve cluster review |
| `edge_candidate_agent` | Event is strong enough to export as an edge research prompt |
| `parabolic_short_watch` | Reversal-risk profile is high enough for study-only exhaustion review |


---

## SKILL: stockbee-episodic-pivot-analyzer

- Fuente: `tradermonty/claude-trading-skills` → `skills/stockbee-episodic-pivot-analyzer` (MIT)
- Cuándo usarla: Analyze Stockbee-style Day 1 Episodic Pivot candidates from earnings, guidance raises, M&A, FDA/regulatory approvals, analyst actions, major contracts, product launches, short-squeeze catalysts, or theme/story events. Scores catalyst quality together with gap/range expansion, volume shock, neglect/revaluation context, liquidity, and risk to the EP-day low. Use when the user asks for EP candidates, episodic pivots, Day 1 catalyst trades, game-changing news reactions, delayed EP watchlists, or handoffs into PEAD monitoring.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/stockbee-episodic-pivot-analyzer/` (requirements.txt, analyze_ep.py, fmp_client.py)

# Stockbee Episodic Pivot Analyzer

Classify Day 1 Episodic Pivot (EP) candidates using both **catalyst quality** and **price/volume confirmation**. The skill is a candidate-quality analyzer, not an execution engine.

## When to Use

- The user asks for Pradeep Bonde / Stockbee style EP candidates
- The user provides earnings, guidance, M&A, FDA, analyst, contract, product, short-squeeze, or theme/news events
- The user wants to separate `ACTIONABLE_DAY1` candidates from `DELAYED_EP_WATCH` names
- The user wants to hand strong earnings/guidance EPs into `pead-screener`
- The user wants to combine catalyst analysis with `stockbee-momentum-burst-screener` price/volume output

## Prerequisites

- Python 3.10+
- Optional: FMP API key for OHLCV enrichment
- One of:
  - Catalyst/events JSON
  - `earnings-trade-analyzer` JSON output
  - Catalyst JSON plus `stockbee-momentum-burst-screener` JSON enrichment
- This skill does not fetch or discover news by itself. If the catalyst is not supplied, first gather the event/news context using the user's preferred news or research process.

## Workflow

### Step 1: Prepare Candidate Inputs

Use one or more of these input modes.

**Mode A — Catalyst/event JSON:**

```json
{
  "events": [
    {
      "symbol": "ABC",
      "event_date": "2026-04-25",
      "catalyst_type": "guidance_raise",
      "headline": "ABC raises FY guidance after record demand",
      "summary": "Management raised revenue and EPS guidance."
    }
  ]
}
```

**Mode B — Earnings pipeline:**

Use the JSON produced by `earnings-trade-analyzer`.

**Mode C — Price/volume enrichment:**

Pass a `stockbee-momentum-burst-screener` JSON report to reuse day-gain, volume, close-location, and risk-distance fields.

### Step 2: Run the Analyzer

```bash
# Catalyst JSON + offline OHLCV
python3 skills/stockbee-episodic-pivot-analyzer/scripts/analyze_ep.py \
  --events-json data/catalysts.json \
  --prices-json data/daily_ohlcv.json \
  --output-dir reports/

# Earnings pipeline input
python3 skills/stockbee-episodic-pivot-analyzer/scripts/analyze_ep.py \
  --earnings-json reports/earnings_trade_analyzer_YYYY-MM-DD_HHMMSS.json \
  --output-dir reports/

# Catalyst JSON + Stockbee momentum enrichment
python3 skills/stockbee-episodic-pivot-analyzer/scripts/analyze_ep.py \
  --events-json data/catalysts.json \
  --momentum-json reports/stockbee_momentum_burst_YYYY-MM-DD_HHMMSS.json \
  --output-dir reports/
```

Optional FMP enrichment:

```bash
export FMP_API_KEY=your_key
python3 skills/stockbee-episodic-pivot-analyzer/scripts/analyze_ep.py \
  --events-json data/catalysts.json \
  --max-api-calls 200 \
  --output-dir reports/
```

### Step 3: Review the Output

For each candidate, present:

- `state`: `ACTIONABLE_DAY1`, `DAY1_WATCH`, `DELAYED_EP_WATCH`, `CATALYST_WATCH`, or `REJECT`
- `ep_type`: `EARNINGS_EP`, `GUIDANCE_EP`, `FDA_EP`, `M_AND_A_EP`, `STORY_EP`, etc.
- Catalyst quality score and reasons
- Price/range expansion, volume shock, and close-location quality
- Risk to EP-day low
- `pead_handoff` and `delayed_ep_watch` flags

### Step 4: Handoff Rules

- `ACTIONABLE_DAY1`: Send to `technical-analyst` and `position-sizer` before any trade decision.
- `DAY1_WATCH`: Keep on the intraday/next-day watchlist; require chart confirmation.
- `DELAYED_EP_WATCH`: Do not chase Day 1; monitor for a controlled pullback or new range.
- `CATALYST_WATCH`: Catalyst may be important, but price/volume confirmation is not yet sufficient.
- `REJECT`: Do not trade from this candidate source.
- Earnings/guidance EPs with `pead_handoff=true` can be sent to `pead-screener` for weekly red-candle / delayed reaction monitoring.

## Output

- `stockbee_episodic_pivot_YYYY-MM-DD_HHMMSS.json` — structured EP scoring report
- `stockbee_episodic_pivot_YYYY-MM-DD_HHMMSS.md` — human-readable candidate report

## Resources

- `references/ep_methodology.md` — Stockbee EP interpretation and setup taxonomy
- `references/catalyst_quality.md` — catalyst classification and quality scoring
- `references/handoff_rules.md` — downstream workflow handoffs and review rules

## Shared FMP client

Live FMP access uses the bundled generated `scripts/fmp_client.py`, loaded only
when an FMP run starts, so offline modes still work without `requests`. CLI
key/environment precedence, the API-call budget and successful output shapes are
preserved. Requests use stable endpoints only; a denied, empty or failed stable
request does not fall back to retired v3 URLs. The shared client masks raw and
URL-encoded key echoes, retries malformed JSON once, and retries a 429 at most once,
after a 60-second wait, before stopping on a repeated rate limit.

### Referencia: references/catalyst_quality.md

# Catalyst Quality Scoring

The analyzer assigns a 35-point catalyst component from the event type, text clues, and optional upstream grades.

## High-Quality Catalysts

| Catalyst | Why It Matters |
|---|---|
| Guidance raise / beat-and-raise | Suggests the market's forward estimates may be too low |
| FDA approval / Phase 3 success | Can change revenue trajectory for smaller biotech names |
| First major earnings acceleration | Can trigger institutional discovery |
| Major contract or customer win | Can validate product-market fit or revenue visibility |
| Regulatory approval | Can remove a major uncertainty or unlock a market |

## Medium / Context-Dependent Catalysts

| Catalyst | Caveat |
|---|---|
| M&A | Often caps upside around the deal price; useful but may not trend |
| Product launch | Needs proof of adoption or demand |
| Partnership | Quality depends on partner credibility and economics |
| Short squeeze | Can be powerful but fragile and liquidity-sensitive |

## Lower-Quality Catalysts

| Catalyst | Caveat |
|---|---|
| Analyst upgrade | Usually weaker unless it confirms a true inflection |
| Story/theme only | Can run quickly but often reverses quickly without fundamentals |
| Vague news | Must be downgraded unless price/volume confirmation is exceptional |

## Negative Text Deductions

Events mentioning dilution, secondary offering, investigation, lawsuit, resignation, downgrade, or similar adverse language should be treated cautiously even when price initially reacts well.

## Manual Review Questions

1. Is this a one-day headline or a durable revaluation?
2. Is the event surprising relative to what the market already expected?
3. Does the event change revenue, earnings, TAM, survival odds, or investor sponsorship?
4. Is the stock already very extended before the event?
5. Can the EP-day low be used as a realistic stop?

### Referencia: references/ep_methodology.md

# Stockbee Episodic Pivot Methodology

An Episodic Pivot (EP) is a price/volume revaluation event triggered by a discrete catalyst. The Stockbee-style interpretation emphasizes Day 1 recognition: a large unexpected event causes participants to rapidly reprice a stock, often creating a multi-day or multi-week drift.

## EP Families

| EP Type | Typical Catalyst | Notes |
|---|---|---|
| `EARNINGS_EP` | Earnings beat, sales/EPS acceleration | Strongest when it is the first major acceleration or a beat-and-raise |
| `GUIDANCE_EP` | Guidance raise or business inflection | Often higher quality than a simple quarterly beat |
| `FDA_EP` | FDA approval, Phase 3 success, PDUFA event | High gap risk; require liquidity and risk control |
| `M_AND_A_EP` | Merger, acquisition, buyout, takeover | Often one-day repricing; upside may be capped by deal terms |
| `CONTRACT_EP` | Large contract/order/customer win | Quality depends on size relative to company revenue |
| `PARTNERSHIP_EP` | Strategic partnership/collaboration | Stronger when partner is credible and commercial impact is clear |
| `ANALYST_EP` | Upgrade, initiation, target raise | Usually lower quality unless it confirms a larger theme |
| `PRODUCT_EP` | Product launch/commercialization | Needs evidence of demand or adoption |
| `STORY_EP` | AI, crypto, nuclear, space, robotics, EV, defense, etc. | Can move fast but often has lower fundamental confirmation |
| `SQUEEZE_EP` | Short squeeze or float squeeze | Treat as high-risk; prioritize liquidity and fast review |

## Day 1 Quality Checklist

A strong Day 1 EP should have most of the following:

- Discrete catalyst that can change market perception
- Price gap or same-day move of at least 4%
- Volume shock, ideally 3x+ average volume or 9M+ absolute shares
- Close in the upper part of the daily range
- Risk to EP-day low small enough to size responsibly
- Prior stock was neglected, basing, or not already extremely extended
- Liquidity is sufficient for realistic entry and exit

## What This Skill Does Not Do

This skill does not decide whether to buy. It ranks and classifies candidates. Before any trade decision, pass candidates through manual catalyst review, chart validation, and risk-based position sizing.

## State Interpretation

- `ACTIONABLE_DAY1`: Strong catalyst and price/volume confirmation with manageable risk.
- `DAY1_WATCH`: Good EP candidate, but needs chart/context confirmation.
- `DELAYED_EP_WATCH`: The event is strong but Day 1 risk or close quality is not acceptable; wait for a new base/pullback.
- `CATALYST_WATCH`: Catalyst may matter but the price/volume reaction is not confirmed.
- `REJECT`: Weak event, weak reaction, low quality, or poor tradability.

### Referencia: references/handoff_rules.md

# Handoff Rules

## To Technical Analyst

Send `ACTIONABLE_DAY1` and high-quality `DAY1_WATCH` names to `technical-analyst` for chart validation. The chart review should reject candidates with:

- Long upper wick / intraday fade
- Obvious overhead supply
- Chaotic low-liquidity price action
- Already extended multi-day move before the catalyst
- Stop distance too wide for the account's risk model

## To Position Sizer

For Stockbee EPs, the default stop reference is the EP-day low. Use:

```text
risk_per_share = entry_reference - ep_day_low
shares = account_risk_dollars / risk_per_share
```

If the EP-day low is too far away, do not force the trade. Keep it in `DELAYED_EP_WATCH` and wait for a controlled pullback or secondary range.

## To PEAD Screener

Send earnings/guidance candidates with `pead_handoff=true` to `pead-screener` when:

- The Day 1 move is strong but too extended to chase
- The candidate needs a weekly red-candle / delayed reaction setup
- The trader wants a 1-5 week post-earnings monitoring process

## To Stockbee Momentum Burst Screener

Use `stockbee-momentum-burst-screener` to confirm whether the EP also has:

- 4% breakout
- Dollar breakout
- Range expansion
- Volume expansion
- Close near high

The best candidates often show both catalyst quality and momentum-burst confirmation.

## To Trader Memory Core

Record only candidates that pass manual review or are intentionally kept on a delayed EP watchlist. Do not pollute the thesis store with every low-grade headline. For broad learning on rejected candidates, use a separate model-book or research log.


---

## SKILL: stockbee-exhaustion-hammer-screener

- Fuente: `tradermonty/claude-trading-skills` → `skills/stockbee-exhaustion-hammer-screener` (MIT)
- Cuándo usarla: Screen US stocks for Stockbee-style selling-exhaustion hammer setups using prior momentum, pullback depth, undercut/reclaim, long lower-wick geometry, close-location, volume confirmation, quality/liquidity gates, and risk-distance scoring. Use when the user asks for Stockbee, Pradeep Bonde, exhaustion setup, selling exhaustion, hammer reversal, undercut reclaim, near-close reversal candidates, or pullback entries in high-quality funds-owned stocks.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/stockbee-exhaustion-hammer-screener/` (requirements.txt, fmp_client.py, screen_exhaustion_hammer.py)

# Stockbee Exhaustion Hammer Screener

Screen US equities for Stockbee-style selling-exhaustion hammer candidates. The skill is a candidate-generation and setup-quality workflow, not a signal service or an auto-execution system.

## When to Use

- User asks for Stockbee / Pradeep Bonde style exhaustion setup screening
- User wants near-close hammer / long lower-wick reversal candidates
- User wants to scan strong, liquid stocks that pulled back and may be seeing selling exhaustion
- User wants undercut/reclaim candidates before the close or after the close
- User provides a symbol list, universe file, or historical / provisional OHLCV JSON for screening
- User wants candidate outputs to feed into `technical-analyst`, `position-sizer`, `trader-memory-core`, or `stockbee-setup-fluency-trainer`

## Prerequisites

- FMP API key for live universe and historical OHLCV screening:
  ```bash
  export FMP_API_KEY=your_api_key_here
  ```
- Optional no-API path: provide `--prices-json` containing daily OHLCV bars by symbol. For the intended near-close use case, the latest bar should be a provisional current-day bar captured near the close.
- Optional `--profiles-json` can add quality metadata such as `marketCap`, `mutualFundHolders`, `institutionalHolders`, or `institutionalOwnershipPct`.
- Run only after the market-regime workflow allows new swing risk, or mark output as manual-review-only.

## Workflow

### Step 1: Choose Input Mode

Use one of three modes:

**Mode A: FMP universe scan**
```bash
python3 skills/stockbee-exhaustion-hammer-screener/scripts/screen_exhaustion_hammer.py \
  --fmp-universe \
  --max-symbols 300 \
  --market-gate allowed \
  --output-dir reports/
```

**Mode B: Explicit symbols**
```bash
python3 skills/stockbee-exhaustion-hammer-screener/scripts/screen_exhaustion_hammer.py \
  --symbols APP ENPH NVDA TSLA \
  --market-gate allowed \
  --output-dir reports/
```

**Mode C: Offline / near-close OHLCV JSON**
```bash
python3 skills/stockbee-exhaustion-hammer-screener/scripts/screen_exhaustion_hammer.py \
  --prices-json data/near_close_daily_ohlcv.json \
  --profiles-json data/quality_profiles.json \
  --market-gate allowed \
  --output-dir reports/
```

For a best-effort FMP near-close run, use quote override. This costs one additional quote call per symbol and depends on provider freshness:

```bash
python3 skills/stockbee-exhaustion-hammer-screener/scripts/screen_exhaustion_hammer.py \
  --fmp-universe \
  --use-quote-latest \
  --max-api-calls 700 \
  --market-gate allowed \
  --output-dir reports/
```

### Step 2: Run the Screening Pass

The script detects these setup families:

- **Selling exhaustion hammer:** long lower wick, small body, strong close-location, and recovery from the day low
- **Undercut/reclaim hammer:** current low undercuts the prior short-term low and the near-close price reclaims that level
- **Prior momentum pullback:** recent high formed within the configured lookback, followed by a controlled pullback rather than a long-term downtrend
- **High-quality / liquid context:** price, volume, 20-day average dollar volume, market-cap metadata, and optional holder metadata

It then scores setup quality using:

- Quality / liquidity
- Prior momentum
- Pullback and selling-exhaustion context
- Hammer candle geometry
- Risk distance to the day low plus buffer
- Market gate alignment

### Step 3: Review Output

Read the generated JSON and Markdown reports. For each candidate, present:

- Trigger type and all matched tags
- Pullback depth from recent high and days since that high
- Undercut/reclaim status and short-term prior low
- Hammer geometry: lower wick, body, upper wick, close location, recovery from low
- Volume ratios, average dollar volume, and quality metadata
- Entry reference, stop reference, and risk percentage to stop
- Setup score, rating, state, and reject reasons
- Suggested downstream action

### Step 4: Send Survivors to Trade Planning

Use the output conservatively:

- **A / A- candidates:** validate chart manually, check earnings/news risk, then send to `position-sizer`
- **B candidates:** manual review or next-day hammer-high confirmation
- **Watch candidates:** keep on watchlist / model book; wait for follow-through or tighter risk
- **Rejected candidates:** retain for post-analysis, not for execution

## Output

- `stockbee_exhaustion_hammer_YYYY-MM-DD_HHMMSS.json` - Structured candidate list, metadata, thresholds, score components, and rejects
- `stockbee_exhaustion_hammer_YYYY-MM-DD_HHMMSS.md` - Human-readable report grouped by rating/state

## Resources

- `references/exhaustion_hammer_methodology.md` - Stockbee-style method summary and implementation boundaries
- `references/scoring_system.md` - Component weights, state thresholds, and failure filters
- `references/near_close_operations.md` - Near-close operational checklist and scheduling notes

## Shared FMP client

Live FMP access uses the bundled generated `scripts/fmp_client.py`, loaded only
when an FMP run starts, so offline modes still work without `requests`. CLI
key/environment precedence, the API-call budget and successful output shapes are
preserved. Requests use stable endpoints only; a denied, empty or failed stable
request does not fall back to retired v3 URLs. The shared client masks raw and
URL-encoded key echoes, retries malformed JSON once, and retries a 429 at most once,
after a 60-second wait, before stopping on a repeated rate limit.

The quote override reads stable `/quote`; its default bar date is the
America/New_York calendar date, matching the history window.

### Referencia: references/exhaustion_hammer_methodology.md

# Stockbee Exhaustion Hammer Methodology

This skill screens for a specific reversal context, not generic hammer candles.

The target pattern is:

1. A liquid, high-quality stock with prior momentum or institutional sponsorship.
2. A recent high followed by several days or weeks of selling.
3. A final push lower that shakes out weak holders, ideally undercutting a short-term low.
4. Buyers appearing before the close, leaving a long lower wick and a close in the upper part of the daily range.
5. A nearby day-low stop that makes risk definable.

## Why not screen every hammer?

A hammer in a structurally weak stock is often just a pause in a downtrend. The edge being modeled here is narrower: strong or widely watched stocks can attract buyers after selling pressure exhausts itself. That is why the script combines quality/liquidity, prior momentum, pullback context, undercut/reclaim, volume, and risk distance.

## Intended Timing

The primary operational use is a near-close scan, roughly two minutes before the regular session close. The latest bar can be:

- A provisional daily OHLCV bar from a live/near-live data provider
- A FMP quote-derived best-effort bar via `--use-quote-latest`
- A post-close daily bar for after-close review and model-book building

## Manual Review Requirements

Before treating any candidate as actionable, review:

- Weekly chart context and Stage 2 / broader trend quality
- Whether the pullback is orderly or caused by a thesis-breaking event
- Earnings date, guidance/news risk, and gap-risk exposure
- Risk from entry reference to stop reference
- Portfolio heat and current market-regime gate

## Non-goals

This skill does not:

- Place orders
- Recommend automatic execution
- Verify real-time quote freshness
- Discover catalysts/news by itself
- Replace chart review or risk sizing

### Referencia: references/near_close_operations.md

# Near-Close Operations

The intended production cadence is relative to the market close rather than a fixed wall-clock time.

## Suggested Routine

| Time | Action |
|---|---|
| Close - 15 min | Optional broad scan to see whether many names are forming lower-wick reversals |
| Close - 5 min | Refresh candidates and remove names with weak close-location or wide risk |
| Close - 2 min | Run final scan, review top candidates manually, and decide whether any deserve a small planned entry |
| Close + 1 min | Save final report and ingest studyable examples into the model book |

## Example Commands

Offline/provisional OHLCV feed:

```bash
python3 skills/stockbee-exhaustion-hammer-screener/scripts/screen_exhaustion_hammer.py \
  --prices-json data/near_close_daily_ohlcv.json \
  --profiles-json data/quality_profiles.json \
  --market-gate allowed \
  --output-dir reports/
```

FMP quote override path:

```bash
python3 skills/stockbee-exhaustion-hammer-screener/scripts/screen_exhaustion_hammer.py \
  --fmp-universe \
  --use-quote-latest \
  --max-symbols 300 \
  --max-api-calls 700 \
  --market-gate allowed \
  --output-dir reports/
```

## Scheduling Note

If scheduling this scan, use an exchange calendar and run at `market_close - 2 minutes`. Do not hard-code 15:58 ET without handling early-close sessions and market holidays.

## Handling Half Days

On early-close days, either:

- Run at the adjusted close minus two minutes, or
- Disable near-close actionability and use the output for study only.

### Referencia: references/scoring_system.md

# Stockbee Exhaustion Hammer Scoring System

The composite score ranges from 0 to 100.

| Component | Max Points | Meaning |
|---|---:|---|
| Quality / liquidity | 20 | Price, 20-day average dollar volume, market cap, optional fund/institutional-holder metadata |
| Prior momentum | 15 | A recent high within the lookback, 20/60-day strength, and constructive location versus the 50-day average |
| Pullback exhaustion | 20 | Controlled pullback depth, short-term undercut/reclaim, recent selling pressure, and volume confirmation |
| Hammer geometry | 25 | Long lower wick, small body, strong close-location, recovery from low, and limited upper wick |
| Risk distance | 15 | Distance from entry reference to day-low stop plus buffer |
| Market gate | 5 | Rewards alignment with a permissive market regime |

## Ratings

| Score | Rating | State |
|---:|---|---|
| 90-100 | A | `ACTIONABLE_CLOSE_BUY` after chart/news/risk review |
| 82-89 | A- | `ACTIONABLE_CLOSE_BUY` after chart/news/risk review |
| 70-81 | B | `MANUAL_REVIEW` or next-day confirmation |
| 55-69 | Watch | `WATCH_TOMORROW` |
| <55 | Reject | `REJECTED` |

## Hard Rejection Rules

A candidate is rejected before actionability if any of these are true:

- Insufficient OHLCV history
- Current price or current volume is below the configured floor
- 20-day average dollar volume is below the configured floor
- Known market cap is below the configured floor
- Hammer geometry fails lower-wick, body-size, close-location, wick/body, or recovery-from-low thresholds
- Pullback from the recent high is too shallow or too deep
- Recent high is too close or too stale
- `--require-undercut-reclaim` is set and the current low did not undercut/reclaim the short-term prior low
- Risk to stop exceeds the configured maximum

## Soft Failure Tags

These do not automatically reject unless the hard filters or total score fail:

- `no_undercut_reclaim`
- `deep_pullback`
- `stale_high`
- `weak_volume_confirmation`
- `moderate_close_location`
- `still_down_big_on_day`
- `wide_risk`

## Market Gate

Use `--market-gate allowed`, `neutral`, or `restrictive`.

- `allowed`: normal scoring; adds full market-gate points
- `neutral`: modest market-gate score; report remains usable but conservative
- `restrictive`: high-scoring candidates are marked manual-review-only and the market component is zero


---

## SKILL: stockbee-momentum-burst-screener

- Fuente: `tradermonty/claude-trading-skills` → `skills/stockbee-momentum-burst-screener` (MIT)
- Cuándo usarla: Screen US stocks for Stockbee-style short-term Momentum Burst setups using 4% breakout, dollar breakout, range expansion, volume expansion, prior range contraction, close-location, failure filters, and risk-distance scoring. Use when the user asks for Stockbee, Pradeep Bonde, momentum burst, 4% breakout, range expansion, dollar breakout, short-term swing momentum candidates, or 3-5 day burst setup review.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/stockbee-momentum-burst-screener/` (requirements.txt, fmp_client.py, screen_momentum_burst.py)

# Stockbee Momentum Burst Screener

Screen US equities for Stockbee-style short-term Momentum Burst candidates. The skill is a candidate-generation and setup-quality workflow, not a signal service or an auto-execution system.

## When to Use

- User asks for Stockbee / Pradeep Bonde style Momentum Burst screening
- User wants 4% breakout, dollar breakout, or range expansion candidates
- User asks for short-term 3-5 day swing momentum setups
- User wants to review whether a daily breakout has A/B/C setup quality
- User provides a symbol list, universe file, or historical OHLCV JSON for screening
- User wants candidate outputs to feed into `technical-analyst`, `position-sizer`, or `trader-memory-core`

## Prerequisites

- FMP API key for live universe and historical OHLCV screening:
  ```bash
  export FMP_API_KEY=your_api_key_here
  ```
- Optional no-API path: provide `--prices-json` containing daily OHLCV bars by symbol.
- Run only after the market-regime workflow allows new swing risk, or mark output as manual-review-only.

## Workflow

### Step 1: Choose Input Mode

Use one of three modes:

**Mode A: FMP universe scan**
```bash
python3 skills/stockbee-momentum-burst-screener/scripts/screen_momentum_burst.py \
  --fmp-universe \
  --max-symbols 300 \
  --output-dir reports/
```

**Mode B: Explicit symbols**
```bash
python3 skills/stockbee-momentum-burst-screener/scripts/screen_momentum_burst.py \
  --symbols NVDA SMCI PLTR TSLA \
  --output-dir reports/
```

**Mode C: Offline OHLCV JSON**
```bash
python3 skills/stockbee-momentum-burst-screener/scripts/screen_momentum_burst.py \
  --prices-json data/daily_ohlcv.json \
  --output-dir reports/
```

### Step 2: Run the Screening Pass

The script detects these trigger families:

- **4% Breakout:** `close / previous_close >= 1.04`, volume above previous day, and volume above the liquidity floor
- **Dollar Breakout:** `close - open >= 0.90`, volume above the liquidity floor
- **Range Expansion:** current daily range exceeds the prior three daily ranges while the prior day was not already extended

It then scores setup quality using:

- Trigger strength
- Volume expansion
- Prior base / range contraction quality
- Close location near the high of day
- Risk distance to the trigger-day low
- Failure filters such as prior 3-day run-up or recent 4% breakdown
- Market gate alignment

### Step 3: Review Output

Read the generated JSON and Markdown reports. For each candidate, present:

- Trigger type and all matched trigger tags
- Day gain, dollar gain, volume ratio, and close-location percentage
- Prior base length and base width
- Entry reference, stop reference, and risk percentage to stop
- Setup score, rating, state, and reject reasons
- Suggested downstream action

### Step 4: Send Survivors to Trade Planning

Use the output conservatively:

- **A / A- candidates:** send to `technical-analyst` for manual chart validation, then `position-sizer`
- **B candidates:** watchlist or smaller-risk review only
- **Watch-only candidates:** keep in model book; do not plan a trade unless chart review upgrades the setup
- **Rejected candidates:** retain for post-analysis, not for execution

## Output

- `stockbee_momentum_burst_YYYY-MM-DD_HHMMSS.json` - Structured candidate list, metadata, thresholds, score components, and rejects
- `stockbee_momentum_burst_YYYY-MM-DD_HHMMSS.md` - Human-readable report grouped by rating/state

## Resources

- `references/momentum_burst_methodology.md` - Stockbee-style method summary and implementation boundaries
- `references/scoring_system.md` - Component weights, state thresholds, and failure filters
- `references/entry_exit_rules.md` - Entry reference, stop, sizing handoff, and exit template

## Shared FMP client

Live FMP access uses the bundled generated `scripts/fmp_client.py`, loaded only
when an FMP run starts, so offline modes still work without `requests`. CLI
key/environment precedence, the API-call budget and successful output shapes are
preserved. Requests use stable endpoints only; a denied, empty or failed stable
request does not fall back to retired v3 URLs. The shared client masks raw and
URL-encoded key echoes, retries malformed JSON once, and retries a 429 at most once,
after a 60-second wait, before stopping on a repeated rate limit.

### Referencia: references/entry_exit_rules.md

# Entry and Exit Rules

## Entry Reference

The default entry reference is the latest close because the script is primarily an end-of-day / near-close screener.

If used intraday with current OHLCV bars, treat the entry reference as an indicative planning price. Manual review should confirm that the breakout is still valid near the intended order time.

## Stop Reference

The default stop reference is the trigger-day low.

```text
risk_per_share = entry_reference - stop_reference
risk_pct_to_stop = risk_per_share / entry_reference * 100
```

Reject candidates where the stop is too far away for the account's risk policy.

## Position Sizing Handoff

Send only validated candidates to `position-sizer`.

```text
position_size = account_risk_dollars / (entry_reference - stop_reference)
```

The screener should not decide final share count. It only provides the fields needed by a position-sizing skill.

## Exit Template

Default template:

- Stop out if the trigger-day low fails
- Review after 3-5 sessions
- Protect gains if the stock advances abnormally fast, especially a 10%+ move in one session
- Treat a full signal reversal or no follow-through after several sessions as a failed burst

## Practical Notes

- A 4% trigger is not enough by itself. Require setup quality and manageable risk.
- Avoid using the screener as a standalone buy list.
- Keep rejected names for model-book review because failures help calibrate pattern recognition.

### Referencia: references/momentum_burst_methodology.md

# Stockbee Momentum Burst Methodology

## Purpose

This skill operationalizes a Stockbee-style short-term Momentum Burst review process. It is designed to find candidates for manual chart review, not to issue automatic buy signals.

## Core Hypothesis

Some stocks produce short, sharp momentum bursts after a period of range contraction. The useful part of the move often occurs over the next several sessions rather than over a long trend-following window.

The script looks for three trigger families:

1. **4% Breakout**
   - Close is at least 4% above the previous close
   - Volume is higher than the previous day
   - Volume exceeds the configured liquidity floor

2. **Dollar Breakout**
   - Close minus open is at least the configured dollar threshold, default `$0.90`
   - Useful for higher-priced stocks where a dollar move can matter even if the percentage move is under 4%

3. **Range Expansion**
   - Current daily range is larger than each of the prior three daily ranges
   - Prior day was not already extended
   - Volume confirms the expansion

## What Makes a Better Candidate

The screener scores the following qualities:

- Clean prior base or short consolidation
- Prior-day narrow range or down day
- Breakout volume expansion
- Close near the high of day
- Entry-day low close enough to define risk
- No recent 4% breakdown
- Not already up three days before the trigger
- Market regime allows new swing risk

## What the Script Does Not Do

The script does not:

- Place orders
- Guarantee follow-through
- Replace manual chart review
- Verify news/catalysts
- Model intraday slippage or liquidity at the level-2/order-book level
- Decide final position size

## Recommended Downstream Flow

```text
stockbee-momentum-burst-screener
        ↓
technical-analyst
        ↓
position-sizer
        ↓
breakout-trade-planner optional
        ↓
trader-memory-core
```

The strongest use case is a daily routine after the market closes or near the close, followed by a manual chart review and a pre-planned stop.

### Referencia: references/scoring_system.md

# Stockbee Momentum Burst Scoring System

The composite score ranges from 0 to 100.

| Component | Max Points | Meaning |
|---|---:|---|
| Trigger strength | 20 | 4% breakout, dollar breakout, range expansion, and 9M+ volume tag |
| Volume expansion | 15 | Volume relative to previous day and 20-day average |
| Setup quality | 25 | Prior base length, base width, prior-day narrow/down behavior, volume dry-up |
| Close quality | 10 | Close location within the daily range |
| Risk distance | 15 | Distance from entry reference to trigger-day low |
| Failure filters | 10 | Penalizes recent 4% breakdowns, three-day run-ups, and wide/loose action |
| Market gate | 5 | Rewards alignment with a permissive market regime |

## Ratings

| Score | Rating | State |
|---:|---|---|
| 90-100 | A | `ACTIONABLE_DAY1` after chart review |
| 80-89 | A- | `ACTIONABLE_DAY1` after chart review |
| 70-79 | B | `MANUAL_REVIEW` or reduced-size planning |
| 55-69 | Watch | `WATCH_ONLY` |
| <55 | Reject | `REJECTED` |

## Hard Rejection Rules

A candidate is rejected before scoring if any of these are true:

- Insufficient OHLCV history
- Current volume is below the configured minimum
- Price is below the configured minimum
- No trigger family is matched
- Risk to trigger-day low exceeds the configured maximum

## Soft Failure Filters

These reduce the score but do not automatically reject unless they make the score too low:

- Three consecutive up closes before the trigger day
- Recent 4% breakdown within the lookback window
- Prior base is too wide
- Close is in the lower half of the daily range
- Volume expands but not enough to confirm broad interest

## Market Gate

Use `--market-gate allowed`, `neutral`, or `restrictive`.

- `allowed`: normal scoring; adds full market-gate points
- `neutral`: modest market-gate score; report remains usable but conservative
- `restrictive`: output is marked as manual-review-only and the market component is zero


---

## SKILL: stockbee-setup-fluency-trainer

- Fuente: `tradermonty/claude-trading-skills` → `skills/stockbee-setup-fluency-trainer` (MIT)
- Cuándo usarla: Build a Stockbee-style setup model book from momentum-burst screener candidates, then update 3-day and 5-day forward outcomes with MFE/MAE, stop-hit status, outcome tags, and cohort statistics. Use when the user wants to study Stockbee Momentum Burst examples, track failed candidates, build setup fluency, review A/B setup quality, or convert screener outputs into a learning loop rather than immediate trade signals.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/stockbee-setup-fluency-trainer/` (requirements.txt, build_model_book.py, fmp_client.py)

# Stockbee Setup Fluency Trainer

Build and maintain a model book for Stockbee-style Momentum Burst setups. This skill turns daily screener candidates into structured study records, updates them after the 3-day and 5-day windows mature, and summarizes which setup features are working or failing.

## When to Use

- User wants to study Stockbee Momentum Burst setups systematically
- User asks to build a model book from `stockbee-momentum-burst-screener` output
- User wants to review failed candidates, missed trades, or A/B setup quality
- User wants 3-day / 5-day forward returns, MFE, MAE, and stop-hit outcomes
- User wants to improve setup recognition before increasing position size
- User asks which Stockbee tags should be promoted, downgraded, or filtered

## Prerequisites

- Python 3.10+
- A `stockbee-momentum-burst-screener` JSON report, or compatible candidate JSON
- Optional: FMP API key for outcome updates when offline OHLCV JSON is not supplied
- Recommended local state path: `state/stockbee/model_book.jsonl`

## Workflow

### Step 1: Ingest Momentum Burst Candidates

Run after the Stockbee Momentum Burst screener has produced a JSON report.

```bash
python3 skills/stockbee-setup-fluency-trainer/scripts/build_model_book.py ingest \
  --screener-json reports/stockbee_momentum_burst_YYYY-MM-DD_HHMMSS.json \
  --model-book state/stockbee/model_book.jsonl \
  --output-dir reports/
```

Use `--include-rejects` when intentionally building a negative-example set. Otherwise rejected candidates are skipped.

### Step 2: Update 3-Day and 5-Day Outcomes

Use FMP:

```bash
python3 skills/stockbee-setup-fluency-trainer/scripts/build_model_book.py update \
  --model-book state/stockbee/model_book.jsonl \
  --horizons 3,5 \
  --output-dir reports/
```

Use offline OHLCV JSON:

```bash
python3 skills/stockbee-setup-fluency-trainer/scripts/build_model_book.py update \
  --model-book state/stockbee/model_book.jsonl \
  --prices-json data/daily_ohlcv.json \
  --horizons 3,5 \
  --output-dir reports/
```

The update step records:

- Forward close return for each horizon
- MFE and MAE over each horizon
- Stop-hit status and first stop-hit date
- Outcome tags such as `STRONG_WINNER`, `WORKED`, `FAILED_STOP`, `FAILED_FADE`, `CHOPPY_FAILURE`, or `NEUTRAL`

### Step 3: Summarize Cohorts

```bash
python3 skills/stockbee-setup-fluency-trainer/scripts/build_model_book.py summarize \
  --model-book state/stockbee/model_book.jsonl \
  --group-by rating,primary_trigger,setup_tags \
  --min-sample 5 \
  --output-dir reports/
```

Review the generated Markdown and JSON reports. Treat `rule_candidates` as evidence prompts, not automatic rule changes.

### Step 4: Convert Evidence Into Practice

For cohorts with enough examples:

- Promote tags with high win rate, positive 5-day expectancy, and acceptable average MAE
- Downgrade or filter tags with weak 5-day expectancy, frequent stop hits, or repeated fade failures
- Inspect representative charts manually before changing trade rules
- Log accepted lessons in `trader-memory-core` or the monthly review process

## Model Book Fields

Each JSONL record includes:

- `record_id`, `symbol`, `setup_date`, `primary_trigger`
- `rating`, `setup_score`, `setup_tags`
- `entry_reference`, `stop_reference`, `risk_pct_to_stop`
- `human_label`, `human_decision`, `human_notes`
- `outcomes.3d` and `outcomes.5d`
- `overall_outcome`, `matured`, `raw_candidate`

## Interpretation Rules

- `STRONG_WINNER`: 5-day close return >= 8% or MFE >= 12%, with no stop hit
- `WORKED`: 5-day close return >= 4% or MFE >= 6%, with no stop hit
- `FAILED_STOP`: Stop was touched within the horizon
- `FAILED_FADE`: Forward return <= -2% without a recorded stop hit
- `CHOPPY_FAILURE`: Adverse excursion was large and forward progress was poor
- `NEUTRAL`: No decisive follow-through or failure
- `PENDING`: Not enough future bars yet

## Output

- `state/stockbee/model_book.jsonl` - Durable setup model book
- `stockbee_setup_fluency_ingest_YYYY-MM-DD_HHMMSS.json/md`
- `stockbee_setup_fluency_update_YYYY-MM-DD_HHMMSS.json/md`
- `stockbee_setup_fluency_summary_YYYY-MM-DD_HHMMSS.json/md`

## Resources

- `references/model_book_schema.md` - JSONL schema and lifecycle states
- `references/outcome_tags.md` - Outcome classification and tag definitions
- `references/review_workflow.md` - Daily, 3-day, 5-day, and monthly review routine

## Shared FMP client

Live FMP access uses the bundled generated `scripts/fmp_client.py`, loaded only
when an FMP run starts, so offline modes still work without `requests`. CLI
key/environment precedence, the API-call budget and successful output shapes are
preserved. Requests use stable endpoints only; a denied, empty or failed stable
request does not fall back to retired v3 URLs. The shared client masks raw and
URL-encoded key echoes, retries malformed JSON once, and retries a 429 at most once,
after a 60-second wait, before stopping on a repeated rate limit.

If every requested symbol fails at the transport level, `update` exits 1 and
leaves the model book unchanged instead of stamping each record `missing_prices`.

### Referencia: references/model_book_schema.md

# Stockbee Setup Model Book Schema

The model book is a JSONL file. Each line is one study record for one setup candidate on one setup date.

Default path:

```text
state/stockbee/model_book.jsonl
```

## Record Identity

```json
{
  "schema_version": "1.0",
  "record_id": "stockbee_mb:TEST:2026-06-20:4pct_breakout",
  "source_skill": "stockbee-momentum-burst-screener",
  "source_report": "reports/stockbee_momentum_burst_2026-06-20_174954.json",
  "symbol": "TEST",
  "setup_date": "2026-06-20",
  "setup_type": "stockbee_momentum_burst",
  "primary_trigger": "4pct_breakout"
}
```

`record_id` is deterministic so repeated ingest runs update the same record instead of duplicating it.

## Setup Quality Fields

```json
{
  "rating": "A-",
  "setup_score": 84,
  "state_at_ingest": "ACTIONABLE_DAY1",
  "trigger_tags": ["4pct_breakout", "range_expansion"],
  "setup_tags": ["close_near_high", "tight_base", "compact_risk"],
  "entry_reference": 52.4,
  "stop_reference": 50.9,
  "risk_pct_to_stop": 2.86,
  "day_gain_pct": 5.22,
  "volume_ratio_1d": 2.99,
  "close_location_pct": 86.0,
  "prior_base_days": 8,
  "base_width_pct": 4.8
}
```

The `setup_tags` field is the core of the fluency loop. It turns subjective chart-review features into analyzable cohorts.

## Human Review Fields

```json
{
  "human_label": "A-",
  "human_decision": "entered",
  "human_notes": "Clean 8-day base, high close, theme support."
}
```

The script initializes these fields but does not overwrite human edits during re-ingest.

## Outcome Fields

```json
{
  "outcomes": {
    "3d": {
      "matured": true,
      "close_date": "2026-06-25",
      "forward_return_pct": 6.42,
      "mfe_pct": 8.15,
      "mae_pct": -1.20,
      "stop_hit": false,
      "outcome_tag": "WORKED"
    },
    "5d": {
      "matured": true,
      "close_date": "2026-06-29",
      "forward_return_pct": 9.11,
      "mfe_pct": 12.40,
      "mae_pct": -1.20,
      "stop_hit": false,
      "outcome_tag": "STRONG_WINNER"
    }
  },
  "overall_outcome": "STRONG_WINNER",
  "matured": true
}
```

The primary summary outcome uses the longest requested horizon, usually 5 trading days.

## Lifecycle

```text
PENDING_OUTCOME
  Ingested, but not enough future bars exist yet.

MATURED_OUTCOME
  3-day and/or 5-day windows have enough data.

REVIEWED_BY_HUMAN
  Trader has inspected the chart and added human_label / human_notes.
```

The current script uses `matured: true/false`; human review status can be inferred from `human_label` and `human_notes`.

### Referencia: references/outcome_tags.md

# Outcome Tags

The trainer classifies each 3-day and 5-day window into a compact outcome tag. These are learning labels, not trading signals.

## STRONG_WINNER

Conditions:

```text
MFE >= 12% OR forward close return >= 8%
AND stop was not hit
```

Interpretation: The setup produced the kind of fast follow-through Stockbee Momentum Burst is designed to find.

## WORKED

Conditions:

```text
MFE >= 6% OR forward close return >= 4%
AND stop was not hit
```

Interpretation: The setup had tradable follow-through, even if it was not exceptional.

## FAILED_STOP

Condition:

```text
Any low in the horizon <= stop_reference
```

Interpretation: The setup would have violated the planned invalidation level. This is the most important failure type for risk discipline.

## FAILED_FADE

Condition:

```text
forward close return <= -2%
AND stop was not recorded as hit
```

Interpretation: The stock faded after triggering. Review for weak close location, wide base, low volume quality, broad-market weakness, or late-stage extension.

## CHOPPY_FAILURE

Condition:

```text
MAE <= -5%
AND forward close return < 2%
AND stop was not recorded as hit
```

Interpretation: The setup may have looked strong but created too much adverse excursion for a short-term swing process.

## NEUTRAL

Condition:

```text
No decisive follow-through or failure
```

Interpretation: These examples are still useful. A neutral cluster can reveal setups that consume attention without enough reward.

## PENDING

Condition:

```text
Not enough future trading bars are available
```

Interpretation: Leave the record in the model book and update it after the 3-day or 5-day window matures.

### Referencia: references/review_workflow.md

# Stockbee Setup Fluency Review Workflow

This workflow separates candidate generation from learning. The goal is to build procedural recognition of A-quality setups by repeatedly comparing what the setup looked like on day 1 with what happened over the next 3 to 5 trading days.

## Daily After-Close Routine

1. Run `stockbee-momentum-burst-screener`.
2. Ingest the JSON report into the model book.
3. Add human notes for any A/A- setups reviewed manually.
4. Do not change trading rules from one day of examples.

```bash
python3 skills/stockbee-setup-fluency-trainer/scripts/build_model_book.py ingest \
  --screener-json reports/stockbee_momentum_burst_*.json \
  --model-book state/stockbee/model_book.jsonl \
  --output-dir reports/
```

## 3-Day / 5-Day Outcome Routine

Run the update command daily or a few times per week. Matured records will receive forward returns, MFE, MAE, and outcome tags.

```bash
python3 skills/stockbee-setup-fluency-trainer/scripts/build_model_book.py update \
  --model-book state/stockbee/model_book.jsonl \
  --horizons 3,5 \
  --output-dir reports/
```

## Weekly Review

Run a summary with a small sample threshold to see early patterns.

```bash
python3 skills/stockbee-setup-fluency-trainer/scripts/build_model_book.py summarize \
  --model-book state/stockbee/model_book.jsonl \
  --min-sample 3 \
  --output-dir reports/
```

Review:

- Best A/A- winners
- Worst failed-stop examples
- False positives with weak close quality
- Any `wide_risk`, `wide_base`, or `three_days_up_before_trigger` clusters

## Monthly Review

Use a higher sample threshold before changing rules.

```bash
python3 skills/stockbee-setup-fluency-trainer/scripts/build_model_book.py summarize \
  --model-book state/stockbee/model_book.jsonl \
  --min-sample 10 \
  --output-dir reports/
```

Possible actions:

- Promote tags that repeatedly produce positive 5-day expectancy
- Downgrade tags with high stop-hit or fade failure rates
- Add manual chart examples to a separate visual model book
- Feed accepted lessons into `trader-memory-core` or the monthly review process

## Review Discipline

Do not overfit to a tiny sample. Treat `rule_candidates` as prompts for chart review. A rule change should normally require enough examples, plausible market logic, and manual inspection of representative charts.


---

## SKILL: strategy-pivot-designer

- Fuente: `tradermonty/claude-trading-skills` → `skills/strategy-pivot-designer` (MIT)
- Cuándo usarla: Detect backtest iteration stagnation and generate structurally different strategy pivot proposals when parameter tuning reaches a local optimum.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/strategy-pivot-designer/` (requirements.txt, detect_stagnation.py, generate_pivots.py)

# Strategy Pivot Designer

## Overview

Detect when a strategy's backtest iteration loop has stalled and propose structurally different strategy architectures. This skill acts as the feedback loop for the Edge pipeline (hint-extractor -> concept-synthesizer -> strategy-designer -> candidate-agent), breaking out of local optima by redesigning the strategy's skeleton rather than tweaking parameters.

## When to Use

- Backtest scores have plateaued despite multiple refinement iterations.
- A strategy shows signs of overfitting (high in-sample, low robustness).
- Transaction costs defeat the strategy's thin edge.
- Tail risk or drawdown exceeds acceptable thresholds.
- You want to explore fundamentally different strategy architectures for the same market hypothesis.

## Prerequisites

- Python 3.9+
- `PyYAML`
- Iteration history JSON (accumulated backtest-expert evaluations)
- Source strategy draft YAML (from edge-strategy-designer)

## Output

- `pivot_drafts/research_only/*.yaml` — strategy_draft compatible YAML proposals
- `pivot_drafts/exportable/*.yaml` — export-ready drafts + ticket YAML for candidate-agent
- `pivot_report_*.md` — human-readable pivot analysis
- `pivot_manifest_*.json` — metadata for all generated files
- `pivot_diagnosis_*.json` — stagnation detection results

## Workflow

1. Accumulate backtest evaluation results into an iteration history file using `--append-eval`.
2. Run stagnation detection on the history to identify triggers (plateau, overfitting, cost defeat, insufficient profit factor, tail risk). A no-loss profit factor is not cost defeat; an undefined or overflowed ratio requires review.
3. If the diagnosis says `review_required`, repair or re-evaluate the underlying metrics first; do not generate pivots. If stagnation is confirmed, generate pivot proposals using three techniques: assumption inversion, archetype switch, objective reframe.
4. Review ranked proposals (scored by quality potential + novelty).
5. For exportable proposals, ticket YAML is ready for edge-candidate-agent pipeline.
6. For research_only proposals, manual strategy design needed before pipeline integration.
7. Feed the selected pivot draft back into backtest-expert for the next iteration cycle.

## Quick Commands

Append a backtest evaluation to history (creates history if new):

```bash
python3 skills/strategy-pivot-designer/scripts/detect_stagnation.py \
  --append-eval reports/backtest_eval_2026-02-10_120000.json \
  --history reports/iteration_history.json \
  --strategy-id draft_edge_concept_breakout_behavior_riskon_core \
  --changes "Widened stop_loss from 5% to 7%"
```

Detect stagnation:

```bash
python3 skills/strategy-pivot-designer/scripts/detect_stagnation.py \
  --history reports/iteration_history.json \
  --output-dir reports/
```

Generate pivot proposals:

```bash
python3 skills/strategy-pivot-designer/scripts/generate_pivots.py \
  --diagnosis reports/pivot_diagnosis_*.json \
  --strategy reports/edge_strategy_drafts/draft_*.yaml \
  --max-pivots 3 \
  --output-dir reports/
```

## Resources

- `skills/strategy-pivot-designer/scripts/detect_stagnation.py`
- `skills/strategy-pivot-designer/scripts/generate_pivots.py`
- `references/stagnation_triggers.md`
- `references/strategy_archetypes.md`
- `references/pivot_techniques.md`
- `references/pivot_proposal_schema.md`
- `skills/backtest-expert/scripts/evaluate_backtest.py`
- `skills/edge-strategy-designer/scripts/design_strategy_drafts.py`

### Referencia: assets/pivot_report_template.md

# Pivot Report: {strategy_id}

**Generated**: {generated_at_utc}
**Source Strategy**: {source_strategy_id}
**Diagnosis**: {diagnosis_summary}

---

## Stagnation Diagnosis

**Triggers Fired**: {triggers_count}
**Recommendation**: {recommendation}

{triggers_detail}

### Score Trajectory

{score_trajectory}

---

## Pivot Proposals

{pivot_proposals}

### Proposal: {proposal_id}

**Technique**: {pivot_technique}
**Target Archetype**: {target_archetype}
**Category**: {category}

**What Changed**:
- Signal: {signal_change}
- Horizon: {horizon_change}
- Risk: {risk_change}

**Why**: {why_explanation}

**Targeted Triggers**: {targeted_triggers}

**Scores**:
- Quality Potential: {quality_potential}
- Novelty: {novelty}
- Combined: {combined}

**Expected Failure Modes**:
{failure_modes}

---

## Summary

| Rank | Proposal | Archetype | Combined | Category |
|------|----------|-----------|----------|----------|
{summary_table}

---

## Next Steps

1. Review proposals and select the most promising pivot direction
2. For **exportable** proposals: ticket YAML is ready for `edge-candidate-agent` pipeline
3. For **research_only** proposals: manual strategy design needed before pipeline integration
4. Run backtest-expert on the selected pivot draft to begin the next iteration cycle

### Referencia: references/pivot_proposal_schema.md

# Pivot Proposal Schema

Pivot drafts are `strategy_draft`-compatible YAML files with an additive `pivot_metadata` extension. Downstream tools can ignore the extension and treat pivots as regular strategy drafts.

## Required Fields (strategy_draft compatible)

```yaml
# Identity
id: pivot_{source_archetype}_to_{target_archetype}_{timestamp}
as_of: "YYYY-MM-DD"
concept_id: <original concept_id from source strategy>
variant: research_probe
name: "<Target archetype name> (pivoted from <source>)"

# Classification
hypothesis_type: <from target archetype>
mechanism_tag: <from target archetype>
regime: <inherited from source or adjusted>
export_ready_v1: <true only if entry_family in EXPORTABLE_FAMILIES>
entry_family: <from target archetype, or research_only>

# Entry
entry:
  conditions: [<list of entry condition strings>]
  trend_filter: [<list of trend filter strings>]
  note: "Probe setup with small size for hypothesis validation."

# Exit
exit:
  stop_loss_pct: <float, e.g. 0.04>
  take_profit_rr: <float, e.g. 2.0>
  time_stop_days: <int>

# Risk
risk:
  position_sizing: fixed_risk
  risk_per_trade: <float, e.g. 0.005>
  max_positions: <int>
  max_sector_exposure: <float, e.g. 0.3>

# Validation
validation_plan:
  period: "2016-01-01 to latest"
  entry_timing: next_open
  hold_days: [<list of int>]
  success_criteria:
    - "<criterion 1>"
    - "<criterion 2>"

# Context
thesis: "<strategy thesis>"
invalidation_signals: [<list of invalidation signals>]
```

## Pivot Metadata Extension (additive)

```yaml
pivot_metadata:
  pivot_technique: <assumption_inversion | archetype_switch | objective_reframe>
  source_strategy_id: <id of the original strategy draft>
  target_archetype: <archetype id from catalog>
  what_changed:
    signal: "<description of signal change>"
    horizon: "<description of horizon change>"
    risk: "<description of risk change>"
  why: "<explanation of why this pivot addresses the trigger>"
  targeted_triggers: [<list of trigger IDs this pivot addresses>]
  expected_failure_modes:
    - "<potential failure mode 1>"
    - "<potential failure mode 2>"
  scores:
    quality_potential: <float 0-1>
    novelty: <float 0-1>
    combined: <float 0-1>
```

## Output Directory Structure

```
{output-dir}/
├── pivot_drafts/
│   ├── research_only/
│   │   └── pivot_{source}_{archetype}_{timestamp}.yaml
│   └── exportable/
│       ├── pivot_{source}_{archetype}_{timestamp}.yaml
│       └── ticket_{source}_{archetype}_{timestamp}.yaml
├── pivot_report_{strategy_id}_{timestamp}.md
└── pivot_manifest_{strategy_id}_{timestamp}.json
```

## Exportable Ticket Generation

Tickets are generated only when `entry_family` is in `EXPORTABLE_FAMILIES`:
- `pivot_breakout`
- `gap_up_continuation`

Ticket format follows `build_export_ticket()` from `design_strategy_drafts.py:222`.

## Manifest Schema

```json
{
  "generated_at_utc": "ISO-8601",
  "strategy_id": "source strategy id",
  "diagnosis_file": "path to diagnosis JSON",
  "strategy_file": "path to source draft YAML",
  "triggers_fired": ["trigger_id_1", "trigger_id_2"],
  "total_pivots_generated": 3,
  "exportable_count": 1,
  "research_only_count": 2,
  "drafts": [
    {
      "id": "pivot_...",
      "path": "relative path",
      "category": "research_only | exportable",
      "ticket_path": "relative path or null",
      "scores": {"quality_potential": 0.7, "novelty": 0.8, "combined": 0.74}
    }
  ],
  "errors": []
}
```

### Referencia: references/pivot_techniques.md

# Pivot Techniques

Three systematic techniques for generating structurally different strategy proposals when the backtest iteration loop stalls.

---

## Technique 1: Assumption Inversion

**Principle**: Identify the core assumptions of the current strategy and invert them based on which stagnation trigger fired.

### Inversion Rules by Trigger

| Trigger | Module | Inversion |
|---------|--------|-----------|
| `cost_defeat` | horizon | Shorten holding period (reduce friction exposure) |
| `cost_defeat` | universe | Shift to higher-liquidity names (reduce slippage) |
| `tail_risk` | risk | Tighten stops, reduce position size, add max drawdown cap |
| `tail_risk` | structure | Move toward market-neutral or hedged approach |
| `improvement_plateau` | signal | Change signal source (price-based → volume/fundamental) |
| `improvement_plateau` | entry | Change entry timing mechanism |
| `overfitting_proxy` | complexity | Reduce parameters, use simpler entry model |
| `overfitting_proxy` | validation | Extend test period, add regime subsamples |

### Application Process

1. Read the trigger(s) fired from the diagnosis
2. Look up the corresponding inversion rules
3. Apply each inversion to the current strategy's modules
4. Generate a new draft with the inverted assumptions

---

## Technique 2: Archetype Switch

**Principle**: Jump to a structurally different strategy archetype that addresses the same market inefficiency from a different angle.

### Process

1. Identify the current strategy's archetype from its `hypothesis_type`, `mechanism_tag`, and `entry_family`
2. Look up compatible pivot targets in the archetype catalog's `compatible_pivots_from` mapping
3. For each compatible target, generate a draft using the target archetype's default modules
4. Preserve the original concept_id and thesis where applicable

### Archetype Identification Rules

| hypothesis_type | mechanism_tag | entry_family | Archetype |
|----------------|---------------|--------------|-----------|
| breakout | behavior | pivot_breakout | trend_following_breakout |
| breakout | structural | pivot_breakout | volatility_contraction |
| mean_reversion | statistical | * | mean_reversion_pullback OR statistical_pairs |
| mean_reversion | information | * | event_driven_fade |
| earnings_drift | information | gap_up_continuation | earnings_drift_pead |
| momentum | behavior | * | sector_rotation_momentum |
| regime | macro | * | regime_conditional_carry |

When multiple archetypes match, prefer the one whose `entry_family` matches the current draft.

---

## Technique 3: Objective Reframe

**Principle**: Change what "success" means for the strategy, shifting the optimization target.

### Reframe Options

| Current Objective | Reframed To | Rationale |
|-------------------|-------------|-----------|
| Maximize Sharpe ratio | Minimize max drawdown | Better tail risk control |
| Maximize expectancy | Maximize win rate | More consistent (smaller but more frequent wins) |
| Maximize total return | Maximize risk-adjusted return per unit exposure | Capital efficiency focus |

### Application

1. Read the current strategy's `success_criteria` from `validation_plan`
2. Select a reframe based on the trigger:
   - `tail_risk` → drawdown minimization
   - `cost_defeat` → win rate maximization (smaller targets, tighter stops)
   - `improvement_plateau` → risk-adjusted return (different efficiency lens)
   - `overfitting_proxy` → simpler criteria (fewer optimization targets)
3. Adjust exit rules and risk parameters to align with the new objective
4. Update `success_criteria` in the generated draft

---

## Technique Selection by Trigger

| Trigger | Primary Technique | Secondary Technique |
|---------|-------------------|---------------------|
| `improvement_plateau` | Archetype Switch | Assumption Inversion |
| `overfitting_proxy` | Assumption Inversion | Objective Reframe |
| `cost_defeat` | Assumption Inversion | Archetype Switch |
| `tail_risk` | Assumption Inversion | Objective Reframe |

The generate_pivots script applies all applicable techniques and lets scoring determine the best candidates.

---

## Scoring

### Quality Potential (0-1)

Heuristic score based on how well a target archetype addresses the specific trigger. Defined in `QUALITY_TABLE` dictionary mapping `(trigger, archetype) → score`.

### Novelty (0-1)

Jaccard distance between the module sets of the original strategy and the proposed pivot:

```
novelty = 1 - |A ∩ B| / |A ∪ B|
```

Where A and B are sets of (key, value) pairs constructed from:
- `("hypothesis_type", <value>)`
- `("mechanism_tag", <value>)`
- `("regime", <value>)`
- `("entry_family", <value>)`
- `("horizon", <"short"|"medium"|"long">)` — time_stop_days ≤ 7: short, ≤ 30: medium, else: long
- `("risk_style", <"tight"|"normal"|"wide">)` — stop_loss_pct ≤ 0.04: tight, ≤ 0.08: normal, else: wide

### Combined Score

```
combined = 0.6 * quality_potential + 0.4 * novelty
```

### Tiebreak Rules (deterministic)

1. Combined score descending
2. Novelty descending (prefer more novel proposals)
3. Proposal ID alphabetical ascending (deterministic final sort)

### Diversity Constraint

Maximum 1 proposal per target archetype. If multiple techniques produce candidates for the same archetype, keep the one with the highest combined score.

### Referencia: references/stagnation_triggers.md

# Stagnation Triggers

Five deterministic triggers detect when a strategy's backtest iteration loop has stalled. Each trigger maps directly to fields in `evaluate_backtest.py` output accumulated in an iteration history file.

## Field Reference Mapping

| Data Point | JSON Path | Type |
|---|---|---|
| total_score | `eval.total_score` | int |
| Expectancy dim score | `eval.dimensions` (lookup by `name == "Expectancy"`) | int |
| Risk Management dim score | `eval.dimensions` (lookup by `name == "Risk Management"`) | int |
| Robustness dim score | `eval.dimensions` (lookup by `name == "Robustness"`) | int |
| red_flag IDs | `[f["id"] for f in eval.red_flags]` | list[str] |
| expectancy | `eval.expectancy` | float |
| profit_factor | `eval.profit_factor` | float or null |
| profit_factor_status | `eval.profit_factor_status` | `FINITE`, `NO_LOSSES`, `UNDEFINED_ZERO_GROSS`, or `OVERFLOW` |
| slippage_tested | `eval.inputs.slippage_tested` | bool |
| max_drawdown_pct | `eval.inputs.max_drawdown_pct` | float |

**Note**: Dimension scores are looked up by `name` field, not by array index. This makes the system resilient to future dimension reordering or additions.

---

## Trigger 1: Improvement Plateau

**ID**: `improvement_plateau`
**Severity**: high

**Condition**: Over the last K iterations (default K=3), the range of `total_score` values is less than threshold (default 3).

**Rationale**: When score stops moving despite parameter changes, the strategy architecture itself has reached a local maximum.

**Evidence fields**:
- `last_k_scores`: list of total_score values for the last K iterations
- `score_range`: max - min of last_k_scores
- `threshold`: the configured threshold

**Minimum iterations**: K (default 3). Cannot fire with fewer iterations.

---

## Trigger 2: Overfitting Proxy

**ID**: `overfitting_proxy`
**Severity**: medium

**Condition**: ALL of the following must be true:
1. Expectancy dimension score >= 15
2. Risk Management dimension score >= 15
3. Robustness dimension score < 10
4. red_flags IDs contain `over_optimized` OR `short_test_period`

**Rationale**: High in-sample performance combined with low robustness and red flags for curve-fitting suggests the strategy is optimized to historical noise rather than genuine edge.

**Minimum iterations**: 2 (needs at least some iteration history to be meaningful).

---

## Trigger 3: Cost Defeat

**ID**: `cost_defeat`
**Severity**: medium

**Condition**: ALL of the following must be true:
1. `eval.expectancy` < 0.3
2. `eval.profit_factor` < 1.3
3. `eval.inputs.slippage_tested` == True

**Rationale**: When expectancy and profit factor are thin AND slippage has already been modeled, the edge is too narrow to survive real-world execution costs. Further parameter tuning cannot create edge that isn't there.

**Minimum iterations**: 2 (requires slippage to have been tested, which implies at least one refinement cycle).

If `profit_factor` is null with `NO_LOSSES`, this trigger does not fire: positive gross profit with no gross losses is not evidence of cost defeat. Other null, non-finite, or unknown profit-factor values cannot support the ratio comparison and instead fire `insufficient_profit_factor` (high severity). This includes zero gross wins/losses and ratio overflow. Older evaluations without `profit_factor_status` are treated as unknown when their ratio is null.

---

## Trigger 4: Insufficient Profit Factor

**ID**: `insufficient_profit_factor`
**Severity**: high

**Condition**: At least two iterations and the latest profit factor is unavailable or non-finite, except an explicit `NO_LOSSES` result.

**Rationale**: The cost-defeat comparison cannot be made reliably. The reported status is retained as evidence for manual review. The diagnosis recommends `review_required`, with `stagnation_detected: false`, and pivot generation stops until a valid evaluation is available.

---

## Trigger 5: Tail Risk

**ID**: `tail_risk`
**Severity**: high

**Condition**: EITHER of the following:
1. `eval.inputs.max_drawdown_pct` > 35
2. Risk Management dimension score <= 5

**Rationale**: Extreme drawdown or catastrophically low risk management scores indicate structural risk problems that parameter tuning alone cannot fix. Requires architectural changes to risk module.

**Minimum iterations**: 1 (can fire on the very first evaluation — if drawdown is extreme, early pivot is warranted).

---

## Recommendation Decision Table

Evaluated in priority order (first match wins):

| Priority | Condition | Recommendation |
|----------|-----------|---------------|
| 1 | Latest evaluation has `decision: NOT_EVALUABLE` or `insufficient_profit_factor` | `review_required` |
| 2 | Latest `total_score` < 30 AND `iterations >= 3` AND score trajectory (last 3) is monotonically non-increasing | `abandon` |
| 3 | An actionable trigger fired | `pivot` |
| 4 | None of the above | `continue` |

**Note**: `abandon` is evaluated first. This catches cases where scores are consistently terrible but may not trip any specific trigger threshold (e.g., all scores hovering around 25 with no single trigger matching).

### Referencia: references/strategy_archetypes.md

# Strategy Archetypes Catalog

Eight canonical strategy archetypes cover the primary systematic trading approaches. Each archetype defines default modules, typical failure modes, and compatible pivot targets.

---

## 1. Trend Following Breakout (`trend_following_breakout`)

**Description**: Buy when price breaks above a consolidation range with volume confirmation. Ride the trend with trailing stops.

**Default Modules**:
- hypothesis_type: breakout
- mechanism_tag: behavior
- entry_family: pivot_breakout
- horizon: medium (10-60 days)
- risk_style: wide (trailing stop 8-12%)

**Typical Failure Modes**:
- Whipsaws in range-bound markets
- Late entries after extended moves
- Gap-downs through stop levels

**Compatible Pivots From**: mean_reversion_pullback, volatility_contraction, sector_rotation_momentum

---

## 2. Mean Reversion Pullback (`mean_reversion_pullback`)

**Description**: Buy oversold pullbacks within an established uptrend. Profit from reversion to mean.

**Default Modules**:
- hypothesis_type: mean_reversion
- mechanism_tag: statistical
- entry_family: research_only
- horizon: short (3-14 days)
- risk_style: tight (stop 3-5%)

**Typical Failure Modes**:
- Catching falling knives in trend changes
- Insufficient recovery within time stop
- Sector-wide selloffs overwhelming individual stock mean reversion

**Compatible Pivots From**: trend_following_breakout, volatility_contraction, earnings_drift_pead

---

## 3. Earnings Drift PEAD (`earnings_drift_pead`)

**Description**: Exploit post-earnings announcement drift by entering after significant earnings surprises.

**Default Modules**:
- hypothesis_type: earnings_drift
- mechanism_tag: information
- entry_family: gap_up_continuation
- horizon: medium (5-30 days)
- risk_style: normal (stop 5-8%)

**Typical Failure Modes**:
- One-day gap fills that reverse the drift
- Market-wide selloffs overwhelming individual stock drift
- Late entry after drift has already occurred

**Compatible Pivots From**: event_driven_fade, trend_following_breakout, mean_reversion_pullback

---

## 4. Volatility Contraction (`volatility_contraction`)

**Description**: Enter when volatility contracts to historical lows (VCP pattern), anticipating expansion in the trend direction.

**Default Modules**:
- hypothesis_type: breakout
- mechanism_tag: structural
- entry_family: pivot_breakout
- horizon: medium (10-40 days)
- risk_style: tight (stop 3-6%)

**Typical Failure Modes**:
- False breakouts from contraction zones
- Extended contraction periods draining capital via time stops
- Volatility expanding in the wrong direction

**Compatible Pivots From**: trend_following_breakout, mean_reversion_pullback, statistical_pairs

---

## 5. Regime Conditional Carry (`regime_conditional_carry`)

**Description**: Hold positions only during favorable macro regimes, using regime detection to filter entries.

**Default Modules**:
- hypothesis_type: regime
- mechanism_tag: macro
- entry_family: research_only
- horizon: long (30-120 days)
- risk_style: normal (stop 5-8%)

**Typical Failure Modes**:
- Regime detection lag causing late entries/exits
- Whipsaws during regime transitions
- Underperformance during trending markets due to conservative entry timing

**Compatible Pivots From**: sector_rotation_momentum, event_driven_fade, statistical_pairs

---

## 6. Sector Rotation Momentum (`sector_rotation_momentum`)

**Description**: Rotate into sectors showing relative strength momentum, exit when momentum fades.

**Default Modules**:
- hypothesis_type: momentum
- mechanism_tag: behavior
- entry_family: research_only
- horizon: medium (20-60 days)
- risk_style: normal (stop 5-8%)

**Typical Failure Modes**:
- Momentum reversals during sector rotation shifts
- Crowded trades in popular sectors
- Correlation spikes during market stress nullifying diversification

**Compatible Pivots From**: trend_following_breakout, regime_conditional_carry, earnings_drift_pead

---

## 7. Event Driven Fade (`event_driven_fade`)

**Description**: Fade overreactions to scheduled or unscheduled events, betting on mean reversion after the initial move.

**Default Modules**:
- hypothesis_type: mean_reversion
- mechanism_tag: information
- entry_family: research_only
- horizon: short (1-10 days)
- risk_style: tight (stop 2-5%)

**Typical Failure Modes**:
- Events that represent genuine regime changes (not overreactions)
- Cascading events that compound the initial move
- Liquidity gaps during extreme events

**Compatible Pivots From**: earnings_drift_pead, mean_reversion_pullback, volatility_contraction

---

## 8. Statistical Pairs (`statistical_pairs`)

**Description**: Trade cointegrated pairs, going long the undervalued and short the overvalued member when spread deviates from equilibrium.

**Default Modules**:
- hypothesis_type: mean_reversion
- mechanism_tag: statistical
- entry_family: research_only
- horizon: medium (10-30 days)
- risk_style: normal (stop via z-score threshold)

**Typical Failure Modes**:
- Cointegration breakdown due to fundamental changes
- Extended spread divergence exceeding risk limits
- Execution risk on short leg (borrow costs, locate difficulty)

**Compatible Pivots From**: mean_reversion_pullback, volatility_contraction, regime_conditional_carry

---

## Archetype Compatibility Matrix

| Source Archetype | Compatible Pivot Targets |
|---|---|
| trend_following_breakout | mean_reversion_pullback, volatility_contraction, sector_rotation_momentum |
| mean_reversion_pullback | trend_following_breakout, volatility_contraction, earnings_drift_pead |
| earnings_drift_pead | event_driven_fade, trend_following_breakout, mean_reversion_pullback |
| volatility_contraction | trend_following_breakout, mean_reversion_pullback, statistical_pairs |
| regime_conditional_carry | sector_rotation_momentum, event_driven_fade, statistical_pairs |
| sector_rotation_momentum | trend_following_breakout, regime_conditional_carry, earnings_drift_pead |
| event_driven_fade | earnings_drift_pead, mean_reversion_pullback, volatility_contraction |
| statistical_pairs | mean_reversion_pullback, volatility_contraction, regime_conditional_carry |


---

## SKILL: technical-analysis

- Fuente: `staskh/trading_skills` → `.claude/skills/technical-analysis` (MIT)
- Cuándo usarla: Compute technical indicators like RSI, MACD, Bollinger Bands, SMA, EMA for a stock. Use when user asks about technical analysis, indicators, RSI, MACD, moving averages, overbought/oversold, or chart analysis.
- Código: extraer `code/staskh_trading_skills.tar` y usar `.claude/skills/technical-analysis/` (correlation.py, technicals.py)

# Technical Analysis

Compute technical indicators using pandas-ta. Supports multi-symbol analysis and earnings data.

## Instructions

> **Note:** If `uv` is not installed or `pyproject.toml` is not found, replace `uv run python` with `python` in all commands below.

```bash
uv run python scripts/technicals.py SYMBOL [--period PERIOD] [--indicators INDICATORS] [--earnings]
```

## Arguments

- `SYMBOL` - Ticker symbol or comma-separated list (e.g., `AAPL` or `AAPL,MSFT,GOOGL`)
- `--period` - Historical period: 1mo, 3mo, 6mo, 1y (default: 3mo)
- `--indicators` - Comma-separated list: rsi,macd,bb,sma,ema,atr,adx (default: all)
- `--earnings` - Include earnings data (upcoming date + history)

## Output

Single symbol returns:
- `price` - Current price and recent change
- `indicators` - Computed values for each indicator
- `risk_metrics` - Volatility (annualized %) and Sharpe ratio
- `signals` - Buy/sell signals based on indicator levels
- `earnings` - Upcoming date and EPS history (if `--earnings`)

Multiple symbols returns:
- `results` - Array of individual symbol results

### Crossovers

- `indicators.macd.crossover` - Most recent MACD line/signal crossover, or `null`:
  - `direction` - `"up"` (MACD crossed above signal = bullish) or `"down"` (crossed below = bearish)
  - `days_ago` - Trading bars since the crossover (0 = happened on the most recent bar)
- `indicators.ema.crossover` - Most recent EMA9/EMA21 crossover (same shape; `null` if none).
  `indicators.ema` also reports `ema9` and `ema21` alongside `ema12`/`ema26`.

## Interpretation

- RSI > 70 = overbought, RSI < 30 = oversold
- MACD crossover = momentum shift; `crossover.days_ago` of 0-5 = fresh signal
- EMA9/21 crossover confirms short-term momentum; MACD typically leads, EMA confirms
- Price near Bollinger Band = potential reversal
- Golden cross (SMA20 > SMA50) = bullish
- ADX > 25 = strong trend
- Sharpe ratio > 1 = good risk-adjusted returns, > 2 = excellent
- Volatility (annualized) = standard deviation of returns scaled to annual basis

## Examples

```bash
# Single symbol with all indicators
uv run python scripts/technicals.py AAPL

# Multiple symbols
uv run python scripts/technicals.py AAPL,MSFT,GOOGL

# With earnings data
uv run python scripts/technicals.py NVDA --earnings

# Specific indicators only
uv run python scripts/technicals.py TSLA --indicators rsi,macd
```

---

# Correlation Analysis

Compute price correlation matrix between multiple symbols for diversification analysis.

## Instructions

```bash
uv run python scripts/correlation.py SYMBOLS [--period PERIOD]
```

## Arguments

- `SYMBOLS` - Comma-separated ticker symbols (minimum 2)
- `--period` - Historical period: 1mo, 3mo, 6mo, 1y (default: 3mo)

## Output

- `symbols` - List of symbols analyzed
- `period` - Time period used
- `correlation_matrix` - Nested dict with correlation values between all pairs

## Interpretation

- Correlation near 1.0 = highly correlated (move together)
- Correlation near -1.0 = negatively correlated (move opposite)
- Correlation near 0 = uncorrelated (independent movement)
- For diversification, prefer low/negative correlations

## Examples

```bash
# Portfolio correlation
uv run python scripts/correlation.py AAPL,MSFT,GOOGL,AMZN

# Sector comparison
uv run python scripts/correlation.py XLF,XLK,XLE,XLV --period 6mo

# Check hedge effectiveness
uv run python scripts/correlation.py SPY,GLD,TLT
```

## Dependencies

- `numpy`
- `pandas`
- `pandas-ta`
- `yfinance`


## Timezone

All timestamps and time-based calculations must use the `America/New_York` timezone. All JSON output must include `generated_at` (NY time string) and `data_delay` fields.


---

## SKILL: technical-analyst

- Fuente: `tradermonty/claude-trading-skills` → `examples/weekly-trade-strategy/.claude/skills/technical-analyst` (MIT)
- Cuándo usarla: This skill should be used when analyzing weekly price charts for stocks, stock indices, cryptocurrencies, or forex pairs. Use this skill when the user provides chart images and requests technical analysis, trend identification, support/resistance levels, scenario planning, or probability assessments based purely on chart data without consideration of news or fundamental factors.

# Technical Analyst

## Overview

This skill enables comprehensive technical analysis of weekly price charts. Analyze chart images to identify trends, support and resistance levels, moving average relationships, volume patterns, and develop probabilistic scenarios for future price movement. All analysis is conducted objectively using only chart data, without influence from news, fundamentals, or market sentiment.

## Core Principles

1. **Pure Chart Analysis**: Base all conclusions exclusively on technical data visible in the chart
2. **Systematic Approach**: Follow a structured methodology for each chart analysis
3. **Objective Assessment**: Avoid subjective bias; focus on observable patterns and data
4. **Probabilistic Scenarios**: Express future possibilities as probability-weighted scenarios
5. **Sequential Processing**: Analyze each chart individually and document findings immediately

## Analysis Workflow

### Step 1: Receive Chart Images

When the user provides one or more weekly chart images for analysis:

1. Confirm receipt of all chart images
2. Identify the number of charts to analyze
3. Note any specific focus areas requested by the user
4. Proceed to analyze charts sequentially, one at a time

### Step 2: Load Technical Analysis Framework

Before beginning analysis, read the comprehensive technical analysis methodology:

```
Read: references/technical_analysis_framework.md
```

This reference contains detailed guidance on:
- Trend analysis and classification
- Support and resistance identification
- Moving average interpretation
- Volume analysis
- Chart patterns and candlestick analysis
- Scenario development and probability assignment
- Analysis discipline and objectivity

### Step 3: Analyze Each Chart Systematically

For each chart image, conduct a systematic analysis following this sequence:

#### 3.1 Trend Analysis
- Identify trend direction (uptrend, downtrend, sideways)
- Assess trend strength (strong, moderate, weak)
- Note trend duration and potential exhaustion signals
- Examine higher highs/lows or lower highs/lows pattern

#### 3.2 Support and Resistance Analysis
- Mark significant horizontal support levels
- Mark significant horizontal resistance levels
- Identify trendline support/resistance
- Note any support-resistance role reversals
- Assess confluence zones where multiple S/R levels align

#### 3.3 Moving Average Analysis
- Determine price position relative to 20-week, 50-week, and 200-week MAs
- Assess MA alignment (bullish, bearish, or neutral configuration)
- Note MA slope (rising, falling, flat)
- Identify any recent or pending MA crossovers
- Observe MAs acting as dynamic support or resistance

#### 3.4 Volume Analysis
- Assess overall volume trend (increasing, decreasing, stable)
- Identify volume spikes and their context (at support/resistance, on breakouts)
- Check for volume confirmation or divergence with price
- Note any volume climax or exhaustion patterns

#### 3.5 Chart Patterns and Price Action
- Identify any reversal patterns (hammers, shooting stars, engulfing patterns, etc.)
- Identify any continuation patterns (flags, triangles, etc.)
- Note significant candlestick formations
- Observe recent breakouts or breakdowns

#### 3.6 Synthesize Observations
- Integrate all technical elements into coherent current assessment
- Identify the most significant factors influencing the chart
- Note any conflicting signals or ambiguity
- Establish key levels that will determine future direction

### Step 4: Develop Probabilistic Scenarios

For each analyzed chart, create 2-4 distinct scenarios for future price movement:

#### Scenario Structure

Each scenario must include:
1. **Scenario Name**: Clear, descriptive title (e.g., "Bull Case: Breakout Above Resistance")
2. **Probability Estimate**: Percentage likelihood based on technical factors (must sum to 100% across all scenarios)
3. **Description**: What this scenario entails and how it would unfold
4. **Supporting Factors**: Technical evidence supporting this scenario (minimum 2-3 factors)
5. **Target Levels**: Expected price levels if scenario plays out
6. **Invalidation Level**: Specific price level that would negate this scenario

#### Typical Scenario Framework

- **Base Case Scenario (40-60%)**: Most likely outcome based on current structure
- **Bull Case Scenario (20-40%)**: Optimistic scenario requiring upside breakout
- **Bear Case Scenario (20-40%)**: Pessimistic scenario requiring downside breakdown
- **Alternative Scenario (5-15%)**: Lower probability but technically plausible outcome

Adjust probabilities based on strength of supporting technical factors. Ensure probabilities are realistic and sum to 100%.

### Step 5: Generate Analysis Report

For each chart analyzed, create a comprehensive markdown report using the template structure:

```
Read and use as template: assets/analysis_template.md
```

The report must include all sections:
1. Chart Overview
2. Trend Analysis
3. Support and Resistance Levels
4. Moving Average Analysis
5. Volume Analysis
6. Chart Patterns and Price Action
7. Current Market Assessment
8. Scenario Analysis (2-4 scenarios with probabilities)
9. Summary
10. Disclaimer

**File Naming Convention**: Save each analysis as `[SYMBOL]_technical_analysis_[YYYY-MM-DD].md`

Example: `SPY_technical_analysis_2025-11-02.md`

### Step 6: Repeat for Multiple Charts

If multiple charts are provided:

1. Complete the full analysis workflow (Steps 3-5) for the first chart
2. Save the analysis report
3. Proceed to the next chart
4. Repeat until all charts have been analyzed and documented

Do not batch analyses. Complete and save each report before moving to the next chart.

## Quality Standards

### Objectivity Requirements

- Base all analysis strictly on observable chart data
- Avoid incorporating external information (news, fundamentals, sentiment)
- Do not use subjective language like "I think" or "I feel"
- Express uncertainty clearly when signals are ambiguous
- Present both bullish and bearish possibilities to avoid confirmation bias

### Completeness Requirements

- Address all sections of the analysis template
- Provide specific price levels for support, resistance, and targets
- Justify probability estimates with technical factors
- Include invalidation levels for each scenario
- Note any limitations or caveats to the analysis

### Clarity Requirements

- Use precise technical terminology correctly
- Write in clear, professional language
- Structure information logically
- Include specific price levels (not vague descriptions)
- Make scenarios distinct and mutually exclusive

## Example Usage Scenarios

**Example 1: Single Chart Analysis**
```
User: "Please analyze this weekly chart of the S&P 500"
[Provides chart image]

Analyst:
1. Confirms receipt of chart image
2. Reads technical_analysis_framework.md for methodology
3. Conducts systematic analysis (trend, S/R, MA, volume, patterns)
4. Develops 3 scenarios with probabilities (e.g., 55% bullish continuation, 30% consolidation, 15% reversal)
5. Generates comprehensive analysis report using template
6. Saves as SPY_technical_analysis_2025-11-02.md
```

**Example 2: Multiple Chart Analysis**
```
User: "Analyze these three charts: Bitcoin, Ethereum, and Nasdaq"
[Provides 3 chart images]

Analyst:
1. Confirms receipt of 3 charts
2. Reads technical_analysis_framework.md
3. Analyzes Bitcoin chart completely → Generates report → Saves as BTC_technical_analysis_2025-11-02.md
4. Analyzes Ethereum chart completely → Generates report → Saves as ETH_technical_analysis_2025-11-02.md
5. Analyzes Nasdaq chart completely → Generates report → Saves as NDX_technical_analysis_2025-11-02.md
6. Notifies user that all three analyses are complete
```

**Example 3: Focused Analysis Request**
```
User: "I'm particularly interested in whether this stock will break above resistance. Analyze the chart."
[Provides chart image]

Analyst:
1. Conducts full systematic analysis
2. Pays special attention to resistance levels and breakout probability
3. Develops scenarios with emphasis on breakout vs. rejection possibilities
4. Assigns probabilities based on volume, trend strength, and proximity to resistance
5. Generates complete report with focused scenario analysis
```

## Resources

This skill includes the following bundled resources:

### references/technical_analysis_framework.md

Comprehensive methodology for technical analysis including:
- Trend analysis criteria and classification
- Support and resistance identification techniques
- Moving average interpretation guidelines
- Volume analysis principles
- Chart pattern recognition
- Scenario development and probability assignment framework
- Objectivity and discipline reminders

**Usage**: Read this file before conducting analysis to ensure systematic, objective approach.

### assets/analysis_template.md

Structured template for technical analysis reports with all required sections.

**Usage**: Use this template structure for every analysis report. Copy the format and populate with specific findings for each chart.

### Referencia: assets/analysis_template.md

# Technical Analysis Report

**Ticker/Symbol**: [Symbol Name]
**Timeframe**: Weekly
**Analysis Date**: [YYYY-MM-DD]
**Analyst**: Claude Technical Analyst

---

## 1. Chart Overview

[Brief description of what the chart shows - instrument type, current price level, etc.]

---

## 2. Trend Analysis

### Current Trend
- **Direction**: [Uptrend / Downtrend / Sideways]
- **Strength**: [Strong / Moderate / Weak]
- **Duration**: [How long has this trend been in place]

### Trend Details
[Detailed analysis of the trend structure - higher highs/lows, lower highs/lows, etc.]

---

## 3. Support and Resistance Levels

### Key Support Levels
1. **[Price Level 1]**: [Description - why this level is significant]
2. **[Price Level 2]**: [Description]
3. **[Price Level 3]**: [Description]

### Key Resistance Levels
1. **[Price Level 1]**: [Description - why this level is significant]
2. **[Price Level 2]**: [Description]
3. **[Price Level 3]**: [Description]

### Support/Resistance Notes
[Additional observations about S/R dynamics, role reversals, or confluence zones]

---

## 4. Moving Average Analysis

### Current MA Structure
- **Price vs 20-week MA**: [Above / Below / At] - [Current relationship]
- **Price vs 50-week MA**: [Above / Below / At] - [Current relationship]
- **Price vs 200-week MA**: [Above / Below / At] - [Current relationship]

### MA Configuration
- **Alignment**: [Bullish / Bearish / Neutral]
- **Slope**: [Rising / Falling / Flat]
- **Crossovers**: [Any recent or pending crossovers]

### MA as Support/Resistance
[Observations about MAs acting as dynamic support or resistance]

---

## 5. Volume Analysis

### Volume Trend
[Description of recent volume patterns - increasing, decreasing, or stable]

### Volume Observations
- [Key observation 1 - e.g., volume spike at support]
- [Key observation 2 - e.g., declining volume on rally]
- [Key observation 3 - e.g., volume divergence]

### Volume Confirmation
[Assessment of whether volume confirms or contradicts the price action]

---

## 6. Chart Patterns and Price Action

### Identified Patterns
[List any chart patterns, candlestick patterns, or notable price action]

- **Pattern 1**: [Name and description]
- **Pattern 2**: [Name and description]

### Price Action Notes
[Additional observations about recent price behavior, breakouts, rejections, etc.]

---

## 7. Current Market Assessment

### Overall Structure
[Synthesize all the above elements into a coherent view of the current chart structure]

### Key Observations
1. [Most important observation]
2. [Second important observation]
3. [Third important observation]

---

## 8. Scenario Analysis

### Scenario 1: [Scenario Name] - **[XX]% Probability**

**Description**: [What this scenario entails]

**Supporting Factors**:
- [Factor 1]
- [Factor 2]
- [Factor 3]

**Target Levels**: [Upside or downside targets if this scenario plays out]

**Invalidation Level**: [Price level that would negate this scenario]

---

### Scenario 2: [Scenario Name] - **[XX]% Probability**

**Description**: [What this scenario entails]

**Supporting Factors**:
- [Factor 1]
- [Factor 2]
- [Factor 3]

**Target Levels**: [Upside or downside targets if this scenario plays out]

**Invalidation Level**: [Price level that would negate this scenario]

---

### Scenario 3: [Scenario Name] - **[XX]% Probability**

**Description**: [What this scenario entails]

**Supporting Factors**:
- [Factor 1]
- [Factor 2]
- [Factor 3]

**Target Levels**: [Upside or downside targets if this scenario plays out]

**Invalidation Level**: [Price level that would negate this scenario]

---

### Scenario 4 (Optional): [Scenario Name] - **[XX]% Probability**

**Description**: [What this scenario entails]

**Supporting Factors**:
- [Factor 1]
- [Factor 2]

**Target Levels**: [Upside or downside targets if this scenario plays out]

**Invalidation Level**: [Price level that would negate this scenario]

---

## 9. Summary

### Most Likely Outcome
[Brief statement of the highest probability scenario]

### Key Levels to Watch
- **Critical Support**: [Level]
- **Critical Resistance**: [Level]

### Risk Considerations
[Important caveats, limitations of the analysis, or factors that could disrupt scenarios]

---

## 10. Disclaimer

This analysis is based purely on technical chart data and does not consider fundamental factors, news, or market sentiment. It represents a probabilistic assessment of potential scenarios, not a prediction or investment recommendation. All probabilities are estimates based on technical factors and subject to change as new data emerges.

---

**End of Analysis**

### Referencia: references/technical_analysis_framework.md

# Technical Analysis Framework

This reference provides the methodology for conducting objective, chart-based technical analysis of weekly price charts.

## Core Principles

1. **Chart-Only Analysis**: Base all analysis purely on chart data. Ignore external news, fundamental data, and market sentiment.
2. **Objectivity**: Focus on observable patterns and data rather than subjective interpretations.
3. **Weekly Timeframe**: All analysis uses weekly charts for medium to long-term perspective.
4. **Probability-Based**: Express future scenarios as probabilities rather than certainties.

## 1. Trend Analysis

### Trend Classification

**Uptrend Criteria:**
- Higher highs (HH) and higher lows (HL) pattern
- Price trading above key moving averages
- Moving averages aligned in bullish order (shorter MA > longer MA)

**Downtrend Criteria:**
- Lower highs (LH) and lower lows (LL) pattern
- Price trading below key moving averages
- Moving averages aligned in bearish order (shorter MA < longer MA)

**Sideways/Range-bound:**
- No clear higher high/low or lower high/low pattern
- Price oscillating between defined support and resistance levels
- Moving averages flat or intertwined

### Trend Strength Assessment

**Strong Trend:**
- Clear, consecutive higher highs/lows (uptrend) or lower highs/lows (downtrend)
- Minimal retracements
- Volume confirming price direction

**Weak Trend:**
- Irregular higher/lower highs and lows
- Deep retracements (>50% of prior move)
- Divergence between price and volume

**Trend Exhaustion Signals:**
- Decreasing momentum on new highs/lows
- Volume declining as trend progresses
- Extended distance from moving averages
- Candlestick reversal patterns (e.g., shooting star, hammer, engulfing)

## 2. Support and Resistance Analysis

### Identifying Support Levels

Support represents price levels where buying interest has historically prevented further decline.

**Criteria for Valid Support:**
- Price has bounced from the level at least 2-3 times
- Volume spikes during bounces
- Longer timeframe support carries more weight
- Round numbers (psychological levels) often act as support

**Support Types:**
- **Horizontal Support**: Previous lows aligning at similar price levels
- **Trendline Support**: Upward-sloping line connecting higher lows
- **Moving Average Support**: Dynamic support from key MAs (e.g., 20-week, 50-week)

### Identifying Resistance Levels

Resistance represents price levels where selling interest has historically prevented further advance.

**Criteria for Valid Resistance:**
- Price has been rejected from the level at least 2-3 times
- Volume spikes during rejections
- Previous significant highs
- Round numbers often act as resistance

**Resistance Types:**
- **Horizontal Resistance**: Previous highs aligning at similar price levels
- **Trendline Resistance**: Downward-sloping line connecting lower highs
- **Moving Average Resistance**: Dynamic resistance from key MAs

### Support/Resistance Significance

**Strong S/R Levels:**
- Tested multiple times (3+ touches)
- Long-standing (months to years)
- High volume at previous touches
- Confluence with other technical factors (Fibonacci, round numbers, moving averages)

**Weak S/R Levels:**
- Only 1-2 touches
- Recent formation
- Low volume at touches

### Support-Resistance Flip

When broken, support often becomes resistance and vice versa. This "role reversal" is a key concept:
- **Broken Support → Resistance**: After downside break, previous support acts as new resistance on retests
- **Broken Resistance → Support**: After upside break, previous resistance acts as new support on pullbacks

## 3. Moving Average Analysis

### Key Moving Averages for Weekly Charts

- **20-week MA**: Short-term trend indicator (approximately 4 months)
- **50-week MA**: Medium-term trend indicator (approximately 1 year)
- **200-week MA**: Long-term trend indicator (approximately 4 years)

### Moving Average Interpretations

**Price Position Relative to MAs:**
- **Above all MAs**: Strong bullish structure
- **Below all MAs**: Strong bearish structure
- **Between MAs**: Transitional phase, trend unclear

**Moving Average Crossovers:**
- **Golden Cross**: 20-week MA crosses above 50-week MA (bullish signal)
- **Death Cross**: 20-week MA crosses below 50-week MA (bearish signal)

**Moving Average Slope:**
- **Rising MAs**: Bullish momentum
- **Falling MAs**: Bearish momentum
- **Flat MAs**: Consolidation, lack of directional momentum

**Moving Average as Support/Resistance:**
- In uptrends, MAs (especially 20-week and 50-week) often provide dynamic support
- In downtrends, MAs often provide dynamic resistance
- Repeated bounces or rejections from MA increase its significance

### Moving Average Confluence

When multiple MAs cluster together or align:
- **Bullish Alignment**: 20-week > 50-week > 200-week (all rising)
- **Bearish Alignment**: 20-week < 50-week < 200-week (all falling)
- **Compressed/Converging MAs**: Often precedes significant directional move

## 4. Volume Analysis

Volume confirms the strength or weakness of price movements.

### Volume Interpretation Principles

**Volume Confirms Price:**
- **Rising prices + Rising volume**: Healthy uptrend, strong buying
- **Falling prices + Rising volume**: Healthy downtrend, strong selling
- **Rising prices + Falling volume**: Weak uptrend, lack of conviction
- **Falling prices + Falling volume**: Weak downtrend, selling exhaustion possible

### Key Volume Patterns

**Volume Spikes:**
- **At Support**: High volume bounce suggests strong buying interest (bullish)
- **At Resistance**: High volume rejection suggests strong selling interest (bearish)
- **On Breakout**: High volume breakout validates the move
- **Low Volume Breakout**: Often leads to failed breakout (false signal)

**Volume Trends:**
- **Increasing Volume in Trend Direction**: Confirms trend strength
- **Decreasing Volume in Trend Direction**: Warns of potential trend exhaustion
- **Volume Climax**: Extremely high volume often marks trend extremes (capitulation or euphoria)

**Volume Divergence:**
- **Bullish Divergence**: Price making new lows but volume declining (selling exhaustion)
- **Bearish Divergence**: Price making new highs but volume declining (buying exhaustion)

## 5. Chart Patterns and Candlestick Analysis

### Reversal Patterns

**Bullish Reversal:**
- **Hammer**: Long lower wick, small body at top, appears at support
- **Bullish Engulfing**: Large green candle fully engulfing previous red candle
- **Morning Star**: Three-candle pattern (down, small, up)
- **Double/Triple Bottom**: Price tests support 2-3 times then reverses

**Bearish Reversal:**
- **Shooting Star**: Long upper wick, small body at bottom, appears at resistance
- **Bearish Engulfing**: Large red candle fully engulfing previous green candle
- **Evening Star**: Three-candle pattern (up, small, down)
- **Double/Triple Top**: Price tests resistance 2-3 times then reverses

### Continuation Patterns

**Bullish Continuation:**
- **Bull Flag**: Consolidation after strong move up, then breakout higher
- **Ascending Triangle**: Higher lows with flat resistance, breaks up

**Bearish Continuation:**
- **Bear Flag**: Consolidation after strong move down, then breakdown
- **Descending Triangle**: Lower highs with flat support, breaks down

### Pattern Significance

Patterns carry more weight when:
- Forming at key support/resistance levels
- Accompanied by appropriate volume (high on breakout)
- Confirmed by moving averages and trend structure
- Occurring on longer timeframes (weekly > daily)

## 6. Scenario Development and Probability Assignment

### Scenario Development Process

For each chart analysis, develop 2-4 potential scenarios:

1. **Base Case Scenario**: Most likely outcome based on current chart structure
2. **Bull Case Scenario**: Optimistic scenario if key resistance breaks
3. **Bear Case Scenario**: Pessimistic scenario if key support breaks
4. **Alternative Scenario** (optional): Lower probability but plausible outcome

### Probability Assignment Framework

Assign probabilities based on:

**High Probability (50-70%):**
- Scenario aligned with current trend
- Multiple confirming factors (trend, S/R, MA, volume)
- Recent price action supports scenario
- Clear invalidation level

**Medium Probability (25-45%):**
- Scenario requires trend change or major breakout
- Some supporting factors but not all
- Depends on key level holding/breaking

**Low Probability (5-20%):**
- Scenario contrary to most technical factors
- Requires significant shift in structure
- Limited supporting evidence but technically possible

### Probability Assignment Example

Current Structure: Uptrend, above all MAs, holding support

- **Bull Case (60%)**: Continuation higher after pullback to support
  - Reasoning: Trend intact, holding key support, volume confirming

- **Base Case (30%)**: Consolidation/range before next move
  - Reasoning: Approaching resistance, some profit-taking visible

- **Bear Case (10%)**: Break below support, trend reversal
  - Reasoning: No clear reversal signals yet, but always possible

**Note**: Probabilities should sum to 100%. Adjust based on strength of supporting factors.

### Invalidation Levels

For each scenario, define a specific price level that would invalidate it:
- **Bull Scenario Invalidation**: Break below key support
- **Bear Scenario Invalidation**: Break above key resistance
- **Base Case Invalidation**: Breakout from range in either direction

## 7. Analysis Structure and Discipline

### Analysis Checklist

For each chart, systematically evaluate:

1. ✓ **Current Trend**: Identify direction, strength, and duration
2. ✓ **Support Levels**: Mark significant horizontal and dynamic support
3. ✓ **Resistance Levels**: Mark significant horizontal and dynamic resistance
4. ✓ **Moving Averages**: Note position, slope, and crossovers
5. ✓ **Volume Pattern**: Assess if volume confirms or contradicts price
6. ✓ **Chart Patterns**: Identify any significant patterns forming or completing
7. ✓ **Scenarios**: Develop 2-4 scenarios with probability estimates
8. ✓ **Invalidation Levels**: Define what would negate each scenario

### Objectivity Reminders

- Avoid confirmation bias: Consider both bullish and bearish scenarios
- Let the chart speak: Don't force patterns or signals
- Update analysis as new data emerges: Charts are dynamic
- Admit uncertainty: Not every chart provides clear signals
- Focus on probabilities, not predictions: No scenario is 100% certain

### Common Pitfalls to Avoid

- **Overcomplicating**: Too many indicators can lead to analysis paralysis
- **Ignoring Volume**: Price without volume is incomplete picture
- **Forcing Patterns**: Seeing patterns that aren't clearly there
- **Disregarding Timeframe**: Weekly chart may differ from daily
- **Neglecting Context**: Each chart in isolation, but overall market matters
- **Being Too Certain**: Markets are probabilistic, not deterministic


---

## SKILL: technical-analyst

- Fuente: `tradermonty/claude-trading-skills` → `skills/technical-analyst` (MIT)
- Cuándo usarla: This skill should be used when analyzing weekly price charts for stocks, stock indices, cryptocurrencies, or forex pairs. Use this skill when the user provides chart images and requests technical analysis, trend identification, support/resistance levels, scenario planning, or probability assessments based purely on chart data without consideration of news or fundamental factors.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/technical-analyst/` (requirements.txt, check_weekly_price_action.py, weekly_price_action.py)

# Technical Analyst

## Overview

This skill enables comprehensive technical analysis of weekly price charts. Analyze chart images to identify trends, support and resistance levels, moving average relationships, volume patterns, and develop probabilistic scenarios for future price movement. All analysis is conducted objectively using only chart data, without influence from news, fundamentals, or market sentiment.

## When to Use

- User provides weekly chart images (stocks, indices, crypto, forex) and requests technical analysis
- Need to identify trend direction, strength, and potential reversal points
- Looking for support/resistance levels and key price zones
- Want probabilistic scenario planning with specific price targets
- Require objective chart-based analysis without fundamental or news considerations

## Prerequisites

- **Chart Images**: User must provide weekly timeframe chart images for analysis
- **No API Keys Required**: This skill analyzes user-provided images; no external data fetches

## Output

This skill generates markdown analysis reports saved to the `reports/` directory:
- **File format**: `[SYMBOL]_technical_analysis_[YYYY-MM-DD].md`
- **Content**: Comprehensive analysis including trend, S/R levels, MA analysis, volume, patterns, and 2-4 probabilistic scenarios with targets and invalidation levels

## Core Principles

1. **Pure Chart Analysis**: Base all conclusions exclusively on technical data visible in the chart
2. **Systematic Approach**: Follow a structured methodology for each chart analysis
3. **Objective Assessment**: Avoid subjective bias; focus on observable patterns and data
4. **Probabilistic Scenarios**: Express future possibilities as probability-weighted scenarios
5. **Sequential Processing**: Analyze each chart individually and document findings immediately

## Analysis Workflow

### Step 1: Receive Chart Images

When the user provides one or more weekly chart images for analysis:

1. Confirm receipt of all chart images
2. Identify the number of charts to analyze
3. Note any specific focus areas requested by the user
4. Proceed to analyze charts sequentially, one at a time

### Step 2: Load Technical Analysis Framework

Before beginning analysis, read the comprehensive technical analysis methodology:

```
Read: references/technical_analysis_framework.md
```

This reference contains detailed guidance on:
- Trend analysis and classification
- Support and resistance identification
- Moving average interpretation
- Volume analysis
- Chart patterns and candlestick analysis
- Scenario development and probability assignment
- Analysis discipline and objectivity

### Step 3: Analyze Each Chart Systematically

For each chart image, conduct a systematic analysis following this sequence:

#### 3.1 Trend Analysis
- Identify trend direction (uptrend, downtrend, sideways)
- Assess trend strength (strong, moderate, weak)
- Note trend duration and potential exhaustion signals
- Examine higher highs/lows or lower highs/lows pattern

#### 3.2 Support and Resistance Analysis
- Mark significant horizontal support levels
- Mark significant horizontal resistance levels
- Identify trendline support/resistance
- Note any support-resistance role reversals
- Assess confluence zones where multiple S/R levels align

#### 3.3 Moving Average Analysis
- Determine price position relative to 20-week, 50-week, and 200-week MAs
- Assess MA alignment (bullish, bearish, or neutral configuration)
- Note MA slope (rising, falling, flat)
- Identify any recent or pending MA crossovers
- Observe MAs acting as dynamic support or resistance

#### 3.4 Volume Analysis
- Assess overall volume trend (increasing, decreasing, stable)
- Identify volume spikes and their context (at support/resistance, on breakouts)
- Check for volume confirmation or divergence with price
- Note any volume climax or exhaustion patterns

#### 3.5 Chart Patterns and Price Action
- Identify any reversal patterns (hammers, shooting stars, engulfing patterns, etc.)
- Identify any continuation patterns (flags, triangles, etc.)
- Note significant candlestick formations
- Observe recent breakouts or breakdowns

#### 3.6 Synthesize Observations
- Integrate all technical elements into coherent current assessment
- Identify the most significant factors influencing the chart
- Note any conflicting signals or ambiguity
- Establish key levels that will determine future direction

### Step 4: Develop Probabilistic Scenarios

For each analyzed chart, create 2-4 distinct scenarios for future price movement:

#### Scenario Structure

Each scenario must include:
1. **Scenario Name**: Clear, descriptive title (e.g., "Bull Case: Breakout Above Resistance")
2. **Probability Estimate**: Percentage likelihood based on technical factors (must sum to 100% across all scenarios)
3. **Description**: What this scenario entails and how it would unfold
4. **Supporting Factors**: Technical evidence supporting this scenario (minimum 2-3 factors)
5. **Target Levels**: Expected price levels if scenario plays out
6. **Invalidation Level**: Specific price level that would negate this scenario

#### Typical Scenario Framework

- **Base Case Scenario (40-60%)**: Most likely outcome based on current structure
- **Bull Case Scenario (20-40%)**: Optimistic scenario requiring upside breakout
- **Bear Case Scenario (20-40%)**: Pessimistic scenario requiring downside breakdown
- **Alternative Scenario (5-15%)**: Lower probability but technically plausible outcome

Adjust probabilities based on strength of supporting technical factors. Ensure probabilities are realistic and sum to 100%.

### Step 5: Generate Analysis Report

For each chart analyzed, create a comprehensive markdown report using the template structure:

```
Read and use as template: assets/analysis_template.md
```

The report must include all sections:
1. Chart Overview
2. Trend Analysis
3. Support and Resistance Levels
4. Moving Average Analysis
5. Volume Analysis
6. Chart Patterns and Price Action
7. Current Market Assessment
8. Scenario Analysis (2-4 scenarios with probabilities)
9. Summary
10. Disclaimer

**File Naming Convention**: Save each analysis as `[SYMBOL]_technical_analysis_[YYYY-MM-DD].md`

Example: `SPY_technical_analysis_2025-11-02.md`

### Step 6: Repeat for Multiple Charts

If multiple charts are provided:

1. Complete the full analysis workflow (Steps 3-5) for the first chart
2. Save the analysis report
3. Proceed to the next chart
4. Repeat until all charts have been analyzed and documented

Do not batch analyses. Complete and save each report before moving to the next chart.

## Quality Standards

### Objectivity Requirements

- Base all analysis strictly on observable chart data
- Avoid incorporating external information (news, fundamentals, sentiment)
- Do not use subjective language like "I think" or "I feel"
- Express uncertainty clearly when signals are ambiguous
- Present both bullish and bearish possibilities to avoid confirmation bias

### Completeness Requirements

- Address all sections of the analysis template
- Provide specific price levels for support, resistance, and targets
- Justify probability estimates with technical factors
- Include invalidation levels for each scenario
- Note any limitations or caveats to the analysis

### Clarity Requirements

- Use precise technical terminology correctly
- Write in clear, professional language
- Structure information logically
- Include specific price levels (not vague descriptions)
- Make scenarios distinct and mutually exclusive

## Example Usage Scenarios

**Example 1: Single Chart Analysis**
```
User: "Please analyze this weekly chart of the S&P 500"
[Provides chart image]

Analyst:
1. Confirms receipt of chart image
2. Reads technical_analysis_framework.md for methodology
3. Conducts systematic analysis (trend, S/R, MA, volume, patterns)
4. Develops 3 scenarios with probabilities (e.g., 55% bullish continuation, 30% consolidation, 15% reversal)
5. Generates comprehensive analysis report using template
6. Saves as SPY_technical_analysis_2025-11-02.md
```

**Example 2: Multiple Chart Analysis**
```
User: "Analyze these three charts: Bitcoin, Ethereum, and Nasdaq"
[Provides 3 chart images]

Analyst:
1. Confirms receipt of 3 charts
2. Reads technical_analysis_framework.md
3. Analyzes Bitcoin chart completely → Generates report → Saves as BTC_technical_analysis_2025-11-02.md
4. Analyzes Ethereum chart completely → Generates report → Saves as ETH_technical_analysis_2025-11-02.md
5. Analyzes Nasdaq chart completely → Generates report → Saves as NDX_technical_analysis_2025-11-02.md
6. Notifies user that all three analyses are complete
```

**Example 3: Focused Analysis Request**
```
User: "I'm particularly interested in whether this stock will break above resistance. Analyze the chart."
[Provides chart image]

Analyst:
1. Conducts full systematic analysis
2. Pays special attention to resistance levels and breakout probability
3. Develops scenarios with emphasis on breakout vs. rejection possibilities
4. Assigns probabilities based on volume, trend strength, and proximity to resistance
5. Generates complete report with focused scenario analysis
```

## Contrarian Confirmation Mode (Shapiro Step 3)

This is an ADDITIVE mode, separate from the pure chart-analysis workflow
above. It activates only on an explicit contrarian-confirmation request —
typically after `cot-contrarian-detector` (step 1) has flagged a market
crowded and, optionally, `news-reaction-failure-analyzer` (step 2) has
shown it failed to react to favorable news. A plain "analyze this chart"
request still runs the original workflow (Steps 1-6 above) unchanged.

### Purpose

Confirm whether the WEEKLY chart is showing price-action evidence that a
crowded market is reversing: a weekly key reversal, an intraweek failed
extreme, or a confirmed-then-rejected failed breakout — vetoed by a
continuation check (a new closing extreme in the crowd's direction more
recent than any signal found). See
`references/contrarian-confirmation-checklist.md` for the full,
word-for-word methodology shared by both chart mode and script mode.

### Inputs

- **Crowd direction**: `CROWDED_LONG` or `CROWDED_SHORT` — from the user,
  or from a prior `cot-contrarian-detector` report.
- **Chart image (primary)**: a user-supplied weekly chart, read the same
  way as the existing workflow, using the strict definitions below.
- **Script fallback (data-driven)**: `scripts/check_weekly_price_action.py`
  when no chart is supplied, or when an auditable, deterministic result is
  wanted instead of (or alongside) a visual read.

### The Three Checks + Swing Levels

1. **Weekly key reversal**: a new swing-lookback extreme (default 13
   weeks) followed by a close through the prior week's opposite level.
2. **Failed extreme**: an intraweek poke past the prior extreme-lookback
   level (default 52 weeks) that closes back through it the same week.
3. **Failed breakout**: a weekly CLOSING breakout past the prior
   extreme-lookback level, rejected (closed back through) within <=3
   subsequent weeks — `week_of` is the FAILURE week, never the breakout
   week.
4. **Continuation veto**: a new CLOSING extreme in the crowd's direction,
   strictly more recent than the newest triggered signal above, vetoes
   confirmation regardless of what triggered.
5. **Swing levels**: the nearest fractal swing high/low (5-week pivot,
   with a documented fallback) supplies `stop_reference` — the nearest
   swing high when fading a crowded LONG, the nearest swing low when
   fading a crowded SHORT.

Every comparison is a STRICT inequality; window truncation is
per-evaluated-week, not per-run. Full definitions, the direction-mirror
table, worked examples, and the confidence-HIGH rule are in
`references/contrarian-confirmation-checklist.md` — read it before
producing a chart-mode verdict, so chart and script judge identically.

### Output Contract

```yaml
symbol: BT
direction: CROWDED_LONG
mode: data # "chart" for a Claude chart-image read
verdict: CONFIRMED | NOT_CONFIRMED | INSUFFICIENT_DATA
confidence: HIGH | MEDIUM | LOW # LOW reserved, never emitted in v1
verdict_reason: key_reversal | failed_extreme | failed_breakout |
  continuation_intact | no_reversal_evidence |
  insufficient_weekly_bars | no_price_source | ...
checks:
  weekly_key_reversal:
    { triggered, week_of, swing_window_weeks_used,
      extreme_window_weeks_used, is_full_window_extreme, detail }
  failed_extreme: { triggered, attempted_level, week_of, window_weeks_used, detail }
  failed_breakout: { triggered, breakout_level, week_of, window_weeks_used, detail }
  continuation: { new_closing_extreme_with_crowd, week_of, window_weeks_used }
swing_levels:
  nearest_swing_high: { price, week_of, fallback }
  nearest_swing_low: { price, week_of, fallback }
  stop_reference: 0.0
weekly_bars_used: 52
last_completed_week: 2026-07-06
handoff: # consumed by contrarian-setup-gate (#241)
  price_action: { verdict, confidence, stop_reference, report_path }
run_context:
  {
    price_symbol,
    price_source,
    proxy_used,
    as_of,
    lookbacks,
    recency,
    min_weeks,
    detector_json,
    detector_age_days,
    schema_version,
  }
```

**Invariant**: `checks` (and `swing_levels`) is `null` whenever
`verdict: INSUFFICIENT_DATA` — regardless of the specific reason
(`no_price_source`, `insufficient_weekly_bars`, a detector-json refusal,
...). A downstream consumer can check `verdict` alone before deciding
whether `checks.*` is safe to read, without branching on
`verdict_reason`.

**File naming**: `ta_confirmation_<SYMBOL>_<as-of>.json` and
`ta_confirmation_<SYMBOL>_<as-of>.md`, saved to `reports/`.

### Chart-Primary, Script-Fallback

Chart images remain the PRIMARY input, consistent with this skill's
identity. Run the script instead of (or alongside) a chart read when no
chart is supplied, or when an auditable, deterministic result is
preferred:

```bash
python3 skills/technical-analyst/scripts/check_weekly_price_action.py \
  --symbol BT --direction CROWDED_LONG --as-of 2026-07-15 \
  --output-dir reports/
```

Or resolve direction from a `cot-contrarian-detector` report directly:

```bash
python3 skills/technical-analyst/scripts/check_weekly_price_action.py \
  --symbol BT --detector-json reports/cot_crowding_2026-07-12.json \
  --as-of 2026-07-15 --output-dir reports/
```

The script fetches weekly-resampled OHLC via a documented futures-to-ETF
fallback chain (see the module docstring in
`scripts/check_weekly_price_action.py`), truncates daily bars to `--as-of`
BEFORE resampling (no lookahead), and fails closed to
`INSUFFICIENT_DATA` — never a crash — on an unreadable (missing file),
syntactically invalid, stale, or structurally malformed `--detector-json`,
too little price history (`--min-weeks`, default 30), or no usable price
source.

### Conservative Disagreement Rule

If both chart mode and script mode produce a result for the same
symbol/direction and their verdicts DISAGREE, the final verdict is
**`NOT_CONFIRMED`** (`verdict_reason: mode_disagreement`), with both
sub-results attached for review — never silently prefer one mode. If one
mode is `INSUFFICIENT_DATA` and the other is a clean verdict, the clean
verdict stands.

### Guardrails

- **Verdict-only — never a trade recommendation on its own.** This
  confirms step 3 of 5 (Shapiro's process). Entry and exit planning are
  still manual and still required; position sizing belongs to
  `position-sizer` / `futures-position-sizer`, not this mode.
- **`INSUFFICIENT_DATA` never advances the pipeline** — fail-closed on
  every degraded input, always exits 0 with a report written.
- **Weekly timeframe only.**
- **The existing chart-analysis workflow above is unchanged** — this mode
  only activates on an explicit contrarian-confirmation request.
- **A single-signal MEDIUM verdict is deliberately weak evidence** — see
  the Confidence section of `references/contrarian-confirmation-checklist.md`.

## Resources

This skill includes the following bundled resources:

### references/technical_analysis_framework.md

Comprehensive methodology for technical analysis including:
- Trend analysis criteria and classification
- Support and resistance identification techniques
- Moving average interpretation guidelines
- Volume analysis principles
- Chart pattern recognition
- Scenario development and probability assignment framework
- Objectivity and discipline reminders

**Usage**: Read this file before conducting analysis to ensure systematic, objective approach.

### assets/analysis_template.md

Structured template for technical analysis reports with all required sections.

**Usage**: Use this template structure for every analysis report. Copy the format and populate with specific findings for each chart.

### references/contrarian-confirmation-checklist.md

Full methodology for Contrarian Confirmation Mode (Shapiro Step 3): direction
convention, window/truncation rules, the 3 signal checks + continuation
veto, swing-level (fractal pivot) rules, verdict synthesis, confidence
rules, the output contract, a chart-mode walkthrough, and the conservative
disagreement rule.

**Usage**: Read this file before producing a Contrarian Confirmation Mode
verdict — chart mode and `scripts/check_weekly_price_action.py` must judge
identically, so the same strict definitions apply to both.

### scripts/check_weekly_price_action.py

Data-driven fallback CLI for Contrarian Confirmation Mode. Fetches
weekly-resampled OHLC (documented futures-to-ETF fallback chain,
`--as-of` information cutoff applied before resampling), runs the 3
signal checks + continuation veto + swing-level detection, and writes
`ta_confirmation_<SYMBOL>_<as-of>.json`/`.md` to `reports/`.

**Usage**: Run when no chart image is supplied, or when an auditable,
deterministic result is wanted. See the Contrarian Confirmation Mode
section above for invocation examples.

### Referencia: assets/analysis_template.md

# Technical Analysis Report

**Ticker/Symbol**: [Symbol Name]
**Timeframe**: Weekly
**Analysis Date**: [YYYY-MM-DD]
**Analyst**: Claude Technical Analyst

---

## 1. Chart Overview

[Brief description of what the chart shows - instrument type, current price level, etc.]

---

## 2. Trend Analysis

### Current Trend
- **Direction**: [Uptrend / Downtrend / Sideways]
- **Strength**: [Strong / Moderate / Weak]
- **Duration**: [How long has this trend been in place]

### Trend Details
[Detailed analysis of the trend structure - higher highs/lows, lower highs/lows, etc.]

---

## 3. Support and Resistance Levels

### Key Support Levels
1. **[Price Level 1]**: [Description - why this level is significant]
2. **[Price Level 2]**: [Description]
3. **[Price Level 3]**: [Description]

### Key Resistance Levels
1. **[Price Level 1]**: [Description - why this level is significant]
2. **[Price Level 2]**: [Description]
3. **[Price Level 3]**: [Description]

### Support/Resistance Notes
[Additional observations about S/R dynamics, role reversals, or confluence zones]

---

## 4. Moving Average Analysis

### Current MA Structure
- **Price vs 20-week MA**: [Above / Below / At] - [Current relationship]
- **Price vs 50-week MA**: [Above / Below / At] - [Current relationship]
- **Price vs 200-week MA**: [Above / Below / At] - [Current relationship]

### MA Configuration
- **Alignment**: [Bullish / Bearish / Neutral]
- **Slope**: [Rising / Falling / Flat]
- **Crossovers**: [Any recent or pending crossovers]

### MA as Support/Resistance
[Observations about MAs acting as dynamic support or resistance]

---

## 5. Volume Analysis

### Volume Trend
[Description of recent volume patterns - increasing, decreasing, or stable]

### Volume Observations
- [Key observation 1 - e.g., volume spike at support]
- [Key observation 2 - e.g., declining volume on rally]
- [Key observation 3 - e.g., volume divergence]

### Volume Confirmation
[Assessment of whether volume confirms or contradicts the price action]

---

## 6. Chart Patterns and Price Action

### Identified Patterns
[List any chart patterns, candlestick patterns, or notable price action]

- **Pattern 1**: [Name and description]
- **Pattern 2**: [Name and description]

### Price Action Notes
[Additional observations about recent price behavior, breakouts, rejections, etc.]

---

## 7. Current Market Assessment

### Overall Structure
[Synthesize all the above elements into a coherent view of the current chart structure]

### Key Observations
1. [Most important observation]
2. [Second important observation]
3. [Third important observation]

---

## 8. Scenario Analysis

### Scenario 1: [Scenario Name] - **[XX]% Probability**

**Description**: [What this scenario entails]

**Supporting Factors**:
- [Factor 1]
- [Factor 2]
- [Factor 3]

**Target Levels**: [Upside or downside targets if this scenario plays out]

**Invalidation Level**: [Price level that would negate this scenario]

---

### Scenario 2: [Scenario Name] - **[XX]% Probability**

**Description**: [What this scenario entails]

**Supporting Factors**:
- [Factor 1]
- [Factor 2]
- [Factor 3]

**Target Levels**: [Upside or downside targets if this scenario plays out]

**Invalidation Level**: [Price level that would negate this scenario]

---

### Scenario 3: [Scenario Name] - **[XX]% Probability**

**Description**: [What this scenario entails]

**Supporting Factors**:
- [Factor 1]
- [Factor 2]
- [Factor 3]

**Target Levels**: [Upside or downside targets if this scenario plays out]

**Invalidation Level**: [Price level that would negate this scenario]

---

### Scenario 4 (Optional): [Scenario Name] - **[XX]% Probability**

**Description**: [What this scenario entails]

**Supporting Factors**:
- [Factor 1]
- [Factor 2]

**Target Levels**: [Upside or downside targets if this scenario plays out]

**Invalidation Level**: [Price level that would negate this scenario]

---

## 9. Summary

### Most Likely Outcome
[Brief statement of the highest probability scenario]

### Key Levels to Watch
- **Critical Support**: [Level]
- **Critical Resistance**: [Level]

### Risk Considerations
[Important caveats, limitations of the analysis, or factors that could disrupt scenarios]

---

## 10. Disclaimer

This analysis is based purely on technical chart data and does not consider fundamental factors, news, or market sentiment. It represents a probabilistic assessment of potential scenarios, not a prediction or investment recommendation. All probabilities are estimates based on technical factors and subject to change as new data emerges.

---

**End of Analysis**

### Referencia: references/contrarian-confirmation-checklist.md

# Contrarian Confirmation Checklist (Shapiro Step 3)

## Overview

Step 3 of Jason Shapiro's COT contrarian process: once a market is flagged
crowded (`cot-contrarian-detector`, step 1) and, optionally, shown to have
failed to react to favorable news (`news-reaction-failure-analyzer`, step
2), this checklist confirms whether the WEEKLY chart itself is showing
price-action evidence of a reversal. It is the last check before entry
planning (step 4, still manual) and exit planning (step 5, still manual).

**This checklist is judged identically by two consumers**: Claude reading
a user-supplied weekly chart image (chart mode, `technical-analyst`'s
primary workflow) and `scripts/check_weekly_price_action.py` (the
data-driven fallback). The definitions below are written once and applied
the same way by both, so a chart-mode read and a script-mode read of the
same market should reach the same verdict. When they disagree, the
conservative-precedence rule (below) applies.

## Direction Convention

Fading a **CROWDED_LONG** market means seeking BEARISH reversal evidence
at or after UPSIDE extremes: watch highs, watch closes breaking below
prior lows, watch failed pushes above resistance. Fading a **CROWDED_SHORT**
market is the exact mirror: watch lows, watch closes breaking above prior
highs, watch failed pushes below support. Every rule below is stated for
CROWDED_LONG; swap high<->low and above<->below for CROWDED_SHORT.

All comparisons are **STRICT inequalities**. Equal-to-a-prior-extreme
never counts as a new extreme; a close exactly at a prior level never
counts as a reversal, breakout, or failure. This is deliberate: a market
that merely matches (not exceeds) a level has not actually generated new
evidence.

## Window Terminology

- **Swing-lookback weeks** (default 13): defines what counts as a "recent"
  high/low for the weekly key reversal trigger.
- **Extreme-lookback weeks** (default 52): defines what counts as a
  longer-horizon extreme, used by failed-extreme, failed-breakout, and the
  continuation veto, and as the confidence-HIGH bonus condition for weekly
  key reversal.
- **Signal-recency weeks** (default 4): a signal (a triggered check) older
  than this does not confirm. Only the FAILURE week counts as the signal
  for failed_breakout (see below), not the earlier breakout week.
- **Prior weeks strictly exclude the evaluation week itself** — "the prior
  N completed weeks" always means the N completed weeks immediately
  before the week being tested, never including it.
- **Window truncation is per-evaluated-week, not per-run.** When fewer
  completed weeks exist before an evaluated week than the configured
  window, the window truncates to whatever is available. Two different
  weeks within the same recency scan can have genuinely different amounts
  of prior history available (for example 26 vs. 29 weeks, right at the
  `min_weeks` floor) — the confidence-HIGH 52-week-extreme condition
  always reads the window size actually used by the ONE triggering week
  being reported, never any other week's value.
- `min_weeks` (default 30) is the hard floor: fewer completed weeks than
  this and the verdict is `INSUFFICIENT_DATA` (`insufficient_weekly_bars`)
  regardless of anything else.

## The Three Signal Checks

### 1. Weekly Key Reversal

The week's HIGH is a new swing-lookback high — STRICTLY greater than the
max high of the prior swing-lookback completed weeks — AND the week's
CLOSE is STRICTLY below the prior week's LOW.

Bullish mirror (CROWDED_SHORT): new swing-lookback LOW AND close STRICTLY
above the prior week's HIGH.

This is the only check that references TWO lookback windows: the
swing-lookback window drives the trigger itself, and the (larger)
extreme-lookback window is checked SEPARATELY, only to decide whether the
same new high/low also qualifies as an extreme of the full extreme-lookback
window — this second, stronger condition feeds the confidence-HIGH gate
below and never affects whether the check triggers at all.

### 2. Failed Extreme (intraweek poke-and-fail)

Within the signal-recency window, a week traded STRICTLY above the prior
extreme-lookback HIGH but CLOSED back BELOW that same prior high — the
market pushed into new territory intraweek and failed to hold it by the
close. Mirror for lows (CROWDED_SHORT).

Distinct from a key reversal: no requirement about the prior week's own
low/high, and it uses the extreme-lookback window, not the swing-lookback
window.

### 3. Failed Breakout (confirmed-then-rejected)

A weekly CLOSE above the prior extreme-lookback HIGH (a genuine CLOSING
breakout, not just an intraweek poke) at week B, followed within <=3
subsequent completed weeks by a weekly CLOSE back below that same
breakout level. Mirror down for CROWDED_SHORT.

**`week_of` on this check is the FAILURE week** (the close back through
the level), never the breakout week B itself — the breakout week only
appears inside the check's `detail` text. This matters for the
signal-recency window: only the FAILURE week needs to fall within
`signal_recency_weeks`; the breakout week B may be older. It also matters
for the continuation veto (below): because the breakout week is, by
construction, always strictly older than its own failure week, it can
never later be picked up as a "new closing extreme" that vetoes its own
signal (no self-veto).

Only the FIRST close back through the level after a given breakout counts
as that breakout's failure — a later close back through the same level is
not treated as a second, independent failure of the same breakout.

Worked example: breakout at week W, failure at week W+2, no later bars ->
CONFIRMED. Same breakout/failure, but a NEW closing high at week W+3
(within the recency window) -> NOT_CONFIRMED (`continuation_intact`), the
continuation veto fires.

## Continuation Veto

Independent of the three signal checks above: has the market set a new
CLOSING extreme in the crowd's direction (a new highest CLOSE for
CROWDED_LONG, relative to each evaluated week's own prior extreme-lookback
window of CLOSES — not intraweek highs) strictly more recently than the
newest triggered signal?

- If a signal triggered, the scan for a new closing extreme starts the
  week AFTER that signal's own `week_of` — so the signal week itself (and
  anything before it) can never self-veto.
- If NO signal triggered at all, the scan covers the full
  signal-recency window instead, so a market that just kept grinding to
  new highs with no reversal evidence anywhere gets the correct
  `continuation_intact` reason rather than the generic
  `no_reversal_evidence`.

## Swing Levels (fractal pivots, for the stop reference)

A **swing high** is a completed week whose HIGH is STRICTLY greater than
the highs of the 2 completed weeks on EACH side (a 5-week fractal). A
**swing low** mirrors on lows. `nearest` is the most recent such pivot
within the extreme-lookback window.

**Fallback**: if no fractal pivot exists anywhere in that window, fall
back to the max high (min low) of the (smaller) swing-lookback window
instead, flagged `fallback: true` so a consumer knows this is a weaker,
non-fractal substitute.

**`stop_reference`** follows the fade direction, not the crowd's
direction: fading a crowded LONG means going short, so the stop sits
ABOVE at the nearest swing HIGH; fading a crowded SHORT means going long,
so the stop sits BELOW at the nearest swing LOW.

## Verdict Synthesis (fail-closed)

1. Fewer than `min_weeks` completed weeks, or no usable price source ->
   `INSUFFICIENT_DATA` (`insufficient_weekly_bars` / `no_price_source`).
2. Continuation veto fired (a new closing extreme in the crowd's
   direction occurred after the newest signal, or with no signal at all
   within the recency window) -> `NOT_CONFIRMED` (`continuation_intact`).
   This ALWAYS wins over a triggered signal.
3. Otherwise, if any of the 3 signal checks triggered within the
   signal-recency window -> `CONFIRMED`, with `verdict_reason` naming
   whichever detector produced the newest triggered signal
   (`key_reversal` / `failed_extreme` / `failed_breakout`).
4. Otherwise -> `NOT_CONFIRMED` (`no_reversal_evidence`). Absence of
   evidence never confirms.

### Confidence

`HIGH` iff **either**:

- At least 2 DISTINCT detector types triggered within the recency window
  (the same detector firing does not count twice — this module only ever
  reports one, most-recent trigger per detector, so this is automatic);
  **or**
- The triggering `weekly_key_reversal`'s new high/low is ALSO an extreme
  of a FULL, untruncated (>=52-week) extreme-lookback window — i.e. its
  own `extreme_window_weeks_used >= 52` AND `is_full_window_extreme` is
  true.

Otherwise `MEDIUM`. `LOW` is reserved and never emitted in v1.

**A single-signal MEDIUM verdict is deliberately weak evidence.** One
weekly key reversal, one failed extreme, or one failed breakout, on its
own, is suggestive but not strong confirmation — treat a lone MEDIUM
signal as a reason to keep watching, not a reason to size up. The
`confidence` field is carried into the `handoff` block precisely so a
downstream consumer (`contrarian-setup-gate`, #241, not yet built) can
weigh single-signal evidence more cautiously than 2-signal or full-window
evidence.

## Output Contract (script mode; chart mode mirrors the same shape)

```yaml
symbol: BT
direction: CROWDED_LONG
mode: data # "chart" when Claude is reading a user-supplied chart image
verdict: CONFIRMED | NOT_CONFIRMED | INSUFFICIENT_DATA
confidence: HIGH | MEDIUM | LOW # LOW reserved, never emitted in v1
verdict_reason: key_reversal | failed_extreme | failed_breakout |
  continuation_intact | no_reversal_evidence |
  insufficient_weekly_bars | no_price_source | ...
checks:
  weekly_key_reversal:
    { triggered, week_of, swing_window_weeks_used,
      extreme_window_weeks_used, is_full_window_extreme, detail }
  failed_extreme: { triggered, attempted_level, week_of, window_weeks_used, detail }
  failed_breakout: { triggered, breakout_level, week_of, window_weeks_used, detail }
  continuation: { new_closing_extreme_with_crowd, week_of, window_weeks_used }
swing_levels:
  nearest_swing_high: { price, week_of, fallback }
  nearest_swing_low: { price, week_of, fallback }
  stop_reference: 0.0
weekly_bars_used: 52
last_completed_week: 2026-07-06
handoff: # consumed by contrarian-setup-gate (#241)
  price_action: { verdict, confidence, stop_reference, report_path }
run_context:
  {
    price_symbol,
    price_source,
    proxy_used,
    as_of,
    lookbacks,
    recency,
    min_weeks,
    detector_json,
    detector_age_days,
    schema_version,
  }
```

Output filenames: `ta_confirmation_<SYMBOL>_<as-of>.json` /
`ta_confirmation_<SYMBOL>_<as-of>.md`.

**Invariant: `checks` (and `swing_levels`) is `null` whenever `verdict:
INSUFFICIENT_DATA`** — a single, consistent shape regardless of the
specific reason (`no_price_source`, `insufficient_weekly_bars`, any
detector-json refusal reason, ...). This holds for every INSUFFICIENT_DATA
path, both the ones the CLI short-circuits on before ever fetching price
data and the one `run_weekly_price_action()` reaches after a successful
fetch but too little history (`n < min_weeks`). A downstream consumer
(`contrarian-setup-gate`, #241) can check `verdict` alone before deciding
whether `checks.*` is safe to read, without branching on
`verdict_reason` or which code path produced it — never a placeholder
dict of all-`false` checks.

## Chart-Mode Walkthrough

When a user supplies a weekly chart image and asks for a contrarian
confirmation read (rather than, or in addition to, running the script):

1. Confirm the crowd direction being faded (CROWDED_LONG / CROWDED_SHORT)
   — from the user, or from a prior `cot-contrarian-detector` /
   `news-reaction-failure-analyzer` result.
2. Visually scan the most recent `signal_recency_weeks` (default 4) weekly
   bars for each of the 3 signal patterns above, using the SAME strict
   definitions (a new swing-lookback extreme, a close through the prior
   week's opposite level, an intraweek poke that fails, a closing
   breakout that fails within 3 weeks).
3. Check whether the market has since printed a new CLOSING extreme in the
   crowd's direction more recently than any pattern found in step 2 (the
   continuation veto).
4. Identify the nearest fractal swing high/low for the stop reference.
5. Emit the SAME `mode: chart` YAML block as the script (§ above), filling
   `checks.*` from the visual read; `window_weeks_used` fields may be
   approximate (chart mode cannot count bars as precisely as the script)
   — note this explicitly in `detail` rather than fabricating a false
   precision.

## Conservative Disagreement Rule

If BOTH chart mode and script mode produce a result for the same
symbol/direction and their verdicts DISAGREE, the final verdict is
**`NOT_CONFIRMED`** with `verdict_reason: mode_disagreement`, and both
sub-results are attached for the user to review side by side — never
silently pick one mode over the other.

If one mode returns `INSUFFICIENT_DATA` and the other returns a clean
verdict (`CONFIRMED` or `NOT_CONFIRMED`), the clean verdict stands; note
the other mode's insufficiency rather than treating it as a disagreement.

## Guardrails

- **Verdict-only — never a trade recommendation on its own.** This
  confirms step 3 of 5. Entry (step 4) and exit (step 5) are still manual
  and still required, and position sizing belongs to `position-sizer` /
  `futures-position-sizer`, not this checklist.
- **`INSUFFICIENT_DATA` never advances the pipeline.** Fewer than
  `min_weeks` completed weeks, no usable price source, or a
  `--detector-json` that is unreadable (missing/can't be opened),
  syntactically invalid, structurally malformed, stale, future-dated, or
  carries a non-`CROWDED_*` classification all fail closed (reasons
  `detector_json_unreadable` / `detector_json_parse_error` /
  `malformed_detector_json` / `detector_json_stale` /
  `detector_future_data_date` / `not_crowded` respectively) — never a
  crash, never a bare non-zero exit with no report, never a forced call on
  inadequate data.
- **Weekly timeframe only.** This checklist is defined entirely in terms
  of completed ISO calendar weeks; it says nothing about daily or
  intraday price action.
- **The existing chart-analysis workflow is unchanged.** This mode only
  activates on an explicit contrarian-confirmation request (typically
  following `cot-contrarian-detector` and/or
  `news-reaction-failure-analyzer`); a plain "analyze this chart" request
  still runs the skill's original pure technical-analysis workflow.
- **A single-signal MEDIUM verdict is weak evidence** — see the
  Confidence section above. Do not treat it the same as a HIGH-confidence,
  2-signal or full-window-extreme confirmation.

### Referencia: references/technical_analysis_framework.md

# Technical Analysis Framework

This reference provides the methodology for conducting objective, chart-based technical analysis of weekly price charts.

## Core Principles

1. **Chart-Only Analysis**: Base all analysis purely on chart data. Ignore external news, fundamental data, and market sentiment.
2. **Objectivity**: Focus on observable patterns and data rather than subjective interpretations.
3. **Weekly Timeframe**: All analysis uses weekly charts for medium to long-term perspective.
4. **Probability-Based**: Express future scenarios as probabilities rather than certainties.

## 1. Trend Analysis

### Trend Classification

**Uptrend Criteria:**
- Higher highs (HH) and higher lows (HL) pattern
- Price trading above key moving averages
- Moving averages aligned in bullish order (shorter MA > longer MA)

**Downtrend Criteria:**
- Lower highs (LH) and lower lows (LL) pattern
- Price trading below key moving averages
- Moving averages aligned in bearish order (shorter MA < longer MA)

**Sideways/Range-bound:**
- No clear higher high/low or lower high/low pattern
- Price oscillating between defined support and resistance levels
- Moving averages flat or intertwined

### Trend Strength Assessment

**Strong Trend:**
- Clear, consecutive higher highs/lows (uptrend) or lower highs/lows (downtrend)
- Minimal retracements
- Volume confirming price direction

**Weak Trend:**
- Irregular higher/lower highs and lows
- Deep retracements (>50% of prior move)
- Divergence between price and volume

**Trend Exhaustion Signals:**
- Decreasing momentum on new highs/lows
- Volume declining as trend progresses
- Extended distance from moving averages
- Candlestick reversal patterns (e.g., shooting star, hammer, engulfing)

## 2. Support and Resistance Analysis

### Identifying Support Levels

Support represents price levels where buying interest has historically prevented further decline.

**Criteria for Valid Support:**
- Price has bounced from the level at least 2-3 times
- Volume spikes during bounces
- Longer timeframe support carries more weight
- Round numbers (psychological levels) often act as support

**Support Types:**
- **Horizontal Support**: Previous lows aligning at similar price levels
- **Trendline Support**: Upward-sloping line connecting higher lows
- **Moving Average Support**: Dynamic support from key MAs (e.g., 20-week, 50-week)

### Identifying Resistance Levels

Resistance represents price levels where selling interest has historically prevented further advance.

**Criteria for Valid Resistance:**
- Price has been rejected from the level at least 2-3 times
- Volume spikes during rejections
- Previous significant highs
- Round numbers often act as resistance

**Resistance Types:**
- **Horizontal Resistance**: Previous highs aligning at similar price levels
- **Trendline Resistance**: Downward-sloping line connecting lower highs
- **Moving Average Resistance**: Dynamic resistance from key MAs

### Support/Resistance Significance

**Strong S/R Levels:**
- Tested multiple times (3+ touches)
- Long-standing (months to years)
- High volume at previous touches
- Confluence with other technical factors (Fibonacci, round numbers, moving averages)

**Weak S/R Levels:**
- Only 1-2 touches
- Recent formation
- Low volume at touches

### Support-Resistance Flip

When broken, support often becomes resistance and vice versa. This "role reversal" is a key concept:
- **Broken Support → Resistance**: After downside break, previous support acts as new resistance on retests
- **Broken Resistance → Support**: After upside break, previous resistance acts as new support on pullbacks

## 3. Moving Average Analysis

### Key Moving Averages for Weekly Charts

- **20-week MA**: Short-term trend indicator (approximately 4 months)
- **50-week MA**: Medium-term trend indicator (approximately 1 year)
- **200-week MA**: Long-term trend indicator (approximately 4 years)

### Moving Average Interpretations

**Price Position Relative to MAs:**
- **Above all MAs**: Strong bullish structure
- **Below all MAs**: Strong bearish structure
- **Between MAs**: Transitional phase, trend unclear

**Moving Average Crossovers:**
- **Golden Cross**: 20-week MA crosses above 50-week MA (bullish signal)
- **Death Cross**: 20-week MA crosses below 50-week MA (bearish signal)

**Moving Average Slope:**
- **Rising MAs**: Bullish momentum
- **Falling MAs**: Bearish momentum
- **Flat MAs**: Consolidation, lack of directional momentum

**Moving Average as Support/Resistance:**
- In uptrends, MAs (especially 20-week and 50-week) often provide dynamic support
- In downtrends, MAs often provide dynamic resistance
- Repeated bounces or rejections from MA increase its significance

### Moving Average Confluence

When multiple MAs cluster together or align:
- **Bullish Alignment**: 20-week > 50-week > 200-week (all rising)
- **Bearish Alignment**: 20-week < 50-week < 200-week (all falling)
- **Compressed/Converging MAs**: Often precedes significant directional move

## 4. Volume Analysis

Volume confirms the strength or weakness of price movements.

### Volume Interpretation Principles

**Volume Confirms Price:**
- **Rising prices + Rising volume**: Healthy uptrend, strong buying
- **Falling prices + Rising volume**: Healthy downtrend, strong selling
- **Rising prices + Falling volume**: Weak uptrend, lack of conviction
- **Falling prices + Falling volume**: Weak downtrend, selling exhaustion possible

### Key Volume Patterns

**Volume Spikes:**
- **At Support**: High volume bounce suggests strong buying interest (bullish)
- **At Resistance**: High volume rejection suggests strong selling interest (bearish)
- **On Breakout**: High volume breakout validates the move
- **Low Volume Breakout**: Often leads to failed breakout (false signal)

**Volume Trends:**
- **Increasing Volume in Trend Direction**: Confirms trend strength
- **Decreasing Volume in Trend Direction**: Warns of potential trend exhaustion
- **Volume Climax**: Extremely high volume often marks trend extremes (capitulation or euphoria)

**Volume Divergence:**
- **Bullish Divergence**: Price making new lows but volume declining (selling exhaustion)
- **Bearish Divergence**: Price making new highs but volume declining (buying exhaustion)

## 5. Chart Patterns and Candlestick Analysis

### Reversal Patterns

**Bullish Reversal:**
- **Hammer**: Long lower wick, small body at top, appears at support
- **Bullish Engulfing**: Large green candle fully engulfing previous red candle
- **Morning Star**: Three-candle pattern (down, small, up)
- **Double/Triple Bottom**: Price tests support 2-3 times then reverses

**Bearish Reversal:**
- **Shooting Star**: Long upper wick, small body at bottom, appears at resistance
- **Bearish Engulfing**: Large red candle fully engulfing previous green candle
- **Evening Star**: Three-candle pattern (up, small, down)
- **Double/Triple Top**: Price tests resistance 2-3 times then reverses

### Continuation Patterns

**Bullish Continuation:**
- **Bull Flag**: Consolidation after strong move up, then breakout higher
- **Ascending Triangle**: Higher lows with flat resistance, breaks up

**Bearish Continuation:**
- **Bear Flag**: Consolidation after strong move down, then breakdown
- **Descending Triangle**: Lower highs with flat support, breaks down

### Pattern Significance

Patterns carry more weight when:
- Forming at key support/resistance levels
- Accompanied by appropriate volume (high on breakout)
- Confirmed by moving averages and trend structure
- Occurring on longer timeframes (weekly > daily)

## 6. Scenario Development and Probability Assignment

### Scenario Development Process

For each chart analysis, develop 2-4 potential scenarios:

1. **Base Case Scenario**: Most likely outcome based on current chart structure
2. **Bull Case Scenario**: Optimistic scenario if key resistance breaks
3. **Bear Case Scenario**: Pessimistic scenario if key support breaks
4. **Alternative Scenario** (optional): Lower probability but plausible outcome

### Probability Assignment Framework

Assign probabilities based on:

**High Probability (50-70%):**
- Scenario aligned with current trend
- Multiple confirming factors (trend, S/R, MA, volume)
- Recent price action supports scenario
- Clear invalidation level

**Medium Probability (25-45%):**
- Scenario requires trend change or major breakout
- Some supporting factors but not all
- Depends on key level holding/breaking

**Low Probability (5-20%):**
- Scenario contrary to most technical factors
- Requires significant shift in structure
- Limited supporting evidence but technically possible

### Probability Assignment Example

Current Structure: Uptrend, above all MAs, holding support

- **Bull Case (60%)**: Continuation higher after pullback to support
  - Reasoning: Trend intact, holding key support, volume confirming

- **Base Case (30%)**: Consolidation/range before next move
  - Reasoning: Approaching resistance, some profit-taking visible

- **Bear Case (10%)**: Break below support, trend reversal
  - Reasoning: No clear reversal signals yet, but always possible

**Note**: Probabilities should sum to 100%. Adjust based on strength of supporting factors.

### Invalidation Levels

For each scenario, define a specific price level that would invalidate it:
- **Bull Scenario Invalidation**: Break below key support
- **Bear Scenario Invalidation**: Break above key resistance
- **Base Case Invalidation**: Breakout from range in either direction

## 7. Analysis Structure and Discipline

### Analysis Checklist

For each chart, systematically evaluate:

1. ✓ **Current Trend**: Identify direction, strength, and duration
2. ✓ **Support Levels**: Mark significant horizontal and dynamic support
3. ✓ **Resistance Levels**: Mark significant horizontal and dynamic resistance
4. ✓ **Moving Averages**: Note position, slope, and crossovers
5. ✓ **Volume Pattern**: Assess if volume confirms or contradicts price
6. ✓ **Chart Patterns**: Identify any significant patterns forming or completing
7. ✓ **Scenarios**: Develop 2-4 scenarios with probability estimates
8. ✓ **Invalidation Levels**: Define what would negate each scenario

### Objectivity Reminders

- Avoid confirmation bias: Consider both bullish and bearish scenarios
- Let the chart speak: Don't force patterns or signals
- Update analysis as new data emerges: Charts are dynamic
- Admit uncertainty: Not every chart provides clear signals
- Focus on probabilities, not predictions: No scenario is 100% certain

### Common Pitfalls to Avoid

- **Overcomplicating**: Too many indicators can lead to analysis paralysis
- **Ignoring Volume**: Price without volume is incomplete picture
- **Forcing Patterns**: Seeing patterns that aren't clearly there
- **Disregarding Timeframe**: Weekly chart may differ from daily
- **Neglecting Context**: Each chart in isolation, but overall market matters
- **Being Too Certain**: Markets are probabilistic, not deterministic
