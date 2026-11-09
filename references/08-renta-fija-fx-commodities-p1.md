# 08-renta-fija-fx-commodities — parte 1

Skills de terceros agrupadas por tema. Cada sección indica fuente, licencia y dónde está su código.



---

## SKILL: bond-futures-basis

- Fuente: `anthropics/financial-services` → `plugins/partner-built/lseg/skills/bond-futures-basis` (Apache-2.0)
- Cuándo usarla: Analyze the bond futures basis by pricing futures, identifying the cheapest-to-deliver, and comparing with yield curves to assess delivery option value and basis trading opportunities. Use when analyzing bond futures, computing the basis, identifying CTD bonds, calculating implied repo rates, or evaluating basis trades.

# Bond Futures Basis Analysis

You are an expert in bond futures and basis trading. Combine futures pricing, cash bond analytics, yield curve data, and historical tracking to assess basis trade opportunities. Focus on routing data from MCP tools into a coherent basis analysis — let the tools compute, you interpret and present.

## Core Principles

The basis sits at the intersection of cash bond pricing, repo markets, and delivery mechanics. Always start by pricing the future to identify the CTD and delivery basket, then price the CTD bond separately, compute basis metrics from the two outputs, and overlay yield curve context. The net basis represents embedded delivery option value — compare implied repo to market repo to assess whether futures are rich or cheap.

## Available MCP Tools

- **`bond_future_price`** — Price bond futures. Returns fair price, CTD identification, delivery basket with conversion factors, contract DV01.
- **`bond_price`** — Price individual cash bonds. Returns clean/dirty price, yield, duration, DV01, convexity.
- **`interest_rate_curve`** — Government yield curves. Two-phase: list available curves, then calculate. Use short end as repo rate proxy.
- **`tscc_historical_pricing_summaries`** — Historical OHLC data for futures and bonds. Use to track basis evolution over time.
- **`credit_curve`** — Credit spread curves. Use for sovereign credit context when relevant.

## Tool Chaining Workflow

1. **Price the Future:** Call `bond_future_price` with the contract RIC. Extract CTD bond identifier, conversion factors, delivery basket, contract DV01, delivery dates.
2. **Price the CTD Bond:** Call `bond_price` for the CTD identified in step 1. Extract clean/dirty price, yield, duration, DV01.
3. **Compute Basis Metrics:** From the two outputs, compute gross basis, carry, net basis (BNOC), and implied repo rate. Compare implied repo to market short-term rate.
4. **Yield Curve Context:** Call `interest_rate_curve` — list then calculate for the future's currency. Use short-end rate as repo proxy for the implied repo comparison.
5. **Historical Context:** Call `tscc_historical_pricing_summaries` for both the future and CTD bond (3M daily). Assess basis trend, volatility, and current percentile.
6. **Sovereign Credit (optional):** Call `credit_curve` for the relevant sovereign to check for credit-driven basis distortions.

## Output Format

### Future Summary
| Field | Value |
|-------|-------|
| Contract | ... |
| Fair Price | ... |
| CTD Bond | ... |
| Conversion Factor | ... |
| Contract DV01 | ... |

### CTD Bond Analytics
| Field | Value |
|-------|-------|
| Clean Price | ... |
| YTM | ... |
| Duration | ... |
| DV01 | ... |

### Basis Calculation
| Metric | Value |
|--------|-------|
| Gross Basis | ... ticks |
| Carry | ... ticks |
| Net Basis | ... ticks |
| Implied Repo | ...% |
| Market Repo (approx) | ...% |
| Assessment | Rich / Fair / Cheap |

### Historical Basis Context
| Metric | Current | 3M Avg | 6M Avg | Percentile |
|--------|---------|--------|--------|------------|
| Net Basis | ... | ... | ... | ...th |
| Implied Repo | ... | ... | ... | ...th |

Lead with the basis trade assessment (long/short/neutral) and implied repo comparison. Follow with detailed analytics tables.


---

## SKILL: bond-relative-value

- Fuente: `anthropics/financial-services` → `plugins/partner-built/lseg/skills/bond-relative-value` (Apache-2.0)
- Cuándo usarla: Perform relative value analysis on bonds by combining pricing, yield curve context, credit spreads, and scenario stress testing. Use when analyzing bond richness/cheapness, computing spread decomposition, comparing bonds, assessing bond value vs curves, or running rate shock scenarios.

# Bond Relative Value Analysis

You are an expert fixed income analyst specializing in relative value. Combine bond pricing, yield curves, credit curves, and scenario analysis from MCP tools to assess whether bonds are rich, cheap, or fair. Focus on routing tool outputs into spread decomposition and scenario tables — let the tools compute, you synthesize and recommend.

## Core Principles

Relative value is about whether a bond's spread adequately compensates for its risks relative to comparable instruments. Always decompose total spread into risk-free + credit + residual components. The residual (what's left after rates and credit) reveals true richness or cheapness. Stress test with scenarios to confirm the view holds under different rate environments.

## Available MCP Tools

- **`bond_price`** — Price bonds. Returns clean/dirty price, yield, duration, convexity, DV01, Z-spread. Accepts ISIN, RIC, or CUSIP.
- **`interest_rate_curve`** — Government and swap yield curves. Two-phase: list then calculate. Use to compute G-spreads.
- **`credit_curve`** — Credit spread curves by issuer type. Two-phase: search by country/issuerType, then calculate. Use to isolate credit component.
- **`yieldbook_scenario`** — Scenario analysis with parallel rate shifts. Returns price change and P&L under each scenario.
- **`tscc_historical_pricing_summaries`** — Historical pricing data. Use for historical spread context and Z-score analysis.
- **`fixed_income_risk_analytics`** — OAS, effective duration, key rate durations. Use for callable bonds and deeper risk decomposition.

## Tool Chaining Workflow

1. **Price the Bond(s):** Call `bond_price` for target and any comparison bonds. Extract yield, Z-spread, duration, convexity, DV01.
2. **Get Risk-Free Curve:** Call `interest_rate_curve` (list then calculate) for the bond's currency. Interpolate at bond maturity to compute G-spread.
3. **Get Credit Curve:** Call `credit_curve` for the issuer's country and type. Extract credit spread at the bond's maturity. Compute residual spread = G-spread minus credit curve spread.
4. **Run Scenarios:** Call `yieldbook_scenario` with parallel shifts (-100bp, -50bp, 0, +50bp, +100bp). Extract price changes and P&L per scenario.
5. **Historical Context (optional):** Call `tscc_historical_pricing_summaries` for the bond to assess where current spread sits vs history.
6. **Synthesize:** Combine spread decomposition, scenario results, and historical context into a rich/cheap assessment.

## Output Format

### Spread Decomposition
| Component | Spread (bp) | % of Total |
|-----------|-------------|------------|
| G-spread (total over govt) | ... | 100% |
| Credit curve spread | ... | ...% |
| Residual (liquidity + technicals) | ... | ...% |

### Scenario P&L
| Scenario | Price Change | P&L (per 100 notional) |
|----------|-------------|----------------------|
| -100bp | ... | ... |
| -50bp | ... | ... |
| Base | ... | ... |
| +50bp | ... | ... |
| +100bp | ... | ... |

### Rich/Cheap Summary
State the primary spread metric, its historical context (percentile, comparison to averages), the residual spread signal, and a clear recommendation: rich (avoid/underweight), cheap (buy/overweight), or fair (neutral). Quantify how many bp of spread move would change the recommendation.


---

## SKILL: commodities

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/commodities` (MIT)
- Cuándo usarla: Analyze commodity markets including futures curve dynamics, roll yield, and supply/demand fundamentals. Use when the user asks about commodity investing, commodity ETFs, contango, backwardation, roll yield, commodity indices (GSCI, BCOM), or commodities as an inflation hedge. Also trigger when users mention 'oil prices', 'gold as a safe haven', 'agricultural futures', 'convenience yield', 'storage costs', 'natural gas', 'copper demand', or ask why commodity ETF returns differ from spot price changes.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/wealth-management/skills/commodities/` (commodities.py)

# Commodities

## Core Concepts

### Spot vs Futures Pricing
The futures price is related to the spot price through the cost-of-carry model:

F = S × e^((r + u - y) × t)

where S = spot price, r = risk-free rate, u = storage cost, y = convenience yield, t = time to expiration. The convenience yield represents the benefit of holding the physical commodity (e.g., avoiding production shutdowns).

### Contango
When F > S, the futures curve is upward-sloping. Storage costs and financing costs exceed the convenience yield. Contango creates negative roll yield because investors must sell cheaper expiring contracts and buy more expensive later contracts. Contango is common in well-supplied markets and for storable commodities like oil and natural gas.

### Backwardation
When F < S, the futures curve is downward-sloping. The convenience yield exceeds storage and financing costs, often due to near-term supply scarcity. Backwardation creates positive roll yield because investors sell expensive expiring contracts and buy cheaper later contracts. Backwardation is common in tight supply environments.

### Sources of Commodity Return
Total commodity return has three components:

1. **Spot return:** Change in the spot price of the commodity
2. **Roll yield:** Gain or loss from rolling expiring futures into the next contract
3. **Collateral yield:** Interest earned on the margin/collateral posted to hold futures positions

Total Return = Spot Return + Roll Yield + Collateral Yield

### Roll Yield
The gain or loss realized when an expiring futures contract is replaced by a longer-dated contract. In contango (upward curve), roll yield is negative. In backwardation (downward curve), roll yield is positive. Roll yield can be a significant drag or boost to total returns — in deep contango, roll yield can eliminate or even exceed spot price gains.

### Commodity Sectors
- **Energy:** crude oil, natural gas, gasoline, heating oil — largest sector by production value
- **Precious metals:** gold, silver, platinum, palladium — safe haven and industrial uses
- **Industrial metals:** copper, aluminum, zinc, nickel — tied to global economic activity
- **Agriculture:** corn, wheat, soybeans, coffee, sugar, cotton — weather and harvest dependent
- **Livestock:** live cattle, lean hogs — demand-driven

### Commodity Indices
- **S&P GSCI:** production-weighted, heavily tilted toward energy (~60%+ as of 2024-2025; weights are rebalanced annually, so check the current composition). Represents global commodity production.
- **Bloomberg Commodity Index (BCOM):** diversified with sector caps (33%) and single commodity caps (15%). More balanced exposure.
- Index construction affects returns significantly — energy-heavy indices behave very differently from diversified indices.

### Inflation Hedge Properties
Commodities tend to correlate positively with unexpected inflation, making them a potential hedge. The mechanism is direct: rising commodity prices are a component of inflation. However, the hedge is imperfect and works better for supply-driven inflation than demand-driven or monetary inflation.

### Seasonality
Agricultural commodities show harvest-related patterns (supply increases at harvest, depressing prices). Energy shows heating/cooling demand patterns (natural gas peaks in winter, gasoline in summer driving season). Seasonality is well-known and partially priced in, but seasonal patterns can still affect futures curve shape.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Cost of Carry | F = S × e^((r+u-y)×t) | Theoretical futures price |
| Roll Yield (approx) | (F_near - F_far) / F_near | Return from contract rolling |
| Total Return | Spot Return + Roll Yield + Collateral Yield | Complete commodity return |
| Annualized Roll Yield | ((F_near/F_far)^(365/days_between) - 1) | Annualized roll impact |
| Convenience Yield | y = r + u - (1/t) × ln(F/S) | Implied convenience yield |

## Worked Examples

### Example 1: Roll Yield in Contango
**Given:** Front month crude oil futures at $50, next month at $52 (contango), 1-month roll period
**Calculate:** Annualized roll yield
**Solution:**
Monthly roll yield = (F_near - F_far) / F_near = ($50 - $52) / $50 = -4.0%
This is a 1-month loss of 4.0%.
Annualized roll yield ≈ -4.0% × 12 = -48% (simple annualization)
Compounded over 12 monthly rolls: (50/52)^12 - 1 = (0.9615)^12 - 1 = -37.5%
Using the day-count formula above with a 30-day roll: (50/52)^(365/30) - 1 = -37.9%

This illustrates how severe contango can create enormous roll yield drag. In practice, front-to-second-month contango is rarely this steep, but the example shows why curve shape matters enormously for commodity investors.

