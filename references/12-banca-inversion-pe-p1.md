# 12-banca-inversion-pe — parte 1

Skills de terceros agrupadas por tema. Cada sección indica fuente, licencia y dónde está su código.



---

## SKILL: ai-readiness

- Fuente: `anthropics/financial-services` → `plugins/vertical-plugins/private-equity/skills/ai-readiness` (Apache-2.0)
- Cuándo usarla: Scan the portfolio for the highest-leverage AI opportunities and rank where to deploy operating-partner time. Ingests quarterly updates and financials across multiple portfolio companies, identifies quick wins at each, and stacks them into a single ranked action list. Use during quarterly portfolio reviews, annual planning, or when deciding which companies get AI investment first. Triggers on "AI readiness", "AI opportunity scan", "where should we deploy AI", "AI across the portfolio", "AI quick wins", or "which portcos are ready for AI".

# Portfolio AI Readiness

## Workflow

### Step 1: Connect to Portfolio Data

First, ask the user where the portfolio materials live. Don't assume — offer the options:

- **MCP servers** — data room, SharePoint, Google Drive, or a portfolio-ops database if one is connected
- **Local files** — a folder path on disk with quarterly decks, financials, board packs
- **File uploads** — drag PDFs, PowerPoint, or Excel directly into the conversation

Once connected, pull quarterly updates, board decks, and financials for the portfolio (or a subset). For each company, extract: sector, revenue, headcount by function, tech stack mentioned, and any AI/automation initiatives already in flight.

If the user provides a single company, still run the scan but skip the cross-portfolio ranking.

Ask up front if not obvious from materials:
- Hold period remaining per company (AI payback matters less 12 months from exit)
- Whether any portco has already deployed something that worked

### Step 2: Per-Company Scan

For each company, answer three gate questions. All three yes → **Go**. Any no → **Wait** with a note on what unblocks it.

1. **Is the data there?** Can they produce a clean input for the use case — customer list, invoice feed, contract repository — without a 6-month data project first?
2. **Is there an owner?** Someone on the management team who will drive this, not a sponsor who will "support" it.
3. **Can we pilot in 30 days?** One team, one workflow, off-the-shelf tooling. If the answer starts with "first we'd need to...", it's not a quick win.

Then identify the top 2-3 leverage points. Look for these patterns in the cost structure and operations:

**Back Office (usually fastest to pilot)**
- Invoice processing, AP/AR matching, expense categorization
- Contract abstraction — vendor agreements, leases, customer MSAs
- Month-end close: reconciliations, flux commentary, lender reporting first drafts

**Revenue / Front Office**
- RFP and proposal first drafts — big lever if revenue is project-based
- Sales call summaries and CRM hygiene
- Customer support ticket triage and first-response drafting
- Quoting for configured / complex products

**Operations (sector-dependent)**
- SOP and quality documentation generation
- Scheduling and dispatch (field services, logistics)
- Code generation and review (software portcos)

For each leverage point, capture in one line: what it replaces, FTE-hours/week saved (assume 30-50%, not 100%), and whether it's buy-off-the-shelf or needs a light build.

### Step 3: Rank Across the Portfolio

Stack every leverage point from every company into one list. Rank by:

1. **Dollar impact** — annualized EBITDA contribution (cost out + revenue lift, net of tool cost)
2. **Speed to value** — months to first measurable result
3. **Probability** — discount for data quality, change management risk, management team capability

Tiebreaker: favor opportunities with <18 months of hold period remaining — those need to move now or not at all.

Output the stack:

| Rank | Company | Opportunity | Est. EBITDA ($) | Months to Value | Gate | First Step |
|---|---|---|---|---|---|---|
| 1 | | | | | Go | |
| 2 | | | | | Go | |
| 3 | | | | | Wait — [blocker] | |

### Step 4: Find the Replays

The highest-leverage move in a portfolio is running one successful play at multiple companies. Scan for:

- **Same sector, same function** — two healthcare services portcos with manual prior-auth? One implementation, two deployments.
- **Same tool, different company** — if one portco already has a working invoice-processing setup, flag every other portco with >$Xm in AP volume as a fast follower.
- **Shared vendor leverage** — three portcos buying the same tool is a pricing conversation.

List each replay with the lead company (who proves it) and follower companies (who copy it).

### Step 5: Output

One page for the operating partner, structured for a portfolio review:

1. **Top 5 across the portfolio** — the ranked table from Step 3, with owner and 30-day first step
2. **Replays** — 2-3 playbooks that hit multiple companies at once
3. **Go / Wait by company** — one line each; for Waits, what unblocks them
4. **What we're NOT doing** — the opportunities that looked good on paper but failed a gate; saves the operating partner from relitigating them every quarter
5. **Aggregate EBITDA contribution** — total portfolio-wide AI opportunity, split Year 1 quick wins vs. Years 2-3 scale

## Important Notes

- **Rank by dollars, not excitement.** A boring AP automation that saves $400k at a $40m revenue company beats a flashy customer-facing chatbot every time.
- **The binding constraint is almost always data, not models.** If a company can't produce a clean customer list, AI isn't the first project — a data cleanup is. Say so plainly.
- **Off-the-shelf first.** Custom builds are slow, expensive, and fragile for companies without engineering depth. Favor tools they can buy and deploy.
- **Ownership is the real gate.** A quick win with no internal owner dies in 90 days. If no one on the management team wants it, mark it Wait regardless of the dollar size.
- **Hold period drives urgency.** A company 3 years from exit can afford a foundational data project. A company 12 months out needs something that shows up in the LTM EBITDA for the CIM — or skip it.
- **Failed pilots are signal.** If management already tried something and it didn't stick, find out why before proposing the same thing again.


---

## SKILL: buyer-list

- Fuente: `anthropics/financial-services` → `plugins/vertical-plugins/investment-banking/skills/buyer-list` (Apache-2.0)
- Cuándo usarla: Build and organize a universe of potential acquirers for sell-side M&A processes. Identifies strategic and financial buyers, assesses fit, and prioritizes outreach. Use when preparing for a sell-side mandate, building a buyer universe, or evaluating potential partners. Triggers on "buyer list", "buyer universe", "potential acquirers", "who would buy this", "strategic buyers", or "financial sponsors".

# Buyer List

## Workflow

### Step 1: Understand the Target

- Company description, sector, and business model
- Revenue, EBITDA, and growth profile
- Key assets and capabilities (IP, customer relationships, geographic footprint, team)
- Expected valuation range
- Seller preferences (strategic vs. financial, management continuity, timeline)

### Step 2: Strategic Buyers

Identify strategic acquirers across categories:

**Direct Competitors**
- Companies in the same space that would gain market share
- Rationale: Revenue synergies, eliminate competitor, scale

**Adjacent Players**
- Companies in adjacent markets that could expand into the target's space
- Rationale: Product extension, cross-sell, new market entry

**Vertical Integrators**
- Customers or suppliers that could integrate vertically
- Rationale: Supply chain control, margin capture, strategic lock-in

**Platform Builders**
- Large companies building a platform in the space through M&A
- Rationale: Tuck-in acquisition, fill capability gap

For each strategic buyer, assess:

| Buyer | Sector | Revenue | Strategic Fit | Financial Capacity | M&A Track Record | Likelihood | Priority |
|-------|--------|---------|--------------|-------------------|------------------|------------|----------|
| | | | High/Med/Low | | Active/Moderate/None | | A/B/C |

### Step 3: Financial Sponsors

Identify PE/financial buyers:

**Platform Investors**
- Sponsors looking for a new platform in this sector
- Criteria: Fund size, sector focus, deal size range

**Add-on Buyers**
- Sponsors with existing portfolio companies that could acquire the target as a bolt-on
- Identify the specific portfolio company and synergy rationale

**Growth Equity**
- For earlier-stage or high-growth targets
- Minority vs. majority preference

For each sponsor:

| Sponsor | Fund Size | Sector Focus | Portfolio Overlap | Recent Activity | Priority |
|---------|-----------|-------------|-------------------|-----------------|----------|
| | | | | | A/B/C |

### Step 4: Prioritization

Tier the buyer list:

- **Tier 1 (5-10)**: Highest strategic fit, proven acquirers, clear rationale — contact first
- **Tier 2 (10-15)**: Good fit but less obvious — contact in second wave
- **Tier 3 (10-20)**: Possible but lower probability — contact if process needs broadening

### Step 5: Contact Mapping

For each Tier 1 buyer:
- Key decision maker (CEO, Corp Dev head, Partner)
- Relationship status (existing relationship, cold outreach, need introduction)
- Known preferences or constraints (size, geography, structure)
- Best approach channel

### Step 6: Output

- Excel workbook with:
  - Strategic buyers tab (sorted by tier)
  - Financial sponsors tab (sorted by tier)
  - Contact mapping for Tier 1
  - Summary statistics (total buyers by tier, by type)
- One-page buyer universe summary for the engagement letter or pitch

## Important Notes

- Quality over quantity — a focused list of 30-40 well-researched buyers beats a list of 200 names
- Research recent M&A activity — buyers who just did a deal in the space are either hungry for more or tapped out
- Check for antitrust concerns with direct competitors — flag any that might face regulatory issues
- Financial sponsors: check fund vintage and deployment pace — a fund nearing end of investment period may be more motivated
- Always ask the seller if there are buyers they want included or excluded
- Update the list as the process progresses — move buyers between tiers based on feedback


---

## SKILL: cim-builder

- Fuente: `anthropics/financial-services` → `plugins/vertical-plugins/investment-banking/skills/cim-builder` (Apache-2.0)
- Cuándo usarla: Structure and draft a Confidential Information Memorandum for sell-side M&A processes. Organizes company information into a professional, investor-ready document with consistent formatting and narrative flow. Use when preparing sell-side materials, drafting a CIM, or organizing company data for a sale process. Triggers on "CIM", "confidential information memorandum", "offering memorandum", "info memo", "draft CIM", or "sell-side materials".

# CIM Builder

## Workflow

### Step 1: Gather Source Materials

Ask for available inputs:
- Management presentations
- Historical financials (3-5 years)
- Budget/forecast
- Company website and marketing materials
- Customer data (anonymized if needed)
- Org chart
- Prior presentations or board decks
- Quality of earnings report (if available)

### Step 2: CIM Structure

Standard CIM table of contents:

**I. Executive Summary** (2-3 pages)
- Company overview — what they do, why they win
- Investment highlights (5-7 key selling points)
- Financial summary — headline revenue, EBITDA, growth, margins
- Transaction overview — what's being sold, indicative timeline

**II. Company Overview** (3-5 pages)
- History and founding story
- Mission and value proposition
- Products and services description
- Business model and revenue streams
- Key differentiators and competitive advantages

**III. Industry Overview** (3-5 pages)
- Market size and growth dynamics (TAM/SAM/SOM)
- Key industry trends and tailwinds
- Competitive landscape
- Regulatory environment
- Barriers to entry

**IV. Growth Opportunities** (2-3 pages)
- Organic growth levers (new products, markets, pricing)
- M&A / add-on opportunities
- Operational improvements
- Technology investments
- White space analysis

**V. Customers & Sales** (3-5 pages)
- Customer overview (number, segments, geography)
- Top customer analysis (anonymized if pre-LOI)
- Customer concentration and retention metrics
- Sales process and go-to-market strategy
- Pipeline and backlog

**VI. Operations** (2-3 pages)
- Organizational structure
- Key personnel
- Facilities and geographic footprint
- Technology and systems
- Supply chain / vendor relationships

**VII. Financial Overview** (5-8 pages)
- Historical income statement (3-5 years)
- Revenue analysis — by segment, geography, customer type
- EBITDA bridge and margin analysis
- Balance sheet overview
- Cash flow summary
- Capital expenditure history
- Working capital analysis
- Management forecast / budget (if included)

**VIII. Appendix**
- Detailed financial statements
- Customer list (anonymized)
- Product catalog
- Management bios

### Step 3: Drafting Guidelines

- **Tone**: Professional, factual, compelling but not hyperbolic
- **Narrative**: Tell a story — why this business is attractive, defensible, and positioned for growth
- **Data-driven**: Support every claim with data. "Strong growth" → "Revenue grew at a 15% CAGR from 2021-2024"
- **Visuals**: Charts and graphs for financial trends, market size, competitive positioning
- **Length**: 40-60 pages total — enough detail to inform first-round bids, not so long buyers won't read it
- **Confidentiality**: Include a disclaimer page. Anonymize sensitive customer data unless seller approves

### Step 4: Output

- Word document (.docx) with professional formatting
- Separate Excel appendix with detailed financials
- Charts and exhibits embedded in the document

## Important Notes

- The CIM is a sales document — lead with strengths, but don't hide material issues (buyers will find them in diligence)
- Investment highlights should address the 3 things every buyer cares about: growth potential, margin profile, and defensibility
- Financial normalization / pro forma adjustments should be clearly labeled and explained
- Work with legal on the confidentiality disclaimer and any regulatory disclosures
- Get management to review for factual accuracy before distribution
- The CIM sets expectations on valuation — make sure the narrative supports the asking price


---

## SKILL: datapack-builder

- Fuente: `anthropics/financial-services` → `plugins/vertical-plugins/investment-banking/skills/datapack-builder` (Apache-2.0)
- Cuándo usarla: Build professional financial services data packs from various sources including CIMs, offering memorandums, SEC filings, web search, or MCP servers. Extract, normalize, and standardize financial data into investment committee-ready Excel workbooks with consistent structure, proper formatting, and documented assumptions. Use for M&A due diligence, private equity analysis, investment committee materials, and standardizing financial reporting across portfolio companies. Do not use for simple financial calculations or working with already-completed data packs.

# Financial Data Pack Builder

Build professional, standardized financial data packs for private equity, investment banking, and asset management. Transform financial data from CIMs, offering memorandums, SEC filings, web search, or MCP server access into polished Excel workbooks ready for investment committee review.

**Important:** Use the xlsx skill for all Excel file creation and manipulation throughout this workflow.

## CRITICAL SUCCESS FACTORS

Every data pack must achieve these standards. Failure on any point makes the deliverable unusable.

### 1. Data Accuracy (Zero Tolerance for Errors)
- Trace every number to source document with page reference
- Use formula-based calculations exclusively (no hardcoded values)
- Cross-check subtotals and totals for internal consistency
- Verify balance sheet balances: Assets = Liabilities + Equity
- Confirm cash flow ties to balance sheet changes

### 2. ESSENTIAL RULES

**RULE 1: Financial data (measuring money) → Currency format with $**
Triggers: Revenue, Sales, Income, EBITDA, Profit, Loss, Cost, Expense, Cash, Debt, Assets, Liabilities, Equity, Capex
Format: $#,##0.0 for millions, $#,##0 for thousands
Negatives: $(123.0) NOT -$123

