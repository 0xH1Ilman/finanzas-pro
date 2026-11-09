# 04-macro-mercado-breadth — parte 1

Skills de terceros agrupadas por tema. Cada sección indica fuente, licencia y dónde está su código.



---

## SKILL: breadth-chart-analyst

- Fuente: `tradermonty/claude-trading-skills` → `examples/weekly-trade-strategy/.claude/skills/breadth-chart-analyst` (MIT)
- Cuándo usarla: This skill should be used when analyzing market breadth charts, specifically the S&P 500 Breadth Index (200-Day MA based) and the US Stock Market Uptrend Stock Ratio charts. Use this skill when the user provides breadth chart images for analysis, requests market breadth assessment, positioning strategy recommendations, or wants to understand medium-term strategic and short-term tactical market outlook based on breadth indicators. All analysis and output are conducted in English.

# Breadth Chart Analyst

## Overview

This skill enables specialized analysis of two complementary market breadth charts that provide strategic (medium to long-term) and tactical (short-term) market perspectives. Analyze breadth chart images to assess market health, identify trading signals based on backtested strategies, and develop positioning recommendations. All thinking and output are conducted exclusively in English.

## Core Principles

1. **Dual-Timeframe Analysis**: Combine strategic (Chart 1: 200MA Breadth) and tactical (Chart 2: Uptrend Ratio) perspectives
2. **Backtested Strategy Focus**: Apply proven systematic strategies based on historical patterns
3. **Objective Signal Identification**: Focus on clearly defined thresholds, transitions, and markers
4. **English Communication**: Conduct all analysis and generate all reports in English
5. **Actionable Recommendations**: Provide specific positioning guidance for different investor types

## Chart Types and Purposes

### Chart 1: S&P 500 Breadth Index (200-Day MA Based)

**Purpose**: Medium to long-term strategic market positioning

**Key Elements**:
- **8-Day MA (Orange Line)**: Short-term breadth trend, primary entry signal generator
- **200-Day MA (Green Line)**: Long-term breadth trend, primary exit signal generator
- **Red Dashed Line (73%)**: Average peak level - market overheating threshold
- **Blue Dashed Line (23%)**: Average 8MA trough level - extreme oversold, excellent buying opportunity
- **Triangles**:
  - Purple ▼ = 8MA troughs (buy signal when reverses)
  - Blue ▼ = 200MA troughs (major cycle lows)
  - Red ▲ = 200MA peaks (sell signal)
- **Pink Background**: Downtrend periods

**Backtested Strategy**:
- **BUY**: When 8MA reverses from a trough (especially below 23%)
- **SELL**: When 200MA forms a peak (typically near/above 73%)
- **Result**: Historically high performance, avoids bear markets

### Chart 2: US Stock Market - Uptrend Stock Ratio

**Purpose**: Short-term tactical timing and swing trading

**Key Elements**:
- **Uptrend Stock Definition**: Stocks above 200MA/50MA/20MA with positive 1-month performance
- **Green Regions**: Market in uptrend phase
- **Red Regions**: Market in downtrend phase
- **~10% Level (Lower Orange Dashed)**: Short-term bottom, extreme oversold
- **~40% Level (Upper Orange Dashed)**: Short-term top, market overheating

**Swing Trading Strategy**:
- **ENTER LONG**: When color changes from red to green (especially from <10-15% levels)
- **EXIT LONG**: When color changes from green to red (especially from >35-40% levels)
- **Timeframe**: Days to weeks

## Analysis Workflow

### Step 1: Receive Chart Images and Prepare Analysis

When the user provides breadth chart images for analysis:

1. Confirm receipt of chart image(s)
2. Identify which chart(s) are provided:
   - Chart 1 only (200MA Breadth)
   - Chart 2 only (Uptrend Ratio)
   - Both charts
3. Note any specific focus areas or questions from the user
4. Proceed with systematic analysis

**Language Note**: All subsequent thinking, analysis, and output will be in English.

### Step 2: Load Breadth Chart Methodology

Before beginning analysis, read the comprehensive breadth chart methodology:

```
Read: references/breadth_chart_methodology.md
```

This reference contains detailed guidance on:
- Chart 1: 200MA-based breadth index interpretation and strategy
- Chart 2: Uptrend stock ratio interpretation and strategy
- Signal identification and threshold significance
- Strategy rules and risk management
- Combining both charts for optimal decision-making
- Common pitfalls to avoid

### Step 3: Examine Sample Charts (First Time or for Reference)

To understand the chart format and visual elements, review the sample charts included in this skill:

```
View: assets/SP500_Breadth_Index_200MA_8MA.jpeg
View: assets/US_Stock_Market_Uptrend_Ratio.jpeg
```

These samples demonstrate:
- Visual appearance and structure of each chart type
- How signals and thresholds are displayed
- Color coding and marker systems
- Historical patterns and cycles

### Step 4: Analyze Chart 1 (200MA-Based Breadth Index)

If Chart 1 is provided, conduct systematic analysis:

#### 4.1 Extract Current Readings

From the chart image, identify:
- **Current 8MA level** (orange line): Specific percentage
- **Current 200MA level** (green line): Specific percentage
- **8MA slope**: Rising, falling, or flat
- **200MA slope**: Rising, falling, or flat
- **Distance from 73% threshold**: How close to overheating
- **Distance from 23% threshold**: How close to extreme oversold
- **Most recent date** visible on the chart

#### 4.1.5 CRITICAL: Latest Data Point Detailed Trend Analysis

**This step is MANDATORY to avoid misreading recent trend changes.**

**CRITICAL WARNING**: Charts can be deceptive. The MAJORITY of analysis errors occur because the analyst:
1. Confuses the 8MA (orange) with the 200MA (green)
2. Reads historical trends instead of the CURRENT rightmost data points
3. Misidentifies which line is rising vs falling

**BEFORE analyzing trend direction, FIRST confirm line colors**:
- ✓ **8MA = ORANGE line** (fast-moving, more volatile)
- ✓ **200MA = GREEN line** (slow-moving, smoother)
- If unsure which is which, STOP and re-examine the chart legend/colors

Focus intensively on the **rightmost 3-5 data points** of the chart (most recent weeks):

**For 8MA (Orange Line) - Analyze the very latest trajectory**:
1. **Identify the absolute latest position**: Where is the 8MA at the rightmost edge of the chart?
2. **Trace back 3-5 data points** (approximately 3-5 weeks):
   - What was the 8MA level 1 week ago?
   - What was the 8MA level 2 weeks ago?
   - What was the 8MA level 3 weeks ago?
3. **Calculate the directional change**:
   - Is the latest value HIGHER or LOWER than 1 week ago?
   - Is the latest value HIGHER or LOWER than 2 weeks ago?
   - What is the trend: consistently rising, consistently falling, or mixed?
4. **Determine the CURRENT slope** (not historical slope):
   - **Rising**: Latest data point is higher than previous 2-3 points AND shows upward curvature
   - **Falling**: Latest data point is lower than previous 2-3 points AND shows downward curvature
   - **Flat**: Latest data point is approximately equal to previous points (within 2-3%)

**Critical Questions to Answer**:
- [ ] Is the 8MA currently moving UP or DOWN at the rightmost edge?
- [ ] If there was a recent trough, has the 8MA **sustained** the upward move, or has it rolled over?
- [ ] Count consecutive periods of increase: How many consecutive periods has 8MA risen? (Need 2-3 for confirmation)
- [ ] Count consecutive periods of decrease: How many consecutive periods has 8MA fallen? (Indicates failed reversal if declining after trough)

**For 200MA (Green Line) - Analyze the very latest trajectory**:
1. **Identify the absolute latest position**: Where is the 200MA at the rightmost edge?
2. **Trace back 4-6 weeks**:
   - What was the 200MA level 2 weeks ago?
   - What was the 200MA level 4 weeks ago?
3. **Determine the CURRENT slope**:
   - Is it rising, falling, or flat in the most recent period?

**Failed Reversal Detection** (CRITICAL):
If an 8MA trough (purple ▼) was recently identified:
- [ ] Did the 8MA rise for only 1-2 periods and then turn back down?
- [ ] Did the 8MA fail to reach 60% before turning down?
- [ ] Is the 8MA currently declining again after the bounce?
- **If YES to any**: This is a **FAILED REVERSAL** - DO NOT ENTER, signal is INVALID

**Example Analysis Format**:
```
Latest 8MA Data Points (rightmost to left):
- Current (Week 0): 48%
- 1 week ago: 52%
- 2 weeks ago: 55%
- 3 weeks ago: 50%

Analysis: 8MA is FALLING. It rose from 50% to 55% (weeks 3-2), but has since declined to 48%.
This shows a failed reversal pattern - bounce was temporary, downtrend has resumed.
SLOPE: Falling (not rising!)
```

**MANDATORY CROSS-CHECK** (to catch misreadings):
After determining the trend, ask yourself:
- [ ] "If I claimed 8MA is RISING, but it's actually been FALLING for weeks, what would that look like?"
  - Answer: The rightmost data points would be LOWER than previous points (confirming FALLING)
- [ ] "Does my analysis match the visual slope of the orange line at the rightmost edge?"
  - If orange line visually slopes DOWN at the right edge → It's FALLING
  - If orange line visually slopes UP at the right edge → It's RISING
- [ ] "Is there any pink background shading (downtrend) near the rightmost edge?"
  - If YES → This confirms downtrend conditions, 8MA is likely FALLING
- [ ] "Are the 8MA and 200MA converging (getting closer) or diverging?"
  - Converging from below → Potential death cross forming → BEARISH
  - Converging from above → Potential golden cross forming → BULLISH

#### 4.2 Identify Signal Markers

Look for and document:
- **Most recent 8MA trough (purple ▼)**: Date and level
- **Most recent 200MA trough (blue ▼)**: Date and level (if visible in timeframe)
- **Most recent 200MA peak (red ▲)**: Date and level
- **Days/weeks since most recent signals**
- **Any pink background shading** (downtrend periods)

#### 4.3 Assess Market Regime

Based on readings and patterns, classify the current market as:
- Healthy Bull Market
- Overheated Bull Market
- Market Top/Distribution Phase
- Bear Market/Correction
- Capitulation/Extreme Oversold
- Early Recovery

Support the classification with specific evidence from the chart.

#### 4.4 Determine Strategy Position

Apply the backtested strategy rules with STRICT confirmation requirements:

**Check for BUY signal** (ALL criteria must be met):
1. ✓ **Trough Formation**: Has 8MA formed a clear trough (purple ▼)?
2. ✓ **Reversal Initiated**: Has 8MA begun to move upward from the trough?
3. ✓ **Confirmation Achieved**: Has 8MA risen for 2-3 CONSECUTIVE periods after the trough?
4. ✓ **No Recent Reversal**: Based on Step 4.1.5 analysis, is 8MA CURRENTLY rising (not falling)?
5. ✓ **Sustained Move**: Has 8MA maintained the upward trajectory without rolling over?
6. ⭐ **Optional but Strong**: Is 8MA below or near 23% (extreme oversold) at trough?

**BUY Signal Status**:
- **CONFIRMED**: All 5 required criteria met → ENTER LONG
- **DEVELOPING**: Trough formed, but < 2-3 consecutive increases → WAIT, MONITOR
- **FAILED**: Trough formed, but 8MA has rolled over and is declining → DO NOT ENTER, WAIT FOR NEXT TROUGH
- **NO SIGNAL**: No trough formed → WAIT

**Check for SELL signal**:
- Has 200MA formed a peak (red ▲)?
- Is 200MA near or above 73%?
- Is this an active sell signal requiring position exit?

**Current position determination**:
- **Long**: BUY signal confirmed, position entered and held
- **Preparing to Enter**: BUY signal developing (trough formed, watching for confirmation)
- **WAIT / Flat**: No valid signal OR failed reversal detected
- **Preparing to Exit**: SELL signal developing (200MA approaching peak)

#### 4.5 Develop Scenarios

Create 2-3 scenarios with probability estimates:
- Base case scenario (highest probability)
- Alternative scenario(s)
- Each scenario includes: description, supporting factors, strategy implications, key levels

### Step 5: Analyze Chart 2 (Uptrend Stock Ratio)

If Chart 2 is provided, conduct systematic analysis:

#### 5.1 Extract Current Readings

From the chart image, identify:
- **Current uptrend stock ratio**: Specific percentage
- **Current color**: Green (uptrend) or Red (downtrend)
- **Ratio slope**: Rising, falling, or flat
- **Distance from 10% threshold**: How close to extreme oversold
- **Distance from 40% threshold**: How close to overbought
- **Most recent date** visible on the chart

#### 5.2 Identify Trend Transitions

Look for and document:
- **Most recent red-to-green transition**: Date and ratio level at transition
- **Most recent green-to-red transition**: Date and ratio level at transition
- **Duration of current color phase**: How long in current trend
- **Days/weeks since most recent transition**

#### 5.3 Assess Market Condition

Based on current ratio and color, classify as:
- Extreme Oversold (<10%)
- Moderate Bearish (10-20%, red)
- Neutral/Transitional (20-30%)
- Moderate Bullish (30-37%, green)
- Extreme Overbought (>37-40%)

Support the classification with specific evidence from the chart.

#### 5.4 Determine Trading Position

Apply the swing trading strategy rules:

**Check for ENTER LONG signal**:
- Has color changed from red to green?
- Was the transition from an oversold level (<15%)?
- Is the transition confirmed (2-3 days of green)?

**Check for EXIT LONG signal**:
- Has color changed from green to red?
- Was the transition from an overbought level (>35%)?
- Is momentum weakening?

**Current position**: Long, Flat, Preparing to Enter, or Preparing to Exit

#### 5.5 Develop Scenarios

Create 2-3 scenarios with probability estimates:
- Base case scenario (highest probability)
- Alternative scenario(s)
- Each scenario includes: description, supporting factors, trading implications, key levels

### Step 6: Combined Analysis (When Both Charts Provided)

If both charts are provided, integrate the strategic and tactical perspectives:

#### 6.1 Alignment Assessment

Create a positioning matrix:
- **Chart 1 (Strategic)**: Bullish / Bearish / Neutral + signal status
- **Chart 2 (Tactical)**: Bullish / Bearish / Neutral + signal status
- **Combined Implication**: How do they align or conflict?

#### 6.2 Scenario Classification

Determine which of the four scenarios applies:

**Scenario 1: Both Bullish**
- Chart 1: 8MA rising, 200MA not yet peaked
- Chart 2: Green (uptrend), ratio rising from oversold
- Implication: Maximum bullish stance, aggressive positioning

**Scenario 2: Strategic Bullish, Tactical Bearish**
- Chart 1: 8MA rising, 200MA not yet peaked
- Chart 2: Red (downtrend), ratio falling or elevated
- Implication: Hold core long positions, wait for tactical entry

**Scenario 3: Strategic Bearish, Tactical Bullish**
- Chart 1: 200MA peaked or declining
- Chart 2: Green (uptrend), ratio rising
- Implication: Short-term tactical trades only, tight stops

**Scenario 4: Both Bearish**
- Chart 1: Both MAs declining
- Chart 2: Red (downtrend), ratio falling
- Implication: Defensive positioning, cash or shorts

#### 6.3 Unified Recommendation

Provide integrated positioning guidance for:
- **Long-term investors** (based primarily on Chart 1)
- **Swing traders** (based primarily on Chart 2)
- **Active tactical traders** (based on combination)

Address any conflicts between charts and explain resolution.

### Step 7: Generate Analysis Report in English

Create a comprehensive markdown report using the template structure:

```
Read and use as template: assets/breadth_analysis_template.md
```

**IMPORTANT**: All analysis and output must be in English.

The report structure varies based on which chart(s) are analyzed:

**If Chart 1 only**:
- Executive Summary
- Chart 1 full analysis sections
- Summary and Conclusion
- Omit Chart 2 and Combined Analysis sections

**If Chart 2 only**:
- Executive Summary
- Chart 2 full analysis sections
- Summary and Conclusion
- Omit Chart 1 and Combined Analysis sections

**If Both Charts**:
- Executive Summary
- Chart 1 full analysis sections
- Chart 2 full analysis sections
- Combined Analysis section (mandatory)
- Summary and Conclusion

**File Naming Convention**: Save each analysis as:
- Chart 1 only: `breadth_200ma_analysis_[YYYY-MM-DD].md`
- Chart 2 only: `uptrend_ratio_analysis_[YYYY-MM-DD].md`
- Both charts: `breadth_combined_analysis_[YYYY-MM-DD].md`

### Step 8: Quality Assurance

Before finalizing the report, verify:

1. ✓ **Language**: All content is in English (thinking and output)
2. ✓ **Line Color Verification**: Explicitly confirmed 8MA = ORANGE, 200MA = GREEN before trend analysis
3. ✓ **Latest Data Trend Analysis**: Step 4.1.5 was thoroughly completed - the most recent 3-5 data points were analyzed to determine CURRENT trend direction
4. ✓ **Trend Direction Accuracy**: The stated 8MA slope (Rising/Falling/Flat) accurately reflects the RIGHTMOST data points, not historical movement
5. ✓ **Cross-Check Completed**: MANDATORY CROSS-CHECK questions were answered to confirm trend direction matches visual slope
6. ✓ **Death/Golden Cross Check**: If 8MA and 200MA are converging, explicitly identified whether death cross or golden cross is forming
7. ✓ **Failed Reversal Check**: If a trough was identified, explicitly verified whether the reversal sustained or failed by analyzing latest trajectory
8. ✓ **Specific Values**: All readings include specific percentages/levels, not vague descriptions
9. ✓ **Signal Status**: Clear identification of active signals (CONFIRMED BUY / DEVELOPING / FAILED / SELL / WAIT)
10. ✓ **Strategy Alignment**: Recommendations align with backtested strategies and confirmation requirements
11. ✓ **Probabilities**: Scenario probabilities sum to 100%
12. ✓ **Actionable**: Clear positioning recommendations for different trader types
13. ✓ **Context**: Historical comparison and reference to similar past situations
14. ✓ **Risk Management**: Invalidation levels and risk factors clearly stated

**FINAL SANITY CHECK**:
- [ ] If report claims "BUY signal" or "8MA rising", confirm this doesn't contradict user's chart showing death cross or downtrend
- [ ] If report claims "bullish", confirm there's no pink background shading or death cross visible
- [ ] If unsure about ANY trend direction, explicitly state uncertainty rather than guessing

## Quality Standards

### Objectivity Requirements

- Base all analysis strictly on observable chart data
- Do not incorporate external information (news, fundamentals) unless specifically relevant
- Use precise technical terminology consistently
- Distinguish clearly between factual observations and probabilistic forecasts
- Acknowledge uncertainty when signals are ambiguous

### Completeness Requirements

- Address all relevant sections of the analysis template
- Provide specific numerical values for all key metrics
- Justify probability estimates with technical factors
- Include invalidation levels for each scenario
- Compare current readings to historical patterns visible on the charts

### Clarity Requirements

- Write in professional, analytical English
- Use clear section headings and structure
- Present information in tables where appropriate
- Make recommendations specific and actionable
- Avoid jargon without explanation

### Strategy Adherence Requirements

- Apply backtested strategy rules correctly
- Distinguish between strategic (Chart 1) and tactical (Chart 2) signals
- Provide clear position status (Long/Flat/Entering/Exiting)
- Include specific entry/exit levels when applicable
- Address risk management (stop losses, position sizing)

## Example Usage Scenarios

### Example 1: Strategic Breadth Analysis (Chart 1 Only)

```
User: "Please analyze this S&P 500 breadth chart and tell me where we are in the market cycle."
[Provides Chart 1 image: 200MA Breadth Index]

Breadth Analyst (thinking in English):
1. Confirms receipt of Chart 1 (200MA-based breadth index)
2. Reads breadth_chart_methodology.md for Chart 1 guidance
3. Views sample chart for format reference
4. Extracts current readings:
   - 8MA: 68%
   - 200MA: 75%
   - 8MA slope: Flat to slightly declining
   - 200MA slope: Rising but may be forming peak
   - Distance from 73% threshold: +2% (above threshold = overheated)
5. Identifies signals:
   - Most recent 8MA trough: 3 months ago at 25%
   - Most recent 200MA peak: None visible yet, but 200MA at 75% suggests potential peak forming
6. Assesses regime: Overheated Bull Market approaching Distribution Phase
7. Determines strategy position: Long position should prepare to exit; watch for 200MA peak confirmation
8. Develops scenarios:
   - Base Case (55%): 200MA forms peak in next 1-2 weeks, sell signal activates
   - Alternative (35%): Further consolidation at elevated levels before eventual peak
   - Bear Case (10%): Immediate rollover without clear peak formation
9. Generates comprehensive report in English: breadth_200ma_analysis_2025-11-02.md
```

### Example 2: Tactical Uptrend Ratio Analysis (Chart 2 Only)

```
User: "Should I be buying or selling here? Analyze this uptrend ratio chart."
[Provides Chart 2 image: Uptrend Stock Ratio]

Breadth Analyst (thinking in English):
1. Confirms receipt of Chart 2 (Uptrend stock ratio)
2. Reads breadth_chart_methodology.md for Chart 2 guidance
3. Views sample chart for format reference
4. Extracts current readings:
   - Current ratio: 12%
   - Current color: Green (uptrend)
   - Ratio slope: Rising sharply
   - Just transitioned from red to green 3 days ago at 11%
5. Identifies transitions:
   - Most recent red-to-green: 3 days ago at 11% (from extreme oversold)
   - Prior green-to-red: 2 weeks ago at 28%
6. Assesses condition: Early in new uptrend from extreme oversold
7. Determines trading position: ENTER LONG signal active, excellent risk/reward
8. Develops scenarios:
   - Base Case (65%): Ratio continues higher to 30-35% over next 2-3 weeks
   - Alternative (25%): Choppy advance, consolidates around 20% before next leg
   - Bear Case (10%): False breakout, returns to red quickly
9. Generates tactical report in English: uptrend_ratio_analysis_2025-11-02.md
```

### Example 3: Combined Strategic + Tactical Analysis (Both Charts)

```
User: "Analyze both of these breadth charts and give me your overall market view."
[Provides both Chart 1 and Chart 2 images]

Breadth Analyst (thinking in English):
1. Confirms receipt of both charts
2. Reads full breadth_chart_methodology.md
3. Views both sample charts
4. Analyzes Chart 1:
   - 8MA: 55%, rising from trough 2 weeks ago at 30%
   - 200MA: 60%, still rising
   - Regime: Early Recovery to Healthy Bull Market
   - Strategy: Long position, hold
5. Analyzes Chart 2:
   - Ratio: 22%, green (uptrend)
   - Transitioned red-to-green 10 days ago from 14%
   - Condition: Moderate Bullish, building momentum
   - Trading: Hold long, entered on transition
6. Combined assessment:
   - Scenario 1: Both Bullish ✓
   - Strategic: Bullish (8MA reversal confirmed)
   - Tactical: Bullish (uptrend established from oversold)
   - Alignment: Strong alignment = Maximum conviction
7. Unified recommendation:
   - Long-term investors: Aggressive long positioning, core holdings
   - Swing traders: Hold longs entered on red-to-green, target 35%+
   - Active traders: Full position, favorable environment for longs
8. Develops integrated scenarios with probabilities
9. Generates comprehensive combined report in English: breadth_combined_analysis_2025-11-02.md
```

## Common Analysis Errors and How to Avoid Them

### Error 1: Confusing 8MA with 200MA

**Symptom**: Report claims 8MA is rising when it's actually the 200MA that's rising

**Prevention**:
- ALWAYS verify: 8MA = ORANGE, 200MA = GREEN
- Check line volatility: 8MA moves faster with more volatility
- If unsure, state: "Based on line color, I identify the [orange/green] line as [8MA/200MA]"

### Error 2: Reading Historical Trends Instead of Current Direction

**Symptom**: Report describes what happened 1-2 months ago, not what's happening NOW

**Prevention**:
- Focus ONLY on rightmost 3-5 data points
- Explicitly write: "At the CURRENT rightmost edge, 8MA is at X% and is [rising/falling]"
- Ignore what happened in September if we're analyzing November

### Error 3: Missing Death Cross or Golden Cross Formation

**Symptom**: Report is bullish when 8MA and 200MA are about to death cross (bearish)

**Prevention**:
- ALWAYS check: "Are 8MA and 200MA getting closer (converging) or further apart (diverging)?"
- If converging with 8MA above 200MA → Potential death cross → BEARISH
- If converging with 8MA below 200MA → Potential golden cross → BULLISH
- Explicitly state: "8MA is currently [above/below] 200MA, and they are [converging/diverging]"

### Error 4: Ignoring Pink Background Shading

**Symptom**: Report claims bullish setup when chart shows pink downtrend background

**Prevention**:
- Check for pink shading at the rightmost edge
- Pink background = Downtrend period = Bearish conditions
- If pink shading present, report MUST acknowledge bearish conditions

### Error 5: Claiming Reversal Too Early

**Symptom**: Report says "BUY signal confirmed" after only 1 week of increase

**Prevention**:
- Require 2-3 CONSECUTIVE weeks of 8MA increase for confirmation
- If only 1 week: Signal is "DEVELOPING", not "CONFIRMED"
- If 8MA rises then falls again: Signal is "FAILED", not valid

## Resources

This skill includes the following bundled resources:

### references/breadth_chart_methodology.md

Comprehensive methodology covering:
- **Chart 1 (200MA Breadth)**: Components, interpretation, market regimes, backtested strategy, analysis checklist
- **Chart 2 (Uptrend Ratio)**: Components, interpretation, market conditions, swing trading strategy, analysis checklist
- **Combined Analysis**: Alignment scenarios, integrated decision-making
- **Common Pitfalls**: Mistakes to avoid for each chart type

**Usage**: Read this file before conducting any breadth chart analysis to ensure systematic, accurate interpretation.

### assets/breadth_analysis_template.md

Structured template for breadth analysis reports in English:
- Executive Summary
- Chart 1 analysis sections (if applicable)
- Chart 2 analysis sections (if applicable)
- Combined Analysis section (when both charts analyzed)
- Summary and Conclusion
- All sections include tables, checklists, and structured formats

**Usage**: Use this template structure for every analysis report. Adapt sections based on which chart(s) are being analyzed.

### assets/SP500_Breadth_Index_200MA_8MA.jpeg

Sample Chart 1 image showing:
- 8-day MA (orange) and 200-day MA (green) lines
- Threshold levels (73% red dashed, 23% blue dashed)
- Signal markers (triangles for troughs and peaks)
- Pink background downtrend shading
- Historical patterns from 2016-2025

**Usage**: Reference this sample to understand Chart 1 visual format and identify similar patterns in user-provided charts.

### assets/US_Stock_Market_Uptrend_Ratio.jpeg

Sample Chart 2 image showing:
- Green and red color-coded trend phases
- Uptrend ratio percentage on y-axis
- Threshold levels (~10% and ~40% orange dashed lines)
- Short-term momentum patterns
- Historical patterns from 2023-2025

**Usage**: Reference this sample to understand Chart 2 visual format and identify similar patterns in user-provided charts.

## Special Notes

### Language Requirement

**CRITICAL**: All analysis, thinking, and output MUST be in English. This includes:
- Internal analysis and reasoning
- Report generation
- Tables and data presentation
- Scenario descriptions
- Recommendations

Do not translate or use any other language. The user expects English output exclusively.

### Strategy Focus

This skill emphasizes backtested, systematic strategies rather than discretionary interpretation. Always:
- Apply the strategy rules as documented
- Reference historical performance patterns
- Provide specific entry/exit criteria
- Include risk management guidance

### Practical Application

The goal is actionable intelligence. Every analysis should answer:
- **Strategic**: Should I be long, flat, or short the market over the medium term?
- **Tactical**: Should I enter or exit positions in the short term?
- **Timing**: When should I act, and at what levels?
- **Risk**: What would invalidate this view, and where should stops be?

### Referencia: assets/breadth_analysis_template.md

# Market Breadth Analysis Report

**Analysis Date**: [YYYY-MM-DD]
**Analyst**: Claude Breadth Chart Specialist
**Charts Analyzed**: [Chart 1 only / Chart 2 only / Both Charts]

---

## Executive Summary

[Brief 2-4 sentence overview of the key findings from the breadth analysis]

**Strategic Outlook**: [Bullish / Bearish / Neutral]
**Tactical Outlook**: [Bullish / Bearish / Neutral]
**Overall Recommendation**: [Aggressive Long / Moderate Long / Neutral / Defensive / Short]

---

# Chart 1: S&P 500 Breadth Index (200-Day MA Based)

## Current Readings

**Date of Latest Data**: [Latest date visible on chart]

### Key Metrics

| Metric | Current Value | Interpretation |
|--------|---------------|----------------|
| 8-Day MA (Orange) | [X.XX / XX%] | [Above/Below/At threshold] |
| 200-Day MA (Green) | [X.XX / XX%] | [Above/Below/At threshold] |
| Distance from 73% Peak Threshold | [+/- XX%] | [Overheated / Normal / Oversold] |
| Distance from 23% Trough Threshold | [+/- XX%] | [Extreme Oversold / Normal / Elevated] |

### Trend Direction

- **8MA Slope**: [Rising / Falling / Flat] - [Brief description of trajectory]
- **200MA Slope**: [Rising / Falling / Flat] - [Brief description of trajectory]
- **Trend Alignment**: [Both Rising / Both Falling / Diverging / Mixed]

### Latest Data Point Trend Analysis (CRITICAL)

**Focus: Rightmost 3-5 Data Points**

**8MA Recent Trajectory** (Week-by-Week from trough/recent period to present):
- **Current Level** (Week 0): [XX%]
- **1 Week Ago** (Week -1): [XX%] - Change: [+/-XX%]
- **2 Weeks Ago** (Week -2): [XX%] - Change: [+/-XX%]
- **3 Weeks Ago** (Week -3): [XX%] - Change: [+/-XX%]

**Consecutive Period Analysis**:
- Consecutive Increases: [X periods]
- Consecutive Decreases: [X periods]
- Current Momentum: [Accelerating Up / Steady Up / Decelerating / Turning Down / Falling]

**CURRENT Slope Determination** (based on latest edge):
- [ ] Rising: Latest value higher than previous 2-3 points with upward curvature
- [ ] Falling: Latest value lower than previous 2-3 points with downward curvature
- [ ] Flat: Latest value approximately equal to previous points (±2-3%)

**Failed Reversal Check** (if trough recently formed):
- [ ] Has 8MA rolled over after initial bounce?
- [ ] Has 8MA declined for 1-2+ consecutive periods after rising?
- [ ] Has 8MA failed to reach 55-60% before turning down?

**Conclusion**: The 8MA is [CURRENTLY RISING / CURRENTLY FALLING / FLAT] based on the rightmost data points.

## Signal Status

### Recent Signal Markers

**8MA Troughs (Purple ▼)**:
- Most Recent: [Date] at [XX%]
- Status: [X days/weeks since trough]
- Reversal Confirmed: [Yes / No / Developing]

**200MA Troughs (Blue ▼)**:
- Most Recent: [Date] at [XX%]
- Significance: [Major cycle low / Historical context]

**200MA Peaks (Red ▲)**:
- Most Recent: [Date] at [XX%]
- Status: [X days/weeks since peak]
- Implications: [Exit signal active / Historical peak]

### Active Signals

**Current Strategy Signal**: [CONFIRMED BUY / DEVELOPING BUY / FAILED REVERSAL / SELL / HOLD / WAIT]

**Signal Classification**:
- **CONFIRMED BUY**: Trough formed + 2-3 consecutive increases + CURRENTLY rising → ENTER LONG
- **DEVELOPING BUY**: Trough formed + < 2 consecutive increases → WAIT, MONITOR
- **FAILED REVERSAL**: Trough formed + initially rose + now declining → DO NOT ENTER
- **SELL**: 200MA peak formed → EXIT LONG
- **HOLD**: Already long, no exit signal → MAINTAIN POSITION
- **WAIT**: No trough, or waiting for new trough after failed reversal → STAY FLAT

[Detailed explanation of why this signal status is assigned, including specific reference to Latest Data Point Trend Analysis findings]

## Market Regime Assessment

**Current Regime**: [Healthy Bull Market / Overheated Bull Market / Market Top/Distribution / Bear Market/Correction / Capitulation/Extreme Oversold / Early Recovery]

### Regime Characteristics

[Detailed description of the current market regime, including:]
- Key observations supporting this classification
- How current readings align with historical patterns
- Typical duration and behavior in this regime

### Supporting Evidence

1. [First piece of evidence]
2. [Second piece of evidence]
3. [Third piece of evidence]

## Historical Context

### Comparison to Previous Cycles

[Analysis comparing current readings to previous similar situations shown on the chart]

**Similar Historical Periods**:
- **[Date Range 1]**: [Brief description and outcome]
- **[Date Range 2]**: [Brief description and outcome]
- **[Date Range 3]**: [Brief description and outcome]

### Distance from Extremes

- **Time Since Last 8MA Trough**: [X weeks/months]
- **Time Since Last 200MA Peak**: [X weeks/months]
- **Current Reading vs Historical Average**: [Above/Below by XX%]

## Strategy Implications

### Backtested Strategy Positioning

**Current Position**: [Long / Flat / Preparing to Enter / Preparing to Exit]

#### Entry Analysis

**Entry Signal Status**: [Active / Not Active / Pending]

[If active or pending:]
- **Entry Trigger**: [Description of what triggered or would trigger entry]
- **Confirmation Criteria**: [What needs to happen for confirmation]
- **Optimal Entry Zone**: [Price/breadth level range]
- **Entry Timing**: [Immediate / Wait for X / Already entered]

[If not active:]
- **What Would Trigger Entry**: [Specific conditions needed]
- **Estimated Distance to Entry**: [How far from entry conditions]

#### Exit Analysis

**Exit Signal Status**: [Active / Not Active / Monitoring]

[If active or monitoring:]
- **Exit Trigger**: [Description of what triggered or would trigger exit]
- **Key Level to Watch**: [Specific breadth level or 200MA behavior]
- **Exit Timing**: [Immediate / Prepare to exit / Not yet]

[If not active:]
- **What Would Trigger Exit**: [Specific conditions needed]
- **Estimated Distance to Exit**: [How far from exit conditions]

### Risk Management

**Current Risk Level**: [Low / Moderate / High / Extreme]

**Risk Factors**:
- [Risk factor 1]
- [Risk factor 2]
- [Risk factor 3]

**Invalidation Levels**:
- **Bullish Case Invalidation**: [Specific level or condition]
- **Bearish Case Invalidation**: [Specific level or condition]

## Key Levels to Monitor

### Critical Thresholds

1. **[Level 1]**: [Description and significance]
2. **[Level 2]**: [Description and significance]
3. **[Level 3]**: [Description and significance]

### Upcoming Milestones

- **Near-term** (Next 1-2 weeks): [What to watch for]
- **Medium-term** (Next 1-2 months): [What to watch for]
- **Long-term** (Next 3-6 months): [What to watch for]

## Scenario Analysis

### Base Case Scenario: [Title] - **[XX]% Probability**

**Description**: [What this scenario entails]

**Supporting Factors**:
- [Factor 1]
- [Factor 2]
- [Factor 3]

**Implications**:
- Strategy Position: [Long/Flat/Short]
- Expected Duration: [Timeframe]
- Key Levels: [Targets or invalidation levels]

---

### Alternative Scenario: [Title] - **[XX]% Probability**

**Description**: [What this scenario entails]

**Supporting Factors**:
- [Factor 1]
- [Factor 2]

**Implications**:
- Strategy Position: [Long/Flat/Short]
- Expected Duration: [Timeframe]
- Key Levels: [Targets or invalidation levels]

---

# Chart 2: US Stock Market - Uptrend Stock Ratio

## Current Readings

**Date of Latest Data**: [Latest date visible on chart]

### Key Metrics

| Metric | Current Value | Interpretation |
|--------|---------------|----------------|
| Uptrend Stock Ratio | [XX.X%] | [Oversold / Normal / Overbought] |
| Current Trend Color | [Green / Red] | [Uptrend / Downtrend] |
| Distance from 10% Bottom | [+/- XX%] | [Extreme Oversold / Normal / Elevated] |
| Distance from 40% Top | [+/- XX%] | [Overbought / Normal / Oversold] |

### Trend Direction

- **Ratio Slope**: [Rising / Falling / Flat] - [Brief description of trajectory]
- **Trend Duration**: [X days/weeks] in current [Green/Red] phase
- **Momentum**: [Accelerating / Decelerating / Steady]

## Signal Status

### Recent Trend Transitions

**Most Recent Red-to-Green Transition** (Downtrend to Uptrend):
- Date: [Date]
- Ratio at Transition: [XX%]
- Days Since Transition: [X days]
- Performance Since: [Result if applicable]

**Most Recent Green-to-Red Transition** (Uptrend to Downtrend):
- Date: [Date]
- Ratio at Transition: [XX%]
- Days Since Transition: [X days]
- Performance Since: [Result if applicable]

### Active Signals

**Current Trading Signal**: [ENTER LONG / EXIT LONG / HOLD LONG / STAY FLAT / PREPARE TO ENTER]

[Detailed explanation of why this signal is active]

## Market Condition Assessment

**Current Condition**: [Extreme Oversold / Moderate Bearish / Neutral/Transitional / Moderate Bullish / Extreme Overbought]

### Condition Characteristics

[Detailed description of the current market condition, including:]
- Participation breadth analysis
- Short-term momentum assessment
- Risk/reward considerations at current levels

### Supporting Evidence

1. [First piece of evidence]
2. [Second piece of evidence]
3. [Third piece of evidence]

## Historical Context

### Comparison to Recent Extremes

**Recent Oversold Extremes** (<15%):
- [Date]: [Ratio %] - [Outcome]
- [Date]: [Ratio %] - [Outcome]

**Recent Overbought Extremes** (>35%):
- [Date]: [Ratio %] - [Outcome]
- [Date]: [Ratio %] - [Outcome]

### Typical Behavior at Current Level

[Analysis of how the market typically behaves when the ratio is at the current level]

## Trading Strategy Implications

### Swing Trading Strategy Positioning

**Current Position**: [Long / Flat / Preparing to Enter / Preparing to Exit]

#### Entry Analysis

**Entry Signal Status**: [Active / Not Active / Pending Confirmation]

[If active or pending:]
- **Entry Trigger**: [Red-to-green transition / Oversold reversal / etc.]
- **Confirmation Status**: [Confirmed / Needs X more days / Partial confirmation]
- **Optimal Entry Level**: [Current / Wait for ratio to reach X%]
- **Entry Timing**: [Immediate / Next X days / Already entered]
- **Risk/Reward**: [Assessment of risk/reward at current or pending entry]

[If not active:]
- **What Would Trigger Entry**: [Specific color change or level needed]
- **Current Phase**: [Waiting for oversold / Mid-trend / Overbought]

#### Exit Analysis

**Exit Signal Status**: [Active / Not Active / Monitoring / Tighten Stops]

[If active or monitoring:]
- **Exit Trigger**: [Green-to-red transition / Overbought level / etc.]
- **Exit Timing**: [Immediate / When ratio reaches X% / When color changes]
- **Profit Status**: [Up X% from entry / Down / Flat]

[If not active:]
- **What Would Trigger Exit**: [Specific color change or level needed]
- **Current Phase**: [Early in trend / Mid-trend / Late in trend]

### Position Sizing Recommendations

**Suggested Position Size**: [Full / 75% / 50% / 25% / Minimal / Zero]

**Rationale**: [Explanation based on current ratio level, trend status, and risk/reward]

### Risk Management

**Current Risk Level**: [Low / Moderate / High / Extreme]

**Risk Factors**:
- [Risk factor 1]
- [Risk factor 2]
- [Risk factor 3]

**Stop Loss Level**: [Specific ratio level or condition]

**Profit Target**: [Specific ratio level or condition]

## Key Levels to Monitor

### Critical Thresholds

1. **10% Level (Oversold Bottom)**: [Distance from current, significance]
2. **40% Level (Overbought Top)**: [Distance from current, significance]
3. **[Other Key Level]**: [Description and significance]

### Timing Considerations

- **Short-term** (Next few days): [What to watch for]
- **Swing Trade Horizon** (Next 1-3 weeks): [Expected development]

## Scenario Analysis

### Scenario 1: [Title] - **[XX]% Probability**

**Description**: [What this scenario entails]

**Supporting Factors**:
- [Factor 1]
- [Factor 2]

**Implications**:
- Trading Action: [Enter/Hold/Exit]
- Expected Ratio Movement: [Direction and potential range]
- Timeframe: [Days to weeks]

---

### Scenario 2: [Title] - **[XX]% Probability**

**Description**: [What this scenario entails]

**Supporting Factors**:
- [Factor 1]
- [Factor 2]

**Implications**:
- Trading Action: [Enter/Hold/Exit]
- Expected Ratio Movement: [Direction and potential range]
- Timeframe: [Days to weeks]

---

# Combined Analysis: Strategic & Tactical Integration

[This section is included when both charts are analyzed together]

## Alignment Assessment

### Current Positioning Matrix

| Timeframe | Chart | Status | Signal | Implication |
|-----------|-------|--------|--------|-------------|
| Strategic (Medium/Long) | 200MA Breadth | [Bullish/Bearish/Neutral] | [Buy/Sell/Hold/Wait] | [Brief implication] |
| Tactical (Short-term) | Uptrend Ratio | [Bullish/Bearish/Neutral] | [Enter/Exit/Hold/Wait] | [Brief implication] |

### Scenario Classification

**Current Scenario**: [Scenario 1 / Scenario 2 / Scenario 3 / Scenario 4]

**Scenario 1: Both Bullish**
- Chart 1: [Status]
- Chart 2: [Status]
- Combined Implication: [Maximum bullish / Strategic opportunity]

**Scenario 2: Strategic Bullish, Tactical Bearish**
- Chart 1: [Status]
- Chart 2: [Status]
- Combined Implication: [Hold core, wait for tactical entry]

**Scenario 3: Strategic Bearish, Tactical Bullish**
- Chart 1: [Status]
- Chart 2: [Status]
- Combined Implication: [Short-term trade only, tight stops]

**Scenario 4: Both Bearish**
- Chart 1: [Status]
- Chart 2: [Status]
- Combined Implication: [Defensive positioning]

## Unified Recommendation

### Overall Market Assessment

**Strategic Stance** (3-12+ months): [Bullish / Bearish / Neutral]

**Tactical Stance** (Days to weeks): [Bullish / Bearish / Neutral]

**Conviction Level**: [High / Medium / Low]

### Recommended Actions

**For Long-Term Investors**:
1. [Action 1 based on Chart 1]
2. [Action 2 based on Chart 1]
3. [Action 3 - position sizing]

**For Swing Traders**:
1. [Action 1 based on Chart 2]
2. [Action 2 based on Chart 2]
3. [Action 3 - timing and entry/exit levels]

**For Active Tactical Traders**:
1. [Action 1 combining both charts]
2. [Action 2 - nimble positioning]
3. [Action 3 - risk management]

### Optimal Strategy

**Current Market Environment Best Suited For**: [Strategic positioning / Tactical trading / Both / Neither - stay flat]

[Detailed explanation of why this is the optimal approach given the current breadth readings]

## Risk and Opportunity Matrix

### Primary Opportunities

1. **[Opportunity 1]**: [Description and how to capitalize]
2. **[Opportunity 2]**: [Description and how to capitalize]

### Primary Risks

1. **[Risk 1]**: [Description and how to mitigate]
2. **[Risk 2]**: [Description and how to mitigate]

## Conflicts and Considerations

### Chart Divergences

[If there are conflicts between Chart 1 and Chart 2 signals:]

**Divergence Identified**: [Description of the conflict]

**Resolution**: [How to interpret and act on the divergence]

**Precedence**: [Which chart takes priority in this situation and why]

---

# Summary and Conclusion

## Key Takeaways

1. **[Most Important Finding]**: [Brief explanation]
2. **[Second Most Important Finding]**: [Brief explanation]
3. **[Third Most Important Finding]**: [Brief explanation]

## Action Items

**Immediate Actions** (Now):
- [ ] [Action item 1]
- [ ] [Action item 2]

**Pending Actions** (Contingent on market movement):
- [ ] If [condition], then [action]
- [ ] If [condition], then [action]

## Monitoring Plan

**Daily Monitoring Required**: [Yes / No]

**Key Updates to Watch For**:
1. [Update 1 - e.g., new 8MA trough formation]
2. [Update 2 - e.g., color transition in Chart 2]
3. [Update 3 - e.g., breach of key threshold]

**Next Analysis Recommended**: [Timeframe - daily / every 3 days / weekly]

## Confidence and Limitations

**Analysis Confidence Level**: [High / Medium / Low]

**Reasoning for Confidence Level**: [Explanation]

**Limitations and Caveats**:
- [Limitation 1 - e.g., signals work best in trending markets]
- [Limitation 2 - e.g., external shocks can override technical signals]
- [Limitation 3 - e.g., breadth lags price in fast-moving conditions]

---

## Disclaimer

This analysis is based purely on market breadth technical indicators and does not consider fundamental factors, macroeconomic data, geopolitical events, or other external factors that may influence market behavior. The strategies referenced are based on historical backtesting and may not perform identically in future market conditions. This analysis represents a probabilistic assessment of potential scenarios and is not a guarantee of future performance or a recommendation to buy or sell securities.

All probabilities are estimates based on technical factors and historical patterns, and are subject to change as new data emerges.

---

**End of Breadth Analysis Report**

---

## Appendix: Chart Images

[If chart images are to be included in the report]

### Chart 1: S&P 500 Breadth Index
[Chart image or reference]

### Chart 2: Uptrend Stock Ratio
[Chart image or reference]

### Referencia: references/breadth_chart_methodology.md

# Breadth Chart Analysis Methodology

This reference provides comprehensive methodology for analyzing two types of market breadth charts that provide complementary views of market health and trend status.

## Overview

Market breadth indicators measure the participation of stocks in market moves, providing insights into the strength and sustainability of trends that price indices alone cannot reveal. This skill focuses on two specific breadth measurements:

1. **200MA-Based Breadth Index**: Medium to long-term trend assessment tool
2. **Uptrend Stock Ratio**: Short-term trend and momentum indicator

These two charts work together to provide both strategic (medium/long-term) and tactical (short-term) market perspectives.

---

## Chart 1: S&P 500 Breadth Index (200-Day MA Based)

### Purpose and Use Case

This chart measures the percentage of S&P 500 stocks trading above their 200-day moving average, providing insight into the medium to long-term health of the market. It serves as a strategic positioning tool for determining major market cycles.

### Chart Components

#### Primary Lines

**8-Day Moving Average (8MA) - Orange Line**
- Short-term smoothing of the breadth index
- More responsive to rapid market changes
- Key for identifying reversal points
- Used as the primary signal generator for entries

**200-Day Moving Average (200MA) - Green Line**
- Long-term trend of market breadth
- Slower to respond, filters out noise
- Represents the underlying structural health of the market
- Used as the primary signal generator for exits

#### Reference Levels

**Red Dashed Line (0.73 / 73%)**
- **Average Peak Level**: Historical average of 200MA tops
- **Significance**: When the breadth index exceeds this level, the market is in an overheated state
- **Interpretation**:
  - Above 73%: Market is extremely bullish but approaching exhaustion
  - Significantly above 73%: Elevated risk of correction or consolidation
  - Rarely sustainable for extended periods

**Blue Dashed Line (0.23 / 23%)**
- **Average 8MA Trough Level**: Historical average of 8MA bottoms
- **Significance**: When the 8MA falls below this level, the market is in extreme oversold territory
- **Interpretation**:
  - Below 23%: Severe market stress, capitulation-level selling
  - High probability of reversal and recovery
  - Historically represents excellent buying opportunities
  - Extreme fear and pessimism typically present

#### Signal Markers (Triangles)

**Purple/Magenta Downward Triangles (▼)**
- **8MA Troughs**: Mark the bottoms of the 8-day moving average
- **Significance**: Potential reversal points, especially when near or below the 23% threshold
- **Use**: Primary buy signal when 8MA begins to turn up from a trough

**Blue Downward Triangles (▼)**
- **200MA Troughs**: Mark the bottoms of the 200-day moving average
- **Significance**: Major market cycle lows, extremely rare
- **Use**: Indicates the beginning of a new long-term bull market

**Red Upward Triangles (▲)**
- **200MA Peaks**: Mark the tops of the 200-day moving average
- **Significance**: Major market cycle highs indicating trend exhaustion
- **Use**: Primary sell signal for the tested strategy

#### Background Shading

**Pink Background Regions**
- **Downtrend Periods**: Time periods when the market is in a confirmed downtrend
- **Significance**: Higher risk environment, defensive positioning warranted
- **Use**: Visual aid to identify unfavorable market conditions

### Interpretation Framework

#### Market Regimes

**Healthy Bull Market**
- 8MA and 200MA both rising
- Breadth index between 40% and 73%
- Regular pullbacks to 50-60% range that hold above 8MA
- Wide participation across stocks

**Overheated Bull Market**
- Breadth index persistently above 73%
- 8MA and 200MA both very elevated
- High risk of near-term correction
- Market vulnerable to negative catalysts

**Market Top/Distribution Phase**
- 200MA forming a peak (red ▲)
- 8MA begins to roll over even if 200MA hasn't peaked yet
- Breadth index declining from elevated levels
- Signal to exit long positions

**Bear Market/Correction**
- Both 8MA and 200MA declining
- Pink background shading present
- Breadth index below 50%
- High volatility typical

**Capitulation/Extreme Oversold**
- 8MA below 23% (blue dashed line)
- 8MA forming a trough (purple ▼)
- Maximum pessimism and fear
- Historically excellent buying opportunities

**Early Recovery**
- 8MA turning up from a trough
- 200MA may still be declining (lagging)
- Breadth index beginning to rise from extreme lows
- Initial phase of new uptrend

### Backtested Strategy

Based on historical analysis, the following strategy has demonstrated strong performance:

#### Entry Rules

**BUY Signal**: 8MA Trough Reversal
- Wait for 8MA to form a clear bottom (purple ▼)
- Especially strong when 8MA trough is below 23% (extreme oversold)
- Enter long position in S&P 500 index when 8MA begins to turn upward
- Confirmation: 8MA crosses above previous recent high or shows 2-3 consecutive days of increase

#### Detailed Reversal Confirmation Criteria

**CRITICAL**: Do not enter prematurely. A trough formation alone is NOT sufficient for entry. The reversal must be CONFIRMED.

**Required Steps for Confirmation**:

1. **Trough Identification** (Step 1):
   - 8MA forms a clear bottom marked by purple ▼ triangle
   - Trough level should ideally be below 40%, preferably below 30%
   - Extreme troughs below 23% provide highest probability setups

2. **Initial Reversal** (Step 2):
   - 8MA begins to move upward from the trough
   - First 1-2 periods of increase observed
   - **WARNING**: This is NOT yet a confirmed signal - DO NOT ENTER

3. **Confirmation Period** (Step 3 - MANDATORY):
   - 8MA continues to rise for 2-3 CONSECUTIVE periods after the trough
   - Each period should show clear upward progress (at least 2-5% increase)
   - No significant pullbacks or reversals during confirmation period

4. **Latest Data Verification** (Step 4 - CRITICAL):
   - Analyze the RIGHTMOST 3-5 data points on the chart
   - Verify that the 8MA is CURRENTLY rising (at the latest edge of the chart)
   - Confirm no rollover or downward turn has occurred recently
   - This step prevents entry on failed reversals

5. **Resistance Breakout** (Step 5 - Optional but Ideal):
   - 8MA crosses above 55-60% level
   - This confirms strong breadth improvement
   - Provides higher confidence in sustainability

**Confirmation Status Classification**:

- **CONFIRMED (Green Light)**: Steps 1-4 complete, 8MA rising for 2-3+ consecutive periods and CURRENTLY rising → ENTER
- **DEVELOPING (Yellow Light)**: Steps 1-2 complete, but < 2 consecutive increases → WAIT, MONITOR CLOSELY
- **FAILED (Red Light)**: Steps 1-2 occurred, but 8MA has rolled over and is declining → DO NOT ENTER, signal invalidated
- **NO SIGNAL (Red Light)**: No trough formed → WAIT

**Time-Based Confirmation**:
- Typical confirmation period: 2-4 weeks after trough
- If confirmation takes > 6 weeks, signal strength decreases
- If 8MA fails to reach 55% within 6 weeks of trough, reassess validity

#### Failed Reversal Patterns (WARNING SIGNS)

**What is a Failed Reversal?**

A failed reversal occurs when the 8MA forms a trough and begins to rise, but then rolls over and declines again before reaching sustained momentum. This invalidates the buy signal and often leads to deeper corrections.

**Identifying Failed Reversals**:

1. **Weak Bounce Pattern**:
   - 8MA rises for only 1-2 periods after trough
   - 8MA fails to reach 50-55% level
   - 8MA then turns downward again
   - **Result**: False signal, do NOT enter

2. **Premature Rollover**:
   - 8MA rises to 50-60% range
   - 8MA fails to sustain the rise, begins declining
   - 8MA shows consistent downward trajectory at latest data points
   - **Result**: Reversal failed, exit if already entered or do not enter

3. **Double Bottom Formation**:
   - First trough forms, 8MA rises briefly
   - 8MA declines to form second, lower trough
   - **Result**: First trough was not the final bottom, wait for second trough to confirm

**Failed Reversal Action Protocol**:
- Immediately classify signal as INVALID
- Do NOT enter position
- Wait for 8MA to form a NEW, LOWER trough (often below 23%)
- Reset analysis and wait for fresh confirmation from the new trough

**Historical Failed Reversal Examples** (refer to chart):
- Failed reversals are less common but occur during severe corrections
- They typically precede deeper declines to extreme oversold (<23%)
- After failed reversal, the eventual confirmed reversal from lower levels often provides excellent entries

#### Latest Data Point Analysis Protocol

**Why Latest Data Points Matter Most**:

The most recent 3-5 data points on the chart (rightmost edge) represent the CURRENT market condition. Historical movement is context, but the latest trajectory determines whether a signal is active, developing, or failed.

**Protocol**:

1. **Always Start with the Rightmost Data Point**:
   - This is the absolute latest reading
   - This determines the CURRENT slope of the 8MA

2. **Trace Backward 3-5 Data Points**:
   - Compare current level to 1 week ago
   - Compare current level to 2 weeks ago
   - Compare current level to 3 weeks ago
   - Determine if the trend is: Rising, Falling, or Flat

3. **Calculate Consecutive Periods**:
   - Count how many consecutive periods 8MA has risen
   - Count how many consecutive periods 8MA has fallen
   - **Confirmation requires 2-3 consecutive UP periods**
   - **1-2 consecutive DOWN periods after a trough = failed reversal warning**

4. **Visual Slope Assessment**:
   - Visually trace the 8MA line at the rightmost edge
   - Is the line sloping UP, DOWN, or FLAT?
   - Do NOT rely on earlier parts of the chart - focus on the edge

**Example Analysis**:

```
Scenario: 8MA formed trough at 30% three weeks ago

Week-by-Week Analysis (from trough to present):
- Week 1 after trough: 30% → 40% (UP 10%)
- Week 2 after trough: 40% → 52% (UP 12%)
- Week 3 after trough: 52% → 48% (DOWN 4%)

Current Slope: FALLING
Consecutive Increases: 0 (last period was DOWN)
Status: FAILED REVERSAL - 8MA rolled over after initial bounce

Action: DO NOT ENTER. Signal is invalid. Wait for new trough formation.
```

```
Scenario: 8MA formed trough at 25% four weeks ago

Week-by-Week Analysis (from trough to present):
- Week 1 after trough: 25% → 35% (UP 10%)
- Week 2 after trough: 35% → 45% (UP 10%)
- Week 3 after trough: 45% → 55% (UP 10%)
- Week 4 after trough: 55% → 60% (UP 5%)

Current Slope: RISING
Consecutive Increases: 4 (all periods UP)
Status: CONFIRMED - Strong sustained reversal

Action: ENTER LONG. Signal is confirmed and robust.
```

#### Exit Rules

**SELL Signal**: 200MA Peak Detection
- Exit long position when 200MA forms a peak (red ▲)
- 200MA peaks typically occur when breadth index is near or above 73%
- Do not wait for 200MA to turn down; exit at or near the peak
- This signals the end of the bull market phase

#### Risk Management

- **Stop Loss**: Consider exiting if 8MA breaks decisively below its most recent trough
- **Partial Profits**: Consider taking partial profits when breadth index exceeds 73% (overheated)
- **Re-entry**: Do not re-enter during the same cycle unless a new 8MA trough forms

#### Strategy Performance Characteristics

- **Win Rate**: Historically high due to buying extreme oversold and selling into strength
- **Hold Period**: Typically several months to over a year
- **Drawdown Management**: Strategy avoids holding through major bear markets
- **False Signals**: Rare due to the significant smoothing of the indicators

### Analysis Checklist

When analyzing this chart, systematically evaluate:

1. ✓ **Current 8MA Level**: Where is the 8MA relative to historical troughs and the 23% threshold?
2. ✓ **Current 200MA Level**: Where is the 200MA relative to historical peaks and the 73% threshold?
3. ✓ **8MA Slope**: Is the 8MA rising, falling, or flat?
4. ✓ **200MA Slope**: Is the 200MA rising, falling, or flat?
5. ✓ **Recent Signal Markers**: Any recent triangles indicating troughs or peaks?
6. ✓ **Market Regime**: Which regime best describes the current state?
7. ✓ **Strategy Position**: Based on the backtested strategy, should one be long, flat, or preparing to enter/exit?
8. ✓ **Distance from Thresholds**: How close is the breadth index to key levels (23%, 73%)?

---

## Chart 2: US Stock Market - Uptrend Stock Ratio

### Purpose and Use Case

This chart measures the percentage of stocks in confirmed uptrends across the US stock market, providing a real-time view of market momentum and participation. It serves as a tactical tool for short-term swing trading and confirming the strength of market moves.

### Definition of "Uptrend Stock"

A stock is classified as being in an uptrend when it meets ALL of the following criteria:

1. **Price above 200-day MA**: Stock is in a long-term uptrend
2. **Price above 50-day MA**: Stock is in an intermediate-term uptrend
3. **Price above 20-day MA**: Stock is in a short-term uptrend
4. **Positive 1-month performance**: Stock has gained value over the past month

This multi-factor definition ensures that only stocks with confirmed momentum across multiple timeframes are counted as "uptrend stocks."

### Chart Components

#### Primary Visualization

**Color-Coded Trend Identification**

**Green Regions**
- Represent periods when the market is in an **uptrend**
- Uptrend stock ratio is generally rising
- Positive market momentum
- Favorable environment for long positions

**Red Regions**
- Represent periods when the market is in a **downtrend**
- Uptrend stock ratio is generally falling
- Negative market momentum
- Unfavorable for long positions, defensive posture appropriate

**Color Transitions**
- **Red-to-Green Transition**: Downtrend ending, uptrend beginning (BUY signal)
- **Green-to-Red Transition**: Uptrend ending, downtrend beginning (SELL signal)

#### Reference Levels

**Lower Orange Dashed Line (~10%)**
- **Short-Term Market Bottom**: When the uptrend ratio falls to approximately 10%
- **Significance**: Extreme oversold condition
- **Interpretation**:
  - Below 10%: Maximum bearish sentiment, capitulation phase
  - High probability of near-term reversal
  - Short-term bottom often forms at this level
  - Excellent risk/reward for initiating long positions

**Upper Orange Dashed Line (~37-40%)**
- **Short-Term Market Top**: When the uptrend ratio approaches approximately 40%
- **Significance**: Overbought condition, market overheating
- **Interpretation**:
  - Near 40%: Market is short-term overbought
  - High probability of pullback or consolidation
  - Reversal often begins at this level
  - Consider taking profits or tightening stops on long positions

### Interpretation Framework

#### Market Conditions

**Extreme Oversold (Ratio < 10%)**
- Very few stocks participating in uptrend
- Market-wide selling pressure
- High fear and pessimism
- Contrarian buying opportunity
- Often coincides with VIX spikes
- Watch for red-to-green transition

**Moderate Bearish (Ratio 10-20%)**
- Below-average market participation
- Downtrend still in effect (red)
- Selective stock strength only
- Wait for confirmation before entering

**Neutral/Transitional (Ratio 20-30%)**
- Average market participation
- Can be either early uptrend or late downtrend
- Color (green vs red) is critical for context
- Watch for trend changes

**Moderate Bullish (Ratio 30-37%)**
- Healthy uptrend participation
- Green color dominant
- Sustainable momentum
- Favorable for long positions

**Extreme Overbought (Ratio > 37-40%)**
- Very high participation in uptrend
- Market short-term overheated
- Vulnerable to pullback
- Watch for green-to-red transition
- Consider profit-taking

#### Trend Transitions

**Red-to-Green (Downtrend to Uptrend)**
- **Entry Signal**: Marks the beginning of a new uptrend phase
- **Characteristics**:
  - Uptrend ratio bottoms and begins to rise
  - Often occurs from extreme oversold levels (<10-15%)
  - Increasing number of stocks breaking above MAs
  - Momentum shifting from bearish to bullish
- **Action**: Initiate long positions in index or strong individual stocks

**Green-to-Red (Uptrend to Downtrend)**
- **Exit Signal**: Marks the end of an uptrend phase
- **Characteristics**:
  - Uptrend ratio peaks and begins to fall
  - Often occurs from overbought levels (>35-40%)
  - Stocks breaking below key moving averages
  - Momentum shifting from bullish to bearish
- **Action**: Exit long positions, move to cash or defensive positions

### Trading Strategy

#### Short-Term Swing Trading Strategy

**Entry Rules**

1. **Wait for Oversold Condition**:
   - Uptrend ratio declines to 10-15% range
   - Market in red (downtrend) phase

2. **Identify Trend Reversal**:
   - Color changes from red to green
   - Uptrend ratio begins to rise from lows
   - Confirmation: 2-3 consecutive increases in the ratio

3. **Enter Long Position**:
   - Buy S&P 500 index (SPY, ES futures) or basket of leading stocks
   - Position size based on risk tolerance

**Exit Rules**

1. **Watch for Overbought Condition**:
   - Uptrend ratio approaches 37-40% level
   - Market has been green for extended period

2. **Identify Trend Exhaustion**:
   - Color changes from green to red
   - Uptrend ratio begins to fall from highs
   - Momentum waning

3. **Exit Long Position**:
   - Sell index position
   - Move to cash or defensive assets

**Risk Management**

- **Stop Loss**: Exit if uptrend ratio breaks below recent lows while still in supposed uptrend
- **Partial Exits**: Consider scaling out as ratio approaches 35-37%
- **Position Sizing**: Larger positions when entering from extreme oversold (<10%), smaller when entering from moderate levels
- **False Signals**: Quick reversals (red-green-red or green-red-green within days) may be false; wait for confirmation

#### Strategy Performance Characteristics

- **Timeframe**: Days to weeks (swing trading)
- **Win Rate**: Moderate to high, depending on confirmation criteria
- **Hold Period**: Typically 1-4 weeks
- **Best Performance**: When entries align with extreme oversold conditions (<10%)
- **Risk**: Whipsaws during choppy, trendless markets

### Combining Both Charts

For optimal decision-making, use both breadth charts together:

#### Strategic Positioning (Chart 1: 200MA Breadth)

- Determines overall market regime (bull, bear, neutral)
- Guides strategic asset allocation
- Identifies major entry/exit points for core positions
- Longer holding periods (months to year+)

#### Tactical Positioning (Chart 2: Uptrend Ratio)

- Determines short-term momentum and timing
- Guides tactical trades and position sizing
- Identifies short-term entry/exit points for swing trades
- Shorter holding periods (days to weeks)

#### Alignment Scenarios

**Scenario 1: Both Bullish**
- Chart 1: 8MA rising, 200MA rising or flat, breadth < 73%
- Chart 2: Green (uptrend), ratio rising from oversold
- **Action**: Maximum bullish stance, aggressive long positioning

**Scenario 2: Strategic Bullish, Tactical Bearish**
- Chart 1: 8MA rising, 200MA not yet peaked
- Chart 2: Red (downtrend), ratio elevated or falling
- **Action**: Hold core long positions, avoid new tactical longs, wait for oversold

**Scenario 3: Strategic Bearish, Tactical Bullish**
- Chart 1: 200MA peaked or declining
- Chart 2: Green (uptrend), ratio rising from extreme oversold
- **Action**: Short-term tactical longs only, tight stops, prepare for strategic exit

**Scenario 4: Both Bearish**
- Chart 1: Both MAs declining, pink background
- Chart 2: Red (downtrend), ratio falling
- **Action**: Defensive positioning, cash or short positions, wait for 8MA trough

### Analysis Checklist for Chart 2

When analyzing the uptrend stock ratio chart, systematically evaluate:

1. ✓ **Current Ratio Level**: What is the current uptrend stock percentage?
2. ✓ **Current Color**: Is the market in green (uptrend) or red (downtrend)?
3. ✓ **Proximity to Thresholds**: How close is the ratio to 10% (bottom) or 40% (top)?
4. ✓ **Trend Direction**: Is the ratio rising, falling, or flat?
5. ✓ **Recent Transitions**: Any recent color changes from red-to-green or green-to-red?
6. ✓ **Duration of Current Trend**: How long has the current color phase lasted?
7. ✓ **Strategy Position**: Based on the swing trading strategy, should one be long, flat, or preparing to enter/exit?
8. ✓ **Historical Context**: How does the current reading compare to recent extremes?

---

## Output Requirements

### Language and Style

- **Analysis Language**: Conduct all thinking and analysis in English
- **Output Format**: Generate all reports in English using markdown format
- **Tone**: Professional, objective, analytical
- **Terminology**: Use precise technical terms consistently

### Analysis Structure

Each breadth chart analysis report should include:

1. **Current Readings**: Specific values for all key metrics
2. **Signal Status**: Clear identification of any active signals (troughs, peaks, transitions)
3. **Market Regime Assessment**: Classification of the current market environment
4. **Strategy Implications**: Specific positioning recommendations based on the backtested strategies
5. **Key Levels to Watch**: Upcoming thresholds or levels that would change the analysis
6. **Risk Considerations**: Potential invalidation scenarios or alternative interpretations
7. **Combined Analysis** (when both charts analyzed): Integration of strategic and tactical perspectives

### Objectivity Standards

- Base all analysis strictly on observable chart data
- Avoid incorporating external information (news, fundamentals) unless specifically relevant to breadth interpretation
- Clearly distinguish between factual observations and probabilistic forecasts
- Acknowledge uncertainty when signals are ambiguous
- Present both bullish and bearish scenarios when appropriate

---

## Common Pitfalls to Avoid

### Chart 1 (200MA Breadth) Pitfalls

- **Misreading Recent Trend Direction** (MOST COMMON ERROR): Analyzing historical chart movement instead of focusing on the LATEST 3-5 data points at the rightmost edge. This leads to stating "8MA is rising" when it's actually falling at the current edge, or vice versa. ALWAYS analyze the rightmost data points to determine CURRENT slope.

- **Premature Entry**: Buying before clear 8MA reversal is confirmed (2-3 consecutive periods of increase). Entering on just a trough formation without confirmation often results in losses from failed reversals.

- **Ignoring Failed Reversals**: Not recognizing when an 8MA has rolled over after an initial bounce from a trough. If the 8MA rises briefly then turns down again, the signal is INVALID.

- **Late Exit**: Waiting for 200MA to decline instead of exiting at the peak formation. The peak itself is the sell signal - do not wait for confirmation of decline.

- **Ignoring Thresholds**: Not recognizing significance of 23% and 73% levels. These thresholds provide critical context for entry and exit timing.

- **Overtrading**: Trying to trade every wiggle in the 8MA instead of waiting for clear, confirmed trough reversals. Patience is essential for this strategy.

### Chart 2 (Uptrend Ratio) Pitfalls

- **Chasing**: Entering after the ratio has already risen substantially from oversold
- **Ignoring Color**: Focusing only on the ratio level without considering trend direction (color)
- **False Breakouts**: Not waiting for confirmation of color transitions
- **Missing Extremes**: Not recognizing when the ratio reaches <10% or >40%

### General Pitfalls

- **Analyzing in Isolation**: Using only one chart without considering the other
- **Over-Complicating**: Adding too many additional indicators that cloud the core signals
- **Recency Bias**: Giving too much weight to the most recent move
- **Ignoring Historical Context**: Not comparing current readings to historical patterns shown on the charts


---

## SKILL: breadth-chart-analyst

- Fuente: `tradermonty/claude-trading-skills` → `skills/breadth-chart-analyst` (MIT)
- Cuándo usarla: This skill should be used when analyzing market breadth charts, specifically the S&P 500 Breadth Index (200-Day MA based) and the US Stock Market Uptrend Stock Ratio charts. Use this skill when the user provides breadth chart images for analysis, requests market breadth assessment, positioning strategy recommendations, or wants to understand medium-term strategic and short-term tactical market outlook based on breadth indicators. Also works WITHOUT chart images by fetching CSV data directly from public sources. All analysis and output are conducted in English.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/breadth-chart-analyst/` (requirements.txt, detect_breadth_values.py, detect_uptrend_ratio.py, extract_chart_right_edge.py, fetch_breadth_csv.py)

# Breadth Chart Analyst

## Overview

This skill enables specialized analysis of two complementary market breadth charts that provide strategic (medium to long-term) and tactical (short-term) market perspectives. Analyze breadth chart images to assess market health, identify trading signals based on backtested strategies, and develop positioning recommendations. All thinking and output are conducted exclusively in English.

## When to Use

Use this skill when:
- User provides S&P 500 Breadth Index (200-Day MA based) chart images for analysis
- User provides US Stock Market Uptrend Stock Ratio chart images for analysis
- User requests market breadth assessment or market health evaluation
- User asks about medium-term strategic positioning based on breadth indicators
- User needs short-term tactical timing signals for swing trading
- User wants combined strategic and tactical market outlook
- **User requests breadth analysis WITHOUT providing chart images** (CSV data mode)

Do NOT use this skill when:
- User asks about individual stock analysis (use `us-stock-analysis` skill instead)
- User needs sector rotation analysis without breadth charts (use `sector-analyst` skill instead)
- User wants news-based market analysis (use `market-news-analyst` skill instead)

## Prerequisites

- **Chart Images Optional**: CSV data from public sources is the PRIMARY data source; chart images provide supplementary visual context
- **No API Keys Required**: CSV data is fetched from public GitHub Pages; no external API subscriptions needed
- **Language**: All analysis and output conducted in English

## Output

This skill generates markdown analysis reports saved to the `reports/` directory:
- Chart 1 only: `breadth_200ma_analysis_[YYYY-MM-DD].md`
- Chart 2 only: `uptrend_ratio_analysis_[YYYY-MM-DD].md`
- Both charts: `breadth_combined_analysis_[YYYY-MM-DD].md`

Reports include executive summaries, current readings, signal identification, scenario analysis with probabilities, and actionable positioning recommendations for different trader types.

## Core Principles

1. **Dual-Timeframe Analysis**: Combine strategic (Chart 1: 200MA Breadth) and tactical (Chart 2: Uptrend Ratio) perspectives
2. **Backtested Strategy Focus**: Apply proven systematic strategies based on historical patterns
3. **Objective Signal Identification**: Focus on clearly defined thresholds, transitions, and markers
4. **English Communication**: Conduct all analysis and generate all reports in English
5. **Actionable Recommendations**: Provide specific positioning guidance for different investor types

## Chart Types and Purposes

### Chart 1: S&P 500 Breadth Index (200-Day MA Based)

**Purpose**: Medium to long-term strategic market positioning

**Key Elements**:
- **8-Day MA (Orange Line)**: Short-term breadth trend, primary entry signal generator
- **200-Day MA (Green Line)**: Long-term breadth trend, primary exit signal generator
- **Red Dashed Line (73%)**: Average peak level - market overheating threshold
- **Blue Dashed Line (23%)**: Average 8MA trough level - extreme oversold, excellent buying opportunity
- **Triangles**:
  - Purple ▼ = 8MA troughs (buy signal when reverses)
  - Blue ▼ = 200MA troughs (major cycle lows)
  - Red ▲ = 200MA peaks (sell signal)
- **Pink Background**: Downtrend periods

**Backtested Strategy**:
- **BUY**: When 8MA reverses from a trough (especially below 23%)
- **SELL**: When 200MA forms a peak (typically near/above 73%)
- **Result**: Historically high performance, avoids bear markets

### Chart 2: US Stock Market - Uptrend Stock Ratio

**Purpose**: Short-term tactical timing and swing trading

**Key Elements**:
- **Uptrend Stock Definition**: Stocks above 200MA/50MA/20MA with positive 1-month performance
- **Green Regions**: Market in uptrend phase
- **Red Regions**: Market in downtrend phase
- **~10% Level (Lower Orange Dashed)**: Short-term bottom, extreme oversold
- **~40% Level (Upper Orange Dashed)**: Short-term top, market overheating

**Swing Trading Strategy**:
- **ENTER LONG**: When color changes from red to green (especially from <10-15% levels)
- **EXIT LONG**: When color changes from green to red (especially from >35-40% levels)
- **Timeframe**: Days to weeks

## Analysis Workflow

### Step 0: Fetch CSV Data (PRIMARY SOURCE - MANDATORY)

**CRITICAL**: CSV data is the PRIMARY source for all Breadth values. This step MUST be executed BEFORE any image analysis.

```bash
python3 skills/breadth-chart-analyst/scripts/fetch_breadth_csv.py
```

**Why CSV is PRIMARY**:
- OpenCV image detection is fragile -- chart format changes cause catastrophic failures (Issue #7)
- CSV provides exact numerical values directly from the data source
- Image analysis is SUPPLEMENTARY only (for visual trend context)

**Data Sources**:
1. **Market Breadth**: `tradermonty.github.io/market-breadth-analysis/market_breadth_data.csv`
   - Provides: 200-Day MA, 8-Day MA, Trend, Dead Cross status
2. **Uptrend Ratio**: `tradermonty/uptrend-dashboard/data/uptrend_ratio_timeseries.csv`
   - Provides: Current ratio, 10MA, slope, trend (UP/DOWN), color (GREEN/RED)
3. **Sector Summary**: `tradermonty/uptrend-dashboard/data/sector_summary.csv`
   - Provides: Per-sector ratio, trend, status (overbought/oversold)

**Data Source Priority**:
| Priority | Source | Use For | Reliability |
|----------|--------|---------|-------------|
| 1 (PRIMARY) | **CSV Data** | All numerical values, dead cross status, color | HIGH |
| 2 (SUPPLEMENTARY) | **Chart Image** | Visual trend context, pattern confirmation | MEDIUM |
| 3 (DEPRECATED) | ~~OpenCV detect_breadth_values.py~~ | ~~Breadth detection~~ | **UNRELIABLE** |
| 4 (LAST RESORT) | ~~LLM visual reading~~ | ~~Emergency only~~ | LOW |

**Expected Output**:
```
============================================================
Breadth Data (CSV) - 2026-02-13
============================================================
--- Market Breadth (S&P 500) ---
200-Day MA: 62.26% (healthy (>=60%))
8-Day MA:   67.56% (healthy_bullish (60-73%))
8MA vs 200MA: +5.30pt (8MA ABOVE -- NO dead cross)
Trend: UPTREND
--- Uptrend Ratio (All Markets) ---
Current: 33.03% GREEN (neutral_bullish)
10MA: 32.65%, Slope: +0.0055, Trend: UP
--- Sector Summary ---
...
============================================================
```

**Validation**: After running CSV fetch, verify:
- [ ] CSV data retrieved successfully
- [ ] 200-Day MA value recorded
- [ ] 8-Day MA value recorded
- [ ] Dead cross status determined (8MA < 200MA = dead cross)
- [ ] Uptrend Ratio value + color + trend recorded
- [ ] Use these CSV values as the authoritative source for all subsequent analysis

---

### Step 1: Receive Chart Images and Prepare Analysis

When the user provides breadth chart images for analysis:

1. Confirm receipt of chart image(s)
2. Identify which chart(s) are provided:
   - Chart 1 only (200MA Breadth)
   - Chart 2 only (Uptrend Ratio)
   - Both charts
3. Note any specific focus areas or questions from the user
4. **CRITICAL: Extract right edge of chart images before analysis** (Step 1.5)

**If NO chart images are provided**: Skip Steps 1, 1.5, and image-based analysis. Use CSV data from Step 0 as the sole data source and proceed directly to the analysis and report generation steps.

**Language Note**: All subsequent thinking, analysis, and output will be in English.

### Step 1.5: Two-Stage Chart Analysis (MANDATORY when charts provided)

**CRITICAL**: Use a **two-stage analysis** approach to prevent misreading historical data as current values.

#### Stage 1: Full Chart Analysis (Historical Context)

First, analyze the FULL chart image to understand:
- Overall historical trend and cycles
- Key historical events (troughs, peaks, recoveries)
- Long-term patterns and context

#### Stage 2: Right Edge Focused Analysis (Current Values)

Then, extract and analyze the **rightmost 25%** of the chart to accurately determine CURRENT values.

**Execute the Python script to extract the right edge:**

```bash
python3 skills/breadth-chart-analyst/scripts/extract_chart_right_edge.py <image_path> --percent 25
```

#### Why Two-Stage Analysis is Mandatory

| Stage | Purpose | What to Extract |
|-------|---------|-----------------|
| **Stage 1 (Full)** | Historical context, trend cycles | Overall patterns, past troughs/peaks |
| **Stage 2 (Right Edge)** | **Current values (CRITICAL)** | 8MA value, 200MA value, current color, current slope |

**Common Error This Prevents:**
- LLM reads 2025 mid-year dip (8MA ~25-30%) instead of current value (8MA ~60-65%)
- By isolating the right edge, the "current" data is unambiguous

#### Analysis Protocol

1. **Read full chart** → Document historical context
2. **Run extraction script** → Generate right edge image
3. **Read right edge image** → Document current values with HIGH CONFIDENCE
4. **Cross-check**: If Stage 1 and Stage 2 values differ significantly, **Stage 2 (right edge) takes precedence**
5. **Report both**: Include Stage 1 context AND Stage 2 current values in analysis

### Step 2: Load Breadth Chart Methodology

Before beginning analysis, read the comprehensive breadth chart methodology:

```
Read: references/breadth_chart_methodology.md
```

This reference contains detailed guidance on:
- Chart 1: 200MA-based breadth index interpretation and strategy
- Chart 2: Uptrend stock ratio interpretation and strategy
- Signal identification and threshold significance
- Strategy rules and risk management
- Combining both charts for optimal decision-making
- Common pitfalls to avoid

### Step 3: Examine Sample Charts (First Time or for Reference)

To understand the chart format and visual elements, review the sample charts included in this skill:

```
View: assets/SP500_Breadth_Index_200MA_8MA.jpeg
View: assets/US_Stock_Market_Uptrend_Ratio.jpeg
```

These samples demonstrate:
- Visual appearance and structure of each chart type
- How signals and thresholds are displayed
- Color coding and marker systems
- Historical patterns and cycles

### Step 4: Analyze Chart 1 (200MA-Based Breadth Index)

If Chart 1 is provided, conduct systematic analysis:

#### 4.1 Extract Current Readings

From the chart image, identify:
- **Current 8MA level** (orange line): Specific percentage
- **Current 200MA level** (green line): Specific percentage
- **8MA slope**: Rising, falling, or flat
- **200MA slope**: Rising, falling, or flat
- **Distance from 73% threshold**: How close to overheating
- **Distance from 23% threshold**: How close to extreme oversold
- **Most recent date** visible on the chart

#### 4.1.5 CRITICAL: Latest Data Point Detailed Trend Analysis

**This step is MANDATORY to avoid misreading recent trend changes.**

**CRITICAL WARNING**: Charts can be deceptive. The MAJORITY of analysis errors occur because the analyst:
1. Confuses the 8MA (orange) with the 200MA (green)
2. Reads historical trends instead of the CURRENT rightmost data points
3. Misidentifies which line is rising vs falling

**BEFORE analyzing trend direction, FIRST confirm line colors**:
- ✓ **8MA = ORANGE line** (fast-moving, more volatile)
- ✓ **200MA = GREEN line** (slow-moving, smoother)
- If unsure which is which, STOP and re-examine the chart legend/colors

Focus intensively on the **rightmost 3-5 data points** of the chart (most recent weeks):

**For 8MA (Orange Line) - Analyze the very latest trajectory**:
1. **Identify the absolute latest position**: Where is the 8MA at the rightmost edge of the chart?
2. **Trace back 3-5 data points** (approximately 3-5 weeks):
   - What was the 8MA level 1 week ago?
   - What was the 8MA level 2 weeks ago?
   - What was the 8MA level 3 weeks ago?
3. **Calculate the directional change**:
   - Is the latest value HIGHER or LOWER than 1 week ago?
   - Is the latest value HIGHER or LOWER than 2 weeks ago?
   - What is the trend: consistently rising, consistently falling, or mixed?
4. **Determine the CURRENT slope** (not historical slope):
   - **Rising**: Latest data point is higher than previous 2-3 points AND shows upward curvature
   - **Falling**: Latest data point is lower than previous 2-3 points AND shows downward curvature
   - **Flat**: Latest data point is approximately equal to previous points (within 2-3%)

**Critical Questions to Answer**:
- [ ] Is the 8MA currently moving UP or DOWN at the rightmost edge?
- [ ] If there was a recent trough, has the 8MA **sustained** the upward move, or has it rolled over?
- [ ] Count consecutive periods of increase: How many consecutive periods has 8MA risen? (Need 2-3 for confirmation)
- [ ] Count consecutive periods of decrease: How many consecutive periods has 8MA fallen? (Indicates failed reversal if declining after trough)

**For 200MA (Green Line) - Analyze the very latest trajectory**:
1. **Identify the absolute latest position**: Where is the 200MA at the rightmost edge?
2. **Trace back 4-6 weeks**:
   - What was the 200MA level 2 weeks ago?
   - What was the 200MA level 4 weeks ago?
3. **Determine the CURRENT slope**:
   - Is it rising, falling, or flat in the most recent period?

**Failed Reversal Detection** (CRITICAL):
If an 8MA trough (purple ▼) was recently identified:
- [ ] Did the 8MA rise for only 1-2 periods and then turn back down?
- [ ] Did the 8MA fail to reach 60% before turning down?
- [ ] Is the 8MA currently declining again after the bounce?
- **If YES to any**: This is a **FAILED REVERSAL** - DO NOT ENTER, signal is INVALID

**Example Analysis Format**:
```
Latest 8MA Data Points (rightmost to left):
- Current (Week 0): 48%
- 1 week ago: 52%
- 2 weeks ago: 55%
- 3 weeks ago: 50%

Analysis: 8MA is FALLING. It rose from 50% to 55% (weeks 3-2), but has since declined to 48%.
This shows a failed reversal pattern - bounce was temporary, downtrend has resumed.
SLOPE: Falling (not rising!)
```

**MANDATORY CROSS-CHECK** (to catch misreadings):
After determining the trend, ask yourself:
- [ ] "If I claimed 8MA is RISING, but it's actually been FALLING for weeks, what would that look like?"
  - Answer: The rightmost data points would be LOWER than previous points (confirming FALLING)
- [ ] "Does my analysis match the visual slope of the orange line at the rightmost edge?"
  - If orange line visually slopes DOWN at the right edge → It's FALLING
  - If orange line visually slopes UP at the right edge → It's RISING
- [ ] "Is there any pink background shading (downtrend) near the rightmost edge?"
  - If YES → This confirms downtrend conditions, 8MA is likely FALLING
- [ ] "Are the 8MA and 200MA converging (getting closer) or diverging?"
  - Converging from below → Potential death cross forming → BEARISH
  - Converging from above → Potential golden cross forming → BULLISH

#### 4.2 Identify Signal Markers

Look for and document:
- **Most recent 8MA trough (purple ▼)**: Date and level
- **Most recent 200MA trough (blue ▼)**: Date and level (if visible in timeframe)
- **Most recent 200MA peak (red ▲)**: Date and level
- **Days/weeks since most recent signals**
- **Any pink background shading** (downtrend periods)

#### 4.3 Assess Market Regime

Based on readings and patterns, classify the current market as:
- Healthy Bull Market
- Overheated Bull Market
- Market Top/Distribution Phase
- Bear Market/Correction
- Capitulation/Extreme Oversold
- Early Recovery

Support the classification with specific evidence from the chart.

#### 4.4 Determine Strategy Position

Apply the backtested strategy rules with STRICT confirmation requirements:

**Check for BUY signal** (ALL criteria must be met):
1. ✓ **Trough Formation**: Has 8MA formed a clear trough (purple ▼)?
2. ✓ **Reversal Initiated**: Has 8MA begun to move upward from the trough?
3. ✓ **Confirmation Achieved**: Has 8MA risen for 2-3 CONSECUTIVE periods after the trough?
4. ✓ **No Recent Reversal**: Based on Step 4.1.5 analysis, is 8MA CURRENTLY rising (not falling)?
5. ✓ **Sustained Move**: Has 8MA maintained the upward trajectory without rolling over?
6. ⭐ **Optional but Strong**: Is 8MA below or near 23% (extreme oversold) at trough?

**BUY Signal Status**:
- **CONFIRMED**: All 5 required criteria met → ENTER LONG
- **DEVELOPING**: Trough formed, but < 2-3 consecutive increases → WAIT, MONITOR
- **FAILED**: Trough formed, but 8MA has rolled over and is declining → DO NOT ENTER, WAIT FOR NEXT TROUGH
- **NO SIGNAL**: No trough formed → WAIT

**Check for SELL signal**:
- Has 200MA formed a peak (red ▲)?
- Is 200MA near or above 73%?
- Is this an active sell signal requiring position exit?

**Current position determination**:
- **Long**: BUY signal confirmed, position entered and held
- **Preparing to Enter**: BUY signal developing (trough formed, watching for confirmation)
- **WAIT / Flat**: No valid signal OR failed reversal detected
- **Preparing to Exit**: SELL signal developing (200MA approaching peak)

#### 4.5 Develop Scenarios

Create 2-3 scenarios with probability estimates:
- Base case scenario (highest probability)
- Alternative scenario(s)
- Each scenario includes: description, supporting factors, strategy implications, key levels

### Step 5: Analyze Chart 2 (Uptrend Stock Ratio)

If Chart 2 is provided, conduct systematic analysis:

#### 5.0 ~~MANDATORY~~ DEPRECATED: Uptrend Ratio Detection Script (Superseded by Step 0 CSV Fetch)

**NOTE (Issue #7)**: This OpenCV detection step is **DEPRECATED**. Use CSV data from Step 0 as the PRIMARY source. The OpenCV script may be run for supplementary validation only, but CSV values take precedence in all cases.

```bash
python3 skills/breadth-chart-analyst/scripts/detect_uptrend_ratio.py <image_path> [--debug]
```

#### 5.1 Extract Current Readings

From the chart image, identify:
- **Current uptrend stock ratio**: Specific percentage
- **Current color**: Green (uptrend) or Red (downtrend)
- **Ratio slope**: Rising, falling, or flat
- **Distance from 10% threshold**: How close to extreme oversold
- **Distance from 40% threshold**: How close to overbought
- **Most recent date** visible on the chart

#### 5.2 Identify Trend Transitions

Look for and document:
- **Most recent red-to-green transition**: Date and ratio level at transition
- **Most recent green-to-red transition**: Date and ratio level at transition
- **Duration of current color phase**: How long in current trend
- **Days/weeks since most recent transition**

#### 5.3 Assess Market Condition

Based on current ratio and color, classify as:
- Extreme Oversold (<10%)
- Moderate Bearish (10-20%, red)
- Neutral/Transitional (20-30%)
- Moderate Bullish (30-37%, green)
- Extreme Overbought (>37-40%)

Support the classification with specific evidence from the chart.

#### 5.4 Determine Trading Position

Apply the swing trading strategy rules:

**Check for ENTER LONG signal**:
- Has color changed from red to green?
- Was the transition from an oversold level (<15%)?
- Is the transition confirmed (2-3 days of green)?

**Check for EXIT LONG signal**:
- Has color changed from green to red?
- Was the transition from an overbought level (>35%)?
- Is momentum weakening?

**Current position**: Long, Flat, Preparing to Enter, or Preparing to Exit

#### 5.5 Develop Scenarios

Create 2-3 scenarios with probability estimates:
- Base case scenario (highest probability)
- Alternative scenario(s)
- Each scenario includes: description, supporting factors, trading implications, key levels

### Step 6: Combined Analysis (When Both Charts Provided)

If both charts are provided, integrate the strategic and tactical perspectives:

#### 6.1 Alignment Assessment

Create a positioning matrix:
- **Chart 1 (Strategic)**: Bullish / Bearish / Neutral + signal status
- **Chart 2 (Tactical)**: Bullish / Bearish / Neutral + signal status
- **Combined Implication**: How do they align or conflict?

#### 6.2 Scenario Classification

Determine which of the four scenarios applies:

**Scenario 1: Both Bullish**
- Chart 1: 8MA rising, 200MA not yet peaked
- Chart 2: Green (uptrend), ratio rising from oversold
- Implication: Maximum bullish stance, aggressive positioning

**Scenario 2: Strategic Bullish, Tactical Bearish**
- Chart 1: 8MA rising, 200MA not yet peaked
- Chart 2: Red (downtrend), ratio falling or elevated
- Implication: Hold core long positions, wait for tactical entry

**Scenario 3: Strategic Bearish, Tactical Bullish**
- Chart 1: 200MA peaked or declining
- Chart 2: Green (uptrend), ratio rising
- Implication: Short-term tactical trades only, tight stops

**Scenario 4: Both Bearish**
- Chart 1: Both MAs declining
- Chart 2: Red (downtrend), ratio falling
- Implication: Defensive positioning, cash or shorts

#### 6.3 Unified Recommendation

Provide integrated positioning guidance for:
- **Long-term investors** (based primarily on Chart 1)
- **Swing traders** (based primarily on Chart 2)
- **Active tactical traders** (based on combination)

Address any conflicts between charts and explain resolution.

### Step 7: Generate Analysis Report in English

Create a comprehensive markdown report using the template structure:

```
Read and use as template: assets/breadth_analysis_template.md
```

**IMPORTANT**: All analysis and output must be in English.

The report structure varies based on which chart(s) are analyzed:

**If Chart 1 only**:
- Executive Summary
- Chart 1 full analysis sections
- Summary and Conclusion
- Omit Chart 2 and Combined Analysis sections

**If Chart 2 only**:
- Executive Summary
- Chart 2 full analysis sections
- Summary and Conclusion
- Omit Chart 1 and Combined Analysis sections

**If Both Charts**:
- Executive Summary
- Chart 1 full analysis sections
- Chart 2 full analysis sections
- Combined Analysis section (mandatory)
- Summary and Conclusion

**File Naming Convention**: Save each analysis as:
- Chart 1 only: `breadth_200ma_analysis_[YYYY-MM-DD].md`
- Chart 2 only: `uptrend_ratio_analysis_[YYYY-MM-DD].md`
- Both charts: `breadth_combined_analysis_[YYYY-MM-DD].md`

### Step 8: Quality Assurance

Before finalizing the report, verify:

1. ✓ **Language**: All content is in English (thinking and output)
2. ✓ **Line Color Verification**: Explicitly confirmed 8MA = ORANGE, 200MA = GREEN before trend analysis
3. ✓ **Latest Data Trend Analysis**: Step 4.1.5 was thoroughly completed - the most recent 3-5 data points were analyzed to determine CURRENT trend direction
4. ✓ **Trend Direction Accuracy**: The stated 8MA slope (Rising/Falling/Flat) accurately reflects the RIGHTMOST data points, not historical movement
5. ✓ **Cross-Check Completed**: MANDATORY CROSS-CHECK questions were answered to confirm trend direction matches visual slope
6. ✓ **Death/Golden Cross Check**: If 8MA and 200MA are converging, explicitly identified whether death cross or golden cross is forming
7. ✓ **Failed Reversal Check**: If a trough was identified, explicitly verified whether the reversal sustained or failed by analyzing latest trajectory
8. ✓ **Specific Values**: All readings include specific percentages/levels, not vague descriptions
9. ✓ **Signal Status**: Clear identification of active signals (CONFIRMED BUY / DEVELOPING / FAILED / SELL / WAIT)
10. ✓ **Strategy Alignment**: Recommendations align with backtested strategies and confirmation requirements
11. ✓ **Probabilities**: Scenario probabilities sum to 100%
12. ✓ **Actionable**: Clear positioning recommendations for different trader types
13. ✓ **Context**: Historical comparison and reference to similar past situations
14. ✓ **Risk Management**: Invalidation levels and risk factors clearly stated

**FINAL SANITY CHECK**:
- [ ] If report claims "BUY signal" or "8MA rising", confirm this doesn't contradict user's chart showing death cross or downtrend
- [ ] If report claims "bullish", confirm there's no pink background shading or death cross visible
- [ ] If unsure about ANY trend direction, explicitly state uncertainty rather than guessing

## Quality Standards

### Objectivity Requirements

- Base all analysis strictly on observable chart data
- Do not incorporate external information (news, fundamentals) unless specifically relevant
- Use precise technical terminology consistently
- Distinguish clearly between factual observations and probabilistic forecasts
- Acknowledge uncertainty when signals are ambiguous

### Completeness Requirements

- Address all relevant sections of the analysis template
- Provide specific numerical values for all key metrics
- Justify probability estimates with technical factors
- Include invalidation levels for each scenario
- Compare current readings to historical patterns visible on the charts

### Clarity Requirements

- Write in professional, analytical English
- Use clear section headings and structure
- Present information in tables where appropriate
- Make recommendations specific and actionable
- Avoid jargon without explanation

### Strategy Adherence Requirements

- Apply backtested strategy rules correctly
- Distinguish between strategic (Chart 1) and tactical (Chart 2) signals
- Provide clear position status (Long/Flat/Entering/Exiting)
- Include specific entry/exit levels when applicable
- Address risk management (stop losses, position sizing)

## Common Analysis Errors and How to Avoid Them

### Error 1: Confusing 8MA with 200MA

**Symptom**: Report claims 8MA is rising when it's actually the 200MA that's rising

**Prevention**:
- ALWAYS verify: 8MA = ORANGE, 200MA = GREEN
- Check line volatility: 8MA moves faster with more volatility
- If unsure, state: "Based on line color, I identify the [orange/green] line as [8MA/200MA]"

### Error 2: Reading Historical Trends Instead of Current Direction

**Symptom**: Report describes what happened 1-2 months ago, not what's happening NOW

**Prevention**:
- Focus ONLY on rightmost 3-5 data points
- Explicitly write: "At the CURRENT rightmost edge, 8MA is at X% and is [rising/falling]"
- Ignore what happened in September if we're analyzing November

### Error 3: Missing Death Cross or Golden Cross Formation

**Symptom**: Report is bullish when 8MA and 200MA are about to death cross (bearish)

**Prevention**:
- ALWAYS check: "Are 8MA and 200MA getting closer (converging) or further apart (diverging)?"
- If converging with 8MA above 200MA → Potential death cross → BEARISH
- If converging with 8MA below 200MA → Potential golden cross → BULLISH
- Explicitly state: "8MA is currently [above/below] 200MA, and they are [converging/diverging]"

### Error 4: Ignoring Pink Background Shading

**Symptom**: Report claims bullish setup when chart shows pink downtrend background

**Prevention**:
- Check for pink shading at the rightmost edge
- Pink background = Downtrend period = Bearish conditions
- If pink shading present, report MUST acknowledge bearish conditions

### Error 5: Claiming Reversal Too Early

**Symptom**: Report says "BUY signal confirmed" after only 1 week of increase

**Prevention**:
- Require 2-3 CONSECUTIVE weeks of 8MA increase for confirmation
- If only 1 week: Signal is "DEVELOPING", not "CONFIRMED"
- If 8MA rises then falls again: Signal is "FAILED", not valid

## Example Usage Scenarios

### Example 1: CSV-Only Analysis (No Charts)

```
User: "breadth分析して" (Analyze breadth)
[No chart images provided]

Breadth Analyst:
1. Executes fetch_breadth_csv.py to get latest CSV data
2. Reads breadth_chart_methodology.md
3. Analyzes CSV data:
   - 200MA: 62.26% (healthy)
   - 8MA: 67.56% (healthy_bullish)
   - 8MA vs 200MA: +5.30pt (NO dead cross)
   - Uptrend Ratio: 33.03% GREEN (neutral_bullish)
   - Sector summary with overbought/oversold sectors
4. Assesses market regime based on CSV values
5. Generates report: breadth_combined_analysis_2026-03-16.md
```

### Example 2: Strategic Breadth Analysis (Chart 1 Only)

```
User: "Please analyze this S&P 500 breadth chart and tell me where we are in the market cycle."
[Provides Chart 1 image: 200MA Breadth Index]

Breadth Analyst (thinking in English):
1. Executes CSV fetch for authoritative numerical values
2. Confirms receipt of Chart 1 (200MA-based breadth index)
3. Reads breadth_chart_methodology.md for Chart 1 guidance
4. Two-stage analysis: full chart → right edge extraction
5. Cross-checks CSV values with chart readings
6. Generates comprehensive report in English
```

### Example 3: Combined Strategic + Tactical Analysis (Both Charts)

```
User: "Analyze both of these breadth charts and give me your overall market view."
[Provides both Chart 1 and Chart 2 images]

Breadth Analyst (thinking in English):
1. Executes CSV fetch as PRIMARY source
2. Confirms receipt of both charts
3. Reads full breadth_chart_methodology.md
4. Two-stage analysis for each chart
5. Cross-checks all values against CSV data
6. Combined assessment and unified recommendation
7. Generates comprehensive combined report
```

## Resources

This skill includes the following bundled resources:

### references/breadth_chart_methodology.md

Comprehensive methodology covering:
- **Chart 1 (200MA Breadth)**: Components, interpretation, market regimes, backtested strategy, analysis checklist
- **Chart 2 (Uptrend Ratio)**: Components, interpretation, market conditions, swing trading strategy, analysis checklist
- **Combined Analysis**: Alignment scenarios, integrated decision-making
- **Common Pitfalls**: Mistakes to avoid for each chart type

**Usage**: Read this file before conducting any breadth chart analysis to ensure systematic, accurate interpretation.

### assets/breadth_analysis_template.md

Structured template for breadth analysis reports in English.

**Usage**: Use this template structure for every analysis report.

### assets/SP500_Breadth_Index_200MA_8MA.jpeg

Sample Chart 1 image for format reference.

### assets/US_Stock_Market_Uptrend_Ratio.jpeg

Sample Chart 2 image for format reference.

### scripts/fetch_breadth_csv.py

**PRIMARY data source**. Fetches market breadth, uptrend ratio, and sector summary data from public CSV sources. Uses only stdlib (urllib + csv) -- no external dependencies.

```bash
python3 skills/breadth-chart-analyst/scripts/fetch_breadth_csv.py        # Human-readable
python3 skills/breadth-chart-analyst/scripts/fetch_breadth_csv.py --json  # JSON output
```

### scripts/extract_chart_right_edge.py

Extracts the rightmost portion of chart images to help focus on latest data points. Requires PIL/Pillow.

```bash
python3 skills/breadth-chart-analyst/scripts/extract_chart_right_edge.py <image_path> --percent 25
```

### scripts/detect_uptrend_ratio.py (DEPRECATED)

OpenCV-based uptrend ratio detection. Superseded by CSV fetch. Requires opencv-python + numpy.

### scripts/detect_breadth_values.py (DEPRECATED)

OpenCV-based breadth value detection. Superseded by CSV fetch. Requires opencv-python + numpy.

## Special Notes

### Language Requirement

**CRITICAL**: All analysis, thinking, and output MUST be in English. This includes:
- Internal analysis and reasoning
- Report generation
- Tables and data presentation
- Scenario descriptions
- Recommendations

Do not translate or use any other language. The user expects English output exclusively.

### Strategy Focus

This skill emphasizes backtested, systematic strategies rather than discretionary interpretation. Always:
- Apply the strategy rules as documented
- Reference historical performance patterns
- Provide specific entry/exit criteria
- Include risk management guidance

### Practical Application

The goal is actionable intelligence. Every analysis should answer:
- **Strategic**: Should I be long, flat, or short the market over the medium term?
- **Tactical**: Should I enter or exit positions in the short term?
- **Timing**: When should I act, and at what levels?
- **Risk**: What would invalidate this view, and where should stops be?

### Referencia: assets/breadth_analysis_template.md

# Market Breadth Analysis Report

**Analysis Date**: [YYYY-MM-DD]
**Analyst**: Claude Breadth Chart Specialist
**Charts Analyzed**: [Chart 1 only / Chart 2 only / Both Charts]

---

## Executive Summary

[Brief 2-4 sentence overview of the key findings from the breadth analysis]

**Strategic Outlook**: [Bullish / Bearish / Neutral]
**Tactical Outlook**: [Bullish / Bearish / Neutral]
**Overall Recommendation**: [Aggressive Long / Moderate Long / Neutral / Defensive / Short]

---

# Chart 1: S&P 500 Breadth Index (200-Day MA Based)

## Current Readings

**Date of Latest Data**: [Latest date visible on chart]

### Key Metrics

| Metric | Current Value | Interpretation |
|--------|---------------|----------------|
| 8-Day MA (Orange) | [X.XX / XX%] | [Above/Below/At threshold] |
| 200-Day MA (Green) | [X.XX / XX%] | [Above/Below/At threshold] |
| Distance from 73% Peak Threshold | [+/- XX%] | [Overheated / Normal / Oversold] |
| Distance from 23% Trough Threshold | [+/- XX%] | [Extreme Oversold / Normal / Elevated] |

### Trend Direction

- **8MA Slope**: [Rising / Falling / Flat] - [Brief description of trajectory]
- **200MA Slope**: [Rising / Falling / Flat] - [Brief description of trajectory]
- **Trend Alignment**: [Both Rising / Both Falling / Diverging / Mixed]

### Latest Data Point Trend Analysis (CRITICAL)

**Focus: Rightmost 3-5 Data Points**

**8MA Recent Trajectory** (Week-by-Week from trough/recent period to present):
- **Current Level** (Week 0): [XX%]
- **1 Week Ago** (Week -1): [XX%] - Change: [+/-XX%]
- **2 Weeks Ago** (Week -2): [XX%] - Change: [+/-XX%]
- **3 Weeks Ago** (Week -3): [XX%] - Change: [+/-XX%]

**Consecutive Period Analysis**:
- Consecutive Increases: [X periods]
- Consecutive Decreases: [X periods]
- Current Momentum: [Accelerating Up / Steady Up / Decelerating / Turning Down / Falling]

**CURRENT Slope Determination** (based on latest edge):
- [ ] Rising: Latest value higher than previous 2-3 points with upward curvature
- [ ] Falling: Latest value lower than previous 2-3 points with downward curvature
- [ ] Flat: Latest value approximately equal to previous points (±2-3%)

**Failed Reversal Check** (if trough recently formed):
- [ ] Has 8MA rolled over after initial bounce?
- [ ] Has 8MA declined for 1-2+ consecutive periods after rising?
- [ ] Has 8MA failed to reach 55-60% before turning down?

**Conclusion**: The 8MA is [CURRENTLY RISING / CURRENTLY FALLING / FLAT] based on the rightmost data points.

## Signal Status

### Recent Signal Markers

**8MA Troughs (Purple ▼)**:
- Most Recent: [Date] at [XX%]
- Status: [X days/weeks since trough]
- Reversal Confirmed: [Yes / No / Developing]

**200MA Troughs (Blue ▼)**:
- Most Recent: [Date] at [XX%]
- Significance: [Major cycle low / Historical context]

**200MA Peaks (Red ▲)**:
- Most Recent: [Date] at [XX%]
- Status: [X days/weeks since peak]
- Implications: [Exit signal active / Historical peak]

### Active Signals

**Current Strategy Signal**: [CONFIRMED BUY / DEVELOPING BUY / FAILED REVERSAL / SELL / HOLD / WAIT]

**Signal Classification**:
- **CONFIRMED BUY**: Trough formed + 2-3 consecutive increases + CURRENTLY rising → ENTER LONG
- **DEVELOPING BUY**: Trough formed + < 2 consecutive increases → WAIT, MONITOR
- **FAILED REVERSAL**: Trough formed + initially rose + now declining → DO NOT ENTER
- **SELL**: 200MA peak formed → EXIT LONG
- **HOLD**: Already long, no exit signal → MAINTAIN POSITION
- **WAIT**: No trough, or waiting for new trough after failed reversal → STAY FLAT

[Detailed explanation of why this signal status is assigned, including specific reference to Latest Data Point Trend Analysis findings]

## Market Regime Assessment

**Current Regime**: [Healthy Bull Market / Overheated Bull Market / Market Top/Distribution / Bear Market/Correction / Capitulation/Extreme Oversold / Early Recovery]

### Regime Characteristics

[Detailed description of the current market regime, including:]
- Key observations supporting this classification
- How current readings align with historical patterns
- Typical duration and behavior in this regime

### Supporting Evidence

1. [First piece of evidence]
2. [Second piece of evidence]
3. [Third piece of evidence]

## Historical Context

### Comparison to Previous Cycles

[Analysis comparing current readings to previous similar situations shown on the chart]

**Similar Historical Periods**:
- **[Date Range 1]**: [Brief description and outcome]
- **[Date Range 2]**: [Brief description and outcome]
- **[Date Range 3]**: [Brief description and outcome]

### Distance from Extremes

- **Time Since Last 8MA Trough**: [X weeks/months]
- **Time Since Last 200MA Peak**: [X weeks/months]
- **Current Reading vs Historical Average**: [Above/Below by XX%]

## Strategy Implications

### Backtested Strategy Positioning

**Current Position**: [Long / Flat / Preparing to Enter / Preparing to Exit]

#### Entry Analysis

**Entry Signal Status**: [Active / Not Active / Pending]

[If active or pending:]
- **Entry Trigger**: [Description of what triggered or would trigger entry]
- **Confirmation Criteria**: [What needs to happen for confirmation]
- **Optimal Entry Zone**: [Price/breadth level range]
- **Entry Timing**: [Immediate / Wait for X / Already entered]

[If not active:]
- **What Would Trigger Entry**: [Specific conditions needed]
- **Estimated Distance to Entry**: [How far from entry conditions]

#### Exit Analysis

**Exit Signal Status**: [Active / Not Active / Monitoring]

[If active or monitoring:]
- **Exit Trigger**: [Description of what triggered or would trigger exit]
- **Key Level to Watch**: [Specific breadth level or 200MA behavior]
- **Exit Timing**: [Immediate / Prepare to exit / Not yet]

[If not active:]
- **What Would Trigger Exit**: [Specific conditions needed]
- **Estimated Distance to Exit**: [How far from exit conditions]

### Risk Management

**Current Risk Level**: [Low / Moderate / High / Extreme]

**Risk Factors**:
- [Risk factor 1]
- [Risk factor 2]
- [Risk factor 3]

**Invalidation Levels**:
- **Bullish Case Invalidation**: [Specific level or condition]
- **Bearish Case Invalidation**: [Specific level or condition]

## Key Levels to Monitor

### Critical Thresholds

1. **[Level 1]**: [Description and significance]
2. **[Level 2]**: [Description and significance]
3. **[Level 3]**: [Description and significance]

### Upcoming Milestones

- **Near-term** (Next 1-2 weeks): [What to watch for]
- **Medium-term** (Next 1-2 months): [What to watch for]
- **Long-term** (Next 3-6 months): [What to watch for]

## Scenario Analysis

### Base Case Scenario: [Title] - **[XX]% Probability**

**Description**: [What this scenario entails]

**Supporting Factors**:
- [Factor 1]
- [Factor 2]
- [Factor 3]

**Implications**:
- Strategy Position: [Long/Flat/Short]
- Expected Duration: [Timeframe]
- Key Levels: [Targets or invalidation levels]

---

### Alternative Scenario: [Title] - **[XX]% Probability**

**Description**: [What this scenario entails]

**Supporting Factors**:
- [Factor 1]
- [Factor 2]

**Implications**:
- Strategy Position: [Long/Flat/Short]
- Expected Duration: [Timeframe]
- Key Levels: [Targets or invalidation levels]

---

# Chart 2: US Stock Market - Uptrend Stock Ratio

## Current Readings

**Date of Latest Data**: [Latest date visible on chart]

### Key Metrics

| Metric | Current Value | Interpretation |
|--------|---------------|----------------|
| Uptrend Stock Ratio | [XX.X%] | [Oversold / Normal / Overbought] |
| Current Trend Color | [Green / Red] | [Uptrend / Downtrend] |
| Distance from 10% Bottom | [+/- XX%] | [Extreme Oversold / Normal / Elevated] |
| Distance from 40% Top | [+/- XX%] | [Overbought / Normal / Oversold] |

### Trend Direction

- **Ratio Slope**: [Rising / Falling / Flat] - [Brief description of trajectory]
- **Trend Duration**: [X days/weeks] in current [Green/Red] phase
- **Momentum**: [Accelerating / Decelerating / Steady]

## Signal Status

### Recent Trend Transitions

**Most Recent Red-to-Green Transition** (Downtrend to Uptrend):
- Date: [Date]
- Ratio at Transition: [XX%]
- Days Since Transition: [X days]
- Performance Since: [Result if applicable]

**Most Recent Green-to-Red Transition** (Uptrend to Downtrend):
- Date: [Date]
- Ratio at Transition: [XX%]
- Days Since Transition: [X days]
- Performance Since: [Result if applicable]

### Active Signals

**Current Trading Signal**: [ENTER LONG / EXIT LONG / HOLD LONG / STAY FLAT / PREPARE TO ENTER]

[Detailed explanation of why this signal is active]

## Market Condition Assessment

**Current Condition**: [Extreme Oversold / Moderate Bearish / Neutral/Transitional / Moderate Bullish / Extreme Overbought]

### Condition Characteristics

[Detailed description of the current market condition, including:]
- Participation breadth analysis
- Short-term momentum assessment
- Risk/reward considerations at current levels

### Supporting Evidence

1. [First piece of evidence]
2. [Second piece of evidence]
3. [Third piece of evidence]

## Historical Context

### Comparison to Recent Extremes

**Recent Oversold Extremes** (<15%):
- [Date]: [Ratio %] - [Outcome]
- [Date]: [Ratio %] - [Outcome]

**Recent Overbought Extremes** (>35%):
- [Date]: [Ratio %] - [Outcome]
- [Date]: [Ratio %] - [Outcome]

### Typical Behavior at Current Level

[Analysis of how the market typically behaves when the ratio is at the current level]

## Trading Strategy Implications

### Swing Trading Strategy Positioning

**Current Position**: [Long / Flat / Preparing to Enter / Preparing to Exit]

#### Entry Analysis

**Entry Signal Status**: [Active / Not Active / Pending Confirmation]

[If active or pending:]
- **Entry Trigger**: [Red-to-green transition / Oversold reversal / etc.]
- **Confirmation Status**: [Confirmed / Needs X more days / Partial confirmation]
- **Optimal Entry Level**: [Current / Wait for ratio to reach X%]
- **Entry Timing**: [Immediate / Next X days / Already entered]
- **Risk/Reward**: [Assessment of risk/reward at current or pending entry]

[If not active:]
- **What Would Trigger Entry**: [Specific color change or level needed]
- **Current Phase**: [Waiting for oversold / Mid-trend / Overbought]

#### Exit Analysis

**Exit Signal Status**: [Active / Not Active / Monitoring / Tighten Stops]

[If active or monitoring:]
- **Exit Trigger**: [Green-to-red transition / Overbought level / etc.]
- **Exit Timing**: [Immediate / When ratio reaches X% / When color changes]
- **Profit Status**: [Up X% from entry / Down / Flat]

[If not active:]
- **What Would Trigger Exit**: [Specific color change or level needed]
- **Current Phase**: [Early in trend / Mid-trend / Late in trend]

### Position Sizing Recommendations

**Suggested Position Size**: [Full / 75% / 50% / 25% / Minimal / Zero]

**Rationale**: [Explanation based on current ratio level, trend status, and risk/reward]

### Risk Management

**Current Risk Level**: [Low / Moderate / High / Extreme]

**Risk Factors**:
- [Risk factor 1]
- [Risk factor 2]
- [Risk factor 3]

**Stop Loss Level**: [Specific ratio level or condition]

**Profit Target**: [Specific ratio level or condition]

## Key Levels to Monitor

### Critical Thresholds

1. **10% Level (Oversold Bottom)**: [Distance from current, significance]
2. **40% Level (Overbought Top)**: [Distance from current, significance]
3. **[Other Key Level]**: [Description and significance]

### Timing Considerations

- **Short-term** (Next few days): [What to watch for]
- **Swing Trade Horizon** (Next 1-3 weeks): [Expected development]

## Scenario Analysis

### Scenario 1: [Title] - **[XX]% Probability**

**Description**: [What this scenario entails]

**Supporting Factors**:
- [Factor 1]
- [Factor 2]

**Implications**:
- Trading Action: [Enter/Hold/Exit]
- Expected Ratio Movement: [Direction and potential range]
- Timeframe: [Days to weeks]

---

### Scenario 2: [Title] - **[XX]% Probability**

**Description**: [What this scenario entails]

**Supporting Factors**:
- [Factor 1]
- [Factor 2]

**Implications**:
- Trading Action: [Enter/Hold/Exit]
- Expected Ratio Movement: [Direction and potential range]
- Timeframe: [Days to weeks]

---

# Combined Analysis: Strategic & Tactical Integration

[This section is included when both charts are analyzed together]

## Alignment Assessment

### Current Positioning Matrix

| Timeframe | Chart | Status | Signal | Implication |
|-----------|-------|--------|--------|-------------|
| Strategic (Medium/Long) | 200MA Breadth | [Bullish/Bearish/Neutral] | [Buy/Sell/Hold/Wait] | [Brief implication] |
| Tactical (Short-term) | Uptrend Ratio | [Bullish/Bearish/Neutral] | [Enter/Exit/Hold/Wait] | [Brief implication] |

### Scenario Classification

**Current Scenario**: [Scenario 1 / Scenario 2 / Scenario 3 / Scenario 4]

**Scenario 1: Both Bullish**
- Chart 1: [Status]
- Chart 2: [Status]
- Combined Implication: [Maximum bullish / Strategic opportunity]

**Scenario 2: Strategic Bullish, Tactical Bearish**
- Chart 1: [Status]
- Chart 2: [Status]
- Combined Implication: [Hold core, wait for tactical entry]

**Scenario 3: Strategic Bearish, Tactical Bullish**
- Chart 1: [Status]
- Chart 2: [Status]
- Combined Implication: [Short-term trade only, tight stops]

**Scenario 4: Both Bearish**
- Chart 1: [Status]
- Chart 2: [Status]
- Combined Implication: [Defensive positioning]

## Unified Recommendation

### Overall Market Assessment

**Strategic Stance** (3-12+ months): [Bullish / Bearish / Neutral]

**Tactical Stance** (Days to weeks): [Bullish / Bearish / Neutral]

**Conviction Level**: [High / Medium / Low]

### Recommended Actions

**For Long-Term Investors**:
1. [Action 1 based on Chart 1]
2. [Action 2 based on Chart 1]
3. [Action 3 - position sizing]

**For Swing Traders**:
1. [Action 1 based on Chart 2]
2. [Action 2 based on Chart 2]
3. [Action 3 - timing and entry/exit levels]

**For Active Tactical Traders**:
1. [Action 1 combining both charts]
2. [Action 2 - nimble positioning]
3. [Action 3 - risk management]

### Optimal Strategy

**Current Market Environment Best Suited For**: [Strategic positioning / Tactical trading / Both / Neither - stay flat]

[Detailed explanation of why this is the optimal approach given the current breadth readings]

## Risk and Opportunity Matrix

### Primary Opportunities

1. **[Opportunity 1]**: [Description and how to capitalize]
2. **[Opportunity 2]**: [Description and how to capitalize]

### Primary Risks

1. **[Risk 1]**: [Description and how to mitigate]
2. **[Risk 2]**: [Description and how to mitigate]

## Conflicts and Considerations

### Chart Divergences

[If there are conflicts between Chart 1 and Chart 2 signals:]

**Divergence Identified**: [Description of the conflict]

**Resolution**: [How to interpret and act on the divergence]

**Precedence**: [Which chart takes priority in this situation and why]

---

# Summary and Conclusion

## Key Takeaways

1. **[Most Important Finding]**: [Brief explanation]
2. **[Second Most Important Finding]**: [Brief explanation]
3. **[Third Most Important Finding]**: [Brief explanation]

## Action Items

**Immediate Actions** (Now):
- [ ] [Action item 1]
- [ ] [Action item 2]

**Pending Actions** (Contingent on market movement):
- [ ] If [condition], then [action]
- [ ] If [condition], then [action]

## Monitoring Plan

**Daily Monitoring Required**: [Yes / No]

**Key Updates to Watch For**:
1. [Update 1 - e.g., new 8MA trough formation]
2. [Update 2 - e.g., color transition in Chart 2]
3. [Update 3 - e.g., breach of key threshold]

**Next Analysis Recommended**: [Timeframe - daily / every 3 days / weekly]

## Confidence and Limitations

**Analysis Confidence Level**: [High / Medium / Low]

**Reasoning for Confidence Level**: [Explanation]

**Limitations and Caveats**:
- [Limitation 1 - e.g., signals work best in trending markets]
- [Limitation 2 - e.g., external shocks can override technical signals]
- [Limitation 3 - e.g., breadth lags price in fast-moving conditions]

---

## Disclaimer

This analysis is based purely on market breadth technical indicators and does not consider fundamental factors, macroeconomic data, geopolitical events, or other external factors that may influence market behavior. The strategies referenced are based on historical backtesting and may not perform identically in future market conditions. This analysis represents a probabilistic assessment of potential scenarios and is not a guarantee of future performance or a recommendation to buy or sell securities.

All probabilities are estimates based on technical factors and historical patterns, and are subject to change as new data emerges.

---

**End of Breadth Analysis Report**

---

## Appendix: Chart Images

[If chart images are to be included in the report]

### Chart 1: S&P 500 Breadth Index
[Chart image or reference]

### Chart 2: Uptrend Stock Ratio
[Chart image or reference]

### Referencia: references/breadth_chart_methodology.md

# Breadth Chart Analysis Methodology

This reference provides comprehensive methodology for analyzing two types of market breadth charts that provide complementary views of market health and trend status.

## Overview

Market breadth indicators measure the participation of stocks in market moves, providing insights into the strength and sustainability of trends that price indices alone cannot reveal. This skill focuses on two specific breadth measurements:

1. **200MA-Based Breadth Index**: Medium to long-term trend assessment tool
2. **Uptrend Stock Ratio**: Short-term trend and momentum indicator

These two charts work together to provide both strategic (medium/long-term) and tactical (short-term) market perspectives.

---

## Chart 1: S&P 500 Breadth Index (200-Day MA Based)

### Purpose and Use Case

This chart measures the percentage of S&P 500 stocks trading above their 200-day moving average, providing insight into the medium to long-term health of the market. It serves as a strategic positioning tool for determining major market cycles.

### Chart Components

#### Primary Lines

**8-Day Moving Average (8MA) - Orange Line**
- Short-term smoothing of the breadth index
- More responsive to rapid market changes
- Key for identifying reversal points
- Used as the primary signal generator for entries

**200-Day Moving Average (200MA) - Green Line**
- Long-term trend of market breadth
- Slower to respond, filters out noise
- Represents the underlying structural health of the market
- Used as the primary signal generator for exits

#### Reference Levels

**Red Dashed Line (0.73 / 73%)**
- **Average Peak Level**: Historical average of 200MA tops
- **Significance**: When the breadth index exceeds this level, the market is in an overheated state
- **Interpretation**:
  - Above 73%: Market is extremely bullish but approaching exhaustion
  - Significantly above 73%: Elevated risk of correction or consolidation
  - Rarely sustainable for extended periods

**Blue Dashed Line (0.23 / 23%)**
- **Average 8MA Trough Level**: Historical average of 8MA bottoms
- **Significance**: When the 8MA falls below this level, the market is in extreme oversold territory
- **Interpretation**:
  - Below 23%: Severe market stress, capitulation-level selling
  - High probability of reversal and recovery
  - Historically represents excellent buying opportunities
  - Extreme fear and pessimism typically present

#### Signal Markers (Triangles)

**Purple/Magenta Downward Triangles (▼)**
- **8MA Troughs**: Mark the bottoms of the 8-day moving average
- **Significance**: Potential reversal points, especially when near or below the 23% threshold
- **Use**: Primary buy signal when 8MA begins to turn up from a trough

**Blue Downward Triangles (▼)**
- **200MA Troughs**: Mark the bottoms of the 200-day moving average
- **Significance**: Major market cycle lows, extremely rare
- **Use**: Indicates the beginning of a new long-term bull market

**Red Upward Triangles (▲)**
- **200MA Peaks**: Mark the tops of the 200-day moving average
- **Significance**: Major market cycle highs indicating trend exhaustion
- **Use**: Primary sell signal for the tested strategy

#### Background Shading

**Pink Background Regions**
- **Downtrend Periods**: Time periods when the market is in a confirmed downtrend
- **Significance**: Higher risk environment, defensive positioning warranted
- **Use**: Visual aid to identify unfavorable market conditions

### Interpretation Framework

#### Market Regimes

**Healthy Bull Market**
- 8MA and 200MA both rising
- Breadth index between 40% and 73%
- Regular pullbacks to 50-60% range that hold above 8MA
- Wide participation across stocks

**Overheated Bull Market**
- Breadth index persistently above 73%
- 8MA and 200MA both very elevated
- High risk of near-term correction
- Market vulnerable to negative catalysts

**Market Top/Distribution Phase**
- 200MA forming a peak (red ▲)
- 8MA begins to roll over even if 200MA hasn't peaked yet
- Breadth index declining from elevated levels
- Signal to exit long positions

**Bear Market/Correction**
- Both 8MA and 200MA declining
- Pink background shading present
- Breadth index below 50%
- High volatility typical

**Capitulation/Extreme Oversold**
- 8MA below 23% (blue dashed line)
- 8MA forming a trough (purple ▼)
- Maximum pessimism and fear
- Historically excellent buying opportunities

**Early Recovery**
- 8MA turning up from a trough
- 200MA may still be declining (lagging)
- Breadth index beginning to rise from extreme lows
- Initial phase of new uptrend

### Backtested Strategy

Based on historical analysis, the following strategy has demonstrated strong performance:

#### Entry Rules

**BUY Signal**: 8MA Trough Reversal
- Wait for 8MA to form a clear bottom (purple ▼)
- Especially strong when 8MA trough is below 23% (extreme oversold)
- Enter long position in S&P 500 index when 8MA begins to turn upward
- Confirmation: 8MA crosses above previous recent high or shows 2-3 consecutive days of increase

#### Detailed Reversal Confirmation Criteria

**CRITICAL**: Do not enter prematurely. A trough formation alone is NOT sufficient for entry. The reversal must be CONFIRMED.

**Required Steps for Confirmation**:

1. **Trough Identification** (Step 1):
   - 8MA forms a clear bottom marked by purple ▼ triangle
   - Trough level should ideally be below 40%, preferably below 30%
   - Extreme troughs below 23% provide highest probability setups

2. **Initial Reversal** (Step 2):
   - 8MA begins to move upward from the trough
   - First 1-2 periods of increase observed
   - **WARNING**: This is NOT yet a confirmed signal - DO NOT ENTER

3. **Confirmation Period** (Step 3 - MANDATORY):
   - 8MA continues to rise for 2-3 CONSECUTIVE periods after the trough
   - Each period should show clear upward progress (at least 2-5% increase)
   - No significant pullbacks or reversals during confirmation period

4. **Latest Data Verification** (Step 4 - CRITICAL):
   - Analyze the RIGHTMOST 3-5 data points on the chart
   - Verify that the 8MA is CURRENTLY rising (at the latest edge of the chart)
   - Confirm no rollover or downward turn has occurred recently
   - This step prevents entry on failed reversals

5. **Resistance Breakout** (Step 5 - Optional but Ideal):
   - 8MA crosses above 55-60% level
   - This confirms strong breadth improvement
   - Provides higher confidence in sustainability

**Confirmation Status Classification**:

- **CONFIRMED (Green Light)**: Steps 1-4 complete, 8MA rising for 2-3+ consecutive periods and CURRENTLY rising → ENTER
- **DEVELOPING (Yellow Light)**: Steps 1-2 complete, but < 2 consecutive increases → WAIT, MONITOR CLOSELY
- **FAILED (Red Light)**: Steps 1-2 occurred, but 8MA has rolled over and is declining → DO NOT ENTER, signal invalidated
- **NO SIGNAL (Red Light)**: No trough formed → WAIT

**Time-Based Confirmation**:
- Typical confirmation period: 2-4 weeks after trough
- If confirmation takes > 6 weeks, signal strength decreases
- If 8MA fails to reach 55% within 6 weeks of trough, reassess validity

#### Failed Reversal Patterns (WARNING SIGNS)

**What is a Failed Reversal?**

A failed reversal occurs when the 8MA forms a trough and begins to rise, but then rolls over and declines again before reaching sustained momentum. This invalidates the buy signal and often leads to deeper corrections.

**Identifying Failed Reversals**:

1. **Weak Bounce Pattern**:
   - 8MA rises for only 1-2 periods after trough
   - 8MA fails to reach 50-55% level
   - 8MA then turns downward again
   - **Result**: False signal, do NOT enter

2. **Premature Rollover**:
   - 8MA rises to 50-60% range
   - 8MA fails to sustain the rise, begins declining
   - 8MA shows consistent downward trajectory at latest data points
   - **Result**: Reversal failed, exit if already entered or do not enter

3. **Double Bottom Formation**:
   - First trough forms, 8MA rises briefly
   - 8MA declines to form second, lower trough
   - **Result**: First trough was not the final bottom, wait for second trough to confirm

**Failed Reversal Action Protocol**:
- Immediately classify signal as INVALID
- Do NOT enter position
- Wait for 8MA to form a NEW, LOWER trough (often below 23%)
- Reset analysis and wait for fresh confirmation from the new trough

**Historical Failed Reversal Examples** (refer to chart):
- Failed reversals are less common but occur during severe corrections
- They typically precede deeper declines to extreme oversold (<23%)
- After failed reversal, the eventual confirmed reversal from lower levels often provides excellent entries

#### Latest Data Point Analysis Protocol

**Why Latest Data Points Matter Most**:

The most recent 3-5 data points on the chart (rightmost edge) represent the CURRENT market condition. Historical movement is context, but the latest trajectory determines whether a signal is active, developing, or failed.

**Protocol**:

1. **Always Start with the Rightmost Data Point**:
   - This is the absolute latest reading
   - This determines the CURRENT slope of the 8MA

2. **Trace Backward 3-5 Data Points**:
   - Compare current level to 1 week ago
   - Compare current level to 2 weeks ago
   - Compare current level to 3 weeks ago
   - Determine if the trend is: Rising, Falling, or Flat

3. **Calculate Consecutive Periods**:
   - Count how many consecutive periods 8MA has risen
   - Count how many consecutive periods 8MA has fallen
   - **Confirmation requires 2-3 consecutive UP periods**
   - **1-2 consecutive DOWN periods after a trough = failed reversal warning**

4. **Visual Slope Assessment**:
   - Visually trace the 8MA line at the rightmost edge
   - Is the line sloping UP, DOWN, or FLAT?
   - Do NOT rely on earlier parts of the chart - focus on the edge

**Example Analysis**:

```
Scenario: 8MA formed trough at 30% three weeks ago

Week-by-Week Analysis (from trough to present):
- Week 1 after trough: 30% → 40% (UP 10%)
- Week 2 after trough: 40% → 52% (UP 12%)
- Week 3 after trough: 52% → 48% (DOWN 4%)

Current Slope: FALLING
Consecutive Increases: 0 (last period was DOWN)
Status: FAILED REVERSAL - 8MA rolled over after initial bounce

Action: DO NOT ENTER. Signal is invalid. Wait for new trough formation.
```

```
Scenario: 8MA formed trough at 25% four weeks ago

Week-by-Week Analysis (from trough to present):
- Week 1 after trough: 25% → 35% (UP 10%)
- Week 2 after trough: 35% → 45% (UP 10%)
- Week 3 after trough: 45% → 55% (UP 10%)
- Week 4 after trough: 55% → 60% (UP 5%)

Current Slope: RISING
Consecutive Increases: 4 (all periods UP)
Status: CONFIRMED - Strong sustained reversal

Action: ENTER LONG. Signal is confirmed and robust.
```

#### Exit Rules

**SELL Signal**: 200MA Peak Detection
- Exit long position when 200MA forms a peak (red ▲)
- 200MA peaks typically occur when breadth index is near or above 73%
- Do not wait for 200MA to turn down; exit at or near the peak
- This signals the end of the bull market phase

#### Risk Management

- **Stop Loss**: Consider exiting if 8MA breaks decisively below its most recent trough
- **Partial Profits**: Consider taking partial profits when breadth index exceeds 73% (overheated)
- **Re-entry**: Do not re-enter during the same cycle unless a new 8MA trough forms

#### Strategy Performance Characteristics

- **Win Rate**: Historically high due to buying extreme oversold and selling into strength
- **Hold Period**: Typically several months to over a year
- **Drawdown Management**: Strategy avoids holding through major bear markets
- **False Signals**: Rare due to the significant smoothing of the indicators

### Analysis Checklist

When analyzing this chart, systematically evaluate:

1. ✓ **Current 8MA Level**: Where is the 8MA relative to historical troughs and the 23% threshold?
2. ✓ **Current 200MA Level**: Where is the 200MA relative to historical peaks and the 73% threshold?
3. ✓ **8MA Slope**: Is the 8MA rising, falling, or flat?
4. ✓ **200MA Slope**: Is the 200MA rising, falling, or flat?
5. ✓ **Recent Signal Markers**: Any recent triangles indicating troughs or peaks?
6. ✓ **Market Regime**: Which regime best describes the current state?
7. ✓ **Strategy Position**: Based on the backtested strategy, should one be long, flat, or preparing to enter/exit?
8. ✓ **Distance from Thresholds**: How close is the breadth index to key levels (23%, 73%)?

---

## Chart 2: US Stock Market - Uptrend Stock Ratio

### Purpose and Use Case

This chart measures the percentage of stocks in confirmed uptrends across the US stock market, providing a real-time view of market momentum and participation. It serves as a tactical tool for short-term swing trading and confirming the strength of market moves.

### Definition of "Uptrend Stock"

A stock is classified as being in an uptrend when it meets ALL of the following criteria:

1. **Price above 200-day MA**: Stock is in a long-term uptrend
2. **Price above 50-day MA**: Stock is in an intermediate-term uptrend
3. **Price above 20-day MA**: Stock is in a short-term uptrend
4. **Positive 1-month performance**: Stock has gained value over the past month

This multi-factor definition ensures that only stocks with confirmed momentum across multiple timeframes are counted as "uptrend stocks."

### Chart Components

#### Primary Visualization

**Color-Coded Trend Identification**

**Green Regions**
- Represent periods when the market is in an **uptrend**
- Uptrend stock ratio is generally rising
- Positive market momentum
- Favorable environment for long positions

**Red Regions**
- Represent periods when the market is in a **downtrend**
- Uptrend stock ratio is generally falling
- Negative market momentum
- Unfavorable for long positions, defensive posture appropriate

**Color Transitions**
- **Red-to-Green Transition**: Downtrend ending, uptrend beginning (BUY signal)
- **Green-to-Red Transition**: Uptrend ending, downtrend beginning (SELL signal)

#### Reference Levels

**Lower Orange Dashed Line (~10%)**
- **Short-Term Market Bottom**: When the uptrend ratio falls to approximately 10%
- **Significance**: Extreme oversold condition
- **Interpretation**:
  - Below 10%: Maximum bearish sentiment, capitulation phase
  - High probability of near-term reversal
  - Short-term bottom often forms at this level
  - Excellent risk/reward for initiating long positions

**Upper Orange Dashed Line (~37-40%)**
- **Short-Term Market Top**: When the uptrend ratio approaches approximately 40%
- **Significance**: Overbought condition, market overheating
- **Interpretation**:
  - Near 40%: Market is short-term overbought
  - High probability of pullback or consolidation
  - Reversal often begins at this level
  - Consider taking profits or tightening stops on long positions

### Interpretation Framework

#### Market Conditions

**Extreme Oversold (Ratio < 10%)**
- Very few stocks participating in uptrend
- Market-wide selling pressure
- High fear and pessimism
- Contrarian buying opportunity
- Often coincides with VIX spikes
- Watch for red-to-green transition

**Moderate Bearish (Ratio 10-20%)**
- Below-average market participation
- Downtrend still in effect (red)
- Selective stock strength only
- Wait for confirmation before entering

**Neutral/Transitional (Ratio 20-30%)**
- Average market participation
- Can be either early uptrend or late downtrend
- Color (green vs red) is critical for context
- Watch for trend changes

**Moderate Bullish (Ratio 30-37%)**
- Healthy uptrend participation
- Green color dominant
- Sustainable momentum
- Favorable for long positions

**Extreme Overbought (Ratio > 37-40%)**
- Very high participation in uptrend
- Market short-term overheated
- Vulnerable to pullback
- Watch for green-to-red transition
- Consider profit-taking

#### Trend Transitions

**Red-to-Green (Downtrend to Uptrend)**
- **Entry Signal**: Marks the beginning of a new uptrend phase
- **Characteristics**:
  - Uptrend ratio bottoms and begins to rise
  - Often occurs from extreme oversold levels (<10-15%)
  - Increasing number of stocks breaking above MAs
  - Momentum shifting from bearish to bullish
- **Action**: Initiate long positions in index or strong individual stocks

**Green-to-Red (Uptrend to Downtrend)**
- **Exit Signal**: Marks the end of an uptrend phase
- **Characteristics**:
  - Uptrend ratio peaks and begins to fall
  - Often occurs from overbought levels (>35-40%)
  - Stocks breaking below key moving averages
  - Momentum shifting from bullish to bearish
- **Action**: Exit long positions, move to cash or defensive positions

### Trading Strategy

#### Short-Term Swing Trading Strategy

**Entry Rules**

1. **Wait for Oversold Condition**:
   - Uptrend ratio declines to 10-15% range
   - Market in red (downtrend) phase

2. **Identify Trend Reversal**:
   - Color changes from red to green
   - Uptrend ratio begins to rise from lows
   - Confirmation: 2-3 consecutive increases in the ratio

3. **Enter Long Position**:
   - Buy S&P 500 index (SPY, ES futures) or basket of leading stocks
   - Position size based on risk tolerance

**Exit Rules**

1. **Watch for Overbought Condition**:
   - Uptrend ratio approaches 37-40% level
   - Market has been green for extended period

2. **Identify Trend Exhaustion**:
   - Color changes from green to red
   - Uptrend ratio begins to fall from highs
   - Momentum waning

3. **Exit Long Position**:
   - Sell index position
   - Move to cash or defensive assets

**Risk Management**

- **Stop Loss**: Exit if uptrend ratio breaks below recent lows while still in supposed uptrend
- **Partial Exits**: Consider scaling out as ratio approaches 35-37%
- **Position Sizing**: Larger positions when entering from extreme oversold (<10%), smaller when entering from moderate levels
- **False Signals**: Quick reversals (red-green-red or green-red-green within days) may be false; wait for confirmation

#### Strategy Performance Characteristics

- **Timeframe**: Days to weeks (swing trading)
- **Win Rate**: Moderate to high, depending on confirmation criteria
- **Hold Period**: Typically 1-4 weeks
- **Best Performance**: When entries align with extreme oversold conditions (<10%)
- **Risk**: Whipsaws during choppy, trendless markets

### Combining Both Charts

For optimal decision-making, use both breadth charts together:

#### Strategic Positioning (Chart 1: 200MA Breadth)

- Determines overall market regime (bull, bear, neutral)
- Guides strategic asset allocation
- Identifies major entry/exit points for core positions
- Longer holding periods (months to year+)

#### Tactical Positioning (Chart 2: Uptrend Ratio)

- Determines short-term momentum and timing
- Guides tactical trades and position sizing
- Identifies short-term entry/exit points for swing trades
- Shorter holding periods (days to weeks)

#### Alignment Scenarios

**Scenario 1: Both Bullish**
- Chart 1: 8MA rising, 200MA rising or flat, breadth < 73%
- Chart 2: Green (uptrend), ratio rising from oversold
- **Action**: Maximum bullish stance, aggressive long positioning

**Scenario 2: Strategic Bullish, Tactical Bearish**
- Chart 1: 8MA rising, 200MA not yet peaked
- Chart 2: Red (downtrend), ratio elevated or falling
- **Action**: Hold core long positions, avoid new tactical longs, wait for oversold

**Scenario 3: Strategic Bearish, Tactical Bullish**
- Chart 1: 200MA peaked or declining
- Chart 2: Green (uptrend), ratio rising from extreme oversold
- **Action**: Short-term tactical longs only, tight stops, prepare for strategic exit

**Scenario 4: Both Bearish**
- Chart 1: Both MAs declining, pink background
- Chart 2: Red (downtrend), ratio falling
- **Action**: Defensive positioning, cash or short positions, wait for 8MA trough

### Analysis Checklist for Chart 2

When analyzing the uptrend stock ratio chart, systematically evaluate:

1. ✓ **Current Ratio Level**: What is the current uptrend stock percentage?
2. ✓ **Current Color**: Is the market in green (uptrend) or red (downtrend)?
3. ✓ **Proximity to Thresholds**: How close is the ratio to 10% (bottom) or 40% (top)?
4. ✓ **Trend Direction**: Is the ratio rising, falling, or flat?
5. ✓ **Recent Transitions**: Any recent color changes from red-to-green or green-to-red?
6. ✓ **Duration of Current Trend**: How long has the current color phase lasted?
7. ✓ **Strategy Position**: Based on the swing trading strategy, should one be long, flat, or preparing to enter/exit?
8. ✓ **Historical Context**: How does the current reading compare to recent extremes?

---

## Output Requirements

### Language and Style

- **Analysis Language**: Conduct all thinking and analysis in English
- **Output Format**: Generate all reports in English using markdown format
- **Tone**: Professional, objective, analytical
- **Terminology**: Use precise technical terms consistently

### Analysis Structure

Each breadth chart analysis report should include:

1. **Current Readings**: Specific values for all key metrics
2. **Signal Status**: Clear identification of any active signals (troughs, peaks, transitions)
3. **Market Regime Assessment**: Classification of the current market environment
4. **Strategy Implications**: Specific positioning recommendations based on the backtested strategies
5. **Key Levels to Watch**: Upcoming thresholds or levels that would change the analysis
6. **Risk Considerations**: Potential invalidation scenarios or alternative interpretations
7. **Combined Analysis** (when both charts analyzed): Integration of strategic and tactical perspectives

### Objectivity Standards

- Base all analysis strictly on observable chart data
- Avoid incorporating external information (news, fundamentals) unless specifically relevant to breadth interpretation
- Clearly distinguish between factual observations and probabilistic forecasts
- Acknowledge uncertainty when signals are ambiguous
- Present both bullish and bearish scenarios when appropriate

---

## Common Pitfalls to Avoid

### Chart 1 (200MA Breadth) Pitfalls

- **Misreading Recent Trend Direction** (MOST COMMON ERROR): Analyzing historical chart movement instead of focusing on the LATEST 3-5 data points at the rightmost edge. This leads to stating "8MA is rising" when it's actually falling at the current edge, or vice versa. ALWAYS analyze the rightmost data points to determine CURRENT slope.

- **Premature Entry**: Buying before clear 8MA reversal is confirmed (2-3 consecutive periods of increase). Entering on just a trough formation without confirmation often results in losses from failed reversals.

- **Ignoring Failed Reversals**: Not recognizing when an 8MA has rolled over after an initial bounce from a trough. If the 8MA rises briefly then turns down again, the signal is INVALID.

- **Late Exit**: Waiting for 200MA to decline instead of exiting at the peak formation. The peak itself is the sell signal - do not wait for confirmation of decline.

- **Ignoring Thresholds**: Not recognizing significance of 23% and 73% levels. These thresholds provide critical context for entry and exit timing.

- **Overtrading**: Trying to trade every wiggle in the 8MA instead of waiting for clear, confirmed trough reversals. Patience is essential for this strategy.

### Chart 2 (Uptrend Ratio) Pitfalls

- **Chasing**: Entering after the ratio has already risen substantially from oversold
- **Ignoring Color**: Focusing only on the ratio level without considering trend direction (color)
- **False Breakouts**: Not waiting for confirmation of color transitions
- **Missing Extremes**: Not recognizing when the ratio reaches <10% or >40%

### General Pitfalls

- **Analyzing in Isolation**: Using only one chart without considering the other
- **Over-Complicating**: Adding too many additional indicators that cloud the core signals
- **Recency Bias**: Giving too much weight to the most recent move
- **Ignoring Historical Context**: Not comparing current readings to historical patterns shown on the charts


---

## SKILL: calendar

- Fuente: `staskh/trading_skills` → `.claude/skills/calendar` (MIT)
- Cuándo usarla: Report scheduled US economic events (CPI, NFP, FOMC, GDP, PCE, ISM, jobless claims...) with times in ET, impact, actual/consensus/previous. Use when user asks about the economic calendar, macro events, what data comes out today/this week, or release times. Optional ForexFactory cross-check for the current week.
- Código: extraer `code/staskh_trading_skills.tar` y usar `.claude/skills/calendar/` (events.py)

# Economic Calendar

Scheduled US economic releases per weekday, from Nasdaq's public economic-events feed
(through `trading_skills.calendar_nasdaq`, which corrects the feed's day offset and
verifies each day against weekly releases with a fixed weekday).

## Instructions

> **Note:** If `uv` is not installed or `pyproject.toml` is not found, replace `uv run python` with `python` in all commands below.

```bash
uv run python scripts/events.py [--date YYYY-MM-DD] [--days N] [--impact all|high] [--forexfactory]
```

## Arguments

- `--date` - First day, YYYY-MM-DD (default: today ET). A weekend rolls to Monday.
- `--days` - Number of weekdays to report (default: 1). Weekends are skipped.
- `--impact` - `all` (default) or `high` (FOMC, CPI, PPI, PCE, NFP, unemployment, GDP, retail sales, ISM, Fed-chair remarks).
- `--forexfactory` - Also fetch ForexFactory's calendar, cross-check each day, and fill Nasdaq's gaps: high/medium releases Nasdaq lacks are added to `events`, and a day Nasdaq can't serve is taken wholly from ForexFactory. ForexFactory publishes **only the current Sun–Sat week**; other days report `available: false`. The feed rate-limits to about one request per 5 minutes, so the week is cached in the system temp dir for an hour (an older copy is used if a fetch fails).

## Output

- `generated_at`, `data_delay`, `source` (`"nasdaq"`)
- `days` - one entry per weekday:
  - `date`, `weekday`
  - `verified` - true when the day's contents matched the requested weekday; false means use with care
  - `times_verified` - true when Nasdaq's times were converted to ET using a clock measured from fixed-time releases (claims/NFP/CPI 8:30, ISM/JOLTS/Michigan 10:00) on that day or a nearby Thursday in the same daylight/standard period; false means times assume Nasdaq's usual UTC−4 clock — confirm them
  - `feed_date` - the Nasdaq `date` parameter whose rows were used
  - `events` - list of `{event, time_et, impact, actual, consensus, previous, source}`, high-impact first. `source` is `"nasdaq"` or `"forexfactory"` (gap-filled; no `actual`, ForexFactory's own impact rating). `null` when no source can serve the day (`note` says to verify manually — never read null as a quiet day)
  - `forexfactory` (with `--forexfactory`) - `{available, events, cross_check}` or `{available: false, note}`
    - `cross_check.confirmed` - same release at the same time in both sources
    - `cross_check.time_mismatch` - same release, different time (check which time is right)
    - `cross_check.missing_in_nasdaq` - high/medium ForexFactory release Nasdaq lacks
    - `cross_check.nasdaq_only` - high-impact Nasdaq release ForexFactory lacks

## Examples

```bash
# Today
uv run python scripts/events.py

# Yesterday and today, high impact only, cross-checked
uv run python scripts/events.py --date 2026-10-29 --days 2 --impact high --forexfactory

# Next week
uv run python scripts/events.py --date 2026-11-02 --days 5 --impact high
```

Only this report uses ForexFactory.

## Reporting

Group by day; lead with high-impact releases and their ET times. Flag any day with
`events: null` or `verified: false`, mark ForexFactory-sourced events, and list every
`time_mismatch` / `missing_in_nasdaq` from the cross-check. FOMC decision days come from a hardcoded schedule and are
always included.

## Dependencies

- `requests`

## Timezone

All timestamps and time-based calculations must use the `America/New_York` timezone. All JSON output must include `generated_at` (NY time string) and `data_delay` fields.


---

## SKILL: compliance-calendar

- Fuente: `SYasJ/claude-business-skills` → `plugins/risk/skills/compliance-calendar` (MIT)
- Cuándo usarla: Build a calendar of obligations the organization already knows it has, with owners and lead time. Use when the user mentions compliance calendar, obligations calendar, filing calendar, compliance dates, or asks for a compliance calendar. Risk and compliance skill by Yasir Jilani.

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'compliance-calendar' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Compliance Calendar

Build a calendar of obligations the organization already knows it has, with owners and lead time.

## When to use this skill

Use this skill when the user:

- compliance calendar
- obligations calendar
- filing calendar
- compliance dates

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

- Known obligations
- Owners
- External dates they have confirmed
- Last year's misses

## Workflow


### 1. Step 1

Record only obligations they confirmed. Do not invent a filing.
### 2. Step 2

Mark unconfirmed dates as unconfirmed.
### 3. Step 3

Put an internal due date earlier than the external one so review can happen.
### 4. Step 4

Assign an owner and a reviewer.
### 5. Step 5

Note evidence saved when the obligation is met.
### 6. Step 6

Send new-jurisdiction questions to counsel rather than answering them from memory.

## Output

Deliver a **compliance calendar**.

- Purpose of this compliance calendar, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a compliance calendar by 30 September 2026. A team wants every possible global filing listed just in case.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A team wants every possible global filing listed just in case.

Known obligations: Vendor Redline Parts. Stated in the ask, not documented anywhere else
Owners: Priya Shah, controller
External dates they have confirmed: 30 September 2026
Last year's misses: Issue log item 18, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Compliance calendar**
Northline Studio · 14 September 2026 · Due 30 September 2026

**Decision**
A calendar of confirmed obligations, with unknowns flagged for counsel instead of invented.

**Checklist**

- [x] **Known obligations** — Vendor Redline Parts. Stated in the ask, not documented anywhere else  
      Evidenced in the file
- [x] **Owners** — Priya Shah, controller  
      Evidenced in the file
- [x] **External dates they have confirmed** — 30 September 2026  
      Evidenced in the file
- [ ] **Last year's misses** — Issue log item 18, last reviewed 14 September 2026. No owner named since  
      Open — nothing in the file closes this

**The gates this list enforces, in order**

1. Record only obligations they confirmed. Do not invent a filing
2. Mark unconfirmed dates as unconfirmed
3. Put an internal due date earlier than the external one so review can happen
4. Assign an owner and a reviewer
5. Note evidence saved when the obligation is met

**Deliberately not done**
- Invented deadlines.
- A calendar with no owners.
- Dates stored with portal passwords.

**Stop rule**
Do not mark this pack complete while a box above is open. An open box is a finding, not a formality — it is the thing this checklist exists to catch.

Next: Priya Shah closes the open items before 30 September 2026.

## Anti-patterns

- Invented deadlines
- A calendar with no owners
- Dates stored with portal passwords

## Related skills

- `tax-calendar`
- `regulatory-change-log`


---

## SKILL: cot-contrarian-detector

- Fuente: `tradermonty/claude-trading-skills` → `skills/cot-contrarian-detector` (MIT)
- Cuándo usarla: Detect crowded speculative positioning in CFTC futures markets (COT report analysis) to find contrarian setups using Jason Shapiro's methodology. Screens large-speculator ("non-commercial") net positioning across 65 futures markets (indices, rates, FX, metals, energy, crypto) via the FMP Commitment of Traders API, computes a 3-year and 26-week COT Index per market, and classifies extremes as CROWDED_LONG / CROWDED_SHORT. Use when the user asks about COT report analysis, crowded positioning, "who is trapped", speculative positioning extremes, contrarian futures setups, or wants to run Jason Shapiro-style analysis. This skill automates crowding DETECTION only (step 1 of 5) — it does not generate trade signals by itself.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/cot-contrarian-detector/` (requirements.txt, cot_index.py, fmp_client.py, screen_cot_crowding.py)

# COT Contrarian Detector

## Overview

Implements step 1 of Jason Shapiro's COT (Commitment of Traders) contrarian
process: detect when large speculators are crowded into one side of a futures
market. Crowded positioning is a *precondition* for a contrarian trade, not a
trade signal — a market only becomes tradable once crowding is confirmed by a
news failure and price-action reversal (steps 2-3), which this skill guides
the user through manually.

**Core thesis (Shapiro):** Large speculators (hedge funds, CTAs, momentum
traders) tend to be maximally positioned at trend exhaustion, not trend
inception. When they are already crowded onto one side, the next big move is
statistically more likely to run them over than to reward them further. Fade
the *speculators*, not the commercials (commercials hedge for structural
reasons and are not a crowd-psychology signal).

## When to Use This Skill

**English:**
- "What markets are the speculators crowded into right now?"
- "Run a COT report analysis" / "Show me COT positioning extremes"
- "Is anyone 'trapped' in gold / the dollar / bonds right now?"
- User wants to find contrarian futures setups
- User asks for a Jason Shapiro-style COT screen

**Japanese:**
- 「COTレポートで買われすぎ・売られすぎのポジションを調べて」
- 「投機筋が偏っている市場は？」
- 「ジェイソン・シャピロ式の逆張り分析をして」

**Do NOT use when:**
- The user wants a trade signal right now — crowding alone is not
  actionable; see Guardrails below
- The user is asking about individual equities — COT reports cover CFTC
  futures markets only (indices, rates, FX, metals, energy, agri, crypto),
  not single stocks

## Prerequisites

- **FMP API Key:** Required. Set `FMP_API_KEY` environment variable or pass
  `--api-key`. **COT endpoints require an FMP Premium+ plan** — a free-tier
  key will not have access.
- **Python 3.9+** with `requests` installed.
- **API Budget:** One call per market (23 for `--core`, up to ~65 for the
  full universe), plus one call for the market list when neither `--symbols`
  nor `--core` is given.

## Workflow

### Phase 1: Run the crowding screen

```bash
# Curated core futures universe (23 liquid/representative markets)
python3 skills/cot-contrarian-detector/scripts/screen_cot_crowding.py --core --output-dir reports/

# Explicit symbols
python3 skills/cot-contrarian-detector/scripts/screen_cot_crowding.py --symbols "ES,GC,CL" --output-dir reports/

# Full universe (all ~65 markets FMP's COT list covers)
python3 skills/cot-contrarian-detector/scripts/screen_cot_crowding.py --output-dir reports/
```

The script fetches each market's weekly legacy COT report (large-speculator
long/short positions), computes a 156-week (3-year) and 26-week COT Index per
market, and classifies extremes:

- `CROWDED_LONG` — COT Index >= 90 (near the 3-year net-long high)
- `CROWDED_SHORT` — COT Index <= 10 (near the 3-year net-short high)
- `NEUTRAL` — everything in between

Markets with insufficient history to compute the index are never silently
dropped — they appear in a `skipped` list with the reason (e.g. "insufficient
history: 40/156 weeks").

### Phase 2: Present the crowding report

Present the generated Markdown report, highlighting:
- Which markets are `CROWDED_LONG` / `CROWDED_SHORT` and by how much
- The 26-week index for context (is the crowding fresh or aging?)
- Week-over-week net-position swings (fast-moving crowds are more fragile)
- The methodology note and disclaimer — crowding is not a trade signal

### Phase 3: Guide steps 2-5 manually (Shapiro process)

For any `CROWDED_LONG` / `CROWDED_SHORT` market the user wants to pursue,
load `references/shapiro-methodology.md` and walk through the remaining
steps — these are **not automated**:

1. ~~Crowding detection~~ (done — this skill)
2. **News failure** — use WebSearch to check whether recent news favorable to
   the crowd's direction failed to move price the way the crowd would expect
   (e.g. crowded-long market doesn't rally on bullish news). This is the core
   edge and the most important manual confirmation.
3. **Price-action confirmation** — check the weekly chart for a reversal
   pattern or a failure at a new high/low.
4. **Entry** — against the crowd, with a stop at the recent swing extreme and
   small, fixed-risk sizing (see `position-sizer` skill).
5. **Exit** — when positioning normalizes toward neutral (COT Index back
   toward 50) or the stop is hit.

Never recommend an entry from crowding alone — steps 2 and 3 must both
confirm first.

## Output

- **JSON:** `reports/cot_crowding_<as-of-date>.json` — machine-readable, with
  a `run_context` block (schema_version, params, universe, data_date) plus
  `markets` (ranked results) and `skipped` (never silently dropped).
- **Markdown:** `reports/cot_crowding_<as-of-date>.md` — human-readable
  report with Crowded Long / Crowded Short / Full Ranking / Week-over-Week
  Swings / Skipped Markets / Methodology sections.

## Cadence

CFTC publishes the COT report **Fridays ~3:30pm ET**, with positions as of
the **prior Tuesday** — data is always 3+ days old by the time it's
published, and up to 9 days old by the following Friday. Run this skill:
- **Weekly**, after Friday's publication or over the weekend, for a fresh
  read
- **Ad hoc**, when the user asks about a specific market's positioning —
  the underlying data will be from the most recent Friday release either way

## Guardrails

- **Crowdedness alone is NOT a trade signal.** It is a precondition. Never
  suggest an entry without steps 2 (news failure) and 3 (price action) from
  `references/shapiro-methodology.md` also confirming.
- **Data is lagged.** COT positions are 3-9 days old by the time they're
  read; do not treat them as a real-time signal.
- **Fade speculators, not commercials.** This skill only looks at
  non-commercial ("large speculator") positioning — commercial hedging flows
  are structurally different and not a crowd-psychology signal.
- **Not investment advice.** All output is for research/educational purposes.

## Resources

### `references/shapiro-methodology.md`
The full 5-step process (crowding → news failure → price action → entry →
exit), why speculators (not commercials) are the fade target, the 3-day
publication lag caveat, and a table of what this skill automates vs. what
stays manual. Load this whenever guiding a user past step 1.

### `references/cot-index-calculation.md`
The COT Index formula, lookback rationale (156w primary / 26w context),
extreme threshold sensitivity, open-interest normalization rationale, the
legacy-vs-disaggregated report distinction (this skill uses the legacy
report's non-commercial = large-speculator fields), and a glossary of the FMP
COT API field names consumed by `scripts/cot_index.py`.

Vendored client: `scripts/fmp_client.py` (generated) owns FMP transport — rate limiting, single 429 retry, header auth (the key never appears in a URL), and apikey redaction on `(data, error)` results (Issue #495).

### When to Load References
- **First use / explaining the methodology:** Load
  `references/shapiro-methodology.md`
- **Explaining a specific number in the report:** Load
  `references/cot-index-calculation.md`
- **Regular execution:** References not needed — the script handles the
  crowding computation

### Referencia: references/cot-index-calculation.md

# COT Index Calculation

## Formula

```
COT Index = (current_net - window_min) / (window_max - window_min) * 100
```

Where `current_net` is the most recent week's large-speculator net position
(non-commercial long minus non-commercial short), and `window_min` /
`window_max` are the minimum and maximum net position observed over the
lookback window (including the current week).

- **100** = current net position is the highest (most net-long) of the
  lookback window
- **0** = current net position is the lowest (most net-short) of the
  lookback window
- **50** = current net position sits at the midpoint of the window's range

This is the standard "Stochastics of positioning" formulation used across COT
index literature (crowdedmarketreport.com, various CFTC-data commentary
sites) — it is mathematically identical to a %K stochastic applied to net
position instead of price.

**Undefined cases:** the index is `None` (not zero, not fifty) when:
- Fewer than `lookback_weeks` of history are available — there is nothing
  meaningful to compare "current" against
- `window_max == window_min` — every week in the window had the *identical*
  net position, so the range is zero and the division is undefined

Both cases are treated identically by `cot_index.compute_cot_index()`: return
`None` rather than raising, so callers can decide how to surface "no data"
(this skill's screener puts such markets in a `skipped` list with a reason,
never silently drops them or reports a misleading 50).

## Lookback Windows

This skill computes two indices per market:

- **Primary: 156 weeks (~3 years), default `--lookback-weeks`.** The
  conventional COT-index lookback — long enough to span multiple full
  positioning cycles (a market can stay "crowded" for months at a time), short
  enough to stay relevant to the current volatility/rate regime. This is the
  index used for the CROWDED_LONG/CROWDED_SHORT classification.
- **Short: 26 weeks (~6 months), default `--short-lookback-weeks`.** Context
  only — shown alongside the 3-year index so the user can tell whether an
  extreme is *fresh* (also extreme on the 26-week window) or *aging* (was
  more extreme weeks ago and has already started to normalize). A market that
  is CROWDED_LONG on both windows is a stronger, more current signal than one
  that is CROWDED_LONG only on the 3-year window because it peaked months ago.

Both lookbacks are CLI flags (`--lookback-weeks`, `--short-lookback-weeks`)
so the user can adjust for a specific market's cycle length if needed.

## Extreme Thresholds

Default thresholds: **high >= 90**, **low <= 10** (`--threshold-high`,
`--threshold-low`). These are inclusive boundaries — a market at exactly 90.0
classifies as `CROWDED_LONG`.

**Sensitivity note:** 90/10 is a conservative, "clearly extreme" threshold
that will flag fewer markets but with higher conviction. Loosening to 80/20
roughly doubles the number of markets flagged in a typical universe scan but
increases false positives — markets that are "elevated" rather than
"crowded." There is no universally correct threshold; 90/10 is the
conventional starting point in COT-index commentary and matches
crowdedmarketreport.com's public framework. Tighten toward 95/5 for
higher-conviction, fewer signals; loosen toward 80/20 for an earlier,
noisier read.

## Open Interest Normalization

`compute_oi_normalized_net()` expresses net position as a fraction of total
open interest (`net_position / openInterestAll`). This exists because raw net
position isn't comparable across markets of very different sizes — a net
position of -50,000 contracts is trivial in a 2,000,000-contract-OI market
(ES) but enormous in a 100,000-contract-OI market. Normalizing by OI gives a
rough cross-market comparability check; it is *not* used in the
CROWDED_LONG/SHORT classification itself (which is purely about the market's
own historical range via the COT Index), but is surfaced in reports as
additional context.

Returns `None` when open interest is zero, missing, or non-numeric — a
division by an unreliable denominator should never silently produce a
misleading ratio.

## Legacy vs. Disaggregated Report

The CFTC publishes COT data in two formats:

- **Legacy report** (used by this skill): three trader categories —
  Non-Commercial (large speculators), Commercial (hedgers), and
  Non-Reportable (small traders below reporting thresholds). This is the
  original, longest-running COT format and matches Shapiro's own framework of
  fading the speculative crowd.
- **Disaggregated report** (not used): splits traders into four finer
  categories (Producer/Merchant, Swap Dealers, Managed Money, Other
  Reportables) for physical-commodity futures only (not financials). More
  granular but not available for financial futures (equity indices, rates,
  FX) and not what Shapiro's methodology is built around.

This skill exclusively uses the legacy report's non-commercial long/short
fields (`noncommPositionsLongAll` / `noncommPositionsShortAll`) as the
"large speculator" proxy across all 65 markets FMP's COT API covers, so the
same methodology applies uniformly to indices, rates, FX, metals, energy,
agri, and crypto futures.

## FMP API Field Glossary

Field names as returned by `stable/commitment-of-traders-report` (verified
live against the FMP API, 2026-07). All fields below are on a single weekly
report row, one row per market per Tuesday-dated report.

| Field | Meaning |
|---|---|
| `date` | Report date, format `"YYYY-MM-DD 00:00:00"`; positions as of the Tuesday of that week |
| `sector` | Market category, e.g. `"INDICES"`, `"CURRENCIES"`, `"METALS"` |
| `name` | Human-readable market name, e.g. `"S&P 500 E-Mini (ES)"` |
| `contractUnits` | Contract size/unit description, e.g. `"($50 X S&P 500 INDEX)"` |
| `openInterestAll` | Total open interest across all trader categories |
| `noncommPositionsLongAll` | Large-speculator ("non-commercial") long contracts — used as the "large speculator" proxy in `compute_net_position()` |
| `noncommPositionsShortAll` | Large-speculator short contracts |
| `noncommPositionsSpreadAll` | Large-speculator spread contracts (not used — spreads are market-neutral by construction) |
| `commPositionsLongAll` / `commPositionsShortAll` | Commercial (hedger) long/short — not used; see "Why speculators, not commercials" in `shapiro-methodology.md` |
| `nonreptPositionsLongAll` / `nonreptPositionsShortAll` | Non-reportable (small trader) long/short — not used |
| `changeInNoncommLongAll` / `changeInNoncommShortAll` | Week-over-week change in speculator long/short (FMP-computed; this skill computes its own week-over-week net change from the raw series instead, via `compute_week_over_week_change()`, to stay self-consistent with the net-position series used everywhere else) |
| `pctOfOiNoncommLongAll` / `pctOfOiNoncommShortAll` | Speculator long/short as % of open interest — surfaced directly in reports as participation context |
| `tradersNoncommLongAll` / `tradersNoncommShortAll` | Number of distinct large-speculator traders holding long/short — surfaced as participation-breadth context (see "Participation and Open Interest Context" in `shapiro-methodology.md`) |
| `concNetLe4TdrLongAll` / `concNetLe4TdrShortAll` | % of net long/short position held by the largest 4 traders — a concentration signal (not currently used in classification, available for future extension) |

## Handling Data Gaps

`sort_dedupe_rows()` sorts rows ascending by `date` and, when two rows share
the same date (observed occasionally with re-published/corrected reports),
keeps the *last* one in the input order — treated as the more recently
fetched/corrected value. Rows missing a `date` are dropped rather than kept
in an arbitrary position, since an undated row can't be placed in the
lookback window correctly.

### Referencia: references/shapiro-methodology.md

# Jason Shapiro's COT Contrarian Methodology

## Overview

Jason Shapiro is a discretionary futures trader whose approach is documented
in Jack Schwager's *Unknown Market Wizards* (2020), Chapter 2, "The
Contrarian." His edge is built on a simple observation: retail and
speculative trend-following flows tend to be maximally positioned at trend
*exhaustion*, not trend *inception* — because trend followers only get
maximally long or short after a trend has run far enough to convince them
it's real. By the time everyone who wants to be long is long, there is no
incremental buyer left to push price higher, and the market becomes
vulnerable to reversal.

Shapiro's process has five steps. This skill automates step 1 only. Steps 2-5
require news judgment, chart reading, and discretionary risk management, and
are documented here as the manual process to guide the user through.

## The Five Steps

### Step 1: Crowding Detection (AUTOMATED by this skill)

Identify markets where large speculators ("non-commercial" traders in CFTC
terminology — hedge funds, CTAs, momentum funds) are at or near an extreme of
their net positioning over a multi-year lookback. This skill computes a COT
Index (see `cot-index-calculation.md`) over a 156-week (3-year) window and
flags markets where the index is >= 90 (crowded long) or <= 10 (crowded
short).

**Why speculators, not commercials:** Commercial traders (producers, end
users, banks hedging exposure) transact for structural/hedging reasons tied
to their business, not because they believe the market is about to move.
Their positioning reflects supply-chain economics, not crowd psychology.
Speculators, by contrast, are directional bettors — their positioning *is*
the crowd. Shapiro's edge specifically targets fading the speculative crowd,
because commercials being "extreme" carries no comparable behavioral signal.

**Why a 3-year lookback:** A COT Index measures where current positioning
sits relative to its own recent range. Too short a lookback (a few months)
produces false extremes in choppy, range-bound markets. Too long (10+ years)
mixes structurally different regimes (e.g., pre- and post-2008 rate
environments) and can understate a genuine extreme. Three years is the
common convention in COT-index literature and crowdedmarketreport.com's
public methodology — long enough to span multiple full cycles, short enough
to stay regime-relevant.

### Step 2: News Failure (MANUAL — Claude guides via WebSearch)

This is the core of Shapiro's edge and the step most traders skip. Once a
market is flagged as crowded, check whether recent news that *should* have
been favorable to the crowd's direction failed to move price the expected
way.

- **Crowded long + bullish news + no rally (or a fade)** → the buying power
  is exhausted; the crowd has nothing left to push price higher even on good
  news. This is bearish confirmation for a contrarian short.
- **Crowded short + bearish news + no decline (or a rally)** → the selling
  power is exhausted. This is bullish confirmation for a contrarian long.

**Example (illustrative):** Large speculators are crowded long on the S&P
500 (COT Index 95+). A strong jobs report or dovish Fed surprise hits — both
textbook bullish catalysts — and the index barely budges, or sells off into
the news. That non-reaction is the tell: everyone who was going to buy on
good news already has.

**How to check:** Use WebSearch for the market's major news catalysts over
the trailing 1-2 weeks (economic releases, central bank decisions, earnings
for equity-index futures, OPEC/inventory data for energy, etc.), then compare
the news direction to the actual price reaction on that day/week. A
significant *mismatch* (good news, flat/down price; bad news, flat/up price)
is the signal, not the news itself.

### Step 3: Price-Action Confirmation (MANUAL — Claude guides via chart reading)

Look for a weekly-chart reversal signal that corroborates the crowding +
news-failure read:
- A failure to make a new high (crowded long) or new low (crowded short)
  despite the prevailing trend still being intact on paper
- A weekly reversal candle (e.g., an outside week, a key reversal, a
  failed breakout that closes back inside the prior range)
- Loss of a key trendline or moving average that the trend had respected

This step exists because news failure alone can be noisy — requiring price
to actually confirm the exhaustion reduces false positives.

### Step 4: Entry (MANUAL — Claude guides via position-sizer skill)

Enter against the crowd (short a crowded-long market, long a crowded-short
market) once steps 2 and 3 both confirm. Use a fixed, small risk-per-trade
size and place the stop at the recent swing extreme (the high the crowd
formed, for a short; the low, for a long) — if the crowd's positioning
extreme is actually still intact, the trade thesis is wrong and should be
cut quickly. Route sizing through the `position-sizer` skill for
consistent, risk-based share/contract counts.

### Step 5: Exit (MANUAL)

Two exit triggers:
- **Positioning normalizes** — the COT Index drifts back toward 50 (neutral)
  over subsequent weekly releases, indicating the crowd has unwound and the
  edge has played out.
- **Stop hit** — price reclaims the crowd's extreme, invalidating the
  exhaustion thesis.

There is no fixed profit target in Shapiro's framework; the position is
managed against the positioning data itself, re-checked weekly as new COT
reports are published.

## What This Skill Automates vs. What Stays Manual

| Step | Automated? | How |
|---|---|---|
| 1. Crowding detection | Yes | `scripts/screen_cot_crowding.py` computes COT Index per market and classifies CROWDED_LONG/SHORT/NEUTRAL |
| 2. News failure | No | Claude uses WebSearch on the flagged market's recent catalysts and compares to price reaction |
| 3. Price-action confirmation | No | Claude reads the weekly chart (via `technical-analyst` skill or user-provided chart) for a reversal signal |
| 4. Entry | No | Claude sizes via `position-sizer`, places stop at the crowd's swing extreme |
| 5. Exit | No | Claude monitors subsequent weekly COT releases for normalization, or the stop |

## The 3-Day Publication Lag

The CFTC's COT report is published every Friday at approximately 3:30pm ET,
containing positions as of the **prior Tuesday's close**. This means the
data is always at least 3 calendar days old on publication day, and up to 9
days old by the following Friday (just before the next release). Two
practical implications:

1. **Never treat COT data as a real-time signal.** A crowd can unwind
   materially in the days between the Tuesday snapshot and when you're
   reading the report.
2. **News-failure checks (step 2) should focus on news from around and after
   the Tuesday snapshot date**, not the publication date — that's the window
   the positioning data actually reflects.

## Participation and Open Interest Context

A COT Index extreme means more when it comes with meaningful participation.
Two markets can both show a 95 COT Index, but one may have 10 large
speculators holding the extreme and the other 200 — the latter is a broader,
more durable crowd. The screener surfaces `traders_long`/`traders_short`
(trader counts) and `open_interest` alongside the index so this context isn't
lost; a large but thin-participation extreme is more prone to a false
signal than a large, broad-participation one.

## Sources

- Jack D. Schwager, *Unknown Market Wizards* (2020), Chapter 2: "Jason
  Shapiro: The Contrarian"
- crowdedmarketreport.com — public COT Index methodology and market
  commentary (Shapiro's own site)


---

## SKILL: crypto-regime-analyzer

- Fuente: `tradermonty/claude-trading-skills` → `skills/crypto-regime-analyzer` (MIT)
- Cuándo usarla: Quantifies crypto market regime health using free, keyless public data (CoinGecko + Binance funding). Generates a 0-100 composite score across 6 components (100 = risk-on) with a posture recommendation. No API key required. Use when user asks about crypto market conditions, whether it's alt season, BTC dominance, crypto risk-on vs risk-off, funding rates, or whether crypto exposure should be increased or reduced.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/crypto-regime-analyzer/` (requirements.txt, __init__.py, alt_breadth_calculator.py, btc_trend_calculator.py, dominance_calculator.py, drawdown_vol_calculator.py, funding_calculator.py, momentum_thrust_calculator.py, crypto_regime_analyzer.py, data_client.py, numeric_utils.py, report_generator.py …)

# Crypto Regime Analyzer Skill

## Purpose

Quantify the crypto market regime using a data-driven 6-component scoring system (0-100). This is the crypto analog of `market-breadth-analyzer` + `exposure-coach`: it answers "what posture does the crypto market currently support?" before any coin-level analysis happens.

**Score direction:** 100 = Maximum risk-on health (broad participation, healthy trend, sane leverage), 0 = Critical risk-off.

**No API key required** — uses CoinGecko's free public API and Binance's public futures endpoint.

## When to Use This Skill

- User asks "Is crypto risk-on or risk-off right now?" or "How healthy is the crypto market?"
- User asks "Is it alt season?" or about BTC dominance direction
- User asks whether funding rates are overheated
- User wants an exposure posture for a crypto sleeve before screening individual coins
- User wants a daily crypto regime check alongside the equity `market-regime-daily` workflow

## What This Skill Does NOT Do

- No coin picks, no buy/sell signals, no price targets
- No execution or portfolio changes — regime description only
- Human decision gates remain central, consistent with the project vision

## Prerequisites

- **Python 3.9+** with `requests` (live mode only; offline mode is stdlib-only)
- **Internet access** to `api.coingecko.com` and `fapi.binance.com` (live mode)
- **No API keys required**

## Component Model

| # | Component | Weight | Question it answers |
|---|---|---|---|
| 1 | BTC Trend Structure | 25% | Is the reserve asset's primary trend intact? (price vs 50/200DMA stack, 200DMA slope) |
| 2 | Alt Breadth Participation | 20% | How broadly are alts participating? (% of top-N above 200DMA, 50DMA confirmation) |
| 3 | BTC Dominance Regime | 15% | Where is capital rotating? (dominance direction interpreted jointly with BTC trend) |
| 4 | Perpetual Funding Regime | 15% | How crowded is leverage? (avg funding across majors; contrarian at extremes) |
| 5 | Drawdown & Volatility Position | 15% | Where are we in the cycle? (drawdown from 1y high, realized vol percentile) |
| 6 | Momentum Thrust / Washout | 10% | Short-horizon confirmation (% of universe positive over 30d) |

Missing components have their weight proportionally redistributed (same convention as `market-breadth-analyzer`). Full scoring logic: `references/crypto_regime_methodology.md`.

### Regime Zones

| Score | Zone | Posture |
|---|---|---|
| 80-100 | RISK_ON | Broad risk-on conditions observed; review risk limits before decisions |
| 40-79 | NEUTRAL | Mixed conditions observed; no strong regime conclusion |
| 0-39 | RISK_OFF | Defensive market conditions observed; review existing risk controls |

These are heuristic descriptive bands, not validated allocation rules. See
`references/VALIDATION.md` for the current evidence boundary and the artifacts
required before making quantitative performance claims.

---

## Execution Workflow

### Phase 1: Run the Analysis Script

**Live mode** (fetches CoinGecko + Binance; first run of the day takes ~2-4 minutes at the default `--top-n 20` due to free-tier rate-limit throttling; same-day re-runs hit the cache and are instant):

```bash
mkdir -p reports/<routine-or-date>
python3 skills/crypto-regime-analyzer/scripts/crypto_regime_analyzer.py \
  --output-dir reports/<routine-or-date>
```

**Offline mode** (no network; snapshot schema in the methodology reference):

```bash
python3 skills/crypto-regime-analyzer/scripts/crypto_regime_analyzer.py \
  --input-json snapshot.json \
  --output-dir reports/<routine-or-date>
```

Options: `--top-n <int>` universe size (default 20), `--cache-dir <path>` fetch cache location (default `.crypto_regime_cache`), `--quiet`.

### Phase 2: Interpret the Output

The script writes `crypto_regime.json` (machine-readable, for chaining into other skills) and `crypto_regime.md` (one-page report), and prints a one-line summary:

```
CRYPTO REGIME: NEUTRAL (score 68.4/100) — Mixed conditions observed; no strong regime conclusion
```

When presenting results, lead with the zone and posture, then explain the 1-2 components most responsible for the score using their `signal` strings. Flag any components reporting `data_available: false` and what that means for confidence.

### Phase 3 (optional): Feed Downstream

The JSON composite can slot into an `exposure-coach`-style posture summary as
one descriptive crypto-market input. It must not independently authorize,
block, size, or execute a trade.

## Output

The script writes two artifacts to `--output-dir` and prints a one-line summary for workflow chaining:

- `crypto_regime.json` — full machine-readable analysis: `metadata`, per-component results (`score`, `signal`, `data_available`, component-specific fields), and the `composite` block (`score`, `zone`, `guidance`, `effective_weights`).
- `crypto_regime.md` — one-page report: composite score with zone bar, posture line, per-component table (weight / score / signal), and confidence notes.
- Console: `CRYPTO REGIME: <ZONE> (score <N>/100) — <posture>` plus warnings for any skipped components.

## Resources

- `references/VALIDATION.md` — validation status, evidence boundary, and reproduction requirements.
- `references/crypto_regime_methodology.md` — full scoring rationale, every threshold table, the offline snapshot JSON schema, and the live data-source endpoint list.
- `scripts/crypto_regime_analyzer.py` — CLI orchestrator (entry point).
- `scripts/data_client.py` — CoinGecko/Binance fetchers, per-day cache, dominance history accumulator, offline loader.
- `scripts/calculators/` — one module per component; pure functions, fully unit-tested.
- `scripts/scorer.py` — weighted composite with proportional weight redistribution.
- `scripts/tests/` — tests covering every component, the scorer, sparse-data fail-closed behavior, and end-to-end bull/bear/degraded snapshots.

## Known Limitations

- **Dominance history accumulates locally.** CoinGecko's free tier only exposes *current* dominance, so the client stores one observation per run-day in the cache dir. The dominance component reports `data_available: false` until 31 daily observations exist (weight is redistributed until then). Seed it faster via `--input-json`.
- **Funding is best-effort.** If Binance's endpoint is unreachable (geo-restrictions, outage), the component is skipped gracefully.
- **Universe is top-N by market cap** with stablecoins and wrapped/staked assets excluded; it is not a fixed index, so composition drifts with the market.
- Thresholds are heuristic and documented in the methodology reference; they are conservative defaults, not backtested optima.

## Disclaimer

Educational and process-improvement use only. This skill describes market conditions; it does not provide financial advice, signals, or buy/sell instructions. All decisions remain the user's responsibility.

### Referencia: references/VALIDATION.md

# Validation Status and Reproduction Requirements

The component and zone thresholds in this beta skill are documented
heuristics. This repository does not currently include a pinned historical
dataset or a walk-forward harness capable of reproducing quantitative return,
win-rate, or drawdown claims. Accordingly, this skill makes no such claims and
its zone labels must not be treated as allocation or performance rules.

## What is verified in-repository

- Pure component calculations and boundary behavior are covered by unit tests.
- Offline bull, bear, degraded-data, and sparse-data snapshots exercise the
  same `run_analysis()` entry point used by live mode.
- Missing inputs fail closed: a composite classification requires at least four
  components representing at least 65% of original model weight.
- Report and package drift are checked by repository validation gates.

These tests establish deterministic software behavior. They do not establish
predictive power or investment performance.

## Required artifacts for historical validation

A future validation change must include all of the following in the repository:

1. A runnable harness that imports the shipped calculation code.
2. A data manifest with source URLs, retrieval timestamps, hashes, symbol map,
   delisting policy, and point-in-time universe construction.
3. A pinned or deterministically retrievable input snapshot that permits an
   offline rerun without silently substituting current constituents.
4. Explicit no-lookahead rules, missing-data treatment, transaction-cost
   assumptions, and non-overlapping or dependence-aware statistical summaries.
5. Machine-checked expected aggregates and documented commands to reproduce
   them.

Until those artifacts exist, `RISK_ON`, `NEUTRAL`, and `RISK_OFF` are descriptive
heuristic bands only. Any historical experiment performed outside this
repository is exploratory and must not be presented as verified evidence here.

### Referencia: references/crypto_regime_methodology.md

# Crypto Regime Methodology

Scoring rationale, thresholds, and data schemas for `crypto-regime-analyzer`.

## Design Principles

1. **BTC-anchored.** Bitcoin trend structure carries the largest weight (25%) because alt regimes rarely stay risk-on while BTC's primary trend is broken. Alt breadth and dominance are interpreted *conditionally* on BTC trend.
2. **Contrarian at extremes, trend-following in the middle.** Funding, drawdown, and momentum components give small contrarian bumps at washout extremes (near-total negative momentum, >65% drawdown with vol expansion, negative funding) because those readings historically coincide with improving forward returns — while remaining trend-respecting in normal ranges.
3. **Degrade, never fail.** Every component reports `data_available`; missing components have weight proportionally redistributed, mirroring `market-breadth-analyzer`.
4. **Free and keyless.** All live data comes from CoinGecko public + Binance public futures endpoints. Thresholds are heuristics chosen for interpretability, not backtest-optimized parameters — treat them as documented defaults to be revisited, not edge claims.

## Component Details

### 1. BTC Trend Structure (25%)

Inputs: >= 220 daily BTC closes (200-day average plus a 20-day slope lookback).

| Structure | Base |
|---|---|
| price = 50DMA = 200DMA (flat) | 50 |
| price > 50DMA > 200DMA (bull stack) | 90 |
| price between 200DMA and 50DMA, stack intact (pullback) | 65 |
| price below both, 50DMA still > 200DMA | 55 |
| price > 50DMA but 50DMA <= 200DMA (recovery attempt) | 45 |
| price < 50DMA < 200DMA (bear stack) | 15 |

Modifier: 200DMA slope over a 20-day lookback, +10 rising / 0 flat / -10 falling. Signal notes when the 50/200DMA gap is within 1.5% (imminent cross watch). Score clamped to [0, 100].

### 2. Alt Breadth Participation (20%)

Inputs: daily closes for the top-N universe excluding BTC; coins with < 200 observations are skipped and listed. Requires >= 5 usable alts.

Base from % above 200DMA: >=80% → 95, >=65% → 80, >=50% → 65, >=35% → 45, >=20% → 25, else 10. Modifier: 50DMA breadth leading 200DMA breadth by >= 15pts → +5 (fresh thrust); lagging by >= 15pts → -5 (rolling over).

### 3. BTC Dominance Regime (15%)

Inputs: >= 31 daily dominance observations + BTC-trend-constructive flag (Component 1 score >= 60). Direction = 30d change, ±0.5pt flat band.

| BTC trend | Dominance | Score | Reading |
|---|---|---|---|
| up | falling | 90 | Alt rotation (risk-on down the risk curve) |
| up | flat | 75 | — |
| up | rising | 65 | BTC-led, alts lagging |
| down | rising | 30 | Defensive rotation inside crypto |
| down | flat | 25 | — |
| down | falling | 10 | Indiscriminate de-risking |

Extremes: dominance >= 62% in a BTC downtrend → +5 (washout watch); <= 40% in an uptrend → -5 (froth caution).

### 4. Perpetual Funding Regime (15%)

Inputs: latest 8h funding rate per tracked USDT perp (>= 2 symbols). Average across symbols, banded:

| Avg 8h funding | Score | Reading |
|---|---|---|
| <= -0.010% | 80 | Washed out (shorts pay) |
| -0.010% .. 0% | 65 | Skeptical |
| 0% .. +0.010% | 75 | Neutral (Binance baseline is +0.010%) |
| +0.010% .. +0.030% | 55 | Long leverage building |
| +0.030% .. +0.060% | 30 | Crowded longs |
| > +0.060% | 10 | Euphoric; liquidation-cascade risk |

### 5. Drawdown & Volatility Position (15%)

Inputs: >= 365 daily BTC closes. Base from drawdown vs trailing 1y high: <=10% → 90, <=20% → 75, <=35% → 55, <=50% → 35, <=65% → 20, else 10. Modifier: 30d realized vol (annualized, log returns) vs its trailing-1y distribution sampled at weekly stride — bottom third → +10, top third → -10. Contrarian floor: drawdown > 65% AND vol in top third → score floors at 15 (capitulation zone).

### 6. Momentum Thrust / Washout (10%)

Inputs: 31+ daily closes per coin, >= 5 usable coins, BTC included. % of universe with positive 30d return: >=85% → 90, >=65% → 75, >=45% → 55, >=25% → 35, >=10% → 20, <10% → 35 (washout: contrarian bump over the plain mapping).

## Composite & Zones

Weighted average over available components with proportional weight redistribution only when at least four components representing at least 65% of original model weight remain. Sparser inputs return `UNKNOWN`. Zones are heuristic descriptive bands: 80-100 RISK_ON, 40-79 NEUTRAL, and 0-39 RISK_OFF. They are not validated allocation rules; see `VALIDATION.md` for the evidence boundary and reproduction requirements.

## Offline Snapshot Schema (`--input-json`)

```json
{
  "as_of": "2026-07-01T00:00:00Z",
  "series": {
    "BTC": [45000.0, 45210.5, "... daily closes oldest -> newest ..."],
    "ETH": [2400.0, 2415.2],
    "SOL": [140.0, 141.8]
  },
  "dominance_series": [56.1, 56.0, 55.8],
  "funding": {
    "BTCUSDT": 0.0001,
    "ETHUSDT": 0.00008
  }
}
```

Rules:

- `series` **must** include a `"BTC"` key; all other keys are treated as alts.
- Closes are finite positive numbers, oldest -> newest, ideally 400+ observations (220 minimum for BTC trend, 365 for drawdown/vol, 200 for alt breadth membership).
- `dominance_series` is daily BTC dominance percentages oldest -> newest; empty list is allowed (component degrades).
- `dominance_series` values must be finite percentages greater than 0 and at most 100.
- `funding` values are finite decimal 8h rates (`0.0001` = +0.010%) in the inclusive range `[-1, 1]`; empty object is allowed (component degrades). The deliberately wide range is a numerical-safety guard, not a claim that such extreme rates are economically plausible.

## Data Sources (live mode)

| Endpoint | Used for | Auth |
|---|---|---|
| `GET api.coingecko.com/api/v3/coins/markets` | Top-N universe | none |
| `GET api.coingecko.com/api/v3/coins/{id}/market_chart` | Daily close history | none |
| `GET api.coingecko.com/api/v3/global` | Current BTC dominance | none |
| `GET fapi.binance.com/fapi/v1/premiumIndex` | Latest funding per perp | none |

Fetches are throttled at ~6.5s between history calls to respect CoinGecko's free-tier limits and cached per UTC day under `--cache-dir`.


---

## SKILL: downtrend-duration-analyzer

- Fuente: `tradermonty/claude-trading-skills` → `skills/downtrend-duration-analyzer` (MIT)
- Cuándo usarla: Analyze historical downtrend durations and generate interactive HTML histograms showing typical correction lengths by sector and market cap.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/downtrend-duration-analyzer/` (requirements.txt, analyze_downtrends.py, generate_histogram_html.py)

# Downtrend Duration Analyzer

## Overview

Analyze historical price data to identify downtrend periods (peak-to-trough) and build statistical distributions of correction durations. Generate interactive HTML visualizations with histograms segmented by sector and market cap to help traders understand typical recovery timeframes and set realistic expectations for mean reversion strategies.

## When to Use

- Trader asks about typical correction lengths for a sector or market cap tier
- User wants to understand historical drawdown recovery times
- Building mean reversion or pullback strategies that need realistic holding period estimates
- Comparing correction behavior across different market segments
- Setting stop-loss timeouts or position holding period limits

## Prerequisites

- Python 3.9+
- FMP API key (set `FMP_API_KEY` environment variable or use `--api-key`)
- Required packages: `requests`, `pandas`, `numpy` (standard data analysis stack)

## Workflow

### Step 1: Fetch Historical Price Data

Run the analysis script to fetch OHLC data for a universe of stocks and identify downtrend periods.

```bash
python3 skills/downtrend-duration-analyzer/scripts/analyze_downtrends.py \
  --sector "Technology" \
  --lookback-years 5 \
  --output-dir reports/
```

### Step 2: Analyze Downtrend Durations

The script automatically:
1. Identifies local peaks and troughs using rolling window analysis
2. Calculates duration (trading days) and depth (% decline) for each downtrend
3. Segments results by sector and market cap tier (Mega, Large, Mid, Small)
4. Computes summary statistics (median, mean, percentiles)

### Step 3: Generate Interactive HTML Visualization

```bash
python3 skills/downtrend-duration-analyzer/scripts/generate_histogram_html.py \
  --input reports/downtrend_analysis_*.json \
  --output-dir reports/
```

This creates an interactive HTML file with:
- Histogram of downtrend durations
- Filters for sector and market cap
- Hover tooltips with percentile information
- Summary statistics table

### Step 4: Review Distribution Insights

Load the generated markdown report to interpret the findings:
- **Short corrections (5-15 days)**: Typical pullbacks within uptrends
- **Medium corrections (15-40 days)**: Standard sector rotations
- **Extended corrections (40+ days)**: Trend changes or bear markets

## Output Format

### JSON Report

```json
{
  "schema_version": "1.0",
  "analysis_date": "2026-03-28T07:00:00Z",
  "parameters": {
    "lookback_years": 5,
    "sector_filter": "Technology",
    "peak_window": 20,
    "trough_window": 20
  },
  "summary": {
    "total_downtrends": 1234,
    "median_duration_days": 18,
    "mean_duration_days": 24.5,
    "p25_duration_days": 10,
    "p75_duration_days": 32,
    "p90_duration_days": 55
  },
  "by_sector": {
    "Technology": {
      "count": 456,
      "median_days": 15,
      "mean_days": 20.3
    }
  },
  "by_market_cap": {
    "Mega": {"count": 200, "median_days": 12},
    "Large": {"count": 300, "median_days": 16},
    "Mid": {"count": 400, "median_days": 22},
    "Small": {"count": 334, "median_days": 28}
  },
  "downtrends": [
    {
      "symbol": "AAPL",
      "sector": "Technology",
      "market_cap_tier": "Mega",
      "peak_date": "2025-01-15",
      "trough_date": "2025-02-10",
      "duration_days": 18,
      "depth_pct": -12.5
    }
  ]
}
```

### Markdown Report

```markdown
# Downtrend Duration Analysis

**Date**: 2026-03-28
**Lookback**: 5 years
**Sector**: Technology

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total Downtrends | 1,234 |
| Median Duration | 18 days |
| Mean Duration | 24.5 days |
| 25th Percentile | 10 days |
| 75th Percentile | 32 days |
| 90th Percentile | 55 days |

## By Market Cap Tier

| Tier | Count | Median | Mean |
|------|-------|--------|------|
| Mega ($200B+) | 200 | 12 days | 15.2 days |
| Large ($10-200B) | 300 | 16 days | 20.1 days |
| Mid ($2-10B) | 400 | 22 days | 28.4 days |
| Small (<$2B) | 334 | 28 days | 35.6 days |

## Key Insights

1. Larger companies recover faster from corrections
2. Technology sector shows shorter median correction than market average
3. 90% of corrections resolve within 55 trading days
```

### HTML Visualization

Interactive histogram saved to `reports/downtrend_histogram_YYYY-MM-DD.html` with:
- Plotly.js-based interactive charts
- Sector and market cap dropdown filters
- Duration distribution with bin controls
- Percentile markers (P25, P50, P75, P90)

Reports are saved to `reports/` with filenames:
- `downtrend_analysis_YYYY-MM-DD_HHMMSS.json`
- `downtrend_analysis_YYYY-MM-DD_HHMMSS.md`
- `downtrend_histogram_YYYY-MM-DD_HHMMSS.html`

## Resources

- `scripts/analyze_downtrends.py` -- Main analysis script for fetching data and computing downtrend durations
- `scripts/generate_histogram_html.py` -- HTML visualization generator with interactive histograms
- `references/downtrend_methodology.md` -- Peak/trough detection algorithms and market cap tier definitions

## Key Principles

1. **Statistical Rigor**: Use robust peak/trough detection to avoid noise-induced false signals
2. **Segmentation Matters**: Always analyze by sector and market cap; averages hide important differences
3. **Realistic Expectations**: Use percentiles (not just means) to understand the full distribution of outcomes

### Referencia: references/downtrend_methodology.md

# Downtrend Duration Analysis Methodology

## Overview

This document describes the technical methodology for identifying downtrend periods in historical price data and computing duration statistics. The approach is designed to be robust against noise while capturing meaningful corrections.

## Peak and Trough Detection

### Rolling Window Algorithm

The primary algorithm uses a rolling window approach to identify local peaks and troughs:

1. **Peak Detection**: A price point is a local peak if it is the highest close within a `window` trading days on both sides.
   ```
   peak[i] = close[i] == max(close[i-window:i+window+1])
   ```

2. **Trough Detection**: A price point is a local trough if it is the lowest close within a `window` trading days on both sides.
   ```
   trough[i] = close[i] == min(close[i-window:i+window+1])
   ```

### Default Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `peak_window` | 20 | Trading days on each side for peak detection |
| `trough_window` | 20 | Trading days on each side for trough detection |
| `min_depth_pct` | 5.0 | Minimum decline percentage to qualify as a downtrend |

### Noise Filtering

To avoid counting minor fluctuations:
- **Minimum Depth Filter**: Only downtrends with depth >= `min_depth_pct` are included
- **Minimum Duration Filter**: Downtrends shorter than 3 days are excluded
- **Overlap Handling**: When peaks/troughs overlap (multiple detected within window), keep the most extreme value

## Downtrend Definition

A **downtrend period** is defined as:
1. Starts at a detected local peak
2. Ends at the subsequent local trough
3. No higher high occurs between peak and trough
4. Depth (%) = (trough_price - peak_price) / peak_price * 100

### Duration Calculation

Duration is measured in **trading days** (not calendar days):
- Count business days between peak date and trough date (inclusive)
- Excludes weekends and market holidays
- Use market calendar for accurate counting

## Market Cap Tier Definitions

Stocks are segmented into tiers based on market capitalization:

| Tier | Market Cap Range | Typical Characteristics |
|------|------------------|------------------------|
| **Mega** | >= $200B | Index heavyweights, high liquidity, institutional ownership |
| **Large** | $10B - $200B | Established companies, moderate volatility |
| **Mid** | $2B - $10B | Growth phase companies, higher volatility |
| **Small** | < $2B | Emerging companies, less liquidity, higher risk |

### Why Segmentation Matters

Research shows significant differences in correction behavior:
- **Mega caps** typically have shorter, shallower corrections due to:
  - Index fund rebalancing provides buying support
  - Higher analyst coverage means faster price discovery
  - Institutional investors provide liquidity

- **Small caps** experience longer, deeper corrections due to:
  - Lower liquidity amplifies price moves
  - Less analyst coverage delays information incorporation
  - Higher retail participation increases volatility

## Sector-Specific Patterns

Different sectors exhibit characteristic correction patterns:

### Defensive Sectors
- **Utilities, Consumer Staples, Healthcare**: Shorter median corrections (12-18 days)
- Lower depth, faster recovery during risk-off periods

### Cyclical Sectors
- **Technology, Consumer Discretionary, Industrials**: Longer median corrections (20-30 days)
- Deeper drawdowns, correlated with economic cycles

### Commodity-Linked Sectors
- **Energy, Materials**: Highly variable (15-45 days)
- Driven by commodity price cycles, geopolitical events

## Statistical Measures

### Percentile Interpretation

| Percentile | Meaning | Trading Application |
|------------|---------|---------------------|
| P25 | 25% of corrections end by this duration | Aggressive entry timing |
| P50 (Median) | Half of corrections end by this duration | Standard expectation |
| P75 | 75% of corrections end by this duration | Conservative planning |
| P90 | 90% of corrections end by this duration | Extended timeline, consider re-evaluation |

### Why Use Median Over Mean

- Correction durations are **right-skewed** (long tail of extended corrections)
- Mean is inflated by outliers (bear markets, sector crashes)
- Median provides more realistic "typical" expectation
- Always report both, plus percentiles, for complete picture

## Historical Benchmarks

Based on S&P 500 components, 2019-2024:

| Category | P25 | P50 | P75 | P90 |
|----------|-----|-----|-----|-----|
| All Stocks | 8 | 18 | 35 | 62 |
| Mega Cap | 6 | 12 | 25 | 45 |
| Large Cap | 8 | 16 | 32 | 55 |
| Mid Cap | 10 | 22 | 42 | 70 |
| Small Cap | 12 | 28 | 52 | 85 |

*Note: These are illustrative benchmarks; actual values vary by market conditions.*

## Application Guidelines

### Mean Reversion Strategies

1. **Entry Timing**: Use sector-specific P25-P50 range as target entry window
2. **Position Sizing**: Scale in gradually as correction extends beyond median
3. **Stop-Loss Timing**: If correction exceeds P90, reassess thesis

### Pullback Buying

1. **Wait Period**: Allow at least sector median duration before aggressive entry
2. **Depth Confirmation**: Verify decline meets minimum depth threshold
3. **Volume Pattern**: Look for volume spike at trough formation

### Risk Management

1. **Time Stops**: Set maximum holding period based on P90 duration
2. **Recovery Expectations**: Plan for median recovery time, budget for P75
3. **Sector Rotation**: Use relative correction durations to time sector moves

## Limitations

1. **Past Performance**: Historical distributions may not predict future corrections
2. **Regime Changes**: Market structure changes (ETFs, algo trading) affect patterns
3. **Black Swan Events**: Extreme events (2020 COVID, 2008 GFC) are outliers
4. **Survivorship Bias**: Analysis of current constituents excludes delisted stocks

## References

- Fama, E. & French, K. (1993). Common risk factors in the returns on stocks and bonds.
- Jegadeesh, N. (1990). Evidence of predictable behavior of security returns.
- Lo, A. & MacKinlay, A. (1988). Stock market prices do not follow random walks.


---

## SKILL: economic-calendar-fetcher

- Fuente: `tradermonty/claude-trading-skills` → `examples/weekly-trade-strategy/.claude/skills/economic-calendar-fetcher` (MIT)
- Cuándo usarla: Fetch upcoming economic events and data releases using FMP API. Retrieve scheduled central bank decisions, employment reports, inflation data, GDP releases, and other market-moving economic indicators for specified date ranges (default: next 7 days). The script outputs raw JSON or text; the assistant filters, assesses impact, and generates the Markdown report.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `examples/weekly-trade-strategy/.claude/skills/economic-calendar-fetcher/` (get_economic_calendar.py)

# Economic Calendar Fetcher

## Overview

Retrieve upcoming economic events and data releases from the Financial Modeling Prep (FMP) Economic Calendar API. This skill fetches scheduled economic indicators including central bank monetary policy decisions, employment reports, inflation data (CPI/PPI), GDP releases, retail sales, manufacturing data, and other market-moving events that impact financial markets.

The skill uses a Python script to query the FMP API and returns raw JSON or text output. The assistant then filters events, assesses market impact, and generates a chronological Markdown report for each scheduled event. No files are generated automatically.

**Key Capabilities:**
- Fetch economic events for specified date ranges (max 90 days)
- Support flexible API key provision (environment variable or CLI argument)
- Filter by impact level, country, or event type (filtering performed by the assistant)
- Present filtered results as structured Markdown reports with impact analysis (assistant-generated, not script-generated)
- Default to next 7 days for quick market outlook

**Data Source:**
- FMP Economic Calendar API: `https://financialmodelingprep.com/api/v3/economic_calendar`
- Covers major economies: US, EU, UK, Japan, China, Canada, Australia
- Event types: Central bank decisions, employment, inflation, GDP, trade, housing, surveys

## When to Use This Skill

Use this skill when the user requests:

1. **Economic Calendar Queries:**
   - "What economic events are coming up this week?"
   - "Show me the economic calendar for the next two weeks"
   - "When is the next FOMC meeting?"
   - "What major economic data is being released next month?"

2. **Market Event Planning:**
   - "What should I watch for in the markets this week?"
   - "Are there any high-impact economic releases coming?"
   - "When is the next jobs report / CPI release / GDP report?"

3. **Specific Date Range Requests:**
   - "Get economic events from January 1 to January 31"
   - "What's on the economic calendar for Q1 2025?"

4. **Country-Specific Queries:**
   - "Show me US economic data releases next week"
   - "What ECB events are scheduled?"
   - "When is Japan releasing their inflation data?"

**DO NOT use this skill for:**
- Past economic events (use market-news-analyst for historical analysis)
- Corporate earnings calendars (this skill excludes earnings)
- Real-time market data or live quotes
- Technical analysis or chart interpretation

## Workflow

Follow these steps to fetch and analyze the economic calendar:

### Step 1: Obtain FMP API Key

**Check for API key availability (in priority order):**

1. **Recommended:** Check if `FMP_API_KEY` environment variable is set — this keeps the key out of session logs
2. **Acceptable:** Use `--api-key` CLI argument for one-off runs
3. **Not recommended:** Asking the user to paste the key into chat — session logs may retain it
4. If user doesn't have an API key, provide instructions:
   - Visit https://financialmodelingprep.com
   - Sign up for free account (250 requests/day limit)
   - Navigate to API dashboard to obtain key

**Example user interaction:**
```
User: "Show me economic events for next week"
Assistant: "I'll fetch the economic calendar. I'll use the FMP_API_KEY environment variable if it's set. Otherwise, please pass the key via --api-key when running the script."
```

### Step 2: Determine Date Range

**Set appropriate date range based on user request:**

**Default (no specific dates):** Today + 7 days
**User specifies period:** Use exact dates (validate format: YYYY-MM-DD)
**Maximum range:** 90 days (FMP API limitation)

**Examples:**
- "Next week" → Today to +7 days
- "Next two weeks" → Today to +14 days
- "January 2025" → 2025-01-01 to 2025-01-31
- "Q1 2025" → 2025-01-01 to 2025-03-31

**Validate date range:**
- Ensure start date ≤ end date
- Ensure range ≤ 90 days
- Warn if querying past dates

### Step 3: Execute API Fetch Script

**Run the get_economic_calendar.py script with appropriate parameters:**

**Basic usage (default 7 days):**
```bash
python3 /path/to/economic-calendar-fetcher/scripts/get_economic_calendar.py --api-key YOUR_KEY
```

**With specific date range:**
```bash
python3 /path/to/economic-calendar-fetcher/scripts/get_economic_calendar.py \
  --from 2025-01-01 \
  --to 2025-01-31 \
  --api-key YOUR_KEY \
  --format json
```

**Using environment variable (no --api-key needed):**
```bash
export FMP_API_KEY=your_key_here
python3 /path/to/economic-calendar-fetcher/scripts/get_economic_calendar.py \
  --from 2025-01-01 \
  --to 2025-01-07
```

**Script parameters:**
- `--from`: Start date (YYYY-MM-DD) - default: today
- `--to`: End date (YYYY-MM-DD) - default: today + 7 days
- `--api-key`: FMP API key (optional if FMP_API_KEY env var set)
- `--format`: Output format (json or text) - default: json
- `--output`: Output file path (optional, default: stdout)

**Handle errors:**
- Invalid API key → Ask user to verify key
- Rate limit exceeded (429) → Suggest waiting or upgrading FMP tier
- Network errors → Check your connection and re-run the script
- Invalid date format → Provide correct format example

### Step 4: Parse and Filter Events

**Process the JSON response from the script:**

1. **Parse event data:** Extract all events from API response
2. **Apply user filters if specified:**
   - Impact level: "High", "Medium", "Low"
   - Country: "US", "EU", "JP", "CN", etc.
   - Event type: FOMC, CPI, Employment, GDP, etc.
   - Currency: USD, EUR, JPY, etc.

**Filter examples:**
- "Show only high-impact events" → Filter impact == "High"
- "US events only" → Filter country == "US"
- "Central bank decisions" → Search event name for "Rate", "Policy", "FOMC", "ECB", "BOJ"

**Event data structure:**
```json
{
  "date": "2025-01-15 14:30:00",
  "country": "US",
  "event": "Consumer Price Index (CPI) YoY",
  "currency": "USD",
  "previous": 2.6,
  "estimate": 2.7,
  "actual": null,
  "change": null,
  "impact": "High",
  "changePercentage": null
}
```

### Step 5: Assess Market Impact

**Evaluate the market significance of each event:**

**Impact Level Classification (from FMP):**
- **High Impact:** Major market-moving events
  - FOMC rate decisions, ECB/BOJ policy meetings
  - Non-Farm Payrolls (NFP), CPI, GDP
  - Market typically shows 0.5-2%+ intraday volatility

- **Medium Impact:** Significant but less volatile
  - Retail Sales, Industrial Production
  - PMI surveys, Consumer Confidence
  - Housing data, Durable Goods Orders

- **Low Impact:** Minor indicators
  - Weekly jobless claims (unless extreme)
  - Regional manufacturing surveys
  - Minor auction results

**Additional Context Factors:**

1. **Current Market Sensitivity:**
   - High inflation environment → CPI/PPI elevated importance
   - Recession fears → Employment data more critical
   - Rate cut speculation → Central bank meetings crucial

2. **Surprise Potential:**
   - Compare estimate vs. previous reading
   - Large expected changes = higher attention
   - Consensus uncertainty = higher impact potential

3. **Event Clustering:**
   - Multiple related events same day = amplified impact
   - Example: CPI + Retail Sales + Fed speech = Very High impact day

4. **Forward Significance:**
   - Does this event influence upcoming central bank decisions?
   - Is this a preliminary or final reading?
   - Will this data be revised?

### Step 6: Generate Output Report

> **Responsibility:** The script outputs raw JSON or text. This step is performed by the assistant using the script's output. No Markdown files are generated automatically; results are displayed in chat and can be saved to `reports/` on request.

**Create structured markdown report with the following sections:**

**Report Header:**
```markdown
# Economic Calendar
**Period:** [Start Date] to [End Date]
**Report Generated:** [Timestamp]
**Total Events:** [Count]
**High Impact Events:** [Count]
```

**Event Listing (Chronological):**

For each event, provide:

```markdown
## [Date] - [Day of Week]

### [Event Name] ([Impact Level])
- **Country:** [Country Code] ([Currency])
- **Time:** [HH:MM UTC]
- **Previous:** [Value]
- **Estimate:** [Consensus Forecast]
- **Impact Assessment:** [Your analysis]

**Market Implications:**
[2-3 sentences on why this matters, what markets watch for, typical reaction patterns]

---
```

**Example Event Entry:**

```markdown
## 2025-01-15 - Wednesday

### Consumer Price Index (CPI) YoY (High Impact)
- **Country:** US (USD)
- **Time:** 14:30 UTC (8:30 AM ET — converted by assistant based on US DST calendar)
- **Previous:** 2.6%
- **Estimate:** 2.7%
- **Impact Assessment:** Very High - Core inflation metric for Fed policy decisions

**Market Implications:**
CPI reading above estimate (>2.7%) likely strengthens hawkish Fed expectations, potentially pressuring equities and supporting USD. Reading at or below 2.7% could reinforce disinflation narrative and support risk assets. Options market pricing 1.2% S&P 500 move on release day.

---
```

**Summary Section:**

Add analytical summary at the end:

```markdown
## Key Takeaways

**Highest Impact Days:**
- [Date]: [Events] - [Combined impact rationale]
- [Date]: [Events] - [Combined impact rationale]

**Central Bank Activity:**
- [Summary of any scheduled Fed/ECB/BOJ meetings or speeches]

**Major Data Releases:**
- Employment: [NFP, Unemployment Rate dates]
- Inflation: [CPI, PPI dates]
- Growth: [GDP, Retail Sales dates]

**Market Positioning Considerations:**
[2-3 bullets on how traders might position around these events]

**Risk Events:**
[Highlight any particularly high-uncertainty or surprise-potential events]
```

**Filtering Notes:**

If user requested specific filters, note at top:
```markdown
**Filters Applied:**
- Impact Level: High only
- Country: US
- Events shown: [X] of [Y] total events in date range
```

**Output:**
- Results are displayed in chat. No files are generated automatically.
- To save **raw JSON/text data**: use `--output reports/economic_calendar_[START]_to_[END].json` when running the script.
- To save the **Markdown report**: ask the assistant to write it to `reports/` after generating it in chat.

## Assistant-Generated Report Format

**Markdown structure requirements:**

1. **Chronological ordering:** Events sorted by date and time (earliest first)
2. **Impact level indicators:** Use (High Impact), (Medium Impact), (Low Impact) labels
3. **Time zone clarity:** Always specify UTC; ET/PT conversions are performed by the assistant based on US DST calendar
4. **Data completeness:** Include all available fields (previous, estimate, actual if past)
5. **Null handling:** Display "N/A" or "No estimate" for null values
6. **Impact assessment:** Every high/medium impact event must have market implications analysis

**Table format option (for dense listings):**

```markdown
| Date/Time (UTC) | Event | Country | Impact | Previous | Estimate | Assessment |
|-----------------|-------|---------|--------|----------|----------|------------|
| 01-15 14:30 | CPI YoY | US | High | 2.6% | 2.7% | Core inflation metric |
```

**Language:** All reports in English

## Resources

**Python Script:**
- `scripts/get_economic_calendar.py`: Main API fetch script with CLI interface

**Reference Documentation:**
- `references/fmp_api_documentation.md`: Complete FMP Economic Calendar API reference
  - Authentication and API key management
  - Request parameters and date formats
  - Response field definitions
  - Rate limits and error handling
  - Best practices for caching and efficiency

**API Details:**
- Endpoint: `https://financialmodelingprep.com/api/v3/economic_calendar`
- Authentication: API key required (free tier: 250 requests/day)
- Max date range: 90 days per request
- Response format: JSON array of event objects
- Rate limits: 5 requests/second (free tier)

**Event Coverage:**
- Major economies: US, EU, UK, Japan, China, Canada, Australia, Switzerland
- Event categories: Monetary policy, Employment, Inflation, GDP, Trade, Housing, Surveys
- Update frequency: Real-time (events added/updated as scheduled)
- Historical data: Available for past events with actual values

**Usage Tips:**
1. Cache results to minimize API calls (events rarely change once scheduled)
2. Query 7-30 day ranges for optimal request efficiency
3. Don't query >6 months in future (sparse data, speculative dates)
4. Refresh cache daily for upcoming week to catch time changes
5. Use smaller ranges (1-7 days) for real-time event monitoring

**Error Handling:**
- API key errors: Clear user guidance for obtaining free key
- Rate limits (429): Suggest waiting or upgrading FMP tier; re-run the script after the wait
- Network failures: Check connection and re-run; no automatic retry or cache in the script
- Invalid dates: Validation with helpful error messages

### Referencia: references/fmp_api_documentation.md

# FMP Economic Calendar API Documentation

## Overview

The Financial Modeling Prep (FMP) Economic Calendar API provides access to upcoming and historical economic data releases, central bank decisions, and other market-moving events. This API enables traders and investors to stay informed about scheduled economic events that may impact financial markets.

## API Endpoint

```
https://financialmodelingprep.com/api/v3/economic_calendar
```

## Authentication

API access requires a valid FMP API key, which must be included as a query parameter in all requests.

**Parameter:** `apikey`
**Format:** String
**Required:** Yes

### Obtaining an API Key

1. Visit https://financialmodelingprep.com
2. Sign up for an account (free and paid tiers available)
3. Navigate to the API dashboard to view your API key
4. Free tier allows limited requests per day (~250-300 requests)
5. Paid tiers offer higher rate limits and additional features

## Request Parameters

### Required Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `from` | date | Start date for calendar period | `2025-01-01` |
| `to` | date | End date for calendar period | `2025-01-31` |
| `apikey` | string | Your FMP API key | `YOUR_API_KEY` |

### Date Format

- **Format:** `YYYY-MM-DD` (ISO 8601 date format)
- **Example:** `2025-07-20`
- **Maximum Range:** 90 days between `from` and `to` dates
- **Timezone:** All dates are in UTC

### Date Range Limitations

- Minimum range: 1 day
- Maximum range: 90 days
- Past dates: API returns historical events with actual values
- Future dates: API returns scheduled events with estimates (actual values will be null)

## Response Format

The API returns a JSON array of economic event objects.

### Response Structure

```json
[
    {
        "date": "2024-03-01 03:35:00",
        "country": "JP",
        "event": "3-Month Bill Auction",
        "currency": "JPY",
        "previous": -0.112,
        "estimate": null,
        "actual": -0.096,
        "change": 0.016,
        "impact": "Low",
        "changePercentage": 14.286
    }
]
```

### Response Fields

| Field | Type | Description | Nullable |
|-------|------|-------------|----------|
| `date` | string | Event date and time in UTC (format: `YYYY-MM-DD HH:MM:SS`) | No |
| `country` | string | ISO 2-letter country code (e.g., `US`, `JP`, `GB`, `EU`) | No |
| `event` | string | Name/description of the economic event | No |
| `currency` | string | ISO 3-letter currency code (e.g., `USD`, `EUR`, `JPY`) | No |
| `previous` | number | Previous reading/value for this indicator | Yes |
| `estimate` | number | Market consensus estimate/forecast | Yes |
| `actual` | number | Actual released value (null for future events) | Yes |
| `change` | number | Absolute change from previous reading | Yes |
| `impact` | string | Market impact level: `"High"`, `"Medium"`, `"Low"` | No |
| `changePercentage` | number | Percentage change from previous reading | Yes |

### Field Details

**`date`:**
- Format: `YYYY-MM-DD HH:MM:SS` in UTC timezone
- Represents the scheduled release time for the economic data
- For future events, this is the expected release time
- Times may be adjusted if releases are delayed

**`country`:**
- ISO 3166-1 alpha-2 country codes
- Special codes:
  - `EU`: European Union (ECB-related events)
  - `G7`: G7 summit/collaborative events
  - International organizations may use special codes

**`event`:**
- Descriptive name of the economic indicator or event
- Examples:
  - `"Non-Farm Payrolls"`
  - `"Consumer Price Index (CPI)"`
  - `"Federal Funds Rate Decision"`
  - `"GDP Growth Rate QoQ"`
  - `"Unemployment Rate"`

**`currency`:**
- ISO 4217 currency codes
- Indicates which currency's economy the event affects
- May differ from country (e.g., EU events affect EUR across multiple countries)

**`previous`:**
- The last reported value for this indicator
- Used as baseline for comparing current release
- May be revised from originally reported value
- `null` if no prior data available (new indicator)

**`estimate`:**
- Market consensus forecast compiled from analyst surveys
- Typically from Bloomberg, Reuters, or other consensus services
- `null` if no consensus exists or for less-watched indicators
- Comparing `actual` to `estimate` shows "surprise" factor

**`actual`:**
- The officially released value when data is published
- `null` for future events (not yet released)
- This is the critical field that moves markets when released
- May be revised in subsequent releases (preliminary → final revisions)

**`change`:**
- Calculated as: `actual - previous` (for past events)
- `null` if either `actual` or `previous` is null
- Sign indicates direction: positive = increase, negative = decrease
- Absolute value, not percentage

**`impact`:**
- Qualitative assessment of market-moving potential
- Three levels:
  - `"High"`: Major market-moving events (NFP, FOMC, CPI)
  - `"Medium"`: Significant but less volatile (Retail Sales, PMI)
  - `"Low"`: Minor indicators, routine data releases
- Determined by FMP based on historical volatility impact

**`changePercentage`:**
- Calculated as: `((actual - previous) / previous) * 100`
- `null` if either value is null or if `previous` is zero
- Percentage representation of the change
- Useful for comparing relative magnitude across different indicators

## Example Requests

### Fetch Events for Next 7 Days

```bash
curl "https://financialmodelingprep.com/api/v3/economic_calendar?from=2025-01-01&to=2025-01-07&apikey=YOUR_API_KEY"
```

### Fetch High-Impact Events Only (Post-Processing)

Note: API does not have an `impact` filter parameter, so filtering must be done after retrieval.

```python
import requests

response = requests.get(
    "https://financialmodelingprep.com/api/v3/economic_calendar",
    params={
        "from": "2025-01-01",
        "to": "2025-01-31",
        "apikey": "YOUR_API_KEY"
    }
)

events = response.json()
high_impact_events = [e for e in events if e["impact"] == "High"]
```

### Fetch Events for Specific Country (Post-Processing)

```python
us_events = [e for e in events if e["country"] == "US"]
eu_events = [e for e in events if e["country"] == "EU"]
```

## Rate Limits

Rate limits depend on your FMP subscription tier:

| Tier | Requests/Day | Requests/Second |
|------|--------------|-----------------|
| Free | 250 | 5 |
| Starter | 500 | 10 |
| Professional | 1,000+ | 20+ |

If you exceed rate limits, the API returns HTTP 429 (Too Many Requests).

## Error Handling

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | Success | Request successful, data returned |
| 400 | Bad Request | Invalid parameters (malformed dates, missing required params) |
| 401 | Unauthorized | Invalid or missing API key |
| 403 | Forbidden | API key valid but lacks permission (expired subscription) |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | FMP server error (retry after delay) |

### Error Response Format

```json
{
    "Error Message": "Invalid API KEY. Please retry or visit our documentation to create one FREE https://financialmodelingprep.com/developer/docs"
}
```

### Common Errors

**Invalid API Key:**
```json
{"Error Message": "Invalid API KEY..."}
```
**Solution:** Verify API key is correct, active subscription

**Date Range Too Large:**
```json
{"Error Message": "Maximum date range is 90 days"}
```
**Solution:** Reduce date range to 90 days or less

**Rate Limit Exceeded:**
- HTTP 429 response
**Solution:** Wait before next request, upgrade subscription tier

## Best Practices

### 1. Respect Rate Limits

Implement exponential backoff for retries:
```python
import time

def fetch_with_retry(url, params, max_retries=3):
    for attempt in range(max_retries):
        response = requests.get(url, params=params)
        if response.status_code == 429:
            wait_time = 2 ** attempt  # Exponential backoff
            time.sleep(wait_time)
            continue
        return response
    raise Exception("Max retries exceeded")
```

### 2. Cache Results

Economic calendar data doesn't change frequently once released:
- Cache past events indefinitely (actual values don't change)
- Cache future events for 1-24 hours (estimates rarely change)
- Refresh cache after event release time passes

### 3. Efficient Date Ranges

- Query 7-30 day ranges to minimize API calls
- Don't query dates more than 3-6 months in future (sparse data)
- Use smaller ranges (1-7 days) for real-time monitoring

### 4. Handle Null Values

Many fields can be `null`, especially for future events:
```python
event_value = event.get("actual") or event.get("estimate") or event.get("previous")
if event_value is None:
    print("No value available for this event")
```

### 5. Time Zone Awareness

All API times are UTC:
```python
from datetime import datetime, timezone

utc_time = datetime.strptime(event["date"], "%Y-%m-%d %H:%M:%S")
utc_time = utc_time.replace(tzinfo=timezone.utc)

# Convert to local timezone
local_time = utc_time.astimezone()
```

## Data Accuracy and Timeliness

### Release Time Accuracy

- Most release times accurate within ±1 minute
- Delayed releases possible (technical issues, holidays)
- Times may shift due to daylight saving time changes

### Data Revisions

Economic data is often revised:
- **Preliminary:** First release (most market impact)
- **Revised:** 1-2 months later
- **Final:** 2-3 months later

The API `previous` field reflects the latest revised value, not necessarily the original preliminary release.

### Coverage

FMP Economic Calendar covers:
- **Major Economies:** US, EU, UK, Japan, China, Canada, Australia
- **Event Types:**
  - Employment data (NFP, unemployment rate)
  - Inflation (CPI, PPI, PCE)
  - Growth (GDP, retail sales, industrial production)
  - Central bank decisions (FOMC, ECB, BOJ, BOE)
  - Surveys (PMI, consumer confidence, sentiment indices)
  - Trade data (trade balance, exports/imports)
  - Housing data (starts, permits, sales)

## Comparison with Other Sources

| Feature | FMP API | Forex Factory | Investing.com |
|---------|---------|---------------|---------------|
| API Access | Yes | No (scraping only) | No (scraping only) |
| Historical Data | Yes | Limited | Yes (web only) |
| Free Tier | Yes (250/day) | N/A | N/A |
| Data Format | JSON | HTML | HTML |
| Reliability | High | Medium (changes) | Medium (changes) |

FMP is a reliable, legitimate API source compared to scraping financial calendar websites (which violates ToS and is fragile).

## Support and Documentation

- **Official Docs:** https://financialmodelingprep.com/developer/docs/economic-calendar-api
- **API Status:** https://status.financialmodelingprep.com
- **Support:** support@financialmodelingprep.com
- **Community:** Active Discord and forum for FMP users


---

## SKILL: economic-calendar-fetcher

- Fuente: `tradermonty/claude-trading-skills` → `skills/economic-calendar-fetcher` (MIT)
- Cuándo usarla: Fetch upcoming economic events and data releases using FMP API. Retrieve scheduled central bank decisions, employment reports, inflation data, GDP releases, and other market-moving economic indicators for specified date ranges (default: next 7 days). The script outputs raw JSON or text; the assistant filters, assesses impact, and generates the Markdown report.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/economic-calendar-fetcher/` (requirements.txt, fmp_client.py, get_economic_calendar.py)

# Economic Calendar Fetcher

## Overview

Retrieve upcoming economic events and data releases from the Financial Modeling Prep (FMP) Economic Calendar API. This skill fetches scheduled economic indicators including central bank monetary policy decisions, employment reports, inflation data (CPI/PPI), GDP releases, retail sales, manufacturing data, and other market-moving events that impact financial markets.

The skill uses a Python script to query the FMP API and returns raw JSON or text output. The assistant then filters events, assesses market impact, and generates a chronological Markdown report for each scheduled event. No files are generated automatically.

**Key Capabilities:**
- Fetch economic events for specified date ranges (max 90 days)
- Support flexible API key provision (environment variable or CLI argument)
- Filter by impact level, country, or event type (filtering performed by the assistant)
- Present filtered results as structured Markdown reports with impact analysis (assistant-generated, not script-generated)
- Default to next 7 days for quick market outlook

**Data Source:**
- FMP Economic Calendar API: `https://financialmodelingprep.com/stable/economic-calendar` (singular "economic")
- Covers major economies: US, EU, UK, Japan, China, Canada, Australia
- Event types: Central bank decisions, employment, inflation, GDP, trade, housing, surveys
- Note: the legacy `api/v3/economic_calendar` endpoint was fully retired by FMP on 2025-08-31 and now returns `403 Legacy Endpoint` — do not use it, including as a fallback.

## When to Use This Skill

Use this skill when the user requests:

1. **Economic Calendar Queries:**
   - "What economic events are coming up this week?"
   - "Show me the economic calendar for the next two weeks"
   - "When is the next FOMC meeting?"
   - "What major economic data is being released next month?"

2. **Market Event Planning:**
   - "What should I watch for in the markets this week?"
   - "Are there any high-impact economic releases coming?"
   - "When is the next jobs report / CPI release / GDP report?"

3. **Specific Date Range Requests:**
   - "Get economic events from January 1 to January 31"
   - "What's on the economic calendar for Q1 2025?"

4. **Country-Specific Queries:**
   - "Show me US economic data releases next week"
   - "What ECB events are scheduled?"
   - "When is Japan releasing their inflation data?"

**DO NOT use this skill for:**
- Past economic events (use market-news-analyst for historical analysis)
- Corporate earnings calendars (this skill excludes earnings)
- Real-time market data or live quotes
- Technical analysis or chart interpretation

## Prerequisites

- **FMP API Key** (required): Sign up at https://financialmodelingprep.com for a free key (250 requests/day). Set via `FMP_API_KEY` environment variable or pass `--api-key` to the script.
- **Python 3.10+**: Required to run `skills/economic-calendar-fetcher/scripts/get_economic_calendar.py`.
- **No third-party packages**: The script uses only the Python standard library.

## Workflow

Follow these steps to fetch and analyze the economic calendar:

### Step 1: Obtain FMP API Key

**Check for API key availability (in priority order):**

1. **Recommended:** Check if `FMP_API_KEY` environment variable is set — this keeps the key out of session logs
2. **Acceptable:** Use `--api-key` CLI argument for one-off runs
3. **Not recommended:** Asking the user to paste the key into chat — session logs may retain it
4. If user doesn't have an API key, provide instructions:
   - Visit https://financialmodelingprep.com
   - Sign up for free account (250 requests/day limit)
   - Navigate to API dashboard to obtain key

**Example user interaction:**
```
User: "Show me economic events for next week"
Assistant: "I'll fetch the economic calendar. I'll use the FMP_API_KEY environment variable if it's set. Otherwise, please pass the key via --api-key when running the script."
```

### Step 2: Determine Date Range

**Set appropriate date range based on user request:**

**Default (no specific dates):** Today + 7 days
**User specifies period:** Use exact dates (validate format: YYYY-MM-DD)
**Maximum range:** 90 days (FMP API limitation)

**Examples:**
- "Next week" → Today to +7 days
- "Next two weeks" → Today to +14 days
- "January 2025" → 2025-01-01 to 2025-01-31
- "Q1 2025" → 2025-01-01 to 2025-03-31

**Validate date range:**
- Ensure start date ≤ end date
- Ensure range ≤ 90 days
- Warn if querying past dates

### Step 3: Execute API Fetch Script

**Run the get_economic_calendar.py script with appropriate parameters:**

**Basic usage (default 7 days):**
```bash
python3 skills/economic-calendar-fetcher/scripts/get_economic_calendar.py --api-key YOUR_KEY
```

**With specific date range:**
```bash
python3 skills/economic-calendar-fetcher/scripts/get_economic_calendar.py \
  --from 2025-01-01 \
  --to 2025-01-31 \
  --api-key YOUR_KEY \
  --format json
```

**Using environment variable (no --api-key needed):**
```bash
export FMP_API_KEY=your_key_here
python3 skills/economic-calendar-fetcher/scripts/get_economic_calendar.py \
  --from 2025-01-01 \
  --to 2025-01-07
```

**Script parameters:**
- `--from`: Start date (YYYY-MM-DD) - default: today
- `--to`: End date (YYYY-MM-DD) - default: today + 7 days
- `--api-key`: FMP API key (optional if FMP_API_KEY env var set)
- `--format`: Output format (json or text) - default: json
- `--output`: Output file path (optional, default: stdout)

**Handle errors and empty results:**
- Invalid API key → Ask user to verify key
- Rate limit exceeded (429) → Suggest waiting or upgrading FMP tier
- Restricted endpoint (402 Payment Required) → The script raises a clear error stating the current FMP subscription tier does not include the Economic Calendar endpoint. Tell the user they need to upgrade their FMP plan at https://financialmodelingprep.com/ — do not treat this as "zero events" and do not fall back to the legacy v3 endpoint (it was retired 2025-08-31 and returns `403 Legacy Endpoint`).
- Network errors → Check your connection and re-run the script
- Invalid date format → Provide correct format example
- **Empty list `[]` for a plausible current/future range:** As of the current script version, an empty list from the API is a genuine "no events" response — a 404 or restricted-endpoint response now raises an explicit error instead of being silently converted to `[]`. If you still suspect missing data, re-verify the date range and API key rather than assuming a broken endpoint.

### Step 4: Parse and Filter Events

**Process the JSON response from the script:**

1. **Parse event data:** Extract all events from API response
2. **Apply user filters if specified:**
   - Impact level: "High", "Medium", "Low"
   - Country: "US", "EU", "JP", "CN", etc.
   - Event type: FOMC, CPI, Employment, GDP, etc.
   - Currency: USD, EUR, JPY, etc.

**Filter examples:**
- "Show only high-impact events" → Filter impact == "High"
- "US events only" → Filter country == "US"
- "Central bank decisions" → Search event name for "Rate", "Policy", "FOMC", "ECB", "BOJ"

**Event data structure:**
```json
{
  "date": "2025-01-15 14:30:00",
  "country": "US",
  "event": "Consumer Price Index (CPI) YoY",
  "currency": "USD",
  "previous": 2.6,
  "estimate": 2.7,
  "actual": null,
  "change": null,
  "impact": "High",
  "changePercentage": null
}
```

### Step 5: Assess Market Impact

**Evaluate the market significance of each event:**

**Impact Level Classification (from FMP):**
- **High Impact:** Major market-moving events
  - FOMC rate decisions, ECB/BOJ policy meetings
  - Non-Farm Payrolls (NFP), CPI, GDP
  - Market typically shows 0.5-2%+ intraday volatility

- **Medium Impact:** Significant but less volatile
  - Retail Sales, Industrial Production
  - PMI surveys, Consumer Confidence
  - Housing data, Durable Goods Orders

- **Low Impact:** Minor indicators
  - Weekly jobless claims (unless extreme)
  - Regional manufacturing surveys
  - Minor auction results

**Additional Context Factors:**

1. **Current Market Sensitivity:**
   - High inflation environment → CPI/PPI elevated importance
   - Recession fears → Employment data more critical
   - Rate cut speculation → Central bank meetings crucial

2. **Surprise Potential:**
   - Compare estimate vs. previous reading
   - Large expected changes = higher attention
   - Consensus uncertainty = higher impact potential

3. **Event Clustering:**
   - Multiple related events same day = amplified impact
   - Example: CPI + Retail Sales + Fed speech = Very High impact day

4. **Forward Significance:**
   - Does this event influence upcoming central bank decisions?
   - Is this a preliminary or final reading?
   - Will this data be revised?

### Step 6: Generate Output Report

> **Responsibility:** The script outputs raw JSON or text. This step is performed by the assistant using the script's output. No Markdown files are generated automatically; results are displayed in chat and can be saved to `reports/` on request.

**Create structured markdown report with the following sections:**

**Report Header:**
```markdown
# Economic Calendar
**Period:** [Start Date] to [End Date]
**Report Generated:** [Timestamp]
**Total Events:** [Count]
**High Impact Events:** [Count]
```

**Event Listing (Chronological):**

For each event, provide:

```markdown
## [Date] - [Day of Week]

### [Event Name] ([Impact Level])
- **Country:** [Country Code] ([Currency])
- **Time:** [HH:MM UTC]
- **Previous:** [Value]
- **Estimate:** [Consensus Forecast]
- **Impact Assessment:** [Your analysis]

**Market Implications:**
[2-3 sentences on why this matters, what markets watch for, typical reaction patterns]

---
```

**Example Event Entry:**

```markdown
## 2025-01-15 - Wednesday

### Consumer Price Index (CPI) YoY (High Impact)
- **Country:** US (USD)
- **Time:** 14:30 UTC (8:30 AM ET)
- **Previous:** 2.6%
- **Estimate:** 2.7%
- **Impact Assessment:** Very High - Core inflation metric for Fed policy decisions

**Market Implications:**
CPI reading above estimate (>2.7%) likely strengthens hawkish Fed expectations, potentially pressuring equities and supporting USD. Reading at or below 2.7% could reinforce disinflation narrative and support risk assets. Options market pricing 1.2% S&P 500 move on release day.

---
```

**Summary Section:**

Add analytical summary at the end:

```markdown
## Key Takeaways

**Highest Impact Days:**
- [Date]: [Events] - [Combined impact rationale]
- [Date]: [Events] - [Combined impact rationale]

**Central Bank Activity:**
- [Summary of any scheduled Fed/ECB/BOJ meetings or speeches]

**Major Data Releases:**
- Employment: [NFP, Unemployment Rate dates]
- Inflation: [CPI, PPI dates]
- Growth: [GDP, Retail Sales dates]

**Market Positioning Considerations:**
[2-3 bullets on how traders might position around these events]

**Risk Events:**
[Highlight any particularly high-uncertainty or surprise-potential events]
```

**Filtering Notes:**

If user requested specific filters, note at top:
```markdown
**Filters Applied:**
- Impact Level: High only
- Country: US
- Events shown: [X] of [Y] total events in date range
```

**Output:**
- Results are displayed in chat. No files are generated automatically.
- To save **raw JSON/text data**: use `--output reports/economic_calendar_[START]_to_[END].json` when running the script.
- To save the **Markdown report**: ask the assistant to write it to `reports/` after generating it in chat.

## Assistant-Generated Report Format

**Markdown structure requirements:**

1. **Chronological ordering:** Events sorted by date and time (earliest first)
2. **Impact level indicators:** Use (High Impact), (Medium Impact), (Low Impact) labels
3. **Time zone clarity:** Always specify UTC; ET/PT conversions are performed by the assistant based on US DST calendar
4. **Data completeness:** Include all available fields (previous, estimate, actual if past)
5. **Null handling:** Display "N/A" or "No estimate" for null values
6. **Impact assessment:** Every high/medium impact event must have market implications analysis

**Table format option (for dense listings):**

```markdown
| Date/Time (UTC) | Event | Country | Impact | Previous | Estimate | Assessment |
|-----------------|-------|---------|--------|----------|----------|------------|
| 01-15 14:30 | CPI YoY | US | High | 2.6% | 2.7% | Core inflation metric |
```

**Language:** All reports in English

## Resources

**Python Script:**
- `skills/economic-calendar-fetcher/scripts/get_economic_calendar.py`: Main API fetch script with CLI interface

**Reference Documentation:**
- `references/fmp_api_documentation.md`: Complete FMP Economic Calendar API reference
  - Authentication and API key management
  - Request parameters and date formats
  - Response field definitions
  - Rate limits and error handling
  - Best practices for caching and efficiency

**API Details:**
- Primary endpoint: `https://financialmodelingprep.com/stable/economic-calendar` (singular "economic" — the plural `economics-calendar` is a dead URL that 404s)
- Legacy endpoint retired: `https://financialmodelingprep.com/api/v3/economic_calendar` was shut down by FMP on 2025-08-31 and now returns `403 Legacy Endpoint`. Do not use it or fall back to it.
- Restricted-endpoint caveat: the stable Economic Calendar endpoint may require a paid FMP subscription tier. If the API key lacks entitlement, it returns `402 Payment Required`, which the script surfaces as a clear error rather than an empty list.
- Date-range caveat: responses can include rows just outside the requested `from`/`to` window; after fetching, filter events locally by parsed `date` so only the requested date range is reported.
- Authentication: API key required (free tier: 250 requests/day)
- Max date range: 90 days per request
- Response format: JSON array of event objects
- Rate limits: 5 requests/second (free tier)

**Event Coverage:**
- Major economies: US, EU, UK, Japan, China, Canada, Australia, Switzerland
- Event categories: Monetary policy, Employment, Inflation, GDP, Trade, Housing, Surveys
- Update frequency: Real-time (events added/updated as scheduled)
- Historical data: Available for past events with actual values

**Usage Tips:**
1. Cache results to minimize API calls (events rarely change once scheduled)
2. Query 7-30 day ranges for optimal request efficiency
3. Don't query >6 months in future (sparse data, speculative dates)
4. Refresh cache daily for upcoming week to catch time changes
5. Use smaller ranges (1-7 days) for real-time event monitoring

**Error Handling:**
- Malformed event rows, missing/renamed fields, changed types, invalid UTC event timestamps, and non-finite readings fail before formatting or opening the output file. Stderr contains `ZERO_RESULT_REASON=economic_calendar_schema_drift`; exit code is 1. Normal null readings are supported, and impact `"None"` is a valid provider string.
- An empty provider array is **unverified**, not proof that no events are scheduled: stderr contains `ZERO_RESULT_REASON=empty_calendar_unverified`; exit code is 1 and any existing output file is preserved. Check the provider/date window before writing a quiet-calendar report.
- Acquisition failures emit `ZERO_RESULT_REASON=calendar_fetch_failed` and exit 1. This includes HTTP/tier/network failures and the generated client's generic failure cases (HTTP-200 null or invalid JSON after its bounded retry). A non-null, non-array JSON response is schema drift. Error diagnostics redact API keys; they do not print malformed event values.
- API key errors: Clear user guidance for obtaining free key
- Rate limits (429): Suggest waiting or upgrading FMP tier; re-run the script after the wait
- Restricted endpoint (402): Script raises a clear error — the FMP subscription tier lacks access to this endpoint; direct the user to upgrade at https://financialmodelingprep.com/. Do not fall back to the legacy v3 endpoint (retired 2025-08-31, returns 403).
- Network failures: surface the clear ``Network error: ...`` message and re-run; single 429 retry, timeouts, and per-call rate limiting are handled by the vendored generated `fmp_client.py` (Issue #495)
- Genuine 404: The script now raises an error instead of silently returning an empty list — investigate rather than assuming zero events.
- Invalid dates: Validation with helpful error messages

### Referencia: references/fmp_api_documentation.md

# FMP Economic Calendar API Documentation

> **⚠️ Stale endpoint warning (2026-07-04):** This entire document, including every code example below, is written against the legacy `api/v3/economic_calendar` endpoint. FMP fully retired that endpoint on 2025-08-31 — it now returns `403 Legacy Endpoint`. The script (`scripts/get_economic_calendar.py`) uses the current endpoint, `https://financialmodelingprep.com/stable/economic-calendar` (singular "economic"), which may itself require a paid FMP tier (returns `402 Payment Required` otherwise). Treat the URLs and curl/Python snippets in this file as historical reference only, not as current instructions.

## Overview

The Financial Modeling Prep (FMP) Economic Calendar API provides access to upcoming and historical economic data releases, central bank decisions, and other market-moving events. This API enables traders and investors to stay informed about scheduled economic events that may impact financial markets.

## API Endpoint

```
https://financialmodelingprep.com/api/v3/economic_calendar
```

## Authentication

API access requires a valid FMP API key, which must be included as a query parameter in all requests.

**Parameter:** `apikey`
**Format:** String
**Required:** Yes

### Obtaining an API Key

1. Visit https://financialmodelingprep.com
2. Sign up for an account (free and paid tiers available)
3. Navigate to the API dashboard to view your API key
4. Free tier allows limited requests per day (~250-300 requests)
5. Paid tiers offer higher rate limits and additional features

## Request Parameters

### Required Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `from` | date | Start date for calendar period | `2025-01-01` |
| `to` | date | End date for calendar period | `2025-01-31` |
| `apikey` | string | Your FMP API key | `YOUR_API_KEY` |

### Date Format

- **Format:** `YYYY-MM-DD` (ISO 8601 date format)
- **Example:** `2025-07-20`
- **Maximum Range:** 90 days between `from` and `to` dates
- **Timezone:** All dates are in UTC

### Date Range Limitations

- Minimum range: 1 day
- Maximum range: 90 days
- Past dates: API returns historical events with actual values
- Future dates: API returns scheduled events with estimates (actual values will be null)

## Response Format

The API returns a JSON array of economic event objects.

### Response Structure

```json
[
    {
        "date": "2024-03-01 03:35:00",
        "country": "JP",
        "event": "3-Month Bill Auction",
        "currency": "JPY",
        "previous": -0.112,
        "estimate": null,
        "actual": -0.096,
        "change": 0.016,
        "impact": "Low",
        "changePercentage": 14.286
    }
]
```

### Response Fields

| Field | Type | Description | Nullable |
|-------|------|-------------|----------|
| `date` | string | Event date and time in UTC (format: `YYYY-MM-DD HH:MM:SS`) | No |
| `country` | string | ISO 2-letter country code (e.g., `US`, `JP`, `GB`, `EU`) | No |
| `event` | string | Name/description of the economic event | No |
| `currency` | string | ISO 3-letter currency code (e.g., `USD`, `EUR`, `JPY`) | No |
| `previous` | number | Previous reading/value for this indicator | Yes |
| `estimate` | number | Market consensus estimate/forecast | Yes |
| `actual` | number | Actual released value (null for future events) | Yes |
| `change` | number | Absolute change from previous reading | Yes |
| `impact` | string | Market impact level: `"High"`, `"Medium"`, `"Low"` | No |
| `changePercentage` | number | Percentage change from previous reading | Yes |

### Field Details

**`date`:**
- Format: `YYYY-MM-DD HH:MM:SS` in UTC timezone
- Represents the scheduled release time for the economic data
- For future events, this is the expected release time
- Times may be adjusted if releases are delayed

**`country`:**
- ISO 3166-1 alpha-2 country codes
- Special codes:
  - `EU`: European Union (ECB-related events)
  - `G7`: G7 summit/collaborative events
  - International organizations may use special codes

**`event`:**
- Descriptive name of the economic indicator or event
- Examples:
  - `"Non-Farm Payrolls"`
  - `"Consumer Price Index (CPI)"`
  - `"Federal Funds Rate Decision"`
  - `"GDP Growth Rate QoQ"`
  - `"Unemployment Rate"`

**`currency`:**
- ISO 4217 currency codes
- Indicates which currency's economy the event affects
- May differ from country (e.g., EU events affect EUR across multiple countries)

**`previous`:**
- The last reported value for this indicator
- Used as baseline for comparing current release
- May be revised from originally reported value
- `null` if no prior data available (new indicator)

**`estimate`:**
- Market consensus forecast compiled from analyst surveys
- Typically from Bloomberg, Reuters, or other consensus services
- `null` if no consensus exists or for less-watched indicators
- Comparing `actual` to `estimate` shows "surprise" factor

**`actual`:**
- The officially released value when data is published
- `null` for future events (not yet released)
- This is the critical field that moves markets when released
- May be revised in subsequent releases (preliminary → final revisions)

**`change`:**
- Calculated as: `actual - previous` (for past events)
- `null` if either `actual` or `previous` is null
- Sign indicates direction: positive = increase, negative = decrease
- Absolute value, not percentage

**`impact`:**
- Qualitative assessment of market-moving potential
- Three levels:
  - `"High"`: Major market-moving events (NFP, FOMC, CPI)
  - `"Medium"`: Significant but less volatile (Retail Sales, PMI)
  - `"Low"`: Minor indicators, routine data releases
- Determined by FMP based on historical volatility impact

**`changePercentage`:**
- Calculated as: `((actual - previous) / previous) * 100`
- `null` if either value is null or if `previous` is zero
- Percentage representation of the change
- Useful for comparing relative magnitude across different indicators

## Example Requests

### Fetch Events for Next 7 Days

```bash
curl "https://financialmodelingprep.com/api/v3/economic_calendar?from=2025-01-01&to=2025-01-07&apikey=YOUR_API_KEY"
```

### Fetch High-Impact Events Only (Post-Processing)

Note: API does not have an `impact` filter parameter, so filtering must be done after retrieval.

```python
import requests

response = requests.get(
    "https://financialmodelingprep.com/api/v3/economic_calendar",
    params={
        "from": "2025-01-01",
        "to": "2025-01-31",
        "apikey": "YOUR_API_KEY"
    }
)

events = response.json()
high_impact_events = [e for e in events if e["impact"] == "High"]
```

### Fetch Events for Specific Country (Post-Processing)

```python
us_events = [e for e in events if e["country"] == "US"]
eu_events = [e for e in events if e["country"] == "EU"]
```

## Rate Limits

Rate limits depend on your FMP subscription tier:

| Tier | Requests/Day | Requests/Second |
|------|--------------|-----------------|
| Free | 250 | 5 |
| Starter | 500 | 10 |
| Professional | 1,000+ | 20+ |

If you exceed rate limits, the API returns HTTP 429 (Too Many Requests).

## Error Handling

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | Success | Request successful, data returned |
| 400 | Bad Request | Invalid parameters (malformed dates, missing required params) |
| 401 | Unauthorized | Invalid or missing API key |
| 403 | Forbidden | API key valid but lacks permission (expired subscription) |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | FMP server error (retry after delay) |

### Error Response Format

```json
{
    "Error Message": "Invalid API KEY. Please retry or visit our documentation to create one FREE https://financialmodelingprep.com/developer/docs"
}
```

### Common Errors

**Invalid API Key:**
```json
{"Error Message": "Invalid API KEY..."}
```
**Solution:** Verify API key is correct, active subscription

**Date Range Too Large:**
```json
{"Error Message": "Maximum date range is 90 days"}
```
**Solution:** Reduce date range to 90 days or less

**Rate Limit Exceeded:**
- HTTP 429 response
**Solution:** Wait before next request, upgrade subscription tier

## Best Practices

### 1. Respect Rate Limits

Implement exponential backoff for retries:
```python
import time

def fetch_with_retry(url, params, max_retries=3):
    for attempt in range(max_retries):
        response = requests.get(url, params=params)
        if response.status_code == 429:
            wait_time = 2 ** attempt  # Exponential backoff
            time.sleep(wait_time)
            continue
        return response
    raise Exception("Max retries exceeded")
```

### 2. Cache Results

Economic calendar data doesn't change frequently once released:
- Cache past events indefinitely (actual values don't change)
- Cache future events for 1-24 hours (estimates rarely change)
- Refresh cache after event release time passes

### 3. Efficient Date Ranges

- Query 7-30 day ranges to minimize API calls
- Don't query dates more than 3-6 months in future (sparse data)
- Use smaller ranges (1-7 days) for real-time monitoring

### 4. Handle Null Values

Many fields can be `null`, especially for future events:
```python
event_value = event.get("actual") or event.get("estimate") or event.get("previous")
if event_value is None:
    print("No value available for this event")
```

### 5. Time Zone Awareness

All API times are UTC:
```python
from datetime import datetime, timezone

utc_time = datetime.strptime(event["date"], "%Y-%m-%d %H:%M:%S")
utc_time = utc_time.replace(tzinfo=timezone.utc)

# Convert to local timezone
local_time = utc_time.astimezone()
```

## Data Accuracy and Timeliness

### Release Time Accuracy

- Most release times accurate within ±1 minute
- Delayed releases possible (technical issues, holidays)
- Times may shift due to daylight saving time changes

### Data Revisions

Economic data is often revised:
- **Preliminary:** First release (most market impact)
- **Revised:** 1-2 months later
- **Final:** 2-3 months later

The API `previous` field reflects the latest revised value, not necessarily the original preliminary release.

### Coverage

FMP Economic Calendar covers:
- **Major Economies:** US, EU, UK, Japan, China, Canada, Australia
- **Event Types:**
  - Employment data (NFP, unemployment rate)
  - Inflation (CPI, PPI, PCE)
  - Growth (GDP, retail sales, industrial production)
  - Central bank decisions (FOMC, ECB, BOJ, BOE)
  - Surveys (PMI, consumer confidence, sentiment indices)
  - Trade data (trade balance, exports/imports)
  - Housing data (starts, permits, sales)

## Comparison with Other Sources

| Feature | FMP API | Forex Factory | Investing.com |
|---------|---------|---------------|---------------|
| API Access | Yes | No (scraping only) | No (scraping only) |
| Historical Data | Yes | Limited | Yes (web only) |
| Free Tier | Yes (250/day) | N/A | N/A |
| Data Format | JSON | HTML | HTML |
| Reliability | High | Medium (changes) | Medium (changes) |

FMP is a reliable, legitimate API source compared to scraping financial calendar websites (which violates ToS and is fragile).

## Support and Documentation

- **Official Docs:** https://financialmodelingprep.com/developer/docs/economic-calendar-api
- **API Status:** https://status.financialmodelingprep.com
- **Support:** support@financialmodelingprep.com
- **Community:** Active Discord and forum for FMP users


---

## SKILL: exposure-coach

- Fuente: `tradermonty/claude-trading-skills` → `skills/exposure-coach` (MIT)
- Cuándo usarla: Generate a one-page Market Posture summary with net exposure ceiling, growth-vs-value bias, participation breadth, and new-entry-allowed vs cash-priority recommendation by integrating signals from breadth, regime, and flow analysis skills.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/exposure-coach/` (requirements.txt, calculate_exposure.py, provenance_contract.py)

# Exposure Coach

## Overview

Exposure Coach synthesizes outputs from market-breadth-analyzer, uptrend-analyzer, macro-regime-detector, market-top-detector, ftd-detector, theme-detector, sector-analyst, and institutional-flow-tracker into a unified control-plane decision. The skill answers the solo trader's core question: "How much capital should I commit to equities right now?" before any individual stock analysis begins.

## When to Use

- Before initiating any new stock positions to determine appropriate capital commitment
- At the start of each trading week to calibrate portfolio exposure
- When multiple market signals conflict and a unified posture is needed
- After significant macro or market events to reassess exposure ceiling
- When transitioning between market regimes (broadening, concentration, contraction)

## Prerequisites

- Python 3.9+
- FMP API key (set `FMP_API_KEY` environment variable) for institutional-flow-tracker data
- Input JSON files from upstream skills (see Workflow Step 1)
- Standard library + `argparse`, `json`, `datetime`

## Workflow

### Step 1: Gather Upstream Skill Outputs

Collect the most recent JSON outputs from integrated skills. Each file provides a specific signal dimension:

| Skill | Output File Pattern | Signal Provided |
|-------|---------------------|-----------------|
| market-breadth-analyzer | `breadth_*.json` | Advance/decline ratios, new highs/lows |
| uptrend-analyzer | `uptrend_*.json` | Uptrend participation percentage |
| macro-regime-detector | `regime_*.json` | Current regime (Concentration, Broadening, etc.) |
| market-top-detector | `top_risk_*.json` | Distribution day count, top probability score |
| ftd-detector | `ftd_*.json` | Follow-Through Day quality (market bottom confirmation) |
| theme-detector | `theme_detector_*.json` or `theme_*.json` | Active investment themes and rotation |
| sector-analyst | `sector_*.json` | Sector performance rankings |
| institutional-flow-tracker | `institutional_*.json` | Net institutional buying/selling |

### Step 2: Run Exposure Scoring Engine

Execute the exposure scoring script with paths to upstream outputs:

```bash
python3 skills/exposure-coach/scripts/calculate_exposure.py \
  --breadth reports/breadth_latest.json \
  --uptrend reports/uptrend_latest.json \
  --regime reports/regime_latest.json \
  --top-risk reports/top_risk_latest.json \
  --ftd reports/ftd_latest.json \
  --theme reports/theme_latest.json \
  --sector reports/sector_latest.json \
  --institutional reports/institutional_latest.json \
  --output-dir reports/
```

The script accepts partial inputs; missing files reduce confidence but do not block execution.

Canonical macro-regime reports must include nested `regime.confidence` and
`composite.data_quality` with valid integer component counts. Missing or malformed
availability metadata, `very_low` confidence, and zero usable components are
treated as missing critical input. They do not contribute a regime score or bias,
and the normal missing-input haircut and confidence cap apply. Never override this
degradation by manually copying the report's regime label into the exposure decision.

**Verification pitfall:** After each run, inspect the generated JSON fields `inputs_provided` and `inputs_missing`. If a file you passed on the CLI still appears in `inputs_missing` (for example a theme-detector JSON that the exposure engine did not recognize), report the affected dimension as degraded and keep confidence capped; do not assume the supplied input was incorporated just because the CLI argument was present.

**Theme-detector ingestion caveat:** The theme detector commonly emits `theme_detector_YYYY-MM-DD_HHMMSS.json` with a `themes` object. If that file is not recognized by `calculate_exposure.py` and `theme` remains in `inputs_missing`, do not fold theme strength into the exposure ceiling manually. Instead, keep the Exposure Coach confidence capped, state that the theme dimension was not incorporated, and summarize theme/sector findings separately in the broader trading brief.

### Step 3: Interpret the Market Posture Summary

Review the generated posture report containing:

1. **Exposure Ceiling** -- Maximum recommended equity allocation (0-100%)
2. **Bias Direction** -- Growth vs Value tilt based on regime and flow
3. **Participation Assessment** -- Broad (healthy) vs Narrow (fragile) market
4. **Action Recommendation** -- NEW_ENTRY_ALLOWED, REDUCE_ONLY, or CASH_PRIORITY
5. **Confidence Level** -- HIGH, MEDIUM, or LOW based on input completeness

### Step 4: Apply Exposure Guidance

Map the posture recommendation to portfolio actions:

| Recommendation | Action |
|----------------|--------|
| NEW_ENTRY_ALLOWED | Proceed with stock-level analysis and new positions |
| REDUCE_ONLY | No new entries; trim existing positions on strength |
| CASH_PRIORITY | Raise cash aggressively; avoid all new commitments |

## Output Format

### JSON Report

```json
{
  "schema_version": "1.0",
  "generated_at": "2026-03-16T07:00:00Z",
  "exposure_ceiling_pct": 70,
  "bias": "GROWTH",
  "participation": "BROAD",
  "recommendation": "NEW_ENTRY_ALLOWED",
  "confidence": "HIGH",
  "component_scores": {
    "breadth_score": 65,
    "uptrend_score": 72,
    "regime_score": 80,
    "top_risk_score": 25,
    "ftd_score": 10,
    "theme_score": 68,
    "sector_score": 70,
    "institutional_score": 75
  },
  "inputs_provided": ["breadth", "uptrend", "regime", "top_risk"],
  "inputs_missing": ["ftd", "theme", "sector", "institutional"],
  "rationale": "Broad participation with low top risk supports elevated exposure."
}
```

### Markdown Report

The markdown report provides a one-page summary suitable for quick review:

```markdown
# Market Posture Summary
**Date:** 2026-03-16 | **Confidence:** HIGH

## Exposure Ceiling: 70%

| Dimension | Score | Status |
|-----------|-------|--------|
| Breadth | 65 | Healthy |
| Uptrend Participation | 72% | Broad |
| Regime | Broadening | Favorable |
| Top Risk | 25 | Low |

## Recommendation: NEW_ENTRY_ALLOWED

**Bias:** Growth > Value
**Participation:** Broad (healthy internals)

### Rationale
Broad participation with low distribution day count supports elevated equity exposure.
New positions allowed within the 70% ceiling.
```

Reports are saved to `reports/` with filenames `exposure_posture_YYYY-MM-DD_HHMMSS.{json,md}`.

## Resources

- `scripts/calculate_exposure.py` -- Main orchestrator that scores and synthesizes inputs
- `references/exposure_framework.md` -- Scoring rules and threshold definitions
- `references/regime_exposure_map.md` -- Regime-to-exposure ceiling mappings

## Key Principles

1. **Safety First** -- Default to lower exposure when inputs are incomplete or conflicting
2. **Regime Alignment** -- Let macro regime set the baseline; breadth adjusts within bounds
3. **Actionable Output** -- Always produce a clear recommendation, not just data aggregation

## Strict provenance for market-regime-daily

Add `--require-provenance --run-id daily-20261017-unique
--as-of 2026-10-17T13:00:00Z --max-age-days 3` to validate breadth and uptrend
before scoring. Both producers must receive the same unique run ID; pass their
exact printed JSON paths. `--as-of` is the timezone-aware evaluation instant,
not an override of the source business date.

The gate checks schema 1.0, expected run ID, UTC retrieval no later than evaluation,
nonfuture source date and configured age. Default three calendar days is a
conservative policy, not an exchange holiday calendar. Failure stops before
report output. Successful output records accepted lineage and verification limits.
Optional top-risk/other inputs and auxiliary summary dates remain outside this
gate; unknown quality flags stay false. Legacy mode retains its existing schema.
Run IDs are consistency markers, not authenticity or point-in-time proof.

### Referencia: references/exposure_framework.md

# Exposure Framework

## Overview

This document defines the scoring rules and threshold logic used by the Exposure Coach to synthesize multiple market signals into a unified exposure recommendation.

## Component Scoring (0-100 Scale)

Each input dimension is normalized to a 0-100 score where:
- **0-30**: Bearish / Risk-off signal
- **31-50**: Cautious / Neutral-bearish
- **51-70**: Neutral-bullish / Constructive
- **71-100**: Bullish / Risk-on signal

### Breadth Score

Derived from advance/decline ratios and new highs vs new lows:

| A/D Ratio (10-day) | NH/NL Ratio | Breadth Score |
|-------------------|-------------|---------------|
| > 1.5 | > 3.0 | 80-100 |
| 1.0 - 1.5 | 1.0 - 3.0 | 50-79 |
| 0.7 - 1.0 | 0.5 - 1.0 | 30-49 |
| < 0.7 | < 0.5 | 0-29 |

### Uptrend Score

Direct mapping from uptrend participation percentage:

| Uptrend % | Score |
|-----------|-------|
| > 50% | 75-100 |
| 35-50% | 50-74 |
| 20-35% | 30-49 |
| < 20% | 0-29 |

### Regime Score

Based on macro-regime-detector output:

| Regime | Score | Rationale |
|--------|-------|-----------|
| Broadening | 80 | Healthy expansion; rising tide lifts all boats |
| Concentration | 60 | Narrow leadership; selective opportunities |
| Transitional | 50 | Uncertainty; reduce commitment |
| Inflationary | 40 | Rotation stress; defensive posture |
| Contraction | 20 | Risk-off; preserve capital |

### Top Risk Score (Inverted)

Higher distribution day counts and top probability → lower score:

| Distribution Days | Top Probability | Score |
|-------------------|-----------------|-------|
| 0-2 | < 20% | 80-100 |
| 3-4 | 20-40% | 50-79 |
| 5-6 | 40-60% | 30-49 |
| 7+ | > 60% | 0-29 |

### FTD Score (Inverted)

High failure-to-deliver anomalies indicate stress:

| FTD Anomaly Level | Score |
|-------------------|-------|
| None / Low | 80-100 |
| Moderate | 50-79 |
| Elevated | 30-49 |
| Critical | 0-29 |

### Theme Score

Based on theme strength and rotation patterns:

| Theme Status | Score |
|--------------|-------|
| Strong, expanding | 80-100 |
| Stable | 50-79 |
| Rotating / Churning | 30-49 |
| Collapsing | 0-29 |

### Sector Score

Based on sector performance dispersion and leadership quality:

| Sector Condition | Score |
|------------------|-------|
| Broad strength, low dispersion | 80-100 |
| Mixed with clear leaders | 50-79 |
| High dispersion, defensive leading | 30-49 |
| Broad weakness | 0-29 |

### Institutional Score

Net institutional buying/selling trend:

| Flow Direction | Score |
|----------------|-------|
| Strong net buying | 80-100 |
| Mild net buying | 50-79 |
| Neutral / Mixed | 30-49 |
| Net selling | 0-29 |

## Composite Calculation

### Weighted Average

The composite score uses these weights:

| Component | Weight | Rationale |
|-----------|--------|-----------|
| Regime | 25% | Sets the macro baseline |
| Top Risk | 20% | Critical for downside protection |
| Breadth | 15% | Market health indicator |
| Uptrend | 15% | Participation confirmation |
| Institutional | 10% | Smart money signal |
| Sector | 5% | Rotation context |
| Theme | 5% | Thematic momentum |
| FTD | 5% | Stress indicator |

### Missing Input Handling

When inputs are missing:
1. Exclude missing components from weighted average
2. Reduce confidence level proportionally
3. Apply a 10% haircut per missing critical input (Regime, Top Risk, Breadth)

## Exposure Ceiling Mapping

| Composite Score | Exposure Ceiling |
|-----------------|------------------|
| 80-100 | 90-100% |
| 65-79 | 70-89% |
| 50-64 | 50-69% |
| 35-49 | 30-49% |
| 20-34 | 10-29% |
| 0-19 | 0-9% |

## Recommendation Logic

### NEW_ENTRY_ALLOWED
- Composite score >= 50
- Top risk score >= 40
- No critical inputs missing

### REDUCE_ONLY
- Composite score 30-49, OR
- Top risk score 25-39, OR
- 2+ critical inputs missing

### CASH_PRIORITY
- Composite score < 30, OR
- Top risk score < 25, OR
- Regime = Contraction with top risk score < 50

## Bias Determination

### Growth Bias
- Regime = Broadening or Concentration
- Theme score > 60
- Sector shows technology/growth leadership

### Value Bias
- Regime = Inflationary
- Sector shows financials/energy/materials leadership
- Institutional flow favoring value sectors

### Neutral Bias
- Conflicting signals or transitional regime
- Balanced sector performance

## Participation Assessment

### Broad Participation
- Uptrend score >= 50
- Breadth score >= 50
- Low sector dispersion

### Narrow Participation
- Uptrend score < 50
- Breadth score < 50 OR high sector dispersion
- Few sectors carrying the market

## Confidence Levels

| Condition | Confidence |
|-----------|------------|
| 6+ inputs provided, no conflicts | HIGH |
| 4-5 inputs provided OR minor conflicts | MEDIUM |
| < 4 inputs OR major conflicts | LOW |

### Referencia: references/regime_exposure_map.md

# Regime-to-Exposure Mapping

## Overview

This document maps macro regime states to baseline exposure ceilings and bias recommendations. The macro regime provides the foundational context; other signals adjust within these bounds.

## Regime Definitions

### Broadening
**Characteristics:**
- RSP/SPY ratio rising (equal-weight outperforming cap-weight)
- Uptrend participation > 40%
- Multiple sectors contributing to gains
- Credit spreads stable or tightening

**Baseline Exposure:** 80-100%
**Bias:** Growth-tilted
**Action:** Aggressive new entries allowed

### Concentration
**Characteristics:**
- RSP/SPY ratio falling (mega-caps dominating)
- Uptrend participation 25-40%
- Leadership in few sectors (Technology, Communications)
- Narrow breadth despite index gains

**Baseline Exposure:** 60-80%
**Bias:** Quality Growth
**Action:** Selective entries in leaders only

### Transitional
**Characteristics:**
- Cross-asset signals conflicting
- Regime indicators at boundary conditions
- High volatility in breadth measures
- Sector rotation accelerating

**Baseline Exposure:** 40-60%
**Bias:** Neutral / Defensive
**Action:** Reduce new entries; hold quality positions

### Inflationary
**Characteristics:**
- Yield curve steepening
- Commodity strength (especially energy, metals)
- Value outperforming growth
- Real assets leading

**Baseline Exposure:** 50-70%
**Bias:** Value / Real Assets
**Action:** Rotate to inflation beneficiaries

### Contraction
**Characteristics:**
- Distribution days accumulating
- Uptrend participation < 20%
- Defensive sectors (Utilities, Staples, Healthcare) leading
- Credit spreads widening
- Institutional selling detected

**Baseline Exposure:** 10-30%
**Bias:** Defensive / Cash
**Action:** CASH_PRIORITY; protect capital

## Regime Transition Signals

### Broadening → Concentration
- RSP/SPY rolling over while SPY makes new highs
- Breadth divergence (fewer stocks at highs)
- Reduce exposure ceiling by 10-20%

### Concentration → Transitional
- Mega-cap leaders showing distribution
- Volatility expansion
- Reduce exposure ceiling by 15-25%

### Transitional → Contraction
- Credit spreads widening
- Safe haven flows (bonds, gold, yen)
- Reduce exposure ceiling by 25-40%

### Contraction → Transitional
- Distribution day count resetting
- Breadth thrusts
- Begin rebuilding exposure cautiously

### Transitional → Broadening
- RSP/SPY ratio turning up
- Uptrend participation expanding
- Aggressive exposure increase warranted

## Exposure Adjustment Rules

### Within-Regime Adjustments

Even within a regime, the exposure ceiling adjusts based on:

1. **Breadth Confirmation**
   - Breadth score aligning with regime: No adjustment
   - Breadth diverging negatively: -10% to ceiling
   - Breadth diverging positively: +5% to ceiling

2. **Top Risk Level**
   - Low top risk: +10% to ceiling
   - Elevated top risk: -15% to ceiling
   - Critical top risk: Force CASH_PRIORITY regardless of regime

3. **Institutional Flow**
   - Strong buying: +5% to ceiling
   - Strong selling: -10% to ceiling

4. **FTD Anomalies**
   - Critical FTD level: -15% to ceiling
   - Forces extra caution on new entries

## Bias-to-Sector Mapping

| Bias | Favored Sectors | Avoid Sectors |
|------|-----------------|---------------|
| Growth | Technology, Consumer Discretionary, Communications | Utilities, Staples |
| Value | Financials, Energy, Industrials, Materials | High-multiple Growth |
| Defensive | Utilities, Healthcare, Staples | Cyclicals |
| Quality | Stable Earnings, Strong Balance Sheets | Speculative, High Debt |

## Example Scenarios

### Scenario 1: Early Bull Market
- Regime: Broadening
- Breadth: Strong (score 85)
- Top Risk: Low (score 90)
- Uptrend: Expanding (score 80)

**Result:**
- Exposure Ceiling: 95%
- Bias: Growth
- Recommendation: NEW_ENTRY_ALLOWED

### Scenario 2: Late Cycle Concentration
- Regime: Concentration
- Breadth: Weak (score 45)
- Top Risk: Moderate (score 55)
- Uptrend: Narrow (score 35)

**Result:**
- Exposure Ceiling: 55%
- Bias: Quality Growth
- Recommendation: REDUCE_ONLY

### Scenario 3: Market Top Formation
- Regime: Transitional
- Breadth: Deteriorating (score 30)
- Top Risk: High (score 25)
- Uptrend: Collapsing (score 18)

**Result:**
- Exposure Ceiling: 15%
- Bias: Defensive
- Recommendation: CASH_PRIORITY

## Integration with Other Signals

The regime provides the framework; other signals fine-tune:

1. **Theme Detector** -- Identifies which themes to favor within bias
2. **Sector Analyst** -- Confirms sector leadership alignment
3. **Institutional Flow** -- Validates smart money direction
4. **FTD Detector** -- Flags systemic stress

When signals conflict:
- Default to more conservative posture
- Reduce confidence level
- Flag conflicts in rationale


---

## SKILL: ftd-detector

- Fuente: `tradermonty/claude-trading-skills` → `skills/ftd-detector` (MIT)
- Cuándo usarla: Detects Follow-Through Day (FTD) signals for market bottom confirmation using William O'Neil's methodology. Dual-index tracking (S&P 500 + NASDAQ) with state machine for rally attempt, FTD qualification, and post-FTD health monitoring. Use when user asks about market bottom signals, follow-through days, rally attempts, re-entry timing after corrections, or whether it's safe to increase equity exposure. Complementary to market-top-detector (defensive) - this skill is offensive (bottom confirmation).
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/ftd-detector/` (requirements.txt, fmp_client.py, ftd_detector.py, post_ftd_monitor.py, rally_tracker.py, report_generator.py)

# FTD Detector Skill

## Purpose

Detect Follow-Through Day (FTD) signals that confirm a market bottom, using William O'Neil's proven methodology. Generates a quality score (0-100) with exposure guidance for re-entering the market after corrections.

**Complementary to Market Top Detector:**
- Market Top Detector = defensive (detects distribution, rotation, deterioration)
- FTD Detector = offensive (detects rally attempts, bottom confirmation)

## When to Use This Skill

**English:**
- User asks "Is the market bottoming?" or "Is it safe to buy again?"
- User observes a market correction (3%+ decline) and wants re-entry timing
- User asks about Follow-Through Days or rally attempts
- User wants to assess if a recent bounce is sustainable
- User asks about increasing equity exposure after a correction
- Market Top Detector shows elevated risk and user wants bottom signals

**Japanese:**
- 「底打ちした？」「買い戻して良い？」
- 調整局面（3%以上の下落）からのエントリータイミング
- フォロースルーデーやラリーアテンプトについて
- 直近の反発が持続可能か評価したい
- 調整後のエクスポージャー拡大の判断
- Market Top Detectorが高リスク表示の後の底打ちシグナル確認

## Difference from Market Top Detector

| Aspect | FTD Detector | Market Top Detector |
|--------|-------------|-------------------|
| Focus | Bottom confirmation (offensive) | Top detection (defensive) |
| Trigger | Market correction (3%+ decline) | Market at/near highs |
| Signal | Rally attempt → FTD → Re-entry | Distribution → Deterioration → Exit |
| Score | 0-100 FTD quality | 0-100 top probability |
| Action | When to increase exposure | When to reduce exposure |

---

## Execution Workflow

### Phase 1: Execute Python Script

Run the FTD detector script:

```bash
python3 skills/ftd-detector/scripts/ftd_detector.py --api-key $FMP_API_KEY
```

The script will:
1. Fetch S&P 500 and QQQ historical data (60+ trading days) from FMP API
2. Fetch current quotes for both indices
3. Run dual-index state machine (correction → rally → FTD detection)
4. Assess post-FTD health (distribution days, invalidation, power trend)
5. Calculate quality score (0-100)
6. Generate JSON and Markdown reports

**API Budget:** 4 calls (well within free tier of 250/day)

### Phase 2: Present Results

Present the generated Markdown report to the user, highlighting:
- Current market state (correction, rally attempt, FTD confirmed, etc.)
- Quality score and signal strength
- Recommended exposure level
- Key watch levels (swing low, FTD day low)
- Post-FTD health (distribution days, power trend)

### Phase 3: Contextual Guidance

Based on the market state, provide additional guidance:

**If FTD Confirmed (score 60+):**
- Suggest looking at leading stocks in proper bases
- Reference CANSLIM screener for candidate stocks
- Remind about position sizing and stops

**If Rally Attempt (Day 1-3):**
- Advise patience, do not buy ahead of FTD
- Suggest building watchlists

**If No Correction:**
- FTD analysis is not applicable in uptrend
- Redirect to Market Top Detector for defensive signals

---

## State Machine

```
NO_SIGNAL → CORRECTION → RALLY_ATTEMPT → FTD_WINDOW → FTD_CONFIRMED
                ↑              ↓               ↓              ↓
                └── RALLY_FAILED ←─────────────┘     FTD_INVALIDATED
```

| State | Definition |
|-------|-----------|
| NO_SIGNAL | Uptrend, no qualifying correction |
| CORRECTION | 3%+ decline with 3+ down days |
| RALLY_ATTEMPT | Day 1-3 of rally from swing low |
| FTD_WINDOW | Day 4-10, waiting for qualifying FTD |
| FTD_CONFIRMED | Valid FTD signal detected |
| RALLY_FAILED | Rally broke below swing low |
| FTD_INVALIDATED | Close below FTD day's low |

## Quality Score (0-100)

| Score | Signal | Exposure |
|-------|--------|----------|
| 80-100 | Strong FTD | 75-100% |
| 60-79 | Moderate FTD | 50-75% |
| 40-59 | Weak FTD | 25-50% |
| <40 | No FTD / Failed | 0-25% |

---

## Prerequisites

- **FMP API Key:** Required. Set `FMP_API_KEY` environment variable or pass via `--api-key` flag.
- **Python 3.9+:** With `requests` library installed.
- **API Budget:** 4 calls per execution (well within FMP free tier of 250/day).

## Output Files

- JSON: `ftd_detector_YYYY-MM-DD_HHMMSS.json`
- Markdown: `ftd_detector_YYYY-MM-DD_HHMMSS.md`

## Reference Documents

### `skills/ftd-detector/references/ftd_methodology.md`
- O'Neil's FTD rules in detail
- Rally attempt mechanics and day counting
- Historical FTD examples (2020 March, 2022 October)

### `skills/ftd-detector/references/post_ftd_guide.md`
- Post-FTD distribution day failure rates
- Power Trend definition and conditions
- Success vs failure pattern comparison

### When to Load References
- **First use:** Load `skills/ftd-detector/references/ftd_methodology.md` for full understanding
- **Post-FTD questions:** Load `skills/ftd-detector/references/post_ftd_guide.md`
- **Regular execution:** References not needed - script handles analysis

### Referencia: references/ftd_methodology.md

# Follow-Through Day (FTD) Methodology

## Overview

The Follow-Through Day (FTD) is William O'Neil's market timing signal for confirming a new uptrend after a correction. It is the **single most important signal** for re-entering the market after a decline. Without an FTD, no new bull market or sustained rally has ever begun (per IBD historical analysis).

**Key Insight:** FTD is a necessary but not sufficient condition. Historically, approximately 25% of FTDs lead to sustained uptrends. The remaining 75% fail, which is why quality scoring and post-FTD monitoring are critical.

---

## Step 1: Identify the Correction

### Qualifying Correction
A correction must meet these criteria before FTD analysis begins:

- **Decline magnitude:** Index closes 3% or more below its recent high
- **Duration:** At least 3 down days during the decline
- **Index scope:** S&P 500 and/or NASDAQ Composite (either suffices)

### Swing Low Definition
The swing low is the lowest closing price during the correction that becomes the reference point for the rally attempt:

- Must be preceded by 3%+ decline from a recent high (within 40 trading days)
- Must have at least 3 down days between the high and the low
- Must be a local minimum (adjacent days have higher closes)
- Multiple swing lows can occur; use the most recent qualifying one

**Important:** The swing low is determined by *closing price*, not intraday low.

---

## Step 2: Rally Attempt (Day 1-3)

### Day 1 Detection
Day 1 marks the beginning of a rally attempt. It occurs on the **first qualifying up day** after the swing low:

**Primary criterion:** Close > Previous day's close (up day)

**Alternative criterion:** Close in the top 50% of the day's price range
- Formula: (Close - Low) / (High - Low) >= 0.50
- This captures days where the market recovers significantly from intraday lows even if it doesn't close above the prior day's close

### Day 2-3 Integrity Check
For the rally attempt to remain valid through Day 2-3:

- **Close must not breach Day 1's intraday low** (not the close, the *low*)
- This is a strict rule; even a single day closing below Day 1's low invalidates the attempt
- Day 2 and Day 3 do NOT need to be up days; they just cannot close below Day 1's low

### Rally Invalidation (Reset)
The rally attempt resets completely if:

1. **Any day's close falls below the swing low price** → Start over from new potential swing low
2. **Day 2 or Day 3 closes below Day 1's intraday low** → Wait for new Day 1

When a rally resets, the new lower price may become the new swing low, and the cycle begins again.

---

## Step 3: FTD Window (Day 4-10)

### FTD Qualification Criteria
A Follow-Through Day must satisfy ALL of these conditions:

1. **Day 4-10** of the rally attempt (Day 4-7 is the prime window; Day 8-10 still valid)
2. **Price gain >= 1.25%** (minimum threshold)
   - 1.25-1.49%: Minimum qualifying gain
   - 1.50-1.99%: Recommended gain (higher reliability)
   - 2.00%+: Strong signal
3. **Volume > previous day's volume** (mandatory)
   - This confirms institutional participation
   - Volume does not need to exceed the 50-day average, though it's a positive if it does

### Day Counting Rules
- Day 1 = first qualifying up day after swing low
- Day 2, 3, etc. = every subsequent trading day (regardless of whether it's up or down)
- Days count continues as long as the rally is not invalidated
- The FTD itself must be an up day meeting the gain and volume requirements

### Prime vs Late Window

**Day 4-7 (Prime):**
- Historically higher success rate
- Base quality score: 60 points
- Institutional buyers are more likely to have conviction

**Day 8-10 (Late):**
- Still valid but statistically weaker
- Base quality score: 50 points
- May indicate hesitant institutional buying

**After Day 10:**
- No longer qualifies as a traditional FTD
- Rally without FTD by Day 10 is a warning sign
- May still develop into an uptrend but reliability drops significantly

---

## Step 4: Dual-Index Confirmation

### Single-Index FTD
An FTD on either the S&P 500 or NASDAQ is sufficient to trigger the signal. The signal is actionable on a single-index confirmation.

### Dual-Index FTD
When both S&P 500 and NASDAQ produce FTDs (within a few days of each other):
- Significantly higher reliability
- Quality score bonus: +15 points
- Indicates broader institutional conviction
- Both growth and value participants are buying

### Index Discrepancy
When one index confirms FTD but the other is still in rally attempt or correction:
- FTD is still valid from the confirming index
- Monitor the lagging index for convergence or divergence
- Divergence (one fails while other holds) is a cautionary signal

---

## Quality Score Framework

### Score Components (0-100)

| Factor | Criteria | Points |
|--------|----------|--------|
| **Base (FTD Day)** | Day 4-7 | 60 |
| | Day 8-10 | 50 |
| **Price Gain** | >= 2.0% | +15 |
| | >= 1.5% | +10 |
| | >= 1.25% | +5 |
| **Volume vs 50-day Avg** | Above average | +10 |
| | Below average | +0 |
| **Dual Index Confirm** | Both S&P 500 + NASDAQ | +15 |
| | Single index | +0 |
| **Post-FTD Health** | No distribution (5 days) | +10 |
| | Distribution Day 4-5 | -5 |
| | Distribution Day 3 | -15 |
| | Distribution Day 1-2 | -30 |

### Interpretation

| Score | Signal | Recommended Exposure |
|-------|--------|---------------------|
| 80-100 | Strong FTD | 75-100% equity |
| 60-79 | Moderate FTD | 50-75% equity |
| 40-59 | Weak FTD | 25-50% equity |
| < 40 | No FTD / Failed | 0-25% equity |

---

## Historical FTD Examples

### March 2020 (COVID Crash)
- **Swing Low:** March 23, 2020 (S&P 500: ~2,237)
- **Day 1:** March 24, 2020 (+9.4%)
- **FTD:** April 2, 2020 (Day 8 of rally, +2.3% on higher volume)
- **Outcome:** Successful - began one of the strongest bull markets in history
- **Quality:** Moderate (Day 8 = late window, but strong gain and volume)
- **Note:** Multiple failed rally attempts preceded this successful one

### October 2022 (Bear Market Bottom)
- **Swing Low:** October 13, 2022 (S&P 500: ~3,491)
- **Day 1:** October 14, 2022 (+2.6%)
- **FTD:** October 21, 2022 (Day 6, +2.4% on higher volume)
- **Outcome:** Successful - confirmed the end of the 2022 bear market
- **Quality:** High (Day 6 = prime window, strong gain, above-avg volume)

### June 2022 (Failed FTD)
- **Swing Low:** June 17, 2022 (S&P 500: ~3,666)
- **FTD:** Late June 2022
- **Outcome:** Failed - market made new lows by September 2022
- **Lesson:** FTD occurred but distribution days followed quickly; market environment (rising rates, inflation) was hostile

### December 2018 (Christmas Eve Low)
- **Swing Low:** December 24, 2018 (S&P 500: ~2,351)
- **FTD:** January 4, 2019 (Day 6, +3.4% on higher volume)
- **Outcome:** Successful - powerful rally through 2019
- **Quality:** Very high (prime window, strong gain, Fed pivot as catalyst)

---

## Common Mistakes

1. **Buying before FTD confirmation:** Acting on Day 1-3 before FTD is confirmed
2. **Ignoring volume:** A large gain without volume increase is NOT an FTD
3. **Counting wrong:** Including non-trading days or resetting day count incorrectly
4. **Single vs. dual index:** Treating single-index FTD as equivalent to dual-index
5. **Ignoring post-FTD distribution:** Not monitoring for early distribution days
6. **FTD ≠ all clear:** Treating FTD as guarantee rather than probability shift

### Referencia: references/post_ftd_guide.md

# Post-FTD Monitoring Guide

## Overview

A confirmed Follow-Through Day (FTD) shifts the probability toward a new uptrend, but approximately 75% of FTDs ultimately fail. Post-FTD monitoring is essential for:
1. Confirming the signal is working (exposure increase)
2. Detecting early failure (exposure reduction)
3. Identifying Power Trend confirmation (maximum conviction)

---

## Distribution Day Monitoring After FTD

### What Is a Post-FTD Distribution Day?
A distribution day after an FTD is defined as:
- Index declines >= 0.2% from the prior day's close
- Volume is higher than the previous day's volume
- Occurs within the first 5 trading days after the FTD

### Failure Rate by Distribution Timing

| Distribution Timing | Failure Rate | Quality Score Impact | Action |
|--------------------|-------------|---------------------|--------|
| **Day 1 after FTD** | ~85% fail | -30 points | Immediately reduce exposure |
| **Day 2 after FTD** | ~80% fail | -30 points | Reduce to defensive levels |
| **Day 3 after FTD** | ~65% fail | -15 points | Tighten stops significantly |
| **Day 4 after FTD** | ~50% fail | -5 points | Moderate caution |
| **Day 5 after FTD** | ~45% fail | -5 points | Normal monitoring |
| **No distribution (5 days)** | ~35% fail | +10 points | Increase conviction |

**Key Insight:** The earlier distribution appears after an FTD, the more likely the FTD will fail. Distribution within the first 2 days is a near-certain failure signal.

### Multiple Distribution Days
- 2+ distribution days within 5 days of FTD: ~90% failure rate
- Even if individual days are in the "moderate" timing zone (Day 4-5), accumulation of distribution is bearish

---

## FTD Invalidation

### Invalidation Criteria
An FTD is formally invalidated when:
- **Index closes below the FTD day's intraday low**
- This is a hard stop - the FTD signal is no longer valid

### What to Do After Invalidation
1. Reduce equity exposure to defensive levels (0-25%)
2. Do NOT try to average down or hold through
3. Wait for a new swing low and fresh rally attempt
4. The previous FTD failure provides no information about the next attempt

### Soft Warnings (Not Yet Invalidated)
- Close approaches but doesn't breach FTD low: heightened caution
- Intraday breach but close above: technically valid but weak
- Slow grinding decline toward FTD low: consider preemptive reduction

---

## Power Trend Confirmation

### Definition
A Power Trend is the strongest bullish condition in O'Neil's framework. It occurs when three conditions are simultaneously true:

1. **21-day EMA > 50-day SMA** (short-term momentum above medium-term trend)
2. **50-day SMA slope is positive** (rising over the last 5 trading days)
3. **Price above 21-day EMA** (current price confirming the trend)

### Significance
- Power Trend + FTD = highest conviction bottom signal
- Historically, markets in Power Trend have very low probability of immediate failure
- Power Trend typically develops 2-4 weeks after a successful FTD
- Not required for FTD validity, but serves as strong confirmation

### Power Trend Conditions Breakdown

| Conditions Met | Interpretation |
|---------------|---------------|
| 3/3 | Full Power Trend - maximum conviction |
| 2/3 | Developing trend - monitor for completion |
| 1/3 | No Power Trend - rely on other signals |
| 0/3 | Bearish structure - be cautious despite FTD |

---

## FTD Success vs Failure Patterns

### Characteristics of Successful FTDs

| Factor | Successful Pattern |
|--------|--------------------|
| **Day Timing** | Day 4-7 (prime window) |
| **Gain** | 2.0%+ on heavy volume |
| **Volume** | Above 50-day average |
| **Dual Index** | Both S&P 500 and NASDAQ confirm |
| **Post-FTD** | Clean first 3-5 days (no distribution) |
| **Leading Stocks** | Many breakouts from proper bases |
| **Sector Breadth** | Multiple sectors participating |
| **Catalyst** | Identifiable positive catalyst (Fed pivot, earnings surprise) |
| **Power Trend** | Develops within 2-4 weeks |

### Characteristics of Failed FTDs

| Factor | Failure Pattern |
|--------|--------------------|
| **Day Timing** | Day 8-10 (late window) |
| **Gain** | Minimum qualifying (1.25-1.49%) |
| **Volume** | Below 50-day average |
| **Dual Index** | Only one index confirms |
| **Post-FTD** | Distribution within first 2 days |
| **Leading Stocks** | Few/no quality breakouts |
| **Sector Breadth** | Narrow participation (1-2 sectors) |
| **Catalyst** | No clear catalyst, or hostile macro backdrop |
| **Power Trend** | Never develops, 50 SMA continues declining |

---

## Exposure Management After FTD

### Graduated Exposure Model

The O'Neil approach uses progressive exposure increase, not all-at-once buying:

**Phase 1: Initial (FTD Day)**
- Start at 25% of target exposure
- Buy 1-2 leading stocks breaking out of bases
- Use FTD day's low as initial stop reference

**Phase 2: Confirmation (Days 1-5 post-FTD)**
- If no distribution: increase to 50% exposure
- Add positions in additional leaders
- Tighten stops on initial positions to breakeven

**Phase 3: Acceleration (Days 5-15 post-FTD)**
- If trend confirms (clean action, breakouts working): increase to 75%
- Pyramid into winning positions
- Look for Power Trend development

**Phase 4: Full Exposure (2-4 weeks post-FTD)**
- If Power Trend develops: full 100% exposure
- Focus on strongest leaders
- Normal stop-loss management

### Exposure Reduction Triggers

| Trigger | Action |
|---------|--------|
| Distribution Day 1-2 post-FTD | Cut to 0-25% |
| Distribution Day 3 post-FTD | Cut to 25-50% |
| FTD invalidated | Cut to 0-25% |
| Breakouts failing (stocks reversing after breakout) | Reduce by 25% |
| No quality setups forming | Don't force increase |

---

## Interaction with Market Top Detector

The FTD Detector and Market Top Detector are complementary:

### During Correction (Top Detector score 60+):
1. Top Detector signals defensive posture
2. FTD Detector watches for bottom signals
3. When FTD confirms, begin transitioning from defensive to offensive

### During FTD Confirmed:
1. FTD Detector guides exposure increase
2. Top Detector should show declining score (improving conditions)
3. If Top Detector score remains high despite FTD, exercise extra caution

### Signal Conflict Resolution:
- FTD confirmed but Top Detector still 60+: proceed with caution, use smaller position sizes
- FTD confirmed and Top Detector below 40: higher conviction signal
- FTD invalidated: defer to Top Detector for defensive guidance

---

## Historical Success Rate Context

Based on IBD historical analysis of FTDs since 1900:

- **Overall FTD success rate:** ~25% (1 in 4 leads to sustained uptrend)
- **FTDs with quality score 80+:** ~45-50% success rate
- **FTDs with quality score 60-79:** ~30-35% success rate
- **FTDs with quality score below 60:** ~10-15% success rate

The quality scoring system effectively filters the ~75% failure rate down to a more manageable ~50-55% for high-quality signals. Combined with proper stop-loss management, this creates a positive expected value system despite the sub-50% win rate, because winners significantly outperform losers when properly managed.


---

## SKILL: fx-exposure-review

- Fuente: `SYasJ/claude-business-skills` → `plugins/finance/skills/fx-exposure-review` (MIT)
- Cuándo usarla: Identify where currency actually hits cash, and separate a hedge policy question from a bookkeeping curiosity. Use when the user mentions FX exposure, currency risk, hedging review, exchange rate impact, or asks for a FX exposure review. Finance skill by Yasir Jilani.

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'fx-exposure-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Foreign Exchange Exposure Review

Identify where currency actually hits cash, and separate a hedge policy question from a bookkeeping curiosity.

## When to use this skill

Use this skill when the user:

- FX exposure
- currency risk
- hedging review
- exchange rate impact

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

- Currencies of revenue, costs, and cash
- Which exposures are contractual
- The user's hedge policy, if any
- The decision they need to make

## Workflow


### 1. Map cash exposures

Where currency hits a bank account, not only where a report is translated.
### 2. Separate transaction from translation

Management action usually belongs on contracted cash flows. Say which one the user is looking at.
### 3. Quantify only with their data

A rate move they specify, applied to exposures they listed. Do not invent a forecast rate and call it the market.
### 4. Policy before trades

If they have no hedge policy, recommend writing the policy questions, not a trade ticket.
### 5. Note operational natural hedges

Costs in the same currency as revenue may already offset. Do not propose a hedge that doubles the risk.
### 6. Hand off execution

This skill does not place trades or ask for brokerage logins.

## Output

Deliver a **FX exposure review**.

- Purpose of this FX exposure review, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a FX exposure review by 30 September 2026. A firm invoices in euros and pays staff in dollars and wants to know if last month's margin drop was FX.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A firm invoices in euros and pays staff in dollars and wants to know if last month's margin drop was FX.

Currencies of revenue, costs, and cash: CAD 44 direct. Overhead not in this line
Which exposures are contractual: unsigned draft, 8 pages, no signature date
The user's hedge policy, if any: their one-page rule dated 2 Mar 2026. No exception log
The decision they need to make: A firm invoices in euros and pays staff in dollars and wants to know if last month's margin drop was FX
```

### Example outcome

**Fx exposure review**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A map of contractual cash exposure, a translation-versus-transaction split, and policy questions rather than a trade order.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Currencies of revenue, costs, and cash | CAD 44 direct. Overhead not in this line | Needs confirmation |
| Which exposures are contractual | unsigned draft, 8 pages, no signature date | Carried into the draft |
| The user's hedge policy, if any | their one-page rule dated 2 Mar 2026. No exception log | Carried into the draft |
| The decision they need to make | A firm invoices in euros and pays staff in dollars and wants to know if last month's margin drop was FX | Needs confirmation |

**How this draft was built**

**1. Map cash exposures**  
Where currency hits a bank account, not only where a report is translated.

**2. Separate transaction from translation**  
Management action usually belongs on contracted cash flows. Say which one the user is looking at.

**3. Quantify only with their data**  
A rate move they specify, applied to exposures they listed. Do not invent a forecast rate and call it the market.

**4. Policy before trades**  
If they have no hedge policy, recommend writing the policy questions, not a trade ticket.

**5. Note operational natural hedges**  
Costs in the same currency as revenue may already offset. Do not propose a hedge that doubles the risk.

**Deliberately not done**
- Treating accounting translation as cash risk without checking.
- Inventing a hedge product and telling them to buy it.
- Asking for trading credentials.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Treating accounting translation as cash risk without checking.
- Inventing a hedge product and telling them to buy it.
- Asking for trading credentials.

## Related skills

- `pricing-margin-bridge`
- `cash-flow-forecast`
- `treasury-policy-brief`


---

## SKILL: fxmacrodata-calendar

- Fuente: `tradermonty/claude-trading-skills` → `skills/fxmacrodata-calendar` (MIT)
- Cuándo usarla: Fetch official FXMacroData macro release-calendar events for trade planning, macro regime checks, and event-risk filters. Use before CPI, NFP, GDP, PCE, retail sales, PMI, and central-bank decision windows.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/fxmacrodata-calendar/` (requirements.txt, fetch_calendar.py)

# FXMacroData Calendar

Retrieve official-source macro release-calendar events from FXMacroData. Use
this skill when a trade plan needs event timing, confirmed release dates, or a
top-tier macro risk check.

## Workflow

1. Run the calendar script:

   ```bash
   python3 skills/fxmacrodata-calendar/scripts/fetch_calendar.py --currency usd --min-tier 1
   ```

2. Review `events[]` for top-tier releases.

   Treat a nonzero exit as an unverified event-risk state, never as an empty
   calendar. Only a successful response containing `events: []` establishes
   that no matching events were returned. The client accepts results only when
   the response currency matches the request and `data_quality` confirms an
   official, current, non-proxy, non-fallback, timestamp-complete,
   point-in-time-safe source. Each event must include an announcement timestamp
   and a non-empty release identifier.

3. Fold the event timing into the trade plan:
   - pause new entries around high-impact releases;
   - reduce leverage or position size;
   - schedule follow-up review after the actual value is available;
   - explain which event and timestamp drove the adjustment.

## Authentication

Set `FXMACRODATA_API_KEY` for authenticated FXMacroData endpoints. Public USD
calendar rows can be fetched without a key. The client uses the canonical
`https://api.fxmacrodata.com/v1` endpoint and accepts `--min-tier` values 1,
2, or 3 only. Live calendar responses currently include `market_tier`; the
skill treats it as an extension field and requires integer values 1 through 3
for filtering, although the current `CalendarReleaseRow` OpenAPI schema does
not declare that field.


---

## SKILL: hormuz-strait

- Fuente: `himself65/finance-skills` → `plugins/data-providers/skills/hormuz-strait` (MIT)
- Cuándo usarla: >

# Hormuz Strait Monitor Skill

Fetches real-time status of the Strait of Hormuz from the [Hormuz Strait Monitor](https://hormuzstraitmonitor.com) dashboard API. Covers shipping transits, oil prices, stranded vessels, insurance risk, diplomatic status, global trade impact, and crisis timeline.

**This skill is read-only.** It fetches public dashboard data — no authentication required.

---

## Step 1: Fetch Dashboard Data

Use `curl` to fetch the dashboard API:

```bash
curl -s https://hormuzstraitmonitor.com/api/dashboard
```

Parse the JSON response. The API returns `{ "success": true, "data": { ... }, "timestamp": "..." }`.

If `success` is `false` or the request fails, inform the user the monitor is temporarily unavailable and suggest checking https://hormuzstraitmonitor.com directly.

---

## Step 2: Identify What the User Needs

Match the user's request to the relevant data sections. If the user asks for a general status update, present all sections. If they ask about something specific, focus on the relevant section(s).

| User Request | Data Section | Key Fields |
|---|---|---|
| General status / "is Hormuz open?" | `straitStatus` | `status`, `since`, `description` |
| Ship traffic / transit count | `shipCount` | `currentTransits`, `last24h`, `normalDaily`, `percentOfNormal` |
| Oil price impact | `oilPrice` | `brentPrice`, `change24h`, `changePercent24h`, `sparkline` |
| Stranded / stuck vessels | `strandedVessels` | `total`, `tankers`, `bulk`, `other`, `changeToday` |
| Insurance / war risk | `insurance` | `level`, `warRiskPercent`, `normalPercent`, `multiplier` |
| Cargo throughput | `throughput` | `todayDWT`, `averageDWT`, `percentOfNormal`, `last7Days` |
| Diplomatic situation | `diplomacy` | `status`, `headline`, `parties`, `summary` |
| Global trade impact | `globalTradeImpact` | `percentOfWorldOilAtRisk`, `estimatedDailyCostBillions`, `affectedRegions`, `lngImpact`, `alternativeRoutes`, `supplyChainImpact` |
| Crisis timeline / events | `crisisTimeline` | `events[]` with `date`, `type`, `title`, `description` |
| Tanker freight rates / VLCC rates | `tankerRates` | `currentRate`, `preCrisisRate`, `changePercent`, `route`, `vesselType`, `trend`, `unit` |
| Latest news | `news` | `title`, `source`, `url`, `publishedAt`, `description` |

---

## Step 3: Present the Data

Format the results clearly for financial research. Adapt the presentation based on what the user asked for.

### General status briefing (default)

When the user asks for a general update, cover these sections — a line each while shipping is operating normally, more depth wherever there is active disruption:

1. **Strait Status** — lead with the current status (e.g., "OPEN", "RESTRICTED", "CLOSED"), how long it's been in that state, and the description
2. **Ship Traffic** — current transits, last 24h count, and percent of normal
3. **Oil Price** — Brent price with 24h change
4. **Stranded Vessels** — total count broken down by type, with today's change
5. **Insurance Risk** — risk level, war risk premium percentage, and multiplier vs. normal
6. **Cargo Throughput** — today's DWT vs. average, percent of normal
7. **Diplomatic Status** — current status, headline, and brief summary
8. **Global Trade Impact** — percent of world oil at risk, estimated daily cost, and top affected regions
9. **Tanker Freight Rates** — current VLCC rate on the benchmark route vs. pre-crisis baseline, with trend direction

### Formatting guidelines

- Use tables for structured data (vessel counts, affected regions, alternative routes)
- Highlight abnormal values — if `percentOfNormal` is below 80% or above 120%, call it out
- For `oilPrice.sparkline`, describe the trend (rising, falling, stable) rather than listing raw numbers
- For `throughput.last7Days`, describe the trend direction
- Show `lastUpdated` timestamp so the user knows data freshness
- For news items, include the source and link
- For crisis timeline events, present chronologically with event type labels

### Risk assessment

Based on the data, provide a brief risk assessment. `insurance.level` values come back uppercase:

| Insurance Level | Interpretation |
|---|---|
| `NORMAL` | No elevated risk — shipping operating normally |
| `ELEVATED` | Some disruption concerns — monitor closely |
| `HIGH` | Significant risk — active disruption or credible threat |
| `CRITICAL` | Severe disruption — major impact on global oil supply |
| `EXTREME` | Effective closure — war risk premiums at multi-decade highs, most commercial traffic halted |

If the strait status is anything other than fully open, highlight:
- The estimated daily cost to global trade
- Which regions are most affected and their oil dependency
- Available alternative routes with additional transit days and cost
- LNG impact if applicable
- SPR (Strategic Petroleum Reserve) status in days

---

## Step 4: Respond to the User

- Lead with the most important information: strait status and any active disruption
- Include data freshness (`lastUpdated` timestamp)
- If the situation is elevated or worse, proactively include the global trade impact summary
- Keep the response concise for routine "all clear" statuses; expand for active incidents
- Add a disclaimer: data is sourced from Hormuz Strait Monitor and may have delays

---

## Reference Files

- `references/api_schema.md` — Complete API response schema with field descriptions and data types

Read the reference file when you need exact field names or data type details.

### Referencia: README.md

# hormuz-strait

Real-time Strait of Hormuz monitoring for energy market and geopolitical risk research via the [Hormuz Strait Monitor](https://hormuzstraitmonitor.com) dashboard API.

## What it does

Fetches the current status of the Strait of Hormuz and presents a risk briefing covering:

- **Strait status** — open, restricted, or closed, with duration and description
- **Ship traffic** — current transits, 24h count, and percent of normal baseline
- **Oil price impact** — Brent crude price with 24h change and trend
- **Stranded vessels** — count by type (tankers, bulk, other) with daily change
- **Insurance risk** — war risk premium level, percentage, and multiplier vs. normal
- **Cargo throughput** — daily DWT vs. average with 7-day trend
- **Diplomatic status** — current situation, parties involved, and headline
- **Global trade impact** — percent of world oil/LNG at risk, daily cost, affected regions, alternative routes, and supply chain disruption
- **Crisis timeline** — chronological events (military, diplomatic, economic)
- **Tanker freight rates** — VLCC benchmark rate vs. pre-crisis baseline with trend
- **Latest news** — recent articles with sources and links

**This skill is read-only.** No authentication required — uses the public dashboard API.

## Triggers

- "Hormuz status", "Strait of Hormuz", "is Hormuz open"
- "shipping through the Gulf", "Persian Gulf tanker traffic"
- "oil chokepoint", "war risk premium", "Hormuz crisis"
- "energy supply chain risk", "oil transit disruption", "Middle East shipping"
- Any mention of Hormuz or Persian Gulf in context of oil, shipping, or geopolitical risk

## Platform

Works on **all platforms** (Claude Code, Claude.ai, and other agents). Only requires `curl` for the API call.

## Setup

```bash
# Choose finance-data-providers when prompted.
npx plugins add himself65/finance-skills

# Or install just this skill
npx skills add himself65/finance-skills --skill hormuz-strait
```

See the [main README](../../../../README.md) for more installation options.

## Reference files

- `references/api_schema.md` — Complete API response schema with field descriptions and data types

### Referencia: references/api_schema.md

# Hormuz Strait Monitor — Dashboard API Schema

**Endpoint:** `GET https://hormuzstraitmonitor.com/api/dashboard`

**Authentication:** None (public API)

**Response format:** JSON

---

## Top-level response

| Field | Type | Description |
|---|---|---|
| `success` | boolean | Whether the API call succeeded |
| `data` | object | Dashboard data (see sections below) |
| `timestamp` | string (ISO datetime) | Server response timestamp |

---

## `data.straitStatus`

Current operational status of the strait.

| Field | Type | Description |
|---|---|---|
| `status` | string | Current status enum (observed: "OPEN", "RESTRICTED", "CLOSED") |
| `since` | string (ISO date) | Date the current status began |
| `description` | string | Human-readable status description |

---

## `data.shipCount`

Ship transit statistics.

| Field | Type | Description |
|---|---|---|
| `currentTransits` | number | Ships currently transiting the strait |
| `last24h` | number | Total transits in the last 24 hours |
| `normalDaily` | number | Normal daily transit count (baseline) |
| `percentOfNormal` | number | Current traffic as percentage of normal |

---

## `data.oilPrice`

Brent crude oil price and recent movement.

| Field | Type | Description |
|---|---|---|
| `brentPrice` | number | Current Brent crude price (USD/barrel) |
| `change24h` | number | Absolute price change in last 24 hours |
| `changePercent24h` | number | Percentage price change in last 24 hours |
| `sparkline` | number[] | 24-hour price history (array of prices) |

---

## `data.strandedVessels`

Vessels unable to transit the strait.

| Field | Type | Description |
|---|---|---|
| `total` | number | Total stranded vessels |
| `tankers` | number | Stranded tanker vessels |
| `bulk` | number | Stranded bulk carriers |
| `other` | number | Other stranded vessels |
| `changeToday` | number | Change in stranded vessel count today |

---

## `data.insurance`

Marine insurance and war risk premium levels.

| Field | Type | Description |
|---|---|---|
| `level` | string | Risk level enum (observed: "NORMAL", "ELEVATED", "HIGH", "CRITICAL", "EXTREME") |
| `warRiskPercent` | number | Current war risk premium as percentage |
| `normalPercent` | number | Normal (baseline) insurance rate percentage |
| `multiplier` | number | Current rate as multiplier of normal rate |

---

## `data.throughput`

Cargo throughput in deadweight tonnage (DWT).

| Field | Type | Description |
|---|---|---|
| `todayDWT` | number | Today's cargo throughput in DWT |
| `averageDWT` | number | Average daily throughput in DWT |
| `percentOfNormal` | number | Today's throughput as percentage of average |
| `last7Days` | number[] | Daily DWT values for the last 7 days |

---

## `data.diplomacy`

Current diplomatic situation affecting the strait.

| Field | Type | Description |
|---|---|---|
| `status` | string | Diplomatic status enum (uppercase snake case; e.g., "TALKS_IN_PROGRESS") |
| `headline` | string | Current diplomatic headline |
| `date` | string (ISO date) | Date of the latest diplomatic development |
| `parties` | string[] | Parties involved |
| `summary` | string | Summary of the diplomatic situation |

---

## `data.globalTradeImpact`

Estimated impact on global trade if the strait is disrupted.

| Field | Type | Description |
|---|---|---|
| `percentOfWorldOilAtRisk` | number | Percentage of global oil supply at risk |
| `estimatedDailyCostBillions` | number | Estimated daily cost of disruption in billions USD |
| `affectedRegions` | object[] | List of affected regions (see below) |
| `lngImpact` | object | LNG-specific impact (see below) |
| `alternativeRoutes` | object[] | Available alternative shipping routes (see below) |
| `supplyChainImpact` | object | Broader supply chain impact (see below) |

### `affectedRegions[]`

| Field | Type | Description |
|---|---|---|
| `name` | string | Region name |
| `severity` | string | Impact severity enum (observed: "MODERATE", "HIGH", "CRITICAL") |
| `oilDependencyPercent` | number | Region's dependency on strait-transiting oil |
| `description` | string | Description of impact on this region |

### `lngImpact`

| Field | Type | Description |
|---|---|---|
| `percentOfWorldLngAtRisk` | number | Percentage of global LNG at risk |
| `estimatedLngDailyCostBillions` | number | Estimated daily LNG disruption cost (billions USD) |
| `topAffectedImporters` | string[] | Countries most affected by LNG disruption |
| `description` | string | Description of LNG impact |

### `alternativeRoutes[]`

| Field | Type | Description |
|---|---|---|
| `name` | string | Route name |
| `additionalDays` | number | Extra transit days vs. Hormuz route |
| `additionalCostPerVessel` | number | Extra cost per vessel (USD) |
| `currentUsageStatus` | string | Whether this route is currently in use |

### `supplyChainImpact`

| Field | Type | Description |
|---|---|---|
| `shippingRateIncreasePercent` | number | Percentage increase in shipping rates |
| `consumerPriceImpactPercent` | number | Estimated consumer price impact |
| `sprStatusDays` | number | Strategic Petroleum Reserve coverage in days |
| `keyDisruptions` | string[] | Key supply chain disruptions |

---

## `data.crisisTimeline`

Timeline of events related to the current situation.

### `events[]`

| Field | Type | Description |
|---|---|---|
| `date` | string (ISO date) | Event date |
| `type` | string | Event type enum (observed: "MILITARY", "DIPLOMATIC", "ESCALATION", "ECONOMIC") |
| `title` | string | Event title |
| `description` | string | Event description |

---

## `data.tankerRates`

VLCC tanker freight rate tracker for the Hormuz-adjacent benchmark route.

| Field | Type | Description |
|---|---|---|
| `currentRate` | number | Current freight rate on the benchmark route |
| `preCrisisRate` | number | Pre-crisis baseline rate on the same route |
| `changePercent` | number | Percentage change vs. the pre-crisis baseline |
| `route` | string | Benchmark route code (e.g., "AG-East (TD3C)") |
| `vesselType` | string | Vessel class (e.g., "VLCC") |
| `trend` | number[] | Recent rate history points (aligned with `unit`) |
| `unit` | string | Rate unit (e.g., "WS" for Worldscale, "USD/day" for time-charter equivalent) |

---

## `data.news`

Latest news articles related to the strait.

| Field | Type | Description |
|---|---|---|
| `title` | string | Article title |
| `source` | string | News source name |
| `url` | string | Link to the article |
| `publishedAt` | string (ISO datetime) | Publication timestamp |
| `description` | string | Article summary |

---

## `data.lastUpdated`

String (ISO datetime) — when the dashboard data was last updated. Appears directly on `data`, not as a nested object.


---

## SKILL: ib-report-delta-adjusted-notional-exposure

- Fuente: `staskh/trading_skills` → `.claude/skills/ib-report-delta-adjusted-notional-exposure` (MIT)
- Cuándo usarla: Report delta-adjusted notional exposure across all IBKR accounts. Calculates option deltas using Black-Scholes and reports long/short exposure by account and underlying. Use when user asks about delta exposure, portfolio risk, or directional exposure.
- Código: extraer `code/staskh_trading_skills.tar` y usar `.claude/skills/ib-report-delta-adjusted-notional-exposure/` (delta_exposure.py)

# IB Delta-Adjusted Notional Exposure Report

Calculate and report delta-adjusted notional exposure across all Interactive Brokers accounts.

## IB Connection

TWS or IB Gateway must be running locally with API enabled:
- **Paper trading** — port 7497
- **Live trading** — port 7496
- **`IB_PORT` env var** — default port when `--port` is omitted (e.g. `IB_PORT=4001` for a Gateway container). Precedence: `--port` flag > `IB_PORT` > built-in default. Set it in the shell or a `.env` file.

**Port fallback:** If the configured port fails, automatically retry on the other port.
If the retry succeeds, save to memory which account type worked (live/paper) and reuse it for all IB skill calls in this and future sessions — until the user explicitly asks for the other account.
If both ports fail, ask the user to verify that TWS or IB Gateway is running with API access enabled.

## Instructions

### Step 1: Gather Data

```bash
uv run python scripts/delta_exposure.py [--port PORT]
```

The script returns JSON to stdout with all position deltas and summary data.

### Step 2: Format Report

Read `templates/markdown-template.md` for formatting instructions. Generate a markdown report from the JSON data and save to `sandbox/`.

**Filename**: `delta_exposure_report_{YYYYMMDD}_{HHMMSS}.md`

### Step 3: Report Results

Present the summary table (total long, short, net) and top exposures to the user. Include the saved report path.

## Arguments

- `--port` - IB port (default: 7497 for paper trading)

## JSON Output

Returns delta-adjusted notional exposure with:
- `connected` - Boolean
- `accounts` - List of account IDs
- `position_count` - Total positions
- `positions` - Array of positions with symbol, delta, delta_notional, spot price
- `summary` - Totals for long, short, and net delta notional
  - `by_account` - Long/short breakdown by account
  - `by_underlying` - Long/short/net breakdown by symbol

## Methodology

- **Equity Options**: Delta calculated via Black-Scholes with estimated IV based on moneyness
- **Futures**: Delta = 1.0 (full notional exposure)
- **Futures Options**: Delta calculated with lower IV assumption (20%)
- **Stocks**: Delta = 1.0

Delta-adjusted notional = delta x spot price x quantity x multiplier

## Examples

```bash
# Paper trading (default)
uv run python scripts/delta_exposure.py

# Live trading
uv run python scripts/delta_exposure.py --port 7496
```


## Timezone

All timestamps and time-based calculations must use the `America/New_York` timezone. All JSON output must include `generated_at` (NY time string) and `data_delay` fields.

### Referencia: templates/markdown-template.md

# Delta Exposure Report - Markdown Template

Format the JSON data into a markdown report saved to `sandbox/`.

**Filename**: `delta_exposure_report_{YYYYMMDD}_{HHMMSS}.md`

## JSON Structure

```
{
  "connected": true,
  "accounts": ["ACC1", "ACC2"],
  "position_count": 25,
  "positions": [
    {
      "account": "ACC1",
      "symbol": "AAPL",
      "sec_type": "OPT",       // OPT, FOP, FUT, STK
      "strike": 180.0,         // options only
      "expiry": "20260321",    // options only, YYYYMMDD
      "right": "C",            // C or P, options only
      "qty": -5,
      "spot": 185.50,
      "delta": -0.35,
      "multiplier": 100,
      "raw_notional": -92750.0,
      "delta_notional": -32462.5
    }
  ],
  "summary": {
    "total_long_delta_notional": 500000.0,
    "total_short_delta_notional": -250000.0,
    "net_delta_notional": 250000.0,
    "by_account": {
      "ACC1": { "long": 300000.0, "short": -150000.0 }
    },
    "by_underlying": {
      "AAPL": { "long": 100000.0, "short": -50000.0, "net": 50000.0 }
    }
  }
}
```

## Report Sections

### 1. Header
```markdown
# Delta-Adjusted Notional Exposure Report
**Generated:** YYYY-MM-DD HH:MM:SS
**Accounts:** ACC1, ACC2
**Total Positions:** N
```

### 2. Portfolio Summary

| Metric | Value |
|--------|-------|
| Total Long Delta Notional | $X,XXX,XXX |
| Total Short Delta Notional | ($X,XXX,XXX) |
| **Net Delta Notional** | **$X,XXX,XXX** |

### 3. Summary by Account

| Account | Long | Short | Net |
|---------|------|-------|-----|

Calculate net as `long + short` for each account.

### 4. Summary by Underlying

| Symbol | Long | Short | Net |
|--------|------|-------|-----|

Sort by absolute net (descending).

### 5. Top Long Delta Exposures

Top 10 positions sorted by delta_notional (descending, positive only):

| Account | Symbol | Type | Strike | Expiry | Qty | Delta | Spot | Delta Notional |
|---------|--------|------|--------|--------|-----|-------|------|----------------|

### 6. Top Short Delta Exposures

Top 10 positions sorted by delta_notional (ascending, negative only):

| Account | Symbol | Type | Strike | Expiry | Qty | Delta | Spot | Delta Notional |
|---------|--------|------|--------|--------|-----|-------|------|----------------|

### 7. Detailed Positions by Account (full report only)

Group by account, then split into long/short subsections with full position tables.

### 8. Detailed Positions by Symbol (full report only)

Group by symbol with all positions listed.

## Formatting Rules

- Currency: `$X,XXX.XX` format, negative values in parentheses: `($X,XXX.XX)`
- Delta: 2 decimal places
- Spot: 2 decimal places
- Expiry: format YYYYMMDD as "Mon DD, YYYY"
- Type: "OPT" -> show strike + right (e.g., "$180 C"), "STK" -> "Stock", "FUT" -> "Future"
- Sort tables by absolute delta notional descending unless otherwise specified

## Footer
```markdown
*Report generated by Trading Skills on YYYY-MM-DD HH:MM*
```


---

## SKILL: ibd-distribution-day-monitor

- Fuente: `tradermonty/claude-trading-skills` → `skills/ibd-distribution-day-monitor` (MIT)
- Cuándo usarla: Detect IBD-style Distribution Days for QQQ/SPY (close down at least 0.2% on higher volume), track 25-session expiration and 5% invalidation, count d5/d15/d25 clusters, classify market risk (NORMAL/CAUTION/HIGH/SEVERE), and emit TQQQ/QQQ exposure recommendations. Use after market close, before TQQQ exposure changes, or as input to FTD/market-state frameworks. Does not execute trades.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/ibd-distribution-day-monitor/` (default.yaml, requirements.txt, _fmp_compat.py, data_loader.py, distribution_day_tracker.py, exposure_policy.py, fmp_client.py, history_utils.py, ibd_monitor.py, math_utils.py, models.py, report_generator.py …)

# IBD Distribution Day Monitor

## Purpose
Detect IBD-style Distribution Days for major market ETFs (QQQ as Nasdaq proxy, SPY as S&P 500 proxy) and produce a daily market deterioration signal plus a TQQQ/QQQ exposure recommendation. Designed for post-market review.

## When to Use
Invoke this skill:
- Daily after the US market close.
- Before increasing TQQQ exposure or rebalancing leveraged positions.
- When evaluating whether an uptrend is becoming vulnerable to a correction.
- As an upstream input to FTD (Follow-Through Day) detection or other market-state frameworks.

Do NOT use this skill to:
- Execute trades or modify orders.
- Generate discretionary market predictions outside of the IBD ruleset.

## Inputs
- Symbols (default: QQQ, SPY) and lookback (default 80 trading sessions).
- Optional `--as-of YYYY-MM-DD` for backtesting against a historical session.
- Strategy context: instrument (TQQQ or QQQ), current exposure %, base trailing stop %.
- FMP API key via `--api-key`, `config.data.api_key`, or `FMP_API_KEY` env var (in that priority order).

## Core Rules
A Distribution Day is detected when:
1. Today's close is at least 0.2% below yesterday's close.
2. Today's volume is greater than yesterday's volume.

A Distribution Day is removed from the active count when either:
- More than 25 trading sessions have elapsed since the DD.
- The index has gained 5% from the DD close (using post-DD high by default; configurable to close-source).

Today's DD is never invalidated immediately because there are no post-DD sessions to evaluate the 5% gain against.

## Counting Conventions
- `d5_count` / `d15_count` / `d25_count` count active records with `age_sessions <= N`.
- This means **N+1 sessions** are inspected (age 0..N inclusive). Reports therefore say "within N elapsed sessions" rather than "直近 N 取引日" to avoid ambiguity.

## Risk Classification
| Risk | Trigger |
|------|---------|
| NORMAL | `d25 <= 2` |
| CAUTION | `d25 >= 3` |
| HIGH | `d25 >= 5` OR `d15 >= 3` OR `d5 >= 2` |
| SEVERE | `d25 >= 6` OR `d15 >= 4` OR (`market_below_21ema_or_50ma` AND `d25 >= 5`) |

When both QQQ and SPY are loaded, QQQ-weighted overall logic applies (TQQQ-aware): a single SEVERE escalates to SEVERE; QQQ HIGH escalates to overall HIGH; QQQ NORMAL + SPY HIGH still escalates to HIGH (broad-market spillover).

## TQQQ Exposure Policy
| Risk | Action | Target Exposure | Trailing Stop |
|------|--------|-----------------|---------------|
| NORMAL | HOLD_OR_FOLLOW_BASE_STRATEGY | 100% | base |
| CAUTION | AVOID_NEW_ADDS | 75% | min(base, 7%) |
| HIGH | REDUCE_EXPOSURE | 50% | min(base, 5%) |
| SEVERE | CLOSE_TQQQ_OR_HEDGE | 25% | min(base, 3%) |

QQQ uses a less aggressive policy (HIGH=75%, SEVERE=50%) since it lacks 3x leverage.

## Workflow
1. Load OHLCV for the configured symbols via FMP (`get_historical_prices`).
2. Validate data quality; record skipped sessions in audit.
3. Rebase via `prepare_effective_history` so `effective_history[0]` is the evaluation session.
4. Detect raw Distribution Days; enrich with `high_since`, invalidation event, and status.
5. Count `d5` / `d15` / `d25` active records.
6. Compute 21EMA and 50SMA filters; flag `market_below_21ema_or_50ma` (None if data insufficient).
7. Classify each index, then combine using QQQ-weighted policy.
8. Generate portfolio action for the configured instrument.
9. Write JSON + Markdown reports to `--output-dir` with API keys redacted.

## Outputs
Saved to `reports/` (or `--output-dir`):
- `ibd_distribution_day_monitor_YYYY-MM-DD_HHMMSS.json`
- `ibd_distribution_day_monitor_YYYY-MM-DD_HHMMSS.md`

JSON is UTF-8 with `ensure_ascii=False` (Japanese explanations preserved). Sensitive keys (`api_key`, `fmp_api_key`, `token`, etc.) are redacted automatically.

## Operating Principles
- Do not override the IBD rule definitions unless `config/default.yaml` is changed deliberately.
- Always explain which dates contributed to the active count.
- Treat missing or unreliable volume data as a warning (audit_flag), not as a Distribution Day.
- Do not place trades. The portfolio action is a risk-management suggestion, not an execution instruction.

## CLI
```bash
python3 skills/ibd-distribution-day-monitor/scripts/ibd_monitor.py \
  --symbols QQQ,SPY \
  --lookback-days 80 \
  --instrument TQQQ \
  --current-exposure 100 \
  --base-trailing-stop 10 \
  --output-dir reports/
```

## API Requirements
FMP API key required. Free tier (250 calls/day) is sufficient for daily QQQ + SPY runs.

## Related Skills
- `ftd-detector`: Bottom confirmation via Follow-Through Days (counterpart of this top-side signal).
- `market-top-detector`: Composite 0-100 top probability score using O'Neil distribution + other components.
- `position-sizer`: Convert risk-management recommendations into share counts.

### Referencia: references/ibd_distribution_methodology.md

# IBD Distribution Day Methodology

## Origin
Investor's Business Daily (IBD) and William O'Neil's CAN SLIM framework popularized the concept that institutional selling can be tracked by counting *Distribution Days* on major indexes. A cluster of distribution days is interpreted as a sign that institutions are unloading positions, often preceding a market correction.

## Detection Rule
A Distribution Day is detected when both conditions hold for the daily bar of an index or large ETF proxy (e.g. QQQ, SPY):

1. **Decline:** Today's close is at least 0.2% below yesterday's close (this skill uses `pct_change <= -0.002`).
2. **Higher Volume:** Today's volume is greater than yesterday's volume.

A small *epsilon* is applied at the boundary so that floating-point noise around 0.2% does not cause flaky detection.

## Removal Rules
A Distribution Day is removed from the active count when either:

- **Expiration:** More than `expiration_sessions` (default 25) trading sessions have elapsed since the Distribution Day occurred.
- **Invalidation:** The index has gained `invalidation_gain_pct` (default 5%) from the Distribution Day close.

This skill records the **first chronological post-DD session** to cross the invalidation threshold so that the audit trail shows exactly when invalidation happened and how many sessions after the DD.

## Invalidation Boundary Choices

The 5% invalidation rule uses `invalidation_price_source` ("high" or "close"):

- `high` (default, more conservative): the post-DD intraday high crossing 5% is enough to invalidate.
- `close`: only post-DD closing prices count.

The Distribution Day's own intraday high is **never** used to invalidate it (`invalidation_session_scope: after_distribution_day_only`). IBD's rule is "5% gain from the Distribution Day close", so DD-day high vs DD close cannot represent post-DD strength.

If the 5% threshold is reached **after** the expiration window (more than 25 sessions later), the record is treated as `expired`, not `invalidated`. The implementation enforces this by limiting the invalidation scan to the expiration window.

## Counting Buckets

`d5_count`, `d15_count`, and `d25_count` count active records satisfying `age_sessions <= N`. Note this includes age 0..N inclusive (N+1 sessions). Reports phrase this as "within N elapsed sessions" rather than "直近 N 取引日" because the latter usually means age 0..N-1.

The d25 bucket and the 25-session expiration are aligned: a record at exactly age=25 is still active and still counted in d25. A record at age=26 is expired and excluded from d25.

## Cluster Interpretation
General IBD heuristics:

- 4-5 distribution days in 4-5 weeks is a meaningful warning.
- 6+ distribution days is typically a "Market in Correction" signal.
- A cluster concentrated in the last 5-10 sessions matters more than evenly distributed days.

This skill encodes a deterministic translation:

| Risk | Trigger |
|------|---------|
| NORMAL | `d25 <= 2` |
| CAUTION | `d25 >= 3` |
| HIGH | `d25 >= 5` OR `d15 >= 3` OR `d5 >= 2` |
| SEVERE | `d25 >= 6` OR `d15 >= 4` OR (`market_below_21ema_or_50ma` AND `d25 >= 5`) |

The MA filter (`market_below_21ema_or_50ma`) only escalates to SEVERE when both the 21EMA and the 50SMA are below the latest close. If either MA cannot be computed (insufficient data), the filter is `None` and SEVERE escalation is skipped — see `audit_flags = ["insufficient_data_for_moving_average"]`.

## TQQQ Considerations
TQQQ targets 3x daily Nasdaq returns. In drawn-out correction phases, daily compounding of negative returns produces deep drawdowns even if cumulative Nasdaq returns are mild. Holding 100% TQQQ through a HIGH/SEVERE state has historically produced material left-tail risk. The exposure policy (see `tqqq_exposure_policy.md`) cuts TQQQ exposure faster than QQQ for the same risk level.

## What This Skill Does NOT Do
- It does not declare a market top. Tops are confirmed by additional signals (broken 50DMA on the major index, leadership breakdown, etc.).
- It does not produce buy signals. Use `ftd-detector` (Follow-Through Day) for the offensive counterpart.
- It does not act on intraday volume. Stalling days (volume up, price flat) are intentionally out of scope for v1.
- It does not execute trades.

## References
- William J. O'Neil, *How to Make Money in Stocks*, McGraw-Hill (multiple editions).
- IBD Big Picture columns: distribution day counts and cluster interpretations.

### Referencia: references/tqqq_exposure_policy.md

# TQQQ / QQQ Exposure Policy

## Why TQQQ Needs A Different Policy

TQQQ targets 3x daily returns of the Nasdaq-100. Two structural facts make it more dangerous in distribution clusters than QQQ:

1. **Daily compounding decay.** In choppy or trending-down markets, 3x daily reset compounds losses geometrically. A -1% / -1% Nasdaq sequence translates to roughly -5.91% TQQQ, not -6%.
2. **Larger drawdowns from the same correction.** A 10% Nasdaq pullback typically produces a 25-35% TQQQ drawdown depending on path.

The IBD distribution day signal warns of institutional selling pressure that is not yet captured by trend/MA filters alone. When that signal fires, exposure should be cut faster on TQQQ than on QQQ.

## Policy Mapping

### TQQQ
| Risk | Recommended Action | Target Exposure | Trailing Stop Cap |
|------|--------------------|-----------------|-------------------|
| NORMAL | HOLD_OR_FOLLOW_BASE_STRATEGY | 100% | base |
| CAUTION | AVOID_NEW_ADDS | 75% | min(base, 7%) |
| HIGH | REDUCE_EXPOSURE | 50% | min(base, 5%) |
| SEVERE | CLOSE_TQQQ_OR_HEDGE | 25% | min(base, 3%) |

Alternative actions surfaced for TQQQ:
- HIGH → `SWITCH_PARTIAL_TO_QQQ`
- SEVERE → `SWITCH_TO_QQQ_OR_CASH`

### QQQ
| Risk | Recommended Action | Target Exposure | Trailing Stop Cap |
|------|--------------------|-----------------|-------------------|
| NORMAL | HOLD_OR_FOLLOW_BASE_STRATEGY | 100% | base |
| CAUTION | AVOID_NEW_ADDS | 100% (no cut) | min(base, 8%) |
| HIGH | REDUCE_EXPOSURE | 75% | min(base, 6%) |
| SEVERE | REDUCE_EXPOSURE_OR_HEDGE | 50% | min(base, 5%) |

QQQ does not need to drop to 25-50% at SEVERE because daily compounding hurts it less than TQQQ.

## Trailing Stop Cap Rule
The skill always uses **the tighter of** the user's `base_trailing_stop_pct` and the policy cap. It never widens the trailing stop. If the user provides a base stop already tighter than the policy cap (e.g. base 4%, policy cap 5% at HIGH), the user's value wins.

## What's Out Of Scope
- Position sizing in shares: use `position-sizer`.
- Tax-aware lot selection: not addressed by this skill.
- Hedge instrument selection: the action is named (`CLOSE_TQQQ_OR_HEDGE`) but instrument choice is up to the operator.

## Operator Notes
- The policy is deterministic. Adjust `risk_thresholds` in `config/default.yaml` to change the bands; changing exposure targets requires editing `exposure_policy.py` (deliberate, since the bands are calibrated to TQQQ leverage characteristics).
- The recommendation is just that — a recommendation. The skill never executes orders.


---

## SKILL: lp-math

- Fuente: `agiprolabs/claude-trading-skills` → `skills/lp-math` (MIT)
- Cuándo usarla: AMM liquidity provision mathematics including constant-product, concentrated liquidity, price impact, and LP share calculations
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/lp-math/` (amm_calculator.py, clmm_calculator.py)

# LP Math — AMM Liquidity Provision Mathematics

Automated Market Makers (AMMs) replace traditional orderbooks with liquidity pools. Instead of matching buyers and sellers, a mathematical formula determines prices based on reserve ratios. Liquidity providers (LPs) deposit both assets into a pool and earn fees from every trade.

Understanding the math behind AMMs is essential for:
- Evaluating whether providing liquidity is profitable after impermanent loss
- Estimating price impact before executing large trades
- Comparing capital efficiency across pool types (constant product vs concentrated)
- Calculating expected fee revenue for a given pool position

**Related skills**: See `impermanent-loss` for IL calculations, `yield-analysis` for LP yield modeling, `liquidity-analysis` for pool depth assessment.

---

## 1. Constant Product AMM (xy = k)

The foundational AMM model used by Raydium V4 and most Solana DEXes.

### Core Invariant

```
x * y = k
```

Where:
- `x` = reserve amount of token X (e.g., SOL)
- `y` = reserve amount of token Y (e.g., USDC)
- `k` = constant product (increases over time from fees)

### Spot Price

```
P = x / y    (price of Y in terms of X)
P = y / x    (price of X in terms of Y)
```

For a pool with 100 SOL and 10,000 USDC: price of SOL = 10,000 / 100 = 100 USDC.

### Trade Execution

When a trader swaps Δx of token X into the pool:

```python
# Output amount (before fees)
delta_y = y * delta_x / (x + delta_x)

# With fee (e.g., 0.3%)
delta_y_after_fee = delta_y * (1 - fee_rate)

# New reserves
x_new = x + delta_x
y_new = y - delta_y_after_fee
```

The key insight: larger trades get worse prices because each unit moves the ratio further.

### Inverse Calculation

To get a specific output amount Δy, the required input is:

```python
delta_x = x * delta_y / (y - delta_y)
```

### Price After Trade

```python
price_new = y_new / x_new
```

### Worked Example

Pool: 100 SOL / 10,000 USDC (k = 1,000,000), fee = 0.3%

Buy 5 SOL worth of USDC:
1. Gross output: `10,000 * 5 / (100 + 5) = 476.19 USDC`
2. Fee: `476.19 * 0.003 = 1.43 USDC`
3. Net output: `474.76 USDC`
4. Effective price: `474.76 / 5 = 94.95 USDC/SOL` (vs spot 100)
5. Price impact: `(100 - 94.95) / 100 = 5.05%`
6. New reserves: 105 SOL / 9,525.24 USDC
7. New k: `105 * 9,525.24 = 1,000,150.2` (k increased from fees)

See `references/amm_formulas.md` for complete derivations.

---

## 2. Concentrated Liquidity (CLMM)

Used by Orca Whirlpool, Raydium CLMM, and Meteora DLMM. Liquidity is only active within a chosen price range [P_lower, P_upper].

### Key Concepts

```
L = sqrt(x * y)           # Liquidity within the active range
price_at_tick = 1.0001^tick  # Tick-to-price conversion
```

### Capital Efficiency

Concentrating liquidity in a narrow range provides more depth per dollar:

```python
# Capital efficiency ratio
efficiency = sqrt(P_upper / P_lower) / (sqrt(P_upper / P_lower) - 1)

# Example: ±5% range around $100 SOL
P_lower, P_upper = 95, 105
efficiency = sqrt(105/95) / (sqrt(105/95) - 1)  # ≈ 20.5x
```

A ±5% range is ~20x more capital-efficient than full-range, but the position goes 100% into one asset if price moves outside the range.

### Position Value

For a CLMM position with liquidity L in range [P_lower, P_upper] at current price P:

```python
if P <= P_lower:
    # All in token X (below range)
    value_x = L * (1/sqrt(P_lower) - 1/sqrt(P_upper))
    value_y = 0
elif P >= P_upper:
    # All in token Y (above range)
    value_x = 0
    value_y = L * (sqrt(P_upper) - sqrt(P_lower))
else:
    # In range — holds both tokens
    value_x = L * (1/sqrt(P) - 1/sqrt(P_upper))
    value_y = L * (sqrt(P) - sqrt(P_lower))
```

### Range Strategy Comparison

| Range | Efficiency | IL Risk | Fee Capture | Best For |
|-------|-----------|---------|-------------|----------|
| ±2% | ~50x | Very high | High if in range | Stablecoins, tight pegs |
| ±5% | ~20x | High | Good for trending | Active management |
| ±25% | ~4x | Moderate | Consistent | Semi-passive |
| ±100% | ~2x | Low | Lower per $ | Passive, volatile pairs |
| Full range | 1x | Baseline | Always earning | Set and forget |

See `references/amm_formulas.md` for full CLMM derivations.

---

## 3. Price Impact

### Constant Product Impact

```python
# Price impact as a fraction
price_impact = delta_x / (x + delta_x)

# As percentage of pool
pool_fraction = trade_value / pool_tvl

# Rule of thumb: impact ≈ 2 * pool_fraction for constant product
```

### Multi-Hop Impact

For a route through multiple pools, compound the impacts:

```python
def multi_hop_impact(hops: list[dict]) -> float:
    """Calculate total price impact across route legs.

    Args:
        hops: List of {reserve_in, trade_amount} for each leg.

    Returns:
        Total price impact as a fraction.
    """
    remaining = 1.0
    for hop in hops:
        leg_impact = hop["trade_amount"] / (hop["reserve_in"] + hop["trade_amount"])
        remaining *= (1 - leg_impact)
    return 1 - remaining
```

### Impact Thresholds

| Impact | Assessment | Action |
|--------|-----------|--------|
| < 0.1% | Negligible | Proceed normally |
| 0.1–0.5% | Low | Acceptable for most trades |
| 0.5–2% | Moderate | Consider splitting across pools |
| 2–5% | High | Split trade, use TWAP |
| > 5% | Severe | Reduce size or find deeper pools |

---

## 4. LP Share Calculations

### Initial Deposit (Empty Pool)

```python
shares = sqrt(x_deposited * y_deposited)
```

The first depositor sets the ratio and receives shares equal to the geometric mean.

### Subsequent Deposits

```python
shares_minted = min(
    x_added / x_reserve,
    y_added / y_reserve
) * total_shares
```

Deposits must be proportional to the current reserve ratio. Any excess of one token is not used (or returned, depending on implementation).

### Withdrawal

```python
x_out = (shares_burned / total_shares) * x_reserve
y_out = (shares_burned / total_shares) * y_reserve
```

You always receive both tokens in the current ratio.

### Share Value

```python
share_value = pool_tvl / total_shares
your_value = your_shares * share_value
```

---

## 5. Fee Accrual

Fees accumulate inside the pool, increasing k:

```python
# Before trade: k = x * y
# After trade with fee:
# k_new = (x + delta_x) * (y - delta_y_net) > k
# The difference is the fee retained in the pool

# Fee APR estimation
daily_volume = 500_000  # USD
fee_rate = 0.003        # 0.3%
daily_fees = daily_volume * fee_rate  # $1,500
tvl = 2_000_000         # $2M pool
fee_apr = (daily_fees * 365) / tvl    # 27.4%
```

For CLMM positions, fee earnings depend on:
- Whether price stays within your range (out-of-range = no fees)
- Your share of active liquidity in that range
- Total volume routed through the pool

```python
# CLMM fee estimation
your_liquidity = 50_000     # Your L
total_liquidity = 1_000_000  # Total L in your tick range
your_share = your_liquidity / total_liquidity  # 5%
your_daily_fees = daily_fees * your_share  # $75
```

---

## 6. Solana Pool Types

### Raydium V4 (Constant Product)

- Model: Standard xy = k
- Fee: 0.25% (0.22% to LP, 0.03% to RAY buyback)
- Best for: New token launches, volatile pairs
- Note: Integrated with OpenBook for limit order flow

### Orca Whirlpool (Concentrated Liquidity)

- Model: Concentrated liquidity with tick spacing
- Fee tiers: 0.01%, 0.05%, 0.3%, 1%
- Position: Represented as NFT (each position is unique)
- Best for: Major pairs (SOL/USDC), stablecoin pairs

### Raydium CLMM

- Model: Concentrated liquidity (similar to Uniswap V3)
- Tick spacing: 1, 10, 60, 200
- Fee tiers: 0.01%, 0.05%, 0.25%, 1%
- Best for: Pairs with predictable ranges

### Meteora DLMM (Dynamic Liquidity Market Maker)

- Model: Discrete bins instead of continuous ticks
- Strategies: Spot (uniform), Curve (concentrated), Bid-Ask (around current price)
- Fees: Dynamic, adjusting based on volatility
- Best for: Active LPs who rebalance frequently

See `references/pool_mechanics.md` for detailed mechanics and comparison.

---

## 7. Practical Decision Framework

### Should You LP?

```
1. Calculate expected fee APR
2. Estimate impermanent loss for expected price movement
3. Net return = fee APR - IL
4. Compare to simply holding the assets
```

### Which Pool Type?

```
Stablecoin pair     → CLMM with tight range (±0.5%)
Major pair (SOL/USDC) → CLMM with moderate range (±10-25%)
New/volatile token  → Constant product (full range)
Active management   → Meteora DLMM with dynamic rebalancing
```

### Position Sizing for LP

```python
# Never LP more than you can afford to lose to IL
max_lp_allocation = portfolio_value * 0.20  # 20% max in any single pool

# For volatile pairs, reduce further
volatility_adjustment = 1 - (annualized_vol / 2)  # Scale down for vol
adjusted_allocation = max_lp_allocation * max(0.1, volatility_adjustment)
```

---

## Files

### References
- `references/amm_formulas.md` — Complete mathematical derivations for constant product and concentrated liquidity AMMs
- `references/pool_mechanics.md` — Solana-specific pool mechanics for Raydium, Orca, and Meteora

### Scripts
- `scripts/amm_calculator.py` — Constant product AMM calculator with trade simulation, LP shares, and fee accrual
- `scripts/clmm_calculator.py` — Concentrated liquidity calculator with position valuation, capital efficiency, and range comparison

---

## Quick Reference

| Formula | Expression |
|---------|-----------|
| Constant product | `x * y = k` |
| Spot price | `P = y / x` |
| Trade output | `Δy = y * Δx / (x + Δx)` |
| Required input | `Δx = x * Δy / (y - Δy)` |
| Price impact | `Δx / (x + Δx)` |
| Initial LP shares | `sqrt(x * y)` |
| Subsequent shares | `min(Δx/x, Δy/y) * total` |
| Fee APR | `(daily_fees * 365) / TVL` |
| CLMM efficiency | `sqrt(P_u/P_l) / (sqrt(P_u/P_l) - 1)` |
| Tick to price | `1.0001^tick` |

### Referencia: references/amm_formulas.md

# AMM Formulas — Complete Derivations

## Constant Product AMM (xy = k)

### Price from Reserves

For a pool with reserves `x` (token X) and `y` (token Y):

```
Spot price of X in terms of Y:  P_x = y / x
Spot price of Y in terms of X:  P_y = x / y
```

The price is simply the ratio of reserves. This is the marginal price — the price for an infinitesimally small trade.

### Trade Execution: Selling Token X for Token Y

A trader deposits `Δx` of token X and receives `Δy` of token Y.

The invariant must hold after the trade (ignoring fees):

```
(x + Δx) * (y - Δy) = k = x * y
```

Solving for Δy:

```
y - Δy = x * y / (x + Δx)
Δy = y - x * y / (x + Δx)
Δy = y * (1 - x / (x + Δx))
Δy = y * Δx / (x + Δx)
```

**Key result**: `Δy = y * Δx / (x + Δx)`

### Inverse: Required Input for Desired Output

If you want exactly `Δy` of token Y, how much token X do you need?

```
(x + Δx) * (y - Δy) = x * y
x + Δx = x * y / (y - Δy)
Δx = x * y / (y - Δy) - x
Δx = x * (y / (y - Δy) - 1)
Δx = x * Δy / (y - Δy)
```

**Key result**: `Δx = x * Δy / (y - Δy)`

Note: This diverges as `Δy → y` — you can never drain a pool completely.

### With Fees

Most AMMs charge a fee `f` (e.g., 0.003 for 0.3%). The fee is taken from the input:

```
effective_input = Δx * (1 - f)
Δy = y * effective_input / (x + effective_input)
```

After the trade, the new reserves are:

```
x_new = x + Δx                    # Full input added (fee stays in pool)
y_new = y - Δy                    # Output removed
k_new = x_new * y_new > k         # k increases because fee stays
```

The fee causes k to grow monotonically, which is how LPs earn returns.

### Price Impact

Effective execution price vs spot price:

```
spot_price = y / x
execution_price = Δy / Δx
price_impact = 1 - (execution_price / spot_price)
            = 1 - (y * x) / ((x + Δx) * Δx * (y/x))  # simplifies to:
            = Δx / (x + Δx)
```

**Key result**: Price impact = `Δx / (x + Δx)`

For small trades where `Δx << x`: impact ≈ `Δx / x`

### Worked Example

Pool: 100 SOL / 10,000 USDC. Fee: 0.3%.

**Trade**: Sell 5 SOL into the pool.

```
x = 100 SOL, y = 10,000 USDC, k = 1,000,000
Δx = 5 SOL, fee = 0.003

Step 1: Effective input
  effective = 5 * (1 - 0.003) = 4.985 SOL

Step 2: Output
  Δy = 10,000 * 4.985 / (100 + 4.985) = 474.76 USDC

Step 3: New reserves
  x_new = 100 + 5 = 105 SOL
  y_new = 10,000 - 474.76 = 9,525.24 USDC
  k_new = 105 * 9,525.24 = 1,000,150.2 (> 1,000,000)

Step 4: Prices
  Spot before: 10,000 / 100 = 100 USDC/SOL
  Execution:   474.76 / 5 = 94.95 USDC/SOL
  Spot after:  9,525.24 / 105 = 90.72 USDC/SOL
  Impact:      5 / (100 + 5) = 4.76%

Step 5: Fees earned by LPs
  Fee in USDC terms: 474.76 * 0.003 / (1 - 0.003) ≈ 1.43 USDC
```

---

## Concentrated Liquidity (CLMM)

### Virtual Reserves

In a CLMM, liquidity `L` is concentrated in range `[P_lower, P_upper]`. The relationship to virtual reserves:

```
L = sqrt(x_virtual * y_virtual)
L² = x_virtual * y_virtual
```

Where virtual reserves represent what the pool "acts like" within the range.

### Real vs Virtual Reserves

Real token amounts for liquidity `L` in range `[P_a, P_b]` at current price `P`:

```
x_real = L * (1/sqrt(P) - 1/sqrt(P_b))     when P_a ≤ P ≤ P_b
y_real = L * (sqrt(P) - sqrt(P_a))          when P_a ≤ P ≤ P_b
```

Outside the range:
```
If P < P_a:  x_real = L * (1/sqrt(P_a) - 1/sqrt(P_b)),  y_real = 0
If P > P_b:  x_real = 0,  y_real = L * (sqrt(P_b) - sqrt(P_a))
```

### Position Value

Total value in terms of token Y (e.g., USDC):

```
If P ≤ P_a:
  V = L * (1/sqrt(P_a) - 1/sqrt(P_b)) * P    # All token X, valued at P

If P_a < P < P_b:
  V = L * (sqrt(P) - sqrt(P_a))               # Y component
    + L * (1/sqrt(P) - 1/sqrt(P_b)) * P       # X component valued at P
  V = L * (2*sqrt(P) - sqrt(P_a) - P/sqrt(P_b))

If P ≥ P_b:
  V = L * (sqrt(P_b) - sqrt(P_a))             # All token Y
```

### Liquidity from Deposit

Given a deposit of `Δx` and `Δy` in range `[P_a, P_b]` at price `P`:

```
L_from_x = Δx / (1/sqrt(P) - 1/sqrt(P_b))
L_from_y = Δy / (sqrt(P) - sqrt(P_a))
L = min(L_from_x, L_from_y)
```

The minimum ensures the deposit is balanced for the current price.

### Capital Efficiency

A CLMM position in range `[P_a, P_b]` provides the same depth as a full-range position with:

```
efficiency = sqrt(P_b / P_a) / (sqrt(P_b / P_a) - 1)
```

Examples:
```
±1%  range:  P_b/P_a = 1.02/0.98 = 1.0408 → efficiency ≈ 50x
±5%  range:  P_b/P_a = 1.05/0.95 = 1.1053 → efficiency ≈ 20x
±10% range:  P_b/P_a = 1.10/0.90 = 1.2222 → efficiency ≈ 10x
±25% range:  P_b/P_a = 1.25/0.75 = 1.6667 → efficiency ≈ 4x
±50% range:  P_b/P_a = 1.50/0.50 = 3.0000 → efficiency ≈ 2.4x
```

### Tick Math

Prices are discretized into ticks:

```
price_at_tick = 1.0001^tick
tick_at_price = log(price) / log(1.0001)
```

Tick spacing determines the minimum granularity of price ranges:
- Spacing 1: every tick (~0.01% price increment)
- Spacing 10: every 10 ticks (~0.1% price increment)
- Spacing 60: every 60 ticks (~0.6% price increment)

---

## LP Token Math

### Minting (Initial Deposit)

The first depositor defines the initial price and receives:

```
shares = sqrt(Δx * Δy) - MINIMUM_LIQUIDITY
```

`MINIMUM_LIQUIDITY` (typically 1000 units) is permanently locked to prevent manipulation.

### Minting (Subsequent Deposits)

```
shares = min(Δx / x_reserve, Δy / y_reserve) * total_supply
```

If the depositor provides tokens in a different ratio than the pool, only the proportional amount is used. The excess should be returned or the transaction reverts.

### Burning (Withdrawal)

```
x_out = (shares_burned / total_supply) * x_reserve
y_out = (shares_burned / total_supply) * y_reserve
```

This always returns both tokens in the current pool ratio.

### No-Arbitrage Property

LP share value tracks the pool value. If the pool price deviates from the market price, arbitrageurs trade until they converge. This means:

```
share_price = (x_reserve * P_x + y_reserve * P_y) / total_supply
```

The share price changes when:
1. Trades move the reserves (causes impermanent loss)
2. Fees accumulate (increases share value)
3. External rewards are added (if applicable)

Net LP return = Fee APR - Impermanent Loss + External Rewards

### Referencia: references/pool_mechanics.md

# Solana Pool Mechanics

## Raydium V4 (Constant Product)

### Overview
Standard xy = k AMM, the most common pool type on Solana for new token launches.

### Fee Structure
- Total fee: 0.25% per swap
- LP share: 0.22% (88% of fees go to LPs)
- Protocol: 0.03% (12% used for RAY buyback)

### OpenBook Integration
Raydium V4 pools are linked to an OpenBook (formerly Serum) market. This means:
- Limit orders from OpenBook can fill against the AMM liquidity
- Additional volume flows through the pool from orderbook traders
- Pool creation requires creating an OpenBook market first

### Pool Creation
1. Create an OpenBook market for the token pair
2. Initialize the Raydium AMM pool with initial liquidity
3. Set the initial price via the token ratio deposited
4. LP tokens are minted as SPL tokens

### Characteristics
- Always active across all prices (full range)
- Simple to understand and manage
- Higher impermanent loss for volatile pairs
- No position management needed after deposit
- Suitable for long-tail tokens with unpredictable price movement

---

## Orca Whirlpool (Concentrated Liquidity)

### Overview
Concentrated liquidity AMM similar to Uniswap V3. LPs choose a price range for their liquidity.

### Fee Tiers
| Tier | Fee | Tick Spacing | Best For |
|------|-----|-------------|----------|
| 0.01% | 1 bp | 1 | Stablecoin pairs (USDC/USDT) |
| 0.05% | 5 bp | 8 | Correlated pairs |
| 0.30% | 30 bp | 64 | Standard pairs (SOL/USDC) |
| 1.00% | 100 bp | 128 | Exotic/volatile pairs |

### Position Representation
Each LP position is an NFT. This means:
- Positions are non-fungible (each has unique range)
- Can transfer or sell positions
- Multiple positions in the same pool at different ranges
- Position tracks uncollected fees separately

### Tick Spacing and Precision
- Tick spacing determines minimum range granularity
- Lower spacing = finer control but more gas for swaps crossing many ticks
- Price at tick i: `P = 1.0001^i`
- Ticks must be multiples of the tick spacing

### Fee Collection
Fees are not auto-compounded. LPs must:
1. Collect fees manually (transaction required)
2. Optionally re-deposit collected fees as new liquidity
3. Fees accrue in the tokens of the pool (not LP tokens)

### Characteristics
- Capital efficient for predictable ranges
- Requires active management for optimal returns
- Position goes inactive if price moves outside range
- Higher IL risk for narrow ranges
- Fee income concentrated among in-range LPs

---

## Raydium CLMM

### Overview
Raydium's concentrated liquidity implementation, similar to Orca Whirlpool.

### Fee Tiers and Tick Spacing
| Tier | Fee | Tick Spacing | Use Case |
|------|-----|-------------|----------|
| 0.01% | 1 bp | 1 | Stablecoins |
| 0.05% | 5 bp | 10 | Correlated assets |
| 0.25% | 25 bp | 60 | Major pairs |
| 1.00% | 100 bp | 200 | Volatile pairs |

### Differences from Orca Whirlpool
- Different tick spacing values (10 vs 8, 60 vs 64, etc.)
- Integrated with Raydium's broader ecosystem
- Different fee distribution mechanics
- Protocol fee taken from LP fees

### Position Management
- Positions are represented as on-chain accounts
- Can open multiple positions in the same pool
- Fees tracked per-position and collected manually
- Position can be closed at any time, returning tokens + uncollected fees

---

## Meteora DLMM (Dynamic Liquidity Market Maker)

### Overview
Uses discrete price bins instead of continuous ticks. Each bin holds liquidity at a single price point.

### Bin System
- Price space divided into discrete bins
- Each bin represents a fixed price: `price = (1 + bin_step)^bin_id`
- Bin step determines price granularity (e.g., 0.1% between bins)
- Active bin: the bin containing the current price

### Liquidity Distribution Strategies
| Strategy | Distribution | Best For |
|----------|-------------|----------|
| Spot | Uniform across bins | General purpose, passive LPs |
| Curve | Concentrated around current price | Active LPs expecting range-bound |
| Bid-Ask | Split around current price | Market makers |

### Dynamic Fees
Meteora adjusts fees based on market conditions:
- Base fee: Set at pool creation
- Variable fee: Increases with volatility
- Total fee = base_fee + variable_fee
- Variable component uses an exponential moving average of recent volatility

### Single-Sided Deposits
Unlike constant product pools, DLMM allows:
- Depositing only one token (into bins on one side of the current price)
- Useful for building a position gradually
- Deposit only token X in bins above current price (limit sell behavior)
- Deposit only token Y in bins below current price (limit buy behavior)

### Characteristics
- Most flexible liquidity distribution
- Dynamic fees protect LPs during volatile periods
- Single-sided deposits enable limit-order-like strategies
- Bins make position management more intuitive than ticks
- Rebalancing is straightforward: remove from old bins, add to new bins

---

## Comparison Table

| Feature | Raydium V4 | Orca Whirlpool | Raydium CLMM | Meteora DLMM |
|---------|-----------|---------------|-------------|-------------|
| Model | xy = k | Concentrated | Concentrated | Discrete bins |
| Capital efficiency | 1x | Up to 4000x | Up to 4000x | Up to 4000x |
| Fee tiers | 0.25% fixed | 4 tiers | 4 tiers | Dynamic |
| Position type | Fungible LP token | NFT | Account | Account |
| Active management | Not needed | Recommended | Recommended | Recommended |
| Range selection | Full range only | Custom range | Custom range | Custom bins |
| Single-sided deposit | No | No | No | Yes |
| Fee auto-compound | Yes (in k) | No (manual) | No (manual) | No (manual) |
| Best for | New tokens | Major pairs | Major pairs | Active LPs |
| Complexity | Low | Medium | Medium | Medium-High |

---

## Pool Selection Guide

### By Asset Type
- **Stablecoin pairs**: CLMM with tight range (±0.5%), lowest fee tier
- **Major pairs (SOL/USDC)**: CLMM with ±10-25% range, 0.3% fee tier
- **New token launches**: Raydium V4 constant product
- **Volatile meme tokens**: Raydium V4 or DLMM with wide distribution
- **Actively managed**: Meteora DLMM with frequent rebalancing

### By LP Style
- **Passive**: Raydium V4 (set and forget, no range to manage)
- **Semi-active**: CLMM with wide range, rebalance weekly
- **Active**: Meteora DLMM, rebalance daily based on volatility
- **Professional**: Multiple narrow CLMM positions, algorithmic rebalancing


---

## SKILL: macro-rates-monitor

- Fuente: `anthropics/financial-services` → `plugins/partner-built/lseg/skills/macro-rates-monitor` (Apache-2.0)
- Cuándo usarla: Build macroeconomic and rates dashboards combining macro indicators, yield curves, inflation breakevens, and swap rates. Use when monitoring macro conditions, analyzing yield curve shape, decomposing real vs nominal rates, assessing policy rate expectations, or evaluating financial conditions.

# Macroeconomic and Rates Monitor

You are an expert macro strategist and rates analyst. Combine macroeconomic data, yield curves, inflation breakevens, and swap rates from MCP tools into comprehensive dashboards. Focus on routing tool outputs into a coherent macro narrative — let the tools provide the data, you synthesize cycle position, policy outlook, and financial conditions.

## Core Principles

Macro analysis synthesizes multiple indicators into a narrative. Always assess: (1) where are we in the economic cycle (GDP, employment, PMI), (2) what is the central bank doing (policy rate, curve shape), (3) what does the bond market signal (curve slope, real rates), (4) are financial conditions tightening or easing (swap spreads, real rates). Start broad, drill down.

## Available MCP Tools

- **`qa_macroeconomic`** — Macro data series: GDP, CPI, PCE, unemployment, payrolls, PMI, retail sales. Multiple countries and frequencies. Search by mnemonic pattern or description.
- **`interest_rate_curve`** — Government yield curves and swap curves. Two-phase: list then calculate. Use for curve shape and slope analysis.
- **`inflation_curve`** — Inflation breakeven curves and real yields. Two-phase: search then calculate. Use for real rate decomposition.
- **`ir_swap`** — Swap rates by tenor and currency. Two-phase: list templates then price. Use to compute swap spreads.
- **`tscc_historical_pricing_summaries`** — Historical pricing data. Use for historical yield context and trend analysis.

## Tool Chaining Workflow

1. **Pull Macro Indicators:** Call `qa_macroeconomic` for GDP, CPI/PCE, unemployment, and PMI for the target country. Retrieve latest values and recent series.
2. **Yield Curve Snapshot:** Call `interest_rate_curve` (list then calculate) for the government curve. Extract yields at standard tenors. Compute 2s10s and 3M-10Y slopes. Classify curve shape.
3. **Inflation Decomposition:** Call `inflation_curve` (search then calculate). Compute real rates = nominal minus breakeven at each tenor. Assess whether real rates are accommodative or restrictive.
4. **Swap Spreads:** Call `ir_swap` (list then price) at 2Y, 5Y, 10Y. Compute swap spread = swap rate minus government yield at each tenor. Assess financial conditions.
5. **Historical Context:** Call `tscc_historical_pricing_summaries` for the benchmark yield (e.g., 10Y). Assess where current yields sit vs recent history.
6. **Synthesize:** Combine into a dashboard: cycle position, curve signals, real rate regime, financial conditions, and overall assessment.

## Macro Search Patterns

When querying `qa_macroeconomic`, use wildcard patterns to discover mnemonics:
- US: "US\*GDP\*", "US\*CPI\*", "US\*PCE\*", "US\*UNEMP\*"
- Eurozone: "EZ\*GDP\*", "EZ\*HICP\*"
- UK: "UK\*GDP\*", "UK\*CPI\*"
- Prefer seasonally adjusted series. Monthly for most indicators; GDP is quarterly.

## Output Format

### Macro Summary
| Indicator | Current | Prior | Direction | Signal |
|-----------|---------|-------|-----------|--------|
| GDP Growth | ...% | ...% | ... | Expansion/Contraction |
| Core Inflation (YoY) | ...% | ...% | ... | Above/At/Below target |
| Unemployment | ...% | ...% | ... | Tight/Balanced/Slack |
| PMI Manufacturing | ... | ... | ... | Expansion/Contraction |

### Yield Curve Snapshot
Present yields at key tenors (3M, 2Y, 5Y, 10Y, 30Y). Highlight 2s10s and 3M-10Y slopes. Note curve shape: normal / flat / inverted / humped.

### Real Rate Decomposition
| Tenor | Nominal | Breakeven | Real Rate | Signal |
|-------|---------|-----------|-----------|--------|
| 5Y | ...% | ...% | ...% | Accommodative/Restrictive |
| 10Y | ...% | ...% | ...% | Accommodative/Restrictive |

### Swap Spread Table
| Tenor | Swap Rate | Govt Yield | Swap Spread (bp) | Signal |
|-------|-----------|------------|-------------------|--------|
| 2Y | ... | ... | ... | Normal/Elevated/Stressed |
| 5Y | ... | ... | ... | Normal/Elevated/Stressed |
| 10Y | ... | ... | ... | Normal/Elevated/Stressed |

### Overall Assessment
2-3 sentences on the macro-rates regime: cycle position, policy outlook, financial conditions, and key risks.


---

## SKILL: macro-regime-detector

- Fuente: `tradermonty/claude-trading-skills` → `skills/macro-regime-detector` (MIT)
- Cuándo usarla: Detect structural macro regime transitions (1-2 year horizon) using cross-asset ratio analysis. Analyze RSP/SPY concentration, yield curve, credit conditions, size factor, equity-bond relationship, and sector rotation to identify regime shifts between Concentration, Broadening, Contraction, Inflationary, and Transitional states. Run when user asks about macro regime, market regime change, structural rotation, or long-term market positioning.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/macro-regime-detector/` (requirements.txt, __init__.py, concentration_calculator.py, credit_conditions_calculator.py, equity_bond_calculator.py, sector_rotation_calculator.py, size_factor_calculator.py, utils.py, yield_curve_calculator.py, fmp_client.py, macro_regime_detector.py, report_generator.py …)

# Macro Regime Detector

Detect structural macro regime transitions using monthly-frequency cross-asset ratio analysis. This skill identifies 1-2 year regime shifts that inform strategic portfolio positioning.

## When to Use

- User asks about current macro regime or regime transitions
- User wants to understand structural market rotations (concentration vs broadening)
- User asks about long-term positioning based on yield curve, credit, or cross-asset signals
- User references RSP/SPY ratio, IWM/SPY, HYG/LQD, or other cross-asset ratios
- User wants to assess whether a regime change is underway

## Workflow

1. Load reference documents for methodology context:
   - `references/regime_detection_methodology.md`
   - `references/indicator_interpretation_guide.md`

2. Execute the main analysis script:
   ```bash
   python3 -m pip install -r skills/macro-regime-detector/requirements.txt
   uv run python3 skills/macro-regime-detector/scripts/macro_regime_detector.py --output-dir reports/
   ```
   This fetches 600 days of data for 9 ETFs. With an FMP key, the client tries
   FMP first and fetches Treasury rates (~10 API calls total), then falls back
   to yfinance for unavailable ETF history. Without an FMP key, it runs in
   yfinance-only mode and uses SHY/TLT as the yield-curve fallback.

   The detector fails closed and writes no report when none of its six
   components has usable data. Do not treat a missing report or non-zero exit
   as a valid low-transition regime.

3. Read the generated Markdown report and present findings to user.

4. Provide additional context using `references/historical_regimes.md` when user asks about historical parallels.

## Prerequisites

- **Python dependencies** (required): install `requirements.txt`, including yfinance and requests
- **FMP API Key** (optional): set `FMP_API_KEY` or pass `--api-key` to use FMP and Treasury data before the yfinance/SHY-TLT fallbacks
- The FMP free tier may not serve every ETF; unavailable symbols automatically use yfinance

## 6 Components

| # | Component | Ratio/Data | Weight | What It Detects |
|---|-----------|------------|--------|-----------------|
| 1 | Market Concentration | RSP/SPY | 25% | Mega-cap concentration vs market broadening |
| 2 | Yield Curve | 10Y-2Y spread | 20% | Interest rate cycle transitions |
| 3 | Credit Conditions | HYG/LQD | 15% | Credit cycle risk appetite |
| 4 | Size Factor | IWM/SPY | 15% | Small vs large cap rotation |
| 5 | Equity-Bond | SPY/TLT + correlation | 15% | Stock-bond relationship regime |
| 6 | Sector Rotation | XLY/XLP | 10% | Cyclical vs defensive appetite |

## 5 Regime Classifications

- **Concentration**: Mega-cap leadership, narrow market
- **Broadening**: Expanding participation, small-cap/value rotation
- **Contraction**: Credit tightening, defensive rotation, risk-off
- **Inflationary**: Positive stock-bond correlation, traditional hedging fails
- **Transitional**: Multiple signals but unclear pattern

## Output

- `macro_regime_YYYY-MM-DD_HHMMSS.json` — Structured data for programmatic use
- `macro_regime_YYYY-MM-DD_HHMMSS.md` — Human-readable report with:
  1. Current Regime Assessment
  2. Transition Signal Dashboard
  3. Component Details
  4. Regime Classification Evidence
  5. Portfolio Posture Recommendations

## Relationship to Other Skills

| Aspect | Macro Regime Detector | Market Top Detector | Market Breadth Analyzer |
|--------|----------------------|--------------------|-----------------------|
| Time Horizon | 1-2 years (structural) | 2-8 weeks (tactical) | Current snapshot |
| Data Granularity | Monthly (6M/12M SMA) | Daily (25 business days) | Daily CSV |
| Detection Target | Regime transitions | 10-20% corrections | Breadth health score |
| API Calls | ~10 | ~33 | 0 (Free CSV) |

## Script Arguments

```bash
python3 macro_regime_detector.py [options]

Options:
  --api-key KEY       FMP API key (default: $FMP_API_KEY)
  --output-dir DIR    Output directory (default: current directory)
  --days N            Days of history to fetch (default: 600)
```

## Resources

- `references/regime_detection_methodology.md` — Detection methodology and signal interpretation
- `references/indicator_interpretation_guide.md` — Guide for interpreting cross-asset ratios
- `references/historical_regimes.md` — Historical regime examples for context

### Referencia: references/historical_regimes.md

# Historical Regime Examples

Reference cases for the 5 regime classifications. Use these to contextualize current readings and identify historical parallels.

## Concentration Regimes

### 2023-2024: Magnificent Seven Dominance

- **RSP/SPY**: Declined from ~0.32 to ~0.29, a multi-year low
- **IWM/SPY**: Persistent underperformance of small-caps
- **Credit**: Stable to easing (HYG/LQD steady)
- **Characteristics**: Top 7 stocks drove ~60% of S&P 500 returns
- **Duration**: ~18 months
- **Resolution**: Early signs of broadening in late 2024 (RSP/SPY bottoming)
- **Portfolio posture**: Mega-cap growth overweight was the only winning strategy

### 2019-2020 (Pre-COVID): FAANG+ Concentration

- **RSP/SPY**: Gradual decline through 2019
- **IWM/SPY**: Small-cap underperformance
- **Ended**: Abruptly with COVID crash (exogenous shock)

## Broadening Regimes

### 2003-2004: Post-Dot-Com Recovery

- **RSP/SPY**: Rose significantly as value and small-caps recovered
- **IWM/SPY**: Strong small-cap outperformance
- **Credit**: HYG/LQD rising as credit conditions eased
- **Yield curve**: Steep (accommodative Fed)
- **Duration**: ~24 months
- **Portfolio posture**: Small-cap value, equal-weight strategies outperformed

### 2016-2017: Post-Election Broadening

- **RSP/SPY**: Rose as cyclicals and financials rallied
- **IWM/SPY**: Small-cap surge post-election
- **Credit**: Stable to improving
- **XLY/XLP**: Strong cyclical outperformance
- **Duration**: ~12 months
- **Portfolio posture**: Cyclicals, financials, small-cap growth

## Contraction Regimes

### 2007-2009: Global Financial Crisis

- **Credit**: HYG/LQD collapsed (credit freeze)
- **XLY/XLP**: Extreme defensive rotation
- **SPY/TLT**: Sharp decline as bonds rallied
- **Yield curve**: Initially inverted, then steepened dramatically
- **Duration**: ~18 months (bear phase)
- **Portfolio posture**: Cash, Treasuries, defensive sectors

### 2020 Q1: COVID Crash

- **Credit**: HYG/LQD dropped sharply in March
- **XLY/XLP**: Rapid defensive rotation
- **SPY/TLT**: Crashed as equities sold off
- **Duration**: ~6 weeks (shortest contraction on record)
- **Resolution**: Massive fiscal/monetary response triggered V-shaped recovery
- **Lesson**: Not all contractions are prolonged; policy response matters

## Inflationary Regimes

### 2022: Inflation Shock

- **Stock-bond correlation**: Turned positive (both fell together)
- **SPY/TLT**: Both declined simultaneously
- **10Y-2Y**: Deep inversion (most inverted since 1980s)
- **Yield curve**: Aggressive flattening then inversion
- **Duration**: ~12 months
- **Portfolio posture**: Energy, commodities, real assets, short-duration bonds
- **Key characteristic**: Traditional 60/40 portfolio failed as bonds didn't hedge

### 1970s Stagflation (Historical Reference)

- **Stock-bond correlation**: Persistently positive
- **Commodities**: Outperformed financial assets
- **Duration**: Extended (years)
- **Modern parallel**: 2022 showed echoes but resolved faster

## Transitional Regimes

### 2024 Q4 - 2025 Q1: Current Example

- **RSP/SPY**: Near historical lows (~0.297) but showing early bottoming signs
- **IWM/SPY**: Mixed signals, brief outperformance then reversal
- **Credit**: Stable (HYG/LQD holding)
- **Yield curve**: Normalizing from inversion
- **XLY/XLP**: Choppy, no clear direction
- **Interpretation**: Multiple indicators shifting but no clear new regime yet
- **Portfolio posture**: Maintain diversification, gradual position adjustments

### 2018: Failed Broadening

- **RSP/SPY**: Brief broadening attempt in early 2018
- **Credit**: Tightened in Q4 2018 (HYG selloff)
- **Resolution**: Fed pivot in early 2019 prevented full contraction
- **Lesson**: Transitional periods can resolve in any direction

## Regime Transition Patterns

### Common Sequences

1. **Concentration → Broadening**: Usually requires catalyst (Fed easing, fiscal stimulus, valuation compression in leaders)

2. **Broadening → Contraction**: Credit tightening is the typical trigger. Watch HYG/LQD for early warning.

3. **Contraction → Broadening**: Policy response (rate cuts, QE) → credit easing → small-cap recovery

4. **Any → Inflationary**: Positive stock-bond correlation is the key signal. Can emerge from either broadening or contraction.

### Transition Timing

- Average regime duration: 12-24 months
- Transition phase: Typically 3-6 months of ambiguous signals
- Early signals appear 2-4 months before consensus recognition
- MA crossovers (6M vs 12M) confirm after the fact but provide low false-positive rate

### False Signals

- 2018 Q1: Broadening signal reversed by Q4 (trade war + Fed tightening)
- 2015: Multiple signals of contraction that never fully materialized
- Lesson: Require 3+ months of sustained signals before high-conviction repositioning

### Referencia: references/indicator_interpretation_guide.md

# Indicator Interpretation Guide

Quick reference for interpreting each component's output values and signals.

## Component 1: Market Concentration (RSP/SPY)

**What it measures**: Relative performance of equal-weight S&P 500 vs cap-weight S&P 500.

| RSP/SPY Trend | Interpretation | Regime Signal |
|---------------|---------------|---------------|
| Declining | Mega-caps outperforming, market narrowing | Concentration |
| Rising | Broader participation, equal-weight catching up | Broadening |
| Bottoming + turning | Potential regime shift from concentration to broadening | Transition |

**Key levels** (approximate, varies over time):
- 0.28-0.29: Extreme concentration (2024 lows)
- 0.30-0.32: Moderate concentration
- 0.33+: Broadening phase

**Crossover interpretation**:
- Golden cross (6M > 12M): Broadening gaining momentum
- Death cross (6M < 12M): Concentration deepening

## Component 2: Yield Curve (10Y-2Y Spread)

**What it measures**: Shape of the Treasury yield curve, reflecting rate cycle position.

| Spread Level | Curve State | Typical Environment |
|-------------|-------------|-------------------|
| < -0.5% | Deeply inverted | Pre-recession, aggressive tightening |
| -0.5% to 0% | Inverted | Late-cycle, recession risk elevated |
| 0% to 0.5% | Flat/Normalizing | Transition period |
| 0.5% to 1.5% | Normal | Mid-cycle expansion |
| > 1.5% | Steep | Early recovery, accommodative policy |

**Direction signals**:
- Steepening: Either rates normalizing (bull steepener) or long end rising (bear steepener)
- Flattening: Late-cycle tightening or flight to long bonds

**Fallback (SHY/TLT proxy)**: When Treasury API is unavailable, SHY/TLT ratio provides a rough proxy. Rising SHY/TLT ≈ flattening curve. Less precise than actual spread data.

## Component 3: Credit Conditions (HYG/LQD)

**What it measures**: Risk appetite in credit markets — willingness to hold junk bonds vs investment grade.

| HYG/LQD Trend | Interpretation | Regime Signal |
|---------------|---------------|---------------|
| Rising | Credit risk appetite expanding | Risk-on, easing |
| Falling | Flight to quality | Risk-off, tightening |
| Stable | Established credit regime | No transition |

**Why it matters**: Credit markets often lead equity markets. HYG/LQD deterioration preceded the 2020 crash by ~2 weeks and the 2008 crisis by ~3 months.

**Warning levels**:
- Sharp drop (ROC < -3% over 3 months): Potential credit event
- Persistent decline with negative ROC: Late-cycle deterioration
- Stable with positive ROC: Supportive environment for risk assets

## Component 4: Size Factor (IWM/SPY)

**What it measures**: Relative performance of small-caps (Russell 2000) vs large-caps (S&P 500).

| IWM/SPY Trend | Interpretation | Regime Signal |
|---------------|---------------|---------------|
| Rising | Small-caps outperforming — economic optimism | Broadening |
| Falling | Large-cap preference — defensive/quality bias | Concentration |
| Diverging from RSP/SPY | Inconsistent signal — check credit conditions | Uncertain |

**Cycle position**:
- Small-cap outperformance often starts 3-6 months before economic recovery becomes consensus
- Small-cap underperformance accelerates in late-cycle as credit conditions tighten
- IWM/SPY and RSP/SPY usually move together; divergence warrants investigation

## Component 5: Equity-Bond Relationship (SPY/TLT + Correlation)

**What it measures**: Two aspects of the stock-bond relationship.

### SPY/TLT Ratio

| SPY/TLT Trend | Interpretation |
|---------------|---------------|
| Rising | Equities outperforming bonds (risk-on) |
| Falling | Bonds outperforming equities (risk-off) |

### Stock-Bond Correlation (6-month rolling)

| Correlation | Regime | Implication |
|-------------|--------|-------------|
| < -0.3 | Negative (normal) | Bonds effectively hedge equity risk |
| -0.3 to 0 | Mildly negative | Hedging works but weakened |
| 0 to 0.3 | Near zero | Transitional — hedging unreliable |
| > 0.3 | Positive (inflationary) | Both move together — diversification fails |

**Critical signal**: Correlation sign change (negative → positive or vice versa) is one of the most important regime signals. Positive correlation typically occurs during:
- Inflation shocks (2022)
- Stagflation concerns
- Central bank credibility crises

**Correlation bonus scoring**: When 6M and 12M correlation have opposite signs, an additional 20 points are added to the component score, reflecting the significance of this regime shift.

## Component 6: Sector Rotation (XLY/XLP)

**What it measures**: Consumer sentiment through discretionary vs staples spending preference.

| XLY/XLP Trend | Interpretation | Regime Signal |
|---------------|---------------|---------------|
| Rising | Consumer confidence, risk appetite | Risk-on, broadening |
| Falling | Defensive positioning, consumer caution | Risk-off, contraction |
| Stable | Established consumer sentiment | No transition |

**Why Consumer Discretionary vs Staples**:
- Most direct consumer-facing comparison
- Staples demand is relatively inelastic; discretionary is highly cyclical
- XLY includes Amazon, Tesla — captures both consumer and growth sentiment
- XLP is pure defensive (Procter & Gamble, Coca-Cola, Costco)

## Cross-Component Analysis

### Confirmation Patterns

**Strong Broadening Confirmation** (4+ components aligned):
- RSP/SPY ↑ + IWM/SPY ↑ + HYG/LQD stable/↑ + XLY/XLP ↑

**Strong Contraction Confirmation**:
- HYG/LQD ↓ + XLY/XLP ↓ + SPY/TLT ↓ + Yield curve steepening

**Inflationary Confirmation**:
- Stock-bond correlation positive + SPY/TLT ↓ + Yield curve behavior unusual

### Divergence Signals

- **RSP/SPY ↑ but HYG/LQD ↓**: Broadening without credit support — fragile
- **IWM/SPY ↑ but XLY/XLP ↓**: Small-cap rally without consumer backing — suspicious
- **Yield curve steepening but HYG/LQD ↓**: Rate cuts due to crisis, not growth

## Score Interpretation Quick Reference

| Composite Score | Zone | Action |
|----------------|------|--------|
| 0-20 | Stable | Maintain current positioning |
| 21-40 | Early Signal | Increase monitoring frequency |
| 41-60 | Transition Zone | Begin planning adjustments |
| 61-80 | Active Transition | Execute repositioning |
| 81-100 | Confirmed | Complete repositioning |

### Referencia: references/regime_detection_methodology.md

# Regime Detection Methodology

## Overview

The Macro Regime Detector uses a 3-layer signal detection approach applied to 6 cross-asset ratios, analyzed at monthly frequency with 6-month and 12-month Simple Moving Averages.

## Data Pipeline

```
Daily OHLCV (600 days, ~2.4 years)
  → Monthly Downsampling (last business day per month, ~24 points)
  → Ratio Calculation (e.g., RSP close / SPY close)
  → Moving Average Computation (6M SMA, 12M SMA)
  → Signal Detection (3 layers)
  → Component Scoring (0-100 per component)
  → Weighted Composite (6 components)
  → Regime Classification (decision tree)
  → Transition Probability Assessment
```

## Monthly Downsampling

Daily data is downsampled to monthly frequency by selecting the most recent trading day in each calendar month. This filters out daily noise and focuses on structural trends.

Why monthly: Regime transitions are structural (1-2 year) phenomena. Daily or weekly data introduces noise without adding signal for this time horizon.

## 3-Layer Signal Detection

### Layer 1: MA Crossover (0-40 points)

The primary signal is the relationship between the 6-month and 12-month SMA of each ratio.

- **Golden Cross**: 6M SMA crosses above 12M SMA (recent = 40pts, older = 20pts)
- **Death Cross**: 6M SMA crosses below 12M SMA (recent = 40pts, older = 20pts)
- **Converging**: SMAs within 1% gap, no crossover yet (0-25pts based on proximity)
- **None**: SMAs well separated, established trend (0pts)

Recency matters: A crossover 1-2 months ago is much more actionable than one 6+ months ago.

### Layer 2: Momentum Shift (0-30 points)

Compares 3-month Rate of Change (ROC) against 12-month ROC to detect early reversals.

- **Reversal Signal**: 12M ROC negative but 3M ROC positive (or vice versa). This means the long-term trend is one direction but short-term momentum has reversed — an early warning of transition.
- **Acceleration**: Strong 3M ROC in the same direction as 12M ROC confirms an existing move.

Scoring scales linearly with the magnitude of the short-term ROC (capped at 5%).

### Layer 3: Cross-Confirmation (0-30 points)

Checks alignment of multiple signals for confirmation:

1. Crossover is present (+10)
2. Short-term ROC confirms the crossover direction (+10)
3. SMA gap is widening (momentum building) (+10)

When all three align, the transition signal is strong (80-100 range).

## Component Scoring Scale

Each component produces a score from 0 to 100, representing **transition signal strength** (not "good" or "bad"):

| Range | Interpretation |
|-------|---------------|
| 0-20 | Stable regime, no transition signal |
| 20-40 | Minor fluctuation, possibly noise |
| 40-60 | Transition zone — MAs converging, potential crossover in 3-6 months |
| 60-80 | Clear transition signal — recent crossover or sharp momentum reversal |
| 80-100 | Strong confirmed transition — crossover + momentum + acceleration aligned |

## Composite Score

The 6 component scores are combined using fixed weights:

| Component | Weight | Rationale |
|-----------|--------|-----------|
| Market Concentration (RSP/SPY) | 25% | Primary indicator of market structure |
| Yield Curve (10Y-2Y) | 20% | Most reliable macro cycle indicator |
| Credit Conditions (HYG/LQD) | 15% | Leading indicator of financial stress |
| Size Factor (IWM/SPY) | 15% | Economic sentiment barometer |
| Equity-Bond (SPY/TLT) | 15% | Cross-asset risk regime |
| Sector Rotation (XLY/XLP) | 10% | Consumer sentiment proxy |

## Regime Classification

A decision-tree approach scores each of 5 possible regimes based on component directions:

### Scoring Rules

**Concentration** (+2 each):
- RSP/SPY direction = "concentrating"
- IWM/SPY direction = "large_cap_leading"
- Credit direction = stable/easing (+1)

**Broadening** (+2 each):
- RSP/SPY direction = "broadening"
- IWM/SPY direction = "small_cap_leading"
- Credit direction = stable/easing (+1)
- XLY/XLP direction = risk_on (+1)

**Contraction** (+2 each):
- Credit direction = "tightening"
- XLY/XLP direction = "risk_off"
- SPY/TLT direction = "risk_off" (+1)

**Inflationary** (+3):
- Stock-bond correlation = "positive"
- SPY/TLT direction = "risk_off" (+1)

**Transitional**: Assigned when 3+ components are signaling (score >= 40) but no regime scores >= 3.

### Confidence Levels

- **High**: Best regime score >= 4
- **Moderate**: Best regime score >= 3
- **Low**: Best regime score >= 2
- **Very Low**: Best regime score < 2

## Transition Probability

Combines signaling count and average component scores:

| Signaling Count | Avg Score | Probability |
|----------------|-----------|-------------|
| 4+ | >= 50 | High (70-90%) |
| 3+ | >= 40 | Moderate (40-60%) |
| 2+ | >= 30 | Low (20-40%) |
| < 2 | < 30 | Minimal (<20%) |

## Limitations

1. **Lagging by design**: Monthly frequency means signals appear weeks to months after daily-frequency indicators. This is intentional — the goal is structural confirmation, not early detection.

2. **False positives**: Converging MAs can generate transition signals that reverse before completing. Always check cross-component confirmation.

3. **Regime overlap**: Real markets often exhibit characteristics of multiple regimes simultaneously. The "Transitional" classification explicitly acknowledges this.

4. **Historical bias**: Regime classification rules are derived from post-2000 market patterns. Novel regimes may not fit existing categories.


---

## SKILL: market-breadth-analyzer

- Fuente: `tradermonty/claude-trading-skills` → `skills/market-breadth-analyzer` (MIT)
- Cuándo usarla: Quantifies market breadth health using TraderMonty's public CSV data. Generates a 0-100 composite score across 6 components (100 = healthy). No API key required. Use when user asks about market breadth, participation rate, advance-decline health, whether the rally is broad-based, or general market health assessment.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/market-breadth-analyzer/` (requirements.txt, __init__.py, bearish_signal_calculator.py, cycle_calculator.py, divergence_calculator.py, historical_context_calculator.py, ma_crossover_calculator.py, trend_level_calculator.py, csv_client.py, history_tracker.py, market_breadth_analyzer.py, provenance_contract.py …)

# Market Breadth Analyzer Skill

## Purpose

Quantify market breadth health using a data-driven 6-component scoring system (0-100). Uses TraderMonty's publicly available CSV data to measure how broadly the market is participating in a rally or decline.

**Score direction:** 100 = Maximum health (broad participation), 0 = Critical weakness.

**No API key required** - uses freely available CSV data from GitHub Pages.

## When to Use This Skill

**English:**
- User asks "Is the market rally broad-based?" or "How healthy is market breadth?"
- User wants to assess market participation rate
- User asks about advance-decline indicators or breadth thrust
- User wants to know if the market is narrowing (fewer stocks participating)
- User asks about equity exposure levels based on breadth conditions

**Japanese:**
- 「マーケットブレッドスはどうですか？」「市場の参加率は？」
- 「上昇は広がっている？」「一部の銘柄だけの上昇？」
- ブレッドス指標に基づくエクスポージャー判断
- 市場の健康度をデータで確認したい

## Prerequisites

- **Python 3.9+** with `requests` library (for fetching CSV data)
- **Internet access** to reach GitHub Pages URLs
- **No API keys required** - uses freely available public CSV data

## Difference from Breadth Chart Analyst

| Aspect | Market Breadth Analyzer | Breadth Chart Analyst |
|--------|------------------------|----------------------|
| Data Source | CSV (automated) | Chart images (manual) |
| API Required | None | None |
| Output | Quantitative 0-100 score | Qualitative chart analysis |
| Components | 6 scored dimensions | Visual pattern recognition |
| Repeatability | Fully reproducible | Analyst-dependent |

---

## Execution Workflow

### Phase 1: Execute Python Script

Run the analysis script. If using a nested or date-stamped `--output-dir` in cron runs, create it first; the history writer expects the directory to already exist.

```bash
mkdir -p reports/<routine-or-date>
python3 skills/market-breadth-analyzer/scripts/market_breadth_analyzer.py \
  --detail-url "https://tradermonty.github.io/market-breadth-analysis/market_breadth_data.csv" \
  --summary-url "https://tradermonty.github.io/market-breadth-analysis/market_breadth_summary.csv" \
  --output-dir reports/<routine-or-date>
```

For a simple ad-hoc run, omit `--output-dir` or use an existing directory. In scheduled cron runs from the repository root, prefer a repo-relative output directory such as `reports/after-close-YYYY-MM-DD` rather than an absolute path. If an absolute nested `--output-dir` unexpectedly fails at the history-writing step despite the directory existing, rerun once with the equivalent repo-relative path before treating the breadth analysis as unavailable.

The script will:
1. Fetch detail CSV (~2,500 rows, 2016-present) and summary CSV (8 metrics)
2. Validate data freshness (warn if > 5 days old)
3. Calculate all 6 component scores (with automatic weight redistribution if any component lacks data)
4. Generate composite score with zone classification
5. Track score history and compute trend (improving/deteriorating/stable)
6. Output JSON and Markdown reports

### Phase 2: Present Results

Present the generated Markdown report to the user, highlighting:
- Composite score and health zone
- Strongest and weakest components
- Recommended equity exposure level
- Key breadth levels to watch
- Any data freshness warnings

---

## 6-Component Scoring System

| # | Component | Weight | Key Signal |
|---|-----------|--------|------------|
| 1 | Breadth Level & Trend | **25%** | Current 8MA level + 200MA trend direction + 8MA direction modifier |
| 2 | 8MA vs 200MA Crossover | **20%** | Momentum via MA gap and direction |
| 3 | Peak/Trough Cycle | **20%** | Position in breadth cycle |
| 4 | Bearish Signal | **15%** | Backtested bearish signal flag |
| 5 | Historical Percentile | **10%** | Current vs full history distribution |
| 6 | S&P 500 Divergence | **10%** | Multi-window (20d + 60d) price vs breadth divergence |

**Weight Redistribution:** If any component lacks sufficient data (e.g., no peak/trough markers detected), it is excluded and its weight is proportionally redistributed among the remaining components. The report shows both original and effective weights.

**Score History:** Composite scores are persisted across runs (keyed by data date). The report includes a trend summary (improving/deteriorating/stable) when multiple observations are available.

## Health Zone Mapping (100 = Healthy)

| Score | Zone | Equity Exposure | Action |
|-------|------|-----------------|--------|
| 80-100 | Strong | 90-100% | Full position, growth/momentum favored |
| 60-79 | Healthy | 75-90% | Normal operations |
| 40-59 | Neutral | 60-75% | Selective positioning, tighten stops |
| 20-39 | Weakening | 40-60% | Profit-taking, raise cash |
| 0-19 | Critical | 25-40% | Capital preservation, watch for trough |

---

## Data Sources

**Detail CSV:** `market_breadth_data.csv`
- ~2,500 rows from 2016-02 to present
- Columns: Date, S&P500_Price, Breadth_Index_Raw, Breadth_Index_200MA, Breadth_Index_8MA, Breadth_200MA_Trend, Bearish_Signal, Is_Peak, Is_Trough, Is_Trough_8MA_Below_04

**Summary CSV:** `market_breadth_summary.csv`
- 8 aggregate metrics (average peaks, average troughs, counts, analysis period)

Both are publicly hosted on GitHub Pages - no authentication required.

## Output Files

- JSON: `market_breadth_YYYY-MM-DD_HHMMSS.json`
- Markdown: `market_breadth_YYYY-MM-DD_HHMMSS.md`
- History: `market_breadth_history.json` (persists across runs, max 20 entries)

## Reference Documents

### `references/breadth_analysis_methodology.md`
- Full methodology with component scoring details
- Threshold explanations and zone definitions
- Historical context and interpretation guide

### When to Load References
- **First use:** Load methodology reference for framework understanding
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

### Referencia: references/breadth_analysis_methodology.md

# Market Breadth Analysis Methodology

## Overview

Market breadth measures the degree of participation in a market move. A healthy advance is characterized by broad participation (many stocks rising), while a narrowing market (fewer stocks leading) often precedes corrections.

This methodology uses TraderMonty's breadth dataset to quantify market health across 6 dimensions, producing a composite score from 0 (critical) to 100 (maximum health).

---

## Data Description

### Breadth Index
The breadth index (0-1) measures the proportion of S&P 500 stocks trading above their 200-day moving average. Key derivatives:
- **Raw:** Daily breadth value (percentage of stocks above 200DMA)
- **8-day EMA (8MA):** Short-term exponentially weighted moving average (fast signal)
- **200-day EMA (200MA):** Long-term exponentially weighted moving average (trend filter)

**Important:** Both moving averages use **EMA** (Exponential Moving Average), not SMA. The source repository calculates them as `ewm(span=N, adjust=False)`. EMA gives more weight to recent data points, making it more responsive to changes than SMA.

### Key Thresholds
| Level | Interpretation |
|-------|---------------|
| 8MA > 0.70 | Very strong breadth - broad rally |
| 8MA > 0.60 | Healthy breadth - above average participation |
| 8MA > 0.50 | Neutral - about half of stocks participating |
| 8MA > 0.40 | Weakening - below average participation |
| 8MA < 0.40 | Extreme weakness - potential trough formation |
| 8MA < 0.20 | Crisis levels - rare, precedes major bottoms |

### Signal Flags
- **Breadth_200MA_Trend:** 1 = 200MA rising (bullish regime), -1 = 200MA falling (bearish regime). Uses hysteresis with threshold=0.001 to prevent whipsaw signals.
- **Bearish_Signal:** Backtested signal combining trend and momentum deterioration
- **Is_Peak / Is_Trough:** Cyclical turning points detected using `scipy.signal.find_peaks` with `distance=50, prominence=0.015` on the 200MA. This ensures at least 50 trading days (~10 weeks) between consecutive peaks/troughs and a minimum prominence of 0.015.
- **Is_Trough_8MA_Below_04:** Extreme trough marker detected with `prominence=0.02` on inverted 8MA values below 0.4.

### Pink Zone (Bearish Region)
The source repository's charts use a pink background to highlight the most dangerous market condition:

```
Pink Zone = (Breadth_200MA_Trend == -1) AND (8MA < 200MA)
```

This means the long-term trend is declining AND the short-term breadth has fallen below the long-term average. Historically, markets in the Pink Zone experience elevated volatility and downside risk. The Pink Zone is distinct from the Bearish_Signal flag - it is a structural condition that can persist for weeks or months.

---

## Component Details

### C1: Current Breadth Level & Trend (25%)

**Rationale:** The most direct measure of current market health. Higher 8MA means more stocks participating; uptrend in 200MA means the long-term structure is supportive.

**Weighting within component:**
- 8MA Level: 70% - immediate health snapshot
- 200MA Trend: 30% - longer-term regime confirmation

**8MA Direction Modifier:** A 5-day lookback on the 8MA itself adjusts the score based on the short-term direction of breadth. This ensures C1 considers not just the level, but whether breadth is accelerating or decelerating:

| Condition | Modifier | Rationale |
|-----------|----------|-----------|
| 8MA falling & level > 0.60 | -10 | Deceleration from a high level — early warning of potential peak |
| 8MA falling & level < 0.40 | +5 | Near-bottom with limited further downside — less penalty |
| 8MA rising & level < 0.60 | +5 | Early recovery bonus — breadth improving from a weak base |
| Otherwise | 0 | No adjustment needed |

**Key insight:** An 8MA of 0.65 in an uptrend (score ~80) is healthier than 0.65 in a downtrend (score ~62), because the downtrend context suggests the level may be transient. The direction modifier further differentiates: a falling 8MA at 0.65 signals emerging weakness (-10), while a rising 8MA at the same level confirms strength.

### C2: 8MA vs 200MA Crossover Dynamics (20%)

**Rationale:** The gap between fast and slow MAs reveals momentum. A wide positive gap means breadth is accelerating above trend; a negative gap means it's deteriorating below trend.

**Direction modifier:** When the 8MA is recovering (rising) while still below the 200MA, this early recovery signal adds +10. Conversely, when 8MA is falling while still above 200MA, this early deterioration signal subtracts -10.

**Key insight:** The crossover point (8MA crossing 200MA) is a significant signal. Bull markets maintain 8MA above 200MA; bear phases see 8MA below 200MA.

### C3: Peak/Trough Cycle Position (20%)

**Rationale:** Breadth moves in cycles. Knowing whether we are in the early, middle, or late phase of a cycle helps calibrate expectations.

**Cycle phases:**
1. **Trough → Early Recovery (0-20 days):** Highest potential for upside if 8MA is rising
2. **Sustained Recovery (21-60 days):** Confirmed recovery with decreasing upside magnitude
3. **Mature Recovery (60+ days):** Late-cycle, watch for next peak
4. **Post-Peak Decline (0-20 days):** Highest risk period
5. **Sustained Decline (21-60 days):** Deep correction territory
6. **Prolonged Decline (60+ days):** Potential bottom formation if 8MA starts rising

**Extreme trough bonus:** When 8MA drops below 0.4 at a trough, history shows these are often excellent long-term entry points, warranting a +10 bonus.

### C4: Bearish Signal Status (15%)

**Rationale:** The dataset includes a backtested bearish signal flag that combines multiple factors. Its value depends on context.

**Interpretation matrix:**
| Signal | Trend | Score | Meaning |
|--------|-------|-------|---------|
| Off | Up | 85 | All clear - no concerns |
| Off | Down | 50 | No immediate danger but bearish backdrop |
| On | Up | 30 | Warning in otherwise bullish environment |
| On | Down | 10 | Full bearish alignment |

**Context matters:** A bearish signal when 8MA is above 0.50 is less concerning (+15 adjustment) than one when 8MA is below 0.25 (-5 adjustment).

**Pink Zone integration:** When in the Pink Zone (200MA downtrend + 8MA below 200MA) but without an active bearish signal, a -10 penalty is applied to reflect structural weakness that the bearish flag alone may not capture.

### C5: Historical Percentile (10%)

**Rationale:** Knowing where current breadth stands relative to the full 10-year history provides framing. Is this level normal, unusually high, or unusually low?

**Overheated/oversold adjustments:** When current 8MA approaches the average peak level, a -10 penalty reflects elevated risk of mean reversion. When near the average trough level, a +10 bonus reflects contrarian opportunity.

### C6: S&P 500 vs Breadth Divergence (10%)

**Rationale:** The most dangerous market condition is when the index makes new highs but breadth is declining (fewer stocks participating). This divergence preceded major tops in 2000, 2007, and 2021.

**Multi-Window Analysis (20d + 60d):** Divergence is measured at two time scales and combined:
- **60-day window (weight 60%):** Captures structural, medium-term divergence
- **20-day window (weight 40%):** Detects short-term emerging divergence

Composite score = 60d_score x 0.6 + 20d_score x 0.4

**Early Warning flag:** When the 20-day window shows bearish divergence (score <= 25) while the 60-day window is still healthy (score >= 50), an Early Warning is triggered. This signals that short-term breadth deterioration has begun before it becomes visible in the structural window.

**Near-flat classification:** When both S&P 500 change and breadth change are below noise thresholds (|S&P %| < 0.5 and |breadth change| < 0.01), the window is classified as "Near-flat (insufficient movement)" with a neutral score of 50. This prevents misclassification of trivial movements as divergence or alignment signals.

**Key patterns (per window):**
- **S&P up + Breadth up:** Healthy, sustainable rally (70)
- **S&P up + Breadth down:** Dangerous narrow market (10-25)
- **S&P down + Breadth up:** Bullish divergence, potential bottom (65-80)
- **S&P down + Breadth down:** Consistent decline, wait for stabilization (30)
- **Both near-flat:** Neutral (50) - insufficient movement to classify

### Weight Redistribution

When a component has `data_available: False` (e.g., insufficient rows for divergence analysis), its weight is excluded and the remaining weights are proportionally redistributed:

```
effective_weight[i] = base_weight[i] / sum(base_weight[j] for all available j)
```

**Example:** If C6 (10%) is unavailable, the remaining 90% is redistributed:
- C1: 25/90 = 27.8%, C2: 20/90 = 22.2%, C3: 20/90 = 22.2%, C4: 15/90 = 16.7%, C5: 10/90 = 11.1%

**Zero-division guard:** If all components are unavailable, the composite score defaults to 50 with zone "Neutral" and a warning that the score is a reference value only.

**Data Quality Labels:**

| Available Components | Label | Interpretation |
|---------------------|-------|----------------|
| 6/6 | Complete | Full confidence |
| 4-5/6 | Partial | Interpret with caution |
| 0-3/6 | Limited | Low confidence |

---

## Composite Score Interpretation

### Zone Thresholds

| Score | Zone | Exposure | Key Actions |
|-------|------|----------|-------------|
| 80-100 | **Strong** | 90-100% | Full position sizing; growth/momentum strategies; wide stops |
| 60-79 | **Healthy** | 75-90% | Normal operations; standard risk management |
| 40-59 | **Neutral** | 60-75% | Selective; tighter stops; avoid speculative names |
| 20-39 | **Weakening** | 40-60% | Profit-taking; raise cash; defensive rotation |
| 0-19 | **Critical** | 25-40% | Capital preservation; hedging; watch for trough |

### Guidance Caution Warning

When the 8MA direction modifier is negative in C1 (Breadth Level & Trend) or C2 (MA Crossover), the report automatically appends a Caution warning to the Overall Assessment guidance. This alerts analysts that the zone-based guidance (e.g., "Normal operations") may be overly optimistic given the deteriorating short-term momentum.

The Caution warning also triggers additional protective actions in the Recommended Actions section:
- "Reduce new position sizes until 8MA stabilizes"
- "Tighten stop-loss levels on existing positions"

These are appended to the standard zone-based actions, not replacing them.

### Cross-Referencing with Other Skills

- **Market Top Detector:** If breadth is Weakening (20-39) AND top detector is Orange/Red, this is strong confirmation of topping conditions.
- **CANSLIM Screener:** In Strong/Healthy zones, CANSLIM stock selections have higher success rates.
- **Sector Analyst:** Weakening breadth often coincides with rotation from offensive to defensive sectors.

### Score History & Trend

The analyzer maintains a rolling history of composite scores to detect trend direction.

**Storage format:** JSON file (`market_breadth_history.json`) in the output directory, structured as an array of objects:

```json
[
  {"data_date": "2025-06-10", "composite_score": 72.3, "component_scores": {"breadth_level_trend": 80, "ma_crossover": 70, "...": "..."}, "recorded_at": "2025-06-10 14:30:00"},
  {"data_date": "2025-06-11", "composite_score": 68.1, "component_scores": {"breadth_level_trend": 75, "ma_crossover": 65, "...": "..."}, "recorded_at": "2025-06-11 09:15:00"}
]
```

**Key rules:**
- **Keyed by data date:** Each entry uses the latest data row's date, not the analysis run date.
- **Duplicate prevention:** If an entry with the same date already exists, it is overwritten (no duplicates).
- **Rolling window:** Maximum 20 entries retained. When the limit is reached, the oldest entry is pruned first.
- **Trend detection:** The delta between the first and last score in the most recent N entries (default N=5) determines the trend label:
  - `delta > 2` → "Improving"
  - `delta < -2` → "Deteriorating"
  - `-2 <= delta <= 2` → "Stable"

**Usage in reports:** The trend summary (`direction`, `delta`, `entries`) is included in both JSON and Markdown outputs, giving analysts a quick read on whether market breadth is accelerating or decelerating.

---

## Historical Context

### Average Values (from Summary CSV)
- **Average Peak (200MA):** ~0.729 - breadth cycles typically top around this level
- **Average Trough (8MA < 0.4):** ~0.232 - extreme troughs average around this level
- **Peak Count:** ~5 over 10 years (roughly every 2 years)
- **Trough Count:** ~10 extreme troughs (roughly twice per year on average)

### Notable Historical Patterns
- **COVID-19 (March 2020):** 8MA crashed to extreme lows, followed by one of the sharpest breadth recoveries in history
- **2022 Bear Market:** Sustained period of 8MA below 200MA with multiple bearish signals
- **2023 Recovery:** Gradual breadth improvement with 8MA crossing above 200MA

---

## Live Resources

- **Interactive Dashboard:** https://tradermonty.github.io/market-breadth-analysis/
- **Data CSV:** https://tradermonty.github.io/market-breadth-analysis/market_breadth_data.csv
- **Summary CSV:** https://tradermonty.github.io/market-breadth-analysis/market_breadth_summary.csv
- **Source Repository:** https://github.com/tradermonty/market-breadth-analysis

Data is automatically updated twice daily via GitHub Actions. CSV files are freely accessible without API keys.

---

## Limitations

1. **Lagging indicator:** Breadth data reflects what has happened, not what will happen. Use alongside forward-looking indicators.
2. **No sector granularity:** The breadth index is market-wide. A few large sectors can dominate the reading.
3. **CSV update frequency:** Data depends on TraderMonty's update schedule. Check data freshness before analysis.
4. **Single market:** Covers S&P 500 only. Does not reflect international markets, small caps, or other asset classes.
5. **No volume context:** The breadth index is price-based and does not incorporate volume data.


---

## SKILL: market-environment-analysis

- Fuente: `tradermonty/claude-trading-skills` → `examples/weekly-trade-strategy/.claude/skills/market-environment-analysis` (MIT)
- Cuándo usarla: Comprehensive market environment analysis and reporting tool. Analyzes global markets including US, European, Asian markets, forex, commodities, and economic indicators. Provides risk-on/risk-off assessment, sector analysis, and technical indicator interpretation. Triggers on keywords like market analysis, market environment, global markets, trading environment, market conditions, investment climate, market sentiment, forex analysis, stock market analysis, 相場環境, 市場分析, マーケット状況, 投資環境.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `examples/weekly-trade-strategy/.claude/skills/market-environment-analysis/` (requirements.txt, _market_calendar.py, market_utils.py)

# Market Environment Analysis

Comprehensive analysis tool for understanding market conditions and creating professional market reports anytime.

## Core Workflow

### 1. Initial Data Collection
Collect latest market data using web_search tool:
1. Major stock indices (S&P 500, NASDAQ, Dow, Nikkei 225, Shanghai Composite, Hang Seng)
2. Forex rates (USD/JPY, EUR/USD, major currency pairs)
3. Commodity prices (WTI crude, Gold, Silver)
4. US Treasury yields (2-year, 10-year, 30-year)
5. VIX index (Fear gauge)
6. Market trading status (open/close/current values)

### 2. Market Environment Assessment
Evaluate the following from collected data:
- **Trend Direction**: Uptrend/Downtrend/Range-bound
- **Risk Sentiment**: Risk-on/Risk-off
- **Volatility Status**: Market anxiety level from VIX
- **Sector Rotation**: Where capital is flowing

### 3. Report Structure

#### Standard Report Format:
```
1. Executive Summary (3-5 key points)
2. Global Market Overview
   - US Markets
   - Asian Markets
   - European Markets
3. Forex & Commodities Trends
4. Key Events & Economic Indicators
5. Risk Factor Analysis
6. Investment Strategy Implications
```

## Script Usage

### market_utils.py
Provides common functions for report creation:
```bash
# Generate report header
python scripts/market_utils.py

# Available functions:
- format_market_report_header(): Create header
- get_market_session_times(): Check trading hours
- categorize_volatility(vix): Interpret VIX levels
- format_percentage_change(value): Format price changes
```

## Reference Documentation

### Key Indicators Interpretation (references/indicators.md)
Reference when you need:
- Important levels for each index
- Technical analysis key points
- Sector-specific focus areas

### Analysis Patterns (references/analysis_patterns.md)
Reference when analyzing:
- Risk-on/Risk-off criteria
- Economic indicator interpretation
- Inter-market correlations
- Seasonality and market anomalies

## Output Examples

### Quick Summary Version
```
📊 Market Summary [2025/01/15 14:00]
━━━━━━━━━━━━━━━━━━━━━
【US】S&P 500: 5,123.45 (+0.45%)
【JP】Nikkei 225: 38,456.78 (-0.23%)
【FX】USD/JPY: 149.85 (↑0.15)
【VIX】16.2 (Normal range)

⚡ Key Events
- Japan GDP Flash
- US Employment Report

📈 Environment: Risk-On Continues
```

### Detailed Analysis Version
Start with executive summary, then analyze each section in detail.
Key clarifications:
1. Current market phase (Bullish/Bearish/Neutral)
2. Short-term direction (1-5 days outlook)
3. Risk events to monitor
4. Recommended position adjustments

## Important Considerations

### Timezone Awareness
- Consider all major market timezones
- US markets: Evening to early morning (Asian time)
- European markets: Afternoon to evening (Asian time)
- Asian markets: Morning to afternoon (Local time)

### Economic Calendar Priority
Categorize by importance:
- ⭐⭐⭐ Critical (FOMC, NFP, CPI, etc.)
- ⭐⭐ Important (GDP, Retail Sales, etc.)
- ⭐ Reference level

### Data Source Priority
1. Official releases (Central banks, Government statistics)
2. Major financial media (Bloomberg, Reuters)
3. Broker reports
4. Analyst consensus estimates

## Troubleshooting

### Data Collection Notes
- Check market holidays (holiday calendars)
- Be aware of daylight saving time changes
- Distinguish between flash and final data

### Market Volatility Response
1. First organize the facts
2. Reference historical similar events
3. Verify with multiple sources
4. Maintain objective analysis

## Customization Options

Adjust based on user's investment style:
- **Day Traders**: Intraday charts, order flow focus
- **Swing Traders**: Daily/weekly technicals emphasis
- **Long-term Investors**: Fundamentals, macro economics focus
- **Forex Traders**: Currency correlations, interest rate differentials
- **Options Traders**: Volatility analysis, Greeks monitoring

### Referencia: references/analysis_patterns.md

# Market Analysis Patterns

## Market Pattern Analysis

### Trend Identification
1. **Uptrend**
   - Higher highs and higher lows
   - Moving averages trending upward
   - Price rises accompanied by volume increases

2. **Downtrend**
   - Lower highs and lower lows
   - Moving averages trending downward
   - Decreased volume on bounces

3. **Range-Bound Market**
   - Trading within defined range
   - Moving averages sideways
   - Declining volume trend

### Risk-On / Risk-Off Assessment

#### Risk-On Environment Characteristics
- Stock markets rising (especially emerging markets)
- High-yield currency buying (AUD, NZD, etc.)
- VIX index declining
- Interest rates rising
- Risk assets like crude oil rising

#### Risk-Off Environment Characteristics
- Flight to safe assets (yen buying, Swiss franc buying)
- Gold prices rising
- Bond buying (yields falling)
- VIX index rising
- Emerging market currencies and stocks selling

## Economic Indicator Interpretation

### Employment Data (US)

- **Nonfarm Payrolls (NFP)**
  - +200k or more above expectations: Strong employment, rate hike expectations
  - -100k or more below expectations: Employment deterioration, rate cut expectations

- **Unemployment Rate**
  - 3.5% or below: Near full employment
  - 4.0% or above: Signs of employment environment deterioration

### Inflation Indicators

- **CPI (Consumer Price Index)**
  - 2% YoY: Fed target level
  - 3%+: Inflation alert
  - Below 1%: Deflation risk

- **PPI (Producer Price Index)**
  - Important as CPI leading indicator
  - Captures upstream inflation

### Central Bank Policy

- **Fed (Federal Reserve)**
  - Watch dot plot
  - Policy rate outlook changes

- **BOJ (Bank of Japan)**
  - YCC (Yield Curve Control) policy
  - ETF purchase trends

- **ECB (European Central Bank)**
  - 2% inflation target
  - Response to regional disparities

## Inter-Market Correlation Analysis

### Positive Correlation Patterns
- Stocks ↑ → Interest rates ↑ (strong economy)
- USD/JPY ↑ → Nikkei ↑ (exporters favorable)
- Crude oil ↑ → Inflation expectations ↑

### Inverse Correlation Patterns
- Interest rates ↑ → Bond prices ↓
- Dollar ↑ → Gold prices ↓
- VIX ↑ → Stocks ↓

## Seasonality & Anomalies

### Monthly Patterns
- **January Effect**: New year fund inflows
- **Sell in May**: Pre-summer doldrums position closing
- **September**: Historically weak month
- **December**: Tax-loss selling, Santa Claus rally

### Day-of-Week Effects
- **Monday**: Weekend risk pricing
- **Friday**: Position adjustments

### Fiscal Year-End
- **End of March**: Japanese corporate fiscal year, repatriation flows
- **End of December**: Western corporate fiscal year

## Technical Indicator Usage

### Trend Indicators
- **Moving Averages**: 25-day, 75-day, 200-day line relationships
- **MACD**: Identifying trend turning points
- **Bollinger Bands**: Volatility and contrarian entry points

### Oscillators
- **RSI**: Over 70 overbought, below 30 oversold
- **Stochastics**: Short-term turning points
- **Volume**: Confirming price movement reliability

## Sentiment Analysis

### Capturing Investor Psychology
- **Put/Call Ratio**: Option market skew
- **Bull/Bear Ratio**: Investor surveys
- **Fear & Greed Index**: CNN Fear & Greed Index

### News Flow Analysis
- Headline tone changes
- Media coverage frequency
- Social media buzzwords

### Referencia: references/indicators.md

# Market Indicators Reference

## Major Stock Indices

### Japan
- **Nikkei 225**: Stock price average of 225 representative stocks on Tokyo Stock Exchange Prime
  - Key levels: 30,000, 35,000, 40,000 yen
  - Moving averages: Emphasize 25-day, 75-day, 200-day lines

- **TOPIX**: Market-cap weighted average of all Tokyo Stock Exchange Prime stocks
  - Better reflects overall market
  - Heavily influenced by banking/financial sector

### United States
- **S&P 500**: 500 large-cap US stocks
  - Most representative US stock index
  - Key levels: 4,000, 4,500, 5,000 points

- **NASDAQ**: Tech-focused
  - Reflects mega-cap tech stock trends like GAFAM
  - Higher volatility

- **Dow Jones Industrial Average**: Simple average of 30 stocks
  - Historically significant but limited representation

## Foreign Exchange Rates

### USD/JPY (Dollar-Yen)
- Greatest impact on Japanese economy
- Key levels: 140, 145, 150, 155 yen
- BOJ intervention alert line: Reference past intervention records

### EUR/JPY (Euro-Yen)
- Related to European economy
- Influenced by ECB policy

### CNY/JPY (Yuan-Yen)
- Reflects Chinese economic trends
- Indicator of Asian trade

## Volatility Indicators

### VIX Index (Fear Index)
- Calculated from S&P 500 option prices
- Quantifies market anxiety psychology
- Interpretation:
  - 10-15: Low volatility, stable market
  - 15-20: Normal range
  - 20-30: Unstable, caution needed
  - 30+: High stress, panic selling

### Nikkei VI
- Volatility indicator for Nikkei Average
- Japanese version of VIX

## Commodities

### Crude Oil (WTI/Brent)
- Important as inflation indicator
- Reflects geopolitical risks
- Key levels: 70, 80, 90, 100 dollars/barrel

### Gold
- Representative safe asset
- Tends to rise during dollar weakness/inflation
- Key levels: 1,900, 2,000, 2,100 dollars/ounce

## Interest Rates & Bonds

### US 10-Year Treasury Yield
- Most critical interest rate indicator
- Direct impact on stock valuations
- Key levels: 3.5%, 4.0%, 4.5%, 5.0%

### Japan 10-Year Government Bond Yield
- Reflects BOJ policy
- Watch YCC target range

## Sector-Specific Focus Points

### Technology
- AI-related stock trends
- Semiconductor cycle
- Regulatory risks

### Financials
- Heavily influenced by interest rate trends
- Bank lending attitudes
- Non-performing loan ratios

### Energy
- Linked to crude oil prices
- Impact of decarbonization policies
- Renewable energy shift

### Consumer
- Consumer confidence index
- Retail sales
- Inflation impact


---

## SKILL: market-environment-analysis

- Fuente: `tradermonty/claude-trading-skills` → `skills/market-environment-analysis` (MIT)
- Cuándo usarla: Comprehensive market environment analysis and reporting tool. Analyzes global markets including US, European, Asian markets, forex, commodities, and economic indicators. Provides risk-on/risk-off assessment, sector analysis, and technical indicator interpretation. Triggers on keywords like market analysis, market environment, global markets, trading environment, market conditions, investment climate, market sentiment, forex analysis, stock market analysis, 相場環境, 市場分析, マーケット状況, 投資環境.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/market-environment-analysis/` (requirements.txt, _market_calendar.py, market_utils.py)

# Market Environment Analysis

Comprehensive analysis tool for understanding market conditions and creating professional market reports anytime.

## When to Use

- When you need a comprehensive overview of global market conditions
- Before making trading or investment decisions
- For daily/weekly market briefings
- When assessing risk-on/risk-off sentiment
- For understanding inter-market correlations and sector rotation
- When preparing market reports for clients or personal records

## Prerequisites

- **WebSearch access**: Required for fetching real-time market data
- **No API keys required**: This skill uses web search for data collection
- **Optional**: Economic calendar data for event-driven analysis

## Core Workflow

### 1. Initial Data Collection
Collect latest market data using web_search tool:
1. Major stock indices (S&P 500, NASDAQ, Dow, Nikkei 225, Shanghai Composite, Hang Seng)
2. Forex rates (USD/JPY, EUR/USD, major currency pairs)
3. Commodity prices (WTI crude, Gold, Silver)
4. US Treasury yields (2-year, 10-year, 30-year)
5. VIX index (Fear gauge)
6. Market trading status (open/close/current values)

### 2. Market Environment Assessment
Evaluate the following from collected data:
- **Trend Direction**: Uptrend/Downtrend/Range-bound
- **Risk Sentiment**: Risk-on/Risk-off
- **Volatility Status**: Market anxiety level from VIX
- **Sector Rotation**: Where capital is flowing

### 3. Report Structure

#### Standard Report Format:
```
1. Executive Summary (3-5 key points)
2. Global Market Overview
   - US Markets
   - Asian Markets
   - European Markets
3. Forex & Commodities Trends
4. Key Events & Economic Indicators
5. Risk Factor Analysis
6. Investment Strategy Implications
```

## Script Usage

### market_utils.py
Provides common functions for report creation:
```bash
# Generate report header
python scripts/market_utils.py

# Available functions:
- format_market_report_header(): Create header
- get_market_session_times(): Check trading hours
- categorize_volatility(vix): Interpret VIX levels
- format_percentage_change(value): Format price changes
```

## Exchange Calendar and Replay

Install `requirements.txt` before using `scripts/market_utils.py`. Its
`--as-of` flag requires an offset-bearing ISO-8601 timestamp (or `Z`); a bare
date is rejected because Tokyo, London, and New York status must share one
unambiguous instant. Session status is holiday-, lunch-break-, DST-, and
early-close-aware.

## Reference Documentation

### Key Indicators Interpretation
Load `references/indicators.md` when you need:
- Important levels for each index
- Technical analysis key points
- Sector-specific focus areas

### Analysis Patterns
Load `references/analysis_patterns.md` when analyzing:
- Risk-on/Risk-off criteria
- Economic indicator interpretation
- Inter-market correlations
- Seasonality and market anomalies

## Output Examples

### Quick Summary Version
```
📊 Market Summary [2025/01/15 14:00]
━━━━━━━━━━━━━━━━━━━━━
【US】S&P 500: 5,123.45 (+0.45%)
【JP】Nikkei 225: 38,456.78 (-0.23%)
【FX】USD/JPY: 149.85 (↑0.15)
【VIX】16.2 (Normal range)

⚡ Key Events
- Japan GDP Flash
- US Employment Report

📈 Environment: Risk-On Continues
```

### Detailed Analysis Version
Start with executive summary, then analyze each section in detail.
Key clarifications:
1. Current market phase (Bullish/Bearish/Neutral)
2. Short-term direction (1-5 days outlook)
3. Risk events to monitor
4. Recommended position adjustments

## Important Considerations

### Timezone Awareness
- Consider all major market timezones
- US markets: Evening to early morning (Asian time)
- European markets: Afternoon to evening (Asian time)
- Asian markets: Morning to afternoon (Local time)

### Economic Calendar Priority
Categorize by importance:
- ⭐⭐⭐ Critical (FOMC, NFP, CPI, etc.)
- ⭐⭐ Important (GDP, Retail Sales, etc.)
- ⭐ Reference level

### Data Source Priority
1. Official releases (Central banks, Government statistics)
2. Major financial media (Bloomberg, Reuters)
3. Broker reports
4. Analyst consensus estimates

## Troubleshooting

### Data Collection Notes
- Check market holidays (holiday calendars)
- Be aware of daylight saving time changes
- Distinguish between flash and final data

### Market Volatility Response
1. First organize the facts
2. Reference historical similar events
3. Verify with multiple sources
4. Maintain objective analysis

## Customization Options

Adjust based on user's investment style:
- **Day Traders**: Intraday charts, order flow focus
- **Swing Traders**: Daily/weekly technicals emphasis
- **Long-term Investors**: Fundamentals, macro economics focus
- **Forex Traders**: Currency correlations, interest rate differentials
- **Options Traders**: Volatility analysis, Greeks monitoring

## Resources

- `references/indicators.md` - Key market indicators and interpretation guides
- `references/analysis_patterns.md` - Risk-on/risk-off criteria and inter-market correlations
- `scripts/market_utils.py` - Utility functions for report formatting and market status

### Referencia: references/analysis_patterns.md

# Market Analysis Patterns

## Market Pattern Analysis

### Trend Identification
1. **Uptrend**
   - Higher highs and higher lows
   - Moving averages trending upward
   - Price rises accompanied by volume increases

2. **Downtrend**
   - Lower highs and lower lows
   - Moving averages trending downward
   - Decreased volume on bounces

3. **Range-Bound Market**
   - Trading within defined range
   - Moving averages sideways
   - Declining volume trend

### Risk-On / Risk-Off Assessment

#### Risk-On Environment Characteristics
- Stock markets rising (especially emerging markets)
- High-yield currency buying (AUD, NZD, etc.)
- VIX index declining
- Interest rates rising
- Risk assets like crude oil rising

#### Risk-Off Environment Characteristics
- Flight to safe assets (yen buying, Swiss franc buying)
- Gold prices rising
- Bond buying (yields falling)
- VIX index rising
- Emerging market currencies and stocks selling

## Economic Indicator Interpretation

### Employment Data (US)

- **Nonfarm Payrolls (NFP)**
  - +200k or more above expectations: Strong employment, rate hike expectations
  - -100k or more below expectations: Employment deterioration, rate cut expectations

- **Unemployment Rate**
  - 3.5% or below: Near full employment
  - 4.0% or above: Signs of employment environment deterioration

### Inflation Indicators

- **CPI (Consumer Price Index)**
  - 2% YoY: Fed target level
  - 3%+: Inflation alert
  - Below 1%: Deflation risk

- **PPI (Producer Price Index)**
  - Important as CPI leading indicator
  - Captures upstream inflation

### Central Bank Policy

- **Fed (Federal Reserve)**
  - Watch dot plot
  - Policy rate outlook changes

- **BOJ (Bank of Japan)**
  - YCC (Yield Curve Control) policy
  - ETF purchase trends

- **ECB (European Central Bank)**
  - 2% inflation target
  - Response to regional disparities

## Inter-Market Correlation Analysis

### Positive Correlation Patterns
- Stocks ↑ → Interest rates ↑ (strong economy)
- USD/JPY ↑ → Nikkei ↑ (exporters favorable)
- Crude oil ↑ → Inflation expectations ↑

### Inverse Correlation Patterns
- Interest rates ↑ → Bond prices ↓
- Dollar ↑ → Gold prices ↓
- VIX ↑ → Stocks ↓

## Seasonality & Anomalies

### Monthly Patterns
- **January Effect**: New year fund inflows
- **Sell in May**: Pre-summer doldrums position closing
- **September**: Historically weak month
- **December**: Tax-loss selling, Santa Claus rally

### Day-of-Week Effects
- **Monday**: Weekend risk pricing
- **Friday**: Position adjustments

### Fiscal Year-End
- **End of March**: Japanese corporate fiscal year, repatriation flows
- **End of December**: Western corporate fiscal year

## Technical Indicator Usage

### Trend Indicators
- **Moving Averages**: 25-day, 75-day, 200-day line relationships
- **MACD**: Identifying trend turning points
- **Bollinger Bands**: Volatility and contrarian entry points

### Oscillators
- **RSI**: Over 70 overbought, below 30 oversold
- **Stochastics**: Short-term turning points
- **Volume**: Confirming price movement reliability

## Sentiment Analysis

### Capturing Investor Psychology
- **Put/Call Ratio**: Option market skew
- **Bull/Bear Ratio**: Investor surveys
- **Fear & Greed Index**: CNN Fear & Greed Index

### News Flow Analysis
- Headline tone changes
- Media coverage frequency
- Social media buzzwords

### Referencia: references/indicators.md

# Market Indicators Reference

## Major Stock Indices

### Japan
- **Nikkei 225**: Stock price average of 225 representative stocks on Tokyo Stock Exchange Prime
  - Key levels: 30,000, 35,000, 40,000 yen
  - Moving averages: Emphasize 25-day, 75-day, 200-day lines

- **TOPIX**: Market-cap weighted average of all Tokyo Stock Exchange Prime stocks
  - Better reflects overall market
  - Heavily influenced by banking/financial sector

### United States
- **S&P 500**: 500 large-cap US stocks
  - Most representative US stock index
  - Key levels: 4,000, 4,500, 5,000 points

- **NASDAQ**: Tech-focused
  - Reflects mega-cap tech stock trends like GAFAM
  - Higher volatility

- **Dow Jones Industrial Average**: Simple average of 30 stocks
  - Historically significant but limited representation

## Foreign Exchange Rates

### USD/JPY (Dollar-Yen)
- Greatest impact on Japanese economy
- Key levels: 140, 145, 150, 155 yen
- BOJ intervention alert line: Reference past intervention records

### EUR/JPY (Euro-Yen)
- Related to European economy
- Influenced by ECB policy

### CNY/JPY (Yuan-Yen)
- Reflects Chinese economic trends
- Indicator of Asian trade

## Volatility Indicators

### VIX Index (Fear Index)
- Calculated from S&P 500 option prices
- Quantifies market anxiety psychology
- Interpretation:
  - 10-15: Low volatility, stable market
  - 15-20: Normal range
  - 20-30: Unstable, caution needed
  - 30+: High stress, panic selling

### Nikkei VI
- Volatility indicator for Nikkei Average
- Japanese version of VIX

## Commodities

### Crude Oil (WTI/Brent)
- Important as inflation indicator
- Reflects geopolitical risks
- Key levels: 70, 80, 90, 100 dollars/barrel

### Gold
- Representative safe asset
- Tends to rise during dollar weakness/inflation
- Key levels: 1,900, 2,000, 2,100 dollars/ounce

## Interest Rates & Bonds

### US 10-Year Treasury Yield
- Most critical interest rate indicator
- Direct impact on stock valuations
- Key levels: 3.5%, 4.0%, 4.5%, 5.0%

### Japan 10-Year Government Bond Yield
- Reflects BOJ policy
- Watch YCC target range

## Sector-Specific Focus Points

### Technology
- AI-related stock trends
- Semiconductor cycle
- Regulatory risks

### Financials
- Heavily influenced by interest rate trends
- Bank lending attitudes
- Non-performing loan ratios

### Energy
- Linked to crude oil prices
- Impact of decarbonization policies
- Renewable energy shift

### Consumer
- Consumer confidence index
- Retail sales
- Inflation impact