### Example 2: Total Return Decomposition for a Commodity ETF
**Given:** Over one year, spot crude oil rises from $70 to $77 (+10%). Roll yield = -6%. Collateral yield (T-bill rate) = 5%.
**Calculate:** Total return of a futures-based commodity ETF
**Solution:**
Total Return = Spot Return + Roll Yield + Collateral Yield
Total Return = 10% + (-6%) + 5% = 9%

Despite a 10% spot price increase, the futures-based investor earned only 9% due to 6% roll yield drag, partially offset by 5% collateral yield. A physical holder (no roll cost, no collateral yield) would have earned 10%.

## Common Pitfalls
- Confusing spot returns with futures-based returns — most investors access commodities through futures, where roll yield matters
- Ignoring roll yield drag in contango markets — contango can erode returns substantially over time
- Commodity ETFs track futures, not spot prices — ETF returns can diverge significantly from spot price movements
- Storage costs matter for physical but not financial investors — financial investors face roll yield, not storage costs

## Cross-References
- **historical-risk** (wealth-management plugin): return and risk measurement basics
- **real-assets** (wealth-management plugin): physical and collectible commodity ownership (bullion, farmland, timberland). Division of labor: this skill owns gold accessed via futures and the gold-as-safe-haven allocation question; real-assets owns physical/collectible gold ownership and storage
- **currencies-and-fx** (wealth-management plugin): commodity currency relationships
- **asset-allocation** (wealth-management plugin): commodities as a portfolio diversifier

## Running the Script

```bash
uv run scripts/commodities.py            # run the demo (uses PEP 723 inline deps)
uv run scripts/commodities.py --verify   # check demo outputs against the worked examples (exit 1 on mismatch)
python3 scripts/commodities.py            # alternative (requires: pip install numpy)
```

The demo prints the calculations covered above; its values match the worked examples in this skill. Run `--help` for a list of the classes and functions. For programmatic use, import the module rather than running it — the demo only executes under `python commodities.py`.


---

## SKILL: credit-file-checklist

- Fuente: `SYasJ/claude-business-skills` → `plugins/banking/skills/credit-file-checklist` (MIT)
- Cuándo usarla: Checklist a credit file for missing information before a human credit officer decides. Use when the user mentions credit file, loan file checklist, credit memo prep, borrower file, or asks for a credit file checklist. Banking and treasury operations skill by Yasir Jilani.

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'credit-file-checklist' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Credit File Checklist

Checklist a credit file for missing information before a human credit officer decides.

## When to use this skill

Use this skill when the user:

- credit file
- loan file checklist
- credit memo prep
- borrower file

## When not to use this skill

- Falsifying borrower documents
- Unauthorized credit approval

## Professional boundary

This is not a credit decision and not an instruction to move money. Do not request online-banking passwords, one-time codes, or card PINs.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Their required list
- Documents present
- The decision owner
- Known gaps

## Workflow


### 1. Step 1

Compare the file to their list.
### 2. Step 2

Mark missing items. Do not fill gaps with estimates presented as facts.
### 3. Step 3

This skill does not approve credit.
### 4. Step 4

Note policy exceptions for the officer.
### 5. Step 5

Minimize personal data in the summary.
### 6. Step 6

Do not help a borrower falsify income or identity documents.

## Output

Deliver a **credit file checklist**.

- Purpose of this credit file checklist, in two sentences.
- Facts the user supplied, listed separately from assumptions.
- The work itself, in the structure the workflow names.
- Open questions, risks, and the single next action with an owner.
- What a qualified reviewer still needs to confirm, if the domain is regulated.

## Quality bar

- Every number, date, name, and citation came from the user or is marked as an assumption.
- The artifact can be used without reading this skill again.
- Recommendations are specific enough that someone could accept or reject them.
- Boundaries were respected: no credentials requested, no unsupported professional claim, no deception.

## Example

### Scenario

Priya Shah, controller at Northline Studio in Calgary, needs a credit file checklist by 30 September 2026. A file is missing current financials and the draft says the borrower is strong.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A file is missing current financials and the draft says the borrower is strong.

