# 10-wealth-planning-fiscal — parte 1

Skills de terceros agrupadas por tema. Cada sección indica fuente, licencia y dónde está su código.



---

## SKILL: alternatives

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/alternatives` (MIT)
- Cuándo usarla: Analyze alternative investments including hedge funds, private equity, and venture capital. Use when the user asks about hedge fund strategies (long/short, macro, event-driven), PE or VC performance metrics (IRR, TVPI, DPI), fee structures ('2-and-20', carry, hurdle rates), the J-curve effect, illiquidity premiums, lock-up periods, or hedge fund replication. Also trigger when users mention 'managed futures', 'CTA', 'fund of funds', 'vintage year', 'capital calls', 'distributions', 'carried interest', or ask how to evaluate an alternative investment manager.

# Alternatives

## Core Concepts

### Hedge Fund Strategies
- **Long/Short Equity:** Combines long positions in undervalued stocks with short positions in overvalued stocks. Net exposure can range from net long to market neutral.
- **Market Neutral:** Targets zero beta to the market. Returns driven by stock selection alpha, not market direction.
- **Global Macro:** Takes positions in currencies, rates, equities, and commodities based on macroeconomic views. Highly discretionary.
- **Event-Driven:** Profits from corporate events — mergers (merger arbitrage), restructurings, spinoffs, bankruptcies.
- **Relative Value:** Exploits pricing discrepancies between related securities (convertible arbitrage, fixed income arbitrage, capital structure arbitrage).
- **Managed Futures/CTA:** Systematic trend-following strategies across futures markets. Historically provide positive convexity (perform well in crises).

### Fee Structures
The standard hedge fund fee is "2-and-20" — 2% annual management fee on AUM plus 20% performance fee on profits.

- **High-water mark:** Performance fees are only charged on new profits above the previous peak NAV. Protects investors from paying fees to recover losses.
- **Hurdle rate:** A minimum return (often a risk-free rate) that must be exceeded before performance fees apply.
- **Clawback:** Mechanism to recover performance fees if subsequent losses erode earlier gains (more common in PE).

### Private Equity Metrics
- **IRR (Internal Rate of Return):** The discount rate that sets the NPV of all cash flows (capital calls and distributions) to zero. The canonical money-weighted return — it is sensitive to the timing and size of cash flows, unlike the time-weighted returns used for public market funds.
- **TVPI (Total Value to Paid-In):** (Distributions + Remaining Value) / Total Capital Called. A multiple of invested capital.
- **DPI (Distributions to Paid-In):** Distributions / Total Capital Called. Measures realized returns only — the "cash-on-cash" multiple.
- **RVPI (Residual Value to Paid-In):** Remaining Value / Total Capital Called. Measures unrealized value. TVPI = DPI + RVPI.

### J-Curve
Private equity funds typically show negative returns in the early years because management fees are charged on committed capital, initial investments are carried at cost or slightly written down, and returns have not yet materialized. As portfolio companies mature and are exited, returns improve. The characteristic shape — initial losses followed by gains — resembles the letter J.

### Vintage Year Diversification
PE fund performance is significantly influenced by the economic environment at the time of investment. Spreading commitments across multiple vintage years reduces the risk of investing all capital at unfavorable valuations.

### Illiquidity Premium
The expected excess return demanded for accepting illiquidity — the inability to sell quickly at fair value. Private equity, venture capital, and certain hedge funds impose lock-up periods (1-10+ years). The illiquidity premium is theoretically 150-400bp for PE and private credit, though estimates vary and are debated.

### Lock-Up Periods, Gates, and Side Pockets
- **Lock-up:** Period during which investors cannot redeem (typically 1-3 years for hedge funds, 7-12 years for PE).
- **Gates:** Limits on the percentage of fund assets that can be redeemed in any single period (e.g., 10-25% per quarter).
- **Side pockets:** Illiquid or hard-to-value positions segregated from the main portfolio. Investors cannot redeem side-pocketed assets until they are realized.

### Replication and Factor Exposure
Many hedge fund returns can be replicated with systematic factor exposure (equity market, size, value, momentum, credit, volatility selling). Research shows that a significant portion of hedge fund "alpha" is actually alternative beta — compensation for well-known risk factors. True alpha (manager skill net of factor exposure) is scarce and diminishing.

### Due Diligence
Key areas: operational risk (back-office, custody, valuation practices), strategy capacity (can the strategy scale?), manager skill vs factor exposure, transparency and reporting, alignment of interests, and regulatory compliance.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Management Fee | AUM × Management Fee Rate | Annual fee on assets |
| Performance Fee | max(0, Gains Above HWM) × Perf Fee Rate | Fee on profits |
| Net Return (2-and-20) | Gross Return - 2% - 20% × max(0, Gross - Hurdle) | After-fee return |
| TVPI | (Distributions + NAV) / Paid-In Capital | Total return multiple |
| DPI | Distributions / Paid-In Capital | Realized return multiple |
| RVPI | NAV / Paid-In Capital | Unrealized return multiple |
| IRR | Rate r: sum CF_t/(1+r)^t = 0 | Money-weighted return |

## Worked Examples

### Example 1: Fee Drag on a Hedge Fund
**Given:** $10M invested, gross return = 8%, 2% management fee, 20% performance fee, no hurdle rate
**Calculate:** Net return and fee drag
**Solution:**
Management fee = $10M × 2% = $200,000
Gross profit = $10M × 8% = $800,000
Performance fee = 20% × $800,000 = $160,000 (charged on gross profits; under this fee structure the management fee is calculated independently and is not deducted first — some funds instead charge the incentive fee net of the management fee, which would give 20% × $600,000 = $120,000; always check the fund documents)
Total fees = $200,000 + $160,000 = $360,000
Net return = ($800,000 - $360,000) / $10,000,000 = 4.4%
Fee drag = 8.0% - 4.4% = 3.6 percentage points

The investor keeps 4.4% of the 8.0% gross return. Fees consume 45% of gross returns in this example. At lower gross returns, the fee drag as a percentage becomes even more severe.

### Example 2: Private Equity J-Curve and Multiples
**Given:** A PE fund calls $2M/year for 5 years (total $10M). Distributions: Year 4 = $1M, Year 5 = $3M, Year 6 = $5M, Year 7 = $8M, Year 8 = $4M. No residual value after Year 8.
**Calculate:** DPI, TVPI, and approximate IRR
**Solution:**
Total distributions = $1M + $3M + $5M + $8M + $4M = $21M
Total paid-in = $2M × 5 = $10M
DPI = $21M / $10M = 2.1x
TVPI = (21M + 0) / $10M = 2.1x (no residual, so TVPI = DPI)

Cash flows for IRR: Year 1: -$2M, Year 2: -$2M, Year 3: -$2M, Year 4: -$2M + $1M = -$1M, Year 5: -$2M + $3M = +$1M, Year 6: +$5M, Year 7: +$8M, Year 8: +$4M
Solving for IRR numerically yields approximately 23%.

The J-curve is visible: negative net cash flows in years 1-4, turning positive in year 5, with the bulk of value returned in years 6-7.

## Common Pitfalls
- IRR manipulation through subscription credit lines — borrowing at the fund level delays capital calls, artificially boosting early IRR without improving actual returns
- Survivorship and backfill bias in hedge fund databases — failed funds are removed and new entrants can backfill historical returns, inflating reported industry performance
- Illiquidity masking true volatility — PE and hedge fund returns are based on appraisals or marks, which smooth reported volatility and understate true risk
- Comparing PE IRR directly to public market time-weighted returns — use PME (Public Market Equivalent) for an apples-to-apples comparison

## Cross-References
- **historical-risk** (wealth-management plugin): return measurement and risk-adjusted performance
- **equities** (wealth-management plugin): long/short equity strategies and factor exposures
- **fixed-income-corporate** (wealth-management plugin): private credit and leveraged loan markets
- **performance-attribution** (wealth-management plugin): evaluating manager alpha vs factor beta
- **private-placements** (compliance plugin): the regulatory eligibility and exempt-offering compliance side of investing in private funds


---

## SKILL: client-review

- Fuente: `anthropics/financial-services` → `plugins/agent-plugins/meeting-prep-agent/skills/client-review` (Apache-2.0)
- Cuándo usarla: Prepare for client review meetings with portfolio performance summary, allocation analysis, talking points, and action items. Pulls together account data into a concise meeting-ready format. Use before quarterly reviews, annual checkups, or ad-hoc client meetings. Triggers on "client review", "meeting prep for [client]", "quarterly review", "prep for [client name]", or "client meeting".

# Client Review Prep

## Workflow

### Step 1: Client Context

Gather or look up:
- **Client name** and household members
- **Account types**: Taxable, IRA, Roth, 401(k), trust, etc.
- **Total AUM** across accounts
- **Investment Policy Statement (IPS)**: Target allocation, risk tolerance, constraints
- **Life stage**: Accumulation, pre-retirement, retirement, legacy
- **Last meeting date** and any outstanding action items

### Step 2: Portfolio Performance

For each account and the household aggregate:

| Metric | QTD | YTD | 1-Year | 3-Year | Since Inception |
|--------|-----|-----|--------|--------|----------------|
| Portfolio return | | | | | |
| Benchmark return | | | | | |
| Alpha | | | | | |

**Performance Attribution:**
- Which asset classes / positions drove returns?
- Top 3 contributors and top 3 detractors
- Any outsized single-position impact?

### Step 3: Allocation Review

Current vs. target allocation:

| Asset Class | Target | Current | Drift | Action |
|------------|--------|---------|-------|--------|
| US Large Cap | | | | |
| US Mid/Small | | | | |
| International Developed | | | | |
| Emerging Markets | | | | |
| Fixed Income | | | | |
| Alternatives | | | | |
| Cash | | | | |

Flag any drift exceeding the IPS rebalancing threshold (typically 3-5%).

### Step 4: Talking Points

Generate a meeting agenda:

1. **Market overview** (2-3 min): Brief macro context and outlook
2. **Portfolio performance** (5 min): How did we do? Why?
3. **Allocation review** (5 min): Any rebalancing needed?
4. **Planning updates** (5-10 min):
   - Life changes? (job, health, family, home, education)
   - Income needs changing?
   - Tax situation updates
   - Estate planning updates
5. **Action items** (5 min): What are we doing before next meeting?

### Step 5: Proactive Recommendations

Based on the review, suggest:
- Rebalancing trades (if drift exceeds thresholds)
- Tax-loss harvesting opportunities
- Cash deployment or withdrawal planning
- Roth conversion opportunities (if applicable)
- Beneficiary updates or estate planning needs
- Insurance review (life, disability, LTC)

### Step 6: Output

- One-page client review summary (Word or PDF)
- Performance table with benchmarks
- Allocation pie chart (current vs. target)
- Recommended action items
- Meeting agenda

## Important Notes

- Know your client before the meeting — review notes from last meeting
- Lead with what the client cares about, not what you want to talk about
- If performance was bad, address it directly — don't hide or spin
- Always end with clear action items and next steps with dates
- Document the meeting notes and any changes to the IPS
- Compliance: ensure all materials are compliant with firm policies and regulatory requirements


---

## SKILL: client-review-prep

- Fuente: `JoelLewis/finance_skills` → `plugins/advisory-practice/skills/client-review-prep` (MIT)
- Cuándo usarla: Prepare advisors for client review meetings by assembling context packages, performance summaries, drift analysis, talking points, and meeting agendas. Use when the user asks about preparing for a client review, building a pre-meeting checklist, generating talking points for an upcoming meeting, identifying allocation drift before a review, automating review prep workflows, or assembling a meeting package with exhibits. Also trigger when users mention 'client meeting prep', 'review preparation', 'what should I discuss with my client', 'proactive recommendations', 'life event triggered review', 'meeting agenda', or 'compliance pre-check before review'.

# Client Review Preparation

## Core Concepts

### Client Context Assembly

The foundation of review preparation is assembling everything the advisor needs to know about the client before the meeting. This context package draws from multiple systems and should be gathered systematically rather than ad hoc.

**Data to assemble:**

1. **Client profile and household** -- pull from CRM: names, ages, employment status, retirement dates, household members, service tier, assigned advisor, communication preferences
2. **Investment Policy Statement (IPS)** -- the governing document for the relationship: stated objectives, risk tolerance, time horizon, return targets, asset allocation targets with tolerance bands, investment restrictions, benchmark selections, liquidity constraints
3. **Account inventory** -- all accounts in the household: account types (taxable, IRA, Roth, trust, etc.), custodians, current market values, cash positions, cost basis summary
4. **Recent life events** -- any changes since the last review: job change, retirement, marriage, divorce, inheritance, birth of child, health event, home purchase or sale, business sale. These come from CRM notes, advisor logs, and financial planning system updates.
5. **Prior meeting notes** -- what was discussed at the last review, what action items were assigned, which items were completed. Unresolved items carry forward to the agenda.
6. **Financial plan status** -- if the client has a financial plan: probability of success, progress toward goals (retirement funding, education, legacy), any goals that have drifted off track since the last review
7. **Compliance and administrative status** -- date of last IPS update, date of last suitability questionnaire, advisory agreement renewal date, fee schedule, any pending compliance items

Assemble this data into a one-page client context summary that the advisor can review in under five minutes before the meeting.

### Performance Review Preparation

Performance data is the centerpiece of most review conversations. The goal is not to re-create a full performance report (that is the domain of performance reporting and client reporting delivery), but to extract the key numbers and narratives the advisor needs for the discussion.

**Data to collect:**

- Period returns for each account and the consolidated household: quarter-to-date, year-to-date, trailing 1-year, since inception (or since last review date)
- Benchmark comparison: portfolio return versus the IPS-designated benchmark for each period
- Attribution highlights: which asset classes or positions contributed most to outperformance or underperformance. Focus on the two or three largest contributors and detractors -- the client does not need a 50-line attribution table in a meeting.
- Fees paid: advisory fees, fund expense ratios, transaction costs. Summarize total cost in dollars and as a percentage of AUM for the review period.
- Income generated: dividends and interest received during the period, withdrawal activity

**Prepare the narrative:** Translate raw numbers into a short (3-5 sentence) performance summary the advisor can use as a talking point. Example: "The consolidated household returned 4.2% for the quarter versus the benchmark's 3.8%, primarily driven by overweight exposure to international equities. Fixed income underperformed as rates rose, but the short-duration tilt limited the drag. Total fees for the quarter were $3,750 (0.15% of AUM)."

### Allocation Drift Analysis

Before the meeting, compare each account's current allocation to its IPS target and identify any positions that have drifted beyond tolerance bands. This analysis feeds directly into rebalancing discussion points but does not re-derive the rebalancing math (see the rebalancing skill for methodology).

**Steps:**

1. Pull current holdings and market values by asset class from the PMS
2. Calculate current allocation percentages for each asset class
3. Compare to IPS target allocation
4. Flag any asset class where the drift exceeds the tolerance band (e.g., target 60% equity with +/-5% band; current 67% equity is 2% beyond the upper band)
5. Summarize drift in a simple table: asset class, target, current, drift, in/out of tolerance

If drift is beyond tolerance, prepare a rebalancing recommendation as a talking point. Include the estimated tax impact of rebalancing (realized gains or losses) for taxable accounts.

### Talking Points Generation

Talking points are the structured notes the advisor uses to guide the meeting conversation. They should be specific to this client, not generic market commentary.

**Categories of talking points:**

1. **Market commentary relevant to the portfolio** -- select 2-3 market developments that directly affect the client's holdings or strategy. If the client is overweight technology, discuss tech sector trends. If the client holds municipal bonds, discuss the muni market environment. Avoid generic "the market was up 5%" statements.
2. **Rebalancing needs** -- if drift analysis identified out-of-tolerance positions, frame the rebalancing conversation: what to trim, what to add, estimated tax impact, rationale tied to the IPS.
3. **Upcoming events** -- RMD deadlines, estimated tax payment dates, option expirations, bond maturities, CD renewals, vesting events for RSUs or stock options, trust distribution dates
4. **Action item follow-up** -- status of any actions agreed upon at the last meeting: was the beneficiary update completed? Was the insurance review done? Was the estate plan referral followed through?
5. **Life event implications** -- if any life events have occurred, prepare talking points on financial implications: new retirement date changes the distribution strategy, inheritance needs to be integrated into the portfolio and plan, divorce requires account retitling and beneficiary updates

### Proactive Recommendations

A well-prepared review goes beyond reporting what happened and proactively identifies optimization opportunities. The advisor should walk into the meeting with 2-3 specific, actionable recommendations tailored to the client's situation.

**Common proactive recommendation categories:**

- **Tax-loss harvesting opportunities** -- identify positions with unrealized losses that could be harvested before year-end. Note wash sale considerations and replacement security options. Reference the tax-loss-harvesting and tax-efficiency skills for methodology; do not re-derive here.
- **Roth conversion windows** -- if the client has a low-income year (early retirement, sabbatical, gap between retirement and Social Security), flag the opportunity to convert traditional IRA assets to Roth at a lower marginal rate. Estimate the tax cost and long-term benefit.
- **RMD planning** -- for clients age 73+ or approaching RMD age: calculate the upcoming RMD amount, discuss the timing of the distribution, evaluate whether to take it in cash or in-kind, consider qualified charitable distributions (QCDs) if the client is charitably inclined.
- **Beneficiary review** -- flag accounts where beneficiary designations have not been reviewed in over two years, or where a life event (marriage, divorce, birth, death) may have made the current designation inappropriate.
- **Insurance and estate review** -- if the client's net worth has changed materially, flag the need to review life insurance coverage, umbrella liability, and estate planning documents.
- **Cash management** -- if cash balances exceed the client's liquidity needs (as defined in the IPS), recommend deploying excess cash to the investment strategy.
- **Concentrated position management** -- if any single position exceeds a threshold (commonly 10-15% of portfolio), prepare a discussion on diversification strategies: systematic sales, exchange funds, hedging with options, charitable giving of appreciated shares.

### Agenda and Meeting Package Assembly

Structure the meeting with a timed agenda so the conversation covers all important topics without running over.

**Standard review meeting agenda (60 minutes):**

1. Personal update and life event check-in (5-10 minutes) -- open with the client, not the portfolio. Ask about family, health, career, goals. Listen for new information that affects the financial plan.
2. Performance review (10-15 minutes) -- present the performance summary prepared above. Walk through returns relative to benchmarks, highlight key drivers, address any underperformance directly.
3. Allocation and rebalancing (5-10 minutes) -- show the drift analysis. If rebalancing is needed, present the recommendation and get client agreement.
4. Financial plan progress (10-15 minutes) -- review goal status, probability of success, any changes needed to contributions, spending, or timeline.
5. Proactive recommendations (10-15 minutes) -- present the 2-3 tailored recommendations prepared above. Explain the rationale, estimated impact, and next steps for each.
6. Action items and next steps (5 minutes) -- summarize agreed-upon actions, assign owners and deadlines, confirm the next review date.

**Supporting exhibits to include in the meeting package:**

- One-page client context summary
- Performance summary (returns, benchmark comparison, key attribution)
- Allocation drift table (current vs target vs tolerance)
- Financial plan snapshot (goal progress, probability of success)
- Proactive recommendation briefs (one paragraph each with estimated impact)
- Fee summary for the review period

### Compliance Pre-Check

Before the meeting, verify that all compliance and administrative items are current. This prevents the advisor from making recommendations based on stale suitability data or expired agreements.

**Pre-check items:**

- **IPS recency** -- has the IPS been reviewed and signed within the past 12-24 months (per firm policy)? If not, add IPS review to the agenda.
- **Suitability data** -- is the client's risk tolerance, time horizon, and financial situation current? If not updated in over 12 months, add suitability re-evaluation to the agenda.
- **Advisory agreement** -- is the fee agreement current and signed? Are fees being charged correctly per the agreement?
- **Disclosure delivery** -- has the client received the current Form ADV Part 2A (or material amendment) and Form CRS? Annual delivery or material change delivery must be documented.
- **Beneficiary designations** -- have beneficiary designations been reviewed? Flag if never reviewed or if a life event has occurred since the last review.
- **Trusted contact** -- does the client have a trusted contact person on file per FINRA Rule 4512? If not, add it to the agenda.
- **Required Minimum Distributions** -- for clients subject to RMDs: has the current-year RMD been calculated and is it on schedule to be distributed by the deadline?

Document any compliance gaps found during the pre-check and add them as agenda items for the meeting.

## Worked Examples

### Example 1: Annual review for a retired couple

**Scenario:** Robert and Linda Chen, both age 72, retired three years ago. They have a joint taxable account ($1.8M), Robert's traditional IRA ($950K), Linda's Roth IRA ($420K), and a family trust ($600K). Their combined portfolio is $3.77M. The IPS targets 40% equity / 50% fixed income / 10% alternatives with +/-5% tolerance bands. Robert turns 73 in four months, triggering his first RMD. Their last review was six months ago. The CRM shows Linda had a hip replacement two months ago (noted by the advisor's assistant).

**Key Review Elements:**

- **Context assembly:** Pull the household profile showing four accounts, service tier (platinum), and the six-month-old meeting notes. The prior meeting flagged two action items: (1) update the trust's beneficiary designations after their grandson's birth, and (2) review umbrella insurance coverage. Check CRM for status of both.
- **Performance:** Consolidated household returned 2.1% for the trailing six months versus the blended benchmark's 2.4%. Fixed income allocation (53% actual vs 50% target) slightly underperformed due to rising rates. Equity (37% actual vs 40% target) outperformed but was underweight. Fees for the period: $9,425 advisory fee (0.50% annualized).
- **Drift analysis:** Equity at 37% is 3% below target (within the 5% band). Fixed income at 53% is 3% above target (within band). Alternatives at 10% are on target. No tolerance band breaches, but equity is trending toward the lower bound. Recommend monitoring; no rebalancing action required yet.
- **Proactive recommendations:** (1) RMD planning -- Robert's first RMD is due by April 1 of next year. Estimated RMD is approximately $36,900 based on the IRA balance and Uniform Lifetime Table divisor. Discuss timing: take before December 31 to avoid bunching two RMDs in the first distribution year. Consider a qualified charitable distribution if the Chens make charitable gifts. (2) Linda's hip replacement may trigger a review of health care cost assumptions in the financial plan. (3) Check whether the trust beneficiary update was completed per the prior meeting's action item.
- **Compliance pre-check:** IPS was last signed 18 months ago; due for re-review at this meeting. Suitability data last updated 18 months ago; add re-confirmation to the agenda. Robert does not have a trusted contact on file; Linda's is listed as their daughter. Add trusted contact for Robert.

**Analysis:** The meeting should lead with a personal check-in about Linda's recovery, then focus on three substantive items: Robert's upcoming RMD (time-sensitive), the IPS re-review (compliance-driven), and follow-up on the prior meeting's open action items. Performance and allocation are stable and require only a brief update. The agenda should allocate more time to the RMD discussion and IPS re-review and less time to performance, since there are no significant drift or performance issues.

### Example 2: Quarterly review for a high-net-worth executive

**Scenario:** Priya Sharma, age 48, is a VP at a publicly traded technology company. Her portfolio consists of a taxable brokerage account ($2.1M diversified), a 401(k) at her employer ($1.4M), a backdoor Roth IRA ($380K), and unvested RSUs worth approximately $1.2M (vesting over the next 3 years in quarterly tranches). Her concentrated stock position in her employer is $850K (vested shares in the taxable account), representing 14% of total investable assets. The IPS targets 70% equity / 25% fixed income / 5% alternatives. The market has been volatile with tech stocks down 12% in the quarter. She has $180K in unrealized losses across three positions in her taxable account.

**Key Review Elements:**

- **Context assembly:** Pull Priya's profile, four-account inventory, RSU vesting schedule from the most recent equity compensation statement, and prior meeting notes. The last quarterly review flagged that the concentrated stock position was approaching the 15% threshold for discussion. No life events on record.
- **Performance:** Taxable account down 6.2% for the quarter due to tech exposure. 401(k) down 3.8% (more diversified). Roth IRA down 2.1% (conservative growth allocation). Consolidated portfolio down 4.1% versus the blended benchmark's -3.5%. The 60 basis point underperformance is primarily attributable to the concentrated employer stock position.
- **Drift analysis:** Current equity allocation is 73%, 3% above the 70% target (within the +/-5% band). However, equity concentration risk is elevated: employer stock at 14% of total assets is near the 15% discussion threshold. If the next RSU tranche vests ($100K), the combined employer exposure rises to approximately 16%. Fixed income at 22% is 3% below target.
- **Proactive recommendations:** (1) Tax-loss harvesting -- the $180K in unrealized losses across three positions represents a significant harvesting opportunity. Identify replacement securities to maintain market exposure while realizing the losses. At Priya's marginal tax rate (estimated 35% federal + state), these harvested losses could offset up to $63K in future gains. (2) Concentrated stock management -- with employer stock at 14% and approaching 16% after the next vest, recommend beginning a systematic diversification program: sell a portion of each RSU tranche as it vests via a 10b5-1 plan, and consider selling some existing shares in the current quarter to offset against the harvested losses (netting the tax impact). (3) Roth conversion -- Priya's income is high, so a direct conversion is not tax-efficient now, but flag this for future planning if she ever has a career transition or sabbatical.
- **Compliance pre-check:** IPS current (updated 8 months ago). Suitability data current. Check that the firm has Priya's most recent equity compensation plan documents on file to verify trading window restrictions before recommending any employer stock sales. Confirm advisory agreement fee schedule.

**Analysis:** This review should focus on the actionable opportunities created by the market downturn: the tax-loss harvesting is time-sensitive (approach before year-end or before prices recover) and the concentrated position management is proactive risk reduction. The agenda should allocate significant time to the TLH and concentration discussion, with a brief performance review focused on explaining the underperformance relative to benchmark. Frame the market downturn as creating opportunities (TLH, buying at lower prices for rebalancing) rather than dwelling on losses.

### Example 3: Triggered review after a major life event

**Scenario:** David Patel, age 55, recently received a $1.5M inheritance from his mother's estate. He is an existing client with a taxable account ($600K) and a traditional IRA ($480K). His current IPS targets 60% equity / 35% fixed income / 5% cash. The inheritance is currently sitting in the estate's money market account and will be distributed to David within 30 days. David also inherited his mother's house, which he plans to sell (estimated value $450K). The CRM shows the advisor logged a call two weeks ago when David first informed them of the inheritance.

**Key Review Elements:**

- **Context assembly:** Pull David's existing profile and accounts. Note that his investable assets are about to nearly triple (from $1.08M to approximately $2.58M in financial assets, plus the $450K house sale pending). This magnitude of change requires a comprehensive review, not a routine quarterly meeting. Pull the prior meeting notes and the advisor's call log from two weeks ago to understand what was discussed initially.
- **Performance:** While normal performance review is secondary in a life-event-triggered meeting, provide the current portfolio summary for context: existing accounts are performing in line with benchmarks. The focus of this meeting is forward-looking, not retrospective.
- **IPS re-evaluation:** The existing IPS was written for a $1.08M portfolio. With $2.58M+ in assets, David's risk capacity has materially changed. He may be able to take less risk (same lifestyle supported by a larger asset base) or may choose to maintain his risk level with a higher expected return. The IPS must be re-evaluated and re-signed. Time horizon, liquidity needs, and objectives should all be revisited.
- **Proactive recommendations:** (1) Inheritance integration strategy -- develop a plan for deploying the $1.5M. Options: lump-sum investment into the target allocation, dollar-cost averaging over 6-12 months (suitable if David is anxious about market timing), or a hybrid approach. Factor in current market conditions and David's risk tolerance. (2) Tax planning for the inherited assets -- determine the cost basis of inherited securities (stepped-up basis at date of death). If the estate holds appreciated securities, the stepped-up basis eliminates embedded gains, which may influence the decision to liquidate vs transfer in-kind. (3) House sale planning -- the inherited home receives a stepped-up basis. If David sells within a reasonable period at a price close to the date-of-death value, there should be minimal capital gains. Coordinate timing with the overall investment plan. (4) Estate plan update -- David's own estate plan should be revisited given the nearly tripled net worth. Beneficiary designations on the IRA should be reviewed. (5) Evaluate whether David's employer group life insurance and umbrella liability coverage are adequate for his new net worth.
- **Compliance pre-check:** The IPS must be re-done given the material change in circumstances. Suitability data must be updated to reflect the new financial situation. If the inherited assets include any securities on the firm's restricted list, flag immediately. Verify that the advisory agreement's fee schedule applies to the combined AUM (check breakpoint tiers).

**Analysis:** This is not a standard review; it is a financial planning event triggered by a significant life change. The agenda should prioritize (1) understanding David's emotional state and goals for the inheritance, (2) re-evaluating the IPS with updated financial data, (3) developing the deployment strategy for the $1.5M, and (4) coordinating the house sale with the broader plan. Performance review of existing accounts is a minor agenda item. Allow 90 minutes rather than the standard 60 for this meeting. Consider splitting into two sessions: an initial planning session to discuss goals and update the IPS, and a follow-up session to present the specific investment recommendation once the plan is updated.

## Common Pitfalls

- Presenting performance data without preparing a narrative explanation of the key drivers -- raw numbers without context invite confusion and anxiety
- Skipping the life event check-in and jumping straight to portfolio data -- missed life events lead to stale plans and missed advice opportunities
- Preparing generic market commentary that is not connected to the client's actual holdings or strategy
- Failing to check the status of action items from the prior meeting, which signals to the client that follow-through is weak
- Not running the compliance pre-check before the meeting, leading to outdated IPS, suitability data, or disclosure delivery gaps discovered after the fact
- Over-preparing the meeting package with 30 pages of data instead of a focused 5-6 page package with the key exhibits
- Presenting rebalancing recommendations without estimating the tax impact for taxable accounts
- Not adjusting the standard agenda for triggered or life-event reviews, which require more time and a different conversation structure than routine periodic reviews
- Ignoring upcoming deadlines (RMDs, estimated tax payments, RSU vesting dates) that require time-sensitive action
- Treating all clients identically rather than tailoring the depth and focus of preparation to the client's complexity and service tier

## Cross-References

- **performance-reporting** (wealth-management plugin): provides the performance data assembled into the review package; review prep extracts summary metrics and narratives from the full performance report
- **performance-attribution** (wealth-management plugin): attribution analysis highlights for discussing what drove returns; review prep pulls the top contributors and detractors for talking points
- **investment-policy** (wealth-management plugin): the IPS provides the reference framework for evaluating drift and suitability; review prep checks IPS recency and uses targets for drift analysis
- **rebalancing** (wealth-management plugin): drift analysis and rebalancing recommendations are core review talking points; review prep identifies drift but references rebalancing for execution methodology
- **tax-efficiency** (wealth-management plugin): tax-aware recommendations (Roth conversions, asset location) for proactive review items; review prep flags opportunities without re-deriving the underlying analysis
- **tax-loss-harvesting** (wealth-management plugin): TLH opportunities are flagged during review prep as proactive recommendations; the TLH skill provides the methodology and wash sale rules
- **client-onboarding** (advisory-practice plugin): onboarding data populates the initial client profile used in reviews; the profile assembled during onboarding is the starting point for all future review prep
- **client-reporting-delivery** (advisory-practice plugin): review prep feeds into and complements the report delivery workflow; the meeting package may include or accompany the formal client report
- **crm-client-lifecycle** (advisory-practice plugin): CRM provides client segmentation, review scheduling data, life event logs, and prior meeting notes that drive review preparation
- **financial-planning-workflow** (advisory-practice plugin): financial plan progress is a key review agenda item; review prep pulls goal status and probability-of-success metrics from the planning system


---

## SKILL: emergency-fund

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/emergency-fund` (MIT)
- Cuándo usarla: Size and structure an emergency fund based on individual circumstances, income stability, and expense profile. Use when the user asks about emergency fund sizing, how many months of expenses to save, where to keep emergency savings, or tiered fund structures. Also trigger when users mention 'rainy day fund', 'how much cash should I keep', 'high-yield savings account', 'money market fund', 'freelancer cash reserve', 'variable income buffer', or ask what counts as an emergency expense.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/wealth-management/skills/emergency-fund/` (emergency_fund.py)

# Emergency Fund Planning

## Core Concepts

### Rule of Thumb
- **Employed with stable income:** 3-6 months of essential expenses
- **Dual-income household (both stable):** 3 months may suffice (lower probability of simultaneous job loss)
- **Single income, variable income, or self-employed:** 6-12 months of essential expenses
- **High job-search risk (niche industry, senior executive, specialized role):** 6-12 months
- These are guidelines — individual assessment is essential

### Essential Expenses
The emergency fund should cover non-discretionary spending only:

- **Housing:** Mortgage/rent, property tax, insurance, HOA
- **Food:** Groceries (not dining out)
- **Insurance:** Health, auto, life (premiums that cannot be paused)
- **Utilities:** Electric, gas, water, internet, phone
- **Transportation:** Car payment, gas, basic maintenance, public transit
- **Minimum debt payments:** Credit cards, student loans, other obligations
- **Healthcare:** Regular medications, co-pays
- **Exclude:** Dining out, entertainment, travel, shopping, subscriptions that can be cancelled

### Expense-Based Sizing
Monthly essential expenses multiplied by the desired months of coverage:

- Emergency fund = monthly essential expenses × months of coverage
- Example: $4,500/month essentials × 6 months = $27,000
- More precise than income-based because it reflects actual spending needs during a crisis

### Income Replacement Approach
After-tax monthly income multiplied by months of coverage:

- Emergency fund = after-tax monthly income × months of coverage
- Simpler to calculate but may overstate need (assumes maintaining full spending during emergency)
- Useful as an upper bound or for high earners whose expenses scale with income

### Variable Income Adjustment
For commission-based, freelance, seasonal, or gig workers:

- Calculate average monthly income over 12-24 months
- Set base budget at the lowest 3-month average income level
- Buffer = average income - base budget (accumulated during high-earning months)
- Emergency fund should be 6-12 months of essential expenses (longer because income disruption is more likely and less predictable)
- Maintain a separate "income smoothing" buffer beyond the emergency fund

### Tiered Emergency Fund
Structure the fund across tiers for optimal balance of access and yield:

- **Tier 1 — Immediate access (1 month):** Checking or savings account at primary bank. Instantly accessible for urgent needs. Low or no yield, but maximum liquidity.
- **Tier 2 — Short-term (2-3 months):** High-yield savings account (HYSA) or money market fund. Available in 1-2 business days. Earns competitive short-term rates.
- **Tier 3 — Extended (3-6 months):** Short-term Treasury bills, I-bonds (after 1-year lock-up), short-term bond fund, or CD ladder. May take a few days to a few weeks to access. Higher yield compensates for slightly lower liquidity.

### Vehicle Selection

| Vehicle | Yield | Liquidity | FDIC/SIPC | Best For |
|---------|-------|-----------|-----------|----------|
| Checking account | Very low | Instant | FDIC | Tier 1 (1 month) |
| HYSA | Moderate | 1-2 days | FDIC | Tier 2 (core fund) |
| Money market fund | Moderate | 1-2 days | SIPC | Tier 2 (core fund) |
| T-bills (4-week) | Moderate-high | At maturity | Full faith & credit | Tier 2/3 (ladder) |
| CD (3-12 month) | Moderate-high | At maturity (penalty) | FDIC | Tier 3 (ladder) |
| I-bonds | Inflation-linked | After 12 months | Full faith & credit | Tier 3 (long-term) |
| Short-term bond fund | Variable | 1-3 days | SIPC | Tier 3 (flexible) |

### Opportunity Cost
Holding cash has a real cost — the difference between what the cash earns and what it could earn if invested:

- **Cash drag:** Emergency fund earning 4% HYSA vs 8-10% equity expected return = 4-6% annual opportunity cost
- On a $30K emergency fund: $1,200-$1,800/year in foregone returns
- **Mitigant:** The purpose of the fund is insurance, not investment return. The "premium" is the opportunity cost.
- **Over-funded risk:** Holding 12+ months when 3-6 months suffices wastes significant capital
- **Under-funded risk:** Having to use credit cards at 20%+ APR or sell investments at a loss during an emergency

### When to Tap the Emergency Fund
**Appropriate uses:**
- Job loss or significant income reduction
- Medical emergency or unexpected healthcare costs
- Essential home repair (roof leak, HVAC failure, plumbing emergency)
- Essential car repair (needed for commuting to work)
- Unexpected essential travel (family emergency)

**NOT appropriate uses:**
- Vacations or planned travel
- Planned purchases (holiday gifts, electronics)
- Investment opportunities ("buy the dip")
- Non-essential home improvements
- Expenses that should have been budgeted (annual insurance, property tax)

### Replenishment Plan
After using the emergency fund:

- Prioritize rebuilding before resuming discretionary spending or non-essential savings goals
- Set a monthly replenishment target (e.g., rebuild within 6-12 months)
- Temporarily reduce or pause contributions to other goals if needed
- Redirect windfalls (tax refund, bonus) to accelerate replenishment

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Expense-based fund | Monthly essentials × months of coverage | Core sizing calculation |
| Income-based fund | After-tax monthly income × months of coverage | Upper bound estimate |
| Opportunity cost | Fund balance × (investment return - cash return) | Cost of holding cash |
| Replenishment timeline | Fund shortfall / monthly replenishment amount | Months to rebuild |
| Variable income buffer | Avg monthly income - base budget | Surplus for smoothing |

## Worked Examples

### Example 1: Emergency fund sizing for a dual-income household
**Given:** Married couple, both employed in stable jobs. Monthly essential expenses: $4,500 (housing $1,800, food $600, insurance $400, utilities $300, transportation $500, debt minimums $400, healthcare $200, other essentials $300).
**Calculate:** Recommended emergency fund size.
**Solution:**
1. **Dual income, stable employment:** 3 months is the baseline; 4 months provides a comfortable margin.
2. **Emergency fund = $4,500 × 3 = $13,500** (minimum) to **$4,500 × 4 = $18,000** (recommended).
3. **Considerations:** If either spouse works in a cyclical industry or has less job security, increase to 6 months ($27,000).
4. **If one spouse could cover essentials alone:** May reduce to 3 months since the risk of zero income is lower.
5. **Recommendation:** $13,500-$18,000 for this stable dual-income household.

### Example 2: Tiered fund allocation
**Given:** Target emergency fund of $27,000 (6 months × $4,500/month) for a single-income household.
**Calculate:** Optimal tiered allocation.
**Solution:**
1. **Tier 1 — Checking account: $4,500 (1 month).** Immediate access for sudden expenses (car repair, medical co-pay). Earning ~0.01% but provides instant liquidity.
2. **Tier 2 — High-yield savings account: $13,500 (3 months).** Core emergency reserves. Earning ~4.5% APY (illustrative, in the ~4-5% range seen as of 2026 — check current HYSA rates). Available in 1-2 business days via transfer.
3. **Tier 3 — T-bill ladder: $9,000 (2 months).** Three $3,000 T-bills maturing at 4-week, 8-week, and 13-week intervals. Earning ~4.8% (illustrative, in the ~4-5% range seen as of 2026 — check current T-bill rates). At least one tranche matures every ~4 weeks.
4. **Blended yield:** (4,500 × 0.01% + 13,500 × 4.5% + 9,000 × 4.8%) / 27,000 ≈ **3.85% weighted average.**
5. **vs all checking (0.01%):** Earning ~$1,040/year more with the tiered approach — effectively free money for modest complexity.

## Common Pitfalls
- Too little: financial stress during emergencies, forced to use high-interest debt (credit cards at 20%+), potential to sell investments at a loss
- Too much: significant opportunity cost from excess cash eroded by inflation; common among risk-averse savers
- Not adjusting for life changes — new baby (higher expenses), job change (less stability), mortgage (larger fixed obligation), spouse stops working
- Keeping the emergency fund in investments that can lose value — stocks, long-term bonds, or crypto are not appropriate vehicles
- Using the emergency fund for non-emergencies — erodes the safety net and creates a cycle of depletion
- Not having a replenishment plan — spending the fund without a strategy to rebuild leaves ongoing vulnerability
- Ignoring inflation: a $20K fund in 2020 has less purchasing power in 2030; periodically reassess the target
- Treating the emergency fund as an investment account rather than an insurance policy

## Cross-References
- **liquidity-management** (wealth-management plugin): emergency fund is the foundation of the personal liquidity tier structure
- **savings-goals** (wealth-management plugin): emergency fund is typically the highest priority savings goal
- **debt-management** (wealth-management plugin): adequate emergency fund prevents taking on new high-interest debt during crises
- **lending** (wealth-management plugin): emergency reserves are a factor in mortgage qualification
- **investment-policy** (wealth-management plugin): emergency fund size feeds the liquidity constraint in an IPS
- **financial-planning-workflow** (advisory-practice plugin): emergency fund adequacy is assessed early in the comprehensive financial planning process
- **insurance-planning** (wealth-management plugin): emergency fund size supports higher deductibles and longer disability elimination periods in the risk retention decision
- **retirement-decumulation** (wealth-management plugin): the cash-reserve discipline extends into retirement as bucket one of a bucket withdrawal strategy
## Running the Script

```bash
uv run scripts/emergency_fund.py            # run the demo (uses PEP 723 inline deps)
uv run scripts/emergency_fund.py --verify   # check demo outputs against the worked examples (exit 1 on mismatch)
python3 scripts/emergency_fund.py            # alternative (requires: pip install numpy)
```

The demo prints the calculations covered above; its values match the worked examples in this skill. Run `--help` for a list of the classes and functions. For programmatic use, import the module rather than running it — the demo only executes under `python emergency_fund.py`.


---

## SKILL: equities

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/equities` (MIT)
- Cuándo usarla: Analyze equity securities, factor models, and equity portfolio construction. Use when the user asks about stocks, equity valuation ratios, index construction methods, or style analysis. Also trigger when users mention 'P/E ratio', 'growth vs value', 'market cap weighting', 'sector allocation', 'GICS classification', 'earnings per share', 'Fama-French factors', 'CAPM', 'dividend yield', 'PEG ratio', 'EV/EBITDA', or ask which factors explain equity returns.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/wealth-management/skills/equities/` (equities.py)

# Equities

This skill is a decision procedure: which valuation metric to use for which company, which index methodology fits which mandate, and the order of operations for analyzing a stock. It assumes the user can look up definitions; the value here is choosing the right tool.

## Core Concepts

### Choosing the Valuation Metric

Match the metric to the sector and capital structure — using the wrong one is the most common equity-analysis error.

| Situation | Use | Avoid | Why |
|-----------|-----|-------|-----|
| Financials (banks, insurers) | P/B, P/TBV, ROE vs P/B | EV/EBITDA | Debt is raw material, not financing — EV and EBITDA are meaningless; book value is marked closer to fair value |
| Capital-intensive (industrials, telecom, energy) | EV/EBITDA, EV/EBIT | P/E alone | Neutralizes depreciation policy and leverage differences across peers |
| Mature dividend payers (utilities, staples) | Dividend yield + payout sustainability, P/E | PEG | Growth is low and stable; income and coverage matter most |
| High-growth, low/no earnings | EV/Sales, PEG (if earnings exist), unit economics | P/E, P/B | Earnings are depressed by reinvestment; book value is mostly intangibles |
| Cyclicals (autos, semis, materials) | Mid-cycle or normalized P/E, P/B at trough | Spot P/E | P/E is lowest at the cycle peak and highest at the trough — spot P/E inverts the buy/sell signal |
| Negative earnings, positive cash flow | EV/EBITDA, P/FCF | P/E, earnings yield | Ratio is undefined or misleading with negative denominator |
| REITs and listed real estate | P/FFO, P/AFFO, NAV | P/E | GAAP depreciation distorts earnings for property — handled in detail by the real-assets skill |
| Cross-border / different leverage | EV-based multiples | Equity multiples | Enterprise value normalizes for capital structure |

Cross-checks that apply everywhere:
- Use forward (next-12-month) estimates for the numerator decision when the business is changing; trailing figures when estimate quality is poor.
- Compare against the company's own history and a true peer set, not the whole market.
- Translate any multiple into its implied assumptions (growth, margin, required return) before declaring cheap/expensive — a low multiple usually encodes a real problem.

### Choosing the Index Methodology

| Mandate | Methodology | Trade-off to flag |
|---------|-------------|-------------------|
| Cheap, tax-efficient market exposure | Cap-weighted (S&P 500, total market) | Momentum-chasing by construction; concentration in mega-caps — a single sector can exceed 30% |
| Reduce concentration / small-cap tilt | Equal-weighted | Higher turnover and rebalancing cost; structural size and contrarian tilt |
| Break the price-weight link | Fundamental-weighted (revenue, earnings, book) | Effectively a value tilt with extra steps; compare cost vs an explicit value fund |
| Explicit factor exposure | Factor/style index (value, momentum, quality, low vol) | Verify the factor definition and rebalance rules; factor timing rarely works |
| Avoid | Price-weighted (DJIA-style) | Weight proportional to share price is economically arbitrary — legacy only |

Selection rules: default to cap-weighted for core beta; add equal- or fundamental-weighted only when the user explicitly wants the embedded tilt and accepts the turnover; treat any "smart beta" product as a factor portfolio and evaluate its factor loadings, not its marketing name.

### Security Analysis Sequence

1. **Classify the business** — sector (GICS or equivalent), cyclical vs defensive, capital intensity, leverage. This determines the valuation toolkit (table above).
2. **Quality screen** — revenue trend, margin trend, ROIC vs cost of capital, balance-sheet risk (net debt/EBITDA, interest coverage), share count trajectory (dilution vs buybacks).
3. **Earnings basis** — pick trailing vs forward EPS, check for one-offs, use diluted share count. For cyclicals, normalize to mid-cycle.
4. **Value with the matched metric** — primary multiple from the table, one cross-check multiple, and where dividends are central a dividend-based check (Gordon growth: P = D1 / (r - g), valid only when g < r).
5. **Factor and style context** — regress (or eyeball) exposures to market beta, size, value, momentum, quality. Distinguish stock-specific thesis from a factor bet you could buy more cheaply via an index.
6. **Portfolio fit** — marginal effect on sector concentration and factor tilts; total return (price + dividends) is the comparison basis, never price return alone.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| EV/EBITDA | (Market Cap + Debt - Cash) / EBITDA | Capital-structure-neutral valuation |
| Earnings Yield | EPS / Price | Compare equity vs bond yields |
| PEG | (P/E) / Earnings Growth Rate (in %) | Growth-adjusted valuation |
| Gordon Growth | P = D1 / (r - g) | Dividend-based intrinsic value |
| CAPM | E(R) = R_f + beta × (E(R_m) - R_f) | Required return input for valuation |
| Total Return | Price Return + Dividend Return | Performance comparison basis |

## Worked Examples

### Metric Selection and Valuation

**Given:** An industrial company with market cap $500M, total debt $100M, cash $50M, EBITDA $75M, EPS $7.50, price $150.
**Decide and calculate:**
1. Capital-intensive industrial → primary metric is EV/EBITDA (table above), with P/E as cross-check.
2. EV = $500M + $100M - $50M = $550M. EV/EBITDA = $550M / $75M = **7.33x**.
3. Cross-check: P/E = $150 / $7.50 = 20.0x; earnings yield = 7.50 / 150 = **5.0%**.
4. Interpretation: 7.33x EV/EBITDA is modest for an industrial if margins are stable — compare against the peer set and the company's own 5-10 year range. The 20x P/E looks richer than the EV multiple because the company carries little net debt; the EV multiple is the better cross-peer comparison.

## Common Pitfalls
- Applying EV/EBITDA to banks or P/E to REITs — metric/sector mismatch is the dominant error this skill exists to prevent
- Buying cyclicals on low trailing P/E at the cycle peak (the "value trap" inversion)
- Treating a fundamental-weighted or smart-beta index as alpha rather than a packaged factor tilt
- Confusing price return with total return — dividends compound to a large share of long-run equity returns
- Survivorship bias in backtested factor or screen results

## Cross-References
- **historical-risk** (wealth-management plugin): volatility and drawdown measurement for equity return series
- **statistics-fundamentals** (core plugin): beta estimation via CAPM regression
- **performance-metrics** (wealth-management plugin): Sharpe ratio and related risk-adjusted return measures
- **fund-vehicles** (wealth-management plugin): equity fund selection (ETFs, mutual funds, SMAs)
- **currencies-and-fx** (wealth-management plugin): international equity currency effects
- **asset-allocation** (wealth-management plugin): equity allocation within multi-asset portfolios
- **real-assets** (wealth-management plugin): REIT valuation (P/FFO, NAV) is owned by that skill
- **qualitative-valuation** (wealth-management plugin) and **quantitative-valuation** (wealth-management plugin): deeper single-company valuation workflows
- **financial-statements** (wealth-management plugin): EBITDA, free cash flow, ROIC, and margin analysis underpinning fundamental stock selection
- **equity-compensation** (wealth-management plugin): employer stock acquired through RSUs, options, and ESPPs carries equity risk plus tax and insider-trading constraints
- **factor-investing** (wealth-management plugin): the factor-loading evaluation of smart-beta and style products prescribed above lives in that skill
## Running the Script

```bash
uv run scripts/equities.py            # run the demo (uses PEP 723 inline deps)
uv run scripts/equities.py --verify   # check demo outputs against the worked example (exit 1 on mismatch)
python3 scripts/equities.py            # alternative (requires: pip install numpy)
```

The demo prints valuation metrics (including the worked example's EV/EBITDA and earnings yield), a factor regression on synthetic data, and sector concentration analysis. Run `--help` for a list of the classes and functions. For programmatic use, import the module rather than running it — the demo only executes under `python equities.py`.


---

## SKILL: equity-compensation

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/equity-compensation` (MIT)
- Cuándo usarla: Guides equity compensation planning for wealth management clients: RSU vesting and the supplemental-withholding gap, NSO and ISO exercise taxation, AMT on ISO spreads and the AMT credit, qualifying vs disqualifying dispositions, 83(b) elections for restricted stock, qualified Section 423 ESPPs, and managing concentrated employer stock (staged diversification, exchange funds, protective collars, charitable strategies, Rule 10b5-1 trading plans, Section 16 insider constraints). Use when the user asks about stock options, RSUs, ESPP purchases, or trading windows — e.g. 'my RSUs vested', 'should I exercise my ISOs', 'will I get an AMT hit', 'file an 83(b) election', 'disqualifying disposition', 'set up a 10b5-1 plan', 'I have too much company stock', or questions about selling employer shares as an executive or insider.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/wealth-management/skills/equity-compensation/` (equity_compensation.py)

# Equity Compensation

## Core Concepts

### Restricted Stock Units (RSUs)
RSUs are a promise of shares delivered at vesting. There is no election to make and no exercise decision:

- **Taxation:** Full FMV of shares at vest is ordinary income (W-2 wages), subject to income tax, Social Security (up to the wage base), and Medicare. Cost basis = FMV at vest; holding period starts at vest.
- **Withholding shortfall trap:** Employers withhold federal tax on RSU income at the flat supplemental wage rate — 22% on supplemental wages up to $1 million cumulative for the year, with a mandatory 37% rate on the excess above $1 million (rates as of 2026, tied to statutory brackets — verify current). A client whose actual marginal rate is 32-37% is systematically under-withheld and can face a large April balance due plus underpayment penalties. Plan estimated payments or extra withholding in vest years.
- **Post-vest decision:** Holding vested RSU shares is economically identical to buying employer stock with a cash bonus. The default recommendation is sell-at-vest unless there is a deliberate concentration thesis; there is no tax benefit to holding beyond starting the capital gains clock.

### Nonqualified Stock Options (NSOs)
- **At exercise:** Spread (FMV − strike) × shares is ordinary income (W-2 for employees), with payroll tax and withholding. Basis = FMV at exercise; subsequent gain/loss is capital.
- **No AMT preference** — NSO taxation is entirely in the regular system.
- Exercise timing is a bet on rate arbitrage and appreciation: early exercise moves future appreciation from ordinary income to capital gains but accelerates tax and concentrates risk.

### Incentive Stock Options (ISOs)
- **At exercise:** No regular-tax income. The spread (FMV − strike) × shares is an AMT preference item in the exercise year (unless the shares are sold in a disqualifying disposition in that same calendar year, which eliminates the AMT adjustment).
- **Qualifying disposition:** Sale more than 2 years from grant AND more than 1 year from exercise. Entire gain over strike is long-term capital gain.
- **Disqualifying disposition:** Either holding test fails. Spread at exercise (capped at actual gain if the stock declined) becomes ordinary income in the year of sale; any gain above FMV-at-exercise is capital gain (short- or long-term by holding period from exercise). No payroll tax on the ordinary portion.
- **$100,000 ISO limit:** Aggregate grant-date FMV of ISOs first exercisable in any calendar year cannot exceed $100,000 (IRC 422(d)). This is a statutory figure and is NOT inflation-indexed. The excess is treated as NSOs.
- ISOs must be exercised within 3 months of termination (12 months for disability) to retain ISO status.

### The AMT Mechanism and AMT Credit
The alternative minimum tax is a parallel tax computation. Simplified flow:

1. Start with regular taxable income, add back preference/adjustment items (the ISO spread is the dominant one for equity-comp clients) to get AMTI.
2. Subtract the AMT exemption — an inflation-indexed amount (in the low-to-mid $130,000s for MFJ as of recent years — verify the current figure) that phases out above a high AMTI threshold (thresholds and phaseout rate were changed by 2025 tax legislation effective 2026 — verify current parameters before advising).
3. Apply the two AMT rates: 26% up to an indexed breakpoint (roughly the low $200,000s of AMT base — verify current) and 28% above it, giving the tentative minimum tax (TMT).
4. AMT due = max(0, TMT − regular tax). The client pays the higher of the two systems.

**AMT credit:** AMT paid on *deferral* items (like the ISO spread) generates a minimum tax credit carried forward indefinitely, usable in future years when regular tax exceeds TMT. The ISO AMT is largely a prepayment, not a permanent cost — but the credit can take many years to recover. Shares exercised also get a higher AMT basis (FMV at exercise), so a later qualifying sale produces a smaller AMT gain, helping unlock the credit.

**Planning levers:** Exercise early in the year (option to disqualify before Dec 31 if the stock collapses — the classic dot-com trap was owing AMT on vanished paper gains); exercise only up to the "AMT crossover" amount where TMT just equals regular tax; spread exercises across years.

### 83(b) Elections (Restricted Stock, Not RSUs)
For restricted *stock* (including early-exercised options), Section 83(b) lets the holder elect to be taxed at grant/early-exercise on (FMV − price paid) rather than at vesting:

- **30-day deadline from the transfer date — statutory, no extensions.** File with the IRS and give a copy to the employer.
- Converts all post-grant appreciation to capital gain and starts the holding period immediately. Most valuable when current spread is near zero (founder stock, early exercise at strike = FMV).
- **Risk:** Tax paid is not refundable if the shares are later forfeited; no deduction for the forfeited income (only a capital loss for actual amounts paid).
- RSUs are not eligible — there is no property transferred at grant.

### Employee Stock Purchase Plans (ESPP, Section 423)
- Qualified plans allow purchase at up to a 15% discount, often with a lookback applying the discount to the lower of the offering-date or purchase-date price. Statutory cap: $25,000 per year of stock (valued at offering-date FMV) — IRC 423(b)(8), not indexed.
- **Qualifying disposition** (>2 years from offering date and >1 year from purchase): ordinary income = the lesser of (a) actual gain and (b) the discount computed on the offering-date price; the rest is long-term capital gain. With a lookback and an appreciated stock, this often converts most of the gain to LTCG.
- **Disqualifying disposition:** ordinary income = FMV at purchase − purchase price (the full bargain element, even if later sold at a loss); remainder is capital gain/loss.
- A 15% discount with a 6-month purchase period is roughly a 15/85 ≈ 17.6% return over ≤6 months even selling immediately — max participation with immediate sale is the low-risk baseline recommendation; holding for qualifying treatment adds concentration risk for a modest tax benefit.

### Concentrated Stock Management
A single position above roughly 10% of net worth warrants a plan. Tools, in rough order of simplicity:

- **Staged diversification:** Preset sell schedule (e.g., equal tranches quarterly over 1-3 years) removes timing regret and market-timing behavior; coordinate lots (highest basis first) and gain budgets with the tax plan; insiders execute via a 10b5-1 plan.
- **Charitable strategies:** Donate long-term appreciated shares directly (or to a donor-advised fund) — full FMV deduction and the embedded gain is never taxed. Charitable remainder trusts (CRTs) allow diversification inside the trust with tax deferral and an income stream.
- **Exchange funds:** Contribute the concentrated position to a partnership pooling many investors' stocks; receive diversified units without a current sale. Requires a 7-year holding period for tax-deferred treatment (redemption in kind carries over basis); funds must hold at least 20% in qualifying illiquid assets; expect fees, lockup, limited control, and accreditation requirements.
- **Protective collars:** Buy a put, sell a call (often zero-premium). Caps downside without a sale. Watch: a collar that is too tight risks constructive-sale treatment under IRC 1259 (no bright line; meaningful band retained in practice); straddle rules can suspend the holding period and defer losses; a protective put on stock not yet held long-term restarts/suspends the LTCG clock. Collared stock supports high loan-to-value margin borrowing for diversification or liquidity ("collar and loan").
- **Completion strategies:** Build the rest of the portfolio to underweight the employer's sector so total exposure is closer to market weight.

### Rule 10b5-1 Plans and Section 16 (High Level)
- A Rule 10b5-1 plan is a written trading plan adopted while not in possession of MNPI, giving an affirmative defense to insider-trading liability for trades executed later under its formula.
- **2022 SEC amendments (effective February 2023):** Mandatory cooling-off periods before the first trade — for directors and officers, the later of 90 days after adoption/modification or 2 business days after filing the 10-Q/10-K covering the adoption quarter, capped at 120 days; for other insiders, 30 days. Also: good-faith condition, director/officer certification, a general bar on overlapping plans, one single-trade plan per 12 months, and quarterly issuer disclosure of plan adoptions/terminations.
- **Section 16** (directors, officers, >10% holders): Form 4 within 2 business days of transactions; short-swing profit recapture under 16(b) on matched purchases and sales within 6 months (this can trap ESPP/option activity paired with open-market sales). Affiliates selling in the open market are also subject to Rule 144 volume limits and Form 144 filings. Coordinate every diversification plan with company counsel and the insider-trading policy's window periods.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| RSU income at vest | shares × FMV_vest | Ordinary W-2 income |
| RSU withholding gap | income × (t_marginal − t_supplemental) | Estimated additional tax due in April |
| NSO ordinary income | shares × (FMV_exercise − strike) | Taxed at exercise, ordinary rates |
| ISO AMT preference | shares × (FMV_exercise − strike) | Added to AMTI in exercise year |
| Tentative minimum tax | 26% × base up to breakpoint + 28% × excess, base = AMTI − exemption | Parallel AMT computation |
| AMT due / credit | max(0, TMT − regular tax) | Incremental tax; credit carryforward for deferral items |
| Disqualifying ISO ordinary income | min(FMV_exercise, sale price) − strike, floored at 0 | Ordinary portion when holding test fails |
| ESPP qualifying ordinary income | min(actual gain, discount% × offer-date FMV) | Ordinary portion; remainder LTCG |

## Worked Examples

### Example 1: RSU withholding gap
**Given:** 10,000 RSUs vest at $40/share. Employer withholds federal tax at the 22% supplemental rate (net-share settlement). Client's actual federal marginal rate: 35%.
**Solution:**
1. Ordinary income at vest: 10,000 × $40 = **$400,000** (W-2).
2. Federal withholding: $400,000 × 22% = $88,000 → 2,200 shares withheld; client receives **7,800 net shares**.
3. Actual federal tax on the vest income: $400,000 × 35% = $140,000.
4. **Shortfall: $140,000 − $88,000 = $52,000** owed at filing — before state tax and any Medicare surtax. The client should make an estimated payment in the vest quarter to avoid underpayment penalties.

### Example 2: ISO exercise AMT computation
**Given:** Exercise 5,000 ISOs, strike $10, FMV at exercise $50, and hold the shares. Other AMTI (income after regular deductions, before the spread): $250,000 MFJ. Regular tax: $60,000. Illustrative AMT parameters: exemption $137,000 with no phaseout at this income level, 28% rate above $220,000 of AMT base (both figures indexed — verify current year).
**Solution:**
1. AMT preference (spread): 5,000 × ($50 − $10) = **$200,000**. No regular-tax income.
2. AMTI: $250,000 + $200,000 = $450,000.
3. AMT base: $450,000 − $137,000 = $313,000.
4. TMT: 26% × $220,000 + 28% × ($313,000 − $220,000) = $57,200 + $26,040 = **$83,240**.
5. AMT due: $83,240 − $60,000 = **$23,240** on top of regular tax — an effective 11.6% prepayment on the $200,000 spread, carried forward as a minimum tax credit for future years when regular tax exceeds TMT.
6. AMT basis in the shares becomes $50 (vs $10 regular basis), shrinking the AMT gain on a later qualifying sale and helping recover the credit.

### Example 3: Disqualifying vs qualifying ISO disposition
**Given:** 2,000 ISOs, strike $15, exercised at FMV $35, later sold at $60. Ordinary/STCG rate 35%, LTCG rate 15%.
**Qualifying (>2 yrs from grant, >1 yr from exercise):**
1. Entire gain is LTCG: 2,000 × ($60 − $15) = $90,000. Tax: $90,000 × 15% = **$13,500**. (The $40,000 spread was an AMT preference in the exercise year — see Example 2 mechanics.)
**Disqualifying (sold 8 months after exercise):**
2. Ordinary income = spread at exercise: 2,000 × ($35 − $15) = $40,000 → tax $14,000.
3. Remaining gain is STCG: 2,000 × ($60 − $35) = $50,000 → tax $17,500.
4. Total: **$31,500** — **$18,000 more** than the qualifying path. If the sale had occurred in the same calendar year as exercise, the AMT preference on the spread would be eliminated, which can make deliberate same-year disqualification rational when the stock has fallen.

## Common Pitfalls
- Assuming the RSU shares withheld at vest cover the full tax bill — the 22% supplemental rate (as of 2026 — verify current) under-withholds for anyone in the 32%+ brackets
- Exercising ISOs late in the year and holding: if the stock collapses the next year, AMT is still owed on the vanished exercise-date spread; exercising early in the year preserves the same-year disqualification escape hatch
- Missing the 83(b) 30-day deadline (statutory, no relief) or filing one for RSUs, which are ineligible
- Treating the AMT on ISO exercise as a permanent cost — it is mostly a prepayment recoverable via the minimum tax credit, but model the recovery timeline
- Breaking the ISO $100,000 first-exercisable-per-year limit (statutory, NOT indexed) with a large grant and assuming everything is ISO — the excess is NSO
- Selling ESPP shares one day short of the offering-date or purchase-date holding tests, converting favorable qualifying treatment into full bargain-element ordinary income
- Forgetting that a disqualifying ESPP or ISO disposition creates ordinary income even when the position is sold at an overall loss relative to the purchase-date FMV
- Letting an insider sell without a 10b5-1 plan, or trading before the cooling-off period ends (directors/officers: up to 120 days under the 2022 amendments, effective February 2023)
- Matching an open-market sale against any purchase (including ESPP) within 6 months as a Section 16 insider — short-swing profit recapture applies mechanically
- Writing a collar so tight it risks constructive-sale treatment, or ignoring straddle rules that suspend the holding period on unhedged appreciation
- Ignoring wash-sale interactions: recurring RSU vests and ESPP purchases can wash out losses harvested on employer stock in the surrounding 61-day window
- Anchoring on the grant-date or peak price ("I'll diversify when it gets back to $X") instead of treating vested equity as cash compensation to be invested per the plan

## Cross-References
- **tax-efficiency** (wealth-management plugin): bracket management around vest and exercise years, lot selection when diversifying, and charitable giving with appreciated employer stock
- **diversification** (wealth-management plugin): concentrated single-stock exposure from equity compensation is the classic case for staged diversification and completion portfolios
- **equities** (wealth-management plugin): valuation and risk characteristics of the underlying employer shares inform hold/sell and exercise decisions
- **liquidity-management** (wealth-management plugin): funding exercise costs, AMT bills, and withholding shortfalls without forced sales requires planned liquidity
- **tax-loss-harvesting** (wealth-management plugin): harvested losses offset gains realized while diversifying; recurring vests and ESPP purchases create wash-sale exposure on employer stock
- **investment-suitability** (compliance plugin): concentration levels and insider status are suitability considerations for hedging, lending, and diversification recommendations

## Running the script
Run with `uv run scripts/equity_compensation.py` (the PEP 723 header resolves dependencies automatically) or directly with `python3 scripts/equity_compensation.py` (standard library only). The bare run prints a demo covering RSU vest withholding and the withholding gap, an NSO exercise, the simplified ISO/AMT computation, qualifying vs disqualifying ISO dispositions, and ESPP purchase/disposition taxation. Pass `--verify` to assert the outputs match this skill's worked examples (prints PASS/FAIL and exits nonzero on mismatch), or `--help` for an overview of the available methods. The file is primarily meant to be imported as a module (e.g., `from equity_compensation import EquityCompensation`).


---

## SKILL: estate-gifting

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/estate-gifting` (MIT)
- Cuándo usarla: Estate and gifting architecture for wealth management: the unified estate/gift/GST framework, lifetime exemption vs annual exclusion, basis step-up vs carryover, trust taxonomy, and beneficiary planning. Use when the user asks about the 'estate tax exemption', 'annual gift exclusion', 'step-up in basis', a 'revocable trust' or 'irrevocable trust', 'gifting to my kids', '529 superfunding', or the 'portability election'. Also trigger on questions about gift-splitting, Form 706 or Form 709, DSUE, ILITs, GRATs, SLATs, IDGTs, charitable remainder trusts, state estate or inheritance taxes, the SECURE Act 10-year rule for inherited IRAs, whether to gift appreciated stock now or leave it at death, or how to fund estate taxes for an illiquid estate. For income-tax angles of charitable giving (QCDs, donating appreciated securities, DAF bunching), see the tax-efficiency skill.

# Estate and Gifting Strategy

## Core Concepts

### The Unified Estate/Gift/GST Framework
Federal transfer taxes operate as one unified system: lifetime taxable gifts and the estate at death draw down a single lifetime exemption, with a flat 40% tax on transfers above it.

- **Lifetime exemption:** $15 million per person effective 2026 under the One Big Beautiful Bill Act (2025), indexed for inflation thereafter — verify the current-year figure. This made the higher exemption permanent and replaced the scheduled TCJA sunset; the pre-2026 planning frame of "use it before it drops to ~$7M" is obsolete. Urgency-driven exemption-use strategies should be re-evaluated on their standalone merits.
- **Annual gift exclusion:** $19,000 per donor per recipient as of 2025, indexed in $1,000 increments — verify the current-year figure. Exclusion gifts consume no lifetime exemption and require no gift tax return if that is the only gifting.
- **Gift-splitting:** Spouses may elect on Form 709 to treat gifts made by either as made half by each, doubling the effective exclusion per recipient ($38,000 per couple per recipient as of 2025). The election applies to all gifts by both spouses that year.
- **GST tax:** A separate exemption (same dollar amount as the estate exemption) applies to transfers that skip a generation (e.g., to grandchildren or to trusts that will benefit them). GST exemption must be affirmatively allocated (often on Form 709) to shelter trusts intended to last for multiple generations.
- **Filing mechanics:** Gifts above the annual exclusion are reported on Form 709 and reduce the lifetime exemption; no tax is due until the exemption is exhausted. The estate tax return is Form 706.

### Portability and the DSUE
A deceased spouse's unused exemption (DSUE) can transfer to the survivor — but only by election:

- The executor must file a **timely Form 706 to elect portability**, even when no tax is due and no return would otherwise be required. A simplified late election (Rev. Proc. 2022-32) is available up to five years after death for estates not otherwise required to file, but relying on it is a fallback, not a plan.
- The survivor's shelter becomes their own exemption plus the DSUE amount. DSUE is frozen at the first death (not indexed afterward), and remarriage followed by the new spouse's death can forfeit a prior DSUE.
- **The GST catch: GST exemption is not portable.** A couple relying solely on portability wastes the first spouse's GST exemption. Families with generation-skipping intent generally need trust planning (e.g., a credit shelter/bypass trust with GST allocation) at the first death, not portability alone.

### Step-Up at Death vs Carryover Basis for Gifts
The central gift-or-bequeath tradeoff:

- **Assets transferred at death** receive a basis step-up (or step-down) to date-of-death fair market value, erasing unrealized gains for income tax purposes.
- **Gifted assets carry over** the donor's basis (for gain purposes; for loss purposes the recipient uses the lower of carryover basis or FMV at gift).
- **Rule of thumb:** For estates comfortably under the exemption, hold low-basis appreciated assets until death (free step-up) and gift cash or high-basis assets. For taxable estates, lifetime gifts of appreciating assets remove future appreciation from the 40% estate tax base — often worth more than the forgone step-up. The breakeven depends on estate tax exposure, embedded gain, expected appreciation, and the heir's capital gains rate.
- Gifting loss positions is almost always wrong: the built-in loss can vanish under the dual-basis rule. The donor should sell (harvest the loss) and gift proceeds instead.

### Annual Gifting Programs
Systematic use of the free transfer channels:

- **Exclusion gifts:** $19,000 per donor per recipient as of 2025 (see above). A married couple with three married children and six grandchildren can move $456,000 per year ($38,000 x 12 recipients) with no exemption use — compounding over a decade, a material estate reduction.
- **Direct payment of tuition and medical expenses** (IRC 2503(e)) is an unlimited exclusion — not indexed, not capped — provided payment goes directly to the institution or provider, never through the beneficiary. Tuition only (not room, board, or books); medical includes health insurance premiums.
- **529 superfunding:** A donor may elect (Form 709) to treat a lump-sum 529 contribution as made ratably over five years — 5x the annual exclusion at once ($95,000 per donor per beneficiary as of 2025). If the donor dies within the five years, the untaken years' portions are pulled back into the estate.

### Trust Taxonomy at Advisor Altitude
What each vehicle is for — advisors should recognize them, not draft them:

- **Revocable living trust:** Probate avoidance, privacy, incapacity management, and smooth multi-state property administration. It provides no estate or income tax savings — assets remain in the grantor's estate. Funding (retitling assets into the trust) is where these plans most often fail.
- **ILIT (irrevocable life insurance trust):** Owns life insurance so the death benefit stays outside the taxable estate; commonly the liquidity engine for illiquid estates. Premium gifts typically use annual exclusions via Crummey withdrawal powers.
- **GRAT (grantor retained annuity trust):** Transfers asset appreciation above the IRS 7520 hurdle rate to heirs at little or no gift tax cost; suited to concentrated positions or assets expected to appreciate rapidly.
- **IDGT (intentionally defective grantor trust):** The grantor pays the trust's income taxes (an additional tax-free transfer in effect) and can sell assets to the trust without recognizing gain; a workhorse for freezing estate value.
- **SLAT (spousal lifetime access trust):** Uses exemption on gifts to an irrevocable trust benefiting the spouse, keeping indirect household access to the assets. Reciprocal SLATs for both spouses must differ enough to avoid the reciprocal trust doctrine.
- **CRT (charitable remainder trust):** Income stream to the donor/family for a term or life, remainder to charity; useful for diversifying low-basis concentrated positions with deferred gain recognition.
- **CLT (charitable lead trust):** Mirror image — charity receives the lead payments, remainder passes to heirs at reduced transfer tax cost; attractive in low-rate environments.

### State Estate and Inheritance Taxes
Roughly a third of states impose their own estate tax, inheritance tax, or both, with exemptions far below the federal level — some states exempt only around $1-2 million, and inheritance-tax states tax the recipient based on relationship to the decedent (thresholds and rates vary by state; verify current law for the client's state of domicile and for any real property held in other states). A client irrelevant to federal estate tax may face a six-figure state bill, and out-of-state real estate can trigger ancillary probate and a second state's tax. Domicile changes must be genuinely established, not merely declared.

### Retirement Account Beneficiary Planning
Beneficiary designations override wills and trusts — they are estate planning documents in their own right:

- **SECURE Act 10-year rule:** Most non-spouse beneficiaries of IRAs/401(k)s must empty the inherited account within 10 years of death (for deaths in 2020 or later). If the owner died on or after their required beginning date, the beneficiary must also take annual RMDs within the 10-year window.
- **Eligible designated beneficiaries (EDBs)** — surviving spouses, minor children of the owner (until majority, then 10-year rule), disabled or chronically ill individuals, and beneficiaries not more than 10 years younger — may still stretch over life expectancy; spouses can roll over to their own IRA.
- Consequences: the old "stretch IRA" for children is gone; large traditional IRAs left to high-earning children compress taxable income into 10 years. This raises the value of Roth conversions during the owner's lifetime, naming a spouse first, charitable beneficiaries for pre-tax dollars, and reviewing any trust named as beneficiary (conduit trusts drafted pre-SECURE can force a full year-10 distribution).

### Charitable Strategies at the Estate Level
Structure choice, deferring income-tax mechanics to the tax-efficiency skill: a **donor-advised fund** is the low-cost, low-administration default for most families (no payout mandate, successor advisors for a giving legacy); a **private foundation** offers control, family employment/governance, and perpetuity at the cost of a 5% minimum annual payout, excise tax, and public filings — generally sensible only above roughly $5-10 million of dedicated charitable capital; a **CRT/CLT** blends charitable and family transfers as above. Pre-tax retirement accounts are the most tax-efficient asset to leave to charity (no income tax on the charity, estate deduction for the estate); appreciated taxable assets are best left to heirs for the step-up.

### Liquidity Planning for Illiquid Estates
Federal estate tax is generally due nine months after death, in cash. Estates concentrated in businesses, real estate, or restricted stock need a liquidity plan: life insurance in an ILIT (the standard answer), standing buy-sell agreements funded with insurance, pre-arranged credit, IRC 6166 installment deferral for qualifying closely held business interests, or planned partial sales. Forced fire-sales of illiquid assets to meet the tax deadline are the classic failure mode.

### Practice Boundary
Advisors inform, model, and coordinate — they do not draft. Wills, trusts, powers of attorney, and beneficiary-designation strategies with legal effect require a licensed estate attorney; drafting documents or giving specific legal advice is unauthorized practice of law. The advisor's role is to identify exposure, quantify tradeoffs, maintain the balance sheet and beneficiary inventory, and ensure the attorney's design actually gets funded and titled correctly.

## Worked Examples

### Example 1: Gift now vs bequeath — the basis tradeoff
**Scenario:** A widowed client, total estate $8 million (comfortably under the $15 million exemption as of 2026), holds stock worth $1,000,000 with a $100,000 basis. She wants her daughter to have it and asks whether to gift it now or leave it in her will. Assume the daughter would sell promptly either way, at a 23.8% combined LTCG rate (20% + 3.8% NIIT).
**Analysis:** Gifted, the stock carries over the $100,000 basis. The daughter's sale realizes a $1,000,000 - $100,000 = $900,000 gain and $900,000 x 23.8% = $214,200 of tax, netting $785,800. Bequeathed, the basis steps up to $1,000,000 at death; a prompt sale realizes no gain, netting the full $1,000,000. Holding until death is worth **$214,200** — and since the estate is far below the exemption, gifting buys no estate tax benefit to offset it. If the client wants to transfer value now, she should gift cash or high-basis assets and keep the low-basis stock. The answer can flip for a taxable estate: if this stock were expected to triple inside a $25 million estate, removing the future appreciation from the 40% estate tax base could outweigh the heir's capital gains cost. Run the numbers both ways before defaulting to either rule.

### Example 2: Portability election — and the GST hole it leaves
**Scenario:** Husband dies in 2026 leaving his entire $6 million share outright to his wife. The marital deduction makes his taxable estate zero, so the executor sees no tax due and asks whether filing Form 706 is worth the cost. The couple's combined estate is $21 million and growing; there are children and young grandchildren.
**Analysis:** With no Form 706, the husband's roughly $15 million of unused exemption (as of 2026) evaporates. If the wife later dies with a $25 million estate and only her own $15 million exemption (ignoring later indexing for simplicity), $10 million is taxable at 40% — **$4,000,000 of tax**. A timely Form 706 electing portability gives her his DSUE, sheltering up to $30 million and reducing that tax to zero. The filing is cheap insurance and should be near-automatic at a first death in a wealthy household. But portability does not carry the GST exemption: if the family intends trusts for grandchildren, the husband's GST exemption is lost. That argues for funding a trust at the first death with his GST exemption allocated to it, rather than an outright marital bequest plus portability. Also note the DSUE is frozen — it does not index after his death — and could be forfeited if she remarries and survives the new spouse.

### Example 3: 529 superfunding for two grandchildren
**Scenario:** Grandparents (married, both willing to gift) want to front-load college funding for two newborn grandchildren without touching their lifetime exemptions.
**Analysis:** Each grandparent elects five-year averaging on Form 709 and contributes 5 x $19,000 = $95,000 per beneficiary (as of 2025 — verify the current exclusion). As a couple: $190,000 per grandchild, $380,000 total, all within annual exclusions. At 6% for 18 years, each grandchild's $190,000 grows to roughly $190,000 x 1.06^18 = **about $542,000** of tax-free education funding. Two cautions: the election absorbs those beneficiaries' annual exclusions for five years — further gifts to the same grandchildren in that window eat lifetime exemption — and if a donor dies in, say, year three, the two untaken years ($38,000 per beneficiary for that donor) are pulled back into the taxable estate. Direct tuition payments under 2503(e) remain available on top, unlimited, once the grandchildren are in school.

## Common Pitfalls
- Planning against the obsolete TCJA sunset frame ("exemption drops to ~$7M") — the One Big Beautiful Bill Act (2025) set a permanent $15 million exemption effective 2026, indexed thereafter; re-underwrite any urgency-driven strategy
- Skipping the Form 706 portability filing at a first death because "no tax is due" — the DSUE is lost without a timely (or qualifying late) election
- Assuming portability covers GST — the GST exemption is not portable and is wasted without trust planning at the first death
- Gifting low-basis appreciated assets out of an estate that will never owe estate tax, forfeiting a free step-up; or gifting loss positions, destroying the loss under the dual-basis rule
- Paying tuition or medical bills to the family member instead of directly to the institution/provider, converting an unlimited exclusion into an ordinary taxable gift
- Creating a revocable living trust and never retitling assets into it — the estate ends up in probate anyway
- Treating beneficiary designations as an afterthought: stale ex-spouse designations, estates named as IRA beneficiary, and pre-SECURE conduit trusts that now force a lump-sum year-10 payout
- Ignoring state estate and inheritance taxes with exemptions far below federal (thresholds vary by state — verify), and out-of-state real property that triggers ancillary probate
- No liquidity plan for an estate dominated by a business or real estate — the 40% federal tax is due in cash nine months after death
- Advisors drifting into drafting trust terms or amending documents — unauthorized practice of law; coordinate with the estate attorney instead

## Cross-References
- **tax-efficiency** (wealth-management plugin): owns the income-tax side — QCDs, donating appreciated securities, DAF bunching, Roth conversions that also shrink future taxable estates and inherited-IRA burdens
- **insurance-planning** (wealth-management plugin): life insurance design and ILIT ownership as the liquidity engine for estate taxes on illiquid estates
- **savings-goals** (wealth-management plugin): 529 plan mechanics and education funding targets that superfunding accelerates
- **investment-policy** (wealth-management plugin): trust provisions and multi-generational objectives enter the IPS as legal/regulatory and time-horizon constraints
- **financial-planning-workflow** (advisory-practice plugin): estate and beneficiary review is a standing module in the comprehensive planning process
- **client-onboarding** (advisory-practice plugin): opening and titling trust accounts, and capturing beneficiary designations correctly at account setup


---

## SKILL: fee-billing

- Fuente: `JoelLewis/finance_skills` → `plugins/advisory-practice/skills/fee-billing` (MIT)
- Cuándo usarla: Build and manage advisory fee billing operations from fee schedule design through calculation, collection, revenue recognition, and compliance disclosure. Use when the user asks about tiered or breakpoint fee schedules, billing cycle configuration, AUM valuation for billing, direct-debit vs invoice collection, GAAP revenue recognition for fees, ADV Part 2A or Reg BI fee disclosure, diagnosing billing exceptions or refunds, migrating from spreadsheet billing to automated systems, or forecasting advisory revenue. Also trigger when users mention 'fee calculation', 'billing engine', 'effective fee rate', 'household billing aggregation', 'mid-period adjustment', 'billing in advance vs arrears', 'fee compression', or 'ERISA 408(b)(2)'.

# Fee Billing

## Core Concepts

### 1. Fee Schedule Structures

Advisory firms employ a range of fee structures, often combining several within a single practice.

**Flat Fee (Fixed Dollar).** A predetermined dollar amount charged per period regardless of account size. Common for financial planning engagements or retainer-based advice. Straightforward to bill but disconnected from asset growth.

**AUM-Based (Percentage of Assets).** The most prevalent model for registered investment advisers. A single percentage (e.g., 1.00%) is applied to the market value of managed assets. Simple to communicate but can become expensive for large portfolios and cheap for small ones.

**Tiered / Breakpoint (Declining Rate).** A graduated schedule where successive tiers of assets are billed at progressively lower rates. For example:

| Tier | AUM Range | Annual Rate |
|------|-----------|-------------|
| 1 | First $500,000 | 1.00% |
| 2 | Next $500,000 | 0.80% |
| 3 | Next $1,000,000 | 0.60% |
| 4 | Over $2,000,000 | 0.40% |

Under a true tiered schedule each dollar is billed at the rate for the tier it falls within. Under a breakpoint schedule the entire balance is billed at the rate corresponding to the highest tier reached. The distinction matters significantly for large accounts and must be clearly defined in the advisory agreement.

**Flat-Plus-AUM Hybrid.** Combines a fixed planning fee with a lower AUM percentage. Useful for firms that want to be compensated for planning work independently of portfolio size.

**Hourly.** Charges based on advisor time. Rarely used as the sole billing method for ongoing relationships but common for project-based planning engagements.

**Financial Planning Fees.** One-time or recurring fees for plan creation and updates, often billed separately from investment management fees.

**Performance-Based Fees.** Permitted only for "qualified clients" under SEC Rule 205-3. Under the SEC's 2026 inflation adjustment (order issued April 2026, effective June 29, 2026), a qualified client must have at least $1.4 million in AUM with the adviser or a net worth exceeding $2.7 million — up from the $1.1 million / $2.2 million thresholds set in 2021. The SEC adjusts these thresholds for inflation every five years, and prior thresholds generally continue to apply to pre-existing contracts; verify current values. Requires a high-water mark or similar mechanism to prevent double-charging after drawdowns. Rarely used by typical RIAs due to complexity and regulatory constraints.

**Family / Household Billing Aggregation.** Assets across related accounts (spouses, trusts, custodial accounts, IRAs) are combined for fee-tier determination, then the calculated fee is allocated back to individual accounts. This gives the household the benefit of breakpoint pricing. The aggregation definition (who qualifies as "household") must be documented in the advisory agreement.

### 2. AUM Valuation for Billing

The accuracy and consistency of AUM valuation directly determines billing accuracy.

**Valuation Date Selection.** The most common approaches are:
- **Quarter-end value:** Assets valued as of the last business day of the billing quarter. Simple and widely used.
- **Prior quarter-end value:** Assets valued as of the end of the preceding quarter. Avoids billing on unrealized gains or losses that occurred during the period just ended. Common for advance billing.
- **Period average:** The average of daily or month-end values across the billing period. Smooths volatility but is operationally complex.

**Market Value vs. Cost Basis.** Nearly all advisory agreements specify market value. Cost basis would understate the true value being managed and is almost never used.

**Held-Away Assets.** Assets the adviser monitors but that are not custodied at the primary custodian (e.g., 401(k) plans, outside brokerage accounts, annuities). Whether these are included in the billable AUM depends on the advisory agreement. If included, obtaining timely and accurate valuations is a persistent operational challenge.

**Accrued Income.** Bond accrued interest and declared but unpaid dividends may be included or excluded. Most custodian feeds include accrued interest in the total market value, so the default is typically inclusion unless the fee schedule specifies otherwise.

**Margin Debit Treatment.** If a client uses margin, the question arises whether to bill on gross assets or net equity. The advisory agreement should specify. Most firms bill on net equity (gross market value minus margin balance).

**Cash Inclusion / Exclusion.** Some agreements exclude cash or money market positions from billable AUM, particularly if the adviser is not actively managing those balances. This is uncommon but must be handled when present.

**New Account Proration.** Accounts opened mid-period require proration. The standard method is to calculate the fee based on the number of days the account was open relative to the total days in the billing period. Some firms use a simpler approach and bill for the partial quarter only if the account was opened before the midpoint of the period.

### 3. Billing Cycle Mechanics

**Quarterly Billing.** The dominant cycle for RIAs. Billing quarters typically align with calendar quarters (Jan-Mar, Apr-Jun, Jul-Sep, Oct-Dec), though some firms use fiscal quarters.

**Monthly Billing.** Less common for investment management but used for financial planning retainers or firms that want to smooth revenue. Requires more operational overhead.

**Annual Billing.** Occasionally used for flat-fee or financial-planning-only arrangements. May be billed as a single payment or split into installments.

**Advance vs. Arrears Billing.**
- **Advance (in advance):** Fees are billed at the start of the period for services to be rendered. Creates a deferred revenue liability on the firm's balance sheet. Requires refund calculation for accounts terminated mid-period. Most common for RIAs.
- **Arrears (in arrears):** Fees are billed at the end of the period for services already rendered. Simpler from a revenue-recognition standpoint (revenue is earned when billed) but delays cash collection. Growing in popularity due to its alignment with the service delivery timeline.

**Pro-Ration Rules.** Events requiring proration include:
- Account openings mid-period
- Account closings or terminations mid-period
- Large contributions (some firms apply a materiality threshold, e.g., only prorate for contributions exceeding $10,000 or 10% of account value)
- Large withdrawals (same materiality threshold logic)
- Transfers between accounts within the same household (should be revenue-neutral)

The standard proration formula is:

```
Prorated Fee = Full-Period Fee * (Days in Period Account Was Active / Total Days in Period)
```

**Billing Period Alignment.** When a firm converts billing cycles (e.g., from quarterly to monthly), a transition period is needed. Clients should not be double-billed or under-billed during the switch. A reconciliation calculation comparing what was billed under the old cycle against what is owed under the new cycle is essential.

### 4. Fee Calculation Engine

A systematic fee calculation follows these steps:

**Step 1: Determine Household Composition.** Identify all accounts linked to the billing household. Include all account types per the advisory agreement (individual, joint, IRA, Roth IRA, trust, UGMA/UTMA, entity accounts).

**Step 2: Retrieve Account Valuations.** Pull market values as of the valuation date from the custodian or portfolio management system. Apply any exclusions (cash exclusion, held-away asset inclusion, margin debit netting).

**Step 3: Aggregate Household AUM.** Sum the billable market values across all accounts in the household to determine the household-level AUM for tier determination.

**Step 4: Apply Fee Schedule.** Using the household's assigned fee schedule, calculate the annual fee. For a tiered schedule:

```
Household AUM: $1,800,000
Tier 1: $500,000 * 1.00% = $5,000
Tier 2: $500,000 * 0.80% = $4,000
Tier 3: $800,000 * 0.60% = $4,800
Annual Fee: $13,800
Effective Rate: 0.767%
```

**Step 5: Convert to Billing Period.** Divide the annual fee by the number of billing periods (4 for quarterly, 12 for monthly).

```
Quarterly Fee: $13,800 / 4 = $3,450
```

**Step 6: Apply Overrides and Adjustments.** Check for negotiated rate overrides, minimum fee floors, fee caps, waivers, or credits. Apply in the correct order (typically: calculate standard fee, then apply negotiated rate, then apply minimum, then apply cap, then apply waivers).

**Step 7: Allocate to Accounts.** Distribute the household fee across individual accounts, typically pro-rata by market value:

```
Account A ($900,000 / $1,800,000) = 50% * $3,450 = $1,725.00
Account B ($500,000 / $1,800,000) = 27.78% * $3,450 = $958.33
Account C ($400,000 / $1,800,000) = 22.22% * $3,450 = $766.67
```

**Step 8: Apply Proration.** For any accounts opened or closed mid-period, prorate the allocated fee.

**Step 9: Rounding.** Apply consistent rounding rules (typically round to the nearest cent). Ensure rounding differences are allocated to a designated account (usually the largest) so the sum of account-level fees equals the household fee exactly.

**Step 10: Generate Billing Output.** Produce the custodian debit instruction file or invoice, the billing detail report, and the audit trail record.

**Minimum Fee Application.** Many firms set a minimum quarterly or annual fee (e.g., $250/quarter). If the calculated fee falls below the minimum, the minimum is charged instead. This should be applied at the household level, not the account level.

**Fee Cap Application.** Less common but sometimes offered to attract large accounts. A cap ensures the dollar fee does not exceed a maximum regardless of AUM growth.

**Negotiated Rate Overrides.** Individual clients or households may have rates that differ from the published fee schedule. The billing system must support per-household or per-account rate overrides while maintaining an audit trail of who authorized the deviation and when.

**Rounding Rules.** Define and document the rounding convention. Typical practice rounds each account fee to the nearest cent. Allocate any remainder (positive or negative) from rounding to the largest account in the household.

### 5. Collection Methods

**Direct Debit from Custodian Account.** The most common method for RIAs. The adviser sends fee debit instructions to the custodian (Schwab, Fidelity, Pershing, etc.), and the custodian debits the client's account directly. Requires:
- Written authorization in the advisory agreement or a separate billing authorization form
- Custodian-specific file format (varies by custodian; typically CSV or fixed-width)
- Submission within the custodian's billing window (often the first 10-15 business days of the quarter)
- The custodian sends a statement to the client showing the fee deduction, providing a layer of independent oversight

**Invoice Billing.** The adviser sends an invoice and the client pays by check, wire, or ACH. More common for institutional clients, financial planning fees, or clients who prefer not to authorize direct debits. Increases accounts receivable management burden.

**Split Billing Across Accounts.** When a household has multiple accounts, the fee can be debited from each account in proportion to its share of the household AUM (the most common approach) or debited entirely from one designated account.

**Billing from Specific Accounts.** Some clients designate a specific account for fee payment. Common when clients prefer fees to come from a taxable account (for potential tax deductibility) rather than a retirement account.

**Tax-Advantaged Account Billing Considerations.** Fees can be debited from IRAs and other tax-advantaged accounts, but there are considerations:
- IRA fee debits are not treated as distributions if the fee is for investment management of the IRA assets
- If the fee covers services beyond the IRA (e.g., financial planning for the household), the debit may be treated as a distribution
- Some practitioners recommend paying fees from taxable accounts when possible because the fee payment from an IRA reduces the tax-advantaged balance, whereas paying from a taxable account may be deductible (subject to limitations)
- ERISA plan accounts have additional rules under DOL guidance

**Third-Party Billing.** When the adviser bills through a TAMP (Turnkey Asset Management Platform) or sub-advisory arrangement, the TAMP may handle billing and remit the adviser's share. The adviser must reconcile the revenue received against the expected calculation.

### 6. Billing Exceptions and Adjustments

**Fee Waivers.** Common categories include:
- Employee and employee-family accounts (full or partial waiver)
- Charitable organization accounts (reduced rate or full waiver)
- Pro bono or scholarship accounts
- Accounts below a size threshold during an initial ramp-up period

All waivers should be documented with authorization and expiration (if applicable).

**Negotiated Rates.** Large clients or those with longstanding relationships may receive custom rates below the standard schedule. The billing system must store the effective date, the negotiated schedule, and the approving authority.

**Legacy Fee Schedules.** When a firm updates its published fee schedule, existing clients may be grandfathered on the old schedule. The billing system must support multiple active fee schedules concurrently. Over time, legacy schedules create operational complexity and should be periodically reviewed for consolidation.

**Retroactive Adjustments.** Occur when an error is discovered after billing has been processed. The adjustment should be applied in the next billing cycle (credit or additional debit) with clear documentation of the original error, the corrected calculation, and the net adjustment.

**Billing Disputes.** When a client disputes a fee, the process should include:
1. Immediate acknowledgment of the dispute
2. Detailed recalculation and documentation
3. Resolution within a defined timeframe (e.g., 30 days)
4. If the client is correct, issue a credit or refund
5. Maintain a dispute log for compliance review

**Refunds for Terminated Accounts.** For advance-billed accounts, calculate the unearned portion of the fee from the termination date through the end of the billing period and issue a refund. The advisory agreement should specify the refund methodology.

```
Refund = Quarterly Fee * (Remaining Days / Total Days in Quarter)
```

**Fee Reversals.** Full reversal of a fee debit at the custodian level. Typically used when a billing error is caught within the custodian's reversal window (often same-day or next-day). After the reversal window, the correction must be handled as a retroactive adjustment.

### 7. Revenue Recognition

**GAAP Treatment: Advance Billing.** When fees are billed at the start of a quarter, the firm recognizes a liability (deferred revenue or unearned fees) at the billing date. Revenue is then recognized ratably over the service period (the quarter). At the end of the quarter, all deferred revenue for that period has been earned and recognized.

**GAAP Treatment: Arrears Billing.** Revenue accrues over the service period. At the end of each month within the quarter, the firm recognizes one-third of the estimated quarterly fee as accrued revenue. When the fee is billed and collected at quarter-end, the accrual is reversed and replaced with recognized revenue.

**Revenue Per Client Metrics.** Key metrics include:
- Average revenue per household
- Average revenue per account
- Revenue per advisor
- Effective fee rate (total fees / total AUM) as a blended measure

**Revenue Concentration Analysis.** Regulators and business prudence demand awareness of concentration risk. If a single client or small group of clients represents a disproportionate share of revenue, the firm faces business risk. Common thresholds to monitor: no single household should exceed 5-10% of total revenue.

**Revenue Forecasting.** Forecast advisory revenue using:
- Current AUM multiplied by the blended effective fee rate
- Adjust for expected market appreciation or depreciation
- Adjust for expected net new assets (organic growth) or attrition
- Adjust for known fee schedule changes or renegotiations
- Sensitivity analysis across bull, base, and bear market scenarios

### 8. Compliance and Disclosure

**ADV Part 2A (Brochure) Fee Disclosure.** Item 5 of Form ADV Part 2A requires clear disclosure of:
- Fee schedules and how fees are calculated
- Whether fees are negotiable
- Billing frequency and collection method
- Whether fees are billed in advance or arrears
- Refund policy for terminated accounts
- Other costs clients may bear (custodian transaction fees, fund expenses, etc.)

The disclosure must be sufficiently detailed that a client can understand the total cost of the advisory relationship.

**Fee-on-Fee Issues.** When an adviser charges an AUM-based fee on a portfolio that includes mutual funds or ETFs, the client pays both the advisory fee and the underlying fund expense ratio. This "fee on a fee" must be disclosed. Some advisers offset the fund expenses against the advisory fee or use the lowest-cost share classes available to mitigate this concern.

**Total Cost of Ownership Disclosure.** Best practice (and increasingly expected by regulators) is to present the client with a comprehensive view of all costs: advisory fees, fund expenses, custodian fees, transaction costs, and any other charges. This aligns with the SEC's guidance on adviser fiduciary duty.

**Regulation Best Interest (Reg BI) Cost Considerations.** For dual-registrant firms, Reg BI requires disclosure of material fees and costs and their impact on the client's investment. The cost comparison between advisory and brokerage accounts is a key element.

**ERISA 408(b)(2) Fee Disclosure.** For advisers serving retirement plans, ERISA Section 408(b)(2) requires detailed disclosure of all direct and indirect compensation received in connection with plan services. The disclosure must be provided before the engagement begins and updated within 60 days of any change.

**Fee Reasonableness Documentation.** Advisers should maintain documentation supporting the reasonableness of their fees. This includes periodic benchmarking against industry surveys (e.g., the annual RIA benchmarking studies from Schwab, Fidelity, or InvestmentNews), documentation of the services provided for the fee, and consideration of the client's total cost.

### 9. Billing System Architecture

**Core Components:**

- **Fee Schedule Repository.** A database of all fee schedules (standard and negotiated), including effective dates, tier structures, and associated metadata. Must support versioning so historical calculations can be recreated.

- **Account/Household Master.** Links accounts to billing households, assigns fee schedules, stores billing preferences (collection method, billing account designation, proration rules).

- **Valuation Engine.** Retrieves or calculates account market values as of the billing date. Sources include custodian position files, portfolio management systems, and manual entries for held-away assets.

- **Calculation Engine.** The core logic that executes the ten-step process described in Section 4. Must handle all fee schedule types, proration, overrides, minimums, caps, and rounding.

- **Custodian Debit Instruction Generator.** Produces the custodian-specific file format for fee debits. Each custodian (Schwab, Fidelity, Pershing, TD Ameritrade legacy, etc.) has its own format requirements, submission deadlines, and reversal procedures.

- **Invoice Generator.** For clients billed by invoice, produces statements with fee detail.

**Integration Points:**

- **Portfolio Management System (PMS).** The billing system pulls valuations and account structure from the PMS. In some platforms (e.g., Orion, Black Diamond, Tamarac), the billing engine is integrated into the PMS.
- **Custodian.** Bidirectional: the billing system sends debit instructions to the custodian and receives confirmation (or rejection) files back.
- **CRM.** Fee schedule assignments and negotiated rates may be managed in the CRM and synchronized to the billing system.
- **Accounting System.** Billing output feeds revenue entries in the firm's general ledger.

**Billing Preview and Approval Workflow.**
1. The billing engine runs in preview mode, producing a billing preview report.
2. Operations staff review the preview for anomalies (unusually large fees, negative fees, zero-dollar fees, fees that deviate significantly from the prior period).
3. Exceptions are investigated and resolved.
4. An authorized person approves the billing run.
5. The engine generates the final debit instructions or invoices.
6. Instructions are submitted to custodians.

**Audit Trail.** Every billing run must produce a complete audit trail including:
- Valuation date and source
- Fee schedule applied (with version identifier)
- Household AUM and per-account AUM
- Step-by-step calculation detail
- Any overrides, waivers, or adjustments applied
- The identity of the person who approved the billing run
- Timestamp of submission to the custodian

**Billing Reports.** Standard reports include:
- Billing summary by household (fee, effective rate, AUM)
- Billing detail by account
- Period-over-period comparison (fee change from prior quarter)
- Exception report (new accounts, terminated accounts, large variances)
- Revenue summary by advisor, team, or branch
- Accounts receivable aging (for invoice-billed clients)

## Worked Examples

See [references/examples.md](references/examples.md) for three end-to-end worked examples — a quarterly tiered-fee calculation for a five-account household, mid-quarter proration for contributions/transfers/terminations, and a spreadsheet-to-automated billing migration. Load it when the user needs a full numerical walkthrough.

## Common Pitfalls

- **Confusing tiered and breakpoint pricing.** A tiered schedule charges each dollar at the rate for its tier. A breakpoint schedule charges the entire balance at the rate for the highest tier reached. Mixing these up leads to significant billing errors, especially for large accounts.
- **Failing to prorate for mid-period events.** Not adjusting fees for material contributions, withdrawals, or account openings/closings results in overbilling or underbilling and invites client complaints.
- **Ignoring rounding allocation.** When per-account fees are rounded independently, the sum may not equal the household fee. Without a systematic rounding allocation, small discrepancies accumulate and create reconciliation headaches.
- **Billing retirement accounts for non-retirement services.** Debiting an IRA for advisory fees that cover financial planning or services unrelated to the IRA assets can trigger a taxable distribution. Always confirm that fees debited from tax-advantaged accounts correspond to services for those accounts.
- **Neglecting to update negotiated rates.** When a fee schedule is updated but negotiated rate clients are forgotten, those clients may continue paying outdated rates indefinitely. Maintain a review cadence for all non-standard arrangements.
- **Inadequate disclosure of fee-on-fee costs.** Failing to disclose that clients pay both the advisory fee and underlying fund expenses is a recurring SEC examination finding. Ensure ADV Part 2A and client communications address total cost clearly.
- **Missing the custodian billing window.** Each custodian has a defined window for accepting fee debit instructions. Missing the window delays fee collection by an entire quarter and disrupts cash flow.
- **Not reconciling custodian confirmations.** After submitting debit instructions, the custodian returns a confirmation file indicating which debits were processed and which were rejected (insufficient funds, account closed, etc.). Failing to review this file means rejected debits go uncollected.
- **Advance-billing refund errors on termination.** When an advance-billed account terminates mid-quarter, the firm owes a prorated refund. Incorrect day-count calculations or failing to issue the refund entirely creates compliance risk and client ill will.
- **Overcomplicating household definitions.** Overly broad household aggregation (e.g., including extended family members who are not part of the advisory relationship) can inflate tier benefits. Overly narrow definitions deprive clients of legitimate aggregation. The definition must match the advisory agreement.
- **Lack of billing audit trail.** Without a detailed record of every calculation input and output, the firm cannot defend its billing in the event of a client dispute or regulatory examination.
- **Revenue recognition timing errors.** Recognizing advance-billed fees as revenue immediately rather than deferring and recognizing ratably overstates revenue in the billing period and understates it in subsequent periods.

## Cross-References

- **fee-disclosure** (compliance plugin) — Detailed requirements for fee disclosure in client-facing documents and regulatory filings.
- **portfolio-management-systems** (advisory-practice plugin) — Integration between billing engines and PMS platforms for valuation and account data.
- **advisor-dashboards** (advisory-practice plugin) — Revenue metrics, billing status, and fee analytics displayed on advisor-facing dashboards.
- **client-reporting-delivery** (advisory-practice plugin) — Inclusion of fee summaries and performance-net-of-fee figures in client reports.
- **investment-policy** (wealth-management plugin) — Fee schedule terms as specified in the investment policy statement or advisory agreement.
- **reg-bi** (compliance plugin) — Regulation Best Interest cost disclosure obligations for dual-registrant firms.
- **fiduciary-standards** (compliance plugin) — Fiduciary duty to charge reasonable fees and act in the client's best interest regarding cost.
- **tax-efficiency** (wealth-management plugin) — Tax implications of fee payment source (taxable vs. tax-advantaged accounts) and deductibility considerations.
- **performance-reporting** (wealth-management plugin) — Gross-of-fee vs. net-of-fee performance calculation and the role of accurate fee data.

### Referencia: references/examples.md

# Worked Examples — Fee Billing

## Table of Contents

1. [Quarterly Fee Calculation for a Household with Tiered Pricing](#example-1-quarterly-fee-calculation-for-a-household-with-tiered-pricing) — five-account household, tier math, pro-rata allocation, rounding allocation, split debit/invoice output
2. [Mid-Quarter Account Events — Transfers, Contributions, and Terminations](#example-2-mid-quarter-account-events--transfers-contributions-and-terminations) — proration math for advance billing with next-cycle adjustments
3. [Billing System Migration from Spreadsheet to Automated Platform](#example-3-billing-system-migration-from-spreadsheet-to-automated-platform) — five-phase migration with parallel run and cutover controls

### Example 1: Quarterly Fee Calculation for a Household with Tiered Pricing

**Scenario:** The Harrison household has five accounts under a tiered fee schedule. The firm bills quarterly in advance based on prior quarter-end values. The fee schedule is:

| Tier | AUM Range | Annual Rate |
|------|-----------|-------------|
| 1 | First $500,000 | 1.00% |
| 2 | Next $500,000 | 0.85% |
| 3 | Next $2,000,000 | 0.65% |
| 4 | Over $3,000,000 | 0.50% |

Account valuations as of the prior quarter-end (December 31):

| Account | Type | Market Value |
|---------|------|-------------|
| Harrison Joint | Taxable | $1,200,000 |
| Harrison IRA (Mr.) | IRA | $650,000 |
| Harrison IRA (Mrs.) | IRA | $480,000 |
| Harrison Trust | Irrevocable Trust | $850,000 |
| Harrison 529 | 529 Plan | $120,000 |

**Design Considerations:**
- The 529 plan is held away at a separate custodian. The advisory agreement specifies it is included in billable AUM for tier determination but fees on the 529 are billed by invoice, not direct debit.
- The household prefers that direct-debit fees come from the taxable joint account, not the IRAs or trust.
- The firm applies rounding to the nearest cent and allocates rounding differences to the largest account.

**Analysis:**

Step 1 — Aggregate household AUM:
$1,200,000 + $650,000 + $480,000 + $850,000 + $120,000 = $3,300,000

Step 2 — Apply tiered schedule:
- Tier 1: $500,000 at 1.00% = $5,000.00
- Tier 2: $500,000 at 0.85% = $4,250.00
- Tier 3: $2,000,000 at 0.65% = $13,000.00
- Tier 4: $300,000 at 0.50% = $1,500.00
- Annual fee: $23,750.00
- Effective rate: $23,750 / $3,300,000 = 0.7197%

Step 3 — Quarterly fee:
$23,750.00 / 4 = $5,937.50

Step 4 — Allocate to accounts pro rata by market value:

| Account | Market Value | Weight | Allocated Fee |
|---------|-------------|--------|---------------|
| Harrison Joint | $1,200,000 | 36.3636% | $2,159.09 |
| Harrison IRA (Mr.) | $650,000 | 19.6970% | $1,170.01 |
| Harrison IRA (Mrs.) | $480,000 | 14.5455% | $863.64 |
| Harrison Trust | $850,000 | 25.7576% | $1,529.36 |
| Harrison 529 | $120,000 | 3.6364% | $215.91 |
| **Total** | **$3,300,000** | **100%** | **$5,938.01** |

The raw allocation sums to $5,938.01 due to rounding, which is $0.51 over the $5,937.50 quarterly fee. The rounding adjustment of -$0.51 is applied to the largest account (Harrison Joint), reducing its fee to $2,158.58.

Final billing output:
- Direct debit from Harrison Joint account: $5,721.59 (covering Joint $2,158.58 + IRA Mr. $1,170.01 + IRA Mrs. $863.64 + Trust $1,529.36)
- Invoice to Harrison for 529 plan: $215.91

Note: Because the household prefers all direct-debit fees to come from the joint account, the custodian debit instruction is a single debit of $5,721.59 from the joint account. However, the billing detail report still shows the per-account allocation for transparency and performance reporting accuracy.

### Example 2: Mid-Quarter Account Events — Transfers, Contributions, and Terminations

**Scenario:** The Martinez household bills quarterly in advance (Q2: April 1 through June 30, 91 days). At the start of Q2, the household has two accounts:

| Account | Market Value (Mar 31) | Allocated Q2 Fee |
|---------|----------------------|-----------------|
| Martinez Taxable | $800,000 | $1,000.00 |
| Martinez IRA | $400,000 | $500.00 |
| **Total** | **$1,200,000** | **$1,500.00** |

During Q2, three events occur:
1. On April 20 (day 20 of 91), a $200,000 contribution is made to the taxable account.
2. On May 15 (day 45 of 91), a new Roth IRA is opened with a $50,000 transfer from the taxable account.
3. On June 10 (day 71 of 91), the IRA is terminated and the balance is rolled over to another firm.

**Design Considerations:**
- The firm's policy is to prorate for contributions over $25,000 and for all account openings and closings.
- Since billing is in advance, the Q2 fee was already debited on April 1. Adjustments will appear on the Q3 billing run.
- Internal transfers (item 2) should be revenue-neutral at the household level.

**Analysis:**

Event 1 — $200,000 contribution on April 20:
Additional billable days: 71 days remaining out of 91 (April 20 through June 30).
Additional annual fee on $200,000 at the household's effective rate (1.00% flat in this case): $2,000.
Additional quarterly fee: $2,000 / 4 = $500.
Prorated additional fee: $500 * (71 / 91) = $390.11.
This will be charged as an adjustment on the Q3 billing run.

Event 2 — Roth IRA opened May 15 via internal transfer:
The $50,000 moves from the taxable account to the new Roth IRA. Since this is an intra-household transfer, the household AUM does not change and no fee adjustment is needed. The per-account allocation will be updated for the new account going forward, but the household-level fee remains the same.

Event 3 — IRA terminated June 10:
The IRA was billed $500 for the full quarter. Days active: 71 out of 91 (April 1 through June 10).
Days unused: 20 out of 91.
Refund: $500 * (20 / 91) = $109.89.
This refund is applied as a credit on the Q3 billing run.

Net Q3 adjustment for the Martinez household:
- Additional charge for contribution: +$390.11
- Refund for early termination: -$109.89
- Net adjustment: +$280.22 added to the Q3 fee

The billing detail report for Q3 will show the standard Q3 fee plus a line item for the Q2 adjustment with a reference to each underlying event.

### Example 3: Billing System Migration from Spreadsheet to Automated Platform

**Scenario:** A 15-advisor RIA managing $2.1 billion across 1,800 households currently calculates fees using a series of Excel workbooks maintained by two operations staff. The firm is migrating to an integrated billing module within their portfolio management system. The spreadsheet system has worked for years but is error-prone, poorly documented, and dependent on key personnel.

**Design Considerations:**
- The firm has 14 distinct fee schedules (including 6 legacy schedules that apply to fewer than 50 households each).
- Approximately 120 households have negotiated rates that differ from the standard schedule.
- The firm bills quarterly in advance, debiting from custodian accounts at Schwab and Fidelity.
- The migration must not disrupt the next quarterly billing cycle.

**Analysis:**

Phase 1 — Data Extraction and Documentation (Weeks 1-3):
- Export all fee schedules from the existing spreadsheets into a structured format (schedule name, tier breakpoints, rates, effective date).
- Document every negotiated rate override with the associated household, effective date, and authorizing advisor.
- Catalog all billing exceptions: waivers, caps, minimum overrides, split-billing arrangements, invoice-billed accounts.
- Extract two years of historical billing data (household, account, AUM, fee charged, period) for parallel-run comparison.

Phase 2 — System Configuration (Weeks 3-6):
- Configure all 14 fee schedules in the new billing module with correct tier structures and effective dates.
- Enter negotiated rate overrides per household.
- Configure billing preferences per household: collection method, billing account designation, proration rules.
- Set up custodian debit file formats for Schwab and Fidelity.
- Configure the approval workflow (preview, review, approve, submit).

Phase 3 — Parallel Run (Weeks 6-9, coinciding with one billing cycle):
- Run the new system in parallel with the spreadsheet process for one full quarterly cycle.
- Compare results at the household level. Accept a tolerance of $0.01 per household for rounding differences.
- Investigate and resolve every variance exceeding the tolerance.
- Common variance sources: different rounding methods, different day-count conventions for proration, fee schedule data entry errors, missing negotiated rate overrides.

Phase 4 — Cutover (Week 10):
- After parallel-run sign-off, the new system becomes the system of record.
- The spreadsheet process is retained as a reference but is no longer used for production billing.
- First live billing cycle is run with enhanced review (every household is spot-checked, not just exceptions).

Phase 5 — Post-Migration Monitoring (Weeks 10-22, two billing cycles):
- Heightened review of billing output for two additional cycles.
- Monitor client inquiries or complaints related to fee amounts.
- Validate that custodian debit files are accepted without error.
- Confirm revenue recognition entries in the accounting system match prior methodology.

Key success metrics:
- Zero missed billing cycles during migration.
- Variance rate below 0.5% of households in the first live cycle.
- Reduction in billing processing time from approximately 40 person-hours per quarter to under 8 person-hours.
- Elimination of single-point-of-failure key-person risk.


---

## SKILL: fee-disclosure

- Fuente: `JoelLewis/finance_skills` → `plugins/compliance/skills/fee-disclosure` (MIT)
- Cuándo usarla: Evaluate whether the substance of fee and cost disclosures is complete, accurate, and not misleading across advisory, brokerage, fund, and retirement plan contexts. Use when the user asks whether Form ADV Item 5 fee content is adequate, prospectus fee table format, Reg BI cost disclosure content, 12b-1 fee transparency, revenue sharing arrangements, wrap fee program cost-effectiveness, or ERISA 408(b)(2)/404a-5 fee disclosure content. Also trigger when users mention 'hidden fees', 'total cost to the client', 'are we disclosing all layers of fees', 'expense ratio comparison', 'fee billing in advance vs arrears', 'share class selection', or 'indirect compensation'. (For which disclosure documents must exist and when they are delivered, use client-disclosures.)

# Fee Disclosure

Regulatory status current as of June 2026 — verify effective dates, dollar thresholds, and pending rulemakings against current SEC/FINRA/FinCEN sources before advising.

## Core Concepts

### Form ADV Part 2A — Item 5 (Fees and Compensation)
RIAs must disclose in their firm brochure:
- **Fee schedule** — how fees are calculated (asset-based, fixed, hourly, performance-based), fee rates and tiers, minimum account sizes
- **Billing method** — frequency (monthly, quarterly), in advance or arrears, pro-ration for partial periods
- **Other fees and expenses** — custodian fees, fund expense ratios, transaction costs, wire fees, and any other costs the client will bear in addition to the advisory fee
- **Compensation for sales of securities** — if the adviser or its supervised persons receive commissions, 12b-1 fees, or other sales-based compensation, this must be disclosed with a description of the conflict
- **Refund policy** — how prepaid fees are refunded if the relationship terminates mid-period

The disclosure must be "full and fair" and not misleading. The SEC has brought enforcement actions for advisers who disclosed fee schedules but obscured the total cost to clients by omitting indirect compensation or failing to describe how fund-level fees compound on top of advisory fees.

### Form CRS Fee Disclosure
The "What are your fees?" section of Form CRS must include:
- Principal fees and costs for the firm's services
- A description of other fees and costs the client may pay (transaction, custodian, fund expenses)
- A statement that the client will pay fees and costs whether or not they make or lose money
- Conversation starters: "Help me understand how these fees and costs might affect my investments. If I give you $10,000 to invest, how much will go to fees and costs, and how much will be invested for me?"

Form CRS is limited to 2 pages (4 for dual registrants), so fee disclosure is necessarily summarized. It must direct clients to the ADV Part 2A for more detailed information.

### Reg BI Disclosure Obligation — Costs
Reg BI requires broker-dealers to disclose material facts about costs and fees before or at the time of a recommendation:
- All fees and costs that apply to the customer's transactions, holdings, and accounts
- Material limitations on recommendations (e.g., proprietary products only, limited product shelf)
- Compensation the BD and representative receive, including from third parties

The SEC has emphasized that the disclosure must be specific enough to allow the customer to understand the total cost of the recommendation and compare it to alternatives. Vague references to "standard industry fees" are insufficient.

### Prospectus Fee Tables
SEC rules require a standardized fee table in mutual fund and ETF prospectuses:

**Shareholder Fees (paid directly from the investor's investment):**
- Maximum sales charge (load) on purchases
- Maximum deferred sales charge (CDSC)
- Redemption fees
- Exchange fees
- Account fees

**Annual Fund Operating Expenses (deducted from fund assets):**
- Management fees
- Distribution (12b-1) fees
- Other expenses
- Acquired fund fees and expenses (for fund-of-funds)
- Total annual fund operating expenses
- Fee waiver/expense reimbursement (if applicable)
- Net expenses after waiver

**Expense Example:** A standardized illustration showing the dollar cost of investing $10,000 over 1, 3, 5, and 10 years, assuming a 5% annual return and redemption at the end of each period. This enables cross-fund comparison regardless of marketing language.

### 12b-1 Fees
Named after SEC Rule 12b-1, these are annual distribution and marketing fees charged to fund assets:
- **Maximum permitted:** 0.75% for distribution, plus 0.25% for shareholder services (total 1.00%)
- **Disclosure:** Must appear in the prospectus fee table and in the fund's Statement of Additional Information
- **Conflict:** 12b-1 fees create an incentive for advisers and brokers to recommend higher-cost share classes. The SEC and FINRA have brought numerous enforcement actions for recommending share classes with 12b-1 fees when lower-cost share classes of the same fund were available to the client.
- **Share class selection:** Firms must have policies to ensure clients are placed in the most appropriate share class. The SEC's Share Class Selection Disclosure Initiative (2018) resulted in over $139 million in disgorgement from advisers who failed to disclose 12b-1 revenue.

### Revenue Sharing and Shelf-Space Arrangements
Fund companies may pay broker-dealers or advisory platforms for preferred placement, marketing support, or inclusion on recommended lists:
- **Revenue sharing** — payments above standard 12b-1 fees, often basis points on assets held on the platform
- **Shelf space** — payments for inclusion on "preferred" or "recommended" fund lists
- **Sub-TA fees** — payments for sub-transfer agency and recordkeeping services, which may exceed the actual cost of providing those services

Disclosure requirements: Both FINRA and the SEC expect clear disclosure of revenue sharing arrangements. Failure to disclose that a firm receives additional compensation for recommending specific funds is a serious conflict-of-interest violation. The SEC has brought enforcement actions where firms described fund selection as "objective" while receiving undisclosed revenue sharing.

### Wrap Fee Programs
Wrap fee programs bundle advisory, brokerage, custody, and other services into a single asset-based fee:
- **Form ADV Part 2A Appendix 1** — wrap fee sponsors must deliver a wrap fee brochure disclosing the services included, the total fee, and a comparison to unbundled pricing
- **Cost-effectiveness analysis** — wrap fees benefit active traders (who would otherwise pay per-trade commissions) but penalize buy-and-hold investors. Firms must evaluate whether wrap is cost-effective for each client.
- **Trading away** — when a wrap program adviser executes trades through a broker-dealer other than the wrap sponsor, the client may pay additional transaction costs. These must be disclosed.
- **Reverse churning** — the wrap equivalent of churning: charging an ongoing asset-based fee for an account with little trading activity. FINRA and the SEC have flagged this as a concern.

### ERISA Fee Disclosure
**DOL Section 408(b)(2) disclosure** — retirement plan service providers must disclose to plan fiduciaries:
- A description of services
- Whether the provider will act as an ERISA fiduciary
- All direct and indirect compensation (including revenue sharing, 12b-1 fees, float, sub-TA fees)
- Compensation paid among related parties

**DOL Section 404a-5 disclosure** — plan administrators must provide participants with:
- Plan-level information (general plan administration and individual expenses that may be charged)
- Investment-level information (performance, benchmark, fees and expenses for each investment option)
- Quarterly statements showing actual fees and expenses charged to the participant's account

### Hidden Fees and All-In Cost
Beyond explicit fees, clients bear costs that may not be separately disclosed:
- **Trading costs** — bid-ask spreads, market impact, commission-equivalent costs in "commission-free" accounts
- **Soft dollars** — research and services paid for with client brokerage, under Section 28(e) safe harbor
- **Cash sweep rates** — below-market interest rates on uninvested cash, where the spread constitutes implicit compensation
- **Securities lending revenue** — funds may retain a portion of securities lending income rather than passing it to shareholders
- **Foreign exchange markups** — spreads on currency conversions for international securities

Comprehensive fee analysis requires looking beyond the stated fee schedule to capture total cost of ownership.

## Worked Examples

### Example 1: RIA failing to disclose 12b-1 fee revenue
**Scenario:** An RIA charges clients a 1% annual advisory fee. The firm also recommends mutual funds that pay 0.25% 12b-1 fees to the adviser. The ADV Part 2A describes the 1% advisory fee in detail but mentions 12b-1 fees only in a general statement: "Some funds we recommend may charge distribution fees." The firm does not disclose that it receives these 12b-1 payments.
**Compliance Issues:** ADV Part 2A Item 5 requires disclosure of compensation received from third parties, including 12b-1 fees. The failure to disclose that the firm receives this revenue — and that it creates a conflict (incentive to recommend funds with 12b-1 fees over those without) — violates the fiduciary duty of loyalty. Total client cost is actually 1.25%, not 1%.
**Analysis:** This scenario matches the pattern targeted by the SEC's Share Class Selection Disclosure Initiative. The firm must: (1) specifically disclose that it receives 12b-1 fee revenue, (2) quantify or estimate the amount, (3) explain the conflict it creates, (4) evaluate whether lower-cost share classes are available, and (5) document why the recommended share class is in the client's best interest. If an institutional share class without 12b-1 fees is available and the client qualifies, recommending the 12b-1 class without disclosure is a violation.

### Example 2: Wrap fee program cost-effectiveness
**Scenario:** A BD places a 68-year-old retired buy-and-hold client in a wrap fee program charging 1.5% annually. The client's $800,000 account holds 5 ETFs and rebalances once per year. An unbundled account would cost approximately 0.3% (advisory fee) plus ~$50 in annual trading costs.
**Compliance Issues:** Potential reverse churning. The wrap fee ($12,000/year) is dramatically higher than unbundled cost (~$2,450/year) for a client whose low trading activity does not benefit from the wrap structure. The firm's wrap fee brochure must assess cost-effectiveness, and both FINRA and Reg BI require that the account type recommendation serve the client's interest.
**Analysis:** The firm should have a periodic cost-effectiveness review process for wrap accounts. A client paying $9,550 more per year for a structure designed for active trading is not receiving corresponding value. Under Reg BI's Care Obligation, the BD must consider whether this account type is in the client's best interest. Under IA fiduciary duty (if the firm is dually registered), the ongoing fee without corresponding service may violate the duty of care.

### Example 3: Inadequate 401(k) participant fee disclosure
**Scenario:** A 401(k) plan with $15M in assets provides participants with an annual fee disclosure that lists fund names and ticker symbols but does not include expense ratios, benchmark performance, or a statement of actual fees charged to each participant's account. Quarterly statements show account balances but not fee deductions.
**Compliance Issues:** DOL Section 404a-5 violation. The regulation requires investment-level fee and performance information in a specific format (chart/table), including total annual operating expenses as both a percentage and dollar amount per $1,000 invested. Quarterly statements must show actual dollar amounts of fees and expenses charged.
**Analysis:** The plan fiduciary (and its service provider under 408(b)(2)) must provide compliant disclosures. Non-compliant fee disclosure exposes the plan fiduciary to liability and undermines participants' ability to make informed investment decisions. The fix requires producing the DOL-prescribed comparative chart with expense ratios, benchmark comparisons, and website URLs for additional information, plus detailed fee breakdowns on quarterly statements.

## Common Pitfalls
- Disclosing the advisory fee but omitting indirect compensation (12b-1 fees, revenue sharing, sub-TA fees)
- Using boilerplate language about fund fees without disclosing the firm's financial interest in specific share classes
- Not evaluating wrap fee cost-effectiveness for each client based on actual trading patterns
- Failing to update fee disclosures when fee schedules change or new indirect compensation arrangements are established
- Describing fund selection as "objective" or "independent" while receiving revenue sharing from recommended funds
- Not providing the standardized prospectus fee table format when required
- ERISA plans failing to provide participant-level fee disclosure in the DOL-prescribed format
- Overlooking cash sweep rate differentials as a form of indirect compensation
- Not distinguishing between gross and net expense ratios in fund comparisons
- Assuming "commission-free" means "cost-free" — bid-ask spreads and payment for order flow still represent costs

## Cross-References
- **fund-vehicles** (wealth-management plugin): Fund mechanics, expense ratios, share classes — the product knowledge underlying fee disclosure
- **conflicts-of-interest** (compliance plugin): Revenue sharing, 12b-1 fees, and differential compensation are core conflicts requiring disclosure
- **reg-bi** (compliance plugin): Reg BI's Disclosure Obligation specifically addresses fees and costs
- **client-disclosures** (compliance plugin): Form ADV and Form CRS are the delivery vehicles for fee disclosure
- **fiduciary-standards** (compliance plugin): Fee transparency is a core fiduciary obligation
- **investment-policy** (wealth-management plugin): IPS fee assumptions must reflect actual total cost


---

## SKILL: finance-psychology

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/finance-psychology` (MIT)
- Cuándo usarla: Recognize and mitigate cognitive biases that impair financial decisions, and coach clients toward values-driven financial lives. Use when the user asks about behavioral finance, money psychology, loss aversion, overconfidence, herd behavior, or emotional investing. Also trigger when users mention 'why do I panic sell', 'money fights with my spouse', 'I can never save enough', 'fear of investing', 'lifestyle creep', 'keeping up with the Joneses', 'Rich Life', 'money scripts', or ask how emotions affect financial decisions.

# Finance Psychology — Behavioral Finance & Money Coaching

Personal finance is mostly psychology, not mechanics. Until a client understands *why* they behave the way they do with money, and *what* they want money to do for them, spreadsheet optimization will not stick. This skill covers the coaching principles, client archetypes, cognitive biases, and conversation frameworks for behavioral money work.

## Core Concepts

### Foundational Principles

Short principles that should inform every coaching interaction:

- **No one is crazy.** Financial behavior that looks irrational usually made sense in the lived experience that produced it. Ask "what experience taught you this was the right way to handle money?" before trying to change the behavior.
- **Luck and risk are real.** Judge decisions by process, not outcome. This reduces both the overconfidence that follows wins and the shame that follows losses.
- **Define "enough" explicitly.** Social comparison keeps the goalpost moving; no number feels sufficient if the reference point keeps shifting. Help clients name "enough" as a life, in writing — and never risk reputation, freedom, family, or happiness for more.
- **Compounding requires time, not heroics.** Years invested matter more than return rate. Anything that interrupts compounding — panic selling, lifestyle inflation that eliminates savings, blow-up risk — is more destructive than earning merely average returns.
- **Getting wealthy and staying wealthy are different skills.** Growth requires optimism and risk-taking; preservation requires humility, margin of safety, and liquidity. Coach risk-takers on preservation and natural savers on deployment.
- **Freedom is the underlying goal.** When a client names a number, probe for the freedom underneath ("what would that let you *do*?") — it is often achievable earlier than the number.
- **Wealth is what you don't see.** Visible spending is wealth already converted to consumption. Rich is current income; wealth is future optionality.
- **Reasonable beats rational.** A slightly suboptimal plan the client can hold through a 35% drawdown beats an optimal plan they abandon. Ask: "If this dropped 35% next month, would you change anything?" If the answer is sell, de-risk now.

(Sources: Housel, Kahneman & Tversky, Thaler & Sunstein, Sethi — see Key Sources.)

### Invisible Money Scripts
Unconscious beliefs about money absorbed from family and early experience: "we can't afford that" (scarcity even amid abundance), "rich people are greedy" (self-sabotage), "investing is gambling" (cash paralysis), "don't talk about money" (can't negotiate or discuss finances with a partner).

**Identification:** Ask "What did your parents say about money when you were growing up? What did they *not* say?" Listen for reflexive phrases ("I probably shouldn't spend that much") — scripts operating in real time.

**Coaching approach:** Name the script explicitly. Frame it as an inherited survival strategy that made sense in its original context; the client gets to choose which scripts to keep.

### The Four Money Types
Most clients blend archetypes, but one usually dominates. Identify it to tailor the coaching approach.

**The Avoider** — deflects money conversations, doesn't know balances, defers decisions to a partner; rooted in anxiety.
*Coaching moves:* Start small and concrete (log into one account, not a full plan). Celebrate engagement, not optimization. Automate heavily so the system works when they aren't looking.

**The Optimizer** — tracks every dollar, comparison-shops for hours, but often cannot spend on things that bring joy; optimizes the system at the expense of the life it serves.
*Coaching moves:* Zoom out: "Your savings rate is 38% — what is that saving *for*?" Challenge them to spend *more* on their highest-value categories. Redirect optimization energy from cost-minimization to life-design, and from trivial questions to the big levers (below).

**The Worrier** — plays defense, sees threats everywhere; anxiety does not match objectively healthy finances.
*Coaching moves:* Give data and structure: concrete projections under pessimistic/base/optimistic scenarios. Build generous margins of safety — not because the math requires it, but because it buys emotional permission to live. Name the feelings-vs-reality gap compassionately.

**The Dreamer** — magical thinking; big plans, no mechanism; often insulated by a partner or avoidance.
*Coaching moves:* Don't crush the vision — connect it to a mechanism: "The restaurant in five years — what does it cost, what's the monthly saving, what's the first step this week?"

### Spending as Values Expression
Identify the few categories where spending produces disproportionate joy (Sethi calls these "Money Dials"): ask "What do you spend on that makes you irrationally happy?" and "What do you spend on that you genuinely don't care about?" Then spend deliberately more on the first and cut mercilessly on the second. This replaces moralistic "good/bad spending" with a personalized values test: not "is this too much?" but "does this reflect what you actually value?"

### Big Levers vs Trivial Questions
Most people obsess over trivial questions (cancel a $12 subscription?) while ignoring the decisions worth tens of thousands: asset allocation and fees, savings rate, debt sequencing, career and salary negotiation, insurance, tax-advantaged account order (employer match → Roth IRA → max 401k → HSA). When a client fixates on a small optimization, redirect to the unaddressed big levers — small optimizations are often avoidance of the hard, high-stakes questions.

### Start at 85%, Then Iterate
A plan that is 85% optimal and actually implemented beats a perfect plan stalled in research. Four index funds are functionally identical; pick one and start. Automation and consistency beat precision.

### The Four-Bucket Spending Plan
A values-aligned alternative to a restrictive budget (the word "budget" itself triggers scarcity for many clients):
- **Fixed costs:** 50-60% of take-home
- **Investments:** 10%+
- **Savings:** 5-10%
- **Guilt-free spending:** 20-35% — *meant* to be spent, because the important categories are already funded

The guilt-free bucket flips the emotional valence of discretionary spending and breaks the guilt → deprivation → binge cycle. This is deliberate, constructive mental accounting.

### Automation as Behavioral Architecture
Remove willpower from the loop: paycheck → pre-tax retirement contribution → automatic transfers to IRA/savings/investments → auto-paid bills → remainder is guilt-free. Automation leverages status quo bias, cuts decision fatigue, and reduces money management to ~90 minutes a month.

### Cognitive Biases in Financial Decisions

| Bias | Typical damage | Primary mitigations |
|------|----------------|---------------------|
| Loss aversion (losses hurt ~2x gains; Kahneman & Tversky 1979) | Disposition effect: sell winners early, hold losers hoping to break even | Pre-commit exit criteria at purchase; rules-based rebalancing; "would I buy this today at this price?"; purchase price is a sunk cost |
| Overconfidence | Overtrading, concentration, underestimating tail risk | Track prediction hit rate; base rates (~10-15% of active pickers beat the index over 10 years); accept that average returns sustained are excellent |
| Anchoring | Fixating on purchase price or 52-week high | Value on current fundamentals; multiple independent valuation methods |
| Recency bias | Performance chasing; panic selling; extrapolating trends | Long-term return distributions; 20%+ drawdowns recur every ~4-6 years — the price of admission, not an anomaly; DCA and systematic rebalancing |
| Herding | Buying euphoric tops, selling panicked bottoms | Pre-committed IPS with rebalancing bands; pause when the urge to follow the crowd is strongest |
| Mental accounting | "House money" risk-taking; low-yield savings beside high-interest debt | Recognize fungibility — but harness it deliberately (guilt-free bucket) when it enables good behavior |
| Status quo bias | Never rebalancing; staying in high-fee funds | Harness via defaults: auto-enrollment (~50%→~90% participation), auto-escalation; "would I build this portfolio from scratch today?" |
| Confirmation bias | Reading only bullish research on holdings | Seek the strongest opposing argument; pre-mortem ("it's a year later and this failed — why?") |
| Framing effects | Same facts, different decisions ("90% survival" vs "10% mortality"; nominal vs real) | Reframe every major decision multiple ways; present both gains and losses, percentages and dollars |

Knowing about biases does not eliminate them — debiasing requires structural safeguards: written rules, automation, cooling-off periods (48-72 hours before any news-driven trade), and accountability.

### Coaching Couples Through Money Conversations
Money is a leading source of relationship conflict, usually because couples have never had a structured money conversation.

**First conversation:** 15-20 minutes maximum. Lead with feelings, not accusations ("I feel anxious when..." not "You always..."). Start with the shared vision, not the problems. Avoid trigger words: "budget," "you always/never," shame-loaded phrases.

**Monthly Money Meeting agenda (keep to one hour):**
1. Open with appreciation — name something your partner did with money that you valued.
2. Review the numbers together — income, expenses, goal progress. Keep it factual.
3. Discuss vision progress — what moved forward? What's one thing to experience this month?
4. End on something positive.

**Couple-dynamic playbooks:**
- **Avoider + Optimizer:** The Optimizer manages everything and resents it; the Avoider feels controlled and disengages further. *Play:* give the Avoider full ownership of one bounded area (e.g., the vacation fund); structure conversations via the monthly meeting so the Avoider isn't ambushed; challenge the Optimizer's trivial-vs-big-lever balance.
- **Worrier + Dreamer:** Catastrophe vs magic — they talk past each other. *Play:* make the Dreamer's vision concrete with numbers; show the Worrier the numbers support more freedom than they feel.
- Both partners must engage. One "innocent" partner who touches nothing creates fragility and resentment.

### Visioning Before Tactics
Before tactical work, have the client articulate a specific, vivid picture of the life money should enable (a "Rich Life" vision): fill-in-the-blank prompts ("a perfect ordinary Tuesday in 10 years looks like ______"), an inventory of what makes them irrationally happy, a designed perfect day, and a 10-year "what would I regret not doing?" list. Two rules: get specific (vagueness enables procrastination), and live part of the vision now while building toward the rest — this is not deferred gratification.

## Worked Examples

### Example 1: Disposition Effect — Holding a Loser
**Given:** Investor bought XYZ at $100; now $80 after two quarters of declining revenue, a lost major customer, and a new competitor. "I can't sell now — I'd be locking in a loss."

**Approach:** Name the bias (loss aversion → disposition effect; the $100 anchor). Reframe: purchase price is sunk — "If you held $80 in cash, would you buy XYZ today?" The original thesis is broken, so the rational action is to sell regardless of cost basis (tax-loss harvesting is a tangible consolation). Safeguard: write exit criteria at purchase time ("re-evaluate at -15% or two consecutive revenue misses").

### Example 2: Recency Bias — Panic After a Drawdown
**Given:** After a 25% drawdown: "The market is broken. I'm going to cash."

**Approach:** Validate the emotion first. Provide context: 20%+ drawdowns recur every ~4-6 years and every prior bear market has been followed by recovery — volatility is the price of admission. Quantify the timing cost: selling now converts a paper loss into a need to time re-entry (two correct decisions instead of zero), and the best days cluster near the worst. Revisit the horizon ("retirement is 20 years away"). If they must act, offer a reasonable compromise — trim equity 5-10%, not 100%. Reasonable beats rational.

### Example 3: The Couple Who Can't Spend
**Given:** Couple earning $280K, $1.2M invested, no debt, no vacation in four years: "We can't justify $8,000 on a trip when we could invest it."

**Approach:** Identify types (Optimizer with Worrier traits + disengaged partner). Surface the script ("What did your parents say about spending on vacations?") and test it against present reality. Run the numbers: $8,000 at 7% for 20 years is ~$31,000 — and their current savings rate already exceeds the retirement goal with margin, so the trip changes nothing material. Reconnect spending to values: if travel is a core category, spending there is the *point* of the system. Walk both partners through the visioning exercise — Optimizers often discover their vision includes the experiences they've been denying.

### Example 4: Couples Conflict — Avoider + Optimizer
**Given:** One partner manages everything, tracks every expense, and resents the other "not caring about money." The other feels controlled and shut out; arguments are frequent and circular.

**Approach:** Name the dynamic without blame — neither approach is wrong, but together they spiral (manage more → disengage more → resent more). Reframe the goal: shared engagement at a level both can sustain, not converting the Avoider into an Optimizer. Install the Monthly Money Meeting to replace ad hoc ambushes. Give the Avoider one bounded area of full ownership. Redirect the Optimizer: "You track every coffee but haven't reviewed investment fees in two years — what if that energy went to the big levers?"

## Common Pitfalls
- Biases are easier to spot in others; self-awareness without structural safeguards changes little.
- Contrarianism for its own sake is also a bias — it needs independent analysis behind it.
- Assuming "irrational" is always bad: extra cash held for sleep-at-night comfort may be utility-maximizing. Reasonable > rational.
- Patronizing tone when naming biases — the goal is to empower, not to win.
- Jumping to tactics before surfacing scripts, money type, and vision — optimizing a system without knowing what it should produce.
- Treating a couple as one financial entity: each partner has their own type, scripts, and risk relationship.
- Letting trivial-question conversations crowd out the big levers.

## Cross-References
- **statistics-fundamentals** (core plugin): base rates, probability calibration, compounding math
- **time-value-of-money** (core plugin): framing decisions in present value terms
- **historical-risk** (wealth-management plugin): long-term drawdown context for recency-bias conversations
- **asset-allocation** (wealth-management plugin): systematic rebalancing as a debiasing mechanism
- **diversification** (wealth-management plugin): structural protection against overconfidence and concentration
- **tax-efficiency** (wealth-management plugin): tax-loss harvesting as a consolation for loss aversion; account sequencing
- **performance-reporting** (wealth-management plugin): framing effects in how returns are presented; nominal vs real

## Key Sources
- Kahneman, D. & Tversky, A. (1979). Prospect Theory: An Analysis of Decision under Risk.
- Thaler, R. & Sunstein, C. (2008). *Nudge.*
- Housel, M. (2020). *The Psychology of Money.*
- Sethi, R. (2019). *I Will Teach You to Be Rich*; (2024) *Money for Couples.*


---

## SKILL: financial-planning-integration

- Fuente: `JoelLewis/finance_skills` → `plugins/advisory-practice/skills/financial-planning-integration` (MIT)
- Cuándo usarla: Integrate financial planning engines with the advisor technology stack — data flows between planning tools, CRM, PMS, custodians, and aggregation platforms; capital market assumption (CMA) governance and synchronization; plan-to-IPS-to-model linkage; and governed tax reference parameters in planning tools. Use when the user asks about connecting eMoney, MoneyGuidePro, or RightCapital to CRM or portfolio systems, eliminating manual re-entry between systems, keeping plan and portfolio assumptions consistent, mapping plan outputs (required return, risk capacity, withdrawal schedule) into the IPS and model assignment, or establishing plan update cadence and data-freshness rules. Also trigger on 'plan-to-IPS linkage', 'assumption synchronization', 'CMA governance', or 'planning tool integration'. For planning methodology itself — Monte Carlo modeling, Roth conversion strategy, Social Security claiming, retirement projections — use financial-planning-workflow instead.

# Financial Planning Integration

## Core Concepts

### Financial Planning System Architecture
The financial planning engine is the analytical hub of the advisor technology stack. It ingests client data from multiple systems, models the client's financial future, and produces outputs that drive portfolio construction, cash management, and ongoing advisory recommendations. (For the planning methodology those engines implement, see financial-planning-workflow.)

**Relationship to other systems in the advisor technology stack:**
- **CRM (client relationship management):** Source of client demographic data, household composition, employment status, life events, and planning review triggers. The CRM is the system of record for client facts; the planning tool consumes these facts as inputs.
- **PMS (portfolio management system):** Source of current portfolio holdings, asset allocation, and account types. The plan produces a required return target and risk capacity that feed back to the PMS as constraints for portfolio construction.
- **Custodian:** Source of account balances, positions, and transaction history. Custodial data feeds ensure the plan reflects actual account values rather than stale estimates.
- **Aggregation platform:** Source of held-away assets — accounts at other custodians, employer retirement plans, bank accounts, real estate equity estimates, stock options. Aggregation fills the gap between what the advisor custodies and what the client actually owns, which is essential for a complete financial picture.

**Common financial planning platforms (as of 2026; verify current vendor lineups):** eMoney Advisor, MoneyGuidePro (Envestnet), RightCapital, Naviplan (InvestCloud), and planning modules embedded within all-in-one platforms (e.g., Orion Planning, Advyzon). Platform selection depends on firm size, integration requirements, planning complexity, and client-facing presentation needs. Some platforms emphasize interactive client portals (eMoney, RightCapital); others emphasize advisor-facing analytical depth (MoneyGuidePro, Naviplan).

### Goal Data Model and Status Tracking
Goals are the structured records that flow between the planning tool, CRM, and client portal. Each goal carries a defined set of attributes that downstream systems consume:

- **Target amount:** The dollar amount needed, in today's or future dollars
- **Target date:** When the funds are needed (single date or range for ongoing goals like retirement income)
- **Priority:** Essential, important, or aspirational
- **Funding source:** Which accounts and income streams fund the goal — this account linkage is what connects the plan to the PMS
- **Inflation assumption:** The category-specific inflation rate applied (general CPI, education, healthcare)

Each goal carries a status derived from its current probability of success, and status updates flow out to the CRM and client portal:

- **On track:** Probability at or above the target threshold (commonly 80-90%)
- **Needs attention:** 60-80%, where modest adjustments could restore on-track status
- **At risk:** 40-60%, requiring significant plan changes
- **Unlikely:** Below 40%, where the goal may need restructuring or deprioritization

These status indicators must update dynamically as portfolio feeds refresh plan inputs. How to set goals, prioritize among them, and model trade-offs is methodology — see financial-planning-workflow.

### Capital Market Assumptions as Governed Inputs
The expected return, volatility, and correlation assumptions behind plan projections are the most consequential — and most frequently desynchronized — data elements in the planning stack.

- Small changes are high-leverage: reducing an expected equity return from 8% to 7% can shift a plan's probability of success by 10-15 percentage points. A single probability number presented without assumption context creates false precision.
- The firm should maintain a single authoritative capital market assumptions (CMA) document — owned by the investment committee, reviewed on a defined cadence (quarterly or annually) — that every system (planning tool, PMS, proposal engine) references. Assumptions set independently in each system will drift apart.
- When CMAs change, all systems must update simultaneously and all client plans should be re-run, with material probability changes flagged for advisor review.
- Distribution choices (normal vs. log-normal, historical bootstrapping, regime-switching) are also assumptions that should be documented in the CMA governance record, since different planning tools default to different methods.

Monte Carlo mechanics and how to interpret probability-of-success results are covered in financial-planning-workflow.

### Tax Reference Parameters as Governed Inputs
Planning-tool tax projections depend on annually updated reference data: federal and state bracket thresholds, standard deduction amounts, IRMAA (Medicare income-related monthly adjustment amount) thresholds, contribution limits, and RMD ages. These parameters are data-governance concerns, not just planning inputs:

- Most planning vendors push annual tax-table updates, but firms must verify the update landed before running year-end conversion or withdrawal analyses. A plan computed on last year's brackets silently misstates bracket-fill room and IRMAA exposure.
- Anchor every figure to a tax year in client-facing output. For reference, 2026 values: standard deduction $32,200 (married filing jointly); 22% bracket tops out at $211,400 of MFJ taxable income; first IRMAA threshold $218,000 MFJ (based on MAGI from two years prior). Always verify current-year values — these adjust annually.
- Custom overrides (e.g., a state tax assumption entered manually) should be inventoried and re-validated each year, since they do not refresh with vendor updates.

### Plan-to-Portfolio Linkage
The financial plan and the investment portfolio are two sides of the same coin. The plan determines what the portfolio must deliver (required return, risk budget, withdrawal schedule), and the portfolio must be constructed to meet those requirements. When the plan and portfolio are disconnected, the client receives inconsistent advice.

**From plan to portfolio — the forward link:**
- The plan produces a required rate of return: the return the portfolio must achieve for the plan to succeed at the target probability.
- The plan identifies the client's risk capacity: the maximum tolerable drawdown or volatility before the plan fails. Risk capacity is derived from the plan — a client with a well-funded plan and flexible spending has high risk capacity; a client on the edge of plan failure has low risk capacity.
- These outputs feed the Investment Policy Statement (IPS), which translates planning assumptions into portfolio constraints: target allocation, allowable ranges, rebalancing triggers, withdrawal rules.

**The IPS as the bridge document:**
- The IPS connects the financial plan to the portfolio. It specifies the return objective (from the plan), the risk tolerance (ability from the plan, willingness from client assessment), and the constraints (liquidity needs from the plan's withdrawal schedule, time horizon from the plan's goal dates, tax considerations from the plan's tax projection).
- When the plan changes, the IPS should be reviewed and updated. When the IPS changes, the portfolio should be adjusted accordingly.

**From portfolio to plan — the feedback loop:**
- Portfolio performance (actual returns, contributions, withdrawals) feeds back to update the plan. If the portfolio outperforms, the plan's probability of success improves. If the portfolio underperforms, the plan may need adjustment.
- Account-level activity (Roth conversions executed, RMDs taken, tax-loss harvesting realized) affects the plan's tax projection and should be reflected in the next plan update.

**Closed-loop planning:** Changes in the portfolio feed back to update the plan; changes in the plan feed forward to update the portfolio. This two-way connection is the hallmark of integrated advisory practice. Without it, the plan and portfolio drift apart over time, and the client receives conflicting messages about their financial situation.

**Mapping goals to accounts and time horizons:**
- Short-term goals (1-3 years) map to low-risk allocations: cash, short-term bonds, money market funds.
- Medium-term goals (3-10 years) map to moderate allocations: intermediate-term bonds, balanced strategies.
- Long-term goals (10+ years) map to growth allocations: equities, real assets, alternatives.
- This goal-to-account mapping ("bucketing" or "time segmentation") is the data linkage that lets clients see why different parts of the portfolio are invested differently — and it only works if the planning tool's goal records are linked to specific PMS accounts.

### Data Flows and Integration Patterns
The financial plan is only as good as the data that flows into it and the degree to which its outputs are acted upon.

**Data flowing into the financial plan:**
- **Client demographics** (from CRM): names, dates of birth, marital status, dependents, employment status, expected retirement date, health status, state of residence.
- **Current portfolio** (from PMS/custodian): account types, balances, holdings, asset allocation, cost basis, unrealized gains/losses.
- **Held-away assets** (from aggregation): 401(k) plans at current or former employers, spouse's accounts, bank accounts, real estate equity, stock options, restricted stock units, deferred compensation.
- **Insurance policies** (from client interview or document upload): life, disability, long-term care, annuity contracts.
- **Real estate** (from client interview or third-party valuation): primary residence value, mortgage balance, rental and vacation properties.
- **Income and expense data** (from client interview, tax returns, or budgeting tools): salary, bonus, rental and investment income, Social Security estimates (from SSA statements), pension details, itemized expenses or estimated spending rates.

**Data flowing out of the financial plan:**
- **Required return target** (to PMS/IPS): drives asset allocation decisions.
- **Risk capacity** (to PMS/IPS): the maximum risk the plan can tolerate before probability of success drops below the acceptable threshold.
- **Recommended savings rate** (to advisor/client): the annual savings needed to keep the plan on track.
- **Withdrawal schedule** (to PMS for cash management): timing and amount of withdrawals from each account, accounting for tax optimization and RMD requirements.
- **Roth conversion schedule** (to PMS for execution): recommended conversion amounts by year.
- **Goal status updates** (to CRM/client portal): on-track, needs attention, at risk, unlikely — for each goal.

**Integration challenges:**
- **Manual re-entry:** Many advisory firms still manually re-enter data between systems (e.g., typing client data from the CRM into the planning tool, or manually updating the plan when portfolio values change). This introduces errors, consumes advisor time, and causes data staleness.
- **Data freshness:** If the plan uses a portfolio snapshot from three months ago, the plan's outputs may not reflect current reality. Automated data feeds (via APIs or custodial data feeds) keep the plan current.
- **Assumption synchronization:** The financial plan and the PMS must use consistent return assumptions. If the plan assumes a 7% return for equities but the PMS uses 8%, the plan and portfolio will produce conflicting messages. Assumption synchronization requires a documented process: assumptions are set once (typically in the CMA document), and all downstream systems reference the same source.
- **Bidirectional updates:** Changes in the portfolio (performance, deposits, withdrawals, Roth conversions) should flow back to update the plan automatically. Changes in the plan (new goals, revised assumptions, updated claiming strategy) should flow forward to trigger portfolio review. Most current platforms support one direction reasonably well but not both.

### Plan Outputs, Update Cadence, and Documentation
**Standard visual outputs from planning tools** (useful when specifying portal or report integrations): probability gauge (overall probability of success), goal funding chart (per-goal probability), cash flow waterfall (income sources stacked against expenses by year), net worth projection (base case plus scenario lines), and Monte Carlo fan chart (median and percentile bands). Modern tools also support real-time scenario recalculation during client meetings, which requires live data connections rather than stale imports.

**Plan update cadence and triggers:**
- **Annual review:** At minimum, the plan is updated once per year with current portfolio values, revised income/expense assumptions, and any goal changes.
- **Event-driven updates:** Major life events recorded in the CRM (job change, retirement, inheritance, divorce, death of a spouse, birth of a child, home purchase or sale) should trigger a plan update automatically.
- **Continuous monitoring:** Some platforms provide daily plan updates from live portfolio feeds, alerting the advisor when probability of success drops below a threshold. Batch re-runs after major market dislocations (e.g., a drawdown exceeding 15%) identify clients whose plans need attention.

**Plan acceptance and documentation:** After presenting the plan, document the client's acknowledgment of the assumptions used, the recommendations made, and the client's decisions (accepted, deferred, declined). This supports compliance requirements and ensures the planning tool, CRM, and IPS all reflect the same agreed state.

## Worked Examples

### Example 1: Closing the Loop Between Financial Planning and Portfolio Management

**Scenario:** A mid-size RIA with $800M in assets under management uses separate systems for financial planning (eMoney) and portfolio management (Orion). The firm discovers that the planning tool assumes a 6.5% return for a balanced portfolio while the PMS assumes 7.5% for the same allocation. This 100-basis-point discrepancy means the plans are more conservative than the portfolios imply, leading to inconsistent client communications: the plan says "you need to save more" while the portfolio projection says "you are ahead of schedule." The firm wants to close the loop.

**Design Considerations:**
1. **Assumption synchronization.** The root cause is that assumptions are set independently in each system. The fix requires a single authoritative source for capital market assumptions (CMAs). Establish a formal CMA document — reviewed and approved quarterly or annually by the firm's investment committee — that specifies expected return, standard deviation, and correlation for each asset class. Both the planning tool and the PMS must reference this document. When CMAs change, both systems must be updated simultaneously.

2. **Plan-to-IPS-to-model mapping.** Define a clear chain: the financial plan produces a required return and risk capacity for each client. These flow into the client's IPS, which specifies a target allocation and model portfolio. The model portfolio is implemented in the PMS. The mapping should be explicit and documented:
   - Plan output: "This client needs a 5.2% real return with a maximum drawdown tolerance of -25%."
   - IPS translation: "Target allocation: 65% equity / 30% fixed income / 5% alternatives. Benchmark: 65% MSCI ACWI / 30% Bloomberg Aggregate / 5% HFRI Fund Weighted."
   - PMS implementation: "Assign to Balanced Growth Model (Model BG-65)."

3. **Integration architecture.** Map the data flows between systems:
   - CRM to planning tool: client demographics, household data, life events (automated via API or manual entry).
   - Custodian to PMS: account balances, positions, transactions (automated via custodial data feed — daily).
   - PMS to planning tool: current portfolio value, allocation, account types (automated via API, or manual export/import if no API exists). This feed should refresh at least monthly, preferably daily.
   - Planning tool to PMS: required return target, withdrawal schedule, Roth conversion schedule (typically manual — the advisor interprets plan outputs and implements in the PMS, but the firm should document this handoff).
   - Planning tool to CRM: goal status, plan review date, plan probability of success (for advisor dashboard and client portal display).

4. **Ongoing update workflow.** Define the cadence and triggers:
   - **Quarterly:** PMS pushes updated portfolio values to the planning tool. The plan recalculates probability of success. If the probability changes by more than 5 percentage points, the advisor reviews the plan and considers whether action is needed.
   - **Annually:** The investment committee reviews and publishes updated CMAs. Both the planning tool and PMS are updated simultaneously. All client plans are re-run with the new assumptions. Material changes in probability are flagged for advisor review.
   - **Event-driven:** Major client life events (recorded in CRM) trigger a plan review. Major market events (a drawdown exceeding 15%) trigger a batch re-run of all plans to identify clients whose probability has dropped below the threshold.

**Analysis:**
The assumption mismatch is a governance failure, not a technology failure. The technology fix (syncing assumptions) is straightforward; the governance fix (establishing a single source of truth for CMAs, with a documented review and update process) is what prevents the problem from recurring.

Implementation steps:
1. The investment committee publishes a formal CMA document with expected returns, standard deviations, and correlations for all asset classes used in the firm's models. Include both nominal and real return expectations.
2. Update the planning tool to use the published CMAs. Most planning tools allow custom asset class assumptions — enter the exact figures from the CMA document.
3. Update the PMS to use the same CMAs for portfolio projections and performance expectations.
4. Verify consistency: run a test case through both systems. A client with a 60/40 portfolio should see the same expected return in the plan and the PMS projection. Document the verification.
5. Establish the quarterly/annual review cadence and assign ownership (the investment committee owns CMAs; the planning team owns the plan-side update; the portfolio operations team owns the PMS-side update).
6. Build a reconciliation check: quarterly, compare the expected return assumptions in the planning tool and PMS for a sample of clients. Flag any discrepancies.
7. Document the plan-to-IPS-to-model mapping for each client tier or model portfolio. When a new client plan is completed, the advisor uses the mapping to assign the appropriate model in the PMS.

The closed-loop workflow ensures that the plan drives the portfolio (forward link) and the portfolio updates the plan (feedback loop), with consistent assumptions at every step. The client hears one coherent story, not conflicting messages from disconnected systems.

### Example 2: Governing the Tax Parameters Behind a Roth Conversion Schedule

**Scenario:** An advisor uses the planning tool to model a multi-year Roth conversion ladder for a recently retired client, filling lower tax brackets each year while staying under IRMAA thresholds. (The conversion methodology itself — bracket-fill logic, conversion sizing, paying conversion tax from taxable assets — is covered in financial-planning-workflow.) The integration question: the conversion schedule's correctness depends entirely on the tax reference parameters loaded in the planning tool, and on the schedule flowing accurately to the PMS for execution.

**Design Considerations:**
1. **Tax parameter currency.** The bracket-fill calculation hinges on three annually updated figures, each of which must reflect the correct tax year in the planning tool. For tax year 2026 (verify current-year values): the MFJ standard deduction is $32,200; the 22% bracket tops out at $211,400 of taxable income; and the first IRMAA surcharge threshold is $218,000 of MAGI (MFJ), applied with a two-year lookback. If the tool still carries prior-year tables, every year of the conversion schedule is mis-sized — the plan will either leave bracket room unused or push conversions over an IRMAA threshold, where the surcharge can add several thousand dollars per person per year in Medicare costs.
2. **Parameter audit before year-end runs.** Add a checklist item to the firm's planning operations calendar: confirm the vendor's annual tax-table update has been applied, and re-validate any manually entered overrides (state tax rates, custom deduction assumptions) before running year-end conversion analyses.
3. **Schedule handoff to the PMS.** The plan's output — the recommended conversion amount by year — must reach the team executing conversions in the PMS/custodian. Document this handoff: who transcribes the schedule, where it lives in the PMS, and how mid-year income changes (which alter remaining bracket room) trigger a recalculation in the planning tool before the conversion is executed.
4. **Feedback loop.** Executed conversions must flow back into the plan (via the custodial feed or manual update) so the next year's bracket-fill calculation starts from the actual remaining traditional IRA balance, not the projected one.

**Analysis:**
The recurring failure mode is not bad planning logic but stale or unsynchronized data: prior-year tax tables, a conversion schedule executed from an outdated plan version, or executed conversions never reflected back into the plan. Treat tax parameters like CMAs — versioned, owned, and verified on a calendar — and treat the conversion schedule like any other plan-to-PMS data flow, with a documented handoff and a return feed. Because IRMAA uses a two-year MAGI lookback, the plan must also retain prior-year income data accurately; a planning tool that only models the current year forward will miss surcharges triggered by income already realized.

## Common Pitfalls
- Using different capital market assumptions in the financial planning tool and the portfolio management system, leading to conflicting client communications about whether the plan is on track.
- Manual re-entry of data between planning and portfolio systems, introducing errors and data staleness that undermine plan accuracy.
- Treating assumption updates as ad hoc rather than governed — without a single CMA source of truth with assigned ownership and review cadence, systems drift apart again after every fix.
- Presenting a single Monte Carlo probability number without acknowledging assumption sensitivity — a 1-2% change in expected return can move the probability by 10-15 percentage points, so assumption governance is inseparable from honest plan communication.
- Running year-end tax analyses (Roth conversions, gain harvesting) on stale tax reference parameters — bracket thresholds, standard deductions, and IRMAA thresholds change every year and must be verified in the tool.
- Supporting only one direction of synchronization — portfolio changes that never update the plan, or plan changes that never trigger portfolio review, break the closed loop.
- Not linking goals to specific accounts and time horizons — without this linkage, the portfolio allocation has no data connection to the plan's requirements, and goal status cannot be computed from live account values.
- Not documenting the client's acknowledgment of planning assumptions and recommendations — this creates compliance risk and makes it difficult to demonstrate the advisor's reasoning at future review meetings.

## Cross-References
- **financial-planning-workflow** (advisory-practice plugin): The single home for planning methodology — data gathering, retirement modeling, Monte Carlo interpretation, Roth conversion and Social Security strategy, scenario modeling, and plan presentation. This skill covers how that methodology connects to the rest of the technology stack.
- **investment-policy** (wealth-management plugin): The financial plan drives IPS construction by providing the required return, risk capacity, time horizon, and constraint inputs that the IPS formalizes into portfolio governance.
- **asset-allocation** (wealth-management plugin): The plan's required return and risk capacity set the boundaries for strategic asset allocation; plan goals map to time-horizon-based allocation buckets.
- **portfolio-management-systems** (advisory-practice plugin): The PMS implements the portfolio derived from the financial plan's outputs; data flows between the planning tool and PMS must be bidirectional and assumption-consistent.
- **client-reporting-delivery** (advisory-practice plugin): Plan progress reporting — goal status, probability of success, milestone tracking — is a core component of the client report package.
- **proposal-generation** (advisory-practice plugin): Financial plan outputs (required return, recommended allocation, account types) feed directly into the investment proposal presented to new and existing clients.
- **crm-client-lifecycle** (advisory-practice plugin): The CRM stores planning data (goals, assumptions, plan review dates), triggers event-driven plan updates based on life events, and displays plan status on the advisor dashboard.
- **tax-efficiency** (wealth-management plugin): Defines the asset location, Roth conversion, withdrawal sequencing, and harvesting principles whose outputs flow through the integrations described here.


---

## SKILL: financial-planning-workflow

- Fuente: `JoelLewis/finance_skills` → `plugins/advisory-practice/skills/financial-planning-workflow` (MIT)
- Cuándo usarla: Orchestrate the advisor workflow for assembling and delivering a comprehensive financial plan — data gathering, cash flow analysis, retirement modeling, Monte Carlo analysis, Roth conversion and withdrawal sequencing, Social Security claiming strategy, education and estate goals, scenario modeling, and prioritized recommendations. Use when the user asks about building a financial plan, structuring a planning engagement, retirement or Social Security modeling, Roth conversion strategy, scenario analysis, prioritizing competing recommendations, preparing a plan presentation, or deciding when a plan needs updating. Also trigger on 'comprehensive financial plan', 'discovery meeting', 'retirement modeling', 'Monte Carlo', 'Roth conversion', 'Social Security claiming', 'savings rate', or 'is my client on track'. For planning-tool data flows, capital market assumption governance, or connecting planning software to CRM/PMS, use financial-planning-integration instead.

# Financial Planning Workflow

## Core Concepts

### Client Profile and Data Gathering
The financial plan begins with a structured intake that captures the client's complete financial picture. Incomplete data leads to unreliable projections and missed planning opportunities. The advisor should collect the following categories systematically before any analysis begins:

**Household demographics** — ages, marital status, dependents (ages and expected years of financial support), health status and family longevity history, employment status and expected retirement dates, state of residence (for state tax modeling).

**Income and benefits** — gross salary, bonuses, commissions, self-employment income, rental income, pension details (defined benefit formula, COLA, survivor options), Social Security statements for both spouses, deferred compensation schedules, stock option or RSU vesting schedules.

**Expense analysis** — fixed obligations (mortgage, loan payments, insurance premiums, property taxes), discretionary spending (travel, dining, entertainment), irregular expenses (home maintenance, vehicle replacement, medical), and expected changes (mortgage payoff date, child-related expenses aging out, healthcare costs in retirement).

**Assets and accounts** — taxable brokerage accounts, traditional and Roth IRAs, 401(k)/403(b) balances and contribution rates, HSAs, 529 plans, real estate (primary residence and investment properties with basis information), business ownership interests, cash reserves, and any concentrated stock positions.

**Liabilities** — mortgage balance, rate, and remaining term; student loans; auto loans; credit card balances; HELOCs; any contingent liabilities (co-signed loans, pending legal obligations).

**Insurance** — life insurance (term and permanent, face amounts, premiums, cash values), disability coverage (employer-provided and individual, benefit amounts, elimination periods, own-occupation vs any-occupation), long-term care coverage, umbrella liability, and health insurance details.

**Estate documents** — wills, trusts, powers of attorney, healthcare directives, beneficiary designations on all accounts and insurance policies, any existing irrevocable trusts or family limited partnerships.

**Tax returns** — most recent two to three years of federal and state returns, revealing effective tax rates, deduction patterns, AMT exposure, capital gain/loss carryforwards, and charitable giving history.

### Cash Flow Analysis
Cash flow is the engine of the financial plan. Before projecting any future goals, the advisor must establish a reliable baseline of current income, spending, and savings. Key steps include:

1. **Categorize income sources** by stability (guaranteed vs variable), tax treatment (ordinary, qualified dividend, capital gain, tax-exempt), and expected duration (salary until retirement, pension for life, Social Security from age 62-70).
2. **Build the expense baseline** from actual spending data (bank and credit card statements), not estimates. Clients consistently underestimate discretionary spending. Apply a 10-15% buffer if only using estimates.
3. **Calculate the savings rate** as a percentage of gross income. A rate below 15% for clients more than 15 years from retirement is a yellow flag. Document where current savings flow (401k, IRA, taxable, 529).
4. **Project cash flow changes** over time: salary growth assumptions, expense step-downs (mortgage payoff, children finishing college), expense step-ups (healthcare in early retirement before Medicare, long-term care in later years), and inflation-adjusted lifestyle spending.
5. **Identify surplus or deficit** in the current year and in projected future years. A current surplus is the raw material for all goal funding. A current deficit means the plan must address spending reduction or income enhancement before layering on new goals.

### Retirement Modeling
Retirement is typically the largest and most complex goal in the plan. The analysis has two phases: accumulation (saving and investing toward retirement) and distribution (drawing down assets to fund retirement spending).

**Accumulation phase** — project account balances forward using current savings rates, employer matches, expected returns by asset class, and tax-deferred growth. Model the impact of increasing savings rates (e.g., saving all future raises). Account for expected lump-sum events (inheritance, home downsizing, stock option exercises).

**Social Security optimization** — model claiming at 62, full retirement age, and 70 for both spouses. The optimal strategy depends on relative earnings, age difference, health, and other income sources. Delayed claiming increases the inflation-adjusted guaranteed income floor. For married couples, evaluate the restricted application and survivor benefit interaction.

**Pension integration** — if the client has a defined benefit pension, model the lump-sum vs annuity decision, survivor benefit election (joint-and-survivor percentages), and COLA provisions. The pension's guaranteed income reduces the withdrawal burden on the investment portfolio.

**Sustainable withdrawal strategy** — establish the initial withdrawal rate (commonly benchmarked against 4% but adjusted for plan duration, asset allocation, and flexibility). Model withdrawal sequencing across account types: draw from taxable first to allow tax-deferred accounts to compound, but consider Roth conversion opportunities in low-income years between retirement and Social Security/RMD onset.

**Monte Carlo simulation** — run probability-of-success analysis using 1,000+ randomized return sequences to stress-test the plan against sequence-of-returns risk. A plan with 80-90% success probability is generally considered funded. Below 70% requires material adjustment. Present results as a confidence range rather than a single deterministic projection.

**Longevity risk** — plan to age 90-95 for at least one spouse. Use mortality tables adjusted for client health and family history. Discuss the asymmetry: running out of money is catastrophic, while dying with a surplus is merely suboptimal.

### Education Funding
For clients with children or grandchildren, education funding is modeled as a specific goal with its own timeline and inflation rate:

- **Estimate total cost** using current tuition for target institution types (public in-state, public out-of-state, private) inflated at the education inflation rate (historically 5-6% annually, higher than general CPI).
- **Assess current 529 balances** and ongoing contribution capacity. Model the investment glide path within the 529 (aggressive early, conservative as enrollment approaches).
- **Analyze the funding gap** between projected 529 balances and total cost. Determine how much must come from current cash flow at the time of enrollment.
- **Consider financial aid interaction** — 529 assets owned by the parent count as parental assets on the FAFSA (assessed at up to 5.64% vs 20% for student assets). The simplified FAFSA replaced the Expected Family Contribution with the Student Aid Index (SAI), and under SAI rules distributions from grandparent-owned 529s no longer count as student income. Verify current FAFSA treatment when modeling aid eligibility.
- **Evaluate trade-offs** between fully funding education and other goals. Retirement should generally take priority because education can be funded with loans while retirement cannot.

### Estate Planning Integration
The financial plan must address wealth transfer, even for clients who do not consider themselves wealthy. Key elements:

- **Estate tax exposure** — calculate the gross estate (all assets including life insurance death benefits, retirement accounts, and real estate) against the current federal exemption. The scheduled TCJA sunset never took effect: the One Big Beautiful Bill Act (2025) set the exemption at $15 million per person (about $30 million per married couple) for 2026, made it permanent, and indexed it for inflation beginning in 2027. Verify current-year exemption values before modeling. For clients near or above the exemption, model lifetime gifting and trust strategies that use the exemption.
- **Trust structures** — identify whether existing or new trusts serve the client's goals: revocable living trusts for probate avoidance, irrevocable life insurance trusts (ILITs) for removing life insurance from the estate, generation-skipping trusts, and special needs trusts for dependents with disabilities.
- **Beneficiary designation audit** — verify that beneficiary designations on retirement accounts, insurance policies, and TOD/POD accounts are current and consistent with the estate plan. Beneficiary designations override wills.
- **Charitable giving strategy** — for charitably inclined clients, evaluate donor-advised funds, qualified charitable distributions (QCDs) from IRAs after age 70.5, charitable remainder trusts, and bunching strategies for itemized deductions.
- **Business succession** — for business owners, integrate the succession or sale timeline with the retirement plan. Model the after-tax proceeds from a business sale and the transition of income from active business earnings to investment portfolio withdrawals.

### Risk Management Review
Assess whether the client's insurance coverage matches the risks identified in the plan:

- **Life insurance gap** — calculate the capital needed to replace the insured's income contribution, fund remaining goals (education, mortgage payoff), and provide for surviving dependents. Subtract existing coverage and assets. The gap determines additional coverage needed.
- **Disability coverage** — verify that combined employer and individual coverage replaces at least 60% of gross income. Check elimination periods, benefit duration, own-occupation definitions, and coordination with other income sources.
- **Long-term care** — for clients over age 50, model the potential cost of extended care (in-home, assisted living, skilled nursing) and evaluate traditional LTC insurance, hybrid life/LTC products, or self-insurance strategies based on asset levels.
- **Liability coverage** — ensure umbrella liability coverage is adequate relative to net worth. Minimum recommended coverage is typically equal to net worth or $1 million, whichever is greater.

### Scenario Modeling
A single deterministic projection creates false precision. The plan should present at least three scenarios to frame the range of outcomes:

1. **Base case** — reasonable assumptions for returns, inflation, income growth, and spending. This is the plan the client tracks against.
2. **Optimistic case** — higher returns, earlier-than-expected inheritance, lower healthcare costs, or ability to work part-time in early retirement. Shows upside potential and what becomes possible.
3. **Pessimistic case** — lower returns, job loss at age 55, major health event, market crash in early retirement years (sequence-of-returns stress test), or need to support aging parents. Shows downside risk and what breaks.

Additionally, model specific what-if questions the client raises: "What if I retire at 58 instead of 62?" "What if we move to a no-income-tax state?" "What if we pay for private school?" Each what-if should show the impact on retirement success probability and the trade-off with other goals.

### Prioritized Recommendations
The output of the planning process is a ranked list of action items. Prioritization follows this framework:

1. **Foundation items first** — emergency fund adequacy, appropriate insurance coverage, estate document completion. These protect against catastrophic risk and cost relatively little.
2. **Employer match capture** — maximize 401(k) contributions to the employer match. This is an immediate 50-100% return.
3. **High-interest debt elimination** — pay down debt with interest rates above the expected portfolio return (typically any debt above 6-7%).
4. **Tax-advantaged account maximization** — fill remaining 401(k)/403(b) space, fund Roth IRAs (or backdoor Roth), HSA contributions.
5. **Goal-specific funding** — direct remaining surplus to prioritized goals (retirement shortfall, education funding, home purchase).
6. **Tax optimization moves** — Roth conversions in low-income years, tax-loss harvesting, asset location optimization, charitable giving strategies.
7. **Estate planning actions** — trust creation, beneficiary updates, gifting strategies.

Each recommendation should include a specific action, responsible party, target completion date, and the quantified impact on the plan (e.g., "Increasing 401k contribution from 6% to 10% improves retirement success probability from 72% to 84%").

### Plan Presentation and Delivery
The plan presentation meeting converts analysis into client commitment. Effective delivery requires:

- **Lead with goals, not numbers** — begin by restating the client's goals and concerns as expressed in the discovery meeting. This demonstrates that the plan is personalized, not generic.
- **Present the base case first** — show that the plan works under reasonable assumptions before introducing stress scenarios. Clients anchor on the first number they see.
- **Use plain language** — translate Monte Carlo success rates into concrete terms: "In 85 out of 100 simulated market environments, your portfolio sustains your spending through age 95."
- **Discuss trade-offs explicitly** — when goals compete for limited resources, present the trade-off clearly: "Fully funding both children's education at private universities reduces your retirement success probability from 88% to 71%. Here are three alternatives that balance both goals."
- **Document agreed-upon actions** — end the meeting with a written list of next steps, owners, and deadlines. This becomes the implementation checklist that the advisory team tracks.

### Ongoing Monitoring
A financial plan is a living document. Establish triggers for plan updates:

- **Scheduled reviews** — full plan update annually, brief progress check at semi-annual or quarterly client reviews.
- **Life event triggers** — marriage, divorce, birth of a child, job change, inheritance, health diagnosis, home purchase or sale, retirement date change, death of a spouse.
- **Market-driven triggers** — portfolio value deviates more than 20% from the plan projection, interest rate environment changes materially (affecting bond allocation and mortgage decisions), or tax law changes affect planning assumptions.
- **Goal completion** — when a goal is achieved (mortgage paid off, child graduates, insurance need expires), reallocate the freed cash flow to remaining or new goals.

At each update, re-run the probability-of-success analysis and compare to the prior review. Track whether the plan is improving, stable, or deteriorating, and adjust recommendations accordingly.

## Worked Examples

### Example 1: Dual-Income Couple with Retirement and Education Goals
**Scenario:** Michael (44) and Sarah (42) are married with two children (ages 10 and 7). Combined gross income is $285,000. They have $620,000 in retirement accounts (mix of 401k and Roth IRA), $85,000 in 529 plans, a $480,000 mortgage at 3.25% with 22 years remaining, and $45,000 in taxable savings. Both have employer-sponsored health and disability insurance. They have basic term life policies ($500,000 each) and outdated wills drafted before their second child was born. They want to retire at 62, send both children to four-year public universities, and pay off the mortgage before retirement.

**Planning Elements:**
- Cash flow analysis reveals a $2,800/month surplus after all current obligations and savings. Current savings rate is 18% of gross income (strong).
- Retirement modeling projects $2.1M in retirement assets at age 62 assuming 6.5% nominal returns, current contribution rates, and employer matches. Estimated retirement spending is $9,500/month in today's dollars. Social Security at full retirement age (67) provides combined $5,200/month. Monte Carlo simulation shows 79% success probability at current trajectory — below the 85% target.
- Education funding gap: projected four-year public university cost is $140,000 per child (in future dollars). Current 529 balances plus ongoing contributions cover approximately 65% of costs. Remaining $98,000 gap across both children.
- Mortgage payoff by 62 requires $1,400/month in additional principal payments starting now, which consumes half the current surplus.
- Life insurance gap analysis shows $500,000 per spouse is insufficient — Michael's income supports the mortgage and retirement savings; Sarah's supports education funding and lifestyle. Recommended coverage: $1.2M on Michael, $800,000 on Sarah.
- Estate documents need updating: add second child as beneficiary, establish guardianship designations, update healthcare directives.

**Analysis:** The plan reveals competing demands on a finite surplus. Prioritized recommendations: (1) Update wills and beneficiary designations immediately — no cost, high risk reduction. (2) Increase term life coverage to recommended levels — adds approximately $120/month. (3) Increase 401(k) contributions by 2% of salary each ($475/month combined) to close the retirement gap — improves Monte Carlo success to 86%. (4) Maintain current 529 contributions but do not accelerate — the education gap can be bridged with cash flow from reduced expenses as children age and from the surplus freed when the mortgage reaches its natural payoff date (age 66). (5) Do not accelerate mortgage payoff — the 3.25% rate is below expected portfolio returns, and the capital is more productive in retirement accounts. The mortgage payoff falls after the target retirement date, but the remaining balance ($68,000) is manageable from retirement assets. Present this trade-off explicitly so the client can make an informed decision about the emotional value of entering retirement debt-free versus the financial efficiency of maintaining the mortgage.

### Example 2: Near-Retirement Single Professional
**Scenario:** Patricia (58) is a single corporate attorney earning $210,000 annually. She has $1.4M in her 401(k), $180,000 in a Roth IRA, $95,000 in a taxable brokerage account, and owns her home outright (valued at $550,000). She wants to retire at 62 but is concerned about healthcare costs before Medicare eligibility at 65. Her Social Security benefit at 62 is $2,100/month; at 67 it is $3,100/month; at 70 it is $3,850/month. She has no pension, no dependents, and her estate plan leaves everything to a sibling and two nieces. She has employer-provided life and disability insurance that terminates at retirement.

**Planning Elements:**
- Cash flow analysis shows current spending of $7,800/month. In retirement, work-related expenses drop but healthcare costs add approximately $1,200/month for ACA marketplace coverage (ages 62-65). Net retirement spending estimate: $7,200/month in today's dollars.
- Retirement modeling: at age 62, projected portfolio is $1.72M across all accounts. Required annual withdrawal is approximately $86,400 (before Social Security). If she claims Social Security at 62 ($25,200/year), portfolio withdrawal drops to $61,200/year — a 3.6% withdrawal rate on the portfolio. Monte Carlo simulation shows 83% success probability.
- Delaying Social Security to 67 increases the annual benefit by $12,000/year (guaranteed, inflation-adjusted) but requires higher portfolio withdrawals for five additional years. Net present value analysis favors delay if Patricia lives past age 80. Delaying to 70 improves success probability to 91% but requires $86,400/year from the portfolio for eight years.
- Roth conversion opportunity: between ages 62 and 67, Patricia's income drops from $210,000 to near zero (only taxable portfolio withdrawals). This creates a five-year window to convert 401(k) assets to Roth at lower tax brackets, reducing future RMD tax burden and providing tax-free income flexibility in later years.
- Healthcare bridge: ACA marketplace premiums are income-sensitive (premium tax credits phase in below 400% FPL). Managing taxable income through strategic Roth conversions and withdrawal sequencing can optimize premium subsidies during the 62-65 gap.
- No dependents means life insurance is unnecessary post-retirement. Disability insurance is no longer needed once she stops working.

**Analysis:** Prioritized recommendations: (1) Build a two-year cash reserve ($175,000) in the taxable account before retirement to fund the first two years of expenses without forced portfolio withdrawals in a potential down market — begin redirecting current savings surplus now. (2) Retire at 62 as planned — the numbers support it. (3) Delay Social Security to age 70 — the guaranteed income increase is the most efficient longevity insurance available, and her portfolio can sustain the interim withdrawals. (4) Execute systematic Roth conversions of $80,000-$100,000 annually from ages 62-67, filling the 22% and 24% tax brackets. This front-loads tax liability but reduces lifetime taxes and eliminates RMD pressure. (5) Manage ACA income carefully — keep MAGI below the subsidy cliff during ages 62-65 by coordinating Roth conversion amounts with healthcare premium optimization. (6) Simplify the estate plan — current documents are adequate, but consider adding a revocable living trust to avoid probate on the real estate and ensure seamless transfer to the sibling and nieces.

### Example 3: Post-Divorce Financial Reset
**Scenario:** David (47) recently finalized a divorce. He received $310,000 from the division of retirement accounts (rolled into an IRA), $120,000 in a taxable account, and retains the family home (valued at $425,000 with a $280,000 mortgage at 4.75%). He has primary custody of two children (ages 12 and 14) and receives $2,400/month in child support until each child turns 18. His salary is $135,000. He has a $250,000 term life policy from his employer but no individual coverage. His previous financial plan was built around dual incomes and is now obsolete. He has no updated will or estate documents.

**Planning Elements:**
- Cash flow analysis reveals a tight budget: after mortgage ($1,850/month), child-related expenses, and basic living costs, the monthly surplus is only $400. Child support of $2,400/month expires in 4 years (older child) and 6 years (younger child). Current savings rate is under 4% of gross income — a critical concern.
- Retirement modeling: $310,000 in the IRA at age 47 with minimal ongoing contributions projects to approximately $740,000 by age 67 at 6.5% returns. Combined with Social Security (estimated $2,600/month at 67), this supports only $5,200/month in retirement — well below his current $7,800/month spending. Monte Carlo success probability: 52%. The plan is significantly underfunded.
- Housing decision: the mortgage at 4.75% on a home sized for a family may not be optimal for a single parent whose children will leave in 4-6 years. Selling the home, capturing approximately $145,000 in equity, moving to a less expensive property, and redirecting the savings could materially improve the retirement outlook. However, this must be weighed against stability for the children during the post-divorce transition.
- Insurance gaps: the $250,000 employer term policy is insufficient. If David dies, the children lose his income ($135,000/year) and child support ends. They need a guardian with resources to fund their care and education. Recommended coverage: $750,000-$1,000,000 of individual term life, decreasing as the children age out.
- Estate documents are urgent: the former spouse is likely still named as beneficiary on retirement accounts, insurance policies, and possibly the will. These must be updated immediately. A new will must name a guardian for the minor children.
- Education funding: no 529 accounts exist. With the tight budget, starting 529 contributions is unrealistic until child support expenses end and the surplus increases.

**Analysis:** This plan requires honest conversation about trade-offs and a phased approach. Prioritized recommendations: (1) Update all beneficiary designations and estate documents within 30 days — this is the highest-urgency item. Name a guardian for the children. Remove the former spouse from all accounts. (2) Obtain individual term life insurance ($750,000, 15-year term) immediately while David is healthy — estimated cost $65/month. (3) Increase 401(k) contribution to capture the full employer match if not already doing so. (4) Build a three-month emergency fund ($18,000) in a high-yield savings account — currently has no dedicated emergency reserve. (5) When child support for the older child ends (in 4 years), redirect $1,200/month to retirement savings — this single change improves Monte Carlo success to 68%. When the second child's support ends, redirect another $1,200/month — success probability reaches 79%. (6) Evaluate the housing decision at the 4-year mark when the older child leaves for college. At that point, downsizing becomes practical and can unlock equity for retirement savings. (7) Education funding is deferred — David should discuss expectations honestly with the children. Community college for two years followed by university transfer, merit scholarships, and modest student loans are realistic alternatives to full four-year residential funding. Retirement must take priority because it cannot be financed with debt. Present the full timeline showing how the plan improves materially as child-related expenses roll off over the next six years.

## Common Pitfalls
- Treating the financial plan as a one-time deliverable rather than a living document that requires regular updates and course corrections
- Starting analysis before completing data gathering, leading to inaccurate projections and missed planning opportunities
- Using a single deterministic projection instead of scenario modeling, which creates false confidence in a specific outcome
- Failing to model the interaction between goals — funding one goal aggressively may starve another
- Allowing the client's emotional preference (e.g., paying off a low-rate mortgage) to override financial efficiency without at least quantifying the trade-off
- Ignoring the healthcare cost bridge between early retirement and Medicare eligibility at 65
- Neglecting to audit beneficiary designations, which override wills and can direct assets to former spouses or deceased individuals
- Modeling retirement spending as a flat inflation-adjusted number when spending patterns actually change (higher early in retirement during active years, lower in middle years, higher again if long-term care is needed)
- Prioritizing education funding over retirement — clients can borrow for education but cannot borrow for retirement
- Presenting too many recommendations at once without clear prioritization, leading to client overwhelm and inaction

## Cross-References
- **savings-goals** (wealth-management plugin): provides goal-based savings calculations referenced during retirement and education analysis
- **debt-management** (wealth-management plugin): debt payoff strategies are evaluated during cash flow and recommendation phases
- **emergency-fund** (wealth-management plugin): emergency fund adequacy is assessed early in the planning process
- **liquidity-management** (wealth-management plugin): cash flow tier structure informs the plan's liquidity analysis
- **tax-efficiency** (wealth-management plugin): tax-aware strategies (Roth conversions, asset location) are core plan recommendations
- **investment-policy** (wealth-management plugin): the financial plan informs and is codified in the investment policy statement
- **time-value-of-money** (core plugin): PV/FV/annuity calculations underpin all projection modeling
- **client-review-prep** (advisory-practice plugin): plan progress review is integrated into the periodic client review workflow
- **financial-planning-integration** (advisory-practice plugin): covers the software and system integration for planning tools
- **proposal-generation** (advisory-practice plugin): the financial plan often leads to an investment proposal for implementation
- **tax-loss-harvesting** (wealth-management plugin): TLH is a specific tax recommendation that may emerge from the plan
- **insurance-planning** (wealth-management plugin): risk management and insurance coverage review is a standard module of the comprehensive planning process
- **estate-gifting** (wealth-management plugin): estate, gifting, and beneficiary review content for the estate planning module of the comprehensive plan
- **retirement-decumulation** (wealth-management plugin): decumulation strategy — withdrawal rates, RMDs, Social Security timing — is a core deliverable of the retirement-income phase of the plan


---

## SKILL: fund-vehicles

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/fund-vehicles` (MIT)
- Cuándo usarla: Compare and select investment vehicles including mutual funds, ETFs, index funds, and separately managed accounts. Use when the user asks about ETF vs mutual fund, expense ratios, fund tax efficiency, ETF creation/redemption, tracking error, or share class comparisons. Also trigger when users mention 'which fund should I buy', 'Vanguard vs Fidelity', 'index fund costs', '12b-1 fees', 'load vs no-load', 'SMA vs ETF', 'fund turnover ratio', 'securities lending', or ask how fees compound over time.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/wealth-management/skills/fund-vehicles/` (fund_vehicles.py)

# Fund Vehicles

## Core Concepts

### Vehicle Comparison: Decision-Relevant Differences
- **Trading:** ETFs trade intraday at market prices that can deviate from NAV (premiums/discounts, especially in volatile markets or for illiquid underlying assets); mutual funds transact once daily at NAV.
- **Tax efficiency:** ETFs generally distribute far fewer capital gains than mutual funds (mechanism below); SMAs allow lot-level tax-loss harvesting that pooled vehicles cannot.
- **Customization:** SMAs hold individual securities directly, so investors can exclude stocks/sectors and harvest specific lots; minimums are typically $100K-$1M+ with fees above index ETFs.
- **Cost:** broad index ETFs and index mutual funds cost as little as 0.01-0.05%; active mutual funds commonly cost 0.50-1.00%+ before any loads.

### Expense Ratios
Total annual cost as a percentage of AUM, deducted from fund returns. Includes management fees, administrative costs, and sometimes 12b-1 distribution fees. The expense ratio is the single most predictive factor of future fund performance — lower-cost funds consistently outperform higher-cost funds within the same category.

### Tracking Difference
The actual return gap between a fund and its benchmark index over a period. Tracking difference = Fund Return - Index Return. Expense ratio is a floor for tracking difference, but additional factors (securities lending income, sampling, cash drag, trading costs) can make tracking difference better or worse than the expense ratio.

### Tax Efficiency and the Creation/Redemption Mechanism
The general tax-efficiency hierarchy: ETFs > index mutual funds > actively managed mutual funds.

Authorized Participants (APs) create ETF shares by delivering a basket of the underlying securities in-kind, and redeem by receiving securities in-kind. These in-kind transfers do not trigger capital gains, so ETFs rarely distribute gains. Mutual funds must sell securities to meet redemptions, distributing the resulting gains to all remaining shareholders — taxable events even for buy-and-hold investors.

### Securities Lending Revenue
Funds can lend their holdings to short sellers in exchange for a fee. This revenue can partially or fully offset fund expenses, sometimes resulting in tracking difference better than the expense ratio. Large index funds are major securities lenders.

### Turnover Ratio
Measures how frequently a fund buys and sells its holdings. Higher turnover leads to more taxable capital gains distributions, higher transaction costs, and greater market impact. Typical turnover: index funds 3-10%, active funds 50-200%+.

### 12b-1 Fees and Loads
- **12b-1 fees:** annual distribution and marketing fees (0.25-1.0%), included in the expense ratio.
- **Front-end loads:** one-time sales charge at purchase (typically 3-5.75%), reducing the initial investment.
- **Back-end loads (CDSCs):** Contingent Deferred Sales Charges paid upon redemption, typically declining to 0% over 5-7 years.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Expense Drag (annual) | AUM × Expense Ratio | Annual cost of fund ownership |
| Tracking Difference | Fund Return - Index Return | Actual cost of indexing |
| Fee Impact (compounded) | FV = PV × (1 + r - ER)^n vs PV × (1 + r)^n | Long-term fee drag |
| Tax Cost Ratio | Pre-Tax Return - After-Tax Return | Tax efficiency measure |
| NAV | (Total Assets - Liabilities) / Shares Outstanding | Fund share value |

## Worked Examples

### Example 1: Long-Term Fee Impact
**Given:** $100,000 invested for 30 years at 8% gross return. Fund A: 0.03% expense ratio. Fund B: 0.75% expense ratio.
**Calculate:** Final values and fee drag for each fund
**Solution:**
Fund A: $100,000 × (1 + 0.08 - 0.0003)^30 = $100,000 × (1.0797)^30 = $997,914
Fund B: $100,000 × (1 + 0.08 - 0.0075)^30 = $100,000 × (1.0725)^30 = $816,430
Difference: $997,914 - $816,430 = $181,484

The 0.72% annual fee difference (0.75% - 0.03%) compounds to $181,484 over 30 years — approximately 18% of the low-cost fund's terminal value. This is wealth destroyed by fees for an identical gross return.

### Example 2: ETF vs Mutual Fund Tax Efficiency
**Given:** Identical S&P 500 portfolios, $100,000 invested for 20 years. Gross return 10%, expense ratio 0.03% for both, so both grow at 9.97% before distribution taxes. The ETF distributes $0 in capital gains (in-kind redemptions). The mutual fund distributes 2% of NAV in long-term capital gains each year-end. The investor is in the 20% LTCG bracket.

**Assumptions:** Distributions are taxed at 20% in the year received; the after-tax remainder is reinvested and adds to cost basis. Both positions are liquidated after year 20, with remaining unrealized gains taxed at 20%.

**Calculate:** After-tax liquidation values
**Solution:**

ETF — all gains deferred until sale:
- Pre-tax terminal value: $100,000 × (1.0997)^20 = $669,090
- Liquidation tax: ($669,090 - $100,000) × 20% = $113,818
- **After-tax value: $555,272**

Mutual fund — year-by-year, each year the position grows 9.97%, distributes 2% of NAV, and pays 20% tax on the distribution (equivalent to multiplying by 1.0997 × 0.996 each year):
- Pre-liquidation value after 20 years: $617,549
- Taxes paid on distributions along the way: $23,888 (on $119,442 of cumulative distributions)
- Cost basis: $100,000 + $95,554 reinvested after-tax distributions = $195,554
- Liquidation tax: ($617,549 - $195,554) × 20% = $84,399
- **After-tax value: $617,549 - $84,399 = $533,150**

The ETF's tax deferral advantage is $555,272 - $533,150 = **$22,122** over 20 years on this $100,000 investment — the cost of paying tax annually instead of letting the full balance compound until sale.

## Common Pitfalls
- Ignoring tracking difference — it can be worse than the expense ratio due to cash drag, sampling, and trading costs
- Not considering tax efficiency when comparing returns — pre-tax fund returns overstate what taxable investors actually keep
- Confusing NAV with market price for ETFs — ETFs can trade at premiums or discounts to NAV, especially in volatile markets or for illiquid underlying assets
- Overlooking securities lending income that offsets expenses — some index funds achieve tracking difference better than their expense ratio

## Cross-References
- **equities** (wealth-management plugin): equity fund selection and equity index tracking
- **fixed-income-sovereign** (wealth-management plugin): bond fund considerations (see also **fixed-income-corporate** (wealth-management plugin))
- **tax-efficiency** (wealth-management plugin): comprehensive after-tax investment analysis
- **asset-allocation** (wealth-management plugin): selecting vehicles within an asset allocation
- **factor-investing** (wealth-management plugin): evaluating factor ETFs and smart-beta funds on factor purity, turnover, capacity, and fee per unit of loading
## Running the script

```
uv run scripts/fund_vehicles.py
```

The PEP 723 header resolves the numpy dependency automatically. Alternatively run `python3 scripts/fund_vehicles.py` after `pip install numpy`.

- Bare run prints a demo covering fee impact, tracking error, NAV premium/discount, fund overlap, and ETF-vs-mutual-fund tax efficiency.
- `--verify` re-runs the demo computations and asserts the outputs match this skill's worked examples (prints PASS/FAIL, nonzero exit on mismatch).
- `--help` lists the available classes.

The file is primarily meant to be imported as a module, e.g. `from fund_vehicles import ExpenseAnalysis, TrackingAnalysis, TaxEfficiency`.


---

## SKILL: insurance-planning

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/insurance-planning` (MIT)
- Cuándo usarla: Integrate insurance into a financial plan: decide what risks to retain vs transfer, size life insurance with needs-based and human-life-value analysis, and evaluate disability, long-term care, annuity, and liability coverage. Use when the user asks 'how much life insurance do I need', 'term vs whole life', about 'disability insurance' (own-occupation vs any-occupation, group vs individual), 'long-term care' insurance or self-insuring LTC, 'should I buy an annuity' (SPIA, DIA, variable, indexed), or an 'umbrella policy' for liability protection. Also trigger on 'DIME method', 'life insurance calculator', 'whole life vs invest the difference', 'elimination period', 'benefit period', 'hybrid LTC policy', '1035 exchange', 'beneficiary review', or questions about insurance riders, surrender charges, or whether an advisor can recommend insurance products.

# Insurance Planning

## Core Concepts

### Risk Transfer vs Retention Framework
Insurance is a risk-financing decision, not an investment. Classify each exposure by frequency and severity:

- **High frequency / low severity** (minor repairs, small medical bills): retain. Self-fund through the emergency fund and cash flow; insuring these trades dollars with an insurer plus overhead. Raise deductibles to avoid paying for this layer.
- **Low frequency / high severity** (premature death, permanent disability, liability judgment, long-term care): transfer. These losses are rare but financially catastrophic, and the premium is small relative to the exposure.
- **High frequency / high severity**: avoid or mitigate the activity itself — insurance is expensive or unavailable.
- **Low frequency / low severity**: retain; do not bother insuring.
- **Retention capacity** grows with wealth: a household with large liquid assets can raise deductibles, extend elimination periods, and eventually self-insure entire categories (e.g., life insurance after financial independence, LTC above a threshold).

### Life Insurance Needs Analysis
Two standard approaches; use needs-based as primary and the others as cross-checks:

- **Needs-based (capital needs) approach:** Sum the survivors' actual needs — final expenses, debt payoff (including mortgage if the plan is to retire it), education funding, and the present value of ongoing income replacement — then subtract existing resources (liquid assets earmarked for survivors, existing coverage, survivor benefits). Coverage = total needs − available resources.
- **Human life value (HLV):** Present value of the insured's future after-tax earnings, net of self-consumption, over remaining working years. Tends to produce larger numbers; useful as a ceiling and in wrongful-death contexts.
- **DIME quick check:** Debt + final expenses, Income × years of replacement, Mortgage, Education. Fast but crude — the income multiple ignores the survivor's own earnings, investment returns on proceeds, and can double-count debt service already inside the income need.
- Reassess at every life event (birth, home purchase, divorce, business sale) — need is not static, and it generally declines as assets grow and horizons shorten (a "decreasing need against level coverage" glide path).

### Term vs Permanent
- **Term:** Pure death-benefit protection for a defined period (10/20/30 years). Cheapest per dollar of coverage; matches the temporary nature of most needs (children to independence, mortgage payoff, working years). Prefer guaranteed level premium and a convertibility rider (convert to permanent without new underwriting).
- **Permanent — whole life:** Guaranteed level premium, guaranteed cash value schedule, potential dividends (participating policies). Premiums roughly 8-15x term for the same face amount at typical issue ages (as of 2026 pricing; verify current quotes).
- **Permanent — universal life (UL):** Flexible premiums, interest-crediting on cash value; guaranteed-UL variants trade cash value for a lifetime death-benefit guarantee. Underfunded UL can lapse late in life exactly when needed — require in-force illustrations at reviews.
- **Permanent — variable life (VUL):** Cash value in market subaccounts; policyholder bears investment risk. VUL is a security — see the regulatory note below.
- **When permanent is actually warranted:** the need itself is permanent — estate liquidity for illiquid estates (business, real estate) and estate tax, often inside an ILIT; lifetime support for a special-needs dependent; business succession funding (buy-sell agreements, key person); equalizing inheritances. Permanent insurance as a *default* accumulation vehicle for someone who has not maxed tax-advantaged accounts is usually a mis-sale — "buy term and invest the difference" wins when the need is temporary.

### Disability Insurance
Disability during working years is more probable than death and destroys the plan's core asset: earning power.

- **Own-occupation vs any-occupation:** Own-occ pays if you cannot perform *your* occupation (critical for specialized professionals — surgeon, dentist); any-occ pays only if you cannot work in any reasonable occupation. Many policies are own-occ for 2 years, then any-occ.
- **Elimination period:** The waiting period before benefits begin (30-365 days; 90 is typical). Coordinate with the emergency fund — a larger cash reserve supports a longer elimination period and a lower premium.
- **Benefit period:** To age 65/67 is the standard for long-term disability (LTD); short benefit periods (2-5 years) leave the largest risk uncovered.
- **Group vs individual:** Group LTD is cheap but typically covers 60% of *base* salary (excluding bonus/commission), is capped, ends at job change, and is non-portable. Individual policies are portable, underwritten once, and can be own-occ with riders (residual/partial disability, cost-of-living adjustment, future increase option).
- **Taxation follows the premium payer:** employer-paid (or pre-tax) premiums produce *taxable* benefits; premiums paid by the individual with after-tax dollars produce *tax-free* benefits. A 60% gross replacement ratio from a taxable group plan can net to well under 50% of take-home pay.

### Long-Term Care (LTC)
- **Exposure:** Extended custodial care. Private-room nursing home costs run roughly $110,000-$130,000/year nationally (as of 2026; highly regional — verify current cost surveys). Typical need is 2-3 years; tail risk (dementia) is 5+ years.
- **Traditional LTC insurance:** Pure LTC coverage; premiums are not guaranteed and the industry has a history of large in-force rate increases. Choose inflation protection (3% compound) — a level benefit purchased at 55 is badly eroded by 85.
- **Hybrid (asset-based) policies:** Life insurance or annuity with an LTC rider — return-of-premium/death benefit if care is never needed, guaranteed premiums. Costlier per dollar of LTC benefit but eliminates use-it-or-lose-it and rate-increase risk; funded with a single premium or short pay, often via 1035 exchange from an old policy.
- **Self-insuring:** Plausible when liquid assets comfortably exceed roughly $2.5-3M per person (as of 2026 cost levels; verify against current regional care costs) *and* the plan survives a 4-5 year care event without impoverishing the healthy spouse. Between roughly $300K and that threshold is the classic insure zone.
- **Medicaid backstop caveat:** Medicaid pays for care only after assets are spent down to poverty levels, with a 5-year look-back on transfers, limited facility choice, and state estate recovery. It is a safety net, not a plan; do not present it as the default strategy for clients with meaningful assets.

### Annuities as Longevity Risk Transfer
Annuities are the mirror image of life insurance: they insure against living too long.

- **SPIA / DIA (income annuities):** Single-premium immediate annuities pay income now; deferred income annuities (including QLACs inside retirement accounts) start at a future age (e.g., 80-85), which is cheap pure longevity insurance. Simple, low-overhead, irreversible — mortality credits are the return source. Best fit: covering the gap between essential expenses and guaranteed income (Social Security, pension) for retirees without a pension.
- **Deferred variable / indexed annuities:** Accumulation products with optional income riders. Understand the cost stack before recommending: M&E charges, subaccount fund fees, and rider fees can total 2.5-3.5%/year on a VA; indexed annuities embed costs in caps/participation rates rather than explicit fees. Surrender schedules commonly run 5-10 years with charges starting at 7-10% (as of 2026; verify the specific contract).
- **When each fits:** income annuities fit the retiree flooring essential spending; deferred annuities with guarantees fit a narrower band (risk-averse investors who will actually use the rider) and are frequently oversold for the commission.
- **1035 exchange cautions:** IRC Section 1035 allows tax-free exchange of annuity-to-annuity and life-to-life/annuity/LTC. An exchange restarts the surrender schedule and may forfeit accrued rider benefits or old-contract guarantees — a new commission is not a reason to exchange. Exchanges of annuities are a recognized FINRA exam focus.

### Property, Casualty, and Umbrella Liability
- **Homeowners/auto:** Insure to full replacement cost (not market value) for the dwelling; raise liability limits to the maximum offered before buying umbrella; use deductibles consistent with the retention framework.
- **Umbrella liability:** Excess liability above home/auto limits. For HNW clients, size to at least net worth plus a measure of future income exposure; $1M-$5M is common, more for significant wealth. Premiums are modest — roughly $200-$400/year per $1M of coverage (as of 2026; verify current) — making it the cheapest large risk transfer in the plan. Confirm underlying-limit requirements so no gap exists between auto/home limits and the umbrella attachment point.
- **HNW-specific gaps:** domestic employees (workers' comp/EPLI), directors-and-officers exposure from board seats, valuable articles floaters, short-term rental of residences, teenage drivers, watercraft.

### Regulatory Intersection (brief)
- **Variable products (VUL, variable annuities) are securities:** recommendations fall under Reg BI for broker-dealers and fiduciary duty for RIAs; FINRA Rule 2330 imposes specific suitability, disclosure, and principal-review requirements for deferred variable annuity purchases and exchanges. Sellers need securities registration plus a state insurance license.
- **Fixed products (term/whole life, fixed and fixed-indexed annuities) are state-regulated insurance**, subject to state suitability/best-interest rules (NAIC model adopted in most states as of 2026). An investment adviser recommending or selling them generally needs a state insurance license; fee-only advisers who cannot sell should still analyze coverage and refer.
- See **investment-suitability** for the full suitability and Reg BI framework.

### Policy Review Cadence and Beneficiary Hygiene
- **Annual:** confirm coverage still matches needs; request in-force illustrations for UL/VUL; check group coverage after any job change; re-shop term at rate-class improvements (e.g., quit smoking).
- **Beneficiary hygiene:** review primary *and contingent* beneficiaries at every life event. Beneficiary designations override the will. Common failures: ex-spouse still named, estate named as beneficiary (creditor exposure, probate delay), minors named directly (court guardianship — use a trust or UTMA), and ILIT-owned policies where premiums are not being paid via proper Crummey notices.
- **Ownership check:** for estates above the federal exclusion, insured-owned policies are included in the gross estate; ownership by an ILIT keeps proceeds outside (see estate-gifting).

## Worked Examples

### Example 1: Needs-based life insurance for a dual-income household
**Given:** Spouse A earns $110,000; Spouse B earns $70,000. Mortgage balance $320,000; other debts $25,000. Two children, ages 4 and 7; education goal $120,000 per child. If A dies, the family needs $60,000/year of income replacement for 15 years (until the youngest is independent), discounted at a 3% real rate. Existing resources: $220,000 group life on A (2x salary), $150,000 of taxable investments the couple would apply to survivor needs.
**Calculate:** Recommended coverage on Spouse A.
**Solution:**
1. Final expenses and transition fund: **$15,000**.
2. Debt payoff: $320,000 + $25,000 = **$345,000**.
3. Education: 2 × $120,000 = **$240,000**.
4. Income replacement: PV of $60,000/year for 15 years at 3% real = $60,000 × [1 − 1.03^(−15)] / 0.03 = $60,000 × 11.938 ≈ **$716,000**.
5. Total needs = 15,000 + 345,000 + 240,000 + 716,000 = **$1,316,000**.
6. Less resources = $220,000 group + $150,000 investments = $370,000.
7. Net need = 1,316,000 − 370,000 = **$946,000 → buy a $1M 20-year level term policy** (round up; group coverage disappears at job change, so some advisors exclude it and would size at ~$1.2M).
8. DIME cross-check: Debt+final ($40K) + Income ($110K × 10 = $1.1M) + Mortgage ($320K) + Education ($240K) = $1.7M — higher because the income multiple ignores B's $70,000 income and investment returns on proceeds. Repeat the analysis for Spouse B: B's income also needs replacing, and a survivor-A household would need childcare B currently provides — dual-income households need coverage on both lives.

### Example 2: Term vs whole life decision
**Scenario:** A 35-year-old with the $1M need from Example 1 is quoted a 20-year level term policy at ~$700/year and a $1M whole life policy at ~$9,500/year (illustrative, as of 2026 pricing for a preferred non-smoker; verify current quotes). The agent presents whole life as "insurance you don't throw away."
**Analysis:**
1. The need is temporary: in 20 years the mortgage is largely paid, children are independent, and retirement assets should have grown — the insurable need declines toward zero.
2. The $8,800/year premium difference, invested at 7% for 20 years, grows to roughly $8,800 × 41.0 ≈ **$360,000** (future value of an ordinary annuity, factor [1.07^20 − 1]/0.07 ≈ 41.0) — money the family owns outright, versus whole life cash value that is typically well below cumulative premiums in the first decade.
3. Whole life would be defensible only if a *permanent* need existed: projected estate liquidity problem, special-needs child, or business succession funding. None applies here.
4. **Decision: buy the 20-year term with a conversion rider.** The rider preserves the option to convert to permanent later without underwriting if a permanent need (estate liquidity, health deterioration) emerges.

### Example 3: Disability coverage gap
**Given:** Salaried professional earning $10,000/month gross; take-home after taxes and benefits about $7,200/month; essential expenses $6,500/month. Employer-paid group LTD covers 60% of base salary with a $6,000/month cap and 90-day elimination period.
**Calculate:** The net replacement gap and the fix.
**Solution:**
1. Group benefit = 60% × $10,000 = $6,000/month — at the cap, so raises would not increase it.
2. Employer paid the premium, so benefits are **taxable**: at a ~25% effective tax rate, net benefit ≈ $6,000 × 0.75 = **$4,500/month**.
3. Gap vs essential expenses = $6,500 − $4,500 = **$2,000/month** — and any bonus income is uncovered entirely.
4. Fix: an individual supplemental DI policy of ~$2,000-$2,500/month, own-occupation, benefit to age 65, paid personally with after-tax dollars so benefits are **tax-free**. Keep the 90-day elimination period and hold a 3-month-plus emergency fund to bridge it.
5. Portability bonus: the individual policy survives a job change; the group policy does not.

## Common Pitfalls
- Buying permanent insurance as a default investment when the need is temporary — cash-value accumulation rarely beats "term plus invest the difference" for buyers who have not exhausted tax-advantaged accounts
- Sizing life insurance by rules of thumb ("10x income") without netting out the survivor's income, existing coverage, and assets — or ignoring the second spouse's insurable value entirely
- Relying on group life and group LTD as if permanent — both typically vanish at job change and group LTD caps and taxability shrink real replacement
- Ignoring the taxation asymmetry of disability benefits: pre-tax/employer-paid premiums mean taxable benefits precisely when income has stopped
- Buying LTC coverage without compound inflation protection, or presenting Medicaid as an LTC plan for clients with meaningful assets (spend-down, 5-year look-back, estate recovery)
- Recommending a 1035 exchange that restarts a surrender schedule or forfeits accrued rider benefits without a documented client-benefit rationale (FINRA Rule 2330 scrutiny for VAs)
- Treating an indexed annuity's cap/participation structure as "market upside with no downside" without disclosing that caps are repriceable and surrender charges apply
- Skipping umbrella liability for HNW clients — the cheapest protection in the plan against the largest liability exposures
- Beneficiary neglect: ex-spouses still named, no contingent beneficiary, minors named directly, or estate named (probate and creditor exposure); designations override the will
- Letting underfunded universal life drift toward late-life lapse — no in-force illustration requested for years

## Cross-References
- **emergency-fund** (wealth-management plugin): cash reserves set the retention layer — deductibles and disability elimination periods should be sized against the fund
- **debt-management** (wealth-management plugin): outstanding debts are a direct input to life insurance needs analysis
- **savings-goals** (wealth-management plugin): education and survivor-income goals quantified there feed the capital-needs calculation
- **tax-efficiency** (wealth-management plugin): taxation of disability benefits, annuity income, and life insurance proceeds drives structure and premium-payer decisions
- **estate-gifting** (wealth-management plugin): permanent life insurance for estate liquidity, ILIT ownership, and keeping proceeds out of the gross estate
- **financial-planning-workflow** (advisory-practice plugin): risk management review is a standard module of the comprehensive planning process
- **investment-suitability** (compliance plugin): suitability, Reg BI, and FINRA Rule 2330 obligations when recommending variable insurance products and annuity exchanges


---

## SKILL: investment-policy

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/investment-policy` (MIT)
- Cuándo usarla: Construct comprehensive Investment Policy Statements governing return objectives, risk tolerance, and portfolio constraints. Use when the user asks about building an IPS, setting return objectives, assessing risk tolerance, defining investment constraints, or establishing rebalancing and benchmark policies. Also trigger when users mention 'investment plan', 'policy portfolio', 'risk capacity vs willingness', 'spending rate for an endowment', 'foundation payout', 'manager selection criteria', or ask how to document their investment strategy.

# Investment Policy Statement Construction

## Core Concepts

### Investment Policy Statement (IPS)
The IPS is the governing document for all investment decisions. It specifies objectives (return and risk), constraints, asset allocation ranges, rebalancing policy, benchmark selection, and review schedule. Every portfolio action should be traceable back to IPS provisions.

### Return Objective
The required return is the rate that funds all future liabilities and goals.

- **Required return:** Solve for the discount rate that equates the present value of assets to the present value of future liabilities/spending needs.
- **Spending rate (endowments/foundations):** Typically set as a percentage of a rolling average of portfolio value (e.g., 5% of 3-year rolling average AUM). The required nominal return must cover spending + inflation + fees.
  - Required nominal return = spending rate + expected inflation + investment management fees

### Risk Tolerance
Risk tolerance has two dimensions that must be assessed independently:

- **Ability (financial capacity):** Determined by time horizon, wealth relative to liabilities, income stability, and liquidity needs. Longer horizons and greater surplus increase ability.
- **Willingness (psychological comfort):** Determined by behavioral assessment, past responses to losses, and stated preferences.
- **Conflict resolution rule:** When ability and willingness conflict, the lower of the two governs. A client with high ability but low willingness should be invested conservatively (with education to potentially raise willingness over time).

### Constraints (LLTU+U)
Five categories of constraints must be addressed in every IPS:

- **Liquidity:** Anticipated cash needs, emergency reserves, near-term spending requirements
- **Legal/Regulatory:** ERISA rules, trust provisions, foundation payout requirements, prudent investor standards
- **Time horizon:** Single-stage or multi-stage; longer horizons generally permit more risk
- **Tax:** Taxable vs tax-deferred vs tax-exempt status; impact on asset allocation and rebalancing
- **Unique circumstances:** ESG/SRI restrictions, concentrated stock positions, employer stock, legacy holdings, personal preferences

### Asset Allocation Policy
Strategic Asset Allocation (SAA) defines long-term target ranges:

- Example ranges: equity 50-70%, fixed income 20-40%, alternatives 0-15%
- Ranges permit tactical tilts within policy bounds
- Policy allocation is the primary driver of long-term returns (commonly cited as explaining ~90% of return variability across time)

### Rebalancing Policy
Specifies when and how the portfolio is brought back to target weights:

- **Calendar-based:** Rebalance at fixed intervals (quarterly, semi-annually)
- **Threshold-based (percentage-of-portfolio):** Rebalance when any asset class drifts beyond a specified band (e.g., ±5% absolute)
- **Combined:** Check at calendar intervals, rebalance only if thresholds are breached
- Wider bands reduce transaction costs but allow more drift; narrower bands maintain discipline but increase costs

### Benchmark Selection
An appropriate benchmark must be:

- **Investable:** Represents a viable passive alternative
- **Measurable:** Returns can be calculated on a timely basis
- **Specified in advance:** Chosen before the evaluation period, not after
- **Appropriate:** Matches the portfolio's asset classes, style, and risk profile
- **Owned by the manager:** The manager should agree the benchmark is fair

### Manager Selection Criteria (The Five Ps)
- **Philosophy:** Clear, coherent investment belief system
- **Process:** Systematic, repeatable approach consistent with philosophy
- **People:** Experienced, stable team with aligned incentives
- **Performance:** Track record evaluated against appropriate benchmark over full market cycles
- **Price:** Fees competitive relative to peers and value added

### Review Schedule
- **Annual IPS review:** Reassess objectives, constraints, and circumstances
- **Quarterly performance review:** Evaluate returns, attribution, and benchmark comparison
- **Trigger-based review:** Major life events, market dislocations, or material changes in circumstances

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Required nominal return | R_nom = spending_rate + inflation + fees | Endowment/foundation return target |
| Required return (goal-based) | Solve: PV(assets) = Σ [CF_t / (1+R)^t] | Individual required return |
| Real return from nominal | R_real ≈ R_nom - inflation | Converting between real and nominal |
| Spending amount (rolling avg) | Spend = rate × (1/3)(AUM_t + AUM_{t-1} + AUM_{t-2}) | Endowment annual distribution |
| Rebalancing trigger | |w_actual - w_target| > threshold | Threshold-based rebalancing |

## Worked Examples

### Example 1: IPS for a 45-year-old pre-retiree
**Given:** Age 45, current portfolio $2M, needs $100K/year (today's dollars) starting at age 65, life expectancy 90, inflation 2.5%, portfolio fees 0.5%.
**Calculate:** Required nominal return and the resulting allocation guidance.
**Solution:**
1. Time horizon: 20 years to retirement + 25 years in retirement = two-stage horizon.
2. At retirement, need $100K × (1.025)^20 = $163,862/year in nominal terms.
3. Required nest egg at 65 (25-year payout, assuming the retirement portfolio earns ~5% real, roughly 7.5% nominal at 2.5% inflation): the inflation-growing withdrawals are a level annuity in real terms, so N = $163,862 × [1 - 1.05^(-25)] / 0.05 = $163,862 × 14.094 ≈ **$2.31M** (in age-65 dollars).
4. Required return (no additional contributions): solve $2M × (1+R)^20 = $2.31M → R = (2.31/2.0)^(1/20) - 1 ≈ **0.7% nominal net of fees** (≈1.2% gross adding the 0.5% fee). That is below the 2.5% inflation assumption — the required real return is roughly -1.7%.
5. If the client also contributes $30K/year, the required return falls to essentially zero. Return needs alone do not compel an equity-heavy portfolio.
6. Allocation logic: ability to take risk is high (20-year accumulation horizon, assets large relative to the goal), so willingness governs the choice within a wide acceptable range. The required return is modest, but a 45-year total horizon, longevity beyond age 90, and inflation risk argue for substantial equities; if willingness is moderate, a 60/40 allocation is comfortable, and the client could de-risk to 40/60 and still expect to meet the goal. Document in the IPS that the equity allocation is held for inflation protection and longevity risk, not because the return target demands it.

### Example 2: Endowment spending policy
**Given:** $50M endowment, 5% spending rule on 3-year rolling average, expected inflation 2.5%, investment fees 0.5%.
**Calculate:** Required nominal return to maintain real value.
**Solution:**
1. Annual spending = 5% × $50M = $2.5M (assuming stable AUM at $50M).
2. To maintain purchasing power, the endowment must grow by at least inflation: 2.5%.
3. Required nominal return = spending rate + inflation + fees = 5.0% + 2.5% + 0.5% = **8.0%**.
4. This implies a growth-oriented allocation (e.g., 70% equity, 20% fixed income, 10% alternatives).
5. If 8% seems aggressive, the board may need to reduce spending rate or accept gradual real erosion.

## Common Pitfalls
- Setting return objectives higher than risk tolerance allows — the return target must be achievable within the risk budget
- Ignoring inflation in required return calculations — understating the true return hurdle
- Not revisiting the IPS when circumstances change — life events, market regimes, and regulatory changes demand updates
- Confusing risk ability with risk willingness — they are separate assessments and must be reconciled
- Setting constraints too rigid (reduces flexibility and increases costs) or too loose (provides no discipline)
- Choosing benchmarks after the fact to make performance look better
- Ignoring the interaction between constraints (e.g., tax considerations affecting asset allocation ranges)

## Cross-References
- **tax-efficiency** (wealth-management plugin): asset location and withdrawal sequencing affect IPS constraint section
- **performance-attribution** (wealth-management plugin): benchmark selection in IPS directly feeds performance evaluation
- **liquidity-management** (wealth-management plugin): liquidity constraint in IPS depends on cash flow analysis
- **savings-goals** (wealth-management plugin): return objectives often derived from goal-based planning
- **emergency-fund** (wealth-management plugin): emergency reserve requirement feeds into IPS liquidity constraint
- **client-review-prep** (advisory-practice plugin): IPS provides the reference framework for evaluating drift and suitability during reviews
- **financial-planning-workflow** (advisory-practice plugin): the financial plan informs and is codified in the investment policy statement
- **tax-loss-harvesting** (wealth-management plugin): IPS may specify TLH policy parameters (minimum loss threshold, approved replacement pairs)
- **estate-gifting** (wealth-management plugin): trust structures and multi-generational transfer objectives feed the IPS legal/regulatory and time-horizon constraints
- **retirement-decumulation** (wealth-management plugin): the IPS spending policy documents the withdrawal rate, guardrail rules, and rebalancing discipline used in decumulation


---

## SKILL: investment-proposal

- Fuente: `anthropics/financial-services` → `plugins/agent-plugins/meeting-prep-agent/skills/investment-proposal` (Apache-2.0)
- Cuándo usarla: Create professional investment proposals for prospective clients. Covers the firm's approach, proposed allocation, expected outcomes, and fee structure. Use when pitching new clients or presenting a new investment strategy. Triggers on "investment proposal", "prospect presentation", "pitch new client", "proposal for [client]", or "new client presentation".

# Investment Proposal

## Workflow

### Step 1: Prospect Context

Gather:
- **Prospect name** and household details
- **Current situation**: Existing advisor? Self-directed? What prompted the meeting?
- **Assets**: Estimated AUM, account types, current holdings (if shared)
- **Goals**: Retirement, wealth preservation, growth, income, education, estate
- **Risk tolerance**: Conservative, moderate, aggressive (or questionnaire score)
- **Constraints**: ESG preferences, concentrated stock, illiquidity needs
- **Fee sensitivity**: What are they paying now?
- **Competition**: Who else are they considering?

### Step 2: Proposal Structure

**I. About Our Firm** (1 page)
- Firm overview, history, AUM
- Investment philosophy (in plain English)
- Team bios (relevant to this client)
- Client service model (how often do we meet, who do they call)

**II. Understanding Your Needs** (1 page)
- Restate their goals and concerns — show you listened
- Key planning considerations identified in discovery
- What success looks like for them

**III. Proposed Investment Strategy** (2-3 pages)
- Recommended asset allocation with rationale
- How allocation maps to their goals and risk tolerance
- Investment vehicles (ETFs, mutual funds, individual securities, alternatives)
- Tax-aware strategy (asset location, tax-loss harvesting)

Proposed allocation:

| Asset Class | Allocation | Vehicle | Rationale |
|------------|-----------|---------|-----------|
| | | | |

**IV. Expected Outcomes** (1-2 pages)
- Projected growth scenarios (conservative, moderate, optimistic)
- Monte Carlo probability of meeting goals
- Income projections (if retirement or income-focused)
- Risk metrics (max drawdown, volatility)
- Comparison to current portfolio (if known)

**V. Fee Structure** (1 page)
- Advisory fee schedule (tiered if applicable)
- Underlying fund expenses
- Total all-in cost estimate
- How fees compare to industry averages
- Value proposition — what they get for the fee

**VI. Getting Started** (1 page)
- Account opening process
- Asset transfer timeline
- Transition plan (if moving from another advisor)
- First 90 days — what to expect
- Required documents and next steps

### Step 3: Customization

- Match the tone to the prospect (corporate executive vs. small business owner vs. retiree)
- If they have a concentrated stock position, address it directly
- If they're comparing you to robo-advisors, emphasize the planning and relationship value
- If they're price-sensitive, lead with total value and outcomes, not just fees

### Step 4: Output

- PowerPoint presentation (12-15 slides) with firm branding
- PDF leave-behind version
- One-page summary for follow-up email

## Important Notes

- The proposal should feel personalized, not templated — reference their specific situation
- Don't oversell performance — set realistic expectations and emphasize process
- Always include disclaimers (projections are hypothetical, past performance, etc.)
- The transition plan matters — clients fear the disruption of switching advisors
- Follow up within 48 hours with the proposal and a clear next step
- Compliance must review before presenting to prospects


---

## SKILL: investment-suitability

- Fuente: `JoelLewis/finance_skills` → `plugins/compliance/skills/investment-suitability` (MIT)
- Cuándo usarla: Assess investment suitability obligations under FINRA Rules 2111 and 2090 across all three suitability prongs. Use when the user asks about reasonable-basis, customer-specific, or quantitative suitability, product-specific concerns for complex products, leveraged ETFs, variable annuities, or alternatives, household-level suitability and concentration analysis, hold recommendations, or the institutional suitability exemption. Also trigger when users mention 'is this investment suitable', 'suitability questionnaire design', 'complex product due diligence', 'concentrated position in a client account', 'customer refused to provide their risk tolerance', or ask whether a recommendation fits a customer's profile. (For churning, turnover-ratio, and excessive-trading enforcement triggers, use sales-practices.)

# Investment Suitability

Regulatory status current as of June 2026 — verify effective dates, dollar thresholds, and pending rulemakings against current SEC/FINRA/FinCEN sources before advising.

## Core Concepts

### FINRA Rule 2111 — Suitability
The foundational rule requiring that a broker-dealer or associated person have a reasonable basis for believing a recommendation is suitable for the customer. Applies to recommendations of securities and investment strategies involving securities, including recommendations to hold. Three distinct obligations arise from Rule 2111:

### Three Suitability Obligations

**1. Reasonable-Basis Suitability (Rule 2111.05(a))**
The firm or associated person must perform reasonable diligence to understand the nature of the recommended security or strategy, including its risks, rewards, and features. This is a product-level obligation — the representative must understand what they are recommending before recommending it to anyone. A representative who does not understand a complex product cannot satisfy reasonable-basis suitability regardless of how well it might fit a particular customer.

**2. Customer-Specific Suitability (Rule 2111.05(b))**
The recommendation must be suitable for the particular customer based on that customer's investment profile. The investment profile includes, but is not limited to: age, other investments, financial situation and needs, tax status, investment objectives, investment experience, investment time horizon, liquidity needs, risk tolerance, and any other information the customer discloses.

**3. Quantitative Suitability (Rule 2111.05(c))**
The firm or associated person must have a reasonable basis for believing that a series of recommended transactions, even if each is individually suitable, is not excessive and unsuitable when taken together in light of the customer's investment profile. The former requirement that the broker have "actual or de facto control" over the account was removed by FINRA's 2020 amendments to Rule 2111 (Regulatory Notice 20-18; SR-FINRA-2020-007, effective June 30, 2020), aligning the obligation with Reg BI's Care Obligation — quantitative suitability now turns on the recommendations alone, without any control element. Key metrics: turnover ratio (annualized), cost-to-equity ratio, and use of in-and-out trading patterns. Generally, turnover ratios above 6 and cost-to-equity ratios above 20% raise presumptive concerns.

### FINRA Rule 2090 — Know Your Customer
Requires every member to use reasonable diligence to know and retain the essential facts concerning every customer and the authority of each person acting on the customer's behalf. This is the foundation that feeds suitability analysis — you cannot assess suitability without first knowing the customer. Essential facts include identity, financial status, investment objectives, and the nature and type of account.

### Suitability Profile Factors
The customer investment profile under Rule 2111 includes:
- **Age** — affects time horizon, risk capacity, and product suitability
- **Financial situation and needs** — income, net worth, liquid net worth, expenses, liabilities
- **Tax status** — marginal tax bracket, tax-deferred vs taxable accounts
- **Investment objectives** — capital preservation, income, growth, speculation
- **Investment time horizon** — short-term (<3 years), intermediate (3-10), long-term (>10)
- **Liquidity needs** — anticipated cash needs, emergency reserves
- **Risk tolerance** — willingness and capacity to bear losses
- **Investment experience** — familiarity with securities types, strategies, and risks
- **Other investments** — existing portfolio holdings, concentration risk, held-away assets

A customer may decline to provide profile information, but the firm must document the refusal and recognize that the more information withheld, the narrower the range of suitable recommendations.

### Product-Specific Suitability Concerns

**Complex Products:** FINRA Regulatory Notice 12-03 provides heightened suitability guidance for complex products (structured products, leveraged/inverse ETFs, hedge funds, non-traded REITs). Firms must perform heightened reasonable-basis diligence, develop targeted training, and consider whether enhanced customer-specific suitability review is needed.

**Leveraged and Inverse ETFs:** These products reset daily, meaning their performance over periods longer than one day can deviate significantly from the leveraged/inverse benchmark return. FINRA has flagged that these are generally unsuitable for buy-and-hold investors. Suitability analysis must account for the daily reset mechanism and its compounding effects.

**Variable Annuities:** Subject to FINRA Rule 2330, which imposes heightened suitability requirements. Before recommending a VA, the representative must consider: liquidity needs (surrender charges typically 5-8 years), tax status (tax-deferred growth is redundant in an IRA), subaccount investment options, rider costs and benefits, and whether a 1035 exchange is in the customer's interest.

**Options:** FINRA Rule 2360 requires account-level approval before options trading, with suitability assessed across strategy tiers (covered writing, spreads, uncovered writing, etc.). The Options Disclosure Document (ODD) must be delivered before account approval.

**Alternative Investments:** Private placements, hedge funds, and non-traded products present heightened suitability concerns due to illiquidity, complexity, high fees, and limited transparency. FINRA expects enhanced due diligence on the product issuer and heightened customer-specific suitability review.

### Household vs Account-Level Suitability
Suitability is assessed at the customer level, not the account level, but household context matters. A concentrated position in one account may be suitable if diversified across the household. However, firms must have a reasonable basis for knowing the household context — relying on assumptions about held-away assets without verification creates risk. FINRA expects firms to consider a customer's overall financial picture to the extent it is known or reasonably discoverable.

### The Hold Recommendation
Since the 2012 adoption of Rule 2111 (which extended suitability to recommended "investment strategies involving securities," including explicit recommendations to hold), a hold recommendation is subject to suitability obligations. This closed a longstanding gap under predecessor NASD Rule 2310, where representatives could avoid suitability review by recommending inaction. A hold recommendation on a concentrated or illiquid position must be evaluated against the customer's current profile.

### Institutional Suitability Exemption (Rule 2111.07)
The customer-specific suitability obligation may be modified for institutional accounts (as defined in FINRA Rule 4512(c)) if: (1) the firm has a reasonable basis to believe the institutional customer is capable of evaluating investment risks independently, and (2) the institutional customer affirmatively indicates it is exercising independent judgment. Both conditions must be met — the exemption is not automatic for all institutional clients.

### Reg BI's Elevation Beyond Suitability
Since June 30, 2020, broker-dealer recommendations to retail customers are governed by Regulation Best Interest (Reg BI), which imposes a higher standard than FINRA suitability. Reg BI's Care Obligation requires consideration of reasonably available alternatives and a cost-benefit analysis — obligations that go beyond traditional suitability. FINRA suitability remains relevant for institutional clients and as a component of the Reg BI framework. See the **reg-bi** skill for full Reg BI coverage.

### Enforcement Patterns
FINRA disciplinary actions frequently target:
- Recommending complex products without understanding them (reasonable-basis failures)
- Recommending concentrated positions to risk-averse or elderly customers
- Excessive trading in discretionary or de facto controlled accounts
- Failure to update customer profiles after material life changes
- Ignoring red flags (customer complaints, account losses inconsistent with stated objectives)
- VA exchanges that serve the representative's commission interest but not the customer's investment interest

## Worked Examples

### Example 1: Concentrated position recommended to a retiree
**Scenario:** A registered representative recommends that a 72-year-old retired client invest 60% of her $500,000 IRA in a single technology stock. The client's investment objective is listed as "income" with a "moderate" risk tolerance. She relies on the account for living expenses.
**Compliance Issues:** Customer-specific suitability violation. The recommendation creates concentration risk inconsistent with income objectives, moderate risk tolerance, short time horizon (income-dependent), and high liquidity needs. Age is a significant factor — the client has limited ability to recover from a loss.
**Analysis:** The representative should have recommended a diversified income-oriented portfolio consistent with the stated objectives. Even if the client expressed enthusiasm for the stock, the representative has an independent obligation to assess suitability and document the rationale. FINRA would likely view this as a customer-specific suitability violation and potentially a supervision failure if the firm lacked exception reporting for concentration.

### Example 2: Complex product recommended without adequate understanding
**Scenario:** A representative recommends a leveraged inverse ETF to a moderate-risk client as a "hedge" against market declines, suggesting the client hold it for six months. The representative cannot explain the daily reset mechanism or the compounding effects over multi-day holding periods.
**Compliance Issues:** Reasonable-basis suitability violation. The representative does not understand the product's key feature (daily reset) and is recommending a holding period inconsistent with the product's design. Additionally, customer-specific suitability is questionable for a moderate-risk investor.
**Analysis:** FINRA Regulatory Notice 09-31 specifically warns that leveraged/inverse ETFs that reset daily are typically unsuitable for retail investors who plan to hold them longer than one trading session. The representative's inability to explain the reset mechanism is a clear reasonable-basis failure. The firm should have product-specific training requirements and suitability guardrails for leveraged ETF recommendations.

### Example 3: Excessive trading in a discretionary account
**Scenario:** A representative with discretionary authority over a client's $200,000 account executes 150 trades over 12 months, generating $46,000 in commissions. The account's annualized turnover ratio is 8.2 and the cost-to-equity ratio is 23%. The client's objective is "growth" with a "moderate-to-aggressive" risk tolerance.
**Compliance Issues:** Quantitative suitability violation. The turnover ratio (8.2 > 6 threshold) and cost-to-equity ratio (23% > 20% threshold) both exceed presumptive thresholds for excessive trading. Since the 2020 amendments, no showing of control is required under Rule 2111.05(c) — the recommended (here, discretionary) transactions alone are evaluated.
**Analysis:** Even though individual trades may have been suitable, the pattern of trading is excessive in the aggregate. The account must generate returns exceeding 23% just to break even after costs — an unreasonable hurdle. FINRA would examine the excessive activity itself (quantitative metrics); control and scienter remain relevant only if regulators also pursue fraud-based churning charges under Rule 10b-5. The firm's supervision system should have flagged this through exception reporting on turnover and cost-to-equity ratios.

## Common Pitfalls
- Treating suitability as a one-time assessment at account opening — it must be reassessed with each recommendation and when circumstances change
- Confusing account-level suitability with customer-level suitability — the customer's full financial picture matters
- Recommending complex products without completing reasonable-basis diligence on the product
- Failing to document the rationale for recommendations, especially for higher-risk or concentrated positions
- Ignoring the hold recommendation obligation — advising a client to maintain a concentrated or unsuitable position is itself a recommendation
- Assuming institutional clients are automatically exempt from customer-specific suitability — both prongs of Rule 2111.07 must be satisfied
- Not updating customer profiles after life events (retirement, inheritance, divorce, job loss)
- Applying suitability standards when Reg BI's higher standard applies to retail customers
- Overlooking quantitative suitability in accounts with high activity but no single unsuitable trade
- Failing to consider tax status — recommending tax-deferred products (VAs) in already tax-deferred accounts (IRAs) without justification

## Cross-References
- **reg-bi** (compliance plugin): Higher standard for BD recommendations to retail customers; supersedes suitability for retail
- **know-your-customer** (compliance plugin): KYC obligations provide the customer profile that feeds suitability analysis
- **fiduciary-standards** (compliance plugin): IA fiduciary duty parallel; different standard, similar customer-interest focus
- **investment-policy** (wealth-management plugin): IPS constraints (time horizon, risk tolerance, liquidity) map directly to suitability factors
- **sales-practices** (compliance plugin): Churning/excessive trading enforcement overlaps with quantitative suitability
- **conflicts-of-interest** (compliance plugin): Compensation conflicts can drive unsuitable recommendations
- **tax-loss-harvesting** (wealth-management plugin): replacement securities selected during TLH must still satisfy suitability requirements
- **insurance-planning** (wealth-management plugin): variable insurance products and annuity exchanges recommended in planning trigger Reg BI and FINRA Rule 2330 obligations
- **private-placements** (compliance plugin): Reg D eligibility gates (accredited/qualified purchaser) and FINRA 5122/5123 filings that precede the suitability analysis for private offerings
- **equity-compensation** (wealth-management plugin): concentrated employer stock and insider status inform suitability of diversification, hedging, and lending recommendations


---

## SKILL: kanchi-dividend-review-monitor

- Fuente: `tradermonty/claude-trading-skills` → `skills/kanchi-dividend-review-monitor` (MIT)
- Cuándo usarla: Monitor dividend portfolios with Kanchi-style forced-review triggers (T1-T5) and convert anomalies into OK/WARN/REVIEW states without auto-selling. Use when users ask for 減配検知, 8-Kガバナンス監視, 配当安全性モニタリング, REVIEWキュー自動化, or periodic dividend risk checks.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/kanchi-dividend-review-monitor/` (openai.yaml, requirements.txt, build_review_queue.py)

# Kanchi Dividend Review Monitor

## Overview

Detect abnormal dividend-risk signals and route them into a human review queue.
Treat automation as anomaly detection, not automated trade execution.

## When to Use

Use this skill when the user needs:
- Daily/weekly/quarterly anomaly detection for dividend holdings.
- Forced review queueing for T1-T5 risk triggers.
- 8-K/governance keyword scans tied to portfolio tickers.
- Deterministic `OK/WARN/REVIEW` output before manual decision making.

## Prerequisites

Provide normalized input JSON that follows:
- `references/input-schema.md`

If upstream data is unavailable, provide at least:
- `ticker`
- `instrument_type`
- `dividend.latest_regular`
- `dividend.prior_regular`

## Non-Negotiable Rule

Never auto-sell based only on machine triggers.
Always create `WARN` or `REVIEW` evidence for human confirmation first.

## State Machine

- `OK`: no action.
- `WARN`: add to next check cycle and pause optional adds.
- `REVIEW`: immediate human review ticket + pause adds.

Use `references/trigger-matrix.md` for trigger thresholds and actions.

### Flat-dividend cadence caveat

When T6 is driven only by `freeze_flag` / latest regular dividend equal to prior regular dividend, treat it as a `WARN` for cadence confirmation, not as proof of dividend deterioration. Many quarterly dividend payers repeat the same dividend for several quarters between annual raise cycles. In reports, phrase this as “confirm next dividend-growth cadence / pause optional adds until checked” and avoid implying a cut or broken thesis unless T1/T2/T3/T4/T5 evidence also supports escalation.

## Monitoring Cadence

- Daily:
  - T1 dividend cut/suspension.
  - T4 SEC filing keyword scan (8-K oriented).
- Weekly:
  - T3 proxy credit stress checks.
- Quarterly:
  - T2 coverage deterioration and T5 structural decline scoring.

## Workflow

### 1) Normalize input dataset

Collect per ticker fields in one JSON document:
- Dividend points (latest regular, prior regular, missing/zero flag).
- Coverage fields (FCF or FFO or NII, dividends paid, ratio history).
- Balance-sheet trend fields (net debt, interest coverage, buybacks/dividends).
- Filing text snippets (especially recent 8-K or equivalent alert text).
- Operations trend fields (revenue CAGR, margin trend, guidance trend).

Use `references/input-schema.md` for field definitions
and sample payload.

### 2) Run the rule engine

Run:

```bash
python3 skills/kanchi-dividend-review-monitor/scripts/build_review_queue.py \
  --input /path/to/monitor_input.json \
  --output-dir reports/
```

The script maps each ticker to `OK/WARN/REVIEW` based on T1-T5.
Output files are saved to the specified directory with dated filenames (e.g., `review_queue_20260227.json` and `.md`).

### 3) Prioritize and deduplicate

If multiple triggers fire:
- Keep all findings for audit trail.
- Escalate final state to highest severity only.
- Store trigger reasons as single-line evidence.

### 4) Generate human review tickets

For each `REVIEW` ticker, include:
- Trigger IDs and evidence.
- Suspected failure mode.
- Required manual checks for next decision.

Use `references/review-ticket-template.md` output format.

## SEC Filing Guardrail

When implementing live SEC fetchers:
- Include a compliant `User-Agent` string (name + email).
- Use caching and throttling.
- Respect SEC fair-access guidance.
- In scheduled portfolio reviews where upstream filing snippets are empty, use SEC `company_tickers.json` plus `https://data.sec.gov/submissions/CIK##########.json` to enumerate recent 8-K / 8-K/A filings for each holding, then scan primary filing documents for the T4 keyword family (`Item 4.02`, non-reliance, restatement, material weakness, SEC investigation, subpoena, going concern, auditor resignation, internal control). Record the scan window, recent 8-K count, and whether hits were found. Treat "no keyword hits" as a narrow T4 scan result, not a full governance clearance.

## Output Contract

Always return:
1. Queue JSON with summary counts and ticker-level findings.
2. Markdown dashboard for quick triage.
3. List of immediate `REVIEW` tickets.

## Multi-Skill Handoff

- Consume ticker universe and baseline assumptions from `kanchi-dividend-sop`.
- Feed `REVIEW` results back to `kanchi-dividend-sop` for re-underwriting and position-size review.
- Share account-type context with `kanchi-dividend-us-tax-accounting` when risk events imply account relocation decisions.

## Resources

- `scripts/build_review_queue.py`: local rule engine for T1-T5.
- `scripts/tests/test_build_review_queue.py`: unit tests for T1-T5 and report rendering.
- `references/trigger-matrix.md`: trigger definitions, cadence, and actions.
- `references/input-schema.md`: normalized input schema and sample JSON.
- `references/review-ticket-template.md`: standardized manual-review ticket layout.

### Referencia: references/input-schema.md

# Input Schema

Use this normalized JSON schema for `build_review_queue.py`.

## Required Top-Level Fields

- `as_of`: ISO date string.
- `holdings`: array of ticker records.

## Optional Top-Level Fields

- `schema_version`: integer emitted by `kanchi-dividend-sop`
  `build_entry_signals.py` (current: 2). Consumers MUST tolerate unknown
  future versions and unknown fields rather than failing (MJ-10).

## Holding Object

```json
{
  "ticker": "ABC",
  "instrument_type": "stock",
  "dividend": {
    "latest_regular": 0.50,
    "prior_regular": 0.52,
    "is_missing": false,
    "flags": {
      "cut_flag": false,
      "freeze_flag": false,
      "special_dividend_flag": false,
      "variable_policy_flag": false
    }
  },
  "cashflow": {
    "fcf": 1200.0,
    "ffo": null,
    "nii": null,
    "dividends_paid": 900.0,
    "coverage_ratio_history": [0.72, 0.85]
  },
  "balance_sheet": {
    "net_debt_history": [3000.0, 3400.0, 3800.0],
    "interest_coverage_history": [4.6, 3.8, 2.9]
  },
  "capital_returns": {
    "buybacks": 250.0,
    "dividends_paid": 900.0,
    "fcf": 1200.0
  },
  "filings": {
    "recent_text": "8-K filed. No restatement language.",
    "latest_8k_text": "Item 4.02 non-reliance ...",
    "headlines": ["Company files 8-K", "Audit committee review announced"]
  },
  "operations": {
    "revenue_cagr_5y": -1.2,
    "margin_trend": "down",
    "guidance_trend": "down",
    "dividend_growth_stalled": true
  }
}
```

## Minimal Viable Input

If upstream data is partial, include at least:
- `ticker`
- `instrument_type`
- `dividend.latest_regular`
- `dividend.prior_regular`

The rule engine will still run and skip unavailable triggers.

### Referencia: references/review-ticket-template.md

# Review Ticket Template

Use this template for each `REVIEW` ticker.

```markdown
# REVIEW Ticket: [Ticker]

## Trigger Summary
- Final status: REVIEW
- Trigger hits: [T1,T4]
- Generated at:

## Evidence (One Line Each)
- T1:
- T2:
- T3:
- T4:
- T5:

## Manual Checks Required
1. Read latest filing/release primary source text.
2. Confirm scope and duration of the issue.
3. Assess impact on dividend continuity.
4. Recalculate payout/coverage assumptions.
5. Decide portfolio action (hold / trim / exit review).

## Decision Log
- Decision:
- Rationale:
- Owner:
- Due date:
```

### Referencia: references/trigger-matrix.md

# Trigger Matrix (T1-T5)

Apply these rules to route tickers into `OK`, `WARN`, or `REVIEW`.

## Severity Policy

- `OK`: no forced action.
- `WARN`: queue for next checkpoint and pause optional adds.
- `REVIEW`: immediate human review ticket and pause adds.

## Trigger Definitions

| Trigger | Core signal | Default machine rule | Frequency | Default action |
|---|---|---|---|---|
| T1 | Dividend cut or suspension | `latest_regular < prior_regular * 0.99` OR `latest_regular <= 0` OR missing dividend feed | Daily | `REVIEW` |
| T2 | Coverage deterioration | `denominator <= 0` with positive dividends OR coverage ratio `>1.0` for 2 periods | Quarterly | `WARN/REVIEW` |
| T3 | Credit stress proxy | Net debt rising 3 periods + weakening interest coverage and/or stretched capital return | Weekly + Quarterly confirm | `WARN/REVIEW` |
| T4 | Governance/accounting red flag | Filing text hits Item 4.02, non-reliance, restatement, material weakness, SEC investigation | Daily | `REVIEW` |
| T5 | Structural decline | 2+ simultaneous negatives: revenue CAGR <0, margin downtrend, guidance downtrend, stalled dividend growth | Quarterly | `WARN/REVIEW` |
| T6 | Dividend-policy change (WS-1 basis flags) | `cut_flag` OR `variable_policy_flag` → `REVIEW`; `freeze_flag` OR `special_dividend_flag` → `WARN` | Daily | `WARN/REVIEW` |

T6 consumes the WS-1 `dividend_basis` flags emitted by
`kanchi-dividend-sop/build_entry_signals.py` (schema v2+). Flags are read
from `dividend.flags` (preferred) or directly off `dividend`. A top-level
`schema_version` and any unknown fields are ignored, so a newer upstream
schema cannot silently break this monitor.

## Denominator Mapping For T2

| Instrument | Denominator |
|---|---|
| Stock | FCF (`CFO - CapEx`) |
| REIT | FFO/AFFO |
| BDC | NII |
| ETF | Use holdings-level quality proxies if fund-level coverage is unavailable |

## Escalation Rule

If multiple triggers fire, keep all findings and set final state to highest severity:
- `OK < WARN < REVIEW`.

Within T2 itself, sustained breach (`>1.0` for 2 periods) takes priority over single-period breach.


---

## SKILL: kanchi-dividend-sop

- Fuente: `tradermonty/claude-trading-skills` → `skills/kanchi-dividend-sop` (MIT)
- Cuándo usarla: Convert Kanchi-style dividend investing into a repeatable US-stock operating procedure. Use when users ask for かんち式配当投資, dividend screening, dividend growth quality checks, PERxPBR adaptation for US sectors, pullback limit-order planning, or one-page stock memo creation. Covers screening, deep dive, entry planning, and post-purchase monitoring cadence.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/kanchi-dividend-sop/` (openai.yaml, requirements.txt, build_entry_signals.py, build_sop_plan.py, dividend_basis.py, event_scanner.py, fmp_client.py, payout_safety.py, thresholds.py, verdict.py)

# Kanchi Dividend Sop

## Overview

Implement Kanchi's 5-step method as a deterministic workflow for US dividend investing.
Prioritize safety and repeatability over aggressive yield chasing.

## When to Use

Use this skill when the user needs:
- Kanchi-style dividend stock selection adapted for US equities.
- A repeatable screening and pullback-entry process instead of ad-hoc picks.
- One-page underwriting memos with explicit invalidation conditions.
- A handoff package for monitoring and tax/account-location workflows.

## Prerequisites

### API Key Setup

The entry signal script requires FMP API access:

```bash
export FMP_API_KEY=your_api_key_here
```

### Input Sources

Prepare one of the following inputs before running the workflow:
1. Output from `skills/value-dividend-screener/scripts/screen_dividend_stocks.py`.
2. Output from `skills/dividend-growth-pullback-screener/scripts/screen_dividend_growth_rsi.py`.
3. User-provided ticker list (broker export or manual list).

#### Expected JSON Input Format

When using `--input`, provide JSON in one of these formats:

```json
{
  "profile": "balanced",
  "candidates": [
    {"ticker": "JNJ", "bucket": "core"},
    {"ticker": "O", "bucket": "satellite"}
  ]
}
```

Or simplified:

```json
{
  "tickers": ["JNJ", "PG", "KO"]
}
```

The optional `value-dividend-screener` and
`dividend-growth-pullback-screener` handoffs use `stocks[].symbol`.
Both `build_sop_plan.py --input` and `build_entry_signals.py --input`
accept that shape directly, as well as the native `candidates[].ticker` and
`tickers[]` shapes above.

For deterministic artifact generation, provide tickers to:

```bash
python3 skills/kanchi-dividend-sop/scripts/build_sop_plan.py \
  --tickers "JNJ,PG,KO" \
  --output-dir reports/
```

For Step 5 entry timing artifacts. **`--yield-floor` is mandatory** — it is
the Step-1 yield gate; without it every row fail-safes to `STEP1-RECHECK`
(a row can never reach a PASS tier without Step 1). Pass `--profile` /
`--safety-bias` for run_context, and `--events-json` for the Step 4b scan
(absent ⇒ every row is treated as `SKIPPED` and a TRIGGERED name is capped
to `HOLD-REVIEW` — never silently clean):

```bash
python3 skills/kanchi-dividend-sop/scripts/build_entry_signals.py \
  --tickers "JNJ,PG,KO" \
  --alpha-pp 0.5 \
  --yield-floor 3.0 \
  --profile balanced --safety-bias medium \
  --events-json reports/kanchi_events_2026-05-17.json \
  --output-dir reports/
```

## Workflow

### 1) Define mandate before screening

Collect and lock the parameters first:
- Objective: current cash income vs dividend growth.
- Max positions and position-size cap.
- Allowed instruments: stock only, or include REIT/BDC/ETF.
- Preferred account type context: taxable vs IRA-like accounts.

Load `references/default-thresholds.md` and apply baseline
settings unless the user overrides.

### 2) Build the investable universe

Start with a quality-biased universe:
- Core bucket: long dividend growth names (for example, Dividend Aristocrats style quality set).
- Satellite bucket: higher-yield sectors (utilities, telecom, REITs) in a separate risk bucket.

Use explicit source priority for ticker collection:
1. `skills/value-dividend-screener/scripts/screen_dividend_stocks.py` output (FMP/FINVIZ).
2. `skills/dividend-growth-pullback-screener/scripts/screen_dividend_growth_rsi.py` output.
3. User-provided broker export or manual ticker list when APIs are unavailable.

Return a ticker list grouped by bucket before moving forward.

### 3) Apply Kanchi Step 1 (yield filter with trap flag)

Primary rule:
- Step-1 yield = the **regular forward yield** = `latest_declared_regular
  dividend × cadence-implied frequency / price` (WS-1 `dividend_basis.py`).
  Never use `profile.lastDividend` / TTM — it lags the latest declared raise
  (defect D5) and silently bundles specials (D4).
- Apply the profile floor (income-now 4.0% / balanced 3.0% / growth-first
  1.5%) to the **regular** yield only.

Trap & freshness controls (machine-emitted by `dividend_basis.py`):
- `special_dividend_flag` → exclude specials; report regular vs ttm yield.
- `variable_policy_flag` → `FAIL` (CALM-style; not an income base).
- `cut_flag` → `FAIL`; `suspension_flag` → `FAIL`.
- `freeze_flag` → `HOLD-REVIEW` (income cash-cow exception decided in
  Step 8 synthesis only if safety is clean & unblocked).
- **Data Freshness Gate**: if the regular yield is within ±0.20pp of the
  floor (`floor_borderline`) and the latest declared dividend is not
  confirmed from an authoritative source, emit `STEP1-RECHECK` — **never a
  hard FAIL** (this is the CFR D5 fix).

### 4) Apply Kanchi Step 2 (growth and safety) — sector-dispatched

Safety is **sector-specific** — a uniform GAAP/FCF triad mis-judges banks
(FCF meaningless) and regulated utilities (FCF structurally negative).
Use `references/sector-step2-modules.md`; the deterministic dispatch is
`scripts/payout_safety.py`.

- Always compute the **payout triad**: GAAP-EPS payout, Adjusted-EPS
  payout, FCF payout. The safety verdict uses **Adjusted-EPS + FCF**
  (consumer), or the sector module (bank / utility / insurer).
- `adjusted_eps_source = UNAVAILABLE` ⇒ cap `HOLD-REVIEW` (fail-safe;
  never a silent PASS).
- GAAP↔Adjusted EPS divergence > 25% ⇒ Step-4 one-off flag.
- A merger **completed within 4 quarters** presumes GAAP EPS is distorted
  ⇒ force the adjusted path or `HOLD-REVIEW` (FITB/Comerica golden case).
- Regulated utilities: **negative FCF is not an auto-FAIL** — judge on
  FFO/debt + allowed ROE + rate-case + equity-issuance risk.

When trend is mixed but not broken, classify as `HOLD-REVIEW` instead of
hard reject.

### 5) Apply Kanchi Step 3 (valuation) with US sector mapping

Use `references/valuation-and-one-off-checks.md` and apply
sector-specific valuation logic:
- Financials: `PER x PBR` can remain primary.
- REITs: use `P/FFO` or `P/AFFO` instead of plain `P/E`.
- Asset-light sectors: combine forward `P/E`, `P/FCF`, and historical range.

Always report which valuation method was used for each ticker.

### 6) Apply Kanchi Step 4 (one-off event filter)

Reject or downgrade names where recent profits rely on one-time effects:
- Asset sale gains, litigation settlement, tax effect spikes.
- Margin spike unsupported by sales trend.
- Repeated "one-time/non-recurring" adjustments.

Record one-line evidence for each `FAIL` to keep auditability.

### 6b) Apply Kanchi Step 4b (forward structural-event scan)

Step 4 is backward-looking; Step 4b catches *pending/recent* structural
events (the MKC-Unilever miss, D3). For each surviving candidate, run a
WebSearch + issuer-IR/SEC check using the **source hierarchy**: issuer IR
→ SEC filing (8-K/10-Q/10-K/proxy/S-4) → exchange/company deck →
reputable wire → finance portals (secondary only). Record findings into a
curated events JSON and pass it via `build_entry_signals.py --events-json`.

- Only a **major structural event** caps the verdict to `HOLD-REVIEW`
  (tx > 10% mcap, share issuance > 10–20%, leverage +0.5x EBITDA,
  control/listing/HQ change, merger-of-equals / RMT / spin-off / large
  asset sale, dividend/rating/leverage-policy change, sector-specific
  materiality, or rolling-24m cumulative M&A > 15% mcap). Minor bolt-ons
  are a CAUTION note only.
- **Pessimistic cap**: `FAILED-DEGRADED` / `SKIPPED` / `NO_EVENT_FOUND`
  on a Step-5 TRIGGERED name ⇒ `HOLD-REVIEW` + **T1 BLOCKED**. WebSearch
  unavailable (web app / offline) is treated the same — never a silent
  skip. `CLEAN_CONFIRMED` (primary source checked) is stronger than
  `NO_EVENT_FOUND` (search only).

### 7) Apply Kanchi Step 5 (buy on weakness with rules)

Set entry triggers mechanically:
- Yield trigger: current yield above 5y average yield + alpha (default `+0.5pp`).
- Valuation trigger: target multiple reached (`P/E`, `P/FFO`, or `P/FCF`).

Execution pattern:
- Split orders: `40% -> 30% -> 30%`.
- **Pre-order blockers**: if a candidate has any unresolved
  `pre_order_blockers[]` (from WS-1/2/3 — variable/cut/suspension,
  adjusted-EPS-unavailable, GAAP/Adj divergence, bank credit, utility
  FFO/debt, event-scan failed/skipped, stale dividend, …) OR
  `t1_blocked` is true, the first tranche is **blocked or downsized to a
  ≤20% tracking tranche** — not 40%.
- **Sector cluster risk**: when ≥ `SECTOR_CLUSTER_WARN_COUNT` same-sector
  names pass (e.g. many small banks share one macro beta), emit a
  portfolio-level `CLUSTER-RISK` warning.
- Require one-sentence sanity check before each *unblocked* add: "thesis
  intact vs structural break".

### 8) Produce standardized outputs

Always produce:
1. Screening table with the **actionable verdict tier**: `CLEAN-PASS`,
   `PASS-CAUTION`, `CONDITIONAL-PASS`, `HOLD-REVIEW`, `STEP1-RECHECK`,
   `FAIL` (synthesized by `verdict.py` from Step 1 + Step 2 + Step 4b +
   blockers). Include evidence per row.
2. One-page stock memo (use `references/stock-note-template.md`) with the
   per-ticker **provenance block** (price/dividend/payout/event sources,
   `unresolved_blockers`, `evidence_refs[]`).
3. Limit-order plan with split sizing, blocker gate, and invalidation.
4. Top-level **run_context** (profile, yield_floor_pct, safety_bias,
   universe_source, excluded_asset_types) so a 3%-run result is never
   silently reused inside a 4%-run.

## Output

Return and/or generate:
1. SOP screening summary in markdown.
2. Underwriting memo set based on
`references/stock-note-template.md`.
3. Optional plan artifact file generated by
`skills/kanchi-dividend-sop/scripts/build_sop_plan.py` in `reports/`.
4. Optional Step 5 entry-signal artifacts generated by
`skills/kanchi-dividend-sop/scripts/build_entry_signals.py` in `reports/`.

## Cadence

Use this minimum rhythm:
- Weekly (15 min): check dividend and business-news changes only.
- Monthly (30 min): rerun screening and refresh order levels.
- Quarterly (60 min): deep safety review using latest filings/earnings.

## Multi-Skill Handoff

Run this skill first, then hand off outputs:
1. To `kanchi-dividend-review-monitor` for daily/weekly/quarterly anomaly detection.
2. To `kanchi-dividend-us-tax-accounting` for account-location and tax classification planning.

## Guardrails

- Do not issue blind buy calls without Step 4, Step 4b and safety checks.
- Do not treat high yield as value before validating coverage quality.
- Use the **regular** forward yield for Step 1, never a special/TTM-inclusive
  figure; near-floor + unconfirmed ⇒ `STEP1-RECHECK`, not FAIL.
- A failed/skipped event scan on a TRIGGERED name ⇒ `HOLD-REVIEW` + T1
  blocked. Never silently skip Step 4b.
- Keep assumptions explicit; `adjusted_eps`/data missing ⇒ fail-safe
  `HOLD-REVIEW`, never silent PASS.

## Resources

- `scripts/thresholds.py`: **single source of truth** for all SOP
  thresholds + `SCHEMA_VERSION` (downstream schema-evolution guard).
- `scripts/dividend_basis.py`: WS-1 regular/special/variable/freeze/cut +
  Data Freshness Gate engine (pure, offline).
- `scripts/payout_safety.py`: WS-2 sector-aware GAAP/Adjusted/FCF payout
  triad + completed-merger linkage.
- `scripts/event_scanner.py`: WS-3 isolated forward/recent corporate-action
  scanner + materiality gate + pessimistic cap.
- `scripts/verdict.py`: WS-5 actionable-tier synthesis + run_context +
  evidence_ref helpers.
- `scripts/build_entry_signals.py`: orchestrator (Step 5 targets + WS-1/2/3/5
  integration). Flags: `--yield-floor`, `--events-json`, `--profile`,
  `--safety-bias`, `--universe-source`.
- `scripts/build_sop_plan.py`: deterministic SOP plan scaffold generator.
- `scripts/tests/test_golden_p0.py`: **P0 merge gate** — end-to-end frozen
  verdicts for CALM/ORI/CMCSA/MKC/CFR/cut (run via `scripts/run_all_tests.sh`).
- `references/default-thresholds.md`: human-readable threshold mirror.
- `references/sector-step2-modules.md`: Step 2 safety indicators by sector.
- `references/valuation-and-one-off-checks.md`: Step 3 valuation + Step 4 one-off.
- `references/stock-note-template.md`: one-page memo + provenance block.


## Shared FMP client

FMP data access uses the bundled generated `scripts/fmp_client.py`. Existing CLI
key/environment precedence, financial calculations and successful output shapes
are preserved. The migrated paths use stable endpoints only; a denied or failed
stable request does not fall back to retired v3 URLs. The shared client masks raw
and URL-encoded key echoes, retries malformed JSON once, and retries a 429 once
with a 60-second wait before stopping on a repeated rate limit. FINVIZ, where
used, remains a separate client.

The Python client retains `sleep_seconds`, `timeout` and `api_calls`. Sleep now
sets the minimum interval between requests; accounting includes retried HTTP
responses. Quote/profile retrieval remains one symbol per request.

### Referencia: references/default-thresholds.md

# Default Thresholds

Use these defaults when users do not provide custom risk settings.

## Baseline (US Stock-Focused)

| Category | Metric | Default | Interpretation |
|---|---|---:|---|
| Yield | Forward dividend yield | >= 3.5% | Kanchi Step 1 core filter |
| Yield trap | Extreme yield flag | >= 8.0% | Force deep dive before pass |
| Growth | Revenue CAGR (5y) | > 0% | Basic business expansion check |
| Growth | EPS CAGR (5y) | > 0% | Earnings trend health |
| Dividend trend | Dividend growth (5y) | Non-declining | Allow flat only with strong safety |
| Safety | EPS payout ratio | <= 70% | `70-85%` = caution |
| Safety | FCF payout ratio | <= 80% | `>100%` = high risk |
| Balance sheet | Net debt trend | Not persistently rising | Rising 3 periods = warning |
| Balance sheet | Interest coverage | >= 3.0x | `<2.5x` = caution |
| Entry trigger | Yield alpha vs 5y average | +0.5pp | Default Kanchi Step 5 pullback threshold |

## Instrument-Specific Notes

Use these denominator replacements for coverage checks:

| Instrument type | Primary denominator | Notes |
|---|---|---|
| Stock | FCF | Use `CFO - CapEx` |
| REIT | FFO/AFFO | Prefer AFFO if available |
| BDC | NII | Compare NII with distribution |
| ETF | Fund-level distribution coverage unavailable in many cases | Focus on methodology and holdings quality |

## Objective Tuning

Apply profile-specific adjustments:

| Profile | Yield floor | Safety bias | Notes |
|---|---:|---|---|
| Income now | 4.0% | Tight safety checks | Avoid overconcentration in one high-yield sector |
| Balanced | 3.0-3.5% | Medium | Blend current income and dividend growth |
| Growth first | 1.5-2.5% | High quality first | Accept lower initial yield for higher dividend CAGR |

## Step 5 Alpha Tuning

Use this range for yield-trigger alpha:
- Stable mega-cap compounders: `+0.3pp`.
- Default baseline: `+0.5pp`.
- Higher-volatility names: `+0.8pp` to `+1.0pp`.

## Entry Signal Interpretation

When using `build_entry_signals.py`, interpret signals as follows:

| Signal | Meaning | Action |
|---|---|---|
| TRIGGERED | Current price <= buy target price | Ready for first tranche (40%) if thesis intact |
| WAIT | Current price > buy target price | Monitor; set limit order at buy target |
| ASSUMPTION-REQUIRED | Missing data (yield history or dividend) | Manual research needed before entry |

### Drop Needed Percentage

- `0%`: Price already at or below target.
- `1-10%`: Near entry zone; consider scaling in if pullback accelerates.
- `>10%`: Significant gap; wait for pullback or reassess target.

## Portfolio Constraints

Use these as practical defaults:
- Max positions: `15-30`.
- Max single position at cost: `<= 8%`.
- Max sector exposure: `<= 25%`.
- High-yield bucket (REIT/telecom/utilities combined): `<= 35%`.

Override only when user explicitly chooses a different policy.

### Referencia: references/sector-step2-modules.md

# Sector-Specific Step 2 Modules (WS-4)

Step 2 (growth & safety) is sector-dispatched. This file holds the
**Step 2 safety indicators by sector**. It is the companion to
`valuation-and-one-off-checks.md`, which owns **Step 3 valuation** and
**Step 4 one-off** logic. Responsibility boundary (MN-2):

| Concern | Owner file |
|---|---|
| Step 2 safety indicators by sector | `sector-step2-modules.md` (this file) |
| Step 3 valuation mapping | `valuation-and-one-off-checks.md` |
| Step 4 backward one-off checklist | `valuation-and-one-off-checks.md` |
| Step 4b forward structural-event scan | `event_scanner.py` + SKILL.md Step 4b |

The deterministic thresholds are the SSOT in `scripts/thresholds.py`; the
numbers quoted below are human-readable mirrors. The script
`scripts/payout_safety.py` implements the dispatch.

## Why a uniform triad fails

FCF payout is the right anchor for consumer/industrial cash-cows, but:

- **Banks**: FCF is not a meaningful concept; capital adequacy and credit
  quality govern dividend safety.
- **Regulated utilities**: FCF is *structurally negative* (rate-base capex
  funded by debt/equity, recovered through rates). Auto-FAIL on negative
  FCF wrongly rejects healthy regulated names — this was the income-now vs
  balanced inconsistency in the 2026-05 runs.
- **Insurers**: GAAP earnings are noisy; statutory capital, reserve
  development and the combined ratio govern dividend capacity.

## Consumer / Industrial / Communication / default

Primary: **Adjusted-EPS payout + FCF payout**.

- Adjusted-EPS payout ≤ 70% PASS; 70–85% CAUTION; > 85% FAIL.
- FCF payout ≤ 80% PASS; > 100% FAIL.
- GAAP↔Adjusted EPS divergence > 25% ⇒ Step-4 one-off flag (MKC de Mexico
  non-cash remeasurement gain is the golden case).
- `adjusted_eps_source = UNAVAILABLE` ⇒ cap HOLD-REVIEW (never silent PASS).

## Banks

Primary: **EPS payout + capital + credit trend** (FCF ignored).

| Indicator | Caution / blocker condition |
|---|---|
| CET1 ratio | missing ⇒ `bank_capital_unavailable`; low vs peers ⇒ CAUTION |
| NPL trend | deteriorating ⇒ `bank_npl_nco_deteriorating` (CAUTION) |
| NCO trend | deteriorating ⇒ same blocker |
| Criticized / classified loans | rising ⇒ CAUTION |
| CRE / construction concentration | high or unavailable ⇒ `bank_cre_concentration_unavailable` (CAUTION) |
| Deposit cost / beta | rising sharply ⇒ CAUTION |
| Uninsured deposit % / AOCI hit | elevated ⇒ CAUTION |

Golden case: **OZK** — strong serial raiser, low payout, but NPL 0.20%→0.90%
and NCO 0.25%→0.57% (Q1-2026) ⇒ **PASS-CAUTION**, not clean PASS.

## Regulated Utilities

Primary: **EPS payout + FFO/debt + allowed ROE + rate-case + equity issuance**.
Negative FCF is **not** an auto-FAIL.

| Indicator | Caution / blocker condition |
|---|---|
| FFO / debt | missing ⇒ `utility_ffo_debt_unavailable` (CAUTION); weak ⇒ CAUTION |
| Allowed ROE | falling / adverse order ⇒ CAUTION |
| Rate-case status | adverse / pending-adverse ⇒ `utility_rate_case_adverse` (HOLD-REVIEW) |
| Equity issuance risk | high / dilutive ⇒ `utility_equity_issuance_risk` (CAUTION) |
| EPS payout | > 100% ⇒ FAIL |

Golden cases: **WTRG** (AWK all-stock merger — Step 4b event, not a clean
utility PASS), **HTO** (Quadvest + ~$2.7B capex funding ⇒ equity-issuance
risk, low-priority).

## Insurers

Primary: **Operating-EPS payout + combined ratio + reserve development +
statutory capital**. Separate regular vs special dividends (ORI pays large
specials; the headline ~9% yield is a special-inclusive artifact — Step 1
must use the regular forward yield, ≈3.2%).

| Indicator | Caution / blocker condition |
|---|---|
| Combined ratio | missing ⇒ `insurer_combined_ratio_unavailable`; > 100 ⇒ CAUTION |
| Reserve development | adverse ⇒ `insurer_reserve_development_adverse` (HOLD-REVIEW) |
| Statutory capital | weak ⇒ HOLD-REVIEW |
| Special vs regular split | specials must be excluded from the income base |

Golden case: **ORI** — regular yield clears the 3% (balanced) floor →
Step-1 PASS → insurer-module HOLD-REVIEW (lumpy specials), NOT "trap /
below floor".

### Referencia: references/stock-note-template.md

# One-Page Stock Memo Template

Use one memo per ticker. Keep each section concise and evidence-based.

```markdown
# [Ticker] - Dividend Memo

## Business Model
- Revenue engine:
- Core customer segments:
- Structural moat/risk:

## Dividend Policy
- Current forward yield:
- Dividend growth track record:
- Historical cuts/suspensions:

## Dividend Safety
- EPS payout ratio:
- FCF payout ratio (or FFO/NII coverage):
- Net debt trend:
- Interest coverage:
- Verdict: PASS / CAUTION / FAIL

## Kanchi Step 3 Valuation
- Method used: (PERxPBR / P-FFO / P-FCF / forward PE)
- Current value:
- Historical reference:
- Valuation verdict:

## Kanchi Step 4 One-Off Check
- Key finding (one sentence):
- Verdict: PASS / FAIL

## Verdict (WS-5 actionable tier)
- Tier: CLEAN-PASS / PASS-CAUTION / CONDITIONAL-PASS / HOLD-REVIEW / STEP1-RECHECK / FAIL
- Verdict reasons:

## Pre-Order Blockers (WS-6)
- pre_order_blockers[]: <list, or "none">
- t1_blocked: true / false
- If any blocker is unresolved OR t1_blocked: **T1 is blocked or downsized
  to a ≤20% tracking tranche** (never the full 40%). Resolve / acknowledge
  each blocker (status: blocked → acknowledged → cleared) before sizing up.

## Entry Plan (Kanchi Step 5)
- Trigger type: Yield / Valuation / Both
  - **Yield trigger**: current yield >= 5y avg yield + alpha (default +0.5pp)
  - **Valuation trigger**: price reaches target multiple (P/E, P/FFO, P/FCF)
- Buy zone: $[lower] - $[upper]
- Split orders: 40% / 30% / 30%  (T1 gated by Pre-Order Blockers above)
- Invalidation condition:

## Maximum Risk
- "If this happens, thesis is broken":

## Provenance (audit trail)
```yaml
provenance:
  price_source:
  price_asof:
  dividend_source:        # fmp_stock_dividend | issuer_ir
  dividend_dates_used: []
  payout_source:          # FMP | issuer non-GAAP recon | UNAVAILABLE
  event_scan_result:      # CLEAN_CONFIRMED | NO_EVENT_FOUND | MAJOR_EVENT | ...
  event_scan_checked_at:
  unresolved_blockers: []
  evidence_refs:
    - claim:
      source_type:        # issuer_ir | sec_filing | exchange | wire | portal
      source_url:
      checked_at:
      raw_value:
      normalized_value:
      confidence:          # high | medium | low
```

## Run Context (profile guard — never reuse a 3%-run result in a 4%-run)
```yaml
run_context:
  profile:                # income-now | balanced | growth-first
  yield_floor_pct:
  safety_bias:            # tight | medium
  universe_source:
  excluded_asset_types: []
```
```

Do not skip the invalidation condition, the provenance block, or the
pre-order blocker gate.

### Referencia: references/valuation-and-one-off-checks.md

# Valuation And One-Off Checks

Use this file for Kanchi Step 3 and Step 4 decisions.

## Step 3: Valuation Mapping By Sector

| Sector/Type | Primary metric | Secondary metric | Pass condition example |
|---|---|---|---|
| Banks/Insurers | `P/TBV` | `PER x PBR` (compatibility) + historical percentile | Reject when clearly above historical fair band |
| REIT | `P/FFO` or `P/AFFO` | Implied cap rate vs peers | Prefer below own 5y median multiple |
| Asset-light growth | Forward `P/E` | `P/FCF` and 5y range | Require at least one valuation metric near lower half of range |
| Mature cash cows | `P/FCF` | Dividend yield vs 5y average | Prefer yield above historical mean with intact fundamentals |

Note:
- Kanchi's original Japan-style filter uses `PER x PBR`.
- For US banks, `P/TBV` is typically more robust because tangible book is the standard anchor.

If metrics disagree, choose `HOLD-FOR-REVIEW` instead of forcing `PASS`.

## Step 4: One-Off Profit Checklist

Mark each item `YES/NO`. Two or more `YES` values require downgrade or reject.

1. Profit jump driven by asset sales or disposal gains.
2. EPS lifted by legal settlement or tax one-time effects.
3. Margin expansion without matching revenue quality.
4. Management repeatedly labels key profit items as "non-recurring."
5. Dividend support appears linked to debt increase or asset liquidation.

## Step 4 Output Format

Use this exact compact output in reports:

```text
Step4 verdict: FAIL
Reason: EPS uplift mostly from one-time asset sale; recurring margin trend still weak.
```

Keep each reason to one sentence.


---

## SKILL: kanchi-dividend-us-tax-accounting

- Fuente: `tradermonty/claude-trading-skills` → `skills/kanchi-dividend-us-tax-accounting` (MIT)
- Cuándo usarla: Provide US dividend tax and account-location workflow for Kanchi-style income portfolios. Use when users ask about qualified vs ordinary dividends, 1099-DIV interpretation, REIT/BDC distribution treatment, holding-period checks, or taxable-vs-IRA account placement decisions for dividend assets.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/kanchi-dividend-us-tax-accounting/` (openai.yaml, requirements.txt, build_tax_planning_sheet.py)

# Kanchi Dividend Us Tax Accounting

## Overview

Apply a practical US-tax workflow for dividend investors while keeping decisions auditable.
Focus on account placement and classification, not legal/tax advice replacement.

## When to Use

Use this skill when the user needs:
- US dividend tax classification planning (qualified vs ordinary assumptions).
- Holding-period checks before year-end tax planning.
- Account-location decisions for stock/REIT/BDC/MLP income holdings.
- A standardized annual dividend tax memo format.

## Prerequisites

Prepare holding-level inputs:
- `ticker`
- `instrument_type`
- `account_type`
- `hold_days_in_window` (if available)

Use the exact JSON contract and examples in `references/input-schema.md`.

For deterministic output artifacts, provide JSON input and run:

```bash
python3 skills/kanchi-dividend-us-tax-accounting/scripts/build_tax_planning_sheet.py \
  --input /path/to/tax_input.json \
  --output-dir reports/
```

## Guardrails

Always state this clearly: tax outcomes depend on individual facts and jurisdiction.
Treat this skill as planning support, then escalate final filing decisions to a tax professional.

## Workflow

### 1) Classify each distribution stream

For each holding, classify expected cash flow into:
- Potential qualified dividend.
- Ordinary dividend/non-qualified distribution.
- REIT/BDC-specific distribution components where applicable.

Use `references/qualified-dividend-checklist.md`
for holding-period and classification checks.

### 2) Validate holding-period eligibility assumptions

For potential qualified treatment:
- Check ex-dividend date windows.
- Check required minimum holding days in the measurement window.
- Flag positions at risk of failing holding-period requirement.

If data is incomplete, mark status as `ASSUMPTION-REQUIRED`.

### 3) Map to reporting fields

Map planning assumptions to expected tax-form buckets:
- Ordinary dividend total.
- Qualified dividend subset.
- REIT-related components when reported separately.

Use form terminology consistently so year-end reconciliation is straightforward.

### 4) Build account-location recommendation

Use `references/account-location-matrix.md` to place
assets by tax profile:
- Taxable account for holdings likely to remain qualified-focused.
- Tax-advantaged account for higher ordinary-income style distributions.

When constraints conflict (liquidity, strategy, concentration), explain the tradeoff explicitly.

### 5) Produce annual planning memo

Use `references/annual-tax-memo-template.md` and include:
- Assumptions used.
- Distribution classification summary.
- Placement actions taken.
- Open items for CPA/tax-advisor review.

## Output

Always output:
1. Holding-level distribution classification table.
2. Account-location recommendation table with rationale.
3. Open-risk checklist for unresolved tax assumptions.
4. Optional generated artifacts from
`skills/kanchi-dividend-us-tax-accounting/scripts/build_tax_planning_sheet.py`.

## Cadence

Use this minimum rhythm:
- Annually (60 min): full tax planning memo with account-location review.
- Quarterly (15 min): refresh holding-period status for recent acquisitions.
- Ad-hoc: rerun after material position changes, REIT/BDC additions, or triggered reviews from `kanchi-dividend-review-monitor`.

## Multi-Skill Handoff

- Receive candidate and holding list from `kanchi-dividend-sop`.
- Receive risk-event context (`WARN/REVIEW`) from `kanchi-dividend-review-monitor`.
- Return account-location constraints back to `kanchi-dividend-sop` before new entries.

## Resources

- `skills/kanchi-dividend-us-tax-accounting/scripts/build_tax_planning_sheet.py`: tax planning sheet generator.
- `skills/kanchi-dividend-us-tax-accounting/scripts/tests/test_build_tax_planning_sheet.py`: tests for tax planning outputs.
- `references/qualified-dividend-checklist.md`: classification and holding-period checks.
- `references/account-location-matrix.md`: placement matrix by account type and instrument.
- `references/annual-tax-memo-template.md`: reusable memo structure.

### Referencia: references/account-location-matrix.md

# Account Location Matrix

Use this matrix to propose placement between taxable and tax-advantaged accounts.

## Baseline Placement Logic

| Instrument profile | Taxable account | Tax-advantaged account | Rationale |
|---|---|---|---|
| Qualified-dividend-heavy US equity | Usually preferred | Optional | Potentially better ongoing tax efficiency in taxable account |
| REIT-heavy income holdings | Less preferred | Often preferred | Distribution may include higher ordinary-income components |
| BDC/high-distribution structures | Less preferred | Often preferred | Tax treatment can be less favorable in taxable account |
| MLP (partnership units) | Case-by-case | Caution in tax-advantaged accounts | UBTI and K-1 complexity can make placement non-trivial |
| Broad index ETF with low turnover | Often acceptable | Also acceptable | Depends on overall asset-location design |

If MLP is outside mandate, mark it explicitly as `OUT-OF-SCOPE` and exclude from default allocation logic.

## Conflict Resolution Rules

When account-location recommendation conflicts with other needs:
1. Respect concentration and risk controls first.
2. Respect liquidity/withdrawal constraints second.
3. Optimize taxes third.

## Output Format

Return one line per holding:

```text
[Ticker] -> [Recommended Account] | Why: [one sentence]
```

### Referencia: references/annual-tax-memo-template.md

# Annual Dividend Tax Planning Memo Template

```markdown
# Annual Dividend Tax Planning Memo ([Year])

## Filing Timeline
- Tax year:
- Filing deadline:
- Extension status (filed/planned/not needed):
- Expected filing date:

## Scope
- Accounts included:
- Holdings covered:
- Data sources used:

## Assumptions
- Rule set version/date:
- Missing data assumptions:

## Distribution Classification Summary
| Ticker | Account | Ordinary (est.) | Qualified (est.) | REIT/other components | Confidence |
|---|---|---:|---:|---|---|
| ... | ... | ... | ... | ... | High/Med/Low |

## Account-Location Actions
| Ticker | Current location | Proposed location | Reason |
|---|---|---|---|
| ... | ... | ... | ... |

## Open Risks / Follow-Ups
1. ...
2. ...
3. ...

## Advisor Questions
1. ...
2. ...
```

Keep the memo concise and assumption-driven.

### Referencia: references/input-schema.md

# Tax Planning Input Schema

Provide one JSON object with a non-empty `holdings` array.

```json
{
  "holdings": [
    {
      "ticker": "JNJ",
      "instrument_type": "stock",
      "account_type": "taxable",
      "security_type": "common",
      "hold_days_in_window": 75
    }
  ]
}
```

## Holding fields

- `ticker`: ticker symbol. Required operationally; missing values render as
  `UNKNOWN` and must be corrected before acting.
- `instrument_type`: `stock`, `reit`, `bdc`, or `mlp`; defaults to `stock`.
- `account_type`: account label such as `taxable` or `ira`; defaults to
  `unknown`.
- `security_type`: `common` or `preferred`; defaults to `common`.
- `hold_days_in_window`: non-negative integer holding days in the applicable
  ex-dividend window. Missing or `null` values remain unknown: stock rows emit
  `assumption_required`, while REIT/BDC/MLP rows retain their instrument-specific
  planning labels. Strings, booleans, floats, and negative counts are rejected;
  the CLI exits 1 with an error on stderr before writing reports.

For a not-yet-owned candidate, create a hypothetical row using the intended
account type and leave `hold_days_in_window` absent. Treat the resulting advice
as planning support, not a confirmed tax classification.

### Referencia: references/qualified-dividend-checklist.md

# Qualified Dividend Checklist (US)

Use this checklist for planning assumptions.

## Classification Pass

For each holding, verify:
1. Distribution is potentially eligible for qualified treatment by instrument/type.
2. Shares meet required holding-period test around the ex-dividend date window.
3. No known disqualifying condition in the current fact pattern.

If any item is uncertain, mark as `ASSUMPTION-REQUIRED`.

## Holding-Period Rules (US Federal, Common Planning Baseline)

- Common stock baseline: hold shares for **more than 60 days** during the **121-day period** that starts **60 days before** the ex-dividend date.
- Preferred stock (certain long-period dividends): often uses **more than 90 days** during a **181-day period** starting **90 days before** ex-dividend date.

Use current IRS guidance as source of truth:
- [IRS Publication 550, Qualified Dividends](https://www.irs.gov/publications/p550).
- IRS Form 1099-DIV instructions.

## Script Planning Limitations

`build_tax_planning_sheet.py` compares an operator-supplied day count against
61 days for common stock or 91 days for `security_type: preferred`. It does
not derive the applicable window from acquisition, disposal, or ex-dividend
dates, and it does not subtract days when the risk of loss was reduced.
Prepare the qualifying day count before supplying it to the script.

Publication 550 limits the preferred-stock 91-day test to dividends covering
periods longer than 366 days; shorter-period preferred dividends follow the
common-stock test. The script has no dividend-period field and applies the
91-day preferred threshold as a planning shortcut. Its result can therefore
be more restrictive for shorter-period preferred dividends. Verify those
cases manually against the applicable IRS window rather than treating the
script label as a final tax determination. The same manual review applies
to issuer eligibility and other conditions beyond the supplied day count.

REIT and BDC rows retain an `ordinary_likely` planning label regardless of
the day count. Actual distributions may contain multiple tax components;
use broker/issuer breakdowns to determine the final treatment.

## Practical Data Fields

Track these fields for each position:
- Ticker
- Account type
- Ex-dividend date
- Purchase date(s)
- Disposal date(s), if any
- Days held in required window
- Preliminary classification (`qualified-likely`, `ordinary-likely`, `unknown`)

## Common Pitfalls

- Assuming all common-stock dividends will be qualified without holding-period verification.
- Ignoring short holding periods caused by frequent tactical trading.
- Treating REIT/BDC distributions as identical to standard qualified-dividend flows.
- **Modeling special / variable dividends as steady qualified income**
  (WS-8 hand-off from `kanchi-dividend-sop`). When the upstream
  `dividend_basis` carries `special_dividend_flag` or
  `variable_policy_flag` (e.g. ORI annual specials, CALM variable policy),
  treat that cash as **lumpy and non-recurring** for account-location and
  cash-flow planning: budget the *regular* run-rate as base income and the
  special/variable component separately (timing unpredictable; may still
  be qualified but must not be annualized as if recurring).

## Recommended Source Hierarchy

1. Broker tax documents and distribution breakdowns.
2. Official IRS publications/instructions for current-year rules (Publication 550, 1099-DIV instructions).
3. Issuer or fund notices when classification is revised.


---

## SKILL: proposal-generation

- Fuente: `JoelLewis/finance_skills` → `plugins/advisory-practice/skills/proposal-generation` (MIT)
- Cuándo usarla: Generate end-to-end investment proposals covering risk profiling, model portfolio recommendation, fee illustration, projections, and compliance review. Use when the user asks about creating a proposal for a prospect, mapping risk questionnaire scores to model portfolios, building fee illustrations with tiered costs, producing Monte Carlo or scenario projections, analyzing a prospect's current portfolio for improvement opportunities, reviewing proposals for SEC Marketing Rule compliance, or designing proposal templates for a multi-advisor firm. Also trigger when users mention 'investment proposal', 'proposal generation', 'risk profiling', 'Riskalyze', 'Nitrogen', 'fee illustration', 'transition analysis', 'current vs proposed portfolio', or 'proposal compliance review'.

# Proposal Generation

## Core Concepts

### Proposal Workflow Architecture
The investment proposal is the centerpiece of the advisory sales process. It translates a prospect's financial situation and goals into a specific, actionable investment recommendation. The end-to-end workflow proceeds through defined stages:

1. **Discovery meeting** — the advisor meets with the prospect to understand their financial situation, goals, concerns, and expectations. The advisor collects current account statements, tax returns, and any existing financial plan. The discovery meeting establishes the advisory relationship's tone and sets expectations for the proposal.
2. **Data collection and organization** — the advisor or operations team enters prospect data into the proposal system: personal information, current holdings (manually or via account aggregation), financial goals, time horizons, income, expenses, tax situation, and any unique circumstances (concentrated positions, restricted stock, estate planning needs).
3. **Risk profiling** — the prospect completes a risk tolerance questionnaire. The system scores the responses and produces a risk profile that maps to a position on the firm's risk-return spectrum. The risk profile is the bridge between subjective client preferences and objective portfolio construction.
4. **Model portfolio selection** — the risk profile score maps to a specific model portfolio from the firm's lineup. The advisor reviews the mapping, considers any client-specific factors that might warrant adjustment (tax sensitivity, income needs, ESG preferences, concentrated positions), and confirms the recommended model.
5. **Current portfolio analysis** — if the prospect has existing investments, the system analyzes their current holdings: asset allocation, risk metrics, expense ratios, tax lots, concentrated positions, overlap, and style drift. This analysis quantifies the gap between the current portfolio and the recommended model.
6. **Proposal document generation** — the system assembles the proposal document from templates, populating it with client-specific data, the recommended portfolio, fee schedule, projections, and disclaimers. The proposal document is the deliverable that the prospect reviews and uses to make their decision.
7. **Compliance review** — before the proposal is presented, it undergoes supervisory review to verify suitability documentation, performance presentation compliance, fee disclosure adequacy, and proper disclaimers. For firms subject to the SEC Marketing Rule, proposals that include performance data require additional scrutiny.
8. **Presentation and discussion** — the advisor presents the proposal to the prospect, walks through the analysis and recommendation, answers questions, and addresses concerns. The presentation meeting is where the advisory value proposition is demonstrated.
9. **Revision and finalization** — based on the prospect's feedback, the advisor may revise the recommendation (different model, adjusted allocation, modified fee structure) and regenerate the proposal.
10. **Acceptance and onboarding** — the prospect accepts the proposal by signing the advisory agreement (IMA or similar). The proposal data flows into the onboarding process: account opening, funding, and initial investment in the recommended model.

The workflow is iterative, not strictly linear. Prospects may request multiple revisions, ask for comparisons between different models, or bring additional assets into scope after the initial proposal. The proposal system must support version tracking and efficient regeneration.

### Risk Profiling and Model Mapping
Risk profiling is the foundation of the proposal recommendation. The risk questionnaire produces a quantitative score that determines which model portfolio is appropriate for the prospect.

**Risk questionnaire design:**
- Questionnaires typically contain 10-25 questions assessing both willingness (behavioral/emotional tolerance for loss) and capacity (financial ability to absorb losses without jeopardizing goals).
- Common question formats include: scenario-based loss tolerance ("If your portfolio lost 20% in a month, would you sell, hold, or buy more?"), time horizon assessment, income stability evaluation, and investment experience self-assessment.
- Scoring produces a numerical result (e.g., 1-100) or a categorical classification (Conservative, Moderately Conservative, Moderate, Moderately Aggressive, Aggressive).
- Third-party risk profiling tools (Riskalyze/Nitrogen, Tolerisk, FinaMetrica) provide validated, statistically tested questionnaires with defensible scoring methodologies. These are preferred over home-built questionnaires because they have undergone psychometric validation and are widely accepted by regulators.

**Model portfolio lineup design:**
A typical advisory firm maintains 5-10 model portfolios spanning the risk-return spectrum:

| Risk Score Range | Model Name | Equity/Fixed Income | Expected Return Range | Expected Max Drawdown |
|-----------------|------------|--------------------|-----------------------|----------------------|
| 1-20 | Conservative Income | 20/80 | 3-5% | -8 to -12% |
| 21-35 | Moderate Conservative | 35/65 | 4-6% | -12 to -18% |
| 36-50 | Moderate | 50/50 | 5-7% | -18 to -25% |
| 51-65 | Moderate Growth | 65/35 | 6-8% | -25 to -32% |
| 66-80 | Growth | 80/20 | 7-9% | -32 to -40% |
| 81-100 | Aggressive Growth | 95/5 | 8-11% | -40 to -50% |

Each model is defined by a strategic asset allocation with target weights and permissible ranges for each asset class, along with specific fund or ETF selections that implement the allocation. Models should be reviewed and rebalanced on a defined schedule (typically quarterly or semi-annually).

**Suitability alignment:**
The risk profile alone does not determine the recommendation. The advisor must also consider:
- **Time horizon** — a young investor with a long horizon may be profiled as moderate but could reasonably be placed in a growth model, while a retiree with the same risk score needs more conservative positioning due to sequence-of-returns risk.
- **Income needs** — a prospect requiring portfolio income may need a model tilted toward income-producing assets, regardless of risk score.
- **Tax sensitivity** — a taxable account may warrant a tax-managed version of the model (municipal bonds, tax-loss harvesting overlay, low-turnover equity strategies).
- **Concentrated positions** — a prospect with a large single-stock position may need a transition strategy rather than an immediate full model assignment.
- **ESG preferences** — if the prospect has environmental, social, or governance preferences, the firm may offer ESG-screened variants of its standard models.

**Documenting the recommendation rationale:**
The proposal must articulate why this specific model is appropriate for this prospect. The rationale should reference the risk profile score, the model's risk-return characteristics, and how the recommendation aligns with the prospect's stated objectives, time horizon, and constraints. This documentation serves both as a client communication tool and as a suitability record for compliance purposes.

### Proposal Document Components
A complete investment proposal typically includes the following sections:

**Executive summary** — a one-page overview of the recommendation: who the client is, what is being recommended, why it is appropriate, and the expected outcome. The executive summary is often the only page some decision-makers read in detail; it must be clear and compelling.

**Client profile recap** — a summary of the prospect's financial situation as understood by the advisor: personal information, financial goals, time horizon, risk profile score and interpretation, income and expense summary, tax situation, and any special circumstances. This section demonstrates that the advisor listened during discovery and correctly understands the prospect's needs.

**Current portfolio analysis (if applicable)** — for prospects with existing investments, this section provides:
- Holdings list with current market values
- Asset allocation breakdown (pie chart and table) compared to the recommended allocation
- Risk metrics: portfolio standard deviation, beta, Sharpe ratio, maximum drawdown estimate
- Expense analysis: weighted average expense ratio, total annual cost in dollars
- Concentrated position identification: any single holding exceeding 5-10% of the portfolio
- Style analysis: Morningstar style box mapping, factor exposures
- Income analysis: current yield, income projection
- Tax lot summary: unrealized gains and losses, short-term vs long-term, estimated tax impact of liquidation

**Recommended portfolio** — the core of the proposal:
- Asset allocation targets with visual representation (pie chart, bar chart)
- Holdings list: each fund or ETF, its asset class role, expense ratio, target weight, and dollar amount
- Risk-return profile of the recommended portfolio: expected return, standard deviation, Sharpe ratio, maximum drawdown estimate
- Comparison table: current portfolio vs recommended portfolio on key metrics
- Income projection: expected yield and annual income from the recommended portfolio

**Fee schedule** — a complete disclosure of all costs the client will bear (see Fee Illustration section below).

**Historical performance context** — how the recommended model or a similar allocation has performed historically. This section requires careful attention to compliance (see Performance Projections and Disclaimers section below). Common presentations include:
- Historical returns of the model portfolio (if a track record exists) or a blended benchmark representing the target allocation
- Calendar-year returns showing both up and down years
- Growth of $1 million chart over a trailing period (e.g., 10 or 20 years)
- Performance during specific market events (2008-2009 crisis, 2020 COVID drawdown, 2022 rate shock)

**Scenario projections** — forward-looking analysis showing potential outcomes:
- Monte Carlo simulation results: probability of meeting the client's goal, median outcome, 10th percentile (bad case), 90th percentile (good case)
- Straight-line projections at expected return (with explicit disclaimer that this is illustrative only)
- Stress test scenarios: how the portfolio would perform in a repeat of historical crises

**Disclaimers and disclosures** — required legal language (see Compliance Review section below).

**Next steps** — a clear call to action: sign the advisory agreement, fund the account, and begin investing. Include a timeline for implementation.

### Fee Illustration
The fee illustration section of the proposal must present costs clearly, completely, and in compliance with fee disclosure requirements. Prospects make decisions based on fees; incomplete or misleading fee disclosure undermines trust and creates regulatory risk.

**Advisory fee presentation:**
- Present the firm's fee schedule with all tiers and breakpoints. For a tiered schedule, show both the marginal rate at each tier and the blended (effective) rate for the prospect's specific asset level.
- Example tiered fee schedule illustration for a $2M portfolio:

| Tier | Rate | Assets in Tier | Fee for Tier |
|------|------|---------------|-------------|
| First $500K | 1.00% | $500,000 | $5,000 |
| Next $500K | 0.85% | $500,000 | $4,250 |
| Next $1M | 0.75% | $1,000,000 | $7,500 |
| **Total** | **Blended: 0.8375%** | **$2,000,000** | **$16,750/year** |

- Show the fee in both percentage and dollar terms. Dollar amounts are more tangible to prospects. (Reg BI requires disclosure of material fees and costs but does not prescribe dollar-amount illustrations; presenting dollar figures is a best practice for making the disclosure concrete.)
- Specify billing frequency (quarterly in advance or arrears) and the per-quarter dollar amount.

**Fund-level expense disclosure (fee-on-fee):**
- Disclose the weighted average expense ratio of the funds in the recommended portfolio.
- Show the total annual cost combining advisory fees and fund expenses.
- Example: Advisory fee 0.84% + weighted average fund expense ratio 0.12% = total annual cost 0.96%, or $19,200 on a $2M portfolio.
- For proposals recommending funds-of-funds or wrap programs with underlying fund costs, the layered fee structure must be made transparent.

**Total cost of ownership:**
- Beyond advisory fees and fund expenses, disclose any other costs: custodian fees, transaction costs (if applicable), account maintenance fees, wire fees, and any other charges.
- Present a single "all-in" annual cost figure and percentage so the prospect can compare to alternatives.

**Breakpoint analysis:**
- If the prospect's assets are near a fee tier breakpoint, show the impact of consolidating additional assets to reach the next lower rate.
- Example: "At your current $475,000, your blended rate is 1.00%. By consolidating an additional $25,000, your blended rate drops to 0.985%, saving approximately $75 per year. At $1,000,000, your blended rate is 0.925%."

**Fee comparison vs alternatives:**
- Prospects often compare advisory fees to robo-advisors, self-directed brokerage, or other advisory firms. The proposal may include a comparison showing the additional services provided for the advisory fee (financial planning, tax management, behavioral coaching, rebalancing).
- Be factual and avoid disparaging competitors. Focus on value delivered rather than competitor shortcomings.

**Reg BI cost disclosure requirements:**
- For broker-dealers making recommendations, Reg BI requires that the cost disclosure be specific to the recommendation, not generic. The prospect must be able to understand the total cost of the specific securities and account type being recommended.
- The Disclosure Obligation under Reg BI requires written disclosure of all material fees and costs, including indirect compensation (12b-1 fees, revenue sharing).

### Performance Projections and Disclaimers
Performance presentation in proposals is one of the most compliance-sensitive areas of the advisory business. The SEC Marketing Rule (Rule 206(4)-1 under the Advisers Act, effective November 2022) substantially governs how investment advisers present performance.

**Is a proposal "advertising"?**
Under the Marketing Rule, "advertisement" includes any communication to more than one person (or designed for such use) that offers or promotes advisory services. A one-on-one proposal to a specific prospect is generally not an advertisement if it is truly tailored to that individual. However, if the firm uses a standardized proposal template that is distributed broadly with only minor customization, regulators may view it as advertising. Best practice: treat all performance presentations in proposals as if the Marketing Rule applies, even for one-on-one presentations.

**Historical performance presentation:**
- If presenting actual model portfolio track records, the Marketing Rule requires: gross and net-of-fee performance shown with equal prominence, a disclosure of whether the performance reflects actual client accounts or a model/hypothetical, the time period covered, and material conditions or assumptions.
- If presenting index or benchmark returns as a proxy for the recommended allocation, clearly label them as benchmark returns, not the firm's performance. Disclose that the benchmark is not directly investable and does not reflect fees, trading costs, or taxes.

**Hypothetical performance:**
- The Marketing Rule permits hypothetical performance (including backtested model portfolios) in one-on-one presentations, provided the adviser adopts policies and procedures reasonably designed to ensure the performance is relevant to the recipient's financial situation and investment objectives, and the adviser provides sufficient information for the recipient to understand the assumptions and limitations.
- Required disclosures for hypothetical performance: the results do not represent actual trading, the results were achieved by retroactive application of a model, actual results may differ materially, and the specific methodology and assumptions used.
- Backtested performance must disclose the material assumptions (rebalancing frequency, dividend reinvestment, fund selection dates, any survivorship bias corrections).

**Monte Carlo projections:**
- Monte Carlo simulations generate a distribution of potential outcomes by running thousands of randomized return scenarios based on the portfolio's expected return, standard deviation, and correlation assumptions.
- Key outputs: probability of achieving the client's goal (e.g., "85% probability of maintaining your income through age 95"), median projected portfolio value at target date, range of outcomes (10th to 90th percentile fan chart).
- Required disclosures: Monte Carlo simulations are hypothetical, based on assumptions that may not reflect future market conditions, do not guarantee results, and are sensitive to the input assumptions (small changes in expected return or volatility can significantly alter the output).
- Do not present Monte Carlo results as predictions. Use language like "based on the assumptions described, the analysis suggests..." rather than "your portfolio will grow to..."

**Expected return ranges:**
- When presenting expected returns for a recommended portfolio, always present a range rather than a single point estimate. A single expected return figure implies false precision.
- Disclose the methodology: are expected returns based on capital market assumptions from a third-party provider (e.g., BlackRock, J.P. Morgan, Vanguard), the firm's internal research, or historical averages? Each approach has limitations that must be acknowledged.

**Required disclaimers (at minimum):**
- "Past performance is not indicative of future results."
- "Investing involves risk, including the potential loss of principal."
- "Hypothetical performance results have many inherent limitations. No representation is being made that any account will or is likely to achieve profits or losses similar to those shown."
- "The projections or other information regarding the likelihood of various investment outcomes are hypothetical in nature, do not reflect actual investment results, and are not guarantees of future results."
- For tax-related projections: "This analysis is not tax advice. Consult a qualified tax professional regarding your specific situation."

### Current Portfolio Analysis
When a prospect has an existing portfolio at another firm, the current portfolio analysis is one of the most persuasive sections of the proposal. It quantifies the specific improvements the prospect will experience by moving to the recommended portfolio.

**Holdings review:**
- Import the prospect's current holdings from account statements, a CSV export, or an account aggregation tool (ByAllAccounts, Plaid — which absorbed Quovo in 2019 — or Yodlee).
- Classify each holding by asset class, sub-asset class, and style to build a complete picture of the current allocation.
- Identify any holdings that are not transferable in-kind (proprietary funds, annuities with surrender charges, illiquid alternatives).

**Risk assessment:**
- Calculate the current portfolio's risk metrics: annualized standard deviation, beta relative to a blended benchmark, maximum drawdown over the historical period, Value at Risk (VaR) at 95% confidence.
- Compare these metrics side-by-side with the recommended portfolio. If the current portfolio has higher risk for the same or lower expected return, this is a compelling argument for transition.
- Use risk visualization tools (Riskalyze/Nitrogen Risk Number, Morningstar risk/return scatterplot) to make the comparison accessible to non-technical prospects.

**Tax lot analysis:**
- For taxable accounts, identify unrealized gains and losses by holding and by tax lot.
- Classify gains and losses as short-term or long-term, as the tax impact differs substantially (short-term gains taxed as ordinary income vs long-term gains at preferential capital gains rates).
- Calculate the estimated tax cost of full liquidation vs a phased transition.
- Identify holdings with large embedded gains that may be candidates for retention or gradual disposition.

**Transition cost estimation:**
- The transition from current portfolio to recommended portfolio involves costs: capital gains taxes (for taxable accounts), transaction costs (commissions or spreads), and potential market impact for large or illiquid positions.
- Present a transition cost analysis: estimated tax liability, estimated transaction costs, and the net benefit of transitioning (reduced ongoing fees, improved risk-adjusted returns, better diversification) vs the one-time transition cost.
- For large embedded gains, propose a phased transition plan: sell short-term lots and loss positions immediately, transition long-term gain positions over 12-24 months, retain specific holdings that fit within the recommended allocation.

**Concentrated position identification:**
- Flag any single security representing more than 5% of the portfolio (or a lower threshold per firm policy).
- For each concentrated position, disclose the specific risk: single-stock risk (company-specific, sector-specific), lack of diversification, potential regulatory or insider trading restrictions.
- Propose strategies for managing the concentration: direct sale (with tax analysis), exchange funds, charitable remainder trusts, protective put options, systematic diversification over time.

**Improvement quantification:**
The proposal should clearly quantify the improvements the prospect will experience:
- Fee savings: current total cost vs proposed total cost, in dollars per year
- Risk reduction: current portfolio risk metrics vs proposed, expressed in terms the prospect understands ("Your current portfolio could lose up to $X in a severe downturn; the proposed portfolio limits that to approximately $Y")
- Diversification improvement: number of holdings, asset class coverage, geographic diversification, sector concentration reduction
- Income improvement: current yield vs proposed yield, annual income difference

### Compliance Review of Proposals
Every proposal must undergo compliance review before presentation to the prospect. The review ensures suitability documentation, performance presentation, fee disclosure, and disclaimers meet regulatory requirements.

**Supervisory review requirements:**
- FINRA Rule 3110 (broker-dealers) and SEC guidance for RIAs require supervisory review of communications with the public. While a one-on-one proposal may not technically be "correspondence" or "advertising" under FINRA's definitions, most firm compliance manuals require supervisory sign-off on proposals, particularly those containing performance data or projections.
- The supervisor's review should verify: (1) the recommendation is suitable given the documented client profile, (2) performance data is presented in compliance with the Marketing Rule or FINRA advertising rules, (3) fee disclosure is complete and accurate, (4) all required disclaimers are present, and (5) any claims about the firm or its services are substantiated.

**Advertising rule applicability:**
- Under the SEC Marketing Rule, a one-on-one proposal to a specific prospect is generally not an advertisement. However, the proposal becomes advertising if it is used with more than one person or is designed for broad distribution. Template proposals with standardized performance and marketing language should be treated as advertisements.
- FINRA Rule 2210 classifies communications as institutional, retail, or correspondence. A proposal to a retail prospect is typically retail communication, requiring principal pre-approval if it makes performance claims or recommendations.

**Performance presentation rules:**
- If the proposal includes actual performance of the firm's models or composites, the Marketing Rule requires gross and net performance with equal prominence, the period covered, and material assumptions.
- If the proposal includes hypothetical or backtested performance, it must include disclosures about the limitations of hypothetical results and the methodology used.
- GIPS-compliant firms must present performance consistent with GIPS standards if they claim GIPS compliance; mixing GIPS and non-GIPS presentations creates confusion and potential violations.

**Fee disclosure adequacy:**
- Verify that the fee illustration includes all layers of cost: advisory fees, fund expenses, transaction costs, custodian fees, and any other charges.
- Confirm that fee tier calculations are accurate for the prospect's specific asset level.
- Ensure that any fee comparison to alternatives is fair and not misleading.

**Suitability documentation:**
- The compliance reviewer should verify that the prospect's risk profile, investment objectives, time horizon, and financial situation are documented and that the recommendation is consistent with this profile.
- If the recommendation deviates from the standard model mapping (e.g., the risk score maps to Moderate but the advisor recommends Moderate Growth), the rationale for the deviation must be documented and approved.

### Proposal Technology and Automation
Modern proposal generation relies on technology platforms that integrate data, automate document assembly, and streamline the workflow from discovery to delivery.

**Major proposal generation platforms:**

- **Orion Portfolio Solutions** — provides proposal generation integrated with its portfolio management and reporting platform. Features include model portfolio comparison, fee illustration, risk analysis, and automated document assembly. Strong integration with Orion's trading and reporting ecosystem.
- **Black Diamond (SS&C Advent)** — offers proposal tools as part of its wealth platform, including prospect pipeline tracking, proposal document generation, performance comparison, and integration with its reporting and billing systems.
- **Riskalyze/Nitrogen** — specializes in risk profiling and risk-aligned proposals. The Risk Number system provides an intuitive way to show prospects their current portfolio risk vs the proposed portfolio risk. Proposals include the "95% Historical Range" visualization that resonates with prospects. Nitrogen has expanded from risk assessment into a broader proposal and financial planning workflow.
- **MoneyGuidePro (Envestnet)** — primarily a financial planning tool, but its proposal capabilities include goal-based projections, Monte Carlo analysis, and integration with Envestnet's managed account platform. Proposals frame the investment recommendation within the context of the client's overall financial plan.
- **RightCapital** — financial planning platform with proposal generation that includes tax-aware projections, estate planning visualizations, and a modern client-facing interface. Strong with younger advisory firms and RIAs focused on comprehensive planning.
- **Orion Risk Intelligence (formerly HiddenLevers, acquired by Orion in 2021)** — stress testing and scenario analysis capability that generates proposal-ready reports showing how current and proposed portfolios would perform under various economic scenarios.
- **Advyzon** — all-in-one platform combining CRM, portfolio management, reporting, billing, and client portal with proposal generation capabilities.

**Template management:**
- Firms should maintain a library of approved proposal templates covering common scenarios: new prospect with no current portfolio, prospect with existing brokerage account, prospect with employer retirement plan rollover, institutional prospect, and trust/entity prospect.
- Templates should be version-controlled and require compliance approval before deployment. When performance data or model portfolio holdings change, all affected templates must be updated.
- Template customization should be limited to client-specific data fields; the narrative sections, disclaimers, and compliance language should be locked to prevent advisors from inadvertently making non-compliant modifications.

**Data integration:**
- Proposal systems should pull data from multiple sources: CRM (prospect information), risk profiling tool (risk score), portfolio management system (model portfolio details), market data provider (current prices, historical returns), and custodian (existing account data for current portfolio analysis).
- Account aggregation tools (Plaid, Yodlee, ByAllAccounts) can import the prospect's held-away account data for current portfolio analysis, eliminating manual data entry from account statements.

**Digital delivery:**
- Proposals should be deliverable digitally through a secure client portal or encrypted email, in addition to printed copies for in-person presentations.
- Interactive digital proposals allow the prospect to explore different scenarios, adjust assumptions, and compare models — increasing engagement and reducing the number of revision cycles.
- Digital delivery creates an audit trail: when the prospect received the proposal, how long they viewed it, and which sections they engaged with. This data helps advisors prepare for the presentation meeting.

**E-signature for advisory agreements:**
- When the prospect accepts the proposal, the advisory agreement (Investment Management Agreement or similar) should be available for immediate electronic signature within the proposal platform or via integration with an e-signature provider (DocuSign, Adobe Sign).
- The signed advisory agreement triggers the onboarding workflow: account opening, funding, and initial investment in the recommended model.
- Capturing acceptance digitally reduces the time between proposal acceptance and first investment, which is critical because prospect commitment can wane with delay.

## Worked Examples

See [references/examples.md](references/examples.md) for three end-to-end worked examples — a $2M 401(k) rollover proposal (including NUA considerations), a current-vs-proposed comparison against a broker-dealer portfolio, and a proposal template system for a 25-advisor firm. Load it when the user needs a full scenario walkthrough.

## Common Pitfalls
- Presenting hypothetical or backtested performance without the required disclosures about limitations, methodology, and the fact that results do not represent actual trading
- Showing only gross-of-fee performance without equal-prominence net-of-fee returns, violating the SEC Marketing Rule
- Using Monte Carlo projections without disclosing the input assumptions (expected return, standard deviation, correlation matrix) or the limitations of the simulation
- Mapping risk scores to models mechanically without considering time horizon, income needs, and other suitability factors that may warrant a different recommendation
- Omitting fund-level expenses from the fee illustration, presenting only the advisory fee as the total cost
- Failing to disclose surrender charges, tax consequences, or other transition costs when recommending a move from an existing portfolio
- Generating proposals with stale model portfolio data (holdings or allocations that have changed since the last rebalance)
- Allowing advisors to customize disclaimer language or remove required disclosures from proposal templates
- Presenting a current portfolio analysis that cherry-picks unfavorable metrics to make the current portfolio look worse than it is — comparisons must be fair and balanced
- Not documenting the rationale for recommending a model that deviates from the standard risk profile mapping
- Treating the proposal as a one-time document rather than versioning it — when assumptions change or the prospect requests modifications, the firm must track which version was presented and accepted
- Neglecting to address the prospect's existing concentrated positions, restricted stock, or illiquid holdings in the transition plan
- Using projected returns without clearly labeling them as hypothetical and subject to the Marketing Rule's requirements for hypothetical performance

## Cross-References
- **asset-allocation** (wealth-management plugin): Strategic and tactical asset allocation frameworks that underpin model portfolio construction and the recommended allocation in proposals
- **investment-policy** (wealth-management plugin): IPS construction defines the policy framework that the proposal recommendation must satisfy; the proposal is often the precursor to a formal IPS
- **performance-reporting** (wealth-management plugin): Ongoing performance reporting follows the same presentation standards established in the proposal; consistency between proposal projections and actual reporting builds credibility
- **performance-metrics** (wealth-management plugin): Risk-return metrics (Sharpe ratio, standard deviation, max drawdown) used in proposals to compare current vs recommended portfolios
- **fee-disclosure** (compliance plugin): Regulatory requirements for fee presentation that the proposal's fee illustration section must satisfy
- **reg-bi** (compliance plugin): Regulation Best Interest's Care and Disclosure Obligations govern how broker-dealers present recommendations and costs in proposals
- **client-disclosures** (compliance plugin): Form ADV, Form CRS, and other required disclosures that must accompany or be delivered alongside the proposal
- **investment-suitability** (compliance plugin): Suitability standards that the proposal recommendation must satisfy; the risk profile and model mapping must align with documented suitability requirements
- **advertising-compliance** (compliance plugin): SEC Marketing Rule and FINRA advertising rules that govern performance presentation, testimonials, and promotional claims in proposals
- **financial-planning-integration** (advisory-practice plugin): Proposals increasingly embed financial planning elements (retirement projections, goal funding analysis); the planning integration skill covers how to connect proposals to comprehensive financial plans
- **quantitative-valuation** (wealth-management plugin): Valuation frameworks relevant when proposals include analysis of individual securities in the prospect's current portfolio
- **diversification** (wealth-management plugin): Diversification principles used to evaluate current portfolio concentration and demonstrate the improvement offered by the recommended model

### Referencia: references/examples.md

# Worked Examples — Proposal Generation

### Example 1: Generating a proposal for a new prospect with a $2M rollover from a 401(k)
**Scenario:** A 58-year-old prospect recently left her employer and has $2M in a 401(k) plan invested in a mix of target-date funds and company stock. She is considering rolling the assets to an IRA managed by an advisory firm. She has no other significant investable assets outside her home. She plans to retire at 63 and needs the portfolio to generate $80,000/year (in today's dollars) in retirement income starting at age 63. She completed the firm's risk questionnaire and scored 42 out of 100 (Moderate).

**Design Considerations:**
- The rollover is from a 401(k) to a Traditional IRA, which is a tax-free direct rollover if handled properly. The proposal should explicitly note that this is a direct (trustee-to-trustee) rollover, not a distribution, to avoid a taxable event.
- The 5-year time horizon to retirement combined with a Moderate risk score suggests a portfolio in the Moderate to Moderate Conservative range. While the risk score maps to Moderate (50/50 equity/fixed income), the relatively short time horizon and high dependence on this single portfolio for retirement income argue for a more conservative positioning. The advisor should consider recommending the Moderate Conservative model (35/65) or a custom blend, and document the rationale for any deviation from the standard risk mapping.
- Retirement income analysis: $80,000/year starting at 63, adjusted for 2.5% inflation, funded by a $2M portfolio over a 30+ year retirement (to age 95). The proposal should include Monte Carlo analysis showing the probability of sustaining this income. At a 4% initial withdrawal rate ($80,000/$2,000,000), the prospect is at the widely cited sustainable withdrawal threshold — the analysis should show the sensitivity of success probability to different return scenarios.
- The current 401(k) holdings include company stock, which may have Net Unrealized Appreciation (NUA) tax benefits. The proposal should address whether the NUA strategy is advantageous: if the cost basis of the company stock is low, distributing the shares in-kind to a taxable account (not rolling them to the IRA) allows the NUA to be taxed at long-term capital gains rates rather than ordinary income rates upon distribution from the IRA. This requires careful tax analysis and should be presented as a consideration, not as tax advice.
- Fee illustration: show the firm's tiered fee schedule applied to $2M, the weighted average expense ratio of the recommended funds, and the total cost. Compare this to the prospect's current 401(k) plan expenses (typically 0.50-1.50% all-in for employer plans, depending on plan size and investment options).

**Analysis:** The proposal document should include: (1) Executive summary framing the recommendation as a retirement transition strategy, not just a portfolio change. (2) Client profile recap emphasizing the 5-year accumulation phase followed by a 30+ year distribution phase. (3) Current portfolio analysis showing the 401(k) allocation — likely over-concentrated in company stock and potentially misallocated in the target-date fund (which may be targeting a different retirement date or risk level than appropriate). Quantify the single-stock concentration risk. (4) Recommended portfolio: Moderate Conservative model with 35% equity, 55% investment-grade fixed income, and 10% alternatives/real assets for inflation protection. Include a holdings detail table with specific funds, expense ratios, and target weights. (5) Retirement income projection using Monte Carlo showing 85-90% probability of sustaining $80,000/year (inflation-adjusted) through age 95 — if the probability is lower, discuss options (delaying retirement, reducing spending, part-time work). (6) Fee illustration showing the blended advisory fee of 0.8375% on $2M ($16,750/year) plus fund expenses of approximately 0.12% ($2,400/year) for a total of $19,150/year, compared to the estimated 401(k) plan cost. (7) NUA analysis as a supplementary section, clearly labeled as requiring tax professional review. (8) Transition plan: direct rollover of all non-company-stock assets; separate analysis for company stock disposition. (9) All required disclaimers regarding projections, past performance, and tax information.

### Example 2: Creating a proposal that compares current broker-dealer portfolio vs proposed advisory portfolio
**Scenario:** A prospect with $1.5M at a full-service broker-dealer is unhappy with performance and fees. The current portfolio consists of 18 individual stocks, 6 actively managed mutual funds (A-shares with front loads previously paid), and a fixed annuity. The prospect is 52 years old, risk score 65 (Moderate Growth), retired military with a pension covering basic expenses, and views the investment portfolio as growth capital with a 20+ year horizon. The advisor wants to demonstrate the advantages of the proposed advisory model vs the current BD portfolio.

**Design Considerations:**
- The current portfolio analysis is the most important section of this proposal. The prospect is motivated by dissatisfaction, so the analysis must honestly and accurately quantify the issues with the current portfolio while complying with rules against misleading comparisons.
- Current portfolio issues to analyze: (a) 18 individual stocks likely create concentration risk — measure diversification vs the recommended model; (b) actively managed A-share mutual funds have higher expense ratios (often 0.75-1.25%) than the ETFs or institutional share class funds in the proposed model (often 0.05-0.25%); (c) the prospect may be paying ongoing 12b-1 fees (0.25%) within the A-shares; (d) the fixed annuity may have surrender charges if liquidated before the surrender period expires — this is a critical transition cost to disclose; (e) calculate the total current cost: any ongoing BD advisory or account fees + fund expense ratios + 12b-1 fees.
- The comparison must be fair and not misleading. Do not compare the BD portfolio's worst year to the advisory portfolio's best year. Compare on risk-adjusted metrics (Sharpe ratio, Sortino ratio) over the same time periods. If comparing performance, ensure the comparison uses consistent time periods and accounts for survivorship bias in the current holdings.
- The fixed annuity requires careful handling: if it has a remaining surrender period, disclose the surrender charge and analyze whether the benefit of transition outweighs the surrender cost. If the annuity has favorable guaranteed rates, it may be appropriate to retain it.
- Transition tax analysis: the 18 individual stocks and mutual funds in a taxable account have embedded gains and losses. The proposal must include a tax lot analysis showing the estimated tax cost of liquidation. A phased transition may be more tax-efficient than an immediate full liquidation.

**Analysis:** The proposal should present a structured comparison: (1) Side-by-side asset allocation: current portfolio (likely equity-heavy given 18 stocks plus equity funds, possibly 85-90% equity) vs recommended Moderate Growth model (65/35). The current portfolio may actually carry more risk than the prospect's score supports — this is a powerful finding. (2) Cost comparison: Current all-in cost (estimate BD advisory fee at 1.0-1.5% + fund expenses at 0.90% average + 12b-1 fees at 0.25% on applicable funds) vs proposed (advisory fee of approximately 0.90% blended on $1.5M + fund expenses at 0.12%) — expected annual savings of $8,000-15,000 depending on current BD fee structure. Present this as a 10-year and 20-year cumulative savings. (3) Risk comparison: current portfolio standard deviation and max drawdown estimate vs recommended model. If the current portfolio is carrying 85-90% equity risk, the max drawdown in a 2008-type event would have been approximately -45 to -50%, vs -32% for the recommended model. (4) Diversification comparison: current 18-stock portfolio may have 40-50% in 3-4 sectors vs broad market diversification in the recommended model. (5) Transition plan: retain the fixed annuity if surrender charges apply, harvest tax losses in current holdings to offset gains, transition individual stocks with large embedded gains over 12-18 months, immediately transition mutual fund positions (A-share loads are sunk costs and should not factor into the decision to stay or leave). (6) Disclaimers: the comparison uses historical data and assumptions; actual future performance of either portfolio cannot be predicted; the comparison does not account for all factors that may affect performance; the prospect should consider the tax implications with a qualified professional.

### Example 3: Building a proposal template system for a multi-advisor firm with standardized models
**Scenario:** A growing RIA with 25 advisors and $4B AUM is transitioning from an ad-hoc proposal process (each advisor creates their own proposals using PowerPoint and Excel) to a standardized, automated proposal generation system. The firm has 7 model portfolios, a uniform fee schedule, and uses Schwab as its custodian, Orion for portfolio management, and Salesforce for CRM. The chief compliance officer wants every proposal to pass through a compliance workflow before delivery.

**Design Considerations:**
- The primary challenge is balancing standardization (for compliance, efficiency, and brand consistency) with advisor flexibility (each advisor has their own style, client base, and value proposition). The system should lock compliance-critical elements (disclaimers, performance presentation, fee disclosure) while allowing advisors to customize narrative sections (personal letter, firm value proposition, service description).
- Template architecture should include: (a) a master template with locked compliance sections, (b) modular components that advisors can include or exclude (current portfolio analysis module, retirement income module, tax transition module, estate planning integration module), (c) advisor-specific elements (advisor bio, contact information, personal branding within firm guidelines), and (d) model-specific content (each of the 7 models has a pre-written description, historical context, and risk-return profile).
- Data integration requirements: Salesforce provides prospect data (name, contact, financial information collected during discovery); the risk profiling tool provides the risk score and model mapping; Orion provides model portfolio details (holdings, allocation, historical performance); Schwab provides account data for current portfolio analysis (via account aggregation or statement import); the proposal system assembles all data into the selected template.
- Compliance workflow: after the advisor generates a proposal, it enters a compliance review queue. The compliance reviewer checks suitability alignment, performance data accuracy, fee calculation correctness, and disclaimer completeness. The system should flag proposals that deviate from standard model mappings or contain customized language that has not been pre-approved. Approved proposals are released for delivery; rejected proposals return to the advisor with specific correction requirements.
- Version control: when model portfolios are updated (quarterly rebalance, fund substitution), all templates must be refreshed. Proposals generated before the update should be flagged if they are still pending delivery, as they contain stale data. The system should prevent delivery of proposals with outdated model information.

**Analysis:** The recommended implementation plan: (1) Phase 1 — Template design (weeks 1-4): Work with the compliance team to define the locked compliance sections: disclaimers, performance presentation format, fee disclosure format, and required disclosures. Create the 7 model-specific content blocks with CCO approval. Design the modular components. Build the master template in the proposal platform with content controls that prevent unauthorized editing of locked sections. (2) Phase 2 — Integration (weeks 3-8): Connect Salesforce (prospect data), the risk profiling tool (risk score and model mapping), and Orion (model details and current portfolio data) to the proposal platform via API. Implement the compliance review workflow with status tracking, reviewer assignment, and approval/rejection routing. (3) Phase 3 — Pilot (weeks 8-10): Deploy to 3-5 advisors for testing. Gather feedback on usability, template quality, data accuracy, and compliance workflow efficiency. Identify edge cases that the templates do not handle well (complex trusts, institutional prospects, prospects with annuities). (4) Phase 4 — Rollout (weeks 10-14): Train all 25 advisors. Provide proposal generation guides and best practices. Establish metrics: proposals generated per advisor per month, compliance review turnaround time, revision rate (percentage of proposals requiring revisions), and time from proposal generation to client acceptance. (5) Ongoing governance: Quarterly template review aligned with model portfolio rebalancing. Annual compliance review of all template content. Advisor feedback loop for template improvements. Dashboard monitoring proposal pipeline, compliance review backlog, and conversion rates. The expected outcome is a reduction in proposal generation time from 3-5 hours (ad-hoc PowerPoint/Excel) to 30-60 minutes (templated, data-integrated), a near-elimination of compliance errors in delivered proposals, and consistent brand and message quality across all 25 advisors.


---

## SKILL: real-assets

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/real-assets` (MIT)
- Cuándo usarla: Analyze real estate and infrastructure investments including REITs, direct property valuation, and infrastructure assets. Use when the user asks about real estate investing, REITs, cap rates, NOI, FFO, AFFO, property valuation, or infrastructure investments. Also trigger when users mention 'rental property analysis', 'cash-on-cash return', 'gross rent multiplier', 'REIT dividends', 'real estate sectors', 'cell towers', 'toll roads', 'LTV ratio', 'DSCR', or ask whether to invest in real estate directly or through REITs.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/wealth-management/skills/real-assets/` (real_assets.py)

# Real Assets

## Core Concepts

### Property Income and Return Metrics
- **NOI (Net Operating Income):** effective gross rental income (after vacancy) minus operating expenses; excludes debt service, capex, and depreciation.
- **Cap rate:** NOI divided by property value — the unlevered property yield; lower cap rates mean higher valuations.
- **Income-approach value:** NOI divided by the prevailing cap rate for comparable properties.
- **Cash-on-cash return:** annual pre-tax cash flow (NOI minus debt service) divided by total cash invested — the levered equity yield.
- **GRM (Gross Rent Multiplier):** price divided by gross annual rent; a quick screen that ignores expenses, vacancy, and financing.

### REITs and REIT Metrics
REITs must distribute 90%+ of taxable income as dividends and trade on exchanges like equities. Sectors include residential, office, retail, industrial, data center, healthcare, self-storage, and specialty.

- **FFO (Funds From Operations):** net income plus depreciation minus gains on property sales — the standard REIT earnings measure, since real estate depreciation overstates actual value decline.
- **AFFO (Adjusted FFO):** FFO minus maintenance capex and straight-line rent adjustments — the conservative measure of recurring distributable cash flow.
- **P/FFO and P/AFFO:** the REIT equivalents of P/E; compare within the same sector.
- **NAV premium/discount:** share price relative to per-share net asset value of the underlying properties; indicates market sentiment.

### Infrastructure Investments
Infrastructure assets include toll roads, utilities, pipelines, cell towers, airports, and ports. Characteristics: long asset lives, high barriers to entry, regulated or contracted revenue streams, and inflation-linked cash flows (many contracts include CPI adjustments). Infrastructure provides stable, bond-like income with equity-like upside from traffic/usage growth.

### Leverage in Real Estate
- **LTV (Loan-to-Value):** mortgage amount / property value. Higher LTV means more leverage and more risk. Typical commercial LTV is 60-75%.
- **DSCR (Debt Service Coverage Ratio):** NOI / annual debt service. Lenders typically require 1.20x-1.50x minimum. Higher DSCR means more cushion to service debt.

## Direct Real Estate vs REITs: Decision Checklist

Work through these factors before recommending a vehicle:

| Factor | Direct ownership | REITs |
|--------|------------------|-------|
| Liquidity | Sales take months; high transaction costs | Trade intraday on exchanges |
| Management | Active management required, or pay a property manager | Passive; professional management included |
| Leverage access | Non-recourse mortgage leverage at attractive LTVs (60-75%), chosen by the investor | Entity-level leverage set by REIT management; investors cannot choose property-level leverage |
| 1031 exchange | Eligible — defer capital gains by exchanging into like-kind property | Not eligible — REIT shares do not qualify |
| Diversification | Concentrated in one or a few properties | A REIT fund spreads across hundreds of properties and multiple sectors |
| Minimum check size | Typically $50K+ equity (down payment plus closing costs) | From one share |

Mapping investor situations to the preferred vehicle:

| Investor situation | Preferred vehicle |
|--------------------|-------------------|
| May need the money within months, or rebalances regularly | REITs |
| Wants control over leverage, tenants, and improvements | Direct |
| Holds appreciated property and wants tax-deferred reinvestment | Direct (1031 exchange) |
| Allocation under ~$50K, or wants broad diversification immediately | REITs |
| Willing to manage tenants and repairs (or pay a manager from rent) | Direct |
| Wants passive, hands-off exposure with no operational involvement | REITs |

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| NOI | Gross Rental Income - Operating Expenses | Property income measure |
| Cap Rate | NOI / Property Value | Unlevered property yield |
| Property Value | NOI / Cap Rate | Income-based valuation |
| Cash-on-Cash | Annual Cash Flow / Total Cash Invested | Levered equity return |
| GRM | Price / Gross Annual Rent | Quick screening metric |
| FFO | Net Income + Depreciation - Gains on Sales | REIT earnings measure |
| AFFO | FFO - Maintenance Capex - Straight-Line Rent Adj | Recurring cash flow |
| LTV | Loan Amount / Property Value | Leverage measure |
| DSCR | NOI / Annual Debt Service | Debt coverage measure |

## Worked Examples

### Example 1: Property Valuation Using Cap Rate
**Given:** NOI = $100,000 per year, prevailing cap rate for comparable properties = 6%
**Calculate:** Property value
**Solution:**
Value = NOI / Cap Rate = $100,000 / 0.06 = $1,666,667

The property is valued at approximately $1,666,667. If the cap rate compressed to 5% (e.g., in a hot market), the value would rise to $2,000,000 — a 20% increase from a 100bp cap rate decline. This illustrates the sensitivity of real estate values to cap rate changes.

### Example 2: Cash-on-Cash Return with Leverage
**Given:** Property value = $500,000, down payment = $200,000 (40%), mortgage = $300,000 at 6%, NOI = $35,000, annual debt service = $17,000
**Calculate:** Cash-on-cash return
**Solution:**
Annual pre-tax cash flow = NOI - Debt Service = $35,000 - $17,000 = $18,000
Cash-on-Cash Return = $18,000 / $200,000 = 9.0%

Compare to the unlevered cap rate: $35,000 / $500,000 = 7.0%. Leverage boosts the equity return from 7.0% to 9.0% because the cost of debt (6%) is below the cap rate (7.0%) — this is positive leverage. If the mortgage rate exceeded the cap rate, leverage would reduce returns (negative leverage).

## Common Pitfalls
- Confusing cap rate with total return — cap rate ignores appreciation, leverage effects, and capital expenditures
- Using P/E instead of P/FFO for REITs — depreciation distorts net income, making P/E misleading for real estate companies
- Ignoring vacancy rates in NOI calculation — always use effective gross income (after vacancy allowance), not gross potential rent
- Overstating returns by ignoring maintenance capex — use AFFO rather than FFO for a realistic view of distributable cash flow

## Cross-References
- **time-value-of-money** (core plugin): discounted cash flow analysis of property investments
- **equities** (wealth-management plugin): REIT stock analysis and equity market context
- **fixed-income-structured** (wealth-management plugin): MBS and the mortgage market underlying real estate
- **asset-allocation** (wealth-management plugin): real assets as a portfolio diversifier and inflation hedge

## Running the script

```
uv run scripts/real_assets.py
```

The PEP 723 header resolves the numpy dependency automatically. Alternatively run `python3 scripts/real_assets.py` after `pip install numpy`.

- Bare run prints a demo covering property valuation, cash-on-cash and leverage analysis, REIT metrics, and inflation-adjusted returns.
- `--verify` re-runs the demo computations and asserts the outputs match this skill's worked examples (prints PASS/FAIL, nonzero exit on mismatch).
- `--help` lists the available classes.

The file is primarily meant to be imported as a module, e.g. `from real_assets import PropertyValuation, LeverageMetrics, REITMetrics, RealReturn`.


---

## SKILL: retirement-decumulation

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/retirement-decumulation` (MIT)
- Cuándo usarla: Turn a retirement portfolio into sustainable lifetime income: sequence-of-returns risk, the 4% rule and its assumptions, Guyton-Klinger-style guardrails, RMD calculation from the Uniform Lifetime Table, Social Security claiming math (early reduction, delayed credits, breakeven age, survivor benefits), gap-year bracket-filling with Roth conversions, bucket strategies vs total-return, and SPIA annuitization as longevity insurance. Use when the user asks about a 'safe withdrawal rate', 'when should I claim Social Security', a 'guardrails strategy', 'sequence of returns risk', or 'how much can I spend in retirement'. Also trigger on RMD amounts or missed-RMD penalties, Social Security breakeven analysis, '4% rule', 'bucket strategy', retirement paycheck design, drawdown or decumulation planning, and whether to buy an annuity. For accumulation-side savings math, see savings-goals; for asset location and tax mechanics, see tax-efficiency.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/wealth-management/skills/retirement-decumulation/` (retirement_decumulation.py)

# Retirement Decumulation

## Core Concepts

### Sequence-of-Returns Risk
Two retirees earning identical average returns can finish with very different wealth if the returns arrive in a different order while money is being withdrawn. Without withdrawals, order is irrelevant — multiplication commutes. With withdrawals, dollars sold after a decline are gone permanently and never participate in the recovery, so poor early returns do disproportionate damage. The danger zone is roughly the five to ten years on either side of the retirement date. Mitigants: flexible spending rules (guardrails), a cash/short-bond buffer, reduced equity exposure near retirement (or a rising equity glide path), and part-time income that lowers the withdrawal rate in early years.

### Safe Withdrawal Rate (SWR) Framework
Bengen's 1994 study (extended by the 1998 Trinity study) found that an initial withdrawal of 4% of the portfolio, adjusted for inflation each year thereafter, survived every rolling 30-year US historical period with 50-75% stocks — the "4% rule." Its assumptions are also its criticisms: it relies on US historical returns (an unusually strong market), a fixed 30-year horizon, rigid inflation-adjusted spending with zero flexibility, and it ignores fees and taxes. Longer retirements, high starting valuations, or lower expected returns argue for 3-3.5% initial rates; dynamic rules (guardrails, amortization-based, RMD-style percent-of-balance) support higher initial rates because spending flexes with the portfolio.

### Guardrails (Guyton-Klinger-Style Decision Rules)
A concrete dynamic rule set:
- **Initial rate:** withdraw, e.g., 5.0% of the starting portfolio in year one.
- **Inflation rule:** each year, increase the prior dollar withdrawal by inflation.
- **Guardrails:** compute the current withdrawal rate = this year's withdrawal / current portfolio. Set guardrails at plus or minus 20% of the initial rate (for 5.0%: upper 6.0%, lower 4.0%).
- **Capital-preservation rule:** if the current rate rises above the upper guardrail, cut the withdrawal 10%.
- **Prosperity rule:** if the current rate falls below the lower guardrail, raise the withdrawal 10%.

The full Guyton-Klinger rule set also skips the inflation increase after a negative-return year. The trade-off: a higher starting income than the 4% rule, paid for with variable spending — the retiree must actually take the cuts when triggered.

### Required Minimum Distributions (RMDs)
RMDs from tax-deferred accounts begin at age 73 under SECURE 2.0, rising to 75 in 2033 for those born in 1960 or later. Mechanics:
- RMD = prior December 31 balance / distribution period (divisor) from the IRS Uniform Lifetime Table (use the Joint Life table instead if the sole beneficiary is a spouse more than 10 years younger).
- Uniform Lifetime Table excerpt (table effective 2022, current as of 2026): age 73 → 26.5, 75 → 24.6, 80 → 20.2, 85 → 16.0, 90 → 12.2.
- Missed-RMD penalty: 25% excise tax on the shortfall, reduced to 10% if corrected within the correction window (SECURE 2.0; previously 50%).
- The first RMD can be delayed until April 1 of the year after the first RMD year, but then two RMDs land in one tax year.
- Roth IRAs have no lifetime RMDs; since 2024, designated Roth 401(k) accounts are also exempt.
- An RMD is a distribution requirement, not a spending requirement — excess can be reinvested in taxable or given via qualified charitable distribution (QCD, available at age 70 1/2, limit indexed annually — verify the current figure).

### Social Security Claiming
Full retirement age (FRA) is 67 for those born in 1960 or later. The adjustment factors are statutory:
- **Early claiming:** benefit reduced 5/9 of 1% per month for the first 36 months before FRA, and 5/12 of 1% per month beyond 36. Claiming at 62 with FRA 67 (60 months early): 36 x 5/9% + 24 x 5/12% = 20% + 10% = 30% reduction — the retiree gets 70% of the Primary Insurance Amount (PIA).
- **Delayed retirement credits:** 2/3 of 1% per month (8% per year) for each month past FRA, up to age 70. Claiming at 70 with FRA 67: 36 x 2/3% = 24% increase — 124% of PIA.
- **Breakeven:** months after the later claim age = B_early x months_delayed / (B_late - B_early), ignoring COLAs and discounting (COLAs apply proportionally to both paths).
- **Survivor benefit:** the survivor keeps the larger of the two benefits, so delaying the higher earner's claim is longevity insurance on the second-to-die — breakeven for that decision should use joint life expectancy, which typically favors delay.
- Claiming before FRA while still working triggers the earnings test (threshold indexed annually — verify the current figure); withheld benefits are restored through recomputation at FRA.

### Withdrawal Sequencing and Gap-Year Bracket-Filling
The conventional order — taxable first, then tax-deferred, then Roth — preserves tax-free growth longest (see tax-efficiency for the tax mechanics and asset-location foundations). The decumulation refinement is the **gap years**: after retiring but before Social Security and RMDs begin, taxable-only withdrawals can leave the ordinary brackets nearly empty. Filling low brackets with partial Roth conversions (or tax-deferred withdrawals) in those years shrinks future RMDs, reduces the survivor's single-filer bracket exposure, and smooths lifetime tax rates — while watching Medicare IRMAA surcharge thresholds (indexed annually) that behave as cliffs. Delaying Social Security to 70 both earns delayed credits and widens the conversion window.

### Bucket Strategies vs Total-Return
A bucket strategy holds 1-2 years of spending in cash, several more years in bonds, and the remainder in equities; spending comes from cash, refilled from the growth buckets opportunistically. A total-return approach holds one target allocation and funds withdrawals by rebalancing. Mathematically a maintained bucket structure is close to a fixed allocation with rebalancing discipline; its real value is behavioral — retirees tolerate equity drawdowns better knowing near-term spending is secured. The main failure mode is leaving the refill rules undefined.

### Annuitization as Longevity Insurance
A single premium immediate annuity (SPIA) converts an irrevocable premium into lifetime income. Because payments pool longevity risk across annuitants, mortality credits let a SPIA sustain a higher payout rate than a self-insured portfolio at the same confidence level — insurance, not an investment to benchmark against market returns. A floor-and-upside design annuitizes enough (with Social Security) to cover essential expenses and invests the rest for growth. Trade-offs: nominal SPIAs carry inflation risk, liquidity and bequest are surrendered, and payments depend on insurer solvency (state guaranty association limits vary). Deferred income annuities and QLACs push income to advanced ages as a tail-longevity hedge (QLAC premium cap: $200,000 statutory base under SECURE 2.0, indexed annually — verify the current limit).

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Balance recursion (start-of-year withdrawal) | B_t = (B_{t-1} - W_t) x (1 + r_t) | Simulate a withdrawal plan / sequence risk |
| Inflation-adjusted withdrawal | W_t = W_1 x (1 + i)^(t-1) | Fixed-real spending path |
| Current withdrawal rate | CWR = W / B | Guardrail test each year |
| Guardrail bands | upper = r_0 x 1.20; lower = r_0 x 0.80 | Trigger thresholds |
| Guardrail adjustment | W' = W x 0.90 (cut) or W x 1.10 (raise) | Capital-preservation / prosperity rules |
| RMD | RMD = balance_Dec31 / divisor | Required minimum distribution |
| SS early reduction | factor = 1 - [min(m,36) x 5/9 + max(m-36,0) x 5/12]/100 | Benefit if claimed m months before FRA |
| SS delayed credit | factor = 1 + m x (2/3)/100 | Benefit if claimed m months after FRA (to 70) |
| SS breakeven | months after late claim = B_e x Δm / (B_l - B_e) | Age where delaying pulls ahead |

## Worked Examples

### Example 1: Sequence-of-returns risk
**Given:** $1,000,000 portfolio, $50,000 withdrawn at the start of each year (no inflation adjustment for clarity). Sequence A returns: -20%, +10%, +25%. Sequence B: the same returns reversed (+25%, +10%, -20%).
**Calculate:** Ending balances.
**Solution:**
- **No withdrawals:** both orderings end at $1,000,000 x 0.80 x 1.10 x 1.25 = **$1,100,000** — order is irrelevant.
- **Sequence A (crash first):** Y1: (1,000,000 - 50,000) x 0.80 = 760,000. Y2: (760,000 - 50,000) x 1.10 = 781,000. Y3: (781,000 - 50,000) x 1.25 = **$913,750**.
- **Sequence B (crash last):** Y1: 950,000 x 1.25 = 1,187,500. Y2: 1,137,500 x 1.10 = 1,251,250. Y3: 1,201,250 x 0.80 = **$961,000**.
- Identical returns, identical withdrawals — the early-crash retiree ends **$47,250 poorer**. Over a 30-year retirement the same effect determines success or failure.

### Example 2: Guardrails adjustment
**Given:** Retiree starts with $1,000,000 and a 5.0% initial rate ($50,000). Guardrails at plus or minus 20% of 5.0%: upper 6.0%, lower 4.0%. Adjustments are 10%.
**Calculate:** The required action in a bad-market year and a strong-market year.
**Solution:**
- **Capital preservation:** after a bad year the portfolio is $780,000; the inflation-adjusted plan (3% inflation) calls for $50,000 x 1.03 = $51,500. Current rate = 51,500 / 780,000 = **6.60%** > 6.0% upper guardrail → cut 10%: new withdrawal = 51,500 x 0.90 = **$46,350** (rate 5.94%, back inside the bands).
- **Prosperity:** later the portfolio reaches $1,400,000 with a planned $52,000 withdrawal. Current rate = 52,000 / 1,400,000 = **3.71%** < 4.0% lower guardrail → raise 10%: new withdrawal = 52,000 x 1.10 = **$57,200** (rate 4.09%).

### Example 3: RMD at age 73
**Given:** Retiree turns 73 in 2026; the Traditional IRA balance on December 31 of the prior year was $850,000. Uniform Lifetime Table divisor at 73 = 26.5.
**Calculate:** The RMD and the penalty if entirely missed.
**Solution:**
- RMD = 850,000 / 26.5 = **$32,075.47** (about 3.77% of the balance).
- If entirely missed: 25% excise tax = 32,075.47 x 0.25 = **$8,018.87**; if corrected within the correction window, 10% = **$3,207.55**.

### Example 4: Social Security claiming breakeven
**Given:** PIA = $2,000/month at FRA 67 (born 1960 or later).
**Calculate:** Benefits at 62 and 70, and the breakeven ages (ignoring COLA and discounting).
**Solution:**
- **Claim at 62** (60 months early): reduction = 36 x 5/9% + 24 x 5/12% = 30% → **$1,400/month**.
- **Claim at 70** (36 months delayed): credit = 36 x 2/3% = 24% → **$2,480/month**.
- **62 vs 67:** head start = 60 x 1,400 = $84,000; monthly gain from waiting = $600. Breakeven = 84,000 / 600 = 140 months after 67 → age **78.7**.
- **67 vs 70:** head start = 36 x 2,000 = $72,000; monthly gain = $480. Breakeven = 72,000 / 480 = 150 months after 70 → age **82.5**.
- A single claimant expecting to live past roughly 80-82 gains from delaying; for couples, the higher earner's delay is evaluated on joint life expectancy because of the survivor benefit.

## Common Pitfalls
- Treating the 4% rule as a guarantee rather than a historical US backtest with rigid assumptions — and applying it to 40-year early retirements or high-fee portfolios unadjusted
- Planning with average returns and ignoring sequence: a Monte Carlo mean hides the early-crash paths that deplete portfolios
- Adopting guardrails but refusing the spending cut when the capital-preservation rule triggers — the higher initial rate is only safe because of the cuts
- Treating the RMD as a spending rule: it forces a taxable distribution, not consumption, and it is a floor, not a plan
- Missing the two-RMDs-in-one-year trap when delaying the first RMD to April 1
- Claiming Social Security at 62 by default, ignoring the survivor benefit — the higher earner's early claim permanently reduces the widow(er)'s income
- Running Roth conversions that trip IRMAA surcharge cliffs or push conversion income into the next bracket
- Leaving bucket refill rules undefined, so the strategy silently drifts to an ad hoc allocation
- Judging a SPIA as an investment by implied return instead of as longevity insurance priced with mortality credits — or annuitizing so much that liquidity and bequest goals fail

## Cross-References
- **savings-goals** (wealth-management plugin): the accumulation-side counterpart — the safe withdrawal rate sizes the nest egg target that savings plans aim for
- **tax-efficiency** (wealth-management plugin): asset location, Roth conversion breakeven, and the tax mechanics behind withdrawal sequencing and RMDs
- **asset-allocation** (wealth-management plugin): glide paths and the equity/bond mix that governs sequence-risk exposure in decumulation
- **historical-risk** (wealth-management plugin): drawdown and volatility measures that quantify the return sequences retirees must survive
- **emergency-fund** (wealth-management plugin): the cash-reserve discipline that becomes bucket one of a retirement bucket strategy
- **investment-policy** (wealth-management plugin): the IPS documents the spending policy, guardrail rules, and rebalancing discipline for decumulation
- **financial-planning-workflow** (advisory-practice plugin): decumulation strategy is a core deliverable of the retirement-income phase of a comprehensive plan

## Running the script
Run the reference implementation directly:

```
uv run scripts/retirement_decumulation.py      # PEP 723 header resolves dependencies automatically
python3 scripts/retirement_decumulation.py     # standard library only — no installs needed
```

A bare run prints a demo covering sequence-of-returns comparison, guardrails adjustments, RMD calculation and penalties, Social Security claiming factors, and breakeven ages. Use `--verify` to recompute the demo figures and assert they match this skill's worked examples (prints PASS/FAIL, exits nonzero on mismatch), and `--help` to list the available classes and functions. The file is primarily meant to be imported as a module (`from retirement_decumulation import RetirementDecumulation`) rather than run standalone.


---

## SKILL: savings-goals

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/savings-goals` (MIT)
- Cuándo usarla: Plan and track savings for specific financial goals including retirement, education, and home purchase. Use when the user asks about required savings rates, 529 plans, retirement accumulation targets, down payment planning, or goal prioritization. Also trigger when users mention 'how much do I need to save each month', 'am I on track for retirement', 'college savings', 'safe withdrawal rate', '4% rule', 'FIRE savings rate', 'catch-up contributions', 'employer match', or ask how to balance competing savings goals.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/wealth-management/skills/savings-goals/` (savings_goals.py)

# Savings Goals

## Core Concepts

### Required Monthly Savings
To accumulate a future value FV in n periods at rate r per period:

PMT = FV × r / [(1+r)^n - 1]

This is the sinking fund formula (future value of annuity solved for PMT).

### Inflation-Adjusted Targets
Always compute goals in future (nominal) dollars:

FV_nominal = FV_today × (1 + inflation)^years

Then solve for the required savings using the nominal return, or use the real return with today's dollars.

### Education Funding
- **529 plans**: tax-free growth for qualified education expenses, state tax deductions in many states
- **Current costs** (2025-26, total cost of attendance, College Board Trends in College Pricing): ~$30K/year (public four-year in-state) to ~$65K/year (private nonprofit), growing ~5%/year
- **Front-loading**: maximize early contributions for compound growth
- **Superfunding**: 5-year gift tax averaging (contribute 5× annual exclusion at once)
- **Financial aid impact**: parent-owned 529 assets are assessed at a maximum of 5.64% in the federal Student Aid Index (SAI) formula — FAFSA has used the SAI in place of the Expected Family Contribution (EFC) since the 2024-25 award year

### Retirement Accumulation
- **Target nest egg**: annual spending need / safe withdrawal rate
  - Example: $80K/year spending / 0.04 = $2,000,000
- **Safe withdrawal rate**: traditionally 4% (Bengen rule), adjusted for fees, taxes, longevity
- **Required savings rate**: depends on starting age, current savings, expected returns
- **Employer match**: always capture full match — it's an immediate 50-100% return
- **Catch-up contributions**: additional 401(k)/IRA contributions allowed after age 50

### Down Payment Saving
- Typical target: 20% of home price (avoids PMI)
- Timeline: typically 2-7 years → conservative allocation (HYSA, short-term bonds)
- Include closing costs (2-5% of purchase price) in savings target

### Goal Priority Framework
Recommended priority order:
1. Emergency fund (3-6 months expenses)
2. Employer 401(k) match (free money)
3. High-interest debt payoff (>6-8% rate)
4. HSA (triple tax advantage if eligible)
5. Max retirement accounts (401k, IRA, Roth)
6. Education funding (529)
7. Other goals (home, vacation, etc.)

### Multiple Goal Balancing
- Allocate savings across goals based on priority, timeline, and flexibility
- Non-negotiable goals (retirement) take precedence over flexible goals
- Shorter timelines need more conservative investment allocation
- Use goal-based investing: separate sub-portfolios per goal with appropriate risk

### Savings Rate Benchmarks
- Minimum: 15% of gross income for retirement (including employer match)
- Aggressive: 25-50%+ for early retirement / FIRE
- Savings rate = total savings / gross income

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Required savings (PMT) | PMT = FV × r / [(1+r)^n - 1] | Monthly savings for a goal |
| Future value with savings | FV = PV(1+r)^n + PMT×[(1+r)^n - 1]/r | Project goal balance |
| Inflation adjustment | FV_real = FV_today × (1+π)^t | Convert today's dollars to future |
| Retirement target | Nest egg = annual spend / SWR | Size the retirement goal |
| Years to goal | n = ln(FV×r/PMT + 1) / ln(1+r) | How long until goal is funded |
| Savings rate | SR = total savings / gross income | Track savings discipline |

## Worked Examples

### Example 1: College Savings (529)
**Given:** Need $200,000 in 18 years, expect 7% annual return, starting from $0
**Calculate:** Required monthly savings
**Solution:**
- Monthly rate: r = 0.07/12 = 0.005833
- Months: n = 18 × 12 = 216
- PMT = $200,000 × 0.005833 / [(1.005833)^216 - 1]
- PMT = $1,166.67 / [3.5125 - 1]
- PMT = $1,166.67 / 2.5125 = **$464.34/month**

### Example 2: Retirement Accumulation
**Given:** Age 30, $50,000 currently saved, wants $2,000,000 by age 65, expects 8% annual return
**Calculate:** Required monthly savings
**Solution:**
- Monthly rate: r = 0.08/12 = 0.006667; months: n = 35 × 12 = 420
- FV of current savings (monthly compounding): $50,000 × (1.006667)^420 = $50,000 × 16.2925 = $814,627
- Remaining needed: $2,000,000 - $814,627 = $1,185,373
- PMT = $1,185,373 × 0.006667 / [(1.006667)^420 - 1]
- PMT = $7,902.49 / [16.2925 - 1]
- PMT = $7,902.49 / 15.2925 = **$517/month**
- With employer match of $200/mo: personal contribution = **$317/month**

## Common Pitfalls
- Not inflation-adjusting future goals (college in 18 years costs much more than today)
- Neglecting employer match — it's the highest guaranteed return available
- Too conservative allocation for long-horizon goals (20+ years can tolerate equity risk)
- Saving for college before adequately funding retirement (retirement has no financial aid)
- Not revisiting savings rate as income grows (lifestyle creep absorbs raises)
- Using average returns without considering sequence risk near goal date

## Cross-References
- **time-value-of-money** (core plugin): FV/PV calculations, annuity formulas
- **emergency-fund** (wealth-management plugin): must be funded before other goals
- **debt-management** (wealth-management plugin): high-interest debt payoff competes with savings
- **tax-efficiency** (wealth-management plugin): 529 tax benefits, Roth vs traditional, HSA
- **investment-policy** (wealth-management plugin): goal-based allocation aligns with IPS constraints
- **asset-allocation** (wealth-management plugin): glide paths for target-date retirement savings
- **finance-psychology** (wealth-management plugin): mental accounting, present bias, commitment devices
- **financial-planning-workflow** (advisory-practice plugin): savings goals are key inputs to the comprehensive financial planning process
- **insurance-planning** (wealth-management plugin): education and survivor-income goals feed the capital-needs calculation for life insurance sizing
- **estate-gifting** (wealth-management plugin): 529 superfunding (5-year gift-tax election) lets grandparents front-load education goals within annual exclusions
- **retirement-decumulation** (wealth-management plugin): the drawdown-side counterpart — safe withdrawal rates and spending rules for the nest egg accumulated here
## Running the script
Run the reference implementation directly:

```
uv run scripts/savings_goals.py      # PEP 723 header resolves dependencies automatically
python3 scripts/savings_goals.py     # standard library only — no installs needed
```

A bare run prints a demo covering required monthly savings, retirement accumulation, time-to-goal, inflation adjustment, shortfall analysis, education funding, savings rate, and real returns. Use `--verify` to recompute the demo figures and assert they match this skill's worked examples (prints PASS/FAIL, exits nonzero on mismatch), and `--help` to list the available classes and functions. The file is primarily meant to be imported as a module (`from savings_goals import SavingsGoals`) rather than run standalone.


---

## SKILL: tax-efficiency

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/tax-efficiency` (MIT)
- Cuándo usarla: Maximizes after-tax returns through strategic asset location, gain/loss management, and withdrawal sequencing. Use when the user asks about asset location, Roth conversions, tax-efficient withdrawals, tax lot selection, or charitable giving with appreciated securities. Also trigger when users mention 'which account should I hold bonds in', 'tax drag', 'Roth vs Traditional', 'RMD planning', 'bracket stuffing', 'HIFO vs FIFO', or ask how to minimize taxes on investments. For tax-loss harvesting execution and wash-sale mechanics, see the tax-loss-harvesting skill.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/wealth-management/skills/tax-efficiency/` (tax_efficiency.py)

# Tax-Efficient Investing

## Core Concepts

### Asset Location
Place tax-inefficient assets in tax-advantaged accounts and tax-efficient assets in taxable accounts:

- **Tax-deferred accounts (Traditional IRA, 401k):** Bonds, REITs, high-turnover funds, TIPS — assets generating ordinary income
- **Tax-exempt accounts (Roth IRA, Roth 401k):** Highest expected growth assets — all growth is permanently tax-free
- **Taxable accounts:** Index equity funds (low turnover, qualified dividends, tax-loss harvesting eligible), municipal bonds, tax-managed funds

The benefit of asset location increases with the spread between ordinary income tax rates and capital gains rates, and with the size of the tax-advantaged accounts relative to total portfolio.

### Tax-Loss Harvesting (TLH)
Realize investment losses to offset capital gains, reducing current tax liability while maintaining market exposure:

- Sell a losing position, immediately buy a similar (but not "substantially identical") replacement
- Harvested losses offset gains dollar-for-dollar; net losses offset up to $3,000 of ordinary income per year; excess carries forward indefinitely
- **Wash-sale rule (61-day window):** Cannot repurchase the same or substantially identical security within the 61-day window (30 days before + sale date + 30 days after) — applies across all accounts (including spouse's accounts and IRAs)
- **Tax alpha from TLH:** Estimated 0.5-1.5% per year in early years of a portfolio's life, declining as cost basis rises
- Best opportunities arise during market volatility and in the first few years of investing

### After-Tax Return
Different income types face different tax rates:

- **Interest income:** Taxed at ordinary income rates
- **Qualified dividends:** Taxed at long-term capital gains rates (0%, 15%, or 20% + 3.8% NIIT)
- **Short-term capital gains (held ≤ 1 year):** Ordinary income rates
- **Long-term capital gains (held > 1 year):** Preferential rates (0%, 15%, or 20% + 3.8% NIIT)
- The 3.8% NIIT applies above $250,000 MAGI (MFJ) — a statutory threshold that is not inflation-indexed
- After-tax return on income: R_at = R × (1 - t)
- Capital gains are taxed only at realization, providing a deferral benefit

### Tax Drag
The annual cost of taxes on investment returns:

- Tax drag = pre-tax return - after-tax return
- High-turnover funds generate more short-term gains → higher tax drag
- Index funds with low turnover minimize tax drag
- ETFs generally more tax-efficient than mutual funds (in-kind creation/redemption process)

### Tax Lot Management
When selling partial positions, the method of selecting which lots to sell affects tax liability:

- **Specific identification:** Choose exactly which lots to sell
- **HIFO (Highest In, First Out):** Sell highest-cost-basis lots first to minimize gains
- **FIFO (First In, First Out):** Default method; may realize larger gains on older lots
- **Tax-optimal:** Select lots to minimize current-year tax liability considering holding period and gains/losses

### Roth Conversion
Convert Traditional IRA/401k assets to Roth, paying ordinary income tax now for tax-free growth and withdrawals later:

- **Breakeven analysis:** Conversion is beneficial if current marginal tax rate < expected future marginal tax rate
- **Factors favoring conversion:** Long time horizon, low current income year, expectation of higher future rates, desire to reduce future RMDs, estate planning benefits
- **Partial conversions:** Convert just enough to fill current tax bracket ("bracket stuffing")
- Tax on conversion: conversion amount × current marginal rate

### Required Minimum Distributions (RMDs)
Mandatory annual withdrawals from tax-deferred accounts (Traditional IRA, 401k) beginning at age 73 (under SECURE 2.0, rising to 75 in 2033):

- RMD = account balance (Dec 31 prior year) / distribution period (from IRS Uniform Lifetime Table)
- Failure penalty: 25% excise tax on shortfall (reduced from prior 50%)
- RMDs are taxed as ordinary income and can push retirees into higher brackets
- Roth IRAs have no RMDs during the owner's lifetime

### Withdrawal Sequencing
The order of withdrawals from different account types in retirement:

- **General rule:** Taxable → Tax-deferred → Roth (preserves tax-free growth longest)
- **Optimized approach:** Withdraw from taxable first, then fill low tax brackets with tax-deferred withdrawals, use Roth to avoid bracket jumps
- **Dynamic strategy:** Adjust each year based on income, deductions, and bracket thresholds

### Charitable Giving Strategies
- **Donate appreciated stock:** Avoid capital gains tax and deduct full fair market value (must be held > 1 year)
- **Qualified Charitable Distributions (QCDs):** Donate up to $111,000/year (2026 limit, indexed annually) directly from IRA to charity (counts toward RMD, excluded from taxable income); available at age 70½+
- **Donor-Advised Funds (DAFs):** Bunch multiple years of donations for itemized deduction, invest tax-free, distribute to charities over time

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| After-tax return (income) | R_at = R × (1 - t) | Bond/interest income after tax |
| After-tax return (deferred gains) | R_at = ((1 + R)^n × (1 - t_cg) + t_cg)^(1/n) - 1 | Unrealized equity with deferral benefit |
| Tax-loss harvesting value | TLH_value = loss × marginal_tax_rate | Immediate tax benefit of harvesting |
| Roth conversion breakeven | t_now < t_future | Convert when current rate < future rate |
| RMD amount | RMD = balance_Dec31 / distribution_period | Required minimum distribution |
| Appreciated-stock donation benefit | Tax saved = FMV × t_income + gain × t_cg_avoided | Tax benefit of donating appreciated stock (deduction + avoided gains tax) |

## Worked Examples

### Example 1: Asset location optimization
**Given:** $500K in taxable brokerage + $500K in Traditional IRA. Portfolio target: 50% bonds (yielding 5%) and 50% equities (expected 10% total return, 2% qualified dividends). Marginal tax rate: 32% ordinary, 15% LTCG.
**Calculate:** Optimal asset placement and annual tax savings vs naive allocation.
**Solution:**
1. **Optimal placement:** Bonds ($500K) in IRA; Equities ($500K) in taxable.
2. **Naive placement (50/50 each):** Taxable has $250K bonds + $250K equities; IRA has $250K bonds + $250K equities.
3. **Tax drag — naive:** Taxable bonds: $250K × 5% × 32% = $4,000. Taxable equity dividends: $250K × 2% × 15% = $750. Total tax = $4,750.
4. **Tax drag — optimal:** Taxable equity dividends only: $500K × 2% × 15% = $1,500. Total tax = $1,500.
5. **Annual tax savings:** $4,750 - $1,500 = **$3,250/year** (0.325% of total portfolio).
6. Over 20 years compounded, this adds significantly to after-tax wealth.

### Example 2: Roth conversion breakeven
**Given:** Consider converting $50,000 from Traditional IRA to Roth. Current marginal tax rate: 24%. Tax on conversion paid from outside funds. Investment horizon: 20 years. Expected return: 7%.
**Simplifying assumption:** Assume the $12,000, if not used for conversion tax, would grow at the same 7% with no tax drag — i.e., side-fund growth itself is untaxed.
**Calculate:** Future marginal tax rate at which conversion breaks even.
**Solution:**
1. **Cost of conversion now:** $50,000 × 24% = $12,000 tax paid today.
2. **Traditional IRA path:** $50,000 grows to $50,000 × (1.07)^20 = $193,484. After-tax at withdrawal: $193,484 × (1 - t_future).
3. **Roth path:** $50,000 grows to $193,484 tax-free, but the $12,000 side fund forgoes growth to $12,000 × (1.07)^20 = $46,436. Roth net value: $193,484 - $46,436 = $147,048.
4. **Breakeven:** Set Traditional after-tax = Roth net value. $193,484 × (1 - t_future) = $193,484 - $46,436 → t_future = $46,436 / $193,484 = **24.0%**.
5. **Conclusion:** Under this simplification the breakeven future rate equals the current rate (24%) — both sides scale by the same (1.07)^20, so the horizon and return cancel. In reality the taxable side fund suffers tax drag on its dividends and realized gains, so paying conversion tax from outside funds tilts the comparison toward Roth even when the future rate merely equals the current rate.

## Common Pitfalls
- TLH wash sale violations, including purchases in other accounts, IRAs, or a spouse's account within the 61-day wash-sale window (30 days before through 30 days after the sale)
- Over-harvesting losses that defer gains to higher tax brackets later (basis step-down compounds)
- Not considering state taxes in asset location decisions — state tax treatment varies significantly
- Ignoring the tax benefit of donating appreciated securities vs cash (avoids capital gains and gets full deduction)
- RMD-driven forced selling at inopportune times — plan withdrawals ahead of deadlines
- Roth converting too aggressively and pushing into a higher bracket in the conversion year
- Forgetting the 3.8% Net Investment Income Tax (NIIT) above $250,000 MAGI (MFJ) — a statutory threshold that is not inflation-indexed, so it captures more taxpayers each year
- Not coordinating tax strategy across spouses' accounts

## Cross-References
- **investment-policy** (wealth-management plugin): Tax constraint in IPS governs asset location and turnover management
- **performance-attribution** (wealth-management plugin): After-tax return attribution requires tax-aware calculations
- **debt-management** (wealth-management plugin): Mortgage interest deductibility interacts with tax planning
- **savings-goals** (wealth-management plugin): Account type selection (Roth vs Traditional) is a core tax decision
- **liquidity-management** (wealth-management plugin): Tax implications of accessing different account types affect liquidity planning
- **tax-loss-harvesting** (wealth-management plugin): dedicated TLH workflow skill with detailed candidate identification, wash-sale tracking, and execution planning
- **financial-planning-workflow** (advisory-practice plugin): tax-aware strategies are core recommendations in comprehensive financial plans
- **financial-statements** (wealth-management plugin): cost basis and embedded capital gains fundamentals behind lot selection and deferral decisions
- **insurance-planning** (wealth-management plugin): premium-payer decisions drive taxation of disability benefits, annuity income, and life insurance proceeds
- **estate-gifting** (wealth-management plugin): owns the transfer-tax side — lifetime exemption, annual exclusion gifting, basis step-up vs carryover, and estate-level charitable structure choice
- **retirement-decumulation** (wealth-management plugin): applies withdrawal sequencing and RMD mechanics to retirement spending plans — guardrails, gap-year bracket-filling, and Social Security timing
- **equity-compensation** (wealth-management plugin): RSU/option taxation, AMT on ISO exercises, and charitable use of appreciated employer stock extend tax planning to compensation events
## Running the script
Run with `uv run scripts/tax_efficiency.py` (the PEP 723 header resolves dependencies automatically) or with `python3 scripts/tax_efficiency.py` after `pip install numpy scipy`. The bare run prints a demo covering after-tax returns, tax drag, TLH benefit, asset location placement, and Roth conversion breakeven. Pass `--verify` to assert the demo outputs match this skill's worked examples (prints PASS/FAIL), or `--help` for an overview of the available classes. The file is primarily meant to be imported as a module (e.g., `from tax_efficiency import AfterTaxReturn, AssetLocation, BreakevenAnalysis`).


---

## SKILL: tax-liability-tracking

- Fuente: `agiprolabs/claude-trading-skills` → `skills/tax-liability-tracking` (MIT)
- Cuándo usarla: Real-time tax liability analysis for active crypto traders with proportional cost basis, gain classification, and tax-aware trading signals
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/tax-liability-tracking/` (tax_tracker.py)

# Tax Liability Tracking

Real-time tax liability analysis purpose-built for active Solana traders. Track proportional cost basis across partial sells, classify realized vs unrealized gains, project quarterly tax obligations, and surface tax-aware signals that feed back into trading decisions.

## Why This Matters

Active crypto traders generate hundreds of taxable events per year. Without real-time tracking:

- You do not know your actual after-tax P&L until year-end
- Partial sells (the "house money" play) create cost basis confusion
- Short-term vs long-term classification shifts your effective tax rate by 15-20%
- Tax-loss harvesting windows close without you noticing
- Quarterly estimated payments become guesswork

This skill keeps a running tax ledger alongside your trading activity so every decision incorporates its tax consequence.

## Core Concepts

### Proportional Cost Basis for Partial Sells

This is the most critical concept. When you sell a portion of a position, the cost basis splits proportionally — it does not shift to zero for the remaining tokens.

**Example — The Accumulate / House-Money Play:**

1. **Buy**: 1,000 tokens at $1.00 each. Total cost basis = $1,000.
2. **Partial sell**: Sell 800 tokens at $1.25 each. Proceeds = $1,000.
3. **What happened**:
   - The 800 sold tokens had proportional cost basis = 800 x $1.00 = $800
   - Realized gain on the sale = $1,000 - $800 = **$200**
   - The remaining 200 tokens retain cost basis = 200 x $1.00 = **$200**
   - The remaining tokens are NOT "free" — they carry their original per-unit cost

**Common mistake**: Recording the partial sell as "capital recovered, remaining basis = $0." This understates the realized gain on the partial sell and overstates the gain when the remaining tokens are eventually sold. The total tax owed is the same either way, but the timing and classification (short-term vs long-term) can differ significantly.

### Gain Classification

| Classification | Holding Period | US Federal Rate (2024) |
|---|---|---|
| Short-term capital gain | < 1 year | Ordinary income rate (10-37%) |
| Long-term capital gain | >= 1 year | 0%, 15%, or 20% |

Each tax lot tracks its own acquisition date. Partial sells consume lots in the order specified by your accounting method (FIFO, LIFO, or specific identification).

### SOL-Denominated Trading with USD Reporting

Solana traders typically think in SOL but US tax obligations are denominated in USD. Every taxable event requires:

1. **SOL price at acquisition** — establishes USD cost basis
2. **SOL price at disposition** — establishes USD proceeds
3. **Token price in SOL at both events** — converted to USD via SOL/USD rate

The skill tracks SOL/USD rates at each event timestamp to compute USD-denominated gains.

### Realized vs Unrealized Gains

- **Realized**: Position closed (fully or partially). Taxable event occurred.
- **Unrealized**: Position still open. No tax event yet, but contributes to estimated liability if you plan to close before year-end.

The after-tax P&L view shows both, with unrealized gains marked at current estimated tax rates.

## Capabilities

### Tax Lot Tracking
- Record buys, sells, and token-to-token swaps as taxable events
- Maintain per-lot cost basis with acquisition date
- Support FIFO, LIFO, and specific identification accounting methods
- Handle partial sells with proportional cost basis allocation

### Gain Classification Engine
- Classify each realized gain as short-term or long-term
- Track days remaining until long-term threshold for each open lot
- Flag positions approaching the 1-year boundary

### Quarterly Tax Projection
- Estimate federal tax liability using progressive bracket rates
- Include state tax estimate (configurable rate)
- Project Q1-Q4 estimated payment amounts
- Track cumulative realized gains by quarter

### Tax-Aware Trading Signals
- **Long-term threshold alert**: "Position crosses long-term threshold in N days"
- **Profit-taking cost**: "Taking profit here triggers $X short-term liability"
- **Loss harvesting**: "You have $X in unrealized losses available to harvest"
- **Timing value**: "Selling now vs waiting 30 days saves $X in taxes"
- **Wash sale warning**: "Repurchasing within 30 days may trigger wash sale rules"

### After-Tax P&L View
- Standard trading P&L alongside estimated after-tax P&L
- Per-position breakdown of pre-tax and after-tax returns
- Running year-to-date tax liability total

## Prerequisites

- Python 3.10+
- No external dependencies for core tracking (stdlib only)
- Historical SOL/USD prices for accurate USD conversion
- Trade history in structured format (timestamp, side, token, amount, price)

## Quick Start

```python
from tax_tracker import TaxTracker, Trade

tracker = TaxTracker(
    accounting_method="fifo",
    federal_bracket=0.32,   # Your marginal federal rate
    state_rate=0.05,        # Your state income tax rate
    long_term_rate=0.15,    # Your long-term capital gains rate
)

# Record the accumulate/house-money play
tracker.add_trade(Trade(
    timestamp="2025-06-15T10:00:00Z",
    side="buy",
    token="BONK",
    amount=1_000_000,
    price_usd=0.00002,      # Per-token price in USD
    total_usd=20.00,
))

tracker.add_trade(Trade(
    timestamp="2025-07-20T14:30:00Z",
    side="sell",
    token="BONK",
    amount=800_000,          # Sell 80% to recover capital
    price_usd=0.000025,
    total_usd=20.00,
))

# Check what happened
summary = tracker.position_summary("BONK")
print(f"Realized gain: ${summary.realized_gain:.2f}")
# Realized gain: $4.00  (sold 800k at $0.000025 = $20, basis = $16, gain = $4)

print(f"Remaining basis: ${summary.remaining_cost_basis:.2f}")
# Remaining basis: $4.00  (200k tokens x $0.00002 = $4)

print(f"Classification: {summary.gain_type}")
# Classification: short-term  (held ~35 days)

# Tax-aware signals
signals = tracker.get_signals("BONK", current_price_usd=0.00003)
for signal in signals:
    print(f"  [{signal.type}] {signal.message}")
# [long_term_countdown] Position crosses long-term threshold in 330 days
# [profit_taking_cost] Taking full profit triggers $2.80 short-term liability
```

## Use Cases

### 1. Day Trader Tax Tracking
Track hundreds of daily trades, all short-term. Focus on quarterly estimated payment accuracy and cumulative liability.

### 2. Swing Trader with House-Money Plays
Partial sell to recover capital, let remaining position ride. Proportional cost basis ensures both legs are tracked correctly.

### 3. Long-Term Holder Monitoring
Track positions approaching the 1-year long-term threshold. Signals alert when selling now vs waiting N days changes the tax classification.

### 4. Tax-Loss Harvesting
Identify positions with unrealized losses. Harvest losses to offset gains while being mindful of wash sale rules.

### 5. Year-End Tax Planning
Project remaining quarterly liability, identify optimization opportunities before Dec 31.

### 6. Multi-Token Portfolio
Track cost basis and gains across dozens of tokens simultaneously, with per-token and aggregate views.

## Accounting Methods

### FIFO (First In, First Out)
Sells consume the oldest lots first. Default for most traders. Generally results in more long-term gains if you have been accumulating over time.

### LIFO (Last In, First Out)
Sells consume the newest lots first. Can minimize short-term gains if recent purchases were at higher prices.

### Specific Identification
Choose which lots to sell. Maximum flexibility for tax optimization, but requires careful record-keeping. Must be elected before the trade, not after.

## Integration with Trading Workflow

```
Trade Signal → Tax-Aware Filter → Execute/Defer Decision
                    │
                    ├─ "Short-term gain: $X liability"
                    ├─ "Long-term in N days — consider waiting"
                    ├─ "Loss harvest opportunity: $X offset"
                    └─ "Net after-tax profit: $Y"
```

The tax-aware filter does not block trades — it provides information so the trader can make informed decisions about timing.

## Files

### References
- `references/planned_features.md` — Detailed feature list, proportional cost basis math with worked examples, gain classification rules, quarterly estimation methodology

### Scripts
- `scripts/tax_tracker.py` — Demo implementation with proportional cost basis, gain classification, tax-aware signals, and quarterly projection. Run with `--demo` for an example accumulate/house-money scenario.

## Limitations

- US federal and state tax rules only (no international tax support yet)
- Does not handle staking rewards, airdrops, or DeFi yield as income events (planned)
- Wash sale rules are flagged but not automatically enforced
- Token-to-token swaps treated as sell + buy (two taxable events) per IRS guidance
- Does not generate official tax forms (use for tracking and planning only)

## Disclaimer

Tax calculations produced by this skill are for **informational tracking purposes only**. Cryptocurrency tax law is complex and evolving. All tax figures should be verified by a qualified tax professional before filing. This skill does not constitute tax advice. Consult a CPA or tax attorney for guidance specific to your situation.

### Referencia: references/planned_features.md

# Tax Liability Tracking — Planned Features & Methodology

## Feature Overview

### Core Tracking
- Per-trade tax lot creation with acquisition date, amount, per-unit cost basis
- Proportional cost basis allocation on partial sells
- FIFO, LIFO, and specific identification accounting methods
- Realized vs unrealized gain classification
- Short-term vs long-term gain classification with countdown timers

### Tax Projection
- Progressive federal bracket estimation
- Configurable state tax rate
- Quarterly estimated payment projection (Q1-Q4)
- Year-to-date cumulative liability tracking
- After-tax P&L view per position and aggregate

### Tax-Aware Signals
- Long-term threshold countdown per lot
- Profit-taking tax cost estimation
- Loss harvesting opportunity detection
- Timing value analysis (sell now vs wait N days)
- Wash sale proximity warning (30-day window)

### SOL/USD Conversion
- Historical SOL/USD price lookup at each event timestamp
- Token price in SOL converted to USD via SOL/USD rate
- All tax figures reported in USD per IRS requirements

---

## Proportional Cost Basis — Detailed Math

### The Rule

When selling a fraction of a position, cost basis is allocated proportionally:

```
sold_basis = (amount_sold / total_amount) * total_cost_basis
remaining_basis = total_cost_basis - sold_basis
```

This is equivalent to:

```
per_unit_basis = total_cost_basis / total_amount
sold_basis = amount_sold * per_unit_basis
remaining_basis = amount_remaining * per_unit_basis
```

### Worked Example 1 — House-Money Play

**Setup**: Buy 1,000 tokens at $1.00 each.

| Field | Value |
|---|---|
| Total amount | 1,000 |
| Per-unit basis | $1.00 |
| Total basis | $1,000.00 |

**Partial sell**: Sell 800 tokens at $1.25 each.

| Calculation | Value |
|---|---|
| Proceeds | 800 x $1.25 = $1,000.00 |
| Sold basis | 800 x $1.00 = $800.00 |
| Realized gain | $1,000.00 - $800.00 = **$200.00** |
| Remaining amount | 200 |
| Remaining basis | 200 x $1.00 = **$200.00** |

**Later sell**: Sell remaining 200 tokens at $2.00 each.

| Calculation | Value |
|---|---|
| Proceeds | 200 x $2.00 = $400.00 |
| Sold basis | 200 x $1.00 = $200.00 |
| Realized gain | $400.00 - $200.00 = **$200.00** |

**Total gain across both sells**: $200 + $200 = $400.

**Verification**: Total proceeds ($1,000 + $400 = $1,400) minus total basis ($1,000) = $400. Correct.

### Worked Example 2 — Multiple Accumulations

**Buy 1**: 500 tokens at $0.50 = $250 basis.
**Buy 2**: 300 tokens at $0.80 = $240 basis.
**Total**: 800 tokens, $490 total basis.

**Partial sell (FIFO)**: Sell 600 tokens at $1.00.

Under FIFO, the 600 sold tokens come from:
- Lot 1: 500 tokens at $0.50 = $250 basis
- Lot 2: 100 tokens at $0.80 = $80 basis
- Total sold basis = $330

| Calculation | Value |
|---|---|
| Proceeds | 600 x $1.00 = $600.00 |
| Sold basis (FIFO) | $250 + $80 = $330.00 |
| Realized gain | $600 - $330 = **$270.00** |
| Remaining | 200 tokens from Lot 2 |
| Remaining basis | 200 x $0.80 = **$160.00** |

### Worked Example 3 — Zero-Basis Misconception

**The wrong way** (do NOT do this):

Buy 1,000 at $1.00 ($1,000 basis). Sell 800 at $1.25 ($1,000 proceeds). "I recovered my capital, so remaining basis = $0."

This is **incorrect** because:
- It records $0 realized gain on the partial sell (understated by $200)
- It records $400 gain on the final sell of 200 tokens at $2.00 (overstated by $200)
- If the partial sell is in one tax year and the final sell in another, income shifts between years
- If the holding period crosses the 1-year boundary between sells, the gain classification changes

---

## Gain Classification Rules

### Holding Period Determination

- **Start date**: The date the tokens were acquired (trade settlement)
- **End date**: The date the tokens were disposed of
- **Short-term**: Holding period < 1 year (365 days)
- **Long-term**: Holding period >= 1 year

### Special Cases

**Token-to-token swaps**: Treated as two events — a sale of the source token and a purchase of the destination token. Both events use the USD value at the time of the swap.

**Wash sales**: If you sell at a loss and repurchase the same or "substantially identical" token within 30 days (before or after the sale), the loss may be disallowed. The disallowed loss is added to the basis of the repurchased tokens. Crypto wash sale rules are not yet codified in US tax law but may apply under proposed legislation.

**Airdrops and staking rewards**: Treated as ordinary income at fair market value when received. The FMV becomes the cost basis for future disposition.

---

## Quarterly Estimation Methodology

### US Estimated Tax Payments

Self-employed and high-income taxpayers must make quarterly estimated payments:

| Quarter | Period | Due Date |
|---|---|---|
| Q1 | Jan 1 — Mar 31 | April 15 |
| Q2 | Apr 1 — May 31 | June 15 |
| Q3 | Jun 1 — Aug 31 | September 15 |
| Q4 | Sep 1 — Dec 31 | January 15 (next year) |

### Estimation Formula

```
quarterly_liability = (realized_short_term_gains * short_term_rate
                     + realized_long_term_gains * long_term_rate
                     + state_gains * state_rate)
```

Where:
- `short_term_rate` = marginal federal income tax rate
- `long_term_rate` = 0%, 15%, or 20% based on total income
- `state_rate` = state income tax rate (varies by state, 0-13.3%)

### Safe Harbor Rule

To avoid underpayment penalties, pay the lesser of:
- 90% of current year tax liability, or
- 100% of prior year tax liability (110% if AGI > $150,000)

The tracker projects based on year-to-date realized gains annualized, then compares against safe harbor thresholds.

---

## Planned Enhancements

### Phase 1 (Current)
- Core proportional cost basis tracking
- FIFO accounting method
- Short-term / long-term classification
- Basic quarterly projection
- Tax-aware trading signals

### Phase 2
- LIFO and specific identification methods
- Wash sale detection and basis adjustment
- Multi-year tracking with carryover losses
- CSV/JSON import from exchange exports

### Phase 3
- Staking reward and airdrop income tracking
- DeFi yield as ordinary income events
- LP position entry/exit as taxable events
- Integration with Helius transaction history API

### Phase 4
- Form 8949 data export
- TurboTax/TaxAct import format
- CoinTracker/Koinly reconciliation
- Multi-jurisdiction support (UK, EU, AU)


---

## SKILL: tax-loss-harvesting

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/tax-loss-harvesting` (MIT)
- Cuándo usarla: Execute a complete tax-loss harvesting workflow from candidate identification through post-harvest monitoring. Use when the user asks about finding TLH candidates, gain/loss budgeting, replacement security selection, wash-sale compliance, or harvest execution planning. Also trigger when users mention 'unrealized losses in my portfolio', 'swap ETFs for tax purposes', 'harvest losses before year-end', 'substantially identical security', 'wash-sale window', 'NIIT offset', 'loss carryforward', or ask how much tax they can save by harvesting.

# Tax-Loss Harvesting

## Core Concepts

### Candidate Identification
Scan the portfolio for positions with unrealized losses that meet all three filters:

- **Materiality threshold:** Minimum absolute loss (e.g., $2,000) or minimum loss-to-value ratio (e.g., loss exceeds 5% of position market value). Harvesting a $200 loss on a $50,000 portfolio is not worth the operational cost.
- **Holding period filter:** Positions held less than 31 days may not have meaningful losses and create short-term wash-sale complexity. Positions approaching the one-year mark (days 335-365) may benefit from waiting to convert a short-term loss into a long-term loss only if the position is expected to continue declining.
- **Loss magnitude ranking:** Rank candidates by Tax Benefit = Unrealized Loss * Applicable Tax Rate. Prioritize short-term losses (taxed at ordinary rates up to 37%) over long-term losses (taxed at capital gains rates of 15-20%) when gain/loss budget allows.

### Gain/Loss Budgeting
Before harvesting, build the year-to-date tax budget:

1. **Realized gains YTD:** Sum all short-term and long-term capital gains already realized (including fund distributions).
2. **Planned gain exposure:** Estimate gains from pending rebalancing trades, planned liquidations, or expected fund capital gain distributions.
3. **Loss carryforward balance:** Check prior-year unused capital loss carryforwards (these offset gains before new harvests do).
4. **Target harvest amount:** Target Harvest = (Realized Gains YTD + Planned Gains) - Loss Carryforward + $3,000 ordinary income offset. Harvesting this amount offsets all expected gains AND captures the full $3,000 annual deduction against ordinary income; harvest more to build carryforward for future years.

### Replacement Security Selection
The replacement must maintain market exposure without being "substantially identical":

- **ETF-to-ETF swaps:** Switch between funds tracking different indices (e.g., Vanguard Total Stock Market to Schwab Broad Market, or S&P 500 to Russell 1000). Different index methodology is generally sufficient.
- **Individual stock replacement:** Replace a single stock with a sector ETF or a peer company. Example: sell Apple, buy Technology Select Sector SPDR (XLK).
- **Tracking error budget:** The replacement should have a correlation of 0.95+ and tracking error under 2% annualized relative to the original holding. Wider tracking error is acceptable for larger tax benefits.
- **Expense ratio delta:** Ensure the replacement does not have meaningfully higher expenses. A 10 bps cost increase on a $100K position held for 30 days costs roughly $8 — negligible against a $2,000+ tax benefit.

### Wash-Sale Compliance
The wash-sale rule (IRC Section 1091) disallows a loss if a substantially identical security is acquired within the 61-day window (30 days before + sale date + 30 days after):

- **Cross-account scope:** The rule applies across ALL accounts owned by the taxpayer: taxable brokerage, Traditional IRA, Roth IRA, 401(k), HSA, and spouse's accounts. A purchase in any of these accounts triggers wash-sale disallowance.
- **IRA wash-sale trap:** If a wash sale is triggered by a purchase in an IRA, the disallowed loss is permanently lost — it cannot be added to the IRA cost basis. This is the most dangerous wash-sale scenario.
- **DRIP suspension:** Automatic dividend reinvestment (DRIP) in the sold security or a substantially identical fund must be suspended during the 61-day window. Reinvesting even a small dividend triggers a partial wash sale.
- **Spouse coordination:** Purchases in a spouse's accounts (including retirement accounts) trigger wash-sale rules. Both spouses' automatic investments, 401(k) contributions, and DRIP settings must be reviewed.

### Execution Planning
Translate candidates into an actionable trade list:

- **Lot selection method:** Use Specific Identification (Spec ID) to select the highest-cost-basis lots first (HIFO). This maximizes the realized loss per share sold. If only partial harvesting is needed, sell only the lots with cost basis above current market price.
- **Coordination with rebalancing:** If the portfolio also needs rebalancing, combine TLH sells with rebalance sells to reduce total trade count. A position that is both overweight and at a loss is the ideal candidate — the harvest and rebalance are the same trade.
- **Timing strategy:** Year-end harvesting (October-December) captures the full year's losses but faces market timing risk. Opportunistic harvesting throughout the year during drawdowns of 5%+ captures losses that may recover by year-end.
- **Trade list fields:** Security, account, action (sell/buy), shares, lot IDs, estimated loss, replacement security, wash-sale window start/end dates.

### Tax Savings Calculation
Quantify the dollar value of each proposed harvest:

- **Federal rate selection:** Short-term losses offset short-term gains first (up to 37% ordinary rate). Long-term losses offset long-term gains (15-20% rate). Net losses of either type can cross over to offset the other, then up to $3,000 offsets ordinary income.
- **State tax impact:** Most states tax capital gains as ordinary income (rates range from 0% up to California's top statutory rate on investment income of 13.3%; California's effective top rate on wage income is 14.4%+ since the 2024 SDI uncapping). Include state tax savings in the calculation; for a California resident at the 13.3% bracket, state tax roughly doubles the benefit of each harvest.
- **NIIT interaction:** The 3.8% Net Investment Income Tax (IRC Section 1411) applies to the lesser of net investment income or MAGI exceeding $250,000 (MFJ) — a statutory threshold that is not inflation-indexed. Harvested losses reduce net investment income, potentially eliminating NIIT exposure.

### Post-Harvest Monitoring
After executing the harvest:

- **Wash-sale window tracking:** Maintain a calendar of open wash-sale windows with security identifiers and expiration dates. Flag any pending purchases (including automated ones) that would violate the window.
- **Replacement performance:** Monitor tracking error between the replacement and original security. If the replacement significantly underperforms (>3% divergence), evaluate whether the tax benefit justified the swap.
- **Cost basis updates:** Verify that broker statements reflect the new (lower) cost basis on replacement securities. The replacement's basis equals purchase price, not the original security's basis.
- **Swap-back timing:** After the 31st day, the investor may sell the replacement and repurchase the original security if desired. Evaluate whether the swap-back itself triggers a taxable gain on the replacement position.

### Household-Level Coordination
TLH across a household with multiple accounts requires centralized tracking:

- **Account type matrix:** Taxable accounts are the only accounts where TLH generates direct tax benefits. Retirement accounts have no realized gains/losses for tax purposes, but they can trigger wash sales in taxable accounts.
- **Advisor-managed vs held-away:** If the client has accounts at other institutions (401(k) plan, outside brokerage), the advisor cannot control purchases. Document held-away holdings and instruct the client to avoid purchasing substantially identical securities during open wash-sale windows.
- **Spousal coordination checklist:** (1) Review spouse's 401(k) fund lineup for overlap, (2) suspend DRIP in spouse's accounts for harvested securities, (3) coordinate any year-end tax trades across both spouses.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Tax Benefit | Benefit = Realized_Loss * Applicable_Tax_Rate | Dollar value of a single harvest |
| Net Tax Alpha | Alpha = Tax_Savings - Tracking_Error_Cost - Transaction_Costs | True value after implementation costs |
| Break-Even Holding Period | T_be = Tax_Savings / (Annual_Tracking_Error_Cost + Annual_Expense_Delta) | How long replacement can be held before costs exceed benefit |
| Wash-Sale Adjusted Basis | New_Basis = Replacement_Purchase_Price + Disallowed_Loss | Cost basis when wash sale is triggered |
| Annual TLH Capacity | Capacity = Portfolio_Value * Expected_Volatility * Loss_Capture_Rate | Estimate of harvestable losses per year |
| Target Harvest Amount | Target = Realized_Gains_YTD + Planned_Gains - Loss_Carryforward + 3000 | Harvest needed to offset all gains plus the $3,000 ordinary-income deduction |

## Worked Examples

### Example 1: Single Position Harvest with Replacement Selection
**Given:**
- Client holds 500 shares of XYZ Corp purchased at $80/share ($40,000 cost basis), current price $62/share ($31,000 market value), held 8 months (short-term)
- Client has $12,000 in short-term realized gains YTD, marginal federal rate 35%, state rate 9.3%, NIIT applies (3.8%)
- Replacement candidate: Sector ETF (correlation 0.97, tracking error 1.4% annualized, expense ratio 0.10% vs 0% for individual stock)

**Calculate:** Tax benefit, net tax alpha, and break-even holding period for the replacement.

**Solution:**
1. **Unrealized loss:** $31,000 - $40,000 = -$9,000 (short-term)
2. **Applicable rate:** 35% federal + 9.3% state + 3.8% NIIT = 48.1% combined
3. **Tax benefit:** $9,000 * 48.1% = **$4,329**
4. **Transaction costs:** Commission $0 (zero-commission broker) + estimated spread cost 0.05% * $31,000 * 2 trades = $31
5. **Tracking error cost:** 1.4% annualized * $31,000 * (30/365) = **$36** (for the 30-day minimum hold)
6. **Net tax alpha:** $4,329 - $31 - $36 = **$4,262**
7. **Annual cost of replacement:** $31,000 * (0.10% expense + 1.4% tracking error drag estimate of 0.05%) = $46.50/year
8. **Break-even holding period:** $4,262 / $46.50 = **91.7 years** — the tax benefit overwhelmingly justifies the swap
9. **Action:** Sell XYZ Corp (Spec ID, all lots), buy Sector ETF. Set wash-sale window reminder for 31 calendar days. Suspend any XYZ DRIP in all household accounts.

### Example 2: Portfolio-Wide TLH Scan with Gain/Loss Budget
**Given:**
- $2M taxable portfolio, 15 equity positions, year is mid-October
- Realized gains YTD: $18,000 long-term, $5,000 short-term
- Loss carryforward from prior years: $0
- Planned rebalancing trades will realize approximately $4,000 in additional long-term gains
- Three positions show unrealized losses: Position A (-$14,000 LT), Position B (-$6,500 ST), Position C (-$2,100 LT)
- Federal LTCG rate 20%, ordinary rate 37%, state 5%, NIIT 3.8%

**Calculate:** Target harvest amount, prioritized trade list, and total tax savings.

**Solution:**
1. **Gain/loss budget:**
   - Total expected gains: $18,000 LT + $5,000 ST + $4,000 LT (planned) = $22,000 LT + $5,000 ST = $27,000
   - Loss carryforward: $0
   - Target harvest: $27,000 - $0 + $3,000 = **$30,000** to fully offset gains and capture the $3,000 ordinary income deduction
2. **Candidate ranking by tax benefit:**
   - Position B: $6,500 ST * (37% + 5% + 3.8%) = $6,500 * 45.8% = **$2,977** (highest rate — harvest first)
   - Position A: $14,000 LT * (20% + 5% + 3.8%) = $14,000 * 28.8% = **$4,032** (largest absolute benefit)
   - Position C: $2,100 LT * 28.8% = **$605**
3. **Harvest plan:** Harvest all three: $14,000 + $6,500 + $2,100 = $22,600 in total losses — $7,400 short of the $30,000 target, so every harvested dollar is consumed offsetting gains and the $3,000 ordinary-income offset is not reached
   - $5,000 ST losses offset $5,000 ST gains at 45.8% = $2,290 saved
   - $1,500 remaining ST losses cross over to offset LT gains at 28.8% = $432 saved
   - $16,100 LT losses ($14,000 A + $2,100 C) offset $16,100 of $22,000 LT gains at 28.8% = $4,637 saved
   - Remaining taxable LT gains: $22,000 - $16,100 - $1,500 = **$4,400** still taxable
   - **Total tax savings: $2,290 + $432 + $4,637 = $7,359**
4. **Coordinate with rebalancing:** Position A is also 2% overweight — its TLH sell doubles as a rebalance sell, saving one round-trip trade.

### Example 3: Wash-Sale Violation Across Accounts
**Given:**
- On November 5, client sells VTI (Vanguard Total Stock Market ETF) in taxable account for a $8,000 long-term loss
- On November 20 (15 days later), client's 401(k) makes its regular bi-weekly contribution, which includes an allocation to a Vanguard Total Stock Market Index Fund (institutional share class of the same fund)
- 401(k) contribution to the total stock market fund: $750

**Calculate:** Wash-sale impact and corrected cost basis.

**Solution:**
1. **Wash-sale triggered:** The 401(k) fund is substantially identical to VTI (same underlying index, same fund family). The purchase on November 20 falls within the 30-day post-sale window (November 5 + 30 = December 5).
2. **Disallowed loss:** The wash-sale disallowance is proportional to the replacement shares acquired. If 500 VTI shares were sold and the $750 401(k) purchase acquired the equivalent of approximately 3 shares at $250/share, then 3/500 = 0.6% of the loss is disallowed.
3. **Disallowed amount:** $8,000 * (3/500) = **$48 disallowed**
4. **Remaining allowable loss:** $8,000 - $48 = **$7,952** — still deductible
5. **Basis adjustment — 401(k) trap:** The $48 disallowed loss would normally be added to the replacement security's cost basis. However, because the replacement was purchased inside a 401(k), the cost basis adjustment provides NO future tax benefit (401(k) distributions are taxed as ordinary income regardless of basis). The $48 is permanently lost.
6. **Prevention:** Before executing TLH, review the client's 401(k) fund lineup and contribution schedule. If the 401(k) holds a substantially identical fund, either (a) temporarily redirect that 401(k) allocation to a non-identical fund during the wash-sale window, or (b) delay the TLH sale until after the next 401(k) contribution and ensure no contribution occurs for 30 days after.

## Common Pitfalls
- Harvesting losses without checking for substantially identical holdings in retirement accounts, triggering permanent loss disallowance in IRAs/401(k)s
- Forgetting to suspend DRIP on the sold security and related funds across all household accounts during the 61-day window
- Harvesting small losses (under $1,000) where transaction costs and operational complexity exceed the tax benefit
- Over-harvesting in early years, depressing cost basis so severely that future sales generate outsized gains (basis step-down compounding)
- Failing to coordinate with spouse's automated investments (401(k) payroll contributions, robo-advisor purchases)
- Selecting a replacement security that is substantially identical (same index, same fund family, different share class) — this does not avoid wash-sale rules
- Not tracking the holding period of replacement securities, leading to unintended short-term gains when the replacement is later sold
- Ignoring state tax differences when calculating harvest value — states with no income tax (FL, TX, NV) reduce the benefit by 5-13 percentage points versus high-tax states

## Cross-References
- **tax-efficiency** (wealth-management plugin): broader tax-aware investing context; TLH is one strategy within the overall tax-efficiency framework
- **rebalancing** (wealth-management plugin): TLH trades should be coordinated with rebalancing to minimize total transaction count
- **investment-suitability** (compliance plugin): replacement securities must still satisfy suitability requirements
- **investment-policy** (wealth-management plugin): IPS may specify TLH policy parameters (minimum loss threshold, approved replacement pairs)
- **performance-attribution** (wealth-management plugin): tax alpha from TLH should be tracked and attributed separately
- **client-review-prep** (advisory-practice plugin): TLH opportunities are flagged during periodic client review preparation
- **financial-planning-workflow** (advisory-practice plugin): TLH is a specific tax recommendation that may emerge from the financial plan
- **equity-compensation** (wealth-management plugin): recurring RSU vests and ESPP purchases can trigger wash sales against losses harvested in employer stock
