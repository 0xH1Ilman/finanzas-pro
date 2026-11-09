# 04-macro-mercado-breadth — parte 2

Skills de terceros agrupadas por tema. Cada sección indica fuente, licencia y dónde está su código.



---

## SKILL: market-top-detector

- Fuente: `tradermonty/claude-trading-skills` → `skills/market-top-detector` (MIT)
- Cuándo usarla: Assesses heuristic market top risk using O'Neil Distribution Days, Minervini Leading Stock Deterioration, and Monty Defensive Sector Rotation. Generates a 0-100 composite score with risk zone classification. Use when user asks about market top risk, distribution days, defensive rotation, leadership breakdown, or whether to reduce equity exposure. Focuses on 2-8 week tactical timing signals for 10-20% corrections.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/market-top-detector/` (requirements.txt, _market_calendar.py, breadth_csv_client.py, __init__.py, breadth_calculator.py, defensive_rotation_calculator.py, distribution_day_calculator.py, index_technical_calculator.py, leading_stock_calculator.py, math_utils.py, sentiment_calculator.py, fmp_client.py …)

# Market Top Detector Skill

## Purpose

Assess heuristic market top risk using a 6-component scoring system (0-100). Integrates three market risk methodologies:

1. **O'Neil** - Distribution Day accumulation (institutional selling)
2. **Minervini** - Leading stock deterioration pattern
3. **Monty** - Defensive sector rotation signal

Unlike the Bubble Detector (macro/multi-month evaluation), this skill focuses on **tactical 2-8 week timing signals** that precede 10-20% market corrections.

## Score interpretation

Treat the 0-100 composite as a **heuristic risk score**, not an estimated event
probability. A score of 70 does not mean a 70% chance of a top. Risk-budget
percentages are policy heuristics, not measured outcome frequencies.
Historical patterns are retrospective estimates, not point-in-time evidence.
Report **no comparable episode** when any component is unavailable/invalid or
nearest-pattern weighted RMS exceeds 15 points. This tolerance is a predeclared
heuristic, not an empirically validated similarity threshold.
Follow [the point-in-time evaluation protocol](references/point_in_time_evaluation.md)
before making calibration claims. No measured calibration results are supplied.

## When to Use This Skill

**English:**
- User asks "Is the market topping?" or "Are we near a top?"
- User notices distribution days accumulating
- User observes defensive sectors outperforming growth
- User sees leading stocks breaking down while indices hold
- User asks about reducing equity exposure timing
- User wants to assess correction risk for the next 2-8 weeks

**Japanese:**
- 「天井が近い？」「今は利確すべき？」
- ディストリビューションデーの蓄積を懸念
- ディフェンシブセクターがグロースをアウトパフォーム
- 先導株が崩れ始めているが指数はまだ持ちこたえている
- エクスポージャー縮小のタイミング判断
- 今後2〜8週間の調整リスクを評価したい

## Prerequisites

**Required:**
- **FMP API Key:** Set `$FMP_API_KEY` environment variable or pass `--api-key`. Free tier sufficient (~33 API calls per execution).
- **WebSearch Access:** Required to collect S&P 500 breadth (50DMA %) and CBOE Put/Call ratio data.

**Optional:**
- **Margin Debt Data:** Enhances sentiment scoring but typically 1-2 months lagged.
- **VIX Term Structure:** Auto-detected from FMP API if VIX3M quote available; manual override via `--vix-term`.

**Data Freshness:** All manually collected data should be from the most recent 3 business days for accurate analysis.

## Difference from Bubble Detector

| Aspect | Market Top Detector | Bubble Detector |
|--------|-------------------|-----------------|
| Timeframe | 2-8 weeks | Months to years |
| Target | 10-20% correction | Bubble collapse (30%+) |
| Methodology | O'Neil/Minervini/Monty | Minsky/Kindleberger |
| Data | Price/Volume + Breadth | Valuation + Sentiment + Social |
| Score Range | 0-100 composite | 0-15 points |

---

## Execution Workflow

### Phase 1: Data Collection via WebSearch

Before running the Python script, collect the following data using WebSearch.
**Data Freshness Requirement:** All data must be from the most recent 3 business days. Stale data degrades analysis quality.

```
1. S&P 500 Breadth (200DMA above %)
   AUTO-FETCHED from TraderMonty CSV (no WebSearch needed)
   The script fetches this automatically from GitHub Pages CSV data.
   Override: --breadth-200dma [VALUE] to use a manual value instead.
   Disable: --no-auto-breadth to skip auto-fetch entirely.

2. [REQUIRED] S&P 500 Breadth (50DMA above %)
   Valid range: 20-100
   Primary search: "S&P 500 percent stocks above 50 day moving average"
   Fallback: "market breadth 50dma site:barchart.com"
   Direct fallback when search snippets are poor: fetch `https://www.barchart.com/stocks/quotes/$S5FI/overview` and extract the embedded `lastPrice` / `tradeTime` for “S&P 500 Stocks Above 50-Day Average”.
   Record the data date

3. [REQUIRED] CBOE Equity Put/Call Ratio
   Valid range: 0.30-1.50
   Primary search: "CBOE equity put call ratio today"
   Fallback: "CBOE total put call ratio current"
   Fallback: "put call ratio site:cboe.com"
   Direct fallback when Cboe CSV endpoints are stale: fetch `https://ycharts.com/indicators/cboe_equity_put_call_ratio` and parse the “Last Value” / “Latest Period” table fields. Treat this as a secondary source and cite it in freshness notes.
   Record the data date

4. [OPTIONAL] VIX Term Structure
   Values: steep_contango / contango / flat / backwardation
   Primary search: "VIX VIX3M ratio term structure today"
   Fallback: "VIX futures term structure contango backwardation"
   Note: Auto-detected from FMP API if VIX3M quote available.
   CLI --vix-term overrides auto-detection.

5. [OPTIONAL] Margin Debt YoY %
   Primary search: "FINRA margin debt latest year over year percent"
   Fallback: "NYSE margin debt monthly"
   Note: Typically 1-2 months lagged. Record the reporting month.
```

### Phase 2: Execute Python Script

Run the script with collected data as CLI arguments:

```bash
python3 skills/market-top-detector/scripts/market_top_detector.py \
  --api-key $FMP_API_KEY \
  --breadth-50dma [VALUE] --breadth-50dma-date [YYYY-MM-DD] \
  --put-call [VALUE] --put-call-date [YYYY-MM-DD] \
  --vix-term [steep_contango|contango|flat|backwardation] \
  --margin-debt-yoy [VALUE] --margin-debt-date [YYYY-MM-DD] \
  --output-dir reports/ \
  --context "Consumer Confidence=[VALUE]" "Gold Price=[VALUE]"
# 200DMA breadth is auto-fetched from TraderMonty CSV.
# Override with --breadth-200dma [VALUE] if needed.
# Disable with --no-auto-breadth to skip auto-fetch.
```

The script will:
1. Fetch S&P 500, QQQ, VIX quotes and history from FMP API
2. Fetch Leading ETF (ARKK, WCLD, IGV, XBI, SOXX, SMH, KWEB, TAN) data
3. Fetch Sector ETF (XLU, XLP, XLV, VNQ, XLK, XLC, XLY) data
4. Calculate all 6 components
5. Generate composite score and reports

### Phase 3: Present Results

Present the generated Markdown report to the user, highlighting:
- Composite score and risk zone
- Data freshness warnings (if any data older than 3 days)
- Strongest warning signal (highest component score)
- Historical comparison (closest past top pattern)
- What-if scenarios (sensitivity to key changes)
- Recommended actions based on risk zone
- Follow-Through Day status (if applicable)
- Delta vs previous run (if prior report exists)

---

## 6-Component Scoring System

| # | Component | Weight | Data Source | Key Signal |
|---|-----------|--------|-------------|------------|
| 1 | Distribution Day Count | **25%** | FMP API | Institutional selling in last 25 trading days |
| 2 | Leading Stock Health | **20%** | FMP API | Growth ETF basket deterioration |
| 3 | Defensive Sector Rotation | **15%** | FMP API | Defensive vs Growth relative performance |
| 4 | Market Breadth Divergence | **15%** | Auto (CSV) + WebSearch | 200DMA (auto) / 50DMA (WebSearch) breadth vs index level |
| 5 | Index Technical Condition | **15%** | FMP API | MA structure, failed rallies, lower highs |
| 6 | Sentiment & Speculation | **10%** | FMP + WebSearch | VIX, Put/Call, term structure |

## Risk Zone Mapping

| Score | Zone | Risk Budget | Action |
|-------|------|-------------|--------|
| 0-20 | Green (Normal) | 100% | Normal operations |
| 21-40 | Yellow (Early Warning) | 80-90% | Tighten stops, reduce new entries |
| 41-60 | Orange (Elevated Risk) | 60-75% | Profit-taking on weak positions |
| 61-80 | Red (High Risk) | 40-55% | Aggressive profit-taking |
| 81-100 | Critical (Very High Risk) | 20-35% | Maximum defense, hedging |

---

## Exchange Calendar and Replay

Install `requirements.txt` before running the detector. Freshness uses XNYS
sessions rather than weekdays. `--as-of YYYY-MM-DD` is accepted for the live
evaluation date, but historical live replay fails closed because the current
quote endpoints are not point-in-time sources.

## API Requirements

**Required:** FMP API key (free tier sufficient: ~33 calls per execution)
**Optional:** WebSearch data for breadth and sentiment (improves accuracy)

## Output Files

- JSON: `market_top_YYYY-MM-DD_HHMMSS.json`
- Markdown: `market_top_YYYY-MM-DD_HHMMSS.md`

## Reference Documents

### `references/market_top_methodology.md`
- Full methodology with O'Neil, Minervini, and Monty frameworks
- Component scoring details and thresholds
- Historical validation notes

### `references/distribution_day_guide.md`
- Detailed O'Neil Distribution Day rules
- Stalling day identification
- Follow-Through Day (FTD) mechanics

### `references/historical_tops.md`
- Analysis of 2000, 2007, 2018, 2022 market tops
- Component score patterns during historical tops
- Lessons learned and retrospective illustrative estimates

### When to Load References
- **First use:** Load `market_top_methodology.md` for full framework understanding
- **Distribution day questions:** Load `distribution_day_guide.md`
- **Historical context:** Load `historical_tops.md`
- **Regular execution:** References not needed - script handles scoring

### Referencia: references/distribution_day_guide.md

# Distribution Day Guide

## What is a Distribution Day?

A Distribution Day occurs when a major stock index (S&P 500 or NASDAQ Composite) declines by 0.2% or more on volume that is higher than the previous trading day. This pattern indicates institutional investors are selling stocks in volume - "distributing" their holdings.

William O'Neil introduced this concept in "How to Make Money in Stocks" as one of the most reliable signals that a market uptrend is under pressure.

## Precise Rules

### Distribution Day Criteria (BOTH must be met):
1. **Price decline >= 0.2%** from previous session's close
2. **Volume > previous day's volume** (even slightly higher counts)

### Stalling Day Criteria (BOTH must be met):
1. **Volume > previous day's volume** (institutional activity present)
2. **Price gain < 0.1%** (price fails to advance meaningfully despite volume)
3. Stalling days count as **0.5 distribution days** in the effective count

### 25-Day Expiration Rule:
- A distribution day automatically expires after **25 trading days** (approximately 5 weeks)
- Only the rolling 25-day window matters
- This prevents old distribution from affecting current assessment

### What Does NOT Count as Distribution:
- Index declines on lower volume (normal profit-taking)
- Large gap-up open followed by slight closing decline (still net positive day)
- Volume below average (lack of institutional participation)

## Counting and Interpretation

| Effective Count | Interpretation | Action |
|----------------|----------------|--------|
| 0-1 | Healthy market | Normal operations |
| 2-3 | Some selling but normal | Monitor closely |
| 4 | O'Neil's initial warning | Tighten stops |
| 5 | Significant distribution | Reduce exposure |
| 6+ | Heavy distribution | Protect capital aggressively |

**Effective Count Formula:**
```
Effective Count = Distribution Days + (0.5 × Stalling Days)
```

## Dual-Index Approach

This tool monitors both the S&P 500 and NASDAQ (via QQQ). The higher effective count between the two indices is used for scoring, because:

1. Distribution can concentrate in one index before the other
2. NASDAQ often leads due to higher growth stock concentration
3. The worst signal from either index is the most conservative approach

## Common Patterns at Market Tops

### Classic Distribution Sequence (2022 Example):
1. Week 1: One distribution day (seems harmless)
2. Week 2: Two more distribution days
3. Week 3: One stalling day (selling into rallies)
4. Week 4: Two more distribution days (total: 5-6 effective)
5. Market breaks down shortly after

### False Alarm Pattern:
1. Two distribution days in quick succession
2. Market rallies strongly, erasing concerns
3. Distribution days expire without reaching critical mass
4. Uptrend continues

### Key Distinction:
The **clustering** of distribution days matters. Three distribution days in one week is more alarming than three spread over five weeks.

## Follow-Through Day (FTD)

The FTD is the counterpart to distribution days - it signals a potential new uptrend after a correction.

### FTD Rules:
1. **Rally Attempt:** Market makes its low and begins to rally (first up day)
2. **Counting:** Start counting from day 1 of the rally attempt
3. **FTD Occurs on Day 4-7:** A significant price gain (>1.5%) with volume higher than the previous day
4. **Confirmation:** The FTD should be on day 4 at the earliest (premature rallies on days 1-3 are unreliable)

### FTD Reliability:
- Not all FTDs lead to sustained uptrends (~25% fail)
- Multiple FTDs within a short period increase confidence
- FTDs work best when combined with improving breadth
- O'Neil: "I never try to buy at the bottom. I wait for the Follow-Through Day."

## Practical Tips

### When Monitoring Distribution:
1. Check distribution count DAILY during uncertain markets
2. Pay special attention when count reaches 3 (pre-warning)
3. At 4+, begin defensive actions regardless of other signals
4. Don't wait for 6+ to act - by then, significant damage may be done

### Common Mistakes:
1. **Ignoring stalling days:** They're subtle but significant
2. **Resetting count manually:** Trust the 25-day expiration rule
3. **Using wrong volume data:** Must compare day-to-day, not vs average
4. **Mixing indices:** Count separately for S&P 500 and NASDAQ
5. **Ignoring context:** 4 distribution days in a strong uptrend is different from 4 in a range-bound market

### Referencia: references/historical_tops.md

# Historical Market Top Analysis

## Overview

Analysis of major market tops through the lens of the 6-component Market Top Detector framework. These historical cases are retrospective illustrations with estimated component scores, not point-in-time calibration data.

## 2000: Dot-Com Bubble Top (March 2000)

### Timeline
- **S&P 500 Peak:** March 24, 2000 (1,527.46)
- **NASDAQ Peak:** March 10, 2000 (5,048.62)
- **Subsequent Decline:** S&P -49%, NASDAQ -78% over 2.5 years

### Component Signals (Estimated Scores)

| Component | Signal Level | Est. Score | Notes |
|-----------|-------------|------------|-------|
| Distribution Days | Very High | 90-100 | Heavy distribution throughout March 2000 |
| Leading Stocks | Critical | 85-95 | Internet stocks peaked weeks before indices |
| Defensive Rotation | Strong | 70-80 | Value/defensive outperformed for months |
| Breadth | Critical Divergence | 80-90 | Advance/Decline line peaked in April 1998 |
| Index Technical | Breaking Down | 70-80 | NASDAQ broke 50DMA first |
| Sentiment | Extreme | 90-100 | IPO mania, "new paradigm" narrative |

**Estimated Composite: 82-92 (Critical)**

### Key Lesson
Breadth divergence was the earliest signal (nearly 2 YEARS before the top). Distribution days and leading stock breakdown were the final confirmation signals. By the time all 6 components were flashing red, the decline had already begun.

---

## 2007: Financial Crisis Top (October 2007)

### Timeline
- **S&P 500 Peak:** October 9, 2007 (1,565.15)
- **Subsequent Decline:** -57% over 17 months (March 2009 low)

### Component Signals (Estimated Scores)

| Component | Signal Level | Est. Score | Notes |
|-----------|-------------|------------|-------|
| Distribution Days | High | 75-85 | Multiple distribution clusters in Sept-Oct 2007 |
| Leading Stocks | High | 70-80 | Homebuilders (ITB) peaked in Feb 2006, financials (XLF) peaked in June 2007 |
| Defensive Rotation | Moderate | 55-65 | Utilities and healthcare outperforming |
| Breadth | Diverging | 60-70 | NYSE advance/decline line peaked July 2007 |
| Index Technical | Weakening | 50-60 | S&P still near highs but internal structure deteriorating |
| Sentiment | Elevated | 55-65 | VIX was very low (sub-12) for extended period in 2006-2007 |

**Estimated Composite: 62-72 (Red Zone)**

### Key Lesson
The 2007 top was a slow-motion process. Leading sector (financials/housing) peaked 12-18 months before the S&P 500. The composite would have been in the "Orange" zone for months before reaching "Red." This top rewarded patience in reducing exposure rather than a single binary call.

---

## 2018: Q4 Sell-Off (September-December 2018)

### Timeline
- **S&P 500 Peak:** September 20, 2018 (2,930.75)
- **Subsequent Decline:** -20% (correction, not bear market)
- **Recovery:** V-bottom in December 2018, new highs by April 2019

### Component Signals (Estimated Scores)

| Component | Signal Level | Est. Score | Notes |
|-----------|-------------|------------|-------|
| Distribution Days | Moderate | 55-65 | Distribution accumulated through October |
| Leading Stocks | Moderate | 50-60 | FAANG stocks peaked at different times (FB in July, AMZN in September) |
| Defensive Rotation | Moderate | 45-55 | Utilities outperformed in Q3 |
| Breadth | Mild Divergence | 40-50 | Breadth narrowing but not extreme |
| Index Technical | Weakening | 55-65 | 50DMA crossed below 200DMA in December |
| Sentiment | Mixed | 35-45 | VIX was elevated but not extreme |

**Estimated Composite: 47-57 (Orange Zone)**

### Key Lesson
This was a classic "correction" case (not a bear market). The composite correctly would have been in Orange zone - enough to warrant profit-taking but not full defensive posture. The rapid V-recovery demonstrated why the composite avoids going to "Critical" without extreme readings across multiple components.

---

## 2022: Fed Tightening Bear Market (January 2022)

### Timeline
- **S&P 500 Peak:** January 3, 2022 (4,796.56)
- **NASDAQ Peak:** November 19, 2021 (16,057.44)
- **Subsequent Decline:** S&P -25%, NASDAQ -33%

### Component Signals (Estimated Scores at January 2022)

| Component | Signal Level | Est. Score | Notes |
|-----------|-------------|------------|-------|
| Distribution Days | High | 75-90 | Heavy distribution in late December 2021 and early January 2022 |
| Leading Stocks | Critical | 80-90 | ARKK peaked Feb 2021 (11 months early), many growth stocks -50%+ from highs |
| Defensive Rotation | Strong | 65-75 | XLU, XLP outperforming strongly |
| Breadth | Severe Divergence | 70-80 | NASDAQ new highs/new lows diverging sharply |
| Index Technical | Breaking | 60-70 | NASDAQ broke 200DMA, S&P testing key levels |
| Sentiment | Elevated | 50-60 | Margin debt at record highs, crypto speculation |

**Estimated Composite: 68-78 (Red Zone)**

### Key Lesson
ARKK (leading stock proxy) peaked 11 months before S&P 500. This is a textbook Minervini signal - leading stocks deteriorate long before the index. By January 2022, the composite would have been solidly in the Red zone, correctly signaling aggressive profit-taking. The 2022 case validates the "Leading Stock Health" component as an early warning signal.

---

## Cross-Case Patterns

### What All Tops Had in Common:
1. **Distribution days clustered** (not spread out) in the weeks before the decline
2. **Leading stocks peaked before the index** (by weeks to months)
3. **Breadth diverged** from index price (the rally became increasingly narrow)
4. **Defensive rotation** accelerated as the top formed

### What Varied:
1. **Severity:** Ranged from -20% correction (2018) to -78% NASDAQ crash (2000)
2. **Speed:** 2018 was a fast decline (3 months), 2000-2002 was slow (2.5 years)
3. **Recovery time:** 2018 recovered in 4 months, 2000 took 7 years (NASDAQ)
4. **Breadth divergence timing:** 2000 had 2-year divergence, 2022 had months

### Illustrative Score Patterns:
- **Orange Zone (41-60):** Retrospective correction illustration (2018-type, -10-20%)
- **Red Zone (61-80):** Retrospective major-decline illustration (2007, 2022-type, -20-35%)
- **Critical (81-100):** Retrospective bubble-top illustration (2000-type, -40%+)

### Important Caveat:
These retrospective examples do not establish measured calibration. Each market environment is unique. The composite score should be used as one input into investment decisions, not as a definitive prediction. Markets can remain in "warning" zones for extended periods before actually declining.

---

## Pattern: Leading Stocks as Early Warning

From the Monty article:
> 弱気相場の初期段階では、特定の主導株が下降トレンドに抵抗するかのように強く、
> 上昇できるという印象を与えます。

This pattern appeared in every historical top:
- **2000:** Blue-chip tech (MSFT, INTC) held up while dot-coms crashed
- **2007:** Energy sector rallied while financials imploded
- **2022:** AAPL, MSFT relatively stable while ARKK stocks crashed
- **Current analog:** Some mega-caps hold while growth/speculative names deteriorate

This is why Component 2 (Leading Stock Health) uses a broad basket of growth ETFs rather than just the S&P 500 components - it captures the deterioration that indices mask.

### Referencia: references/market_top_methodology.md

# Market Top Detection Methodology

## Overview

This framework integrates three approaches to market top detection, each targeting different aspects of institutional behavior that precede significant market declines (10-20% corrections).

## The Three Pillars

### Pillar 1: O'Neil - Distribution Day Accumulation

**Source:** William O'Neil, "How to Make Money in Stocks"

**Core Concept:** Institutional investors (mutual funds, hedge funds, pensions) cannot sell their large positions in a single day. Their selling creates a distinctive pattern: the index declines on higher-than-previous-day volume. When these "distribution days" accumulate, it signals that smart money is systematically exiting.

**Distribution Day Definition:**
- Index declines >= 0.2% from previous close
- Volume is higher than previous day's volume
- Both conditions must be met simultaneously

**Stalling Day Definition:**
- Volume increases from previous day
- But price gain is minimal (< 0.1%)
- Indicates institutional selling into strength
- Counted at half weight (0.5 distribution days)

**25-Day Window:**
- Distribution days expire after 25 trading days
- Only the rolling 25-day count matters
- This prevents old events from distorting current assessment

**O'Neil's Warning Thresholds:**
- 4-5 distribution days in 25 trading days = "market under pressure"
- 6+ distribution days = "distribution is heavy, protect capital"
- Combined with stalling days for full picture

### Pillar 2: Minervini - Leading Stock Deterioration

**Source:** Mark Minervini, "Trade Like a Stock Market Wizard" / "Think & Trade Like a Champion"

**Core Concept:** Market tops do not appear suddenly. They develop through a process where leading stocks - the strongest performers of the previous rally - begin breaking down before the major indices. This is because institutional investors sell their biggest winners first to lock in profits.

**Key Observation from Monty Article:**
> "弱気相場の初期段階では、特定の主導株が下降トレンドに抵抗するかのように強く、上昇できるという印象を与えます。"
> (In the early stages of a bear market, certain leading stocks appear to resist the downtrend, giving the impression they can still rise.)

**Detection Method:**
Using a basket of growth/innovation ETFs as proxy for market leadership:
- ARKK (Innovation), WCLD (Cloud), IGV (Software)
- XBI (Biotech), SOXX/SMH (Semiconductors)
- KWEB (China Tech), TAN (Solar)

**Deterioration Signals per ETF:**
1. Distance from 52-week high (>10% = concerning, >25% = bear territory)
2. Price below 50-day moving average
3. Price below 200-day moving average
4. Formation of lower highs pattern

**Amplification Rule:** When 60%+ of leading ETFs show deterioration, the signal is amplified by 1.3x. This reflects the systemic nature of leadership breakdown.

### Pillar 3: Monty - Defensive Sector Rotation

**Source:** monty-trader.com "米国株 株式相場の天井の見極め方と下落局面でやるべきこと"

**Core Concept:** Before a market top, capital flows from offensive/growth sectors into defensive/value sectors. This "rotation" occurs because institutional investors are becoming defensive while maintaining their equity allocation. It's a critical early warning signal.

**Defensive Sectors (Safety Seekers):**
- XLU (Utilities) - stable cash flows, bond-like
- XLP (Consumer Staples) - recession-resistant demand
- XLV (Healthcare) - non-discretionary spending
- VNQ (Real Estate) - income-focused

**Offensive Sectors (Growth/Risk):**
- XLK (Technology) - growth-dependent
- XLC (Communication Services) - ad-spend sensitive
- XLY (Consumer Discretionary) - economically sensitive
- QQQ (NASDAQ 100) - tech-heavy growth proxy

**Signal:** When defensive sectors outperform offensive sectors over a 20-day rolling period, capital is flowing defensively. A relative performance spread of +3% or more is a strong warning signal.

---

## Supplementary Components

### Component 4: Market Breadth Divergence

**Concept:** When the index makes new highs but fewer stocks participate, the rally is narrowing and vulnerable. This "divergence" between index price and market breadth is a classic top signal.

**Key Metric:** Percentage of S&P 500 stocks above their 200-day moving average.
- Healthy market: >70% of stocks above 200DMA
- Warning zone: 50-70% with index near highs
- Critical: <50% with index at highs

**Important Nuance:** Breadth divergence is most meaningful when the index is near its 52-week high (within -5%). If the index has already corrected significantly, weak breadth is expected and less informative.

### Component 5: Index Technical Condition

**Moving Average Structure:**
- Healthy: Price > 21 EMA > 50 EMA > 200 SMA
- Deteriorating: Any of these relationships inverting
- Bearish: Price below all major moving averages

**Pattern Recognition:**
- Failed Rally: Price bounces but fails to exceed recent peak
- Lower Highs: Sequential swing highs declining
- Gap Downs on Volume: Institutional panic selling

### Component 6: Sentiment & Speculation

**VIX (Fear Index):**
- <12: Extreme complacency (warning)
- 12-16: Low volatility (mild warning)
- 16-20: Normal
- >25: Fear elevated (top less likely, correction may be underway)

**Put/Call Ratio:**
- <0.60: Extreme call buying (maximum complacency)
- 0.60-0.70: Elevated optimism
- 0.70-0.80: Mildly bullish
- >0.80: Healthy caution

**VIX Term Structure:**
- Steep Contango: Market expects calm (complacency signal)
- Backwardation: Hedging demand elevated (fear present)

---

## Follow-Through Day (FTD) Monitor

O'Neil's concept for bottom confirmation, relevant when composite score > 40:

1. **Rally Attempt Day:** First day the index closes up after a decline
2. **Counting begins:** Day 1 of potential new uptrend
3. **Follow-Through Day:** On days 4-7 of rally attempt, a strong gain (1.5%+) on higher volume than previous day
4. **Significance:** "The most powerful uptrends usually begin with a Follow-Through Day on day 4-7"

**False FTD Rate:** Approximately 25% of FTDs fail. Multiple FTDs increase confidence.

---

## Scoring Philosophy

### Why Weighted Composite?

No single indicator perfectly predicts market tops. Each pillar captures a different dimension:
- Distribution Days: Direct measurement of institutional selling
- Leading Stocks: Quality of market leadership
- Defensive Rotation: Institutional positioning shift
- Breadth: Market participation health
- Technicals: Price structure integrity
- Sentiment: Psychological extremes

### Weight Rationale

- **Distribution Days (25%):** Most direct measure of institutional behavior
- **Leading Stocks (20%):** Minervini's strongest conviction signal
- **Defensive Rotation (15%):** Monty's key differentiator
- **Breadth (15%):** Classic confirmation signal
- **Technicals (15%):** Structural integrity check
- **Sentiment (10%):** Context and extremes (less reliable alone)

### Heuristic Design Targets

The heuristic scoring was designed around the following illustrative targets; these are not measured calibration results:
- A "normal" healthy market scores 10-20
- An "early warning" market scores 25-40
- A market in the "initial to middle stage of top formation" scores 40-55
- A clear top formation scores 60-80
- A completed top with breakdown scores 80+

### Referencia: references/point_in_time_evaluation.md

# Point-in-time evaluation protocol v1

Status: specification only; no dataset or measured calibration results are supplied.
The existing four historical component vectors are illustrative retrospective
estimates and must never be substituted for archived observations.

## Frozen estimand and score

Before collecting outcomes, freeze a manifest with protocol version `market-top-pit-v1`,
score version `market-top-risk-v1`, code commit, configuration hash, provider versions,
universe-selection rules, missing-data policy and calendar version. Preserve the
current weights, correlation discount and availability-based redistribution in the
score implementation. Record all six raw components, availability flags, adjusted
components, effective weights and final score. Do not pool different availability
masks or score versions when reporting band frequencies.

Define the primary event as an S&P 500 closing-price loss of at least 10% relative
to the as-of close at any of the next 40 trading-session closes. This operational
correction event does not identify a literal local market top. Freeze this endpoint;
other horizons (10/20 sessions) and thresholds (15/20%) are secondary and reported
separately, without replacing a disappointing primary result.

## Versioned dataset specification

Store immutable UTF-8 JSONL observations and a JSON manifest with file SHA-256 hashes.
One observation per Friday session close (last session of a holiday week); sample
all eligible weeks, including ordinary/non-event periods, without top-based selection.
Each row contains:

- `schema_version`: `market-top-pit-v1`; unique `observation_id`, `as_of` (UTC),
  exchange session date, score version, code commit and configuration hash.
- `inputs`: immutable artifact URI and SHA-256 for every input; source, vintage,
  publication time, retrieval time, original timezone and maximum observation time.
  Every observation/publication must be no later than `as_of`. Retrieval after
  `as_of` is acceptable only for a verifiable archived vintage available then.
- Point-in-time basket membership and selection evidence (including delisted names);
  six raw scores and availability flags, adjustments, effective weights and final score.
- `split`: development or holdout; `label_status`: pending, complete or excluded;
  forward 40 session dates/closes, as-of close, minimum forward return and event boolean.
  Outcome data lives separately from scoring inputs and is never read by scoring.
- Exclusion reason for unverifiable vintage, missing calendar/prices, unavailable
  required inputs or incomplete horizon. Never encode excluded/pending as non-events.

No historical live `--as-of` run is valid evidence: the current CLI rejects it because
live quotes are not archived point-in-time quotes. A future offline replay must read
only hashed archived inputs and reproduce component/score outputs before evaluation.

## Chronological evaluation and leakage controls

Pre-register a date range and split: development 2000-01-01 through 2015-12-31;
holdout 2016-01-01 through 2025-12-31. Purge development observations whose 40-session
outcome crosses the holdout boundary. If these dates cannot be reconstructed from
verifiable vintages, report infeasible and pre-register a new untouched prospective
holdout; do not manufacture history. These periods are protocol choices, not results.
Fit any thresholds solely on development data, freeze hashes before opening holdout
outcomes, and evaluate the holdout once. Record previous exposure to holdout data;
if already used for tuning it cannot be described as untouched.

## Reproducibility and reporting contract

A future evaluator must validate input hashes/timestamps, reconstruct scores from
archived inputs, label complete horizons, enforce split/purge rules, then emit a
versioned JSON metrics artifact plus a human report. Fixed inputs and code must
produce identical rows/metrics; missing vintages stop that observation with a reason.

Use fixed score bands [0,20], (20,40], (40,60], (60,80], (80,100]. For each split,
availability mask and band, report n, events, non-events, empirical event rate and
95% Wilson interval. These are observed frequencies, not a new probability model.
At a predeclared score >60 alert threshold report TP/FP/FN/TN, false alarms (FP),
misses (FN), precision, recall and coverage; undefined denominators yield null.
Report pending/excluded counts and reasons separately. Since weekly 40-session
outcomes overlap, Wilson intervals are descriptive only: also report uncertainty
using a moving-block bootstrap (52-week blocks, 2,000 replicates, fixed seed 515),
flag insufficient blocks/samples, and publish split-level counts. Never imply
independent trials. Publish non-event and event examples with provenance.

A trained probability mapping requires a separate version, development-only fitting
and untouched holdout calibration metrics. Until those measured results exist, retain
`calibrated_probability: false`. The 15-point analogue tolerance is heuristic and
cannot be tuned against these illustrative historical vectors to claim validation.


---

## SKILL: next-best-action

- Fuente: `JoelLewis/finance_skills` → `plugins/advisory-practice/skills/next-best-action` (MIT)
- Cuándo usarla: Design and implement next-best-action engines that surface proactive, prioritized recommendations to advisors based on portfolio, life, market, and compliance events. Use when the user asks about building event-driven advisor alerts, designing trigger logic for portfolio drift or large cash movements, prioritizing competing actions across a book of business, routing NBA recommendations to the right team member, measuring NBA acceptance rates, or automating compliance-driven actions like annual review reminders. Also trigger when users mention 'next best action', 'advisor nudges', 'proactive outreach', 'what should I do for this client', 'event-driven triggers', 'action queue', 'client contact gap', 'RMD reminder', or 'advisor productivity tool'.

# Next-Best-Action — Event-Driven Advisor Recommendations

## Core Concepts

### Next-Best-Action Framework
Next-best-action is an advisor productivity and client service methodology that analyzes client data across systems to surface the single most valuable action an advisor should take for each client at any given time. The concept originates in CRM and marketing automation — industries that have long used event-driven recommendation engines to guide customer-facing personnel toward high-value interactions — but its application in wealth management addresses a distinct set of challenges: advisors managing hundreds of client relationships cannot manually monitor every portfolio, life event, compliance deadline, and practice touchpoint across their entire book of business.

NBA differs fundamentally from traditional task management. Traditional task management is reactive and manual: advisors create their own to-do lists, respond to inbound client requests, and rely on memory or periodic reviews to identify outreach opportunities. NBA is proactive and data-driven: the system continuously monitors client data across custodial feeds, CRM records, financial plans, compliance calendars, and market data, automatically identifying situations that warrant advisor attention and recommending specific actions with supporting context.

The core components of an NBA system are:

- **Event detection** — Continuous monitoring of data sources to identify triggering events (portfolio drift, large cash movement, life milestone, compliance deadline, market dislocation).
- **Action identification** — Mapping detected events to a catalog of recommended actions (schedule review, propose rebalancing, discuss tax-loss harvesting, update beneficiaries).
- **Prioritization** — Scoring and ranking competing actions across all clients to ensure advisors focus on the highest-value activities given limited time.
- **Routing** — Directing each action to the appropriate person based on role, expertise, relationship, and availability.
- **Delivery** — Presenting recommendations through the channels advisors actually use (dashboard, mobile notification, email digest, CRM task).
- **Tracking** — Recording action outcomes (accepted, deferred, rejected, completed) to close the feedback loop and improve future recommendations.

### Event Detection and Trigger Types
The quality of an NBA system depends on the breadth and reliability of its event detection. Events fall into five categories, each requiring different data sources and detection logic.

**Portfolio events** are detected from custodial data feeds, portfolio management systems, and market data:

- Drift beyond threshold — A client's actual allocation has deviated from the target model beyond the firm's tolerance band (e.g., equity allocation at 72% vs. 65% target with a 5% tolerance). Requires real-time or daily position data and model assignment.
- Large cash deposit or withdrawal — A significant cash movement (typically defined by absolute amount or percentage of portfolio) has occurred. Detected from custodial transaction feeds. A $200,000 deposit into a $1 million account signals an investment opportunity; a $200,000 withdrawal from the same account may signal a liquidity event requiring plan reassessment.
- Concentrated position — A single holding has grown to exceed a concentration threshold (e.g., 10% or 15% of portfolio value), whether through appreciation, additional purchases, or stock compensation vesting. Detected from position-level holdings data.
- Tax-loss harvesting opportunity — Unrealized losses in taxable accounts exceed a significance threshold, particularly near year-end or after market declines. Requires lot-level cost basis data and market prices.
- Required minimum distribution (RMD) due — A client with a traditional IRA or inherited IRA is approaching or has reached an RMD deadline. Requires account type data and client date of birth. RMD deadlines are absolute (December 31 for most, April 1 of the following year for the year the owner turns 73).
- Margin call — A client's margin account has breached maintenance requirements. Requires margin balance and equity data from the custodian. Margin calls are time-sensitive and typically require same-day or next-day resolution.

**Life events** are detected from CRM data, client-reported information, and public records:

- Birthday milestones — Age-based financial triggers: 59-1/2 (penalty-free IRA withdrawals), 62 (early Social Security eligibility), 65 (Medicare eligibility), 70-1/2 (qualified charitable distributions from IRAs), 73 (RMD beginning age under SECURE 2.0 for those born 1951-1959). Detected from client date of birth in CRM.
- Marriage, divorce, death of spouse — Major life transitions requiring comprehensive financial plan review, beneficiary updates, account re-titling, and potentially revised investment strategy. Typically detected through advisor-reported CRM updates or client-initiated contact.
- New child or grandchild — Triggers discussions about education savings (529 plans), life insurance review, estate plan updates, and beneficiary designation changes.
- Job change or retirement — Income changes, employer benefit transitions (401k rollover), stock option/RSU vesting acceleration, and potential shift in investment time horizon and risk profile.

**Market events** are detected from market data feeds, portfolio analytics, and research systems:

- Sector or asset class drawdown affecting client holdings — A significant decline in a sector or asset class in which the client has meaningful exposure. Requires mapping client holdings to sectors and monitoring sector-level returns.
- Interest rate change impacting fixed income allocation — Significant rate movements that affect the duration risk, yield, or relative value of a client's fixed income holdings. Particularly relevant for clients with large bond allocations or approaching income-distribution phase.
- New fund or product launch replacing a current holding — A lower-cost, better-performing, or more tax-efficient alternative to a fund currently held by clients. Detected through product research and comparison analytics.

**Compliance events** are detected from compliance calendars, CRM activity logs, and regulatory data:

- Annual review overdue — The client has not received a formal portfolio or suitability review within the firm's required interval (typically 12 months). Detected by comparing the last review date in CRM to the current date.
- Suitability or best-interest re-certification due — Client profile information is stale and requires re-confirmation. Particularly important under Reg BI, where the care obligation requires that recommendations reflect current client circumstances.
- Disclosure delivery required — New regulations or rule amendments require delivery of updated disclosures (Form CRS updates, Form ADV amendments, privacy notices) to existing clients.

**Practice events** are detected from CRM activity tracking and practice management data:

- Client contact gap — A client has not been contacted (by any channel) within the firm's service standard for that client's tier. For example, a Tier 1 client ($5M+ AUM) with a quarterly contact standard who has not been contacted in 100 days.
- Upcoming contract renewal — An advisory agreement renewal or fee schedule review is approaching.
- Referral opportunity — A client has recently had a positive experience (strong performance period, successful financial plan milestone, positive service interaction) that presents a natural referral conversation opportunity.

### Action Library and Recommendation Logic
The action library is the catalog of all actions the NBA system can recommend. Each action is a defined, repeatable unit of advisor work with associated templates, context requirements, and completion criteria.

**Action catalog design.** A well-designed action library typically includes 30 to 60 distinct actions organized by category. Examples:

- Schedule annual review meeting
- Propose portfolio rebalancing to target model
- Discuss tax-loss harvesting opportunity with estimated tax savings
- Recommend Roth IRA conversion analysis (relevant for clients in temporarily low tax brackets)
- Update beneficiary designations following life event
- Review life insurance coverage adequacy
- Discuss estate plan review (triggered by legislative change, asset growth, or family change)
- Contact client regarding large uninvested cash position
- Congratulate client on life milestone (birthday, retirement, grandchild)
- Offer financial planning engagement to investment-only client
- Present charitable giving strategy (donor-advised fund, qualified charitable distribution)
- Discuss Social Security claiming strategy (approaching eligibility age)
- Review held-away account for consolidation opportunity
- Deliver required compliance disclosure

**Action templates.** Each action in the library includes pre-built supporting materials that reduce the advisor's preparation time and increase the likelihood of action completion:

- Talking points — Key discussion topics tailored to the specific trigger and client context (e.g., "Your portfolio has drifted to 72% equities vs. your 65% target. I recommend we rebalance by trimming the overweight in large-cap growth and adding to international and fixed income. This trade would also harvest approximately $12,000 in losses to offset the gains we realized earlier this year.").
- Email drafts — Pre-composed outreach emails personalized with client name, specific trigger details, and proposed next steps. The advisor reviews and edits before sending.
- Meeting agendas — Structured agendas for review meetings, planning discussions, or specific topic conversations.
- Analysis summaries — Pre-generated quantitative analysis (drift report, tax-loss harvesting estimate, RMD calculation, fee comparison) attached to the recommendation.

**Recommendation logic.** NBA systems use two primary approaches to map triggers to actions:

- Rule-based logic — Deterministic IF-THEN rules that map specific triggers to specific actions. Example: IF client age reaches 72 AND has traditional IRA AND no RMD distribution recorded this year THEN recommend "Contact client re: RMD before December 31 deadline." Rule-based logic is transparent, auditable, and appropriate for compliance-driven and well-understood triggers.
- ML-enhanced logic — Machine learning models that learn from historical advisor behavior to improve recommendations. The model observes which recommended actions advisors accept or reject, which actions lead to positive outcomes (client retention, additional assets, completed plans), and which client characteristics predict action relevance. ML enhancement is layered on top of rule-based logic — rules ensure required actions are never missed, while ML improves the ranking and presentation of discretionary actions.

### Prioritization and Scoring
Not all actions are equal. An advisor with 200 clients might have 50 pending actions on any given day, but can realistically complete five to seven. Prioritization scoring determines which actions rise to the top of the queue.

**Scoring dimensions.** Effective prioritization considers multiple dimensions, each scored on a normalized scale:

- **Urgency** — How time-sensitive is the action? An RMD deadline in December is more urgent in November than in March. A margin call is urgent immediately. A referral opportunity is low urgency. Urgency scoring should incorporate hard deadlines (compliance dates, regulatory deadlines) and soft deadlines (optimal timing windows that pass but do not create violations).
- **Impact** — What is the potential benefit of completing the action? Impact can be measured along several sub-dimensions: revenue potential (will the action lead to new assets, a planning engagement, or retained AUM?), retention risk (is the client at risk of leaving if this issue is not addressed?), compliance requirement (is the action mandated by regulation or firm policy?), client satisfaction (will the action strengthen the relationship?).
- **Effort** — How much advisor time and preparation does the action require? A quick congratulatory call requires five minutes; a comprehensive financial plan review requires several hours of preparation and a 90-minute meeting. Effort scoring ensures that the queue includes a realistic mix of quick wins and substantial engagements.
- **Client importance** — What is the client's tier, AUM, relationship depth, and strategic value? Most firms weight actions for higher-tier clients more heavily, reflecting the disproportionate business impact of retaining and deepening large relationships. However, this weighting should not result in lower-tier clients being systematically neglected — compliance-driven and risk-driven actions should override tier-based scoring.

**Composite scoring.** The overall priority score is a weighted combination of dimension scores:

Priority = (W_urgency x Urgency) + (W_impact x Impact) - (W_effort x Effort) + (W_client x ClientImportance)

Weights are calibrated to the firm's strategic priorities. A firm focused on growth may weight impact and client importance heavily. A firm under regulatory scrutiny may weight urgency and compliance-driven impact heavily. Weights should be reviewed and adjusted periodically based on business outcomes.

**Priority queue management.** Queue design prevents action fatigue — the phenomenon where advisors ignore recommendations because the system generates too many:

- Cap the daily queue at five to seven actions per advisor — a practical rule of thumb (not a cited research finding): larger queues tend to depress completion rates and breed action fatigue.
- Ensure the queue includes a mix of action types — not exclusively compliance items or exclusively revenue-driven items.
- Allow advisors to defer actions (with a snooze period) without permanently dismissing them. Deferred actions return to the queue after the snooze period with an adjusted priority score.
- Compliance-driven actions with approaching deadlines should be flagged as non-deferrable once they enter a critical window (e.g., within 15 days of the deadline).

**Advisor capacity consideration.** The NBA system should account for advisor availability when generating queues. An advisor returning from vacation faces a backlog; an advisor with a light meeting day has capacity for a complex action. Integration with the advisor's calendar and CRM activity log enables capacity-aware queue generation.

### Action Routing and Assignment
Not every action requires the advisor's personal attention. Effective routing directs each action to the right person based on the nature of the work, the relationship requirement, and the team structure.

**Role-based routing rules:**

- **Advisor** — Relationship decisions, complex discussions, high-value client interactions, investment strategy conversations, financial planning reviews. The advisor handles actions where the personal relationship and professional judgment are essential.
- **Client service associate (CSA)** — Scheduling meetings, document collection, routine follow-up calls, account maintenance requests, birthday and milestone acknowledgments (if the firm delegates these). CSAs handle actions that are important but do not require the advisor's expertise.
- **Operations team** — Account transfers, beneficiary designation processing, cost basis corrections, distribution processing, account opening paperwork. Operations handles actions that involve back-office execution.
- **Compliance team** — Regulatory disclosure delivery, suitability re-certification review, advertising review items, compliance-exception resolution. Compliance handles actions that require regulatory expertise or supervisory approval.

**Escalation rules.** Actions that are not completed within their service-level agreement (SLA) should escalate automatically:

- Level 1 (approaching SLA) — Visual indicator in the dashboard (color change from green to yellow).
- Level 2 (at SLA) — Push notification to the assigned individual and their supervisor.
- Level 3 (past SLA) — Escalation to the practice manager or branch manager, with the overdue action flagged in management reports.
- Level 4 (compliance actions past SLA) — Escalation to the Chief Compliance Officer, with the overdue action logged as a compliance exception.

**Team-based routing.** In team-based advisory practices, routing rules should consider advisor specialization (tax planning, estate planning, retirement income), current workload, and client assignment. If the primary advisor is unavailable, the system should route time-sensitive actions to a designated backup advisor rather than allowing them to age in the queue.

### Delivery Channels and Nudges
The most carefully prioritized recommendation is worthless if the advisor never sees it. Delivery channel design and nudge formatting directly affect adoption rates.

**Delivery channels:**

- **Dashboard widget (morning briefing)** — A dedicated section of the advisor's home screen displaying the day's priority queue. The morning briefing is the primary delivery channel for most NBA implementations, designed to be the first thing the advisor reviews each day. Effective morning briefings display the top five to seven actions ranked by priority, with a one-line summary and the client name for each.
- **Push notifications (mobile and desktop)** — Real-time alerts for urgent, time-sensitive actions (margin call, large cash deposit, compliance deadline within 48 hours). Push notifications should be reserved for genuinely urgent items to avoid notification fatigue.
- **Email digest (daily or weekly)** — A summary email listing pending actions, upcoming deadlines, and completed actions from the prior period. The email digest serves as a secondary channel and a record that the advisor can reference outside the dashboard. Weekly digests work well for practice-level summaries; daily digests suit high-volume practices.
- **CRM task creation** — NBA recommendations automatically create tasks in the firm's CRM system, ensuring that actions are tracked in the advisor's existing workflow tool. CRM integration is critical for adoption — if advisors must check a separate system for NBA recommendations, adoption will be low.
- **Calendar integration** — For actions involving client meetings, the system can auto-suggest or auto-block calendar time based on the client's preferred meeting times and the advisor's availability. This reduces the friction between "I should schedule a review with this client" and actually scheduling it.

**Nudge design.** A nudge is the atomic unit of NBA delivery — the brief, actionable message that presents the recommendation to the advisor. Effective nudges share several characteristics:

- Brief — Two to three sentences maximum for the initial display. The advisor should be able to read the nudge in under 10 seconds and decide whether to act.
- Contextual — The nudge includes enough client-specific information that the advisor understands why the action matters without opening the full client record. Include the trigger event, the relevant data point, and the recommended action.
- Actionable — The nudge includes a clear call to action and a direct link to execute it. "John Smith deposited $150K yesterday. His portfolio is now 12% cash vs. 3% target -- recommend investing per his growth model. [View Account] [Create Proposal]."
- Prioritized — Visual cues (color coding, icons, position in the queue) communicate the action's priority relative to other items.

**Timing.** When nudges are delivered affects adoption:

- Morning delivery (7:00-8:00 AM) for the daily priority queue, so advisors start the day with a clear action plan.
- Real-time delivery for urgent items (margin calls, same-day compliance deadlines, large cash movements).
- Post-market-close delivery for performance-related triggers (drawdown alerts, drift notifications) that should not interrupt the trading day.
- End-of-week delivery for practice-level summaries and the following week's preview.

### Client Context and Personalization
Effective NBA recommendations require deep client context. A generic "call this client" recommendation is far less actionable than a recommendation that explains why the call matters and provides client-specific talking points.

**Context assembly.** When an event triggers an NBA recommendation, the system should assemble a context package that includes:

- **Investment profile** — Current allocation, target model, risk profile, investment objectives, account types, tax status, cost basis summary.
- **Financial plan status** — Current plan (if any), funded status of goals, Monte Carlo probability, key assumptions, upcoming milestones. A client whose retirement plan is 95% funded requires a different conversation than one at 60%.
- **Recent interactions** — Last contact date, last meeting date, topics discussed, outstanding action items from prior meetings, recent service requests. The advisor should not call a client unaware that the client called the service desk with a complaint yesterday.
- **Communication preferences** — Preferred contact method (phone, email, video), preferred meeting time, preferred frequency. Respecting preferences increases engagement and demonstrates attentiveness.
- **Life stage and upcoming events** — Current life stage (accumulation, pre-retirement, distribution, legacy), upcoming milestones (age-based, contract-based), recent life events.
- **Household context** — Spouse/partner information, dependent children, other family members who are also clients, household-level asset aggregation, estate plan status.

**Personalization.** The recommended action and its supporting materials should reflect the specific client's situation:

- Talking points should reference the client's specific holdings, goals, and circumstances — not generic advice.
- Analysis summaries should use the client's actual data (actual drift amount, actual tax-loss estimate, actual RMD calculation).
- Email drafts should reflect the client's communication style and relationship tone (formal vs. informal, detail-oriented vs. summary-focused).

**Historical context.** The system should track the history of NBA recommendations for each client:

- What actions were previously recommended? Did the advisor accept, defer, or reject them?
- Were deferred actions eventually completed?
- What was the client's response to prior outreach driven by NBA recommendations?

This history prevents repetitive recommendations (do not recommend the same action that was rejected last week) and enables trend analysis (a client who consistently defers review meetings may need a different engagement approach).

### Workflow Integration
NBA delivers maximum value when the recommendation connects seamlessly to the execution workflow. Clicking "Propose Rebalancing" should not just remind the advisor to rebalance — it should open the rebalancing tool with the client's accounts pre-loaded, the current drift analysis displayed, and the proposed trades ready for review.

**Execution workflow connections:**

- "Propose Rebalancing" opens the portfolio management system with the client's account, current vs. target allocation, and proposed trades pre-populated.
- "Schedule Review" opens the calendar with the client's preferred meeting times highlighted, a pre-built agenda template attached, and a draft invitation email ready to send.
- "Send Tax-Loss Report" generates the tax-loss harvesting analysis from the portfolio system, formats it into the firm's reporting template, and queues it for delivery through the client's preferred channel.
- "Update Beneficiaries" opens the account maintenance workflow with the client's current beneficiary designations displayed and a form pre-populated with the client's information.
- "Deliver Disclosure" queues the required document for delivery through the firm's document delivery system, with tracking confirmation.

**CRM activity logging.** When an advisor completes an NBA-recommended action, the system should automatically log the activity in the CRM:

- Record the trigger event, recommended action, advisor action (accepted/deferred/rejected), completion timestamp, and outcome.
- Link the activity to the client record and the advisor record.
- If the action involved a client interaction, log the interaction details (date, method, duration, topics, next steps).

Automatic logging eliminates the manual data entry that advisors routinely skip, ensuring that the CRM reflects actual practice activity and providing the data foundation for relationship tracking, compliance documentation, and practice analytics.

**Feedback loop.** Advisor acceptance and rejection of NBA recommendations should feed back into the system to improve future recommendations:

- Track acceptance rates by action type, trigger type, advisor, and client segment.
- Identify actions that are consistently rejected and investigate whether the trigger logic, prioritization, or action template needs refinement.
- Identify advisors with low acceptance rates and determine whether the issue is action quality, delivery timing, or advisor engagement.
- Use acceptance/rejection data to train ML models that improve action ranking and personalization over time.

### Compliance-Driven Actions
NBA systems serve a dual purpose: enhancing advisor productivity and ensuring compliance-mandated actions are completed on time. Compliance-driven NBA actions differ from discretionary actions in several important ways.

**Examples of compliance-driven NBA actions:**

- Annual suitability review or best-interest review due for a client whose last review was 11 months ago.
- Form CRS delivery required because the firm filed an amended Form CRS and must deliver the updated version to existing clients.
- Best-interest documentation needed for a recent recommendation that lacks the required documentation under Reg BI.
- Account restriction review required — a restricted account (e.g., deceased account holder, legal dispute, regulatory freeze) requires periodic review and cannot be traded until the restriction is resolved.
- Annual privacy notice delivery due under Reg S-P.
- Client identity verification incomplete — CIP documentation gap identified during periodic review.

**Non-dismissible actions.** Unlike discretionary actions (where an advisor can reasonably decide that a referral conversation is not appropriate this week), compliance-driven actions cannot be ignored or permanently dismissed without supervisory override. The system should enforce this:

- Compliance actions cannot be snoozed beyond their regulatory deadline.
- Dismissal of a compliance action requires entry of a reason and supervisor approval.
- Overdue compliance actions are automatically escalated per the escalation rules.

**Audit trail.** All compliance-driven NBA actions must maintain a comprehensive audit trail:

- Timestamp of trigger detection (when the system identified the compliance event).
- Timestamp of action creation (when the recommendation was generated).
- Timestamp of advisor notification (when the recommendation was delivered).
- Advisor response (accepted, deferred with date, escalated).
- Completion timestamp and evidence (meeting notes, signed documents, delivery confirmation).
- Responsible party (the individual who completed the action).
- Supervisor acknowledgment (for escalated or overdue items).

This audit trail serves as evidence of supervisory oversight during regulatory examinations. When an SEC or FINRA examiner asks, "How do you ensure that all clients receive annual reviews?" the firm can produce the NBA compliance log showing trigger dates, notification dates, completion dates, and escalation records for every client.

### Measurement and Optimization
An NBA system that cannot measure its own effectiveness cannot improve. Measurement frameworks should track both operational metrics (is the system working?) and outcome metrics (is the system creating value?).

**Operational metrics:**

- **Action acceptance rate** — What percentage of recommended actions do advisors accept and complete? As an illustrative planning target (not an industry-verified statistic), a mature implementation might aim for 60-75% acceptance; persistent rates below 40% suggest the recommendations are not relevant or the delivery is not effective.
- **Time-to-action** — How quickly are accepted actions completed after recommendation? Measure the distribution, not just the average. A median of two days with a long tail of 30+ day completions indicates a queue management problem.
- **Queue utilization** — What percentage of the daily queue capacity (five to seven actions) is being used? Persistent under-utilization suggests insufficient triggers or overly conservative scoring. Persistent over-utilization (advisors consistently receiving more actions than they can complete) suggests the cap needs adjustment or the practice needs additional staff.
- **Trigger accuracy** — What percentage of detected events actually warrant an action? False positive triggers (e.g., flagging a cash deposit that the client has already discussed with the advisor) reduce trust in the system.
- **Compliance completion rate** — What percentage of compliance-driven actions are completed before their deadline? Target: 100% for hard regulatory deadlines, 95%+ for firm-imposed deadlines.

**Outcome metrics:**

- **Revenue impact** — Do clients who receive NBA-driven outreach produce more revenue (through additional assets, planning engagements, or product adoption) than comparable clients who do not? This requires careful measurement with appropriate controls, as NBA-targeted clients may differ systematically from non-targeted clients.
- **Retention impact** — Is the client retention rate higher for clients who receive regular NBA-driven advisor contact? Retention is a lagging indicator, so firms should also track leading indicators like client satisfaction scores and engagement frequency.
- **Advisor productivity** — Are advisors completing more client-facing activities per day/week after NBA implementation? Measure both quantity (number of client interactions) and quality (actions that lead to outcomes vs. check-the-box contacts).

**Continuous improvement:**

- A/B testing — Compare different action templates, delivery times, and nudge formats to identify what drives higher acceptance and completion rates. Run tests within advisor cohorts to control for individual differences.
- Advisor feedback — Collect qualitative input from advisors on action quality, relevance, and timing through periodic surveys and advisory councils. Advisors who feel the system works for them become champions; advisors who feel it works against them become resisters.
- Trigger refinement — Periodically review trigger thresholds and logic. If 80% of drift-triggered rebalancing actions are deferred because the drift is near the threshold but not compelling, the threshold may be too tight. If large-cash-deposit actions are consistently accepted, the system is working well for that trigger type.
- Template refresh — Update action templates (talking points, email drafts, analysis summaries) based on advisor feedback and changing market conditions. Templates that reference outdated market themes or stale data points undermine credibility.

## Worked Examples

See [references/examples.md](references/examples.md) for three end-to-end worked examples — designing an NBA engine for a 15-advisor RIA (trigger catalog, scoring weights, sample queue), a large-cash-deposit trigger flowing through the full workflow, and a compliance-driven annual-review completion system. Load it when the user needs a full scenario walkthrough.

## Common Pitfalls
- Generating too many actions per advisor per day, causing action fatigue and system abandonment — cap daily queues at five to seven items and invest in prioritization quality over trigger quantity.
- Implementing NBA as a standalone system disconnected from the CRM, portfolio management, and financial planning tools — if advisors must check a separate system, adoption will fail; NBA must integrate into existing workflows.
- Relying entirely on rule-based logic without incorporating advisor feedback — rules that generate irrelevant or poorly timed recommendations erode trust; build feedback mechanisms from day one.
- Treating all actions as equal priority — without a robust scoring model, compliance deadlines, revenue opportunities, and routine touchpoints compete for the same queue positions, and important items get buried.
- Designing nudges that lack client-specific context — a generic "Contact this client" recommendation provides no value; nudges must include the trigger reason, relevant data, and a specific recommended action.
- Failing to connect NBA recommendations to execution workflows — if clicking "Propose Rebalancing" merely creates a reminder rather than opening the rebalancing tool with the client's data pre-loaded, the system adds overhead instead of reducing it.
- Making compliance-driven actions dismissible without supervisory oversight — compliance items must be non-deferrable past their regulatory deadline, with escalation to supervisors and the CCO.
- Not tracking action outcomes (acceptance, completion, client response) — without outcome data, the system cannot improve, and the firm cannot measure the return on its NBA investment.
- Ignoring advisor capacity when generating queues — recommending seven complex actions on a day when the advisor has six hours of meetings is counterproductive.
- Deploying the system without advisor input on trigger thresholds, action templates, and delivery preferences — top-down implementation without advisor buy-in consistently produces low adoption rates.
- Omitting the audit trail for compliance-driven actions — the entire compliance value of NBA depends on the ability to produce timestamped, complete records during regulatory examinations.
- Allowing the action library to become stale — talking points referencing outdated market conditions, email templates with old branding, or analysis summaries using last year's data undermine the system's credibility.

## Cross-References
- **crm-client-lifecycle** (advisory-practice plugin) — CRM activity records, client segmentation, and lifecycle data are primary inputs for NBA triggers; every NBA action updates the CRM.
- **portfolio-management-systems** (advisory-practice plugin) — Portfolio events (drift, cash position, concentrated holdings, performance) are a primary category of NBA triggers; the portfolio management system provides the data feeds and execution tools.
- **advisor-dashboards** (advisory-practice plugin) — The advisor dashboard is the primary delivery channel for NBA recommendations; the morning briefing widget displays the prioritized action queue.
- **financial-planning-integration** (advisory-practice plugin) — Financial plan status changes (goal progress, funded status, assumption changes) trigger planning-related NBA actions; plan data enriches action context.
- **rebalancing** (wealth-management plugin) — Portfolio drift and rebalancing triggers are a key category of NBA events; the NBA recommendation links directly to the rebalancing workflow.
- **tax-efficiency** (wealth-management plugin) — Tax-loss harvesting opportunities detected from cost basis data trigger NBA recommendations; tax context (gain/loss position, holding periods) enriches rebalancing and investment actions.
- **investment-suitability** (compliance plugin) — Annual suitability reviews and profile re-certifications are compliance-driven NBA actions; suitability data informs the client context assembled for all NBA recommendations.
- **examination-readiness** (compliance plugin) — NBA compliance action logs (trigger timestamps, escalation records, completion evidence) serve as auditable proof of supervisory oversight during SEC and FINRA examinations.

### Referencia: references/examples.md

# Worked Examples — Next-Best-Action

### Example 1: Building an NBA engine for a 15-advisor RIA

**Scenario:** A registered investment adviser with 15 advisors collectively managing 1,200 client households ($3.2 billion AUM) is designing its first NBA engine. The firm uses a leading CRM platform, a third-party portfolio management system with custodial data feeds from two custodians, and a financial planning tool. Advisors currently manage their own task lists and rely on periodic (semi-annual or annual) review cycles to identify client needs. The firm wants to shift to a proactive, event-driven engagement model that ensures no high-value action is missed and no compliance deadline is breached.

**Design Considerations:**

The trigger catalog should cover all five event categories, calibrated to the firm's specific thresholds and data availability.

Portfolio triggers: drift beyond 5% absolute deviation from the target model (available daily from the portfolio management system); cash position exceeding 5% of portfolio value for more than 10 business days (from custodial cash balance data); single-position concentration exceeding 12% of portfolio value (from position-level holdings); unrealized tax losses exceeding $5,000 in taxable accounts (from lot-level cost basis data, available from the custodian); RMD due within 90 days (from account type and client date of birth in CRM, cross-referenced with distribution history).

Life event triggers: age milestones at 59.5, 62, 65, 70.5, and 73 (from CRM date of birth, triggered 60 days before the milestone); marriage, divorce, death of spouse, new child (from CRM life event fields, entered by advisors or CSAs during client interactions); retirement or job change (from CRM, typically advisor-reported).

Compliance triggers: annual review overdue (last review date + 365 days, from CRM activity records); client profile update due (last suitability update + 365 days, from CRM); Form ADV delivery required (triggered by firm-level compliance calendar when amendments are filed).

Practice triggers: no client contact in 90 days for Tier 1 clients, 180 days for Tier 2, 365 days for Tier 3 (from CRM activity timestamps); advisory agreement renewal within 60 days (from contract dates in CRM).

Market triggers: sector drawdown exceeding 10% in a 30-day period where the client has more than 15% exposure to the affected sector (from portfolio holdings mapped to sector classifications and market data).

The prioritization scoring model should use four dimensions with firm-specific weights. For this firm — which is growth-oriented but has had compliance findings in the past — suggested weights are: urgency 30%, impact 30%, client importance 25%, effort adjustment -15%. Urgency receives a score of 1-10 based on time sensitivity (10 for same-day compliance deadlines, 1 for opportunities with no expiration). Impact receives a score of 1-10 based on revenue potential, retention risk, and compliance requirement (compliance-mandated actions receive a floor score of 7). Client importance receives a score of 1-10 based on household AUM tier (Tier 1 above $5M = 10, Tier 2 $1-5M = 7, Tier 3 below $1M = 4). Effort receives a negative adjustment of 1-5 reflecting the time required (quick call = -1, comprehensive review = -5), ensuring that the queue does not fill with only time-intensive items.

The daily action queue is capped at six actions per advisor. The system generates the queue at 6:00 AM each morning, drawing from the scored action pool. Queue composition rules ensure variety: no more than two compliance-only items (unless hard deadlines require it), at least one quick-win action (effort score of -1 or -2) to provide a sense of accomplishment, and compliance actions with deadlines within 15 days are always included regardless of other scoring.

A sample morning queue for one advisor managing 85 client households might display:

1. Priority 9.2 — "Margaret Chen (Tier 1, $6.8M): RMD of $48,200 due by Dec 31. No distribution recorded. Contact to confirm distribution method and timing. [View RMD Calculator] [Draft Email]"
2. Priority 8.5 — "David and Susan Park (Tier 1, $5.1M): Portfolio drifted to 74% equity vs. 65% target after tech rally. Propose rebalancing with $18K tax-loss harvest in international fund. [View Drift Report] [Create Proposal]"
3. Priority 7.8 — "Robert Hartley (Tier 2, $2.3M): Turned 65 last week. Discuss Medicare enrollment, supplemental insurance review, and potential retirement income plan update. [View Financial Plan] [Schedule Meeting]"
4. Priority 7.1 — "Compliance: Patricia Alvarez (Tier 2, $1.8M): Annual review overdue by 22 days. Schedule and complete review within 15 days. [Schedule Meeting] [Generate Review Package]"
5. Priority 6.5 — "James O'Brien (Tier 3, $620K): Deposited $85K eight days ago. Cash now 18% of portfolio. Recommend investing per balanced model. [View Account] [Create Proposal]"
6. Priority 5.8 — "Lisa Yamamoto (Tier 2, $3.1M): No contact in 95 days (Tier 2 standard: 90 days). Quick check-in call recommended. [View Recent Activity] [Log Call]"

Delivery is through a dedicated dashboard widget displayed as the advisor's home screen in the CRM, with push notifications reserved for items reaching Priority 9.0+ or compliance deadlines within 48 hours.

The measurement framework tracks: weekly acceptance rate by advisor (target above 65%), average time-to-action (target under 3 business days), compliance action completion rate (target 100% before deadline), and quarterly revenue attribution (comparing AUM growth and planning engagement rates between NBA-active and pre-NBA periods).

### Example 2: Large cash deposit triggers end-to-end NBA workflow

**Scenario:** At 9:15 AM on a Tuesday, the custodial data feed reports that client Thomas Brennan deposited $200,000 into his taxable brokerage account via wire transfer. Thomas is a Tier 1 client ($4.2M total relationship) assigned to advisor Sarah Kim. His investment profile indicates a growth objective with moderate-to-aggressive risk tolerance. His current allocation is 68% equity, 22% fixed income, 10% alternatives — closely aligned with his target model of 70/20/10. The $200K deposit shifts his effective allocation to approximately 60% equity, 19% fixed income, 9% alternatives, and 12% cash.

**Design Considerations:**

The event detection layer should process custodial transaction feeds at least daily (ideally intraday for large-cash triggers). The large-cash-deposit trigger fires when: (a) a cash deposit exceeds $50,000 or 5% of the account value, AND (b) the resulting cash position exceeds the target cash allocation by more than 3 percentage points. In this case, both conditions are met: the $200K deposit exceeds $50,000, and the resulting 12% cash allocation exceeds the 0% target cash position by 12 percentage points.

Context assembly begins immediately after the trigger fires. The system gathers: (1) Thomas's investment profile from CRM — growth objective, moderate-to-aggressive risk, 15+ year time horizon, high marginal tax bracket (37% federal); (2) current portfolio composition from the portfolio management system — position-level holdings, model assignment, drift analysis showing the portfolio is now 10 percentage points underweight equity due to cash dilution; (3) financial plan status from the planning tool — retirement plan is 88% funded with current contributions, and investing the $200K would increase the funded status to approximately 93%; (4) tax situation — the taxable account has $14,000 in unrealized short-term losses in an international equity ETF and $32,000 in unrealized long-term gains in a large-cap growth fund, suggesting tax-lot-level attention during investment; (5) recent interactions from CRM — Sarah spoke with Thomas 12 days ago about a general portfolio check-in, no mention of an incoming deposit, suggesting this may be an inheritance, bonus, real estate proceeds, or other liquidity event that Sarah should understand before investing.

Action recommendation: the system recommends "Invest Large Cash Position Per Growth Model with Tax-Lot Optimization." The action template includes: talking points for Sarah's call to Thomas (congratulate/inquire about the source of funds, recommend investing per his growth model to bring allocation back to target, note the opportunity to harvest the $14K international equity loss while redeploying, explain that the investment will improve his retirement plan funded status from 88% to approximately 93%); a pre-generated trade proposal showing the specific purchases needed to restore target allocation (approximately $140K to equities across three funds, $40K to fixed income, $20K to alternatives, with tax-lot selection optimized to harvest losses); and a draft email for Thomas summarizing the recommendation.

Advisor notification: Sarah receives a push notification at 9:45 AM (within 30 minutes of the trigger event, reflecting the high priority of a large cash deposit): "Thomas Brennan deposited $200K. Portfolio now 12% cash vs. 0% target. Recommend investing per growth model. Est. tax-loss harvest: $14K. [View Proposal] [Call Thomas]." The action also appears as the top item in Sarah's morning dashboard queue with a Priority score of 8.9 (high urgency due to uninvested cash, high impact due to Tier 1 client and plan improvement, moderate effort for the call and trade execution).

Execution workflow: Sarah taps "Call Thomas" to initiate the call. During the conversation, she learns the $200K is the proceeds from selling a rental property — useful context for tax planning (Thomas may have capital gains from the property sale that the international equity losses could offset). Sarah then taps "View Proposal" to review the pre-generated trade proposal, makes a minor adjustment (increasing the international equity allocation slightly to improve diversification), and submits the trades through the order management system with the tax-lot selection preserving the loss-harvesting opportunity.

Action completion logging: when the trades are executed, the system automatically logs the completed action in CRM: trigger event (large cash deposit, $200K, detected 9:15 AM), advisor notification (9:45 AM), advisor action (accepted, called client at 10:20 AM, 18-minute call), trades submitted (10:45 AM), trades executed (11:02 AM), outcome (portfolio restored to target allocation, $14K tax loss harvested, client expressed satisfaction). The entire workflow — from cash deposit to invested portfolio — completed in under two hours.

### Example 3: Compliance-driven NBA for annual review completion

**Scenario:** A wealth management firm with 400 client households has a compliance policy requiring that every client receive a documented annual review. The firm's last FINRA examination cited a deficiency: 23% of clients had not received an annual review within the required 12-month window. The CCO is implementing a compliance-driven NBA workflow to ensure 100% annual review completion and provide auditable evidence of supervisory oversight.

**Design Considerations:**

The trigger logic uses a simple but reliable date calculation: for each client, the system compares the date of the last documented annual review (stored in CRM as a completed activity of type "Annual Review") to the current date. The trigger fires at three escalation points:

- 60-day advance notice: when (current date + 60 days) exceeds (last review date + 365 days), the system generates a "Schedule Annual Review" action. This gives the advisor two months to schedule and complete the review before the deadline. Priority score: 5.0 (moderate urgency, mandatory compliance item, standard effort).
- 30-day warning: when (current date + 30 days) exceeds (last review date + 365 days) and no review has been scheduled, the system escalates the action. The priority score increases to 7.5, the dashboard displays the item in amber, and the advisor receives a direct notification: "Annual review for [Client Name] due in 30 days. Schedule immediately. [Schedule Meeting] [Generate Review Package]."
- 15-day alert: when (current date + 15 days) exceeds (last review date + 365 days) and no review has been scheduled or conducted, the system escalates further. Priority score increases to 9.0, the dashboard displays the item in red, the advisor and the advisor's supervisor both receive notifications, and the action becomes non-deferrable. The notification to the supervisor reads: "[Advisor Name] has an annual review for [Client Name] due in 15 days — not yet scheduled. Supervisor action required."
- Overdue escalation: when the current date exceeds (last review date + 365 days) and no review has been completed, the system logs a compliance exception and notifies the Chief Compliance Officer. The CCO notification includes: client name, advisor name, original deadline, days overdue, and all prior escalation timestamps. The CCO can assign the review to another advisor, require a written explanation from the responsible advisor, or take other supervisory action.

Scheduling automation: when the advisor clicks "Schedule Meeting" from the NBA recommendation, the system should: (1) display the client's preferred meeting times and communication method from CRM; (2) cross-reference the advisor's calendar to identify available slots within the next 14 days; (3) generate a meeting invitation with a pre-built annual review agenda template; (4) upon client confirmation, automatically update the CRM with the scheduled review date and change the NBA action status to "Scheduled — Awaiting Completion."

Review preparation package generation: when a review meeting is scheduled, the system automatically generates a preparation package that includes: (a) a portfolio summary report showing current allocation, performance since last review, benchmark comparison, and drift analysis; (b) a financial plan update showing current funded status, progress toward goals, and any assumption changes needed; (c) a client profile summary showing demographic information, investment profile, risk tolerance, and any profile changes since the last review; (d) a compliance checklist covering suitability confirmation, beneficiary verification, contact information update, disclosure delivery status, and any outstanding action items from the prior review; (e) a list of all NBA-recommended actions taken for this client since the last annual review, demonstrating the ongoing service provided between reviews.

Completion tracking and compliance reporting: the review is not marked as complete until the advisor records the review activity in CRM with required fields: meeting date, attendees, topics discussed, any changes to the client profile or investment strategy, next steps, and confirmation that the suitability/best-interest review was conducted. The system validates that all required fields are populated before closing the action.

The compliance reporting dashboard provides the CCO with real-time visibility into: total clients with current annual reviews (target: 100%), clients with reviews due within 30 days (action required), clients with overdue reviews (compliance exceptions), completion rate by advisor (identifying advisors who consistently lag), and a historical trend chart showing the firm's review completion rate month-over-month.

For the FINRA examination response, the firm can produce: a system-generated report showing the trigger date, all escalation timestamps, scheduling date, completion date, and review documentation for every client — demonstrating that the firm has implemented a systematic, automated supervisory process that ensures annual review completion. This directly addresses the prior deficiency finding and demonstrates the "reasonably designed" supervisory system that FINRA expects under Rule 3110.


---

## SKILL: pumpfun-mechanics

- Fuente: `agiprolabs/claude-trading-skills` → `skills/pumpfun-mechanics` (MIT)
- Cuándo usarla: PumpFun bonding curve math, graduation mechanics, instruction parsing, and PumpSwap migration
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/pumpfun-mechanics/` (curve_calculator.py, parse_events.py)

# PumpFun Mechanics — Bonding Curves, Graduation & Instruction Parsing

PumpFun is the dominant Solana token launchpad. Understanding its bonding curve math, graduation process, and instruction formats is essential for analyzing new token launches, building trading strategies around graduation events, and parsing on-chain PumpFun activity.

## Bonding Curve Math

PumpFun uses a **virtual constant-product (CPMM)** bonding curve:

```
k = virtualSolReserves × virtualTokenReserves
```

### Initial Parameters

| Parameter | Value |
|-----------|-------|
| Initial Virtual SOL | 30 SOL (30,000,000,000 lamports) |
| Initial Virtual Tokens | ~1.073B tokens (1,073,000,000,000,000 raw, 6 decimals) |
| Token Total Supply | 1B tokens (1,000,000,000,000,000 raw) |
| Real Token Reserves | ~793M tokens (793,000,000,000,000 raw) |
| Real SOL Reserves | 0 (no real SOL at launch) |
| Fee | 1% (applied externally by the program) |

**Virtual vs Real**: Virtual reserves define the curve shape. Real reserves track actual withdrawable funds. The difference (1.073B - 793M = 280M virtual tokens) shapes the initial price but can never be withdrawn.

### Spot Price

```python
price_sol_per_token = virtual_sol_reserves / virtual_token_reserves

# In human-readable units:
price = (virtual_sol / 1e9) / (virtual_token / 1e6)

# At genesis: 30 / 1,073,000,000 ≈ 2.796e-8 SOL/token
# At graduation: ~4.1e-7 SOL/token (~14.7x from launch)
```

### Buy Tokens (SOL → Tokens)

```python
def buy_tokens(v_sol: int, v_tok: int, real_tok: int, sol_in: int) -> int:
    """Calculate tokens received for a given SOL input.

    Args:
        v_sol: Virtual SOL reserves (lamports).
        v_tok: Virtual token reserves (raw).
        real_tok: Real token reserves (raw).
        sol_in: SOL to spend (lamports, BEFORE 1% fee).

    Returns:
        Tokens received (raw units).
    """
    k = v_sol * v_tok
    new_v_sol = v_sol + sol_in
    new_v_tok = k // new_v_sol + 1  # +1 matches on-chain rounding
    tokens_out = v_tok - new_v_tok
    return min(tokens_out, real_tok)
```

### Sell Tokens (Tokens → SOL)

```python
def sell_tokens(v_sol: int, v_tok: int, real_sol: int, tokens_in: int) -> int:
    """Calculate SOL received for selling tokens.

    Args:
        v_sol: Virtual SOL reserves (lamports).
        v_tok: Virtual token reserves (raw).
        real_sol: Real SOL reserves (lamports).
        tokens_in: Tokens to sell (raw units).

    Returns:
        SOL received (lamports, BEFORE 1% fee).
    """
    k = v_sol * v_tok
    new_v_tok = v_tok + tokens_in
    new_v_sol = k // new_v_tok
    sol_out = v_sol - new_v_sol - 1  # -1 matches on-chain floor rounding
    return min(sol_out, real_sol)
```

### Buy Cost (Exact token amount → SOL needed)

```python
def buy_cost(v_sol: int, v_tok: int, tokens_wanted: int) -> int:
    """Calculate SOL needed to buy exact token amount.

    Returns:
        SOL cost in lamports (before fee). Returns max int if impossible.
    """
    if tokens_wanted >= v_tok:
        return 2**64 - 1  # impossible
    k = v_sol * v_tok
    new_v_tok = v_tok - tokens_wanted
    new_v_sol = k // new_v_tok + 1
    return new_v_sol - v_sol
```

### Fee Handling

The 1% fee is **not** part of the curve math. It's applied externally:

```python
# Buying: fee deducted from SOL input before curve
actual_sol_to_curve = sol_input * 0.99

# Selling: fee deducted from SOL output after curve
actual_sol_received = sol_from_curve * 0.99

# Roundtrip minimum cost: ~2% from fees alone, plus price impact
```

### Market Cap

```python
market_cap_sol = (token_total_supply * virtual_sol_reserves) / virtual_token_reserves
```

## Graduation

Graduation occurs when `realSolReserves` reaches **~85 SOL** (~$12K-14K depending on SOL price). Only ~1.4% of PumpFun tokens ever graduate.

### What Happens

1. `complete` flag set to `true` on bonding curve account
2. `CompleteEvent` emitted (discriminator `5f72619cd42e9808`)
3. Bonding curve stops accepting trades
4. ~$12K liquidity deposited to the destination DEX
5. Token becomes tradeable on PumpSwap (or Raydium for older tokens)

### Fill Percentage

```python
GRADUATION_THRESHOLD = 85_000_000_000  # 85 SOL in lamports

fill_pct = (real_sol_reserves / GRADUATION_THRESHOLD) * 100.0
```

### Migration Targets

- **March 2025+**: PumpSwap (`pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA`) — native AMM, no migration fee
- **Before March 2025**: Raydium V4 (`675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8`) — 6 SOL fee

### PumpSwap Post-Graduation

PumpSwap is a constant-product AMM with 1% fee (same as bonding curve). Key differences:
- Base asset is always WSOL, quote is token
- Instruction semantics are inverted: "buy" instruction sells tokens, "sell" instruction buys tokens
- Supports creator revenue sharing (0.05% of volume to original creator)

## Program IDs & Addresses

| Program/Account | Address |
|-----------------|---------|
| PumpFun Program | `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P` |
| PumpSwap Program | `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA` |
| Fee Program | `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ` |
| Global Account | `4wTV1YmiEkRvAtNtsSGPtUrqRYQMe5SKy2uB4Jjaxnjf` |
| Fee Recipient | `62qc2CNXwrYqQScmEdiZFFAnJR262PxWEuNQtxfafNgV` |
| Event Authority | `Ce6TQqeHC9p8KetsN6JsjHK7UTZk7nasjjnr7XxXp9F1` |

## Event Parsing

Events are Anchor-style: `sha256("event:<EventName>")[0..8]`

| Event | Discriminator (hex) |
|-------|-------------------|
| CreateEvent | `1b72a94ddeeb6376` |
| TradeEvent | `bddb7fd34ee661ee` |
| CompleteEvent | `5f72619cd42e9808` |

### TradeEvent Layout (after 8-byte discriminator)

```
mint:                  pubkey   32 bytes
solAmount:             u64       8 bytes
tokenAmount:           u64       8 bytes
isBuy:                 bool      1 byte
user:                  pubkey   32 bytes
timestamp:             i64       8 bytes
virtualSolReserves:    u64       8 bytes
virtualTokenReserves:  u64       8 bytes
realSolReserves:       u64       8 bytes
realTokenReserves:     u64       8 bytes
```

**Critical**: Events are in CPI inner instructions. Search for discriminators **anywhere** in instruction data, not just at offset 0.

### Bonding Curve Account Layout

```
Offset 0:   discriminator          8 bytes
Offset 8:   virtualTokenReserves   u64
Offset 16:  virtualSolReserves     u64
Offset 24:  realTokenReserves      u64
Offset 32:  realSolReserves        u64
Offset 40:  tokenTotalSupply       u64
Offset 48:  complete               bool (1 byte)
Offset 49:  creator                pubkey (32 bytes)
```

### PDA Derivation

| PDA | Seeds |
|-----|-------|
| Bonding Curve | `["bonding-curve", mint]` |
| Bonding Curve V2 | `["bonding-curve-v2", mint]` |
| Creator Vault | `["creator-vault", creator]` |

## Instruction Discriminators

| Instruction | Hex | Notes |
|-------------|-----|-------|
| buy_exact_sol_in (V2) | `38fc74089edfcd5f` | Current production buy |
| sell (V2) | `33e685a4017f83ad` | Current production sell |
| buy (V1/legacy) | `66063d1201daebea` | Legacy, still seen occasionally |
| create | `181ec828051c0777` | Token creation |

### Buy Instruction Data (24 bytes)

```
[0..8]:   discriminator
[8..16]:  spendable_sol_in    u64 LE (total SOL budget, fees deducted internally)
[16..24]: min_tokens_out      u64 LE (slippage floor)
```

### Sell Instruction Data (24 bytes)

```
[0..8]:   discriminator
[8..16]:  amount_tokens       u64 LE (tokens to sell, raw)
[16..24]: min_sol_output      u64 LE (minimum SOL out, lamports)
```

## Price Impact & Sizing

```python
def price_impact(v_sol: int, v_tok: int, sol_in: int) -> float:
    """Calculate price impact for a buy as a percentage."""
    spot = v_sol / v_tok
    tokens = buy_tokens(v_sol, v_tok, v_tok, sol_in)
    if tokens == 0:
        return float('inf')
    exec_price = sol_in / tokens
    return (exec_price / spot - 1) * 100

# Example: 1 SOL buy at genesis
# impact = price_impact(30_000_000_000, 1_073_000_000_000_000, 1_000_000_000)
# ≈ 3.3% price impact
```

## Files

### References
- `references/bonding_curve_math.md` — Complete mathematical derivations with worked examples
- `references/graduation_process.md` — Graduation threshold, migration, PumpSwap mechanics
- `references/instruction_reference.md` — Full instruction and event layouts for parsing

### Scripts
- `scripts/curve_calculator.py` — Interactive bonding curve calculator: price, impact, fill %
- `scripts/parse_events.py` — Parse PumpFun events from transaction data

### Referencia: references/bonding_curve_math.md

# PumpFun Bonding Curve — Mathematical Reference

## Invariant

PumpFun uses a virtual constant-product market maker (CPMM):

```
k = V_sol × V_tok = constant
```

Where `V_sol` and `V_tok` are **virtual** reserves that include both real (withdrawable) and phantom reserves.

## Initial State

| Variable | Value | Raw |
|----------|-------|-----|
| V_sol (virtual SOL) | 30 SOL | 30,000,000,000 lamports |
| V_tok (virtual tokens) | ~1.073B | 1,073,000,000,000,000 |
| R_tok (real tokens) | ~793M | 793,000,000,000,000 |
| R_sol (real SOL) | 0 | 0 |
| Supply | 1B | 1,000,000,000,000,000 |
| k | — | 3.219 × 10²⁵ |

The virtual-real gap: V_tok - R_tok ≈ 280M tokens are virtual — they shape the curve but cannot be withdrawn.

## Spot Price

At any point on the curve:

```
P = V_sol / V_tok   (in lamports per raw token)

P_human = (V_sol / 10⁹) / (V_tok / 10⁶)   (SOL per token)
```

### Price progression examples

| Fill % | R_sol | V_sol | V_tok | Price (SOL) | Multiplier |
|--------|-------|-------|-------|-------------|------------|
| 0% | 0 | 30B | 1.073T | 2.796e-8 | 1.0x |
| 5% | 3.75B | 33.75B | 953.7B | 3.539e-8 | 1.27x |
| 25% | 21.9B | 51.9B | 620.7B | 8.354e-8 | 2.99x |
| 50% | 45.8B | 75.8B | 424.7B | 1.784e-7 | 6.38x |
| 75% | 63.8B | 93.8B | 343.2B | 2.733e-7 | 9.78x |
| 100% | 85B | 115B | 279.9B | 4.109e-7 | 14.70x |

A token that goes from launch to graduation (100% fill) achieves approximately **14.7x** price appreciation.

## Buy Formula

Given SOL input `Δsol` (after 1% fee is deducted externally):

```
V_sol' = V_sol + Δsol
V_tok' = ⌊k / V_sol'⌋ + 1          (ceiling division match)
tokens_out = V_tok - V_tok'
result = min(tokens_out, R_tok)     (can't buy more than real reserves)
```

The `+1` on V_tok' matches on-chain rounding behavior. Validated against 9K+ live trades.

### Worked Example: Buy 1 SOL at genesis

```
V_sol = 30,000,000,000
V_tok = 1,073,000,000,000,000
k = 30,000,000,000 × 1,073,000,000,000,000 = 3.219e25

sol_in = 1,000,000,000 (1 SOL, before fee; actual to curve = 990,000,000)
V_sol' = 30,990,000,000
V_tok' = 3.219e25 / 30,990,000,000 + 1 = 1,038,722,168,441,433
tokens_out = 1,073,000,000,000,000 - 1,038,722,168,441,433 = 34,277,831,558,567

Result: ~34.28M tokens (34,277,831,558,567 raw / 10^6 = 34,277,831.56)
```

## Sell Formula

Given `Δtok` tokens to sell:

```
V_tok' = V_tok + Δtok
V_sol' = ⌊k / V_tok'⌋
sol_out = V_sol - V_sol' - 1         (floor division match)
result = min(sol_out, R_sol)         (can't withdraw more than real SOL)
```

The `-1` is critical for matching on-chain floor division behavior.

## Buy Cost Formula

Given exact `tokens_wanted`:

```
V_tok' = V_tok - tokens_wanted
V_sol' = ⌊k / V_tok'⌋ + 1
cost = V_sol' - V_sol
```

Returns infinity if `tokens_wanted >= V_tok`.

## Price Impact

```
impact = (execution_price / spot_price - 1) × 100%

Where:
  spot_price = V_sol / V_tok
  execution_price = sol_in / tokens_out
```

### Impact at genesis for various sizes

| Buy Size | Tokens | Impact | % of Supply |
|----------|--------|--------|-------------|
| 0.1 SOL | ~3.5M | 0.33% | 0.35% |
| 1 SOL | ~34.3M | 3.33% | 3.43% |
| 5 SOL | ~152M | 16.7% | 15.2% |
| 10 SOL | ~268M | 33.3% | 26.8% |

Impact grows super-linearly due to the constant-product curve.

## Fee Structure

| Action | Fee | Deducted From |
|--------|-----|---------------|
| Buy | 1% (100 bps) | SOL input (before curve) |
| Sell | 1% (100 bps) | SOL output (after curve) |
| Create | Free | — |

Fee is applied by the on-chain program, NOT by the curve math. Always calculate curve math with pre-fee amounts, then apply fee externally.

### Roundtrip Cost

```
Roundtrip loss = 1 - (1 - 0.01) × (1 - 0.01) × (1 - impact_buy) × (1 - impact_sell)
              ≈ 2% + 2 × avg_impact

For a 1 SOL buy at genesis: ~2% + 2 × 3.3% ≈ 8.6% roundtrip loss
```

## Edge Cases

1. **Zero reserves**: If `R_tok = 0`, no more buys possible (curve depleted)
2. **Zero real SOL**: If `R_sol = 0`, sells return 0 (no SOL to withdraw)
3. **Dust trades**: For amounts < 100K lamports, the `+1/-1` rounding corrections become significant
4. **Completed curve**: After graduation (`complete = true`), all buy/sell calls revert

### Referencia: references/graduation_process.md

# PumpFun Graduation — Process & PumpSwap Migration

## Graduation Threshold

A token graduates when its **realSolReserves** reaches approximately **85 SOL** (85,000,000,000 lamports).

At graduation:
- Virtual SOL ≈ 115 SOL (30 initial + 85 real)
- Virtual Tokens ≈ 279.9M
- Spot price ≈ 4.109 × 10⁻⁷ SOL/token
- Market cap ≈ 115 SOL × supply ratio ≈ $12-14K USD (varies with SOL price)
- Price is approximately **14.7x** the initial launch price

## Graduation Rate

Only approximately **1.4%** of tokens launched on PumpFun ever graduate. The vast majority die before reaching the 85 SOL threshold.

## Graduation Event Sequence

1. A buy transaction pushes `realSolReserves` past the graduation threshold
2. The PumpFun program sets `complete = true` on the bonding curve account
3. A `CompleteEvent` is emitted (discriminator `5f72619cd42e9808`)
4. The bonding curve stops accepting new trades (attempts revert)
5. Liquidity (~$12K worth) is automatically deposited to the destination DEX
6. Token becomes tradeable on the destination DEX

## CompleteEvent Layout

After the 8-byte discriminator:

```
user:           pubkey   32 bytes  (wallet that triggered graduation)
mint:           pubkey   32 bytes  (token mint address)
bondingCurve:   pubkey   32 bytes  (bonding curve account)
timestamp:      i64       8 bytes  (unix seconds)
```

Total: 104 bytes after discriminator.

## Migration Targets

### PumpSwap (March 2025+, current default)

- **Program**: `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA`
- **Type**: Constant-product AMM
- **Fee**: 1% (100 bps), same as bonding curve
- **Migration fee**: None (free)
- **Creator revenue**: 0.05% of PumpSwap trading volume
- **95%+** of current graduations go to PumpSwap

### Raydium V4 (legacy, before March 2025)

- **Program**: `675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8`
- **Type**: Constant-product AMM
- **Fee**: 0.25% (25 bps)
- **Migration fee**: 6 SOL (deducted from reserves)
- **Status**: No longer the default migration target

## PumpSwap Mechanics

### Instruction Semantics Inversion

PumpSwap uses base=WSOL, quote=token. This creates an unintuitive naming:

| Action You Want | PumpSwap Instruction | What It Does |
|-----------------|---------------------|-------------|
| Buy tokens (spend SOL) | `sell` | "Sell" SOL base to receive token quote |
| Sell tokens (receive SOL) | `buy` | "Buy" SOL base by spending token quote |

This is a common source of bugs. The discriminators:
- PumpSwap `buy` (selling tokens): `66063d1201daebea`
- PumpSwap `sell` (buying tokens): `33e685a4017f83ad`

### PumpSwap Pool Layout

```
Offset 0:    discriminator        8 bytes
Offset 8:    bump                 1 byte
Offset 9:    index                2 bytes
Offset 11:   creator              32 bytes (pool creator, NOT token creator)
Offset 43:   base_mint            32 bytes (always WSOL)
Offset 75:   quote_mint           32 bytes (the token)
Offset 107:  lp_mint              32 bytes
Offset 139:  pool_base_account    32 bytes (SOL vault)
Offset 171:  pool_quote_account   32 bytes (token vault)
Offset 203:  lp_supply            8 bytes
Offset 211:  coin_creator         32 bytes (original token creator)
```

### PumpSwap PDAs

| PDA | Seeds | Program |
|-----|-------|---------|
| Global Config | `["global_config"]` | PumpSwap |
| Event Authority | `["__event_authority"]` | PumpSwap |
| Creator Vault Authority | `["creator_vault", coin_creator]` | PumpSwap |
| Fee Config | `["fee_config", pumpswap_program_id]` | Fee Program |

## Tracking Graduation Progress

### Fill Percentage

```python
GRAD_THRESHOLD = 85_000_000_000  # 85 SOL in lamports

def fill_percentage(real_sol_reserves: int) -> float:
    """Calculate how close a token is to graduation."""
    return (real_sol_reserves / GRAD_THRESHOLD) * 100.0
```

### Fill Velocity

Track the rate of SOL accumulation to predict graduation timing:

```python
def estimated_time_to_graduation(
    current_sol: int,
    previous_sol: int,
    time_delta_seconds: float,
) -> float | None:
    """Estimate seconds until graduation based on current velocity."""
    remaining = GRAD_THRESHOLD - current_sol
    if remaining <= 0:
        return 0
    velocity = (current_sol - previous_sol) / time_delta_seconds  # lamports/sec
    if velocity <= 0:
        return None  # not progressing
    return remaining / velocity
```

### Monitoring via gRPC

Subscribe to the PumpFun program via Yellowstone gRPC to receive:
- **TradeEvents**: Every buy/sell with updated reserves
- **CompleteEvents**: Graduation trigger

Filter by program ID `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P` in your subscription.

## Fee Comparison Post-Graduation

| DEX | Fee | Notes |
|-----|-----|-------|
| PumpFun bonding curve | 1.00% | Before graduation |
| PumpSwap | 1.00% | After graduation (PumpSwap) |
| Raydium V4 | 0.25% | After graduation (legacy) |
| Raydium CPMM | 0.25% | — |
| Orca Whirlpool | 0.30% | — |
| Meteora DLMM | 0.30% | — |

Note: PumpSwap's 1% fee is higher than other Solana DEXes. This is relevant for cost modeling.

### Referencia: references/instruction_reference.md

# PumpFun — Instruction & Event Reference

## Program IDs

| Program | Address | Purpose |
|---------|---------|---------|
| PumpFun | `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P` | Bonding curve trades |
| PumpSwap | `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA` | Post-graduation AMM |
| Fee Program | `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ` | Fee handling |
| Metaplex Metadata | `metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s` | Token metadata |

## Well-Known Accounts

| Account | Address |
|---------|---------|
| Global | `4wTV1YmiEkRvAtNtsSGPtUrqRYQMe5SKy2uB4Jjaxnjf` |
| Fee Recipient | `62qc2CNXwrYqQScmEdiZFFAnJR262PxWEuNQtxfafNgV` |
| Event Authority | `Ce6TQqeHC9p8KetsN6JsjHK7UTZk7nasjjnr7XxXp9F1` |

---

## Instruction Discriminators

Discriminators are the first 8 bytes of instruction data.

### PumpFun Instructions

| Instruction | Hex | Use |
|-------------|-----|-----|
| buy_exact_sol_in (V2) | `38fc74089edfcd5f` | Current buy |
| sell (V2) | `33e685a4017f83ad` | Current sell |
| buy (V1/legacy) | `66063d1201daebea` | Legacy buy |
| create | `181ec828051c0777` | Token creation |
| initialize | `afaf6d1f0d989bed` | Global state init |
| setParams | `a51f8635bdb482ff` | Admin config |

### Buy V2 — Instruction Data (24 bytes)

```
Bytes 0-7:   discriminator         0x38fc74089edfcd5f
Bytes 8-15:  spendable_sol_in      u64 LE (total SOL budget)
Bytes 16-23: min_tokens_out        u64 LE (slippage floor)
```

Note: `spendable_sol_in` is the TOTAL SOL budget. The 1% fee is deducted internally by the program before applying to the curve.

### Sell V2 — Instruction Data (24 bytes)

```
Bytes 0-7:   discriminator         0x33e685a4017f83ad
Bytes 8-15:  amount_tokens         u64 LE (tokens to sell, raw units)
Bytes 16-23: min_sol_output        u64 LE (minimum SOL received)
```

### Buy V2 — Account Layout (17 accounts)

```
 0: global                        (readonly)
 1: feeRecipient                  (writable)
 2: mint                          (readonly)
 3: bondingCurve                  (writable)
 4: associatedBondingCurve        (writable)   ATA(bondingCurve, mint)
 5: associatedUser                (writable)   ATA(user, mint)
 6: user                          (signer)
 7: systemProgram                 (readonly)
 8: tokenProgram                  (readonly)
 9: creatorVault                  (writable)   PDA: ["creator-vault", creator]
10: eventAuthority                (readonly)
11: program                       (readonly)
12: globalVolumeAccumulator       (readonly)
13: userVolumeAccumulator         (writable)   PDA: ["user_volume_accumulator", user]
14: feeConfig                     (readonly)   PDA: ["fee_config", pumpfun_program]
15: feeProgram                    (readonly)
16: bondingCurveV2                (readonly)   PDA: ["bonding-curve-v2", mint]
```

### Sell V2 — Account Layout (15 accounts)

```
 0: global                        (readonly)
 1: feeRecipient                  (writable)
 2: mint                          (readonly)
 3: bondingCurve                  (writable)
 4: associatedBondingCurve        (writable)
 5: associatedUser                (writable)
 6: user                          (signer)
 7: systemProgram                 (readonly)
 8: creatorVault                  (writable)
 9: tokenProgram                  (readonly)
10: eventAuthority                (readonly)
11: program                       (readonly)
12: feeConfig                     (readonly)
13: feeProgram                    (readonly)
14: bondingCurveV2                (readonly)   (remaining account)
```

**Note**: Sell has 15 accounts vs buy's 17. Sell does NOT include volume accumulators. Account ordering differs — `creatorVault` and `tokenProgram` swap positions between buy (8=tokenProgram, 9=creatorVault) and sell (8=creatorVault, 9=tokenProgram).

---

## Event Discriminators

Events use Anchor's convention: `sha256("event:<EventName>")[0..8]`

| Event | Hex Discriminator |
|-------|------------------|
| CreateEvent | `1b72a94ddeeb6376` |
| TradeEvent | `bddb7fd34ee661ee` |
| CompleteEvent | `5f72619cd42e9808` |

### CreateEvent Layout (after discriminator)

```
name:           string    (4-byte LE length prefix + UTF-8 data)
symbol:         string    (4-byte LE length prefix + UTF-8 data)
uri:            string    (4-byte LE length prefix + UTF-8 data)
mint:           pubkey    32 bytes
bondingCurve:   pubkey    32 bytes
user:           pubkey    32 bytes (the creator)
```

### TradeEvent Layout (after discriminator)

```
mint:                   pubkey    32 bytes
solAmount:              u64        8 bytes LE
tokenAmount:            u64        8 bytes LE
isBuy:                  bool       1 byte (1=buy, 0=sell)
user:                   pubkey    32 bytes
timestamp:              i64        8 bytes LE (unix seconds)
virtualSolReserves:     u64        8 bytes LE
virtualTokenReserves:   u64        8 bytes LE
realSolReserves:        u64        8 bytes LE
realTokenReserves:      u64        8 bytes LE
```

Total: 121 bytes. Every field is fixed-size — no variable-length data.

### CompleteEvent Layout (after discriminator)

```
user:           pubkey    32 bytes
mint:           pubkey    32 bytes
bondingCurve:   pubkey    32 bytes
timestamp:      i64        8 bytes LE
```

Total: 104 bytes.

---

## Parsing Pattern

Events are emitted via CPI (Cross-Program Invocation), so they appear in **inner instructions**, not top-level instructions. The discriminator may not be at byte offset 0.

```python
def find_event(data: bytes, discriminator: bytes) -> int:
    """Find event discriminator anywhere in instruction data.

    Args:
        data: Raw instruction data bytes.
        discriminator: 8-byte event discriminator.

    Returns:
        Byte offset of the event data (after discriminator), or -1 if not found.
    """
    idx = data.find(discriminator)
    if idx == -1:
        return -1
    return idx + 8  # skip discriminator, return start of event data
```

---

## Bonding Curve Account Layout

Account data for the bonding curve PDA (`["bonding-curve", mint]`):

```
Offset 0:    discriminator          u64    8 bytes
Offset 8:    virtualTokenReserves   u64    8 bytes
Offset 16:   virtualSolReserves     u64    8 bytes
Offset 24:   realTokenReserves      u64    8 bytes
Offset 32:   realSolReserves        u64    8 bytes
Offset 40:   tokenTotalSupply       u64    8 bytes
Offset 48:   complete               bool   1 byte
Offset 49:   creator                pubkey 32 bytes
```

Total minimum: 81 bytes.

```python
import struct

def parse_bonding_curve(data: bytes) -> dict:
    """Parse bonding curve account data."""
    if len(data) < 81:
        return {}
    return {
        "virtualTokenReserves": struct.unpack_from("<Q", data, 8)[0],
        "virtualSolReserves":   struct.unpack_from("<Q", data, 16)[0],
        "realTokenReserves":    struct.unpack_from("<Q", data, 24)[0],
        "realSolReserves":      struct.unpack_from("<Q", data, 32)[0],
        "tokenTotalSupply":     struct.unpack_from("<Q", data, 40)[0],
        "complete":             bool(data[48]),
        "creator":              data[49:81],  # 32-byte pubkey
    }
```

---

## PDA Seeds

| PDA | Seeds | Program |
|-----|-------|---------|
| Bonding Curve | `["bonding-curve", mint_pubkey]` | PumpFun |
| Bonding Curve V2 | `["bonding-curve-v2", mint_pubkey]` | PumpFun |
| Mint Authority | `["mint-authority"]` | PumpFun |
| Global | `["global"]` | PumpFun |
| Creator Vault | `["creator-vault", creator_pubkey]` | PumpFun |
| Global Volume Acc | `["global_volume_accumulator"]` | PumpFun |
| User Volume Acc | `["user_volume_accumulator", user_pubkey]` | PumpFun |
| Fee Config | `["fee_config", pumpfun_program_id]` | Fee Program |


---

## SKILL: regime-detection

- Fuente: `agiprolabs/claude-trading-skills` → `skills/regime-detection` (MIT)
- Cuándo usarla: Market regime identification using volatility clustering, trend detection, and statistical methods for adaptive trading
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/regime-detection/` (detect_regime.py, regime_backtest.py)

# Regime Detection

Identify the current market regime so you can pick the right strategy, size positions correctly, and avoid deploying trend-following logic in a ranging market (or vice versa).

## Why Regime Detection Matters

Every strategy has a "home regime." A momentum strategy prints money in a clean uptrend but bleeds in a choppy range. A mean-reversion grid thrives in low-volatility consolidation but gets steamrolled by a trending breakout. Regime detection tells you **which playbook to use right now**.

Key benefits:
- **Strategy selection**: Route signals to the right strategy for the current environment
- **Position sizing**: Reduce exposure in hostile regimes, increase in favorable ones
- **Stop adaptation**: Wider stops in high-vol regimes, tighter in low-vol trends
- **Drawdown control**: Sit out "danger zone" regimes (high vol + no trend)

## Core Regime Dimensions

Two orthogonal axes define the four-quadrant regime model:

| | Low Volatility | High Volatility |
|---|---|---|
| **Trending** | Q1: Clean trend — best for trend following | Q2: Volatile trend — momentum with caution |
| **Ranging** | Q3: Quiet range — mean-reversion paradise | Q4: Choppy chaos — reduce or sit out |

A third dimension — **mean-reversion tendency** (Hurst exponent) — refines Q3 by telling you how reliably price reverts.

## Simple Approaches (No ML Required)

### 1. ATR Volatility Percentile

Rank the current ATR against its own recent history to get a 0–100 percentile score.

```python
import pandas as pd
import numpy as np

def atr_percentile(
    high: pd.Series, low: pd.Series, close: pd.Series,
    atr_period: int = 14, lookback: int = 100
) -> pd.Series:
    """ATR percentile rank over a rolling window."""
    tr = pd.concat([
        high - low,
        (high - close.shift(1)).abs(),
        (low - close.shift(1)).abs()
    ], axis=1).max(axis=1)
    atr = tr.rolling(atr_period).mean()
    return atr.rolling(lookback).apply(
        lambda x: pd.Series(x).rank(pct=True).iloc[-1], raw=False
    )
```

- **< 25th percentile** → Low volatility regime
- **25th–75th** → Normal volatility
- **> 75th percentile** → High volatility regime

### 2. ADX Trend Strength

ADX above 25 signals a trending market; below 20 signals a range.

```python
def compute_adx(
    high: pd.Series, low: pd.Series, close: pd.Series,
    period: int = 14
) -> pd.Series:
    """Average Directional Index."""
    plus_dm = high.diff().clip(lower=0)
    minus_dm = (-low.diff()).clip(lower=0)
    # Zero out when the other is larger
    plus_dm[plus_dm < minus_dm] = 0
    minus_dm[minus_dm < plus_dm] = 0

    tr = pd.concat([
        high - low,
        (high - close.shift(1)).abs(),
        (low - close.shift(1)).abs()
    ], axis=1).max(axis=1)

    atr = tr.ewm(span=period, adjust=False).mean()
    plus_di = 100 * plus_dm.ewm(span=period, adjust=False).mean() / atr
    minus_di = 100 * minus_dm.ewm(span=period, adjust=False).mean() / atr
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di)
    return dx.ewm(span=period, adjust=False).mean()
```

### 3. EMA Slope + Price Position

```python
def trend_direction(close: pd.Series, period: int = 20) -> pd.Series:
    """Returns +1 (uptrend), -1 (downtrend), 0 (neutral)."""
    ema = close.ewm(span=period, adjust=False).mean()
    slope = ema.diff(5)  # 5-bar slope
    above = (close > ema).astype(int)
    direction = pd.Series(0, index=close.index)
    direction[(slope > 0) & (above == 1)] = 1
    direction[(slope < 0) & (above == 0)] = -1
    return direction
```

### 4. Bollinger Band Width Percentile

BB width (upper - lower) / middle as a volatility proxy. A "squeeze" (low percentile) often precedes a breakout.

```python
def bb_width_percentile(
    close: pd.Series, period: int = 20,
    std_dev: float = 2.0, lookback: int = 100
) -> pd.Series:
    """Bollinger Band width percentile."""
    sma = close.rolling(period).mean()
    std = close.rolling(period).std()
    width = (2 * std_dev * std) / sma
    return width.rolling(lookback).apply(
        lambda x: pd.Series(x).rank(pct=True).iloc[-1], raw=False
    )
```

## Statistical Approaches

### Rolling Hurst Exponent

The Hurst exponent H classifies time series behavior:
- **H < 0.4** → Mean-reverting (anti-persistent)
- **0.4 ≤ H ≤ 0.6** → Random walk (no exploitable structure)
- **H > 0.6** → Trending (persistent)

Computed via the Rescaled Range (R/S) method. See `references/methodology.md` for the full derivation.

```python
def hurst_exponent(series: pd.Series, max_lag: int = 50) -> float:
    """Estimate Hurst exponent using R/S method."""
    lags = range(2, max_lag)
    rs_values = []
    for lag in lags:
        chunks = [series.iloc[i:i+lag] for i in range(0, len(series) - lag, lag)]
        rs_list = []
        for chunk in chunks:
            if len(chunk) < lag:
                continue
            mean_val = chunk.mean()
            devs = chunk - mean_val
            cumdev = devs.cumsum()
            r = cumdev.max() - cumdev.min()
            s = chunk.std(ddof=1)
            if s > 0:
                rs_list.append(r / s)
        if rs_list:
            rs_values.append(np.mean(rs_list))
        else:
            rs_values.append(np.nan)
    valid = [(l, r) for l, r in zip(lags, rs_values) if not np.isnan(r)]
    if len(valid) < 5:
        return 0.5
    log_lags = np.log([v[0] for v in valid])
    log_rs = np.log([v[1] for v in valid])
    coeffs = np.polyfit(log_lags, log_rs, 1)
    return coeffs[0]
```

### Change-Point Detection (CUSUM)

Detects abrupt shifts in mean or variance of a return series.

```python
def cusum_test(
    returns: pd.Series, threshold: float = 2.0
) -> list[int]:
    """CUSUM change-point detection on returns.

    Returns indices where regime changes are detected.
    """
    mean_r = returns.mean()
    std_r = returns.std()
    if std_r == 0:
        return []
    s_pos, s_neg = 0.0, 0.0
    changes = []
    for i, r in enumerate(returns):
        z = (r - mean_r) / std_r
        s_pos = max(0, s_pos + z - 0.5)
        s_neg = max(0, s_neg - z - 0.5)
        if s_pos > threshold or s_neg > threshold:
            changes.append(i)
            s_pos, s_neg = 0.0, 0.0
    return changes
```

### Hidden Markov Models

For 2–3 state regime models using `hmmlearn`. This is optional — all core functionality works with numpy/pandas only.

```python
# Optional: requires `uv pip install hmmlearn`
from hmmlearn import hmm

def fit_hmm_regimes(
    returns: np.ndarray, n_states: int = 2, n_iter: int = 100
) -> tuple[np.ndarray, object]:
    """Fit a Gaussian HMM to return series."""
    X = returns.reshape(-1, 1)
    model = hmm.GaussianHMM(
        n_components=n_states, covariance_type="full", n_iter=n_iter
    )
    model.fit(X)
    states = model.predict(X)
    return states, model
```

See `references/methodology.md` for details on feature selection and state interpretation.

## Crypto-Specific Considerations

### Regime Speed

Crypto regimes change **much faster** than equities:

| Parameter | Equities | Crypto (large cap) | Crypto (micro cap / PumpFun) |
|---|---|---|---|
| ATR lookback | 100–200 bars | 50–100 bars | 20–50 bars |
| ADX period | 14–28 | 10–14 | 7–10 |
| Regime persistence | Weeks–months | Days–weeks | Hours–days |
| Hurst window | 200+ bars | 100 bars | 50 bars |

### Volume as a Regime Signal

In crypto, volume confirms regime quality:
- **High volume + trend** → Strong conviction, ride it
- **Low volume + trend** → Drift, unreliable, reduce size
- **High volume + range** → Distribution or accumulation, watch for breakout
- **Low volume + range** → Dead market, skip

### PumpFun Micro-Regimes

New token launches follow a stereotyped sequence:
1. **Launch pump** (minutes): Vertical move, extreme vol, no mean-reversion
2. **First dump** (minutes–hours): Profit-taking, high vol, trending down
3. **Consolidation** (hours–days): Low vol range, potential mean-reversion
4. **Second wave or death**: Either breaks out again (new trend) or fades to zero

Each micro-regime lasts minutes to hours. Use 1-minute bars with 20–50 bar windows.

## Combined Regime Classification

```python
def classify_regime(
    vol_percentile: float, adx: float, hurst: float,
    trend_dir: int
) -> dict[str, str]:
    """Classify into the 4-quadrant model."""
    vol_regime = (
        "low" if vol_percentile < 0.30
        else "high" if vol_percentile > 0.70
        else "normal"
    )
    trend_regime = (
        "trending" if adx > 25
        else "ranging" if adx < 20
        else "transitional"
    )
    direction = (
        "up" if trend_dir > 0
        else "down" if trend_dir < 0
        else "neutral"
    )
    mr_regime = (
        "mean_reverting" if hurst < 0.4
        else "trending" if hurst > 0.6
        else "random"
    )
    return {
        "volatility": vol_regime,
        "trend": trend_regime,
        "direction": direction,
        "mean_reversion": mr_regime,
        "quadrant": f"{vol_regime}_vol_{trend_regime}",
    }
```

## Strategy Adaptation

See `references/strategy_adaptation.md` for the full regime-strategy matrix.

Quick reference:

| Current Regime | Action |
|---|---|
| Low vol + trending up | Full size trend-following, tight stops |
| High vol + trending | Half size momentum, wide stops |
| Low vol + ranging | Mean-reversion / grid strategies |
| High vol + ranging | Reduce to 25% size or sit out |
| Regime transition | Flatten or reduce to minimum size |

## Integration with Other Skills

- **`pandas-ta`**: Compute ATR, ADX, Bollinger Bands, EMAs
- **`volatility-modeling`**: Advanced vol forecasting (GARCH, realized vol)
- **`strategy-framework`**: Route signals through regime filter before execution
- **`position-sizing`**: Scale position size by regime volatility
- **`risk-management`**: Adjust portfolio risk limits per regime

## Files

### References
- `references/methodology.md` — Detailed math for Hurst exponent, HMM, change-point detection, and volatility estimation methods
- `references/strategy_adaptation.md` — Full regime-strategy matrix with position sizing, stop adaptation, and PumpFun micro-regime playbook

### Scripts
- `scripts/detect_regime.py` — Compute regime indicators on live or demo data, classify into 4-quadrant model
- `scripts/regime_backtest.py` — Compare regime-adaptive vs static strategy on synthetic data with clear regime transitions

### Referencia: references/methodology.md

# Regime Detection — Methodology Reference

Detailed mathematical methods for identifying market regimes.

## Volatility Regime Detection

### Rolling Standard Deviation of Returns

The simplest volatility estimator. Compute log returns, then rolling standard deviation:

```
r_t = ln(close_t / close_{t-1})
σ_rolling = std(r_{t-N+1}, ..., r_t)
```

- **Window**: 20 bars for crypto, 50–100 for equities
- **Percentile rank**: Rank current σ against the last 100 values → 0–100 score
- **Annualization**: Multiply by √(bars_per_year) if needed, but percentile rank doesn't require it

### ATR Normalization

Raw ATR depends on price level. Normalize for cross-asset comparison:

```
NATR = (ATR / close) × 100
```

NATR of 5% means average true range is 5% of price. Useful for comparing BTC (NATR ~3%) vs a micro-cap (NATR ~15%).

### Parkinson Volatility

Uses high-low range instead of close-to-close. More efficient estimator:

```
σ_park = sqrt( (1 / (4N ln2)) × Σ (ln(H_i / L_i))² )
```

Advantages:
- Uses intrabar information (high/low)
- ~5x more efficient than close-to-close estimator
- Less affected by overnight gaps (less relevant for 24/7 crypto)

Disadvantage:
- Does not capture gap risk (opening jumps)

### Garman-Klass Volatility

Extends Parkinson by incorporating open and close:

```
σ_gk = sqrt( (1/N) × Σ [ 0.5 × (ln(H/L))² - (2ln2 - 1) × (ln(C/O))² ] )
```

Most efficient estimator using OHLC data. Recommended for crypto where you have reliable OHLC.

## Trend Detection

### ADX Calculation

The Average Directional Index measures trend strength regardless of direction.

**Step 1**: Directional Movement
```
+DM = max(high_t - high_{t-1}, 0)  if > |low_{t-1} - low_t|, else 0
-DM = max(low_{t-1} - low_t, 0)    if > (high_t - high_{t-1}), else 0
```

**Step 2**: Directional Indicators (smoothed over N periods)
```
+DI = 100 × smooth(+DM, N) / smooth(TR, N)
-DI = 100 × smooth(-DM, N) / smooth(TR, N)
```

**Step 3**: ADX
```
DX = 100 × |+DI - -DI| / (+DI + -DI)
ADX = smooth(DX, N)
```

Interpretation:
- **ADX < 20**: No trend (ranging)
- **20–25**: Weak trend or emerging trend
- **25–40**: Strong trend
- **> 40**: Very strong trend (often near exhaustion in crypto)

ADX does not indicate direction — only strength. Use +DI vs -DI or price vs EMA for direction.

### Linear Regression Slope + R²

Fit a linear regression to the last N closing prices:

```
slope = Σ((i - ī)(p_i - p̄)) / Σ((i - ī)²)
R² = 1 - Σ(p_i - ŷ_i)² / Σ(p_i - p̄)²
```

- **slope > 0 + R² > 0.6**: Clean uptrend
- **slope < 0 + R² > 0.6**: Clean downtrend
- **R² < 0.3**: No linear trend (ranging or chaotic)

R² is the key signal — high R² means price is "well-behaved" along the regression line, ideal for trend-following.

### EMA Spread as Trend Strength

```
trend_strength = (EMA_fast - EMA_slow) / ATR
```

Normalizing by ATR makes the spread comparable across assets and timeframes. Values > 1.5 indicate strong trend, < 0.5 indicates weak/no trend.

## Hurst Exponent

### Rescaled Range (R/S) Method

The Hurst exponent H characterizes time series persistence.

**Algorithm**:
1. For each lag τ from 2 to max_lag:
   a. Divide series into chunks of length τ
   b. For each chunk:
      - Compute mean m
      - Compute cumulative deviations: Y_t = Σ(x_i - m) for i=1..t
      - R = max(Y) - min(Y) (range of cumulative deviations)
      - S = std(chunk) (standard deviation)
      - RS = R / S
   c. Average RS across all chunks for this lag
2. Plot log(RS) vs log(τ)
3. H = slope of the best-fit line

**Interpretation**:
- **H < 0.4**: Anti-persistent (mean-reverting). Past up-moves predict future down-moves.
- **0.4 ≤ H ≤ 0.6**: No significant memory. Approximately random walk.
- **H > 0.6**: Persistent (trending). Past up-moves predict future up-moves.

**Practical notes**:
- Need at least 100 data points for reliable estimation
- Rolling Hurst: compute H over a sliding window of 100 bars, step by 1
- Crypto assets frequently oscillate between H=0.3 and H=0.7 over days
- Hurst near 0.5 is uninformative — don't trade on it

### Detrended Fluctuation Analysis (DFA)

An alternative to R/S that handles non-stationary trends better:

1. Compute cumulative sum of mean-centered returns
2. Divide into windows of size n
3. Fit a polynomial trend to each window
4. Compute RMS of residuals F(n)
5. H = slope of log(F(n)) vs log(n)

DFA is more robust than R/S for short series but computationally heavier.

## Change-Point Detection

### CUSUM (Cumulative Sum)

Detects shifts in the mean of a standardized series.

**Algorithm**:
```
S⁺_0 = S⁻_0 = 0
S⁺_t = max(0, S⁺_{t-1} + z_t - k)
S⁻_t = max(0, S⁻_{t-1} - z_t - k)
```

Where z_t = (r_t - μ) / σ and k = 0.5 (slack parameter).

A change point is detected when S⁺ or S⁻ exceeds threshold h (typically 2–5). Higher h = fewer false alarms but slower detection.

**Tuning for crypto**:
- k = 0.5, h = 2.0 for fast detection (more false positives)
- k = 0.5, h = 4.0 for conservative detection
- Recompute μ and σ using the last 50–100 bars, not the full history

### Pettitt Test

Non-parametric test for a single change point in the series. Tests whether the distribution before and after a candidate point differs significantly.

Good for confirming CUSUM-detected change points with a p-value.

## Hidden Markov Models

### Model Setup

A Gaussian HMM with N states models regime-switching:
- **States**: Unobserved regimes (e.g., bull, bear, neutral)
- **Observations**: Return features (returns, volatility, volume change)
- **Transition matrix**: Probability of switching between states
- **Emission**: Each state has a Gaussian distribution over observations

### Feature Selection

Recommended feature vector for crypto:
1. Log returns (captures direction + magnitude)
2. Rolling volatility (captures vol regime)
3. Volume ratio: volume / rolling_mean_volume (captures participation)

### Practical Limitations

- **Labels are arbitrary**: HMM assigns state 0, 1, 2 — you must interpret them by examining each state's mean return and volatility
- **Non-stationary**: Retrain periodically (every 200–500 bars)
- **Sensitive to initialization**: Run multiple times, pick best log-likelihood
- **Overfitting with >3 states**: Stick to 2–3 states for crypto
- **Look-ahead risk**: Use only past data for training when backtesting

### State Interpretation

After fitting, examine each state:
```python
for i in range(n_states):
    mask = (states == i)
    print(f"State {i}: mean_return={returns[mask].mean():.4f}, "
          f"vol={returns[mask].std():.4f}, "
          f"pct_time={mask.mean():.1%}")
```

Label states by their characteristics:
- Highest mean return + moderate vol → "Bull"
- Lowest mean return + high vol → "Bear"
- Near-zero return + low vol → "Neutral/Range"

### Referencia: references/strategy_adaptation.md

# Regime Detection — Strategy Adaptation Reference

How to adapt trading strategies, position sizing, and risk parameters based on the detected market regime.

## Regime-Strategy Matrix

| Regime | Best Strategies | Worst Strategies | Notes |
|---|---|---|---|
| **Low vol + trend up** | Trend following, breakout, momentum | Mean reversion, short selling | Cleanest edge. Full position size. Tight trailing stops. |
| **Low vol + trend down** | Trend following (short), hedging | Buying dips, grid trading | Less common in crypto. Often precedes capitulation. |
| **High vol + trend up** | Momentum with wide stops, scale-in | Tight stop trend following | Stops get hunted. Use half size, 2x normal stop width. |
| **High vol + trend down** | Short momentum, hedging, cash | Buying dips, mean reversion | Most dangerous. Drawdowns accelerate. Preserve capital. |
| **Low vol + range** | Mean reversion, grid, market making | Trend following, breakout | Bollinger band bounce, RSI mean reversion. High win rate. |
| **High vol + range** | Volatility strategies, wide grids | Tight stops, trend following | Danger zone. Whipsaws destroy both trend and MR strategies. |
| **Transitional** | Reduce size, wait for clarity | Any full-size strategy | Regime shifts cause the biggest losses. Wait for confirmation. |

## Position Sizing by Regime

### Volatility-Adjusted Sizing

Base position size on the inverse of current volatility:

```python
def regime_adjusted_size(
    base_size: float,
    vol_percentile: float,
    adx: float
) -> float:
    """Adjust position size based on regime.

    Args:
        base_size: Normal position size (e.g., 1.0 = 100%).
        vol_percentile: Current ATR percentile (0-1).
        adx: Current ADX value.

    Returns:
        Adjusted position size.
    """
    # Volatility adjustment: scale inversely with vol
    if vol_percentile > 0.80:
        vol_mult = 0.25  # Very high vol: quarter size
    elif vol_percentile > 0.60:
        vol_mult = 0.50  # High vol: half size
    elif vol_percentile < 0.20:
        vol_mult = 1.25  # Very low vol: can go slightly over
    else:
        vol_mult = 1.0   # Normal vol: full size

    # Trend clarity adjustment
    if adx > 30:
        trend_mult = 1.25  # Strong trend: increase size
    elif adx < 15:
        trend_mult = 0.50  # No trend: reduce size
    else:
        trend_mult = 1.0

    return base_size * vol_mult * trend_mult
```

### Sizing Rules of Thumb

| Regime | Size Multiplier | Rationale |
|---|---|---|
| Low vol + strong trend | 1.25–1.50x | Best risk/reward, exploit it |
| Normal vol + trend | 1.0x | Standard sizing |
| High vol + trend | 0.50x | Same direction conviction, more noise |
| Low vol + range | 0.75x | Lower expected return per trade |
| High vol + range | 0.25x | Danger zone, minimal exposure |
| Any transition | 0.25–0.50x | Wait for regime to establish |

## Stop Loss Adaptation

### ATR-Based Stop Scaling

```python
def regime_stop_distance(
    atr: float,
    vol_percentile: float,
    regime: str
) -> float:
    """Compute stop distance adapted to current regime.

    Returns distance in price units.
    """
    if regime == "trending":
        # Wider stops to avoid getting shaken out
        if vol_percentile > 0.70:
            return atr * 3.0  # High vol trend: 3x ATR
        else:
            return atr * 2.0  # Low vol trend: 2x ATR
    else:
        # Range: tighter stops, expect mean reversion
        if vol_percentile > 0.70:
            return atr * 2.5  # High vol range: wide but capped
        else:
            return atr * 1.5  # Low vol range: tight
```

### Stop Adaptation Summary

| Regime | Stop Width (ATR multiples) | Stop Type |
|---|---|---|
| Low vol trend | 2.0x ATR | Trailing stop |
| High vol trend | 3.0x ATR | Trailing stop, wider |
| Low vol range | 1.5x ATR | Fixed stop at range edge |
| High vol range | 2.5x ATR | Fixed stop, or time-based exit |

## Indicator Parameter Adaptation

Adjust indicator lookback periods based on regime speed:

| Parameter | Low Vol / Slow | High Vol / Fast |
|---|---|---|
| EMA fast period | 20 | 8–12 |
| EMA slow period | 50 | 20–30 |
| RSI period | 14 | 7–10 |
| ADX period | 14 | 7–10 |
| ATR period | 14 | 7–10 |
| Bollinger period | 20 | 10–14 |
| Hurst window | 100–200 | 50–100 |

Rationale: High-volatility regimes have faster information incorporation. Longer-period indicators lag too much and generate late signals.

## Regime Transition Signals

Early warning that a regime is about to change:

### Volatility Regime Transitions

- **Low → High vol**: Bollinger Band width expanding rapidly (BB width crosses above 75th percentile from below). ATR increasing 2+ consecutive bars.
- **High → Low vol**: BB squeeze forming. ATR decreasing. Volume declining.

### Trend Regime Transitions

- **Range → Trend**: ADX crossing above 20 from below. Price breaking out of Bollinger Bands. Volume spike (>2x average).
- **Trend → Range**: ADX declining from above 30. DI+ and DI- converging. Hurst dropping toward 0.5.

### Transition Playbook

1. **Detect potential transition** (2+ signals aligning)
2. **Reduce position size to 50%** until new regime confirms
3. **Wait 3–5 bars** for regime to establish (avoid whipsaws)
4. **Switch strategy** only after regime persists for 5+ bars
5. **Never fully switch** on a single bar signal

## PumpFun Micro-Regime Playbook

For new token launches on Solana, regimes compress into minutes/hours.

### Phase Detection

```python
def detect_pump_phase(
    close: pd.Series, volume: pd.Series,
    bars_since_launch: int
) -> str:
    """Identify current micro-regime phase for a new token."""
    recent_return = (close.iloc[-1] / close.iloc[-10] - 1) if len(close) > 10 else 0
    vol_ratio = volume.iloc[-5:].mean() / volume.mean() if len(volume) > 20 else 1

    if bars_since_launch < 20:
        if recent_return > 0.5:  # Up 50%+ in first bars
            return "launch_pump"
        return "launch_uncertain"
    elif bars_since_launch < 60:
        if recent_return < -0.3 and vol_ratio > 1.5:
            return "first_dump"
        elif abs(recent_return) < 0.1 and vol_ratio < 0.5:
            return "consolidation"
        else:
            return "volatile_transition"
    else:
        if recent_return > 0.3 and vol_ratio > 1.0:
            return "second_wave"
        elif recent_return < -0.2:
            return "fading"
        else:
            return "consolidation"
```

### Micro-Regime Actions

| Phase | Action | Position Size | Stop |
|---|---|---|---|
| Launch pump | Don't chase | 0% | — |
| First dump | Watch, don't catch knife | 0% | — |
| Consolidation | Assess holders, volume | Scout (10%) | Below range low |
| Second wave | Enter if volume confirms | 25–50% | Below consolidation low |
| Fading | Avoid | 0% | — |

## Risk Regime Override

Regardless of regime classification, apply these hard overrides:

1. **Drawdown override**: If portfolio down > 5% today, reduce all sizes to 25% regardless of regime
2. **Correlation spike**: If BTC drops > 5% in 1 hour, all altcoin regimes reset to "danger" — everything correlates in crashes
3. **Volume death**: If volume drops below 20th percentile of its own history, treat any trend signal as unreliable
4. **Spread blowout**: If bid-ask spread exceeds 2%, the regime is "illiquid" — reduce size and widen stops regardless


---

## SKILL: scenario-analyzer

- Fuente: `tradermonty/claude-trading-skills` → `skills/scenario-analyzer` (MIT)
- Cuándo usarla: |

# Scenario Analyzer

## Overview

This skill analyzes medium-to-long-term (18-month) investment scenarios
starting from a news headline. It invokes two specialized agents in sequence
(`scenario-analyst` and `strategy-reviewer`) and integrates multi-angle
analysis with a critical review into a comprehensive report.

## When to Use This Skill

Use this skill when:

- You want to analyze the medium-to-long-term investment impact of a news headline
- You want to construct multiple 18-month scenarios
- You want sector/stock impacts organized into 1st/2nd/3rd-order effects
- You need a comprehensive analysis that includes a second opinion

**Examples:**
```
/scenario-analyzer "Fed raises interest rates by 50bp, signals more hikes ahead"
/scenario-analyzer "China announces new tariffs on US semiconductors"
/scenario-analyzer "OPEC+ agrees to cut oil production by 2 million barrels per day"
```

## Prerequisites

- **API Keys**: None (uses only WebSearch/WebFetch)
- **MCP Servers**: None
- **Dependencies**: The scenario-analyst and strategy-reviewer agents must be available via the Task tool

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Skill (orchestrator)                              │
│                                                                      │
│  Phase 1: Preparation                                                │
│  ├─ Headline parsing                                                 │
│  ├─ Event type classification                                        │
│  └─ Reference loading                                                │
│                                                                      │
│  Phase 2: Agent invocation                                           │
│  ├─ scenario-analyst (primary analysis)                              │
│  └─ strategy-reviewer (second opinion)                               │
│                                                                      │
│  Phase 3: Integration & report generation                            │
│  └─ reports/scenario_analysis_<topic>_YYYYMMDD.md                   │
└─────────────────────────────────────────────────────────────────────┘
```

## Workflow

### Phase 1: Preparation

#### Step 1.1: Headline Parsing

Parse the headline provided by the user.

1. **Headline check**
   - Confirm a headline was passed as an argument
   - If not provided, ask the user for input

2. **Keyword extraction**
   - Key entities (company names, country names, institution names)
   - Numeric data (rates, prices, quantities)
   - Actions (raise, cut, announce, agree, etc.)

#### Step 1.2: Event Type Classification

Classify the headline into one of the following categories:

| Category | Examples |
|----------|----------|
| Monetary Policy | FOMC, ECB, BOJ, rate hike, rate cut, QE/QT |
| Geopolitics | War, sanctions, tariffs, trade friction |
| Regulation & Policy | Environmental regulation, financial regulation, antitrust |
| Technology | AI, EV, renewables, semiconductors |
| Commodities | Crude oil, gold, copper, agricultural products |
| Corporate & M&A | Acquisitions, bankruptcies, earnings, industry restructuring |

#### Step 1.3: Reference Loading

Based on the event type, load the relevant references:

```
Read references/headline_event_patterns.md
Read references/sector_sensitivity_matrix.md
Read references/scenario_playbooks.md
```

**Reference contents:**
- `headline_event_patterns.md`: Historical event patterns and market reactions
- `sector_sensitivity_matrix.md`: Event × sector impact-magnitude matrix
- `scenario_playbooks.md`: Scenario-construction templates and best practices

---

### Phase 2: Agent Invocation

#### Step 2.1: Invoke scenario-analyst

Use the Agent tool to invoke the primary analysis agent.

```
Agent tool:
- subagent_type: "scenario-analyst"
- prompt: |
    Perform an 18-month scenario analysis for the following headline.

    ## Target Headline
    [the input headline]

    ## Event Type
    [classification result]

    ## Reference Information
    [summary of the loaded references]

    ## Analysis Requirements
    1. Use WebSearch to collect related news from the past 2 weeks
    2. Construct 3 scenarios — Base/Bull/Bear (probabilities sum to 100%)
    3. Analyze 1st/2nd/3rd-order impacts by sector
    4. Select 3-5 positive- and 3-5 negative-impact stocks (US market only)
    5. Output everything in English
```

**Expected output:**
- List of related news articles
- Details of the 3 scenarios (Base/Bull/Bear)
- Sector impact analysis (1st/2nd/3rd-order)
- Stock recommendation list

#### Step 2.2: Invoke strategy-reviewer

Using the scenario-analyst's results, invoke the review agent.

```
Agent tool:
- subagent_type: "strategy-reviewer"
- prompt: |
    Review the following scenario analysis.

    ## Target Headline
    [the input headline]

    ## Analysis Result
    [the full scenario-analyst output]

    ## Review Requirements
    Review from the following angles:
    1. Overlooked sectors/stocks
    2. Validity of the scenario probability allocation
    3. Logical consistency of the impact analysis
    4. Detection of optimism/pessimism bias
    5. Proposal of alternative scenarios
    6. Realism of the timeline

    Output constructive and specific feedback in English.
```

**Expected output:**
- Pointing out blind spots
- Opinion on the scenario probabilities
- Pointing out bias
- Proposal of alternative scenarios
- Final recommendations

---

### Phase 3: Integration & Report Generation

#### Step 3.1: Integrate Results

Integrate the output of both agents to produce the final investment judgment.

**Integration points:**
1. Fill in the blind spots raised in the review
2. Adjust the probability allocation (if needed)
3. Make the final judgment accounting for bias
4. Formulate a concrete action plan

#### Step 3.2: Generate Report

Generate the final report in the following format and save it to a file.

**Save location:** `reports/scenario_analysis_<topic>_YYYYMMDD.md`

```markdown
# Headline Scenario Analysis Report

**Analyzed at**: YYYY-MM-DD HH:MM
**Target headline**: [the input headline]
**Event type**: [classification category]

---

## 1. Related News Articles
[news list collected by scenario-analyst]

## 2. Scenario Overview (through 18 months out)

### Base Case (XX% probability)
[scenario details]

### Bull Case (XX% probability)
[scenario details]

### Bear Case (XX% probability)
[scenario details]

## 3. Sector / Industry Impact

### 1st-Order Impact (direct)
[impact table]

### 2nd-Order Impact (value chain / related industries)
[impact table]

### 3rd-Order Impact (macro / regulation / technology)
[impact table]

## 4. Stocks Expected to Benefit (3-5 tickers)
[stock table]

## 5. Stocks Expected to Be Hurt (3-5 tickers)
[stock table]

## 6. Second Opinion / Review
[strategy-reviewer output]

## 7. Final Investment Judgment & Implications

### Recommended Actions
[concrete actions informed by the review]

### Risk Factors
[list of key risks]

### Monitoring Points
[indicators / events to follow]

---
**Generated by**: scenario-analyzer skill
**Agents**: scenario-analyst, strategy-reviewer
```

#### Step 3.3: Save the Report

1. Create the `reports/` directory if it does not exist
2. Save as `scenario_analysis_<topic>_YYYYMMDD.md` (e.g., `scenario_analysis_venezuela_20260104.md`)
3. Notify the user that the save completed
4. **Do not save directly to the project root**

---

## Output

This skill generates the following file:

| File | Format | Description |
|------|--------|-------------|
| `reports/scenario_analysis_<topic>_YYYYMMDD.md` | Markdown | Comprehensive scenario analysis report |

**Output contents:**
- List of related news articles
- 3 scenarios — Base/Bull/Bear (with probability allocation)
- Sector impact analysis (1st/2nd/3rd-order)
- Positive/negative stock recommendations
- Second opinion / review
- Final investment judgment & implications

## Resources

### References
- `references/headline_event_patterns.md` - Event patterns and market reactions
- `references/sector_sensitivity_matrix.md` - Sector sensitivity matrix
- `references/scenario_playbooks.md` - Scenario-construction templates

### Agents
- `scenario-analyst` - Primary scenario analysis
- `strategy-reviewer` - Second opinion / review

---

## Important Notes

### Language
- All analysis and output are in **English**
- Stock tickers remain in their standard (English) symbols

### Target Market
- Stock selection is **US-listed equities only**
- ADRs included

### Time Horizon
- Scenarios target **18 months**
- Described in 3 phases: 0-6 months / 6-12 months / 12-18 months

### Probability Allocation
- Base + Bull + Bear = **100%**
- Each scenario's probability is described with its rationale

### Second Opinion
- **Mandatory** (always invoke strategy-reviewer)
- Review results are reflected in the final judgment

### Output Location (Important)
- **Always** save under the `reports/` directory
- Path: `reports/scenario_analysis_<topic>_YYYYMMDD.md`
- Example: `reports/scenario_analysis_fed_rate_hike_20260104.md`
- Create the `reports/` directory if it does not exist
- **Must not save directly to the project root**

---

## Quality Checklist

Confirm the following before finalizing the report:

- [ ] Is the headline parsed correctly?
- [ ] Is the event type classification appropriate?
- [ ] Do the 3 scenario probabilities sum to 100%?
- [ ] Are the 1st/2nd/3rd-order impacts logically connected?
- [ ] Is the stock selection backed by concrete rationale?
- [ ] Is the strategy-reviewer review included?
- [ ] Is the final judgment reflecting the review documented?
- [ ] Is the report saved to the correct path?

### Referencia: references/headline_event_patterns.md

# Headline Event Patterns

This reference documents the typical impact patterns that various event types
have on markets. Use it during scenario analysis to infer future developments
from past analogous events.

## 1. Monetary Policy Events

### Federal Reserve (FOMC)

#### Rate Hike
**Typical pattern:**
- **Immediate reaction (0-1 week)**: Equities dip temporarily, bond yields rise, USD strengthens
- **Short term (1-3 months)**: Growth stocks underperform value stocks
- **Medium term (3-12 months)**: Financials firm, real estate and utilities soft
- **Long term (12-18 months)**: Economic-slowdown concerns may surface

**Sector impact:**
| Sector | Impact | Reason |
|--------|--------|--------|
| Financials | + | Higher net interest income |
| Technology | - | Higher discount rate on high-valuation names |
| Real Estate | - | Weaker demand as mortgage rates rise |
| Utilities | - | Reduced appeal as a bond substitute |
| Consumer Discretionary | - | Higher borrowing costs dampen consumption |

**Historical cases:**
- 2022 hiking cycle: Nasdaq -33%, financials relatively resilient
- After Dec 2018 hike: S&P 500 -9% (December), rebound the following January

#### Rate Cut
**Typical pattern:**
- **Immediate reaction**: Equities rise, bond yields fall, USD weakens
- **Short term**: Growth stocks outperform
- **Medium term**: Real estate and utilities recover
- **Long term**: Corporate earnings improve on stimulus effect

**Caveats:**
- Recession-driven cuts may initially come with falling equities
- Market reaction differs between an "insurance cut" and a "recession response"

#### QE (Quantitative Easing) / QT (Quantitative Tightening)
**QE start:**
- Strong tailwind for equities (liquidity injection)
- Benefits all risk assets
- Weaker USD, higher commodities

**QT start:**
- Headwind for equities as liquidity shrinks
- Especially large impact on speculative assets and small caps
- Tendency toward a stronger USD

### European Central Bank (ECB)

**Characteristics:**
- Large impact on the EUR/USD exchange rate
- Direct impact on European bank stocks
- Peripheral-country spreads (Italy, Spain, etc.) are a key indicator

### Bank of Japan (BOJ)

**Characteristics:**
- Changes to YCC (Yield Curve Control) policy have an extremely large market impact
- Impact on the yen carry trade
- Japanese equities (Nikkei) tend to rise on a weaker yen

**2024 YCC adjustment case:**
- Raising the 10-year yield cap → sharp yen appreciation, global yields spill over higher

---

## 2. Geopolitical Events

### War / Armed Conflict

**Typical pattern:**
- **Immediate reaction**: Equities down, gold up, oil up, sovereign bonds up (flight to safe assets)
- **Short term**: Defense names rise, energy stocks firm
- **Medium term**: Impact on supply chains dependent on the conflict region
- **Long term**: Inflationary pressure, fiscal deterioration

**Sector impact:**
| Sector | Impact | Reason |
|--------|--------|--------|
| Defense | ++ | Higher military spending |
| Energy | + | Commodity prices rise on supply concerns |
| Airlines | - | Higher fuel costs, weaker demand |
| Insurance | - | Geopolitical-risk reserves |
| Supply-chain related | - | Logistics disruption, procurement risk |

**Historical cases:**
- Russia-Ukraine conflict (2022): WTI crude over $130, European gas crisis
- Middle East conflict (2023): Red Sea route risk, higher shipping costs

### Economic Sanctions

**Impact pattern:**
- Hits companies dependent on trade with the targeted country
- Commodity-supply concerns (when the target is a major exporter)
- Benefits to alternative suppliers

### Tariffs / Trade Friction

**Typical pattern:**
- **Immediate reaction**: Equity market of the targeted country falls, related sectors sold off
- **Short term**: Earnings concerns for export-dependent companies
- **Medium term**: Moves to rebuild supply chains
- **Long term**: Progress of onshoring / friend-shoring

**2018-2019 US-China trade friction case:**
- Impact on China-dependent semiconductors and agricultural machinery
- Shift to Mexico/Vietnam to avoid tariffs

---

## 3. Regulation & Policy Changes

### Environmental Regulation

**Tighter carbon regulation:**
- **Beneficiaries**: Renewables, EV, clean tech
- **Hurt**: Oil & gas, coal, airlines, heavy industry

**Emissions trading:**
- Rising carbon-credit prices → higher costs for high-emission companies

### Financial Regulation

**Tighter capital regulation:**
- Higher bank capital-ratio requirements → pressure on bank profitability
- Larger impact on small and mid-sized banks

**Crypto-asset regulation:**
- Tighter regulation → hits crypto-related stocks, benefits traditional finance
- Regulatory clarity → can also be received positively by the market

### Antitrust

**Blocking large M&A:**
- Share-price decline of the target companies
- Delay in industry consolidation

**Big Tech regulation:**
- Business-breakup risk for platform companies
- Benefits to competitors and emerging companies

---

## 4. Technology Shifts

### AI Revolution

**Beneficiary sectors:**
| Sector | Example tickers | Reason |
|--------|-----------------|--------|
| Semiconductors | NVDA, AMD, AVGO | AI chip demand |
| Cloud | MSFT, AMZN, GOOGL | AI foundational infrastructure |
| Software | CRM, NOW, ADBE | AI feature integration |

**Hurt sectors:**
| Sector | Example tickers | Reason |
|--------|-----------------|--------|
| Call centers | - | AI automation |
| Translation / localization | - | Replacement by AI |
| Simple-task BPO | - | RPA/AI replacement |

### EV (Electric Vehicle) Adoption

**Beneficiaries:**
- Lithium, cobalt, nickel related
- EV charging infrastructure
- Utilities (higher demand)

**Hurt:**
- Legacy auto parts (engines, transmissions)
- Gas stations
- Oil refining

### Renewable Energy

**When policy support expands:**
- Solar/wind related stocks rise
- Utility-scale storage demand

**When policy retreats:**
- Clean-energy stocks fall
- Capital rotates back to legacy energy stocks

---

## 5. Commodity Shocks

### Crude Oil Price

**Spike scenario (supply shock):**
- **Beneficiaries**: Oil majors, shale companies, oilfield services
- **Hurt**: Airlines, transportation, chemicals, consumer goods

**Crash scenario (demand decline):**
- **Beneficiaries**: Airlines, transportation, consumer goods
- **Hurt**: Energy sector broadly

**Thresholds:**
- Below $80: Energy stocks soft
- Above $100: Inflation concerns, deteriorating consumer sentiment

### Gold

**Drivers of an increase:**
- Geopolitical risk
- Inflation concerns
- Falling real interest rates
- Weaker USD

**Related tickers:**
- Gold miners: NEM, GOLD, AEM
- Gold ETFs: GLD, IAU

### Copper

**Role as an economic indicator (Dr. Copper):**
- Rising copper price → economic-expansion signal
- Falling copper price → economic-slowdown signal

**Related sectors:**
- Mining: FCX, SCCO
- Construction / infrastructure
- EV (copper is a key material)

---

## 6. Corporate & M&A

### Large Acquisition Announcement

**Typical pattern:**
- Acquired company: +20-40% (premium reflected)
- Acquiring company: -3-10% (dilution / premium concerns)
- Industry peers: +5-15% (speculation as the next acquisition target)

### Large Bankruptcy

**Systemic-risk concern:**
- Spills over to the entire financial sector
- Widening credit spreads

**Single-company bankruptcy:**
- Benefits competitors (market-share gains)
- Hurts suppliers

### Spin-off

**Typical pattern:**
- Parent company: uncertain in the short term, valued for slimming down in the medium term
- Spin-off company: tends to rise on post-independence growth expectations

---

## Usage Notes

1. **Past patterns are a reference**: Reactions differ depending on the market environment
2. **Consider compound factors**: Analyze the interaction of multiple factors, not a single event
3. **Importance of timing**: Reactions change based on how much the market has priced in
4. **Check the scale**: Impact magnitude differs with the scale of the event
5. **Periodic updates**: Revisit patterns as market structure changes

### Referencia: references/scenario_playbooks.md

# Scenario Playbooks

This reference provides templates and best practices for constructing
18-month scenarios. Use it during scenario analysis to produce consistent,
high-quality scenarios.

## Core Principles of Scenario Construction

### 1. MECE Principle (Mutually Exclusive, Collectively Exhaustive)

Scenarios should satisfy:
- **Mutually exclusive**: scenarios do not overlap
- **Collectively exhaustive**: cover all major possibilities

### 2. Probability Allocation Guidelines

| Scenario | Typical range | Rationale for the allocation |
|----------|---------------|------------------------------|
| Base Case | 50-65% | Most probable development |
| Bull Case | 15-25% | Positive upside |
| Bear Case | 20-30% | Negative downside |
| Total | 100% | Always adjust so it sums to 100% |

**When an asymmetric allocation is appropriate:**
- Bull > Bear: environment with many bullish drivers
- Bear > Bull: environment with many risk factors
- Base > 60%: low-uncertainty situation
- Base < 50%: extremely high-uncertainty situation (even the Base Case is uncertain)

### 3. Timeline Segmentation

**3-phase structure:**
- **0-6 months**: short-term reaction, initial moves
- **6-12 months**: medium-term development, trend formation
- **12-18 months**: long-term outcome, new equilibrium

---

## Scenario Templates

### Base Case Template

```markdown
### Base Case (XX% probability)

**Summary**:
[Summarize the scenario in 1-2 sentences. Describe the most probable development.]

**Assumptions**:
- [Assumption 1]: [specific condition]
- [Assumption 2]: [specific condition]
- [Assumption 3]: [specific condition]

**Timeline**:

**0-6 months:**
- [Key development 1]
- [Key development 2]
- [Expected market reaction]

**6-12 months:**
- [Medium-term development 1]
- [Medium-term development 2]
- [Trend direction]

**12-18 months:**
- [Long-term outcome 1]
- [New equilibrium state]
- [Structural change (if any)]

**Impact on economic indicators**:
| Indicator | Current | 6-month forecast | 12-month forecast | 18-month forecast |
|-----------|---------|------------------|-------------------|-------------------|
| GDP growth | X% | X% | X% | X% |
| Inflation | X% | X% | X% | X% |
| Policy rate | X% | X% | X% | X% |
| Unemployment | X% | X% | X% | X% |

**Key catalysts**:
- [Factor that supports this scenario 1]
- [Factor that supports this scenario 2]

**Invalidation signals**:
- [Sign this scenario is breaking down 1]
- [Sign this scenario is breaking down 2]
```

### Bull Case Template

```markdown
### Bull Case (XX% probability)

**Summary**:
[Summarize the optimistic scenario in 1-2 sentences. What kind of upside occurs.]

**Assumptions**:
- [Optimistic assumption 1]: [specific condition]
- [Optimistic assumption 2]: [specific condition]
- [Optimistic assumption 3]: [specific condition]

**Timeline**:

**0-6 months:**
- [Positive development 1]
- [Positive development 2]
- [Expected favorable market reaction]

**6-12 months:**
- [Continuation of the upside trend]
- [Additional positive factors]
- [Improving market sentiment]

**12-18 months:**
- [Outcome of the optimistic scenario]
- [State achieved]
- [Sustainability assessment]

**Impact on economic indicators**:
[Assume figures better than the Base Case]

**Upside catalysts**:
- [Factor that realizes this scenario 1]
- [Factor that realizes this scenario 2]

**Conditions that raise this scenario's probability**:
- [Condition 1]
- [Condition 2]
```

### Bear Case Template

```markdown
### Bear Case (XX% probability)

**Summary**:
[Summarize the risk scenario in 1-2 sentences. What kind of downside occurs.]

**Assumptions**:
- [Risk assumption 1]: [specific condition]
- [Risk assumption 2]: [specific condition]
- [Risk assumption 3]: [specific condition]

**Timeline**:

**0-6 months:**
- [Negative development 1]
- [Negative development 2]
- [Expected adverse market reaction]

**6-12 months:**
- [Continuation/deepening of the downside trend]
- [Secondary problems surfacing]
- [Deteriorating market sentiment]

**12-18 months:**
- [Outcome of the risk scenario]
- [Worst-case state]
- [Recovery path (if any)]

**Impact on economic indicators**:
[Assume figures worse than the Base Case]

**Downside risk factors**:
- [Factor that triggers this scenario 1]
- [Factor that triggers this scenario 2]

**Conditions that raise this scenario's probability**:
- [Condition 1]
- [Condition 2]

**Risk-mitigating factors**:
- [Factor that may mitigate this scenario 1]
- [Factor that may mitigate this scenario 2]
```

---

## Scenario Playbooks by Event Type

### 1. Monetary Policy Event (Rate Hike)

**Base Case (55%):**
- Rate hike implemented as expected
- Market has largely priced it in
- Mild equity dip, slight rise in bond yields

**Bull Case (20%):**
- Hike smaller than expected
- Dovish forward guidance
- Equity-market rally

**Bear Case (25%):**
- Hike larger than expected
- Hawkish forward guidance
- Sharp equity selloff, widening credit spreads

### 2. Geopolitical Event (Conflict Outbreak)

**Base Case (50%):**
- Limited escalation of the conflict
- Short-term rise in commodity prices
- Situation stabilizes within a few months

**Bull Case (15%):**
- Early ceasefire / peace agreement
- Commodity prices normalize
- Market recovers early

**Bear Case (35%):**
- Prolonged / expanded conflict
- Serious disruption of commodity supply
- Accelerating global inflation, recession risk

### 3. Technology Shift (AI Regulation)

**Base Case (50%):**
- Gradual introduction of regulation
- Industry self-regulation predominates
- Limited impact on innovation

**Bull Case (25%):**
- Regulation formulated in a way favorable to the industry
- Regulatory clarity actually accelerates investment
- Entry barriers formed that favor incumbents

**Bear Case (25%):**
- Strict regulation introduced
- Significant restrictions on AI development
- Decline in US companies' competitiveness

### 4. Corporate Event (Large M&A)

**Base Case (60%):**
- Regulatory approval obtained
- Closing on schedule
- Gradual realization of integration synergies

**Bull Case (15%):**
- Synergies realized beyond expectations
- Integration goes smoothly
- Additional M&A strategy succeeds

**Bear Case (25%):**
- Blocked by regulators or conditional approval
- Delay / failure of integration
- Synergies not achieved

---

## Scenario Quality Checklist

### Internal Consistency
- [ ] Are the assumptions of each scenario logically consistent?
- [ ] Is the causality of the timeline development clear?
- [ ] Are the economic-indicator forecasts mutually consistent?

### External Validity
- [ ] Is it consistent with past analogous events?
- [ ] Does it appropriately reflect the current market environment?
- [ ] Does it not diverge greatly from expert views?

### Practicality
- [ ] Is there enough specificity to be useful for investment decisions?
- [ ] Are monitorable catalysts identified?
- [ ] Are invalidation signals clear?

### Comprehensiveness
- [ ] Are the major risk scenarios included?
- [ ] Is the upside possibility appropriately considered?
- [ ] Is there mention of tail risk?

---

## Common Mistakes and How to Avoid Them

### 1. Status-quo bias
**Problem**: Assigning excessive probability to the Base Case (70%+)
**Avoid**: Recognize that historically the probability of "nothing changes" is low

### 2. Recency bias
**Problem**: Overestimating the impact of the most recent event
**Avoid**: Maintain a long-term view, refer to past patterns

### 3. Confirmation bias
**Problem**: Adopting only interpretations aligned with the headline
**Avoid**: Deliberately seek out opposing views

### 4. Excessive precision
**Problem**: Forecasting figures 18 months out to decimal places
**Avoid**: Acknowledge uncertainty, express as a range

### 5. Scenario overlap
**Problem**: Base/Bull/Bear partially overlap
**Avoid**: Clarify the boundary conditions of each scenario

---

## Probability Update Guidelines

Probability adjustment when new information arrives:

| Nature of new information | Direction of probability adjustment |
|---------------------------|-------------------------------------|
| Data supporting a scenario | +5-15% |
| Data contradicting a scenario | -5-15% |
| Decisive evidence | +20-30% or -20-30% |
| Emergence of a new risk factor | Bear Case +5-10% |
| Resolution of a risk factor | Bear Case -5-10% |

**After adjustment, always re-normalize to 100% total**

---

## Output Quality Standards

Characteristics of a high-quality scenario:
1. **Specificity**: not abstract; includes figures, dates, names
2. **Logic**: clear causality
3. **Verifiability**: correctness can be judged later
4. **Practicality**: includes information directly tied to investment decisions
5. **Humility**: appropriately expresses uncertainty

### Referencia: references/sector_sensitivity_matrix.md

# Sector Sensitivity Matrix

This reference organizes sector-by-sector sensitivity to various event types
in matrix form. Use it during scenario analysis to quickly judge which sectors
are most likely to be affected.

## Legend

**Impact:**
- `++` : Strong positive impact
- `+` : Positive impact
- `0` : Neutral / minor impact
- `-` : Negative impact
- `--` : Strong negative impact

**Confidence:**
- `H` : High (past patterns are consistent)
- `M` : Medium (situation-dependent)
- `L` : Low (high uncertainty)

---

## 1. Monetary Policy Event Matrices

### Rate-Hike Environment

| Sector | Impact | Confidence | Representative tickers | Notes |
|--------|--------|------------|------------------------|-------|
| Financials (banks) | + | H | JPM, BAC, WFC | Higher net interest income |
| Financials (insurance) | + | M | MET, PRU, AIG | Improved investment income |
| Technology | - | H | AAPL, MSFT, NVDA | High-valuation discount |
| Consumer Discretionary | - | H | AMZN, HD, NKE | Higher borrowing costs |
| Real Estate (REIT) | -- | H | AMT, PLD, EQIX | Rate-sensitive, higher funding costs |
| Utilities | - | H | NEE, DUK, SO | Reduced appeal as a bond substitute |
| Healthcare | 0 | M | UNH, JNJ, PFE | Relatively defensive |
| Consumer Staples | 0 | M | PG, KO, WMT | Relatively defensive |
| Energy | 0 | L | XOM, CVX, COP | Macro-environment dependent |
| Materials | - | M | LIN, APD, ECL | Economically sensitive |
| Industrials | - | M | CAT, DE, HON | Capex-slowdown concern |
| Communication Services | 0 | M | GOOGL, META, DIS | Idiosyncratic factors dominate |

### Rate-Cut Environment

| Sector | Impact | Confidence | Representative tickers | Notes |
|--------|--------|------------|------------------------|-------|
| Technology | ++ | H | AAPL, MSFT, NVDA | Growth-stock valuation expansion |
| Real Estate (REIT) | ++ | H | AMT, PLD, EQIX | Lower funding costs |
| Utilities | + | H | NEE, DUK, SO | Relatively more attractive dividend yield |
| Consumer Discretionary | + | H | AMZN, HD, NKE | Consumption stimulus |
| Financials (banks) | - | H | JPM, BAC, WFC | Lower net interest income |
| Healthcare | 0 | M | UNH, JNJ, PFE | Relatively defensive |
| Consumer Staples | 0 | M | PG, KO, WMT | Relatively defensive |
| Energy | 0 | L | XOM, CVX, COP | Macro-environment dependent |

---

## 2. Geopolitical Event Matrices

### War / Armed Conflict

| Sector | Impact | Confidence | Representative tickers | Notes |
|--------|--------|------------|------------------------|-------|
| Defense | ++ | H | LMT, RTX, NOC, GD | Higher military spending |
| Energy | + | H | XOM, CVX, COP | Prices rise on supply concerns |
| Gold (miners) | ++ | H | NEM, GOLD, AEM | Safe-asset demand |
| Airlines | -- | H | DAL, UAL, AAL | Fuel costs, weaker demand |
| Travel & Leisure | -- | H | MAR, HLT, BKNG | Demand decline |
| Insurance | - | M | AIG, TRV, ALL | Geopolitical-risk reserves |
| Semiconductors | - | M | NVDA, AMD, INTC | Supply-chain risk |
| Shipping | +/- | L | ZIM, DAC, MATX | Impact differs by route dependence |

### Tariffs / Trade Friction (vs. China)

| Sector | Impact | Confidence | Representative tickers | Notes |
|--------|--------|------------|------------------------|-------|
| Semiconductors (equipment) | -- | H | AMAT, LRCX, KLAC | China-market restrictions |
| Consumer goods (China-dependent) | - | H | NKE, AAPL | Impact on both manufacturing and sales |
| Agriculture | - | H | DE, ADM, BG | Lower exports to China |
| Mexico-production companies | + | M | - | Supply-chain substitution benefit |
| Domestic manufacturers | + | M | - | Onshoring benefit |

---

## 3. Regulation & Policy Change Matrices

### Tighter Environmental Regulation

| Sector | Impact | Confidence | Representative tickers | Notes |
|--------|--------|------------|------------------------|-------|
| Renewables (solar) | ++ | H | ENPH, SEDG, FSLR | Expanded policy support |
| Renewables (wind) | ++ | H | NEE, AES | Expanded policy support |
| EV | ++ | H | TSLA, RIVN, LCID | Demand increase from regulation |
| Lithium / batteries | ++ | H | ALB, LTHM | Tied to EV demand |
| Oil & gas | -- | H | XOM, CVX, COP | Stranded-asset risk |
| Coal | -- | H | - | Accelerated fade-out |
| Airlines | - | M | DAL, UAL, AAL | SAF-mandate cost |
| Automakers (legacy) | - | M | F, GM | EV-transition cost |

### Tighter Financial Regulation

| Sector | Impact | Confidence | Representative tickers | Notes |
|--------|--------|------------|------------------------|-------|
| Large banks | - | H | JPM, BAC, C | Higher capital requirements, profit pressure |
| Regional banks | -- | H | - | Heavy regulatory-cost burden |
| Fintech | +/- | M | SQ, PYPL | Benefit/hurt depending on regulation |
| Crypto-asset related | - | M | COIN | Regulatory uncertainty |

### Tighter Antitrust

| Sector | Impact | Confidence | Representative tickers | Notes |
|--------|--------|------------|------------------------|-------|
| Big Tech | - | M | GOOGL, META, AMZN, AAPL | Business-breakup risk |
| Telecom | - | M | T, VZ | M&A-blocking risk |
| Small/mid tech | + | M | - | Improved competitive-environment benefit |

---

## 4. Technology Shift Matrices

### Accelerating AI Revolution

| Sector | Impact | Confidence | Representative tickers | Notes |
|--------|--------|------------|------------------------|-------|
| Semiconductors (GPU) | ++ | H | NVDA, AMD | AI training/inference chip demand |
| Semiconductors (memory) | ++ | H | MU, WDC | HBM demand |
| Cloud infrastructure | ++ | H | MSFT, AMZN, GOOGL | Provides AI foundation |
| Enterprise SW | + | H | CRM, NOW, ADBE | AI feature integration |
| Data-center REIT | ++ | H | EQIX, DLR | Surging demand |
| Utilities | + | M | NEE, SO | Data-center power demand |
| BPO / outsourcing | -- | M | - | Replacement by AI automation |

### Accelerating EV Adoption

| Sector | Impact | Confidence | Representative tickers | Notes |
|--------|--------|------------|------------------------|-------|
| EV manufacturing | ++ | H | TSLA, RIVN | Market expansion |
| Battery / lithium | ++ | H | ALB, LTHM, LAC | Material demand |
| Charging infrastructure | ++ | H | CHPT, BLNK | Infrastructure investment |
| Utilities | + | M | NEE, SO | Higher power demand |
| Legacy automakers | - | M | F, GM | Transition cost |
| Auto parts (engines) | -- | H | - | Demand-structure change |
| Oil refining | - | M | VLO, PSX | Lower gasoline demand |

---

## 5. Commodity Shock Matrices

### Crude Oil Price Spike ($100+/bbl)

| Sector | Impact | Confidence | Representative tickers | Notes |
|--------|--------|------------|------------------------|-------|
| Oil majors | ++ | H | XOM, CVX, COP | Surging profits |
| Shale companies | ++ | H | PXD, EOG, DVN | Large improvement in economics |
| Oilfield services | ++ | H | SLB, HAL, BKR | Increased drilling activity |
| Airlines | -- | H | DAL, UAL, AAL | Sharply higher fuel costs |
| Transportation | -- | H | UPS, FDX | Higher fuel costs |
| Chemicals | - | H | DOW, LYB | Higher feedstock costs |
| Consumer goods | - | M | Broad | Lower consumer purchasing power |

### Crude Oil Price Crash ($50-/bbl)

| Sector | Impact | Confidence | Representative tickers | Notes |
|--------|--------|------------|------------------------|-------|
| Oil majors | -- | H | XOM, CVX, COP | Lower profits, capex cuts |
| Shale companies | -- | H | PXD, EOG, DVN | Below-breakeven risk |
| Airlines | ++ | H | DAL, UAL, AAL | Lower fuel costs |
| Consumer goods | + | M | Broad | Higher disposable income |
| Chemicals | + | M | DOW, LYB | Lower feedstock costs |

### Gold Price Spike

| Sector | Impact | Confidence | Representative tickers | Notes |
|--------|--------|------------|------------------------|-------|
| Gold miners | ++ | H | NEM, GOLD, AEM | Leverage effect |
| Silver miners | ++ | H | PAAS, AG, HL | Precious-metals linkage |
| Jewelry | 0 | M | SIG, TIF | Demand decline offset by higher inventory value |

---

## 6. Economic Cycle Matrices

### Economic Expansion

| Sector | Impact | Confidence | Representative tickers | Notes |
|--------|--------|------------|------------------------|-------|
| Technology | ++ | H | AAPL, MSFT, NVDA | Higher corporate IT spending |
| Consumer Discretionary | ++ | H | AMZN, HD, NKE | Consumption expansion |
| Industrials | ++ | H | CAT, DE, HON | Higher capex |
| Materials | + | H | LIN, APD, FCX | Higher demand |
| Financials | + | H | JPM, BAC, GS | Credit expansion, active M&A |

### Economic Recession

| Sector | Impact | Confidence | Representative tickers | Notes |
|--------|--------|------------|------------------------|-------|
| Consumer Staples | + | H | PG, KO, WMT | Defensive |
| Healthcare | + | H | UNH, JNJ, PFE | Non-discretionary spending |
| Utilities | + | H | NEE, DUK, SO | Stable dividends |
| Consumer Discretionary | -- | H | AMZN, HD, NKE | Discretionary-spending cuts |
| Industrials | -- | H | CAT, DE, HON | Capex freeze |
| Financials | - | H | JPM, BAC | Rising loan-loss concerns |

---

## How to Use

1. **Identify the event type**: Judge the event category from the headline
2. **Refer to the relevant matrix**: Select the appropriate matrix above
3. **Check impact and confidence**: Understand the impact per sector
4. **Use representative tickers as a starting point**: As the basis for deeper analysis
5. **For compound scenarios, refer to multiple matrices**: Integrate multiple matrices when several events are involved

## Caveats

- **Single-stock situation**: Sector impact and single-stock impact can differ
- **Timing**: Distinguish immediate impact from delayed impact
- **Scale**: Impact magnitude varies with the scale of the event
- **Degree of market pricing-in**: If the market has already priced it in, the reaction is limited


---

## SKILL: sector-analyst

- Fuente: `tradermonty/claude-trading-skills` → `examples/weekly-trade-strategy/.claude/skills/sector-analyst` (MIT)
- Cuándo usarla: This skill should be used when analyzing sector and industry performance charts to assess market positioning and rotation patterns. Use this skill when the user provides performance chart images (1-week or 1-month timeframes) for sectors or industries and requests market cycle assessment, sector rotation analysis, or strategic positioning recommendations based on performance data. All analysis and output are conducted in English.

# Sector Analyst

## Overview

This skill enables comprehensive analysis of sector and industry performance charts to identify market cycle positioning and predict likely rotation scenarios. The analysis combines observed performance data with established sector rotation principles to provide objective market assessment and probabilistic scenario forecasting.

## When to Use This Skill

Use this skill when:
- User provides sector performance charts (typically 1-week and 1-month timeframes)
- User provides industry performance charts showing relative performance data
- User requests analysis of current market cycle positioning
- User asks for sector rotation assessment or predictions
- User needs probability-weighted scenarios for market positioning

Example user requests:
- "Analyze these sector performance charts and tell me where we are in the market cycle"
- "Based on these performance charts, what sectors should outperform next?"
- "What's the probability of a defensive rotation based on this data?"
- "Review these sector and industry charts and provide scenario analysis"

## Analysis Workflow

Follow this structured workflow when analyzing sector/industry performance charts:

### Step 1: Data Collection and Observation

First, carefully examine all provided chart images to extract:
- **Sector-level performance**: Identify which sectors (Technology, Financials, Consumer Discretionary, etc.) are outperforming/underperforming
- **Industry-level performance**: Note specific industries showing strength or weakness
- **Timeframe comparison**: Compare 1-week vs 1-month performance to identify trend consistency or divergence
- **Magnitude of moves**: Assess the size of relative performance differences
- **Breadth of movement**: Determine if performance is concentrated or broad-based

Think in English while analyzing the charts. Document specific numerical performance figures for key sectors and industries.

### Step 2: Market Cycle Assessment

Load the sector rotation knowledge base to inform analysis:
- Read `references/sector_rotation.md` to access market cycle and sector rotation frameworks
- Compare observed performance patterns against expected patterns for each cycle phase:
  - Early Cycle Recovery
  - Mid Cycle Expansion
  - Late Cycle
  - Recession

Identify which cycle phase best matches current observations by:
- Mapping outperforming sectors to typical cycle leaders
- Mapping underperforming sectors to typical cycle laggards
- Assessing consistency across multiple sectors
- Evaluating alignment with defensive vs cyclical sector performance

### Step 3: Current Situation Analysis

Synthesize observations into an objective assessment:
- State which market cycle phase current performance most closely resembles
- Highlight supporting evidence (which sectors/industries confirm this view)
- Note any contradictory signals or unusual patterns
- Assess confidence level based on consistency of signals

Use data-driven language and specific references to performance figures.

### Step 4: Scenario Development

Based on sector rotation principles and current positioning, develop 2-4 potential scenarios for the next phase:

For each scenario:
- Describe the market cycle transition
- Identify which sectors would likely outperform
- Identify which sectors would likely underperform
- Specify the catalysts or conditions that would confirm this scenario
- Assign a probability (see Probability Assessment Framework in sector_rotation.md)

Scenarios should range from most likely (highest probability) to alternative/contrarian scenarios.

### Step 5: Output Generation

Create a structured Markdown document with the following sections:

**Required Sections:**
1. **Executive Summary**: 2-3 sentence overview of key findings
2. **Current Situation**: Detailed analysis of current performance patterns and market cycle positioning
3. **Supporting Evidence**: Specific sector and industry performance data supporting the cycle assessment
4. **Scenario Analysis**: 2-4 scenarios with descriptions and probability assignments
5. **Recommended Positioning**: Strategic and tactical positioning recommendations based on scenario probabilities
6. **Key Risks**: Notable risks or contradictory signals to monitor

## Output Format

Save analysis results as a Markdown file with naming convention: `sector_analysis_YYYY-MM-DD.md`

Use this structure:

```markdown
# Sector Performance Analysis - [Date]

## Executive Summary

[2-3 sentences summarizing key findings]

## Current Situation

### Market Cycle Assessment
[Which cycle phase and why]

### Performance Patterns Observed

#### 1-Week Performance
[Analysis of recent performance]

#### 1-Month Performance
[Analysis of medium-term trends]

#### Sector-Level Analysis
[Detailed breakdown by sector]

#### Industry-Level Analysis
[Notable industry-specific observations]

## Supporting Evidence

### Confirming Signals
- [List data points supporting cycle assessment]

### Contradictory Signals
- [List any conflicting indicators]

## Scenario Analysis

### Scenario 1: [Name] (Probability: XX%)
**Description**: [What happens]
**Outperformers**: [Sectors/industries]
**Underperformers**: [Sectors/industries]
**Catalysts**: [What would confirm this scenario]

### Scenario 2: [Name] (Probability: XX%)
[Repeat structure]

[Additional scenarios as appropriate]

## Recommended Positioning

### Strategic Positioning (Medium-term)
[Sector allocation recommendations]

### Tactical Positioning (Short-term)
[Specific adjustments or opportunities]

## Key Risks and Monitoring Points

[What to watch that could invalidate the analysis]

---
*Analysis Date: [Date]*
*Data Period: [Timeframe of charts analyzed]*
```

## Key Analysis Principles

When conducting analysis:

1. **Objectivity First**: Let the data guide conclusions, not preconceptions
2. **Probabilistic Thinking**: Express uncertainty through probability ranges
3. **Multiple Timeframes**: Compare 1-week and 1-month data for trend confirmation
4. **Relative Performance**: Focus on relative strength, not absolute returns
5. **Breadth Matters**: Broad-based moves are more significant than isolated movements
6. **No Absolutes**: Markets rarely follow textbook patterns exactly
7. **Historical Context**: Reference typical rotation patterns but acknowledge uniqueness

## Probability Guidelines

Apply these probability ranges based on evidence strength:

- **70-85%**: Strong evidence with multiple confirming signals across sectors and timeframes
- **50-70%**: Moderate evidence with some confirming signals but mixed indicators
- **30-50%**: Weak evidence with limited or conflicting signals
- **15-30%**: Speculative scenario contrary to current indicators but possible

Total probabilities across all scenarios should sum to approximately 100%.

## Resources

### references/
- `sector_rotation.md` - Comprehensive knowledge base covering market cycle phases, typical sector performance patterns, and probability assessment frameworks

### assets/
Sample charts demonstrating the expected input format:
- `sector_performance.jpeg` - Example sector-level performance chart (1-week and 1-month)
- `industory_performance_1.jpeg` - Example industry performance chart (outperformers)
- `industory_performance_2.jpeg` - Example industry performance chart (underperformers)

These samples illustrate the type of visual data this skill analyzes. User-provided charts may vary in format but should contain similar relative performance information.

## Important Notes

- All analysis thinking should be conducted in English
- Output Markdown files must be in English
- Reference the sector rotation knowledge base for each analysis
- Maintain objectivity and avoid confirmation bias
- Update probability assessments if new data becomes available
- Charts typically show performance over 1-week and 1-month periods

### Referencia: references/sector_rotation.md

# Sector Rotation Knowledge Base

## Market Cycle Framework

The economic cycle can be divided into four primary phases, each characterized by distinct economic conditions and sector performance patterns.

### 1. Early Cycle Recovery

**Economic Characteristics:**
- Economy begins recovering from recession
- GDP growth accelerates from negative/low to positive
- Interest rates remain low
- Central banks maintain accommodative policy
- Credit conditions begin to ease
- Consumer and business confidence starts improving

**Outperforming Sectors:**
- **Technology**: Benefits from improving economic outlook and investment spending
- **Consumer Cyclical/Discretionary**: Rebounds as consumer confidence returns
- **Industrials**: Early beneficiary of economic recovery and capital spending
- **Financials**: Benefits from steepening yield curve and improving credit conditions
- **Real Estate**: Low interest rates support property valuations

**Underperforming Sectors:**
- **Utilities**: Low growth characteristics become less attractive
- **Consumer Defensive/Staples**: Defensive qualities less valued in recovery
- **Healthcare**: Stable growth profile less appealing in early recovery

### 2. Mid Cycle Expansion

**Economic Characteristics:**
- Strong GDP growth continues
- Corporate earnings growth robust
- Employment gains accelerating
- Interest rates begin rising from lows
- Credit spreads narrow
- Inflation remains moderate

**Outperforming Sectors:**
- **Technology**: Continued strong earnings growth
- **Industrials**: Peak capital spending and economic activity
- **Consumer Discretionary**: Strong consumer spending continues
- **Materials**: Strong demand from construction and manufacturing
- **Energy**: Rising economic activity drives energy demand

**Underperforming Sectors:**
- **Utilities**: Rising rates pressure valuations
- **Consumer Staples**: Growth acceleration favors cyclical exposure
- **Telecommunications**: Low growth profile less attractive

### 3. Late Cycle

**Economic Characteristics:**
- GDP growth begins decelerating but remains positive
- Interest rates peak or plateau at higher levels
- Inflation pressures build
- Labor markets tight, wage pressures increase
- Credit conditions begin tightening
- Economic indicators show signs of slowing

**Outperforming Sectors:**
- **Energy**: Benefits from inflation and commodity price strength
- **Materials**: Inflation hedge characteristics
- **Financials**: Higher interest rates support net interest margins
- **Healthcare**: Defensive qualities become attractive as growth slows
- **Consumer Staples**: Defensive positioning as uncertainty rises

**Underperforming Sectors:**
- **Technology**: High valuations pressured by rising rates
- **Consumer Discretionary**: Weakening consumer confidence
- **Real Estate**: High interest rates pressure valuations
- **Industrials**: Capital spending begins to slow

### 4. Recession

**Economic Characteristics:**
- GDP contracts (negative growth)
- Rising unemployment
- Interest rates cut by central banks
- Credit spreads widen significantly
- Corporate earnings decline
- Consumer and business confidence deteriorate

**Outperforming Sectors:**
- **Utilities**: Defensive, stable cash flows attractive
- **Consumer Staples**: Essential goods demand remains stable
- **Healthcare**: Non-discretionary spending, defensive characteristics
- **Telecommunications/Communication Services**: Stable revenue streams

**Underperforming Sectors:**
- **Financials**: Credit losses and economic stress
- **Consumer Discretionary**: Discretionary spending cuts
- **Industrials**: Sharp decline in capital spending
- **Materials**: Demand destruction
- **Energy**: Economic weakness reduces demand
- **Real Estate**: Economic stress and potential defaults

## Sector Characteristics Summary

### Cyclical Sectors (Outperform in Early/Mid Cycle)
- Technology
- Consumer Discretionary
- Industrials
- Materials
- Financials (with varying timing)
- Energy (stronger in Mid/Late Cycle)

### Defensive Sectors (Outperform in Late Cycle/Recession)
- Utilities
- Consumer Staples
- Healthcare
- Communication Services

### Interest Rate Sensitive Sectors
- **Benefit from Rising Rates**: Financials (banks)
- **Hurt by Rising Rates**: Utilities, Real Estate, Technology (high growth)

## Industry-Level Nuances

Within each sector, industry-level performance can vary:

### Technology Sector
- **Early/Mid Cycle Leaders**: Software, Semiconductors, Hardware
- **Late Cycle/Defensive**: IT Services, Enterprise Software (recurring revenue models)

### Consumer Discretionary
- **Early/Mid Cycle Leaders**: Auto Manufacturers, Homebuilders, Retail, Leisure
- **More Resilient**: Education, Entertainment (streaming)

### Financials
- **Early Cycle**: Diversified Banks, Investment Banks
- **Mid/Late Cycle**: Insurance, Asset Managers
- **Recession Vulnerable**: Regional Banks, Consumer Finance

### Industrials
- **Early/Mid Cycle**: Construction, Machinery, Transportation
- **More Defensive**: Aerospace & Defense, Waste Management

### Healthcare
- **Cyclical Elements**: Elective procedures, Medical Devices
- **Defensive Elements**: Pharmaceuticals, Healthcare Plans, Hospitals

### Materials
- **Early/Mid Cycle**: Construction Materials, Chemicals
- **Late Cycle/Inflation Hedge**: Precious Metals (Gold, Silver)

## Key Analysis Principles

1. **No Cycle is Identical**: While patterns repeat, timing and magnitude vary
2. **Multiple Indicators**: Combine sector performance with economic indicators
3. **Rotation is Gradual**: Transitions between cycles occur over months, not days
4. **Relative Performance**: Focus on relative strength vs absolute returns
5. **Leading vs Lagging**: Some sectors lead cycle transitions, others lag
6. **Global Factors**: International economic conditions affect sector performance
7. **Policy Impact**: Central bank and fiscal policy can accelerate or delay rotations

## Probability Assessment Framework

When assessing future scenarios, consider:

- **Strong Evidence (70-85% probability)**: Multiple confirming indicators across sectors
- **Moderate Evidence (50-70% probability)**: Some confirming signals but mixed data
- **Weak Evidence (30-50% probability)**: Limited or conflicting signals
- **Speculative (15-30% probability)**: Contrary to current indicators but possible

Probabilities should reflect:
- Consistency of sector rotation signals
- Breadth of performance patterns
- Alignment with economic indicators
- Historical precedent strength


---

## SKILL: sector-analyst

- Fuente: `tradermonty/claude-trading-skills` → `skills/sector-analyst` (MIT)
- Cuándo usarla: This skill should be used when analyzing sector rotation patterns and market cycle positioning. It fetches sector uptrend data from CSV (no API key required) and optionally accepts chart images for supplementary analysis. Use this skill when the user requests sector rotation analysis, cyclical vs defensive assessment, overbought/oversold identification, or market cycle phase estimation. All analysis and output are conducted in English.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/sector-analyst/` (requirements.txt, analyze_sector_rotation.py)

# Sector Analyst

## Overview

This skill enables comprehensive analysis of sector rotation and market cycle positioning by fetching uptrend ratio data from TraderMonty's public CSV dataset. It ranks sectors, calculates cyclical vs defensive risk regime scores, identifies overbought/oversold conditions, and estimates the current market cycle phase. Chart images can optionally supplement the data-driven analysis with industry-level detail.

## When to Use This Skill

Use this skill when:
- User requests sector rotation analysis (no chart images required)
- User asks about cyclical vs defensive positioning
- User wants to know which sectors are overbought or oversold
- User requests market cycle phase estimation
- User provides sector performance charts for supplementary analysis
- User asks for sector-based scenario analysis or predictions

Example user requests:
- "Run a sector rotation analysis"
- "Which sectors are leading — cyclical or defensive?"
- "Are any sectors overbought right now?"
- "What phase of the market cycle are we in?"
- "Analyze these sector performance charts and tell me where we are in the market cycle"

## Prerequisites

- **Python 3.9+**; no third-party libraries required (CSV fetched via stdlib `urllib`)
- **No API keys required** — data is fetched from a public GitHub repository
- **Optional**: Sector performance chart images for supplementary analysis

## Data Source

Sector uptrend ratios are fetched from TraderMonty's public GitHub repository (no API key required):
- **Sector Summary**: `sector_summary.csv` — uptrend ratio, trend, slope, and status per sector
- **Freshness Check**: `uptrend_ratio_timeseries.csv` — max(date) used to verify data recency

## Running the Script

```bash
# Default: fetch CSV, print human-readable analysis
python3 scripts/analyze_sector_rotation.py

# JSON output
python3 scripts/analyze_sector_rotation.py --json

# Save to file
python3 scripts/analyze_sector_rotation.py --save --output-dir reports/
```

## Analysis Workflow

Follow this structured workflow:

### Step 1: CSV Data Collection

1. Run the analysis script: `python3 scripts/analyze_sector_rotation.py`
2. Extract from the output:
   - Sector ranking by uptrend ratio
   - Risk regime (cyclical vs defensive) and score
   - Overbought/oversold sectors
   - Cycle phase estimate and confidence level
3. If a data freshness warning appears, note it in the analysis

### Step 2: Market Cycle Assessment

Use the script's cycle phase estimate as a starting point:
- Read `references/sector_rotation.md` to access market cycle and sector rotation frameworks
- Compare the script's quantitative findings against expected patterns for each cycle phase:
  - Early Cycle Recovery
  - Mid Cycle Expansion
  - Late Cycle
  - Recession
- Add qualitative interpretation informed by the knowledge base

If chart images are provided, use them to supplement with industry-level detail:
- Extract industry-level performance data from chart images
- Compare 1-week vs 1-month performance for trend consistency
- Note specific industries showing strength or weakness within sectors

### Step 3: Current Situation Analysis

Synthesize observations into an objective assessment:
- State which market cycle phase current performance most closely resembles
- Highlight supporting evidence (which sectors/industries confirm this view)
- Note any contradictory signals or unusual patterns
- Assess confidence level based on consistency of signals

Use data-driven language and specific references to performance figures.

### Step 4: Scenario Development

Based on sector rotation principles and current positioning, develop 2-4 potential scenarios for the next phase:

For each scenario:
- Describe the market cycle transition
- Identify which sectors would likely outperform
- Identify which sectors would likely underperform
- Specify the catalysts or conditions that would confirm this scenario
- Assign a probability (see Probability Assessment Framework in sector_rotation.md)

Scenarios should range from most likely (highest probability) to alternative/contrarian scenarios.

### Step 5: Output Generation

Create a structured Markdown document with the following sections:

**Required Sections:**
1. **Executive Summary**: 2-3 sentence overview of key findings
2. **Current Situation**: Detailed analysis of current performance patterns and market cycle positioning
3. **Supporting Evidence**: Specific sector and industry performance data supporting the cycle assessment
4. **Scenario Analysis**: 2-4 scenarios with descriptions and probability assignments
5. **Recommended Positioning**: Strategic and tactical positioning recommendations based on scenario probabilities
6. **Key Risks**: Notable risks or contradictory signals to monitor

## Output Format

Save analysis results as a Markdown file with naming convention: `sector_analysis_YYYY-MM-DD.md`

Use this structure:

```markdown
# Sector Performance Analysis - [Date]

## Executive Summary

[2-3 sentences summarizing key findings]

## Current Situation

### Market Cycle Assessment
[Which cycle phase and why]

### Performance Patterns Observed

#### 1-Week Performance
[Analysis of recent performance]

#### 1-Month Performance
[Analysis of medium-term trends]

#### Sector-Level Analysis
[Detailed breakdown by sector]

#### Industry-Level Analysis
[Notable industry-specific observations]

## Supporting Evidence

### Confirming Signals
- [List data points supporting cycle assessment]

### Contradictory Signals
- [List any conflicting indicators]

## Scenario Analysis

### Scenario 1: [Name] (Probability: XX%)
**Description**: [What happens]
**Outperformers**: [Sectors/industries]
**Underperformers**: [Sectors/industries]
**Catalysts**: [What would confirm this scenario]

### Scenario 2: [Name] (Probability: XX%)
[Repeat structure]

[Additional scenarios as appropriate]

## Recommended Positioning

### Strategic Positioning (Medium-term)
[Sector allocation recommendations]

### Tactical Positioning (Short-term)
[Specific adjustments or opportunities]

## Key Risks and Monitoring Points

[What to watch that could invalidate the analysis]

---
*Analysis Date: [Date]*
*Data Period: [Timeframe of charts analyzed]*
```

## Key Analysis Principles

When conducting analysis:

1. **Objectivity First**: Let the data guide conclusions, not preconceptions
2. **Probabilistic Thinking**: Express uncertainty through probability ranges
3. **Multiple Timeframes**: Compare 1-week and 1-month data for trend confirmation
4. **Relative Performance**: Focus on relative strength, not absolute returns
5. **Breadth Matters**: Broad-based moves are more significant than isolated movements
6. **No Absolutes**: Markets rarely follow textbook patterns exactly
7. **Historical Context**: Reference typical rotation patterns but acknowledge uniqueness

## Probability Guidelines

Apply these probability ranges based on evidence strength:

- **70-85%**: Strong evidence with multiple confirming signals across sectors and timeframes
- **50-70%**: Moderate evidence with some confirming signals but mixed indicators
- **30-50%**: Weak evidence with limited or conflicting signals
- **15-30%**: Speculative scenario contrary to current indicators but possible

Total probabilities across all scenarios should sum to approximately 100%.

## Resources

### scripts/
- `analyze_sector_rotation.py` - Fetches sector CSV data and produces sector rankings, risk regime scoring, overbought/oversold flags, and cycle phase estimation. No API key required.

### references/
- `sector_rotation.md` - Comprehensive knowledge base covering market cycle phases, typical sector performance patterns, and probability assessment frameworks

### assets/
Sample charts demonstrating the expected input format for optional image-based analysis:
- `sector_performance.jpeg` - Example sector-level performance chart (1-week and 1-month)
- `industory_performance_1.jpeg` - Example industry performance chart (outperformers)
- `industory_performance_2.jpeg` - Example industry performance chart (underperformers)

## Important Notes

- All analysis thinking should be conducted in English
- Output Markdown files must be in English
- Reference the sector rotation knowledge base for each analysis
- Maintain objectivity and avoid confirmation bias
- Update probability assessments if new data becomes available
- Chart images are optional; CSV data provides the primary analysis input
- The script uses the same sector classification as uptrend-analyzer for consistency

### Referencia: references/sector_rotation.md

# Sector Rotation Knowledge Base

## Market Cycle Framework

The economic cycle can be divided into four primary phases, each characterized by distinct economic conditions and sector performance patterns.

### 1. Early Cycle Recovery

**Economic Characteristics:**
- Economy begins recovering from recession
- GDP growth accelerates from negative/low to positive
- Interest rates remain low
- Central banks maintain accommodative policy
- Credit conditions begin to ease
- Consumer and business confidence starts improving

**Outperforming Sectors:**
- **Technology**: Benefits from improving economic outlook and investment spending
- **Consumer Cyclical/Discretionary**: Rebounds as consumer confidence returns
- **Industrials**: Early beneficiary of economic recovery and capital spending
- **Financials**: Benefits from steepening yield curve and improving credit conditions
- **Real Estate**: Low interest rates support property valuations

**Underperforming Sectors:**
- **Utilities**: Low growth characteristics become less attractive
- **Consumer Defensive/Staples**: Defensive qualities less valued in recovery
- **Healthcare**: Stable growth profile less appealing in early recovery

### 2. Mid Cycle Expansion

**Economic Characteristics:**
- Strong GDP growth continues
- Corporate earnings growth robust
- Employment gains accelerating
- Interest rates begin rising from lows
- Credit spreads narrow
- Inflation remains moderate

**Outperforming Sectors:**
- **Technology**: Continued strong earnings growth
- **Industrials**: Peak capital spending and economic activity
- **Consumer Discretionary**: Strong consumer spending continues
- **Materials**: Strong demand from construction and manufacturing
- **Energy**: Rising economic activity drives energy demand

**Underperforming Sectors:**
- **Utilities**: Rising rates pressure valuations
- **Consumer Staples**: Growth acceleration favors cyclical exposure
- **Telecommunications**: Low growth profile less attractive

### 3. Late Cycle

**Economic Characteristics:**
- GDP growth begins decelerating but remains positive
- Interest rates peak or plateau at higher levels
- Inflation pressures build
- Labor markets tight, wage pressures increase
- Credit conditions begin tightening
- Economic indicators show signs of slowing

**Outperforming Sectors:**
- **Energy**: Benefits from inflation and commodity price strength
- **Materials**: Inflation hedge characteristics
- **Financials**: Higher interest rates support net interest margins
- **Healthcare**: Defensive qualities become attractive as growth slows
- **Consumer Staples**: Defensive positioning as uncertainty rises

**Underperforming Sectors:**
- **Technology**: High valuations pressured by rising rates
- **Consumer Discretionary**: Weakening consumer confidence
- **Real Estate**: High interest rates pressure valuations
- **Industrials**: Capital spending begins to slow

### 4. Recession

**Economic Characteristics:**
- GDP contracts (negative growth)
- Rising unemployment
- Interest rates cut by central banks
- Credit spreads widen significantly
- Corporate earnings decline
- Consumer and business confidence deteriorate

**Outperforming Sectors:**
- **Utilities**: Defensive, stable cash flows attractive
- **Consumer Staples**: Essential goods demand remains stable
- **Healthcare**: Non-discretionary spending, defensive characteristics
- **Telecommunications/Communication Services**: Stable revenue streams

**Underperforming Sectors:**
- **Financials**: Credit losses and economic stress
- **Consumer Discretionary**: Discretionary spending cuts
- **Industrials**: Sharp decline in capital spending
- **Materials**: Demand destruction
- **Energy**: Economic weakness reduces demand
- **Real Estate**: Economic stress and potential defaults

## Sector Characteristics Summary

### Cyclical Sectors (Outperform in Early/Mid Cycle)
- Technology
- Consumer Discretionary
- Industrials
- Materials
- Financials (with varying timing)
- Energy (stronger in Mid/Late Cycle)

### Defensive Sectors (Outperform in Late Cycle/Recession)
- Utilities
- Consumer Staples
- Healthcare
- Communication Services

### Interest Rate Sensitive Sectors
- **Benefit from Rising Rates**: Financials (banks)
- **Hurt by Rising Rates**: Utilities, Real Estate, Technology (high growth)

## Industry-Level Nuances

Within each sector, industry-level performance can vary:

### Technology Sector
- **Early/Mid Cycle Leaders**: Software, Semiconductors, Hardware
- **Late Cycle/Defensive**: IT Services, Enterprise Software (recurring revenue models)

### Consumer Discretionary
- **Early/Mid Cycle Leaders**: Auto Manufacturers, Homebuilders, Retail, Leisure
- **More Resilient**: Education, Entertainment (streaming)

### Financials
- **Early Cycle**: Diversified Banks, Investment Banks
- **Mid/Late Cycle**: Insurance, Asset Managers
- **Recession Vulnerable**: Regional Banks, Consumer Finance

### Industrials
- **Early/Mid Cycle**: Construction, Machinery, Transportation
- **More Defensive**: Aerospace & Defense, Waste Management

### Healthcare
- **Cyclical Elements**: Elective procedures, Medical Devices
- **Defensive Elements**: Pharmaceuticals, Healthcare Plans, Hospitals

### Materials
- **Early/Mid Cycle**: Construction Materials, Chemicals
- **Late Cycle/Inflation Hedge**: Precious Metals (Gold, Silver)

## Key Analysis Principles

1. **No Cycle is Identical**: While patterns repeat, timing and magnitude vary
2. **Multiple Indicators**: Combine sector performance with economic indicators
3. **Rotation is Gradual**: Transitions between cycles occur over months, not days
4. **Relative Performance**: Focus on relative strength vs absolute returns
5. **Leading vs Lagging**: Some sectors lead cycle transitions, others lag
6. **Global Factors**: International economic conditions affect sector performance
7. **Policy Impact**: Central bank and fiscal policy can accelerate or delay rotations

## Probability Assessment Framework

When assessing future scenarios, consider:

- **Strong Evidence (70-85% probability)**: Multiple confirming indicators across sectors
- **Moderate Evidence (50-70% probability)**: Some confirming signals but mixed data
- **Weak Evidence (30-50% probability)**: Limited or conflicting signals
- **Speculative (15-30% probability)**: Contrary to current indicators but possible

Probabilities should reflect:
- Consistency of sector rotation signals
- Breadth of performance patterns
- Alignment with economic indicators
- Historical precedent strength


---

## SKILL: sensitivity-and-scenarios

- Fuente: `SYasJ/claude-business-skills` → `plugins/finance/skills/sensitivity-and-scenarios` (MIT)
- Cuándo usarla: Show how a model moves when a few inputs move, without pretending the spreadsheet is a crystal ball. Use when the user mentions sensitivity analysis, what if this input changes, tornado chart, scenario versus sensitivity, or asks for a sensitivity note. Finance skill by Yasir Jilani.

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'sensitivity-and-scenarios' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Sensitivity and Scenarios

Show how a model moves when a few inputs move, without pretending the spreadsheet is a crystal ball.

## When to use this skill

Use this skill when the user:

- sensitivity analysis
- what if this input changes
- tornado chart
- scenario versus sensitivity

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

- The model outcome that matters
- The inputs the user can actually vary
- A base case from their numbers
- The range they consider plausible

## Workflow


### 1. Pick the outcome

Cash, margin, or runway. One outcome per pass.
### 2. Vary one input at a time first

That is a sensitivity. Combinations are scenarios and should be named, not hidden in a data table.
### 3. Use their ranges

Do not widen a range to make a picture look dramatic.
### 4. Rank the drivers

Which input moves the outcome most across the stated range.
### 5. Tell them what not to precise

If the top driver is a guess, more decimal places will not help.
### 6. Recommend a measurement

The useful next step is often to learn the top driver, not to add more tabs.

## Output

Deliver a **sensitivity note**.

- Purpose of this sensitivity note, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a sensitivity note by 30 September 2026. A launch model depends on conversion and fulfillment cost, and the team is arguing about formatting rather than drivers.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A launch model depends on conversion and fulfillment cost, and the team is arguing about formatting rather than drivers.

The model outcome that matters: A launch model depends on conversion and fulfillment cost, and the team is arguing about formatting rather than drivers. Stated once, in the ask. Not written down anywhere else
The inputs the user can actually vary: Operating cash, recorded 14 September 2026. No supporting file attached
A base case from their numbers: Harbor & Co receipt and one other, both unconfirmed as of 14 September 2026
The range they consider plausible: Operating cash, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Sensitivity note**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A one-way sensitivity on the user's ranges, the dominant driver, and a recommendation to measure that driver before adding detail.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The model outcome that matters | A launch model depends on conversion and fulfillment cost, and the team is arguing about formatting rather than drivers. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| The inputs the user can actually vary | Operating cash, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| A base case from their numbers | Harbor & Co receipt and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| The range they consider plausible | Operating cash, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Pick the outcome**  
Cash, margin, or runway. One outcome per pass.

**2. Vary one input at a time first**  
That is a sensitivity. Combinations are scenarios and should be named, not hidden in a data table.

**3. Use their ranges**  
Do not widen a range to make a picture look dramatic.

**4. Rank the drivers**  
Which input moves the outcome most across the stated range.

**5. Tell them what not to precise**  
If the top driver is a guess, more decimal places will not help.

**Deliberately not done**
- A tornado built from invented ranges.
- Calling a one-way table a scenario plan.
- False precision.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A tornado built from invented ranges.
- Calling a one-way table a scenario plan.
- False precision.

## Related skills

- `scenario-planning`
- `forecast-accuracy`
- `three-statement-model`


---

## SKILL: swap-curve-strategy

- Fuente: `anthropics/financial-services` → `plugins/partner-built/lseg/skills/swap-curve-strategy` (Apache-2.0)
- Cuándo usarla: Analyze the interest rate swap curve by pricing swaps at multiple tenors, overlaying government and inflation curves, and identifying curve trade opportunities. Use when analyzing swap curves, computing swap spreads, decomposing real rates, identifying steepener/flattener/butterfly trades, or comparing swap rates across currencies.

# Swap Curve Strategy Analysis

You are an expert rates strategist specializing in swap curve analysis. Combine swap pricing, government yield curves, and inflation curves from MCP tools to analyze curve shape, compute swap spreads, decompose real rates, and identify curve trade opportunities. Focus on routing tool outputs into curve metrics and trade recommendations — let the tools price, you analyze the shape and recommend.

## Core Principles

The swap curve prices the market's expectation of future short-term rates, credit conditions, and funding costs. Always build the full swap curve first, overlay the government curve to compute swap spreads, then add inflation breakevens for real rate decomposition. Curve metrics (2s10s slope, 5s30s slope, butterfly) and their historical context drive trade ideas. For trade recommendations, always include DV01-neutral sizing and carry/roll-down estimates.

## Available MCP Tools

- **`ir_swap`** — Swap pricing. Two-phase: list templates (by currency/index) then price at specific tenors. Returns par swap rate, DV01, NPV.
- **`interest_rate_curve`** — Government yield curves. Two-phase: list then calculate. Use for swap spread computation and curve shape context.
- **`inflation_curve`** — Inflation breakeven curves. Two-phase: search then calculate. Use for real rate decomposition.
- **`tscc_historical_pricing_summaries`** — Historical pricing data. Use for historical curve slope context and trend analysis.
- **`qa_macroeconomic`** — Macro data. Use to establish economic context for curve analysis and assess consistency with curve signals.

## Tool Chaining Workflow

1. **Discover Swap Templates:** Call `ir_swap` in list mode for the target currency. Identify available indices and tenors.
2. **Build Swap Curve:** Call `ir_swap` in price mode for standard tenors (2Y, 5Y, 7Y, 10Y, 20Y, 30Y). Extract par swap rate and DV01 at each point.
3. **Overlay Government Curve:** Call `interest_rate_curve` (list then calculate) for the same currency. Compute swap spread = swap rate minus government yield at each tenor.
4. **Inflation Decomposition:** Call `inflation_curve` (search then calculate). Compute real rate = nominal swap rate minus inflation breakeven at each tenor.
5. **Compute Curve Metrics:** From the swap curve: 2s10s slope, 5s30s slope, 2s5s10s butterfly. Note curve shape classification.
6. **Synthesize:** Combine into a complete analysis with swap curve table, swap spreads, real rate decomposition, curve metrics, and trade recommendations with DV01-neutral sizing.

## Output Format

### Swap Curve Table
| Tenor | Swap Rate (%) | Govt Yield (%) | Swap Spread (bp) | DV01 | Inflation BE (%) | Real Rate (%) |
|-------|-------------|----------------|-------------------|------|-------------------|---------------|
| 2Y | ... | ... | ... | ... | ... | ... |
| 5Y | ... | ... | ... | ... | ... | ... |
| 10Y | ... | ... | ... | ... | ... | ... |
| 30Y | ... | ... | ... | ... | ... | ... |

### Curve Metrics
| Metric | Current |
|--------|---------|
| 2s10s slope (bp) | ... |
| 5s30s slope (bp) | ... |
| 2s5s10s butterfly (bp) | ... |
| Curve shape | Normal / Flat / Inverted / Humped |

### Real Rate Decomposition
| Tenor | Nominal Swap | Inflation BE | Real Rate | Signal |
|-------|-------------|-------------|-----------|--------|
| 2Y | ...% | ...% | ...% | Accommodative/Restrictive |
| 5Y | ...% | ...% | ...% | Accommodative/Restrictive |
| 10Y | ...% | ...% | ...% | Accommodative/Restrictive |

### Curve Trade Recommendation
For each trade: structure (e.g., 2s10s steepener), legs, DV01-neutral notionals, estimated 3M carry, estimated 3M roll-down, breakeven curve move, target, stop-loss, and thesis (1-2 sentences).


---

## SKILL: tax-calendar

- Fuente: `SYasJ/claude-business-skills` → `plugins/accounting/skills/tax-calendar` (MIT)
- Cuándo usarla: Build an internal calendar of tax and filing dates the user already knows they must meet, with owners. Not tax advice. Use when the user mentions tax calendar, filing calendar, compliance dates, when are filings due, or asks for a internal tax calendar. Accounting skill by Yasir Jilani.

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'tax-calendar' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Tax Calendar

Build an internal calendar of tax and filing dates the user already knows they must meet, with owners. Not tax advice.

## When to use this skill

Use this skill when the user:

- tax calendar
- filing calendar
- compliance dates
- when are filings due

## When not to use this skill

- Tax advice or invented statutory deadlines

## Professional boundary

This is not an audit opinion, compilation, or tax advice. Do not invent accounting standards. Use the policy, framework, and chart of accounts the organization actually follows.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Jurisdictions they operate in, as they list them
- Filings they already know about
- Owners
- Last year's late items

## Workflow


### 1. Use their list

Record filings they know they have. Do not invent a filing obligation or a statutory deadline from memory.
### 2. Ask them to confirm dates

Where a date is uncertain, mark it unconfirmed rather than filling in a confident wrong day.
### 3. Add preparation lead time

The internal due date is earlier than the external date so review can happen.
### 4. Owner and reviewer

One prepares, another reviews. A calendar with no names will slip.
### 5. Evidence

What is saved when a filing is submitted. No credentials in the calendar.
### 6. Hand off advice

Unusual positions, nexus questions, and interpretations go to their tax advisor. Say that explicitly.

## Output

Deliver a **internal tax calendar**.

- Purpose of this internal tax calendar, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs an internal tax calendar by 30 September 2026. A company added a second state and the controller wants a calendar, but is unsure which filings apply.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A company added a second state and the controller wants a calendar, but is unsure which filings apply.

Jurisdictions they operate in, as they list them: Operating cash; Undeposited funds; Sales tax payable
Filings they already know about: Undeposited funds. Partly documented: the what is written down, the who is not
Owners: Priya Shah, controller
Last year's late items: Sales tax payable, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Internal tax calendar**
Northline Studio · 14 September 2026 · Due 30 September 2026

**Decision**
A calendar of known filings, unconfirmed items marked as such, internal lead times, and a clear handoff to their tax advisor for the new state.

**Checklist**

- [x] **Jurisdictions they operate in, as they list them** — Operating cash; Undeposited funds; Sales tax payable  
      Evidenced in the file
- [x] **Filings they already know about** — Undeposited funds. Partly documented: the what is written down, the who is not  
      Evidenced in the file
- [x] **Owners** — Priya Shah, controller  
      Evidenced in the file
- [ ] **Last year's late items** — Sales tax payable, last reviewed 14 September 2026. No owner named since  
      Open — nothing in the file closes this

**The gates this list enforces, in order**

1. Use their list
2. Ask them to confirm dates
3. Add preparation lead time
4. Owner and reviewer
5. Evidence

**Deliberately not done**
- Inventing deadlines.
- Giving a tax opinion.
- Storing portal passwords in the calendar.

**Stop rule**
Do not mark this pack complete while a box above is open. An open box is a finding, not a formality — it is the thing this checklist exists to catch.

Next: Priya Shah closes the open items before 30 September 2026.

## Anti-patterns

- Inventing deadlines.
- Giving a tax opinion.
- Storing portal passwords in the calendar.

## Related skills

- `compliance-calendar`
- `payroll-accounting-review`
- `audit-prep-pbc`


---

## SKILL: theme-detector

- Fuente: `tradermonty/claude-trading-skills` → `skills/theme-detector` (MIT)
- Cuándo usarla: Detect and analyze trending market themes across sectors. Use when user asks about current market themes, trending sectors, sector rotation, thematic investing, what themes are hot or cold, or wants to identify bullish and bearish market narratives with lifecycle analysis.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/theme-detector/` (requirements.txt, _market_calendar.py, __init__.py, heat_calculator.py, industry_ranker.py, lifecycle_calculator.py, theme_classifier.py, theme_discoverer.py, config_loader.py, default_theme_config.py, etf_scanner.py, finviz_performance_client.py …)

# Theme Detector

## Overview

This skill detects and ranks trending market themes by analyzing cross-sector momentum, volume, and breadth signals. It identifies both bullish (upward momentum) and bearish (downward pressure) themes, assesses lifecycle maturity (Emerging/Accelerating/Trending/Mature/Exhausting), and provides a confidence score combining quantitative data with narrative analysis.

**3-Dimensional Scoring Model:**
1. **Theme Heat** (0-100): Direction-neutral strength of the theme (momentum, volume, uptrend ratio, breadth)
2. **Lifecycle Maturity**: Stage classification (Emerging / Accelerating / Trending / Mature / Exhausting) based on duration, extremity clustering, valuation, and ETF proliferation
3. **Confidence** (Low / Medium / High): Reliability of the detection, combining quantitative breadth with narrative confirmation. Script output is capped at Medium; Claude's WebSearch narrative confirmation step can elevate to High.
4. **Stock Leadership**: Optional daily scan-hit evidence from 5D+20%, EP9M, range expansion, new highs, and high-RS stocks. When supplied, this is blended into Theme Heat v2; when absent, it lowers confidence coverage but does not force leadership to zero.
5. **Theme Match Quality**: Specificity of the theme match from industry participation, explicit stock-basket hits, proxy ETF confirmation, and optional offline narrative scores. This is evidence quality, not a trade recommendation.

**Key Features:**
- Cross-sector theme detection using FINVIZ industry data
- Direction-aware scoring (bullish and bearish themes)
- Lifecycle maturity assessment to identify crowded vs. emerging trades
- ETF proliferation scoring (more ETFs = more mature/crowded theme)
- Integration with uptrend-dashboard for 3-point evaluation
- Stock-level leadership evidence via `--scan-hits`
- Theme match quality via explicit stock baskets and proxy ETF confirmation
- Leader candidate evidence ranked by abnormal move/volume/range/RS metrics, with market cap shown only as a risk bucket
- Theme history and acceleration metrics via `--history-file`
- Dual-mode operation: FINVIZ Elite (fast) or public scraping (slower, limited)
- WebSearch-based narrative confirmation for top themes

---

## When to Use This Skill

**Explicit Triggers:**
- "What market themes are trending right now?"
- "Which sectors are hot/cold?"
- "Detect current market themes"
- "What are the strongest bullish/bearish narratives?"
- "Is AI/clean energy/defense still a strong theme?"
- "Where is sector rotation heading?"
- "Show me thematic investing opportunities"

**Implicit Triggers:**
- User wants to understand broad market narrative shifts
- User is looking for thematic ETF or sector allocation ideas
- User asks about crowded trades or late-cycle themes
- User wants to know which themes are emerging vs. exhausted

**When NOT to Use:**
- Individual stock analysis (use us-stock-analysis instead)
- Specific sector deep-dive with chart reading (use sector-analyst instead)
- Portfolio rebalancing (use portfolio-manager instead)
- Dividend/income investing (use value-dividend-screener instead)

---

## Prerequisites

**Required:**
- Python 3.9+ with core dependencies.
  ```bash
  pip install -r skills/theme-detector/requirements.txt
  ```

**Cron / mixed-Python fallback:** If the active `python3` is older than 3.10, or a newer Hermes venv lacks the data-science dependencies, run the detector through `uv` with an explicit modern interpreter and temporary dependencies instead of editing the environment mid-cron:
```bash
uv run --python 3.12 \
  --with requests --with beautifulsoup4 --with lxml \
  --with pandas --with numpy --with yfinance \
  --with finvizfinance --with PyYAML \
  python skills/theme-detector/scripts/theme_detector.py \
  --finviz-api-key "$FINVIZ_API_KEY" \
  --fmp-api-key "$FMP_API_KEY" \
  --output-dir reports/
```
Use this as a setup workaround, not as evidence that the detector is broken; still report FINVIZ/FMP/API-data caveats separately.

**Optional API Keys:**

FINVIZ Elite (recommended for full industry coverage and speed):
```bash
export FINVIZ_API_KEY=your_finviz_elite_api_key_here
```

FMP API (optional, for P/E ratio valuation data):
```bash
export FMP_API_KEY=your_fmp_api_key_here
```

The requirements include `finvizfinance`, PyYAML, pandas/numpy, requests, and
yfinance because normal public-mode execution imports or uses each of them.

Without FINVIZ Elite, the skill uses public FINVIZ scraping (limited to ~20 stocks per industry, slower rate limits).

---

## Workflow

### Step 1: Verify Environment

Check that API keys are configured (see Prerequisites):

```bash
# Verify FINVIZ Elite API key (optional but recommended)
echo $FINVIZ_API_KEY

# Verify FMP API key (optional)
echo $FMP_API_KEY
```

### Step 2: Execute Theme Detection Script

Run the main detection script:

```bash
python3 skills/theme-detector/scripts/theme_detector.py \
  --output-dir reports/
```

**Script Options:**
```bash
# Full run (public FINVIZ mode, no API key required)
python3 skills/theme-detector/scripts/theme_detector.py \
  --output-dir reports/

# With FINVIZ Elite API key
python3 skills/theme-detector/scripts/theme_detector.py \
  --finviz-api-key $FINVIZ_API_KEY \
  --output-dir reports/

# With FMP API key for enhanced stock data
python3 skills/theme-detector/scripts/theme_detector.py \
  --fmp-api-key $FMP_API_KEY \
  --output-dir reports/

# Custom limits
python3 skills/theme-detector/scripts/theme_detector.py \
  --max-themes 5 \
  --max-stocks-per-theme 10 \
  --output-dir reports/

# Explicit FINVIZ mode
python3 skills/theme-detector/scripts/theme_detector.py \
  --finviz-mode public \
  --output-dir reports/

# Add Stockbee/Pradeep-style leadership evidence
python3 skills/theme-detector/scripts/theme_detector.py \
  --scan-hits data/theme_scan_hits_YYYY-MM-DD.json \
  --narrative-scores data/theme_narrative_scores_YYYY-MM-DD.json \
  --history-file reports/theme_detector_history.json \
  --as-of-date YYYY-MM-DD \
  --output-dir reports/
```

**Scan-hit input contract:** `--scan-hits` accepts JSON, JSONL, or CSV. Rows may be pre-labeled with `scan_type` / `scan_types`, or raw rows with fields such as `symbol`, `return_5d`, `change_pct`, `volume`, `avg_volume_50d`, `relative_volume`, `true_range`, `atr_20`, `atr_expansion`, `close_location`, `industry`, `sector`, and `theme_guess`. A raw row can expand into multiple hits when it satisfies multiple rules.

Initial scan rules:
- `five_day_20pct`: `return_5d >= 20`
- `ep9m`: `volume >= 9,000,000`, `relative_volume >= 2.0`, and `change_pct >= 4`
- `range_expansion`: `change_pct >= 4`, `true_range / atr_20 >= 1.5` or `atr_expansion >= 1.5`, and `close_location >= 0.75`
- `new_high`: explicit `new_high` / `is_new_high`, or 52-week high evidence
- `high_rs`: `rs_rating >= 90` or normalized `relative_strength >= 0.90`

**Narrative-score input contract:** `--narrative-scores` is an offline JSON input, not a live WebSearch call. It accepts either `{"Theme Name": 82}` or `{"themes": {"Theme Name": {"narrative_keyword_score": 82}}}`. Missing narrative input leaves `narrative_keyword_score` as `null` and reduces `theme_match_coverage`; it does not fail the run.

**Expected Execution Time:**
- FINVIZ Elite mode: ~2-3 minutes (14+ themes)
- Public FINVIZ mode: ~5-8 minutes (rate-limited scraping)

### Step 3: Read and Parse Detection Results

The script generates two output files:
- `theme_detector_YYYY-MM-DD_HHMMSS.json` - Structured data for programmatic use
- `theme_detector_YYYY-MM-DD_HHMMSS.md` - Human-readable report

Read the JSON output to understand quantitative results:

```bash
# Find the latest report
ls -lt reports/theme_detector_*.json | head -1

# Read the JSON output
cat reports/theme_detector_YYYY-MM-DD_HHMMSS.json
```

### Step 4: Perform Narrative Confirmation via WebSearch

For the top 5 themes (by Theme Heat score), execute WebSearch queries to confirm narrative strength:

**Search Pattern:**
```
"[theme name] stocks market [current month] [current year]"
"[theme name] sector momentum [current month] [current year]"
```

**Evaluate narrative signals:**
- **Strong narrative**: Multiple major outlets covering the theme, analyst upgrades, policy catalysts
- **Moderate narrative**: Some coverage, mixed sentiment, no clear catalyst
- **Weak narrative**: Little coverage, or predominantly contrarian/skeptical tone

Update Confidence levels based on findings:
- Quantitative High + Narrative Strong = **High** confidence
- Quantitative High + Narrative Weak = **Medium** confidence (possible momentum divergence)
- Quantitative Low + Narrative Strong = **Medium** confidence (narrative may lead price)
- Quantitative Low + Narrative Weak = **Low** confidence

### Step 5: Analyze Results and Provide Recommendations

Cross-reference detection results with knowledge bases:

**Reference Documents to Consult:**
1. `references/cross_sector_themes.md` - Theme definitions and constituent industries
2. `references/thematic_etf_catalog.md` - ETF exposure options by theme
3. `references/theme_detection_methodology.md` - Scoring model details
4. `references/finviz_industry_codes.md` - Industry classification reference

**Analysis Framework:**

For **Hot Bullish Themes** (Heat >= 70, Direction = Bullish):
- Identify lifecycle stage (Emerging = opportunity, Mature/Exhausting = caution)
- List top-performing industries within the theme
- Recommend proxy ETFs for exposure
- Flag if ETF proliferation is high (crowded trade warning)

For **Hot Bearish Themes** (Heat >= 70, Direction = Bearish):
- Identify industries under pressure
- Assess if bearish momentum is accelerating or decelerating
- Recommend hedging strategies or sectors to avoid
- Note potential mean-reversion opportunities if lifecycle is Mature/Exhausting

For **Emerging Themes** (Heat 40-69, Lifecycle = Emerging):
- These may represent early rotation signals
- Recommend monitoring with watchlist
- Identify catalyst events that could accelerate the theme

For **Exhausted Themes** (Heat >= 60, Lifecycle = Exhausting):
- Warn about crowded trade risk
- High ETF count confirms excessive retail participation
- Consider contrarian positioning or reducing exposure

### Step 6: Generate Final Report

Present the final report to the user using the report template structure:

```markdown
# Theme Detection Report
**Date:** YYYY-MM-DD
**Mode:** FINVIZ Elite / Public
**Themes Analyzed:** N
**Data Quality:** [note any limitations]

## Theme Dashboard
[Top themes table with Heat, Direction, Lifecycle, Confidence]

## What Changed Today
[Newly emerging themes, largest heat acceleration, new EP9M clusters, fading themes]

## Leadership Evidence
[5D+20%, EP9M, range expansion, new highs, high-RS counts and leader symbols]

## Bullish Themes Detail
[Detailed analysis of bullish themes sorted by Heat]

## Bearish Themes Detail
[Detailed analysis of bearish themes sorted by Heat]

## All Themes Summary
[Complete theme ranking table]

## Industry Rankings
[Top performing and worst performing industries]

## Sector Uptrend Ratios
[Sector-level aggregation if uptrend data available]

## Methodology Notes
[Brief explanation of scoring model]
```

Save the report to `reports/` directory.

---

## Output

The skill generates two output files in the `reports/` directory:

**JSON Output** (`theme_detector_YYYY-MM-DD_HHMMSS.json`):
```json
{
  "report_type": "theme_detector",
  "generated_at": "2026-04-18 10:30:00",
  "metadata": {
    "generated_at": "2026-04-18 10:30:00",
    "data_mode": "full",
    "finviz_mode": "elite",
    "fmp_available": true,
    "max_themes": 14,
    "max_stocks_per_theme": 5,
    "data_sources": {
      "finviz_industries": 152,
      "yfinance_stocks": 68,
      "etf_volume": 24
    }
  },
  "summary": {
    "total_themes": 14,
    "bullish_count": 8,
    "bearish_count": 6,
    "top_bullish": "AI & Machine Learning",
    "top_bearish": "Regional Banks"
  },
  "themes": {
    "all": [
      {
        "name": "AI & Machine Learning",
        "direction": "bullish",
        "heat": 85.3,
        "maturity": 42.1,
        "stage": "Accelerating",
        "confidence": "Medium",
        "heat_label": "Hot",
        "industries": ["Software - Infrastructure", "Semiconductors"],
        "representative_stocks": ["NVDA", "MSFT"],
        "stock_details": [{"symbol": "NVDA"}, {"symbol": "MSFT"}],
        "proxy_etfs": ["BOTZ", "ROBO"],
        "theme_match_score": 78.4,
        "theme_match_components": {
          "industry_match_score": 84.2,
          "static_stock_hit_score": 80.0,
          "proxy_etf_momentum_score": 70.0,
          "narrative_keyword_score": null
        },
        "leader_candidates": [
          {
            "symbol": "NVDA",
            "leader_score": 91.2,
            "scan_types": ["ep9m", "range_expansion"],
            "risk_bucket": "mega"
          }
        ],
        "theme_origin": "seed"
      }
    ],
    "bullish": [...],
    "bearish": [...],
    "match_ranked": [...]
  },
  "industry_rankings": {
    "top": [...],
    "bottom": [...]
  },
  "sector_uptrend": {...},
  "data_quality": {...}
}
```

**Markdown Report** (`theme_detector_YYYY-MM-DD_HHMMSS.md`):
- Theme Dashboard with sortable rankings
- Bullish/Bearish theme detail sections
- Industry performance rankings
- Sector uptrend ratio summary
- Methodology notes

**Key Output Fields (per theme):**
| Field | Description |
|-------|-------------|
| `heat` | 0-100 direction-neutral theme strength |
| `direction` | `"bullish"` (LEAD) or `"bearish"` (LAG) |
| `stage` | Emerging / Accelerating / Trending / Mature / Exhausting |
| `confidence` | Low / Medium / High (script caps at Medium; WebSearch can elevate) |
| `representative_stocks` | Top ticker symbols for the theme |
| `stock_details` | Optional stock metric objects for the selected representatives |
| `proxy_etfs` | Thematic ETF tickers (length = ETF count; higher = more crowded) |
| `theme_match_score` | 0-100 evidence-quality score from industries, stock basket hits, proxy ETF confirmation, and optional narrative input |
| `theme_match_components` | Inspectable sub-scores explaining the theme match |
| `leader_candidates` | Evidence-ranked symbols for the theme; not entry/stop/invalidation guidance |
| `fresh_leadership_symbols` | Current-run symbols with EP9M, range expansion, or new-high evidence |
| `extended_symbols` | Current-run symbols with 5D+20% evidence; used as overextension evidence only |
| `theme_origin` | `"seed"` (from YAML config) or `"discovered"` (auto-clustered) |

---

## Resources

### Scripts Directory (`scripts/`)

**Main Scripts:**
- `theme_detector.py` - Main orchestrator script
  - Coordinates industry data collection, theme classification, and scoring
  - Generates JSON + Markdown output
  - Usage: `python3 theme_detector.py [options]`

- `theme_classifier.py` - Maps industries to cross-sector themes
  - Reads theme definitions from `cross_sector_themes.md`
  - Calculates theme-level aggregated scores
  - Determines direction (bullish/bearish) from constituent industries
  - Display mapping: "bullish" → "LEAD", "bearish" → "LAG" (see report_generator.py::_direction_label())

- `finviz_industry_scanner.py` - FINVIZ industry data collection
  - Elite mode: CSV export with full stock data per industry
  - Public mode: Web scraping with rate limiting
  - Extracts: performance, volume, change%, avg volume, market cap

- `calculators/lifecycle_calculator.py` - Lifecycle maturity assessment
  - Duration scoring, extremity clustering, valuation analysis
  - ETF proliferation scoring from thematic_etf_catalog.md
  - Stage classification: Emerging / Accelerating / Trending / Mature / Exhausting

- `report_generator.py` - Report output generation
  - Markdown report from template
  - JSON structured output
  - Theme dashboard formatting

### References Directory (`references/`)

**Knowledge Bases:**
- `cross_sector_themes.md` - Theme definitions with industries, ETFs, stocks, and matching criteria
- `thematic_etf_catalog.md` - Comprehensive thematic ETF catalog with counts per theme
- `finviz_industry_codes.md` - Complete FINVIZ industry-to-filter-code mapping
- `theme_detection_methodology.md` - Technical documentation of the 3D scoring model

### Assets Directory (`assets/`)

- `report_template.md` - Markdown template for report generation with placeholder format

---

## Exchange Calendar and Replay

Install `requirements.txt` before running the detector. `--as-of-date` is a
strict `YYYY-MM-DD` ceiling used by both uptrend freshness checks and provider
history windows. Because FINVIZ, quote, profile, and uptrend inputs are live
rather than PIT snapshots, a non-current `--as-of-date` fails closed. Freshness
counts XNYS sessions and excludes future-dated source rows.

## Important Notes

### FINVIZ Mode Differences

| Feature | Elite Mode | Public Mode |
|---------|-----------|-------------|
| Industry coverage | All ~145 industries | All ~145 industries |
| Stocks per industry | Full universe | ~20 stocks (page 1) |
| Rate limiting | 0.5s between requests | 2.0s between requests |
| Data freshness | Real-time | 15-min delayed |
| API key required | Yes ($39.50/mo) | No |
| Execution time | ~2-3 minutes | ~5-8 minutes |

### Direction Detection Logic

Theme direction is determined by majority vote of constituent industries' relative rank:

1. **Industry ranking**: All ~145 industries are ranked by multi-timeframe momentum score
2. **Rank-based direction**: Industries in the top half of the ranked list are classified as "bullish"; bottom half as "bearish"
3. **Theme majority vote**: `_majority_direction()` counts bullish vs. bearish industries within each theme; the majority wins

Display mapping: "bullish" → **LEAD**, "bearish" → **LAG** (see `report_generator.py::_direction_label()`)

A LEAD theme indicates relative outperformance of its constituent industries. A LAG theme may still have positive absolute returns — it indicates relative underperformance, not a short signal.

### Known Limitations

1. **Survivorship bias**: Only analyzes currently listed stocks and ETFs
2. **Lag**: FINVIZ data may lag intraday moves by 15 minutes (public mode)
3. **Theme boundaries**: Some stocks fit multiple themes; classification uses primary industry
4. **ETF proliferation**: Catalog is static and may not capture very new ETFs
5. **Narrative scoring**: WebSearch-based and inherently subjective
6. **Public mode limitation**: ~20 stocks per industry may miss small-cap signals

### Disclaimer

**This analysis is for educational and informational purposes only.**
- Not investment advice
- Past thematic trends do not guarantee future performance
- Theme detection identifies momentum, not fundamental value
- Conduct your own research before making investment decisions

---

**Version:** 1.0
**Last Updated:** 2026-02-16
**API Requirements:** FINVIZ Elite (recommended) or public mode (free); FMP API optional
**Execution Time:** ~2-8 minutes depending on mode
**Output Formats:** JSON + Markdown
**Themes Covered:** 14+ cross-sector themes

### Referencia: assets/report_template.md

# Theme Detection Report

**Date:** {{date}}
**Mode:** {{mode}}
**Themes Analyzed:** {{themes_analyzed}}
**Industries Scanned:** {{industries_scanned}}
**Total Stocks:** {{total_stocks}}
**Uptrend Data:** {{uptrend_data_status}}
**Execution Time:** {{execution_time}}

---

## 1. Theme Dashboard

| Rank | Theme | Direction | Heat | Lifecycle | Confidence |
|------|-------|-----------|------|-----------|------------|
{{#each top_themes}}
| {{rank}} | {{name}} | {{direction_emoji}} {{direction}} | {{heat}}/100 | {{lifecycle}} | {{confidence}} |
{{/each}}

**Legend:** Direction: LEAD/LAG (Dashboard), ^/v (Summary) | Heat: 0-100 scale | Lifecycle: Emerging/Accelerating/Trending/Mature/Exhausting

---

## 2. Bullish Themes Detail

{{#each bullish_themes}}
### {{name}} - Heat: {{heat}}/100

**Direction:** Bullish ({{direction_strength}}) | **Lifecycle:** {{lifecycle}} | **Confidence:** {{confidence}}

**Heat Components:**
- Momentum: {{momentum}}/100
- Volume: {{volume}}/100
- Uptrend: {{uptrend}}/100
- Breadth: {{breadth}}/100

**Lifecycle Factors:**
- Duration: {{duration_weeks}} weeks
- Extremity clustering: {{extremity_pct}}%
- Relative P/E: {{relative_pe}}x
- ETF proliferation: {{etf_count}} ETFs (score: {{etf_score}}/100)
- Narrative: {{narrative_assessment}}

**Top Industries:**
{{#each industries}}
- {{name}}: {{change_pct}}% ({{stock_count}} stocks, uptrend {{uptrend_ratio}}%)
{{/each}}

**Top Movers:**
{{#each top_stocks}}
- {{ticker}}: {{change_pct}}% | Vol: {{relative_volume}}x
{{/each}}

**Proxy ETFs:** {{proxy_etfs}}

**Assessment:** {{assessment}}

---
{{/each}}

## 3. Bearish Themes Detail

{{#each bearish_themes}}
### {{name}} - Heat: {{heat}}/100

**Direction:** Bearish ({{direction_strength}}) | **Lifecycle:** {{lifecycle}} | **Confidence:** {{confidence}}

**Heat Components:**
- Momentum: {{momentum}}/100
- Volume: {{volume}}/100
- Downtrend: {{downtrend}}/100
- Breadth: {{breadth}}/100

**Top Declining Industries:**
{{#each industries}}
- {{name}}: {{change_pct}}% ({{stock_count}} stocks, downtrend {{downtrend_ratio}}%)
{{/each}}

**Worst Performers:**
{{#each bottom_stocks}}
- {{ticker}}: {{change_pct}}% | Vol: {{relative_volume}}x
{{/each}}

**Assessment:** {{assessment}}

---
{{/each}}

## 4. All Themes Summary

| Theme | Direction | Heat | Momentum | Volume | Uptrend | Breadth | Lifecycle | Confidence |
|-------|-----------|------|----------|--------|---------|---------|-----------|------------|
{{#each all_themes}}
| {{name}} | {{direction}} | {{heat}} | {{momentum}} | {{volume}} | {{uptrend}} | {{breadth}} | {{lifecycle}} | {{confidence}} |
{{/each}}

---

## 5. Industry Rankings

### Top 10 Industries (by performance)

| Rank | Industry | Sector | Change % | Rel. Volume | Uptrend Ratio | Theme |
|------|----------|--------|----------|-------------|---------------|-------|
{{#each top_industries}}
| {{rank}} | {{name}} | {{sector}} | {{change_pct}}% | {{rel_volume}}x | {{uptrend_ratio}}% | {{theme}} |
{{/each}}

### Bottom 10 Industries (by performance)

| Rank | Industry | Sector | Change % | Rel. Volume | Downtrend Ratio | Theme |
|------|----------|--------|----------|-------------|-----------------|-------|
{{#each bottom_industries}}
| {{rank}} | {{name}} | {{sector}} | {{change_pct}}% | {{rel_volume}}x | {{downtrend_ratio}}% | {{theme}} |
{{/each}}

---

## 6. Sector Uptrend Ratios

| Sector | Uptrend Ratio | Avg Change % | Dominant Theme | Direction |
|--------|---------------|-------------|----------------|-----------|
{{#each sectors}}
| {{name}} | {{uptrend_ratio}}% | {{avg_change_pct}}% | {{dominant_theme}} | {{direction}} |
{{/each}}

---

## 7. Methodology Notes

**Scoring Model:** 3-Dimensional (Heat x Lifecycle x Confidence)
- **Theme Heat** (0-100): Momentum (30%) + Volume (25%) + Uptrend (25%) + Breadth (20%)
- **Lifecycle**: Duration + Extremity clustering + Valuation + ETF proliferation + Narrative saturation
- **Confidence**: Quantitative breadth + Cross-sector confirmation + Narrative verification

**Data Sources:**
- FINVIZ {{mode}} (industry performance, volume, 52-week data)
{{#if uptrend_data}}
- uptrend-dashboard (3-point technical evaluation)
{{/if}}
{{#if fmp_data}}
- FMP API (P/E ratios for valuation analysis)
{{/if}}
- WebSearch (narrative confirmation for top themes)

**Limitations:**
- Theme definitions are static (predefined in cross_sector_themes.md)
- {{mode_limitation}}
- Duration tracking requires historical baseline data
- Narrative assessment is subjective

---

*Generated by Theme Detector v1.0 | {{date}} {{time}}*

### Referencia: references/cross_sector_themes.md

# Cross-Sector Theme Definitions

This reference defines market themes by their constituent FINVIZ industries, sectors, proxy ETFs, and representative stocks. The theme_classifier.py script reads these definitions to map industry-level data into theme-level aggregations.

**Usage Notes:**
- Industry names must exactly match FINVIZ industry names (see `finviz_industry_codes.md`)
- `min_matching_industries`: Design-intent minimum for each theme. In practice, theme detection uses the global `cross_sector_min_matches` setting (default: 2, configurable in themes.yaml) as the threshold. Per-theme values below are informational and not individually enforced in code
- `static_stocks`: Fallback representative stocks used when industry-level data is insufficient
- `proxy_etfs`: Used for quick volume/momentum checks and as user-facing exposure recommendations

---

## AI & Semiconductors

- **Direction bias**: Bullish (typically)
- **Industries**: Semiconductors, Software - Application, Software - Infrastructure, Information Technology Services, Electronic Components, Computer Hardware, Scientific & Technical Instruments
- **Sectors**: Technology (primary), Communication Services, Industrials
- **Proxy ETFs**: SMH, SOXX, AIQ, BOTZ, CHAT
- **Static stocks**: NVDA, AVGO, AMD, INTC, QCOM, MRVL, AMAT, LRCX, KLAC, TSM, MU, ARM, SNPS, CDNS, MCHP
- **Min matching industries**: 2

---

## Clean Energy & EV

- **Direction bias**: Bullish (typically)
- **Industries**: Solar, Utilities - Renewable, Auto Manufacturers, Auto Parts, Electrical Equipment & Parts, Specialty Chemicals
- **Sectors**: Utilities, Consumer Cyclical, Industrials, Basic Materials
- **Proxy ETFs**: ICLN, QCLN, TAN, DRIV, LIT
- **Static stocks**: ENPH, SEDG, FSLR, RUN, TSLA, RIVN, LCID, NIO, PLUG, BE, CHPT, ALB, SQM, LAC, LTHM
- **Min matching industries**: 2

---

## Cybersecurity

- **Direction bias**: Bullish (typically)
- **Industries**: Software - Infrastructure, Information Technology Services, Software - Application, Communication Equipment
- **Sectors**: Technology (primary)
- **Proxy ETFs**: CIBR, HACK, BUG
- **Static stocks**: CRWD, PANW, FTNT, ZS, NET, S, OKTA, CYBR, QLYS, RPD, TENB, VRNS, SAIL, MNDT, DDOG
- **Min matching industries**: 2

**Note:** Cybersecurity overlaps with broader software industries. Theme classification uses proxy ETF volume and static stock performance to differentiate from general software themes.

---

## Cloud Computing & SaaS

- **Direction bias**: Bullish (typically)
- **Industries**: Software - Application, Software - Infrastructure, Information Technology Services
- **Sectors**: Technology (primary), Communication Services
- **Proxy ETFs**: SKYY, WCLD, CLOU
- **Static stocks**: CRM, NOW, SNOW, DDOG, TEAM, MDB, ESTC, NET, ZS, HUBS, BILL, TTD, PLTR, DOCN, DT
- **Min matching industries**: 2

**Note:** Cloud/SaaS overlaps significantly with Cybersecurity and AI themes. When multiple themes share the same industries, proxy ETF performance differentiates them.

---

## Biotech & Genomics

- **Direction bias**: Bullish (typically, but highly volatile)
- **Industries**: Biotechnology, Drug Manufacturers - Specialty & Generic, Medical Devices, Diagnostics & Research, Drug Manufacturers - General
- **Sectors**: Healthcare (primary)
- **Proxy ETFs**: XBI, IBB, ARKG, GNOM
- **Static stocks**: AMGN, GILD, VRTX, REGN, MRNA, BIIB, ILMN, CRSP, NTLA, BEAM, EDIT, EXAS, TWST, SGEN, BMRN
- **Min matching industries**: 2

---

## Infrastructure & Construction

- **Direction bias**: Bullish (typically, policy-driven)
- **Industries**: Engineering & Construction, Building Materials, Industrial Distribution, Farm & Heavy Construction Machinery, Steel, Specialty Industrial Machinery, Railroads, Waste Management
- **Sectors**: Industrials (primary), Basic Materials
- **Proxy ETFs**: PAVE, IFRA, SIMS
- **Static stocks**: CAT, DE, VMC, MLM, URI, PWR, EME, MTZ, GVA, AECOM, STRL, GBX, NUE, CLF, RS
- **Min matching industries**: 3

---

## Gold & Precious Metals

- **Direction bias**: Bullish (typically in risk-off or inflation)
- **Industries**: Gold, Silver, Other Precious Metals & Mining
- **Sectors**: Basic Materials (primary)
- **Proxy ETFs**: GDX, GDXJ, RING, SIL
- **Static stocks**: NEM, GOLD, AEM, FNV, WPM, RGLD, KGC, AGI, AU, HMY, PAAS, CDE, HL, MAG, EQX
- **Min matching industries**: 2

---

## Oil & Gas (Energy Sector)

- **Direction bias**: Varies (cyclical)
- **Industries**: Oil & Gas E&P, Oil & Gas Equipment & Services, Oil & Gas Midstream, Oil & Gas Refining & Marketing, Oil & Gas Integrated, Oil & Gas Drilling
- **Sectors**: Energy (primary)
- **Proxy ETFs**: XLE, XOP, OIH
- **Static stocks**: XOM, CVX, COP, EOG, SLB, HAL, PXD, DVN, MPC, VLO, PSX, OXY, FANG, HES, WMB
- **Min matching industries**: 2

---

## Financial Services & Banks

- **Direction bias**: Varies (rate-sensitive)
- **Industries**: Banks - Diversified, Banks - Regional, Capital Markets, Insurance - Diversified, Insurance - Property & Casualty, Financial Data & Stock Exchanges, Credit Services, Asset Management, Insurance Brokers, Mortgage Finance
- **Sectors**: Financial Services (primary)
- **Proxy ETFs**: XLF, KBE, KRE, IAI
- **Static stocks**: JPM, BAC, WFC, GS, MS, C, SCHW, BLK, AXP, ICE, CME, MCO, SPGI, BX, KKR
- **Min matching industries**: 3

---

## Healthcare & Pharma

- **Direction bias**: Varies (defensive in downturns)
- **Industries**: Drug Manufacturers - General, Health Care Plans, Medical Care Facilities, Health Information Services, Medical Distribution, Medical Instruments & Supplies, Pharmaceutical Retailers
- **Sectors**: Healthcare (primary)
- **Proxy ETFs**: XLV, IHE, IHI
- **Static stocks**: UNH, JNJ, LLY, PFE, ABT, TMO, DHR, MDT, ISRG, SYK, BSX, EW, HCA, CVS, CI
- **Min matching industries**: 3

**Note:** Healthcare & Pharma is distinct from Biotech & Genomics. Healthcare focuses on established pharma, insurance, and medical devices; Biotech focuses on emerging drug development and genomics.

---

## Defense & Aerospace

- **Direction bias**: Bullish (typically in geopolitical tension)
- **Industries**: Aerospace & Defense, Airlines, Security & Protection Services
- **Sectors**: Industrials (primary)
- **Proxy ETFs**: ITA, PPA, ROKT, ARKX
- **Static stocks**: LMT, RTX, NOC, BA, GD, LHX, HII, TDG, HWM, AXON, LDOS, BWXT, KTOS, RKLB, SPR
- **Min matching industries**: 2

---

## Real Estate & REITs

- **Direction bias**: Varies (rate-sensitive)
- **Industries**: REIT - Residential, REIT - Industrial, REIT - Retail, REIT - Office, REIT - Healthcare Facilities, REIT - Diversified, REIT - Hotel & Motel, REIT - Specialty, Real Estate Services, Real Estate - Diversified, Real Estate - Development
- **Sectors**: Real Estate (primary)
- **Proxy ETFs**: VNQ, XLRE, IYR
- **Static stocks**: PLD, AMT, CCI, EQIX, SPG, O, WELL, DLR, PSA, VICI, EXR, AVB, ARE, MAA, IRM
- **Min matching industries**: 3

---

## Retail & Consumer

- **Direction bias**: Varies (consumer sentiment driven)
- **Industries**: Internet Retail, Specialty Retail, Apparel Retail, Home Improvement Retail, Department Stores, Discount Stores, Luxury Goods, Restaurants, Leisure, Resorts & Casinos, Gambling, Apparel Manufacturing, Footwear & Accessories
- **Sectors**: Consumer Cyclical (primary), Consumer Defensive
- **Proxy ETFs**: XLY, XRT, XLP, IBUY
- **Static stocks**: AMZN, HD, LOW, TJX, COST, WMT, TGT, NKE, SBUX, MCD, DPZ, LULU, ROST, BURL, DECK
- **Min matching industries**: 3

---

## Crypto & Blockchain

- **Direction bias**: Bullish (typically in risk-on)
- **Industries**: Capital Markets, Software - Application, Financial Data & Stock Exchanges, Information Technology Services
- **Sectors**: Financial Services, Technology
- **Proxy ETFs**: BITO, BLOK, BITQ, IBIT, DAPP
- **Static stocks**: COIN, MSTR, MARA, RIOT, CLSK, HUT, BITF, SQ, PYPL, HOOD, CIFR, IREN, HIVE, CORZ, BTBT
- **Min matching industries**: 2

**Note:** Crypto theme uses proxy ETFs and static stocks as primary signals rather than industry classification, since blockchain companies span multiple traditional industries.

---

## Nuclear Energy

- **Direction bias**: Bullish (policy-driven, AI data center demand)
- **Industries**: Uranium, Utilities - Independent Power Producers, Specialty Industrial Machinery, Electrical Equipment & Parts
- **Sectors**: Energy, Utilities, Industrials
- **Proxy ETFs**: URA, URNM, NLR, NUKZ
- **Static stocks**: CCJ, UEC, NXE, DNN, UUUU, LEU, SMR, OKLO, BWX, GEV, CEG, VST, TLN, NRG, BWXT
- **Min matching industries**: 2

---

## Uranium

- **Direction bias**: Bullish (supply deficit narrative)
- **Industries**: Uranium, Other Industrial Metals & Mining
- **Sectors**: Energy (primary), Basic Materials
- **Proxy ETFs**: URA, URNM, URNJ
- **Static stocks**: CCJ, UEC, NXE, DNN, UUUU, LEU, URG, GLATF, EU, PALAF, SRUUF, LTBR, FCUUF, AEC, WSTRF
- **Min matching industries**: 1

**Note:** Uranium is a sub-theme of Nuclear Energy but tracked separately due to its distinct commodity-driven dynamics. Requires only 1 matching industry due to narrow sector focus.

---

## Obesity & GLP-1

- **Direction bias**: Bullish (medical innovation)
- **Industries**: Drug Manufacturers - General, Drug Manufacturers - Specialty & Generic, Medical Devices, Biotechnology
- **Sectors**: Healthcare (primary)
- **Proxy ETFs**: SLIM, HRTS
- **Static stocks**: LLY, NVO, AMGN, VKTX, ALT, GPCR, SMLR, RVMD, PTGX, IVA
- **Min matching industries**: 2

**Note:** Obesity/GLP-1 is a narrow theme that overlaps with Healthcare & Pharma. It is differentiated primarily through proxy ETF volume and static stock performance rather than industry classification.

---

## Summary Table

| Theme | Industries | Sectors | Proxy ETFs | Static Stocks | Min Industries |
|-------|-----------|---------|-----------|--------------|----------------|
| AI & Semiconductors | 7 | 3 | 5 | 15 | 2 |
| Clean Energy & EV | 6 | 4 | 5 | 15 | 2 |
| Cybersecurity | 4 | 1 | 3 | 15 | 2 |
| Cloud Computing & SaaS | 3 | 2 | 3 | 15 | 2 |
| Biotech & Genomics | 5 | 1 | 4 | 15 | 2 |
| Infrastructure & Construction | 8 | 2 | 3 | 15 | 3 |
| Gold & Precious Metals | 3 | 1 | 4 | 15 | 2 |
| Oil & Gas (Energy) | 6 | 1 | 3 | 15 | 2 |
| Financial Services & Banks | 10 | 1 | 4 | 15 | 3 |
| Healthcare & Pharma | 7 | 1 | 3 | 15 | 3 |
| Defense & Aerospace | 3 | 1 | 4 | 15 | 2 |
| Real Estate & REITs | 11 | 1 | 3 | 15 | 3 |
| Retail & Consumer | 13 | 2 | 4 | 15 | 3 |
| Crypto & Blockchain | 4 | 2 | 5 | 15 | 2 |
| Nuclear Energy | 4 | 3 | 4 | 15 | 2 |
| Uranium | 2 | 2 | 3 | 15 | 1 |
| Obesity & GLP-1 | 4 | 1 | 2 | 10 | 2 |

**Total: 17 themes** covering all major market narratives.

---

## Theme Overlap Matrix

Some industries contribute to multiple themes. When scoring, each industry's data is used in all applicable themes:

| Industry | Themes |
|----------|--------|
| Software - Application | AI, Cybersecurity, Cloud, Crypto |
| Software - Infrastructure | AI, Cybersecurity, Cloud |
| Drug Manufacturers - General | Healthcare, Biotech, Obesity |
| Biotechnology | Biotech, Obesity |
| Capital Markets | Financial Services, Crypto |
| Electrical Equipment & Parts | Clean Energy, Nuclear |
| Uranium | Nuclear, Uranium |

This overlap is intentional - a strong software industry may boost multiple themes simultaneously, reflecting the interconnected nature of market narratives.

### Referencia: references/finviz_industry_codes.md

# FINVIZ Industry Filter Codes

This reference maps all FINVIZ industry names to their corresponding filter codes used in the FINVIZ Screener API and Elite CSV export URLs.

**URL Pattern (Elite CSV Export):**
```
https://elite.finviz.com/export.ashx?v=151&f=ind_{code},cap_smallover&auth={API_KEY}
```

**URL Pattern (Public Screener):**
```
https://finviz.com/screener.ashx?v=151&f=ind_{code},cap_smallover
```

**Filter Code Convention:** `ind_` + lowercase industry name with spaces, hyphens, ampersands, and special characters removed.

---

## Aerospace & Defense

| Industry Name | Filter Code |
|---|---|
| Aerospace & Defense | ind_aerospacedefense |

## Auto & Transport

| Industry Name | Filter Code |
|---|---|
| Airlines | ind_airlines |
| Auto Manufacturers | ind_automanufacturers |
| Auto Parts | ind_autoparts |
| Railroads | ind_railroads |
| Recreational Vehicles | ind_recreationalvehicles |
| Trucking | ind_trucking |
| Marine Shipping | ind_marineshipping |

## Basic Materials

| Industry Name | Filter Code |
|---|---|
| Aluminum | ind_aluminum |
| Building Materials | ind_buildingmaterials |
| Chemicals | ind_chemicals |
| Coking Coal | ind_cokingcoal |
| Copper | ind_copper |
| Gold | ind_gold |
| Lumber & Wood Production | ind_lumberwoodproduction |
| Other Industrial Metals & Mining | ind_otherindustrialmetalsmining |
| Other Precious Metals & Mining | ind_otherpreciousmetalsmining |
| Paper & Paper Products | ind_paperpaperproducts |
| Silver | ind_silver |
| Specialty Chemicals | ind_specialtychemicals |
| Steel | ind_steel |
| Uranium | ind_uranium |

## Communication Services

| Industry Name | Filter Code |
|---|---|
| Advertising Agencies | ind_advertisingagencies |
| Broadcasting | ind_broadcasting |
| Electronic Gaming & Multimedia | ind_electronicgamingmultimedia |
| Entertainment | ind_entertainment |
| Internet Content & Information | ind_internetcontentinformation |
| Publishing | ind_publishing |
| Telecom Services | ind_telecomservices |

## Consumer Cyclical

| Industry Name | Filter Code |
|---|---|
| Apparel Manufacturing | ind_apparelmanufacturing |
| Apparel Retail | ind_apparelretail |
| Auto & Truck Dealerships | ind_autotruckdealerships |
| Department Stores | ind_departmentstores |
| Discount Stores | ind_discountstores |
| Footwear & Accessories | ind_footwearaccessories |
| Furnishings, Fixtures & Appliances | ind_furnishingsfixturesappliances |
| Gambling | ind_gambling |
| Home Improvement Retail | ind_homeimprovementretail |
| Internet Retail | ind_internetretail |
| Leisure | ind_leisure |
| Lodging | ind_lodging |
| Luxury Goods | ind_luxurygoods |
| Packaging & Containers | ind_packagingcontainers |
| Personal Services | ind_personalservices |
| Residential Construction | ind_residentialconstruction |
| Resorts & Casinos | ind_resortscasinos |
| Restaurants | ind_restaurants |
| Specialty Retail | ind_specialtyretail |
| Textile Manufacturing | ind_textilemanufacturing |
| Travel Services | ind_travelservices |

## Consumer Defensive

| Industry Name | Filter Code |
|---|---|
| Beverages - Brewers | ind_beveragesbrewers |
| Beverages - Non-Alcoholic | ind_beveragesnonalcoholic |
| Beverages - Wineries & Distilleries | ind_beverageswineriesanddistilleries |
| Confectioners | ind_confectioners |
| Discount Stores | ind_discountstores |
| Education & Training Services | ind_educationtrainingservices |
| Farm Products | ind_farmproducts |
| Food Distribution | ind_fooddistribution |
| Grocery Stores | ind_grocerystores |
| Household & Personal Products | ind_householdpersonalproducts |
| Packaged Foods | ind_packagedfoods |
| Tobacco | ind_tobacco |

## Energy

| Industry Name | Filter Code |
|---|---|
| Oil & Gas Drilling | ind_oilgasdrilling |
| Oil & Gas E&P | ind_oilgasep |
| Oil & Gas Equipment & Services | ind_oilgasequipmentservices |
| Oil & Gas Integrated | ind_oilgasintegrated |
| Oil & Gas Midstream | ind_oilgasmidstream |
| Oil & Gas Refining & Marketing | ind_oilgasrefiningmarketing |
| Thermal Coal | ind_thermalcoal |
| Uranium | ind_uranium |

## Financial Services

| Industry Name | Filter Code |
|---|---|
| Asset Management | ind_assetmanagement |
| Banks - Diversified | ind_banksdiversified |
| Banks - Regional | ind_banksregional |
| Capital Markets | ind_capitalmarkets |
| Credit Services | ind_creditservices |
| Financial Conglomerates | ind_financialconglomerates |
| Financial Data & Stock Exchanges | ind_financialdatastockexchanges |
| Insurance - Diversified | ind_insurancediversified |
| Insurance - Life | ind_insurancelife |
| Insurance - Property & Casualty | ind_insurancepropertycasualty |
| Insurance - Reinsurance | ind_insurancereinsurance |
| Insurance - Specialty | ind_insurancespecialty |
| Insurance Brokers | ind_insurancebrokers |
| Mortgage Finance | ind_mortgagefinance |
| Shell Companies | ind_shellcompanies |

## Healthcare

| Industry Name | Filter Code |
|---|---|
| Biotechnology | ind_biotechnology |
| Diagnostics & Research | ind_diagnosticsresearch |
| Drug Manufacturers - General | ind_drugmanufacturersgeneral |
| Drug Manufacturers - Specialty & Generic | ind_drugmanufacturersspecialtygeneric |
| Health Information Services | ind_healthinformationservices |
| Health Care Plans | ind_healthcareplans |
| Medical Care Facilities | ind_medicalcarefacilities |
| Medical Devices | ind_medicaldevices |
| Medical Distribution | ind_medicaldistribution |
| Medical Instruments & Supplies | ind_medicalinstrumentssupplies |
| Pharmaceutical Retailers | ind_pharmaceuticalretailers |

## Industrials

| Industry Name | Filter Code |
|---|---|
| Aerospace & Defense | ind_aerospacedefense |
| Business Equipment & Supplies | ind_businessequipmentsupplies |
| Conglomerates | ind_conglomerates |
| Consulting Services | ind_consultingservices |
| Electrical Equipment & Parts | ind_electricalequipmentparts |
| Engineering & Construction | ind_engineeringconstruction |
| Farm & Heavy Construction Machinery | ind_farmheavyconstructionmachinery |
| Industrial Distribution | ind_industrialdistribution |
| Infrastructure Operations | ind_infrastructureoperations |
| Integrated Freight & Logistics | ind_integratedfreightlogistics |
| Metal Fabrication | ind_metalfabrication |
| Pollution & Treatment Controls | ind_pollutiontreatmentcontrols |
| Rental & Leasing Services | ind_rentalleasingservices |
| Security & Protection Services | ind_securityprotectionservices |
| Specialty Business Services | ind_specialtybusinessservices |
| Specialty Industrial Machinery | ind_specialtyindustrialmachinery |
| Staffing & Employment Services | ind_staffingemploymentservices |
| Tools & Accessories | ind_toolsaccessories |
| Waste Management | ind_wastemanagement |

## Real Estate

| Industry Name | Filter Code |
|---|---|
| Real Estate - Development | ind_realestatedevelopment |
| Real Estate - Diversified | ind_realestatediversified |
| Real Estate Services | ind_realestateservices |
| REIT - Diversified | ind_reitdiversified |
| REIT - Healthcare Facilities | ind_reithealthcarefacilities |
| REIT - Hotel & Motel | ind_reithotelandmotel |
| REIT - Industrial | ind_reitindustrial |
| REIT - Mortgage | ind_reitmortgage |
| REIT - Office | ind_reitoffice |
| REIT - Residential | ind_reitresidential |
| REIT - Retail | ind_reitretail |
| REIT - Specialty | ind_reitspecialty |

## Technology

| Industry Name | Filter Code |
|---|---|
| Communication Equipment | ind_communicationequipment |
| Computer Hardware | ind_computerhardware |
| Consumer Electronics | ind_consumerelectronics |
| Electronic Components | ind_electroniccomponents |
| Electronics & Computer Distribution | ind_electronicscomputerdistribution |
| Information Technology Services | ind_informationtechnologyservices |
| Scientific & Technical Instruments | ind_scientifictechnicalinstruments |
| Semiconductor Equipment & Materials | ind_semiconductorequipmentmaterials |
| Semiconductors | ind_semiconductors |
| Software - Application | ind_softwareapplication |
| Software - Infrastructure | ind_softwareinfrastructure |
| Solar | ind_solar |

## Utilities

| Industry Name | Filter Code |
|---|---|
| Utilities - Diversified | ind_utilitiesdiversified |
| Utilities - Independent Power Producers | ind_utilitiesindependentpowerproducers |
| Utilities - Regulated Electric | ind_utilitiesregulatedelectric |
| Utilities - Regulated Gas | ind_utilitiesregulatedgas |
| Utilities - Regulated Water | ind_utilitiesregulatedwater |
| Utilities - Renewable | ind_utilitiesrenewable |

---

## Complete Alphabetical Index

This flat list provides all industry filter codes in alphabetical order for quick lookup:

| # | Industry Name | Filter Code |
|---|---|---|
| 1 | Advertising Agencies | ind_advertisingagencies |
| 2 | Aerospace & Defense | ind_aerospacedefense |
| 3 | Airlines | ind_airlines |
| 4 | Aluminum | ind_aluminum |
| 5 | Apparel Manufacturing | ind_apparelmanufacturing |
| 6 | Apparel Retail | ind_apparelretail |
| 7 | Asset Management | ind_assetmanagement |
| 8 | Auto & Truck Dealerships | ind_autotruckdealerships |
| 9 | Auto Manufacturers | ind_automanufacturers |
| 10 | Auto Parts | ind_autoparts |
| 11 | Banks - Diversified | ind_banksdiversified |
| 12 | Banks - Regional | ind_banksregional |
| 13 | Beverages - Brewers | ind_beveragesbrewers |
| 14 | Beverages - Non-Alcoholic | ind_beveragesnonalcoholic |
| 15 | Beverages - Wineries & Distilleries | ind_beverageswineriesanddistilleries |
| 16 | Biotechnology | ind_biotechnology |
| 17 | Broadcasting | ind_broadcasting |
| 18 | Building Materials | ind_buildingmaterials |
| 19 | Business Equipment & Supplies | ind_businessequipmentsupplies |
| 20 | Capital Markets | ind_capitalmarkets |
| 21 | Chemicals | ind_chemicals |
| 22 | Coking Coal | ind_cokingcoal |
| 23 | Communication Equipment | ind_communicationequipment |
| 24 | Computer Hardware | ind_computerhardware |
| 25 | Confectioners | ind_confectioners |
| 26 | Conglomerates | ind_conglomerates |
| 27 | Consulting Services | ind_consultingservices |
| 28 | Consumer Electronics | ind_consumerelectronics |
| 29 | Copper | ind_copper |
| 30 | Credit Services | ind_creditservices |
| 31 | Department Stores | ind_departmentstores |
| 32 | Diagnostics & Research | ind_diagnosticsresearch |
| 33 | Discount Stores | ind_discountstores |
| 34 | Drug Manufacturers - General | ind_drugmanufacturersgeneral |
| 35 | Drug Manufacturers - Specialty & Generic | ind_drugmanufacturersspecialtygeneric |
| 36 | Education & Training Services | ind_educationtrainingservices |
| 37 | Electrical Equipment & Parts | ind_electricalequipmentparts |
| 38 | Electronic Components | ind_electroniccomponents |
| 39 | Electronic Gaming & Multimedia | ind_electronicgamingmultimedia |
| 40 | Electronics & Computer Distribution | ind_electronicscomputerdistribution |
| 41 | Engineering & Construction | ind_engineeringconstruction |
| 42 | Entertainment | ind_entertainment |
| 43 | Farm & Heavy Construction Machinery | ind_farmheavyconstructionmachinery |
| 44 | Farm Products | ind_farmproducts |
| 45 | Financial Conglomerates | ind_financialconglomerates |
| 46 | Financial Data & Stock Exchanges | ind_financialdatastockexchanges |
| 47 | Food Distribution | ind_fooddistribution |
| 48 | Footwear & Accessories | ind_footwearaccessories |
| 49 | Furnishings, Fixtures & Appliances | ind_furnishingsfixturesappliances |
| 50 | Gambling | ind_gambling |
| 51 | Gold | ind_gold |
| 52 | Grocery Stores | ind_grocerystores |
| 53 | Health Care Plans | ind_healthcareplans |
| 54 | Health Information Services | ind_healthinformationservices |
| 55 | Home Improvement Retail | ind_homeimprovementretail |
| 56 | Household & Personal Products | ind_householdpersonalproducts |
| 57 | Industrial Distribution | ind_industrialdistribution |
| 58 | Infrastructure Operations | ind_infrastructureoperations |
| 59 | Information Technology Services | ind_informationtechnologyservices |
| 60 | Insurance - Diversified | ind_insurancediversified |
| 61 | Insurance - Life | ind_insurancelife |
| 62 | Insurance - Property & Casualty | ind_insurancepropertycasualty |
| 63 | Insurance - Reinsurance | ind_insurancereinsurance |
| 64 | Insurance - Specialty | ind_insurancespecialty |
| 65 | Insurance Brokers | ind_insurancebrokers |
| 66 | Integrated Freight & Logistics | ind_integratedfreightlogistics |
| 67 | Internet Content & Information | ind_internetcontentinformation |
| 68 | Internet Retail | ind_internetretail |
| 69 | Leisure | ind_leisure |
| 70 | Lodging | ind_lodging |
| 71 | Lumber & Wood Production | ind_lumberwoodproduction |
| 72 | Luxury Goods | ind_luxurygoods |
| 73 | Marine Shipping | ind_marineshipping |
| 74 | Medical Care Facilities | ind_medicalcarefacilities |
| 75 | Medical Devices | ind_medicaldevices |
| 76 | Medical Distribution | ind_medicaldistribution |
| 77 | Medical Instruments & Supplies | ind_medicalinstrumentssupplies |
| 78 | Metal Fabrication | ind_metalfabrication |
| 79 | Mortgage Finance | ind_mortgagefinance |
| 80 | Oil & Gas Drilling | ind_oilgasdrilling |
| 81 | Oil & Gas E&P | ind_oilgasep |
| 82 | Oil & Gas Equipment & Services | ind_oilgasequipmentservices |
| 83 | Oil & Gas Integrated | ind_oilgasintegrated |
| 84 | Oil & Gas Midstream | ind_oilgasmidstream |
| 85 | Oil & Gas Refining & Marketing | ind_oilgasrefiningmarketing |
| 86 | Other Industrial Metals & Mining | ind_otherindustrialmetalsmining |
| 87 | Other Precious Metals & Mining | ind_otherpreciousmetalsmining |
| 88 | Packaged Foods | ind_packagedfoods |
| 89 | Packaging & Containers | ind_packagingcontainers |
| 90 | Paper & Paper Products | ind_paperpaperproducts |
| 91 | Personal Services | ind_personalservices |
| 92 | Pharmaceutical Retailers | ind_pharmaceuticalretailers |
| 93 | Pollution & Treatment Controls | ind_pollutiontreatmentcontrols |
| 94 | Publishing | ind_publishing |
| 95 | Railroads | ind_railroads |
| 96 | Real Estate - Development | ind_realestatedevelopment |
| 97 | Real Estate - Diversified | ind_realestatediversified |
| 98 | Real Estate Services | ind_realestateservices |
| 99 | Recreational Vehicles | ind_recreationalvehicles |
| 100 | REIT - Diversified | ind_reitdiversified |
| 101 | REIT - Healthcare Facilities | ind_reithealthcarefacilities |
| 102 | REIT - Hotel & Motel | ind_reithotelandmotel |
| 103 | REIT - Industrial | ind_reitindustrial |
| 104 | REIT - Mortgage | ind_reitmortgage |
| 105 | REIT - Office | ind_reitoffice |
| 106 | REIT - Residential | ind_reitresidential |
| 107 | REIT - Retail | ind_reitretail |
| 108 | REIT - Specialty | ind_reitspecialty |
| 109 | Rental & Leasing Services | ind_rentalleasingservices |
| 110 | Residential Construction | ind_residentialconstruction |
| 111 | Resorts & Casinos | ind_resortscasinos |
| 112 | Restaurants | ind_restaurants |
| 113 | Scientific & Technical Instruments | ind_scientifictechnicalinstruments |
| 114 | Security & Protection Services | ind_securityprotectionservices |
| 115 | Semiconductor Equipment & Materials | ind_semiconductorequipmentmaterials |
| 116 | Semiconductors | ind_semiconductors |
| 117 | Shell Companies | ind_shellcompanies |
| 118 | Silver | ind_silver |
| 119 | Software - Application | ind_softwareapplication |
| 120 | Software - Infrastructure | ind_softwareinfrastructure |
| 121 | Solar | ind_solar |
| 122 | Specialty Business Services | ind_specialtybusinessservices |
| 123 | Specialty Chemicals | ind_specialtychemicals |
| 124 | Specialty Industrial Machinery | ind_specialtyindustrialmachinery |
| 125 | Specialty Retail | ind_specialtyretail |
| 126 | Staffing & Employment Services | ind_staffingemploymentservices |
| 127 | Steel | ind_steel |
| 128 | Telecom Services | ind_telecomservices |
| 129 | Textile Manufacturing | ind_textilemanufacturing |
| 130 | Thermal Coal | ind_thermalcoal |
| 131 | Tobacco | ind_tobacco |
| 132 | Tools & Accessories | ind_toolsaccessories |
| 133 | Travel Services | ind_travelservices |
| 134 | Trucking | ind_trucking |
| 135 | Uranium | ind_uranium |
| 136 | Utilities - Diversified | ind_utilitiesdiversified |
| 137 | Utilities - Independent Power Producers | ind_utilitiesindependentpowerproducers |
| 138 | Utilities - Regulated Electric | ind_utilitiesregulatedelectric |
| 139 | Utilities - Regulated Gas | ind_utilitiesregulatedgas |
| 140 | Utilities - Regulated Water | ind_utilitiesregulatedwater |
| 141 | Utilities - Renewable | ind_utilitiesrenewable |
| 142 | Waste Management | ind_wastemanagement |

**Total: 142 industries**

---

## Notes

1. **Filter code derivation**: Remove spaces, hyphens, ampersands (`&`), and other special characters from the industry name, then lowercase the result. Prefix with `ind_`.

2. **Cross-sector industries**: Some industries (e.g., Uranium) appear under multiple FINVIZ sectors (Energy and Basic Materials). The filter code is the same regardless of which sector view you navigate from.

3. **Industry changes**: FINVIZ occasionally adds, removes, or renames industries. This list was compiled as of February 2026. If a filter code returns no results, verify the industry name on FINVIZ directly.

4. **Combining filters**: Multiple industry filters can be combined in FINVIZ URLs using comma separation:
   ```
   f=ind_semiconductors,ind_softwareapplication,cap_smallover
   ```

5. **Market cap filter**: For theme detection, always combine with `cap_smallover` (market cap > $300M) to filter out micro-caps that may distort aggregated metrics.

6. **Special cases**:
   - "E&P" becomes "ep" (ampersand removed)
   - "REIT - " prefix becomes "reit" (hyphen and spaces removed)
   - "Wineries & Distilleries" becomes "wineriesanddistilleries" (ampersand becomes "and" in this case)
   - Verify edge cases against FINVIZ directly if results seem incorrect

### Referencia: references/thematic_etf_catalog.md

# Thematic ETF Catalog

This catalog maps market themes to their associated ETFs. The ETF count per theme is used for the `etf_proliferation_score` in lifecycle maturity assessment.

**ETF Proliferation Scoring:**
| ETF Count | Score |
|-----------|-------|
| 0         | 0     |
| 1         | 20    |
| 2-3       | 40    |
| 4-6       | 60    |
| 7-10      | 80    |
| >10       | 100   |

Higher ETF proliferation indicates more retail/institutional interest and a potentially more mature (crowded) theme.

---

## AI & Semiconductors

**ETF Count: 11** | Proliferation Score: 100

| Ticker | Name | Focus | AUM Tier |
|--------|------|-------|----------|
| SMH    | VanEck Semiconductor ETF | Semiconductor equities | Large |
| SOXX   | iShares Semiconductor ETF | Semiconductor equities | Large |
| SOXQ   | Invesco PHLX Semiconductor ETF | Semiconductor equities | Medium |
| AIQ    | Global X Artificial Intelligence & Technology ETF | AI & big data | Medium |
| BOTZ   | Global X Robotics & Artificial Intelligence ETF | AI & robotics | Medium |
| ROBT   | First Trust Nasdaq Artificial Intelligence & Robotics ETF | AI & robotics | Small |
| IRBO   | iShares Robotics and Artificial Intelligence Multisector ETF | AI multi-sector | Small |
| CHAT   | Roundhill Generative AI & Technology ETF | Generative AI | Small |
| WTAI   | WisdomTree Artificial Intelligence and Innovation Fund | AI innovation | Small |
| IGPT   | North Shore AI Powered Large Cap Growth ETF | AI large-cap | Small |
| AIVI   | WisdomTree International AI Enhanced Value Fund | AI value | Small |

---

## Clean Energy & EV

**ETF Count: 9** | Proliferation Score: 80

| Ticker | Name | Focus | AUM Tier |
|--------|------|-------|----------|
| ICLN   | iShares Global Clean Energy ETF | Global clean energy | Large |
| QCLN   | First Trust NASDAQ Clean Edge Green Energy ETF | Clean energy technology | Medium |
| TAN    | Invesco Solar ETF | Solar energy | Medium |
| FAN    | First Trust Global Wind Energy ETF | Wind energy | Small |
| LIT    | Global X Lithium & Battery Tech ETF | Lithium & batteries | Medium |
| DRIV   | Global X Autonomous & Electric Vehicles ETF | EVs & autonomous driving | Medium |
| IDRV   | iShares Self-Driving EV and Tech ETF | EVs & self-driving tech | Small |
| ACES   | ALPS Clean Energy ETF | US clean energy | Small |
| PBW    | Invesco WilderHill Clean Energy ETF | Clean energy innovation | Small |

---

## Cybersecurity

**ETF Count: 4** | Proliferation Score: 60

| Ticker | Name | Focus | AUM Tier |
|--------|------|-------|----------|
| CIBR   | First Trust NASDAQ Cybersecurity ETF | Cybersecurity equities | Large |
| HACK   | ETFMG Prime Cyber Security ETF | Cybersecurity equities | Medium |
| BUG    | Global X Cybersecurity ETF | Cybersecurity equities | Small |
| IHAK   | iShares Cybersecurity and Tech ETF | Cybersecurity & tech | Small |

---

## Cloud Computing & SaaS

**ETF Count: 4** | Proliferation Score: 60

| Ticker | Name | Focus | AUM Tier |
|--------|------|-------|----------|
| SKYY   | First Trust Cloud Computing ETF | Cloud computing | Medium |
| WCLD   | WisdomTree Cloud Computing Fund | Cloud software | Small |
| CLOU   | Global X Cloud Computing ETF | Cloud computing | Small |
| CLDL   | Direxion Daily Cloud Computing Bull 2X Shares | Cloud computing (leveraged) | Small |

---

## Biotech & Genomics

**ETF Count: 6** | Proliferation Score: 60

| Ticker | Name | Focus | AUM Tier |
|--------|------|-------|----------|
| XBI    | SPDR S&P Biotech ETF | Biotech equities (equal-weight) | Large |
| IBB    | iShares Biotechnology ETF | Biotech equities (cap-weight) | Large |
| ARKG   | ARK Genomic Revolution ETF | Genomics & biotech | Medium |
| GNOM   | Global X Genomics & Biotechnology ETF | Genomics | Small |
| IDNA   | iShares Genomics Immunology and Healthcare ETF | Genomics & immunology | Small |
| LABU   | Direxion Daily S&P Biotech Bull 3X Shares | Biotech (leveraged) | Medium |

---

## Infrastructure & Construction

**ETF Count: 3** | Proliferation Score: 40

| Ticker | Name | Focus | AUM Tier |
|--------|------|-------|----------|
| PAVE   | Global X U.S. Infrastructure Development ETF | US infrastructure | Large |
| IFRA   | iShares U.S. Infrastructure ETF | US infrastructure equities | Medium |
| SIMS   | SPDR S&P Kensho Intelligent Structures ETF | Smart infrastructure | Small |

---

## Cannabis

**ETF Count: 3** | Proliferation Score: 40

| Ticker | Name | Focus | AUM Tier |
|--------|------|-------|----------|
| MSOS   | AdvisorShares Pure US Cannabis ETF | US cannabis operators | Medium |
| MJ     | ETFMG Alternative Harvest ETF | Global cannabis | Small |
| THCX   | The Cannabis ETF | Cannabis equities | Small |

---

## Blockchain & Crypto

**ETF Count: 5** | Proliferation Score: 60

| Ticker | Name | Focus | AUM Tier |
|--------|------|-------|----------|
| BITO   | ProShares Bitcoin Strategy ETF | Bitcoin futures | Large |
| BLOK   | Amplify Transformational Data Sharing ETF | Blockchain companies | Medium |
| BITQ   | Bitwise Crypto Industry Innovators ETF | Crypto industry equities | Small |
| DAPP   | VanEck Digital Transformation ETF | Digital assets ecosystem | Small |
| IBIT   | iShares Bitcoin Trust ETF | Spot Bitcoin | Large |

---

## Defense & Aerospace

**ETF Count: 5** | Proliferation Score: 60

| Ticker | Name | Focus | AUM Tier |
|--------|------|-------|----------|
| ITA    | iShares U.S. Aerospace & Defense ETF | Aerospace & defense equities | Large |
| PPA    | Invesco Aerospace & Defense ETF | Aerospace & defense equities | Medium |
| ROKT   | SPDR S&P Kensho Final Frontiers ETF | Space & deep sea exploration | Small |
| UFO    | Procure Space ETF | Space industry | Small |
| ARKX   | ARK Space Exploration & Innovation ETF | Space exploration & innovation | Small |

---

## Obesity & GLP-1

**ETF Count: 2** | Proliferation Score: 40

| Ticker | Name | Focus | AUM Tier |
|--------|------|-------|----------|
| SLIM   | Themes Obesity & Cardiometabolic ETF | Obesity & cardiometabolic drugs | Small |
| HRTS   | Tema Cardiovascular and Metabolic ETF | Cardiovascular & metabolic health | Small |

---

## Nuclear Energy

**ETF Count: 3** | Proliferation Score: 40

| Ticker | Name | Focus | AUM Tier |
|--------|------|-------|----------|
| NLR    | VanEck Uranium+Nuclear Energy ETF | Uranium & nuclear energy | Medium |
| NUKZ   | Range Nuclear Renaissance Index ETF | Nuclear renaissance | Small |
| NUCL   | Horizons Global Uranium Index ETF | Global uranium | Small |

---

## Water Resources

**ETF Count: 3** | Proliferation Score: 40

| Ticker | Name | Focus | AUM Tier |
|--------|------|-------|----------|
| PHO    | Invesco Water Resources ETF | Water utilities & infrastructure | Medium |
| FIW    | First Trust Water ETF | Water industry | Medium |
| CGW    | Invesco S&P Global Water Index ETF | Global water equities | Small |

---

## Robotics & Automation

**ETF Count: 3** | Proliferation Score: 40

| Ticker | Name | Focus | AUM Tier |
|--------|------|-------|----------|
| ROBO   | Robo Global Robotics and Automation Index ETF | Robotics & automation | Medium |
| ARKQ   | ARK Autonomous Technology & Robotics ETF | Autonomous tech & robotics | Medium |
| IRBO   | iShares Robotics and Artificial Intelligence Multisector ETF | Robotics & AI (also in AI theme) | Small |

---

## Lithium & Battery Technology

**ETF Count: 2** | Proliferation Score: 40

| Ticker | Name | Focus | AUM Tier |
|--------|------|-------|----------|
| LIT    | Global X Lithium & Battery Tech ETF | Lithium mining & battery tech (also in Clean Energy) | Medium |
| BATT   | Amplify Lithium & Battery Technology ETF | Battery technology value chain | Small |

---

## Gold & Precious Metals

**ETF Count: 5** | Proliferation Score: 60

| Ticker | Name | Focus | AUM Tier |
|--------|------|-------|----------|
| GDX    | VanEck Gold Miners ETF | Gold mining equities | Large |
| GDXJ   | VanEck Junior Gold Miners ETF | Junior gold miners | Large |
| RING   | iShares MSCI Global Gold Miners ETF | Global gold miners | Medium |
| SGDM   | Sprott Gold Miners ETF | Gold miners (rules-based) | Small |
| SIL    | Global X Silver Miners ETF | Silver miners | Medium |

---

## Uranium

**ETF Count: 3** | Proliferation Score: 40

| Ticker | Name | Focus | AUM Tier |
|--------|------|-------|----------|
| URA    | Global X Uranium ETF | Uranium mining & nuclear components | Medium |
| URNM   | Sprott Uranium Miners ETF | Pure-play uranium miners | Medium |
| URNJ   | Sprott Junior Uranium Miners ETF | Junior uranium miners | Small |

---

## Oil & Gas (Energy)

**ETF Count: 6** | Proliferation Score: 60

| Ticker | Name | Focus | AUM Tier |
|--------|------|-------|----------|
| XLE    | Energy Select Sector SPDR Fund | US energy sector | Large |
| XOP    | SPDR S&P Oil & Gas Exploration & Production ETF | Oil & gas E&P | Large |
| OIH    | VanEck Oil Services ETF | Oil services equities | Medium |
| AMLP   | Alerian MLP ETF | Energy MLPs | Medium |
| FCG    | First Trust Natural Gas ETF | Natural gas equities | Small |
| CRAK   | VanEck Oil Refiners ETF | Oil refiners | Small |

---

## Financial Services & Banks

**ETF Count: 5** | Proliferation Score: 60

| Ticker | Name | Focus | AUM Tier |
|--------|------|-------|----------|
| XLF    | Financial Select Sector SPDR Fund | US financial sector | Large |
| KBE    | SPDR S&P Bank ETF | US bank equities | Medium |
| KRE    | SPDR S&P Regional Banking ETF | Regional bank equities | Large |
| IAI    | iShares U.S. Broker-Dealers & Securities Exchanges ETF | Broker-dealers | Small |
| KBWB   | Invesco KBW Bank ETF | Large-cap bank equities | Medium |

---

## Healthcare & Pharma

**ETF Count: 5** | Proliferation Score: 60

| Ticker | Name | Focus | AUM Tier |
|--------|------|-------|----------|
| XLV    | Health Care Select Sector SPDR Fund | US healthcare sector | Large |
| IHE    | iShares U.S. Pharmaceuticals ETF | US pharmaceutical equities | Medium |
| XHS    | SPDR S&P Health Care Services ETF | Healthcare services | Small |
| IHI    | iShares U.S. Medical Devices ETF | Medical devices | Medium |
| PPH    | VanEck Pharmaceutical ETF | Pharmaceutical equities | Small |

---

## Real Estate & REITs

**ETF Count: 4** | Proliferation Score: 60

| Ticker | Name | Focus | AUM Tier |
|--------|------|-------|----------|
| VNQ    | Vanguard Real Estate ETF | US REITs | Large |
| XLRE   | Real Estate Select Sector SPDR Fund | US real estate sector | Large |
| IYR    | iShares U.S. Real Estate ETF | US real estate equities | Large |
| MORT   | VanEck Mortgage REIT Income ETF | Mortgage REITs | Small |

---

## Retail & Consumer

**ETF Count: 4** | Proliferation Score: 60

| Ticker | Name | Focus | AUM Tier |
|--------|------|-------|----------|
| XLY    | Consumer Discretionary Select Sector SPDR Fund | Consumer discretionary | Large |
| XRT    | SPDR S&P Retail ETF | Retail equities | Medium |
| XLP    | Consumer Staples Select Sector SPDR Fund | Consumer staples | Large |
| IBUY   | Amplify Online Retail ETF | Online retail equities | Small |

---

## Summary Table

| Theme | ETF Count | Proliferation Score |
|-------|-----------|-------------------|
| AI & Semiconductors | 11 | 100 |
| Clean Energy & EV | 9 | 80 |
| Biotech & Genomics | 6 | 60 |
| Oil & Gas (Energy) | 6 | 60 |
| Gold & Precious Metals | 5 | 60 |
| Defense & Aerospace | 5 | 60 |
| Blockchain & Crypto | 5 | 60 |
| Financial Services & Banks | 5 | 60 |
| Healthcare & Pharma | 5 | 60 |
| Cloud Computing & SaaS | 4 | 60 |
| Cybersecurity | 4 | 60 |
| Real Estate & REITs | 4 | 60 |
| Retail & Consumer | 4 | 60 |
| Infrastructure & Construction | 3 | 40 |
| Cannabis | 3 | 40 |
| Nuclear Energy | 3 | 40 |
| Water Resources | 3 | 40 |
| Robotics & Automation | 3 | 40 |
| Uranium | 3 | 40 |
| Obesity & GLP-1 | 2 | 40 |
| Lithium & Battery Technology | 2 | 40 |

**Notes:**
- Some ETFs appear in multiple themes (e.g., LIT in both Clean Energy and Lithium, IRBO in both AI and Robotics)
- AUM Tier: Large (>$1B), Medium ($100M-$1B), Small (<$100M)
- Leveraged ETFs (LABU, CLDL) included for completeness but not recommended for theme exposure measurement
- Catalog should be updated quarterly to capture new ETF launches and closures

### Referencia: references/theme_detection_methodology.md

# Theme Detection Methodology

## Overview

The Theme Detector uses a **3-Dimensional Scoring Model** to identify, rank, and assess market themes. Unlike single-score ranking systems, this approach separates the intensity of a theme (heat), its maturity stage (lifecycle), and the reliability of the signal (confidence) into independent dimensions.

---

## Dimension 1: Theme Heat (0-100)

Theme Heat measures the **direction-neutral strength** of a theme. A high heat score means the theme is generating significant market activity, regardless of whether it is bullish or bearish.

### Components

#### 1.1 Momentum Strength (weight: 35%)

Measures the direction-neutral momentum strength using a log-sigmoid function on the absolute weighted return.

**Formula:**
```
weighted_return = perf_1w * 0.10 + perf_1m * 0.25 + perf_3m * 0.35 + perf_6m * 0.30
momentum_score = 100 / (1 + exp(-2.0 * (ln(1 + |weighted_return|) - ln(16))))
```

Midpoint at |15%| weighted return. Log transform compresses extreme values for better mid-range separation. Absolute value is used so both strong bullish and strong bearish moves generate high heat.

**Data Source:** FINVIZ industry performance (1W, 1M, 3M, 6M change %)

**Example Scores (continuous, not stepped):**
| |Weighted Return| | Score |
|---------------------|-------|
| 0% | ~3 |
| 5% | ~27 |
| 15% | 50 (midpoint) |
| 30% | ~73 |
| 50% | ~86 |

#### 1.2 Volume Intensity (weight: 20%)

Measures abnormal volume using sqrt scaling on the 20-day/60-day volume ratio.

**Formula:**
```
ratio = vol_20d / vol_60d
volume_score = min(100, sqrt(max(0, ratio - 0.8)) / sqrt(1.2) * 100)
```

Returns 50.0 if either volume input is None or zero.

**Data Source:** FINVIZ relative volume (volume / avg volume ratio)

**Example Scores:**
| Volume Ratio | Score |
|-------------|-------|
| 1.0 | ~37 |
| 1.2 | ~58 |
| 1.5 | ~76 |
| 2.0 | 100 (ceiling) |

#### 1.3 Uptrend Signal (weight: 25%)

Continuous score from sector uptrend data with base + bonus structure.

**Formula per sector:**
```
base = min(80, ratio * 100)        # continuous 0-80
ma_bonus = 10 if ratio > ma_10     # MA above bonus
slope_bonus = 10 if slope > 0      # positive slope bonus
sector_score = base + ma_bonus + slope_bonus  # 0-100
```

Final score = weighted average of sector scores. For bearish themes, result is inverted (100 - score).

**Data Source:** uptrend-dashboard output (ratio, ma_10, slope per sector)

Returns 50.0 if no sector data available.

#### 1.4 Breadth Signal (weight: 20%)

Measures directionally-aligned industry participation using a power curve with industry count bonus.

**Formula:**
```
breadth_score = min(100, ratio^2.5 * 80 + count_bonus)
count_bonus = min(20, industry_count * 2)
```

The ratio is the fraction of matched industries with directionally-aligned weighted returns (positive for LEAD themes, negative for LAG themes). Power curve (exponent 2.5) suppresses low ratios and amplifies high ones.

**Data Source:** Industry-level weighted returns (not stock-level)

**Example Scores (no count bonus):**
| Breadth Ratio | Score |
|-------------|-------|
| 0.5 | ~14 |
| 0.7 | ~33 |
| 0.9 | ~61 |
| 1.0 | 80 |

Returns 50.0 if ratio is None.

### Theme Heat Composite

```
theme_heat = (momentum * 0.35) + (volume * 0.20) + (uptrend * 0.25) + (breadth * 0.20)
```

Any None sub-score defaults to 50.0. Result clamped to 0-100.

---

## Dimension 2: Lifecycle Maturity

Lifecycle assessment classifies a theme into one of five stages: **Emerging**, **Accelerating**, **Trending**, **Mature**, or **Exhausting**. This is critical for distinguishing emerging opportunities from crowded trades.

### Components

#### 2.1 Duration Score (weight: 25%)

How long the theme has been active (consecutive weeks of elevated heat).

**Measurement:** Count weeks where theme_heat >= 40.

| Duration | Stage Signal |
|----------|-------------|
| 1-3 weeks | Emerging |
| 4-8 weeks | Accelerating |
| 9-12 weeks | Trending |
| 13-16 weeks | Mature |
| > 16 weeks | Exhausting |

**Limitation:** Duration tracking requires historical data. On first run, duration defaults to "Unknown" and lifecycle uses other factors only.

#### 2.2 Extremity Clustering Score (weight: 25%)

Percentage of stocks in the theme near 52-week highs or lows.

**Formula:**
```
extremity_pct = count(within_5pct_of_52wk_high_or_low) / count(total_stocks)
```

| Extremity % | Stage Signal |
|-------------|-------------|
| < 15%       | Emerging |
| 15-30%      | Accelerating |
| 30-45%      | Trending |
| 45-60%      | Mature |
| > 60%       | Exhausting |

**Data Source:** FINVIZ 52-week high/low data

#### 2.3 Price Extreme Saturation Score (weight: 25%)

Proportion of stocks near 52-week extremes (within 5%).

**Formula:**
```
bullish: pct = count(dist_from_52w_high <= 0.05) / total
bearish: pct = count(dist_from_52w_low <= 0.05) / total
score = min(100, pct * 200)
```

#### 2.4 Valuation Score (weight: 15%)

Average P/E ratio of theme constituents relative to S&P 500 P/E.

**Formula:**
```
relative_pe = avg_theme_pe / sp500_pe
```

| Relative P/E | Stage Signal |
|---------------|-------------|
| < 0.8         | Emerging (undervalued) |
| 0.8-1.0       | Accelerating (fair value) |
| 1.0-1.4       | Trending (slightly elevated) |
| 1.4-2.0       | Mature (overvalued) |
| > 2.0         | Exhausting (extreme) |

**Data Source:** FMP API for P/E ratios (optional; uses FINVIZ forward P/E as fallback)

#### 2.5 ETF Proliferation Score (weight: 10%)

Number of thematic ETFs tracking the theme. More ETFs indicate greater retail/institutional attention.

**Source:** `thematic_etf_catalog.md` (static reference)

| ETF Count | Score | Stage Signal |
|-----------|-------|-------------|
| 0         | 0     | Emerging |
| 1         | 20    | Emerging |
| 2-3       | 40    | Accelerating |
| 4-6       | 60    | Trending |
| 7-10      | 80    | Mature |
| > 10      | 100   | Exhausting |

### Lifecycle Maturity Composite

```
maturity = (duration * 0.25) + (extremity * 0.25) + (price_extreme * 0.25) + (valuation * 0.15) + (etf_proliferation * 0.10)
```

### Lifecycle Stage Classification

The lifecycle stage is classified from the maturity score:

| Maturity Score | Stage |
|----------------|-------|
| 0-20 | Emerging |
| 20-40 | Accelerating |
| 40-60 | Trending |
| 60-80 | Mature |
| 80-100 | Exhausting |

**Note:** Media/Narrative Saturation is not included in the automated maturity calculation. Claude's WebSearch narrative confirmation can be used to qualitatively adjust the lifecycle assessment.

---

## Dimension 3: Confidence (Low / Medium / High)

Confidence measures **how reliable** the theme detection is, based on data quality and confirmation signals.

### Layers

#### 3.1 Quantitative Layer (base)

Based on data breadth and consistency:

| Condition | Level |
|-----------|-------|
| >= 4 industries matching, >= 20 stocks analyzed | High |
| 2-3 industries matching, >= 10 stocks analyzed | Medium |
| 1 industry matching or < 10 stocks | Low |

#### 3.2 Breadth Layer (modifier)

Cross-sector participation adds confidence:

| Condition | Modifier |
|-----------|----------|
| Theme spans 3+ sectors | +1 level (cap at High) |
| Theme spans 2 sectors | No change |
| Theme in 1 sector only | -1 level (floor at Low) |

#### 3.3 Narrative Layer (modifier, applied in Step 4)

WebSearch confirmation adjusts confidence:

| Narrative Finding | Modifier |
|-------------------|----------|
| Strong confirmation (multiple sources, clear catalysts) | +1 level |
| Mixed signals | No change |
| Contradictory narrative (bearish articles for bullish theme) | -1 level |

### Final Confidence

```
confidence = apply_modifiers(quantitative_base, breadth_modifier, narrative_modifier)
confidence = clamp(confidence, Low, High)
```

---

## Direction Detection

Theme direction (**leading** vs. **lagging**) is determined by relative rank, not absolute price change:

### Algorithm

1. Each industry gets a `rank_direction` based on its position in the momentum-ranked list: top half = "bullish" (leading), bottom half = "bearish" (lagging).
2. Theme direction is the majority vote of its constituent industries' `rank_direction`.

```python
# Industry-level (industry_ranker.py)
rank_direction = "bullish" if rank <= len(industries) // 2 else "bearish"

# Theme-level (theme_classifier.py)
direction = majority_vote([ind.rank_direction for ind in theme.industries])
```

### Important: Relative, Not Absolute

**LEAD/LAG direction is relative.** A "lagging" theme may still have positive absolute returns — it simply underperforms relative to other themes. This means:
- **LEAD** themes: Suitable for overweight / new positions
- **LAG** themes: Candidates for underweight reduction, **not** short signals

---

## Data Sources

### Primary: FINVIZ

**Elite Mode (recommended):**
- CSV export endpoint: `https://elite.finviz.com/export.ashx?v=151&f=ind_{code},cap_smallover,...&auth=KEY`
- Provides: ticker, company, sector, industry, market cap, P/E, change%, volume, avg volume, 52wk high/low, RSI, SMA20/50/200
- Rate limit: 0.5s between requests
- Coverage: Full stock universe per industry

**Public Mode (fallback):**
- HTML scraping: `https://finviz.com/screener.ashx?v=151&f=ind_{code},cap_smallover`
- Provides: Same fields but limited to page 1 (~20 stocks per industry)
- Rate limit: 2.0s between requests (aggressive scraping may trigger blocks)
- Coverage: Top 20 stocks per industry by market cap

### Secondary: FMP API (optional)

- P/E ratios for valuation analysis
- Not required; FINVIZ forward P/E used as fallback
- Useful for more granular valuation metrics

### Tertiary: uptrend-dashboard (optional)

- CSV output from the uptrend-dashboard skill
- Provides 3-point technical evaluation per stock
- Significantly improves uptrend ratio accuracy
- If unavailable, FINVIZ price-vs-SMA200 is used as proxy

### Quaternary: WebSearch (narrative layer)

- Used for narrative confirmation in Step 4
- Not automated; Claude performs searches during workflow
- Subjective assessment of media coverage and analyst sentiment

---

## Integration with uptrend-dashboard

When uptrend-dashboard data is available, the theme detector uses it for enhanced 3-point evaluation:

**3-Point Evaluation Criteria:**
1. Price > 50-day SMA (short-term trend)
2. 50-day SMA > 200-day SMA (medium-term trend, golden/death cross)
3. 200-day SMA is rising (long-term trend confirmation)

**Stocks meeting all 3 points** = in confirmed uptrend
**Stocks meeting 0 points** = in confirmed downtrend

This provides more accurate uptrend ratios than simple price-above-SMA200 proxy.

---

## Output Schema

### JSON Output Structure

```json
{
  "metadata": {
    "date": "2026-02-16",
    "mode": "elite",
    "themes_analyzed": 14,
    "industries_scanned": 145,
    "total_stocks": 5200,
    "uptrend_data_available": true,
    "execution_time_seconds": 150
  },
  "themes": [
    {
      "name": "AI & Semiconductors",
      "direction": "Bullish",
      "direction_strength": "Strong",
      "theme_heat": 82,
      "heat_components": {
        "momentum": 90,
        "volume": 75,
        "uptrend": 85,
        "breadth": 70
      },
      "lifecycle": {
        "stage": "Mature",
        "duration_weeks": 12,
        "extremity_pct": 45,
        "relative_pe": 1.8,
        "etf_proliferation_score": 100,
        "etf_count": 11
      },
      "confidence": "High",
      "confidence_components": {
        "quantitative": "High",
        "breadth_modifier": "+1",
        "narrative_modifier": "pending"
      },
      "industries": [
        {
          "name": "Semiconductors",
          "change_pct": 4.2,
          "avg_relative_volume": 1.8,
          "uptrend_ratio": 0.75,
          "stock_count": 35
        }
      ],
      "top_stocks": [
        {"ticker": "NVDA", "change_pct": 6.5, "relative_volume": 2.1},
        {"ticker": "AVGO", "change_pct": 4.8, "relative_volume": 1.9}
      ],
      "proxy_etfs": ["SMH", "SOXX", "AIQ", "BOTZ"]
    }
  ],
  "industry_rankings": {
    "top_10": [...],
    "bottom_10": [...]
  },
  "sector_summary": {
    "Technology": {"uptrend_ratio": 0.65, "avg_change_pct": 2.1},
    "Energy": {"uptrend_ratio": 0.40, "avg_change_pct": -1.5}
  }
}
```

---

## Known Limitations

1. **Static theme definitions**: Cross-sector themes are predefined in `cross_sector_themes.md`. New themes (e.g., a sudden meme-stock theme) are not automatically detected.

2. **Industry granularity**: FINVIZ industry classification may not perfectly map to investment themes. Some industries span multiple themes.

3. **Single-stock dominance**: Large-cap stocks (e.g., NVDA in AI) can skew theme-level metrics. Market-cap weighting amplifies this effect.

4. **Temporal lag**: Weekly performance data does not capture intraday or same-day momentum shifts.

5. **ETF catalog staleness**: The thematic ETF catalog is manually maintained and may not reflect recent ETF launches or closures.

6. **Public mode data limits**: Only ~20 stocks per industry are captured, which may underrepresent small/mid-cap participation.

7. **Duration tracking**: First-run analysis cannot assess theme duration without historical baseline data.

8. **Narrative subjectivity**: Confidence adjustment from WebSearch is inherently subjective and depends on search result quality.

9. **Survivorship bias**: Analysis only covers currently listed stocks and active ETFs, missing delisted or closed instruments.

10. **FINVIZ data delays**: Public FINVIZ data is 15-minute delayed; Elite provides real-time during market hours.


---

## SKILL: token-economics

- Fuente: `agiprolabs/claude-trading-skills` → `skills/token-economics` (MIT)
- Cuándo usarla: Token supply dynamics, vesting analysis, inflation modeling, and valuation frameworks for crypto tokens
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/token-economics/` (supply_modeler.py, tokenomics_analyzer.py)

# Token Economics

Tokenomics — the study of token supply dynamics, distribution, and value accrual — is one of the most important factors in crypto asset analysis. Supply changes directly affect price: new tokens entering circulation create selling pressure, while burns and locks reduce it. Understanding these dynamics lets you estimate dilution risk, identify overvalued or undervalued tokens, and anticipate price-moving unlock events.

## Why Tokenomics Matters

Price is a function of demand **and** supply. In crypto, supply is programmable and constantly changing:

- A token inflating at 50%/year needs 50% demand growth just to maintain price
- A large unlock releasing 10% of circulating supply in one day often causes 5-20% drawdowns
- Tokens with >80% of supply locked have extreme dilution risk ahead
- Protocols that burn fees can become net deflationary, creating structural price support

## Key Supply Concepts

### Total Supply vs Circulating Supply

```
total_supply      = maximum tokens that will ever exist (or current total minted)
circulating_supply = tokens currently available for trading
locked_supply     = total_supply - circulating_supply
circulating_pct   = circulating_supply / total_supply * 100
```

### Market Cap vs Fully Diluted Valuation

```
market_cap = price * circulating_supply
fdv        = price * total_supply
fdv_mcap_ratio = fdv / market_cap
```

The **FDV/MCap ratio** measures future dilution risk:

| FDV/MCap | Dilution Risk | Interpretation |
|----------|---------------|----------------|
| 1.0-1.5  | Low           | Most supply already circulating |
| 1.5-3.0  | Moderate      | Significant supply still locked |
| 3.0-5.0  | High          | Majority of supply not yet released |
| >5.0     | Very High     | Token will face massive dilution |

### Net Inflation Rate

```python
annual_new_tokens = emissions + vesting_unlocks + rewards
annual_burned     = fee_burns + buyback_burns
net_new_tokens    = annual_new_tokens - annual_burned
net_inflation_rate = net_new_tokens / circulating_supply * 100  # percent per year
```

## Supply Dynamics

### Inflationary Pressure (tokens entering circulation)

- **Emissions**: Block rewards, liquidity mining, staking rewards
- **Vesting unlocks**: Team, investor, and advisor tokens unlocking on schedule
- **Unlock events**: Large one-time releases (cliff expirations)
- **Treasury spending**: DAO or foundation distributing tokens

### Deflationary Pressure (tokens leaving circulation)

- **Fee burns**: Protocol burns a portion of transaction fees (like EIP-1559)
- **Buyback and burn**: Protocol uses revenue to buy and permanently destroy tokens
- **Staking locks**: Tokens locked in staking (temporarily removed from circulation)
- **Lost tokens**: Permanently inaccessible tokens (lost keys, burn addresses)

### Selling Pressure Estimation

```python
daily_emissions_usd = daily_new_tokens * token_price
percent_sold = 0.50  # assume 50% of new tokens are sold (conservative)
daily_sell_pressure = daily_emissions_usd * percent_sold
sell_pressure_ratio = daily_sell_pressure / daily_volume
# > 0.05 (5%) = significant selling pressure
# > 0.10 (10%) = heavy selling pressure
```

## Vesting and Unlock Schedules

### Key Concepts

- **Cliff**: Period before any tokens unlock (typically 6-12 months)
- **Linear vesting**: Constant rate of unlock after cliff (monthly or daily)
- **Stepped vesting**: Periodic unlocks at set intervals (quarterly)
- **TGE unlock**: Percentage released at Token Generation Event

### Analyzing Unlock Impact

```python
unlock_amount_tokens = 10_000_000
avg_daily_volume_tokens = 5_000_000
unlock_volume_ratio = unlock_amount_tokens / avg_daily_volume_tokens

# Impact assessment:
# < 1x daily volume: minor impact
# 1-5x daily volume: moderate impact, expect 2-5% drawdown
# 5-10x daily volume: major impact, expect 5-15% drawdown
# > 10x daily volume: severe impact, expect 10-30% drawdown
```

### Tracking Sources

- **CoinGecko / CoinMarketCap**: Basic supply data
- **Token Terminal**: Revenue and valuation metrics
- **Token Unlocks (token.unlocks.app)**: Detailed unlock schedules
- **Project documentation**: Whitepapers, tokenomics pages
- **On-chain**: Vesting contract state, treasury balances

## Token Distribution Analysis

### Typical Allocation Ranges

| Category | Typical Range | Red Flag |
|----------|---------------|----------|
| Team/Founders | 15-25% | >30% |
| Investors (Seed+Series) | 10-30% | >40% |
| Community/Ecosystem | 20-40% | <15% |
| Treasury/DAO | 10-20% | <5% |
| Public Sale | 5-20% | <2% |
| Advisors | 2-5% | >10% |

### Distribution Red Flags

- **>50% insider allocation** (team + investors): Insiders control price
- **Short vesting** (<1 year): Quick dump risk
- **No cliff**: Immediate selling from day one
- **Large single wallets**: Concentration risk (use `token-holder-analysis` skill)
- **Unlabeled large allocations**: Hidden insider holdings

### Distribution Quality Score

```python
def distribution_score(team_pct: float, investor_pct: float,
                       community_pct: float, cliff_months: int,
                       vesting_months: int) -> str:
    """Rate token distribution quality."""
    score = 0
    insider_pct = team_pct + investor_pct

    if insider_pct < 30: score += 3
    elif insider_pct < 50: score += 1

    if community_pct > 30: score += 2
    elif community_pct > 20: score += 1

    if cliff_months >= 12: score += 2
    elif cliff_months >= 6: score += 1

    if vesting_months >= 36: score += 2
    elif vesting_months >= 24: score += 1

    if score >= 8: return "Excellent"
    if score >= 6: return "Good"
    if score >= 4: return "Moderate"
    return "Poor"
```

## Valuation Frameworks

### Revenue-Based Metrics

```python
# Price-to-Earnings (for fee-generating protocols)
pe_ratio = fdv / annualized_net_revenue

# Price-to-Sales
ps_ratio = fdv / annualized_total_volume

# Price-to-Fees
pf_ratio = fdv / annualized_protocol_fees

# Revenue Multiple (adjusted for token value accrual)
rev_multiple = fdv / (annualized_fees * fee_share_to_token_holders)
```

**Typical ranges** (crypto, highly variable):
- P/E: 10x-100x+ (DeFi protocols)
- P/S: 0.5x-50x
- P/F: 20x-500x

### Network Value Metrics

```python
# Network Value to Transactions (NVT)
nvt = market_cap / daily_transaction_volume_usd
# High NVT (>100): potentially overvalued or store-of-value
# Low NVT (<20): potentially undervalued or high activity

# Market Value to Realized Value (MVRV)
# realized_value = sum of each token at its last-moved price
mvrv = market_cap / realized_value
# MVRV > 3.0: historically overvalued zone
# MVRV < 1.0: historically undervalued zone
```

### Comparable Analysis

```python
def comparable_analysis(target: dict, peers: list[dict]) -> dict:
    """Compare target token metrics against peer group.

    Each dict has: name, fdv, revenue, tvl, users
    Returns premium/discount percentages.
    """
    peer_fdv_rev = [p["fdv"] / p["revenue"] for p in peers if p["revenue"] > 0]
    peer_fdv_tvl = [p["fdv"] / p["tvl"] for p in peers if p["tvl"] > 0]

    avg_fdv_rev = sum(peer_fdv_rev) / len(peer_fdv_rev) if peer_fdv_rev else 0
    avg_fdv_tvl = sum(peer_fdv_tvl) / len(peer_fdv_tvl) if peer_fdv_tvl else 0

    target_fdv_rev = target["fdv"] / target["revenue"] if target["revenue"] > 0 else 0
    target_fdv_tvl = target["fdv"] / target["tvl"] if target["tvl"] > 0 else 0

    return {
        "fdv_rev_premium": (target_fdv_rev / avg_fdv_rev - 1) * 100 if avg_fdv_rev else None,
        "fdv_tvl_premium": (target_fdv_tvl / avg_fdv_tvl - 1) * 100 if avg_fdv_tvl else None,
    }
```

### Token Value Accrual Mechanisms

| Mechanism | Description | Valuation Impact |
|-----------|-------------|-----------------|
| Fee sharing | Holders receive protocol revenue | Direct cash flow, use DCF |
| Governance | Voting rights on protocol | Hard to value, often overpriced |
| Utility | Required for protocol use | Demand scales with usage |
| Buyback & burn | Protocol buys and burns | Reduces supply, structural bid |
| Staking rewards | Yield from staking | Inflationary if from emissions |
| veToken model | Lock for boosted rewards + governance | Reduces circulating supply |

## PumpFun Token Economics

PumpFun tokens on Solana have simplified tokenomics:

- **Fixed supply**: 1,000,000,000 tokens (1 billion)
- **No vesting**: All tokens available immediately at launch
- **No team allocation**: 100% available on bonding curve
- **Bonding curve pricing**: Price determined by curve math, not supply changes
- **Post-graduation**: After bonding curve completes, supply is fully liquid on Raydium
- **No inflation**: No emissions, no staking rewards, no additional minting

Analysis focus for PumpFun tokens shifts from supply dynamics to:
- Holder concentration (use `token-holder-analysis`)
- Volume sustainability
- Liquidity depth (use `liquidity-analysis`)
- Dev wallet behavior

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| `defillama-api` | Fetch TVL, revenue, fees for valuation metrics |
| `token-holder-analysis` | Analyze holder concentration and whale behavior |
| `coingecko-api` | Fetch supply data, market cap, FDV |
| `liquidity-analysis` | Assess trading liquidity relative to supply |
| `risk-management` | Supply dilution as risk factor |
| `position-sizing` | Adjust size for dilution risk |

## Files

### References
- `references/supply_analysis.md` — Circulating supply tracking, inflation modeling, unlock analysis, burn mechanics
- `references/valuation_frameworks.md` — Revenue-based valuation, NVT, MVRV, comparable analysis, value accrual

### Scripts
- `scripts/tokenomics_analyzer.py` — Fetch and analyze token supply metrics from CoinGecko, calculate dilution risk and basic valuations
- `scripts/supply_modeler.py` — Project token supply over 12 months given emission and burn parameters, scenario analysis

### Referencia: references/supply_analysis.md

# Supply Analysis Reference

Comprehensive guide to tracking circulating supply, modeling inflation, analyzing unlock schedules, and evaluating burn mechanisms.

## Circulating Supply Tracking

### Data Sources

**CoinGecko API (free tier)**:
```python
import httpx

resp = httpx.get(
    "https://api.coingecko.com/api/v3/coins/solana",
    params={"localization": "false", "tickers": "false",
            "community_data": "false", "developer_data": "false"}
)
data = resp.json()
circulating = data["market_data"]["circulating_supply"]
total = data["market_data"]["total_supply"]
max_supply = data["market_data"]["max_supply"]  # None if unlimited
```

**On-chain calculation** (Solana SPL tokens):
```
circulating = total_minted - burned - locked_in_vesting - treasury_held - staked_locked
```

Common locked account types:
- Team vesting contracts (PDA accounts with time-lock)
- DAO treasury multisigs
- Staking contracts (may or may not count as circulating)
- Burn address (`1111111111111111111111111111111111`)

### Supply Classification

| Category | Counts as Circulating? | Notes |
|----------|----------------------|-------|
| Trading on DEX/CEX | Yes | Active market supply |
| In user wallets | Yes | Potentially tradeable |
| Staked (liquid staking) | Yes | Can be unstaked and sold |
| Staked (locked period) | Depends | Locked for fixed term |
| Team vesting (locked) | No | Cannot be sold yet |
| Treasury (DAO-controlled) | Depends | Requires governance vote |
| Burned | No | Permanently removed |

## Inflation Modeling

### Emission Sources

1. **Block rewards / Staking rewards**: Continuous issuance to validators/stakers
2. **Liquidity mining**: Token incentives for LPs (often largest source)
3. **Ecosystem grants**: Foundation distributing to builders
4. **Vesting unlocks**: Scheduled release of locked tokens

### Calculating Current Inflation Rate

```python
def annual_inflation_rate(
    daily_staking_rewards: float,
    daily_lm_emissions: float,
    monthly_vesting_unlocks: float,
    annual_grants: float,
    circulating_supply: float
) -> float:
    """Calculate annualized inflation rate as a percentage.

    Args:
        daily_staking_rewards: Tokens issued as staking rewards per day.
        daily_lm_emissions: Tokens emitted for liquidity mining per day.
        monthly_vesting_unlocks: Tokens unlocking from vesting per month.
        annual_grants: Tokens distributed as ecosystem grants per year.
        circulating_supply: Current circulating supply.

    Returns:
        Annualized inflation rate as percentage.
    """
    annual_new = (
        daily_staking_rewards * 365
        + daily_lm_emissions * 365
        + monthly_vesting_unlocks * 12
        + annual_grants
    )
    return (annual_new / circulating_supply) * 100
```

### Inflation Impact Tiers

| Annual Inflation | Impact | Examples |
|-----------------|--------|----------|
| 0-2% | Minimal | Bitcoin (post-2024 halving) |
| 2-5% | Low | Mature L1s, established protocols |
| 5-15% | Moderate | Growing protocols with LM programs |
| 15-30% | High | Early-stage with aggressive emissions |
| >30% | Severe | Yield farms, Ponzi-adjacent |

### Projecting Supply Over Time

```python
def project_supply(
    current_circulating: float,
    total_supply: float,
    monthly_emissions: float,
    monthly_burns: float,
    vesting_schedule: list[float],  # monthly unlock amounts, 12 entries
    months: int = 12
) -> list[dict]:
    """Project circulating supply month by month.

    Args:
        current_circulating: Starting circulating supply.
        total_supply: Maximum total supply cap.
        monthly_emissions: New tokens from emissions per month.
        monthly_burns: Tokens burned per month.
        vesting_schedule: List of monthly vesting unlock amounts.
        months: Number of months to project.

    Returns:
        List of monthly projections with supply and inflation data.
    """
    projections = []
    circ = current_circulating

    for m in range(months):
        vest = vesting_schedule[m] if m < len(vesting_schedule) else 0
        new_tokens = monthly_emissions + vest
        net_new = new_tokens - monthly_burns
        circ = min(circ + net_new, total_supply)
        monthly_rate = net_new / (circ - net_new) * 100 if circ > net_new else 0

        projections.append({
            "month": m + 1,
            "circulating": circ,
            "circulating_pct": circ / total_supply * 100,
            "monthly_inflation_pct": monthly_rate,
            "net_new_tokens": net_new,
        })
    return projections
```

## Unlock Schedule Analysis

### Unlock Types and Impact

**Cliff unlocks** (one-time large release):
- Typically 10-25% of allocation at cliff expiration
- Often the highest-impact event
- Price impact: correlates with unlock_amount / daily_volume ratio

**Linear vesting** (continuous drip):
- Steady daily/monthly release after cliff
- Creates consistent but manageable sell pressure
- Impact spread over time

**Stepped unlocks** (periodic releases):
- Quarterly or monthly batch releases
- Each step is a mini-cliff event
- Plan for each step individually

### Estimating Price Impact

```python
def estimate_unlock_impact(
    unlock_tokens: float,
    token_price: float,
    avg_daily_volume_usd: float,
    sell_assumption: float = 0.30
) -> dict:
    """Estimate the price impact of a token unlock event.

    Args:
        unlock_tokens: Number of tokens being unlocked.
        token_price: Current token price in USD.
        avg_daily_volume_usd: Average daily trading volume in USD.
        sell_assumption: Fraction of unlocked tokens expected to be sold.

    Returns:
        Impact assessment with severity rating.
    """
    unlock_value = unlock_tokens * token_price
    expected_sell = unlock_value * sell_assumption
    days_to_absorb = expected_sell / avg_daily_volume_usd if avg_daily_volume_usd > 0 else float("inf")

    if days_to_absorb < 0.5:
        severity = "Minor"
        est_drawdown = "0-2%"
    elif days_to_absorb < 2:
        severity = "Moderate"
        est_drawdown = "2-5%"
    elif days_to_absorb < 5:
        severity = "Significant"
        est_drawdown = "5-15%"
    else:
        severity = "Severe"
        est_drawdown = "15-30%+"

    return {
        "unlock_value_usd": unlock_value,
        "expected_sell_usd": expected_sell,
        "days_to_absorb": round(days_to_absorb, 2),
        "severity": severity,
        "estimated_drawdown": est_drawdown,
    }
```

### Historical Unlock Behavior

Empirical observations from major token unlocks:
- **Team/founder tokens**: ~30-50% sold within 30 days of unlock
- **VC/investor tokens**: ~40-70% sold within 30 days (profit-taking)
- **Ecosystem/community**: ~10-20% sold (often redistributed, not dumped)
- **Staking unlocks**: ~5-15% sold (most restake)

## Burn Mechanisms

### Types of Burns

| Mechanism | Predictability | Examples |
|-----------|---------------|----------|
| Fee burn (per-tx) | High (scales with usage) | Ethereum EIP-1559, Solana partial burns |
| Buyback & burn | Medium (depends on revenue) | BNB quarterly burns, MKR surplus auctions |
| Manual/scheduled burn | High (announced schedule) | Periodic planned burns |
| Deflationary tax | High (on every transfer) | Reflection tokens (often unsustainable) |

### Net Inflation Calculation

```python
def net_inflation(
    annual_emissions: float,
    annual_burns: float,
    circulating_supply: float
) -> dict:
    """Calculate net inflation accounting for burns.

    Args:
        annual_emissions: Total new tokens emitted per year.
        annual_burns: Total tokens burned per year.
        circulating_supply: Current circulating supply.

    Returns:
        Net inflation metrics.
    """
    net = annual_emissions - annual_burns
    rate = (net / circulating_supply) * 100
    return {
        "gross_inflation_pct": (annual_emissions / circulating_supply) * 100,
        "burn_rate_pct": (annual_burns / circulating_supply) * 100,
        "net_inflation_pct": rate,
        "is_deflationary": net < 0,
        "years_to_double": 72 / rate if rate > 0 else None,  # Rule of 72
    }
```

## Worked Example: Analyzing SOL Supply Dynamics

**Solana (SOL) as of early 2025:**
- Total supply: ~590M SOL
- Circulating supply: ~430M SOL
- Circulating %: ~73%
- FDV/MCap ratio: ~1.37 (low dilution risk)
- Staking rewards: ~5.5% APY (inflationary but offset by 50% fee burn)
- Annual inflation: ~5% gross, ~4.5% net (after fee burns)
- No vesting events remaining (all early vesting completed)

**Assessment:**
- Low dilution risk (FDV/MCap near 1)
- Moderate net inflation (~4.5%/year)
- Fee burns increasing with network usage
- Path to net deflation if transaction volume grows significantly

### Referencia: references/valuation_frameworks.md

# Valuation Frameworks Reference

Comprehensive guide to revenue-based valuation, network value metrics, comparable analysis, and token value accrual assessment for crypto assets.

## Revenue-Based Valuation

### Price-to-Earnings (P/E)

```
P/E = FDV / annualized_net_revenue
```

- **Net revenue** = protocol fees retained (not distributed to LPs or users)
- Most directly comparable to traditional P/E
- Only applicable to fee-generating protocols

**Crypto P/E ranges** (as of 2025, highly variable):

| Range | Interpretation | Typical Protocols |
|-------|---------------|-------------------|
| <10x | Potentially undervalued or declining | Legacy protocols losing share |
| 10-30x | Reasonable for mature protocols | Established DEXs, lending |
| 30-100x | Growth premium | Fast-growing protocols |
| 100-500x | High growth expectations | New category leaders |
| >500x | Speculative or minimal revenue | Most tokens |

### Price-to-Sales (P/S)

```
P/S = FDV / annualized_total_volume
```

- Uses total volume, not just protocol revenue
- Better for comparing protocols with different fee structures
- Lower P/S suggests better value per unit of activity

### Price-to-Fees (P/F)

```
P/F = FDV / annualized_total_fees
```

- Total fees generated (including LP fees, not just protocol take)
- Measures total economic activity, not just protocol capture
- Useful for comparing DEXs with different fee splits

### Revenue Quality Assessment

Not all revenue is equal:

| Revenue Type | Quality | Sustainability |
|-------------|---------|----------------|
| Trading fees (organic) | High | Scales with market activity |
| Lending interest | High | Consistent in all markets |
| Liquidation fees | Medium | Spikes in volatility, zero otherwise |
| LM-incentivized volume | Low | Disappears when incentives end |
| MEV revenue | Medium | Structural but variable |
| Bridge fees | Medium | Dependent on cross-chain activity |

```python
def revenue_quality_score(
    organic_fees_pct: float,
    incentivized_fees_pct: float,
    one_time_pct: float,
    months_of_data: int
) -> dict:
    """Score revenue quality for valuation purposes.

    Args:
        organic_fees_pct: Percentage of fees from organic activity.
        incentivized_fees_pct: Percentage from LM-incentivized activity.
        one_time_pct: Percentage from one-time events.
        months_of_data: How many months of revenue history.

    Returns:
        Quality assessment with adjustment factor.
    """
    base = organic_fees_pct * 1.0 + incentivized_fees_pct * 0.3 + one_time_pct * 0.1
    history_factor = min(months_of_data / 12, 1.0)  # penalize short history
    score = base * history_factor

    if score > 70:
        quality = "High"
        valuation_discount = 0  # no discount needed
    elif score > 40:
        quality = "Medium"
        valuation_discount = 20  # apply 20% discount to revenue multiple
    else:
        quality = "Low"
        valuation_discount = 50  # apply 50% discount

    return {
        "quality": quality,
        "score": round(score, 1),
        "valuation_discount_pct": valuation_discount,
    }
```

## Network Value to Transactions (NVT)

### Calculation

```
NVT = market_cap / daily_on_chain_transaction_volume_usd
```

NVT is the crypto equivalent of P/E for networks without traditional revenue. It measures how much the market values each dollar of on-chain activity.

### Interpretation

| NVT Range | Signal | Context |
|-----------|--------|---------|
| <20 | Potentially undervalued | High activity relative to valuation |
| 20-50 | Fair value zone | Balanced activity and valuation |
| 50-100 | Potentially overvalued | Low activity relative to valuation |
| >100 | Overvalued or store-of-value | May be justified for BTC-like assets |

### NVT Signal (smoothed)

```python
def nvt_signal(
    market_cap: float,
    daily_volumes: list[float],
    window: int = 90
) -> float:
    """Calculate smoothed NVT Signal using moving average of volume.

    Args:
        market_cap: Current market capitalization.
        daily_volumes: List of daily on-chain volumes (most recent last).
        window: Moving average window in days.

    Returns:
        NVT Signal value.
    """
    if len(daily_volumes) < window:
        window = len(daily_volumes)
    avg_volume = sum(daily_volumes[-window:]) / window
    return market_cap / avg_volume if avg_volume > 0 else float("inf")
```

NVT Signal smooths out daily volume noise, giving a more reliable valuation indicator than raw NVT.

## Market Value to Realized Value (MVRV)

### Concept

**Realized value** sums each token at the price it last moved on-chain, representing the aggregate cost basis of all holders.

```
MVRV = market_cap / realized_value
```

### Interpretation

| MVRV | Zone | Historical Meaning |
|------|------|--------------------|
| <0.8 | Deep undervalue | Aggregate holders at a loss, capitulation |
| 0.8-1.0 | Undervalue | Most holders near breakeven or slightly down |
| 1.0-2.0 | Fair value | Moderate unrealized gains |
| 2.0-3.0 | Overvalue caution | Significant unrealized gains, profit-taking likely |
| >3.0 | Overvalue danger | Historical tops often occur here |

### Limitations

- Only available for UTXO chains (BTC) and some account-based chains
- Not applicable to most DeFi tokens (insufficient on-chain transfer data)
- Realized value can be skewed by exchange movements
- Works best as a macro cycle indicator, not for short-term trading

## Comparable Analysis

### Methodology

1. **Select peer group**: Tokens in the same sector (DEX, lending, L1, L2, etc.)
2. **Gather metrics**: FDV, revenue, TVL, users, volume for each
3. **Calculate ratios**: FDV/Revenue, FDV/TVL, FDV/DAU
4. **Rank**: Where does the target fall vs peers?
5. **Assess premium/discount**: Is it justified by growth, moat, risk?

### Standard Comparison Metrics

```python
def build_comp_table(protocols: list[dict]) -> list[dict]:
    """Build comparable analysis table for a set of protocols.

    Args:
        protocols: List of dicts with keys: name, fdv, revenue, tvl, dau, volume.

    Returns:
        List of dicts with calculated valuation ratios.
    """
    result = []
    for p in protocols:
        row = {"name": p["name"], "fdv": p["fdv"]}
        row["fdv_revenue"] = p["fdv"] / p["revenue"] if p.get("revenue", 0) > 0 else None
        row["fdv_tvl"] = p["fdv"] / p["tvl"] if p.get("tvl", 0) > 0 else None
        row["fdv_dau"] = p["fdv"] / p["dau"] if p.get("dau", 0) > 0 else None
        row["revenue_per_tvl"] = p.get("revenue", 0) / p["tvl"] if p.get("tvl", 0) > 0 else None
        result.append(row)
    return result
```

### Sector-Specific Benchmarks (approximate ranges, 2025)

| Sector | FDV/Revenue | FDV/TVL | Notes |
|--------|-------------|---------|-------|
| DEX | 20-100x | 1-10x | Higher for growing DEXs |
| Lending | 30-150x | 0.5-5x | Stable revenue, lower multiples |
| L1 | 50-500x | 5-50x | Premium for ecosystem size |
| L2 | 100-1000x | 10-100x | Early stage, growth premium |
| Perpetuals | 15-80x | 2-15x | High revenue efficiency |

## Token Value Accrual

### Fee Sharing

Tokens that distribute protocol revenue directly to holders:

```python
def fee_share_yield(
    annualized_fees: float,
    fee_share_pct: float,
    token_fdv: float
) -> float:
    """Calculate implied yield from fee sharing.

    Args:
        annualized_fees: Total protocol fees per year in USD.
        fee_share_pct: Percentage of fees distributed to token holders.
        token_fdv: Fully diluted valuation of the token.

    Returns:
        Implied annual yield as a percentage.
    """
    distributed = annualized_fees * (fee_share_pct / 100)
    return (distributed / token_fdv) * 100
```

### Buyback & Burn Valuation

```python
def buyback_burn_impact(
    annual_burn_usd: float,
    circulating_supply: float,
    token_price: float
) -> dict:
    """Calculate the supply reduction from buyback and burn.

    Args:
        annual_burn_usd: USD value of annual buyback and burn.
        circulating_supply: Current circulating supply.
        token_price: Current token price.

    Returns:
        Annual supply reduction metrics.
    """
    tokens_burned = annual_burn_usd / token_price
    supply_reduction_pct = (tokens_burned / circulating_supply) * 100
    return {
        "tokens_burned_annually": tokens_burned,
        "supply_reduction_pct": supply_reduction_pct,
        "implied_yield_pct": supply_reduction_pct,  # equivalent to dividend yield
    }
```

### veToken Model

Tokens locked for governance + boosted rewards (e.g., CRV -> veCRV):

**Value drivers:**
- Reduces circulating supply (locked for 1-4 years typically)
- Generates yield from fees + bribes
- Governance power over emissions
- Longer lock = more power (incentivizes long-term holding)

**Assessment:**
```python
def ve_token_metrics(total_supply: float, locked_in_ve: float,
                     annual_fees_to_ve: float, annual_bribes: float,
                     ve_token_price: float) -> dict:
    """Calculate veToken model metrics."""
    lock_pct = (locked_in_ve / total_supply) * 100
    ve_value = locked_in_ve * ve_token_price
    total_yield = annual_fees_to_ve + annual_bribes
    yield_pct = (total_yield / ve_value) * 100 if ve_value > 0 else 0
    return {
        "lock_pct": round(lock_pct, 2),
        "ve_yield_pct": round(yield_pct, 2),
        "health": "Strong" if lock_pct > 50 and yield_pct > 5 else "Moderate" if lock_pct > 30 else "Weak",
    }
```

## Summary: Valuation Workflow

1. **Supply**: FDV/MCap ratio, inflation rate, upcoming unlocks
2. **Revenue**: P/E, P/F — is there real, sustainable revenue?
3. **Peers**: Compare ratios to similar protocols
4. **Accrual**: How does the token capture value (fees, burns, utility)?
5. **Risks**: Dilution, insider allocation, revenue sustainability


---

## SKILL: uptrend-analyzer

- Fuente: `tradermonty/claude-trading-skills` → `skills/uptrend-analyzer` (MIT)
- Cuándo usarla: Analyzes market breadth using Monty's Uptrend Ratio Dashboard data to diagnose the current market environment. Generates a 0-100 composite score from 5 components (breadth, sector participation, rotation, momentum, historical context). Use when asking about market breadth, uptrend ratios, or whether the market environment supports equity exposure. No API key required.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/uptrend-analyzer/` (requirements.txt, __init__.py, historical_context_calculator.py, market_breadth_calculator.py, momentum_calculator.py, sector_participation_calculator.py, sector_rotation_calculator.py, data_fetcher.py, provenance_contract.py, report_generator.py, scorer.py, uptrend_analyzer.py)

# Uptrend Analyzer Skill

## Purpose

Diagnose market breadth health using Monty's Uptrend Ratio Dashboard, which tracks ~2,800 US stocks across 11 sectors. Generates a 0-100 composite score (higher = healthier) with exposure guidance.

Unlike the Market Top Detector (API-based risk scorer), this skill uses free CSV data to assess "participation breadth" - whether the market's advance is broad or narrow.

## When to Use This Skill

**English:**
- User asks "Is the market breadth healthy?" or "How broad is the rally?"
- User wants to assess uptrend ratios across sectors
- User asks about market participation or breadth conditions
- User needs exposure guidance based on breadth analysis
- User references Monty's Uptrend Dashboard or uptrend ratios

**Japanese:**
- 「市場のブレドスは健全？」「上昇の裾野は広い？」
- セクター別のアップトレンド比率を確認したい
- 相場参加率・ブレドス状況を診断したい
- ブレドス分析に基づくエクスポージャーガイダンスが欲しい
- Montyのアップトレンドダッシュボードについて質問

## Prerequisites

- **Python 3.9+** with the `requests` library (CSV parsing uses the stdlib `csv`/`io` modules)
- **Internet connection** to fetch CSV data from GitHub (no API key required)
- No paid API subscriptions needed

## Difference from Market Top Detector

| Aspect | Uptrend Analyzer | Market Top Detector |
|--------|-----------------|-------------------|
| Score Direction | Higher = healthier | Higher = riskier |
| Data Source | Free GitHub CSV | FMP API (paid) |
| Focus | Breadth participation | Top formation risk |
| API Key | Not required | Required (FMP) |
| Methodology | Monty Uptrend Ratios | O'Neil/Minervini/Monty |

---

## Execution Workflow

### Phase 1: Execute Python Script

Run the analysis script (no API key needed):

```bash
python3 skills/uptrend-analyzer/scripts/uptrend_analyzer.py
```

The script will:
1. Download CSV data from Monty's GitHub repository
2. Calculate 5 component scores
3. Generate composite score and reports

### Phase 2: Present Results

Present the generated Markdown report to the user, highlighting:
- Composite score and zone classification
- Exposure guidance (Full/Normal/Reduced/Defensive/Preservation)
- Sector heatmap showing strongest and weakest sectors
- Key momentum and rotation signals

---

## 5-Component Scoring System

| # | Component | Weight | Key Signal |
|---|-----------|--------|------------|
| 1 | Market Breadth (Overall) | **30%** | Ratio level + trend direction |
| 2 | Sector Participation | **25%** | Uptrend sector count + ratio spread |
| 3 | Sector Rotation | **15%** | Cyclical vs Defensive balance |
| 4 | Momentum | **20%** | Slope direction + acceleration |
| 5 | Historical Context | **10%** | Percentile rank in history |

## Scoring Zones

| Score | Zone | Exposure Guidance |
|-------|------|-------------------|
| 80-100 | Strong Bull | Full Exposure (100%) |
| 60-79 | Bull | Normal Exposure (80-100%) |
| 40-59 | Neutral | Reduced Exposure (60-80%) |
| 20-39 | Cautious | Defensive (30-60%) |
| 0-19 | Bear | Capital Preservation (0-30%) |

### 7-Level Zone Detail

Each scoring zone is further divided into sub-zones for finer-grained assessment:

| Score | Zone Detail | Color |
|-------|-------------|-------|
| 80-100 | Strong Bull | Green |
| 70-79 | Bull-Upper | Light Green |
| 60-69 | Bull-Lower | Light Green |
| 40-59 | Neutral | Yellow |
| 30-39 | Cautious-Upper | Orange |
| 20-29 | Cautious-Lower | Orange |
| 0-19 | Bear | Red |

### Warning System

Active warnings trigger exposure penalties that tighten guidance even when the composite score is high:

| Warning | Condition | Penalty |
|---------|-----------|---------|
| **Late Cycle** | Commodity avg > both Cyclical and Defensive | -5 |
| **High Spread** | Max-min sector ratio spread > 40pp | -3 |
| **Divergence** | Intra-group std > 8pp, spread > 20pp, or trend dissenters | -3 |

Penalties stack (max -10) + multi-warning discount (+1 when ≥2 active). Applied after composite scoring.

### Momentum Smoothing

Slope values are smoothed using EMA(3) (Exponential Moving Average, span=3) before scoring. Acceleration is calculated by comparing the recent 10-point average vs prior 10-point average of smoothed slopes (10v10 window), with fallback to 5v5 when fewer than 20 data points are available.

### Historical Confidence Indicator

The Historical Context component includes a confidence assessment based on:
- **Sample size:** Number of historical data points available
- **Regime coverage:** Proportion of distinct market regimes (bull/bear/neutral) observed
- **Recency:** How recent the latest data point is

Confidence levels: High, Medium, Low.

---

## API Requirements

**Required:** None (uses free GitHub CSV data)

## Output Files

- JSON: `uptrend_analysis_YYYY-MM-DD_HHMMSS.json`
- Markdown: `uptrend_analysis_YYYY-MM-DD_HHMMSS.md`

## Reference Documents

### `references/uptrend_methodology.md`
- Uptrend Ratio definition and thresholds
- 5-component scoring methodology
- Sector classification (Cyclical/Defensive/Commodity)
- Historical calibration notes

### When to Load References
- **First use:** Load `uptrend_methodology.md` for full framework understanding
- **Regular execution:** References not needed - script handles scoring

## Same-run provenance

Pass `--run-id daily-20261017-unique` to both required market-regime-daily
producers. Without it each producer generates its own unique ID. JSON includes
schema 1.0 `data_provenance` with actual primary timeseries business date,
UTC retrieval time, source and run ID. Unknown adjustment, point-in-time,
survivorship and corporate-action flags are false. Auxiliary summary dates
are unverified; this does not certify the freshness of every composite input.
Missing or malformed primary dates stop report generation.

Pass the exact JSON paths printed by these invocations to Exposure Coach's
`--require-provenance --run-id … --as-of …` mode. Run IDs are caller-provided
consistency markers, not authenticity or point-in-time proof.

### Referencia: references/uptrend_methodology.md

# Uptrend Analyzer Methodology

## Data Source: Monty's Uptrend Ratio Dashboard

Monty's Uptrend Ratio Dashboard tracks approximately 2,800 US stocks across 11 GICS sectors. For each stock, it determines whether the stock is in an "uptrend" based on the criteria below. The dashboard publishes daily CSV data on GitHub.

**GitHub Repository:** `tradermonty/uptrend-dashboard`
**Live Dashboard:** https://uptrend-dashboard.streamlit.app/

### Uptrend Definition (Finviz Elite Screener)

A stock is classified as "uptrend" when it meets **all** of the following conditions:

| Condition | Description |
|-----------|-------------|
| Price > $10 | Penny stocks excluded |
| Avg Volume > 100K | Sufficient liquidity |
| Market Cap > $50M | Micro-cap and above |
| Price > SMA20 | Short-term uptrend |
| Price > SMA200 | Long-term uptrend |
| SMA50 > SMA200 | Golden cross (bullish structure) |
| 52W High/Low > 30% above Low | Recovering from bottom |
| 4-Week Performance: Up | Recent momentum positive |

The **uptrend ratio** = (stocks meeting all conditions) / (stocks meeting base filters: price, volume, market cap).

### CSV Files

| File | Description | Update Frequency |
|------|-------------|------------------|
| `uptrend_ratio_timeseries.csv` | Daily ratios for "all" + 11 sectors | Daily |
| `sector_summary.csv` | Latest snapshot of all sectors | Daily |

**Data availability:**
- "all" (full market): Since 2023-08-11
- Sector-level data: Since 2024-07-21

### Timeseries Columns

| Column | Type | Description |
|--------|------|-------------|
| worksheet | string | "all" or sector slug (e.g., "sec_technology") |
| date | string | YYYY-MM-DD format |
| count | int | Number of stocks in uptrend |
| total | int | Total stocks tracked |
| ratio | float | count/total (0-1 scale, raw decimal) |
| ma_10 | float | 10-day simple moving average of ratio |
| slope | float | 1-day difference of ma_10 (`ma_10.diff()`) |
| trend | string | "up" (slope > 0) or "down" (slope <= 0) |

### Sector Summary Columns

| Column | Type | Description |
|--------|------|-------------|
| Sector | string | Display name (e.g., "Technology") |
| Ratio | float | Current uptrend ratio (0-1) |
| 10MA | float | 10-day MA of ratio |
| Trend | string | "Up" or "Down" |
| Slope | float | 1-day difference of MA |
| Status | string | "Overbought", "Oversold", or "Normal" |

### Indicator Calculations (from source code)

All indicators are computed on-the-fly from raw count/total data:

```
ratio    = count / total
ma_10    = ratio.rolling(10).mean()       # 10-day simple MA
slope    = ma_10.diff()                   # 1-day change of MA
trend    = "up" if slope > 0 else "down"
```

**Peak/Trough Detection:** The dashboard uses `scipy.signal.find_peaks` with parameters `distance=20, prominence=0.015` to identify local tops and bottoms in the 10MA series.

---

## Official Dashboard Thresholds

These thresholds are defined in `src/constants.py` of the source repository:

| Threshold | Value | Meaning |
|-----------|-------|---------|
| **Upper (Overbought)** | **37%** | Ratio above this = overbought conditions |
| **Lower (Oversold)** | **9.7%** | Ratio below this = oversold / crisis |
| MA Period | 10 | Simple moving average window |

### Status Determination

```
ratio > 0.37  -> "Overbought"
ratio < 0.097 -> "Oversold"
otherwise     -> "Normal"
```

### Practical Interpretation

| Ratio | Interpretation | Market Environment |
|-------|---------------|-------------------|
| 50%+ | Strong breadth | Broad bull market, most stocks participating |
| 37-50% | Overbought / Healthy | Above upper threshold, strong but extended |
| 25-37% | Normal / Recovering | Between thresholds, typical trading range |
| 9.7-25% | Weak | Below normal, breadth deteriorating |
| < 9.7% | Oversold / Crisis | Below lower threshold, extreme selling |

---

## 5-Component Scoring System

### Component 1: Market Breadth (Overall) - Weight: 30%

**Rationale:** The overall uptrend ratio is the single most important measure of market health. A high ratio means broad participation; a low ratio means a narrow, fragile market.

**Scoring Bands (aligned with dashboard thresholds):**

| Ratio | Score Range | Signal |
|-------|-------------|--------|
| >= 50% | 90-100 | Strong Bull |
| 37-50% | 70-89 | Bullish (above overbought threshold) |
| 25-37% | 40-69 | Neutral/Recovering |
| 9.7-25% | 10-39 | Weak (between thresholds) |
| < 9.7% | 0-9 | Crisis (below oversold threshold) |

**Trend Adjustment:** +5 when trend="up" and slope>0, -5 when trend="down" and slope<0.

### Component 2: Sector Participation - Weight: 25%

**Rationale:** A healthy market has most sectors participating. When only 2-3 sectors lead, the market is fragile and vulnerable to sector rotation shocks.

**Sub-scores:**
- **Uptrend Count (60%):** Number of sectors in uptrend mapped to 0-100
- **Spread (40%):** Max-min ratio spread. Narrow spread = uniform participation (good). Wide spread = selective market (risky).

**Overbought/Oversold classification uses dashboard thresholds:** >37% = Overbought, <9.7% = Oversold.

### Component 3: Sector Rotation - Weight: 15%

**Rationale:** In a healthy bull market, cyclical sectors (Technology, Consumer Cyclical) lead defensive sectors (Utilities, Consumer Defensive). When defensives lead, it signals risk-off behavior.

**Sector Classification:**

| Group | Sectors |
|-------|---------|
| Cyclical | Technology, Consumer Cyclical, Communication Services, Financial, Industrials |
| Defensive | Utilities, Consumer Defensive, Healthcare, Real Estate |
| Commodity | Energy, Basic Materials |

**Scoring:** Based on cyclical_avg - defensive_avg difference.
- Cyclical lead > +15pp = Strong risk-on (90-100)
- Balanced within +/-5pp = Neutral (45-69)
- Defensive lead > +15pp = Strong risk-off (0-19)

**Commodity Adjustment:** When commodity sectors outperform both cyclical and defensive groups, it may signal late-cycle dynamics. A penalty of -5 to -10 is applied.

**Intra-Group Divergence Detection:** The system detects significant dispersion within Cyclical and Defensive groups. A divergence flag triggers when any of:
- Group internal standard deviation > 8 percentage points
- Group internal max-min spread > 20 percentage points
- One or more sectors trend in the opposite direction from the group majority

When divergence is detected, a -5 penalty is applied to the Component 3 score. This prevents group averages from masking important internal disagreements (e.g., Financial declining while other Cyclicals rise).

> **Note (Dual-Layer Penalty):** Divergence triggers penalties at two levels:
> (1) -5 to the Component 3 score (making the rotation score more truthful), and
> (2) -3 to the composite score (triggering exposure guidance tightening, see Warning System below).
> Net composite impact ≈ 5 × 0.15 (weight) + 3 = **3.75 points**.

### Component 4: Momentum - Weight: 20%

**Rationale:** The direction and rate of change in breadth matters as much as the level. Improving breadth (positive slope, accelerating) suggests the environment is getting better; deteriorating breadth suggests caution.

**Sub-scores:**
- **Slope Score (50%):** Smoothed slope (EMA-3) mapped to 0-100 (typical range: -0.02 to +0.02). The raw 1-day slope (`ma_10.diff()`) is smoothed with a 3-period Exponential Moving Average to reduce daily noise.
- **Acceleration (30%):** Recent 10-point smoothed slope average vs prior 10-point average (10v10 window). Falls back to 5v5 when fewer than 20 data points are available.
- **Sector Slope Breadth (20%):** Count of sectors with positive slope

**Momentum Smoothing:** The raw slope signal from Monty's dashboard is inherently noisy because it is a 1-day difference of a 10-day moving average. The EMA(3) smoothing filter reduces single-day volatility while preserving directional trends. Both raw and smoothed slope values are reported for transparency.

### Component 5: Historical Context - Weight: 10%

**Rationale:** Knowing where the current ratio falls in historical distribution provides perspective. A ratio that seems "low" might be historically average, or vice versa.

**Scoring:** Percentile rank of current ratio in the full historical distribution (Aug 2023 to present).

**Note:** The "all" dataset starts from 2023-08-11 (~650+ data points), while sector data starts from 2024-07-21 (~370+ data points each).

**Confidence Assessment:** Because the historical dataset is limited (~650 data points), the system assesses and reports the confidence level of percentile analysis:

| Factor | Criteria | Score |
|--------|----------|-------|
| **Sample Size** | >=1000: full (3), 500-999: moderate (2), 200-499: limited (1), <200: minimal (0) | 0-3 |
| **Regime Coverage** | Has bear data (min<10%) AND bull data (max>40%): Both (2), one: Partial (1), neither: Narrow (0) | 0-2 |
| **Recency Bias** | Recent 90 days cover >=30% of full range: balanced (1), otherwise: biased (0) | 0-1 |

Total score 5-6 = High, 3-4 = Moderate, 1-2 = Low, 0 = Very Low confidence.

When confidence is Low or Very Low, the signal text includes a `[confidence: Low]` caveat.

---

## Scoring Zones and Exposure Guidance

### 5-Level Zones (backward-compatible)

| Score | Zone | Exposure | Description |
|-------|------|----------|-------------|
| 80-100 | Strong Bull | Full (100%) | Broad participation, strong momentum. Ideal for aggressive positioning. |
| 60-79 | Bull | Normal (80-100%) | Healthy breadth. Standard position management. |
| 40-59 | Neutral | Reduced (60-80%) | Mixed signals. Participate selectively. |
| 20-39 | Cautious | Defensive (30-60%) | Weak breadth. Prioritize capital preservation. |
| 0-19 | Bear | Preservation (0-30%) | Severe deterioration. Maximum defense. |

### 7-Level Zone Detail

The `zone_detail` field provides finer granularity, splitting the Bull and Cautious zones:

| Score | Zone (5-level) | Zone Detail (7-level) | Exposure Range |
|-------|----------------|----------------------|----------------|
| 80-100 | Strong Bull | Strong Bull | 100% |
| 70-79 | Bull | Bull-Upper | 90-100% |
| 60-69 | Bull | Bull-Lower | 80-90% |
| 40-59 | Neutral | Neutral | 60-80% |
| 30-39 | Cautious | Cautious-Upper | 45-60% |
| 20-29 | Cautious | Cautious-Lower | 30-45% |
| 0-19 | Bear | Bear | 0-30% |

**Why:** The original Bull zone (60-79) was too wide. A score of 66 and 78 both showed "Bull" but warrant different exposure levels. Bull-Lower signals caution compared to Bull-Upper.

### Zone Proximity Indicator

When the composite score falls within 10 points of a zone boundary (20, 40, 60, 80), the `zone_proximity` field flags `at_boundary=True` with the distance and direction. This alerts users that a small score change could shift the zone classification.

---

## Warning System

### Component-Level Warnings

Warnings detect conditions where the composite score may overstate market health:

| Warning | Trigger | Composite Penalty | Rationale |
|---------|---------|-------------------|-----------|
| **Late Cycle** | Commodity avg > both Cyclical and Defensive group averages | -5 | Commodity leadership often precedes broader market weakness |
| **High Spread** | Max-min sector ratio spread > 40pp | -3 | Wide spread indicates narrowing leadership masked by averages |
| **Divergence** | Intra-group std > 8pp, spread > 20pp, or trend dissenters | -3 | Group averages hide internal disagreement (also -5 to Component 3 score) |

### Multi-Warning Discount

When 2 or more warnings are active simultaneously, the total penalty is reduced by 1 point to account for correlation between warning conditions.

**Example:** Late Cycle (-5) + High Spread (-3) = -8 + discount (+1) = **-7 total penalty**

### Warning Impact on Guidance

When warnings are active in Bull or Strong Bull zones:
- Exposure guidance is tightened (e.g., "Normal Exposure, Lower End (80-90%)" instead of "Normal Exposure (80-100%)")
- Guidance text notes the tension between score and warnings
- Warning-specific actions are prepended to recommended actions

The raw score (before penalty) is preserved as `composite_score_raw` for transparency.

---

## Weight Rationale

| Component | Weight | Rationale |
|-----------|--------|-----------|
| Market Breadth | 30% | Most direct measure of market health |
| Sector Participation | 25% | Breadth of sector-level participation is critical for sustainability |
| Momentum | 20% | Direction matters as much as level |
| Sector Rotation | 15% | Rotation signals provide important risk-on/off context |
| Historical Context | 10% | Provides perspective but less actionable than real-time signals |

---

## Limitations

1. **Data History:** "all" data starts from Aug 2023; sector data from Jul 2024. Long-term percentile analysis is limited. The confidence indicator helps quantify this limitation.
2. **Single Source:** Relies entirely on Monty's dashboard (Finviz Elite data); no cross-validation with other breadth measures.
3. **No Volume Data:** Uptrend ratio is price-based only; no volume confirmation.
4. **Lagging Indicator:** 10-day moving average and slope introduce inherent lag. EMA(3) smoothing adds marginal additional lag but reduces noise.
5. **US Only:** Covers US stocks only; no international market breadth.
6. **Sector Classification:** Uses fixed GICS sectors which may not capture all rotation dynamics.
7. **Finviz Dependency:** Upstream data depends on Finviz Elite availability and screener accuracy.

---

## Complementary Analysis

This skill works best when combined with:
- **Market Top Detector:** For distribution day and leadership deterioration signals
- **Technical Analyst:** For index-level chart confirmation
- **Sector Analyst:** For detailed sector rotation analysis
- **Market News Analyst:** For fundamental catalyst context


---

## SKILL: us-market-bubble-detector

- Fuente: `tradermonty/claude-trading-skills` → `examples/weekly-trade-strategy/.claude/skills/us-market-bubble-detector` (MIT)
- Cuándo usarla: Evaluates market bubble risk through quantitative data-driven analysis using the revised Minsky/Kindleberger framework v2.1. Prioritizes objective metrics (Put/Call, VIX, margin debt, breadth, IPO data) over subjective impressions. Features strict qualitative adjustment criteria with confirmation bias prevention. Supports practical investment decisions with mandatory data collection and mechanical scoring. Use when user asks about bubble risk, valuation concerns, or profit-taking timing.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `examples/weekly-trade-strategy/.claude/skills/us-market-bubble-detector/` (bubble_scorer.py)

# US Market Bubble Detection Skill (Revised v2.1)

## Key Revisions in v2.1

**Critical Changes from v2.0:**
1. ✅ **Mandatory Quantitative Data Collection** - Use measured values, not impressions or speculation
2. ✅ **Clear Threshold Settings** - Specific numerical criteria for each indicator
3. ✅ **Two-Phase Evaluation Process** - Quantitative evaluation → Qualitative adjustment (strict order)
4. ✅ **Stricter Qualitative Criteria** - Max +3 points (reduced from +5), requires measurable evidence
5. ✅ **Confirmation Bias Prevention** - Explicit checklist to avoid over-scoring
6. ✅ **Granular Risk Phases** - Added "Elevated Risk" phase (8-9 points) for nuanced risk management

---

## When to Use This Skill

Use this skill when:

**English:**
- User asks "Is the market in a bubble?" or "Are we in a bubble?"
- User seeks advice on profit-taking, new entry timing, or short-selling decisions
- User reports social phenomena (non-investors entering, media frenzy, IPO flood)
- User mentions narratives like "this time is different" or "revolutionary technology" becoming mainstream
- User consults about risk management for existing positions

**Japanese:**
- ユーザーが「今の相場はバブルか?」と尋ねる
- 投資の利確・新規参入・空売りのタイミング判断を求める
- 社会現象(非投資家の参入、メディア過熱、IPO氾濫)を観察し懸念を表明
- 「今回は違う」「革命的技術」などの物語が主流化している状況を報告
- 保有ポジションのリスク管理方法を相談

---

## Evaluation Process (Strict Order)

### Phase 1: Mandatory Quantitative Data Collection

**CRITICAL: Always collect the following data before starting evaluation**

#### 1.1 Market Structure Data (Highest Priority)
```
□ Put/Call Ratio (CBOE Equity P/C)
  - Source: CBOE DataShop or web_search "CBOE put call ratio"
  - Collect: 5-day moving average

□ VIX (Fear Index)
  - Source: Yahoo Finance ^VIX or web_search "VIX current"
  - Collect: Current value + percentile over past 3 months

□ Volatility Indicators
  - 21-day realized volatility
  - Historical position of VIX (determine if in bottom 10th percentile)
```

#### 1.2 Leverage & Positioning Data
```
□ FINRA Margin Debt Balance
  - Source: web_search "FINRA margin debt latest"
  - Collect: Latest month + Year-over-Year % change

□ Breadth (Market Participation)
  - % of S&P 500 stocks above 50-day MA
  - Source: web_search "S&P 500 breadth 50 day moving average"
```

#### 1.3 IPO & New Issuance Data
```
□ IPO Count & First-Day Performance
  - Source: Renaissance Capital IPO or web_search "IPO market 2025"
  - Collect: Quarterly count + median first-day return
```

**⚠️ CRITICAL: Do NOT proceed with evaluation without Phase 1 data collection**

---

### Phase 2: Quantitative Evaluation (Quantitative Scoring)

Score mechanically based on collected data using the following criteria:

#### Indicator 1: Put/Call Ratio (Market Sentiment)
```
Scoring Criteria:
- 2 points: P/C < 0.70 (excessive optimism, call-heavy)
- 1 point: P/C 0.70-0.85 (slightly optimistic)
- 0 points: P/C > 0.85 (healthy caution)

Rationale: P/C < 0.7 is historically characteristic of bubble periods
```

#### Indicator 2: Volatility Suppression + New Highs
```
Scoring Criteria:
- 2 points: VIX < 12 AND major index within 5% of 52-week high
- 1 point: VIX 12-15 AND near highs
- 0 points: VIX > 15 OR more than 10% from highs

Rationale: Extreme low volatility + highs indicates excessive complacency
```

#### Indicator 3: Leverage (Margin Debt Balance)
```
Scoring Criteria:
- 2 points: YoY +20% or more AND all-time high
- 1 point: YoY +10-20%
- 0 points: YoY +10% or less OR negative

Rationale: Rapid leverage increase is a bubble precursor
```

#### Indicator 4: IPO Market Overheating
```
Scoring Criteria:
- 2 points: Quarterly IPO count > 2x 5-year average AND median first-day return +20%+
- 1 point: Quarterly IPO count > 1.5x 5-year average
- 0 points: Normal levels

Rationale: Poor-quality IPO flood is characteristic of late-stage bubbles
```

#### Indicator 5: Breadth Anomaly (Narrow Leadership)
```
Scoring Criteria:
- 2 points: New high AND < 45% of stocks above 50DMA (narrow leadership)
- 1 point: 45-60% above 50DMA (somewhat narrow)
- 0 points: > 60% above 50DMA (healthy breadth)

Rationale: Rally driven by few stocks is fragile
```

#### Indicator 6: Price Acceleration
```
Scoring Criteria:
- 2 points: Past 3-month return exceeds 95th percentile of past 10 years
- 1 point: Past 3-month return in 85-95th percentile of past 10 years
- 0 points: Below 85th percentile

Rationale: Rapid price acceleration is unsustainable
```

---

### Phase 3: Qualitative Adjustment (REVISED v2.1)

**Limit: +3 points maximum (REDUCED from +5 in v2.0)**

**⚠️ CONFIRMATION BIAS PREVENTION CHECKLIST:**
```
Before adding ANY qualitative points:
□ Do I have concrete, measurable data? (not impressions)
□ Would an independent observer reach the same conclusion?
□ Am I avoiding double-counting with Phase 2 scores?
□ Have I documented specific evidence with sources?
```

#### Adjustment A: Social Penetration (0-1 points, STRICT CRITERIA)
```
+1 point: ALL THREE criteria must be met:
  ✓ Direct user report of non-investor recommendations
  ✓ Specific examples with names/dates/conversations
  ✓ Multiple independent sources (minimum 3)

+0 points: Any criteria missing

⚠️ INVALID EXAMPLES:
- "AI narrative is prevalent" (unmeasurable)
- "I saw articles about retail investors" (not direct report)
- "Everyone is talking about stocks" (vague, unverified)

✅ VALID EXAMPLE:
"My barber asked about NVDA (Nov 1), dentist mentioned AI stocks (Nov 2),
Uber driver discussed crypto (Nov 3)"
```

#### Adjustment B: Media/Search Trends (0-1 points, REQUIRES MEASUREMENT)
```
+1 point: BOTH criteria must be met:
  ✓ Google Trends showing 5x+ YoY increase (measured)
  ✓ Mainstream coverage confirmed (Time covers, TV specials with dates)

+0 points: Search trends <5x OR no mainstream coverage

⚠️ CRITICAL: "Elevated narrative" without data = +0 points

HOW TO VERIFY:
1. Search "[topic] Google Trends 2025" and document numbers
2. Search "[topic] Time magazine cover" for specific dates
3. Search "[topic] CNBC special" for episode confirmation

✅ VALID EXAMPLE:
"Google Trends: 'AI stocks' at 780 (baseline 150 = 5.2x).
Time cover 'AI Revolution' (Oct 15, 2025).
CNBC 'AI Investment Special' (3 episodes Oct 2025)."

⚠️ INVALID EXAMPLE:
"AI/technology narrative seems elevated" (unmeasurable)
```

#### Adjustment C: Valuation Disconnect (0-1 points, AVOID DOUBLE-COUNTING)
```
+1 point: ALL criteria must be met:
  ✓ P/E >25 (if NOT already counted in Phase 2 quantitative)
  ✓ Fundamentals explicitly ignored in mainstream discourse
  ✓ "This time is different" documented in major media

+0 points: P/E <25 OR fundamentals support valuations

⚠️ SELF-CHECK QUESTIONS (if ANY is YES, score = 0):
- Is P/E already in Phase 2 quantitative scoring?
- Do companies have real earnings supporting valuations?
- Is the narrative backed by fundamental improvements?

✅ VALID EXAMPLE for +1:
"S&P P/E = 35x (vs historical 18x).
CNBC article: 'Earnings don't matter in AI era' (Oct 2025).
Bloomberg: 'Traditional metrics obsolete' (Nov 2025)."

⚠️ INVALID EXAMPLE:
"P/E 30.8 but companies have real earnings and AI has fundamental backing"
(fundamentals support = +0 points)
```

**Phase 3 Total: Maximum +3 points**

---

### Phase 4: Final Judgment (REVISED v2.1)

```
Final Score = Phase 2 Total (0-12 points) + Phase 3 Adjustment (0 to +3 points)
Range: 0 to 15 points

Judgment Criteria (with Risk Budget):
- 0-4 points: Normal (Risk Budget: 100%)
- 5-7 points: Caution (Risk Budget: 70-80%)
- 8-9 points: Elevated Risk (Risk Budget: 50-70%) ⚠️ NEW in v2.1
- 10-12 points: Euphoria (Risk Budget: 40-50%)
- 13-15 points: Critical (Risk Budget: 20-30%)
```

**Key Change in v2.1:**
- Added "Elevated Risk" phase (8-9 points) for more nuanced positioning
- 9 points is no longer extreme defensive zone (was 40% risk budget)
- Now allows 50-70% risk budget at 8-9 point level
- More gradual transition from Caution to Euphoria phases

---

## Data Sources (Required)

### US Market
- **Put/Call**: https://www.cboe.com/tradable_products/vix/
- **VIX**: Yahoo Finance (^VIX) or https://www.cboe.com/
- **Margin Debt**: https://www.finra.org/investors/learn-to-invest/advanced-investing/margin-statistics
- **Breadth**: https://www.barchart.com/stocks/indices/sp/sp500?viewName=advanced
- **IPO**: https://www.renaissancecapital.com/IPO-Center/Stats

### Japanese Market
- **Nikkei Futures P/C**: https://www.barchart.com/futures/quotes/NO*0/options
- **JNIVE**: https://www.investing.com/indices/nikkei-volatility-historical-data
- **Margin Debt**: JSF (Japan Securities Finance) Monthly Report
- **Breadth**: https://en.macromicro.me/series/31841/japan-topix-index-200ma-breadth
- **IPO**: https://www.pwc.co.uk/services/audit/insights/global-ipo-watch.html

---

## Implementation Checklist

Verify the following when using:

```
□ Have you collected all Phase 1 data?
□ Did you apply each indicator's threshold mechanically?
□ Did you keep qualitative evaluation within +5 point limit?
□ Are you NOT assigning points based on news article impressions?
□ Does your final score align with other quantitative frameworks?
```

---

## Important Principles (Revised)

### 1. Data > Impressions
Ignore "many news reports" or "experts are cautious" without quantitative data.

### 2. Strict Order: Quantitative → Qualitative
Always evaluate in this order: Phase 1 (Data Collection) → Phase 2 (Quantitative) → Phase 3 (Qualitative Adjustment).

### 3. Upper Limit on Subjective Indicators
Qualitative adjustment has a total limit of +5 points. It cannot override quantitative evaluation.

### 4. "Taxi Driver" is Symbolic
Do not readily acknowledge mass penetration without direct recommendations from non-investors.

---

## Common Failures and Solutions (Revised)

### Failure 1: Evaluating Based on News Articles
❌ "Many reports on Takaichi Trade" → Media saturation 2 points
✅ Verify Google Trends numbers → Evaluate with measured values

### Failure 2: Overreaction to Expert Comments
❌ "Warning of overheating" → Euphoria zone
✅ Judge with measured values of Put/Call, VIX, margin debt

### Failure 3: Emotional Reaction to Price Rise
❌ 4.5% rise in 1 day → Price acceleration 2 points
✅ Verify position in 10-year distribution → Objective evaluation

### Failure 4: Judgment Based on Valuation Alone
❌ P/E 17 → Valuation disconnect 2 points
✅ P/E + narrative dependence + other quantitative indicators for comprehensive judgment

---

## Recommended Actions by Bubble Stage (REVISED v2.1)

### Normal (0-4 points)
**Risk Budget: 100%**
- Continue normal investment strategy
- Set ATR 2.0× trailing stop
- Apply stair-step profit-taking rule (+20% take 25%)

**Short-Selling: Not Allowed**
- Composite conditions not met (0/7 items)

### Caution (5-7 points)
**Risk Budget: 70-80%**
- Begin partial profit-taking (20-30% reduction)
- Tighten ATR to 1.8×
- Reduce new position sizing by 50%

**Short-Selling: Not Recommended**
- Wait for clearer reversal signals

### Elevated Risk (8-9 points) ⚠️ NEW in v2.1
**Risk Budget: 50-70%**
- Increase profit-taking (30-50% reduction)
- Tighten ATR to 1.6×
- New positions: highly selective, quality only
- Begin building cash reserves for future opportunities

**Short-Selling: Consider Cautiously**
- Only after confirming at least 2/7 composite conditions
- Small exploratory positions (10-15% of normal size)
- Strict stop-loss (ATR 2.0×)

**Rationale for NEW phase:**
This zone represents heightened caution without extreme defensiveness.
Market shows warning signs but not imminent collapse.
Maintain exposure to quality positions while building flexibility.

### Euphoria (10-12 points)
**Risk Budget: 40-50%**
- Accelerate stair-step profit-taking (50-60% reduction)
- Tighten ATR to 1.5×
- No new long positions except on major pullbacks

**Short-Selling: Active Consideration**
- After confirming at least 3/7 composite conditions
- Small positions (20-25% of normal size)
- Defined risk only (options, tight stops)

### Critical (13-15 points)
**Risk Budget: 20-30%**
- Major profit-taking or full hedge implementation
- ATR 1.2× or fixed stop-loss
- Cash preservation mode - prepare for major dislocation

**Short-Selling: Recommended**
- After confirming at least 5/7 composite conditions
- Scale in with small positions, pyramid on confirmation
- Tight stop-loss (ATR 1.5× or higher)
- Consider put options for defined risk

---

## Composite Conditions for Short-Selling (7 Items)

Only consider shorts after confirming at least 3 of the following:

```
1. Weekly chart shows lower highs
2. Volume peaks out
3. Leverage indicators drop sharply (margin debt decline)
4. Media/search trends peak out
5. Weak stocks start to break down first
6. VIX surges (spike above 20)
7. Fed/policy shift signals
```

---

## Output Format

### Evaluation Report Structure (v2.1)

```markdown
# [Market Name] Bubble Evaluation Report (Revised v2.1)

## Overall Assessment
- Final Score: X/15 points (v2.1: max reduced from 16)
- Phase: [Normal/Caution/Elevated Risk/Euphoria/Critical]
- Risk Level: [Low/Medium/Medium-High/High/Extremely High]
- Evaluation Date: YYYY-MM-DD

## Quantitative Evaluation (Phase 2)

| Indicator | Measured Value | Score | Rationale |
|-----------|----------------|-------|-----------|
| Put/Call | [value] | [0-2] | [reason] |
| VIX + Highs | [value] | [0-2] | [reason] |
| Margin YoY | [value] | [0-2] | [reason] |
| IPO Heat | [value] | [0-2] | [reason] |
| Breadth | [value] | [0-2] | [reason] |
| Price Accel | [value] | [0-2] | [reason] |

**Phase 2 Total: X/12 points**

## Qualitative Adjustment (Phase 3) - STRICT CRITERIA

**⚠️ Confirmation Bias Check:**
- [ ] All qualitative points have measurable evidence
- [ ] No double-counting with Phase 2
- [ ] Independent observer would agree

### A. Social Penetration (0-1 points)
- Evidence: [REQUIRED: Direct user reports with dates/names]
- Score: [+0 or +1]
- Justification: [Must meet ALL three criteria]

### B. Media/Search Trends (0-1 points)
- Google Trends Data: [REQUIRED: Measured numbers, YoY multiplier]
- Mainstream Coverage: [REQUIRED: Specific Time covers, TV specials with dates]
- Score: [+0 or +1]
- Justification: [Must have 5x+ search AND mainstream confirmation]

### C. Valuation Disconnect (0-1 points)
- P/E Ratio: [Current value]
- Fundamental Backing: [Yes/No - if Yes, score = 0]
- Narrative Analysis: [REQUIRED: Specific media quotes ignoring fundamentals]
- Score: [+0 or +1]
- Justification: [Must show fundamentals actively ignored]

**Phase 3 Total: +X/3 points (max reduced from +5 in v2.0)**

## Recommended Actions

**Risk Budget: X%** (Phase: [Normal/Caution/Elevated Risk/Euphoria/Critical])
- [Specific action 1]
- [Specific action 2]
- [Specific action 3]

**Short-Selling: [Not Allowed/Consider Cautiously/Active/Recommended]**
- Composite conditions: X/7 met
- Minimum required: [0/2/3/5] for current phase

## Key Changes in v2.1
- Stricter qualitative criteria (max +3, down from +5)
- Added "Elevated Risk" phase for 8-9 points
- Confirmation bias prevention checklist
- All qualitative points require measurable evidence
```

---

## Reference Documents

### `references/implementation_guide.md` (English) - **RECOMMENDED FOR FIRST USE**
- Step-by-step evaluation process with mandatory data collection
- NG examples vs OK examples
- Self-check quality criteria (4 levels)
- Red flags during review
- Best practices for objective evaluation

### `references/bubble_framework.md` (Japanese)
- Detailed theoretical framework
- Explanation of Minsky/Kindleberger model
- Behavioral psychology elements

### `references/historical_cases.md` (Japanese)
- Analysis of past bubble cases
- Dotcom, Crypto, Pandemic bubbles
- Common pattern extraction

### `references/quick_reference.md` (Japanese)
### `references/quick_reference_en.md` (English)
- Daily checklist
- Emergency 3-question assessment
- Quick scoring guide
- Key data sources

### When to Load References
- **First use or need detailed guidance:** Load `implementation_guide.md`
- **Need theoretical background:** Load `bubble_framework.md`
- **Need historical context:** Load `historical_cases.md`
- **Daily operations:** Load `quick_reference.md` (Japanese) or `quick_reference_en.md` (English)

---

## Summary: Essence of v2.1 Revision

**v2.0 Problem (Identified Nov 2025):**
- Qualitative adjustment too loose (+5 max)
- "AI narrative elevated" → +1 point (no data)
- "P/E 30.8" → +1 point (double-counting with quantitative)
- **Result: 11/16 points - overly bearish without evidence**

**v2.1 Solution:**
- Qualitative adjustment stricter (+3 max)
- "AI narrative elevated" → 0 points (unmeasured)
- "P/E 30.8 but AI has fundamental backing" → 0 points (fundamentals support)
- **Result: 9/15 points - balanced, data-driven assessment**

**Key Improvements:**
1. **Confirmation Bias Prevention**: Explicit checklist before adding qualitative points
2. **Measurable Evidence Required**: No points without concrete data (Google Trends, media coverage)
3. **Double-Counting Prevention**: Valuation must not duplicate Phase 2 quantitative
4. **Granular Risk Phases**: Added "Elevated Risk" (8-9 points) for nuanced positioning
5. **Balanced Risk Budgets**: 9 points = 50-70% (not 40% extreme defensive)

**Core Principle:**
> "In God we trust; all others must bring data." - W. Edwards Deming

**2025 Lesson:**
Even data-driven frameworks can be undermined by subjective qualitative adjustments.
v2.1 requires MEASURABLE evidence for ALL qualitative points.
Independent observers must be able to verify each adjustment.

---

**Version History:**
- **v2.0** (Oct 27, 2025): Mandatory quantitative data collection
- **v2.1** (Nov 3, 2025): Stricter qualitative criteria, confirmation bias prevention, granular risk phases

**Reason for v2.1 Revision:**
Prevent over-scoring through unmeasured "narrative" assessments and double-counting.
Ensure all bubble risk evaluations are independently verifiable and free from confirmation bias.

### Referencia: CHANGELOG.md

# US Market Bubble Detector - Changelog

## Version 2.1 (November 3, 2025)

### Critical Issue Fixed
**Problem Identified:** v2.0 allowed excessive qualitative adjustments based on unmeasured "narratives" and subjective impressions, leading to inflated bubble risk scores.

**Example Case (Nov 3, 2025):**
- Quantitative Score (Phase 2): 9 points (objective, data-driven)
- Qualitative Adjustment (v2.0): +2 points
  - Media Narrative: +1 (based on "elevated AI narrative" - NO DATA)
  - Valuation: +1 (P/E 30.8 - DOUBLE COUNTED, ignored fundamental backing)
- **Result**: 11/16 points → Euphoria phase → 40% risk budget (overly defensive)

**Root Cause:** Confirmation bias - analyst had bearish conclusion first, then adjusted qualitative points to match expectation.

### Changes in v2.1

#### 1. Stricter Qualitative Criteria (MAX +3, down from +5)

**A. Social Penetration (0-1 points)**
- **v2.0**: Loose criteria, "general awareness" acceptable
- **v2.1**: ALL three required:
  - Direct user report of non-investor recommendations
  - Specific examples with dates/names
  - Multiple independent sources (minimum 3)

**B. Media/Search Trends (0-1 points)**
- **v2.0**: Subjective "many reports" acceptable
- **v2.1**: BOTH required:
  - Google Trends 5x+ YoY (measured data)
  - Mainstream coverage confirmed (Time covers, TV specials with dates)
- **Critical**: "Elevated narrative" without data = 0 points

**C. Valuation Disconnect (0-1 points)**
- **v2.0**: P/E >25 alone sufficient
- **v2.1**: ALL required AND avoid double-counting:
  - P/E >25 (if NOT in Phase 2)
  - Fundamentals explicitly ignored in discourse
  - "This time is different" documented in major media
- **Self-check**: If companies have real earnings supporting valuations → 0 points

#### 2. Confirmation Bias Prevention

New mandatory checklist before adding ANY qualitative points:
```
□ Do I have concrete, measurable data? (not impressions)
□ Would an independent observer reach the same conclusion?
□ Am I avoiding double-counting with Phase 2 scores?
□ Have I documented specific evidence with sources?
```

#### 3. Granular Risk Phases

**New "Elevated Risk" Phase (8-9 points)**
- **v2.0**: 9 points = Euphoria = 40% risk budget (extreme defensive)
- **v2.1**: 9 points = Elevated Risk = 50-70% risk budget (balanced caution)

**Updated Risk Budget Matrix:**
| Score | Phase | v2.0 Risk Budget | v2.1 Risk Budget | Change |
|-------|-------|------------------|------------------|--------|
| 0-4 | Normal | 100% | 100% | - |
| 5-7 | Caution | 70% | 70-80% | More flexible |
| 8-9 | Elevated Risk | 40% (Euphoria) | 50-70% | **NEW PHASE** |
| 10-12 | Euphoria | 40% | 40-50% | More balanced |
| 13-15 | Critical | 20% | 20-30% | Reduced max |

#### 4. Maximum Score Reduction

- **v2.0**: 0-16 points (Phase 2: 12, Phase 3: -1 to +5)
- **v2.1**: 0-15 points (Phase 2: 12, Phase 3: 0 to +3)

### Impact on Nov 3, 2025 Analysis

**Under v2.0:**
- Score: 11/16 → Euphoria phase
- Risk Budget: 40%
- Positioning: Extreme defensive

**Under v2.1 (corrected):**
- Quantitative: 9/12 (unchanged, data-driven)
- Qualitative:
  - Media Narrative: 0 points (no Google Trends data)
  - Valuation: 0 points (AI has fundamental backing, double-counting)
- **Score: 9/15 → Elevated Risk phase**
- **Risk Budget: 50-70%**
- **Positioning: Cautious but not extreme**

### Key Learnings

1. **Data > Impressions**: "Elevated narrative" is not measurable evidence
2. **Avoid Double-Counting**: Valuation in Phase 2 quantitative ≠ add again in Phase 3
3. **Check Internal Consistency**: If report admits "AI has fundamental backing," then valuation disconnect score must be 0
4. **Independent Verification**: All qualitative points must be verifiable by independent observers

### Documentation Updates

- `SKILL.md`: Updated to v2.1 with strict criteria
- `references/implementation_guide.md`: Enhanced Phase 3 with bias prevention checklist
- `references/quick_reference.md`: Updated action matrix with new Elevated Risk phase
- `references/bubble_framework.md`: Updated risk budget table

---

## Version 2.0 (October 27, 2025)

### Initial Major Revision
- Introduced mandatory quantitative data collection
- Eliminated reliance on impressions and speculation
- Established clear threshold settings for each indicator
- Two-phase evaluation process: Quantitative → Qualitative

---

**Version Control:**
- v1.x: Original framework (deprecated)
- v2.0: Data-driven quantitative focus
- v2.1: Strict qualitative criteria + confirmation bias prevention

### Referencia: references/bubble_framework.md

# Detailed Bubble Theory Framework

## Table of Contents
1. [Core Concept](#core-concept)
2. [Minsky/Kindleberger Model](#minskykindleberger-model)
3. [Behavioral Psychology Elements](#behavioral-psychology-elements)
4. [Quantitative Indicators for Detection](#quantitative-indicators-for-detection)
5. [Practical Response Strategies](#practical-response-strategies)

---

## Core Concept

### The Essence of Bubbles: Social Norm Inversion Through Social Contagion

True bubbles are determined not by **price levels** but by **the phase of crowd psychology**.

#### Core Characteristics

1. **Critical Information Cascade**
   - Spread to all layers (including non-investors) is complete
   - FOMO (Fear of Missing Out) becomes social norm
   - Social cost of being skeptical is maximized

2. **Social Calculation Inversion**
   ```
   Normal state: Conformity pressure < Value of independent judgment
   Bubble state: Conformity pressure > Value of independent judgment
   ```
   Completion is near when "pain of not conforming < pain of holding contrarian views"

3. **Institutionalized Confirmation Bias**
   - Media, experts, and laypeople repeat the same narrative
   - Counterevidence is ignored or excluded
   - "This time is different" becomes the mantra

### Signal Example: Taxi Driver Investment Talk

Modern version of Joe Kennedy selling before the 1929 crash after hearing a shoeshine boy talk stocks.

**Why this is a decisive signal:**
- Information reaches the final tier = cascade complete
- "Last buyer" cohort enters = demand exhaustion near
- "Sure to profit" perception without expertise = peak risk ignorance

---

## Minsky/Kindleberger Model

5-stage bubble progression model (Hyman Minsky / Charles Kindleberger)

### 1. Displacement (Trigger)

**Characteristics:**
- Structural changes like new technology, institutional reform, monetary easing
- Legitimate investment opportunities emerge
- Rational price rises

**Real Examples:**
- 1990s: Internet revolution
- 2010s: Mobile/cloud
- 2020-21: Pandemic-response ultra-easing + remote work technology

### 2. Boom (Expansion)

**Characteristics:**
- Self-reinforcing loop: price rise → media exposure → new participants → liquidity expansion
- Positive expert views increase
- Valuations high but "explainable by growth expectations"

**Psychology:**
- Availability bias: Success stories dominate
- Herding: Even institutional investors feel pressure to join

**Detection Indicators:**
- Sustained trading volume increase
- Accelerating new account openings
- Annual returns in 75-90th percentile

### 3. Euphoria (Exuberance)

**Characteristics:**
- Narrative becomes "common sense," dissent labeled "outdated"
- Leverage increases (margin trading, futures, derivatives)
- New issuances proliferate (IPO/ICO/SPAC)
- Even low-quality stocks rally

**Psychology:**
- Overconfidence: "I'm special"
- Confirmation bias: Accept only favorable information
- Regret aversion: Overly fear "missing gains after selling"

**Detection Indicators:**
- VIX falls (risk dismissal)
- Extreme Put/Call ratio bias
- Margin balances at all-time highs
- Proliferation of "XX-related" products

### 4. Profit Taking (Exit Begins)

**Characteristics:**
- Early participants (smart money) begin taking profits
- But crowd continues chasing with FOMO
- Volatility (price fluctuation) increases

**Psychological Divergence:**
- Smart money: Loss aversion (prioritize securing gains)
- Crowd: FOMO peaks ("don't miss out")

**Detection Indicators:**
- Volume surges + increased price swings
- Insider selling increases
- Short interest rises (sophisticated skepticism)

### 5. Panic (Reversal)

**Characteristics:**
- Objective confirmation of trend breakdown (failure to make new highs, MA breaks)
- Forced liquidations → liquidation cascade
- Liquidity evaporates

**Psychology:**
- Loss aversion reverses: "don't want to realize loss" → "must avoid further loss by panic selling"
- Herding reverses: buying crowd → selling crowd

**Detection Indicators:**
- Circuit breakers triggered
- Chain of margin calls
- Mark-to-market losses at all-time worst levels

---

## Behavioral Psychology Elements

### 1. FOMO (Fear of Missing Out)

**Mechanism:**
- Social proof: "Everyone's buying → must be right"
- Regret aversion: "regret of missing out" > "regret of losing money"

**Bubble Condition:**
FOMO elevates from individual psychology to **social norm** → non-conformity becomes professional/social risk

### 2. Confirmation Bias

**Bubble-Period Amplification:**
- Media echo chambers
- Social media algorithm filter bubbles
- Expert conformity pressure (contrarianism = career risk)

### 3. Overconfidence

**Bubble-Period Characteristics:**
- "Only I can sell at the top"
- "This time is different"
- Risk management neglect

### 4. Dangerous Combination: Loss Aversion × Regret Aversion

**Most Dangerous Phase:**
Investors who experienced "rapid rise after early profit-taking"

1. Take profit → price rises further → regret
2. Re-enter → buy high → can't cut loss due to loss aversion
3. Further rise → illusion of being "right" reinforces
4. Miss exit when reversal comes

---

## Quantitative Indicators for Detection

### Category 1: Social Penetration

| Indicator | Data Source | Alert Threshold |
|-----------|------------|----------------|
| Google Search Trends | Google Trends API | 5x+ normal |
| Social Media Mentions | Twitter/Reddit API | z-score > +3 |
| New Account Openings | Brokerage data | 200%+ YoY |
| Media Coverage | News APIs | Weekly article count 10x normal |

### Category 2: Price Dynamics

| Indicator | Calculation | Alert Threshold |
|-----------|------------|----------------|
| Annualized Return | Annualize 90-day return | Exceeds 95th percentile |
| Price Acceleration | 2nd derivative sign and magnitude | Positive and increasing |
| Volatility Skew | Put/Call ratio | < 0.5 (extreme optimism) |
| Distance from 52W High | (Current - 52W High) / 52W High | Within -5%, clustering |

### Category 3: Leverage & Positioning

| Indicator | Data Source | Alert Threshold |
|-----------|------------|----------------|
| Margin Balance | FINRA | All-time high |
| Mark-to-Market P&L | Exchange data | Extreme unrealized gains (reversal risk) |
| Futures Positioning | CFTC COT | Speculators extremely long |
| Funding Rate | Crypto exchanges | 50%+ annual sustained |

### Category 4: New Issuance & Entry

| Indicator | Data Source | Alert Threshold |
|-----------|------------|----------------|
| IPO Count | Renaissance IPO Index | 100%+ YoY |
| SPAC Formation | SPAC statistics | 100+ per quarter |
| Theme ETF Launches | ETF.com | 5+ "XX-related" per month |

### Category 5: Valuation

| Indicator | Calculation | Alert Threshold |
|-----------|------------|----------------|
| Shiller CAPE | P/E using 10-year real earnings average | >30 (historically high) |
| Buffett Indicator | Market cap / GDP | >150% (overheating) |
| Sector Divergence | Top sector vs bottom sector P/E difference | 3x+ gap |

---

## Practical Response Strategies

### Offense: Profit-Taking Strategy

#### 1. Mechanical Stair-Step Profit-Taking

```
Target Return    Profit %    Remaining Position
+20%             25%         75%
+40%             25%         50%
+60%             25%         25%
+80%             25%         0%
```

**Benefits:**
- Eliminates psychological pressure
- Mitigates "post-sale rise" regret
- Guarantees partial profit capture

#### 2. Time-Diversified Exit

**NG Pattern:**
Concentrate profit-taking on specific events (earnings, product launch, index inclusion)

**Recommended:**
- Sell 10% daily over 2 weeks
- Distribute before/during/after events

#### 3. Trailing Stop (Volatility-Adjusted)

```python
stop_price = current_price - (ATR × coefficient)
# ATR: Average True Range (20-day average fluctuation)
# Coefficient: 2.0 (normal), 1.5 (bubble zone, tightened)
```

### Defense: Risk Management

#### 1. Pre-Determined Drawdown Tolerance

```
Expected Max DD    Position Size
-10%               100% (full position)
-20%               50%
-30%               33%
-40%               25%
```

#### 2. Risk Budget by Bubble Stage (REVISED v2.1)

| Bubble Stage | Score | Total Risk Budget | New Entry | Stop Coefficient |
|-------------|-------|------------------|-----------|-----------------|
| Normal | 0-4 | 100% | Normal | 2.0 ATR |
| Caution | 5-7 | 70-80% | 50% reduced | 1.8 ATR |
| Elevated Risk | 8-9 | 50-70% | Selective | 1.6 ATR |
| Euphoria | 10-12 | 40-50% | Stop | 1.5 ATR |
| Critical | 13-15 | 20-30% | Stop | 1.2 ATR |

**Key Changes in v2.1:**
- Added "Elevated Risk" phase (8-9 points) for more granular risk management
- Adjusted risk budgets to be less extreme at 9-point level
- Maximum score reduced to 15 (Phase 2: 12 max, Phase 3: 3 max with strict criteria)

#### 3. Short-Selling Timing (Critical)

**NG Pattern:**
- Early shorts based on subjective "too high"
- Bubbles "last longer than expected" ("Markets can remain irrational longer than you can remain solvent")

**Recommended Conditions (Composite):**
1. Weekly chart shows clear lower highs
2. Volume peaks out (enters declining trend)
3. Funding rate drops sharply (crypto) / margin balance declines (stocks)
4. Media/search trends peak out
5. Weak stocks within sector start breaking down first

Consider starting when minimum 3 conditions met.

#### 4. Separate Cash Accounts

- **Long-term investment account**: Buy & hold, dividend reinvestment, rebalancing only
- **Trading account**: Short-term trading, bubble profit-taking, reversal shorts

**Purpose:** Prevent decision confusion, maintain psychological stability

### Practical Daily Checklist

Check every morning before market open:

- [ ] Update Bubble-O-Meter (score 8 indicators)
- [ ] Update ATR trailing stops for held positions
- [ ] Verify planned new entries are appropriate given bubble stage
- [ ] Check for sudden media/social media trend changes
- [ ] Confirm major indices' distance from 52-week highs
- [ ] Check leverage indicators (margin balance, funding rate)
- [ ] Check VIX level and Put/Call ratio
- [ ] Check sector breadth (broad rally or selective)

---

## Summary: Golden Rules for Practice

1. **"See process, not price"**
   Evaluate bubbles not by levels but by crowd psychology phase transitions

2. **"When taxi drivers talk stocks, exit"**
   Last buyer cohort entry = demand exhaustion near

3. **"'This time is different' is always the same"**
   When "This time is different" becomes the mantra, be very cautious

4. **"Mechanical rules protect psychology"**
   When conformity pressure peaks, strict adherence to pre-determined rules is lifeline

5. **"Short after confirmation, take profits early"**
   Bubble collapses come late but suddenly. Contrarian shorts dangerous. Profits mechanically.

6. **"When skepticism hurts, the end begins"**
   The moment social cost exceeds independent judgment is the critical point

### Referencia: references/historical_cases.md

# Historical Bubble Cases and Pattern Analysis

## Table of Contents
1. [Late 1990s: Dotcom Bubble](#dotcom-bubble)
2. [Late 2017: Crypto Bubble](#crypto-bubble)
3. [2020-21: Pandemic Bubble Complex](#pandemic-bubble)
4. [Common Patterns and Lessons](#common-patterns)

---

## Dotcom Bubble (1995-2000)

### Timeline

**1995-1997: Displacement (Trigger)**
- Netscape IPO (August 1995): More than doubled on first day
- Internet penetration: US 5% → 20%
- Legitimate technological innovation and investment opportunities

**1998-Early 1999: Boom (Expansion)**
- NASDAQ 100: Sustained +40% annual growth
- Adding ".com" to name alone drove stock prices up ("the .com effect")
- IPO first-day returns averaged +70%

**Late 1999-March 2000: Euphoria (Exuberance)**
- "Old Economy vs New Economy" binary opposition
- "Clicks vs Bricks" (online is invincible)
- Valuation metrics ignored: "P/E is outdated"

**March 10, 2000: Peak (NASDAQ 5,048.62)**

**March 2000-October 2002: Panic & Crash**
- NASDAQ: -78% (5,048 → 1,114)
- Many bankruptcies: Pets.com, Webvan, eToys, etc.

### Bubble-O-Meter Score Estimate (March 2000)

| Indicator | Score | Rationale |
|-----------|-------|-----------|
| Mass Penetration | 2 | Family/friends entering "day trading" |
| Media Saturation | 2 | Time magazine cover "Amazon.com", CNBC ratings surge |
| New Entrants | 2 | Online brokerage accounts +300% YoY |
| Issuance Flood | 2 | 457 IPOs (1999), many low-quality |
| Leverage | 1 | Margin trading increased, but not to mortgage levels |
| Price Acceleration | 2 | NASDAQ +85% annual (1999) |
| Valuation Disconnect | 2 | "Profits unnecessary, only revenue growth matters" |
| Correlation & Breadth | 2 | Even unprofitable companies rallying, no quality selection |

**Total: 15/16 points (Critical Zone)**

### Lessons

1. **The Magic of the ".com" Suffix**
   Name change alone drove +50%+ stock price gains (e.g., Zapata → Zap.com)

2. **IPO Mania Danger**
   First-day returns of +100%+ becoming normal = abnormal demand overheating

3. **"Growth Without Profits" Limits**
   Many "Get Big Fast" strategies failed, ignoring cash flow consequences

4. **Fed Rate Hikes as Trigger**
   Consecutive rate hikes 1999-2000 → funding cost rise → valuation justification impossible

---

## Crypto Bubble (2017)

### Timeline

**2016-Early 2017: Displacement & Boom**
- Bitcoin: $1,000 → $3,000 (June 2017)
- Emergence of ICO (Initial Coin Offering)
- Rise of altcoins like Ethereum, Ripple

**August-November 2017: Accelerating Boom**
- Bitcoin: $3,000 → $10,000
- Coinbase app #1 on US App Store
- "Blockchain revolution" narrative spreads

**December 2017: Euphoria Peak**
- Bitcoin: $10,000 → $19,783 (December 17 peak)
- **Taxi drivers preaching crypto** (iconic episode from text)
- University lectures producing "instant experts"
- Family gatherings dominated by investment talk

**December 18, 2017-December 2018: Crash**
- Bitcoin: $19,783 → $3,200 (-84%)
- ICO scams exposed, regulatory crackdown

### Bubble-O-Meter Score Estimate (Mid-December 2017)

| Indicator | Score | Rationale |
|-----------|-------|-----------|
| Mass Penetration | 2 | Taxi drivers, grandparents asserting "must buy" |
| Media Saturation | 2 | Google searches for "Bitcoin" at all-time high, daily CNBC specials |
| New Entrants | 2 | Coinbase new accounts exceeding 300k/day |
| Issuance Flood | 2 | 966 ICOs (2017), majority fraudulent |
| Leverage | 2 | 100x leverage trading on BitMEX etc. surging |
| Price Acceleration | 2 | Doubled in one month ($10k→$20k), acceleration positive and increasing |
| Valuation Disconnect | 2 | "Digital gold," "end of fiat currency" narratives dominant |
| Correlation & Breadth | 2 | Even obscure altcoins +1000%+ |

**Total: 16/16 points (Critical Zone - Perfect Score)**

### Lessons

1. **"Most Dangerous Phase: Rapid Rise After Selling"**
   Example from text: Took profit at $8k→$13k → 10 days later approaching $20k → regret and re-entry impulse

2. **Leverage Destructive Power**
   100x leverage = total loss on 5% adverse move, liquidation cascade accelerates crash

3. **ICO Scam Proliferation**
   Raised billions with only whitepapers → many absconded

4. **Regulatory Risk Underestimation**
   "Impossible to regulate" narrative → collapse when China/Korea closed exchanges

---

## Pandemic Bubble (2020-2021)

### Timeline

**March-June 2020: Displacement**
- COVID-19 panic → historic monetary easing
- Fed asset purchases, zero rates, fiscal support
- "TINA" (There Is No Alternative): No investment alternative to stocks

**July 2020-Early 2021: Boom**
- NASDAQ 100: +50% (2020 full year)
- Work-from-home/DX stocks lead (Zoom, Peloton, Shopify)
- Robinhood account openings surge, "Stonks" meme culture

**Early 2021: Euphoria**
- Meme stocks (GME, AMC) wild swings
- SPAC boom (Q1 2021: 298 formations)
- NFT mania (Beeple artwork $69M, "Bored Ape" etc.)
- Crypto resurgence (BTC $64k, "DeFi Summer")

**November 2021: Peak (NASDAQ 16,057)**

**2022: Reversal**
- Fed hawkish pivot (inflation response)
- Interest rate rises → growth stock plunge
- NASDAQ: -33% (2022 full year)
- Crypto bubble collapse (Luna, FTX failures)

### Bubble-O-Meter Score Estimate (November 2021)

| Indicator | Score | Rationale |
|-----------|-------|-----------|
| Mass Penetration | 2 | WallStreetBets, TikTok investment influencers proliferating |
| Media Saturation | 2 | CNBC ratings surge, housewife investment specials |
| New Entrants | 2 | Young demographic accounts 3x on Robinhood etc. |
| Issuance Flood | 2 | 613 SPACs (2021 full year), many low-quality |
| Leverage | 1 | Individual options trading surged, but not excessive mortgage levels |
| Price Acceleration | 2 | Numerous growth stocks +100%+ annual |
| Valuation Disconnect | 2 | Extreme DCF assuming "zero discount rate," profit ignored |
| Correlation & Breadth | 1 | Concentrated in FAANG etc., not broad rally |

**Total: 14/16 points (Critical Zone)**

### Special Factors

1. **Composite Bubble**
   Stocks, crypto, NFTs, SPACs simultaneously erupting, capital swirling

2. **Memeification**
   Investment decisions shift from "fundamentals" to "memes" and "community" (GME, DOGE)

3. **Zero-Rate Side Effects**
   "Risk-free rate = 0" → illusion that theoretical price of all assets approaches ∞

### Lessons

1. **End of Monetary Easing = Bubble Collapse Trigger**
   Reversal moment Fed turned hawkish (November 2021)

2. **Multi-Asset Simultaneous Bubbles Amplify Danger**
   Correlation approaches 1.0 → diversification benefit vanishes

3. **Meme Investment Limits**
   Short-term crowd frenzy unsustainable, fundamental reversion inevitable

---

## Common Patterns

### Pattern 1: Trigger Always "Monetary Policy Shift"

| Bubble | Peak Timing | Policy Shift | Time Lag |
|--------|------------|--------------|----------|
| Dotcom | March 2000 | Fed rate hikes (1999-2000) | Immediate |
| Crypto 2017 | December 2017 | China regulatory crackdown | 1 month |
| Pandemic | November 2021 | Fed hawkish signal | Immediate |

### Pattern 2: Bubble Stage Time Allocation

```
Typical Bubble Cycle (total 18-36 months):
Displacement:   20% of duration (tech innovation, policy change)
Boom:           40% of duration (rational expansion)
Euphoria:       30% of duration (exuberance)
Profit Taking:  5% of duration (caution period)
Panic:          5% of duration (crash)
```

**Important:** Euphoria occupies 1/3 of total = source of "lasts too long" impression

### Pattern 3: Staged Social Penetration Expansion

```
Phase 1: Experts, early adopters (institutional investors, tech enthusiasts)
    ↓ 1-2 years
Phase 2: Educated class, white-collar workers (doctors, lawyers, salarymen)
    ↓ 6-12 months
Phase 3: General public (taxi drivers, housewives, students)
    ↓ 1-3 months
Peak reached
```

**Lesson:** When Phase 3 detected, 1-3 months remaining

### Pattern 4: Media Role

**Boom Period:**
- Cautiously optimistic "expert views"
- Risks also mentioned

**Euphoria Period:**
- FOMO incitement: "Don't miss out"
- Over-exposure of success stories
- Risk warners labeled "outdated"

**Panic Period:**
- Flip to pessimism
- "Who's to blame" witch hunt

### Pattern 5: Price Patterns

**Uptrend:**
```
Stage 1: Gradual rise (+15-25% annual)
Stage 2: Acceleration (+40-60% annual)
Stage 3: Parabolic (100%+ in months)
         ↑ Public entry here
```

**Downtrend:**
```
Stage 1: Correction (-10-15%) → "buying opportunity" perception
Stage 2: Failed bounce, double top forms
Stage 3: Collapse (-50%+) → Panic
```

### Pattern 6: "This Time Is Different" Excuse Patterns

| Bubble | "This Time Is Different" Reason | Reality |
|--------|--------------------------------|---------|
| Dotcom | Internet revolution, Old Economy over | Growth without profits unsustainable |
| Housing 2008 | Housing prices never fall, securitization spreads risk | Subprime collapse |
| Crypto 2017 | End of fiat, governments can't regulate | Regulatory crackdown causes crash |
| Pandemic | Infinite QE, perpetual zero rates, no inflation | Inflation surge → tightening |

**Lesson:** When "this time is different" becomes the mantra, historical repetition is near

---

## Application to Practice

### Case Study: Ideal Response During 2017 Crypto Bubble

**Premise:** Purchased Bitcoin in January 2017 at $1k with $1,000

**Actual Price Progression:**
- June: $3k (+200%)
- August: $5k (+400%)
- November: $10k (+900%)
- December 17: $19.8k (+1,880%, peak)
- December 2018: $3.2k (-84% from peak)

#### Scenario A: "Perfect Timing" Illusion (Impossible to Execute)

Sell everything at $19.8k = $19,800 profit

**Problem:** Cannot predict peak in advance, pure luck

#### Scenario B: Stair-Step Profit-Taking (Executable)

```
$3k   → Sell 25% = $750 (remaining $2,250 invested)
$5k   → Sell 25% = $1,250 (remaining $1,500 invested)
$10k  → Sell 25% = $2,500 (remaining $750 invested)
$15k  → Sell 25% = $3,750 (position fully closed)
```

**Total Profit:** $8,250
**vs Peak:** 42% (less than half of perfect)
**But:** Reliably executable, psychologically stable

#### Scenario C: ATR Trailing Stop (Executable + Upside Capture)

- Early December 2017, ATR (20-day) ≈ $1,500
- Using coefficient 1.5: Stop = $10,000 - ($1,500 × 1.5) = $7,750
- December 17 peak $19,800 → Stop updated: $19,800 - $2,250 = $17,550
- Decline starts → Sell all at $17,550

**Total Profit:** $16,550 (-11% from peak exit)
**Benefits:** Maximum upside capture, early decline exit

### Integrated Lessons

1. **Abandon "Perfection"**
   Peak selling impossible. Aim for "satisfaction" with stair-step profit-taking

2. **Mechanical Rule Superiority**
   ATR trailing eliminates emotion, exits early in bubble collapse

3. **Flexibility by Bubble Stage**
   - Boom period: Stair-step profit-taking (conservative)
   - Euphoria period: ATR trailing (aggressive)
   - Panic signs: Immediate exit (defensive)

4. **Managing Post-Hoc Regret**
   Evaluation criterion: "secure profit capture" not "could have made more"

### Referencia: references/implementation_guide.md

# Bubble Detector Implementation Guide (Revised v2.0)

## Required Checklist Before Use

### Pre-verification
```
□ User is asking "Is it a bubble?"
□ Objective evaluation is requested (not impressions)
□ You have time to collect measured data
```

---

## Step-by-Step Evaluation Process

### Step 1: Identify Market and Verify Data Sources

**For US Market:**
```
Required Data Sources:
1. CBOE - Put/Call ratio, VIX
2. FINRA - Margin debt balance
3. Renaissance Capital - IPO statistics
4. Barchart/TradingView - Breadth indicators
```

**For Japanese Market:**
```
Required Data Sources:
1. Barchart - Nikkei Futures Options P/C
2. Investing.com - JNIVE (Nikkei VI)
3. JSF - Margin debt balance
4. MacroMicro - TOPIX Breadth
5. PwC - Global IPO Watch
```

### Step 2: Quantitative Data Collection (MANDATORY)

**Use web_search to collect the following in order:**

```python
# US Market Example
queries = [
    "CBOE put call ratio current",  # P/C ratio
    "VIX index current level",       # VIX
    "FINRA margin debt latest",      # Margin debt
    "S&P 500 breadth 50 day MA",     # Breadth
    "Renaissance IPO market 2025",   # IPO statistics
]

# Japanese Market Example
queries_japan = [
    "Nikkei 225 futures options put call ratio",
    "Nikkei Volatility Index JNIVE current",
    "JSF margin trading balance latest",
    "TOPIX constituent stocks 200 day moving average",
    "Japan IPO market 2025 statistics",
]
```

**Important: Collect specific numerical values for each search**
- ❌ "VIX is at low levels" → Insufficient
- ✅ "VIX is 15.3" → OK

### Step 3: Organize and Verify Data

Organize collected data in table format:

```markdown
| Indicator | Collected Value | Source | Collection Date |
|-----------|----------------|---------|----------------|
| Put/Call | 0.95 | CBOE | 2025-10-27 |
| VIX | 15.3 | Yahoo Finance | 2025-10-27 |
| Margin YoY | +8% | FINRA | 2025-09 |
| Breadth (50DMA) | 68% | Barchart | 2025-10-27 |
| IPO Count | 45/Q3 | Renaissance | 2025 Q3 |
```

**Verification Points:**
- □ All indicators have specific numerical values
- □ Sources are reliable
- □ Data is recent (within 1 week)

### Step 4: Mechanical Scoring

**Score mechanically by referring to threshold tables:**

```
Indicator 1: Put/Call = 0.95
  → 0.95 > 0.85 → 0 points

Indicator 2: VIX = 15.3 + near highs
  → VIX > 15 → 0 points

Indicator 3: Margin YoY = +8%
  → +8% < +10% → 0 points

Indicator 4: IPO = 45 count (5-year average 35)
  → 45/35 = 1.29x < 1.5x → 0 points

Indicator 5: Breadth = 68%
  → 68% > 60% → 0 points

Indicator 6: Price Acceleration (requires calculation)
  → Past 3 months +12%, 75th percentile in 10-year distribution → 0 points

Phase 2 Total: 0 points
```

### Step 5: Qualitative Adjustment (Upper limit +3 points, STRICT CRITERIA)

**⚠️ CRITICAL: Qualitative adjustments require MEASURABLE evidence. Subjective impressions are NOT allowed.**

**Confirmation Bias Prevention Checklist:**
```
Before adding any qualitative points, verify:
□ Do you have concrete, measurable data? (not impressions)
□ Would an independent observer reach the same conclusion?
□ Are you avoiding double-counting with Phase 2 quantitative scores?
□ Have you documented the specific evidence?
```

**A. Social Penetration (0-1 points):**
```
REQUIRED EVIDENCE (all three must be present for +1 point):
✓ Direct user report: "Non-investor asked me about [asset]"
✓ Specific examples: Names, dates, conversations
✓ Multiple independent sources (minimum 3)

Scoring:
+1 point: All three criteria met (taxi driver/barber investment advice)
+0 points: Any criteria missing

Example of VALID evidence:
"User reported: 'My barber asked me about NVDA stock on Nov 1.
My dentist mentioned AI stocks on Nov 2.
My Uber driver discussed crypto on Nov 3.'"

Example of INVALID evidence:
"AI narrative is prevalent" (too vague, unmeasurable)
```

**B. Media/Search Trends (0-1 points):**
```
REQUIRED EVIDENCE (measurable data only):
✓ Google Trends data showing 5x+ increase YoY
✓ Mainstream media coverage count (Time/Newsweek covers, TV specials)
✓ Web search data from multiple sources confirming saturation

Scoring:
+1 point: Search trends 5x+ baseline AND mainstream coverage confirmed
+0 points: Search trends <5x OR no mainstream coverage confirmation

⚠️ CRITICAL: "Elevated narrative" without data = +0 points

How to verify:
1. Use Google Trends API or web search for "[topic] search volume 2025"
2. Search for "[topic] Time magazine cover" or "[topic] CNBC special"
3. Document specific numbers and dates

Example of VALID evidence:
"Google Trends shows 'AI stocks' at 780 (baseline 150 = 5.2x).
Time Magazine cover 'The AI Revolution' (Oct 15, 2025).
CNBC aired 'AI Investment Special' (3 episodes in Oct 2025)."

Example of INVALID evidence:
"AI/technology narrative seems elevated" (unmeasurable)
```

**C. Valuation Disconnect (0-1 points):**
```
⚠️ WARNING: Avoid double-counting with Phase 2 quantitative scores

REQUIRED EVIDENCE:
✓ P/E ratio >25 (if not already counted in Phase 2)
✓ Narrative explicitly ignores fundamentals
✓ "This time is different" reasoning documented in mainstream media

Scoring:
+1 point: P/E >25 AND fundamentals actively ignored in public discourse
+0 points: High P/E but fundamentals support valuation

Self-check questions:
- Is this already captured in Phase 2 quantitative scoring? If yes, +0 points
- Do companies have real earnings supporting valuations? If yes, +0 points
- Is the narrative backed by fundamental improvements? If yes, +0 points

Example of VALID evidence for +1 point:
"S&P 500 P/E = 35x (vs. historical 18x).
Mainstream articles: 'Earnings don't matter in AI era' (CNBC, Oct 2025).
'Traditional valuation metrics obsolete' (Bloomberg, Nov 2025)."

Example of INVALID evidence:
"P/E 30.8 but AI has fundamental backing" (fundamentals support valuation = +0)
```

**Phase 3 Adjustment Calculation:**
```
Maximum possible: +3 points (1+1+1)

Common mistakes to avoid:
❌ Adding points based on "feeling" or "sense"
❌ Double-counting valuation already in Phase 2
❌ Accepting narrative claims without measuring data
✅ Require concrete, independently verifiable evidence
✅ Document specific sources and dates
✅ Apply strict interpretation standards
```

### Step 6: Final Judgment and Report

```markdown
# [Market Name] Bubble Evaluation Report (Revised v2.0)

## Overall Assessment
- Final Score: 0/16 points
- Phase: Normal
- Risk Level: Low
- Evaluation Date: 2025-10-27

## Quantitative Data (Phase 2)

| Indicator | Measured Value | Score | Rationale |
|-----------|----------------|-------|-----------|
| Put/Call | 0.95 | 0 pts | > 0.85 healthy |
| VIX + Highs | 15.3 | 0 pts | > 15 normal |
| Margin YoY | +8% | 0 pts | < +10% normal |
| IPO Heat | 1.29x | 0 pts | < 1.5x |
| Breadth | 68% | 0 pts | > 60% healthy |
| Price Accel | 75th %ile | 0 pts | < 85th %ile |

**Phase 2 Total: 0 points**

## Qualitative Adjustment (Phase 3)

- Social Penetration: No user reports (+0 pts)
- Media: Google Trends 1.8x (+0 pts)
- Valuation: P/E 21x (+0 pts)

**Phase 3 Adjustment: +0 points**

## Recommended Actions

**Risk Budget: 100%**
- Continue normal investment strategy
- Set ATR 2.0× trailing stop
- Apply stair-step profit-taking rule (+20% take 25%)

**Short-Selling: Not Allowed**
- Composite conditions: 0/7 met
```

---

## NG Examples vs OK Examples

### NG Example 1: No Data Collection

```
❌ Bad Evaluation:
"Many Takaichi Trade reports"
"Experts warn of overheating"
→ Media saturation 2 points

✅ Good Evaluation:
[web_search: "Google Trends Japan stocks Takaichi"]
Result: 1.8x year-over-year
→ Google Trends adjustment +0 points (below 3x)
```

### NG Example 2: Scoring Based on Impressions

```
❌ Bad Evaluation:
"VIX seems to be at low levels"
→ Volatility suppression 2 points

✅ Good Evaluation:
[web_search: "VIX current level"]
Result: VIX 15.8
→ VIX > 15 = 0 points
```

### NG Example 3: Emotional Reaction to Price Rise

```
❌ Bad Evaluation:
"2,100 yen rise in one day is abnormal"
→ Price acceleration 2 points

✅ Good Evaluation:
[Verify daily return distribution over past 10 years]
4.5% rise = 80th percentile over past 10 years (rare but not extreme)
→ Price acceleration 0 points
```

---

## Self-Check: Quality of Evaluation

After completing evaluation, verify the following:

```
□ Did you collect data for all indicators in Phase 1?
  - Put/Call: [  ]
  - VIX: [  ]
  - Margin: [  ]
  - Breadth: [  ]
  - IPO: [  ]
  - Price Distribution: [  ]

□ Does each score have measured value basis?
  - Have you excluded impressions like "many reports"?

□ Did you keep qualitative adjustment within +5 point limit?
  - Adjustment A: [  ] points
  - Adjustment B: [  ] points
  - Adjustment C: [  ] points
  - Total ≤ 5 points?

□ Is the final score reasonable?
  - Compare with other quantitative frameworks
  - Re-verify if there is a difference of 10+ points
```

---

## Evaluation Quality Judgment Criteria

### Level 1: Failed (Insufficient Data)
```
- Quantitative data collection for 3 or fewer of 6 indicators
- Scoring based on impressions
- No source documentation
```

### Level 2: Pass Minimum (Needs Improvement)
```
- Quantitative data collection for 4-5 of 6 indicators
- Some impression-based evaluation mixed in
- Source documentation present but incomplete
```

### Level 3: Good (Recommended Level)
```
- Quantitative data collection for all 6 indicators
- Mechanical scoring implemented
- Source and date for all data
- Qualitative adjustment is conservative (+2 points or less)
```

### Level 4: Excellent (Best Practice)
```
- Perfect quantitative data collection
- Comparative analysis with historical data
- Cross-check with multiple sources
- Consistency check with quantitative frameworks
- Explicit statement of uncertainties
```

---

## Evaluation Report Template

```markdown
# [Market Name] Bubble Evaluation Report v2.0

**Evaluation Date:** YYYY-MM-DD
**Evaluator Confidence:** [0-100]
**Data Completeness:** [0-100]%

---

## Executive Summary

**Conclusion:** [One-sentence conclusion]
**Score:** X/16 points ([Normal/Caution/Euphoria/Critical])
**Recommendation:** [Concise action]

---

## Quantitative Evaluation (Phase 2)

[Table of 6 indicators]

**Phase 2 Total:** X points

---

## Qualitative Adjustment (Phase 3)

[3 adjustment items]

**Phase 3 Adjustment:** +Y points

---

## Final Judgment

**Final Score:** X + Y = Z points
**Risk Budget:** [0-100]%
**Recommended Actions:**
1. [Specific action 1]
2. [Specific action 2]
3. [Specific action 3]

---

## Data Quality Notes

**Collected Data:**
- [Indicator name]: [value] ([source], [date])
- ...

**Limitations:**
- [Document if there are data constraints]

**Confidence Level:**
- Confidence in this evaluation: [reason]
```

---

## Red Flags During Review

If any of the following are observed, redo the evaluation:

```
🚩 "Many reports" → No numbers
🚩 "Experts are cautious" → No quantitative data
🚩 "Obviously too high" → Subjective judgment
🚩 Score 10+ points but Put/Call > 1.0
🚩 Score 10+ points but VIX > 20
🚩 Score 10+ points but Margin YoY < +15%
🚩 No data source documentation
🚩 No collection date documentation
```

---

## Reference Materials

### Data Analysis Principles
- "In God we trust; all others must bring data." - W. Edwards Deming
- "Without data, you're just another person with an opinion." - W. Edwards Deming

### Guarding Against Biases
- Confirmation bias: Collecting only information that supports your hypothesis
- Availability bias: Overweighting recently seen information
- Narrative fallacy: Oversimplifying causal relationships with stories

---

## Final Check

Before submitting evaluation:

```
□ All quantitative data have numerical values
□ All data have sources and dates
□ Excluded impressions and emotional expressions
□ Scored mechanically
□ Qualitative adjustment is conservative (+2 points or less recommended)
□ Consistency verified with other quantitative frameworks
□ Uncertainties explicitly stated
```

**If all of these are ✓, you are ready to report.**

---

**Last Updated:** 2025-10-27
**Next Review:** Reflect feedback after actual evaluation implementation

### Referencia: references/quick_reference.md

# Bubble Detection Quick Reference

## Daily Checklist (Complete in 5 Minutes)

### Morning Routine (Before Market Open)

```
□ Step 1: Update Bubble-O-Meter (2 minutes)
   - Score 8 indicators on 0-2 scale
   - Confirm risk budget based on total score

□ Step 2: Position Management (2 minutes)
   - Update ATR trailing stops
   - Check if stair-step profit-taking targets reached
   - Determine new entry eligibility

□ Step 3: Signal Confirmation (1 minute)
   - Media/social media trends (Google Trends, Twitter)
   - Major indices' distance from 52-week highs
   - VIX & Put/Call ratio
```

---

## Emergency Assessment: 3 Questions

When uncertain about investment decisions, answer these 3 questions:

### Q1: "Are non-investors recommending?"
- YES → Mass penetration complete, likely late stage
- NO → Still early-to-mid stage

### Q2: "Has the narrative become 'common sense'?"
- YES → Euphoria stage, dissent socially unacceptable
- NO → Skeptical views still tolerated, healthy state

### Q3: "Is 'this time is different' the mantra?"
- YES → Historically typical bubble sign
- NO → Healthy caution still functioning

**All 3 YES → Critical zone, prioritize profit-taking/exit**

---

## Action Matrix by Bubble Stage (REVISED v2.1)

| Phase | Score | Risk Budget | Entry | Profit-Taking | Stop | Shorts |
|-------|-------|------------|-------|--------------|------|--------|
| **Normal** | 0-4 | 100% | Normal | At target | 2.0 ATR | No |
| **Caution** | 5-7 | 70-80% | 50% reduced | 25% at +20% | 1.8 ATR | No |
| **Elevated Risk** | 8-9 | 50-70% | Selective | 40% at +20% | 1.6 ATR | Consider |
| **Euphoria** | 10-12 | 40-50% | Stop | 50% at +20% | 1.5 ATR | After conditions |
| **Critical** | 13-15 | 20-30% | Stop | 75-100% immediate | 1.2 ATR | Recommended |

**Note**: Maximum score reduced from 16 to 15 points (Phase 2: max 12, Phase 3: max 3)

---

## Quick Scoring for 8 Indicators

### 1. Mass Penetration
```
0 points: Investors only
1 point: General awareness but investment still limited
2 points: Taxi drivers/family recommending
```

### 2. Media Saturation
```
0 points: Normal coverage level
1 point: Search trends 2-3x
2 points: TV specials/magazine covers, searches 5x+
```

### 3. New Entrants
```
0 points: Normal account opening pace
1 point: 50-100% YoY increase
2 points: 200%+ YoY, beginner flood
```

### 4. Issuance Flood
```
0 points: Normal IPO count
1 point: 50% increase in IPOs/related products
2 points: Low-quality IPOs, theme ETF proliferation
```

### 5. Leverage
```
0 points: Normal range
1 point: Margin balance 1.5x
2 points: All-time high, funding rates elevated
```

### 6. Price Acceleration
```
0 points: Near historical median
1 point: Exceeds 90th percentile
2 points: 95-99th percentile or accelerating
```

### 7. Valuation Disconnect
```
0 points: Explainable by fundamentals
1 point: High valuation but explained by growth expectations
2 points: Completely "narrative"-dependent, fundamentals ignored
```

### 8. Correlation & Breadth
```
0 points: Only some leaders rising
1 point: Sector-wide spread
2 points: Even low-quality/zombie companies rallying
```

---

## Key Data Sources

### Instantly Checkable Indicators

| Indicator | Source | Example URL |
|-----------|--------|------------|
| Google Search Trends | Google Trends | trends.google.com |
| VIX (Fear Index) | CBOE | cboe.com/vix |
| Put/Call Ratio | CBOE | cboe.com/data |
| Margin Balance | FINRA | finra.org/data |
| Futures Positions | CFTC COT | cftc.gov/reports |
| IPO Statistics | Renaissance IPO | renaissancecapital.com |

### API-Accessible Auto-Retrieval

```python
# Example: Google Trends (pytrends)
from pytrends.request import TrendReq
pytrends = TrendReq()
pytrends.build_payload(['SPY', 'stock market'])
data = pytrends.interest_over_time()

# Example: VIX (yfinance)
import yfinance as yf
vix = yf.Ticker('^VIX')
current_vix = vix.history(period='1d')['Close'].iloc[-1]
```

---

## Profit-Taking Strategy Templates

### Template 1: Stair-Step Profit-Taking (Conservative)

```
Position: $10,000 initial investment
Targets:  +20%, +40%, +60%, +80%

+20% ($12,000) → Sell 25% = $3,000 secured
+40% ($14,000) → Sell 25% = $3,500 secured
+60% ($16,000) → Sell 25% = $4,000 secured
+80% ($18,000) → Sell 25% = $4,500 secured

Total profits: $15,000 (+50% equivalent)
```

### Template 2: ATR Trailing (Aggressive)

```python
def calculate_trailing_stop(current_price, atr_20d, bubble_phase):
    """
    Calculate trailing stop based on bubble stage

    bubble_phase: 'normal', 'caution', 'euphoria', 'critical'
    """
    multipliers = {
        'normal': 2.0,
        'caution': 1.8,
        'euphoria': 1.5,
        'critical': 1.2
    }
    multiplier = multipliers.get(bubble_phase, 2.0)
    stop_price = current_price - (atr_20d * multiplier)
    return stop_price

# Usage example
current_price = 450.0
atr_20d = 10.0  # Average True Range over 20 days
bubble_phase = 'euphoria'

stop = calculate_trailing_stop(current_price, atr_20d, bubble_phase)
print(f"Trailing Stop: ${stop:.2f}")
# Output: Trailing Stop: $435.00
```

### Template 3: Hybrid (Recommended)

```
Stage 1 (Boom period):
  → Reduce 50% of position via stair-step profit-taking

Stage 2 (Euphoria period):
  → Apply ATR trailing to remaining 50%, follow upside

Stage 3 (Panic signs):
  → Exit immediately when ATR stop hit
```

---

## Short-Selling Timing Assessment (Critical)

### ❌ Absolutely NG: Early Contrarian

```
Reason: Normal for prices to rise 2-3x more after feeling "too high"
Risk: "Markets can remain irrational longer than you can remain solvent"
```

### ✅ Recommended: After Composite Conditions Clear

**Consider starting when at least 3 apply:**

1. □ Weekly chart shows clear lower highs
2. □ Volume peaks out (3 consecutive weeks declining)
3. □ Sharp drop in leverage indicators (margin balance -20%+)
4. □ Media/search trends peak out
5. □ Weak stocks within sector start breaking down first
6. □ VIX surges (+30%+)
7. □ Fed/policy shift signals

**Execution Example:**

```
Condition Check:
[✓] 1. Weekly lower highs forming
[✓] 2. Volume declining 3 weeks straight
[×] 3. Margin balance still elevated
[✓] 4. Google search trends -40%
[×] 5. Still broad rally continuing
[✓] 6. VIX +35% surge
[×] 7. No policy changes

→ 4/7 met, shorts consideration OK
→ Small position (25% of normal) for test entry
```

---

## Common Failure Patterns & Solutions

### Failure 1: "Too late" paralysis, missing opportunities

**Psychology:** Regret aversion (fear of being late)
**Solution:**
- Conduct Bubble-O-Meter when feeling "too late"
- Score ≤8: Small position entry OK
- Score ≥9: Correct to stay out

### Failure 2: Re-entry after profit-taking (buying high)

**Psychology:** Hindsight bias ("knew it would go higher")
**Solution:**
- 72-hour no re-entry rule after profit-taking
- Re-entry decisions only after Bubble-O-Meter check

### Failure 3: Can't take profits due to "still rising"

**Psychology:** Greed + Overconfidence
**Solution:**
- Automate stair-step profit-taking (pre-set limit orders)
- Aim for "satisfaction," abandon "perfection"

### Failure 4: Too-early shorts

**Psychology:** Subjective "obviously too high" judgment
**Solution:**
- Mechanically verify composite conditions
- Wait for minimum 3 conditions to clear

---

## Emergency Response Flowchart

```
Detect market volatility
    ↓
Q: Have positions?
    ↓YES
Q: Down -5% or more?
    ↓YES
Q: ATR stop reached?
    ↓YES
→ Sell immediately (no debate)

    ↓NO (Stop not reached)
Q: Bubble-O-Meter score 13+?
    ↓YES
→ Consider 75%+ profit-taking

    ↓NO (Score ≤12)
Q: VIX surge +30%+?
    ↓YES
→ 50% profit-taking, tighten remaining stops

    ↓NO
→ Business as usual, continue calm observation
```

---

## Golden Rules (10 Commandments to Post on Wall)

1. **See process, not price**

2. **When taxi drivers talk stocks, exit**

3. **"This time is different" is always the same**

4. **Mechanical rules protect psychology**

5. **Short after confirmation, take profits early**

6. **When skepticism hurts, the end begins**

7. **Aim for satisfaction, abandon perfection**

8. **Bubbles last longer than expected, collapses are faster**

9. **Leverage is an express ticket to ruin**

10. **"Markets can remain irrational longer than you can remain solvent"**

---

## Resources for Further Learning

### Books
- **"Manias, Panics, and Crashes"** - Charles Kindleberger
- **"Irrational Exuberance"** - Robert Shiller
- **"The Alchemy of Finance"** - George Soros

### Research
- Hyman Minsky's Financial Instability Hypothesis
- Classic papers in Behavioral Finance

### Data & Tools
- **TradingView**: Charts and technical indicators
- **FRED (Federal Reserve)**: Economic indicator time series
- **Finviz**: Screening and heatmaps
- **Google Trends**: Social trends

---

**Last Updated:** 2025 Edition
**License:** Educational and personal use only, redistribution prohibited

### Referencia: references/quick_reference_en.md

# Bubble Detection Quick Reference (English)

## Daily Checklist (5 minutes)

### Morning Routine (Before Market Open)

```
□ Step 1: Update Bubble-O-Meter (2 min)
   - Score 8 indicators (0-2 points each)
   - Check risk budget based on total score

□ Step 2: Position Management (2 min)
   - Update ATR trailing stops
   - Check stair-step profit targets
   - Evaluate new entry eligibility

□ Step 3: Signal Check (1 min)
   - Media/Social trends (Google Trends, Twitter)
   - Major indices distance from 52-week highs
   - VIX & Put/Call ratio
```

---

## Emergency Assessment: 3 Questions

When uncertain about an investment decision, answer these 3 questions:

### Q1: "Are non-investors recommending it?"
- YES → Mass penetration complete, likely late stage
- NO → Still early to mid stage

### Q2: "Has the narrative become 'common sense'?"
- YES → Euphoria stage, contrarian views socially unacceptable
- NO → Healthy skepticism still functions

### Q3: "Is 'this time is different' the catchphrase?"
- YES → Classic historical bubble signal
- NO → Healthy caution still present

**All 3 YES → Critical zone, prioritize profit-taking/exit**

---

## Action Matrix by Bubble Phase

| Phase | Score | Risk Budget | Entry | Profit-Taking | Stop | Short |
|-------|-------|------------|-------|---------------|------|-------|
| **Normal** | 0-4 | 100% | Normal | At target | 2.0 ATR | No |
| **Caution** | 5-8 | 70% | 50% reduced | 25% at +20% | 1.8 ATR | No |
| **Euphoria** | 9-12 | 40% | Stopped | 50% at +20% | 1.5 ATR | After confirm |
| **Critical** | 13-16 | 20% | Stopped | 75-100% now | 1.2 ATR | Recommended |

---

## 8 Indicators Quick Scoring

### 1. Mass Penetration
```
0 pts: Investors only
1 pt: General awareness but investment limited
2 pts: Taxi drivers/family recommending
```

### 2. Media Saturation
```
0 pts: Normal coverage
1 pt: Search trends 2-3x normal
2 pts: TV specials/magazine covers, 5x+ search spike
```

### 3. New Accounts & Inflows
```
0 pts: Normal account openings
1 pt: 50-100% YoY increase
2 pts: 200%+ YoY, first-time investor flood
```

### 4. New Issuance Flood
```
0 pts: Normal IPO volume
1 pt: IPO/SPAC/ETFs up 50%+
2 pts: Low-quality IPO flood, "theme" fund proliferation
```

### 5. Leverage Indicators
```
0 pts: Margin debt in normal range
1 pt: Margin debt 1.5x average
2 pts: All-time high margin, funding rates elevated, extreme positioning
```

### 6. Price Acceleration
```
0 pts: Annualized returns near historical median
1 pt: Returns exceed 90th percentile
2 pts: Returns at 95-99th percentile, or positive second derivative
```

### 7. Valuation Disconnect
```
0 pts: Fundamentally explainable
1 pt: High valuation but "growth expectations" provide cover
2 pts: Pure "narrative" dependent, fundamentals ignored
```

### 8. Breadth & Correlation
```
0 pts: Only leader stocks rising
1 pt: Sector-wide participation
2 pts: Low-quality/zombie companies rising (last buyers in)
```

---

## Profit-Taking Strategy Templates

### Template 1: Stair-Step (Conservative)

```
Position: $10,000 initial investment
Targets: +20%, +40%, +60%, +80%

+20% ($12,000) → Sell 25% = $3,000 secured
+40% ($14,000) → Sell 25% = $3,500 secured
+60% ($16,000) → Sell 25% = $4,000 secured
+80% ($18,000) → Sell 25% = $4,500 secured

Total profit secured: $15,000 (+50% equivalent)
```

### Template 2: ATR Trailing (Aggressive)

```python
def calculate_trailing_stop(current_price, atr_20d, bubble_phase):
    """
    Calculate trailing stop based on bubble phase

    bubble_phase: 'normal', 'caution', 'euphoria', 'critical'
    """
    multipliers = {
        'normal': 2.0,
        'caution': 1.8,
        'euphoria': 1.5,
        'critical': 1.2
    }
    multiplier = multipliers.get(bubble_phase, 2.0)
    stop_price = current_price - (atr_20d * multiplier)
    return stop_price
```

### Template 3: Hybrid (Recommended)

```
Stage 1 (Boom):
  → Stair-step reduces 50% of position

Stage 2 (Euphoria):
  → Apply ATR trailing to remaining 50%, ride upside

Stage 3 (Panic signals):
  → Exit immediately when ATR stop hit
```

---

## Short-Selling Timing Decision (Critical)

### ❌ Absolutely Avoid: Early Contrarian

```
Reason: Often 2-3x further rise after "obviously too high"
Risk: "Markets can remain irrational longer than you can remain solvent"
```

### ✅ Recommended: After Composite Conditions Met

**Need at least 3 of 7 conditions before considering:**

1. □ Weekly chart shows clear lower highs
2. □ Volume peaked out (3 weeks declining)
3. □ Leverage metrics drop sharply (margin debt -20%+)
4. □ Media/search trends peaked out
5. □ Weak stocks in sector breaking down first
6. □ VIX spike (+30%+)
7. □ Fed or policy reversal signals

**Execution example:**

```
Conditions check:
[✓] 1. Weekly lower highs
[✓] 2. Volume declining 3 weeks
[×] 3. Margin debt still elevated
[✓] 4. Google trends -40%
[×] 5. Still broad rally
[✓] 6. VIX +35% spike
[×] 7. No policy change

→ 4/7 met, short consideration OK
→ Small size (25% of normal) test entry
```

---

## Common Failure Patterns & Solutions

### Failure 1: "Too late" mentality, perpetual waiting

**Psychology:** Regret aversion (FOMO about missing out)
**Solution:**
- Run Bubble-O-Meter when feeling too late
- If score ≤8, small entry OK
- If score ≥9, correct to wait

### Failure 2: Re-entry after taking profits (buying high)

**Psychology:** Hindsight bias ("I knew it would go up")
**Solution:**
- 72-hour re-entry ban after profit-taking
- Re-entry only after Bubble-O-Meter check

### Failure 3: "Still going up" paralysis on profit-taking

**Psychology:** Greed + Overconfidence
**Solution:**
- Automate stair-step (preset limit orders)
- Target "satisfaction" not "perfection"

### Failure 4: Premature short selling

**Psychology:** Subjective "obviously too high"
**Solution:**
- Mechanically check composite conditions
- Wait for minimum 3 conditions

---

## Emergency Response Flowchart

```
Market shock detected
    ↓
Q: Have positions?
    ↓YES
Q: Down -5%+ ?
    ↓YES
Q: ATR stop hit?
    ↓YES
→ Sell immediately (no debate)

    ↓NO (stop not hit)
Q: Bubble-O-Meter 13+?
    ↓YES
→ Consider 75%+ profit-taking

    ↓NO (score ≤12)
Q: VIX spike +30%+?
    ↓YES
→ Take 50% profits, tighten stops on rest

    ↓NO
→ Normal monitoring, stay calm
```

---

## Golden Rules (Post on Your Wall)

1. **Watch the process, not the price**

2. **When taxi drivers talk stocks, exit**

3. **"This time is different" is the same every time**

4. **Mechanical rules protect your psychology**

5. **Short after confirmation, take profits early**

6. **When skepticism hurts socially, the end begins**

7. **Aim for satisfaction, abandon perfection**

8. **Bubbles last longer than expected, crashes faster**

9. **Leverage is an express ticket to ruin**

10. **"Markets can remain irrational longer than you can remain solvent"**

---

## Key Data Sources

### Instantly Accessible Indicators

| Indicator | Source | URL Example |
|-----------|--------|-------------|
| Google Search Trends | Google Trends | trends.google.com |
| VIX (Fear Index) | CBOE | cboe.com/vix |
| Put/Call Ratio | CBOE | cboe.com/data |
| Margin Debt | FINRA | finra.org/data |
| Futures Positioning | CFTC COT | cftc.gov/reports |
| IPO Statistics | Renaissance IPO | renaissancecapital.com |

### API-Accessible for Automation

```python
# Example: Google Trends (pytrends)
from pytrends.request import TrendReq
pytrends = TrendReq()
pytrends.build_payload(['SPY', 'stock market'])
data = pytrends.interest_over_time()

# Example: VIX (yfinance)
import yfinance as yf
vix = yf.Ticker('^VIX')
current_vix = vix.history(period='1d')['Close'].iloc[-1]
```

---

## Further Learning

### Books
- "Manias, Panics, and Crashes" - Charles Kindleberger
- "Irrational Exuberance" - Robert Shiller
- "The Alchemy of Finance" - George Soros

### Research
- Hyman Minsky's Financial Instability Hypothesis
- Behavioral Finance classics

### Data & Tools
- TradingView: Charts & technical indicators
- FRED (Federal Reserve): Economic time series
- Finviz: Screening & heatmaps
- Google Trends: Social trends

---

**Last Updated:** 2025 Edition
**License:** Educational/personal use only