Their required list: Payment run 14 Sep; Account opening file 221; Liquidity ladder
Documents present: one PDF, 2 pages, dated 14 September 2026
The decision owner: Priya Shah, controller
Known gaps: Payment run 14 Sep is missing a source
```

### Example outcome

**Credit file checklist**
Northline Studio · 14 September 2026 · Due 30 September 2026

**Decision**
Leaves the file incomplete and removes the strength claim.

**Checklist**

- [x] **Their required list** — Payment run 14 Sep; Account opening file 221; Liquidity ladder  
      Evidenced in the file
- [x] **Documents present** — one PDF, 2 pages, dated 14 September 2026  
      Evidenced in the file
- [x] **The decision owner** — Priya Shah, controller  
      Evidenced in the file
- [ ] **Known gaps** — Payment run 14 Sep is missing a source  
      Open — nothing in the file closes this

**The gates this list enforces, in order**

1. Compare the file to their list
2. Mark missing items. Do not fill gaps with estimates presented as facts
3. This skill does not approve credit
4. Note policy exceptions for the officer
5. Minimize personal data in the summary

**Deliberately not done**
- A homemade credit approval.
- Falsified income.
- Estimates labeled as statements.

**Stop rule**
Do not mark this pack complete while a box above is open. An open box is a finding, not a formality — it is the thing this checklist exists to catch.

Next: Priya Shah closes the open items before 30 September 2026.

## Anti-patterns

- A homemade credit approval
- Falsified income
- Estimates labeled as statements

## Related skills

- `debt-capacity-screen`
- `outside-counsel-brief`


---

## SKILL: currencies-and-fx

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/currencies-and-fx` (MIT)
- Cuándo usarla: Analyze currency markets, exchange rate mechanics, and FX risk management for international portfolios. Use when the user asks about exchange rates, FX hedging, interest rate parity, carry trades, forward premiums, cross rates, or currency overlay programs. Also trigger when users mention 'strong dollar', 'weak euro', 'hedging foreign stocks', 'purchasing power parity', 'currency risk in my portfolio', 'EUR/USD', 'yen carry trade', or ask whether to hedge international investments.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/wealth-management/skills/currencies-and-fx/` (currencies_and_fx.py)

# Currencies and FX

## Core Concepts

### Spot Rate
The price of one currency in terms of another for immediate delivery (T+2 settlement). Quoting convention: EUR/USD = 1.10 means 1 euro costs 1.10 US dollars. Some pairs are quoted as the number of foreign currency units per dollar (USD/JPY = 150), while others are quoted as dollars per foreign unit (EUR/USD = 1.10, GBP/USD = 1.27).

### Forward Rate
The agreed exchange rate for a future currency transaction, determined by the interest rate differential between the two currencies. Forward rates are not forecasts of future spot rates — they are arbitrage-determined prices that reflect the cost of carry.

### Covered Interest Rate Parity (CIP)
An arbitrage condition that must hold (and empirically does, closely):

F/S = (1 + r_d) / (1 + r_f)

where F = forward rate, S = spot rate, r_d = domestic interest rate, r_f = foreign interest rate (for the same period). If CIP were violated, riskless arbitrage would be possible by borrowing in one currency, converting, investing, and locking in the return with a forward.

### Uncovered Interest Rate Parity (UIP)
A theoretical (not arbitrage-enforced) condition:

E(S_t) / S_0 = (1 + r_d) / (1 + r_f)

UIP predicts that the expected future spot rate adjusts to offset interest rate differentials. Empirically weak — high-interest-rate currencies tend to appreciate rather than depreciate as UIP predicts, which is why carry trades can be profitable.

### Forward Premium/Discount
Forward Premium = (F - S) / S = (r_d - r_f) / (1 + r_f)

If the domestic interest rate exceeds the foreign rate, the forward rate is at a premium to spot (the foreign currency is more expensive forward). If the domestic rate is lower, the forward is at a discount.

### Carry Trade
Borrow in a low-interest-rate currency and invest in a high-interest-rate currency, profiting from the interest rate differential. Profitable when UIP fails (i.e., the high-rate currency does not depreciate enough to offset the interest differential). Carry trades exhibit positive returns on average but with significant tail risk — sudden unwinds during risk-off episodes can cause severe losses (negative skewness, fat tails).

### Cross Rate
Derive the exchange rate between two currencies using their rates against a common third currency:

EUR/GBP = (EUR/USD) / (GBP/USD)

For example, if EUR/USD = 1.10 and GBP/USD = 1.27, then EUR/GBP = 1.10 / 1.27 = 0.8661.

### Currency Hedging
Use forward contracts to eliminate FX risk in international investments. A US investor with EUR assets can sell EUR forward to lock in the conversion rate. The hedging cost equals the interest rate differential between the two currencies (per CIP). When the domestic rate exceeds the foreign rate, hedging earns a positive return; when it is lower, hedging has a cost.

### Real Exchange Rate
Adjusts the nominal exchange rate for relative price levels:

Real Rate = Nominal Rate × (Foreign Price Level / Domestic Price Level)

Changes in the real exchange rate reflect changes in competitiveness. If the real rate appreciates, domestic goods become more expensive relative to foreign goods.

### Purchasing Power Parity (PPP)
The long-run anchor for exchange rates. PPP posits that exchange rates should adjust so that identical goods cost the same across countries. Empirically, PPP holds poorly in the short run but provides a reasonable guide to fair value over decades. Deviations from PPP can persist for years.

### Currency Overlay
A systematic hedging program for international portfolios, managed separately from the underlying asset allocation. Overlay managers implement hedging ratios (e.g., hedge 50% of foreign exposure) and may make tactical adjustments based on valuation, carry, and momentum signals.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| CIP Forward Rate | F = S × (1+r_d)/(1+r_f) | Arbitrage-determined forward |
| UIP Expected Spot | E(S_t) = S_0 × (1+r_d)/(1+r_f) | Theoretical future spot |
| Forward Premium | (F-S)/S = (r_d-r_f)/(1+r_f) | Forward vs spot differential |
| Cross Rate | A/B = (A/C) / (B/C) | Derive from common currency |
| Real Exchange Rate | q = e × (P*/P) | Competitiveness measure |
| Hedging Cost | ≈ r_d - r_f (annualized) | Cost to hedge FX exposure |

## Worked Examples

### Example 1: Forward Rate Calculation
**Given:** USD/JPY spot = 150, US 1-year rate = 5%, Japan 1-year rate = 0.5%
**Calculate:** 1-year forward rate
**Solution:**
F = S × (1 + r_JPY) / (1 + r_USD)
F = 150 × (1 + 0.005) / (1 + 0.05)
F = 150 × 1.005 / 1.05
F = 150 × 0.95714 = 143.57

The forward rate is 143.57 JPY/USD. The yen is at a forward premium (fewer yen per dollar forward than spot) because Japanese rates are lower. A US investor hedging yen assets back to dollars would receive this favorable forward rate, effectively earning the interest rate differential.

### Example 2: Hedging Cost for EUR Investor
**Given:** EUR/USD spot = 1.10, EUR 1-year rate = 3%, USD 1-year rate = 5%
**Calculate:** Annual cost/benefit of hedging USD exposure back to EUR
**Solution:**
Forward rate: F = 1.10 × (1.03)/(1.05) = 1.10 × 0.98095 = 1.0790

A EUR investor hedging USD assets sells USD forward at 1.0790 EUR/USD.
Hedging benefit = (S - F) / S = (1.10 - 1.079) / 1.10 = 1.91%

Because EUR rates (3%) are lower than USD rates (5%), the EUR investor earns a positive hedging return of approximately 2% (the interest rate differential). The hedged return on USD assets for a EUR investor is the USD return plus approximately 2% from the hedge.

## Common Pitfalls
- Currency quoting conventions — EUR/USD vs USD/JPY use opposite conventions; always clarify which currency is base and which is quote
- Confusing nominal and real interest rate differentials — CIP uses nominal rates; real rate differentials affect real exchange rates differently
- Carry trade crash risk — carry strategies exhibit negative skewness and fat tails; profits accumulate slowly but losses can be sudden and severe
- CIP holds by arbitrage; UIP is a theory that often fails empirically — do not assume forward rates predict future spot rates

## Cross-References
- **historical-risk** (wealth-management plugin): return measurement in multi-currency portfolios
- **equities** (wealth-management plugin): international equity investing and currency effects
- **fixed-income-sovereign** (wealth-management plugin): international bond investing and rate differentials
- **asset-allocation** (wealth-management plugin): currency hedging decisions in portfolio context

## Running the Script

```bash
uv run scripts/currencies_and_fx.py            # run the demo (uses PEP 723 inline deps)
uv run scripts/currencies_and_fx.py --verify   # check demo outputs against the worked examples (exit 1 on mismatch)
python3 scripts/currencies_and_fx.py            # alternative (stdlib only, no installs needed)
```

The demo prints the calculations covered above; its values match the worked examples in this skill. Run `--help` for a list of the classes and functions. For programmatic use, import the module rather than running it — the demo only executes under `python currencies_and_fx.py`.


---

## SKILL: debt-management

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/debt-management` (MIT)
- Cuándo usarla: Provide frameworks for managing and paying off personal debt effectively. Use when the user asks about debt payoff strategies (avalanche vs snowball), refinancing decisions, debt consolidation, debt-to-income ratios, or the opportunity cost of paying off debt vs investing. Also trigger when users mention 'which debt to pay first', 'should I refinance', 'credit card debt', 'student loan payoff', 'DTI for mortgage', 'balance transfer', 'good debt vs bad debt', or ask how to get out of debt faster.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/wealth-management/skills/debt-management/` (debt_management.py)

# Debt Management

## Core Concepts

### Debt Avalanche
Pay minimum payments on all debts, then direct all extra payment to the debt with the **highest interest rate** first:

- **Mathematically optimal:** Minimizes total interest paid over the life of all debts
- Once the highest-rate debt is paid off, the freed-up payment rolls to the next highest rate
- Requires discipline — the highest-rate debt may also be the largest balance, meaning slow visible progress initially
- Always saves money compared to snowball, though the difference varies by debt profile

### Debt Snowball
Pay minimum payments on all debts, then direct all extra payment to the debt with the **smallest balance** first:

- **Psychologically effective:** Quick wins build momentum and motivation
- Research (Kellogg School) shows people are more likely to stick with snowball and actually become debt-free
- May cost more in total interest than avalanche, but adherence is higher
- Best for individuals who need motivational wins to stay committed

### Debt-to-Income Ratio (DTI)
Total monthly debt payments expressed as a percentage of gross monthly income:

- **Front-end DTI (housing ratio):** Monthly housing costs (PITI: principal, interest, taxes, insurance) / gross monthly income
  - Guideline: < 28%
- **Back-end DTI (total debt ratio):** All monthly debt payments (housing + car + student loans + credit cards + other) / gross monthly income
  - Guideline: < 36% (conventional), up to 43% (FHA), some lenders allow up to 50% for qualified borrowers
- DTI is a key factor in mortgage qualification and overall financial health assessment

### Refinancing Analysis
Compare the total cost of the existing loan vs the new loan, accounting for closing costs:

- **Monthly savings:** Old payment - new payment
- **Breakeven months:** Total closing costs / monthly savings
- **Total cost comparison:** Sum of all remaining payments (old) vs sum of all payments (new) + closing costs
- If you plan to keep the loan beyond the breakeven point, refinancing saves money
- Consider: remaining term, resetting the amortization clock, and cash-out implications

### Debt Consolidation
Combine multiple debts into a single loan, ideally at a lower interest rate:

- **Potential benefits:** Lower rate, single payment, simplified management
- **Risks:** Longer term may increase total interest even at lower rate; freed-up credit lines may tempt new borrowing
- **Evaluate:** Compare total interest paid (all debts independently) vs total interest paid (consolidated loan)
- Balance transfer cards (0% intro rate) can be effective but require payoff before the rate expires

### Good Debt vs Bad Debt
- **Good debt:** Low interest rate, potentially tax-deductible, finances an appreciating asset or increases earning power (mortgage, student loans, business loans)
- **Bad debt:** High interest rate, finances depreciating assets or consumption (credit cards, payday loans, auto loans on luxury vehicles)
- The line is not absolute — a low-rate auto loan for a reliable commuter car can be reasonable

### Opportunity Cost Analysis
When debt carries a low interest rate, paying it off aggressively may not be optimal:

- **Decision rule:** If expected after-tax investment return > after-tax debt interest rate, investing the extra cash may build more wealth
- **Example:** 3.5% mortgage (2.5% after tax deduction) vs 7-10% expected equity returns — investing likely wins mathematically
- **Caveats:** Investment returns are uncertain, debt payoff is guaranteed; psychological benefit of being debt-free has real value
- Consider risk tolerance: guaranteed 3.5% return (debt payoff) vs variable 7-10% (investing)

### Debt Payoff Timeline
Amortization calculation with extra payments:

- Standard amortization: n = -ln(1 - (P×r)/PMT) / ln(1+r)
- With extra payment: replace PMT with PMT + extra, recalculate n
- Total interest = (n × PMT) - P (adjusting for extra payments)

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Front-end DTI | Housing payments / gross monthly income | Mortgage qualification |
| Back-end DTI | All debt payments / gross monthly income | Overall debt health |
| Refinance breakeven | Closing costs / monthly savings | Months to recoup refi costs |
| Months to payoff | n = -ln(1 - Pr/PMT) / ln(1+r) | Debt payoff timeline |
| Total interest paid | (n × PMT) - Principal | Cost of borrowing |
| Effective rate (after tax) | r × (1 - marginal_tax_rate) | Tax-deductible debt comparison |

## Worked Examples

### Example 1: Avalanche vs snowball comparison
**Given:** Three debts with $500/month available for extra payments (above minimums):
- Credit card: $5,000 balance, 22% APR, $100 minimum
- Student loan: $12,000 balance, 6% APR, $200 minimum
- Personal loan: $3,000 balance, 15% APR, $75 minimum

**Calculate:** Order of payoff, total months, and total interest for each strategy (month-by-month simulation; see `scripts/debt_management.py`).
**Solution — Avalanche (highest rate first: 22% → 15% → 6%):**
1. Pay minimums on all ($375/mo). Extra $500 goes to credit card ($600/mo total to CC).
2. Credit card ($5K at 22%, $600/mo): paid off in month 10, ~$476 interest.
3. Freed payment rolls to the personal loan ($75 + $600 = $675/mo to PL): paid off in month 14, ~$408 interest.
4. All payments roll to the student loan ($200 + $675 = $875/mo): paid off in month 26, ~$1,062 interest (the 6% loan accrues interest on its full $12K balance throughout the earlier phases, not just at the end).
5. **Total: 26 months, ~$1,946 total interest.**

**Solution — Snowball (smallest balance first: $3K → $5K → $12K):**
1. Extra $500 goes to personal loan ($575/mo total to PL).
2. Personal loan ($3K at 15%, $575/mo): paid off in month 6, ~$123 interest.
3. Freed payment rolls to the credit card ($100 + $575 = $675/mo): paid off in month 14, ~$911 interest.
4. All payments roll to the student loan: paid off in month 26, ~$1,071 interest.
5. **Total: 26 months, ~$2,104 total interest.**

**Comparison:** Avalanche saves ~$158 in interest; both finish in 26 months. The difference is modest because the highest-rate debt is not the largest. Snowball gives a quicker first win (month 6 vs month 10 to first payoff) — for many people that motivational difference is worth $158.

### Example 2: Refinance breakeven
**Given:** Current mortgage: $300K remaining, 6.5%, 25 years left, payment $2,028/mo. New offer: 5.5%, 25 years, closing costs $6,000, payment $1,838/mo.
**Calculate:** Breakeven period and total interest savings.
**Solution:**
1. Monthly savings: $2,028 - $1,838 = **$190/month**.
2. Breakeven: $6,000 / $190 = **31.6 months ≈ 32 months (2 years 8 months)**.
3. If staying in the home beyond 32 months, refinancing saves money.
4. Total payments (old): 25 × 12 × $2,028 = $608,400 → total interest = $608,400 - $300,000 = $308,400.
5. Total payments (new): 25 × 12 × $1,838 + $6,000 = $557,400 → total interest = $557,400 - $300,000 = $257,400.
6. **Total interest savings: $308,400 - $257,400 = $51,000.**

## Common Pitfalls
- Ignoring psychological factors — snowball works better for many people despite costing slightly more in interest
- Not including all closing costs in refinancing analysis (origination fees, appraisal, title insurance, points)
- Consolidation at a lower rate but longer term may cost more in total interest — always compare total cost
- Paying off low-rate debt instead of investing (opportunity cost) without considering risk tolerance and guaranteed vs uncertain returns
- Not considering tax deductibility of mortgage or student loan interest when comparing effective rates
- Making only minimum payments on high-interest debt while saving in low-yield accounts
- Consolidation freeing up credit lines that lead to new debt accumulation
- Ignoring the amortization reset: refinancing to a new 30-year term extends the payoff date

## Cross-References
- **lending** (wealth-management plugin): mortgage analysis, loan terms, and amortization calculations
- **emergency-fund** (wealth-management plugin): adequate emergency fund prevents taking on new high-interest debt during crises
- **savings-goals** (wealth-management plugin): debt payoff competes with savings goals for cash flow allocation
- **tax-efficiency** (wealth-management plugin): tax deductibility of certain debt interest affects optimal payoff order
- **liquidity-management** (wealth-management plugin): debt payments are fixed obligations in cash flow planning
- **financial-planning-workflow** (advisory-practice plugin): debt payoff strategies are evaluated during the cash flow and recommendation phases of financial planning
- **insurance-planning** (wealth-management plugin): outstanding debt balances are a direct input to life insurance needs analysis
## Running the Script

```bash
uv run scripts/debt_management.py            # run the demo (uses PEP 723 inline deps)
uv run scripts/debt_management.py --verify   # check demo outputs against the worked examples (exit 1 on mismatch)
python3 scripts/debt_management.py            # alternative (requires: pip install numpy)
```

The demo prints the calculations covered above; its values match the worked examples in this skill. Run `--help` for a list of the classes and functions. For programmatic use, import the module rather than running it — the demo only executes under `python debt_management.py`.


---

## SKILL: fixed-income

- Fuente: `agiprolabs/claude-trading-skills` → `skills/fixed-income` (MIT)
- Cuándo usarla: [STUB] Bond pricing, yield curves, duration and convexity analysis, and DeFi lending rate modeling
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/fixed-income/` (bond_calculator.py)

# Fixed Income

> **Status: STUB** — This skill provides a basic bond calculator and an overview of planned capabilities. Full implementation is awaiting community contribution.

Fixed income analysis bridges traditional bond mathematics with DeFi lending rate modeling. Bond pricing fundamentals — present value of cash flows, yield curves, duration, and convexity — translate directly to analyzing DeFi lending protocols where depositors earn variable or fixed rates on crypto assets.

On Solana, lending protocols like Marginfi, Kamino, and Solend offer variable-rate lending/borrowing. Understanding term structure and rate dynamics helps optimize yield farming strategies and compare opportunities across protocols.

This skill is informational and analytical only. It does not provide financial advice or trading recommendations.

---

## Current Capabilities

This stub includes a working bond calculator with price, yield-to-maturity, duration, and convexity computations. See `scripts/bond_calculator.py` for the implementation.

```python
def bond_price(
    face: float, coupon_rate: float, ytm: float, periods: int, freq: int = 2
) -> float:
    """Calculate bond price as present value of all cash flows.

    Args:
        face: Face (par) value of the bond.
        coupon_rate: Annual coupon rate (decimal, e.g., 0.05 for 5%).
        ytm: Yield to maturity (annual, decimal).
        periods: Number of coupon periods remaining.
        freq: Coupon frequency per year (2 = semi-annual).

    Returns:
        Bond price (dirty price).
    """
    coupon = face * coupon_rate / freq
    y = ytm / freq
    pv_coupons = sum(coupon / (1 + y) ** t for t in range(1, periods + 1))
    pv_face = face / (1 + y) ** periods
    return pv_coupons + pv_face
```

Run the demo:

```bash
python scripts/bond_calculator.py --demo
```

---

## Planned Capabilities

When fully implemented, this skill will cover:

### Bond Pricing

| Concept | Description |
|---------|-------------|
| Clean/Dirty Price | Price excluding/including accrued interest |
| Accrued Interest | Interest earned since last coupon date |
| Day Count Conventions | 30/360, ACT/360, ACT/365, ACT/ACT |
| Zero-Coupon Bonds | Discount bonds with no periodic coupons |