**RULE 2: Operational data (counting things) → Number format, NO $**
Triggers: Units, Stores, Locations, Employees, Customers, Square Feet, Properties, Headcount
Format: #,##0 with commas
Negatives: (123) consistent with rest of table

**RULE 3: Percentages (rates and ratios) → Percentage format**
Triggers: Margin, Growth, Rate, Percentage, Yield, Return, Utilization, Occupancy
Format: 0.0% for one decimal place
Display: 15.0% NOT 0.15

**RULE 4: Years → Text format to prevent comma insertion**
Format: Text or custom to prevent 2,024
Display: 2020, 2021, 2022, 2023A, 2024E

**RULE 5: When context is mixed, each metric gets its own appropriate format**
Example:
```
Segment Analysis, 2022, 2023, 2024
Retail Revenue, $50.0, $55.0, $60.0
  Stores, 100, 110, 120
  Revenue per Store, $0.5, $0.5, $0.5
```
Revenue and per-store metrics use $, Store count uses number format.

**RULE 6: Use formulas for all calculations → Never hardcode calculated values**
All subtotals, totals, ratios, and derived metrics must be formula-based, not hardcoded values. This ensures accuracy and allows for dynamic updates.

### 3. Professional Presentation Standards

**Formatting Standards:**

**Color Scheme - Two Layers:**

**Layer 1: Font Colors (MANDATORY from xlsx skill)**
- **Blue text (RGB: 0,0,255)**: ALL hardcoded inputs (historical data, assumptions), NOT normal text
- **Black text (RGB: 0,0,0)**: ALL formulas and calculations
- **Green text (RGB: 0,128,0)**: Links to other sheets

**Layer 2: Fill Colors (Optional for enhanced presentation)**
- Fill colors are optional and should only be applied if requested by the user or if enhancing presentation
- If the user requests colors or professional formatting, use this standard scheme:
  - **Section headers**: Dark blue (RGB: 68,114,196) background with white text
  - **Sub-headers/column headers**: Light blue (RGB: 217,225,242) background with black text
  - **Input cells**: Light green/cream (RGB: 226,239,218) background with blue text
  - **Calculated cells**: White background with black text
- Users can override with custom brand colors if specified

**How the layers work together (if fill colors are used):**
- Input cell: Blue text + light green fill = "User-entered data"
- Formula cell: Black text + white background = "Calculated value"
- Sheet link: Green text + white background = "Reference from another tab"

**Font color tells you WHAT it is. Fill color tells you WHERE it is (if used).**

**IMPORTANT:** Font colors from xlsx skill are mandatory. Fill colors are optional - default is white/no fill unless the user requests enhanced formatting or colors.

**Always apply:**
- Bold headers, left-aligned
- Numbers right-aligned
- 2-space indentation for sub-items
- Single underline above subtotals
- Double underline below final totals
- Freeze panes on row/column headers
- Minimal borders (only where structurally needed)
- Consistent font (typically Calibri or Arial 11pt)

**Never include:**
- Borders around every cell
- Multiple fonts or font sizes
- Charts unless specifically requested
- Excessive formatting or decoration

## Structural Consistency
Use the standard 8-tab structure unless explicitly instructed otherwise:
1. Executive Summary
2. Historical Financials (Income Statement)
3. Balance Sheet
4. Cash Flow Statement
5. Operating Metrics
6. Property/Segment Performance (if applicable)
7. Market Analysis
8. Investment Highlights

### Tab 1: Executive Summary
Purpose: One-page overview for busy executives

Contents:
- Company overview (2-3 sentences on business model)
- Key investment highlights (3-5 bullet points)
- Financial snapshot table (Revenue, EBITDA, Growth for last 3 years + projections)
- Transaction overview if applicable
- Key metrics prominently displayed

Format: Clean, bold headers, minimal decoration, critical numbers emphasized

### Tab 2: Historical Financials (Income Statement)
Purpose: Complete profit and loss history

Contents:
- Revenue breakdown by segment/product line
- Cost of goods sold / Cost of revenue
- Gross profit and gross margin %
- Operating expenses detailed (S&M, R&D, G&A)
- EBITDA and Adjusted EBITDA
- Below-the-line items (D&A, interest, taxes)
- Net income

Format:
- Years as columns (text format: 2020, 2021, 2022)
- $ millions or $ thousands (specify units clearly at top)
- Accounting format for all financial data
- Single underline above subtotals, double underline below net income
- Right-align all numbers

### Tab 3: Balance Sheet
Purpose: Financial position at period end

Contents:
- Current assets (cash, AR, inventory, prepaid, other)
- Long-term assets (PP&E, intangibles, goodwill, other)
- Current liabilities (AP, accrued expenses, current portion of debt, other)
- Long-term liabilities (long-term debt, deferred taxes, other)
- Shareholders' equity (common stock, retained earnings, other)

Format:
- Verify formula: Assets = Liabilities + Equity
- Consistent date labeling
- Include working capital calculation
- Single underline above major subtotals, double underline for final totals

### Tab 4: Cash Flow Statement
Purpose: Cash generation and use analysis

Contents:
- Operating cash flow (indirect method preferred)
- Investing cash flow (capex, acquisitions, asset sales)
- Financing cash flow (debt issuance/repayment, equity, dividends)
- Net change in cash
- Beginning and ending cash balances

Format:
- Link to income statement and balance sheet where possible
- Show reconciliation of net income to operating cash flow
- Clear labeling of cash uses (outflows) vs sources (inflows)

### Tab 5: Operating Metrics
Purpose: Non-financial KPIs and operational data

Contents (industry-dependent):
- Unit volumes, customer counts, locations
- Productivity metrics (revenue per employee, per store, per unit)
- Capacity utilization
- Market share
- Customer retention/churn rates
- Industry-specific KPIs

**CRITICAL FORMAT NOTE:**
NO dollar signs on operational metrics. These are quantities, not currency.

Format:
- Clear units specified (customers, employees, stores, square feet, etc.)
- Whole numbers with commas: 1,250 NOT $1,250
- Percentages for rates: 95.0%
- Right-align numbers

### Tab 6: Property/Segment Performance (if applicable)
Purpose: Detailed breakdown by business unit, property, or segment

Contents:
- Revenue and profitability by segment
- Key metrics by location/product
- Segment-specific KPIs
- Comparative performance analysis

Format: Consistent with financial tabs for revenue/EBITDA, number format for operational metrics

### Tab 7: Market Analysis
Purpose: Industry context and competitive positioning

Contents:
- Market size and growth trends
- Competitive landscape overview
- Market share analysis
- Industry benchmarks and peer comparisons
- Regulatory environment if relevant

Format: Mix of narrative text and tables, cite sources for market data

### Tab 8: Investment Highlights
Purpose: Narrative summary of key investment thesis points

Contents:
- Detailed writeup of competitive strengths
- Growth opportunities and strategic initiatives
- Risk factors and mitigation strategies
- Management assessment and track record
- Investment thesis summary

Format: Clear headers, bullet points, concise paragraphs

## STEP-BY-STEP WORKFLOW

### Phase 1: Document Processing and Data Extraction

**Step 1.1: Analyze source data**
- Access source materials: uploaded documents, web search for public filings, or MCP server data
- Review data structure and identify key sections
- Locate financial statements (typically 3-5 years historical)
- Identify management projections if included
- Note fiscal year end date
- Flag any data quality issues immediately

**Step 1.2: Extract financial statements**
- Locate historical income statement data
- Extract balance sheet snapshots (year-end or quarter-end)
- Find cash flow statement
- Extract management projections if available
- Note all page references for traceability

**Step 1.3: Extract operating metrics**
- Identify non-financial KPIs relevant to industry
- Capture unit economics data
- Extract customer/location/capacity data
- Document growth metrics and trends

**Step 1.4: Extract market and industry data**
- Competitive positioning information
- Market size and growth rates
- Industry benchmark data
- Peer comparison information

**Step 1.5: Note key context**
- Transaction structure and rationale
- Management team background
- Investment highlights from source materials
- Risk factors and considerations
- Any data gaps or inconsistencies

### Phase 2: Data Normalization and Standardization

**Step 2.1: Normalize accounting presentation**
- Ensure consistent line item names across all years
- Standardize revenue recognition treatment
- Identify and document one-time charges
- Create "Adjusted EBITDA" reconciliation if needed
- Note any accounting policy changes

**Step 2.2: Apply format detection logic**
For each data point, determine format based on full context:
- Read tab name, table title, column header, and row label
- Apply essential rules (see above)
- When uncertain, examine original source document
- Default to cleaner formatting (less is more)

**Step 2.3: Identify normalization adjustments**
Common adjustments to document:
- Restructuring charges (add back if truly non-recurring)
- Stock-based compensation (add back per industry standard)
- Acquisition-related costs (add back, specify amounts)
- Legal settlements or litigation costs (evaluate recurrence risk)
- Asset sales or impairments (exclude from operating results)
- Related party adjustments (normalize to market rates)
Note: Source citation format varies by data source (page numbers for documents, URLs for web sources, server references for MCP data)

**Step 2.4: Create adjustment schedule**
For every normalization:
- Document what was adjusted and why
- Cite source (document page number, URL, or data source reference)
- Quantify dollar impact by year
- Assess recurrence risk
- Show calculation from reported to adjusted figures

**Step 2.5: Verify data integrity**
- Confirm subtotals sum correctly using formulas
- Verify balance sheet balances
- Check cash flow ties to balance sheet changes
- Cross-check numbers across tabs for consistency
- Flag any discrepancies for investigation

### Phase 3: Build Excel Workbook

**CRITICAL: Use xlsx skill for all Excel file manipulation. Read xlsx skill documentation before proceeding.**

**Step 3.1: Create standardized tab structure**
Create workbook with tabs:
- Executive Summary
- Historical Financials
- Balance Sheet
- Cash Flow
- Operating Metrics
- Property Performance (if applicable)
- Market Analysis
- Investment Highlights

**Step 3.2: Build each tab with proper formatting**
Apply formatting rules systematically:
- Headers: Bold, left-aligned, 11pt font
- Financial data: Currency format $#,##0.0 for millions
- Operational data: Number format #,##0 (no $)
- Percentages: 0.0% format
- Years: Text format to prevent comma insertion
- Negatives: Use accounting format with parentheses
- Underlines: Single above subtotals, double below totals

**Step 3.3: Insert formulas for calculations**
- All subtotals and totals must be formula-based
- Link balance sheet to income statement where appropriate
- Link cash flow to both income statement and balance sheet
- Create cross-tab references for validation
- Avoid hardcoding any calculated values

<correct_patterns>

### Row Reference Tracking - Copy This Pattern

**Store row numbers when writing data, then reference them in formulas:**

```python
# ✅ CORRECT - Track row numbers as you write
revenue_row = row
write_data_row(ws, row, "Revenue", revenue_values)
row += 1

ebitda_row = row
write_data_row(ws, row, "EBITDA", ebitda_values)
row += 1

# Use stored row numbers in formulas
margin_row = row
for col in year_columns:
    cell = ws.cell(row=margin_row, column=col)
    cell.value = f"={get_column_letter(col)}{ebitda_row}/{get_column_letter(col)}{revenue_row}"
```

**For complex models, use a dictionary:**

```python
row_refs = {
    'revenue': 5,
    'cogs': 6,
    'gross_profit': 7,
    'ebitda': 12
}

# Later in formulas
margin_formula = f"=B{row_refs['ebitda']}/B{row_refs['revenue']}"
```

</correct_patterns>

<common_mistakes>

### WRONG: Hardcoded Row Offsets

**Don't use relative offsets - they break when table structure changes:**

```python
# ❌ WRONG - Fragile offset-based references
formula = f"=B{row-15}/B{row-19}"  # What is row-15? What is row-19?

# ❌ WRONG - Magic numbers
formula = f"=B{current_row-10}*C{current_row-20}"
```

**Why this fails:**
- Breaks silently when you add/remove rows
- Impossible to verify correctness by reading code
- Creates debugging nightmares in the delivered Excel file

</common_mistakes>

**Step 3.4: Apply professional presentation**
- Freeze top row and first column on each data tab
- Set appropriate column widths (typically 12-15 characters)
- Right-align all numeric data
- Left-align all text and headers
- Add single/double underlines per accounting standards
- Ensure clean, minimal appearance

### Phase 4: Scenario Building (if projections included)

**Management Case:**
Present company's projections as provided in source materials:
- Extract all management assumptions
- Document growth rates, margin expansion, capital requirements
- Note key drivers and sensitivities
- Flag any "hockey stick" inflections that require skepticism
- Present as "Management Case" with clear labeling

**Base Case (Risk-Adjusted):**
Apply conservative adjustments to management projections based on company-specific risk factors:
- Apply revenue growth haircut reflecting execution risk and historical forecast accuracy
- Moderate margin expansion assumptions based on industry benchmarks and operating leverage
- Increase capex assumptions if growth-dependent
- Add working capital requirements if understated
- Delay synergy realization if applicable, based on integration complexity
- Document all adjustments with rationale and supporting analysis

**Downside Case (optional but recommended for LBO analysis):**
Stress test scenario based on industry cyclicality and company vulnerabilities:
- Model revenue decline reflecting recession risk or competitive pressure
- Assume margin compression under stress (volume deleverage, pricing pressure)
- Test covenant compliance and liquidity
- Assess downside protection
- Document key risks being stress-tested

**Documentation requirements for scenarios:**
Create assumptions schedule showing:
- Key assumptions by scenario (revenue growth, margins, capex %)
- Rationale for each adjustment
- Sensitivity analysis on key variables
- Historical forecast accuracy if available
- Comparison to industry benchmarks

### Phase 5: Quality Control and Validation

**Step 5.1: Data accuracy checks**
Validate:
- Every number traces to source (check spot samples, cite documents/URLs/servers)
- All calculations are formula-based (no hardcoded values)
- Subtotals and totals are mathematically correct
- Years display without commas (2024 NOT 2,024)
- No formula errors: #REF!, #VALUE!, #DIV/0!, #N/A

**Step 5.2: Format consistency checks**
Verify:
- Financial data has $ signs in format
- Operational data has NO $ signs
- Percentages display as % (15.0% not 0.15)
- Negative numbers use parentheses for financial data
- Headers are bold and left-aligned
- Numbers are right-aligned
- Years are text format

**Step 5.3: Structure and completeness checks**
Confirm:
- All required tabs present and properly sequenced
- Executive summary is concise (fits on one page)
- All key metrics captured comprehensively
- Logical flow from summary to detail
- Appropriate level of granularity in each tab
- No missing data or incomplete sections

