# 07-riesgo-sizing-portfolio — parte 1

Skills de terceros agrupadas por tema. Cada sección indica fuente, licencia y dónde está su código.



---

## SKILL: asset-allocation

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/asset-allocation` (MIT)
- Cuándo usarla: Determine how to distribute capital across asset classes using strategic and tactical allocation frameworks. Use when the user asks about portfolio allocation, mean-variance optimization, Black-Litterman, risk parity, glide paths, or target-date strategies. Also trigger when users mention 'how much in stocks vs bonds', '60/40 portfolio', 'policy portfolio', 'core-satellite', 'liability-driven investing', 'asset-liability matching', or ask how to split their money across investments.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/wealth-management/skills/asset-allocation/` (asset_allocation.py)

# Asset Allocation

## Core Concepts

### Strategic Asset Allocation (SAA)
The long-term policy portfolio based on an investor's risk tolerance, return objectives, time horizon, and constraints. SAA determines the baseline target weights (e.g., 60% equity / 30% bonds / 10% alternatives) and is the dominant driver of long-term portfolio returns. SAA should be revisited when investor circumstances change, not in response to market movements.

### Tactical Asset Allocation (TAA)
Short-to-medium-term deviations from the SAA based on market views, valuations, or momentum signals. TAA requires a disciplined process to avoid becoming ad hoc market timing. Key considerations:
- Define allowable deviation bands (e.g., +/- 10% from SAA)
- Have a clear signal framework (valuation, momentum, macro)
- Set reversion rules: when to return to SAA weights

### Mean-Variance Optimization (MVO)
Markowitz's framework for finding optimal portfolio weights that maximize risk-adjusted return:

max w'*mu - (lambda/2) * w'*Sigma*w

subject to: sum(w_i) = 1, w_i >= 0 (if long-only), and any additional constraints.

Where:
- w = weight vector
- mu = expected return vector
- Sigma = covariance matrix
- lambda = risk aversion parameter

MVO requires three inputs: expected returns, the covariance matrix, and risk aversion. The solution is highly sensitive to expected return inputs.

### Black-Litterman Model
Combines market equilibrium returns with investor views to produce more stable, intuitive portfolio weights. Two-step process:

**Step 1 — Implied Equilibrium Returns:**
Pi = lambda * Sigma * w_mkt

where w_mkt is the market-capitalization weight vector, lambda is the risk aversion parameter, and Sigma is the covariance matrix. These are the returns the market implicitly expects given current prices.

**Step 2 — Blending with Views:**
E(R) = [(tau*Sigma)^(-1) + P'*Omega^(-1)*P]^(-1) * [(tau*Sigma)^(-1)*Pi + P'*Omega^(-1)*Q]

where:
- tau = scalar (uncertainty of equilibrium, typically 0.025-0.05)
- P = pick matrix (identifies assets in each view)
- Q = view vector (expected returns from views)
- Omega = diagonal matrix of view uncertainties

The result is a posterior expected return vector that tilts away from equilibrium toward the investor's views, proportional to confidence.

### Risk Parity
Equalizes the risk contribution from each asset (or factor) rather than equalizing capital allocation:

RC_i = w_i * (Sigma*w)_i / sigma_p

Set RC_i = RC_j for all i, j.

In a simple two-asset case with no correlation:
w_i is proportional to 1/sigma_i

Risk parity portfolios allocate more capital to lower-volatility assets (typically bonds) and often require leverage to achieve competitive return targets.

### Glide Path
An age-based or time-based allocation that systematically shifts from growth assets to defensive assets as the investor ages or the target date approaches:

Common rule of thumb: Equity % = 110 - Age

Target-date fund glide paths typically:
- Start at 90% equity for young investors
- Decrease by ~1-2% per year
- Reach 30-40% equity at retirement
- Continue to "through" allocation post-retirement

### Core-Satellite
A hybrid approach combining:
- **Core (60-80%):** Low-cost, broadly diversified index funds or ETFs
- **Satellites (20-40%):** Active strategies, factor tilts, alternatives, or concentrated positions

This structure captures the market return efficiently (core) while allowing alpha generation or specific exposures (satellites).

### Asset-Liability Matching
For investors with defined liabilities (pensions, insurance, endowments with spending rules):
- Match asset duration and cash flows to liability duration and timing
- Surplus optimization: optimize the portfolio relative to liabilities, not absolute return
- Liability-driven investing (LDI): hedge liability risk with duration-matched bonds, invest surplus in return-seeking assets

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| MVO Objective | max w'*mu - (lambda/2)*w'*Sigma*w | Optimal portfolio weights |
| Equilibrium Returns | Pi = lambda * Sigma * w_mkt | Black-Litterman starting point |
| BL Posterior | E(R) = [(tau*Sigma)^(-1) + P'*Omega^(-1)*P]^(-1) * [(tau*Sigma)^(-1)*Pi + P'*Omega^(-1)*Q] | Blended expected returns |
| Risk Contribution | RC_i = w_i * (Sigma*w)_i / sigma_p | Risk parity target |
| Risk Parity Condition | RC_i = RC_j for all i, j | Equal risk contribution |
| Glide Path Rule | Equity % = 110 - Age | Age-based allocation |

## Worked Examples

### Example 1: Three-Asset Mean-Variance Optimization
**Given:**
- Assets: US Equity (mu=8%, sigma=16%), Int'l Equity (mu=7%, sigma=18%), US Bonds (mu=3%, sigma=4%)
- Correlations: US/Intl Equity = 0.75, US Equity/Bonds = 0.10, Intl Equity/Bonds = 0.05
- Risk aversion: lambda = 4
- Constraints: long-only, fully invested

**Calculate:** Optimal weights

**Solution:**

Covariance matrix:
- Cov(US,US) = 0.16^2 = 0.0256
- Cov(Intl,Intl) = 0.18^2 = 0.0324
- Cov(Bond,Bond) = 0.04^2 = 0.0016
- Cov(US,Intl) = 0.75 * 0.16 * 0.18 = 0.0216
- Cov(US,Bond) = 0.10 * 0.16 * 0.04 = 0.00064
- Cov(Intl,Bond) = 0.05 * 0.18 * 0.04 = 0.00036

MVO with lambda=4 (solving numerically or via quadratic programming):

Optimal weights (long-only):
- US Equity: 51.9%
- Int'l Equity: 0%
- US Bonds: 48.1%

Portfolio: expected return = 5.60%, volatility = 8.71%

Note: International equity is driven to zero — it is highly correlated with US equity (0.75) but has a lower expected return, so the optimizer sees no reason to hold it. This is classic MVO behavior: small input differences produce corner solutions. Adding a maximum-weight or minimum-allocation constraint would force diversification. The high bond allocation reflects the heavy variance penalty (lambda=4); reducing lambda shifts toward equities.

### Example 2: Black-Litterman with a Relative View
**Given:** The same three assets and covariance matrix as Example 1.
- Market-cap weights: US Equity 55%, Int'l Equity 30%, US Bonds 15%
- Risk aversion lambda = 2.5, tau = 0.05
- Investor view: Int'l Equity will outperform US Bonds by 3% (view uncertainty Omega = [0.001]; lower = higher confidence)

**Calculate:** Equilibrium and posterior expected returns

**Solution:**

Step 1 — Equilibrium returns, Pi = lambda × Sigma × w_mkt:
- US Equity: 5.16%
- Int'l Equity: 5.41%
- US Bonds: 0.18%

Step 2 — View specification: P = [0, 1, -1], Q = [3%].

The equilibrium already implies Int'l beats Bonds by 5.23%, so a 3% view is *bearish* relative to equilibrium. Applying the Black-Litterman posterior formula:
- US Equity: 4.28% (pulled down via its 0.75 correlation with Int'l)
- Int'l Equity: 4.07% (down from 5.41%)
- US Bonds: 0.23% (up slightly)

The posterior tilts returns toward the view in proportion to confidence. Fed into MVO, these returns shift weights away from equities and toward bonds relative to market-cap weights — moderately, avoiding the extreme corner solutions that raw MVO produces (compare Example 1). Note that views are always evaluated relative to what equilibrium already implies, not in isolation.

## Common Pitfalls
- MVO is highly sensitive to expected return inputs and has been called an "error maximizer" — small changes in returns produce large changes in weights
- Unconstrained MVO often produces extreme, concentrated positions — always add constraints (long-only, max weight, turnover limits)
- Black-Litterman requires the analyst to specify confidence in views (Omega), which is itself uncertain
- Risk parity portfolios require leverage to achieve equity-like returns, introducing borrowing costs and leverage risk
- Ignoring implementation costs: transaction costs, bid-ask spreads, and taxes can significantly erode theoretical optimal returns
- Ignoring liquidity constraints: some asset classes (private equity, real estate) cannot be rebalanced quickly
- Glide paths assume a generic investor — individual circumstances may require customization
- Over-reliance on historical covariance matrices that may not reflect future relationships

## Cross-References
- **historical-risk** (wealth-management plugin): volatility and correlation inputs for mean-variance optimization
- **forward-risk** (wealth-management plugin): expected return forecasts and scenario analysis for portfolio optimization
- **diversification** (wealth-management plugin): diversification principles underpin all allocation frameworks
- **bet-sizing** (wealth-management plugin): position sizing within the allocated asset classes
- **rebalancing** (wealth-management plugin): maintaining allocation targets over time
- **quantitative-valuation** (wealth-management plugin): valuation signals can inform TAA decisions
- **retirement-decumulation** (wealth-management plugin): decumulation-phase glide paths and the sequence-of-returns risk that allocation choices must manage
- **factor-investing** (wealth-management plugin): sizing factor tilts as deliberate, survivable deviations from the policy portfolio
## Running the Script

```bash
uv run scripts/asset_allocation.py            # run the demo (uses PEP 723 inline deps)
uv run scripts/asset_allocation.py --verify   # check demo outputs against the worked examples (exit 1 on mismatch)
python3 scripts/asset_allocation.py            # alternative (requires: pip install numpy scipy)
```

The demo prints the calculations covered above; its values match the worked examples in this skill. Run `--help` for a list of the classes and functions. For programmatic use, import the module rather than running it — the demo only executes under `python asset_allocation.py`.


---

## SKILL: client-reporting-delivery

- Fuente: `JoelLewis/finance_skills` → `plugins/advisory-practice/skills/client-reporting-delivery` (MIT)
- Cuándo usarla: Design, generate, and deliver client performance reports across all channels, covering quarterly reports, tax reporting, portal integration, and compliance review. Use when the user asks about building or redesigning report templates, choosing what to include in quarterly or annual client reports, transitioning from print to digital delivery, integrating a client portal, presenting net-of-fee performance with benchmarks, managing report production timelines, or handling e-delivery consent. Also trigger when users mention 'client reporting', 'quarterly performance report', 'report customization', 'tax lot report', '1099 supplement', 'report disclaimers', 'UHNW reporting', or 'report QA process'.

# Client Reporting and Delivery

## Core Concepts

### Client Reporting Architecture

The reporting pipeline in an advisory firm flows from data sources through a generation engine to client delivery. The primary data sources are the portfolio management system (PMS), custodian data feeds, financial planning tools, and the billing system. Each source contributes distinct data elements: the PMS provides portfolio holdings, performance calculations, and asset allocation; the custodian provides official transaction records, settled positions, and tax lot data; the financial planning tool provides goal progress and projection data; and the billing system provides fee calculations and payment history.

Report types span the full advisory relationship:

- **Quarterly performance reports** — The cornerstone deliverable. Summarizes portfolio performance, allocation, holdings, and transactions for the quarter with trailing period returns.
- **Annual reviews** — Comprehensive year-in-review combining performance, planning progress, and forward outlook. Often presented in person.
- **Financial plan updates** — Progress toward goals, updated projections, and recommended adjustments. May be quarterly or semi-annual.
- **Tax reports** — Realized gains and losses, unrealized gains and losses, cost basis reports, 1099 supplements, wash sale reports, and tax-loss harvesting summaries.
- **Billing summaries** — Detailed fee calculations showing AUM tiers, fee rates, amounts debited, and billing period.
- **Custom and ad-hoc reports** — Client-requested reports outside the standard cycle, such as a holdings detail for a mortgage application or a performance report for a specific date range.

Reporting platforms fall into several categories. PMS-embedded reporting tools (Orion Portfolio Solutions, Black Diamond, Tamarac Reporting) generate reports directly from the portfolio management database, ensuring data consistency. Standalone reporting platforms (e.g., Addepar) aggregate data from multiple sources and offer advanced customization, often favored by firms serving UHNW clients and family offices. (Backstop Solutions, sometimes miscategorized here, is an institutional research-management/CRM platform rather than a client reporting tool.) Client portal integration layers the reporting function into a broader digital client experience.

Custodian statements and advisor-produced reports serve complementary but distinct purposes. Custodian statements are the official record of account activity and positions, produced by the custodian (Schwab, Fidelity, Pershing). Advisor-produced reports add value through consolidated household views, custom benchmarks, goal-based framing, blended performance across custodians, and advisor commentary. Clients receive both, and firms should help clients understand the relationship between the two, particularly when minor data differences arise from timing or methodology.

### Report Content and Structure

A well-designed quarterly performance report follows a logical structure that guides the client from high-level summary to supporting detail:

1. **Cover page** — Firm branding, client or household name, reporting period, key headline metrics (total portfolio value, period return, net change in value). The cover page sets the tone and provides the most critical data points at a glance.

2. **Executive summary and market commentary** — A brief narrative (typically one page) covering market conditions during the period, key events that affected portfolios, and a forward-looking perspective. This section can be firm-level (same for all clients) or personalized by the advisor.

3. **Portfolio summary** — Asset allocation (current vs target, shown as pie chart or bar chart and table), total holdings count, cash position, and net deposits/withdrawals during the period. Household-level view aggregating all accounts.

4. **Performance summary** — Period returns (MTD, QTD, YTD, 1-year, 3-year, 5-year, 10-year, since inception) with benchmark comparison. Displayed as both table and chart. Net-of-fee returns as the primary presentation with gross-of-fee available.

5. **Account detail** — Individual account summaries within the household, each showing account type, custodian, value, allocation, and performance. Important for clients with multiple accounts across different registration types.

6. **Holdings detail** — Complete listing of positions by account or by asset class, showing security name, ticker, shares/units, market value, percentage of portfolio, unrealized gain/loss, and yield.

7. **Transaction summary** — Purchases, sales, income received, contributions, withdrawals, and fee debits during the period. Level of detail varies by client preference.

8. **Fee summary** — Advisory fees charged during the period, showing calculation methodology (AUM, billing rate, proration if applicable). Increasingly important given regulatory emphasis on fee transparency.

9. **Disclosures and disclaimers** — Required legal language including past performance disclaimers, benchmark descriptions, fee impact disclosure, and firm registration information.

Content customization by client segment is essential. Mass affluent clients typically prefer simplified reports emphasizing total value, return, and allocation with minimal holdings detail. High-net-worth (HNW) clients generally want comprehensive reports including full holdings, transaction detail, and benchmark comparisons. Ultra-high-net-worth (UHNW) and family office clients often require institutional-grade reporting with performance attribution, alternative investment detail, multi-entity consolidation, and custom analytics. The challenge is balancing comprehensiveness with readability — a 40-page report that goes unread serves no one.

### Performance Presentation in Reports

Performance is the most scrutinized section of any client report. Presenting returns accurately and clearly requires attention to methodology, time periods, benchmarks, and context.

**Return methodologies:** For TWR vs. MWR definitions and calculation, see the wealth-management performance-metrics and performance-reporting skills. In client reports: TWR is the standard for strategy evaluation; MWR answers "how did my money do?" and is increasingly presented alongside TWR. Presenting both can be powerful when accompanied by a brief explanation of the difference — when the two diverge significantly, it signals that cash flow timing had a material impact and opens a productive conversation.

**Return periods:**

Standard periods displayed in quarterly reports include MTD (month-to-date), QTD (quarter-to-date), YTD (year-to-date), trailing 1-year, trailing 3-year, trailing 5-year, trailing 10-year, and since-inception. Annualization conventions are critical: returns for periods exceeding one year should be annualized (geometric annualization), while returns for periods of one year or less should be presented as cumulative (non-annualized). Mixing conventions without clear labeling is a common source of confusion and potential compliance issues.

**Benchmark selection and display:**

Every portfolio should have a clearly defined benchmark. The primary benchmark should reflect the portfolio's strategic asset allocation and investment universe. For diversified portfolios, a blended benchmark (e.g., 60% MSCI ACWI / 40% Bloomberg US Aggregate) is more appropriate than a single index. Reports should include the benchmark description, component indices and weights, and a note that the benchmark is not investable and does not reflect fees. Some firms also display peer group comparisons or risk-adjusted metrics (Sharpe ratio, Sortino ratio) for sophisticated clients.

**Net-of-fee vs gross-of-fee returns:**

Net-of-fee returns are the preferred presentation for client reports because they represent the client's actual experience after paying advisory fees. Gross-of-fee returns may be shown alongside net for transparency or for GIPS-compliant presentations. The fee impact over long periods is substantial and should not be obscured.

**GIPS compliance considerations:**

Firms that claim compliance with the Global Investment Performance Standards must adhere to specific presentation requirements in composite reports, including required disclosures, composite construction rules, and prescribed return calculation methodologies. Individual client reports are not composites, but firms claiming GIPS compliance should ensure client-level reporting does not contradict or undermine their composite presentations.

**Performance disclaimers:**

Every report displaying performance data must include disclaimers stating that past performance is not indicative of future results, describing the benchmark and its limitations, disclosing whether returns are net or gross of fees, and noting any material factors affecting comparability across periods (e.g., strategy change, benchmark change).

### Report Customization and Personalization

Report customization operates at multiple levels, from firm-wide template design to individual client preferences.

**Level of detail:** Some clients want a two-page summary; others want 30 pages of detail. The reporting system should support configurable section inclusion, allowing advisors to toggle sections on or off per client. Common toggleable sections include holdings detail, transaction detail, individual account breakdowns, and performance attribution.

**Grouping and organization:** Reports can organize portfolio data in several ways depending on client preference and portfolio structure:

- **By account** — Each account presented separately, useful for clients focused on specific account objectives (IRA vs taxable).
- **By asset class** — All holdings grouped by asset class across accounts, useful for clients focused on overall allocation.
- **By goal or sleeve** — Holdings grouped by investment objective (retirement, education, legacy), useful for goal-based planning relationships.
- **By manager or strategy** — Holdings grouped by underlying manager or model portfolio, useful for multi-manager platforms.

**Household vs account-level reporting:** Most clients prefer a consolidated household view as the primary presentation, with account-level detail as a secondary section. The household view enables total portfolio allocation, consolidated performance, and a single net worth perspective. Account-level detail remains important for tax planning, beneficiary considerations, and account-specific objectives.

**Custom benchmarks:** Clients with unique portfolio constraints (ESG exclusions, concentrated stock positions, alternative allocations) may require custom benchmarks that reflect their investable universe. The reporting system should support advisor-defined blended benchmarks with custom weights and component indices, updated as the target allocation evolves.

**Personalized commentary:** The highest-value customization is advisor-written commentary specific to the client's situation. This might address recent portfolio changes, progress toward financial plan goals, upcoming planning actions, or responses to client questions. Some firms provide a firm-level market commentary as a default with an editable field for advisor personalization. Advisors who consistently add personalized commentary report stronger client engagement and retention.

**White-labeling:** Multi-advisor firms, RIA aggregators, and sub-advisory relationships often require white-labeled reports carrying the presenting firm's branding rather than the platform or TAMP provider's branding. The reporting system should support configurable logos, firm names, disclosures, and contact information.

**Language and terminology:** Reports should use language appropriate to the client's financial sophistication. A retired schoolteacher needs different terminology than a former CFO. Avoid unnecessary jargon where plain language suffices, but do not oversimplify for sophisticated clients who expect precision.

### Delivery Channels and Methods

Report delivery has evolved from exclusively print-and-mail to a multi-channel environment. Firms must manage several delivery methods simultaneously.

**Client portal (primary digital channel):**

The client portal is the hub of digital delivery. Reports are published to the portal where clients can view them online, download as PDF, and access historical reports in an archive. Portal-based delivery offers several advantages: immediate availability (no mail delay), persistent access (clients can revisit reports anytime), reduced cost (no printing or postage), environmental sustainability, and integration with other portal features (real-time portfolio view, document vault, secure messaging). The portal should provide notification (email or push) when new reports are available.

**Email delivery:**

Email delivery remains common, typically as an encrypted PDF attachment or a link to the client portal. Email is familiar and requires no portal login, making it accessible for less tech-savvy clients. However, email delivery raises security concerns (sensitive financial data in transit or in inboxes), so best practices include PDF encryption with a client-specific password, secure email platforms, or portal links rather than attachments. Firms should document email delivery preferences and security measures.

**Print and mail:**

Physical printed reports delivered via postal mail are declining but not extinct. Some clients, particularly older individuals or those in jurisdictions with specific requirements, prefer or require printed reports. Print delivery involves additional cost (printing, paper, postage), longer delivery time (days vs instant), and environmental impact. Firms transitioning to digital-first delivery should maintain a print capability for clients who opt in and for any regulatory requirements that mandate physical delivery.

**In-person review:**

Many advisors present reports during client meetings rather than simply delivering them. The meeting context allows the advisor to walk through results, provide context, answer questions in real time, and connect performance to financial plan progress. In-person presentation may use the same PDF report, a slide-deck derivative, or an interactive portal screen share. The report serves as both a leave-behind document and a meeting framework.

**Multi-channel strategy:**

The recommended approach is digital-first with print opt-in. Default delivery is portal publication with email notification. Clients who prefer print explicitly opt in and receive mailed copies in addition to (not instead of) digital access. This ensures every client has portal access to current and historical reports while accommodating print preferences.

**E-delivery consent:**

SEC rules on electronic delivery (primarily from SEC guidance releases and interpretive letters) require that firms provide notice that documents are available electronically, ensure the client has access to the electronic format, and obtain evidence of delivery (or evidence of notice with access). Firms should document client consent to electronic delivery, provide clear instructions for portal access, and maintain systems that confirm report availability and client access. Under FINRA rules, broker-dealers have additional requirements for implied consent and opt-out rights.

**Delivery confirmation and tracking:**

Firms should track report delivery status: portal published, email sent, email opened (if tracked), portal accessed, print mailed, print delivered (via tracking number if warranted). Delivery tracking supports compliance (evidence of delivery), operations (identifying delivery failures), and client service (confirming clients received their reports).

### Report Generation Workflow

The quarterly reporting cycle is a firm's most operationally intensive recurring process, typically spanning T+5 to T+15 after quarter-end (5 to 15 business days after the quarter closes).

**Workflow stages:**

1. **Data finalization (T+1 to T+5):** Custodian data feeds settle, reconciliation between PMS and custodian records completes, corporate actions process, and pricing finalizes. Reports cannot be generated until data is clean. The most common delay is waiting for custodian reconciliation to complete, particularly for accounts holding alternative investments, private placements, or international securities with delayed settlement.

2. **Report generation (T+5 to T+7):** Batch report generation runs for all client accounts and households. The PMS or reporting platform compiles data into report templates, calculates performance for all required periods, generates charts and tables, and produces PDF output. Batch runs may take several hours for large firms (thousands of accounts). Exception reports flag accounts with data issues that prevent clean report generation.

3. **Quality assurance (T+7 to T+9):** QA is the critical gate between generation and delivery. The QA process includes automated validation (returns within expected ranges, AUM totals match PMS, fee calculations correct, no missing data fields) and manual spot-checking (visual inspection of formatting, chart rendering, correct client names and account numbers, cross-referencing with custodian statements). QA should cover a statistical sample at minimum; many firms review all reports for households above a materiality threshold.

4. **Compliance review (T+9 to T+10):** Compliance reviews a sample of reports to verify disclaimers are present and current, performance presentation is accurate and not misleading, benchmark descriptions are complete, and fee disclosures are appropriate. Any reports used for marketing purposes (e.g., shared with prospects) trigger additional review under the SEC Marketing Rule.

5. **Advisor review and commentary (T+8 to T+11):** Advisors review reports for their client relationships, add personalized commentary where applicable, and flag any issues (data they know to be incorrect, clients with special circumstances requiring modified reports). This stage often runs in parallel with compliance review.

6. **Approval and release (T+11 to T+12):** Final approval, either by a designated operations manager, the Chief Compliance Officer, or through an automated workflow, clears reports for delivery. Once approved, reports are locked against further editing.

7. **Delivery (T+12 to T+15):** Reports are published to the client portal, email notifications are sent, and print reports are dispatched. Delivery may be staggered (largest clients first, or by advisor team) to manage volume and catch any last-minute issues before the full batch goes out.

**Handling exceptions:**

- Accounts with unresolved data issues receive delayed reports with a communication to the client explaining the delay.
- New accounts with short history (less than one full quarter) may receive a modified report or a welcome package in lieu of a performance report.
- Closed accounts require a final report covering the period from the last report through the closing date, including final performance and distribution details.

**Timeline management:**

The reporting cycle compresses many dependencies into a tight window. Bottleneck identification is essential: late custodian data, slow reconciliation, advisor commentary delays, and compliance review capacity are the most common constraints. Firms should establish clear deadlines for each stage with escalation procedures when deadlines slip.

### Client Portal Integration

The client portal has become central to the reporting strategy, serving as both a delivery channel and an interactive extension of the static report.

**Report access models:**

- **Batch-published reports:** Traditional PDF reports generated quarterly and published to the portal on a scheduled date. Clients access them like a digital filing cabinet.
- **On-demand reports:** Clients can generate reports for custom date ranges or specific accounts directly through the portal, without waiting for the quarterly cycle.
- **Interactive dashboards:** Real-time or near-real-time portfolio views that complement static reports. Dashboards show current allocation, performance, holdings, and transactions with drill-down capability.

The most effective portal strategy combines all three: periodic batch reports for the formal record, on-demand capability for ad-hoc needs, and interactive dashboards for day-to-day engagement.

**Portal features that complement reports:**

- **Real-time portfolio view** — Current holdings, values, and allocation without waiting for the next report cycle.
- **Transaction history** — Searchable history of all transactions across accounts.
- **Document vault** — Secure storage for financial plans, tax documents, estate documents, and other sensitive files shared between advisor and client.
- **Secure messaging** — Encrypted communication channel between client and advisor, replacing unsecured email for sensitive topics.
- **Goal tracking** — Visual progress toward financial plan goals (retirement funded percentage, education savings target, etc.) that contextualizes portfolio performance.
- **Fee transparency** — Itemized fee history and current fee schedule accessible through the portal.

**Driving portal adoption:**

Many firms struggle with portal adoption rates, which typically range from 40% to 70% of clients actively using the portal. Strategies to improve adoption include making the portal the default delivery channel, demonstrating the portal during client meetings, simplifying the registration process (single sign-on, mobile-friendly), providing portal training materials, and emphasizing features beyond report access (document vault, secure messaging, goal tracking). Younger clients and those with larger portfolios tend to have higher adoption rates.

**Portal vendors:**

Leading platforms include Orion Connect (integrated with Orion PMS, strong reporting and planning integration), Black Diamond Client Experience (known for visual report quality and client experience), Tamarac Reporting (integrated with Envestnet ecosystem), Addepar Client Portal (favored by UHNW and family office firms for advanced analytics), and custom-built portals (used by larger firms wanting full control over the client experience). Selection criteria include integration with the firm's PMS, report customization capability, mobile experience, security features, and total cost of ownership.

### Tax Reporting and Year-End Deliverables

Tax reporting is a distinct reporting function with its own timeline, data requirements, and audience (the client's CPA or tax preparer in addition to the client).

**Tax-related reports:**

- **Realized gain/loss report** — Lists all securities sold during the tax year with purchase date, sale date, proceeds, cost basis, and gain or loss. Categorized by short-term vs long-term. This is the primary report used for tax return preparation. Must reconcile to the custodian's 1099-B.
- **Unrealized gain/loss report** — Shows the embedded gains and losses in current holdings as of year-end. Critical for year-end tax planning: identifying positions to sell for tax-loss harvesting or gain realization before year-end.
- **1099 supplement** — A reconciliation document explaining any differences between the custodian-issued 1099 and the firm's records. Differences commonly arise from amortization methods, return of capital classification, or wash sale adjustments.
- **Cost basis report** — Detailed tax lot information for all current holdings, showing original purchase date, acquisition cost, adjustments (wash sales, corporate actions, return of capital), and current tax basis.
- **Wash sale report** — Identifies wash sale events where losses were disallowed due to repurchase of substantially identical securities within the 30-day window before or after the sale.
- **Tax-loss harvesting summary** — For firms that actively harvest tax losses, a summary of harvesting activity during the year: losses harvested, replacement securities purchased, estimated tax benefit.

**Year-end deliverables beyond tax reports:**

- **Annual performance summary** — Full-year performance across all standard periods, often presented in a more polished format than the Q4 report.
- **Annual fee summary** — Total fees paid during the calendar year, useful for tax deduction purposes where applicable and for client awareness of total cost.
- **Year-end portfolio appraisal** — Complete holdings listing with market values as of December 31, often used as a reference point for estate planning, insurance reviews, and net worth statements.

**Timing and coordination:**

Tax reporting follows a distinct timeline from performance reporting. Preliminary tax reports are typically available in January, based on the best available data. However, custodians issue corrected 1099s through February and sometimes into March (particularly for accounts holding partnerships, REITs, or international securities). Final tax reports should be issued only after the custodian's 1099 correction period closes. Firms should communicate the timeline clearly to clients and their CPAs to avoid filing with preliminary data that later changes.

Coordination with client CPAs is a value-added service. Proactive firms send tax reports directly to the client's CPA (with client authorization), provide a cover letter explaining the reports and any notable items, and make themselves available to answer CPA questions during tax season. This reduces friction for the client and positions the advisor as a hub of the client's financial team.

### Compliance Requirements for Client Reports

Client reports are communications to clients and therefore subject to regulatory scrutiny. Compliance requirements vary based on the firm's registration type (RIA, broker-dealer, dual registrant) and how the reports are used.

**Regulatory framework:**

- **SEC Marketing Rule (Rule 206(4)-1):** If client reports or performance extracts are shared with prospective clients, they become advertisements subject to the Marketing Rule. This includes requirements for performance presentation (net returns, one/five/ten year periods, prominent disclosure), prohibitions on misleading statements, and compliance review and approval before use.
- **FINRA Rule 2210 (Communications with the Public):** For broker-dealers, client reports are "correspondence" (communication with up to 25 retail investors in 30 days) or "retail communication" (more than 25). Retail communications require principal pre-approval; correspondence requires supervisory procedures. All communications must be fair, balanced, and not misleading.
- **SEC Custody Rule:** Reports may create "custody" implications if the firm has the ability to deduct fees directly. Fee disclosures in reports should be consistent with the firm's custody rule compliance.
- **Regulation S-P (Privacy):** Reports contain non-public personal information and must be delivered securely. Delivery methods (email, portal, mail) must comply with the firm's privacy policies and procedures.

**Required disclaimers:**

- Past performance is not indicative of future results.
- Description of each benchmark used, including that the benchmark is not investable and does not reflect fees or expenses.
- Whether returns are presented net or gross of advisory fees, and the impact of fees on returns.
- Firm registration information (RIA registration with the SEC or state, FINRA membership if applicable).
- Material facts necessary to avoid misleading the client (e.g., strategy changes, benchmark changes, calculation methodology changes).

**Supervisory review:**

Firms must establish supervisory procedures for client report review. The scope of supervisory review typically includes verifying performance accuracy (sampling), confirming disclaimers are present and current, reviewing advisor-written commentary for compliance (no guarantees, no promissory language, fair and balanced), and checking that reports are consistent with the client's actual account and investment strategy. Compliance should document the review process, the reviewer, the date, and any issues identified and resolved.

**Record retention:**

Under the SEC's books-and-records rules (Rule 204-2 for RIAs, Rule 17a-4 for broker-dealers), firms must retain copies of all communications delivered to clients, including client reports. Retention periods are typically five years (RIAs) or six years (broker-dealers) from the date of delivery. The retained copy must be the exact version delivered to the client. Digital archiving of PDFs published to portals satisfies this requirement when properly indexed and backed up.

**GIPS requirements:**

Firms claiming GIPS compliance must present composite-level performance in GIPS-compliant reports to prospective clients. Individual client reports are not composites, but the firm should ensure that client-level performance data does not contradict composite presentations and that GIPS-required disclosures appear on any report used to market the firm's investment capabilities.

### Report Quality Assurance

Quality assurance is the safeguard between report generation and client delivery. Errors in client reports damage credibility, create compliance risk, and generate costly re-issuance work.

**Automated validation checks:**

- **Return reasonableness:** Period returns for each account and the household fall within expected ranges (e.g., equity-heavy portfolios during a quarter when the S&P 500 returned 5% should show returns in a reasonable band around that figure). Flag outliers for manual review.
- **AUM reconciliation:** Total market value on the report matches the PMS balance and is within tolerance of the custodian statement balance. Differences exceeding a threshold (e.g., 0.1%) trigger investigation.
- **Fee calculation validation:** Advisory fees shown on the report match the billing system records. Fee rates match the client's fee schedule.
- **Completeness checks:** No missing data fields (blank returns, zero AUM for active accounts, missing benchmark data, absent disclaimers). All accounts in the household are included.
- **Period consistency:** The reporting period is correct (e.g., the Q4 report covers October 1 through December 31, not a different range).

**Visual and manual inspection:**

- **Formatting:** Charts render correctly, tables are properly aligned, page breaks fall at logical points, fonts and colors are consistent with the template.
- **Client-specific accuracy:** The correct client name, account numbers, and advisor name appear on the report. Reports are not crossed (Client A receiving Client B's data).
- **Data cross-check:** Spot-check report data against the PMS and custodian statement for a sample of accounts. Verify that holdings, transactions, and performance are consistent across sources.

**Common errors and root causes:**

- **Stale data:** Reports generated before custodian reconciliation is complete, reflecting outdated positions or missing transactions.
- **Incorrect benchmark:** A benchmark assignment error in the PMS causes the wrong benchmark to appear on the report, making performance comparison meaningless.
- **Wrong time period:** A configuration error causes reports to display incorrect period dates or returns for the wrong quarter.
- **Formatting glitches:** Template updates that break chart rendering, cause text overflow, or misalign columns.
- **Missing accounts:** An account recently added to the household is excluded from the consolidated report because the PMS grouping was not updated.
- **Cross-client errors:** The most severe error type — delivering a report containing another client's data. This is both a compliance violation and a privacy breach requiring notification.

**Error tracking and resolution:**

Firms should maintain an error log tracking each identified issue: date discovered, report affected, error type, root cause, resolution, and corrective action to prevent recurrence. Error rate metrics (errors per 1,000 reports generated) should be tracked over time and reported to management. A rising error rate signals a systemic issue (data quality, template instability, staffing) requiring intervention.

**Client-reported errors:**

When a client identifies an error, the resolution workflow includes acknowledgment (prompt response to the client), investigation (verify the error and identify the cause), correction (generate a corrected report), re-issuance (deliver the corrected report with a brief explanation), and root cause analysis (determine whether the error is isolated or systemic). The tone of client communication should be transparent and professional, treating the error seriously while reassuring the client that their actual account and investments are unaffected if the error is limited to the report.

## Worked Examples

See [references/examples.md](references/examples.md) for three end-to-end worked examples — redesigning a quarterly reporting package with tiered templates, transitioning from print to digital-first delivery, and remediating performance calculation errors in delivered reports. Load it when the user needs a full scenario walkthrough.

## Common Pitfalls

- **Generating reports before data is final.** Rushing to meet a delivery deadline with preliminary data — particularly for alternative investments, international securities, or accounts with pending corporate actions — leads to inaccurate reports and costly re-issuance. Establish a data readiness gate that must pass before report generation begins.

- **One-size-fits-all report design.** Delivering the same 25-page report to every client regardless of portfolio size, complexity, or sophistication wastes the client's time and the firm's resources. Tier-based customization ensures each client receives an appropriately scoped report.

- **Neglecting the performance disclaimer.** Omitting or using outdated performance disclaimers creates compliance risk. Disclaimers must be reviewed and updated at least annually by compliance, covering past performance language, benchmark descriptions, fee impact, and calculation methodology.

- **Ignoring delivery preferences.** Forcing all clients to digital delivery or continuing to print for clients who prefer digital wastes resources and frustrates clients. Maintain an accurate delivery preference database and honor stated preferences.

- **Presenting annualized returns for periods under one year.** Annualizing a three-month return inflates the apparent performance and is misleading. Only annualize returns for periods exceeding one year, and clearly label all return periods.

- **Failing to reconcile advisor reports to custodian statements.** When clients notice discrepancies between the advisor's report and the custodian statement, they lose confidence in the advisor's data. Proactively explain common differences (timing, methodology, household consolidation) and ensure the report includes a note about the relationship between the two.

- **Treating the report as a standalone document rather than a conversation tool.** Reports are most valuable when reviewed with the client, not simply mailed. Advisors who use reports as a framework for client meetings extract significantly more relationship value from the reporting investment.

- **Underinvesting in quality assurance.** Skipping or minimizing QA to speed delivery is a false economy. A single cross-client error (delivering Client A's data to Client B) creates a privacy breach, compliance violation, and severe reputational damage that far exceeds the cost of thorough QA.

- **Not tracking portal adoption metrics.** Launching a client portal without measuring adoption leads to low usage and wasted technology investment. Set specific adoption targets and actively manage the onboarding funnel.

- **Delaying tax report delivery without client communication.** Clients and their CPAs expect tax reports by a certain date. When corrected 1099s delay final tax reporting, proactive communication about the timeline prevents frustration and demonstrates professionalism.

## Cross-References

- **performance-reporting** (wealth-management plugin) — Client reports implement the performance reporting standards defined in this skill. Report templates and content must align with the firm's performance reporting policy.
- **performance-metrics** (wealth-management plugin) — Reports display the return and risk metrics calculated per this skill. Ensures consistency between the metrics definition and their presentation in reports.
- **performance-attribution** (wealth-management plugin) — Attribution analysis is included in detailed client reports for HNW and UHNW tiers. The attribution skill defines the methodology; this skill addresses how to present attribution results clearly.
- **gips-compliance** (compliance plugin) — GIPS presentation standards apply to composite-level performance reporting and influence client-level report design for firms claiming compliance.
- **advertising-compliance** (compliance plugin) — Reports shared with prospects become marketing materials subject to the SEC Marketing Rule and advertising compliance requirements.
- **books-and-records** (compliance plugin) — Delivered reports must be retained per SEC and FINRA recordkeeping rules. The delivery channel and archiving process must support compliant record retention.
- **client-disclosures** (compliance plugin) — Required disclaimers and disclosures that appear in client reports are defined and maintained per this compliance skill.
- **portfolio-management-systems** (advisory-practice plugin) — The PMS is the primary data source for report generation. Data quality, reconciliation status, and system configuration directly affect report accuracy.
- **advisor-dashboards** (advisory-practice plugin) — Dashboards provide real-time portfolio views that complement the periodic snapshots in client reports. Together they form a complete client information ecosystem.
- **fee-billing** (advisory-practice plugin) — Fee summaries included in client reports draw data from the billing system. Fee calculation accuracy in reports depends on billing system integration.
- **financial-planning-integration** (advisory-practice plugin) — Financial plan progress reporting is included in comprehensive client reports, connecting portfolio performance to goal achievement.
- **client-review-prep** (advisory-practice plugin) — Review preparation feeds into and complements the report delivery workflow; reports are a key component of the review meeting package.

### Referencia: references/examples.md

# Worked Examples — Client Reporting and Delivery

## Table of Contents

1. [Redesigning a Quarterly Reporting Package](#example-1-redesigning-a-quarterly-reporting-package) — modular tier-based templates, production timeline, portal-first delivery for a 20-advisor RIA
2. [Transitioning from Print to Digital-First Delivery](#example-2-transitioning-from-print-to-digital-first-delivery) — phased rollout, e-delivery consent, adoption metrics for an older client base
3. [Remediating Performance Calculation Errors in Quarterly Reports](#example-3-remediating-performance-calculation-errors-in-quarterly-reports) — root cause analysis, data readiness gates, re-issuance process

### Example 1: Redesigning a Quarterly Reporting Package

**Scenario:**

A 20-advisor RIA firm managing $3.5 billion across 2,400 households is redesigning its quarterly reporting package. The current reports are generic, text-heavy PDF exports from the PMS with no customization by client segment. Advisors report that clients find the reports confusing, and the operations team spends two weeks each quarter manually adjusting reports for key clients. The firm uses Orion as its PMS and has a client portal but only 35% portal adoption. The firm wants a modern, tiered reporting approach with efficient production.

**Design Considerations:**

The report template structure should follow a modular design where sections can be toggled by client tier:

- **Cover page:** Firm-branded, household name, reporting period, headline metrics (portfolio value, quarterly return, year-to-date return, net contributions/withdrawals). Clean visual design with the firm's color palette.
- **Executive summary (1 page):** Firm-level market commentary (written by the CIO or investment committee) with an editable field for advisor personalization. Advisors for top-tier clients write 2-3 sentences specific to the client's situation.
- **Portfolio summary (1-2 pages):** Asset allocation chart (current vs target), allocation table, total portfolio value, cash position. Household-level view as the primary presentation.
- **Performance summary (1-2 pages):** TWR and MWR for the portfolio and each account. Periods: QTD, YTD, 1-year, 3-year, 5-year, since inception. Benchmark comparison with blended benchmark matching the portfolio's target allocation. Chart showing cumulative growth of portfolio vs benchmark since inception.
- **Holdings detail (2-5 pages, toggleable):** Complete position listing by asset class. Security name, ticker, shares, market value, percentage of portfolio, unrealized gain/loss. Included by default for HNW and UHNW tiers; excluded by default for mass affluent (available on request).
- **Transaction summary (1-2 pages, toggleable):** Purchases, sales, dividends, contributions, withdrawals, fees. Included for HNW and above by default.
- **Fee summary (1 page):** Quarterly fee calculation detail: beginning AUM, fee rate, fee amount, payment method. Always included for transparency.
- **Disclosures (1-2 pages):** Standard disclaimers, benchmark descriptions, firm information. Updated quarterly by compliance.

Client tier customization:

- **Mass affluent (under $1M):** Cover page, executive summary, portfolio summary, performance summary, fee summary, disclosures. Total approximately 6-8 pages. Simplified language, fewer metrics.
- **HNW ($1M-$10M):** All sections included. Approximately 12-18 pages. Full detail with benchmark comparison and advisor commentary.
- **UHNW ($10M+) and family office:** All sections plus performance attribution summary, alternative investment detail, multi-entity consolidation, and custom analytics. Approximately 20-30 pages. Advisor writes substantive personalized commentary for each household.

For digital delivery via the client portal: all reports are published to the Orion Connect portal with automated email notification. The email contains a branded message with the client's name and a direct link to the portal (no PDF attachment for security). To boost portal adoption from 35% toward 70%, the firm launches a portal onboarding campaign concurrent with the new report rollout, with advisors demonstrating the portal during quarterly review meetings.

The 10-business-day production workflow from quarter-end:

- T+1 to T+4: Data finalization, custodian reconciliation, corporate action processing.
- T+5 to T+6: Batch report generation for all households, exception report produced.
- T+6 to T+7: Automated QA validation, manual spot-check of a 10% sample plus all UHNW households.
- T+7 to T+8: Compliance review of a 5% sample plus all reports containing advisor-written commentary.
- T+7 to T+9: Advisor review and personalized commentary entry (runs in parallel with compliance review).
- T+9: Final approval by operations manager and compliance officer.
- T+10: Batch publication to portal, email notifications sent, print copies mailed for opt-in clients.

**Analysis:**

The modular template design eliminates manual per-client adjustments by encoding customization rules into the report generation configuration. Tier-based defaults reduce the operations team's workload from two weeks of manual adjustments to exception handling only. The 10-business-day cycle is achievable with disciplined data finalization and parallel compliance/advisor review stages. The portal-first delivery strategy, paired with an adoption campaign, should reduce print volume by 50% or more within two quarters. Key risk: advisor commentary delays can push the timeline past T+10, so the firm should establish a hard T+9 deadline for commentary with an auto-populated default if the advisor does not provide custom text.

### Example 2: Transitioning from Print to Digital-First Delivery

**Scenario:**

A 45-year-old advisory firm with 1,800 clients is transitioning from mailing printed quarterly reports to digital-first delivery. Currently, 100% of clients receive printed reports via USPS mail at a cost of $4.50 per report (printing, assembly, postage), totaling approximately $32,400 per year for quarterly reports alone. The firm has a client portal (Black Diamond Client Experience) but has never used it for report delivery. The client base skews older — 40% of clients are over 65 — and the firm is concerned about resistance to change.

**Design Considerations:**

The transition plan should balance efficiency gains with client experience, executed in phases:

**Phase 1 — Communication and consent (Month 1-2):**

- Send a personalized letter to all clients announcing the transition to digital delivery, emphasizing benefits (faster access, 24/7 availability, historical archive, environmental sustainability).
- Include a response form for delivery preference: digital-only (portal and email notification), digital with print supplement (portal access plus mailed copy), or print-only (opt-in exception, requires written request).
- Advisors call their top 50 clients personally to explain the transition and address concerns.
- E-delivery consent documentation collected and filed per SEC electronic delivery guidance.

**Phase 2 — Portal onboarding (Month 2-3):**

- Dedicated onboarding support: a team member or recorded webinar walks clients through portal registration, login, and report access.
- Simplified registration process: pre-populated registration links sent via email requiring only password creation.
- Mobile-friendly portal experience, since many older clients are comfortable with tablets even if not desktop computers.
- Printed quick-start guide mailed to all clients with step-by-step portal access instructions and support phone number.
- Advisors demonstrate the portal during every client meeting during the transition quarter.

**Phase 3 — Parallel delivery (Quarter 1 of new approach):**

- For the first quarterly cycle, deliver reports through both channels: publish to portal with email notification and mail printed copies. This gives clients a safety net and builds confidence in the digital experience.
- Track portal access: which clients logged in, viewed their report, and downloaded PDFs.
- Follow up with clients who did not access the portal, offering additional onboarding support.

**Phase 4 — Digital-first (Quarter 2 onward):**

- Default delivery switches to digital-only (portal publication with email notification).
- Clients who opted for print supplement or print-only continue receiving mailed copies.
- Quarterly review of print opt-in list: advisors gently encourage digital adoption during meetings.

**Exception handling for print-required clients:**

- Clients over age 80 or with documented technology barriers are automatically enrolled in the print supplement program.
- No client is denied printed reports if they request them.
- Print reports are identical to digital (same PDF), printed in color, and mailed in a firm-branded envelope.
- The firm budgets for 20-30% of clients remaining on print in Year 1, declining to 10-15% by Year 3.

**Compliance review of electronic delivery:**

- E-delivery consent forms reviewed by compliance counsel to ensure they meet SEC guidance requirements (informed consent, evidence of access, opt-out ability).
- Portal security reviewed: encryption in transit and at rest, authentication requirements (multi-factor authentication recommended), session timeout, and access logging.
- Record retention: portal automatically archives all published reports with delivery timestamp, satisfying books-and-records requirements. Emailed notification records are also retained.
- Privacy review: portal access controls ensure each client sees only their own data.

**Adoption metrics tracking:**

- Portal registration rate (target: 85% within 6 months).
- Active portal usage rate (logged in at least once per quarter; target: 65% within 12 months).
- Report access rate (percentage of clients who viewed their report within 14 days of publication).
- Print opt-in rate (track trend quarterly, targeting decline).
- Client satisfaction: survey question on report delivery satisfaction added to annual client survey.
- Cost savings: track printing, postage, and assembly cost reduction quarterly.

**Analysis:**

The phased approach minimizes client disruption while systematically driving digital adoption. The parallel delivery quarter is costly (double delivery) but critical for building client confidence. The 40% over-65 demographic is a legitimate concern, but portal adoption among older adults has increased significantly and the firm's approach of personal outreach, simplified onboarding, tablet-friendly design, and continued print availability mitigates the risk. Expected cost savings are substantial: if 70% of clients move to digital-only, annual printing and mailing costs drop from $32,400 to under $10,000, with additional savings in staff time for assembly and mailing. The compliance framework for e-delivery must be established before the first digital delivery, not after.

### Example 3: Remediating Performance Calculation Errors in Quarterly Reports

**Scenario:**

During a routine internal audit, a mid-size RIA discovers that approximately 5% of quarterly reports (60 out of 1,200 households) delivered in the most recent quarter contained performance calculation errors. The errors originated from late custodian data corrections for accounts holding a specific alternative investment fund that revised its NAV two weeks after the initial quarter-end pricing. The firm's reporting workflow generated reports using the preliminary NAV, and the corrected NAV arrived after reports were already delivered. The differences in reported returns ranged from 5 to 35 basis points, affecting since-inception and trailing-period returns for the affected accounts.

**Design Considerations:**

**Root cause analysis:**

The root cause is a timing mismatch between the report generation schedule and the data finalization timeline for alternative investments. The firm's standard T+7 report generation date assumed all custodian data was final, but the alternative investment fund in question consistently provides corrected NAVs at T+14 to T+18. The PMS ingested the corrected data after reports were generated and delivered, but no process existed to flag that delivered reports contained stale pricing for specific holdings.

Contributing factors: (a) no data readiness checklist identifying securities with known delayed pricing, (b) no automated comparison between report-date pricing and current PMS pricing after corrections, (c) the alternative investment was added to client portfolios 18 months ago without updating the reporting workflow to accommodate its pricing timeline.

**Data validation checks to implement:**

- **Pre-generation data readiness gate:** Before batch report generation, run an automated check confirming that all holdings have final pricing. Maintain a watchlist of securities with known delayed pricing (alternatives, private placements, international funds with delayed NAVs). If any watchlist security has preliminary pricing, delay report generation for affected accounts or flag them for manual review.
- **Post-generation pricing comparison:** After the custodian data correction window closes (T+20), automatically compare the pricing used in delivered reports against current PMS pricing. Flag any account where the pricing difference exceeds a materiality threshold (e.g., 10 basis points of return impact).
- **Alternative investment pricing tracker:** Maintain a log of all alternative investments with their expected pricing finalization dates. Cross-reference against the reporting calendar to identify conflicts.

**QA workflow enhancements:**

- Add a specific QA step for accounts holding alternative investments, private placements, or other securities with delayed pricing.
- Implement a two-tier generation process: generate reports for accounts with all-final pricing on the standard timeline (T+7); hold accounts with pending pricing data for a second generation run (T+18 to T+20) after corrections are received.
- Establish a materiality threshold for pricing changes: differences below 5 basis points may not warrant re-issuance; differences above 5 basis points trigger the re-issuance process.

**Re-issuance process for affected clients:**

1. Generate corrected reports for all 60 affected households using final pricing data.
2. QA review all corrected reports (100% review, not sampling, given the sensitivity).
3. Compliance review of corrected reports and the client communication.
4. Prepare a client communication letter (reviewed by compliance counsel) explaining: (a) a pricing correction for a specific investment affected the performance data in the previously delivered report, (b) the corrected report is enclosed/attached/available on the portal, (c) the actual portfolio holdings and transactions were not affected — only the reported performance calculation, (d) the specific line items that changed and the magnitude of the difference, and (e) an apology for the error and a description of the steps the firm is taking to prevent recurrence.
5. Deliver corrected reports and communication letter through each client's preferred channel. Advisors for top-tier clients call the client before or concurrently with the letter to provide a personal explanation.
6. File the corrected reports and communication in the firm's books and records, noting the original report, the correction, and the reason.

**Ongoing monitoring to prevent recurrence:**

- Quarterly review of the security watchlist for delayed-pricing holdings, updated as new investments are added to client portfolios.
- Monthly reporting operations meeting that includes a review of the data readiness gate results and any exceptions.
- Annual review of the reporting timeline relative to custodian data correction windows, adjusting the production calendar as needed.
- Error rate tracking: monitor the corrected-report rate quarterly with a target of zero re-issuances due to data timing issues.
- If the firm adds additional alternative investments, the onboarding process must include updating the reporting watchlist and confirming the pricing timeline is compatible with the report production schedule.

**Analysis:**

The 5% error rate, while seemingly modest, represents a meaningful compliance and reputational risk. Performance reporting accuracy is a fundamental fiduciary obligation, and delivering incorrect returns — even by a few basis points — erodes client trust. The remediation approach addresses both the immediate issue (corrected reports with transparent client communication) and the systemic cause (inadequate data readiness checking for delayed-pricing securities). The two-tier generation process adds operational complexity but is necessary for firms holding alternatives with delayed pricing. The materiality threshold (5 basis points) provides a practical standard for triggering re-issuance while avoiding excessive corrections for immaterial differences. The firm should also evaluate whether its compliance manual and supervisory procedures need updating to reflect the new QA steps and data readiness requirements.


---

## SKILL: control-design

- Fuente: `SYasJ/claude-business-skills` → `plugins/risk/skills/control-design` (MIT)
- Cuándo usarla: Design a control that prevents or detects a named failure, and specify the evidence it leaves. Use when the user mentions design a control, control activity, preventive control, detective control, or asks for a control design. Risk and compliance skill by Yasir Jilani.

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'control-design' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Control Design

Design a control that prevents or detects a named failure, and specify the evidence it leaves.

## When to use this skill

Use this skill when the user:

- design a control
- control activity
- preventive control
- detective control

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

- The failure to prevent
- How the work happens today
- Who can perform the control
- Evidence available

## Workflow


### 1. Step 1

State the failure in one sentence.
### 2. Step 2

Choose preventive or detective based on when the harm becomes irreversible.
### 3. Step 3

Assign a performer who is not the only person benefiting from a bypass, when they can staff that.
### 4. Specify the evidence

a review note, a system log, or a sign-off.
### 5. Step 5

Define the frequency.
### 6. Step 6

A control with no evidence is a hope. Say so.

## Output

Deliver a **control design**.

- Purpose of this control design, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a control design by 30 September 2026. The control is 'management reviews revenue' with no sample and no sign-off.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

The control is 'management reviews revenue' with no sample and no sign-off.

The failure to prevent: Control 7.2 access review, first seen 14 September 2026. No root cause recorded yet
How the work happens today: Control 7.2 access review; Vendor Redline Parts. Both unassigned as of 14 September 2026
Who can perform the control: Priya Shah, controller
Evidence available: one PDF, 2 pages, dated 14 September 2026
```

### Example outcome

**Control design**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Names the sample, the reviewer, and the evidence left behind.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The failure to prevent | Control 7.2 access review, first seen 14 September 2026. No root cause recorded yet | Needs confirmation |
| How the work happens today | Control 7.2 access review; Vendor Redline Parts. Both unassigned as of 14 September 2026 | Carried into the draft |
| Who can perform the control | Priya Shah, controller | Carried into the draft |
| Evidence available | one PDF, 2 pages, dated 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. State the failure in one sentence**

**2. Choose preventive or detective based on when the harm becomes irreversible**

**3. Assign a performer who is not the only person benefiting from a bypass, when they can staff that**

**4. Specify the evidence**  
a review note, a system log, or a sign-off.

**5. Define the frequency**

**Deliberately not done**
- A control with no evidence.
- The beneficiary is the only reviewer.
- A policy sentence with no activity.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A control with no evidence
- The beneficiary is the only reviewer
- A policy sentence with no activity

## Related skills

- `internal-controls-walkthrough`
- `sox-walkthrough`


---

## SKILL: counterparty-risk

- Fuente: `JoelLewis/finance_skills` → `plugins/trading-operations/skills/counterparty-risk` (MIT)
- Cuándo usarla: Guide counterparty credit risk measurement and management for OTC and securities trading, organized around three workflows: assessing a new counterparty, responding to a credit-deterioration event, and executing a default close-out. Use when measuring current or potential future exposure to a counterparty, setting or reviewing counterparty credit limits, evaluating ISDA Master Agreement netting and close-out mechanics, designing CSA collateral terms or uncleared margin compliance (VM/IM, SIMM), assessing central clearing mandates under Dodd-Frank or EMIR and CCP default waterfalls, monitoring creditworthiness via CDS spreads or ratings, quantifying wrong-way risk, or computing EAD, SA-CCR, and CVA. For Reg T and FINRA Rule 4210 brokerage margin see margin-operations; for settlement risk, DVP, and CLS see settlement-clearing.

# Counterparty Risk

## Core Concepts

### Workflow A: Assessing a New Counterparty

1. **Identify the legal entity and verify netting enforceability.** Map the exact legal entity (not the corporate group), its jurisdiction, and entity type. Confirm close-out netting enforceability via ISDA netting opinions for that jurisdiction and entity-type combination before counting any netting benefit — where enforceability is uncertain, risk and capital must be measured gross. Apply the sovereign ceiling for counterparties in jurisdictions with material sovereign risk.
2. **Assess credit quality from three angles.** External ratings are a baseline but a lagging indicator — they typically reprice after the market has. Internal scoring: for banks, focus on CET1 (strong banks hold >12%), leverage ratio (well-capitalized banks target 5%+), LCR/NSFR (minimum 100%), and NPL trend; for corporates, debt/EBITDA, interest coverage (below 2x signals stress), free cash flow, and Altman Z-score, plus qualitative factors (management, franchise, regulatory standing). Market-implied: CDS spreads react fastest — annual PD ≈ CDS_spread / (1 − recovery); a 200bp spread at 40% recovery implies roughly 3.3% annual default probability.
3. **Determine the trading channel: cleared vs. bilateral.** Standardized interest rate swaps in major currencies and index CDS must clear under Dodd-Frank Title VII / EMIR (end-user hedging exemptions exist). Non-mandated products stay bilateral under the uncleared margin rules: zero VM threshold, IM threshold up to $50 million per counterparty group, and IM held segregated at a third-party custodian with no rehypothecation. Client clearing adds clearing-member risk: evaluate portability provisions and maintain a backup clearing member.
4. **Negotiate documentation.** ISDA Master Agreement (the 2002 version uses the Close-out Amount methodology; many legacy relationships remain on the 1992 version's Market Quotation/Loss — know which governs each relationship), Schedule elections (governing law, Specified Entities, cross-default thresholds, additional termination events such as NAV triggers), and CSA terms: threshold, minimum transfer amount, independent amount/IM, eligible collateral and haircuts, valuation frequency (daily is standard), and dispute resolution. Link the CSA threshold to ratings so it steps down — ideally to zero — on downgrade.
5. **Set the credit limit.** Tier by credit quality, with sub-limits by product and tenor (long-dated exposure is more uncertain) and a settlement limit separate from the pre-settlement limit. Apply explicit add-ons or reduced limits for wrong-way risk, where exposure and counterparty credit quality are positively correlated (general WWR: PD correlated with market factors; specific WWR: structural, e.g., a put written on the counterparty's own stock).
6. **Stand up measurement and monitoring.** Compute current exposure CE = max(V, 0); PFE at 95-97.5% confidence via Monte Carlo (simulate risk-factor paths, revalue the netting set at each time step, take the percentile of max(value, 0)); EE/EPE as the capital basis; EAD = 1.4 × (RC + PFE add-on) under SA-CCR; CVA = LGD × Σ EE_i × PD_i × DF_i. Aggregate across all desks, products, and legal entities facing the counterparty — a trade missing from the counterparty risk system is unmeasured exposure. Wire pre-deal limit checks into order flow, monitor post-trade for market-driven breaches, alert at ~80% utilization, and hard-block at 100%. Review cadence: annual full review for top-tier names, semi-annual for lower tiers, monthly (or more) for the watch list.

### Workflow B: Responding to a Credit-Deterioration Event

Early-warning thresholds that should put a counterparty on the watch list before any downgrade: sustained CDS widening (e.g., 50bp over 30 days, or absolute spread above 300bp), stock price decline >30% over 60 days, negative rating outlook, covenant breaches, regulatory enforcement actions, accounting restatements, or significant client withdrawals.

1. **Confirm and classify the trigger.** Initiate a formal credit review: temporary setback (a bad quarter, a one-time loss) or structural deterioration (capital erosion, rising NPLs, franchise decline)? Review the latest financials, disclosures, and analyst coverage.
2. **Enforce CSA downgrade provisions.** Check for ratings-linked threshold step-downs and additional termination events; call any collateral the CSA now permits (a threshold stepping to zero converts the prior threshold amount into an immediate collateral call).
3. **Reduce the credit limit.** Convene the credit committee and re-tier the counterparty. If current exposure now exceeds the reduced limit, document the breach and a dated remediation plan.
4. **Reduce exposure.** In rough order of cost: let maturing trades roll off without replacement; execute offsetting trades; novate trades to other counterparties (requires consent); unwind by agreement with a close-out payment. Prioritize long-dated, high-PFE trades for novation or unwind; short-dated trades maturing within weeks rarely justify early-termination costs.
5. **Restrict new trading.** Hold on exposure-increasing trades; require credit-officer approval for any new trade, which must be flat or exposure-reducing.
6. **Escalate monitoring to daily** — exposure, CDS, collateral disputes, news — and explicitly stress wrong-way risk by jointly shocking the exposure drivers and the counterparty's default (e.g., a European bank counterparty and euro depreciation that inflates FX-forward exposure simultaneously).
7. **Pre-position for default.** Pre-calculate close-out amounts and collateral adequacy, identify replacement counterparties for critical hedges, and confirm which agreement version and close-out methodology governs.
8. **Document everything** — committee decisions, limit rationale, the reduction plan, and communications — as evidence of prudent risk management for internal audit and examiners.

### Workflow C: Default Close-Out Playbook

Maintain this playbook pre-built for every watch-list counterparty: pre-drafted Event of Default and termination notices, pre-identified valuation sources (dealer panels, pricing services, internal marks), pre-computed exposure and collateral figures, and a contact tree (legal, credit, trading, operations). Close-out must execute in days, not weeks — every day of delay is unhedged market risk on the terminated portfolio.

1. **Confirm the Event of Default** under the governing Master Agreement (failure to pay, credit support default, cross-default above the threshold, bankruptcy, merger without assumption). Distinguish from Termination Events (illegality, force majeure, tax events, ATEs), which may permit termination of only the affected transactions.
2. **Deliver the default notice** using the pre-drafted form, observing the agreement's notice mechanics and grace periods.
3. **Designate the Early Termination Date** (same day or a future date, as the agreement permits).
4. **Value the terminated transactions** using commercially reasonable procedures — 2002 ISDA Close-out Amount (flexible but more subjective) or 1992 Market Quotation/Loss — drawing on the pre-identified valuation sources. Document quotes and marks contemporaneously; valuation disputes are the most litigated part of close-outs.
5. **Net to a single Early Termination Amount.** The single-agreement provision defeats cherry-picking by the bankruptcy estate: all transactions terminate together and net to one claim, including unpaid amounts. This is where the netting-enforceability verification from Workflow A pays off.
6. **Apply collateral** held under the CSA against the net amount. Expect exposure drift over the margin period of risk (regulatory MPOR ~10 business days bilateral, ~5 days cleared) between the last margin collection and final close-out — this is the exposure IM was sized to cover.
7. **Re-hedge the terminated portfolio** immediately. The close-out crystallizes the claim, but the market risk of the vanished trades is live until replaced.
8. **For cleared trades, the CCP runs default management instead.** The default waterfall applies resources in order: (1) the defaulter's initial margin, (2) the defaulter's default fund contribution, (3) the CCP's own capital (skin-in-the-game), (4) non-defaulting members' default fund contributions, (5) capped supplemental assessments, (6) recovery tools (variation margin gains haircutting, partial tear-up). CCPs size resources to the Cover 1 / Cover 2 standard — the default of the largest one or two members under extreme but plausible conditions. Clients of a defaulted clearing member should trigger porting of positions and margin to a backup member within one to two days.

### Core Reference

**Exposure measures (one line each).** Current exposure: CE = max(V, 0), where V is the net mark-to-market of the netting set. PFE: the high-percentile (95-97.5%) simulated exposure profile over time — rising with horizon, then rolling off as trades mature. EE/EPE: average exposure at a date / time-averaged EE, the basis for regulatory capital under SA-CCR and IMM. EAD (SA-CCR): 1.4 × (RC + PFE add-on). CVA: the market value of counterparty credit risk — LGD × Σ(EE_i × PD_i × DF_i), where LGD = 1 − recovery rate, EE_i is expected exposure at time i, PD_i the default probability in period i, and DF_i the discount factor — a separate Basel III capital charge that raises the cost of bilateral OTC trades. Market-implied PD can be backed out of CDS spreads as spread / (1 − recovery rate). Limit utilization is monitored as current exposure / credit limit. Wrong-way risk: standard PFE models assume exposure-default independence — add joint stress scenarios where they correlate.

**Netting.** Payment netting reduces settlement flows; close-out netting is the credit-risk tool. Netting benefit = gross exposure − net exposure; netting ratio = net/gross (a ratio of 0.3 means netting cut exposure 70%). CCP multilateral netting nets across all clearing members and can exceed any bilateral result.

**Collateral.** VM covers current exposure (daily exchange, typically title transfer and reusable); IM covers close-out-period exposure (posted at inception, segregated, no rehypothecation under the uncleared margin rules). Collateralized exposure = max(V − haircut-adjusted collateral, 0); with a CSA threshold, residual uncollateralized exposure = max(V − threshold, 0) − collateral held. ISDA SIMM (sensitivity-based, recalibrated annually) generally produces lower IM than the regulatory schedule because it recognizes hedging and diversification. Typical haircuts: cash 0%; Treasuries 0.5-4% by maturity; investment-grade corporates 5-10%; equities 15-25%; plus ~8% FX haircut for non-domestic-currency collateral. Valuation disputes are routine — transfer the undisputed amount while escalating per the CSA.

**CCP margin methodology.** CCPs compute IM with historical-simulation VaR or Expected Shortfall at 99%+ confidence over the MPOR (typically 5 days for cleared swaps, 2 days for listed futures), plus concentration, liquidity, and wrong-way add-ons; VM is exchanged daily or intraday. Clearing concentrates risk in the CCP itself — CCPs are designated SIFMUs with heightened supervision, and members should assess each CCP's default waterfall adequacy.

**Settlement risk.** Settlement risk mechanics — DVP, PvP/CLS, Herstatt risk — are owned by the settlement-clearing skill (trading-operations); the counterparty-risk implication is that settlement limits must be set separately from pre-settlement limits because the exposure is full notional, not mark-to-market.

## Worked Examples

Two worked examples are in [references/examples.md](references/examples.md) — load for an end-to-end scenario: (1) setting up a counterparty credit limit framework with tiering, sub-limits, and governance, (2) designing collateral management for bilateral OTC trades under the uncleared margin rules.

## Common Pitfalls
- Relying solely on credit ratings as the primary indicator of counterparty creditworthiness — ratings are lagging indicators that often reflect deterioration only after the market has repriced the risk; CDS spreads and equity-implied metrics provide more timely signals
- Failing to verify netting enforceability in each counterparty's jurisdiction before counting netting benefits in exposure calculations — unenforced netting provides no risk reduction and regulators require gross exposure treatment where enforceability is uncertain
- Neglecting wrong-way risk in exposure measurement — standard PFE models assume independence between exposure and default probability, which can dramatically underestimate risk when the two are positively correlated
- Setting counterparty credit limits at inception but failing to reduce them when credit quality deteriorates — limits must be dynamic, with formal processes for downward revision triggered by early warning indicators
- Using a single aggregate credit limit without sub-limits by product type and tenor — a counterparty with a $200 million limit concentrated entirely in 30-year interest rate swaps presents fundamentally different risk than one with the same limit spread across short-dated FX forwards
- Treating the CSA threshold as a static parameter without linking it to the counterparty's credit rating — thresholds should step down (or reduce to zero) upon rating downgrade to ensure additional collateral is posted as credit quality weakens
- Failing to calculate and maintain pre-computed close-out amounts for counterparties on the watch list — if a counterparty defaults, the firm needs to act within hours, not days, to terminate and hedge
- Ignoring settlement risk for currencies not covered by CLS — the full notional of the first-delivered leg is exposed during the time-zone gap (mechanics in settlement-clearing)
- Assuming that central clearing eliminates counterparty risk entirely — clearing reduces but does not eliminate risk; the firm still faces clearing member default risk (for client clearers) and CCP tail risk, and must contribute to the default fund
- Permitting rehypothecation of initial margin received for uncleared derivatives — this violates uncleared margin rules and, even where not prohibited, introduces a chain of credit risk that defeats the purpose of initial margin
- Not stress testing the collateral portfolio for scenarios where collateral values decline simultaneously with exposure increases — a concentrated collateral portfolio of corporate bonds may lose value in the same market stress that increases derivative exposure
- Maintaining ISDA documentation with outdated Schedules that reference superseded regulations or contain stale credit thresholds, creating legal uncertainty about close-out mechanics and collateral obligations during a default event

## Cross-References
- **settlement-clearing** (trading-operations plugin): Owns settlement risk mechanics — DVP/PvP, CLS, Herstatt risk, and fail management; clearing and settlement infrastructure are the structural mitigants for counterparty exposure.
- **margin-operations** (trading-operations plugin): Owns Reg T and FINRA Rule 4210 brokerage margin; margin call workflows are the operational implementation of the collateral concepts in this skill.
- **trade-execution** (trading-operations plugin): Pre-deal credit limit checks must be integrated into the trade execution workflow to prevent trades that would breach counterparty exposure limits.
- **order-lifecycle** (trading-operations plugin): Counterparty selection and credit validation are pre-execution steps in the order lifecycle.
- **operational-risk** (trading-operations plugin): Counterparty default events require documented escalation, remediation, and loss attribution processes.
- **forward-risk** (wealth-management plugin): PFE calculation shares Monte Carlo risk-factor simulation techniques and infrastructure with forward-looking portfolio risk analysis.
- **fixed-income-corporate** (wealth-management plugin): Credit analysis of corporate bond issuers uses many of the same financial metrics and rating frameworks applied to counterparty credit assessment.

### Referencia: references/examples.md

# Counterparty Risk — Worked Examples

### Example 1: Setting Up a Counterparty Credit Limit Framework
**Scenario:** A mid-size institutional trading desk is establishing a counterparty credit limit framework for its OTC derivatives business. The desk trades interest rate swaps, FX forwards, and equity options with approximately 40 counterparties including major global banks, regional banks, and several large corporate end-users. The desk needs a structured framework for setting, monitoring, and enforcing counterparty credit limits.

**Design Considerations:**

The framework begins with counterparty tiering based on credit quality. The desk categorizes counterparties into four tiers:
- **Tier 1 (AA- or higher):** Major global banks with strong capital positions and diversified revenue. Maximum aggregate limit of $500 million per counterparty. These counterparties have deep liquidity, robust ISDA documentation, and active CSAs with daily margining.
- **Tier 2 (A- to A+):** Large regional banks and well-capitalized financial institutions. Maximum aggregate limit of $200 million per counterparty. These counterparties have standard ISDA documentation and CSAs, though some may have higher thresholds or less frequent margining.
- **Tier 3 (BBB- to BBB+):** Investment-grade corporates and smaller financial institutions. Maximum aggregate limit of $50 million per counterparty. These counterparties may have limited ISDA documentation and may not post collateral, requiring stricter exposure limits.
- **Tier 4 (below BBB- or unrated):** Sub-investment-grade or unrated counterparties. Maximum aggregate limit of $10 million per counterparty. Trading is restricted to short-dated, fully collateralized transactions where possible.

Within each tier, individual counterparty limits are set based on specific credit analysis. The credit analyst evaluates the counterparty's financial statements (focusing on capital adequacy ratios for banks, leverage and interest coverage for corporates), market indicators (CDS spreads, equity volatility), qualitative factors (management, business model, regulatory standing), and the expected trading relationship (product types, tenors, netting potential).

Limits are sub-allocated by product type and tenor. For a Tier 1 counterparty with a $500 million aggregate limit, the sub-allocation might be: interest rate swaps up to $300 million (with sub-limits of $200 million for tenors under 5 years and $100 million for tenors 5-30 years), FX forwards up to $150 million (all tenors under 1 year), and equity options up to $100 million. These sub-limits need not sum to the aggregate limit — the aggregate limit caps total exposure regardless of product mix.

Settlement limits are set separately from pre-settlement limits. A counterparty may have a pre-settlement limit of $200 million (covering mark-to-market exposure on outstanding trades) and a settlement limit of $50 million (covering the notional amount at risk during the settlement window). Settlement limits are particularly important for FX transactions where Herstatt risk is present and CLS is not used.

**Analysis:**

The pre-deal limit check process integrates with the trading system. Before any new trade is executed, the system calculates the incremental exposure the trade would add to the counterparty's current exposure (using a pre-deal PFE add-on based on the trade's notional, product type, and tenor) and checks whether the resulting total would exceed the limit. If the limit would be breached, the trade is blocked and routed to the credit officer for review.

Limit utilization is monitored continuously. The exposure management system recalculates counterparty exposure as market prices change, not just when new trades are booked. A counterparty whose exposure was at 60% of limit in the morning could reach 90% by afternoon if market movements cause the portfolio's mark-to-market value to increase significantly. The system generates tiered alerts: amber at 80% utilization, red at 95%, and hard block at 100%.

The credit committee reviews the entire limit framework quarterly, with ad hoc reviews triggered by material credit events. Annual reviews include a comprehensive reassessment of each counterparty's creditworthiness, a review of limit utilization patterns (counterparties whose limits are consistently underutilized may have limits reduced to free up aggregate capacity), and stress testing of the limit framework under adverse scenarios (what would happen to exposure and limit utilization if interest rates moved 200bp, FX rates moved 10%, or equity markets dropped 30%).

Governance and reporting are integral to the framework. The credit risk management function produces a daily counterparty exposure report showing each counterparty's current exposure, PFE, collateral held, net exposure, limit, and utilization percentage. A weekly summary report aggregates exposure by tier, product type, and geography, highlighting concentration risks (e.g., if 60% of total exposure is concentrated in three Tier 1 banks, the firm has significant concentration risk even if each counterparty is individually well-rated). A monthly report to senior management and the risk committee includes trend analysis, limit breach history, watch list updates, and any material changes to the credit environment. These reports form part of the firm's risk governance framework and are subject to internal audit review.

The framework should also address the treatment of wrong-way risk within the limit structure. For counterparties where the desk has identified potential wrong-way risk, the credit limit should be set more conservatively, and the PFE calculation should incorporate stress scenarios that capture the correlation between exposure and counterparty credit quality. For example, if the desk holds commodity derivatives with an energy company, and the energy company's creditworthiness deteriorates when commodity prices fall (which is precisely when the derivatives may have high positive value to the desk), the standard PFE model may understate the true risk. Explicit wrong-way risk add-ons or dedicated wrong-way risk limits can address this gap.

### Example 2: Designing Collateral Management for Bilateral OTC Trades
**Scenario:** An asset management firm is establishing bilateral OTC derivative trading capability for the first time. The firm will trade interest rate swaps and FX options to hedge portfolio exposures. The firm needs to design collateral management processes that comply with uncleared margin rules and efficiently manage collateral across multiple counterparty relationships.

**Design Considerations:**

The firm must first determine its regulatory obligations. Under the BCBS-IOSCO uncleared margin rules (implemented in the US via CFTC and prudential regulator rules, and in the EU via EMIR margin RTS), the firm must exchange both initial margin (IM) and variation margin (VM) for uncleared OTC derivatives if its aggregate average notional amount (AANA) exceeds the applicable threshold. Variation margin requirements apply to virtually all financial counterparties. Initial margin requirements apply in phased implementation based on AANA thresholds, with the final phase covering entities with AANA above $8 billion (US) or EUR 8 billion (EU).

The CSA negotiation with each counterparty must address several critical terms:

Threshold and minimum transfer amount: Under the uncleared margin rules, the VM threshold must be zero (no uncollateralized exposure is permitted for entities in scope). The MTA can be set up to $500,000 for VM. For IM, the threshold can be up to $50 million per counterparty group. The firm should negotiate these terms within regulatory constraints, balancing credit protection against operational burden.

Eligible collateral and haircuts: The firm specifies which collateral types it will accept and post. A typical schedule includes cash in major currencies (USD, EUR, GBP, JPY) with zero haircut, US Treasuries and equivalent sovereign bonds with haircuts of 0.5% to 4% depending on maturity, and investment-grade corporate bonds with haircuts of 5% to 10%. The firm should establish whether it will accept equities (higher haircut, more volatile) and set concentration limits (no more than a specified percentage of collateral in any single issuer for non-sovereign securities).

Segregation requirements: Under the uncleared margin rules, IM must be held in a segregated account at a third-party custodian. The IM cannot be rehypothecated, commingled with the receiving party's assets, or used for any purpose other than satisfying the margin obligation. VM does not have the same segregation requirement and can be held directly by the receiving party. The firm must establish custodial relationships with one or more third-party custodians (such as BNY Mellon, State Street, or JPMorgan as custody banks) to hold segregated IM.

The daily margining process follows a defined workflow. Each business day: the firm's risk system calculates the current mark-to-market value of the portfolio with each counterparty; the system calculates the required VM call (the change in net exposure since the last margin exchange) and the required IM (using either the ISDA SIMM model or a schedule-based approach); the collateral management team issues margin calls to counterparties where the firm is owed additional collateral, and responds to margin calls from counterparties where the firm owes collateral; collateral is transferred by the agreed settlement deadline (typically T+1 for cash, T+2 for securities); and the firm's records are updated to reflect the new collateral balances.

**Analysis:**

Dispute resolution is a critical operational consideration. If the firm and a counterparty disagree on the portfolio valuation (and therefore the margin call amount), the CSA dispute resolution provisions apply. The standard approach is: the parties exchange their respective valuations; if the difference exceeds a tolerance (typically $1-5 million), the parties engage in good faith negotiation; the undisputed amount is transferred while the dispute is resolved; escalation to senior management or a third-party valuation agent if the dispute is not resolved within a defined timeframe. The firm should track dispute frequency and magnitude by counterparty — persistent disputes may indicate valuation model differences that need to be reconciled.

ISDA SIMM (Standard Initial Margin Model) is the industry-standard model for calculating IM on uncleared derivatives. SIMM uses a sensitivity-based approach: the firm calculates the sensitivities of each trade to defined risk factors (delta, vega, curvature), and SIMM applies calibrated risk weights and correlations to compute the IM requirement. SIMM is recalibrated annually by ISDA using recent market data. Using SIMM rather than the regulatory schedule-based approach typically results in lower IM requirements because SIMM recognizes portfolio diversification and hedging benefits.

Collateral optimization is an ongoing operational challenge. The firm holds a pool of eligible collateral assets and must decide which assets to post to each counterparty. Cash is the cheapest to post (no haircut, immediate settlement) but has the highest opportunity cost (the firm forgoes the return on cash). Government securities are nearly as efficient (low haircut) but require settlement infrastructure and incur a small haircut cost. The firm should implement a collateral allocation algorithm that minimizes the total cost of collateral across all counterparty relationships, considering haircuts, opportunity costs, settlement timing, and any counterparty-specific collateral preferences.

The firm should also prepare for stressed collateral scenarios. During market stress, the value of non-cash collateral may decline (increasing the amount of collateral needed to meet margin requirements), margin calls may increase sharply (as portfolio MTM values swing), and counterparties may reject previously acceptable collateral types. The firm should maintain a buffer of high-quality liquid assets (cash and short-dated government securities) above minimum margin requirements to absorb margin call increases without needing to liquidate portfolio positions.

Operational infrastructure is a significant consideration for a firm establishing bilateral OTC capability for the first time. The firm needs: a collateral management system that tracks collateral balances by counterparty, calculates margin calls, and manages substitution requests; connectivity to custodian banks for collateral transfers (SWIFT messaging, custodian portals); legal documentation (CSAs negotiated and executed with each counterparty); accounting processes for recording collateral received and posted, including treatment of interest on cash collateral (typically paid at the federal funds rate or a negotiated rate); and trained personnel to manage the daily margin call process, respond to disputes, and coordinate collateral movements across counterparties and custodians. The operational cost of collateral management is non-trivial — firms should budget for systems, custody fees, and dedicated operations staff before entering bilateral OTC markets.


---

## SKILL: diversification

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/diversification` (MIT)
- Cuándo usarla: Build diversified portfolios using correlation analysis, efficient frontier construction, and factor-based diversification. Use when the user asks about portfolio variance, correlation effects, the efficient frontier, minimum variance portfolios, diversification ratios, or factor diversification. Also trigger when users mention 'don't put all eggs in one basket', 'how many stocks do I need', 'correlation breakdown in a crisis', 'are my holdings really diversified', 'risk contributions', or ask why diversification fails during market crashes.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/wealth-management/skills/diversification/` (diversification.py)

# Diversification

## Core Concepts

### Portfolio Variance (2 Assets)
For a portfolio of two assets with weights w_1 and w_2, volatilities sigma_1 and sigma_2, and correlation rho_12:

sigma^2_p = w_1^2 * sigma_1^2 + w_2^2 * sigma_2^2 + 2 * w_1 * w_2 * sigma_1 * sigma_2 * rho_12

Diversification benefit arises whenever rho_12 < 1, because the portfolio volatility will be less than the weighted average of individual volatilities.

### Portfolio Variance (n Assets)
In matrix notation for n assets with weight vector w and covariance matrix Sigma:

sigma^2_p = w' * Sigma * w

This generalizes to any number of assets and captures all pairwise correlations.

### Diversification Benefit
Portfolio volatility is strictly less than the weighted average of individual volatilities whenever any pairwise correlation is below 1:

sigma_p < Sigma(w_i * sigma_i)  when rho_ij < 1 for some i,j

The lower the average correlation, the greater the diversification benefit.

### Efficient Frontier
The efficient frontier is the set of portfolios that offer the highest expected return for each level of risk (or equivalently, the lowest risk for each level of return). Portfolios below the frontier are suboptimal — they can be improved by reallocating weights.

### Minimum Variance Portfolio
The portfolio with the lowest possible volatility, regardless of expected returns:

w_mv = Sigma^(-1) * 1 / (1' * Sigma^(-1) * 1)

where 1 is a vector of ones. This portfolio depends only on the covariance matrix, not on expected returns, making it more robust to estimation error.

### Correlation Regimes
Correlations are not constant. In market crises, correlations between risky assets tend to increase sharply ("correlation breakdown" or "correlation tightening"), reducing the diversification benefit precisely when it is needed most. Key implications:
- Stress-test portfolios using crisis-period correlation matrices
- Diversification across asset classes (stocks, bonds, commodities, real assets) is more robust than within-asset-class diversification

### Diversification Ratio
A measure of how much diversification a portfolio achieves:

DR = (Sigma(w_i * sigma_i)) / sigma_p

A portfolio of perfectly correlated assets has DR = 1. Higher DR indicates more effective diversification. A fully diversified equal-volatility portfolio with zero correlations has DR = sqrt(n).

### Maximum Diversification Portfolio
The portfolio that maximizes the diversification ratio. This is an alternative to mean-variance optimization that does not require expected return inputs — it relies only on volatilities and correlations.

### Factor Diversification
True diversification means exposure to multiple independent risk factors, not merely holding many assets. Assets that share the same factor exposures (e.g., multiple tech stocks all driven by growth factor) provide less diversification than their number suggests. Key factors:
- Market, size, value, momentum, quality, low volatility
- Interest rate, credit, inflation
- Geographic, sector, currency

### Risk Contribution
The risk contribution of asset i to portfolio volatility:

RC_i = w_i * (Sigma * w)_i / sigma_p

where (Sigma * w)_i is the i-th element of the vector Sigma * w. The sum of all risk contributions equals the portfolio volatility. This decomposition reveals which assets truly drive portfolio risk.

### Marginal Risk Contribution
The rate of change of portfolio volatility with respect to the weight of asset i:

MRC_i = (Sigma * w)_i / sigma_p

Risk contribution = weight * marginal risk contribution: RC_i = w_i * MRC_i

### Diminishing Marginal Diversification
The diversification benefit of adding assets decreases rapidly. Empirically:
- 15-20 uncorrelated assets capture most of the diversification benefit
- Beyond 30 assets, incremental risk reduction is minimal
- The asymptotic portfolio variance equals the average covariance (systematic risk cannot be diversified away)

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| 2-Asset Portfolio Variance | sigma^2_p = w_1^2*sigma_1^2 + w_2^2*sigma_2^2 + 2*w_1*w_2*sigma_1*sigma_2*rho_12 | Two-asset risk calculation |
| n-Asset Portfolio Variance | sigma^2_p = w' * Sigma * w | General portfolio risk |
| Minimum Variance Weights | w_mv = Sigma^(-1)*1 / (1'*Sigma^(-1)*1) | Lowest-risk portfolio |
| Diversification Ratio | DR = Sigma(w_i*sigma_i) / sigma_p | Measure of diversification |
| Risk Contribution | RC_i = w_i * (Sigma*w)_i / sigma_p | Asset-level risk attribution |
| Marginal Risk Contribution | MRC_i = (Sigma*w)_i / sigma_p | Sensitivity of risk to weight |
| Asymptotic Variance | sigma^2_p → avg(cov_ij) as n → infinity | Diversification limit |

## Worked Examples

### Example 1: Two-Asset Portfolio Volatility
**Given:**
- Stock: sigma = 20%, weight = 60%
- Bond: sigma = 5%, weight = 40%
- Correlation: rho = 0.2

**Calculate:** Portfolio volatility

**Solution:**

sigma^2_p = (0.60)^2 * (0.20)^2 + (0.40)^2 * (0.05)^2 + 2 * (0.60) * (0.40) * (0.20) * (0.05) * (0.20)

sigma^2_p = 0.36 * 0.04 + 0.16 * 0.0025 + 2 * 0.60 * 0.40 * 0.20 * 0.05 * 0.20

sigma^2_p = 0.0144 + 0.0004 + 0.00096

sigma^2_p = 0.01576

sigma_p = sqrt(0.01576) = 0.1255 = **12.55%**

Weighted average volatility = 0.60 * 20% + 0.40 * 5% = 14.0%

Diversification benefit = 14.0% - 12.55% = **1.45 percentage points** of risk reduction.

### Example 2: Diversification Ratio for a 4-Asset Portfolio
**Given:**
- Assets: A (sigma=15%, w=25%), B (sigma=20%, w=25%), C (sigma=10%, w=25%), D (sigma=18%, w=25%)
- Portfolio volatility (computed from full covariance matrix): sigma_p = 10.5%

**Calculate:** Diversification ratio

**Solution:**

Weighted average volatility = 0.25*15% + 0.25*20% + 0.25*10% + 0.25*18%
= 3.75% + 5.0% + 2.5% + 4.5% = 15.75%

Diversification Ratio = 15.75% / 10.5% = **1.50**

Interpretation: The portfolio achieves significant diversification — the weighted average volatility is 50% higher than the actual portfolio volatility. A DR of 1.50 indicates meaningful correlation benefits. For comparison, a portfolio of perfectly correlated assets would have DR = 1.0.

## Common Pitfalls
- Diversification is not just about holding more assets — correlation structure is what matters; 50 highly correlated stocks provide less diversification than 10 uncorrelated ones
- Correlations are unstable and tend to increase during market stress, reducing the diversification benefit precisely when it is most needed
- Over-diversification (diworsification): holding too many positions dilutes high-conviction ideas and guarantees mediocre returns after costs
- Home country bias: investors systematically under-allocate to international assets, missing a major source of diversification
- Confusing asset diversification with factor diversification: a portfolio of 20 growth stocks is not diversified despite holding many names
- Using historical correlations without testing sensitivity to regime changes

## Cross-References
- **historical-risk** (wealth-management plugin): volatility, correlation, and systematic vs. idiosyncratic risk foundations
- **asset-allocation** (wealth-management plugin): diversification principles feed directly into portfolio construction and optimization
- **rebalancing** (wealth-management plugin): maintaining diversification targets over time through rebalancing
- **bet-sizing** (wealth-management plugin): position sizing interacts with diversification — concentrated vs. diversified approaches
- **equity-compensation** (wealth-management plugin): concentrated employer stock from RSUs, options, and ESPPs is a common source of single-stock concentration requiring staged diversification
- **factor-investing** (wealth-management plugin): diversifying across factor premia (value, momentum, quality) as a layer distinct from asset-class diversification
## Running the Script

```bash
uv run scripts/diversification.py            # run the demo (uses PEP 723 inline deps)
uv run scripts/diversification.py --verify   # check demo outputs against the worked examples (exit 1 on mismatch)
python3 scripts/diversification.py            # alternative (requires: pip install numpy)
```

The demo prints the calculations covered above; its values match the worked examples in this skill. Run `--help` for a list of the classes and functions. For programmatic use, import the module rather than running it — the demo only executes under `python diversification.py`.


---

## SKILL: drawdown-circuit-breaker

- Fuente: `tradermonty/claude-trading-skills` → `skills/drawdown-circuit-breaker` (MIT)
- Cuándo usarla: Evaluate account-level drawdown circuit breaker rules from trader-memory-core state and decide whether new trade risk is allowed today. Uses realized P&L, losing-streak cooldowns, and weekly/monthly drawdown limits without any external API.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/drawdown-circuit-breaker/` (requirements.txt, _market_calendar.py, check_circuit_breaker.py)

# Drawdown Circuit Breaker

## Overview

Evaluate whether the trader should take new trade risk today based on account-level realized P&L and recent terminal trade outcomes. This skill reads trader-memory-core thesis YAML files only. It produces a `circuit_breaker_decision` artifact that complements the market-side `exposure_decision` from exposure-coach.

The circuit breaker is a recommendation and recordkeeping tool. It does not replace human judgment, and it does not enforce broker-side blocks or automated order rejection.

## When to Use

- Before screening or sizing any new swing trade candidate
- After a losing trade or partial trim to check whether a cooldown is active
- During daily planning when trader-memory-core contains recent closed or partially closed positions
- As a workflow gate before swing-opportunity-daily proceeds to candidate generation
- When reviewing whether daily, weekly, or monthly loss limits have been breached

## Prerequisites

- Python 3.9+
- Local trader-memory-core thesis YAML files, usually under `state/theses/`
- Account size in dollars
- No API keys or network access required

## Workflow

### Step 1: Read Trader Memory State

Point the script at the thesis state directory:

```bash
python3 skills/drawdown-circuit-breaker/scripts/check_circuit_breaker.py \
  --state-dir state/theses \
  --account-size 100000 \
  --output-dir reports/
```

The script scans every `th_*.yaml` file and reads realized P&L from each thesis `status_history[]` ledger entry. It does not use `_index.json` for P&L, because the index is a lightweight lookup file and does not contain the required realized-P&L ledger.

After validating each file, the script groups valid theses by the case-sensitive, whitespace-trimmed `thesis_id`. If two or more valid files share an ID, it excludes the entire duplicate group from P&L and losing-streak calculations, reports every actual source path, and returns `PARTIAL` + `HALTED` until the duplicate state is repaired and the decision is rerun. `metrics.theses_scanned` counts only accepted theses with unique IDs.

If the state directory is missing or is an empty directory, the skill returns `TRADING_ALLOWED` with `data_quality: EMPTY_STATE` so a new user is not blocked by the absence of history. If the configured state path exists but is not a directory, the skill fails closed as incomplete state data.

If state exists but a thesis, ledger event, or terminal result must be skipped or conflicts with another recorded value, the skill fails closed with `data_quality: PARTIAL`, `recommendation: HALTED`, and an `incomplete_state_data` rule. Repair the warnings and rerun before taking new risk. The one recoverable exception is a finite terminal `outcome.pnl_dollars` fallback for a legacy thesis with no realized-P&L ledger entry; it remains visible as `PARTIAL` but does not by itself override the calculated recommendation. For `ACTIVE`, `PARTIALLY_CLOSED`, `CLOSED`, and `INVALIDATED` theses, each history event must be an object with a recognized `status` and parseable `at`, and the last history status must match the thesis status. `ACTIVE` and `PARTIALLY_CLOSED` theses must also carry entry actuals; `PARTIALLY_CLOSED` must carry a position. Malformed, stale, or skeletal lifecycle history disqualifies terminal fallback and halts. Ledger-shaped events whose `realized_pnl` is missing, untyped, or non-finite also halt instead of being coerced.

### Step 2: Evaluate Circuit Breaker Rules

The default rules are:

| Rule | Default | Triggered State | Release |
|------|---------|-----------------|---------|
| Max daily loss | 2.0% of account | HALTED | Next ET weekday |
| Losing streak cooldown | 2 terminal losing theses | COOLDOWN | 24 hours after latest loss exit |
| Weekly drawdown halt | 5.0% of account | HALTED | Next Monday ET |
| Monthly drawdown halt | 8.0% of account | HALTED | First day of next month ET |

Day, week, and month boundaries use `America/New_York`. Date-only producer
timestamps from `trader-memory-core` are counted on the named ET date. Set
`--as-of` for deterministic evaluation; date-only `--as-of` values cover the
full ET day, while timestamp values exclude future events after that time:

```bash
python3 skills/drawdown-circuit-breaker/scripts/check_circuit_breaker.py \
  --state-dir state/theses \
  --account-size 100000 \
  --as-of 2026-07-02T12:00:00-04:00 \
  --output-dir reports/
```

### Step 3: Override Thresholds When Needed

Override individual thresholds on the CLI:

```bash
python3 skills/drawdown-circuit-breaker/scripts/check_circuit_breaker.py \
  --account-size 100000 \
  --max-daily-loss-pct 1.5 \
  --losing-streak-n 3 \
  --cooldown-hours 48 \
  --weekly-drawdown-pct 4 \
  --monthly-drawdown-pct 6
```

Or provide a JSON config file:

```json
{
  "max_daily_loss_pct": 1.5,
  "losing_streak_n": 3,
  "cooldown_hours": 48,
  "weekly_drawdown_pct": 4.0,
  "monthly_drawdown_pct": 6.0
}
```

CLI arguments override config-file values.

### Step 4: Interpret the Decision

Use the generated decision as a gate for new trade risk:

| Recommendation | Meaning |
|----------------|---------|
| TRADING_ALLOWED | No circuit breaker rule is active; new trade risk may proceed through the rest of the workflow |
| COOLDOWN | Do not open new positions; continue managing existing positions and review the recent losses |
| HALTED | Stop new entries because a drawdown limit is active or account-state data is incomplete; repair/rerun any data warnings before proceeding |

Existing position management remains a human decision. The circuit breaker is designed to prevent new risk escalation after realized damage, not to force liquidation.

Time-based rules carry an ISO 8601 `active_until`. The non-time-based `incomplete_state_data` rule uses `active_until: null`; its Markdown report says the halt lasts until the state is repaired and the decision is rerun.

## Output Format

The script writes `circuit_breaker_decision_YYYY-MM-DD_HHMMSS.json` and, unless `--json-only` is set, a matching markdown report.

```json
{
  "schema_version": "1.0",
  "generated_at": "2026-07-02T16:00:00+00:00",
  "as_of_date": "2026-07-02",
  "recommendation": "COOLDOWN",
  "triggered_rules": [
    {
      "rule": "losing_streak_cooldown",
      "threshold": 2,
      "observed": 2,
      "active_until": "2026-07-02T15:30:00-04:00",
      "detail": "2 consecutive losing closes; last loss exit 2026-07-01T15:30:00-04:00."
    }
  ],
  "metrics": {
    "realized_pnl_today": 0.0,
    "realized_pnl_wtd": -250.0,
    "realized_pnl_mtd": -250.0,
    "consecutive_losses": 2,
    "last_loss_exit_at": "2026-07-01T15:30:00-04:00",
    "theses_scanned": 12
  },
  "account_size": 100000.0,
  "config": {
    "max_daily_loss_pct": 2.0,
    "losing_streak_n": 2,
    "cooldown_hours": 24.0,
    "weekly_drawdown_pct": 5.0,
    "monthly_drawdown_pct": 8.0
  },
  "data_quality": "OK",
  "warnings": [],
  "rationale": "Recent losing closes triggered a cooldown. Avoid new entries until the cooldown expires."
}
```

## Exchange Calendar Contract

Install `requirements.txt` before running the checker. Daily, weekly, and
monthly halt dates use actual XNYS sessions. `active_until` remains compatible:
the halt ends at 00:00 America/New_York on the next eligible session date, not
at that session's opening bell. Use `--as-of` for deterministic evaluation.

## Resources

- `scripts/check_circuit_breaker.py` - Main CLI and rule engine
- `references/circuit_breaker_framework.md` - Rule definitions, defaults, and data-source notes
- `skills/trader-memory-core/schemas/thesis.schema.json` - Source schema for thesis state

## Key Principles

1. **Realized damage only** - Use recorded realized P&L, not unrealized P&L or thesis-level cumulative fields for daily calculations.
2. **Survival first** - A circuit breaker exists to prevent escalation after losses.
3. **Advisory, not automatic execution** - The output informs the workflow gate; it does not place, cancel, or block broker orders.
4. **Fail closed on incomplete state** - Empty state allows a new user to begin, but malformed, discarded, conflicting, or non-finite risk data returns `PARTIAL` + `HALTED` without crashing. A finite legacy outcome fallback is reported as recoverable `PARTIAL` and remains non-blocking.

### Referencia: references/circuit_breaker_framework.md

# Drawdown Circuit Breaker Framework

## Purpose

The drawdown circuit breaker is an account-level risk gate for new trade risk. It answers one question before screening or sizing: "Is the trader's account state clear enough to take another new trade today?"

This is the trader-side companion to the market-side exposure gate. Exposure-coach asks whether the market environment allows new exposure. Drawdown-circuit-breaker asks whether the trader's realized account damage and recent execution results allow new risk.

## Source Data

Read only trader-memory-core thesis YAML files from `state/theses/` or a caller-provided `--state-dir`.

Use these fields:

- `status_history[][].realized_pnl` for realized P&L ledger entries
- `status_history[][].at` for the realized P&L event timestamp
- `status` to identify terminal theses (`CLOSED`, `INVALIDATED`)
- `exit.actual_date`, falling back to the last terminal `status_history[].at`, parsed and converted to `America/New_York` for terminal trade ordering
- `outcome.pnl_dollars` for terminal win/loss classification

Do not use `_index.json` for P&L. It is a lightweight lookup index and does not contain the ledger required for partial trims or daily realized-P&L accounting.

Treat the case-sensitive, whitespace-trimmed `thesis_id` as the logical identity only after a thesis file has passed validation. If multiple valid files share an ID, exclude every file in that duplicate group from both realized-P&L and terminal-streak calculations. Emit a deterministic warning with every actual source path, return `PARTIAL` + `HALTED`, and require state repair plus a rerun. Do not use an input YAML `_source_path` value as audit evidence. `metrics.theses_scanned` is the count of accepted valid theses whose IDs are unique.

## Calendar Rules

All daily, weekly, and monthly realized-P&L aggregations use `America/New_York` dates.

- Daily: events whose ET date equals the as-of date and whose timestamp is not after `--as-of`
- Weekly: events from Monday ET through the as-of timestamp
- Monthly: events from the first calendar day of the ET month through the as-of timestamp

`trader-memory-core` widens bare producer dates to UTC midnight (for example
`2026-07-02T00:00:00+00:00`). This artifact is counted on the named ET
accounting date, not the prior ET evening.

The script accepts `--as-of` so tests and sample runs can freeze the evaluation date.
Date-only values cover the full ET day; timestamp values are exact cutoffs.

## Default Rules

| Rule | Default | State | Active Until |
|------|---------|-------|--------------|
| `max_daily_loss` | Realized loss reaches 2.0% of account size on the as-of ET date | `HALTED` | Next ET weekday |
| `losing_streak_cooldown` | Two consecutive terminal theses have negative `outcome.pnl_dollars` | `COOLDOWN` | 24 hours after the latest losing exit |
| `weekly_drawdown_halt` | Week-to-date realized loss reaches 5.0% of account size | `HALTED` | Next Monday ET |
| `monthly_drawdown_halt` | Month-to-date realized loss reaches 8.0% of account size | `HALTED` | First day of next ET month |

Break-even terminal theses count as wins. This matches trader-memory-core monthly review behavior, where `pnl >= 0` is classified as a win.

If multiple rules trigger, return the strictest state:

1. `HALTED`
2. `COOLDOWN`
3. `TRADING_ALLOWED`

Include every active triggered rule in the JSON artifact even when a stricter rule determines the final recommendation.

## Data Quality

| Value | Meaning |
|-------|---------|
| `OK` | State directory existed, thesis files loaded, and no malformed ledger or terminal records were skipped |
| `EMPTY_STATE` | State directory was missing, or it was an existing directory containing no `th_*.yaml` files |
| `PARTIAL` | At least one data warning was emitted, including skipped/conflicting risk data or a recovered finite legacy outcome |

`EMPTY_STATE` returns `TRADING_ALLOWED`. The skill should not block a new user just because no trader-memory-core state exists yet.

`PARTIAL` fails closed with `HALTED` and an `incomplete_state_data` rule whenever the configured state path is not a directory, whenever a valid `thesis_id` is duplicated, or whenever a thesis, ledger entry, or terminal result is skipped, malformed, non-finite, missing, or conflicts with another P&L source. Its `active_until` is `null` because release requires state repair and a rerun, not elapsed time. The sole recoverable warning is a finite `outcome.pnl_dollars` value used for a legacy terminal thesis that has no realized-P&L ledger entry and otherwise has parseable terminal history. For `ACTIVE`, `PARTIALLY_CLOSED`, `CLOSED`, and `INVALIDATED` theses, every history event must be an object with a recognized `status` and parseable `at`, and the last history status must match the thesis status. `ACTIVE` and `PARTIALLY_CLOSED` theses must also carry entry actuals; `PARTIALLY_CLOSED` must carry a position. Malformed, stale, or skeletal lifecycle history disqualifies the fallback and halts. Ledger-shaped events -- `status: PARTIALLY_CLOSED`, or any of `shares_sold`, `quantity_sold`, `price`, `proceeds` -- whose `realized_pnl` is missing, untyped, or non-finite also halt instead of being coerced. The recoverable fallback remains `PARTIAL` for audit visibility but does not by itself change the calculated recommendation.

Account size and all percentage/hour thresholds must be positive and finite. Non-finite P&L never enters metrics or terminal streak calculations, and JSON output is serialized with non-finite values disabled.

## Configuration

Defaults can be overridden with CLI flags or a JSON config file. CLI flags take precedence.

```json
{
  "max_daily_loss_pct": 2.0,
  "losing_streak_n": 2,
  "cooldown_hours": 24,
  "weekly_drawdown_pct": 5.0,
  "monthly_drawdown_pct": 8.0
}
```

Use lower thresholds for capital-preservation mode and higher thresholds only after the trader has documented why the extra variance is acceptable.

## Workflow Gate Contract

The workflow artifact ID is `circuit_breaker_decision`.

The swing-opportunity-daily workflow should proceed to new candidate generation only when:

```text
circuit_breaker_decision.recommendation == "TRADING_ALLOWED"
```

`COOLDOWN` and `HALTED` both block new entries. They do not automatically force exits or broker actions.


---

## SKILL: ethics-hotline-triage

- Fuente: `SYasJ/claude-business-skills` → `plugins/risk/skills/ethics-hotline-triage` (MIT)
- Cuándo usarla: Triage a hotline report toward the right independent handler, without retaliation or a verdict. Use when the user mentions ethics hotline, speak-up report, ethics triage, hotline intake, or asks for a hotline triage. Risk and compliance skill by Yasir Jilani.

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'ethics-hotline-triage' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Ethics Hotline Triage

Triage a hotline report toward the right independent handler, without retaliation or a verdict.

## When to use this skill

Use this skill when the user:

- ethics hotline
- speak-up report
- ethics triage
- hotline intake

## When not to use this skill

- Retaliation
- Cover-up

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

- The allegation summary
- Who it names
- Safety issues
- The company's routing rules

## Workflow


### 1. Step 1

If someone is in immediate danger, point to emergency services and their safety process.
### 2. Step 2

Record the allegation without adding motive.
### 3. Step 3

Route away from anyone named in the report.
### 4. Step 4

Minimize personal data in the routing note.
### 5. Step 5

Refuse any request to identify or punish the reporter for reporting.
### 6. Step 6

This triage is not an investigation finding.

## Output

Deliver a **hotline triage**.

- Purpose of this hotline triage, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a hotline triage by 30 September 2026. A report names the division president, and the president asks to handle it personally.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A report names the division president, and the president asks to handle it personally.

The allegation summary: Control 7.2 access review, recorded 14 September 2026. No supporting file attached
Who it names: Priya Shah, controller
Safety issues: Issue log item 18. Partly documented: the what is written down, the who is not
The company's routing rules: their one-page rule dated 2 Mar 2026. No exception log since
```

### Example outcome

**Hotline triage**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Routes around the president and refuses retaliation against the reporter.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The allegation summary | Control 7.2 access review, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| Who it names | Priya Shah, controller | Carried into the draft |
| Safety issues | Issue log item 18. Partly documented: the what is written down, the who is not | Carried into the draft |
| The company's routing rules | their one-page rule dated 2 Mar 2026. No exception log since | Needs confirmation |

**How this draft was built**

**1. If someone is in immediate danger, point to emergency services and their safety process**

**2. Record the allegation without adding motive**

**3. Route away from anyone named in the report**

**4. Minimize personal data in the routing note**

**5. Refuse any request to identify or punish the reporter for reporting**

**Deliberately not done**
- A verdict at triage.
- Retaliation.
- Routing to the accused.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A verdict at triage
- Retaliation
- Routing to the accused

## Related skills

- `whistleblower-intake`
- `employee-relations-intake`


---

## SKILL: fixed-income-portfolio

- Fuente: `anthropics/financial-services` → `plugins/partner-built/lseg/skills/fixed-income-portfolio` (Apache-2.0)
- Cuándo usarla: Review fixed income portfolios by pricing multiple bonds, retrieving reference data, analyzing cashflows, and running scenario analysis. Use when reviewing bond portfolios, computing portfolio duration and DV01, analyzing cashflow waterfalls, stress testing rate scenarios, or assessing portfolio composition.

# Fixed Income Portfolio Analysis

You are an expert fixed income portfolio analyst. Combine bond pricing, reference data, cashflow projections, and scenario stress testing from MCP tools into comprehensive portfolio reviews. Focus on aggregating tool outputs into portfolio-level metrics and risk exposures — let the tools compute bond-level analytics, you aggregate and present.

## Core Principles

Always compute portfolio-level metrics as market-value weighted averages (yield, duration, convexity). Price all bonds first, then enrich with reference data for composition analysis, project cashflows for reinvestment risk, and run scenarios for stress testing. Frame everything relative to a benchmark when available.

## Available MCP Tools

- **`bond_price`** — Price bonds. Returns clean/dirty price, yield, duration, convexity, DV01, spread. Accepts comma-separated identifiers for batch pricing.
- **`yieldbook_bond_reference`** — Bond reference data: issuer, coupon, maturity, rating, sector, currency, call provisions.
- **`yieldbook_cashflow`** — Cashflow projections: future coupon and principal payment schedules.
- **`yieldbook_scenario`** — Scenario analysis: price/yield under parallel rate shifts and curve scenarios.
- **`interest_rate_curve`** — Government yield curves. Use for spread-to-curve context and curve environment assessment.
- **`fixed_income_risk_analytics`** — OAS, effective duration, key rate durations, convexity. Use for bonds with embedded options.

## Tool Chaining Workflow

1. **Price All Bonds:** Call `bond_price` for all holdings. Extract yield, duration, DV01, convexity, spread per bond.
2. **Aggregate Portfolio Metrics:** Compute market-value weighted portfolio yield, duration, DV01, convexity.
3. **Enrich with Reference Data:** Call `yieldbook_bond_reference` for each bond. Build sector, rating, maturity, and currency breakdowns.
4. **Project Cashflows:** Call `yieldbook_cashflow` for the portfolio. Aggregate into a quarterly cashflow waterfall. Flag concentration periods.
5. **Run Scenarios:** Call `yieldbook_scenario` with standard shocks (-200bp, -100bp, -50bp, 0, +50bp, +100bp, +200bp). Identify top risk contributors.
6. **Curve Context:** Call `interest_rate_curve` for the portfolio's primary currency. Compute spread to curve for each bond.
7. **Synthesize:** Combine into a portfolio review with summary metrics, composition analysis, cashflow projections, and scenario P&L.

## Output Format

### Portfolio Summary
| Metric | Portfolio | Benchmark | Active |
|--------|-----------|-----------|--------|
| Market Value | ... | -- | -- |
| Yield (YTW) | ... | ... | +/-... bp |
| Mod. Duration | ... | ... | +/-... |
| DV01 ($) | ... | ... | +/-... |
| Avg Rating | ... | ... | -- |

### Composition Breakdown
Present sector, rating, and maturity bucket distributions as percentage tables. Flag overweights/underweights vs benchmark.

### Cashflow Waterfall
| Period | Coupon Income | Principal | Total Cash |
|--------|--------------|-----------|-----------|
| Q1 | ... | ... | ... |
| Q2 | ... | ... | ... |

### Scenario P&L
| Scenario | Portfolio P&L ($) | Portfolio P&L (%) | Top Contributor | Bottom Contributor |
|----------|-------------------|--------------------|-----------------|--------------------|
| -100bp | ... | ... | ... | ... |
| Base | -- | -- | -- | -- |
| +100bp | ... | ... | ... | ... |
| +200bp | ... | ... | ... | ... |


---

## SKILL: forward-risk

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/forward-risk` (MIT)
- Cuándo usarla: Estimate potential future losses using VaR, Expected Shortfall, Monte Carlo simulation, and stress testing. Use when the user asks about Value-at-Risk, CVaR, Expected Shortfall, scenario analysis, stress testing, or factor-based risk decomposition. Also trigger when users mention 'how much could I lose', 'worst-case scenario', 'tail risk', 'risk budget', 'component VaR', 'marginal VaR', '99% confidence loss', 'Monte Carlo simulation', or ask how to project portfolio risk forward.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/wealth-management/skills/forward-risk/` (forward_risk.py)

# Forward-Looking Risk Analysis

## Core Concepts

### Parametric (Variance-Covariance) VaR
Assumes returns are normally distributed. For a single asset or portfolio in dollar terms (assuming zero expected return over short horizons):

```
VaR = W * z_alpha * sigma_p
```

where:
- W = portfolio value
- z_alpha = z-score for confidence level (1.645 for 95%, 2.326 for 99%)
- sigma_p = portfolio volatility over the relevant horizon

More generally, including expected return:

```
VaR_alpha = mu - z_alpha * sigma
```

To convert from 1-day VaR to h-day VaR (assuming i.i.d. returns):

```
VaR_h = VaR_1 * sqrt(h)
```

### Portfolio VaR (Multiple Assets)
For a portfolio with weight vector w and covariance matrix Sigma:

```
sigma_p = sqrt(w' * Sigma * w)
VaR_p   = W * z_alpha * sqrt(w' * Sigma * w)
```

The covariance matrix captures both individual volatilities and correlations between assets.

### Monte Carlo VaR
Simulate a large number of portfolio return scenarios (e.g., 10,000+), then take the alpha-percentile of the simulated loss distribution.

Steps:
1. Estimate the return distribution parameters (mean vector, covariance matrix, or use a copula model).
2. Generate N random return scenarios (e.g., via Cholesky decomposition of the covariance matrix for multivariate normal).
3. Compute portfolio return for each scenario.
4. Sort results and identify the alpha-percentile loss.

Monte Carlo VaR can accommodate non-normal distributions, fat tails, path-dependent instruments, and nonlinear payoffs (e.g., options).

### Conditional VaR (CVaR) / Expected Shortfall
CVaR answers: "Given that losses exceed VaR, what is the expected loss?"

```
ES_alpha = E[Loss | Loss > VaR_alpha]
```

For a normal distribution:

```
ES_alpha = mu + sigma * phi(z_alpha) / (1 - alpha)
```

where phi is the standard normal PDF.

CVaR is a **coherent risk measure** (unlike VaR) because it satisfies subadditivity: CVaR(A+B) <= CVaR(A) + CVaR(B). This means diversification always reduces or maintains CVaR, which is not guaranteed for VaR.

### Component VaR
Decomposes total portfolio VaR into contributions from each position. Component VaRs sum to total VaR.

```
CVaR_i = w_i * beta_i * VaR_p
```

where beta_i = Cov(R_i, R_p) / Var(R_p) is the asset's beta to the portfolio.

Equivalently:

```
CVaR_i = w_i * (partial VaR / partial w_i)
sum(CVaR_i) = VaR_p
```

This decomposition identifies which positions are the largest contributors to portfolio risk.

### Marginal VaR
Measures the rate of change of portfolio VaR with respect to a small increase in a position's weight.

```
MVaR_i = partial(VaR_p) / partial(w_i) = z_alpha * (Sigma * w)_i / sigma_p
```

Marginal VaR is used for position sizing: adding to a position with low marginal VaR reduces portfolio risk more efficiently.

### Scenario Analysis
Apply specific historical or hypothetical market moves to the current portfolio to estimate P&L impact.

- **Historical scenarios:** Replay actual market events (e.g., 2008 GFC, 2020 COVID crash, 2022 rate hiking cycle) with current holdings.
- **Hypothetical scenarios:** Construct custom shocks (e.g., "equities -20%, rates +200bp, credit spreads +300bp, USD +10%").

Scenario P&L is computed by applying the scenario returns to current position exposures and revaluing.

### Stress Testing
A structured framework for assessing portfolio resilience under extreme but plausible conditions.

Common stress scenarios:
- Equity crash: S&P 500 -30% to -40%
- Interest rate shock: +300bp parallel shift
- Credit crisis: investment-grade spreads +200bp, high-yield +800bp
- Liquidity freeze: bid-ask spreads widen 10x, forced selling at discount
- Currency shock: major currency pair moves 15-20%
- Stagflation: inflation +5%, GDP -3%, rates +200bp

Stress tests should include second-order effects: margin calls, liquidity demands, correlation spikes, counterparty risk.

### Factor-Based Risk Decomposition
Separate total portfolio risk into systematic factor risk and idiosyncratic (security-specific) risk.

```
sigma^2_p = b' * Sigma_f * b + sum(w_i^2 * sigma^2_epsilon_i)
```

where:
- b = vector of portfolio factor exposures
- Sigma_f = factor covariance matrix
- sigma^2_epsilon_i = idiosyncratic variance of asset i

Common factor models: Fama-French (market, size, value, momentum), Barra risk models, PCA-based statistical factors.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Parametric VaR (single) | W * z_alpha * sigma | Simple position VaR |
| Portfolio VaR | W * z_alpha * sqrt(w' * Sigma * w) | Multi-asset VaR |
| Multi-day VaR | VaR_1 * sqrt(h) | Scale to h-day horizon |
| CVaR (normal) | mu + sigma * phi(z_alpha) / (1 - alpha) | Expected tail loss |
| Component VaR | w_i * beta_i * VaR_p | Risk contribution per position |
| Marginal VaR | z_alpha * (Sigma * w)_i / sigma_p | Sensitivity to weight change |
| Factor Risk | b' * Sigma_f * b | Systematic risk component |
| Idiosyncratic Risk | sum(w_i^2 * sigma^2_epsilon_i) | Security-specific risk |

## Worked Examples

### Example 1: Parametric 95% VaR
**Given:** A $1,000,000 equity portfolio with an annualized volatility of 15%.

**Calculate:** 1-day 95% parametric VaR (assuming 252 trading days and zero expected daily return).

**Solution:**

Daily volatility:

```
sigma_daily = 0.15 / sqrt(252) = 0.15 / 15.875 = 0.00945
```

1-day 95% VaR:

```
VaR = $1,000,000 * 1.645 * 0.00945 = $15,545
```

Alternatively, computing directly from annual figures:

```
VaR_annual = $1,000,000 * 1.645 * 0.15 = $246,750
VaR_1day   = $246,750 / sqrt(252)       = $15,545
```

Interpretation: There is a 5% chance of losing more than $15,545 in a single day under normal market conditions.

### Example 2: Monte Carlo VaR
**Given:** A two-asset portfolio (60% equities, 40% bonds). Equities: mu = 10%, sigma = 18%. Bonds: mu = 4%, sigma = 5%. Correlation rho = -0.2. Portfolio value = $1,000,000.

**Calculate:** 95% annual VaR via Monte Carlo simulation (conceptual steps).

**Solution:**

1. **Construct covariance matrix:**

```
Sigma = | 0.0324  -0.0018 |
        | -0.0018  0.0025 |
```

2. **Cholesky decomposition** of Sigma to get lower triangular matrix L.

3. **Simulate 10,000 scenarios:** For each simulation, draw z ~ N(0, I), compute r = mu + L*z, then portfolio return R_p = w' * r.

4. **Compute portfolio P&L** for each scenario: P&L = $1,000,000 * R_p.

5. **Sort P&L** from worst to best. The 500th worst (5th percentile) is the 95% VaR.

For this portfolio, the analytical answer provides a benchmark:

```
sigma_p = sqrt(0.6^2 * 0.0324 + 0.4^2 * 0.0025 + 2 * 0.6 * 0.4 * (-0.0018))
        = sqrt(0.011664 + 0.0004 - 0.000864)
        = sqrt(0.0112)
        = 10.58%

VaR_95% = $1,000,000 * 1.645 * 0.1058 = $174,090
```

The Monte Carlo result should converge to approximately this value for a multivariate normal assumption.

### Example 3: Expected Shortfall
**Given:** From the Monte Carlo simulation above, the losses exceeding VaR (the worst 500 out of 10,000 scenarios) have an average loss of $225,000.

**Calculate:** 95% CVaR.

**Solution:**

```
CVaR_95% = $225,000
```

Interpretation: When losses exceed the 95% VaR threshold, the average loss is $225,000. This is roughly 29% worse than the $174,090 VaR figure, highlighting the severity of tail events.

## Common Pitfalls
- **VaR says nothing about tail shape:** VaR only identifies a threshold. Two portfolios with identical VaR can have vastly different tail losses. Always compute CVaR alongside VaR to understand tail severity.
- **Parametric VaR assumes normality:** Financial returns exhibit fat tails and skewness. Parametric VaR systematically underestimates tail risk. Use Monte Carlo with fat-tailed distributions or historical simulation for more realistic estimates.
- **Correlation breakdown in crises:** Correlations spike toward 1.0 during market stress, precisely when diversification is most needed. Stress tests should use crisis-period correlations, not calm-period correlations.
- **Using too short a lookback for covariance estimation:** Too short a window is noisy; too long a window includes stale data from different market regimes. A common compromise is 1-3 years of daily data, or use EWMA-weighted covariances.
- **Not distinguishing between absolute VaR and relative VaR:** Absolute VaR includes expected return (VaR = -mu + z*sigma); relative VaR excludes it (VaR = z*sigma). For short horizons (1-10 days), the expected return is negligible and the distinction is minor. For longer horizons, it matters.
- **Square-root-of-time scaling limitations:** VaR_h = VaR_1 * sqrt(h) assumes i.i.d. returns. With serial correlation or volatility clustering, this scaling is inaccurate.

## Cross-References
- **historical-risk** (wealth-management plugin): Historical VaR and realized volatility serve as non-parametric alternatives and calibration benchmarks for the forward-looking models in this skill.
- **performance-metrics** (wealth-management plugin): VaR and CVaR can be used as risk denominators in modified risk-adjusted ratios (e.g., return/CVaR).
- **volatility-modeling** (wealth-management plugin): EWMA and GARCH volatility forecasts provide the volatility inputs (sigma) for parametric and Monte Carlo VaR.

## Running the Script

```bash
uv run scripts/forward_risk.py            # run the demo (uses PEP 723 inline deps)
uv run scripts/forward_risk.py --verify   # check demo outputs against the worked examples (exit 1 on mismatch)
python3 scripts/forward_risk.py            # alternative (requires: pip install numpy scipy)
```

The demo prints the calculations covered above; its values match the worked examples in this skill. Run `--help` for a list of the classes and functions. For programmatic use, import the module rather than running it — the demo only executes under `python forward_risk.py`.


---

## SKILL: futures-position-sizer

- Fuente: `tradermonty/claude-trading-skills` → `skills/futures-position-sizer` (MIT)
- Cuándo usarla: Calculate contract-based futures position sizes from a direction, entry, and stop-loss, using verified per-symbol contract specs (multiplier, tick size, tick value). Use when the user asks how many futures contracts to trade, wants to size a futures position (ES, NQ, ZB, GC, CL, 6E/E6, VX, BT, ...), or is handing off a contrarian-setup-gate READY_FOR_PLAN direction/invalidation_level for sizing. Pure, offline calculation -- no API keys, no network.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/futures-position-sizer/` (requirements.txt, futures_position_sizer.py, futures_sizing.py)

# Futures Position Sizer

## Overview

Shapiro pipeline step 4: convert a direction, entry price, and stop-loss into a contract count, given an account risk budget and a verified contract spec (multiplier, tick size, tick value). This is a NEW, separate skill from `position-sizer` -- futures contracts are leveraged, multiplier-based instruments with wildly different dollar-per-point values (a $0.25 move is $12.50 on ES but $5.00 on NQ and $31.25 on ZB); reusing the equity share-count sizer for futures would silently produce wrong position sizes.

Two ways to size a trade:

- **Mode A (explicit)**: supply `--symbol --direction --entry --stop` directly.
- **Mode B (gate handoff)**: supply `--gate-json <contrarian-setup-gate report> --entry`. Direction and stop (the gate's `invalidation_level`) come from the gate's `READY_FOR_PLAN` report -- the sizer never sizes a setup the gate has not confirmed as READY, and never accepts an explicit `--direction`/`--stop` alongside `--gate-json` (the gate is authoritative when provided).

`--entry` is ALWAYS required, in both modes -- neither this skill nor the gate ever derives an entry price; the operator supplies it.

## When to Use

- After `contrarian-setup-gate` reaches `READY_FOR_PLAN` and you need a contract count for the confirmed direction and stop
- User asks "how many ES/NQ/GC/CL/... contracts should I trade?"
- User has a futures trade idea with a known entry and stop and wants risk-based sizing
- User wants to check the verified contract spec (multiplier/tick size/tick value) for a symbol before sizing (`--list-specs`)

## Prerequisites

- Python 3.9+, standard library only -- no API keys, fully offline
- A direction, entry, and stop (mode A), or a `contrarian-setup-gate` JSON report with `setup_status: READY_FOR_PLAN` (mode B)
- For a symbol outside the verified 23-market core table: its multiplier, tick size, and quote currency (all three, together)

## Workflow

### Step 1: Size the Position

**Mode A -- explicit:**

```bash
python3 skills/futures-position-sizer/scripts/futures_position_sizer.py \
  --symbol ES --direction LONG --entry 5000.25 --stop 4980.00 \
  --account-size 100000 --risk-pct 1.0 \
  --output-dir reports/ --format both
```

**Mode B -- gate handoff:**

```bash
python3 skills/futures-position-sizer/scripts/futures_position_sizer.py \
  --gate-json reports/contrarian_setup_gate_B6_2026-07-15.json \
  --entry 1.3400 \
  --account-size 100000 --risk-pct 1.0 \
  --output-dir reports/ --format both
```

`--symbol` may be omitted in mode B -- it is taken from the gate report. If both are given, they must match (`gate_symbol_mismatch` otherwise). `--direction`/`--stop` are rejected alongside `--gate-json` (usage error, exit 2) -- pass one mode or the other, never both.

### Step 2: Read the Result

| `sizing_status` | Meaning |
|---|---|
| `SIZED` | `contracts` >= 1; `total_risk_usd`/`risk_pct_of_account` are the actual risk taken |
| `NO_TRADE` | Never a crash -- always carries `no_trade_reason`. See the reason glossary below |

A `NO_TRADE` result from `risk_below_one_contract` still reports the full risk math (risk per contract, risk budget, stop distance) -- the account simply cannot afford one contract at this risk percentage and stop distance. Consider a smaller contract (e.g. a micro), deliberately reassess the risk percentage within your existing risk policy, or skip the trade. Keep the stop at the setup-defined invalidation level: widening it increases risk per contract and makes affordability worse; do not tighten it merely to fit the budget.

For a smaller contract, use its own symbol and verified specifications; if it is outside the core table, supply `--multiplier`, `--tick-size`, and `--contract-currency` together (plus `--fx-rate` for non-USD quotes). Do not lower an existing symbol's multiplier to simulate a micro. In mode B, use a `READY_FOR_PLAN` gate for that same smaller-contract symbol; do not relabel the original gate to bypass the symbol check.

### Step 3: Check Warnings

`warnings` (top-level list) never blocks sizing -- it flags audit-worthy conditions: `risk_pct_above_2` (risk above the 2% guideline), `off_tick_grid_entry`/`off_tick_grid_stop` (a non-bond symbol's price is not exactly on the tick grid -- legitimate for a mid-quote, but worth a second look).

### Step 4: Inspect the Verified Contract Spec Table

```bash
python3 skills/futures-position-sizer/scripts/futures_position_sizer.py --list-specs
```

Prints the full 23-market core table (multiplier, tick size, tick value, currency, exchange) sourced from official exchange contract-spec pages -- see `references/futures-contract-specs.md` for the per-row source URLs and verification dates.

## Worked Example: Bond Off-Grid Guard (32nds -> Decimal)

Bond/note futures (ZT, ZF, ZN, ZB) quote in fractions of a point (32nds, or 32nds-of-32nds), commonly written with an apostrophe: `110'16` means `110 + 16/32 = 110.50`. Typing `110.16` instead -- reading the digits after the apostrophe as if they were decimal cents -- is a classic, silent, wrong-money-math mistake: `110.16` is not on the ZB tick grid (`0.03125` = 1/32) at all.

```bash
# WRONG -- 110.16 is not on the 1/32 grid; this is almost certainly a
# mistyped "110'16" (which means 110.50). Exits 2, no report written:
python3 skills/futures-position-sizer/scripts/futures_position_sizer.py \
  --symbol ZB --direction LONG --entry 110.16 --stop 108.00 \
  --account-size 100000 --risk-pct 1.0

# CORRECT -- decimal points, not the raw 32nds digits:
python3 skills/futures-position-sizer/scripts/futures_position_sizer.py \
  --symbol ZB --direction LONG --entry 110.50 --stop 108.00 \
  --account-size 100000 --risk-pct 1.0
```

Every other symbol in the table quotes in plain decimal points -- an off-grid price there (a mid-quote, for instance) is only a soft `off_tick_grid_*` warning, never a rejection.

## Output Contract

Writes `futures_position_size_<SYMBOL>_<as-of>.json` to `--output-dir` when `--format json|both`; `--format text|both` prints a formatted summary to stdout. `--as-of` defaults to today (this is an operator-time sizing tool, not a backtest tool).

```yaml
schema_version: "1.0"
symbol: ES
direction: LONG
sizing_status: SIZED | NO_TRADE
no_trade_reason: null | risk_below_one_contract | gate_not_ready | gate_symbol_mismatch | ...
entry: 5000.25
stop: 4980.00
stop_distance_points: 20.25
stop_distance_ticks: 81
contract_spec: {multiplier: 50, tick_size: 0.25, tick_value: 12.5, currency: USD, source: cme, verified: "2026-07-17"}
risk_per_contract_usd: 1012.50
risk_budget_usd: 2000.00
contracts: 1
total_risk_usd: 1012.50
risk_pct_of_account: 1.01
max_contracts_cap_applied: false
fx_rate_used: 1.0
margin_note: "Exchange margin requirements are broker/time-dependent and NOT computed here; verify initial/maintenance margin with your broker."
gate: {report_path, setup_status, gate_confidence, warnings}   # mode B only
warnings: []
run_context: {symbol, as_of, schema_version, skill}
```

## Guardrails

1. **Never sizes a position without an explicit stop.** `--stop` is required in mode A; mode B refuses to size (`gate_not_ready`) until the gate itself reports `READY_FOR_PLAN` with a valid `invalidation_level`.
2. **Floor, never round up -- exact by construction, no epsilon.** `contracts = floor(risk_budget / risk_per_contract)` is computed with exact rational arithmetic (Python's `Fraction`, not float division), so `contracts * risk_per_contract <= risk_budget` holds by construction -- no epsilon nudge, no float-representation edge case, and no risk of ever exceeding the budget. Also rejected outright if the resulting count is economically implausible (an absurd input like a denormal-scale multiplier override). Zero contracts is a legitimate, fail-closed `NO_TRADE` outcome, not an error.
3. **Two fail-closed classes, matched to who supplied the bad value.** An operator-caused problem (an explicit `--stop` on the wrong side of `--entry`, a stop closer than one tick, a bond price typed off the tick grid) is a usage error: exit 2, no report written. The identical class of problem on a value that came from the untrusted gate-report file (mode B's stop) is instead a fail-closed `NO_TRADE` result: exit 0, a report IS written, naming the reason -- this never crashes on a bad or not-yet-ready gate file, matching every other skill in this pipeline.
4. **Bond-family off-grid prices are a hard rejection, not a warning.** ZT/ZF/ZN/ZB quote in 32nds/64ths notation; a price that doesn't land on the tick grid is almost certainly a notation mistype and would silently produce wrong money math if sized. Every other symbol only warns.
5. **Margin is never computed.** `margin_note` is a static, never-stale reminder -- margin requirements are broker- and time-dependent; this skill does not estimate them.
6. **Currency-aware.** Every core-table symbol is USD-quoted (confirmed by a table-wide unit test), including the CME FX futures whose contract SIZE is denominated in a foreign currency (e.g. B6's GBP 62,500) but which trade and settle in USD. A symbol quoted in a non-USD currency (via `--contract-currency` override) requires an explicit `--fx-rate` -- there is no silent default.
7. **Not investment advice.** This skill performs risk-based arithmetic on operator-supplied or gate-confirmed inputs; it does not recommend a trade, a direction, or an entry.

## Resources

- `scripts/futures_position_sizer.py` -- CLI: argument parsing, hardened gate-json loading (unreadable / parse_error incl. RecursionError / non_finite via an iterative whole-file scan), report generation
- `scripts/futures_sizing.py` -- Pure sizing core: numeric validators, the verified 23-market contract-spec table, risk math, the floor algorithm, tick-grid guards, and gate-report shape normalization
- `references/futures-contract-specs.md` -- The verified contract-spec table with per-row official source URLs and verification dates
- `references/sizing-methodology.md` -- Formulas, the exact-rational floor algorithm's rationale, the fail-closed exit-code convention, and worked examples (ES long, B6 short via gate handoff)

### Referencia: references/futures-contract-specs.md

# Futures Contract Specifications (Verified)

The 23-market core table `CONTRACT_SPECS` in `scripts/futures_sizing.py`, sourced from the
official exchange contract-spec pages and rulebook chapters (CME Group, Cboe, ICE) --
never blogs, aggregator sites, or secondary sources. Every row is verified independently
against its own `source_url`. A table-wide unit test asserts `tick_value == multiplier x
tick_size` (within 1e-9 relative) for every row -- this catches a transcription error
mechanically -- and three literal spot-checks (ES, GC, ZB) are pinned independently of the
table itself, so a bad edit to `CONTRACT_SPECS` would still fail even though it might
satisfy the internal-consistency invariant.

**Currency column = QUOTE currency, not underlying.** All 23 rows are USD-quoted (a
table-wide unit test asserts this). The CME FX futures (E6/J6/B6/A6/D6/S6) and ICE's DX
have non-USD contract SIZES -- e.g. B6's contract size is GBP 62,500 -- but they trade
and settle in USD. Mislabeling the currency column as the underlying would trigger a
spurious `missing_fx_rate` error or a double currency conversion.

**Outright tick, not spread tick.** SI, NG, and VX each have a finer minimum price
increment that applies only to spread/straddle trades, TAS Block/ECRP order types, or
inter-commodity spreads -- never to a single-leg position. Since this skill sizes a
single-leg stop-loss, every row below uses the OUTRIGHT tick (documented per-row where
a spread tick also exists).

## Table

| Symbol | Product | Multiplier | Tick Size | Tick Value | Currency | Exchange | Source | Verified |
|---|---|---|---|---|---|---|---|---|
| ES | E-mini S&P 500 Index futures | 50 | 0.25 | $12.50 | USD | CME | [Rulebook Ch.358](https://www.cmegroup.com/rulebook/CME/IV/350/358/358.pdf) | 2026-07-17 |
| NQ | E-mini Nasdaq-100 Index futures | 20 | 0.25 | $5.00 | USD | CME | [Rulebook Ch.359](https://www.cmegroup.com/rulebook/CME/IV/350/359/359.pdf) | 2026-07-17 |
| YM | E-mini Dow Jones Industrial Average ($5) Index futures | 5 | 1.00 | $5.00 | USD | CBOT | [Rulebook Ch.27](https://www.cmegroup.com/rulebook/CBOT/III/27.pdf) | 2026-07-17 |
| QR | E-mini Russell 2000 Index futures (Globex ticker RTY) | 50 | 0.10 | $5.00 | USD | CME | [Rulebook Ch.393](https://www.cmegroup.com/rulebook/CME/III/300/393.pdf) | 2026-07-17 |
| VX | Cboe Volatility Index (VIX) futures | 1000 | 0.05 (outright) | $50.00 | USD | CFE | [Cboe VIX Futures Specs](https://www.cboe.com/tradable-products/vix/vix-futures/specifications/) | 2026-07-17 |
| ZT | 2-Year U.S. Treasury Note futures | 2000 | 0.00390625 (1/8-of-1/32) | $7.8125 | USD | CBOT | [Rulebook Ch.21](https://www.cmegroup.com/rulebook/CBOT/II/21.pdf) | 2026-07-17 |
| ZF | 5-Year U.S. Treasury Note futures | 1000 | 0.0078125 (1/4-of-1/32) | $7.8125 | USD | CBOT | [Rulebook Ch.20](https://www.cmegroup.com/rulebook/CBOT/II/20.pdf) | 2026-07-17 |
| ZN | 10-Year U.S. Treasury Note futures | 1000 | 0.015625 (1/2-of-1/32, i.e. 1/64) | $15.625 | USD | CBOT | [Rulebook Ch.19](https://www.cmegroup.com/rulebook/CBOT/II/19.pdf) | 2026-07-17 |
| ZB | 30-Year U.S. Treasury Bond futures | 1000 | 0.03125 (1/32) | $31.25 | USD | CBOT | [Rulebook Ch.18](https://www.cmegroup.com/rulebook/CBOT/V/18/18.pdf) | 2026-07-17 |
| DX | ICE U.S. Dollar Index futures | 1000 | 0.005 | $5.00 | USD | ICE | [ICE Product Specs](https://www.ice.com/products/194/specs) | 2026-07-17 |
| E6 | Euro FX futures (CME ticker 6E) | 125,000 | 0.00005 | $6.25 | USD | CME | [CME Euro FX Specs](https://www.cmegroup.com/markets/fx/g10/euro-fx.contractSpecs.html) | 2026-07-17 |
| J6 | Japanese Yen futures (CME ticker 6J) | 12,500,000 | 0.0000005 | $6.25 | USD | CME | [CME Japanese Yen Specs](https://www.cmegroup.com/markets/fx/g10/japanese-yen.contractSpecs.html) | 2026-07-17 |
| B6 | British Pound futures (CME ticker 6B) | 62,500 | 0.0001 | $6.25 | USD | CME | [CME British Pound Specs](https://www.cmegroup.com/markets/fx/g10/british-pound.contractSpecs.html) | 2026-07-17 |
| A6 | Australian Dollar futures (CME ticker 6A) | 100,000 | 0.00005 | $5.00 | USD | CME | [CME Australian Dollar Specs](https://www.cmegroup.com/markets/fx/g10/australian-dollar.contractSpecs.html) | 2026-07-17 |
| D6 | Canadian Dollar futures (CME ticker 6C) | 100,000 | 0.00005 | $5.00 | USD | CME | [CME Canadian Dollar Specs](https://www.cmegroup.com/markets/fx/g10/canadian-dollar.contractSpecs.html) | 2026-07-17 |
| S6 | Swiss Franc futures (CME ticker 6S) | 125,000 | 0.00005 | $6.25 | USD | CME | [CME Swiss Franc Specs](https://www.cmegroup.com/markets/fx/g10/swiss-franc.contractSpecs.html) | 2026-07-17 |
| GC | Gold futures | 100 | 0.10 | $10.00 | USD | COMEX | [CME Gold Specs](https://www.cmegroup.com/markets/metals/precious/gold.contractSpecs.html) | 2026-07-17 |
| SI | Silver futures | 5,000 | 0.005 (outright) | $25.00 | USD | COMEX | [CME Silver Specs](https://www.cmegroup.com/markets/metals/precious/silver.contractSpecs.html) | 2026-07-17 |
| HG | Copper futures | 25,000 | 0.0005 | $12.50 | USD | COMEX | [CME Copper Specs](https://www.cmegroup.com/markets/metals/base/copper.contractSpecs.html) | 2026-07-17 |
| PL | Platinum futures | 50 | 0.10 | $5.00 | USD | NYMEX | [CME Platinum Specs](https://www.cmegroup.com/markets/metals/precious/platinum.contractSpecs.html) | 2026-07-17 |
| CL | WTI Crude Oil futures | 1,000 | 0.01 | $10.00 | USD | NYMEX | [CME WTI Crude Specs](https://www.cmegroup.com/markets/energy/crude-oil/light-sweet-crude.contractSpecs.html) | 2026-07-17 |
| NG | Henry Hub Natural Gas futures | 10,000 | 0.001 (outright) | $10.00 | USD | NYMEX | [CME Natural Gas Specs](https://www.cmegroup.com/markets/energy/natural-gas/natural-gas.contractSpecs.html) | 2026-07-17 |
| BT | Bitcoin futures (CME ticker BTC) | 5 | 5.00 | $25.00 | USD | CME | [Rulebook Ch.350](https://www.cmegroup.com/rulebook/CME/IV/350/350.pdf) | 2026-07-17 |

## Notable Rows

### QR = E-mini Russell 2000 (Globex ticker RTY), not the discontinued ICE product

"QR" is not a commonly known ticker. Resolved by pulling live 2026 FMP COT data for
symbol QR directly (the raw CFTC fields, not FMP's own label): every recent weekly
report shows `marketAndExchangeNames="RUSSELL E-MINI - CHICAGO MERCANTILE EXCHANGE"`,
`cftcContractMarketCode="239742"`, `cftcMarketCode="CME"`,
`contractUnits="(RUSSELL 2000 INDEX X $50)"`, with roughly 400K open interest --
i.e. an actively-traded contract. Cross-confirmed against CME Rulebook Chapter 393:
"$50.00 times the Russell 2000 Index... minimum price increment of 0.10 Index points,
equal to $5.00 per contract." This is CME's current E-mini Russell 2000 (Globex ticker
RTY today), NOT the discontinued ICE "Russell 2000 Mini" (legacy ticker TF, a $100
multiplier, delisted around 2017 when the Russell index license moved back to CME) --
using the ICE product's multiplier would double the correct risk-per-contract figure.

### ZT's tick: resolved as 1/8-of-1/32, not 1/4-of-1/32

ZT's minimum price increment is disputed among third-party aggregator sites. Resolved
here ONLY against CME Group's own Rulebook Chapter 21, which states verbatim:
"The minimum price fluctuation shall be one-eighth of one thirty-second of one point
(equal to $7.8125 per contract), including intermonth spreads." That is
1/8 x 1/32 = 1/256 = 0.00390625 points on a $200,000 face-value contract (2-year and
3-year Treasury futures are the only CBOT products with $200,000 par instead of
$100,000) -> $2,000/point x 0.00390625 = $7.8125. This is a DIFFERENT fraction from
ZF's 1/4-of-1/32 -- the two land on the same $7.8125 dollar tick only because ZT's par
value is 2x ZF's while its fraction is half as fine, which is likely the source of the
aggregator confusion.

### A6/D6/S6: CME halved the minimum price increment between 2016 and 2022

CME reduced the outright minimum price increment (MPI) on these three FX futures from
0.0001 to 0.00005 in three separate, dated changes:

- **A6 (6A):** 0.0001 ($10.00/tick) -> 0.00005 ($5.00/tick), effective November 23, 2020
  (CME Product Modification Summary Chadv20-353).
- **S6 (6S):** 0.0001 ($12.50/tick) -> 0.00005 ($6.25/tick), effective May 2022
  (CME notice SER-8936).
- **D6 (6C):** 0.0001 ($10.00/tick) -> 0.00005 ($5.00/tick), effective July 11, 2016
  (`cmegroup.com/trading/fx/mpi.html`).

Confirmed by the per-symbol footnotes in CME's own "2023 FX Product Guide" (22nd
edition) and cross-checked against `cmegroup.com/trading/fx/mpi.html` (the MPI
change-history page). Many generic aggregator sites and default web-search snippets
still quote the stale, pre-reduction values -- an earlier provisional draft of this
table made exactly that mistake for all three rows.

### D6 = CME 6C (Canadian Dollar), not TBD

Confirmed via CME's 2023 FX Product Guide (CAD/USD futures page): Product Code 6C,
contract size 100,000 CAD, quoted USD per CAD -- matching the "D6" vendor-symbol
convention (D for "Dollar"/CAD, since a leading digit isn't a valid symbol character
for some data vendors) used by this project's COT-report symbol list.

### VX: outright tick vs. spread tick

Cboe's own specifications page states 0.05 index points ($50.00/contract) as the
standard/outright minimum price interval; a finer 0.01-point ($10.00) tick applies only
to the individual legs and net prices of SPREAD trades, and a still-finer 0.005-point
tick applies only to TAS Block Trades and Exchange-for-Related-Position (ECRP) order
types. This table uses 0.05/$50.00 -- the correct tick for sizing a single-leg outright
stop-loss; using the spread tick would understate risk by 5x.

### BT: CME's own ticker is "BTC", not "BT"; distinct from the Micro contract "MBT"

CME has no product literally ticked "BT". The standard-size, 5-BTC-per-contract, USD
cash-settled Bitcoin future is officially ticker **BTC** (Rulebook Chapter 350: "Each
futures contract shall be valued at 5 bitcoin... minimum price increment shall be
$5.00, equal to $25.00 per contract"). This is entirely distinct from CME's **Micro
Bitcoin futures, ticker MBT** (Rulebook Chapter 348), which is 0.1 BTC/contract -- 50x
smaller notional per contract. "BT" is this project's own COT/vendor-feed symbol
(matching `cot-contrarian-detector`'s `CORE_SYMBOLS` convention) and is mapped to
CME's BTC contract here, not MBT.

## Verification Method

Every row above was verified against the official exchange's own contract-spec or
rulebook page (`cmegroup.com`, `ice.com`, `cboe.com`) -- never a blog, aggregator site
(Barchart, TradingView, Investing.com, Wikipedia), or other secondary source. Where
CME's live `contractSpecs.html` marketing pages were unreachable via automated fetch
(client-side JS rendering / bot-detection blocking direct scraping), verification fell
back to CME's own official static PDF rulebook chapters (the legally authoritative
contract text, arguably more authoritative than the marketing page) or a
Wayback-Machine-mirrored snapshot of CME's own official PDF/HTML bytes -- both are
still the exchange's own primary-source content, not a third party's restatement of
it. Every `tick_value` was independently arithmetic-checked
(`multiplier x tick_size`) against what the source states as the per-contract dollar
figure, with zero discrepancies across all 23 rows.

### Referencia: references/sizing-methodology.md

# Futures Position Sizing Methodology

## Why a Separate Skill from `position-sizer`

`position-sizer` computes a SHARE count for long equity trades: `shares = floor(dollar_risk / (entry - stop))`, where one share's dollar risk is simply its own price move. Futures contracts are different in a way that makes that formula silently wrong if reused as-is: every contract has a **multiplier** that converts a one-point price move into a dollar amount, and that multiplier varies by roughly two orders of magnitude across symbols in the same table -- a 0.25-point move is $12.50 on ES (multiplier 50) but $5.00 on NQ (multiplier 20) and $31.25 on ZB (multiplier 1000, tick 1/32). Feeding a futures entry/stop into the equity sizer would compute a "share" count using the raw point difference as if it were a dollar difference, understating or overstating real risk by 20-1000x depending on the symbol. This skill exists specifically to apply the correct multiplier, tick size, and (for FX/international contracts) currency conversion before any risk arithmetic happens.

## Core Formula

```
stop_distance       = |entry - stop|                          (price points)
risk_per_contract   = stop_distance * multiplier * fx_rate     (USD)
risk_budget         = account_size * risk_pct / 100            (USD)
contracts            = floor(risk_budget / risk_per_contract)   (never rounds up)
total_risk           = contracts * risk_per_contract            (USD, when SIZED)
```

`fx_rate` converts a non-USD-quoted contract's risk into USD; it is `1.0` for every symbol in the verified core table (all 23 are USD-quoted -- see `futures-contract-specs.md`) and is required, with no default, for any operator-supplied override symbol quoted in another currency.

## The Floor Algorithm (Exact Rational Arithmetic -- No Epsilon)

```python
from fractions import Fraction
q = Fraction(risk_budget) / Fraction(risk_per_contract)
contracts = math.floor(q)
```

`Fraction(finite_float)` converts a float64 to the *exact* rational number it represents -- every float64 is a dyadic rational (an exact fraction with a power-of-2 denominator), so this conversion loses nothing. The division and floor that follow are then exact rational operations: `contracts * risk_per_contract <= risk_budget` holds *by construction*, with no epsilon, no iteration, and no float-representation edge case of any kind.

This design replaced two earlier float-heuristic attempts, both of which were bugs caught by independent user review across two rounds:

1. **A relative epsilon** (`math.floor(q * (1 + 1e-9))`, an early plan-review addition meant to recover a contract lost to float64 under-counting at an exact `k * risk_per_contract` boundary). A relative nudge's *absolute* size grows with `q`, and at large scale (`q ~ 1e8`, a big account against a cheap contract) a `1e-9`-relative nudge was already large enough (~0.1 in absolute terms) to swallow a *genuine* fractional shortfall and round the contract count UP past the actual risk budget -- the reported repro was `q = 99999999.95` (a true 0.05-contract shortfall) rounding to `100,000,000` contracts, $50 over budget, still `SIZED`.
2. **An absolute epsilon plus a hard post-condition loop** (`contracts = floor(q + 1e-9)`, then `while contracts * risk_per_contract > risk_budget: contracts -= 1` to walk any over-count back down). This fixed the rounding-up defect, but a *second* independent re-review found it could not terminate in practice at large scale: once `contracts` is large enough (the reported repro reached roughly `2.4e285`), float64 can no longer represent the difference between `contracts` and `contracts - 1` when each is multiplied by `risk_per_contract` -- `(contracts - 1) * risk_per_contract` and `contracts * risk_per_contract` become bit-for-bit identical -- so the loop's exit condition never becomes true and it decrements toward zero one candidate contract at a time. Not an infinite loop in the mathematical sense, but computationally indistinguishable from a hang.

Both defects came from trying to patch float64's inherent imprecision with more float64 heuristics. The fix is to stop doing float arithmetic for this comparison at all -- `Fraction` sidesteps the entire problem class rather than adding another layer meant to compensate for it.

**A consequence worth knowing:** this design is money-safe in a way that can look surprising at a glance. Take `risk_per_contract = 0.1 * 3 = 0.30000000000000004` (slightly *above* the mathematical 0.3) against a budget of exactly `0.9`: `3 * risk_per_contract = 0.9000000000000001`, which *exceeds* the 0.9 budget in float64 terms. Three contracts would cost more than the budget allows; the exact-rational floor correctly returns `2`, not `3` -- even though "3 times risk-per-contract is about 0.9" looks intuitively fine at a glance. This is the same "never round up" guarantee working correctly at a scale where naive intuition (and the old epsilon-based designs) got it wrong.

**Sanity cap on the result.** The exact-rational floor can no longer hang on an absurd input (e.g. a denormal-scale `--multiplier` override combined with a large `--account-size`), but it can still return a technically correct, economically meaningless answer -- the hang repro above computes an exact contract count with hundreds of digits. `CONTRACTS_SANITY_MAX` (1e12, four orders of magnitude above the largest legitimate case this skill's own tests exercise, ~1e8) rejects anything above it outright as `contracts_implausibly_large`, turning nonsense input into a clean `ConfigError` instead of a nonsensical `SIZED` report.

The tick-grid check (`is_on_tick_grid`) and the minimum-stop-distance guard (`meets_min_stop_distance`) are unrelated to this and keep their own *relative* float epsilon (unchanged) -- that construction is still correct for them, since tick sizes span multiple orders of magnitude across symbols and a ratio-based (not budget-based) comparison is what they're doing; the float-epsilon defects above were specific to the contract-count floor, where the "risk_budget / risk_per_contract" quotient's own scale set the failure mode.

**Minimum-stop-distance guard.** If the entry/stop distance is less than one tick, sizing is refused rather than silently computing an ultra-high, effectively meaningless contract count from a near-zero `risk_per_contract`. This closes the regime where `risk_per_contract` itself would be vanishingly small and even a tiny risk budget would imply an enormous (and nonsensical) contract count -- now doubly guarded by `CONTRACTS_SANITY_MAX` as well.

## Two Fail-Closed Classes: ConfigError vs. NO_TRADE

Every validation failure in this skill resolves to one of two outcomes, and which one depends on **who supplied the offending value** -- not on which rule was violated:

| Violation | Operator-supplied value (mode A `--stop`, or entry in either mode) | Gate-supplied value (mode B `--stop` = gate's `invalidation_level`) |
|---|---|---|
| Geometry (LONG stop >= entry, or SHORT stop <= entry) | `ConfigError` "direction_stop_mismatch" -- exit 2, no report | `NO_TRADE` "entry_on_wrong_side_of_stop" -- exit 0, report written |
| Stop closer than one tick | `ConfigError` "stop_too_close" -- exit 2 | `NO_TRADE` "gate_stop_too_close" -- exit 0 |
| Bond-family (ZT/ZF/ZN/ZB) off tick grid | `ConfigError` "entry_off_tick_grid" / "stop_off_tick_grid" -- exit 2 | `NO_TRADE` "gate_stop_off_tick_grid" -- exit 0 (entry is always operator-supplied, so an off-grid ENTRY is always a ConfigError even in mode B) |

This mirrors `contrarian-setup-gate`'s own convention for untrusted-file handling: a CLI usage mistake is the operator's problem (loud failure, no report, exit 2); a problem discovered inside an untrusted input FILE is never allowed to crash the tool -- it always produces a report naming exactly why sizing was refused (exit 0). Blaming the CLI invocation for a bad value that actually came from the gate's JSON file would be misleading, and would break the "every run either sizes or explains why not" contract every skill in this pipeline follows.

`risk_below_one_contract` (the risk budget can't afford even one contract at this stop distance) is **not** in this two-class table -- it is always `NO_TRADE`, in both modes, because it isn't anyone's mistake. It is the correct, expected output of risk-based sizing when the numbers simply don't support a position; consider a smaller contract (e.g. a micro), deliberately reassess `--risk-pct` within your existing risk policy, or accept no trade. Preserve the setup-defined invalidation level: widening the stop increases `risk_per_contract` and makes affordability worse, and tightening it merely to fit the budget changes the setup. The CLI's 10% ceiling is an input limit, not a recommended risk level.

A smaller contract requires its own symbol and verified contract specifications. For a symbol outside the core table, pass `--multiplier`, `--tick-size`, and `--contract-currency` together, plus `--fx-rate` for a non-USD quote. Never reduce a known symbol's multiplier to imitate a micro. In gate-handoff mode, obtain a `READY_FOR_PLAN` gate for the smaller-contract symbol; do not relabel an existing gate or bypass the symbol match.

## Bond/Note Off-Grid Guard: Why It's Hard, Not Soft

ZT (2-Year), ZF (5-Year), ZN (10-Year), and ZB (30-Year) Treasury futures are the only fractional-notation family among the 23 core symbols -- they quote in 32nds (or, for ZN, 64ths; for ZF, quarter-32nds) of a point, conventionally written with an apostrophe: `110'16` means `110 + 16/32 = 110.50`. Every other symbol in the table quotes in plain decimal points.

The trap: an operator who mentally reads `110'16` and types `110.16` into `--entry` has entered a price that is **not on the tick grid at all** (`110.16 / 0.03125` is nowhere near an integer), and would have the sizer compute a stop distance using a price roughly 34 cents away from the intended one -- a small-looking but real, silent, wrong-money-math error. Every other symbol's off-grid price is legitimate (a mid-quote, an odd fill price) and only produces a warning; the bond family's off-grid price is treated as almost certainly a notation mistake and is a hard, fail-closed rejection instead, with a message that spells out the 32nds-to-decimal conversion.

## Worked Examples

### ES, LONG, explicit mode

```
entry = 5000.25, stop = 4980.00, multiplier = 50, tick_size = 0.25
stop_distance = 20.25 points = 81 ticks
risk_per_contract = 20.25 * 50 = $1,012.50
account_size = 100,000, risk_pct = 2.0% -> risk_budget = $2,000.00
contracts = floor(2000.00 / 1012.50) = floor(1.975...) = 1
total_risk = 1 * 1012.50 = $1,012.50 (1.01% of account)
```

At `risk_pct = 1.0%` instead, `risk_budget = $1,000.00 < risk_per_contract`, so `contracts = 0` -- `sizing_status: NO_TRADE`, `no_trade_reason: risk_below_one_contract`. The risk math (stop distance, risk per contract, risk budget) is still reported in full; only the trade itself is refused.

### B6, SHORT, gate handoff

A `contrarian-setup-gate` report for B6 reaches `READY_FOR_PLAN` with `direction: SHORT` and `invalidation_level: 1.3450` (the gate's stop reference). The operator supplies only the entry:

```bash
python3 skills/futures-position-sizer/scripts/futures_position_sizer.py \
  --gate-json reports/contrarian_setup_gate_B6_2026-07-15.json \
  --entry 1.3400 --account-size 100000 --risk-pct 1.0 \
  --output-dir reports/ --format both
```

B6 (British Pound, contract size GBP 62,500) is USD-quoted, so no `--fx-rate` is needed. `direction` and `stop` come entirely from the gate file; if `1.3400` (SHORT entry) were on the wrong side of `1.3450` (stop) -- i.e. the entry were above the stop for a SHORT -- the result would be `NO_TRADE` with reason `entry_on_wrong_side_of_stop`, exit 0, not a crash.

## Risk-Percentage Guardrails

`--risk-pct` accepts `(0, 10]`; values above `10` are an argparse-level usage error (no override). A value above `2.0` produces the `risk_pct_above_2` warning (never a rejection) -- consistent with `position-sizer`'s own 1-2% guideline for a single trade's risk. Futures leverage means the SAME percentage risk moves faster in dollar terms than an unlevered equity position of the same nominal size; this warning is a deliberately low bar.

## Margin Is Never Computed

The `margin_note` field is always the same static reminder text, never a computed number. Exchange initial/maintenance margin requirements are broker-specific and change with volatility regimes, sometimes intraday during stress -- a computed "margin estimate" would either be wrong the moment it's stale, or would require live broker data this skill deliberately does not fetch (fully offline, no API keys, no network). The issue that motivated this skill (#242) asked for a "margin estimate note"; this skill reads that as "a note ABOUT margin" (honest, never-stale) rather than "a computed estimate presented as a note" (which would rot). This interpretation was flagged explicitly for review rather than decided silently -- see the PR description.


---

## SKILL: gifts-and-entertainment

- Fuente: `SYasJ/claude-business-skills` → `plugins/risk/skills/gifts-and-entertainment` (MIT)
- Cuándo usarla: Apply a gifts and entertainment rule to a specific offer, and record the decision. Use when the user mentions gift policy, can we accept this, entertainment request, hospitality gift, or asks for a gift decision note. Risk and compliance skill by Yasir Jilani.

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'gifts-and-entertainment' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Gifts and Entertainment

Apply a gifts and entertainment rule to a specific offer, and record the decision.

## When to use this skill

Use this skill when the user:

- gift policy
- can we accept this
- entertainment request
- hospitality gift

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

- The offer and its value if known
- Who offered it
- The decision pending with that party
- Their policy

## Workflow


### 1. Step 1

State the offer, the giver, and whether a decision is pending with that party.
### 2. Step 2

Apply their policy thresholds. If they have no policy, recommend a decision from leadership rather than inventing a legal rule.
### 3. Step 3

A pending procurement or hiring decision raises the risk. Say so.
### 4. Step 4

Recommend accept, decline, or accept with disclosure, for their approver to confirm.
### 5. Step 5

Record it.
### 6. Step 6

Do not help disguise a gift as something else.

## Output

Deliver a **gift decision note**.

- Purpose of this gift decision note, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a gift decision note by 30 September 2026. A bidder offers tickets during an open RFP and the draft calls them a friendly dinner.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A bidder offers tickets during an open RFP and the draft calls them a friendly dinner.

The offer and its value if known: CAD 120, dates not set, cap not set
Who offered it: CAD 120, dates not set, cap not set
The decision pending with that party: A bidder offers tickets during an open RFP and the draft calls them a friendly dinner
Their policy: their one-page rule dated 2 Mar 2026. No exception log
```

### Example outcome

**Gift decision note**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Names the open RFP, refuses the disguise, and recommends decline or disclosure under their policy.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The offer and its value if known | CAD 120, dates not set, cap not set | Needs confirmation |
| Who offered it | CAD 120, dates not set, cap not set | Carried into the draft |
| The decision pending with that party | A bidder offers tickets during an open RFP and the draft calls them a friendly dinner | Carried into the draft |
| Their policy | their one-page rule dated 2 Mar 2026. No exception log | Needs confirmation |

**How this draft was built**

**1. State the offer, the giver, and whether a decision is pending with that party**

**2. Apply their policy thresholds. If they have no policy, recommend a decision from leadership rather than inventing a legal rule**

**3. A pending procurement or hiring decision raises the risk. Say so**

**4. Recommend accept, decline, or accept with disclosure, for their approver to confirm**

**5. Record it**

**Deliberately not done**
- Disguising a gift.
- Inventing a legal threshold.
- Accepting a gift during a live bid without flagging it.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Disguising a gift
- Inventing a legal threshold
- Accepting a gift during a live bid without flagging it

## Related skills

- `conflict-of-interest`
- `procurement-award-note`


---

## SKILL: historical-risk

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/historical-risk` (MIT)
- Cuándo usarla: Quantify realized risk from historical data using volatility estimators, drawdown analysis, and downside risk metrics. Use when the user asks about historical volatility, maximum drawdown, drawdown duration, historical VaR, downside deviation, semi-variance, or tracking error. Also trigger when users mention 'how risky has this been', 'worst decline', 'Parkinson estimator', 'Yang-Zhang', 'peak-to-trough loss', 'recovery time', 'annualized volatility', or ask how to measure past investment risk.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/wealth-management/skills/historical-risk/` (historical_risk.py)

# Historical Risk Analysis

## Core Concepts

### Close-to-Close Volatility
The simplest and most common volatility estimator. Compute the standard deviation of log returns and annualize.

```
sigma_annual = sigma_daily * sqrt(N)
```

where N = number of trading periods per year (typically 252 for daily, 52 for weekly, 12 for monthly).

Log returns are preferred: r_t = ln(P_t / P_{t-1}).

### Parkinson (High-Low) Estimator
Uses intraday high and low prices to capture intraday volatility that close-to-close misses. More efficient than close-to-close when the true process is continuous.

```
sigma^2_Park = (1 / (4 * n * ln(2))) * sum( ln(H_i / L_i)^2 )
```

This estimator is roughly 5x more efficient than close-to-close for a diffusion process, but is biased downward when there are jumps or when the range is discretized.

### Yang-Zhang Estimator
Combines overnight (close-to-open), open-to-close, and Rogers-Satchell components. It is unbiased for processes with both drift and opening jumps.

```
sigma^2_YZ = sigma^2_overnight + k * sigma^2_open-to-close + (1 - k) * sigma^2_RS
```

where k is chosen to minimize estimator variance:

```
k = 0.34 / (1.34 + (n + 1) / (n - 1))
```

with n the number of observations, and sigma^2_RS is the Rogers-Satchell estimator that uses all four OHLC prices within each period.

### Drawdown Analysis
Drawdown at time t measures the decline from the running peak:

```
DD_t = (Peak_t - Value_t) / Peak_t
```

where Peak_t = max(Value_s) for all s <= t.

- **Maximum Drawdown (MDD):** MDD = max(DD_t) over the evaluation period.
- **Drawdown Duration:** The number of periods from a peak until a new peak is reached.
- **Recovery Time:** The number of periods from the trough back to the prior peak level.

### Historical VaR
The non-parametric (empirical) Value-at-Risk is simply the alpha-percentile of the historical return distribution. No distributional assumptions are made.

```
VaR_alpha = -Percentile(R, alpha)
```

For example, 95% VaR uses the 5th percentile of returns. The negative sign is a convention so that VaR is expressed as a positive loss number.

### Downside Deviation
Measures dispersion of returns below a Minimum Acceptable Return (MAR):

```
sigma_d = sqrt( (1/n) * sum( min(R_i - MAR, 0)^2 ) )
```

Common choices for MAR: 0%, the risk-free rate, or the mean return.

### Tracking Error
Standard deviation of the difference between portfolio and benchmark returns, annualized:

```
TE = std(R_p - R_b) * sqrt(N)
```

This measures how consistently the portfolio tracks (or deviates from) its benchmark.

### Semi-Variance
Variance computed using only returns below the mean (or below a threshold):

```
SV = (1/n) * sum( min(R_i - mean(R), 0)^2 )
```

Semi-variance isolates downside risk and is the foundation for the Sortino ratio (see performance-metrics).

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Annualized Volatility | sigma_ann = sigma_period * sqrt(N) | Convert period vol to annual vol |
| Log Return | r_t = ln(P_t / P_{t-1}) | Compute continuously compounded returns |
| Parkinson Variance | sigma^2 = (1 / (4n ln2)) * sum(ln(H/L)^2) | Volatility from high-low data |
| Drawdown | DD_t = (Peak_t - Value_t) / Peak_t | Measure peak-to-trough decline |
| Max Drawdown | MDD = max(DD_t) | Worst historical decline |
| Historical VaR (95%) | 5th percentile of return series | Non-parametric loss estimate |
| Downside Deviation | sigma_d = sqrt((1/n) * sum(min(R_i - MAR, 0)^2)) | Asymmetric risk below MAR |
| Tracking Error | TE = std(R_p - R_b) * sqrt(N) | Portfolio vs benchmark deviation |
| Semi-Variance | (1/n) * sum(min(R_i - mean(R), 0)^2) | Below-mean variance |

## Worked Examples

### Example 1: Annualized Volatility from Daily Returns
**Given:** A stock has daily log returns with a sample standard deviation of 1.2%. Assume 252 trading days per year.

**Calculate:** Annualized volatility.

**Solution:**

```
sigma_annual = 0.012 * sqrt(252)
             = 0.012 * 15.875
             = 0.1905
             ~ 19.05%
```

The stock's annualized volatility is approximately 19%.

### Example 2: Maximum Drawdown from a Price Series
**Given:** A fund's NAV follows this path over six months: $120, $135, $150, $130, $105, $125.

**Calculate:** Maximum drawdown and identify the peak and trough.

**Solution:**

Running peaks: $120, $135, $150, $150, $150, $150.

Drawdowns at each point:
- $120: (120-120)/120 = 0%
- $135: (135-135)/135 = 0%
- $150: (150-150)/150 = 0%
- $130: (150-130)/150 = 13.3%
- $105: (150-105)/150 = 30.0%
- $125: (150-125)/150 = 16.7%

**Maximum Drawdown = 30.0%**, occurring from the peak of $150 to the trough of $105. As of the last observation ($125), the drawdown has not yet fully recovered.

### Example 3: Historical VaR
**Given:** 500 daily returns sorted from worst to best. The 25th-worst return is -2.8% and the 26th-worst is -2.6%.

**Calculate:** 95% 1-day historical VaR.

**Solution:**

The 5th percentile corresponds to the 25th observation out of 500 (500 * 0.05 = 25).

```
VaR_95% = -(-2.8%) = 2.8%
```

Interpretation: On 95% of days, the loss is expected not to exceed 2.8% based on the historical distribution.

## Common Pitfalls
- **Not annualizing volatility correctly:** Volatility scales with the square root of time (multiply by sqrt(N)), not linearly. Multiplying daily vol by 252 instead of sqrt(252) produces wildly inflated numbers.
- **Using calendar days vs trading days inconsistently:** Use 252 trading days (not 365 calendar days) for equity markets when annualizing. Bond markets and some international markets may differ.
- **Survivorship bias in historical data:** Data sets that exclude delisted or failed securities understate realized risk.
- **Lookback period sensitivity:** A 1-year lookback captures different risk regimes than a 5-year lookback. Always state the lookback window and consider whether it spans relevant market conditions.
- **Confusing VaR confidence level direction:** 95% VaR corresponds to the 5th percentile of returns (the loss tail). The "95%" refers to the confidence level, not the percentile of gains.
- **Log returns vs simple returns:** For volatility estimation, log returns are preferred because they are additive across time. For reporting cumulative performance, simple returns are more intuitive.

## Cross-References
- **performance-metrics** (wealth-management plugin): Uses volatility, downside deviation, tracking error, and max drawdown as denominators in risk-adjusted ratios (Sharpe, Sortino, Information Ratio, Calmar).
- **forward-risk** (wealth-management plugin): Historical VaR and historical volatility serve as inputs to forward-looking VaR models and stress tests.
- **volatility-modeling** (wealth-management plugin): EWMA and GARCH models extend the simple historical volatility estimators covered here into forecasting frameworks.
- **retirement-decumulation** (wealth-management plugin): drawdown and volatility history drives sequence-of-returns risk in withdrawal-phase portfolios
## Running the script
Run with `uv run scripts/historical_risk.py` (the PEP 723 header resolves numpy automatically) or with `python3 scripts/historical_risk.py` after `pip install numpy scipy`. A bare run prints a full risk analysis (annualized and Parkinson volatility, maximum drawdown with timing, 95%/99% historical VaR, downside deviation, semi-variance, tracking error, rolling volatility) on seeded synthetic data with an injected drawdown event. Use `--verify` to assert outputs match this skill's worked examples and the demo's expected values (exit code 0 on PASS) and `--help` for an overview of the class. The file is primarily meant to be imported as a module (e.g., `from historical_risk import HistoricalRiskAnalyzer`).


---

## SKILL: ib-portfolio

- Fuente: `staskh/trading_skills` → `.claude/skills/ib-portfolio` (MIT)
- Cuándo usarla: Get portfolio positions from Interactive Brokers. Use when user asks about their portfolio, positions, holdings, or what stocks they own. Requires TWS or IB Gateway running locally.
- Código: extraer `code/staskh_trading_skills.tar` y usar `.claude/skills/ib-portfolio/` (portfolio.py)

# IB Portfolio

Fetch current portfolio positions from Interactive Brokers.

## IB Connection

TWS or IB Gateway must be running locally with API enabled:
- **Paper trading** — port 7497
- **Live trading** — port 7496
- **`IB_PORT` env var** — default port when `--port` is omitted (e.g. `IB_PORT=4001` for a Gateway container). Precedence: `--port` flag > `IB_PORT` > built-in default. Set it in the shell or a `.env` file.

**Port fallback:** If the configured port fails, automatically retry on the other port.
If the retry succeeds, save to memory which account type worked (live/paper) and reuse it for all IB skill calls in this and future sessions — until the user explicitly asks for the other account.
If both ports fail, ask the user to verify that TWS or IB Gateway is running with API access enabled.

## Instructions

> **Note:** If `uv` is not installed or `pyproject.toml` is not found, replace `uv run python` with `python` in all commands below.

```bash
uv run python scripts/portfolio.py [--port PORT]
```

## Arguments

- `--port` - IB port (default: 7497 for paper trading)
- `--account` - Specific IB account ID (optional, defaults to first account)

## Output

Returns JSON with:
- `connected` - Whether connection succeeded
- `positions` - Array of positions with symbol, quantity, avg_cost, market_value, unrealized_pnl

If not connected, explain that TWS/Gateway needs to be running.

## Dependencies

- `ib-async`


## Timezone

All timestamps and time-based calculations must use the `America/New_York` timezone. All JSON output must include `generated_at` (NY time string) and `data_delay` fields.


---

## SKILL: ib-portfolio-action-report

- Fuente: `staskh/trading_skills` → `.claude/skills/ib-portfolio-action-report` (MIT)
- Cuándo usarla: Generate a comprehensive portfolio action report with earnings dates and risk assessment. Use when user asks for portfolio review, action items, earnings risk, or position management across IB accounts. Requires TWS or IB Gateway running locally.
- Código: extraer `code/staskh_trading_skills.tar` y usar `.claude/skills/ib-portfolio-action-report/` (report.py)

# IB Portfolio Action Report

Generate a comprehensive portfolio action report that analyzes all positions across Interactive Brokers accounts, fetches earnings dates, and provides traffic-light risk indicators (🔴🟡🟢) for each position.

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

> **Note:** If `uv` is not installed or `pyproject.toml` is not found, replace `uv run python` with `python` in all commands below.

```bash
uv run python scripts/report.py [--port PORT] [--account ACCOUNT]
```

The script returns JSON to stdout with analyzed portfolio data including risk levels, earnings dates, technical indicators, and spread groupings.

### Step 2: Format Report

Read `templates/markdown-template.md` for formatting instructions. Generate a markdown report from the JSON data and save to `sandbox/`.

**Filename**: `ib_portfolio_action_report_{ACCOUNT}_{YYYY-MM-DD}_{HHmm}.md`

### Step 3: Report Results

Present critical findings to the user: red/yellow items requiring attention, top priority actions, and the saved report path.

## Arguments

- `--port` - IB port (default: 7497 for paper trading)
- `--account` - Specific account ID to analyze (optional, defaults to all accounts)

## JSON Output

The script returns structured JSON with:
- `generated_at` - NY timestamp (e.g. `"2026-04-29 19:35 ET"`)
- `data_delay` - Data freshness (`"real-time"`)
- `accounts` - List of account IDs
- `summary` - Red/yellow/green counts
- `spreads` - All positions grouped into spreads with risk level, urgency, and recommendations
- `technicals` - Technical indicators per symbol (RSI, trend, SMAs, MACD, ADX)
- `earnings` - Earnings dates per symbol
- `prices` - Current prices per symbol
- `earnings_calendar` - Upcoming earnings with account/position info
- `account_summary` - Position and risk counts per account

## Report Sections

1. **Critical Summary**: Count of positions by risk level (🔴/🟡/🟢)
2. **Immediate Action Required**: Positions expiring within 2 days
3. **Urgent - Expiring Within 1 Week**: Short-term positions needing attention
4. **Critical Earnings Alert**: Positions with earnings this week
5. **Earnings Next Week**: Upcoming earnings exposure
6. **Expiring in 2 Weeks**: Medium-term expirations
7. **Longer-Dated Positions**: Core holdings with spread analysis
8. **Top Priority Actions**: Numbered action items by urgency
9. **Position Size Summary**: Account-level breakdown
10. **Earnings Calendar**: Next 30 days of earnings dates
11. **Technical Analysis Summary**: RSI, trend, SMAs, MACD, ADX for each underlying

## Example Usage

```bash
# All accounts (paper, default)
uv run python scripts/report.py

# Live account
uv run python scripts/report.py --port 7496

# Specific account
uv run python scripts/report.py --account U790497
```

## Dependencies

- `ib-async`
- `pandas-ta`
- `yfinance`


## Timezone

All timestamps and time-based calculations must use the `America/New_York` timezone. All JSON output must include `generated_at` (NY time string) and `data_delay` fields.

### Referencia: templates/markdown-template.md

# Portfolio Action Report - Markdown Template

Format the JSON data into a markdown report saved to `sandbox/`.

**Filename**: `ib_portfolio_action_report_{ACCOUNT}_{YYYY-MM-DD}_{HHmm}.md`
- Use first account ID if single account, "multi" if multiple

## JSON Structure

```
{
  "generated": "YYYY-MM-DD HH:MM",
  "accounts": ["ACC1", "ACC2"],
  "summary": { "red_count": N, "yellow_count": N, "green_count": N },
  "today_earnings_symbols": ["SYM1"],
  "spreads": [
    {
      "symbol": "AAPL",
      "account": "ACC1",
      "long": { "strike": 150, "expiry": "YYYYMMDD", "right": "C", "quantity": 1, "avg_cost": 5.00, "days_to_exp": 30 },
      "short": { ... },
      "underlying_price": 155.50,
      "earnings_date": "2026-03-15",
      "risk_level": "red|yellow|green",
      "risk_emoji": "🔴|🟡|🟢",
      "recommendation": "text",
      "min_days_to_exp": 7,
      "urgency": "expiring_2_days|expiring_1_week|expiring_2_weeks|longer_dated",
      "earnings_urgency": "this_week|next_week" (optional)
    }
  ],
  "earnings": { "AAPL": "2026-03-15", ... },
  "technicals": { "AAPL": { "rsi": 65.2, "trend": "bullish", "sma20": 150.5, "above_sma20": true, ... } },
  "prices": { "AAPL": 155.50 },
  "earnings_calendar": [ { "date": "2026-03-15", "symbol": "AAPL", "accounts": ["ACC1"], "position_types": ["Spread"] } ],
  "account_summary": [ { "account": "ACC1", "position_count": 10, "spread_count": 5, "red_count": 1, ... } ]
}
```

## Report Sections

### 1. Header
```markdown
# IB Portfolio Action Report - All Accounts
**Generated:** {generated}
**Market Status:** Earnings day (SYM1, SYM2 reporting today)  ← only if today_earnings_symbols non-empty
```

### 2. Critical Summary

| Status | Count | Description |
|--------|-------|-------------|
| 🔴 **RED** | {red_count} | Immediate action required |
| 🟡 **YELLOW** | {yellow_count} | Warning - earnings/expiration within 2 weeks |
| 🟢 **GREEN** | {green_count} | Monitor - no immediate action needed |

### 3. Urgency Sections

Group spreads by `urgency` field. For each group, render by account:

- **expiring_2_days**: `## 🔴 IMMEDIATE ACTION REQUIRED (Expiring ~{date} - 2 DAYS)`
- **expiring_1_week**: `## 🔴 URGENT - Expiring Within 1 Week` (include earnings column)
- **expiring_2_weeks**: `## 🟡 EXPIRING IN 2 WEEKS` (include earnings column)
- **longer_dated**: `## 🟢 LONGER-DATED POSITIONS (No Immediate Action)`

Table columns for short positions:
| Symbol | Position | Strike | Exp | Avg Cost | Underlying | [Earnings] | Action |

For longer-dated, use spread summary format:
| Spread | Long | Short | Underlying | Status |

### 4. Earnings Sections

Group spreads by `earnings_urgency`:
- **this_week**: `## 🔴 CRITICAL EARNINGS ALERT - This Week`
- **next_week**: `## 🟡 EARNINGS NEXT WEEK`

Show by symbol with position details and OTM/ITM status.

### 5. Top Priority Actions

Red spreads: `### 🔴 DO TODAY ({date})`
Yellow spreads: `### 🟡 MONITOR THIS WEEK`

Numbered list, top 5 each.

### 6. Position Size Summary

Use `account_summary` array:

| Account | Positions | Spreads | 🔴 Red | 🟡 Yellow | 🟢 Green |

### 7. Earnings Calendar

Use `earnings_calendar` array:

| Date | Symbol | Account | Position Type |

### 8. Technical Analysis Summary

Use `technicals` and `prices`:

| Symbol | Price | RSI | Trend | SMA20 | SMA50 | MACD | ADX |

Formatting:
- RSI >70: bold + 🔴; RSI <30: bold + 🟢
- Trend: bullish 📈, bearish 📉, neutral ➡️
- SMA: show price + ✓/✗ for above/below
- ADX >25: bold (strong trend)

### 9. Footer
```markdown
*Report generated by Trading Skills on {generated}*
```

## Traffic Light Indicators

- 🔴 **RED**: Immediate action (expiring soon, ITM short, earnings gap risk)
- 🟡 **YELLOW**: Warning zone (earnings within 2 weeks, monitor)
- 🟢 **GREEN**: Safe, no immediate action

## Expiry Formatting

Convert YYYYMMDD to "Mon DD" (e.g., "Feb 14").


---

## SKILL: ib-stop-loss

- Fuente: `staskh/trading_skills` → `.claude/skills/ib-stop-loss` (MIT)
- Cuándo usarla: Downside stop-loss management for PMCC, naked LEAPS, and stock positions in IB. Computes stop prices, detects alerts, and places conditional combo orders. Dry-run by default. Requires TWS or IB Gateway running locally.
- Código: extraer `code/staskh_trading_skills.tar` y usar `.claude/skills/ib-stop-loss/` (stop_loss.py)

# IB Stop-Loss Manager

Analyzes PMCC (diagonal call spread), naked LEAPS, and stock positions in the IB portfolio and manages conditional stop-loss orders.

**Default mode is dry-run** — no orders are placed unless `--execute` is in the request.

## IB Connection

TWS or IB Gateway must be running locally with API enabled:
- **Paper trading** — port 7497
- **Live trading** — port 7496
- **`IB_PORT` env var** — default port when `--port` is omitted (e.g. `IB_PORT=4001` for a Gateway container). Precedence: `--port` flag > `IB_PORT` > built-in default. Set it in the shell or a `.env` file.

**Port fallback:** If the configured port fails, automatically retry on the other port.
If the retry succeeds, save to memory which account type worked (live/paper) and reuse it for all IB skill calls in this and future sessions — until the user explicitly asks for the other account.
If both ports fail, ask the user to verify that TWS or IB Gateway is running with API access enabled.

## Instructions

### Step 1: Run the script

Dry-run (default — no orders placed):
```bash
uv run python .claude/skills/ib-stop-loss/scripts/stop_loss.py
```

Execute (cancel orphan orders + place SL_ conditional orders):
```bash
uv run python .claude/skills/ib-stop-loss/scripts/stop_loss.py --execute
```

Execute forced (basis = current mid price, can lower existing stops):
```bash
uv run python .claude/skills/ib-stop-loss/scripts/stop_loss.py --execute --forced
```

### Step 2: Format the report

Format JSON output as a markdown report with four sections:

#### Section 1: Alert Soon
List symbols in `alert_soon` prominently — these are past the early-warning threshold.

#### Section 2: Existing Conditional Orders
Show `all_conditional_orders.module` (SL_ orders) and `all_conditional_orders.manual` (manually placed).
If `orphan_orders` is non-empty, warn that these were cancelled (execute mode) or need manual cancellation (dry-run).

#### Section 3: Positions
For each entry in `positions`, show a table:

| Field | Value |
|---|---|
| Symbol | NVDA — pmcc (3 contracts) |
| Spot | $219.05 |
| LEAPS | 200C 20270115 · avg cost $44.27 · current $44.23 · basis $44.27 |
| **Stop price** | $22.14 (40% stop) → action: place_new |
| LEAPS loss | 0.1% |
| Shorts | 235C 20260515 · received $0.61 · current $0.56 · 9.5% decayed |

Show `preserve_existing` when a more-protective stop already exists.
Show `overwrite` (red) when `forced=true` lowers an existing stop.

#### Section 4: Alerts
Group alerts by symbol. Types:

| Type | Meaning |
|---|---|
| `leaps_early_warning` | LEAPS down ≥ stop_pct/2% from basis |
| `short_premium_decay` | 90%+ of short premium captured — close or roll |
| `short_near_strike` | Spot at/above or within X% of short strike |

### Step 3: Report to user

- State dry-run vs execute mode prominently.
- Lead with `alert_soon` symbols.
- For each position: show stop action and current loss %.
- Show alerts section last.

## Arguments

| Flag | Default | Description |
|------|---------|-------------|
| `--port` | 7497 | IB Gateway/TWS port |
| `--account` | all | Specific account ID |
| `--symbols` | all | Analyze only these symbols |
| `--legs` | none | Specific option legs: `SYMBOL:STRIKE[C\|P]:EXPIRY` (e.g. `IBKR:70C:20270115 IBKR:100C:20260918`). Right defaults to `C`. Takes precedence over `--symbols`. Use when multiple PMCC/LEAPS coexist on the same symbol and only one pairing should get a stop. |
| `--stop-pct` | 40 | Loss % that triggers exit |
| `--short-near-strike-pct` | 5 | Near-strike alert threshold |
| `--price-mode` | mid | Option pricing: `mid` or `last` |
| `--execute` | off | Cancel orphans + place SL_ orders |
| `--forced` | off | Use current mid as basis (requires `--execute`) |

## JSON Output Structure

```json
{
  "generated_at": "2026-05-12 10:00 ET",
  "dry_run": true,
  "forced": false,
  "stop_pct": 40.0,
  "short_near_strike_pct": 5.0,
  "accounts": ["U1234567"],
  "symbols_filter": null,
  "all_conditional_orders": {"module": [], "manual": []},
  "orphan_orders": [],
  "alert_soon": ["PFE"],
  "positions": [
    {
      "symbol": "NVDA",
      "type": "pmcc",
      "account": "U1234567",
      "qty": 3,
      "underlying_price": 219.05,
      "leaps": {
        "strike": 200.0, "expiry": "20270115", "avg_cost": 44.27,
        "current_price": 44.23, "stop_basis": 44.27,
        "stop_price": 22.14, "loss_pct": 0.1
      },
      "shorts": [
        {"strike": 235.0, "expiry": "20260515",
         "premium_received": 0.61, "current_price": 0.56, "decay_pct": 9.5}
      ],
      "stop_loss": {"stop_price": 22.14, "action": "place_new", "existing_stop": null},
      "alert_soon": false,
      "alerts": []
    },
    {
      "symbol": "AAPL",
      "type": "stock",
      "account": "U1234567",
      "qty": 100,
      "underlying_price": 189.50,
      "stock": {
        "avg_cost": 175.00, "stop_basis": 189.50,
        "stop_price": 94.75, "loss_pct": 0.0
      },
      "stop_loss": {"stop_price": 94.75, "action": "place_new", "existing_stop": null},
      "alert_soon": false,
      "alerts": []
    }
  ]
}
```

## Key Fields

- `alert_soon` — top-level list of symbols where loss ≥ stop_pct/2%
- `position.type` — `pmcc` | `leaps` | `stock`
- `stop_loss.action` — `place_new` | `preserve_existing` | `overwrite`
- `stop_loss.existing_stop` — price of the existing SL_FALL_ order if present
- For PMCC: stop order is a single combo (BAG) order closing LEAPS + all shorts atomically
- In execute mode: orphan SL_ orders (no matching position) are cancelled first

## Order Identification

- `SL_FALL_{SYM}_{STRIKE}_{EXPIRY}` — options (PMCC or naked LEAPS)
- `SL_FALL_{SYM}_STK` — stock positions

## Architecture

All analytics live in `src/trading_skills/broker/stop_loss.py`:

**Analytics (no IBKR — testable in isolation):**
- `calc_stop_basis` — max(mid, avg_cost) normally; current_mid if forced
- `calc_stop_price` — basis × (1 - stop_pct/100)
- `calc_short_premium_decay_pct` — % of short premium captured
- `identify_positions` — classify normalized positions into pmcc/leaps/stock
- `build_position_analysis` — full per-position output dict
- `detect_orphan_orders` — SL_FALL_ orders for gone positions
- `summarize_all_conditional_orders` — splits IB orders into module vs manual

**Data layer (IBKR):**
- `get_stop_loss_data` — main entry point
- `_cancel_orphan_orders` — cancel stale SL_ orders
- `_place_combo_stop_order` — BAG order for PMCC (atomic LEAPS + shorts)
- `_place_simple_stop_order` — single order for naked LEAPS or stock
- `_execute_position_stop` — dispatch per position type


---

## SKILL: ib-trailing-stop

- Fuente: `staskh/trading_skills` → `.claude/skills/ib-trailing-stop` (MIT)
- Cuándo usarla: Server-side trailing stop management for stocks and naked LEAPS in IB. Places native TRAIL orders that auto-ratchet the stop as price climbs. Dry-run by default. Requires TWS or IB Gateway running locally.
- Código: extraer `code/staskh_trading_skills.tar` y usar `.claude/skills/ib-trailing-stop/` (trailing_stop.py)

# IB Trailing Stop Manager

Places IB native **TRAIL** orders against stocks and naked LEAPS in the portfolio.
IB auto-adjusts the stop trigger as the price climbs and locks it as price falls.

PMCC positions are intentionally excluded — use `ib-stop-loss` for those (a standalone
trailing stop on the PMCC long leg would break the hedge at trigger).

**Default mode is dry-run** — no orders are placed unless `--execute` is in the request.

## IB Connection

TWS or IB Gateway must be running locally with API enabled:
- **Paper trading** — port 7497
- **Live trading** — port 7496
- **`IB_PORT` env var** — default port when `--port` is omitted (e.g. `IB_PORT=4001` for a Gateway container). Precedence: `--port` flag > `IB_PORT` > built-in default. Set it in the shell or a `.env` file.

**Port fallback:** If the configured port fails, automatically retry on the other port.
If the retry succeeds, save to memory which account type worked (live/paper) and reuse it for all IB skill calls in this and future sessions — until the user explicitly asks for the other account.
If both ports fail, ask the user to verify that TWS or IB Gateway is running with API access enabled.

## Instructions

### Step 1: Run the script

Dry-run (default — no orders placed):
```bash
uv run python .claude/skills/ib-trailing-stop/scripts/trailing_stop.py --symbols JOBY --trail-pct 20
```

Execute (cancel orphan TS_ orders + place new TS_ TRAIL orders):
```bash
uv run python .claude/skills/ib-trailing-stop/scripts/trailing_stop.py --symbols JOBY --trail-pct 20 --execute
```

Execute forced (cancel + replace existing TS_ orders with current parameters):
```bash
uv run python .claude/skills/ib-trailing-stop/scripts/trailing_stop.py --execute --forced
```

### Step 2: Format the report

Format JSON output as a markdown report with three sections:

#### Section 1: Existing TRAIL Orders
Show `all_trail_orders.module` (TS_ orders) and `all_trail_orders.manual` (manually placed).
If `orphan_orders` is non-empty, warn that these were cancelled (execute mode) or need manual cancellation (dry-run).

#### Section 2: Positions
For each entry in `positions`, show a table:

| Field | Value |
|---|---|
| Symbol | JOBY — stock (1000 shares) |
| Spot | $7.50 |
| Reference | $7.50 (max of current $7.50, avg cost $5.00) |
| **Trail params** | 20% (initial stop $6.00) → action: place_new |
| Existing trail | none |

For LEAPS rows, also show the option leg (strike/expiry) and current option mark.

`action` values:
- `place_new` — no existing TS_ order; one will be created in execute mode
- `preserve_existing` — TS_ already in place; left alone (IB has been tracking the high)
- `overwrite` — `--forced` is on; existing TS_ will be cancelled and replaced

#### Section 3: Order Results (execute mode only)
Per-position result with `order_id` and `order_ref`.

### Step 3: Report to user

- State dry-run vs execute mode prominently.
- Lead with positions that have `action: place_new` (these are about to get a new TRAIL).
- Call out `preserve_existing` separately so user knows nothing changed.
- Show existing trail details (current `trail_stop_price`) so user knows where IB has trailed to.

## Arguments

| Flag | Default | Description |
|------|---------|-------------|
| `--port` | 7497 | IB Gateway/TWS port |
| `--account` | all | Specific account ID |
| `--symbols` | all | Analyze only these symbols |
| `--trail-pct` | 20 | Trail amount as percentage of reference |
| `--trail-amt` | — | Trail amount in dollars (mutually exclusive with --trail-pct) |
| `--price-mode` | mid | Option pricing: `mid` or `last` (LEAPS only) |
| `--execute` | off | Cancel orphans + place TS_ TRAIL orders |
| `--forced` | off | Cancel and replace existing TS_ orders (requires `--execute`) |

## JSON Output Structure

```json
{
  "generated_at": "2026-05-29 10:00 ET",
  "data_delay": "real-time",
  "dry_run": true,
  "forced": false,
  "trail_pct": 20.0,
  "trail_amt": null,
  "accounts": ["U1234567"],
  "symbols_filter": ["JOBY"],
  "all_trail_orders": {"module": [], "manual": []},
  "orphan_orders": [],
  "positions": [
    {
      "symbol": "JOBY",
      "type": "stock",
      "account": "U1234567",
      "qty": 1000,
      "underlying_price": 7.50,
      "stock": {
        "avg_cost": 5.00,
        "current_price": 7.50
      },
      "trail_stop": {
        "trail_pct": 20.0,
        "trail_amt": null,
        "reference": 7.50,
        "initial_stop_price": 6.00,
        "action": "place_new",
        "existing_trail": null
      }
    }
  ]
}
```

## Key Behaviors

- **Reference price** = `max(current_price, avg_cost)` — locks in profit when above cost, never starts below entry.
- **Forced mode** uses `current_price` as the reference (can place an initial stop below entry, useful when re-arming after a drawdown).
- **Existing TS_ orders are preserved by default** because IB has been ratcheting the trail since placement — replacing would reset that tracked high. Use `--forced` to deliberately reset.
- **Scope**: stocks + naked LEAPS only. PMCC positions are excluded; use `ib-stop-loss` for those.

## Order Identification

- `TS_{SYM}_{STRIKE}_{EXPIRY}_{RIGHT}` — naked LEAPS TRAIL orders (right is `C` or `P` so calls and puts on the same strike/expiry don't collide)
- `TS_{SYM}_STK` — stock TRAIL orders

## Architecture

All analytics live in `src/trading_skills/broker/trailing_stop.py`:

**Analytics (no IBKR — testable in isolation):**
- `calc_trail_reference` — `max(current_price, avg_cost)` normally; `current_price` if forced
- `calc_initial_trail_stop_price` — reference × (1 − trail_pct/100) or reference − trail_amt
- `identify_trailable_positions` — stocks + naked LEAPS; PMCC excluded
- `build_trail_analysis` — full per-position output dict
- `detect_orphan_trail_orders` — TS_ TRAIL orders for gone positions
- `summarize_all_trail_orders` — splits IB TRAIL orders into module vs manual

**Data layer (IBKR):**
- `get_trailing_stop_data` — main entry point
- `_cancel_orphan_orders` — cancel stale TS_ orders
- `_place_simple_trail_order` — native TRAIL order on stock or option
- `_execute_position_trail` — dispatch per position type


---

## SKILL: issue-management

- Fuente: `SYasJ/claude-business-skills` → `plugins/risk/skills/issue-management` (MIT)
- Cuándo usarla: Record a compliance or control issue with severity, owner, and a dated remediation. Use when the user mentions issue management, control issue, remediation plan, audit issue, or asks for a issue record. Risk and compliance skill by Yasir Jilani.

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'issue-management' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Issue Management

Record a compliance or control issue with severity, owner, and a dated remediation.

## When to use this skill

Use this skill when the user:

- issue management
- control issue
- remediation plan
- audit issue

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

- The issue
- The failed control or obligation
- The harm
- The proposed fix

## Workflow


### 1. Step 1

Describe the issue as a fact, not as a softening adjective.
### 2. Step 2

Link it to the control or obligation.
### 3. Step 3

Rate severity with their scale or a labeled proposal.
### 4. Step 4

Write remediation with an owner and a date. A plan without either is a wish.
### 5. Step 5

Note compensating control until the fix lands.
### 6. Step 6

Verify closure with evidence, not with an email that says done.

## Output

Deliver a **issue record**.

- Purpose of this issue record, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs an issue record by 30 September 2026. An issue is marked closed because the owner said the spreadsheet was updated, with no sample.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

An issue is marked closed because the owner said the spreadsheet was updated, with no sample.

The issue: Control 7.2 access review, recorded 14 September 2026. No supporting file attached
The failed control or obligation: their one-page rule dated 2 Mar 2026. No exception log since
The harm: Control 7.2 access review, recorded 14 September 2026. No supporting file attached
The proposed fix: Control 7.2 access review, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Issue record**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
An open issue until a sample shows the control operating, with a dated owner.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The issue | Control 7.2 access review, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The failed control or obligation | their one-page rule dated 2 Mar 2026. No exception log since | Carried into the draft |
| The harm | Control 7.2 access review, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The proposed fix | Control 7.2 access review, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Describe the issue as a fact, not as a softening adjective**

**2. Link it to the control or obligation**

**3. Rate severity with their scale or a labeled proposal**

**4. Write remediation with an owner and a date. A plan without either is a wish**

**5. Note compensating control until the fix lands**

**Deliberately not done**
- Closure without evidence.
- No owner.
- A softened description that hides the gap.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Closure without evidence
- No owner
- A softened description that hides the gap

## Related skills

- `control-design`
- `audit-response`


---

## SKILL: know-your-customer

- Fuente: `JoelLewis/finance_skills` → `plugins/compliance/skills/know-your-customer` (MIT)
- Cuándo usarla: Guide customer onboarding identification, due diligence, and profile maintenance under FINRA Rule 2090, the CIP rules, and the FinCEN CDD Rule. Use when the user asks about onboarding identity verification, beneficial ownership collection for entity accounts, enhanced due diligence for PEPs or high-risk customers at account opening, assigning the initial customer risk rating, KYC refresh triggers, or documentary vs non-documentary verification. Also trigger when users mention 'account opening requirements', 'who is the beneficial owner', 'new client identity check', 'how often to update KYC', 'essential facts for the account', 'foreign customer onboarding', or ask what information must be gathered before opening an account. (For ongoing transaction monitoring, SAR filing, and surveillance-driven risk re-rating, use anti-money-laundering.)

# Know Your Customer

Regulatory status current as of June 2026 — verify effective dates, dollar thresholds, and pending rulemakings against current SEC/FINRA/FinCEN sources before advising.

## Core Concepts

### FINRA Rule 2090 — Know Your Customer
Every FINRA member must use reasonable diligence, with regard to the opening and maintenance of every account, to know and retain the essential facts concerning every customer and concerning the authority of each person acting on behalf of the customer. "Essential facts" are those required to: (a) effectively service the account, (b) act in accordance with any special handling instructions, (c) understand the authority of each person acting on behalf of the customer, and (d) comply with applicable laws, regulations, and rules.

### Customer Identification Program (CIP)
Required under USA PATRIOT Act Section 326 and implementing regulations. The broker-dealer CIP rule is **31 CFR 1023.220**; the bank CIP rule is 31 CFR 1020.220. (SEC Rule 17a-8 separately requires broker-dealers to comply with BSA recordkeeping and reporting.) The CIP must include:

- **Identity verification** for each customer opening an account: name, date of birth (for individuals), address, and identification number (SSN for US persons; passport number/country or other government ID for non-US persons)
- **Verification procedures** using documentary methods (government-issued ID), non-documentary methods (credit bureau checks, public database searches, financial statement review), or a combination
- **Recordkeeping** — retain identifying information and verification methods for 5 years after account closure
- **Comparison with government lists** — check customer names against OFAC and other government terrorist/sanctions lists
- **Customer notice** — inform customers that information is being collected to verify identity

### Customer Due Diligence (CDD) Rule
FinCEN's CDD Rule (31 CFR 1010.230, effective May 2018) requires covered financial institutions to:

1. **Identify and verify the identity of customers** (overlaps with CIP)
2. **Identify and verify the identity of beneficial owners of legal entity customers** — any individual who owns 25% or more of the equity interests, plus one individual with significant responsibility for managing the entity (a control person)
3. **Understand the nature and purpose of customer relationships** to develop a customer risk profile
4. **Conduct ongoing monitoring** to identify suspicious transactions and, on a risk basis, maintain and update customer information

The 25% beneficial ownership threshold applies to legal entities (corporations, LLCs, partnerships). Certain entities are exempt: publicly traded companies, regulated financial institutions, government entities, and others listed in the rule.

### Enhanced Due Diligence (EDD)
Higher-risk customers require additional scrutiny beyond standard CDD:

- **Politically Exposed Persons (PEPs)** — senior foreign political figures and their families/associates. No US regulatory definition mandates PEP screening for domestic customers, but FinCEN guidance and FATF standards expect it for foreign PEPs. Firms should understand the source of wealth and funds.
- **Foreign correspondent accounts** — BSA Section 312 requires EDD for correspondent accounts maintained for foreign financial institutions, with heightened requirements for institutions in jurisdictions of concern
- **High-risk jurisdictions** — countries identified by FATF, FinCEN advisories, or firm risk assessments as presenting elevated ML/TF risk
- **Complex ownership structures** — multi-layered entities, trusts with opaque beneficiary structures, nominee arrangements
- **Unusual account activity** — customers whose transaction patterns deviate significantly from expected activity based on their profile

EDD measures include: senior management approval for account opening, source of wealth/funds verification, more frequent account reviews, enhanced transaction monitoring, and ongoing negative media screening.

### Documentary vs Non-Documentary Verification
**Documentary methods:** Unexpired government-issued photo ID (driver's license, passport, state ID), documents showing formation of a legal entity (articles of incorporation, partnership agreement, trust instrument).

**Non-documentary methods:** Credit bureau inquiries, public database verification (Lexis-Nexis, etc.), financial statement verification, references from other financial institutions. Required as a backup when documentary verification is unavailable, inconclusive, or the customer is not physically present (e.g., online account opening).

Firms must use non-documentary methods in at least the following situations: (1) the customer opens an account without appearing in person, (2) the firm is not familiar with the documents presented, (3) other circumstances that increase risk.

### Ongoing Monitoring and Profile Updates
KYC is not a one-time event. Customer profiles must be updated when:

- **Material life events** occur (retirement, marriage/divorce, inheritance, job loss, significant health changes)
- **Account review triggers** fire (periodic reviews, risk-based reviews, transaction-triggered reviews)
- **Transaction patterns** deviate significantly from the established profile
- **The customer provides new information** that changes their investment profile
- **Regulatory changes** require additional information (e.g., new beneficial ownership requirements)

FINRA does not mandate a specific refresh cycle, but firms typically establish risk-based review schedules (e.g., annual review for high-risk accounts, every 3 years for standard risk).

### SEC Requirements for Investment Advisers
Investment advisers have a fiduciary duty to understand their clients, which creates KYC-like obligations independent of FINRA rules. Form ADV Part 2A describes the adviser's services and client relationships. The SEC expects advisers to gather sufficient information to fulfill their fiduciary duty of care — including financial situation, investment objectives, risk tolerance, and any constraints. FinCEN's 2024 final rule (31 CFR Part 1032) would extend BSA/AML program and SAR requirements to SEC-registered investment advisers, but its effective date was postponed from January 1, 2026 to January 1, 2028, and FinCEN has said it will revisit the rule's substance (and the companion proposed adviser CIP rule, jointly with the SEC) before then — verify current status.

### Recordkeeping Requirements
- **CIP records:** Identifying information, verification documents/methods, and resolution of discrepancies must be retained for 5 years after account closure
- **CDD/beneficial ownership:** Copies of beneficial ownership certification forms and verification records retained for 5 years after account closure
- **Account records:** FINRA Rule 4512 requires maintenance of customer name, tax ID, address, date of birth, employment status, associated person relationship, trusted contact person, and other information specified in the rule
- **Reliance on other institutions:** Under Section 326 reliance provisions, a firm may rely on another financial institution's CIP if: (a) the relying firm's CIP incorporates this reliance, (b) the other institution is subject to an AML program rule, and (c) the other institution enters into a written contract for this purpose

## Worked Examples

### Example 1: Opening a trust account without identifying beneficial owners
**Scenario:** A wealth management firm opens a revocable living trust account for a family trust. The account opening team collects the trust agreement and identifies the grantor/trustee but does not collect beneficial ownership information on the trust beneficiaries. The trust holds $2M in investable assets.
**Compliance Issues:** Potential CDD Rule violation. While revocable living trusts are generally exempt from the beneficial ownership requirement (since the grantor maintains control), irrevocable trusts and other legal entity structures require beneficial ownership identification. The team must correctly classify the trust type. Additionally, FINRA Rule 4512 requires identification of all persons authorized to transact in the account.
**Analysis:** The firm should have a clear trust classification workflow that determines: (1) whether beneficial ownership requirements apply based on the trust type, (2) who has authority to act on the account, and (3) what documentation is required. For revocable trusts, identifying the grantor/trustee as the beneficial owner and control person is typically sufficient, but the firm should verify the trust is truly revocable and document the determination. The trust agreement must be reviewed — not just collected.

### Example 2: Failing to update KYC after a client retires
**Scenario:** A long-standing client retires at age 65 after 20 years at the firm. Her account profile still lists her investment objective as "aggressive growth," risk tolerance as "high," and annual income at $250,000. Post-retirement, her income drops to $80,000 (Social Security and pension) and she begins taking regular distributions from the account. No profile update is triggered.
**Compliance Issues:** Stale KYC data leading to potential suitability violations. The client's investment profile has materially changed — time horizon has shifted, income has declined, liquidity needs have increased (regular distributions), and risk capacity has decreased. Continued aggressive growth recommendations based on outdated profile data would likely violate suitability obligations.
**Analysis:** The firm should have systems that flag material life events (age milestones, distribution patterns, income changes) as triggers for KYC refresh. A representative who knows a client has retired but does not update the profile is failing the "reasonable diligence" standard of Rule 2090. Best practice: establish automated triggers (client turns 65, regular withdrawals begin, account balance drops significantly) and require profile confirmation at each periodic review.

### Example 3: Onboarding a high-risk foreign entity
**Scenario:** A broker-dealer receives an account application from a newly formed LLC registered in Delaware with a single listed owner who is a citizen of a jurisdiction flagged in a FinCEN advisory. The stated purpose is "general investing." The LLC provides articles of organization but limited information about the source of funds.
**Compliance Issues:** Multiple red flags requiring enhanced due diligence: newly formed entity, high-risk jurisdiction connection, limited transparency on source of funds, Delaware LLC (common in layering structures). Standard CDD is insufficient.
**Analysis:** The firm must: (1) complete standard CDD including beneficial ownership (25% owners and one control person), (2) escalate to enhanced due diligence given the risk factors, (3) verify source of funds and source of wealth, (4) conduct OFAC screening on all identified individuals, (5) obtain senior management approval before opening, (6) establish enhanced ongoing monitoring. The firm should also consider whether the limited information provided is itself a red flag warranting a SAR filing or account refusal. Simply accepting "general investing" as a purpose statement for a high-risk entity is insufficient.

## Common Pitfalls
- Treating KYC as a one-time account-opening exercise rather than an ongoing obligation
- Collecting but not verifying beneficial ownership information — the CDD Rule requires both identification and verification
- Applying the same due diligence to all customers regardless of risk — risk-based approach is required
- Not documenting when a customer declines to provide information and failing to narrow the recommendation universe accordingly
- Relying solely on documentary verification for online/remote account opening without implementing non-documentary backup methods
- Failing to establish automated triggers for profile refresh (life events, transaction anomalies, age milestones)
- Not screening beneficial owners and control persons against OFAC and other sanctions lists
- Confusing the CDD Rule's beneficial ownership requirements with FINRA Rule 4512's account record requirements — they overlap but are distinct
- Incomplete trust classification leading to incorrect application of beneficial ownership requirements
- Not training frontline staff to recognize when a customer's circumstances have changed, triggering a profile update obligation

## Cross-References
- **anti-money-laundering** (compliance plugin): KYC/CDD data feeds directly into AML monitoring and suspicious activity detection
- **investment-suitability** (compliance plugin): Customer profile gathered through KYC is the foundation for suitability analysis
- **reg-bi** (compliance plugin): Reg BI's Care Obligation requires understanding the customer's investment profile — sourced from KYC
- **investment-policy** (wealth-management plugin): IPS constraints (time horizon, risk tolerance, liquidity) derive from KYC profiling
- **account-opening-compliance** (client-operations plugin): The onboarding compliance workflow that operationalizes CIP verification, CDD, and beneficial ownership collection defined here
- **account-opening-workflow** (client-operations plugin): The operational account opening process where KYC data collection and verification are embedded


---

## SKILL: margin-operations

- Fuente: `JoelLewis/finance_skills` → `plugins/trading-operations/skills/margin-operations` (MIT)
- Cuándo usarla: Guide margin lending, margin requirements, and margin call operations for brokerage and advisory accounts. Use when calculating Reg T initial margin or buying power, determining maintenance margin or house requirements, evaluating portfolio margin eligibility under OCC TIMS, generating or resolving margin calls (fed call, house call, exchange call, day-trade call), designing forced liquidation waterfall logic, structuring securities-backed lines of credit (SBLOC), computing margin interest impact on returns, assessing concentrated position margin, understanding pattern day trader rules, or reviewing FINRA 4210 and Reg U requirements. Also covers SMA calculations and short margin mechanics. For OTC derivatives margin (variation/initial margin, CSAs, SIMM) see counterparty-risk.

# Margin Operations

## Core Concepts

### Regulation T Initial Margin
The Federal Reserve's Regulation T establishes the initial margin requirement for purchasing securities on credit. Key provisions:

- **50% initial margin requirement:** An investor must deposit at least 50% of the purchase price of marginable securities. For a $100,000 purchase, the investor must deposit $50,000 (cash or marginable securities); the broker-dealer may lend the remaining $50,000.
- **Reg T buying power:** The maximum dollar amount a client can purchase given their available equity. Buying power = SMA x 2 (for equity securities under Reg T). If a client deposits $100,000 cash in a new margin account, buying power is $200,000.
- **Special Memorandum Account (SMA):** A bookkeeping entry that tracks the client's excess Reg T equity. SMA increases when: the account has excess equity above 50%, securities are sold, dividends or cash are deposited. SMA decreases when used to purchase securities or withdraw cash. SMA is a high-water mark — it does not decrease when market values decline (unless used).
- **Reg T extension procedures:** When a client fails to meet the initial margin requirement by settlement date, the broker-dealer must request an extension from a self-regulatory organization (SRO). Extensions are typically granted for 1-5 business days. Failure to meet the call results in forced liquidation and a 90-day freeze (restricted account).
- **Exempt securities:** U.S. government bonds, municipal bonds, and certain agency securities are exempt from Reg T margin requirements — they can be purchased with lower or no initial margin.
- **Day-trade margin:** FINRA Rule 4210 provides pattern day traders (4+ day trades in 5 business days) with 4:1 intraday buying power (25% margin) but requires a minimum equity of $25,000 — day-trade buying power = (equity - $25,000 minimum) × 4. Overnight positions revert to standard 2:1 Reg T buying power.

### Maintenance Margin
After the initial purchase, ongoing maintenance margin requirements determine the minimum equity the account must maintain:

- **FINRA Rule 4210 minimum:** 25% equity for long positions. Account equity = market value of securities minus debit balance. If equity falls below 25% of market value, a maintenance margin call is triggered.
- **House maintenance requirements:** Most broker-dealers impose requirements above the FINRA minimum, typically 30-40% for diversified accounts. House requirements vary by firm and may change based on market conditions.
- **Concentrated position margin:** Single-stock positions exceeding a threshold (e.g., 40-60% of account value) face elevated margin requirements, often 50-75% or higher. This discourages excessive concentration in margin accounts.
- **Long margin formula:** Maintenance call triggered when equity / market value < maintenance requirement, where account equity = market value - debit balance. Equivalently, a call is triggered when market value falls to: debit balance / (1 - maintenance requirement). The call amount due is (maintenance requirement × market value) - equity.
- **Short margin requirements:** Short positions require initial margin of 50% (Reg T) and maintenance of 30% of market value (FINRA minimum). Short account equity = credit balance - market value of short securities. A short squeeze (rising prices) increases the maintenance requirement.
- **Options margin:** Options strategies have specific margin requirements under FINRA Rule 4210 and exchange rules. Covered calls require no additional margin (shares serve as collateral). Naked short options require substantial margin — typically the greater of: (a) option premium + 20% of underlying value - out-of-the-money amount, or (b) option premium + 10% of underlying value. Spreads have defined-risk margin equal to the maximum loss.

### Portfolio Margin
A risk-based margining methodology that can significantly reduce margin requirements for hedged or diversified portfolios:

- **Methodology:** Uses the Options Clearing Corporation's Theoretical Intermarket Margin System (OCC TIMS) to compute margin based on the theoretical maximum loss of the portfolio under a range of stress scenarios, rather than applying fixed percentage requirements to each position independently.
- **Eligibility requirements:** Minimum account equity of $100,000 (FINRA Rule 4210(g)), options trading approval (typically Level 3 or 4), and the firm may impose additional requirements such as minimum net worth, trading experience, or completion of a portfolio margin agreement.
- **Stress test scenarios:** The OCC TIMS model evaluates portfolio profit and loss under standardized moves:
  - Large-cap equities: +/- 15% (with intermediate points at +/- 5%, +/- 10%)
  - Small-cap equities: +/- 10% higher stress (effectively +/- 25%)
  - Broad market indices: +/- 8% to +/- 15%
  - High-volatility securities: firm-specific add-ons
  - The largest theoretical loss across all scenarios becomes the margin requirement
- **Portfolio margin vs Reg T comparison:** A hedged equity portfolio with offsetting options positions might require 50% margin under Reg T (applied position-by-position) but only 10-20% under portfolio margin (reflecting the actual net risk). Conversely, a concentrated, unhedged portfolio may see little benefit from portfolio margin.
- **Benefits:** More efficient use of capital, margin requirements that reflect actual portfolio risk, ability to maintain larger or more complex positions, and alignment between margin and true economic risk.
- **Risks:** Lower margin requirements increase leverage, amplifying both gains and losses. A sudden correlation shift or gap move can produce losses exceeding the stress test scenarios. Portfolio margin accounts can experience rapid, severe margin calls during market dislocations.

### Margin Call Types
Multiple types of margin calls can arise, each with distinct triggers, deadlines, and resolution procedures:

- **Reg T initial call (federal call):** Triggered when a client purchases marginable securities and the account does not have sufficient equity to satisfy the 50% Reg T requirement. Must be met by settlement date (T+1 for most securities). Met by depositing cash or fully paid marginable securities. Failure to meet triggers liquidation and potential 90-day account restriction.
- **Maintenance margin call (house call):** Triggered when account equity falls below the firm's house maintenance requirement (typically 30-40%). The client is typically given T+5 business days (or less, at the firm's discretion) to deposit funds or securities, or the firm will liquidate positions. Unlike Reg T calls, there is no SRO extension mechanism for house calls — the timeline is at the firm's discretion.
- **Exchange minimum call:** Triggered when account equity falls below the FINRA/exchange minimum of 25%. These calls demand immediate attention and may be subject to same-day or next-day resolution.
- **Day-trade call:** Triggered when a pattern day trader's account equity falls below the $25,000 minimum or when day-trade buying power is exceeded. Must be met within 5 business days. Failure restricts the account to cash-available trading.
- **Concentration call:** Triggered when a single position exceeds the firm's concentration threshold and the account's equity is insufficient to meet the elevated requirement. Common in accounts holding large positions in a single stock.

### Margin Call Procedures
The end-to-end process from call generation through resolution:

- **Call generation:** Margin calls are generated during the end-of-day mark-to-market process. The firm's margin system reprices all positions at closing market values, recalculates equity and margin requirements, and identifies accounts in deficit. Intraday monitoring may generate real-time alerts for large deficits.
- **Notification requirements:** FINRA requires prompt notification to the customer. Firms typically notify via multiple channels: automated system alerts, email, phone calls from the margin department. Written notification must document the call amount, the positions involved, and the deadline for resolution.
- **Client communication:** The margin department communicates the amount due, the deadline, and the options available: deposit cash, deposit marginable securities, liquidate positions, or some combination. Best practice is to confirm the client's intentions in writing.
- **Call resolution tracking:** The margin system tracks each open call, the deadline, any partial payments received, and escalation status. Calls are resolved when equity is restored to or above the required level.
- **Extension requests:** For Reg T calls, the firm may request an extension from its designated examining authority (DEA) or SRO — typically 1-5 business days. Extensions are not automatic and are granted based on the circumstances (e.g., pending settlement of a sale, wire transfer in process). Repeated extension requests for the same account may trigger regulatory scrutiny.
- **Automatic liquidation triggers:** If the call is not met by the deadline and no extension is granted, the firm is obligated to liquidate sufficient positions to bring the account into compliance. Many firms have automated systems that initiate liquidation at a specified time on the deadline day.
- **Partial call satisfaction:** A client may partially satisfy a call through a combination of deposits and sales. The margin system must track partial payments and recalculate the remaining call amount after each action.

### Forced Liquidation
When a margin call is not met, the broker-dealer must liquidate positions to bring the account into compliance:

- **Liquidation waterfall:** Firms establish a priority order for which positions to liquidate first. A common waterfall:
  1. Fully paid (non-margin) positions with no tax consequences if available for transfer
  2. Positions specifically identified by the client (if communicated in time)
  3. Most liquid positions (highest average daily volume, tightest bid-ask spreads)
  4. Positions with the lowest unrealized gain or highest unrealized loss (minimizing tax impact where feasible)
  5. Concentrated positions contributing most to the margin deficit
  6. Least liquid positions as a last resort
- **Liquidation priority rules:** The firm has discretion over which positions to liquidate and is not required to follow client preferences, though best practice is to accommodate client requests when operationally feasible. The firm's primary obligation is to reduce the margin deficit.
- **Client notification:** The firm should notify the client before or promptly after liquidation, though FINRA does not require prior consent for liquidation of margin-deficient accounts. The client cannot prevent the firm from liquidating.
- **Best execution in liquidation:** Forced liquidation must still comply with best execution obligations. Orders should be routed to obtain the best reasonably available price, even under time pressure. Market orders in illiquid securities during forced liquidation can create adverse price impact.
- **Restricted account status:** An account that fails to meet a Reg T call may be restricted for 90 days, during which the client must fully prepay any purchases (no margin extension). Subsequent violations may result in longer restrictions or account closure.
- **Close-out obligations:** Under SEC Rule 15c3-3 and SRO rules, the firm must close out fail-to-deliver positions within specified timeframes. Margin liquidation must be completed promptly, and any resulting short positions or failed deliveries must be resolved per regulatory requirements.

### Securities-Backed Lines of Credit (SBLOC)
Lending products that use an investment portfolio as collateral, distinct from traditional margin lending:

- **Non-purpose loans vs purpose loans:** An SBLOC is typically a non-purpose loan — the proceeds may be used for any purpose except purchasing, carrying, or trading securities. This distinction matters because non-purpose loans are governed by Regulation U (for banks) or Regulation T (for broker-dealers), with different requirements depending on the lender type.
- **Collateral requirements:** The investment portfolio secures the loan. Lenders apply loan-to-value (LTV) ratios to determine borrowing capacity:
  - Equities (large-cap, diversified): 50-70% LTV
  - Fixed income (investment grade): 70-90% LTV
  - Mutual funds/ETFs (broad market): 50-75% LTV
  - Cash and money market: 90-95% LTV
  - Concentrated single-stock positions: 30-50% LTV (reduced due to specific risk)
  - Alternative investments, restricted stock, penny stocks: 0% LTV (not accepted as collateral)
- **Concentration limits:** Lenders limit the percentage of the collateral portfolio that can be in a single security (typically 40-60% maximum). Positions exceeding the concentration limit receive reduced or zero LTV on the excess.
- **Maintenance and call procedures:** Similar to margin accounts, SBLOC facilities have maintenance requirements. If the portfolio value declines such that the LTV exceeds the maintenance threshold, the lender issues a collateral call. The borrower must deposit additional collateral, repay part of the loan, or face liquidation of the pledged portfolio.
- **Regulatory considerations:** Banks offering SBLOCs are subject to Regulation U (Fed), which imposes a 50% maximum LTV for purpose loans but has no specific LTV limit for non-purpose loans — the bank applies its own underwriting standards. Broker-dealers offering similar credit are subject to Regulation T. The distinction between purpose and non-purpose must be documented (Form U-1 for banks, Form T-4 for broker-dealers).
- **Risks to the borrower:** Portfolio declines can trigger collateral calls; forced liquidation of securities may occur at unfavorable prices and create taxable events; the interest rate is typically variable (prime + spread); and the borrower retains full investment risk on the pledged portfolio while adding debt service obligations.

### Margin Risk Management
Ongoing monitoring and management of margin-related risks across the firm and client accounts:

- **Portfolio-level margin monitoring:** The firm's risk management system continuously monitors aggregate margin exposure, identifying accounts approaching margin call thresholds, concentrated positions, and correlated risks across the client base. Real-time intraday monitoring supplements end-of-day calculations. FINRA Rule 4521 requires member firms to report aggregate margin balances and related data to FINRA.
- **Stress testing margin requirements:** The firm should stress test margin exposure under adverse scenarios — market declines of 10-20%, sector-specific shocks, volatility spikes, and correlation breakdowns. Stress tests reveal accounts and portfolios that would face large margin calls under stressed conditions.
- **Concentrated position risk:** Positions that represent a large percentage of account value or a large percentage of a security's outstanding shares create elevated margin risk. Firms typically impose higher margin requirements and may impose position limits or require diversification plans.
- **Margin impact on investment returns:** Margin amplifies both gains and losses — return on equity = (portfolio return × leverage) - (interest rate × (leverage - 1)). A 50% margin (2:1 leverage) doubles the percentage gain or loss:
  - Unleveraged: $100K invested, market +10% = $10K gain (10% return)
  - Leveraged at 2:1: $200K invested with $100K equity, market +10% = $20K gain minus interest = ~18% return on equity
  - Leveraged at 2:1: $200K invested with $100K equity, market -10% = $20K loss plus interest = ~-22% return on equity
- **Interest rate calculation on margin debit balances:** Margin interest is calculated daily on the outstanding debit balance:
  - Daily interest = debit balance x (annual rate / 360)
  - Interest is typically charged monthly (sum of daily accruals)
  - Rates are tiered by debit balance size: larger balances receive lower rates
  - Illustrative rate schedule: <$25K = broker call rate + 1.5%; $25K-$100K = call rate + 1.0%; >$100K = call rate + 0.5% (spreads and the call rate itself vary by firm and rate environment)
- **Tax treatment of margin interest:** Margin interest is deductible as investment interest expense on Schedule A (Form 1040), but only up to the amount of net investment income. Excess margin interest can be carried forward. Investment interest does not include qualified dividends or long-term capital gains unless the taxpayer elects to treat them as ordinary income. This deduction requires itemizing.

## Worked Examples

Three worked examples are in [references/examples.md](references/examples.md) — load for an end-to-end scenario: (1) calculating margin requirements and buying power for a new diversified account, (2) managing a margin call sequence from generation through resolution, (3) evaluating portfolio margin vs Reg T for an active options trader.

## Common Pitfalls
- Confusing SMA with account equity — SMA is a high-water mark that does not decline with market value drops, leading clients to believe they have more cushion than they do
- Failing to account for margin interest as a drag on returns — at the 7-8% margin rates typical of recent rate environments, the hurdle rate for margined positions is substantial
- Relying on Reg T buying power without monitoring maintenance levels — a position can be purchased within buying power but quickly trigger a maintenance call after a decline
- Assuming portfolio margin is always more favorable — concentrated, unhedged positions may receive similar or higher margin under portfolio margin stress tests
- Not planning for margin call deadlines — margin calls arrive during market stress when the client is least likely to have available cash
- Treating SBLOC as "free" liquidity — a market decline can trigger a collateral call simultaneously with the investment losses, creating a double impact
- Liquidating positions for margin calls without considering tax consequences — forced sales may realize gains or losses at inopportune times
- Pattern day trader margin surprise — accounts can be reclassified as pattern day trader and face the $25,000 minimum equity requirement unexpectedly
- Ignoring correlation between margin calls and market stress — the client's ability to deposit cash may be impaired at exactly the time a margin call demands it
- Assuming the firm must contact the client before liquidation — the firm has the right to liquidate margin-deficient accounts without prior notice or client consent
- Overlooking the purpose/non-purpose distinction in SBLOCs — using non-purpose loan proceeds to buy securities violates Regulation U and can result in regulatory action

## Cross-References
- **order-lifecycle** (trading-operations plugin): Margin requirements are checked as part of the order validation and pre-trade process
- **trade-execution** (trading-operations plugin): Forced liquidation requires best execution compliance even under time pressure
- **settlement-clearing** (trading-operations plugin): Margin is settled as part of the trade settlement process; fails can trigger margin obligations
- **lending** (wealth-management plugin): SBLOC products overlap with personal lending analysis; HELOC vs SBLOC comparison
- **liquidity-management** (wealth-management plugin): Margin calls create sudden liquidity demands that must be anticipated in cash flow planning
- **pre-trade-compliance** (trading-operations plugin): Pre-trade margin checks prevent orders that would exceed margin capacity
- **operational-risk** (trading-operations plugin): Margin system failures, forced liquidation errors, and call processing breakdowns are key operational risks
- **counterparty-risk** (trading-operations plugin): Margin lending creates counterparty exposure between the firm and the client
- **investment-suitability** (compliance plugin): Margin accounts and leverage strategies require suitability assessment
- **diversification** (wealth-management plugin): Concentrated position margin requirements reinforce diversification principles

### Referencia: references/examples.md

# Margin Operations — Worked Examples

## Contents

1. Example 1: Calculating margin requirements and buying power for a diversified brokerage account
2. Example 2: Managing a margin call sequence from generation through resolution
3. Example 3: Evaluating portfolio margin benefits for an active options trader

### Example 1: Calculating margin requirements and buying power for a diversified brokerage account

**Given:** A client opens a new margin account and deposits $150,000 in cash. The client wants to build a diversified portfolio.

**Step 1 — Determine Reg T buying power:**
- Cash deposit: $150,000
- SMA: $150,000 (initial cash deposit establishes the SMA)
- Reg T buying power: $150,000 x 2 = **$300,000**

**Step 2 — Client purchases a diversified portfolio:**
- $120,000 in large-cap equity ETF (VTI)
- $60,000 in international equity ETF (VXUS)
- $40,000 in investment-grade bond ETF (BND)
- $30,000 in REIT ETF (VNQ)
- Total purchases: $250,000

**Step 3 — Post-purchase account status:**
- Market value: $250,000
- Debit balance: $250,000 - $150,000 = $100,000
- Account equity: $250,000 - $100,000 = $150,000
- Equity percentage: $150,000 / $250,000 = **60%** (above 50% Reg T requirement)
- Remaining SMA: $150,000 - ($250,000 x 50%) = $150,000 - $125,000 = $25,000
- Remaining buying power: $25,000 x 2 = **$50,000**

**Step 4 — Determine maintenance call trigger (assuming 30% house requirement):**
- House maintenance: 30%
- Call triggered when: equity / market value < 30%
- Equivalently: market value falls to debit balance / (1 - 0.30) = $100,000 / 0.70 = **$142,857**
- This represents a decline of ($250,000 - $142,857) / $250,000 = **42.9%** from current value

**Step 5 — Margin interest cost estimate:**
- Debit balance: $100,000
- Assume margin rate: broker call rate (6.50%, illustrative — actual rates vary with the rate environment) + 0.75% = 7.25%
- Annual interest: $100,000 x 7.25% = $7,250
- Monthly interest: approximately $604
- This cost must be offset by portfolio returns exceeding 7.25% (on the borrowed portion) to add value through leverage

**Step 6 — Impact of a 15% market decline:**
- New market value: $250,000 x 0.85 = $212,500
- Debit balance unchanged: $100,000
- New equity: $212,500 - $100,000 = $112,500
- Equity percentage: $112,500 / $212,500 = **52.9%** (still above 30% house requirement; no margin call)
- New SMA: remains at $25,000 (SMA is a high-water mark; does not decrease with market decline)

### Example 2: Managing a margin call sequence from generation through resolution

**Given:** An existing margin account with the following position prior to market decline:
- Market value: $400,000 (80% equities, 20% bonds)
- Debit balance: $160,000
- Equity: $240,000 (60%)
- House maintenance requirement: 35%

**Days 1-12 — progressive decline, no call:** Equities fall in stages (down 18%, 28%, 35%, then 45% cumulatively from the original $320,000; bonds drift down 5%), taking the equity percentage from 60% to 53.3%, 48.5%, 44.0%, and finally 36.5% on Day 12 — approaching but never breaching the 35% house requirement.

**Day 14 — Call triggered:**
- Equities down 48% total; bonds down 5%
- New equity market value: $320,000 x 0.52 = $166,400
- New bond market value: $76,000
- New total market value: $166,400 + $76,000 = $242,400
- Debit balance: $160,000
- New equity: $242,400 - $160,000 = $82,400
- Equity percentage: $82,400 / $242,400 = **34.0%** — **below 35% house requirement**
- **House margin call generated** at end of day

**Margin call amount calculation:**
- Required equity: 35% x $242,400 = $84,840
- Current equity: $82,400
- **Call amount: $84,840 - $82,400 = $2,440**

**Day 14 — Notification and communication:**
- Automated margin call alert sent via system notification and email
- Margin department places phone call to client
- Notification states: $2,440 due by Day 19 (T+5 business days)
- Options presented: deposit cash, deposit marginable securities (at loan value), or liquidate positions

**Day 16 — Client responds:**
- Client deposits $5,000 cash (exceeds call amount to provide buffer)
- New debit balance: $160,000 - $5,000 = $155,000
- Assuming market unchanged: equity = $242,400 - $155,000 = $87,400
- Equity percentage: $87,400 / $242,400 = **36.1%** (above 35%)
- **Margin call satisfied**

**Alternative resolution — Partial liquidation:**
- If client cannot deposit, sell $7,000 of bond ETF
- Proceeds reduce debit balance: $160,000 - $7,000 = $153,000
- New market value: $242,400 - $7,000 = $235,400
- New equity: $235,400 - $153,000 = $82,400
- Equity percentage: $82,400 / $235,400 = **35.0%** (at the requirement; call met but no buffer)
- Better approach: sell more to create a buffer above the requirement

### Example 3: Evaluating portfolio margin benefits for an active options trader

**Given:** An experienced options trader maintains the following portfolio:
- Account equity: $500,000
- Long 2,000 shares SPY at $450 = $900,000
- Long 20 SPY 420 puts (protective puts, 3-month expiry), premium paid $8 per contract = $16,000
- Short 20 SPY 480 calls (covered calls, 3-month expiry), premium received $5 per contract = $10,000
- Net portfolio delta: reduced from 2,000 to approximately 1,400 (hedged)

**Step 1 — Calculate Reg T margin requirement:**
Under Reg T, margin is calculated position-by-position:
- Long 2,000 shares SPY at $450: 50% initial margin = $450,000
- Long 20 SPY 420 puts: fully paid (no margin required; cost $16,000 already paid)
- Short 20 SPY 480 calls: covered by long shares (no additional margin required)
- **Total Reg T margin requirement: $450,000**
- Account equity: $500,000
- Excess equity: $500,000 - $450,000 = $50,000
- The protective puts and covered calls provide risk reduction, but Reg T does not recognize the hedge

**Step 2 — Calculate portfolio margin requirement:**
Under portfolio margin (OCC TIMS), the entire position is evaluated as a unit under stress scenarios:
- The key stress scenario is SPY -15% (worst case for this long-biased portfolio):
  - SPY drops from $450 to $382.50
  - Long stock loss: 2,000 x ($450 - $382.50) = -$135,000
  - Long 420 puts gain: puts move deep in-the-money; approximate gain: 20 x 100 x ($420 - $382.50 - $8) = +$59,000
  - Short 480 calls gain: calls expire worthless; gain: 20 x 100 x $5 = +$10,000
  - **Net portfolio loss under -15% stress: -$135,000 + $59,000 + $10,000 = -$66,000**
- Additional stress scenarios (+15%, +/-5%, +/-10%) produce smaller losses for this position
- **Portfolio margin requirement: approximately $66,000** (the largest loss across all scenarios)

**Step 3 — Compare Reg T vs portfolio margin:**

| Metric | Reg T | Portfolio Margin |
|--------|-------|-----------------|
| Margin requirement | $450,000 | $66,000 |
| Equity required | $450,000 | $66,000 |
| Excess equity | $50,000 | $434,000 |
| Additional buying power | $100,000 | $868,000 |
| Margin as % of market value | 50% | 7.3% |
| Leverage ratio | 1.8x | 13.6x (available, not necessarily used) |

**Step 4 — Assess the implications:**
- Portfolio margin reduces the requirement by **85%** because it recognizes the protective puts and covered calls as risk-reducing hedges
- The trader can deploy excess capital to additional strategies or maintain a larger cash buffer
- **Risk consideration:** The 13.6x available leverage is dangerous if fully utilized. The trader should maintain a self-imposed margin buffer well above the minimum — targeting no more than 50-60% utilization of portfolio margin capacity
- **Stress test beyond the model:** If SPY gaps down 25% overnight (beyond the 15% stress scenario), the portfolio loss would be approximately $100,000 — still within the $500,000 equity but illustrating that the OCC TIMS scenarios do not capture tail risk. The trader should run their own stress tests at more extreme levels
- **Qualification check:** The account meets the $100,000 minimum equity requirement. The trader must have appropriate options approval and complete the firm's portfolio margin agreement


---

## SKILL: operational-risk

- Fuente: `JoelLewis/finance_skills` → `plugins/trading-operations/skills/operational-risk` (MIT)
- Cuándo usarla: Guide identification, measurement, and management of operational risk in trading and brokerage operations. Use when designing trade error detection and correction procedures, investigating trade breaks and reconciliation failures, classifying loss events under Basel taxonomy, developing key risk indicators (KRIs) and dashboards, responding to system outages or data feed failures or order routing errors, conducting root cause analysis after a trade error or operational incident, planning business continuity and disaster recovery for trading desks, preparing for FINRA or SEC operational risk examinations, or assessing technology risk in OMS and market data systems. Also covers fat-finger errors, error account P&L, and corrective action tracking.

# Operational Risk

## Core Concepts

### Operational Risk Framework
Operational risk is the risk of loss resulting from inadequate or failed internal processes, people, and systems, or from external events. The Basel Committee's seven event-type categories map to trading operations as follows:

| Basel event type | Trading-operations examples |
|---|---|
| 1. Internal fraud | Unauthorized trading, intentional position mismarking, fictitious trade booking, front-running |
| 2. External fraud | Account takeover, phishing for trade credentials, wire fraud in settlement instructions, counterparty manipulation |
| 3. Employment practices and workplace safety | Inadequate operations training, key-person dependency, error-inducing workload |
| 4. Clients, products, and business practices | Suitability failures, improper execution, best execution violations, failure to follow client instructions |
| 5. Damage to physical assets | Data center or trading floor damage from natural disasters or civil disruption |
| 6. Business disruption and system failures | OMS outages, market data feed failures, connectivity loss, exchange gateway and clearing system downtime |
| 7. Execution, delivery, and process management | Trade errors, settlement fails, reconciliation breaks, failed corporate action processing, incorrect margin calculations (typically the largest loss category) |

**Risk identification** involves cataloging all operational risk exposures through process mapping, risk and control self-assessments (RCSAs), loss event analysis, scenario analysis, and audit findings. **Risk assessment** scores each risk on likelihood and impact dimensions, typically using a 5x5 heat map. **Risk monitoring** tracks KRIs, loss events, and control effectiveness. **Risk mitigation** applies controls (preventive and detective), process redesign, technology solutions, insurance, and business continuity planning.

### Trade Errors
A trade error occurs when a transaction is executed incorrectly due to human mistake, system malfunction, or miscommunication. Common trade error types include:

- **Wrong security.** The wrong CUSIP, ISIN, or ticker is entered, resulting in a purchase or sale of an unintended security. Often caused by similar ticker symbols (e.g., entering "AAPL" instead of "APLE") or selecting the wrong line item from a dropdown.
- **Wrong quantity.** The number of shares, bonds, or contracts is incorrect. A frequent subcategory is the "fat finger" error where an extra digit is entered (e.g., 10,000 shares instead of 1,000).
- **Wrong side.** A buy is entered as a sell, or vice versa, resulting in a position that is the opposite of intended. The net exposure error is twice the intended trade size.
- **Wrong account.** The trade is executed in the wrong client account or in the firm's proprietary account instead of a client account. This creates suitability, allocation, and potential conflict-of-interest issues.
- **Duplicate orders.** The same order is submitted more than once due to system timeout and resubmission, double-clicking, or failure of deduplication logic. The firm ends up with twice the intended position.
- **Wrong price type or limit.** A market order is placed instead of a limit order, or the limit price is set incorrectly, resulting in execution at an unintended price.
- **Stale or cancelled order execution.** An order that should have been cancelled is executed because the cancellation was not processed in time or was lost in transit.

**Error detection methods.** Errors are detected through: real-time position monitoring (unexpected position changes trigger alerts), pre-trade validation rules (quantity limits, security restrictions, account eligibility checks), post-trade reconciliation (comparing expected vs. actual positions), client complaints, clearing firm or counterparty rejection notices, and P&L attribution (unexplained P&L often signals an error).

**Error correction procedures.** Once detected, errors must be corrected promptly:

- **Cancel and rebook.** The erroneous trade is cancelled and the correct trade is booked. If the error is caught before settlement, the cancel/rebook may occur on the same trade date. If caught after settlement, an as-of trade is used to adjust the position retroactively.
- **Error account.** Most broker-dealers maintain one or more error accounts (also called difference accounts) where erroneous trades are transferred pending resolution. The error account isolates the incorrect position from client accounts and tracks the resulting P&L. Error account activity is subject to supervisory review and must be documented.
- **Error P&L allocation.** Losses from trade errors are absorbed by the firm and may not be passed to clients. Gains from trade errors present a more nuanced situation — regulatory guidance and firm policy dictate whether the gain reverts to the client's account or remains in the error account. FINRA has stated that firms should not systematically benefit from trade errors at clients' expense.
- **Root cause analysis.** Every trade error should trigger a root cause analysis to determine whether the error was caused by a process deficiency, a technology issue, inadequate training, or an individual's mistake. Root cause findings feed into the operational risk framework's risk identification and mitigation cycle.

### Trade Breaks and Reconciliation
A trade break occurs when two records of the same transaction do not match. Breaks arise at multiple points in the trade lifecycle:

- **Front-to-back breaks.** The order management system (OMS) record does not match the execution management system (EMS) fill, or the trade record in the front-office system does not match the middle-office booking. Causes include partial fills that are not properly aggregated, manual booking errors, and system integration failures.
- **Firm-to-counterparty breaks.** The firm's trade record does not match the counterparty's record. Detected through trade matching and confirmation processes (e.g., DTCC CTM, Omgeo, SWIFT matching). Common causes are quantity discrepancies, price differences (especially for OTC trades with negotiated prices), settlement date mismatches, and incorrect settlement instruction details (SSI mismatches).
- **Firm-to-custodian breaks.** The firm's position records do not match the custodian's records. Detected through daily or intra-day position reconciliation. Causes include unbooked trades, corporate action processing differences, failed settlements not reflected in one system, and timing differences in trade date vs. settlement date accounting.
- **Cash breaks.** The firm's cash ledger does not match the bank or custodian's cash statement. Causes include unbooked cash movements, fee deductions not recorded, interest accrual differences, and foreign exchange conversion discrepancies.

**Reconciliation process.** Firms conduct three primary types of reconciliation:

1. **Position reconciliation.** Compares the firm's securities positions to the custodian's, clearing firm's, or depository's records. Performed daily for actively traded accounts.
2. **Transaction reconciliation.** Matches individual transactions between the firm's records and external records (counterparty confirmations, clearing statements, custodian statements). Ensures every trade is captured in both systems.
3. **Cash reconciliation.** Compares the firm's cash balances and movements to bank and custodian statements. Identifies unrecorded debits, credits, or fee charges.

**Break resolution workflow.** A typical break resolution process includes: (1) automated matching to clear breaks that are within tolerance thresholds (e.g., price differences under $0.01, quantity differences due to rounding); (2) assignment of unresolved breaks to operations analysts; (3) investigation to identify the root cause; (4) correction of the erroneous record in the appropriate system; (5) confirmation with the counterparty or custodian that the break is resolved; (6) documentation of the resolution and root cause.

**Aging and escalation.** Unresolved breaks are tracked by age. Industry standards and regulatory expectations require escalation based on aging thresholds:

| Age | Status | Action |
|---|---|---|
| T+0 to T+1 | Normal | Investigate and resolve in the ordinary course |
| T+2 to T+3 | Attention | Escalate to senior operations staff; increase priority |
| T+4 to T+5 | Warning | Escalate to operations management; engage counterparty directly |
| T+5+ | Critical | Escalate to head of operations and compliance; assess financial exposure |

**Tolerance thresholds.** Firms establish tolerance levels below which breaks are auto-resolved. Common thresholds: price tolerance of +/- $0.01 per unit for exchange-traded securities, quantity tolerance of +/- 1 unit for rounding differences, and cash tolerance of +/- $1.00 for minor rounding. Tolerances must be reviewed periodically and should not be set so wide as to mask genuine errors.

### Loss Event Management
Loss events are actual losses resulting from operational risk incidents. Effective loss event management requires:

**Loss event identification.** Sources include trade error P&L, settlement fail charges (buy-in costs, overdraft interest), regulatory fines and penalties, litigation settlements, system outage costs (missed trades, manual processing costs), and compensation payments to clients for service failures.

**Loss event classification.** Each loss event is classified by:

- **Basel event type** (one of the seven categories above)
- **Business line** (trading desk, operations, technology, compliance)
- **Causal category** (people, process, system, external)
- **Severity** (minor, moderate, significant, major, critical — based on dollar thresholds established by the firm)

**Loss event documentation.** Each event record should include: date of occurrence, date of discovery, date of resolution, description of the event, root cause, Basel category, business line, gross loss amount, recoveries (insurance, counterparty reimbursement), net loss amount, corrective actions taken, and responsible manager.

**Near-miss tracking.** Events that could have resulted in a loss but did not (due to timely detection or favorable market movement) are tracked as near-misses. Near-misses are leading indicators of control weaknesses and are analyzed alongside actual losses. Example: a fat finger error that was caught by a pre-trade quantity limit before execution is a near-miss.

**Loss event database.** Firms maintain an internal loss event database (often part of a GRC — Governance, Risk, and Compliance — platform) that aggregates all loss events across the organization. The database enables trend analysis, root cause pattern identification, and reporting to senior management and the board.

**Threshold reporting.** Firms establish reporting thresholds:

| Threshold | Action |
|---|---|
| > $10,000 | Report to department head within 24 hours |
| > $50,000 | Report to Chief Risk Officer within 24 hours |
| > $100,000 | Report to senior management and Risk Committee |
| > $500,000 | Board notification; assess regulatory reporting obligations |

These thresholds are illustrative; each firm calibrates to its size, complexity, and risk appetite.

**Regulatory notification.** Certain loss events trigger regulatory reporting obligations. FINRA Rule 4530 requires member firms to report specified events, including significant operational incidents. SEC Rule 17a-11 requires broker-dealers to notify the SEC of certain financial and operational conditions. Firms must maintain a matrix mapping loss event types and thresholds to applicable regulatory notification requirements.

### Key Risk Indicators (KRIs)
KRIs are metrics that provide early warning of increasing operational risk exposure. They are distinguished from key performance indicators (KPIs) in that KRIs are specifically designed to signal risk rather than measure performance, though some metrics serve both purposes.

**Leading vs. lagging indicators.** Leading indicators predict future risk events (e.g., rising system latency may predict an outage). Lagging indicators measure events that have already occurred (e.g., number of trade errors last month). An effective KRI program includes both types.

**Common trading operations KRIs:**

| KRI | Definition | Leading/Lagging |
|---|---|---|
| NIGO rate | Not-In-Good-Order rate: percentage of trade instructions received with missing or incorrect information | Leading |
| Trade break rate | Number of unmatched trades as a percentage of total trades | Lagging |
| Settlement fail rate | Number of failed settlements as a percentage of total settlements | Lagging |
| Trade error rate | Number of trade errors per 1,000 trades executed | Lagging |
| Error account balance | Aggregate dollar value of positions in error accounts | Lagging |
| STP rate | Straight-Through Processing rate: percentage of trades processed without manual intervention | Leading |
| System availability | Uptime percentage of critical trading and operations systems | Leading |
| Margin call volume | Number and dollar value of margin calls issued or received | Leading |
| Aged break count | Number of trade breaks older than the escalation threshold | Leading |
| Cancel/correct ratio | Number of trade cancellations and corrections as a percentage of total trades | Lagging |
| Reconciliation completion rate | Percentage of daily reconciliations completed by the target deadline | Leading |
| Open incident count | Number of unresolved operational incidents | Leading |

**KRI thresholds.** Each KRI is assigned threshold levels using a traffic-light model:

- **Green.** Within normal operating range. No action required beyond routine monitoring.
- **Amber.** Approaching risk tolerance. Triggers enhanced monitoring, investigation, and may require management attention. Root cause analysis begins.
- **Red.** Exceeds risk tolerance. Requires immediate management action, escalation to senior management or risk committee, and a documented remediation plan with target dates.

**Example threshold calibration for trade break rate:**

| Level | Threshold | Action |
|---|---|---|
| Green | < 2% of daily trade volume | Routine monitoring |
| Amber | 2% - 5% of daily trade volume | Investigate root cause; increase reconciliation frequency |
| Red | > 5% of daily trade volume | Escalate to Head of Operations; halt new activity if warranted |

**KRI trending and reporting.** KRIs are tracked over time to identify trends. A KRI that remains in the green zone but is trending upward toward amber is more informative than a snapshot reading. Monthly KRI reports to management should include current values, threshold status, trend direction, and commentary on any amber or red indicators.

### Incident Management
Operational incidents in trading operations range from minor system glitches to major outages that affect market participation. A structured incident management process ensures consistent response and resolution.

**Incident classification (severity levels):**

| Severity | Definition | Examples | Response Time |
|---|---|---|---|
| SEV-1 (Critical) | Complete loss of trading capability or significant financial exposure | Order management system down; inability to route orders to any exchange; clearing system failure preventing settlement | Immediate; all-hands response |
| SEV-2 (Major) | Significant degradation of trading capability or material financial risk | Market data feed failure for a major exchange; inability to process a specific order type; partial connectivity loss | Within 15 minutes |
| SEV-3 (Moderate) | Limited impact on trading operations; workaround available | Slow system performance; failure of a non-critical reporting function; single counterparty connectivity issue | Within 1 hour |
| SEV-4 (Minor) | Minimal operational impact; no financial exposure | Cosmetic UI issues; non-urgent report delays; minor data quality issues with no trade impact | Within 4 hours |

**Incident response procedures.** A standard incident lifecycle includes:

1. **Detection and reporting.** Incidents are detected through monitoring alerts, user reports, counterparty notifications, or automated health checks.
2. **Triage and classification.** The incident is assessed for severity, scope, and potential financial impact. A severity level is assigned.
3. **Communication.** Stakeholders are notified according to the communication protocol. For SEV-1 and SEV-2, this includes trading desk heads, operations management, technology leadership, compliance, and senior management. A designated incident commander coordinates the response.
4. **Containment.** Immediate actions to prevent the incident from expanding. This may include halting automated trading, switching to manual order entry, activating backup systems, or notifying exchanges and counterparties.
5. **Resolution.** Technical teams work to restore normal operations. For system outages, this involves failover to backup systems, restarting services, or deploying emergency patches.
6. **Recovery.** After the root cause is addressed, normal operations resume. Outstanding orders, trades, and positions are reconciled. Any trades missed during the outage are evaluated for client impact.
7. **Post-incident review.** A formal review is conducted to document root cause, timeline, impact, response effectiveness, and corrective actions.

**Escalation matrix.** The escalation path is defined by severity level:

- SEV-1: Incident Commander, CTO/COO, Head of Trading, Chief Risk Officer, CEO (if market-wide impact)
- SEV-2: Incident Commander, VP of Technology, Head of Trading Operations, Chief Risk Officer
- SEV-3: Technology team lead, Operations manager
- SEV-4: Individual contributor, supervisor

**Root cause analysis techniques.** Two widely used methods:

- **5 Whys.** Iteratively ask "why" until the root cause is identified. Example: Why did the trade error occur? Because the wrong account was selected. Why? Because the account dropdown displayed similar names. Why? Because the UI does not show account numbers alongside names. Why? Because the account display format was never updated after the firm acquired new clients. Root cause: inadequate UI design compounded by post-acquisition system integration gaps.
- **Fishbone (Ishikawa) diagram.** Categorizes potential causes into six branches: People, Process, Technology, Data, Environment, and External. Each branch is explored to identify contributing factors.

**Corrective action tracking.** Every root cause analysis produces corrective actions. Each action is assigned an owner, a target completion date, and a status (open, in progress, completed, verified). A corrective action register is maintained and reviewed at regular operational risk meetings. Corrective actions are not considered closed until they have been independently verified as effective.

### Business Continuity and Disaster Recovery
Trading operations must maintain the ability to continue critical functions during disruptive events. Regulatory requirements (including FINRA Rule 4370) mandate business continuity planning for broker-dealers.

**FINRA Rule 4370 (Business Continuity Plans and Emergency Contact Information).** Every FINRA member must create and maintain a written business continuity plan (BCP) that addresses, at a minimum: data backup and recovery, all mission-critical systems, financial and operational assessments, alternate communications with customers and regulators, alternate physical location, critical business constituent impact, regulatory reporting, and communications with regulators. The plan must be updated in the event of any material change to the firm's operations, structure, business, or location.

**Recovery Time Objective (RTO).** The maximum acceptable duration of a system outage before the business impact becomes unacceptable. For trading operations, RTOs are typically measured in minutes to hours:

| System | Typical RTO |
|---|---|
| Order management system | < 30 minutes |
| Market data feeds | < 15 minutes |
| Exchange connectivity | < 15 minutes |
| Risk management system | < 1 hour |
| Settlement/clearing interface | < 2 hours |
| Client reporting systems | < 4 hours |

**Recovery Point Objective (RPO).** The maximum acceptable amount of data loss measured in time. An RPO of 5 minutes means the firm can tolerate losing at most 5 minutes of transaction data. For trading systems, RPOs are typically near-zero (synchronous replication) for order and execution data, and minutes for less critical data.

**Failover procedures.** Critical systems should have automated or semi-automated failover to secondary environments. This includes: active-passive database replication with automated promotion of the standby, redundant network paths to exchanges and clearing firms, geographically separated data centers, and pre-configured disaster recovery trading environments.

**Remote trading capabilities.** Firms must ensure that traders and operations staff can operate from alternate locations. This includes: VPN access to trading systems, pre-provisioned remote trading workstations, tested voice communication (trading turrets, recorded phone lines) from remote locations, and documented procedures for activating remote trading.

**Communication plans.** During a disruption, the firm must communicate with: clients (regarding order status, account access, and alternate contact methods), regulators (FINRA, SEC, exchanges), counterparties and clearing firms, employees, and critical vendors. Contact trees and communication templates should be pre-established and tested.

**Testing requirements.** FINRA Rule 4370 requires that BCPs be reviewed and tested at least annually. Industry best practice includes: tabletop exercises (walkthrough of scenarios), functional testing of backup systems and failover, full-scale simulation exercises, and third-party testing with exchanges and clearing firms. Test results should be documented and deficiencies addressed through corrective actions.

### Technology Risk
Technology risk is a subset of operational risk that is particularly acute in trading operations due to the dependence on automated systems for order routing, execution, risk management, and settlement processing.

**System reliability.** Trading systems must meet high availability standards. Common targets are 99.95% uptime (approximately 4.4 hours of allowable downtime per year) for mission-critical systems. Reliability is achieved through redundant architecture, automated monitoring, capacity planning, and regular performance testing.

**Change management.** Software and configuration changes to trading systems are a leading source of operational incidents. A disciplined change management process includes: change request documentation, impact assessment, testing in non-production environments, scheduled deployment windows (avoiding market hours for high-risk changes), rollback procedures, and post-deployment verification. Emergency changes during market hours require expedited approval with heightened risk awareness.

**Vendor risk management.** Trading operations depend on numerous third-party vendors for market data, order routing, clearing, settlement, and technology infrastructure. Vendor risk management includes: due diligence before onboarding, service level agreements (SLAs) with measurable performance standards, ongoing monitoring of vendor performance and financial health, contingency plans for vendor failure, and concentration risk assessment (avoiding excessive dependence on a single vendor for critical functions).

**Cybersecurity in trading systems.** Trading systems are high-value targets for cyberattack. Key cybersecurity controls include: network segmentation to isolate trading systems, multi-factor authentication for system access, encryption of data in transit and at rest, intrusion detection and prevention systems, regular penetration testing, and incident response plans specific to cyber events.

**Market data system failures.** Loss of market data (prices, quotes, reference data) can prevent accurate order pricing, risk calculation, and compliance checking. Firms should maintain: redundant market data feeds from multiple vendors, fallback pricing mechanisms (last known price, manual price entry with controls), and alerts for stale or missing data. Market data failures that affect order routing or execution quality should be classified and managed as operational incidents.

**Order routing system failures.** Inability to route orders to exchanges or market centers is a SEV-1 incident for a trading operation. Controls include: redundant FIX connections to each execution venue, alternative order routing paths, manual order entry capabilities at exchange terminals as a last resort, and pre-established procedures for notifying clients of execution delays.

## Worked Examples

Three worked examples are in [references/examples.md](references/examples.md) — load for an end-to-end scenario: (1) building an operational risk framework for a broker-dealer's trading desks, (2) designing a standardized trade error handling and correction process, (3) implementing a KRI dashboard for trading operations management.

## Common Pitfalls
- Treating operational risk management as a compliance exercise rather than a business management discipline — forms are completed but risks are not actively managed or mitigated.
- Failing to track near-misses alongside actual losses, thereby missing early warning signals of deteriorating controls.
- Setting KRI thresholds based on aspiration rather than data — thresholds that are perpetually in the red lose credibility and are ignored by management.
- Allowing trade error corrections without documentation, creating invisible risk exposure and preventing root cause analysis.
- Under-investing in reconciliation processes — aged breaks are a leading indicator of operational failures and potential financial losses, yet break resolution is often deprioritized relative to new trade processing.
- Relying solely on end-of-day reconciliation when intra-day position monitoring would detect errors hours earlier and reduce the P&L impact.
- Conducting business continuity plan testing as a check-the-box exercise without realistic scenarios, thereby failing to identify actual recovery gaps.
- Ignoring technology change management as a source of operational risk — a disproportionate share of major incidents originates from software deployments and configuration changes.
- Failing to establish clear escalation matrices, resulting in ad hoc responses to incidents that vary depending on who happens to be on duty.
- Classifying all operational risk events under a single category rather than using the Basel taxonomy, which prevents meaningful trend analysis and benchmarking.
- Overlooking vendor concentration risk — a single vendor failure affecting market data, order routing, or clearing can be a firm-wide operational risk event.
- Not closing the loop on corrective actions — root cause analyses produce recommendations, but without tracking and verification, the same failures recur.

## Cross-References
- **order-lifecycle** (trading-operations plugin): The order lifecycle from order entry through execution is where many operational risk events originate; error detection and prevention are embedded at each stage.
- **settlement-clearing** (trading-operations plugin): Settlement fails and clearing breaks are a primary operational risk category; settlement fail management processes are closely linked to the operational risk framework.
- **counterparty-risk** (trading-operations plugin): Counterparty failures (failure to deliver securities or pay cash) are an external operational risk that intersects with credit risk management.
- **trade-execution** (trading-operations plugin): Execution quality failures, routing errors, and best execution violations are operational risk events with regulatory implications.
- **pre-trade-compliance** (trading-operations plugin): Pre-trade checks serve as preventive controls against trade errors, unauthorized trading, and account restriction violations.
- **post-trade-compliance** (trading-operations plugin): Post-trade surveillance detects errors and anomalies that escaped pre-trade controls.
- **books-and-records** (compliance plugin): Loss event documentation, incident records, and error account activity are regulatory books and records subject to retention requirements.
- **examination-readiness** (compliance plugin): Operational risk frameworks, incident logs, and BCP documentation are common examination topics for FINRA and SEC examiners.
- **privacy-data-security** (compliance plugin): Cybersecurity incidents affecting trading systems are operational risk events that also trigger data protection and breach notification obligations.

### Referencia: references/examples.md

# Operational Risk — Worked Examples

## Contents

1. Example 1: Building an Operational Risk Framework for a Broker-Dealer's Trading Desk
2. Example 2: Designing a Trade Error Handling and Correction Process
3. Example 3: Implementing a KRI Dashboard for Trading Operations Management

### Example 1: Building an Operational Risk Framework for a Broker-Dealer's Trading Desk

**Scenario.** A mid-size broker-dealer executes approximately 15,000 equity trades per day across four trading desks (institutional agency, retail, proprietary, and electronic market-making). The firm has experienced a rising number of trade errors and settlement fails over the past six months. The Chief Risk Officer has asked the operations team to design a formal operational risk framework for the trading desks.

**Step 1 — Risk identification.** The team conducts a risk and control self-assessment (RCSA) for each desk. The process involves structured interviews with desk heads, operations managers, and technology leads. They also review the past 12 months of trade errors, settlement fails, system incidents, and client complaints. The RCSA identifies the following top risks:

- Fat finger errors on the proprietary desk (no pre-trade quantity limits)
- Settlement fails on institutional trades due to SSI mismatches (clients providing incorrect settlement instructions)
- Market data feed interruptions causing stale pricing on the electronic market-making desk
- Key-person dependency in the operations team (one senior analyst handles all corporate action processing)
- Duplicate order submissions on the retail platform during peak volume periods

**Step 2 — Risk assessment.** Each risk is scored on a 5x5 likelihood-impact matrix. Likelihood scale: 1 (rare) to 5 (almost certain). Impact scale: 1 (negligible, under $10K) to 5 (severe, over $500K). The team plots risks on a heat map.

| Risk | Likelihood | Impact | Score | Priority |
|---|---|---|---|---|
| Fat finger errors | 4 | 4 | 16 | High |
| SSI mismatch settlement fails | 3 | 3 | 9 | Medium |
| Market data interruptions | 2 | 5 | 10 | High |
| Key-person dependency | 3 | 4 | 12 | High |
| Duplicate order submissions | 3 | 2 | 6 | Medium |

**Step 3 — Control design.** For each high-priority risk, the team designs preventive and detective controls:

- **Fat finger errors:** Implement pre-trade quantity limits (hard block at 10x normal order size, soft warning at 3x). Add a four-eyes confirmation requirement for orders exceeding $1 million notional.
- **Market data interruptions:** Deploy a secondary market data feed from an alternative vendor. Implement stale data detection (alert if a quote has not updated in 5 seconds during market hours). Define fallback pricing procedures.
- **Key-person dependency:** Cross-train two additional analysts on corporate action processing. Document all corporate action procedures. Implement a buddy system for coverage during absences.

**Step 4 — KRI dashboard.** The team establishes KRIs with thresholds:

- Trade error rate: Green < 0.5 per 1,000 trades; Amber 0.5-1.0; Red > 1.0
- Settlement fail rate: Green < 1%; Amber 1-3%; Red > 3%
- System availability (OMS): Green > 99.95%; Amber 99.9-99.95%; Red < 99.9%
- Aged breaks (> T+3): Green < 10; Amber 10-25; Red > 25

**Step 5 — Loss event tracking.** The team implements a loss event register in the firm's GRC platform. All trade errors with P&L impact above $1,000 are logged, classified by Basel category, and reviewed monthly by the operational risk committee.

**Step 6 — Governance.** A monthly Operational Risk Committee meeting is established, chaired by the CRO, with attendance from heads of trading, operations, technology, and compliance. The meeting reviews the KRI dashboard, loss event trends, open incidents, and corrective action status.

**Outcome.** Over six months, the framework reduces trade errors by 40% (driven primarily by the pre-trade quantity limits) and settlement fails by 25% (driven by SSI validation improvements). The KRI dashboard provides management with a single view of operational risk across all desks.

### Example 2: Designing a Trade Error Handling and Correction Process

**Scenario.** A broker-dealer's compliance team has found that trade errors are handled inconsistently across desks. Some traders correct errors informally without documentation, while others escalate every error regardless of materiality. The firm needs a standardized trade error handling process.

**Step 1 — Error detection.** The firm implements multiple detection layers:

- **Pre-trade checks.** The OMS validates every order against configurable rules: security eligibility (is the security tradeable in this account?), quantity limits (is the order size within bounds?), account restrictions (is the account frozen or restricted?), and duplicate order detection (was an identical order submitted in the last 60 seconds?). Orders that fail pre-trade checks are blocked with an explanatory message.
- **Real-time position monitoring.** The operations team monitors intra-day position changes. Alerts fire when a position moves by more than a configurable threshold (e.g., a new position appears in an account, or a position changes by more than 50% in a single trade).
- **Post-trade reconciliation.** End-of-day reconciliation between the OMS and the clearing firm identifies any discrepancies in positions, trade details, or settlement instructions.

**Step 2 — Error classification.** When an error is detected, it is classified by type and severity:

| Severity | Criteria | Examples |
|---|---|---|
| Level 1 (Minor) | Estimated P&L impact < $5,000; no client impact; easily correctable | Small quantity overfill; minor price improvement on error |
| Level 2 (Moderate) | Estimated P&L impact $5,000-$50,000; client notified; correction required | Wrong account allocation; moderate fat finger error |
| Level 3 (Major) | Estimated P&L impact > $50,000; significant client or market impact | Wrong-side trade; large unauthorized position; error affecting multiple clients |

**Step 3 — Error correction workflow.**

1. **Immediate containment.** The trader or operations analyst immediately assesses whether additional market exposure needs to be neutralized. For wrong-side errors, the offsetting trade is executed as soon as possible to limit further P&L impact.
2. **Error account transfer.** The erroneous trade is moved to the firm's designated error account. The correct trade (if any) is booked to the client's account at the originally intended terms.
3. **Documentation.** An error ticket is created in the operations workflow system. The ticket records: date and time of the error, date and time of detection, the erroneous trade details, the correct trade details, the root cause, the estimated P&L impact, and the corrective actions taken.
4. **Supervisory review.** All errors are reviewed by a supervisor. Level 2 and Level 3 errors require review by the desk head and the compliance department. Level 3 errors are reported to the CRO.
5. **Client communication.** If the error affected a client's account (even briefly), the client is notified of the error and the correction. The notification includes a description of what happened and confirmation that the client's account has been restored to the correct position.
6. **P&L resolution.** Error losses are absorbed by the firm in the error account. Error gains are evaluated on a case-by-case basis; the firm's policy should address whether gains are returned to the client or retained. Best practice is to return gains that would have accrued to the client absent the error.

**Step 4 — Root cause analysis and corrective actions.** Every error undergoes root cause analysis proportional to its severity. Level 1 errors receive a brief written explanation. Level 2 and Level 3 errors receive a formal root cause analysis using the 5 Whys method. Corrective actions are tracked in the operational risk register. Recurring root causes trigger process or system changes.

**Step 5 — Reporting.** A monthly error report is produced for management, summarizing: total errors by desk, error rate per 1,000 trades, total error P&L (gross loss, recovery, net), root cause breakdown (people, process, system, external), and trend analysis. The report highlights any recurring root causes and the status of corrective actions.

**Outcome.** The standardized process ensures every error is captured, documented, and analyzed. Management gains visibility into error trends and can allocate resources to the highest-impact corrective actions.

### Example 3: Implementing a KRI Dashboard for Trading Operations Management

**Scenario.** A broker-dealer's Head of Operations wants a consolidated dashboard that provides a daily view of operational risk across the firm's trading operations. The dashboard must be actionable — it should highlight areas requiring immediate attention and enable drill-down into underlying data.

**Step 1 — KRI selection.** The team selects 10 KRIs from the standard trading-operations KRI set in the skill's Core Concepts table (trade error rate, settlement fail rate, trade break rate, aged breaks, error account balance, STP rate, OMS availability, margin call exceptions, cancel/correct ratio, NIGO rate) based on relevance, measurability, and alignment with the firm's risk appetite.

**Step 2 — Threshold calibration.** For each KRI, green/amber/red thresholds are set using a combination of historical performance (baseline from the prior 12 months), peer benchmarks (industry surveys and clearing firm data), and risk appetite (approved by the Risk Committee), following the traffic-light model in Core Concepts. Calibrations are firm-specific — for example, this firm sets the error account balance amber at $50K and red at $200K, and OMS availability amber below 99.95%.

**Step 3 — Data sourcing and automation.** Each KRI is mapped to a data source:

- Trade error rate: sourced from the error ticketing system
- Settlement fail rate: sourced from the clearing firm's daily settlement report
- Trade break rate: sourced from the reconciliation platform
- OMS availability: sourced from the technology monitoring system
- STP rate: calculated from the OMS (trades requiring manual intervention flagged by exception code)

Data feeds are automated where possible. Manual data entry is limited to KRIs where automated sourcing is not yet available (e.g., NIGO rate may require manual classification initially).

**Step 4 — Dashboard design.** The dashboard displays:

- A summary panel showing all 10 KRIs with current status (green/amber/red) and trend arrows (improving, stable, deteriorating)
- A time-series chart for each KRI showing the trailing 30 days of values with threshold bands
- A drill-down capability: clicking on a red or amber KRI shows the underlying data (individual breaks, errors, or incidents contributing to the metric)
- A commentary section where the operations team records explanations for any amber or red indicators

**Step 5 — Governance and response protocol.** The dashboard is reviewed daily by the Head of Operations and weekly by the Operational Risk Committee. Response protocol:

- Any KRI moving from green to amber triggers an investigation by the responsible team within 24 hours. Findings are documented in the commentary section.
- Any KRI in red triggers an immediate escalation to the CRO and a mandatory corrective action plan within 48 hours.
- KRIs that remain in amber for more than 5 consecutive business days are auto-escalated to red status.
- Monthly trend reports are presented to the Risk Committee with analysis of systemic patterns.

**Outcome.** The dashboard provides a single source of truth for operational risk status. Early detection through leading indicators (STP rate, NIGO rate, aged breaks) enables the operations team to intervene before minor issues escalate into material losses. Over three months of use, the average time to detect and resolve operational issues decreases by 35%.


---

## SKILL: performance-attribution

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/performance-attribution` (MIT)
- Cuándo usarla: Decompose portfolio returns into explainable components to identify where value was added or lost. Use when the user asks about Brinson attribution, allocation vs selection effects, factor-based attribution, fixed-income attribution, or currency attribution. Also trigger when users mention 'what drove my returns', 'was it stock picking or sector bets', 'alpha decomposition', 'multi-period linking', 'interaction effect', 'active return breakdown', or ask why their portfolio outperformed or underperformed the benchmark.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/wealth-management/skills/performance-attribution/` (performance_attribution.py)

# Performance Attribution

## Core Concepts

### Brinson-Fachler Attribution (Single Period)
The classic equity attribution model decomposes active return (portfolio return minus benchmark return) into three effects:

- **Allocation effect:** Value added by over/underweighting sectors relative to the benchmark
  - A_i = (w_p,i - w_b,i) × (R_b,i - R_b)
  - Rewards overweighting sectors that outperform the total benchmark
- **Selection effect:** Value added by picking better securities within each sector
  - S_i = w_b,i × (R_p,i - R_b,i)
  - Rewards outperforming the sector benchmark regardless of weight
- **Interaction effect:** Combined effect of both overweighting and outperforming (or vice versa)
  - I_i = (w_p,i - w_b,i) × (R_p,i - R_b,i)
  - Captures the joint benefit of overweighting a sector AND selecting better securities in it
- **Total active return:** R_p - R_b = Σ A_i + Σ S_i + Σ I_i

Where: w_p,i = portfolio weight in sector i, w_b,i = benchmark weight in sector i, R_p,i = portfolio return in sector i, R_b,i = benchmark return in sector i, R_b = total benchmark return.

### Multi-Period Attribution
Single-period attribution does not compound across periods. Geometric linking methods are required:

- **Carino method:** Applies a smoothing factor to make arithmetic effects compound to the correct geometric total
- **Menchero method:** Uses a logarithmic approach for smoother decomposition
- **GRAP (Geometric Return Attribution Program):** Converts arithmetic effects to geometric equivalents
- Key principle: the sum of linked attribution effects must equal the total geometric active return over the full period

### Factor-Based Attribution
Decomposes returns into exposures to systematic risk factors:

- **Model:** R_p = Σ β_k × F_k + α
  - β_k = portfolio's exposure (loading) to factor k
  - F_k = return of factor k during the period
  - α = residual return unexplained by factors (true alpha)
- **Common factors:** Market (MKT), Size (SMB), Value (HML), Momentum (UMD), Quality (QMJ), Low Volatility (BAB)
- **Factor contribution:** β_k × F_k for each factor
- **Active factor contribution:** (β_p,k - β_b,k) × F_k
- The model chosen (Fama-French 3, Carhart 4, Fama-French 5, Barra, Axioma) affects results

### Fixed-Income Attribution
Decomposes bond portfolio returns into component sources:

- **Yield return (income):** Coupon income accrued during the period (yield × time)
- **Roll return:** Price appreciation as bonds "roll down" the yield curve toward maturity
- **Curve change return:** Impact of parallel and non-parallel yield curve shifts
  - Duration effect: -D × Δy (parallel shift)
  - Curve reshaping: key rate duration contributions
- **Spread change return:** Impact of credit spread changes: -spread_duration × Δspread
- **Credit/default return:** Losses from defaults or credit events
- **Residual:** Unexplained return (convexity effects, model error)

### Currency Attribution
For international portfolios, returns decompose into:

- **Local return:** Return of the asset in its local currency
- **Currency return:** Gain/loss from exchange rate movements
- **Cross-product:** Interaction between local return and currency return
- **Total return (base currency):** R_base ≈ R_local + R_currency + R_local × R_currency
- **Hedged return:** Local return + hedge cost (forward premium/discount)
- Attribution of active currency decisions: actual currency exposure vs benchmark currency exposure

### Holdings-Based vs Returns-Based Attribution
- **Holdings-based:** Uses actual portfolio positions; more accurate but requires detailed holdings data at each evaluation point
- **Returns-based (style analysis):** Regresses portfolio returns against a set of style indices (e.g., Sharpe style analysis); less precise but requires only return series
- **Transaction-based:** Most accurate; accounts for intra-period trading by using actual transaction records

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Allocation effect (sector i) | A_i = (w_p,i - w_b,i) × (R_b,i - R_b) | Sector weighting decisions |
| Selection effect (sector i) | S_i = w_b,i × (R_p,i - R_b,i) | Security selection within sector |
| Interaction effect (sector i) | I_i = (w_p,i - w_b,i) × (R_p,i - R_b,i) | Joint allocation-selection effect |
| Total active return | R_p - R_b = Σ(A_i + S_i + I_i) | Sum of all effects equals active return |
| Factor return contribution | C_k = β_k × F_k | Return from factor k exposure |
| Duration effect | ΔP/P ≈ -D × Δy | Bond price change from yield shift |
| Currency return | R_fx = (S_end - S_start) / S_start | Exchange rate impact |

## Worked Examples

### Example 1: Brinson-Fachler equity attribution
**Given:** Two-sector portfolio (Tech and Healthcare). Portfolio: 35% Tech (returned 15%), 65% Healthcare (returned 8%). Benchmark: 25% Tech (returned 12%), 75% Healthcare (returned 6%). Total benchmark return: 0.25×12% + 0.75×6% = 7.5%.
**Calculate:** Allocation, selection, and interaction effects for each sector, and total active return.
**Solution:**
1. **Total portfolio return:** 0.35×15% + 0.65×8% = 5.25% + 5.20% = 10.45%.
2. **Total active return:** 10.45% - 7.50% = **2.95%**.
3. **Tech allocation effect:** (0.35 - 0.25) × (12% - 7.5%) = 0.10 × 4.5% = **+0.45%** (overweight a sector that beat the benchmark).
4. **Tech selection effect:** 0.25 × (15% - 12%) = 0.25 × 3% = **+0.75%** (stock picks in Tech beat Tech benchmark).
5. **Tech interaction effect:** (0.35 - 0.25) × (15% - 12%) = 0.10 × 3% = **+0.30%** (overweight AND outperformed).
6. **Healthcare allocation effect:** (0.65 - 0.75) × (6% - 7.5%) = -0.10 × -1.5% = **+0.15%** (underweight a sector that lagged the benchmark).
7. **Healthcare selection effect:** 0.75 × (8% - 6%) = 0.75 × 2% = **+1.50%** (stock picks in Healthcare beat Healthcare benchmark).
8. **Healthcare interaction effect:** (0.65 - 0.75) × (8% - 6%) = -0.10 × 2% = **-0.20%** (underweight but outperformed — interaction is negative).
9. **Totals:** Allocation = 0.45 + 0.15 = **0.60%**. Selection = 0.75 + 1.50 = **2.25%**. Interaction = 0.30 + (-0.20) = **0.10%**. Sum = 0.60 + 2.25 + 0.10 = **2.95%** ✓.

### Example 2: Factor-based attribution
**Given:** A fund has factor loadings: β_mkt = 1.1, β_smb = 0.3, β_hml = -0.2. During the period: MKT = 5%, SMB = 2%, HML = -1%. Risk-free rate = 1%. Fund excess return = 7%.
**Calculate:** Factor contributions and alpha.
**Solution:**
1. **Market contribution:** 1.1 × 5% = **5.50%**.
2. **Size (SMB) contribution:** 0.3 × 2% = **0.60%**.
3. **Value (HML) contribution:** -0.2 × (-1%) = **+0.20%**.
4. **Total factor-explained return:** 5.50 + 0.60 + 0.20 = **6.30%**.
5. **Alpha (residual):** 7.00% - 6.30% = **+0.70%**.
6. **Interpretation:** The fund's excess return of 7% is mostly explained by above-market beta (5.5%) and a small-cap tilt (0.6%). The negative value loading helped (+0.2%) as value underperformed. After accounting for all factors, the manager generated 0.70% of true alpha.

## Common Pitfalls
- Interaction effect is hard to interpret — some attribution models fold it into allocation or selection, which changes reported results significantly
- Multi-period attribution requires geometric linking — simple arithmetic attribution does not compound correctly and residuals grow over time
- Returns-based attribution (style analysis) may not reflect actual holdings, especially for managers who trade actively or change style
- Factor attribution results depend heavily on the chosen factor model — different models yield different alpha estimates
- Currency attribution is often overlooked in international portfolios, hiding or inflating apparent skill
- Survivorship bias in manager evaluation: only surviving funds are analyzed, overstating average skill
- Confusing gross-of-fee and net-of-fee returns when comparing to benchmarks
- Using inappropriate benchmarks that do not match the portfolio's investment universe

## Cross-References
- **investment-policy** (wealth-management plugin): Benchmark selection in IPS directly feeds performance attribution analysis
- **tax-efficiency** (wealth-management plugin): After-tax attribution requires adjusting returns for tax impact
- **savings-goals** (wealth-management plugin): Attribution helps assess whether investment strategy is on track to meet goals
- **liquidity-management** (wealth-management plugin): Cash drag from liquidity reserves affects portfolio-level attribution
- **client-review-prep** (advisory-practice plugin): attribution analysis highlights are key talking points in client review meetings
- **tax-loss-harvesting** (wealth-management plugin): tax alpha from TLH should be tracked and attributed separately

## Running the script
Run with `uv run scripts/performance_attribution.py` (the PEP 723 header resolves numpy automatically) or with `python3 scripts/performance_attribution.py` after `pip install numpy scipy`. A bare run prints three demos: the Brinson-Fachler attribution from Worked Example 1, an OLS factor attribution on seeded synthetic data, and Carino multi-period linking. Use `--verify` to assert outputs match this skill's worked example numbers (exit code 0 on PASS) and `--help` for an overview of the classes. The file is primarily meant to be imported as a module (e.g., `from performance_attribution import BrinsonFachler`).


---

## SKILL: performance-metrics

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/performance-metrics` (MIT)
- Cuándo usarla: Evaluate investment performance on a risk-adjusted basis using industry-standard ratios and capture analysis. Use when the user asks about Sharpe ratio, Sortino ratio, Information Ratio, Treynor ratio, Calmar ratio, Omega ratio, or upside/downside capture. Also trigger when users mention 'risk-adjusted returns', 'return per unit of risk', 'M-squared', 'is this fund worth the volatility', 'how to compare two managers', 'capture ratio', or ask which investment performed better after accounting for risk.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/wealth-management/skills/performance-metrics/` (performance_metrics.py)

# Performance Metrics

## Core Concepts

### Sharpe Ratio
The most widely used risk-adjusted performance measure. It divides excess return (over the risk-free rate) by total volatility.

```
SR = (R_p - R_f) / sigma_p
```

- R_p: annualized portfolio return
- R_f: annualized risk-free rate
- sigma_p: annualized portfolio volatility (standard deviation of returns)

A higher Sharpe ratio indicates more return per unit of total risk. Typical benchmarks: SR < 0.5 is poor, 0.5-1.0 is acceptable, > 1.0 is strong, > 2.0 is exceptional.

**Annualization:** If computed from monthly data, SR_annual = SR_monthly * sqrt(12).

### Sortino Ratio
Replaces total volatility with downside deviation, penalizing only harmful volatility (returns below a Minimum Acceptable Return).

```
Sortino = (R_p - R_f) / sigma_downside
```

where sigma_downside = sqrt((1/n) * sum(min(R_i - MAR, 0)^2)).

Common MAR choices: 0%, risk-free rate, or a target return. Always state which MAR is used, and use the same reference point in the numerator as in the downside deviation: if the MAR is not the risk-free rate, the numerator should be (R_p - MAR), not (R_p - R_f). Mixing reference points makes the ratio internally inconsistent.

### Information Ratio
Measures active return (alpha) per unit of active risk (tracking error) relative to a benchmark.

```
IR = (R_p - R_b) / TE
```

where TE = std(R_p - R_b) * sqrt(N).

An IR above 0.5 is generally considered good; above 1.0 is exceptional and difficult to sustain.

### Treynor Ratio
Measures excess return per unit of systematic risk (beta) rather than total risk.

```
Treynor = (R_p - R_f) / beta_p
```

Useful for evaluating diversified portfolios where idiosyncratic risk has been diversified away. For undiversified holdings, the Sharpe ratio is more appropriate.

### Calmar Ratio
Relates annualized return to the worst peak-to-trough drawdown.

```
Calmar = CAGR / |MaxDrawdown|
```

A Calmar ratio above 1.0 means the annualized return exceeds the maximum drawdown. This ratio is popular among CTAs and hedge fund investors. Typically computed over a 3-year window.

### Omega Ratio
A gain-loss ratio that considers the entire return distribution above and below a threshold tau.

```
Omega(tau) = integral from tau to +inf of [1 - F(r)] dr
             / integral from -inf to tau of F(r) dr
```

where F(r) is the cumulative distribution function of returns.

In practice, this is computed as:

```
Omega(tau) = sum(max(R_i - tau, 0)) / sum(max(tau - R_i, 0))
```

Omega > 1 means expected gains above tau exceed expected losses below tau. Unlike Sharpe, Omega captures the full shape of the distribution (skewness, kurtosis).

### Upside and Downside Capture Ratios
Measure how the portfolio participates in benchmark up and down markets.

```
Up Capture   = R_p(in up months) / R_b(in up months) * 100
Down Capture = R_p(in down months) / R_b(in down months) * 100
Capture Ratio = Up Capture / Down Capture
```

Ideal profile: Up Capture > 100% and Down Capture < 100%, yielding a Capture Ratio > 1. "Up months" and "down months" are defined by the benchmark return being positive or negative, respectively.

### M-Squared (Modigliani-Modigliani)
Expresses risk-adjusted return in the same units as return, by leveraging or deleveraging the portfolio to match benchmark volatility.

```
M^2 = R_f + SR_p * sigma_b
    = R_f + ((R_p - R_f) / sigma_p) * sigma_b
```

Interpretation: "If this portfolio were scaled to have the same volatility as the benchmark, it would have returned M-squared." This makes it directly comparable to benchmark returns.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Sharpe Ratio | (R_p - R_f) / sigma_p | Return per unit of total risk |
| Sortino Ratio | (R_p - R_f) / sigma_downside | Return per unit of downside risk |
| Information Ratio | (R_p - R_b) / TE | Active return per unit of active risk |
| Treynor Ratio | (R_p - R_f) / beta_p | Return per unit of systematic risk |
| Calmar Ratio | CAGR / |MaxDD| | Return per unit of drawdown risk |
| Omega Ratio | sum(max(R_i - tau, 0)) / sum(max(tau - R_i, 0)) | Full-distribution gain-loss ratio |
| Up Capture | R_p(up) / R_b(up) * 100 | Participation in rising markets |
| Down Capture | R_p(down) / R_b(down) * 100 | Participation in falling markets |
| M-Squared | R_f + SR_p * sigma_b | Risk-adjusted return in return units |

## Worked Examples

### Example 1: Sharpe Ratio Calculation
**Given:** A fund returned 12% annualized, the risk-free rate is 4%, and the fund's annualized volatility is 15%.

**Calculate:** Sharpe Ratio.

**Solution:**

```
SR = (0.12 - 0.04) / 0.15
   = 0.08 / 0.15
   = 0.533
```

The fund earned 0.533 units of excess return per unit of risk. This is in the "acceptable" range but below 1.0.

### Example 2: Comparing Funds with Sharpe and Sortino
**Given:**
- Fund A: Sharpe = 0.8, Sortino = 1.2
- Fund B: Sharpe = 0.7, Sortino = 1.5

**Calculate:** Which fund is better for a downside-averse investor?

**Solution:**

Fund A has a higher Sharpe ratio (0.8 vs 0.7), indicating better total-risk-adjusted performance. However, Fund B has a notably higher Sortino ratio (1.5 vs 1.2), meaning it delivers significantly more return per unit of downside risk.

The divergence implies Fund B's volatility is more skewed to the upside -- its total volatility includes more "good" volatility (gains), while its downside volatility is relatively contained.

**For a downside-averse investor, Fund B is preferable** because the Sortino ratio better captures the risk they care about (losses), and Fund B's superior Sortino indicates better downside risk management.

### Example 3: Information Ratio
**Given:** A portfolio returned 10% annualized, its benchmark returned 8%, and the tracking error is 4%.

**Calculate:** Information Ratio.

**Solution:**

```
IR = (0.10 - 0.08) / 0.04
   = 0.02 / 0.04
   = 0.50
```

The manager generated 0.50 units of active return per unit of active risk. This is generally considered a good IR, suggesting consistent alpha generation relative to benchmark deviations.

## Common Pitfalls
- **Annualizing Sharpe incorrectly:** The Sharpe ratio scales by sqrt(N) where N is the number of periods per year. SR_annual = SR_monthly * sqrt(12), not * 12. The excess return and volatility must be in consistent units before dividing.
- **Using wrong risk-free rate frequency:** If computing monthly Sharpe, use the monthly risk-free rate (annual rate / 12), not the annual rate directly.
- **Sortino MAR ambiguity:** The Sortino ratio result changes significantly depending on whether MAR = 0, MAR = risk-free rate, or MAR = some target return. Always state the MAR assumption explicitly.
- **Small sample sizes making ratios unreliable:** Ratios computed from fewer than 36 monthly observations are statistically unreliable. A Sharpe ratio from 12 months of data has a standard error of approximately sqrt((1 + SR^2/2) / 12), which is very wide.
- **Comparing Sharpe ratios across different time periods:** A Sharpe of 1.0 in a low-vol environment is not the same as 1.0 in a high-vol environment. Performance ratios are period-specific and not directly comparable across different market regimes.

## Cross-References
- **historical-risk** (wealth-management plugin): Provides the risk measures (volatility, drawdown, downside deviation, tracking error) used as denominators in these performance ratios.
- **performance-reporting** (wealth-management plugin) and **return-calculations** (core plugin): For TWR/MWR calculation methodology and reporting presentation, see performance-reporting and core/return-calculations.
- **forward-risk** (wealth-management plugin): Forward-looking risk measures (VaR, CVaR) complement retrospective performance assessment by estimating future potential losses.
- **volatility-modeling** (wealth-management plugin): Volatility forecasts from GARCH or EWMA can be used to compute forward-looking or conditional Sharpe ratios.
- **factor-investing** (wealth-management plugin): Factor regressions decompose the alpha behind these ratios; the closet-index screen uses tracking error and a breakeven Information Ratio
## Running the script
Run with `uv run scripts/performance_metrics.py` (the PEP 723 header resolves numpy automatically) or with `python3 scripts/performance_metrics.py` after `pip install numpy scipy`. A bare run prints a full scorecard (Sharpe, Sortino, Information Ratio, Calmar, Treynor, Omega, capture ratios, batting average, win/loss) on seeded synthetic portfolio and benchmark data. Use `--verify` to assert outputs match this skill's worked examples and the demo's expected values (exit code 0 on PASS) and `--help` for an overview of the class. The file is primarily meant to be imported as a module (e.g., `from performance_metrics import PerformanceScorecard`).


---

## SKILL: performance-reporting

- Fuente: `JoelLewis/finance_skills` → `plugins/wealth-management/skills/performance-reporting` (MIT)
- Cuándo usarla: Generate clear, accurate performance reports for investment portfolios with benchmarks, attribution, and risk dashboards. Use when the user asks about portfolio performance reports, return summaries, benchmark comparison, risk dashboards, goal progress tracking, or GIPS-compliant reporting. Also trigger when users mention 'quarterly report', 'how did my portfolio do', 'time-weighted vs money-weighted return', 'annualized returns', 'net-of-fee performance', 'rolling Sharpe', or ask how to present investment results to clients.
- Código: extraer `code/JoelLewis_finance_skills.tar` y usar `plugins/wealth-management/skills/performance-reporting/` (performance_reporting.py)

# Performance Reporting — Reporting & Communication

## Core Concepts

### Return Reporting
Accurate and consistent return calculation is the foundation of all performance reporting.

**Period returns:** Report standard time periods — MTD (month-to-date), QTD (quarter-to-date), YTD (year-to-date), 1Y, 3Y, 5Y, 10Y, and since inception. Always state the exact inception date.

**Cumulative vs annualized:** Annualize returns only for periods greater than 1 year. Annualizing a 3-month return is misleading because it implies the rate is sustainable for a full year. For periods under 1 year, report cumulative (total) returns only.

- Annualized return formula: `(1 + cumulative_return)^(1/years) - 1`
- For multi-year periods, always present both cumulative and annualized figures so the reader can see total wealth growth and the rate of compounding.

**Gross vs net of fees:** Always specify whether returns are gross or net of management fees, advisory fees, and transaction costs. Net-of-fee returns are what the investor actually experiences and should be the primary presentation. If showing gross returns, also show the fee drag.

**GIPS (Global Investment Performance Standards):** For institutional reporting, follow GIPS requirements — composite construction, full disclosure, verified calculations, and standardized presentation. Even for non-GIPS reports, the principles of fair representation and full disclosure apply.

**Time-weighted vs money-weighted returns:**
- Time-weighted return (TWR) removes the impact of cash flows — use for evaluating the investment manager's skill.
- Money-weighted return (MWR / IRR) reflects the investor's actual experience including timing of contributions and withdrawals — use for evaluating the investor's outcome.

### Calculation Engines
`scripts/performance_reporting.py` implements the return calculations behind these reports:

- **Modified Dietz (`ModifiedDietz`):** approximates TWR by weighting each external cash flow by the fraction of the period it was invested: R = (V_end - V_start - sum(CF)) / (V_start + sum(w_i * CF_i)), with w_i = (D - d_i)/D. A GIPS-acceptable approximation when daily valuations are unavailable.
- **True TWR (`TimeWeightedReturn`):** chain-links sub-period returns, prod(1 + r_t) - 1, with an annualization helper that refuses periods under 1 year.
- **IRR / MWR (`MoneyWeightedReturn`):** solves NPV(rate) = 0 numerically using Brent's root-finding method (`scipy.optimize.brentq`) over a bracketing interval, returning the annual money-weighted return.
- **GIPS composites (`CompositeReturn`):** asset-weighted composite return using beginning-of-period values as weights, plus equal-weighted return and the asset-weighted internal dispersion GIPS requires for composites with 6+ portfolios.
- **Standard periods (`PeriodReturns`):** MTD/QTD/YTD-style trailing windows (1M through 10Y) and inception-to-date from a daily return series, annualizing only periods of 1 year or more.

### Benchmark Comparison
A return number in isolation is meaningless. Context requires a benchmark.

**Appropriate benchmark selection:** The benchmark must match the portfolio's investment style, geography, capitalization, and asset class mix. A US large-cap equity portfolio should be compared to the S&P 500 or Russell 1000, not the MSCI Emerging Markets Index.

- For multi-asset portfolios, use a blended benchmark (e.g., 60% S&P 500 / 40% Bloomberg Aggregate).
- The benchmark should be investable — the investor could have held it as a passive alternative.
- Document the benchmark rationale and keep it consistent over time to avoid cherry-picking.

**Active return (alpha):** Portfolio return minus benchmark return. Positive alpha indicates outperformance; negative alpha indicates underperformance.

**Tracking error and information ratio:** For definitions and computation, see performance-metrics. In reports, present these alongside active return so the reader can judge how consistently outperformance was achieved.

### Risk Dashboard
Complement return reporting with risk metrics to give a complete picture. For definitions and computation of these metrics (volatility, VaR, drawdown, etc.), see historical-risk.

**Current snapshot metrics:**
- Annualized volatility
- Maximum drawdown and current drawdown
- Value at Risk (VaR) at 95% and 99% confidence levels
- Beta relative to the benchmark

**Rolling metrics:** Show how risk evolves over time, not just a point-in-time estimate.
- 12-month rolling Sharpe ratio
- 12-month rolling volatility
- 36-month rolling beta
- Rolling drawdown chart

**Risk exposure breakdown:**
- Sector concentration and weights vs benchmark
- Factor exposures (value, growth, momentum, quality, size)
- Geographic allocation
- Duration and credit quality (for fixed income)

### Attribution Summary
Explain *why* the portfolio outperformed or underperformed.

**Brinson attribution (allocation, selection, interaction) and factor decomposition:** For methodology and formulas, see performance-attribution. In a report, summarize each effect in one plain-language sentence (e.g., "sector weighting added 0.2%, stock selection added 0.4%").

**Top/bottom contributors (holdings-level):**
- List the 5-10 holdings that contributed most positively and most negatively to portfolio returns.
- Show both the return of the holding and its contribution to total portfolio return (weight x return).
- Provide brief commentary on why each top/bottom contributor performed as it did.

### Goal Progress Tracking
For goal-based investors, frame performance in terms of progress toward their specific objectives.

**On-track assessment:** Is the portfolio on track, behind, or ahead relative to the financial plan?

**Probability of success:** Use Monte Carlo simulation to estimate the probability of reaching the goal given current assets, savings rate, time horizon, and expected return/risk assumptions. Express as a percentage (e.g., "82% probability of funding retirement at age 65").

**Projected vs required return:** Compare the return needed to reach the goal with the expected return of the current portfolio. If the required return exceeds what is reasonable, flag this as a planning gap.

**Milestone tracking:** Express progress as percentage of goal funded. For example: "Retirement goal: $2,000,000. Current portfolio: $850,000. 42.5% funded with 15 years remaining."

### Visualization Best Practices
Charts communicate faster than tables. Choose the right chart for the message.

**Growth of $10,000 chart:** Shows cumulative wealth growth of portfolio vs benchmark over time. Intuitive for all audiences. Use log scale for long time periods to avoid visual distortion from compounding.

**Rolling return chart:** Shows trailing 12-month or 36-month returns over time. Reveals consistency and regime changes. More informative than a single annualized number.

**Drawdown chart:** Shows peak-to-trough declines over time. Viscerally communicates risk in a way that volatility numbers cannot.

**Asset allocation pie/bar chart:** Current allocation vs target/benchmark. Use a grouped bar chart to show both side by side.

**Risk-return scatter plot:** Plot portfolio and benchmark (and possibly peer group) on an annualized return vs annualized volatility plane. Positions in the upper-left (high return, low risk) are desirable.

### Report Frequency and Structure
- **Monthly brief:** 1-page summary — headline return, benchmark comparison, major attribution drivers, any notable events.
- **Quarterly detailed:** 3-5 pages — full return table, attribution, risk dashboard, goal progress, market commentary, and outlook.
- **Annual comprehensive:** 8-15 pages — everything in the quarterly report plus year-in-review, tax reporting summary, planning updates, and IPS review.

### Plain Language Communication
The most important reporting skill is translating numbers into meaning.

- Do not just state "the portfolio returned 8.1% YTD." Add context: "The portfolio returned 8.1% YTD, outperforming its benchmark by 0.6 percentage points, driven primarily by strong stock selection in the technology sector."
- Explain whether performance is good or bad relative to expectations and the plan.
- Use analogies and comparisons the audience understands.
- Define technical terms on first use or include a glossary.
- Lead with the conclusion, then provide supporting detail for those who want to dig deeper.

## Worked Examples

### Example 1: Quarterly Performance Report Summary
**Given:** A balanced portfolio (60% equity / 40% fixed income) returned 3.2% in Q3 (benchmark: 2.8%). YTD the portfolio returned 8.1% vs 7.5% for the benchmark. The portfolio Sharpe ratio is 0.85 over the trailing 12 months. Equity selection in technology (+0.3%) and an underweight in energy (-0.1%) were the main attribution drivers.

**Analysis:**

**Headline:** The portfolio outperformed its benchmark by 0.4 percentage points in Q3 and 0.6 percentage points YTD, driven by strong stock selection in technology.

**Return summary table:**

| Period | Portfolio | Benchmark | Active Return |
|--------|-----------|-----------|---------------|
| Q3     | +3.2%     | +2.8%     | +0.4%         |
| YTD    | +8.1%     | +7.5%     | +0.6%         |

**Attribution highlights:**
- Technology stock selection contributed +0.3% — the largest single driver of outperformance.
- Underweight energy allocation detracted -0.1% as energy prices rallied in the quarter.
- Net active return of +0.4% demonstrates disciplined bottom-up security selection.

**Risk context:**
- Trailing 12-month Sharpe ratio of 0.85 indicates the portfolio is generating meaningful risk-adjusted excess return.
- Portfolio volatility remains in line with the benchmark, so outperformance is not coming from taking additional risk.

**Plain-language summary for the client:** "Your portfolio gained 3.2% this quarter, beating the benchmark by about half a percent. Year-to-date, you are ahead of the benchmark by a similar margin. The main driver was our technology stock picks, which outperformed the broader tech sector. We remain on track relative to your long-term financial plan."

### Example 2: Goal Progress — Retirement Funding
**Given:** A client has a retirement goal of $2,000,000 in today's dollars. Current portfolio value is $850,000. Time horizon is 15 years. Current annual contribution is $30,000 (increasing 3% per year). Portfolio expected return is 7% nominal, expected volatility is 12%. Inflation assumption is 2.5%.

**Analysis:**

**Current status:**
- Goal: $2,000,000 (in today's dollars)
- Current assets: $850,000
- Funded ratio: 42.5%
- Time remaining: 15 years

**Projection (deterministic):**
- Future value of current assets at 4.5% real return over 15 years: $850,000 x (1.045)^15 = approximately $1,636,000
- Future value of contributions ($30,000/yr escalating 3%/yr) at 4.5% real: approximately $620,000
- Projected total (real): approximately $2,256,000
- Deterministic assessment: **On track** — projected to exceed goal by ~$256,000

**Projection (Monte Carlo, 10,000 simulations):**
- Median outcome: $2,180,000
- 25th percentile: $1,650,000
- 10th percentile: $1,320,000
- Probability of reaching $2,000,000 goal: **68%**

**Interpretation:** While the deterministic projection shows the client is on track, the Monte Carlo analysis reveals a 68% probability of success — reasonable but not highly confident. The gap between the deterministic and probabilistic views is driven by sequence-of-returns risk and volatility drag.

**Recommendations to improve probability of success:**
- Increase annual contributions by $5,000 (raises probability to ~78%).
- Consider modest reduction in spending goal or flexible retirement date.
- Maintain current allocation — reducing risk at this stage would lower expected return and reduce success probability.

**Client-facing summary:** "You have $850,000 saved toward your $2,000,000 retirement goal, which is 42.5% of the way there with 15 years to go. Based on our projections, you have roughly a 68% chance of reaching your goal with your current savings plan. This is a reasonable position, but we can improve your odds by increasing your annual contribution or building in some flexibility on your retirement date."

## Common Pitfalls
- Cherry-picking favorable time periods to present performance in the best light. Always show standard periods and since-inception returns.
- Not showing risk alongside returns. A 15% return with 30% volatility is a very different story than 15% with 10% volatility.
- Using inappropriate benchmarks to flatter performance. Comparing a growth equity fund to a value index during growth-favoring markets is dishonest.
- Too much jargon for non-technical audiences. Sharpe ratios and tracking error mean nothing to most clients without explanation.
- Not providing context for numbers. Is 8% good or bad? It depends on the benchmark, the risk taken, the market environment, and the goal.
- Showing short-period returns annualized. A 5% return in one month is not "60% annualized" — this is misleading and should never be presented.
- Presenting only time-weighted returns when the client's cash flow timing significantly impacted their actual experience. Show money-weighted returns alongside TWR when there are large or ill-timed flows.
- Survivorship bias in composite reporting: excluding terminated accounts or poor-performing strategies from historical track records.
- Ignoring taxes: for taxable investors, after-tax returns are what actually matters.

## Cross-References
- **statistics-fundamentals** (core plugin): return distributions, confidence intervals for projections
- **time-value-of-money** (core plugin): future value projections, annualization math
- **performance-metrics** (wealth-management plugin): Sharpe, Sortino, Information Ratio calculation details
- **historical-risk** (wealth-management plugin): volatility, drawdown, VaR computation for risk dashboards
- **asset-allocation** (wealth-management plugin): benchmark construction for multi-asset portfolios
- **quantitative-valuation** (wealth-management plugin): forward-looking return assumptions for goal projections
- **finance-psychology** (wealth-management plugin): framing effects in how performance is presented to clients
- **client-review-prep** (advisory-practice plugin): performance data is assembled into the client review meeting package

## Running the script
Run with `uv run scripts/performance_reporting.py` (the PEP 723 header resolves numpy/scipy automatically) or with `python3 scripts/performance_reporting.py` after `pip install numpy scipy`. A bare run prints five demos: a Modified Dietz return, chain-linked TWR, an IRR solved via Brent's method, a GIPS composite summary, and a standard-period return table. Use `--verify` to assert the demo outputs match expected values (exit code 0 on PASS) and `--help` for an overview of the classes. The file is primarily meant to be imported as a module (e.g., `from performance_reporting import ModifiedDietz, MoneyWeightedReturn`).


---

## SKILL: policy-writer

- Fuente: `SYasJ/claude-business-skills` → `plugins/risk/skills/policy-writer` (MIT)
- Cuándo usarla: Draft a policy people can follow, with an owner, an exception path, and a review date. Use when the user mentions write a policy, policy draft, governance policy, company policy, or asks for a policy draft. Risk and compliance skill by Yasir Jilani.

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'policy-writer' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Policy Writer

Draft a policy people can follow, with an owner, an exception path, and a review date.

## When to use this skill

Use this skill when the user:

- write a policy
- policy draft
- governance policy
- company policy

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

- The behavior to govern
- The owner
- The audience
- Related procedures

## Workflow


### 1. Step 1

State the purpose and who it applies to.
### 2. Step 2

Write requirements as behaviors.
### 3. Step 3

Point to the procedure for how. The policy should not be a novel.
### 4. Step 4

Add an exception path and an owner.
### 5. Step 5

Set a review date.
### 6. Step 6

Mark it draft until the owner adopts it. Do not invent regulatory citations.

## Output

Deliver a **policy draft**.

- Purpose of this policy draft, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a policy draft by 30 September 2026. A draft cites several laws from memory to sound serious.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A draft cites several laws from memory to sound serious.

The behavior to govern: Control 7.2 access review, recorded 14 September 2026. No supporting file attached
The owner: Priya Shah, controller
The audience: people who already buy from Northline Studio
Related procedures: their one-page rule dated 2 Mar 2026. No exception log since
```

### Example outcome

**Policy draft**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Removes the invented citations, names an owner, and stays short enough to follow.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The behavior to govern | Control 7.2 access review, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The owner | Priya Shah, controller | Carried into the draft |
| The audience | people who already buy from Northline Studio | Carried into the draft |
| Related procedures | their one-page rule dated 2 Mar 2026. No exception log since | Needs confirmation |

**How this draft was built**

**1. State the purpose and who it applies to**

**2. Write requirements as behaviors**

**3. Point to the procedure for how. The policy should not be a novel**

**4. Add an exception path and an owner**

**5. Set a review date**

**Deliberately not done**
- A policy with no owner.
- Invented legal citations.
- Requirements nobody can perform.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A policy with no owner
- Invented legal citations
- Requirements nobody can perform

## Related skills

- `handbook-policy-draft`
- `security-policy-draft`


---

## SKILL: portfolio-analytics

- Fuente: `agiprolabs/claude-trading-skills` → `skills/portfolio-analytics` (MIT)
- Cuándo usarla: Portfolio-level performance measurement including return metrics, risk metrics, risk-adjusted ratios, rolling analysis, and HTML reports
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/portfolio-analytics/` (analyze_portfolio.py, compare_strategies.py)

# Portfolio Analytics

Compute portfolio-level performance metrics from equity curves and trade logs. Covers return metrics, risk metrics, risk-adjusted ratios, drawdown analysis, rolling windows, benchmark comparison, trade-level statistics, and automated HTML report generation via quantstats.

## When to Use This Skill

- After backtesting a strategy (e.g., from `vectorbt` or `strategy-framework`)
- Comparing multiple strategies or parameter sets side-by-side
- Generating investor-ready performance reports
- Evaluating live trading performance against benchmarks
- Assessing risk-adjusted returns for portfolio allocation decisions

## Prerequisites

```bash
uv pip install pandas numpy quantstats
```

## Input Format

All analytics start from an **equity curve** — a time-indexed Series of portfolio values:

```python
import pandas as pd
import numpy as np

# From a backtest
equity = pd.Series(
    [10000, 10150, 10080, 10320, 10510, 10440, 10680],
    index=pd.date_range("2025-01-01", periods=7, freq="D"),
    name="strategy_equity"
)

# Convert to returns
returns = equity.pct_change().dropna()
```

## Return Metrics

### Total Return

```python
total_return = (equity.iloc[-1] / equity.iloc[0]) - 1
```

### CAGR (Compound Annual Growth Rate)

```python
days = (equity.index[-1] - equity.index[0]).days
cagr = (equity.iloc[-1] / equity.iloc[0]) ** (365.25 / days) - 1
```

### Daily Mean Return

```python
daily_mean = returns.mean()
annualized_mean = daily_mean * 252  # trading days
```

### Cumulative Returns

```python
cumulative = (1 + returns).cumprod() - 1
```

## Risk Metrics

### Annualized Volatility

```python
daily_vol = returns.std()
annual_vol = daily_vol * np.sqrt(252)
```

### Value at Risk (VaR)

Historical VaR at a given confidence level:

```python
def historical_var(returns: pd.Series, confidence: float = 0.95) -> float:
    """Compute historical VaR.

    Args:
        returns: Daily return series.
        confidence: Confidence level (e.g., 0.95 for 95%).

    Returns:
        VaR as a positive number representing potential loss.
    """
    return -np.percentile(returns, (1 - confidence) * 100)
```

### Conditional VaR (CVaR / Expected Shortfall)

```python
def historical_cvar(returns: pd.Series, confidence: float = 0.95) -> float:
    """Mean of returns below the VaR threshold."""
    var = historical_var(returns, confidence)
    return -returns[returns <= -var].mean()
```

### Maximum Drawdown

```python
def max_drawdown(equity: pd.Series) -> float:
    """Maximum peak-to-trough decline."""
    peak = equity.cummax()
    drawdown = (equity - peak) / peak
    return drawdown.min()  # negative number

def drawdown_series(equity: pd.Series) -> pd.Series:
    """Full drawdown time series."""
    peak = equity.cummax()
    return (equity - peak) / peak
```

### Time Underwater

```python
def time_underwater(equity: pd.Series) -> int:
    """Longest consecutive period below previous peak (in days)."""
    dd = drawdown_series(equity)
    is_underwater = dd < 0
    groups = (~is_underwater).cumsum()
    underwater_periods = is_underwater.groupby(groups).sum()
    return int(underwater_periods.max()) if len(underwater_periods) > 0 else 0
```

## Risk-Adjusted Ratios

### Sharpe Ratio

```python
def sharpe_ratio(
    returns: pd.Series,
    rf: float = 0.0,
    periods_per_year: int = 252
) -> float:
    """Annualized Sharpe ratio.

    Args:
        returns: Period returns.
        rf: Risk-free rate per period.
        periods_per_year: Annualization factor.

    Returns:
        Annualized Sharpe ratio.
    """
    excess = returns - rf
    if excess.std() == 0:
        return 0.0
    return (excess.mean() / excess.std()) * np.sqrt(periods_per_year)
```

### Sortino Ratio

```python
def sortino_ratio(
    returns: pd.Series,
    rf: float = 0.0,
    periods_per_year: int = 252
) -> float:
    """Annualized Sortino ratio (penalizes only downside vol)."""
    excess = returns - rf
    downside = excess[excess < 0]
    if len(downside) == 0 or downside.std() == 0:
        return float("inf") if excess.mean() > 0 else 0.0
    return (excess.mean() / downside.std()) * np.sqrt(periods_per_year)
```

### Calmar Ratio

```python
def calmar_ratio(equity: pd.Series, periods_per_year: int = 252) -> float:
    """CAGR divided by max drawdown (absolute value)."""
    returns = equity.pct_change().dropna()
    days = (equity.index[-1] - equity.index[0]).days
    cagr = (equity.iloc[-1] / equity.iloc[0]) ** (365.25 / days) - 1
    mdd = abs(max_drawdown(equity))
    if mdd == 0:
        return float("inf") if cagr > 0 else 0.0
    return cagr / mdd
```

### Omega Ratio

```python
def omega_ratio(
    returns: pd.Series,
    threshold: float = 0.0
) -> float:
    """Ratio of probability-weighted gains to losses."""
    excess = returns - threshold
    gains = excess[excess > 0].sum()
    losses = abs(excess[excess <= 0].sum())
    if losses == 0:
        return float("inf") if gains > 0 else 1.0
    return gains / losses
```

### Information Ratio

```python
def information_ratio(
    returns: pd.Series,
    benchmark_returns: pd.Series,
    periods_per_year: int = 252
) -> float:
    """Excess return per unit of tracking error."""
    active = returns - benchmark_returns
    if active.std() == 0:
        return 0.0
    return (active.mean() / active.std()) * np.sqrt(periods_per_year)
```

## Rolling Analysis

### Rolling Sharpe

```python
def rolling_sharpe(
    returns: pd.Series,
    window: int = 63,
    rf: float = 0.0,
    periods_per_year: int = 252
) -> pd.Series:
    """Rolling annualized Sharpe ratio."""
    excess = returns - rf
    roll_mean = excess.rolling(window).mean()
    roll_std = excess.rolling(window).std()
    return (roll_mean / roll_std) * np.sqrt(periods_per_year)
```

### Rolling Max Drawdown

```python
def rolling_max_drawdown(equity: pd.Series, window: int = 252) -> pd.Series:
    """Rolling max drawdown over a fixed window."""
    result = pd.Series(index=equity.index, dtype=float)
    for i in range(window, len(equity)):
        window_eq = equity.iloc[i - window:i + 1]
        peak = window_eq.cummax()
        dd = (window_eq - peak) / peak
        result.iloc[i] = dd.min()
    return result
```

## Trade-Level Analysis

When you have individual trade records:

```python
def trade_statistics(pnl: pd.Series) -> dict:
    """Compute trade-level statistics from a series of trade PnL values.

    Args:
        pnl: Series where each value is the PnL of one trade.

    Returns:
        Dictionary of trade statistics.
    """
    wins = pnl[pnl > 0]
    losses = pnl[pnl < 0]
    total = len(pnl)

    win_rate = len(wins) / total if total > 0 else 0.0
    avg_win = wins.mean() if len(wins) > 0 else 0.0
    avg_loss = losses.mean() if len(losses) > 0 else 0.0
    largest_win = wins.max() if len(wins) > 0 else 0.0
    largest_loss = losses.min() if len(losses) > 0 else 0.0

    gross_profit = wins.sum() if len(wins) > 0 else 0.0
    gross_loss = abs(losses.sum()) if len(losses) > 0 else 0.0
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else float("inf")

    expectancy = pnl.mean() if total > 0 else 0.0

    return {
        "total_trades": total,
        "win_rate": win_rate,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "largest_win": largest_win,
        "largest_loss": largest_loss,
        "profit_factor": profit_factor,
        "expectancy": expectancy,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
    }
```

## Monthly / Yearly Return Tables

```python
def monthly_returns_table(returns: pd.Series) -> pd.DataFrame:
    """Pivot returns into a month-by-year table.

    Returns:
        DataFrame with years as rows, months (1-12) as columns,
        and an Annual column.
    """
    monthly = returns.resample("ME").apply(lambda x: (1 + x).prod() - 1)
    table = monthly.groupby([monthly.index.year, monthly.index.month]).first()
    table = table.unstack(level=1)
    table.columns = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]
    # Annual column
    annual = returns.resample("YE").apply(lambda x: (1 + x).prod() - 1)
    table["Annual"] = annual.values[:len(table)]
    return table
```

## Benchmark Comparison

```python
def benchmark_comparison(
    strategy_returns: pd.Series,
    benchmark_returns: pd.Series,
    rf: float = 0.0
) -> dict:
    """Compare strategy to benchmark across key metrics."""
    strat_eq = (1 + strategy_returns).cumprod()
    bench_eq = (1 + benchmark_returns).cumprod()

    return {
        "strategy_total_return": strat_eq.iloc[-1] - 1,
        "benchmark_total_return": bench_eq.iloc[-1] - 1,
        "strategy_sharpe": sharpe_ratio(strategy_returns, rf),
        "benchmark_sharpe": sharpe_ratio(benchmark_returns, rf),
        "strategy_max_dd": max_drawdown(strat_eq),
        "benchmark_max_dd": max_drawdown(bench_eq),
        "information_ratio": information_ratio(strategy_returns, benchmark_returns),
        "correlation": strategy_returns.corr(benchmark_returns),
        "beta": (
            strategy_returns.cov(benchmark_returns)
            / benchmark_returns.var()
        ),
        "alpha": (
            strategy_returns.mean()
            - (strategy_returns.cov(benchmark_returns) / benchmark_returns.var())
            * benchmark_returns.mean()
        ) * 252,
    }
```

## Quantstats HTML Reports

Generate investor-ready HTML reports with one function call:

```python
import quantstats as qs

# From returns Series
qs.reports.html(
    returns,
    benchmark=benchmark_returns,  # optional
    output="report.html",
    title="My Strategy",
    rf=0.0,
    periods_per_year=252
)

# Individual metrics
print(f"Sharpe: {qs.stats.sharpe(returns):.2f}")
print(f"Sortino: {qs.stats.sortino(returns):.2f}")
print(f"Max DD: {qs.stats.max_drawdown(returns):.2%}")
print(f"Calmar: {qs.stats.calmar(returns):.2f}")

# Console tearsheet
qs.reports.full(returns)
```

See `references/quantstats_guide.md` for full API reference and customization.

## Integration with Vectorbt

```python
import vectorbt as vbt

# After running a vectorbt backtest
portfolio = vbt.Portfolio.from_signals(close, entries, exits, init_cash=10000)

# Extract equity curve
equity = portfolio.value()
returns = portfolio.returns()

# Use quantstats
qs.reports.html(returns, output="backtest_report.html")
```

## Files

| File | Description |
|------|-------------|
| `references/metrics_guide.md` | Formulas, derivations, annualization factors, interpretation benchmarks |
| `references/quantstats_guide.md` | Quantstats library API, customization, integration patterns |
| `scripts/analyze_portfolio.py` | Single portfolio analysis with all metrics, rolling stats, monthly table |
| `scripts/compare_strategies.py` | Multi-strategy comparison with ranking by risk-adjusted metrics |

## Related Skills

- `vectorbt` — Backtesting engine that produces equity curves for analysis
- `risk-management` — Portfolio-level risk guardrails and allocation
- `position-sizing` — Optimal position sizing using portfolio metrics
- `kelly-criterion` — Optimal growth rate sizing from win rate and payoff
- `trading-visualization` — Chart generation for equity curves and drawdowns

### Referencia: references/metrics_guide.md

# Portfolio Metrics — Formulas & Interpretation Guide

## Notation

| Symbol | Meaning |
|--------|---------|
| R_t | Return in period t |
| R_f | Risk-free rate per period |
| N | Annualization factor (252 daily, 52 weekly, 12 monthly) |
| T | Total number of periods |
| P_t | Portfolio value at time t |

## Return Metrics

### Total Return

```
Total Return = (P_final / P_initial) - 1
```

### CAGR (Compound Annual Growth Rate)

```
CAGR = (P_final / P_initial) ^ (365.25 / days) - 1
```

Where `days` is the calendar day count between first and last observation. CAGR smooths out volatility and shows the constant annual rate that would produce the same terminal value.

### Annualized Mean Return

```
Annualized Mean = mean(R_t) * N
```

This is the arithmetic annualization. It overstates the geometric growth rate when returns are volatile. Use CAGR for the geometric rate.

### Cumulative Return Series

```
Cumulative_t = product(1 + R_i for i in 1..t) - 1
```

In pandas: `(1 + returns).cumprod() - 1`

## Risk Metrics

### Annualized Volatility

```
Vol_annual = std(R_t) * sqrt(N)
```

Uses sample standard deviation. The sqrt(N) scaling assumes returns are IID — an approximation. For crypto and memecoin markets, volatility clustering makes this a rough estimate.

### Value at Risk (VaR) — Historical Method

```
VaR(alpha) = -percentile(R_t, (1 - alpha) * 100)
```

For 95% confidence: `VaR = -percentile(returns, 5)`. This means "on 95% of days, the loss will not exceed VaR."

**Interpretation**: A daily VaR of 3% at 95% confidence means you expect to lose more than 3% on roughly 1 in 20 trading days.

**Parametric VaR** (assumes normal distribution):

```
VaR(alpha) = -(mean(R_t) + z_alpha * std(R_t))
```

Where z_alpha is the z-score for the confidence level (1.645 for 95%, 2.326 for 99%).

### Conditional VaR (CVaR / Expected Shortfall)

```
CVaR(alpha) = -mean(R_t where R_t <= -VaR(alpha))
```

CVaR answers: "When we do breach VaR, how bad is the average loss?" It is always >= VaR and better captures tail risk.

**Example**: If VaR(95%) = 3% and the average loss on the worst 5% of days is 5.2%, then CVaR = 5.2%.

### Maximum Drawdown

```
Drawdown_t = (P_t - max(P_1..P_t)) / max(P_1..P_t)
Max Drawdown = min(Drawdown_t for all t)
```

Maximum drawdown measures the worst peak-to-trough decline. It is always negative (or zero). Report the absolute value when comparing.

### Time Underwater

The longest consecutive period where the portfolio is below its previous peak. Measured in trading days or calendar days. Long underwater periods indicate difficulty recovering from drawdowns.

## Risk-Adjusted Ratios

### Sharpe Ratio

```
Sharpe = (mean(R_t) - R_f) / std(R_t) * sqrt(N)
```

**Derivation**: The Sharpe ratio is the slope of the Capital Allocation Line — the excess return per unit of total risk. Annualization multiplies by sqrt(N) because mean scales linearly with N while standard deviation scales with sqrt(N).

**Interpretation benchmarks**:
| Sharpe | Rating |
|--------|--------|
| < 0 | Losing money |
| 0 - 0.5 | Poor |
| 0.5 - 1.0 | Acceptable |
| 1.0 - 2.0 | Good |
| 2.0 - 3.0 | Excellent |
| > 3.0 | Exceptional (verify — may indicate overfitting) |

**Limitations**: Assumes symmetric return distribution. Penalizes upside volatility equally with downside. Sensitive to measurement frequency.

### Sortino Ratio

```
Sortino = (mean(R_t) - R_f) / std(R_t where R_t < R_f) * sqrt(N)
```

**Derivation**: Replaces total standard deviation with downside deviation. Only penalizes returns below the threshold (usually the risk-free rate or zero). Better than Sharpe for strategies with positive skew (large winners, small losers).

**Interpretation**: Same scale as Sharpe but typically higher because downside deviation <= total deviation.

### Calmar Ratio

```
Calmar = CAGR / |Max Drawdown|
```

**Interpretation**: Return earned per unit of worst-case drawdown. A Calmar of 2.0 means the strategy earns twice its maximum historical drawdown per year.

| Calmar | Rating |
|--------|--------|
| < 0.5 | Poor |
| 0.5 - 1.0 | Acceptable |
| 1.0 - 3.0 | Good |
| > 3.0 | Excellent |

### Omega Ratio

```
Omega(threshold) = integral[threshold to +inf] (1 - F(x)) dx
                   ────────────────────────────────────────────
                   integral[-inf to threshold] F(x) dx
```

In practice (discrete):

```
Omega = sum(max(R_t - threshold, 0)) / sum(max(threshold - R_t, 0))
```

**Interpretation**: The ratio of probability-weighted gains above a threshold to probability-weighted losses below it. Unlike Sharpe, Omega uses the entire return distribution, not just mean and variance. Omega > 1 means the strategy outperforms the threshold on a probability-weighted basis.

### Information Ratio

```
IR = mean(R_strategy - R_benchmark) / std(R_strategy - R_benchmark) * sqrt(N)
```

**Derivation**: The Sharpe ratio of the active (excess over benchmark) returns. Measures how consistently a strategy outperforms its benchmark.

| IR | Rating |
|----|--------|
| < 0 | Underperforming benchmark |
| 0 - 0.5 | Moderate skill |
| 0.5 - 1.0 | Good skill |
| > 1.0 | Exceptional |

## Annualization Factors

| Frequency | Periods per Year (N) | sqrt(N) |
|-----------|---------------------|---------|
| Daily (trading) | 252 | 15.875 |
| Daily (calendar) | 365 | 19.105 |
| Weekly | 52 | 7.211 |
| Monthly | 12 | 3.464 |
| Hourly (24/7 crypto) | 8760 | 93.59 |
| 5-minute (24/7 crypto) | 105120 | 324.22 |

**Important for crypto**: Traditional equities use 252 trading days. Crypto markets trade 24/7/365, so use 365 for daily or 8760 for hourly when analyzing crypto-native strategies. Solana memecoin strategies typically use 365-day annualization.

## Trade-Level Metrics

### Win Rate

```
Win Rate = count(trades where PnL > 0) / count(all trades)
```

Win rate alone is uninformative. A 30% win rate with 5:1 reward-to-risk is excellent.

### Profit Factor

```
Profit Factor = sum(winning trade PnL) / |sum(losing trade PnL)|
```

| PF | Rating |
|----|--------|
| < 1.0 | Losing |
| 1.0 - 1.5 | Marginal |
| 1.5 - 2.0 | Good |
| 2.0 - 3.0 | Excellent |
| > 3.0 | Exceptional (small sample?) |

### Expectancy

```
Expectancy = (Win Rate * Avg Win) + ((1 - Win Rate) * Avg Loss)
```

Where Avg Loss is negative. Expectancy is the expected PnL per trade. Positive expectancy is necessary (but not sufficient) for a viable strategy.

### Payoff Ratio

```
Payoff Ratio = |Avg Win| / |Avg Loss|
```

Combined with win rate, determines whether a strategy is viable:
- High win rate + low payoff = scalping
- Low win rate + high payoff = trend following
- Both high = very rare, verify with out-of-sample data

## Common Pitfalls

1. **Annualization errors**: Using sqrt(252) on monthly data (should be sqrt(12)).
2. **Survivorship bias**: Only analyzing strategies that survived; ignoring blown-up variants.
3. **Overfitting Sharpe**: Optimizing for Sharpe on in-sample data inflates the metric.
4. **Ignoring drawdown duration**: A 20% drawdown lasting 2 days is very different from one lasting 6 months.
5. **Comparing different frequencies**: A daily Sharpe of 2.0 is not comparable to a monthly Sharpe of 2.0 unless both are annualized identically.
6. **Small sample sizes**: 30 trades is not enough to draw conclusions about win rate or profit factor. Aim for 100+ trades minimum.

### Referencia: references/quantstats_guide.md

# Quantstats Library — Usage Guide

## Installation

```bash
uv pip install quantstats
```

Quantstats depends on pandas, numpy, scipy, matplotlib, and seaborn. These install automatically.

## Core Concepts

Quantstats operates on a pandas Series of **returns** (not prices). Index must be DatetimeIndex.

```python
import quantstats as qs
import pandas as pd

# From an equity curve
equity = pd.Series([10000, 10200, 10150, 10400], index=pd.date_range("2025-01-01", periods=4))
returns = equity.pct_change().dropna()
```

## Reports

### HTML Report

```python
qs.reports.html(
    returns,
    benchmark=None,          # Optional: benchmark returns Series
    output="report.html",    # File path for HTML output
    title="Strategy Report", # Report title
    rf=0.0,                  # Risk-free rate (annual)
    periods_per_year=252,    # Annualization factor
    compounded=True,         # Use geometric compounding
    download_filename=None,  # Custom download filename
)
```

The HTML report includes:
- Cumulative returns chart (with benchmark if provided)
- Drawdown chart
- Monthly returns heatmap
- Return distribution histogram
- Rolling Sharpe and rolling volatility
- Key statistics table
- Worst drawdowns table

### Console Full Report

```python
qs.reports.full(returns, benchmark=benchmark_returns)
```

Prints all metrics to stdout in a formatted table.

### Metrics-Only Report

```python
qs.reports.metrics(
    returns,
    benchmark=benchmark_returns,
    mode="full",  # "full", "basic", or a list of metric names
)
```

## Individual Statistics

All functions accept a returns Series and return a scalar.

### Return Metrics

```python
qs.stats.comp(returns)               # Total compounded return
qs.stats.cagr(returns)               # CAGR
qs.stats.expected_return(returns)     # Mean return (annualized)
qs.stats.best(returns)               # Best single period return
qs.stats.worst(returns)              # Worst single period return
qs.stats.avg_return(returns)         # Average period return
qs.stats.avg_win(returns)            # Average winning return
qs.stats.avg_loss(returns)           # Average losing return
qs.stats.win_rate(returns)           # Fraction of positive periods
```

### Risk Metrics

```python
qs.stats.volatility(returns)         # Annualized volatility
qs.stats.max_drawdown(returns)       # Maximum drawdown (negative)
qs.stats.value_at_risk(returns)      # Daily VaR at 95%
qs.stats.conditional_value_at_risk(returns)  # CVaR at 95%
qs.stats.tail_ratio(returns)         # Ratio of 95th to 5th percentile
qs.stats.common_sense_ratio(returns) # Profit factor * tail ratio
qs.stats.outlier_win_ratio(returns)  # Ratio of max win to average win
qs.stats.outlier_loss_ratio(returns) # Ratio of max loss to average loss
```

### Risk-Adjusted Ratios

```python
qs.stats.sharpe(returns, rf=0.0)     # Annualized Sharpe ratio
qs.stats.sortino(returns, rf=0.0)    # Annualized Sortino ratio
qs.stats.calmar(returns)             # Calmar ratio
qs.stats.omega(returns)              # Omega ratio (threshold=0)
qs.stats.information_ratio(returns, benchmark)  # Information ratio
qs.stats.treynor_ratio(returns, benchmark)      # Treynor ratio
qs.stats.gain_to_pain_ratio(returns) # Gain-to-pain ratio
qs.stats.risk_return_ratio(returns)  # Return / volatility
```

### Drawdown Analysis

```python
qs.stats.max_drawdown(returns)       # Worst drawdown
qs.stats.to_drawdown_series(returns) # Full drawdown time series
qs.stats.kelly_criterion(returns)    # Kelly optimal fraction
```

## Plotting Functions

Quantstats includes matplotlib-based plotting:

```python
# Cumulative returns
qs.plots.returns(returns, benchmark=benchmark_returns, savefig="returns.png")

# Drawdown periods
qs.plots.drawdown(returns, savefig="drawdown.png")

# Monthly returns heatmap
qs.plots.monthly_heatmap(returns, savefig="monthly.png")

# Distribution of returns
qs.plots.histogram(returns, savefig="histogram.png")

# Rolling Sharpe
qs.plots.rolling_sharpe(returns, savefig="rolling_sharpe.png")

# Rolling volatility
qs.plots.rolling_volatility(returns, savefig="rolling_vol.png")

# Yearly returns bar chart
qs.plots.yearly_returns(returns, savefig="yearly.png")

# All plots
qs.plots.snapshot(returns, savefig="snapshot.png")
```

All plotting functions accept `savefig` to save to file instead of displaying.

## Customization

### Risk-Free Rate

The `rf` parameter is an **annual** rate. Quantstats converts it per-period internally.

```python
# 5% annual risk-free rate
qs.stats.sharpe(returns, rf=0.05)
```

### Annualization

```python
# Hourly crypto data
qs.stats.sharpe(returns, rf=0.0, periods=8760)  # 24 * 365

# Weekly data
qs.stats.sharpe(returns, rf=0.0, periods=52)
```

### Compounding

```python
# Arithmetic vs geometric returns
qs.stats.cagr(returns, compounded=True)   # geometric (default)
qs.stats.cagr(returns, compounded=False)  # arithmetic
```

## Integration with Vectorbt

```python
import vectorbt as vbt
import quantstats as qs

# Run backtest
portfolio = vbt.Portfolio.from_signals(close, entries, exits, init_cash=10000)

# Extract returns
returns = portfolio.returns()

# Generate HTML report
qs.reports.html(returns, output="backtest_report.html", title="VBT Backtest")

# Or access individual metrics
sharpe = qs.stats.sharpe(returns)
sortino = qs.stats.sortino(returns)
max_dd = qs.stats.max_drawdown(returns)
```

## Common Patterns

### Strategy Comparison

```python
strategies = {
    "momentum": momentum_returns,
    "mean_rev": mean_reversion_returns,
    "hybrid": hybrid_returns,
}

for name, ret in strategies.items():
    print(f"\n{'='*40}")
    print(f"Strategy: {name}")
    print(f"  Sharpe:  {qs.stats.sharpe(ret):.2f}")
    print(f"  Sortino: {qs.stats.sortino(ret):.2f}")
    print(f"  Max DD:  {qs.stats.max_drawdown(ret):.2%}")
    print(f"  Calmar:  {qs.stats.calmar(ret):.2f}")
    print(f"  CAGR:    {qs.stats.cagr(ret):.2%}")
```

### Monthly Table from Quantstats

```python
# Get monthly returns as DataFrame
monthly = qs.stats.monthly_returns(returns)
print(monthly.to_string(float_format=lambda x: f"{x:.2%}"))
```

### Export All Metrics

```python
# Get all metrics as a DataFrame
all_metrics = qs.reports.metrics(returns, mode="full", display=False)
all_metrics.to_csv("strategy_metrics.csv")
```

## Limitations

- Quantstats assumes daily data by default. Always set `periods_per_year` for other frequencies.
- The HTML report renderer requires a graphical backend for matplotlib. On headless servers, set `matplotlib.use("Agg")` before importing quantstats.
- Benchmark data must be aligned (same dates) with strategy returns. Use `.reindex()` or `.align()` if needed.
- Large datasets (10+ years of daily data) may slow down the HTML report generation.
- Some metrics return `nan` or `inf` for very short return series (under 20 observations).

## Troubleshooting

**"No display" error on servers:**
```python
import matplotlib
matplotlib.use("Agg")
import quantstats as qs
```

**Benchmark alignment:**
```python
strategy, benchmark = strategy_returns.align(benchmark_returns, join="inner")
qs.reports.html(strategy, benchmark=benchmark, output="report.html")
```

**Missing dates:**
```python
# Fill missing dates with 0 returns
returns = returns.asfreq("D", fill_value=0.0)
```


---

## SKILL: portfolio-management-systems

- Fuente: `JoelLewis/finance_skills` → `plugins/advisory-practice/skills/portfolio-management-systems` (MIT)
- Cuándo usarla: Select, configure, and operate portfolio management systems for advisory firms, covering model portfolios, UMA/sleeve management, drift monitoring, rebalancing, and custodian data feeds. Use when the user asks about choosing a PMS platform, building or distributing model portfolios, implementing UMA or sleeve-based management, setting drift monitoring thresholds, aggregating held-away assets, reconciling PMS with custodian records, configuring PMS-based billing, or troubleshooting custodian feed issues. Also trigger when users mention 'portfolio management system', 'Orion', 'Black Diamond', 'Tamarac', 'Addepar', 'Advent APX', 'model portfolio', 'sleeve management', 'rebalancing engine', 'custodian feed', or 'PMS migration'.

# Portfolio Management Systems

## Core Concepts

> Expanded detail for each numbered section below lives in
> [references/platform-details.md](references/platform-details.md). Load it when the task needs:
> §1 the platform comparison table or IBOR/OBOR reconciliation dimensions; §2 full model
> specification, governance steps, or marketplace detail; §3 UMA cash-waterfall rules or the
> UMA/SMA/wrap comparison table; §4 drift measurement formulas, threshold configurations, or
> tax-aware rebalancing logic; §5 aggregation data sources and data-quality failure modes;
> §6 break-resolution workflow, corporate-action types, or cost basis methods; §8 daily vs.
> monthly calculation and benchmark tracking detail; §10 the custodian data-flow table,
> integration methods, and feed timing. (Reference §7 trading and §9 billing are pointers to
> the order-management-advisor and fee-billing skills — load those skills directly instead.)

### 1. Portfolio Management System Architecture

The PMS is the operational nerve center of an advisory practice, orchestrating data flow between custodians, trading platforms, reporting engines, CRM, and planning tools. Core functions include portfolio construction, model management, rebalancing, trading, performance reporting, and billing. Major platforms: Orion, Black Diamond, Tamarac, Addepar, Morningstar Direct, Advent/APX. The PMS serves as the firm's Investment Book of Record (IBOR), which must be reconciled daily against the custodian's Official Book of Record (OBOR).

### 2. Model Portfolio Management

Model portfolios define target allocations (asset classes, securities, weights) applied consistently across client accounts. Types include strategic (SAA), tactical (TAA overlays), and specialty models (income, ESG, tax-managed). Firms typically use a two-tier hierarchy (firm-level + advisor-customized). Model changes trigger versioning, account identification, trade proposal generation, and tax-aware transition. Third-party model marketplaces (BlackRock, DFA, Vanguard, PIMCO) allow smaller firms to access institutional-quality investment management.

### 3. Sleeve-Based and UMA Architecture

Unified Managed Accounts (UMAs) divide a single custodial account into virtual sub-accounts (sleeves), each following its own strategy or manager. Benefits: cross-sleeve tax optimization, simplified reporting, reduced account proliferation, and unified cash management. Cash waterfall rules govern deposits, withdrawals, and income allocation across sleeves. UMAs differ from SMAs (single-strategy, one manager) and mutual fund wraps (indirect ownership, limited customization). Typical minimums: $250K-$1M+.

### 4. Drift Monitoring and Rebalancing

Drift is the divergence of actual weights from targets caused by differential returns and cash flows. Measured as absolute drift (percentage-point difference) or relative drift (percentage of target). Threshold configurations range from conservative (3%/15%) to permissive (7%/30%). Rebalancing approaches: calendar-based, threshold-based, opportunistic (cash-flow-directed), and hybrid. Tax-aware rebalancing incorporates capital gains minimization, loss harvesting, wash sale avoidance, and gain budgets.

### 5. Held-Away Asset Aggregation

A complete client picture requires visibility into all assets, including employer plans, stock options, RSUs, bank accounts, and accounts at other custodians. Data sources: aggregation services (Plaid, Yodlee, MX, ByAllAccounts), custodian feeds, manual entry, and employer plan integrations. Challenges include data staleness, categorization errors, and broken connections. The PMS should provide both managed-only and total-household reporting views.

### 6. Portfolio Accounting and Reconciliation

Portfolio accounting tracks positions, transactions, cost basis, cash flows, and accrued income. Daily reconciliation compares PMS against custodian across three dimensions: positions, transactions, and cash. Breaks require classification, root-cause diagnosis, correction, and documentation. Common break sources: corporate actions (splits, mergers, spin-offs, DRIP), trade settlement timing, and data feed issues. Cost basis methods: specific identification, FIFO, and average cost.

### 7. Trading and Order Management Integration

The PMS generates trade proposals from model changes, rebalancing triggers, cash flows, and ad-hoc instructions. In larger firms, trades flow through a separate OMS for compliance checks, block aggregation, and execution routing. Block trading aggregates orders across accounts for best execution with pro-rata allocation. Pre-trade checks cover restricted securities, concentration limits, client restrictions, regulatory limits, and cash minimums. Implementation methods: direct custodian trading, third-party EMS, and mutual fund trading platforms.

### 8. Performance Calculation Engine

The PMS computes returns at multiple levels: security, sleeve, account, household, model, composite, and firm. TWR (time-weighted) eliminates cash flow impact for manager evaluation and GIPS compliance. MWR (money-weighted/IRR) reflects the investor's actual experience. Daily performance provides the most precise TWR; monthly uses approximations like Modified Dietz. Benchmarks (primary, blended, custom) must be tracked at the same frequency as portfolio returns.

### 9. Billing and Fee Calculation

Fee structures: AUM-based (flat or tiered/breakpoint), flat/retainer, performance-based (qualified clients only), and blended. Billing frequency: quarterly (most common), monthly, or annual. Advance billing requires proration; arrears billing delays revenue recognition. Billable AUM determination requires clear policies on included/excluded assets and household aggregation. Fee deduction via direct debit (most common) or invoice. Revenue tracking covers client, advisor, model, and strategy dimensions.

### 10. Custodian Integration and Data Feeds

Custodian integration provides the data backbone: positions, transactions, cash, cost basis, corporate actions, and new accounts flow from custodian to PMS; trade instructions and fee invoices flow from PMS to custodian. Integration methods: proprietary batch feeds (CSV/XML), FIX protocol, APIs, and third-party aggregators. Feed timing: EOD batch (most common), intraday updates, and real-time streaming. Multi-custodian management requires data normalization, consolidated views, custodian-specific trade routing, and separate reconciliation. Custodian transitions (e.g., TD Ameritrade to Schwab) require account mapping, feed migration, and historical data transfer.

## Worked Examples

See [references/examples.md](references/examples.md) for three end-to-end worked examples —
a PMS migration for a growing RIA, a UMA/sleeve implementation for HNW clients, and a
reconciliation break investigation. Load it when the user needs a full scenario walkthrough.

## Common Pitfalls

1. **Treating the PMS as the official record.** The custodian, not the PMS,
   maintains the legally authoritative record of client assets. When discrepancies
   exist, the custodian record governs. Firms that rely solely on PMS data without
   reconciliation risk reporting incorrect positions and performance.

2. **Neglecting daily reconciliation.** Firms that reconcile weekly or monthly
   allow breaks to compound, making root-cause diagnosis much harder. A corporate
   action missed on Monday may cause cascading errors in performance, billing,
   and rebalancing throughout the week.

3. **Over-engineering drift thresholds.** Setting drift bands too tight (e.g., 1%
   absolute) generates excessive trading, increasing costs and tax drag. Setting
   bands too loose (e.g., 10% absolute) allows portfolios to deviate significantly
   from the intended risk profile. Calibrate thresholds based on asset class
   volatility and client tax sensitivity.

4. **Ignoring wash sale rules across accounts.** Tax-loss harvesting in one account
   while purchasing substantially identical securities in another account with the
   same tax ID disallows the loss. The PMS must monitor wash sale windows across
   all accounts for a client or household.

5. **Stale held-away data.** Aggregated held-away data that has not refreshed in
   weeks or months can lead to materially incorrect total-household allocation views
   and flawed planning recommendations. Implement alerts for stale connections and
   establish a process for client re-authentication.

6. **Inconsistent model governance.** Allowing advisors to freely modify firm models
   without oversight creates style drift and compliance risk. Establish clear
   policies on which model elements advisors can customize and require documentation
   of deviations.

7. **Cost basis discrepancies between PMS and custodian.** The PMS and custodian may
   calculate cost basis differently, especially after corporate actions, transfers,
   or wash sale adjustments. If the firm relies on PMS cost basis for tax-loss
   harvesting decisions but the custodian reports different basis to the IRS
   (Form 1099-B), clients may face unexpected tax consequences.

8. **Billing on stale or unreconciled data.** Calculating fees on PMS positions that
   have not been reconciled against the custodian may result in over- or under-billing.
   Always reconcile before running billing.

9. **Failing to test custodian feed changes.** Custodians periodically update their
   data feed formats. Firms that do not monitor for format changes or test in a
   staging environment before production risk silent data-import failures.

10. **Overlooking performance calculation methodology.** Reporting MWR when TWR
    is appropriate (or vice versa) can mislead clients or violate GIPS standards.
    Understand when each methodology is appropriate and clearly label which method
    is used in client-facing reports.

## Cross-References

- **asset-allocation** (wealth-management plugin) — PMS implements the strategic
  and tactical asset allocation defined in the client's investment policy. Model
  portfolios in the PMS are the operational expression of asset allocation decisions.
- **rebalancing** (wealth-management plugin) — The PMS rebalancing engine applies
  rebalancing theory (threshold-based, calendar-based, opportunistic) to live client
  portfolios. The rebalancing skill defines the theory; this skill covers the
  system implementation.
- **tax-efficiency** (wealth-management plugin) — PMS tax-loss harvesting,
  wash sale monitoring, and tax-aware rebalancing apply the tax-efficiency
  principles defined in the tax-efficiency skill to operational workflows.
- **performance-metrics** (wealth-management plugin) — The PMS calculates the
  return metrics (TWR, MWR, alpha, Sharpe ratio) defined in the performance-metrics
  skill. That skill defines the math; this skill covers how the PMS implements the
  calculations.
- **performance-reporting** (wealth-management plugin) — The PMS generates the
  underlying performance data that feeds client-facing performance reports. The
  reporting skill covers presentation and communication; this skill covers
  calculation and data infrastructure.
- **gips-compliance** (compliance plugin) — PMS composite construction and
  performance calculation must satisfy GIPS requirements for firms that claim
  compliance. The GIPS skill defines the standards; this skill covers the PMS
  configuration needed to meet them.
- **order-management-advisor** (advisory-practice plugin) — The OMS receives
  trade lists generated by the PMS. This skill covers trade list generation; the
  OMS skill covers order routing, execution, and allocation.
- **financial-planning-integration** (advisory-practice plugin) — The PMS
  current portfolio (including held-away aggregation) feeds financial planning
  tools for projections and scenario analysis.
- **fee-billing** (advisory-practice plugin) — The PMS fee engine handles
  billing calculations described here. The fee-billing skill covers the broader
  billing operations workflow including invoicing, collections, and revenue
  recognition.
- **client-reporting-delivery** (advisory-practice plugin) — PMS performance
  data, portfolio holdings, and asset allocation feeds the client reporting and
  delivery workflow.

### Referencia: references/examples.md

# Worked Examples — Portfolio Management Systems

## Table of Contents

1. [PMS Migration for a Growing RIA](#example-1-pms-migration-for-a-growing-ria) — spreadsheet-to-Orion migration: platform selection, data migration, model setup, feed configuration, parallel go-live
2. [UMA/Sleeve Implementation for HNW Clients](#example-2-umasleeve-implementation-for-hnw-clients) — consolidating SMAs into a five-sleeve UMA with cross-sleeve tax management
3. [Reconciliation Break Investigation and Resolution](#example-3-reconciliation-break-investigation-and-resolution) — diagnosing 48 position breaks by root cause and building preventive controls

### Example 1: PMS Migration for a Growing RIA

**Scenario:**

A $500M RIA with 800 client households has been managing portfolios using Excel
spreadsheets and the custodian's online platform. The firm operates 12 model
portfolios across two custodians (Schwab and Fidelity). As the firm grows, the
spreadsheet approach creates unacceptable operational risk: rebalancing is
inconsistent, performance reporting is delayed by weeks, and the firm recently
discovered it had been billing a client at the wrong fee rate for two quarters.
The firm decides to implement Orion as its portfolio management system.

**Design Considerations:**

**Platform selection criteria:**

- Multi-custodian support (Schwab and Fidelity integration required).
- Rebalancing engine capable of handling 12+ models across 800+ households.
- Tax-aware rebalancing with wash sale tracking.
- Automated billing with tiered fee schedule support.
- Performance reporting with composite construction for marketing materials.
- Integration with the firm's existing CRM (Salesforce).
- Client portal for on-demand performance access.

**Data migration planning:**

- Export current positions and cost basis from both custodians.
- Reconstruct historical transactions from custodian records (typically 3-5
  years for performance history, full history for cost basis).
- Map existing security positions to Orion's security master.
- Import client and account demographic data from CRM.
- Establish the 12 model portfolios in Orion with target allocations and
  security selections.

**Model setup and configuration:**

- Define each of the 12 models with target weights, drift bands, and
  rebalancing rules.
- Assign each client account to the appropriate model.
- Configure substitution rules for taxable vs. tax-deferred accounts.
- Set drift thresholds (the firm selects 5% absolute / 25% relative).
- Configure cash reserve rules (2% minimum cash per account).

**Custodian feed setup:**

- Establish Schwab data feeds: positions, transactions, cash balances,
  cost basis, corporate actions. Test file delivery and parsing.
- Establish Fidelity data feeds: same data categories. Test independently.
- Configure daily reconciliation jobs for both custodians.
- Validate initial reconciliation: resolve any breaks before go-live.

**Go-live workflow:**

- Run parallel operations for 30 days (maintain spreadsheets alongside Orion).
- Compare rebalancing recommendations from both systems.
- Validate performance calculations against custodian-reported returns.
- Validate billing calculations against historical invoices.
- Train advisors and operations staff on the new workflows.
- Decommission spreadsheet processes after successful parallel period.

**Analysis:**

The migration represents a significant operational transformation. The firm should
budget 3-6 months for full implementation, including 1-2 months for data migration
and setup, 1 month for parallel testing, and 1-2 months for staff training and
workflow refinement. Key risks include data quality issues during migration
(especially historical cost basis), disruption to client reporting during the
transition, and staff resistance to new workflows. The firm should designate a
dedicated project manager and plan for temporary increases in operations staffing
during the transition. Post-implementation, the firm should expect significant
efficiency gains: rebalancing that previously took two days per quarter should
complete in hours, billing errors should be eliminated by automated fee calculation,
and performance reports should be available daily rather than weeks after quarter-end.

### Example 2: UMA/Sleeve Implementation for HNW Clients

**Scenario:**

A wealth management firm serving high-net-worth clients ($1M+ investable assets)
currently manages client portfolios using 3-5 separate SMAs per client, each
following a different strategy. This creates operational burden (multiple account
statements, separate rebalancing for each SMA, inability to coordinate tax
management across accounts) and client confusion. The firm decides to transition
its HNW clients to a UMA/sleeve-based structure using its existing PMS (Tamarac).

**Design Considerations:**

**Sleeve structure design:**

The firm designs a five-sleeve UMA architecture:

| Sleeve | Allocation Range | Strategy | Management |
|---|---|---|---|
| Core U.S. Equity | 25-45% | Broad U.S. equity exposure | Firm proprietary model |
| International Equity | 10-25% | Developed and emerging markets | DFA model via Tamarac |
| Fixed Income | 15-35% | Investment-grade and municipal bonds | PIMCO model |
| Alternatives | 5-15% | Real assets, liquid alternatives | Third-party manager |
| Tactical Overlay | 0-10% | Short-term tactical tilts | CIO discretion |

Cash is managed at the total account level rather than within individual sleeves,
with a 2% minimum cash target.

**Model assignment rules:**

- Each client's Investment Policy Statement (IPS) dictates the overall allocation
  across sleeves based on their risk profile.
- Conservative clients: higher fixed income and lower alternatives allocation.
- Aggressive clients: higher equity and alternatives allocation.
- Sleeve-level models operate independently within their assigned allocation.
- The overlay manager (CIO) can make tactical adjustments within the overlay
  sleeve without affecting other sleeves.

**Cross-sleeve tax management:**

- The PMS overlay engine monitors unrealized gains and losses across all sleeves.
- When rebalancing triggers a sell in one sleeve, the overlay engine checks
  whether a loss can be harvested in another sleeve to offset the gain.
- Wash sale rules are monitored across sleeves: if the fixed income sleeve sells
  a bond fund at a loss, the equity sleeve cannot purchase a substantially
  identical fund within 30 days.
- Year-end tax management: the overlay engine runs a cross-sleeve analysis to
  identify harvesting opportunities before December 31.

**Reporting configuration:**

- **Client-facing reports** show total UMA performance alongside per-sleeve
  performance attribution, so clients understand how each strategy contributes.
- **Internal reports** track model-level performance (how well each model
  performed independent of client cash flows) and implementation efficiency
  (how closely client accounts track their assigned models).
- **Billing reports** calculate fees on total UMA AUM (not per-sleeve).
- **Household reports** aggregate across multiple UMAs and non-UMA accounts
  for clients with more than one account.

**Analysis:**

The UMA transition consolidates 3-5 accounts per client into a single account,
reducing custodian fees, simplifying client statements, and enabling cross-strategy
tax optimization that was previously impossible. The firm should expect a 2-3 month
transition per client cohort, as existing SMA positions must be transferred in-kind
to the new UMA account structure. Tax implications of the transition must be
carefully managed — the firm should avoid realizing gains during the restructuring
by transferring positions in-kind wherever possible. The ongoing operational benefit
is substantial: the overlay manager can rebalance all sleeves simultaneously,
dividends and income flow to a single cash pool, and withdrawals can be sourced
from the most tax-efficient sleeve. The firm should track client satisfaction
metrics before and after the transition, anticipating improvement in client
comprehension of their portfolio structure and investment strategy.

### Example 3: Reconciliation Break Investigation and Resolution

**Scenario:**

An advisory practice managing $350M across 600 accounts discovers during its
Monday morning reconciliation review that 48 accounts (8% of the total) show
position discrepancies between the PMS and the custodian (Schwab). The breaks
range from minor share-count differences to entirely missing positions. The
operations team needs to diagnose the causes, resolve the breaks, and implement
controls to prevent recurrence.

**Design Considerations:**

**Break classification and diagnosis:**

The operations team categorizes the 48 breaks into root-cause buckets:

| Category | Count | Typical Cause |
|---|---|---|
| Missed corporate action | 18 | A stock split processed at custodian but not reflected in PMS |
| Trade settlement timing | 12 | Friday trades settled at custodian over the weekend but PMS shows pending |
| Data feed failure | 8 | The Saturday custodian file failed to load due to a format change in one field |
| Dividend reinvestment | 6 | DRIP shares added at custodian but PMS not configured for auto-DRIP on these accounts |
| Genuine error | 4 | Trades executed at custodian but not initiated through PMS (advisor placed directly) |

**Resolution workflow:**

1. **Corporate action breaks (18 accounts):** The PMS operations team identifies
   that a widely-held equity (held in 18 accounts) underwent a 3:1 stock split
   on the prior Thursday. The custodian processed the split automatically, but
   the PMS corporate action module failed to pick it up from the data feed. The
   team manually applies the split in the PMS, adjusting share counts and cost
   basis for all 18 accounts.

2. **Settlement timing breaks (12 accounts):** These breaks are expected and
   will self-resolve when Monday's end-of-day reconciliation runs. The team marks
   them as "expected timing difference" and monitors for resolution.

3. **Data feed failure (8 accounts):** The Saturday batch file from Schwab
   contained a format change in the corporate action field that caused the PMS
   file parser to reject the entire file for 8 accounts. The team contacts the
   PMS vendor to update the parser, manually imports the affected data, and
   re-runs reconciliation for those accounts.

4. **DRIP configuration (6 accounts):** Six accounts are configured for dividend
   reinvestment at the custodian but the PMS does not reflect this setting. When
   dividends reinvest into fractional shares, the PMS records a cash dividend
   instead. The team updates the DRIP flag in the PMS for these accounts and
   adjusts positions to match the custodian.

5. **Unauthorized trades (4 accounts):** An advisor placed 4 trades directly
   through the custodian platform without going through the PMS. The team enters
   the trades into the PMS after the fact and counsels the advisor on the
   requirement to use the PMS for all trade activity.

**Controls to reduce future breaks:**

- **Automated corporate action processing:** Configure the PMS to automatically
  apply mandatory corporate actions (splits, mergers) from the custodian data
  feed, with alerts for actions requiring manual review (tenders, elections).
- **Feed monitoring:** Implement automated alerts when custodian data files
  fail to arrive, arrive with unexpected format changes, or contain fewer
  records than expected.
- **DRIP audit:** Run a quarterly audit comparing DRIP settings in the PMS
  against custodian DRIP elections for all accounts.
- **Trade workflow enforcement:** Configure custodian access so that advisors
  cannot place trades directly; all trades must originate from the PMS.
- **Daily break dashboard:** Implement a dashboard showing break counts by
  category, age, and resolution status, with escalation rules for breaks
  older than 3 business days.

**Analysis:**

An 8% break rate is above the industry target of under 2% for well-run operations.
The immediate resolution of the 48 breaks eliminates the risk of incorrect
performance reports or billing. However, the more important outcome is the
implementation of preventive controls. Automated corporate action processing alone
should eliminate the largest break category (37.5% of all breaks). Feed monitoring
prevents silent data-quality failures that can cascade into reporting and billing
errors. The trade workflow enforcement addresses a compliance concern: trades placed
outside the PMS bypass pre-trade compliance checks and block-trading allocations,
creating best-execution and fair-allocation risks. The firm should target a break
rate below 1% within 90 days of implementing these controls and track the metric
weekly in operations meetings.

### Referencia: references/platform-details.md

# Platform Details — Portfolio Management Systems

## Table of Contents

1. [Portfolio Management System Architecture](#1-portfolio-management-system-architecture) — core functions, major platform comparison table, IBOR vs. OBOR
2. [Model Portfolio Management](#2-model-portfolio-management) — model specification, types, hierarchy, change governance, marketplaces
3. [Sleeve-Based and UMA Architecture](#3-sleeve-based-and-uma-architecture) — UMA structure, cash management rules, UMA vs. SMA vs. wrap comparison
4. [Drift Monitoring and Rebalancing](#4-drift-monitoring-and-rebalancing) — drift measurement, threshold configurations, rebalancing approaches, tax-aware logic
5. [Held-Away Asset Aggregation](#5-held-away-asset-aggregation) — data sources, data-quality challenges, reporting views
6. [Portfolio Accounting and Reconciliation](#6-portfolio-accounting-and-reconciliation) — IBOR ledger, daily reconciliation, break resolution, corporate actions, cost basis
7. [Trading and Order Management Integration](#7-trading-and-order-management-integration) — pointer to order-management-advisor
8. [Performance Calculation Engine](#8-performance-calculation-engine) — daily vs. monthly calculation, benchmark tracking, performance levels
9. [Billing and Fee Calculation](#9-billing-and-fee-calculation) — pointer to fee-billing
10. [Custodian Integration and Data Feeds](#10-custodian-integration-and-data-feeds) — data flow table, integration methods, feed timing, multi-custodian management

## Core Concepts

### 1. Portfolio Management System Architecture

The portfolio management system is the operational nerve center of an investment advisory
practice. It sits at the intersection of investment management, client servicing, and
compliance, orchestrating the flow of data between custodians, trading platforms, reporting
engines, CRM systems, and financial planning tools.

**Core PMS Functions:**

- **Portfolio construction** — Building and maintaining investment portfolios aligned with
  client objectives and firm models.
- **Model management** — Defining, versioning, and distributing model portfolios across
  the client base.
- **Rebalancing** — Detecting portfolio drift from targets and generating trade proposals
  to restore alignment.
- **Trading** — Producing trade lists, supporting block trading, and routing orders to
  custodians or execution platforms.
- **Performance reporting** — Calculating time-weighted and money-weighted returns at the
  security, account, household, and composite levels.
- **Billing** — Computing advisory fees based on AUM, generating invoices or direct-debit
  instructions, and tracking revenue.

**Major PMS Platforms:**

| Platform | Provider | Typical Firm Size | Key Strengths |
|---|---|---|---|
| Orion Portfolio Solutions | Orion Advisor Solutions | Mid to large RIAs | Deep rebalancing, compliance, and reporting; Eclipse trading engine |
| Black Diamond | SS&C Technologies | Mid-size RIAs | Strong performance reporting and client portal |
| Tamarac | Envestnet | Mid to large RIAs | Rebalancing, CRM integration (via Envestnet ecosystem) |
| Addepar | Addepar | Large RIAs, family offices | Complex asset support, alternatives, data visualization |
| Morningstar Direct | Morningstar | Research-oriented firms | Investment research integration, manager analysis |
| Advent/APX | SS&C Technologies | Large RIAs, institutional | Institutional-grade accounting and multi-currency support |

**Investment Book of Record (IBOR) vs. Official Book of Record:**

The PMS serves as the firm's investment book of record (IBOR), maintaining the advisory
firm's view of positions, transactions, cost basis, and performance. The custodian
maintains the official book of record (OBOR) — the legally authoritative record of client
assets. These two records must be reconciled daily to ensure accuracy. Discrepancies
(breaks) require investigation and resolution before reporting or billing can proceed
with confidence.

**Key reconciliation dimensions:**

- Position reconciliation — Do PMS and custodian agree on shares/units held?
- Transaction reconciliation — Are all trades, dividends, and corporate actions reflected
  in both systems?
- Cash reconciliation — Do cash balances match after accounting for pending settlements?

### 2. Model Portfolio Management

Model portfolios are the foundation of scalable portfolio management. A model defines a
target investment allocation — specifying asset classes, individual securities or funds,
and their target weights — that can be applied consistently across many client accounts.

**Defining a Model Portfolio:**

A model portfolio specification includes:

- **Target asset allocation** — The percentage assigned to each asset class (e.g., 60%
  equity, 35% fixed income, 5% alternatives).
- **Security selection** — The specific ETFs, mutual funds, or individual securities
  used to represent each asset class.
- **Target weights** — The precise weight for each security within the model (e.g.,
  VTI 30%, VXUS 15%, BND 25%, BNDX 10%, VNQ 5%, cash 5%, etc.).
- **Substitution rules** — Tax-efficient alternatives for taxable accounts, ESG
  substitutions, or client-specific restrictions.

**Model Types:**

- **Strategic models (SAA)** — Long-term, policy-driven allocations reflecting the firm's
  capital market assumptions. Changed infrequently (annually or less). Example: a
  "Moderate Growth" model targeting 60/40 equity/fixed income.
- **Tactical models (TAA overlays)** — Short-term tilts applied on top of strategic
  allocations to capitalize on market dislocations or risk management. Example:
  underweighting international equities by 5% during a dollar-strengthening cycle.
- **Specialty models** — Purpose-built allocations for specific objectives: income
  generation, ESG/SRI mandates, tax-managed (municipal bonds, low-turnover equity),
  concentrated stock diversification.

**Model Hierarchy:**

Most firms operate a two-tier model structure:

- **Firm-level models** — Centrally managed by the investment committee or CIO. These
  represent the firm's house view and ensure consistency.
- **Advisor-customized models** — Advisors may create variants of firm models with
  client-specific adjustments (e.g., excluding a sector due to concentrated employer
  stock, adding a charitable giving sleeve). The PMS should track these customizations
  and flag when they deviate materially from the base model.

**Model Changes and Governance:**

When the investment committee changes a model — whether adjusting allocation weights,
substituting a security, or adding a new asset class — the PMS must:

1. Version the model change with an effective date.
2. Identify all accounts assigned to the affected model.
3. Generate rebalancing trade proposals for those accounts.
4. Apply tax-aware logic to minimize the cost of transitioning.
5. Route trades through the trading workflow for review and execution.

**Model Marketplace:**

Major PMS and TAMP platforms offer access to third-party model portfolios from asset
managers such as BlackRock, DFA (Dimensional Fund Advisors), Vanguard, PIMCO, and
JP Morgan. Advisors can adopt these models wholesale or blend them with proprietary
models. This allows smaller firms to leverage institutional-quality investment management
without building in-house research capabilities.

### 3. Sleeve-Based and UMA Architecture

The Unified Managed Account (UMA) structure represents an evolution from single-strategy
managed accounts to multi-strategy, multi-manager portfolios held within a single
brokerage account.

**UMA Structure:**

A UMA divides a single custodial account into multiple virtual sub-accounts called
sleeves. Each sleeve follows its own investment strategy, model, or external manager,
but all sleeves share a single account number, tax ID, and custodial registration.

**Typical UMA Sleeve Examples:**

| Sleeve | Strategy | Manager/Model |
|---|---|---|
| Core U.S. Equity | Large-cap growth + value | Firm proprietary model |
| International Equity | Developed + emerging markets | DFA International Core model |
| Fixed Income | Investment-grade bonds | PIMCO model |
| Alternatives | Real assets, hedge fund replication | Third-party manager |
| Tactical Overlay | Short-term tilts | CIO tactical model |
| Cash/Liquidity | Money market, short-term | Cash management rules |

**Benefits of UMA/Sleeve Architecture:**

- **Tax efficiency** — The overlay manager or PMS can harvest losses in one sleeve and
  avoid realizing gains in another, optimizing the tax outcome at the account level. This
  cross-sleeve tax coordination is impossible when strategies are held in separate accounts.
- **Simplified reporting** — One account statement instead of multiple, with the option
  to show performance by sleeve or for the total account.
- **Reduced account proliferation** — A client who might otherwise need 5-6 separate
  managed accounts can consolidate into a single UMA, reducing operational complexity.
- **Unified cash management** — Cash flows (dividends, interest, withdrawals, deposits)
  can be managed at the account level and allocated across sleeves according to rules.

**Cash Management Across Sleeves:**

The PMS must define how cash is handled across sleeves:

- **Cash waterfall rules** — When a client deposits funds, which sleeves receive
  the cash and in what priority order?
- **Cash raise logic** — When a client requests a withdrawal, which sleeves are
  liquidated and in what order (typically selling the most overweight sleeve first
  or the sleeve with the most harvestable losses)?
- **Income allocation** — Dividends and interest generated within a sleeve may stay
  in that sleeve or flow to a central cash sleeve.

**UMA vs. SMA vs. Mutual Fund Wrap:**

| Feature | UMA | SMA | Mutual Fund Wrap |
|---|---|---|---|
| Number of strategies | Multiple | Single | Multiple (via funds) |
| Account structure | One account, multiple sleeves | One account, one strategy | One account, fund portfolio |
| Security ownership | Direct (individual securities) | Direct | Indirect (fund shares) |
| Tax management | Cross-sleeve optimization | Single-strategy only | Limited (fund-level) |
| Customization | High (per-sleeve and cross-sleeve) | Moderate (single strategy) | Low |
| Typical minimum | $250K-$1M+ | $100K-$250K | $25K-$100K |
| Manager access | Multiple managers, one account | One manager | Multiple managers via funds |

### 4. Drift Monitoring and Rebalancing

Portfolio drift is the divergence of actual portfolio weights from target model weights
caused by differential asset returns, cash flows, and corporate actions over time. The
PMS continuously monitors drift and generates rebalancing recommendations when
thresholds are breached.

**Measuring Drift:**

- **Absolute drift** — The simple difference between actual weight and target weight.
  If U.S. equity target is 40% and actual is 44%, absolute drift is +4 percentage
  points.
- **Relative drift** — The drift as a percentage of the target weight. Using the same
  example, relative drift is 4/40 = 10%.
- **Band-based monitoring** — Each asset class or security has an allowable range
  (band) around the target. Rebalancing triggers only when a holding breaches the
  band boundary. Example: target 40% with a +/-5% band means rebalancing triggers
  below 35% or above 45%.

**Drift Thresholds:**

Common threshold configurations in PMS platforms:

- Conservative: 3% absolute or 15% relative drift.
- Moderate: 5% absolute or 25% relative drift.
- Permissive: 7% absolute or 30% relative drift.

The appropriate threshold depends on tax sensitivity, turnover tolerance, trading costs,
and client preferences.

**Rebalancing Approaches:**

- **Calendar-based** — Rebalancing at fixed intervals (quarterly, semi-annually,
  annually) regardless of drift levels. Simple to implement but may miss significant
  interim drift or trigger unnecessary trades.
- **Threshold-based** — Rebalancing only when drift exceeds defined thresholds.
  More responsive than calendar-based and avoids unnecessary trading, but requires
  continuous monitoring.
- **Opportunistic (cash-flow-directed)** — Using client deposits, withdrawals,
  dividends, and other cash flows as opportunities to move toward targets without
  generating incremental trades. The most tax-efficient approach for accounts with
  regular cash flows.
- **Hybrid** — Combining threshold-based monitoring with opportunistic cash flow
  rebalancing. Thresholds serve as the outer guardrail while cash flows handle
  minor drift continuously.

**Tax-Aware Rebalancing:**

A sophisticated PMS rebalancing engine incorporates tax considerations:

- **Capital gains minimization** — When selling overweight positions, prefer lots
  with losses or long-term gains over short-term gains.
- **Loss harvesting** — Proactively selling positions with unrealized losses to
  generate tax deductions, then replacing with similar (but not substantially
  identical) securities.
- **Wash sale avoidance** — The PMS must track the 30-day wash sale window across
  all accounts for the same tax ID to prevent disallowed losses.
- **Gain budget** — Some firms set a maximum dollar amount of realized gains per
  account per year, and the rebalancing engine respects this constraint.

**Cash-Flow-Directed Rebalancing:**

When a client deposits $50,000 into a portfolio, the PMS calculates the optimal
allocation of that cash to move the portfolio closer to target weights. Rather than
investing proportionally to the current allocation, the deposit is directed to the
most underweight positions. Similarly, withdrawals are funded by selling the most
overweight positions first.

### 5. Held-Away Asset Aggregation

A complete picture of a client's financial situation requires visibility into all assets,
not just those managed by the advisory firm. Held-away assets include employer retirement
plans (401(k), 403(b)), stock options, restricted stock units (RSUs), bank accounts,
annuities, real estate, and accounts at other custodians.

**Data Sources for Held-Away Assets:**

- **Account aggregation services** — Technology platforms that connect to financial
  institutions via screen-scraping or API to retrieve account data. Major providers
  include Plaid, Yodlee (Envestnet), MX, and ByAllAccounts (Morningstar). These
  services pull positions, balances, and sometimes transactions on a scheduled basis.
- **Custodian data feeds** — Some custodians provide direct feeds for accounts
  held at their institution, enabling higher-quality data than aggregation services.
- **Manual entry** — For assets that cannot be electronically aggregated (real estate,
  private equity, collectibles), advisors or clients enter valuations manually. These
  require periodic updates to remain useful.
- **Employer plan integration** — Specialized feeds from retirement plan recordkeepers
  (Fidelity NetBenefits, Empower, Vanguard) that provide participant-level data.

**Challenges with Held-Away Data:**

- **Data freshness** — Aggregated data may be 1-3 days stale, and connections can
  break when institutions change login procedures or add multi-factor authentication.
- **Categorization accuracy** — Aggregation services may misclassify securities or
  asset types, requiring manual correction in the PMS.
- **Stale connections** — Clients must periodically re-authenticate their linked
  accounts. Stale connections produce outdated data that can lead to incorrect
  planning recommendations.
- **Incomplete data** — Some institutions block aggregation, and certain asset types
  (unvested RSUs, stock options) may not transmit full detail (exercise price,
  vesting schedule).

**Use in Financial Planning and Portfolio Management:**

Held-away assets directly affect advisory decisions:

- **Asset allocation assessment** — A client's managed account may appear well
  diversified, but when combined with a 401(k) heavily concentrated in employer
  stock, the total household allocation could be dangerously concentrated.
- **Planning recommendations** — Held-away 401(k) assets affect retirement
  projections, Roth conversion analysis, and Social Security claiming strategies.
- **Tax planning** — Knowing the asset location (tax-deferred, Roth, taxable) across
  all accounts enables better tax-efficient asset placement decisions.

**Reporting Views:**

The PMS should provide two distinct reporting perspectives:

- **Managed-only view** — Shows only assets under the firm's management, used for
  billing, performance reporting, and regulatory filings.
- **Total household view** — Includes held-away assets, used for financial planning
  discussions, asset allocation reviews, and comprehensive client presentations.

### 6. Portfolio Accounting and Reconciliation

Portfolio accounting is the systematic tracking of all investment positions, transactions,
cost basis, cash flows, and accrued income within the PMS. Accuracy in portfolio
accounting is the foundation for reliable performance reporting, tax management, and
client trust.

**PMS as Investment Book of Record (IBOR):**

The PMS maintains a complete transaction history and position ledger for every managed
account:

- **Positions** — Current holdings with quantity, market value, unrealized gain/loss.
- **Transactions** — Buys, sells, exchanges, transfers-in, transfers-out, dividends,
  interest, fees, corporate actions.
- **Cost basis** — Original purchase price and date for each tax lot, adjusted for
  corporate actions (splits, mergers, return of capital).
- **Cash balances** — Settled and pending cash, including accrued income not yet
  received.
- **Accrued income** — Interest accrued on fixed-income holdings between coupon
  payment dates.

**Daily Reconciliation Process:**

Reconciliation compares the PMS investment book of record against the custodian's
official book of record across three dimensions:

1. **Position reconciliation** — Compares shares/units held per security per account.
   Breaks typically result from unprocessed trades, missed corporate actions, or
   data-feed errors.
2. **Transaction reconciliation** — Compares trade activity for the day. Breaks may
   indicate trades executed at the custodian but not reflected in the PMS, or PMS
   trades that failed to execute.
3. **Cash reconciliation** — Compares cash balances accounting for settled and
   unsettled activity. Cash breaks often result from timing differences in
   dividend/interest posting or fee deductions.

**Break Identification and Resolution:**

A break is any discrepancy between PMS and custodian records. Break resolution follows
a standard workflow:

1. Identify break in the daily reconciliation report.
2. Classify the break type (position, transaction, cash, cost basis).
3. Determine root cause (missed corporate action, trade error, feed issue, timing).
4. Apply correction in the appropriate system (PMS adjustment, custodian inquiry).
5. Verify the break is resolved in the next reconciliation cycle.
6. Document the resolution for audit trail purposes.

**Corporate Actions Processing:**

Corporate actions are among the most common sources of reconciliation breaks:

- **Cash dividends** — Record income and increase cash balance.
- **Stock dividends** — Increase share count without cash impact.
- **Stock splits** — Adjust share count and cost basis per share.
- **Reverse splits** — Reduce share count and adjust cost basis.
- **Mergers/acquisitions** — Remove acquired security, add acquiring security,
  adjust cost basis for tax-free reorganizations.
- **Spin-offs** — Add new security, allocate cost basis from parent.
- **Tender offers** — Partial or full redemption at specified price.
- **Return of capital** — Reduce cost basis rather than record income.

**Cost Basis Methods:**

The PMS must support multiple cost basis methods, as the method affects realized
gains and losses:

- **Specific identification** — The investor (or PMS algorithm) selects which tax
  lots to sell, enabling optimal tax management. This is the most common method
  for advisory accounts.
- **FIFO (First In, First Out)** — Sells the oldest lots first. Simple but may
  result in larger gains in rising markets.
- **Average cost** — Uses the average cost of all shares. Permitted only for mutual
  fund shares and certain other securities.

**Tax Lot Management:**

Effective tax lot management enables gain/loss optimization:

- Maintain lot-level detail (purchase date, cost, quantity) for every position.
- Track holding period (short-term vs. long-term) to distinguish gain character.
- Support lot selection strategies (highest cost, lowest cost, loss harvesting,
  gain minimization).
- Track wash sale adjustments across accounts with the same tax ID.

### 7. Trading and Order Management Integration

Trade list generation, PMS-to-OMS handoff, block trading, pre-trade compliance, and
order routing are covered in the **order-management-advisor** skill (advisory-practice
plugin) — load that skill for trading workflow detail.

### 8. Performance Calculation Engine

The PMS serves as the performance calculation engine for the advisory practice,
computing returns at multiple levels and across multiple methodologies. For the
definitions and mathematics of time-weighted (TWR) vs. money-weighted (MWR/IRR)
returns and when each is appropriate, see the wealth-management **performance-metrics**
and **performance-reporting** skills.

**Daily vs. Monthly Performance:**

- **Daily performance** — Returns calculated every day using daily valuations.
  Provides the most precise TWR calculation and enables intra-month reporting.
  Requires daily position and pricing data from custodians.
- **Monthly performance** — Returns calculated at month-end using month-end
  valuations. Less precise for TWR (uses Modified Dietz or similar approximation
  for intra-month cash flows) but requires less infrastructure.

Most modern PMS platforms support daily performance calculation.

**Benchmark Assignment and Tracking:**

Each model, account, or composite is assigned one or more benchmarks:

- **Primary benchmark** — The market index most representative of the portfolio's
  investment strategy (e.g., 60% MSCI ACWI / 40% Bloomberg U.S. Aggregate for
  a 60/40 portfolio).
- **Blended benchmarks** — Weighted combinations of multiple indices matching
  the portfolio's asset allocation.
- **Custom benchmarks** — Firm-constructed benchmarks reflecting specific
  investment policies.

The PMS must track benchmark returns at the same frequency and over the same periods
as portfolio returns to enable meaningful comparison.

**Performance at Multiple Levels:**

A comprehensive PMS calculates performance at every level of the investment hierarchy:

- **Security level** — Return contribution of each holding.
- **Sleeve level** — Performance of each UMA sleeve or sub-strategy.
- **Account level** — Total account performance (TWR and MWR).
- **Household level** — Aggregated performance across all accounts for a client
  or household.
- **Model level** — Theoretical performance of the model itself (useful for
  evaluating model quality separately from implementation).
- **Composite level** — Aggregated performance of all accounts following a
  similar strategy, used for GIPS reporting and marketing.
- **Firm level** — Overall firm AUM-weighted performance.

### 9. Billing and Fee Calculation

Fee schedule structures, billable-AUM determination, billing cycles, fee deduction,
and revenue tracking are covered in the **fee-billing** skill (advisory-practice
plugin) — load that skill for billing detail.

### 10. Custodian Integration and Data Feeds

Custodian integration is the data backbone of the PMS. The quality, completeness,
and timeliness of custodian data feeds directly determine the accuracy of portfolio
accounting, performance reporting, rebalancing, and billing.

**Data Flowing Between PMS and Custodians:**

| Data Type | Direction | Frequency | Purpose |
|---|---|---|---|
| Positions | Custodian to PMS | Daily (EOD) | Reconciliation, reporting |
| Transactions | Custodian to PMS | Daily (EOD) | Accounting, performance |
| Cash balances | Custodian to PMS | Daily (EOD) | Cash management, rebalancing |
| Cost basis | Custodian to PMS | Daily or on-demand | Tax reporting, gain/loss |
| Corporate actions | Custodian to PMS | As-occurs + EOD | Accounting adjustments |
| New accounts | Custodian to PMS | Daily or real-time | Account setup |
| Trade instructions | PMS to custodian | Real-time or batch | Order execution |
| Fee invoices | PMS to custodian | Quarterly/monthly | Fee deduction |

**Integration Methods:**

- **Custodian proprietary data feeds** — Major custodians provide standardized
  data files in proprietary or industry-standard formats. Examples: Schwab
  (Schwab Advisor Center data feeds), Fidelity (Wealthscape data feeds),
  Pershing (NetX360 data feeds). These are typically delivered as batch files
  (CSV, XML, or fixed-width) at end-of-day.
- **FIX protocol** — Financial Information eXchange protocol for real-time trade
  messaging. Used for order routing, execution reporting, and position updates.
  More common for institutional trading than advisory account management.
- **API-based integration** — RESTful APIs provided by custodians for real-time
  data access. Increasingly available but with varying levels of completeness.
  Schwab and Fidelity have expanded API offerings for RIAs.
- **Third-party data aggregators** — Services like Plaid (which absorbed Quovo in 2019), ByAllAccounts
  (Morningstar), or Addepar's data infrastructure that normalize data from
  multiple custodians into a standard format for PMS consumption.

**Feed Timing:**

- **End-of-day (EOD) batch** — The most common feed timing. Custodian generates
  files after market close and settlement processing (typically available by
  early morning of the following business day). EOD feeds provide the settled
  view of positions and transactions.
- **Intraday updates** — Some custodians provide intraday position snapshots and
  real-time trade confirmations. Useful for same-day rebalancing and cash
  management but not universally available.
- **Real-time streaming** — Available for limited data types (trade confirmations,
  price updates) via FIX or websocket connections. Primarily used by firms with
  active trading or time-sensitive operations.

**Multi-Custodian Management:**

Many advisory firms custody client assets at two or more custodians (e.g., Schwab
and Fidelity). The PMS must:

- Ingest and normalize data feeds from each custodian into a unified data model.
- Present a consolidated view of positions, performance, and asset allocation
  across custodians.
- Generate trades appropriate for each custodian's trading platform and rules.
- Reconcile separately against each custodian's records.
- Handle custodian-specific differences in security identifiers, transaction
  types, corporate action processing, and settlement conventions.

**Custodian Transition Management:**

When a firm changes its primary custodian (e.g., transitioning from TD Ameritrade
to Schwab following the 2023-2024 acquisition), the PMS must support:

- Mapping accounts from the old custodian to the new.
- Ingesting the new custodian's data feeds and formats.
- Transferring historical data to maintain performance continuity.
- Managing the transition period when accounts may exist at both custodians
  simultaneously.
- Re-establishing automated trading and fee deduction with the new custodian.
- Communicating changes to clients and managing expectations around
  temporary data gaps.