### Yield Measures

| Yield Measure | Use Case |
|---------------|----------|
| Yield to Maturity (YTM) | Total return if held to maturity |
| Current Yield | Annual coupon / price |
| Yield to Call | Return if called at first call date |
| Spread to Benchmark | Credit risk premium over risk-free rate |

### Duration and Convexity

| Metric | Measures |
|--------|----------|
| Macaulay Duration | Weighted average time to cash flows |
| Modified Duration | Price sensitivity to yield changes |
| Effective Duration | Duration for bonds with embedded options |
| Convexity | Second-order price sensitivity |
| Dollar Duration (DV01) | Dollar change per 1bp yield move |

### Yield Curve Construction

| Method | Description |
|--------|-------------|
| Bootstrap | Extract spot rates from par bond prices |
| Nelson-Siegel | Parametric model with level, slope, curvature |
| Nelson-Siegel-Svensson | Extended model with additional curvature term |
| Cubic Spline | Non-parametric interpolation |

### DeFi Lending Rate Analysis

| Protocol | Chain | Type |
|----------|-------|------|
| Marginfi | Solana | Variable rate |
| Kamino | Solana | Variable rate |
| Solend | Solana | Variable rate |
| Aave | Ethereum/Multi | Variable + stable rate |
| Compound | Ethereum | Variable rate |

Planned DeFi features:
- Lending rate time series analysis
- Supply/borrow APY comparison across protocols
- Utilization rate impact on lending rates
- Fixed vs variable rate comparison (when fixed-rate protocols available)
- Rate arbitrage opportunity detection

---

## Prerequisites

```bash
# For full implementation
uv pip install numpy scipy

# For visualization
uv pip install matplotlib
```

The included `scripts/bond_calculator.py` uses only the Python standard library and runs without any dependencies.

---

## Use Cases

### Yield Farming Comparison
Compare DeFi lending rates across protocols using fixed income analytics. Annualize variable rates, compute effective yields accounting for compounding frequency, and identify the most capital-efficient opportunities.

### Lending Rate Analysis
Track lending rates over time to understand rate dynamics. Identify periods of rate compression (low utilization) vs rate expansion (high utilization) to time deposits optimally.

### Rate Arbitrage
Borrow at lower rates on one protocol and lend at higher rates on another. Duration and convexity concepts help assess the risk of rate changes during the arbitrage holding period.

### Risk Assessment
Use duration to estimate how lending positions change in value as rates move. Higher duration means greater sensitivity to rate changes.

---

## Quick Reference: Bond Pricing Formulas

**Bond price (present value of cash flows):**
```
P = Σ [C / (1+y)^t] + F / (1+y)^n
    t=1..n

Where:
  C = periodic coupon payment = Face * coupon_rate / frequency
  y = periodic yield = YTM / frequency
  F = face value
  n = total number of periods
```

**Macaulay Duration:**
```
D_mac = (1/P) * Σ [t * C / (1+y)^t] + (n * F) / ((1+y)^n * P)
```

**Modified Duration:**
```
D_mod = D_mac / (1 + y)
```

**Convexity:**
```
Convexity = (1/P) * Σ [t*(t+1) * C / (1+y)^(t+2)] + [n*(n+1)*F] / [(1+y)^(n+2) * P]
```

**Price change approximation:**
```
ΔP/P ≈ -D_mod * Δy + 0.5 * Convexity * (Δy)²
```

---

## Files

| File | Description |
|------|-------------|
| `references/planned_features.md` | Planned features, bond formulas, DeFi protocols, and implementation priorities |
| `scripts/bond_calculator.py` | Bond price, YTM, duration, and convexity calculator |

---

## Contributing

This skill is a stub awaiting full implementation. To contribute:

1. Implement yield curve bootstrapping from market data
2. Add Nelson-Siegel yield curve fitting
3. Build DeFi lending rate data fetcher (Marginfi, Kamino APIs)
4. Add day count convention support for accurate accrued interest
5. Create rate comparison dashboard across protocols

See `references/planned_features.md` for the full feature list and implementation priorities.

---

*This skill provides analytical tools and mathematical models for informational purposes only. It does not constitute financial advice. Fixed income and DeFi lending involve risk of loss.*

### Referencia: references/planned_features.md

# Fixed Income — Planned Features

> **Status: STUB** — This document outlines the planned feature set for the fixed-income skill.

---

## 1. Bond Pricing (Implemented in stub)

### Present Value of Cash Flows

The fundamental bond pricing equation:

```
P = Σ [C / (1+y)^t] + F / (1+y)^n
    t=1..n

Where:
  P = bond price (dirty price)
  C = periodic coupon = Face * annual_coupon_rate / frequency
  y = periodic yield = YTM / frequency
  F = face (par) value
  n = total coupon periods remaining
```

### Clean vs Dirty Price

```
Clean Price = Dirty Price - Accrued Interest
Accrued Interest = C * (days since last coupon / days in coupon period)
```

Day count conventions affect accrued interest calculation:
- **30/360**: Assumes 30-day months, 360-day year
- **ACT/360**: Actual days elapsed, 360-day year
- **ACT/365**: Actual days elapsed, 365-day year
- **ACT/ACT**: Actual days in both numerator and denominator

Priority: Day count conventions are **Medium** priority for stub expansion.

---

## 2. Yield Measures

### Yield to Maturity (Implemented — Newton's method solver)

YTM is the discount rate that equates the bond price to the present value of all future cash flows. Solved numerically since no closed-form solution exists for coupon bonds.

### Current Yield (Implemented)

```
Current Yield = Annual Coupon / Clean Price
```

Simple but ignores time value and capital gains/losses.

### Yield to Call (Planned)

For callable bonds, replace maturity with call date and face value with call price:

```
P = Σ [C / (1+y)^t] + Call_Price / (1+y)^n_call
```

### Spread Measures (Planned)

| Spread | Definition |
|--------|-----------|
| Nominal Spread | YTM - Treasury YTM at same maturity |
| Z-Spread | Constant spread over zero curve |
| OAS | Spread over zero curve, adjusting for optionality |

Priority: **Low** for crypto context (no active crypto bond market yet).

---

## 3. Duration and Convexity (Implemented in stub)

### Macaulay Duration

Weighted average time to receive cash flows:

```
D_mac = (1/P) * [Σ t*C/(1+y)^t + n*F/(1+y)^n]
```

Interpretation: A bond with Macaulay duration of 5.2 years behaves like a zero-coupon bond maturing in 5.2 years.

### Modified Duration

Price sensitivity per unit yield change:

```
D_mod = D_mac / (1 + y/freq)

ΔP/P ≈ -D_mod * Δy
```

A modified duration of 4.8 means a 1% yield increase causes approximately a 4.8% price decline.

### Convexity

Second-order price sensitivity (curvature):

```
Convexity = (1/P) * Σ [t*(t+1)*CF_t / (1+y)^(t+2)]

ΔP/P ≈ -D_mod * Δy + 0.5 * Convexity * (Δy)²
```

Convexity improves the duration approximation for large yield changes.

### DV01 / Dollar Duration

Dollar value of a basis point:

```
DV01 = D_mod * P * 0.0001
```

Priority: All duration/convexity measures are **implemented** in the stub calculator.

---

## 4. Yield Curve Construction (Planned)

### Bootstrap Method

Extract spot (zero) rates from par bond prices sequentially:

1. Start with the shortest maturity bond to get the first spot rate
2. Use known spot rates to solve for the next spot rate
3. Repeat until the full curve is constructed

```
For a 2-period bond:
P = C/(1+z1) + (C+F)/(1+z2)^2
Solve for z2 given known z1
```

### Nelson-Siegel Model

Parametric yield curve with three factors:

```
y(τ) = β0 + β1 * [(1-e^(-τ/λ)) / (τ/λ)]
         + β2 * [(1-e^(-τ/λ)) / (τ/λ) - e^(-τ/λ)]

Where:
  β0 = long-term rate level
  β1 = slope (short-term component)
  β2 = curvature (medium-term hump)
  λ  = decay factor
  τ  = time to maturity
```

### Nelson-Siegel-Svensson Extension

Adds a second curvature term for more flexibility:

```
y(τ) = Nelson-Siegel + β3 * [(1-e^(-τ/λ2)) / (τ/λ2) - e^(-τ/λ2)]
```

Priority: **High** — yield curve construction is fundamental for rate analysis.

---

## 5. DeFi Lending Protocols on Solana

### Marginfi

- Variable-rate lending/borrowing
- Utilization-based rate model
- API: On-chain program data via Solana RPC
- Key metric: Supply APY, borrow APY, utilization rate

### Kamino

- Automated lending vaults
- Concentrated liquidity integration
- API: REST API + on-chain data
- Key metric: Vault APY, leverage ratio

### Solend

- Pool-based lending
- Multiple isolated pools by risk tier
- API: REST API at `api.solend.fi`
- Key metric: Pool APY, reserve utilization

### Cross-Protocol Analysis (Planned)

- Rate comparison dashboard
- Historical rate time series
- Utilization-to-rate curve fitting
- Optimal deposit allocation across protocols
- Rate arbitrage detection (borrow low, lend high)

### Rate Model Mathematics

Most DeFi protocols use a kinked utilization model:

```
If utilization ≤ optimal:
  borrow_rate = base_rate + (utilization / optimal) * slope1

If utilization > optimal:
  borrow_rate = base_rate + slope1 + ((utilization - optimal) / (1 - optimal)) * slope2

supply_rate = borrow_rate * utilization * (1 - reserve_factor)
```

Priority: **High** — DeFi lending rate analysis is the primary crypto use case.

---

## 6. Implementation Priorities

| Priority | Feature | Complexity | Dependencies |
|----------|---------|-----------|-------------|
| 1 (Done) | Bond price calculator | Low | math stdlib |
| 2 (Done) | YTM solver | Low | math stdlib |
| 3 (Done) | Duration & convexity | Low | math stdlib |
| 4 | Day count conventions | Low | datetime |
| 5 | Yield curve bootstrap | Medium | numpy |
| 6 | Nelson-Siegel fitting | Medium | scipy |
| 7 | DeFi rate data fetcher | Medium | httpx |
| 8 | Rate comparison tool | Medium | httpx, pandas |
| 9 | Rate model curve fitting | Medium | scipy |
| 10 | Fixed vs variable analysis | High | numpy, scipy |

---

## 7. Crypto-Specific Considerations

- **No standard maturities:** DeFi lending is mostly variable rate with no fixed term
- **Continuous compounding:** Many protocols compound per block or per slot
- **Utilization-driven rates:** Rates change with pool utilization, unlike fixed coupon bonds
- **Smart contract risk:** Lending rate analysis must account for protocol risk premium
- **Cross-chain rates:** Same protocol may offer different rates on different chains
- **Token incentives:** Effective yield includes token rewards (emissions) on top of base APY

---

*This document is for informational and planning purposes only. It does not constitute financial advice.*


---

## SKILL: fixed-income-corporate

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/fixed-income-corporate` (MIT)
- Cuándo usarla: Analyze corporate bonds and credit instruments including investment grade and high yield debt. Use when the user asks about corporate bonds, credit spreads (OAS, Z-spread, G-spread), credit ratings, default probabilities, callable bonds, or private credit. Also trigger when users mention 'junk bonds', 'fallen angel', 'yield-to-worst', 'covenant analysis', 'CDS spreads', 'recovery rates', 'direct lending', 'mezzanine debt', 'BBB downgrade risk', or ask how to evaluate corporate credit risk.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/wealth-management/skills/fixed-income-corporate/` (fixed_income_corporate.py)

# Fixed Income — Corporate

## Core Concepts

### Credit Spreads
Compensation for default risk, liquidity risk, and downgrade risk above the risk-free rate. Multiple spread measures exist with increasing precision:

**G-spread (Government Spread):** Bond yield minus interpolated Treasury yield of the same maturity. Simple but assumes a flat term structure between benchmark maturities.

**Z-spread (Zero-Volatility Spread):** The constant spread added to each point on the risk-free spot rate curve such that the sum of discounted cash flows equals the bond's market price. Superior to G-spread because it accounts for the full shape of the term structure.