**Step 5.4: Professional presentation checks**
Review:
- Minimal borders (only for structure)
- Consistent indentation (2 spaces for sub-items)
- Proper accounting underlines (single and double)
- Clean, professional appearance throughout
- Appropriate column widths (not too narrow or wide)

**Step 5.5: Documentation and assumptions checks**
Ensure:
- All normalization adjustments documented with rationale
- Source citations included (document page numbers, URLs, or data source references)
- Assumptions clearly stated and reasonable
- Executive summary accurate and impactful
- Filename includes company name and date

### Phase 6: Final Delivery

**Step 6.1: Create executive summary**
Write concise, impactful summary including:
- Company overview: business model, products/services, geography (2-3 sentences)
- Key financial metrics: Revenue, EBITDA, Growth rates (table format)
- Investment highlights: 3-5 key strengths or opportunities
- Notable risks or considerations (briefly)
- Transaction context if applicable

**Step 6.2: Final file preparation**
- Save workbook with proper naming: CompanyName_DataPack_YYYY-MM-DD.xlsx

## NORMALIZATION PATTERNS

### Common Adjustments to EBITDA

**1. Restructuring charges**
- Add back if truly non-recurring (facility closure, one-time severance)
- Do NOT add back if company restructures every year
- Document specific nature and rationale for non-recurrence
- Example: "2023 restructuring: $3.0M facility closure, documented in source materials, one-time event"

**2. Stock-based compensation**
- Industry standard: add back for private equity analysis
- Treat as non-cash operating expense
- Be consistent across all periods
- Note if unusually high or includes one-time grants

**3. Acquisition-related costs**
- Add back transaction fees, integration costs
- Document specific amounts by type
- Do not add back ongoing integration investments
- Cite source for each adjustment

**4. Legal settlements and litigation**
- Add back if truly isolated incident
- Assess recurrence risk (one settlement vs pattern of litigation)
- Document nature of settlement
- Consider if this is normal course of business

**5. Asset sales or impairments**
- Exclude gains/losses on asset sales from operating EBITDA
- Remove impairment charges if truly non-recurring
- Document what assets were sold/impaired and why
- Adjust revenue if assets generated operating income

**6. Related party adjustments**
- Normalize above-market related party expenses (rent, management fees)
- Adjust to market rates with supporting documentation
- Remove personal expenses run through business
- Document market rate comparison

### Conservative vs Aggressive Normalization

**Management Case:**
- Include all adjustments management proposes
- Accept company's definition of "non-recurring"
- More aggressive EBITDA adjustments
- Use for understanding management's view

**Base Case (Recommended for investment decisions):**
- Only clearly non-recurring items
- Apply higher scrutiny to recurring "one-time" charges
- Exclude speculative adjustments
- More conservative, defensible to investment committee

## INDUSTRY-SPECIFIC ADAPTATIONS

### Technology/SaaS
Key metrics to capture:
- ARR (Annual Recurring Revenue) and MRR
- Customer count by cohort
- CAC (Customer Acquisition Cost) and LTV (Lifetime Value)
- Churn rate (gross and net)
- Net revenue retention
- Rule of 40 (Growth % + EBITDA Margin %)
- Magic number (sales efficiency)

Format notes: ARR is currency ($), customer count is number (no $), rates are %

### Manufacturing/Industrial
Key metrics to capture:
- Production capacity and capacity utilization %
- Units produced by product line
- Inventory turns
- Gross margin by product line
- Order backlog

Format notes: Units, capacity are numbers (no $), utilization is %, revenue/costs are currency

### Real Estate/Hospitality
Key metrics to capture:
- Properties/rooms/square footage
- Occupancy rates %
- ADR (Average Daily Rate) - currency format
- RevPAR (Revenue per Available Room) - currency format
- NOI (Net Operating Income) - currency format
- Cap rates %
- FF&E reserve

Format notes: Rooms/sqft are numbers, occupancy is %, ADR/RevPAR are currency

### Healthcare/Services
Key metrics to capture:
- Locations/facilities
- Providers/employees
- Patients/visits (volume metrics)
- Revenue per visit - currency
- Payor mix %
- Same-store growth %

Format notes: Locations/visits are numbers, revenue per visit is currency, rates are %

## FINAL DELIVERY CHECKLIST

Complete this checklist before delivering the data pack:

**Structure:**
- All required tabs present and in logical sequence
- Each tab has clear header and title
- Executive summary is concise (fits on one page)

**Data Accuracy:**
- All numbers trace to source (documents, URLs, or data servers)
- Source references documented for key figures (page numbers, URLs, etc.)
- All calculations are formula-based (no hardcoded calculated values)
- Subtotals and totals verified
- Balance sheet balances (Assets = Liabilities + Equity)
- No #REF!, #VALUE!, or #DIV/0! errors

**Formatting - Years and Numbers:**
- Years display correctly: 2020, 2021, 2022 (no commas)
- Financial data has $ signs: $50.0, $125.5
- Operational metrics have NO $ signs: 100 stores, 250 employees
- Percentages formatted correctly: 15.0%, 25.5%
- Negatives in parentheses: $(15.0) not -$15.0

**Formatting - Professional Standards:**
- Headers bold and left-aligned
- Numbers right-aligned
- Consistent indentation (2 spaces for sub-items)
- Single underline above subtotals
- Double underline below final totals
- Frozen panes on headers
- Consistent font throughout
- Minimal borders (only for structure)
- Clean, professional appearance throughout

**Content Completeness:**
- Financial statements complete (IS, BS, CF)
- Operating metrics comprehensively captured
- Normalization adjustments documented
- Assumptions clearly stated
- Executive summary clear, concise, and impactful
- Investment highlights compelling
- Market analysis provides context

**Documentation:**
- All normalization adjustments explained
- Every data cell cited from source with comments and links (document page numbers, URLs, or data source references)
- Assumptions documented with rationale
- Any data limitations noted
- Filename follows convention: CompanyName_DataPack_YYYY-MM-DD.xlsx

**Final Output:**
- File saved to outputs with proper naming convention
- All quality control checks passed


---

## SKILL: dd-checklist

- Fuente: `anthropics/financial-services` → `plugins/vertical-plugins/private-equity/skills/dd-checklist` (Apache-2.0)
- Cuándo usarla: Generate and track comprehensive due diligence checklists tailored to the target company's sector, deal type, and complexity. Covers all major workstreams with request lists, status tracking, and red flag escalation. Use when kicking off diligence, organizing a data room review, or tracking outstanding items. Triggers on "dd checklist", "due diligence tracker", "diligence request list", "what do we still need", or "data room review".

# Due Diligence Checklist

## Workflow

### Step 1: Scope the Diligence

Ask the user for:
- **Target company**: Name, sector, business model
- **Deal type**: Platform acquisition, add-on, growth equity, recap, carve-out
- **Deal size / complexity**: Determines depth of diligence
- **Key concerns**: Any known issues to prioritize (customer concentration, regulatory, environmental, etc.)
- **Timeline**: When is LOI / close targeted?

### Step 2: Generate Workstream Checklists

Generate a checklist across all major workstreams, tailored to the sector:

**Financial Due Diligence**
- Quality of earnings (QoE) — revenue and EBITDA adjustments
- Working capital analysis — normalized vs. actual
- Debt and debt-like items
- Capital expenditure (maintenance vs. growth)
- Tax structure and exposure
- Audit history and accounting policies
- Pro forma adjustments (run-rate, synergies)

**Commercial Due Diligence**
- Market size and growth (TAM/SAM/SOM)
- Competitive positioning and market share
- Customer analysis — concentration, retention, NPS
- Pricing power and contract structure
- Sales pipeline and backlog
- Go-to-market effectiveness

**Legal Due Diligence**
- Corporate structure and org chart
- Material contracts (customer, supplier, partnership)
- Litigation history and pending claims
- IP portfolio and protection
- Regulatory compliance
- Employment agreements and non-competes

**Operational Due Diligence**
- Management team assessment
- Organizational structure and key person risk
- IT systems and infrastructure
- Supply chain and vendor dependencies
- Facilities and real estate
- Insurance coverage

**HR / People Due Diligence**
- Org chart and headcount trends
- Compensation benchmarking
- Benefits and pension obligations
- Key employee retention risk
- Culture assessment
- Union/labor agreements

**IT / Technology Due Diligence** (for tech-enabled businesses)
- Technology stack and architecture
- Technical debt assessment
- Cybersecurity posture
- Data privacy compliance (GDPR, CCPA, SOC2)
- Product roadmap and R&D spend
- Scalability assessment

**Environmental / ESG** (where applicable)
- Environmental liabilities
- Regulatory compliance history
- ESG risks and opportunities

### Step 3: Status Tracking

For each item, track:

| Item | Workstream | Priority | Status | Owner | Notes |
|------|-----------|----------|--------|-------|-------|
| QoE report | Financial | P0 | Pending | | |
| Customer interviews | Commercial | P0 | In Progress | | 3 of 10 complete |

Status options: Not Started → Requested → Received → In Review → Complete → Red Flag

### Step 4: Red Flag Summary

Maintain a running list of red flags discovered during diligence:
- What was found
- Which workstream
- Severity (deal-breaker / significant / manageable)
- Mitigant or path to resolution
- Impact on valuation or deal terms

### Step 5: Output

- Excel workbook with tabs per workstream (default)
- Summary dashboard: % complete by workstream, outstanding items, red flags
- Weekly status update format for deal team

## Sector-Specific Additions

Automatically add relevant items based on sector:
- **Software/SaaS**: ARR quality, cohort analysis, hosting costs, SOC2
- **Healthcare**: Regulatory approvals, reimbursement risk, payor mix
- **Industrial**: Equipment condition, environmental remediation, safety record
- **Financial services**: Regulatory capital, compliance history, credit quality
- **Consumer**: Brand health, channel mix, seasonality, inventory management

## Important Notes

- Prioritize P0 items that are gating to LOI or close
- Flag items where the seller is slow to respond — may indicate issues
- Cross-reference data room contents against the checklist to identify gaps
- Update the checklist as diligence progresses — it's a living document


---

## SKILL: dd-meeting-prep

- Fuente: `anthropics/financial-services` → `plugins/vertical-plugins/private-equity/skills/dd-meeting-prep` (Apache-2.0)
- Cuándo usarla: Prepare for due diligence meetings — management presentations, expert network calls, customer references, and advisor sessions. Generates targeted question lists, benchmarks to reference, and red flags to probe. Use before any diligence meeting or call. Triggers on "prep for management meeting", "diligence call prep", "expert call questions", "customer reference questions", or "meeting prep for [company]".

# Diligence Meeting Prep

## Workflow

### Step 1: Meeting Context

Ask the user for:
- **Meeting type**: Management presentation, expert call, customer reference, advisor check-in, site visit
- **Attendees**: Who from the target company or third party
- **Topic focus**: Full business overview, or specific workstream (financial, commercial, operational, tech)
- **What you already know**: Prior meetings, CIM, data room findings
- **Key concerns**: Specific issues to probe

### Step 2: Generate Question List

Organize questions by priority and topic. Structure depends on meeting type:

#### Management Presentation
**Business Overview (warm-up)**
- Walk us through the founding story and key milestones
- How do you describe the business to someone unfamiliar with the space?
- What are you most proud of? What would you do differently?

**Revenue & Growth**
- Walk us through revenue by customer/segment/geography
- What's driving growth? Price vs. volume vs. new customers
- What does the sales cycle look like? How has win rate trended?
- Where do you see the biggest growth opportunities in the next 3-5 years?

**Competitive Positioning**
- Who do you lose deals to and why?
- What's your moat? How defensible is it?
- How do customers evaluate you vs. alternatives?

**Operations & Team**
- Walk us through the org chart — who are the key people?
- What roles are you hiring for? What's been hardest to fill?
- What keeps you up at night operationally?

**Financial Deep-Dive**
- Walk us through the margin bridge — what's changed and why?
- Any one-time or non-recurring items we should understand?
- How do you think about capex — maintenance vs. growth?
- Working capital seasonality?

**Forward Look**
- Walk us through the budget/plan for next year
- What assumptions are you most/least confident in?
- What would need to go right/wrong to significantly beat/miss plan?

#### Expert Network Call
- How do you view [company]'s positioning in the market?
- What are the secular trends driving this space?
- Who are the strongest competitors and why?
- What risks should an investor be aware of?
- If you were buying this business, what would you diligence most carefully?

#### Customer Reference Call
- How did you find [company] and why did you choose them?
- What alternatives did you evaluate?
- What do they do well? Where could they improve?
- How likely are you to renew/expand? What would change that?
- If they raised prices 10-20%, how would you react?

### Step 3: Benchmarks & Context

For each key topic, provide relevant benchmarks:
- Industry growth rates and margin profiles
- Comparable company metrics (if comps analysis exists in session)
- Data points from the CIM or data room that warrant follow-up
- Discrepancies between different data sources to clarify

### Step 4: Red Flags to Probe

Based on what's known, flag specific areas to dig into:
- Inconsistencies in the CIM or financials
- Customer concentration or churn signals
- Management team gaps or recent departures
- Unusual accounting treatments
- Missing data room items

### Step 5: Output

One-page meeting prep doc:
1. **Meeting logistics**: Who, when, where, duration
2. **Objectives**: Top 3 things you need to learn from this meeting
3. **Question list**: Prioritized, grouped by topic (star the must-asks)
4. **Benchmarks**: Key numbers to reference
5. **Red flags**: Specific items to probe
6. **Follow-up items**: What to request after the meeting

## Important Notes

- Lead with open-ended questions — let management talk, then follow up on specifics
- Don't lead the witness — ask neutral questions, not "isn't it true that..."
- Take notes on body language and confidence levels, not just answers
- Always end with: "What haven't we asked about that we should?"
- Keep the question list to 15-20 max — you won't get through more in a 60-90 min session


---

## SKILL: deal-sourcing

- Fuente: `anthropics/financial-services` → `plugins/vertical-plugins/private-equity/skills/deal-sourcing` (Apache-2.0)
- Cuándo usarla: PE deal sourcing workflow — discover target companies, check CRM for existing relationships, and draft personalized founder outreach emails. Use when sourcing new deals, prospecting companies in a sector, or reaching out to founders. Triggers on "find companies", "source deals", "draft founder email", "check if we've seen this company", or "outreach to founder".

# Deal Sourcing

## Workflow

This skill follows a 3-step sourcing pipeline:

### Step 1: Discover Companies

Research and identify potential target companies based on the user's criteria:

