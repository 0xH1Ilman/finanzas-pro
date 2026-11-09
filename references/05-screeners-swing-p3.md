# 05-screeners-swing — parte 3

Skills de terceros agrupadas por tema. Cada sección indica fuente, licencia y dónde está su código.



---

## SKILL: us-undervalued-growth-screener

- Fuente: `tradermonty/claude-trading-skills` → `skills/us-undervalued-growth-screener` (MIT)
- Cuándo usarla: Autonomously screen NYSE, Nasdaq, and NYSE American operating-company stocks for undervalued-growth/GARP opportunities using forward same-basis valuation, driver-derived EPS/FCF forecasts, primary-source financial verification, SBC and dilution controls, sector and cycle normalization, auditable candidate-pool coverage, and fail-closed final reporting. Use when asked to find, screen, rank, or refresh US undervalued-growth stocks, including minimal requests with no ticker list or parameters.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/us-undervalued-growth-screener/` (annual-estimates.example.jsonl, broad-screen-audit.example.json, broad-screen-results.example.jsonl, broad-screen-shortlist.example.json, candidate-input.example.json, claude-code-config.example.json, discovery-audit.example.json, discovery-pool.example.jsonl, enriched-candidate-pool.example.jsonl, enrichment-queue.example.json, global-sources.example.json, listing-only-input.example.jsonl …)

# US Undervalued Growth Screener — v3.6 (Claude Code Direct-FMP)

## Overview

Run an end-to-end US undervalued-growth/GARP screen from a minimal request. Find companies whose EPS or FCF per share can compound enough to support attractive two- to three-year returns **without assuming multiple expansion**, while controlling for accounting basis, forecast construction, SBC, dilution, leverage, cyclicality, corporate actions, peer context, source freshness, and evidence quality.

**Claude Code is the preferred execution environment.** In Claude Code, run the local direct-FMP pipeline once. The Python process performs bulk retrieval, persistent caching, FY1 normalization, liquidity calculation, four-lane discovery, and deterministic broad screening while keeping raw FMP payloads on disk and out of the model context. Claude reads only the compact run summary and selected candidate packets, then completes SEC/IR underwriting and the existing strict evaluation sequence.

Treat a request such as **“use this skill to screen for undervalued-growth stocks” as complete**. Resolve defaults, collect current data, choose a viable acquisition path, checkpoint the work, repair obtainable blockers, and return the finished result in the same task. Never ask the user to supply a ticker list, API-plan details, output path, or a separate “continue” instruction unless the user explicitly narrows the scope.

**Deep-dive budget and lane coverage:** The bounded direct-FMP path defaults to `max_deep_dive_candidates: 3`. Three selected names cannot represent all four research lanes. The default lane targets are core GARP 2, high-growth exception 1, quality near miss 1, and cyclical normalization 1 (five slots total). A three-name run prioritizes candidates across lanes; it does not promise one name per lane. For a five-slot lane-first selection, set `max_deep_dive_candidates: 5` in a local copy of `assets/claude-code-config.example.json` and rerun the bounded pipeline with that config. Eligible candidates and diversification preferences still determine actual lane representation. The separate full-snapshot path requires `full_snapshot_deep_dive_candidates: 5`. See `references/claude-code-execution.md` for selection and budget-change details.

## Non-Negotiable Runtime Preflight

Before reading or reusing any prior run artifact, verify the installed runtime:

```bash
python3 skills/us-undervalued-growth-screener/scripts/run_pipeline.py --version
python3 skills/us-undervalued-growth-screener/scripts/screen_universe.py --version
python3 skills/us-undervalued-growth-screener/scripts/build_discovery_pool.py --version
python3 skills/us-undervalued-growth-screener/scripts/build_provider_prefilter_pool.py --version
python3 skills/us-undervalued-growth-screener/scripts/normalize_estimates.py --version
python3 skills/us-undervalued-growth-screener/scripts/manage_run_state.py --version
python3 skills/us-undervalued-growth-screener/scripts/evaluate_candidates.py --version
python3 skills/us-undervalued-growth-screener/scripts/prepublish_audit.py --version
python3 skills/us-undervalued-growth-screener/scripts/bundle_run_artifacts.py --version
```

Every command must report the same metadata:

```text
skill_version = 3.6.1
schema_version = 3
contract_revision = 3.5
runtime_fingerprint = ug-v3.6.1-claude-code-direct-fmp-20260830
```

Discard and regenerate any audit, checkpoint, or snapshot whose runtime metadata differs. Do not mix scripts, assets, or run artifacts from v3.1 through v3.5. A stale or cached same-name skill is a hard execution failure, not a warning.

## Autonomous Completion Contract

For a minimal request, perform all of the following without handing control back to the user:

1. Fix `analysis_as_of` and the latest completed US regular-session close.
2. Collect current market context with field-level source support and freshness checks.
3. In Claude Code, invoke `run_pipeline.py` instead of issuing bulk FMP MCP calls. Keep provider payloads on disk and expose only compact summaries to the model.
4. Audit the requested NYSE/Nasdaq/NYSE American listing universe through adaptive, exhausted market-cap bands when provider responses saturate.
5. Build a reproducible economic candidate pool. Do not require complete financial statements across the whole market.
6. Distinguish **enrichment attempted** from **enrichment resolved**.
7. Apply the deterministic broad-screen script. Do not replace its statuses with ad hoc LLM cutoffs.
8. Select up to three economically plausible deep-dive candidates in Claude Code through deterministic multi-lane sampling: core GARP, high-growth exceptions, quality near misses, and cyclicals requiring normalization. Apply a two-name sector cap when alternatives exist. Growth thresholds remain guidelines, not isolated hard gates.
9. Resolve every row in the chosen candidate pool or record sourced exhaustion evidence.
10. Perform corporate-action preflight and primary-source underwriting for every selected symbol.
11. Save every selected symbol as a verified candidate record, including `review_required`, `screened_out`, and `excluded` outcomes.
12. Assemble the schema-v3 / contract-v3.5 snapshot.
13. Run `evaluate_candidates.py --strict --require-final`.
14. Apply the final quality eligibility gate; route weak-cash-flow, low-ROIC, overleveraged, heavily dilutive, fragile-low-case, or severe-LOE names to `conditional` or `review_required`.
15. Run `prepublish_audit.py`; repair every obtainable blocker and rerun.
16. Run `bundle_run_artifacts.py` to produce a self-contained audit ZIP containing every referenced artifact.
17. Present a formal ranking and downloadable bundle only when all gates pass.

An exit code of `2` means **continue the same execution**: enrich the queue, verify the pool-generation audit, complete selected deep dives, or repair contract failures. It never means “ask the user to say continue.” After attaching the audit, run `manage_run_state.py next-action`; execute the returned action and every returned symbol. Never ask whether to process two versus five selected names. To change the budget, rerun the broad screen first so omitted names become `deferred_by_budget`.

## Completion Semantics

### Final ranking from an audited bounded pool

A reproducibly generated bounded pool may support a **scoped final ranking** when:

```text
candidate-pool generation audit is valid
candidate_pool_exhausted = true
all_rows_resolved = true
unresolved_count = 0
queue_count = 0
all selected symbols have verified candidate records
strict final evaluation passes
```

Label the conclusion scope, such as `stratified_discovery_pool` or `provider_prefilter`. Do not imply that unexamined market listings were economically screened.

### Market-wide “no qualifying candidates”

A market-wide no-candidates conclusion requires all of the above plus full in-scope economic coverage:

```text
conclusion_scope = full_listing_universe
candidate_pool covers every in-scope listing
in_scope_missing_count = 0
at least one row was economically assessable
selected_symbols = []
```

### Bounded-pool “no qualifying candidates”

A bounded pool may conclude only:

```text
no qualifying candidates in the audited bounded pool
```

It must not claim that the entire US small/mid-cap market has no qualifying company.

Read `references/autonomous-execution.md` before a live minimal-request run.

## When to Use

Use this skill to:

- Discover and rank US-listed undervalued-growth or GARP stocks.
- Screen operating-company common stocks on NYSE, Nasdaq, and NYSE American.
- Test whether EPS or FCF-per-share growth alone supports roughly 30%–50% upside over two to three years.
- Refresh a prior screen after earnings, guidance, filings, corporate actions, or estimate revisions.
- Compare candidates on forward valuation, growth durability, ROIC, standard FCF, SBC, dilution, peers, cycle risk, and sector-specific KPIs.

Do not use it for:

- A generic single-ticker report after a stock is already selected; use `us-stock-analysis`.
- Pure dividend, momentum, technical-pattern, pre-revenue biotechnology, or merger-arbitrage screening.
- Automatic order placement.

## Prerequisites

- Python 3.9 or later.
- `requests` for the generated direct-FMP client; deterministic evaluation and audit scripts otherwise use the standard library.
- `FMP_API_KEY` in the environment for Claude Code direct mode. Never commit or print the key.
- Current SEC, company-IR, and macro sources accessible for selected-company underwriting.
- Writable `reports/` and `.cache/` directories.
- No specific paid FMP plan is assumed. Bulk endpoint failures fall back to bounded per-symbol enrichment and are disclosed in diagnostics.

## Default Scope

Unless the user specifies otherwise:

- Exchanges: NYSE, Nasdaq, NYSE American.
- Security type: active operating-company common stock.
- Market-cap focus: USD 500 million–20 billion.
- Minimum price: USD 5.
- Preferred average daily dollar volume: USD 5 million; hard floor USD 1 million.
- Claude Code provider-prefilter pool: target 30 symbols after code-side economics and verified liquidity; bounded per-symbol fallback may inspect up to 80 names without loading their provider payloads into model context.
- Deep-dive budget: three symbols by default on the bounded Claude Code path, selected from four deterministic research lanes; three slots cannot represent all four lanes. Once selected, every symbol must be resolved; lower the budget only by rerunning the broad screen so omitted names become `deferred_by_budget`.
- Maximum ranked output: ten, though the verified deep-dive set may be smaller.
- Minimum formal constant-multiple upside: 30% over a supported two- or three-year horizon.
- Multiple-contraction stress: current forward multiple reduced by 20%.
- Minimum analysts for a rankable consensus horizon: three, unless a fully sourced independent forecast is constructed.

### Immutable request scope and bounded execution

For a minimal request, the user-requested market-cap scope is always USD 500M–20B. Never rewrite the run config so a convenient 3–4B band becomes the requested scope. Record `user_requested_scope` and `executed_scope` separately. A narrower executed scope is incomplete unless the user explicitly requested it; context or tool-budget pressure is not authorization. Stream listing pages/bands to JSONL rather than loading every row into the conversation context.

### Liquidity evidence

Never calculate ADDV from one session's volume. Candidate generation requires a provider average-dollar-volume measure or `price × average_volume` with an explicit averaging window of at least 20 trading days and source IDs. Rows lacking valid average-liquidity evidence remain `needs_enrichment` and cannot enter the discovery pool.

### Current forward horizon

A current P/E must be explicitly NTM or FY1 and must reconcile to a positive current forward EPS, price, fiscal-year/period metadata, estimate date, analyst count, and source IDs. Generic outer-year P/E values are invalid. A missing FY1/NTM row, a range crossing zero, or extreme forecast dispersion sends the name to enrichment or `unavailable_after_enrichment`; it must never appear as a low-P/E selection.

## Result-Quality Controls

### Deterministic multi-lane candidate discovery

Do not let one global score fill the research budget with a single style or sector. Allocate the default five deep dives across these lanes when qualifying names exist:

- two core GARP names,
- one high-growth exception with Forward P/E up to 30x,
- one quality near miss whose low valuation may compensate for sub-guideline headline growth,
- one cyclical candidate that requires an explicit mid-cycle model.

Backfill unused slots by deterministic priority and limit selections to two per sector when alternatives exist. Report each selected name's `selection_lane`. The LLM may explain these decisions but may not replace them with ad hoc cutoffs.

### Formal eligibility quality gate

A name that passes the upside test is not automatically `eligible`. Formal ranking also requires:

- final score at least 70,
- SBC-adjusted FCF yield at least 3% **or** EV/FCF at most 30x,
- ROIC at least 8%,
- Net Debt/EBITDA no more than 3.0x when applicable,
- diluted-share CAGR no more than 5%,
- at least 15% upside under a supported low-consensus case,
- no severe LOE tail loss worse than the configured threshold.

One or two ordinary failures may produce `conditional`; severe FCF or LOE failures and broader weakness produce `review_required`. Never label a low-P/E/high-EV-FCF transition story as a formal winner merely because average-consensus EPS implies 30% upside.

### Independent forecast-driver evidence

Every ranked year-2/year-3 bridge must use `construction_method=independent_driver_model`. Each revenue, margin, interest, tax, share-count, FCF, and adjustment driver needs an origin and source IDs. Mark any driver solved backwards from target EPS with `target_solved=true`; this fails the bridge. A residual adjustment that merely forces the model to consensus is not independent validation.

### Publish only self-contained results

The final report is not publishable until `prepublish_audit.py` verifies all referenced audit files, counts, hashes, scenario arithmetic, candidate statuses, final-three labels, and absence of unfinished-run language. Package the entire run directory with `bundle_run_artifacts.py`; a ZIP containing only Markdown/JSON summaries is incomplete.

## Data Acquisition Strategy

### Preferred Claude Code path — direct FMP, compact model context

Run one local command:

```bash
python3 skills/us-undervalued-growth-screener/scripts/run_pipeline.py \
  --config skills/us-undervalued-growth-screener/assets/claude-code-config.example.json \
  --output-dir reports/us-undervalued-growth-screener
```

The generated FMP client reuses the repository's central `scripts/fmp_client/` source-of-truth pattern. It writes raw responses and a persistent SQLite cache to disk. Do **not** paste or read the raw provider trees into the language-model context. Read only `run-summary.json`, `NEXT_ACTION.json`, `audit/broad-screen-audit.json`, and the compact packets under `candidate-packets/`.

For a market-wide run on a plan without bulk estimates, collect every frozen
universe shard first, then screen the verified snapshot:

```bash
python3 skills/us-undervalued-growth-screener/scripts/run_pipeline.py \
  --stage collect-estimates --shard-index 0 --shard-count 8 \
  --snapshot-dir .cache/us-garp/snapshot-current \
  --config skills/us-undervalued-growth-screener/assets/claude-code-config.example.json \
  --resume

python3 skills/us-undervalued-growth-screener/scripts/run_pipeline.py \
  --stage screen-full-snapshot \
  --snapshot-dir .cache/us-garp/snapshot-current \
  --config skills/us-undervalued-growth-screener/assets/claude-code-config.example.json \
  --output-dir reports/us-undervalued-growth-screener
```

Run each shard once without `--resume`; use `--resume` only to continue an
existing partial shard. Both collection and screening are current-only:
collection fixes the estimate-normalization basis, while screening adds exact
liquidity and TTM quality evidence. The first collection binds the exhausted
listing-enumeration audit into the snapshot manifest. Screening performs a
read-only content/freshness preflight before creating provider or run
artifacts, carries a digest binding the enumeration proof and every verified
shard into downstream audits, backfills liquidity failures until 50 valid
names or full eligible exhaustion, and commits five probed deep-dive names. Read
`references/full-universe-snapshot.md` for the full collection and screening
contract.

If the provider call budget is exhausted during screen enrichment, the command
exits 2 and writes `audit/partial-run-diagnostic.json` plus
`audit/enriched-estimates.partial.jsonl`. The diagnostic is the last atomic
commit marker and records the snapshot ID/digest, stage, deterministic
attempted/completed/pending/interrupted symbols, interrupted provider
operation, provider counters, and hashes for the partial artifacts. Read a
partial artifact only when that marker exists and its recorded hashes and row
counts verify; a missing or mismatched marker makes the partial output
non-authoritative. `screen-full-snapshot` has no `--resume`: rerun the same
verified snapshot after restoring the provider budget, allowing new cache/raw
records from successful calls and reusing existing cache/raw data without
deleting or rewriting it. A packet-stage budget failure also marks
`broad-screen-audit.json` incomplete/diagnostic, clears all nested selection
commitment fields, and rewrites **all** broad-screen rows (including rejected
rows) to `deferred_by_budget` with selection eligibility disabled. The original
`decision` is preserved in `prior_decision`, and original top-level selection
fields in `prior_selection`; these archives are audit-only, never selection
authority, and repeated invalidation retains the first archive. Neither the
audit nor any partial output is a final market-wide conclusion. Quality-probe
`calls_used` and `actual_eps_calls` count FMP provider-budget units: cached or
unsent calls cost zero, and consumed retry responses remain counted. Each retry uses a new empty run directory. The CLI adds a unique
attempt suffix and keeps raw responses in a sibling attempt directory, while
direct callers must not reuse a non-empty output directory.

The direct runner first attempts bulk ratios, key metrics, estimate, and EOD datasets. It falls back to bounded per-symbol enrichment only when bulk access is unavailable; a plan-gated (402/403) bulk endpoint is remembered in the cache for 30 days so later runs do not spend calls re-probing it. On the fallback path the estimate seed is a stratified sector × market-cap sample (√-weighted Hamilton quota, liquidity-ranked within cells, hash tie-break) whose size is derived from the remaining call budget; `audit/seed-audit.json` states the selection basis. Before pool selection, the top lane candidates receive a `key-metrics-ttm` quality probe (ROIC, FCF yield, EV/FCF, leverage, SBC) and a probe-resolved row with SBC-adjusted FCF yield below 1% cannot enter any lane except `high_growth_exception`. Exact 20-day ADDV work is prioritized by the four economic lanes, not by ticker order. Read `references/claude-code-execution.md` and `references/migration-v3.6-to-v3.6.1.md` for the full execution contract.

### Layer 1 — Listing-Universe Audit

Collect only fields suitable for broad coverage:

- symbol and exchange,
- active/common-stock status,
- price and quote timestamp,
- market capitalization,
- average daily dollar volume or enough data to calculate it,
- sector and industry when available.

Do not substitute a share-volume floor for an ADDV threshold. If an API can filter only by share volume, fetch broadly, calculate `price × average volume`, and apply the dollar-liquidity rule locally.

Target at least 95% listing-field completeness. Prove enumeration using provider totals and exhausted pagination or exhausted gap-free market-cap bands. Matching only the requested lower and upper market-cap endpoints is not proof of completeness.

### Layer 2 — Economic Candidate Pool

Choose the best route in this order:

1. Multi-lane provider prefilter built with `build_provider_prefilter_pool.py`. Retrieve broad rows separately for core GARP, P/E 21–30 high growth, low-P/E quality near misses, and cyclicals requiring normalization; union and audit the lanes instead of using one narrow `P/E≤20 + revenue≥8% + low-cycle` query.
2. Available estimates/fundamentals already attached to listing rows, then apply the same four-lane tags.
3. Stratified discovery fallback with `build_discovery_pool.py`, followed by enrichment.
4. User-supplied pool only when explicitly supplied.

For a bounded live run, target at least 30 resolved pool rows and at least three represented lanes unless the provider is demonstrably exhausted. A smaller convenience pool may be diagnostic but should not be described as a high-recall GARP search.

State the economic scope honestly. `run-summary.json` separates `listing_enumeration_complete` from `economic_screen_scope_complete` and reports `estimate_seed_coverage_pct` / `valid_estimate_coverage_pct`; on the bounded per-symbol fallback path the economic scope is never complete and the discovery audit records `provider_exhausted_scope: estimate_seed`. Describe such a result as "N seeded names evaluated with consensus estimates", never as a market-wide conclusion. Only `screen-full-snapshot` with a deeply verified full-universe classification and bound verification digest may emit `final_marketwide` on the per-symbol route.

Do not stop because a TTM or statement endpoint is plan-gated. Switch routes automatically.

#### Deterministic broad-screen rules

- Revenue growth, per-share growth, ROIC, leverage, and preferred valuation levels are guidelines, not isolated hard cutoffs.
- Store soft misses in `guideline_misses`.
- Use `screen_fail_reasons` only for severe disqualifiers such as non-positive standard FCF when required, negative ROIC, excessive leverage, extreme valuation unsupported by growth, or negative forward growth.
- Permit `near_miss_review` when valuation is attractive and per-share growth remains credible despite a soft revenue-growth miss.
- Permit P/E 21–30 high-growth exceptions when growth and evidence justify review.
- For cyclicality score 3–5, add `mid_cycle_normalization_required`; do not automatically reject the row.
- If `peak_profit_risk=true`, require normalization regardless of the numeric cyclicality score.
- Banks, insurers, REITs, BDCs, MLPs, and auto dealers remain blocked until sector-appropriate valuation or leverage evidence is available.
- Use the script-generated shortlist as authoritative. Do not remove GDDY-like near misses or KGS/AMKR-like cyclicals by applying an informal revenue-growth or cycle gate after the script runs.

### Layer 3 — Primary-Source Deep Dive

For selected symbols only, verify material facts with SEC filings and company IR. Vendors may supply discovery and consensus data, but primary sources must support actual revenue, cash flow, debt, shares, SBC, guidance, corporate actions, and accounting adjustments whenever available.

## Source and Evidence Rules

Use this hierarchy:

1. SEC filings.
2. Company IR.
3. Official macro/statistical sources.
4. Market-data and consensus vendors.
5. Reputable news and third-party transcripts as supplementary context only.
6. Analyst calculations and assumptions, explicitly labeled.

Every source requires:

```text
unique source ID
tier and kind
publication timestamp
retrieval timestamp
data_as_of when different
URL
non-empty supports[] array
```

Official-source labels must match official domains. A third-party transcript is never company IR. Dynamic market fields are tested against their underlying data date, not just retrieval time.

## Financial and Forecast Controls

### Standard FCF and TTM evidence

Use:

```text
standard FCF = operating cash flow − capex cash outflow
```

Capex is a positive cash outflow. Build TTM cash flow through one documented method:

- reported TTM,
- four discrete quarters, or
- latest FY + current YTD − prior-year YTD.

Every component period must have resolving source IDs. Do not double-count cumulative 10-Q cash-flow values.

### Cash classification

For ordinary operating companies, normalize reported cash and equivalents to `corporate_cash`; separately identify eligible marketable securities. For payments, custodial, marketplace, broker, or money-movement businesses, explicitly separate corporate cash from settlement/customer funds and restricted cash. Enterprise value and net debt use only shareholder-available cash.

### Driver-derived forecast bridge

Do not validate a forecast by dividing a numerator that was merely set equal to `EPS × shares`.

For EPS, independently reconstruct:

```text
forecast operating income = forecast revenue × forecast operating margin
forecast pretax income = operating income + net interest/other income
forecast GAAP net income = pretax income × (1 − tax rate)
forecast adjusted net income = GAAP net income + sourced after-tax adjustments
forecast EPS = forecast net income ÷ forecast diluted shares
```

For FCF per share, derive standard FCF from OCF and capex or a fully sourced revenue/FCF-margin model, then divide by forecast diluted shares.

The driver result must tie to the claimed metric within tolerance. Supplied numerator/denominator fields are cross-checks only. Adjusted periods must also tie the driver-derived GAAP metric and after-tax adjustments to the GAAP reconciliation.

### GAAP and adjusted metrics

Store the basis separately for current, year 2, and year 3. Mixed bases block the formal scenario. Recurrent “one-time” exclusions, SBC, acquisition costs, and intangible amortization must be described and reflected in quality/risk assessment.

### ROIC, EBITDA, and quality evidence

ROIC and EBITDA used in scoring or leverage calculations require source-linked inputs or a transparent analyst calculation. Missing evidence caps data quality and blocks an unsupported 100 score.

## Sector and Cycle Controls

### Commercial biopharma and royalty/drug-delivery platforms

Normalize aliases such as `biopharma`, `pharma`, `biotechnology`, `royalty_biopharma`, and `drug_delivery_platform` to `commercial_biopharma` when the company has commercial product/royalty exposure.

Require:

- product or royalty concentration,
- nearest material LOE/patent event,
- years to LOE,
- resolving source IDs,
- configured 6x and 8x LOE stress scenarios when material.

Missing structural-risk evidence produces `review_required` and a quality cap.

### Cyclicals and peak-profit risk

If cyclicality is 3–5 **or** `peak_profit_risk=true`, require a sourced normalization object with mid-cycle revenue/margin/EPS/FCF or a documented reason the current economics are sustainable. A risk flag without normalization is not enough for `eligible`.

## Workflow

### Step 1 — Run direct discovery in Claude Code

For Claude Code, start with the direct runner above. It creates the run directory, listing and candidate-pool audits, compact candidate packets, `run-summary.json`, and `NEXT_ACTION.json`. Follow `NEXT_ACTION.json` without asking the user for confirmation. The manual commands below remain the fallback for hosts that cannot execute direct HTTP code.

### Step 1B — Manual host fallback: create the run directory and live context

```text
reports/us-undervalued-growth-screener/<run-id>/
├── market-context.json
├── global-sources.json
├── universe.jsonl
├── discovery/
├── broad-screen/
├── run/
└── final/
```

Never copy values, URLs, dates, source IDs, or tickers from synthetic example assets into a live run.

### Step 2 — Build, normalize, and audit the candidate pool

Keep the original user-requested scope in the run contract. If bulk economics are unavailable, build a bounded discovery pool from the fully audited listing universe without narrowing the requested market-cap range. Every listing row used for pool generation must carry validated provider-average or 20+ trading-day liquidity evidence.

When provider screening is available, save one JSONL per lane and combine them deterministically:

```bash
python3 skills/us-undervalued-growth-screener/scripts/build_provider_prefilter_pool.py \
  --universe reports/us-undervalued-growth-screener/<run-id>/universe.jsonl \
  --lane core_garp=reports/us-undervalued-growth-screener/<run-id>/provider/core.jsonl \
  --lane high_growth_exception=reports/us-undervalued-growth-screener/<run-id>/provider/high-growth.jsonl \
  --lane quality_near_miss=reports/us-undervalued-growth-screener/<run-id>/provider/near-miss.jsonl \
  --lane cyclical_normalization=reports/us-undervalued-growth-screener/<run-id>/provider/cyclical.jsonl \
  --output-dir reports/us-undervalued-growth-screener/<run-id>/provider \
  --analysis-as-of <ISO-8601> \
  --source-id <provider-source-id> \
  --per-lane 15 --max-pool 60 --minimum-pool 30
```

Use the emitted `provider-prefilter-audit.json` as `--discovery-audit` and `provider-prefilter-pool.jsonl` as the candidate pool.

```bash
python3 skills/us-undervalued-growth-screener/scripts/build_discovery_pool.py \
  --input reports/us-undervalued-growth-screener/<run-id>/universe.jsonl \
  --output-dir reports/us-undervalued-growth-screener/<run-id>/discovery \
  --source-id <listing-source-id> \
  --min-market-cap 500000000 \
  --max-market-cap 20000000000 \
  --user-requested-min-market-cap 500000000 \
  --user-requested-max-market-cap 20000000000 \
  --max-pool 120 \
  --per-cell 3
```

Normalize dated annual consensus rows before Broad Screen. `--estimate-as-of` is mandatory. A company without a resolving NTM/FY1 row keeps its raw outer-year data only for diagnostics and becomes `unavailable` or remains in enrichment; it cannot receive a current Forward P/E.

```bash
python3 skills/us-undervalued-growth-screener/scripts/normalize_estimates.py \
  --estimates reports/us-undervalued-growth-screener/<run-id>/discovery/raw-annual-estimates.jsonl \
  --listing-input reports/us-undervalued-growth-screener/<run-id>/discovery/discovery-pool.jsonl \
  --analysis-as-of <ISO-8601> \
  --estimate-as-of <ISO-8601> \
  --source-id <estimate-source-id> \
  --output reports/us-undervalued-growth-screener/<run-id>/discovery/enriched-candidate-pool.jsonl
```

Merge the normalized estimate rows into the bounded pool, then run `screen_universe.py`. Supply explicit retrieval bounds and listing enumeration proof. Pass the generation audit with `--discovery-audit`.

```bash
python3 skills/us-undervalued-growth-screener/scripts/screen_universe.py \
  --input reports/us-undervalued-growth-screener/<run-id>/universe.jsonl \
  --candidate-pool reports/us-undervalued-growth-screener/<run-id>/discovery/enriched-candidate-pool.jsonl \
  --discovery-audit reports/us-undervalued-growth-screener/<run-id>/discovery/discovery-audit.json \
  --output-dir reports/us-undervalued-growth-screener/<run-id>/broad-screen \
  --analysis-as-of <ISO-8601> \
  --source-id <listing-source-id> \
  --candidate-source-id <estimate-source-id> \
  --candidate-generation-mode liquidity_stratified_estimates \
  --retrieval-min-market-cap 500000000 \
  --retrieval-max-market-cap 20000000000 \
  --user-requested-min-market-cap 500000000 \
  --user-requested-max-market-cap 20000000000 \
  --provider-reported-total <count> \
  --pages-fetched <count> \
  --pagination-exhausted \
  --config skills/us-undervalued-growth-screener/assets/screening-config.example.json \
  --max-deep-dives 5
```

If the command exits `2`, inspect `enrichment-queue.json` and `broad-screen-audit.json`, continue enrichment in the same task, and rerun. Pass `--candidate-pool-exhausted` only after every row is resolved and the generation audit proves the bounded scope.

### Step 3 — Checkpoint the run

Initialize and attach the screening audit:

```bash
python3 skills/us-undervalued-growth-screener/scripts/manage_run_state.py init \
  --run-dir reports/us-undervalued-growth-screener/<run-id>/run \
  --analysis-as-of <ISO-8601> \
  --price-as-of <ISO-8601> \
  --session regular_close \
  --price-source-id <source-id> \
  --market-context reports/us-undervalued-growth-screener/<run-id>/market-context.json \
  --global-sources reports/us-undervalued-growth-screener/<run-id>/global-sources.json \
  --base-commit <git-sha>

python3 skills/us-undervalued-growth-screener/scripts/manage_run_state.py set-screening-audit \
  --run-dir reports/us-undervalued-growth-screener/<run-id>/run \
  --audit reports/us-undervalued-growth-screener/<run-id>/broad-screen/broad-screen-audit.json \
  --universe-artifact reports/us-undervalued-growth-screener/<run-id>/broad-screen/universe-audit-results.jsonl \
  --candidate-artifact reports/us-undervalued-growth-screener/<run-id>/broad-screen/broad-screen-results.jsonl
```

### Step 4 — Complete selected deep dives

For every selected symbol:

1. Perform corporate-action preflight first.
2. Verify the latest quarter and full year separately.
3. Build standard FCF and TTM evidence.
4. Normalize cash classification.
5. Build same-basis current/year-2/year-3 valuation periods.
6. Construct the independent forecast bridge.
7. Reconcile adjusted metrics to GAAP.
8. Source ROIC, EBITDA, SBC, dilution, peers, and sector/cycle evidence.
9. Save the candidate as `verified`, even when the final candidate status will be `review_required`, `screened_out`, or `excluded`.

```bash
python3 skills/us-undervalued-growth-screener/scripts/manage_run_state.py save-candidate \
  --run-dir reports/us-undervalued-growth-screener/<run-id>/run \
  --candidate reports/us-undervalued-growth-screener/<run-id>/candidates/<SYMBOL>.json \
  --stage verified
```

### Step 5 — Complete and assemble

```bash
python3 skills/us-undervalued-growth-screener/scripts/manage_run_state.py set-status \
  --run-dir reports/us-undervalued-growth-screener/<run-id>/run \
  complete

python3 skills/us-undervalued-growth-screener/scripts/manage_run_state.py assemble \
  --run-dir reports/us-undervalued-growth-screener/<run-id>/run \
  --output reports/us-undervalued-growth-screener/<run-id>/final/final-snapshot.json
```

### Step 6 — Strict evaluation and repair loop

```bash
python3 skills/us-undervalued-growth-screener/scripts/evaluate_candidates.py \
  --input reports/us-undervalued-growth-screener/<run-id>/final/final-snapshot.json \
  --artifact-root reports/us-undervalued-growth-screener/<run-id> \
  --output-dir reports/us-undervalued-growth-screener/<run-id>/final \
  --language ja \
  --strict \
  --require-final
```

Do not present a formal result unless the exit code is `0` and the output contains:

```text
contract.valid = true
ranking_status = final
unprocessed_candidates = []
runtime.contract_revision = 3.5
```

### Step 7 — Prepublication audit and self-contained bundle

Locate the generated final JSON and Markdown, then run:

```bash
python3 skills/us-undervalued-growth-screener/scripts/prepublish_audit.py \
  --report-json reports/us-undervalued-growth-screener/<run-id>/final/<report>.json \
  --report-md reports/us-undervalued-growth-screener/<run-id>/final/<report>.md \
  --artifact-root reports/us-undervalued-growth-screener/<run-id> \
  --output reports/us-undervalued-growth-screener/<run-id>/final/prepublish-audit.json

python3 skills/us-undervalued-growth-screener/scripts/bundle_run_artifacts.py \
  --run-dir reports/us-undervalued-growth-screener/<run-id> \
  --report-json reports/us-undervalued-growth-screener/<run-id>/final/<report>.json \
  --report-md reports/us-undervalued-growth-screener/<run-id>/final/<report>.md \
  --output reports/us-undervalued-growth-screener/<run-id>/final/us-undervalued-growth-screen-<date>.zip
```

Both commands must exit `0`. Present the self-contained ZIP together with the report.

## Output Format

Generate both JSON and Markdown. The Markdown must include:

- runtime/version and conclusion scope,
- analysis and price timestamps,
- market context and source ledger,
- listing and candidate-pool audit/funnel,
- broad-screen selected, deferred, review, unavailable, screened-out, and excluded rows,
- formal ranking and score breakdown,
- explicit 2Y/3Y constant-multiple and 2Y/3Y 20%-contraction scenarios,
- candidate details, latest earnings, forecast bridge, GAAP reconciliation, peers, cycle/sector risks, catalysts, and invalidation conditions,
- final three only when ranking is final,
- unresolved data and global warnings.

Never combine a 2Y base case with a 3Y stress case in one unlabeled column.

## Resources

- `references/claude-code-execution.md` — direct-FMP execution, cache, compact-context, and handoff contract.
- `references/autonomous-execution.md` — same-turn execution, fallback, runtime, and completion contract.
- `references/data-contract.md` — schema-v3 / contract-v3.5 source, audit, candidate, and output contract.
- `references/methodology.md` and `methodology-ja.md` — financial and investment methodology.
- `references/research-checklist.md` — primary-source underwriting checklist.
- `references/scoring-rubric.md` — score, penalties, quality caps, and status gates.
- `references/sector-kpis.md` — sector valuation/KPI requirements.
- `references/output-template.md` — required JSON/Markdown presentation.
- `references/checkpointing.md` — atomic save/resume procedure.
- `references/review-regression-matrix.md` — observed failures and preventing tests.
- `references/migration-v3.5-to-v3.6.md` — Claude Code direct-FMP migration and operating changes.
- `references/migration-v3.4-to-v3.5.md` — prior breaking changes and upgrade steps.
- `scripts/skill_version.py` — canonical runtime/version constants.
- `scripts/fmp_client.py` — generated stable-first FMP client with SQLite cache and raw-artifact storage.
- `scripts/run_pipeline.py` — Claude Code-native direct-FMP discovery runner with compact stdout.
- `scripts/build_provider_prefilter_pool.py` — audited four-lane provider pool builder.
- `scripts/build_discovery_pool.py` — deterministic fallback pool generation with average-liquidity validation.
- `scripts/normalize_estimates.py` — identify and validate current NTM/FY1 consensus horizons.
- `scripts/screening_semantics.py` — shared fail-closed liquidity and forward-horizon semantics.
- `scripts/screen_universe.py` — listing audit and broad-screen engine.
- `scripts/manage_run_state.py` — checkpoint and final snapshot manager.
- `scripts/evaluate_candidates.py` — deterministic strict evaluator, quality eligibility gate, and report renderer.
- `scripts/prepublish_audit.py` — final artifact/count/scenario/prose audit.
- `scripts/bundle_run_artifacts.py` — deterministic self-contained audit bundle builder.

### Referencia: references/autonomous-execution.md

# Autonomous Execution Contract — v3.6 Runtime / Contract 3.5

## Purpose

Make a minimal instruction sufficient for a complete screen. The operator supplies the research request; the skill supplies defaults, current data acquisition, fallback routing, deterministic screening, primary-source underwriting, checkpointing, repair, and final reporting.

Never pause after an intermediate stage to ask for “continue.” Exit code `2` from a helper script is an internal continuation signal, not a user handoff.

In Claude Code, the mandatory default is the local direct-FMP runner. Do not consume the listing universe through repeated MCP calls. Run `run_pipeline.py`, keep raw payloads in its cache/artifact directories, and read only the compact summary, audits, and selected candidate packets.

## Runtime Identity

All run artifacts must contain the installed runtime metadata:

```json
{
  "skill_name": "us-undervalued-growth-screener",
  "skill_version": "3.6.1",
  "schema_version": 3,
  "contract_revision": "3.5",
  "runtime_fingerprint": "ug-v3.6.1-claude-code-direct-fmp-20260830"
}
```

Run every helper with `--version` before a live screen. Reject stale or mixed artifacts. This prevents a cached v3.1-v3.5 package from producing a seemingly valid contract-3.5 result.

## Request-Scope and Evidence Guardrails

- Preserve the default USD 500M–20B user request unless the user explicitly changes it.
- Never turn one convenient market-cap band into the requested scope. Stream exhausted pages/bands to disk or use a reproducible provider-prefilter grid across the entire requested range.
- Use only 20+ session average-dollar-liquidity evidence. Raw single-session volume is not ADDV.
- Run raw annual consensus rows through `normalize_estimates.py`; a current multiple must be NTM/FY1, dated, sourced, positive, and reconciled to price/EPS.
- Run `manage_run_state.py next-action` after each checkpoint and execute every returned symbol. The selected set is committed; changing its size requires rerunning the Broad Screen.

## Staged Coverage Model

### Listing coverage

Audit the complete requested listing universe for identity, active/common-stock status, quote, market cap, liquidity, sector, and exchange. This stage does not require full financial statements.

### Bounded economic pool

Generate a reproducible bounded pool by provider prefilter, available estimates, or stratified discovery. The generation audit must prove exactly how the pool was selected from the listing universe.

### Selected-name underwriting

Use SEC and company IR for the small selected set. Complete corporate-action, financial, forecast, peer, cycle, and sector evidence before ranking.

## Completion Invariants

A final ranking requires:

```text
valid runtime metadata
valid market context
valid listing-universe enumeration
valid candidate-pool generation audit
candidate pool exhausted
all candidate-pool rows resolved
queue empty
all selected symbols saved as verified candidate records
unprocessed_candidates empty
strict evaluator exit 0
```

A bounded pool can support a final **scoped ranking**. It cannot support a market-wide no-candidates claim unless every in-scope listing was economically covered.

## Attempted Is Not Resolved

`enrichment_attempted=true` records a query attempt or partial data receipt. A row becomes resolved only when it receives one of:

- `selected`
- `deferred_by_budget`
- `screened_out`
- `excluded`
- `unavailable_after_enrichment`

`unavailable_after_enrichment` requires a specific exhaustion reason and resolving source IDs.

## Deterministic Broad-Screen Authority

Always execute `screen_universe.py`. Preserve its decisions and requirements. The LLM may explain a decision but must not replace it with an informal gate.

Examples:

- Revenue growth below a guideline does not by itself remove a low-multiple, credible per-share grower.
- A cyclical candidate is routed to mid-cycle normalization, not automatically rejected.
- A high-growth 21–30x candidate may advance under the high-growth exception.
- Sector-specific rows remain review-blocked until the appropriate measure exists.


## Immutable Requested Scope

For a minimal request, retain the default USD 500M–20B request even when execution uses streaming, pagination, or a bounded discovery pool. Never rewrite the requested scope to a convenient band such as USD 3B–4B. A narrower executed scope requires explicit user authorization and must remain visibly separate from the original request.

## Liquidity and Forward-Horizon Gates

- ADDV requires provider-average evidence or price multiplied by an average-volume series covering at least 20 trading days. One-session volume is invalid.
- Current formal P/E requires NTM/FY1 metadata and a positive matching EPS. Distant outer-year estimates, missing intervening years, pre-operating names, zero-crossing ranges, or extreme dispersion cannot become the current multiple.
- Run raw annual estimates through `normalize_estimates.py` with an explicit estimate-as-of timestamp before deterministic screening.

## Selected-Set Commitment

The Broad Screen owns the selected set. Every committed selected symbol must be underwritten to a terminal verified record. The model cannot later ask whether to research two instead of three, or silently drop difficult names. Reduce the budget only by rerunning the deterministic Broad Screen and recording omitted names as `deferred_by_budget`.

A packet-stage provider-budget stop invalidates the entire broad-screen selection,
including rejected rows: every active decision becomes `deferred_by_budget`,
selection eligibility is disabled, and active lane/reason fields are removed.
The first original decision remains in `prior_decision`, with top-level selection
fields in `prior_selection`. These fields preserve the selected/rejected audit
trail only; they never authorize deep dives. Rerun in a new empty output directory
after restoring the budget.

## Provider Fallback Hierarchy

1. Use bulk listing and estimate/fundamental data when available.
2. Use a reproducible provider prefilter.
3. Build a stratified discovery pool and enrich it.
4. Use SEC/IR only for the selected set.

Do not stop because a premium endpoint is unavailable. Do not make an API-plan upgrade or CSV upload the primary user action.

## Candidate-Pool Scope

### Full-universe fundamentals

May support a market-wide final ranking or no-candidates conclusion when the full in-scope universe is economically covered and resolved.

### Provider prefilter or stratified discovery

May support a scoped final ranking after the bounded pool is audited, exhausted, and resolved. The report must state the bounded conclusion scope.

### User-supplied pool

May support only a user-supplied-pool conclusion unless the user explicitly claims broader coverage and supplies evidence.

## Tool-Budget Discipline

- Build a pool that can be completed.
- Limit deep dives to three by default for a minimal one-shot request; an explicit user override may raise the cap to five.
- Checkpoint after every selected candidate.
- Start selected deep dives while lower-priority enrichment continues when useful, but do not publish final until the pool is resolved.
- If tool budget becomes constrained, reduce the pool prospectively or resolve lower-priority rows as `deferred_by_budget`; never silently abandon them.

## Mandatory Repair Loop

After strict evaluation:

1. Read contract review reasons and candidate warnings.
2. Acquire missing obtainable evidence.
3. Correct source types, periods, cash classification, bridges, or funnel counts.
4. Rerun the deterministic evaluator.
5. Repeat until final or until a genuine unavailable condition is fully documented.

A genuine unavailable condition can lead to `review_required` or `unavailable_after_enrichment`; it does not justify invented numbers.

## Failure Behavior

When finality cannot be achieved, return a clearly labeled partial diagnostic, not a formal ranking. State the exact unresolved rows, selected candidate state, next internal action, and preserved artifact path. Do not invite the user to say “continue”; continue automatically when execution capacity remains.

## v3.5 Result-Quality and Publication Loop

1. Select through the deterministic multi-lane plan rather than a single global score.
2. Resolve every selected name and run the formal eligibility quality gate.
3. Permit `conditional` and `review_required`; do not lower quality floors to manufacture a ranked list.
4. Generate JSON and Markdown only after strict evaluation.
5. Run `prepublish_audit.py`. Exit code 2 is an internal repair instruction.
6. Run `bundle_run_artifacts.py` and present the self-contained ZIP.

The narrative layer must never announce completion before these steps finish. It must not contain “continue,” “next turn,” or similar handoff language in a final report.

### Provider-prefilter recall protection

Never use one narrow provider query as the whole economic pool. Retrieve and save four separate lanes—core GARP, high-growth exception, quality near miss, and cyclical normalization—then combine them with `build_provider_prefilter_pool.py`. This avoids systematically dropping GDDY-like low-headline-growth compounders, KGS-like high-growth exceptions, and AMKR-like cyclicals before primary-source review.

### Referencia: references/checkpointing.md

# Checkpoint and Completion Guide — Contract v3.5

## Purpose

Preserve every stage of a long screen, make resumption deterministic, and prevent selected candidates or unresolved pool rows from disappearing.

## Layout

```text
run/
├── run_state.json
├── screening_audit.json
├── screening_funnel.json
├── market_context.json
├── global_sources.json
├── universe_artifact.jsonl
├── candidate_pool_artifact.jsonl
├── candidates/
│   ├── SYMBOL.draft.json
│   └── SYMBOL.verified.json
└── final-snapshot.json
```

Write state atomically. Every state and audit carries v3.5 runtime metadata.

## Initialize

Use `manage_run_state.py init` with live market context, source ledger, price basis, and optional base repository commit.

## Attach the Audit

Use `attach-audit` only with a contract-3.5 audit whose runtime fingerprint matches the installed skill. The manager independently hashes the listing and candidate artifacts and checks their row counts and decisions.

## Save Every Selected Candidate

For each selected symbol, save a draft early and replace it with a verified record after primary-source review. A selected company that becomes an M&A exclusion still receives a verified `excluded` candidate record.

## Funnel Counts

Maintain:

```text
universe_count
listing_in_scope_count
candidate_pool_count
discovery_evaluable_count
deep_dive_selected_count
preflight_passed_count
deep_dive_completed_count
```

`preflight_passed_count` and `deep_dive_completed_count` refer only to selected symbols. The evaluator independently recomputes both counts.

## Completion Gate

The manager enforces:

```text
unprocessed_candidates = selected_symbols − verified_candidate_symbols
```

It refuses `complete` when:

- the pool is unresolved or not exhausted,
- the queue is nonempty,
- generation audit/runtime evidence is invalid,
- any selected symbol lacks a verified record,
- funnel counts are inconsistent.

## Assemble and Evaluate

Assemble only from the attached audit, live source ledger, current context, and verified candidates. Then run:

```bash
python3 skills/us-undervalued-growth-screener/scripts/evaluate_candidates.py \
  --input <final-snapshot.json> \
  --artifact-root <run-root> \
  --output-dir <final-dir> \
  --strict --require-final --language ja
```

## Resume

On resume:

1. verify installed runtime with `--version`;
2. inspect `run_state.json` runtime metadata;
3. reject stale contract revisions/fingerprints;
4. inspect selected, verified, unprocessed, and enrichment queue states;
5. continue from the earliest incomplete stage.

## v3.5 Publication Checkpoint

After strict evaluation, store the generated report JSON/Markdown under the run directory, run the prepublication audit, then build the complete ZIP. A run is operationally complete only when:

```text
strict evaluator exit = 0
prepublish audit exit = 0
bundle builder exit = 0
bundle manifest contains every referenced artifact
```

Do not delete intermediate audit or candidate files before bundling.

### Referencia: references/claude-code-execution.md

# Claude Code Direct-FMP Execution — v3.6

## Purpose

The v3.6 path prevents bulk FMP responses from consuming the language-model context. Claude Code launches one local Python process. Python performs provider retrieval, persistent caching, listing enumeration, FY1 normalization, liquidity calculation, four-lane discovery, and deterministic broad screening. Claude reads only the compact summary and selected-company evidence packets.

The underwriting and final-ranking contract remains schema 3 / contract 3.5.

## Required environment

```bash
export FMP_API_KEY="..."
```

Never commit or print the key. Cache identities and raw-artifact metadata remove `apikey` and `api_key` fields.

The direct client requires `requests`; SQLite is provided by Python's standard library.

## Standard command

```bash
python3 skills/us-undervalued-growth-screener/scripts/run_pipeline.py \
  --config skills/us-undervalued-growth-screener/assets/claude-code-config.example.json \
  --output-dir reports/us-undervalued-growth-screener
```

The program prints one compact JSON object, normally below 20 KB. It does not print provider payloads.

## Reused repository components

- Repository-level generated FMP-client registry and vendoring pattern.
- Stable-first / legacy-v3 fallback, request pacing, retry, circuit breaking, and call-budget conventions.
- `normalize_estimates.py` for dated FY1/FY2/FY3 normalization.
- `build_provider_prefilter_pool.py` for four-lane candidate-pool construction.
- `screen_universe.py` for deterministic broad-screen decisions and deep-dive commitment.
- Existing checkpoint, evaluation, prepublication-audit, and bundle scripts.

## Retrieval strategy

1. Enumerate NASDAQ, NYSE, and AMEX with the company screener.
2. If a response reaches the configured limit, recursively split the market-cap band. A listing enumeration is complete only when all leaf bands are unsaturated.
3. Attempt bulk ratios, key metrics, income-statement growth, annual analyst estimates, and daily EOD datasets.
4. If bulk annual estimates cover enough symbols, normalize all covered listings. Otherwise choose a deterministic sector × market-cap seed and use per-symbol estimate calls.
5. Prefer bulk 20-day EOD volume. If unavailable, rank exact-liquidity work by the four economic lanes and fetch per-symbol history only for the bounded target set.
6. Build core GARP, high-growth exception, quality near-miss, and cyclical-normalization lanes.
7. Produce a 12–30 name audited provider-prefilter pool and select up to three deep-dive names.
8. Fetch candidate-level FMP data once. Store full payloads under `provider/candidate-data/`; write compact projected packets under `candidate-packets/`.

Bulk endpoint names remain configuration-driven because availability varies by FMP plan. A missing bulk endpoint is a fallback condition, not permission to invent data.

## Context discipline

Claude may read:

```text
run-summary.json
NEXT_ACTION.json
audit/listing-enumeration-audit.json
audit/provider-prefilter-audit.json
audit/broad-screen-audit.json
audit/partial-run-diagnostic.json
audit/enriched-estimates.partial.jsonl
candidate-packets/*.fmp-packet.json
```

The CLI stores provider raw responses in a sibling, attempt-specific
`.provider-raw/<run-id>/` directory so creating the FMP client cannot make a
new run directory look stale. An explicitly supplied raw-store path must also
remain outside the screen run directory.

`audit/partial-run-diagnostic.json` is a commit marker for a budget-exhausted
`screen-full-snapshot` attempt. Read the partial JSONL, summary, or preserved
artifacts only after verifying the marker's recorded SHA-256 values and row
counts. A missing or mismatched marker means the preceding files are not
authoritative. Screening has no `--resume`; rerun the same verified snapshot
into a new empty run directory after the provider budget is restored. The
snapshot is read-only. Existing
cache/raw records are not deleted or rewritten, while successful calls may add
new records and a later rerun may reuse them.

Claude must not load the raw provider-response tree into context. Open a raw file only to resolve a specific named mismatch. Provider packets remain secondary evidence; SEC/IR verification is mandatory for formal underwriting.

## Persistent cache

The generated client uses SQLite. Default TTLs are:

| Dataset | TTL |
|---|---:|
| Quotes | 1 hour |
| Listing universe | 7 days |
| Analyst estimates | 3 days |
| Statements / ratios / metrics | 7 days |
| Historical prices | 1 day |

The first run may issue many HTTP requests inside one Python invocation. Later runs reuse the cache and primarily refresh prices, estimates, and selected-company data.

## Key artifacts

```text
<run>/run-summary.json
<run>/NEXT_ACTION.json
<run>/audit/listing-enumeration-audit.json
<run>/audit/universe.jsonl
<run>/audit/enriched-estimates.jsonl
<run>/audit/provider-prefilter-pool.jsonl
<run>/audit/provider-prefilter-audit.json
<run>/audit/broad-screen-results.jsonl
<run>/audit/broad-screen-audit.json
<run>/audit/partial-run-diagnostic.json   # only for budget-exhausted screen attempts
<run>/audit/enriched-estimates.partial.jsonl
<run>/candidate-packets/<SYMBOL>.fmp-packet.json
<run>/provider/candidate-data/<SYMBOL>/*.json
```

## Handoff to underwriting

`run_pipeline.py` stops at `ready_for_underwriting` when selected symbols exist. Claude must then:

1. perform corporate-action preflight;
2. verify current quarter and full year separately using SEC/IR;
3. reconstruct standard FCF with primary-source period evidence;
4. build same-basis valuation periods and an independent forecast bridge;
5. verify SBC, dilution, ROIC, leverage, peers, and cycle/sector evidence;
6. save all selected symbols, regardless of final status;
7. run strict evaluation, prepublication audit, and bundling.

A helper exit code 2 is an internal continuation signal. It is not a reason to ask the user for another turn.

## Deep-dive budget versus lane coverage

The bounded direct-FMP example config keeps `max_deep_dive_candidates: 3` to limit downstream underwriting work. This is a total candidate limit, not a promise of coverage across all four research lanes. The default lane targets are core GARP 2, high-growth exception 1, quality near miss 1, and cyclical normalization 1: five slots in total.

When the limit is below that total, the first selection pass walks candidates in priority order and applies each lane target as a cap. With a limit of three, at least one lane must be absent. At a limit of five or more, the first pass fills lane targets in lane order. In either case, later passes fill unused slots by priority without lane caps; the final pass can relax the sector preference if it would otherwise leave slots unused. Targets and the two-name sector preference therefore do not guarantee the final lane counts or sector counts. Only eligible candidates can be selected.

To allow the five-slot plan on the bounded path, copy `assets/claude-code-config.example.json` to your run configuration, set `max_deep_dive_candidates` to `5`, and pass that copy to `run_pipeline.py --config`. This allows more underwriting work but does not guarantee that every lane has an eligible selected name. Rerun the broad screen through the pipeline to establish the new selected set; when reducing the limit, omitted eligible names must become `deferred_by_budget`. Do not simply stop underwriting part of an already committed set: every selected symbol must be resolved.

The full-snapshot path uses the separate `full_snapshot_deep_dive_candidates` setting and requires it to equal `5`. Changing the bounded-path limit does not change that requirement. Neither a three-name nor a five-name deep-dive set alone establishes market-wide economic coverage; that depends on the full-snapshot verification contract.

### Referencia: references/data-contract.md

# Schema-v3 / Screening-Audit-v3.5 Data Contract

## Contract Versions

```text
Top-level snapshot schema_version: 3
Screening audit audit_schema_version: 3
Screening audit contract_revision: 3.5
```

Snapshot schema 3 retains the accounting, source, forecast, and candidate structure introduced in v3.0. Screening contract 3.5 hardens immutable requested scope, average-liquidity evidence, current NTM/FY1 normalization, selected-set commitments, universe enumeration, enrichment resolution, completion, source freshness, and report-disposition rules.


## v3.5 Discovery Evidence Contract

### User-request scope versus executed scope

The default user request remains USD 500 million–20 billion unless the user explicitly changes it. Store both:

```json
{
  "user_requested_scope": {
    "min_market_cap": 500000000,
    "max_market_cap": 20000000000,
    "source": "skill_default | explicit_user_request"
  },
  "executed_scope": {
    "min_market_cap": 500000000,
    "max_market_cap": 20000000000
  },
  "scope_reduced": false,
  "scope_override_authorized": false,
  "user_scope_evidence": null
}
```

Internal context or tool-budget pressure never authorizes a narrower market-cap request. Use a cross-range provider prefilter or stream exhausted bands to disk. A single convenient band is incomplete unless the user explicitly requested that band.

### Average daily dollar volume

A row is valid for discovery only when it provides an allowed averaging method, a window of at least 20 sessions, and resolving source IDs. Raw one-session `volume` is never interpreted as average volume.

```json
{
  "average_daily_dollar_volume": 12000000,
  "average_daily_dollar_volume_method": "provider_average_dollar_volume",
  "average_volume_period_days": 20,
  "liquidity_source_ids": ["quote-source"]
}
```

### Current forward metric

`forward_pe` alone is invalid. Current valuation must identify NTM or FY1 and reconcile to price and a positive current forward EPS:

```json
{
  "forward_pe_period": "FY1",
  "forward_fiscal_year": "FY2027",
  "forward_period_end": "2027-06-30",
  "forward_eps": 3.25,
  "forward_pe": 15.4,
  "forward_estimate_as_of": "2026-08-28T12:00:00Z",
  "forward_estimate_source_ids": ["consensus-source"],
  "forward_metric_origin": "computed_from_price_and_fy1_eps",
  "analyst_count": 6
}
```

Outer-year substitutions, pre-operating companies, a forecast range crossing zero, excessive dispersion, stale estimates, or non-contiguous annual rows cannot become current Forward P/E inputs. Use `normalize_estimates.py` to produce this structure from raw dated annual estimates.

### Committed selected set

The broad-screen audit commits the selected set with a SHA-256 payload. Every selected symbol must receive a verified candidate record. Reducing the deep-dive count requires a fresh deterministic broad-screen run; narrative-stage discretion cannot drop an already selected name.

## Top-Level Snapshot

```json
{
  "schema_version": 3,
  "runtime": {
    "skill_name": "us-undervalued-growth-screener",
    "skill_version": "3.6.1",
    "schema_version": 3,
    "contract_revision": "3.5",
    "runtime_fingerprint": "ug-v3.6.1-claude-code-direct-fmp-20260830"
  },
  "analysis_as_of": "ISO-8601 with timezone",
  "run_metadata": {
    "run_id": "string",
    "status": "partial | complete",
    "base_repository_commit": "optional SHA",
    "selected_symbols": [],
    "unprocessed_candidates": []
  },
  "price_basis": {
    "as_of": "ISO-8601 with timezone",
    "session": "regular_close | pre_market | after_hours | intraday",
    "timezone": "America/New_York",
    "source_id": "source-id"
  },
  "config": {},
  "market_context": {},
  "screening_funnel": {},
  "global_sources": [],
  "screening_audit": {},
  "candidates": []
}
```

All timestamps must be at or before `analysis_as_of` unless a field explicitly represents a future fiscal period.

## Source Ledger

```json
{
  "id": "unique-id",
  "tier": 1,
  "kind": "sec_filing",
  "title": "Form 10-Q",
  "published_at": "2026-08-10T16:05:00-04:00",
  "data_as_of": "2026-06-30T00:00:00-04:00",
  "retrieved_at": "2026-08-22T10:05:00-07:00",
  "url": "https://...",
  "supports": ["latest_earnings.quarter", "financials.cash_flow_ttm"]
}
```

`supports` is always a non-empty string array. `data_as_of` is optional but preferred for dynamic fields whose data date differs from publication time. Retrieval time never makes old data current.

| Kind | Usual tier |
|---|---:|
| `sec_filing` | 1 |
| `official_macro`, `official_statistics` | 1 |
| `company_ir` | 2 |
| `exchange_status` | 2 or 3 |
| `market_data`, `consensus`, `news`, `third_party_transcript` | 3 |
| `analyst_calculation`, `analyst_assumption`, `local_artifact` | 4 |

A third-party transcript is never `company_ir`.

## Market Context

Required fields:

```json
{
  "summary": "non-placeholder narrative",
  "as_of": "ISO-8601",
  "policy_rate_pct": 3.625,
  "treasury_10y_yield_pct": 4.74,
  "real_gdp_growth_pct": 1.5,
  "inflation_yoy_pct": 3.4,
  "market_forward_pe": 21.2,
  "small_mid_cap_valuation_context": "current context",
  "sector_cycle_notes": [],
  "source_ids": [],
  "inferences": []
}
```

Field-level evidence and default maximum ages:

| Field | Default max age | Source rule |
|---|---:|---|
| Policy rate | 60 days | official macro/statistics |
| 10-year Treasury | 7 days | official macro/statistics |
| Inflation | 45 days | official statistics |
| GDP | 120 days | official statistics |
| Market forward P/E | 14 days | current market-data/research source |
| Small/mid-cap context | 14 days | current market-data/research source |

Market-rate expectation language such as “markets price hikes/cuts” requires a source supporting `market_context.market_rate_expectations` or an `analyst_inference` object with resolving source IDs.

## Layered Screening Audit

```json
{
  "audit_schema_version": 3,
  "contract_revision": "3.5",
  "runtime": {
    "skill_name": "us-undervalued-growth-screener",
    "skill_version": "3.6.1",
    "schema_version": 3,
    "contract_revision": "3.5",
    "runtime_fingerprint": "ug-v3.6.1-claude-code-direct-fmp-20260830"
  },
  "conclusion_scope": "full_listing_universe | provider_prefilter | stratified_discovery_pool | bounded_available_fundamentals | user_supplied",
  "generated_at": "ISO-8601",
  "analysis_as_of": "ISO-8601",
  "candidate_generation_mode": "liquidity_stratified_estimates",
  "candidate_pool_status": "sufficient | sufficient_pending_enrichment | no_qualifying_candidates | no_qualifying_candidates_in_bounded_pool | insufficient_data",
  "selection_outcome": "selected | selected_pending_enrichment | no_candidates | no_candidates_in_bounded_pool | insufficient_data",
  "selected_symbols": ["AAA"],
  "filters": {},
  "source_ids": ["listing-source", "estimate-source"],
  "scope": {
    "requested_min_market_cap": 500000000,
    "requested_max_market_cap": 20000000000,
    "retrieval_min_market_cap": 500000000,
    "retrieval_max_market_cap": 20000000000,
    "retrieval_scope_explicit": true,
    "scope_override_authorized": false,
    "scope_complete": true,
    "reasons": [],
    "enumeration": {
      "verified": true,
      "provider_reported_total": 1786,
      "rows_fetched": 1786,
      "pages_fetched": 18,
      "pagination_exhausted": true,
      "band_audit": [],
      "bands_verified": false
    }
  },
  "universe": {
    "row_count": 1786,
    "in_scope_count": 1600,
    "listing_data_complete_count": 1770,
    "listing_data_complete_pct": 99.1,
    "decision_counts": {},
    "artifact_path": "audit/universe-audit-results.jsonl",
    "artifact_sha256": "64-character SHA-256"
  },
  "candidate_pool": {
    "row_count": 120,
    "discovery_evaluable_count": 40,
    "selection_eligible_count": 8,
    "selected_count": 5,
    "in_scope_covered_count": 120,
    "in_scope_missing_count": 1480,
    "in_scope_missing_symbols": ["..."],
    "coverage_complete": true,
    "coverage_scope": "stratified_discovery_pool",
    "listing_coverage_complete": false,
    "generation_audit": {
      "audit_schema_version": 2,
      "runtime": {},
      "selection_method": "sector_market_cap_stratified",
      "input_row_count": 1786,
      "selected_count": 120,
      "selected_symbols": [],
      "source_ids": [],
      "artifact_path": "discovery/discovery-pool.jsonl",
      "artifact_sha256": "64-character SHA-256",
      "valid": true
    },
    "fundamental_complete_count": 12,
    "decision_counts": {},
    "symbols_not_in_universe": [],
    "artifact_path": "audit/broad-screen-results.jsonl",
    "artifact_sha256": "64-character SHA-256"
  },
  "enrichment": {
    "status": "pending | complete",
    "next_action": "build_discovery_pool | enrich_queue | expand_candidate_pool | verify_candidate_pool_exhaustion | proceed_to_deep_dive | publish_no_candidates",
    "discovery_pool_required": false,
    "attempted_count": 120,
    "resolved_count": 118,
    "unresolved_count": 2,
    "resolution_pct": 98.3333,
    "all_rows_resolved": false,
    "maximum_attempts": 120,
    "candidate_pool_exhaustion_declared": false,
    "candidate_pool_exhausted": false,
    "candidate_pool_covers_in_scope": false,
    "queue_count": 2,
    "queue_symbols": ["BBB", "CCC"],
    "artifact_path": "enrichment-queue.json",
    "artifact_sha256": "64-character SHA-256"
  }
}
```

## Scope and Enumeration

`scope_complete=true` requires all of:

```text
retrieval_scope_explicit = true
retrieval bounds cover requested bounds
enumeration.verified = true
```

Enumeration is verified when:

- pagination is exhausted and any provider-reported total is consistent with fetched rows, or
- every row in `band_audit` has valid lower/upper bounds, a nonnegative row count, and `provider_exhausted=true`, and the ordered bands cover the complete requested market-cap range without gaps.

A matching lower/upper market-cap bound alone is insufficient. `bands_verified=true` is derived from the band evidence; it is not accepted as self-attestation.


## Requested Scope, Executed Scope, and Authorization

Keep the user's request separate from the data slice actually executed:

```json
{
  "user_requested_scope": {
    "min_market_cap": 500000000,
    "max_market_cap": 20000000000,
    "source": "default_contract | explicit_user_request"
  },
  "executed_scope": {
    "min_market_cap": 500000000,
    "max_market_cap": 20000000000,
    "reduction_authorized": false,
    "authorization_source": null
  }
}
```

A tool/context budget is not authorization to replace the default USD 500M–20B request with a USD 3B–4B request. Stream pages or market-cap bands to disk. A narrower execution may be published only as an explicitly user-authorized scoped run; otherwise the contract remains partial.

## Listing Liquidity Evidence

A listing or discovery row may satisfy ADDV only with a provider-average dollar-volume value or `price × average_volume`, where the averaging window is at least 20 trading days:

```json
{
  "average_daily_dollar_volume": 12500000,
  "average_daily_dollar_volume_method": "provider_average_dollar_volume | price_times_average_volume",
  "average_volume_period_days": 20,
  "liquidity_source_ids": ["quote-history-source"]
}
```

Single-session volume, an unlabeled `volume` field, or a share-volume floor cannot populate ADDV.

## Current Forward Estimate Normalization

The formal current multiple must use a resolving NTM or FY1 period:

```json
{
  "forward_pe": 14.2,
  "forward_eps": 3.10,
  "forward_pe_period": "NTM | FY1",
  "forward_period_end": "2027-06-30",
  "forward_fiscal_year": "FY2027",
  "forward_estimate_as_of": "2026-08-28T00:00:00-04:00",
  "forward_estimate_source_ids": ["consensus-source"],
  "forward_estimate_analyst_count": 6,
  "estimate_normalization_status": "valid"
}
```

For FY1, the period must be the nearest supported fiscal year after `analysis_as_of` and within the configured horizon. A missing FY1/NTM row, pre-operating status, a forecast range crossing zero, extreme dispersion, or noncontiguous outer-year-only estimates produces `estimate_normalization_status="unavailable"`. Canonical `forward_pe` and `forward_eps` are then null; raw outer-year values may be retained only under `raw_forward_candidate` for diagnostics.

## Selected-Set Commitment

The deterministic Broad Screen commits its selected symbols and budget:

```json
{
  "selected_symbols": ["AAA", "BBB"],
  "selected_set_sha256": "64-character SHA-256",
  "max_deep_dive_candidates": 3
}
```

Every committed selected symbol must reach a verified terminal candidate record. The model cannot later process only a preferred subset. To change the budget or selected set, rerun the deterministic Broad Screen so omitted names become `deferred_by_budget`.

## Universe Artifact

`universe-audit-results.jsonl` has one row per listing-universe symbol. Allowed decisions include:

- `in_scope`
- `liquidity_review`
- `out_of_scope`
- `excluded`

`listing_data_complete` refers only to listing/quote/scope fields, not financial statements.

## Candidate-Pool Artifact

`broad-screen-results.jsonl` has one row per bounded economic candidate.

### Resolution fields

```json
{
  "enrichment_attempted": true,
  "enrichment_resolved": false,
  "selection_eligible": false,
  "decision": {
    "status": "needs_enrichment",
    "resolution": "unresolved",
    "selection_eligible": false
  }
}
```

`enrichment_attempted` means a source was queried or at least one economic value was supplied. It does not imply resolution.

### Allowed final broad statuses

| Status | Resolution | Can be selected? | Score |
|---|---|---:|---:|
| `selected` | resolved | yes | numeric |
| `deferred_by_budget` | resolved | no | numeric |
| `screened_out` | resolved | no | numeric when assessable |
| `excluded` | resolved | no | optional |
| `unavailable_after_enrichment` | resolved | no | null |
| `needs_enrichment` | unresolved | no | null |

Before budget assignment, economically plausible rows may use `passed`, `passed_exception`, `near_miss_review`, or `sector_review_required`. The serialized final artifact converts selected/deferred rows to `selected` or `deferred_by_budget` while preserving `preselection_status` and deep-dive requirements.

### Unavailable after enrichment

A row may be resolved as `unavailable_after_enrichment` only with:

```json
{
  "enrichment_exhausted": true,
  "enrichment_exhaustion_reason": "specific reason",
  "enrichment_source_ids": ["attempt-source"]
}
```

The source IDs must resolve in the ledger.

## Candidate-Pool Outcomes

### `sufficient / selected`

- one or more selected rows;
- candidate pool exhausted;
- all rows resolved;
- queue empty.

### `sufficient_pending_enrichment / selected_pending_enrichment`

- one or more selected rows;
- unresolved rows or unverified exhaustion remain.

Deep dives may start, but formal final output is prohibited.

### `no_qualifying_candidates / no_candidates`

A **market-wide** conclusion is allowed only when:

```text
conclusion_scope = full_listing_universe
selected_symbols = []
candidate_pool.coverage_complete = true
candidate_pool.in_scope_missing_count = 0
candidate_pool_exhaustion_declared = true
candidate_pool_exhausted = true
all_rows_resolved = true
unresolved_count = 0
queue_count = 0
discovery_evaluable_count > 0
```

### `no_qualifying_candidates_in_bounded_pool / no_candidates_in_bounded_pool`

A reproducibly generated bounded pool may reach this status when its generation audit is valid, every pool row is resolved, exhaustion is verified, the queue is empty, and at least one row was economically assessable. The report must name the bounded `conclusion_scope` and must not make a market-wide claim.

### `insufficient_data`

- no selected rows;
- unresolved evidence remains, enumeration is incomplete, or no row was economically assessable.

Do not describe this as “no qualifying candidates.”

## Soft Guidelines and Hard Broad Failures

Growth, preferred valuation, ROIC, and preferred leverage values are guidelines. Store misses in `guideline_misses`; do not automatically reject a row for one miss.

Hard failures belong in `screen_fail_reasons`, for example:

- `non_positive_standard_fcf`
- `negative_roic`
- `excessive_leverage`
- `extreme_forward_valuation`
- `negative_forward_growth`
- `valuation_not_supported_by_growth`
- `growth_and_valuation_combination_below_review_threshold`

Cyclical normalization is normally a `deep_dive_requirement`, not a hard failure.

## Candidate Deep-Dive Record

Each selected candidate retains schema-v3 structures for:

- identity and price basis,
- sources and evidence,
- corporate-action check,
- latest quarter and full year as separate records,
- financials and TTM cash-flow reconstruction,
- forward same-basis valuation periods,
- forecast bridge and GAAP reconciliation,
- peer set,
- sector profile,
- cyclicality normalization,
- thesis, catalysts, risks, and invalidation conditions,
- score components and penalties.


## Runtime Compatibility

Every snapshot, screening audit, discovery audit, and checkpoint must match the installed v3.6 runtime metadata. A mismatch in skill version, schema version, contract revision, or runtime fingerprint is a hard contract error. File names and human-readable version labels are not sufficient proof.

## Driver-Derived Forecast Contract

For each rankable future period, `forecast_bridge` must contain operating drivers sufficient to calculate the metric independently.

### EPS

```json
{
  "revenue": 1000000000,
  "operating_margin_pct": 20.0,
  "net_interest_and_other": -5000000,
  "tax_rate_pct": 22.0,
  "diluted_shares": 100000000,
  "after_tax_adjustments": 10000000,
  "source_ids": ["forecast-source"]
}
```

The evaluator derives GAAP net income from revenue, margin, interest/other, and tax, then adds sourced after-tax adjustments only for an adjusted basis. A supplied `metric_numerator` is only a cross-check. A bridge that merely sets numerator equal to target EPS times shares fails.

For adjusted periods, driver-derived GAAP EPS must tie to the GAAP reconciliation and driver adjustments must tie to the reconciliation adjustment amount.

### FCF per share

Derive standard FCF from OCF minus positive capex cash outflow, or from a sourced revenue/FCF-margin model, then divide by diluted shares.

## TTM Cash-Flow Evidence

A TTM method is valid only when the construction periods have resolving source IDs:

- `reported_ttm`: source IDs for the reported TTM value;
- `sum_4_discrete`: source IDs for all four discrete quarters;
- `fy_plus_current_ytd_minus_prior_ytd`: source IDs for FY, current YTD, and prior-year YTD.

## Cash and Financial-Quality Evidence

Ordinary companies may normalize reported cash/equivalents into `corporate_cash`. Payments and custodial businesses must explicitly separate corporate cash, customer/settlement funds, and restricted cash. ROIC and EBITDA used for scoring or leverage require resolving primary-source or transparent analyst-calculation evidence.

## Sector and Peak-Profit Evidence

Sector aliases `biopharma`, `pharma`, `biotechnology`, `royalty_biopharma`, and `drug_delivery_platform` normalize to `commercial_biopharma`. Material product/royalty concentration, nearest LOE, source IDs, and 6x/8x stress scenarios are required.

`peak_profit_risk=true` requires sourced mid-cycle normalization even when the numeric cyclicality score is 1 or 2.

## Completion and Checkpoint Invariants

```text
unprocessed_candidates = selected_symbols - verified_candidate_symbols
```

A run cannot be complete when:

- screening audit is invalid;
- candidate pool status is `insufficient_data` or `sufficient_pending_enrichment`;
- candidate pool does not cover every in-scope listing symbol;
- pool exhaustion was not explicitly declared and independently verified;
- any broad row is unresolved;
- queue is nonempty;
- a selected symbol is not verified;
- `no_qualifying_candidates` is claimed without an assessable exhausted pool.

## Markdown Output Contract

The Markdown report must separately show:

### Broad-screen stage

- selected,
- deferred by budget,
- unresolved/review rows,
- unavailable after enrichment,
- screened out,
- excluded.

### Deep-dive stage

- ranked,
- review required,
- screened out,
- excluded.

Never display `0 / 0 / 0 / 0 / 0` for deep-dive counts in a way that hides nonzero broad-screen dispositions.

## v3.5 Multi-Lane Selection and Publication Contract

### Selection lanes

Every selected Broad Screen row records one of:

```text
core_garp
high_growth_exception
quality_near_miss
cyclical_normalization
```

The default five-name plan targets 2/1/1/1 names across these lanes and applies a two-name sector cap when alternatives exist. Unused lane capacity is deterministically backfilled. The selected set remains committed and every selected symbol must receive a verified terminal candidate record.

### Independent driver provenance

Each year-2/year-3 forecast bridge uses:

```json
{
  "construction_method": "independent_driver_model",
  "driver_provenance": {
    "revenue": {
      "origin": "market_consensus",
      "source_ids": ["consensus-source"],
      "target_solved": false
    },
    "operating_margin_pct": {
      "origin": "historical_run_rate",
      "source_ids": ["10-k-source", "analyst-model"],
      "target_solved": false
    }
  }
}
```

Allowed origins are `company_guidance`, `market_consensus`, `historical_run_rate`, `company_target`, `analyst_assumption`, and `primary_source_calculation`. Any driver solved backwards from target EPS or FCF fails the bridge.

### Explicit cash-flow period support

A generic `financials.cash_flow_ttm` support label does not validate four discrete periods. Each source must explicitly support its period path, for example:

```text
financials.cash_flow_periods.2026-06-30
financials.ttm_reconstruction.latest_fy
financials.cash_flow_ttm.reported_ttm
```

### Corporate transitions

Recent spin-offs, transformative acquisitions, and large divestitures are corporate-transition evidence, not sector valuation special cases. Store `identity.special_case = none` and a sourced `corporate_transition` object. Missing pro-forma normalization routes the candidate to `review_required`, not hard exclusion.

### Publication bundle

A formal publication contains the complete run directory plus `BUNDLE_MANIFEST.json`. The manifest records runtime identity, file paths, sizes, SHA-256 values, and the passing prepublication audit. Summary-only ZIP files are invalid.

### Multi-lane provider-prefilter generation audit

A provider-prefilter pool records:

```json
{
  "selection_method": "provider_prefilter",
  "lane_input_counts": {
    "core_garp": 30,
    "high_growth_exception": 20,
    "quality_near_miss": 25,
    "cyclical_normalization": 25
  },
  "lane_selected_counts": {
    "core_garp": 15,
    "high_growth_exception": 15,
    "quality_near_miss": 15,
    "cyclical_normalization": 15
  },
  "lane_coverage_count": 4,
  "minimum_pool": 30,
  "pool_adequate": true,
  "provider_exhausted": false
}
```

A valid high-recall bounded pool normally has at least 30 rows and at least three represented lanes. `provider_exhausted=true` may waive the row floor, but not liquidity evidence or lane disclosure.

### v3.6.1 discovery additions

The discovery audit additionally carries:

```json
{
  "provider_exhausted_scope": "estimate_seed",
  "listing_provider_exhausted": true,
  "estimate_seed_exhausted": true,
  "economic_candidate_universe_exhausted": false,
  "seed_audit": {
    "seed_selection_basis": "stratified_liquidity_proxy",
    "economic_metrics_available_for_seed": false,
    "cell_count": 55,
    "quota_method": "sqrt_hamilton",
    "alphabetic_tie_break_used_count": 0,
    "hash_tie_break_used_count": 3,
    "seed_limit_configured": 180,
    "seed_limit_effective": 180,
    "reserved_calls": 130
  },
  "quality_probe": {"attempted": [], "resolved": [], "source_id": "fmp-key-metrics-ttm-<date>", "calls_used": 0},
  "fcf_prefilter_excluded_symbols": [],
  "fcf_prefilter_exclusions": [{"symbol": "AAA", "lane": "core_garp", "reason": "fcf_yield_below_prefilter_floor"}]
}
```

`provider_exhausted` may waive the pool row and lane floors only together with `provider_exhausted_scope` in {`economic_candidate_universe`, `full_input`}; a missing scope fails closed (no waiver), `estimate_seed` exhaustion never waives either floor, and `pool_floor_waived` / `lane_floor_waived` record the outcomes. The `sharded_snapshot` candidate-generation mode is distinct from a bounded `provider_prefilter`: it requires a screen-ready same-read snapshot bundle, a 64-character digest binding the explicit listing-enumeration audit, manifest, universe, and all shard hashes, economic attempts and classification totals exactly equal to the frozen universe, current per-row normalization provenance, and a final pool containing only `evaluable` rows. Enumeration verification recomputes continuous full-range coverage independently for every requested exchange, and the frozen market-cap/price scope must contain the later screen request. Exact-liquidity attempts continue past empty/failed histories until the 30–50 name target is met or every eligible name has an explicit outcome; only the latter can justify a short-pool exhaustion claim. That proof supports `conclusion_scope: full_listing_universe` even though deep-dive work is budgeted to the deterministic top pool. The unit gate fails closed on unknown context: a row is exempt only when PROVEN domestic (country `US`, no non-US ISIN, not an ADR/ADS, currency USD or unstated) — a missing country, non-USD currency, non-US ISIN, or ADR/ADS flag requires `unit_reconciliation_verified: true` (listing/statement currency and ordinary-shares-per-ADS evidence); without it the row carries the blocking `unit_reconciliation_required` review and, on the direct-FMP path, resolves as `unavailable_after_enrichment`. `normalize_listing` preserves `isin` and `is_adr` for this purpose. Implausible ratios (forward P/E below 2, FCF yield above 50%, reported EPS above twice the listing price) fail the broad screen as `unit_mismatch_suspected` — suspected currency/ADS-unit mismatch, never "deep value". `sector_profile_type` is inferred from an explicit FMP-taxonomy map (`INDUSTRY_PROFILE_MAP` + family-prefix rules + BDC name needles + the `sector_profile_overrides` config pin); `capital_markets` (advisory/investment banking) is labelled but deliberately not a blocked profile. The run summary and report JSON carry a tri-state `ranking_scope` (`final_marketwide` / `final_scoped` / `diagnostic`) with per-stage coverage counts and percentages (`economic_attempt_*`, `economically_evaluable_*`, `quality_probe_*`, `deep_dive_*`); `final_marketwide` requires estimate acquisition attempted for every listing-universe symbol (exact counts) — a seed-based run is at most `final_scoped` and its conclusions never generalize to the market. Sector-profile rows (`sector_profile_type` in reit / insurance / bank / asset_manager / bdc / mlp) skip the general `excessive_leverage` hard gate and instead require sector-specific valuation evidence (`sector_specific_valuation_required`). `economic_candidate_universe_exhausted` and `economic_screen_scope_complete` are true only when bulk estimates covered every listing-universe symbol (exact `covered_symbol_count == universe_symbol_count`; not a configurable ratio), or when the same exact invariant is proven by a verified `sharded_snapshot`; merely using the bulk route (from 20% coverage) does not qualify. `latest_actual_eps` must be a verified reported figure (`latest_actual_verified: true`, `latest_actual_basis`, `latest_actual_source_ids` resolving to an annual statement accepted at or before `analysis_as_of`, or a provider row marked actual whose period has ended); otherwise the actual-derived fields are null. `growth_pattern` and `current_year_growth_pct` are derived on the consensus basis from `fy0_consensus_eps` (the provider's prior-year row, never labelled actual; `growth_pattern_basis`), and `estimate_basis_likely_adjusted` flags a >15% gap between that row and the GAAP actual. Pool rows may carry `quality_probe_attempted`, `quality_probe_resolved`, `quality_probe_source_ids`, `sbc_adjusted_fcf_yield_pct`, `provider_prefilter_flags` (`weak_fcf_support`, `earnings_recovery`, `foreign_private_issuer_review`), and the growth-basis fields `latest_actual_eps`, `fy1_eps_below_latest_actual`, `current_year_growth_pct`, `eps_growth_actual_to_fy3_pct`, `growth_pattern`.

`run-summary.json` / `NEXT_ACTION.json` add `listing_enumeration_complete`, `economic_screen_scope_complete`, `listing_universe_count`, `estimate_seed_count`, `estimate_seed_coverage_pct`, `valid_estimate_count`, `valid_estimate_coverage_pct`; `scope_complete` remains as a deprecated alias of listing-enumeration completeness. The contract-validated `screening_audit.scope` block is unchanged.

### Full-snapshot partial budget diagnostic

`screen-full-snapshot` may return exit 2 with a provider-budget diagnostic
before it can publish a final screening result. The non-final diagnostic has
this shape:

```json
{
  "schema_version": 1,
  "status": "provider_budget_exhausted",
  "stage": "liquidity | quality_probe | candidate_packets",
  "snapshot_id": "string",
  "snapshot_verification_digest": "64-character SHA-256",
  "progress": {
    "target_symbols": ["AAA", "BBB"],
    "attempted_symbols": ["AAA"],
    "completed_symbols": [],
    "pending_symbols": ["AAA", "BBB"],
    "interrupted_symbols": ["AAA"],
    "interrupted_at": {"symbol": "AAA", "operation": "provider_method"}
  },
  "no_final_marketwide_conclusion": true,
  "artifacts": {
    "partial_enriched_estimates": {"path": "...", "sha256": "...", "row_count": 2},
    "run_summary": {"path": "...", "sha256": "..."},
    "next_action": {"path": "...", "sha256": "..."}
  },
  "commit_marker": "audit/partial-run-diagnostic.json"
}
```

The target and progress arrays are uppercase, duplicate-free, and retain target
order. `completed` means all provider calls required by the stage finished;
the interrupted current symbol can therefore be in `attempted` and `pending`.
Consumers must verify the marker exists and every listed artifact hash and row
count matches before reading any partial output. Screening has no resume cursor:
rerun the same verified snapshot after restoring the provider budget. The
snapshot is read-only; existing cache/raw records are retained, successful
calls may append new records, and later runs may reuse them. If packet
generation is interrupted, the broad-screen audit is explicitly non-authoritative:
its status and ranking scope are `incomplete`/`diagnostic`, its top-level,
deep-dive, candidate-pool, and generation-audit selection commitment fields are
cleared, and every broad-screen row is downgraded from `selected` to
`deferred_by_budget`. The candidate artifact hash is rewritten after this
invalidation. Each screen attempt also requires a new empty run directory;
the CLI adds a unique attempt suffix so retries cannot mix stale final
artifacts with a partial run.

### Referencia: references/full-universe-snapshot.md

# Full-universe estimate snapshot (v3.7 — sharded collection)

The v3.6.1 pilot economically evaluates ~4% of the listed universe and is
therefore permanently `ranking_scope: final_scoped`. The v3.7 path earns
`final_marketwide` the only honest way: by attempting estimate acquisition for
EVERY listed symbol at least once. On plans where bulk endpoints are 402, that
means collecting per-symbol across deterministic shards within each run's API
budget, persisted into a frozen snapshot.

## Stage: `collect-estimates`

```bash
python3 scripts/run_pipeline.py \
  --stage collect-estimates \
  --shard-index 0 --shard-count 8 \
  --snapshot-dir .cache/us-garp/snapshot-2026-08 \
  --config assets/claude-code-config.example.json \
  [--resume]
```

- The FIRST invocation enumerates listings and **freezes the universe** into
  the snapshot directory (`snapshot-manifest.json` + `universe.jsonl` +
  `listing-enumeration-audit.json`,
  identified by `snapshot_id` = timestamp + universe SHA-256). Every later
  shard run writes into that frozen snapshot; new listings and delistings go
  to the NEXT snapshot, never mixed in.
- Collection is current-only: a historical or future `--analysis-as-of` is
  rejected before client/cache/raw/snapshot creation. Each row records
  `snapshot_normalization_as_of`; shard manifests aggregate its bounds so a
  later screen cannot treat an old FY-period normalization as current.
- Shard membership is `sha256(symbol) % shard_count` — the same symbol always
  lands in the same shard, so multi-day collection is deterministic.
- Each attempted symbol is normalized (FY1-FY3 EPS/revenue, analyst counts)
  and classified into exactly one bucket:
  `evaluable / no_estimates / negative_eps / unit_mismatch / excluded`
  (precedence: excluded > unit_mismatch > no_estimates > negative_eps >
  evaluable; the unit gate is the round-8 fail-closed
  `requires_unit_reconciliation`).
- **Provider failures are never classified.** The client returns an empty
  list for HTTP failures, offline cache misses and invalid JSON as well as
  for genuinely empty consensus; the stage distinguishes them via the
  client's per-call diagnostics (calls / cache hits / failure count) and
  records failures as `fetch_failed` — the symbol stays uncollected, the
  shard stays `partial` (`shard_partial_fetch_failures`, exit 3), and the
  marketwide invariant cannot be satisfied by outages. HTTP-200 error
  bodies (`{"Error Message": ...}` plan-limit style) are validated in the
  client itself: recorded as `provider_error_payload`, never cached; a
  malformed object that predates validation in an existing cache is
  flagged `unexpected_payload_shape` on read and likewise becomes a fetch
  failure.
- Budget exhaustion mid-shard exits with code **3**, records the shard as
  `partial` in the manifest, and is resumable with `--resume`. A shard file
  that already exists without `--resume` is refused.
- **The frozen universe is re-verified on every load** (manifest schema,
  row count, symbol uniqueness, canonical SHA-256) before any API access or
  shard append; a swapped `universe.jsonl` is refused.
- Every collected row carries `snapshot_retrieved_at` — the ACTUAL fetch
  time. Cache-served rows (any cache hit, including a failed stable HTTP
  attempt falling back to the v3 cache) are stamped from the cache entry's
  creation time; when that provenance cannot be resolved the stamp stays
  **null** (counted as `retrieval_time_unknown`, never back-filled with
  "now"). Shards aggregate `oldest_retrieved_at` / `newest_retrieved_at`,
  and a run that collects nothing does NOT refresh the shard's `as_of`
  freshness stamp.
- Shard summaries (`shard-<i>-summary.json`) and the manifest carry attempted
  / expected / fetch-failed counts, per-bucket classification, `as_of`,
  retrieval and normalization bounds, and calls used.

## Stage: `screen-full-snapshot`

After every shard is complete, run the current-only market-wide screen:

```bash
python3 scripts/run_pipeline.py \
  --stage screen-full-snapshot \
  --snapshot-dir .cache/us-garp/snapshot-2026-08 \
  --config assets/claude-code-config.example.json \
  --output-dir reports/us-undervalued-growth-screener
```

This stage performs its read-only snapshot preflight before constructing the
FMP client or creating cache, provider-raw, or run directories. It refuses an
incomplete, stale, future-dated, tampered, or semantically misclassified
snapshot with exit code 1 and creates no run artifact tree.

The screen is deliberately current-only. Exact-liquidity and TTM quality
probes use current provider evidence, so an operator-supplied historical
`--analysis-as-of` is rejected before those calls rather than mixing current
fundamentals into a historical ranking. The allowed wall-clock skew defaults
to five minutes.

For a ready snapshot, the stage:

1. uses the verified in-memory shard rows from the same reads that produced
   the readiness verdict;
2. rechecks gap-free exhausted bands for every requested exchange, requires
   the frozen market-cap/price scope to contain the screen request, then binds
   that audit, the manifest, frozen-universe SHA-256, and every shard SHA-256
   into a `snapshot_verification_digest` carried by all downstream audits;
3. records the estimate-attempt classification and retrieval provenance for
   every frozen symbol in `universe-audit-results.jsonl`;
4. builds a deterministic 30–50 name multi-lane pool (default 50), backfills
   failed/empty exact-liquidity calls until the target succeeds or every
   eligible symbol has an explicit outcome, probes every preliminary-pool
   name for current quality evidence, and never selects an unprobed deep-dive
   name; and
5. commits five deep-dive slots for the market-wide path.

A verified snapshot with no economically evaluable names can produce a formal
market-wide no-candidate result. Missing coverage, an unresolved enrichment
queue, or a short pool that cannot prove exhaustion remains diagnostic and
exits 2. A successful underwriting handoff or verified no-candidate result
exits 0.

### Budget exhaustion and partial screen diagnostics

Liquidity, quality-probe, and candidate-packet enrichment are fail-closed. If
the provider budget is exhausted, `screen-full-snapshot` exits 2 and persists
`audit/enriched-estimates.partial.jsonl` and
`audit/partial-run-diagnostic.json`. The diagnostic is written last as the
commit marker and records the snapshot ID/digest, stage, target-order
progress, interrupted symbol and provider operation, provider counters, and
SHA-256/row-count records for the partial summary and rows. Consumers must
verify the marker and every recorded hash before reading partial artifacts;
without a valid marker, the preceding files are not authoritative.

The current symbol is `attempted` and `interrupted`, and remains `pending`; a
symbol is `completed` only after all provider calls required by its current
stage finish. Quality-probe interruption preserves a current row even when its
key-metrics call succeeded but its actual-EPS call did not. A packet interrupted
inside an endpoint is not written as a packet; completed packets and provider
raw/cache evidence remain available. The already-written broad-screen audit is
rewritten as `status: incomplete`, `conclusion_scope: diagnostic`, and
`ranking_scope: diagnostic`, with top-level, deep-dive, candidate-pool, and
generation-audit selection commitment fields cleared. Broad-screen rows are
rewritten from `selected` to `deferred_by_budget`, and the audit's row hash is
updated before the diagnostic marker is written.

Each screen attempt uses a new empty run directory. The CLI adds a unique
attempt suffix to the run ID and stores provider raw responses in a sibling,
attempt-specific `.provider-raw/<run-id>/` directory; direct callers are
rejected if they pass a non-empty output directory. An explicitly supplied raw
store must also remain outside the run directory. This prevents a retry from
mixing partial output with stale final artifacts from an earlier attempt.

There is no `--resume` for screening. After the budget is restored, rerun the
same verified snapshot; successful new calls may append cache/raw records and
the rerun may reuse existing records, but the snapshot itself remains
read-only. Partial output never authorizes a market-wide conclusion or a real
trade.

## Readiness and content binding

Two layers, deliberately separate:

- **`snapshot_status(manifest)` → `collection_ready`** — manifest-level
  aggregation only (all shards complete with zero `fetch_failed`,
  classification counts summing exactly to the frozen universe,
  `retrieval_time_unknown == 0`, `normalization_time_unknown == 0`). It trusts
  the manifest's own counters and
  therefore proves nothing about the shard files.
- **`load_verified_snapshot(snapshot_dir, screening_as_of=..., max_staleness_days=...)`
  → `verdict + verified rows`** — the ONLY source of the screening verdict and
  consumable rows. It
  reads the hash-bound listing-enumeration audit and every `shard-*.jsonl`
  exactly once and verifies against the frozen universe:
  file presence and SHA-256 vs the manifest, no duplicate symbols, every
  symbol in the frozen universe and in its `stable_shard` shard, the union
  covering the universe EXACTLY, classifications limited to allowed values,
  per-shard counts matching the manifest — plus staleness measured from the
  ACTUAL aggregated `oldest_retrieved_at` and
  `oldest_normalization_as_of` against
  `screening_as_of - max_staleness_days` (never the operator-supplied
  collection `as_of`).

Only a run screened from this same-read bundle with
`ready_for_screening: true`, an exact classification total, and a bound
`snapshot_verification_digest` may emit `ranking_scope: final_marketwide`.

## Operating on the FMP Starter plan

~2,371 symbols ≈ 1 estimate call each. With a 350-call per-run budget and the
750-call daily plan limit, 8 shards (~300 symbols each) collect in 2 shards/day
over 4 days. After the initial build, only incremental refresh is needed
(new snapshot per refresh cycle; post-earnings and revised names first).

## Shared coverage semantics

`scripts/coverage_semantics.py` is the single source of truth for
`classify_ranking_scope` / `build_coverage_block` /
`derive_ranking_scope_from_audit` / `validate_coverage_block`; both
`run_pipeline` (discovery) and `evaluate_candidates` (final evaluation) import
it, so the tri-state semantics cannot drift between the two sides.

### Referencia: references/methodology-ja.md

# 米国割安成長株スクリーニング運用ガイド

## 1. 目的

米国上場企業の中から、単なる低PER株ではなく、**現在のバリュエーションが上昇しなくても、EPSまたはFCF per shareの健全な成長だけで、2～3年間に30～50％程度以上の株価上昇を期待できる企業**を発見する。

重視するのは次の組み合わせである。

- 中長期の売上成長
- 1株当たり利益・FCFの成長
- 高い資本効率
- 良好な利益の質
- 過大でない負債
- 小さいSBC・希薄化
- 妥当な同業比較
- 景気循環を平準化しても残る割安度


## v3.5の必須統制

v3.5では、schema v3の会計・証拠管理を維持しつつ、v3.1で発生した「未解決候補が残っているのに該当なしで完了する」問題を修正する。

1. 全母集団では上場状態、株価、時価総額、流動性を監査する。
2. Provider総件数とページ枯渇、または全時価総額帯の枯渇証拠を記録する。取得上下限が一致するだけでは母集団完全性としない。
3. 市場全体の大半についてROIC、FCF、負債、Forward PERを取得することを完了条件にしない。
4. ベンダープリフィルター、利用可能な予想値、またはセクター×時価総額×流動性で層化した限定候補プールを作る。
5. `enrichment_attempted`と`enrichment_resolved`を分離する。試行数や評価可能数の閾値だけでは未解決キューを完了扱いにしない。
6. 売上成長率、1株成長率、ROIC、優先PERは単独の機械的足切りではなくガイドラインとして扱う。
7. PER21～30倍の高成長例外や、売上成長率が低めでもForward PERと1株成長が魅力的な近似候補を詳細調査へ進める。
8. シクリカル度3～5は`mid_cycle_normalization_required`を付けて詳細調査へ進める。金融・REIT・自動車販売など、一般企業指標が不適切な業種は専用指標が揃うまでブロックする。
9. エンリッチメント順はGARP適合可能性、予想人数、不足項目、ベース効果で決め、流動性やティッカー順だけで決めない。
10. `no_qualifying_candidates`は、プール枯渇、未解決0、キュー0、全行最終処分、評価可能行1件以上のときだけ許可する。
11. `unprocessed = selected - verified`を不変条件とし、選定した全銘柄に検証済みレコードを作る。
12. Markdownには一次選定、予算繰越、要補完、取得不能、一次落ち、除外をすべて表示する。
13. 市場指標の鮮度は取得日時ではなく、`data_as_of`または公表日時で検証する。

従来のschema v3統制も継続する。四半期と通期の分離、NTM/FY1倍率、予想人数、情報源型、EV/FCFの現金定義、医薬品LOE、自動車販売会社のFloorplan Debt、企業イベント事前確認、設備投資符号、TTM再構築、標準FCFとAdjusted FCFの分離、GAAP調整表、チェックポイント、`--require-final`である。

### v3.5追加統制

1. 監査、チェックポイント、最終スナップショットに同一の実行時フィンガープリントを必須とし、v3.1／v3.2の古い成果物を拒否する。
2. 監査済み限定プールは、その範囲を明示した正式ランキングを作れるが、市場全体の「該当なし」と表現しない。
3. EPS・FCF予想は、売上高、利益率、金利・その他、税率、税引後調整、希薄化後株式数から独立再計算する。目標EPS×株数で逆算した分子は検証にならない。
4. Adjusted予想は、ドライバーから算出したGAAP指標と税引後調整額をGAAP調整表へ別々に一致させる。
5. TTMキャッシュフローを構成する各期間に情報源IDを要求する。
6. 現金分類、ROIC、EBITDAに根拠がなければ、データ品質点を制限する。
7. `biopharma`、`royalty_biopharma`、`drug_delivery_platform`等もcommercial biopharmaへ正規化し、製品・ロイヤリティ集中、LOE、6倍・8倍ストレスを要求する。
8. `peak_profit_risk=true`なら、シクリカル度が1～2でも平準化を必須とする。
9. Broad Screenの決定論的ステータスを説明生成段階で上書きしない。
10. ユーザー依頼の時価総額範囲と実際の取得範囲を分離し、内部予算を理由に依頼範囲を書き換えない。
11. 流動性は20営業日以上の平均売買代金またはProvider平均出来高から計算し、単日出来高を使用しない。
12. Forward PERは日付付きのNTMまたはFY1 EPSからのみ計算し、FY1欠損時にFY2・FY3を代用しない。
13. Broad Screenで選定した集合をハッシュで確定し、全選定銘柄を完了させる。予算変更はBroad Screenの再実行で行う。
14. Helperのexit code 2は同一実行内の継続指示であり、ユーザーへ「続けて」と求めない。

## 段階的スクリーニング

### レイヤーA：全母集団の上場・流動性監査

取引所、普通株・アクティブ状態、株価、時価総額、売買代金を確認する。この層は対象範囲の監査であり、全社の財務精査を意味しない。

### レイヤーB：限定された経済候補プール

Forward評価と1株当たり成長予想を取得できる透明な候補プールを作る。ベンダーのプリフィルターを優先し、利用できない場合はセクターと時価総額で層化した流動性の高い銘柄を予想値で補完する。

### レイヤーC：一次情報による精査

選定した銘柄だけをSEC・IRで確認し、キャッシュフロー、会計基準、同業、景気循環、業種KPI、シナリオを完成させる。

## 2. 調査範囲

標準条件：

- NYSE、Nasdaq、NYSE American
- 普通株
- 時価総額5億～200億ドルを中心
- 株価5ドル以上
- 平均売買代金500万ドル以上
- 最終候補は最大10銘柄。条件を満たさなければ無理に10銘柄へ増やさない

原則除外：

- OTC、ペニー株、極端な低流動性銘柄
- 実質的な事業を持たないSPAC・シェル
- 売上がほとんどない開発段階バイオ
- 継続的な増資を前提とする企業
- M&A価格に株価が固定された合併裁定銘柄
- 未解決の重大な会計・内部統制・ガバナンス問題
- 事業実態よりミーム需給だけで評価される銘柄

除外した企業と理由を記録し、黙って候補から消さない。

## 3. 段階的スクリーニング

### 第0段階：全上場母集団の監査

依頼範囲の各銘柄について、上場状態、普通株判定、取引所、株価、時価総額、流動性、情報源、実際の取得上下限を保存する。この層は対象範囲と売買可能性の監査であり、全社の完全な財務データを意味しない。

### 第1段階：限定候補プールの作成と補完

再現可能なベンダー絞り込み、利用可能な一括予想値、またはセクター×時価総額×流動性の層化抽出を使う。限定プールだけにForward評価と1株当たり成長予想を補完する。Forward評価、1株成長、予想人数などのブロック項目が足りない行は`needs_enrichment`とし、点数を付けない。金融・REIT・自動車販売は専用指標が揃うまで同様にブロックする。高シクリカル企業の平準化不足は非ブロックとし、魅力的な候補は`sector_review_required`として実スコア付きで詳細調査へ進める。

候補発見の目安：

- 売上成長率10％前後以上
- EPSまたはFCF per share成長率15％前後以上、20～30％を高評価
- Forward PER 20倍以下を中心とし、高成長・高品質なら30倍まで例外
- 標準FCF黒字または業種別適切指標
- ROIC 10％前後以上
- 業種調整後Net Debt / EBITDA 2.5倍以下
- 希薄化後株式数の年率増加3％以下
- 十分な売買代金

限定プールは、全行が解決済みで、プール枯渇を確認した場合だけ完了扱いにする。試行しただけでは解決済みにしない。選定0であっても、未解決行やキューが残る場合は`insufficient_data`であり、「該当なし」ではない。正式な「該当なし」には、評価可能な行が1件以上必要である。

### 第2段階：企業イベント事前確認

詳細調査前に、上場状態、M&A、上場停止・廃止、ティッカー変更、株式分割、スピンオフ、最新重要イベント日時を確認する。進行中・完了済みM&Aや非アクティブ銘柄は通常ランキングから除外し、選定済みであれば除外レコードとして完了保存する。

### 第3段階：一次情報による精査

選定した全銘柄をSEC・IRで確認し、`eligible`、`review_required`、`screened_out`、`excluded`のいずれかへ完了させる。

最終的に必ず答える問い：

1. 成長は持続可能か。
2. 総額ではなく1株当たりでも成長しているか。
3. 利益は営業キャッシュフローに裏付けられているか。
4. 割安理由は一時的か、構造的か。
5. PERが上昇しなくても十分なリターンがあるか。
6. PERが20％低下してもプラスのリターンが残るか。
7. どの数値・事象で投資仮説を無効化するか。

## 4. 分析時点の固定

候補間で比較する前に、分析スナップショットを固定する。

記録項目：

- 分析日時とタイムゾーン
- 株価取得日時、通常終値・プレマーケット・時間外の区分
- 最新決算期と発表日時
- 最新の重要な企業イベント
- コンセンサス取得日時
- FY1、FY2、FY3の会計年度対応
- 通貨と株式分割調整の有無

決算発表後の情報と決算発表前の終値を混在させない。混在する場合は株価を更新するか、明確に「イベント前評価」と表示する。厳格モードでは除外する。

## 5. 情報源と分類

重要な数字を次の4種類へ分類する。

- `reported_fact`：報告済み実績
- `company_guidance`：会社予想
- `market_consensus`：市場コンセンサス
- `analyst_estimate`：分析上の独自予想

優先順位：

1. SEC提出資料
2. 企業の決算リリース、株主書簡、説明資料、Prepared Remarks、Investor Day
3. 信頼できるデータベンダーの会社予想・コンセンサス
4. ニュース・外部分析は補足

情報が矛盾する場合はSEC提出資料を優先し、差異を説明する。

コンセンサスには、取得日、対象年度、FY1/FY2/NTM、GAAP/Adjusted、アナリスト数、可能なら予想レンジを付ける。

## 6. 主要計算

### 標準FCF

設備投資は**正のキャッシュ支出額**へ正規化する。ベンダーが負号付きで返す値をそのまま入力しない。

```text
標準FCF = 営業キャッシュフロー - 設備投資キャッシュ支出額
```

TTMは、報告済みTTM、独立した4四半期の合計、または「直近通期＋当期YTD－前年同期YTD」のいずれかで作る。3カ月・6カ月・9カ月の累計値を重複合計しない。会社独自Adjusted FCFは定義を付けて別表示し、標準FCFの代替にしない。

### SBC控除後の経済的FCF

```text
SBC調整後FCF = 標準FCF - Stock-Based Compensation
```

これはGAAPのキャッシュフロー指標ではなく、株主経済価値を見る補助指標である。標準FCFと併記する。

### FCF per share

```text
FCF per share = 標準FCF / 希薄化後加重平均株式数
```

### ネットデットと利用可能現金

```text
利用可能現金 = 企業現金 + 株主に利用可能な有価証券
Net Debt = 有利子負債 - 利用可能現金
```

顧客資金、加盟店・決済フロート、制限現金を企業現金へ含めない。特に決済会社では総現金とCorporate cashを分ける。

### ROIC

原則としてNOPATを平均投下資本で割る。ベンダー値を使う場合は定義を確認する。銀行・保険・REIT等には業種別指標を使う。

## 7. 成長の評価

過去3～5年：

- 売上CAGR
- GAAP EPS CAGR
- 標準FCF per share CAGR
- 基本・希薄化後株式数の増減
- 粗利益率、営業利益率、FCFマージン
- ROIC推移

将来2～3年：

- 今期・来期の売上成長
- 今期・来期のEPS成長
- 2年後・3年後のEPSまたはFCF per share
- 将来の希薄化後株式数

市場拡大、シェア上昇、ストック収益、スイッチングコスト、ネットワーク効果、製品ミックス、海外展開、営業レバレッジは加点する。

顧客・製品集中、M&Aだけの成長、株式発行を伴う成長、特需、補助金依存、コモディティ価格だけの増益、数量減を伴う値上げ、利益を犠牲にした売上成長は減点する。

## 8. EPS・FCF予想の整合性

コンセンサスをそのまま転載せず、少なくとも以下へ分解する。

```text
売上高
× 粗利益率
- 営業費用
= 営業利益
+/- 金利・その他
- 税金
= 純利益
÷ 希薄化後株式数
= EPS
```

FCFは、利益、非現金費用、運転資本、設備投資に分解する。

利益率の急上昇、税率の異常低下、過大な自社株買い、希薄化無視など、説明のない前提を警告する。

## 9. GAAPとNon-GAAP

現在、2年後、3年後の評価指標は、`gaap`、`company_adjusted`、`analyst_normalized`、`sector_defined`のいずれか一つへ統一する。現在GAAP、将来Adjustedのような混在では、PER据え置きシナリオを計算しない。Adjustedまたは分析者正規化指標は、GAAP指標、調整項目、反復性、算術一致、情報源IDを示す。


GAAP営業利益、Adjusted営業利益、GAAP EPS、Adjusted EPS、GAAP純利益、Adjusted EBITDA、標準FCF、Adjusted FCFを混同しない。

毎期繰り返すSBC、リストラクチャリング、買収費用、無形資産償却等を「一時的」として除外している企業は、Adjusted利益を割り引いて評価する。

## 10. 利益の質

確認項目：

- 純利益と営業キャッシュフローの乖離
- 売掛金・DSO
- 在庫・在庫日数
- 未請求売上・契約資産
- ソフトウェア開発費やR&Dの資本化
- リストラクチャリング・買収費用の常態化
- のれん・無形資産・減損
- 税効果・資産売却益・年金会計
- 関連当事者取引
- 監査法人変更
- Internal Control Weakness、修正再表示、SEC調査
- KPI定義の頻繁な変更

運転資本の一時的改善でFCFが増えている場合、通常状態のFCFを別途評価する。

## 11. SBC・希薄化・自社株買い

必ず確認：

- SBC金額
- SBC / 売上高
- SBC / 営業キャッシュフロー
- 基本・希薄化後株式数の3年推移
- RSU、オプション、ワラント、転換社債、ATM、Shelf、公募
- 実際の買い戻し額・株数

自社株買いの発表額ではなく、SBC発行分を差し引いた純減少株式数を評価する。負債で高値買い戻しをしていないかも確認する。

## 12. バリュエーションとシナリオ

利用指標：

- NTM/FY1/FY2予想PER
- EV/EBITDA、EV/EBIT、EV/FCF
- FCF利回り、SBC調整後FCF利回り
- PEG
- 自社5年中央値
- 真に比較可能な同業中央値

### PER据え置き

```text
将来株価 = 将来EPS × 現在Forward PER
上昇率 = 将来株価 / 現在株価 - 1
年率リターン = (将来株価 / 現在株価)^(1/年数) - 1
```

### PER20％低下

```text
ストレスPER = 現在PER × 0.8
ストレス将来株価 = 将来EPS × ストレスPER
```

### 同業中央値

比較基準が同一の場合のみ補助的に計算する。ランキングはリレーティングを前提にしない。

## 13. 同業比較

3～5社を、事業構造、顧客、成長段階、収益モデル、利益率、資本集約度で選ぶ。選定理由を説明する。

比較する指標：

- 成長率
- 利益率
- ROICまたは業種別収益性
- レバレッジ
- FCF利回り
- SBC
- 希薄化
- Forward valuation

対象企業だけが安い理由を、一時的・構造的・合理的のいずれかに分類する。

## 14. シクリカル評価

1～5で評価する。

- 1：景気影響が小さい
- 2：やや影響
- 3：中程度
- 4：大きい
- 5：極めて大きい

シクリカル企業は5～10年の売上、利益率、EPS、FCF、受注、受注残、Book-to-Bill、在庫、稼働率、顧客設備投資、商品価格、景気後退時の利益減少を確認する。

ピーク利益ではなく、ミッドサイクルEPS・FCFで実質PER・EV/FCFを計算する。

## 15. 直近決算

記録：

- 決算期・発表日
- 売上高、前年比、前四半期比、Organic Growth
- 粗利益率、GAAP営業利益・利益率
- GAAP EPS、Adjusted EPS
- 営業キャッシュフロー、FCF、設備投資、SBC
- 希薄化後株式数
- 会社予想と修正方向
- セグメント、受注、受注残、業種別KPI
- 一時項目、運転資本、税率

成長状態を、加速、安定、やや減速、明確に減速、底打ち、ピークアウトに分類する。

## 16. カタリスト・リスク・無効化条件

6～24カ月のカタリストを、時期、実現確率、影響経路とともに記載する。

最大リスクを抽象語だけで書かない。無効化条件は数値・事象で示す。

例：

- 売上成長率が2四半期連続で8％未満
- 受注残が前年比減少
- 粗利益率が55％未満
- NRRが100％未満
- Net Debt / EBITDAが3倍超
- 年率希薄化率が5％超
- FCF赤字化
- 主要顧客喪失
- 通期ガイダンス撤回

## 17. Fail-Closed方針

次の場合はランキングしない。

- 株価・決算・予想の基準時点が不整合
- 業種に不適切な評価指標
- 重要数値の出典不足
- データ品質が最低基準未満
- Hard exclusionが未解決
- 将来1株指標の整合性を確認できない
- 必須の同業比較・サイクル平準化ができない

状態：

- `eligible`：ランキング可能
- `review_required`：有望だが未解決事項あり
- `screened_out`：上場・取引は有効だが経済条件で一次選考落ち
- `excluded`：M&A完了、非アクティブ、上場廃止、ハード除外条件または無効入力

未処理銘柄がある実行は`provisional`とし、完了済み銘柄の計算を表示しても最終3銘柄は選定しない。

条件を満たす企業がなければ「現時点では該当なし」と結論づける。

## v3.5 候補品質の改善

- コアGARP、高成長例外、割安ニアミス、ミッドサイクル精査銘柄を複数レーンで選び、単一スタイルへの偏りを抑える。
- 30%上昇余地だけでなく、SBC控除後FCF、EV/FCF、ROIC、負債、希薄化、予想下限ケース、LOE尾部リスクを正式ランク条件にする。
- 軽微な不足は`conditional`、重大な不足は`review_required`とし、質の弱い候補を無理にランキングしない。
- 売上、利益率、金利、税率、株式数など各予想ドライバーに独立した根拠を要求し、目標EPSからの逆算を禁止する。
- スピンオフや大型買収はハード除外ではなく、Pro Forma平準化を必要とする企業移行イベントとして扱う。
- 最終レポートは事前監査を通し、参照した全原票を含む自己完結ZIPとして提供する。

### Providerプリフィルターの再現率保護

単一の「PER20倍以下・売上成長8%以上・低シクリカル」という条件だけで候補プールを作らない。コアGARP、高成長例外、割安ニアミス、シクリカル平準化の4レーンを別々に取得して統合する。限定プールは原則30銘柄以上、少なくとも3レーンを含め、選定前に全行を解決する。

### Referencia: references/methodology.md

# US Undervalued Growth Screening Methodology

## 1. Objective

Identify US-listed companies whose **per-share economic value** can compound fast enough to produce attractive two- to three-year returns without relying on multiple expansion.

The central test is:

> If the current valuation multiple remains unchanged, can healthy EPS or free-cash-flow-per-share growth alone support a credible 30% to 50% total price increase over two to three years?

A low P/E ratio is not sufficient. The candidate must also demonstrate sustainable growth, acceptable financial risk, high-quality earnings, sensible capital allocation, limited dilution, and a defensible business position.


## Version 3.5 Mandatory Controls

Contract 3.5 adds the following non-negotiable controls:

1. Every artifact carries the installed runtime fingerprint; stale v3.1-v3.4 artifacts are rejected.
2. A bounded provider/discovery pool can support a scoped final ranking only when its generation is audited and every pool row is resolved; it cannot support a market-wide no-candidates claim.
3. Forecasts are reconstructed from revenue, margin, interest/other, tax, adjustments, and diluted shares. A numerator reverse-engineered from target EPS is not a forecast bridge.
4. Adjusted forecasts separately reconcile the driver-derived GAAP metric and after-tax adjustments.
5. TTM cash-flow periods require resolving source evidence.
6. Cash classification, ROIC, and EBITDA require evidence before quality points can be awarded.
7. Commercial-biopharma aliases trigger concentration, LOE, and 6x/8x stress controls.
8. `peak_profit_risk=true` requires normalization regardless of the numeric cycle score.
9. The deterministic broad-screen decision is authoritative; the narrative layer cannot reintroduce a mechanical revenue-growth or cyclical exclusion.
10. Preserve the user-requested market-cap range independently from the executed retrieval range; internal budget pressure cannot silently redefine the request.
11. Accept only 20+ session average-dollar-liquidity evidence; one-session volume cannot determine discovery eligibility or order.
12. Normalize dated annual estimates to the current NTM/FY1 horizon before computing Forward P/E; never substitute FY2/FY3 because FY1 is missing.
13. Commit the selected set and complete every selected symbol; any budget reduction requires a new deterministic broad-screen run.
14. Treat helper exit code 2 as an internal continuation signal and never require a separate user “continue” turn.

## Inherited v3.2 Controls Retained in v3.5

Contract revision 3.2 preserves schema-v3 accounting and evidence controls while correcting the v3.1 completion and candidate-routing defects:

1. Audit listing, quote, market-cap, and liquidity fields across the full requested universe.
2. Prove universe enumeration through provider totals plus exhausted pagination or exhausted market-cap-band audits. Requested/retrieved endpoints alone do not prove completeness.
3. Do **not** require complete statements, ROIC, FCF, leverage, and forward estimates for most of the market.
4. Generate a bounded candidate pool through a provider prefilter, available estimates, or a deterministic sector/market-cap/liquidity fallback.
5. Distinguish `enrichment_attempted` from `enrichment_resolved`. Attempt-count and evaluable-count thresholds never complete a pool with unresolved rows.
6. Permit high-quality near misses and P/E 21–30 high-growth exceptions. Growth thresholds are guidelines, not isolated hard gates.
7. Route strong cyclicals to deep dive with `mid_cycle_normalization_required`; do not automatically reject them. Financial-sector and auto-dealer valuation/leverage gaps remain blocking.
8. Prioritize enrichment by GARP information value, not ticker order or liquidity alone.
9. A valid no-candidates result requires an exhausted pool, zero unresolved rows, an empty queue, all final dispositions, and at least one economically assessable row.
10. Enforce `unprocessed = selected - verified`; every selected symbol ends with a verified candidate record.
11. Render broad-screen selected, deferred, review, unavailable, screened-out, and excluded rows in the final Markdown instead of hiding them behind empty deep-dive counts.
12. Validate dynamic market fields against their `data_as_of`/publication date and require official sources for policy, Treasury, inflation, and GDP.

The existing schema-v3 controls remain mandatory: separate quarter/full-year records; NTM/FY1 formal valuation; analyst-count rankability; typed source ledgers; consistent EV/FCF cash definition; commercial-biopharma concentration/LOE stress; auto-dealer floorplan treatment; corporate-action preflight; evidence-derived quality; positive capex-outflow convention; explicit TTM reconstruction; standard versus adjusted FCF separation; same-basis periods; GAAP reconciliation; checkpointing; and `--require-final`.

## Tiered Screening Process

### Layer A: Listing-universe audit

Audit all retrieved symbols for exchange, active/common-stock status, price, market cap, and liquidity. This layer establishes scope and trading eligibility; it does not claim full financial coverage.

### Layer B: Bounded economic discovery

Create a transparent candidate pool with forward valuation and per-share growth evidence. Use a provider prefilter when available. If bulk fundamentals are unavailable, stratify up to 120 liquid in-scope symbols across sectors and market-cap bands, enrich them with available estimates, and record every attempt.

### Layer C: Primary-source underwriting

Verify the selected set with SEC and IR materials, normalize cash flow and accounting basis, compare genuine peers, apply cycle/sector controls, and calculate formal scenarios.

## 2. Universe

### Default scope

- Exchanges: NYSE, Nasdaq, NYSE American.
- Security type: operating-company common stock.
- Market capitalization: normally USD 500 million to USD 20 billion.
- Minimum price: configurable; default USD 5.
- Minimum average daily dollar volume: configurable; default USD 5 million.
- Final ranking: no more than 10 candidates, and fewer when evidence is weak.

### Allowed exceptions

Include a company outside the default market-cap range only when it strongly satisfies the methodology. Record the reason for the exception.

### Hard or presumptive exclusions

- OTC securities.
- Penny stocks or extreme liquidity risk.
- Shell companies and pre-combination SPACs.
- Development-stage biotechnology companies with little operating revenue.
- Businesses dependent on repeated equity issuance for survival.
- Pending merger-arbitrage situations where price is anchored to transaction terms.
- Companies with unresolved material restatements, internal-control weaknesses, severe governance concerns, or active SEC investigations.
- Meme-driven securities without operating support.

Preserve excluded names and reasons in the screening audit trail.

## 3. Staged Screening Process

### Stage 0: Full listing-universe audit

Retain one row per requested symbol with active/common-stock status, exchange, price, market capitalization, liquidity, source ID, and actual retrieval bounds. This layer proves scope and tradability; it does not claim full financial coverage.

### Stage 1: Bounded candidate generation and enrichment

Use a reproducible provider prefilter, already-available estimates, or a deterministic sector × market-cap × liquidity discovery pool. Enrich only the bounded pool with forward valuation and per-share growth. Missing blocking discovery metrics become `needs_enrichment` and receive no score. Financial-sector or auto-dealer valuation/leverage gaps remain blocking. A cyclical normalization requirement is nonblocking: a strong candidate may receive `sector_review_required`, a real score, and selection for mid-cycle deep-dive verification.

Suggested guidelines for assessable rows:

- Revenue growth near 10% or better where appropriate.
- EPS or FCF-per-share growth near 15% or better; 20%–30% preferred.
- Forward P/E normally 20x or lower, with justified high-growth exceptions through 30x.
- Positive standard FCF or a sector-appropriate substitute.
- ROIC near 10% or better where relevant.
- Net debt/EBITDA normally 2.5x or lower using sector adjustments.
- Diluted-share growth normally 3% or lower.
- Adequate dollar-volume liquidity.

The pool is complete only after every bounded row is resolved and the operator has verified exhaustion. A query attempt does not equal resolution. `no_qualifying_candidates` additionally requires zero selected rows and at least one economically assessable row. If no assessable row exists, the result is `insufficient_data`, not “no candidates.”

### Stage 2: Corporate-action preflight

Before deep financial work, verify active listing/symbol, pending or completed M&A, delisting/suspension, ticker changes, splits, spin-offs, and the latest material-event time. Pending/completed M&A and inactive/delisted securities are hard exclusions from normal GARP ranking. Preserve source IDs and checkpoint the result.

### Stage 3: Primary-source underwriting

For every selected name, verify load-bearing facts with SEC filings or company IR and complete one auditable record even when the final classification is review-required, screened-out, or excluded.

The deep dive must answer:

1. Is growth real and durable?
2. Is growth visible on a per-share basis?
3. Is reported profit supported by operating cash flow?
4. Is the valuation low for a temporary reason or a structural one?
5. Does the return case survive without re-rating?
6. Does the return case survive a 20% multiple contraction?
7. What measurable facts would invalidate the thesis?

## 4. Immutable Analysis Snapshot

Create one analysis snapshot before comparing candidates.

Record:

- Analysis timestamp and timezone.
- Price timestamp, session, and timezone.
- Whether price is regular close, pre-market, or after-hours.
- Latest earnings period and publication timestamp.
- Latest material corporate action timestamp.
- Consensus retrieval timestamp.
- Fiscal-year mapping used for FY1, FY2, and FY3.
- Currency and split-adjustment status.

### Stale-data gate

A price is stale when it predates a later earnings release or material corporate action while the analysis uses the post-event information. Either update the price or clearly label the report as a pre-event valuation. In strict mode, reject the candidate.

### Fiscal-year consistency

Do not mix calendar-year estimates with fiscal-year estimates. Do not compare a trailing metric for one company with a forward metric for another without labeling the mismatch.

## 5. Source Classification and Hierarchy

Classify every important figure as one of:

- `reported_fact`
- `company_guidance`
- `market_consensus`
- `analyst_estimate`

Primary-source hierarchy:

1. SEC 10-K, 10-Q, 8-K, 20-F, or 6-K.
2. Company earnings release, shareholder letter, investor presentation, prepared remarks, or investor-day material.
3. Company guidance transcribed by a reputable data source.
4. Market-data vendor or consensus database.
5. Reputable news or analysis for context only.

When sources conflict, prefer the SEC filing, then explain the discrepancy.

For consensus estimates record:

- retrieval date,
- fiscal period,
- FY1/FY2/NTM classification,
- GAAP or adjusted basis,
- analyst count,
- estimate range or dispersion when available.

Never silently fill missing values.

## 6. Core Financial Definitions

### Standard free cash flow

Normalize capex as a **non-negative cash-outflow magnitude**. A vendor value reported with a negative cash-flow sign must be converted before evaluation.

```text
Standard FCF = operating cash flow - capex cash outflow
```

Declare one TTM method: explicitly reported TTM; four unique discrete quarters; or latest FY plus current YTD minus prior-year comparable YTD. Never sum overlapping cumulative 3-, 6-, and 9-month cash-flow statements. If the company presents adjusted FCF, show it separately with its definition; do not substitute it for standard FCF.

### SBC-adjusted economic FCF

```text
SBC-adjusted FCF = standard FCF - stock-based compensation
```

This is an economic lens, not a GAAP cash-flow measure. Show both values. Do not double-count SBC if the selected FCF definition already deducts it.

### FCF per share

```text
FCF per share = standard FCF / diluted weighted-average shares
```

Use diluted shares and a consistent period.

### Enterprise value

```text
Enterprise value = market capitalization + total debt + preferred stock
                   + non-controlling interest - cash and equivalents
```

Use a consistent definition and document material adjustments.

### Net debt / EBITDA

```text
Usable cash = corporate cash + eligible marketable securities
Net debt / EBITDA = (total debt - usable cash) / EBITDA
```

Exclude customer, merchant, settlement, and restricted funds from usable cash. Use normalized EBITDA for cyclicals. Negative net debt is acceptable and should not be forced to zero.

### ROIC

Preferred definition:

```text
NOPAT = adjusted operating income * (1 - normalized cash tax rate)
Invested capital = average operating assets - average operating liabilities
ROIC = NOPAT / average invested capital
```

Use a vendor ROIC only after confirming its definition. For financial companies, use sector-appropriate returns instead.

## 7. Growth Analysis

Measure both aggregate and per-share growth.

Required historical views when available:

- Three- to five-year revenue CAGR.
- Three-year GAAP EPS CAGR.
- Three-year standard FCF-per-share CAGR.
- Basic and diluted-share change.
- Gross, operating, and FCF margin trends.
- ROIC trend.

Required forward views:

- Current fiscal-year revenue and EPS growth.
- Next fiscal-year revenue and EPS growth.
- Two- and three-year EPS or FCF-per-share forecast.
- Forecast diluted-share count.

### Growth-quality checklist

Positive drivers include:

- market expansion,
- market-share gains,
- recurring revenue,
- switching costs,
- network effects,
- pricing backed by stable volume,
- mix improvement,
- new products or capacity,
- international expansion,
- cross-selling,
- aftermarket revenue,
- operating leverage.

Negative drivers include:

- customer or product concentration,
- acquisition-only growth,
- equity-funded acquisitions,
- temporary demand surges,
- subsidy dependence,
- commodity-price-only growth,
- price increases with declining volume,
- deteriorating customer-acquisition economics,
- growth achieved by sacrificing unit economics.

## 8. Forecast Bridge

Do not treat consensus as self-validating. Reconstruct the estimate.

At minimum bridge:

```text
Revenue
x gross margin
- operating expenses
= operating income
+/- interest and other income
- taxes
= net income
/ diluted shares
= EPS
```

For FCF, bridge:

```text
Operating income / net income
+ non-cash charges
+/- working-capital change
- capex
= standard FCF
/ diluted shares
= FCF per share
```

Test whether margins, tax rate, interest, and share count are plausible. Flag forecasts that rely on unexplained linear extrapolation, abrupt margin expansion, or aggressive buyback assumptions.

## 9. GAAP and Non-GAAP Discipline

The current, year-2, and year-3 valuation metrics must use one accounting basis: `gaap`, `company_adjusted`, `analyst_normalized`, or `sector_defined`. A current GAAP metric cannot be compared with future adjusted consensus under a constant multiple. Mixed bases block the scenario. Company-adjusted and analyst-normalized metrics require an arithmetic reconciliation from GAAP with labeled adjustment rows, recurring/nonrecurring classification, and source IDs.


Always distinguish:

- GAAP operating income,
- adjusted operating income,
- GAAP net income,
- GAAP EPS,
- adjusted EPS,
- adjusted EBITDA,
- standard FCF,
- company-defined adjusted FCF.

Investigate recurring exclusions:

- stock-based compensation,
- restructuring costs,
- acquisition costs,
- intangible amortization,
- litigation costs,
- impairment charges,
- one-time tax benefits.

A cost that recurs every quarter or year is not economically one-time. Penalize large or widening GAAP/non-GAAP gaps.

## 10. Earnings and Cash-Flow Quality

Review:

- Net income versus operating cash flow.
- Accounts-receivable growth and DSO.
- Inventory growth and days inventory.
- Unbilled revenue and contract assets.
- Capitalized software or R&D.
- Recurring restructuring and acquisition charges.
- Goodwill and intangible growth.
- Asset sales, tax benefits, or pension income.
- Related-party transactions.
- Auditor changes.
- Material weaknesses, restatements, or SEC inquiries.
- Frequent changes to KPI definitions.

Working-capital releases can temporarily inflate FCF. Identify the structural and temporary portions.

## 11. Stock-Based Compensation, Dilution, and Buybacks

Collect:

- SBC amount.
- SBC / revenue.
- SBC / operating cash flow.
- Basic and diluted shares for at least three years.
- RSUs, options, warrants, convertibles, ATM programs, shelves, and recent offerings.
- Actual repurchase amount and shares retired.

Evaluate buybacks by **net share reduction**, not authorization announcements.

```text
Net share change = ending diluted shares / beginning diluted shares - 1
```

Ask:

- Did repurchases offset employee issuance?
- Were shares bought above reasonable value?
- Was debt increased to fund repurchases?
- Did diluted shares actually decline?

## 12. Valuation

Use multiple measures:

- NTM, FY1, and FY2 P/E.
- EV/EBITDA.
- EV/EBIT.
- EV/FCF.
- FCF yield.
- SBC-adjusted FCF yield.
- PEG.
- Five-year own-history median.
- Genuine peer median.

### Value-trap checks

A low multiple is not attractive when:

- earnings are at a cycle peak,
- orders or revenue are decelerating,
- EPS includes one-time tax or asset-sale gains,
- leverage is excessive,
- market share is structurally eroding,
- customer concentration is severe,
- EPS rises while FCF does not,
- dilution transfers value away from owners.

## 13. Return Scenarios

### Constant-multiple scenario

For an EPS-based candidate:

```text
Future price = future diluted EPS * current forward P/E
Upside = future price / current price - 1
CAGR = (future price / current price)^(1 / years) - 1
```

For other sectors, substitute the appropriate per-share metric and multiple.

### 20% multiple-contraction stress

```text
Stressed multiple = current multiple * 0.80
Stressed future price = future metric * stressed multiple
```

### Peer-median scenario

Use only when peers are economically comparable and the same metric basis is available.

```text
Peer case price = future metric * peer median multiple
```

The peer case is secondary. Never rank primarily on assumed re-rating.

## 14. Peer Selection

Choose three to five peers based on:

- business economics,
- customers and end markets,
- growth stage,
- recurring versus transactional revenue,
- margins,
- capital intensity,
- geographic mix.

Explain each peer choice. Do not use a faster-growing or unrelated company merely to make the target look cheap.

Compare:

- growth,
- margins,
- ROIC or sector return measure,
- leverage,
- FCF yield,
- SBC,
- dilution,
- forward valuation.

Classify the discount as:

- temporary and potentially resolvable,
- structural and difficult to resolve,
- justified by superior risk,
- unsupported because the peer set is weak.

## 15. Cyclicality

Rate cyclicality from 1 to 5:

1. Low economic sensitivity.
2. Mild sensitivity.
3. Moderate sensitivity.
4. High sensitivity.
5. Extreme cyclicality.

For cyclical companies analyze five to ten years when available:

- revenue,
- operating margin,
- EPS,
- FCF,
- orders and backlog,
- book-to-bill,
- inventory and utilization,
- customer and industry capex,
- commodity prices,
- price versus volume,
- recession drawdowns.

Calculate mid-cycle revenue, margin, EPS, and FCF when possible. Use normalized earnings for valuation, not peak earnings.

## 16. Latest-Earnings Assessment

Record:

- fiscal period and publication date,
- revenue and year-over-year / sequential growth,
- organic growth,
- gross and operating margins,
- GAAP and adjusted EPS,
- operating cash flow and FCF,
- capex and SBC,
- diluted shares,
- guidance changes,
- consensus differences,
- segment results,
- orders/backlog and sector KPIs,
- one-time items,
- working-capital and tax changes.

Classify the growth state:

- accelerating,
- stable,
- modestly decelerating,
- clearly decelerating,
- cycle bottoming,
- cycle peaking.

A headline beat does not override deteriorating guidance, cash flow, backlog, or core KPIs.

## 17. Catalysts, Risks, and Invalidation

Evaluate catalysts over six to 24 months and specify timing, probability, and likely mechanism.

Examples:

- growth reacceleration,
- end of inventory correction,
- order recovery,
- new product or capacity,
- margin improvement,
- debt reduction,
- actual buybacks,
- divestiture or spin-off,
- regulatory or litigation resolution.

Define the largest risk concretely. Write measurable invalidation conditions, such as:

- revenue growth below a threshold for two quarters,
- backlog declining year over year,
- gross margin below a threshold,
- NRR below a threshold,
- net leverage above a threshold,
- annualized dilution above a threshold,
- FCF turning negative,
- loss of a major customer,
- guidance withdrawal.

## 18. Fail-Closed Decision Policy

Do not rank a candidate when:

- critical snapshot data is stale,
- the valuation basis is inappropriate,
- source provenance is missing for load-bearing numbers,
- data-quality score is below the configured floor,
- a hard-exclusion flag is unresolved,
- future per-share estimates cannot be reconciled,
- peer or cyclical normalization is essential but unavailable.

Status values:

- `eligible`: enough evidence to rank.
- `review_required`: promising but unresolved evidence prevents final ranking.
- `screened_out`: active/researchable security that failed the broad economic screen.
- `excluded`: hard exclusion, inactive security, special-situation pricing, or invalid input.

A partial run or a run with unprocessed candidates is `provisional`. It may show completed candidate calculations but must not publish final-three selections.

## 19. Final Selection

Select up to three categories:

- Highest conviction.
- Most undervalued.
- Largest upside.

For each answer:

1. Why it qualifies.
2. Return from per-share growth alone.
3. What the market may be missing.
4. Most important catalyst.
5. Largest risk.
6. Best reason not to buy now.
7. Bear case.
8. Invalidation condition.
9. KPI to monitor next quarter.

The same company may occupy multiple categories. No candidate is preferable to a forced recommendation.

## Version 3.5 Candidate-Quality Improvements

- Use deterministic multi-lane sampling to improve discovery diversity and avoid selecting only one factor style.
- Apply formal quality gates after the upside screen so low-P/E/high-EV-FCF transition stories do not become automatic winners.
- Test low-consensus-case upside in addition to average consensus.
- Require independent, sourced driver provenance and reject target-solved bridges.
- Treat spin-offs and transformative M&A as pro-forma corporate transitions.
- Publish only self-contained, pre-audited run bundles.

### Referencia: references/migration-v1-to-v2.md

# Migration from Schema Version 1 to Version 2

## Breaking Change

Schema version 2 is intentionally fail-closed. A version 1 input cannot be converted by relabeling `schema_version`; it lacks evidence and period semantics needed to prevent false rankings.

## Required Changes

### 1. Add run metadata and funnel

Add `run_metadata`, `screening_funnel`, and explicit `partial`/`complete` status.

### 2. Replace self-attestation

Remove reliance on `research_completeness`. Add:

- candidate-level `evidence` map,
- resolving `sources` rows,
- field-specific source IDs.

A Boolean claim such as `forecast_bridge_verified: true` no longer earns quality credit.

### 3. Add corporate-action preflight

Create `corporate_action_check` with listing status, M&A status, active-symbol flag, timestamp, latest material event, and source IDs.

### 4. Normalize capex sign and TTM period semantics

Replace ambiguous `capex_ttm` with non-negative `capex_cash_outflow`. Select one TTM method:

- `reported_ttm`
- `sum_4_discrete`
- `fy_plus_current_ytd_minus_prior_ytd`

Do not sum overlapping YTD periods.

### 5. Separate standard and company-adjusted FCF

Use `cash_flow_ttm.standard_fcf` for OCF minus capex. Keep `company_adjusted_fcf` and its definition separate.

### 6. Classify cash

Replace a single cash value with:

- `corporate_cash`
- `marketable_securities`
- `customer_or_settlement_funds`
- `restricted_cash`

### 7. Replace flat valuation fields with period objects

Version 1:

```json
{
  "metric_basis": "gaap",
  "current_metric": 3.0,
  "year_2_metric": 4.2,
  "year_3_metric": 5.0
}
```

Version 2:

```json
{
  "periods": {
    "current": {"metric": 3.0, "metric_basis": "gaap", "period_kind": "fy1"},
    "year_2": {"metric": 4.2, "metric_basis": "gaap", "period_kind": "fy2", "years": 2},
    "year_3": {"metric": 5.0, "metric_basis": "gaap", "period_kind": "fy3", "years": 3}
  }
}
```

Add source type, retrieval timestamp, source IDs, analyst count, and estimate range to each period.

### 8. Add arithmetic forecast bridge

For each future metric, provide numerator, denominator, operating drivers, metric basis, and source IDs.

### 9. Reconcile adjusted metrics to GAAP

For every `company_adjusted` or `analyst_normalized` period, provide the GAAP metric plus labeled adjustment rows and sources.

### 10. Use the four-status model

- `eligible`
- `review_required`
- `screened_out`
- `excluded`

Ordinary economic screen failures belong in `screened_out`; completed M&A or inactive listing belongs in `excluded`.

## Migration Procedure

1. Preserve the original v1 JSON for audit.
2. Re-run corporate-action checks and quote freshness.
3. Re-read cash-flow periods and normalize capex signs.
4. Re-query consensus with explicit GAAP/adjusted basis.
5. Build forecast and reconciliation evidence.
6. Create v2 candidate checkpoints.
7. Run strict evaluation.

There is no automatic migration script because missing evidence cannot be reconstructed safely from a v1 file alone.

### Referencia: references/migration-v2-to-v3.md

# Migration from Schema v2 to v3

## Breaking Changes

Schema v3 makes the research run—not just each candidate—auditable and finalizable.

### New top-level requirements

- `market_context` must contain current numeric context and source IDs.
- `global_sources` must use the strict source ledger schema.
- `screening_audit` must reference or embed a hash-verifiable row-level universe artifact.
- `run_metadata.status = complete` is valid only when every selected broad-screen symbol has a candidate record.

### Source ledger

`supports` changed from an informal string to a required array:

```json
{"supports": ["latest_earnings", "financials.cash_flow_ttm"]}
```

Source `kind` and `tier` must be compatible. Third-party transcripts are not company IR.

### Latest earnings

Replace a single mixed record with separate records:

```json
{
  "latest_report_type": "annual",
  "quarter": {"period_type": "quarter", "period": "Q4 FY2026"},
  "full_year": {"period_type": "full_year", "period": "FY2026"}
}
```

### Formal valuation basis

The current formal period must be `ntm` or `fy1`. A TTM metric may be supplemental but cannot drive the constant-multiple ranking scenario.

### Estimate breadth

A consensus horizon with fewer than the configured minimum analysts is supplemental unless accompanied by a fully sourced independent model.

### Cash and EV/FCF

EV now uses:

```text
market cap + total debt - corporate cash - eligible marketable securities
```

Customer/settlement funds and restricted cash are excluded from shareholder-available cash.

### New sector controls

- Commercial biopharma concentration may be derived from product and total revenue.
- Near-LOE concentrated franchises receive 6x and 8x stress scenarios.
- Auto dealerships require floorplan-adjusted leverage.
- Payments require corporate/settlement cash separation.

### New scripts and flags

- `screen_universe.py`: complete row-level broad-screen audit.
- `research_contract.py`: schema-v3 validation.
- `evaluate_candidates.py --require-final`: exit 2 for a provisional or globally invalid run after writing diagnostics.

## Migration Procedure

1. Create current market context and global source files.
2. Run the broad-screen audit script.
3. Initialize a new v3 run; do not mutate a v2 state directory in place.
4. Convert earnings records and forward periods.
5. Correct source `supports` types and source classifications.
6. Reconcile cash/debt and forward forecast bases.
7. Save every selected candidate.
8. Run strict evaluation with `--require-final`.

### Referencia: references/migration-v3-to-v3.1.md

# Migration Guide — v3.0 to v3.1

## Why v3.1 Exists

A v3.0 execution correctly refused to publish a ranking, but it failed operationally because it required near-complete financial coverage for the full market, silently used a reduced USD 10B–20B universe, selected unresolved sector-review rows using equal placeholder scores, and produced inconsistent selected/unprocessed state. The distributed standalone package also differed from the package embedded in the repository overlay.

```text
Top-level snapshot schema: 3
Screening audit schema: 3 / contract revision 3.1
Run-state schema: 2
Skill version: 3.1.0
```

v3.1 keeps the strict primary-source, accounting, and forward-valuation controls while replacing the impossible market-wide financial-completeness requirement with a two-layer coverage model.

## Required Changes

### Screening artifacts

Old single artifact:

```text
broad-screen-results.jsonl
```

v3.1 artifacts:

```text
universe-audit-results.jsonl
broad-screen-results.jsonl
enrichment-queue.json
broad-screen-audit.json
broad-screen-shortlist.json
```

### Audit metadata

```text
audit_schema_version: 3
contract_revision: 3.1
candidate_pool_status: sufficient | no_qualifying_candidates | insufficient_data
selection_outcome: selected | no_candidates | insufficient_data
```

### Checkpoint attachment

Replace the legacy single `--artifact` invocation with:

```bash
--universe-artifact .../universe-audit-results.jsonl \
--candidate-artifact .../broad-screen-results.jsonl
```

### Plan-gated fundamentals

Do not abandon the run or demand a paid endpoint. Build a transparent stratified discovery pool with `build_discovery_pool.py`, enrich that bounded pool with available estimates/fundamentals, and rerun `screen_universe.py`.

### Status migration

| v3.0 behavior | v3.1 behavior |
|---|---|
| Missing full-universe financial fields counted as global audit failure | Missing candidate-pool economics become `needs_enrichment` |
| Review-only rows could share a placeholder score | Review rows use `broad_score=null` and cannot be selected |
| Listing-only pool could be mistaken for no candidates | `insufficient_data`; final no-candidates conclusion prohibited |
| Reduced provider scope could continue | Scope marked incomplete; final contract blocked |
| Selected count could disagree with unprocessed state | `unprocessed = selected - verified` invariant enforced |

## Package Migration

1. Replace the entire skill directory; do not mix v3.0 and v3.1 scripts or assets.
2. Start a new run directory and regenerate both audit layers.
3. Remove the old standalone package.
4. Install only the v3.1 package whose SHA-256 matches the package embedded in the v3.1 overlay.

### Referencia: references/migration-v3.1-to-v3.2.md

# Migration v3.1 → v3.2

## Why v3.2 Exists

A v3.1 live run produced `ranking_status=final` and `no_qualifying_candidates` while 15 candidate-pool rows remained in an enrichment queue and `candidate_pool_exhausted=false`. The direct cause was a completion shortcut based on minimum attempted/evaluable counts. The same run also failed to advance strong cyclical/high-growth rows, treated growth guidelines as mechanical cutoffs, hid broad-screen review/failure rows in Markdown, and accepted universe/macro freshness evidence that was too weak.

v3.2 removes those paths.

## Version Changes

```text
Skill version: 3.2.0
Top-level snapshot schema: 3
Screening audit schema: 3
Screening contract revision: 3.2
```

## Breaking Audit Changes

v3.1 broad-screen audit artifacts are not valid v3.2 evidence. Regenerate:

```text
universe-audit-results.jsonl
broad-screen-results.jsonl
enrichment-queue.json
broad-screen-audit.json
broad-screen-shortlist.json
```

### New scope proof

`scope.enumeration` is required:

```json
{
  "verified": true,
  "provider_reported_total": 1786,
  "rows_fetched": 1786,
  "pages_fetched": 18,
  "pagination_exhausted": true,
  "band_audit": [],
  "bands_verified": false
}
```

### New enrichment proof

```json
{
  "attempted_count": 120,
  "resolved_count": 118,
  "unresolved_count": 2,
  "resolution_pct": 98.3333,
  "all_rows_resolved": false,
  "candidate_pool_exhaustion_declared": false,
  "candidate_pool_exhausted": false,
  "candidate_pool_covers_in_scope": false,
  "queue_count": 2,
  "queue_symbols": ["BBB", "CCC"]
}
```

Attempted is not resolved.

### New candidate-pool coverage proof

A market-wide no-candidates conclusion requires the economic candidate pool to represent every in-scope listing symbol:

```json
{
  "in_scope_covered_count": 1786,
  "in_scope_missing_count": 0,
  "in_scope_missing_symbols": [],
  "coverage_complete": true
}
```

`candidate_pool_exhaustion_declared=true` is an operator/agent declaration. `candidate_pool_exhausted=true` is emitted only after the script independently confirms full in-scope coverage and zero unresolved rows.

### New candidate-pool statuses

```text
sufficient
sufficient_pending_enrichment
no_qualifying_candidates
insufficient_data
```

A final no-candidates outcome requires coverage of every in-scope listing symbol, explicit pool exhaustion, zero unresolved rows, an empty queue, all final dispositions, and at least one economically assessable row.

## Candidate Decision Changes

- Growth and preferred valuation thresholds are soft guidelines.
- `near_miss_review` may advance when valuation and per-share growth justify deeper work.
- P/E 21–30 high-growth exceptions remain eligible.
- Cyclical normalization is nonblocking for broad selection; the selected deep dive must calculate mid-cycle economics before ranking.
- Bank/REIT/BDC/MLP valuation and auto-dealer floorplan-adjusted leverage remain blocking.
- `unavailable_after_enrichment` requires a specific reason and resolving source IDs.
- Enrichment queue ordering is GARP-priority based, with liquidity only a tiebreaker.

## Source and Market-Context Changes

- Dynamic market fields use `data_as_of` or publication date for freshness.
- Policy, Treasury, inflation, and GDP require official support.
- Market-implied rate-path statements require explicit source support or a sourced analyst inference.

## Report Changes

Markdown now separates:

- broad selected,
- deferred by budget,
- unresolved/review,
- unavailable after enrichment,
- broad screened out,
- broad excluded,
- deep-dive ranked/review/screened-out/excluded.

An empty deep-dive set no longer hides nonzero broad-stage dispositions.

## Upgrade Procedure

1. Replace the complete `skills/us-undervalued-growth-screener/` directory. Do not mix v3.1 and v3.2 scripts or assets.
2. Replace the committed `.skill` package with the package generated from the same v3.2 source tree.
3. Add/update the `skills-index.yaml` entry from `snippets/skills-index-entry.yaml`.
4. Discard or migrate old run-state/audit artifacts; do not resume a v3.1 broad-screen audit.
5. Re-enumerate the listing universe with pagination/band exhaustion proof.
6. Rebuild and enrich the bounded candidate pool.
7. Run the v3.2 tests and strict final smoke test.
8. Verify standalone and overlay-embedded `.skill` SHA-256 values are identical.

### Referencia: references/migration-v3.2-to-v3.3.md

# Migration v3.2 → v3.3

## Why v3.3 Exists

A live run intended for v3.2 was generated by a stale v3.1 runtime. Subsequent review also found that forecast bridges could be circular, commercial biopharma aliases could bypass LOE stress, peak-profit risk could avoid normalization, and data quality could remain too high without cash, TTM-period, ROIC, or EBITDA evidence.

v3.3 makes those failures mechanically detectable.

## Breaking Changes

```text
skill version: 3.3.0
snapshot schema: 3
screening audit schema: 3
contract revision: 3.3
runtime fingerprint: ug-v3.3-driver-bridge-bounded-pool-20260828
```

Old audits and snapshots are not resumable. Regenerate them.

## Required Changes

1. Replace the complete skill directory and `.skill` package from the same release.
2. Verify all helper scripts with `--version`.
3. Regenerate listing, discovery, broad-screen, checkpoint, and final artifacts.
4. Add `runtime` metadata to every audit/snapshot.
5. Add a valid generation audit for bounded pools.
6. Rebuild forecasts from operating drivers rather than a preselected numerator.
7. Add TTM-period source IDs, cash classification, ROIC/EBITDA evidence, and sector/cycle evidence.
8. Use normalized `commercial_biopharma` sector semantics or a supported alias.
9. Rerun all tests and the strict final smoke test.

## Candidate Data Changes

- Forecast drivers now require sufficient information to independently calculate the metric.
- Adjusted forecasts must tie both GAAP and adjustment portions to the reconciliation.
- Cash classification records `corporate_cash`, eligible marketable securities, restricted/customer funds, and normalization method.
- TTM cash-flow methods require source IDs for reported TTM or each construction period.
- `peak_profit_risk=true` requires normalization.
- Commercial biopharma requires product concentration and LOE evidence.

## Package Migration

Delete any installed same-name older skill before installing v3.3. Confirm the package SHA-256 and `--version` output after installation. Do not trust a filename alone.

### Referencia: references/migration-v3.3-to-v3.4.md

# Migration v3.3 → v3.4

## Why this release is breaking

A live v3.3 run exposed five discovery/orchestration defects:

1. the default USD 500M–20B request was silently rewritten to USD 3B–4B;
2. one session's volume was labeled as average daily dollar volume;
3. a pre-operating company without FY1 estimates appeared at roughly 4x using distant outer-year EPS;
4. five deterministic selections were later proposed to be reduced to two without rerunning the screen;
5. the workflow again asked the user for a separate “continue” turn.

v3.4 makes these conditions fail closed.

## Required input changes

### Liquidity

Discovery rows need one of the supported 20+ session average-liquidity forms, plus source IDs:

```json
{
  "average_daily_dollar_volume": 12000000,
  "average_daily_dollar_volume_method": "provider_average_dollar_volume",
  "average_volume_period_days": 20,
  "liquidity_source_ids": ["quote-source"]
}
```

Raw single-session `volume` is ignored for ADDV.

### Current forward valuation

`forward_pe` alone is no longer accepted. Use `normalize_estimates.py` or supply dated NTM/FY1 metadata, positive EPS, analyst count, source IDs, and price/EPS reconciliation.

### Scope

The default user request remains USD 500M–20B. Internal budget pressure cannot turn a single band into the request. A genuinely narrower user request needs explicit authorization evidence and matching requested/executed bounds.

### Selected-set commitment

Every Broad Screen-selected symbol must receive a verified terminal candidate record. Change the deep-dive budget only by rerunning `screen_universe.py`; omitted eligible names then become `deferred_by_budget` deterministically.

## Upgrade steps

1. Replace the full `skills/us-undervalued-growth-screener/` directory.
2. Replace `skill-packages/us-undervalued-growth-screener.skill`.
3. Remove stale installed/cached copies of the same skill name.
4. Verify the five runtime entry points with `--version`.
5. Rebuild discovery liquidity from provider average volume or a 20+ session series.
6. Normalize dated annual estimates through `normalize_estimates.py`.
7. Discard v3.3 audits, checkpoints, and snapshots.
8. Run the skill tests, index validation, package-drift checks, and repository CI.

### Referencia: references/migration-v3.4-to-v3.5.md

# Migration v3.4 → v3.5

## Breaking changes

1. Runtime identity is now `3.5.0 / contract 3.5 / ug-v3.5-multilane-quality-bundle-20260828`.
2. Default deep-dive budget is five and uses multi-lane selection.
3. Candidate metrics must retain `average_volume` and `liquidity_source_ids`.
4. Provider-side share-volume filters prevent a full-listing enumeration claim.
5. Forecast bridges require `construction_method=independent_driver_model` and per-driver provenance with `target_solved=false`.
6. Discrete/YTD/reported TTM cash-flow evidence requires exact support paths.
7. Recent spin-offs and transformative M&A use `corporate_transition`, not `identity.special_case`.
8. Formal eligibility has score, FCF, ROIC, leverage, dilution, low-case, and LOE quality gates. A new `conditional` status is available.
9. Final-three categories are nullable and use category-specific thresholds.
10. Final publication requires `prepublish_audit.py` and `bundle_run_artifacts.py`.

## Candidate migration

Add driver provenance under every year-2/year-3 bridge:

```json
{
  "construction_method": "independent_driver_model",
  "driver_provenance": {
    "revenue": {
      "origin": "market_consensus",
      "source_ids": ["consensus-source"],
      "target_solved": false
    }
  }
}
```

Add exact cash-flow supports to source rows:

```text
financials.cash_flow_periods.<period-end>
financials.ttm_reconstruction.<component>
financials.cash_flow_ttm.reported_ttm
```

## Run migration

Discard v3.4 audits/checkpoints; their fingerprint is intentionally incompatible. Re-run runtime preflight, Broad Screen, candidate verification, strict evaluation, prepublication audit, and bundle generation.

### Referencia: references/migration-v3.5-to-v3.6.md

# Migration v3.5 → v3.6

v3.6 changes the preferred execution architecture while retaining schema 3 and the contract-3.5 underwriting/evaluation semantics.

## Runtime identity

```text
skill_version       = 3.6.0
schema_version      = 3
contract_revision   = 3.5
runtime_fingerprint = ug-v3.6-claude-code-direct-fmp-20260829
```

Do not reuse v3.5 audits or checkpoints. The evidence schema is compatible, but runtime identity is intentionally different so a cached package cannot be mistaken for the direct-FMP release.

## New preferred path

```bash
export FMP_API_KEY="..."
python3 skills/us-undervalued-growth-screener/scripts/run_pipeline.py \
  --config skills/us-undervalued-growth-screener/assets/claude-code-config.example.json \
  --output-dir reports/us-undervalued-growth-screener
```

The runner keeps bulk FMP responses on disk, uses a persistent SQLite cache, normalizes FY1 estimates, validates 20-day ADDV, builds the four discovery lanes, and prints only a compact run summary. Claude Code then reads selected candidate packets and performs the existing SEC/IR underwriting and strict final sequence.

## Reused central infrastructure

The skill's `fmp_client.py` is generated from the repository-level `scripts/fmp_client/` source of truth. Regenerate and verify it with:

```bash
python3 scripts/generate_fmp_client.py
python3 scripts/generate_fmp_client.py --check
```

## New files

- `scripts/fmp_client/specials/garp.py.tmpl`
- generated `skills/us-undervalued-growth-screener/scripts/fmp_client.py`
- `skills/us-undervalued-growth-screener/scripts/run_pipeline.py`
- `skills/us-undervalued-growth-screener/assets/claude-code-config.example.json`
- `skills/us-undervalued-growth-screener/references/claude-code-execution.md`
- `commands/us-undervalued-growth-screen.md`

## Operational changes

- Direct FMP HTTP calls replace bulk FMP MCP calls in Claude Code.
- Adaptive market-cap-band splitting prevents silent company-screener truncation.
- Bulk analyst-estimate and EOD endpoints are attempted first; bounded per-symbol fallbacks remain available.
- Exact liquidity work is allocated by GARP opportunity lane.
- Raw provider payloads are never printed to stdout and should not be loaded into model context.
- The Claude Code default deep-dive commitment is three names.
- `evaluate_candidates.py`, `prepublish_audit.py`, and `bundle_run_artifacts.py` remain the publication gates.

### Referencia: references/migration-v3.6-to-v3.6.1.md

# Migration v3.6 → v3.6.1

v3.6.1 hardens the bounded per-symbol fallback that runs when FMP bulk endpoints are plan-gated (HTTP 402). Schema 3 and contract 3.5 are unchanged; the discovery stage gains an honest scope vocabulary, a stratified seed with a documented selection basis, a pre-selection quality probe, and a persistent endpoint-capability cache.

## Runtime identity

```text
skill_version       = 3.6.1
schema_version      = 3
contract_revision   = 3.5
runtime_fingerprint = ug-v3.6.1-claude-code-direct-fmp-20260830
```

Runtime identity is intentionally different from v3.6.0. Do not mix v3.6.0 audits, packets, or checkpoints with v3.6.1 artifacts; rerun discovery.

## Why

A live run on 2026-08-30 (2,371 listings, all five bulk endpoints 402) showed that the fallback seeded 80 of 2,371 names with no economic data at seed time, that the within-cell ranking saturated at USD 100M/day and fell back to ticker order for large caps, that `provider_exhausted=true` was passed unconditionally, that `scope_complete=true` was read as economic coverage, and that a name with EV/FCF 126x reached the deep-dive slots because no FCF evidence existed before selection.

## Behavioural changes

### Seed selection (`diversified_seed`)

- Cells are sector × market-cap bucket. Quota per cell ∝ √(cell size), reconciled to the seed limit with Hamilton apportionment; every non-empty cell gets at least one seat. The result is independent of cell iteration order.
- Within a cell: `pre_enrichment_score` desc → raw single-day dollar volume desc → market cap desc → fewer missing price/volume fields → `sha256(analysis_date:symbol)`. The raw ticker string is never a tie-break. The log10 dollar-volume term is no longer capped.
- `audit/seed-audit.json` (also embedded in `provider-prefilter-audit.json` and `run-summary.json`) records `seed_selection_basis` (`stratified_liquidity_proxy` when economic fields are absent for the majority of rows), `economic_metrics_available_for_seed`, `cell_count`, `quota_method`, tie-break counters, and the configured/effective seed limits.

### Dynamic seed limit

New config keys with defaults: `pre_enrichment_limit: 180` (was 80), `seed_limit_cap: 200`, `quality_probe_limit: 35`, `candidate_packet_reserve_calls: 30`, `retry_reserve_calls: 25`.

```text
reserved  = quality_probe_limit + exact_liquidity_limit
          + candidate_packet_reserve_calls + retry_reserve_calls
effective = min(pre_enrichment_limit, seed_limit_cap,
                max_api_calls - api_calls_made - reserved)
```

An effective limit below 20 fails the run with `estimate seed budget insufficient` instead of silently producing a thin pool. The probe reserve is counted twice per target (key metrics + annual income statement).

### Quality probe before pool selection

After estimate normalization, the union of lane rows is ranked by best lane score and the top `quality_probe_limit` symbols receive one `key-metrics-ttm` call each. Rows gain `roic_pct`, `fcf_yield_pct`, `ev_to_fcf`, `net_debt_to_ebitda`, `sbc_revenue_pct`, and `sbc_adjusted_fcf_yield_pct` (computed on the market-cap basis: FCF yield − SBC/revenue × revenue/market cap). `audit/quality-probe-audit.json` records attempts, resolutions, and calls used.

Lane scores now include an FCF-yield term (weight 1.0 core_garp / quality_near_miss, 0.5 high_growth_exception) and a leverage penalty above 2.5x net debt / EBITDA. A probe-resolved row with SBC-adjusted (or standard) FCF yield below 1% is excluded from every lane except `high_growth_exception`, where it stays with `provider_prefilter_flags: ["weak_fcf_support"]` and a −10 score. Exclusions are listed under `fcf_prefilter_excluded_symbols` in the discovery audit.

### Honest scope fields

Route selection and completeness are separate thresholds: the bulk route is used from `bulk_estimate_minimum_coverage_pct` (20%), but `economic_screen_scope_complete` / `economic_candidate_universe_exhausted` are true only when the bulk estimates covered every listing-universe symbol (exact count equality, `covered_symbol_count >= universe_symbol_count`; deliberately not a configurable ratio, so no setting can declare a partially covered run complete). A 25%- or even 99%-covered bulk run is a bounded economic screen, exactly like the per-symbol fallback.

`run-summary.json` and `NEXT_ACTION.json` add `listing_enumeration_complete`, `economic_screen_scope_complete`, `listing_universe_count`, `estimate_seed_count`, `estimate_seed_coverage_pct`, `valid_estimate_count`, `valid_estimate_coverage_pct`. `scope_complete` is retained for readers of v3.6.0 output and now carries `scope_complete_deprecated_note`. The discovery audit adds `listing_provider_exhausted`, `estimate_seed_exhausted`, `economic_candidate_universe_exhausted`, and `provider_exhausted_scope` (`estimate_seed` on the fallback path). The contract-validated `screening_audit.scope` block is unchanged.

### Growth basis

**Actuals are verified or absent, and growth is compared on one basis.** `latest_actual_eps` is populated only from (a) a provider row explicitly marked as actual whose period has ended AND whose publication timestamp is at or before `analysis_as_of` (rows without a provable publication time are rejected — a current snapshot replayed against a historical as-of must not leak later-published actuals), or (b) the annual income statement fetched during the quality probe whose `acceptedDate` (with time of day; the date-only `filingDate` is never accepted) is at or before `analysis_as_of` (`latest_actual_verified: true`, `latest_actual_basis: gaap_diluted`, `latest_actual_source_ids`). An unmarked prior-year estimate row is never reported as an actual; it is exposed as `fy0_consensus_eps` and, because it shares the provider's (usually adjusted) basis with FY1/FY3, it is the comparator for `current_year_growth_pct`, `fy1_eps_below_fy0_consensus`, and `growth_pattern` (`growth_pattern_basis: consensus_same_basis`; `unknown` without a prior-year row). The GAAP actual is reported alongside (`current_year_growth_pct_vs_gaap_actual`, `fy1_eps_below_latest_actual`) and, when it differs from the FY0 consensus by more than 15%, `estimate_basis_likely_adjusted: true` warns that GAAP-vs-consensus comparisons are mixed-basis. Found on DOCS: FY1 non-GAAP consensus $1.35 vs GAAP actual $0.98 looked like a decline; same-basis FY26 non-GAAP $1.52 → $1.35 is the real (and still negative) comparison.

`normalize_estimates.py` adds `latest_actual_eps`, `latest_actual_period_end`, `fy1_eps_below_latest_actual`, `current_year_growth_pct`, `eps_growth_fy1_to_fy3_pct` (alias of `eps_growth_pct`), `eps_growth_actual_to_fy3_pct`, `growth_pattern` (`steady | accelerating | trough_recovery | declining | unknown`), and `growth_basis_source_ids`. A `trough_recovery` row is removed from `core_garp` and admitted to `quality_near_miss` with the `earnings_recovery` flag.

### Deep-dive selection with a small budget

`screen_universe._selection_lane` now also routes `growth_pattern == trough_recovery` rows to `quality_near_miss` (the pool-stage rule alone did not reach the final lane). When `max_deep_dive_candidates` is smaller than the lane plan total (default 2/1/1/1 = 5), selection walks the priority order and treats each lane quota as a cap instead of filling lanes in plan order; with a 3-name budget the best cyclical can now win a slot rather than every slot going to the first two lanes. Budgets at or above the plan total keep the lane-first fill.

### Cyclicality and foreign private issuers

Gold, silver, precious/base metals, copper, uranium, coal, metals & mining, and mineral names classify as cyclicality 4; aluminum and semiconductor equipment as 3 (the bare `semiconductor` needle was removed so equipment names do not inherit 4). Rows whose ISIN prefix (or, failing that, listing country) is not `US` carry `foreign_private_issuer_review`, and their packets add `form_20f_6k_verification` to `required_next_checks`. Neither flag excludes a name.

### Pool floor and sector profiles (round-4 review)

- `build_provider_prefilter_pool` waives the minimum-pool row floor only when `provider_exhausted_scope` is a full exhaustion (`economic_candidate_universe` or `full_input`). The per-symbol fallback passes `estimate_seed`, which never waives the floor; `pool_floor_waived` is recorded in the audit. Round-5 hardening removed the legacy missing-scope waiver: an unstated scope now fails closed.
- `normalize_listing` infers `sector_profile_type` (reit / insurance / bank / asset_manager / bdc / mlp / auto_dealership) from sector+industry text, so `screen_universe`'s existing sector gates actually fire: such names without sector-specific valuation evidence go to `sector_specific_valuation_required`, and the general-company `excessive_leverage` hard gate is skipped for them (a mortgage REIT at 13x net debt/EBITDA is normal, not a failure). On the direct-FMP path such rows are then declared enrichment-exhausted (the provider cannot supply P/FFO-AFFO, P/TBV, or adjusted leverage) and resolve as `unavailable_after_enrichment` -- audited and excluded from selection, available for manual sector underwriting in a scoped follow-up.
- The Markdown report renames "Universe scope" to "Listing enumeration" and adds an "Economic estimate coverage" line (mode, covered/universe counts, conclusion scope), so the bounded economic scope is visible in prose, not only in JSON.

### Unit reconciliation, taxonomy map, and the ET filing clock (round-5 review)

- Foreign issuers (non-US ISIN prefix or listing country) are now blocked from selection unless `unit_reconciliation_verified: true` with currency/ADS-unit evidence: a USD ADS price against local-currency statements produced QFIN at forward P/E 0.45x and 94% FCF yield — a unit mismatch, not deep value. On the direct-FMP path such rows are declared enrichment-exhausted and resolve as `unavailable_after_enrichment`. Independent circuit breakers stop implausible ratios on any issuer (`minimum_plausible_forward_pe` 2.0, `maximum_plausible_fcf_yield_pct` 50, reported EPS > 2x price) as `unit_mismatch_suspected`.
- Sector-profile inference now uses an explicit map over real FMP taxonomy labels instead of substring needles: `Auto - Dealerships` maps to `auto_dealership` (the old needle never matched it), `Investment - Banking & Investment Services` maps to `capital_markets` (labelled, valued on ordinary multiples — never the deposit-bank gate), `Banks - *` prefixes map to `bank`, and BDCs are caught by industry (`Business Development ...`) or company-name needles, with `sector_profile_overrides` in config to pin names the listing frame cannot classify (e.g. `{"ARCC": "bdc"}`).
- FMP `acceptedDate` / naive publish stamps are US/Eastern (the SEC acceptance clock), not UTC: a 17:23 ET acceptance read as UTC leaked the filing 4-5 hours early. Both `_verified_annual_actual` and the consensus publish check convert from `America/New_York`; date-only publish stamps count only after the whole publication day (ET) has passed.
- The scope-less pool-floor waiver was removed (fail closed; see the round-4 section above).

### Fail-closed unit context, actual attempt counts, capital_markets exemption (round-8 review)

- The unit gate is inverted from "block what is proven foreign" to "exempt only what is proven domestic": the shared `requires_unit_reconciliation()` (in `screen_universe`, used by both discovery's exhaustion marker and the screen's blocking gate) demands reconciliation evidence whenever the country is missing or non-US, the currency is non-USD, the ISIN is non-US, or the row is an ADR/ADS. `normalize_listing` now preserves `isin` and `is_adr` so those signals survive into the pipeline — a provider dropping the country field can no longer route a CNY-denominated row through as domestic.
- Discovery records the ACTUAL attempted count (`economic_attempt_count = len(estimate frame)`) in the generation audit; the evaluator copies it and fails closed to `diagnostic` when the field is missing, zero, or exceeds the universe (a 180 seed LIMIT over a 50-name universe must never display 360% coverage).
- `capital_markets` (advisory/investment banking) is excluded from the sector-enrichment exhaustion marker: only profiles the screen actually blocks (`SECTOR_PROFILES` + `auto_dealership`) are declared provider-unservable.

### Honest ranking scope (round-6 review)

- Listing 2,371 names and economically comparing 2,371 names are different claims: a run that attempted estimates for 180 seeds (98 evaluable, 4.1% of the universe) is a **scoped pilot**, not a market ranking, and the remaining ~96% are *unexamined*, not rejected. Every run now carries a tri-state `ranking_scope` — `final_marketwide` (estimate acquisition attempted for every listed symbol, exact counts), `final_scoped` (a bounded, fully processed subset; conclusions bind only to it), or `diagnostic` (unresolved queue) — plus per-stage coverage counts and percentages (`economic_attempt_*`, `economically_evaluable_*`, `quality_probe_*`, `deep_dive_*`) in the run summary and report JSON.
- The report title, scope banner, and the no-qualifying-candidates conclusion state the subset explicitly ("Scoped Pilot (180 of 2,371 listed names economically attempted)"; "the remaining names were never economically compared").
- `final_marketwide` is currently unreachable on the direct-FMP Starter path by design: reaching it requires the v3.7 sharded full-universe estimate collection (persistent snapshot store, ~8 deterministic shards within the per-run call budget) tracked as a follow-up issue, together with a discovery-recall gold-set harness (Recall@K against known past candidates).

### Endpoint capability cache

The generated client remembers a 402/403 bulk response in the SQLite cache (`capability:<url>`, 30-day TTL) and pre-disables that endpoint on later runs without spending a call. `respect_capability_cache=False` re-probes unconditionally. Diagnostics add `capability_cache_hits` and `remaining_calls`.

## Operator checklist

1. Build `market-context.json` and `global-sources.json` **before** running `run_pipeline.py`; every source `retrieved_at` must precede `analysis_as_of`.
2. Run discovery, then `manage_run_state.py init` / `set-screening-audit` / `set-funnel --preflight-passed-count N`.
3. `set-screening-audit` now copies the enrichment queue and provider-prefilter pool into `run/audit/` and rewrites their paths to the same run-relative base as the universe/candidate artifacts, and `prepublish_audit.py` also accepts audit-relative bare names, so `--artifact-root <run>` resolves every artifact from one root.
4. Keep shared `fmp-*` source entries byte-identical across candidate ledgers and the global ledger.

### Referencia: references/original-prompt-mapping.md

# Source Prompt Coverage Map

The original Japanese prompt remains the methodological authority. The skill reorganizes it into progressive research instructions, a source-linked schema, deterministic calculations, audit statuses, and tests.

| Original prompt area | Skill implementation |
|---|---|
| Undervalued growth rather than low P/E | `SKILL.md` overview; methodology objective; minimum constant-multiple upside gate |
| NYSE/Nasdaq/NYSE American and USD 500M–20B focus | scope/configuration and screening funnel |
| Exclusions and liquidity | corporate-action preflight, flags, liquidity gates, hard-exclusion log |
| SEC/IR source priority | evidence map, source ledger, research checklist, data-quality weights |
| Consensus date/period/type/analyst count | separate current/year-2/year-3 valuation records |
| Price timestamp/session and post-event consistency | common price basis, latest-event timestamp, stale-data gate |
| Revenue, EPS, FCF-per-share growth | historical CAGRs and forward per-share periods |
| ROIC, margins, leverage | normalized financials and score components |
| Standard FCF = OCF − capex | non-negative capex convention and three TTM reconstruction methods |
| Company-adjusted FCF disclosure | separate supplemental field and definition; never substitutes for standard FCF |
| GAAP vs non-GAAP | per-period metric basis and arithmetic GAAP reconciliation |
| SBC, dilution, and actual buybacks | SBC/FCF metrics, diluted-share history, explicit penalties |
| Three-to-five genuine peers | sourced peer rows, basis/period validation, peer-median scenario |
| Strict cyclical review | sourced normalization object and fail-closed gate |
| Latest earnings and growth-state classification | latest-earnings object and full report section |
| Sector-specific KPI rules | sector profile; commercial-biopharma LOE and payments cash/take-rate controls |
| Earnings/accounting quality | TTM reconstruction, working-capital review, source checklist |
| Constant multiple, 20% contraction, peer median | deterministic evaluator |
| EPS/FCF forecast construction | numerator/denominator bridge, drivers, arithmetic tolerance |
| Why discounted and market may be right | qualitative contract and report section |
| Catalysts, risk, and invalidation | detailed candidate and final-three sections |
| 100-point ranking | seven preserved score components plus deterministic penalties |
| Complete output contract | full Markdown renderer and structured JSON |
| Do not guess or force recommendations | null contract, evidence gates, review status, no-qualifier result |
| Preserve incomplete work honestly | checkpoint manager and provisional partial-run status |

## Version 2 Enhancements

1. Corporate-action preflight runs before detailed financial research, catching completed acquisitions and inactive symbols early.
2. Data-quality points require resolving evidence and arithmetic; self-attested completeness flags are ignored.
3. Capex sign convention is explicit and negative normalized outflows fail closed.
4. TTM OCF/capex supports four discrete quarters or FY+YTD−prior YTD without double-counting cumulative statements.
5. Standard FCF and company-adjusted FCF are separate.
6. Corporate cash is separated from customer/settlement and restricted funds.
7. Current, year-2, and year-3 accounting bases are stored separately; mixed bases block scenarios.
8. Adjusted/normalized periods require GAAP reconciliation.
9. `screened_out` is distinct from hard `excluded`.
10. Long runs checkpoint every candidate and can resume.
11. Partial coverage produces a provisional report with no final-three claims.
12. Commercial-biopharma LOE and payments take-rate/cash controls are explicit.
13. Full Markdown output now follows all major sections of the original prompt.
14. Synthetic tests cover evidence, FCF, period basis, corporate actions, sector controls, partial runs, and packaging behavior.

## Version 3 Review-Driven Controls

| Original requirement | v3 implementation |
|---|---|
| Current market valuation, rates, economy, sector cycle | Mandatory sourced `market_context`; placeholders/future dates rejected |
| Latest price and latest earnings | Quote/event timestamp gate; latest quarter and full year separated |
| Forward P/E constant-multiple analysis | NTM/FY1 current metric required; TTM supplemental only |
| Do not uncritically use consensus | Analyst-count/range and rankable-horizon controls; forecast bridge required |
| Compare 3–5 peers | Same-basis sourced peer gate |
| Do not mechanically reject 21–30x high growers | Broad-screen high-growth exception |
| Industry-specific leverage | Auto-dealer floorplan-adjusted leverage gate |
| Product concentration and structural risk | Derived/sourced commercial-biopharma concentration and LOE stress |
| Important numbers need source/period/retrieval date | Strict source ledger with typed `supports` arrays |
| Scope and candidate counts | Full listing audit plus bounded candidate-pool artifact, explicit scope, enrichment counts, and SHA-256 |
| Do not recommend when conditions are unmet | `--require-final`, no final-three on provisional runs, explicit no-candidate result |

## Version 3.1 Execution Controls

| Original requirement | v3.5 execution implementation |
|---|---|
| Screen the major US exchanges, with emphasis on USD 500M–20B | Full listing-universe audit records requested and retrieved bounds; reduced scope is disclosed and cannot silently complete |
| Do not guess missing numbers | Missing discovery data is `needs_enrichment`; no placeholder zeros or scores |
| Use multiple metrics but respect industry characteristics | General-company candidate screen plus explicit sector-review routing for banks, REITs, insurers, BDCs, MLPs, cyclicals, and auto dealers |
| Do not force ten recommendations | Deep-dive set is bounded; evidence-based `no_candidates` is a valid final result |
| Important data must be current and sourced | Full listing source, candidate-estimate source, SEC/IR sources, artifact hashes, and timestamps are separate |
| Conditions not met means no recommendation | `insufficient_data` triggers more discovery; it is never relabeled as “no candidates” |
| Complete the task from the screening request | Plan-gated bulk statements automatically route to provider-prefilter or stratified estimate enrichment before selected-name primary-source underwriting |

## Version 3.3 Evidence and Runtime Controls

| Original requirement | v3.5 implementation |
|---|---|
| Do not mix old and current data/processes | Runtime version, contract, schema, and fingerprint are embedded and hard-validated. |
| Do not uncritically use consensus | EPS/FCF is independently rebuilt from operating drivers; circular numerator checks fail. |
| Distinguish GAAP and adjusted forecasts | Driver-derived GAAP and after-tax adjustments separately tie to the reconciliation. |
| Standard FCF and source period integrity | TTM construction method and every component-period source are verified. |
| Do not overstate cash or EV/FCF | Corporate cash normalization and customer/restricted-fund separation feed evaluator-calculated EV. |
| Treat product concentration/LOE structurally | Biopharma aliases normalize to commercial-biopharma and require concentration/LOE/6x/8x stress. |
| Do not use peak cyclical profits | `peak_profit_risk=true` forces sourced normalization even with a low numeric cycle score. |
| Important numbers need sources | ROIC, EBITDA, cash, TTM periods, sector evidence, and forecasts affect quality points and caps. |
| Do not overclaim scope | Audited bounded pools produce explicitly scoped conclusions; market-wide no-candidates requires full economic coverage. |

## Version 3.5 Discovery and Autonomy Controls

| Original requirement | v3.5 implementation |
|---|---|
| Screen the requested US small/mid-cap range | Immutable `user_requested_scope` plus separately audited `executed_scope`; internal single-band narrowing is rejected |
| Exclude extreme illiquidity using trading liquidity | 20+ session ADDV provenance contract; raw one-session volume is ignored |
| Use current Forward P/E and do not mix periods | Dated NTM/FY1 normalization, price/EPS reconciliation, analyst breadth, range-dispersion and continuity checks |
| Do not force the user to supervise internal steps | Exit code 2 and `next-action` are same-execution continuation; selected-set commitment requires every selected name to finish |

### Referencia: references/output-template.md

# Required Output Template — v3.5

## 1. Files

Write both:

```text
us_undervalued_growth_<timestamp>.json
us_undervalued_growth_<timestamp>.md
```

Use the evaluator-generated files as the canonical calculation artifacts. Preserve timestamps and source IDs.

## 2. Run Status

At the beginning, state:

- analysis timestamp,
- quote timestamp and session,
- strict-mode flag,
- `ranking_status` (`final` or `provisional`),
- deep-dive input/ranked/review/screened-out/excluded counts,
- broad-screen selected/deferred/unresolved/unavailable/screened-out/excluded counts.

When `ranking_status = provisional`, `selection_outcome = insufficient_data`, or `selection_outcome = selected_pending_enrichment`:

- place a prominent incomplete-coverage warning,
- list unprocessed candidates,
- do not present final-three selections,
- do not describe the displayed order as the final market ranking.

## 3. Screening Funnel and Market Context

Include:

- requested and actual retrieval scope,
- full listing-universe count and listing-data coverage,
- bounded candidate-pool count and generation mode,
- discovery-evaluable count, enrichment attempted/resolved/unresolved counts, resolution percentage, queue, and exhaustion state,
- `candidate_pool_status` and `selection_outcome`,
- selected/deferred/enrichment/sector-review/screened-out/excluded counts,
- corporate-action preflight pass count,
- detailed-underwriting count,
- market valuation, rates, growth, inflation, and sector-cycle assumptions,
- main data sources and as-of dates.

## 4. A. Ranking Table

Recommended columns:

| Rank | Company | Ticker | Price | Market cap | Valuation basis | Current multiple | Standard FCF yield | ROIC/sector return | Diluted-share CAGR | Cyclicality | 3Y constant-multiple upside | Final score | Data quality |
|---:|---|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|

Use `確認できず` / `not verified` for missing values.

## 5. B. Scenario Table

Include current metric/multiple and year-2/year-3 results for:

- constant multiple,
- configured multiple contraction,
- peer median only when basis/period/source validation passes.

Do not render a scenario when accounting bases are mixed.

## 6. C. Candidate Detail

For each eligible candidate, use the following order.

### 1. Basic Information

- company, ticker, exchange,
- sector/industry/special case,
- price, market cap, liquidity,
- price timestamp and source,
- business overview.

### 2. Investment Thesis

Three to five sentences covering per-share compounding, valuation, quality, and why the opportunity exists.

### 3. Valuation

- basis, accounting basis, period kind,
- current metric and recomputed multiple,
- peer median and validity,
- EV/FCF where meaningful,
- standard and SBC-adjusted FCF yield,
- supplied-multiple reconciliation warning if any.

### 4. Growth History and Forecast

- revenue CAGR,
- GAAP EPS CAGR,
- standard FCF-per-share CAGR,
- diluted-share CAGR,
- current/year-2/year-3 metrics,
- forecast-bridge verdict and source classification,
- analyst count and dispersion.

### 5. Latest Earnings

- fiscal period and publication time,
- revenue and growth,
- GAAP operating margin,
- GAAP/adjusted EPS,
- OCF and standard FCF,
- guidance, key KPIs, segments, one-time items,
- growth-state classification.

### 6. Growth Drivers

List the two- to three-year drivers in priority order.

### 7. Peer Comparison

Show three to five genuine peers with multiple, basis, period, and selection reason. Explain why the comparison is valid.

### 8. Why It Is Discounted

- market concern,
- temporary versus structural classification,
- why the market may be correct,
- conditions for discount narrowing,
- whether returns remain attractive without narrowing.

### 9. Constant-Multiple Scenario

| Item | Current | Year 2 | Year 3 |
|---|---:|---:|---:|
| Per-share metric | | | |
| Multiple | | | |
| Implied price | | | |
| Upside | — | | |
| Annualized return | — | | |

### 10. Multiple-Contraction Scenario

Show year-2/year-3 price and return using the configured contraction, normally 20%.

### 11. Catalysts

List 6–24 month catalysts with timing and probability where available.

### 12. Maximum Risk

State the single most important concrete risk.

### 13. Invalidation Conditions

Use measurable thresholds or events.

### 14. Cyclical Assessment

- score 1–5,
- cycle position,
- peak-profit risk,
- normalized metric/multiple and method when required.

### 15. Score

Show all seven raw components, raw total, explicit penalties, and final score.

### 16. Cash-Flow and Evidence Audit

- TTM method,
- OCF, capex cash outflow, standard FCF,
- company-adjusted FCF and definition,
- corporate versus settlement cash where relevant,
- data-quality score and item breakdown,
- warnings, blockers, and unresolved data.

## 7. D. Review-Required and Deferred Work

### Deep-dive review blockers

| Ticker | Company | Final score | Blockers | Evidence needed |
|---|---|---:|---|---|

Keep these out of the ranked list until blockers are resolved.

### Broad-screen dispositions

Always surface nonzero broad-screen rows that still require or defer work:

| Ticker | Company | Status | Fwd P/E | Revenue growth | Per-share growth | Priority | Reasons / requirements |
|---|---|---|---:|---:|---:|---:|---|

Include `selected`, `deferred_by_budget`, `needs_enrichment`, `sector_review_required`/preselection requirements, `near_miss_review`, and `unavailable_after_enrichment` as applicable. A selected cyclical must show its mid-cycle requirement.

## 8. E. Screened-Out Log

Show deep-dive and broad-screen failures separately.

| Stage | Ticker | Company | Reason |
|---|---|---|---|

Do not hide broad-screen failures merely because no deep-dive candidate record exists. Do not mix these with corporate-action or listing exclusions.

## 9. F. Hard Exclusion Log

Include inactive/delisted symbols, completed/pending M&A, OTC, shell/SPAC, extreme illiquidity, invalid sector basis, and other hard flags.

| Ticker | Company | Reason |
|---|---|---|

## 10. G. Final Three

Render only for a final run with at least one eligible candidate.

Categories:

- highest conviction,
- most undervalued,
- largest upside.

For each selection include all nine required points:

1. reason it is most attractive,
2. upside from EPS/FCF-per-share growth alone,
3. what the market may be missing,
4. best catalyst,
5. largest risk,
6. best reason not to buy now,
7. bear case,
8. invalidation conditions,
9. next-earnings KPIs.

The same ticker may occupy more than one category.

## 11. H. Source Ledger

Show source ID, tier, kind, publication/retrieval timestamps, and supported fields. Do not cite a source for a field it does not support.

## 12. I. Unresolved Data and Global Warnings

List:

- unprocessed candidates,
- missing funnel data,
- stale estimates or quotes,
- source conflicts,
- weak analyst coverage,
- basis mismatches,
- unresolved sector/cycle evidence,
- limitations of the run.

If none, state none explicitly.

## 13. JSON Output Contract

The evaluator output contains:

```json
{
  "schema_version": 3,
  "runtime": {"skill_version": "3.6.1", "contract_revision": "3.5", "runtime_fingerprint": "..."},
  "analysis_as_of": "...",
  "run_metadata": {},
  "ranking_status": "final",
  "strict_mode": true,
  "config": {},
  "contract": {"valid": true},
  "market_context": {},
  "global_sources": [],
  "price_basis": {},
  "screening_funnel": {},
  "screening_audit": {"valid": true},
  "broad_screen": {
    "counts": {
      "selected": 0,
      "deferred_by_budget": 0,
      "review_required": 0,
      "screened_out": 0,
      "excluded": 0,
      "unavailable_after_enrichment": 0
    },
    "selected": [],
    "deferred_by_budget": [],
    "review_required": [],
    "screened_out": [],
    "excluded": [],
    "unavailable_after_enrichment": []
  },
  "counts": {
    "input_candidates": 0,
    "ranked": 0,
    "review_required": 0,
    "screened_out": 0,
    "excluded": 0
  },
  "ranked_candidates": [],
  "review_required": [],
  "screened_out": [],
  "excluded": [],
  "final_three": {},
  "global_warnings": []
}
```

Each candidate result preserves:

- status and reasons,
- identity and source-linked corporate-action result,
- normalized financial metrics and TTM method,
- valuation periods and scenarios,
- forecast/reconciliation details,
- sector profile,
- score components and penalties,
- data-quality item details,
- warnings and unresolved fields,
- qualitative thesis fields,
- source ledger.

## 14. Schema-v3 Mandatory Presentation Controls

The final Markdown must additionally show:

- forward metric period kind and accounting basis,
- analyst count/range for each forecast horizon,
- whether each horizon is rankable,
- market-context values and source-backed timestamp,
- listing-enumeration evidence, broad-screen artifact row count, and SHA-256,
- broad-screen attempted/resolved/unresolved and pool-exhaustion state,
- all nonzero broad-screen disposition groups,
- runtime/version and bounded/full conclusion scope,
- separate latest-quarter and latest-full-year blocks,
- evaluator-calculated EV/FCF and cash definition,
- cash/debt reconciliation status,
- sector stress scenarios where applicable,
- source `supports` values,
- `final` versus `provisional` status.

Never render example/placeholder text. Always show 2Y base, 2Y 20%-contraction, 3Y base, and 3Y 20%-contraction as four separately labeled values. A provisional report must not populate the final-three section. `No qualifying candidates` may appear only when the exhausted pool has zero unresolved rows, an empty queue, all final dispositions, and at least one economically assessable row.

## v3.5 Conditional Candidates and Publication Bundle

Insert a distinct **Conditional Candidates** section between ranked and review-required names. State each failed quality gate and the KPI that would promote the name to `eligible`.

`final_three` labels are optional and category-gated. Use `確認できず` when no candidate meets the relevant conviction, cash-flow valuation, or low-case upside threshold.

Before publication, provide:

```text
prepublish-audit.json
us-undervalued-growth-screen-<date>.zip
BUNDLE_MANIFEST.json inside the ZIP
```

The ZIP must include every file referenced by the final snapshot: universe audit, candidate-pool audit/results, generation audit, enrichment queue, candidate records, source ledger, market context, final JSON, and final Markdown.

### Referencia: references/research-checklist.md

# Primary-Source Research Checklist — Schema 3 / Contract 3.5 / Audit v3.5

Use this checklist for every broad-screen survivor. Mark each item `verified`, `not applicable`, or `not verified`. A blank field or a Boolean assertion without a resolving source ID is not a pass.


## v3.5 Runtime and Independent-Bridge Checks

- [ ] Every helper `--version` reports v3.6.1 / contract 3.5 / the expected fingerprint.
- [ ] Audit, checkpoint, and snapshot runtime metadata match the installed skill.
- [ ] The user-requested scope remains separate from the executed retrieval scope; no internal single-band rewrite occurred.
- [ ] Discovery liquidity uses a documented 20+ session average and source IDs, never one-session volume.
- [ ] Current Forward P/E is dated NTM/FY1 and reconciles to positive EPS and price; no distant outer-year substitution.
- [ ] Every Broad Screen-selected symbol is present in the committed set and reaches a verified terminal candidate record.
- [ ] A bounded pool has a valid generation audit and a clearly labeled conclusion scope.
- [ ] Forecast EPS/FCF is independently derived from operating drivers; numerator is not reverse-engineered from target per-share metric.
- [ ] Adjusted forecast GAAP and adjustment portions separately tie to the reconciliation.
- [ ] Each TTM cash-flow component period has resolving source IDs.
- [ ] Corporate cash, eligible securities, customer/settlement funds, and restricted cash are correctly classified.
- [ ] ROIC and EBITDA have source-linked inputs or transparent calculations.
- [ ] Commercial-biopharma aliases trigger concentration, LOE, and 6x/8x stress checks.
- [ ] `peak_profit_risk=true` has sourced normalization.
- [ ] Broad-screen statuses were not overridden by an informal revenue-growth or cycle gate.

## 0. Checkpoint and Run Integrity

- [ ] Initialize a run with `manage_run_state.py`.
- [ ] Record `analysis_as_of`, common quote basis, repository commit, and configuration.
- [ ] Record requested and actual retrieval scope; do not silently narrow the market-cap range.
- [ ] Preserve `user_requested_scope` separately from `executed_scope`; tool/context budget is not scope authorization.
- [ ] If execution is narrower, confirm explicit user authorization and label the limited conclusion scope.
- [ ] Reject single-session volume as ADDV; require provider-average or 20+ trading-day average-volume evidence with source IDs.
- [ ] Prove universe enumeration with provider total plus exhausted pagination or exhausted market-cap-band audits.
- [ ] Attach both listing-universe and candidate-pool audit artifacts with verified SHA-256.
- [ ] Record listing-data coverage separately from candidate-pool economic coverage.
- [ ] Record candidate-pool status (`sufficient`, `sufficient_pending_enrichment`, `no_qualifying_candidates`, or `insufficient_data`).
- [ ] Preserve the enrichment queue and documented attempts when bulk fundamentals are unavailable.
- [ ] Record attempted, resolved, and unresolved counts separately.
- [ ] Confirm every in-scope listing symbol is represented in the candidate pool before a market-wide no-candidates claim.
- [ ] Confirm `candidate_pool_exhaustion_declared=true` only after every candidate row is resolved or evidenced as unavailable.
- [ ] Confirm independently verified `candidate_pool_exhausted=true`; do not rely on the declaration alone.
- [ ] Confirm only genuinely scored, selection-eligible rows enter the deep-dive set.
- [ ] Permit strong cyclicals to enter deep dive with a mid-cycle-normalization requirement.
- [ ] Treat growth thresholds as guidelines; document isolated misses rather than using them as automatic rejects.
- [ ] Record every screening-funnel stage.
- [ ] Save each candidate after preflight and after full verification.
- [ ] Enforce `unprocessed_candidates = selected_symbols - verified_symbols`.
- [ ] Verify the selected-set SHA-256 commitment and configured deep-dive budget.
- [ ] Resolve every committed selected symbol; never let an LLM silently choose a smaller subset.
- [ ] Keep an interrupted run `partial`; do not publish final-three selections.
- [ ] Before publishing “no candidates,” confirm full in-scope candidate coverage, explicit and verified exhaustion, zero queue/unresolved rows, all final dispositions, and at least one assessable row.
- [ ] Confirm Markdown exposes nonzero broad-screen review, unavailable, screened-out, and exclusion groups.

## 1. Corporate-Action Preflight — Perform First

- [ ] Confirm exchange listing is active.
- [ ] Confirm symbol is active and quote volume is plausible.
- [ ] Search for pending or completed acquisitions/mergers.
- [ ] Check delisting, suspension, ticker change, split, reverse split, and spin-off.
- [ ] Record `checked_at` and `latest_material_event_at`.
- [ ] Attach resolving source IDs.
- [ ] Hard-exclude completed/pending M&A and inactive/delisted securities from normal GARP ranking.
- [ ] Route rumors, unknown status, or stale preflight to review.

## 2. Snapshot Integrity

- [ ] Record current-price timestamp, timezone, and session.
- [ ] Confirm regular-close versus after-hours/pre-market/intraday.
- [ ] Record latest earnings period and publication timestamp.
- [ ] Confirm no earnings release or material event occurred after the price timestamp.
- [ ] Confirm split adjustment for price, EPS, and shares.
- [ ] Confirm reporting currency.
- [ ] Map FY1, FY2, and FY3 to the company's fiscal calendar.
- [ ] Normalize the formal current valuation period as NTM or FY1 with period end, estimate-as-of date, analyst count, and source IDs.
- [ ] Reject outer-year-only, pre-operating, zero-crossing, or excessively dispersed consensus as a current Forward P/E.
- [ ] Confirm fiscal versus calendar-year estimates.

## 3. Source Ledger and Evidence Map

For every load-bearing field, create a source-ledger row with:

- source ID,
- tier,
- document kind,
- title,
- publication and retrieval timestamps,
- URL or filing identifier,
- supported field names.

Create candidate-level `evidence` entries for price, latest earnings, revenue, cash flow, SBC, debt, cash classification, diluted shares, and corporate-action preflight.

### Tier 1 — SEC

- [ ] 10-K
- [ ] 10-Q
- [ ] 8-K
- [ ] DEF 14A
- [ ] S-3 / 424B5 when dilution risk exists
- [ ] Form 4 when insider activity matters
- [ ] 20-F / 6-K for foreign issuers

### Tier 2 — Company IR

- [ ] Earnings release
- [ ] Shareholder letter
- [ ] Investor presentation
- [ ] Prepared remarks/transcript supplied by company
- [ ] Guidance
- [ ] Investor-day materials

### Tier 3/4 — Supplemental

- [ ] Quote/market-data vendor
- [ ] Consensus database with retrieval time and analyst count
- [ ] Exchange/company status source
- [ ] Analyst model or calculation with explicit assumptions
- [ ] News/context source

When sources conflict, prefer the latest correcting SEC filing and document the discrepancy.

## 4. Business and Growth

- [ ] Summarize business model and revenue drivers.
- [ ] Identify recurring, transactional, cyclical, project, and acquired revenue.
- [ ] Calculate three- to five-year revenue CAGR.
- [ ] Calculate three-year GAAP EPS CAGR when meaningful.
- [ ] Calculate three-year standard FCF-per-share CAGR.
- [ ] Separate organic and acquisition growth.
- [ ] Separate price, volume, mix, and FX where material.
- [ ] Identify customer, product, platform, channel, and geographic concentration.
- [ ] Assess market share and competitive advantages.
- [ ] Classify growth as accelerating, stable, modestly decelerating, clearly decelerating, bottoming, or peaking.

## 5. Latest Earnings

- [ ] Fiscal period/end date/release timestamp
- [ ] Revenue, YoY, sequential, and organic growth
- [ ] Gross profit and margin
- [ ] GAAP operating income and margin
- [ ] Adjusted operating income and margin
- [ ] GAAP and adjusted EPS
- [ ] Operating cash flow
- [ ] Standard FCF
- [ ] Capex cash-outflow magnitude
- [ ] SBC
- [ ] Basic and diluted shares
- [ ] Guidance and revision direction
- [ ] Same-basis consensus comparison
- [ ] Segment performance
- [ ] Orders, backlog, or sector KPIs
- [ ] One-time costs/gains
- [ ] Working-capital and tax-rate changes

Do not let a headline beat override deteriorating guidance, cash flow, backlog, take rate, prescription growth, or another core KPI.

## 6. TTM Cash Flow and FCF

- [ ] Identify source statement as standalone quarter, YTD cumulative, FY, or explicit TTM.
- [ ] Normalize every `capex_cash_outflow` as a non-negative magnitude.
- [ ] Select one method: `reported_ttm`, `sum_4_discrete`, or `fy_plus_current_ytd_minus_prior_ytd`.
- [ ] For `sum_4_discrete`, confirm four unique standalone quarters.
- [ ] For YTD reconstruction, confirm comparable current/prior periods.
- [ ] Recalculate standard FCF = OCF − capex cash outflow.
- [ ] Reconcile supplied and reconstructed values within configured tolerance.
- [ ] Keep company-adjusted FCF separate and document its definition.
- [ ] Calculate SBC-adjusted economic FCF separately.
- [ ] Explain working-capital contributions.

## 7. GAAP / Adjusted Discipline

- [ ] Record a separate `metric_basis` for current, year-2, and year-3 periods.
- [ ] Confirm all periods use one basis.
- [ ] Never combine current GAAP EPS with future adjusted EPS under one multiple.
- [ ] For adjusted/normalized metrics, record the GAAP starting metric.
- [ ] List every adjustment, amount, label, and recurring status.
- [ ] Confirm arithmetic tie-out to the valuation metric.
- [ ] Attach source IDs.
- [ ] Distinguish company non-GAAP from analyst-created normalization.
- [ ] Flag recurring exclusions and changed definitions.

Review exclusions:

- SBC
- restructuring
- acquisition costs
- intangible amortization
- acquired IPR&D
- litigation
- impairment
- tax items
- asset-sale gains
- other recurring “one-time” items

## 8. Accounting and Earnings Quality

- [ ] Reconcile net income and operating cash flow.
- [ ] Review receivables, DSO, inventory, and inventory days.
- [ ] Review unbilled revenue, contract assets, deferred revenue, and customer advances.
- [ ] Review capitalized software/R&D.
- [ ] Review goodwill, intangibles, and impairments.
- [ ] Review asset-sale gains, tax effects, and pension/non-operating income.
- [ ] Review related parties, auditor changes, material weaknesses, restatements, and SEC investigations.

## 9. Balance Sheet and Cash Classification

- [ ] Corporate cash
- [ ] Marketable securities available to shareholders
- [ ] Customer/settlement funds
- [ ] Restricted cash
- [ ] Total debt
- [ ] Net debt using only eligible cash
- [ ] Net debt/EBITDA
- [ ] Interest expense and coverage
- [ ] Debt maturities, rates, covenants, leases, preferred stock, and minority interests
- [ ] Goodwill/intangibles and contingent acquisition obligations

For payments/marketplace businesses, never treat settlement float as corporate cash.

## 10. SBC, Dilution, and Capital Allocation

- [ ] SBC amount, SBC/revenue, and SBC/OCF
- [ ] Basic and diluted share history
- [ ] Annualized diluted-share change
- [ ] RSUs, options, warrants, convertibles
- [ ] ATM, shelf, and public-offering history
- [ ] Actual buyback dollars and shares
- [ ] Average repurchase price
- [ ] Net share reduction after employee issuance
- [ ] Buyback funding source
- [ ] Acquisition returns and impairment history

## 11. Forecast Quality and Arithmetic Bridge

For every current/year-2/year-3 metric used:

- [ ] Period label and period kind
- [ ] Metric basis
- [ ] Source classification
- [ ] Retrieval time and source IDs
- [ ] Analyst count
- [ ] Estimate low/high or dispersion

For year-2/year-3:

- [ ] Revenue assumption
- [ ] Gross/operating or FCF margin assumption
- [ ] Interest assumption
- [ ] Tax rate
- [ ] Diluted shares
- [ ] Buyback/dilution assumptions
- [ ] Acquisition/divestiture assumptions
- [ ] Metric numerator and denominator
- [ ] Arithmetic tie to valuation metric within tolerance

Flag single-analyst outer-year estimates and unexplained linear extrapolation.

## 12. Valuation and Scenarios

- [ ] Sector-appropriate valuation basis
- [ ] Current multiple recomputed as price/current metric
- [ ] Supplied multiple reconciled
- [ ] NTM/FY1/FY2 multiple labels
- [ ] EV/EBITDA, EV/EBIT, EV/FCF where appropriate
- [ ] Standard and SBC-adjusted FCF yield
- [ ] Own-history median
- [ ] Three to five genuine peers
- [ ] Same-basis/same-period peer median
- [ ] Constant-multiple 2Y and 3Y cases
- [ ] 20% contraction 2Y and 3Y cases
- [ ] Peer-median case only when valid

## 13. Sector-Specific Review

### Commercial biopharma

- [ ] Product-level revenue and top-product concentration
- [ ] Nearest material LOE date
- [ ] Patent settlement/litigation status
- [ ] Next-generation formulation/indication strategy
- [ ] Replacement pipeline and launch costs
- [ ] Source IDs for concentration and LOE

### Payments

- [ ] TPV growth
- [ ] Revenue/TPV and gross-profit/TPV
- [ ] Current and prior gross-profit take rate
- [ ] Corporate versus settlement cash
- [ ] FX and country exposure
- [ ] Standard versus adjusted FCF
- [ ] Source IDs

Use `sector-kpis.md` for all other sectors.

## 14. Cyclical Review

For scores 3–5:

- [ ] Five- to ten-year revenue, margin, EPS, and FCF history
- [ ] Orders/backlog/book-to-bill
- [ ] Inventory/utilization/capacity
- [ ] Customer/industry capex
- [ ] Commodity/freight exposure
- [ ] Price versus volume
- [ ] Recession drawdown
- [ ] Mid-cycle revenue and margin
- [ ] Normalized per-share metric and multiple
- [ ] Normalization method and source IDs

## 15. Peer Set

- [ ] Three to five genuine peers
- [ ] Selection reason per peer
- [ ] Same metric basis and period kind
- [ ] Growth, margins, ROIC/sector return, leverage, SBC, dilution, and valuation compared
- [ ] Discount classified as temporary, structural, justified, or unverified

## 16. Governance and Thesis

- [ ] Management capital allocation
- [ ] Insider ownership and transactions with 10b5-1 context
- [ ] Dual-class/founder control
- [ ] Related parties and compensation alignment
- [ ] Three- to five-sentence thesis
- [ ] Why discounted and why market may be right
- [ ] Six- to 24-month catalysts
- [ ] Largest concrete risk
- [ ] Bear case
- [ ] Measurable invalidation conditions
- [ ] Next-quarter KPIs
- [ ] Best reason not to buy now

## 17. Final Gate

A candidate may be `eligible` only when:

- [ ] Corporate action is fresh, active, and sourced.
- [ ] No hard flag is unresolved.
- [ ] Price and event timestamps are consistent.
- [ ] Core financial fields have Tier 1/2 evidence.
- [ ] TTM cash flow and capex signs are valid.
- [ ] Current/future metric bases match.
- [ ] Forecast bridge and required GAAP reconciliation pass.
- [ ] Valuation basis is sector-appropriate.
- [ ] Peer set is valid or explicitly unavailable without inventing a median.
- [ ] Data-quality score meets threshold.
- [ ] Required cyclical/sector evidence is complete.
- [ ] Minimum upside gate passes.
- [ ] Invalidation conditions are measurable.
- [ ] Run is complete before final-three publication.

## 18. Schema-v3 Autonomous Completion Checks

Before presenting a live run, confirm:

- [ ] Market context contains no placeholder text, is not future-dated, and has policy rate, 10Y yield, inflation, market forward P/E, small/mid-cap context, and resolving source IDs.
- [ ] `screening_audit` hashes to the full row-level universe artifact.
- [ ] Every audit-selected symbol has a verified candidate checkpoint.
- [ ] No selected symbol remains in `unprocessed_candidates`.
- [ ] `source.supports` is an array for every source.
- [ ] Source kind/tier is correct; no third-party transcript is labeled company IR.
- [ ] Q4 and full-year figures are stored separately.
- [ ] Current formal valuation metric is NTM or FY1.
- [ ] At least one future horizon is rankable after analyst-count checks.
- [ ] Current/future metric bases match.
- [ ] EV/FCF uses corporate cash plus eligible marketable securities consistently.
- [ ] Latest-release and normalized cash/debt values reconcile or have a source-backed note.
- [ ] High-growth 21–30x P/E exceptions were not mechanically discarded.
- [ ] Auto dealers use floorplan-adjusted leverage.
- [ ] Commercial biopharma product concentration and LOE are sourced or derived.
- [ ] `evaluate_candidates.py --strict --require-final` exits 0.
- [ ] The first diagnostic report was inspected and repairable blockers were corrected.

## v3.5 Final Quality Checklist

- [ ] Broad Screen selected lanes are diversified across core/high-growth/near-miss/cyclical opportunities where available.
- [ ] Candidate rows retain `average_volume` and `liquidity_source_ids`.
- [ ] Provider-side share-volume filters are disclosed and do not count as full listing enumeration.
- [ ] Every forecast driver has origin, source IDs, and `target_solved=false`.
- [ ] No margin, share count, or residual adjustment was reverse-solved merely to match target EPS.
- [ ] Every discrete cash-flow period has explicit source support.
- [ ] SEC filing evidence uses an accession-specific Archives URL.
- [ ] Recent spin-offs/acquisitions have pro-forma transition normalization.
- [ ] Formal eligible names pass score, FCF, ROIC, leverage, dilution, low-case, and LOE quality gates.
- [ ] `final_three` categories remain null when category thresholds are not met.
- [ ] `prepublish_audit.py` exits 0.
- [ ] `bundle_run_artifacts.py` produces a self-contained, manifest-hashed ZIP.

### Referencia: references/review-regression-matrix.md

# Review Regression Matrix — v3.6

The first section records inherited contract-3.5 controls; the final section covers the v3.6 Claude Code acquisition architecture.

| Observed failure | Prevention | Regression/release check |
|---|---|---|
| Default USD 500M–20B request was silently changed to USD 3B–4B | Immutable `user_requested_scope`, separate `executed_scope`, and explicit authorization gate | scope-preservation and unauthorized-reduction tests |
| One-session volume was labeled as ADDV and used to build the pool | Shared average-liquidity validator requires provider average or 20+ trading days and source IDs | single-session rejection and 20-day/provider-average acceptance tests |
| FRMI-like outer-year EPS produced a misleading 4x current Forward P/E | Estimate normalizer requires a resolving NTM/FY1 horizon and clears canonical values for outer-year/pre-operating/zero-crossing data | normalizer outer-year, FY1-horizon, and FRMI regression tests |
| Five selected names were later reduced to two by model preference | Selected-set SHA-256 commitment; every selected symbol must reach a terminal verified record; budget changes require re-screening | selected-commitment and all-selected completion tests |
| Intermediate output asked the user whether to continue or choose a subset | Exit code 2 is an internal continuation signal; run-state next action is deterministic and never requires user confirmation | autonomous-continuation and no-user-choice tests |
| A cached v3.1 package produced artifacts after v3.5 was installed | Single-source runtime metadata and fingerprint in every audit/snapshot; hard mismatch rejection; `--version` on all entry points | stale-runtime and cross-script version tests |
| LLM replaced deterministic broad-screen rules with an 8% revenue gate | Script output is authoritative; soft misses remain `guideline_misses`; near-miss/high-growth/cyclical routing preserved | broad-screen near-miss and high-growth tests |
| Cyclicals were rejected instead of normalized | Cycle 3–5 or `peak_profit_risk=true` forces sourced normalization before eligibility | peak-profit and cyclical normalization tests |
| A bounded 20-name pool was treated as a full-market conclusion | Explicit conclusion scope and validated generation audit; bounded ranking/no-candidate wording | bounded-pool completion and scoped no-candidate tests |
| Candidate pool stayed unresolved while run claimed final | Exhausted + all resolved + queue zero required; checkpoint and evaluator recompute | unresolved-pool finality tests |
| Forecast bridge passed because numerator was set to EPS × shares | Driver-derived revenue/margin/interest/tax/share reconstruction; numerator is cross-check only | circular-numerator rejection and valid driver bridge tests |
| Adjusted EPS bridge did not tie back to GAAP | Driver GAAP EPS and after-tax adjustments must tie to GAAP reconciliation | adjusted bridge reconciliation tests |
| `biopharma` alias bypassed LOE controls | Sector aliases normalize to `commercial_biopharma`; concentration/LOE/6x/8x evidence required | biopharma alias LOE test |
| Peak-profit risk was flagged but normalization was marked unnecessary | `peak_profit_risk=true` overrides a low numeric cyclicality score | peak-profit normalization test |
| EV/FCF text used manual cash while evaluator could not classify cash | Ordinary cash normalization; payments/custodial cash separation; evaluator-calculated EV only | cash normalization and payments cash tests |
| Data-quality score was 100 despite missing ROIC/EBITDA evidence | Source-linked ROIC/EBITDA evidence required; fail-closed quality cap | financial-quality evidence-cap test |
| TTM FCF periods cited only the latest 10-Q | Every TTM method/component requires resolving period source IDs | TTM period-source test |
| Funnel said preflight passed 0 although selected candidates passed | Evaluator recomputes selected-candidate preflight and completion counts | funnel-count consistency test |
| Report mixed 2Y base with 3Y stress | Explicit 2Y/3Y base and 2Y/3Y contraction columns | scenario-rendering regression |
| Official-statistics label pointed to a nonofficial domain | Source kind/domain validation | official-domain validation test |
| Standalone and overlay packages differed | Build package once from canonical source, embed identical bytes, compare SHA-256 and logical contents | release packaging checks |
| Global priority selected only one factor style | Four deterministic selection lanes with quotas, sector cap, and backfill | multi-lane opportunity-type test |
| Candidate serializer dropped average-volume provenance | Broad-screen metrics preserve `average_volume` and `liquidity_source_ids` | serializer provenance test |
| Provider share-volume filters were called full-universe enumeration | Retrieval-filter inspection downgrades conclusion scope and enumeration claim | provider-prefilter scope test |
| DKS-like low-P/E name ranked despite EV/FCF 79x and sub-1% adjusted FCF yield | Post-score quality eligibility gate routes severe weak-FCF names to review | low-FCF quality-gate test |
| Driver margins were solved backwards to consensus EPS | Per-driver provenance and `target_solved=false` contract | target-solved bridge rejection test |
| SEC browse page stood in for an immutable filing | Accession-specific SEC Archives URL required | SEC browse-page rejection test |
| Generic TTM support label stood in for four discrete quarters | Exact period support paths required | discrete-period support test |
| Recent spin-off was hard-excluded as an invalid special case | Corporate-transition normalization routes to review | recent-spin-off migration test |
| One eligible name was forced into every final-three category | Category-specific thresholds and nullable labels | nullable final-three test |
| Final ZIP contained only summaries, not audit evidence | Prepublication audit plus deterministic complete-run bundle | bundle completeness test |
| Final prose asked the user to continue | Prepublication prose audit rejects unfinished-run language | continue-language rejection test |

## v3.6 Claude Code direct-FMP regressions

| Observed failure | v3.6 prevention | Regression/release check |
|---|---|---|
| Bulk FMP JSON consumed the model context before underwriting | Direct Python pipeline writes provider payloads to disk and prints a compact summary only | direct-pipeline compact-summary test |
| Existing skills duplicated FMP transport, fallback, and retry logic | GARP client is generated from the repository-level `scripts/fmp_client/` registry/special-template source of truth | generator-source/package equivalence check |
| Repeated runs refetched unchanged provider data | SQLite response cache with dataset TTLs | persistent-cache cross-client test |
| Company-screener responses silently truncated at the provider limit | Adaptive overlapping market-cap-band splitting; scope is complete only when every leaf is unsaturated | saturated-band enumeration test |
| Per-symbol liquidity work was allocated before economic relevance was known | Bulk EOD first; fallback exact-liquidity targets are chosen round-robin from the four GARP lanes | direct-pipeline lane-target test |
| Overlapping core/high-growth symbols made the provider-pool audit report too few represented lanes | Lane coverage is calculated from final candidate memberships, not only the insertion loop | overlapping-lane provider-pool test |
| Full FMP packets still burdened the model after discovery | Full payloads remain under `provider/candidate-data`; projected packets contain only underwriting-relevant fields and artifact paths | candidate-packet size/content review |
| Claude stopped and requested another user turn | `NEXT_ACTION.json` sets `user_confirmation_required=false`; Claude Code command forbids “Continue” handoff | command contract and prepublish phrase gate |

### Referencia: references/scoring-rubric.md

# Scoring Rubric, Evidence Quality, Penalties, and Gates — v3.5

## 1. Philosophy

Use two independent dimensions:

1. **Investment score** — attractiveness of the company and return setup.
2. **Data-quality score** — whether the evidence is sufficient to trust the investment score.

A high investment score never overrides missing evidence. A candidate below the configured data-quality floor is `review_required`, not rankable.

## 2. Raw Investment Score — 100 Points

### A. Growth Sustainability — 20

Assess:

- two- to three-year revenue and per-share growth visibility,
- durability of drivers,
- organic versus acquisition growth,
- customer/product concentration,
- forecast breadth and plausibility,
- sector-specific lifecycle or cycle risks.

Guide:

- 17–20: durable 20%+ per-share growth or exceptional 15%+ visibility.
- 13–16: credible mid-teens growth with manageable risks.
- 8–12: growth exists but is volatile, concentrated, or fading.
- 0–7: weak or unsupported growth.

### B. Valuation Attractiveness — 20

Assess:

- same-basis current/forward multiple,
- standard and SBC-adjusted FCF yield,
- own-history and peer comparison,
- constant-multiple upside,
- 20% contraction resilience,
- value-trap risk.

Do not award a high score merely for low trailing P/E.

### C. Financial Quality and Capital Efficiency — 15

Assess:

- ROIC/sector return metric,
- margins and operating leverage,
- usable corporate cash,
- net leverage and refinancing risk,
- goodwill/intangible burden,
- resilience under stress.

### D. FCF and Earnings Quality — 15

Assess:

- correctly reconstructed standard FCF,
- OCF versus net income,
- working-capital quality,
- standard versus company-adjusted FCF gap,
- SBC-adjusted economics,
- accounting red flags.

### E. Competitive Advantage — 10

Assess:

- switching costs,
- network effects,
- brand/data/regulatory moat,
- recurring revenue,
- customer retention,
- market-share durability.

### F. Capital Allocation, SBC, and Dilution — 10

Assess:

- actual net share change,
- buyback price discipline and funding,
- SBC burden,
- acquisition returns and impairments,
- debt repayment and reinvestment quality.

### G. Catalyst / Risk Balance — 10

Assess:

- catalyst timing and probability,
- identifiable route to estimate delivery,
- downside asymmetry,
- measurable invalidation conditions,
- reason not to buy now.

## 2A. Broad-Screen Guidance Versus Hard Gates

Broad-screen growth and preferred valuation thresholds are guidelines. Store isolated misses in `guideline_misses`; they reduce priority or trigger a near-miss review but do not automatically reject a company.

Selection-eligible patterns include:

- preferred forward valuation plus credible per-share growth,
- P/E 21–30 with 20%+ per-share growth,
- attractive P/E and mid-teens per-share growth even when headline revenue growth is below the preferred range,
- strong cyclical growth/valuation combinations that require mid-cycle normalization.

Hard broad failures are reserved for severe conditions such as non-positive standard FCF when applicable, negative ROIC, excessive leverage beyond the hard limit, extreme forward valuation unsupported by growth, or negative revenue and per-share growth.

`sector_review_required` is selection-eligible when the remaining work is nonblocking cyclical normalization. Missing bank/REIT/BDC/MLP valuation or auto-dealer floorplan-adjusted leverage remains blocking and produces `needs_enrichment`.


## 3. Evidence-Derived Data-Quality Score — 100

The evaluator awards points only when fields and resolving source IDs pass. Self-attested completeness flags are ignored.

| Item | Weight | Required evidence |
|---|---:|---|
| Quote verified | 5 | Price source resolves. |
| Latest earnings verified | 7 | Quarter/full-year separation, timestamps, Tier 1/2 source. |
| Core financials and TTM periods verified | 10 | Revenue, TTM OCF/capex periods, SBC, debt, cash, and shares have primary evidence. |
| Guidance/consensus labeled | 8 | Each valuation period has type, date, analysts, and sources. |
| Driver-derived forecast bridge | 15 | Independent operating-driver arithmetic and source evidence pass. |
| Diluted shares verified | 8 | History and Tier 1/2 evidence. |
| SBC verified | 8 | TTM SBC and Tier 1/2 evidence. |
| Peer set verified | 8 | At least three genuine same-basis forward peers. |
| GAAP/non-GAAP reconciled | 8 | Adjusted periods tie GAAP and adjustment components. |
| Corporate actions verified | 4 | Fresh active listing/symbol/M&A preflight. |
| Cyclical/peak-profit normalization | 5 | Sourced normalization whenever cycle or peak-profit risk requires it. |
| Cash classification verified | 5 | Source-backed corporate cash; customer/restricted funds separated where applicable. |
| ROIC/EBITDA evidence verified | 4 | Reported or transparent analyst-calculated values with sources. |
| Sector risk verified | 5 | LOE/concentration, payments cash, or auto-dealer leverage evidence as applicable. |
| **Total** | **100** | |

Default minimum: 70. A score of 100 means deterministic evidence checks passed; it does not guarantee the thesis is correct.

## 4. Deterministic Penalties

Penalties subtract from the raw 100-point investment score.

### Data-quality penalty

| Data quality | Penalty |
|---:|---:|
| 90–100 | 0 |
| 80–89 | 2 |
| 70–79 | 5 |
| 60–69 | 10 |
| below 60 | 20 |

The minimum-quality gate may still prevent ranking regardless of penalty.

### Cyclicality penalty

| Score | Penalty |
|---:|---:|
| 1 | 0 |
| 2 | 1 |
| 3 | 3 |
| 4 | 6 |
| 5 | 10 |

Missing required normalization is also a review blocker.

### Estimate breadth

Use the minimum analyst count among available year-2/year-3 metrics.

| Minimum count | Penalty |
|---:|---:|
| 5+ | 0 |
| 3–4 | 2 |
| 1–2 | 4 |
| unavailable | 5 |

### Estimate dispersion

Use the maximum normalized low/high spread among future periods.

| Dispersion | Penalty |
|---:|---:|
| ≤20% | 0 |
| >20–30% | 1 |
| >30–50% | 2 |
| >50% | 4 |

### SBC / revenue

| SBC/revenue | Penalty |
|---:|---:|
| missing | 2 |
| ≤5% | 0 |
| >5–10% | 2 |
| >10–15% | 3 |
| >15–25% | 5 |
| >25% | 8 |

### Annualized diluted-share growth

| Growth | Penalty |
|---:|---:|
| missing | 2 |
| ≤3% | 0 |
| >3–5% | 2 |
| >5–10% | 4 |
| >10% | 8 |

Net share reduction is not inferred from a buyback authorization.

### Liquidity

- Below preferred dollar-volume threshold but above hard floor: 2 points.
- Below hard floor: hard exclusion as extreme illiquidity.

### Sector-specific risk

Current deterministic examples:

- Commercial biopharma with top-product concentration ≥50% and nearest material LOE within five years: 2 points.
- The same condition with LOE within three years: 4 points.

Missing required sector evidence causes review rather than a silent neutral score.

## 5. Gates and Statuses

### `excluded`

Hard exclusion includes:

- inactive, delisted, or suspended symbol,
- pending or completed M&A/special-situation pricing,
- OTC, penny stock, shell/SPAC, or development-stage economics,
- repeated financing dependence,
- unresolved restatement/material weakness/SEC investigation,
- meme-only thesis,
- extreme illiquidity,
- invalid special-case valuation basis.

### `screened_out`

Use when the security is valid and active but does not satisfy the broad economic screen. Preserve reasons and sources.

### `review_required`

Examples:

- stale quote/event mismatch,
- stale or unresolved corporate-action preflight,
- TTM/capex reconstruction failure,
- mixed GAAP/adjusted periods,
- forecast bridge or required reconciliation failure,
- data quality below threshold,
- missing cyclicality normalization,
- missing sector-critical evidence,
- insufficient constant-multiple upside when configured,
- materially conflicting supplied multiple.

### `eligible`

All hard and review gates pass. Eligible does not mean “buy”; it means the candidate may be compared and ranked.

## 6. Run-Level Ranking Status

- `final`: run metadata says complete and no symbols remain unprocessed.
- `provisional`: partial run or non-empty unprocessed list.

A provisional report may show completed candidate calculations, but `final_three` must remain empty.

## 7. Confidence Labels

- `high`: eligible, data quality ≥85, analyst breadth ≥5, and no major unresolved caveat.
- `medium`: eligible with data quality 70–84 or analyst breadth 3–4.
- `low`: eligible only under an exception or with fragile estimates.
- `not_ranked`: review-required, screened-out, or excluded.

## 8. Sorting and Tie-Breaking

Sort eligible candidates by:

1. final score,
2. data-quality score,
3. preferred three-year constant-multiple upside,
4. lower cyclicality,
5. symbol for deterministic stability.

Final selections use separate lenses:

- highest conviction: final score, data quality, confidence,
- most undervalued: SBC-adjusted FCF yield and lower current multiple,
- largest upside: preferred three-year constant-multiple upside.

## 9. Schema-v3 Quality Caps

The lowest applicable cap wins.

| Failure | Maximum data-quality score |
|---|---:|
| Latest quarter/full-year mixed or incomplete | 55 |
| Source ledger kind/domain/supports invalid | 60 |
| Forward basis or driver-derived forecast bridge invalid | 60 |
| Core financial/TTM-period evidence incomplete | 65 |
| Required cyclical or peak-profit normalization missing | 65 |
| Required sector/LOE stress evidence missing | 65 |
| ROIC/EBITDA evidence incomplete | 65 |
| Broad-screen audit/runtime invalid | 65 |
| Cash classification incomplete or conflicting | 70 |
| Market context absent, stale, future-dated, or placeholder | 70 |

These caps prevent unsupported 90–100 quality scores.

## 10. Forecast-Horizon Rankability

- Current formal valuation: NTM or FY1.
- A consensus future horizon normally requires at least three analysts.
- A one- or two-analyst horizon is supplemental unless a sourced independent model passes the forecast bridge.
- A candidate must have at least one rankable two- or three-year horizon.
- TTM multiples, unsupported outer-year estimates, and mixed metric bases cannot satisfy the 30% upside gate.

## 11. Run-Level Finality

A final ranking requires:

```text
run_metadata.status = complete
unprocessed_candidates = []
screening_audit.valid = true
screening_audit.runtime matches installed v3.6 fingerprint
screening_audit.candidate_pool.generation_audit.valid = true for bounded pools
screening_audit.enrichment.candidate_pool_exhausted = true
screening_audit.enrichment.unresolved_count = 0
screening_audit.enrichment.queue_count = 0
screening_audit.enrichment.all_rows_resolved = true
contract.valid = true
```

A full-market no-candidates conclusion additionally requires full in-scope economic coverage. A bounded-pool no-candidates conclusion must be explicitly scoped to the audited bounded pool and requires at least one economically assessable row. Attempt counts and evaluable-count thresholds cannot replace pool resolution.

The CLI `--require-final` returns exit code 2 otherwise. Diagnostic files are still written for the repair loop.

## 12. v3.5 Formal Eligibility Quality Gate

Passing the 30% base-case upside test is necessary but not sufficient. A formal `eligible` name must satisfy all configured floors:

| Gate | Default |
|---|---:|
| Final investment score | ≥70 |
| SBC-adjusted FCF yield | ≥3%, **or** EV/FCF ≤30x |
| ROIC / sector-equivalent return | ≥8% |
| Net Debt / EBITDA | ≤3.0x when applicable |
| Diluted-share CAGR | ≤5% |
| Supported low-consensus-case upside | ≥15% |
| Severe LOE stress | no loss worse than -25% |

A candidate with one or two ordinary failures may be labeled `conditional`. A candidate with more failures, severely weak FCF support (for example SBC-adjusted yield below 1% or EV/FCF above 50x), or severe LOE downside is `review_required`.

### Category-specific final selections

`final_three` categories may be null. Never force the sole eligible name into every label.

- **Highest conviction:** score ≥75, DQ ≥80, stress upside ≥0.
- **Most undervalued:** SBC-adjusted FCF yield ≥5% or EV/FCF ≤20x.
- **Largest upside:** supported low-consensus-case upside ≥20%.

If no ranked candidate meets a category threshold, render `確認できず` / `not verified`.

### Referencia: references/sector-kpis.md

# Sector-Specific Valuation and KPI Rules

Apply these rules in addition to the common framework. A sector-specific metric replaces, rather than decorates, an inappropriate generic metric.

## 1. SaaS and Software

### Required KPIs

- ARR and ARR growth
- Net revenue retention (NRR)
- Gross retention
- RPO and current RPO
- Subscription versus services mix
- Gross margin
- FCF margin
- Rule of 40
- SBC / revenue
- Diluted-share growth
- Capitalized software development
- Customer concentration

### Valuation

Use EV/revenue only as a secondary measure. Prefer EV/FCF, FCF yield, normalized operating margin, and per-share FCF growth once FCF is positive.

### Red flags

- ARR growth falling faster than revenue growth
- NRR below 100%
- SBC / revenue above 15% without rapid decline
- FCF driven mainly by SBC or deferred revenue
- GAAP losses masked by recurring adjusted exclusions

## 2. Semiconductors and Semiconductor Equipment

### Required KPIs

- Inventory and inventory days
- Book-to-bill
- Backlog
- Utilization
- Lead times
- Channel inventory
- Customer capex
- End-market mix
- Product mix
- Gross-margin cycle
- Customer concentration

### Valuation

Use normalized/mid-cycle EPS, EBIT, and FCF. A low trailing P/E at peak margins is not cheap.

### Red flags

- Inventory growth exceeding revenue growth
- Backlog cancellation or book-to-bill below 1
- Margin well above historical median without structural evidence
- Customer capex rolling over

## 3. Industrials and Capital Goods

### Required KPIs

- Orders
- Backlog
- Book-to-bill
- Organic growth
- Price and volume
- Utilization
- Customer capex
- Aftermarket/service mix
- Working-capital requirements

### Valuation

Use EV/EBIT, EV/FCF, and normalized EPS. For highly cyclical businesses calculate mid-cycle margins.

## 4. Retail, Restaurants, and Consumer Companies

### Required KPIs

- Comparable sales
- Traffic
- Average ticket
- Unit growth
- Store-level margin
- New-unit payback
- Inventory turnover
- Markdown rate
- Customer-acquisition cost
- Direct-to-consumer mix
- International growth

### Valuation

Use P/E and FCF yield with lease-aware enterprise value where material. Distinguish growth from unit expansion, price, traffic, and mix.

### Red flags

- Price-led comps with declining traffic
- Inventory rising faster than sales
- New-unit returns deteriorating
- Buybacks funded by leverage while store economics weaken

## 5. Healthcare Services and Medical Devices

### Required KPIs

- Procedure or patient volume
- Reimbursement trends
- Utilization
- Installed base
- Consumable/recurring revenue
- Pipeline or product-launch milestones
- Gross margin
- Regulatory actions
- Customer or payer concentration

### Valuation

Use P/E, EV/EBIT, and EV/FCF. For product-concentrated businesses, scenario-test loss of exclusivity or reimbursement changes.

## 6. Commercial Biotechnology and Specialty Pharmaceuticals

### Eligibility

Exclude pre-revenue or development-stage companies. Admit only businesses with meaningful commercial revenue and a valid earnings/standard-FCF framework.

### Required KPIs

- Product-level revenue and growth
- Top-product revenue concentration (`top_product_revenue_pct`)
- Prescription, patient, or demand growth
- Gross-to-net deductions
- Market share
- Nearest material loss-of-exclusivity date (`nearest_material_loe_date`)
- ANDA/patent settlement or litigation status
- Next-generation formulation, indication, or lifecycle-extension strategy
- Replacement pipeline probability and milestones
- R&D and launch intensity
- Acquisition integration and contingent obligations
- Source IDs supporting concentration and LOE

### Valuation and Risk

Use P/E and standard FCF only when operating economics are established. Do not mix a current GAAP metric with future adjusted consensus. Treat product concentration and LOE as structural risk even when near-term growth is strong. Do not count pipeline NPV as certain value.

The evaluator applies a sector penalty when the top product is at least 50% of revenue and nearest material LOE is within five years; missing sourced concentration/LOE evidence is review-required in strict mode.

## 7. Payments, Marketplaces, and Money Movement

### Required KPIs

- TPV or payment volume and growth
- Revenue/TPV and gross-profit/TPV
- Current and prior gross-profit take rate (`gross_profit_to_tpv_pct`, `gross_profit_to_tpv_prior_pct`)
- Transaction count and active merchants/users
- Cross-border, country, and FX exposure
- Credit or chargeback losses where applicable
- Corporate cash and marketable securities
- Customer/merchant/settlement funds and restricted cash
- Standard FCF versus company-adjusted FCF
- Working-capital normalization
- Dilution and SBC
- Source IDs for cash classification and take rates

### Valuation and Risk

Use corporate cash only for net-debt analysis; settlement float is not shareholder cash. A revenue surge caused by lower-margin pass-through volume is not equivalent to gross-profit growth. Track gross-profit/TPV and operating leverage. If the take rate declines, explain whether mix, geography, competition, or accounting presentation caused it.

Strict mode requires sourced separation of corporate and settlement cash.

## 8. Banks

Do not use EV/EBITDA.

### Required KPIs

- P/TBV and P/book
- ROTCE and ROE
- Net interest margin
- Deposit beta
- Deposit mix and uninsured deposits
- Loan growth
- Nonperforming loans
- Net charge-offs
- Provision expense
- CET1
- Commercial real-estate exposure
- Securities marks and accumulated other comprehensive income

### Scenario basis

Use TBV per share or book value per share and an appropriate P/TBV or P/book multiple. Model credit and deposit stress.

## 9. Insurance

### Required KPIs

- P/book or P/TBV
- ROE
- Combined ratio
- Underwriting income
- Reserve development
- Investment income
- Catastrophe exposure
- Premium growth
- Retention

### Scenario basis

Use book/TBV per share or normalized EPS. Adjust for reserve quality and catastrophe-cycle conditions.

## 10. REITs

Do not use ordinary EPS or P/E as the primary basis.

### Required KPIs

- P/FFO and P/AFFO
- AFFO growth
- NAV premium/discount
- Same-store NOI
- Occupancy
- Leasing spreads
- Lease maturities
- Net debt / EBITDA
- Fixed-charge coverage
- Dividend payout

### Scenario basis

Use AFFO per share or NAV per share. Include refinancing and cap-rate sensitivity.

## 11. Business Development Companies (BDCs)

### Required KPIs

- Price/NAV
- Net investment income per share
- Non-accruals
- Portfolio yield
- Debt/equity
- Interest coverage
- First-lien exposure
- Payment-in-kind income
- Dividend coverage
- NAV trend

### Scenario basis

Use NAV per share or normalized NII per share. Do not use industrial-company EV/EBITDA.

## 12. MLPs and Midstream Partnerships

### Required KPIs

- Distributable cash flow per unit
- Distribution coverage
- Leverage
- Contracted versus commodity-sensitive cash flow
- Counterparty concentration
- Maintenance versus growth capex
- Unit issuance/buybacks
- IDRs or sponsor conflicts

### Scenario basis

Prefer DCF per unit, FCF per unit, and EV/EBITDA on a consistently defined basis. Treat tax structure separately.

## 13. Energy, Mining, Materials, Chemicals, Steel, and Shipping

### Required KPIs

- Commodity or freight prices
- Production/volume
- Realized price
- Unit costs
- Capacity/utilization
- Capital intensity
- Maintenance capex
- Reserve life where relevant
- Contract coverage
- Balance-sheet sensitivity

### Valuation

Use normalized commodity assumptions and mid-cycle margins. Do not annualize a spot-price windfall.

## 14. Homebuilders and Housing-Related Companies

### Required KPIs

- Orders and cancellations
- Backlog
- Community count
- ASP
- Gross margin excluding unusual items
- Incentives
- Land inventory
- Net debt/capital
- Mortgage-rate sensitivity

### Valuation

Use normalized EPS, book value, and land-cycle analysis. A low P/E at peak closings may be misleading.

## 15. Advertising, Staffing, Transportation, Airlines, and Autos

These are normally cyclicality score 3 to 5.

### Required KPIs

- Volume and utilization
- Price/yield
- Customer budget or hiring trends
- Capacity
- Load factor or miles/hours where relevant
- Used-asset values
- Backlog/order intake
- Labor and fuel/input costs

Use normalized operating margins and recession drawdown history.

## 16. Auto Dealerships and Floorplan Debt

Do not apply general-company net-debt/EBITDA mechanically to auto dealers. Obtain a sourced sector-adjusted leverage measure that explicitly excludes inventory floorplan financing when appropriate.

Required schema-v3 fields:

- `adjusted_net_debt_to_ebitda`
- `floorplan_debt_excluded = true`
- source IDs

Without these fields, route the candidate to `review_required`, not `screened_out` solely because unadjusted leverage appears high.

## 17. Commercial Biopharma LOE Stress

When a top product contributes at least 50% of revenue and a material LOE is within five years:

- calculate or source product concentration,
- record the nearest material LOE date,
- distinguish base patent, pediatric exclusivity, settlements, formulation/use patents, and replacement products,
- calculate 6x and 8x year-3 metric stress cases in addition to the generic 20% multiple-contraction case.

Product concentration may be derived as:

```text
top product revenue / total revenue
```

only when both values share the same period and source evidence.

## v3.5 Normalization Rules

- Normalize `biopharma`, `pharma`, `biotechnology`, `royalty_biopharma`, and `drug_delivery_platform` to `commercial_biopharma` when commercial product or royalty economics exist.
- Commercial biopharma requires sourced product/revenue-stream concentration, nearest material LOE, and configured 6x/8x stress scenarios.
- `peak_profit_risk=true` forces mid-cycle normalization regardless of the numeric cyclicality score.
- Sector evidence is part of the data-quality score and can cap it at 65 when missing.


---

## SKILL: value-dividend-screener

- Fuente: `tradermonty/claude-trading-skills` → `skills/value-dividend-screener` (MIT)
- Cuándo usarla: Screen US stocks for high-quality dividend opportunities combining value characteristics (P/E ratio under 20, P/B ratio under 2), attractive yields (3% or higher), and consistent growth (dividend/revenue/EPS trending up over 3 years). Supports two-stage screening using FINVIZ Elite API for efficient pre-filtering followed by FMP API for detailed analysis. Use when user requests dividend stock screening, income portfolio ideas, or quality value stocks with strong fundamentals.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/value-dividend-screener/` (requirements.txt, fmp_client.py, screen_dividend_stocks.py)

# Value Dividend Screener

## Overview

This skill identifies high-quality dividend stocks that combine value characteristics, attractive income generation, and consistent growth using a **two-stage screening approach**:

1. **FINVIZ Elite API (Optional but Recommended)**: Pre-screen stocks with basic criteria (fast, cost-effective)
2. **Financial Modeling Prep (FMP) API**: Detailed fundamental analysis of candidates

Screen US equities based on quantitative criteria including valuation ratios, dividend metrics, financial health, and profitability. Generate comprehensive reports ranking stocks by composite quality scores with detailed fundamental analysis.

**Efficiency Advantage**: Using FINVIZ pre-screening can reduce FMP API calls by 90%, making this approach ideal for free-tier API users.

## When to Use

Invoke this skill when the user requests:
- "Find high-quality dividend stocks"
- "Screen for value dividend opportunities"
- "Show me stocks with strong dividend growth"
- "Find income stocks trading at reasonable valuations"
- "Screen for sustainable high-yield stocks"
- Any request combining dividend yield, valuation metrics, and fundamental analysis

## Workflow

### Step 1: Verify API Key Availability

**For Two-Stage Screening (Recommended):**

Check if both API keys are available:

```python
import os
fmp_api_key = os.environ.get('FMP_API_KEY')
finviz_api_key = os.environ.get('FINVIZ_API_KEY')
```

If not available, ask user to provide API keys or set environment variables:
```bash
export FMP_API_KEY=your_fmp_key_here
export FINVIZ_API_KEY=your_finviz_key_here
```

**For FMP-Only Screening:**

Check if FMP API key is available:

```python
import os
api_key = os.environ.get('FMP_API_KEY')
```

If not available, ask user to provide API key or set environment variable:
```bash
export FMP_API_KEY=your_key_here
```

**FINVIZ Elite API Key:**
- Requires FINVIZ Elite subscription (~$40/month or ~$330/year)
- Provides access to CSV export of pre-screened results
- Highly recommended for reducing FMP API usage

Provide instructions from `references/fmp_api_guide.md` if needed.

### Step 2: Execute Screening Script

Run the screening script with appropriate parameters:

#### **Two-Stage Screening (RECOMMENDED)**

Uses FINVIZ for pre-screening, then FMP for detailed analysis:

**Default execution (Top 20 stocks):**
```bash
python3 scripts/screen_dividend_stocks.py --use-finviz
```

**With explicit API keys:**
```bash
python3 scripts/screen_dividend_stocks.py --use-finviz \
  --fmp-api-key $FMP_API_KEY \
  --finviz-api-key $FINVIZ_API_KEY
```

**Custom top N:**
```bash
python3 scripts/screen_dividend_stocks.py --use-finviz --top 50
```

**Custom output location:**
```bash
python3 scripts/screen_dividend_stocks.py --use-finviz --output /path/to/results.json
```

**Script behavior (Two-Stage):**
1. FINVIZ Elite pre-screening:
   - Market cap: Mid-cap or higher
   - Dividend yield: 3%+
   - Dividend growth (3Y): 5%+
   - EPS growth (3Y): Positive
   - P/B: Under 2
   - P/E: Under 20
   - Sales growth (3Y): Positive
   - Geography: USA
2. FMP detailed analysis of FINVIZ results (typically 20-50 stocks):
   - Dividend growth rate calculation (3-year CAGR)
   - Revenue and EPS trend analysis
   - Dividend sustainability assessment (payout ratios, FCF coverage)
   - Financial health metrics (debt-to-equity, current ratio)
   - Quality scoring (ROE, profit margins)
3. Composite scoring and ranking
4. Output top N stocks to JSON file

**Expected runtime (Two-Stage):** 2-3 minutes for 30-50 FINVIZ candidates (much faster than FMP-only)

#### **FMP-Only Screening (Original Method)**

Uses only FMP Stock Screener API (higher API usage):

**Default execution:**
```bash
python3 scripts/screen_dividend_stocks.py
```

**With explicit API key:**
```bash
python3 scripts/screen_dividend_stocks.py --fmp-api-key $FMP_API_KEY
```

**Script behavior (FMP-Only):**
1. Initial screening using FMP Stock Screener API (dividend yield >=3.0%, P/E <=20, P/B <=2)
2. Detailed analysis of candidates (typically 100-300 stocks):
   - Same detailed analysis as two-stage approach
3. Composite scoring and ranking
4. Output top N stocks to JSON file

**Expected runtime (FMP-Only):** 5-15 minutes for 100-300 candidates (rate limiting applies)

**API Usage Comparison:**
- Two-Stage: ~50-100 FMP API calls (FINVIZ pre-filters to ~30 stocks)
- FMP-Only: ~500-1500 FMP API calls (analyzes all screener results)

### Step 3: Parse and Analyze Results

Read the generated JSON file:

```python
import json

with open('dividend_screener_results.json', 'r') as f:
    data = json.load(f)

metadata = data['metadata']
stocks = data['stocks']
```

**Key data points per stock:**
- Basic info: `symbol`, `company_name`, `sector`, `market_cap`, `price`
- Valuation: `dividend_yield`, `pe_ratio`, `pb_ratio`
- Growth metrics: `dividend_cagr_3y`, `revenue_cagr_3y`, `eps_cagr_3y`
- Sustainability: `payout_ratio`, `fcf_payout_ratio`, `fcf_amount`, `fcf_status`, `fcf_coverage_status`, `sustainability_basis`, `dividend_sustainable`, `sustainability_bonus`, `sustainability_note`
- Financial health: `debt_to_equity`, `current_ratio`, `financially_healthy`
- Quality: `roe`, `profit_margin`, `quality_score`
- Overall ranking: `composite_score`

### Step 4: Generate Markdown Report

Create structured markdown report for user with following sections:

#### Report Structure

```markdown
# Value Dividend Stock Screening Report

**Generated:** [Timestamp]
**Screening Criteria:**
- Dividend Yield: >= 3.5%
- P/E Ratio: <= 20
- P/B Ratio: <= 2
- Dividend Growth (3Y CAGR): >= 5%
- Revenue Trend: Positive over 3 years
- EPS Trend: Positive over 3 years

**Total Results:** [N] stocks

---

## Top 20 Stocks Ranked by Composite Score

| Rank | Symbol | Company | Yield | P/E | Div Growth | Score |
|------|--------|---------|-------|-----|------------|-------|
| 1 | [TICKER] | [Name] | [%] | [X.X] | [%] | [XX.X] |
| ... |

---

## Detailed Analysis

### 1. [SYMBOL] - [Company Name] (Score: XX.X)

**Sector:** [Sector Name]
**Market Cap:** $[X.XX]B
**Current Price:** $[XX.XX]

**Valuation Metrics:**
- Dividend Yield: [X.X]%
- P/E Ratio: [XX.X]
- P/B Ratio: [X.X]

**Growth Profile (3-Year):**
- Dividend CAGR: [X.X]% [✓ Consistent / ⚠ One cut]
- Revenue CAGR: [X.X]%
- EPS CAGR: [X.X]%

**Dividend Sustainability:**
- Payout Ratio: [XX]%
- FCF Payout Ratio: [XX]%
- FCF Observed: [amount or unavailable] ([POSITIVE / ZERO / NEGATIVE / MISSING_DATA])
- FCF Coverage: [COVERED / AT_LIMIT / INSUFFICIENT_FCF / ZERO_FCF / NEGATIVE_FCF / MISSING_DATA / NO_DIVIDEND]
- Decision Basis: [EARNINGS_AND_FCF / FFO]
- Status: [✓ Sustainable / ⚠ Not confirmed]; Bonus: [0 / 10] points
- Explanation: [sustainability_note]

**Financial Health:**
- Debt-to-Equity: [X.XX]
- Current Ratio: [X.XX]
- Status: [✓ Healthy / ⚠ Caution]

**Quality Metrics:**
- ROE: [XX]%
- Net Profit Margin: [XX]%
- Quality Score: [XX]/100

**Investment Considerations:**
- [Key strength 1]
- [Key strength 2]
- [Risk factor or consideration]

---

[Repeat for other top stocks]

---

## Portfolio Construction Guidance

**Diversification Recommendations:**
- Sector breakdown of top 20 results
- Suggested allocation strategy
- Concentration risk warnings

**Monitoring Recommendations:**
- Key metrics to track quarterly
- Warning signs for each position
- Rebalancing triggers

**Risk Considerations:**
- Market cap concentration
- Sector biases in results
- Economic sensitivity warnings
```

In the human report, keep observed FCF and dividend coverage separate. Negative FCF means an observed shortfall; zero FCF means no cash coverage; `MISSING_DATA` means the source fields were unavailable. None proves a future dividend cut. `AT_LIMIT` means FCF equals dividends with no buffer and earns no bonus. For confirmed REITs, use FFO as the decision basis and show FCF status as context even when it is negative; do not apply FFO treatment to a company solely because its sector is Real Estate. Copy `sustainability_note` into the explanation rather than replacing an unknown status with a sustainability claim.

### Step 5: Provide Context and Methodology

Reference screening methodology when explaining results:

**Key concepts to explain:**
- Why these specific thresholds (3.5% yield, P/E 20, P/B 2)
- Importance of dividend growth vs. static high yield
- How composite score balances value, growth, and quality
- Dividend sustainability vs. dividend trap distinction
- Financial health metrics significance

Load `references/screening_methodology.md` to provide detailed explanations of:
- Phase 1: Initial quantitative filters
- Phase 2: Growth quality filters
- Phase 3: Sustainability and quality analysis
- Composite scoring system
- Investment philosophy and limitations

### Step 6: Answer Follow-up Questions

Anticipate common user questions:

**"Why did [stock] not make the list?"**
- Check which criteria it failed (yield, valuation, growth, sustainability)
- Explain the specific filter that excluded it

**"Can I screen for specific sectors?"**
- Filtering capability exists in script (modify line 383-388)
- Suggest re-running with sector parameter additions

**"What if I want higher/lower yield threshold?"**
- Script parameters are adjustable
- Trade-offs between yield and growth
- Recommend re-screening with new parameters

**"How often should I re-run this screen?"**
- Quarterly recommended (aligns with earnings cycles)
- Semi-annually sufficient for long-term holders
- Market conditions may warrant more frequent checks

**"How many stocks should I buy?"**
- Diversification guidance: minimum 10-15 for dividend portfolio
- Sector balance considerations
- Position sizing based on risk tolerance

## Resources

### scripts/screen_dividend_stocks.py

Comprehensive screening script that:
- Interfaces with FMP API for data retrieval
- Implements multi-phase filtering logic
- Calculates growth rates (CAGR) over 3-year periods
- Evaluates dividend sustainability via payout ratios and FCF coverage
- Assesses financial health (debt-to-equity, current ratio)
- Computes quality scores (ROE, profit margins)
- Ranks stocks by composite scoring system
- Outputs structured JSON results

**Dependencies:** `requests` library (install via `pip install requests`)

**Rate limiting:** Built-in delays to respect FMP API limits (250 requests/day free tier)

**Error handling:** Graceful degradation for missing data, rate limit retries, API errors

### references/screening_methodology.md

Comprehensive documentation of screening approach:

**Phase 1: Initial Quantitative Filters**
- Dividend yield >= 3.5% rationale and calculation
- P/E ratio <= 20 threshold justification
- P/B ratio <= 2 valuation logic

**Phase 2: Growth Quality Filters**
- Dividend growth (3-year CAGR >= 5%)
- Revenue positive trend analysis
- EPS positive trend analysis

**Phase 3: Quality & Sustainability Analysis**
- Dividend sustainability metrics (payout ratios, FCF coverage)
- Financial health indicators (D/E, current ratio)
- Quality scoring methodology (ROE, profit margins)

**Composite Scoring System (0-100 points)**
- Score component breakdown and weighting
- Interpretation guidelines

**Investment Philosophy**
- Why this approach works
- What this strategy avoids (dividend traps, value traps)
- Ideal candidate profile

**Usage Notes & Limitations**
- Best practices for portfolio construction
- When to sell criteria
- Historical context for threshold selection

### references/fmp_api_guide.md

Complete guide for Financial Modeling Prep API:

**API Key Setup**
- Obtaining free API key
- Setting environment variables
- Free tier limits (250 requests/day)

**Key Endpoints Used**
- Stock Screener API
- Income Statement API
- Balance Sheet API
- Cash Flow Statement API
- Key Metrics API
- Historical Dividend API

**Rate Limiting Strategy**
- Built-in protection in script
- Request budget management
- Best practices for free tier

**Error Handling**
- Common errors and solutions
- Debugging techniques

**Data Quality Considerations**
- Data freshness and gaps
- Data accuracy caveats
- When to verify with SEC filings

## Advanced Usage

### Customizing Screening Criteria

Modify thresholds in `scripts/screen_dividend_stocks.py`:

**Line 383-388** - Initial screening parameters:
```python
candidates = client.screen_stocks(
    dividend_yield_min=3.5,  # Adjust yield threshold
    pe_max=20,               # Adjust P/E threshold
    pb_max=2,                # Adjust P/B threshold
    market_cap_min=2_000_000_000  # Minimum $2B market cap
)
```

**Line 423** - Dividend CAGR threshold:
```python
if not div_cagr or div_cagr < 5.0:  # Adjust growth threshold
```

### Sector-Specific Screening

Add sector filtering after initial screening:

```python
# Filter for specific sectors
target_sectors = ['Consumer Defensive', 'Utilities', 'Healthcare']
candidates = [s for s in candidates if s.get('sector') in target_sectors]
```

### Excluding REITs and Financials

REITs and financial stocks have different dividend characteristics (higher payouts, different metrics):

```python
# Exclude REITs and Financials
exclude_sectors = ['Real Estate', 'Financial Services']
candidates = [s for s in candidates if s.get('sector') not in exclude_sectors]
```

### Exporting to CSV

Convert JSON results to CSV for Excel analysis:

```python
import json
import csv

with open('dividend_screener_results.json', 'r') as f:
    data = json.load(f)

stocks = data['stocks']

with open('screening_results.csv', 'w', newline='') as csvfile:
    if stocks:
        fieldnames = stocks[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(stocks)
```

## Troubleshooting

### "ERROR: requests library not found"
**Solution:** Install requests library
```bash
pip install requests
```

### "ERROR: FMP API key required"
**Solution:** Set environment variable or provide via command-line
```bash
export FMP_API_KEY=your_key_here
# OR
python3 scripts/screen_dividend_stocks.py --fmp-api-key your_key_here
```

### "ERROR: FINVIZ API key required when using --use-finviz"
**Solution:** Set environment variable or provide via command-line
```bash
export FINVIZ_API_KEY=your_key_here
# OR
python3 scripts/screen_dividend_stocks.py --use-finviz --finviz-api-key your_key_here
```

**Note:** FINVIZ Elite subscription required (~$40/month or ~$330/year)

### "ERROR: FINVIZ API authentication failed"
**Possible causes:**
1. Invalid FINVIZ API key
2. FINVIZ Elite subscription expired
3. API key format incorrect

**Solution:**
- Verify FINVIZ Elite subscription is active
- Check API key for typos (should be alphanumeric string)
- Log into FINVIZ Elite account and verify API key in settings
- Try accessing FINVIZ Elite screener manually to confirm subscription

### "ERROR: FINVIZ pre-screening failed or returned no results"
**Possible causes:**
1. FINVIZ API connection issue
2. Screening criteria too restrictive (no stocks match)
3. Market conditions (bear market may yield fewer results)

**Solution:**
- Check internet connection
- Verify FINVIZ Elite website is accessible
- Try FMP-only method as fallback:
  ```bash
  python3 scripts/screen_dividend_stocks.py
  ```

### "WARNING: Rate limit exceeded"
**Solution:** Script automatically retries after 60 seconds. If persistent:
- Wait until next day (free tier resets daily)
- Reduce number of stocks analyzed (modify line 394 limit)
- Consider upgrading to paid FMP tier

### "No stocks found matching all criteria"
**Solution:** Criteria may be too restrictive
- Relax P/E threshold (increase from 20)
- Lower dividend yield requirement (decrease from 3.5%)
- Reduce dividend growth requirement (decrease from 5%)
- Check market conditions (bear markets may have fewer qualifiers)

### Script runs slowly
**Expected behavior:** Script includes 0.3s delay between API calls for rate limiting
- 100 stocks analyzed = ~8-10 minutes
- First 20-30 qualifying stocks usually found within first 50-70 analyzed

## Performance & Cost Optimization

### API Call Comparison

**Two-Stage Screening (FINVIZ + FMP):**
- FINVIZ: 1 API call
- FMP Quote API: ~30-50 calls (one per pre-screened symbol)
- FMP Financial Data: ~150-250 calls (5 endpoints × 30-50 symbols)
- **Total FMP calls: ~180-300**

**FMP-Only Screening:**
- FMP Stock Screener: 1 call (returns 100-1000 stocks)
- FMP Financial Data: ~500-5000 calls (5 endpoints × 100-1000 symbols)
- **Total FMP calls: ~500-5000**

**Savings: 60-94% reduction in FMP API usage**

### Cost Analysis

**FINVIZ Elite:**
- Monthly: $39.50
- Annual: $299.50 (~$24.96/month)

**FMP API:**
- Free tier: 250 calls/day (sufficient for two-stage screening)
- Starter tier: $29.99/month for 750 calls/day
- Professional tier: $79.99/month for 2000 calls/day

**Recommendation:**
- **For free FMP tier users**: Use two-stage screening (FINVIZ + FMP free tier)
- **For paid FMP tier users**: Either approach works; two-stage is faster
- **Budget option**: FMP-only with free tier (run screening every few days)
- **Optimal option**: FINVIZ Elite ($330/year) + FMP free tier = Complete solution

## Version History

- **v1.1** (November 2025): Added FINVIZ Elite integration for two-stage screening
- **v1.0** (November 2025): Initial release with comprehensive multi-phase screening


## Shared FMP client

FMP data access uses the bundled generated `scripts/fmp_client.py`. Existing CLI
key/environment precedence, financial calculations and successful output shapes
are preserved. The migrated paths use stable endpoints only; a denied or failed
stable request does not fall back to retired v3 URLs. The shared client masks raw
and URL-encoded key echoes, retries malformed JSON once, and retries a 429 once
with a 60-second wait before stopping on a repeated rate limit. FINVIZ, where
used, remains a separate client.

### Referencia: references/fmp_api_guide.md

# Financial Modeling Prep (FMP) API Guide

## Overview

Financial Modeling Prep provides comprehensive financial data APIs for stocks, forex, cryptocurrencies, and more. This guide focuses on endpoints used for dividend stock screening.

## API Key Setup

### Obtaining an API Key

1. Visit https://financialmodelingprep.com/developer/docs
2. Sign up for a free account
3. Navigate to Dashboard → API Keys
4. Copy your API key

### Free Tier Limits

- **250 requests per day**
- **Rate limit**: ~5 requests per second
- **No credit card required**
- Sufficient for daily/weekly screening runs

### Paid Tiers (Optional)

- **Starter ($14/month)**: 500 requests/day
- **Professional ($29/month)**: 1,000 requests/day
- **Enterprise ($99/month)**: 10,000 requests/day

## Setting API Key

### Method 1: Environment Variable (Recommended)

**Linux/macOS:**
```bash
export FMP_API_KEY=your_api_key_here
```

**Windows (Command Prompt):**
```cmd
set FMP_API_KEY=your_api_key_here
```

**Windows (PowerShell):**
```powershell
$env:FMP_API_KEY="your_api_key_here"
```

**Persistent (add to shell profile):**
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export FMP_API_KEY=your_api_key_here' >> ~/.bashrc
source ~/.bashrc
```

### Method 2: Command-Line Argument

```bash
python3 scripts/screen_dividend_stocks.py --api-key your_api_key_here
```

## Key Endpoints Used

### 1. Stock Screener

**Endpoint:** `/v3/stock-screener`

**Purpose:** Initial filtering by dividend yield, P/E, P/B, market cap

**Parameters:**
- `dividendYieldMoreThan`: Minimum dividend yield (e.g., 3.5)
- `priceEarningRatioLowerThan`: Maximum P/E ratio (e.g., 20)
- `priceToBookRatioLowerThan`: Maximum P/B ratio (e.g., 2)
- `marketCapMoreThan`: Minimum market cap (e.g., 2000000000 = $2B)
- `exchange`: Exchanges to include (e.g., "NASDAQ,NYSE")
- `limit`: Max results (default: 1000)

**Example Request:**
```
https://financialmodelingprep.com/api/v3/stock-screener?
  dividendYieldMoreThan=3.5&
  priceEarningRatioLowerThan=20&
  priceToBookRatioLowerThan=2&
  marketCapMoreThan=2000000000&
  exchange=NASDAQ,NYSE&
  limit=1000&
  apikey=YOUR_API_KEY
```

**Response Format:**
```json
[
  {
    "symbol": "T",
    "companyName": "AT&T Inc.",
    "marketCap": 150000000000,
    "sector": "Communication Services",
    "industry": "Telecom Services",
    "beta": 0.65,
    "price": 20.50,
    "lastAnnualDividend": 1.11,
    "volume": 35000000,
    "exchange": "NYSE",
    "exchangeShortName": "NYSE",
    "country": "US",
    "isEtf": false,
    "isActivelyTrading": true,
    "dividendYield": 0.0541,
    "pe": 7.5,
    "priceToBook": 1.2
  }
]
```

### 2. Income Statement

**Endpoint:** `/v3/income-statement/{symbol}`

**Purpose:** Revenue, EPS, net income analysis

**Parameters:**
- `symbol`: Stock ticker (e.g., "AAPL")
- `limit`: Number of periods (e.g., 5 for 5 years)
- `period`: "annual" or "quarter"

**Example Request:**
```
https://financialmodelingprep.com/api/v3/income-statement/AAPL?
  limit=5&
  apikey=YOUR_API_KEY
```

**Key Fields Used:**
- `revenue`: Total revenue
- `eps`: Earnings per share
- `netIncome`: Net income
- `date`: Fiscal period end date

### 3. Balance Sheet Statement

**Endpoint:** `/v3/balance-sheet-statement/{symbol}`

**Purpose:** Debt, equity, liquidity analysis

**Parameters:**
- `symbol`: Stock ticker
- `limit`: Number of periods

**Key Fields Used:**
- `totalDebt`: Total debt (short-term + long-term)
- `totalStockholdersEquity`: Shareholders' equity
- `totalCurrentAssets`: Current assets
- `totalCurrentLiabilities`: Current liabilities

### 4. Cash Flow Statement

**Endpoint:** `/v3/cash-flow-statement/{symbol}`

**Purpose:** Free cash flow, dividends paid analysis

**Parameters:**
- `symbol`: Stock ticker
- `limit`: Number of periods

**Key Fields Used:**
- `operatingCashFlow`: Cash from operations
- `capitalExpenditure`: Capex (negative value)
- `dividendsPaid`: Dividends paid (negative value)
- `freeCashFlow`: OCF - Capex

### 5. Key Metrics

**Endpoint:** `/v3/key-metrics/{symbol}`

**Purpose:** ROE, ROA, and other quality metrics

**Parameters:**
- `symbol`: Stock ticker
- `limit`: Number of periods

**Key Fields Used:**
- `roe`: Return on Equity (decimal, e.g., 0.15 = 15%)
- `roa`: Return on Assets
- `roic`: Return on Invested Capital
- `debtToEquity`: Debt-to-equity ratio
- `currentRatio`: Current ratio

### 6. Historical Dividend

**Endpoint:** `/v3/historical-price-full/stock_dividend/{symbol}`

**Purpose:** Dividend history for growth rate calculation

**Example Request:**
```
https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/AAPL?
  apikey=YOUR_API_KEY
```

**Response Format:**
```json
{
  "symbol": "AAPL",
  "historical": [
    {
      "date": "2024-11-08",
      "label": "November 08, 24",
      "adjDividend": 0.25,
      "dividend": 0.25,
      "recordDate": "2024-11-11",
      "paymentDate": "2024-11-14",
      "declarationDate": "2024-10-31"
    }
  ]
}
```

## Rate Limiting Strategy

### Built-in Protection

The screening script includes rate limiting:
- **0.3 second delay** between requests (~3 requests/second)
- **Automatic retry** on 429 (rate limit exceeded) with 60-second backoff
- **Timeout**: 30 seconds per request

### Managing Request Budget

For free tier (250 requests/day):

**Requests per stock analyzed:**
- Stock Screener: 1 request (returns 100-1000 stocks)
- Income Statement: 1 request per symbol
- Balance Sheet: 1 request per symbol
- Cash Flow: 1 request per symbol
- Key Metrics: 1 request per symbol
- Dividend History: 1 request per symbol

**Total: 5 requests per symbol + 1 screener request**

**Budget allocation:**
- Initial screener: 1 request
- Detailed analysis: 5 × N stocks = 5N requests
- **Maximum stocks per run**: (250 - 1) / 5 = ~49 stocks

**Script default**: Analyzes first 100 candidates but typically finds ~20-30 that pass all criteria

### Best Practices

1. **Run during off-peak hours**: Lower chance of rate limits
2. **Space out runs**: Once daily or weekly, not multiple times per hour
3. **Cache results**: Save JSON output and analyze locally
4. **Upgrade if needed**: If screening large universes frequently, consider paid tier

## Error Handling

### Common Errors

**1. Invalid API Key**
```json
{
  "Error Message": "Invalid API KEY. Please retry or visit our documentation."
}
```
**Solution**: Check API key, verify it's active in FMP dashboard

**2. Rate Limit Exceeded (429)**
```json
{
  "Error Message": "You have exceeded the rate limit. Please wait."
}
```
**Solution**: Script automatically retries after 60 seconds

**3. Symbol Not Found**
```json
{
  "Error Message": "Invalid ticker symbol"
}
```
**Solution**: Script skips symbol and continues (expected for delisted/invalid tickers)

**4. Insufficient Data**
- Empty array returned for financial statements
**Solution**: Script skips symbol (common for newly listed stocks or incomplete data)

### Debugging

**Check request count:**
```bash
# Count API calls in script output
python3 scripts/screen_dividend_stocks.py 2>&1 | grep "Analyzing" | wc -l
```

**Verbose mode (add to script if needed):**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Data Quality Considerations

### Data Freshness

- **Annual statements**: Updated after fiscal year end (delays possible)
- **Quarterly data**: Available ~1-2 months after quarter end
- **Real-time prices**: Updated during market hours
- **Dividend history**: Updated after declaration/payment

### Data Gaps

Some stocks may have:
- **Incomplete history**: < 4 years of data (newly public companies)
- **Missing dividends**: Not all dividend-paying stocks report via API
- **Inconsistent metrics**: Different accounting standards, restatements

**Script behavior**: Skips stocks with insufficient data (requires 4+ years)

### Data Accuracy

FMP sources data from:
- SEC EDGAR filings (US companies)
- Company investor relations
- Exchange data feeds

**Note**: Always verify critical investment decisions with company filings (10-K, 10-Q)

## API Documentation

**Official Docs**: https://financialmodelingprep.com/developer/docs

**Key Sections:**
- Stock Fundamentals API
- Stock Screener API
- Historical Dividend API
- Ratios API

**Support**: support@financialmodelingprep.com

## Alternative Data Sources

If FMP limits are restrictive:

1. **Alpha Vantage**: Free tier, 500 requests/day
2. **Yahoo Finance (yfinance)**: Free, unlimited (but less reliable)
3. **Quandl/Nasdaq Data Link**: Free tier available
4. **IEX Cloud**: Free tier, 50k messages/month

**Note**: Alternative sources may require script modifications for different data formats.

### Referencia: references/screening_methodology.md

# Value Dividend Stock Screening Methodology

## Overview

This screening methodology identifies high-quality dividend stocks that combine:
- **Value characteristics**: Reasonable valuations (low P/E, P/B)
- **Income generation**: Attractive dividend yields (>=3.5%)
- **Growth profile**: Consistent dividend, revenue, and EPS growth
- **Quality metrics**: Strong profitability, financial health, and dividend sustainability

## Screening Criteria

### Phase 1: Initial Quantitative Filters

#### 1. Dividend Yield >= 3.5%
**Rationale**: Provides meaningful income above typical market yields (S&P 500 average: ~1.5-2%)

**Calculation**:
```
Dividend Yield = (Annual Dividends per Share / Current Stock Price) × 100
```

**Threshold Logic**:
- 3.5%+ provides attractive income
- Not so high as to signal dividend risk (>8% often unsustainable)
- Balances income and growth potential

#### 2. P/E Ratio <= 20
**Rationale**: Identifies stocks trading at reasonable multiples relative to earnings

**Calculation**:
```
P/E Ratio = Market Price per Share / Earnings per Share (TTM)
```

**Threshold Logic**:
- S&P 500 historical average: ~15-18x
- P/E <= 20 indicates value territory
- Excludes overvalued growth stocks
- Focuses on mature, profitable companies

#### 3. P/B Ratio <= 2.0
**Rationale**: Ensures stock price is reasonable relative to book value

**Calculation**:
```
P/B Ratio = Market Price per Share / Book Value per Share
```

**Threshold Logic**:
- P/B <= 2.0 suggests reasonable valuation
- Avoids paying excessive premium over net assets
- Particularly relevant for asset-heavy businesses

### Phase 2: Growth Quality Filters

#### 4. Dividend Growth: 3-Year CAGR >= 5%
**Rationale**: Identifies companies with consistent dividend-raising track record

**Calculation**:
```
Dividend CAGR = [(End Dividend / Start Dividend)^(1/3) - 1] × 100
```

**Threshold Logic**:
- 5% annual growth compounds meaningfully over time
- Demonstrates management confidence in cash flows
- Protects against inflation (long-term average: 2-3%)
- Signals business health and shareholder commitment

**Consistency Check**:
- No dividend cuts in the period
- Allows one year of flat dividends (economic cycles)
- Cuts signal financial stress or strategy changes

#### 5. Revenue Growth: Positive 3-Year Trend
**Rationale**: Confirms top-line growth supports dividend sustainability

**Evaluation**:
- Revenue in Year 3 > Revenue in Year 1
- Allows one year of decline (cyclical businesses, one-time events)
- Overall upward trajectory required

**Why Not a Fixed %**:
- Different industries have different growth rates
- Mature dividend stocks may have modest but stable growth
- Focus is on **trend direction** rather than absolute rate

#### 6. EPS Growth: Positive 3-Year Trend
**Rationale**: Ensures earnings power is expanding, not eroding

**Evaluation**:
- EPS in Year 3 > EPS in Year 1
- Allows one year of decline
- Overall upward trajectory required

**Significance**:
- Earnings fund dividends
- EPS growth = potential for future dividend increases
- Distinguishes quality companies from dividend traps

### Phase 3: Quality & Sustainability Analysis

#### 7. Dividend Sustainability Metrics

**A. Payout Ratio**
```
Payout Ratio = (Dividends Paid / Net Income) × 100
```

**Healthy Range**: 30-70%
- < 30%: Conservative, room for growth
- 30-70%: Balanced, sustainable
- > 80%: Caution, limited flexibility

**B. Free Cash Flow Payout Ratio**
```
FCF Payout Ratio = (Dividends Paid / Free Cash Flow) × 100
where FCF = Operating Cash Flow - Capital Expenditures
```

**Healthy Range**: < 100%
- FCF is the true source of sustainable dividends
- < 100%: Dividends covered by actual cash generation
- > 100%: Unsustainable, funded by debt or asset sales

**Sustainability Flag**: ✅ if Payout Ratio < 80% AND FCF Payout Ratio < 100%

#### 8. Financial Health Metrics

**A. Debt-to-Equity Ratio**
```
D/E Ratio = Total Debt / Shareholders' Equity
```

**Healthy Range**: < 2.0
- Lower is generally better
- Varies by industry (utilities typically higher)
- < 2.0: Reasonable leverage, not overleveraged

**B. Current Ratio**
```
Current Ratio = Current Assets / Current Liabilities
```

**Healthy Range**: > 1.0 (ideally > 1.5)
- > 1.0: Can cover short-term obligations
- > 1.5: Strong liquidity cushion
- < 1.0: Liquidity risk

**Health Flag**: ✅ if D/E < 2.0 AND Current Ratio > 1.0

#### 9. Quality Score (0-100)

**Components**:

**A. Return on Equity (ROE)** - Max 50 points
```
ROE = Net Income / Shareholders' Equity

Points = min((ROE% / 20%) × 50, 50)
```

- 20%+ ROE = 50 points (excellent capital efficiency)
- 10% ROE = 25 points (average)
- < 5% ROE = poor capital returns

**B. Net Profit Margin** - Max 50 points
```
Profit Margin = (Net Income / Revenue) × 100

Points = min((Margin% / 15%) × 50, 50)
```

- 15%+ margin = 50 points (highly profitable)
- 7.5% margin = 25 points (average)
- < 3% margin = low profitability

**Quality Score Interpretation**:
- 80-100: Excellent quality (high profitability, efficiency)
- 60-79: Good quality
- 40-59: Average quality
- < 40: Below average quality

## Composite Scoring System

### Purpose
Rank stocks by overall attractiveness, balancing value, growth, and quality.

### Score Components (Total: 100 points)

1. **Dividend Growth** (Max 20 points)
   - 10%+ CAGR = 20 points
   - 5% CAGR = 10 points
   - Linear scaling

2. **Revenue Growth** (Max 15 points)
   - 10%+ CAGR = 15 points
   - 5% CAGR = 7.5 points
   - Linear scaling

3. **EPS Growth** (Max 15 points)
   - 15%+ CAGR = 15 points
   - 7.5% CAGR = 7.5 points
   - Linear scaling

4. **Dividend Sustainability** (10 points)
   - Pass (sustainable) = 10 points
   - Fail = 0 points

5. **Financial Health** (10 points)
   - Pass (healthy) = 10 points
   - Fail = 0 points

6. **Quality Score** (Max 30 points)
   - Quality Score × 0.3
   - 100 quality = 30 points
   - 50 quality = 15 points

### Interpretation

- **80-100**: Exceptional (high growth, quality, sustainability)
- **60-79**: Strong (solid all-around profile)
- **40-59**: Good (meets criteria, some trade-offs)
- **20-39**: Acceptable (passes filters but lower quality)
- **< 20**: Marginal (barely meets criteria)

## Investment Philosophy

### Why This Approach Works

1. **Value + Growth + Quality**: Combines three proven factor premiums
2. **Dividend Focus**: Signals management discipline and cash generation
3. **Sustainability Screen**: Avoids dividend traps and value traps
4. **Growth Requirements**: Ensures businesses are healthy, not declining
5. **Quality Filters**: Identifies durable competitive advantages

### What This Strategy Avoids

1. **Dividend Traps**: High yields from struggling companies (growth filters catch these)
2. **Value Traps**: Cheap stocks that stay cheap (quality metrics catch these)
3. **Overvaluation**: Growth stocks trading at expensive multiples (P/E, P/B filters)
4. **Financial Risk**: Overleveraged or illiquid companies (health metrics)

### Ideal Candidate Profile

A stock scoring highly in this screen typically:
- Operates in stable, mature industry
- Has sustainable competitive advantage (moat)
- Generates consistent free cash flow
- Committed to shareholder returns (dividends)
- Trades at reasonable valuation (not hyped)
- Growing modestly but consistently
- Strong balance sheet and profitability

Examples: Dividend Aristocrats, quality REITs (if included), stable utilities, consumer staples leaders

## Usage Notes

### Limitations

1. **Market Cap Bias**: Typically finds large/mid-cap stocks (small-caps less likely to meet all criteria)
2. **Sector Bias**: May overweight certain sectors (utilities, consumer staples, REITs)
3. **Excludes High Growth**: Tech and growth stocks generally won't qualify (by design)
4. **Historical Performance**: Past growth doesn't guarantee future results
5. **Economic Sensitivity**: Some qualified stocks may be cyclical

### Best Practices

1. **Diversification**: Don't concentrate in top 5; spread across top 20
2. **Sector Balance**: Monitor sector exposure, avoid overconcentration
3. **Rescreen Regularly**: Quarterly or semi-annually; fundamentals change
4. **Valuation Check**: Just because it passed doesn't mean buy at any price
5. **Dividend Safety**: Monitor payout ratios and cash flows quarterly
6. **Hold for Long Term**: This is a quality dividend growth strategy, not trading

### When to Sell

1. **Dividend Cut**: Immediate red flag; review business health
2. **Deteriorating Fundamentals**: Revenue/EPS declining multiple quarters
3. **Payout Ratio > 100%**: Dividend unsustainable
4. **Debt Spike**: Leverage increasing significantly without clear reason
5. **Better Opportunities**: Capital allocation to higher-scoring stocks
6. **Valuation Extreme**: Stock becomes significantly overvalued (P/E > 30, for example)

## Historical Context

### Why 3.5% Yield Threshold?

- **US 10-Year Treasury**: Historically 2-4%
- **S&P 500 Dividend Yield**: 1.5-2%
- **Equity Risk Premium**: 3.5% provides ~1.5-2% premium over Treasuries
- **Tax Efficiency**: Qualified dividends taxed favorably vs. bonds

### Why P/E <= 20?

- **S&P 500 Historical Average**: ~15-18x
- **Fair Value Range**: 15-20x for mature, stable businesses
- **Margin of Safety**: Leaves room for multiple compression
- **Cyclically Adjusted**: Not overpaying at peak earnings

### Why 5% Dividend CAGR?

- **Inflation Protection**: Beats long-term inflation (2-3%)
- **Real Income Growth**: Provides rising purchasing power
- **Achievable**: Sustainable for quality companies
- **Compound Power**: 5% doubles in 14.4 years

## References

- Benjamin Graham: "The Intelligent Investor" (value investing principles)
- Jeremy Siegel: "The Future for Investors" (dividend growth research)
- CFA Institute: Equity Valuation standards
- S&P Dow Jones Indices: Dividend Aristocrats methodology
- Morningstar: Dividend Sustainability Research


---

## SKILL: vcp-screener

- Fuente: `tradermonty/claude-trading-skills` → `skills/vcp-screener` (MIT)
- Cuándo usarla: Screen S&P 500 stocks for Mark Minervini's Volatility Contraction Pattern (VCP) and detect historical VCPs in a single ticker's price path. Identifies Stage 2 uptrend stocks forming tight bases with contracting volatility near breakout pivot points; in historical single-ticker mode walks a multi-year history and emits every VCP that formed with forward-outcome stats (breakout / stop-hit / timeout). Use when user requests VCP screening, Minervini-style setups, tight base patterns, volatility contraction breakout candidates, Stage 2 momentum stock scanning, or historical VCP pattern study on a specific ticker (e.g. FIX, TSLA).
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/vcp-screener/` (requirements.txt, _fmp_compat.py, __init__.py, execution_state.py, forward_outcome.py, pattern_classifier.py, pivot_proximity_calculator.py, relative_strength_calculator.py, trend_template_calculator.py, vcp_pattern_calculator.py, volume_pattern_calculator.py, fmp_client.py …)

# VCP Screener - Minervini Volatility Contraction Pattern

Screen S&P 500 stocks for Mark Minervini's Volatility Contraction Pattern (VCP), identifying Stage 2 uptrend stocks with contracting volatility near breakout pivot points.

## When to Use

- User asks for VCP screening or Minervini-style setups
- User wants to find tight base / volatility contraction patterns
- User requests Stage 2 momentum stock scanning
- User asks for breakout candidates with defined risk
- User asks "find every historical VCP in <TICKER>" or wants to study one ticker's
  past VCP setups with forward outcomes (`--history --ticker SYM`)

## Prerequisites

- FMP API key (set `FMP_API_KEY` environment variable or pass `--api-key`)
- Free tier (250 calls/day) is sufficient for default screening (top 100 candidates)
- Paid tier recommended for full S&P 500 screening (`--full-sp500`)

## Workflow

### Step 1: Prepare and Execute Screening

Run the VCP screener script:

```bash
# Default: S&P 500, top 100 candidates
python3 skills/vcp-screener/scripts/screen_vcp.py --output-dir skills/vcp-screener/scripts

# Custom universe
python3 skills/vcp-screener/scripts/screen_vcp.py --universe AAPL NVDA MSFT AMZN META --output-dir skills/vcp-screener/scripts

# Full S&P 500 (paid API tier)
python3 skills/vcp-screener/scripts/screen_vcp.py --full-sp500 --output-dir skills/vcp-screener/scripts
```

### Strict Mode (Minervini pure setup)

Only return stocks with `valid_vcp=True` AND `execution_state` in `(Pre-breakout, Breakout)`:

```bash
python3 skills/vcp-screener/scripts/screen_vcp.py --strict --output-dir reports/
```

### Historical single-ticker mode

Walk one ticker's multi-year history, detect every VCP that ever formed, and
attach forward-outcome stats (breakout / stop-hit / timeout, days-to-outcome,
max gain, max loss) per detection. Useful for pattern study and backtesting
context — not a real-time screener.

```bash
# Default: scan ~5 years (1260 trading days), 5-day stride, 60-day outcome window
python3 skills/vcp-screener/scripts/screen_vcp.py \
  --history --ticker FIX --output-dir reports/

# Custom scan length: 750 trading days (~3 years), 90-day outcome window
python3 skills/vcp-screener/scripts/screen_vcp.py \
  --history 750 --ticker TSLA \
  --stride-days 5 --outcome-days 90 \
  --output-dir reports/

# Long scan: 10 years (2520 trading days)
python3 skills/vcp-screener/scripts/screen_vcp.py \
  --history 2520 --ticker NVDA --output-dir reports/
```

Outputs (timestamped):
- `vcp_history_<SYM>_<YYYY-MM-DD_HHMMSS>.json` — timeline of detections with full
  analyzer payload + `forward_outcome` per detection + summary stats.
- `vcp_history_<SYM>_<YYYY-MM-DD_HHMMSS>.md` — human-readable timeline.

Mode-specific flags:

| Parameter | Default | Range | Effect |
|-----------|---------|-------|--------|
| `--history [DAYS]` | (off) / 1260 if bare | 100-5040 | Enable historical mode; optionally specify trading-day scan window (requires `--ticker`) |
| `--ticker SYM` | — | — | Ticker to scan |
| `--stride-days` | 5 | 1-60 | Trading-day step between as-of cursor positions |
| `--outcome-days` | 60 | 5-252 | Forward window evaluated per detection |

Notes:
- Two FMP API calls per scan (ticker + SPY history), not 100+ like the
  cross-sectional pipeline.
- `marketCap` and absolute RS percentile reflect the ticker in isolation,
  not against the live screening universe — use this report for pattern
  study, not portfolio sizing.
- Detections are deduplicated by `(T1_high_date, last_low_date, pivot)` so
  the same VCP isn't reported repeatedly as the cursor ages.

### Advanced Tuning (for backtesting)

Adjust VCP detection parameters for research and backtesting:

```bash
python3 skills/vcp-screener/scripts/screen_vcp.py \
  --min-contractions 3 \
  --t1-depth-min 12.0 \
  --breakout-volume-ratio 2.0 \
  --trend-min-score 90 \
  --atr-multiplier 1.5 \
  --output-dir reports/
```

| Parameter | Default | Range | Effect |
|-----------|---------|-------|--------|
| `--min-contractions` | 2 | 2-4 | Higher = fewer but higher-quality patterns |
| `--t1-depth-min` | 10.0% | 1-50 | Higher = excludes shallow first corrections |
| `--breakout-volume-ratio` | 1.5x | 0.5-10 | Higher = stricter volume confirmation |
| `--trend-min-score` | 85 | 0-100 | Higher = stricter Stage 2 filter |
| `--atr-multiplier` | 1.5 | 0.5-5 | Lower = more sensitive swing detection |
| `--contraction-ratio` | 0.70 | 0.1-1 | Lower = requires tighter contractions |
| `--min-contraction-days` | 5 | 1-30 | Higher = longer minimum contraction |
| `--lookback-days` | 120 | 30-365 | Longer = finds older patterns |
| `--max-sma200-extension` | 50.0% | — | SMA200 distance threshold for Overextended state and penalty |
| `--wide-and-loose-threshold` | 15.0% | — | Final contraction depth above which wide-and-loose flag triggers |
| `--strict` | off | — | Minervini strict mode: only Pre-breakout or Breakout with valid VCP |

### Step 2: Review Results

1. Read the generated JSON and Markdown reports
2. Load `references/vcp_methodology.md` for pattern interpretation context
3. Load `references/scoring_system.md` for score threshold guidance

### Step 3: Present Analysis

For each top candidate, present:
- **Quality** (`composite_score` / rating) — how well-formed is the VCP pattern?
- **Execution State** (`execution_state`) — is it buyable now? (Pre-breakout / Breakout = actionable)
- **Pattern Type** (`pattern_type`) — Textbook VCP / VCP-adjacent / Post-breakout / Extended Leader / Damaged
- `★` marker if a State Cap was applied (raw score was downgraded)
- Contraction details (T1/T2/T3 depths and ratios)
- Trade setup: pivot price, stop-loss, risk percentage
- Volume dry-up ratio and breakout_volume_score
- Relative strength rank

### Step 4: Provide Actionable Guidance

**By Execution State (primary filter):**
- **Pre-breakout / Breakout:** Pattern is in the active entry window — apply rating-based sizing
- **Early-post-breakout:** Breakout underway but above ideal entry — reduced size or wait for pullback
- **Extended / Overextended:** Trade missed — add to watchlist for next base
- **Damaged / Invalid:** Setup invalidated — do not enter

**By Rating (secondary, after state confirms actionability):**
- **Textbook VCP (90+):** Buy at pivot with aggressive sizing (1.5-2x)
- **Strong VCP (80-89):** Buy at pivot with standard sizing (1x)
- **Good VCP (70-79):** Buy on volume confirmation above pivot (0.75x)
- **Developing (60-69):** Add to watchlist, wait for tighter contraction
- **Weak/No VCP (<60):** Monitor only or skip

## 3-Phase Pipeline

1. **Pre-Filter** - Quote-based screening (price, volume, 52w position) ~101 API calls
2. **Trend Template** - 7-point Stage 2 filter with 260-day histories ~100 API calls
3. **VCP Detection** - Pattern analysis, scoring, report generation (no additional API calls)

## Output

- `vcp_screener_YYYY-MM-DD_HHMMSS.json` - Structured results
- `vcp_screener_YYYY-MM-DD_HHMMSS.md` - Human-readable report

## Resources

- `references/vcp_methodology.md` - VCP theory and Trend Template explanation
- `references/scoring_system.md` - Scoring thresholds and component weights
- `references/fmp_api_endpoints.md` - API endpoints and rate limits

### Referencia: references/fmp_api_endpoints.md

# FMP API Endpoints Used by VCP Screener

## Endpoints

### 1. S&P 500 Constituents
- **URL:** `GET /stable/sp500-constituent`
- **Calls:** 1 (cached)
- **Returns:** `[{symbol, name, sector, subSector}, ...]`
- **Used in:** Phase 1 - Universe definition

### 2. Batch Quote
- **URL:** `GET /api/v3/quote/{symbols}` (comma-separated, max 5)
- **Calls:** ~101 (503 stocks / 5 per batch)
- **Returns:** `[{symbol, price, yearHigh, yearLow, avgVolume, marketCap, ...}]`
- **Used in:** Phase 1 - Pre-filter

### 3. Historical Prices
- **URL:** `GET /api/v3/historical-price-full/{symbol}?timeseries=260`
- **Calls:** 1 (SPY) + up to 100 (candidates)
- **Returns:** `{symbol, historical: [{date, open, high, low, close, adjClose, volume}, ...]}`
- **Used in:** Phase 2 - Trend Template, Phase 3 - VCP detection

## API Budget Summary

| Phase | Operation | API Calls |
|-------|-----------|-----------|
| 1 | S&P 500 constituents | 1 |
| 1 | Batch quotes (503 / 5) | ~101 |
| 2 | SPY 260-day history | 1 |
| 2 | Candidate histories (max 100) | 100 |
| **Total (default)** | | **~203** |
| **Total (--full-sp500)** | | **~350** |

## Rate Limits

- **Free tier:** 250 API calls/day - Default screening fits within this limit
- **Starter tier ($29.99/mo):** 750 calls/day
- **Rate limiting:** 0.3s delay between requests, automatic retry on 429
- **Caching:** In-memory session cache prevents duplicate requests

## Notes

- All historical data uses `timeseries=260` parameter (260 trading days = ~1 year)
- Phase 3 (VCP detection, scoring, reporting) requires NO additional API calls
- The `--full-sp500` flag fetches histories for all pre-filter passers (~250 stocks)

### Referencia: references/scoring_system.md

# VCP Screener Scoring System

## 5-Component Composite Score

| Component | Weight | Source |
|-----------|--------|--------|
| Trend Template (Stage 2) | 25% | 7-point Minervini criteria |
| Contraction Quality | 25% | VCP pattern detection |
| Volume Pattern | 20% | Volume dry-up analysis |
| Pivot Proximity | 15% | Distance from breakout level |
| Relative Strength | 15% | Minervini-weighted RS vs S&P 500 |

## Component Scoring Details

### 1. Trend Template (0-100)

Each of the 7 criteria contributes 14.3 points:

| Criteria Passed | Score | Status |
|-----------------|-------|--------|
| 7/7 | 100 | Perfect Stage 2 |
| 6/7 | 85.8 | Pass (minimum threshold) |
| 5/7 | 71.5 | Borderline |
| <= 4/7 | <= 57 | Fail |

**Pass threshold:** Raw score >= 85 (6+ criteria) to proceed to VCP analysis.

**SMA200 Extension Penalty** (metadata only -- NOT applied to the trend template score):

| Price above SMA200 | Penalty (stored as metadata) |
|--------------------|------------------------------|
| > 70% | -20 |
| > 60% | -15 |
| > 50% | -10 |
| > 40% | -5 |

The SMA200 penalty is computed and stored in `sma200_penalty` / `sma200_distance_pct` for downstream use by the Execution State engine (Overextended classification). It is intentionally excluded from the trend template score to avoid double-penalizing with state caps.

### 2. Contraction Quality (0-100)

| # Contractions | Base Score |
|----------------|-----------|
| 4 | 90 |
| 3 | 80 |
| 2 | 60 |
| 1 or invalid | 0-40 |

**Modifiers:**
- Tight final contraction (< 5% depth): +10
- Good average contraction ratio (< 0.4 of T1): +10
- Deep T1 (> 30%): -10

### 3. Volume Pattern (0-100)

Based on dry-up ratio (`Zone B avg volume / 50-day avg`):

| Dry-Up Ratio | Base Score |
|-------------|-----------|
| < 0.30 | 90 |
| 0.30-0.50 | 75 |
| 0.50-0.70 | 60 |
| 0.70-1.00 | 40 |
| > 1.00 | 20 |

**Zone-based analysis (when contractions are provided):**
- **Zone A**: Last contraction period (volume during tightening)
- **Zone B**: Pivot approach — bars 1-10 (bar[0] excluded to avoid breakout contamination)
- **Zone C**: Bar[0] if price > pivot (breakout bar volume)

**Zone B is the dry-up source.** Bar[0] (potential breakout bar) is intentionally excluded from the dry-up calculation. Its quality is tracked separately via `breakout_volume_score`.

**Breakout Volume Score (independent of dry-up):**
| Zone C ratio (bar[0] / 50d avg) | Score |
|----------------------------------|-------|
| ≥ 3.0x | 100 |
| 2.0x–2.9x | 80 |
| 1.5x–1.9x | 60 |
| 1.0x–1.4x | 30 |
| < 1.0x or below pivot | 0 |

**Modifiers to composite volume score:**
- Breakout on 1.5x+ volume (bar[0] above pivot): +10
- Net accumulation > 3 days (in 20d): +10
- Net distribution > 3 days (in 20d): -10
- Declining volume across contraction periods: +10

### 4. Pivot Proximity (0-100) — Distance-Priority Scoring

Scoring is distance-first. Volume confirmation adds a bonus only within 0-5% above pivot (Minervini: never chase >5% above pivot).

| Distance from Pivot | Base Score | Volume Bonus | Final Score | Trade Status |
|--------------------|-----------|-------------|------------|--------------|
| 0-3% above | 90 | +10 | 100 | BREAKOUT CONFIRMED |
| 3-5% above | 65 | +10 | 75 | EXTENDED - Moderate chase risk (vol confirmed) |
| 5-10% above | 50 | — (none) | 50 | EXTENDED - High chase risk |
| 10-20% above | 35 | — (none) | 35 | EXTENDED - Very high chase risk |
| >20% above | 20 | — (none) | 20 | OVEREXTENDED - Do not chase |
| 0 to -2% below | 90 | — | 90 | AT PIVOT (within 2%) |
| -2% to -5% | 75 | — | 75 | NEAR PIVOT |
| -5% to -8% | 60 | — | 60 | APPROACHING |
| -8% to -10% | 45 | — | 45 | DEVELOPING |
| -10% to -15% | 30 | — | 30 | EARLY |
| < -15% | 10 | — | 10 | FAR FROM PIVOT |

**Volume bonus rules:**
- 0-3% above pivot + volume: +10 points, status = "BREAKOUT CONFIRMED"
- 3-5% above pivot + volume: +10 points, "(vol confirmed)" appended to status
- >5% above pivot: no volume bonus (Minervini: do not chase extended breakouts)
- Below pivot: volume bonus not applicable

**Chase risk rule (Minervini):** Do not buy stocks >5% above their pivot point. Distance determines the base score; volume confirmation is a bonus, not an override.

### 5. Relative Strength (0-100)

Minervini weighting (emphasizes recent performance):
- 40%: Last 3 months (63 trading days)
- 20%: Last 6 months (126 trading days)
- 20%: Last 9 months (189 trading days)
- 20%: Last 12 months (252 trading days)

| Weighted RS vs S&P 500 | Score | RS Rank Estimate |
|-------------------------|-------|------------------|
| >= +50% | 100 | ~99 (top 1%) |
| >= +30% | 95 | ~95 (top 5%) |
| >= +20% | 90 | ~90 (top 10%) |
| >= +10% | 80 | ~80 (top 20%) |
| >= +5% | 70 | ~70 (top 30%) |
| >= 0% | 60 | ~60 (top 40%) |
| >= -5% | 50 | ~50 (average) |
| >= -10% | 40 | ~40 |
| >= -20% | 20 | ~25 |
| < -20% | 0 | ~10 |

## 2-Axis Scoring: Quality × Execution State

The screener separates two independent questions:

- **Axis 1 — Structure Quality** (`composite_score`): How well-formed is the VCP pattern? (unchanged 5-component weighted score)
- **Axis 2 — Execution State** (`execution_state`): Is the stock buyable *right now*?

These axes are computed independently and then combined through **State Caps**.

---

## Execution State Engine

`compute_execution_state()` applies a 10-rule decision tree and returns one of 7 states:

| State | Meaning |
|-------|---------|
| `Invalid` | Price below SMA50 < SMA200 — not a Stage 2 stock |
| `Damaged` | Price below last contraction low OR below SMA50 — pattern invalidated |
| `Overextended` | Price >50% above SMA200 OR >10% above pivot — late-cycle risk |
| `Extended` | Price 5-10% above pivot — elevated chase risk |
| `Early-post-breakout` | Price 3-5% above pivot, OR 0-3% above pivot without volume confirmation |
| `Breakout` | Price 0-3% above pivot with breakout volume confirmation (1.5x+ avg) |
| `Pre-breakout` | Price below pivot — ideal entry zone |

### State Caps

Each execution state imposes a maximum allowable rating regardless of composite score:

| Execution State | Maximum Rating | Rationale |
|----------------|----------------|-----------|
| `Invalid` | No VCP | Price structure failed completely |
| `Damaged` | No VCP | Pattern invalidated by breach of low |
| `Overextended` | Weak VCP | Too extended for a safe entry |
| `Extended` | Developing VCP | Chasing risk too high |
| `Early-post-breakout` | Strong VCP | Breakout in progress; watch for follow-through |
| `Breakout` | Textbook VCP | No cap — valid breakout |
| `Pre-breakout` | Textbook VCP | No cap — ideal setup |

When a cap is applied, `state_cap_applied=True` and `★` appears in the Quick Scan table.

### Wide-and-Loose Cap

When the final contraction has `depth_pct > 15%` AND `duration_days < 10`, the pattern is flagged as `wide_and_loose=True` and capped at **Developing VCP** (prevents Textbook/Strong/Good ratings for sloppy late contractions).

---

## Pattern Classifier

`classify_pattern()` assigns one of 5 pattern types based on structural characteristics:

| Pattern Type | Criteria |
|-------------|---------|
| `Textbook VCP` | valid_vcp=True, not wide_and_loose, 3+ contractions, final depth ≤10%, dry_up ≤0.70, state=Pre-breakout |
| `VCP-adjacent` | valid_vcp=True but misses one Textbook criterion |
| `Post-breakout` | state in (Breakout, Early-post-breakout) |
| `Extended Leader` | state in (Overextended, Extended) |
| `Damaged` | state in (Invalid, Damaged) |

---

## Rating Bands

| Composite Score | Rating | Position Sizing | Action |
|-----------------|--------|-----------------|--------|
| 90-100 | Textbook VCP | 1.5-2x normal | Buy at pivot, aggressive |
| 80-89 | Strong VCP | 1x normal | Buy at pivot, standard |
| 70-79 | Good VCP | 0.75x normal | Buy on volume confirmation |
| 60-69 | Developing VCP | Wait | Watchlist only |
| 50-59 | Weak VCP | Skip | Monitor only |
| < 50 | No VCP | Skip | Not actionable |

### Cap Priority

Multiple caps can apply simultaneously. The most restrictive (lowest) cap wins:

1. `valid_vcp=False` cap (Developing VCP max)
2. Execution State cap (per table above)
3. Wide-and-Loose cap (Developing VCP max)

The final displayed rating reflects all caps. `state_cap_applied=True` indicates at least one cap was applied.

## Entry Ready Conditions

A stock is classified as `entry_ready=True` when all of the following conditions are met:

| Condition | Default Threshold | CLI Override |
|-----------|-------------------|--------------|
| `execution_state` | Not in (Invalid, Damaged, Overextended, Extended, Early-post-breakout) | — |
| `valid_vcp` | `True` | `--no-require-valid-vcp` |
| `distance_from_pivot_pct` | -8.0% to +3.0% | `--max-above-pivot` |
| `dry_up_ratio` | <= 1.0 | — |
| `trade_status` | Not "BELOW STOP LEVEL" | — |
| `risk_pct` | > 0% and <= 15.0% | `--max-risk` |

**Report sections:**
- **Section A: Pre-Breakout Watchlist** — `entry_ready=True` stocks, sorted by composite score
- **Section B: Extended / Quality VCP** — `entry_ready=False` stocks, sorted by composite score

**CLI mode:**
- `--mode all` (default): Shows both sections
- `--mode prebreakout`: Shows only entry_ready=True stocks
- `--strict`: Minervini strict mode — only includes stocks with `valid_vcp=True` AND `execution_state in (Pre-breakout, Breakout)`

## Pre-Filter Criteria (Phase 1)

Quick filter using quote data only (no historical needed):

| Criterion | Threshold | Purpose |
|-----------|-----------|---------|
| Price | > $10 | Exclude penny stocks |
| % above 52w low | > 20% | Roughly in uptrend |
| % below 52w high | < 30% | Not in deep correction |
| Average volume | > 200,000 | Sufficient liquidity |

### Referencia: references/vcp_methodology.md

# VCP Methodology - Minervini's Volatility Contraction Pattern

## Overview

The Volatility Contraction Pattern (VCP) was developed by Mark Minervini, two-time U.S. Investing Championship winner. It identifies stocks in Stage 2 uptrends that are forming progressively tighter consolidation patterns before a potential breakout.

## Stage Analysis Foundation

### The 4 Stages (Stan Weinstein / Minervini)

1. **Stage 1 - Accumulation/Basing:** Stock trades sideways after a decline. Smart money accumulates.
2. **Stage 2 - Advancing/Uptrend:** Stock is in a confirmed uptrend. This is where VCPs form. **The only stage to buy.**
3. **Stage 3 - Distribution/Topping:** Stock stalls after an advance. Smart money distributes.
4. **Stage 4 - Declining/Downtrend:** Stock is in a confirmed downtrend. Avoid or short.

### Minervini's 7-Point Trend Template (Stage 2 Confirmation)

A stock MUST pass all (or nearly all) of these criteria to be in a confirmed Stage 2:

| # | Criterion | Purpose |
|---|-----------|---------|
| 1 | Price > 150-day SMA AND Price > 200-day SMA | Above major trend lines |
| 2 | 150-day SMA > 200-day SMA | Shorter MA above longer (bullish alignment) |
| 3 | 200-day SMA trending up for 22+ trading days | Long-term trend is up |
| 4 | Price > 50-day SMA | Above intermediate trend line |
| 5 | Price at least 25% above 52-week low | Sufficient distance from lows |
| 6 | Price within 25% of 52-week high | Not in a deep correction |
| 7 | Relative Strength rating > 70 | Outperforming most stocks |

**Pass threshold:** 6 of 7 criteria (score >= 85) to proceed to VCP detection.

## VCP Pattern Mechanics

### What is a VCP?

A VCP occurs when a stock in a Stage 2 uptrend pulls back and then rallies, but each successive pullback is **shallower** (less volatile) than the previous one. This "volatility contraction" signals that:

1. Selling pressure is being absorbed
2. Remaining sellers are being exhausted
3. Supply is drying up
4. A breakout becomes more probable

### Contraction Structure

```
        H1 (Highest swing high)
       / \
      /   \  T1 (First contraction: deepest)
     /     \
    /       L1
   /       / \
  /       /   \ T2 (Second contraction: tighter)
         H2    \
          \    L2
           \  / \
            \/   \ T3 (Third contraction: tightest)
            H3    L3
             \   /
              \ /  ← PIVOT POINT (buy here on volume)
               P
```

### Contraction Rules

- **T1 (first correction):** 8-35% depth for S&P 500 large-caps (up to 50% for small-caps)
- **T2:** Must be at least 25% tighter than T1 (ratio <= 0.75)
- **T3:** Must be at least 25% tighter than T2 (if present)
- **T4:** Extremely tight, often < 5% (rare, very bullish)
- **Minimum:** 2 contractions required
- **Ideal:** 3-4 contractions with progressive tightening
- **Duration:** 15-325 trading days for the complete pattern

### Pivot Point

The **pivot** is the high of the last contraction. This is the buy point:

- Buy when price moves above the pivot on volume 1.5x+ above the 50-day average
- Place stop-loss 1-2% below the last contraction low
- Risk per trade should be 5-8% from entry to stop

### Volume Signature

Ideal volume behavior during a VCP:

1. **During corrections:** Volume should decrease (sellers exhausting)
2. **Near the pivot:** Volume should "dry up" (extremely low, calm before the storm)
3. **On breakout:** Volume should surge to 1.5-2x the 50-day average

**Dry-up ratio** = Average volume (last 10 bars near pivot) / 50-day average volume
- < 0.30: Exceptional (textbook)
- 0.30-0.50: Strong
- 0.50-0.70: Adequate
- \> 0.70: Weak (caution)

## Historical VCP Examples

### Classic 3-Contraction VCP
- T1: 20% pullback over 6 weeks
- T2: 12% pullback over 3 weeks (40% tighter)
- T3: 5% pullback over 2 weeks (58% tighter)
- Breakout on 2x volume → 50%+ advance

### Tight 2-Contraction VCP (Large-Cap)
- T1: 12% pullback over 4 weeks
- T2: 5% pullback over 2 weeks (58% tighter)
- Breakout on 1.8x volume → 25-30% advance

## Common Pitfalls

1. **Buying before the pivot:** Wait for the breakout, not the setup
2. **Ignoring volume:** A breakout without volume often fails
3. **Wide stops:** Keep stops tight (below last contraction low)
4. **Wrong stage:** VCPs only work in Stage 2; verify with Trend Template first
5. **Deep T1:** If T1 > 35% for large-caps, the pattern is less reliable
6. **Expanding contractions:** If T2 > T1, it's NOT a VCP

## Position Sizing by VCP Quality

| Rating | Position Size | Risk Budget |
|--------|---------------|-------------|
| Textbook (90+) | 1.5-2x normal | Full |
| Strong (80-89) | 1x normal | Full |
| Good (70-79) | 0.75x normal | Standard |
| Developing (60-69) | Wait/Watch | Reduced |


---

## SKILL: vectorbt

- Fuente: `agiprolabs/claude-trading-skills` → `skills/vectorbt` (MIT)
- Cuándo usarla: High-performance vectorized backtesting with parameter optimization, portfolio simulation, and rich performance metrics
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/vectorbt/` (backtest_example.py, parameter_sweep.py)

# Vectorized Backtesting with vectorbt

## Overview

vectorbt is a Python library for **vectorized backtesting** — running strategy simulations using NumPy/pandas array operations instead of bar-by-bar loops. This makes it 100–1000x faster than event-driven frameworks (backtrader, zipline), enabling parameter optimization across thousands of combinations in seconds.

**Key strengths:**
- Blazing speed via NumPy vectorization
- Built-in parameter grid search and optimization
- 50+ built-in performance metrics (Sharpe, Sortino, Calmar, max drawdown, profit factor)
- Rich plotting (equity curves, drawdowns, trade markers, heatmaps)
- Native pandas integration — your data stays in DataFrames throughout

## Installation

```bash
uv pip install vectorbt pandas numpy
```

vectorbt pulls in pandas, NumPy, and Plotly automatically. For technical indicators, also install pandas-ta:

```bash
uv pip install vectorbt pandas-ta
```

## Core Concepts

### 1. Signals — Boolean Entry/Exit Arrays

Strategies in vectorbt are expressed as boolean pandas Series (or arrays) indicating where to enter and exit positions:

```python
import vectorbt as vbt
import pandas as pd

# Entry: buy when fast EMA crosses above slow EMA
entries = fast_ema > slow_ema
# Exit: sell when fast EMA crosses below slow EMA
exits = fast_ema < slow_ema
```

vectorbt resolves conflicting signals automatically (you can't enter while already in a position).

### 2. Portfolio — The Backtesting Engine

`vbt.Portfolio.from_signals()` is the primary backtesting function. It takes price data and entry/exit signals, simulates trades, and computes performance:

```python
pf = vbt.Portfolio.from_signals(
    close=close_prices,
    entries=entries,
    exits=exits,
    init_cash=10_000,
    fees=0.003,       # 0.3% per trade
    slippage=0.005,   # 0.5% slippage
    freq="1h",        # hourly data
)
```

### 3. Metrics — Built-in Performance Analysis

```python
# Full stats summary
print(pf.stats())

# Individual metrics
print(f"Total Return: {pf.total_return():.2%}")
print(f"Sharpe Ratio: {pf.sharpe_ratio():.3f}")
print(f"Max Drawdown: {pf.max_drawdown():.2%}")
print(f"Win Rate:     {pf.trades.win_rate():.2%}")
```

### 4. Parameter Optimization — Grid Search in Seconds

Pass arrays instead of scalars to test many parameter combos simultaneously:

```python
import numpy as np

fast_periods = np.arange(5, 25, 2)   # 10 values
slow_periods = np.arange(20, 60, 5)  # 8 values

fast_ma = vbt.MA.run(close, fast_periods, short_name="fast")
slow_ma = vbt.MA.run(close, slow_periods, short_name="slow")

# This creates 80 parameter combinations automatically
entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)
```

## Basic Workflow

### Step 1: Load OHLCV Data

```python
import pandas as pd

# From CSV
df = pd.read_csv("ohlcv.csv", parse_dates=["timestamp"], index_col="timestamp")
close = df["close"]

# From Yahoo Finance (traditional markets)
btc = vbt.YFData.download("BTC-USD", start="2023-01-01", end="2025-01-01")
close = btc.get("Close")
```

For Solana tokens, fetch data via the `birdeye-api` skill and load into a DataFrame.

### Step 2: Compute Indicators

```python
import pandas_ta as ta

# Using pandas-ta (see pandas-ta skill)
df.ta.ema(length=12, append=True)
df.ta.ema(length=26, append=True)
df.ta.rsi(length=14, append=True)
df.ta.bbands(length=20, std=2, append=True)

# Or using vectorbt built-ins
rsi = vbt.RSI.run(close, window=14)
bbands = vbt.BBANDS.run(close, window=20, alpha=2)
```

### Step 3: Generate Entry/Exit Signals

```python
# EMA crossover
entries = df["EMA_12"] > df["EMA_26"]
exits = df["EMA_12"] < df["EMA_26"]

# RSI mean reversion
entries = rsi.rsi_below(30)
exits = rsi.rsi_above(70)
```

### Step 4: Run Backtest

```python
pf = vbt.Portfolio.from_signals(
    close=close,
    entries=entries,
    exits=exits,
    init_cash=10_000,
    fees=0.003,
    slippage=0.005,
    size=0.95,               # use 95% of available cash
    size_type="percent",
    freq="1h",
)
```

### Step 5: Analyze Results

```python
# Summary statistics
print(pf.stats())

# Trade-level analysis
trades = pf.trades.records_readable
print(f"\nTrade count: {len(trades)}")
print(f"Avg holding period: {trades['Duration'].mean()}")

# Equity curve
pf.plot().show()

# Drawdown chart
pf.drawdowns.plot().show()
```

## Key Portfolio Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `close` | Price series (pd.Series or DataFrame) | `df["close"]` |
| `entries` | Boolean entry signals | `fast > slow` |
| `exits` | Boolean exit signals | `fast < slow` |
| `init_cash` | Starting capital | `10_000` |
| `fees` | Fee per trade (fraction) | `0.003` (0.3%) |
| `slippage` | Slippage per trade (fraction) | `0.005` (0.5%) |
| `size` | Position size | `0.95` |
| `size_type` | How to interpret size | `"percent"`, `"amount"`, `"value"` |
| `freq` | Data frequency | `"1h"`, `"4h"`, `"1d"` |
| `direction` | Trade direction | `"both"`, `"longonly"`, `"shortonly"` |
| `accumulate` | Allow adding to positions | `False` |
| `sl_stop` | Stop-loss level (fraction) | `0.05` (5%) |
| `tp_stop` | Take-profit level (fraction) | `0.10` (10%) |

## Performance Metrics

### Returns
- `total_return()` — cumulative return over the period
- `annualized_return()` — annualized compound return
- `daily_returns()` — Series of daily returns

### Risk
- `max_drawdown()` — maximum peak-to-trough decline
- `annualized_volatility()` — annualized standard deviation of returns
- `value_at_risk()` — VaR at specified confidence level

### Risk-Adjusted
- `sharpe_ratio()` — excess return per unit volatility
- `sortino_ratio()` — excess return per unit downside deviation
- `calmar_ratio()` — annualized return / max drawdown
- `omega_ratio()` — probability-weighted gain/loss ratio

### Trade Statistics
- `trades.win_rate()` — fraction of profitable trades
- `trades.profit_factor()` — gross profit / gross loss
- `trades.expectancy()` — average P&L per trade
- `trades.avg_winning_trade()` — mean profit on winners
- `trades.avg_losing_trade()` — mean loss on losers
- `trades.count()` — total number of completed trades

## Parameter Optimization

### Grid Search

```python
fast_windows = [5, 8, 12, 15, 20]
slow_windows = [20, 26, 30, 40, 50]

# Run all 25 combos at once
fast_ma = vbt.MA.run(close, fast_windows, short_name="fast")
slow_ma = vbt.MA.run(close, slow_windows, short_name="slow")

entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

pf = vbt.Portfolio.from_signals(close, entries, exits, fees=0.003)

# Find best params by Sharpe
sharpe = pf.sharpe_ratio()
best_idx = sharpe.idxmax()
print(f"Best params: {best_idx}, Sharpe: {sharpe[best_idx]:.3f}")
```

### Walk-Forward Validation

Always validate optimized parameters on out-of-sample data:

```python
# Split: 70% train, 30% test
split_idx = int(len(close) * 0.7)
train_close = close.iloc[:split_idx]
test_close = close.iloc[split_idx:]

# Optimize on training data
# ... (run grid search on train_close)

# Validate best params on test data
# ... (run single backtest on test_close with best params)
```

See `references/optimization_guide.md` for detailed walk-forward methodology and overfitting prevention.

## Crypto-Specific Considerations

### 24/7 Markets
Crypto markets never close. Use hourly or minute-based frequencies, not business-day frequencies:
```python
# Correct for crypto
pf = vbt.Portfolio.from_signals(close, entries, exits, freq="1h")

# Wrong — business days assume market closures
# pf = vbt.Portfolio.from_signals(close, entries, exits, freq="1B")
```

### Realistic Fees
DEX swaps on Solana typically cost 0.25–1% including AMM fees. CEX spot fees are 0.05–0.1%.
```python
# Solana DEX (conservative)
pf = vbt.Portfolio.from_signals(close, entries, exits, fees=0.005)

# CEX spot
pf = vbt.Portfolio.from_signals(close, entries, exits, fees=0.001)
```

### Slippage
Low-liquidity tokens can have 1–5% slippage. Always model this:
```python
# High-liquidity (SOL, ETH): 0.1–0.5%
pf = vbt.Portfolio.from_signals(close, entries, exits, slippage=0.003)

# Low-liquidity memecoins: 1–3%
pf = vbt.Portfolio.from_signals(close, entries, exits, slippage=0.02)
```

### Short History
Many tokens have less than 1 year of data. Be cautious about annualizing metrics from short samples.

## Common Strategy Patterns

### EMA Crossover
```python
fast = vbt.MA.run(close, 12, short_name="fast")
slow = vbt.MA.run(close, 26, short_name="slow")
entries = fast.ma_crossed_above(slow)
exits = fast.ma_crossed_below(slow)
```

### RSI Mean Reversion
```python
rsi = vbt.RSI.run(close, 14)
entries = rsi.rsi_crossed_below(30)
exits = rsi.rsi_crossed_above(70)
```

### Bollinger Band Breakout
```python
bb = vbt.BBANDS.run(close, window=20, alpha=2)
entries = close > bb.upper
exits = close < bb.lower
```

### Stop-Loss and Take-Profit
```python
pf = vbt.Portfolio.from_signals(
    close, entries, exits,
    sl_stop=0.05,    # 5% stop-loss
    tp_stop=0.10,    # 10% take-profit
)
```

## Related Skills

- **pandas-ta** — Technical indicator computation (feeds vectorbt signals)
- **birdeye-api** — Fetch Solana token OHLCV data for backtesting
- **trading-visualization** — Advanced chart generation for backtest results
- **portfolio-analytics** — Deeper portfolio-level risk/return analysis
- **position-sizing** — Optimal position sizing methodology
- **risk-management** — Portfolio-level risk guardrails
- **regime-detection** — Market regime awareness for adaptive strategies

## Files

### References
- `references/api_guide.md` — Complete vectorbt API reference for Portfolio, indicators, plotting, and data loading
- `references/optimization_guide.md` — Grid search, walk-forward validation, overfitting prevention, and optimization best practices

### Scripts
- `scripts/backtest_example.py` — Three-strategy backtest comparison using synthetic data (EMA crossover, RSI mean reversion, Bollinger breakout)
- `scripts/parameter_sweep.py` — EMA crossover parameter grid search with walk-forward validation

### Referencia: references/api_guide.md

# vectorbt API Guide

## Portfolio.from_signals()

The primary backtesting entry point. Takes price data and boolean entry/exit signals, simulates trades, returns a Portfolio object.

```python
pf = vbt.Portfolio.from_signals(
    close,              # pd.Series or DataFrame of close prices
    entries,            # boolean Series/DataFrame — True = enter long
    exits,              # boolean Series/DataFrame — True = exit long
    short_entries=None, # boolean — True = enter short
    short_exits=None,   # boolean — True = exit short
    init_cash=100.0,    # starting capital (float or array)
    fees=0.0,           # fee fraction per trade (0.001 = 0.1%)
    slippage=0.0,       # slippage fraction (0.005 = 0.5%)
    size=np.inf,        # position size (inf = use all available cash)
    size_type="amount", # "amount", "value", "percent"
    direction="longonly",  # "longonly", "shortonly", "both"
    accumulate=False,   # allow adding to existing position
    sl_stop=None,       # stop-loss fraction (0.05 = 5%)
    tp_stop=None,       # take-profit fraction (0.10 = 10%)
    freq=None,          # data frequency ("1h", "1d", etc.)
    upon_opposite_entry="reversereduce",  # action on conflicting signals
)
```

### Size Type Options
| Value | Meaning | Example |
|-------|---------|---------|
| `"amount"` | Number of units (shares/tokens) | `size=100` → buy 100 tokens |
| `"value"` | Dollar/SOL value | `size=1000` → buy $1000 worth |
| `"percent"` | Fraction of available cash | `size=0.95` → use 95% of cash |

### Direction Options
| Value | Meaning |
|-------|---------|
| `"longonly"` | Only long positions (default) |
| `"shortonly"` | Only short positions |
| `"both"` | Allow both long and short |

## Portfolio.from_orders()

For complex order logic beyond simple signals:

```python
pf = vbt.Portfolio.from_orders(
    close=close,
    size=order_sizes,       # Series of order sizes (+buy, -sell)
    size_type="amount",
    init_cash=10_000,
    fees=0.003,
    freq="1h",
)
```

Use `from_orders()` when you need variable position sizes, partial exits, or order-level logic that signals can't express.

## Portfolio Object — Key Methods

### Summary Statistics
```python
pf.stats()                    # Full stats dictionary
pf.stats(agg_func=None)      # Stats for each column (multi-param)
```

### Return Metrics
```python
pf.total_return()             # Cumulative return (float)
pf.annualized_return()        # CAGR
pf.returns()                  # pd.Series of period returns
pf.cumulative_returns()       # pd.Series of cumulative returns
pf.daily_returns()            # Daily return series
```

### Risk Metrics
```python
pf.max_drawdown()             # Maximum peak-to-trough decline
pf.max_drawdown_duration()    # Longest drawdown in time
pf.annualized_volatility()    # Annualized std dev of returns
pf.value_at_risk()            # Value at Risk
pf.conditional_value_at_risk()  # CVaR / Expected Shortfall
```

### Risk-Adjusted Metrics
```python
pf.sharpe_ratio()             # Sharpe ratio (default rf=0)
pf.sortino_ratio()            # Sortino ratio
pf.calmar_ratio()             # Calmar ratio
pf.omega_ratio()              # Omega ratio
pf.information_ratio()        # Information ratio (vs benchmark)
```

### Trade Analysis
```python
pf.trades.count()             # Number of completed trades
pf.trades.win_rate()          # Fraction of winners
pf.trades.profit_factor()     # Gross profit / gross loss
pf.trades.expectancy()        # Average P&L per trade
pf.trades.avg_winning_trade() # Mean winner P&L
pf.trades.avg_losing_trade()  # Mean loser P&L
pf.trades.records_readable    # DataFrame of all trades
```

### Portfolio Value
```python
pf.value()                    # Portfolio value over time
pf.cash()                     # Cash balance over time
pf.asset_value()              # Asset value over time
```

## Plotting

```python
# Equity curve
pf.plot().show()

# Drawdowns
pf.drawdowns.plot().show()

# Trade markers on price chart
pf.trades.plot().show()

# Cumulative returns
pf.cumulative_returns().vbt.plot().show()
```

### Heatmaps for Parameter Sweeps
```python
# 2D heatmap of metric across parameter grid
sharpe = pf.sharpe_ratio()
sharpe_2d = sharpe.unstack()  # reshape to 2D
sharpe_2d.vbt.heatmap(
    x_level="fast_window",
    y_level="slow_window",
    title="Sharpe Ratio by EMA Parameters"
).show()
```

## Built-in Indicators

### Moving Average — vbt.MA
```python
ma = vbt.MA.run(close, window=[10, 20, 50], short_name="ma")
ma.ma                          # MA values (multi-column if array window)
ma.ma_above(close)             # Boolean: MA > close
ma.ma_below(close)             # Boolean: MA < close
ma.ma_crossed_above(close)     # Boolean: MA crossed above close
ma.ma_crossed_below(close)     # Boolean: MA crossed below close
```

### RSI — vbt.RSI
```python
rsi = vbt.RSI.run(close, window=14)
rsi.rsi                        # RSI values
rsi.rsi_above(70)              # Boolean: RSI > 70
rsi.rsi_below(30)              # Boolean: RSI < 30
rsi.rsi_crossed_above(70)      # Boolean: RSI crossed above 70
rsi.rsi_crossed_below(30)      # Boolean: RSI crossed below 30
```

### Bollinger Bands — vbt.BBANDS
```python
bb = vbt.BBANDS.run(close, window=20, alpha=2)
bb.upper                       # Upper band
bb.middle                      # Middle band (SMA)
bb.lower                       # Lower band
bb.bandwidth                   # Band width
bb.percent_b                   # %B indicator
```

### ATR — vbt.ATR
```python
atr = vbt.ATR.run(high, low, close, window=14)
atr.atr                        # ATR values
```

## Parameter Arrays and Grid Search

When you pass an array for an indicator parameter, vectorbt computes all values simultaneously and returns a multi-column DataFrame:

```python
# Single window → single-column output
ma_20 = vbt.MA.run(close, window=20)

# Array of windows → multi-column output
ma_multi = vbt.MA.run(close, window=[10, 20, 50])
# Result has columns: (10,), (20,), (50,)
```

For 2D grid search, use two indicators with different parameters:

```python
fast_ma = vbt.MA.run(close, [5, 10, 15], short_name="fast")
slow_ma = vbt.MA.run(close, [20, 30, 40], short_name="slow")

# Broadcasting creates 3x3=9 combinations
entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)
# entries/exits have MultiIndex columns: (fast, slow) pairs
```

## Data Loading

### Yahoo Finance (Traditional Assets)
```python
data = vbt.YFData.download(
    "BTC-USD",
    start="2023-01-01",
    end="2025-01-01",
    interval="1d",
)
close = data.get("Close")
```

### Custom Data (Crypto / Solana)
```python
import pandas as pd

# Load from CSV or API response
df = pd.DataFrame({
    "timestamp": timestamps,
    "open": opens,
    "high": highs,
    "low": lows,
    "close": closes,
    "volume": volumes,
})
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.set_index("timestamp").sort_index()

# Use close prices for backtesting
close = df["close"]
```

For Solana token data, see the `birdeye-api` skill for fetching OHLCV data via the Birdeye API.

## Tips

- **Multi-column operations**: When entries/exits have multiple columns (from parameter arrays), `Portfolio.from_signals()` automatically runs all combinations.
- **Memory**: Large parameter sweeps with long time series can use significant RAM. Start with coarse grids and narrow down.
- **Frequency**: Always set `freq` correctly — it affects annualization of Sharpe, volatility, and other time-scaled metrics.
- **NaN handling**: vectorbt treats NaN signals as "no action". Indicator warm-up periods produce NaN automatically.

### Referencia: references/optimization_guide.md

# vectorbt Optimization Guide

## Grid Search Methodology

Grid search tests every combination of parameter values. vectorbt makes this fast by vectorizing all combinations in a single pass.

### Step-by-Step Grid Search

```python
import numpy as np
import vectorbt as vbt

# 1. Define parameter ranges
fast_windows = np.arange(5, 25, 2)    # [5, 7, 9, ..., 23] → 10 values
slow_windows = np.arange(20, 60, 5)   # [20, 25, 30, ..., 55] → 8 values
# Total combinations: 10 × 8 = 80

# 2. Run indicators with array parameters
fast_ma = vbt.MA.run(close, fast_windows, short_name="fast")
slow_ma = vbt.MA.run(close, slow_windows, short_name="slow")

# 3. Generate signals (broadcasted across all combos)
entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

# 4. Run portfolio for all combos simultaneously
pf = vbt.Portfolio.from_signals(
    close, entries, exits,
    init_cash=10_000,
    fees=0.003,
    slippage=0.005,
    freq="1h",
)

# 5. Extract metrics
sharpe = pf.sharpe_ratio()
total_return = pf.total_return()
max_dd = pf.max_drawdown()
trade_count = pf.trades.count()

# 6. Find best parameters
best_sharpe_idx = sharpe.idxmax()
print(f"Best Sharpe: {sharpe[best_sharpe_idx]:.3f} at {best_sharpe_idx}")
```

### Filtering Results

```python
# Only consider combos with enough trades
valid = trade_count >= 20
filtered_sharpe = sharpe[valid]
best = filtered_sharpe.idxmax()

# Only consider combos where fast < slow (sensible constraint)
# This is handled automatically if your parameter ranges don't overlap
```

### Heatmap Visualization

```python
# Reshape to 2D for heatmap
sharpe_2d = sharpe.unstack(level="slow_window")
sharpe_2d.vbt.heatmap(
    title="Sharpe Ratio: Fast vs Slow EMA",
).show()
```

## Walk-Forward Optimization

In-sample optimization always overfits. Walk-forward validation is the minimum standard for credible results.

### Concept

1. Split data into sequential windows
2. Optimize parameters on each training window
3. Test optimized parameters on the next (unseen) window
4. Aggregate out-of-sample results

### Implementation

```python
import pandas as pd
import numpy as np
import vectorbt as vbt

def walk_forward_backtest(
    close: pd.Series,
    fast_windows: list[int],
    slow_windows: list[int],
    train_frac: float = 0.7,
    n_splits: int = 3,
    fees: float = 0.003,
    slippage: float = 0.005,
) -> dict:
    """Run walk-forward optimization on EMA crossover strategy.

    Args:
        close: Price series.
        fast_windows: Fast EMA periods to test.
        slow_windows: Slow EMA periods to test.
        train_frac: Fraction of each window used for training.
        n_splits: Number of walk-forward windows.
        fees: Trading fee fraction.
        slippage: Slippage fraction.

    Returns:
        Dictionary with in-sample and out-of-sample results.
    """
    total_len = len(close)
    window_size = total_len // n_splits
    results = []

    for i in range(n_splits):
        start = i * window_size
        end = min(start + window_size, total_len)
        window = close.iloc[start:end]

        split = int(len(window) * train_frac)
        train = window.iloc[:split]
        test = window.iloc[split:]

        # Optimize on training data
        fast_ma = vbt.MA.run(train, fast_windows, short_name="fast")
        slow_ma = vbt.MA.run(train, slow_windows, short_name="slow")
        entries = fast_ma.ma_crossed_above(slow_ma)
        exits = fast_ma.ma_crossed_below(slow_ma)

        pf_train = vbt.Portfolio.from_signals(
            train, entries, exits,
            fees=fees, slippage=slippage, freq="1h",
        )
        best_params = pf_train.sharpe_ratio().idxmax()

        # Validate on test data with best params
        best_fast, best_slow = best_params
        fast_test = vbt.MA.run(test, best_fast, short_name="fast")
        slow_test = vbt.MA.run(test, best_slow, short_name="slow")
        ent_test = fast_test.ma_crossed_above(slow_test)
        ext_test = fast_test.ma_crossed_below(slow_test)

        pf_test = vbt.Portfolio.from_signals(
            test, ent_test, ext_test,
            fees=fees, slippage=slippage, freq="1h",
        )

        results.append({
            "window": i,
            "best_fast": best_fast,
            "best_slow": best_slow,
            "is_sharpe": pf_train.sharpe_ratio()[best_params],
            "oos_sharpe": pf_test.sharpe_ratio(),
            "is_return": pf_train.total_return()[best_params],
            "oos_return": pf_test.total_return(),
        })

    return results
```

### Interpreting Walk-Forward Results

| Metric | Good Sign | Warning Sign |
|--------|-----------|--------------|
| OOS Sharpe / IS Sharpe | > 0.5 | < 0.3 |
| OOS returns | Positive across most windows | Negative in most windows |
| Parameter stability | Same params chosen repeatedly | Different params every window |
| OOS drawdown | Smaller than IS drawdown | Much larger than IS |

## Overfitting Prevention

### 1. Minimum Trade Count
Never trust results with fewer than 30 trades per parameter combination. Ideally 100+.

```python
# Filter out low-trade-count results
valid_mask = pf.trades.count() >= 30
sharpe_filtered = pf.sharpe_ratio()[valid_mask]
```

### 2. Parameter Stability
If optimal parameters change dramatically across walk-forward windows, the strategy is likely overfit.

```python
# Check if best params are consistent
for r in wf_results:
    print(f"Window {r['window']}: fast={r['best_fast']}, slow={r['best_slow']}")
# Consistent: fast=12 in all windows
# Overfit: fast=5, 21, 9, 17 across windows
```

### 3. Simplicity Preference
Fewer parameters = less overfitting. Prefer 2-parameter strategies over 5-parameter ones.

| Parameters | Risk Level | Minimum Data |
|------------|------------|--------------|
| 1-2 | Low | 6 months hourly |
| 3-4 | Medium | 1+ year hourly |
| 5+ | High | 2+ years hourly |

### 4. Out-of-Sample Decay Budget
Expect 30–60% Sharpe decay from in-sample to out-of-sample. If your IS Sharpe is 1.5, expect OOS Sharpe of 0.6–1.0.

### 5. Deflated Sharpe Ratio
When testing many parameter combos, the best Sharpe is inflated by multiple testing. Apply a haircut:

```python
import numpy as np

def deflated_sharpe(sharpe_best: float, n_trials: int, n_obs: int) -> float:
    """Estimate probability that best Sharpe is genuine.

    Args:
        sharpe_best: Best observed Sharpe ratio.
        n_trials: Number of parameter combinations tested.
        n_obs: Number of return observations.

    Returns:
        Approximate deflated Sharpe (lower is more skeptical).
    """
    expected_max = np.sqrt(2 * np.log(n_trials))
    return sharpe_best - expected_max / np.sqrt(n_obs)
```

## Common Optimization Mistakes

### 1. Optimizing on Full Dataset
Using the entire dataset for optimization means there's no unseen data to validate on. Always hold out at least 30% for testing.

### 2. Cherry-Picking Time Periods
Testing only on bull markets (or bear markets) gives misleading results. Use the full available history.

### 3. Ignoring Transaction Costs
Strategies that look great with zero fees often break even or lose money with realistic fees. Always include fees and slippage.

### 4. Annualizing Short Samples
A 50% return over 2 weeks annualizes to ~130,000%. This is meaningless. Require at least 6 months of data before annualizing.

### 5. Ignoring Drawdown
A strategy with 200% return and 80% max drawdown is not tradeable. Always check max drawdown alongside returns.

### 6. Data Snooping
If you tried 50 strategy ideas before finding one that works, you've effectively run 50 optimizations. Apply the deflated Sharpe correction.

## Combinatorial Purged Cross-Validation (CPCV)

For advanced users, CPCV provides more robust validation than simple walk-forward:

1. Divide data into N groups
2. Select all combinations of N-k groups for training, k groups for testing
3. Purge overlapping data between train and test (remove a buffer)
4. Run optimization on each training set, validate on each test set
5. Aggregate all out-of-sample results

This produces more test paths and is harder to overfit than single walk-forward splits. Implementation requires significant code — see the `regime-detection` skill for related statistical validation techniques.

## Recommended Workflow

1. **Explore**: Run a coarse grid search (5-10 values per parameter) on 80% of data
2. **Narrow**: Identify the promising region, run a fine grid search
3. **Validate**: Walk-forward test with 3-5 splits
4. **Stress test**: Check OOS Sharpe decay, parameter stability, trade count
5. **Deploy cautiously**: Start with small size, monitor live performance vs backtest
6. **Re-optimize**: Re-run optimization monthly or quarterly with new data