**OAS (Option-Adjusted Spread):** For bonds with embedded options, OAS = Z-spread minus the value of the embedded option. OAS represents the "true" credit compensation after removing the option component. Requires an interest rate model to compute.

### Credit Ratings
AAA/AA/A/BBB are investment grade. BB/B/CCC/CC/C/D are high yield (speculative grade). The BBB/BB boundary is the most consequential threshold — many institutional mandates prohibit sub-investment-grade holdings. A downgrade across this boundary ("fallen angel") forces selling by constrained investors.

### Migration Matrix
A transition matrix shows the probability of moving from one rating to another over a 1-year horizon. A BBB-rated issuer has roughly 85-90% probability of remaining BBB, 4-5% chance of upgrade, 4-5% chance of downgrade, and a small probability (~0.2%) of default. Migration matrices are published annually by rating agencies.

### Default Probability, Loss Given Default, and Recovery Rate
- PD = Probability of Default over a given horizon
- LGD = Loss Given Default (percentage of exposure lost)
- Recovery Rate (RR) = 1 - LGD
- Expected Loss: EL = PD × LGD × EAD (Exposure at Default)

Recovery rates vary by seniority: senior secured (60-65%), senior unsecured (40-50%), subordinated (20-30%).

### Callable Bonds
The issuer can redeem the bond early. Call schedules specify prices and dates. Yield-to-call (YTC) is calculated using the call date and call price. Yield-to-worst (YTW) is the minimum of YTM and all possible YTCs. For callable bonds, OAS is the appropriate spread measure (not G-spread or Z-spread).

### Covenants
**Maintenance covenants:** Tested periodically (e.g., quarterly). Issuer must maintain financial ratios at all times. Common in bank loans.

**Incurrence covenants:** Tested only when the issuer takes a specific action (e.g., issues new debt). Common in bond indentures. Key covenants include leverage ratio (Debt/EBITDA), interest coverage (EBITDA/Interest), and restricted payments.

### Private Credit
Direct lending by non-bank lenders to middle-market companies. Offers an illiquidity premium of 150-400bp over comparable syndicated loans. Typically features stronger covenant protection than public market deals. Valuations are mark-based (quarterly), which smooths reported volatility.

### CDS (Credit Default Swaps)
A derivative where the protection buyer pays a periodic spread and receives payment upon a credit event. CDS spreads can be used to derive market-implied default probabilities. CDS spreads are often more responsive to credit deterioration than bond spreads.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| G-spread | Bond Yield - Interpolated Treasury Yield | Simple spread measure |
| Z-spread | Constant spread s: P = sum CF_t / (1+s_t+s)^t | Full curve spread |
| OAS | Z-spread - Option Cost | Spread for callable bonds |
| Expected Loss | EL = PD × LGD × EAD | Credit loss estimation |
| Recovery Rate | RR = 1 - LGD | Recovery from default |
| Yield-to-Worst | min(YTM, YTC_1, YTC_2, ...) | Conservative yield measure |

## Worked Examples

### Example 1: Compare Z-spread vs G-spread
**Given:** A 7-year corporate bond yields 5.8%. The 7-year interpolated Treasury yield is 4.5%. The Z-spread (computed using the full spot curve) is 118bp.
**Calculate:** G-spread and compare to Z-spread
**Solution:**
G-spread = 5.8% - 4.5% = 1.30% = 130bp
Z-spread = 118bp
The G-spread (130bp) exceeds the Z-spread (118bp) by 12bp. This difference arises because the G-spread uses a single interpolated benchmark point while the Z-spread properly accounts for the shape of the entire yield curve. In a steep curve environment, G-spread tends to overstate the true spread.

### Example 2: Expected Loss Calculation
**Given:** PD = 2% (annual), LGD = 60%, EAD = $1,000,000
**Calculate:** Expected annual loss
**Solution:**
EL = PD × LGD × EAD
EL = 0.02 × 0.60 × $1,000,000
EL = $12,000

The expected annual credit loss is $12,000, or 1.2% of the exposure. This represents the actuarial cost of credit risk — the spread must at least cover this expected loss, with additional compensation for unexpected losses and risk aversion.

## Common Pitfalls
- Using G-spread for callable bonds — use OAS instead, which removes the option component
- Ignoring liquidity premium in spread analysis — part of the spread compensates for illiquidity, not just default risk
- Rating agency lag vs market-implied credit quality — CDS spreads often move before rating actions
- Assuming recovery rates are constant — they vary significantly by seniority and economic cycle (lower in recessions)

## Cross-References
- **fixed-income-sovereign** (wealth-management plugin): the Treasury curve used as the risk-free benchmark
- **fixed-income-structured** (wealth-management plugin): CLOs and structured credit products
- **alternatives** (wealth-management plugin): private credit as an alternative investment
- **asset-allocation** (wealth-management plugin): credit allocation in multi-asset portfolios

## Running the Script

```bash
uv run scripts/fixed_income_corporate.py            # run the demo (uses PEP 723 inline deps)
uv run scripts/fixed_income_corporate.py --verify   # check demo outputs against the worked examples (exit 1 on mismatch)
python3 scripts/fixed_income_corporate.py            # alternative (requires: pip install numpy scipy)
```

The demo prints the calculations covered above; its values match the worked examples in this skill. Run `--help` for a list of the classes and functions. For programmatic use, import the module rather than running it — the demo only executes under `python fixed_income_corporate.py`.


---

## SKILL: fixed-income-municipal

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/fixed-income-municipal` (MIT)
- Cuándo usarla: Analyze municipal bonds including tax-equivalent yield calculations, GO vs revenue bond evaluation, and muni credit analysis. Use when the user asks about municipal bonds, tax-exempt income, tax-equivalent yield, AMT bonds, callable bonds, yield-to-worst on munis, or muni credit quality. Also trigger when users mention 'muni bonds', 'tax-free bonds', 'state tax exemption', 'general obligation', 'revenue bonds', 'Build America Bonds', 'muni yield ratio', 'de minimis rule', or ask whether munis make sense for their tax bracket.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/wealth-management/skills/fixed-income-municipal/` (fixed_income_municipal.py)

# Fixed Income — Municipal

## Core Concepts

### General Obligation (GO) Bonds
Backed by the full faith, credit, and taxing power of the issuing municipality. The issuer pledges to use any available revenue source (property tax, income tax, sales tax) to repay bondholders. GO bonds typically require voter approval and are considered safer due to the broad taxing pledge.

### Revenue Bonds
Backed solely by the revenue generated from a specific project or source — toll roads (toll collections), water/sewer systems (utility fees), hospitals (patient revenue), airports (landing fees, terminal rents). Revenue bonds typically carry higher yields than GO bonds of comparable maturity and credit quality because of the narrower revenue pledge.

### Tax-Equivalent Yield (TEY)
The core calculation for comparing municipal bonds to taxable alternatives:

Federal only: TEY = Muni Yield / (1 - federal_marginal_rate)

Federal + state (for in-state munis): TEY = Muni Yield / (1 - federal_rate - state_rate × (1 - federal_rate))

This converts a tax-exempt yield to the pre-tax yield a taxable bond would need to offer to match the muni's after-tax income.

Note: the state_rate × (1 - federal_rate) term assumes state income tax is fully deductible against federal tax. For taxpayers at or above the SALT deduction cap (or taking the standard deduction), state tax provides no incremental federal deduction, and the formula simplifies to TEY = Muni Yield / (1 - federal_rate - state_rate) — the combined formula above understates the in-state muni's advantage for capped itemizers and overstates the precision of the comparison generally. Check the client's actual SALT position before choosing the formula.

### Alternative Minimum Tax (AMT)
Certain private activity bonds generate interest that is subject to AMT. For taxpayers subject to AMT, the tax advantage of these bonds is reduced. AMT-subject bonds typically trade at slightly higher yields to compensate. Non-AMT munis (governmental purpose bonds) are not affected.

### Muni Credit Analysis
**GO bonds:** evaluate tax base diversity and trends, debt burden ratios (debt per capita, debt/assessed value), fund balance as % of expenditures, economic base (population, employment), pension/OPEB obligations.

**Revenue bonds:** evaluate debt service coverage ratio (DSCR = net revenue / annual debt service), rate covenants, additional bonds tests, demand analysis, and reserve fund adequacy.

### De Minimis Tax Rule
Discount bonds purchased below a threshold (typically par minus 0.25% per year to maturity) may lose tax-exempt status on the discount portion — the gain is taxed as ordinary income rather than being tax-exempt. This affects the after-tax return calculation for discount munis.

### Muni Yield Ratios
Muni yield / Treasury yield. Historically this ratio averages approximately 80% for AAA munis. Ratios above 80-85% suggest munis are cheap relative to Treasuries; below 70% suggests they are rich. The ratio varies with supply/demand, tax policy expectations, and credit conditions.

### Build America Bonds (BABs)
Taxable municipal bonds created under the 2009 stimulus. The federal government subsidizes 35% of interest cost. Expired for new issuance after 2010 but outstanding BABs continue to trade. They allowed issuers to access the broader taxable bond market.

### Pre-Refunded/Escrowed Bonds
When an issuer advance-refunds a callable bond, it places US Treasuries in escrow sufficient to pay remaining coupons and the call price. These defeased bonds are effectively AAA-quality and trade at very tight spreads.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| TEY (federal only) | Muni Yield / (1 - federal_rate) | Compare muni to taxable bond |
| TEY (federal + state) | Muni Yield / (1 - fed_rate - state_rate × (1 - fed_rate)) | In-state muni comparison |
| DSCR | Net Revenue / Annual Debt Service | Revenue bond credit quality |
| De Minimis Threshold | Par - 0.25% × years to maturity | Tax treatment of discount munis |
| Muni Yield Ratio | Muni Yield / Treasury Yield | Relative value assessment |

## Worked Examples

### Example 1: Tax-Equivalent Yield with Federal and State Tax
**Given:** Muni yield = 3.5%, federal marginal rate = 37%, state marginal rate = 5%
**Calculate:** Tax-equivalent yield for an in-state bond
**Solution:**
TEY = 3.5% / (1 - 0.37 - 0.05 × (1 - 0.37))
TEY = 3.5% / (1 - 0.37 - 0.05 × 0.63)
TEY = 3.5% / (1 - 0.37 - 0.0315)
TEY = 3.5% / 0.5985
TEY = 5.85%

A taxable bond would need to yield 5.85% to match the after-tax income of this 3.5% muni for this taxpayer. The state tax benefit adds approximately 29bp of value compared to the federal-only TEY of 5.56%.

### Example 2: GO vs Revenue Bond Comparison
**Given:** Same issuer, same maturity (10 years). GO bond yields 3.2%, revenue bond (water/sewer) yields 3.6%. DSCR on revenue bond = 1.8x.
**Calculate:** Which bond offers better value?
**Solution:**
The revenue bond yields 40bp more than the GO bond. The DSCR of 1.8x is well above the typical 1.25x minimum for investment grade, indicating strong coverage. Water/sewer is an essential service with stable demand. The 40bp additional yield compensates for the narrower revenue pledge, but the strong coverage ratio suggests the credit risk is modest. For investors comfortable with revenue bond structures, the 40bp pickup may represent good relative value.

## Common Pitfalls
- Forgetting state tax benefits for in-state bonds — the combined federal+state TEY can be meaningfully higher than federal-only
- AMT implications for high-income investors — private activity bond interest may trigger AMT liability
- De minimis rule on discount munis — gains on deep-discount munis may be taxed as ordinary income
- Confusing call provisions — many munis are callable at par after 10 years; always check yield-to-worst

## Cross-References
- **time-value-of-money** (core plugin): present value and discounting fundamentals
- **fixed-income-sovereign** (wealth-management plugin): yield curve context and duration concepts
- **fixed-income-corporate** (wealth-management plugin): comparing muni spreads to corporate spreads
- **tax-efficiency** (wealth-management plugin): muni bonds as a primary tax management tool

## Running the Script

```bash
uv run scripts/fixed_income_municipal.py            # run the demo (uses PEP 723 inline deps)
uv run scripts/fixed_income_municipal.py --verify   # check demo outputs against the worked examples (exit 1 on mismatch)
python3 scripts/fixed_income_municipal.py            # alternative (requires: pip install numpy)
```

