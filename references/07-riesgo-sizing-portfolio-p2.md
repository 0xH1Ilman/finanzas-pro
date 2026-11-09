# 07-riesgo-sizing-portfolio — parte 2

Skills de terceros agrupadas por tema. Cada sección indica fuente, licencia y dónde está su código.



---

## SKILL: portfolio-manager

- Fuente: `tradermonty/claude-trading-skills` → `skills/portfolio-manager` (MIT)
- Cuándo usarla: Comprehensive portfolio analysis using Alpaca MCP Server integration to fetch holdings and positions, then analyze asset allocation, risk metrics, individual stock positions, diversification, and generate rebalancing recommendations. Use when user requests portfolio review, position analysis, risk assessment, performance evaluation, or rebalancing suggestions for their brokerage account.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/portfolio-manager/` (fictional_holdings.csv, requirements.txt, check_alpaca_connection.py, reconcile_positions.py, review_csv.py)

# Portfolio Manager

## Overview

Analyze and manage investment portfolios by integrating with Alpaca MCP Server to fetch real-time holdings data, then performing comprehensive analysis covering asset allocation, diversification, risk metrics, individual position evaluation, and rebalancing recommendations. Generate detailed portfolio reports with actionable insights.

The full brokerage analysis uses Alpaca's API through MCP for live portfolio data. A separate limited CSV allocation review is available offline; it does not provide the full brokerage analysis or workflow.

## When to Use

Invoke this skill when the user requests:
- "Analyze my portfolio"
- "Review my current positions"
- "What's my asset allocation?"
- "Check my portfolio risk"
- "Should I rebalance my portfolio?"
- "Evaluate my holdings"
- "Portfolio performance review"
- "What stocks should I buy or sell?"
- Any request involving portfolio-level analysis or management

## Prerequisites

### Limited Offline CSV Review

For a local USD equity holdings snapshot without credentials, read
`references/csv-holdings-review.md` and run `scripts/review_csv.py` with an explicit
source timestamp. Use the bundled fictional CSV to verify offline execution.
This produces gross allocation and per-position unrealized P&L only; it cannot
measure account exposure, leverage or historical performance. Keep personal
holdings and reports local. Do not fetch brokerage data or continue the full
workflow for this limited mode. Navigator/workflow integration remains unshipped.

### Alpaca MCP Server Setup (Full Brokerage Analysis)

The full brokerage analysis requires Alpaca MCP Server to be configured and connected. The MCP server provides access to:
- Current portfolio positions
- Account equity and buying power
- Historical positions and transactions
- Market data for held securities

**MCP Server Tools Used:**
- `get_account_info` - Fetch account equity, buying power, cash balance
- `get_positions` - Retrieve all current positions with quantities, cost basis, market value
- `get_portfolio_history` - Historical portfolio performance data
- Market data tools for price quotes and fundamentals

If Alpaca MCP Server is not connected, inform the user and provide setup instructions from `references/alpaca-mcp-setup.md`.

### REST Fallback Connection Check

Run the connection check from the repository root. Use paper credentials first;
never paste credentials into a report or commit them to the repository.

```bash
export ALPACA_API_KEY="<alpaca-key-id>"
export ALPACA_SECRET_KEY="<alpaca-secret-key>"
export ALPACA_PAPER="true"
uv run python skills/portfolio-manager/scripts/check_alpaca_connection.py
```

The command writes a redacted diagnostic summary to stdout and returns zero only
when the account and positions endpoints succeed. It does not create a report
file or place orders.

## Workflow

### Step 1: Fetch Portfolio Data via Alpaca MCP or REST fallback

Use Alpaca MCP Server tools to gather current portfolio information when available. In scheduled Hermes jobs, MCP tools may not be exposed even when Alpaca credentials are present; in that case, use the Alpaca REST API directly with `ALPACA_API_KEY`, `ALPACA_SECRET_KEY`, and `ALPACA_PAPER`.

**1.1 Get Account Information:**
```
Preferred: use mcp__alpaca__get_account_info to fetch:
- Account equity (total portfolio value)
- Cash balance
- Buying power
- Account status

Fallback REST endpoints:
- paper: https://paper-api.alpaca.markets/v2/account
- live:  https://api.alpaca.markets/v2/account
Headers:
- APCA-API-KEY-ID=$ALPACA_API_KEY
- APCA-API-SECRET-KEY=$ALPACA_SECRET_KEY
```

**1.2 Get Current Positions:**
```
Preferred: use mcp__alpaca__get_positions to fetch all holdings:
- Symbol ticker
- Quantity held
- Average entry price (cost basis)
- Current market price
- Current market value
- Unrealized P&L ($ and %)
- Position size as % of portfolio

Fallback REST endpoints:
- paper: https://paper-api.alpaca.markets/v2/positions
- live:  https://api.alpaca.markets/v2/positions
```

**1.3 Get Portfolio History (Optional):**
```
Preferred: use mcp__alpaca__get_portfolio_history for performance analysis:
- Historical equity values
- Time-weighted return calculation
- Drawdown analysis

Fallback REST endpoint:
- /v2/account/portfolio/history
```

**Scheduled-job fallback discipline:**
- Clearly label the source as `Alpaca REST fallback` rather than MCP.
- Use `ALPACA_PAPER=true` to choose paper endpoint; otherwise use live endpoint.
- Still validate that long market value plus cash approximately reconciles to equity, and highlight margin/leverage if `long_market_value > equity`.
- For weekly core portfolio cron jobs, compute exposure using equity as the denominator as well as gross market value: `gross_long_exposure = long_market_value / equity`, `cash_pct = cash / equity`, and explicitly flag margin-funded portfolios when gross exposure is materially above 100% or cash is negative. Do not let sector weights look benign by using only gross-long denominator when the account is levered.
- When the request emphasizes dividend holdings or forced-review triggers, build normalized monitor input from the live holdings and hand it to `kanchi-dividend-review-monitor` rather than treating dividend review as a narrative-only section. Also build tax-planning input for `kanchi-dividend-us-tax-accounting` when account-location notes are requested; label it degraded if account type or holding-period windows are unavailable.

**Data Validation:**
- Verify all positions have valid ticker symbols
- Confirm market values sum to approximate account equity
- Check for any stale or inactive positions
- Handle edge cases (fractional shares, options, crypto if supported)

### Reconcile holdings before weekly allocation review

For `core-portfolio-weekly`, follow
[`references/position-reconciliation.md`](references/position-reconciliation.md)
to compare complete broker and ACTIVE / PARTIALLY_CLOSED memory snapshots using
`scripts/reconcile_positions.py`. Generate the JSON and Markdown reconciliation
reports. Stop allocation and rebalance review if `can_continue` is false or if
snapshot completeness, account attribution or freshness cannot be established.
Keep discrepancies for manual resolution; never place orders or modify theses
through reconciliation. This is an offline, manually prepared gate; existing
weekly replay fixtures do not yet execute it.

### Step 2: Enrich Position Data

For each position in the portfolio, gather additional market data and fundamentals:

**2.1 Current Market Data:**
- Real-time or delayed price quotes
- Daily volume and liquidity metrics
- 52-week range
- Market capitalization

**2.2 Fundamental Data:**
Use WebSearch or available market data APIs to fetch:
- Sector and industry classification
- Key valuation metrics (P/E, P/B, dividend yield)
- Recent earnings and financial health indicators
- Analyst ratings and price targets
- Recent news and material developments

**2.3 Technical Analysis:**
- Price trend (20-day, 50-day, 200-day moving averages)
- Relative strength
- Support and resistance levels
- Momentum indicators (RSI, MACD if available)

### Step 3: Portfolio-Level Analysis

Perform comprehensive portfolio analysis using frameworks from reference files:

#### 3.1 Asset Allocation Analysis

**Read references/asset-allocation.md** for allocation frameworks

Analyze current allocation across multiple dimensions:

**By Asset Class:**
- Equities vs Fixed Income vs Cash vs Alternatives
- Compare to target allocation for user's risk profile
- Assess if allocation matches investment goals

**By Sector:**
- Technology, Healthcare, Financials, Consumer, etc.
- Identify sector concentration risks
- Compare to benchmark sector weights (e.g., S&P 500)

**By Market Cap:**
- Large-cap vs Mid-cap vs Small-cap distribution
- Concentration in mega-caps
- Market cap diversification score

**By Geography:**
- US vs International vs Emerging Markets
- Domestic concentration risk assessment

**Output Format (illustrative values):**
```markdown
## Asset Allocation

### Current Allocation vs Target
| Asset Class | Current | Target | Variance |
|-------------|---------|--------|----------|
| US Equities | 70.0% | 60.0% | +10.0 pp |

### Sector Breakdown
[Pie chart description or table with sector percentages]

### Top 10 Holdings
| Rank | Symbol | % of Portfolio | Sector |
|------|--------|----------------|--------|
| 1 | AAPL | 8.5% | Technology |
```

#### 3.2 Diversification Analysis

**Read references/diversification-principles.md** for diversification theory

Evaluate portfolio diversification quality:

**Position Concentration:**
- Identify top holdings and their aggregate weight
- Flag if any single position exceeds 10-15% of portfolio
- Calculate Herfindahl-Hirschman Index (HHI) for concentration measurement

**Sector Concentration:**
- Identify dominant sectors
- Flag if any sector exceeds 30-40% of portfolio
- Compare to benchmark sector diversity

**Correlation Analysis:**
- Estimate correlation between major positions
- Identify highly correlated holdings (potential redundancy)
- Assess true diversification benefit

**Number of Positions:**
- Optimal range: 15-30 stocks for individual portfolios
- Flag if under-diversified (<10 stocks) or over-diversified (>50 stocks)

**Output (illustrative values):**
```markdown
## Diversification Assessment

**Concentration Risk:** [Low / Medium / High]
- Top 5 holdings represent 42% of portfolio
- Largest single position: AAPL at 12%

**Sector Diversification:** [Excellent / Good / Fair / Poor]
- Dominant sector: Technology at 31%
- [Assessment of balance across sectors]

**Position Count:** [Optimal / Under-diversified / Over-diversified]
- Total positions: 18 stocks
- [Recommendation]

**Correlation Concerns:**
- [List any highly correlated position pairs]
- [Diversification improvement suggestions]
```

#### 3.3 Risk Analysis

**Read references/portfolio-risk-metrics.md** for risk measurement frameworks

Calculate and interpret key risk metrics:

**Volatility Measures:**
- Estimated portfolio beta (weighted average of position betas)
- Individual position volatilities
- Portfolio standard deviation (if historical data available)

**Downside Risk:**
- Maximum drawdown (from portfolio history)
- Current drawdown from peak
- Positions with significant unrealized losses

**Risk Concentration:**
- Percentage in high-volatility stocks (beta > 1.5)
- Percentage in speculative/unprofitable companies
- Leverage usage (if applicable)

**Tail Risk:**
- Exposure to potential black swan events
- Single-stock concentration risk
- Sector-specific event risk

**Output (illustrative values):**
```markdown
## Risk Assessment

**Overall Risk Profile:** [Conservative / Moderate / Aggressive]

**Portfolio Beta:** 1.12 (vs market at 1.00)
- Interpretation: Portfolio is [more/less] volatile than market

**Maximum Drawdown:** -14.2% (from $125,000 to $107,250)
- Current drawdown from peak: -6.3%

**High-Risk Positions:**
| Symbol | % of Portfolio | Beta | Risk Factor |
|--------|----------------|------|-------------|
| NVDA | 11% | 1.65 | High volatility |

**Risk Concentrations:**
- 31% in a single sector (Technology)
- 18% in stocks with beta above 1.5
- [Other concentration risks]

**Risk Score:** 68/100 (Medium risk)
```

#### 3.4 Performance Analysis

Evaluate portfolio performance using available data:

**Absolute Returns:**
- Overall portfolio unrealized P&L ($ and %)
- Best performing positions (top 5 by % gain)
- Worst performing positions (bottom 5 by % loss)

**Time-Weighted Returns (if history available):**
- YTD return
- 1-year, 3-year, 5-year annualized returns
- Compare to benchmark (S&P 500, relevant index)

**Position-Level Performance:**
- Winners vs Losers ratio
- Average gain on winning positions
- Average loss on losing positions
- Positions near 52-week highs/lows

**Output (illustrative values):**
```markdown
## Performance Review

**Total Portfolio Value:** $100,000
**Total Unrealized P&L:** $8,500 (+9.3%)
**Cash Balance:** $5,000 (5% of portfolio)

**Best Performers:**
| Symbol | Gain | Position Value |
|--------|------|----------------|
| AAPL | +22.4% | $12,240 |

**Worst Performers:**
| Symbol | Loss | Position Value |
|--------|------|----------------|
| INTC | -12.0% | $6,600 |

**Performance vs Benchmark (illustrative values):**
- Portfolio return: +9.3%
- S&P 500 return: +7.8%
- Alpha: +1.5 percentage points
```

### Step 4: Individual Position Analysis

For key positions (top 10-15 by portfolio weight), perform detailed analysis:

**Read references/position-evaluation.md** for position analysis framework

For each significant position:

**4.1 Current Thesis Validation:**
- Why was this position initiated? (if known from user context)
- Has the investment thesis played out or broken?
- Recent company developments and news

**4.2 Valuation Assessment:**
- Current valuation metrics (P/E, P/B, etc.)
- Compare to historical valuation range
- Compare to sector peers
- Overvalued / Fair / Undervalued assessment

**4.3 Technical Health:**
- Price trend (uptrend, downtrend, sideways)
- Position relative to moving averages
- Support and resistance levels
- Momentum status

**4.4 Position Sizing:**
- Current weight in portfolio
- Is size appropriate given conviction and risk?
- Overweight or underweight vs optimal

**4.5 Action Recommendation:**
- **HOLD** - Position is well-sized and thesis intact
- **ADD** - Underweight given opportunity, thesis strengthening
- **TRIM** - Overweight or valuation stretched
- **SELL** - Thesis broken, better opportunities elsewhere

**Output per position (illustrative values):**
```markdown
### AAPL - Apple Inc. (8.5% of portfolio)

**Position Details:**
- Shares: 50
- Avg Cost: $150.00
- Current Price: $170.00
- Market Value: $8,500
- Unrealized P/L: $1,000 (+13.3%)

**Fundamental Snapshot:**
- Sector: [Sector]
- Market Cap: $3.2T
- P/E: 31.4 | Dividend Yield: 0.5%
- Recent developments: [Key news or earnings]

**Technical Status:**
- Trend: [Uptrend / Downtrend / Sideways]
- Price vs 50-day MA: Above by 4.2%
- Support: $162.00 | Resistance: $176.00

**Position Assessment:**
- **Thesis Status:** [Intact / Weakening / Broken / Strengthening]
- **Valuation:** [Undervalued / Fair / Overvalued]
- **Position Sizing:** [Optimal / Overweight / Underweight]

**Recommendation:** [HOLD / ADD / TRIM / SELL]
**Rationale:** [1-2 sentence explanation]
```

### Step 5: Rebalancing Recommendations

**Read references/rebalancing-strategies.md** for rebalancing approaches

Generate specific rebalancing recommendations:

**5.1 Identify Rebalancing Triggers:**
- Positions that have drifted significantly from target weights
- Sector/asset class allocations requiring adjustment
- Overweight positions to trim (exceeded threshold)
- Underweight areas to add (below threshold)
- Tax considerations (capital gains implications)

**5.2 Develop Rebalancing Plan:**

**Positions to TRIM:**
- Overweight positions (>threshold deviation from target)
- Stocks that have run up significantly (valuation concerns)
- Concentrated positions exceeding 15-20% of portfolio
- Positions with broken thesis

**Positions to ADD:**
- Underweight sectors or asset classes
- High-conviction positions currently underweight
- New opportunities to improve diversification

**Cash Deployment:**
- If excess cash (>10% of portfolio), suggest deployment
- Prioritize based on opportunity and allocation gaps

**5.3 Prioritization:**
Rank rebalancing actions by priority:
1. **Immediate** - Risk reduction (trim concentrated positions)
2. **High Priority** - Major allocation drift (>10% from target)
3. **Medium Priority** - Moderate drift (5-10% from target)
4. **Low Priority** - Fine-tuning and opportunistic adjustments

**Output (illustrative values):**
```markdown
## Rebalancing Recommendations

### Summary
- **Rebalancing Needed:** [Yes / No / Optional]
- **Primary Reason:** [Concentration risk / Sector drift / Cash deployment / etc]
- **Estimated Trades:** 2 sell orders, 3 buy orders

### Recommended Actions

#### HIGH PRIORITY: Risk Reduction
**TRIM NVDA** from 18% to 12% of portfolio
- **Shares to Sell:** 25 shares (about $3,000)
- **Rationale:** [Overweight / Valuation extended / etc]
- **Tax Impact:** $600 capital gain (estimate)

#### MEDIUM PRIORITY: Asset Allocation
**ADD investment-grade bond exposure**
- **Target:** Increase from 10% to 20%
- **Suggested Securities:** [Select liquid securities that fit the user's mandate]
- **Amount to Invest:** About $10,000

#### CASH DEPLOYMENT
**Current Cash:** $5,000 (5% of portfolio)
- **Recommendation:** [Deploy / Keep for opportunities / Reduce to target]
- **Suggested Allocation:** [Distribution across sectors/stocks]

### Implementation Plan
1. [First action - highest priority]
2. [Second action]
3. [Third action]
...

**Timing Considerations:**
- [Tax year-end planning / Earnings season / Market conditions]
- [Suggested phasing if applicable]
```

### Step 6: Generate Portfolio Report

Create comprehensive markdown report saved to repository root:

**Filename:** `portfolio_analysis_YYYY-MM-DD.md`

**Report Structure:**

```markdown
# Portfolio Analysis Report

**Account:** [Account type if available]
**Report Date:** 2026-07-25
**Portfolio Value:** $100,000
**Total P&L:** $8,500 (+9.3%)

---

## Executive Summary

[3-5 bullet points summarizing key findings]
- Overall portfolio health assessment
- Major strengths
- Key risks or concerns
- Primary recommendations

---

## Holdings Overview

[Summary table of all positions]

---

## Asset Allocation
[Section from Step 3.1]

---

## Diversification Analysis
[Section from Step 3.2]

---

## Risk Assessment
[Section from Step 3.3]

---

## Performance Review
[Section from Step 3.4]

---

## Position Analysis
[Detailed analysis of top 10-15 positions from Step 4]

---

## Rebalancing Recommendations
[Section from Step 5]

---

## Action Items

**Immediate Actions:**
- [ ] [Action 1]
- [ ] [Action 2]

**Medium-Term Actions:**
- [ ] [Action 3]
- [ ] [Action 4]

**Monitoring Priorities:**
- [ ] [Watch list item 1]
- [ ] [Watch list item 2]

---

## Appendix: Full Holdings

[Complete table with all positions and metrics]
```

### Step 7: Interactive Follow-up

Be prepared to answer follow-up questions:

**Common Questions:**

**"Why should I sell [SYMBOL]?"**
- Explain specific concerns (valuation, thesis breakdown, concentration)
- Provide supporting data
- Offer alternative positions if applicable

**"What should I buy instead?"**
- Suggest specific stocks to improve allocation
- Explain how they address portfolio gaps
- Provide brief investment thesis

**"What's my biggest risk?"**
- Identify primary risk factor (concentration, sector exposure, volatility)
- Quantify the risk
- Suggest mitigation strategies

**"How does my portfolio compare to [benchmark]?"**
- Compare allocation, sector weights, risk metrics
- Highlight key differences
- Assess if differences are justified

**"Should I rebalance now or wait?"**
- Consider market conditions, tax implications, transaction costs
- Provide timing recommendation with rationale

**"Can you analyze [specific position] in more detail?"**
- Perform deep-dive analysis using us-stock-analysis skill if needed
- Integrate findings back into portfolio context

## Analysis Frameworks

### Target Allocation Templates

This skill includes reference allocation models for different investor profiles:

**Read references/target-allocations.md** for detailed models:

- **Conservative** (Capital preservation, income focus)
- **Moderate** (Balanced growth and income)
- **Growth** (Long-term capital appreciation)
- **Aggressive** (Maximum growth, high risk tolerance)

Each model includes:
- Asset class targets (Stocks/Bonds/Cash/Alternatives)
- Sector guidelines
- Market cap distribution
- Geographic allocation
- Position sizing rules

Use these as comparison benchmarks when user hasn't specified their allocation strategy.

### Risk Profile Assessment

If user's target allocation is unknown, assess appropriate risk profile based on:
- Age (if mentioned)
- Investment timeline (if mentioned)
- Current allocation (reveals preferences)
- Position types (conservative vs speculative stocks)

**Read references/risk-profile-questionnaire.md** for assessment framework

## Output Guidelines

**Tone and Style:**
- Objective and analytical
- Actionable recommendations with clear rationale
- Acknowledge uncertainty in market forecasts
- Balance optimism with risk awareness
- Quantify whenever possible

**Data Presentation:**
- Tables for comparisons and metrics
- Percentages for allocations and returns
- Dollar amounts for absolute values
- Consistent formatting throughout report

**Recommendation Clarity:**
- Explicit action verbs (TRIM, ADD, HOLD, SELL)
- Specific quantities derived from live position sizes and current prices
- Priority levels (Immediate, High, Medium, Low)
- Supporting rationale for each recommendation

**Visual Descriptions:**
- Describe allocation breakdowns as if creating pie charts
- Sector weights as bar chart equivalents
- Performance trends with directional indicators (↑ ↓ →)

## Resources

Load these references as needed during analysis:

**references/alpaca-mcp-setup.md**
- When: User needs help setting up Alpaca MCP Server
- Contains: Installation instructions, API key configuration, MCP server connection steps, troubleshooting

**references/asset-allocation.md**
- When: Analyzing portfolio allocation or creating rebalancing plan
- Contains: Asset allocation theory, optimal allocation by risk profile, sector allocation guidelines, rebalancing triggers

**references/diversification-principles.md**
- When: Assessing portfolio diversification quality
- Contains: Modern portfolio theory basics, correlation concepts, optimal position count, concentration risk thresholds, diversification metrics

**references/portfolio-risk-metrics.md**
- When: Calculating risk scores or interpreting volatility
- Contains: Beta calculation, standard deviation, Sharpe ratio, maximum drawdown, Value at Risk (VaR), risk-adjusted return metrics

**references/position-evaluation.md**
- When: Analyzing individual holdings for buy/hold/sell decisions
- Contains: Position analysis framework, thesis validation checklist, position sizing guidelines, sell discipline criteria

**references/rebalancing-strategies.md**
- When: Developing rebalancing recommendations
- Contains: Rebalancing methodologies (calendar-based, threshold-based, tactical), tax optimization strategies, transaction cost considerations, implementation timing

**references/target-allocations.md**
- When: Need benchmark allocations for comparison
- Contains: Model portfolios for conservative/moderate/growth/aggressive investors, sector target ranges, market cap distributions

**references/risk-profile-questionnaire.md**
- When: User hasn't specified risk tolerance or target allocation
- Contains: Risk assessment questions, scoring methodology, risk profile classification

## Error Handling

**If Alpaca MCP Server is not connected:**
1. Inform user that Alpaca integration is required
2. Provide setup instructions from references/alpaca-mcp-setup.md
3. Offer alternative: manual data entry (less ideal, user provides CSV of positions)

**If API returns incomplete data:**
- Proceed with available data
- Note limitations in report
- Suggest manual verification for missing positions

**If position data seems stale:**
- Flag the issue
- Recommend refreshing connection or checking Alpaca status
- Proceed with analysis but caveat findings

**If user has no positions:**
- Acknowledge empty portfolio
- Offer portfolio construction guidance instead of analysis
- Suggest using value-dividend-screener or us-stock-analysis for stock ideas

## Advanced Features

### Tax-Loss Harvesting Opportunities

Identify positions with unrealized losses suitable for tax-loss harvesting:
- Positions with losses >5%
- Holding period considerations (avoid wash sale rule)
- Replacement security suggestions (similar but not substantially identical)

### Dividend Income Analysis

For portfolios with dividend-paying stocks:
- Estimate annual dividend income
- Dividend growth rate trajectory
- Dividend coverage and sustainability
- Yield on cost for long-term holdings

### Correlation Matrix

For portfolios with 5-20 positions:
- Estimate correlation between major positions
- Identify redundant positions (correlation >0.8)
- Suggest diversification improvements

### Scenario Analysis

Model portfolio behavior under different scenarios:
- **Bull Market** (+20% equity appreciation)
- **Bear Market** (-20% equity decline)
- **Sector Rotation** (Tech weakness, Value strength)
- **Rising Rates** (Impact on growth stocks and bonds)

## Example Queries

**Basic Portfolio Review:**
- "Analyze my portfolio"
- "Review my positions"
- "How's my portfolio doing?"

**Allocation Analysis:**
- "What's my asset allocation?"
- "Am I too concentrated in tech?"
- "Show me my sector breakdown"

**Risk Assessment:**
- "Is my portfolio too risky?"
- "What's my portfolio beta?"
- "What are my biggest risks?"

**Rebalancing:**
- "Should I rebalance?"
- "What should I buy or sell?"
- "How can I improve diversification?"

**Performance:**
- "What are my best and worst positions?"
- "How am I performing vs the market?"
- "Which stocks are winning and losing?"

**Position-Specific:**
- "Should I sell [SYMBOL]?"
- "Is [SYMBOL] overweight in my portfolio?"
- "What should I do with [SYMBOL]?"

## Limitations and Disclaimers

**Include in all reports:**

*This analysis is for informational purposes only and does not constitute financial advice. Investment decisions should be made based on individual circumstances, risk tolerance, and financial goals. Past performance does not guarantee future results. Consult with a qualified financial advisor before making investment decisions.*

*Data accuracy depends on Alpaca API and third-party market data sources. Verify critical information independently. Tax implications are estimates only; consult a tax professional for specific guidance.*

### Referencia: README.md

# Portfolio Manager

Comprehensive portfolio analysis and management skill that integrates with Alpaca MCP Server to fetch real-time holdings data and generate detailed portfolio reports with rebalancing recommendations.

## Overview

Portfolio Manager analyzes your investment portfolio across multiple dimensions:

- **Asset Allocation** - Stocks, bonds, cash distribution vs target allocation
- **Diversification** - Sector breakdown, position concentration, correlation analysis
- **Risk Assessment** - Portfolio beta, volatility, maximum drawdown, risk score
- **Performance Review** - Winners/losers, absolute and relative returns, benchmarking
- **Position Analysis** - Detailed evaluation of individual holdings (HOLD/ADD/TRIM/SELL recommendations)
- **Rebalancing Plan** - Specific actions to optimize portfolio allocation

## Features

✅ **Alpaca Integration** - Automatically fetches positions via Alpaca MCP Server
✅ **Multi-Dimensional Analysis** - Asset class, sector, geography, market cap, style
✅ **Risk Metrics** - Beta, volatility, drawdown, concentration, HHI
✅ **Position Evaluation** - Thesis validation, valuation, sizing, relative opportunity
✅ **Rebalancing Recommendations** - Prioritized actions (TRIM/ADD/HOLD/SELL)
✅ **Comprehensive Reports** - Markdown reports saved to repository
✅ **Model Portfolios** - Compare to Conservative/Moderate/Growth/Aggressive benchmarks

## Prerequisites

### Required: Alpaca Account and MCP Server

This skill requires:

1. **Alpaca Brokerage Account** (paper or live)
   - Sign up: https://alpaca.markets/
   - Paper trading account (free, simulated money) recommended for testing

2. **Alpaca MCP Server** configured in Claude
   - Provides access to portfolio positions via MCP tools
   - Setup guide: `references/alpaca-mcp-setup.md`

3. **API Credentials** (API Key ID and Secret Key)
   - Generate in Alpaca dashboard
   - Set environment variables:
     ```bash
     export ALPACA_API_KEY="your_api_key_id"
     export ALPACA_SECRET_KEY="your_secret_key"
     export ALPACA_PAPER="true"  # or "false" for live trading
     ```

### Optional: Manual Data Entry

If Alpaca MCP Server is unavailable, you can provide portfolio data manually via CSV:

```csv
symbol,quantity,cost_basis,current_price
AAPL,100,150.00,175.50
MSFT,50,280.00,310.25
```

## Installation

### For Claude Desktop/Code Users

1. **Copy skill to Claude Skills directory:**
   ```bash
   cp -r portfolio-manager ~/.claude/skills/
   ```

2. **Restart Claude** to detect the skill

3. **Configure Alpaca credentials** (see Prerequisites)

### For Claude Web App Users

1. **Download skill package:**
   - `skill-packages/portfolio-manager.skill`

2. **Upload to Claude:**
   - Click "+" in Claude web interface
   - Select "Upload Skill"
   - Choose `portfolio-manager.skill`

3. **Note:** Alpaca MCP Server may not be available in web version; use manual CSV data entry

## Usage

### Basic Portfolio Analysis

Simply ask Claude to analyze your portfolio:

```
"Analyze my portfolio"
"Review my current positions"
"How's my portfolio doing?"
```

The skill will:
1. Fetch positions from Alpaca via MCP
2. Enrich data with market information
3. Perform comprehensive analysis
4. Generate detailed report
5. Provide rebalancing recommendations

### Specific Analysis Types

**Asset Allocation Check:**
```
"What's my current asset allocation?"
"Am I properly diversified?"
```

**Risk Assessment:**
```
"How risky is my portfolio?"
"What's my portfolio beta?"
"What are my biggest risks?"
```

**Rebalancing:**
```
"Should I rebalance my portfolio?"
"What should I buy or sell?"
"Is anything too concentrated?"
```

**Position Review:**
```
"Should I sell Tesla?"
"Is Apple overweight in my portfolio?"
"What should I do with my tech stocks?"
```

**Performance:**
```
"What are my best performing stocks?"
"Which positions are losing money?"
"How am I doing vs the S&P 500?"
```

## Analysis Output

Portfolio Manager generates a comprehensive markdown report including:

### 1. Executive Summary
- Overall portfolio health
- Key strengths and concerns
- Primary recommendations

### 2. Holdings Overview
- All positions with quantities, values, P/L

### 3. Asset Allocation Analysis
- Current vs target allocation
- Sector breakdown
- Geographic distribution
- Market cap distribution

### 4. Diversification Assessment
- Position concentration analysis
- Sector diversification score
- Correlation concerns
- HHI concentration index

### 5. Risk Assessment
- Portfolio beta and volatility
- Maximum drawdown
- Risk concentrations
- Overall risk score

### 6. Performance Review
- Total portfolio value and P/L
- Best and worst performers
- Performance vs benchmark (if available)

### 7. Position Analysis
- Detailed analysis of top 10-15 holdings
- Thesis validation
- Valuation assessment
- Position sizing
- HOLD/ADD/TRIM/SELL recommendations

### 8. Rebalancing Recommendations
- Prioritized actions (High/Medium/Low priority)
- Specific trade recommendations
- Cash deployment suggestions
- Tax considerations

### 9. Action Items
- Immediate actions
- Medium-term tasks
- Monitoring priorities

**Report Location:** `portfolio_analysis_YYYY-MM-DD.md` in repository root

## Reference Materials

The skill includes comprehensive reference documentation:

- **`references/alpaca-mcp-setup.md`** - Alpaca API setup guide
- **`references/asset-allocation.md`** - Asset allocation theory and frameworks
- **`references/diversification-principles.md`** - Diversification concepts and metrics
- **`references/portfolio-risk-metrics.md`** - Risk measurement and interpretation
- **`references/position-evaluation.md`** - Position analysis framework
- **`references/rebalancing-strategies.md`** - Rebalancing methodologies
- **`references/target-allocations.md`** - Model portfolios by risk profile
- **`references/risk-profile-questionnaire.md`** - Risk tolerance assessment

These references are loaded automatically by the skill as needed during analysis.

## Testing Alpaca Connection

Before using the skill, test your Alpaca API connection:

```bash
uv run python skills/portfolio-manager/scripts/check_alpaca_connection.py
```

Expected output:
```
✓ Successfully connected to Alpaca API
Account Status: ACTIVE
Account Number: ****6789
Equity: $100,000.00
Cash: $50,000.00
Buying Power: $200,000.00
Positions: 5
```

The diagnostic never prints the API key or secret and masks the account number.
It writes only to stdout and does not create a report or place orders.

If you see errors, consult `references/alpaca-mcp-setup.md` for troubleshooting.

## Example Workflow

### Initial Portfolio Review

1. **Trigger analysis:**
   ```
   User: "Analyze my portfolio"
   ```

2. **Skill workflow:**
   - Fetches positions from Alpaca MCP
   - Retrieves account information
   - Gathers market data for each position
   - Performs comprehensive analysis
   - Generates detailed report

3. **Report generated:**
   - `portfolio_analysis_2025-11-08.md`
   - Includes all analysis sections
   - Specific recommendations provided

4. **Follow-up questions:**
   ```
   User: "Why should I trim NVDA?"
   User: "What should I buy instead?"
   User: "Is my tech allocation too high?"
   ```

### Ongoing Monitoring

**Quarterly Review:**
```
User: "Review my portfolio for Q4 2025"
```

**After Market Events:**
```
User: "How did the market crash affect my portfolio?"
```

**Before Rebalancing:**
```
User: "Generate rebalancing recommendations"
```

## Key Concepts

### Asset Allocation
Distribution of portfolio across asset classes (stocks, bonds, cash). The primary driver of portfolio risk and return.

### Diversification
Spreading investments across multiple positions, sectors, and geographies to reduce unsystematic risk.

### Rebalancing
Systematically selling overweight positions and buying underweight positions to maintain target allocation.

### Position Sizing
Determining appropriate weight for each holding based on conviction, risk, and portfolio constraints.

### Risk-Adjusted Returns
Evaluating performance relative to risk taken (Sharpe ratio, Sortino ratio).

### Concentration Risk
Excessive exposure to single position, sector, or theme that creates elevated portfolio risk.

## Limitations and Disclaimers

**Important Notes:**

1. **Not Financial Advice** - This tool provides informational analysis only, not personalized financial advice.

2. **Data Accuracy** - Analysis quality depends on Alpaca API data accuracy and third-party market data.

3. **Market Conditions** - Historical analysis may not predict future performance, especially during regime changes.

4. **Tax Implications** - Tax impact estimates are approximate only; consult a tax professional.

5. **Execution Risk** - Recommendations assume ability to execute trades at current market prices.

**Always:**
- Verify critical data independently
- Consult qualified financial advisor before major decisions
- Consider your unique circumstances, risk tolerance, and goals
- Review tax implications with tax professional

## Troubleshooting

### "Alpaca MCP Server not connected"

**Solutions:**
1. Verify MCP server is running (`claude mcp status` if available)
2. Check environment variables are set: `echo $ALPACA_API_KEY`
3. Restart Claude to reinitialize MCP servers
4. Verify API keys in Alpaca dashboard
5. See `references/alpaca-mcp-setup.md` for detailed setup

### "Invalid API credentials"

**Solutions:**
1. Verify API Key ID and Secret Key (no typos, spaces)
2. Check `ALPACA_PAPER` setting matches your keys (paper vs live)
3. Regenerate API keys in Alpaca dashboard
4. Ensure account status is active

### "No positions found"

**Solutions:**
1. Verify positions exist in Alpaca dashboard
2. Confirm you're checking correct account (paper vs live)
3. Check account number matches
4. Try refreshing: ask Claude to fetch positions again

### Report seems inaccurate

**Solutions:**
1. Verify Alpaca data is current (check Alpaca dashboard)
2. Check if market data is delayed (free tier is 15-min delayed)
3. Manually verify a few key positions
4. Report discrepancies to improve analysis

## Version History

- **v1.0** (November 2025) - Initial release
  - Alpaca MCP Server integration
  - Comprehensive portfolio analysis
  - Multi-dimensional risk assessment
  - Position evaluation framework
  - Rebalancing recommendations
  - Model portfolio benchmarks

## Support and Contributing

**For Issues:**
- Check `references/` documentation
- Review troubleshooting section above
- Test Alpaca connection with `check_alpaca_connection.py`
- Check Alpaca API status: https://status.alpaca.markets/

**For Questions:**
- Alpaca API docs: https://alpaca.markets/docs/
- Alpaca community: https://forum.alpaca.markets/

**Skill Enhancement Ideas:**
- Additional broker integrations (Interactive Brokers, Schwab)
- Options portfolio analysis
- Factor exposure analysis
- Monte Carlo retirement projections
- Tax-loss harvesting automation

## Related Skills

This skill works well in combination with:

- **US Stock Analysis** - Deep dive into individual positions
- **Value Dividend Screener** - Find replacement stocks for rebalancing
- **Market News Analyst** - Understand recent market-moving events
- **Sector Analyst** - Analyze sector rotation patterns
- **US Market Bubble Detector** - Assess overall market risk environment

## License

See repository root for license information.

---

**Remember:** Successful portfolio management requires discipline, patience, and long-term perspective. Use this skill to maintain systematic approach and avoid emotional decision-making. The best portfolio is one you can stick with through all market conditions.

### Referencia: references/alpaca-mcp-setup.md

# Alpaca MCP Server Setup Guide

This guide explains how to set up and configure the Alpaca MCP (Model Context Protocol) Server for use with the Portfolio Manager skill.

## What is Alpaca MCP Server?

The Alpaca MCP Server is a Model Context Protocol server that provides Claude with access to your Alpaca brokerage account data through a standardized interface. This allows the Portfolio Manager skill to fetch real-time portfolio positions, account information, and transaction history directly from your Alpaca account.

## Prerequisites

### 1. Alpaca Account

You need an Alpaca brokerage account (paper trading or live):

- **Sign up:** https://alpaca.markets/
- **Paper Trading:** Free, uses simulated money (recommended for testing)
- **Live Trading:** Real money account (requires funding)

### 2. Alpaca API Keys

Generate API keys from your Alpaca dashboard:

**For Paper Trading:**
1. Log into Alpaca dashboard: https://app.alpaca.markets/
2. Navigate to "Paper Trading" account
3. Go to "Your API Keys" section
4. Click "Generate New Key"
5. Save your:
   - **API Key ID** (public key)
   - **Secret Key** (private key - only shown once!)

**For Live Trading:**
1. Log into Alpaca dashboard
2. Navigate to "Live Trading" account
3. Go to "Your API Keys" section
4. Click "Generate New Key"
5. Save your API credentials

⚠️ **Security Note:** Never share your Secret Key or commit it to version control. Treat it like a password.

## Installation

### Option 1: Using MCP Server (Recommended for Claude Desktop/Web)

**Step 1: Install Alpaca MCP Server**

The Alpaca MCP server may be available through Claude's MCP marketplace or as a standalone package.

Check if available in your Claude environment:
```bash
# List available MCP servers
claude mcp list
```

If not installed, follow Anthropic's MCP server installation guide for your platform.

**Step 2: Configure API Keys**

Set environment variables with your Alpaca credentials:

**On macOS/Linux:**
```bash
# For Paper Trading
export ALPACA_API_KEY="your_api_key_id"
export ALPACA_SECRET_KEY="your_secret_key"
export ALPACA_PAPER=true

# For Live Trading
export ALPACA_API_KEY="your_api_key_id"
export ALPACA_SECRET_KEY="your_secret_key"
export ALPACA_PAPER=false
```

Add to `~/.bashrc` or `~/.zshrc` to persist across sessions:
```bash
echo 'export ALPACA_API_KEY="your_api_key_id"' >> ~/.bashrc
echo 'export ALPACA_SECRET_KEY="your_secret_key"' >> ~/.bashrc
echo 'export ALPACA_PAPER=true' >> ~/.bashrc
source ~/.bashrc
```

**On Windows (PowerShell):**
```powershell
# For Paper Trading
$env:ALPACA_API_KEY="your_api_key_id"
$env:ALPACA_SECRET_KEY="your_secret_key"
$env:ALPACA_PAPER="true"

# For Live Trading
$env:ALPACA_API_KEY="your_api_key_id"
$env:ALPACA_SECRET_KEY="your_secret_key"
$env:ALPACA_PAPER="false"
```

To persist environment variables on Windows:
```powershell
[System.Environment]::SetEnvironmentVariable('ALPACA_API_KEY', 'your_api_key_id', 'User')
[System.Environment]::SetEnvironmentVariable('ALPACA_SECRET_KEY', 'your_secret_key', 'User')
[System.Environment]::SetEnvironmentVariable('ALPACA_PAPER', 'true', 'User')
```

**Step 3: Start MCP Server**

The MCP server should start automatically when Claude launches. Verify connection:
```bash
# Check MCP server status (if CLI available)
claude mcp status
```

### Option 2: Direct API Integration (Alternative)

If MCP server is unavailable, the skill can fall back to direct Alpaca API integration using Python:

**Step 1: Install Alpaca Python SDK**
```bash
pip install alpaca-trade-api
```

**Step 2: Create Configuration File**

Create `~/.alpaca/config.ini`:
```ini
[alpaca]
api_key_id = your_api_key_id
secret_key = your_secret_key
base_url = https://paper-api.alpaca.markets  # For paper trading
# base_url = https://api.alpaca.markets     # For live trading
```

Set proper permissions:
```bash
chmod 600 ~/.alpaca/config.ini
```

**Step 3: Test Connection**

Use the provided test script:
```bash
python3 skills/portfolio-manager/scripts/check_alpaca_connection.py
```

Expected output:
```
✓ Successfully connected to Alpaca API
Account Status: ACTIVE
Equity: $100,000.00
Cash: $50,000.00
Buying Power: $200,000.00
Positions: 5
```

## Available MCP Tools

Once configured, the Portfolio Manager skill can use these Alpaca MCP tools:

### `mcp__alpaca__get_account_info`
Fetches account summary:
- Total equity (portfolio value)
- Cash balance
- Buying power
- Account status
- Day trading buying power (if applicable)

### `mcp__alpaca__get_positions`
Retrieves all open positions:
- Symbol ticker
- Quantity (shares)
- Average entry price (cost basis)
- Current market price
- Current market value
- Unrealized P&L ($ and %)
- Today's P&L

### `mcp__alpaca__get_portfolio_history`
Gets historical portfolio performance:
- Equity time series
- Profit/loss time series
- Timeframes: 1D, 1W, 1M, 3M, 1Y, All

### `mcp__alpaca__get_orders`
Lists orders (open, filled, cancelled):
- Order ID
- Symbol
- Quantity
- Order type (market, limit, stop, etc.)
- Status
- Fill price (if filled)
- Timestamps

### `mcp__alpaca__get_activities`
Retrieves account activities:
- Trades (fills)
- Dividend payments
- Stock splits
- Journal entries

## Verification and Testing

### Test 1: Account Connection

Ask Claude to fetch account info:
```
"Can you get my Alpaca account information?"
```

Expected response should include your equity, cash, and buying power.

### Test 2: Portfolio Positions

Request current positions:
```
"What positions do I have in my portfolio?"
```

Expected response should list all holdings with quantities and values.

### Test 3: Portfolio Analysis

Trigger the Portfolio Manager skill:
```
"Analyze my portfolio"
```

The skill should:
1. Fetch positions via MCP
2. Gather additional market data
3. Perform comprehensive analysis
4. Generate detailed report

## Troubleshooting

### Error: "Alpaca MCP Server not connected"

**Possible causes:**
1. MCP server not running
2. API keys not configured
3. API keys invalid or expired

**Solutions:**
1. Restart Claude to reinitialize MCP servers
2. Verify environment variables are set: `echo $ALPACA_API_KEY`
3. Check API keys in Alpaca dashboard (regenerate if needed)
4. Verify account status (ensure not suspended)

### Error: "Invalid API credentials"

**Possible causes:**
1. Wrong API keys
2. Using live keys with paper mode (or vice versa)
3. API keys revoked

**Solutions:**
1. Double-check API Key ID and Secret Key (no extra spaces)
2. Verify `ALPACA_PAPER` setting matches your API keys
3. Regenerate API keys in Alpaca dashboard
4. Ensure you're using the correct account (paper vs live)

### Error: "Forbidden - insufficient permissions"

**Possible causes:**
1. API keys have restricted permissions
2. Account not approved for trading

**Solutions:**
1. Regenerate API keys with full permissions
2. Check Alpaca dashboard for account status
3. For live accounts, ensure account approval is complete

### Error: "No positions found"

**Possible causes:**
1. Portfolio is actually empty
2. Wrong account selected (paper vs live)
3. API returning stale data

**Solutions:**
1. Verify positions exist in Alpaca dashboard
2. Confirm `ALPACA_PAPER` setting matches intended account
3. Try refreshing: ask Claude to fetch positions again
4. Check Alpaca API status page: https://status.alpaca.markets/

### MCP Server Not Responding

**Solutions:**
1. Restart Claude application
2. Check MCP server logs (if available)
3. Verify network connectivity
4. Fall back to direct API integration (Option 2)

## Security Best Practices

### 1. Use Paper Trading for Testing
Always test with paper trading account first. Never risk real money until thoroughly tested.

### 2. Protect API Keys
- Never commit API keys to GitHub or version control
- Use environment variables, not hardcoded values
- Set file permissions: `chmod 600` for config files
- Rotate keys periodically (every 90 days)

### 3. Use Read-Only Keys (If Available)
For portfolio analysis only, use read-only API keys if Alpaca supports them. This prevents accidental trading.

### 4. Monitor API Usage
- Check Alpaca dashboard for API call logs
- Review account activities regularly
- Set up alerts for unusual activity

### 5. Separate Paper and Live Environments
- Use different environment variable prefixes
- Never mix paper and live credentials
- Document which keys are which

## API Rate Limits

Alpaca imposes rate limits on API calls:

**Free Tier:**
- 200 requests per minute
- Data delayed by 15 minutes (for free market data)

**Paid Tier (Alpaca Markets Data subscription):**
- Higher rate limits
- Real-time data

**Best Practices:**
- Portfolio Manager skill includes built-in rate limiting
- Avoid running analysis more than once per minute
- For frequent monitoring, consider caching results

## Alternative: Manual Data Entry

If Alpaca integration is unavailable, Portfolio Manager can accept manually entered portfolio data:

**CSV Format:**
```csv
symbol,quantity,cost_basis,current_price
AAPL,100,150.00,175.50
MSFT,50,280.00,310.25
GOOGL,25,2500.00,2750.00
```

**Usage:**
1. Export positions from your broker as CSV
2. Provide file to Claude: "Analyze my portfolio using this CSV file"
3. Skill will parse data and perform analysis

**Limitations:**
- No real-time updates
- No historical performance data
- Manual updates required

## Additional Resources

**Alpaca Documentation:**
- API docs: https://alpaca.markets/docs/
- Python SDK: https://github.com/alpacahq/alpaca-trade-api-python
- API reference: https://alpaca.markets/docs/api-references/trading-api/

**MCP Protocol:**
- Anthropic MCP docs: https://docs.anthropic.com/claude/docs/model-context-protocol
- MCP specification: https://github.com/anthropics/mcp

**Support:**
- Alpaca support: support@alpaca.markets
- Alpaca community: https://forum.alpaca.markets/
- API status: https://status.alpaca.markets/

### Referencia: references/asset-allocation.md

# Asset Allocation Framework

This document provides comprehensive guidance on asset allocation principles, target allocations by risk profile, and rebalancing triggers for portfolio management.

## Core Principles

### 1. Asset Allocation Drives Returns

Academic research shows that asset allocation accounts for approximately 90% of portfolio return variability over time. Security selection and market timing contribute far less to long-term outcomes.

**Key Insight:** Getting the allocation right is more important than picking individual stocks.

### 2. Diversification Across Asset Classes

Different asset classes have different risk-return characteristics and respond differently to economic conditions:

| Asset Class | Expected Return | Volatility | Purpose |
|-------------|----------------|------------|---------|
| **Stocks (Equities)** | 8-10% | High (15-20%) | Growth, long-term appreciation |
| **Bonds (Fixed Income)** | 3-5% | Low (3-6%) | Income, capital preservation, volatility dampening |
| **Cash & Equivalents** | 1-2% | Very Low | Liquidity, stability, opportunistic deployment |
| **Real Estate** | 6-8% | Medium (10-15%) | Income, inflation hedge, diversification |
| **Commodities** | 4-6% | High (15-25%) | Inflation hedge, diversification |
| **Alternatives** | Varies | Varies | Non-correlated returns, risk management |

*Note: Returns are historical long-term averages and not guaranteed. Actual returns vary significantly.*

### 3. Risk Tolerance Alignment

Asset allocation should match investor's risk tolerance and time horizon:

- **Risk Capacity:** Financial ability to withstand losses (net worth, income stability, time horizon)
- **Risk Tolerance:** Emotional ability to withstand volatility (behavioral, psychological)
- **Risk Requirement:** Return needed to achieve financial goals

Optimal allocation balances all three factors.

## Asset Allocation by Risk Profile

### Conservative (Capital Preservation)

**Investor Profile:**
- Age: Typically 60+ or near retirement
- Time Horizon: 0-5 years
- Primary Goal: Preserve capital, generate income
- Risk Tolerance: Low - cannot afford significant losses
- Volatility Tolerance: Minimal (<5-8% annual drawdown)

**Target Allocation:**
- **Stocks:** 20-40%
  - US Large Cap: 15-25%
  - US Small/Mid Cap: 0-5%
  - International: 5-10%
- **Bonds:** 50-70%
  - Investment Grade Corporate: 20-30%
  - Government Bonds: 20-30%
  - High Yield: 0-10%
- **Cash:** 10-20%
- **Alternatives:** 0-10%

**Sector Guidelines (Equity Portion):**
- Defensive sectors: 60-70% (Utilities, Consumer Staples, Healthcare)
- Cyclical sectors: 30-40%
- Avoid: High-growth tech, speculative stocks

**Expected Outcomes:**
- Annual Return: 4-6%
- Max Drawdown: -10 to -15%
- Recovery Time: 1-2 years

### Moderate (Balanced Growth & Income)

**Investor Profile:**
- Age: Typically 40-60
- Time Horizon: 5-15 years
- Primary Goal: Balanced growth and income
- Risk Tolerance: Medium - can handle moderate volatility
- Volatility Tolerance: Moderate (10-15% annual drawdown)

**Target Allocation:**
- **Stocks:** 50-70%
  - US Large Cap: 30-40%
  - US Small/Mid Cap: 10-15%
  - International: 10-15%
- **Bonds:** 25-40%
  - Investment Grade Corporate: 15-25%
  - Government Bonds: 5-10%
  - High Yield: 5-10%
- **Cash:** 5-10%
- **Alternatives:** 0-10%

**Sector Guidelines (Equity Portion):**
- Defensive sectors: 40-50%
- Growth sectors: 30-40% (Technology, Communication, Consumer Discretionary)
- Cyclical sectors: 20-30% (Industrials, Financials, Materials)

**Expected Outcomes:**
- Annual Return: 6-8%
- Max Drawdown: -15 to -25%
- Recovery Time: 2-4 years

### Growth (Long-Term Capital Appreciation)

**Investor Profile:**
- Age: Typically 30-50
- Time Horizon: 10-25 years
- Primary Goal: Long-term wealth accumulation
- Risk Tolerance: Medium-High - can withstand volatility for higher returns
- Volatility Tolerance: Significant (15-20% annual drawdown)

**Target Allocation:**
- **Stocks:** 75-90%
  - US Large Cap: 40-50%
  - US Small/Mid Cap: 15-20%
  - International: 15-20%
  - Emerging Markets: 5-10%
- **Bonds:** 10-20%
  - Investment Grade Corporate: 5-10%
  - High Yield: 5-10%
- **Cash:** 2-5%
- **Alternatives:** 0-10%

**Sector Guidelines (Equity Portion):**
- Growth sectors: 45-55% (Technology, Healthcare, Communication)
- Cyclical sectors: 25-35%
- Defensive sectors: 20-30%

**Expected Outcomes:**
- Annual Return: 8-10%
- Max Drawdown: -20 to -35%
- Recovery Time: 3-5 years

### Aggressive (Maximum Growth)

**Investor Profile:**
- Age: Typically <40 or high net worth with long horizon
- Time Horizon: 15+ years
- Primary Goal: Maximize wealth, comfortable with high risk
- Risk Tolerance: High - can emotionally and financially withstand major losses
- Volatility Tolerance: Very high (20-30%+ annual drawdown)

**Target Allocation:**
- **Stocks:** 90-100%
  - US Large Cap: 40-50%
  - US Small/Mid Cap: 20-25%
  - International: 15-20%
  - Emerging Markets: 10-15%
  - Alternatives: 0-5%
- **Bonds:** 0-10%
- **Cash:** 0-5%

**Sector Guidelines (Equity Portion):**
- Growth sectors: 50-60% (Technology, Healthcare, Consumer Discretionary)
- Cyclical sectors: 30-35%
- Defensive sectors: 10-20%
- May include speculative positions (small caps, growth stocks)

**Expected Outcomes:**
- Annual Return: 9-12%
- Max Drawdown: -30 to -50%
- Recovery Time: 4-7 years

## Sector Allocation Guidelines

### Defensive Sectors (Lower Volatility)

**Utilities (3-5% of equity allocation)**
- Characteristics: Stable cash flows, dividend-focused, regulated
- Economic Sensitivity: Low
- Use: Income generation, volatility dampening
- Overweight when: Late cycle, high uncertainty, rising rates

**Consumer Staples (5-10%)**
- Characteristics: Steady demand, pricing power, recession-resistant
- Economic Sensitivity: Low
- Use: Stability, dividend income
- Overweight when: Economic slowdown, defensive posture

**Healthcare (10-15%)**
- Characteristics: Demographic tailwinds, innovation-driven, essential services
- Economic Sensitivity: Low to Medium
- Use: Growth with defensive qualities
- Overweight when: Aging demographics, innovation cycle

### Growth Sectors (Higher Volatility, Higher Expected Returns)

**Technology (15-25%)**
- Characteristics: High growth, innovation-driven, secular trends
- Economic Sensitivity: Medium to High
- Use: Capital appreciation, secular growth
- Overweight when: Economic expansion, innovation cycles, low rates
- Caution: Concentration risk, valuation sensitivity

**Communication Services (5-10%)**
- Characteristics: Platform businesses, network effects, advertising-driven
- Economic Sensitivity: Medium
- Use: Growth, secular trends (digital transformation)
- Overweight when: Ad market strength, content consumption growth

**Consumer Discretionary (8-12%)**
- Characteristics: Cyclical demand, premium brands, e-commerce
- Economic Sensitivity: High
- Use: Economic growth exposure, consumer trends
- Overweight when: Strong consumer confidence, wage growth

### Cyclical Sectors (Economic Cycle Sensitive)

**Financials (10-15%)**
- Characteristics: Interest rate sensitive, credit cycle dependent
- Economic Sensitivity: High
- Use: Economic expansion exposure, dividend income
- Overweight when: Rising rates, strong economy, steepening yield curve

**Industrials (8-12%)**
- Characteristics: Capital goods, infrastructure, global trade
- Economic Sensitivity: High
- Use: Economic growth, infrastructure spending
- Overweight when: Fiscal stimulus, manufacturing upturn, globalization

**Materials (3-6%)**
- Characteristics: Commodity-driven, economic cycle dependent
- Economic Sensitivity: Very High
- Use: Inflation hedge, economic growth
- Overweight when: Infrastructure spending, commodity supercycles

**Energy (3-8%)**
- Characteristics: Commodity price driven, capital intensive, volatile
- Economic Sensitivity: High
- Use: Inflation hedge, commodity exposure
- Overweight when: Rising oil prices, underinvestment supply cycles
- Caution: ESG concerns, energy transition risk

**Real Estate (3-6%)**
- Characteristics: Income-focused, interest rate sensitive, inflation hedge
- Economic Sensitivity: Medium
- Use: Diversification, income, inflation protection
- Overweight when: Low rates, economic expansion, inflation

## Geographic Allocation

### US Equities (60-75% of total equity)

**Rationale:**
- Home market bias (reduce currency risk, familiar companies)
- Deepest, most liquid markets
- Strong corporate governance and shareholder rights
- Dollar-denominated returns

**Allocation by Market Cap:**
- Large Cap (>$10B): 60-70% of US equity
- Mid Cap ($2B-$10B): 20-25%
- Small Cap (<$2B): 10-15%

### International Developed Markets (15-25% of total equity)

**Regions:**
- Europe: 8-12%
- Japan: 3-5%
- UK: 2-4%
- Other (Canada, Australia): 2-4%

**Rationale:**
- Diversification (different economic cycles)
- Currency diversification
- Access to global industry leaders
- Valuation opportunities

**Considerations:**
- Currency risk (hedge or leave unhedged based on view)
- Political risk (EU regulatory environment, Brexit impact)
- Lower growth rates vs US

### Emerging Markets (5-15% of total equity)

**Regions:**
- China: 2-5%
- India: 1-3%
- Other Asia (Taiwan, Korea): 1-3%
- Latin America: 0-2%
- Other: 0-2%

**Rationale:**
- Higher growth potential
- Demographic advantages
- Commodity exposure
- Diversification

**Considerations:**
- Higher volatility
- Political and regulatory risk
- Currency volatility
- Liquidity concerns

**Risk Management:**
- Limit to 5-10% for moderate investors
- Use broad ETFs rather than individual stocks
- Monitor geopolitical developments

## Rebalancing Framework

### Rebalancing Triggers

**1. Time-Based Rebalancing**
- **Frequency:** Quarterly or Semi-Annually
- **Methodology:** Review allocation every 3-6 months, rebalance if needed
- **Pros:** Disciplined, predictable, simple
- **Cons:** May rebalance when not necessary (costs), or miss urgent needs

**2. Threshold-Based Rebalancing**
- **Trigger:** Allocation drifts >5% from target
- **Example:** If target is 60% stocks, rebalance when stocks reach <55% or >65%
- **Pros:** Responsive to market moves, cost-efficient
- **Cons:** Requires monitoring, may miss small drifts

**3. Hybrid Approach (Recommended)**
- **Method:** Check quarterly, rebalance only if drift >5%
- **Best of both worlds:** Disciplined review, cost-conscious execution

### Rebalancing Thresholds

| Allocation Drift | Action | Priority |
|-----------------|--------|----------|
| **<3%** | Monitor, no action needed | None |
| **3-5%** | Consider rebalancing (optional) | Low |
| **5-10%** | Rebalance recommended | Medium |
| **>10%** | Rebalance immediately | High |

**Position-Level Thresholds:**
- Single stock >15% of portfolio → Trim immediately
- Single stock >20% of portfolio → Urgent trim required
- Any position doubling target weight → Review and likely trim

### Rebalancing Methods

**1. Sell and Redeploy**
- **Method:** Sell overweight positions, buy underweight positions
- **Pros:** Precise rebalancing
- **Cons:** Tax implications (capital gains), transaction costs

**2. Direct New Contributions**
- **Method:** Use new cash to buy underweight positions
- **Pros:** No selling (tax-efficient), simple
- **Cons:** Slower rebalancing, requires regular contributions

**3. Dividend Reinvestment**
- **Method:** Reinvest dividends into underweight positions
- **Pros:** Tax-efficient, gradual rebalancing
- **Cons:** Very slow, limited impact

**4. Opportunistic (Tactical)**
- **Method:** Sell overweight positions on strength, buy underweight on weakness
- **Pros:** Improve execution prices
- **Cons:** Requires active monitoring, may delay rebalancing

**Recommendation:** Use method #1 (sell and redeploy) for large drifts (>10%), method #2 for small drifts (<5%), and method #4 when actively managing.

### Tax Considerations

**Tax-Loss Harvesting:**
- Sell positions with losses to offset capital gains
- Reinvest in similar (but not substantially identical) securities
- Avoid wash sale rule (30-day rule)

**Tax-Efficient Rebalancing:**
- Prioritize rebalancing in tax-advantaged accounts (IRA, 401k)
- In taxable accounts, hold winners >1 year for long-term capital gains rates
- Use new contributions to rebalance rather than selling

**Timing:**
- Rebalance in December to harvest losses
- Rebalance in January to deploy fresh capital
- Avoid year-end if sitting on large gains (defer taxes)

## Tactical Adjustments

While strategic asset allocation should be stable, tactical adjustments can enhance returns:

### Market Cycle Adjustments

**Early Bull Market:**
- Overweight: Cyclicals (Financials, Industrials, Materials)
- Underweight: Defensives (Utilities, Staples)
- Rationale: Economic acceleration favors cyclical sectors

**Mid Bull Market:**
- Overweight: Growth (Technology, Healthcare)
- Neutral: Cyclicals and Defensives
- Rationale: Expansion matures, focus on quality growth

**Late Bull Market:**
- Overweight: Defensives (Utilities, Staples, Healthcare)
- Underweight: Cyclicals
- Rationale: Prepare for slowdown, reduce beta

**Bear Market:**
- Overweight: Cash, Bonds, Defensive equities
- Underweight: Cyclical equities
- Rationale: Capital preservation, prepare for recovery

### Valuation-Based Adjustments

**When US stocks expensive (high Shiller PE >30):**
- Reduce US equity allocation by 5-10%
- Increase international or value stocks
- Increase cash/bonds

**When sectors extremely overvalued:**
- Trim sector allocation by 3-5%
- Redistribute to undervalued sectors
- Maintain overall equity target

### Interest Rate Adjustments

**Rising Rate Environment:**
- Shorten bond duration
- Overweight: Financials, Value stocks
- Underweight: High P/E growth, Utilities, REITs

**Falling Rate Environment:**
- Lengthen bond duration
- Overweight: Growth stocks, Technology, REITs
- Underweight: Financials

## Common Mistakes to Avoid

### 1. Market Timing
**Mistake:** Drastically changing allocation based on market predictions
**Impact:** Missing recoveries, buying high/selling low
**Solution:** Stick to strategic allocation, make only minor tactical adjustments

### 2. Over-Diversification
**Mistake:** Holding 100+ positions across 50 funds
**Impact:** Closet indexing, high fees, complexity
**Solution:** 15-30 individual stocks OR 5-10 ETFs for most investors

### 3. Under-Diversification
**Mistake:** Heavy concentration in single stock/sector (often employer stock)
**Impact:** Excessive risk, correlated life outcomes (job + portfolio)
**Solution:** Limit single stock to <10%, single sector to <25%

### 4. Ignoring Rebalancing
**Mistake:** "Let winners run" indefinitely
**Impact:** Portfolio drifts to high risk, concentration increases
**Solution:** Disciplined rebalancing schedule, trim winners

### 5. Emotional Rebalancing
**Mistake:** Panic selling in crashes, euphoric buying in bubbles
**Impact:** Locking in losses, buying tops
**Solution:** Systematic rebalancing rules, ignore emotions

### 6. Chasing Performance
**Mistake:** Shifting to last year's top-performing sectors
**Impact:** Mean reversion, buying expensive
**Solution:** Maintain strategic allocation, resist recency bias

## Allocation Review Checklist

Use this checklist when reviewing portfolio allocation:

**Asset Class Level:**
- [ ] Current stock/bond/cash allocation vs target (within 5%?)
- [ ] Risk profile still appropriate for goals/timeline?
- [ ] Any major life changes requiring allocation shift?
- [ ] Tax considerations for rebalancing?

**Sector Level:**
- [ ] Any sector >30% of equity allocation?
- [ ] Defensive sectors appropriate for market cycle?
- [ ] Growth vs value balance appropriate?
- [ ] Sector allocations reasonable vs benchmark?

**Geographic Level:**
- [ ] US vs International allocation on target?
- [ ] Emerging market exposure appropriate for risk tolerance?
- [ ] Any country concentration concerns?
- [ ] Currency exposure considerations?

**Position Level:**
- [ ] Any single stock >15% of portfolio?
- [ ] Top 10 holdings represent what % of portfolio?
- [ ] Any highly correlated positions creating concentration?
- [ ] Position sizes match conviction and risk?

**Performance Level:**
- [ ] Performance vs benchmark acceptable?
- [ ] Any positions consistently underperforming?
- [ ] Winners becoming too large (>2x initial allocation)?
- [ ] Losers requiring re-evaluation (broken thesis)?

## Summary

**Key Takeaways:**

1. **Asset allocation is the primary driver of returns** - Get the big picture right
2. **Match allocation to risk tolerance and time horizon** - Don't take more risk than you can handle
3. **Diversify across asset classes, sectors, and geographies** - Don't put all eggs in one basket
4. **Rebalance systematically** - Trim winners, add to losers, maintain discipline
5. **Minimize taxes and costs** - Tax-efficient rebalancing, low-cost implementation
6. **Stay the course** - Avoid emotional decisions, stick to the plan
7. **Review regularly but change rarely** - Annual review, infrequent major changes

**Remember:** Asset allocation should reflect your personal circumstances, not market forecasts. The best allocation is one you can stick with through market cycles.

### Referencia: references/csv-holdings-review.md

# Offline CSV holdings review (Issue #512 foundation)

Run from the repository root with Python 3.9+; no API keys or third-party imports:

```bash
python3 skills/portfolio-manager/scripts/review_csv.py \
  --input skills/portfolio-manager/assets/fictional_holdings.csv \
  --as-of 2026-10-20T12:00:00Z --output-dir reports
```

For a standalone package, run `python3 scripts/review_csv.py --input
assets/fictional_holdings.csv --as-of 2026-10-20T12:00:00Z --output-dir reports`
from the extracted skill directory. The fixture contains fictional USD equities.
Supply the actual source snapshot timestamp for your own CSV; the script does
not verify prices, ownership, completeness or freshness. It never fetches quotes.

## Input contract

UTF-8 CSV (optional BOM), one header row, comma separator, at most 10,000 holdings.
Required headers: `symbol,asset_type,quantity,direction,price,currency`.
Optional headers: `cost_basis,account`. Header order is arbitrary; unknown,
missing and duplicate headers are errors. Every record must match the header width.

| Field | Contract |
|---|---|
| symbol | Strip surrounding spaces, uppercase; `[A-Z][A-Z0-9.-]{0,23}`. Operator asserts this identifies the intended instrument. |
| asset_type | Exactly `equity`; options, futures and other instruments are unsupported. |
| quantity | Positive share count; fractional shares supported. |
| direction | Exactly `LONG` or `SHORT`; quantities are always positive. |
| price | Positive snapshot price per share, supplied by operator. |
| currency | Exactly `USD`; currency conversion is unavailable. |
| cost_basis | Optional nonnegative acquisition price per share; blank/missing means unknown. Excludes fees, dividends and tax adjustments. |
| account | Optional ignored field, discarded before reporting. Review one account at a time; never use this column to infer account completeness. |

Numbers use plain unsigned decimal notation, at most 32 characters and 12
fractional digits, and cannot exceed 1e12. Exponents, signs, whitespace, NaN,
infinity and zero quantity/price are invalid. A zero cost basis is permitted.
Duplicate normalized symbols, including separate tax lots or long/short rows,
are rejected: consolidate them manually into the intended single holding first;
do not net hedges merely to bypass the validator. Empty/header-only files fail;
this tool does not establish that an account is empty.

## Output contract

Writes `portfolio_csv_review.json` and `portfolio_csv_review.md` into the output
directory, replacing previous reports with those names. Use a new directory to
retain history. Validation errors return exit 1, write a safe stderr diagnostic
with row/field context, and create no reports. Argument errors return exit 2.
I/O errors return exit 1; if writing fails midway, discard both report files and
rerun. Existing reports are not proof that the latest invocation succeeded.

JSON `schema_version: 1`, `report_type: holdings_allocation_only` contains:

- `provenance`: `source: local_csv`, UTC `as_of`, `freshness: operator_asserted`.
- `gross_holdings_value`: sum of quantity × price across all positions.
- `net_holdings_value`: signed sum (shorts negative). Neither is account equity.
- `positions`: sorted sanitized symbols, asset_type, direction, quantity, price,
  currency, nullable cost_basis, gross_market_value, net_market_value,
  gross_weight_pct and nullable unrealized_pnl. Decimal values are strings to
  preserve precision. Weights use gross holdings value, rounded to six decimal
  percentage places; rounded weights may not sum exactly to 100.
- `unrealized_pnl`: quantity × (price − cost_basis), sign reversed for shorts.
  Unknown costs yield null, rendered `unavailable`. No aggregate P&L is emitted.
- `limitations`: explicit unavailable analyses and integration boundaries.

The fictional fixture yields gross value 80, signed net value 20, gross weights
62.5% and 37.5%, and per-position unrealized P&L of 12.5 and 10 USD.
Cash, equity, margin/leverage, sector allocations, beta, historical returns,
dividend health and trading recommendations are unavailable. Gross weights can
look benign in a leveraged account: never use them as account exposure or as
authorization to trade.

## Privacy and integration boundary

No network, broker access, orders, memory edits or reconciliation gate. The input
filename/path and account column are excluded from script diagnostics and output.
Reports still contain potentially sensitive holdings, quantities and cost data;
keep inputs/reports local and do not commit or upload personal data. This is
field minimization, not anonymization. CLI arguments/paths can remain in shell
history. Never pass secrets in a command or CSV.

This standalone allocation foundation does **not** make `core-portfolio-weekly`
runnable from CSV. Navigator retains its honest unshipped-workflow diagnostic.
Workflow/skillset integration, replay and an API/CSV shared analysis contract
remain outstanding under #512. Broker reports currently have a broader contract;
do not present this report as equivalent or bypass broker/memory reconciliation.

### Referencia: references/diversification-principles.md

# Diversification Principles

This document explains the theory and practice of portfolio diversification, providing frameworks for assessing diversification quality and identifying concentration risks.

## Core Concepts

### What is Diversification?

Diversification is the practice of spreading investments across various assets, sectors, and geographies to reduce portfolio risk without proportionally reducing expected returns.

**Harry Markowitz's Key Insight (1952):**
> "Diversification is the only free lunch in finance."

By combining assets with imperfect correlation, investors can achieve better risk-adjusted returns than holding individual securities.

### The Math Behind Diversification

**Portfolio Risk Formula:**

For a two-asset portfolio:
```
σ_p = √(w₁²σ₁² + w₂²σ₂² + 2w₁w₂σ₁σ₂ρ₁₂)

Where:
σ_p = Portfolio standard deviation (risk)
w₁, w₂ = Weights of assets 1 and 2
σ₁, σ₂ = Standard deviations of assets 1 and 2
ρ₁₂ = Correlation between assets 1 and 2
```

**Key Insight:** When correlation < 1.0, portfolio risk is less than the weighted average of individual risks.

### Types of Risk

**1. Systematic Risk (Market Risk)**
- **Definition:** Risk inherent to the entire market
- **Examples:** Recessions, interest rate changes, geopolitical events
- **Cannot be eliminated** by diversification
- **Beta** measures exposure to systematic risk

**2. Unsystematic Risk (Specific Risk)**
- **Definition:** Risk specific to individual companies or sectors
- **Examples:** Management failures, product recalls, competitive losses
- **Can be reduced** through diversification
- **Diversification benefit:** Holding 15-30 stocks eliminates ~90% of unsystematic risk

**Modern Portfolio Theory Goal:** Eliminate unsystematic risk while accepting systematic risk (compensated by market risk premium).

## Optimal Number of Holdings

### Individual Stocks

Research shows diminishing diversification benefits beyond a certain number of holdings:

| Number of Stocks | % of Unsystematic Risk Eliminated |
|------------------|----------------------------------|
| 1 | 0% (all risk remains) |
| 5 | ~40% |
| 10 | ~65% |
| 15 | ~75% |
| 20 | ~85% |
| 30 | ~90% |
| 50 | ~93% |
| 100 | ~95% |

**Recommended Range: 15-30 stocks**

**Why not more than 30?**
- Marginal diversification benefit very small
- Increased complexity and monitoring burden
- Higher transaction costs
- Diluted impact of high-conviction ideas
- "Closet indexing" (might as well own an ETF)

**Why not fewer than 15?**
- Insufficient elimination of unsystematic risk
- Concentration risk remains significant
- Single-stock events can severely impact portfolio
- Correlation underestimation risk

### ETFs and Mutual Funds

**For diversified funds (broad market, sector, international):**
- **5-10 ETFs** can provide excellent diversification
- Each ETF already holds dozens to thousands of stocks
- Focus on low overlap and complementary exposures

**Example Well-Diversified 6-ETF Portfolio:**
1. US Large Cap (S&P 500)
2. US Small/Mid Cap
3. International Developed Markets
4. Emerging Markets
5. US Bonds (Aggregate)
6. Real Estate (REITs)

## Correlation and Diversification

### Understanding Correlation

**Correlation coefficient (ρ) ranges from -1.0 to +1.0:**

| Correlation | Interpretation | Diversification Benefit |
|-------------|----------------|------------------------|
| **+1.0** | Perfect positive correlation | None (redundant holdings) |
| **+0.7 to +0.9** | Very high correlation | Minimal |
| **+0.3 to +0.7** | Moderate positive correlation | Good |
| **0 to +0.3** | Low positive correlation | Excellent |
| **0** | No correlation | Maximum benefit |
| **-0.3 to 0** | Low negative correlation | Excellent (hedging) |
| **< -0.3** | Moderate to strong negative correlation | Hedging properties |

### Typical Stock Correlations

**Within Same Sector:**
- Large tech stocks (AAPL, MSFT, GOOGL): ρ ≈ 0.6-0.8
- Banks (JPM, BAC, WFC): ρ ≈ 0.7-0.9
- Oil companies (XOM, CVX): ρ ≈ 0.8-0.9

**Across Different Sectors:**
- Tech vs Healthcare: ρ ≈ 0.3-0.5
- Utilities vs Technology: ρ ≈ 0.2-0.4
- Consumer Staples vs Energy: ρ ≈ 0.3-0.5

**Defensive vs Cyclical:**
- Utilities vs Industrials: ρ ≈ 0.2-0.4
- Consumer Staples vs Consumer Discretionary: ρ ≈ 0.4-0.6

**US vs International:**
- US stocks vs International Developed: ρ ≈ 0.7-0.9 (increasing over time)
- US stocks vs Emerging Markets: ρ ≈ 0.6-0.8

**Stocks vs Bonds:**
- US Stocks vs US Treasuries: ρ ≈ -0.2 to +0.3 (varies by regime)
- Stocks vs Corporate Bonds: ρ ≈ 0.4-0.6

### Correlation Pitfalls

**1. Correlation Instability**
- Correlations increase during market crashes ("correlation goes to 1 in a crisis")
- Diversification benefits diminish when most needed
- Solution: Include truly uncorrelated assets (gold, volatility strategies)

**2. Hidden Correlations**
- Stocks may appear different but share common risk factors
- Example: Bank stocks + homebuilders both exposed to interest rates
- Solution: Analyze underlying risk factors, not just sector labels

**3. Globalization Effect**
- International diversification less effective than historically
- US and global markets increasingly correlated
- Solution: Still valuable, but expect lower diversification benefit than in past

## Concentration Risk Measurement

### Position Concentration

**Single Position Thresholds:**

| Position Size | Risk Level | Action |
|---------------|------------|--------|
| **<5%** | Low | Acceptable for all positions |
| **5-10%** | Medium | Monitor, ensure high conviction |
| **10-15%** | High | Trim recommended unless exceptional conviction |
| **15-20%** | Very High | Trim immediately (except rare cases) |
| **>20%** | Extreme | Urgent trim required |

**Top Holdings Concentration:**

| Top 5 Holdings | Risk Assessment |
|----------------|-----------------|
| **<25%** | Well-diversified |
| **25-40%** | Moderate concentration |
| **40-60%** | High concentration |
| **>60%** | Excessive concentration |

**Example:**
- If top 5 positions = 55% of portfolio → High concentration risk
- If largest single position = 18% → Immediate trim recommended

### Sector Concentration

**Sector Allocation Thresholds:**

| Sector Weight | Risk Level | Guidance |
|---------------|------------|----------|
| **<15%** | Underweight | May be intentional or opportunity |
| **15-25%** | Normal | Typical for major sectors |
| **25-30%** | Moderate overweight | Monitor, ensure intentional |
| **30-40%** | High overweight | Trim recommended |
| **>40%** | Excessive concentration | Urgent diversification needed |

**S&P 500 Sector Benchmarks (approximate):**
- Technology: 25-30%
- Healthcare: 12-15%
- Financials: 10-13%
- Consumer Discretionary: 10-12%
- Communication Services: 8-10%
- Industrials: 8-10%
- Consumer Staples: 6-8%
- Energy: 3-5%
- Utilities: 2-3%
- Real Estate: 2-3%
- Materials: 2-3%

**Deviation Analysis:**
- **>10% above benchmark** = Significant overweight (ensure intentional)
- **>20% above benchmark** = Excessive overweight (trim recommended)

### Herfindahl-Hirschman Index (HHI)

**Formula:**
```
HHI = Σ(w_i × 100)²

Where w_i = weight of position i (as decimal)
```

**Interpretation:**

| HHI Score | Concentration Level | Portfolio Characteristics |
|-----------|---------------------|--------------------------|
| **<1000** | Low concentration | Well-diversified (25+ equal positions) |
| **1000-1800** | Moderate concentration | Typical diversified portfolio (15-25 stocks) |
| **1800-2500** | High concentration | Concentrated portfolio (8-15 stocks) |
| **>2500** | Very high concentration | Very concentrated (5-8 stocks) |
| **>4000** | Extreme concentration | Poorly diversified (<5 stocks) |

**Example Calculation:**

Portfolio with 5 positions:
- Position A: 30% → (30)² = 900
- Position B: 25% → (25)² = 625
- Position C: 20% → (20)² = 400
- Position D: 15% → (15)² = 225
- Position E: 10% → (10)² = 100

HHI = 900 + 625 + 400 + 225 + 100 = **2250** (High concentration)

## Multi-Dimensional Diversification

Effective diversification requires spreading risk across multiple dimensions:

### 1. Number of Holdings (Quantity)
- **Target:** 15-30 individual stocks OR 5-10 diversified funds
- **Measure:** Count of positions
- **Risk:** Too few = concentration; too many = over-diversification

### 2. Position Sizing (Weight)
- **Target:** No single position >10-15%, top 5 <40%
- **Measure:** HHI, top-N concentration
- **Risk:** Unequal weighting creates concentration despite many holdings

### 3. Sector Allocation (Industry)
- **Target:** No sector >30-35%, diversified across 6+ sectors
- **Measure:** Sector breakdown, compare to benchmark
- **Risk:** Industry-specific shocks (e.g., tech crash 2000, financial crisis 2008)

### 4. Market Cap (Size)
- **Target:** Mix of large-cap (60-70%), mid-cap (20-25%), small-cap (10-15%)
- **Measure:** Weighted average market cap, cap-based breakdown
- **Risk:** Small caps more volatile; large caps may underperform in recoveries

### 5. Geography (Region)
- **Target:** US 60-75%, International Developed 15-25%, Emerging Markets 5-15%
- **Measure:** Revenue geography, listing geography
- **Risk:** Country-specific risks (politics, currency, regulation)

### 6. Style (Growth vs Value)
- **Target:** Balanced or slight tilt based on market cycle
- **Measure:** Average P/E, P/B, growth rates of holdings
- **Risk:** Style rotation (growth outperforms in some periods, value in others)

### 7. Correlation (Independence)
- **Target:** Average pairwise correlation <0.6
- **Measure:** Correlation matrix of holdings
- **Risk:** High correlation = false diversification

### 8. Factor Exposures (Risk Factors)
- **Target:** Balanced exposure to momentum, quality, volatility, etc.
- **Measure:** Factor loadings (requires advanced analytics)
- **Risk:** Concentrated factor bets (e.g., all momentum stocks)

## Practical Diversification Strategies

### Strategy 1: Equal Weighting

**Method:** Each position gets equal allocation (e.g., 20 stocks = 5% each)

**Pros:**
- Simple to implement
- Automatic rebalancing to smaller positions
- Reduces concentration risk

**Cons:**
- Ignores conviction levels
- May overweight low-quality names
- Higher turnover (frequent rebalancing)

**Best for:** Passive investors, index-like approaches

### Strategy 2: Conviction Weighting

**Method:** Allocate more to high-conviction ideas, less to lower conviction

**Example Tiers:**
- High conviction: 7-10% positions (5-8 stocks)
- Medium conviction: 4-6% positions (8-12 stocks)
- Low conviction / Satellite: 2-3% positions (5-10 stocks)

**Pros:**
- Reflects analytical edge
- Better risk-adjusted returns if skill exists
- Maintains diversification

**Cons:**
- Requires honest conviction assessment
- Risk of overconfidence
- Can lead to concentration

**Best for:** Active investors with research capability

### Strategy 3: Risk Parity

**Method:** Allocate based on risk contribution, not dollar value

**Example:**
- Volatile stock (beta 1.8): 3% allocation
- Moderate stock (beta 1.0): 5% allocation
- Stable stock (beta 0.6): 8% allocation

**Pros:**
- True diversification of risk
- More stable portfolio performance
- Thoughtful risk management

**Cons:**
- Complex to implement
- Requires volatility estimates
- May overweight low-quality stable stocks

**Best for:** Sophisticated investors, risk-focused approaches

### Strategy 4: Core-Satellite

**Method:**
- **Core (60-80%):** Diversified, low-cost index funds
- **Satellite (20-40%):** High-conviction individual stocks or sector bets

**Pros:**
- Combines passive diversification with active upside
- Reduces risk of stock-picking errors
- Cost-efficient

**Cons:**
- Performance depends on satellite selection
- Complexity in management
- Tax efficiency varies

**Best for:** Investors who want both diversification and active involvement

## Diversification Quality Checklist

Use this checklist to assess portfolio diversification:

**Position Diversification:**
- [ ] Portfolio has 15-30 stocks (or 5-10 diversified funds)
- [ ] No single position exceeds 10% of portfolio
- [ ] No single position exceeds 15% of portfolio
- [ ] Top 5 positions represent less than 40% of portfolio
- [ ] HHI score below 1800

**Sector Diversification:**
- [ ] No single sector exceeds 30% of equity allocation
- [ ] Portfolio includes at least 6 different sectors
- [ ] Sector weights reasonably close to benchmark (within 15%)
- [ ] Balance between growth, defensive, and cyclical sectors
- [ ] No overconcentration in single industry (e.g., semiconductors within tech)

**Correlation Diversification:**
- [ ] Holdings span multiple industries with different drivers
- [ ] Average pairwise correlation estimated below 0.6
- [ ] Not all positions are high-beta growth stocks
- [ ] Includes mix of cyclical and defensive names
- [ ] Some low-correlation positions included (staples, utilities, healthcare)

**Geographic Diversification:**
- [ ] International exposure present (15-30% of equities)
- [ ] Not 100% dependent on US economic performance
- [ ] Emerging market exposure if appropriate for risk tolerance
- [ ] Consider revenue geography, not just listing location

**Market Cap Diversification:**
- [ ] Mix of large-cap, mid-cap, and potentially small-cap
- [ ] Not exclusively mega-caps (>$500B)
- [ ] Not exclusively small-caps (<$2B)
- [ ] Weighted average market cap appropriate for risk tolerance

**Asset Class Diversification:**
- [ ] Equity allocation matches risk tolerance
- [ ] Fixed income present (unless very aggressive allocation)
- [ ] Cash buffer for opportunities and liquidity
- [ ] Alternative assets if appropriate (real estate, commodities)

## Common Diversification Mistakes

### Mistake 1: False Diversification

**Problem:** Holding many stocks that are highly correlated

**Example:**
- Portfolio: AAPL, MSFT, GOOGL, AMZN, META, NVDA, TSLA (all large-cap tech/growth)
- **Appears** diversified (7 stocks)
- **Actually** highly concentrated (single sector, similar risk factors)

**Solution:** Diversify across sectors, not just number of names

### Mistake 2: Over-Diversification ("Diworsification")

**Problem:** Holding too many positions, diluting returns with no additional risk reduction

**Example:**
- 100 individual stock positions
- Overlap with index funds
- Closet indexing with higher fees

**Solution:** Stick to 15-30 best ideas OR use low-cost index funds

### Mistake 3: Home Country Bias

**Problem:** Overweighting domestic stocks, missing global opportunities

**Example:**
- US investor with 95% US stocks
- US represents ~60% of global market cap
- Missing international diversification benefit

**Solution:** Allocate 15-30% to international equities

### Mistake 4: Employer Stock Concentration

**Problem:** Large position in employer stock creates correlated life risks

**Example:**
- 40% of portfolio in employer stock
- Job + portfolio both dependent on same company
- "Double jeopardy" if company struggles

**Solution:** Trim to <10% of portfolio, diversify proceeds

### Mistake 5: Sector Drift

**Problem:** Letting winners run creates unintended sector concentration

**Example:**
- Tech stocks appreciate 200%, now 50% of portfolio
- Investor didn't actively overweight tech, just didn't rebalance
- Concentrated risk without conviction

**Solution:** Regular rebalancing to maintain diversification

### Mistake 6: Forgetting About Bonds

**Problem:** 100% equities for investors who can't handle volatility

**Example:**
- Aggressive investor holds all stocks
- Market drops 30%, investor panics and sells at bottom
- Would have been better with 70/30 stock/bond mix

**Solution:** Match allocation to risk tolerance and time horizon

### Mistake 7: Low-Quality Diversification

**Problem:** Adding poor-quality stocks just to increase position count

**Example:**
- Has 20 quality stocks, adds 10 speculative names to "diversify"
- Speculative names drag down returns without meaningfully reducing risk
- Quality dilution

**Solution:** Diversify within quality standards, don't lower bar for diversification

## Advanced Topics

### Factor-Based Diversification

Beyond traditional diversification, consider factor exposures:

**Common Factors:**
- **Value:** Low P/E, P/B stocks
- **Growth:** High revenue/earnings growth
- **Momentum:** Recent price performance
- **Quality:** High ROE, stable earnings
- **Low Volatility:** Low beta, stable returns
- **Size:** Small cap vs large cap

**Factor Diversification:**
- Avoid loading entirely on one factor (e.g., all momentum stocks)
- Balance factor exposures or tilt deliberately
- Recognize factor cycles (value outperforms in some periods, growth in others)

### Tail Risk and Black Swans

**Problem:** Normal diversification fails in extreme events

**2008 Financial Crisis Example:**
- Stocks fell 50%+
- Most correlations approached 1.0
- Traditional diversification provided limited protection

**Solutions:**
- **Include uncorrelated assets:** Gold, long-volatility strategies, managed futures
- **Tail hedges:** Put options, VIX calls (expensive, insurance-like)
- **Portfolio construction:** Barbell approach (safe core + aggressive satellites)

### Dynamic Diversification

**Concept:** Adjust diversification based on market conditions

**High Volatility Regimes:**
- Increase diversification (more positions, lower concentration)
- Add defensive positions
- Reduce correlation among holdings

**Low Volatility Regimes:**
- Can handle slightly higher concentration
- Focus on highest conviction ideas
- Accept higher correlation

**Implementation Challenge:** Requires market regime detection and discipline

## Summary

**Key Principles:**

1. **Diversification reduces unsystematic risk** without eliminating systematic risk
2. **Optimal range:** 15-30 individual stocks OR 5-10 diversified funds
3. **Multi-dimensional approach:** Number, weight, sector, geography, correlation
4. **Avoid false diversification:** Many holdings with high correlation
5. **Avoid over-diversification:** Too many positions dilute returns
6. **Regular rebalancing** prevents concentration drift
7. **Match to risk tolerance:** More diversification for lower risk tolerance

**Practical Guidelines:**

- No single stock >10-15%
- No single sector >30-35%
- Top 5 holdings <40% of portfolio
- 6+ sectors represented
- International exposure 15-30%
- Asset allocation matches time horizon and risk tolerance

**Remember:** Diversification is about risk management, not return maximization. A well-diversified portfolio sacrifices some upside potential to protect against catastrophic losses. The goal is to "stay in the game" through all market conditions.

### Referencia: references/portfolio-risk-metrics.md

# Portfolio Risk Metrics

This document provides comprehensive guidance on measuring and interpreting portfolio risk using standard financial metrics.

## Overview

Portfolio risk assessment requires both quantitative metrics and qualitative judgment. This guide covers:

1. Volatility-based metrics (standard deviation, beta)
2. Downside risk measures (maximum drawdown, semi-deviation)
3. Risk-adjusted return metrics (Sharpe ratio, Sortino ratio)
4. Concentration and correlation metrics
5. Interpretation frameworks for different investor types

## Volatility Metrics

### Standard Deviation (σ)

**Definition:** Measure of how much returns vary from the average return over time.

**Formula:**
```
σ = √[Σ(R_i - R_avg)² / (n-1)]

Where:
R_i = Return in period i
R_avg = Average return
n = Number of periods
```

**Interpretation:**

| Annual Std Dev | Risk Level | Typical Assets |
|---------------|------------|----------------|
| **<5%** | Very Low | Cash, short-term bonds |
| **5-10%** | Low | Bond portfolios, conservative balanced |
| **10-15%** | Moderate | Balanced portfolios (60/40), dividend stocks |
| **15-20%** | High | Stock portfolios, growth stocks |
| **>20%** | Very High | Small caps, emerging markets, sector funds |

**S&P 500 Historical:** ~15-18% annualized standard deviation

**Usage in Portfolio Analysis:**
- Compare portfolio volatility to benchmarks
- Assess if volatility matches investor risk tolerance
- Track changes in volatility over time (increasing volatility = warning sign)

**Limitations:**
- Assumes normal distribution (actual returns have "fat tails")
- Treats upside and downside volatility equally
- Based on historical data (may not predict future)

### Beta (β)

**Definition:** Measure of portfolio sensitivity to market movements.

**Formula:**
```
β = Cov(R_portfolio, R_market) / Var(R_market)

Or estimated as:
β = (Σw_i × β_i)

Where:
w_i = Weight of position i
β_i = Beta of position i
```

**Interpretation:**

| Beta | Market Sensitivity | Portfolio Behavior |
|------|-------------------|-------------------|
| **β < 0.5** | Very low | Defensive, low correlation to market |
| **β = 0.5-0.8** | Low | Below-market volatility, defensive tilt |
| **β = 0.8-1.0** | Moderate | Slightly less volatile than market |
| **β = 1.0** | Market | Moves in line with market (index-like) |
| **β = 1.0-1.3** | Moderate-high | More volatile than market |
| **β = 1.3-1.6** | High | Significantly more volatile |
| **β > 1.6** | Very high | Extremely volatile, aggressive |

**Typical Security Betas:**
- Utilities: 0.4-0.7
- Consumer Staples: 0.5-0.8
- Healthcare: 0.8-1.1
- S&P 500 Index: 1.0
- Technology: 1.1-1.5
- Small-cap growth: 1.3-2.0
- Leveraged ETFs: 2.0-3.0

**Example Portfolio Beta Calculation:**

Portfolio:
- 40% SPY (S&P 500 ETF, β=1.0): 0.40 × 1.0 = 0.40
- 30% QQQ (Nasdaq ETF, β=1.2): 0.30 × 1.2 = 0.36
- 20% VNQ (REIT ETF, β=0.9): 0.20 × 0.9 = 0.18
- 10% TLT (Bond ETF, β=0.3): 0.10 × 0.3 = 0.03

**Portfolio Beta** = 0.40 + 0.36 + 0.18 + 0.03 = **0.97**

**Interpretation:** Portfolio expected to move 97% as much as the market (slightly defensive).

**Usage:**
- Assess portfolio aggressiveness
- Predict portfolio behavior in market moves (β=1.2 means 12% drop when market drops 10%)
- Identify need for hedging or rebalancing

**Limitations:**
- Beta changes over time
- Based on historical correlations
- May not hold in extreme markets

### Semi-Deviation

**Definition:** Standard deviation of returns below the mean (focuses on downside volatility only).

**Formula:**
```
Semi-deviation = √[Σ(R_i - R_avg)² for all R_i < R_avg / n]
```

**Interpretation:**
- Lower semi-deviation = better downside protection
- Useful for risk-averse investors who care more about losses than gains
- Typically 60-70% of standard deviation for symmetric distributions

**Usage:**
- Evaluate downside risk specifically
- Compare defensive vs aggressive strategies
- Input for Sortino ratio (risk-adjusted return metric)

## Downside Risk Metrics

### Maximum Drawdown (MDD)

**Definition:** Largest peak-to-trough decline in portfolio value over a specific period.

**Formula:**
```
MDD = (Trough Value - Peak Value) / Peak Value

Or: MDD = max[(P_peak - P_trough) / P_peak] over all peaks
```

**Example:**
- Portfolio peak: $150,000 (March 2020)
- Portfolio trough: $105,000 (March 2020 crash)
- MDD = ($105k - $150k) / $150k = **-30%**

**Historical Maximum Drawdowns:**

| Asset/Portfolio | Max Drawdown | Period |
|----------------|--------------|--------|
| S&P 500 | -57% | 2007-2009 (Financial Crisis) |
| S&P 500 | -34% | 2020 (COVID Crash) |
| Nasdaq 100 | -83% | 2000-2002 (Tech Bubble) |
| Nasdaq 100 | -32% | 2021-2022 (Rate Hikes) |
| 60/40 Portfolio | -32% | 2007-2009 |
| Treasury Bonds | -48% | 2020-2023 (Rising Rates) |

**Risk Tolerance Guide:**

| Investor Type | Max Acceptable Drawdown |
|--------------|------------------------|
| **Conservative** | -10 to -15% |
| **Moderate** | -15 to -25% |
| **Growth** | -25 to -35% |
| **Aggressive** | -35 to -50% |

**Usage:**
- Assess worst-case historical scenario
- Compare to investor risk tolerance
- Set risk management triggers (e.g., hedge if drawdown >20%)
- Estimate recovery time needed

**Recovery Time:**
- 20% drawdown requires +25% gain to recover
- 30% drawdown requires +43% gain
- 50% drawdown requires +100% gain (doubling)

### Current Drawdown

**Definition:** Decline from most recent peak to current value.

**Formula:**
```
Current Drawdown = (Current Value - Recent Peak Value) / Recent Peak Value
```

**Example:**
- Recent peak: $150,000 (last month)
- Current value: $142,500
- Current drawdown = ($142.5k - $150k) / $150k = **-5%**

**Interpretation:**

| Current Drawdown | Status | Action |
|-----------------|--------|--------|
| **0%** | At all-time high | Monitor for complacency |
| **-1% to -5%** | Minor pullback | Normal, no action |
| **-5% to -10%** | Moderate correction | Review positions, monitor |
| **-10% to -20%** | Correction | Assess portfolio, consider adjustments |
| **>-20%** | Bear market territory | Review allocation, consider rebalancing |

**Usage:**
- Real-time risk monitoring
- Identify when portfolio is under stress
- Trigger rebalancing or risk reduction

### Value at Risk (VaR)

**Definition:** Maximum expected loss over a given time period at a given confidence level.

**Example:**
- 1-month VaR at 95% confidence = $10,000
- **Interpretation:** 95% confident that portfolio will not lose more than $10,000 in the next month (or: 5% chance of losing more than $10,000)

**Calculation Methods:**

1. **Historical VaR:** Use historical return distribution
2. **Parametric VaR:** Assume normal distribution, use mean and std dev
3. **Monte Carlo VaR:** Simulate thousands of scenarios

**Simplified Parametric VaR Formula:**
```
VaR = Portfolio Value × (z-score × σ - μ)

Where:
z-score = 1.65 for 95% confidence, 2.33 for 99% confidence
σ = Portfolio standard deviation (daily or monthly)
μ = Expected return (daily or monthly)
```

**Example Calculation:**
- Portfolio value: $100,000
- Annual std dev: 18%
- Monthly std dev: 18% / √12 = 5.2%
- Expected monthly return: 0.5%

**95% 1-month VaR:**
```
VaR = $100,000 × (1.65 × 5.2% - 0.5%)
    = $100,000 × (8.58% - 0.5%)
    = $100,000 × 8.08%
    = $8,080
```

**Interpretation:** 95% confident that portfolio will not lose more than $8,080 in the next month.

**Usage:**
- Risk budgeting
- Setting position limits
- Regulatory compliance (for institutions)

**Limitations:**
- Assumes historical patterns continue
- Underestimates tail risk (extreme events)
- Doesn't tell you about losses beyond VaR threshold

## Risk-Adjusted Return Metrics

### Sharpe Ratio

**Definition:** Excess return per unit of risk (reward-to-variability ratio).

**Formula:**
```
Sharpe Ratio = (R_portfolio - R_f) / σ_portfolio

Where:
R_portfolio = Portfolio return (annualized)
R_f = Risk-free rate (typically 10-year Treasury)
σ_portfolio = Portfolio standard deviation (annualized)
```

**Example Calculation:**
- Portfolio return: 12%
- Risk-free rate: 4%
- Portfolio std dev: 15%

**Sharpe = (12% - 4%) / 15% = 8% / 15% = 0.53**

**Interpretation:**

| Sharpe Ratio | Quality | Interpretation |
|--------------|---------|----------------|
| **< 0** | Poor | Return less than risk-free rate |
| **0 - 0.5** | Suboptimal | Low excess return for risk taken |
| **0.5 - 1.0** | Good | Adequate risk-adjusted return |
| **1.0 - 2.0** | Very Good | Strong risk-adjusted return |
| **> 2.0** | Excellent | Exceptional risk-adjusted return |

**Typical Sharpe Ratios:**
- S&P 500 (long-term): 0.3-0.5
- Well-managed equity portfolio: 0.5-0.8
- Exceptional hedge fund: 1.0-1.5
- Market-neutral strategy: 1.5-2.0+

**Usage:**
- Compare different portfolios or strategies
- Assess if additional risk is being compensated
- Benchmark against market (S&P 500 Sharpe)

**Limitations:**
- Penalizes upside volatility equally with downside
- Assumes normal distribution
- Sensitive to time period chosen

### Sortino Ratio

**Definition:** Like Sharpe ratio, but uses downside deviation instead of total volatility.

**Formula:**
```
Sortino Ratio = (R_portfolio - R_f) / Semi-deviation

Where semi-deviation only counts returns below risk-free rate
```

**Example:**
- Portfolio return: 12%
- Risk-free rate: 4%
- Semi-deviation (downside only): 10%

**Sortino = (12% - 4%) / 10% = 0.80**

**Interpretation:**
- Higher Sortino = better downside-adjusted returns
- Sortino typically higher than Sharpe (since semi-deviation < standard deviation)
- Preferred metric for risk-averse investors

**Usage:**
- Evaluate strategies with asymmetric returns (e.g., option strategies)
- Focus on downside protection
- Compare portfolios with different return distributions

### Calmar Ratio

**Definition:** Return relative to maximum drawdown.

**Formula:**
```
Calmar Ratio = Annualized Return / |Max Drawdown|
```

**Example:**
- Annualized return: 10%
- Max drawdown: -25%

**Calmar = 10% / 25% = 0.40**

**Interpretation:**

| Calmar Ratio | Quality |
|--------------|---------|
| **< 0.5** | Poor (high drawdown relative to return) |
| **0.5 - 1.0** | Acceptable |
| **1.0 - 2.0** | Good |
| **> 2.0** | Excellent (low drawdown, high return) |

**Usage:**
- Focus on worst-case scenarios
- Evaluate hedge funds and absolute return strategies
- Assess recovery potential

## Concentration and Correlation Metrics

### Concentration Metrics

**1. Top-N Concentration**

Percentage of portfolio in largest N positions:

```
Top-N % = (Σ Top N Position Values) / Total Portfolio Value
```

**Guidelines:**
- Top 1 position: <10% ideal, <15% maximum
- Top 5 positions: <40% ideal, <50% maximum
- Top 10 positions: <60% ideal, <70% maximum

**2. Herfindahl-Hirschman Index (HHI)**

(See diversification-principles.md for detailed explanation)

```
HHI = Σ(Weight_i × 100)²
```

**Quick Assessment:**
- HHI < 1000: Well-diversified
- HHI 1000-1800: Moderately concentrated
- HHI > 1800: High concentration

### Correlation Metrics

**Average Pairwise Correlation**

Average correlation between all position pairs:

```
Avg Correlation = Σ(ρ_ij) / Number of pairs

Where:
ρ_ij = correlation between positions i and j
Number of pairs = n(n-1)/2 for n positions
```

**Example (5 positions):**
- 10 pairs total
- Sum of correlations: 5.2
- Average: 5.2 / 10 = **0.52**

**Interpretation:**

| Avg Correlation | Diversification Quality |
|----------------|------------------------|
| **< 0.3** | Excellent (low correlation) |
| **0.3 - 0.5** | Good |
| **0.5 - 0.7** | Moderate (typical equity portfolio) |
| **> 0.7** | Poor (positions move together) |

## Risk Scoring Framework

### Composite Risk Score (0-100)

Combine multiple metrics into single score:

**Scoring Formula:**

```
Risk Score =
  (Volatility Score × 30%) +
  (Beta Score × 20%) +
  (Drawdown Score × 25%) +
  (Concentration Score × 25%)
```

**Individual Component Scores (0-100):**

**1. Volatility Score:**
- <10% std dev: 0-20 points (low risk)
- 10-15% std dev: 20-40 points
- 15-20% std dev: 40-60 points
- 20-25% std dev: 60-80 points
- >25% std dev: 80-100 points (very high risk)

**2. Beta Score:**
- β < 0.8: 0-20 points
- β 0.8-1.0: 20-40 points
- β 1.0-1.3: 40-60 points
- β 1.3-1.6: 60-80 points
- β > 1.6: 80-100 points

**3. Drawdown Score:**
- Max DD <10%: 0-20 points
- Max DD 10-20%: 20-40 points
- Max DD 20-30%: 40-60 points
- Max DD 30-40%: 60-80 points
- Max DD >40%: 80-100 points

**4. Concentration Score:**
- HHI <1000: 0-20 points
- HHI 1000-1500: 20-40 points
- HHI 1500-2000: 40-60 points
- HHI 2000-2500: 60-80 points
- HHI >2500: 80-100 points

**Composite Risk Score Interpretation:**

| Score | Risk Level | Appropriate For |
|-------|-----------|-----------------|
| **0-20** | Very Low | Ultra-conservative, retirees |
| **20-40** | Low | Conservative investors |
| **40-60** | Moderate | Balanced investors |
| **60-80** | High | Growth-oriented investors |
| **80-100** | Very High | Aggressive, long time horizon |

## Practical Risk Assessment Workflow

### Step 1: Calculate Basic Metrics

1. **Portfolio Beta** (weighted average of position betas)
2. **Standard Deviation** (if historical data available, else estimate)
3. **Maximum Drawdown** (from portfolio history)
4. **Current Drawdown** (vs recent peak)
5. **Top-5 Concentration** (sum of 5 largest positions)
6. **HHI** (concentration index)

### Step 2: Compare to Benchmarks

**Against S&P 500:**
- Is beta higher or lower than 1.0?
- Is volatility higher or lower than ~16%?

**Against Risk Profile Targets:**
- Does risk level match investor's stated risk tolerance?
- Is maximum drawdown acceptable?

### Step 3: Identify Risk Concentrations

**Position-Level:**
- Any position >15%? → Immediate trim
- Top 5 >50%? → High concentration

**Sector-Level:**
- Any sector >35%? → Concentration risk
- Any sector missing? → Diversification gap

**Factor-Level:**
- All high-beta growth stocks? → Factor concentration
- All value stocks? → Style concentration

### Step 4: Risk-Adjusted Performance

1. **Calculate Sharpe Ratio** (if return history available)
2. **Compare to benchmark:** Is portfolio delivering better risk-adjusted returns?
3. **Calculate Sortino Ratio** for downside focus
4. **Assess if excess risk is being rewarded**

### Step 5: Generate Risk Assessment

**Summary Format:**

```markdown
## Portfolio Risk Assessment

**Overall Risk Profile:** [Conservative / Moderate / Growth / Aggressive]

**Risk Score:** XX/100 ([Low / Medium / High / Very High])

**Key Metrics:**
- Portfolio Beta: X.XX (vs market 1.00)
- Estimated Volatility: XX% annualized
- Maximum Drawdown: -XX% (acceptable for [risk profile])
- Current Drawdown: -X% (vs recent peak)

**Risk Concentrations:**
- Top 5 positions: XX% of portfolio ([OK / High / Excessive])
- Largest single position: [SYMBOL] at XX% ([OK / Trim recommended])
- HHI: XXXX ([Well-diversified / Concentrated])

**Risk-Adjusted Performance:**
- Sharpe Ratio: X.XX ([Below / In-line / Above] market)
- Sortino Ratio: X.XX
- Performance for risk taken: [Excellent / Good / Fair / Poor]

**Risk Recommendations:**
- [List specific actions to reduce risk if needed]
```

## Risk Management Guidelines

### When to Reduce Risk

**Signals:**
- Portfolio beta >1.5 for moderate risk tolerance investor
- Max drawdown exceeds investor's tolerance
- Single position >15% of portfolio
- Sector concentration >40%
- Current drawdown >20% (entering bear market)

**Actions:**
- Trim concentrated positions
- Add defensive sectors (Utilities, Staples, Healthcare)
- Increase bond allocation
- Raise cash levels

### When to Increase Risk

**Signals:**
- Portfolio beta <0.7 for growth-oriented investor
- Cash position >15% (unless intentionally defensive)
- Underperforming benchmark significantly with lower volatility
- Long time horizon with conservative allocation

**Actions:**
- Add growth sectors (Technology, Consumer Discretionary)
- Increase equity allocation
- Deploy excess cash
- Add higher-conviction positions

## Summary

**Key Takeaways:**

1. **Multiple metrics needed:** No single metric tells the full story
2. **Volatility measures:** Standard deviation and beta for overall risk
3. **Downside risk:** Maximum drawdown, current drawdown, VaR for worst-case scenarios
4. **Risk-adjusted returns:** Sharpe and Sortino ratios for performance quality
5. **Concentration:** HHI and top-N positions for diversification assessment
6. **Match to investor:** Risk metrics must align with risk tolerance and goals
7. **Monitor continuously:** Risk characteristics change as markets move

**Practical Application:**

- Calculate key metrics quarterly
- Compare to investor risk tolerance
- Identify concentrations and gaps
- Adjust allocation to maintain target risk level
- Document risk assessment in portfolio reports

**Remember:** Risk metrics are tools, not absolute truth. Use judgment and consider qualitative factors (market environment, economic outlook, investor circumstances) alongside quantitative metrics.

### Referencia: references/position-evaluation.md

# Position Evaluation Framework

This document provides a systematic framework for evaluating individual positions within a portfolio to determine appropriate actions: HOLD, ADD, TRIM, or SELL.

## Overview

Position evaluation requires both quantitative analysis and qualitative judgment. This framework helps answer:

1. Is the original investment thesis still intact?
2. Is the position appropriately sized given current conviction and risk?
3. Has the valuation become stretched or attractive?
4. What is the expected forward return vs risk?
5. Are there better opportunities elsewhere?

## Four-Factor Evaluation Model

Every position should be evaluated across four dimensions:

### 1. Thesis Validation (40% weight)
- Is the investment thesis playing out as expected?
- Have fundamentals improved, remained stable, or deteriorated?
- Are growth prospects intact or changed?

### 2. Valuation Assessment (30% weight)
- Is the stock overvalued, fairly valued, or undervalued?
- How does current valuation compare to historical range?
- How does it compare to peer group?

### 3. Position Sizing (20% weight)
- Is current position size appropriate?
- Does it match conviction level?
- Is it creating concentration risk?

### 4. Relative Opportunity (10% weight)
- Are there better uses of capital?
- Would selling this improve portfolio?
- Cost of holding vs deploying elsewhere

## Detailed Evaluation Framework

### Thesis Validation Analysis

**Original Thesis Documentation:**

For each position, document the original investment thesis:

**Example Thesis Template:**
```
Symbol: AAPL
Initial Thesis (Date: Jan 2023):
- Services revenue growing 15%+ annually
- Installed base expansion (1.8B → 2.0B devices)
- Margin expansion from services mix shift
- Capital return program (dividends + buybacks)
- Valuation: P/E 24x vs historical 18x, justified by services growth

Entry Price: $145
Target Price: $180 (12-month)
Expected Return: 24% (+2% dividend = 26% total)
Risk Factors: iPhone demand slowdown, China regulatory risk
```

**Thesis Validation Checklist:**

- [ ] **Revenue/Earnings Growth:** On track vs expectations?
  - Expected: +15% revenue growth
  - Actual: +12% (slightly below, acceptable / -5% (concerning))

- [ ] **Margins:** Improving, stable, or declining?
  - Expected: Expanding by 100bps
  - Actual: Expanded 80bps (close enough / Contracted 50bps (negative))

- [ ] **Competitive Position:** Strengthening or weakening?
  - Market share trends
  - New product success/failures
  - Competitor actions

- [ ] **Management Execution:** Meeting targets?
  - Guidance met/beaten/missed
  - Capital allocation decisions
  - Strategic pivots if any

- [ ] **Industry Tailwinds:** Still present?
  - Secular trends intact?
  - Regulatory changes
  - Technology shifts

**Thesis Status Classification:**

| Status | Criteria | Action Bias |
|--------|----------|-------------|
| **Strengthening** | Fundamentals improving, thesis accelerating | Consider ADD |
| **Intact** | On track with expectations, no changes | HOLD |
| **Weakening** | Some concerns, thesis partially impaired | Consider TRIM |
| **Broken** | Thesis invalid, fundamentals deteriorating | SELL |

### Valuation Assessment

**Valuation Methodology:**

Compare current valuation across multiple dimensions:

**1. Historical Valuation Range**

| Metric | Current | 1Y Avg | 3Y Avg | 5Y Avg | Min | Max |
|--------|---------|--------|--------|--------|-----|-----|
| P/E | 28x | 25x | 22x | 20x | 12x | 35x |
| P/B | 6.5x | 5.8x | 5.2x | 4.8x | 3.5x | 8.0x |
| EV/EBITDA | 22x | 19x | 17x | 16x | 10x | 25x |
| Div Yield | 1.2% | 1.4% | 1.6% | 1.8% | 0.8% | 2.5% |

**Analysis:**
- Current P/E (28x) near 3Y max (35x) → Expensive vs history
- P/B elevated vs 5Y avg → Premium valuation
- Dividend yield low vs range → Not a value play

**2. Peer Group Comparison**

| Company | P/E | P/B | EV/EBITDA | Dividend Yield | Rev Growth | Margin |
|---------|-----|-----|-----------|----------------|------------|--------|
| **[Target]** | 28x | 6.5x | 22x | 1.2% | 12% | 28% |
| Peer A | 22x | 4.2x | 18x | 1.8% | 8% | 22% |
| Peer B | 31x | 7.8x | 25x | 0.9% | 18% | 32% |
| Peer C | 25x | 5.1x | 20x | 1.5% | 10% | 25% |
| **Sector Median** | 25x | 5.5x | 20x | 1.4% | 11% | 26% |

**Analysis:**
- P/E slightly above sector median → Modest premium
- Growth (12%) above median (11%) → Premium partially justified
- Margins (28%) above median (26%) → Quality justifies some premium
- **Assessment:** Fair to slightly expensive vs peers

**3. Growth-Adjusted Valuation (PEG Ratio)**

```
PEG Ratio = P/E / Earnings Growth Rate

Example:
P/E: 28x
Expected EPS growth: 15%
PEG = 28 / 15 = 1.87

Interpretation:
< 1.0 = Undervalued
1.0-2.0 = Fair value
> 2.0 = Overvalued
```

**4. DCF Fair Value Estimate (Simplified)**

If time permits, estimate intrinsic value using discounted cash flow:

```
Fair Value = (FCF × (1 + growth rate)^5) / (discount rate - terminal growth)

Example inputs:
Current FCF: $100B
Growth (5Y): 12%
Discount rate: 10%
Terminal growth: 4%
```

**Valuation Status Classification:**

| Status | Criteria | Action Bias |
|--------|----------|-------------|
| **Undervalued** | Below historical avg, below peers, low PEG | ADD |
| **Fair Value** | In-line with history and peers | HOLD |
| **Overvalued** | Above historical range, premium to peers, high PEG | TRIM |
| **Severely Overvalued** | Extreme multiples, bubble-like | SELL |

### Position Sizing Analysis

**Current Position Assessment:**

```
Position Size = Position Value / Total Portfolio Value

Example:
Position value: $18,000
Portfolio value: $120,000
Position size: 18,000 / 120,000 = 15%
```

**Position Sizing Guidelines:**

| Conviction Level | Target Position Size | Max Position Size |
|------------------|---------------------|-------------------|
| **High Conviction** | 8-12% | 15% |
| **Medium Conviction** | 5-8% | 10% |
| **Low Conviction / Speculative** | 2-5% | 7% |
| **Starter Position** | 2-3% | 5% |

**Position Sizing Risk Assessment:**

| Current Size | Risk Level | Typical Action |
|--------------|-----------|----------------|
| **<5%** | Low | Can add if conviction high |
| **5-10%** | Normal | Monitor |
| **10-15%** | Elevated | Trim if conviction not very high |
| **15-20%** | High | Trim recommended |
| **>20%** | Excessive | Urgent trim required |

**Position Drift Analysis:**

Track how position size has changed due to price appreciation:

```
Position Appreciation Impact:

Initial investment: $10,000 (10% of $100K portfolio)
Other holdings flat, this position doubled
Current value: $20,000 (18% of $110K portfolio)

Position drift: 10% → 18% (increased 8 percentage points)
Exceeded target: Yes (assuming 10% target)
Action: Trim back to 10-12% range
```

**Rebalancing Calculation:**

```
To trim from 18% to 10%:

Target value: $110,000 × 10% = $11,000
Current value: $20,000
Amount to sell: $20,000 - $11,000 = $9,000
Shares to sell: $9,000 / Current Price
```

### Relative Opportunity Analysis

**Opportunity Cost Framework:**

Ask: "If I sold this position today, where would I deploy the capital?"

**Comparison Matrix:**

| Option | Expected Return | Risk Level | Conviction | Notes |
|--------|----------------|------------|-----------|-------|
| **Hold [Current]** | 8% | Medium | Medium | Fairly valued, thesis intact |
| Alternative A | 15% | High | High | Undervalued, strong thesis |
| Alternative B | 10% | Low | Medium | Defensive, lower risk |
| Cash (wait) | 4% | None | N/A | Opportunity cost |

**Decision Logic:**

If (Alternative Expected Return - Hold Expected Return) > Switching Cost:
→ Consider selling current, buying alternative

**Switching Costs to Consider:**
- **Taxes:** Capital gains (15-20% long-term, ordinary income short-term)
- **Transaction costs:** Commissions (minimal) + bid-ask spread
- **Opportunity risk:** Wrong about alternative, miss rebound in current

**Example Calculation:**

```
Current position: Expected 8% return
Alternative: Expected 15% return
Differential: 7%

Unrealized gain: $8,000 on $20,000 position (67% gain)
Tax on sale (20% long-term): $8,000 × 0.20 = $1,600
After-tax proceeds: $20,000 - $1,600 = $18,400

After-tax opportunity gain (1 year):
Hold current: $20,000 × 1.08 = $21,600
Buy alternative: $18,400 × 1.15 = $21,160

Conclusion: Tax drag eliminates benefit for 1-year hold
Consider if: (1) Multi-year horizon, or (2) Tax-advantaged account, or (3) Can tax-loss harvest elsewhere
```

## Position Action Decision Matrix

Combine the four factors to determine action:

### HOLD Decision

**Criteria:**
- ✅ Thesis: Intact or strengthening
- ✅ Valuation: Fair to undervalued
- ✅ Position Size: Within target range (5-10% for medium conviction)
- ✅ Relative Opportunity: No clearly better alternative after costs

**Example:**
```
Position: Johnson & Johnson (JNJ)
Thesis: ✅ Intact (healthcare demand, dividend aristocrat)
Valuation: ✅ Fair (P/E 16x vs 15x historical avg)
Position Size: ✅ 7% of portfolio (target range)
Opportunity: ✅ No compelling alternative in healthcare

Decision: HOLD
Rationale: Position performing as expected, appropriately sized, no reason to change
Next Review: Quarterly earnings (Q3 2024)
```

### ADD Decision

**Criteria:**
- ✅ Thesis: Strengthening or intact with high conviction
- ✅ Valuation: Undervalued or fair with improving fundamentals
- ✅ Position Size: Below target, room to add without excessive concentration
- ✅ Opportunity: Among top ideas, better than alternatives

**Example:**
```
Position: Meta Platforms (META)
Thesis: ✅ Strengthening (AI monetization exceeding expectations, cost discipline)
Valuation: ✅ Undervalued (P/E 22x vs 28x historical, PEG 1.2)
Position Size: ✅ 5% of portfolio (room to add to 8-10%)
Opportunity: ✅ Top conviction, better expected return than alternatives

Decision: ADD 3-5% more (increase position to 8-10% total)
Rationale: Thesis improving, valuation attractive, high conviction
Entry Strategy: Add 3% now, 2% more if pullback to $450 support
Risk Management: Set stop-loss at $420 (recent low)
```

### TRIM Decision

**Criteria:**
- ⚠️ Thesis: Weakening OR still intact but lower conviction
- ⚠️ Valuation: Overvalued or expensive vs historical/peers
- ⚠️ Position Size: Exceeded target (>12% for medium conviction, >15% for high conviction)
- ⚠️ Opportunity: Better alternatives available or risk reduction needed

**Example:**
```
Position: NVIDIA (NVDA)
Thesis: ✅ Intact (AI demand strong) ⚠️ but slowing growth rates expected
Valuation: ⚠️ Expensive (P/E 65x vs 45x historical, extended vs peers)
Position Size: ⚠️ 18% of portfolio (exceeded 15% max)
Opportunity: ⚠️ Other high-quality tech at better valuations

Decision: TRIM from 18% to 10-12%
Rationale: Valuation extended, position too large, take some profits
Trim Strategy: Sell 6% now, consider selling another 2% if rallies above $950
Redeployment: Add to underweight healthcare and financials sectors
Tax Strategy: Sell highest-cost-basis shares first (minimize tax impact)
```

### SELL Decision

**Criteria:**
- ❌ Thesis: Broken or significantly impaired
- OR: Valuation severely overvalued with deteriorating fundamentals
- OR: Better opportunities + need to reduce position count
- OR: Risk management (stop-loss triggered, risk too high)

**Example:**
```
Position: Teladoc (TDOC)
Thesis: ❌ Broken (telehealth adoption slower than expected, competition intense, path to profitability unclear)
Valuation: ❌ Expensive vs peers despite losses (EV/Sales 2.5x vs 1.2x sector)
Position Size: ⚠️ 4% of portfolio (not excessive, but capital can be better deployed)
Opportunity: ❌ Multiple better healthcare alternatives (UNH, ELW, CVS)

Decision: SELL (exit position entirely)
Rationale: Investment thesis has not materialized, competitive position weakening, capital better deployed elsewhere
Exit Strategy: Sell entire position over 2-3 days (avoid moving market)
Redeployment: Reallocate to UnitedHealth Group (stronger healthcare thesis)
Tax Benefit: Harvest $2,000 capital loss to offset gains
Lesson Learned: Avoid unprofitable growth stocks in competitive industries
```

## Position Review Checklist

Use this checklist when reviewing each position:

### Fundamental Review
- [ ] Read recent earnings report and call transcript
- [ ] Review updated financial metrics (revenue, margins, EPS)
- [ ] Check for guidance changes (raised, lowered, maintained)
- [ ] Read recent analyst reports or news
- [ ] Verify competitive position (market share, new entrants)

### Valuation Review
- [ ] Calculate current P/E, P/B, EV/EBITDA
- [ ] Compare to 1Y, 3Y, 5Y historical averages
- [ ] Compare to peer group
- [ ] Calculate PEG ratio
- [ ] Assess if valuation justified by fundamentals

### Portfolio Fit Review
- [ ] Calculate current position size (% of portfolio)
- [ ] Assess if size matches conviction
- [ ] Check if position contributes to concentration risk
- [ ] Verify sector allocation impact
- [ ] Evaluate correlation with other holdings

### Risk Review
- [ ] Identify new risks (regulatory, competitive, macro)
- [ ] Assess if stop-loss should be updated
- [ ] Review downside scenario (what could go wrong?)
- [ ] Check beta and volatility (has it increased?)
- [ ] Evaluate if risk/reward still favorable

### Action Decision
- [ ] Does thesis warrant HOLD/ADD/TRIM/SELL?
- [ ] If change needed, what is specific action?
- [ ] What is timeline for action (immediate, gradual, wait for level)?
- [ ] What are trigger points for future action?
- [ ] Document decision and rationale

## Common Position Evaluation Mistakes

### Mistake 1: Anchoring to Purchase Price

**Problem:** "I bought at $100, now it's $80, I'll wait to break even before selling"

**Why wrong:** Purchase price is irrelevant to forward returns. Sunk cost fallacy.

**Correct approach:** Evaluate position based on current fundamentals and forward outlook. If thesis broken, sell now regardless of gain/loss.

### Mistake 2: Letting Winners Run Indefinitely

**Problem:** "It's my best performer, I'll never sell!"

**Why wrong:** Position becomes oversized, creates concentration risk, valuation may become stretched.

**Correct approach:** Trim winners back to target weight periodically. Take some profits. Reinvest in undervalued areas.

### Mistake 3: Selling Losers Too Quickly

**Problem:** "It's down 15%, I need to cut losses"

**Why wrong:** Volatility is normal. Selling in panic often locks in losses before recovery.

**Correct approach:** Evaluate if thesis still intact. If yes, consider adding (averaging down). If no, sell regardless of loss size.

### Mistake 4: Ignoring Valuation ("Quality at Any Price")

**Problem:** "This is a great company, valuation doesn't matter"

**Why wrong:** Even great companies can be overvalued. Future returns depend on entry price.

**Correct approach:** Great companies at fair prices. Trim when expensive, add when cheap, even for high-quality names.

### Mistake 5: Falling in Love with Stocks

**Problem:** Emotional attachment prevents objective evaluation

**Why wrong:** Stocks don't love you back. Capital allocation should be ruthlessly rational.

**Correct approach:** Treat positions as capital deployment decisions, not relationships. Be willing to sell anything if better opportunity exists.

## Summary

**Position Evaluation Framework:**

1. **Thesis Validation (40%)** - Is the story still true?
2. **Valuation Assessment (30%)** - Is the price right?
3. **Position Sizing (20%)** - Is the size appropriate?
4. **Relative Opportunity (10%)** - Are there better uses of capital?

**Four Actions:**

- **HOLD:** Thesis intact, fair valuation, appropriate size
- **ADD:** Strengthening thesis, undervalued, room to add
- **TRIM:** Weakening thesis OR expensive OR oversized
- **SELL:** Broken thesis OR severely overvalued OR much better alternatives

**Best Practices:**

- Review positions quarterly (at minimum)
- Document thesis at purchase
- Update thesis as new information emerges
- Be willing to admit mistakes early
- Trim winners to maintain diversification
- Average down only if thesis intact
- Ignore purchase price (sunk cost)
- Remain objective and unemotional

**Remember:** Position evaluation is both art and science. Combine quantitative metrics with qualitative judgment. When in doubt, reduce position size rather than holding full position or selling entirely.

### Referencia: references/position-reconciliation.md

# Read-only broker / trader-memory reconciliation

Run this manual gate after fetching holdings and **before** allocation or rebalance
review in `core-portfolio-weekly`. Compare actual remaining positions with the
trader's recorded lifecycle. Never place orders, edit theses, or silently repair
mismatches through this tool.

## Prepare comparable snapshots

Create two local JSON files with this contract (fictional example):

```json
{
  "schema_version": 1,
  "account_scope": "paper_demo",
  "as_of": "2026-10-09T12:00:00Z",
  "complete": true,
  "positions": [
    {"symbol": "FICTA", "asset_type": "equity", "direction": "LONG", "quantity": "0.125"}
  ]
}
```

- Use the **same complete account scope and snapshot instant** for both files.
  Use a non-sensitive account alias, never an account number. `as_of` must include
  a timezone; equivalent offsets are accepted. Record the actual capture instant,
  not the thesis creation date. Freeze the comparison view during export; if
  broker or memory changes during capture, capture both again. Do not relabel old
  data with a new timestamp to bypass this requirement.
- Set `complete: true` only after confirming all open equity positions in the
  selected account are represented, including positions absent from memory.
  `positions: []` means a verified empty account, never a failed/missing export.
- Map broker equity/ETF positions to `symbol`, `asset_type: equity`, explicit
  `LONG`/`SHORT`, and **positive absolute remaining share quantity**. When the
  broker encodes shorts as negative quantities, verify the broker's side field
  agrees before taking the absolute value. Resolve inconsistent signs manually.
  Omit cash; do not omit unsupported options, crypto or futures to get a pass:
  any such instrument makes this equity-only gate unsuitable and requires review.
- Obtain **both ACTIVE and PARTIALLY_CLOSED** memory records. `thesis_store.py list`
  (or `query()` / `list_active()`) returns lightweight index entries, not complete
  position records; `list_active()` alone also misses partial closes. First run
  the read-only `doctor` command to check file/index consistency, then enumerate
  both statuses and load each full thesis with `get` / `get()` and validate it
  using `validate_thesis()`. Do not run `rebuild-index` as part of this gate.
- For memory equities, map `ticker` to symbol, direction to **LONG** (the current
  equity lifecycle is long-only), and `position.shares_remaining` to quantity.
  Never use original `position.shares` for a trimmed position. Missing remaining
  quantity on a legacy ACTIVE record requires manual resolution, not a fallback.
  Exclude IDEA, ENTRY_READY, CLOSED and INVALIDATED records; futures use contracts
  and are unsupported here. Do not treat an arbitrary memory `position.direction`
  extra field as authoritative for equities.
- Trader-memory currently has no native account attribution. The operator must
  verify each thesis belongs to this account; ambiguous assignment blocks review.
  Reject duplicate symbols, including opposite directions. Resolve multi-thesis
  lots and split-account records manually before normalization; do not silently
  sum them or net longs and shorts. This tool does not automate that attribution.
- Quantities may be JSON numbers or decimal strings (strings preserve fractional
  precision). Accepted range is 1e-12 through 1e12 shares, at most 64 characters.
  Zero, negative, Boolean, non-finite and missing quantities block the gate.
  Symbol comparison trims surrounding whitespace and uppercases symbols; confirm
  symbol/asset identity manually for renamed tickers or multiple share classes.

## Compare and stop on unresolved differences

```bash
python3 skills/portfolio-manager/scripts/reconcile_positions.py \
  --broker reports/broker-normalized.json \
  --memory reports/memory-normalized.json \
  --output-dir reports/portfolio-reconciliation
```

The command uses only local files, writes `reconciliation_report.json` and
`reconciliation_report.md` to the requested directory, and prints JSON to stdout.
Omit `--output-dir` for stdout-only comparison. Both source files remain unchanged.
Keep reports private: position quantities and the account alias can still reveal
sensitive trading information. Do not commit real snapshots or reports.

### Report status

| Status | Meaning | Manual gate |
| --- | --- | --- |
| MATCH | Every equity matches, including two verified empty accounts | Allocation review may continue after verifying provenance |
| REVIEW_REQUIRED | Valid snapshots contain at least one item discrepancy | Stop and review |
| INVALID_INPUT | Incomplete, malformed, duplicate, unsupported or incompatible inputs | Stop; no report files are written |

Read failures name the input side (`broker:` or `memory:`) and cause: file not
found, file read error, encoding error (expected UTF-8), invalid JSON, duplicate
JSON object key, or JSON too deeply nested. Diagnostics omit paths and input data.
If both files are unreadable, the first failure (broker) is reported.

### Item status

| Status | Meaning |
| --- | --- |
| MATCH | Remaining quantity and direction agree |
| BROKER_ONLY | Broker holding has no matching memory position |
| MEMORY_ONLY | Open memory position is absent from broker |
| QUANTITY_MISMATCH | Remaining share counts differ |
| DIRECTION_MISMATCH | Broker and memory sides differ |

Missing quantities and directions are JSON `null` and appear as `-` in Markdown.

Items are sorted by symbol and decimal quantities are emitted as strings without
rounding or tolerance. If direction and quantity both differ, direction takes
precedence; both quantities and directions remain visible in the report.
Exit status is 0 only when `can_continue: true`; discrepancies, invalid inputs or
report-write errors exit 1. Invalid inputs still print a JSON report with
`requires_review: true` and `can_continue: false`. Argument usage errors exit 2.

A MATCH relies on the operator's completeness/account/freshness assertions; the
tool cannot verify live data or detect a deliberately incomplete normalized
export. `can_continue` permits only the **manual allocation review**, never orders
or automatic thesis changes. Repair discrepancies through separately reviewed
broker or trader-memory lifecycle actions, then capture and compare again.

## Preparation status

This is an offline comparison tool plus a documented manual workflow gate.
Automatic broker export, automatic complete memory export/account attribution,
and machine-enforced replay gating remain follow-up work under Issue #493.
The existing `core-portfolio-weekly` replay fixtures demonstrate the earlier
holdings/allocation/dividend/rebalance/journal contracts; they do **not** execute
or verify this new reconciliation gate. Passing those historical replays is
regression evidence only. Keep Issue #493 open until those remaining integration
and end-to-end requirements are verified.

### Referencia: references/rebalancing-strategies.md

# Rebalancing Strategies

This document provides comprehensive guidance on portfolio rebalancing methodologies, timing strategies, tax optimization, and implementation best practices.

## What is Rebalancing?

**Definition:** Rebalancing is the process of realigning portfolio weights back to target allocation by buying and selling assets.

**Purpose:**
1. **Maintain target risk level** - Prevent portfolio from becoming too aggressive or conservative
2. **Enforce discipline** - "Buy low, sell high" systematically
3. **Control concentration** - Prevent winners from creating excessive risk
4. **Optimize diversification** - Maintain intended asset allocation benefits

**Example of Portfolio Drift:**

```
Initial Allocation (Jan 2023):
Stocks: 60% ($60,000)
Bonds: 40% ($40,000)
Total: $100,000

After 1 Year (No Rebalancing):
Stocks: +20% → $72,000 (now 69% of portfolio)
Bonds: +2% → $40,800 (now 31% of portfolio)
Total: $112,800

Result: Portfolio is now riskier than intended (69/31 vs 60/40 target)
```

## Rebalancing Methodologies

### 1. Calendar-Based Rebalancing

**Method:** Rebalance on a fixed schedule regardless of market conditions.

**Common Frequencies:**
- **Monthly:** Very frequent, high transaction costs, rarely needed
- **Quarterly:** Popular for active investors, balances responsiveness with costs
- **Semi-Annually:** Good middle ground, aligns with tax planning
- **Annually:** Simplest, lowest cost, sufficient for buy-and-hold investors

**Pros:**
- Simple and predictable
- Prevents procrastination
- Emotionally easier (mechanical process)
- Can align with tax planning (year-end)

**Cons:**
- May rebalance when not needed (small drifts)
- May not rebalance when urgently needed (between scheduled dates)
- Higher transaction costs if frequent
- Potential tax inefficiency

**Best For:**
- Passive investors
- Tax-advantaged accounts (no tax impact)
- Investors who want simplicity

**Implementation:**
```
Set calendar reminder: Q1 (January), Q2 (April), Q3 (July), Q4 (October)

At each date:
1. Calculate current allocation percentages
2. Compare to target allocation
3. If drift > 5%, rebalance
4. If drift < 5%, skip rebalancing
```

### 2. Threshold-Based Rebalancing

**Method:** Rebalance only when allocation drifts beyond specified threshold.

**Common Thresholds:**
- **Absolute threshold:** Asset class deviates >5 percentage points from target
  - Example: Target 60% stocks, rebalance if <55% or >65%
- **Relative threshold:** Asset class deviates >10-20% from target weight
  - Example: Target 60% stocks, rebalance if <54% (60% × 0.9) or >66% (60% × 1.1)

**Pros:**
- Responsive to market volatility
- Rebalances only when necessary
- Lower transaction costs than calendar-based
- Tax-efficient (fewer trades)

**Cons:**
- Requires monitoring
- Can be psychologically harder (rebalancing during extremes)
- May not rebalance in low-volatility periods (not necessarily bad)

**Best For:**
- Active investors who monitor regularly
- Taxable accounts (minimize turnover)
- Volatile portfolios

**Implementation:**
```
Check allocation monthly or quarterly

Rebalance triggers:
- Stocks: Target 60% ± 5% (rebalance if <55% or >65%)
- Bonds: Target 40% ± 5% (rebalance if <35% or >45%)

Single position triggers:
- Any position >15% → Immediate rebalance
- Any sector >35% → Immediate rebalance
```

### 3. Hybrid Approach (Recommended)

**Method:** Combine calendar and threshold - check on schedule, rebalance only if threshold exceeded.

**Implementation:**
```
Check allocation: Quarterly (Jan, Apr, Jul, Oct)
Rebalance only if: Drift > 5% from target

Example:
Q1 Review: Stocks 62% (target 60%) → Drift 2% → No action
Q2 Review: Stocks 67% (target 60%) → Drift 7% → Rebalance
Q3 Review: Stocks 59% (target 60%) → Drift 1% → No action
Q4 Review: Stocks 71% (target 60%) → Drift 11% → Rebalance
```

**Pros:**
- Best of both worlds
- Disciplined review schedule
- Cost-efficient execution
- Balances responsiveness and simplicity

**Cons:**
- Slightly more complex

**Best For:**
- Most investors
- Both taxable and tax-advantaged accounts

### 4. Cash Flow Rebalancing

**Method:** Use new contributions and withdrawals to rebalance rather than selling.

**Implementation:**
```
Every contribution (monthly, quarterly):
1. Identify underweight asset classes
2. Direct new money to underweight areas
3. Over time, allocation drifts back to target

Example:
Monthly contribution: $1,000
Current allocation: Stocks 67%, Bonds 33% (Target 60/40)
Action: Contribute 100% to bonds until allocation normalizes
```

**Pros:**
- Tax-efficient (no selling, no capital gains)
- No transaction costs
- Psychologically easier (always buying)
- Dollar-cost averaging benefit

**Cons:**
- Slow rebalancing (may take months/years)
- Requires regular contributions
- May not work for large drifts
- Not applicable for retired investors (withdrawing, not contributing)

**Best For:**
- Accumulation phase (regular contributions)
- Taxable accounts
- Small drift corrections

### 5. Tactical Rebalancing

**Method:** Rebalance strategically based on market conditions and valuations, not just drift.

**Factors to Consider:**
- Market valuations (Shiller CAPE, valuation metrics)
- Economic cycle position (early, mid, late expansion)
- Volatility regime (VIX levels)
- Sentiment indicators (put/call ratio, investor surveys)

**Example Tactical Adjustments:**
```
Normal target: 60% stocks, 40% bonds

When stocks expensive (CAPE >30):
Adjust to: 50% stocks, 50% bonds (defensive tilt)

When stocks cheap (CAPE <15):
Adjust to: 70% stocks, 30% bonds (aggressive tilt)
```

**Pros:**
- Can enhance returns vs mechanical rebalancing
- Incorporates market insight
- Responds to changing opportunity sets

**Cons:**
- Requires market timing skill (difficult)
- Risk of being wrong
- Subjective judgment required
- Easy to rationalize not rebalancing

**Best For:**
- Sophisticated investors
- Those with market analysis capability
- Supplement to systematic rebalancing (not replacement)

**Warning:** Tactical rebalancing can become an excuse to avoid rebalancing. Use sparingly and document rationale.

## Rebalancing Across Portfolio Dimensions

### Asset Class Rebalancing

**Most Important:** Stock/Bond/Cash allocation drives risk

**Example:**
```
Target: 70% Stocks, 25% Bonds, 5% Cash
Current: 78% Stocks, 20% Bonds, 2% Cash

Rebalancing trades:
- Sell stocks: $10,000 (reduce from 78% to 70%)
- Buy bonds: $6,000 (increase from 20% to 25%)
- Add to cash: $4,000 (increase from 2% to 5%)
```

**Priority:** High - Asset allocation most important driver of risk/return

### Sector Rebalancing

**Purpose:** Prevent sector concentration, maintain diversification

**Example:**
```
Target Allocation:
- Technology: 25%
- Healthcare: 15%
- Financials: 15%
- Consumer: 15%
- Industrials: 10%
- Other: 20%

Current Allocation (after tech rally):
- Technology: 38% (overweight by 13%)
- Healthcare: 12% (underweight by 3%)
- Financials: 13% (underweight by 2%)
- Others: unchanged

Rebalancing:
- Trim Technology from 38% to 25-28% (sell ~10-13%)
- Add to Healthcare and Financials
```

**Priority:** Medium-High - Sector concentration creates risk

### Position-Level Rebalancing

**Purpose:** Trim individual winners, add to losers (if thesis intact)

**Example:**
```
Target: No position >10%, typical position 5-7%

Current Positions:
- NVDA: 18% (winner, appreciated)
- AAPL: 12% (winner)
- MSFT: 8% (on target)
- Others: <5% each

Rebalancing:
- NVDA: Trim from 18% to 10% (sell 8%)
- AAPL: Trim from 12% to 10% (sell 2%)
- Redeploy 10% to underweight positions
```

**Priority:** High if single position >15%, otherwise Medium

### Geographic Rebalancing

**Example:**
```
Target: 70% US, 20% International Developed, 10% Emerging Markets
Current: 75% US, 18% Int'l Dev, 7% EM (US outperformed)

Rebalancing:
- Sell US equities: 5%
- Buy Int'l Developed: 2%
- Buy Emerging Markets: 3%
```

**Priority:** Low to Medium - Less critical than asset class, but maintains diversification

## Rebalancing Implementation Strategies

### Strategy 1: Full Rebalancing (Precise)

**Method:** Simultaneously buy and sell to restore exact target weights.

**Example:**
```
Portfolio: $200,000
Target: 60% Stocks ($120k), 40% Bonds ($80k)
Current: 68% Stocks ($136k), 32% Bonds ($64k)

Trades:
- Sell stocks: $16,000 (reduce to $120k)
- Buy bonds: $16,000 (increase to $80k)

Result: Exactly 60/40
```

**Pros:**
- Precise restoration of targets
- Immediate rebalancing

**Cons:**
- Transaction costs on both sides
- Tax implications (capital gains on sales)
- Market impact if large trades

**Best For:** Tax-advantaged accounts, large drift corrections

### Strategy 2: Partial Rebalancing

**Method:** Rebalance halfway back to target (or other partial percentage).

**Example:**
```
Portfolio: $200,000
Target: 60% Stocks, 40% Bonds
Current: 68% Stocks, 32% Bonds
Drift: Stocks +8%, Bonds -8%

50% Rebalancing:
- Reduce stock overweight by 50%: 68% → 64% (sell $8k stocks)
- Increase bond underweight by 50%: 32% → 36% (buy $8k bonds)

Result: 64/36 (halfway between current and target)
```

**Pros:**
- Lower transaction costs
- Less tax impact
- Preserves some momentum
- Still reduces risk

**Cons:**
- Doesn't fully restore targets
- May need another rebalance soon

**Best For:** Moderate drifts (5-10%), trending markets, taxable accounts

### Strategy 3: Threshold Rebalancing

**Method:** Only rebalance asset classes that exceed threshold.

**Example:**
```
Thresholds: Rebalance only if drift >5%

Current vs Target:
- Stocks: 68% vs 60% (drift +8%) → Rebalance
- Bonds: 32% vs 40% (drift -8%) → Rebalance
- Cash: 0% vs 0% (no drift) → No action

Only stocks and bonds trade, cash unchanged
```

**Pros:**
- Avoids unnecessary trades
- Cost-efficient

**Cons:**
- Portfolio not perfectly balanced

**Best For:** Most situations

### Strategy 4: Opportunistic Rebalancing

**Method:** Rebalance strategically using market volatility.

**Implementation:**
```
Stocks overweight at 68%:
- Set limit order to sell stocks on strength (e.g., at +2% day)
- Wait for rally to execute

Bonds underweight at 32%:
- Set limit order to buy bonds on weakness (e.g., at -1% day)
- Wait for dip to execute

Result: Better execution prices vs market orders
```

**Pros:**
- Improved execution prices
- "Sell high, buy low" even within rebalancing

**Cons:**
- Delayed execution (orders may not fill)
- Requires active monitoring
- Rebalancing may not complete

**Best For:** Patient investors, non-urgent rebalancing

### Strategy 5: Gradual Rebalancing

**Method:** Rebalance over time in multiple tranches.

**Implementation:**
```
Need to trim stocks by 8%:

Week 1: Sell 2% (1/4 of target)
Week 2: Sell 2%
Week 3: Sell 2%
Week 4: Sell 2%

Total: 8% trimmed over one month
```

**Pros:**
- Reduces market impact
- Dollar-cost averaging effect
- Less stressful (not one big decision)

**Cons:**
- Delayed full rebalancing
- Multiple transaction fees
- Complex to track

**Best For:** Large positions, concentrated portfolios, volatile markets

## Tax-Efficient Rebalancing

### Tax-Loss Harvesting During Rebalancing

**Strategy:** Combine rebalancing with tax-loss harvesting to offset gains.

**Example:**
```
Rebalancing Plan:
- Sell Stock A (winner): +$10,000 gain
- Sell Stock B (loser): -$5,000 loss

Tax Impact:
- Net capital gain: $10,000 - $5,000 = $5,000
- Tax (20% long-term): $5,000 × 0.20 = $1,000
- Effective tax rate on Stock A: $1,000 / $10,000 = 10% (vs 20% without harvesting)

Additional benefit: Harvested loss reduces taxes
```

**Best Practices:**
- Prioritize selling losses to offset rebalancing gains
- Harvest losses in December, rebalance in January (timing)
- Avoid wash sale rule (wait 30 days before repurchasing)

### Tax Lot Management

**Strategy:** Select which shares to sell to minimize taxes.

**Methods:**
1. **Specific Identification:** Choose highest-cost shares (minimize gain)
2. **FIFO (First In, First Out):** Sell oldest shares (often long-term)
3. **LIFO (Last In, First Out):** Sell newest shares (minimize gain)
4. **Highest Cost:** Sell shares with highest cost basis (minimize gain)

**Example:**
```
Need to sell 100 shares of AAPL (currently $180):

Purchase lots:
- Lot A: 50 shares @ $150 (2 years ago) → $1,500 gain → $300 tax
- Lot B: 50 shares @ $170 (6 months ago) → $500 gain → $185 tax (short-term)
- Lot C: 50 shares @ $175 (1 month ago) → $250 gain → $93 tax (short-term)

Best approach: Sell Lot C (minimize tax) or Lot A (long-term rates)

Tax savings: $300 - $93 = $207 vs worst choice
```

### Account Location Strategy

**Strategy:** Rebalance in tax-advantaged accounts when possible.

**Tax Treatment by Account Type:**
- **401(k), IRA, Roth IRA:** No tax on trades (best for rebalancing)
- **Taxable brokerage:** Capital gains tax on sales

**Optimization:**
```
Rebalancing needed: Sell $20,000 stocks, buy $20,000 bonds

Option 1 (Non-optimal):
- Sell stocks in taxable account → Trigger $4,000 capital gain → $800 tax

Option 2 (Optimal):
- Sell stocks in IRA → No tax
- Result: Same allocation, $800 saved

If stocks not held in IRA:
- Sell bonds in IRA, buy stocks in IRA
- Sell stocks in taxable, buy bonds in taxable
- Net effect: Rebalanced, but different holdings per account
```

### Tax-Deferred Rebalancing

**Strategy:** Delay rebalancing to next tax year or until qualifying for long-term rates.

**Example:**
```
Need to rebalance in November:
Current: Stock position 6 months old (short-term gains)
Options:
1. Rebalance now → Short-term capital gains (37% max tax)
2. Wait until January (long-term status) → Long-term gains (20% max tax)

Tax savings: 17 percentage points (depends on income)

Decision factors:
- How urgent is rebalancing? (Risk tolerance)
- How much gain? (Tax dollars at stake)
- Market outlook? (Risk of waiting)
```

## Rebalancing in Different Market Environments

### Bull Market Rebalancing

**Characteristics:**
- Stocks consistently outperforming
- Portfolio drifting more aggressive
- Rebalancing means selling winners

**Strategy:**
- Trim equities back to target regularly
- Don't let greed prevent rebalancing
- "No one went broke taking profits"
- Use proceeds to buy underperforming assets

**Emotional Challenge:** Feels like leaving money on the table

**Discipline Required:** Sell winners even when they're going up

### Bear Market Rebalancing

**Characteristics:**
- Stocks underperforming, declining
- Portfolio drifting more conservative
- Rebalancing means buying stocks

**Strategy:**
- Buy equities to restore target (contrarian)
- "Buy when there's blood in the streets"
- Gradual buying (dollar-cost average into weakness)
- Maintain emotional discipline

**Emotional Challenge:** Buying feels risky when markets falling

**Discipline Required:** Buy when fearful, stick to plan

**Example:**
```
2020 COVID Crash:
March: Stocks down 30%
Portfolio drift: 60/40 → 48/52 (stocks fell, bonds rose)
Rebalancing: Buy stocks (sell bonds)
Result: Bought at bottom, participated in recovery
```

### High Volatility Rebalancing

**Characteristics:**
- Wild market swings
- Frequent drift beyond thresholds
- Risk of over-trading

**Strategy:**
- Widen rebalancing thresholds (e.g., 5% → 7%)
- Use partial rebalancing (50% toward target)
- Gradual rebalancing over time
- Avoid panic-driven trades

**Best Practice:** Don't rebalance daily, stick to schedule

### Low Volatility Rebalancing

**Characteristics:**
- Markets calm, low drift
- Infrequent rebalancing needs

**Strategy:**
- May go 12+ months without rebalancing
- Focus on position-level adjustments
- Opportunistic trimming of winners
- Portfolio construction improvements

## Rebalancing Costs and Break-Even Analysis

### Transaction Costs

**Cost Components:**
1. **Commissions:** $0 at most brokers (2024)
2. **Bid-ask spreads:** 0.01-0.10% for liquid stocks, higher for bonds/ETFs
3. **Market impact:** Minimal for small trades, higher for large positions
4. **Taxes:** Largest cost (15-20% long-term, up to 37% short-term)

**Total Cost Estimate:**
```
Rebalancing $50,000 position:
- Bid-ask spread: $50,000 × 0.05% = $25
- Capital gain: $20,000 (assumes doubled)
- Tax (20% long-term): $20,000 × 0.20 = $4,000

Total cost: $4,025 (8% of trade value)
```

### Break-Even Analysis

**Question:** Does rebalancing benefit outweigh costs?

**Benefits of Rebalancing:**
- Risk reduction (volatility drag reduction)
- "Buy low, sell high" systematic discipline
- Maintain target risk level

**Academic Research:**
- Rebalancing adds 0.3-0.5% annual return (after costs) for 60/40 portfolio
- Benefit higher in volatile markets
- Benefit lower in trending markets

**Rule of Thumb:**
```
Rebalance if:
(Expected Risk Reduction Benefit × Time Horizon) > (Transaction Costs + Tax Costs)

Example:
Expected benefit: 0.4% per year
Time horizon: 10 years
Total benefit: ~4%

Costs: 8% (from example above)

Conclusion: Don't rebalance if costs >4% (wait for long-term rates, use tax-advantaged account, or accept drift)
```

## Rebalancing Checklist

### Quarterly Review Checklist

- [ ] **Calculate Current Allocation**
  - Asset class percentages (stocks, bonds, cash, alternatives)
  - Sector percentages (within equities)
  - Position sizes (% of portfolio)
  - Geographic allocation

- [ ] **Compare to Targets**
  - Asset class drift from target (% points)
  - Sector drift from target
  - Position size vs maximum thresholds
  - Identify overweight and underweight areas

- [ ] **Assess Rebalancing Need**
  - Any drift >5%? (Rebalancing recommended)
  - Any position >15%? (Immediate trim)
  - Any sector >35%? (Immediate trim)
  - Overall risk level vs target

- [ ] **Plan Rebalancing Trades**
  - List positions to sell (overweight)
  - List positions to buy (underweight)
  - Calculate trade sizes ($)
  - Select which account to trade in (tax optimization)

- [ ] **Tax Optimization**
  - Identify tax-loss harvest opportunities
  - Select tax lots (highest cost basis)
  - Consider timing (short-term vs long-term)
  - Estimate tax impact

- [ ] **Execute Rebalancing**
  - Place sell orders (overweight positions)
  - Wait for settlement (T+2)
  - Place buy orders (underweight positions)
  - Verify allocation after trades

- [ ] **Document Decision**
  - Record pre-rebalancing allocation
  - Record trades executed
  - Record post-rebalancing allocation
  - Note any deviations from plan
  - Set next review date

## Summary

**Key Principles:**

1. **Systematic discipline** - Rebalance on schedule or threshold, not emotions
2. **Tax efficiency** - Use tax-advantaged accounts, harvest losses, manage lots
3. **Cost awareness** - Balance rebalancing benefits vs transaction costs
4. **Appropriate frequency** - Quarterly or semi-annually for most investors
5. **Maintain perspective** - Rebalancing is risk management, not return maximization

**Recommended Approach for Most Investors:**

- **Frequency:** Quarterly review, rebalance if drift >5%
- **Method:** Hybrid (calendar + threshold)
- **Implementation:** Full rebalancing in tax-advantaged accounts, partial in taxable
- **Tax optimization:** Harvest losses, select tax lots, time for long-term rates

**Remember:** Rebalancing is a risk management tool, not a performance enhancement technique. The primary goal is to maintain your target risk level and prevent portfolio drift. The discipline of rebalancing enforces "buy low, sell high" behavior that is emotionally difficult but mathematically sound.

### Referencia: references/risk-profile-questionnaire.md

# Risk Profile Questionnaire

This document provides a framework for assessing investor risk tolerance and determining appropriate target asset allocation.

## Overview

Risk profile assessment helps answer:
1. How much volatility can the investor handle emotionally?
2. How much loss can they afford financially?
3. What allocation matches their risk capacity and tolerance?
4. What expected return do they need to meet goals?

**Three Components of Risk Assessment:**

1. **Risk Capacity** - Financial ability to withstand losses (objective)
2. **Risk Tolerance** - Emotional willingness to accept volatility (subjective)
3. **Risk Requirement** - Return needed to achieve goals (objective)

Optimal allocation balances all three components.

## Risk Capacity Assessment (Financial)

Risk capacity is determined by objective financial factors:

### 1. Time Horizon

**Question:** When will you need to withdraw a significant portion of this portfolio?

| Answer | Years | Risk Capacity | Typical Allocation |
|--------|-------|---------------|-------------------|
| **A.** Retired, currently withdrawing | 0-3 | Very Low | 20-30% stocks |
| **B.** Retiring soon | 3-5 | Low | 30-40% stocks |
| **C.** Mid-career, 10-15 years | 10-15 | Medium | 50-70% stocks |
| **D.** Early career, 20+ years | 20-30 | High | 70-85% stocks |
| **E.** Very young, 30+ years | 30+ | Very High | 85-100% stocks |

**Scoring:**
- A = 1 point
- B = 2 points
- C = 3 points
- D = 4 points
- E = 5 points

**Rationale:** Longer time horizons allow recovery from market downturns, supporting higher equity allocation.

### 2. Income Stability

**Question:** How stable and predictable is your income?

| Answer | Risk Capacity Impact |
|--------|---------------------|
| **A.** Fixed pension or annuity (very stable) | Very High (can handle portfolio volatility) |
| **B.** Stable salary, secure job | High |
| **C.** Salary with some variability | Medium |
| **D.** Commission or bonus-heavy | Low |
| **E.** Entrepreneur/self-employed | Low (income correlates with markets) |

**Scoring:**
- A = 5 points
- B = 4 points
- C = 3 points
- D = 2 points
- E = 2 points (or 1 if business is cyclical)

**Rationale:** Stable income allows taking more risk in portfolio; variable income requires conservative portfolio as ballast.

### 3. Net Worth and Liquidity

**Question:** What percentage of your total net worth is this investment portfolio? (Exclude home equity and retirement accounts you can't access)

| Answer | Risk Capacity Impact |
|--------|---------------------|
| **A.** Less than 25% (most wealth elsewhere) | Very High |
| **B.** 25-50% | High |
| **C.** 50-75% | Medium |
| **D.** 75-90% | Low |
| **E.** Over 90% (nearly all wealth) | Very Low |

**Scoring:**
- A = 5 points
- B = 4 points
- C = 3 points
- D = 2 points
- E = 1 point

**Rationale:** If portfolio represents most of your wealth, you can't afford large losses. Diversified wealth allows higher risk in this account.

### 4. Emergency Fund Status

**Question:** Do you have a separate emergency fund (3-6 months expenses) outside this portfolio?

| Answer | Risk Capacity Impact |
|--------|---------------------|
| **A.** Yes, fully funded (6+ months) | High (no need to tap portfolio) |
| **B.** Partially funded (3-4 months) | Medium |
| **C.** No, this portfolio is my emergency fund | Low (need liquidity) |

**Scoring:**
- A = 5 points
- B = 3 points
- C = 1 point

**Rationale:** Emergency fund prevents forced liquidation at market lows; its absence requires higher cash allocation.

### 5. Debt Level

**Question:** What is your debt situation?

| Answer | Risk Capacity Impact |
|--------|---------------------|
| **A.** No debt (or only mortgage) | High |
| **B.** Moderate debt, manageable payments | Medium |
| **C.** High debt, significant payments | Low |
| **D.** High-interest debt (credit cards) | Very Low |

**Scoring:**
- A = 5 points
- B = 3 points
- C = 2 points
- D = 1 point

**Rationale:** High debt reduces capacity to handle portfolio losses; paying down debt may be better use of funds than risky investments.

**Risk Capacity Score (Financial):**
```
Total Points: ___ / 25

20-25 points: Very High Capacity (can handle 80-100% stocks)
15-19 points: High Capacity (60-80% stocks)
10-14 points: Medium Capacity (40-60% stocks)
5-9 points: Low Capacity (20-40% stocks)
0-4 points: Very Low Capacity (0-20% stocks)
```

## Risk Tolerance Assessment (Emotional/Behavioral)

Risk tolerance is subjective - how much volatility can you handle emotionally?

### 1. Loss Reaction

**Question:** If your $100,000 portfolio dropped to $80,000 (-20%) in a market crash, how would you react?

| Answer | Risk Tolerance |
|--------|----------------|
| **A.** Panic, sell everything, can't sleep at night | Very Low |
| **B.** Very concerned, consider selling | Low |
| **C.** Uncomfortable but hold steady | Medium |
| **D.** Stay calm, stick to plan | High |
| **E.** Excited, buy more at lower prices | Very High |

**Scoring:**
- A = 1 point
- B = 2 points
- C = 3 points
- D = 4 points
- E = 5 points

### 2. Historical Behavior

**Question:** Have you experienced a major market downturn (2008, 2020)? How did you react?

| Answer | Risk Tolerance |
|--------|----------------|
| **A.** Sold stocks near the bottom, locked in losses | Very Low |
| **B.** Reduced equity exposure significantly | Low |
| **C.** Held steady, didn't trade | Medium |
| **D.** Held steady and added to stocks | High |
| **E.** Increased equity exposure significantly | Very High |
| **F.** Haven't experienced a major downturn yet | Unknown (rate yourself hypothetically) |

**Scoring:**
- A = 1 point
- B = 2 points
- C = 3 points
- D = 4 points
- E = 5 points
- F = Use answer to Question 1

**Insight:** Past behavior is the best predictor of future behavior. If you sold in prior crashes, you likely will again.

### 3. Sleep Test

**Question:** What is the largest portfolio decline you could tolerate without losing sleep?

| Answer | Drawdown Tolerance | Risk Tolerance | Suitable Allocation |
|--------|-------------------|----------------|---------------------|
| **A.** -5% | Very Low | Very Low | 20% stocks |
| **B.** -10% | Low | Low | 30-40% stocks |
| **C.** -15% | Medium-Low | Medium-Low | 40-50% stocks |
| **D.** -20% | Medium | Medium | 50-60% stocks |
| **E.** -25% | Medium-High | Medium-High | 60-70% stocks |
| **F.** -30% | High | High | 70-80% stocks |
| **G.** -40% or more | Very High | Very High | 80-100% stocks |

**Scoring:**
- A = 1 point
- B = 2 points
- C = 2.5 points
- D = 3 points
- E = 3.5 points
- F = 4 points
- G = 5 points

**Key Insight:** This is the most important question. Be honest - what loss would cause you to sell in panic?

### 4. Investment Timeframe and Patience

**Question:** If your portfolio underperformed the market for 3 years straight, would you:

| Answer | Risk Tolerance |
|--------|----------------|
| **A.** Immediately switch to index funds | Very Low |
| **B.** Re-evaluate and likely make changes within 6 months | Low |
| **C.** Review carefully, make changes if thesis broken | Medium |
| **D.** Stay patient, 3 years is short-term | High |
| **E.** Add more, contrarian opportunity | Very High |

**Scoring:**
- A = 1 point
- B = 2 points
- C = 3 points
- D = 4 points
- E = 5 points

### 5. Volatility Preference

**Question:** Which investment would you prefer?

| Option | Expected Return | Possible Outcomes | Risk Level |
|--------|----------------|-------------------|------------|
| **A.** Conservative | 4% per year | Range: 2% to 6% | Very Low |
| **B.** Moderate | 6% per year | Range: -5% to 15% | Low |
| **C.** Balanced | 8% per year | Range: -10% to 25% | Medium |
| **D.** Growth | 10% per year | Range: -20% to 40% | High |
| **E.** Aggressive | 12% per year | Range: -35% to 60% | Very High |

**Scoring:**
- A = 1 point
- B = 2 points
- C = 3 points
- D = 4 points
- E = 5 points

**Risk Tolerance Score (Emotional):**
```
Total Points: ___ / 25

20-25 points: Very High Tolerance (comfortable with 80-100% stocks)
15-19 points: High Tolerance (comfortable with 60-80% stocks)
10-14 points: Medium Tolerance (comfortable with 40-60% stocks)
5-9 points: Low Tolerance (comfortable with 20-40% stocks)
0-4 points: Very Low Tolerance (comfortable with 0-20% stocks)
```

## Risk Requirement Assessment (Goals)

Risk requirement is determined by what return you need to achieve financial goals.

### 1. Return Needed

**Question:** What annual return do you need to meet your financial goals?

Calculate: Required Return = (Future Goal - Current Savings) / (Years × Current Savings)

Simplified Self-Assessment:

| Required Return | Risk Requirement | Suitable Allocation |
|----------------|-----------------|---------------------|
| **< 4%** | Low (bonds/cash sufficient) | 20-40% stocks |
| **4-6%** | Medium-Low (conservative stocks work) | 40-60% stocks |
| **6-8%** | Medium (balanced portfolio) | 60-70% stocks |
| **8-10%** | Medium-High (equity-heavy) | 70-85% stocks |
| **> 10%** | High (aggressive growth) | 85-100% stocks |

**Scoring:**
- <4% = 1 point
- 4-6% = 2 points
- 6-8% = 3 points
- 8-10% = 4 points
- >10% = 5 points

### 2. Savings Rate

**Question:** Are you contributing regularly to this portfolio?

| Answer | Risk Requirement Impact |
|--------|------------------------|
| **A.** High savings rate (>20% of income) | Low (can achieve goals with lower returns) |
| **B.** Moderate savings rate (10-20%) | Medium |
| **C.** Low savings rate (<10%) | High (need higher returns) |
| **D.** No contributions, portfolio must grow itself | Very High |
| **E.** Net withdrawing from portfolio | N/A (preservation focus) |

**Scoring:**
- A = 1 point (don't need high risk)
- B = 2 points
- C = 4 points (need higher returns)
- D = 5 points
- E = 1 point (focus shifts to preservation)

**Rationale:** High savings rate means goals can be met with lower investment returns; low savings requires taking more risk.

### 3. Goal Flexibility

**Question:** How flexible are your financial goals?

| Answer | Risk Requirement Impact |
|--------|------------------------|
| **A.** Very flexible (can delay retirement, reduce spending) | Low (can afford conservative approach) |
| **B.** Somewhat flexible | Medium |
| **C.** Not flexible (specific retirement date, fixed expenses) | High (must meet return target) |

**Scoring:**
- A = 1 point
- B = 3 points
- C = 5 points

**Risk Requirement Score:**
```
Total Points: ___ / 15

12-15 points: High Requirement (need 70-100% stocks)
9-11 points: Medium-High Requirement (need 60-80% stocks)
6-8 points: Medium Requirement (need 40-60% stocks)
3-5 points: Low Requirement (need 20-40% stocks)
0-2 points: Very Low Requirement (can use conservative allocation)
```

## Synthesizing the Three Assessments

### Step 1: Calculate Component Scores

```
Risk Capacity Score: ___ / 25 → Convert to 1-5 scale = ___
Risk Tolerance Score: ___ / 25 → Convert to 1-5 scale = ___
Risk Requirement Score: ___ / 15 → Convert to 1-5 scale = ___
```

**Conversion Table:**

| Raw Score (out of max) | Converted Score (1-5) |
|------------------------|----------------------|
| 0-20% | 1 |
| 21-40% | 2 |
| 41-60% | 3 |
| 61-80% | 4 |
| 81-100% | 5 |

### Step 2: Determine Overall Risk Profile

**Method 1: Conservative (Recommended for Most Investors)**

Use the **lowest** of the three scores. This ensures you don't take more risk than you can handle.

```
Risk Capacity: 4
Risk Tolerance: 2 ← Lowest
Risk Requirement: 4

Overall Risk Profile: 2 (Low)
Recommended Allocation: 30-40% stocks
```

**Rationale:** If emotional tolerance is low (2), it doesn't matter that capacity and requirement are higher - investor will sell in panic during crash.

**Method 2: Balanced**

Use the **average** of the three scores.

```
Risk Capacity: 4
Risk Tolerance: 2
Risk Requirement: 4

Average: (4 + 2 + 4) / 3 = 3.33 → 3 (Medium)
Recommended Allocation: 50-60% stocks
```

**Rationale:** Balances all factors, may take slightly more risk than emotional tolerance suggests.

**Method 3: Adaptive**

Weight the scores based on individual circumstances:

```
Typical weighting:
Risk Tolerance: 50% (most important - behavioral)
Risk Capacity: 30% (financial constraints)
Risk Requirement: 20% (goals)

Example:
Capacity: 4 × 0.30 = 1.2
Tolerance: 2 × 0.50 = 1.0
Requirement: 4 × 0.20 = 0.8

Weighted Score: 1.2 + 1.0 + 0.8 = 3.0 (Medium)
```

### Step 3: Map to Asset Allocation

| Overall Risk Score | Risk Profile | Recommended Stocks % | Recommended Bonds % |
|-------------------|--------------|---------------------|---------------------|
| **1.0 - 1.5** | Very Low (Conservative) | 20-30% | 60-70% |
| **1.6 - 2.5** | Low (Conservative) | 30-40% | 50-60% |
| **2.6 - 3.5** | Medium (Moderate) | 50-60% | 35-45% |
| **3.6 - 4.5** | High (Growth) | 70-80% | 15-25% |
| **4.6 - 5.0** | Very High (Aggressive) | 85-100% | 0-10% |

### Step 4: Resolve Conflicts

**Conflict Example:**

```
Risk Capacity: 5 (Very High - young, stable income, long horizon)
Risk Tolerance: 2 (Low - can't handle volatility emotionally)
Risk Requirement: 4 (High - need high returns to meet goals)
```

**Resolution:**

This investor **needs** to take risk (requirement), **can** take risk (capacity), but **can't handle** risk emotionally (tolerance).

**Options:**

1. **Conservative approach (Recommended):**
   - Use risk tolerance as limit (30-40% stocks)
   - Accept that goals may not be met with investment returns alone
   - Increase savings rate to compensate for lower returns
   - Work longer or reduce spending goals

2. **Education approach:**
   - Work on improving risk tolerance through education
   - Start with moderate allocation (50% stocks)
   - Gradually increase equity exposure as comfort grows
   - Build tolerance through experience

3. **Mismatch acceptance (Not Recommended):**
   - Use higher allocation (70%+ stocks) despite low tolerance
   - **Risk:** Will likely panic-sell in crash, locking in losses
   - **Outcome:** Worst of both worlds - volatility AND poor returns

**Best Practice:** Never exceed emotional risk tolerance. If goals can't be met with acceptable risk level, adjust goals or increase savings.

## Risk Profile Classification

### Conservative Profile (Risk Score: 1-2)

**Characteristics:**
- Low risk tolerance (can't handle >10-15% loss)
- Near retirement or retired
- Portfolio represents most of wealth
- Needs capital preservation and income

**Recommended Allocation:** 20-40% stocks, 60-80% bonds

**Behavioral Tendencies:**
- May sell stocks during corrections (>10% drop)
- Prefers stability over growth
- Anxious about volatility
- Needs reassurance during downturns

**Management Approach:**
- Conservative allocation with high bond allocation
- Focus on dividend income and bond interest
- Avoid volatile stocks (high-beta tech)
- Regular communication during volatility
- Emphasis on stability and capital preservation

### Moderate Profile (Risk Score: 2.6-3.5)

**Characteristics:**
- Medium risk tolerance (can handle 15-25% loss)
- Mid-career, 10-20 year horizon
- Balanced income and growth needs
- Some anxiety about volatility but can stay the course

**Recommended Allocation:** 50-60% stocks, 35-45% bonds

**Behavioral Tendencies:**
- May consider selling in bear markets but likely holds
- Wants growth but also wants to sleep at night
- Seeks balanced approach
- Needs data and reassurance during volatility

**Management Approach:**
- Balanced portfolio with stock and bond components
- Diversified across sectors and asset classes
- Regular rebalancing to maintain targets
- Education on long-term perspective
- Quarterly reviews with clear communication

### Growth Profile (Risk Score: 3.6-4.5)

**Characteristics:**
- High risk tolerance (can handle 25-35% loss)
- Long time horizon (15-30 years)
- Focus on capital appreciation
- Emotionally stable during volatility

**Recommended Allocation:** 70-80% stocks, 15-25% bonds

**Behavioral Tendencies:**
- Stays invested during downturns
- May add to stocks during corrections
- Comfortable with volatility
- Understands risk/reward tradeoffs

**Management Approach:**
- Equity-heavy portfolio with growth focus
- Diversified across sectors and geographies
- Limited bond allocation (volatility dampening only)
- Emphasis on long-term performance
- Semi-annual or annual reviews

### Aggressive Profile (Risk Score: 4.6-5.0)

**Characteristics:**
- Very high risk tolerance (can handle >35% loss)
- Very long time horizon (25+ years)
- Seeks maximum growth
- Views volatility as opportunity

**Recommended Allocation:** 85-100% stocks, 0-10% bonds

**Behavioral Tendencies:**
- Buys during crashes
- Comfortable with extreme volatility
- Focuses on long-term compounding
- Rational decision-making during panic

**Management Approach:**
- Equity-focused or 100% equity portfolio
- Growth-oriented stock selection
- International and emerging market exposure
- Minimal to no bonds
- Annual reviews with emphasis on strategy

## Questionnaire Summary

Use this simplified questionnaire for quick assessment:

```
INVESTOR RISK PROFILE QUESTIONNAIRE

Name: _______________  Date: _______________

1. Age: ___ → Time horizon: ___ years

2. Investment time horizon before major withdrawal:
   [ ] 0-5 years  [ ] 5-10 years  [ ] 10-20 years  [ ] 20+ years

3. What is the maximum portfolio decline you could tolerate?
   [ ] -5%  [ ] -10%  [ ] -15%  [ ] -20%  [ ] -30%  [ ] -40%+

4. Income stability:
   [ ] Very stable (pension)  [ ] Stable (salary)  [ ] Variable (commission/business)

5. This portfolio represents what % of your net worth?
   [ ] <25%  [ ] 25-50%  [ ] 50-75%  [ ] >75%

6. Emergency fund status:
   [ ] Fully funded (6+ months)  [ ] Partial (3 months)  [ ] None

7. If market crashed 25%, would you:
   [ ] Panic sell  [ ] Sell some  [ ] Hold steady  [ ] Buy more

8. Investment experience with bear markets:
   [ ] Never experienced  [ ] Experienced, sold stocks  [ ] Experienced, held  [ ] Experienced, bought more

9. Return needed to meet goals:
   [ ] <4%  [ ] 4-6%  [ ] 6-8%  [ ] 8-10%  [ ] >10%

10. Primary investment objective:
    [ ] Capital preservation  [ ] Income  [ ] Balanced growth & income  [ ] Growth  [ ] Aggressive growth

SCORING & RECOMMENDATION:

Risk Capacity Score: ___ / 25
Risk Tolerance Score: ___ / 25
Risk Requirement Score: ___ / 15

Overall Risk Profile: [ ] Conservative  [ ] Moderate  [ ] Growth  [ ] Aggressive

Recommended Allocation:
Stocks: ___%
Bonds: ___%
Cash: ___%

Notes:
________________________________________________________________
________________________________________________________________
________________________________________________________________

Advisor Signature: _______________  Client Signature: _______________
```

## Summary

**Key Principles:**

1. **Three-dimensional assessment:** Capacity, Tolerance, Requirement
2. **Tolerance is the constraint:** Never exceed emotional tolerance
3. **Honest self-assessment:** Past behavior predicts future behavior
4. **Resolve conflicts conservatively:** When scores conflict, use lowest
5. **Periodic reassessment:** Risk profile changes with age and circumstances
6. **Allocation must match profile:** Mismatch leads to behavioral errors

**Remember:** The best allocation is one you can stick with through market cycles. It's better to have a moderate allocation you can maintain than an aggressive allocation you'll abandon in a crash. Behavioral discipline matters more than optimal allocation.

### Referencia: references/target-allocations.md

# Target Allocation Models

This document provides model portfolio allocations for different investor risk profiles, serving as benchmarks for portfolio analysis and rebalancing.

## Overview

Target allocations provide a framework for:
1. Assessing if current portfolio matches investor risk tolerance
2. Identifying allocation gaps and concentration risks
3. Guiding rebalancing decisions
4. Setting position sizing guidelines

**Important:** These are templates, not prescriptions. Actual allocations should be customized based on individual circumstances, goals, time horizon, and constraints.

## Investor Risk Profile Classification

### Factors Determining Risk Profile

| Factor | Conservative | Moderate | Growth | Aggressive |
|--------|-------------|----------|--------|------------|
| **Age** | 60+ | 45-60 | 30-45 | <30 |
| **Time Horizon** | 0-5 years | 5-15 years | 15-25 years | 25+ years |
| **Income Stability** | Fixed income (retired) | Stable salary | Growing career | Variable/high |
| **Net Worth** | Low to moderate | Moderate | High | Very high |
| **Loss Tolerance** | Cannot afford >10% loss | Can handle 15-25% loss | Can handle 25-35% loss | Can handle >40% loss |
| **Investment Goal** | Preserve capital, income | Balanced growth & income | Long-term growth | Maximum growth |
| **Market Experience** | Limited | Moderate | Experienced | Very experienced |

**Self-Assessment:**
Rate yourself on each factor, assign the corresponding risk profile, and determine your overall profile based on the majority classification.

## Conservative Portfolio (Capital Preservation)

### Profile
- **Investor:** Near or in retirement, low risk tolerance, need for income and capital preservation
- **Time Horizon:** 0-5 years
- **Max Acceptable Drawdown:** -10 to -15%
- **Expected Annual Return:** 4-6%
- **Expected Volatility:** 6-10%

### Asset Allocation

```
Total Portfolio Allocation:
├── Equities: 30%
│   ├── US Stocks: 20%
│   ├── International Developed: 7%
│   └── Emerging Markets: 3%
├── Fixed Income: 55%
│   ├── Investment Grade Bonds: 30%
│   ├── Government Bonds: 20%
│   └── High Yield Bonds: 5%
├── Cash & Equivalents: 10%
└── Alternatives (Optional): 5%
    ├── REITs: 3%
    └── Gold: 2%
```

### Equity Allocation (30% of total portfolio)

**US Stocks (20% of total, 67% of equity):**

| Sector | % of Total Portfolio | % of US Equity | Characteristics |
|--------|---------------------|----------------|-----------------|
| **Utilities** | 3.5% | 17.5% | High dividends, stable cash flows |
| **Consumer Staples** | 3.0% | 15.0% | Defensive, recession-resistant |
| **Healthcare** | 3.5% | 17.5% | Defensive with growth potential |
| **Financials** | 2.5% | 12.5% | Dividend income, moderate growth |
| **Technology** | 2.5% | 12.5% | Quality large-caps only (AAPL, MSFT) |
| **Communication Services** | 2.0% | 10.0% | Stable cash flows (T, VZ) |
| **Consumer Discretionary** | 1.5% | 7.5% | Underweight cyclicals |
| **Industrials** | 1.0% | 5.0% | Minimal exposure |
| **Real Estate** | 0.5% | 2.5% | Via separate REIT allocation |
| **Energy** | 0% | 0% | Avoid volatility |
| **Materials** | 0% | 0% | Avoid volatility |

**International & Emerging (10% of total, 33% of equity):**
- International Developed: 7% (Europe, Japan, UK - stable, dividend-focused)
- Emerging Markets: 3% (minimal exposure, diversification only)

**Position Sizing:**
- Maximum single position: 5% of total portfolio
- Typical position: 2-3%
- Number of positions: 12-20 stocks OR 4-6 diversified ETFs

**Preferred Holdings:**
- Large-cap dividend aristocrats (25+ years of dividend growth)
- Defensive sectors with recession resistance
- Low beta stocks (β < 0.8)
- Established companies with strong balance sheets

**Example Portfolio (ETF-based):**
- 10% VZ (Verizon) - Telecom, 6% yield
- 10% JNJ (Johnson & Johnson) - Healthcare, dividend aristocrat
- 10% PG (Procter & Gamble) - Consumer staples, stable
- 5% SO (Southern Company) - Utility, high yield
- 5% KO (Coca-Cola) - Consumer staples, dividend
- 5% PFE (Pfizer) - Healthcare, value
- (Or equivalent via dividend-focused ETFs: VYM, SCHD, DVY)

### Fixed Income Allocation (55% of total portfolio)

| Bond Type | % of Total Portfolio | Purpose |
|-----------|---------------------|---------|
| **Investment Grade Corporate** | 30% | Income, moderate risk |
| **US Treasury Bonds** | 15% | Safety, low risk |
| **TIPS (Inflation-Protected)** | 5% | Inflation hedge |
| **High Yield (Junk Bonds)** | 5% | Higher income, higher risk |

**Duration:** Short to intermediate (3-7 years) to reduce interest rate risk

**Example Holdings:**
- AGG (Core Bond ETF)
- BND (Total Bond Market)
- LQD (Investment Grade Corporate)
- TIP (TIPS)
- HYG (High Yield - small allocation)

### Cash & Equivalents (10%)

**Purpose:**
- Emergency liquidity
- Opportunistic buying on dips
- Reduce overall volatility

**Holdings:**
- Money market funds
- Short-term Treasury bills
- High-yield savings accounts

---

## Moderate Portfolio (Balanced Growth & Income)

### Profile
- **Investor:** Mid-career, balanced objectives, moderate risk tolerance
- **Time Horizon:** 5-15 years
- **Max Acceptable Drawdown:** -15 to -25%
- **Expected Annual Return:** 6-8%
- **Expected Volatility:** 10-14%

### Asset Allocation

```
Total Portfolio Allocation:
├── Equities: 60%
│   ├── US Stocks: 42%
│   ├── International Developed: 12%
│   └── Emerging Markets: 6%
├── Fixed Income: 32%
│   ├── Investment Grade Bonds: 20%
│   ├── Government Bonds: 7%
│   └── High Yield Bonds: 5%
├── Cash & Equivalents: 5%
└── Alternatives (Optional): 3%
    ├── REITs: 2%
    └── Commodities/Gold: 1%
```

### Equity Allocation (60% of total portfolio)

**US Stocks (42% of total, 70% of equity):**

| Sector | % of Total Portfolio | % of US Equity | Benchmark (S&P 500) |
|--------|---------------------|----------------|---------------------|
| **Technology** | 11.0% | 26% | 28% |
| **Healthcare** | 7.0% | 17% | 13% |
| **Financials** | 6.0% | 14% | 13% |
| **Consumer Discretionary** | 5.5% | 13% | 11% |
| **Industrials** | 4.0% | 10% | 9% |
| **Consumer Staples** | 3.5% | 8% | 7% |
| **Communication Services** | 2.5% | 6% | 9% |
| **Energy** | 1.0% | 2% | 4% |
| **Utilities** | 1.0% | 2% | 3% |
| **Real Estate** | 0.5% | 1% | 3% |
| **Materials** | 0.5% | 1% | 3% |

**Sector Strategy:**
- Slight overweight in Technology and Healthcare (growth + quality)
- Balanced exposure to Financials and Consumer sectors
- Underweight Energy and Materials (volatility)
- Defensive sectors (Utilities, Staples) lower than conservative portfolio

**International & Emerging (18% of total, 30% of equity):**
- International Developed: 12% (Europe, Japan, UK, Canada)
- Emerging Markets: 6% (China, India, Brazil - growth exposure)

**Position Sizing:**
- Maximum single position: 8% of total portfolio
- High conviction positions: 6-8%
- Medium conviction: 4-6%
- Low conviction: 2-3%
- Number of positions: 15-25 stocks OR 6-10 ETFs

**Market Cap Distribution:**
- Large-cap (>$10B): 70% of US equity
- Mid-cap ($2-10B): 20%
- Small-cap (<$2B): 10%

**Example Portfolio (Individual Stocks):**
- 8% MSFT - Technology, quality growth
- 7% AAPL - Technology, ecosystem
- 6% GOOGL - Technology, advertising
- 6% JNJ - Healthcare, defensive
- 5% JPM - Financials, dividend
- 5% UNH - Healthcare, growth
- 4% V - Financials, payments
- 4% HD - Consumer Discretionary, housing
- 4% DIS - Communication, entertainment
- 3% BA - Industrials, aerospace
- (Additional 15% in 8-10 smaller positions)
- 18% International (VEA, VWO, or individual stocks)

### Fixed Income Allocation (32% of total portfolio)

| Bond Type | % of Total Portfolio | Purpose |
|-----------|---------------------|---------|
| **Investment Grade Corporate** | 20% | Core income, moderate risk |
| **US Treasury Bonds** | 5% | Safety ballast |
| **TIPS** | 2% | Inflation hedge |
| **High Yield Bonds** | 5% | Enhanced income |

**Duration:** Intermediate (5-10 years)

---

## Growth Portfolio (Long-Term Capital Appreciation)

### Profile
- **Investor:** Younger investor, long time horizon, growth-focused
- **Time Horizon:** 15-25 years
- **Max Acceptable Drawdown:** -25 to -35%
- **Expected Annual Return:** 8-10%
- **Expected Volatility:** 14-18%

### Asset Allocation

```
Total Portfolio Allocation:
├── Equities: 80%
│   ├── US Stocks: 52%
│   ├── International Developed: 18%
│   └── Emerging Markets: 10%
├── Fixed Income: 15%
│   ├── Investment Grade Bonds: 8%
│   └── High Yield Bonds: 7%
├── Cash & Equivalents: 3%
└── Alternatives: 2%
    └── REITs or Commodities: 2%
```

### Equity Allocation (80% of total portfolio)

**US Stocks (52% of total, 65% of equity):**

| Sector | % of Total Portfolio | % of US Equity | Notes |
|--------|---------------------|----------------|-------|
| **Technology** | 16.0% | 31% | Growth focus, secular trends |
| **Healthcare** | 8.0% | 15% | Innovation, demographics |
| **Consumer Discretionary** | 7.5% | 14% | Economic growth exposure |
| **Communication Services** | 6.0% | 12% | Digital transformation |
| **Financials** | 5.5% | 11% | Economic expansion |
| **Industrials** | 5.0% | 10% | Capital spending cycles |
| **Consumer Staples** | 2.0% | 4% | Underweight defensive |
| **Energy** | 1.0% | 2% | Minimal exposure |
| **Materials** | 0.5% | 1% | Minimal exposure |
| **Utilities** | 0.5% | 1% | Minimal exposure |
| **Real Estate** | 0% | 0% | Separate REIT allocation |

**Sector Strategy:**
- Heavy overweight Technology (innovation, secular growth)
- Overweight Healthcare (demographics, innovation)
- Growth and cyclical sectors emphasized
- Minimal defensive sectors (don't need stability)

**International & Emerging (28% of total, 35% of equity):**
- International Developed: 18% (quality international growth)
- Emerging Markets: 10% (higher growth potential)

**Position Sizing:**
- Maximum single position: 10% of total portfolio
- High conviction positions: 8-10%
- Medium conviction: 5-7%
- Low conviction: 2-4%
- Number of positions: 15-30 stocks

**Market Cap Distribution:**
- Large-cap: 60% of US equity
- Mid-cap: 25%
- Small-cap: 15% (growth potential)

**Growth vs Value Tilt:** Balanced to slight growth tilt (not extreme)

**Example Portfolio:**
- 10% NVDA - Technology, AI leadership
- 9% MSFT - Technology, cloud + AI
- 8% AAPL - Technology, ecosystem
- 7% GOOGL - Technology, AI + advertising
- 6% AMZN - Consumer Discretionary, AWS
- 6% META - Communication, digital advertising
- 5% TSLA - Consumer Discretionary, EV + energy
- 5% UNH - Healthcare, managed care
- 4% V - Financials, payments
- 4% MA - Financials, payments
- (Remaining 36% in 15-20 smaller positions + international)

### Fixed Income Allocation (15% of total portfolio)

| Bond Type | % of Total Portfolio | Purpose |
|-----------|---------------------|---------|
| **Investment Grade Corporate** | 8% | Moderate income, volatility dampening |
| **High Yield Bonds** | 7% | Enhanced returns, equity-like exposure |

**Duration:** Intermediate to long (7-15 years) - can handle rate risk

---

## Aggressive Portfolio (Maximum Growth)

### Profile
- **Investor:** Young, high income, very high risk tolerance, long horizon
- **Time Horizon:** 20+ years
- **Max Acceptable Drawdown:** -35 to -50%
- **Expected Annual Return:** 9-12%
- **Expected Volatility:** 18-22%

### Asset Allocation

```
Total Portfolio Allocation:
├── Equities: 95%
│   ├── US Stocks: 57%
│   ├── International Developed: 23%
│   └── Emerging Markets: 15%
├── Fixed Income: 0-5%
└── Cash & Equivalents: 0-5%
```

### Equity Allocation (95% of total portfolio)

**US Stocks (57% of total, 60% of equity):**

| Sector | % of Total Portfolio | % of US Equity | Strategy |
|--------|---------------------|----------------|----------|
| **Technology** | 20.0% | 35% | Maximum exposure to innovation |
| **Healthcare** | 9.0% | 16% | Biotech, medical devices, innovation |
| **Consumer Discretionary** | 9.0% | 16% | E-commerce, luxury, travel |
| **Communication Services** | 6.0% | 11% | Digital platforms, streaming |
| **Financials** | 6.0% | 11% | Fintechs, growth-oriented |
| **Industrials** | 4.0% | 7% | Aerospace, automation |
| **Consumer Staples** | 1.0% | 2% | Minimal |
| **Energy** | 1.0% | 2% | Renewables focus |
| **Materials** | 0.5% | 1% | Minimal |
| **Utilities** | 0.5% | 1% | Minimal |

**Sector Strategy:**
- Extreme overweight Technology (35% vs 28% benchmark)
- Growth sectors dominate (80%+ of portfolio)
- Minimal defensive exposure
- Willing to accept high volatility

**International & Emerging (38% of total, 40% of equity):**
- International Developed: 23% (European tech, Asian growth)
- Emerging Markets: 15% (China tech, India growth, LatAm)

**Position Sizing:**
- Maximum single position: 12% of total portfolio
- High conviction positions: 10-12%
- Medium conviction: 6-9%
- Low conviction: 3-5%
- Number of positions: 12-25 stocks (concentrated)

**Market Cap Distribution:**
- Large-cap: 55%
- Mid-cap: 30%
- Small-cap: 15% (higher growth potential, higher risk)

**Growth vs Value:** Strong growth tilt

**Style Characteristics:**
- High P/E ratios acceptable (growth premium)
- Focus on revenue growth over profitability (for some positions)
- Secular themes: AI, cloud, EVs, fintech, biotech
- May include speculative positions (5-10% total)

**Example Portfolio:**
- 12% NVDA - Technology, AI chips
- 10% TSLA - Consumer Discretionary, EVs + autonomy
- 9% MSFT - Technology, cloud + AI
- 8% GOOGL - Technology, AI + advertising
- 8% META - Communication, VR/AI
- 7% AMZN - Consumer Discretionary, AWS
- 6% AAPL - Technology, ecosystem
- 5% SHOP - Technology, e-commerce platform
- 5% SQ - Fintech, payments
- 4% CRSP - Healthcare, gene editing
- 4% ENPH - Energy, solar
- (Remaining 22% in smaller growth positions + international exposure)

### Fixed Income Allocation (0-5% of total portfolio)

**Minimal to none:**
- 0-5% investment grade or cash for liquidity only
- No need for volatility dampening given time horizon
- 100% equity acceptable for this profile

---

## Specialized Allocation Considerations

### Dividend Income Portfolio

**Objective:** Maximize current income while preserving capital

**Allocation:**
- Equities: 60% (dividend-focused)
  - High-yield stocks (4-7% yields): 40%
  - Dividend growth stocks: 20%
- Fixed Income: 30% (income-focused)
  - Investment grade corporate: 15%
  - High yield bonds: 10%
  - Preferred stocks: 5%
- REITs: 10% (high dividends, inflation hedge)

**Target Yield:** 4-6% on total portfolio

### Tax-Efficient Portfolio (Taxable Account)

**Considerations:**
- Minimize turnover (reduce capital gains)
- Favor qualified dividends and long-term gains
- Tax-loss harvesting opportunities
- Municipal bonds (if high tax bracket)

**Allocation Adjustments:**
- Growth stocks (low/no dividends): Higher weight
- Municipal bonds: Replace corporate bonds
- Index funds: Higher weight vs active funds
- International: Lower weight (foreign tax complexity)

### Retirement Portfolio (Post-Retirement)

**Objective:** Generate income, preserve capital, manage longevity risk

**Allocation (varies by age):**
- Age 65: 40/60 stocks/bonds
- Age 75: 30/70 stocks/bonds
- Age 85: 20/80 stocks/bonds

**Income Strategy:**
- 4% withdrawal rate (sustainable)
- Bucket approach:
  - Bucket 1 (0-2 years expenses): Cash
  - Bucket 2 (3-7 years): Bonds
  - Bucket 3 (8+ years): Stocks

---

## Position Sizing Guidelines by Risk Profile

| Risk Profile | Max Single Position | Typical Position | Min # of Stocks | Max # of Stocks |
|--------------|--------------------|--------------------|----------------|----------------|
| **Conservative** | 5% | 2-3% | 12 | 20 |
| **Moderate** | 8% | 4-6% | 15 | 25 |
| **Growth** | 10% | 5-7% | 15 | 30 |
| **Aggressive** | 12% | 6-9% | 12 | 25 |

**Single Sector Maximums:**

| Risk Profile | Max Single Sector |
|--------------|------------------|
| **Conservative** | 25% |
| **Moderate** | 30% |
| **Growth** | 35% |
| **Aggressive** | 40% |

---

## Rebalancing Triggers by Risk Profile

| Risk Profile | Rebalancing Frequency | Asset Class Drift Trigger | Position Drift Trigger |
|--------------|----------------------|--------------------------|------------------------|
| **Conservative** | Quarterly | >3% | >2% |
| **Moderate** | Quarterly | >5% | >3% |
| **Growth** | Semi-Annually | >7% | >4% |
| **Aggressive** | Annually | >10% | >5% |

---

## Lifecycle Allocation (Age-Based)

**Traditional Rule of Thumb:** "120 minus your age" in stocks

| Age | Stock % | Bond % | Formula |
|-----|---------|--------|---------|
| 25 | 95% | 5% | 120 - 25 |
| 35 | 85% | 15% | 120 - 35 |
| 45 | 75% | 25% | 120 - 45 |
| 55 | 65% | 35% | 120 - 55 |
| 65 | 55% | 45% | 120 - 65 |
| 75 | 45% | 55% | 120 - 75 |

**Modern Adjustment:** "130 minus your age" (accounts for longer lifespans, low interest rates)

---

## Using Target Allocations in Portfolio Analysis

### 1. Identify Current Allocation
Calculate actual portfolio percentages across:
- Asset classes (stocks/bonds/cash)
- Sectors (within stocks)
- Geographic regions
- Market caps

### 2. Compare to Target Model
Select appropriate model based on:
- Investor risk tolerance assessment
- Time horizon
- Financial situation
- Goals

### 3. Calculate Deviations
```
Deviation = Current % - Target %

Example:
Target (Moderate): 60% stocks
Current: 68% stocks
Deviation: +8% (overweight stocks)
```

### 4. Generate Rebalancing Plan
- Trim overweight positions/sectors
- Add to underweight positions/sectors
- Prioritize based on magnitude of deviation

### 5. Adjust for Individual Circumstances
Templates are starting points, not rigid rules:
- Tax situation may favor certain holdings
- Unique expertise may justify sector overweight
- Employer stock may create concentration
- Real estate holdings (home) affect allocation

---

## Summary

**Key Takeaways:**

1. **Target allocations are guidelines,** not mandates - customize to individual circumstances
2. **Risk profile drives allocation** - match stocks/bonds to risk tolerance and time horizon
3. **Sector allocation matters** - within equity allocation, sector mix drives risk and return
4. **Position sizing discipline** - enforce maximum position sizes to control concentration
5. **Rebalance systematically** - maintain target allocation over time, don't drift unintentionally
6. **Lifecycle matters** - adjust allocation as you age and circumstances change

**Remember:** The best allocation is one you can stick with through market cycles. Don't choose an aggressive allocation if you'll panic-sell in a 30% drawdown. Match allocation to your true risk tolerance, not your aspirational risk tolerance.


---

## SKILL: portfolio-monitoring

- Fuente: `anthropics/financial-services` → `plugins/agent-plugins/valuation-reviewer/skills/portfolio-monitoring` (Apache-2.0)
- Cuándo usarla: Track and analyze portfolio company performance against plan. Ingests monthly/quarterly financial packages (Excel, PDF), extracts KPIs, flags variances to budget, and produces summary dashboards. Use when reviewing portfolio company financials, preparing board materials, or monitoring covenant compliance. Triggers on "review portfolio company", "monthly financials", "how is [company] performing", "covenant check", or "portfolio update".

# Portfolio Monitoring

## Workflow

### Step 1: Ingest Financial Package

- Accept the user's portfolio company financial package (Excel workbook, PDF, or CSV)
- Extract key financials: Revenue, EBITDA, cash balance, debt outstanding, capex, working capital
- Identify the reporting period and compare to prior period and budget/plan

### Step 2: KPI Extraction & Variance Analysis

Key metrics to track (adapt to the company's sector):

**Financial KPIs:**
- Revenue vs. budget ($ and %)
- EBITDA and EBITDA margin vs. budget
- Cash balance and net debt
- Leverage ratio (Net Debt / LTM EBITDA)
- Interest coverage ratio
- Capex vs. budget
- Free cash flow

**Operational KPIs** (ask user or infer from data):
- Customer count / revenue per customer
- Employee headcount / revenue per employee
- Backlog / pipeline
- Churn / retention rates

### Step 3: Flag & Summarize

- **Green**: Within 5% of plan
- **Yellow**: 5-15% below plan — flag for discussion
- **Red**: >15% below plan or covenant breach risk — immediate attention

Output a concise summary:
1. One-paragraph executive summary ("Company X is tracking [ahead/behind/on] plan...")
2. KPI table with actual vs. budget vs. prior period
3. Red/yellow flags with context
4. Covenant compliance status (if applicable)
5. Questions for management

### Step 4: Trend Analysis

If multiple periods are provided:
- Chart key metrics over time (revenue, EBITDA, cash)
- Identify trends — accelerating, decelerating, or stable
- Compare vs. underwriting case

## Important Notes

- Always ask for the budget/plan to compare against if not provided
- Don't assume sector-specific KPIs — ask what matters for this company
- If covenant levels aren't known, ask the user for the credit agreement terms
- Output should be board-ready — concise, factual, no fluff


---

## SKILL: position-sizer

- Fuente: `tradermonty/claude-trading-skills` → `skills/position-sizer` (MIT)
- Cuándo usarla: Calculate risk-based position sizes for long stock trades. Use when user asks about position sizing, how many shares to buy, risk per trade, Kelly criterion, ATR-based sizing, fractional-share sizing, or portfolio risk allocation. Supports stop-loss distance calculation, volatility scaling, and sector concentration checks.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/position-sizer/` (requirements.txt, position_sizer.py)

# Position Sizer

## Overview

Calculate the optimal number of shares to buy for a long stock trade based on risk management principles. Supports three sizing methods:

- **Fixed Fractional**: Risk a fixed percentage of account equity per trade (default: 1%)
- **ATR-Based**: Use Average True Range to set volatility-adjusted stop distances
- **Kelly Criterion**: Calculate mathematically optimal risk allocation from historical win/loss statistics

All methods apply portfolio constraints (max position %, max sector %) and output a final recommended share count with full risk breakdown. The default output is whole shares. Use `--fractional` only when the user's broker supports fractional shares for the security and order type.

## When to Use

- User asks "how many shares should I buy?"
- User wants to calculate position size for a specific trade setup
- User mentions risk per trade, stop-loss sizing, or portfolio allocation
- User asks about Kelly Criterion or ATR-based position sizing
- User has a small account where whole-share rounding would under-deploy a defined risk budget
- User wants to check if a position fits within portfolio concentration limits

## Prerequisites

- No API keys required
- Python 3.9+ with standard library only

## Workflow

### Step 1: Gather Trade Parameters

Collect from the user:
- **Required**: Account size (total equity)
- **Mode A (Fixed Fractional)**: Entry price, stop price, risk percentage (default 1%)
- **Mode B (ATR-Based)**: Entry price, ATR value, ATR multiplier (default 2.0x), risk percentage
- **Mode C (Kelly Criterion)**: Win rate, average win, average loss; optionally entry and stop for share calculation
- **Stop constraint**: `--stop` must be positive and below `--entry`
- **Optional constraints**: Max position % of account, max sector %, current sector exposure
- **Optional share mode**: Whole shares by default, or fractional shares with `--fractional --share-precision N` when supported by the broker

If the user provides a stock ticker but not specific prices, use available tools to look up the current price and suggest entry/stop levels based on technical analysis.

### Step 2: Execute Position Sizer Script

Run the position sizing calculation:

```bash
# Fixed Fractional (most common)
python3 skills/position-sizer/scripts/position_sizer.py \
  --account-size 100000 \
  --entry 155 \
  --stop 148.50 \
  --risk-pct 1.0 \
  --output-dir reports/

# Fractional shares for small accounts or high-priced stocks
python3 skills/position-sizer/scripts/position_sizer.py \
  --account-size 1000 \
  --entry 155 \
  --stop 148.50 \
  --risk-pct 1.0 \
  --fractional \
  --share-precision 4 \
  --output-dir reports/

# ATR-Based
python3 skills/position-sizer/scripts/position_sizer.py \
  --account-size 100000 \
  --entry 155 \
  --atr 3.20 \
  --atr-multiplier 2.0 \
  --risk-pct 1.0 \
  --output-dir reports/

# Kelly Criterion (budget mode - no entry)
python3 skills/position-sizer/scripts/position_sizer.py \
  --account-size 100000 \
  --win-rate 0.55 \
  --avg-win 2.5 \
  --avg-loss 1.0 \
  --output-dir reports/

# Kelly Criterion (shares mode - with entry/stop)
python3 skills/position-sizer/scripts/position_sizer.py \
  --account-size 100000 \
  --entry 155 \
  --stop 148.50 \
  --win-rate 0.55 \
  --avg-win 2.5 \
  --avg-loss 1.0 \
  --output-dir reports/
```

### Step 3: Load Methodology Reference

Read `references/sizing_methodologies.md` to provide context on the chosen method, risk guidelines, and portfolio constraint best practices.

### Step 4: Calculate Multiple Scenarios

If the user has not specified a single method, run multiple scenarios for comparison:
- Fixed Fractional at 0.5%, 1.0%, and 1.5% risk
- ATR-based at 1.5x, 2.0x, and 3.0x multipliers
- Present a comparison table showing shares, position value, and dollar risk for each

### Step 5: Apply Portfolio Constraints and Determine Final Size

Add constraints if the user has portfolio context:

```bash
python3 skills/position-sizer/scripts/position_sizer.py \
  --account-size 100000 \
  --entry 155 \
  --stop 148.50 \
  --risk-pct 1.0 \
  --max-position-pct 10 \
  --max-sector-pct 30 \
  --current-sector-exposure 22 \
  --output-dir reports/
```

Explain which constraint is binding and why it limits the position.

### Step 6: Generate Position Report

Present the final recommendation including:
- Method used and rationale
- Exact share count and position value
- Dollar risk and percentage of account
- Stop-loss price
- Any binding constraints
- Risk management reminders (portfolio heat, loss-cutting discipline)
- Small-account reminders: fractional shares do not remove broker minimums, spread/slippage, commissions/fees, margin limits, borrow availability, or day-trading controls

## Output Format

In risk-percentage mode (no Kelly inputs), when both `--stop` and `--atr` are supplied, the shares and `final_risk_*` figures follow the ATR-based method (the method that sized the trade); the explicit `--stop` is ignored for risk reporting and the ATR-derived stop appears in `parameters.stop_price`. In Kelly shares mode the stop (or entry price) drives shares and risk instead, and ATR inputs are ignored (Kelly budget mode takes no prices and reports no risk figures). Risk dollars and percentage round half-up (ties report the larger risk).

### JSON Report

```json
{
  "schema_version": "1.0",
  "mode": "shares",
  "parameters": {
    "entry_price": 155.0,
    "account_size": 100000,
    "stop_price": 148.50,
    "risk_pct": 1.0
  },
  "calculations": {
    "fixed_fractional": {
      "method": "fixed_fractional",
      "shares": 153,
      "risk_per_share": 6.50,
      "dollar_risk": 1000.0,
      "stop_price": 148.50
    },
    "atr_based": null,
    "kelly": null
  },
  "constraints_applied": [],
  "final_recommended_shares": 153,
  "final_position_value": 23715.0,
  "final_risk_dollars": 994.50,
  "final_risk_pct": 0.99,
  "binding_constraint": null
}
```

### Markdown Report

Generated automatically alongside the JSON report. Contains:
- Parameters summary
- Calculation details for the active method
- Constraints analysis (if any)
- Final recommendation with shares, value, and risk

Reports are saved to `reports/` with filenames `position_sizer_YYYY-MM-DD_HHMMSS.json` and `.md`.

## Resources

- `references/sizing_methodologies.md`: Comprehensive guide to Fixed Fractional, ATR-based, and Kelly Criterion methods with examples, comparison table, and risk management principles
- `scripts/position_sizer.py`: Main calculation script (CLI interface)

## Key Principles

1. **Survival first**: Position sizing is about surviving losing streaks, not maximizing winners
2. **The 1% rule**: Default to 1% risk per trade; never exceed 2% without exceptional reason
3. **Default to whole shares**: Existing workflows remain integer-share by default
4. **Floor, never round up**: Whole-share mode floors to an integer; fractional mode floors to the requested precision so risk and concentration budgets are not exceeded
5. **Strictest constraint wins**: When multiple limits apply, the tightest one determines final size
6. **Half Kelly**: Never use full Kelly in practice; half Kelly captures 75% of growth with far less risk
7. **Portfolio heat**: Total open risk should not exceed 6-8% of account equity
8. **Intraday rules are broker-specific**: FINRA replaced the old pattern-day-trader day-count and $25,000 minimum-equity requirements with intraday margin standards effective 2026-06-04, with broker phase-in allowed through 2027-10-20. Check the broker's current rules before repeated same-day trading in a margin account.
9. **Asymmetry of losses**: A 50% loss requires a 100% gain to recover; size accordingly

### Referencia: references/sizing_methodologies.md

# Position Sizing Methodologies

## Overview

Position sizing determines how many shares to buy on each trade. Correct sizing is the single most important factor in long-term portfolio survival. A great stock pick with bad sizing can destroy an account; a mediocre pick with proper sizing preserves capital for the next opportunity.

This reference covers three primary methods: Fixed Fractional, ATR-based, and Kelly Criterion. Each has distinct strengths and ideal use cases.

---

## Fixed Fractional Method (Percentage Risk)

### Concept

Risk a fixed percentage of the account on every trade. The most widely used method among professional traders, popularized by Van Tharp and applied rigorously by Mark Minervini and William O'Neil.

### Formula

```
risk_per_share = entry_price - stop_price
dollar_risk    = account_size * risk_pct / 100
shares         = int(dollar_risk / risk_per_share)
```

In the CLI, whole-share mode remains the default and floors to an integer.
When the broker supports fractional shares, `--fractional --share-precision N`
floors to the requested decimal precision instead of rounding up.

### Standard Risk Levels

| Risk % | Trader Profile | Notes |
|--------|---------------|-------|
| 0.25-0.50% | Conservative / large account | Institutional-grade risk |
| 0.50-1.00% | Experienced swing trader | Minervini recommended range |
| 1.00-1.50% | Active trader, proven edge | Standard for tested systems |
| 1.50-2.00% | Aggressive, high win-rate | Maximum for most strategies |
| > 2.00% | Dangerous | Ruin risk increases rapidly |

### Example

- Account: $100,000
- Entry: $155.00, Stop: $148.50
- Risk per share: $6.50
- At 1% risk: $1,000 / $6.50 = **153 shares**
- Position value: $23,715 (23.7% of account)

### When to Use

- Default method for most swing and position trades
- When you have a clear technical stop level (support, moving average, prior low)
- When trading a system with established risk parameters
- When a small account or high-priced stock would otherwise round the position to zero shares, provided the broker supports fractional trading for that security and order type

### Fractional-Share Mode

Fractional shares can make the risk budget usable for small accounts, high-priced stocks, or very tight risk budgets:

```bash
python3 skills/position-sizer/scripts/position_sizer.py \
  --account-size 1000 \
  --entry 155 \
  --stop 148.50 \
  --risk-pct 1.0 \
  --fractional \
  --share-precision 4 \
  --output-dir reports/
```

With the inputs above, the risk budget is $10 and risk per share is $6.50.
Whole-share mode returns 1 share. Fractional mode floors to 1.5384 shares,
keeping risk at or below the $10 budget while using more of the account's
intended risk allocation.

Use fractional mode as a sizing calculation, not as broker permission. Brokers
can impose minimum order sizes, limited fractional support by security or order
type, wider effective spreads for small notional orders, margin restrictions,
and different tax-lot behavior.

### Minervini / O'Neil Integration

Mark Minervini recommends:
- Risk no more than 1% per trade during the early stages of a rally
- Tighten to 0.5% after consecutive losses
- Use a "progressive exposure" model: start with half position, add on confirmation
- Maximum portfolio heat (total open risk): 6-8%

William O'Neil recommends:
- Cut losses at 7-8% below purchase price (hard maximum)
- Preferred loss cut: 3-5% for experienced traders
- Use a "follow-through day" to confirm market direction before increasing exposure

---

## ATR-Based Method (Volatility Sizing)

### Concept

Use the Average True Range (ATR) to set stop distance, automatically adjusting position size to a stock's volatility. Originated with the Turtle Traders (Richard Dennis, 1983).

### Formula

```
stop_distance  = atr * atr_multiplier
stop_price     = entry_price - stop_distance
risk_per_share = stop_distance
dollar_risk    = account_size * risk_pct / 100
shares         = int(dollar_risk / risk_per_share)
```

### ATR Multiplier Guidance

When both a stop price and ATR inputs are provided in risk-percentage mode, sizing and the reported risk (`final_risk_*`) follow the ATR-based method — the method that set the share count — and the explicit stop is ignored for risk reporting. In Kelly shares mode the stop (or entry price) drives shares and risk instead, and ATR inputs are ignored (Kelly budget mode takes no prices and reports no risk figures). Risk dollars and percentage round half-up (ties report the larger risk); other rounded outputs in this skill use Python's default half-even `round()`, and only `final_risk_*` rounds half-up by design.

| Multiplier | Stop Width | Style |
|-----------|-----------|-------|
| 1.0x | Tight | Day trading, very short-term |
| 1.5x | Moderate-tight | Swing trading, 2-5 day holds |
| 2.0x | Standard | Default for most swing trades (Turtle Traders) |
| 2.5x | Wide | Position trading, 2-8 week holds |
| 3.0x | Very wide | Trend following, multi-month holds |

### Example

- Account: $100,000, Risk: 1%
- Entry: $155.00, ATR(14) = $3.20, Multiplier = 2.0x
- Stop distance: $6.40, Stop: $148.60
- Dollar risk: $1,000
- Shares: int($1,000 / $6.40) = **156 shares**

### When to Use

- When you want volatility-adjusted sizing across different stocks
- When a stock lacks clear support/resistance for a discrete stop
- For systematic/mechanical trading systems
- When comparing positions across stocks with different price ranges and volatilities

### Advantages Over Fixed Stop

1. Low-volatility stocks get larger positions (tighter stop relative to price)
2. High-volatility stocks get smaller positions (wider stop protects against noise)
3. Normalizes risk across the portfolio regardless of stock price

---

## Kelly Criterion

### Concept

The Kelly Criterion calculates the mathematically optimal fraction of capital to risk, given known win rate and payoff ratio. Developed by John L. Kelly Jr. (1956) at Bell Labs.

### Formula

```
R         = avg_win / avg_loss       (payoff ratio)
kelly_pct = W - (1 - W) / R          (full Kelly percentage)
half_kelly = kelly_pct / 2            (practical recommendation)
```

Where W = historical win rate (0 to 1).

### Full Kelly vs. Half Kelly

**Full Kelly** maximizes long-term geometric growth but produces extreme volatility. Drawdowns of 50%+ are common. No professional fund uses full Kelly.

**Half Kelly** achieves approximately 75% of the theoretical growth rate with dramatically lower drawdowns. This is the standard recommendation for real trading.

| Metric | Full Kelly | Half Kelly | Quarter Kelly |
|--------|-----------|-----------|---------------|
| Growth rate | 100% | ~75% | ~50% |
| Max drawdown | Severe (50%+) | Moderate (25-35%) | Mild (15-20%) |
| Practical use | Never | Aggressive | Conservative |

### Example

- Win rate: 55%, Avg win: $2.50, Avg loss: $1.00
- R = 2.5 / 1.0 = 2.5
- Kelly = 0.55 - 0.45 / 2.5 = 0.55 - 0.18 = 0.37 = **37%**
- Half Kelly = **18.5%**
- On $100,000 account: risk budget = $18,500

### Negative Expectancy

When the Kelly formula produces a negative value, the system has negative expected value. The Kelly percentage is floored at 0%, meaning "do not trade this system."

Example:
- Win rate: 30%, Avg win: $1.00, Avg loss: $1.50
- R = 1.0 / 1.5 = 0.667
- Kelly = 0.30 - 0.70 / 0.667 = 0.30 - 1.05 = **-0.75** -> floored to **0%**

### Two Modes of Use

1. **Budget Mode** (no entry price): Returns a recommended risk budget as a percentage of account. Useful for capital allocation planning before identifying specific entries.

2. **Shares Mode** (with entry and stop): Converts the half-Kelly budget into a specific share count using the entry/stop distance.

### When to Use

- When you have reliable historical win rate and payoff statistics (100+ trades minimum)
- For portfolio-level capital allocation across multiple strategies
- As a ceiling check: "Am I risking more than Kelly suggests?"
- Not suitable for discretionary traders without track records

---

## Portfolio Constraints

### Maximum Position Size

Limit any single position to a percentage of account value:

```
max_shares = int(account_size * max_position_pct / 100 / entry_price)
```

**Guidelines:**
- 5-10%: Conservative (diversified portfolio, 10-20 positions)
- 10-15%: Moderate (concentrated portfolio, 7-10 positions)
- 15-25%: Aggressive (high-conviction portfolio, 4-7 positions)
- > 25%: Speculative (not recommended for most traders)

### Sector Concentration

Limit total exposure to any single sector:

```
remaining_pct = max_sector_pct - current_sector_exposure
remaining_dollars = remaining_pct / 100 * account_size
max_shares = int(remaining_dollars / entry_price)
```

**Guidelines:**
- Individual stock: 5-10% of portfolio
- Single sector: 25-30% maximum
- Correlated positions: Treat as a single exposure

### Position Count and Diversification

| Positions | Diversification | Notes |
|-----------|----------------|-------|
| 1-4 | Very concentrated | High volatility, requires high conviction |
| 5-10 | Focused | Sweet spot for active traders |
| 10-20 | Diversified | Diminishing returns above 15 |
| 20+ | Over-diversified | Dilutes edge, approaches index performance |

Research shows that beyond 20 uncorrelated positions, additional diversification benefit is minimal. For active traders, 5-10 positions with proper sizing often produces better risk-adjusted returns than 20+ positions with diluted conviction.

### Binding Constraint Logic

When multiple constraints apply, the strictest (minimum share count) wins. The position sizer identifies which constraint is "binding" so the trader understands what limits the position.

Priority order:
1. Risk-based shares (from Fixed Fractional, ATR, or Kelly)
2. Max position % limit
3. Max sector % limit
4. Final = minimum of all candidates

---

## Method Comparison

| Feature | Fixed Fractional | ATR-Based | Kelly Criterion |
|---------|-----------------|-----------|-----------------|
| Input needed | Entry, stop, risk % | Entry, ATR, multiplier, risk % | Win rate, avg win/loss |
| Adjusts for volatility | No | Yes | No (uses historical stats) |
| Requires track record | No | No | Yes (100+ trades) |
| Best for | Discretionary trades | Systematic/mechanical | Capital allocation |
| Complexity | Low | Medium | Medium |
| Typical use | Primary sizing | Primary sizing | Ceiling check / allocation |
| Stop determined by | Chart analysis | ATR calculation | External (chart or ATR) |

### Recommended Workflow

1. **Start with Fixed Fractional** at 1% risk for new strategies or market conditions
2. **Switch to ATR-based** when comparing opportunities across different volatility profiles
3. **Use Kelly as a ceiling** after accumulating 100+ trade records
4. **Always apply constraints** (position limit, sector limit) as a final filter
5. **Reduce risk** after consecutive losses (Minervini's "progressive exposure" in reverse)

---

## Risk Management Principles

### The 1% Rule

Never risk more than 1% of account equity on a single trade. This ensures survival through inevitable losing streaks:

- 10 consecutive losses at 1% = 9.6% drawdown (recoverable)
- 10 consecutive losses at 5% = 40.1% drawdown (devastating)
- 10 consecutive losses at 10% = 65.1% drawdown (account-threatening)

### Portfolio Heat

Total open risk across all positions should not exceed 6-8% of account:

```
portfolio_heat = sum(shares_i * risk_per_share_i) / account_size * 100
```

If portfolio heat exceeds 8%, do not add new positions until existing trades are moved to breakeven or closed.

### Small-Account Friction

For small accounts, the calculated risk budget can be smaller than the
practical cost of trading. Before accepting a position size, check:

- Bid/ask spread as a percentage of notional value
- Commission, regulatory, platform, or currency-conversion fees
- Slippage on marketable orders
- Broker minimum order value and fractional-share support
- Margin eligibility, borrow availability for shorts, and settlement rules

If these costs consume a meaningful share of planned risk, reduce frequency,
raise the setup-quality bar, use wider time frames, or skip the trade.

### Intraday Margin and Day-Trading Controls

Do not treat the legacy "$25,000 pattern day trader" rule as the only current
constraint. FINRA Notice 26-10 replaced the old day-trading margin requirements,
including the pattern-day-trader day-count and $25,000 minimum-equity
requirements, with new intraday margin standards effective 2026-06-04. FINRA
allows firms to phase in implementation through 2027-10-20, so the practical
rule a trader experiences can still vary by broker during the transition.

Source: https://www.finra.org/rules-guidance/notices/26-10

### Asymmetry of Losses

Losses require disproportionately larger gains to recover:

| Loss | Gain to Recover |
|------|----------------|
| 10% | 11.1% |
| 20% | 25.0% |
| 30% | 42.9% |
| 50% | 100.0% |
| 75% | 300.0% |

This asymmetry is why position sizing and loss cutting are more important than stock selection.


---

## SKILL: position-sizing

- Fuente: `agiprolabs/claude-trading-skills` → `skills/position-sizing` (MIT)
- Cuándo usarla: Trade sizing methods including fixed fractional, volatility-adjusted, Kelly criterion, and liquidity-constrained sizing
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/position-sizing/` (portfolio_sizer.py, size_calculator.py)

# Position Sizing

Position sizing is the single most important risk management decision in trading. Your entry signal determines direction; your position size determines survival. A mediocre strategy with proper sizing will outperform a great strategy with reckless sizing over any meaningful time horizon.

**Core principle**: Size determines survival, not entries. Two traders with the same signals but different sizing will have wildly different outcomes. The one who sizes conservatively survives drawdowns and compounds capital; the one who oversizes blows up.

## Methods Covered

| Method | Best For | Key Input |
|--------|----------|-----------|
| Fixed Fractional | General trading, most recommended | Account risk % |
| Volatility-Adjusted | Volatile markets, multi-asset | ATR or realized vol |
| Kelly Criterion | Quantified edge with track record | Win rate + payoff ratio |
| Liquidity-Constrained | Low-liquidity Solana tokens | Pool depth |
| Anti-Martingale | Trend-following strategies | Recent P&L streak |

---

## 1. Fixed Fractional Sizing

The most recommended method for most traders. Risk a fixed percentage of your account on each trade.

### Formula

```
risk_amount = account_value * risk_percentage
price_risk_per_unit = entry_price - stop_loss_price
position_size_units = risk_amount / price_risk_per_unit
position_value = position_size_units * entry_price
```

### Risk Tiers

| Tier | Risk Per Trade | Use Case |
|------|---------------|----------|
| Conservative | 0.5–1% | New strategies, drawdown recovery |
| Standard | 1–2% | Most traders, proven strategies |
| Aggressive | 3–5% | High-conviction setups with strong, measured edge |

### Example

```python
account = 10_000  # $10,000 or 100 SOL
risk_pct = 0.02   # 2%
entry = 1.50
stop_loss = 1.30

risk_amount = account * risk_pct          # $200
price_risk = entry - stop_loss            # $0.20
position_units = risk_amount / price_risk # 1,000 tokens
position_value = position_units * entry   # $1,500
```

With this sizing, if the stop loss is hit, you lose exactly 2% of your account regardless of the token's price or volatility.

---

## 2. Volatility-Adjusted Sizing

Scale position size inversely with volatility. When volatility is high, take smaller positions; when low, take larger positions. This normalizes the dollar risk across different market conditions.

### Formula

```
adjusted_size = base_size * (target_vol / current_vol)
```

Where:
- `target_vol`: your desired daily portfolio volatility (e.g., 2%)
- `current_vol`: the token's current daily volatility (from ATR or realized vol)

### Using ATR

```python
atr_14 = 0.12          # 14-period ATR
close_price = 1.50
daily_vol_pct = atr_14 / close_price  # 8%

target_daily_vol = account * 0.02      # $200 target daily move
position_size = target_daily_vol / atr_14  # 1,667 units
```

This automatically reduces exposure in volatile markets and increases it in calm ones.

---

## 3. Kelly Criterion

The mathematically optimal fraction of capital to risk, maximizing long-term growth rate. Derived from maximizing expected logarithmic utility.

### Formula

```
f* = (p * b - q) / b
```

Where:
- `p` = win rate (probability of winning trade)
- `q` = 1 - p (probability of losing trade)
- `b` = average win / average loss (payoff ratio)
- `f*` = optimal fraction of capital to risk

Equivalent form: `f* = (p * (b + 1) - 1) / b`

### Critical Rule: NEVER Use Full Kelly

Full Kelly assumes perfect knowledge of your edge. In practice, edge estimates are noisy. Always use fractional Kelly:

| Fraction | Use Case | Notes |
|----------|----------|-------|
| 0.25x Kelly | Conservative, recommended default | Robust to edge estimation error |
| 0.50x Kelly | Moderate, for well-measured edges | Still significant drawdown risk |
| 1.0x Kelly | Never in practice | Theoretical maximum, catastrophic if edge is overestimated |

### Example

```python
win_rate = 0.55       # 55% win rate
avg_win = 2.0         # Average win is 2x the average loss
avg_loss = 1.0
payoff_ratio = avg_win / avg_loss  # b = 2.0

kelly = (win_rate * payoff_ratio - (1 - win_rate)) / payoff_ratio
# kelly = (0.55 * 2.0 - 0.45) / 2.0 = 0.325 = 32.5%

quarter_kelly = kelly * 0.25  # 8.1% — use this
half_kelly = kelly * 0.50     # 16.25%
```

**If Kelly is negative, you have no edge. Do not trade.**

See `references/sizing_formulas.md` for the full mathematical derivation.

---

## 4. Liquidity-Constrained Sizing

Critical for Solana tokens. Even if your risk model says you can take a large position, the pool may not support it without unacceptable slippage.

### Formula (Constant-Product AMM)

```
slippage ≈ trade_size / pool_liquidity
max_trade = pool_liquidity * max_slippage_pct
```

### Rules of Thumb

| Constraint | Guideline |
|-----------|-----------|
| Max single trade | 2% of pool liquidity |
| Max position | 5% of pool liquidity |
| Minimum pool depth | 10x your desired position size |

### Example

```python
pool_sol = 500          # 500 SOL in pool
max_slippage = 0.02     # 2% max slippage

max_trade_sol = pool_sol * max_slippage  # 10 SOL
# For a $150 SOL price, that's $1,500 max per trade
```

**Always check all pools**, not just the largest. Aggregate liquidity across Raydium, Orca, and Meteora for the full picture. See the `liquidity-analysis` skill for pool depth assessment.

---

## 5. Anti-Martingale Sizing

Increase size after wins, decrease after losses. This is the opposite of the gambler's fallacy (Martingale). The logic: winning streaks may indicate your strategy is in sync with the market; losing streaks may indicate regime change.

### Implementation

```python
def anti_martingale_size(
    base_size: float,
    consecutive_wins: int,
    consecutive_losses: int,
    scale_factor: float = 0.25,
    max_multiplier: float = 2.0,
    min_multiplier: float = 0.5,
) -> float:
    if consecutive_losses > 0:
        multiplier = max(min_multiplier, 1.0 - consecutive_losses * scale_factor)
    elif consecutive_wins > 0:
        multiplier = min(max_multiplier, 1.0 + consecutive_wins * scale_factor)
    else:
        multiplier = 1.0
    return base_size * multiplier
```

Use conservatively. After 3+ consecutive losses, reducing size by 50% protects capital during drawdowns.

---

## Position Sizing Ladder

Combine all methods and take the most conservative result:

```
1. Calculate Kelly size          → theoretical max based on edge
2. Calculate fixed fractional    → risk-based size
3. Calculate volatility-adjusted → vol-normalized size
4. Calculate liquidity-constrained max → market-based ceiling
5. Final size = min(all four)    → binding constraint wins
```

The binding constraint tells you what is limiting your size:
- **Kelly-bound**: your edge is small, size accordingly
- **Risk-bound**: standard risk management is the limit
- **Volatility-bound**: market is too volatile for larger size
- **Liquidity-bound**: pool cannot absorb more without slippage

---

## Account-Level Limits

Individual position sizing is necessary but not sufficient. You also need portfolio-level constraints:

| Limit | Guideline | Rationale |
|-------|-----------|-----------|
| Max single position | 10% of portfolio | Diversification floor |
| Max correlated exposure | 25% of portfolio | Correlated assets move together |
| Max total exposure | 50–80% of portfolio | Cash reserve for opportunities/margin |
| Max positions | 5–10 concurrent | Attention and management bandwidth |

---

## PumpFun / Meme Token Sizing

PumpFun and early-stage meme tokens require special sizing discipline:

- **Very small positions**: 0.1–1 SOL per trade due to extreme risk
- **Scale with bonding curve fill %**: smaller when early (high rug risk), slightly larger when proven (graduated to Raydium)
- **Never size based on expected return** — size based on acceptable total loss
- **Treat as lottery tickets**: expect most to go to zero
- **Position limit**: no more than 5–10% of portfolio across all meme positions combined

```python
# PumpFun sizing example
account_sol = 100
meme_budget = account_sol * 0.05   # 5 SOL total for memes
per_trade = meme_budget / 10       # 0.5 SOL each, 10 shots
```

---

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| `risk-management` | Portfolio-level limits, drawdown rules |
| `liquidity-analysis` | Pool depth data for liquidity constraints |
| `kelly-criterion` | Deeper Kelly math, edge estimation |
| `exit-strategies` | Stop loss placement affects fixed fractional sizing |
| `volatility-modeling` | Better vol estimates for volatility-adjusted sizing |
| `slippage-modeling` | Precise slippage estimates for liquidity constraints |

---

## Files

### References
- `references/sizing_formulas.md` — Mathematical derivations for all sizing methods with worked examples
- `references/practical_guide.md` — Sizing by account size, token type, and common mistakes

### Scripts
- `scripts/size_calculator.py` — Calculates position size using all methods, shows binding constraint
- `scripts/portfolio_sizer.py` — Portfolio risk dashboard with per-position risk and available budget

---

## Quick Reference

```python
# Minimal fixed fractional sizing — copy-paste starter
def calc_position_size(
    account: float, risk_pct: float, entry: float, stop: float
) -> float:
    """Return number of units to buy."""
    risk_amount = account * risk_pct
    price_risk = abs(entry - stop)
    if price_risk == 0:
        return 0.0
    return risk_amount / price_risk
```

### Referencia: references/practical_guide.md

# Position Sizing — Practical Guide

Actionable sizing guidelines by account size, token type, and situation. Covers common mistakes and adjustment rules.

---

## Sizing by Account Size

### Micro Accounts (<$1K / <7 SOL)

- **Fixed amount per trade**: 0.05–0.1 SOL
- **Focus**: Learning, not profit. Treat as tuition.
- **Max concurrent positions**: 3
- **Total exposure**: up to 80% (small accounts need concentration)
- **Key rule**: Never deposit more to "average down"

### Small Accounts ($1K–$10K / 7–70 SOL)

- **Risk per trade**: 1–2% of account
- **Max concurrent positions**: 5
- **Max single position**: 10% of account
- **Total exposure**: 50–70%
- **Key rule**: Fees matter — avoid tokens with wide spreads

### Medium Accounts ($10K–$100K / 70–700 SOL)

- **Risk per trade**: 0.5–1% of account
- **Max concurrent positions**: 7–10
- **Max single position**: 8% of account
- **Total exposure**: 40–60%
- **Key rule**: Start considering liquidity constraints on smaller tokens

### Large Accounts (>$100K / >700 SOL)

- **Risk per trade**: 0.25–0.5% of account
- **Max concurrent positions**: 10–15
- **Max single position**: 5% of account
- **Total exposure**: 30–50%
- **Key rule**: Liquidity is your primary constraint. Split entries across time.

---

## Sizing by Token Type

### Blue Chip (SOL, ETH, BTC)

- **Max position size**: up to 10% of portfolio
- **Sizing method**: Fixed fractional or volatility-adjusted
- **Typical ATR daily vol**: 3–6%
- **Liquidity constraint**: rarely binding (deep pools)
- **Stop loss distance**: 5–10% from entry typical

### Mid-Cap (Top 100 — JUP, BONK, WIF, PYTH)

- **Max position size**: up to 5% of portfolio
- **Sizing method**: Fixed fractional with liquidity check
- **Typical ATR daily vol**: 5–15%
- **Liquidity constraint**: check for accounts >$50K
- **Stop loss distance**: 8–15% from entry typical

### Small-Cap (Top 500)

- **Max position size**: up to 2% of portfolio
- **Sizing method**: Fixed fractional, liquidity-constrained
- **Typical ATR daily vol**: 10–30%
- **Liquidity constraint**: almost always binding
- **Stop loss distance**: 15–25% from entry typical

### PumpFun / Meme / Micro-Cap

- **Max position size**: 0.5–1% of portfolio per token
- **Max total meme allocation**: 5–10% of portfolio
- **Sizing method**: Fixed amount (lottery ticket sizing)
- **Typical ATR daily vol**: 30–100%+
- **Liquidity constraint**: always binding
- **Stop loss**: assume 100% loss is possible; size accordingly

---

## When to Adjust Sizing

### Reduce Size

| Trigger | Action | Rationale |
|---------|--------|-----------|
| 3 consecutive losses | Reduce to 50% normal size | Possible regime change |
| Drawdown > 10% from peak | Reduce to minimum size | Capital preservation mode |
| New/untested strategy | Start at 25% normal size | Earn the right to full size |
| Market volatility spike (VIX-like) | Reduce by vol ratio | Same dollar risk needs less exposure |
| Unusual correlation across positions | Cut weakest positions | Correlated risk compounds |

### Increase Size (Cautiously)

| Trigger | Action | Rationale |
|---------|--------|-----------|
| 50+ trade track record with edge | Scale from 25% to 100% over time | Statistical confidence |
| Win streak > 5 | Allow up to 1.5x normal size | Strategy may be in sync |
| Low volatility regime | Vol-adjusted increase is mechanical | Same risk, larger notional |
| Account growth milestone | Recalculate base size upward | Compound growth |

### Never Increase Size When

- Trying to recover from losses ("revenge trading")
- A single trade seems like a "sure thing" (no such thing)
- You haven't adjusted stops to match the larger size
- Your recent win streak is < 10 trades (not statistically significant)

---

## Position Sizing Mistakes

### 1. Sizing Based on Conviction

**Wrong**: "I'm really confident in this trade, so I'll 5x my normal size."

**Right**: Let the math decide. Conviction is emotional, not quantitative. If you have a measured edge that justifies larger size, the Kelly formula will tell you.

### 2. Not Accounting for Fees and Slippage

**Wrong**: Calculating stop distance as `entry - stop` only.

**Right**: Include round-trip fees (0.3–0.6% typical) and expected slippage (0.1–2% depending on token) in your risk calculation.

### 3. Ignoring Correlation Between Positions

**Wrong**: "I'm risking 2% on each of 10 positions = 20% max risk."

**Right**: If 8 of those positions are meme tokens that all dump together, your effective risk is closer to 16% in a single correlated move. Account for correlation in portfolio limits.

### 4. Increasing Size to Make Back Losses

**Wrong**: After a 10% drawdown, doubling size to "get back to even faster."

**Right**: Reduce size during drawdowns. You need to earn back losses with smaller, consistent gains. The math: a 10% loss needs 11.1% gain to recover; a 50% loss needs 100%.

### 5. Using Position Size as Stop Loss

**Wrong**: "I'll just buy a small amount so if it goes to zero it's fine."

**Right**: Always use an explicit stop loss. "Small size, no stop" leads to holding worthless positions that tie up capital. Exception: PumpFun lottery tickets explicitly sized for 100% loss.

### 6. Not Adjusting for Timeframe

**Wrong**: Using the same 2% risk for a 5-minute scalp and a multi-week swing trade.

**Right**: Shorter timeframes need tighter stops relative to volatility, which means either smaller position sizes or accepting more noise. Scale risk per trade with expected hold time.

### 7. Forgetting Portfolio-Level Limits

**Wrong**: Each trade is individually sized, but no check on total exposure.

**Right**: Before each new position, verify:
- Total portfolio exposure is within limits
- Correlated exposure is within limits
- Total risk-on (sum of all position risks) is acceptable

---

## Quick Decision Tree

```
Want to enter a trade?
│
├─ Do you have a measured edge (50+ trades)?
│  ├─ Yes → Calculate Kelly size (use 0.25x)
│  └─ No  → Use fixed fractional (1% risk)
│
├─ Calculate fixed fractional size
│
├─ Is the token volatile (ATR > 10% daily)?
│  ├─ Yes → Also calculate vol-adjusted size
│  └─ No  → Skip vol adjustment
│
├─ Is pool liquidity < 50x your desired position?
│  ├─ Yes → Calculate liquidity-constrained max
│  └─ No  → Liquidity is not binding
│
├─ Take minimum of all calculated sizes
│
├─ Check portfolio limits:
│  ├─ Single position < 10% portfolio? ✓
│  ├─ Correlated exposure < 25%? ✓
│  └─ Total exposure < 80%? ✓
│
└─ Execute at recommended size
```

---

## SOL-Denominated Quick Reference

For a 100 SOL account ($15,000 at $150/SOL):

| Risk Level | Risk/Trade | SOL at Risk | Typical Position |
|-----------|-----------|-------------|-----------------|
| Conservative (0.5%) | 0.5 SOL | $75 | 2–5 SOL notional |
| Standard (1%) | 1.0 SOL | $150 | 5–10 SOL notional |
| Moderate (2%) | 2.0 SOL | $300 | 10–20 SOL notional |
| Aggressive (3%) | 3.0 SOL | $450 | 15–30 SOL notional |
| PumpFun | 0.1–0.5 SOL | $15–$75 | 0.1–0.5 SOL per play |

### Referencia: references/sizing_formulas.md

# Position Sizing — Formulas Reference

Complete mathematical derivations for all sizing methods with worked examples.

---

## Fixed Fractional Sizing

### Derivation

The goal: lose at most `R%` of account value if the stop loss is hit.

```
risk_amount = account_value × risk_percentage
price_risk_per_unit = |entry_price - stop_loss_price|
position_size_units = risk_amount / price_risk_per_unit
position_value = position_size_units × entry_price
leverage_ratio = position_value / account_value
```

### Worked Example

| Parameter | Value |
|-----------|-------|
| Account value | $10,000 |
| Risk per trade | 2% |
| Entry price | $1.50 |
| Stop loss | $1.30 |

```
risk_amount = $10,000 × 0.02 = $200
price_risk  = $1.50 - $1.30 = $0.20
units        = $200 / $0.20 = 1,000 tokens
position_value = 1,000 × $1.50 = $1,500 (15% of account)
```

If the stop is hit: loss = 1,000 × $0.20 = $200 = 2% of account.

### Fee-Adjusted Version

In practice, include fees and slippage in the risk:

```
effective_risk = price_risk + (entry_price × fee_rate × 2) + estimated_slippage
position_size = risk_amount / effective_risk
```

Example with 0.3% fees each way and 0.5% slippage:

```
fee_cost = $1.50 × 0.003 × 2 = $0.009
slippage = $1.50 × 0.005 = $0.0075
effective_risk = $0.20 + $0.009 + $0.0075 = $0.2165
units = $200 / $0.2165 = 924 tokens (vs 1,000 without fees)
```

---

## Volatility-Adjusted Sizing

### Derivation

Normalize position sizes so each position contributes roughly the same dollar volatility to the portfolio.

```
target_daily_pnl_vol = account_value × target_vol_pct
token_daily_vol = price × daily_return_std
position_size_units = target_daily_pnl_vol / token_daily_vol
```

### Using ATR (Average True Range)

ATR is a smoothed measure of daily price range:

```
daily_vol_pct = ATR(14) / close_price
position_units = (account × target_vol_pct) / ATR(14)
```

### Worked Example

| Parameter | Value |
|-----------|-------|
| Account | $10,000 |
| Target daily vol | 2% of account ($200) |
| Token price | $1.50 |
| ATR(14) | $0.12 |

```
daily_vol_pct = $0.12 / $1.50 = 8%
position_units = $200 / $0.12 = 1,667 tokens
position_value = 1,667 × $1.50 = $2,500
expected_daily_pnl_range = 1,667 × $0.12 = $200 (2% of account)
```

### Comparing Across Assets

This method lets you hold equal-risk positions across assets with very different volatilities:

| Token | Price | ATR(14) | Vol % | Units | Value |
|-------|-------|---------|-------|-------|-------|
| SOL | $150 | $6.00 | 4% | 33 | $4,950 |
| BONK | $0.00002 | $0.0000016 | 8% | 125M | $2,500 |
| JUP | $0.80 | $0.064 | 8% | 3,125 | $2,500 |

Each contributes ~$200 daily PnL volatility despite different position sizes.

---

## Kelly Criterion

### Full Derivation

The Kelly criterion maximizes the expected logarithm of wealth (geometric growth rate).

Given a binary bet with:
- Probability `p` of winning `b` units per unit risked
- Probability `q = 1 - p` of losing 1 unit per unit risked

Maximize: `E[ln(W)] = p × ln(1 + f×b) + q × ln(1 - f)`

Taking the derivative and setting to zero:

```
dE/df = p×b/(1+f×b) - q/(1-f) = 0
p×b×(1-f) = q×(1+f×b)
p×b - p×b×f = q + q×f×b
p×b - q = f×b×(p + q) = f×b
f* = (p×b - q) / b
```

Equivalent forms:
```
f* = (p×b - q) / b
f* = p - q/b
f* = (p×(b+1) - 1) / b
```

### Fractional Kelly

Full Kelly maximizes growth but produces large drawdowns. The variance of returns under Kelly is:

```
Var = p×q×(b+1)² × f²
```

Fractional Kelly reduces variance quadratically while reducing growth only linearly:

| Fraction | Growth Rate | Drawdown Risk | Recommended? |
|----------|-------------|---------------|-------------|
| 1.0x | 100% | Very high | No |
| 0.5x | 75% | Moderate | For well-measured edges |
| 0.25x | 44% | Low | Default recommendation |
| 0.1x | 19% | Very low | Ultra-conservative |

Growth rate at fraction `g`: `G(g) = g × (2 - g) × G(1)` approximately.

### Worked Examples

**Example 1: Moderate edge**
```
Win rate = 55%, avg win = 1.5x avg loss
p = 0.55, q = 0.45, b = 1.5
f* = (0.55 × 1.5 - 0.45) / 1.5 = 0.25 / 1.5 = 0.167 (16.7%)
Quarter Kelly: 4.2% risk per trade
Half Kelly: 8.3% risk per trade
```

**Example 2: High win rate, small payoff**
```
Win rate = 70%, avg win = 0.8x avg loss
p = 0.70, q = 0.30, b = 0.8
f* = (0.70 × 0.8 - 0.30) / 0.8 = 0.26 / 0.8 = 0.325 (32.5%)
Quarter Kelly: 8.1%
```

**Example 3: Low win rate, large payoff (trend following)**
```
Win rate = 35%, avg win = 4x avg loss
p = 0.35, q = 0.65, b = 4.0
f* = (0.35 × 4.0 - 0.65) / 4.0 = 0.75 / 4.0 = 0.1875 (18.75%)
Quarter Kelly: 4.7%
```

**Example 4: No edge**
```
Win rate = 45%, avg win = 1.0x avg loss
f* = (0.45 × 1.0 - 0.55) / 1.0 = -0.10
Negative Kelly → NO EDGE → do not trade
```

---

## Liquidity-Constrained Sizing

### Constant-Product AMM Slippage

For a constant-product AMM (x × y = k):

```
price_impact = trade_size / (pool_reserve + trade_size)
```

For small trades relative to pool size:

```
slippage ≈ trade_size / pool_reserve
```

### Maximum Trade Size

Given a maximum acceptable slippage:

```
max_trade = pool_reserve × max_slippage_pct
```

### Worked Example

| Parameter | Value |
|-----------|-------|
| Pool SOL reserve | 500 SOL |
| Pool token reserve | 5,000,000 tokens |
| Token price | 0.0001 SOL |
| Max slippage | 2% |

```
max_trade_sol = 500 × 0.02 = 10 SOL
max_trade_tokens = 5,000,000 × 0.02 = 100,000 tokens
```

### Multi-Pool Aggregation

When a token has liquidity across multiple pools:

```
total_available = sum(pool_reserve_i × max_slippage for each pool_i)
```

However, a DEX aggregator (Jupiter) will split the order optimally. The effective available liquidity is typically 70-90% of the simple sum due to routing overhead.

### Position vs Trade Size

A position may require multiple trades to build:

```
max_single_trade = pool_liquidity × 0.02   # 2% per trade
max_position = pool_liquidity × 0.05       # 5% total (built in chunks)
trades_needed = ceil(desired_position / max_single_trade)
```

---

## Combined Sizing Ladder

Calculate all four methods and take the minimum:

```python
def sizing_ladder(
    account: float,
    risk_pct: float,
    entry: float,
    stop: float,
    atr: float,
    target_vol: float,
    win_rate: float,
    payoff_ratio: float,
    kelly_fraction: float,
    pool_liquidity: float,
    max_slippage: float,
) -> dict:
    # 1. Fixed fractional
    ff_units = (account * risk_pct) / abs(entry - stop)

    # 2. Volatility-adjusted
    vol_units = (account * target_vol) / atr

    # 3. Kelly
    kelly_f = (win_rate * payoff_ratio - (1 - win_rate)) / payoff_ratio
    kelly_risk = max(0, kelly_f * kelly_fraction)
    kelly_units = (account * kelly_risk) / abs(entry - stop)

    # 4. Liquidity-constrained
    liq_value = pool_liquidity * max_slippage
    liq_units = liq_value / entry

    sizes = {
        "fixed_fractional": ff_units,
        "volatility_adjusted": vol_units,
        "kelly": kelly_units,
        "liquidity": liq_units,
    }
    binding = min(sizes, key=sizes.get)
    return {"sizes": sizes, "recommended": sizes[binding], "binding": binding}
```


---

## SKILL: pricing-margin-bridge

- Fuente: `SYasJ/claude-business-skills` → `plugins/finance/skills/pricing-margin-bridge` (MIT)
- Cuándo usarla: Trace price, mix, and cost so a margin change has a cause and a commercial response. Use when the user mentions margin bridge, price mix cost, why did margin fall, pricing review, or asks for a price-mix-cost bridge. Finance skill by Yasir Jilani.

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'pricing-margin-bridge' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Pricing and Margin Bridge

Trace price, mix, and cost so a margin change has a cause and a commercial response.

## When to use this skill

Use this skill when the user:

- margin bridge
- price mix cost
- why did margin fall
- pricing review

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

- Revenue and cost for two periods
- Price and volume detail if available
- Known mix shifts
- Discount or rebate practice

## Workflow


### 1. Start with the margin change

State gross margin or contribution change in the user's currency and in points.
### 2. Separate price, volume, and mix

Use the detail the user has. If mix cannot be seen, say the bridge is incomplete rather than forcing a fake split.
### 3. Put discounts in price

A discount is a price decision. Do not hide it in cost.
### 4. Isolate cost inflation

Input cost changes sit on their own step, with the user's evidence.
### 5. Recommend one commercial move

A price test, a mix target, or a cost action. Not all three at full strength unless the user has capacity.
### 6. Flag customer impact

Who would feel the move. Do not draft deceptive pricing.

## Output

Deliver a **price-mix-cost bridge**.

- Purpose of this price-mix-cost bridge, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a price-mix-cost bridge by 30 September 2026. Gross margin fell two points and sales says it was only product mix.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Gross margin fell two points and sales says it was only product mix.

Revenue and cost for two periods: month ending 14 September 2026
Price and volume detail if available: CAD 180
Known mix shifts: Harbor & Co receipt. Stated in the ask, not documented anywhere else
Discount or rebate practice: 55 in the last period. No prior period attached, so no trend
```

### Example outcome

**Price-mix-cost bridge**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Shows what portion is mix, price, and cost on the available data, plus one commercial response.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Revenue and cost for two periods | month ending 14 September 2026 | Needs confirmation |
| Price and volume detail if available | CAD 180 | Carried into the draft |
| Known mix shifts | Harbor & Co receipt. Stated in the ask, not documented anywhere else | Carried into the draft |
| Discount or rebate practice | 55 in the last period. No prior period attached, so no trend | Needs confirmation |

**How this draft was built**

**1. Start with the margin change**  
State gross margin or contribution change in the user's currency and in points.

**2. Separate price, volume, and mix**  
Use the detail the user has. If mix cannot be seen, say the bridge is incomplete rather than forcing a fake split.

**3. Put discounts in price**  
A discount is a price decision. Do not hide it in cost.

**4. Isolate cost inflation**  
Input cost changes sit on their own step, with the user's evidence.

**5. Recommend one commercial move**  
A price test, a mix target, or a cost action. Not all three at full strength unless the user has capacity.

**Deliberately not done**
- A margin story with no bridge.
- Blaming mix when the data cannot show mix.
- Recommending a price increase with no customer consequence.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A margin story with no bridge.
- Blaming mix when the data cannot show mix.
- Recommending a price increase with no customer consequence.

## Related skills

- `unit-economics`
- `pricing-packaging`
- `budget-variance-review`


---

## SKILL: rebalancing

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/rebalancing` (MIT)
- Cuándo usarla: Maintain portfolio allocations over time using calendar-based, threshold-based, and tax-efficient rebalancing strategies. Use when the user asks about when to rebalance, rebalancing bands, transaction cost trade-offs, tax-efficient rebalancing, or the rebalancing premium. Also trigger when users mention 'my portfolio drifted', 'how often should I rebalance', 'rebalancing across taxable and IRA accounts', 'volatility harvesting', 'buy low sell high automatically', or ask whether to use cash flows to rebalance.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/wealth-management/skills/rebalancing/` (rebalancing.py)

# Rebalancing

## Core Concepts

### Calendar Rebalancing
Rebalance at fixed time intervals regardless of drift magnitude:

- **Monthly:** Tightest tracking to targets; highest transaction costs
- **Quarterly:** Common institutional frequency; good balance of tracking and costs
- **Annually:** Lowest cost; may allow significant drift between dates

Calendar rebalancing is simple to implement and schedule but may miss large dislocations between dates or trigger unnecessary trades when drift is minimal.

### Threshold (Band) Rebalancing
Rebalance when any asset weight drifts beyond a defined tolerance band around its target:

- Monitor weights continuously (or at regular intervals)
- Trigger rebalancing when |w_actual - w_target| > tolerance
- Typical bands: +/- 3% to +/- 5% (absolute) or +/- 20% to +/- 25% (relative)

Threshold rebalancing is more responsive to market dislocations and avoids unnecessary trades when markets are calm. However, it requires more frequent monitoring.

### Optimal Band Width (Leland Model)
Leland (2000) derived the optimal no-trade band width as a function of transaction costs, risk aversion, and asset variance:

Band width proportional to (3 * transaction_cost / (2 * risk_aversion * variance))^(1/3)

Key intuition:
- Higher transaction costs → wider bands (trade less)
- Higher risk aversion → narrower bands (maintain target more tightly)
- Higher variance → narrower bands (drift happens faster, risk of deviation is greater)

### Rebalancing Premium
Systematic rebalancing generates a "volatility harvesting" or "rebalancing premium" through the buy-low/sell-high mechanism:

- When an asset rises, its weight increases → rebalancing sells some (sell high)
- When an asset falls, its weight decreases → rebalancing buys some (buy low)

This effect is sometimes called **Shannon's Demon**: in a two-asset portfolio with equal expected returns but independent volatility, the constantly rebalanced portfolio outperforms buy-and-hold. The rebalancing premium is larger when:
- Asset volatilities are higher
- Correlations are lower
- Assets have similar expected returns (so mean-reversion dominates trends)

Note: The rebalancing premium is not a free lunch — it underperforms in trending markets where winners keep winning.

### Transaction Costs
Costs incurred when rebalancing that reduce net returns:

- **Commissions:** Per-trade or per-share fees (increasingly zero for retail)
- **Bid-ask spread:** The cost of crossing the spread; wider for less liquid assets
- **Market impact:** Price movement caused by the trade itself; significant for large positions in less liquid markets
- **Opportunity cost:** Delay cost if rebalancing is deferred to avoid transaction costs

Total implementation cost = commissions + half-spread + market impact + opportunity cost

### Tax-Efficient Rebalancing
Strategies to minimize tax impact when rebalancing in taxable accounts:

1. **Use cash flows:** Direct new contributions to underweight assets and withdrawals from overweight assets
2. **Redirect dividends and interest:** Reinvest income from overweight assets into underweight assets
3. **Rebalance with new contributions:** The most tax-efficient method — no selling required
4. **Asset location:** Hold tax-inefficient assets (bonds, REITs) in tax-deferred accounts; rebalance these freely
5. **Selective lot identification:** When selling, choose tax lots with the highest cost basis (lowest gain) or lots held over one year (long-term capital gains rate)

### Coordinating with Tax-Loss Harvesting (TLH)
Rebalancing and TLH should be planned together, not as separate trade lists:

- **Combine TLH sells with rebalance sells** to reduce total trade count and transaction costs
- **An overweight position sitting at a loss is the ideal dual-purpose trade** — the harvest and the rebalance are the same sell
- **Check open wash-sale windows before buying back** or before rebalance buys in any account (including IRAs and spouse accounts)

Tax benefit = Realized loss * Marginal tax rate. For the 61-day wash-sale window, the $3,000 ordinary-income offset, replacement selection, and full TLH mechanics, see the **tax-loss-harvesting** skill.

### Rebalancing Across Account Types
When an investor has multiple account types (taxable, IRA, 401k), optimize rebalancing by:

- **Tax-deferred accounts (IRA, 401k):** Rebalance freely — no tax consequences
- **Taxable accounts:** Minimize selling; use cash flows, TLH, and selective lot sales
- **Cross-account rebalancing:** Consider the aggregate portfolio across all accounts and rebalance within the most tax-efficient account

### Drift Tolerance Setting
Factors that determine optimal band width:

- **Tighter bands (e.g., +/- 2%):** Better risk control, higher costs, appropriate for low-cost/institutional settings
- **Wider bands (e.g., +/- 10%):** Lower costs, more drift risk, appropriate for taxable accounts with high tax impact
- **Asset-specific bands:** More volatile assets may need wider absolute bands but tighter relative bands

### Cash Flow Rebalancing
Use regular deposits or withdrawals to move toward target weights without explicit rebalancing trades:

- Calculate current vs. target weights
- Direct 100% of new contributions to the most underweight asset(s)
- Process withdrawals from the most overweight asset(s)
- This "natural rebalancing" is the most cost-effective and tax-efficient approach

### Rebalancing Workflow

The concepts above describe the *what* and *why* of rebalancing. This section covers the operational *how* — the step-by-step process an advisor follows to execute a rebalance for a client household.

**Step 1: Aggregate Household View**
Assemble the complete picture across all accounts (taxable brokerage, Traditional IRA, Roth IRA, 401(k), 529, trust). Calculate the household-level allocation by summing positions across all accounts, not just individual account allocations. Many drift problems are invisible at the account level but obvious at the household level.

**Step 2: Asset Location Review**
Before proposing trades, document which account types hold which asset classes:
- Tax-inefficient assets (bonds, REITs, high-turnover funds) should be in tax-deferred accounts
- Tax-efficient assets (index equity ETFs, municipal bonds) should be in taxable accounts
- Highest-growth assets should be in Roth accounts (permanent tax-free growth)

If asset location is suboptimal, the rebalance is an opportunity to improve it — but only if the tax cost of repositioning is justified by the long-term tax savings.

**Step 3: Drift Analysis and Trade Generation**
For each asset class, calculate drift from target and compare against tolerance bands (from the IPS or firm default):
- Generate a preliminary trade list: sell overweight positions, buy underweight positions
- Prioritize trades by drift magnitude — address the largest deviations first
- Check whether cash flows (pending contributions, withdrawals, dividends) can partially or fully close the drift without explicit trades

**Step 4: Tax-Impact Estimation**
For each proposed sell trade in a taxable account, estimate the tax consequence:
- Identify available tax lots and their holding periods (short-term vs long-term)
- Calculate the estimated capital gain or loss for each lot using specific identification (HIFO preferred)
- Sum the estimated tax liability across all proposed sells
- Compare the tax cost against the risk-reduction benefit of rebalancing — defer trades where tax cost outweighs the tracking error reduction
- Coordinate with any pending tax-loss harvesting opportunities (see **tax-loss-harvesting** skill)

**Step 5: Cross-Account Optimization**
Minimize total household tax impact by choosing *where* to execute each trade:
- Execute sells of appreciated positions in tax-deferred accounts when possible (no tax consequence)
- Execute sells of depreciated positions in taxable accounts (harvest the loss)
- Use cross-account rebalancing: if equities are overweight in the taxable account and underweight in the IRA, sell equities in the IRA and buy bonds in the IRA, rather than selling equities in the taxable account
- Check for wash-sale conflicts: if harvesting a loss in the taxable account, ensure no purchase of a substantially identical security occurs within 30 days in any account (including IRA, 401(k), and spouse accounts)

**Step 6: Before/After Comparison**
Generate a before/after allocation comparison for advisor review and client communication:
- Current allocation vs target allocation vs post-rebalance allocation (three columns)
- Estimated transaction costs (commissions, spreads)
- Estimated tax impact (net gains/losses realized)
- Expected tracking error reduction
- Number of trades and accounts affected

This comparison serves as both a decision tool (does the rebalance justify its costs?) and a compliance artifact (documenting the rationale for the trades).

**Step 7: Execution and Confirmation**
- Submit the approved trade list through the order management system
- For block trades across multiple accounts, ensure fair allocation per the firm's allocation policy
- Confirm fills and reconcile actual vs intended post-rebalance weights
- Document the rebalance event: date, reason (scheduled, threshold trigger, or ad-hoc), trades executed, and resulting allocation

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Threshold Trigger | |w_actual - w_target| > tolerance | Rebalancing trigger condition |
| Optimal Band Width | band ~ (3*tc / (2*lambda*sigma^2))^(1/3) | Leland optimal no-trade zone |
| Tax-Loss Benefit | Benefit = Loss * Tax Rate | Value of harvested losses |
| Transaction Cost | TC = commission + spread/2 + impact | Total rebalancing cost |
| Drift | Drift_i = w_actual_i - w_target_i | Weight deviation from target |
| Trade Size | Trade_i = (w_target_i - w_actual_i) * Portfolio Value | Dollar amount to trade |
| Rebalancing Premium | RP ~ (1/2) * Σ w_i * sigma_i^2 - (1/2) * sigma_p^2 | Volatility harvesting estimate |

## Worked Examples

### Example 1: Threshold Rebalancing — 60/40 Portfolio
**Given:**
- Target: 60% equity / 40% bonds
- Rebalancing threshold: +/- 5% (absolute)
- Current portfolio value: $1,000,000
- After market movement: equity = $680,000 (68%), bonds = $320,000 (32%)

**Calculate:** Rebalancing trigger and required trades

**Solution:**

Check drift:
- Equity drift: 68% - 60% = +8% → exceeds +5% threshold → **TRIGGER**
- Bond drift: 32% - 40% = -8% → exceeds -5% threshold → **TRIGGER**

Target dollar amounts:
- Equity target: 60% * $1,000,000 = $600,000
- Bond target: 40% * $1,000,000 = $400,000

Required trades:
- Sell equity: $680,000 - $600,000 = **$80,000**
- Buy bonds: $400,000 - $320,000 = **$80,000**

Proceeds from equity sales fund the bond purchases. In a taxable account, check the cost basis of equity lots being sold to estimate tax impact before executing.

### Example 2: Tax-Loss Harvesting Benefit
**Given:**
- Position purchased for $50,000, current value $40,000
- Unrealized loss: $10,000
- Investor's marginal federal tax rate: 37% (ordinary income) / 20% (long-term capital gains)
- Investor has $15,000 in realized capital gains this year

**Calculate:** Tax benefit of harvesting the loss

**Solution:**

Realized loss from sale: **$10,000**

Tax benefit calculation:
- The $10,000 loss offsets $10,000 of the $15,000 in realized capital gains
- Tax saved: $10,000 * 20% = **$2,000** (assuming long-term gains rate)
- Remaining gains: $15,000 - $10,000 = $5,000 (still taxable)

If the investor had no capital gains to offset:
- First $3,000 offsets ordinary income: $3,000 * 37% = $1,110
- Remaining $7,000 carries forward to future years
- Total immediate benefit: $1,110; total eventual benefit up to $2,000+ depending on future gains

Implementation:
1. Sell the losing position for $40,000
2. Immediately purchase a similar but not substantially identical replacement (e.g., swap a total US stock ETF for an S&P 500 ETF)
3. Do NOT repurchase the original security within 30 days (wash sale rule)
4. After 31 days, may swap back to original security if preferred

Note: TLH creates a lower cost basis in the replacement security, so taxes are deferred, not eliminated. However, the time value of the tax deferral and the ability to offset gains at favorable rates makes TLH valuable.

## Common Pitfalls
- Over-rebalancing: trading too frequently erodes returns through transaction costs and taxes, especially in taxable accounts
- Under-rebalancing: allowing excessive drift exposes the portfolio to unintended risk levels and style drift
- Wash sale violations when tax-loss harvesting: purchasing a substantially identical security within the 61-day window triggers wash sale rules, disallowing the loss
- Ignoring tax impact of rebalancing in taxable accounts: rebalancing by selling winners generates taxable capital gains
- Calendar rebalancing may miss large dislocations between dates (e.g., a 20% market crash between quarterly rebalancing dates)
- Not accounting for the rebalancing premium when comparing strategies — buy-and-hold backtests may understate rebalanced portfolio returns
- Forgetting to consider the full 61-day wash sale window (30 days before and after the sale)
- Rebalancing into the wrong account: selling appreciated assets in taxable accounts when the same rebalancing could be done in tax-deferred accounts

## Cross-References
- **asset-allocation** (wealth-management plugin): rebalancing maintains the target asset allocation over time
- **diversification** (wealth-management plugin): rebalancing preserves the intended diversification structure
- **bet-sizing** (wealth-management plugin): position sizes drift and need rebalancing to maintain conviction weighting
- **historical-risk** (wealth-management plugin): drift changes portfolio risk profile; rebalancing controls it
- **financial-statements** (wealth-management plugin): tax implications of rebalancing require understanding of tax accounting
- **tax-loss-harvesting** (wealth-management plugin): TLH trades should be coordinated with rebalancing to minimize total transaction count and avoid wash-sale conflicts
- **tax-efficiency** (wealth-management plugin): asset location and tax-lot selection strategies directly affect rebalancing trade decisions
- **client-review-prep** (advisory-practice plugin): drift analysis and rebalancing recommendations are core agenda items in periodic client reviews

## Running the script
Run with `uv run scripts/rebalancing.py` (the PEP 723 header resolves dependencies automatically) or with `python3 scripts/rebalancing.py` after `pip install numpy scipy`. The bare run prints a demo covering drift analysis, threshold checks, trade generation, cash flow rebalancing, transaction costs, tax-aware lot selection, Leland bands, and the rebalancing premium. Pass `--verify` to assert the demo outputs match this skill's worked examples (prints PASS/FAIL), or `--help` for an overview of the available classes. The file is primarily meant to be imported as a module (e.g., `from rebalancing import DriftAnalyzer, TradeGenerator, TaxAwareLotSelector`).


---

## SKILL: records-retention

- Fuente: `SYasJ/claude-business-skills` → `plugins/risk/skills/records-retention` (MIT)
- Cuándo usarla: Draft a retention schedule from the record types they know they keep, with owners and legal questions marked. Use when the user mentions records retention, retention schedule, how long do we keep this, record series, or asks for a retention schedule draft. Risk and compliance skill by Yasir Jilani.

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'records-retention' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Records Retention Schedule

Draft a retention schedule from the record types they know they keep, with owners and legal questions marked.

## When to use this skill

Use this skill when the user:

- records retention
- retention schedule
- how long do we keep this
- record series

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Risk work prioritizes uncertainty. It is not a certification. Do not claim SOC 2, ISO, HIPAA, or similar compliance unless the user has evidence of it.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Record types
- Where they live
- Business need they stated
- Legal holds they know about

## Workflow


### 1. Step 1

List record types they actually keep, not a generic encyclopedia.
### 2. Step 2

Record the business reason to keep each one.
### 3. Step 3

Mark the legal period as a question for counsel unless they supplied it. Do not invent a statutory period.
### 4. Step 4

Note systems so people can find and delete on purpose.
### 5. Step 5

Holds override deletion. Say that, and do not help delete held records.
### 6. Step 6

Name an owner for the schedule.

## Output

Deliver a **retention schedule draft**.

- Purpose of this retention schedule draft, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a retention schedule draft by 30 September 2026. A team wants a seven-year rule on everything because it sounds safe.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A team wants a seven-year rule on everything because it sounds safe.

Record types: one file, dated 14 September 2026. No earlier version attached for comparison
Where they live: Vendor Redline Parts, recorded 14 September 2026. No supporting file attached
Business need they stated: Vendor Redline Parts. Partly documented: the what is written down, the who is not
Legal holds they know about: Issue log item 18 and one other, both unconfirmed as of 14 September 2026
```

### Example outcome

**Retention schedule draft**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Refuses the blanket rule, separates business need from legal questions, and protects holds.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Record types | one file, dated 14 September 2026. No earlier version attached for comparison | Needs confirmation |
| Where they live | Vendor Redline Parts, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Business need they stated | Vendor Redline Parts. Partly documented: the what is written down, the who is not | Carried into the draft |
| Legal holds they know about | Issue log item 18 and one other, both unconfirmed as of 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. List record types they actually keep, not a generic encyclopedia**

**2. Record the business reason to keep each one**

**3. Mark the legal period as a question for counsel unless they supplied it. Do not invent a statutory period**

**4. Note systems so people can find and delete on purpose**

**5. Holds override deletion. Say that, and do not help delete held records**

**Deliberately not done**
- Invented statutory periods.
- Deleting records under a known hold.
- A schedule of records they do not have.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Invented statutory periods
- Deleting records under a known hold
- A schedule of records they do not have

## Related skills

- `legal-hold-notice`
- `policy-writer`


---

## SKILL: return-calculations

- Fuente: `JoelLewis/finance_skills` → `plugins/core/skills/return-calculations` (MIT)
- Cuándo usarla: Compute and compare investment return metrics including TWR, MWR (dollar-weighted IRR on portfolio cash flows), CAGR, and annualized returns. Use when the user asks about portfolio performance calculation, comparing manager returns, linking sub-period returns, understanding why different return methods give different numbers, converting returns across time periods, or computing the IRR of an investor's own contributions and withdrawals. Also trigger when users mention 'how much did I make', 'annual return', 'compound growth', 'dollar-weighted vs time-weighted', 'what was my rate of return', 'geometric vs arithmetic mean', 'log returns', or ask about the effect of cash flows on reported returns. For project or loan IRR, NPV, and generic 'solve for the rate' problems, use time-value-of-money instead.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/core/skills/return-calculations/` (return_calculations.py)

# Return Calculations

## Core Concepts

### Simple (Holding Period) Return

$$R = \frac{V_{end} - V_{begin} + D}{V_{begin}}$$

where `D` = distributions (dividends, interest) received during the period. If `V_end` already reflects reinvested distributions, do not add `D` again.

### Mean and Log Return Conventions

- **Arithmetic mean** `R_a = (1/n) * sum(R_i)` — unbiased estimate of the expected *single-period* return (use for forward-looking inputs, e.g., mean-variance optimization). Always >= geometric mean; overstates realized compound growth.
- **Geometric mean** `R_g = [prod(1 + R_i)]^(1/n) - 1` — the correct measure of realized multi-period compound growth. The gap below the arithmetic mean approximates `sigma^2 / 2` (volatility drag).
- **Log return** `r = ln(V_end / V_begin)` — time-additive (`r_total = r_1 + ... + r_n`), so preferred for statistical modeling and multi-period aggregation. Convert with `R_simple = e^r - 1` and `r = ln(1 + R_simple)`. Log returns are additive across time but NOT across assets.

### CAGR (Compound Annual Growth Rate)

$$CAGR = \left(\frac{V_{end}}{V_{begin}}\right)^{1/n} - 1$$

where `n` is measured in years. The annualized geometric growth rate between two valuations with no intermediate cash flows.

### Time-Weighted Return (TWR)
Chain-links sub-period returns calculated between each external cash flow, removing the effect of cash flow timing. TWR measures the manager's investment skill independent of investor deposit/withdrawal decisions, and is the GIPS standard for manager performance.

$$1 + R_{TWR} = \prod_{i=1}^{n}(1 + R_i), \qquad R_i = \frac{V_{end,i}}{V_{begin,i} + CF_i} - 1$$

Exact TWR requires a portfolio valuation on every cash flow date.

### Modified Dietz Return
When valuations on each cash flow date are unavailable, Modified Dietz approximates the period return by day-weighting each external cash flow within the period:

$$R_{MD} = \frac{V_{end} - V_{begin} - CF_{net}}{V_{begin} + \sum_i CF_i \times w_i}, \qquad w_i = \frac{CD - D_i}{CD}$$

where `CF_net` = sum of external cash flows, `CD` = calendar days in the period, and `D_i` = day of flow `i` (so `w_i` is the fraction of the period the flow was invested). It is a money-weighted approximation; chain-linking Modified Dietz sub-period returns approximates TWR. Accuracy degrades when flows are large relative to portfolio value or markets are volatile within the period — revalue on large-flow dates instead.

### Money-Weighted Return (MWR / IRR)
The internal rate of return that sets the NPV of all investor cash flows (contributions, withdrawals, and terminal value) to zero:

$$0 = \sum_{t=0}^{T} \frac{CF_t}{(1 + r)^t}$$

MWR reflects the actual investor experience because it is sensitive to the timing and magnitude of cash flows. Solved numerically (Newton-Raphson or bisection).

### Annualization

$$R_{annual} = (1 + R_{period})^{periods\_per\_year} - 1$$

For example, a 2% quarterly return annualizes to `(1.02)^4 - 1 = 8.24%`.

### Sub-Period Linking

$$(1 + R_{total}) = \prod_{i=1}^{n}(1 + R_i)$$

The foundational identity behind TWR and CAGR.

## Worked Examples

### Example 1: Computing CAGR from a 5-Year Investment
**Given:** An investment of $10,000 grows to $16,105.10 over exactly 5 years with no intermediate cash flows.

**Calculate:** The compound annual growth rate (CAGR).

**Solution:**

```
CAGR = (V_end / V_begin)^(1/n) - 1
CAGR = (16,105.10 / 10,000)^(1/5) - 1
CAGR = (1.610510)^(0.2) - 1
CAGR = 1.10 - 1
CAGR = 0.10 = 10%
```

The investment grew at a compound annual rate of **10%** per year.

Verification: `$10,000 * (1.10)^5 = $10,000 * 1.61051 = $16,105.10`

### Example 2: TWR vs MWR Divergence with Poorly Timed Cash Flow
**Given:** A fund has the following history:
- Start of Year 1: Portfolio value = $100,000
- End of Year 1: Portfolio value = $120,000 (return = +20%)
- Start of Year 2: Investor deposits $100,000, bringing portfolio to $220,000
- End of Year 2: Portfolio value = $198,000 (return = -10%)

**Calculate:** Both TWR and MWR, and explain the divergence.

**Solution:**

**Time-Weighted Return (TWR):**
```
Sub-period 1 return: R_1 = (120,000 - 100,000) / 100,000 = +20%
Sub-period 2 return: R_2 = (198,000 - 220,000) / 220,000 = -10%

TWR (cumulative) = (1 + 0.20) * (1 + (-0.10)) - 1
                  = 1.20 * 0.90 - 1
                  = 1.08 - 1
                  = +8.0%

TWR (annualized) = (1.08)^(1/2) - 1 = 3.92%
```

**Money-Weighted Return (MWR / IRR):**
Cash flows from the investor's perspective:
- t=0: -$100,000 (initial investment)
- t=1: -$100,000 (additional deposit)
- t=2: +$198,000 (terminal value)

Solve: `-100,000 + (-100,000)/(1+r) + 198,000/(1+r)^2 = 0`

This is quadratic in `x = 1/(1+r)`; the positive root gives r = -0.66815% (verifiable with the bundled script or any IRR solver).

NPV check at r = -0.0066815:
```
-100,000 + (-100,000)/0.9933185 + 198,000/0.9933185^2
= -100,000 - 100,672.65 + 200,672.65
= 0.00  (exact)
```

The MWR is approximately **-0.67% annualized**.

**Interpretation:** The TWR of +3.92% annualized reflects the manager's skill: the fund gained 20% then lost 10%, netting +8% over two years. The MWR of approximately -0.67% reflects the investor's experience: more money was at risk during the losing year (Year 2) because of the large deposit, so the investor's dollar-weighted outcome was slightly negative. This divergence highlights why TWR is preferred for evaluating manager performance, while MWR better describes the specific investor's realized result.

## Common Pitfalls
- Confusing arithmetic and geometric means: the arithmetic mean is always greater than or equal to the geometric mean (AM-GM inequality). Using arithmetic mean to project compounded growth overstates terminal wealth.
- Using arithmetic mean for multi-period compounding: always use geometric mean or CAGR when describing compound growth over multiple periods.
- Annualizing returns from very short periods: annualizing a 2% weekly return yields `(1.02)^52 - 1 = 180%`, which amplifies noise and is misleading. Annualization is most meaningful for periods of at least one year.
- Ignoring cash flow timing when TWR is appropriate: MWR conflates manager skill with investor timing decisions. Use TWR for manager evaluation.
- Double-counting dividends: if the ending value `V_end` already includes reinvested dividends, do not add `D` separately in the holding period return formula.
- Trusting Modified Dietz with large intra-period flows: when a single flow exceeds roughly 10% of portfolio value, revalue the portfolio on the flow date rather than day-weighting.

## Running the Script
`scripts/return_calculations.py` provides a `Returns` class with static methods for every formula above (holding period return, TWR, MWR/IRR via Newton's method, Modified Dietz is straightforward to compose from these, CAGR, annualization, linking, arithmetic/geometric means, log-return conversions).

- Run: `uv run scripts/return_calculations.py` (PEP 723 inline metadata resolves numpy automatically), or `python3 scripts/return_calculations.py` with numpy installed.
- Bare invocation (or `--verify`) prints a demo of all functions **and** asserts the worked-example values above (Example 1 CAGR = 10%, Example 2 TWR = +8.0% cumulative / 3.92% annualized, MWR = -0.6682%), exiting nonzero on any mismatch.
- `--help` lists the available functions and import usage.
- For programmatic use, import rather than run: `from return_calculations import Returns`.

## Cross-References
- **time-value-of-money** (core plugin): NPV, IRR, and discounting concepts overlap with MWR calculations; owns project/loan IRR
- **statistics-fundamentals** (core plugin): Arithmetic and geometric means, return distribution analysis


---

## SKILL: risk-assessment

- Fuente: `SYasJ/claude-business-skills` → `plugins/risk/skills/risk-assessment` (MIT)
- Cuándo usarla: Assess a few real risks with a scenario, a control, and an owner, using the organization's own scale. Use when the user mentions risk assessment, assess this risk, risk workshop, enterprise risk item, or asks for a risk assessment. Risk and compliance skill by Yasir Jilani.

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'risk-assessment' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Risk Assessment

Assess a few real risks with a scenario, a control, and an owner, using the organization's own scale.

## When to use this skill

Use this skill when the user:

- risk assessment
- assess this risk
- risk workshop
- enterprise risk item

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Risk work prioritizes uncertainty. It is not a certification. Do not claim SOC 2, ISO, HIPAA, or similar compliance unless the user has evidence of it.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The objective at risk
- Scenarios they can describe
- Existing controls
- Their scale

## Workflow


### 1. Step 1

Write scenarios as events, not as one-word categories.
### 2. Step 2

Use their likelihood and impact scale. If none exists, propose a simple one and label it.
### 3. Step 3

Name the current control and whether they have evidence it operates.
### 4. Step 4

Rate residual risk only after the control is described.
### 5. Step 5

Recommend mitigate, accept, or transfer as a question for the owner. Insurance transfer is not confirmed unless they say a policy exists.
### 6. Step 6

Do not claim a certification because a risk was written down.

## Output

Deliver a **risk assessment**.

- Purpose of this risk assessment, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a risk assessment by 30 September 2026. A workshop list says 'cyber' and 'talent' with no scenario.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A workshop list says 'cyber' and 'talent' with no scenario.

The objective at risk: Control 7.2 access review is open. No score in the file
Scenarios they can describe: Control 7.2 access review. Partly documented: the what is written down, the who is not
Existing controls: their one-page rule dated 2 Mar 2026. No exception log since
Their scale: Vendor Redline Parts, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Risk assessment**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Rewrites those into specific events or drops them until a scenario exists.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The objective at risk | Control 7.2 access review is open. No score in the file | Needs confirmation |
| Scenarios they can describe | Control 7.2 access review. Partly documented: the what is written down, the who is not | Carried into the draft |
| Existing controls | their one-page rule dated 2 Mar 2026. No exception log since | Carried into the draft |
| Their scale | Vendor Redline Parts, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. Write scenarios as events, not as one-word categories**

**2. Use their likelihood and impact scale. If none exists, propose a simple one and label it**

**3. Name the current control and whether they have evidence it operates**

**4. Rate residual risk only after the control is described**

**5. Recommend mitigate, accept, or transfer as a question for the owner. Insurance transfer is not confirmed unless they say a policy exists**

**Deliberately not done**
- One-word risks.
- A certification claim.
- Ratings with no scale.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- One-word risks
- A certification claim
- Ratings with no scale

## Related skills

- `risk-register`
- `control-design`


---

## SKILL: risk-assessment

- Fuente: `staskh/trading_skills` → `.claude/skills/risk-assessment` (MIT)
- Cuándo usarla: Assess risk metrics for a stock or position including volatility, beta, VaR, and drawdown analysis. Use when user asks about risk, volatility, beta, VaR, value at risk, drawdown, or position sizing.
- Código: extraer `code/staskh_trading_skills.tar` y usar `.claude/skills/risk-assessment/` (risk.py)

# Risk Assessment

Calculate risk metrics for stocks and positions.

## Instructions

> **Note:** If `uv` is not installed or `pyproject.toml` is not found, replace `uv run python` with `python` in all commands below.

```bash
uv run python scripts/risk.py SYMBOL [--period PERIOD] [--position-size SIZE]
```

## Arguments

- `SYMBOL` - Ticker symbol
- `--period` - Analysis period: 1mo, 3mo, 6mo, 1y (default: 1y)
- `--position-size` - Dollar amount for position-specific metrics (optional)

## Output

Returns JSON with:
- `volatility` - Historical volatility (annualized)
- `beta` - Beta vs SPY
- `var_95` - 95% Value at Risk (daily)
- `var_99` - 99% Value at Risk (daily)
- `max_drawdown` - Maximum drawdown in period
- `sharpe_ratio` - Risk-adjusted return
- `position_risk` - If position-size provided, dollar VaR

Explain what the risk metrics mean and suggest position sizing if relevant.

## Dependencies

- `numpy`
- `yfinance`


## Timezone

All timestamps and time-based calculations must use the `America/New_York` timezone. All JSON output must include `generated_at` (NY time string) and `data_delay` fields.


---

## SKILL: risk-management

- Fuente: `agiprolabs/claude-trading-skills` → `skills/risk-management` (MIT)
- Cuándo usarla: Portfolio-level risk controls, drawdown management, exposure limits, and circuit breakers for crypto trading
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/risk-management/` (drawdown_analyzer.py, risk_dashboard.py)

# Risk Management

Portfolio-level risk controls for crypto and Solana trading. This skill provides frameworks for drawdown management, exposure limits, circuit breakers, and crypto-specific risk considerations.

## Risk Management Hierarchy

Every decision must respect this priority order:

1. **Survival** — Never risk account ruin. No single trade, day, or week should threaten your ability to continue trading.
2. **Capital preservation** — Protect what you have. Losses compound geometrically; recovery requires outsized gains.
3. **Growth** — Only after survival and preservation are secured, pursue returns.

Violating this hierarchy (chasing growth at the expense of survival) is the primary cause of account blowups.

## Portfolio-Level Controls

### 1. Maximum Drawdown Limits

Halt trading when portfolio drawdown from equity peak reaches a threshold:

| Account Type | Max Drawdown | Action |
|---|---|---|
| Conservative | -15% | Full stop, review all strategies |
| Moderate | -20% | Full stop, reduce to minimum size on recovery |
| Aggressive | -25% | Full stop, mandatory cooling period |

Recovery math makes this critical: a -20% drawdown requires +25% to recover. A -50% drawdown requires +100%. See `references/drawdown_management.md` for the full recovery table.

### 2. Daily Loss Limits

Stop opening new positions after daily P&L (realized + unrealized) hits:

- **Conservative**: -3% of account
- **Moderate**: -4% of account
- **Aggressive**: -5% of account

Reset at midnight UTC. Three consecutive days hitting the daily limit triggers a weekly halt.

### 3. Weekly Loss Limits

Reduce size or halt after weekly P&L reaches:

- **Reduce size by 50%**: -5% weekly loss
- **Minimum size only**: -7% weekly loss
- **Full halt**: -10% weekly loss

### 4. Concentration Limits

Maximum allocation to any single dimension:

| Dimension | Max Concentration |
|---|---|
| Single token (blue chip) | 10% of account |
| Single token (mid-cap) | 5% |
| Single token (small-cap) | 2% |
| Single token (PumpFun/micro) | 0.5% |
| Single sector/narrative | 30% |
| Single strategy | 40% |

### 5. Exposure Limits

Total deployed capital constraints:

- **Normal conditions**: 50–80% deployed, 20–50% cash reserve
- **Elevated risk**: 30–50% deployed
- **Drawdown >10%**: 20–30% deployed
- **Max concurrent positions**: 5–10 depending on account size

### 6. Correlation Management

Crypto assets correlate >0.7 during sell-offs. Effective diversification requires:

- Treat all meme tokens as a single correlated bucket
- Limit total meme exposure to one position-size equivalent
- Diversify across *strategies* (trend, mean-reversion, scalp), not just tokens
- Monitor rolling correlation and reduce when correlations spike

See `references/exposure_limits.md` for detailed limits by token type and strategy.

## Drawdown Management

### Response Framework

| Drawdown | Status | Response |
|---|---|---|
| 0–5% | Normal | Continue trading at full size |
| 5–10% | Caution | Reduce position sizes by 25–50% |
| 10–15% | Warning | Minimum position sizes only |
| 15–20% | Critical | Halt new trades, manage existing positions only |
| >20% | Emergency | Full stop, review everything before resuming |

### Recovery Requirements

| Loss | Required Gain to Recover |
|---|---|
| -5% | +5.3% |
| -10% | +11.1% |
| -15% | +17.6% |
| -20% | +25.0% |
| -30% | +42.9% |
| -40% | +66.7% |
| -50% | +100.0% |

The asymmetry accelerates rapidly. Managing small drawdowns prevents them from becoming catastrophic. See `references/drawdown_management.md` for the full framework.

## Circuit Breakers

Automated controls that restrict trading when conditions are met:

### Time-Based
- No trading for 24 hours after hitting daily loss limit
- 48-hour cooling period after weekly loss limit
- Mandatory weekly review day (no new positions)

### Loss-Based
- 3 consecutive losses → reduce size 50%
- 5 consecutive losses → minimum size only
- 7 consecutive losses → halt 24 hours, full review

### Volatility-Based
- Portfolio volatility >2× rolling average → reduce exposure 50%
- Market-wide liquidation events → pause all new entries
- Individual token volatility spike → exit or tighten stops

### Emotional (Self-Assessed)
- Recognize tilt: anger after losses, urge to "make it back"
- FOMO: rushing entries without proper analysis
- Overconfidence: increasing size after a win streak without justification

See `references/circuit_breakers.md` for implementation details.

## Risk Metrics

### Value at Risk (VaR)

95th-percentile daily loss estimate using historical returns:

```python
import numpy as np

def historical_var(returns: list[float], confidence: float = 0.95) -> float:
    """Calculate historical VaR at given confidence level."""
    sorted_returns = sorted(returns)
    index = int((1 - confidence) * len(sorted_returns))
    return abs(sorted_returns[index])

# Example: 95% VaR of 3.2% means on 95% of days, loss won't exceed 3.2%
```

### Expected Shortfall (CVaR)

Average loss in the worst (1 - confidence)% of scenarios:

```python
def expected_shortfall(returns: list[float], confidence: float = 0.95) -> float:
    """Average loss beyond VaR threshold."""
    sorted_returns = sorted(returns)
    index = int((1 - confidence) * len(sorted_returns))
    tail = sorted_returns[:index]
    return abs(sum(tail) / len(tail)) if tail else 0.0
```

### Maximum Drawdown

```python
def max_drawdown(equity_curve: list[float]) -> float:
    """Peak-to-trough decline as a fraction."""
    peak = equity_curve[0]
    max_dd = 0.0
    for value in equity_curve:
        peak = max(peak, value)
        dd = (peak - value) / peak
        max_dd = max(max_dd, dd)
    return max_dd
```

### Additional Metrics

- **Win/loss streak tracking**: Detect hot/cold streaks for circuit breaker logic
- **Rolling Sharpe ratio**: 30-day rolling risk-adjusted returns
- **Calmar ratio**: Annualized return / max drawdown
- **Sortino ratio**: Return / downside deviation (penalizes only negative volatility)

## Crypto-Specific Risks

### Smart Contract Risk
- Never allocate >5% of account to a single unaudited protocol
- Diversify across audited protocols for yield strategies
- Monitor exploit databases and social channels for emerging threats

### Rug Pull Risk
- Size inversely with token age: newer tokens get smaller positions
- Verify: locked liquidity, renounced mint authority, holder distribution
- Cross-reference with `token-holder-analysis` skill for red flags

### Bridge and Custody Risk
- Don't hold >20% on any single platform or bridge
- Self-custody the majority of trading capital
- Budget for bridge fees and delays in execution planning

### MEV and Execution Risk
- Budget 1–3% for MEV/slippage on Solana DEX trades
- Use priority fees during congestion
- See `slippage-modeling` skill for detailed cost estimation

### Correlation Spikes
- In crashes, crypto correlations approach 1.0
- Your "diversified" portfolio may behave as one position
- Stress-test portfolio assuming all positions drop simultaneously

## PumpFun Risk Framework

PumpFun and similar meme token platforms require a distinct risk approach:

### Core Principle
Treat every PumpFun trade as a potential 100% loss. Size accordingly.

### Position Limits
- **Per-token maximum**: 0.1–0.5 SOL
- **Daily PumpFun budget**: Fixed allocation (e.g., 2 SOL/day)
- **Never exceed budget**: When daily allocation is gone, stop

### Tracking
- Track PumpFun P&L separately from main portfolio
- Calculate PumpFun win rate and expectancy independently
- Don't let PumpFun losses affect main portfolio risk limits

### Risk Adjustments
- No stop-losses on PumpFun (assume 100% loss at entry)
- Take profits aggressively: 2×, 3×, 5× partial exits
- Time-based exit: close within hours, not days

## Integration with Other Skills

- **`position-sizing`**: Use risk limits from this skill to constrain position sizes
- **`exit-strategies`**: Circuit breakers override exit strategies (forced exits)
- **`portfolio-analytics`**: Feed portfolio metrics back for risk assessment
- **`liquidity-analysis`**: Adjust position limits based on available liquidity
- **`slippage-modeling`**: Factor execution costs into risk calculations

## Files

### References
- `references/drawdown_management.md` — Drawdown math, response framework, causes, and remediation
- `references/exposure_limits.md` — Position limits by token type, portfolio limits, correlation management
- `references/circuit_breakers.md` — Implementation details for all circuit breaker types

### Scripts
- `scripts/risk_dashboard.py` — Portfolio risk dashboard with limit checking and color-coded status
- `scripts/drawdown_analyzer.py` — Equity curve drawdown analysis with response recommendations

## Quick Start

```bash
# Run the risk dashboard with demo data
python scripts/risk_dashboard.py --demo

# Analyze drawdowns on a demo equity curve
python scripts/drawdown_analyzer.py --demo
```

### Referencia: references/circuit_breakers.md

# Circuit Breakers

Automated controls that restrict or halt trading activity when predefined conditions are met. Circuit breakers protect against compounding losses, emotional decisions, and system failures.

## Daily Loss Limit

### Implementation

```python
from datetime import datetime, timezone

class DailyLossBreaker:
    """Track daily P&L and halt trading when limit is hit."""

    def __init__(self, account_size: float, limit_pct: float = 0.03):
        self.account_size = account_size
        self.limit_pct = limit_pct
        self.limit_amount = account_size * limit_pct
        self.realized_pnl = 0.0
        self.unrealized_pnl = 0.0
        self.reset_date = datetime.now(timezone.utc).date()
        self.consecutive_limit_days = 0

    def update(self, realized: float, unrealized: float) -> None:
        today = datetime.now(timezone.utc).date()
        if today != self.reset_date:
            if self.is_triggered():
                self.consecutive_limit_days += 1
            else:
                self.consecutive_limit_days = 0
            self.realized_pnl = 0.0
            self.unrealized_pnl = 0.0
            self.reset_date = today
        self.realized_pnl = realized
        self.unrealized_pnl = unrealized

    def total_pnl(self) -> float:
        return self.realized_pnl + self.unrealized_pnl

    def is_triggered(self) -> bool:
        return self.total_pnl() <= -self.limit_amount

    def needs_weekly_halt(self) -> bool:
        return self.consecutive_limit_days >= 3
```

### Rules

| Rule | Detail |
|---|---|
| Tracking | Realized P&L + unrealized P&L combined |
| Trigger | Stop opening new positions when limit hit |
| Existing positions | May be managed (tighten stops) but not added to |
| Reset | Midnight UTC |
| Escalation | 3 consecutive days hitting limit → halt for remainder of week |

### Recommended Limits

| Profile | Daily Limit | Weekly Escalation |
|---|---|---|
| Conservative | -3% | 2 consecutive days |
| Moderate | -4% | 3 consecutive days |
| Aggressive | -5% | 3 consecutive days |

## Consecutive Loss Breaker

### Implementation

```python
class ConsecutiveLossBreaker:
    """Track consecutive losses and enforce size/halt rules."""

    def __init__(self):
        self.consecutive_losses = 0
        self.consecutive_wins = 0

    def record_trade(self, pnl: float) -> None:
        if pnl < 0:
            self.consecutive_losses += 1
            self.consecutive_wins = 0
        elif pnl > 0:
            self.consecutive_wins += 1
            if self.consecutive_wins >= 2:
                self.consecutive_losses = 0

    def size_multiplier(self) -> float:
        if self.consecutive_losses >= 7:
            return 0.0  # Halt
        elif self.consecutive_losses >= 5:
            return 0.25  # Minimum size
        elif self.consecutive_losses >= 3:
            return 0.50  # Half size
        return 1.0  # Full size

    def status(self) -> str:
        if self.consecutive_losses >= 7:
            return "HALT — 7+ consecutive losses, 24h mandatory break"
        elif self.consecutive_losses >= 5:
            return "MINIMUM SIZE — 5+ consecutive losses"
        elif self.consecutive_losses >= 3:
            return "HALF SIZE — 3+ consecutive losses"
        return "NORMAL"
```

### Rules

| Consecutive Losses | Action | Reset Condition |
|---|---|---|
| 3 | Reduce position size by 50% | 2 consecutive wins |
| 5 | Minimum position size only | 2 consecutive wins |
| 7 | Halt trading for 24 hours | 24h elapsed + review complete |
| 10+ | Full stop, strategy review | Complete strategy audit |

### Reset Logic

- Consecutive loss counter resets after 2 consecutive wins (not 1, to avoid whipsaw)
- After a 7+ loss halt, counter resets only after the mandatory break AND 2 consecutive wins in paper trading
- The counter persists across days — it tracks consecutive trade outcomes, not daily

## Volatility Circuit Breaker

### Implementation

```python
import numpy as np

class VolatilityBreaker:
    """Monitor portfolio volatility and restrict trading in extreme conditions."""

    def __init__(self, lookback: int = 20, trigger_multiple: float = 2.0,
                 reset_multiple: float = 1.5):
        self.lookback = lookback
        self.trigger_multiple = trigger_multiple
        self.reset_multiple = reset_multiple
        self.returns: list[float] = []
        self.baseline_vol: float | None = None

    def update(self, daily_return: float) -> None:
        self.returns.append(daily_return)
        if len(self.returns) > self.lookback * 3:
            self.returns = self.returns[-self.lookback * 3:]
        if len(self.returns) >= self.lookback:
            self.baseline_vol = float(np.std(self.returns[-self.lookback:]))

    def current_vol(self, window: int = 5) -> float | None:
        if len(self.returns) < window:
            return None
        return float(np.std(self.returns[-window:]))

    def is_triggered(self) -> bool:
        if self.baseline_vol is None:
            return False
        current = self.current_vol()
        if current is None:
            return False
        return current > self.baseline_vol * self.trigger_multiple

    def is_reset(self) -> bool:
        if self.baseline_vol is None:
            return True
        current = self.current_vol()
        if current is None:
            return True
        return current <= self.baseline_vol * self.reset_multiple
```

### Rules

| Condition | Trigger | Action | Reset |
|---|---|---|---|
| Short-term vol > 2× baseline | Triggered | Reduce exposure to 50%, widen stops | Vol drops below 1.5× baseline |
| Short-term vol > 3× baseline | Extreme | Reduce exposure to 25%, exit weak setups | Vol drops below 2× baseline |
| Market-wide liquidation event | Manual | Halt all entries | Manual assessment complete |

### Crypto Volatility Indicators

- SOL 1-hour realized volatility vs 7-day average
- BTC dominance change rate (rapid shifts signal risk-off)
- DEX volume spikes (>3× average may indicate panic)
- Funding rates extreme readings (>0.1% or <-0.1%)

## System Failure Breaker

### Triggers

| Failure Type | Trigger | Action |
|---|---|---|
| API errors | 3+ consecutive failed API calls | Halt new trades |
| RPC failures | Primary + backup RPC unreachable | Halt all activity |
| Price feed stale | No price update for >60 seconds | Halt new trades |
| Unexpected P&L | Single trade P&L > 5× expected | Halt, investigate |
| Execution anomaly | Fill price >5% from expected | Halt, investigate |

### Recovery

1. Identify the failure and confirm it is resolved
2. Verify all position data is accurate (reconcile on-chain state)
3. Resume with reduced size for first 3 trades
4. Return to normal only after 3 successful trades at reduced size

## Combining Circuit Breakers

Multiple breakers can be active simultaneously. Use the most restrictive rule:

```python
def effective_size_multiplier(
    daily_loss_breaker: DailyLossBreaker,
    consecutive_loss_breaker: ConsecutiveLossBreaker,
    volatility_breaker: VolatilityBreaker,
) -> float:
    """Return the most restrictive size multiplier across all breakers."""
    multipliers = []

    if daily_loss_breaker.is_triggered():
        multipliers.append(0.0)
    if consecutive_loss_breaker.size_multiplier() < 1.0:
        multipliers.append(consecutive_loss_breaker.size_multiplier())
    if volatility_breaker.is_triggered():
        multipliers.append(0.5)

    return min(multipliers) if multipliers else 1.0
```

## Implementation Checklist

- [ ] Implement daily loss tracking (realized + unrealized)
- [ ] Set up daily loss limit with UTC reset
- [ ] Track consecutive losses across all strategies
- [ ] Calculate rolling portfolio volatility
- [ ] Define volatility baseline (20-period rolling std)
- [ ] Set up system health monitoring (API, RPC, price feeds)
- [ ] Log all circuit breaker activations with timestamp and cause
- [ ] Review circuit breaker thresholds monthly
- [ ] Test breaker logic with simulated extreme scenarios
- [ ] Ensure breakers cannot be overridden without explicit acknowledgment

### Referencia: references/drawdown_management.md

# Drawdown Management

Comprehensive framework for detecting, responding to, and recovering from portfolio drawdowns in crypto trading.

## Drawdown Mathematics

### Recovery Table

A drawdown of X% requires a gain greater than X% to recover, and the relationship is nonlinear:

| Drawdown | Required Gain | Ratio |
|---|---|---|
| -1% | +1.01% | 1.01× |
| -2% | +2.04% | 1.02× |
| -3% | +3.09% | 1.03× |
| -5% | +5.26% | 1.05× |
| -7% | +7.53% | 1.08× |
| -10% | +11.11% | 1.11× |
| -15% | +17.65% | 1.18× |
| -20% | +25.00% | 1.25× |
| -25% | +33.33% | 1.33× |
| -30% | +42.86% | 1.43× |
| -35% | +53.85% | 1.54× |
| -40% | +66.67% | 1.67× |
| -45% | +81.82% | 1.82× |
| -50% | +100.00% | 2.00× |
| -60% | +150.00% | 2.50× |
| -70% | +233.33% | 3.33× |
| -80% | +400.00% | 5.00× |
| -90% | +900.00% | 10.00× |

**Formula**: `required_gain = drawdown / (1 - drawdown)`

### Why Small Drawdowns Matter

At -10%, recovery is manageable (+11.1%). At -20%, it becomes difficult (+25%). Past -30%, recovery is unlikely without exceptional conditions. The priority is always to keep drawdowns small.

A trader earning 1% per day on average needs:
- 6 trading days to recover from -5%
- 11 days to recover from -10%
- 25 days to recover from -20%
- 100 days to recover from -50%

## Drawdown Detection

### Calculating Current Drawdown

```python
def current_drawdown(equity_curve: list[float]) -> float:
    """Calculate current drawdown from peak.

    Returns:
        Drawdown as a positive fraction (0.10 = 10% drawdown).
    """
    peak = max(equity_curve)
    current = equity_curve[-1]
    if peak <= 0:
        return 0.0
    return (peak - current) / peak
```

### Rolling Peak Tracking

Track the high-water mark continuously:

```python
def rolling_peak(equity_curve: list[float]) -> list[float]:
    """Calculate rolling peak (high-water mark) at each point."""
    peaks = []
    current_peak = equity_curve[0]
    for value in equity_curve:
        current_peak = max(current_peak, value)
        peaks.append(current_peak)
    return peaks
```

### Drawdown Duration

Track not just depth but how long the portfolio has been underwater:

```python
def time_underwater(equity_curve: list[float]) -> int:
    """Count periods since last equity high."""
    peak = equity_curve[0]
    periods = 0
    for value in equity_curve:
        if value >= peak:
            peak = value
            periods = 0
        else:
            periods += 1
    return periods
```

## Drawdown Response Framework

### Level 0: Normal (0–5% drawdown)
- **Detection**: Equity within 5% of peak
- **Action**: Continue trading at full size
- **Monitoring**: Standard daily P&L review
- **Psychology**: Expected fluctuation, no concern

### Level 1: Caution (5–10% drawdown)
- **Detection**: Alert triggers at 5% threshold
- **Action**: Reduce position sizes by 25–50%
- **Monitoring**: Review each trade more carefully before entry
- **Psychology**: Increased discipline, no revenge trading
- **Additional**: Review recent trades for pattern of errors

### Level 2: Warning (10–15% drawdown)
- **Detection**: Alert triggers at 10% threshold
- **Action**: Trade at minimum position sizes only
- **Monitoring**: Daily strategy review, check for edge decay
- **Psychology**: Accept the drawdown, focus on process not P&L
- **Additional**: Consider whether market regime has changed

### Level 3: Critical (15–20% drawdown)
- **Detection**: Alert triggers at 15% threshold
- **Action**: Halt all new trades, manage existing positions only
- **Monitoring**: Review entire strategy, check assumptions
- **Psychology**: Step back, no trading decisions while emotional
- **Additional**: Consult trading journal for similar past periods

### Level 4: Emergency (>20% drawdown)
- **Detection**: Alert triggers at 20% threshold
- **Action**: Full stop — close positions systematically, not in panic
- **Monitoring**: Complete portfolio review before any resumption
- **Psychology**: Mandatory break (48–72 hours minimum)
- **Additional**: Re-evaluate all strategies, parameters, and risk limits

## Recovery Criteria

Before resuming normal-size trading after a drawdown halt:

1. **Time requirement**: Minimum 48 hours of no trading
2. **Analysis complete**: Root cause identified and documented
3. **Strategy validated**: Backtested the strategy on recent data
4. **Paper trading**: 5–10 simulated trades showing the edge still exists
5. **Gradual ramp**: Start at 25% size → 50% → 75% → 100% over 1–2 weeks

## Drawdown Causes and Remediation

### Strategy Decay
- **Symptoms**: Win rate declining over weeks/months, not days
- **Cause**: The edge was arbitraged away or market structure changed
- **Remediation**: Retire the strategy, develop new ones on out-of-sample data

### Regime Change
- **Symptoms**: Sudden performance drop, previously profitable setups failing
- **Cause**: Market shifted (trending → ranging, low vol → high vol)
- **Remediation**: Add regime detection, adapt parameters per regime
- **Reference**: See `regime-detection` skill

### Overexposure
- **Symptoms**: Multiple positions stopping out simultaneously
- **Cause**: Too many correlated positions
- **Remediation**: Enforce correlation limits, reduce concurrent positions

### Emotional Trading
- **Symptoms**: Deviation from plan, increasing size after losses, FOMO entries
- **Cause**: Psychological response to losses
- **Remediation**: Enforce circuit breakers, journal every trade, take breaks

### Incorrect Position Sizing
- **Symptoms**: Single trades causing outsized impact on portfolio
- **Cause**: Position sizes too large relative to stop distance or account size
- **Remediation**: Review `position-sizing` skill, enforce maximum risk per trade

## Historical Drawdown Tracking

Maintain a drawdown log with these fields for every significant drawdown (>5%):

| Field | Description |
|---|---|
| Start date | When equity first dropped below prior peak |
| Trough date | Date of maximum drawdown depth |
| Recovery date | When equity returned to prior peak (or N/A) |
| Depth | Maximum drawdown percentage |
| Duration | Start to trough (periods) |
| Recovery time | Trough to recovery (periods) |
| Cause | Primary cause category |
| Lessons | Key takeaways documented |

This log is invaluable for identifying patterns: Are drawdowns seasonal? Strategy-specific? Correlated with market events?

## Key Principles

1. **Drawdowns are inevitable** — The goal is management, not avoidance
2. **Small drawdowns are recoverable** — Keep them under 15%
3. **Time heals, size kills** — A small position that goes wrong is a learning opportunity; a large one is a disaster
4. **Process over outcome** — Follow the framework even when it feels overly cautious
5. **Document everything** — Future you will thank present you for the drawdown log

### Referencia: references/exposure_limits.md

# Exposure Limits

Detailed position and portfolio exposure constraints for crypto trading risk management.

## Single Position Limits

### By Token Type

Token classification determines maximum position size as a percentage of total account value:

| Token Type | Examples | Max Position | Rationale |
|---|---|---|---|
| Blue chip | SOL, ETH, BTC | 10% | High liquidity, lower rug risk |
| Large cap | RAY, JUP, BONK | 7% | Established but more volatile |
| Mid cap | Top 100 by mcap | 5% | Moderate liquidity risk |
| Small cap | Top 500 by mcap | 2% | Significant liquidity/rug risk |
| Micro cap | Sub-$10M mcap | 1% | Very high risk |
| PumpFun/meme | New launches | 0.5% | Assume potential 100% loss |

### By Strategy Type

Different strategies carry different risk profiles:

| Strategy | Max Position | Rationale |
|---|---|---|
| Trend following | 5% | Wider stops, longer holds |
| Mean reversion | 3% | Can gap through stop levels |
| Momentum/scalp | 2% | High frequency, errors compound |
| Breakout | 3% | False breakouts are common |
| PumpFun snipe | 0.5% | Binary outcome expected |

### By Confidence Level

Scale position size with conviction, but never exceed token-type limits:

| Confidence | Size Multiplier | Criteria |
|---|---|---|
| High | 100% of allowed max | Multiple confirming signals, strong setup |
| Medium | 50% of allowed max | Decent setup, some conflicting signals |
| Low | 25% of allowed max | Marginal setup, taking for diversification |

**Example**: High confidence on a mid-cap token = 5% × 100% = 5% position. Low confidence on same = 5% × 25% = 1.25%.

## Portfolio-Level Limits

### Total Exposure

Percentage of total account value deployed in open positions:

| Market Condition | Max Exposure | Cash Reserve |
|---|---|---|
| Strong trend, low vol | 80% | 20% |
| Normal conditions | 60% | 40% |
| High volatility | 40% | 60% |
| Drawdown >10% | 30% | 70% |
| Drawdown >15% | 20% | 80% |
| Circuit breaker active | 0% (existing only) | 100% |

### Cash Reserve Purpose

The cash reserve serves multiple functions:
1. **Opportunity capital**: Ability to take advantage of sudden setups
2. **Margin buffer**: Prevents forced liquidations on leveraged positions
3. **Psychological comfort**: Reduces pressure to exit positions prematurely
4. **Drawdown cushion**: Limits portfolio drawdown speed

### Maximum Concurrent Positions

| Account Size (SOL) | Max Positions | Rationale |
|---|---|---|
| <10 | 3 | Focus, meaningful size per trade |
| 10–50 | 5 | Moderate diversification |
| 50–200 | 7 | Balanced diversification |
| 200–1000 | 10 | Full diversification |
| >1000 | 15 | Diminishing returns beyond this |

### Sector Concentration

Maximum allocation to any single narrative or sector:

| Sector | Max Allocation |
|---|---|
| DeFi protocols | 30% |
| Meme/culture tokens | 15% |
| Infrastructure/L1/L2 | 30% |
| Gaming/NFT-adjacent | 20% |
| AI tokens | 20% |
| Stablecoins (non-reserve) | 10% |

## Correlation Management

### The Correlation Problem

During normal markets, crypto assets may show moderate correlation (0.3–0.5). During sell-offs, correlations spike to 0.7–0.9+. A "diversified" portfolio of 10 crypto tokens may behave like 2–3 independent positions in a crash.

### Effective Diversification

**What does NOT diversify well**:
- Multiple meme tokens (all driven by same sentiment)
- Multiple DeFi tokens (correlated with DeFi TVL)
- Multiple tokens on the same chain (correlated with chain activity)
- Long-only positions across any crypto tokens (all correlate with BTC)

**What DOES diversify**:
- Different strategies: trend + mean-reversion + market-neutral
- Different timeframes: scalp + swing + position
- Different exposures: long + short (when available)
- Cash reserves (zero correlation by definition)

### Correlation Buckets

Group positions into correlation buckets and apply limits per bucket:

| Bucket | Contents | Max Allocation |
|---|---|---|
| BTC-correlated | BTC, SOL, ETH, major L1s | 30% |
| DeFi | DEX tokens, lending, yield | 20% |
| Meme | All meme/culture tokens | 15% |
| Stablecoin yield | LP positions, lending | 20% |
| Uncorrelated | Market-neutral strategies | No limit |

### Calculating Portfolio Correlation

```python
import numpy as np

def portfolio_correlation(returns_matrix: np.ndarray) -> float:
    """Average pairwise correlation of portfolio assets.

    Args:
        returns_matrix: N×T matrix (N assets, T time periods).

    Returns:
        Average pairwise correlation coefficient.
    """
    corr = np.corrcoef(returns_matrix)
    n = corr.shape[0]
    # Extract upper triangle (excluding diagonal)
    upper = corr[np.triu_indices(n, k=1)]
    return float(np.mean(upper))
```

## Dynamic Limit Adjustments

### Tightening During Drawdowns

When the portfolio is in drawdown, tighten all limits proportionally:

```python
def adjusted_limit(base_limit: float, drawdown: float) -> float:
    """Reduce limits during drawdowns.

    Args:
        base_limit: Normal limit (e.g., 0.05 for 5%).
        drawdown: Current drawdown as fraction (e.g., 0.10 for 10%).

    Returns:
        Adjusted limit, reduced proportionally.
    """
    if drawdown < 0.05:
        return base_limit
    elif drawdown < 0.10:
        return base_limit * 0.75
    elif drawdown < 0.15:
        return base_limit * 0.50
    else:
        return base_limit * 0.25
```

### Widening During Strong Performance

Expand limits cautiously when the portfolio is performing well:

- Only expand after 20+ days of positive equity curve slope
- Maximum expansion: 125% of base limits (never more)
- Revert to base limits immediately if drawdown begins
- Never expand PumpFun or micro-cap limits regardless of performance

### Seasonal Adjustments

Historical crypto volatility patterns suggest:
- **Reduce exposure**: During major token unlock events, regulatory announcements
- **Standard exposure**: Normal market conditions
- **Increase caution**: Holiday periods (low liquidity), end-of-quarter (fund rebalancing)

## Implementation Checklist

- [ ] Define token-type classification for each traded asset
- [ ] Set strategy-specific position limits
- [ ] Configure total exposure limits for current market regime
- [ ] Set up sector tracking and concentration alerts
- [ ] Calculate correlation buckets and apply bucket limits
- [ ] Implement dynamic adjustment based on drawdown level
- [ ] Review and update limits monthly


---

## SKILL: sox-walkthrough

- Fuente: `SYasJ/claude-business-skills` → `plugins/risk/skills/sox-walkthrough` (MIT)
- Cuándo usarla: Prepare a walkthrough of a financial control so the performer can show what they actually do. Use when the user mentions SOX walkthrough, control walkthrough prep, audit walkthrough, ICFR prep, or asks for a SOX walkthrough prep. Risk and compliance skill by Yasir Jilani.

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'sox-walkthrough' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# SOX Walkthrough Prep

Prepare a walkthrough of a financial control so the performer can show what they actually do.

## When to use this skill

Use this skill when the user:

- SOX walkthrough
- control walkthrough prep
- audit walkthrough
- ICFR prep

## When not to use this skill

- Misleading an auditor

## Professional boundary

Risk work prioritizes uncertainty. It is not a certification. Do not claim SOC 2, ISO, HIPAA, or similar compliance unless the user has evidence of it.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The control description
- The performer
- The evidence
- The period

## Workflow


### 1. Step 1

Restate the risk and the control in plain language.
### 2. Step 2

Ask the performer to walk a real transaction, not a theoretical one.
### 3. Step 3

Match the walk to the control description. Differences are findings, not things to hide.
### 4. Step 4

Identify missing evidence before the auditor does, and say so to management.
### 5. Step 5

Do not coach anyone to misrepresent the control.
### 6. Step 6

Note samples you did not test. A prep is not a test of operating effectiveness.

## Output

Deliver a **SOX walkthrough prep**.

- Purpose of this SOX walkthrough prep, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a SOX walkthrough prep by 30 September 2026. A manager wants the performer to describe a review that does not happen.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A manager wants the performer to describe a review that does not happen.

The control description: their one-page rule dated 2 Mar 2026. No exception log since
The performer: Control 7.2 access review, recorded 14 September 2026. No supporting file attached
The evidence: one PDF, 2 pages, dated 14 September 2026
The period: month ending 14 September 2026
```

### Example outcome

**Sox walkthrough prep**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Refuses the false story and writes the gap for management.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The control description | their one-page rule dated 2 Mar 2026. No exception log since | Needs confirmation |
| The performer | Control 7.2 access review, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The evidence | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| The period | month ending 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Restate the risk and the control in plain language**

**2. Ask the performer to walk a real transaction, not a theoretical one**

**3. Match the walk to the control description. Differences are findings, not things to hide**

**4. Identify missing evidence before the auditor does, and say so to management**

**5. Do not coach anyone to misrepresent the control**

**Deliberately not done**
- Coaching a false story.
- Hiding a gap.
- Claiming effectiveness from a prep chat.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Coaching a false story
- Hiding a gap
- Claiming effectiveness from a prep chat

## Related skills

- `control-design`
- `audit-response`


---

## SKILL: third-party-risk

- Fuente: `SYasJ/claude-business-skills` → `plugins/risk/skills/third-party-risk` (MIT)
- Cuándo usarla: Screen a third party for the risk created by the access and data you will give them. Use when the user mentions third-party risk, vendor risk, supplier risk review, outsourcing risk, or asks for a third-party risk note. Risk and compliance skill by Yasir Jilani.

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'third-party-risk' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Third-Party Risk

Screen a third party for the risk created by the access and data you will give them.

## When to use this skill

Use this skill when the user:

- third-party risk
- vendor risk
- supplier risk review
- outsourcing risk

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Risk work prioritizes uncertainty. It is not a certification. Do not claim SOC 2, ISO, HIPAA, or similar compliance unless the user has evidence of it.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The service
- Data and access involved
- Their evidence
- The business owner

## Workflow


### 1. Step 1

Rate inherent risk from access and data, in plain tiers you label as a proposal if they have no method.
### 2. Step 2

Review only evidence they collected. A missing questionnaire is a gap.
### 3. Step 3

Recommend a lighter review for low access and a deeper one for sensitive data.
### 4. Step 4

Name the business owner who accepts residual risk.
### 5. Step 5

Tie contract questions to the legal and security skills. Do not duplicate a fake certification.
### 6. Step 6

Re-review on a date or when the service changes.

## Output

Deliver a **third-party risk note**.

- Purpose of this third-party risk note, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a third-party risk note by 30 September 2026. A design tool and a payroll processor are put through an identical unread checklist.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A design tool and a payroll processor are put through an identical unread checklist.

The service: the one named in the ask. Version and owner not recorded
Data and access involved: Control 7.2 access review. Partly documented: the what is written down, the who is not
Their evidence: one PDF, 2 pages, dated 14 September 2026
The business owner: Priya Shah, controller
```

### Example outcome

**Third-party risk note**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Deepens the payroll review, lightens the design-tool review, and names the owner.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The service | the one named in the ask. Version and owner not recorded | Needs confirmation |
| Data and access involved | Control 7.2 access review. Partly documented: the what is written down, the who is not | Carried into the draft |
| Their evidence | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| The business owner | Priya Shah, controller | Needs confirmation |

**How this draft was built**

**1. Rate inherent risk from access and data, in plain tiers you label as a proposal if they have no method**

**2. Review only evidence they collected. A missing questionnaire is a gap**

**3. Recommend a lighter review for low access and a deeper one for sensitive data**

**4. Name the business owner who accepts residual risk**

**5. Tie contract questions to the legal and security skills. Do not duplicate a fake certification**

**Deliberately not done**
- The same heavy review for every vendor regardless of data.
- A pass with no evidence.
- No business owner.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- The same heavy review for every vendor regardless of data
- A pass with no evidence
- No business owner

## Related skills

- `vendor-security-review`
- `vendor-ops-review`


---

## SKILL: trade-performance-coach

- Fuente: `tradermonty/claude-trading-skills` → `skills/trade-performance-coach` (MIT)
- Cuándo usarla: >-
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/trade-performance-coach/` (performance_coach_report.schema.json, requirements.txt, review_trade_performance.py)

# Trade Performance Coach

## Overview

Trade Performance Coach reviews recorded trade outcomes and journal evidence to
help a human trader improve their decision process. It converts closed-trade
records, postmortem findings, risk rules, and optional market-regime context into
an evidence-based coaching report covering:

- process adherence
- risk discipline
- execution quality
- possible trading-behavior patterns
- next-session operating rules
- coach questions for reflection

This skill is intended to fill the support role that a risk manager, desk lead,
or trading coach might provide in a professional trading environment. It is
strictly a process-review skill: it never recommends entering, exiting, buying,
selling, shorting, holding, or sizing a specific security.

## When to Use

Use this skill when any of the following are true:

- A trade has been closed and the user wants a post-trade coaching review.
- A partial close occurred and the user wants to inspect sizing, stop, or exit behavior.
- The user has `trader-memory-core` thesis records and `signal-postmortem` findings and wants next-session operating rules.
- The user wants a monthly review of recurring process, risk, execution, or behavior patterns.
- The user asks for a risk-manager style review of their own recorded trades.
- The user asks whether a loss was a process error, execution error, market environment issue, or acceptable variance.
- The user wants possible FOMO, revenge-trade, overconfidence, hesitation, stop-moving, or size-creep patterns flagged with evidence.

## When Not to Use

Do not use this skill to:

- Pick stocks or rank trade candidates.
- Approve or reject a live trade as financial advice.
- Place orders or draft broker instructions.
- Provide therapy, mental-health diagnosis, or personality assessment.
- Infer private psychological traits beyond the trade evidence supplied.
- Shame the user for losses or rule violations.
- Replace `trader-memory-core`; this skill consumes journal/thesis records and produces coaching findings.

If the input is incomplete, default to `REVIEW_REQUIRED` or `journal_only` mode and ask for missing records rather than inventing evidence.

## Prerequisites

Recommended upstream records:

- `trader-memory-core` closed thesis record or journal entry
- `signal-postmortem` postmortem findings
- original trade plan or trade ticket
- actual entry / exit / partial-close actions
- user-defined risk plan, if available
- optional `market-regime-daily` / `exposure-coach` context

No paid API key is required. The deterministic script works from local JSON/YAML-like records.

## Inputs

Minimum useful input is one recorded trade or one monthly aggregate.

Preferred fields:

```yaml
review_type: single_trade | partial_close | monthly_aggregate
trade_id: string
ticker: string
outcome: win | loss | breakeven | mixed
planned:
  thesis: string
  entry: number
  stop: number
  target: number
  risk_r: number
  thesis_recorded_before_entry: boolean
  setup_confirmed: boolean
  market_regime: allowed | restrictive | cash_priority | unknown
actual:
  entry: number
  exit: number
  risk_r: number
  portfolio_heat_r: number
  stop_moved: boolean
  stop_move_planned: boolean
  entry_before_confirmation: boolean
  traded_against_regime: boolean
risk_plan:
  max_risk_per_trade_r: number
  max_portfolio_heat_r: number
  max_weekly_loss_r: number
postmortem:
  root_cause: thesis_quality | execution | risk_sizing | market_environment | rule_violation | randomness | unknown
  notes: [string]
journal:
  reflection: string
  emotions: [string]
monthly:
  trades: [object]
  consecutive_losses: number
  rule_violations: number
```

The script tolerates partial records. Missing evidence is marked as `unclear`.

For the numeric fields actually evaluated (`planned.risk_r`, `actual.risk_r`,
`risk_plan.max_risk_per_trade_r`, `actual.portfolio_heat_r`,
`risk_plan.max_portfolio_heat_r`, and `monthly.consecutive_losses`), supplied
non-null values must be finite and nonnegative. Numeric strings and zero are
accepted; consecutive losses must be a whole number. Booleans, negative values,
NaN, infinity, malformed strings, and conversion overflow are rejected. An
explicitly invalid maximum never falls back to planned risk. Missing/null fields
retain the partial-record behavior. The CLI validates every source record,
including multiple inputs, and returns exit code 2 with a field-specific error
before creating or modifying reports when a numeric value is invalid.

This skill remains beta. Numeric validation does not establish production
readiness; report-ID path safety and the documented shallow multi-input wrapper
still require separate assessment.

## Workflow

### Step 1 — Collect source records

Collect the most recent closed trade record, postmortem, risk plan, and journal notes.

```bash
python3 skills/trade-performance-coach/scripts/review_trade_performance.py \
  --input reports/trade_memory/closed_thesis_EXMPL.json \
  --output-dir reports/trade-performance-coach
```

### Step 2 — Evaluate process adherence

Compare actual actions against the user's documented plan and rules. Check for:

- missing pre-entry thesis
- setup confirmation skipped
- trade taken against market-regime gate
- stop moved without a pre-defined rule
- exit / partial close inconsistent with plan
- incomplete record quality

### Step 3 — Evaluate risk discipline

Compare actual risk and heat against the risk plan. Check for:

- per-trade risk above max
- portfolio heat above max
- weekly loss or consecutive-loss escalation
- oversized trade after a winner or loser
- correlated exposure if provided

### Step 4 — Evaluate execution quality

Classify entry, stop, exit, add, trim, and review behavior. Separate clean-process losses from execution mistakes.

### Step 5 — Detect possible behavior patterns

Use evidence from journal notes and action flags to tag possible trading behavior patterns. Always tie a tag to evidence and use non-diagnostic language.

Supported MVP tags:

- `fomo_entry`
- `revenge_trade`
- `premature_exit`
- `overconfidence_after_winner`
- `stop_moved`
- `size_creep`
- `hesitation`
- `rule_drift`
- `no_pattern_detected`

### Step 6 — Produce next-session operating rules

Convert findings into temporary, concrete guardrails. Examples:

- require thesis record and screenshot before the next entry
- cap risk at 0.5R for the next two trades after a rule violation
- switch to review-only mode after repeated revenge-trade evidence
- do not chase a missed entry; add to watchlist for the next valid setup

### Step 7 — Human decision gate

End every report with a human decision gate. The default action is `journal_only`.

Allowed actions:

```text
accept_rules / modify_rules / defer / journal_only
```

## Output

The skill produces a JSON report and optionally a Markdown report.

Required top-level JSON fields:

- `schema_version`
- `review_type`
- `review_id`
- `overall_verdict`
- `summary`
- `scores`
- `process_adherence_findings`
- `risk_manager_notes`
- `execution_quality_assessment`
- `behavioral_pattern_tags`
- `next_session_operating_rules`
- `coach_questions`
- `human_decision_gate`
- `disclaimer`

Verdicts:

| Verdict | Meaning |
|---|---|
| `OK` | No material process violation found. Outcome appears compatible with the plan. |
| `WARN` | Minor process or record-quality concern. |
| `REVIEW_REQUIRED` | Meaningful process, risk, or behavior finding before next similar trade. |
| `RULE_VIOLATION` | Explicit user rule appears to have been broken. |
| `COOL_DOWN` | Repeated violations, drawdown/revenge pattern, or escalation suggests review-only mode. |

## Example Command

```bash
python3 skills/trade-performance-coach/scripts/review_trade_performance.py \
  --input skills/trade-performance-coach/scripts/tests/fixtures/single_trade_rule_violation_loss.json \
  --output-dir reports/trade-performance-coach \
  --markdown
```

## Resources

Read these selectively when invoked:

- `references/review-framework.md` — five-axis review model, scoring, verdicts
- `references/behavior-tags.md` — behavior tag definitions and evidence rules
- `references/risk-review-checklist.md` — risk manager checklist and severity rules
- `references/output-contract.md` — JSON output contract and schema notes
- `references/hermes-integration.md` — suggested Hermes `/post-trade-coach` and monthly coaching integration
- `assets/performance_coach_report.schema.json` — machine-readable output schema
- `scripts/review_trade_performance.py` — deterministic local reviewer

## Guardrails

- This is process-review support, not financial advice.
- Do not recommend buying, selling, shorting, holding, or sizing a specific security.
- Do not provide therapy or mental-health diagnosis.
- Do not infer personality traits.
- Do not shame or moralize the user.
- Tie every behavior tag to evidence.
- Use "possible pattern" language for behavior tags.
- Always include a human decision gate.
- Default to journal/review mode when data is incomplete.

### Referencia: references/behavior-tags.md

# Trading Behavior Tags

## Principle

Behavior tags are not psychological diagnoses. They are evidence-based hypotheses
about trading behavior that may explain process drift. Always use language like
"possible pattern" and include evidence plus a reflection question.

## MVP Tags

| Tag | Meaning | Evidence Examples | Guardrail Ideas |
|---|---|---|---|
| `fomo_entry` | Entered because of fear of missing a move rather than setup confirmation. | journal says "didn't want to miss", entry before confirmation, chased above plan | require thesis + screenshot before entry; no chase after missed trigger |
| `revenge_trade` | Trade appears motivated by making back a prior loss. | journal says "make it back", trade immediately after loss, oversized after loss | review-only mode after two losses; 24h delay after max loss |
| `premature_exit` | Exited before plan due to discomfort without invalidation. | exit before stop/target; journal says "got scared" | predefine partial/exit rules; no discretionary exit without invalidation note |
| `overconfidence_after_winner` | Risk increased after a win without rule justification. | actual risk > plan after prior winner; journal says "easy money" | cap risk after large winner; require normal sizing until next review |
| `stop_moved` | Stop was moved after entry without a pre-defined plan. | `actual.stop_moved = true` and not planned | stop changes must be pre-written; unplanned move triggers review |
| `size_creep` | Actual risk or size exceeded risk plan. | actual R > planned max R (explicit comparison) | reduce next trade size; require position-size screenshot |
| `unknown_size_discipline` | Risk discipline could not be assessed because actual.risk_r or the risk plan reference is missing. | position_size warning emitted because actual or reference risk is None | record planned and actual risk on the next trade so size discipline becomes verifiable |
| `hesitation` | Valid plan was not executed due to hesitation. | missed planned entry; journal says "hesitated" | use if/then trigger checklist; define no-entry after missed trigger |
| `rule_drift` | Repeated small deviations from rules. | multiple minor deviations or unclear records | simplify rules; pick one rule to enforce next week |
| `no_pattern_detected` | No behavior pattern detected from available evidence. | clean record with no supportive evidence | no behavior-specific guardrail needed |

## Tagging Rules

1. Never infer personality traits.
2. Never claim a medical or mental-health diagnosis.
3. Use low/medium/high confidence based on evidence strength.
4. Include exactly what evidence supports each tag.
5. Include a reflection question.
6. If evidence is weak, use `confidence: low` or do not tag.

## Reflection Question Examples

- FOMO: "What evidence did you have before entry that would not have been available after waiting for confirmation?"
- Revenge: "Would you have taken this trade if the prior trade had been a winner?"
- Premature exit: "What rule did the exit satisfy, or was it driven by discomfort?"
- Overconfidence: "Did the prior win change the size or quality threshold for this trade?"
- Stop moved: "Was the new stop part of the plan before entry?"
- Size creep: "What would this trade have looked like at the planned risk size?"

### Referencia: references/hermes-integration.md

# Hermes Integration Notes

## Suggested Slash Command: `/post-trade-coach`

Purpose: review a closed or partially closed trade and generate process, risk,
execution, and possible behavior-pattern feedback.

Suggested bundle flow:

```text
trader-memory-core
→ signal-postmortem
→ trade-performance-coach
```

Required output sections:

- Data freshness / source provenance
- Trade summary
- Process adherence
- Risk manager notes
- Execution quality
- Possible behavioral patterns
- Coach questions
- Next-session operating rules
- Human decision gate

## Suggested Slash Command: `/monthly-performance-coach`

Purpose: review recurring process, risk, and behavior patterns across the month.

Suggested bundle flow:

```text
trader-memory-core
→ signal-postmortem
→ trade-performance-coach
→ monthly-performance-review
```

## Guardrails for Hermes Prompts

Hermes prompts should state:

- This is not financial advice.
- This is not therapy or mental-health diagnosis.
- The assistant must not place or prepare broker orders.
- The assistant must not tell the user to buy, sell, short, hold, or size a specific security.
- All recommendations are process guardrails for the human trader to accept, modify, defer, or journal.

## Naming

Existing alias can remain:

```text
trading-research-assistant
```

Future public positioning can broaden to:

```text
Hermes Trading Desk Assistant
```

Suggested subtitle:

```text
A trading desk assistant for research, journaling, risk review, and performance coaching.
```

### Referencia: references/output-contract.md

# Output Contract

## Top-Level JSON

```json
{
  "schema_version": 1,
  "review_type": "single_trade | partial_close | monthly_aggregate",
  "review_id": "string",
  "source_records": ["string"],
  "overall_verdict": "OK | WARN | REVIEW_REQUIRED | RULE_VIOLATION | COOL_DOWN",
  "summary": {
    "outcome": "win | loss | breakeven | open | mixed | unknown",
    "primary_root_cause": "thesis_quality | execution | risk_sizing | market_environment | rule_violation | randomness | unknown",
    "secondary_root_causes": ["string"],
    "confidence": "low | medium | high"
  },
  "scores": {
    "process_score": 0,
    "risk_score": 0,
    "execution_score": 0,
    "review_quality_score": 0
  },
  "process_adherence_findings": [],
  "risk_manager_notes": [],
  "execution_quality_assessment": [],
  "behavioral_pattern_tags": [],
  "next_session_operating_rules": [],
  "coach_questions": [],
  "human_decision_gate": {
    "question": "string",
    "allowed_actions": ["accept_rules", "modify_rules", "defer", "journal_only"],
    "default_action": "journal_only"
  },
  "disclaimer": "string"
}
```

## Findings

Each finding should include:

```json
{
  "rule": "string",
  "status": "met | missed | unclear | not_applicable",
  "evidence": "string",
  "severity": "info | warning | critical"
}
```

Risk notes use:

```json
{
  "topic": "position_size | portfolio_heat | drawdown | correlation | stop_discipline | loss_limit | regime_gate",
  "finding": "string",
  "severity": "info | warning | critical",
  "evidence": "string"
}
```

Behavior tags use:

```json
{
  "tag": "fomo_entry | revenge_trade | premature_exit | overconfidence_after_winner | loss_aversion | rule_drift | stop_moved | size_creep | unknown_size_discipline | hesitation | no_pattern_detected",
  "confidence": "low | medium | high",
  "evidence": "string",
  "reflection_question": "string"
}
```

## Markdown Report

Markdown reports should include:

1. Verdict
2. Trade / period summary
3. Process adherence
4. Risk manager notes
5. Execution quality
6. Possible behavior patterns
7. Next-session operating rules
8. Coach questions
9. Human decision gate
10. Disclaimer

### Referencia: references/review-framework.md

# Trade Performance Coach Review Framework

## Purpose

This framework turns recorded trade evidence into process-improvement feedback.
It evaluates the quality of the trader's decision process, not whether the trade
made money.

A clean-process loss can be acceptable. A profitable rule violation can still be
a serious process problem.

## Five-Axis Review Model

| Axis | Question | Typical Evidence | Output |
|---|---|---|---|
| Thesis Quality | Was the original idea clear, falsifiable, and aligned with the setup? | trade thesis, invalidation, catalyst, setup notes | root-cause finding |
| Process Adherence | Did actual behavior follow the plan and workflow? | entry timing, setup confirmation, thesis record, stop plan | process findings |
| Risk Discipline | Did actual risk follow predefined limits? | planned R, actual R, portfolio heat, weekly loss, correlations | risk manager notes |
| Execution Quality | Were entry, stop, adds/trims, and exits consistent with plan? | execution log, partial close, stop changes | execution assessment |
| Behavior Pattern | Did the journal suggest repeated behavior patterns? | journal text, timing, rule deviations | behavior tags + questions |

## Root-Cause Categories

Use one primary root cause and optional secondary causes:

- `thesis_quality`
- `execution`
- `risk_sizing`
- `market_environment`
- `rule_violation`
- `randomness`
- `unknown`

Classification guidance:

- If the plan was followed and the setup was valid, but the market simply moved
  against the trade, prefer `randomness` or `market_environment`.
- If the trade was taken without the required setup confirmation, prefer
  `execution` or `rule_violation`.
- If the actual risk exceeded the user-defined plan, prefer `risk_sizing`.
- If the user's note shows the trade was taken to make back a prior loss, prefer
  `rule_violation` with a possible `revenge_trade` behavior tag.

## Verdicts

| Verdict | Use When |
|---|---|
| `OK` | The record is complete enough, no material process/risk issue appears, and no behavior pattern is detected. |
| `WARN` | Minor issue, incomplete evidence, or soft process concern. |
| `REVIEW_REQUIRED` | Meaningful process/risk/execution issue, but not a hard rule violation. |
| `RULE_VIOLATION` | Explicit rule breach: risk limit, stop discipline, regime gate, or unplanned add/trim. |
| `COOL_DOWN` | Repeated violations, revenge pattern, drawdown escalation, or multiple critical findings. |

## Scoring

Scores are advisory, not scientific. They help the user compare reviews over
time.

Start at 100 and subtract:

- info finding: 0-5
- warning finding: 10-20
- critical finding: 25-40
- missing critical record: 10-20

Recommended score fields:

```yaml
process_score: 0-100
risk_score: 0-100
execution_score: 0-100
review_quality_score: 0-100
```

`review_quality_score` reflects evidence completeness. Do not over-interpret
behavior tags when review quality is low.

## Next-Session Operating Rules

Each review should produce concrete, temporary operating rules. Good rules are:

- observable
- time-boxed
- tied to evidence
- simple enough to follow before the next trade

Examples:

- "For the next two trades, max planned risk is 0.5R."
- "No entry without a pre-entry thesis record and invalidation point."
- "If two rule violations occur in one week, switch to review-only mode."
- "A missed entry may be added to the watchlist, but not chased above the planned trigger."

## Evidence Standard

Every warning or tag should cite evidence:

- field value (`actual.risk_r = 1.8` vs `max_risk_per_trade_r = 1.0`)
- journal phrase
- missing required record
- explicit flag (`stop_moved = true`)

Avoid unsupported claims. If evidence is unclear, say so.

### Referencia: references/risk-review-checklist.md

# Risk Review Checklist

## Purpose

This checklist gives the skill a risk-manager style review framework. It compares
actual actions with the user's own documented rules. It does not create financial
advice or decide whether a trade should be taken.

## Checks

| Check | Required Evidence | Warning | Critical |
|---|---|---|---|
| Per-trade risk | planned max R and actual R | actual > planned by <=25% | actual > planned by >25% |
| Portfolio heat | max heat and actual heat | actual near max | actual > max |
| Weekly loss limit | max weekly loss and current weekly loss | within 10% of limit | breached limit |
| Consecutive losses | count and threshold | near threshold | at/above threshold |
| Regime gate | market regime and allowed trade types | unclear gate | trade taken against restrictive/cash-priority gate |
| Stop discipline | planned stop and actual stop changes | unclear stop change | unplanned stop move |
| Adds/trims | original add/trim rules | discretionary add/trim unclear | add to loser or add without plan |
| Correlation cluster | holdings and sector/theme exposure | concentrated exposure | new trade increases high-risk cluster |

## Severity Guidance

`info`: observation only. No rule concern.

`warning`: possible issue or incomplete evidence. Human should review.

`critical`: explicit user rule violation or repeated pattern. Should produce
`RULE_VIOLATION` or `COOL_DOWN` depending on recurrence.

## Risk Manager Language

Use objective rule language:

- Good: "Actual risk was 1.8R versus a stated max of 1.0R."
- Bad: "This was a stupid trade."
- Good: "This is a rule-adherence issue, not proof that the setup had no edge."
- Bad: "Never trade this pattern again."

## Incomplete Data

If a risk plan is missing:

- mark risk findings as `unclear`
- ask for the missing risk plan
- avoid claiming a rule violation
- still flag actual risk values if they are present


---

## SKILL: wash-sale-detection

- Fuente: `agiprolabs/claude-trading-skills` → `skills/wash-sale-detection` (MIT)
- Cuándo usarla: Wash sale detection under 2025 US crypto rules with 61-day window monitoring, disallowed loss tracking, and safe re-entry countdown
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/wash-sale-detection/` (wash_sale_scanner.py)

# Wash Sale Detection

Detect wash sales under current US crypto tax rules (effective 2025), monitor the 61-day window around realized losses, track disallowed losses with basis adjustments, and compute safe re-entry countdowns.

> **Disclaimer**: This skill provides informational analysis only. It is NOT tax advice. Consult a qualified tax professional or CPA for guidance on your specific situation. Tax law is complex, and the application of wash sale rules to cryptocurrency may vary based on individual circumstances, IRS guidance updates, and court rulings.

## Background

Before 2025, cryptocurrency was not subject to the wash sale rule because digital assets were classified as property rather than securities. The **Infrastructure Investment and Jobs Act** and subsequent IRS rulemaking extended wash sale treatment to digital assets beginning January 1, 2025.

Under **IRC Section 1091** (as amended for digital assets), if you sell or dispose of a cryptocurrency at a loss and acquire a **substantially identical** asset within a **61-day window** (30 days before the sale through 30 days after), the loss is **disallowed** for tax purposes. The disallowed loss is added to the cost basis of the replacement position.

## Key Concepts

### The 61-Day Window

```
Day -30 ................. Day 0 ................. Day +30
  |--- 30 days before ---|--- sale day ---|--- 30 days after ---|
  ^                       ^                                      ^
  Window opens        Loss realized                    Window closes
```

- **Day 0**: The day you sell a position at a realized loss
- **Days -30 to -1**: Purchases in this range trigger a wash sale retroactively
- **Days +1 to +30**: Purchases in this range trigger a wash sale prospectively
- The window is **calendar days**, not trading days

### Substantially Identical Assets

For crypto, "substantially identical" generally means the **same token**. Selling SOL at a loss and buying SOL within 30 days is a wash sale. Selling SOL and buying ETH is not (they are different assets).

Edge cases that may be scrutinized:
- Wrapped vs unwrapped versions of the same token (e.g., SOL vs wSOL)
- Tokens across different chains (e.g., USDC on Solana vs USDC on Ethereum)
- Derivative tokens that track the same underlying (e.g., stSOL and SOL)

### Disallowed Loss and Basis Adjustment

When a wash sale occurs:
1. The realized loss is **disallowed** — you cannot deduct it in the current tax year
2. The disallowed loss is **added to the cost basis** of the replacement position
3. The holding period of the original position may carry over to the replacement

**Example**:
- Buy 10 SOL at $100 each (cost basis: $1,000)
- Sell 10 SOL at $80 each (proceeds: $800, loss: $200)
- Buy 10 SOL at $85 within 15 days (wash sale triggered)
- New cost basis: $850 + $200 disallowed loss = **$1,050**
- The $200 loss is not gone — it is deferred into the new position

## Prerequisites

- Python 3.10+
- No external dependencies required (standard library only)
- Trade history data in CSV or structured format with: date, action (buy/sell), token, quantity, price, proceeds, cost basis

## Capabilities

1. **Wash Sale Scanning** — Analyze a trade history and flag all wash sale violations
2. **61-Day Window Monitoring** — Track open windows for recent loss-generating sales
3. **Disallowed Loss Calculation** — Compute the exact disallowed amount per wash sale
4. **Basis Adjustment Tracking** — Show adjusted cost basis for replacement positions
5. **Safe Re-Entry Countdown** — For each token sold at a loss, show days remaining until safe to re-enter
6. **Automation Hazard Detection** — Flag copy-trade systems or bot strategies that may inadvertently trigger wash sales

## Quick Start

```python
from datetime import date

# Define your trade history
trades = [
    {"date": date(2025, 3, 1), "action": "buy",  "token": "SOL", "qty": 10, "price": 100.0},
    {"date": date(2025, 3, 15), "action": "sell", "token": "SOL", "qty": 10, "price": 80.0},
    {"date": date(2025, 3, 25), "action": "buy",  "token": "SOL", "qty": 10, "price": 85.0},
]

# Check for wash sales
from scripts.wash_sale_scanner import WashSaleScanner

scanner = WashSaleScanner(trades)
results = scanner.scan()

for ws in results.wash_sales:
    print(f"WASH SALE: {ws.token} — Loss ${ws.disallowed_loss:.2f} disallowed")
    print(f"  Sale: {ws.sale_date} | Re-entry: {ws.replacement_date}")
    print(f"  Adjusted basis: ${ws.adjusted_basis:.2f}")

# Check safe re-entry countdowns
for countdown in results.countdowns:
    print(f"{countdown.token}: {countdown.days_remaining} days until safe re-entry")
```

## Use Cases

### 1. End-of-Year Tax Review

Scan your full year of trading activity to identify all wash sales before filing taxes. Generate a report showing total disallowed losses and adjusted cost bases.

### 2. Real-Time Monitoring

Before placing a buy order, check whether the token has an open wash sale window from a recent loss. Avoid inadvertent wash sales by waiting for the countdown to expire.

### 3. Copy-Trade and Bot Audit

Automated trading systems (copy-trading bots, DCA bots, grid bots) frequently trigger wash sales because they buy and sell the same tokens repeatedly. Run this scanner on bot trade exports to quantify the tax impact.

### 4. Tax-Loss Harvesting Coordination

When executing a tax-loss harvesting strategy, use the safe re-entry countdown to plan when you can re-enter positions. Swap into a non-identical asset during the 30-day window if you want to maintain market exposure.

### 5. Multi-Account Wash Sale Detection

The wash sale rule applies across all accounts controlled by the same taxpayer. If you trade SOL on multiple exchanges or wallets, aggregate the trade history before scanning.

## Edge Cases and Automation Hazards

### DCA Bots and Grid Bots

Dollar-cost averaging bots that buy a token weekly will almost certainly trigger wash sales if the token is also sold at a loss during the same period. The scanner flags overlapping buy/sell patterns within the 61-day window.

### Copy-Trading

If a copy-trade system sells a token at a loss and the leader re-enters within 30 days, your copied trades inherit the wash sale. There is no "I didn't place the trade" exception.

### Partial Fills and Multiple Lots

When a sale at a loss is followed by multiple smaller purchases, the wash sale applies to each purchase up to the quantity of the loss-generating sale. The scanner handles partial matching.

### Cross-Wallet Transfers

Transferring tokens to another wallet you control and selling there does not avoid the wash sale rule. The rule follows the taxpayer, not the account.

## Safe Re-Entry Strategy

After selling a token at a loss:

1. **Wait 31 calendar days** before repurchasing the same token
2. During the waiting period, consider holding a **non-identical substitute** (e.g., sell SOL, hold ETH for exposure to crypto broadly)
3. Use the countdown timer to know exactly when re-entry is safe
4. Set calendar reminders for window expiration dates

```
Token: SOL
Sale Date: 2025-03-15
Loss: $200.00
Window Closes: 2025-04-14
Days Remaining: 12
Status: DO NOT BUY — wash sale window active
```

## Basis Adjustment Walkthrough

Detailed step-by-step basis adjustment example:

```
TRADE 1: Buy 100 SOL @ $150.00    → Basis: $15,000.00
TRADE 2: Sell 100 SOL @ $120.00   → Proceeds: $12,000.00, Loss: $3,000.00
TRADE 3: Buy 100 SOL @ $125.00    → Basis before adjustment: $12,500.00
         (within 30 days of Trade 2)

WASH SALE TRIGGERED:
  Disallowed loss:    $3,000.00
  Adjusted basis:     $12,500.00 + $3,000.00 = $15,500.00
  Effective price:    $155.00 per SOL (not $125.00)

Later sale at $160.00:
  Proceeds:    $16,000.00
  Adj. basis:  $15,500.00
  Gain:        $500.00 (not $3,500.00)
  The $3,000 loss is recovered through the higher basis.
```

## Files

### References
- `references/planned_features.md` — Wash sale rules in depth, 61-day window mechanics, basis adjustment examples, automation edge cases, IRS guidance references

### Scripts
- `scripts/wash_sale_scanner.py` — Complete wash sale scanner: loads trade history, identifies wash sales, computes disallowed losses and basis adjustments, shows safe re-entry countdowns. Run with `--demo` for example scenarios.

## Limitations

- This tool implements a simplified interpretation of wash sale rules as applied to crypto
- "Substantially identical" determination for wrapped tokens and derivatives may require professional judgment
- The scanner does not handle options, futures, or other derivative instruments on crypto
- Multi-account detection requires you to aggregate trade data manually
- Rules may change as IRS issues further guidance on digital asset wash sales
- State tax rules may differ from federal treatment

### Referencia: references/planned_features.md

# Wash Sale Detection — Rules, Mechanics, and Planned Features

## IRS Wash Sale Rule — IRC Section 1091

### Statutory Foundation

The wash sale rule was originally enacted in 1921 to prevent taxpayers from claiming artificial tax losses by selling securities at a loss and immediately repurchasing them. The rule was codified as **Internal Revenue Code Section 1091**.

Prior to 2025, cryptocurrency was classified as "property" (IRS Notice 2014-21) and was explicitly **excluded** from wash sale treatment. The **Infrastructure Investment and Jobs Act** (signed November 2021) and subsequent IRS rulemaking extended the definition of covered assets to include "specified digital assets" effective **January 1, 2025**.

### What Triggers a Wash Sale

A wash sale occurs when ALL of the following conditions are met:

1. A taxpayer disposes of a digital asset at a **realized loss**
2. Within the **61-day window** (30 days before through 30 days after the sale), the taxpayer acquires a **substantially identical** digital asset
3. The acquisition is by **purchase**, receipt as compensation, or through a contract or option

### What Does NOT Trigger a Wash Sale

- Selling at a **gain** — wash sale rules only apply to losses
- Buying a **different** token after selling at a loss (SOL loss, then buying ETH)
- Repurchasing the same token **after 30 calendar days** have elapsed
- Gifting the asset (though gift tax rules may apply separately)

## 61-Day Window Mechanics

### Calendar Day Counting

The 61-day window uses **calendar days**, not trading days or business days.

```
Example: Sale on March 15, 2025

Pre-sale window:  Feb 13, 2025 — Mar 14, 2025  (30 calendar days)
Sale day:         Mar 15, 2025                  (Day 0)
Post-sale window: Mar 16, 2025 — Apr 14, 2025   (30 calendar days)

Total window:     Feb 13, 2025 — Apr 14, 2025   (61 calendar days)
```

### Retroactive Triggering

A wash sale can be triggered **retroactively**. If you buy a token on March 1 and then sell the same token at a loss on March 20, the March 1 purchase falls within the 30-day pre-sale window. The loss is disallowed.

### Multiple Sales and Purchases

When multiple purchases fall within the wash sale window of a single loss-generating sale, the wash sale rule applies to purchases in **chronological order** up to the quantity of the loss sale.

```
Mar 1:  Buy 50 SOL @ $100
Mar 15: Sell 100 SOL @ $80 (loss of $2,000)
Mar 20: Buy 30 SOL @ $85
Mar 25: Buy 40 SOL @ $82
Apr 1:  Buy 50 SOL @ $90

Wash sales:
  Mar 20 purchase: 30 SOL matched → $600 disallowed
  Mar 25 purchase: 40 SOL matched → $800 disallowed
  Total matched: 70 of 100 SOL → $1,400 of $2,000 disallowed
  Remaining deductible loss: $600 (for the unmatched 30 SOL)
  Apr 1 purchase: outside window (Day 17 is within window — recalculate)
```

Important: count days carefully. April 1 is Day 17 after March 15, still within the 30-day window. All 100 SOL would be matched in this example.

### Partial Quantity Matching

If you sell 100 tokens at a loss but only repurchase 60 within the window:
- 60 tokens' worth of loss is disallowed (proportional)
- 40 tokens' worth of loss is deductible
- The disallowed amount is added to the basis of the 60 replacement tokens

## Basis Adjustment Examples

### Simple Case

```
Jan 10: Buy 10 SOL @ $200  (basis: $2,000)
Feb 5:  Sell 10 SOL @ $150 (proceeds: $1,500, loss: $500)
Feb 20: Buy 10 SOL @ $160  (basis before adj: $1,600)

Wash sale: $500 loss disallowed
Adjusted basis: $1,600 + $500 = $2,100
Per-unit adjusted basis: $210 (not $160)
```

### Partial Match Case

```
Jan 10: Buy 100 SOL @ $200  (basis: $20,000)
Feb 5:  Sell 100 SOL @ $150 (proceeds: $15,000, loss: $5,000)
Feb 20: Buy 40 SOL @ $160   (basis before adj: $6,400)

Wash sale on 40 of 100 SOL:
  Disallowed loss: $5,000 * (40/100) = $2,000
  Deductible loss: $5,000 - $2,000 = $3,000
  Adjusted basis of 40 new SOL: $6,400 + $2,000 = $8,400
  Per-unit adjusted basis: $210 per SOL
```

### Chained Wash Sales

A wash sale can chain: if the replacement position is also sold at a loss and repurchased within 30 days, the accumulated disallowed losses carry forward.

```
Jan 10: Buy 10 SOL @ $200  (basis: $2,000)
Feb 1:  Sell 10 SOL @ $150 (loss: $500 → disallowed)
Feb 15: Buy 10 SOL @ $155  (adj basis: $1,550 + $500 = $2,050)
Mar 1:  Sell 10 SOL @ $140 (loss: $2,050 - $1,400 = $650 → disallowed)
Mar 15: Buy 10 SOL @ $145  (adj basis: $1,450 + $650 = $2,100)

After two chained wash sales, the new position carries $1,150
of accumulated disallowed losses in its adjusted basis.
```

## Automation Edge Cases

### DCA Bot Hazard

A DCA bot buying SOL every week creates a near-guaranteed wash sale scenario if SOL is ever sold at a loss:

```
Weekly DCA: Buy 1 SOL every Monday
Mar 3:  Buy 1 SOL @ $180
Mar 10: Buy 1 SOL @ $170
Mar 17: Sell 5 SOL @ $160 (loss)
Mar 24: Buy 1 SOL @ $155  ← Wash sale (Day +7)
Mar 31: Buy 1 SOL @ $150  ← Wash sale (Day +14)

The DCA bot must be paused for 31 days after any loss-generating sale
to avoid wash sales on that token.
```

### Copy-Trading Systems

Copy-trade bots replicate a leader's trades. If the leader sells at a loss and re-enters within 30 days, all copiers inherit the wash sale. The copier has no defense — the rule applies regardless of intent or automation.

**Mitigation**: Filter copy-trade signals to suppress re-entry buys for tokens with active wash sale windows.

### Grid Bot Hazard

Grid bots place buy and sell orders at fixed intervals. They frequently sell and rebuy the same token within minutes. Every loss-generating sell followed by a grid buy is a wash sale.

**Mitigation**: Grid bots on tokens expected to be volatile should account for wash sale costs in profitability calculations.

### Multi-Exchange / Multi-Wallet

The wash sale rule applies to the **taxpayer**, not to individual accounts. A sale on Exchange A and a purchase on Exchange B within the window is a wash sale. This includes:
- Multiple CEX accounts
- DEX wallets
- Custodial vs self-custody
- Spouse's accounts (for joint filers)

## IRS Guidance References

| Source | Key Point |
|--------|-----------|
| IRC § 1091 | Statutory wash sale rule |
| IRS Notice 2014-21 | Crypto treated as property |
| Infrastructure Investment and Jobs Act (2021) | Extended reporting and wash sale rules to digital assets |
| IRC § 6045 (amended) | Broker reporting requirements for digital assets |
| IRS Publication 550 | Investment income and expenses, wash sale details |
| Rev. Rul. 2019-24 | Hard forks and airdrops treatment |

### Effective Dates

- **January 1, 2025**: Wash sale rule applies to digital assets
- **January 1, 2025**: Broker reporting (Form 1099-DA) requirements begin phased rollout
- **January 1, 2026**: Full cost basis reporting by brokers mandatory

### Open Questions in IRS Guidance

As of early 2025, the IRS has not issued definitive guidance on several crypto-specific questions:

1. Are wrapped tokens (wSOL) "substantially identical" to the unwrapped token (SOL)?
2. Are cross-chain versions of the same token (USDC on Solana vs Ethereum) substantially identical?
3. Are liquid staking derivatives (stSOL, mSOL, jitoSOL) substantially identical to SOL?
4. How do LP tokens interact with wash sale rules when the LP contains the sold token?
5. Does staking/unstaking constitute a disposition for wash sale purposes?

**Conservative approach**: Treat all of the above as substantially identical until IRS clarifies otherwise.

## Planned Scanner Features

- [ ] CSV and JSON trade history import
- [ ] Multi-token parallel scanning
- [ ] Partial quantity matching with proportional loss allocation
- [ ] Chained wash sale detection across sequential trades
- [ ] Multi-account aggregation from combined exports
- [ ] Integration with exchange API exports (Coinbase, Kraken, Binance)
- [ ] Holding period carryover tracking
- [ ] Tax-loss harvesting coordination with substitute asset suggestions
- [ ] Real-time pre-trade wash sale warning
- [ ] Annual tax summary report generation