- **Sector/industry focus**: Ask the user what space they're looking in (e.g., "B2B SaaS in healthcare", "industrial services in the Southeast")
- **Deal parameters**: Revenue range, EBITDA range, growth profile, geography, ownership type (founder-owned, PE-backed, corporate carve-out)
- **Sources**: Use web search to find companies matching criteria. Look at industry reports, conference attendee lists, trade publications, and competitor landscapes
- **Output**: A shortlist of companies with: name, description, estimated revenue/size, location, founder/CEO name, website, and why they fit the thesis

### Step 2: CRM Check

Before outreach, check if the company or founder already exists in the firm's CRM:

- Search the user's email (Gmail) for prior correspondence with the company or founder
- Search Slack for any internal mentions or prior discussions about the target
- Ask the user: "Have you or your team had any prior contact with [Company]?"
- Flag any existing relationships, prior passes, or known context
- **Output**: For each company, note: "New" (no prior contact), "Existing" (prior correspondence found — summarize), or "Previously Passed" (if evidence of a prior pass)

### Step 3: Draft Founder Outreach

Draft personalized cold emails to founders/CEOs:

- **Tone**: Professional but warm. Not overly formal — founders respond better to genuine, concise outreach
- **Structure**:
  1. Brief intro — who you are and your firm (ask user for their firm intro if not known)
  2. Why this company caught your attention — reference something specific (product, market position, growth)
  3. What you're looking for — partnership, not just a transaction
  4. Soft ask — "Would you be open to a brief conversation?"
- **Personalization**: Reference the company's specific product, recent news, or market position. Never use generic templates
- **Length**: 4-6 sentences max. Founders are busy
- **Voice matching**: If the user has sent prior outreach emails, study them to match their tone and style. Search Gmail for "sent" emails with keywords like "reaching out", "introduction", "partnership" to find examples

### Email Draft Guidelines

- Subject line: Keep it short and specific. Reference the company or sector, not "Investment Opportunity"
- No attachments on first touch
- Include a clear but low-pressure CTA
- Draft in Gmail if available, otherwise output as text for the user to copy

## Example Interaction

**User**: "Find me founder-owned industrial services companies in Texas doing $10-50M revenue"

**Assistant**:
1. Searches web for industrial services companies in Texas matching the criteria
2. Presents a shortlist of 5-8 companies with key details
3. For each, checks Gmail/Slack for prior contact
4. Drafts personalized outreach emails for the ones marked "New"
5. Presents drafts for user review before sending

## Important Notes

- Always present the shortlist for user review before drafting emails
- Never send emails without explicit user approval
- If the user's firm intro or investment criteria aren't clear, ask before drafting
- Prioritize quality over quantity — 5 well-researched targets beat 20 generic ones


---

## SKILL: deal-tracker

- Fuente: `anthropics/financial-services` → `plugins/vertical-plugins/investment-banking/skills/deal-tracker` (Apache-2.0)
- Cuándo usarla: Track multiple live deals with milestones, deadlines, action items, and status updates. Maintains a deal pipeline view and surfaces upcoming deadlines and overdue items. Use when managing a book of business, tracking process milestones, or preparing for weekly deal reviews. Triggers on "deal tracker", "deal status", "where are we on", "process update", "deal pipeline", or "weekly deal review".

# Deal Tracker

## Workflow

### Step 1: Deal Setup

For each deal, capture:
- **Deal name / code name**: Project [Name]
- **Client**: Seller or buyer name
- **Deal type**: Sell-side, buy-side, financing, restructuring
- **Role**: Lead advisor, co-advisor, fairness opinion
- **Deal size**: Expected enterprise value
- **Stage**: Pre-mandate → Engaged → Marketing → IOI → Diligence → Final bids → Signing → Close
- **Team**: MD, VP, Associate, Analyst assigned
- **Key dates**: Engagement date, CIM distribution, IOI deadline, management meetings, final bid deadline, target close

### Step 2: Milestone Tracking

Track key milestones per deal:

| Milestone | Target Date | Actual Date | Status | Notes |
|-----------|------------|-------------|--------|-------|
| Engagement letter signed | | | | |
| CIM / teaser drafted | | | | |
| Buyer list approved | | | | |
| Teaser distributed | | | | |
| NDA execution | | | | |
| CIM distributed | | | | |
| IOI deadline | | | | |
| IOIs received / reviewed | | | | |
| Shortlist selected | | | | |
| Management meetings | | | | |
| Data room opened | | | | |
| Final bid deadline | | | | |
| Bids received / reviewed | | | | |
| Exclusivity granted | | | | |
| Confirmatory diligence | | | | |
| Purchase agreement signed | | | | |
| Regulatory approval | | | | |
| Close | | | | |

Status: On Track / At Risk / Delayed / Complete

### Step 3: Action Items

Maintain a running action item list across all deals:

| Action | Deal | Owner | Due Date | Priority | Status |
|--------|------|-------|----------|----------|--------|
| | | | | P0/P1/P2 | Open/Done/Blocked |

### Step 4: Weekly Deal Review

Generate a summary for weekly team meetings:

**For each active deal:**
1. One-line status update
2. Key developments this week
3. Upcoming milestones (next 2 weeks)
4. Blockers or risks
5. Action items for next week

**Pipeline summary:**
- Total active deals by stage
- Deals at risk (missed milestones, stalled processes)
- New mandates / pitches in pipeline
- Expected closings this quarter

### Step 5: Output

- Excel workbook with:
  - Pipeline overview (all deals, one row each)
  - Per-deal milestone tracker tabs
  - Action item master list
  - Weekly review summary
- Optional: Markdown summary for email/Slack distribution

## Important Notes

- Update the tracker weekly at minimum — stale trackers are worse than no tracker
- Flag deals where milestones are slipping — early warning prevents surprises
- Action items without owners and due dates don't get done — be specific
- The pipeline view should show deal stage, size, and likelihood — useful for revenue forecasting
- Keep notes on buyer/investor feedback — patterns in feedback inform strategy adjustments
- Archive closed/dead deals separately — keep the active view clean


---

## SKILL: ic-memo

- Fuente: `anthropics/financial-services` → `plugins/agent-plugins/valuation-reviewer/skills/ic-memo` (Apache-2.0)
- Cuándo usarla: Draft a structured investment committee memo for PE deal approval. Synthesizes due diligence findings, financial analysis, and deal terms into a professional IC-ready document. Use when preparing for investment committee, writing up a deal, or creating a formal recommendation. Triggers on "write IC memo", "investment committee memo", "deal write-up", "prepare IC materials", or "recommendation memo".

# Investment Committee Memo

## Workflow

### Step 1: Gather Inputs

Collect from the user (or from prior analysis in the session):

- Company overview and business description
- Industry/market context
- Historical financials (3-5 years)
- Management assessment
- Deal terms (price, structure, financing)
- Due diligence findings (commercial, financial, legal, operational)
- Value creation plan / 100-day plan
- Returns analysis (base, upside, downside)

### Step 2: Draft Memo Structure

Standard IC memo format:

**I. Executive Summary** (1 page)
- Company description, deal rationale, key terms
- Recommendation and headline returns
- Top 3 risks and mitigants

**II. Company Overview** (1-2 pages)
- Business description, products/services
- Customer base and go-to-market
- Competitive positioning
- Management team

**III. Industry & Market** (1 page)
- Market size and growth
- Competitive landscape
- Secular trends / tailwinds
- Regulatory environment

**IV. Financial Analysis** (2-3 pages)
- Historical performance (revenue, EBITDA, margins, cash flow)
- Quality of earnings adjustments
- Working capital analysis
- Capex requirements

**V. Investment Thesis** (1 page)
- Why this is an attractive investment (3-5 pillars)
- Value creation levers (organic growth, margin expansion, M&A, multiple expansion)
- 100-day priorities

**VI. Deal Terms & Structure** (1 page)
- Enterprise value and implied multiples
- Sources & uses
- Capital structure / leverage
- Key legal terms

**VII. Returns Analysis** (1 page)
- Base, upside, and downside scenarios
- IRR and MOIC across scenarios
- Key assumptions driving returns
- Sensitivity analysis

**VIII. Risk Factors** (1 page)
- Key risks ranked by severity and likelihood
- Mitigants for each risk
- Deal-breaker risks (if any)

**IX. Recommendation**
- Clear recommendation: Proceed / Pass / Conditional proceed
- Key conditions or next steps

### Step 3: Output Format

- Default: Word document (.docx) with professional formatting
- Alternative: Markdown for quick review
- Include tables for financials and returns, not just prose

## Important Notes

- IC memos should be factual and balanced — present both bull and bear cases honestly
- Don't minimize risks. IC members will find them anyway; credibility matters
- Use the firm's standard memo template if the user provides one
- Financial tables should tie — check that EBITDA bridges, S&U balances, and returns math is consistent
- Ask for missing inputs rather than making assumptions on deal terms or returns


---

## SKILL: pitch-deck

- Fuente: `anthropics/financial-services` → `plugins/agent-plugins/pitch-agent/skills/pitch-deck` (Apache-2.0)
- Cuándo usarla: Populates investment banking pitch deck templates with data from source files. Use when: user provides a PowerPoint template to fill in, user has source data (Excel/CSV) to populate into slides, user mentions populating or filling a pitch deck template, or user needs to transfer data into existing slide layouts. Not for creating presentations from scratch.

# Populating Investment Banking Pitch Deck Templates

## Reference Files

**Read all reference files at task start before beginning any work.** These contain critical patterns and anti-patterns that will affect your approach. Do not wait until you encounter issues.

| File | Purpose |
|------|---------|
| [`formatting-standards.md`](reference/formatting-standards.md) | Text, bullets, tables, charts, alignment |
| [`slide-templates.md`](reference/slide-templates.md) | Content mapping guidance for common slide types |
| [`xml-reference.md`](reference/xml-reference.md) | PowerPoint XML patterns for tables, shapes, arrows |
| [`calculation-standards.md`](reference/calculation-standards.md) | Financial formulas for verification (CAGR, consensus) |

---

## Workflow Decision Tree

**What type of task is this?**

```
┌─ Populating empty template with source data?
│  └─→ Follow "Template Population Workflow" below
│
├─ Editing existing populated slides?
│  └─→ Extract current content, modify, revalidate
│
└─ Fixing formatting issues on existing slides?
   └─→ See "Common Failures" table, apply targeted fixes
```

---

## ⚠️ Critical Rendering Limitation

**LibreOffice is used for validation but DOES NOT render PowerPoint files accurately.** It will mangle fonts, gradients, shape positions, text wrapping, and some table formatting.

**What this means:** A slide that passes visual validation in LibreOffice may still have issues in Microsoft PowerPoint. The validation loop catches structural issues (missing content, broken tables, placeholder formatting retained) but **cannot** catch font substitution, subtle alignment shifts, or gradient problems.

**Required action:** Always include this statement when delivering output:
> "This file was validated using LibreOffice. Please review in Microsoft PowerPoint before distribution, as rendering differences may exist."

---

## Template Population Workflow

Copy and track progress:

```
Pitch Deck Progress:
- [ ] Phase 1: Extract and validate source data
- [ ] Phase 2: Map content to template sections
- [ ] Phase 3: Populate slides with proper formatting
- [ ] Phase 4: Validate → Fix → Repeat until clean
- [ ] Phase 5: Final verification
```

### Phase 1: Data Extraction
1. **Create backup** of original template before any modifications — copy to `[filename]_backup.pptx`. Direct XML editing or unexpected errors can corrupt files.
2. Identify all source materials (Excel, CSV, PDF reports, Word documents, databases, web sources)
3. Extract relevant data points from each source
4. Validate all numbers against original sources
5. Standardize units and currency (convert all figures to the primary unit/currency used in the template)
6. Note any calculations that need verification → see [`calculation-standards.md`](reference/calculation-standards.md) for formulas