The demo prints the calculations covered above; its values match the worked examples in this skill. Run `--help` for a list of the classes and functions. For programmatic use, import the module rather than running it — the demo only executes under `python fixed_income_municipal.py`.


---

## SKILL: fixed-income-sovereign

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/fixed-income-sovereign` (MIT)
- Cuándo usarla: Analyze US Treasury securities and interest rate risk: bond pricing, yield curve construction, duration, convexity, TIPS, and forward/spot rate analysis. Use when the user asks about Treasury bonds, yield curve construction, interest rate risk, duration, convexity, TIPS, or breakeven inflation rates. Also trigger when users mention 'T-bills', 'T-notes', 'bond pricing', 'yield to maturity', 'inverted yield curve', 'forward rates', 'spot rates', 'DV01', 'real yields', or ask how bonds react to interest rate changes.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/wealth-management/skills/fixed-income-sovereign/` (fixed_income_sovereign.py)

# Fixed Income — Sovereign

Scope: US Treasuries and rates analytics. Sovereign *credit* risk — emerging market debt, default analysis, country risk spreads — is out of scope for this skill.

## Core Concepts

### Bond Pricing
The price of a bond is the present value of its future cash flows:

P = sum(t=1 to n) [C / (1+y)^t] + F / (1+y)^n

where C = coupon payment per period, y = yield to maturity per period, F = face value, n = total number of periods. For semi-annual bonds, divide the annual coupon by 2 and the annual yield by 2, and double the number of years to get n.

### Yield to Maturity (YTM)
The discount rate y that solves the bond pricing equation — the single rate that equates the bond's market price to the present value of all future cash flows. Assumes reinvestment of coupons at the YTM rate. It is the standard yield measure for bonds.

### Current Yield
Current Yield = Annual Coupon / Price. A simple income measure that ignores capital gains/losses and the time value of money.

### Yield Curve: Spot Rates, Forward Rates, Par Curve
The spot curve gives zero-coupon yields for each maturity. The par curve gives coupon rates at which bonds would price at par. Forward rates are implied future rates derived from spot rates. The three curves contain equivalent information and can be derived from one another.

### Bootstrapping the Spot Curve
Extract spot (zero-coupon) rates from par yields by starting at the shortest maturity and working outward. Each step uses previously derived spot rates to solve for the next spot rate.

### Forward Rate
The implied rate between two future dates derived from spot rates:

f(t1,t2) = [(1+s_t2)^t2 / (1+s_t1)^t1]^(1/(t2-t1)) - 1

where s_t1 and s_t2 are spot rates for maturities t1 and t2.

### Duration (Macaulay)
The weighted average time to receive cash flows, where weights are the present value of each cash flow as a proportion of the bond's price:

D_mac = (1/P) × sum(t × CF_t / (1+y)^t)

Measured in years. Longer maturity, lower coupon, and lower yield all increase duration.

### Modified Duration
D_mod = D_mac / (1 + y/m)

where m = number of coupon periods per year. Gives the approximate percentage price change for a 1 percentage point change in yield: dP/P ≈ -D_mod × dy.

### Dollar Duration (DV01)
The dollar change in price for a 1 basis point change in yield:

DV01 ≈ -D_mod × P × 0.0001

Used for hedging — match DV01 exposures to immunize a portfolio against parallel rate shifts.

### Convexity
Measures the curvature of the price-yield relationship (second derivative):

C = (1/P) × sum(t(t+1) × CF_t / (1+y)^(t+2))

For option-free bonds, convexity is always positive — duration alone overstates losses and understates gains.

### Price Change Approximation
ΔP/P ≈ -D_mod × Δy + 0.5 × Convexity × (Δy)²

The convexity term is a correction that becomes important for large yield changes.

### TIPS (Treasury Inflation-Protected Securities)
Principal adjusts with CPI. The coupon rate is fixed but applied to the inflation-adjusted principal. Real yield = TIPS yield. Breakeven inflation = nominal Treasury yield - TIPS real yield. TIPS have a deflation floor that protects par value at maturity.

### Key Rate Duration
Sensitivity to specific points on the yield curve (e.g., 2yr, 5yr, 10yr, 30yr). Allows analysis of non-parallel yield curve shifts such as steepening, flattening, or butterfly moves. Sum of key rate durations equals effective duration.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Bond Price | P = sum C/(1+y)^t + F/(1+y)^n | Price from yield |
| Current Yield | Annual Coupon / Price | Simple income measure |
| Forward Rate | f(t1,t2) = [(1+s_t2)^t2 / (1+s_t1)^t1]^(1/(t2-t1)) - 1 | Implied future rate |
| Macaulay Duration | (1/P) × sum(t × CF_t / (1+y)^t) | Weighted avg time to cash flows |
| Modified Duration | D_mac / (1 + y/m) | % price sensitivity to yield |
| DV01 | D_mod × P × 0.0001 | Dollar price change per 1bp |
| Convexity | (1/P) × sum(t(t+1) × CF_t / (1+y)^(t+2)) | Curvature of price-yield curve |
| Price Change | ΔP/P ≈ -D_mod×Δy + 0.5×Convexity×(Δy)² | Estimate price impact of rate move |

## Worked Examples

### Example 1: Price a 5-Year 4% Semi-Annual Coupon Bond at 5% YTM
**Given:** Face = $1,000, coupon = 4% (semi-annual), YTM = 5%, maturity = 5 years
**Calculate:** Bond price
**Solution:**
Semi-annual coupon = $1,000 × 4% / 2 = $20
Semi-annual yield = 5% / 2 = 2.5%
Number of periods = 5 × 2 = 10
P = $20 × [(1 - (1.025)^(-10)) / 0.025] + $1,000 / (1.025)^10
P = $20 × 8.7521 + $1,000 × 0.7812
P = $175.04 + $781.20 = $956.24

The bond trades at a discount ($956.24 < $1,000) because the coupon rate (4%) is below the market yield (5%).

### Example 2: Modified Duration and Price Change Estimate
**Given:** A bond with Macaulay duration = 4.5 years, YTM = 5% (semi-annual), price = $956.24, convexity = 22.5
**Calculate:** Estimated price change for a +50bp rate increase
**Solution:**
D_mod = 4.5 / (1 + 0.05/2) = 4.5 / 1.025 = 4.39 years
ΔP/P ≈ -4.39 × 0.005 + 0.5 × 22.5 × (0.005)²
ΔP/P ≈ -0.02195 + 0.000281 = -0.02167 = -2.167%
ΔP ≈ -2.167% × $956.24 = -$20.72
New price ≈ $956.24 - $20.72 = $935.52

Duration alone would estimate -2.195%; the convexity correction reduces the estimated loss by about 3bp.

## Common Pitfalls
- Confusing Macaulay and modified duration — Macaulay is in years, modified gives price sensitivity
- Ignoring convexity for large yield changes — duration alone overstates losses and understates gains
- Day count conventions (30/360 vs actual/actual) — Treasuries use actual/actual, corporates use 30/360
- Clean price vs dirty price (accrued interest) — quoted prices exclude accrued interest, but settlement requires paying it

## Cross-References
- **time-value-of-money** (core plugin): discounting and present value fundamentals
- **fixed-income-corporate** (wealth-management plugin): credit spreads over the sovereign curve
- **fixed-income-municipal** (wealth-management plugin): muni-to-Treasury yield ratios
- **asset-allocation** (wealth-management plugin): bonds as an asset class in portfolio construction

## Running the Script

```bash
uv run scripts/fixed_income_sovereign.py            # run the demo (uses PEP 723 inline deps)
uv run scripts/fixed_income_sovereign.py --verify   # check demo outputs against the worked examples (exit 1 on mismatch)
python3 scripts/fixed_income_sovereign.py            # alternative (requires: pip install numpy scipy)
```

The demo prints the calculations covered above; its values match the worked examples in this skill. Run `--help` for a list of the classes and functions. For programmatic use, import the module rather than running it — the demo only executes under `python fixed_income_sovereign.py`.


---

## SKILL: fixed-income-structured

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/fixed-income-structured` (MIT)
- Cuándo usarla: Analyze structured fixed income products including mortgage-backed securities, asset-backed securities, and CLOs. Use when the user asks about MBS, ABS, CLOs, CDOs, prepayment risk, tranching, or waterfall structures. Also trigger when users mention 'mortgage bonds', 'agency MBS', 'pass-through securities', 'PSA prepayment speed', 'negative convexity', 'extension risk', 'contraction risk', 'CMO tranches', 'securitization', or ask how structured products redistribute credit and prepayment risk.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/wealth-management/skills/fixed-income-structured/` (fixed_income_structured.py)

# Fixed Income — Structured Products

## Core Concepts

### MBS Pass-Throughs
A pool of mortgages whose cash flows (principal, interest, prepayments) are passed through to investors on a pro-rata basis. Agency MBS (Ginnie Mae, Fannie Mae, Freddie Mac) carry a government or GSE guarantee against credit losses, isolating prepayment risk as the primary concern. Non-agency MBS lack this guarantee and carry both credit and prepayment risk.

### Prepayment Risk
Borrowers can refinance when rates drop, returning principal early. This creates negative convexity — when rates fall, MBS prices rise less than comparable Treasuries because prepayments accelerate and shorten the bond's effective life. Prepayment risk has two faces:

**Contraction risk:** Rates fall, prepayments accelerate, duration shortens. Investors receive principal back when reinvestment rates are lower.

**Extension risk:** Rates rise, prepayments slow, duration extends. Investors are locked into below-market coupons for longer than expected.

### PSA Prepayment Model
The Public Securities Association model provides a benchmark prepayment speed:

100% PSA = ramp from 0% CPR to 6% CPR linearly over the first 30 months, then constant at 6% CPR thereafter.

At 150% PSA, all speeds are multiplied by 1.5 (e.g., the plateau is 9% CPR). At 200% PSA, the plateau is 12% CPR.

### CPR and SMM
**CPR (Conditional Prepayment Rate):** Annualized prepayment rate as a percentage of the remaining pool balance.

**SMM (Single Monthly Mortality):** Monthly prepayment rate.

SMM = 1 - (1 - CPR)^(1/12)

### Weighted Average Life (WAL)
WAL = sum(t × Principal_t) / Total Principal. Unlike maturity, WAL accounts for the timing of principal repayments (both scheduled and prepayments). WAL is shorter than maturity for amortizing securities and is sensitive to prepayment assumptions.

### CMO Tranches
Collateralized Mortgage Obligations redistribute MBS cash flows into tranches with different risk profiles:

**Sequential pay:** Principal flows to the first tranche until retired, then the second, etc. Earlier tranches have shorter duration, later tranches have longer duration.

**PAC (Planned Amortization Class):** Provides a predictable principal schedule within a band of prepayment speeds (e.g., 100-250% PSA). Stability comes at the expense of companion/support tranches that absorb prepayment variability.

**Support/Companion tranches:** Absorb excess or deficit prepayments to protect PAC tranches. Highly volatile duration.

### ABS (Asset-Backed Securities)
Securitized pools of non-mortgage assets:
- Auto loans: amortizing, relatively predictable cash flows
- Credit cards: revolving, with a revolving period followed by a controlled amortization period
- Student loans: longer duration, income-driven repayment creates uncertainty

### CLOs (Collateralized Loan Obligations)
Tranched portfolios of leveraged loans (typically 150-250 loans). AAA tranches benefit from significant subordination (30-40% of the structure below them). Equity tranches receive residual cash flows after all senior tranches are paid. Waterfall tests (overcollateralization and interest coverage tests) redirect cash flows to protect senior tranches when the portfolio deteriorates.

### Waterfall Structure
Cash flows are distributed by seniority: senior tranches receive interest and principal first, mezzanine next, equity last. If pool performance deteriorates, lower tranches absorb losses first (subordination protects senior tranches). Overcollateralization (OC) tests and interest coverage (IC) tests trigger cash flow diversions when breached.

