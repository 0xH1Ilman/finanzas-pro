# 04-macro-mercado-breadth — parte 3

Skills de terceros agrupadas por tema. Cada sección indica fuente, licencia y dónde está su código.



---

## SKILL: us-market-bubble-detector

- Fuente: `tradermonty/claude-trading-skills` → `skills/us-market-bubble-detector` (MIT)
- Cuándo usarla: Evaluates market bubble risk through quantitative data-driven analysis using the revised Minsky/Kindleberger framework v2.1. Prioritizes objective metrics (Put/Call, VIX, margin debt, breadth, IPO data) over subjective impressions. Features strict qualitative adjustment criteria with confirmation bias prevention. Supports practical investment decisions with mandatory data collection and mechanical scoring. Use when user asks about bubble risk, valuation concerns, or profit-taking timing.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/us-market-bubble-detector/` (requirements.txt, bubble_scorer.py)

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
□ Did you keep qualitative evaluation within +3 point limit?
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
Qualitative adjustment has a total limit of +3 points. It cannot override quantitative evaluation.

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

**Why this is a warning signal to investigate:**
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

2. **"When taxi drivers talk stocks, run the full quantitative assessment"**
   Social anecdotes alone establish neither a phase nor an exit decision.
   Complete Phase 1 data collection, Phase 2 quantitative scoring, and the
   evidence-based Phase 3 adjustments in SKILL.md before using the final score.

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

### Bubble-O-Meter v2.1 Score Estimate (March 2000)

| Indicator | Score | Rationale |
|-----------|-------|-----------|
| Put/Call Ratio | 2 | Speculative call demand and day-trading optimism dominated |
| Volatility Suppression + New Highs | 2 | NASDAQ at repeated highs with complacency toward drawdown risk |
| Leverage | 1 | Margin trading increased, but not to mortgage levels |
| IPO Market Overheating | 2 | 457 IPOs (1999), many low-quality |
| Breadth Anomaly | 2 | Low-quality internet names rallied alongside leaders |
| Price Acceleration | 2 | NASDAQ +85% annual (1999) |
| Social Penetration | 1 | Family/friends entering "day trading" |
| Media/Search Trends | 1 | Time magazine cover "Amazon.com", CNBC ratings surge |
| Valuation Disconnect | 1 | "Profits unnecessary, only revenue growth matters" |

**Total: 15/15 points (Critical Zone)**

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

### Bubble-O-Meter v2.1 Score Estimate (Mid-December 2017)

| Indicator | Score | Rationale |
|-----------|-------|-----------|
| Put/Call Ratio | 2 | Crypto derivatives and call-like upside speculation were extreme |
| Volatility Suppression + New Highs | 2 | Traders treated repeated new highs as normal despite extreme volatility |
| Leverage | 2 | 100x leverage trading on BitMEX etc. surging |
| IPO Market Overheating | 2 | 966 ICOs (2017), majority fraudulent |
| Breadth Anomaly | 2 | Even obscure altcoins +1000%+ |
| Price Acceleration | 2 | Doubled in one month ($10k→$20k), acceleration positive and increasing |
| Social Penetration | 1 | Taxi drivers, grandparents asserting "must buy" |
| Media/Search Trends | 1 | Google searches for "Bitcoin" at all-time high, daily CNBC specials |
| Valuation Disconnect | 1 | "Digital gold," "end of fiat currency" narratives dominant |

**Total: 15/15 points (Critical Zone - Max Score)**

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

### Bubble-O-Meter v2.1 Score Estimate (November 2021)

| Indicator | Score | Rationale |
|-----------|-------|-----------|
| Put/Call Ratio | 2 | Retail call-option demand and meme-stock option activity surged |
| Volatility Suppression + New Highs | 2 | Major indices made highs while risk was treated as temporary |
| Leverage | 1 | Individual options trading surged, but not excessive mortgage levels |
| IPO Market Overheating | 2 | 613 SPACs (2021 full year), many low-quality |
| Breadth Anomaly | 1 | Concentrated in FAANG and speculative cohorts, not universal breadth |
| Price Acceleration | 2 | Numerous growth stocks +100%+ annual |
| Social Penetration | 1 | WallStreetBets, TikTok investment influencers proliferating |
| Media/Search Trends | 1 | CNBC ratings surge, housewife investment specials |
| Valuation Disconnect | 1 | Extreme DCF assuming "zero discount rate," profit ignored |

**Total: 13/15 points (Critical Zone)**

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

# Bubble Detector Implementation Guide (Revised v2.1)

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
# [Market Name] Bubble Evaluation Report (Revised v2.1)

## Overall Assessment
- Final Score: 0/15 points
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
→ Google Trends adjustment +0 points (below 5x)
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

□ Did you keep qualitative adjustment within +3 point limit?
  - Adjustment A: [  ] points
  - Adjustment B: [  ] points
  - Adjustment C: [  ] points
  - Total <= 3 points?

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
# [Market Name] Bubble Evaluation Report v2.1

**Evaluation Date:** YYYY-MM-DD
**Evaluator Confidence:** [0-100]
**Data Completeness:** [0-100]%

---

## Executive Summary

**Conclusion:** [One-sentence conclusion]
**Score:** X/15 points ([Normal/Caution/Elevated Risk/Euphoria/Critical])
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
   - Score 6 quantitative indicators (0-2) + 3 qualitative adjustments (0-1)
   - Confirm risk budget based on the 0-15 total score

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

Use these questions to flag concerns that need a full evaluation:

### Q1: "Are non-investors recommending it?"
- YES → Record specific, independent recommendations for verification
- NO → No social-penetration concern identified by this question

### Q2: "Has the narrative become 'common sense'?"
- YES → Record examples of consensus and treatment of dissent for verification
- NO → No consensus concern identified by this question

### Q3: "Is 'this time is different' the catchphrase?"
- YES → Record specific media examples for verification
- NO → No narrative concern identified by this question

**All 3 YES → Strong warning signal: run the full quantitative evaluation before acting.**

YES/NO answers alone establish neither a phase nor an action, including when all
answers are NO. Complete Phase 1 data collection and Phase 2 quantitative scoring,
then apply Phase 3 evidence-based adjustments under the strict criteria in
`../SKILL.md`. Use the final score for the phase and action matrix below;
Critical requires a final score of 13-15. If required data are missing, leave the assessment incomplete
and request the missing inputs instead of assigning a phase or action.

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

## v2.1 Quick Scoring: 6 Quantitative + 3 Qualitative

### Quantitative Indicators (0-2 each)

### 1. Put/Call Ratio
```
0 points: P/C > 0.85
1 point: P/C 0.70-0.85
2 points: P/C < 0.70
```

### 2. Volatility Suppression + New Highs
```
0 points: VIX > 15 or index more than 10% from highs
1 point: VIX 12-15 and index near highs
2 points: VIX < 12 and major index within 5% of 52-week high
```

### 3. Leverage
```
0 points: Margin debt YoY <= +10% or negative
1 point: Margin debt YoY +10-20%
2 points: Margin debt YoY +20% or more and all-time high
```

### 4. IPO Market Overheating
```
0 points: Normal levels
1 point: Quarterly IPO count >1.5x five-year average
2 points: Quarterly IPO count >2x five-year average and median first-day return +20%+
```

### 5. Breadth Anomaly
```
0 points: >60% of S&P 500 stocks above 50DMA
1 point: 45-60% above 50DMA
2 points: New high and <45% above 50DMA
```

### 6. Price Acceleration
```
0 points: Past 3-month return below 85th percentile
1 point: Past 3-month return in 85-95th percentile
2 points: Past 3-month return above 95th percentile
```

### Qualitative Adjustments (0-1 each; +3 max)

### A. Social Penetration
```
0 points: Any required evidence missing
1 point: Direct user report + specific examples + at least 3 independent sources
```

### B. Media/Search Trends
```
0 points: Search trends <5x or no mainstream coverage confirmation
1 point: Google Trends 5x+ YoY and mainstream coverage confirmed
```

### C. Valuation Disconnect
```
0 points: P/E <25 or fundamentals support valuation
1 point: P/E >25, fundamentals ignored, and "this time is different" documented
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

    bubble_phase: 'normal', 'caution', 'elevated_risk', 'euphoria', 'critical'
    """
    multipliers = {
        'normal': 2.0,
        'caution': 1.8,
        'elevated_risk': 1.6,
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
- Score <=7: Small position entry OK
- Score 8-9: Only exceptional setups with reduced position size
- Score >=10: Correct to stay out

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

2. **When taxi drivers talk stocks, run the full quantitative assessment**

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
   - Score 6 quantitative indicators (0-2) + 3 qualitative adjustments (0-1)
   - Check risk budget based on 0-15 total score

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

Use these questions to flag concerns that need a full evaluation:

### Q1: "Are non-investors recommending it?"
- YES → Record specific, independent recommendations for verification
- NO → No social-penetration concern identified by this question

### Q2: "Has the narrative become 'common sense'?"
- YES → Record examples of consensus and treatment of dissent for verification
- NO → No consensus concern identified by this question

### Q3: "Is 'this time is different' the catchphrase?"
- YES → Record specific media examples for verification
- NO → No narrative concern identified by this question

**All 3 YES → Strong warning signal: run the full quantitative evaluation before acting.**

YES/NO answers alone establish neither a phase nor an action, including when all
answers are NO. Complete Phase 1 data collection and Phase 2 quantitative scoring,
then apply Phase 3 evidence-based adjustments under the strict criteria in
`../SKILL.md`. Use the final score for the phase and action matrix below;
Critical requires a final score of 13-15. If required data are missing, leave the assessment incomplete
and request the missing inputs instead of assigning a phase or action.

---

## Action Matrix by Bubble Phase

| Phase | Score | Risk Budget | Entry | Profit-Taking | Stop | Short |
|-------|-------|------------|-------|---------------|------|-------|
| **Normal** | 0-4 | 100% | Normal | At target | 2.0 ATR | No |
| **Caution** | 5-7 | 70-80% | 50% reduced | 25% at +20% | 1.8 ATR | No |
| **Elevated Risk** | 8-9 | 50-70% | Selective | 40% at +20% | 1.6 ATR | Consider |
| **Euphoria** | 10-12 | 40-50% | Stopped | 50% at +20% | 1.5 ATR | After confirm |
| **Critical** | 13-15 | 20-30% | Stopped | 75-100% now | 1.2 ATR | Recommended |

---

## v2.1 Quick Scoring: 6 Quantitative + 3 Qualitative

### Quantitative Indicators (0-2 each)

### 1. Put/Call Ratio
```
0 pts: P/C > 0.85
1 pt: P/C 0.70-0.85
2 pts: P/C < 0.70
```

### 2. Volatility Suppression + New Highs
```
0 pts: VIX > 15 or index more than 10% from highs
1 pt: VIX 12-15 and index near highs
2 pts: VIX < 12 and major index within 5% of 52-week high
```

### 3. Leverage
```
0 pts: Margin debt YoY <= +10% or negative
1 pt: Margin debt YoY +10-20%
2 pts: Margin debt YoY +20% or more and all-time high
```

### 4. IPO Market Overheating
```
0 pts: Normal levels
1 pt: Quarterly IPO count >1.5x five-year average
2 pts: Quarterly IPO count >2x five-year average and median first-day return +20%+
```

### 5. Breadth Anomaly
```
0 pts: >60% of S&P 500 stocks above 50DMA
1 pt: 45-60% above 50DMA
2 pts: New high and <45% above 50DMA
```

### 6. Price Acceleration
```
0 pts: Past 3-month return below 85th percentile
1 pt: Past 3-month return in 85-95th percentile
2 pts: Past 3-month return above 95th percentile
```

### Qualitative Adjustments (0-1 each; +3 max)

### A. Social Penetration
```
0 pts: Any required evidence missing
1 pt: Direct user report + specific examples + at least 3 independent sources
```

### B. Media/Search Trends
```
0 pts: Search trends <5x or no mainstream coverage confirmation
1 pt: Google Trends 5x+ YoY and mainstream coverage confirmed
```

### C. Valuation Disconnect
```
0 pts: P/E <25 or fundamentals support valuation
1 pt: P/E >25, fundamentals ignored, and "this time is different" documented
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

    bubble_phase: 'normal', 'caution', 'elevated_risk', 'euphoria', 'critical'
    """
    multipliers = {
        'normal': 2.0,
        'caution': 1.8,
        'elevated_risk': 1.6,
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
- If score <=7, small entry OK
- If score 8-9, enter only on exceptional setups with reduced size
- If score >=10, correct to wait

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

2. **When taxi drivers talk stocks, run the full quantitative assessment**

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


---

## SKILL: walk-forward-validation

- Fuente: `agiprolabs/claude-trading-skills` → `skills/walk-forward-validation` (MIT)
- Cuándo usarla: Walk-forward validation framework for trading strategies and ML models with time-series-aware splits, overfit detection, and regime-aware validation
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/walk-forward-validation/` (overfit_detector.py, walk_forward.py)

# Walk-Forward Validation

Walk-forward validation framework for trading strategies and ML models. Standard cross-validation (k-fold, random splits) fails catastrophically for financial time series because it introduces lookahead bias and ignores autocorrelation. This skill covers proper time-series validation techniques including rolling and expanding windows, purged cross-validation, combinatorial purged cross-validation (CPCV), and overfit detection metrics.

## Why Standard Cross-Validation Fails

Standard k-fold CV assumes data points are independent and identically distributed (IID). Financial time series violate both assumptions:

1. **Lookahead bias** — Random splits let the model train on future data and predict past data, artificially inflating performance.
2. **Autocorrelation** — Adjacent observations are correlated. A random split that puts Monday in test and Tuesday in train leaks information.
3. **Regime dependence** — Markets shift between regimes. A model trained on a bull market and tested on a bull market tells you nothing about bear market performance.
4. **Label overlap** — If labels are computed over windows (e.g., 24h forward return), adjacent train/test samples share label computation periods, leaking information.

## Walk-Forward Framework

### Rolling Window (Fixed Train Size)

The train window has a fixed size and slides forward in time. This is preferred when you believe older data is less relevant (common in crypto).

```
Window 1: [===TRAIN===][=TEST=]
Window 2:    [===TRAIN===][=TEST=]
Window 3:       [===TRAIN===][=TEST=]
```

**Parameters:**
- `train_size`: Number of bars/days in the training window
- `test_size`: Number of bars/days in the test window
- `step_size`: How far to advance between folds (often equals `test_size`)

### Expanding Window (Growing Train)

The train window starts at the beginning and expands forward. This uses all available historical data, which helps when data is scarce.

```
Window 1: [==TRAIN==][=TEST=]
Window 2: [====TRAIN====][=TEST=]
Window 3: [======TRAIN======][=TEST=]
```

**Parameters:**
- `min_train_size`: Minimum training samples before first fold
- `test_size`: Fixed test window size
- `step_size`: How far to advance between folds

### Choosing Between Them

| Factor | Rolling | Expanding |
|---|---|---|
| Data recency | Prioritizes recent data | Uses all history |
| Regime changes | Better adapts to new regimes | May dilute recent regime |
| Sample size | Fixed, may be small | Grows over time |
| Crypto preference | Preferred for < 6mo horizons | Better for regime-stable models |

## Purging and Embargo

### Purging

Remove training samples whose labels overlap with the test set's time range. If a label is computed as the 24h forward return starting at time `t`, any training sample where `t + 24h` extends into the test period must be purged.

```python
def purge_train_indices(
    train_idx: list[int],
    test_start: int,
    label_horizon: int,
    timestamps: list[int],
) -> list[int]:
    """Remove train samples whose label windows overlap test period."""
    test_start_time = timestamps[test_start]
    return [
        i for i in train_idx
        if timestamps[i] + label_horizon < test_start_time
    ]
```

### Embargo

Add a buffer gap between the end of training and start of testing to account for serial correlation that purging alone does not eliminate.

```
[===TRAIN===][--EMBARGO--][=TEST=]
```

Typical embargo sizes:
- **1-minute bars**: 60–240 bars (1–4 hours)
- **5-minute bars**: 12–48 bars (1–4 hours)
- **Hourly bars**: 6–24 bars (6–24 hours)
- **Daily bars**: 2–5 bars (2–5 days)
- **Crypto rule of thumb**: Embargo >= 2x the label computation horizon

## Combinatorial Purged Cross-Validation (CPCV)

CPCV (Lopez de Prado, 2018) generates all possible train/test combinations from `N` groups while maintaining temporal ordering. This produces far more test paths than standard walk-forward, enabling statistical tests for overfitting.

**Key properties:**
- Splits data into `N` contiguous groups
- For each combination of `k` test groups, the remaining `N-k` groups form the training set
- Applies purging and embargo at each train/test boundary
- Produces `C(N, k)` backtest paths (e.g., N=6, k=2 gives 15 paths)

See `references/methodology.md` for the full CPCV algorithm and formulas.

## Overfit Detection

### Deflated Sharpe Ratio (DSR)

The observed Sharpe ratio must be adjusted for:
- Number of strategies tested (multiple testing)
- Non-normality of returns (skewness, kurtosis)
- Length of the backtest

```python
import numpy as np
from scipy.stats import norm

def deflated_sharpe_ratio(
    observed_sr: float,
    num_trials: int,
    backtest_length: int,
    skewness: float = 0.0,
    kurtosis: float = 3.0,
) -> float:
    """Compute the probability that observed SR > 0 after deflation.

    Args:
        observed_sr: Annualized Sharpe ratio of the selected strategy.
        num_trials: Number of strategies tested (including discarded ones).
        backtest_length: Number of return observations.
        skewness: Skewness of returns.
        kurtosis: Excess kurtosis of returns.

    Returns:
        p-value (probability SR is genuinely > 0).
    """
    sr_std = np.sqrt(
        (1 - skewness * observed_sr + (kurtosis - 1) / 4 * observed_sr**2)
        / (backtest_length - 1)
    )
    # Expected max SR under null (Euler-Mascheroni approximation)
    euler_mascheroni = 0.5772156649
    expected_max_sr = norm.ppf(1 - 1 / num_trials) * (
        1 - euler_mascheroni
    ) + euler_mascheroni * norm.ppf(1 - 1 / (num_trials * np.e))
    dsr = norm.cdf((observed_sr - expected_max_sr) / sr_std)
    return dsr
```

A DSR below 0.95 suggests the observed performance is likely due to overfitting across the trials tested.

### Probability of Backtest Overfitting (PBO)

PBO uses CPCV to measure the fraction of backtest paths where the in-sample optimal strategy underperforms the median out-of-sample. A PBO above 0.50 indicates more-likely-than-not overfitting.

See `references/overfit_detection.md` for complete derivations and implementation details.

## Crypto-Specific Considerations

1. **Shorter windows**: Crypto regimes change faster than equities. A 90-day rolling window may be more appropriate than 252 days.
2. **24/7 markets**: No weekends or holidays to account for, but funding rate resets (every 8h on perps) create microstructure effects.
3. **Survivorship bias**: Many tokens delist. Validation must include delisted tokens or at minimum acknowledge this limitation.
4. **Liquidity regime shifts**: A token's liquidity profile can change dramatically (new CEX listing, liquidity mining end). Train/test splits should ideally not straddle major liquidity events.
5. **Data availability**: Many tokens have < 1 year of data. Expanding windows with small `min_train_size` may be necessary.

## Practical Window Sizes for Crypto

| Strategy Timeframe | Train Window | Test Window | Embargo |
|---|---|---|---|
| Scalping (1-5min) | 3-7 days | 1 day | 2-4 hours |
| Intraday (15min-1h) | 14-30 days | 3-7 days | 12-24 hours |
| Swing (4h-daily) | 30-90 days | 7-14 days | 2-5 days |
| Position (daily-weekly) | 90-180 days | 30 days | 5-10 days |

## Quick Start

```python
from walk_forward import WalkForwardValidator, WalkForwardConfig

config = WalkForwardConfig(
    train_size=90,
    test_size=14,
    step_size=14,
    window_type="rolling",
    embargo_size=3,
    purge_horizon=1,
)

validator = WalkForwardValidator(config)
for fold in validator.split(price_data):
    model.fit(fold.train_X, fold.train_y)
    predictions = model.predict(fold.test_X)
    fold.record_performance(predictions, fold.test_y)

results = validator.aggregate_results()
print(f"OOS Sharpe: {results.oos_sharpe:.3f}")
print(f"Train/Test Sharpe ratio: {results.sharpe_ratio_ratio:.2f}")
```

## Files

### References
- `references/methodology.md` — Walk-forward theory, window types, purging, embargo, CPCV algorithm with formulas
- `references/overfit_detection.md` — Deflated Sharpe ratio, probability of backtest overfitting, multiple testing corrections
- `references/practical_guide.md` — Window size selection for crypto, regime considerations, common validation mistakes

### Scripts
- `scripts/walk_forward.py` — Walk-forward validation engine with rolling and expanding windows; `--demo` mode with synthetic data
- `scripts/overfit_detector.py` — Deflated Sharpe ratio and PBO computation; `--demo` mode with synthetic backtest results

### Referencia: references/methodology.md

# Walk-Forward Validation — Methodology

## Overview

Walk-forward validation is the gold standard for evaluating trading strategies and financial ML models. It simulates the real-world process of training on historical data and trading on unseen future data.

## Time Series Splitting

### Rolling Window

Fixed-size training window slides forward through data:

```
Time:  t0 ──────────────────────────────────────────── tN

Fold 1: [────TRAIN────][─TEST─]
Fold 2:        [────TRAIN────][─TEST─]
Fold 3:               [────TRAIN────][─TEST─]
```

**Formal definition:**
- Given data `X[0..T]`, train size `W`, test size `H`, step `S`
- Fold `i`: train = `X[i*S .. i*S + W - 1]`, test = `X[i*S + W .. i*S + W + H - 1]`
- Number of folds: `floor((T - W - H + 1) / S) + 1`

### Expanding Window

Training window grows from a fixed start:

```
Time:  t0 ──────────────────────────────────────────── tN

Fold 1: [──TRAIN──][─TEST─]
Fold 2: [──────TRAIN──────][─TEST─]
Fold 3: [──────────TRAIN──────────][─TEST─]
```

**Formal definition:**
- Given data `X[0..T]`, minimum train size `W_min`, test size `H`, step `S`
- Fold `i`: train = `X[0 .. W_min + i*S - 1]`, test = `X[W_min + i*S .. W_min + i*S + H - 1]`
- Number of folds: `floor((T - W_min - H + 1) / S) + 1`

## Purging

### The Problem

When labels are computed over a forward-looking horizon (e.g., "5-day forward return"), a training sample at time `t` uses information up to time `t + horizon`. If the test set begins at time `t_test`, any training sample where `t + horizon >= t_test` has label information that overlaps with the test period.

### The Solution

Remove (purge) training samples whose label computation windows overlap with the test set:

```
purged_train = {i in train : timestamp[i] + label_horizon < test_start_time}
```

### Example

- Label = 24-hour forward return
- Test starts at hour 100
- Training sample at hour 98 uses data from hours 98–122 (overlaps test)
- Training sample at hour 75 uses data from hours 75–99 (overlaps test by 1 hour at boundary)
- Training sample at hour 74 uses data from hours 74–98 (safe, does not reach hour 100)
- Purge samples 75–99 from training

## Embargo

### The Problem

Even after purging, serial correlation in features means that training samples just before the test boundary carry information about the test period through correlated features.

### The Solution

Add a buffer (embargo) between the last training sample and the first test sample:

```
[===TRAIN===][~~EMBARGO~~][===TEST===]
```

The embargo period is excluded from both training and testing. Typical size: 1–5x the autocorrelation decay length of the features.

### Sizing the Embargo

Compute the autocorrelation function (ACF) of your features. The embargo should span enough lags for the ACF to decay below a significance threshold (commonly 2/sqrt(N)):

```python
import numpy as np

def estimate_embargo_size(feature_series: np.ndarray, threshold: float = 0.05) -> int:
    """Estimate embargo size from autocorrelation decay."""
    n = len(feature_series)
    mean = np.mean(feature_series)
    var = np.var(feature_series)
    if var == 0:
        return 1
    acf_values = []
    for lag in range(1, min(n // 4, 100)):
        c = np.mean((feature_series[:-lag] - mean) * (feature_series[lag:] - mean)) / var
        acf_values.append(abs(c))
        if abs(c) < threshold:
            return lag
    return len(acf_values)
```

## Combinatorial Purged Cross-Validation (CPCV)

### Motivation

Standard walk-forward produces a small number of test paths (typically 5–20 folds). This is insufficient for statistical tests like PBO, which need many independent backtest paths. CPCV solves this by generating all valid combinations.

### Algorithm

1. **Partition** the data into `N` contiguous, non-overlapping groups: `G_1, G_2, ..., G_N`
2. **Choose** `k` groups as the test set (typically `k = 2`)
3. **Train** on the remaining `N - k` groups
4. **Purge** training samples at each boundary between a training group and an adjacent test group
5. **Embargo** additional samples after each purge boundary
6. **Repeat** for all `C(N, k)` combinations

### Number of Paths

With `N` groups and `k` test groups:
- Number of combinations: `C(N, k) = N! / (k! * (N-k)!)`
- Each combination produces one backtest path

| N | k | Combinations |
|---|---|---|
| 6 | 2 | 15 |
| 8 | 2 | 28 |
| 10 | 2 | 45 |
| 10 | 3 | 120 |
| 12 | 2 | 66 |

### Purging at Internal Boundaries

Unlike simple walk-forward, CPCV may have train-test boundaries in the middle of the data (not just at the end of training). Every boundary between a training group and a test group requires purging:

```
Groups: [G1:train][G2:test][G3:train][G4:test][G5:train]

Purge zones:
  - End of G1 (train before G2 test)
  - Start of G3 (train after G2 test)
  - End of G3 (train before G4 test)
  - Start of G5 (train after G4 test)
```

### CPCV Implementation Sketch

```python
from itertools import combinations

def cpcv_splits(
    n_samples: int,
    n_groups: int,
    n_test_groups: int,
    purge_window: int = 0,
    embargo_window: int = 0,
) -> list[tuple[list[int], list[int]]]:
    """Generate all CPCV train/test splits."""
    group_size = n_samples // n_groups
    groups = []
    for i in range(n_groups):
        start = i * group_size
        end = (i + 1) * group_size if i < n_groups - 1 else n_samples
        groups.append(list(range(start, end)))

    splits = []
    for test_combo in combinations(range(n_groups), n_test_groups):
        test_set = set()
        for g in test_combo:
            test_set.update(groups[g])

        train_set = set(range(n_samples)) - test_set

        # Purge and embargo at each boundary
        for g in test_combo:
            test_start = groups[g][0]
            test_end = groups[g][-1]
            # Purge before test
            for j in range(max(0, test_start - purge_window), test_start):
                train_set.discard(j)
            # Embargo after test
            for j in range(test_end + 1, min(n_samples, test_end + 1 + embargo_window)):
                train_set.discard(j)

        splits.append((sorted(train_set), sorted(test_set)))
    return splits
```

## Aggregating Results

### Per-Fold Metrics

For each fold, compute:
- **Out-of-sample Sharpe ratio**: `mean(oos_returns) / std(oos_returns) * sqrt(annualization_factor)`
- **Out-of-sample returns**: Total return over the test period
- **Hit rate**: Fraction of correct directional predictions
- **Maximum drawdown**: Worst peak-to-trough decline in test period

### Cross-Fold Aggregation

- **Mean OOS Sharpe**: Average Sharpe across all folds (primary metric)
- **Sharpe ratio of Sharpe ratios**: Stability measure — high variance across folds suggests overfitting
- **Train/Test Sharpe ratio**: If train Sharpe >> test Sharpe, the model is overfitting
- **Rank correlation (IS vs OOS)**: Spearman correlation between in-sample and out-of-sample rankings across parameter sets

A train/test Sharpe ratio above 2.0 is a strong signal of overfitting. Ratios near 1.0 indicate robust generalization.

### Referencia: references/overfit_detection.md

# Overfit Detection Methods

## The Overfitting Problem in Finance

Every backtest is a hypothesis test. When you test many strategies and select the best performer, you are conducting multiple comparisons. The probability that at least one strategy appears profitable by chance increases rapidly with the number of trials.

If you test `N` strategies at a 5% significance level, the probability that at least one falsely appears significant is `1 - (1 - 0.05)^N`. With 20 strategies, this exceeds 64%.

## Deflated Sharpe Ratio (DSR)

### Concept

The Deflated Sharpe Ratio (Bailey and Lopez de Prado, 2014) adjusts the observed Sharpe ratio for:

1. **Number of trials** — How many strategies/parameter sets were tested
2. **Non-normality** — Skewness and kurtosis of returns
3. **Backtest length** — More data points increase statistical reliability

### Formula

The DSR computes the probability that the observed Sharpe ratio exceeds the expected maximum Sharpe ratio under the null hypothesis (all strategies have zero true Sharpe):

```
DSR = Phi((SR_observed - SR_expected_max) / sigma_SR)
```

Where:
- `Phi` = standard normal CDF
- `SR_observed` = Sharpe ratio of the selected strategy
- `SR_expected_max` = expected maximum SR from `N` IID trials
- `sigma_SR` = standard error of the Sharpe ratio estimator

### Standard Error of the Sharpe Ratio

```
sigma_SR = sqrt((1 - gamma_3 * SR + (gamma_4 - 1)/4 * SR^2) / (T - 1))
```

Where:
- `gamma_3` = skewness of returns
- `gamma_4` = kurtosis of returns (not excess kurtosis)
- `T` = number of return observations
- `SR` = observed Sharpe ratio (non-annualized)

### Expected Maximum Sharpe Ratio

Under the null hypothesis that all `N` strategies have zero true Sharpe ratio, the expected maximum observed SR is approximately:

```
E[max(SR)] ≈ Z_inv(1 - 1/N) * (1 - gamma) + gamma * Z_inv(1 - 1/(N*e))
```

Where:
- `Z_inv` = inverse standard normal CDF (quantile function)
- `gamma ≈ 0.5772` = Euler-Mascheroni constant
- `N` = number of independent trials
- `e ≈ 2.7183` = Euler's number

### Interpretation

| DSR Value | Interpretation |
|---|---|
| > 0.95 | Strong evidence of genuine skill |
| 0.80 – 0.95 | Moderate evidence, proceed with caution |
| 0.50 – 0.80 | Weak evidence, likely partially overfitted |
| < 0.50 | Likely overfitted, performance is noise |

### Practical Notes

- `N` must include ALL strategies tested, including those discarded. This is the hardest part — researchers forget or undercount.
- Non-annualized SR should be used in the formula; annualize the result afterward.
- For crypto with 24/7 trading, annualization factor is 365 (daily) or 8760 (hourly).

## Probability of Backtest Overfitting (PBO)

### Concept

PBO (Bailey et al., 2017) uses combinatorial splits to measure the probability that in-sample optimization selects a strategy that underperforms out-of-sample.

### Algorithm

1. Generate multiple train/test splits using CPCV (N groups, k=2 test groups)
2. For each split:
   a. Rank all `S` strategies by in-sample performance
   b. Identify the IS-optimal strategy (best in-sample rank)
   c. Record its out-of-sample rank
3. Compute the relative OOS rank: `w_bar = OOS_rank / S`
4. PBO = fraction of splits where `w_bar > 0.5` (IS-best is worse than OOS median)

### Logit Transformation

For better statistical properties, apply the logit transform before aggregating:

```
lambda = ln(w_bar / (1 - w_bar))
```

PBO is then estimated as the fraction of splits where `lambda > 0` (i.e., OOS rank is worse than median).

### Interpretation

| PBO Value | Interpretation |
|---|---|
| < 0.10 | Low overfitting risk |
| 0.10 – 0.30 | Moderate risk, additional validation recommended |
| 0.30 – 0.50 | High risk, results are unreliable |
| > 0.50 | More likely than not overfitted |

### Stochastic Dominance

PBO can be extended by checking if the IS-optimal strategy's OOS performance distribution stochastically dominates a uniform distribution. If it does not, the strategy selection process has no predictive power.

## Multiple Testing Corrections

When testing multiple hypotheses simultaneously, use corrections to control the family-wise error rate (FWER) or false discovery rate (FDR).

### Bonferroni Correction

The simplest approach — divide the significance level by the number of tests:

```
alpha_adjusted = alpha / N
```

Conservative but guarantees FWER control. With 100 strategies at alpha=0.05, each strategy must achieve p < 0.0005.

### Holm-Bonferroni (Step-Down)

Less conservative than Bonferroni while still controlling FWER:

1. Sort p-values: `p_(1) <= p_(2) <= ... <= p_(N)`
2. For each `i`, reject H_i if `p_(i) <= alpha / (N - i + 1)`
3. Stop at the first non-rejection

### Benjamini-Hochberg (FDR Control)

Controls the expected proportion of false discoveries rather than FWER:

1. Sort p-values: `p_(1) <= p_(2) <= ... <= p_(N)`
2. Find largest `k` where `p_(k) <= k/N * alpha`
3. Reject hypotheses 1 through k

### Which to Use

- **Bonferroni**: When false positives are catastrophic (capital at risk)
- **Holm**: When you want more power than Bonferroni with same FWER guarantee
- **BH**: When testing many strategies and some false positives are acceptable (screening stage)

For trading: Use Bonferroni or Holm when selecting a single strategy to deploy. Use BH when screening a large universe of strategies for further investigation.

## Minimum Backtest Length (MinBTL)

The minimum number of observations needed for a Sharpe ratio to be statistically significant:

```
MinBTL = 1 + (1 - gamma_3 * SR + (gamma_4 - 1)/4 * SR^2) * (Z_alpha / SR)^2
```

Where:
- `Z_alpha` = critical value for desired significance level
- `SR` = target non-annualized Sharpe ratio
- `gamma_3`, `gamma_4` = skewness, kurtosis of returns

### Practical Implications

For a strategy with daily SR = 0.1 (annualized ~1.6) and normal returns:
- At 95% confidence: MinBTL ≈ 385 daily observations (1.05 years)
- At 99% confidence: MinBTL ≈ 664 daily observations (1.82 years)

For crypto with hourly SR = 0.01:
- At 95% confidence: MinBTL ≈ 38,416 hourly observations (4.4 years)

This underscores why high-frequency strategies need very long backtests or very high Sharpe ratios to be statistically validated.

## Combining DSR and PBO

Use both metrics together for robust overfit detection:

1. **DSR** answers: "Is this Sharpe ratio likely real given how many things I tried?"
2. **PBO** answers: "Does my strategy selection process have any predictive power?"

If DSR > 0.95 AND PBO < 0.20, the strategy has strong evidence of genuine edge. If either metric fails, additional out-of-sample testing (preferably paper trading) is essential before deploying capital.

### Referencia: references/practical_guide.md

# Walk-Forward Validation — Practical Guide for Crypto

## Window Size Selection

### Principles

1. **Train window must span at least one full market cycle** — or else the model only learns one regime. In crypto, a "cycle" can be as short as 2–4 weeks for altcoins.
2. **Train window should not be so long that stale data dilutes signal** — crypto market structure changes rapidly. Data from 2 years ago may be from a fundamentally different market.
3. **Test window must be long enough for statistical significance** — a 1-day test window produces noisy estimates. Aim for at least 30 independent observations.
4. **Step size determines compute cost** — smaller steps = more folds = better estimates but longer runtime.

### Recommended Window Sizes

| Strategy Type | Train | Test | Step | Embargo | Rationale |
|---|---|---|---|---|---|
| HFT / Scalping (1-5min bars) | 3-7 days | 1 day | 1 day | 2-4 hours | Microstructure changes fast |
| Intraday (15min-1h bars) | 14-30 days | 3-7 days | 3 days | 12-24 hours | Need multiple day/night cycles |
| Swing (4h-daily bars) | 30-90 days | 7-14 days | 7 days | 2-5 days | Must span regime transitions |
| Position (daily-weekly) | 90-180 days | 14-30 days | 14 days | 5-10 days | Longer horizon, need full cycles |
| ML Features (daily) | 60-120 days | 14-21 days | 7 days | 3-5 days | Balance data volume vs recency |

### Crypto vs Equities

| Aspect | Equities | Crypto |
|---|---|---|
| Typical train window | 1-3 years (252-756 bars) | 1-6 months (30-180 bars) |
| Market hours | 6.5h/day, 252 days/year | 24/7/365 |
| Regime change frequency | Quarterly to yearly | Weekly to monthly |
| Data availability | Decades | 2-8 years for most tokens |
| Survivorship bias severity | Moderate | Severe (tokens delist constantly) |
| Recommended approach | Expanding window | Rolling window |

## Regime-Aware Validation

### Why Regimes Matter

A strategy that works in high-volatility trending markets may lose money in low-volatility mean-reverting markets. If your train and test windows both fall within the same regime, validation results are misleading.

### Simple Regime Detection for Splits

Use volatility and trend to classify market regime before splitting:

```python
import numpy as np

def classify_regime(
    returns: np.ndarray,
    lookback: int = 20,
) -> np.ndarray:
    """Classify each bar as trending-volatile, trending-quiet, etc."""
    n = len(returns)
    regimes = np.empty(n, dtype="U20")
    for i in range(lookback, n):
        window = returns[i - lookback : i]
        vol = np.std(window) * np.sqrt(365)  # Annualized
        trend = np.sum(window)  # Cumulative return
        if vol > 0.8:  # High vol threshold (crypto)
            regimes[i] = "trending-up" if trend > 0 else "trending-down"
        else:
            regimes[i] = "quiet-up" if trend > 0 else "quiet-down"
    regimes[:lookback] = "unknown"
    return regimes
```

### Regime-Aware Split Strategy

1. **Classify** each bar into a regime
2. **Verify** that each train window spans at least 2 different regimes
3. **Track** the regime composition of each test window
4. **Report** performance broken down by regime
5. **Flag** folds where train and test are the same regime

If most folds have matching train/test regimes, the validation is unreliable for out-of-regime performance.

## Common Validation Mistakes

### 1. Not Purging Labels

**Mistake:** Using 5-day forward returns as labels without purging the 5-day overlap between train and test.

**Result:** Information leakage inflates accuracy by 10–30%.

**Fix:** Always purge `label_horizon` bars from the end of training data.

### 2. Using Future Information in Features

**Mistake:** Normalizing features using the full dataset's mean/std before splitting.

**Result:** Test set statistics leak into training features.

**Fix:** Fit scalers/normalizers on training data only. Transform test data using training statistics.

```python
# WRONG
scaler.fit(all_data)
train_scaled = scaler.transform(train_data)
test_scaled = scaler.transform(test_data)

# RIGHT
scaler.fit(train_data)
train_scaled = scaler.transform(train_data)
test_scaled = scaler.transform(test_data)
```

### 3. Optimizing Hyperparameters on Test Data

**Mistake:** Using the test fold to tune hyperparameters (learning rate, lookback periods, thresholds).

**Result:** Hyperparameters are fit to the test set, destroying its validity.

**Fix:** Use a three-way split: train / validation / test. Tune on validation, evaluate on test. Or use nested cross-validation.

### 4. Ignoring Transaction Costs

**Mistake:** Computing walk-forward returns without accounting for spreads, slippage, and fees.

**Result:** A strategy with 200 trades/day and 0.5 bps edge appears profitable, but 5 bps per round-trip cost makes it a loser.

**Fix:** Always include realistic transaction costs. For Solana DEX trades, minimum 0.3% (swap fee + slippage).

### 5. Too Few Folds

**Mistake:** Using 3 walk-forward folds and reporting the average.

**Result:** High variance in the estimate. One good or bad fold dominates.

**Fix:** Use at least 8–10 folds, or CPCV to generate 15+ paths.

### 6. Reporting In-Sample Metrics

**Mistake:** Reporting training set performance alongside (or instead of) test set performance.

**Result:** Misleading impression of strategy quality.

**Fix:** Only report out-of-sample metrics. Track the train/test ratio as an overfitting diagnostic.

### 7. Not Accounting for Multiple Testing

**Mistake:** Testing 50 parameter combinations, selecting the best, and reporting its backtest result.

**Result:** The best of 50 random strategies will look profitable by chance alone.

**Fix:** Use the Deflated Sharpe Ratio to adjust for the number of trials.

### 8. Survivorship Bias in Token Universe

**Mistake:** Backtesting on tokens that exist today, ignoring delisted tokens.

**Result:** Returns are inflated because you only test tokens that survived.

**Fix:** Include delisted tokens in your universe, or at minimum report that survivorship bias is present and estimate its magnitude.

## Validation Checklist

Before trusting any backtest result, verify:

- [ ] Time series ordering is respected (no future data in training)
- [ ] Labels are purged at train/test boundaries
- [ ] Embargo period is applied after purging
- [ ] Features are normalized using training data only
- [ ] Transaction costs are included (realistic for the venue)
- [ ] At least 8 walk-forward folds or 15 CPCV paths
- [ ] Deflated Sharpe Ratio > 0.95 (accounting for all trials)
- [ ] PBO < 0.30 (if using strategy selection)
- [ ] Train/test Sharpe ratio < 2.0
- [ ] Results reported per-regime if possible
- [ ] Hyperparameters tuned on validation set, not test set
- [ ] Survivorship bias acknowledged or addressed

## Reporting Template

When presenting walk-forward results, include:

```
Walk-Forward Validation Report
==============================
Window type:        Rolling (90-day train, 14-day test)
Number of folds:    12
Embargo:            3 days
Purge horizon:      1 day
Date range:         2025-01-01 to 2025-12-31
Strategies tested:  25

Out-of-Sample Results:
  Mean Sharpe:        1.42
  Sharpe Std Dev:     0.38
  Mean Return:        +3.2% per fold
  Win Rate:           58.3%
  Max Drawdown:       -8.7%

Overfitting Metrics:
  Train/Test SR:      1.65
  Deflated SR:        0.87
  PBO:                0.22

Regime Breakdown:
  Trending-Up:    SR 2.1 (4 folds)
  Trending-Down:  SR 0.8 (3 folds)
  Quiet:          SR 1.1 (5 folds)
```


---

## SKILL: weekly-performance-digest

- Fuente: `tradermonty/claude-trading-skills` → `skills/weekly-performance-digest` (MIT)
- Cuándo usarla: Generate a weekly performance summary from closed trader-memory-core theses — win rate, expectancy, profit factor, R-multiple, MAE/MFE, and win/loss pattern analysis by source skill, exit reason, thesis type, sector, and mechanism. No API required; pure local calculation.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/weekly-performance-digest/` (requirements.txt, generate_weekly_digest.py)

# Weekly Performance Digest

## Overview

Weekly Performance Digest aggregates the trades you closed during a week into a single
performance report. It reads CLOSED theses tracked by `trader-memory-core`
(`state/theses/th_*.yaml`), computes headline metrics (win rate, expectancy, profit
factor, R-multiple, MAE/MFE), breaks results down across several pattern dimensions
(source skill, exit reason, thesis type, sector, mechanism tag, screening grade), and
surfaces the week's biggest winners, losers, and lessons. Output is a JSON record plus
a human-readable Markdown report. Pure calculation — no API key required.

## When to Use

- At the end of a trading week to review aggregate realized performance
- To measure win rate and expectancy across all closed positions
- To see which source skills, exit reasons, sectors, or mechanisms drove wins vs losses
- To feed a month-end review (combine four weekly digests) or a postmortem
- For a quick "what worked / what didn't" snapshot grounded in real closed trades

## When Not to Use

- For a single-trade deep review — use `trade-performance-coach`
- For signal-level true/false-positive classification — use `signal-postmortem`
- For buy/sell recommendations or position sizing — this skill is descriptive only

## Prerequisites

- Python 3.9+ with `PyYAML` (already a repo dependency)
- A `trader-memory-core` state directory of thesis YAML files (`state/theses/`)
- No API key required

## Workflow

### Step 1: Run the digest for a week

```bash
python3 skills/weekly-performance-digest/scripts/generate_weekly_digest.py \
  --state-dir state/theses \
  --from-date 2026-06-13 --to-date 2026-06-20 \
  --output-dir reports/ -v
```

Defaults: `--state-dir state/theses`, `--from-date` = 7 days before `--to-date`,
`--to-date` = today, `--output-dir reports/`. With no date flags it digests the
trailing 7 days.

### Step 2: Read the report

The run writes `reports/weekly_digest_<to-date>.json` and
`reports/weekly_digest_<to-date>.md`. Review the Markdown for the executive summary,
metrics table, pattern breakdowns, and top winners/losers; consume the JSON downstream.

### Step 3 (optional): Feed downstream

Combine several weekly JSON digests for a monthly review, or pass the JSON to a
postmortem/coach step. The skill is descriptive — act on its findings via your normal
review process.

## How It Works

- **Trade selection.** A trade counts in a week if its `exit.actual_date` falls in
  `[from-date, to-date]` and `status == CLOSED`.
- **Win/loss.** `outcome.pnl_dollars > 0` is a winner, `< 0` a loser, `== 0` breakeven;
  `win_rate = winners / total_trades`.
- **R-multiple.** `pnl_dollars / ((entry.actual_price − exit.stop_loss) × position.shares)`.
  (Stop-loss is read from `exit.stop_loss`, per the real thesis schema.)
- **Double-counting safeguard.** A CLOSED thesis's `outcome.pnl_dollars` is the
  *cumulative* realized P&L across all trims plus the final leg. Headline metrics use
  that cumulative value over CLOSED theses only. The separate `partial_trims` block
  scans `status_history[]` of **PARTIALLY_CLOSED theses only** (still open) and is
  reported for information — it is **never** added into the headline totals/win-rate.
  A position trimmed in week 1 then closed in week 2 therefore shows as a partial trim
  in week 1 and inside week 2's CLOSED headline; that is intended, not a duplicate.

## Output Format

### JSON (`weekly_digest_<to-date>.json`)

```json
{
  "schema_version": "1.0",
  "report_type": "weekly_performance_digest",
  "period": {"from": "2026-06-13", "to": "2026-06-20"},
  "generated_at": "2026-06-20T21:39:07Z",
  "summary": {
    "total_trades": 2, "winners": 1, "losers": 1, "breakeven": 0,
    "win_rate": 0.5, "expectancy": 25.0, "profit_factor": 2.0,
    "total_realized_pnl": 50.0, "total_realized_pnl_pct": 4.17
  },
  "metrics": {
    "avg_winner": 100.0, "avg_loser": -50.0,
    "largest_winner": 100.0, "largest_loser": -50.0,
    "avg_holding_days_winners": 9.0, "avg_holding_days_losers": 6.0,
    "r_multiple_avg": 0.25, "r_multiple_stdev": 1.06,
    "avg_mae_pct": -3.75, "avg_mfe_pct": 4.5
  },
  "pattern_analysis": {
    "by_source_skill": {"...": {"wins": 1, "losses": 0, "total": 1, "win_rate": 1.0}},
    "by_exit_reason": {}, "by_thesis_type": {}, "by_sector": {},
    "by_mechanism_tag": {}, "by_screening_grade": {}
  },
  "partial_trims": {"count": 0, "total_realized_pnl": 0.0, "trims": []},
  "lessons": {"top_wins": [], "top_losses": [], "process_improvements": []}
}
```

### Markdown (`weekly_digest_<to-date>.md`)

Sections: `# Weekly Performance Digest`, `## Executive Summary`,
`## Performance Metrics`, `## Pattern Analysis`, `## Lessons Learned`
(`### Top Winners` / `### Top Losers` / `### Process Improvements`).

An empty week still produces a valid report with zeroed metrics (exit code 0).

## Resources

- `scripts/generate_weekly_digest.py` — digest generator (JSON + Markdown)
- `references/weekly-digest-metrics.md` — metric formulas and interpretation

## Key Principles

1. **Closed trades only for headline numbers** — cumulative `outcome.*`, keyed on exit date.
2. **No double-counting** — partial trims are informational and excluded from totals.
3. **Pattern attribution** — every win/loss is attributed across multiple dimensions.
4. **Descriptive, not prescriptive** — the digest reports; you decide.

### Referencia: references/weekly-digest-metrics.md

# Weekly Digest — Metric Definitions

Definitions and formulas used by `generate_weekly_digest.py`. All headline metrics are
computed over **CLOSED theses only**, selected by `exit.actual_date` within the week.

## Win / loss classification

- A trade is a **winner** when `outcome.pnl_dollars > 0`, a **loser** when `< 0`, and
  **breakeven** when `== 0`.
- When `pnl_dollars` is absent, `pnl_pct` is used as a fallback signal of sign.

## Headline metrics

| Metric | Formula |
|---|---|
| Win rate | `winners / total_trades` |
| Expectancy | `mean(pnl_dollars)` across all closed trades (avg P&L per trade) |
| Profit factor | `gross_profit / abs(gross_loss)`; `null` when there are no losers (undefined) |
| Total realized P&L | `sum(pnl_dollars)` |
| Avg / largest winner | `mean` / `max` of winning `pnl_dollars` |
| Avg / largest loser | `mean` / `min` of losing `pnl_dollars` |
| Avg holding days (W/L) | `mean(holding_days)` for winners and losers separately |

`expectancy` can also be reasoned about as
`(avg_win × win_rate) + (avg_loss × loss_rate)`; the script computes it directly as the
mean P&L per trade, which is equivalent.

## R-multiple

```
R = pnl_dollars / initial_risk
initial_risk = (entry.actual_price − exit.stop_loss) × position.shares
```

- Stop-loss is read from **`exit.stop_loss`** (the real thesis schema location).
- `R` is `null` when any of `pnl_dollars`, `entry.actual_price`, `exit.stop_loss`, or
  `position.shares` is missing, or when initial risk is zero.
- `r_multiple_stdev` uses the sample standard deviation; it is `0.0` for a single trade.

## MAE / MFE

- **MAE** (Maximum Adverse Excursion, `outcome.mae_pct`) is the worst drawdown while the
  position was open. By convention it is **≤ 0** (adverse).
- **MFE** (Maximum Favorable Excursion, `outcome.mfe_pct`) is the best unrealized gain
  while open. By convention it is **≥ 0** (favorable).
- `trader-memory-core` does not clamp these fields, so an always-profitable trade can
  carry `mae_pct > 0` (and an always-underwater one `mfe_pct < 0`). The digest **clamps
  on read** to preserve the convention: MAE → `min(value, 0)`, MFE → `max(value, 0)`.
- The digest aggregates `avg_mae_pct` and `avg_mfe_pct` across closed trades. Large
  average MFE relative to realized P&L suggests trades are being exited too early; large
  average MAE relative to risk suggests stops are too wide or entries are mistimed.

## Pattern analysis

Each closed trade is bucketed across six dimensions, each reporting `{wins, losses,
total, win_rate}` (win_rate = wins / decided, where decided = wins + losses):

| Dimension | Source field |
|---|---|
| `by_source_skill` | `origin.skill` |
| `by_exit_reason` | `exit.exit_reason` |
| `by_thesis_type` | `thesis_type` |
| `by_sector` | `market_context.sector` |
| `by_mechanism_tag` | `mechanism_tag` |
| `by_screening_grade` | `origin.screening_grade` |

Missing values bucket as `unknown` rather than dropping the trade.

## Partial trims (informational only)

`partial_trims` scans `status_history[]` of **PARTIALLY_CLOSED** theses for entries with
a `realized_pnl` whose `at` date is in-week. These are realized gains/losses on still-open
positions; they are reported separately and **never** added to the headline totals or
win-rate, because a CLOSED thesis's `outcome.pnl_dollars` already includes its own trims
cumulatively (counting both would double-count).

## Luck vs. skill heuristics

- A small sample (few closed trades) makes win rate and expectancy noisy — treat a single
  week as directional, not conclusive; confirm patterns across multiple weeks.
- Consistent positive expectancy with R-multiple average ≥ 0 across many trades is the
  signal of an edge; a high win rate with negative expectancy means losers are too large.


---

## SKILL: yield-analysis

- Fuente: `agiprolabs/claude-trading-skills` → `skills/yield-analysis` (MIT)
- Cuándo usarla: DeFi yield evaluation including fee APR, real vs nominal yield, net APY after costs, and yield sustainability analysis
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/yield-analysis/` (yield_calculator.py, yield_comparison.py)

# Yield Analysis — DeFi Yield Evaluation & Comparison

DeFi yields are often misleading. A pool advertising 200% APY may deliver negative real returns once you account for impermanent loss, gas costs, and emission token depreciation. This skill provides the framework to decompose, evaluate, and compare yield opportunities accurately.

## Why Yield Analysis Matters

Most DeFi yield dashboards show **nominal** yield — the headline number. Real yield requires decomposing that number into its components and subtracting all costs. Without this decomposition:

- LPs chase high-APY pools that destroy capital through IL
- Emission-driven yields collapse as reward tokens lose value
- Gas and rebalancing costs eat into thin margins
- Opportunity cost is ignored (you could be staking SOL at ~7%)

## Yield Components

Every DeFi yield breaks down into one or more of these sources:

### 1. Trading Fee Income
Swap fees earned by liquidity providers. This is the most sustainable yield source because it comes from real economic activity.

```python
fee_apr = (daily_volume * fee_rate / tvl) * 365
your_daily_fees = daily_volume * fee_rate * (your_liquidity / total_liquidity)
```

For CLMM pools (concentrated liquidity), fee income is amplified by how tightly you concentrate your range. See the `lp-math` skill for CLMM mechanics.

### 2. Token Emissions / Incentives
Protocol reward tokens distributed to LPs. Often the largest component of advertised yields, but frequently unsustainable.

```python
emission_apr = (daily_emission_tokens * token_price * 365) / tvl
```

The critical question: will the emission token hold its value? If everyone farms and dumps, the token depreciates and actual USD yield is much lower.

### 3. Lending Interest
Interest earned from lending protocol deposits (Marginfi, Kamino, Solend). Driven by borrowing demand — more sustainable than emissions but fluctuates with utilization.

### 4. Staking Rewards
Validator staking yield (~7% APR on Solana) or liquid staking token (LST) yield. The baseline risk-free rate for the Solana ecosystem.

## Real vs Nominal Yield

| Metric | What It Includes | What It Ignores |
|--------|-----------------|-----------------|
| Nominal APY | Fee APR + emission APR (compounded) | IL, gas, depreciation, risk |
| Real Yield | Everything, net of all costs | Nothing — this is the true return |

### Real Yield Formula

```
real_yield = fee_apr
           + emission_apr × (1 - emission_depreciation)
           - il_cost
           - gas_cost
           - rebalancing_cost
```

Where:
- `fee_apr`: annualized fee income as fraction of position value
- `emission_apr`: annualized emission income at current token price
- `emission_depreciation`: expected decline in emission token price (0.0 to 1.0)
- `il_cost`: expected impermanent loss as annualized rate (see `impermanent-loss` skill)
- `gas_cost`: transaction fees for deposits, withdrawals, claims, compounds
- `rebalancing_cost`: for CLMM positions, cost of rebalancing out-of-range positions

### Example: SOL-USDC Pool

```
Nominal APY displayed:    45%
Decomposition:
  Fee APR:               18%
  Emission APR:          30%  (RAY token rewards)
  Emission depreciation: 40%  (RAY down 40% over 30d)
  Effective emission:    18%  (30% × 0.6)
  IL cost (estimated):   12%  (SOL volatile against USDC)
  Gas + rebalance:        1%

Real yield = 18% + 18% - 12% - 1% = 23%
```

The 45% nominal yield is really 23% after accounting for all factors.

## Fee APR Calculation

### Constant-Product Pools

```python
fee_apr = fee_rate * daily_volume / tvl * 365
```

For a pool with 0.25% fee rate, $2M daily volume, and $10M TVL:

```
fee_apr = 0.0025 * 2_000_000 / 10_000_000 * 365 = 18.25%
```

### Concentrated Liquidity (CLMM) Pools

CLMM fee income depends on your position range relative to trading activity:

```python
# Simplified — see lp-math skill for full CLMM math
fee_apr = fee_rate * daily_volume_in_range / position_liquidity * 365
```

Tighter ranges earn higher fees per dollar deployed but go out of range more frequently, requiring rebalancing.

### Per-LP Share

```python
your_share = your_liquidity / total_pool_liquidity
your_daily_fees = total_daily_fees * your_share
```

## Emission Sustainability

### The Death Spiral Pattern

1. Protocol launches with high emission rewards → attracts LPs
2. TVL grows → yield per LP drops → protocol increases emissions
3. LPs farm and dump emission tokens → token price drops
4. Lower token price → lower USD-denominated yield
5. LPs leave → TVL drops → protocol increases emissions further
6. Spiral continues until emissions stop or protocol fails

### Sustainability Metrics

```python
# Protocol P/E ratio
pe_ratio = fully_diluted_valuation / annual_protocol_revenue

# Revenue-to-emission ratio (> 1.0 is sustainable)
sustainability = annual_revenue / annual_emission_value

# Token velocity (high = lots of sell pressure)
velocity = daily_emission_selling / daily_token_volume
```

**Interpretation:**
- P/E < 20 and sustainability > 1.0: Likely sustainable yield
- P/E 20-100 and sustainability 0.3-1.0: Moderate risk
- P/E > 100 or sustainability < 0.3: Emission-dependent, high risk

### Red Flags

- APY > 100% sourced primarily from emissions
- Emission token price declining consistently over 30+ days
- TVL declining while emission rate stays constant or increases
- Protocol revenue is a small fraction of emission cost
- No vesting or lockup on emission tokens

## Yield Comparison Framework

When comparing yield opportunities, normalize across these dimensions:

### 1. Same-Asset Basis

Compare like for like. For SOL:

| Strategy | Expected APR | Risk Level | IL Exposure |
|----------|-------------|------------|-------------|
| Native staking | ~7% | Low | None |
| Liquid staking (mSOL) | ~7.5% | Low | Minimal |
| SOL-USDC LP (Orca) | ~15-25% | Medium | High |
| SOL lending (Marginfi) | ~3-8% | Low-Med | None |
| Leveraged yield | ~20-50% | High | Varies |

### 2. Risk-Adjusted Yield

```python
risk_score = (
    il_risk * 0.3 +
    smart_contract_risk * 0.25 +
    emission_sustainability_risk * 0.2 +
    liquidity_risk * 0.15 +
    protocol_risk * 0.1
)

risk_adjusted_yield = net_apr / risk_score
```

### 3. Total Cost Accounting

Include all costs:
- Impermanent loss (see `impermanent-loss` skill)
- Gas fees for all transactions (deposit, withdraw, claim, compound)
- Opportunity cost (what you could earn risk-free)
- Smart contract risk premium
- Rebalancing costs (CLMM positions)

## Solana Yield Sources

### Liquidity Provision

| Protocol | Pool Types | Fee Tiers | Notes |
|----------|-----------|-----------|-------|
| Raydium | CPMM, CLMM | 0.01-1% | Largest Solana DEX by volume |
| Orca | CLMM (Whirlpool) | 0.01-2% | Concentrated liquidity focused |
| Meteora | DLMM, Dynamic | Variable | Dynamic fee adjustment |

### Lending

| Protocol | Assets | Typical APR | Notes |
|----------|--------|-------------|-------|
| Marginfi | SOL, USDC, etc. | 2-10% | Points program active |
| Kamino | SOL, USDC, etc. | 2-12% | Auto-compound vaults |
| Solend | SOL, USDC, etc. | 1-8% | Established protocol |

### Staking

| Method | APR | Lock Period | Notes |
|--------|-----|------------|-------|
| Native SOL staking | ~7% | 1 epoch (~2d) | Validator selection matters |
| mSOL (Marinade) | ~7.2% | Instant | Liquid, usable in DeFi |
| jitoSOL (Jito) | ~7.5% | Instant | Includes MEV rewards |
| bSOL (BlazeStake) | ~7% | Instant | Decentralized validator set |

## Data Sources

### DeFiLlama Yields API (Free, No Auth)

```python
import httpx

# All yield pools
pools = httpx.get("https://yields.llama.fi/pools").json()

# Filter for Solana
solana_pools = [p for p in pools["data"] if p["chain"] == "Solana"]

# Sort by TVL
solana_pools.sort(key=lambda p: p.get("tvlUsd", 0), reverse=True)
```

Response fields: `pool`, `chain`, `project`, `symbol`, `tvlUsd`, `apy`, `apyBase`, `apyReward`, `il7d`, `exposure`.

### Protocol-Specific APIs

- Raydium: `https://api-v3.raydium.io/pools/info/list`
- Orca: `https://api.mainnet.orca.so/v1/whirlpool/list`
- Marginfi: On-chain account data via Solana RPC

## Integration with Other Skills

- **`lp-math`**: AMM formulas for fee calculation and position math
- **`impermanent-loss`**: IL estimation for real yield calculation
- **`defillama-api`**: Fetching yield and TVL data across protocols
- **`risk-management`**: Portfolio-level yield allocation decisions
- **`position-sizing`**: How much capital to allocate to yield strategies

## Files

### References
- `references/yield_math.md` — Fee APR, APR/APY conversion, net yield formulas, break-even analysis
- `references/sustainability_analysis.md` — Emission sustainability metrics, death spiral patterns, real yield identification

### Scripts
- `scripts/yield_calculator.py` — Offline yield calculator with fee APR, IL estimation, net yield, break-even, and sensitivity analysis
- `scripts/yield_comparison.py` — Fetches DeFiLlama yield data and compares Solana yield opportunities with risk-adjusted ranking

### Referencia: references/sustainability_analysis.md

# Sustainability Analysis — Evaluating DeFi Yield Durability

## Protocol Revenue vs Emissions

Every DeFi protocol that pays yield through token emissions faces a fundamental question: can the protocol generate enough real revenue to justify its token's value?

### Revenue Sources

- **Trading fees**: Protocol's share of swap fees (e.g., Raydium takes a cut of LP fees)
- **Lending spread**: Difference between borrow and lend rates
- **Liquidation fees**: Earned when undercollateralized positions are liquidated
- **Protocol-owned liquidity (POL)**: Yield from the protocol's own LP positions
- **Treasury yield**: Interest on treasury holdings

### Emission Costs

- **LP incentives**: Tokens distributed to liquidity providers
- **Staking rewards**: Tokens for governance stakers
- **Referral/growth programs**: Tokens for user acquisition
- **Team/investor unlocks**: Vesting schedules adding supply

### The Core Equation

```
sustainable = (annual_protocol_revenue >= annual_emission_cost_usd)
```

When revenue exceeds emission costs, the protocol can sustain its yield without diluting token holders. When emissions exceed revenue, the protocol is paying for growth with inflation.

## The Yield Farming Death Spiral

### Phase 1: Launch (Weeks 1-4)
- Protocol announces high emission rewards (200%+ APY)
- Capital floods in seeking yield
- TVL grows rapidly
- Token price rises on hype and buying pressure from yield seekers

### Phase 2: Peak (Weeks 4-12)
- TVL stabilizes at high level
- Yield per LP drops as more capital enters
- Early farmers begin selling emission tokens
- Token price plateaus

### Phase 3: Decline (Weeks 12-26)
- Farmers sell emission tokens → price drops
- Lower token price → lower USD yield
- LPs start leaving → TVL drops
- Protocol may increase emissions to retain LPs → more sell pressure
- Remaining LPs earn less and face higher IL from declining token

### Phase 4: Collapse or Stabilization
- **Collapse**: TVL drops 90%+, token price drops 95%+, protocol becomes ghost chain
- **Stabilization**: Revenue-generating protocols find equilibrium where real fees sustain modest yield

### Key Observation

The difference between collapse and stabilization is whether the protocol generates real trading volume and fees independent of emission incentives. Protocols with genuine product-market fit (Raydium, Orca) stabilize. Pure yield farms collapse.

## Sustainability Metrics

### Protocol P/E Ratio

```
pe_ratio = fully_diluted_valuation / annual_protocol_revenue
```

| P/E Range | Interpretation |
|-----------|---------------|
| < 10 | Strong value — revenue well supports valuation |
| 10-30 | Healthy — typical for established DeFi |
| 30-100 | Growth premium — market expects revenue growth |
| 100-500 | Speculative — valuation not supported by current revenue |
| > 500 | Extremely speculative — almost entirely narrative-driven |

### Revenue-to-Emission Ratio

```
rev_emission_ratio = annual_revenue / annual_emission_value_usd
```

| Ratio | Interpretation |
|-------|---------------|
| > 1.0 | Sustainable — revenue covers emissions |
| 0.5-1.0 | Approaching sustainability |
| 0.1-0.5 | Emission-dependent — moderate risk |
| < 0.1 | Highly unsustainable — yield is almost entirely inflationary |

### Emission Sell Pressure

```
daily_sell_pressure = daily_emissions_usd / daily_token_volume
```

| Sell Pressure | Interpretation |
|--------------|---------------|
| < 1% | Minimal impact on token price |
| 1-5% | Noticeable but manageable |
| 5-15% | Significant downward pressure |
| > 15% | Severe — token likely in decline |

### TVL Retention Rate

```
tvl_retention_30d = current_tvl / tvl_30d_ago
```

Values below 0.8 (20% TVL loss in 30 days) signal potential death spiral.

## Real Yield vs Inflationary Yield

### Real Yield Protocols

Yield comes from actual economic activity:
- **DEX fees**: Traders pay to swap tokens — LPs earn from real demand
- **Lending interest**: Borrowers pay interest — lenders earn from real demand
- **Staking rewards**: Network inflation distributed to validators/delegators (predictable, protocol-level)
- **MEV sharing**: Jito shares MEV revenue with jitoSOL holders

### Inflationary Yield

Yield comes from new token creation:
- **Farm rewards**: Protocol mints tokens and distributes them
- **Points programs**: Promise of future token airdrop (deferred inflation)
- **Governance staking rewards**: Staking rewards funded by token inflation

### How to Identify Real Yield

```python
def is_real_yield(pool: dict) -> bool:
    """Check if a pool's yield is primarily from real sources.

    Args:
        pool: Pool data with apyBase and apyReward fields.

    Returns:
        True if base (fee) APY exceeds reward (emission) APY.
    """
    base_apy = pool.get("apyBase", 0) or 0
    reward_apy = pool.get("apyReward", 0) or 0
    total = base_apy + reward_apy
    if total == 0:
        return False
    return base_apy / total > 0.5
```

DeFiLlama separates `apyBase` (real, from fees) and `apyReward` (from emissions), making this check straightforward.

## Red Flags Checklist

### High Risk Indicators

- [ ] APY > 100% with majority from emissions
- [ ] Emission token price down > 30% in 30 days
- [ ] TVL declining while emissions stay constant
- [ ] Protocol revenue < 10% of emission cost
- [ ] No token vesting — all emissions immediately sellable
- [ ] Team allocation > 30% of total supply
- [ ] Emission schedule increases over time (not decreasing)
- [ ] No working product beyond yield farm
- [ ] Anonymous team with no track record
- [ ] Forked code with minimal changes

### Moderate Risk Indicators

- [ ] APY 50-100% with mixed fee/emission sources
- [ ] Emission token price stable but flat
- [ ] TVL stable but not growing
- [ ] Protocol revenue covers 30-80% of emissions
- [ ] Some token vesting (3-12 month)

### Low Risk Indicators

- [ ] APY < 30% primarily from fees
- [ ] Established protocol (6+ months, audited)
- [ ] Growing or stable TVL
- [ ] Revenue exceeds emissions
- [ ] Long vesting schedules for team tokens
- [ ] Multiple audits from reputable firms

## Historical Patterns

### Common Yield Farming Collapse Patterns

**Pattern 1: The Vampire Attack Fade**
- Protocol launches by offering higher yields than competitors
- Attracts TVL initially
- Cannot sustain yields without real product differentiation
- TVL leaves when emissions drop

**Pattern 2: The Governance Token Illusion**
- Protocol distributes governance token with no revenue sharing
- Token has voting power but no cash flow
- Market initially values governance, then realizes it is worthless
- Token price trends to zero, yield trends to zero

**Pattern 3: The Leverage Spiral**
- Protocol enables leveraged yield farming
- Users borrow to farm, multiplying apparent TVL
- Market downturn triggers cascading liquidations
- TVL collapses 80%+ in days

### Solana-Specific Examples

Solana's low transaction costs enable more frequent compounding and rebalancing, which amplifies both the benefits and risks of yield strategies. Protocols that survived the 2022-2023 bear market (Raydium, Orca, Marinade) proved their revenue models. Newer protocols should be evaluated more skeptically until they demonstrate sustainable revenue.

## Evaluation Framework

When assessing any yield opportunity:

1. **Decompose**: What percentage comes from fees vs emissions?
2. **Validate**: Is the fee APR consistent with actual trading volume?
3. **Project**: If emission token drops 50%, is the yield still attractive?
4. **Compare**: Does the risk-adjusted yield beat SOL staking (7%)?
5. **Monitor**: Set alerts for TVL changes, emission token price, volume trends

```python
def yield_sustainability_score(
    fee_pct: float,
    rev_emission_ratio: float,
    tvl_retention_30d: float,
    token_price_change_30d: float,
) -> float:
    """Score yield sustainability from 0 (unsustainable) to 100 (sustainable).

    Args:
        fee_pct: Fraction of yield from fees (0-1).
        rev_emission_ratio: Protocol revenue / emission cost.
        tvl_retention_30d: Current TVL / TVL 30 days ago.
        token_price_change_30d: Price change ratio (e.g. 0.8 = down 20%).

    Returns:
        Sustainability score 0-100.
    """
    score = 0.0
    score += min(fee_pct, 1.0) * 35          # Max 35 for 100% fee-based
    score += min(rev_emission_ratio, 1.0) * 25 # Max 25 for revenue-backed
    score += min(tvl_retention_30d, 1.2) / 1.2 * 20  # Max 20 for stable TVL
    price_factor = max(min(token_price_change_30d, 1.5), 0) / 1.5
    score += price_factor * 20                 # Max 20 for stable/rising token
    return round(score, 1)
```

### Referencia: references/yield_math.md

# Yield Math — Formulas & Worked Examples

## Fee APR Calculation

### Constant-Product Pools (x × y = k)

All LPs share fees proportionally to their liquidity share:

```
fee_apr = fee_rate × daily_volume / tvl × 365
```

**Worked Example:**
- Pool: SOL-USDC on Raydium
- Fee rate: 0.25% (0.0025)
- Daily volume: $3,000,000
- TVL: $12,000,000

```
daily_fees = 3,000,000 × 0.0025 = $7,500
fee_apr = 7,500 / 12,000,000 × 365 = 22.81%
```

Your share with $10,000 deposited:
```
your_share = 10,000 / 12,000,000 = 0.000833
your_daily_fees = 7,500 × 0.000833 = $6.25
your_annual_fees = 6.25 × 365 = $2,281
```

### Concentrated Liquidity (CLMM) Pools

Fee income depends on your range width relative to active trading range:

```
concentration_factor = full_range_liquidity / your_range_width
effective_fee_apr = base_fee_apr × concentration_factor
```

**Worked Example:**
- Base fee APR (full range): 20%
- Your range: ±10% around current price
- Full range equivalent: ±100% (roughly)
- Concentration factor: ~5x (simplified)

```
effective_fee_apr = 20% × 5 = 100%
```

But you only earn when price is in your range. If price stays in range 60% of the time:
```
realized_fee_apr = 100% × 0.60 = 60%
```

Minus rebalancing costs each time you go out of range (gas + potential slippage).

### Volume-Weighted Fee APR

When volume varies significantly day to day, use a trailing average:

```python
trailing_7d_volume = sum(daily_volumes[-7:]) / 7
fee_apr = fee_rate * trailing_7d_volume / current_tvl * 365
```

Using 7-day trailing average smooths out spikes from single large trades.

## APR vs APY Conversion

### Definitions

- **APR** (Annual Percentage Rate): Simple interest, no compounding
- **APY** (Annual Percentage Yield): Includes compounding effect

### Formulas

```
APY = (1 + APR / n)^n - 1
APR = n × ((1 + APY)^(1/n) - 1)
```

Where `n` = number of compounding periods per year.

| Compounding | n | 20% APR → APY |
|------------|---|---------------|
| Annual | 1 | 20.00% |
| Monthly | 12 | 21.94% |
| Weekly | 52 | 22.09% |
| Daily | 365 | 22.13% |
| Continuous | ∞ | 22.14% |

### Continuous Compounding

```
APY = e^APR - 1
APR = ln(1 + APY)
```

### When to Use Which

- **Manual LP** (you claim and reinvest): Use APR — you compound when you choose
- **Auto-compounding vault** (Kamino, Tulip): Use APY — vault compounds for you
- **Lending protocols**: Usually display APY with continuous compounding
- **Staking**: Usually display APR

### Daily Rate

```
daily_rate = APR / 365                     # Simple
daily_rate = (1 + APY)^(1/365) - 1        # Compound-adjusted
```

## Net Yield Calculation

### Full Formula

```
net_daily = fee_income + emission_income - il_cost - gas_cost - rebalance_cost
net_apr = (net_daily × 365) / position_value
```

### Step-by-Step Example

**Pool:** SOL-USDC, $50,000 position

| Component | Daily | Annual | Source |
|-----------|-------|--------|--------|
| Fee income | $20.55 | $7,500 | 15% APR |
| Emission income | $13.70 | $5,000 | 10% APR (RAY) |
| Emission adj. (-30%) | $9.59 | $3,500 | RAY declining |
| IL cost | -$8.22 | -$3,000 | ~6% annual IL |
| Gas costs | -$0.14 | -$50 | Solana tx fees |
| Rebalancing | -$0.27 | -$100 | CLMM adjustments |

```
net_daily = 20.55 + 9.59 - 8.22 - 0.14 - 0.27 = $21.51
net_apr = 21.51 × 365 / 50,000 = 15.70%
```

Compare to nominal displayed APY of 25% — real yield is 15.70%.

## Emission Token Yield

### Basic Calculation

```
daily_emission_usd = daily_tokens_emitted × token_price
emission_apr = (daily_emission_usd × 365) / tvl
```

### Adjusted for Depreciation

Emission tokens face constant sell pressure from farmers. Adjust expected yield:

```
retention_factor = current_price / price_30d_ago
effective_emission_apr = emission_apr × retention_factor
```

**Example:**
- RAY emissions: 1,000 RAY/day to pool
- RAY price today: $2.00 (was $3.00 thirty days ago)
- Pool TVL: $5,000,000

```
daily_emission_usd = 1,000 × 2.00 = $2,000
emission_apr = 2,000 × 365 / 5,000,000 = 14.6%
retention_factor = 2.00 / 3.00 = 0.667
effective_emission_apr = 14.6% × 0.667 = 9.74%
```

### Forward-Looking Emission Adjustment

For more conservative estimates, project further depreciation:

```python
# If token dropped 33% last 30d, project another 33% next 30d
pessimistic_price = current_price * retention_factor
pessimistic_emission_apr = emission_apr * (retention_factor ** 2)
```

## Break-Even Analysis

### Time to Break Even

Given upfront costs (gas to enter, potential IL on entry):

```
entry_cost = deposit_gas + initial_slippage
daily_net_income = daily_fees + daily_emissions_adj - daily_il
break_even_days = entry_cost / daily_net_income
```

### Minimum Fee APR for IL Break-Even

Given expected IL (from the `impermanent-loss` skill):

```
min_fee_apr = expected_il_annual + gas_cost_annual + opportunity_cost
```

**Example:** If expected annual IL is 8%, gas costs 0.5%, and SOL staking yields 7%:
```
min_fee_apr = 8% + 0.5% + 7% = 15.5%
```

The pool must generate at least 15.5% fee APR to justify LP over staking.

### Hold Duration Impact

IL accumulates over time if price keeps trending. Shorter hold periods can be better for volatile pairs:

```python
def optimal_hold_days(fee_apr: float, volatility: float) -> int:
    """Estimate optimal holding period before IL exceeds fees.

    Args:
        fee_apr: Annual fee rate as decimal (e.g. 0.20 for 20%).
        volatility: Annual volatility as decimal (e.g. 0.80 for 80%).

    Returns:
        Approximate optimal hold period in days.
    """
    daily_fee = fee_apr / 365
    # IL grows roughly with sqrt(time) × volatility^2
    # Break-even when cumulative_fees = cumulative_il
    # Simplified: days ≈ (2 × daily_fee / (vol^2 / 365))
    daily_vol_sq = (volatility ** 2) / 365
    if daily_vol_sq == 0:
        return 365
    return int(2 * daily_fee / daily_vol_sq)
```

## Common Pitfalls

1. **Comparing APR to APY**: Always convert to the same basis before comparing
2. **Ignoring IL on volatile pairs**: Fee APR looks great until you account for IL
3. **Assuming emission APR is stable**: Token price changes daily; recalculate regularly
4. **Using spot volume for fee APR**: Use 7-day trailing average, not single-day volume
5. **Forgetting gas on Solana**: Low but not zero — matters for small positions and frequent compounds
6. **Double-counting auto-compound yield**: If vault auto-compounds, don't manually compound APR → APY
