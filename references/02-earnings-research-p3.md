# 02-earnings-research — parte 3

Skills de terceros agrupadas por tema. Cada sección indica fuente, licencia y dónde está su código.



---

## SKILL: market-news-analyst

- Fuente: `tradermonty/claude-trading-skills` → `skills/market-news-analyst` (MIT)
- Cuándo usarla: This skill should be used when analyzing recent market-moving news events and their impact on equity markets and commodities. Use this skill when the user requests analysis of major financial news from the past 10 days, wants to understand market reactions to monetary policy decisions (FOMC, ECB, BOJ), needs assessment of geopolitical events' impact on commodities, or requires comprehensive review of earnings announcements from mega-cap stocks. The skill automatically collects news using WebSearch/WebFetch tools and produces impact-ranked analysis reports. All analysis thinking and output are conducted in English.

# Market News Analyst

## Overview

This skill enables comprehensive analysis of market-moving news events from the past 10 days, focusing on their impact on US equity markets and commodities. The skill automatically collects news from trusted sources using WebSearch and WebFetch tools, evaluates market impact magnitude, analyzes actual market reactions, and produces structured English reports ranked by market impact significance.

## Prerequisites

- **Tools:** WebSearch and WebFetch tools must be available for news collection
- **API Keys:** None required (uses built-in web search capabilities)
- **Knowledge:** Familiarity with financial markets terminology is helpful but not required

## Output

This skill produces **conversational guidance** during the analysis session. When the full workflow is executed, Claude generates a comprehensive Markdown report (see Step 6 for format) that can be saved to the `reports/` directory upon user request. No files are generated automatically; output is presented in the conversation.

## When to Use This Skill

Use this skill when:
- User requests analysis of recent major market news (past 10 days)
- User wants to understand market reactions to specific events (FOMC decisions, earnings, geopolitical)
- User needs comprehensive market news summary with impact assessment
- User asks about correlations between news events and commodity price movements
- User requests analysis of how central bank policy announcements affected markets

Example user requests:
- "Analyze the major market news from the past 10 days"
- "How did the latest FOMC decision impact the market?"
- "What were the most important market-moving events this week?"
- "Analyze recent geopolitical news and commodity price reactions"
- "Review mega-cap tech earnings and their market impact"

## Analysis Workflow

Follow this structured 6-step workflow when analyzing market news:

### Step 1: News Collection via WebSearch/WebFetch

**Objective:** Gather comprehensive news from the past 10 days covering major market-moving events.

**Search Strategy:**

Execute parallel WebSearch queries covering different news categories:

**Monetary Policy:**
- Search: "FOMC meeting past 10 days", "Federal Reserve interest rate", "ECB policy decision", "Bank of Japan"
- Target: Central bank decisions, forward guidance changes, inflation commentary

**Inflation/Economic Data:**
- Search: "CPI inflation report [current month]", "jobs report NFP", "GDP data", "PPI producer prices"
- Target: Major economic data releases and surprises

**Mega-Cap Earnings:**
- Search: "Apple earnings [current quarter]", "Microsoft earnings", "NVIDIA earnings", "Amazon earnings", "Tesla earnings", "Meta earnings", "Google earnings"
- Target: Results, guidance, market reactions for largest companies

**Geopolitical Events:**
- Search: "Middle East conflict oil prices", "Ukraine war", "US China tensions", "trade war tariffs"
- Target: Conflicts, sanctions, trade disputes affecting markets

**Commodity Markets:**
- Search: "oil prices news past week", "gold prices", "OPEC meeting", "natural gas prices", "copper prices"
- Target: Supply disruptions, demand shifts, price movements

**Corporate News:**
- Search: "major M&A announcement", "bank earnings", "tech sector news", "bankruptcy", "credit rating downgrade"
- Target: Large corporate events beyond mega-caps

**Recommended News Sources (Priority Order):**
1. Official sources: FederalReserve.gov, SEC.gov (EDGAR), Treasury.gov, BLS.gov
2. Tier 1 financial news: Bloomberg, Reuters, Wall Street Journal, Financial Times
3. Specialized: CNBC (real-time), MarketWatch (summaries), S&P Global Platts (commodities)

**Search Execution:**
- Use WebSearch for broad topic searches
- Use WebFetch for specific URLs from official sources or major news outlets
- Collect publication dates to ensure news is within 10-day window
- Capture: Event date, source, headline, key details, market context (pre-market, trading hours, after-hours)

**Filtering Criteria:**
- Focus on Tier 1 market-moving events (see references/market_event_patterns.md)
- Prioritize news with clear market impact (price moves, volume spikes)
- Exclude: Stock-specific small-cap news, minor product updates, routine filings

Think in English throughout collection process. Document each significant news item with:
- Date and time
- Event type (monetary policy, earnings, geopolitical, etc.)
- Source reliability tier
- Initial market reaction (if observable)

### Step 2: Load Knowledge Base References

**Objective:** Access domain expertise to inform impact assessment.

Load relevant reference files based on collected news types:

**Always Load:**
- `references/market_event_patterns.md` - Comprehensive patterns for all major event types
- `references/trusted_news_sources.md` - Source credibility assessment

**Conditionally Load (Based on News Collected):**

If **monetary policy news** found:
- Focus on: market_event_patterns.md → Central Bank Monetary Policy Events section
- Key frameworks: Interest rate hike/cut reactions, QE/QT impacts, hawkish/dovish tone

If **geopolitical events** found:
- Load: `references/geopolitical_commodity_correlations.md`
- Focus on: Energy Commodities, Precious Metals, regional frameworks matching event

If **mega-cap earnings** found:
- Load: `references/corporate_news_impact.md`
- Focus on: Specific company sections, sector contagion patterns

If **commodity news** found:
- Load: `references/geopolitical_commodity_correlations.md`
- Focus on: Specific commodity sections (Oil, Gold, Copper, etc.)

**Knowledge Integration:**
Compare collected news against historical patterns to:
- Predict expected market reactions
- Identify anomalies (market reacted differently than historical pattern)
- Assess whether reaction was typical magnitude or outsized
- Determine if contagion occurred as expected

### Step 3: Impact Magnitude Assessment

**Objective:** Rank each news event by market impact significance.

**Impact Assessment Framework:**

For each news item, evaluate across three dimensions:

**1. Asset Price Impact (Primary Factor):**

Measure actual or estimated price movements:

**Equity Markets:**
- Index-level: S&P 500, Nasdaq 100, Dow Jones
  - Severe: ±2%+ in day
  - Major: ±1-2%
  - Moderate: ±0.5-1%
  - Minor: ±0.2-0.5%
  - Negligible: <0.2%

- Sector-level: Specific sector ETFs
  - Severe: ±5%+
  - Major: ±3-5%
  - Moderate: ±1-3%
  - Minor: <1%

- Stock-specific: Individual mega-caps
  - Severe: ±10%+ (and index weight causes index move)
  - Major: ±5-10%
  - Moderate: ±2-5%

**Commodity Markets:**
- Oil (WTI/Brent):
  - Severe: ±5%+
  - Major: ±3-5%
  - Moderate: ±1-3%

- Gold:
  - Severe: ±3%+
  - Major: ±1.5-3%
  - Moderate: ±0.5-1.5%

- Base Metals (Copper, etc.):
  - Severe: ±4%+
  - Major: ±2-4%
  - Moderate: ±1-2%

**Bond Markets:**
- 10-Year Treasury Yield:
  - Severe: ±20bps+ in day
  - Major: ±10-20bps
  - Moderate: ±5-10bps

**Currency Markets:**
- USD Index (DXY):
  - Severe: ±1.5%+
  - Major: ±0.75-1.5%
  - Moderate: ±0.3-0.75%

**2. Breadth of Impact (Multiplier):**

Assess how many markets/sectors affected:

- **Systemic (3x multiplier):** Multiple asset classes, global markets
  - Examples: FOMC surprise, banking crisis, major war outbreak

- **Cross-Asset (2x multiplier):** Equities + commodities, or equities + bonds
  - Examples: Inflation surprise, geopolitical supply shock

- **Sector-Wide (1.5x multiplier):** Entire sector or related sectors
  - Examples: Tech earnings cluster, energy policy announcement

- **Stock-Specific (1x multiplier):** Single company (unless mega-cap with index impact)
  - Examples: Individual company earnings, M&A

**3. Forward-Looking Significance (Modifier):**

Consider future implications:

- **Regime Change (+50%):** Fundamental market structure shift
  - Examples: Fed pivot from hiking to cutting, major geopolitical realignment

- **Trend Confirmation (+25%):** Reinforces existing trajectory
  - Examples: Consecutive strong inflation prints, sustained earnings beats

- **Isolated Event (0%):** One-off with limited forward signal
  - Examples: Single data point within range, company-specific issue

- **Contrary Signal (-25%):** Contradicts prevailing narrative
  - Examples: Good news ignored by market, bad news rallied

**Impact Score Calculation:**

```
Impact Score = (Price Impact Score × Breadth Multiplier) + Forward-Looking Modifier

Price Impact Score:
- Severe: 10 points
- Major: 7 points
- Moderate: 4 points
- Minor: 2 points
- Negligible: 1 point
```

**Example Calculations:**

**FOMC 75bps Rate Hike (hawkish tone):**
- Price Impact: S&P 500 -2.5% (Severe = 10 points)
- Breadth: Systemic (equities, bonds, USD, commodities all moved) = 3x
- Forward: Trend confirmation (ongoing tightening) = +25%
- **Score: (10 × 3) × 1.25 = 37.5**

**NVIDIA Earnings Beat:**
- Price Impact: NVDA +15%, Nasdaq +1.5% (Severe = 10 points)
- Breadth: Sector-wide (semis, tech broadly) = 1.5x
- Forward: Trend confirmation (AI demand) = +25%
- **Score: (10 × 1.5) × 1.25 = 18.75**

**Geopolitical Flare-up (Middle East):**
- Price Impact: Oil +8%, S&P -1.2% (Severe = 10 points)
- Breadth: Cross-asset (oil, equities, gold) = 2x
- Forward: Isolated event (no escalation) = 0%
- **Score: (10 × 2) × 1.0 = 20**

**Single Stock Earnings (Non-Mega-Cap):**
- Price Impact: Stock +12%, no index impact (Major = 7 points)
- Breadth: Stock-specific = 1x
- Forward: Isolated = 0%
- **Score: (7 × 1) × 1.0 = 7**

**Ranking:**
After scoring all news items, rank from highest to lowest impact score. This determines report ordering.

### Step 4: Market Reaction Analysis

**Objective:** Analyze how markets actually responded to each event.

For each significant news item (Impact Score >5), conduct detailed reaction analysis:

**Immediate Reaction (Intraday):**
- Direction: Positive, negative, mixed
- Magnitude: Align with price impact categories
- Timing: Pre-market, during trading, after-hours
- Volatility: VIX movement, bid-ask spreads

**Multi-Asset Response:**

**Equities:**
- Index performance (S&P 500, Nasdaq, Dow, Russell 2000)
- Sector rotation (which sectors outperformed/underperformed)
- Individual stock moves (mega-caps, relevant companies)
- Growth vs Value, Large vs Small Cap divergences

**Fixed Income:**
- Treasury yields (2Y, 10Y, 30Y)
- Yield curve shape (steepening, flattening, inversion)
- Credit spreads (IG, HY)
- TIPS breakevens (inflation expectations)

**Commodities:**
- Energy: Oil (WTI, Brent), Natural Gas
- Precious Metals: Gold, Silver
- Base Metals: Copper, Aluminum (if relevant)
- Agricultural: Wheat, Corn, Soybeans (if relevant)

**Currencies:**
- USD Index (DXY)
- EUR/USD, USD/JPY, GBP/USD
- Emerging market currencies
- Safe havens (JPY, CHF)

**Derivatives:**
- VIX (volatility index)
- Options activity (put/call ratio, unusual volume)
- Futures positioning

**Pattern Comparison:**

Compare observed reaction against expected pattern from knowledge base:

- **Consistent:** Reaction matched historical pattern
  - Example: Fed hike → Tech stocks down, USD up (as expected)

- **Amplified:** Reaction exceeded typical pattern
  - Example: Inflation print +0.3% above consensus → Selloff 2x typical
  - Investigate: Positioning, sentiment, cumulative factors

- **Dampened:** Reaction less than historical pattern
  - Example: Geopolitical event → Oil barely moved
  - Investigate: Already priced in, other offsetting factors

- **Inverse:** Reaction opposite of historical pattern
  - Example: Good news ignored, bad news rallied
  - Investigate: "Good news is bad news" dynamics, Fed pivot hopes

**Anomaly Identification:**

Flag reactions that deviate significantly from patterns:
- Market shrugged off typically market-moving news
- Overreaction to typically minor news
- Contagion failed to spread as expected
- Safe havens didn't work (correlations broke)

**Sentiment Indicators:**

- Risk-On vs Risk-Off: Which regime dominated
- Positioning: Evidence of crowded trades unwinding
- Momentum: Follow-through in subsequent sessions or reversal

### Step 5: Correlation and Causation Assessment

**Objective:** Distinguish direct impacts from coincidental timing.

**Multi-Event Analysis:**

When multiple significant events occurred in the 10-day period, assess interactions:

**Reinforcing Events:**
- Same directional impact
- Example: Hawkish FOMC + hot CPI → Both bearish for equities, amplified move
- Combined impact often non-linear (greater than sum of parts)

**Offsetting Events:**
- Opposite directional impacts
- Example: Strong earnings (positive) + geopolitical tensions (negative) → Muted net reaction
- Identify which factor dominated

**Sequential Events:**
- One event set up reaction to next
- Example: First rate hike modest reaction, second rate hike severe (cumulative tightening concerns)
- Path dependence matters

**Coincidental Timing:**
- Events unrelated but occurred simultaneously
- Difficult to isolate individual impacts
- Note uncertainty in attribution

**Geopolitical-Commodity Correlations:**

For geopolitical events, specifically analyze commodity market reactions using geopolitical_commodity_correlations.md:

**Energy:**
- Map conflict/sanction to supply disruption risk
- Assess actual vs feared supply impact
- Duration: Temporary spike vs sustained elevation

**Precious Metals:**
- Safe-haven flows vs real rate drivers
- Gold response to risk-off events
- Central bank buying implications

**Industrial Metals:**
- Demand destruction from economic slowdown fears
- Supply chain disruptions
- China factor in copper, aluminum

**Agriculture:**
- Black Sea grain exports (Russia-Ukraine)
- Weather overlays
- Food security policy responses

**Transmission Mechanisms:**

Trace how news impacts flowed through markets:

**Direct Channel:**
- News → Immediate asset price reaction
- Example: OPEC cuts → Oil prices up immediately

**Indirect Channels:**
- News → Economic impact → Asset prices
- Example: Rate hike → Mortgage rates up → Housing slows → Homebuilder stocks down

**Sentiment Channel:**
- News → Risk appetite shift → Broad asset reallocation
- Example: Banking crisis → Flight to quality → Treasuries rally, stocks sell

**Feedback Loops:**
- Initial reaction creates secondary effects
- Example: Stock selloff → Margin calls → Forced selling → Deeper selloff

### Step 6: Report Generation

**Objective:** Create structured English Markdown report ranked by market impact.

**Report Structure:**

```markdown
# Market News Analysis Report - [Date Range]

## Executive Summary

[3-4 sentences covering:]
- Period analyzed (specific dates)
- Number of significant events identified
- Dominant market theme/regime (risk-on/risk-off, sector rotation)
- Top 1-2 highest-impact events

## Market Impact Rankings

[Table format, sorted by Impact Score descending]

| Rank | Event | Date | Impact Score | Asset Classes Affected | Market Reaction |
|------|-------|------|--------------|------------------------|-----------------|
| 1 | [Event] | [Date] | [Score] | [Equities, Commodities, etc.] | [Brief reaction] |
| 2 | ... | ... | ... | ... | ... |

---

## Detailed Event Analysis

[For each event in rank order, provide comprehensive analysis]

### [Rank]. [Event Name] (Impact Score: [X])

**Event Date:** [Date, Time]
**Event Type:** [Monetary Policy / Earnings / Geopolitical / Economic Data / Corporate]
**News Source:** [Source, with credibility tier]

#### Event Summary
[3-4 sentences describing what happened]
- Key details (e.g., rate decision, earnings beat/miss magnitude, conflict developments)
- Context (was this expected, surprise factor)
- Forward guidance or implications stated

#### Market Reaction

**Immediate (Day-of):**
- **Equities:** S&P 500 [+/-X%], Nasdaq [+/-X%], Sector rotation [details]
- **Bonds:** 10Y yield [change], credit spreads [movement]
- **Commodities:** Oil [+/-X%], Gold [+/-X%], Copper [+/-X%] (if relevant)
- **Currencies:** USD [+/-X%], [other relevant pairs]
- **Volatility:** VIX [level/change]

**Follow-Through (Subsequent Sessions):**
- [Direction: sustained, reversed, or consolidated]
- [Additional price action details if significant]

**Pattern Comparison:**
- **Expected Reaction:** [Based on historical patterns from knowledge base]
- **Actual vs Expected:** [Consistent / Amplified / Dampened / Inverse]
- **Explanation of Deviation:** [If applicable, why reaction differed]

#### Impact Assessment Detail

**Asset Price Impact:** [Severe/Major/Moderate/Minor] - [Justification]
**Breadth:** [Systemic/Cross-Asset/Sector/Stock-Specific] - [Affected markets]
**Forward Significance:** [Regime Change/Trend Confirmation/Isolated/Contrary] - [Rationale]

**Calculated Score:** ([Price Score] × [Breadth Multiplier]) × [Forward Modifier] = [Total]

#### Sector-Specific Impacts

[If relevant, detail which sectors/industries were most affected]
- [Sector 1]: [Impact and reason]
- [Sector 2]: [Impact and reason]
- [Example: Technology -3% (rate sensitivity), Energy +5% (oil price spillover)]

#### Geopolitical-Commodity Correlation Analysis

[Include this section only for geopolitical events]
- [Specific commodity affected]: [Price movement]
- [Supply/demand mechanism]: [Explanation]
- [Historical precedent]: [Comparison to similar past events]
- [Expected duration]: [Temporary shock vs sustained impact]

[Repeat detailed analysis for each ranked event]

---

## Thematic Synthesis

### Dominant Market Narrative
[Identify overarching theme across the 10-day period]
- [E.g., "Persistent inflation concerns dominated despite mixed economic data"]
- [E.g., "Tech sector strength drove markets higher despite geopolitical headwinds"]

### Interconnected Events
[Analyze how events related or compounded]
- [Event A] + [Event B] → [Combined impact analysis]
- [Sequential causation if applicable]

### Market Regime Assessment
**Risk Appetite:** [Risk-On / Risk-Off / Mixed]
**Evidence:**
- [Supporting indicators: sector performance, safe haven flows, credit spreads, VIX]

**Sector Rotation Trends:**
- [Growth vs Value]
- [Cyclicals vs Defensives]
- [Outperformers and underperformers]

### Anomalies and Surprises
[Highlight unexpected market reactions]
1. [Event]: Market reacted [unexpectedly] because [explanation]
2. [Continue for significant anomalies]

---

## Commodity Market Deep Dive

[Dedicated section for commodity movements]

### Energy
- **Crude Oil (WTI/Brent):** [Price level, % change over period, key drivers]
- **Natural Gas:** [If significant movement]
- **Key Events:** [Specific news impacting energy: OPEC, geopolitics, inventory data]

### Precious Metals
- **Gold:** [Price level, % change, safe-haven flows vs real rate dynamics]
- **Silver:** [If significant divergence from gold]
- **Drivers:** [Geopolitical risk premium, inflation hedging, USD strength]

### Base Metals
- **Copper:** [As economic barometer - demand signals]
- **Aluminum, Nickel:** [If relevant supply/demand news]
- **China Factor:** [Impact of Chinese economic data/policy]

### Agricultural (If Relevant)
- **Grains:** [Wheat, Corn, Soybeans - weather, Ukraine conflict impacts]

[For each commodity, reference geopolitical events from main analysis and draw correlations]

---

## Forward-Looking Implications

### Market Positioning Insights
[What the news suggests for current market positioning]
- [Trend continuation or reversal signals]
- [Overvaluation or undervaluation indications]
- [Sentiment extremes (complacency or panic)]

### Upcoming Catalysts
[Events on horizon that may be set up by recent news]
- [Next FOMC meeting expectations post-recent decision]
- [Upcoming earnings seasons based on guidance]
- [Geopolitical developments to monitor]

### Risk Scenarios
[Based on recent news, identify key risks]
1. **[Risk Name]:** [Description, probability, potential impact]
2. **[Risk Name]:** [Description, probability, potential impact]
3. [Continue for 3-5 key risks]

---

## Data Sources and Methodology

### News Sources Consulted
[List primary sources used, organized by tier]
- **Official Sources:** [e.g., FederalReserve.gov, SEC.gov]
- **Tier 1 Financial News:** [e.g., Bloomberg, Reuters, WSJ]
- **Specialized:** [e.g., S&P Global Platts for commodities]

### Analysis Period
- **Start Date:** [Specific date]
- **End Date:** [Specific date]
- **Total Days:** 10

### Market Data
- Equity indices: [Data sources]
- Commodity prices: [Data sources]
- Economic data: [Government sources]

### Knowledge Base References
- `market_event_patterns.md` - Historical reaction patterns
- `geopolitical_commodity_correlations.md` - Geopolitical-commodity frameworks
- `corporate_news_impact.md` - Mega-cap impact analysis
- `trusted_news_sources.md` - Source credibility assessment

---

*Analysis Date: [Date report generated]*
*Language: English*
*Analysis Thinking: English*

```

**File Naming Convention:**
`market_news_analysis_[START_DATE]_to_[END_DATE].md`

Example: `market_news_analysis_2024-10-25_to_2024-11-03.md`

**Report Quality Standards:**
- Objective, fact-based analysis (no speculation beyond probability-weighted scenarios)
- Quantify price movements with specific percentages
- Cite sources for major claims
- Distinguish between correlation and causation
- Acknowledge uncertainty when attributing market moves to specific news
- Use proper financial terminology
- Maintain consistent English throughout

## Key Analysis Principles

When conducting market news analysis:

1. **Impact Over Noise:** Focus on truly market-moving news, filter out minor events
2. **Multi-Asset Perspective:** Analyze across equities, bonds, commodities, currencies to understand full impact
3. **Pattern Recognition:** Compare against historical precedents while noting unique aspects
4. **Causation Discipline:** Be rigorous about attributing market moves to specific news vs coincidental timing
5. **Forward-Looking:** Emphasize implications for future market behavior, not just backward-looking description
6. **Objectivity:** Separate market reaction (what happened) from personal market view (what should happen)
7. **Quantification:** Use specific numbers (%, bps) rather than vague terms ("significant," "large")
8. **Source Credibility:** Weight official sources and Tier 1 news over rumors and unverified reports
9. **Breadth Analysis:** Individual stock moves only significant if mega-cap or systemic signal
10. **English Consistency:** All thinking, analysis, and output in English for consistency

## Common Pitfalls to Avoid

**Over-Attribution:**
- Not every market move is news-driven (technicals, flows, month-end rebalancing exist)
- Acknowledge when attribution is uncertain

**Recency Bias:**
- Latest news isn't always most important
- Rank by actual impact, not chronological order

**Hindsight Bias:**
- Distinguish "obvious in retrospect" from "surprising at the time"
- Note consensus expectations vs actual outcomes

**Single-Factor Analysis:**
- Markets respond to multiple factors simultaneously
- Acknowledge interaction effects

**Ignoring Magnitude:**
- A "hot" CPI that's 0.1% above consensus is different from 0.5% above
- Quantify surprise factor

## Resources

### references/

**market_event_patterns.md** - Comprehensive knowledge base covering:
- Central bank monetary policy events (FOMC, ECB, BOJ, PBOC)
- Inflation data releases (CPI, PPI, PCE)
- Employment data (NFP, unemployment, wages)
- GDP reports
- Geopolitical events (conflicts, trade wars, sanctions)
- Corporate earnings (mega-cap technology, banks, energy)
- Credit events and rating changes
- Commodity-specific events (OPEC, weather, supply disruptions)
- Recession indicators
- Historical case studies (2008 crisis, COVID-19, 2022 inflation)
- Pattern recognition framework and sentiment analysis

**geopolitical_commodity_correlations.md** - Detailed correlations covering:
- Energy commodities (crude oil, natural gas, coal) and geopolitical conflicts
- Precious metals (gold, silver, platinum, palladium) safe-haven dynamics
- Base metals (copper, aluminum, nickel, zinc) and economic/political risks
- Agricultural commodities (wheat, corn, soybeans) and weather/policy
- Rare earth elements and critical minerals (China dominance, supply security)
- Regional geopolitical frameworks (Middle East, Russia-Europe, Asia-Pacific, Latin America)
- Correlation summary tables
- Time horizon considerations

**corporate_news_impact.md** - Mega-cap analysis framework:
- "Magnificent 7" technology stocks (NVIDIA, Apple, Microsoft, Amazon, Meta, Google, Tesla)
- Financial sector mega-caps (JPMorgan, Bank of America, etc.)
- Healthcare mega-caps (UnitedHealth, Pfizer, J&J, Merck)
- Energy mega-caps (Exxon Mobil, Chevron)
- Consumer staples mega-caps (P&G, Coca-Cola, PepsiCo)
- Industrial mega-caps (Boeing, Caterpillar)
- Earnings impact frameworks, product launches, M&A, regulatory issues
- Sector contagion patterns
- Impact magnitude framework

**trusted_news_sources.md** - Source credibility guide:
- Tier 1 primary sources (central banks, government agencies, SEC)
- Tier 2 major financial news (Bloomberg, Reuters, WSJ, FT, CNBC)
- Tier 3 specialized sources (energy, tech, emerging markets, China-specific, crypto)
- Tier 4 analysis and research (independent research, central bank publications, think tanks)
- Search and aggregation tools
- Source quality assessment criteria
- Speed vs accuracy trade-offs
- Recommended search strategies for 10-day analysis
- Source credibility framework
- Red flag sources to avoid

## Important Notes

- All analysis thinking must be conducted in English
- All output Markdown files must be in English
- Use WebSearch and WebFetch tools to collect news automatically
- Focus on trusted news sources as defined in references
- Rank events by impact score (price impact × breadth × forward significance)
- Target analysis period: Past 10 days from current date
- Emphasize US equity markets and commodities as primary analysis subjects
- FOMC and other central bank policy decisions receive highest priority analysis
- Distinguish between correlation and causation rigorously
- Quantify all market reactions with specific percentages
- Load appropriate reference files based on news types collected
- Generate comprehensive reports ranked by market impact (highest impact first)

### Referencia: references/corporate_news_impact.md

# Corporate News Impact Analysis Framework

## Mega-Cap Technology Stocks

### Market Cap Significance

**"Magnificent 7" Era (2023-2024):**
- Apple, Microsoft, NVIDIA, Amazon, Google, Meta, Tesla
- Combined: ~25-30% of S&P 500 market cap
- Index-level impact from individual company moves

**Historical Context:**
- 2000s: Microsoft, Cisco, Intel, Oracle
- 2010s: FAANG (Facebook, Apple, Amazon, Netflix, Google)
- Concentration risk at historic highs

### Earnings Impact Framework

**NVIDIA (Market Leader, AI Infrastructure):**

**Positive Scenarios:**
- Beat + raise guidance: +10-15% stock, Nasdaq +1-2%, semiconductor sector +3-5%
- AI chip demand exceeding expectations: Broad tech rally
- New product launches (Blackwell, etc.): Sector enthusiasm

**Negative Scenarios:**
- Miss earnings: -10-20% stock, Nasdaq -1-2%, AMD/chip stocks -5-8%
- Guidance cut: Severe (questions AI demand sustainability)
- Supply constraints mentioned: Concerns about cycle peak

**Broader Market Implications:**
- NVIDIA results as AI investment proxy
- Cloud/data center spending indicator
- Risk appetite barometer

**Example:**
- May 2024 earnings: Beat + strong guide → Stock +9%, pulled Nasdaq up significantly

**Apple (Largest Market Cap, Consumer Bellwether):**

**Positive Scenarios:**
- iPhone sales beat: +5-8% stock, Consumer Discretionary rally
- Services growth acceleration: Margin expansion narrative
- China demand resilience: EM concerns alleviated

**Negative Scenarios:**
- iPhone unit decline: -5-10% stock, supply chain (AAPL suppliers) -8-15%
- China weakness: Broader EM demand concerns
- Services slowdown: Margin pressure fears

**Broader Market Implications:**
- Consumer health indicator
- China economy proxy
- Index weight means S&P 500 moves with AAPL

**Microsoft (Cloud, AI, Software):**

**Positive Scenarios:**
- Azure growth acceleration: +6-10% stock, cloud sector rally
- AI monetization evidence: Broad tech enthusiasm
- Margin expansion: Quality growth narrative

**Negative Scenarios:**
- Azure deceleration: -7-12% stock, GOOGL/AMZN cloud concerns
- AI investment costs without revenue: Profitability concerns
- Enterprise spending weakness: B2B recession fears

**Broader Market Implications:**
- Enterprise IT spending health
- Cloud growth trajectory
- AI investment ROI evidence

**Amazon (E-commerce, Cloud, Logistics):**

**Positive Scenarios:**
- AWS reacceleration: +8-12% stock, validates cloud growth
- E-commerce margin expansion: Efficiency narrative
- Advertising growth: High-margin revenue stream

**Negative Scenarios:**
- AWS slowdown: -8-15% stock, enterprise spending concerns
- E-commerce margin compression: Consumer weakness + competition
- Capex surge without ROIC: Capital allocation concerns

**Broader Market Implications:**
- Consumer discretionary spending
- Cloud infrastructure demand
- Logistics/fulfillment efficiency trends

**Meta (Digital Advertising, AI, Metaverse):**

**Positive Scenarios:**
- Ad revenue beat: +10-15% stock, digital ad market health (GOOGL, SNAP benefit)
- User growth/engagement: Platform strength
- AI-driven ad targeting: Margin expansion

**Negative Scenarios:**
- Ad revenue miss: -12-20% stock, digital ad recession fears (GOOGL, SNAP sell-off)
- Reality Labs losses exceeding: Metaverse skepticism
- Regulatory headwinds: Antitrust, privacy concerns

**Broader Market Implications:**
- Digital advertising market health
- Consumer engagement trends
- Big Tech regulation trajectory

**Tesla (EVs, Energy, AI/Autonomy):**

**Positive Scenarios:**
- Delivery beat: +8-15% stock, EV demand strength (rivian, lucid benefit)
- Margin expansion: Pricing power narrative
- FSD/autonomy progress: Massive TAM expansion story

**Negative Scenarios:**
- Delivery miss: -10-20% stock, EV demand concerns (all EV stocks sell)
- Price cuts needed: Margin compression, competition intensifying
- Production issues: Execution concerns

**Broader Market Implications:**
- EV adoption trajectory
- China auto market health
- Autonomy/AI hardware theme

### Product Launch Impact

**iPhone Launch (Annual, September):**
- Pre-orders strong: AAPL +3-5%, suppliers rally
- Weak demand: AAPL -5-8%, supply chain sells
- Ripple effect: Asian tech suppliers (Taiwan, Korea, Japan)

**AI Model Releases (OpenAI, Google, Anthropic):**
- GPT-4, Gemini, Claude releases
- Competitive dynamics: MSFT, GOOGL, META positioning
- Infrastructure demand: NVDA, cloud providers benefit

**New Hardware (VR, AR, Wearables):**
- Meta Quest, Apple Vision Pro
- Adoption rates critical
- Ecosystem development

### M&A Announcements

**Mega-Cap Acquisitions:**

**Positive for Acquirer:**
- Strategic fit clear
- Reasonable valuation
- Synergy potential
- Example: MSFT-LinkedIn (2016): Initially -3%, long-term positive

**Negative for Acquirer:**
- Overpayment perception
- Integration risks
- Regulatory concerns
- Example: MSFT-Activision: Regulatory uncertainty weighed

**Sector Consolidation:**
- Horizontal mergers: Competitive concerns
- Vertical integration: Supply chain control
- Regulatory scrutiny high for mega-caps

### Regulatory/Legal Issues

**Antitrust Actions:**
- DOJ/FTC investigations: Stock -5-10%, sector concerns
- EU fines: Direct financial impact moderate, precedent concerns
- Breakup threats: Severe (20-30% declines possible)

**Examples:**
- Google antitrust (2020-2024): Search monopoly concerns
- Meta FTC lawsuit: Instagram/WhatsApp acquisition challenges
- Apple App Store: Epic Games lawsuit, DMA compliance

**Privacy Regulations:**
- GDPR, CCPA impacts
- App tracking transparency (Apple): META -20%+ (2022)
- Cookie deprecation: Digital ad ecosystem shifts

**Content Moderation:**
- Section 230 debates
- Government pressure (US, EU, China)
- Advertiser boycotts

## Financial Sector Mega-Caps

### JPMorgan Chase (Largest US Bank)

**Earnings Impact:**

**Positive:**
- NIM expansion: +4-6% stock, bank sector +2-3%
- Credit quality stable: No recession fears
- Trading revenue beat: Market volatility benefited

**Negative:**
- NIM compression: -5-8% stock, rate cut expectations increase
- Provision builds: Recession indicator, financials -3-5%
- Investment banking weakness: M&A market dead

**CEO Commentary (Jamie Dimon):**
- Market watches closely for economic outlook
- Regulatory environment commentary
- Geopolitical risk assessment

**Broader Implications:**
- Economic health leading indicator
- Credit cycle positioning
- Net interest income trajectory for all banks

### Bank of America, Wells Fargo, Citigroup

**Similar Dynamics to JPM:**
- NIM sensitivity
- Credit quality
- Regulatory issues (especially WFC)

**Regional Bank Contagion:**
- March 2023: SVB, Signature, First Republic failures
- Mega-cap banks benefited (flight to quality)
- But systemic concerns weighed on all financials initially

## Healthcare Mega-Caps

### UnitedHealth Group, CVS Health

**Policy Sensitivity:**
- Medicare Advantage rate changes
- Drug pricing legislation (IRA impacts)
- Medicaid expansion/contraction

**Operational Metrics:**
- Medical loss ratio (MLR)
- Membership growth
- PBM (Pharmacy Benefit Manager) profitability

**Broader Implications:**
- Healthcare cost trends
- Regulatory environment for sector
- M&A possibilities (vertical integration)

### Pharmaceutical Giants (Pfizer, J&J, Merck)

**Drug Pipeline:**
- Phase 3 trial results: Stock ±10-20%
- FDA approvals: Positive 5-15%
- Patent cliffs: Negative 10-20% (generic competition)

**COVID-19 Era:**
- Vaccine/treatment sales: Massive (Pfizer, Moderna)
- Post-pandemic normalization: Revenue concerns

**M&A Activity:**
- Pipeline acquisition common
- Biotech targets
- Oncology, rare disease focus

## Energy Mega-Caps

### Exxon Mobil, Chevron

**Oil Price Correlation:**
- High beta to crude oil prices
- Production volumes
- Refining margins

**Capital Allocation:**
- Shareholder returns (buybacks, dividends): Positive
- Drilling capex: Mixed (growth vs discipline)
- M&A (Exxon-Pioneer, Chevron-Hess): Scale benefits

**Energy Transition:**
- Renewable investments: Modest impact
- Carbon capture: Future potential
- Natural gas positioning

**Geopolitical Exposure:**
- International operations (Middle East, Africa)
- Sanctions compliance
- OPEC+ policy interactions

## Consumer Staples Mega-Caps

### Procter & Gamble, Coca-Cola, PepsiCo

**Pricing Power:**
- Pass-through inflation: Margin protection
- Volume declines from price increases: Demand concerns
- Private label competition

**Emerging Markets:**
- China exposure (P&G): Economic growth sensitivity
- Currency headwinds/tailwinds

**Operational Efficiency:**
- Cost-cutting programs
- Supply chain optimization

**Defensive Nature:**
- Outperform in recession fears
- Underperform in growth acceleration

## Industrial Mega-Caps

### Boeing (Aerospace, Defense)

**Commercial Aviation:**
- Aircraft deliveries: Supply chain challenges (2020-2024)
- 737 MAX issues: Safety, regulatory, reputational
- Order book: Airline industry health

**Defense:**
- Government contracts
- Geopolitical tensions supportive

**Broader Implications:**
- Air travel demand
- Supply chain health (Spirit AeroSystems, etc.)
- China relations (COMAC competition)

### Caterpillar (Construction, Mining Equipment)

**Economic Indicator:**
- "Canary in coal mine" for industrial economy
- Dealer inventories critical metric
- Order backlog

**End Market Exposure:**
- Construction: Housing, infrastructure
- Mining: Commodity prices
- Energy: Oil/gas capex

**China Sensitivity:**
- Major market for construction equipment
- Trade relations impact

## Sector Contagion Patterns

### Technology Sector

**Supply Chain:**
- AAPL warning → Suppliers (AAPL, Foxconn, TSMC) sell-off
- Semiconductor demand → NVDA, AMD, INTC, ASML correlated

**Cloud Spending:**
- MSFT Azure, AMZN AWS, GOOGL Cloud trends
- Enterprise software (CRM, NOW, ADBE) follow

**Digital Advertising:**
- META, GOOGL ad revenue
- SNAP, PINS, TTD correlate

### Financial Sector

**Credit Quality:**
- One bank's provision build → Sector concern
- Regional bank stress → Flight to quality (mega-caps benefit)

**Net Interest Margin:**
- Rate environment impacts all banks similarly
- Yield curve shape critical

### Energy Sector

**Oil Price Pass-Through:**
- Integrated (XOM, CVX) benefit from upstream
- Refiners (MPC, VLO) benefit from downstream
- Service providers (SLB, HAL) lag upstream capex

### Healthcare Sector

**Regulatory:**
- Drug pricing legislation → All pharma/biotech
- Medicare policy → Insurers, providers

**Clinical Trials:**
- Platform technologies (mRNA, gene therapy)
- Failure cascades to similar approaches

## Impact Magnitude Framework

### Stock-Specific Impact

**Minor (±2-5%):**
- In-line earnings
- Expected product updates
- Management changes (non-CEO)

**Moderate (±5-10%):**
- Earnings beat/miss
- Guidance adjustments
- M&A rumors

**Major (±10-20%):**
- Significant earnings surprise
- Large M&A announcements
- Regulatory actions
- Product failures/major launches

**Severe (±20%+):**
- Accounting scandals
- Bankruptcy risk
- Existential regulatory threats
- Major competitive disruption

### Sector Impact

**Minor (±0.5-1%):**
- Single company issues (unless mega-cap)
- Narrow product developments

**Moderate (±1-3%):**
- Mega-cap earnings
- Regulatory proposals
- Commodity price moves

**Major (±3-5%+):**
- Systemic issues (banking crisis)
- Major policy shifts
- Supply shocks

### Index Impact

**S&P 500 Impact Estimation:**
- Top 10 stocks: ~35% of index
- 1% move in mega-cap ≈ 0.03-0.05% index move
- Concurrent mega-cap moves: Amplified

**Nasdaq Impact:**
- Tech concentration even higher (~50% in top 10)
- AAPL, MSFT, NVDA, AMZN, META, GOOGL dominate
- Single stock can move index 0.1-0.2%

## News Analysis Checklist

When analyzing corporate news, assess:

1. **Company Size/Index Weight** - Mega-cap vs small-cap impact
2. **Surprise Factor** - Beat/miss magnitude vs expectations
3. **Guidance** - Forward-looking more important than backward
4. **Sector Positioning** - Leader or follower
5. **Contagion Risk** - Isolated or systemic
6. **Timing** - Earnings season cluster vs standalone
7. **Macro Implications** - Economy-wide signal or company-specific
8. **Competitive Dynamics** - Zero-sum or rising tide
9. **Regulatory Overlay** - Policy risks amplifying
10. **Sentiment Context** - Bull market vs bear market reaction asymmetry

### Referencia: references/geopolitical_commodity_correlations.md

# Geopolitical Events and Commodity Correlations

## Energy Commodities

### Crude Oil (WTI / Brent)

**Middle East Conflicts:**

**Supply Disruption Risk:**
- Strait of Hormuz tensions: ~20% of global oil supply passes through
  - Iran tensions: Oil +5-15% immediately
  - Historical: 2019 Saudi Aramco attacks: Oil +15% in single day
- Saudi Arabia/UAE production: ~15% of global supply
  - Instability: Oil rallies sharply
- Iraq/Libya disruptions: Regional conflicts impact production
  - Libya civil war: Removed 1M+ barrels/day periodically

**Israel-Palestine Conflicts:**
- Direct impact minimal (neither major producer)
- Indirect via regional escalation concerns
- Safe-haven bid for oil typically +2-5%

**Iranian Tensions:**
- Nuclear program concerns
- Sanctions/sanctions relief
  - Sanctions: Removes ~1-2M barrels/day, oil +10-20%
  - Sanctions relief: Adds supply, oil -10-15%
- Proxy conflicts (Yemen, Syria, Lebanon)

**Russia-Ukraine Conflict:**

**Natural Gas:**
- European dependence on Russian gas (~40% pre-conflict)
- Nord Stream disruptions: Natural gas prices +300-400% (2022)
- Coal as alternative: Thermal coal rallied strongly
- LNG exports from US/Qatar beneficiaries

**Crude Oil:**
- Russia ~10% of global supply
- Sanctions impact: Removed ~1M barrels/day from market
- Oil price: +40% in initial months (2022)
- Urals discount to Brent widened to $30-40/barrel

**Petroleum Products:**
- Diesel shortages in Europe (Russia major supplier)
- Gasoline prices globally impacted

**US-China Tensions:**

**Energy Demand Implications:**
- Trade war: Chinese growth slowdown concerns, oil -5-10%
- Taiwan tensions: Regional instability premium, oil +3-7%
- Technology restrictions: Minimal direct impact on oil

**US-Iran Relations:**
- Sanctions enforcement cycles
- Oil supply ~1-2M barrels/day swing factor
- Price impact: ±10-15% depending on direction

**Venezuela Political Crisis:**
- Production collapsed from ~3M to ~0.7M barrels/day
- Sanctions impact
- Regime change prospects: Oil price sensitive to potential supply return

### Natural Gas

**European Energy Crisis (Russia-Ukraine):**
- As detailed above, massive impact
- Coal-to-gas switching reversed
- Renewables acceleration

**US Production Growth:**
- Shale revolution reduced geopolitical sensitivity
- LNG export capacity growth
- Winter weather events still create volatility

**Asian LNG Markets:**
- Japan/South Korea/China major importers
- Competition for LNG cargoes during crises
- Price spikes in supply disruptions

### Coal

**Russia-Ukraine Conflict:**
- Russian coal sanctions
- European utilities switching gas-to-coal
- Thermal coal prices +200% (2022)

**China-Australia Trade Tensions:**
- Informal coal import ban (2020-2021)
- China shifted to Indonesian/Russian coal
- Australian coal exporters found alternative buyers
- Metallurgical coal (steel-making) less impacted

**Climate Policy:**
- Long-term decline narrative
- Short-term supply tightness from underinvestment

## Precious Metals

### Gold

**Geopolitical Risk Premium:**

**General Pattern:**
- Conflicts/crises: Gold +2-10% immediate rally
- Safe-haven flows dominate
- Negative real rates amplify gains

**Specific Events:**

**Russia-Ukraine Conflict:**
- Gold rallied from $1,800 to $2,070 (March 2022)
- Central bank buying increased (dedollarization theme)
- Physical demand surge

**Middle East Escalations:**
- Historical: Iraq War (2003): Gold +7%
- Syria conflicts: Moderate impact (+2-4%)
- Recent Israel-Gaza: Gold +5-8%

**US-China Tensions:**
- Gradual safe-haven bid
- Central bank reserve diversification (China buying gold)
- Currency war implications

**Banking Crises:**
- 2008: Gold rallied during acute stress
- 2023 regional bank failures: Gold +10% in weeks
- Trust in fiat currency undermined

**Currency Debasement Concerns:**
- Massive fiscal deficits
- QE programs
- Inflation hedging demand

**Interest Rate Interaction:**
- Geopolitical premium can override rate headwinds
- Real rates still primary driver long-term
- Risk-off overrides opportunity cost considerations short-term

### Silver

**Industrial Demand Component:**
- 50% industrial use (solar, electronics, EVs)
- Economic slowdown from geopolitics: Negative
- Green energy push: Positive

**Gold Correlation:**
- Trades with gold during risk-off (0.7-0.8 correlation)
- Amplified moves (higher beta to gold)

**Russia-Ukraine Example:**
- Industrial recession fears limited silver gains vs gold
- Gold/Silver ratio widened (gold outperformed)

### Platinum/Palladium

**Russian Supply Dominance:**
- Russia ~40% of palladium supply
- ~10% of platinum supply
- Sanctions concerns: Prices spiked 2022

**Automotive Demand:**
- Catalytic converters
- EV transition threat long-term
- Recession fears negative

**South African Supply Risks:**
- Political instability
- Power shortages (load-shedding)
- Mining strikes frequent

## Base Metals

### Copper

**"Dr. Copper" - Economic Barometer:**

**China Demand (50% of global):**
- China-US trade war: Copper -20% (2018-2019)
- China stimulus: Copper rallies sharply
- Property sector troubles: Negative (major copper consumer)
- Infrastructure spending: Positive

**Chilean Supply (25% of global):**
- Political instability (2019 protests): Copper +5%
- Mining strikes: Immediate price spikes
- Environmental restrictions: Long-term supply concerns
- Water scarcity issues

**Peruvian Supply (10% of global):**
- Political instability frequent
- Community protests at mines
- Supply disruptions: Price supportive

**Zambia/DRC (African Copper Belt):**
- Political risk elevated
- Infrastructure challenges
- Chinese investment dominance

**Energy Transition Demand:**
- EVs use 4x copper vs ICE vehicles
- Grid infrastructure buildout
- Long-term bullish narrative

**Geopolitical Implications:**
- US-China tech war: Copper demand impact (semiconductors, data centers)
- Green energy policies: Demand support
- Recession fears: Demand destruction

### Aluminum

**China Production Dominance (60%):**
- Energy-intensive production
- Power shortages: Production curtailments, price spikes
- Environmental regulations: Supply constraints

**Russia Supply (~6%):**
- Sanctions concerns (Ukraine war)
- Aluminum rallied 2022
- European smelters curtailed (high energy costs)

**Guinea Bauxite (Major Supplier):**
- Political instability (2021 coup)
- Supply concerns for aluminum feedstock

**Applications:**
- Aerospace (geopolitical tensions affect demand)
- Automotive (EVs increasing content)
- Construction (economic growth sensitive)

### Nickel

**Indonesia Supply Dominance (Growing):**
- Ore export ban (2020): Reshuffled global supply chains
- Chinese investment in Indonesian processing
- Environmental concerns

**Russia Supply (~10%):**
- Sanctions risk (Ukraine war)
- Nickel short squeeze (LME chaos, March 2022): +250% in days
- Tsingshan vs LME positions

**Philippines Supply:**
- Environmental regulations
- Mining permit uncertainties
- Typhoon disruptions

**EV Battery Demand:**
- Nickel-rich cathodes (NMC, NCA)
- Competition with iron-phosphate (LFP) batteries
- Indonesia-China battery supply chain

### Zinc

**China Production/Consumption (~40%):**
- Galvanizing steel (construction, auto)
- Smelter margins squeeze when energy costs high
- Production cuts when unprofitable

**Peru/Australia Supply:**
- Mining disruptions
- Concentrate availability

**Russia Supply (~5%):**
- Sanctions impact moderate

## Agricultural Commodities

### Wheat

**Russia-Ukraine (30% of Global Exports):**
- Black Sea export disruptions
- Ukraine ports blockaded (2022): Wheat +50%
- Russia export restrictions/export tax adjustments
- Grain deal negotiations critical

**Weather Events:**
- Droughts in major producers (US Plains, Australia, Argentina)
- Floods in harvest seasons
- Climate change increasing volatility

**India Export Bans:**
- Domestic food security priorities
- Heat waves trigger export restrictions
- Sudden policy changes create price spikes

**North Africa/Middle East Importers:**
- Political instability when bread prices spike
- Arab Spring correlation with wheat prices
- Food security national security issue

### Corn

**US Production Dominance (35% of Global):**
- Weather in Midwest (drought/floods)
- USDA crop reports market-moving

**Brazil/Argentina (Major Exporters):**
- Weather patterns (La Niña impacts)
- Currency fluctuations affect export competitiveness
- Infrastructure challenges (Brazil transport)

**China Demand:**
- Livestock feed demand
- Trade deal purchase commitments
- ASF (African Swine Fever) impacts herd sizes

**Ukraine Supply Disruptions:**
- Corn exports halted during war
- Black Sea logistics

**Ethanol Demand:**
- US biofuel mandates
- Energy prices correlation

### Soybeans

**Brazil-China Trade:**
- China imports 60% of global soybeans
- US-China trade war: Brazil beneficiary
- Brazil overtook US as top exporter

**Argentina Processing:**
- Crushing industry
- Export taxes policy changes

**Weather Risks:**
- Brazil (drought in key states)
- Argentina (La Niña flooding/drought cycles)
- US Midwest (flash droughts)

**China Demand Drivers:**
- Livestock feed (pig herd cycles)
- African Swine Fever devastation (2019): Demand collapsed
- Herd rebuilding: Demand recovery

**Geopolitical Leverage:**
- US-China trade tool
- Brazil-China relationship benefits

## Rare Earth Elements / Critical Minerals

### Rare Earths

**China Dominance (60% Production, 90% Processing):**
- Export restrictions as geopolitical tool
- US-China tensions: Supply security concerns
- Price manipulation capability

**Applications:**
- Defense systems (missiles, jets)
- EVs (motors)
- Wind turbines
- Electronics

**Alternative Supply Development:**
- US (Mountain Pass mine)
- Australia (Lynas)
- Processing capacity bottleneck

**Historical Example:**
- 2010 China-Japan dispute: China restricted exports, prices surged

### Lithium

**EV Battery Critical Component:**

**Australia/Chile Supply (~75%):**
- Australia: Spodumene (hard rock)
- Chile: Brine deposits (Atacama)
- Political risks moderate

**China Processing Dominance (~60%):**
- Refining bottleneck
- US/Europe scrambling to build capacity

**Argentina "Lithium Triangle":**
- Chile-Argentina-Bolivia
- Nationalization risks
- Water usage controversies

**Price Volatility:**
- 2022: +400% on EV demand surge
- 2023: -70% on overcapacity concerns
- Geopolitical diversification premium

### Cobalt

**DRC Production (70% of Global):**
- Political instability
- Child labor controversies
- Chinese control of mines

**Battery Chemistry Shift:**
- Reducing cobalt content (ethical concerns, cost)
- Cobalt-free batteries development

**Sanctions/Ethical Sourcing:**
- Supply chain scrutiny
- Price premium for certified ethical cobalt

## Regional Geopolitical Frameworks

### Middle East

**Oil Price Transmission:**
- Conflicts → Oil ↑ → Inflation ↑ → Rate hikes → Equities ↓
- Energy stocks benefit
- Emerging markets pressured (oil importers)

**Safe Haven Flows:**
- Gold, USD, JPY, CHF rally
- Equities decline (especially European, EM)

**Shipping Disruptions:**
- Suez Canal (10% of global trade)
- Strait of Hormuz (oil)
- Red Sea shipping costs

### Russia-Europe Energy

**Natural Gas Dependency:**
- Europe vulnerable
- Russia leverage
- Coal, LNG, nuclear substitutes

**Sanctions Effectiveness:**
- Energy payments carve-outs complicated
- Oil price caps
- Gray market/smuggling

### Asia-Pacific

**Taiwan Strait Tensions:**
- Semiconductor supply chain choke point
- Shipping disruptions (South China Sea)
- Technology stocks highly sensitive
- Safe-haven flows massive if conflict

**South China Sea:**
- Shipping lanes (1/3 of global trade)
- Energy deposits disputes

### Latin America

**Commodity Exporters:**
- Political shifts affect mining/energy policy
- Nationalization risks
- Currency volatility amplifies commodity moves

**Examples:**
- Peru mining conflicts
- Chile constitutional changes (mining tax debates)
- Brazil Amazon policies (agricultural land)
- Argentina capital controls, export taxes

## Correlation Summary Table

| Geopolitical Event Type | Oil | Gold | Copper | Wheat | USD | Equities |
|------------------------|-----|------|--------|-------|-----|----------|
| Middle East War | ↑↑ | ↑↑ | ↓ | ↑ | ↑ | ↓↓ |
| Russia-Ukraine | ↑↑ | ↑↑ | ↓ | ↑↑ | ↑ | ↓↓ |
| US-China Trade War | ↓ | ↑ | ↓↓ | ↔ | ↑ | ↓ |
| Taiwan Conflict | ↑ | ↑↑ | ↓↓ | ↑ | ↑↑ | ↓↓↓ |
| Emerging Market Crisis | ↓ | ↑ | ↓↓ | ↔ | ↑↑ | ↓↓ |
| Banking Crisis | ↓↓ | ↑↑ | ↓↓ | ↓ | ↑ | ↓↓↓ |

**Legend:**
- ↑↑↑ = Very strong positive
- ↑↑ = Strong positive
- ↑ = Moderate positive
- ↔ = Neutral/mixed
- ↓ = Moderate negative
- ↓↓ = Strong negative
- ↓↓↓ = Very strong negative

## Time Horizon Considerations

**Immediate (Days):**
- Risk-off knee-jerk reactions
- Safe haven flows
- Energy spikes if supply threatened

**Short-term (Weeks-Months):**
- Reality check vs initial fears
- Supply chain actual disruptions materialize
- Central bank/government responses

**Medium-term (Months-Year):**
- Economic impact transmission
- Inflation effects through commodity channel
- Policy adjustments (strategic reserves, alternative suppliers)

**Long-term (Years):**
- Supply chain restructuring
- Energy transition acceleration
- Reserve currency implications

### Referencia: references/market_event_patterns.md

# Market Event Patterns and Market Reactions

## Central Bank Monetary Policy Events

### Federal Reserve (FOMC)

**Event Types:**
- Federal Funds Rate Decisions
- Quantitative Easing (QE) / Quantitative Tightening (QT) Announcements
- Forward Guidance Changes
- Emergency Policy Actions

**Typical Market Reactions:**

**Interest Rate Hikes:**
- **Equity Markets**: Generally negative, especially for high-growth/tech stocks (higher discount rates reduce present value of future earnings)
- **Bond Markets**: Bond prices fall, yields rise
- **Dollar (USD)**: Strengthens
- **Commodities**: Gold typically weakens (opportunity cost of holding non-yielding asset), Oil may weaken on demand concerns
- **Sectors Most Impacted**:
  - Technology: Negative (high valuations sensitive to rates)
  - Financials: Positive initially (higher net interest margins), but negative if rate hikes slow economy
  - Utilities/REITs: Negative (yield-sensitive sectors)
  - Consumer Discretionary: Negative (higher borrowing costs impact spending)

**Interest Rate Cuts:**
- **Equity Markets**: Generally positive, especially growth stocks
- **Bond Markets**: Bond prices rise, yields fall
- **Dollar (USD)**: Weakens
- **Commodities**: Gold strengthens, commodities generally positive
- **Sectors Most Impacted**:
  - Technology: Positive
  - Real Estate (REITs): Positive
  - Financials: Mixed (lower margins but better credit quality)

**Quantitative Easing (QE):**
- **Equity Markets**: Strong positive (liquidity injection)
- **Bond Markets**: Bond prices rise (central bank buying)
- **Dollar (USD)**: Weakens (currency debasement)
- **Commodities**: Positive across the board (inflation hedge)
- **Risk Assets**: Broad support

**Quantitative Tightening (QT):**
- **Equity Markets**: Negative pressure (liquidity withdrawal)
- **Bond Markets**: Yields rise (reduced central bank demand)
- **Dollar (USD)**: Strengthens
- **Commodities**: Mixed to negative

**Hawkish vs Dovish Tone:**
- **Hawkish** (inflation-focused, tightening bias): Risk-off, USD strength, bond yields up
- **Dovish** (growth-focused, easing bias): Risk-on, USD weakness, bond yields down

### European Central Bank (ECB)

**Key Differences from Fed:**
- Eurozone fragmentation concerns (peripheral vs core spreads)
- Negative rate environment history
- Bank-centric economy (vs capital markets in US)

**Typical Reactions:**
- EUR/USD currency pair highly sensitive
- European bank stocks react strongly to rate decisions
- Sovereign bond spreads (Italy, Spain, Greece vs Germany) sensitive to policy

### Bank of Japan (BOJ)

**Unique Characteristics:**
- Yield Curve Control (YCC) policy
- Decades of ultra-loose policy
- Direct equity ETF purchases

**Typical Reactions:**
- JPY movements extreme when policy shifts (especially YCC band adjustments)
- Japanese equity markets (Nikkei) sensitive to JPY movements (export-dependent)
- Global carry trade implications (JPY as funding currency)

### People's Bank of China (PBOC)

**Policy Tools:**
- Loan Prime Rate (LPR)
- Reserve Requirement Ratio (RRR)
- Medium-term Lending Facility (MLF)

**Typical Reactions:**
- Easing: Positive for commodities (China as major consumer), positive for EM currencies
- Tightening: Negative for commodities, negative for risk assets globally
- Australian Dollar (AUD) highly sensitive (China trade exposure)

## Inflation Data Releases

### US CPI (Consumer Price Index)

**Higher Than Expected:**
- **Equity Markets**: Negative (rate hike expectations increase)
- **Bond Yields**: Rise sharply
- **Dollar**: Strengthens
- **Gold**: Mixed (inflation positive but rate hike negative)
- **Fed Policy Expectations**: Hawkish shift

**Lower Than Expected:**
- **Equity Markets**: Positive rally
- **Bond Yields**: Fall
- **Dollar**: Weakens
- **Gold**: Strengthens
- **Fed Policy Expectations**: Dovish shift

### PPI (Producer Price Index)

- Leading indicator for CPI
- Strong reactions in industrial/materials sectors
- Commodity-linked stocks sensitive

### PCE (Personal Consumption Expenditures)

- Fed's preferred inflation measure
- Core PCE most important
- Similar directional reactions to CPI but often larger magnitude

## Employment Data

### Non-Farm Payrolls (NFP)

**Stronger Than Expected (High Job Growth):**
- **Initial Reaction**: Positive (economic strength)
- **Secondary Reaction**: Can turn negative if triggers rate hike concerns
- **Sectors**: Cyclicals outperform, defensives underperform

**Weaker Than Expected:**
- **Initial Reaction**: Negative (growth concerns)
- **Secondary Reaction**: Can turn positive if dovish policy response expected
- **Sectors**: Defensives outperform

**Wage Growth Component:**
- Higher wages: Inflation concerns, negative for equities
- Lower wages: Disinflationary, positive for equities

### Unemployment Rate

- Below natural rate (~4%): Inflation concerns
- Above natural rate: Growth concerns
- Initial claims (weekly): Leading indicator sensitivity

## GDP Reports

**Stronger Than Expected:**
- Positive for equities generally
- Currency strengthens
- Rate hike expectations increase (if economy already strong)

**Weaker Than Expected:**
- Negative for equities
- Currency weakens
- Rate cut expectations increase (if economy weakening)

**GDP Components Matter:**
- Consumer spending strength: Positive for Consumer sectors
- Business investment: Positive for Industrials, Technology
- Trade balance: Currency implications

## Geopolitical Events

### Military Conflicts / Wars

**Immediate Reactions:**
- **Equity Markets**: Risk-off selloff, especially in affected regions
- **Safe Havens**: USD, JPY, CHF strengthen; Gold rallies
- **Oil**: Spikes if energy supply disruption risk
- **Volatility (VIX)**: Surges

**Examples:**
- Russia-Ukraine conflict: Energy prices surge, European equities weak, defense stocks rally
- Middle East conflicts: Oil volatility, regional equity weakness

### Trade Wars / Tariffs

**Announcement of Tariffs:**
- **Affected Countries' Equities**: Negative
- **Export-Dependent Sectors**: Negative (Industrials, Materials)
- **Domestic-Focused Sectors**: Relative outperformance
- **Currencies**: Affected countries' currencies weaken

**US-China Trade Tensions:**
- Technology sector highly sensitive (supply chain concerns)
- Agricultural commodities volatile (retaliatory tariffs)
- Emerging market currencies under pressure

### Sanctions

- Targeted country's assets decline
- Replacement suppliers benefit (e.g., US LNG exports when Russian gas sanctioned)
- Financial sector compliance costs

## Corporate Earnings Events

### Mega-Cap Technology Earnings

**Companies: Apple, Microsoft, Amazon, Google, Meta, NVIDIA, Tesla**

**Impact on Broader Market:**
- Index-level impact significant (high market cap weights)
- Sector rotation triggers (Tech strength/weakness affects growth vs value)
- Forward guidance critical (AI spending, cloud growth, etc.)

**Typical Reactions:**
- **Beat + Raise**: Strong positive, often lifts entire index
- **Beat + Lower Guidance**: Negative despite beat
- **Miss**: Severe selloff, can drag indices significantly
- **AI-Related Themes**: NVIDIA results particularly market-moving (2023-2024)

### Banking Sector Earnings

**Major Banks: JPMorgan, Bank of America, Wells Fargo, Citigroup**

**Key Metrics:**
- Net Interest Margin (NIM): Rate environment sensitivity
- Credit Loss Provisions: Economic outlook indicator
- Trading Revenue: Market volatility impact
- Loan Growth: Economic activity proxy

**Broader Implications:**
- Financial sector earnings often lead cycle
- Credit quality trends predictive of recession risk
- Regional bank stress contagion risk (March 2023 example)

### Energy Sector Earnings

**Key Drivers:**
- Oil/gas price realizations
- Production volumes
- Capital discipline (buybacks vs drilling)

**Market Impact:**
- Correlated with commodity prices
- Inflation narrative implications
- Geopolitical overlay

## Credit Events

### Corporate Defaults / Distress

- Credit spreads widen
- Flight to quality (Treasuries rally)
- Equity markets negative (systemic risk concerns)
- High-yield bonds decline

### Credit Rating Changes

**Downgrades:**
- Stock price negative
- Bond yields rise (prices fall)
- Sector contagion if systemic

**Upgrades:**
- Stock price positive
- Bond yields fall (prices rise)
- Limited broader impact

## Commodity-Specific Events

### OPEC+ Meetings

**Production Cuts:**
- Oil prices rally
- Energy stocks positive
- Inflation concerns if sustained

**Production Increases:**
- Oil prices decline
- Energy stocks negative
- Disinflationary positive for growth stocks

### Grain/Agricultural Reports (USDA)

- Weather impacts (droughts, floods)
- Planting/harvest data
- Agricultural commodity prices volatile
- Food inflation implications

### Metals Supply Disruptions

- Mining strikes
- Export restrictions
- Positive for metal prices
- Mining stocks rally

## Recession Indicators

### Yield Curve Inversion (2s10s)

**Inversion (short rates > long rates):**
- Historical recession predictor (12-18 month lead time)
- Initial reaction: Risk-off
- Financials particularly negative (NIM compression)

**Steepening (disinversion):**
- Can signal imminent recession (ironically negative initially)
- Or economic acceleration (positive if growth-driven)

### Leading Economic Indicators (LEI)

- Manufacturing PMI (ISM)
- Consumer confidence
- Housing starts
- Composite LEI

**Negative readings:** Recession concerns mount progressively

## Historical Case Studies

### 2008 Financial Crisis

**Lehman Bankruptcy (September 2008):**
- Equities: S&P 500 -40% peak to trough
- Credit spreads: Blew out to crisis levels
- Safe havens: Treasuries rallied, gold initially sold (liquidity crisis) then rallied
- USD: Strengthened (deleveraging)

### COVID-19 Pandemic (March 2020)

**Initial Selloff:**
- Fastest bear market in history (S&P 500 -34% in weeks)
- Oil crashed (WTI briefly negative)
- VIX hit 80+

**Fed Response:**
- Unlimited QE announcement: Market bottom
- Zero rates, emergency facilities
- Equities: V-shaped recovery

### 2022 Inflation Shock

**Aggressive Fed Tightening:**
- 75bps hikes (unprecedented in modern era)
- Growth stocks crushed (Nasdaq -33%)
- Bonds no diversification (60/40 worst year since 1970s)
- Dollar rallied strongly

## Pattern Recognition Framework

### News Type Classification

**Tier 1 (Market-Moving):**
- FOMC decisions
- Inflation surprises (±0.2% from consensus)
- Major geopolitical shocks
- Mega-cap tech earnings misses
- Banking crisis events

**Tier 2 (Sector-Moving):**
- Sector-specific regulation
- Commodity supply disruptions
- Large corporate M&A
- Credit rating changes (investment grade)

**Tier 3 (Stock-Specific):**
- Individual company earnings
- Management changes
- Product launches
- Smaller M&A deals

### Sentiment Analysis

**Risk-On Environment:**
- Growth stocks outperform value
- High-beta outperforms low-beta
- Emerging markets outperform developed
- Credit spreads tight
- VIX low (<15)

**Risk-Off Environment:**
- Value stocks outperform growth (or decline less)
- Low-volatility outperforms
- Developed markets outperform emerging
- Credit spreads widen
- VIX elevated (>20)

### Time Horizon Considerations

**Immediate (Intraday):**
- Algorithmic/HFT reactions
- Often overshoot

**Short-term (Days-Weeks):**
- Fundamental reassessment
- Positioning adjustments

**Medium-term (Months):**
- Earnings revision cycles
- Policy transmission lags

**Long-term (Quarters-Years):**
- Structural shifts
- Regime changes

### Referencia: references/trusted_news_sources.md

# Trusted News Sources for Market Analysis

## Tier 1: Primary Sources (Highest Priority)

### Central Banks and Government Agencies

**Federal Reserve:**
- FederalReserve.gov - FOMC statements, meeting minutes, economic projections
- Federal Reserve Economic Data (FRED) - St. Louis Fed database
- Fed Chair speeches and testimonies

**U.S. Treasury:**
- Treasury.gov - Debt auctions, policy announcements
- Treasury International Capital (TIC) data

**Bureau of Labor Statistics (BLS):**
- Employment reports (Non-Farm Payrolls)
- CPI, PPI inflation data
- Wage statistics

**Bureau of Economic Analysis (BEA):**
- GDP reports
- Personal income and spending data
- Trade balance

**U.S. Census Bureau:**
- Retail sales
- Housing starts and permits
- Durable goods orders

**European Central Bank (ECB):**
- ECB.europa.eu - Policy decisions, press conferences

**Bank of Japan (BOJ):**
- BOJ.or.jp - YCC policy, intervention signals

**People's Bank of China (PBOC):**
- English.pbc.gov.cn - LPR, RRR decisions

**International Organizations:**
- International Monetary Fund (IMF.org)
- World Bank
- Bank for International Settlements (BIS)

### Securities and Exchange Commission (SEC)

- SEC.gov/edgar - Corporate filings
- 10-K/10-Q reports
- 8-K material events
- Form 4 insider trading
- 13-F institutional holdings

## Tier 2: Major Financial News Organizations

### Bloomberg

**Bloomberg.com / Bloomberg Terminal:**
- Real-time market data
- Breaking news (high speed)
- Economic calendar
- Company-specific news
- Commodity market coverage

**Strengths:**
- Speed and accuracy
- Terminal access for professionals
- Global coverage
- Proprietary data/analytics

**Usage Notes:**
- Subscription required for full access
- Terminal news (FIRST) most timely
- Search: "company earnings", "FOMC", "oil prices", "geopolitical"

### Reuters

**Reuters.com:**
- Wire service speed
- Global bureaus
- Political and economic coverage
- Commodities expertise

**Strengths:**
- Fact-based reporting
- International reach
- Breaking news accuracy
- Energy/commodity specialization

**Usage Notes:**
- Search: "central bank", "earnings", "trade war", "sanctions"

### Wall Street Journal (WSJ)

**WSJ.com:**
- In-depth analysis
- Corporate investigations
- Markets section excellent
- Fed coverage authoritative

**Strengths:**
- Quality journalism
- Source credibility
- Business insights
- Investigative depth

**Usage Notes:**
- Paywall (subscription needed)
- Search markets, economy, tech sections
- "Heard on the Street" column valuable

### Financial Times (FT)

**FT.com:**
- European market focus
- Global economics
- Central bank coverage
- Energy/commodities

**Strengths:**
- International perspective
- ECB/BOE expertise
- Emerging markets coverage
- Quality analysis

**Usage Notes:**
- Paywall (subscription)
- Search: "ECB", "emerging markets", "China economy"

### CNBC

**CNBC.com:**
- Real-time market updates
- CEO interviews
- Trader perspectives
- Options/derivatives coverage

**Strengths:**
- Market-moving headlines
- Live coverage during trading hours
- Accessible (free)
- Video content

**Usage Notes:**
- Search: "breaking news", "earnings", "fed", sector-specific
- "Squawk Box", "Closing Bell" segments notable

### MarketWatch

**MarketWatch.com:**
- Retail investor focus
- Market summaries
- Economic calendar
- Real-time quotes

**Strengths:**
- Accessible language
- Free access
- Market wrap coverage
- Economic data releases

### Barron's

**Barrons.com:**
- Weekend edition analysis
- Stock picks and pans
- Macro themes
- Investor interviews

**Strengths:**
- Thoughtful analysis
- Long-term perspective
- Contrarian views
- Technical analysis

## Tier 3: Specialized Sources

### Energy and Commodities

**S&P Global Platts:**
- Oil price assessments
- Energy market data
- Commodity analytics

**Rigzone:**
- Oil & gas industry news
- Upstream/downstream coverage

**Mining.com:**
- Metals and mining news
- Production data
- M&A coverage

**AgWeb / Farm Journal:**
- Agricultural markets
- Weather impacts
- USDA data analysis

### Technology

**The Information:**
- Tech industry scoops
- Startup coverage
- Big Tech investigations
- Subscription investigative journalism

**TechCrunch:**
- Startup funding
- Product launches
- Tech M&A

**Ars Technica:**
- Deep technical analysis
- Hardware/semiconductor coverage

**AnandTech:**
- Semiconductor deep dives
- Chip architecture

### Emerging Markets

**Emerging Markets.com:**
- EM debt and equity
- Currency analysis
- Political risk

**Africa Report, LatAm Reports:**
- Regional focus
- Mining, agriculture coverage

### China-Specific

**Caixin Global:**
- Independent Chinese business news
- Economic data analysis
- English language

**South China Morning Post (SCMP):**
- Hong Kong perspective
- Greater China coverage
- Business section

**China Daily (State Media):**
- Official government view
- Policy direction signals
- Use with awareness of bias

### Cryptocurrency/Digital Assets

**CoinDesk:**
- Crypto market news
- Regulatory developments
- Blockchain technology

**The Block:**
- Crypto investigative journalism
- Industry analysis

## Tier 4: Analysis and Research

### Independent Research

**Strategas Research Partners:**
- Washington policy analysis
- Political impact on markets

**BCA Research:**
- Global macro strategy
- Asset allocation

**Gavekal Research:**
- Macro analysis
- China expertise

### Central Bank Researchers

**Federal Reserve Bank Publications:**
- New York Fed (Liberty Street Economics blog)
- San Francisco Fed (Economic Letter)
- Cleveland Fed (Inflation expectations)

### Think Tanks

**Peterson Institute (PIIE):**
- International economics
- Trade policy

**Brookings Institution:**
- Economic policy research

**Council on Foreign Relations (CFR):**
- Geopolitical analysis

## Search and Aggregation Tools

### News Aggregators

**Google Finance:**
- Company-specific news aggregation
- Stock screeners

**Yahoo Finance:**
- Free real-time quotes
- News aggregation
- Earnings calendar

**Seeking Alpha:**
- Crowdsourced analysis
- Earnings call transcripts
- Varied quality (user-generated)

### Economic Calendars

**Forex Factory:**
- Economic event calendar
- Impact ratings
- Consensus estimates

**Investing.com:**
- Global economic calendar
- Real-time data
- Multi-asset coverage

**TradingEconomics.com:**
- Historical economic data
- Forecasts
- Country-specific

## News Source Quality Assessment

### Reliability Indicators

**Positive Signals:**
- Named sources
- Corroborating reports from multiple outlets
- Official statements/documents referenced
- Transparent corrections policy
- Separation of news and opinion

**Red Flags:**
- Anonymous sources only
- Single-source stories
- Sensational headlines mismatching content
- Lack of verification
- Ideological bias overwhelming facts

### Speed vs. Accuracy Trade-off

**Fastest (Use for Alerts, Verify Later):**
- Bloomberg Terminal (FIRST function)
- Reuters wire
- Twitter/X (major news organizations' verified accounts)

**Most Accurate (Use for Analysis):**
- WSJ, FT investigative pieces
- Official government data releases
- SEC filings
- Central bank statements

**Balanced (Speed + Reliability):**
- Bloomberg web
- Reuters web
- CNBC breaking news

## Source Selection by News Type

### Monetary Policy (Fed, ECB, BOJ)

**Primary:**
1. Central bank official websites
2. WSJ Fed coverage
3. Reuters central bank desk
4. FT central banking section

**Supplementary:**
- Bloomberg central bank reporters (specific journalists)
- CNBC live Fed coverage

### Corporate Earnings

**Primary:**
1. Company press releases (IR websites)
2. SEC filings (10-Q, 8-K)
3. Bloomberg earnings coverage
4. WSJ company coverage

**Supplementary:**
- Seeking Alpha transcripts
- CNBC earnings alerts
- MarketWatch summaries

### Geopolitical Events

**Primary:**
1. Reuters international desk
2. FT geopolitical coverage
3. Bloomberg geopolitical news
4. BBC (for initial breaking news)

**Supplementary:**
- CFR analysis (for context)
- Energy-specific: Platts, Rigzone (if energy-related)

### Commodity Markets

**Primary:**
1. Reuters commodity desk
2. S&P Global Platts
3. Bloomberg commodity coverage

**Supplementary:**
- Mining.com (metals)
- AgWeb (agriculture)
- Rigzone (energy)

### Technology Sector

**Primary:**
1. Bloomberg tech
2. WSJ tech section
3. The Information (scoops)
4. Reuters tech coverage

**Supplementary:**
- TechCrunch (startups)
- Ars Technica (semiconductors)
- Company blogs (for product launches)

## Recommended News Search Strategy

### For Comprehensive 10-Day Analysis

**Day 1-2: Broad Search**
- Search terms: "stock market", "federal reserve", "inflation", "oil prices", "earnings", "geopolitical"
- Sources: Bloomberg, Reuters, WSJ
- Identify major themes

**Day 3-5: Deep Dive on Major Events**
- Identified themes: Search specific (e.g., "FOMC meeting", "NVIDIA earnings", "Israel conflict oil")
- Sources: Add FT, CNBC, specialized (Platts for commodities)
- Read original statements/filings when available

**Day 6-7: Impact Analysis**
- Market reaction search: "[Event] market reaction", "S&P 500 response", sector impacts
- Sources: MarketWatch, Barron's, Seeking Alpha (for varied perspectives)
- Analyst commentary

**Day 8-10: Synthesis**
- Connect dots between events
- Look for contrary indicators
- Verify facts across multiple sources

### WebSearch Query Recommendations

**For Recent News (Past 10 Days):**
- "stock market news past week"
- "FOMC meeting [current month]"
- "major earnings reports [current month]"
- "geopolitical events impacting markets [current month]"
- "oil prices news last 10 days"
- "Federal Reserve policy [current month]"

**For Specific Events:**
- "[Company] earnings [quarter] [year]"
- "FOMC statement [date]"
- "[Geopolitical event] commodity prices"
- "[Country] central bank decision [date]"

**For Market Reactions:**
- "[Event] market reaction"
- "S&P 500 [date] why"
- "[Sector] stocks [event]"

## Source Credibility Framework

### Tier 1 (Official, Primary Sources):
- Use for facts, data, official policy
- No interpretation needed, direct information

### Tier 2 (Major Financial Press):
- Use for breaking news, broad coverage
- Cross-check major scoops
- Trust for market-moving headlines

### Tier 3 (Specialized):
- Use for domain-specific deep dives
- Valuable for niche sectors
- Supplement Tier 1 & 2

### Tier 4 (Analysis):
- Use for interpretation, context
- Understand potential biases
- Compare multiple viewpoints

## Red Flag News Sources (Avoid or Use with Extreme Caution)

- Unverified social media rumors
- Clickbait financial sites
- Pump-and-dump stock promoters
- Anonymous blogs without editorial standards
- News aggregators without source verification
- AI-generated content farms (without human editorial)

## Best Practices

1. **Primary Source First**: Always seek official statements, filings, data releases
2. **Multiple Confirmation**: Major news should appear in 2+ Tier 2 sources
3. **Speed vs Accuracy**: Use fast sources for alerts, authoritative for analysis
4. **Bias Awareness**: Understand each source's perspective (US-centric, China-focused, etc.)
5. **Date Verification**: Ensure news is actually recent (past 10 days for this analysis)
6. **Update Cycle**: Some news develops over days (FOMC speculation → decision → reaction)


---

## SKILL: model-update

- Fuente: `anthropics/financial-services` → `plugins/agent-plugins/earnings-reviewer/skills/model-update` (Apache-2.0)
- Cuándo usarla: Update financial models with new data — quarterly earnings, management guidance, macro changes, or revised assumptions. Adjusts estimates, recalculates valuation, and flags material changes. Use after earnings, guidance updates, or when assumptions need refreshing. Triggers on "update model", "plug earnings", "refresh estimates", "update numbers for [company]", "new guidance", or "revise estimates".

# Model Update

## Workflow

### Step 1: Identify What Changed

Determine the update trigger:
- **Earnings release**: New quarterly actuals to plug in
- **Guidance change**: Company updated forward outlook
- **Estimate revision**: Analyst changing assumptions based on new data
- **Macro update**: Interest rates, FX, commodity prices changed
- **Event-driven**: M&A, restructuring, new product, management change

### Step 2: Plug New Data

#### After Earnings
Update the model with reported actuals:

| Line Item | Prior Estimate | Actual | Delta | Notes |
|-----------|---------------|--------|-------|-------|
| Revenue | | | | |
| Gross Margin | | | | |
| Operating Expenses | | | | |
| EBITDA | | | | |
| EPS | | | | |
| [Key metric 1] | | | | |
| [Key metric 2] | | | | |

**Segment Detail** (if applicable):
- Update each segment's revenue and margin
- Note any segment mix shifts

**Balance Sheet / Cash Flow Updates**:
- Cash and debt balances
- Share count (buybacks, dilution)
- Capex actual vs. estimate
- Working capital changes

### Step 3: Revise Forward Estimates

Based on the new data, adjust forward estimates:

| | Old FY Est | New FY Est | Change | Old Next FY | New Next FY | Change |
|---|-----------|-----------|--------|------------|------------|--------|
| Revenue | | | | | | |
| EBITDA | | | | | | |
| EPS | | | | | | |

**Key Assumption Changes:**
- What assumptions are you changing and why?
- Revenue growth rate: old → new (reason)
- Margin assumption: old → new (reason)
- Any new items (restructuring charges, one-time gains, etc.)

### Step 4: Valuation Impact

Recalculate valuation with updated estimates:

| Valuation Method | Prior | Updated | Change |
|-----------------|-------|---------|--------|
| DCF fair value | | | |
| P/E (NTM EPS × target multiple) | | | |
| EV/EBITDA (NTM EBITDA × target multiple) | | | |
| **Price Target** | | | |

### Step 5: Summary & Action

**Estimate Change Summary:**
- One paragraph: what changed, why, and what it means for the stock
- Is this a thesis-changing event or noise?

**Rating / Price Target:**
- Maintain or change rating?
- New price target (if changed) with methodology
- Upside/downside to current price

### Step 6: Output

- Updated Excel model (if user provides the existing model)
- Estimate change summary (markdown or Word)
- Updated price target derivation

## Important Notes

- Always reconcile your estimates to the company's reported figures before projecting forward
- Note any non-recurring items and whether your estimates are GAAP or adjusted
- Track your estimate revision history — it shows your analytical progression
- If the quarter was noisy, separate signal from noise in your estimate changes
- Check consensus after updating — how do your revised estimates compare to the Street?
- Share count matters — dilution from stock comp, converts, or buybacks can materially affect EPS


---

## SKILL: morning-note

- Fuente: `anthropics/financial-services` → `plugins/agent-plugins/earnings-reviewer/skills/morning-note` (Apache-2.0)
- Cuándo usarla: Draft concise morning meeting notes summarizing overnight developments, trade ideas, and key events for coverage stocks. Designed for the 7am morning meeting format — tight, opinionated, actionable. Triggers on "morning note", "morning meeting", "what happened overnight", "trade idea", "morning call prep", or "daily note".

# Morning Note

## Workflow

### Step 1: Overnight Developments

Scan for relevant events across coverage universe:

**Earnings & Guidance**
- Any coverage companies reporting overnight or pre-market?
- Earnings surprises (beat/miss on revenue, EPS, key metrics)
- Guidance changes (raised, lowered, maintained)

**News & Events**
- M&A announcements or rumors
- Management changes
- Product launches or regulatory decisions
- Analyst upgrades/downgrades from competitors
- Macro data or policy changes affecting the sector

**Market Context**
- Overnight futures / pre-market moves
- Sector ETF performance
- Relevant commodity or currency moves
- Key economic data releases today

### Step 2: Morning Note Format

Keep it tight — a morning note should be readable in 2 minutes:

---

**[Date] Morning Note — [Analyst Name]**
**[Sector Coverage]**

**Top Call: [Headline — the one thing PMs need to hear]**
- 2-3 sentences on the key development and why it matters
- Stock impact: price target, rating reiteration/change

**Overnight/Pre-Market Developments**
- [Company A]: One-line summary of earnings/news + our take
- [Company B]: One-line summary + our take
- [Sector/Macro]: Relevant sector-wide development

**Key Events Today**
- [Time]: [Company] earnings call
- [Time]: Economic data release (expectations vs. our view)
- [Time]: Conference or investor day

**Trade Ideas** (if any)
- [Long/Short] [Company]: 1-2 sentence thesis + catalyst
- Risk: What would make this wrong

---

### Step 3: Quick Takes on Earnings

If a coverage company reported, provide a quick reaction:

| Metric | Consensus | Actual | Beat/Miss |
|--------|-----------|--------|-----------|
| Revenue | | | |
| EPS | | | |
| [Key metric] | | | |
| Guidance | | | |

**Our Take**: 2-3 sentences — is this good or bad for the stock? Does it change our thesis?

**Action**: Maintain / Upgrade / Downgrade rating? Adjust price target?

### Step 4: Output

- Markdown text for email/Slack distribution
- Word document if formal distribution is needed
- Keep to 1 page max — PMs and traders won't read more

## Important Notes

- Be opinionated — morning notes that just summarize news without a view are useless
- Lead with the most important thing — don't bury the headline
- "No news" is a valid morning note — say "nothing material overnight, maintaining positioning"
- Distinguish between actionable events (earnings, M&A) and noise (minor analyst notes, non-events)
- Time-stamp your takes — if you're writing at 6am, note that pre-market may change by open
- If you're wrong, own it in the next morning note — credibility matters more than being right every time


---

## SKILL: news-reaction-failure-analyzer

- Fuente: `tradermonty/claude-trading-skills` → `skills/news-reaction-failure-analyzer` (MIT)
- Cuándo usarla: Judge whether a market FAILED to react to news favorable to a crowded speculative position — step 2 of Jason Shapiro's COT contrarian process. Consumes a cot-contrarian-detector report (or an explicit direction) plus a Claude-curated events JSON, fetches the underlying price series with a documented fallback chain, and produces a fail-closed CONFIRMED / NOT_CONFIRMED / INSUFFICIENT_EVIDENCE verdict using a statistically validated drift-significance test (not a naive failure-ratio, which false-confirms on pure noise). Generic beyond COT — reusable for PEAD and macro-crowding news-failure checks. Use when the user asks to check news-failure confirmation, whether a crowded market "shrugged off" good/bad news, or wants to run Shapiro step 2 on a CROWDED_LONG/CROWDED_SHORT market.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/news-reaction-failure-analyzer/` (requirements.txt, analyze_news_reaction.py, reaction_math.py)

# News Reaction Failure Analyzer

## Overview

Implements step 2 of Jason Shapiro's COT contrarian process: once a market
is flagged as crowded (`cot-contrarian-detector`, step 1), check whether it
FAILED to react to news that should have rewarded the crowd. A crowded-long
market that doesn't rally on genuinely bullish news, or a crowded-short
market that doesn't sell off on genuinely bearish news, is the core
behavioral tell that the crowd has run out of buying/selling power — this
is the confirmation step that turns "crowded" into a contrarian setup
candidate (steps 3-5, still manual: price-action confirmation, entry, exit).

**Why this isn't a naive failure-ratio check:** an earlier design flagged
"news failure" whenever fewer than half the relevant events "responded" —
but under pure noise, roughly 69% of individual events fail to respond by
chance, so that rule would CONFIRM on random noise 48-83% of the time
depending on sample size. This skill instead requires the market to have
moved *significantly against* the crowd's favorable news (a drift-
significance test with a Monte-Carlo-verified null false-positive bound),
never merely "didn't respond enough." See
`references/news-failure-patterns.md` for the full statistical rationale.

## When to Use This Skill

**English:**
- "Did the market shrug off [event] even though [asset] is crowded long/short?"
- "Run a news-failure check on [symbol]"
- "Is [symbol] confirmed for a Shapiro-style contrarian setup?"
- After `cot-contrarian-detector` flags a market CROWDED_LONG / CROWDED_SHORT
  and the user wants to move to step 2

**Japanese:**
- 「この市場は好材料に反応しなかった？」
- 「COTで偏っているこの銘柄のニュース失敗を確認して」

**Do NOT use when:**
- The market isn't crowded (NEUTRAL classification) — this skill refuses
  fail-closed without an explicit `--direction` override
- No curated events JSON exists yet — WebSearch must run first (Phase 2
  below); never fabricate events or URLs to get a verdict

## Prerequisites

- **FMP API Key:** Required. Set `FMP_API_KEY` or pass `--api-key`. Used
  for price data only (`stable/historical-price-eod/light`) — coverage
  varies by symbol; see `references/price-source-map.md`.
- **Python 3.9+** with `requests` installed.
- **WebSearch access** to curate the events JSON (Phase 2). Skill degrades
  gracefully without it (states the limitation; never fabricates events).
- **Optional:** a `cot-contrarian-detector` JSON report (`--detector-json`)
  to auto-resolve symbol + direction, or supply `--direction` explicitly.

## Workflow

### Phase 1: Obtain symbol + direction

From a `cot-contrarian-detector` report (`--detector-json`, symbol looked
up in `markets[]`) or directly from the user (`--symbol` + `--direction`).
A `NEUTRAL` classification, a symbol missing from the report, or a report
older than `--max-detector-age-days` (default 10) all refuse fail-closed
with a specific reason — only an explicit `--direction` overrides.

### Phase 2: Curate the events JSON via WebSearch

Search news in the evaluation window (`--window-days`, default 10) using
the 4-tier source hierarchy (issuer/primary → SEC/official stats → wire →
portal — see `references/news-failure-patterns.md`). Write findings into
an events JSON from `references/news-failure-patterns.md`'s template —
`event`, `event_time` (ISO8601 with explicit UTC offset), `source_url`,
`source_tier`, `expected_impact` (BULLISH/BEARISH) per event.

**Never fabricate events or URLs.** WebSearch unavailable → state it
explicitly; proceed without an events JSON only if the user accepts an
`INSUFFICIENT_EVIDENCE` result (reason `no_events_provided`) — the CLI
never raises an exception for a missing events file, it always exits 0
with a documented reason.

### Phase 3: Run the CLI

```bash
python3 skills/news-reaction-failure-analyzer/scripts/analyze_news_reaction.py \
  --symbol B6 --detector-json reports/cot_crowding_2026-07-12.json \
  --events-json reports/nrf_events_B6_2026-07-12.json \
  --output-dir reports/
```

The script fetches the price series (documented fallback chain — futures
symbol first, ETF proxy if 402/restricted or `rows == 0`; see
`references/price-source-map.md`), computes effective dates / returns /
z-scores per event, clusters events whose 3-trading-day windows overlap
(independence guard), and synthesizes the verdict.

### Phase 4: Present verdict + handoff

Present the verdict, aggregate stats (`drift_stat`, `responded_ratio`), and
the evidence table (per-event returns/z-scores/reaction labels, with any
`dropped_events` reasons shown — never silently hidden). If a proxy
(`run_context.proxy_used`) was used, note the tracking-error caveat.

Emit a handoff block for `contrarian-setup-gate` (#241, not yet built):

```json
{"news_failure": {"verdict": "CONFIRMED", "confidence": "HIGH", "report_path": "reports/nrf_B6_2026-07-12.json"}}
```

## Output

- **JSON:** `reports/nrf_<symbol>_<as-of-date>.json` — `schema_version`,
  `symbol`, `direction`, `expected_direction`, `actual_reaction`
  (`FAILED_TO_RALLY`/`FAILED_TO_SELL_OFF`/`RALLIED`/`SOLD_OFF`/
  `MIXED_REACTION`/`NO_DATA`), `verdict`, `confidence`,
  `relevant_events_used`, `aggregate` (mean_z3/drift_stat/responded_ratio),
  `evidence[]`, `dropped_events[]`, `run_context`.
- **Markdown:** `reports/nrf_<symbol>_<as-of-date>.md` — human-readable
  verdict, aggregate stats, evidence table, dropped-events table, proxy
  caveat (if used), and methodology footnote.

## Guardrails

- **CONFIRMED is not a trade signal.** It confirms step 2 of 5 — price-
  action confirmation (step 3), entry (step 4), and exit (step 5) are still
  manual and still required before any position.
- **INSUFFICIENT_EVIDENCE never advances the pipeline.** Fewer than
  `--min-events` (default 3) usable relevant event *clusters*, a missing
  detector report, or a detector vintage (`data_date`) that's missing,
  unparsable, dated after `--as-of`, or older than
  `--max-detector-age-days` (stale), a `NEUTRAL` classification without an
  explicit override, or no working price source all produce this verdict
  — never a crash, never a forced call on inadequate data.
- **COT publication lag.** COT data is 3-9 days old by the time it's read
  (see `cot-contrarian-detector`); news-failure evidence should be read in
  that context, not as same-day confirmation.
- **Counter-direction events are context only** — shown in the evidence
  table but excluded from the verdict (only events whose `expected_impact`
  matches the crowd's `expected_direction` count).
- **Proxy-based prices are noted, not hidden.** When an ETF proxy was used
  (`run_context.proxy_used`), the report says so — tracking error, expense
  drag, and roll-timing differences make the reaction-direction read
  approximate, not exact.
- **Residual statistical risk under extreme correlation.** The verdict's
  null false-CONFIRMED rate is hard-verified under i.i.d. noise (<8%) and
  under a realistic residual-correlation stress (AR(1) ρ=0.1, <10%). Under
  an intentionally extreme correlation stress (lag-1 ρ=0.3 across
  non-clustered event windows — roughly 10x liquid-futures empirical
  autocorrelation), the measured null rate rises to ~11-13%. This is a
  documented v1 limitation, not a silent gap — see
  `references/news-failure-patterns.md` for the full numbers. Users who
  want the stricter <10% margin even under that stress can pass
  `--drift-z 1.75` (at the cost of missing some genuine news-failure
  signals, not just noise).
- **Not investment advice.** Research/educational purposes only.

## Resources

### `references/news-failure-patterns.md`
Full methodology: what qualifies as a relevant event, the 4-tier source
hierarchy, worked examples, the events-JSON curation guide + template, and
the verdict-threshold rationale (why drift-significance, not a naive
ratio; the Monte-Carlo-verified null bounds).

### `references/price-source-map.md`
Per-market price-source fallback chain, verified/402/0-rows status (live-
probed at implementation time), ETF-proxy caveats, and markets with no
viable source (documented `no_price_source` cases: VX, ZQ, HO, all agri on
this key).

### When to Load References
- **First use / explaining the methodology:** Load
  `references/news-failure-patterns.md`
- **Explaining why a market has no verdict (no_price_source):** Load
  `references/price-source-map.md`
- **Regular execution:** References not needed for the CLI itself — needed
  for Phase 2 (events curation) and for explaining results to the user

### Referencia: references/news-failure-patterns.md

# News Failure Patterns (Shapiro Step 2)

## Overview

Step 2 of Jason Shapiro's COT contrarian process (see
`cot-contrarian-detector/references/shapiro-methodology.md` for the full
5-step process) is the core edge: once a market is crowded, check whether
it FAILED to react to news that should have rewarded the crowd. This
document covers what qualifies as a relevant event, how to curate an
events JSON via WebSearch, and the statistical rationale behind the
verdict this skill computes.

## What Qualifies as a Relevant Event

A relevant event is a discrete, dateable piece of news whose
`expected_impact` matches the crowd's `expected_direction`
(CROWDED_LONG → BULLISH news; CROWDED_SHORT → BEARISH news). Examples:

- **Macro data releases** favorable to the crowd's direction (a strong
  jobs report or dovish Fed surprise for a crowded-long equity index; a
  hot CPI print or hawkish Fed surprise for a crowded-short bond market)
- **Company/sector-specific catalysts** for single-name-adjacent futures
  (e.g. a major constituent's earnings beat for an equity index future)
- **Supply/demand shocks** for commodities (an OPEC production cut for
  crowded-short crude; a bumper-crop report for crowded-long grains)
- **Central bank/policy surprises** in the crowd's favor

Counter-direction events (news that would hurt the crowd) are recorded for
context but excluded from the verdict — mixing them in would test the
wrong thing (whether the market reacted to bad news, not whether it failed
to react to good news).

## Worked Example (illustrative)

Large speculators are crowded long on the S&P 500 (COT Index 95+, per
`cot-contrarian-detector`). Over the following two weeks: a strong jobs
report, a dovish Fed comment, and a mega-cap earnings beat all hit — three
genuinely bullish catalysts. If the index barely moves, or sells off, on
all three, that's the tell: everyone who was going to buy on good news
already has. `verdict: CONFIRMED` here means "the market has stopped
rewarding good news for the crowd's direction" — not a prediction of what
happens next; steps 3-5 (price action, entry, exit) still apply.

## Source Hierarchy (4 tiers)

Matches the tier structure used elsewhere in this repo (see
`kanchi-dividend-sop`'s Step 6 event-scan convention) and the issue's
`source_tier` contract:

1. **`primary`** — the issuer/company/agency's own release (press release,
   IR page, official statement)
2. **`official`** — government/regulatory statistics or filings (BLS, Fed,
   SEC, Treasury, central bank statements)
3. **`wire`** — reputable wire services (Reuters, Bloomberg, AP, Dow Jones)
4. **`portal`** — finance news portals/aggregators (secondary only — use
   when primary/official/wire coverage isn't available, and prefer a
   portal article that itself cites a primary source)

Always prefer the highest tier available for a given event; record the
tier used in `source_tier` so the report's evidence table shows source
quality alongside the reaction data.

## Events JSON Curation Guide

WebSearch news in the CLI's `--window-days` window (default 10 days
before `--as-of`). For each candidate event:

1. Confirm it's genuinely dateable (a specific release date/time, not a
   vague "recent trend")
2. Classify `expected_impact` (BULLISH/BEARISH) from the crowd's
   perspective — ask "would a rational holder of the crowd's position see
   this as good news?"
3. Record `event_time` in ISO8601 **with an explicit UTC offset**
   (`2026-07-08T14:30:00-04:00`) — a naive timestamp is rejected by the
   CLI (dropped with reason `unparsable_event_time`) rather than guessing
   at an implicit timezone
4. Cite the real `source_url` and `source_tier` — **never fabricate a URL
   or an event**. If WebSearch can't find a genuinely relevant event in
   the window, that's a valid (if less useful) outcome — don't pad the
   list to hit `--min-events`

### Template

```json
{
  "schema_version": "1.0",
  "symbol": "ES",
  "curated_at": "2026-07-12",
  "events": [
    {
      "event_id": "e1",
      "event": "Fed cuts rates 25bp, signals more cuts ahead",
      "event_time": "2026-07-08T14:30:00-04:00",
      "source_url": "https://www.federalreserve.gov/newsevents/pressreleases/...",
      "source_tier": "official",
      "expected_impact": "BULLISH",
      "notes": "Dovish surprise vs. consensus hold"
    }
  ]
}
```

Save as `reports/nrf_events_<symbol>_<as-of-date>.json` and pass via
`--events-json`.

## Verdict Thresholds (statistical rationale)

**Why not a naive failure-ratio?** An earlier design flagged CONFIRMED
whenever fewer than half of relevant events "responded" (moved favorably
for the crowd). Under pure noise, P(an individual event's z-score < the
response threshold) is roughly 69%, so that naive rule CONFIRMed on random
noise 48-83% of the time depending on sample size — statistically
worthless. See `cot-contrarian-detector`-style design notes; this is the
same class of flaw a naive threshold rule falls into.

**The drift-significance design** (implemented in
`scripts/reaction_math.py`) instead requires the market to have moved
*significantly against* favorable news, not merely "not enough with it":

- `drift_stat = sqrt(n) * mean(direction-adjusted zscore_3d)` over the
  usable, clustered, relevant events (n = number of clusters, not raw
  event count — see "Event Clustering" below)
- Under the null hypothesis (no real drift, iid noise), `drift_stat` is
  approximately standard normal
- `CONFIRMED` iff `drift_stat <= -drift_z` AND `responded_ratio <= 0.25`
  (both conditions — a strong drift alone isn't enough if a meaningful
  fraction of individual events still "responded")
- `drift_z` default is **1.45**, chosen (over 1.0, 1.28, and 1.35, all
  rejected) so the combined null false-CONFIRMED rate stays under a
  documented bound, verified by a seeded, ≥50,000-trial-per-n Monte Carlo
  test — see `scripts/reaction_math.py`'s `DRIFT_Z_DEFAULT` constant for
  the exhaustive rationale comment and
  `scripts/tests/test_reaction_math.py` for the tests themselves

**Measured null false-CONFIRMED rates at drift_z=1.45** (n ∈ {3,4,5,8},
50,000 trials per n per scenario, seeded for reproducibility):

| Scenario | Bound | Worst measured | Gate |
|---|---|---|---|
| i.i.d. N(0,1) noise | < 8% | 7.28-7.30% (varies by MC run) | Hard-asserted |
| AR(1) lag-1, ρ=0.1 (residual correlation after clustering) | < 10% | 9.00% (n=8); range 8.08-9.00% | Hard-asserted |
| AR(1) lag-1, ρ=0.3 (extreme correlation stress) | informational | 13.11% (n=8); range 10.84-13.11% | Measured only, sanity ceiling < 20% |

**Why ρ=0.1 is hard-gated and ρ=0.3 is informational, not hard-gated:**
the clustering rule (below) already removes the correlation a window
overlap would produce — that is precisely the failure mode a correlation
stress test is meant to probe. Across *non-overlapping* 3-day cluster
windows, a lag-1 correlation of ρ=0.3 is roughly an order of magnitude
stronger than the empirical signed-return autocorrelation of liquid
futures contracts. ρ=0.1 remains conservative relative to that empirical
reality while still exercising the realistic residual channel (e.g. two
related headlines a week apart, outside the clustering window but still
weakly correlated), so it is the asserted regression gate. ρ=0.3 is kept
and measured — not silently dropped — as a documented v1 residual risk:
if real-world correlation between non-clustered events is ever that
extreme, the null false-CONFIRMED rate could rise into the 11-13% range.
**Escape hatch:** `--drift-z 1.75` restores a <10% null rate even under
the ρ=0.3 stress scenario (verified), for users who want that extra
margin — at the cost of reduced sensitivity to genuine news-failure
signals (a stricter threshold also misses some real drift, not just
noise).

## Event Clustering (Independence Guard)

Relevant events whose 3-trading-day return windows share any trading day
are collapsed into one cluster, counted once toward `n`, using the
earliest effective date. Rationale: overlapping windows produce
correlated z-scores (the same price move gets counted as "evidence" for
multiple events), which would silently inflate `n` and violate the
approximately-normal-under-the-null assumption the verdict test relies on.

**Pinned rule: a cluster's z3 is the z3 already computed at the cluster's
own effective date — the earliest member's window z3. Member z3 values
are never averaged into the cluster's contribution to `drift_stat`.**
Averaging would mix z-scores computed over different, overlapping return
windows into a statistic that isn't obviously more meaningful than "what
happened in the window starting at the cluster's own effective date," and
would complicate the variance properties the Monte Carlo verification
above relies on. Cluster membership — including every member's own
individual z3 — is always shown in the evidence (`cluster_members[]`) so
nothing is hidden, even though only the earliest member's z3 drives the
verdict.

## Effective Date and Return Windows

- **Effective date:** the first trading date at/after the event. Events at
  or after 16:00 ET count from the next trading day (the close has
  already happened). Weekend/holiday gaps degrade naturally to the next
  available trading bar — never a crash.
- **Returns:** `close(eff + k - 1 trading days) / close(eff - 1 trading
  day) - 1`, for k ∈ {1, 3} — a true k-trading-session return: the k
  sessions starting at, and including, the effective date itself, against
  the close the day before (capturing any overnight/opening gap). For
  k=1 that's just `close(eff) / close(eff-1)`; for k=3 it's
  `close(eff+2) / close(eff-1)` (the 3 sessions eff, eff+1, eff+2).
- **Z-scores:** `daily_stdev` is the sample stdev of trailing daily
  returns ending the day before the event (60-trading-day lookback by
  default). `zscore_1d = return_1d / daily_stdev`; `zscore_3d = return_3d
  / (daily_stdev * sqrt(3))` — the sqrt(3) horizon scaling is mandatory
  (a k-day return's noise scales with sqrt(k) under a random-walk
  assumption).

## What Stays Manual (Shapiro Steps 3-5)

This skill automates step 2 only. Steps 3 (price-action confirmation), 4
(entry), and 5 (exit) remain manual — see
`cot-contrarian-detector/references/shapiro-methodology.md`. A CONFIRMED
verdict here is a necessary but not sufficient condition for a contrarian
trade.

### Referencia: references/price-source-map.md

# Price Source Map

## Overview

COT symbols (`ES`, `GC`, `B6`, ...) are not FMP price symbols. This skill
maps each COT symbol to a fallback chain of FMP price symbols, tried in
order via `stable/historical-price-eod/light`. A source "fails" on an HTTP
error (commonly 402, "restricted" — this endpoint's per-symbol coverage is
uneven even on a Premium+ plan) **or** on `rows == 0` — a distinct,
important failure mode where the endpoint returns HTTP 200 with an empty
body rather than an error. Both must be checked explicitly; treating only
HTTP errors as failures would silently produce an empty/misleading price
series for symbols like `VXUSD`.

**Field-name gotcha (verified live):** this endpoint's row shape uses a
`price` field for the daily settlement value, not `close` — confirmed
across futures (`ESUSD`), ETF (`QQQ`), and FX (`GBPUSD`) symbols alike, so
it's an endpoint-wide quirk, not an asset-class difference. Missing this
would silently produce an all-rows-dropped empty series (every symbol
would look like a `no_price_source` failure) rather than an obvious error.
`reaction_math.build_sorted_series()` handles this by accepting `close`
first, falling back to `price`.

The chain constant lives in `scripts/analyze_news_reaction.py`
(`PRICE_SOURCE_CHAINS`); this document records the verified status of each
entry so a human (or Claude) can tell at a glance which markets have a
working source, which fall back to an ETF proxy, and which have none.

## Status Table (live-probed 2026-07-12, on the project's FMP key)

| COT symbol | Chain (→ = fallback) | Status |
|---|---|---|
| ES | ESUSD | 200 OK |
| NQ | NQUSD → QQQ | 402 → ETF OK |
| YM | YMUSD → DIA | 402 → ETF OK |
| QR | RTYUSD → IWM | 402 → ETF OK |
| VX | VXUSD | 200, **0 rows** → `no_price_source` |
| GC | GCUSD | 200 OK |
| SI | SIUSD | 200 OK |
| HG | HGUSD → CPER | 402 → ETF OK |
| PL | PLUSD → PPLT | 402 → ETF OK |
| PA | PAUSD → PALL | 402 → ETF OK |
| CL | CLUSD → BZUSD → USO | 402 → BZUSD 200 OK (grade caveat below; USO untried since BZUSD already succeeds) |
| NG | NGUSD → UNG | 402 → ETF OK |
| RB | RBUSD → UGA | 402 → ETF OK |
| HO | HOUSD | 402, no proxy → `no_price_source` |
| ZT | ZTUSD → SHY | 402 → ETF OK |
| ZF | ZFUSD → IEI | 402 → ETF OK |
| ZN | ZNUSD → IEF | 402 → ETF OK |
| ZB | ZBUSD → TLT | 402 → ETF OK |
| ZQ | ZQUSD | 402, no proxy → `no_price_source` |
| DX | DXUSD → UUP | 402 → ETF OK |
| B6 (GBP) | GBPUSD | 200 OK |
| E6 (EUR) | EURUSD | 200 OK |
| J6 (JPY) | JPYUSD | 200 OK |
| S6 (CHF) | CHFUSD | 200 OK |
| D6 (CAD) | CADUSD | 200 OK |
| A6 (AUD) | AUDUSD | 200 OK |
| N6 (NZD) | NZDUSD | 200 OK |
| BT (Bitcoin) | BTCUSD | 200 OK |
| ZC (Corn) | ZCUSD | 200, **0 rows** → `no_price_source` (no proxy documented yet) |
| ZS (Soybeans) | ZSUSD | 200, **0 rows** → `no_price_source` |
| ZM (Soybean Meal) | ZMUSD | 402, no proxy → `no_price_source` |
| ZL (Soybean Oil) | ZLUSD | 200, **0 rows** → `no_price_source` |
| ZW (Wheat) | ZWUSD | 200, **0 rows** → `no_price_source` |

**No viable source documented (v1 limitation):** VX, ZQ, HO, and all five
agri markets probed (ZC, ZS, ZM, ZL, ZW). Every case fails closed —
`analyze_news_reaction.py` returns `verdict: INSUFFICIENT_EVIDENCE`,
reason `no_price_source`, never a crash or a misleading result from an
empty series. An ETF proxy chain can be added for any of these once a
working source is identified (grain ETFs like `CORN`/`SOYB`/`WEAT` exist
and are plausible candidates, but were not verified against this key at
implementation time — do not assume they work without probing first).

## ETF Proxy Caveats

When a chain falls back to an ETF (`kind: "etf"` in `PRICE_SOURCE_CHAINS`,
surfaced as `run_context.proxy_used: true` in the report), the reaction-
direction read is approximate, not exact:

- **Tracking error:** the ETF doesn't perfectly replicate the futures
  contract's daily return (fees, sampling, cash drag)
- **Expense drag:** a small daily headwind (typically single-digit bps
  annualized) not present in the futures contract itself
- **Roll differences:** commodity/rates ETFs that hold futures internally
  (e.g. `USO`, `UNG`) roll their own positions on a different schedule
  than the COT-tracked contract, which can diverge meaningfully during
  contango/backwardation periods — this is the largest caveat for energy
  proxies specifically

For reaction-DIRECTION testing (did the market move the "right" way
relative to news, not by how much precisely) these caveats are usually
acceptable, but the report always surfaces `proxy_used` so a downstream
consumer (e.g. a future `contrarian-setup-gate`) can weigh it rather than
treating proxy-derived and direct-futures-derived verdicts identically.

## `CL → BZUSD` Grade Caveat

`CL` (WTI crude) falls back to `BZUSD` (Brent crude) rather than an ETF —
both are crude oil futures but different grades with a real, sometimes
volatile spread (WTI-Brent). This is a closer proxy than an ETF (both are
direct futures-style feeds, not fund-wrapper products) but still not the
exact contract COT reports on. Documented here rather than silently
treated as equivalent to a direct `CLUSD` read.

## Implementation Notes

- Single constants dict: `{cot_symbol: [(price_symbol, kind, invert), ...]}`
  in `scripts/analyze_news_reaction.py`. `invert` is kept in the schema
  for future exotic/inverted pairs but is `False` for every v1 entry —
  every current market has a direct `XXXUSD`-style symbol, so no release
  gate depends on inversion handling working correctly yet.
- `--price-symbol` (CLI flag) skips the map entirely for a one-off
  override (e.g. testing a specific proxy, or a symbol not yet in the
  map).
- Status in the table above reflects a point-in-time probe (this key,
  2026-07-12). FMP's per-symbol tier gating can change; if a market that
  previously worked starts returning `no_price_source`, re-probe before
  assuming it's a bug in this skill.


---

## SKILL: news-sentiment

- Fuente: `staskh/trading_skills` → `.claude/skills/news-sentiment` (MIT)
- Cuándo usarla: Get recent news and sentiment for a stock. Use when user asks about news, headlines, sentiment, what's happening with a stock, or recent developments.
- Código: extraer `code/staskh_trading_skills.tar` y usar `.claude/skills/news-sentiment/` (news.py)

# News Sentiment

Fetch recent news from Yahoo Finance: yfinance's ticker news first, then Yahoo's per-ticker RSS feed when that comes back empty or fails.

## Instructions

> **Note:** If `uv` is not installed or `pyproject.toml` is not found, replace `uv run python` with `python` in all commands below.

```bash
uv run python scripts/news.py SYMBOL [--limit LIMIT]
```

## Arguments

- `SYMBOL` - Ticker symbol
- `--limit` - Number of articles (default: 10)

## Output

Returns JSON with:
- `articles` - Array of recent news with title, publisher, date (`YYYY-MM-DD HH:MM ET`), link, type
- `count` - Number of articles returned
- `source` - `"yfinance"` or `"yahoo-rss"`
- `note` - With `yahoo-rss`: items are tagged to the ticker, not necessarily about it, and arrive newest first. `publisher` is the link's host (often `finance.yahoo.com`), since the feed carries no publisher
- `message: "No news found"` - both sources answered with no articles
- `error` - no articles and at least one source failed; never read this as "no news"

Present key headlines and note any significant news that could impact the stock. Judge the sentiment from the headlines yourself. With `yahoo-rss`, skip market-wide stories that are not about the company when assessing its sentiment.

## Dependencies

- `yfinance`


## Timezone

All timestamps and time-based calculations must use the `America/New_York` timezone. All JSON output must include `generated_at` (NY time string) and `data_delay` fields.


---

## SKILL: pead-screener

- Fuente: `tradermonty/claude-trading-skills` → `skills/pead-screener` (MIT)
- Cuándo usarla: Screen post-earnings gap-up stocks for PEAD (Post-Earnings Announcement Drift) patterns. Analyzes weekly candle formation to detect red candle pullbacks and breakout signals. Supports two input modes - FMP earnings calendar (Mode A) or earnings-trade-analyzer JSON output (Mode B). Use when user asks about PEAD screening, post-earnings drift, earnings gap follow-through, red candle breakout patterns, or weekly earnings momentum setups.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/pead-screener/` (requirements.txt, _fmp_compat.py, __init__.py, breakout_calculator.py, liquidity_calculator.py, risk_reward_calculator.py, weekly_candle_calculator.py, fmp_client.py, report_generator.py, scorer.py, screen_pead.py)

# PEAD Screener - Post-Earnings Announcement Drift

Screen post-earnings gap-up stocks for PEAD (Post-Earnings Announcement Drift) patterns using weekly candle analysis to detect red candle pullbacks and breakout signals.

## When to Use

- User asks for PEAD screening or post-earnings drift analysis
- User wants to find earnings gap-up stocks with follow-through potential
- User requests red candle breakout patterns after earnings
- User asks for weekly earnings momentum setups
- User provides earnings-trade-analyzer JSON output for further screening

## Prerequisites

- FMP API key (set `FMP_API_KEY` environment variable or pass `--api-key`)
  ```bash
  export FMP_API_KEY=your_api_key_here
  ```
- Free tier (250 calls/day) is sufficient for default screening
- For Mode B: earnings-trade-analyzer JSON output file with schema_version "1.0"

## Workflow

### Step 1: Prepare and Execute Screening

Run the PEAD screener script in one of two modes:

**Mode A (FMP earnings calendar):**
```bash
# Default: last 14 days of earnings, 5-week monitoring window
python3 skills/pead-screener/scripts/screen_pead.py --output-dir reports/

# Custom parameters
python3 skills/pead-screener/scripts/screen_pead.py \
  --lookback-days 21 \
  --watch-weeks 6 \
  --min-gap 5.0 \
  --min-market-cap 1000000000 \
  --output-dir reports/
```

**Mode B (earnings-trade-analyzer JSON input):**
```bash
# From earnings-trade-analyzer output
python3 skills/pead-screener/scripts/screen_pead.py \
  --candidates-json reports/earnings_trade_analyzer_YYYY-MM-DD_HHMMSS.json \
  --min-grade B \
  --output-dir reports/
```

**Scheduled US-equity routine pitfall:** Prefer Mode B for pre-market / US-equity cron briefs after running `earnings-trade-analyzer`. Mode A can pull the global FMP earnings calendar, spend the API budget on non-US symbols, and return weak/non-actionable foreign listings before reaching the intended US watchlist. If Mode A is used anyway and the script reports budget trimming or non-US symbols, mark PEAD output as degraded and treat it as manual-review only rather than a clean candidate source.

### Step 2: Review Results

1. Read the generated JSON and Markdown reports
2. Load `references/pead_strategy.md` for PEAD theory and pattern context
3. Load `references/entry_exit_rules.md` for trade management rules

### Step 3: Present Analysis

For each candidate, present:
- Stage classification (MONITORING, SIGNAL_READY, BREAKOUT, EXPIRED)
- Weekly candle pattern details (red candle location, breakout status)
- Composite score and rating
- Trade setup: entry, stop-loss, target, risk/reward ratio
- Liquidity metrics (ADV20, average volume)

### Step 4: Provide Actionable Guidance

Based on stages and ratings:
- **BREAKOUT + Strong Setup (85+):** High-conviction PEAD trade, full position size
- **BREAKOUT + Good Setup (70-84):** Solid PEAD setup, standard position size
- **SIGNAL_READY:** Red candle formed, set alert for breakout above red candle high
- **MONITORING:** Post-earnings, no red candle yet, add to watchlist
- **EXPIRED:** Beyond monitoring window, remove from watchlist

## Output

- `pead_screener_YYYY-MM-DD_HHMMSS.json` - Structured results with stage classification
- `pead_screener_YYYY-MM-DD_HHMMSS.md` - Human-readable report grouped by stage

### Unknown earnings timing

FMP does not confirm a bmo/amc session for every earnings row; unconfirmed
rows carry `earnings_timing: "unknown"` in Mode A and the price gap
calculation assumes the AMC window as a fallback. The Mode A report shows
`timing_unknown_count` out of `timing_candidates_total` so this assumption
stays visible (Mode B reports `n/a` since timing is inherited from the input
JSON). `timing_candidates_total` is the post-budget-trim population that was
actually analyzed, not the raw earnings-calendar row count.

## Resources

- `references/pead_strategy.md` - PEAD theory and weekly candle approach
- `references/entry_exit_rules.md` - Entry, exit, and position sizing rules

### Referencia: references/entry_exit_rules.md

# PEAD Entry and Exit Rules

## Entry Rules

### Primary Entry: Red Candle Breakout
- **Trigger**: Weekly candle closes above the red candle's high on a green candle (close >= open)
- **Entry Price**: At or slightly above the red candle high
- **Confirmation**: Volume on the breakout week should be above the 4-week average
- **Timing**: Enter after the weekly close confirms the breakout (end of Friday session)

### Gap Minimum Requirement
- Minimum 3% gap-up on earnings day to qualify as a PEAD candidate
- Larger gaps (5%+) generally indicate stronger earnings surprises and more persistent drift
- Gaps below 3% may represent noise rather than genuine earnings surprise

### Pre-Entry Checklist
1. Earnings gap-up was at least 3%
2. A clear red weekly candle has formed (not a doji or inside bar)
3. Current weekly candle is green with close above red candle high
4. ADV20 (20-day average dollar volume) is at least $25M for adequate liquidity
5. Stock price is above $10 to avoid penny stock volatility
6. Within the 5-week monitoring window from earnings date

## Exit Rules

### Stop-Loss
- **Level**: Below the red candle's low
- **Type**: Hard stop (not mental stop)
- **Rationale**: If price drops below the red candle low, the pullback pattern has failed and institutional support has broken

### Profit Target
- **Primary Target**: 2R (2x the risk from entry to stop)
- **Calculation**: Target = Entry + (Entry - Stop) x 2.0
- **Example**: Entry at $100, Stop at $95 (5% risk) -> Target at $110 (10% gain, 2:1 R:R)

### Trailing Stop (Optional)
- After reaching 1R profit, move stop to breakeven
- After reaching 1.5R profit, trail stop at 1R below current price
- This locks in profits while allowing the PEAD drift to continue

### Time-Based Exit
- If the position has not reached the profit target within 4 weeks of entry, consider closing for a scratch or small profit/loss
- PEAD drift weakens significantly after 6-8 weeks post-earnings

## Position Sizing

### Risk-Based Sizing
- Risk no more than 1-2% of portfolio value per trade
- Position size = (Portfolio x Risk%) / (Entry - Stop)
- Example: $100K portfolio, 1% risk = $1,000 risk budget
  - Entry $100, Stop $95 = $5 risk per share
  - Position = $1,000 / $5 = 200 shares ($20,000 position)

### Liquidity-Based Constraints
- Never take a position larger than 1% of ADV20 (20-day average dollar volume)
- This ensures the position can be exited within a single day without significant market impact
- Example: ADV20 = $50M -> Max position = $500K

### Portfolio-Level Constraints
- Maximum 3-5 PEAD positions simultaneously
- Diversify across sectors to avoid correlated earnings risk
- Reduce position size if multiple PEAD trades are open

## Monitoring Window

### Duration
- Default: 5 weeks from earnings date
- The PEAD effect is strongest in weeks 1-3 and diminishes by weeks 4-5
- After 5 weeks without a breakout signal, remove from monitoring

### Weekly Review Process
1. Check if a red candle has formed (MONITORING -> SIGNAL_READY)
2. Check if breakout has occurred (SIGNAL_READY -> BREAKOUT)
3. Review volume on the breakout candle for confirmation
4. Calculate risk/reward based on current red candle levels
5. Verify liquidity is still adequate for entry

## Special Situations

### Multiple Red Candles
- If multiple red candles form, use the most recent one for entry/stop levels
- Multiple red candles may indicate weakening momentum; reduce position size

### Gap-and-Go (No Red Candle)
- Some stocks gap up and never pull back meaningfully
- These are not PEAD screener candidates (require red candle for defined risk)
- Consider alternative entry strategies if conviction is high

### Earnings in Consecutive Quarters
- A stock that gaps up on earnings for 2+ consecutive quarters shows persistent fundamental strength
- These are higher-conviction PEAD candidates when they form the red candle pattern

### Referencia: references/pead_strategy.md

# PEAD Strategy - Post-Earnings Announcement Drift

## What is PEAD

Post-Earnings Announcement Drift (PEAD) is one of the most robust anomalies in financial markets. Stocks that report positive earnings surprises (and gap up on the announcement) tend to continue drifting higher over the following weeks and months. This drift represents a systematic underreaction by the market to new earnings information.

## Academic Foundation

### Ball & Brown (1968)
The seminal paper by Ray Ball and Philip Brown first documented that stock prices continue to drift in the direction of earnings surprises for up to 60 days after the announcement. This was one of the earliest challenges to the Efficient Market Hypothesis.

### Bernard & Thomas (1989)
Victor Bernard and Jacob Thomas provided the most comprehensive analysis of PEAD. Their findings showed:
- Stocks in the highest earnings surprise decile outperformed the lowest decile by approximately 4% in the 60 days following the announcement
- The drift was strongest in the first 2-3 weeks post-announcement
- Smaller, less liquid stocks exhibited stronger drift
- The anomaly persisted across different time periods and market conditions

### Foster, Olsen & Shevlin (1984)
Confirmed that the drift is proportional to the magnitude of the earnings surprise, with larger surprises producing more persistent drift.

## Why It Works: Market Underreaction

PEAD exists because of several behavioral and structural factors:

1. **Anchoring Bias**: Analysts and investors anchor to prior earnings estimates and adjust insufficiently to new information
2. **Gradual Information Diffusion**: Not all market participants process earnings information simultaneously; institutional investors, retail traders, and algorithmic systems react on different timelines
3. **Confirmation Bias**: Investors who were bearish before earnings may dismiss a positive surprise as a one-time event
4. **Liquidity Constraints**: Large institutional investors cannot immediately establish full positions without moving the market
5. **Post-Earnings Volatility Risk**: Many traders avoid the immediate post-earnings period due to elevated implied volatility, creating a delayed response

## Weekly Candle Approach

This screener uses weekly candle analysis rather than daily candles for several reasons:

### Why Weekly Candles

1. **Noise Reduction**: Weekly candles filter out intraday and daily noise, revealing the true post-earnings trend
2. **Institutional Footprints**: Large institutions typically build positions over weeks, not days; weekly candles capture their accumulation patterns
3. **Clear Pattern Recognition**: Red and green weekly candles provide unambiguous signals about buyer/seller dominance
4. **Manageable Monitoring**: Weekly cadence allows systematic monitoring without requiring daily attention

### Red Candle Pullback Pattern

The core pattern this screener identifies:

1. **Earnings Gap-Up**: Stock gaps up 3%+ on earnings announcement (green weekly candle)
2. **Post-Earnings Drift**: Stock may continue higher for 1-2 weeks (green candles)
3. **Red Candle Pullback**: An orderly pullback produces a red weekly candle (close < open)
4. **Breakout Signal**: When the next green candle closes above the red candle's high, this signals the pullback is complete and the PEAD trend is resuming

This pattern works because:
- The red candle represents profit-taking by short-term traders
- The lower wick of the red candle reveals where institutional buyers are willing to support the stock
- The breakout above the red candle high confirms that demand exceeds supply

## Stage-Based Monitoring System

The screener classifies each stock into one of four stages:

### MONITORING
- Stock has gapped up on earnings within the watch window
- No red weekly candle has formed yet
- Action: Add to watchlist, check weekly for red candle formation

### SIGNAL_READY
- A red weekly candle has formed after the earnings gap-up
- No breakout above the red candle high yet
- Action: Set price alert at red candle high; prepare order for breakout

### BREAKOUT
- Current weekly candle is green AND price is above the red candle high
- This is the actionable trade signal
- Action: Enter position with stop below red candle low

### EXPIRED
- More than 5 weeks (configurable) have passed since earnings
- The PEAD effect diminishes significantly after this window
- Action: Remove from watchlist

## Historical Performance Characteristics

Based on academic research and practical observations:

- **Win Rate**: PEAD strategies historically show 55-65% win rates
- **Average Winner vs. Loser**: Winners tend to be 1.5-2.5x larger than losers
- **Optimal Holding Period**: 2-6 weeks post-entry for the core PEAD drift
- **Sector Sensitivity**: Technology and growth sectors tend to show stronger PEAD effects
- **Market Cap Effect**: Mid-cap stocks ($2B-$20B) often show the strongest drift due to analyst coverage gaps
- **Earnings Quality**: Stocks with revenue beats in addition to EPS beats show stronger drift

## Key Differences from Other Momentum Strategies

Unlike pure price momentum strategies, PEAD is fundamentally driven:
- It requires a specific catalyst (earnings announcement)
- The thesis is grounded in information underreaction, not just trend following
- It has a defined entry window (post-earnings) and monitoring period
- Risk management is anchored to the red candle pattern, not arbitrary stop levels


---

## SKILL: prediction-market-live-ops

- Fuente: `agiprolabs/claude-trading-skills` → `skills/prediction-market-live-ops` (MIT)
- Cuándo usarla: Use when building, backtesting, operating, or scaling automated trading on prediction markets (Kalshi or similar) — evidence-gated methodology, live-execution safety rails, and falsification protocols distilled from a real live-money campaign

# Prediction-Market Trading Doctrine

Hard-won operational knowledge from a live Kalshi campaign (Aug–Sep 2026:
crypto/commodity maker ladders, regime tilts, tennis dust vacuum — all
falsified honestly, infrastructure open-sourced). Reference implementation: https://github.com/agiprolabs/kalshi-stack.
Complements `prediction-market-strategy` (edge selection/sizing) — this skill
covers the OPERATIONAL side: validating, executing, and killing strategies
against a live venue without losing more than the lesson costs.

## The prime directive

Every strategy decision is evidence-gated: backtest → paper → live micro-probe
→ ratchet. Each stage has a PRE-DECLARED kill condition with correctly
calibrated probability math, written down BEFORE the data arrives. When a
threshold turns out miscalibrated, correct it openly and re-declare — never
silently move a goalpost in either direction.

## Backtest hygiene (each rule was violated once, expensively)

- **Print-replay EV of passive-fill strategies is an UPPER BOUND, never an
  estimate.** The prints a resting order actually captures are an
  adversely-selected sample of the tape (sweeps deep enough to reach your
  queue skew toward true collapses). A tennis dust book that measured +125%/$
  on prints went 0-for-78 live (P<2%). Only fill-conditioned live outcomes
  validate a maker strategy.
- **Time-series joins use the last bar ending ≤ the decision instant.**
  A candle containing the instant is look-ahead and will fabricate
  covariates that vanish out-of-sample.
- **Taker backtests need print-confirmed executability**, not quoted-ask
  edges — stale quotes create phantom fills.
- **Any bucketed-PnL review includes a top-N-share column.** Lottery-payoff
  books concentrate EV; a "pattern" that is two elephant rounds is noise.
  Same rule when a holdout "wins": check concentration before believing it.
- **Early settlements are selection-biased toward losers** (collapses end
  fast; comebacks are long matches/rounds). Never read a verdict off the
  fast-settling prefix.
- **Static tilts that flip sign between tape halves are regime bets, not
  edges.** A conditioning scheme must beat baseline on BOTH halves and on
  each individual day; pre-register the rules, no per-day fitting.
- Mirror/complement markets are the SAME bet — deduplicate before computing
  independence-based probabilities.

## Live execution rules (the incident ledger)

- **Smoke-test every live order path with a real 1-lot round trip** (place,
  verify resting, cancel, verify gone) before any strategy trades through
  it. Paper cannot exercise venue routing parameters. Cost: $0.01.
- **Cancels must be truthful**: distinguish cancelled / already-gone
  (filled!) / failed. A 404 is not a cancel — it means wrong routing shard
  or a fill-race. Swallowed cancel failures + re-anchor loops = runaway
  position stacking (cost us $84 in one evening).
- **Route the exchange shard (`exchange_index`) consistently on EVERY call**
  — placement, reads, cancels, collateral. Collateral must be pre-positioned
  on the shard before orders.
- **Measure rate limits empirically with dust orders** (burst ladder +
  sustained test). Advertised budgets can be 10× off effective per-order
  cost. Pace bursts to the measured rate with retry-requeue on 429.
- **post_only for any maker strategy** — an "aggressive maker" price on a
  market trading inside your band silently becomes a taker fill of a
  different (unvalidated) trade. Tag and cohort maker vs taker fills
  separately in all realized-EV accounting.
- **Rails, always**: halt-file checked before every order batch (cancel-all
  on appearance), independent scheduler-driven drawdown breaker with
  deposit-jump detection, per-order and per-market size caps with anomaly
  ledger events, equity floor stand-down. The breaker baseline is set at
  session start per the operator's stated loss tolerance.
- **Queue priority is the product** in penny/maker books. Synchronized-open
  venues: NTP + fire at boundary+0 with a retry probe (measure the venue's
  open-transition latency). Event-driven venues: push-based discovery
  (lifecycle WebSocket channels) beats polling; a fresh market's book is
  empty, so first-to-rest owns the level for its lifetime.
- **Restart daemons at activity boundaries**; mid-round restarts orphan
  in-memory state (untracked orders, missed settlements).
- **Geofencing is real**: order-origin IP matters, categories differ
  (sports/elections vs financials), and enforcement can change overnight.
  Datacenter location is part of your compliance posture.

## Scaling doctrine

- **House-money ratchet**: double size only when realized profit at the
  current step covers the next step's incremental risk AND round-count and
  EV-continuity gates pass. Drop back a step on trailing degradation.
- **Measure the capacity curve** (EV/$ by per-print cap) before believing
  any scale projection; then the binding constraint is capture rate ×
  measured pool, and capture rate is only measurable live.
- **Fill quality is the untested link at every new size** — the paper/live
  EV-per-$ ratio at each step gates the next.

## Experiment operations

- Cohort every fill (maker/taker, band, source) at write time — post-hoc
  attribution is what lets a bug contaminate a verdict.
- Ship one variable at a time; changing size and placement logic in the same
  window destroys attribution.
- Run A/B variants in paper against a frozen baseline (small-footprint
  variant, shared rounds, EV/premium-$ as the scale-free judge).
- Log everything to append-only ledgers; reconcile realized PnL to the
  venue's own fills/settlements, never to internal marks.
- Post results (wins AND falsifications) to the operator's channel; write a
  decision record with evidence and reversal conditions for every ship,
  retire, and kill.


---

## SKILL: report-stock

- Fuente: `staskh/trading_skills` → `.claude/skills/report-stock` (MIT)
- Cuándo usarla: Stock ticker symbol(s) - single or space-separated list (e.g., AAPL or "AAPL MSFT GOOGL")
- Código: extraer `code/staskh_trading_skills.tar` y usar `.claude/skills/report-stock/` (report.py)

# Stock Analysis Report Generator

Generates professional reports with comprehensive stock analysis including trend analysis, PMCC viability, and fundamental metrics. Supports both PDF and markdown output formats.

## Instructions

### Step 1: Gather Data

Run the report script for each symbol:

```bash
uv run python scripts/report.py SYMBOL
```

The script returns detailed JSON with:
- `recommendation` - Overall recommendation with strengths/risks
- `company` - Company info (name, sector, industry, market cap)
- `trend_analysis` - Bullish scanner results (score, RSI, MACD, ADX, SMAs)
- `pmcc_analysis` - PMCC viability (score, LEAPS/short details, metrics)
- `fundamentals` - Valuation, profitability, dividend, balance sheet, earnings history
- `piotroski` - F-Score breakdown with all 9 criteria
- `spread_strategies` - Option spread analysis (vertical spreads, straddle, strangle, iron condor)

### Step 2: Generate Report

**Step 2a — Write markdown**

Read `templates/markdown-template.md` for formatting instructions. Generate a markdown report from the JSON data and save to `sandbox/` as:
```
sandbox/{SYMBOL}_Analysis_Report_{YYYY-MM-DD}_{HHmm}.md
```

**Step 2b — Convert to PDF (if requested)**

Invoke the `markdown-to-pdf` skill on the markdown file just created:
```bash
uv run python .claude/skills/markdown-to-pdf/scripts/markdown_to_pdf.py sandbox/{SYMBOL}_Analysis_Report_{YYYY-MM-DD}_{HHmm}.md
```
The PDF is written alongside the markdown file with the same basename.

### Step 3: Report Results

After generating the report, tell the user:
1. The recommendation (BUY/HOLD/AVOID)
2. Key strengths and risks
3. The report file path

## Example

```bash
# Single symbol
uv run python scripts/report.py AAPL

# Multiple symbols - run separately
uv run python scripts/report.py AAPL
uv run python scripts/report.py MSFT
```

## Report Contents

All sections defined in `templates/markdown-template.md`:

1. **Header** — symbol, company name, generated timestamp
2. **Recommendation** — BUY/HOLD/AVOID with strengths and risks
3. **Company Overview** — sector, industry, market cap, beta
4. **Trend Analysis** — bullish score, RSI, MACD, ADX, SMA distances, earnings date, signals list
5. **Fundamental Analysis** — valuation (P/E, P/B, EPS), profitability (margins, ROE, ROA, growth), dividend & balance sheet, earnings history (up to 8 quarters)
6. **Piotroski F-Score** — all 9 criteria with PASS/FAIL
7. **Insider Trading** — net sentiment, buy/sell counts, recent transactions (omitted if no data)
8. **PMCC Viability** — score, IV, LEAPS/short leg details, trade metrics (yield, capital required)
9. **Option Spread Strategies** — bull call, bear put, straddle, strangle, iron condor
10. **Investment Summary** — strengths and risk factors
11. **Disclaimer footer**

## Dependencies

This skill aggregates data from:
- `scanner-bullish` for trend analysis
- `scanner-pmcc` for PMCC viability
- `fundamentals` for financial data and Piotroski score


## Timezone

All timestamps and time-based calculations must use the `America/New_York` timezone. All JSON output must include `generated_at` (NY time string) and `data_delay` fields.

### Referencia: templates/markdown-template.md

# Stock Analysis Report - Markdown Template

Format the JSON data into a markdown report saved to `sandbox/`.

**Filename**: `{SYMBOL}_Analysis_Report_{YYYY-MM-DD}_{HHmm}.md`

## Report Structure

### 1. Header

```markdown
# {SYMBOL} Stock Analysis Report
**{company.name}** - Comprehensive Analysis
Generated: {generated}
```

### 2. Recommendation Box

```markdown
## Recommendation: {recommendation.recommendation}

**Strengths:**
- {strength 1}
- {strength 2}
...

**Risks:**
- {risk 1}
- {risk 2}
...
```

Use `recommendation.recommendation_level` to label: "positive" = BUY, "neutral" = HOLD, "negative" = AVOID.

### 3. Company Overview

| Metric | Value |
|--------|-------|
| Company | `company.name` |
| Sector | `company.sector` |
| Industry | `company.industry` |
| Market Cap | Format as `$X.XB` or `$X.XM` |
| Enterprise Value | Format as `$X.XB` or `$X.XM` |
| Beta | 2 decimals |

### 4. Trend Analysis

| Indicator | Value | Signal |
|-----------|-------|--------|
| Bullish Score | `X.XX / 8` | Strong(≥6)/Moderate(≥4)/Neutral(≥2)/Bearish(<2) |
| Price | `$X.XX` | - |
| 3-Month Return | `±X.X%` | Bullish/Bearish |
| vs SMA20 | `±X.X%` | Above/Below |
| vs SMA50 | `±X.X%` | Above/Below |
| RSI | `X.X` | Overbought(>70)/Oversold(<30)/Bullish(50-70)/Neutral |
| MACD | `X.XX vs Signal X.XX` | Bullish/Bearish |
| ADX | `X.X` | Strong(≥40)/Moderate(25-40)/Weak(<25) Trend |
| Next Earnings | `YYYY-MM-DD` | `BMO`/`AMC` |

**Signals:** List `trend_analysis.signals` as bullet points.

### 5. Fundamental Analysis

#### Valuation

| Metric | Value | Assessment |
|--------|-------|------------|
| Trailing P/E | `X.Xx` | Attractive(<15)/Reasonable(15-25)/Premium(>25) |
| Forward P/E | `X.Xx` | Same |
| Price/Book | `X.Xx` | - |
| EPS (TTM) | `$X.XX` | - |
| Forward EPS | `$X.XX` | - |

#### Profitability

| Metric | Value | Assessment |
|--------|-------|------------|
| Profit Margin | `X.X%` | Excellent(>20%)/Good(10-20%)/Low(<10%) |
| Operating Margin | `X.X%` | Same |
| ROE | `X.X%` | Same |
| ROA | `X.X%` | - |
| Revenue Growth | `±X.X%` | Growing/Declining |
| Earnings Growth | `±X.X%` | Growing/Declining |

#### Dividend & Balance Sheet

| Metric | Value | Assessment |
|--------|-------|------------|
| Dividend Yield | `X.XX%` or "None" | High(>5%)/Attractive(2-5%)/Low(<2%)/None |
| Dividend Rate | `$X.XX/share` | - |
| Payout Ratio | `X%` | At limit(>80%)/Moderate(50-80%)/Conservative(<50%) |
| Debt/Equity | `X.X%` | High(>100%)/Moderate(50-100%)/Low(<50%) |
| Current Ratio | `X.XXx` | Good(>1.5)/Adequate(1-1.5)/Low(<1) |

#### Earnings History

| Date | Estimate | Actual | Surprise |
|------|----------|--------|----------|
| YYYY-MM-DD | $X.XX | $X.XX | ±X.X% |

Up to 8 quarters.

### 6. Piotroski F-Score

**Score: X/9** ({piotroski.interpretation})

| Criteria | Result | Details |
|----------|--------|---------|
| 1. Positive Net Income | PASS/FAIL | Value |
| 2. Positive ROA | PASS/FAIL | Value |
| 3. Positive Operating CF | PASS/FAIL | Value |
| 4. CF > Net Income | PASS/FAIL | CF: X, NI: Y |
| 5. Lower Long-Term Debt | PASS/FAIL | Recent: X, Prev: Y |
| 6. Higher Current Ratio | PASS/FAIL | Recent: X, Prev: Y |
| 7. No Share Dilution | PASS/FAIL | Recent: X, Prev: Y |
| 8. Higher Gross Margin | PASS/FAIL | Recent: X, Prev: Y |
| 9. Higher Asset Turnover | PASS/FAIL | Recent: X, Prev: Y |

### 7. Insider Trading Activity

> Only include this section if `insider_trading.recent_transactions` is non-empty.

**Net Sentiment: {insider_trading.summary.net_sentiment}**  
(map: `net_buying` → "🟢 Net Buying", `net_selling` → "🔴 Net Selling", `neutral` → "⚪ Neutral")

| Metric | Value |
|--------|-------|
| Buys (90 days) | `buy_count` transactions, `$buy_value` total |
| Sells (90 days) | `sell_count` transactions, `$sell_value` total |
| Net Activity | `±$net_value` |

#### Recent Transactions

| Date | Insider | Role | Transaction | Shares | Price | Value | Own |
|------|---------|------|-------------|--------|-------|-------|-----|
| YYYY-MM-DD | Name | Title | Sale/Purchase/Exercise | X,XXX | $XX.XX | $XXX,XXX | D/I |

Up to 10 most recent. Omit `price` and `value` columns if all values are N/A.  
`Ownership` D = Direct, I = Indirect.

### 8. PMCC Viability

| Metric | Value | Assessment |
|--------|-------|------------|
| PMCC Score | `X / {max_pmcc_score}` | Excellent(≥9)/Good(7-8)/Acceptable(5-6)/Poor(<5) |
| Implied Volatility | `X.X%` | Ideal(25-50%)/Acceptable(20-60%)/High(>60%)/Low(<20%) |
| LEAPS Expiry | `YYYY-MM-DD (X days)` | - |
| LEAPS Strike | `$X` | - |
| LEAPS Delta | `0.XXX` | On Target(0.75-0.85)/Off Target |
| LEAPS Bid/Ask | `$X.XX / $X.XX` | - |
| LEAPS Spread | `X.X%` | Good(<10%)/Acceptable(10-20%)/Wide(>20%) |
| Short Expiry | `YYYY-MM-DD (X days)` | - |
| Short Strike | `$X` | - |
| Short Delta | `0.XXX` | On Target(0.15-0.25)/Off Target |
| Short Bid/Ask | `$X.XX / $X.XX` | - |
| Short Spread | `X.X%` | Good(<10%)/Acceptable(10-20%)/Wide(>20%) |

#### Trade Metrics

| Metric | Value |
|--------|-------|
| Net Debit | `$X,XXX.XX` |
| Short Yield (per cycle) | `X.XX%` |
| Estimated Annual Yield | `X.X%` |
| Max Profit (if assigned) | `$X,XXX.XX` |
| ROI at Max Profit | `X.X%` |
| Capital Required | `$X,XXX.XX` |

### 9. Option Spread Strategies

**Expiry:** {spread_strategies.expiry} ({spread_strategies.dte} days)

#### Strategy Summary

| Strategy | Direction | Max Profit | Max Loss | Risk/Reward | Breakeven |
|----------|-----------|------------|----------|-------------|-----------|
| Bull Call Spread | Bullish | $XXX | $XXX | X.XX | $XXX |
| Bear Put Spread | Bearish | $XXX | $XXX | X.XX | $XXX |
| Long Straddle | Neutral | Unlimited | $XXX | - | $XXX / $XXX |
| Long Strangle | Neutral | Unlimited | $XXX | - | $XXX / $XXX |
| Iron Condor | Neutral | $XXX | $XXX | X.XX | $XXX - $XXX |

#### Strategy Details

For each strategy, show legs, cost, breakeven, max profit/loss.

### 10. Investment Summary

**Strengths:**
- (from recommendation.strengths)

**Risk Factors:**
- (from recommendation.risks)

### Footer

```markdown
---
*This analysis is for informational purposes only and does not constitute financial advice.
Options trading involves significant risk of loss. Past performance is not indicative of future results.*
```

## Formatting Rules

- Percentages: Always show sign for changes (`+5.2%`, `-3.1%`)
- Currency: `$123.45`, `$1.2B`, `$45.6M`
- Ratios: 1 decimal for P/E, 2 decimals for delta/beta
- Scores: `X / max` format
- Missing data: "N/A" or "-"


---

## SKILL: sector-overview

- Fuente: `anthropics/financial-services` → `plugins/agent-plugins/market-researcher/skills/sector-overview` (Apache-2.0)
- Cuándo usarla: Create comprehensive industry and sector landscape reports covering market dynamics, competitive positioning, key players, and thematic trends. Use for client requests, sector initiations, thematic research pieces, or internal knowledge building. Triggers on "sector overview", "industry report", "market landscape", "sector analysis", "industry deep dive", or "thematic research".

# Sector Overview

## Workflow

### Step 1: Define Scope

- **Sector / subsector**: What industry and how narrowly defined?
- **Purpose**: Client report, internal research, pitch material, idea generation
- **Depth**: High-level overview (5-10 pages) or deep dive (20-30 pages)
- **Angle**: Neutral landscape vs. thematic thesis (e.g., "AI infrastructure buildout")
- **Universe**: Public companies only, or include private?

### Step 2: Market Overview

**Market Size & Growth**
- Total addressable market (TAM) with source
- Historical growth rate (5-year CAGR)
- Forecast growth rate and key assumptions
- Market segmentation (by product, geography, end market, customer type)

**Industry Structure**
- Fragmented vs. consolidated — top 5 market share
- Value chain map — where does value accrue?
- Business model types (subscription, transaction, licensing, services)
- Barriers to entry (capital, regulatory, technical, network effects)

**Key Trends & Drivers**
- Secular tailwinds (3-5 major trends)
- Headwinds and risks
- Technology disruption vectors
- Regulatory developments
- M&A activity and consolidation trends

### Step 3: Competitive Landscape

**Company Profiles** (for top 5-10 players):

| Company | Revenue | Growth | EBITDA Margin | Market Share | Key Differentiator |
|---------|---------|--------|--------------|-------------|-------------------|
| | | | | | |

For each company, brief profile:
- Business description (2-3 sentences)
- Strategic positioning and moat
- Recent developments (earnings, M&A, product launches)
- Valuation snapshot (P/E, EV/EBITDA, EV/Revenue)

**Competitive Dynamics**
- How do companies compete? (price, product, service, distribution)
- Who is gaining/losing share and why?
- Disruption risk from new entrants or adjacent players

### Step 4: Valuation Context

- Sector trading multiples (current and historical range)
- Premium/discount drivers (growth, margins, market position)
- Recent M&A transaction multiples
- How does the sector compare to the broader market?

### Step 5: Investment Implications

- Where are the best risk/reward opportunities?
- What thematic bets can be expressed through this sector?
- Key debates in the sector (bull vs. bear arguments)
- Catalysts that could change the sector narrative

### Step 6: Output

- Word document or PowerPoint with:
  - Market overview and sizing
  - Competitive landscape map
  - Company comparison table
  - Valuation summary
  - Key charts: market growth, share trends, valuation history
- Excel appendix with detailed company data

## Important Notes

- Source all market size data — cite the research firm or methodology
- Distinguish between TAM hype and realistic addressable market
- Sector overviews age fast — note the date and flag data that may be stale
- Charts are essential — market size waterfall, competitive positioning matrix, valuation scatter plot
- If for a client, tailor the "so what" to their specific situation (M&A target identification, competitive positioning, market entry)


---

## SKILL: sentiment-analysis

- Fuente: `agiprolabs/claude-trading-skills` → `skills/sentiment-analysis` (MIT)
- Cuándo usarla: Market sentiment extraction from social media, news, and on-chain data including mention velocity, fear and greed indices, and influencer tracking
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/sentiment-analysis/` (keyword_sentiment.py, sentiment_scanner.py)

# Sentiment Analysis

Extract and quantify market sentiment from social media, news feeds, and on-chain
data to identify crowd positioning and potential contrarian opportunities.

## When to Use This Skill

- Gauge crowd sentiment before entering or exiting a position
- Detect euphoria/panic extremes that precede reversals
- Monitor social mention velocity for early trend detection
- Track influencer activity around specific tokens
- Build composite sentiment scores for systematic strategies

## Core Concepts

### Sentiment Data Sources

| Source | Data Type | Access |
|--------|-----------|--------|
| Twitter/X | Post text, engagement, follower counts | API (paid tiers) |
| Reddit | Subreddit posts, comments, upvotes | Reddit API |
| Telegram | Channel messages, member counts | Bot API or scraping |
| Discord | Server activity, message volume | Bot integration |
| News | Headlines, article text | NewsAPI, RSS feeds |
| CoinGecko | Community stats, developer activity | Free API |
| Alternative.me | Fear & Greed Index | Free API |
| On-chain | Funding rates, exchange flows | Exchange APIs |

See `references/data_sources.md` for complete API details, rate limits, and access
patterns for each source.

### Sentiment Metrics

**Mention Velocity** — Rate of token mentions over time:

```python
mention_velocity = mentions_last_hour / baseline_hourly_mentions
# > 3.0 = trending, > 10.0 = viral
```

**Sentiment Polarity** — Positive vs negative tone:

```python
polarity = (positive_count - negative_count) / total_count
# Range: -1.0 (all negative) to +1.0 (all positive)
```

**Fear & Greed Index** — Composite market mood (0-100):

| Range | Label | Typical Signal |
|-------|-------|----------------|
| 0-24 | Extreme Fear | Potential accumulation zone |
| 25-44 | Fear | Below-average sentiment |
| 45-55 | Neutral | No strong directional bias |
| 56-74 | Greed | Above-average sentiment |
| 75-100 | Extreme Greed | Potential distribution zone |

**Social Volume** — Total mentions across platforms:

```python
social_volume_z = (current_volume - mean_30d) / std_30d
# z > 2.0 suggests unusual activity
```

### On-Chain Sentiment Proxies

On-chain data reveals what participants are doing, not just saying:

**Funding Rates** — Perpetual futures cost of carry:

```python
# Positive funding = longs pay shorts (bullish crowding)
# Negative funding = shorts pay longs (bearish crowding)
funding_sentiment = -1.0 * normalize(funding_rate, -0.1, 0.1)
# Inverted: high positive funding is contrarian bearish
```

**Long/Short Ratio** — Proportion of leveraged positions:

```python
ls_ratio = long_accounts / short_accounts
# > 2.0 = crowded long, < 0.5 = crowded short
ls_sentiment = -1.0 * normalize(ls_ratio, 0.5, 2.0)
```

**Exchange Flows** — Net deposits/withdrawals:

```python
net_flow = exchange_inflows - exchange_outflows
# Positive net flow (deposits) = bearish (selling pressure)
# Negative net flow (withdrawals) = bullish (accumulation)
flow_sentiment = -1.0 * normalize(net_flow, -threshold, threshold)
```

### Keyword-Based Sentiment Scoring

A simple, LLM-free approach using curated word lists:

```python
BULLISH_KEYWORDS = {
    "moon": 2, "bullish": 2, "pump": 1, "breakout": 2,
    "buy": 1, "long": 1, "accumulate": 2, "undervalued": 2,
    "gem": 1, "rocket": 1, "ath": 1, "rally": 2,
}
BEARISH_KEYWORDS = {
    "dump": 2, "bearish": 2, "crash": 2, "scam": 3,
    "rug": 3, "sell": 1, "short": 1, "overvalued": 2,
    "dead": 2, "rekt": 1, "ponzi": 3, "exit": 1,
}

def score_text(text: str) -> float:
    """Score text from -1.0 (bearish) to +1.0 (bullish)."""
    words = text.lower().split()
    bull_score = sum(BULLISH_KEYWORDS.get(w, 0) for w in words)
    bear_score = sum(BEARISH_KEYWORDS.get(w, 0) for w in words)
    total = bull_score + bear_score
    if total == 0:
        return 0.0
    return (bull_score - bear_score) / total
```

See `references/scoring_methods.md` for the full methodology, temporal decay
weighting, and composite score construction.

### Composite Sentiment Score

Combine multiple signals into a single score:

```python
def composite_sentiment(
    social_polarity: float,    # -1.0 to +1.0
    mention_velocity: float,   # 0 to inf
    fear_greed: int,           # 0 to 100
    funding_rate: float,       # -0.1 to +0.1
    weights: dict | None = None,
) -> float:
    """Compute weighted composite sentiment score (-100 to +100).

    Args:
        social_polarity: Average polarity of social mentions.
        mention_velocity: Current velocity vs baseline.
        fear_greed: Fear & Greed index reading.
        funding_rate: Current perpetual funding rate.
        weights: Optional custom weights.

    Returns:
        Composite score from -100 (extreme fear) to +100 (extreme greed).
    """
    w = weights or {
        "social": 0.30,
        "velocity": 0.15,
        "fear_greed": 0.30,
        "funding": 0.25,
    }
    # Normalize each component to -1.0 to +1.0
    s_social = social_polarity
    s_velocity = min(mention_velocity / 10.0, 1.0)  # Cap at 10x
    s_fg = (fear_greed - 50) / 50.0  # 0-100 -> -1 to +1
    s_funding = -10.0 * funding_rate  # Contrarian: high funding = bearish
    s_funding = max(-1.0, min(1.0, s_funding))

    raw = (
        w["social"] * s_social
        + w["velocity"] * s_velocity
        + w["fear_greed"] * s_fg
        + w["funding"] * s_funding
    )
    return round(raw * 100, 1)
```

### Contrarian Signals

Extreme sentiment readings often precede reversals:

| Condition | Interpretation |
|-----------|----------------|
| Composite < -70 | Extreme fear — historically a buying zone |
| Composite > +70 | Extreme greed — historically a selling zone |
| Velocity > 10x + polarity > 0.6 | Euphoric spike — fade potential |
| Velocity > 10x + polarity < -0.6 | Panic spike — bounce potential |
| Funding > 0.05% + LS ratio > 2.0 | Crowded long — liquidation risk |
| Funding < -0.05% + LS ratio < 0.5 | Crowded short — squeeze risk |

**Key principle**: Sentiment is most useful at extremes. Neutral readings
(composite between -30 and +30) have low predictive value.

### Influencer Tracking

Monitor high-follower accounts for early signal detection:

```python
def influencer_signal(
    posts: list[dict],
    min_followers: int = 50_000,
    lookback_hours: int = 24,
) -> dict:
    """Detect influencer activity around a token.

    Args:
        posts: List of posts with 'followers', 'timestamp', 'sentiment'.
        min_followers: Minimum follower count to qualify as influencer.
        lookback_hours: Time window in hours.

    Returns:
        Dict with influencer_count, avg_sentiment, total_reach.
    """
    cutoff = time.time() - (lookback_hours * 3600)
    relevant = [
        p for p in posts
        if p["followers"] >= min_followers and p["timestamp"] >= cutoff
    ]
    if not relevant:
        return {"influencer_count": 0, "avg_sentiment": 0.0, "total_reach": 0}
    return {
        "influencer_count": len(relevant),
        "avg_sentiment": sum(p["sentiment"] for p in relevant) / len(relevant),
        "total_reach": sum(p["followers"] for p in relevant),
    }
```

## Integration With Other Skills

| Skill | Integration Point |
|-------|------------------|
| `position-sizing` | Reduce size in extreme greed, increase in extreme fear |
| `risk-management` | Tighten stops when sentiment diverges from price |
| `regime-detection` | Sentiment confirms or contradicts regime classification |
| `feature-engineering` | Sentiment metrics as ML features |
| `signal-classification` | Sentiment as input to signal scoring models |
| `whale-tracking` | Combine whale activity with social sentiment |
| `token-holder-analysis` | Holder growth/decline as sentiment proxy |

## Practical Workflow

```
1. Fetch fear/greed index          → Market-wide mood
2. Pull social data for token      → Token-specific sentiment
3. Score text with keyword method  → Polarity scores
4. Compute mention velocity        → Trending detection
5. Check on-chain proxies          → Funding, flows
6. Calculate composite score       → Single decision input
7. Flag contrarian signals         → Extreme readings
8. Integrate with position sizing  → Adjust allocation
```

## Limitations and Warnings

- **Sentiment is noisy.** Individual readings are unreliable — use trends and extremes.
- **Social data is gameable.** Bot activity can inflate mention counts.
- **Keyword scoring is crude.** It misses sarcasm, context, and nuance.
- **Lag exists.** By the time sentiment is measurable, price may have moved.
- **Not financial advice.** Sentiment data is for informational and analytical purposes only.
- **API access varies.** Twitter/X API pricing has changed frequently. Budget accordingly.
- **Survivorship bias.** Tokens that go to zero stop being discussed — absence of mentions is also a signal.

## Files

### References
- `references/data_sources.md` — API details, rate limits, and access patterns for all sentiment data sources
- `references/scoring_methods.md` — Keyword lists, composite scoring methodology, temporal decay, contrarian logic

### Scripts
- `scripts/sentiment_scanner.py` — Fetches live sentiment data from free APIs, computes composite scores, flags contrarian signals
- `scripts/keyword_sentiment.py` — Standalone keyword-based text sentiment analyzer with synthetic demo data

### Referencia: references/data_sources.md

# Sentiment Data Sources

Complete reference for social, aggregator, and on-chain sentiment data APIs.

## Social Media APIs

### Twitter/X API

- **Base URL**: `https://api.twitter.com/2/`
- **Auth**: OAuth 2.0 Bearer Token
- **Key Endpoints**:
  - `GET /tweets/search/recent` — Search tweets from last 7 days
  - `GET /tweets/counts/recent` — Tweet volume over time
  - `GET /users/:id/tweets` — User timeline
- **Rate Limits**:
  - Free tier: 1 app, read-only, 1,500 tweets/month
  - Basic ($100/mo): 10,000 tweets/month, 2 apps
  - Pro ($5,000/mo): 1M tweets/month, full archive search
- **Search Query Examples**:
  ```
  $SOL lang:en -is:retweet           # SOL mentions, English, no RTs
  (solana OR $SOL) (pump OR moon)    # Bullish keywords
  ```
- **Response Fields**: `id`, `text`, `created_at`, `public_metrics.like_count`,
  `public_metrics.retweet_count`, `author_id`
- **Notes**: Pricing changed significantly in 2023. Free tier is very limited.
  Consider third-party aggregators for cost-effective access.

### Reddit API

- **Base URL**: `https://oauth.reddit.com/`
- **Auth**: OAuth2 with client ID and secret
- **Key Endpoints**:
  - `GET /r/{subreddit}/search` — Search within subreddit
  - `GET /r/{subreddit}/hot` — Hot posts
  - `GET /r/{subreddit}/new` — New posts
  - `GET /r/{subreddit}/comments/{article}` — Post comments
- **Rate Limits**: 100 requests/minute per OAuth client
- **Relevant Subreddits**:
  - `r/cryptocurrency` — General crypto discussion
  - `r/solana` — Solana ecosystem
  - `r/defi` — DeFi protocols
  - `r/CryptoMoonShots` — Speculative tokens (high noise)
- **Response Fields**: `title`, `selftext`, `score`, `num_comments`,
  `created_utc`, `author`, `upvote_ratio`
- **Notes**: Free and accessible. High signal in r/cryptocurrency daily threads.

### Telegram

- **Bot API URL**: `https://api.telegram.org/bot{token}/`
- **Key Methods**:
  - `getUpdates` — Receive messages from channels the bot is in
  - `getChatMemberCount` — Channel subscriber count
- **Rate Limits**: 30 messages/second, 20 messages/minute to same chat
- **Access Pattern**: Create a bot via @BotFather, add to target channels.
  Cannot search across public channels without scraping.
- **Monitoring Approach**:
  ```python
  # Poll for new messages in monitored channels
  updates = httpx.get(f"{BOT_URL}/getUpdates?offset={last_id}").json()
  for update in updates["result"]:
      text = update.get("channel_post", {}).get("text", "")
      # Score text for sentiment
  ```
- **Notes**: Many crypto alpha groups use Telegram. Signal quality varies.

### Discord

- **Bot Gateway**: WebSocket-based, requires bot token
- **REST API**: `https://discord.com/api/v10/`
- **Key Endpoints**:
  - `GET /channels/{id}/messages` — Channel message history
  - `GET /guilds/{id}` — Server info including member count
- **Rate Limits**: 50 requests/second globally
- **Notes**: Requires bot to be invited to servers. Good for project-specific
  sentiment (e.g., monitoring a token's official Discord).

## Aggregator APIs

### Alternative.me Fear & Greed Index

- **Endpoint**: `GET https://api.alternative.me/fng/`
- **Auth**: None required (free)
- **Parameters**:
  - `limit` — Number of days (default 1, max ~4000)
  - `date_format` — `us`, `cn`, `kr`, or `world`
- **Rate Limits**: Undocumented, ~100 requests/minute observed
- **Response**:
  ```json
  {
    "data": [
      {
        "value": "25",
        "value_classification": "Extreme Fear",
        "timestamp": "1709856000"
      }
    ]
  }
  ```
- **Composition**: Volatility (25%), market momentum/volume (25%),
  social media (15%), surveys (15%), Bitcoin dominance (10%), trends (10%)
- **Notes**: Bitcoin-focused but correlates with altcoin sentiment. Updated daily.

### LunarCrush

- **Base URL**: `https://lunarcrush.com/api4/public/`
- **Auth**: API key via `Authorization: Bearer {key}`
- **Key Endpoints**:
  - `GET /coins/{symbol}/time-series/v2` — Social metrics over time
  - `GET /coins/list/v2` — All tracked coins with social stats
  - `GET /coins/{symbol}/meta/v1` — Coin metadata and current social stats
- **Rate Limits**: Free tier 100 calls/day, Pro tier 10,000 calls/day
- **Key Metrics**: `galaxy_score` (0-100 composite), `alt_rank`,
  `social_volume`, `social_score`, `social_dominance`
- **Notes**: Best aggregated social data source. Free tier is usable for
  periodic checks.

### Santiment

- **Base URL**: `https://api.santiment.net/graphql`
- **Auth**: API key via header
- **Key Queries** (GraphQL):
  ```graphql
  {
    getMetric(metric: "social_volume_total") {
      timeseriesData(slug: "solana", from: "2025-01-01", to: "2025-01-31") {
        datetime
        value
      }
    }
  }
  ```
- **Key Metrics**: `social_volume_total`, `social_dominance`,
  `sentiment_positive_total`, `sentiment_negative_total`,
  `weighted_social_sentiment`
- **Rate Limits**: Free tier 100 API calls/month, paid tiers higher
- **Notes**: Highest quality sentiment data but expensive for full access.

## On-Chain Sentiment Proxies

### Binance Funding Rates

- **Endpoint**: `GET https://fapi.binance.com/fapi/v1/fundingRate`
- **Auth**: None required for public endpoints
- **Parameters**: `symbol` (e.g., `SOLUSDT`), `limit` (default 100, max 1000)
- **Rate Limits**: 2400 request weight/minute
- **Response**:
  ```json
  [
    {
      "symbol": "SOLUSDT",
      "fundingRate": "0.00010000",
      "fundingTime": 1709856000000
    }
  ]
  ```
- **Interpretation**:
  - `> 0.01%` — Longs paying premium, bullish crowding
  - `< -0.01%` — Shorts paying premium, bearish crowding
  - `> 0.05%` — Extreme: high liquidation risk for longs
  - `< -0.05%` — Extreme: short squeeze risk
- **Notes**: Funding settles every 8 hours. Use `fundingTime` for alignment.

### Binance Long/Short Ratio

- **Endpoint**: `GET https://fapi.binance.com/futures/data/globalLongShortAccountRatio`
- **Auth**: None required
- **Parameters**: `symbol`, `period` (5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d)
- **Response**:
  ```json
  [
    {
      "symbol": "SOLUSDT",
      "longShortRatio": "1.5000",
      "longAccount": "0.6000",
      "shortAccount": "0.4000",
      "timestamp": 1709856000000
    }
  ]
  ```
- **Notes**: Ratio > 2.0 or < 0.5 indicates crowded positioning.

### CoinGecko Community Data

- **Endpoint**: `GET https://api.coingecko.com/api/v3/coins/{id}`
- **Auth**: None for free tier, API key for Pro
- **Rate Limits**: 10-30 calls/minute (free), 500/minute (Pro)
- **Community Fields** (in response):
  ```json
  {
    "community_data": {
      "twitter_followers": 1234567,
      "reddit_subscribers": 456789,
      "reddit_accounts_active_48h": 12345,
      "telegram_channel_user_count": 67890
    },
    "developer_data": {
      "forks": 1234,
      "stars": 5678,
      "commit_count_4_weeks": 200
    },
    "sentiment_votes_up_percentage": 75.5,
    "sentiment_votes_down_percentage": 24.5
  }
  ```
- **Notes**: Free and comprehensive. Community data updates every few hours.
  The `sentiment_votes_up_percentage` field is a direct crowd sentiment gauge.

### CryptoQuant / Glassnode (Exchange Flows)

- **CryptoQuant API**: `https://api.cryptoquant.com/v1/`
  - `GET /btc/exchange-flows/netflow` — Net exchange flow
  - Auth: API key, free tier available with limited data
- **Glassnode API**: `https://api.glassnode.com/v1/metrics/`
  - `GET /transactions/transfers_volume_exchanges_net` — Net transfer volume
  - Auth: API key, free tier with 24h delay
- **Interpretation**:
  - Positive net flow (inflows > outflows) = coins moving to exchanges = sell pressure
  - Negative net flow (outflows > inflows) = coins leaving exchanges = accumulation
- **Notes**: Bitcoin and Ethereum focused. Limited Solana coverage on free tiers.

## Free-Tier Strategy

For cost-effective sentiment monitoring, use these free sources:

1. **Alternative.me Fear & Greed** — Daily market-wide mood (no auth)
2. **CoinGecko community data** — Token-specific social stats (no auth, rate limited)
3. **Binance funding rates** — On-chain positioning (no auth)
4. **Binance long/short ratio** — Crowd positioning (no auth)
5. **Reddit API** — Social text data (free OAuth)

This combination provides market-wide sentiment, token-specific social metrics,
and on-chain positioning data at zero cost.

### Referencia: references/scoring_methods.md

# Sentiment Scoring Methods

Comprehensive reference for keyword-based scoring, composite indices, temporal
decay, and contrarian signal detection.

## Keyword-Based Sentiment

### Approach

Score text by matching tokens against curated positive/negative word lists
weighted by intensity. No ML model required — runs anywhere with zero
dependencies.

### Crypto-Specific Word Lists

**Bullish Keywords** (word: weight):

```
moon: 2, bullish: 2, pump: 1, breakout: 2, buy: 1, long: 1,
accumulate: 2, undervalued: 2, gem: 1, rocket: 1, ath: 1, rally: 2,
surge: 2, soar: 2, lambo: 1, diamond: 1, hodl: 1, dip: 1 (as in "buy the dip"),
alpha: 1, gainz: 1, moonshot: 2, parabolic: 2, reversal: 1, recovery: 1,
bottom: 1, support: 1, accumulation: 2, institutional: 1, adoption: 2
```

**Bearish Keywords** (word: weight):

```
dump: 2, bearish: 2, crash: 2, scam: 3, rug: 3, sell: 1, short: 1,
overvalued: 2, dead: 2, rekt: 1, ponzi: 3, exit: 1, fraud: 3,
bubble: 2, collapse: 2, liquidation: 2, capitulation: 2, resistance: 1,
distribution: 1, top: 1, overbought: 1, bagholding: 2, worthless: 3,
hack: 3, exploit: 3, insolvent: 3, bankrupt: 3, warning: 2
```

### Scoring Formula

```python
def keyword_score(text: str, bullish: dict, bearish: dict) -> float:
    """Score text from -1.0 (bearish) to +1.0 (bullish).

    Formula: (bull_sum - bear_sum) / (bull_sum + bear_sum)
    Returns 0.0 if no keywords matched.
    """
    words = text.lower().split()
    bull = sum(bullish.get(w, 0) for w in words)
    bear = sum(bearish.get(w, 0) for w in words)
    total = bull + bear
    if total == 0:
        return 0.0
    return (bull - bear) / total
```

### Limitations

- Misses sarcasm: "Great, another rug pull" scores partially bullish
- Context-blind: "not bullish" scores as bullish
- Language-specific: English only without translation
- Gameable: Bots can flood channels with keyword-loaded posts

### Mitigation Strategies

- Require minimum text length (> 10 words) to reduce noise
- Weight by engagement: higher-engagement posts count more
- Apply author reputation scoring (account age, follower count)
- Use bigrams for negation detection: "not bullish" -> bearish

## Mention Velocity

### Definition

Rate of token mentions compared to a historical baseline:

```
velocity = mentions_current_period / baseline_mentions_per_period
```

### Baseline Computation

Use a 30-day rolling average as baseline:

```python
def compute_velocity(
    current_mentions: int,
    period_hours: float,
    daily_baseline: float,
) -> float:
    """Compute mention velocity as multiple of baseline.

    Args:
        current_mentions: Mentions observed in the current period.
        period_hours: Length of current observation period in hours.
        daily_baseline: 30-day average daily mentions.

    Returns:
        Velocity as a multiple of baseline (1.0 = normal).
    """
    hourly_baseline = daily_baseline / 24.0
    if hourly_baseline <= 0:
        return 0.0
    hourly_current = current_mentions / max(period_hours, 0.1)
    return hourly_current / hourly_baseline
```

### Interpretation

| Velocity | Meaning |
|----------|---------|
| 0.0-0.5 | Below normal — low interest |
| 0.5-1.5 | Normal range |
| 1.5-3.0 | Elevated — growing interest |
| 3.0-10.0 | Trending — significant event |
| > 10.0 | Viral — major event or coordinated activity |

### Combined Velocity + Polarity Signals

| Velocity | Polarity | Signal |
|----------|----------|--------|
| > 5x | > +0.5 | Euphoria — potential top |
| > 5x | < -0.5 | Panic — potential bottom |
| > 5x | Near 0 | Controversy — uncertain |
| < 0.3x | Any | Forgotten — check if project is dead |

## Fear & Greed Index

### Alternative.me Composition

The crypto Fear & Greed Index uses these components:

| Component | Weight | Source |
|-----------|--------|--------|
| Volatility | 25% | Current vs 30/90-day avg |
| Market Momentum/Volume | 25% | Current vs 30/90-day avg |
| Social Media | 15% | Twitter/Reddit mentions + engagement |
| Surveys | 15% | Community polls (when available) |
| Bitcoin Dominance | 10% | BTC market cap share |
| Google Trends | 10% | Search volume for crypto terms |

### Building a Custom Fear/Greed Score

For token-specific sentiment, build a custom index:

```python
def custom_fear_greed(
    price_vs_sma30: float,    # price / SMA(30) - 1.0
    volume_vs_avg: float,     # volume / avg_volume(30)
    social_polarity: float,   # -1.0 to +1.0
    funding_rate: float,      # perpetual funding rate
    holder_growth_pct: float, # 7d holder count change %
) -> int:
    """Compute custom fear/greed index (0-100).

    Each component maps to 0-100, then weighted average.
    """
    # Price momentum: -20% below SMA = 0, +20% above = 100
    c_price = min(100, max(0, (price_vs_sma30 + 0.2) / 0.4 * 100))

    # Volume: 0.5x avg = 0, 2.0x avg = 100
    c_volume = min(100, max(0, (volume_vs_avg - 0.5) / 1.5 * 100))

    # Social: -1.0 = 0, +1.0 = 100
    c_social = (social_polarity + 1.0) / 2.0 * 100

    # Funding: -0.05% = 0 (fear), +0.05% = 100 (greed)
    c_funding = min(100, max(0, (funding_rate + 0.0005) / 0.001 * 100))

    # Holder growth: -5% = 0, +5% = 100
    c_holders = min(100, max(0, (holder_growth_pct + 5) / 10 * 100))

    score = int(
        0.25 * c_price
        + 0.20 * c_volume
        + 0.25 * c_social
        + 0.15 * c_funding
        + 0.15 * c_holders
    )
    return min(100, max(0, score))
```

## Composite Sentiment Score

### Construction

Combine all available signals into a single -100 to +100 score:

```
composite = w1 * social_polarity_norm
          + w2 * velocity_norm
          + w3 * fear_greed_norm
          + w4 * funding_norm
```

### Default Weights

| Component | Weight | Rationale |
|-----------|--------|-----------|
| Social polarity | 0.30 | Direct sentiment measure |
| Fear/greed index | 0.30 | Broad market context |
| Funding rate | 0.25 | Reveals leveraged positioning |
| Mention velocity | 0.15 | Activity level indicator |

### Normalization

All components must be normalized to the -1.0 to +1.0 range before weighting:

- Social polarity: already -1.0 to +1.0
- Velocity: `min(velocity / 10.0, 1.0)` (caps at 10x baseline)
- Fear/greed: `(value - 50) / 50` (0-100 -> -1 to +1)
- Funding: `-10.0 * rate`, clamped to [-1, 1] (contrarian: inverted)

## Temporal Decay

Recent data points carry more weight than older ones:

```python
def temporal_weight(age_hours: float, half_life_hours: float = 6.0) -> float:
    """Exponential decay weight based on data age.

    Args:
        age_hours: How old the data point is in hours.
        half_life_hours: Hours until weight drops to 50%.

    Returns:
        Weight from 0.0 to 1.0.
    """
    import math
    return math.exp(-0.693 * age_hours / half_life_hours)
```

| Age (hours) | Weight (6h half-life) |
|-------------|----------------------|
| 0 | 1.000 |
| 3 | 0.707 |
| 6 | 0.500 |
| 12 | 0.250 |
| 24 | 0.063 |
| 48 | 0.004 |

## Contrarian Signal Detection

### Rules

1. **Extreme Fear Buy Signal**: Composite < -70 AND velocity > 5x
   - Crowd is panicking — historically precedes bounces
2. **Extreme Greed Sell Signal**: Composite > +70 AND velocity > 5x
   - Crowd is euphoric — historically precedes corrections
3. **Funding Divergence**: Funding > 0.05% but price declining
   - Longs trapped — liquidation cascade risk
4. **Silent Accumulation**: Velocity < 0.3x but holder count increasing
   - Smart money accumulating while retail is disinterested

### Confidence Levels

| Signals Aligned | Confidence |
|----------------|------------|
| 1 | Low — single indicator, could be noise |
| 2 | Moderate — worth monitoring |
| 3+ | High — strong contrarian setup |

### Historical Context

Extreme Fear & Greed readings (< 10 or > 90) have historically occurred
during 5-10% of trading days. The signal is valuable precisely because
it is rare. Do not lower thresholds to generate more signals.


---

## SKILL: slippage-modeling

- Fuente: `agiprolabs/claude-trading-skills` → `skills/slippage-modeling` (MIT)
- Cuándo usarla: Execution cost estimation, slippage curve modeling, and optimal trade sizing based on AMM liquidity depth
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/slippage-modeling/` (execution_cost.py, slippage_curve.py)

# Slippage Modeling

Estimate execution costs, model slippage curves from AMM mechanics and empirical quotes, and determine optimal trade sizes that keep costs within acceptable thresholds.

## What Is Slippage?

Slippage is the difference between the **expected price** at the time you decide to trade and the **actual execution price** you receive. On decentralized exchanges, slippage is deterministic and measurable — unlike CEX slippage, which depends on hidden order book dynamics.

**Example**: You expect to buy a token at 0.001 SOL. Your trade executes at 0.00105 SOL. That 5% difference is slippage — it directly reduces your profit and increases your break-even threshold.

## Sources of Slippage

### 1. AMM Price Impact (Primary Source)

Automated market makers use bonding curves that move price as liquidity is consumed. On a constant-product AMM (`x * y = k`):

```
price_impact = Δx / (x + Δx)
```

Where `x` is the reserve of the input token and `Δx` is your trade size. A 1 SOL trade against a pool with 100 SOL reserves produces ~1% price impact. Against 10 SOL reserves, it produces ~10%.

See `references/slippage_math.md` for full derivations and CLMM adjustments.

### 2. DEX Fees

Every swap incurs a fee taken from the trade:

| DEX      | Fee       | Notes                          |
|----------|-----------|--------------------------------|
| Raydium  | 0.25%     | Standard AMM pools             |
| Orca     | 0.30%     | Whirlpool concentrated pools   |
| Meteora  | 0.1–2.0%  | Dynamic fees based on volatility|
| PumpFun  | 1.0%      | Bonding curve phase            |

### 3. Priority Fees

Solana validators prioritize transactions with higher compute unit prices. During congestion or for time-sensitive trades:
- Normal: 0.0001 SOL (negligible)
- Competitive: 0.001–0.01 SOL
- High congestion: 0.01–0.1 SOL

### 4. MEV (Sandwich Attacks)

Searchers detect pending swaps and sandwich them — buying before your trade (raising the price) and selling after (capturing the difference). MEV cost depends on:
- Trade size (larger = more attractive target)
- Token liquidity (thin pools = easier to manipulate)
- Slippage tolerance setting (higher tolerance = more extractable)

Typical MEV cost: 0–200 bps on vulnerable trades.

### 5. Stale Quotes

Between receiving a quote and landing the transaction on-chain (0.4–2 seconds on Solana), the price may move. Volatile tokens can shift 50–500 bps in that window.

## Constant-Product Slippage Formula

For a pool with reserves `(x, y)` and invariant `k = x * y`:

**Buying tokens with SOL** (input Δx SOL):
```
tokens_received = y * Δx / (x + Δx)
effective_price = Δx / tokens_received = (x + Δx) / y
spot_price      = x / y
price_impact    = effective_price / spot_price - 1 = Δx / (x + Δx)
```

**Selling tokens for SOL** (input Δy tokens):
```
sol_received   = x * Δy / (y + Δy)
effective_price = sol_received / Δy = x / (y + Δy)
spot_price      = x / y
price_impact    = 1 - effective_price / spot_price = Δy / (y + Δy)
```

**Key insight**: Slippage scales with `trade_size / (reserves + trade_size)`. This is approximately linear for small trades and accelerates sharply as trade size approaches reserve size.

### Quick Reference Table

| Trade / Reserve Ratio | Approximate Slippage |
|----------------------|---------------------|
| 0.1%                 | 0.1% (1 bp)         |
| 1%                   | 1.0% (100 bps)      |
| 5%                   | 4.8% (476 bps)      |
| 10%                  | 9.1% (909 bps)      |
| 25%                  | 20% (2000 bps)      |
| 50%                  | 33% (3333 bps)      |

## CLMM Slippage

Concentrated Liquidity Market Makers (Orca Whirlpools, Meteora DLMM) concentrate liquidity in specific price ranges:

- Within the active range: slippage is **lower** than constant-product by a concentration factor
- Crossing tick boundaries: additional slippage as the next tick's liquidity may be sparse
- Approximation: `clmm_slippage ≈ cp_slippage / concentration_factor`

Typical concentration factors: 5–50x for well-managed positions.

## Empirical Slippage Measurement

Theoretical formulas assume single-pool routing. In practice, Jupiter aggregates across multiple pools and routes. **Empirical measurement** is more accurate:

1. Query Jupiter `/quote` at multiple trade sizes (0.01, 0.1, 1, 5, 10, 50 SOL)
2. Record output amount and effective price at each size
3. Compute slippage in bps relative to smallest trade (proxy for spot)
4. Fit a power-law model: `slippage_bps = a * trade_size^b`

This captures real routing behavior, multi-pool splitting, and available liquidity.

See `scripts/slippage_curve.py` for the full implementation.

## Total Execution Cost Model

```
total_cost_bps = price_impact_bps + fee_bps + priority_fee_bps + mev_risk_bps
total_cost_sol = trade_size_sol * total_cost_bps / 10_000
```

See `references/cost_model.md` for component breakdowns and worked examples.

### Break-Even Analysis

For a roundtrip (buy + sell):
```
roundtrip_cost_bps = entry_impact + exit_impact + 2 * fee_bps + 2 * priority_bps + mev_bps
```

The token must move **more than** `roundtrip_cost_bps` in your favor to be profitable. For a token with 200 bps entry slippage, 200 bps exit slippage, and 50 bps fees:
```
roundtrip = 200 + 200 + 50 = 450 bps = 4.5%
```

You need at least a 4.5% price move just to break even.

See `scripts/execution_cost.py` for automated cost estimation.

## Optimal Trade Sizing

### Maximum Size for Slippage Threshold

Given a slippage curve `s(q) = a * q^b`, solve for max trade size:
```
q_max = (threshold_bps / a) ^ (1/b)
```

### Multi-Tranche Execution

For large orders, splitting reduces total slippage because each tranche faces a partially-reset order book (on CLMMs) or allows arbitrageurs to rebalance between tranches:

```
n_tranches = ceil(total_size / q_max)
tranche_size = total_size / n_tranches
wait_between = 2-10 seconds (allow arb rebalancing)
```

### TWAP Strategy

Time-Weighted Average Price execution:
- Divide total order into equal-sized tranches
- Execute one tranche per interval (e.g., every 10 seconds)
- Total slippage is significantly lower than single execution
- Tradeoff: price may move against you during execution window

## Slippage by Token Category

| Category      | Typical Pool TVL | Slippage for 1 SOL | Slippage for 10 SOL |
|---------------|-----------------|---------------------|----------------------|
| Blue chip     | >$10M           | <5 bps              | <20 bps              |
| Mid-cap       | $100K–$10M      | 10–50 bps           | 50–500 bps           |
| Small-cap     | $10K–$100K      | 50–200 bps          | 500–2000 bps         |
| Micro/PumpFun | <$10K           | 200–2000 bps        | Often impossible      |

## Integration Points

- **liquidity-analysis**: Get pool TVL and reserve data to feed slippage estimates
- **position-sizing**: Use max trade size from slippage curve as a position size constraint
- **jupiter-api**: Fetch real quotes for empirical slippage measurement
- **risk-management**: Include execution costs in risk/reward calculations
- **dex-pool-analysis**: Understand pool mechanics that drive slippage

## Files

### References
| File | Description |
|------|-------------|
| `references/slippage_math.md` | AMM slippage derivations, CLMM adjustments, multi-pool routing math |
| `references/cost_model.md` | Total execution cost components, break-even analysis, cost comparison tables |

### Scripts
| File | Description |
|------|-------------|
| `scripts/slippage_curve.py` | Build empirical slippage curves from Jupiter quotes, fit power-law model |
| `scripts/execution_cost.py` | Estimate total execution cost and break-even for a specific trade |

### Referencia: references/cost_model.md

# Total Execution Cost Model

## Component Breakdown

Every trade on Solana DEXes incurs multiple cost components. Understanding each one is critical for accurate break-even analysis and position sizing.

### 1. Price Impact (AMM Slippage)

The largest and most variable cost. Depends on trade size relative to pool liquidity.

| Pool TVL   | 0.1 SOL | 1 SOL   | 10 SOL   | 50 SOL    |
|-----------|---------|---------|----------|-----------|
| $1M+      | <1 bps  | 1-5 bps | 5-50 bps | 50-200 bps|
| $100K     | 1-5 bps | 10-50 bps| 100-500 bps| 500+ bps |
| $10K      | 5-50 bps| 50-500 bps| Often unfeasible | — |
| <$5K      | 50+ bps | 500+ bps | —        | —         |

### 2. DEX Swap Fees

Fees are taken from the input amount before the swap executes.

| Protocol     | Fee Rate | Basis Points | Notes                        |
|-------------|----------|-------------|------------------------------|
| Raydium AMM | 0.25%    | 25 bps      | Standard constant-product     |
| Raydium CLMM| 0.01-1%  | 1-100 bps   | Varies by pool fee tier       |
| Orca Whirlpool| 0.01-1%| 1-100 bps   | Fee tiers: 1, 4, 8, 64, 128 bps|
| Meteora DLMM| 0.1-2%   | 10-200 bps  | Dynamic fees increase with volatility|
| PumpFun     | 1.0%     | 100 bps     | Bonding curve phase           |

Jupiter typically selects the lowest-fee route automatically.

### 3. Solana Base Transaction Fee

- Base fee: 5000 lamports = 0.000005 SOL
- Cost in bps: For a 1 SOL trade, this is 0.0005 bps — completely negligible
- This is the only guaranteed fixed cost

### 4. Priority Fee (Compute Unit Price)

Required for timely inclusion during congestion or competitive trading.

| Scenario           | Priority Fee    | For 1 SOL Trade |
|-------------------|----------------|-----------------|
| Low congestion    | 0.0001 SOL     | 1 bps           |
| Normal            | 0.001 SOL      | 10 bps          |
| High congestion   | 0.005-0.01 SOL | 50-100 bps      |
| Extreme/sniping   | 0.05-0.5 SOL   | 500-5000 bps    |

Priority fees are fixed per transaction, so they have **higher bps impact on smaller trades**.

### 5. MEV Cost (Sandwich Attacks)

Estimated additional cost from MEV extraction. Not guaranteed to occur, but should be budgeted for high-value trades.

**Risk factors**:
- Trade size > 5 SOL on thin pools: high risk
- Slippage tolerance > 5%: high risk
- Popular meme tokens during launch: very high risk
- Blue chip tokens with deep liquidity: low risk

**Estimated MEV cost**:

| Risk Level | Estimated Cost | When                              |
|-----------|---------------|-----------------------------------|
| Negligible | 0 bps         | Small trades, deep liquidity       |
| Low        | 5-20 bps      | Medium trades, good liquidity      |
| Medium     | 20-100 bps    | Large trades on mid-cap tokens     |
| High       | 100-500 bps   | Large trades on thin/hyped tokens  |

**Mitigation**: Use Jupiter's exact-out mode, set tight slippage tolerance, use Jito bundles for MEV protection.

## Total Cost Formula

```
total_bps = impact_bps + fee_bps + priority_bps + mev_bps
total_sol = trade_size_sol * total_bps / 10_000
```

### Example: Buy 5 SOL of a Mid-Cap Token ($500K TVL Pool)

| Component     | Estimate   |
|--------------|-----------|
| Price impact  | 80 bps    |
| DEX fee       | 25 bps    |
| Priority fee  | 10 bps    |
| MEV risk      | 20 bps    |
| **Total**     | **135 bps** |
| **Cost in SOL** | **0.0675 SOL** |

## Break-Even Analysis

### Roundtrip Cost

A complete trade (entry + exit) incurs costs twice:

```
roundtrip_bps = entry_impact + exit_impact + 2 * fee_bps + 2 * priority_bps + mev_bps
```

Note: Exit slippage may differ from entry because:
- Pool liquidity may have changed
- Selling into a pool you bought from has the same reserves minus your tokens
- Market conditions and priority fees may differ

### Conservative Roundtrip Estimates

| Token Category | Entry Cost | Exit Cost | Roundtrip | Min Move to Profit |
|---------------|-----------|----------|-----------|-------------------|
| Blue chip      | 30 bps    | 30 bps   | 60 bps    | 0.6%              |
| Mid-cap        | 135 bps   | 150 bps  | 285 bps   | 2.85%             |
| Small-cap      | 300 bps   | 400 bps  | 700 bps   | 7.0%              |
| Micro/PumpFun  | 800 bps   | 1200 bps | 2000 bps  | 20%               |

### Required Return Calculation

```
required_return = roundtrip_cost_bps / (10_000 - roundtrip_cost_bps)
```

For 285 bps roundtrip: `285 / 9715 = 2.93%` actual price move needed.

### Risk-Adjusted Analysis

Factor in win rate to determine if execution costs make a strategy viable:

```
expected_pnl = win_rate * avg_win - (1 - win_rate) * avg_loss - roundtrip_cost
```

If roundtrip cost is 285 bps per trade and you make 100 trades per month:
- Monthly execution cost: 28,500 bps equivalent
- With 1 SOL average position: 2.85 SOL/month in execution costs alone

## When Costs Make a Trade Unprofitable

Rules of thumb for whether execution costs are prohibitive:

1. **Roundtrip cost > 5% of trade value**: Only trade if expecting 10%+ move
2. **Slippage > expected daily range**: The token cannot reasonably move enough to cover costs in your timeframe
3. **Priority fee > 10% of expected profit**: Reduce urgency or wait for lower congestion
4. **MEV risk is "high"**: Use MEV protection (Jito bundles) or reduce trade size

## Cost Optimization Strategies

### Reduce Price Impact
- Split large orders into tranches (see SKILL.md on multi-tranche execution)
- Trade during high-liquidity hours (US market hours for Solana)
- Use limit orders when available (Jupiter DCA or limit order program)

### Reduce Fees
- Jupiter automatically routes to lowest-fee pools
- Raydium CLMM 1 bps fee tier pools exist for major pairs
- Avoid PumpFun bonding curve when Raydium pool exists

### Reduce Priority Fees
- Avoid trading during network congestion spikes
- Use dynamic priority fee estimation (query recent slot leaders)
- Accept slightly longer confirmation times for non-urgent trades

### Reduce MEV Exposure
- Set slippage tolerance as tight as possible (1-3% for liquid tokens)
- Use Jito bundles for MEV-protected execution
- Trade smaller sizes (not worth sandwiching)
- Avoid mempool-visible transactions where possible

### Referencia: references/slippage_math.md

# Slippage Math — AMM Derivations & Multi-Pool Routing

## Constant-Product AMM (x * y = k)

### Setup

A pool has reserves `(x, y)` where:
- `x` = SOL reserves
- `y` = token reserves
- `k = x * y` = constant invariant (ignoring fees)

Spot price of token in SOL: `P_spot = x / y`

### Buy: Swapping Δx SOL for Tokens

After depositing Δx SOL, new SOL reserves = `x + Δx`. To maintain invariant:

```
(x + Δx) * (y - Δy) = k = x * y
y - Δy = x * y / (x + Δx)
Δy = y - x * y / (x + Δx)
Δy = y * Δx / (x + Δx)
```

**Effective price** (SOL per token):
```
P_eff = Δx / Δy = Δx * (x + Δx) / (y * Δx) = (x + Δx) / y
```

**Price impact** (fractional):
```
impact = P_eff / P_spot - 1
       = [(x + Δx) / y] / [x / y] - 1
       = (x + Δx) / x - 1
       = Δx / x
```

Wait — this gives `Δx / x`, but the commonly cited formula is `Δx / (x + Δx)`. The difference is reference frame:

- `Δx / x` = price impact relative to pre-trade spot price
- `Δx / (x + Δx)` = fraction of output lost vs. a hypothetical zero-impact trade

**Output loss fraction** (more practically useful):
```
ideal_output = y * Δx / x        (at spot price, no impact)
actual_output = y * Δx / (x + Δx)
loss_fraction = 1 - actual/ideal = Δx / (x + Δx)
```

This `Δx / (x + Δx)` is what traders experience as "slippage."

### Worked Example

Pool: 1000 SOL / 10,000,000 tokens (spot price = 0.0001 SOL/token)

**Trade: Buy with 10 SOL**
```
Δy = 10,000,000 * 10 / (1000 + 10) = 99,009.90 tokens
Ideal output = 10,000,000 * 10 / 1000 = 100,000 tokens
Slippage = 1 - 99,009.90 / 100,000 = 0.99% ≈ 99 bps
Check: Δx/(x+Δx) = 10/1010 = 0.99% ✓
```

**Trade: Buy with 100 SOL**
```
Δy = 10,000,000 * 100 / (1000 + 100) = 909,090.9 tokens
Ideal output = 1,000,000 tokens
Slippage = 1 - 909,090.9 / 1,000,000 = 9.09% ≈ 909 bps
Check: 100/1100 = 9.09% ✓
```

### Sell: Swapping Δy Tokens for SOL

Depositing Δy tokens, new token reserves = `y + Δy`:

```
(x - Δx_out) * (y + Δy) = k = x * y
Δx_out = x * Δy / (y + Δy)
```

**Output loss fraction**:
```
ideal_sol = x * Δy / y
actual_sol = x * Δy / (y + Δy)
loss_fraction = Δy / (y + Δy)
```

### Slippage Asymmetry

Buying and selling the same dollar amount produce **different** slippage because they draw from different reserves. If SOL reserves are 1000 and token reserves are 10M:

- Buying 10 SOL worth: slippage = 10/1010 = 0.99%
- Selling 100,000 tokens (worth ~10 SOL): slippage = 100,000/10,100,000 = 0.99%

The slippage is symmetric in value terms for constant-product. But if reserves are imbalanced in value (price moved from initial), the side with less value has higher slippage per dollar.

## Fee-Adjusted Slippage

Most AMMs take fees **before** the swap. For a fee rate `f` (e.g., 0.0025 for 0.25%):

```
effective_input = Δx * (1 - f)
Δy = y * effective_input / (x + effective_input)
total_slippage = 1 - Δy / ideal_output
             = 1 - (1-f) * x / (x + Δx*(1-f))
```

For small trades, total slippage ≈ `f + Δx/x` (fee plus impact).

## Concentrated Liquidity (CLMM)

### How Concentration Affects Slippage

In CLMMs (Orca Whirlpools, Meteora DLMM), liquidity providers specify a price range `[P_low, P_high]`. Within this range, the effective reserves are amplified:

```
effective_x = real_x * concentration_factor
concentration_factor ≈ 1 / (1 - sqrt(P_low/P_high))
```

For a position spanning ±5% around current price:
```
concentration ≈ 1 / (1 - sqrt(0.95/1.05)) ≈ 1 / (1 - 0.951) ≈ 20x
```

**Slippage within active range**:
```
clmm_slippage ≈ cp_slippage / concentration_factor
```

A trade that would cause 100 bps slippage on constant-product only causes ~5 bps on a 20x concentrated position.

### Tick Boundary Crossings

When a trade is large enough to exhaust liquidity in the current tick range, it crosses into the next tick where:
- Liquidity may be different (higher, lower, or zero)
- Each crossing adds a discrete jump in slippage

This makes CLMM slippage **non-smooth** — it can jump sharply at tick boundaries. Empirical measurement (via Jupiter quotes) captures this better than theoretical models.

## Multi-Pool Routing

### Optimal Split Across Pools

When Jupiter routes across `n` pools with reserves `(x_1, y_1), ..., (x_n, y_n)`, the optimal split minimizes total slippage.

For constant-product pools, the optimal fraction to route through pool `i`:

```
fraction_i = sqrt(x_i * y_i) / sum_j(sqrt(x_j * y_j))
           = sqrt(L_i) / sum_j(sqrt(L_j))
```

Where `L_i = x_i * y_i` is the pool's liquidity (k-value).

### Routing Through Intermediaries

Jupiter may route SOL → USDC → TOKEN if the SOL/TOKEN direct pool is thin. Total slippage compounds:

```
total_slippage ≈ slippage_hop1 + slippage_hop2
```

(Approximate for small slippage values; exact: `1 - (1-s1)*(1-s2)`)

### Why Empirical > Theoretical

Theoretical models assume:
- Known pool reserves (may be stale)
- Single pool type (ignoring CLMM/AMM mix)
- No intermediary routing

Jupiter's actual quotes incorporate all of this. Querying at multiple sizes gives the true executable slippage curve.

## Power-Law Slippage Model

Empirically, slippage curves follow a power law:

```
slippage_bps = a * trade_size_sol ^ b
```

Where:
- `a` = slippage coefficient (higher = less liquid)
- `b` = slippage exponent (typically 0.8–1.2; 1.0 = perfectly linear)

**Fitting**: Use log-linear regression on `(log(size), log(slippage))` pairs from Jupiter quotes.

**Inverting** (find max size for a slippage limit):
```
max_size = (limit_bps / a) ^ (1/b)
```

This model works well for interpolation within the fitted range. Extrapolation beyond the largest tested size is unreliable.


---

## SKILL: statistics-fundamentals

- Fuente: `JoelLewis/finance_skills` → `plugins/core/skills/statistics-fundamentals` (MIT)
- Cuándo usarla: Apply statistical methods to financial data including descriptive statistics, covariance estimation, regression, hypothesis testing, and resampling. Use when the user asks about return distributions, correlation between assets, building a covariance matrix, running a CAPM regression, testing whether alpha is significant, checking if returns are normal, or estimating confidence intervals. Also trigger when users mention 'volatility', 'how correlated are these', 'fat tails', 'skewness', 'R-squared', 'beta of a fund', 'bootstrap a Sharpe ratio', 'shrinkage estimator', 'Ledoit-Wolf', or ask why their optimizer produces unstable weights.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/core/skills/statistics-fundamentals/` (statistics_fundamentals.py)

# Statistics Fundamentals

## Core Concepts

### Conventions and Decision Rules

### Sample variance: use n-1
When estimating variance or standard deviation from a sample of returns, divide by `n - 1` (Bessel's correction), not `n`. Dividing by `n` systematically underestimates dispersion. Standard deviation of returns is "volatility"; annualize with `sigma_annual = sigma_period * sqrt(periods_per_year)` (e.g., `* sqrt(12)` for monthly, `* sqrt(252)` for daily).

### Normality testing: Jarque-Bera and its limits
`JB = (n/6) * (skew^2 + excess_kurtosis^2 / 4)`, distributed chi-squared with 2 df under the null of normality (5% critical value: 5.99).

**Low-power caveat:** with small samples (n below roughly 50), JB rarely rejects even for clearly non-normal data — failing to reject is weak evidence of normality, not confirmation. With large samples, financial return series almost always reject due to fat tails and (for equities) negative skewness. Treat the test as a screen, and pair it with a look at the actual skew/kurtosis magnitudes and extreme observations.

### Covariance estimation and Ledoit-Wolf shrinkage
The sample covariance matrix `Sigma_hat = (1/(n-1)) (X - X_bar)^T (X - X_bar)` becomes poorly conditioned or singular when the number of assets `p` approaches the number of observations `n`. Plugging it into a mean-variance optimizer then produces extreme, unstable weights that flip with small data changes.

Shrinkage blends the sample matrix toward a structured target:

$$\hat{\Sigma}_{shrunk} = \delta \cdot F + (1 - \delta) \cdot \hat{\Sigma}$$

where `F` is the target (e.g., scaled identity) and `delta` is the shrinkage intensity. Ledoit-Wolf (2004) derives the `delta` that minimizes expected squared Frobenius distance to the true covariance matrix, trading a little bias for a large variance reduction — yielding better-conditioned, invertible matrices and stable portfolio weights.

**Note:** the bundled script's `shrunk_covariance` implements a *simplified* shrinkage-intensity estimate, not the full Ledoit-Wolf estimator. For production work use `sklearn.covariance.LedoitWolf`.

### Regression diagnostics (CAPM and factor models)
For the single-factor CAPM regression `R_i - R_f = alpha + beta * (R_m - R_f) + epsilon`:
- `beta = rho * sigma_i / sigma_m` (market sensitivity); `alpha` is the risk-adjusted excess return.
- In a single-factor regression, `R^2 = rho^2`.
- Judge coefficients by t-statistics (`t = coefficient / SE`); with `n - 2` df, |t| above roughly 2 indicates 5% significance. A positive alpha point estimate with |t| < 2 is not evidence of skill.
- Adding regressors always raises R-squared; use adjusted R-squared, AIC/BIC, or cross-validation to guard against overfitting.

### Bootstrap procedure
Non-parametric resampling for the sampling distribution of a statistic when analytical standard errors are unavailable (Sharpe ratio, alpha), the distribution is non-normal, or samples are small:

1. From the original `n` observations, draw `B` resamples of size `n` **with replacement** (B = 1,000-10,000).
2. Compute the statistic on each resample.
3. Percentile method: the `(1 - alpha)` confidence interval is the `alpha/2` and `1 - alpha/2` percentiles of the bootstrap distribution; the bootstrap standard error is the std of the `B` statistics.

Caveat: the i.i.d. bootstrap ignores autocorrelation and volatility clustering; use block bootstrap for serially dependent return series.

### Standard Analysis Workflow

Given a return series, run this sequence:

1. **Descriptive stats** — mean, volatility (n-1), skewness, excess kurtosis; annualize for reporting.
2. **Distribution checks** — Jarque-Bera (mind the low-power caveat), inspect skew/kurtosis magnitudes and largest outliers; decide whether normal-based methods (parametric VaR, t-tests) are defensible.
3. **Covariance/correlation** (multi-asset) — sample covariance and correlation matrices; if `p` is large relative to `n`, apply shrinkage before any optimization.
4. **Regression diagnostics** — CAPM or factor regression; report alpha/beta with t-stats and R-squared; check residuals for structure.
5. **Bootstrap CIs** — for statistics without clean analytical standard errors (Sharpe, alpha, drawdown), bootstrap confidence intervals rather than reporting bare point estimates.

## Worked Examples

### Example 1: Descriptive Statistics and Normality Test
**Given:** 12 monthly returns (%): `[2.1, -0.5, 1.8, -3.2, 4.5, 0.3, -1.1, 2.7, -0.8, 3.4, 1.2, -0.6]`

```
Mean      = 9.8 / 12 = 0.8167% per month  (~9.8% annualized, simple x12)
s^2       = 52.977 / 11 = 4.816   ->   s = 2.195% per month
Ann. vol  = 2.195% * sqrt(12) = 7.60%
Skewness  = -0.045  (bias-corrected; near symmetric)
Ex. kurt  = -0.42   (bias-corrected; lighter tails than normal)

JB = (12/6) * ((-0.045)^2 + (-0.42)^2 / 4) = 0.09
```

JB = 0.09 < 5.99 (chi-squared 5% critical, df=2): **fail to reject** normality. With only 12 observations the test has very low power — this is not evidence that the returns are truly normal.

### Example 2: CAPM Regression from Summary Statistics
**Given:** 24 monthly observations. Fund excess returns: mean 0.8%, std 4.2%. Market excess returns: mean 0.6%, std 3.8%. Correlation 0.85.

```
beta  = rho * sigma_i / sigma_m = 0.85 * 4.2 / 3.8 = 0.939
alpha = 0.8% - 0.939 * 0.6% = 0.236% per month (~2.84% annualized)
R^2   = rho^2 = 0.7225

Residual std = 4.2% * sqrt(1 - 0.7225) = 2.213%
SE(alpha) = 2.213% / sqrt(24) = 0.452%   ->  t(alpha) = 0.236 / 0.452 = 0.52
SE(beta)  = 2.213% / (3.8% * sqrt(23)) = 0.121  ->  t(beta) = 0.939 / 0.121 = 7.74
```

With 22 df, the 5% two-tailed critical t is 2.074. Beta is highly significant (7.74 >> 2.074); alpha is **not** significant (0.52 < 2.074) — despite the positive point estimate, the sample cannot distinguish it from zero.

## Common Pitfalls
- Using population variance instead of sample variance: always use `n - 1` (Bessel's correction) when estimating from a sample.
- Assuming normality when financial returns have fat tails: equity returns typically show negative skewness and positive excess kurtosis; normal-based models (standard VaR) underestimate tail risk. Use Student-t or non-parametric methods.
- Ignoring non-stationarity: return distributions shift over time (regime changes, volatility clustering). Rolling-window estimation or GARCH may be more appropriate than full-sample statistics.
- Overfitting with too many regressors: R-squared always rises with added factors; use adjusted R-squared, information criteria, or cross-validation.
- Unstable covariance matrices with small samples: when `p` approaches or exceeds `n`, apply Ledoit-Wolf shrinkage or factor-based covariance models before optimizing.

## Running the Script
`scripts/statistics_fundamentals.py` provides a `StatisticsFundamentals` class with static methods `descriptive_stats`, `covariance_matrix`, `correlation_matrix`, `shrunk_covariance` (simplified Ledoit-Wolf — see note above), `ols_regression`, `rolling_regression`, `bootstrap_mean`, and `jarque_bera_test`.

- Run: `uv run scripts/statistics_fundamentals.py` (PEP 723 inline metadata resolves numpy and scipy), or `python3 scripts/statistics_fundamentals.py` with numpy/scipy installed.
- Bare invocation (or `--verify`) prints a demo on synthetic data **and** asserts the Example 1 worked-example values above (mean 0.8167, std 2.195, JB 0.09 on the 12-month series), exiting nonzero on any mismatch.
- `--help` lists the available methods and import usage.
- For programmatic use, import rather than run: `from statistics_fundamentals import StatisticsFundamentals`, then call e.g. `StatisticsFundamentals.descriptive_stats(...)`.

## Cross-References
- **return-calculations** (core plugin): Arithmetic and geometric mean returns, log returns for statistical modeling
- **time-value-of-money** (core plugin): Discount rate estimation via CAPM regression; NPV and IRR calculations use statistical inputs
- **factor-investing** (wealth-management plugin): Extends the single-factor CAPM/OLS regression to Fama-French multifactor models for alpha attribution and fund evaluation
- **financial-statements** (wealth-management plugin): applies descriptive statistics and trend analysis to financial ratios and peer comparisons


---

## SKILL: tear-sheet

- Fuente: `anthropics/financial-services` → `plugins/partner-built/spglobal/skills/tear-sheet` (Apache-2.0)
- Cuándo usarla: Generate professional company tear sheets using S&P Capital IQ data via the Kensho LLM-ready API MCP server. Use this skill whenever the user asks for a tear sheet, company one-pager, company profile, fact sheet, company snapshot, or company overview document — especially when they mention a specific company name or ticker. Also trigger when users ask for equity research summaries, M&A company profiles, corporate development target profiles, sales/BD meeting prep documents, or any concise single-company financial summary. This skill supports four audience types: equity research, investment banking/M&A, corporate development, and sales/business development. If the user doesn't specify an audience, ask. Works for both public and private companies.

# Financial Tear Sheet Generator

Generate audience-specific company tear sheets by pulling live data from S&P Capital IQ via the S&P Global MCP tools and formatting the result as a professional Word document.

## Style Configuration

These are sensible defaults. To customize for your firm's brand, modify this section — common changes include swapping the color palette, changing the font (Calibri is standard at many banks), and updating the disclaimer text.

**Colors:**
- Primary (header banner background, section header text): #1F3864
- Accent (signature section highlights): #2E75B6
- Table header row fill: #D6E4F0
- Table alternating row fill: #F2F2F2
- Table borders: #CCCCCC
- Header banner text: #FFFFFF

**Typography (sizes in half-points for docx-js):**
- Font family: Arial
- Company name: 18pt bold (size: 36)
- Section headers: 11pt bold (size: 22), Primary color
- Body text: 9pt (size: 18)
- Table text: 8.5pt (size: 17)
- Footer/disclaimer: 7pt italic (size: 14)
- Per-template overrides are specified in each reference file's Formatting Notes.

**Company Header Banner:**
- The header is a navy (#1F3864) banner spanning the full page width with company name in white.
- **Below the banner, key-value pairs MUST be rendered in a two-column borderless table spanning the full page width.** Left column: company identifiers (ticker, HQ, founded, employees, sector). Right column: financial identifiers (market cap, EV, stock price, shares outstanding). Each cell contains a bold label and regular-weight value on the same line (e.g., "**Market Cap** $124.7B"). Do not left-justify all fields in a single column — this wastes horizontal space and looks unprofessional. The two-column spread is the single most important visual signal that distinguishes a professional tear sheet from a default document.
  - **Implementation:** Create a 2-column table with `borders: none` and `shading: none` on all cells. Set column widths to 50% each. Place left-column fields (ticker, HQ, founded, employees) as separate paragraphs in the left cell. Place right-column fields (market cap, EV, stock price, shares outstanding) in the right cell. Each field is a single paragraph: bold run for the label, regular run for the value.
  - The specific fields in each column vary by audience — see the reference file's header spec. The principle is always: spread across the page, not clumped left.
- **Do not use a bordered table for the header key-value block.** Bordered tables are reserved for financial data only.
- Key metrics in the header (market cap, EV, stock price) should be displayed as inline key-value pairs, not in a separate bordered table.

**Section Headers:**
- Each section header gets a horizontal rule (thin line, #CCCCCC, 0.5pt) directly beneath it to create clean visual separation between sections.
- **Render the rule as a bottom border on the header paragraph itself** — do not insert a separate paragraph element for the rule. A separate paragraph adds its own before/after spacing and causes excessive whitespace below section titles.
- **Implementation:** In docx-js, apply a bottom border to the section header paragraph via `paragraph.borders.bottom = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" }`. Do not use `doc.addParagraph()` with a separate horizontal rule element. Do not use `thematicBreak`. The border must be on the heading paragraph itself with 0pt spacing after, so the rule sits tight against the header text.
- Spacing: 12pt before the header paragraph, 0pt after the header paragraph, 4pt before the next content element.

**Bullet Formatting:**
- Use a single bullet character (•) for all bulleted content across all tear sheet types. Do not mix •, -, ▸, or numbered lists within or across tear sheets.
- **Synthesis/analysis bullets** (Earnings Highlights, Strategic Fit, Integration Considerations, Conversation Starters): indented block-style formatting with left indent 360 DXA (0.25") and a hanging indent for the bullet character. These should be visually offset from body text — they're interpretive content and should look distinct from data tables and prose paragraphs.
- **Informational bullets** within relationship sections: standard body indent (180 DXA), no hanging indent.
- **Do not apply left-border accents to any bullet sections.** Left-border styling renders inconsistently in docx-js and creates visual artifacts. Use indentation and text size differentiation to distinguish signature sections instead.

**Tables (financial data only):**
- Header row: Table Header Fill (#D6E4F0) with bold dark text
- Body rows: alternating white / Table Alternating Fill (#F2F2F2)
- Borders: Table Border color (#CCCCCC), thin (BorderStyle.SINGLE, size 1)
- Cell padding: top/bottom 40 DXA, left/right 80 DXA
- Right-align all numeric columns
- Always use ShadingType.CLEAR (never SOLID — SOLID causes black backgrounds)

**Layout:**
- US Letter portrait, 0.75" margins (1080 DXA all sides)

**Number formatting:**
- Currency: USD. Use millions unless company revenue > $50B (then billions, one decimal). Label units in column headers (e.g., "Revenue ($M)"), not in individual cells.
- **Table cells: plain numbers with commas, no dollar signs.** Example: a revenue cell shows "4,916" not "$4,916". The column header carries the unit.
- Fiscal years: actual years (FY2022, FY2023, FY2024), never relative labels (FY-2, FY-1).
- Negatives: parentheses, e.g., (2.3%)
- Percentages: one decimal place
- Large numbers: commas as thousands separators

**Footer (document footer, not inline):**
Place the source attribution and disclaimer in the actual document footer (repeated on every page), not as inline body text at the bottom. The footer is exactly two lines, centered, on every page:
- Line 1: "Data: S&P Capital IQ via Kensho | Analysis: AI-generated | [Month Day, Year]"
- Line 2: "For informational purposes only. Not investment advice."
- Style: 7pt italic, centered, #666666 text color
- This footer text must be identical across all tear sheet types for the same company. Do not vary the wording by audience.
- **This footer is required on every tear sheet, every audience type, every page.** Do not omit it.

## Component Functions

**You MUST use these exact functions to create document elements. Do NOT write custom docx-js styling code.** Copy these functions into your generated Node script and call them. The Style Configuration prose above remains as documentation; these functions are the enforcement mechanism.

```javascript
const docx = require("docx");
const {
  Document, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, AlignmentType, BorderStyle, ShadingType,
  Header, Footer, PageNumber, HeadingLevel, TableLayoutType,
  convertInchesToTwip
} = docx;

// ── Color constants ──
const COLORS = {
  PRIMARY: "1F3864",
  ACCENT: "2E75B6",
  TABLE_HEADER_FILL: "D6E4F0",
  TABLE_ALT_ROW: "F2F2F2",
  TABLE_BORDER: "CCCCCC",
  HEADER_TEXT: "FFFFFF",
  FOOTER_TEXT: "666666",
};

const FONT = "Arial";

// ── 1. createHeaderBanner ──
// Returns an array of docx elements: [banner paragraph, key-value table]
function createHeaderBanner(companyName, leftFields, rightFields) {
  // leftFields / rightFields: arrays of { label: string, value: string }
  const banner = new Paragraph({
    children: [
      new TextRun({
        text: companyName,
        bold: true,
        size: 36, // 18pt
        color: COLORS.HEADER_TEXT,
        font: FONT,
      }),
    ],
    shading: { type: ShadingType.CLEAR, color: "auto", fill: COLORS.PRIMARY },
    spacing: { after: 0 },
    alignment: AlignmentType.LEFT,
  });

  function buildCellParagraphs(fields) {
    return fields.map(
      (f) =>
        new Paragraph({
          children: [
            new TextRun({ text: f.label + "  ", bold: true, size: 18, font: FONT }),
            new TextRun({ text: f.value, size: 18, font: FONT }),
          ],
          spacing: { after: 40 },
        })
    );
  }

  const noBorder = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
  const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };
  const noShading = { type: ShadingType.CLEAR, color: "auto", fill: "FFFFFF" };

  const kvTable = new Table({
    rows: [
      new TableRow({
        children: [
          new TableCell({
            children: buildCellParagraphs(leftFields),
            width: { size: 50, type: WidthType.PERCENTAGE },
            borders: noBorders,
            shading: noShading,
          }),
          new TableCell({
            children: buildCellParagraphs(rightFields),
            width: { size: 50, type: WidthType.PERCENTAGE },
            borders: noBorders,
            shading: noShading,
          }),
        ],
      }),
    ],
    width: { size: 100, type: WidthType.PERCENTAGE },
  });

  return [banner, kvTable];
}

// ── 2. createSectionHeader ──
// Returns a single Paragraph with bottom border rule
function createSectionHeader(text) {
  return new Paragraph({
    children: [
      new TextRun({
        text: text,
        bold: true,
        size: 22, // 11pt
        color: COLORS.PRIMARY,
        font: FONT,
      }),
    ],
    spacing: { before: 240, after: 0 }, // 12pt before, 0pt after
    border: {
      bottom: { style: BorderStyle.SINGLE, size: 1, color: COLORS.TABLE_BORDER },
    },
  });
}

// ── 3. createTable ──
// headers: string[], rows: string[][], options: { accentHeader?, fontSize? }
function createTable(headers, rows, options = {}) {
  const fontSize = options.fontSize || 17; // 8.5pt default
  const headerFill = options.accentHeader ? COLORS.ACCENT : COLORS.TABLE_HEADER_FILL;
  const headerTextColor = options.accentHeader ? COLORS.HEADER_TEXT : "000000";

  const cellBorders = {
    top: { style: BorderStyle.SINGLE, size: 1, color: COLORS.TABLE_BORDER },
    bottom: { style: BorderStyle.SINGLE, size: 1, color: COLORS.TABLE_BORDER },
    left: { style: BorderStyle.SINGLE, size: 1, color: COLORS.TABLE_BORDER },
    right: { style: BorderStyle.SINGLE, size: 1, color: COLORS.TABLE_BORDER },
  };

  const cellMargins = { top: 40, bottom: 40, left: 80, right: 80 };

  function isNumeric(val) {
    if (typeof val !== "string") return false;
    const cleaned = val.replace(/[,$%()]/g, "").trim();
    return cleaned !== "" && !isNaN(cleaned);
  }

  // Header row
  const headerRow = new TableRow({
    children: headers.map(
      (h) =>
        new TableCell({
          children: [
            new Paragraph({
              children: [
                new TextRun({
                  text: h,
                  bold: true,
                  size: fontSize,
                  color: headerTextColor,
                  font: FONT,
                }),
              ],
            }),
          ],
          shading: { type: ShadingType.CLEAR, color: "auto", fill: headerFill },
          borders: cellBorders,
          margins: cellMargins,
        })
    ),
  });

  // Data rows with alternating shading
  const dataRows = rows.map((row, rowIdx) => {
    const fill = rowIdx % 2 === 1 ? COLORS.TABLE_ALT_ROW : "FFFFFF";
    return new TableRow({
      children: row.map((cell, colIdx) => {
        const align = colIdx > 0 && isNumeric(cell)
          ? AlignmentType.RIGHT
          : AlignmentType.LEFT;
        return new TableCell({
          children: [
            new Paragraph({
              children: [
                new TextRun({ text: cell, size: fontSize, font: FONT }),
              ],
              alignment: align,
            }),
          ],
          shading: { type: ShadingType.CLEAR, color: "auto", fill: fill },
          borders: cellBorders,
          margins: cellMargins,
        });
      }),
    });
  });

  return new Table({
    rows: [headerRow, ...dataRows],
    width: { size: 100, type: WidthType.PERCENTAGE },
  });
}

// ── 4. createBulletList ──
// items: string[], style: "synthesis" | "informational"
function createBulletList(items, style = "synthesis") {
  const indent =
    style === "synthesis"
      ? { left: 360, hanging: 180 }   // 360 DXA left, hanging indent for bullet
      : { left: 180 };                 // 180 DXA, no hanging

  return items.map(
    (item) =>
      new Paragraph({
        children: [
          new TextRun({ text: "•  ", font: FONT, size: 18 }),
          new TextRun({ text: item, font: FONT, size: 18 }),
        ],
        indent: indent,
        spacing: { after: 60 },
      })
  );
}

// ── 5. createFooter ──
// date: string (e.g., "February 23, 2026")
function createFooter(date) {
  return new Footer({
    children: [
      new Paragraph({
        children: [
          new TextRun({
            text: `Data: S&P Capital IQ via Kensho | Analysis: AI-generated | ${date}`,
            italics: true,
            size: 14, // 7pt
            color: COLORS.FOOTER_TEXT,
            font: FONT,
          }),
        ],
        alignment: AlignmentType.CENTER,
      }),
      new Paragraph({
        children: [
          new TextRun({
            text: "For informational purposes only. Not investment advice.",
            italics: true,
            size: 14,
            color: COLORS.FOOTER_TEXT,
            font: FONT,
          }),
        ],
        alignment: AlignmentType.CENTER,
      }),
    ],
  });
}
```

**Usage in generated scripts:**
1. Copy all functions and constants above into the generated Node.js script
2. Call `createHeaderBanner(...)` instead of manually building banner paragraphs and tables
3. Call `createSectionHeader(...)` for every section title — never manually set paragraph borders
4. Call `createTable(...)` for **all** tabular data — financial summaries, trading comps, M&A activity, relationship tables, funding history, etc. Pass `{ accentHeader: true }` for M&A activity tables (IB/M&A template). For non-numeric tables (e.g., relationships, ownership), the function still works correctly — it only right-aligns cells that contain numeric values.
5. Call `createBulletList(items, "synthesis")` for earnings highlights, strategic fit, integration considerations, and conversation starters
6. Call `createBulletList(items, "informational")` for relationship entries
7. Pass `createFooter(date)` to the Document constructor's `footers.default` property

**What these functions eliminate:**
- Black background tables (enforces `ShadingType.CLEAR` everywhere)
- Separate horizontal rule paragraphs under section headers (enforces `border.bottom` on the paragraph itself)
- Bordered key-value tables in headers (enforces `borders: none`)
- Inconsistent bullet styles (enforces `•` character only)
- Missing footers (provides the exact footer structure)

## Workflow

### Step 1: Identify Inputs

Gather up to four things before proceeding:

1. **Company** — name or ticker. If only a ticker, resolve the full company name with an initial query (e.g., use the company info tool).
2. **Audience** — one of four types:
   - **Equity Research** — for buy-side/sell-side analysts evaluating an investment
   - **IB / M&A** — for bankers profiling a company in transaction context
   - **Corp Dev** — for internal strategic teams evaluating an acquisition target
   - **Sales / BD** — for commercial teams preparing for a client meeting
3. **Comparable companies** (optional) — if the user has specific comps in mind, note them. Otherwise the skill will identify peers from S&P Global data. This matters for Equity Research, IB/M&A, and Corp Dev tear sheets.
4. **Page length preference** (optional) — defaults vary by audience (see below), but the user can override.

If the user doesn't specify an audience, ask.

### Step 2: Read the Audience-Specific Reference

Read the corresponding reference file from this skill's directory:

- Equity Research → `references/equity-research.md`
- IB / M&A → `references/ib-ma.md`
- Corp Dev → `references/corp-dev.md`
- Sales / BD → `references/sales-bd.md`

Each reference defines sections, a query plan, formatting guidance, and page length defaults.

### Step 3: Pull Data via S&P Global MCP

**First:** Create the intermediate file directory:
```bash
mkdir -p /tmp/tear-sheet/
```

Use the **S&P Global** MCP tools (also known as the Kensho LLM-ready API). Claude will have access to structured tools for financial data, company information, market data, consensus estimates, earnings transcripts, M&A transactions, and business relationships. The query plans in each reference file describe what data to retrieve for each section — map these to the appropriate S&P Global tools available in the conversation.

**After each query step, immediately write the retrieved data to the intermediate file(s) specified in the reference file's query plan.** Do not defer writes — data written to disk is protected from context degradation in long conversations.

**Query strategy:**
Each reference file includes a query plan with 4-6 data retrieval steps. These are starting points, not rigid constraints. Prioritize data completeness over minimizing calls:

- **Always pull 4 fiscal years of financial data**, even though only 3 years are displayed. The fourth (earliest) year is needed to compute YoY revenue growth for the first displayed year. Without it, the earliest year's growth rate will show "N/A" — which looks like missing data, not a design choice.
- Execute the query plan as written, using whichever S&P Global tools match the data needed.
- If a tool call returns incomplete results, try alternative tools or narrower queries. For example, if company summary doesn't include segment detail, try the segments tool directly.
- If a data point isn't returned after a targeted retry, move on — label it "N/A" or "Not disclosed."
- Never fabricate data. If the tools don't return a number, do not estimate from training knowledge.

**User-specified comps:** If the user provided comparable companies, query financials and multiples for each comp explicitly. If no comps were provided, use whatever peer data the tools return, or identify peers from the company's sector using the competitors tool.

**Optional context from the user:** Listen for additional context the user provides naturally. If they mention who the acquirer is ("we're looking at this for our platform"), what they sell ("we sell data analytics to banks"), or who the likely buyers are ("this would be interesting to Salesforce or Microsoft"), incorporate that context into the relevant synthesis sections (Strategic Fit, Conversation Starters, Deal Angle). Don't prompt for this information — just use it if offered.

**Private company handling:**
CIQ includes private company data, so query the same way. However, expect sparser results. When generating for a private company:
- Skip: stock price, 52-week range, beta, stock performance, consensus estimates, trading comps
- Lean into: business overview, relationships, ownership structure, whatever financials are available
- Note "Private Company" prominently in the header

### Step 3b: Calculate Derived Metrics

After all data collection is complete and intermediate files are written, compute all derived metrics in a single dedicated pass. This is a calculation-only step — no new MCP queries.

**Read all intermediate files back into context**, then compute:

- **Margins:** Gross Margin %, EBITDA Margin %, FCF Margin %, Operating Margin %
- **Growth rates:** YoY revenue growth, YoY segment revenue growth, YoY EPS growth
- **Efficiency ratios:** FCF Conversion (FCF/EBITDA), R&D as % of Revenue, Capex as % of Revenue
- **Capital structure:** Net Debt (Total Debt − Cash & Equivalents), Net Debt / EBITDA
- **Segment mix:** Each segment's revenue as % of consolidated total revenue (use consolidated revenue as denominator per Data Integrity Rule 8)

**Validation (moved from Arithmetic Validation):** During this calculation pass, enforce all arithmetic checks:

- **Margin calculations:** Verify EBITDA Margin = EBITDA / Revenue, Gross Margin = Gross Profit / Revenue, etc. If the computed margin doesn't match the raw numbers, use the computation from raw components.
- **Growth rates:** Verify YoY growth = (Current − Prior) / Prior. Don't rely on pre-computed growth rates if you have the underlying values.
- **Segment totals:** If showing revenue by segment, verify segments sum to total revenue (within rounding tolerance). If they don't, omit the total row rather than publishing inconsistent math.
- **Percentage columns:** Verify "% of Total" columns sum to ~100%.
- **Valuation cross-checks:** If you show both EV and EV/Revenue, verify EV / Revenue ≈ the stated multiple.

If a validation fails: attempt recalculation from raw data. If still inconsistent, flag the metric as "N/A" rather than publishing incorrect numbers. Quiet math errors in a tear sheet destroy credibility.

**Write results** to `/tmp/tear-sheet/calculations.csv` with columns: `metric,value,formula,components`

Example rows:
```
metric,value,formula,components
gross_margin_fy2024,72.4%,gross_profit/revenue,"9524/13159"
revenue_growth_fy2024,12.3%,(current-prior)/prior,"13159/11716"
net_debt_fy2024,2150,total_debt-cash,"4200-2050"
```

### Step 3c: Verify Data Files

Before generating the document, verify that all intermediate files are present and populated.

**Read each intermediate file** via separate read operations and print a verification summary:

```
=== Tear Sheet Data Verification ===
company-profile.txt: ✓ (12 fields)
financials.csv:      ✓ (36 rows)
segments.csv:        ✓ (8 rows)
valuation.csv:       ✓ (5 rows)
calculations.csv:    ✓ (18 rows)
earnings.txt:        ✓ (populated)
relationships.txt:   ⚠ MISSING
peer-comps.csv:      ✓ (12 rows)
================================
```

**Soft gate:** If any file expected for the current audience type is missing or empty, print a warning but continue. The tear sheet handles missing data gracefully with "N/A" and section skipping. However, the warning ensures visibility into what data was lost.

**Critical rule: The files — not your memory of earlier conversation — are the single source of truth for every number in the document.** When generating the DOCX in Step 4, read values from the intermediate files. Do not rely on conversation context for financial data.

### Step 4: Format as DOCX

Read `/mnt/skills/public/docx/SKILL.md` for docx creation mechanics (docx-js via Node). Apply the Style Configuration above plus the section-specific formatting in the reference file.

**Page length defaults (user can override):**
- Equity Research: 1 page (density is the convention)
- IB / M&A: 1-2 pages
- Corp Dev: 1-2 pages
- Sales / BD: 1-2 pages

If content exceeds the target, each reference file specifies which sections to cut first.

**Output filename:** `[CompanyName]_TearSheet_[Audience]_[YYYYMMDD].docx`
Example: `Nvidia_TearSheet_CorpDev_20260220.docx`

Save to `/mnt/user-data/outputs/` and present to the user.

## Data Integrity Rules

These override everything else:
1. **S&P Global tools are the only source for financial data.** Do not fill gaps with training knowledge — it may be stale or wrong.
2. **Label what you can't find.** Use "N/A" or "Not disclosed" rather than omitting a row silently.
3. **Dates matter.** Note the fiscal year end or reporting period. Don't assume calendar year = fiscal year. Market data (stock prices, market cap) should include an "as of" date.
4. **Don't mix reporting periods.** If you have FY2023 revenue and LTM EBITDA, label them distinctly.
5. **Prefer MCP-returned fields over manual computation.** If the S&P Global tools return a pre-computed field (e.g., net debt, EBITDA, FCF), use that value directly rather than computing it from components. Only compute derived metrics manually when the tools do not return the field. This reduces discrepancies.
6. **Ensure consistency across tear sheet types.** If generating multiple tear sheets for the same company (e.g., equity research and IB/M&A in the same session), the same underlying data points must produce identical values across all outputs. Net debt, revenue, EBITDA, margins, and growth rates must match exactly. Do not re-query or re-compute independently per report — reuse the same retrieved values.
7. **Never downgrade known transaction values.** If the M&A tools return a deal value for a transaction, that value must appear in the output. Do not replace a known deal value with "Undisclosed." Use "Undisclosed" only when the tools genuinely return no value for a transaction.
8. **Use consolidated revenue as the denominator for segment percentages.** When computing "% of Total" for segment tables, divide each segment's revenue by consolidated total revenue (as reported on the income statement), not by the sum of segment revenues. The sum of segments often exceeds consolidated revenue due to intersegment eliminations. Using consolidated revenue ensures percentages align with the total revenue figure shown elsewhere in the document.
9. **Always include forward (NTM) multiples when available.** If the tools return both trailing and forward valuation multiples, both must appear in the output. Forward multiples are the primary valuation reference for equity research, IB/M&A, and corp dev audiences. Never show only trailing multiples when forward data is available.
10. **No S&P Global tool returns executive or management data.** Do not populate management names, titles, or biographical details from training data — this violates Rule 1 and produces stale information. If a management section appears in a template, omit it entirely. Ownership structure (institutional holders, insider %, PE sponsor) may be included only if returned by the tools — gate with "data permitting."

## Intermediate File Rule

All data retrieved from MCP tools must be persisted to structured intermediate files before document generation. These files — not conversation context — are the single source of truth for every number in the document.

**Setup:** At the start of Step 3, create the working directory:
```
mkdir -p /tmp/tear-sheet/
```

**Write-after-query mandate:** After each MCP query step completes, immediately write the retrieved data to the appropriate intermediate file(s). Do not wait until all queries finish. Each reference file's query plan specifies which file(s) to write after each step.

**File schemas:**

| File | Format | Columns / Structure | Used By |
|---|---|---|---|
| `/tmp/tear-sheet/company-profile.txt` | Key-value text | name, ticker, exchange, HQ, sector, industry, founded, employees, market_cap, enterprise_value, stock_price, 52wk_high, 52wk_low, shares_outstanding, beta, ownership | All |
| `/tmp/tear-sheet/financials.csv` | CSV | `period,line_item,value,source` | All |
| `/tmp/tear-sheet/segments.csv` | CSV | `period,segment_name,revenue,source` | ER, IB, CD |
| `/tmp/tear-sheet/valuation.csv` | CSV | `metric,trailing,forward,source` | ER, IB, CD |
| `/tmp/tear-sheet/consensus.csv` | CSV | `metric,fy_year,value,source` | ER |
| `/tmp/tear-sheet/earnings.txt` | Structured text | Quarter, date, key quotes, guidance, key drivers | ER, IB, Sales |
| `/tmp/tear-sheet/relationships.txt` | Structured text | Customers, suppliers, partners, competitors — each with descriptors | IB, CD, Sales |
| `/tmp/tear-sheet/peer-comps.csv` | CSV | `ticker,metric,value,source` | ER, IB, CD |
| `/tmp/tear-sheet/ma-activity.csv` | CSV | `date,target,deal_value,type,rationale,source` | IB, CD |
| `/tmp/tear-sheet/calculations.csv` | CSV | `metric,value,formula,components` | All (written in Step 3b) |

**Abbreviations:** ER = Equity Research, IB = IB/M&A, CD = Corp Dev, Sales = Sales/BD.

Not every audience type uses every file — the reference files define which query steps apply. Files not relevant to the current audience type need not be created.

**Raw values only.** Intermediate files store raw values as returned by the tools. Do not pre-compute margins, growth rates, or other derived metrics in these files — that happens in Step 3b.

**Page budget enforcement:** Each reference file specifies a default page length and a numbered cut order. If the rendered document exceeds the target, apply cuts in the order specified — do not attempt to shrink font sizes or margins below the template minimums. The cut order is a strict priority stack: cut section 1 completely before touching section 2.

## Content Quality Rules

11. **Rewrite every narrative section for the audience.** The CIQ company summary is an input, not an output. Each audience type needs a different description: concise and thesis-oriented for equity research, pitchbook prose for IB, product-focused for Corp Dev, plain language for Sales/BD. Never paste the CIQ summary verbatim into any tear sheet.
12. **Differentiate earnings highlights by audience.** The same earnings call produces different takeaways for different readers. Equity research wants segment-level performance and consensus beat/miss. IB wants margin trajectory and strategic commentary. Sales/BD wants strategic themes that create conversation angles. Do not reuse the same bullets across tear sheet types.
13. **Synthesis sections are the differentiator.** Strategic Fit Analysis, Integration Considerations, Conversation Starters, and Business Overview paragraphs are where the tear sheet earns its value. These sections require analytical reasoning that connects data points into a narrative — listing company names without context is not synthesis.
14. **Flag pending divestitures in segment tables.** If a company has announced a pending divestiture of a segment or business unit, add a footnote or parenthetical to the segment table noting the pending transaction (e.g., "Mobility* — *Pending divestiture, expected mid-2026"). For Corp Dev and IB/M&A tear sheets, include a one-line note below the segment table showing pro-forma revenue and revenue mix excluding the divested segment. This helps the reader evaluate the "go-forward" business without doing the math themselves.

### Arithmetic Validation

**→ Arithmetic validation is now enforced in Step 3b (Calculate Derived Metrics).** All margin calculations, growth rates, segment totals, percentage columns, and valuation cross-checks are validated during the dedicated calculation pass, before document generation begins. See Step 3b for the full validation checklist.

### Referencia: references/corp-dev.md

# Corporate Development Tear Sheet

## Purpose
A target evaluation profile for an internal Corp Dev team assessing a potential acquisition. Unlike the IB/M&A profile (which tells a strategic *story* for a pitch), this is an analytical document focused on strategic fit: how the target's products, customers, technology, and operations overlap with or complement the acquirer's. The Corp Dev audience already knows their own company — they need to understand the target through the lens of "should we buy this, and what would integration look like?"

**Default page length:** 1-2 pages. Corp Dev teams are comfortable with denser profiles and won't penalize a second page if the content is substantive.

## Query Plan

Start with these queries. Break apart and follow up if results are incomplete.

**Query 1 — Target profile:**
"[Company] business description products services technology platform headquarters founded employees sector industry"
→ Header, Business & Product Overview
→ **Immediately write** to `/tmp/tear-sheet/company-profile.txt`

**Query 2 — Financials:**
"[Company] annual income statement revenue gross profit EBITDA operating income net income capex free cash flow R&D expense total debt cash and equivalents last 4 fiscal years"
→ Financial Summary (pull 4 years; display 3; use the earliest year only for YoY growth computation. R&D is especially important for Corp Dev — they want to understand the target's investment in IP)
→ **Immediately write** raw values to `/tmp/tear-sheet/financials.csv`

**Query 3 — Segments + customers:**
"[Company] revenue by segment business unit last 2 fiscal years key customers end markets customer concentration"
→ Revenue Mix (need 2 years for YoY growth), Customer Analysis
→ **Immediately write** segment data to `/tmp/tear-sheet/segments.csv` (skip if no segment data returned)

**Query 4 — Relationships + competitive landscape:**
"[Company] key customers suppliers partners competitors business relationships technology vendors"
→ Strategic Fit Analysis, Ecosystem Map
→ **Immediately write** to `/tmp/tear-sheet/relationships.txt`

**Query 5 — Valuation + peers:**
If user provided specific comps:
"[Comp company] enterprise value EV/Revenue EV/EBITDA revenue growth EBITDA margin"
Otherwise:
Use the competitors tool to identify 3-5 public peers, then pull EV/Revenue (NTM), EV/EBITDA (NTM), revenue growth %, and EBITDA margin % for each.
Also: "[Company] enterprise value market capitalization valuation multiples"
→ Valuation Context
→ **Immediately write** company multiples to `/tmp/tear-sheet/valuation.csv`
→ **Immediately write** peer data to `/tmp/tear-sheet/peer-comps.csv`

**Query 6 — Ownership (data permitting):**
"[Company] ownership structure investors institutional ownership insider ownership"
→ Ownership snapshot (no intermediate file — included in company-profile.txt if available)

## Sections

Listed in priority order. See "Page Budget & Cut Order" below for explicit cut guidance.

### 1. Company Header
Similar to IB/M&A but adds a "Strategic Relevance" tagline.

| Field | Notes |
|---|---|
| Company name | Large, bold |
| Ticker & Exchange | If public; omit for private |
| HQ Location | |
| Founded / Employees | |
| Enterprise Value | Market cap for public; latest valuation for private |
| Ownership | Public / PE-backed / Founder-led / etc. |
| **Strategic Relevance** | One sentence: why this target is attractive to an acquirer (synthesized from data) |

The "Strategic Relevance" line is unique to Corp Dev. Write from a neutral analytical perspective, not from the target's marketing language. Frame what an acquirer *gets* — not what the target *is*. Good: "Dominant position in commodity price benchmarks with regulatory moat and 70%+ gross margins — a capital-light, high-barrier data asset." Bad: "The world's leading provider of financial data and analytics." The former tells a corp dev team why this is attractive; the latter is a press release.

### 2. Business & Product Overview
**Do not paste the CIQ company summary.** Rewrite in 4-6 sentences (one paragraph, not two) with a product and technology focus — this audience evaluates acquisitions, not investments:
- Core products/services and what problem they solve
- Technology or platform architecture (at a high level)
- Key differentiators and competitive moat
- Customer segments — who buys this and why
- Current strategic direction

Write with an acquirer's lens. The reader is thinking: "How would this fit with what we already have?" The description should make it easy to spot overlaps and complements.

### 3. Revenue Mix & Customer Profile
Two sub-sections:

**a) Revenue by Segment** (if available):

| Segment | Revenue ($M) | % of Total | YoY Growth |
|---|---|---|---|

**b) Customer Analysis:**
Below the segment table (or in place of it if segments aren't available), write a qualitative paragraph covering:
- Customer concentration: are the top 5 customers >30% of revenue? (Critical for acquisition risk)
- Customer type: enterprise vs. SMB vs. consumer
- Contract structure: subscription vs. transactional vs. license (if known)
- Geographic mix

Customer concentration is the single most important signal here — if the tools return any data on top customers or revenue concentration, highlight it prominently. If data is sparse, write what you can infer from the business description and relationships. Keep this to 2-3 sentences — it's context for the segment table, not a standalone analysis.

### 4. Strategic Fit Analysis
**This is the signature section of the Corp Dev tear sheet.** It is required — do not skip or compress it. It uses the Business Relationships data from S&P Capital IQ to map overlaps and complements.

Organize as three buckets. **Each bucket must be 2-3 sentences of analytical reasoning, not a list of company names.** Listing "Customers: Microsoft, JPMorgan, Google" without context is useless. Instead, explain *what the overlap or complement means* for an acquisition.

**Customer Overlap:** Do the target's customers also buy from the acquirer (or the acquirer's industry)? Shared customers = easier cross-sell, but also risk of channel conflict. Name shared relationships and explain the implications.

**Technology / Product Complement:** Does the target fill a gap in the acquirer's portfolio? What does their tech stack look like? Who are their technology vendors? If they're already using the acquirer's technology, explain why that's a strong integration signal.

**Competitive Displacement:** Is the target a competitor, or does acquiring them remove a competitor from the market? Name the target's key competitors and explain how the competitive landscape would change post-acquisition.

This section requires synthesis — combine relationship data with the business overview to draw connections. If the user has told you who the acquirer is, tailor to that acquirer. If not, write it generically but still analytically.

**Length discipline:** The 2-3 sentence target per bucket above is a hard constraint, not a suggestion. Each bullet should front-load the insight, then support with one specific data point. The actual outputs frequently balloon to 5-7 sentences per bullet — this is the primary driver of page 3 spillover. If you find yourself writing more than 3 sentences, move the excess detail to Integration Considerations.

### 5. Financial Summary (3-Year)
Similar to IB/M&A but with added emphasis on R&D and capital efficiency.

| Metric ($M) | FY20XX | FY20XX | FY20XX |
|---|---|---|---|
| Revenue | | | |
| Revenue Growth % | | | |
| Gross Margin % | | | |
| EBITDA | | | |
| EBITDA Margin % | | | |
| R&D Expense | | | |
| R&D as % of Revenue | | | |
| Capex | | | |
| Free Cash Flow | | | |
| FCF Conversion (FCF/EBITDA) | | | |

R&D intensity signals how much of the target's value is in IP vs. services. FCF conversion signals integration complexity — high-capex businesses are harder to integrate. If R&D expense isn't separately reported, note "Not separately disclosed" in the row rather than "N/A" — this itself is informative (suggests R&D may be embedded in COGS or SG&A).

**Capital Structure** (compact sub-table below the financial summary):

| Metric | Value |
|---|---|
| Total Debt | $XXM |
| Cash & Equivalents | $XXM |
| Net Debt | $XXM |
| Net Debt / EBITDA | X.Xx |

Frame for acquisition context: below the table, include one sentence interpreting leverage (e.g., "Net debt of $X represents Y.Yx EBITDA leverage, which is manageable for an investment-grade acquirer but would compound leverage in an LBO scenario."). Pull from the balance sheet data already retrieved.

### 6. Valuation Context
**This section is required for public companies.** Corp Dev teams need market context to frame a potential bid. If the tools return valuation multiples, this section must appear. Do not cut it for space — cut Ownership Snapshot (Section 7) first.

Not a formal valuation — Corp Dev teams do their own DCFs. This provides market context.

**a) Trading multiples** (if public):

**Peer context is essential, not optional.** If the user provided comps, show each in its own column. If no comps were provided, use the competitors tool to identify 3-5 public peers, then pull EV/Revenue (NTM), EV/EBITDA (NTM), revenue growth %, and EBITDA margin % for each.

| Metric | [Company] | [Peer 1] | [Peer 2] | [Peer 3] | Peer Median |
|---|---|---|---|---|---|
| EV/Revenue (NTM) | | | | | |
| EV/EBITDA (NTM) | | | | | |
| Revenue Growth % | | | | | |
| EBITDA Margin % | | | | | |

A company's multiples in isolation tell a corp dev team nothing — they need relative context to assess whether the target is cheap or rich vs. the peer set. This is the minimum viable valuation context for a target profile.

If peer multiples are unavailable from the tools, show the company's own multiples and list selected peer names below the table for the reader's reference.

**b) Precedent transactions (data permitting):**
If the M&A tools return recent transactions involving the company's peers or within the same sub-sector, display them:

| Date | Target | Acquirer | EV ($M) | EV/Rev | EV/EBITDA |
|---|---|---|---|---|---|

Frame as context: "Recent transactions in [sub-sector] have valued targets at X–Yx revenue."

If precedent transaction data is not available from the tools, note "Precedent transaction data not available from data source" rather than omitting silently. Do not fabricate precedent multiples.

For private companies, skip trading multiples. Precedent transactions (data permitting) are still useful.

### 7. Ownership Snapshot (data permitting — omit if tools return nothing)
If the tools return ownership data, include a compact block: founder/family control %, PE sponsor details, institutional concentration. Ownership structure directly impacts deal complexity and is relevant for integration considerations.

**Do not include a Management Team table.** No S&P Global tool returns executive data — see Data Integrity Rule 10. Management names from training data will be stale.

### 8. Integration Considerations
**Required section — do not cut.** This is the analytical capstone of the Corp Dev tear sheet. Synthesized observations drawn from everything above. 3-4 substantive bullets:
- **Key risks:** Customer concentration, key-person dependency, technology debt indicators
- **Integration complexity:** Geography (multi-country = harder), employee count, number of products
- **Synergy signals:** Shared customers, complementary products, overlapping technology vendors
- **Open questions:** What would a corp dev team need to diligence before making a bid? Focus on concrete, actionable diligence items — not open-ended strategic questions. Good examples: regulatory approval timeline and jurisdictions, change-of-control provisions in key contracts, key-person retention risk (especially founders/CTOs), customer contract transferability, IP ownership structure, outstanding litigation. Bad examples: "How defensible is X?" or "What is the long-term market opportunity?" — these are analyst questions, not diligence items.

Label clearly as analytical observations, not facts from the data source.

## Page Budget & Cut Order

**Target: 2 pages.** Corp Dev profiles can fill both pages with substantive content, but must not spill to a third unless the user explicitly requests a longer format. If content exceeds 2 pages, cut in this order (cut each completely before moving to the next):

1. Ownership Snapshot (section 7) — omit entirely
2. Customer Analysis prose under Revenue Mix (section 3) — reduce to 2 sentences max
3. Valuation Context prose (section 6) — keep peer comp table, cut interpretive paragraph below it
4. Precedent Transactions (section 6b) — keep the "not available" note, remove if space-critical
5. Capital Structure prose — keep table, cut interpretive paragraph below it
6. Strategic Fit Analysis (section 4) — compress each bullet to 2-3 sentences max (do not remove the section)

Never cut: Business & Product Overview (2), Financial Summary (5 core table), Integration Considerations (8).

## Formatting Notes
- **Strategic Fit Analysis is the centerpiece.** Give it distinctive formatting:
  - Bump text to 9.5pt (size: 19) — slightly larger than standard body text. This section should look like the most important content on the page.
  - Use the standard indented block-style bullets from the global style config (360 DXA left indent).
  - Do not apply left-border accents — they render inconsistently in docx-js.
- Financial Summary should include R&D and FCF conversion prominently.
- Valuation Context with peer comps is required for public companies — do not cut before Ownership Snapshot.
- For private targets, the profile leans heavily on qualitative sections (Business Overview, Strategic Fit, Relationships) — this is expected and still highly valuable.
- Tone: analytical and evaluative, not promotional. This isn't a pitch — it's an assessment.
- **Two-page discipline:** Before rendering, mentally estimate page count. The combination of Strategic Fit (3 long bullets) + Integration Considerations (4 bullets) alone can consume a full page — if so, compress Strategic Fit bullets first.

### Referencia: references/equity-research.md

# Equity Research Tear Sheet

## Purpose
A dense snapshot for buy-side or sell-side analysts evaluating an investment. Emphasis on valuation, forward estimates, financial trajectory, and analyst consensus. Everything supports or challenges an investment thesis.

**Default page length:** 1 page. Equity research tear sheets are conventionally single-page — density is the point. If the user requests more space, extend to 2 pages.

## Query Plan

Start with these queries. If results are incomplete, break into narrower follow-ups.

**Query 1 — Profile + market data:**
"[Company] company overview sector industry market capitalization enterprise value stock price 52-week high low shares outstanding beta"
→ Header, Business Description
→ **Immediately write** to `/tmp/tear-sheet/company-profile.txt`

**Query 2 — Historical financials:**
"[Company] annual income statement revenue gross profit EBITDA net income EPS free cash flow total debt cash and equivalents last 4 fiscal years"
→ Financial Summary (pull 4 years; display 3; use the earliest year only for YoY growth computation)
→ **Immediately write** raw values to `/tmp/tear-sheet/financials.csv`

**Query 2b — Segments (if available):**
"[Company] revenue by segment business unit last 2 fiscal years"
→ Revenue & Segment Breakdown (need 2 years for YoY growth). If segment data is unavailable, skip this section — do not leave a blank table.
→ **Immediately write** to `/tmp/tear-sheet/segments.csv` (skip if no segment data returned)

**Query 3 — Valuation + consensus:**
"[Company] P/E EV/EBITDA EV/Revenue valuation multiples consensus revenue EPS estimates analyst recommendations price target"
→ Valuation Snapshot, Consensus Estimates
→ **Immediately write** multiples to `/tmp/tear-sheet/valuation.csv`
→ **Immediately write** estimates to `/tmp/tear-sheet/consensus.csv`

**Query 4 — Earnings:**
"[Company] most recent earnings call key takeaways guidance"
→ Earnings Highlights
→ **Immediately write** to `/tmp/tear-sheet/earnings.txt`

**Query 5 — Stock performance:**
"[Company] stock price return 1 month 3 month 6 month 1 year YTD performance"
→ Stock Performance (no intermediate file — data goes directly into document)

**Query 6 (if user provided comps):**
"[Comp company] market cap EV/Revenue EV/EBITDA revenue growth" — repeat for each comp
→ Peer context for Valuation Snapshot
→ **Immediately write** to `/tmp/tear-sheet/peer-comps.csv`

## Sections

Listed in priority order. If constrained to one page, cut from the bottom.

### 1. Company Header
Compact key-value block rendered as a two-column borderless table per the global style config.

Left column: Ticker (exchange), sector / industry, HQ
Right column: Stock price, 52-week range, market cap, EV, shares outstanding, beta

### 2. Business Description
2-3 tight sentences. **Rewrite in your own words for an analyst audience** — do not paste the CIQ company summary verbatim. The CIQ summary is an input; the output should be concise and thesis-oriented.

For well-known, widely covered companies, assume the analyst already knows the basic business. Lead with what's *changing* — strategic pivots, portfolio reshaping, new growth vectors — not a Wikipedia-style overview. For example, for a Fortune 500 company, don't spend a sentence on "provides financial data to institutions." Instead: "Reshaping its portfolio toward higher-margin data and analytics businesses, with a pending Mobility spin-off and aggressive AI investment through its Kensho subsidiary."

For lesser-known companies, a brief "what they do" sentence is appropriate before pivoting to the thesis-relevant dynamics.

### 3. Valuation Snapshot
Centerpiece of the equity tear sheet.

| Metric | Trailing | Forward (NTM) |
|---|---|---|
| P/E | | |
| EV/EBITDA | | |
| EV/Revenue | | |
| P/FCF | | |
| Dividend Yield | | |

**Forward multiples are mandatory when available from the tools.** Showing only trailing multiples when forward data exists is a significant gap — analysts value companies on forward earnings. If forward multiples aren't available, show trailing only and note "Fwd estimates N/A."

If the user provided comparable companies, add columns for each comp (or a "Peer Median" column if 3+ comps). If no user comps, and the tools return peer data, include a Peer Median column. If neither, show the company's multiples only.

### 4. Consensus Estimates
What the Street expects — a key differentiator for this tear sheet type.

**Data availability note:** The depth of consensus data varies by company and coverage. Include whatever the tools return — analyst count, price target, Buy/Hold/Sell distribution — but do not fabricate or estimate any consensus figure. For thinly covered companies, this section may contain only revenue and EPS estimates, which is still valuable.

| Metric | FY[year] Est. | FY[year+1] Est. |
|---|---|---|
| Revenue | | |
| EPS (normalized) | | |
| EBITDA | | |

Use normalized/adjusted EPS where available — GAAP EPS can be distorted by one-time items and is less useful for forward estimates.

Below the main estimates table, include a compact analyst consensus block (if data is available from the tools):

| Analyst Consensus | |
|---|---|
| Mean Price Target | $XXX |
| # of Estimates | XX |
| Buy / Hold / Sell | XX / XX / XX |

If price target or recommendation data is unavailable, omit the analyst consensus block rather than showing empty rows. Do not fabricate these figures.

If consensus data isn't available at all, skip this entire section and note "Consensus estimates not available." Do not estimate.

### 5. Financial Summary (3-Year)
Dense single table using actual fiscal year labels.

| Metric ($M) | FY20XX | FY20XX | FY20XX |
|---|---|---|---|
| Revenue | | | |
| Revenue Growth % | | | |
| Gross Margin % | | | |
| EBITDA | | | |
| EBITDA Margin % | | | |
| Net Income | | | |
| EPS (Diluted) | | | |
| Free Cash Flow | | | |
| Net Debt | | | |

Compute derived metrics (growth %, margins) from raw data rather than querying separately.

**Capital Structure (separate compact sub-table below the Financial Summary):**
Do NOT append these rows to the 3-year Financial Summary table — blank cells in prior-year columns look like missing data. Instead, render as a separate 2-column sub-table (Metric | Value) directly below, showing only the most recent fiscal year:

| Metric | FY[latest] |
|---|---|
| Total Debt | $XXM |
| Cash & Equivalents | $XXM |
| Net Debt | $XXM |

This matches the capital structure format used in Corp Dev and IB/M&A tear sheets. Keep it tight — no extra spacing between the Financial Summary and this sub-table.

### 6. Revenue & Segment Breakdown
If segment data is available from the tools, include a compact segment revenue table. This is essential context for equity research — analysts need to see which business lines are driving growth.

| Segment | Revenue ($M) | % of Total | YoY Growth |
|---|---|---|---|
| [Segment A] | | | |
| [Segment B] | | | |

Keep this compact for the one-pager: table only, no qualitative paragraph. If segment data is unavailable, skip this section entirely — do not include a blank or placeholder table.

### 7. Recent Earnings Highlights
Include the quarter and date (e.g., "Q3 FY2025 — October 2025"). 3-4 bullets with an **investment lens** — this audience wants segment-level specifics, not strategic themes:

**Lead with guidance if provided.** If management issued forward guidance, make it the first bullet with a bold **Guidance:** prefix (e.g., "**Guidance:** FY2026 EPS of $19.40–$19.65, implying 9–10% growth; organic revenue growth of 6–8%."). Guidance is the single most actionable forward-looking data point for an analyst — do not bury it among operating highlights.

**Beat/miss context (data permitting):** If consensus estimate data is available for the reported period, frame the headline result bullet as a beat/miss: "Revenue of $X beat/missed consensus of $Y by Z%." If consensus data for the reported period is not available from the tools, describe results in absolute terms and growth rates only — do not fabricate consensus figures.

Then:
- Segment-level performance: which business lines accelerated or decelerated
- Margin trajectory: any commentary on cost structure or profitability trends

Attribute to management: "Management highlighted…" or "CFO noted…" rather than declarative claims. This section should feel like an earnings recap, not a press release summary.

### 8. Key Operating Metrics
2-3 sector-relevant KPIs if available from the data (subscriber count, same-store sales, NIM, etc.). If nothing sector-specific, compute ROE and ROIC from the financials already retrieved. Optional — drop if space is tight.

### 9. Stock Performance (cut first)
Period return table. Low analytical value for this audience — cut this before anything else.

| Period | Return |
|---|---|
| 1 Month | |
| 3 Month | |
| YTD | |
| 1 Year | |

## Formatting Notes
- **This is the densest tear sheet type.** It should feel noticeably more compressed than the other templates.
- Financial Summary table: 8pt text (size: 16), row height 240 DXA. Tightest spacing of any template.
- Valuation Snapshot and Consensus Estimates: 8.5pt text, occupy the visual center — analysts scan these first.
- Body text: 8.5pt (size: 17) — smaller than the global 9pt default. Every half-point matters on a one-pager.
- Section spacing: minimize. 6pt before section headers (not the global 12pt), 2pt after rules.
- Bold any metric showing a notable inflection (growth turning positive, margin expansion/compression).
- Prioritize information over whitespace at every turn.

### Referencia: references/ib-ma.md

# Investment Banking / M&A Tear Sheet

## Purpose
A company profile for transaction context — potential target, acquirer, or pitchbook inclusion. Emphasis on strategic positioning, segment detail, business relationships, and M&A activity. Valuation framed in transaction multiples, not investment thesis.

**Default page length:** 1-2 pages. IB company profiles routinely spill to a second page, especially when segment and M&A data is rich.

## Query Plan

Start with these queries. Break apart and follow up if results are incomplete.

**Query 1 — Profile + identification:**
"[Company] business description headquarters founded employees sector industry ownership structure major shareholders"
→ Header, Business Overview
→ **Immediately write** to `/tmp/tear-sheet/company-profile.txt`

**Query 2 — Segments + financials:**
"[Company] revenue by segment business unit last 2 fiscal years AND annual income statement revenue gross profit EBITDA operating income net income capex free cash flow total debt cash and equivalents last 4 fiscal years"
→ Segment Breakdown (need 2 years to compute YoY growth), Financial Summary (pull 4 years; display 3; use the earliest year only for YoY growth computation)
→ **Immediately write** raw financials to `/tmp/tear-sheet/financials.csv`
→ **Immediately write** segment data to `/tmp/tear-sheet/segments.csv` (skip if no segment data returned)

**Query 3 — Valuation + comps:**
If the user provided specific comparable companies, query each:
"[Comp company] enterprise value EV/Revenue EV/EBITDA revenue growth EBITDA margin"
Otherwise:
Use the competitors tool to identify 3-5 public peers, then pull EV/Revenue (NTM), EV/EBITDA (NTM), revenue growth %, and EBITDA margin % for each.
Also: "[Company] enterprise value market capitalization EV/Revenue EV/EBITDA valuation multiples"
→ Header (EV/market cap), Trading Comps
→ **Immediately write** company multiples to `/tmp/tear-sheet/valuation.csv`
→ **Immediately write** peer data to `/tmp/tear-sheet/peer-comps.csv`

**Query 4 — M&A activity:**
"[Company] acquisitions divestitures completed transactions last 5 years deal value"
→ Company's own deals
→ **Immediately write** to `/tmp/tear-sheet/ma-activity.csv`

**Query 5 — Comparable transactions (data permitting):**
Use the specific industry from Query 1 results (e.g., "cloud observability software M&A transactions" not "technology M&A"). If the user specified comps, also try: "[comp company] acquisition deal multiples."
→ Comparable Transactions
→ **Append** comparable transactions to `/tmp/tear-sheet/ma-activity.csv` (add `type=precedent` to distinguish from company's own deals)

**Query 6 — Relationships + ownership:**
"[Company] key customers suppliers partners business relationships institutional ownership insider ownership"
→ Business Relationships, Ownership (data permitting)
→ **Immediately write** to `/tmp/tear-sheet/relationships.txt`

## Sections

Listed in priority order. See "Page Budget & Cut Order" below for explicit cut guidance.

### 1. Company Header
Key-value block with transaction-relevant identifiers.

| Field | Notes |
|---|---|
| Company name | Large, bold |
| Ticker & Exchange | If public; omit for private |
| HQ Location | City, State/Country |
| Founded | Year |
| Employees | Approximate headcount |
| Market Cap / Valuation | Market cap if public; latest known valuation if private |
| Enterprise Value | |
| Ownership | Public / PE-backed (name sponsor) / Family / Other |

For private companies: note "Private Company" prominently; skip ticker, exchange.

### 2. Business Overview
**This is a pitchbook paragraph, not a CIQ summary.** Do not paste the company description from the data tools. Rewrite in 4-6 sentences using pitchbook prose:
- Characterize the revenue model (recurring vs. transactional, subscription vs. license)
- Name the customer base at scale ("serves 80% of Fortune 500 banks")
- Identify competitive moats by name ("proprietary dataset of X", "only provider with Y")
- Frame growth vectors that would matter to a buyer or seller

The tone should be confident and specific. A banker reading this paragraph should immediately understand the company's strategic positioning.

### 3. Revenue & Segment Breakdown
Revenue by business unit or product line.

| Segment | Revenue ($M) | % of Total | YoY Growth |
|---|---|---|---|
| [Segment A] | | | |
| [Segment B] | | | |
| **Total** | | **100%** | |

**If segment data isn't available:** Replace the table with 2-3 sentences describing the revenue mix qualitatively (e.g., "Revenue is primarily derived from subscription licenses (~70%) and professional services (~30%)."). A blank table looks broken — a qualitative description still conveys useful information.

### 4. Financial Summary (3-Year + LTM)
Actual fiscal years as column headers. **If LTM (last twelve months) data is available, add an LTM column to the right of the most recent fiscal year.** Label it "LTM [quarter end date]" (e.g., "LTM Q3 2025"). Bankers work off LTM for valuation cross-checks — a fiscal-year-only view can be 6+ months stale.

| Metric ($M) | FY20XX | FY20XX | FY20XX | LTM [date] |
|---|---|---|---|---|
| Revenue | | | | |
| Revenue Growth % | | | | |
| Gross Profit | | | | |
| Gross Margin % | | | | |
| EBITDA | | | | |
| EBITDA Margin % | | | | |
| Operating Income | | | | |
| Net Income | | | | |
| Capex | | | | |
| Free Cash Flow | | | | |
| FCF Margin % | | | | |

In M&A context, margins and FCF conversion matter as much as absolute scale — a buyer is evaluating efficiency and cash generation potential.

**Capital Structure** (compact sub-table below the financial summary):

| Metric | Value |
|---|---|
| Total Debt | $XXM |
| Cash & Equivalents | $XXM |
| Net Debt | $XXM |
| Net Debt / EBITDA | X.Xx |
| S&P Credit Rating | XX (if available) |

Pull from the balance sheet data already retrieved. This is standard in any banker's company profile — total debt, leverage ratio, and credit rating tell a buyer what the financing picture looks like. If credit rating is unavailable, omit that row.

### 5. Trading Comps
Company multiples **and operating metrics** — bankers use these together, not multiples in isolation.

**Forward multiples are mandatory when available.** The table must include NTM multiples if the tools return them. Showing only trailing multiples when forward data exists is a significant gap — bankers price deals on forward earnings.

**Peer columns are expected.** If the user provided comps, each gets its own column. If not, use the competitors tool to identify 3-5 public peers, pull their multiples and operating metrics, and include them. A company-only trading comps table without peer context is incomplete for any banking use case.

| Metric | [Company] | [Comp 1] | [Comp 2] | [Comp 3] | Peer Median |
|---|---|---|---|---|---|
| EV/Revenue (NTM) | | | | | |
| EV/EBITDA (NTM) | | | | | |
| Revenue Growth % | | | | | |
| EBITDA Margin % | | | | | |

If only the company's own multiples are available after attempting peer queries, show those and list selected peer names below the table.

For private companies, skip this section.

### 6. M&A Activity
Two parts. **Deal values are expected in this section** — bankers notice when they're missing.

**Hard rule: If the M&A tools return a transaction value, it must appear in the output.** Never downgrade a known deal value to "Undisclosed" — this is a data integrity violation. Use "Undisclosed" only when the tools genuinely return no value for a transaction.

**a) Company's Own Transactions:**

**The table must include a dedicated Deal Value column.** Do not merge deal values into a Notes or Rationale column — bankers scan for numbers, and a dedicated column enables that.

| Date | Target / Divested | Deal Value ($M) | Type | Rationale |
|---|---|---|---|---|
| | | | Acquisition / Divestiture | |

If none found: "No disclosed transactions in the last 5 years."

**b) Comparable Sector Transactions (data permitting):**
Use the specific industry identified earlier (e.g., "cloud infrastructure software M&A" not "technology M&A"). If the user specified comps, also look for transactions involving those specific companies.

| Date | Target | Acquirer | EV ($M) | EV/Rev | EV/EBITDA |
|---|---|---|---|---|---|

If not available from the tools: "Comparable transaction data not available from data source." Do not fabricate precedent multiples.

### 7. Key Business Relationships
Leverages S&P Capital IQ relationship data. Group by type:

**Customers:** Top 3-5 named clients
**Suppliers:** Key vendors and technology providers
**Partners:** Strategic alliances, distribution, JVs
**Competitors:** Key competitive names

For each entry, include the relationship type and a parenthetical descriptor explaining the nature of the relationship (e.g., "AWS — cloud infrastructure (primary hosting provider)", "JPMorgan — customer (enterprise analytics platform)"). A name alone without context isn't useful. Give this section breathing room — it's strategically valuable and most competing tear sheets lack it.

### 8. Ownership Snapshot (data permitting — omit if tools return nothing)
If the tools return institutional ownership, insider ownership percentage, or top holders, include a compact block:

Top institutional holders (if available): list top 3-5 by ownership %.
Insider ownership: aggregate percentage.

For PE-backed companies, name the sponsor, acquisition year, and ownership stake. Ownership structure directly affects deal complexity — a widely held public company, a founder-controlled company, and a PE-backed company each require fundamentally different deal approaches.

If ownership data is not returned by the tools, omit this section entirely rather than showing placeholders.

**Do not include a Management Team table.** No S&P Global tool returns executive data — see Data Integrity Rule 10. Management names from training data will be stale.

## Page Budget & Cut Order

**Target: 2 pages maximum.** IB profiles can use both pages fully, but must not spill to a third. If content exceeds 2 pages, cut in this order (cut each completely before moving to the next):

1. Ownership Snapshot (section 8) — omit entirely
2. Comparable Sector Transactions (section 6b) — keep company's own M&A, cut precedents
3. Business Relationships (section 7) — compress to top 3 competitors + top 2 each of suppliers/partners/customers, drop descriptors to parenthetical only
4. Capital Structure (section 4) — merge Net Debt/EBITDA into Financial Summary as a single row
5. Trading Comparables (section 5) — reduce to 3 peers

Never cut: Business Overview (2), Revenue & Segment Breakdown (3), Financial Summary (4 core), M&A Activity company transactions (6a).

## Formatting Notes
- Business Overview and Segment Breakdown get the most visual weight.
- **M&A Activity is the signature section:** Use Accent color (#2E75B6) fill with white bold text for M&A table headers — this is the only table that uses a different header color from the standard #D6E4F0. It should catch the eye on a scan.
- **Business Relationships: give breathing room when space permits.** 6pt between each relationship group, full descriptors on each entry. But if hitting page 3, compress per the cut order above — this section is high-value but also the most compressible.
- For private companies, the header, business overview, financials, and relationships form the core; other sections may be sparse.
- **Two-page discipline:** Before rendering, mentally estimate page count. If Business Relationships + M&A Activity together will exceed one full page, start cutting per the cut order.

### Referencia: references/sales-bd.md

# Sales / Business Development Tear Sheet

## Purpose
A briefing document to prepare a sales or BD team for a client meeting. Emphasis on understanding the prospect's business, what leadership is publicly prioritizing, and identifying angles to connect your product/service to their needs. Financials are simplified to scale and trajectory.

This is the most narrative-driven tear sheet type. It reads like a briefing memo, not a data sheet.

**Default page length:** 1-2 pages. No strict convention — prioritize readability over compression.

## Query Plan

Start with these queries. Follow up if results are incomplete.

**Query 1 — Company profile + financials:**
"[Company] business description overview products services headquarters employees sector industry revenue gross margin last 2 fiscal years"
→ Header, Company Overview, Financial Snapshot
→ **Immediately write** to `/tmp/tear-sheet/company-profile.txt`
→ **Immediately write** raw financials to `/tmp/tear-sheet/financials.csv`

**Query 2 — Strategy + earnings:**
"[Company] most recent earnings call strategic priorities CEO commentary guidance key initiatives"
→ Strategic Priorities
→ **Immediately write** to `/tmp/tear-sheet/earnings.txt`

**Query 3 — Relationships + news:**
"[Company] key customers suppliers partners competitors business relationships recent acquisitions partnerships announcements"
→ Key Relationships, Recent News
→ **Immediately write** to `/tmp/tear-sheet/relationships.txt`

Three queries is usually sufficient. For well-known companies, these return rich results. For smaller or private companies, Queries 2 and 3 may be sparse — that's fine. The qualitative sections still deliver value because Claude synthesizes whatever is available into useful framing.

## Sections

Listed in priority order. Cut from the bottom if space is constrained.

### 1. Company Header
Streamlined — identification only, no valuation metrics.

| Field | Notes |
|---|---|
| Company name | Large, bold |
| Ticker & Exchange | If public; omit for private |
| HQ | City, State/Country |
| Industry / Sector | |
| Employees | |
| Annual Revenue (latest) | Round to nearest $B or $M |
| Market Cap | If public; omit for private |
| FY Revenue Guidance | If available from earnings data; e.g., "6–8% organic growth" |
| FY EPS or EPS Guidance | If public company; pull from `earnings.txt` |
| Key Financial Metric | Adj. EPS, EBITDA margin, or similar — one headline number |

Forward guidance and EPS data come from Query 2 (earnings) — source from `earnings.txt` when populating the header, not just `company-profile.txt`.

One horizontal band at the top. No enterprise value, no beta — this audience doesn't need them.

### 2. Company Overview
The most important section. A sales rep should read this and walk into a meeting with a solid grasp of the prospect.

**Do not paste the CIQ company summary.** It reads like an SEC filing and will lose a non-finance audience. Rewrite in 3-5 sentences of plain language:
- What the company does (no investor jargon — say "sells" not "monetizes", say "yearly revenue" not "top-line CAGR")
- Who their customers are
- How they make money
- Where they operate
- What makes them distinctive

Write in prose paragraphs. A non-finance person should understand every sentence.

### 3. Strategic Priorities & Management Commentary
What is leadership focused on right now? If you know what the CEO is talking about, you can align your pitch.

**This is NOT an earnings recap.** Do not reuse the same bullets as the equity research tear sheet. Extract 3-5 *strategic themes* with thematic labels and supporting data points:

- **AI/Data Monetization:** Management is investing aggressively in AI capabilities, allocating $X to R&D in FY2024 and launching three new AI-powered products.
- **Margin Expansion:** CEO cited operational efficiency as a top priority, targeting 200bps of operating margin improvement through automation.
- **International Growth:** Opening new offices in EMEA; Europe now represents 25% of revenue, up from 18%.

Each bullet should answer: "What does this company care about right now, and what evidence supports it?" A sales rep should read these and immediately see angles to connect their product.

If earnings call data isn't available (common for private companies), replace with "Recent Developments" pulling from whatever news or announcements the tools return.

### 4. Financial Snapshot
Simplified. Single compact table — just scale, direction, and one profitability signal. A sales rep needs to know three things: how big is this company, is it growing, and is it healthy.

| Metric | FY[prior year] | FY[latest] | YoY Change |
|---|---|---|---|
| Revenue | | | +X% |
| Gross Margin % | | | +X.Xpp |
| Employees | | | |

Three rows maximum. No EBITDA, no EV multiples, no balance sheet, no net income. Gross margin (not EBITDA, not net income) is the right single profitability metric for a sales audience — it's intuitive ("how much they keep after direct costs") and signals business health without requiring finance literacy. If the rep needs deeper financials, they can request the equity research version.

For private companies, this table may have only revenue and employees — two data points showing scale and growth are enough for a sales meeting.

### 5. Key Relationships & Ecosystem
Helps reps understand the prospect's world and identify angles.

Four labeled lists, 3-5 names each with one-line descriptors:

**Customers:** Who they sell to. Helps understand their go-to-market and shared target customers.
Example: "JPMorgan Chase — customer (enterprise analytics platform deployment)"

**Vendors / Technology:** What they buy. Identifies displacement or integration opportunities.
Example: "AWS — vendor (primary cloud infrastructure); Snowflake — vendor (data warehouse)"

**Partners:** Who they work with. Co-sell angles, mutual connections.
Example: "Deloitte — partner (implementation for enterprise clients)"

**Competitors:** Who they compete against. Positioning context.
Example: "Bloomberg — competitor (financial data terminal)"

Every entry needs a parenthetical descriptor so the rep understands *what* the relationship means, not just *who*.

If relationship data isn't available, note "Relationship data not available" and move on.

### 6. Recent News & Developments
3-5 bullets, each one sentence, most recent first. Include date if available. **Lead with the latest earnings report** — it's the most important recent event for a sales meeting and sets the context for everything else. Then: M&A, product launches, leadership changes, major wins.

**Include upcoming catalysts at the end of the section** with a "**Coming Up:**" label. Examples: upcoming earnings dates, pending divestitures, product launches, investor days, regulatory milestones. These create natural engagement windows for sales outreach and are often the best reason to reach out ("I noticed you have your Investor Day coming up in Q2..."). Pull from earnings call commentary and M&A data (pending transactions).

### 7. Conversation Starters (cut first)
2-3 suggested talking points synthesized from the data above. **Each starter must reference a specific strategic priority from Section 3** — generic questions are useless. Frame as questions.

**Tag each starter with a suggested persona** — e.g., (CTO), (CFO), (CDO), (Head of Data), (VP Engineering), (Head of Procurement). A rep meeting with a CTO needs a different opener than one meeting with a CFO. If the user specified who they're meeting with, generate starters for that persona only.

Examples:
- *(CTO/CDO)* "You mentioned [specific AI initiative from Section 3] on your last earnings call — how is that impacting your [relevant need]?"
- *(CFO/COO)* "With your [margin expansion target from Section 3], are you evaluating tools that could accelerate that timeline?"
- *(VP Strategy/Corp Dev)* "I noticed [Company] recently acquired [target] — does that change your approach to [capability]?"

If the user described what product/service they're selling, tailor these to connect the prospect's priorities to that offering. If not, keep them grounded in the prospect's strategic themes but generic in solution framing.

**Validation test:** Before finalizing each conversation starter, verify it contains at least one specific number, date, product name, or initiative name drawn from the tear sheet. A question that could apply to any company in the sector is not a good conversation starter. "How are you thinking about AI?" is generic. "Your CEO mentioned $1B in AI investment since 2018 and 20% adoption of the iLEVEL auto-ingestion feature — how is that changing your analysts' workflows?" is specific and demonstrates preparation.

This section is Claude's synthesis, not raw data from the tools. Label it clearly.

## Formatting Notes
- **This should be the warmest, most readable tear sheet.** Rigorous content, but the formatting should feel like a briefing memo, not a data terminal.
- Body text: use the full 9pt (size: 18). No compression — readability over density.
- Line spacing: 1.15x on body paragraphs (slightly more generous than default). This template is the one where whitespace is a feature, not waste.
- Company Overview and Strategic Priorities should take ~40-50% of the page.
- Financial Snapshot: visually compact, secondary prominence. Keep it small and clean.
- Key Relationships: consider two-column layout (Customers + Vendors on left, Partners + Competitors on right) to save vertical space while keeping descriptors visible.
- Conversation Starters: use the indented block-style bullets. These are the payoff of the document — they should stand out visually.


---

## SKILL: thesis-tracker

- Fuente: `anthropics/financial-services` → `plugins/vertical-plugins/equity-research/skills/thesis-tracker` (Apache-2.0)
- Cuándo usarla: Maintain and update investment theses for portfolio positions and watchlist names. Track key data points, catalysts, and thesis milestones over time. Use when updating a thesis with new information, reviewing position rationale, or checking if a thesis is still intact. Triggers on "update thesis for [company]", "is my thesis still intact", "thesis check", "add data point to [company]", or "review my positions".

# Thesis Tracker

## Workflow

### Step 1: Define or Load Thesis

If creating a new thesis:
- **Company**: Name and ticker
- **Position**: Long or Short
- **Thesis statement**: 1-2 sentence core thesis (e.g., "Long ACME — margin expansion from pricing power + operating leverage as mix shifts to software")
- **Key pillars**: 3-5 supporting arguments
- **Key risks**: 3-5 risks that would invalidate the thesis
- **Catalysts**: Upcoming events that could prove/disprove the thesis (earnings, product launches, regulatory decisions)
- **Target price / valuation**: What's it worth if the thesis plays out
- **Stop-loss trigger**: What would make you exit

If updating an existing thesis, ask the user for the new data point or development.

### Step 2: Update Log

For each new data point or development:

- **Date**: When this happened
- **Data point**: What changed (earnings beat, management departure, competitor move, etc.)
- **Thesis impact**: Does this strengthen, weaken, or neutralize a specific pillar?
- **Action**: No change / Increase position / Trim / Exit
- **Updated conviction**: High / Medium / Low

### Step 3: Thesis Scorecard

Maintain a running scorecard:

| Pillar | Original Expectation | Current Status | Trend |
|--------|---------------------|----------------|-------|
| Revenue growth >20% | On track | Q3 was 22% | Stable |
| Margin expansion | Behind | Margins flat YoY | Concerning |
| New product launch | Pending | Delayed to Q2 | Watch |

### Step 4: Catalyst Calendar

Track upcoming catalysts:

| Date | Event | Expected Impact | Notes |
|------|-------|-----------------|-------|
| | | | |

### Step 5: Output

Thesis summary suitable for:
- Morning meeting discussion
- Portfolio review
- Risk committee presentation

Format: Concise markdown or Word doc with the scorecard, recent updates, and current conviction level.

## Important Notes

- A thesis should be falsifiable — if nothing could disprove it, it's not a thesis
- Track disconfirming evidence as rigorously as confirming evidence
- Review theses at least quarterly, even when nothing dramatic has happened
- If the user manages multiple positions, offer to do a full portfolio thesis review
- Store thesis data in a structured format so it can be referenced across sessions


---

## SKILL: time-value-of-money

- Fuente: `JoelLewis/finance_skills` → `plugins/core/skills/time-value-of-money` (MIT)
- Cuándo usarla: Calculate present value, future value, NPV, IRR for projects and loans, loan payments, and amortization schedules across all compounding conventions. Use when the user asks about discounting cash flows, valuing an annuity or perpetuity, comparing investments with different timing, building a mortgage amortization table, evaluating whether a project is worth pursuing, or solving for the rate that equates cash flows (project IRR, loan IRR, yield on an investment). Also trigger when users mention 'what is it worth today', 'how much will I have in 20 years', 'monthly payment on a loan', 'discount rate', 'Gordon growth model', 'effective annual rate', 'continuous compounding', or ask how to compare a lump sum versus a stream of payments. For portfolio money-weighted return (dollar-weighted IRR on an investor's contributions and withdrawals), use return-calculations instead.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/core/skills/time-value-of-money/` (time_value_of_money.py)

# Time Value of Money

## Core Concepts

### Future Value (FV)
The value of a present sum after earning interest for `n` periods at rate `r` per period.

$$FV = PV \times (1 + r)^n$$

Future value grows exponentially with time, which is the mathematical basis of compound interest.

### Present Value (PV)
The current worth of a future sum, discounted back at rate `r` for `n` periods. This is the inverse of future value.

$$PV = \frac{FV}{(1 + r)^n}$$

Present value is the cornerstone of all valuation: a dollar today is worth more than a dollar tomorrow because of the opportunity cost of capital.

### Compounding Conventions
Interest can compound at different frequencies. The nominal annual rate `r_nom` compounded `m` times per year produces different effective yields.

**Discrete compounding (m times per year):**

$$FV = PV \times \left(1 + \frac{r_{nom}}{m}\right)^{m \times t}$$

**Continuous compounding:**

$$FV = PV \times e^{r \times t}$$

**Effective Annual Rate (EAR):**

$$EAR = \left(1 + \frac{r_{nom}}{m}\right)^m - 1$$

For continuous compounding: `EAR = e^(r_nom) - 1`

Common frequencies:
| Frequency | m |
|-----------|---|
| Annual | 1 |
| Semi-annual | 2 |
| Quarterly | 4 |
| Monthly | 12 |
| Daily | 365 |
| Continuous | infinity |

### Ordinary Annuity
A series of equal payments made at the **end** of each period for `n` periods.

**Present Value:**

$$PV = PMT \times \frac{1 - (1 + r)^{-n}}{r}$$

**Future Value:**

$$FV = PMT \times \frac{(1 + r)^n - 1}{r}$$

### Annuity Due
A series of equal payments made at the **beginning** of each period. Each cash flow is one period closer than in an ordinary annuity, so values are scaled by `(1 + r)`.

**Present Value:**

$$PV = PMT \times \frac{1 - (1 + r)^{-n}}{r} \times (1 + r)$$

**Future Value:**

$$FV = PMT \times \frac{(1 + r)^n - 1}{r} \times (1 + r)$$

### Growing Annuity
A finite series of payments that grow at a constant rate `g` per period, where `g != r`.

**Present Value:**

$$PV = \frac{PMT}{r - g} \times \left[1 - \left(\frac{1 + g}{1 + r}\right)^n\right]$$

This is widely used in equity valuation (e.g., multi-stage dividend discount models) and salary/pension projections.

### Perpetuity
An infinite stream of equal payments.

$$PV = \frac{PMT}{r}$$

### Growing Perpetuity
An infinite stream of payments growing at constant rate `g`, where `g < r` for convergence.

$$PV = \frac{PMT}{r - g}$$

This is the Gordon Growth Model when applied to dividends.

### Net Present Value (NPV)
The sum of all discounted cash flows, including the initial investment. A positive NPV indicates value creation.

$$NPV = \sum_{t=0}^{T} \frac{CF_t}{(1 + r)^t}$$

Typically, `CF_0` is a negative outflow (initial investment), and subsequent `CF_t` are inflows.

### Internal Rate of Return (IRR)
The discount rate `r` that makes the NPV of all cash flows exactly zero.

$$0 = \sum_{t=0}^{T} \frac{CF_t}{(1 + r)^t}$$

IRR is solved numerically (Newton-Raphson or bisection) since there is no closed-form solution for general cash flow streams. For conventional cash flows (one sign change), a unique IRR exists.

### Amortization
Each payment on an amortizing loan is split into an interest component and a principal component:

- **Interest portion:** `Interest_t = Balance_{t-1} * r`
- **Principal portion:** `Principal_t = PMT - Interest_t`
- **Remaining balance:** `Balance_t = Balance_{t-1} - Principal_t`

Over time, the interest portion decreases and the principal portion increases.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Future Value | `FV = PV * (1 + r)^n` | Compound a lump sum forward |
| Present Value | `PV = FV / (1 + r)^n` | Discount a future lump sum |
| EAR | `(1 + r_nom/m)^m - 1` | Compare rates across compounding frequencies |
| Continuous FV | `FV = PV * e^(r*t)` | Continuous compounding |
| Ordinary Annuity PV | `PMT * [1 - (1+r)^(-n)] / r` | Loan payments, lease valuation |
| Annuity Due PV | `PMT * [1 - (1+r)^(-n)] / r * (1+r)` | Rent, insurance (paid in advance) |
| Growing Annuity PV | `PMT/(r-g) * [1 - ((1+g)/(1+r))^n]` | Salary streams, growing dividends |
| Perpetuity PV | `PMT / r` | Preferred stock, consol bonds |
| Growing Perpetuity PV | `PMT / (r - g)` | Gordon Growth Model |
| NPV | `sum(CF_t / (1+r)^t)` | Project/investment evaluation |
| IRR | `solve: sum(CF_t / (1+r)^t) = 0` | Return metric for uneven cash flows |

## Worked Examples

### Example 1: Monthly Mortgage Payment
**Given:** A $300,000 mortgage at a 6.5% annual interest rate, fixed for 30 years, with monthly payments (ordinary annuity).

**Calculate:** The monthly payment amount.

**Solution:**

First, convert the annual rate to a monthly rate and years to months:
```
r_monthly = 0.065 / 12 = 0.00541667
n = 30 * 12 = 360 months
```

Using the ordinary annuity present value formula, solve for PMT:
```
PV = PMT * [1 - (1 + r)^(-n)] / r

300,000 = PMT * [1 - (1.00541667)^(-360)] / 0.00541667
```

Compute the annuity factor:
```
(1.00541667)^360 = 6.99179
(1.00541667)^(-360) = 0.143010
1 - 0.143010 = 0.856990
0.856990 / 0.00541667 = 158.2108
```

Solve for PMT:
```
PMT = 300,000 / 158.2108 = $1,896.20
```

The monthly mortgage payment is **$1,896.20**.

Over 30 years, total payments = `360 * $1,896.20 = $682,632`, meaning total interest paid is `$682,632 - $300,000 = $382,632`.

### Example 2: NPV of a Project with Uneven Cash Flows
**Given:** A project requires an initial investment of $50,000 and produces the following cash flows:
- Year 1: $12,000
- Year 2: $15,000
- Year 3: $18,000
- Year 4: $22,000
- Year 5: $25,000

The required rate of return (discount rate) is 10%.

**Calculate:** The NPV and whether the project should be accepted.

**Solution:**

Discount each cash flow to present value:
```
PV(CF_0) = -50,000 / (1.10)^0 = -50,000.00
PV(CF_1) =  12,000 / (1.10)^1 =  10,909.09
PV(CF_2) =  15,000 / (1.10)^2 =  12,396.69
PV(CF_3) =  18,000 / (1.10)^3 =  13,523.67
PV(CF_4) =  22,000 / (1.10)^4 =  15,026.30
PV(CF_5) =  25,000 / (1.10)^5 =  15,523.03
```

Sum all present values:
```
NPV = -50,000.00 + 10,909.09 + 12,396.69 + 13,523.67 + 15,026.30 + 15,523.03
NPV = +$17,378.78
```

Since NPV is **positive ($17,378.78)**, the project creates value and should be accepted. It earns more than the 10% required rate of return.

To find the IRR, we would solve for the rate where NPV = 0. Numerically, the IRR for this cash flow stream is approximately **21.2%** (21.18%), well above the 10% hurdle rate.

## Common Pitfalls
- Mismatching rate and period frequency: if payments are monthly, the discount rate must be a monthly rate. Divide the annual nominal rate by 12, do not take the 12th root of `(1 + annual rate)` unless converting from EAR.
- Forgetting the sign convention for cash flows in IRR: outflows (investments) must be negative and inflows (returns) positive, or vice versa, but the convention must be consistent. Incorrect signs produce meaningless IRR results.
- Confusing nominal vs effective rates: a 12% nominal rate compounded monthly produces an EAR of 12.68%, not 12%. Always clarify the compounding basis.
- Off-by-one errors in annuity due vs ordinary annuity: an annuity due shifts all payments one period earlier. Forgetting the `(1 + r)` adjustment factor will undervalue annuity-due streams.
- Multiple IRR solutions with non-conventional cash flows: when cash flows change sign more than once (e.g., initial outflow, inflows, then a large terminal outflow), Descartes' rule allows up to as many positive real IRR solutions as there are sign changes. In such cases, use NPV profiling or the Modified IRR (MIRR) instead.

## Running the Script
`scripts/time_value_of_money.py` implements every formula above as static methods on a `TimeValueOfMoney` class (`present_value`, `future_value`, `npv`, `irr`, `annuity_pv`, `annuity_fv`, `growing_annuity_pv`, `perpetuity_pv`, `fisher_rate`, `continuous_compounding`) plus an `AmortizationSchedule` class.

- Run: `uv run scripts/time_value_of_money.py` (PEP 723 inline metadata; stdlib-only, no third-party dependencies), or simply `python3 scripts/time_value_of_money.py`.
- Bare invocation (or `--verify`) prints a demo of all methods **and** asserts the worked-example values above (Example 1 mortgage payment = $1,896.20; Example 2 NPV = $17,378.78 and IRR = 21.18%), exiting nonzero on any mismatch.
- `--help` lists the available methods and import usage.
- For programmatic use, import rather than run: `from time_value_of_money import TimeValueOfMoney, AmortizationSchedule`, then call e.g. `TimeValueOfMoney.npv(...)`.

## Cross-References
- **return-calculations** (core plugin): CAGR is a special case of compound growth; portfolio MWR uses the same NPV=0 framework and lives there
- **statistics-fundamentals** (core plugin): Discount rate estimation often relies on regression (CAPM beta) and distributional assumptions


---

## SKILL: trade-hypothesis-ideator

- Fuente: `tradermonty/claude-trading-skills` → `skills/trade-hypothesis-ideator` (MIT)
- Cuándo usarla: >
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/trade-hypothesis-ideator/` (example_input.json, example_output.json, sample_input.json, requirements.txt, hypothesis_card.schema.json, input_bundle.schema.json, output_bundle.schema.json, raw_hypotheses.schema.json, __init__.py, evidence_extractor.py, format_output.py, normalize.py …)

# Trade Hypothesis Ideator

Generate 1-5 structured hypothesis cards from a normalized input bundle, critique and rank them, then optionally export `pursue` cards into `strategy.yaml` + `metadata.json` artifacts.

## When to Use

- After gathering trade logs, journal entries, or market observations that suggest a potential edge
- When you have a structured input bundle (JSON) with evidence snippets and want falsifiable hypotheses
- To bridge qualitative observations into quantitative experiment designs
- Before committing capital to validate a new strategy idea with kill criteria

## Prerequisites

- Input JSON bundle with one or more of: `trade_log`, `journal_snippets`, `market_data`, `observations`
- Python 3.9+ with `pyyaml` installed
- No external API keys required (pure calculation skill)

## Workflow

1. Receive input JSON bundle.
2. Run pass 1 normalization + evidence extraction.
3. Generate hypotheses with prompts:
   - `prompts/system_prompt.md`
   - `prompts/developer_prompt_template.md` (inject `{{evidence_summary}}`)
4. Critique hypotheses with `prompts/critique_prompt_template.md`.
5. Run pass 2 ranking + output formatting + guardrails.
6. Optionally export `pursue` hypotheses via Step H strategy exporter.

## Scripts

- Pass 1 (evidence summary):

```bash
python3 skills/trade-hypothesis-ideator/scripts/run_hypothesis_ideator.py \
  --input skills/trade-hypothesis-ideator/examples/example_input.json \
  --output-dir reports/
```

- Pass 2 (rank + output + optional export):

```bash
python3 skills/trade-hypothesis-ideator/scripts/run_hypothesis_ideator.py \
  --input skills/trade-hypothesis-ideator/examples/example_input.json \
  --hypotheses reports/raw_hypotheses.json \
  --output-dir reports/ \
  --export-strategies
```

## Output

- `hypothesis_cards_<date>.json` — Ranked hypothesis cards with verdicts (`pursue`, `revise`, `discard`)
- `hypothesis_cards_<date>.md` — Human-readable summary with experiment designs and kill criteria
- `strategy_<hypothesis_id>.yaml` — (Optional) Edge-finder-compatible strategy export for `pursue` cards
- `metadata_<hypothesis_id>.json` — (Optional) Provenance metadata for exported strategies

## Resources

- `references/hypothesis_types.md` — Taxonomy of hypothesis patterns (mean-reversion, momentum, event-driven, etc.)
- `references/evidence_quality_guide.md` — Criteria for rating evidence strength and sample size requirements

### Referencia: prompts/critique_prompt_template.md

Review each hypothesis card critically.

For each card:
- Point out unsupported claims.
- Flag overfitting and execution realism risks.
- Check whether kill criteria are objective and measurable.
- Suggest a tighter minimum viable experiment when possible.

Return concise critique bullets per hypothesis_id.

### Referencia: prompts/developer_prompt_template.md

## Objective
Generate 1-5 high-quality trade hypothesis cards for iterative testing.

## Evidence Summary
{{evidence_summary}}

## Output Requirements
Return JSON with top-level key `hypotheses`.
Each hypothesis must include all required fields from `schemas/hypothesis_card.schema.json`.
Focus on:
- clear mechanism
- testability with available features
- explicit invalidation and constraints-awareness

### Referencia: prompts/system_prompt.md

You are a trading strategy hypothesis ideation engine.

Produce 1-5 falsifiable hypothesis cards from structured evidence.

Hard requirements:
- Use only evidence provided in the input context.
- Avoid certainty claims and avoid banned phrases.
- Define explicit kill criteria and minimum viable experiment.
- Keep recommendation strictly in {pursue, park, reject}.
- Keep score_components each in [1, 5].

### Referencia: references/evidence_quality_guide.md

# Evidence Quality Guide

Use this lightweight rubric when assembling evidence basis items.

## Source Weights (qualitative)
- High: validated trade logs, reproducible backtest outputs, auditable fills
- Medium: structured journal snippets with explicit outcomes, repeated chart observations
- Low: one-off anecdotes, unconstrained intuition, non-reproducible screenshots

## Checklist
- Prefer evidence that can be traced to a concrete source.
- Distinguish signal from regime-specific noise.
- Include at least one falsifiable counter-condition in kill criteria.
- Penalize hypotheses that require unavailable features or unsupported data granularity.

### Referencia: references/hypothesis_types.md

# Hypothesis Types

## Mapping to entry_family
- `breakout` -> `pivot_breakout` (exportable)
- `earnings_drift` / `gap_continuation` -> `gap_up_continuation` (exportable)
- `momentum` / `pullback` / `regime_shift` -> `research_only` (not exportable in v1)

## Notes
- `edge-finder-candidate/v1` supports only `pivot_breakout` and `gap_up_continuation`.
- `gap_open_scored` is treated as research-only until v2 support is added.


---

## SKILL: us-stock-analysis

- Fuente: `tradermonty/claude-trading-skills` → `examples/weekly-trade-strategy/.claude/skills/us-stock-analysis` (MIT)
- Cuándo usarla: Comprehensive US stock analysis including fundamental analysis (financial metrics, business quality, valuation), technical analysis (indicators, chart patterns, support/resistance), stock comparisons, and investment report generation. Use when user requests analysis of US stock tickers (e.g., "analyze AAPL", "compare TSLA vs NVDA", "give me a report on Microsoft"), evaluation of financial metrics, technical chart analysis, or investment recommendations for American stocks.

# US Stock Analysis

## Overview

Perform comprehensive analysis of US stocks covering fundamental analysis (financials, business quality, valuation), technical analysis (indicators, trends, patterns), peer comparisons, and generate detailed investment reports. Fetch real-time market data via web search tools and apply structured analytical frameworks.

## Data Sources

Always use web search tools to gather current market data:

**Primary Data to Fetch:**
1. **Current stock price and trading data** (price, volume, 52-week range)
2. **Financial statements** (income statement, balance sheet, cash flow)
3. **Key metrics** (P/E, EPS, revenue, margins, debt ratios)
4. **Analyst ratings and price targets**
5. **Recent news and developments**
6. **Peer/competitor data** (for comparisons)
7. **Technical data** (moving averages, RSI, MACD when available)

**Search Strategy:**
- Use ticker symbol + specific data needed (e.g., "AAPL financial metrics 2024")
- For comprehensive data: Search for earnings reports, investor presentations, or SEC filings
- For technical data: Search for "AAPL technical analysis" or use financial data sites
- Always verify data recency (prefer data from last quarter)

**Quality Sources:**
- Yahoo Finance, Google Finance, MarketWatch, Seeking Alpha, Bloomberg, CNBC
- Company investor relations pages
- SEC filings (10-K, 10-Q) for detailed financials
- TradingView, StockCharts for technical data

## Analysis Types

This skill supports four types of analysis. Determine which type(s) the user needs:

1. **Basic Stock Info** - Quick overview with key metrics
2. **Fundamental Analysis** - Deep dive into business, financials, valuation
3. **Technical Analysis** - Chart patterns, indicators, trend analysis
4. **Comprehensive Report** - Complete analysis combining all approaches

## Analysis Workflows

### 1. Basic Stock Information

**When to Use:** User asks for quick overview or basic info

**Steps:**
1. Search for current stock data (price, volume, market cap)
2. Gather key metrics (P/E, EPS, revenue growth, margins)
3. Get 52-week range and year-to-date performance
4. Find recent news or major developments
5. Present in concise summary format

**Output Format:**
- Company description (1-2 sentences)
- Current price and trading metrics
- Key valuation metrics (table)
- Recent performance
- Notable recent news (if any)

### 2. Fundamental Analysis

**When to Use:** User wants financial analysis, valuation assessment, or business evaluation

**Steps:**
1. **Gather comprehensive financial data:**
   - Revenue, earnings, cash flow (3-5 year trends)
   - Balance sheet metrics (debt, cash, working capital)
   - Profitability metrics (margins, ROE, ROIC)

2. **Read references/fundamental-analysis.md** for analytical framework

3. **Read references/financial-metrics.md** for metric definitions and calculations

4. **Analyze business quality:**
   - Competitive advantages
   - Management track record
   - Industry position

5. **Perform valuation analysis:**
   - Calculate key ratios (P/E, PEG, P/B, EV/EBITDA)
   - Compare to historical averages
   - Compare to peer group
   - Estimate fair value range

6. **Identify risks:**
   - Company-specific risks
   - Market/macro risks
   - Red flags from financial data

7. **Generate output** following references/report-template.md structure

**Critical Analyses:**
- Profitability trends (improving/declining margins)
- Cash flow quality (FCF vs earnings)
- Balance sheet strength (debt levels, liquidity)
- Growth sustainability
- Valuation vs peers and historical average

### 3. Technical Analysis

**When to Use:** User asks for technical analysis, chart patterns, or trading signals

**Steps:**
1. **Gather technical data:**
   - Current price and recent price action
   - Volume trends
   - Moving averages (20-day, 50-day, 200-day)
   - Technical indicators (RSI, MACD, Bollinger Bands)

2. **Read references/technical-analysis.md** for indicator definitions and patterns

3. **Identify trend:**
   - Uptrend, downtrend, or sideways
   - Strength of trend

4. **Locate support and resistance levels:**
   - Recent highs and lows
   - Moving average levels
   - Round numbers

5. **Analyze indicators:**
   - RSI: Overbought (>70) or oversold (<30)
   - MACD: Crossovers and divergences
   - Volume: Confirmation or divergence
   - Bollinger Bands: Squeeze or expansion

6. **Identify chart patterns:**
   - Reversal patterns (head and shoulders, double top/bottom)
   - Continuation patterns (flags, triangles)

7. **Generate technical outlook:**
   - Current trend assessment
   - Key levels to watch
   - Risk/reward analysis
   - Short and medium-term outlook

**Interpretation Guidelines:**
- Confirm signals with multiple indicators
- Consider volume for validation
- Note divergences between price and indicators
- Always identify risk levels (stop-loss)

### 4. Comprehensive Investment Report

**When to Use:** User asks for detailed report, investment recommendation, or complete analysis

**Steps:**
1. **Perform data gathering** (as in Basic Info)

2. **Execute fundamental analysis** (follow workflow above)

3. **Execute technical analysis** (follow workflow above)

4. **Read references/report-template.md** for complete report structure

5. **Synthesize findings:**
   - Integrate fundamental and technical insights
   - Develop bull and bear cases
   - Assess risk/reward

6. **Generate recommendation:**
   - Buy/Hold/Sell rating
   - Target price with timeframe
   - Conviction level
   - Entry strategy

7. **Create formatted report** following template structure

**Report Must Include:**
- Executive summary with recommendation
- Company overview
- Investment thesis (bull and bear cases)
- Fundamental analysis section
- Technical analysis section
- Valuation analysis
- Risk assessment
- Catalysts and timeline
- Conclusion

## Stock Comparison Analysis

**When to Use:** User asks to compare two or more stocks (e.g., "compare AAPL vs MSFT")

**Steps:**
1. **Gather data for all stocks:**
   - Follow data gathering steps for each ticker
   - Ensure comparable timeframes

2. **Read references/fundamental-analysis.md** and references/financial-metrics.md

3. **Create side-by-side comparison:**
   - Business models comparison
   - Financial metrics table (all key ratios)
   - Valuation metrics table
   - Growth rates comparison
   - Profitability comparison
   - Balance sheet strength

4. **Identify relative strengths:**
   - Where each company excels
   - Quantified advantages

5. **Technical comparison:**
   - Relative strength
   - Momentum comparison
   - Which is in better technical position

6. **Generate recommendation:**
   - Which stock is more attractive and why
   - Consider both fundamental and technical factors
   - Portfolio allocation suggestion
   - Risk-adjusted return assessment

**Output Format:** Follow "Comparison Report Structure" in references/report-template.md

## Output Guidelines

**General Principles:**
- Use tables for financial data and comparisons (easy to scan)
- Bold key metrics and findings
- Include data sources and dates
- Quantify whenever possible
- Present both bull and bear perspectives
- Be clear about assumptions and uncertainties

**Formatting:**
- **Headers** for clear section separation
- **Tables** for metrics, comparisons, historical data
- **Bullet points** for lists, factors, risks
- **Bold text** for key findings, important metrics
- **Percentages** for growth rates, returns, margins
- **Currency** formatted consistently ($B for billions, $M for millions)

**Tone:**
- Objective and balanced
- Acknowledge uncertainty
- Support claims with data
- Avoid hyperbole
- Present risks clearly

## Reference Files

Load these references as needed during analysis:

**references/technical-analysis.md**
- When: Performing technical analysis or interpreting indicators
- Contains: Indicator definitions, chart patterns, support/resistance concepts, analysis workflow

**references/fundamental-analysis.md**
- When: Performing fundamental analysis or business evaluation
- Contains: Business quality assessment, financial health analysis, valuation frameworks, risk assessment, red flags

**references/financial-metrics.md**
- When: Need definitions or calculation methods for financial ratios
- Contains: All key metrics with formulas (profitability, valuation, growth, liquidity, leverage, efficiency, cash flow)

**references/report-template.md**
- When: Creating comprehensive report or comparison
- Contains: Complete report structure, formatting guidelines, section templates, comparison format

## Example Queries

**Basic Info:**
- "What's the current price of AAPL?"
- "Give me key metrics for Tesla"
- "Quick overview of Microsoft stock"

**Fundamental:**
- "Analyze NVDA's financials"
- "Is Amazon overvalued?"
- "Evaluate Apple's business quality"
- "What's Google's debt situation?"

**Technical:**
- "Technical analysis of TSLA"
- "Is Netflix oversold?"
- "Show me support levels for AAPL"
- "What's the trend for AMD?"

**Comprehensive:**
- "Complete analysis of Microsoft"
- "Give me a full report on AAPL"
- "Should I invest in Tesla? Give me detailed analysis"

**Comparison:**
- "Compare AAPL vs MSFT"
- "Tesla vs Nvidia - which is better?"
- "Analyze Meta vs Google"

### Referencia: references/financial-metrics.md

# Financial Metrics Reference

## Profitability Metrics

**Gross Profit Margin**
- Formula: (Revenue - COGS) / Revenue × 100
- Measures: Production efficiency and pricing power
- Higher is better; compare to industry average

**Operating Profit Margin**
- Formula: Operating Income / Revenue × 100
- Measures: Operational efficiency
- Excludes financing and tax effects

**Net Profit Margin**
- Formula: Net Income / Revenue × 100
- Measures: Overall profitability after all expenses
- Bottom line efficiency

**Return on Equity (ROE)**
- Formula: Net Income / Shareholders' Equity × 100
- Measures: Profitability relative to shareholder investment
- DuPont Analysis: ROE = Net Margin × Asset Turnover × Equity Multiplier

**Return on Assets (ROA)**
- Formula: Net Income / Total Assets × 100
- Measures: Efficiency in using assets to generate profit

**Return on Invested Capital (ROIC)**
- Formula: NOPAT / Invested Capital × 100
- NOPAT = Net Operating Profit After Tax
- Invested Capital = Total Debt + Total Equity - Cash
- Measures: Return on all capital (debt + equity)

## Valuation Metrics

**Price-to-Earnings (P/E) Ratio**
- Formula: Stock Price / Earnings Per Share
- Trailing P/E: Uses past 12 months earnings
- Forward P/E: Uses estimated future earnings
- Interpretation: Higher P/E = higher growth expectations or overvaluation

**Price-to-Earnings-to-Growth (PEG) Ratio**
- Formula: P/E Ratio / Earnings Growth Rate
- Interpretation: PEG < 1 potentially undervalued; PEG > 1 potentially overvalued

**Price-to-Book (P/B) Ratio**
- Formula: Stock Price / Book Value Per Share
- Book Value = Total Assets - Total Liabilities
- Useful for asset-heavy industries

**Price-to-Sales (P/S) Ratio**
- Formula: Market Cap / Total Revenue
- Useful for unprofitable companies or comparing revenue multiples

**Enterprise Value (EV)**
- Formula: Market Cap + Total Debt - Cash
- Represents total company value

**EV/EBITDA**
- Formula: Enterprise Value / EBITDA
- EBITDA = Earnings Before Interest, Tax, Depreciation, Amortization
- Capital structure neutral valuation metric

**EV/Sales**
- Formula: Enterprise Value / Revenue
- Useful when comparing companies with different profitability

**Dividend Yield**
- Formula: Annual Dividend Per Share / Stock Price × 100
- Measures: Income return from stock

## Growth Metrics

**Revenue Growth Rate**
- Formula: (Current Revenue - Prior Revenue) / Prior Revenue × 100
- YoY (Year-over-Year), QoQ (Quarter-over-Quarter)

**Earnings Per Share (EPS) Growth**
- Formula: (Current EPS - Prior EPS) / Prior EPS × 100
- Track both reported and adjusted EPS

**Compound Annual Growth Rate (CAGR)**
- Formula: (Ending Value / Beginning Value)^(1/Years) - 1
- Smoothed growth rate over multiple years

## Liquidity Metrics

**Current Ratio**
- Formula: Current Assets / Current Liabilities
- Measures: Short-term liquidity
- > 1.5 generally considered healthy

**Quick Ratio (Acid-Test)**
- Formula: (Current Assets - Inventory) / Current Liabilities
- More conservative than current ratio
- > 1.0 generally considered healthy

**Cash Ratio**
- Formula: Cash and Cash Equivalents / Current Liabilities
- Most conservative liquidity measure

## Leverage Metrics

**Debt-to-Equity (D/E) Ratio**
- Formula: Total Debt / Total Equity
- Measures: Financial leverage
- Industry-dependent; lower generally safer

**Debt-to-Assets Ratio**
- Formula: Total Debt / Total Assets
- Shows proportion of assets financed by debt

**Interest Coverage Ratio**
- Formula: EBIT / Interest Expense
- Measures: Ability to pay interest
- > 2.5 generally considered safe

## Efficiency Metrics

**Asset Turnover**
- Formula: Revenue / Average Total Assets
- Measures: Efficiency in using assets to generate sales

**Inventory Turnover**
- Formula: COGS / Average Inventory
- Higher = more efficient inventory management

**Receivables Turnover**
- Formula: Revenue / Average Accounts Receivable
- Days Sales Outstanding (DSO) = 365 / Receivables Turnover

## Cash Flow Metrics

**Free Cash Flow (FCF)**
- Formula: Operating Cash Flow - Capital Expenditures
- Available cash for dividends, buybacks, debt repayment

**FCF Yield**
- Formula: Free Cash Flow Per Share / Stock Price × 100
- Similar to dividend yield but for total cash generation

**Cash Conversion Rate**
- Formula: Free Cash Flow / Net Income
- Should be close to or > 100%
- Lower ratio may indicate earnings quality issues

## Per Share Metrics

**Earnings Per Share (EPS)**
- Formula: Net Income / Weighted Average Shares Outstanding
- Basic EPS vs Diluted EPS (includes options, convertibles)

**Book Value Per Share**
- Formula: (Total Assets - Total Liabilities) / Shares Outstanding

**Cash Flow Per Share**
- Formula: Operating Cash Flow / Shares Outstanding

## Share Metrics

**Shares Outstanding**
- Total shares issued and held by investors
- Track dilution over time

**Float**
- Shares available for public trading
- Excludes insider and restricted shares

**Share Buybacks**
- Track net share reduction/increase
- Buybacks can boost EPS without earnings growth

### Referencia: references/fundamental-analysis.md

# Fundamental Analysis Reference

## Analysis Framework

### 1. Business Quality Assessment

**Competitive Advantages (Moats)**
- Brand strength
- Network effects
- Cost advantages
- Switching costs
- Patents and intellectual property
- Regulatory barriers

**Management Quality**
- Track record of capital allocation
- Insider ownership
- Compensation structure alignment
- Communication transparency

**Business Model**
- Revenue streams diversity
- Scalability
- Margin sustainability
- Customer concentration risk

### 2. Financial Health Analysis

**Profitability Analysis**
- Gross margin trends
- Operating margin trends
- Net margin trends
- Return on Equity (ROE) trends
- Return on Assets (ROA) trends
- Return on Invested Capital (ROIC) trends

**Growth Analysis**
- Revenue growth (YoY, QoQ)
- Earnings growth (YoY, QoQ)
- Free cash flow growth
- Market share trends
- Geographic/segment growth breakdown

**Balance Sheet Strength**
- Debt-to-Equity ratio
- Current ratio
- Quick ratio
- Interest coverage ratio
- Cash position vs debt
- Working capital trends

**Cash Flow Analysis**
- Operating cash flow consistency
- Free cash flow (OCF - CapEx)
- Cash conversion rate
- Capital expenditure trends
- Dividend sustainability

### 3. Valuation Analysis

**Relative Valuation Metrics**
- P/E ratio (vs historical, vs peers, vs sector)
- Forward P/E
- PEG ratio (P/E / growth rate)
- P/B ratio (Price-to-Book)
- P/S ratio (Price-to-Sales)
- EV/EBITDA (Enterprise Value / EBITDA)
- EV/Sales

**Absolute Valuation**
- Discounted Cash Flow (DCF) principles
- Estimate intrinsic value range
- Margin of safety calculation

### 4. Industry and Market Analysis

**Industry Dynamics**
- Industry growth rate
- Industry lifecycle stage
- Competitive landscape
- Barriers to entry
- Regulatory environment
- Technological disruption risk

**Market Position**
- Market share
- Competitive positioning
- Customer loyalty metrics
- Pricing power

### 5. Risk Assessment

**Company-Specific Risks**
- Key person dependency
- Customer concentration
- Supplier concentration
- Product concentration
- Litigation risks
- Regulatory risks

**Market Risks**
- Economic sensitivity
- Interest rate sensitivity
- Currency exposure
- Commodity price exposure

## Analysis Workflow

1. **Understand the business** (what they do, how they make money)
2. **Assess competitive position** (moats, market share)
3. **Analyze financial statements** (trends over 3-5 years)
4. **Calculate key metrics** (profitability, growth, leverage)
5. **Compare to peers** (relative positioning)
6. **Value the company** (multiple approaches)
7. **Identify risks** (company and market level)
8. **Determine investment thesis** (bull and bear cases)

## Red Flags to Watch For

- Declining margins
- Consistently negative or declining free cash flow
- Rising debt without revenue growth
- Frequent non-GAAP adjustments
- High executive turnover
- Customer concentration > 10% from single customer
- Inconsistent accounting changes
- Poor cash conversion (earnings growth >> cash flow growth)
- Deteriorating working capital
- Rising accounts receivable/inventory faster than revenue

### Referencia: references/report-template.md

# Stock Analysis Report Template

## Report Structure

### 1. Executive Summary
Brief 2-3 paragraph overview that can stand alone:
- Company overview (1 sentence)
- Investment thesis (bull case in 2-3 sentences)
- Key risks (1-2 sentences)
- Valuation summary (current vs fair value estimate)
- Recommendation (Buy/Hold/Sell) with conviction level

### 2. Company Overview
- **Business Description**: What the company does, main products/services
- **Industry**: Sector classification and industry dynamics
- **Market Position**: Market cap, rank in industry
- **Key Statistics**: Quick reference table
  - Ticker, Exchange
  - Market Cap
  - Current Price
  - 52-Week Range
  - Average Volume

### 3. Investment Thesis
**Bull Case** (Why to invest):
- 3-5 strongest positive factors
- Support each with data/evidence
- Quantify when possible

**Bear Case** (Risks and concerns):
- 3-5 main risk factors
- Alternative scenarios where investment doesn't work
- Probability assessment when possible

### 4. Fundamental Analysis

**Business Quality**
- Competitive advantages/moats
- Management quality assessment
- Business model sustainability

**Financial Performance** (Use tables for clarity)
- Revenue trends (3-5 years)
- Profitability metrics trends
- Balance sheet strength
- Cash flow analysis
- Key ratios

**Growth Analysis**
- Historical growth rates
- Growth drivers
- Future growth prospects
- Market opportunity size

### 5. Valuation Analysis

**Current Valuation Metrics** (Table format)
- P/E (current, forward, 5-year avg)
- PEG
- P/B
- P/S
- EV/EBITDA
- EV/Sales
- Dividend Yield (if applicable)

**Peer Comparison** (Table format)
Compare key metrics against 3-5 direct competitors

**Fair Value Estimate**
- Valuation methodology used
- Key assumptions
- Fair value range (conservative to optimistic)
- Margin of safety vs current price
- Target price with timeframe

### 6. Technical Analysis

**Trend Analysis**
- Current trend direction
- Key support/resistance levels
- Moving average positions

**Indicator Summary**
- RSI reading and interpretation
- MACD status
- Volume trends
- Other relevant indicators

**Chart Patterns**
- Notable patterns forming or completed
- Breakout/breakdown levels to watch

**Technical Outlook**
- Short-term (1-3 months)
- Medium-term (3-6 months)

### 7. Risk Assessment

**Company-Specific Risks** (Prioritized)
1. [Highest risk with impact and probability]
2. [Second risk]
3. [Third risk]

**Market/Macro Risks**
- Economic sensitivity
- Interest rate impact
- Regulatory changes
- Industry disruption

**Risk Mitigation**
- Company's risk management
- Diversification considerations
- Position sizing recommendations

### 8. Catalysts and Timeline

**Positive Catalysts** (with expected timing)
- Upcoming events that could drive price up
- Product launches, earnings, regulatory approvals

**Negative Risks** (with timing)
- Events that could drive price down
- Lockup expirations, debt maturities

### 9. Recommendation

**Rating**: Buy / Hold / Sell
**Conviction Level**: High / Medium / Low
**Target Price**: $XX (timeframe: X months)
**Upside/Downside**: +/-XX%

**For Buy Recommendations**:
- Entry strategy (all at once, DCA, wait for pullback)
- Position sizing suggestion
- Stop-loss consideration
- Target prices (multiple levels)

**For Hold Recommendations**:
- Conditions to upgrade to Buy
- Conditions to downgrade to Sell
- Monitoring priorities

**For Sell Recommendations**:
- Exit strategy (immediate, gradual)
- Alternative investments to consider

### 10. Conclusion
- Summarize key points (3-4 bullets)
- Reiterate recommendation
- Next review date or monitoring triggers

---

## Formatting Guidelines

**Use Tables for:**
- Financial data comparisons
- Peer comparisons
- Key statistics
- Valuation metrics

**Use Bullet Points for:**
- Lists of factors/risks
- Key highlights
- Qualitative assessments

**Use Headers to:**
- Clearly separate sections
- Make report scannable
- Enable quick navigation

**Data Presentation:**
- Always include timeframe context
- Show trends (arrows, YoY%)
- Cite sources for all data
- Use consistent formatting (e.g., $B for billions)

**Writing Style:**
- Be direct and concise
- Quantify when possible
- Avoid jargon unless necessary
- Support opinions with evidence
- Balance bullish and bearish perspectives

## Comparison Report Structure

For "Compare Stock A vs Stock B" requests:

### 1. Side-by-Side Overview Table
Company metrics in columns for easy comparison

### 2. Relative Strengths Analysis
- Where each company excels
- Quantified advantages

### 3. Valuation Comparison
- Metrics comparison table
- Which appears cheaper and why

### 4. Technical Comparison
- Relative strength analysis
- Chart pattern comparison

### 5. Recommendation
- Which to buy/prefer and why
- Portfolio allocation suggestion
- Risk-adjusted return assessment

### Referencia: references/technical-analysis.md

# Technical Analysis Reference

## Key Technical Indicators

### Trend Indicators

**Moving Averages (MA)**
- SMA (Simple Moving Average): Average price over N periods
- EMA (Exponential Moving Average): Weighted towards recent prices
- Common periods: 20-day, 50-day, 200-day
- Golden Cross: 50-day MA crosses above 200-day MA (bullish)
- Death Cross: 50-day MA crosses below 200-day MA (bearish)

**MACD (Moving Average Convergence Divergence)**
- MACD Line: 12-day EMA - 26-day EMA
- Signal Line: 9-day EMA of MACD
- Histogram: MACD - Signal
- Bullish: MACD crosses above signal line
- Bearish: MACD crosses below signal line

### Momentum Indicators

**RSI (Relative Strength Index)**
- Range: 0-100
- Overbought: > 70
- Oversold: < 30
- Divergence: Price makes new high/low but RSI doesn't (reversal signal)

**Stochastic Oscillator**
- %K and %D lines
- Range: 0-100
- Overbought: > 80
- Oversold: < 20

### Volatility Indicators

**Bollinger Bands**
- Middle Band: 20-day SMA
- Upper Band: Middle + (2 × standard deviation)
- Lower Band: Middle - (2 × standard deviation)
- Squeeze: Bands narrow (low volatility, potential breakout)
- Expansion: Bands widen (high volatility)

**ATR (Average True Range)**
- Measures volatility
- Higher ATR = higher volatility
- Used for stop-loss placement

### Volume Indicators

**OBV (On-Balance Volume)**
- Cumulative volume indicator
- Rising OBV + rising price = strong uptrend
- Divergence between OBV and price = potential reversal

**Volume Moving Average**
- Compare current volume to average
- High volume breakout = stronger signal

## Chart Patterns

### Reversal Patterns
- Head and Shoulders (bearish)
- Inverse Head and Shoulders (bullish)
- Double Top (bearish)
- Double Bottom (bullish)

### Continuation Patterns
- Flags and Pennants
- Triangles (ascending, descending, symmetrical)
- Rectangles

## Support and Resistance

**Support**: Price level where buying pressure prevents further decline
**Resistance**: Price level where selling pressure prevents further rise

**Key Levels to Identify:**
- Previous highs and lows
- Round numbers (psychological levels)
- Moving averages
- Fibonacci retracement levels (23.6%, 38.2%, 50%, 61.8%, 78.6%)

## Analysis Workflow

1. **Identify the trend** (uptrend, downtrend, sideways)
2. **Locate support/resistance levels**
3. **Check multiple timeframes** (daily, weekly, monthly)
4. **Confirm with indicators** (don't rely on single indicator)
5. **Look for divergences** (price vs indicators)
6. **Assess volume** (confirms trend strength)
7. **Identify chart patterns**
8. **Determine risk/reward ratio**


---

## SKILL: whale-hunting

- Fuente: `staskh/trading_skills` → `.claude/skills/whale-hunting` (MIT)
- Cuándo usarla: Detect institutional whale activity in options for a given underlying. Use when the user asks about unusual options activity, large block trades, whale trades, or institutional options flow for a specific symbol.
- Código: extraer `code/staskh_trading_skills.tar` y usar `.claude/skills/whale-hunting/` (whale_hunting.py)

# Whale Hunting

Scans option chains for a given underlying to identify institutional-sized trades using a two-step approach:
1. **Crude scan** (Yahoo Finance) — finds contracts with anomalous daily investment vs the rest of the chain.
2. **Precise drill-down** (Massive API) — fetches per-second bars for each candidate and flags seconds with outlier dollar invested.

## Instructions

> **Note:** If `uv` is not installed or `pyproject.toml` is not found, replace `uv run python` with `python` in all commands below.

```bash
uv run python .claude/skills/whale-hunting/scripts/whale_hunting.py SYMBOL [--months N] [--date YYYY-MM-DD] [--sigma F] [--sigma-z F] [--summary]
```

## Arguments

- `SYMBOL` — Underlying ticker (e.g. `AAPL`, `NVDA`, `SPY`)
- `--months` — Max months until option expiration to consider (default: 2)
- `--date` — Trading date to analyze in `YYYY-MM-DD` format (default: latest trading day)
- `--sigma` — Std-deviation multiplier for crude outlier threshold (default: 3.0)
- `--sigma-z` — Modified Z-Score threshold for per-second small-sample detection (default: 3.5)
- `--summary` — Also compute per-ticker summary and include it in the JSON output

## Output

Returns JSON with:
- `underlying` — The scanned symbol
- `trading_date` — Date analyzed
- `source` — `"massive"` (per-second data) or `"yahoo only"` (daily chain data)
- `total_whales` — Total whale events found
- `total_call_invested` — Sum of invested dollars in call whale events
- `total_put_invested` — Sum of invested dollars in put whale events
- `call_put_ratio` — Call invested / put invested (null if no puts)
- `directional_call_invested` — Call invested where break-even is ≥ 1.5% above spot
- `directional_put_invested` — Put invested where break-even is ≥ 1.5% below spot
- `directional_call_put_ratio` — Directional call / directional put invested (null if no directional puts)
- `whales` — List of whale events:
  - `timestamp`, `ticker`, `type`, `strike`, `spot` (underlying price at trade time), `expiry`
  - `close`, `volume`, `transactions`, `invested`, `break_even`, `pct_from_spot` (break-even distance from spot, %)
- `summary` *(present only when `--summary` is passed)* — List of per-ticker aggregates:
  - `ticker`, `type`, `strike`, `expiry`, `whale_count`, `total_invested`, `break_even`

## Examples

```bash
# Hunt whales for AAPL (latest trading day)
uv run python .claude/skills/whale-hunting/scripts/whale_hunting.py AAPL

# Hunt whales for NVDA on a specific date
uv run python .claude/skills/whale-hunting/scripts/whale_hunting.py NVDA --date 2026-03-13

# With per-ticker summary
uv run python .claude/skills/whale-hunting/scripts/whale_hunting.py HOOD --months 3 --summary

# Looser detection threshold
uv run python .claude/skills/whale-hunting/scripts/whale_hunting.py SPY --sigma 2.0
```

## Reporting

After running the script, present the results as follows.

**Header line:**
> Whale activity for **{underlying}** on {trading_date} — source: {source}
> Call flow: ${total_call_invested:,.0f} | Put flow: ${total_put_invested:,.0f} | C/P ratio: {call_put_ratio:.2f}
> Directional (≥1.5% B/E from spot) — Calls: ${directional_call_invested:,.0f} | Puts: ${directional_put_invested:,.0f} | C/P ratio: {directional_call_put_ratio:.2f}

**When `--summary` was requested**, render the `summary` array as a table:

| Time (ET) | Ticker | Type | Strike | Expiry | # Events | Total Invested | Break Even |
|-----------|--------|------|--------|--------|----------|----------------|------------|
| {timestamp} | {ticker} | {type} | {strike} | {expiry} | {whale_count} | ${total_invested:,.0f} | {break_even} |

Sort by `total_invested` descending. For multi-event rows use the time range of first–last event (e.g. `11:46–12:33`).

**Interpretation guidance:**
- `source: "massive"` — High-confidence; per-second block trade data from Massive API
- `source: "yahoo only"` — Fallback; daily-level data (Massive API key missing or no intraday data)
- Judge direction by `directional_call_put_ratio`, not `call_put_ratio` — trades with break-even within 1.5% of spot (deep ITM stock replacement, hedges) carry no directional signal
- Low directional C/P ratio (< 0.5) — Bearish institutional positioning
- High directional C/P ratio (> 2.0) — Bullish institutional positioning
- `transactions: 1` — Single block trade; strongest whale signal

## Requirements

- `MASSIVE_API_KEY` environment variable for per-second data. Without it, falls back to Yahoo Finance daily data.


## Timezone

All timestamps and time-based calculations must use the `America/New_York` timezone. All JSON output must include `generated_at` (NY time string) and `data_delay` fields.


---

## SKILL: whale-tracking

- Fuente: `agiprolabs/claude-trading-skills` → `skills/whale-tracking` (MIT)
- Cuándo usarla: Large wallet monitoring, accumulation and distribution detection, and smart money signal generation for Solana tokens
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/whale-tracking/` (track_whales.py, whale_alerts.py)

# Whale Tracking for Solana Tokens

Whale tracking monitors the on-chain behavior of large wallets to detect accumulation, distribution, and smart money movements before they become visible in price action. On Solana, where token ownership is highly concentrated and whale transactions can move markets instantly, tracking large holders is one of the highest-signal alpha sources available.

## Why Whale Tracking Matters

A single large wallet selling 5% of a token's supply can crash the price 30-50% on thin Solana DEX liquidity. Conversely, a known profitable wallet accumulating a new token often precedes major price runs. Whale tracking converts on-chain transparency into actionable intelligence.

Key use cases:

- **Early warning**: Detect large holder sells before the price impact fully propagates
- **Smart money following**: Identify wallets with strong track records and monitor their new positions
- **Accumulation detection**: Spot gradual buying by whales who split orders to avoid detection
- **Distribution detection**: Catch insiders or early investors offloading positions
- **Risk assessment**: Evaluate token concentration risk before entering a position

## What Constitutes a Whale

Whale classification depends on context. A wallet holding $50K of a $1M market cap token is a whale; the same $50K in SOL is not. Use relative and absolute thresholds:

### Absolute Thresholds

| Category | Trade Size | Portfolio Size | Typical Behavior |
|----------|-----------|---------------|-----------------|
| Retail | < 10 SOL | < 100 SOL | Reactive, follows trends |
| Mid-size | 10-100 SOL | 100-1,000 SOL | Mixed strategies |
| Whale | 100-1,000 SOL | 1,000-10,000 SOL | Informed, moves markets |
| Mega-whale | > 1,000 SOL | > 10,000 SOL | Market makers, funds, insiders |

### Relative Thresholds (Per Token)

| Metric | Threshold | Significance |
|--------|-----------|-------------|
| % of supply held | > 2% | Significant holder |
| % of daily volume | > 5% single trade | Market-moving transaction |
| Top N holders | Top 20 | Core holder group |
| Concentration ratio | Top 10 hold > 50% | High concentration risk |

Use both absolute and relative metrics. A 50 SOL trade in a $200K market cap token is whale-level; the same trade in a $50M token is retail.

## Accumulation vs Distribution Patterns

### Accumulation Signals

Accumulation is when a whale builds a position over time, often trying to minimize price impact.

**DCA pattern** (Dollar-Cost Averaging):
- Multiple buys of similar size over hours or days
- Buys at regular intervals (e.g., every 30 minutes)
- Position grows steadily without large single transactions

**Dip buying**:
- Buys concentrated during price dips
- Larger-than-usual purchases when price drops > 10%
- Position increases during periods of general selling

**Multi-wallet accumulation**:
- New wallets funded from the same source
- Each wallet buys small amounts of the same token
- Positions later consolidated into a primary wallet

**Detection heuristics**:
```
accumulation_score = 0
if buy_count > sell_count * 2:       accumulation_score += 2
if avg_buy_size > avg_sell_size:     accumulation_score += 1
if position_change_7d > 0:          accumulation_score += 1
if buys_during_dips > buys_on_pump:  accumulation_score += 2
if dca_pattern_detected:             accumulation_score += 2
# Score >= 4 = likely accumulating
```

### Distribution Signals

Distribution is when a whale reduces or exits a position, often gradually to avoid crashing the price.

**Gradual selling**:
- Multiple sells over days, each < 5% of position
- Sells increase in frequency over time
- Position shrinks steadily

**Transfer to exchange**:
- Tokens transferred to known exchange deposit addresses
- Large transfers to Binance, OKX, Bybit hot wallets
- Often precedes selling by hours or days

**Rapid exit**:
- Single large market sell (> 20% of position)
- Often triggers cascading liquidations
- Visible as large red candles with high volume

**Detection heuristics**:
```
distribution_score = 0
if sell_count > buy_count * 2:        distribution_score += 2
if position_change_7d < 0:           distribution_score += 1
if transfers_to_exchanges > 0:       distribution_score += 3
if sell_frequency_increasing:        distribution_score += 2
if position_pct_remaining < 50:      distribution_score += 1
# Score >= 4 = likely distributing
```

## Whale Watchlist Management

Maintain a watchlist of wallets worth tracking. Sources for discovering whale wallets:

### Discovery Methods

1. **Top holders per token**: Query `getTokenLargestAccounts` for any token of interest
2. **Large transaction monitoring**: Watch for trades > 100 SOL on key tokens
3. **Profitable trader rankings**: Use SolanaTracker or Birdeye top trader endpoints
4. **Known fund wallets**: Public wallet addresses of crypto funds and DAOs
5. **Cross-referencing**: Wallets that appear in top holders of multiple successful tokens

### Watchlist Structure

Each watchlist entry should track:

```python
whale_entry = {
    "address": "WhaLe...",
    "label": "Smart money #47",        # Human-readable label
    "discovered": "2026-01-15",         # When added to watchlist
    "discovery_reason": "top_trader",   # How they were found
    "win_rate": 0.72,                   # Historical trade win rate
    "avg_pnl": 3.4,                     # Average PnL multiplier
    "tokens_tracked": 12,               # Number of tokens held
    "last_active": "2026-03-09",        # Last on-chain activity
    "tags": ["dex_trader", "sniper"],   # Classification tags
}
```

### Wallet Classification Tags

| Tag | Description |
|-----|-------------|
| `sniper` | Buys tokens within minutes of launch |
| `dex_trader` | Primarily trades on DEXes |
| `accumulator` | Builds positions gradually |
| `flipper` | Short hold times, quick profit-taking |
| `insider` | Connected to token teams (funded by deployer) |
| `fund` | Institutional or fund wallet |
| `market_maker` | Provides liquidity, two-sided flow |

## Cross-Token Analysis

Whale tracking becomes most powerful when you analyze whale behavior across multiple tokens simultaneously.

### Convergence Signals

When multiple tracked whales buy the same token independently, the signal strength compounds:

| Whale Count | Signal | Confidence |
|-------------|--------|------------|
| 1 whale buying | Informational | Low |
| 2-3 whales buying | Notable | Medium |
| 4+ whales buying | Strong convergence | High |
| Whales + volume spike | Confirmed momentum | Very high |

### Cross-Token Flow Analysis

Track where whale capital flows:

```
Token A (selling) → SOL → Token B (buying)

If multiple whales rotate from A to B:
  - Bearish for Token A (smart money exiting)
  - Bullish for Token B (smart money entering)
```

## Data Sources

Whale tracking on Solana uses multiple data sources. See `references/data_sources.md` for complete details.

| Source | Use Case | Auth Required |
|--------|----------|---------------|
| Helius | Transaction history, webhooks | Yes (free tier available) |
| SolanaTracker | Top traders, wallet PnL | Yes |
| Birdeye | Token holder rankings | Yes (free tier available) |
| Solana RPC | Token accounts, signatures | No (public endpoints) |

### Helius Webhooks for Real-Time Tracking

Helius webhooks enable real-time whale alerts without polling:

```python
# Webhook configuration for whale wallet monitoring
webhook_config = {
    "webhookURL": "https://your-server.com/whale-alerts",
    "transactionTypes": ["SWAP", "TRANSFER"],
    "accountAddresses": [
        "WhaLe1...",  # Tracked whale wallets
        "WhaLe2...",
    ],
    "webhookType": "enhanced",  # Parsed transaction data
}
```

## Signal Generation

Convert whale activity into trading signals. Whale signals are one input to a broader decision framework, not standalone trading triggers.

### Signal Types

**Whale Buy Signal**:
- Whale buys > 100 SOL of a token
- Confidence increases with: whale track record, buy size, number of whales buying
- Weaken signal if: token is very new (< 24h), whale is known flipper, high concentration risk

**Whale Sell Signal**:
- Whale sells > 25% of position or > 100 SOL
- Confidence increases with: multiple whales selling, transfers to exchanges, increasing sell frequency
- Weaken signal if: whale is taking partial profit after large gain, whale is known rebalancer

**Accumulation Signal**:
- Whale accumulation score >= 4 (see scoring above)
- Strongest when: multiple whales accumulating same token, accumulation during price downtrend
- Time horizon: days to weeks (accumulation is a slow signal)

**Distribution Signal**:
- Whale distribution score >= 4
- Strongest when: team/insider wallets distributing, post-unlock distribution, increasing sell pace
- Time horizon: hours to days (distribution can accelerate quickly)

### Signal Scoring

```python
def compute_whale_signal(whale_activity: dict) -> dict:
    """Combine whale activity indicators into a composite signal."""
    score = 0.0

    # Trade direction: +1 for buy, -1 for sell
    direction = 1 if whale_activity["is_buy"] else -1

    # Size factor: larger trades = stronger signal
    size_sol = whale_activity["size_sol"]
    if size_sol > 500:
        score += direction * 3
    elif size_sol > 100:
        score += direction * 2
    else:
        score += direction * 1

    # Whale quality: better track record = stronger signal
    win_rate = whale_activity["whale_win_rate"]
    score *= (0.5 + win_rate)  # 0.5x to 1.5x multiplier

    # Convergence: multiple whales = stronger signal
    whale_count = whale_activity["concurrent_whale_count"]
    score *= (1 + 0.3 * (whale_count - 1))

    return {
        "score": round(score, 2),
        "direction": "bullish" if score > 0 else "bearish",
        "confidence": "high" if abs(score) > 5 else "medium" if abs(score) > 2 else "low",
    }
```

## Integration with Other Skills

Whale tracking works best when combined with other analysis:

| Skill | Integration |
|-------|-------------|
| `token-holder-analysis` | Identify concentration risk, insider wallets |
| `liquidity-analysis` | Estimate price impact of whale trades |
| `solana-onchain` | Wallet profiling, transaction history |
| `slippage-modeling` | Predict slippage for whale-sized trades |
| `risk-management` | Factor whale concentration into position sizing |
| `helius-api` | Transaction fetching, webhook setup |

## Files

### References
- `references/detection_methods.md` — Accumulation/distribution detection algorithms, whale classification, alert thresholds and scoring systems
- `references/data_sources.md` — Complete guide to Helius, SolanaTracker, Birdeye, and on-chain data sources for whale tracking

### Scripts
- `scripts/track_whales.py` — Fetches top holders for a token, classifies whale activity as accumulating/distributing/holding, prints a whale report. Run with `--demo` for synthetic data mode.
- `scripts/whale_alerts.py` — Monitors a watchlist of whale wallets for new large transactions, classifies trades, and prints alerts. Run with `--demo` for simulated whale trades.

## Limitations and Caveats

- **Privacy wallets**: Whales using multiple wallets or mixers can evade tracking
- **Misleading signals**: Whales may intentionally create visible accumulation to attract followers, then dump
- **Latency**: By the time you detect a whale buy, the price impact may already be priced in
- **False positives**: Internal transfers between a whale's own wallets look like buys/sells
- **Exchange wallets**: Centralized exchange hot wallets show massive flows that are not individual whale activity
- **Not financial advice**: Whale activity is informational input for analysis, not a standalone trading recommendation

### Referencia: references/data_sources.md

# Whale Tracking Data Sources

Complete guide to the APIs and on-chain methods used for whale tracking on Solana.

## Source Comparison

| Source | Real-Time | Auth | Free Tier | Best For |
|--------|-----------|------|-----------|----------|
| Helius | Yes (webhooks) | API key | 100K credits/mo | Transaction history, webhooks |
| SolanaTracker | Polling | API key | Limited | Top traders, PnL rankings |
| Birdeye | Polling | API key | 100 req/min | Token holder rankings |
| Solana RPC | Polling | None (public) | Unlimited | Token accounts, raw signatures |

## Helius

Helius provides parsed transaction data and webhook-based real-time monitoring. It is the primary data source for whale tracking.

### getSignaturesForAddress

Fetch recent transaction signatures for a wallet:

```
GET https://api.helius.xyz/v0/addresses/{address}/transactions?api-key={KEY}
```

**Parameters:**
- `address` (path): Wallet address
- `api-key` (query): Your Helius API key
- `limit` (query): Max results (default 100, max 1000)
- `before` (query): Signature to paginate before
- `type` (query): Filter by type (e.g., `SWAP`, `TRANSFER`)

**Response** (array of enhanced transactions):
```json
[
  {
    "signature": "5UfD...",
    "timestamp": 1709856000,
    "type": "SWAP",
    "source": "JUPITER",
    "tokenTransfers": [
      {
        "fromUserAccount": "WhaLe...",
        "toUserAccount": "Pool...",
        "mint": "So11...",
        "tokenAmount": 150.5
      },
      {
        "fromUserAccount": "Pool...",
        "toUserAccount": "WhaLe...",
        "mint": "EPjF...",
        "tokenAmount": 45000.0
      }
    ],
    "nativeTransfers": [...],
    "description": "WhaLe... swapped 150.5 SOL for 45000 TOKEN"
  }
]
```

**Rate limit:** Varies by plan. Free tier: ~10 req/sec.

### Webhooks for Real-Time Monitoring

Create a webhook to receive instant notifications for whale activity:

```
POST https://api.helius.xyz/v0/webhooks?api-key={KEY}
```

**Request body:**
```json
{
  "webhookURL": "https://your-server.com/whale-webhook",
  "transactionTypes": ["SWAP", "TRANSFER"],
  "accountAddresses": ["WhaLe1...", "WhaLe2..."],
  "webhookType": "enhanced",
  "encoding": "jsonParsed"
}
```

**Webhook types:**
- `enhanced` — Parsed transaction with human-readable descriptions (recommended)
- `raw` — Full raw transaction data
- `discord` — Formatted for Discord webhooks

**Key considerations:**
- Webhooks fire within seconds of transaction confirmation
- You can monitor up to 100 addresses per webhook on the free tier
- Enhanced type provides token transfer details pre-parsed
- Webhook delivery includes retry on failure (3 attempts)

### Helius DAS API

The Digital Asset Standard API provides token balance snapshots:

```
POST https://mainnet.helius-rpc.com/?api-key={KEY}
```

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "getAssetsByOwner",
  "params": {
    "ownerAddress": "WhaLe...",
    "page": 1,
    "limit": 1000,
    "displayOptions": {
      "showFungible": true
    }
  }
}
```

Returns all tokens held by a wallet with current balances. Useful for building a whale portfolio snapshot.

## SolanaTracker

SolanaTracker provides pre-computed trader rankings and PnL data.

### Top Traders Per Token

```
GET https://data.solanatracker.io/top-traders/{mint}
```

**Headers:** `x-api-key: {SOLANATRACKER_API_KEY}`

**Response:**
```json
{
  "wallets": [
    {
      "wallet": "WhaLe...",
      "pnl": 12500.0,
      "pnlPercent": 340.5,
      "bought": 5000.0,
      "sold": 17500.0,
      "volume": 22500.0,
      "tradeCount": 15,
      "holding": 0.0
    }
  ]
}
```

### Wallet PnL and Trade History

```
GET https://data.solanatracker.io/pnl/{wallet}
```

Returns overall PnL stats for a wallet across all tokens traded.

```
GET https://data.solanatracker.io/wallet/{wallet}/trades
```

Returns recent trades with token, direction, size, and timestamp.

### Top Traders Discovery

```
GET https://data.solanatracker.io/top-traders/all?period=7d&limit=50
```

Returns the most profitable wallets over a time period. Useful for discovering new whales to track.

## Birdeye

Birdeye provides token-centric holder and trader data.

### Token Top Traders

```
GET https://public-api.birdeye.so/defi/v2/tokens/top_traders
```

**Headers:** `X-API-KEY: {BIRDEYE_API_KEY}`, `x-chain: solana`

**Parameters:**
- `address` (query): Token mint address
- `time_frame` (query): `24h`, `7d`, `30d`
- `sort_type` (query): `volume`, `pnl`
- `offset`, `limit`: Pagination

**Response includes:** wallet address, buy/sell volume, trade count, PnL.

### Token Holder Distribution

```
GET https://public-api.birdeye.so/defi/v2/tokens/holder
```

**Parameters:**
- `address`: Token mint
- `offset`, `limit`: Pagination

Returns holder addresses sorted by balance, with percentage of supply.

**Rate limit:** 100 req/min (free), 1000 req/min (paid).

## On-Chain (Solana RPC)

Direct RPC calls require no API key and work with any Solana RPC endpoint.

### getTokenLargestAccounts

Fetch the top token holders directly from the chain:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "getTokenLargestAccounts",
  "params": ["TokenMintAddress..."]
}
```

**Response:**
```json
{
  "result": {
    "value": [
      {
        "address": "TokenAccountAddress...",
        "amount": "1000000000",
        "decimals": 9,
        "uiAmount": 1.0,
        "uiAmountString": "1.0"
      }
    ]
  }
}
```

**Notes:**
- Returns token account addresses, not wallet addresses
- You need `getAccountInfo` to resolve the token account owner (wallet address)
- Returns top 20 accounts by default
- Free, no authentication required

### Resolving Token Account to Wallet

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "getAccountInfo",
  "params": [
    "TokenAccountAddress...",
    {"encoding": "jsonParsed"}
  ]
}
```

The `parsed.info.owner` field contains the wallet address.

### getSignaturesForAddress

Monitor recent transactions for a wallet:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "getSignaturesForAddress",
  "params": [
    "WalletAddress...",
    {"limit": 20}
  ]
}
```

Returns signature, slot, blockTime, and err (null if successful). Use each signature to fetch full transaction details via `getTransaction`.

### Transaction Monitoring Pipeline

For whale tracking via raw RPC: (1) `getTokenLargestAccounts` for target token, (2) resolve each token account to wallet, (3) poll `getSignaturesForAddress` per whale, (4) fetch new transactions with `getTransaction` (jsonParsed), (5) parse token transfers to classify buy/sell/transfer.

## Recommended Stack

| Component | Recommended | Fallback |
|-----------|-------------|----------|
| Real-time alerts | Helius webhooks | Polling RPC signatures |
| Transaction history | Helius enhanced API | Solana RPC + manual parsing |
| Top trader discovery | SolanaTracker rankings | Birdeye top traders |
| Holder snapshots | Solana RPC (getTokenLargestAccounts) | Birdeye holder endpoint |
| Wallet PnL | SolanaTracker wallet PnL | Compute from trade history |

For a cost-effective setup, use free Solana RPC for holder snapshots and Helius free tier for enhanced transaction parsing. Upgrade to paid Helius ($49/mo) for webhook-based real-time tracking.

### Referencia: references/detection_methods.md

# Whale Detection Methods

Algorithms and heuristics for identifying whale wallets, classifying their behavior as accumulation or distribution, and generating scored alerts.

## Whale Classification

### By Trade Size

Classify individual transactions by SOL value:

```python
def classify_trade_size(sol_amount: float) -> str:
    """Classify a single trade by size."""
    if sol_amount >= 1000:
        return "mega_whale"
    elif sol_amount >= 100:
        return "whale"
    elif sol_amount >= 10:
        return "mid_size"
    else:
        return "retail"
```

### By Portfolio Value

Classify wallets by total holdings:

```python
def classify_wallet(total_sol_value: float) -> str:
    """Classify a wallet by total portfolio value in SOL."""
    if total_sol_value >= 10_000:
        return "mega_whale"
    elif total_sol_value >= 1_000:
        return "whale"
    elif total_sol_value >= 100:
        return "mid_size"
    else:
        return "retail"
```

### By Token-Relative Holdings

For a specific token, classify by percentage of supply held:

| % of Supply | Classification | Risk Level |
|-------------|---------------|------------|
| > 10% | Dominant whale | Critical |
| 5-10% | Major whale | High |
| 2-5% | Significant holder | Medium |
| 1-2% | Notable holder | Low |
| < 1% | Minor holder | Minimal |

### By Influence Score

Combine multiple factors into an influence score:

```python
def compute_influence_score(
    pct_supply: float,
    trade_count_30d: int,
    avg_trade_sol: float,
    win_rate: float,
    follower_count: int,
) -> float:
    """Compute a 0-100 influence score for a whale wallet.

    Args:
        pct_supply: Percentage of token supply held (0-100).
        trade_count_30d: Number of trades in the last 30 days.
        avg_trade_sol: Average trade size in SOL.
        win_rate: Historical win rate (0-1).
        follower_count: Number of wallets that copy this wallet.

    Returns:
        Influence score from 0 to 100.
    """
    supply_score = min(pct_supply * 5, 30)       # Max 30 points
    activity_score = min(trade_count_30d * 0.5, 20)  # Max 20 points
    size_score = min(avg_trade_sol / 50, 20)     # Max 20 points
    skill_score = win_rate * 15                   # Max 15 points
    social_score = min(follower_count * 0.5, 15)  # Max 15 points
    return round(supply_score + activity_score + size_score + skill_score + social_score, 1)
```

## Accumulation Detection

### DCA Pattern Detection

Detect Dollar-Cost Averaging by looking for regular, similarly-sized buys:

```python
import statistics

def detect_dca_pattern(
    buy_timestamps: list[float],
    buy_amounts: list[float],
    min_buys: int = 4,
    max_cv: float = 0.5,
) -> bool:
    """Detect DCA buying pattern.

    Args:
        buy_timestamps: Unix timestamps of buy transactions.
        buy_amounts: SOL amounts of each buy.
        min_buys: Minimum number of buys to consider.
        max_cv: Maximum coefficient of variation for amounts.

    Returns:
        True if DCA pattern detected.
    """
    if len(buy_timestamps) < min_buys:
        return False

    # Check amount consistency (low coefficient of variation)
    mean_amt = statistics.mean(buy_amounts)
    if mean_amt == 0:
        return False
    cv = statistics.stdev(buy_amounts) / mean_amt
    if cv > max_cv:
        return False

    # Check time regularity (intervals should be somewhat consistent)
    intervals = [
        buy_timestamps[i + 1] - buy_timestamps[i]
        for i in range(len(buy_timestamps) - 1)
    ]
    mean_interval = statistics.mean(intervals)
    if mean_interval == 0:
        return False
    interval_cv = statistics.stdev(intervals) / mean_interval
    return interval_cv < 1.0  # Intervals within 1 CV
```

### Dip Buying Detection

Calculate what fraction of buys occurred during price dips (drawdown > 10% from rolling high). Compare buy timestamps against price history, compute rolling high at each buy point, and check if price was in drawdown. A dip_buy_ratio > 0.5 is a strong accumulation signal.

### Composite Accumulation Score

```python
def compute_accumulation_score(
    buy_count: int,
    sell_count: int,
    avg_buy_size: float,
    avg_sell_size: float,
    position_change_7d_pct: float,
    dip_buy_ratio: float,
    is_dca: bool,
) -> int:
    """Compute accumulation score from 0 to 10.

    Score >= 4 indicates likely accumulation.
    Score >= 7 indicates strong accumulation.
    """
    score = 0
    if buy_count > sell_count * 2:
        score += 2
    elif buy_count > sell_count:
        score += 1
    if avg_buy_size > avg_sell_size * 1.5:
        score += 1
    if position_change_7d_pct > 10:
        score += 2
    elif position_change_7d_pct > 0:
        score += 1
    if dip_buy_ratio > 0.5:
        score += 2
    elif dip_buy_ratio > 0.25:
        score += 1
    if is_dca:
        score += 2
    return min(score, 10)
```

## Distribution Detection

### Exchange Transfer Detection

Known Solana exchange deposit addresses (partial list):

| Exchange | Hot Wallet Prefix | Notes |
|----------|------------------|-------|
| Binance | 5tzFkiKsc... | Multiple deposit addresses |
| OKX | JCnc... | Rotates addresses |
| Bybit | AC5R... | Rotates addresses |

Detection approach:
1. Maintain a list of known exchange wallet addresses
2. Flag any SPL token transfers to these addresses
3. Weight: transfer to exchange = strong distribution signal (+3 to distribution score)

### Sell Frequency Analysis

```python
def detect_increasing_sell_frequency(
    sell_timestamps: list[float],
    window_days: int = 7,
) -> bool:
    """Detect whether sell frequency is increasing over time.

    Compares sell count in the most recent window to the prior window.
    """
    if len(sell_timestamps) < 4:
        return False

    now = sell_timestamps[-1]
    window_seconds = window_days * 86400
    recent_cutoff = now - window_seconds
    prior_cutoff = now - (2 * window_seconds)

    recent_sells = sum(1 for t in sell_timestamps if t >= recent_cutoff)
    prior_sells = sum(1 for t in sell_timestamps if prior_cutoff <= t < recent_cutoff)

    return recent_sells > prior_sells * 1.5
```

### Composite Distribution Score

```python
def compute_distribution_score(
    buy_count: int,
    sell_count: int,
    position_change_7d_pct: float,
    transfers_to_exchanges: int,
    sell_frequency_increasing: bool,
    position_pct_remaining: float,
) -> int:
    """Compute distribution score from 0 to 10.

    Score >= 4 indicates likely distribution.
    Score >= 7 indicates aggressive distribution.
    """
    score = 0
    if sell_count > buy_count * 2:
        score += 2
    elif sell_count > buy_count:
        score += 1
    if position_change_7d_pct < -20:
        score += 2
    elif position_change_7d_pct < 0:
        score += 1
    if transfers_to_exchanges > 0:
        score += 3
    if sell_frequency_increasing:
        score += 2
    if position_pct_remaining < 50:
        score += 1
    return min(score, 10)
```

## Alert Thresholds

### Transaction-Level Alerts

| Alert Level | Trigger | Action |
|-------------|---------|--------|
| Info | Tracked whale any trade | Log activity |
| Warning | Whale trade > 100 SOL | Notify if subscribed |
| Critical | Whale sells > 25% of position | Immediate alert |
| Emergency | Multiple whales selling same token | Flash alert |

### Scoring Alert Priority

Score by summing points: trade size (1-3 pts), whale influence (2-3 pts), concurrent whale count (0-3 pts), sell bonus (+1). Map total to priority: 8+ = critical, 5+ = high, 3+ = medium, else low.

## Multi-Wallet Detection

Whales often split holdings across wallets. Detect linked wallets by:

1. **Funding source**: Wallets funded from the same parent wallet
2. **Timing correlation**: Wallets that trade the same tokens at similar times
3. **Consolidation events**: Multiple wallets sending tokens to a single address

When linked wallets are detected, treat their combined holdings as a single whale entity for accumulation/distribution scoring.