### OAS for Structured Products
OAS is essential for MBS because it captures prepayment optionality. Standard modified duration is inappropriate for MBS — use effective duration (computed via OAS models) or empirical duration. Monte Carlo simulation of interest rate paths and corresponding prepayment responses is the standard valuation approach for MBS.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| SMM from CPR | SMM = 1 - (1-CPR)^(1/12) | Monthly prepayment rate |
| CPR from SMM | CPR = 1 - (1-SMM)^12 | Annualize monthly rate |
| PSA CPR (month t, t<=30) | CPR = 6% × (t/30) × PSA/100 | Ramping prepayment model |
| PSA CPR (month t, t>30) | CPR = 6% × PSA/100 | Plateau prepayment model |
| WAL | sum(t × Principal_t) / Total Principal | Average principal timing |
| OAS Price | P = E[sum CF_t(path) / (1+s_t+OAS)^t] | MBS valuation |

## Worked Examples

### Example 1: Convert PSA to CPR
**Given:** 150% PSA, month 20
**Calculate:** CPR and SMM in month 20
**Solution:**
At 100% PSA, month 20: CPR = 6% × (20/30) = 4.0%
At 150% PSA: CPR = 4.0% × 1.5 = 6.0%
SMM = 1 - (1 - 0.06)^(1/12) = 1 - (0.94)^(0.0833) = 1 - 0.99486 = 0.00514 = 0.514%

In month 20 at 150% PSA, approximately 0.514% of the remaining pool balance prepays each month, equivalent to 6.0% annualized.

### Example 2: CLO Tranche Analysis
**Given:** A CLO with $500M total assets. AAA tranche = $325M (65%), AA = $50M (10%), A = $37.5M (7.5%), BBB = $25M (5%), BB = $12.5M (2.5%), Equity = $50M (10%).
**Calculate:** Subordination level for the AAA tranche
**Solution:**
Subordination below AAA = AA + A + BBB + BB + Equity
= $50M + $37.5M + $25M + $12.5M + $50M = $175M
Subordination % = $175M / $500M = 35%

The AAA tranche has 35% subordination — the portfolio would need to lose more than 35% of its value before AAA investors suffer any principal loss. This substantial credit enhancement is why CLO AAA tranches have historically experienced zero defaults.

## Common Pitfalls
- Ignoring negative convexity of MBS — MBS underperform Treasuries in both rallies (contraction) and selloffs (extension)
- Using modified duration for MBS — use effective/OAS duration instead, as cash flows change with rates
- Assuming constant prepayment speeds — speeds vary with rates, seasonality, borrower demographics, and housing turnover
- Not understanding that waterfall mechanics affect tranche risk differently — senior and subordinate tranches of the same deal have very different risk profiles

## Cross-References
- **fixed-income-sovereign** (wealth-management plugin): the Treasury curve and duration/convexity concepts
- **fixed-income-corporate** (wealth-management plugin): credit spread concepts applied to non-agency MBS and CLOs
- **real-assets** (wealth-management plugin): real estate market fundamentals underlying MBS
- **asset-allocation** (wealth-management plugin): structured products in multi-asset portfolios

## Running the Script

```bash
uv run scripts/fixed_income_structured.py            # run the demo (uses PEP 723 inline deps)
uv run scripts/fixed_income_structured.py --verify   # check demo outputs against the worked examples (exit 1 on mismatch)
python3 scripts/fixed_income_structured.py            # alternative (requires: pip install numpy)
```

The demo prints the calculations covered above; its values match the worked examples in this skill. Run `--help` for a list of the classes and functions. For programmatic use, import the module rather than running it — the demo only executes under `python fixed_income_structured.py`.


---

## SKILL: fx-carry-trade

- Fuente: `anthropics/financial-services` → `plugins/partner-built/lseg/skills/fx-carry-trade` (Apache-2.0)
- Cuándo usarla: Evaluate FX carry trade opportunities by combining spot rates, forward points, interest rate differentials, volatility surface analysis, and historical price trends. Use when analyzing carry trades, comparing FX forward curves, assessing carry-to-vol ratios, or evaluating currency pair opportunities.

# FX Carry Trade Analysis

You are an expert FX strategist specializing in carry trade analysis. Combine spot rates, forward curves, volatility surfaces, and historical data from MCP tools to evaluate carry trade opportunities. Focus on routing tool outputs into carry-to-vol assessments — let the tools provide pricing data, you compute risk-adjusted metrics and recommend.

## Core Principles

A carry trade earns the interest rate differential but bears FX spot risk. The carry-to-vol ratio (annualized carry / ATM implied vol) is the key metric — it measures risk-adjusted attractiveness. Always map the full forward curve to find the optimal tenor, overlay the vol surface to assess risk, and check historical spot trends for directional context. Carry trades are short-volatility by nature; rising vol is the primary risk signal.

## Available MCP Tools

- **`fx_spot_price`** — Current spot rate for a currency pair. Returns mid/bid/ask. Starting point for all carry analysis.
- **`fx_forward_price`** — Forward rate at a specific tenor. Returns forward points and outright rate. Use to compute carry at the target tenor.
- **`fx_forward_curve`** — Full forward curve across all standard tenors. Two-phase: list then calculate. Use to map the carry term structure.
- **`fx_vol_surface`** — Implied volatility surface by delta and expiry. Returns ATM vol, risk reversals, butterflies. Use for carry-to-vol ratio and skew assessment.
- **`tscc_historical_pricing_summaries`** — Historical spot price data. Use to compute realized vol and assess spot trend direction.
- **`interest_rate_curve`** — Yield curves by currency. Use to understand the rate differential driving the carry.

## Tool Chaining Workflow

1. **Get Spot Rate:** Call `fx_spot_price` for the currency pair. Note bid-ask spread as a liquidity indicator.
2. **Price the Forward:** Call `fx_forward_price` at the target tenor. Compute annualized carry from forward points.
3. **Map Carry Curve:** Call `fx_forward_curve` (list then calculate). Compute annualized carry at each tenor. Identify the sweet-spot tenor with best risk-adjusted carry.
4. **Assess Vol Risk:** Call `fx_vol_surface`. Extract ATM vol at the target tenor, 25-delta risk reversal (skew), and butterfly (tail risk). Compute carry-to-vol ratio.
5. **Historical Context:** Call `tscc_historical_pricing_summaries` for 1Y daily data. Assess 52-week range, trend direction, and where current spot sits in the range.
6. **Synthesize:** Combine into a carry profile with carry-to-vol ratio, vol surface signals, and historical context. Recommend entry with position sizing guidance.

## Output Format

### Carry Profile
| Metric | 1M | 3M | 6M | 1Y |
|--------|-----|-----|-----|-----|
| Forward Points (pips) | ... | ... | ... | ... |
| Annualized Carry (%) | ... | ... | ... | ... |
| ATM Implied Vol (%) | ... | ... | ... | ... |
| Carry-to-Vol Ratio | ... | ... | ... | ... |
| 25d Risk Reversal | ... | ... | ... | ... |

### Vol Surface Summary
| Tenor | ATM Vol | 25d Put | 25d Call | RR | BF |
|-------|---------|---------|----------|-----|-----|
| 1M | ... | ... | ... | ... | ... |
| 3M | ... | ... | ... | ... | ... |
| 6M | ... | ... | ... | ... | ... |

### Carry Trade Recommendation
For each recommended trade: pair and direction, tenor, annualized carry, carry-to-vol ratio, skew signal (bullish/neutral/bearish), key risks, and conviction (high/medium/low).


---

## SKILL: lending

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/lending` (MIT)
- Cuándo usarla: Analyze lending products including mortgages, HELOCs, and personal loans with amortization and comparison tools. Use when the user asks about mortgage comparison, fixed vs ARM rates, loan qualification, amortization schedules, extra payments, or buying points. Also trigger when users mention 'monthly payment calculation', '15-year vs 30-year mortgage', 'PMI', 'APR vs interest rate', 'HELOC', 'home equity', 'should I buy down the rate', 'biweekly payments', or ask how much house they can afford.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/wealth-management/skills/lending/` (lending.py)

# Lending Analysis

## Core Concepts

### Fixed-Rate Mortgage
The interest rate and monthly payment remain constant for the life of the loan:

- **Advantages:** Predictable payments, protection against rising rates, simpler budgeting
- **Disadvantages:** Higher initial rate than ARM, no benefit if rates decline (must refinance)
- Most common terms: 30-year and 15-year fixed

### Adjustable-Rate Mortgage (ARM)
Rate is fixed for an initial period, then adjusts periodically based on an index plus a margin:

- **Notation:** 5/1 ARM = fixed for 5 years, adjusts annually thereafter; 7/1, 10/1 similarly
- **Fully indexed rate:** Index (e.g., SOFR, 1-year Treasury) + margin (e.g., 2.75%)
- **Rate caps** protect against extreme adjustments:
  - Initial adjustment cap (e.g., 2%): maximum first adjustment
  - Periodic cap (e.g., 2%): maximum change per adjustment period
  - Lifetime cap (e.g., 5%): maximum total increase over initial rate
- **When ARM may be appropriate:** Planning to sell or refinance before the fixed period ends, expecting rates to decline, or comfortable with rate variability

### Monthly Payment Calculation
The standard amortization formula for a fixed-rate loan:

- PMT = P × [r(1+r)^n] / [(1+r)^n - 1]
- Where: P = principal (loan amount), r = monthly interest rate (annual rate / 12), n = total number of payments (term in months)
- Each payment splits into interest (decreasing) and principal (increasing) components:
  - Interest portion: remaining balance × monthly rate
  - Principal portion: PMT - interest portion

### Total Interest Paid
- Total interest = (n × PMT) - P
- For a $400K, 30-year loan at 6.5%: PMT = $2,528, total payments = $910,178, total interest = $510,178

### Extra Payments
Additional principal payments reduce the outstanding balance, shorten the loan term, and reduce total interest:

- Each extra dollar goes entirely to principal reduction
- Impact compounds: earlier extra payments save more interest than later ones
- Methods: lump sum, fixed monthly extra, biweekly payments (26 half-payments = 13 full payments per year)

### Mortgage Points
Prepaid interest that reduces the loan's interest rate:

- **1 point = 1% of the loan amount** (e.g., 1 point on $400K = $4,000)
- Typically reduces the rate by approximately 0.25% (varies by lender and market)
- **Breakeven calculation:** Points cost / monthly savings = months to recoup
- Points make sense when: planning to hold the loan beyond breakeven, itemizing deductions (points may be tax-deductible in year of purchase)

### APR vs Interest Rate
- **Interest rate:** The cost of borrowing the principal, expressed annually
- **APR (Annual Percentage Rate):** Includes the interest rate plus certain fees and costs (origination fees, points, PMI), annualized over the loan term
- **APR > interest rate** (always, when there are fees)
- APR is the better metric for comparing loan offers with different fee structures

### HELOC (Home Equity Line of Credit)
A revolving credit line secured by home equity:

- **Combined LTV (CLTV):** (First mortgage balance + HELOC limit) / home value
  - Most lenders require CLTV ≤ 80-90%
- **Draw period** (typically 10 years): borrow and repay flexibly, often interest-only payments
- **Repayment period** (typically 20 years): no new draws, fully amortizing payments
- **Variable rate:** Typically prime rate + margin; rate fluctuates with market
- **Use cases:** Home improvements, debt consolidation, emergency backup (but not as primary emergency fund)
- **Risk:** Home is collateral — default means foreclosure

### Loan Qualification Criteria
- **FICO score:** 620+ for conventional, 580+ for FHA, 700+ for best rates
- **DTI:** Front-end ≤ 28%, back-end ≤ 36-43% (varies by program)
- **LTV (Loan-to-Value):** Loan amount / property value; lower LTV = lower risk = better terms
- **Reserves:** Months of payments held in liquid assets after closing (2-6 months typical)
- **Employment/income:** Stable income history, typically 2 years documentation

### PMI (Private Mortgage Insurance)
Required when conventional loan LTV exceeds 80%:

- **Cost:** 0.5-1.5% of loan amount annually, added to monthly payment
- **Removal:** Automatic at 78% LTV (based on original amortization), requestable at 80% LTV
- **Avoidance strategies:** 20% down payment, piggyback loan (80/10/10), lender-paid PMI (higher rate), VA loan (no PMI)
- PMI benefits the lender, not the borrower — it is pure cost to the borrower