### Phase 2: Content Mapping
1. **Open and visually review the template** — understand its structure, style, and existing content before modifying
2. Analyze template structure — identify all placeholder areas and content boxes
3. Map source data to corresponding template sections → see [`slide-templates.md`](reference/slide-templates.md) for mapping guidance
4. Identify placeholder guidance boxes (colored instruction boxes from task creator)
5. Note any data gaps or mismatches → see [`slide-templates.md`](reference/slide-templates.md#handling-data-template-mismatches) for resolution

### Phase 3: Template Population
1. **Remove or reformat placeholder boxes** — colored instruction boxes show WHAT to create, not HOW to format. Delete them and create properly formatted content in their place. See [Critical Anti-Patterns](#critical-anti-patterns-never-do-these).
2. Populate each section with mapped content (focus on content first)
3. **Then apply formatting** to match template style → see [`formatting-standards.md`](reference/formatting-standards.md)
4. Create tables as actual table objects (NEVER use pipe/tab-separated text) → see [`xml-reference.md`](reference/xml-reference.md#table-implementation)
5. Create arrows/shapes as PowerPoint objects → see [`xml-reference.md`](reference/xml-reference.md#arrow-shapes)
6. Insert company logo if provided in task files; if not available, flag to user: "[LOGO NOT PROVIDED - please supply company logo]"

### Phase 4: Validate → Fix → Repeat

**This is a feedback loop. Repeat until all checks pass OR escalation is triggered.**

```bash
# Convert to images for visual validation
soffice --headless --convert-to pdf presentation.pptx
pdftoppm -jpeg -r 150 presentation.pdf slide
```

**Validation checklist (check each slide image):**
- [ ] Text readable against background?
- [ ] Tables are actual objects (columns aligned, NOT pipe/tab-separated text)?
- [ ] Charts/tables fill designated areas?
- [ ] Bullet formatting consistent within sections?
- [ ] Font sizes match across same-level boxes?
- [ ] No content beyond slide boundaries?
- [ ] **No placeholder formatting retained** (no large colored boxes with data dumped in)?
- [ ] **No text-based "tables"** (no `|` or tab separators creating fake columns)?
- [ ] **Cross-slide consistency**: Same metrics/figures identical across all slides where they appear?

**Fix cycle protocol:**

| Cycle | Action |
|-------|--------|
| 1 | Fix all identified issues, re-validate |
| 2 | Fix remaining issues, re-validate |
| 3 | If issues persist, document remaining problems and escalate to user |

**After 3 cycles, if issues remain:**
1. List each unresolved issue with slide number and description
2. Explain what was attempted
3. Deliver the file with explicit disclaimer: "The following issues could not be resolved automatically: [list]. Manual review required."

**Do not** continue cycling indefinitely. Some issues (font rendering, complex shape alignment) may require manual intervention in PowerPoint.

### Phase 5: Final Verification

Run through the [Final Quality Checklist](#final-quality-checklist) before delivering.

---

## Quick Reference Tables

### Bullet Symbols

| Context | Symbol | Usage |
|---------|--------|-------|
| Included/Positive | ✓ | Items within scope, features present |
| Excluded/Negative | × | Items outside scope, features absent |
| Neutral list | • | General enumeration, commentary |
| Numbered sequence | 1. 2. 3. | Process steps, rankings |
| Sub-bullets | – | Secondary points under main bullets |

### Slide Hierarchy Levels (Typical)

These are typical ranges—adjust based on template specifications:

| Level | Examples | Typical Size | Style |
|-------|----------|--------------|-------|
| Title | Slide title | 40-48pt | Bold |
| Subtitle | Market definition, slide descriptor | 18-22pt | Bold |
| Section Header | "Key Projections", "Commentary" | 14-16pt | Regular |
| Block Label | "Segments Included", "Definition" sidebar | 12-14pt | Regular |
| Block Content | Bullet points, body text | 11-14pt | Regular |
| Table Header | Column headers | 10-12pt | Bold |
| Table Body | Cell content | 9-11pt | Regular |
| Footnotes | Sources, notes | 8-9pt | Italic |

### Font Consistency Matching

Boxes at the **same hierarchy level** MUST use identical font sizes:

| Same Level | Must Match With |
|------------|-----------------|
| "Segments Included" | "Segments Excluded" |
| "Definition" | "Scope Rationale" |
| Left column bullets | Right column bullets |
| All block labels | Each other |
| All section headers | Each other |

### Rounding for Presentation

These are **typical conventions** — adjust based on the magnitude of values and template style:

| Value Type | Typical Rounding | Example |
|------------|------------------|---------|
| Large market sizes ($10bn+) | Nearest $1bn | 18.5 → $19bn |
| Smaller market sizes (<$10bn) | Nearest $0.5bn or $0.1bn | 2.3 → $2.5bn |
| Size ranges | Match precision of sources | 14.9-22.1 → $15-22bn |
| CAGR | Whole % or 0.5% | 16.4% → 16% or 16.5% |
| Market share | Nearest 5% or match source | 21.4% → 20% |
| Multiples | 1 decimal | 9.69 → 9.7x |

**Principle:** Rounding should not materially change the figure. For smaller values, use finer precision.

### Text Density Rules

- Max 6-7 bullets per content box
- Max 2 lines per bullet point
- Parenthetical examples: same line or indented below
- No orphan words (single word on new line)

### Alignment Principles

**Vertically stacked boxes** must have identical:
- Left margin position, bullet indentation, text start position, box width

**Horizontally adjacent boxes** must have identical:
- Top position, height (where possible), internal padding

### Multi-Slide Consistency

When the same data appears on multiple slides:
- Use identical figures, formatting, and terminology
- If a metric is updated on one slide, update all occurrences
- Cross-reference during validation to catch mismatches

---

## MUST Requirements

These requirements are non-negotiable regardless of template:

| Requirement | Details |
|-------------|---------|
| **Text Readability** | All text MUST have sufficient contrast with background. Examples: white/light text on dark blue, dark green, black backgrounds; black/dark text on white, light gray, light yellow backgrounds. |
| **Actual Table Objects** | Tabular data MUST be table objects, not tab-separated text. See [`xml-reference.md`](reference/xml-reference.md#table-implementation). |
| **Proper Chart/Table Sizing** | Pasted visuals MUST fill designated area. See [`formatting-standards.md`](reference/formatting-standards.md#chart-and-image-handling). |
| **Consistent Formatting** | Bullets within section MUST match (symbol, size, indent). Same-level boxes MUST use same font size. |
| **Content Boundaries** | All content MUST stay within slide edges. Footnote box width: ~32.5cm for 16:9, ~24cm for 4:3. |
| **No Placeholder Formatting** | Remove colored instruction boxes. Main body: dark text on light background per template. |

---

## Critical Anti-Patterns: NEVER DO THESE

These failures occur when placeholder formatting is mistaken for output formatting. Recognizing these patterns is essential.

### Anti-Pattern 1: Populating Data INTO Placeholder Boxes

**What happens:** Template has colored instruction boxes (yellow, orange, etc.) with guidance text. Model replaces the guidance text with actual data BUT KEEPS THE COLORED BOX.

**Why it's wrong:** The colored box IS the placeholder. It tells you what content goes there. The output should have different formatting — typically dark text on white/light background, or properly styled shapes.

**Recognition test:** If your populated slide has large colored rectangles filled with data text, you have copied the placeholder format instead of replacing it.

**Critical distinction — two types of "placeholders":**

| Type | How to identify | What to do |
|------|-----------------|------------|
| **Instruction boxes** | Bright colors (yellow, orange), contains guidance text like "Insert X here", white/light text on colored background | DELETE the entire shape, then create new content with production formatting |
| **Layout placeholders** | Part of slide master/layout, neutral colors matching template theme, "Click to add text" | KEEP the shape, REPLACE the text content only |

If uncertain: check if the shape exists on an empty slide from the same template. Layout placeholders persist; instruction boxes are regular shapes.

### Anti-Pattern 2: Text-Based "Tables"

**What happens:** Model creates table-like content using separator characters (`|`, tabs, spaces) instead of actual table objects.

**Why it's wrong:** This is NOT a table. Columns will never align properly, it cannot be formatted consistently, and it looks unprofessional.

**Recognition test:** If you're typing `|` characters or relying on spaces/tabs to create columns, you're creating text, not a table.

**MUST verify:** After creating any table, verify it is an actual table object. See [`xml-reference.md`](reference/xml-reference.md#critical-verify-tables-are-actual-table-objects) for verification methods.

### Anti-Pattern 3: Inheriting Placeholder Contrast

**What happens:** Placeholder uses light text on colored background (e.g., white on yellow). Model populates data but keeps this color scheme, resulting in hard-to-read output.

**Why it's wrong:** Placeholder colors are deliberately distinct to signal "replace me." Production slides typically use dark text on light backgrounds for body content.

**Recognition test:** If your populated content has light/white text on bright colored backgrounds in body areas (not headers), you've inherited placeholder formatting.

**Correct approach:** Apply production formatting — typically dark text (#000000 or #333333) on white or light backgrounds for body content. Headers and accent areas may use brand colors.

### Summary: Placeholder vs. Production

| Element | Placeholder (Input) | Production (Output) |
|---------|---------------------|---------------------|
| Instruction boxes | Colored background, guidance text | Removed or reformatted |
| Data areas | "[Insert data here]" text | Actual data with clean formatting |
| Tables | Description of what table should contain | Actual table object with rows/columns |
| Body text | Light text on colored background | Dark text on light background |

**The placeholder tells you WHAT to create, not HOW to format it.**

---

## Common Failures

For detailed explanations of the most critical failures, see [Critical Anti-Patterns](#critical-anti-patterns-never-do-these) above.

| Failure | Solution | Reference |
|---------|----------|-----------|
| Unstructured text dumps | Break into bullets (✓, ×, •) | [`formatting-standards.md`](reference/formatting-standards.md#bullet-point-structure) |
| Pipe/tab-separated "tables" | Create actual table objects — text with separators is NOT a table | [`xml-reference.md`](reference/xml-reference.md#table-implementation) |
| Poor text/background contrast | Audit every text element | — |
| Tiny pasted charts | Resize to fill area, paste chart only | [`formatting-standards.md`](reference/formatting-standards.md#proper-sizing-workflow) |
| Source data pasted with charts | Select only chart object before copy | — |
| Data dumped into placeholder boxes | Delete colored instruction boxes, create new properly formatted content | [Anti-Patterns](#critical-anti-patterns-never-do-these) |
| Inconsistent bullets | Define style once, apply to all | [`formatting-standards.md`](reference/formatting-standards.md#bullet-consistency) |
| Inconsistent fonts across boxes | Standardize same-level boxes | [`formatting-standards.md`](reference/formatting-standards.md#font-consistency) |
| Content overflow | Set explicit box widths (footnotes: 32.5cm for 16:9, 24cm for 4:3) | — |
| Missing logo | Use logo from task files; if not provided, flag to user | — |
| Remaining `[brackets]` | Search and replace all placeholders | — |
| Text arrows (→, ⟹) | Use PowerPoint shape objects | [`xml-reference.md`](reference/xml-reference.md#arrow-shapes) |

---

## Error Handling

**If PDF/image conversion fails:**
1. Check LibreOffice is installed: `which soffice`
2. Try alternative: `libreoffice --headless --convert-to pdf presentation.pptx`
3. If still failing, open in PowerPoint/LibreOffice manually and export

**If source data has inconsistencies or conflicts:**
1. **Priority order**: Use data explicitly provided in the task files first
2. If using data from other sources (web search, external documents), flag this to the user
3. Document any discrepancies explicitly
4. Add footnote explaining data source choice

**If calculations don't match source projections:**
1. Show your calculation methodology
2. Note the discrepancy and possible causes (different base year, methodology)
3. Present both values if material difference
4. Flag to user for resolution

---

## Table Structure Guidelines

When creating tables (MUST be actual table objects):

**Column Alignment:**
- Text columns: Left-aligned (header and content)
- Numeric columns: Right-aligned or center-aligned (header matches content)

**Header Row:**
- Bold text
- Shaded background (template's brand color)
- White or contrasting text

**Consensus/Total Row:**
- Bold text
- Separator line above
- Distinct background shading

**Width:** Fill designated section width completely.

For XML implementation, see [`xml-reference.md`](reference/xml-reference.md#table-implementation).

---

## Footnote Format

**Format:**
```
Sources: [Source 1] (Year), [Source 2] (Year).
Notes: (1) [First note]; (2) [Second note].
```

**Example:**
```
Sources: Grand View Research (2024), Mordor Intelligence (2024), Markets and Markets (2023).
Notes: (1) Excludes hardware revenue; (2) Includes both B2B and B2C segments.
```

All superscript numbers (¹, ², ³) in slide body MUST have corresponding Notes entries.

---

## Logo Placement

- Use logo file provided in task materials
- If no logo provided, flag to user: "[LOGO NOT PROVIDED - please supply company logo]"
- Position: typically top-right, consistent size across slides, must not overlap content

---

## Data Requirements by Slide Type

For detailed data requirements, formatting principles, and example column headers for each slide type, see [`slide-templates.md`](reference/slide-templates.md#common-slide-types-and-data-requirements).

Common slide types covered: Market Definition, Market Sizing/TAM, Competitive Landscape, Financial Summary, Transaction Comparables.

---

## Final Quality Checklist

Before delivering the populated template, verify:

### Data Accuracy
- [ ] All figures match original source documents
- [ ] Calculated values verified against formulas (see [`calculation-standards.md`](reference/calculation-standards.md))
- [ ] Years and time periods are correct
- [ ] Company/competitor names spelled correctly
- [ ] Same figures are identical across all slides where they appear

### Content Mapping
- [ ] Every template section populated with appropriate data
- [ ] No `[bracket]` placeholder text remaining
- [ ] All source citations included in footnotes
- [ ] Footnote numbers (¹²³) have corresponding Notes entries

### Formatting
- [ ] Text readable against all backgrounds (sufficient contrast)
- [ ] Tables are actual table objects (NOT pipe/tab-separated text)
- [ ] Charts/tables fill designated areas (no thumbnails)
- [ ] Bullet formatting consistent within each section
- [ ] Font sizes match across same-level boxes
- [ ] No content extends beyond slide boundaries
- [ ] No placeholder boxes retained with data dumped inside
- [ ] No colored instruction boxes in final output

### Template Compliance
- [ ] Placeholder instruction boxes reformatted or removed
- [ ] Formatting matches template style (colors, fonts)
- [ ] Logo present and correctly positioned
- [ ] Production formatting applied (dark text on light background for main content)

### Final Step
- [ ] Recommend user validate in Microsoft PowerPoint before distribution (LibreOffice may render differently)

### Referencia: reference/calculation-standards.md

# Calculation Verification Reference

This file provides formulas and guidelines for verifying pre-calculated values in source data before populating templates. Source data should already contain calculated figures—use these formulas to verify accuracy.

## Contents

- [Key Verification Formulas](#key-verification-formulas)
- [Consensus Methodology](#consensus-methodology)
- [Rounding Guidelines](#rounding-guidelines)
- [Verification Checklist](#verification-checklist)
- [Red Flags to Investigate](#red-flags-to-investigate)

---

## Key Verification Formulas

### CAGR Projection

**Formula:**
```
Future Value = Present Value × (1 + CAGR)^n
```

**Variables:**
- Present Value: Current/base year market size
- CAGR: Compound Annual Growth Rate (as decimal, e.g., 16.4% = 0.164)
- n: Number of years between base and target year

**Verification example:**
```
Source claims: $22.1bn (2024) at 16.4% CAGR = $55.0bn (2030)

Verify: 22.1 × (1.164)^6 = 22.1 × 2.488 = 55.0 ✓
```

**Calculating n (years):** Count years between base and target year. Examples: 2024→2030 = 6 years, 2025→2030 = 5 years.

### Valuation Multiples

**EV/Revenue:**
```
EV/Revenue Multiple = Enterprise Value ÷ Revenue
Implied EV = Revenue × Multiple
```

**EV/EBITDA:**
```
EV/EBITDA Multiple = Enterprise Value ÷ EBITDA
Implied EV = EBITDA × Multiple
```

**Verification example:**
```
Source claims: $436m deal at 9.7x revenue multiple on $45m revenue

Verify: 436 ÷ 45 = 9.69 ≈ 9.7x ✓
```

### Market Share

**Formula:**
```
Market Share = (Segment Size ÷ Total Market Size) × 100
```

**Verification example:**
```
Source claims: Online segment ($18bn) is 28% of total market ($65bn)

Verify: 18 ÷ 65 = 0.277 = 27.7% ≈ 28% ✓
```

### Growth Rate

**Year-over-Year:**
```
YoY Growth = (Current Year - Prior Year) ÷ Prior Year × 100
```

**CAGR from endpoints:**
```
CAGR = (End Value ÷ Start Value)^(1/n) - 1
```

---

## Consensus Methodology

When source data contains multiple estimates, verify consensus calculations:

### Size Consensus (Range)

**Method:** Full min-max range across all sources

**Example:**
```
Sources: $14.9bn, $18.3bn, $21.1bn, $21.2bn, $22.1bn
Consensus: $15-22bn (rounded to nearest $1bn)
```

### CAGR Consensus (Central Cluster)

**Method:** Exclude outliers (highest and lowest), use central cluster range

**Example:**
```
Sources: 10.6%, 16.4%, 17.2%, 19.0%, 22.7%
Exclude outliers: 10.6% (low), 22.7% (high)
Central cluster: 16.4%, 17.2%, 19.0%
Consensus: 16-19% or 16-17% (conservative)
```

### Projection Consensus

**Method:** Apply consensus CAGR to midpoint of size range

**Example:**
```
Size range: $15-22bn → Midpoint: $18.5bn
CAGR consensus: 16-17%
At 16%: 18.5 × (1.16)^6 = $45.1bn
At 17%: 18.5 × (1.17)^6 = $47.5bn
Consensus projection: $45-48bn
```

---

## Rounding Guidelines

These are **typical conventions** — adjust based on the magnitude of values and template style:

| Value Type | Typical Rounding | Example |
|------------|------------------|---------|
| Large market sizes ($10bn+) | Nearest $1bn | 18.47 → $18bn |
| Smaller market sizes (<$10bn) | Nearest $0.5bn or $0.1bn | 2.3 → $2.5bn |
| Size ranges | Match precision of sources | 14.9-22.1 → $15-22bn |
| CAGR | Whole % or 0.5% | 16.4% → 16% or 16.5% |
| Market share | Nearest 5% or match source | 27.7% → 25% or 30% |
| Revenue ($m) | 1 decimal | 18.47 → $18.5m |
| Multiples | 1 decimal | 9.688 → 9.7x |

**Rounding principles:**
- Rounding should not materially change the figure — for smaller values, use finer precision
- Consistency matters more than precision — use same rounding across similar figures
- When creating ranges, round down for low end, round up for high end
- For summary statistics (mean, median), match precision of input data

---

## Verification Checklist

Before using any calculated value from source data:

### Formula Verification
- [ ] Projection uses correct CAGR formula: `PV × (1 + r)^n`
- [ ] Multiples calculated as EV ÷ Metric (not reversed)
- [ ] Growth rates use correct base year in denominator
- [ ] Percentage shares sum to ~100% where applicable

### Input Verification
- [ ] Base year figures match source documents
- [ ] CAGR/growth rates match stated source methodology
- [ ] Time periods (n) calculated correctly
- [ ] Currency and units consistent ($bn vs $m)

### Output Verification
- [ ] Calculated result matches source's stated figure
- [ ] If mismatch, investigate methodology difference
- [ ] Rounding applied consistently
- [ ] Results are plausible (no order-of-magnitude errors)

### Consensus Verification
- [ ] All sources included in range calculations
- [ ] Outlier exclusion methodology documented
- [ ] Midpoint calculations use correct averaging
- [ ] Range bounds represent actual min/max or documented subset

---

## Red Flags to Investigate

**Projection mismatches:**
- Calculated projection differs from source by >5%
- Likely cause: Different base year, different CAGR, or rounding

**Multiple mismatches:**
- Calculated multiple differs from source
- Likely cause: Different metric definition (LTM vs. NTM, Revenue vs. Net Revenue)

**Consensus mismatches:**
- Your consensus differs from source's consensus
- Likely cause: Source excluded certain data points, different outlier treatment

**When in doubt:** Note the discrepancy in a footnote and show your calculation methodology.

### Referencia: reference/formatting-standards.md

# Formatting Standards Reference

This reference file contains general PowerPoint formatting guidance for pitch deck creation. These are best practices that should be adapted to the specific template being used.

---

## Table of Contents

1. [Visual Hierarchy and Layout](#visual-hierarchy-and-layout)
2. [Text Formatting](#text-formatting)
3. [Table Creation](#table-creation)
4. [Chart and Image Handling](#chart-and-image-handling)
5. [Data Visualization](#data-visualization)
6. [Font Consistency](#font-consistency)
7. [Template Adaptation](#template-adaptation)

---

## Visual Hierarchy and Layout

### Box and Section Layout

Slide layouts vary based on content requirements and template design. Common elements include:
- Header sections with titles and subtitles
- Content boxes with label sidebars
- Tables for structured data
- Charts for visual data representation
- Footnote bars at slide bottom

The specific layout should follow the template provided. Common content types and their typical structures:
- **Market definition slides**: Label boxes with bullet content + commentary sections
- **TAM/sizing slides**: Metrics callouts + data tables + key takeaways
- **Competitive analysis**: Comparison tables or matrices
- **Financial summaries**: Charts with supporting data tables

### Alignment Principles

**Vertical alignment of parallel sections:**

Boxes that are vertically stacked should have consistent:
- Left margin position
- Bullet indentation
- Text start position
- Box width

Boxes that are horizontally adjacent should have consistent:
- Top position
- Height (where content allows)
- Internal padding

---

## Text Formatting

### Bullet Point Structure

Avoid unstructured text dumps. Break content into scannable bullet points.

**Illustrative Correct Structure:**
```
✓  Consumer mobile and web language learning apps
   (Duolingo, Babbel, Memrise, Busuu)
✓  B2B enterprise language training platforms
   (goFLUENT, Speexx, Learnship)
✓  Online tutoring marketplaces
   (italki, Preply, Cambly)
```

**Illustrative Incorrect Structure (Text Dump):**
```
Consumer mobile/web apps (Duolingo, Babbel, Memrise, Busuu)
B2B enterprise platforms (Speexx, Rosetta Stone Enterprise)
Online tutoring marketplaces (Preply, italki, Cambly)
```

### Bullet Symbol Guidelines

| Context | Symbol | Usage |
|---------|--------|-------|
| Included/Positive | ✓ (checkmark) | Items within scope, features present |
| Excluded/Negative | × (cross) | Items outside scope, features absent |
| Neutral list | • (bullet) | General enumeration, commentary |
| Numbered sequence | 1. 2. 3. | Process steps, rankings |
| Sub-bullets | ‣ or – | Secondary points under main bullets |

Adapt symbol usage to match the template's existing conventions.

### Bullet Consistency

All bullets within a box/section should have identical formatting:
- Same bullet symbol throughout the box (unless intentionally differentiated)
- Same indent level for all primary bullets
- Same bullet size
- Same spacing between bullet and text
- Same font size for all bullet text at same level

### Font Size Guidelines

These are typical ranges - adjust based on template specifications:

| Element | Typical Size (pt) | Style |
|---------|-------------------|-------|
| Slide Title | 40-48 | Bold |
| Subtitle/Definition | 18-22 | Bold |
| Section Headers | 14-16 | Regular |
| Body Text/Bullets | 12-14 | Regular |
| Table Headers | 10-12 | Bold |
| Table Body | 9-11 | Regular |
| Footnotes | 8-9 | Italic |

### Text Density Guidelines

- **Maximum 6-7 bullets** per content box (adjust based on space)
- **Maximum 2 lines** per bullet point
- **Parenthetical examples** on same line or indented below
- **Avoid orphan words** - adjust line breaks to avoid single words on new lines

---

## Table Creation

### CRITICAL: Use Actual Table Objects

**Tables must be actual table objects, NOT text with tab spacing.**

Text with tabs will never align properly and looks unprofessional. Always create proper table objects.

### Table Structure Guidelines

1. **Column alignment**:
   - Text columns: Left-aligned (both header and content)
   - Numeric columns: Center-aligned or right-aligned
   - Headers should align with their column content

2. **Header row**:
   - Bold text
   - Shaded background (use template's brand color)
   - Contrasting text color for readability
   - Alignment matches column content alignment

3. **Alternating rows** (optional):
   - Light shading on alternate rows improves readability

4. **Summary/Total row**:
   - Bold text
   - Heavier top border (separator line)
   - Distinct background shading

5. **Table width**:
   - Fill the designated section width
   - Avoid tables floating in white space

### For XML implementation patterns, see [`xml-reference.md`](xml-reference.md#table-implementation)

---

## Chart and Image Handling

### Pasting Charts from Excel

When pasting charts from Excel:

1. **Paste the chart ONLY** - do not include source data tables
2. **Resize to fill the designated area** - charts should not appear as tiny thumbnails
3. **Maintain aspect ratio** - do not distort the chart
4. **Verify readability** - axis labels, legends, data labels must be legible

### Pasting Tables from Excel

When pasting tables from Excel:

1. **Paste the formatted table ONLY** - exclude any source data or calculations
2. **Resize to fill the designated area** - table should occupy its full section
3. **Verify column widths** - adjust so text is not truncated
4. **Check formatting preservation** - colors, borders, fonts may need adjustment

### Size Guidelines

**Minimum sizing principles:**
- Charts: Should occupy a substantial portion of their designated area
- Tables: Fill the designated section width completely
- Images: Sized appropriately for context, never thumbnail-sized

**Indicators of undersized visuals (avoid these):**
- Chart occupies small fraction of available space
- Text labels are unreadable
- Large empty areas surrounding the visual
- Visual appears as a "thumbnail"

### Proper Sizing Workflow

1. Identify the target area dimensions
2. Paste the chart/table
3. Immediately resize to fill the target area
4. Verify all text remains readable
5. Adjust internal elements if needed (legend position, axis labels)

---

## Data Visualization

### Key Metrics Display

When displaying key metrics (e.g., TAM, CAGR, projections), consider showing relationships between values rather than listing them statically:

- **Visual flow indicators**: Shapes (arrows, chevrons, connectors) showing progression
- **Size hierarchy**: Larger font for primary metrics, smaller for labels
- **Spatial arrangement**: Position elements to show logical flow

### Arrow and Flow Indicators

If using arrows or flow indicators:
- Use PowerPoint shape objects, not text characters
- Do not use text-based arrows (→, ⟹) in the final presentation
- Create arrows using PowerPoint's shape tools or via XML shape elements

**For XML implementation, see [`xml-reference.md`](xml-reference.md#arrow-shapes)**

---

## Font Consistency

### Cross-Box Font Consistency

All text boxes at the same hierarchy level should use identical font sizes.

**Same-level boxes that should match:**

| Box Type | Should Match With |
|----------|-------------------|
| "Segments Included" content | "Segments Excluded" content |
| "Definition" content | "Scope Rationale" content |
| Left column bullets | Right column bullets |
| All label boxes | Each other |
| All section headers | Each other |

### Verification Process

1. Identify all text boxes at the same hierarchy level
2. Check font size of each box
3. If any box differs, adjust all to match
4. Default to the larger size if content fits; otherwise use the smaller size consistently

**Exception**: Sub-bullets or secondary text may use smaller font than primary bullets, but this must be consistent across ALL boxes.

---

## Template Adaptation

These standards should be adapted to match the specific template being used:

1. **Colors**: Use the template's brand colors rather than prescribing specific colors
2. **Fonts**: Use the template's font family
3. **Spacing**: Match the template's existing spacing conventions
4. **Layout**: Follow the template's section structure

The key principles that remain constant regardless of template:
- Text must be readable against its background
- Tables must be actual table objects
- Content should fill available space appropriately
- Formatting should be consistent across parallel elements
- Charts/images should be properly sized

### Referencia: reference/slide-templates.md

# Content Mapping Reference

This file provides guidance for mapping source data to pitch deck template sections. The process is template-agnostic—these principles apply regardless of the specific template design.

## Contents

- [Template Analysis Process](#template-analysis-process)
- [Content Mapping Workflow](#content-mapping-workflow)
- [Common Slide Types and Data Requirements](#common-slide-types-and-data-requirements)
- [Mapping Verification Checklist](#mapping-verification-checklist)
- [Handling Data-Template Mismatches](#handling-data-template-mismatches)
- [Template-Specific Adaptation](#template-specific-adaptation)

---

## Template Analysis Process

Before populating any template, analyze its structure:

### Step 1: Identify All Content Areas

Scan each slide for:
- **Title/header placeholders** — Where slide titles go
- **Subtitle/definition areas** — Secondary headers or definitions
- **Content boxes** — Main content areas (may have label sidebars)
- **Table placeholders** — Areas designated for tabular data
- **Chart/visual areas** — Spaces for charts, diagrams, or images
- **Metric callout boxes** — Highlighted key figures
- **Footnote/source bars** — Bottom areas for citations and notes
- **Logo placeholder** — Usually top-right corner

### Step 2: Note Template Conventions

Each template has its own style. Observe:
- **Color scheme** — What colors are used for headers, backgrounds, accents?
- **Font choices** — What fonts and sizes are already set?
- **Box styling** — Do content boxes have sidebars, borders, or shading?
- **Bullet styles** — What bullet symbols does the template use?
- **Alignment patterns** — How are parallel sections aligned?

### Step 3: Identify Instruction vs. Output Areas

Templates often include guidance:
- **Instruction boxes** — Colored boxes with guidance text (often yellow background, white text)
- **Placeholder text** — Text in [brackets] indicating what to replace
- **Example content** — Sample content showing expected format

**Key distinction**: Instruction boxes tell you what to do; they should be reformatted or removed in final output. Output areas are where your content goes.

---

## Content Mapping Workflow

### Step 1: Inventory Source Data

Create a list of all available data:
- Market size figures and ranges
- Growth rates (CAGR, YoY)
- Company names and descriptions
- Segment definitions
- Financial metrics
- Source citations and dates
- Footnote content

### Step 2: Match Data to Template Sections

For each template section, identify:

| Template Section | Required Data | Source Location |
|------------------|---------------|-----------------|
| [Section name] | [Data needed] | [Where to find it] |

### Step 3: Identify Gaps

After mapping, note:
- **Missing data** — Template requires data not in sources
- **Extra data** — Sources contain data with no template home
- **Format mismatches** — Data exists but in wrong format

### Step 4: Resolve Gaps Before Populating

- Missing data: Flag for user or search for additional sources
- Extra data: Confirm if it should be excluded or if template needs adjustment
- Format mismatches: Transform data to required format

---

## Common Slide Types and Data Requirements

These are typical data requirements for common slide types. Your specific template may vary—always follow the template's actual structure.

### Market Definition Slides

**Typical content areas:**
- Segments included in scope (with examples/key players)
- Segments excluded from scope (with examples)
- Market definition text
- Scope rationale/justification

**Data mapping considerations:**
- Source data should clearly distinguish included vs. excluded segments
- Key players should be mapped to their respective segments
- Definition text should align with how sources define the market

**Data typically needed:**
- List of market segments to include (with key player examples)
- List of market segments to exclude (with examples)
- Market definition text
- Scope rationale or justification

**Formatting principle:** Parallel sections (included vs. excluded) should use matching formatting.

**Verification questions:**
- Does every segment have the appropriate symbol (✓ for included, × for excluded)?
- Are key players correctly assigned to segments?
- Does the definition match the source methodology?

### Market Sizing / TAM Slides

**Typical content areas:**
- Current market size (with year)
- Growth rate (CAGR with period)
- Future projection (with target year)
- Source-by-source breakdown table
- Consensus/summary figures
- Key takeaways or insights

**Data typically needed:**
- Market size figures with base year
- Growth rates (CAGR with time period)
- Projection figures with target year
- Source citations for each data point

**Example column headers:** Source | [Base Year] Size | CAGR | [Target Year] Projection

**Formatting principle:** If showing multiple sources, include a consensus/summary row.

**Data mapping considerations:**
- Multiple sources may have different estimates—map each to table rows
- Consensus figures require calculation from individual sources
- Projections should be verifiable using CAGR formula

**Verification questions:**
- Do all source figures match original documents?
- Is the consensus calculated correctly (not just copied from one source)?
- Are projection years consistent across all figures?
- Do CAGR-based projections match when manually verified?

### Competitive Landscape Slides

**Typical content areas:**
- Comparison table with competitors as columns
- Feature/capability rows
- Financial metric rows (revenue, growth, market share)
- Key observations or positioning notes

**Data typically needed:**
- List of competitors to compare
- Features or capabilities for each
- Financial metrics (revenue, growth, market share) if available
- Time period for financial data

**Formatting principle:** Subject company should be visually distinguished from competitors (e.g., bold text, different background color, border, or positioned in rightmost column).

**Data mapping considerations:**
- Ensure all competitors from source data are included
- Feature comparisons should use consistent criteria
- Financial figures should be from comparable periods

**Verification questions:**
- Are all competitors from the source data represented?
- Is the subject company visually distinguished?
- Are financial figures from the same time period?
- Is the ✓/× usage consistent and accurate?

### Financial Summary Slides

**Typical content areas:**
- Key metric callouts (headline figures)
- Historical financials table (actuals)
- Projected financials table (estimates)
- Growth rates and margins
- Optional trend charts

**Data typically needed:**
- Historical financials (actuals) for recent years
- Projected financials (estimates) for future years
- Key metrics: Revenue, Growth %, Margins, EBITDA

**Example column headers:** Metric | FY[Year-2] | FY[Year-1] | FY[Year]A | FY[Year+1]E | FY[Year+2]E

**Formatting principle:** Clearly distinguish historical (A) from projected (E) data.

**Data mapping considerations:**
- Clearly distinguish historical (A) from projected (E) data
- Ensure metric definitions match source (Revenue vs. Net Revenue, EBITDA vs. Adjusted EBITDA)
- Growth rates should be calculated consistently

**Verification questions:**
- Are historical vs. projected periods clearly labeled?
- Do calculated growth rates match source or manual calculation?
- Are metric definitions consistent with source documents?

### Transaction Comparables Slides

**Typical content areas:**
- Transaction table (date, target, acquirer, deal value)
- Valuation multiples (EV/Revenue, EV/EBITDA)
- Summary statistics (mean, median, high, low)
- Implied valuation for subject company

**Data typically needed:**
- Transaction details: Date, Target, Acquirer, Deal Value
- Valuation multiples: EV/Revenue, EV/EBITDA
- Subject company metrics for implied valuation

**Formatting principle:** Include summary statistics (Mean, Median, High, Low) for multiples.

**Data mapping considerations:**
- Multiples should be calculated from transaction data, not just copied
- Summary statistics require calculation across all transactions
- Implied valuation applies multiples to subject company metrics

**Verification questions:**
- Are all relevant transactions from the source included?
- Are multiples calculated correctly (EV ÷ Metric)?
- Do summary statistics cover all transactions in the table?
- Is implied valuation clearly labeled as illustrative?

---

## Mapping Verification Checklist

Before moving to formatting, verify mapping completeness:

### Data Completeness
- [ ] Every template placeholder has mapped source data
- [ ] All source citations are recorded for footnotes
- [ ] No placeholder [brackets] remain unmapped

### Data Accuracy
- [ ] Figures match original source documents exactly
- [ ] Years and time periods are correctly noted
- [ ] Company names are spelled correctly
- [ ] Calculated values (consensus, projections, multiples) verified

### Logical Consistency
- [ ] Included vs. excluded segments are logically coherent
- [ ] Historical data precedes projected data chronologically
- [ ] Comparison data uses consistent time periods
- [ ] Totals and subtotals sum correctly

### Source Attribution
- [ ] Every data point can be traced to a source
- [ ] Source names and publication years recorded
- [ ] Footnote numbers assigned for special notes

---

## Handling Data-Template Mismatches

### Template Requires More Data Than Available

**Options:**
1. Flag the gap explicitly for user review
2. Mark section as "Data not available" with explanation
3. Search for additional sources if appropriate
4. Recommend template adjustment if data doesn't exist

**Do not:** Fabricate data or make unsupported estimates.

### Source Has More Data Than Template Accommodates

**Options:**
1. Include most relevant/recent data points
2. Summarize or aggregate where appropriate
3. Add footnotes referencing additional available data
4. Recommend template expansion if data is critical

### Data Format Doesn't Match Template Format

**Common transformations:**
- Individual figures → Range (use min-max from sources)
- Detailed breakdown → Summary category
- Annual figures → CAGR (calculate from endpoints)
- Absolute values → Percentages (calculate share)
- Multiple sources → Consensus (apply methodology)

### Template Uses Different Terminology

**Resolution process:**
1. Identify template term and source term
2. Confirm they refer to the same concept
3. Use template terminology in output
4. Add footnote if clarification needed

---

## Template-Specific Adaptation

Remember: This guidance describes common patterns, not requirements. Always:

1. **Follow the template** — If template uses different section names, use those
2. **Match template style** — Use template's existing fonts, colors, bullet styles
3. **Preserve template structure** — Don't rearrange sections unless necessary
4. **Respect template spacing** — Content should fit designated areas without overflow

The goal is to populate the template as designed, not to redesign it.

### Referencia: reference/xml-reference.md

# PowerPoint XML Reference

This file contains XML patterns for programmatic PowerPoint editing. Use these patterns when working directly with OOXML format.

**Note:** Color values in examples (e.g., `E67E22`, `D35400`) are placeholders. Replace with your template's brand colors.

---

## ⚠️ When to Use This Reference

**Use python-pptx for:**
- Creating new tables (handles cell structure and relationships automatically)
- Adding text boxes
- Inserting images
- Most shape creation
- Any operation where python-pptx provides an API

**Use direct XML editing only for:**
- Modifying properties of existing elements that python-pptx doesn't expose
- Fine-tuning cell formatting after table creation via python-pptx
- Adjusting specific shape properties not available via the python-pptx API

**NEVER use direct XML for:**
- Creating tables from scratch (relationship management is error-prone and will likely corrupt the file)
- Initial shape creation (shape ID collision risk)
- Anything you can accomplish via python-pptx

The XML patterns in this file are for **reference and targeted modifications**, not wholesale element construction.

---

## XML Editing Risks

Direct XML editing can corrupt PowerPoint files if not done carefully:
- PowerPoint XML has interdependencies (relationship files, content types)
- Invalid XML or missing relationships can corrupt the entire file
- Shape IDs must be unique across each slide

**Always work on a backup copy** — never edit the original file directly.

---

## Contents
- [Table Implementation](#table-implementation)
- [Arrow Shapes](#arrow-shapes)
- [Text Boxes](#text-boxes)
- [Shapes with Fill](#shapes-with-fill)
- [Image Insertion](#image-insertion)
- [Connector Lines](#connector-lines)
- [Unit Conversions](#unit-conversions)

---

## Table Implementation

### CRITICAL: Verify Tables Are Actual Table Objects

After creating any table, you MUST verify it is an actual table object, not text with separators.

**Programmatic verification (python-pptx):**
```python
for shape in slide.shapes:
    if shape.has_table:
        print(f"✓ Found table: {len(shape.table.rows)} rows, {len(shape.table.columns)} columns")
```

**Visual verification (in exported image):**
- Columns align perfectly regardless of content length
- Cell borders are consistent
- Selecting the table selects all cells as a unit

**Failure indicators — you have created TEXT, not a table:**
- `|` characters visible between values
- Columns misalign when content length varies
- Tab characters (`\t`) used for spacing
- Multiple text boxes arranged to look like a table

Text-based "tables" cannot be edited by the recipient, will misalign when fonts change, and signal amateur work. There is no acceptable use case for pipe/tab-separated tabular data in a pitch deck.

---

### Basic Table Structure

```xml
<a:tbl>
  <a:tblPr firstRow="1" bandRow="1">
    <a:tableStyleId>{5C22544A-7EE6-4342-B048-85BDC9FD1C3A}</a:tableStyleId>
  </a:tblPr>
  <a:tblGrid>
    <a:gridCol w="2000000"/>  <!-- Source column - width in EMUs -->
    <a:gridCol w="1200000"/>  <!-- 2024 Size column -->
    <a:gridCol w="1200000"/>  <!-- CAGR column -->
    <a:gridCol w="1200000"/>  <!-- 2030 Projection column -->
  </a:tblGrid>
  <!-- Row definitions follow -->
</a:tbl>
```

### Table Row with Cells

```xml
<a:tr h="370840">  <!-- Row height in EMUs -->
  <a:tc>
    <a:txBody>
      <a:bodyPr/>
      <a:lstStyle/>
      <a:p>
        <a:pPr algn="l"/>  <!-- Left alignment for text columns -->
        <a:r>
          <a:rPr lang="en-US" sz="1000" b="0"/>
          <a:t>Grand View Research</a:t>
        </a:r>
      </a:p>
    </a:txBody>
    <a:tcPr/>
  </a:tc>
  <a:tc>
    <a:txBody>
      <a:bodyPr/>
      <a:lstStyle/>
      <a:p>
        <a:pPr algn="ctr"/>  <!-- Center alignment for numeric columns -->
        <a:r>
          <a:rPr lang="en-US" sz="1000"/>
          <a:t>22.1</a:t>
        </a:r>
      </a:p>
    </a:txBody>
    <a:tcPr/>
  </a:tc>
  <!-- Additional cells... -->
</a:tr>
```

### Header Row Styling

```xml
<a:tr h="370840">
  <a:tc>
    <a:txBody>
      <a:bodyPr/>
      <a:lstStyle/>
      <a:p>
        <a:pPr algn="l"/>
        <a:r>
          <a:rPr lang="en-US" sz="1000" b="1">  <!-- Bold for headers -->
            <a:solidFill>
              <a:srgbClr val="FFFFFF"/>  <!-- White text -->
            </a:solidFill>
          </a:rPr>
          <a:t>Source</a:t>
        </a:r>
      </a:p>
    </a:txBody>
    <a:tcPr>
      <a:solidFill>
        <a:srgbClr val="E67E22"/>  <!-- Orange background -->
      </a:solidFill>
    </a:tcPr>
  </a:tc>
  <!-- Additional header cells... -->
</a:tr>
```

---

## Arrow Shapes

### Right Arrow Shape

```xml
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="10" name="Arrow Right"/>
    <p:cNvSpPr/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="3000000" y="2500000"/>  <!-- Position in EMUs -->
      <a:ext cx="500000" cy="300000"/>   <!-- Size in EMUs -->
    </a:xfrm>
    <a:prstGeom prst="rightArrow">
      <a:avLst/>
    </a:prstGeom>
    <a:solidFill>
      <a:srgbClr val="E67E22"/>  <!-- Arrow fill color -->
    </a:solidFill>
    <a:ln>
      <a:noFill/>  <!-- No outline -->
    </a:ln>
  </p:spPr>
</p:sp>
```

### Down Arrow Shape

```xml
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="11" name="Arrow Down"/>
    <p:cNvSpPr/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="2500000" y="3000000"/>
      <a:ext cx="300000" cy="500000"/>
    </a:xfrm>
    <a:prstGeom prst="downArrow">
      <a:avLst/>
    </a:prstGeom>
    <a:solidFill>
      <a:srgbClr val="E67E22"/>
    </a:solidFill>
  </p:spPr>
</p:sp>
```

### Chevron Shape

```xml
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="12" name="Chevron"/>
    <p:cNvSpPr/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="3000000" y="2500000"/>
      <a:ext cx="400000" cy="600000"/>
    </a:xfrm>
    <a:prstGeom prst="chevron">
      <a:avLst/>
    </a:prstGeom>
    <a:solidFill>
      <a:srgbClr val="E67E22"/>
    </a:solidFill>
  </p:spPr>
</p:sp>
```

---

## Text Boxes

### Basic Text Box

```xml
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="5" name="TextBox 4"/>
    <p:cNvSpPr txBox="1"/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="500000" y="1500000"/>
      <a:ext cx="4000000" cy="500000"/>
    </a:xfrm>
    <a:prstGeom prst="rect">
      <a:avLst/>
    </a:prstGeom>
    <a:noFill/>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" rtlCol="0">
      <a:spAutoFit/>
    </a:bodyPr>
    <a:lstStyle/>
    <a:p>
      <a:r>
        <a:rPr lang="en-US" sz="1400" dirty="0"/>
        <a:t>Text content here</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

### Text Box with Bullet Points

```xml
<p:txBody>
  <a:bodyPr wrap="square">
    <a:spAutoFit/>
  </a:bodyPr>
  <a:lstStyle/>
  <a:p>
    <a:pPr marL="342900" indent="-342900">
      <a:buFont typeface="Wingdings" panose="05000000000000000000" pitchFamily="2" charset="2"/>
      <a:buChar char="&#252;"/>  <!-- Checkmark character -->
    </a:pPr>
    <a:r>
      <a:rPr lang="en-US" sz="1400" dirty="0"/>
      <a:t>First bullet point</a:t>
    </a:r>
  </a:p>
  <a:p>
    <a:pPr marL="342900" indent="-342900">
      <a:buFont typeface="Wingdings" panose="05000000000000000000" pitchFamily="2" charset="2"/>
      <a:buChar char="&#252;"/>
    </a:pPr>
    <a:r>
      <a:rPr lang="en-US" sz="1400" dirty="0"/>
      <a:t>Second bullet point</a:t>
    </a:r>
  </a:p>
</p:txBody>
```

### Text with White Color (for dark backgrounds)

```xml
<a:r>
  <a:rPr lang="en-US" sz="1000" b="1" i="1" dirty="0">
    <a:solidFill>
      <a:srgbClr val="FFFFFF"/>  <!-- White text -->
    </a:solidFill>
  </a:rPr>
  <a:t>White text on colored background</a:t>
</a:r>
```

---

## Shapes with Fill

### Rectangle with Solid Fill

```xml
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="20" name="Rectangle 19"/>
    <p:cNvSpPr/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="500000" y="2500000"/>
      <a:ext cx="1000000" cy="2000000"/>
    </a:xfrm>
    <a:prstGeom prst="rect">
      <a:avLst/>
    </a:prstGeom>
    <a:solidFill>
      <a:srgbClr val="E67E22"/>  <!-- Orange fill -->
    </a:solidFill>
    <a:ln w="12700">  <!-- Border width -->
      <a:solidFill>
        <a:srgbClr val="D35400"/>  <!-- Darker border -->
      </a:solidFill>
    </a:ln>
  </p:spPr>
  <p:txBody>
    <a:bodyPr rtlCol="0" anchor="ctr"/>  <!-- Vertically centered text -->
    <a:lstStyle/>
    <a:p>
      <a:pPr algn="ctr"/>  <!-- Horizontally centered -->
      <a:r>
        <a:rPr lang="en-US" sz="1600" b="1">
          <a:solidFill>
            <a:srgbClr val="FFFFFF"/>
          </a:solidFill>
        </a:rPr>
        <a:t>Label Text</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

---

## Image Insertion

### Adding Image to Slide

```xml
<p:pic>
  <p:nvPicPr>
    <p:cNvPr id="99" name="Company Logo"/>
    <p:cNvPicPr>
      <a:picLocks noChangeAspect="1"/>
    </p:cNvPicPr>
    <p:nvPr/>
  </p:nvPicPr>
  <p:blipFill>
    <a:blip r:embed="rIdLogo"/>  <!-- Reference to relationship ID -->
    <a:stretch>
      <a:fillRect/>
    </a:stretch>
  </p:blipFill>
  <p:spPr>
    <a:xfrm>
      <a:off x="10800000" y="200000"/>  <!-- Top-right position -->
      <a:ext cx="800000" cy="600000"/>   <!-- Logo dimensions -->
    </a:xfrm>
    <a:prstGeom prst="rect">
      <a:avLst/>
    </a:prstGeom>
  </p:spPr>
</p:pic>
```

### Adding Image Relationship

In `ppt/slides/_rels/slideN.xml.rels`:

```xml
<Relationship Id="rIdLogo" 
  Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" 
  Target="../media/logo.png"/>
```

---

## Connector Lines

### Straight Connector

```xml
<p:cxnSp>
  <p:nvCxnSpPr>
    <p:cNvPr id="15" name="Straight Connector 14"/>
    <p:cNvCxnSpPr>
      <a:cxnSpLocks/>
    </p:cNvCxnSpPr>
    <p:nvPr/>
  </p:nvCxnSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="500000" y="2500000"/>
      <a:ext cx="5000000" cy="0"/>  <!-- Horizontal line -->
    </a:xfrm>
    <a:prstGeom prst="line">
      <a:avLst/>
    </a:prstGeom>
    <a:ln w="12700">
      <a:solidFill>
        <a:srgbClr val="E67E22"/>
      </a:solidFill>
    </a:ln>
  </p:spPr>
</p:cxnSp>
```

### Dashed Line

```xml
<p:spPr>
  <a:xfrm>
    <a:off x="500000" y="4500000"/>
    <a:ext cx="5000000" cy="0"/>
  </a:xfrm>
  <a:prstGeom prst="line">
    <a:avLst/>
  </a:prstGeom>
  <a:ln w="12700">
    <a:solidFill>
      <a:srgbClr val="E67E22"/>
    </a:solidFill>
    <a:prstDash val="dash"/>  <!-- Dashed style -->
  </a:ln>
</p:spPr>
```

---

## Unit Conversions

| Unit | EMUs per unit |
|------|---------------|
| 1 inch | 914400 |
| 1 cm | 360000 |
| 1 point | 12700 |
| 1 pixel (96 DPI) | 9525 |

### Common Slide Dimensions (16:9)

- Width: 12192000 EMUs (13.333 inches)
- Height: 6858000 EMUs (7.5 inches)

### Typical Element Positions

| Element | X Position | Y Position |
|---------|------------|------------|
| Logo (top-right) | 10800000 | 200000 |
| Title | 342583 | 286603 |
| Subtitle | 402591 | 1767390 |
| Footer | 342583 | 6435334 |


---

## SKILL: process-letter

- Fuente: `anthropics/financial-services` → `plugins/vertical-plugins/investment-banking/skills/process-letter` (Apache-2.0)
- Cuándo usarla: Draft process letters and bid instructions for sell-side M&A processes. Covers initial indication of interest (IOI) instructions, final bid procedures, and management meeting logistics. Triggers on "process letter", "bid instructions", "IOI letter", "bid procedures", "final round letter", or "management meeting invite".

# Process Letter

## Workflow

### Step 1: Determine Letter Type

- **Initial process letter**: Sent with teaser/CIM to outline the process and IOI requirements
- **IOI instructions**: Specific requirements for first-round indications of interest
- **Second round / final bid letter**: Instructions for submitting binding offers after diligence
- **Management meeting invitation**: Logistics for in-person management presentations

### Step 2: Initial Process Letter / IOI Instructions

**Header:**
- Date, deal code name
- "Confidential"
- Addressed to prospective buyer

**Sections:**

1. **Introduction**: Brief overview of the opportunity and the seller's objectives
2. **Process Overview**: Timeline, key dates, expected number of rounds
3. **IOI Requirements**: What to include in the initial indication:
   - Proposed valuation range (enterprise value)
   - Consideration form (cash, stock, earnout, rollover)
   - Financing sources and certainty
   - Key due diligence requirements
   - Indicative timeline to close
   - Any conditions or contingencies
   - Brief description of the buyer and strategic rationale
4. **Submission Details**: Where to send, deadline (date and time), format
5. **Confidentiality Reminder**: Reference to NDA, data room access
6. **Contact Information**: Banker contacts for questions

### Step 3: Final Bid / Second Round Letter

Additional requirements beyond IOI:

1. **Markup of purchase agreement**: Provide the draft SPA/APA and request markup
2. **Detailed financing commitments**: Committed financing letters required
3. **Remaining diligence items**: Specify what confirmatory diligence is expected
4. **Exclusivity terms**: Duration and conditions of any exclusivity period
5. **Regulatory analysis**: Antitrust filing requirements and timeline
6. **Key personnel terms**: Employment agreements, compensation, rollover equity
7. **Binding vs. non-binding**: Clarify what is binding at this stage
8. **Evaluation criteria**: How bids will be evaluated (price, certainty, speed, fit)

### Step 4: Management Meeting Invitation

1. **Logistics**: Date, time, location (or video link), duration
2. **Attendees**: Who from the company will present, who from the buyer should attend
3. **Agenda**: Typical management presentation agenda (overview, financials, operations, growth, Q&A)
4. **Ground rules**: No recording, confidentiality, questions format
5. **Materials**: What will be distributed (presentation deck, data room access)
6. **Follow-up**: Process for submitting additional questions after the meeting

### Step 5: Output

- Word document (.docx) with professional letter formatting
- Firm letterhead placeholder
- Track changes version for client review

## Important Notes

- Process letters set the tone for the entire deal — be clear, professional, and organized
- Deadlines should be firm but reasonable — typically 2-3 weeks for IOIs, 3-4 weeks for final bids
- Always include the evaluation criteria — buyers want to know how they'll be judged
- Coordinate with legal on any representations or commitments in the letter
- Client should review and approve before sending — they may want to adjust tone or terms
- Keep a log of who received each letter and when — this becomes the process tracker


---

## SKILL: teaser

- Fuente: `anthropics/financial-services` → `plugins/vertical-plugins/investment-banking/skills/teaser` (Apache-2.0)
- Cuándo usarla: Draft anonymous one-page company teasers for sell-side M&A processes. Creates a compelling summary without revealing the company's identity, designed to gauge buyer interest before NDA execution. Triggers on "teaser", "blind teaser", "anonymous profile", "one-pager for process", or "draft teaser for sell-side".

# Teaser

## Workflow

### Step 1: Gather Inputs

- Company description (what they do, how they make money)
- Sector / industry
- Key financial metrics: revenue, EBITDA, growth rate, margins
- Geographic footprint
- Key selling points (3-5 highlights)
- What to anonymize vs. disclose
- Target buyer audience (strategic, financial, or both)

### Step 2: Teaser Structure

One page, professionally formatted:

**Header**
- Deal code name (e.g., "Project [Name]")
- Sector descriptor (e.g., "Leading Specialty Industrial Services Platform")
- "Confidential — For Discussion Purposes Only"

**Company Description** (2-3 sentences)
- What the company does, without naming it
- Market position (e.g., "a leading provider of...", "a top-3 player in...")
- Geography (region-level, not city-specific)

**Investment Highlights** (4-6 bullet points)
- Market leadership / positioning
- Revenue quality (recurring %, retention, diversification)
- Growth profile and trajectory
- Margin profile and expansion opportunity
- Management team strength
- Strategic value / synergy potential

**Financial Summary** (table or key metrics)

| Metric | Value |
|--------|-------|
| Revenue | $XXM |
| Revenue Growth | XX% CAGR |
| EBITDA | $XXM |
| EBITDA Margin | XX% |
| Employees | XXX |

**Transaction Overview** (2-3 sentences)
- What's being offered (100% sale, majority stake, growth equity)
- Indicative timeline
- Contact information for expressions of interest

### Step 3: Anonymization Check

Ensure the teaser doesn't inadvertently identify the company:
- No company name, brand names, or product names
- No specific city (use region: "Southeast US", "Midwest")
- No named customers or partners
- No employee count if it's too distinctive
- Revenue ranges instead of exact figures if the sector is small
- No logos, screenshots, or identifiable imagery

### Step 4: Output

- Word document (.docx) — one page, clean formatting
- PDF version for distribution
- Optional PowerPoint version (single slide)

## Important Notes

- The teaser's job is to generate interest, not close a deal — keep it tight and compelling
- Less is more — a good teaser makes buyers want to sign the NDA to learn more
- Use aspirational but accurate language — "leading", "differentiated", "high-growth" are fine if true
- Include enough financial detail to qualify serious buyers but not so much that tire-kickers waste your time
- Always have the client and legal review before distribution
- Track who receives the teaser — it becomes the outreach log for the process


---

## SKILL: value-creation-plan

- Fuente: `anthropics/financial-services` → `plugins/vertical-plugins/private-equity/skills/value-creation-plan` (Apache-2.0)
- Cuándo usarla: Structure post-acquisition value creation plans with revenue, cost, and operational levers mapped to an EBITDA bridge. Includes 100-day priorities, KPI targets, and accountability frameworks. Use when planning post-close execution, preparing operating partner materials, or building a board-ready value creation roadmap. Triggers on "value creation plan", "100-day plan", "post-close plan", "EBITDA bridge", "operating plan", or "value creation levers".

# Value Creation Plan

## Workflow

### Step 1: Baseline Assessment

Understand the starting point:
- Current revenue, EBITDA, and margins
- Organizational structure and capabilities
- Key operational metrics by function
- Management team strengths and gaps
- Quick wins already identified during diligence

### Step 2: Value Creation Levers

Map all levers to an EBITDA bridge over the hold period:

#### Revenue Growth Levers
- **Organic growth**: Price increases, volume growth, market expansion
- **Cross-sell / upsell**: New products to existing customers
- **New market entry**: Geographic expansion, new verticals, new channels
- **Sales force effectiveness**: Hire reps, improve conversion, shorten cycle
- **M&A / add-ons**: Bolt-on acquisitions to add revenue and capabilities

For each lever:
- Current state → Target state
- Revenue impact ($)
- Timeline to impact
- Investment required
- Confidence level (high/medium/low)

#### Margin Expansion Levers
- **Pricing optimization**: Price increases, mix shift, bundling
- **COGS reduction**: Procurement savings, supplier consolidation, automation
- **OpEx optimization**: Overhead reduction, shared services, offshoring
- **Technology investment**: Automation, systems integration, data analytics
- **Scale leverage**: Fixed cost leverage as revenue grows

#### Strategic / Multiple Expansion
- **Platform building**: Add-on acquisitions, tuck-ins
- **Recurring revenue shift**: Move from project to recurring/subscription
- **Market positioning**: Category leadership, brand building
- **Management upgrades**: Key hires to professionalize the business
- **ESG / governance**: Board formation, reporting improvements

### Step 3: EBITDA Bridge

Build the walk from current to target EBITDA:

| Lever | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
|-------|--------|--------|--------|--------|--------|
| Base EBITDA | | | | | |
| Organic revenue growth | | | | | |
| Pricing | | | | | |
| Add-on M&A | | | | | |
| COGS savings | | | | | |
| OpEx optimization | | | | | |
| Technology investment | | | | | |
| **Pro Forma EBITDA** | | | | | |
| **Margin** | | | | | |

### Step 4: 100-Day Plan

Prioritize the first 100 days post-close:

**Days 1-30: Stabilize & Assess**
- Management alignment and retention (sign employment agreements, set comp)
- Quick wins — pricing, obvious cost cuts, low-hanging fruit
- Detailed operational assessment by function
- Customer communication plan
- Set up reporting and KPI dashboards

**Days 31-60: Plan & Initiate**
- Finalize strategic plan and communicate to organization
- Launch top 3-5 value creation initiatives
- Begin add-on M&A pipeline development
- Hire for critical gaps
- Implement new reporting cadence (weekly flash, monthly review, quarterly board)

**Days 61-100: Execute & Measure**
- First results from quick-win initiatives
- First board meeting with operating metrics
- Progress report on each value creation lever
- Adjust plan based on early learnings

### Step 5: KPI Dashboard

Define the metrics that will track value creation:

| KPI | Current | Year 1 Target | Owner | Reporting Frequency |
|-----|---------|---------------|-------|-------------------|
| Revenue | | | CEO | Monthly |
| EBITDA | | | CFO | Monthly |
| EBITDA margin | | | CFO | Monthly |
| New customer wins | | | CRO | Weekly |
| Net retention | | | CRO | Monthly |
| Employee turnover | | | CHRO | Monthly |
| Cash conversion | | | CFO | Monthly |

### Step 6: Output

- Word document or PowerPoint with:
  - Executive summary (1 page)
  - EBITDA bridge chart
  - Value creation levers detail (1 page per lever)
  - 100-day plan timeline
  - KPI dashboard
  - Accountability matrix (who owns what)
- Excel model backing the EBITDA bridge

## Important Notes

- Be realistic about timing — most PE value creation takes 12-24 months to show in financials
- Quick wins matter for momentum and credibility, but don't over-rotate on cost cuts at the expense of growth
- Management buy-in is critical — co-develop the plan, don't impose it
- Track initiative-level P&L impact, not just top-line EBITDA — you need to know what's working
- Add-on M&A is often the largest value creation lever — start the pipeline on Day 1
- Always pressure-test assumptions with operating partners or industry experts