### 15-Year vs 30-Year Comparison
- **15-year:** Higher monthly payment, lower interest rate (typically 0.5-0.75% less), dramatically less total interest, builds equity faster
- **30-year:** Lower required payment, more flexibility, higher total interest cost
- **Hybrid approach:** Take a 30-year for flexibility, make extra payments as if it were a 15-year

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Monthly payment | PMT = P × [r(1+r)^n] / [(1+r)^n - 1] | Fixed-rate loan payment |
| Total interest | n × PMT - P | Total cost of borrowing |
| Remaining balance after k payments | B_k = P × [(1+r)^n - (1+r)^k] / [(1+r)^n - 1] | Balance at any point |
| Points breakeven | Cost of points / monthly savings | Months to recoup points |
| LTV | Loan amount / property value | Risk and PMI assessment |
| CLTV | (First mortgage + HELOC) / home value | Combined leverage |
| ARM fully indexed rate | Index + margin | Rate after fixed period |

## Worked Examples

### Example 1: 30-year vs 15-year mortgage comparison
**Given:** Home price $500K, down payment $100K, loan amount $400K. 30-year rate: 6.5%. 15-year rate: 5.9%.
**Calculate:** Monthly payments, total interest, and interest savings.
**Solution:**
1. **30-year monthly payment:** PMT = $400,000 × [0.005417 × (1.005417)^360] / [(1.005417)^360 - 1]
   - r = 6.5%/12 = 0.005417, n = 360
   - PMT = **$2,528/month**
2. **30-year total interest:** 360 × $2,528 - $400,000 = **$510,178**
3. **15-year monthly payment:** PMT = $400,000 × [0.004917 × (1.004917)^180] / [(1.004917)^180 - 1]
   - r = 5.9%/12 = 0.004917, n = 180
   - PMT = **$3,354/month**
4. **15-year total interest:** 180 × $3,354 - $400,000 = **$203,694**
5. **Payment difference:** $3,354 - $2,528 = **$826/month more** for 15-year.
6. **Interest savings:** $510,178 - $203,694 = **$306,484 saved** by choosing 15-year.
7. The 15-year costs 33% more per month but saves 60% in total interest.

### Example 2: Extra payment impact
**Given:** $300K 30-year mortgage at 6.5% (payment = $1,896.20/month). Borrower adds $200/month extra to principal, making the total payment $2,096.20/month.
**Calculate:** Time saved and interest saved.
**Solution:**
1. **Without extra payments:** 360 months, total interest = 360 × $1,896.20 - $300,000 = **$382,633**.
2. **New term (closed-form estimate):** n = -ln(1 - P × r / PMT_total) / ln(1+r) with r = 0.065/12 = 0.005417:
   - n = -ln(1 - $300,000 × 0.005417 / $2,096.20) / ln(1.005417) ≈ 276.3 payments.
3. **Exact amortization** (month-by-month simulation, final payment partial): payoff in **277 months = 23 years 1 month** (~23.1 years), total interest = **$279,185**. The closed form and the exact schedule agree closely.
4. **Interest saved:** $382,633 - $279,185 = **$103,449**.
5. **Time saved:** 360 - 277 = 83 months ≈ **6.9 years**.
6. Total extra principal paid ≈ 276 × $200 = **$55,200**. Interest saved per dollar of extra payment: $103,449 / $55,200 ≈ **$1.87**.

## Common Pitfalls
- Comparing interest rate instead of APR — APR captures fees and gives a truer cost comparison
- ARM teaser rates creating payment shock when the fixed period ends and rates adjust upward
- Points breakeven: buying points is not worth it if selling or refinancing before the breakeven point
- HELOC variable rate risk during rising rate environments — budget for rate increases
- PMI costs making high-LTV loans more expensive than they appear — factor PMI into total monthly cost
- Ignoring opportunity cost: extra mortgage payments at 3-4% vs investing at 7-10% expected return
- Not shopping multiple lenders — rate quotes can vary 0.5%+ for the same borrower
- Resetting to a 30-year term when refinancing — extends total payoff even if rate is lower
- Ignoring closing costs in refinancing decisions (see debt-management refinance breakeven)

## Cross-References
- **debt-management** (wealth-management plugin): refinancing analysis, debt payoff vs investing decisions, DTI calculations
- **emergency-fund** (wealth-management plugin): adequate reserves required for loan qualification and financial safety
- **tax-efficiency** (wealth-management plugin): mortgage interest deductibility, points deduction
- **savings-goals** (wealth-management plugin): down payment saving is a common goal-based savings target
- **liquidity-management** (wealth-management plugin): mortgage payments are the largest fixed obligation in most household cash flow plans

## Running the script
Run the reference implementation directly:

```
uv run scripts/lending.py          # PEP 723 header resolves dependencies automatically
python3 scripts/lending.py         # after: pip install numpy scipy
```

A bare run prints a demo covering payment calculation, extra-payment impact, LTV/PMI, DSCR, balloon payments, refinance analysis, points breakeven, and ARM resets. Use `--verify` to recompute the demo figures and assert they match this skill's worked examples (prints PASS/FAIL, exits nonzero on mismatch), and `--help` to list the available classes and functions. The file is primarily meant to be imported as a module (`from lending import LendingAnalysis`) rather than run standalone.


---

## SKILL: payment-run-review

- Fuente: `SYasJ/claude-business-skills` → `plugins/banking/skills/payment-run-review` (MIT)
- Cuándo usarla: Review a payment run for duplicates, approvals, and changes to payee details. Use when the user mentions payment run, AP run review, pay cycle review, payment approval, or asks for a payment run review. Banking and treasury operations skill by Yasir Jilani.

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'payment-run-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Payment Run Review

Review a payment run for duplicates, approvals, and changes to payee details.

## When to use this skill

Use this skill when the user:

- payment run
- AP run review
- pay cycle review
- payment approval

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

This is not a credit decision and not an instruction to move money. Do not request online-banking passwords, one-time codes, or card PINs.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The run list
- Approval limits
- Changed payee details
- Exceptions

## Workflow


### 1. Step 1

Check the run against approvals they require.
### 2. Step 2

Flag duplicate-looking items for review, not as accusations.
### 3. Step 3

Any payee detail change needs their verified channel.
### 4. Step 4

Do not ask for banking passwords or one-time codes.
### 5. Step 5

Exceptions need a named approver.
### 6. Step 6

Recommend a hold on items that fail the check rather than a silent release.

## Output

Deliver a **payment run review**.

- Purpose of this payment run review, in two sentences.
- Facts the user supplied, listed separately from assumptions.
- The work itself, in the structure the workflow names.
- Open questions, risks, and the single next action with an owner.
- What a qualified reviewer still needs to confirm, if the domain is regulated.

## Quality bar

- Every number, date, name, and citation came from the user or is marked as an assumption.
- The artifact can be used without reading this skill again.
- Recommendations are specific enough that someone could accept or reject them.
- Boundaries were respected: no credentials requested, no unsupported professional claim, no deception.

## Example

### Scenario

Priya Shah, controller at Northline Studio in Calgary, needs a payment run review by 30 September 2026. A payment run includes a new account number received by email this morning.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A payment run includes a new account number received by email this morning.

The run list: Payment run 14 Sep; Account opening file 221; Liquidity ladder
Approval limits: Account opening file 221. Partly documented: the what is written down, the who is not
Changed payee details: requested 14 September 2026. Not yet approved
Exceptions: Payment run 14 Sep is open. Account opening file 221 was raised verbally and never logged
```

### Example outcome

**Payment run review**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Holds that item until the verified channel confirms it.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The run list | Payment run 14 Sep; Account opening file 221; Liquidity ladder | Needs confirmation |
| Approval limits | Account opening file 221. Partly documented: the what is written down, the who is not | Carried into the draft |
| Changed payee details | requested 14 September 2026. Not yet approved | Carried into the draft |
| Exceptions | Payment run 14 Sep is open. Account opening file 221 was raised verbally and never logged | Needs confirmation |

**How this draft was built**

**1. Check the run against approvals they require**

**2. Flag duplicate-looking items for review, not as accusations**

**3. Any payee detail change needs their verified channel**

**4. Do not ask for banking passwords or one-time codes**

**5. Exceptions need a named approver**

**Deliberately not done**
- A password request.
- A silent release of a failed item.
- An unverified bank-detail change.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A password request
- A silent release of a failed item
- An unverified bank-detail change

## Related skills

- `accounts-payable-control`
- `treasury-policy-brief`


---

## SKILL: treasury-policy-brief

- Fuente: `SYasJ/claude-business-skills` → `plugins/finance/skills/treasury-policy-brief` (MIT)
- Cuándo usarla: Draft the questions and structure of a simple cash and risk policy for a small finance team. Use when the user mentions treasury policy, cash policy, who can move money, investment of surplus cash, or asks for a treasury policy brief. Finance skill by Yasir Jilani.

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'treasury-policy-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Treasury Policy Brief

Draft the questions and structure of a simple cash and risk policy for a small finance team.

## When to use this skill

Use this skill when the user:

- treasury policy
- cash policy
- who can move money
- investment of surplus cash

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

This is not investment, tax, or financial advice. Do not invent rates of return, tax rates, or valuation multiples. A qualified finance professional must review any decision that moves money.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Entities and bank relationships the user mentioned
- Who may approve payments today
- Surplus cash, if any
- Risks they have already hit

## Workflow


### 1. Write the purpose

Safeguard cash, pay on time, and avoid surprises. Do not turn a small company policy into a bank manual.
### 2. Approval matrix

Recommend they document who can approve which payment size. Use their current practice as the starting point and flag gaps.
### 3. Account rules

Which accounts exist and why, in their description. Suggest fewer accounts if they described confusion, and explain why.
### 4. Surplus cash

If they park cash, list policy questions: access, credit quality, and who decides. Do not recommend a product or a yield.
### 5. Exceptions

How an emergency payment is approved and recorded the next day.
### 6. Do not ask for logins

Policy work does not need passwords, tokens, or card numbers.

## Output

Deliver a **treasury policy brief**.

- Purpose of this treasury policy brief, in two sentences.
- Facts the user supplied, listed separately from assumptions.
- The work itself, in the structure the workflow names.
- Open questions, risks, and the single next action with an owner.
- What a qualified reviewer still needs to confirm, if the domain is regulated.

## Quality bar

- Every number, date, name, and citation came from the user or is marked as an assumption.
- The artifact can be used without reading this skill again.
- Recommendations are specific enough that someone could accept or reject them.
- Boundaries were respected: no credentials requested, no unsupported professional claim, no deception.

## Example

### Scenario

Mara Chen, founder at Northline Studio in Calgary, needs a treasury policy brief by 30 September 2026. A controller wants a one-page cash policy after a duplicate payment slipped through.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A controller wants a one-page cash policy after a duplicate payment slipped through.

Entities and bank relationships the user mentioned: Harbor & Co receipt. Stated in the ask, not documented anywhere else
Who may approve payments today: Mara Chen, founder
Surplus cash, if any: Operating cash, recorded 14 September 2026. No supporting file attached
Risks they have already hit: Operating cash is open. No score in the file
```

### Example outcome

**Treasury policy brief**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A policy brief with an approval matrix, an exception path, and no request for credentials or product pitches.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Entities and bank relationships the user mentioned | Harbor & Co receipt. Stated in the ask, not documented anywhere else | Needs confirmation |
| Who may approve payments today | Mara Chen, founder | Carried into the draft |
| Surplus cash, if any | Operating cash, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Risks they have already hit | Operating cash is open. No score in the file | Needs confirmation |

**How this draft was built**

**1. Write the purpose**  
Safeguard cash, pay on time, and avoid surprises. Do not turn a small company policy into a bank manual.

**2. Approval matrix**  
Recommend they document who can approve which payment size. Use their current practice as the starting point and flag gaps.

**3. Account rules**  
Which accounts exist and why, in their description. Suggest fewer accounts if they described confusion, and explain why.

**4. Surplus cash**  
If they park cash, list policy questions: access, credit quality, and who decides. Do not recommend a product or a yield.

**5. Exceptions**  
How an emergency payment is approved and recorded the next day.

**Deliberately not done**
- A hedge fund investment policy for a company with one operating account.
- Requesting banking credentials to 'set up the policy'.
- Promising a return on surplus cash.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A hedge fund investment policy for a company with one operating account.
- Requesting banking credentials to 'set up the policy'.
- Promising a return on surplus cash.

## Related skills

- `fx-exposure-review`
- `internal-controls-walkthrough`
- `cash-flow-forecast`
