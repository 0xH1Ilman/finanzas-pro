# 02-earnings-research — parte 2

Skills de terceros agrupadas por tema. Cada sección indica fuente, licencia y dónde está su código.



---

## SKILL: initiating-coverage

- Fuente: `anthropics/financial-services` → `plugins/vertical-plugins/equity-research/skills/initiating-coverage` (Apache-2.0)
- Cuándo usarla: Create institutional-quality equity research initiation reports through a 5-task workflow. Tasks must be executed individually with verified prerequisites - (1) company research, (2) financial modeling, (3) valuation analysis, (4) chart generation, (5) final report assembly. Each task produces specific deliverables (markdown docs, Excel models, charts, or DOCX reports). Tasks 3-5 have dependencies on earlier tasks.

# Initiating Coverage

Create institutional-quality equity research initiation reports through a structured 5-task workflow. Each task must be executed separately with verified inputs.

## Overview

This skill produces comprehensive first-time coverage reports following institutional standards (JPMorgan, Goldman Sachs, Morgan Stanley format). Tasks are executed individually, each verifying prerequisites before proceeding.

**Default Font**: Times New Roman throughout all documents (unless user specifies otherwise).

---

## ⚠️ CRITICAL: One Task at a Time

**THIS SKILL OPERATES IN SINGLE-TASK MODE ONLY.**

### If User Requests Full Pipeline

When user requests:
- "Create a coverage initiation report for [Company]"
- "Write an initiation report for [Company]"
- "Do the entire equity research process for [Company]"
- "Complete all 5 tasks for [Company]"
- Any request that implies running multiple tasks or the entire workflow

**REQUIRED RESPONSE:**

1. **Ask which specific task to perform:**
   ```
   I can help you create an equity research initiation report for [Company].
   This involves 5 separate tasks that need to be completed individually:

   1. Company Research - Research business, management, industry
   2. Financial Modeling - Build projection model
   3. Valuation Analysis - DCF and comparable companies
   4. Chart Generation - Create 25-35 charts
   5. Report Assembly - Compile final report

   Which task would you like to start with?
   ```

2. **When user explicitly requests all tasks together:**
   ```
   I understand you'd like to complete the entire initiation report pipeline.
   Currently, this skill supports executing one task at a time, which allows
   for better quality control and review at each stage.

   We're working on a seamless end-to-end workflow that will make this process
   more automated, but for now, we'll need to complete each task separately.

   Would you like to start with Task 1 (Company Research)?
   ```

3. **Never automatically assume which task to start** - always ask user to confirm.

4. **Never execute multiple tasks in sequence** - complete one task, deliver outputs, then wait for next user request.

### Task Execution Rules

- ✅ Execute exactly ONE task per user request
- ✅ Always verify prerequisites before starting a task
- ✅ Deliver task outputs and confirm completion
- ✅ Wait for user to explicitly request the next task
- ❌ Never chain multiple tasks together automatically
- ❌ Never assume user wants to proceed to next task
- ❌ Never execute Tasks 3-5 without verifying required inputs exist

### ⚠️ Deliverables Policy: NO SHORTCUTS

**DELIVER ONLY THE SPECIFIED OUTPUTS. DO NOT CREATE EXTRA DOCUMENTS.**

Each task specifies exact deliverables. Do NOT create:
- ❌ "Completion summaries"
- ❌ "Executive summaries"
- ❌ "Quick reference guides"
- ❌ "Next steps documents"
- ❌ "Task completion reports"
- ❌ Any other "helpful" documentation not explicitly specified

**Why**: These extras waste context and are not part of the professional workflow.

**What TO deliver**:
- ✅ Task 1: Research document (.md) — **NOTHING ELSE**
- ✅ Task 2: Financial model (.xlsx) — **NOTHING ELSE**
- ✅ Task 3: Valuation analysis (.md) + Excel tabs added to Task 2 file — **NOTHING ELSE**
- ✅ Task 4: Charts zip file (.zip) — **NOTHING ELSE**
- ✅ Task 5: Final report (.docx) — **NOTHING ELSE**

**If a deliverable is not listed above, DO NOT CREATE IT.**

---

## Task Selection

Select which task to execute:

| Task | Name | Prerequisites | Output |
|------|------|--------------|--------|
| **1** | Company Research | Company name/ticker | 6-8K word document |
| **2** | Financial Modeling | 10-K or financials access | Excel model (6 tabs) |
| **3** | Valuation Analysis | Financial model (Task 2) | Valuation + price target |
| **4** | Chart Generation | Tasks 1, 2, 3 + external data | 25-35 PNG/JPG charts |
| **5** | Report Assembly | ALL previous tasks (1-4) | 30-50 page DOCX report |

---

## How to Use This Skill

### User Request Patterns and Responses

**Pattern 1: User specifies a specific task**
```
User: "Use initiating-coverage, Task 1 for Tesla"
Response: ✅ Execute Task 1 immediately
```

**Pattern 2: User asks for "initiation report" or "full pipeline"**
```
User: "Create a coverage initiation report for Tesla"
Response: ❌ DO NOT start any task automatically
         ✅ Ask which task to start with (see template above)
```

**Pattern 3: User wants to do "all tasks" or "entire workflow"**
```
User: "I want to complete all 5 tasks for Tesla"
Response: ❌ DO NOT chain tasks together
         ✅ Explain one-at-a-time limitation (see template above)
         ✅ Ask if they want to start with Task 1
```

### Correct Usage Examples

**Executing a single task:**
```
"Use initiating-coverage skill, Task 1 for Tesla"
"Do Task 2 of initiating-coverage for Tesla"
"Run Task 3 for Tesla using the initiating-coverage skill"
```

**Completing full report (requires 5 separate requests):**
```
Request 1: "Do Task 1 for Tesla" → Complete → Deliver outputs
Request 2: "Do Task 2 for Tesla" → Complete → Deliver outputs
Request 3: "Do Task 3 for Tesla" → Complete → Deliver outputs
Request 4: "Do Task 4 for Tesla" → Complete → Deliver outputs
Request 5: "Do Task 5 for Tesla" → Complete → Deliver outputs
```

### Task Execution Order

For a complete initiation report, tasks must be executed in separate user requests following this order:

```
Request 1: Task 1 - Company Research (independent)
           ↓ [User reviews outputs and requests next task]
Request 2: Task 2 - Financial Modeling (independent)
           ↓ [User reviews outputs and requests next task]
Request 3: Task 3 - Valuation Analysis (requires Task 2 output)
           ↓ [User reviews outputs and requests next task]
Request 4: Task 4 - Chart Generation (requires Tasks 2 & 3 outputs)
           ↓ [User reviews outputs and requests next task]
Request 5: Task 5 - Report Assembly (requires ALL previous task outputs)
```

**Note**: Tasks 1 and 2 can be run in any order. Tasks 3-5 have strict dependencies and must verify inputs before proceeding.

---

## Task 1: Company Research

**Purpose**: Research company's business, management, competitive position, industry, and risks.

**Prerequisites**: ✅ None (fully independent)
- Company name or ticker symbol

**Process**:
1. Verify company name/ticker provided
2. Load detailed instructions from references/task1-company-research.md
3. Execute qualitative research workflow
4. Deliver research document

**Output**: Company Research Document (6,000-8,000 words)
- Company overview & history
- Management bios (300-400 words × 3-4 execs)
- Products & services analysis
- Industry overview
- Competitive analysis (5-10 competitors)
- TAM sizing
- Risk assessment (8-12 risks)

**File name**: `[Company]_Research_Document_[Date].md`

**⚠️ DELIVER ONLY THIS 1 FILE. NO completion summaries, no extra documents.**

**⚠️ DO NOT TAKE SHORTCUTS:**
- ✅ Write full 6,000-8,000 words (not summaries)
- ✅ Complete 300-400 word bios for ALL 3-4 executives
- ✅ Analyze ALL 5-10 competitors thoroughly
- ✅ Cover all 8-12 risks across 4 categories
- ❌ Do not abbreviate sections to save time
- ❌ Do not skip any required sections

**Verification before proceeding**: None required for this task.

---

## Task 2: Financial Modeling

**Purpose**: Extract historical financials and build comprehensive Excel financial model with projections and scenarios.

**Prerequisites**: ⚠️ Verify before starting
- **Required**: Access to company financial data
  - For public companies: Latest 10-K from SEC EDGAR
  - For private companies: Financial statements or available estimates
  - OR: Pre-extracted historical financials provided by user
- **Optional**: Company research (Task 1) for business context

**Input Verification**:
```
BEFORE STARTING - Select approach:

Option A: Extract financials (most common)
- [ ] Have access to 10-K or financial statements?
- [ ] Ready to extract 3-5 years of data?

Option B: User provided pre-extracted financials
- [ ] Historical financials file received?
- [ ] Contains income statement, cash flow, balance sheet (3-5 years)?

Optional:
- [ ] Company research (Task 1) complete for context?
```

**Process**:
1. Verify access to financial data
2. Load detailed instructions from references/task2-financial-modeling.md
3. **Step 1**: Extract historical financials (if needed)
4. **Step 2+**: Build projection model with 6 essential tabs
5. Deliver Excel model

**Output**: Excel Financial Model (.xlsx)
- 6 essential tabs:
  1. **Revenue Model** - Product breakdown (20-30 rows) + Geography breakdown (15-20 rows)
  2. **Income Statement** - Full P&L with 40-50 line items, historical (3-5 years) + projected (5 years)
  3. **Cash Flow Statement** - Operating/Investing/Financing activities, historical + projected
  4. **Balance Sheet** - Assets/Liabilities/Equity, historical + projected
  5. **Scenarios** - Bull/Base/Bear comparison table
  6. **DCF Inputs** - Prepared for Task 3 valuation

**File name**: `[Company]_Financial_Model_[Date].xlsx`

**⚠️ DELIVER ONLY THIS 1 FILE. NO completion summaries, no extra documents.**

**⚠️ DO NOT TAKE SHORTCUTS:**
- ✅ If extracting financials: Extract ALL line items from 3 financial statements (3-5 years)
- ✅ Build ALL 6 projection tabs completely with full detail
- ✅ Create detailed revenue model with 20-30 product rows AND 15-20 geography rows
- ✅ Build complete income statement with 40-50 line items (not abbreviated)
- ✅ Include full cash flow statement and balance sheet with all line items
- ✅ Complete ALL three scenarios (Bull/Base/Bear) with different parameters
- ❌ Do not create simplified/abbreviated versions
- ❌ Do not skip any of the 6 essential tabs
- ❌ Do not skip historical financials extraction if needed

**Verification before proceeding to Task 3**:
- [ ] Historical financials extracted (if needed) or provided
- [ ] Excel file created and can be opened
- [ ] Model has all 6 essential tabs (Revenue Model, Income Statement, Cash Flow, Balance Sheet, Scenarios, DCF Inputs)
- [ ] Historical data (3-5 years) incorporated
- [ ] Projections complete (5 years forward)
- [ ] Scenarios complete (Bull/Base/Bear)

---

## Task 3: Valuation Analysis

**Purpose**: Perform comprehensive valuation using DCF, comparables, and precedent transactions.

**Prerequisites**: ⚠️ Verify before starting
- **Required**: Financial model from Task 2
  - Projected income statements
  - Projected cash flows
  - Revenue and EBITDA forecasts
  - DCF inputs (unlevered FCF)

**⚠️ CRITICAL: DO NOT START THIS TASK UNLESS TASK 2 IS COMPLETE**

This task requires the financial model from Task 2. Starting without it will result in incomplete work.

**IF TASK 2 IS NOT COMPLETE**: Stop immediately and inform the user that Task 2 (Financial Modeling) must be completed first. Do not attempt to proceed or create placeholder valuations.

**Input Verification**:
```
BEFORE STARTING:
- [ ] Task 2 complete? (Financial model exists)
- [ ] Model file path/location known?
- [ ] Can access projected financials from model?

Required from model:
- [ ] Projected FCF (5 years)
- [ ] Revenue projections
- [ ] EBITDA projections
- [ ] Terminal year metrics
```

**Process**:
1. Verify financial model is accessible
2. Load detailed instructions from references/task3-valuation.md
3. Execute valuation workflow
4. Deliver valuation analysis

**Output**: Valuation Analysis (4-6 pages + Excel tabs)
- DCF analysis with sensitivity tables
- Comparable companies (5-10 peers with statistical summary)
- Precedent transactions (if applicable)
- Valuation football field
- **Price target**: $XX.XX
- **Recommendation**: BUY/HOLD/SELL
- **Upside**: XX%
- Key catalysts (3-5)

**Files**:
- `[Company]_Valuation_Analysis_[Date].md` (written analysis document)
- Excel tabs added to `[Company]_Financial_Model_[Date].xlsx` (from Task 2)
  - DCF tab with calculations
  - Sensitivity analysis tab
  - Comparable companies tab
  - Valuation summary tab

**⚠️ DELIVER ONLY: 1 markdown file + 4 tabs added to existing Excel. NO completion summaries, no extra documents.**

**⚠️ DO NOT TAKE SHORTCUTS:**
- ✅ Complete full DCF analysis with sensitivity matrix (not simplified)
- ✅ Analyze ALL 5-10 comparable companies with full data
- ✅ Include statistical summary in comps table (max/75th/median/25th/min)
- ✅ Create complete sensitivity analysis tab with multiple WACC and terminal growth scenarios
- ✅ Write full 4-6 pages of valuation analysis (not abbreviated)
- ✅ Research and justify price target with specific methodology
- ❌ Do not skip comparable company analysis
- ❌ Do not create simplified DCF without sensitivity

**Verification before proceeding to Task 4**:
- [ ] Price target determined
- [ ] Valuation uses multiple methods (DCF + Comps minimum)
- [ ] DCF sensitivity table complete
- [ ] Comparable companies table includes statistical summary

---

## Task 4: Chart Generation

**Purpose**: Generate 25-35 professional financial charts for the report.

**Prerequisites**: ⚠️ Verify before starting
- **Required**: Company research from Task 1
  - Company history and milestones (for timeline charts)
  - Management team and org structure (for org charts)
  - Product portfolio (for product charts)
  - Customer segmentation (for customer charts)
  - Competitive landscape (for competitive charts)
  - TAM analysis (for market size charts)
- **Required**: Financial model from Task 2 (with Task 3 valuation tabs added)
  - Revenue by product/geography data (Task 2 tabs)
  - Margin trends (Task 2 tabs)
  - Scenario comparison data (Task 2 tabs)
  - DCF sensitivity table (Task 3 tab in same Excel file)
  - Comparable companies data (Task 3 tab in same Excel file)
  - Valuation ranges (Task 3 tab in same Excel file)
- **Required**: External market data
  - Historical stock price data (Yahoo Finance, Bloomberg, etc.)
  - Historical valuation multiples (for historical trend charts)

**⚠️ CRITICAL: DO NOT START THIS TASK UNLESS TASKS 1, 2, AND 3 ARE COMPLETE**

This task requires outputs from all three previous tasks. Starting without them will result in incomplete charts.

**IF ANY OF TASKS 1, 2, OR 3 ARE NOT COMPLETE**: Stop immediately and inform the user which tasks need to be completed first. The specific requirements are:
- Task 1: Company research document (for 9 charts)
- Task 2: Financial model with all 6 tabs (for 8 charts)
- Task 3: Valuation tabs added to the model (for 6 charts)
- External data access (for 2 charts)

Do not attempt to create placeholder charts or skip charts due to missing data.

**Input Verification**:
```
BEFORE STARTING:
- [ ] Task 1 complete? (Company research exists)
- [ ] Task 2 complete? (Financial model exists)
- [ ] Task 3 complete? (Valuation analysis exists)
- [ ] Can access external market data sources?

Required from Task 1:
- [ ] Company history and milestones (for charts 05, 06)
- [ ] Management team structure (for chart 07)
- [ ] Product portfolio details (for chart 08)
- [ ] Customer segmentation data (for chart 09)
- [ ] Competitive landscape analysis (for charts 16, 17, 18)
- [ ] TAM sizing and market data (for chart 15)

Required from Task 2:
- [ ] Revenue by product (historical + projected) - for chart 03 ⭐
- [ ] Revenue by geography (historical + projected) - for chart 04 ⭐
- [ ] Income statement with margins (for charts 02, 10, 11)
- [ ] Cash flow statement (for chart 12)
- [ ] Scenario comparison data (for chart 14)

Required from Task 3:
- [ ] DCF sensitivity matrix - for chart 28 ⭐
- [ ] DCF components (for chart 29)
- [ ] Comparable companies data (for charts 30, 31)
- [ ] Valuation ranges - for chart 32 ⭐

Required from External Sources:
- [ ] Historical stock price data (for chart 01)
- [ ] Historical valuation multiples (for chart 34)
```

**Process**:
1. Verify model and valuation outputs are accessible
2. Load detailed instructions from references/task4-chart-generation.md
3. Execute chart generation workflow
4. Package all charts into a zip file
5. Deliver zip file

**Output**: 25-35 Professional Chart Files (PNG/JPG, 300 DPI) packaged in zip

**4 MANDATORY Charts** (must be present) ⭐:
- chart_03: Revenue by product (stacked area)
- chart_04: Revenue by geography (stacked bar)
- chart_28: DCF sensitivity (2-way heatmap)
- chart_32: Valuation football field (horizontal bars)

**25 REQUIRED Charts** (specific list):
- Investment Summary: chart_01
- Financial Performance: charts 02, 03⭐, 04⭐, 10, 11, 12, 14
- Company 101: charts 05, 06, 07, 08, 09, 15, 16
- Competitive/Market: charts 17, 18
- Scenario Analysis: chart 13
- Valuation: charts 28⭐, 29, 30, 31, 32⭐, 33, 34

**10 OPTIONAL Charts** (for 26-35 range):
- charts 19-27, 35 (customer acquisition, unit economics, product roadmap, etc.)

**IMPORTANT**: Task 5 embeds ALL charts created (25-35) for visual density (1 chart per 200-300 words).

**File naming**: `chart_01_description.png`, `chart_02_description.png`, etc.

**Deliverable**: `[Company]_Charts_[Date].zip` containing all 25-35 chart files + chart_index.txt

**⚠️ DELIVER ONLY THIS 1 ZIP FILE. NO completion summaries, no separate chart lists, no extra documents.**

**⚠️ DO NOT TAKE SHORTCUTS:**
- ✅ Create ALL 25 required charts minimum (specific list provided in task4-chart-generation.md)
- ✅ Include ALL 4 mandatory charts:
  - chart_03: Revenue by product (stacked area) ⭐
  - chart_04: Revenue by geography (stacked bar) ⭐
  - chart_28: DCF sensitivity (heatmap) ⭐
  - chart_32: Valuation football field ⭐
- ✅ Optional: Add 1-10 more charts to reach 26-35 total for greater visual density
- ✅ Generate professional-quality charts at 300 DPI (not low-res placeholders)
- ✅ Create unique, well-formatted charts for each visualization
- ✅ Package all charts in zip file with chart index
- ❌ Do not create only 10-15 charts (minimum is 25)
- ❌ Do not skip any of the 4 mandatory charts
- ❌ Do not use low-quality/placeholder images

**Verification before proceeding to Task 5**:
- [ ] Minimum 25 chart files created (required)
- [ ] All 4 mandatory charts present:
  - [ ] chart_03: Revenue by product ⭐
  - [ ] chart_04: Revenue by geography ⭐
  - [ ] chart_28: DCF sensitivity ⭐
  - [ ] chart_32: Valuation football field ⭐
- [ ] All charts open and display correctly
- [ ] Charts saved at 300 DPI (print quality)
- [ ] Chart index created listing all files with categories
- [ ] All charts packaged in zip file
- [ ] File naming follows convention: chart_##_description.png

---

## Task 5: Report Assembly

**Purpose**: Write and assemble the comprehensive final DOCX report.

**Prerequisites**: ⚠️ Verify before starting
- **Required**: Company research from Task 1
  - All 6-8K words of content
  - Management bios
  - Competitive analysis
  - Risk assessment
- **Required**: Financial model from Task 2
  - Excel workbook
  - All projections and scenarios
- **Required**: Valuation analysis from Task 3
  - Price target and recommendation
  - DCF, comps, precedent transactions
  - All valuation data
- **Required**: Chart files from Task 4
  - Zip file containing all 25-35 PNG/JPG files
  - Chart index included in zip

**⚠️ CRITICAL: DO NOT START THIS TASK UNLESS ALL TASKS 1-4 ARE COMPLETE**

This is the final assembly task. It cannot be completed without all previous work products.

**IF ANY OF TASKS 1, 2, 3, OR 4 ARE NOT COMPLETE**: Stop immediately and inform the user which tasks need to be completed first. The specific requirements are:
- Task 1: Company research document (6-8K words)
- Task 2: Financial model with all 6 tabs
- Task 3: Valuation analysis with price target and recommendation
- Task 4: Charts zip file with 25-35 charts

Do not attempt to create placeholder content, substitute missing sections, or assemble an incomplete report. The report requires ALL inputs to be publication-ready.

**Input Verification**:
```
BEFORE STARTING - ALL TASKS MUST BE COMPLETE:

Task 1 Verification:
- [ ] Company research document exists? (6-8K words)
- [ ] Management bios complete? (300-400 words × 3-4 execs)
- [ ] Competitive analysis complete? (5-10 competitors)
- [ ] Risk assessment complete? (8-12 risks)

Task 2 Verification:
- [ ] Financial model exists and can be opened?
- [ ] Model has projections (5 years)?
- [ ] Scenarios exist (Bull/Base/Bear)?

Task 3 Verification:
- [ ] Valuation analysis complete?
- [ ] Price target determined?
- [ ] Recommendation set? (BUY/HOLD/SELL)
- [ ] DCF and comps complete?

Task 4 Verification:
- [ ] Chart zip file exists?
- [ ] Can extract/access all 25-35 chart files from zip?
- [ ] All 4 mandatory charts present?
  - [ ] Revenue by product (stacked area)
  - [ ] Revenue by geography (stacked bar)
  - [ ] DCF sensitivity (heatmap)
  - [ ] Valuation football field
- [ ] Chart files accessible and can be opened?

IF ANY VERIFICATION FAILS: Stop and complete missing task first.
```

**Process**:
1. **CRITICAL**: Verify ALL prerequisites before starting
2. Load detailed instructions from references/task5-report-assembly.md
3. Execute report assembly workflow using Claude's built-in skills:
   - **Use DOCX skill** to create and manipulate the Word document
   - **Use XLSX skill** to read Excel data from Task 2/3
   - **Use Read tool** to read Task 1 and Task 3 markdown files
   - Read Task 1 .md file → Convert to Word formatting → Insert charts inline
   - Read Task 2 .xlsx file → Extract tables → Write quantitative analysis
   - Read Task 3 .md file + Excel tabs → Copy/adapt valuation analysis
   - Insert Task 4 .png chart files throughout using DOCX skill
   - Create text-dense report with charts interspersed every 200-300 words
4. Save and deliver final DOCX report

**Key Principles**:
- Use Claude's DOCX and XLSX skills (NOT Python libraries)
- Use actual file operations (read .md/.xlsx/.png files, write .docx file)
- Good equity research reports are text-dense with lots of illustrating images (60-80% page coverage, 1+ chart per page)

**🔥 CRITICAL: GO ALL OUT ON THIS TASK**

**THIS IS THE FINAL DELIVERABLE. DO NOT TAKE SHORTCUTS.**

- ✅ **Use full token budget** - This is the culmination of all previous work
- ✅ **Write every section completely** - Do not summarize or abbreviate
- ✅ **Hit ALL minimum requirements** - 30+ pages, 10,000+ words, 25+ charts, 12+ tables
- ✅ **Be thorough on projection assumptions** - 2,000-3,000 words with product-by-product detail
- ✅ **Be comprehensive on scenarios** - 1,500-2,000 words with specific Bull/Base/Bear parameters
- ✅ **Insert ALL charts from Task 4** - Not just a few, ALL 25-35 charts throughout
- ✅ **Create ALL tables from Task 2/3** - Extract every financial table, don't skip any
- ✅ **Use Task 1 content verbatim** - Copy/paste full Company 101 sections (6-8K words)
- ✅ **Professional quality only** - This must be indistinguishable from JPMorgan/Goldman Sachs research

**NEVER:**
- ❌ "This section would include..." - WRITE THE ACTUAL SECTION
- ❌ "Charts would be inserted here..." - INSERT THE ACTUAL CHARTS
- ❌ "See financial model for details..." - EXTRACT AND INCLUDE THE DETAILS
- ❌ Skip sections due to length - Every section MUST be complete
- ❌ Abbreviate for token conservation - Use whatever tokens are needed

**This is publication-ready institutional research. Spare no effort, tokens, or detail.**

**Output**: Comprehensive Equity Research Report (.docx)

**Specifications**:
- **Length**: 30-50 pages (MINIMUM 30)
- **Word count**: 10,000-15,000 words (MINIMUM 10,000)
- **Charts**: 25-35 embedded images
- **Tables**: 12-20 comprehensive tables
- **Format**: Professional DOCX with clickable hyperlinks

**Structure**:
- Page 1: Investment Summary (INITIATING COVERAGE format)
- Pages 2-5: Investment thesis & risks
- Pages 6-17: Company 101
- Pages 18-30: Financial analysis & projections
- Pages 31-40: Valuation analysis
- Pages 41-50: Appendices

**File name**: `[Company]_Initiation_Report_[Date].docx`

**⚠️ DELIVER ONLY THIS 1 DOCX FILE. NO executive summaries, no "highlights" documents, no extra files.**

**Final Verification**:
- [ ] Report is 30-50 pages
- [ ] Word count is 10,000-15,000
- [ ] 25-35 charts embedded
- [ ] 12-20 tables included
- [ ] All citations are clickable hyperlinks
- [ ] Numbers match financial model exactly

---

## Input Verification Protocol

### Why Input Verification Matters

Each task has strict prerequisites. Running a task without required inputs will:
- Waste time with incomplete work
- Produce low-quality outputs
- Require rework

**Always verify inputs before starting a task.**

### Verification Checklist by Task

**Task 1**: ✅ No verification needed (independent)

**Task 2**: Check historical financials available

**Task 3**: Check financial model exists and is accessible

**Task 4**: Check both model (Task 2) AND valuation (Task 3) exist

**Task 5**: Check ALL previous tasks complete (1, 2, 3, 4)

### What to Do if Verification Fails

```
IF prerequisites are missing:
1. Stop the current task
2. Identify which prerequisite task(s) need to be completed
3. Execute the missing task(s) first
4. Return to current task once prerequisites are met
```

### Example Verification Dialogue

```
User: "Use initiating-coverage, Task 5 for Tesla"

Claude: "Starting Task 5: Report Assembly for Tesla

VERIFICATION - Checking prerequisites:
- Task 1 (Company research)... ❌ NOT FOUND
- Task 2 (Financial model)... ❌ NOT FOUND
- Task 3 (Valuation)... ❌ NOT FOUND
- Task 4 (Charts)... ❌ NOT FOUND

⚠️ VERIFICATION FAILED

Task 5 requires ALL previous tasks to be complete.

To proceed:
1. Complete Task 1: Company Research
2. Complete Task 2: Financial Modeling
3. Complete Task 3: Valuation Analysis
4. Complete Task 4: Chart Generation
5. Then return to Task 5

Would you like to start with Task 1 first?"
```

---

## Task Reference Files

Detailed instructions for each task are in separate reference files to keep this skill lean:

- **references/task1-company-research.md** - Company research workflow
- **references/task2-financial-modeling.md** - Financial modeling workflow
- **references/task3-valuation.md** - Valuation methodology
  - Also see: references/valuation-methodologies.md for DCF/comps deep dive
- **references/task4-chart-generation.md** - Chart generation workflow
- **references/task5-report-assembly.md** - Report writing workflow
  - Also see: assets/report-template.md for report structure
  - Also see: assets/quality-checklist.md for quality checks

**When to load reference files**: Load ONLY the reference file associated with the specific task being performed. These files are very large - do not load multiple reference files at once. Read the appropriate task reference file at the start of the task for detailed step-by-step instructions.

---

## Quality Standards

All outputs meet institutional standards from leading investment banks (JPMorgan, Goldman Sachs, Morgan Stanley):

- **Comprehensive**: Meet all minimum requirements
- **Detailed**: Specific data and examples, not generic statements
- **Quantified**: Lead with numbers and metrics
- **Cited**: Proper sources with clickable hyperlinks
- **Professional**: Institutional-quality formatting
- **Accurate**: All numbers verified and cross-checked

---

## Important Notes

### Task Independence

- **Task 1** can run anytime (no dependencies)
- **Task 2** can run anytime (just needs historical data)
- **Tasks 1 & 2** can run in parallel
- **Task 3** requires Task 2
- **Task 4** requires Tasks 2 & 3
- **Task 5** requires Tasks 1, 2, 3, & 4

### Session Management

**Same session**: Outputs automatically available to subsequent tasks

**Different sessions**: Reference previous task outputs explicitly
```
"Use Task 3 with the model from yesterday at [path]"
"Use Task 5 with the research document at [path]"
```

### File Organization

Recommended structure during workflow:
```
ProjectFolder/
├── Task1_Research/
│   └── [Company]_Research_Document.md
├── Task2_Model/
│   └── [Company]_Financial_Model.xlsx
├── Task3_Valuation/
│   └── [Company]_Valuation_Analysis.pdf
├── Task4_Charts/
│   ├── chart_01.png
│   └── ... (25-35 files)
└── Task5_Report/
    └── [Company]_Initiation_Report.docx
```

### No End-to-End Execution

This skill does **NOT** support running all tasks automatically in sequence. Each task must be explicitly requested and verified.

**Why**: This ensures:
- Quality control at each stage
- Ability to review outputs before proceeding
- Flexibility to pause/resume workflow
- Clear verification of prerequisites

---

## Success Criteria

A successful initiation report workflow should:
1. Complete all 5 tasks in order
2. Pass all input verifications
3. Meet all quality standards
4. Produce all required deliverables
5. Numbers cross-check between outputs
6. Final report is publication-ready

**Output quality**: Institutional (JPMorgan/Goldman/Morgan Stanley level)
**Use case**: First-time comprehensive coverage of a company

### Referencia: assets/quality-checklist.md

# Quality Control Checklist for Initiation Reports

Before delivering an initiation report, verify all items below are complete.

## Critical Minimums - Reports Must Meet These

**CRITICAL DO NOT DELIVER IF:**
- ❌ DOCX report fewer than 30 pages → INCOMPLETE
- ❌ Fewer than 25 embedded charts → INCOMPLETE
- ❌ Fewer than 12 comprehensive tables → INCOMPLETE
- ❌ Fewer than 10,000 words → INCOMPLETE
- ❌ No XLS financial model → MISSING DELIVERABLE
- ❌ Charts are text descriptions, not actual PNG/JPG files → MAJOR FAILURE

## Deliverables Checklist

- [ ] DOCX report file created
- [ ] XLS financial model file created
- [ ] Both files named properly: `[Company]_Initiation_Report_[Date].docx` and `[Company]_Financial_Model_[Date].xlsx`

## DOCX Report - Length & Content

**Length Verification:**
- [ ] Report is 30-50 pages (count pages in final document)
- [ ] Word count is 10,000-15,000 words
- [ ] If under 30 pages: STOP and add more content

**Visual Elements:**
- [ ] 25-35 charts embedded (count them: _____ charts)
- [ ] All charts are actual PNG/JPG image files (NOT text descriptions)
- [ ] 12-20 comprehensive tables included (count them: _____ tables)
- [ ] Charts and tables interspersed throughout, not grouped at end

**Chart Requirements:**
- [ ] Revenue by product chart: Stacked Area format ✓
- [ ] Revenue by geography chart: Stacked Bar format ✓
- [ ] DCF sensitivity: 2-way Heat Map with color coding ✓
- [ ] Valuation football field: Horizontal bar chart ✓
- [ ] All other charts are actual image files ✓

**Table Requirements:**
- [ ] Full Income Statement (40-50 rows) with 5 years historical + 5 years projected
- [ ] Full Cash Flow Statement (30-40 rows)
- [ ] Full Balance Sheet (35-45 rows)
- [ ] Revenue by product table (20-30 rows)
- [ ] Revenue by geography table (15-20 rows)
- [ ] Revenue by channel table (10-15 rows)
- [ ] Comparable companies table with statistical summary (max/75th/median/25th/min)
- [ ] DCF calculation table (30-40 rows)
- [ ] WACC calculation table (8-10 rows)
- [ ] Two sensitivity tables
- [ ] 2-3 additional financial/competitive tables

## DOCX Report - Structure

**Page 1 Requirements:**
- [ ] "INITIATING COVERAGE" header present (NOT "Company Update")
- [ ] Thesis-focused title (NOT event-driven like "Strong Q4 Results")
- [ ] Rating box with rating, price, target price, 52-week range, market cap, EV
- [ ] 3-4 paragraph-length bullets with ■ character and bold headers
- [ ] Financial & valuation metrics table with 2-3 years historical, 2 years projected
- [ ] Table shows "A" suffix for actuals, "E" suffix for estimates
- [ ] Source lines on all visuals

**Content Sections:**
- [ ] Table of Contents (Page 2)
- [ ] Investment Thesis & Risks (3-5 pages)
- [ ] Company Overview (6-12 pages) including:
  - [ ] Company description
  - [ ] History and milestones
  - [ ] Management bios (300-400 words EACH for 3-4 executives)
  - [ ] Products/services detail
  - [ ] Competitive landscape
- [ ] Financial Analysis & Projections (10-15 pages)
- [ ] Valuation Analysis (8-12 pages)
- [ ] Assumptions section (2,000-3,000 words documenting ALL projection assumptions)
- [ ] Scenario Analysis (1,500-2,000 words with Bull/Base/Bear parameters)
- [ ] Appendices including Data Sources & References page

## DOCX Report - Formatting

**Figure & Table Formatting:**
- [ ] Every figure has caption above: "Figure X - [Company] [Descriptive Title]"
- [ ] Every figure has source line below: "Source: [Specific sources with dates]"
- [ ] Sequential figure numbering (Figure 1, 2, 3... no gaps)
- [ ] Every table has header row with shading
- [ ] Every table has source line at bottom
- [ ] All years use "A" for actual, "E" for estimate notation

**Professional Formatting:**
- [ ] Consistent fonts throughout (Calibri, Arial, or similar)
- [ ] Headers and footers with page numbers
- [ ] Dense layout: 60-80% page coverage, minimal white space
- [ ] Every page has both text AND visuals (charts or tables)
- [ ] Professional business report template used

## Citations & Sources ⭐⭐⭐ CRITICAL

**Source Attribution:**
- [ ] Every figure has specific source with document name and date
- [ ] Every table has specific source with document reference
- [ ] Key statistics throughout text have footnotes with sources
- [ ] NOT just generic "Company data" - must be specific

**Hyperlinks:** ⭐⭐⭐ MANDATORY
- [ ] ALL URLs are CLICKABLE HYPERLINKS (not plain text)
- [ ] SEC filings hyperlinked to EDGAR viewer
- [ ] Earnings transcripts hyperlinked (Seeking Alpha or company IR)
- [ ] Press releases hyperlinked to company IR page
- [ ] Presentations hyperlinked to PDF URLs
- [ ] Industry reports hyperlinked (if publicly available)
- [ ] Subscription data (Bloomberg, FactSet) noted as "(subscription required)"
- [ ] No raw URLs displayed anywhere - all formatted as hyperlinks
- [ ] Test 3-5 sample hyperlinks to ensure they work (Ctrl+Click)

**Reference Page:**
- [ ] "Data Sources & References" page at end of report
- [ ] Lists ALL sources used in report
- [ ] Sources organized by category (SEC Filings, Earnings Transcripts, etc.)
- [ ] Every source has date
- [ ] Every source has clickable hyperlink (where applicable)

## XLS Financial Model - Structure

**File Structure:**
- [ ] 15+ tabs in Excel workbook
- [ ] Tabs include: Executive Summary, Assumptions, Historical Financials, Revenue Model, Operating Expenses, Income Statement, Balance Sheet, Cash Flow, Supporting Schedules, DCF Valuation, Comps Analysis, Precedent Transactions, Scenarios, Sensitivity Analysis, Charts

**Formatting:**
- [ ] Blue text for hardcoded inputs
- [ ] Black text for formulas
- [ ] Green text for links to other sheets
- [ ] Professional formatting with borders and shading
- [ ] Clear section headers and labels

**Model Functionality:**
- [ ] All numbers flow (change assumption → entire model updates)
- [ ] DCF links to assumptions and projections
- [ ] No circular references or errors
- [ ] All important cells/ranges are named
- [ ] Sensitivity tables work dynamically

## XLS Financial Model - Content

**Projections:**
- [ ] 3-5 years historical data
- [ ] 5 years forward projections (FY+1 through FY+5)
- [ ] Revenue broken down by product, geography, channel
- [ ] Full P&L with 40-50 line items
- [ ] Full cash flow with 30-40 line items
- [ ] Full balance sheet with 35-45 line items

**Valuation:**
- [ ] Complete DCF model with all calculations shown
- [ ] WACC calculation with all components
- [ ] Terminal value calculation
- [ ] Comparable companies analysis (5-10 companies)
- [ ] Precedent transactions analysis (5-10 deals)
- [ ] Scenario analysis (Bull/Base/Bear)
- [ ] Two sensitivity tables

## Cross-File Consistency

**CRITICAL**: Numbers must match EXACTLY between DOCX and XLS

- [ ] Revenue numbers match across both files
- [ ] EPS numbers match across both files
- [ ] Margin percentages match across both files
- [ ] Valuation numbers match across both files
- [ ] Price target matches across both files
- [ ] All projected years match across both files

**Verification Method**: Spot check 10-15 key numbers between DOCX report and XLS model.

## Content Quality

**Investment Thesis:**
- [ ] 3-5 clear thesis pillars
- [ ] Each pillar supported with specific data and quantification
- [ ] Financial impact quantified for each pillar
- [ ] Catalysts identified with timelines

**Analysis Depth:**
- [ ] Comprehensive business model analysis
- [ ] Detailed competitive assessment
- [ ] 3-5 year financial trends analyzed
- [ ] 8-12 risks identified and quantified
- [ ] Management team analyzed (300-400 words per executive)

**Assumptions:**
- [ ] 2,000-3,000 words documenting ALL assumptions
- [ ] Revenue growth assumptions by category/geography
- [ ] Margin assumptions with bridge showing drivers
- [ ] Working capital assumptions
- [ ] CapEx assumptions
- [ ] Each assumption has specific quantification

**Scenarios:**
- [ ] 1,500-2,000 words on scenario analysis
- [ ] Bull case with specific parameters and catalysts
- [ ] Base case with detailed rationale
- [ ] Bear case with specific triggers
- [ ] Probability assessments for each scenario

## Writing Quality

**Style:**
- [ ] Lead with numbers ("Revenue grew 15% to $1.2B" not "Strong revenue")
- [ ] Use "vs." not "versus"
- [ ] Be direct and concise
- [ ] Professional institutional tone throughout
- [ ] No informal language

**Accuracy:**
- [ ] No typos in ticker symbol
- [ ] No typos in company name
- [ ] All dates accurate
- [ ] All calculations verified
- [ ] Charts match text descriptions
- [ ] All numbers properly formatted ($ signs, % signs, commas)

## Pre-Delivery Final Check

Run through this quick final review:

1. **Deliverables**: Both DOCX and XLS files created ✓
2. **Length**: DOCX is 30-50 pages ✓
3. **Charts**: 25-35 actual PNG/JPG files embedded ✓
4. **Tables**: 12-20 comprehensive tables included ✓
5. **Words**: 10,000-15,000 words ✓
6. **Hyperlinks**: Test 3-5 hyperlinks - all work ✓
7. **Cross-check**: Spot check 10 numbers match between DOCX and XLS ✓
8. **Page 1**: "INITIATING COVERAGE" header present ✓

If ANY item fails, DO NOT DELIVER. Go back and fix.

## Actual Count Verification

**Before delivery, fill in actual counts:**

DOCX Report:
- Page count: _____ pages (MUST BE 30-50)
- Chart count: _____ charts (MUST BE 25-35)
- Table count: _____ tables (MUST BE 12-20)
- Word count: _____ words (MUST BE 10,000-15,000)

XLS Model:
- Tab count: _____ tabs (SHOULD BE 15+)
- Model years: _____ historical + _____ projected

If any count is below minimum, STOP and add content before delivery.

### Referencia: assets/report-template.md

# Equity Research Initiation Report Template

This template provides the structure for creating a comprehensive equity research initiation report. Use this as a guide when constructing the final report document.

**NOTE:** The actual report MUST be created using the DOCX skill. DO NOT generate markdown content.

**CRITICAL REQUIREMENTS:**
1. **Generate 20-30+ chart images** using Python (matplotlib/plotly) BEFORE creating the Word document
2. **Use DOCX skill**: Create professional report with proper styles, headers/footers, and formatting
3. **Embed actual chart images**: Insert the generated PNG/JPG chart files into the Word document at appropriate locations
4. **NO MARKDOWN**: Do not generate markdown content. Use DOCX skill to create a .docx file.

**CRITICAL FORMATTING GUIDANCE:**
- **MAXIMUM DENSITY**: Every page should be packed with information. Intersperse text, charts, and tables throughout.
- **NO ORPHANED SECTIONS**: Never have a section header alone or a single chart on its own page.
- **20-30+ ACTUAL CHART IMAGES**: Generate charts as image files, then embed within text sections using DOCX skill.

---

## PAGE 1: INVESTMENT UPDATE (MOST IMPORTANT PAGE)

**CRITICAL**: Page 1 is NOT a traditional executive summary. It is an **Investment Update** with a specific institutional format used by professional equity research firms.

**IMPORTANT STRUCTURAL NOTES:**
- This is an "Investment Update" or "Company Update" page, not "Executive Summary"
- Uses a rating box in top left corner
- Features stock price performance chart (Figure 1) prominently
- Contains 3-4 detailed bullet points with ■ character
- Each bullet has **bold topic header** followed by 3-5 sentence explanation
- Bottom section has financial and valuation metrics table
- All charts must have figure numbers (Figure 1, Figure 2, etc.) with source lines

### Layout Structure

**TOP LEFT - RATING BOX:**
```
Rating:             [OUTPERFORM / NEUTRAL / UNDERWEIGHT / etc.]
Price ([Date]):     $[XX.XX]
Target Price:       $[XX.XX]
52-Week Range:      $[XX.XX] - $[XX.XX]
Market Cap:         $[XX.X]B
Enterprise Value:   $[XX.X]B
```

**TOP LEFT - RESEARCH ANALYSTS:**
```
[Name], [Credentials (Ph.D., CFA, M.D., etc.)]
[Email] | [Phone]

[Name 2], [Credentials]
[Email] | [Phone]
```

**TOP RIGHT - STOCK PRICE PERFORMANCE:**
```
Figure 1 - [Company Name] Stock Price Performance
[Line chart showing stock price over 12-24 months with benchmark comparison]
Source: Company data, [Firm Name] estimates.
```

**MAIN CONTENT - GRAY HEADER BAR:**
```
[OUTPERFORM / NEUTRAL / etc.] RECOMMENDATION / COMPANY UPDATE
```

**MAIN CONTENT - DETAILED BULLETS (3-4 bullets):**

Use ■ character for bullets. Each bullet follows this format:
```
■ **[Bold Topic Header capturing main point].** Regular text explanation providing 3-5 sentences of detail with specific numbers, comparisons, and analysis. Lead with numbers and quantification where possible. Use "vs." not "versus". Be specific and concrete.

■ **[Second Topic Header].** [3-5 sentences of detailed explanation...]

■ **[Third Topic Header].** [3-5 sentences of detailed explanation...]

■ **[Fourth Topic Header - Optional].** [3-5 sentences of detailed explanation...]
```

**EXAMPLE BULLET FORMAT:**
```
■ **Vertical SaaS leadership and regulatory moat should enable $50bn+ TAM by 2030.**
Deep domain expertise in healthcare IT, strong customer retention (95%+ net revenue retention),
and cross-sell capabilities have driven Acme Health's market expansion. With the healthcare IT
market expected to reach $50bn+ by 2030, Acme Health is well-positioned to capture share given
its regulatory moat and high switching costs. Management has indicated that 70% of current
revenue comes from enterprise hospital systems, suggesting strong product-market fit.
```

**BOTTOM SECTION - FINANCIAL AND VALUATION METRICS TABLE:**
```
                            [Year-3]A   [Year-2]A   [Year-1]A   [Year]E    [Year+1]E
Revenue ($M)                [X]         [X]         [X]         [X]        [X]
Revenue Growth (%)          X.X%        X.X%        X.X%        X.X%       X.X%
Gross Margin (%)           X.X%        X.X%        X.X%        X.X%       X.X%
EBITDA ($M)                [X]         [X]         [X]         [X]        [X]
EBITDA Margin (%)          X.X%        X.X%        X.X%        X.X%       X.X%
EPS ($)                    X.XX        X.XX        X.XX        X.XX       X.XX
P/E (x)                    XX.Xx       XX.Xx       XX.Xx       XX.Xx      XX.Xx
EV/Revenue (x)             X.Xx        X.Xx        X.Xx        X.Xx       X.Xx
EV/EBITDA (x)              XX.Xx       XX.Xx       XX.Xx       XX.Xx      XX.Xx

Note: Use "A" suffix for actual/historical years, "E" suffix for estimated/projected years
Source: Company data, [Firm Name] estimates.
```

---

## FIGURE NUMBERING AND FORMATTING STANDARDS

**CRITICAL**: All charts, graphs, and tables must follow strict figure numbering conventions used in professional equity research.

### Figure Numbering Format

**Every chart/table must have:**
1. **Sequential numbering**: Figure 1, Figure 2, Figure 3, etc. (continue sequentially throughout entire report)
2. **Descriptive title**: "Figure X - [Company] [Specific Metric] [Type of Chart/Analysis]"
3. **Source line** (always at bottom): "Source: Company data, [Firm Name] estimates."

**Examples:**
- Figure 1 - [Company] Stock Price Performance
- Figure 2 - [Company] Historical and Projected Revenue Mix by Product
- Figure 3 - [Company] Revenue by Geographic Region
- Figure 4 - [Product Name] Revenue and Price per Patient per Year
- Figure 5 - [Company] Gross Margin Evolution
- Figure 6 - DCF Sensitivity Analysis ($/share)
- Figure 7 - Valuation Football Field

### Caption Format

```
Figure X - [Descriptive Title]
[Chart/Table/Graph content]
Source: Company data, [Firm Name] estimates.
```

For tables with multiple data sources:
```
Figure X - [Descriptive Title]
[Table content]
Source: Company filings, FactSet, [Firm Name] estimates.
```

### Placement Guidelines

- Figures should be numbered in order of appearance in the report
- First figure (Figure 1) is typically the stock price chart or revenue growth trajectory on Page 1
- Each figure must have its caption directly below the visual
- Source line should be in smaller font, italicized, at the very bottom of the figure

---

## PAGE 2: TABLE OF CONTENTS

```
Executive Summary....................................................1
Investment Thesis & Risks..........................................3
Company Overview.......................................................6
  Business Description & History................................6
  Management & Ownership..........................................8
  Products & Technology...........................................9
  Customers & Go-to-Market......................................11
Growth Outlook & Drivers...........................................13
Financial Analysis & Performance.................................16
  Historical Performance........................................16
  Financial Projections.........................................19
Industry Overview & Competitive Landscape.....................21
  Market Size & TAM..............................................21
  Competitive Analysis..........................................23
  Industry Trends................................................25
Valuation Analysis..................................................27
Appendices & Disclosures...........................................31
```

---

## PAGES 3-5: INVESTMENT THESIS & RISKS

**LAYOUT PRINCIPLE**: Intersperse text with 2-3 charts in this section. Each page should have both text AND graphics. Never have pages with text only or charts only.

### Investment Thesis

**[Thesis Pillar 1]: [Title - e.g., "Large and Growing TAM"]**

[Opening sentence with key statistic]

[Paragraph 1: Market opportunity quantification]
- Current market size
- Growth drivers
- Company's positioning

[Paragraph 2: Why company will capture share]
- Competitive advantages
- Go-to-market strategy
- Early traction/proof points

[Paragraph 3: Financial impact]
- Revenue opportunity
- Margin profile
- Timeline

**[EMBED CHART: TAM Growth Chart]** - Stacked area chart showing market size evolution and company's opportunity

**[Thesis Pillar 2]: [Title - e.g., "Differentiated Technology/Product"]**

[Similar structure - 3 paragraphs covering the opportunity, competitive positioning, and financial impact]

**[EMBED CHART: Competitive Positioning Matrix]** - 2×2 chart showing company vs. competitors on key dimensions

**[Thesis Pillar 3]: [Title - e.g., "Strong Execution and Management"]**

[Similar structure]

**[Add 2-3 more pillars as needed]**

**[EMBED CHART: Margin Expansion Pathway]** - Waterfall or line chart showing path to margin improvement

### Investment Risks

**Company-Specific Risks**

**[Risk 1]: [Title - e.g., "Customer Concentration"]**
[Description of risk, quantification if possible, mitigating factors. 2-3 sentences.]

**[Risk 2]: [Title - e.g., "Execution Risk on Product Roadmap"]**
[Description. 2-3 sentences.]

**[Risk 3-5]: [Additional company-specific risks]**
[Continue with 3-5 total company risks]

**Industry/Market Risks**

**[Risk 1]: [Title - e.g., "Regulatory Uncertainty"]**
[Description. 2-3 sentences.]

**[Risk 2]: [Title - e.g., "Intense Competition"]**
[Description. 2-3 sentences.]

**[Risk 3-4]: [Additional industry/market risks]**
[Continue with 2-4 total industry risks]

---

## PAGES 8-19: COMPANY 101

### Company Description (1 page)

**Overview**
[3-4 paragraphs describing:
- What the company does (in plain English)
- How it makes money
- Who its customers are
- Geographic presence
- Scale/size metrics]

**Business Model Diagram/Visual**
[Insert visual showing how the company creates value]

### Company History (2-3 pages)

**The Early Days: [Founding Story Title]**

[Paragraph on founding: who, when, why, initial vision]

**Timeline of Key Milestones**

```
[Year]: [Founding event, initial funding]
[Year]: [Product launch, key milestone]
[Year]: [Major partnership, funding round]
[Year]: [Geographic expansion, new product]
[Year]: [Recent achievement]
```

**[Major Turning Point or Pivot]**
[If applicable, describe any major strategic shifts]

**[Company Name] Today: [Current State Title]**
[Paragraphs describing current position, recent developments, current strategy]

### Management & Ownership (2 pages)

**Key Executives**

For each executive:
```
[Name] - [Title]
[Bio paragraph including:
- Current role and responsibilities
- Prior experience and track record
- Key accomplishments at company
- Education/credentials]
```

**Corporate Structure & Governance**
- Entity type (C-Corp, PBC, etc.)
- Board composition
- Special governance features
- [Include governance diagram if applicable]

**Ownership Structure** [if disclosed]
- Major shareholders and ownership %
- Strategic investors
- Employee ownership
- Insider ownership trends

### Core Technology/Products (2-3 pages)

**Technology Overview**
[Description of core technology/platform]

**Product Portfolio**

For each major product:
```
[Product Name]

Description:
[What it does, key features]

Target Customers:
[Who uses it, use cases]

Pricing Model:
[How it's priced, typical contract values]

Competitive Positioning:
[How it compares to alternatives]

Traction:
[Customers, revenue, growth metrics]
```

**Product Roadmap**
[Future products/features in development]

### Customers & Distribution (2-3 pages)

**Customer Base**
- Total customers: [number]
- Customer segments (Enterprise, Mid-Market, SMB)
- Geographic breakdown
- Customer case studies/testimonials

**Go-to-Market Strategy**
- Sales channels (direct, partner, etc.)
- Sales cycle and CAC
- Key partnerships for distribution
- Marketing strategy

**Customer Economics**
- LTV/CAC ratio
- Net retention rate
- Churn rates
- Expansion rates

---

## PAGES 20-22: GROWTH OUTLOOK

### Growth Framework Overview

**Short-term Growth Drivers (1-2 years)**
1. [Driver 1]
2. [Driver 2]
3. [Driver 3]

**Medium-term Growth Drivers (3-5 years)**
1. [Driver 1]
2. [Driver 2]

### Detailed Growth Driver Analysis

**[Growth Driver 1]: [Title]**

*Current State:*
[Baseline metrics, current performance]

*Opportunity:*
[Market size, company positioning, growth potential]

*Timeline & Milestones:*
- Near-term (1-2 years): [Expected progress]
- Medium-term (3-5 years): [Expected progress]

*Risks & Challenges:*
[What could prevent realization of this opportunity]

**[Repeat for each major growth driver]**

### Financial Projections

**Revenue Build-up**
[Visual showing how revenue grows from current to projected]

**Scenario Analysis**
[Table or chart showing Bear/Base/Bull case projections]

---

## PAGES 21-24: FINANCIAL ANALYSIS & PERFORMANCE

**LAYOUT PRINCIPLE**: This section should be VERY DENSE with 5-7 charts interspersed with financial tables. Each page should have multiple elements (table + 1-2 charts).

### Historical Financial Analysis

**Income Statement Highlights (3-5 Year History)**
```
                    2021    2022    2023    2024    LTM
Revenue ($M)        [X]     [X]     [X]     [X]     [X]
  Growth %          -       X%      X%      X%      X%
Gross Profit ($M)   [X]     [X]     [X]     [X]     [X]
  Margin %          X%      X%      X%      X%      X%
EBITDA ($M)         [X]     [X]     [X]     [X]     [X]
  Margin %          X%      X%      X%      X%      X%
Net Income ($M)     [X]     [X]     [X]     [X]     [X]
  Margin %          X%      X%      X%      X%      X%
FCF ($M)            [X]     [X]     [X]     [X]     [X]
```

**[CHART 1: Revenue Growth Trajectory]**
Line chart showing historical revenue with annotations for key milestones. Include growth % labels on chart.

**[CHART 2: REVENUE BY PRODUCT/SEGMENT]** ⭐ CRITICAL
Stacked area chart showing revenue composition by product line or business segment over time. This shows mix shift and which products are driving growth.
```
Example segments:
- Product A Revenue
- Product B Revenue
- Product C Revenue
- Services Revenue
```

**[CHART 3: REVENUE BY GEOGRAPHY]** ⭐ CRITICAL
Stacked bar chart showing revenue breakdown by geographic region over time.
```
Example regions:
- North America
- Europe
- Asia-Pacific
- Rest of World
```

### Financial Performance Analysis

**[CHART 4: Gross Margin Evolution]**
Line chart with annotations explaining margin drivers (scale, pricing, mix, etc.)

**[CHART 5: Operating Margin Progression]**
Waterfall chart showing path from gross margin to operating margin, or line chart showing EBITDA margin trend

**[CHART 6: Free Cash Flow Generation]**
Bar + line combo chart: Bars = FCF, Line = FCF margin %

**[CHART 7: Key Operating Metrics Dashboard]**
Multi-panel chart showing 3-4 key metrics:
- Customer count or user growth
- ARPU (Average Revenue Per User) or ACV (Annual Contract Value)
- Customer cohort retention or net revenue retention
- LTV/CAC or magic number or other unit economic metric

### Forward Projections (3-5 Years)

**Projected Financial Model**
```
                    2025E   2026E   2027E   2028E   2029E
Revenue ($M)        [X]     [X]     [X]     [X]     [X]
  Growth %          X%      X%      X%      X%      X%
Gross Profit ($M)   [X]     [X]     [X]     [X]     [X]
  Margin %          X%      X%      X%      X%      X%
EBITDA ($M)         [X]     [X]     [X]     [X]     [X]
  Margin %          X%      X%      X%      X%      X%
FCF ($M)            [X]     [X]     [X]     [X]     [X]
  FCF Margin %      X%      X%      X%      X%      X%
```

**Key Assumptions**
- Revenue growth drivers and assumptions
- Margin progression assumptions
- CapEx as % of revenue
- Working capital assumptions

**Charts:**
- Revenue bridge showing growth drivers
- Margin waterfall showing path to profitability/margin expansion
- Free cash flow trajectory

### Fundraising & Valuation [For Private Companies]

**Fundraising History**
```
Round    Date      Amount    Valuation    Lead Investor(s)
Seed     [Date]    $XM       $XM          [Investor]
Series A [Date]    $XM       $XM          [Investor]
Series B [Date]    $XM       $XM          [Investor]
[etc.]
```

**Valuation Evolution Chart**
[Visual showing valuation progression over time]

**Current Valuation Metrics**
- Latest valuation: $XXbn
- Implied valuation multiple: XX.Xx
- Comparison to public peers

---

## PAGES 26-31: INDUSTRY OVERVIEW

### Industry Definition & Market Size

**Industry Overview**
[2-3 paragraphs on:
- Industry definition and scope
- Current market size
- Historical growth rates
- Key trends and drivers]

**Market Size Chart**
[Visual showing market growth from historical through projected]

### Competitive Landscape

**Competitive Positioning Matrix**
[2x2 chart showing company vs. competitors on key dimensions]

**Competitive Comparison Table**
```
Metric              [Company]  Comp A   Comp B   Comp C   Comp D
Revenue ($B)        [X]        [X]      [X]      [X]      [X]
Growth %            X%         X%       X%       X%       X%
Market Share        X%         X%       X%       X%       X%
Gross Margin        X%         X%       X%       X%       X%
Key Differentiator  [X]        [X]      [X]      [X]      [X]
```

**Competitive Analysis Narrative**
[2-3 paragraphs analyzing:
- Competitive strengths and weaknesses
- Market positioning
- Share gains/losses
- Competitive moats]

### Total Addressable Market

**TAM Calculation**
```
Current TAM (2025):              $XXbn
Projected TAM (2030):            $XXbn
CAGR:                            XX%

Segmentation:
- [Segment A]:                   $XXbn
- [Segment B]:                   $XXbn
- [Segment C]:                   $XXbn
```

**TAM Growth Chart**
[Visual showing TAM expansion over time by segment]

**Company's Market Opportunity**
```
Total TAM (2030):                $XXbn
Serviceable TAM:                 $XXbn
Company's Realistic Share:       XX%
Implied Revenue Potential:       $XXbn
```

### Industry Dynamics

**Porter's Five Forces Analysis**
- Threat of new entrants: [High/Medium/Low] - [Explanation]
- Bargaining power of suppliers: [High/Medium/Low] - [Explanation]
- Bargaining power of buyers: [High/Medium/Low] - [Explanation]
- Threat of substitutes: [High/Medium/Low] - [Explanation]
- Industry rivalry: [High/Medium/Low] - [Explanation]

**Key Industry Trends**
1. [Trend 1]: [Description and impact]
2. [Trend 2]: [Description and impact]
3. [Trend 3]: [Description and impact]

---

## PAGES 32-34: VALUATION ANALYSIS

### Valuation Methodology Summary

```
Valuation Method            Weight    Implied Value    Weighted Value
DCF Analysis                50%       $XX - $YY        $ZZ
Trading Comparables         30%       $XX - $YY        $ZZ
Precedent Transactions      20%       $XX - $YY        $ZZ
                           ────       ─────────────    ─────────
Weighted Average Price Target         $AA - $BB        $CC
```

### DCF Analysis

**Key Assumptions**
```
Revenue Growth (2025-2029):         XX% CAGR
Terminal Growth Rate:               X.X%
WACC:                               X.X%
Terminal Year EBITDA Margin:        XX%
```

**Figure X - DCF Sensitivity Analysis ($/share)**

CRITICAL FORMAT: DCF sensitivity must be shown as a 2-way heat map table with color coding.

```
                        Terminal Growth Rate
WACC        2.0%      2.5%      3.0%      3.5%      4.0%
8.0%        $52       $55       $58       $62       $66
9.0%        $48       $51       $54       $57       $61
10.0%       $45       $47       $50       $53       $56
11.0%       $42       $44       $47       $49       $52
12.0%       $39       $41       $44       $46       $49

Color coding: Green (higher values) → Yellow (mid) → Red (lower values)
Source: [Firm Name] estimates.
```

**Scenario Analysis**
```
Scenario      Enterprise Value    Equity Value    Price/Share
Bear Case     $XXbn              $XXbn           $XX
Base Case     $XXbn              $XXbn           $XX
Bull Case     $XXbn              $XXbn           $XX
```

### Trading Comparables

**Figure X - Comparable Companies Analysis**

CRITICAL FORMAT: Comp table must have two-part structure with statistical summary.

**Part 1: Individual Company Data**
```
Company         Ticker   Market   EV/Rev   EV/Rev   EV/EBITDA  EV/EBITDA  Rev     EBITDA
                         Cap($B)  2024E    2025E    2024E      2025E      Growth  Margin
Peer A          PERA     XX.X     X.Xx     X.Xx     XX.X       XX.X       XX%     XX%
Peer B          PERB     XX.X     X.Xx     X.Xx     XX.X       XX.X       XX%     XX%
Peer C          PERC     XX.X     X.Xx     X.Xx     XX.X       XX.X       XX%     XX%
Peer D          PERD     XX.X     X.Xx     X.Xx     XX.X       XX.X       XX%     XX%
[Company]       COMP     XX.X     X.Xx     X.Xx     XX.X       XX.X       XX%     XX%
```

**Part 2: Statistical Summary**
```
Max                      XX.X     X.Xx     X.Xx     XX.X       XX.X       XX%     XX%
75th Percentile          XX.X     X.Xx     X.Xx     XX.X       XX.X       XX%     XX%
Median                   XX.X     X.Xx     X.Xx     XX.X       XX.X       XX%     XX%
25th Percentile          XX.X     X.Xx     X.Xx     XX.X       XX.X       XX%     XX%
Min                      XX.X     X.Xx     X.Xx     XX.X       XX.X       XX%     XX%

Source: FactSet, company filings, [Firm Name] estimates.
```

**Implied Valuation**
[Calculation showing application of peer multiples to company's metrics]

### Precedent Transactions [If Applicable]

**Figure X - Precedent Transaction Analysis**
```
Date        Target       Acquirer      Deal      EV/Rev   EV/EBITDA  Premium
                                      Value($B)
[MM/YYYY]   [Company A]  [Buyer A]    X.X       X.Xx     XX.X       XX%
[MM/YYYY]   [Company B]  [Buyer B]    X.X       X.Xx     XX.X       XX%
[MM/YYYY]   [Company C]  [Buyer C]    X.X       X.Xx     XX.X       XX%
────────────────────────────────────────────────────────────────────
Median                                          X.Xx     XX.X       XX%

Source: Capital IQ, company filings, [Firm Name] estimates.
```

**Control Premium Analysis**
[Discussion of typical premiums in the industry]

### Valuation Summary

**Figure X - Valuation Football Field**

CRITICAL FORMAT: Football field must be a horizontal bar chart showing all valuation methods.

```
Valuation Method                Low End ────── Range ────── High End

DCF Analysis                    $42 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ $58

Trading Comps (NTM)             $45 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ $55

Precedent Trans.                $48 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ $60
                                                      ↑
                                            Current Price: $50
────────────────────────────────────────────────────────────────
Valuation Range:                $42                        $60

Color coding: Each method should have distinct color bar
Add vertical line showing current stock price
Source: [Firm Name] estimates.
```

**Price Target & Recommendation**
```
Current Price:              $XX.XX ([Date])
Price Target:               $YY.YY
Upside/Downside:            ZZ%

Recommendation:             BUY / HOLD / SELL
Time Horizon:               12 months

Catalysts:
• [Near-term catalyst with timeframe]
• [Medium-term catalyst with timeframe]
• [Long-term catalyst with timeframe]
```

---

## PAGES 35+: APPENDICES & DISCLOSURES

### Appendix A: Detailed Financial Model
[Reference to Excel model]

### Appendix B: Management Bios
[Extended bios if not included in main text]

### Appendix C: Product Detail
[Additional product information if needed]

### Appendix D: Industry Data Sources
[List of sources used for industry analysis]

### Required Disclosures
- Analyst certification
- Important disclosures
- Company-specific disclosures
- Legal entity disclosures
- Other regulatory disclosures

---

## GRAPHICS & CHARTS TO INCLUDE

**TARGET: 20-30+ charts throughout the report**

**CRITICAL PRINCIPLE**: Charts should be embedded within text sections, NOT grouped on separate pages. Every page (except TOC) should have at least one chart or table.

### Page 1 - Executive Summary (3 charts)
1. Revenue/ARR growth trajectory (line chart, historical + projected)
2. Key metrics dashboard (multi-panel chart)
3. Market positioning or margin progression

### Pages 3-5 - Investment Thesis & Risks (3 charts)
4. TAM growth and opportunity (stacked area chart)
5. Competitive positioning matrix (2×2 with bubbles)
6. Margin expansion pathway (waterfall or line)

### Pages 6-17 - Company 101 (6-8 charts)
7. Business model diagram (flow chart)
8. Company timeline (horizontal timeline)
9. Funding history (bar chart with valuation line)
10. Organization chart
11. Product portfolio matrix
12. Customer segmentation (pie or tree map)
13. Geographic revenue breakdown
14. Customer cohort retention

### Pages 18-20 - Growth Outlook (4 charts)
15. Revenue bridge showing drivers (waterfall)
16. Market share evolution (line chart)
17. Product roadmap (timeline)
18. Geographic expansion (map with timeline)

### Pages 21-24 - Financials (7 charts) ⭐ CRITICAL SECTION
19. Revenue growth trajectory (line with annotations)
20. **Revenue by product/segment** (stacked area) ⭐ MUST HAVE
21. **Revenue by geography** (stacked bar) ⭐ MUST HAVE
22. Gross margin evolution (line chart)
23. Operating margin progression (waterfall or line)
24. Free cash flow trajectory (bar + line combo)
25. Key operating metrics dashboard (multi-panel)
26. Scenario comparison (grouped bar: Bear/Base/Bull)

### Pages 25-30 - Industry Overview (6 charts)
27. Market size evolution (area chart with CAGR)
28. Competitive landscape map (2×2)
29. Market share pie chart
30. Market share evolution over time (line chart)
31. TAM segmentation
32. Industry trend charts

### Pages 31-34 - Valuation (5 charts)
33. DCF sensitivity analysis (heat map)
34. DCF waterfall (PV of cash flows → equity value)
35. Trading comps scatter plot (growth vs. multiple)
36. Peer valuation multiples (grouped bar)
37. Valuation football field (range chart)
38. Price target scenarios (bar with upside/downside)

**Chart Style Guidelines:**
- **Consistent color scheme** throughout (pick 3-5 brand colors)
- **Professional fonts** (Arial, Calibri, or similar)
- **Clear labels and legends** on every chart
- **Source citations** at bottom of each chart
- **High information density** - use chart space efficiently
- **Mix of chart types** for visual interest
- **Annotations** to highlight key insights
- **Embedded in text** - never standalone pages
- **Sparklines in tables** where appropriate

---

## NOTES ON USING THIS TEMPLATE

1. **PAGE 1 IS CRITICAL:** The executive summary on page 1 must contain ALL key information - fast facts, financial snapshot, 3 charts, valuation summary, thesis, and risks. This is the most important page.

2. **MAXIMUM DENSITY:** Professional equity research is EXTREMELY information-dense. Every page should be packed with interspersed text, charts, and tables. Aim for 60-80% page coverage with minimal white space.

3. **NO ORPHANED SECTIONS:** Never have a section header alone, or a single chart/table on its own page. Always combine elements. Example: DON'T put "Financial Snapshot" on page 6 by itself - integrate it with surrounding content.

4. **20-30+ CHARTS:** Include extensive graphics throughout, with specific emphasis on:
   - **Revenue by product/segment** (stacked area chart)
   - **Revenue by geography** (stacked bar chart)
   - **Financial performance trends** (multiple charts)
   - Charts should be embedded within text, not grouped separately

5. **Use DOC Skill:** This outline should be converted to a professional Word document using the DOC skill, with proper formatting, styles, headers/footers, and page numbers

6. **Intersplice Content:** Text paragraphs should have charts embedded inline. Each page should have 2-4 distinct elements (tables, charts, text blocks).

7. **Consistent Formatting:** Use consistent styles for headers, body text, tables, and charts throughout. Pick a color scheme and stick to it.

8. **References:** Include citations and sources for all data points

9. **Proofread:** Always proofread for accuracy, especially financial data and calculations

10. **Executive Summary Last:** While it appears on page 1, write this section last after completing the full analysis

11. **Balance:** Present both positive and negative aspects objectively

12. **Specific > Generic:** Use specific data and examples rather than generic statements

### Referencia: references/task1-company-research.md

# Task 1: Company Research - Detailed Workflow

This document provides step-by-step instructions for executing Task 1 (Company Research) of the initiating-coverage skill.

## Task Overview

**Purpose**: Research company's business, management, competitive position, industry, and risks.

**Prerequisites**: ✅ None (fully independent)
- Company name or ticker symbol only

**Output**: Company Research Document (6,000-8,000 words)

---

## Data Sources to Gather

### Primary Sources (Company)
- **SEC Filings (for public companies):**
  - Latest 10-K: Business description, risk factors, MD&A, financials
  - Recent 10-Qs: Quarterly updates
  - DEF 14A (Proxy): Executive compensation, board composition
  - 8-Ks: Material events, acquisitions, management changes

- **Company Website & IR:**
  - Investor presentations
  - Earnings transcripts (last 2-3 quarters)
  - Press releases
  - Product documentation

- **For Private Companies:**
  - Company website and blog
  - Press releases and media coverage
  - LinkedIn for management bios
  - Crunchbase or PitchBook for funding history

### Secondary Sources (Industry/Competitive)
- Competitor websites and SEC filings
- Industry research reports (Gartner, Forrester, IDC, etc.)
- News articles and trade publications
- Market research reports
- LinkedIn profiles for key executives

### Key Information to Extract

**Key Information:**
- Company founding date, headquarters, employee count
- Revenue size and growth trajectory (if available)
- Product portfolio and pricing
- Customer segments and case studies
- Management backgrounds and track records
- Competitive landscape and market share
- Industry trends and growth drivers
- Regulatory considerations
- High-level financial metrics (from 10-K prose, not detailed extraction)

---

## Step-by-Step Research Workflow

### Step 1: Initial Data Collection

1. **Start with company website**
   - Read About/Company pages
   - Review product pages
   - Identify customer case studies
   - Note key metrics mentioned (employees, customers, etc.)

2. **Gather SEC filings (if public)**
   - Download latest 10-K from SEC EDGAR
   - Download most recent 10-Q
   - Download latest DEF 14A (proxy statement)
   - Note filing dates

3. **Read earnings materials**
   - Latest earnings transcript
   - Most recent investor presentation
   - Press releases from last 12 months

4. **Document basic facts**
   - Founding date and story
   - Headquarters location
   - Employee count
   - Products/services
   - Key customers

### Step 2: Business Model Analysis

1. **Map revenue streams**
   - What does the company sell?
   - How is it priced? (subscription, transaction, license, etc.)
   - Who pays?
   - What are typical deal sizes?

2. **Understand customer segments**
   - Enterprise vs. SMB vs. consumer
   - Industries served
   - Geographic distribution
   - Customer concentration (top 10 customers)

3. **Document go-to-market**
   - Direct sales vs. channel partners
   - Sales cycle length
   - Customer acquisition strategy
   - Distribution model

4. **Identify unit economics**
   - LTV/CAC if available
   - Gross margins
   - Net revenue retention
   - Payback periods

### Step 3: Management Research

**For each of 3-4 key executives:**

1. **Identify key leaders**
   - CEO (always required)
   - CFO (always required)
   - COO, CTO, or other C-suite (2 additional)

2. **Research each executive**
   - Find LinkedIn profile
   - Review DEF 14A for background
   - Search for press interviews
   - Note tenure at company

3. **Write 300-400 word bio including:**
   - Current role and responsibilities
   - Prior roles and companies (last 2-3 positions)
   - Key accomplishments and track record
   - Education and credentials
   - Years of experience in industry
   - Time at current company

4. **Assess governance**
   - Board composition and independence
   - Key board members and their backgrounds
   - Insider ownership percentage
   - Executive compensation structure

### Step 4: Competitive Intelligence

1. **Identify 5-10 competitors**
   - Direct competitors (same products/markets)
   - Indirect competitors (substitute solutions)
   - Emerging competitors (disruptors)
   - Check 10-K for company's own list of competitors

2. **Research each competitor**
   - Visit competitor website
   - Review their SEC filings (if public)
   - Note key products and positioning
   - Identify differentiators
   - Estimate market share (if data available)

3. **Create competitive framework**
   - Map on key dimensions (price, features, scale, etc.)
   - Identify company's competitive advantages
   - Note competitive vulnerabilities
   - Assess switching costs and network effects

4. **Document competitive insights**
   - Who are the market leaders?
   - Where does this company rank?
   - What are unique differentiators?
   - What are competitive threats?

### Step 5: Industry Analysis

1. **Define the industry**
   - Industry classification (NAICS/SIC)
   - Scope and boundaries
   - Related/adjacent industries

2. **Size the market**
   - Total addressable market (TAM)
   - Serviceable addressable market (SAM)
   - Serviceable obtainable market (SOM)
   - Current penetration rate

3. **Research growth drivers**
   - Historical market growth rate
   - Projected growth rate (next 3-5 years)
   - Key trends accelerating/decelerating growth
   - Technology changes impacting industry

4. **Understand industry structure**
   - Fragmented vs. consolidated
   - Barriers to entry
   - Supplier/buyer power
   - Threat of substitutes
   - Regulatory environment

### Step 6: Risk Assessment

Identify 8-12 risks across four categories. For each risk, write 50-100 words.

**Company-Specific Risks (4-6 risks):**
- Execution risk (can management deliver?)
- Customer concentration (top customers)
- Key person dependency
- Product/technology obsolescence
- Geographic concentration
- Integration risk (if recent M&A)

**Industry/Market Risks (3-4 risks):**
- Competitive intensity
- Regulatory changes
- Technology disruption
- Market saturation

**Financial Risks (2-3 risks):**
- Profitability timeline
- Funding requirements
- Debt levels and covenants
- Cash burn rate (if unprofitable)

**Macroeconomic Risks (2-3 risks):**
- Economic sensitivity (cyclical vs. defensive)
- Interest rate sensitivity
- Foreign exchange exposure
- Geopolitical factors

**For each risk:**
- Describe the risk clearly
- Quantify impact if possible
- Note likelihood/severity
- Identify mitigating factors

### Step 7: Synthesis and Writing

**Write document following this structure:**

1. **Company Overview** (800-1,200 words)
   - What does the company do? (plain English)
   - How do they make money? (business model)
   - Where do they operate? (geographic presence)
   - How large are they? (revenue, employees, customers)
   - Key metrics and scale indicators

2. **Company History** (800-1,200 words)
   - Founding story (who, when, why, where)
   - Timeline of major milestones
   - Strategic pivots or transformations
   - Key acquisitions
   - Recent developments (last 1-2 years)

3. **Management Team** (1,000-1,400 words)
   - 300-400 word bio for each of 3-4 executives
   - Board composition and governance
   - Insider ownership
   - Management track record assessment

4. **Products & Services** (700-1,000 words)
   - Detailed product portfolio
   - Key features and capabilities
   - Product differentiation
   - Target customers and use cases
   - Pricing models and typical deal sizes

5. **Customers & Go-to-Market** (500-700 words)
   - Customer segments and profiles
   - Distribution channels
   - Sales strategy and cycle
   - Key partnerships
   - Customer case studies

6. **Industry Overview** (800-1,200 words)
   - Industry definition and scope
   - Market size and structure
   - Growth rates (historical and projected)
   - Key trends and drivers
   - Regulatory environment
   - Industry dynamics

7. **Competitive Landscape** (700-1,000 words)
   - Analysis of 5-10 key competitors
   - Market positioning framework
   - Company's competitive advantages
   - Competitive vulnerabilities
   - Market share analysis

8. **Market Opportunity** (500-700 words)
   - TAM sizing and methodology
   - Market growth projections
   - Company's serviceable market
   - Market share opportunity
   - Penetration strategy

9. **Risk Assessment** (600-900 words)
   - Company-specific risks (4-6)
   - Industry/market risks (3-4)
   - Financial risks (2-3)
   - Macroeconomic risks (2-3)
   - Each risk: 50-100 word description

**Data Sources Section**
- List all sources used
- Include dates and URLs
- Organize by source type

---

## Quality Standards

### Content Depth
- Each section must meet minimum word count targets
- Analysis should be substantive, not just descriptive
- Use specific examples and quantitative data
- Cite sources throughout
- Maintain objectivity and balance

### Management Bios
- 300-400 words per executive for 3-4 key executives
- Must include: current role, prior experience, key accomplishments, education
- Provide enough detail to assess track record and capabilities

### Competitive Analysis
- Must analyze 5-10 specific competitors
- Include both direct and indirect competitors
- Assess relative positioning on key dimensions
- Identify company's competitive advantages and vulnerabilities
- Use specific data and examples

### Risk Assessment
- Must identify 8-12 distinct risks across all four categories
- Each risk needs 50-100 word description
- Quantify impact where possible
- Note mitigating factors
- Cover all four risk categories

### Writing Quality
- Professional, analytical tone
- Lead with key insights
- Use concrete examples and data
- Avoid generic statements
- Proper citations throughout

---

## Output Format

```
COMPANY RESEARCH REPORT: [Company Name]
Date: [Date]
Analyst: [Your name if applicable]

TABLE OF CONTENTS
1. Company Overview
2. Company History
3. Management Team
4. Products & Services
5. Customers & Go-to-Market
6. Industry Overview
7. Competitive Landscape
8. Market Opportunity (TAM)
9. Risk Assessment

======================================

1. COMPANY OVERVIEW (800-1,200 words)

[Content]

2. COMPANY HISTORY (800-1,200 words)

[Content]

3. MANAGEMENT TEAM (1,000-1,400 words)

[Name], [Title]
[300-400 word bio]

[Repeat for 3-4 key executives]

[Governance section]

4. PRODUCTS & SERVICES (700-1,000 words)

[Content]

5. CUSTOMERS & GO-TO-MARKET (500-700 words)

[Content]

6. INDUSTRY OVERVIEW (800-1,200 words)

[Content]

7. COMPETITIVE LANDSCAPE (700-1,000 words)

[Content]

8. MARKET OPPORTUNITY (500-700 words)

[Content]

9. RISK ASSESSMENT (600-900 words)

Company-Specific Risks:
[4-6 risks with descriptions]

Industry/Market Risks:
[3-4 risks with descriptions]

Financial Risks:
[2-3 risks with descriptions]

Macroeconomic Risks:
[2-3 risks with descriptions]

======================================

DATA SOURCES
[List all sources with dates and URLs]
```

---

## Success Criteria

A successful Task 1 completion should deliver:

1. Meet 6,000-8,000 word target (verify word count)
2. Include all 9 required sections with target word counts
3. Provide substantive analysis, not just description
4. Use specific examples and quantitative data
5. Cite all sources properly
6. Enable reader to understand:
   - What the company does and how it makes money
   - Quality and track record of management team
   - Company's competitive position
   - Market opportunity size
   - Key risks to consider

---

## File Naming Convention

Save the output as:

`[Company]_Research_Document_[Date].md`

Example: `Tesla_Research_Document_2024-10-27.md`

---

## Next Steps

After completing Task 1, the research document will be used:

- As standalone company analysis
- As input for Task 2 (Financial Modeling) - provides business context for projections
- As input for Task 4 (Chart Generation) - provides data for company/competitive charts
- As foundation for Task 5 (Report Assembly) - Company 101 sections copied verbatim

### Referencia: references/task2-financial-modeling.md

# Task 2: Financial Modeling - Detailed Workflow

This document provides step-by-step instructions for executing Task 2 (Financial Modeling) of the initiating-coverage skill.

## Task Overview

**Purpose**: Extract historical financials and build comprehensive Excel financial model with projections and scenarios.

**Prerequisites**: ⚠️ Verify before starting
- **Required**: Access to company financial data
  - For public companies: Latest 10-K and recent 10-Qs from SEC EDGAR
  - For private companies: Financial statements or estimates from available sources
  - OR: Pre-extracted historical financials provided by user
- **Optional**: Company research (Task 1) for business context

**Output**: Excel Financial Model (.xlsx) with 6 essential tabs:
1. Revenue Model
2. Income Statement
3. Cash Flow Statement
4. Balance Sheet
5. Scenarios
6. DCF Inputs

---

## Input Verification

**BEFORE STARTING - CHECK:**

**Option A: Extract financials directly (most common)**
- [ ] Have access to 10-K filings (public company)?
- [ ] OR have access to financial statements (private company)?
- [ ] Ready to create Excel file for historical extraction?

**Option B: User has pre-extracted financials**
- [ ] Historical financials file provided? (.xlsx or other format)
- [ ] Contains 3-5 years of income statement, cash flow, balance sheet?
- [ ] Data is clean and ready to use?

**Optional Context:**
- [ ] Company research (Task 1) complete for business understanding?

**IF VERIFICATION FAILS**: Stop and obtain access to financial statements (10-K or equivalent) before proceeding.

---

## Model Structure and Formatting

### Color Coding (Industry Standard)
- **Blue text**: Hardcoded inputs (user can change)
- **Black text**: Formulas and calculations
- **Green text**: Links to other sheets
- **Red text**: Errors or flags (should be resolved)

### Formatting Standards
- Professional borders and shading
- Clear section headers
- Grouped rows for collapsibility
- Named ranges for key inputs/outputs
- No hardcoded numbers in formulas (except constants like 12 months)
- Clear units ($ thousands, $ millions, etc.)

### Formula Best Practices
- All numbers should flow from assumptions
- Change an assumption → entire model updates
- No circular references
- Use named ranges for key cells
- Keep formulas simple and auditable
- Add comments for complex calculations

---

## Step-by-Step Modeling Workflow

### Step 1: Extract Historical Financials

**If historical financials are already extracted, skip to Step 2.**

**For Public Companies:**

1. **Download 10-K Filing**
   - Go to SEC EDGAR (https://www.sec.gov/edgar/searchedgar/companysearch.html)
   - Search for company name or ticker
   - Download latest 10-K (annual report)
   - Navigate to Item 8: Financial Statements and Supplementary Data

2. **Create Historical Financials Excel File**
   - File name: `[Company]_Historical_Financials_[Date].xlsx`
   - This file will be the foundation for the model

3. **Extract Income Statement (3-5 years)**
   - Create Sheet 1: "Historical Income Statement"
   - Extract ALL line items for 3-5 years:
     - Revenue (total and by segment if disclosed)
     - Cost of revenue / COGS
     - Gross profit
     - Operating expenses (R&D, Sales & Marketing, G&A broken out)
     - EBITDA (calculate if not disclosed: EBIT + D&A)
     - EBIT / Operating income
     - Interest expense/income
     - Other income/expense
     - Pre-tax income
     - Income tax and tax rate
     - Net income
     - EPS (basic and diluted)
     - Shares outstanding (basic and diluted)

4. **Extract Cash Flow Statement (3-5 years)**
   - Create Sheet 2: "Historical Cash Flow"
   - Extract ALL line items:
     - Operating activities (starting from net income)
     - Depreciation & amortization
     - Stock-based compensation
     - Changes in working capital (receivables, inventory, payables)
     - Cash from operations
     - Investing activities (CapEx, acquisitions)
     - Financing activities (debt issuance/repayment, equity, dividends)
     - Net change in cash
     - Beginning and ending cash

5. **Extract Balance Sheet (3-5 years)**
   - Create Sheet 3: "Historical Balance Sheet"
   - Extract ALL line items:
     - Current assets (cash, receivables, inventory, other)
     - Non-current assets (PP&E, intangibles, goodwill)
     - Total assets
     - Current liabilities (payables, accrued expenses, current debt)
     - Non-current liabilities (long-term debt, deferred taxes)
     - Total liabilities
     - Shareholders' equity (common stock, retained earnings)
     - Total liabilities + equity

6. **Calculate Historical Metrics**
   - Create Sheet 4: "Historical Metrics"
   - Calculate from statements:
     - Revenue growth % (YoY)
     - Gross margin %
     - EBITDA margin %
     - Operating margin %
     - Net margin %
     - Free cash flow (CFO - CapEx)
     - FCF margin %
     - ROIC (approximate: NOPAT / Invested Capital)
     - Debt/Equity ratio
     - Current ratio (Current Assets / Current Liabilities)

7. **Document Sources and Notes**
   - Create Sheet 5: "Notes"
   - Document:
     - 10-K filing date and fiscal year end
     - Any one-time items or adjustments noted
     - Non-GAAP vs GAAP differences
     - Segment breakdown (if revenue split by product/geography)
     - Data quality notes and limitations

**For Private Companies:**

1. **Gather Available Data**
   - Financial statements (if available)
   - Press releases with revenue figures
   - Funding announcements
   - Industry estimates or comparable company data

2. **Create Simplified Historical File**
   - Estimated revenue (if available)
   - Estimated margins (from comparables if needed)
   - Key ratios and metrics
   - Document all assumptions and sources

**Verification:**
- [ ] All 3 financial statements extracted (3-5 years)
- [ ] Numbers reconcile across statements (net income ties)
- [ ] Key metrics calculated correctly
- [ ] Excel file saved and can be opened
- [ ] Data sources documented (10-K dates, page numbers)

**Foundation for projection model is now complete. Proceed to Step 2.**
   - Capital expenditures
   - Working capital items
   - Debt and interest expense
   - Share count (basic and diluted)

3. **Organize historical data for entry**
   - Prepare 3-5 years of actuals
   - Will be entered directly into Income Statement, Cash Flow Statement, and Balance Sheet tabs
   - Historical years in columns, projected years following

4. **Calculate historical trends**
   - Revenue CAGR
   - Margin progression
   - OpEx leverage
   - Working capital patterns
   - CapEx as % of revenue
   - These trends will inform projection assumptions

**Note**: Assumptions will be documented directly in each tab as blue text inputs, not in a separate tab.

### Step 2: Model Revenue

**CRITICAL: This is the most important and detailed part of the model.**

#### A. Revenue by Product/Category (20-30 rows)

Create detailed table:
```
                        2021A   2022A   2023A   2024A   2025E   2026E   2027E   2028E   2029E
Product Category A
  Sub-product A1        XX      XX      XX      XX      XX      XX      XX      XX      XX
  Sub-product A2        XX      XX      XX      XX      XX      XX      XX      XX      XX
  Sub-product A3        XX      XX      XX      XX      XX      XX      XX      XX      XX
  Category A Total      XX      XX      XX      XX      XX      XX      XX      XX      XX
  % of Total Rev        X%      X%      X%      X%      X%      X%      X%      X%      X%
  YoY Growth %          -       X%      X%      X%      X%      X%      X%      X%      X%

Product Category B
  [Similar structure]

[Continue for all product categories]

Services Revenue        XX      XX      XX      XX      XX      XX      XX      XX      XX
Other Revenue           XX      XX      XX      XX      XX      XX      XX      XX      XX

TOTAL REVENUE           XX      XX      XX      XX      XX      XX      XX      XX      XX
Total Revenue Growth %  -       X%      X%      X%      X%      X%      X%      X%      X%
```

**Key Requirements:**
- Show absolute revenue ($M) for each category
- Calculate % of total revenue for each category
- Show YoY growth % for each category
- Must have granular sub-categories (not just 3-5 top-level categories)
- Show mix shift over time
- Link all projections to Assumptions tab

#### B. Revenue by Geography (15-20 rows)

Create detailed table:
```
                        2021A   2022A   2023A   2024A   2025E   2026E   2027E   2028E   2029E
North America
  United States         XX      XX      XX      XX      XX      XX      XX      XX      XX
  Canada                XX      XX      XX      XX      XX      XX      XX      XX      XX
  Mexico                XX      XX      XX      XX      XX      XX      XX      XX      XX
  NA Total              XX      XX      XX      XX      XX      XX      XX      XX      XX
  % of Total            X%      X%      X%      X%      X%      X%      X%      X%      X%
  YoY Growth %          -       X%      X%      X%      X%      X%      X%      X%      X%

Europe
  UK                    XX      XX      XX      XX      XX      XX      XX      XX      XX
  Germany               XX      XX      XX      XX      XX      XX      XX      XX      XX
  France                XX      XX      XX      XX      XX      XX      XX      XX      XX
  Other Europe          XX      XX      XX      XX      XX      XX      XX      XX      XX
  Europe Total          XX      XX      XX      XX      XX      XX      XX      XX      XX
  % of Total            X%      X%      X%      X%      X%      X%      X%      X%      X%
  YoY Growth %          -       X%      X%      X%      X%      X%      X%      X%      X%

Asia-Pacific
  [Similar structure]

Rest of World
  [Similar structure]

TOTAL REVENUE           XX      XX      XX      XX      XX      XX      XX      XX      XX
```

**Verification:**
- Revenue by product total = Revenue by geography total = Total revenue
- All percentages sum to 100%
- Growth rates calculated correctly

#### C. Revenue by Channel (if applicable)

```
                        2021A   2022A   2023A   2024A   2025E   2026E   2027E   2028E   2029E
Direct Sales            XX      XX      XX      XX      XX      XX      XX      XX      XX
E-commerce/Online       XX      XX      XX      XX      XX      XX      XX      XX      XX
Wholesale/Partner       XX      XX      XX      XX      XX      XX      XX      XX      XX
Retail Stores
  Company-owned stores  XX      XX      XX      XX      XX      XX      XX      XX      XX
  Store count           XX      XX      XX      XX      XX      XX      XX      XX      XX
  Sales per store       XX      XX      XX      XX      XX      XX      XX      XX      XX
Other Channels          XX      XX      XX      XX      XX      XX      XX      XX      XX

TOTAL REVENUE           XX      XX      XX      XX      XX      XX      XX      XX      XX
```

### Step 3: Model Operating Expenses

#### A. Cost of Revenue
1. **Break down COGS components**
   - Product costs (materials, manufacturing)
   - Shipping and logistics
   - Service delivery costs
   - Other direct costs

2. **Link to revenue**
   - Calculate COGS as % of revenue
   - Model gross margin by year
   - Link to Assumptions tab

#### B. R&D Expenses
```
Research & Development  2021A   2022A   2023A   2024A   2025E   2026E   2027E   2028E   2029E
R&D Headcount           XX      XX      XX      XX      XX      XX      XX      XX      XX
R&D Comp per head       XX      XX      XX      XX      XX      XX      XX      XX      XX
R&D Personnel Costs     XX      XX      XX      XX      XX      XX      XX      XX      XX
R&D Other Costs         XX      XX      XX      XX      XX      XX      XX      XX      XX
Total R&D               XX      XX      XX      XX      XX      XX      XX      XX      XX
% of Revenue            X%      X%      X%      X%      X%      X%      X%      X%      X%
```

#### C. Sales & Marketing Expenses
```
Sales & Marketing       2021A   2022A   2023A   2024A   2025E   2026E   2027E   2028E   2029E
S&M Headcount           XX      XX      XX      XX      XX      XX      XX      XX      XX
S&M Comp per head       XX      XX      XX      XX      XX      XX      XX      XX      XX
S&M Personnel Costs     XX      XX      XX      XX      XX      XX      XX      XX      XX
Marketing Spend         XX      XX      XX      XX      XX      XX      XX      XX      XX
S&M Other Costs         XX      XX      XX      XX      XX      XX      XX      XX      XX
Total S&M               XX      XX      XX      XX      XX      XX      XX      XX      XX
% of Revenue            X%      X%      X%      X%      X%      X%      X%      X%      X%
```

#### D. General & Administrative
```
G&A                     2021A   2022A   2023A   2024A   2025E   2026E   2027E   2028E   2029E
G&A Headcount           XX      XX      XX      XX      XX      XX      XX      XX      XX
G&A Comp per head       XX      XX      XX      XX      XX      XX      XX      XX      XX
G&A Personnel Costs     XX      XX      XX      XX      XX      XX      XX      XX      XX
G&A Other Costs         XX      XX      XX      XX      XX      XX      XX      XX      XX
Total G&A               XX      XX      XX      XX      XX      XX      XX      XX      XX
% of Revenue            X%      X%      X%      X%      X%      X%      X%      X%      X%
```

#### E. Depreciation & Amortization
- Link to CapEx schedule
- Apply depreciation rates from Assumptions
- Calculate annual D&A

### Step 4: Build Income Statement

**Create full P&L with 40-50 line items:**

```
INCOME STATEMENT        2021A   2022A   2023A   2024A   2025E   2026E   2027E   2028E   2029E

REVENUE
[Link to Revenue Model tab]
Total Revenue           XX      XX      XX      XX      XX      XX      XX      XX      XX
  YoY Growth %          -       X%      X%      X%      X%      X%      X%      X%      X%

COST OF REVENUE
[Link to COGS breakdown]
Total COGS              XX      XX      XX      XX      XX      XX      XX      XX      XX

GROSS PROFIT            XX      XX      XX      XX      XX      XX      XX      XX      XX
  Gross Margin %        X%      X%      X%      X%      X%      X%      X%      X%      X%

OPERATING EXPENSES
Total R&D               XX      XX      XX      XX      XX      XX      XX      XX      XX
  % of Revenue          X%      X%      X%      X%      X%      X%      X%      X%      X%
Total S&M               XX      XX      XX      XX      XX      XX      XX      XX      XX
  % of Revenue          X%      X%      X%      X%      X%      X%      X%      X%      X%
Total G&A               XX      XX      XX      XX      XX      XX      XX      XX      XX
  % of Revenue          X%      X%      X%      X%      X%      X%      X%      X%      X%
Depreciation & Amort.   XX      XX      XX      XX      XX      XX      XX      XX      XX

Total Operating Exp.    XX      XX      XX      XX      XX      XX      XX      XX      XX
  % of Revenue          X%      X%      X%      X%      X%      X%      X%      X%      X%

EBITDA                  XX      XX      XX      XX      XX      XX      XX      XX      XX
  EBITDA Margin %       X%      X%      X%      X%      X%      X%      X%      X%      X%

EBIT                    XX      XX      XX      XX      XX      XX      XX      XX      XX
  EBIT Margin %         X%      X%      X%      X%      X%      X%      X%      X%      X%

Interest expense        (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
Interest income         XX      XX      XX      XX      XX      XX      XX      XX      XX
Other income/(expense)  XX      XX      XX      XX      XX      XX      XX      XX      XX

Pre-tax income          XX      XX      XX      XX      XX      XX      XX      XX      XX

Income tax              (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
  Tax rate %            X%      X%      X%      X%      X%      X%      X%      X%      X%

NET INCOME              XX      XX      XX      XX      XX      XX      XX      XX      XX
  Net Margin %          X%      X%      X%      X%      X%      X%      X%      X%      X%

SHARES OUTSTANDING
Basic shares (M)        XX      XX      XX      XX      XX      XX      XX      XX      XX
Diluted shares (M)      XX      XX      XX      XX      XX      XX      XX      XX      XX

EARNINGS PER SHARE
Basic EPS               $X.XX   $X.XX   $X.XX   $X.XX   $X.XX   $X.XX   $X.XX   $X.XX   $X.XX
Diluted EPS             $X.XX   $X.XX   $X.XX   $X.XX   $X.XX   $X.XX   $X.XX   $X.XX   $X.XX
```

### Step 5: Build Cash Flow Statement

```
CASH FLOW STATEMENT     2021A   2022A   2023A   2024A   2025E   2026E   2027E   2028E   2029E

OPERATING ACTIVITIES
Net Income              XX      XX      XX      XX      XX      XX      XX      XX      XX
Adjustments:
  Depreciation & Amort. XX      XX      XX      XX      XX      XX      XX      XX      XX
  Stock-based comp      XX      XX      XX      XX      XX      XX      XX      XX      XX
  Other non-cash        XX      XX      XX      XX      XX      XX      XX      XX      XX

Changes in WC:
  Accounts Receivable   (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
  Inventory             (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
  Accounts Payable      XX      XX      XX      XX      XX      XX      XX      XX      XX
  Other working capital (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)

Cash from Operations    XX      XX      XX      XX      XX      XX      XX      XX      XX

INVESTING ACTIVITIES
Capital Expenditures    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
Acquisitions            (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
Other investing         XX      XX      XX      XX      XX      XX      XX      XX      XX

Cash from Investing     (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)

FREE CASH FLOW          XX      XX      XX      XX      XX      XX      XX      XX      XX
  FCF Margin %          X%      X%      X%      X%      X%      X%      X%      X%      X%

FINANCING ACTIVITIES
Debt issuance           XX      XX      XX      XX      XX      XX      XX      XX      XX
Debt repayment          (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
Equity issuance         XX      XX      XX      XX      XX      XX      XX      XX      XX
Dividends paid          (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
Other financing         XX      XX      XX      XX      XX      XX      XX      XX      XX

Cash from Financing     XX      XX      XX      XX      XX      XX      XX      XX      XX

NET CHANGE IN CASH      XX      XX      XX      XX      XX      XX      XX      XX      XX

Beginning Cash          XX      XX      XX      XX      XX      XX      XX      XX      XX
Ending Cash             XX      XX      XX      XX      XX      XX      XX      XX      XX
```

### Step 6: Build Balance Sheet

Create full balance sheet with 35-45 line items:

```
BALANCE SHEET           2021A   2022A   2023A   2024A   2025E   2026E   2027E   2028E   2029E

ASSETS
Current Assets:
  Cash & Equivalents    XX      XX      XX      XX      XX      XX      XX      XX      XX
  Accounts Receivable   XX      XX      XX      XX      XX      XX      XX      XX      XX
  Inventory             XX      XX      XX      XX      XX      XX      XX      XX      XX
  Prepaid expenses      XX      XX      XX      XX      XX      XX      XX      XX      XX
  Other current assets  XX      XX      XX      XX      XX      XX      XX      XX      XX
Total Current Assets    XX      XX      XX      XX      XX      XX      XX      XX      XX

Non-Current Assets:
  PP&E, gross           XX      XX      XX      XX      XX      XX      XX      XX      XX
  Accumulated Depr.     (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
  PP&E, net             XX      XX      XX      XX      XX      XX      XX      XX      XX
  Intangible assets     XX      XX      XX      XX      XX      XX      XX      XX      XX
  Goodwill              XX      XX      XX      XX      XX      XX      XX      XX      XX
  Other non-current     XX      XX      XX      XX      XX      XX      XX      XX      XX
Total Non-Current       XX      XX      XX      XX      XX      XX      XX      XX      XX

TOTAL ASSETS            XX      XX      XX      XX      XX      XX      XX      XX      XX

LIABILITIES
Current Liabilities:
  Accounts Payable      XX      XX      XX      XX      XX      XX      XX      XX      XX
  Accrued expenses      XX      XX      XX      XX      XX      XX      XX      XX      XX
  Deferred revenue      XX      XX      XX      XX      XX      XX      XX      XX      XX
  Current debt          XX      XX      XX      XX      XX      XX      XX      XX      XX
  Other current liab.   XX      XX      XX      XX      XX      XX      XX      XX      XX
Total Current Liab.     XX      XX      XX      XX      XX      XX      XX      XX      XX

Non-Current Liabilities:
  Long-term debt        XX      XX      XX      XX      XX      XX      XX      XX      XX
  Deferred taxes        XX      XX      XX      XX      XX      XX      XX      XX      XX
  Other non-current     XX      XX      XX      XX      XX      XX      XX      XX      XX
Total Non-Current Liab. XX      XX      XX      XX      XX      XX      XX      XX      XX

TOTAL LIABILITIES       XX      XX      XX      XX      XX      XX      XX      XX      XX

EQUITY
  Common stock          XX      XX      XX      XX      XX      XX      XX      XX      XX
  Additional paid-in    XX      XX      XX      XX      XX      XX      XX      XX      XX
  Retained earnings     XX      XX      XX      XX      XX      XX      XX      XX      XX
  Treasury stock        (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)    (XX)
  Other equity          XX      XX      XX      XX      XX      XX      XX      XX      XX
TOTAL EQUITY            XX      XX      XX      XX      XX      XX      XX      XX      XX

TOTAL LIAB + EQUITY     XX      XX      XX      XX      XX      XX      XX      XX      XX

BALANCE CHECK           OK      OK      OK      OK      OK      OK      OK      OK      OK
```

**Balance Check Formula:**
- Total Assets must equal Total Liabilities + Equity for each year
- Flag any imbalances in red

### Step 7: Build DCF Inputs Tab

Prepare inputs for valuation (Task 3):

```
DCF INPUTS              2025E   2026E   2027E   2028E   2029E

EBIT                    XX      XX      XX      XX      XX
Tax Rate                X%      X%      X%      X%      X%
NOPAT                   XX      XX      XX      XX      XX

Add: D&A                XX      XX      XX      XX      XX
Less: CapEx             (XX)    (XX)    (XX)    (XX)    (XX)
Less: Chg in NWC        (XX)    (XX)    (XX)    (XX)    (XX)

UNLEVERED FCF           XX      XX      XX      XX      XX

Terminal Year Metrics:
  2029E Revenue         $X,XXX
  2029E EBITDA          $XXX
  2029E EBIT            $XXX
  2029E Unlevered FCF   $XXX
```

### Step 8: Build Scenarios Tab

Create three scenarios with different assumptions:

#### Scenario Assumptions Table
```
Assumption                      Bull        Base        Bear
Revenue CAGR (2025-2029)        XX%         XX%         XX%
Gross Margin 2029E              XX%         XX%         XX%
EBITDA Margin 2029E             XX%         XX%         XX%
CapEx as % of Revenue           X%          X%          X%
[Add other key assumptions]
```

#### Scenario Output Table
```
Metric                          Bull        Base        Bear
2029E Revenue ($M)              $X,XXX      $X,XXX      $X,XXX
2029E EBITDA ($M)               $XXX        $XXX        $XXX
2029E EBITDA Margin             XX%         XX%         XX%
2029E Net Income ($M)           $XXX        $XXX        $XXX
2029E EPS                       $X.XX       $X.XX       $X.XX
2029E FCF ($M)                  $XXX        $XXX        $XXX
2029E FCF Margin                XX%         XX%         XX%

Cumulative FCF 2025-2029 ($M)   $XXX        $XXX        $XXX
```

**Document scenario rationale:**
- Bull case: [Describe optimistic but achievable assumptions]
- Base case: [Describe most likely scenario]
- Bear case: [Describe downside risks and triggers]

### Step 9: Quality Check

**Verify model integrity:**
1. [ ] Test all formulas (spot check calculations)
2. [ ] Change assumption → verify model updates correctly
3. [ ] Test scenario switching
4. [ ] Verify color coding (blue/black/green)
5. [ ] Check balance sheet balances for all years
6. [ ] Verify no circular references (Excel will flag)
7. [ ] Check for hardcoded numbers in projections
8. [ ] Verify all cross-sheet links work
9. [ ] Test that revenue totals tie across all tabs
10. [ ] Review formatting and presentation

---

## Quality Standards

### Model Integrity
- All formulas link properly across sheets
- No hardcoded numbers in projections (except in Assumptions tab)
- No circular references
- Balance sheet balances for all years
- Scenario switching works properly

### Completeness
- All 6 essential tabs: Revenue Model, Income Statement, Cash Flow Statement, Balance Sheet, Scenarios, DCF Inputs
- 40-50 line items in Income Statement
- 20-30 rows in Revenue Model (product breakdown)
- 15-20 rows in Revenue Model (geography breakdown)
- Full cash flow and balance sheet with all line items
- Bull/Base/Bear scenarios complete

### Professional Formatting
- Consistent color coding (blue/black/green)
- Clear headers and labels
- Proper borders and shading
- Named ranges for key cells
- Grouped rows for collapsibility
- Units clearly labeled ($ thousands vs. $ millions)

### Documentation
- Assumptions documented with rationale (blue text cells with comments)
- Data sources noted in cell comments or notes section within tabs
- Complex calculations explained with comments
- Methodology described

---

## File Naming Convention

Save the financial model as:
`[Company]_Financial_Model_[Date].xlsx`

Example: `Tesla_Financial_Model_2024-10-27.xlsx`

---

## Success Criteria

A successful financial model should:
1. Have all 6 essential tabs (Revenue Model, Income Statement, Cash Flow Statement, Balance Sheet, Scenarios, DCF Inputs)
2. Be fully dynamic (change assumption → model updates)
3. Have no hardcoded numbers in projections
4. Include detailed revenue breakdowns (20-30 rows by product, 15-20 rows by geography)
5. Contain 40-50 line items in Income Statement
6. Include Bull/Base/Bear scenarios
7. Be professionally formatted with color coding
8. Balance properly (balance sheet, cash flows)
9. Be auditable and easy to follow
10. Support valuation analysis with proper FCF calculations

---

## Common Model Types - Special Considerations

### High-Growth Tech/SaaS
- Focus on ARR growth and net retention
- Model by product line and geography
- Heavy R&D and S&M spend
- Path to profitability timeline
- Unit economics (LTV/CAC)

### E-commerce/Retail
- Revenue by product category and channel
- Store count and comp store growth (if applicable)
- Inventory turns and working capital
- Fulfillment costs
- Customer acquisition

### Manufacturing/Industrial
- Production capacity utilization
- Raw material costs and pricing
- Gross margin bridge (volume/price/mix/cost)
- CapEx heavy models
- Working capital cycles

---

## Next Steps

After completing Task 2, the financial model will be used for:
- **Task 3 (Valuation)**: DCF inputs, projected financials
- **Task 4 (Charts)**: Data for revenue trends, margin charts, scenario comparisons
- **Task 5 (Report Assembly)**: Financial data for report tables and analysis

### Referencia: references/task3-valuation.md

# Task 3: Valuation Analysis - Detailed Workflow

This document provides step-by-step instructions for executing Task 3 (Valuation Analysis) of the initiating-coverage skill.

## Task Overview

**Purpose**: Perform comprehensive valuation using DCF, comparables, and precedent transactions.

**Prerequisites**: ⚠️ Verify before starting
- **Required**: Financial model from Task 2
  - Projected income statements
  - Projected cash flows
  - Revenue and EBITDA forecasts
  - DCF inputs (unlevered FCF)

**⚠️ CRITICAL: DO NOT START THIS TASK UNLESS TASK 2 IS COMPLETE**

This task requires the financial model from Task 2. Starting without it will result in incomplete work.

**IF TASK 2 IS NOT COMPLETE**: Stop immediately and inform the user that Task 2 (Financial Modeling) must be completed first. Do not attempt to proceed or create placeholder valuations.

**Output**: Valuation Analysis (4-6 pages + Excel tabs)
- DCF analysis with sensitivity tables
- Comparable companies analysis
- Precedent transactions (if applicable)
- Valuation football field
- Price target and recommendation

---

## Input Verification

**BEFORE STARTING - CHECK:**
- [ ] Task 2 complete? (Financial model exists)
- [ ] Model file path/location known?
- [ ] Can access projected financials from model?

**Required from model:**
- [ ] Projected FCF (5 years)
- [ ] Revenue projections
- [ ] EBITDA projections
- [ ] Terminal year metrics
- [ ] Balance sheet data (debt, cash, shares)

**IF VERIFICATION FAILS**: Stop and complete Task 2 (Financial Modeling) before proceeding.

---

## Detailed Methodology Reference

For deep dive on valuation methodologies, formulas, and theory, see:
**[valuation-methodologies.md](valuation-methodologies.md)**

This workflow document focuses on execution steps. Reference the methodology file for:
- DCF theory and formulas
- WACC calculation details
- Terminal value methods
- Comparable companies theory
- Precedent transactions theory

---

## Step-by-Step Valuation Workflow

### Step 1: Extract Data from Financial Model

**From Task 2's financial model, extract:**

1. **Projected Financials (5 years)**
   - Revenue by year (2025E-2029E)
   - EBITDA by year
   - EBIT by year
   - Tax rate
   - D&A by year
   - CapEx by year
   - Change in NWC by year

2. **Unlevered Free Cash Flow**
   ```
   Extract from DCF Inputs tab in financial model:

                   2025E   2026E   2027E   2028E   2029E
   EBIT            $XXX    $XXX    $XXX    $XXX    $XXX
   × (1 - Tax Rate)
   = NOPAT         $XXX    $XXX    $XXX    $XXX    $XXX
   + D&A           $XXX    $XXX    $XXX    $XXX    $XXX
   - CapEx         ($XX)   ($XX)   ($XX)   ($XX)   ($XX)
   - Chg in NWC    ($XX)   ($XX)   ($XX)   ($XX)   ($XX)
   = Unlevered FCF $XXX    $XXX    $XXX    $XXX    $XXX
   ```

3. **Balance Sheet Data (current)**
   - Total debt
   - Cash & equivalents
   - Net debt (Debt - Cash)
   - Diluted shares outstanding

4. **Scenario Data**
   - Bull case revenue CAGR and terminal margin
   - Base case revenue CAGR and terminal margin
   - Bear case revenue CAGR and terminal margin

### Step 2: Build DCF Analysis

#### A. Calculate WACC

**1. Determine Risk-Free Rate**
   - Use 10-year Treasury yield (check current rate)
   - Example: 4.0-4.5% as of late 2024

**2. Determine Cost of Equity (CAPM)**
   ```
   Cost of Equity = Risk-Free Rate + Beta × Equity Risk Premium

   Inputs:
   - Risk-Free Rate: [Current 10-year Treasury, e.g., 4.2%]
   - Beta: [Company beta from Bloomberg/FactSet or peer average]
   - Equity Risk Premium: 5-6% (historical average)

   Example:
   Cost of Equity = 4.2% + 1.3 × 5.5% = 11.35%
   ```

**3. Determine Cost of Debt**
   ```
   Cost of Debt = Current borrowing rate or implied yield on bonds

   For private companies:
   Cost of Debt = Risk-Free Rate + Credit Spread (based on rating)

   Example:
   Cost of Debt (pre-tax) = 6.5%
   Cost of Debt (after-tax) = 6.5% × (1 - 25% tax rate) = 4.875%
   ```

**4. Determine Capital Structure**
   ```
   Use market values (not book values):

   Market Value of Equity (E) = Share Price × Shares Outstanding
   Market Value of Debt (D) = Total Debt (use book value if bonds not traded)
   Total Value (V) = E + D

   Weight of Equity = E / V
   Weight of Debt = D / V

   Example:
   E = $5,000M (90.9%)
   D = $500M (9.1%)
   V = $5,500M (100%)
   ```

**5. Calculate WACC**
   ```
   WACC = (E/V × Cost of Equity) + (D/V × Cost of Debt × (1 - Tax Rate))

   Example:
   WACC = (90.9% × 11.35%) + (9.1% × 6.5% × (1 - 25%))
   WACC = 10.32% + 0.44% = 10.76%

   Round to: 10.8% for base case
   ```

#### B. Calculate Terminal Value

**Method 1: Perpetuity Growth (Preferred)**
```
Terminal Value = FCF(2029) × (1 + g) / (WACC - g)

Where:
- FCF(2029) = Final year unlevered FCF from model
- g = Perpetual growth rate (typically 2.0-3.0%)
  - Should not exceed long-term GDP growth
  - Use 2.5% as base case

Example:
FCF(2029) = $500M
g = 2.5%
WACC = 10.8%

Terminal Value = $500M × (1.025) / (0.108 - 0.025)
Terminal Value = $512.5M / 0.083 = $6,175M
```

**Method 2: Exit Multiple (Alternative)**
```
Terminal Value = EBITDA(2029) × Exit Multiple

Where:
- Exit Multiple = Current peer trading median (e.g., 12-15x EBITDA)

Example:
EBITDA(2029) = $800M
Exit Multiple = 13x

Terminal Value = $800M × 13x = $10,400M
```

**Choose one method or average both.**

#### C. Discount Cash Flows to Present Value

```
PV of Projected FCF = Σ [FCFt / (1 + WACC)^t] for t = 1 to 5

Example:
Year    FCF      Discount    PV of FCF
        ($M)     Factor      ($M)
2025    $250     1/(1.108)^1 = 0.9026    $226
2026    $320     1/(1.108)^2 = 0.8147    $261
2027    $390     1/(1.108)^3 = 0.7353    $287
2028    $450     1/(1.108)^4 = 0.6636    $299
2029    $500     1/(1.108)^5 = 0.5988    $299
                              Total PV:  $1,372M

PV of Terminal Value = Terminal Value / (1 + WACC)^5
PV of Terminal Value = $6,175M / (1.108)^5 = $6,175M × 0.5988 = $3,697M

Enterprise Value = $1,372M + $3,697M = $5,069M
```

#### D. Calculate Equity Value and Price Per Share

```
Enterprise Value                 $5,069M
- Net Debt (Debt - Cash)         ($450M)
+ Non-operating Assets           $0M
- Minority Interest              $0M
- Preferred Stock                $0M
= Equity Value                   $4,619M

Diluted Shares Outstanding       100M

Price Per Share = $4,619M / 100M = $46.19

Current Stock Price: $42.00
Implied Upside: 10.0%
```

#### E. DCF Sensitivity Analysis **CRITICAL**

**Table 1: WACC vs. Terminal Growth Rate**

Create 2-way sensitivity table:
```
Price Per Share ($)     Terminal Growth Rate
WACC        1.5%    2.0%    2.5%    3.0%    3.5%
9.0%        $52     $55     $59     $63     $68
9.5%        $48     $51     $54     $58     $62
10.0%       $45     $48     $51     $54     $57
10.5%       $42     $45     $47     $50     $53
11.0%       $40     $42     $44     $47     $50
11.5%       $38     $40     $42     $44     $47
12.0%       $36     $38     $40     $42     $44

Base Case: WACC = 10.8%, g = 2.5% → $46
Format as heatmap: Green (high values) → Yellow → Red (low values)
```

**Table 2: Revenue CAGR vs. Terminal EBITDA Margin**
```
Price Per Share ($)     Terminal EBITDA Margin (2029E)
Revenue CAGR    28%     30%     32%     34%     36%
15%             $38     $42     $46     $50     $54
20%             $42     $46     $51     $56     $61
25%             $46     $51     $56     $62     $68
30%             $51     $56     $62     $68     $75
35%             $56     $62     $68     $75     $83

Base Case: Rev CAGR = 25%, EBITDA Margin = 32% → $56
```

### Step 3: Comparable Companies Analysis

#### A. Select Comparable Companies

**Selection Criteria:**
- Same industry/sector (primary requirement)
- Similar business model
- Comparable size (market cap, revenue)
- Similar growth profile
- Similar geographies

**Identify 5-10 peer companies:**
1. [Peer 1] - Direct competitor
2. [Peer 2] - Direct competitor
3. [Peer 3] - Adjacent player
4. [Peer 4] - Similar business model
5. [Peer 5] - Regional competitor
6. [Add 3-5 more]

**Document rationale for each peer selected.**

#### B. Gather Peer Financial Data

**For each comparable, gather:**
- Current stock price
- Shares outstanding (diluted)
- Market capitalization
- Total debt and cash (for EV calculation)
- Enterprise value
- LTM (Last Twelve Months) financials:
  - Revenue
  - EBITDA
  - EBIT
  - Net Income
- NTM (Next Twelve Months) consensus estimates
- Revenue growth rate
- EBITDA margin

**Data sources:**
- FactSet, CapitalIQ, Bloomberg (preferred)
- Company 10-Ks/10-Qs for actuals
- Consensus estimates from Yahoo Finance, Seeking Alpha (if pro tools unavailable)

#### C. Calculate Valuation Multiples

**For each peer, calculate:**
```
EV/Revenue (LTM) = Enterprise Value / LTM Revenue
EV/Revenue (NTM) = Enterprise Value / NTM Revenue (est.)
EV/EBITDA (LTM) = Enterprise Value / LTM EBITDA
EV/EBITDA (NTM) = Enterprise Value / NTM EBITDA (est.)
P/E (NTM) = Market Cap / NTM Net Income (est.)
```

#### D. Create Comparable Companies Table (MANDATORY FORMAT)

```
COMPARABLE COMPANIES ANALYSIS

Company      Ticker  Mkt Cap  EV/Rev  EV/Rev  EV/EBITDA  EV/EBITDA  P/E   Rev     EBITDA
                     ($B)     LTM     NTM     LTM        NTM        NTM   Growth  Margin
Peer A       PRA     45.2     3.5x    3.2x    15.2x      13.8x      25x   18%     23%
Peer B       PRB     32.8     3.2x    2.9x    14.1x      12.5x      22x   15%     23%
Peer C       PRC     28.5     2.8x    2.6x    12.8x      11.2x      20x   12%     22%
Peer D       PRD     52.1     4.1x    3.7x    17.5x      15.2x      29x   22%     23%
Peer E       PRE     38.9     3.6x    3.3x    15.8x      14.1x      25x   17%     23%
Peer F       PRF     41.2     3.7x    3.4x    16.1x      13.9x      26x   19%     23%
Peer G       PRG     35.5     3.3x    3.0x    14.5x      12.8x      23x   16%     22%

[Target]     TRGT    38.0     3.4x    3.1x    14.8x      13.0x      24x   17%     23%

STATISTICAL SUMMARY
Maximum              52.1     4.1x    3.7x    17.5x      15.2x      29x   22%     23%
75th Percentile      45.2     3.7x    3.4x    16.1x      14.1x      26x   19%     23%
Median               38.9     3.5x    3.2x    15.2x      13.8x      25x   17%     23%
25th Percentile      32.8     3.2x    2.9x    14.1x      12.5x      22x   15%     22%
Minimum              28.5     2.8x    2.6x    12.8x      11.2x      20x   12%     22%

Note: Market data as of [Date]. LTM = Last Twelve Months. NTM = Next Twelve Months.
Source: FactSet, company filings, [Analyst] estimates.
```

**CRITICAL**: The statistical summary (max/75th/median/25th/min) is MANDATORY.

#### E. Apply Multiples to Target Company

**Choose primary multiple (typically EV/EBITDA for mature companies):**

```
Target Company NTM EBITDA = $550M (from financial model)

Apply Median Peer Multiple:
Peer Median EV/EBITDA (NTM) = 13.8x
Implied EV = $550M × 13.8x = $7,590M

Apply 25th Percentile (Conservative):
25th Percentile EV/EBITDA (NTM) = 12.5x
Implied EV = $550M × 12.5x = $6,875M

Apply 75th Percentile (Optimistic):
75th Percentile EV/EBITDA (NTM) = 14.1x
Implied EV = $550M × 14.1x = $7,755M

Valuation Range (Comps): $6,875M - $7,755M
Midpoint: $7,315M

Convert to Equity Value:
Implied EV (Median)        $7,590M
- Net Debt                 ($450M)
= Implied Equity Value     $7,140M

Shares Outstanding         100M
Implied Price/Share        $71.40
```

**Justify Premium/Discount:**
- Target is growing 17% vs. peer median 17% → In-line
- Target EBITDA margin 23% vs. peer median 23% → In-line
- Target market position → [Justify premium/discount]
- **Conclusion**: Apply median multiple (no adjustment)

### Step 4: Precedent Transactions (Optional)

**Note**: Only if M&A is relevant for this sector/company.

#### A. Identify Relevant Transactions

**Search for 5-10 M&A deals:**
- Same industry, last 3-5 years
- Similar size (0.5x to 2x target's size)
- Announced and closed deals

**Example:**
```
PRECEDENT TRANSACTIONS ANALYSIS

Date     Target        Acquirer      Deal     EV/Rev  EV/EBITDA  Premium  Rationale
                                    Value($B)  LTM     LTM
Q1 2024  Comp A       Strategic      $5.2B    4.2x    16.5x      35%      Consolidation
Q3 2023  Comp B       PE Firm        $3.8B    3.8x    14.2x      28%      Platform
Q4 2023  Comp C       Strategic      $4.5B    4.0x    15.8x      32%      Geographic
Q2 2023  Comp D       Strategic      $6.1B    4.5x    17.2x      38%      Strategic fit
Q1 2023  Comp E       PE Firm        $3.2B    3.5x    13.5x      25%      Carve-out

Median                                        4.0x    15.8x      32%

Source: CapitalIQ, company filings, press releases.
```

#### B. Apply to Target Company

```
Target Company LTM EBITDA = $500M
Precedent Median EV/EBITDA (LTM) = 15.8x

Implied EV (Precedent) = $500M × 15.8x = $7,900M

Note: Precedent multiples typically 10-20% higher than trading comps
due to control premium and synergies.
```

### Step 5: Valuation Reconciliation

#### A. Create Valuation Summary Table

```
VALUATION SUMMARY

Method                  Low     Base    High    Weight  Weighted Value
DCF Analysis            $42     $46     $51     50%     $23.00
Trading Comps (NTM)     $64     $71     $78     40%     $28.40
Precedent Trans.        $70     $79     $88     10%     $7.90
                                                        -------
Weighted Average Target                         100%    $59.30

Rounded Price Target: $59.00

Current Price (as of [Date]):    $42.00
Upside to Target:                40% ($59.00 / $42.00 - 1)
```

#### B. Determine Weighting Rationale

**Typical Weighting:**
- DCF: 40-60% (higher when forecasts reliable)
- Trading Comps: 25-40% (reflects market sentiment)
- Precedent Trans: 10-25% (lower unless M&A likely)

**For this example:**
- DCF 50%: High confidence in projections
- Comps 40%: Robust peer set
- Precedent 10%: M&A unlikely near-term

#### C. Create Valuation Football Field Chart

```
VALUATION FOOTBALL FIELD

Method                  Low ◄────────── Range ──────────► High

DCF Analysis            $42 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ $51

Trading Comps (NTM)     $64 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ $78

Precedent Trans.        $70 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ $88
                                          ↑
                                    Current: $42
─────────────────────────────────────────────────────────
Valuation Range         $42                          $88
Price Target: $59 (weighted average)

Color code:
- DCF: Blue
- Trading Comps: Green
- Precedent Trans: Orange
- Vertical line at current price: Red dashed
- Vertical line at target: Black solid
```

#### D. Scenario-Based Valuations

```
VALUATION BY SCENARIO

Scenario    Probability  Revenue  EBITDA    DCF      Comps    Weighted
                        CAGR     Margin    Value    Multiple  Avg
Bear Case   20%         18%      28%       $38      11.5x     $42
Base Case   60%         25%      32%       $46      13.8x     $59
Bull Case   20%         32%      36%       $58      16.0x     $82

Expected Value (probability-weighted): $59
```

### Step 6: Final Price Target & Recommendation

```
═══════════════════════════════════════════════════════════
INVESTMENT RECOMMENDATION
═══════════════════════════════════════════════════════════

Current Price:          $42.00 (as of [Date])
Price Target:           $59.00 (12-month)
Upside/(Downside):      +40.5%

Rating:                 BUY / OUTPERFORM

Valuation Methodology:  Based on weighted average of DCF (50%),
                       trading comparables (40%), and precedent
                       transactions (10%).

Time Horizon:          12 months

───────────────────────────────────────────────────────────
KEY INVESTMENT CATALYSTS
───────────────────────────────────────────────────────────

1. New Product Launch (Q2 2025)
   - Expected to drive 15-20% revenue acceleration
   - Already seeing strong pre-orders

2. Margin Expansion (FY2025-2026)
   - Operating leverage from scale
   - Path to 35% EBITDA margin (from current 28%)

3. Market Share Gains (Ongoing)
   - Taking share from legacy competitors
   - Net Promoter Score improvement

4. International Expansion (H2 2025)
   - Entry into European markets
   - Potential $200M incremental revenue opportunity

5. Potential M&A Target (12-18 months)
   - Strategic fit for larger players
   - Precedent transactions suggest 30-40% premium

───────────────────────────────────────────────────────────
KEY RISKS TO PRICE TARGET
───────────────────────────────────────────────────────────

Downside Risks:
1. Competitive Pressure (High probability, -15% impact)
   - New entrant launched competing product
   - Could pressure pricing and market share

2. Execution Risk (Medium probability, -10% impact)
   - New product launch delays or underperformance
   - Management turnover

3. Macro Slowdown (Medium probability, -20% impact)
   - Economic recession would impact customer spending
   - Operating leverage would reverse

4. Regulatory Risk (Low probability, -25% impact)
   - Potential new regulations in key market
   - Would increase compliance costs

Upside Risks:
1. M&A Bid (Low probability, +35% impact)
   - Strategic acquirer pays control premium

2. Beat-and-Raise (Medium probability, +10% impact)
   - Consistent outperformance vs. estimates

═══════════════════════════════════════════════════════════
```

---

## Quality Standards

### DCF Quality Checks
- [ ] WACC properly calculated with documented components
- [ ] Terminal value reasonable (< 70% of total enterprise value)
- [ ] Sensitivity analysis covers realistic ranges (±200-300bps for WACC, ±100bps for terminal growth)
- [ ] Unlevered FCF properly calculated from EBIT
- [ ] Enterprise to equity value bridge correct
- [ ] Share count is diluted shares, not basic

### Comparables Quality Checks
- [ ] 5-10 comparable companies selected
- [ ] Peer selection defensible (document why each peer was chosen)
- [ ] Statistical summary included (max/75th/median/25th/min) - MANDATORY
- [ ] Multiple selection appropriate (EV/EBITDA for mature, EV/Revenue for high-growth)
- [ ] Premium/discount justified with specific factors
- [ ] Data sourced properly with dates noted

### Overall Valuation Quality Checks
- [ ] At least 2 valuation methods used (DCF + Comps minimum)
- [ ] Weighting explained and appropriate
- [ ] Valuation range provided (low/base/high), not just point estimate
- [ ] Scenarios analyzed (Bull/Base/Bear)
- [ ] Sanity checks performed (see below)
- [ ] All assumptions documented with rationale

---

## Sanity Checks

**Always perform these validation checks:**

1. **Historical Multiple Check**
   - Is implied multiple in line with company's historical trading range?
   - If not, explain why

2. **Peer Comparison**
   - Is premium/discount vs. peers justified by fundamentals?
   - Check: growth, margins, market position

3. **Implied Growth Check**
   - What growth is market pricing in at current price?
   - Is that reasonable given company trajectory?

4. **Market Cap Reasonableness**
   - Does total market cap make sense given company size and peers?
   - Would company be too large/small relative to industry?

5. **Terminal Value Check**
   - Is terminal value < 60-70% of total enterprise value?
   - If > 70%, projections may not be long enough

6. **WACC Reasonableness**
   - Is WACC 8-14% range for typical companies?
   - Tech/high-growth: 10-14%
   - Mature/stable: 7-10%

7. **Implied Returns Check**
   - What IRR from current price to target over 12 months?
   - Is that consistent with recommendation rating?

---

## Output Files

Create the following deliverables:

### 1. Valuation Analysis Document
**File**: `[Company]_Valuation_Analysis_[Date].md` (written analysis)

**Contents** (4-6 pages):
- Executive summary with price target
- DCF analysis (1 page) with sensitivity table
- Comparable companies analysis (1 page) with statistical summary
- Precedent transactions (0.5 page) if applicable
- Valuation summary and football field (0.5 page)
- Investment recommendation (1 page)
- Key catalysts and risks (1 page)

### 2. Excel Valuation Tabs
**Add to Task 2's financial model file:** `[Company]_Financial_Model_[Date].xlsx`

**IMPORTANT**: Do NOT create a separate Excel file. Add these tabs to the existing financial model from Task 2. This keeps all quantitative data in one place.

**Tabs to add:**
- DCF tab with full calculations
- Sensitivity analysis tab
- Comps tab with peer data
- Precedent transactions tab (if applicable)
- Valuation summary tab

---

## Success Criteria

A successful valuation analysis should:
1. Use at least 2 methods (DCF + Comps minimum)
2. Include comprehensive DCF sensitivity analysis (2-way tables)
3. Include statistical summary in comps (max/75th/median/25th/min)
4. Provide valuation range (low/base/high), not point estimate
5. Document all key assumptions with clear rationale
6. Perform sanity checks
7. Arrive at defensible price target
8. Provide clear buy/hold/sell recommendation
9. Identify 3-5 key catalysts
10. Identify 3-5 key risks
11. Be auditable and transparent

---

## Next Steps

After completing Task 3, the valuation analysis will be used for:
- **Task 4 (Charts)**: Create DCF sensitivity heatmaps, valuation football field, scenario comparison charts
- **Task 5 (Report Assembly)**: Integrate valuation analysis into final report

The price target and recommendation are the foundation of the final investment recommendation in the equity research report.

### Referencia: references/task4-chart-generation.md

# Task 4: Chart Generation - Detailed Workflow

This document provides step-by-step instructions for executing Task 4 (Chart Generation) of the initiating-coverage skill.

## Task Overview

**Purpose**: Generate 25-35 professional financial charts for the report.

**Prerequisites**: ⚠️ Verify before starting
- **Required**: Company research from Task 1
  - Company history, milestones (for timeline charts)
  - Management team, org structure (for org charts)
  - Product portfolio (for product charts)
  - Customer segmentation (for customer charts)
  - Competitive landscape (for competitive positioning charts)
  - TAM analysis (for market size charts)
- **Required**: Financial model from Task 2
  - Revenue by product/geography data
  - Margin trends
  - Scenario comparison data
- **Required**: Valuation analysis from Task 3
  - DCF sensitivity table
  - Comparable companies data
  - Valuation ranges
- **Required**: External market data
  - Historical stock price data (Yahoo Finance, Bloomberg)
  - Historical valuation multiples (optional for chart 34)

**⚠️ CRITICAL: DO NOT START THIS TASK UNLESS TASKS 1, 2, AND 3 ARE COMPLETE**

This task requires outputs from all three previous tasks. Starting without them will result in incomplete charts.

**IF ANY OF TASKS 1, 2, OR 3 ARE NOT COMPLETE**: Stop immediately and inform the user which tasks need to be completed first. The specific requirements are:
- Task 1: Company research document (for 9 charts)
- Task 2: Financial model with all 6 tabs (for 8 charts)
- Task 3: Valuation tabs added to the model (for 6 charts)
- External data access (for 2 charts)

Do not attempt to create placeholder charts or skip charts due to missing data.

**Output**: 25-35 Professional Chart Files (PNG/JPG, 300 DPI)

---

## Input Verification

**BEFORE STARTING - CHECK ALL PREREQUISITES:**

### Task 1 Verification (Company Research)
- [ ] Task 1 complete? (Company research document exists)
- [ ] Company history and milestones documented? (for charts 05, 06)
- [ ] Management team and org structure described? (for chart 07)
- [ ] Product portfolio detailed? (for chart 08)
- [ ] Customer segmentation analyzed? (for chart 09)
- [ ] Competitive landscape mapped? (for charts 16, 17, 18)
- [ ] TAM sizing completed? (for chart 15)

### Task 2 Verification (Financial Model)
- [ ] Task 2 complete? (Financial model Excel file exists)
- [ ] Revenue by product breakdown available? (for chart 03 ⭐)
- [ ] Revenue by geography breakdown available? (for chart 04 ⭐)
- [ ] Historical + projected financials complete? (for charts 02, 10, 11, 12)
- [ ] Scenario analysis (Bull/Base/Bear) complete? (for chart 14)
- [ ] Operating metrics available? (for chart 13)

### Task 3 Verification (Valuation)
- [ ] Task 3 complete? (Valuation tabs added to model)
- [ ] DCF sensitivity matrix exists? (for chart 28 ⭐)
- [ ] DCF calculation details available? (for chart 29)
- [ ] Comparable companies data collected? (for charts 30, 31)
- [ ] Valuation ranges calculated? (for chart 32 ⭐)

### External Data Verification
- [ ] Can access historical stock price data? (Yahoo Finance, Bloomberg for chart 01)
- [ ] Can access historical valuation data? (Optional, for chart 34)

**IF ANY VERIFICATION FAILS**:
- Missing Task 1? → Complete Task 1 (Company Research) first
- Missing Task 2? → Complete Task 2 (Financial Modeling) first
- Missing Task 3? → Complete Task 3 (Valuation Analysis) first
- Missing external data? → Gather from Yahoo Finance, Bloomberg, or similar sources

---

## Chart Requirements: 25 Required + 10 Optional

**IMPORTANT**: Task 5 (Report Assembly) will embed **ALL charts created** throughout the report. The report requires dense visual content (1 chart every 200-300 words), so create comprehensive chart coverage.

### 4 MANDATORY Charts (Non-Negotiable) ⭐

These 4 charts are critical visualizations that MUST be present:

1. **chart_03**: Revenue by Product/Segment - Stacked Area Chart ⭐
2. **chart_04**: Revenue by Geography - Stacked Bar Chart ⭐
3. **chart_28**: DCF Sensitivity Analysis - 2-Way Heatmap ⭐
4. **chart_32**: Valuation Football Field - Horizontal Bar Chart ⭐

### 25 REQUIRED Charts (Complete Set)

Create all 25 of these charts. Each has a specific purpose in Task 5:

**Investment Summary Section (1 chart):**
- chart_01: Stock Price Performance (12-24 months)

**Financial Performance Section (6 charts):**
- chart_02: Revenue Growth Trajectory
- chart_03: Revenue by Product - Stacked Area ⭐ MANDATORY
- chart_04: Revenue by Geography - Stacked Bar ⭐ MANDATORY
- chart_10: Gross Margin Evolution
- chart_11: EBITDA Margin Progression
- chart_12: Free Cash Flow Trend

**Company 101 Section (7 charts):**
- chart_05: Company Overview/Timeline
- chart_06: Key Milestones Timeline
- chart_07: Organizational Structure
- chart_08: Product Portfolio Overview
- chart_09: Customer Segmentation
- chart_15: Market Size Evolution (TAM)
- chart_16: Competitive Positioning Matrix

**Competitive & Market Section (2 charts):**
- chart_17: Market Share Breakdown
- chart_18: Competitive Benchmarking

**Scenario Analysis Section (2 charts):**
- chart_13: Operating Metrics Dashboard
- chart_14: Scenario Comparison (Bull/Base/Bear)

**Valuation Section (7 charts):**
- chart_28: DCF Sensitivity Heatmap ⭐ MANDATORY
- chart_29: DCF Valuation Waterfall
- chart_30: Trading Comps Scatter Plot
- chart_31: Peer Multiples Comparison
- chart_32: Valuation Football Field ⭐ MANDATORY
- chart_33: Price Target Scenarios
- chart_34: Historical Valuation Multiples

**Total: 25 Required Charts**

### 10 OPTIONAL Charts (For 30-35 Range)

Add these for greater visual density and storytelling (reach 26-35 total):

- chart_19: Customer Acquisition Trends
- chart_20: Unit Economics Evolution
- chart_21: Product Roadmap Timeline
- chart_22: Geographic Expansion Map
- chart_23: R&D Investment Trends
- chart_24: Sales & Marketing Efficiency
- chart_25: Working Capital Trends
- chart_26: Debt Maturity Schedule
- chart_27: Ownership Structure
- chart_35: Analyst Price Target Distribution

**Total Range: 25-35 Charts (25 required + 0-10 optional)**

---

## Data Source Mapping for Required Charts

Understanding where each chart's data comes from:

### From Task 1 (Company Research) - 9 charts
- chart_05: Company Overview → Task 1: Company Overview section
- chart_06: Key Milestones → Task 1: Company History section
- chart_07: Org Structure → Task 1: Management Team section
- chart_08: Product Portfolio → Task 1: Products & Services section
- chart_09: Customer Segmentation → Task 1: Customers & Go-to-Market section
- chart_15: Market Size Evolution → Task 1: Market Opportunity (TAM) section
- chart_16: Competitive Positioning → Task 1: Competitive Landscape section
- chart_17: Market Share → Task 1: Competitive Landscape section
- chart_18: Competitive Benchmarking → Task 1: Competitive Landscape section

### From Task 2 (Financial Model) - 8 charts
- chart_02: Revenue Growth → Income Statement tab (Revenue row)
- chart_03: Revenue by Product ⭐ → Revenue Model tab (Product breakdown)
- chart_04: Revenue by Geography ⭐ → Revenue Model tab (Geography breakdown)
- chart_10: Gross Margin → Income Statement tab (Gross Profit / Revenue)
- chart_11: EBITDA Margin → Income Statement tab (EBITDA / Revenue)
- chart_12: Free Cash Flow → Cash Flow Statement tab (CFO - CapEx)
- chart_13: Operating Metrics → Multiple tabs (Income Statement, Cash Flow)
- chart_14: Scenario Comparison → Scenarios tab (Bull/Base/Bear)

### From Task 3 (Valuation) - 6 charts
- chart_28: DCF Sensitivity ⭐ → Sensitivity Analysis tab
- chart_29: DCF Waterfall → DCF tab (Enterprise Value components)
- chart_30: Trading Comps Scatter → Comparable Companies tab
- chart_31: Peer Multiples → Comparable Companies tab
- chart_32: Valuation Football Field ⭐ → Valuation Summary tab
- chart_33: Price Target Scenarios → Valuation Summary tab (or calculate from scenarios)

### From External Sources - 2 charts
- chart_01: Stock Price Performance → Yahoo Finance, Bloomberg, Alpha Vantage
- chart_34: Historical Valuation Multiples → Yahoo Finance, Bloomberg (historical P/E, EV/EBITDA)

**IMPORTANT**: Require ALL three tasks (1, 2, 3) complete PLUS external data access to create all 25 required charts.

---

## Step-by-Step Chart Generation Workflow

### Step 1: Set Up Environment

**Install required libraries:**
```bash
pip install matplotlib seaborn pandas numpy plotly
```

**Create Python script header:**
```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')

# Set global style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Global settings
DPI = 300
FIGURE_WIDTH = 10
FIGURE_HEIGHT = 6
TITLE_FONT_SIZE = 14
AXIS_FONT_SIZE = 12
LABEL_FONT_SIZE = 10
```

### Step 2: Extract Data from Model and Valuation

#### A. Extract Revenue Data
```python
# Revenue by Product (from Task 2 model)
years = [2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029]

# Extract from Excel or define manually from model
product_a = [100, 120, 145, 175, 210, 252, 302, 363, 435, 522]
product_b = [80, 95, 115, 138, 165, 198, 238, 285, 342, 411]
product_c = [50, 62, 78, 98, 122, 153, 191, 239, 299, 374]
product_d = [30, 38, 48, 61, 77, 97, 122, 153, 191, 239]

# Revenue by Geography
north_america = [150, 180, 220, 265, 320, 384, 461, 553, 664, 797]
europe = [80, 95, 115, 140, 170, 204, 245, 294, 353, 423]
asia_pacific = [40, 50, 63, 80, 101, 127, 159, 199, 249, 311]
rest_of_world = [20, 25, 32, 40, 51, 64, 80, 100, 125, 156]
```

#### B. Extract Margin Data
```python
# Margin evolution
gross_margin = [58.0, 59.2, 60.5, 61.8, 63.0, 64.5, 66.0, 67.0, 67.5, 68.0]
ebitda_margin = [12.0, 15.5, 18.8, 22.0, 25.0, 28.0, 30.5, 32.0, 33.0, 34.0]
fcf_margin = [8.0, 11.0, 14.5, 18.0, 21.0, 24.0, 26.5, 28.0, 29.0, 30.0]
```

#### C. Extract DCF Sensitivity Data
```python
# DCF Sensitivity (from Task 3 valuation)
wacc_values = [7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
terminal_growth = [1.5, 2.0, 2.5, 3.0, 3.5]

# Price per share matrix (rows = WACC, columns = terminal growth)
dcf_sensitivity = np.array([
    [66, 71, 76, 82, 89],
    [58, 62, 67, 72, 78],
    [52, 55, 59, 63, 68],
    [47, 50, 53, 56, 60],
    [42, 45, 48, 51, 54],
    [39, 41, 44, 46, 49]
])
```

#### D. Extract Valuation Ranges
```python
# Valuation Football Field (from Task 3)
valuation_methods = ['DCF Analysis', 'Trading Comps\n(NTM)', 'Precedent\nTransactions']
valuation_low = [48, 45, 52]
valuation_high = [62, 57, 66]
current_price = 50
target_price = 55
```

### Step 3: Create Mandatory Charts

#### Chart 1: Revenue by Product - Stacked Area ⭐ MANDATORY

```python
def create_revenue_by_product_chart():
    """Create revenue by product stacked area chart"""

    fig, ax = plt.subplots(figsize=(10, 6))

    # Create stacked area chart
    ax.stackplot(years, product_a, product_b, product_c, product_d,
                 labels=['Product A', 'Product B', 'Product C', 'Product D'],
                 colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'],
                 alpha=0.8)

    # Formatting
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Revenue ($M)', fontsize=12, fontweight='bold')
    ax.set_title('Figure 3 - Revenue by Product/Segment (2020-2029E)',
                 fontsize=14, fontweight='bold', pad=20)

    # Legend
    ax.legend(loc='upper left', frameon=False, fontsize=10)

    # Grid
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Add vertical line to separate historical from projected
    ax.axvline(x=2024, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    ax.text(2024.2, ax.get_ylim()[1]*0.95, 'Projected →',
            fontsize=9, color='gray', ha='left')

    # Source line
    fig.text(0.12, 0.02, 'Source: Company data, [Firm] estimates',
             fontsize=9, style='italic', color='gray')

    # Save
    plt.tight_layout()
    plt.savefig('chart_03_revenue_by_product_stacked_area.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Created: chart_03_revenue_by_product_stacked_area.png")

create_revenue_by_product_chart()
```

#### Chart 2: Revenue by Geography - Stacked Bar ⭐ MANDATORY

```python
def create_revenue_by_geography_chart():
    """Create revenue by geography stacked bar chart"""

    years_labels = ['2020', '2021', '2022', '2023', '2024',
                    '2025E', '2026E', '2027E', '2028E', '2029E']

    fig, ax = plt.subplots(figsize=(10, 6))

    # Create stacked bar chart
    width = 0.6
    x = np.arange(len(years_labels))

    p1 = ax.bar(x, north_america, width, label='North America', color='#1f77b4')
    p2 = ax.bar(x, europe, width, bottom=north_america,
                label='Europe', color='#ff7f0e')
    p3 = ax.bar(x, asia_pacific, width,
                bottom=np.array(north_america) + np.array(europe),
                label='Asia-Pacific', color='#2ca02c')
    p4 = ax.bar(x, rest_of_world, width,
                bottom=np.array(north_america) + np.array(europe) + np.array(asia_pacific),
                label='Rest of World', color='#d62728')

    # Formatting
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Revenue ($M)', fontsize=12, fontweight='bold')
    ax.set_title('Figure 4 - Revenue by Geography (2020-2029E)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(years_labels, rotation=45, ha='right')

    # Legend
    ax.legend(loc='upper left', frameon=False, fontsize=10)

    # Grid
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Source line
    fig.text(0.12, 0.02, 'Source: Company data, [Firm] estimates',
             fontsize=9, style='italic', color='gray')

    # Save
    plt.tight_layout()
    plt.savefig('chart_04_revenue_by_geography_stacked_bar.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Created: chart_04_revenue_by_geography_stacked_bar.png")

create_revenue_by_geography_chart()
```

#### Chart 3: DCF Sensitivity - Heatmap ⭐ MANDATORY

```python
def create_dcf_sensitivity_heatmap():
    """Create DCF sensitivity analysis heatmap"""

    # Create DataFrame
    df = pd.DataFrame(dcf_sensitivity,
                      index=[f'{w}%' for w in wacc_values],
                      columns=[f'{g}%' for g in terminal_growth])

    fig, ax = plt.subplots(figsize=(8, 6))

    # Create heatmap
    sns.heatmap(df, annot=True, fmt='d', cmap='RdYlGn',
                cbar_kws={'label': 'Price per Share ($)'},
                linewidths=0.5, linecolor='white',
                ax=ax, vmin=35, vmax=95)

    # Formatting
    ax.set_xlabel('Terminal Growth Rate', fontsize=12, fontweight='bold')
    ax.set_ylabel('WACC', fontsize=12, fontweight='bold')
    ax.set_title('Figure 28 - DCF Sensitivity Analysis ($/share)',
                 fontsize=14, fontweight='bold', pad=20)

    # Rotate y-axis labels
    plt.yticks(rotation=0)

    # Source line
    fig.text(0.12, 0.02, 'Source: [Firm] estimates',
             fontsize=9, style='italic', color='gray')

    # Save
    plt.tight_layout()
    plt.savefig('chart_28_dcf_sensitivity_heatmap.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Created: chart_28_dcf_sensitivity_heatmap.png")

create_dcf_sensitivity_heatmap()
```

#### Chart 4: Valuation Football Field ⭐ MANDATORY

```python
def create_valuation_football_field():
    """Create valuation football field chart"""

    fig, ax = plt.subplots(figsize=(10, 5))

    # Create horizontal bars
    y_positions = np.arange(len(valuation_methods))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

    for i, (method, low, high, color) in enumerate(
            zip(valuation_methods, valuation_low, valuation_high, colors)):
        ax.barh(i, high - low, left=low, height=0.6,
                color=color, alpha=0.7, label=method)

        # Add value labels at ends
        ax.text(low - 1, i, f'${low}', va='center', ha='right', fontsize=10)
        ax.text(high + 1, i, f'${high}', va='center', ha='left', fontsize=10)

    # Add current price line
    ax.axvline(x=current_price, color='red', linestyle='--', linewidth=2,
               label=f'Current: ${current_price}', alpha=0.7)

    # Add target price line
    ax.axvline(x=target_price, color='black', linestyle='-', linewidth=2,
               label=f'Target: ${target_price}')

    # Formatting
    ax.set_yticks(y_positions)
    ax.set_yticklabels(valuation_methods, fontsize=11)
    ax.set_xlabel('Price Per Share ($)', fontsize=12, fontweight='bold')
    ax.set_title('Figure 32 - Valuation Football Field',
                 fontsize=14, fontweight='bold', pad=20)

    # Set x-axis limits
    ax.set_xlim(40, 70)

    # Remove spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Grid
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    # Legend
    ax.legend(loc='upper right', frameon=False, fontsize=9)

    # Source line
    fig.text(0.12, 0.02, 'Source: [Firm] estimates',
             fontsize=9, style='italic', color='gray')

    # Save
    plt.tight_layout()
    plt.savefig('chart_32_valuation_football_field.png',
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Created: chart_32_valuation_football_field.png")

create_valuation_football_field()
```

### Step 4: Create Remaining Required Charts (Charts 1-34)

**Complete the 25 REQUIRED charts** by creating all remaining charts from the required list. Each chart has a specific purpose in Task 5.

#### Investment Summary (1 chart)
```python
# chart_01: Stock Price Performance (12-24 months)
# - Line chart showing stock price over time vs. market index
# - Used on Page 1 of final report
```

#### Financial Performance (5 additional charts beyond chart_03 and chart_04)
```python
# chart_02: Revenue Growth Trajectory
# chart_10: Gross Margin Evolution
# chart_11: EBITDA Margin Progression
# chart_12: Free Cash Flow Trend
# chart_14: Scenario Comparison (Bull/Base/Bear)
```

#### Company 101 Section (7 charts)
```python
# chart_05: Company Overview/Timeline
# chart_06: Key Milestones Timeline
# chart_07: Organizational Structure
# chart_08: Product Portfolio Overview
# chart_09: Customer Segmentation
# chart_15: Market Size Evolution (TAM)
# chart_16: Competitive Positioning Matrix
```

#### Competitive & Market (2 charts)
```python
# chart_17: Market Share Breakdown
# chart_18: Competitive Benchmarking
```

#### Scenario Analysis (1 chart)
```python
# chart_13: Operating Metrics Dashboard
```

#### Valuation Section (6 additional charts beyond chart_28 and chart_32)
```python
# chart_29: DCF Valuation Waterfall
# chart_30: Trading Comps Scatter Plot
# chart_31: Peer Multiples Comparison
# chart_33: Price Target Scenarios
# chart_34: Historical Valuation Multiples
```

**Use consistent formatting across all charts:**
- 300 DPI resolution
- Professional color scheme
- Clear labels, legends, and titles
- Figure numbers (e.g., "Figure 5 - Company Timeline")
- Source citations at bottom

### Step 4B: Create Optional Charts (For 26-35 Total)

**Optional**: Add 1-10 additional charts from this list for greater visual density:

```python
# chart_19: Customer Acquisition Trends
# chart_20: Unit Economics Evolution
# chart_21: Product Roadmap Timeline
# chart_22: Geographic Expansion Map
# chart_23: R&D Investment Trends
# chart_24: Sales & Marketing Efficiency
# chart_25: Working Capital Trends
# chart_26: Debt Maturity Schedule
# chart_27: Ownership Structure
# chart_35: Analyst Price Target Distribution
```

These optional charts provide additional visual storytelling and help achieve the "1 chart per 200-300 words" density target in Task 5.

### Step 5: Create Chart Index

Create a text file documenting all charts:

```python
def create_chart_index():
    """Create index of all charts"""

    # 25 REQUIRED CHARTS
    required_charts = [
        "chart_01_stock_price_performance.png - Stock Price Performance (12-24M)",
        "chart_02_revenue_growth_trajectory.png - Revenue Growth Trajectory",
        "chart_03_revenue_by_product_stacked_area.png - Revenue by Product [MANDATORY]",
        "chart_04_revenue_by_geography_stacked_bar.png - Revenue by Geography [MANDATORY]",
        "chart_05_company_overview.png - Company Overview/Timeline",
        "chart_06_key_milestones_timeline.png - Key Milestones Timeline",
        "chart_07_organizational_structure.png - Organizational Structure",
        "chart_08_product_portfolio.png - Product Portfolio Overview",
        "chart_09_customer_segmentation.png - Customer Segmentation",
        "chart_10_gross_margin_evolution.png - Gross Margin Evolution",
        "chart_11_ebitda_margin_progression.png - EBITDA Margin Progression",
        "chart_12_free_cash_flow_trend.png - Free Cash Flow Trend",
        "chart_13_operating_metrics_dashboard.png - Operating Metrics Dashboard",
        "chart_14_scenario_comparison.png - Scenario Comparison (Bull/Base/Bear)",
        "chart_15_market_size_evolution.png - Market Size Evolution (TAM)",
        "chart_16_competitive_positioning.png - Competitive Positioning Matrix",
        "chart_17_market_share.png - Market Share Breakdown",
        "chart_18_competitive_benchmarking.png - Competitive Benchmarking",
        "chart_28_dcf_sensitivity_heatmap.png - DCF Sensitivity Heatmap [MANDATORY]",
        "chart_29_dcf_waterfall.png - DCF Valuation Waterfall",
        "chart_30_trading_comps_scatter.png - Trading Comps Scatter Plot",
        "chart_31_peer_multiples_comparison.png - Peer Multiples Comparison",
        "chart_32_valuation_football_field.png - Valuation Football Field [MANDATORY]",
        "chart_33_price_target_scenarios.png - Price Target Scenarios",
        "chart_34_historical_valuation_multiples.png - Historical Valuation Multiples",
    ]

    # 10 OPTIONAL CHARTS (for 26-35 range)
    optional_charts = [
        "chart_19_customer_acquisition_trends.png - Customer Acquisition Trends [OPTIONAL]",
        "chart_20_unit_economics_evolution.png - Unit Economics Evolution [OPTIONAL]",
        "chart_21_product_roadmap_timeline.png - Product Roadmap Timeline [OPTIONAL]",
        "chart_22_geographic_expansion_map.png - Geographic Expansion Map [OPTIONAL]",
        "chart_23_rd_investment_trends.png - R&D Investment Trends [OPTIONAL]",
        "chart_24_sales_marketing_efficiency.png - Sales & Marketing Efficiency [OPTIONAL]",
        "chart_25_working_capital_trends.png - Working Capital Trends [OPTIONAL]",
        "chart_26_debt_maturity_schedule.png - Debt Maturity Schedule [OPTIONAL]",
        "chart_27_ownership_structure.png - Ownership Structure [OPTIONAL]",
        "chart_35_analyst_price_targets.png - Analyst Price Target Distribution [OPTIONAL]",
    ]

    with open('chart_index.txt', 'w') as f:
        f.write("CHART INDEX FOR [COMPANY] EQUITY RESEARCH REPORT\n")
        f.write("=" * 60 + "\n\n")

        f.write("4 MANDATORY CHARTS (Must be present):\n")
        f.write("- chart_03: Revenue by Product (Stacked Area) ⭐\n")
        f.write("- chart_04: Revenue by Geography (Stacked Bar) ⭐\n")
        f.write("- chart_28: DCF Sensitivity (Heatmap) ⭐\n")
        f.write("- chart_32: Valuation Football Field ⭐\n\n")

        f.write("25 REQUIRED CHARTS:\n")
        for chart in required_charts:
            f.write(f"  {chart}\n")

        f.write("\n10 OPTIONAL CHARTS (for 26-35 total):\n")
        for chart in optional_charts:
            f.write(f"  {chart}\n")

        f.write("\n" + "=" * 60 + "\n")
        f.write("NOTE: Task 5 will embed ALL charts created (25-35) throughout\n")
        f.write("the report for visual density (1 chart every 200-300 words).\n")

    print("✓ Created: chart_index.txt")

create_chart_index()
```

### Step 6: Quality Check

**Run verification checks:**

```python
import os

def verify_charts():
    """Verify all charts were created successfully"""

    mandatory_charts = [
        'chart_03_revenue_by_product_stacked_area.png',
        'chart_04_revenue_by_geography_stacked_bar.png',
        'chart_28_dcf_sensitivity_heatmap.png',
        'chart_32_valuation_football_field.png'
    ]

    print("\n" + "="*60)
    print("CHART GENERATION VERIFICATION")
    print("="*60)

    # Check mandatory charts
    print("\n1. MANDATORY CHARTS:")
    all_mandatory_present = True
    for chart in mandatory_charts:
        if os.path.exists(chart):
            size = os.path.getsize(chart) / 1024  # KB
            print(f"   ✓ {chart} ({size:.1f} KB)")
        else:
            print(f"   ✗ MISSING: {chart}")
            all_mandatory_present = False

    # Count total charts
    chart_files = [f for f in os.listdir('.') if f.startswith('chart_') and f.endswith('.png')]
    print(f"\n2. TOTAL CHARTS: {len(chart_files)}")
    print(f"   Target: 25-35 charts")
    print(f"   Status: {'✓ PASS' if 25 <= len(chart_files) <= 35 else '⚠ WARNING'}")

    # Check file sizes (should be > 50KB for 300 DPI)
    print("\n3. FILE SIZE CHECK:")
    small_files = []
    for chart in chart_files[:5]:  # Sample first 5
        size = os.path.getsize(chart) / 1024
        if size < 50:
            small_files.append(chart)
        print(f"   {chart}: {size:.1f} KB")

    if small_files:
        print(f"   ⚠ WARNING: {len(small_files)} files may be low resolution")
    else:
        print(f"   ✓ All sampled files have adequate size")

    # Final verdict
    print("\n" + "="*60)
    if all_mandatory_present and 25 <= len(chart_files) <= 35:
        print("✓ VERIFICATION PASSED - Ready for Task 5")
    else:
        print("✗ VERIFICATION FAILED - Review missing charts")
    print("="*60 + "\n")

verify_charts()
```

---

## Quality Standards

### Visual Quality
- [ ] High resolution (300 DPI minimum)
- [ ] Professional color scheme (consistent across all charts)
- [ ] Clear, legible text (no fonts smaller than 9pt)
- [ ] Proper aspect ratio (no distortion)
- [ ] No pixelation or artifacts

### Data Accuracy
- [ ] Data matches source (financial model and valuation)
- [ ] Proper units and labels ($ millions, percentages, etc.)
- [ ] Appropriate scale and range
- [ ] Consistent time periods across charts
- [ ] Verified calculations

### Formatting Quality
- [ ] Consistent styling across all charts
- [ ] Proper figure numbering (sequential)
- [ ] Clear titles and captions
- [ ] Source citations on every chart
- [ ] Professional appearance

### Completeness
- [ ] All 4 mandatory charts created
- [ ] 25-35 total charts
- [ ] Proper file naming (chart_01, chart_02, etc.)
- [ ] Chart index created
- [ ] Ready for embedding in Word

---

## Chart Types Reference

### When to Use Each Chart Type

**Line Charts**: Time series trends (revenue, margins, stock price)

**Stacked Area**: Revenue by product ⭐, market size composition

**Stacked Bar**: Revenue by geography ⭐, quarterly breakdowns

**Heatmap**: DCF sensitivity ⭐, correlation matrices

**Horizontal Bar**: Valuation football field ⭐, peer rankings

**Waterfall**: Revenue bridges, margin analysis, DCF build-up

**Scatter/Bubble**: Growth vs. valuation, competitive positioning

**2×2 Matrix**: Competitive positioning, product portfolio

---

## File Naming Convention

**Always use this format:**
```
chart_[NUMBER]_[DESCRIPTION].png

Examples:
chart_01_stock_price_performance.png
chart_03_revenue_by_product_stacked_area.png
chart_28_dcf_sensitivity_heatmap.png
```

**Number charts sequentially** based on their position in the report, not creation order.

---

## Common Chart Generation Issues

### Issue 1: Low Resolution
**Problem**: Chart looks pixelated
**Solution**: Ensure `dpi=300` in `plt.savefig()`

### Issue 2: Text Cutoff
**Problem**: Labels or titles cut off at edges
**Solution**: Use `bbox_inches='tight'` in `plt.savefig()`

### Issue 3: Poor Colors
**Problem**: Colors don't look professional
**Solution**: Use established palettes like Tableau10 or define custom corporate colors

### Issue 4: Overlapping Labels
**Problem**: Axis labels overlap
**Solution**: Rotate labels (e.g., `rotation=45`) or reduce font size

### Issue 5: White Space
**Problem**: Too much white space around chart
**Solution**: Use `plt.tight_layout()` before saving

---

## Success Criteria

A successful chart package should:
1. **Include all 4 mandatory charts** (verified) ⭐
   - chart_03: Revenue by Product
   - chart_04: Revenue by Geography
   - chart_28: DCF Sensitivity
   - chart_32: Valuation Football Field
2. **Create 25 required charts minimum** (verified)
3. **Optional: 1-10 additional charts** for 26-35 total
4. Have consistent professional styling across all charts
5. Be high resolution (300 DPI) for print quality
6. Have clear labels, legends, and titles on every chart
7. Include proper figure numbers and source citations
8. Be ready for immediate embedding in Word
9. Cover all key financial metrics and analyses
10. Tell a visual story complementing the written analysis
11. Be accurate and auditable to source data (model/valuation)
12. All charts packaged in zip file with chart index

**Remember**: Task 5 will embed ALL charts created (25-35) throughout the report for visual density.

---

## Output Files

After completing Task 4, deliverables include:

**25 REQUIRED Chart Files (Minimum):**
1. chart_01_stock_price_performance.png
2. chart_02_revenue_growth_trajectory.png
3. chart_03_revenue_by_product_stacked_area.png ⭐ MANDATORY
4. chart_04_revenue_by_geography_stacked_bar.png ⭐ MANDATORY
5. chart_05_company_overview.png
6. chart_06_key_milestones_timeline.png
7. chart_07_organizational_structure.png
8. chart_08_product_portfolio.png
9. chart_09_customer_segmentation.png
10. chart_10_gross_margin_evolution.png
11. chart_11_ebitda_margin_progression.png
12. chart_12_free_cash_flow_trend.png
13. chart_13_operating_metrics_dashboard.png
14. chart_14_scenario_comparison.png
15. chart_15_market_size_evolution.png
16. chart_16_competitive_positioning.png
17. chart_17_market_share.png
18. chart_18_competitive_benchmarking.png
19-27. *Reserved for optional charts if created*
28. chart_28_dcf_sensitivity_heatmap.png ⭐ MANDATORY
29. chart_29_dcf_waterfall.png
30. chart_30_trading_comps_scatter.png
31. chart_31_peer_multiples_comparison.png
32. chart_32_valuation_football_field.png ⭐ MANDATORY
33. chart_33_price_target_scenarios.png
34. chart_34_historical_valuation_multiples.png
35. *Reserved for optional chart if created*

**10 OPTIONAL Chart Files (For 26-35 Total):**
- chart_19 through chart_27, chart_35 (if created)

**Chart Index** (1 text file):
- chart_index.txt (listing all charts with descriptions and categories)

**All chart files must be:**
- 300 DPI resolution (print quality)
- 6-10 inches wide (standard Word embedding size)
- White background (professional appearance)
- PNG format (lossless quality)
- Ready for immediate Word embedding

**Final Step: Package All Charts**

Create a zip file containing all chart files and the chart index:

```
[Company]_Charts_[Date].zip
├── chart_01_stock_price_performance.png
├── chart_02_revenue_growth_trajectory.png
├── chart_03_revenue_by_product_stacked_area.png ⭐
├── chart_04_revenue_by_geography_stacked_bar.png ⭐
├── chart_05_company_overview.png
├── ... (all 25-35 chart files)
├── chart_28_dcf_sensitivity_heatmap.png ⭐
├── chart_32_valuation_football_field.png ⭐
├── chart_34_historical_valuation_multiples.png
└── chart_index.txt
```

**Example**: `Tesla_Charts_2024-10-28.zip`

**Why this matters**: Task 5 will embed ALL charts created (25-35) throughout the report. The report requires visual density (1 chart per 200-300 words), so all charts serve a purpose—either for specific analytical sections or for visual storytelling and page density.
- Verify all 25-35 charts are present
- Extract charts for Task 5 (Report Assembly)

---

## Next Steps

After completing Task 4, the zip file will be used for:
- **Task 5 (Report Assembly)**: Extract charts and embed all into the final DOCX report at appropriate locations throughout the document

The 4 mandatory charts are critical for the valuation and financial analysis sections of the report.

### Referencia: references/task5-report-assembly.md

# Task 5: Report Assembly - Detailed Workflow

This document provides step-by-step instructions for executing Task 5 (Report Assembly) of the initiating-coverage skill.

## Task Overview

**Purpose**: Write and assemble the comprehensive final DOCX report.

**Prerequisites**: ⚠️ Verify before starting - ALL PREVIOUS TASKS REQUIRED
- **Required**: Company research from Task 1
- **Required**: Financial model from Task 2
- **Required**: Valuation analysis from Task 3
- **Required**: Chart files from Task 4

**⚠️ CRITICAL: DO NOT START THIS TASK UNLESS ALL TASKS 1-4 ARE COMPLETE**

This is the final assembly task. It cannot be completed without all previous work products.

**IF ANY OF TASKS 1, 2, 3, OR 4 ARE NOT COMPLETE**: Stop immediately and inform the user which tasks need to be completed first. The specific requirements are:
- Task 1: Company research document (6-8K words)
- Task 2: Financial model with all 6 tabs
- Task 3: Valuation analysis with price target and recommendation
- Task 4: Charts zip file with 25-35 charts

Do not attempt to create placeholder content, substitute missing sections, or assemble an incomplete report. The report requires ALL inputs to be publication-ready.

**Output**: Comprehensive Equity Research Report (.docx)
- Length: 30-50 pages (MINIMUM 30)
- Word count: 10,000-15,000 words (MINIMUM 10,000)
- Charts: 25-35 embedded images
- Tables: 12-20 comprehensive tables

---

## 🔥 CRITICAL INSTRUCTION: SPARE NO TOKENS OR EFFORT

**THIS IS THE FINAL DELIVERABLE. GO ALL OUT. NO SHORTCUTS. NO ABBREVIATIONS.**

After completing 4 previous tasks, this final task assembles everything into publication-ready institutional research. **This must be PERFECT.**

### Absolute Requirements

**DO:**
- ✅ **Use ENTIRE token budget if needed** - This is what it's for
- ✅ **Write EVERY section in FULL** - Not summaries, not placeholders, FULL CONTENT
- ✅ **Include ALL 25-35 charts** - Embed every single chart from Task 4 throughout the document
- ✅ **Create ALL 12-20 tables** - Extract every financial table from Excel, don't skip any
- ✅ **Copy ALL 6-8K words from Task 1** - Use Company 101 content verbatim (40-50% of report)
- ✅ **Write 2,000-3,000 words on Projection Assumptions** - Product-by-product, region-by-region detail
- ✅ **Write 1,500-2,000 words on Scenario Analysis** - Specific Bull/Base/Bear parameters
- ✅ **Achieve 10,000-15,000 total words** - This is a MINIMUM, not a suggestion
- ✅ **Produce 30-50 pages minimum** - Text-dense with charts every 200-300 words
- ✅ **Professional institutional quality** - Indistinguishable from JPMorgan/Goldman Sachs

**NEVER:**
- ❌ "This section would include..." - WRITE THE ACTUAL SECTION
- ❌ "Charts would be inserted here..." - INSERT THE ACTUAL CHARTS
- ❌ "See financial model for details..." - EXTRACT AND WRITE THE DETAILS
- ❌ "For brevity, we'll summarize..." - NO SUMMARIZING, WRITE IN FULL
- ❌ Skip sections to conserve tokens - USE WHATEVER TOKENS ARE NEEDED
- ❌ Create abbreviated versions - EVERY SECTION MUST BE COMPLETE
- ❌ Reference external files instead of including content - INCLUDE EVERYTHING

### Quality Standard

**This report will be read by institutional investors making million-dollar decisions.**

It must be:
- **Complete**: Every section written in full with no placeholders
- **Comprehensive**: All data extracted and included, all charts embedded
- **Professional**: Proper formatting, citations, tables, charts throughout
- **Thorough**: Deep analysis with specific numbers, detailed assumptions, complete scenarios
- **Dense**: 60-80% page coverage with text and visuals on every page

**Creating the final work product of a 6-10 hour equity research process. Make it count.**

---

## Input Verification (CRITICAL)

**BEFORE STARTING - ALL TASKS MUST BE COMPLETE:**

### Task 1 Verification:
- [ ] Company research document exists? (6-8K words)
- [ ] Management bios complete? (300-400 words × 3-4 execs)
- [ ] Competitive analysis complete? (5-10 competitors)
- [ ] Risk assessment complete? (8-12 risks)

### Task 2 Verification:
- [ ] Financial model exists and can be opened?
- [ ] Model has projections (5 years)?
- [ ] Scenarios exist (Bull/Base/Bear)?
- [ ] Revenue by product table complete (20-30 rows)?
- [ ] Revenue by geography table complete (15-20 rows)?

### Task 3 Verification:
- [ ] Valuation analysis complete?
- [ ] Price target determined?
- [ ] Recommendation set? (BUY/HOLD/SELL)
- [ ] DCF analysis complete with sensitivity table?
- [ ] Comparable companies analysis complete with statistical summary?

### Task 4 Verification:
- [ ] 25-35 chart files exist?
- [ ] All 4 mandatory charts present?
  - [ ] Revenue by product (stacked area)
  - [ ] Revenue by geography (stacked bar)
  - [ ] DCF sensitivity (heatmap)
  - [ ] Valuation football field
- [ ] Chart files accessible and can be opened?
- [ ] Chart index created?

**IF ANY VERIFICATION FAILS**: Stop and complete missing task first.

---

## Report Specifications

### Length Requirements
- **Pages**: 30-50 (MINIMUM 30 pages)
- **Word Count**: 10,000-15,000 words (MINIMUM 10,000 words)
- **Charts**: 25-35 embedded PNG/JPG images
- **Tables**: 12-20 comprehensive financial tables
- **Density**: 60-80% page coverage

### Critical Sections with Word Counts

| Section | Minimum | Target | Critical? |
|---------|---------|--------|-----------|
| Investment Summary (Page 1) | 500 | 700 | |
| Investment Thesis | 800 | 1,200 | |
| Risk Factors | 600 | 900 | |
| Company Description | 800 | 1,200 | |
| Management Bios | 1,000 | 1,400 | |
| Products & Services | 700 | 1,000 | |
| **Projection Assumptions** | **2,000** | **3,000** | ⭐ YES |
| **Scenario Analysis** | **1,500** | **2,000** | ⭐ YES |
| Financial Analysis | 1,200 | 1,800 | |
| Valuation Methodology | 800 | 1,200 | |

**Total: 10,000-15,000 words**

---

## Report Structure

### Page 1: Investment Summary (CRITICAL PAGE)

**This is the most important page. Must have:**

1. **"INITIATING COVERAGE" header** (NOT "Company Update")
2. **Thesis-focused title** (e.g., "AI Platform Leader Positioned for 40% CAGR")
3. **Rating box** with:
   - Rating (BUY/OUTPERFORM/HOLD/UNDERPERFORM/SELL)
   - Current price
   - Target price
   - 52-week range
   - Market cap
   - Enterprise value
4. **Research analyst information** with credentials
5. **Stock price performance chart** (Figure 1)
6. **3-4 detailed investment bullets** with ■ character
   - Each bullet has **bold topic header** + 3-5 sentences
   - Lead with key numbers
7. **Financial summary table** (2-3 years historical + 2-3 years projected)
   - Years noted as "A" for actual, "E" for estimate

**Bullet Format Example:**
```
■ **Vertical SaaS leadership and regulatory moat should enable $50bn+ TAM by 2030.**
Deep domain expertise in healthcare IT, strong customer retention (95%+ net revenue retention),
and cross-sell capabilities have driven Acme Health's market expansion. With the healthcare IT
market expected to reach $50bn+ by 2030, Acme Health is well-positioned to capture share given
its regulatory moat and high switching costs. Management has indicated that 70% of current
revenue comes from enterprise hospital systems, suggesting strong product-market fit.
```

### Pages 2-5: Investment Thesis & Risks

**Investment Thesis (800-1,200 words)**
- 3-5 key thesis pillars
- Each pillar: 200-300 words
- Lead with key statistic
- Quantify financial impact
- Include timeline

**Risk Assessment (600-900 words)**
- 8-12 identified risks
- Organized by category:
  - Company-specific risks (4-6)
  - Industry/market risks (3-4)
  - Financial risks (2-3)
  - Macroeconomic risks (2-3)
- Each risk: 50-100 word description

### Pages 6-17: Company 101

**Company Description (800-1,200 words)**
- What the company does (plain English)
- Business model and monetization
- Geographic presence
- Scale metrics

**Company History (800-1,200 words)**
- Founding story
- Timeline of major milestones
- Strategic pivots
- Recent developments

**Management Team (1,000-1,400 words)**
- 300-400 word bio for each of 3-4 key executives
- Include: role, background, accomplishments, education
- Governance structure

**Products & Services (700-1,000 words)**
- Detailed product portfolio
- Features and differentiation
- Target customers
- Pricing models

**Customers & Go-to-Market (500-700 words)**
- Customer segments
- Distribution channels
- Sales strategy
- Key partnerships

**Industry Overview (800-1,200 words)**
- Industry definition and scope
- Market size and growth
- Key trends
- Regulatory environment

**Competitive Landscape (700-1,000 words)**
- 5-10 key competitors
- Market positioning
- Competitive advantages
- Market share analysis

**TAM Analysis (500-700 words)**
- Total addressable market sizing
- Market growth projections
- Company's serviceable market

### Pages 18-30: Financial Analysis

**Historical Financial Analysis (1,200-1,800 words)**
- Revenue trends and drivers
- Margin evolution
- Cash flow analysis
- Key metrics trajectory
- Historical context

**Projection Assumptions (2,000-3,000 words)** ⭐ CRITICAL

**MUST be extremely detailed. Structure:**

**A. Revenue by Product Assumptions (1,000-1,500 words)**

For EACH major product category:
```
[Product Category A] Revenue Assumptions

We project [Product A] revenue to grow from $XXM in 2024A to $XXM in 2029E,
representing a XX% CAGR. This growth is driven by:

1. [Driver 1 with specific quantification]
   - Specific metric: from XX to XX
   - Timeline: achieving YY by 2026E
   - Basis: [source or rationale]

2. [Driver 2 with specific quantification]
3. [Driver 3 with specific quantification]
[... 8-12 detailed points total for this product ...]

Specific assumptions by year:
- 2025E: XX% growth driven by [specific factors]
- 2026E: XX% growth as [specific factors]
- 2027-2029E: XX% CAGR as [longer-term factors]

Key risks to these assumptions include [specific risks].
```

**Repeat for EACH major product category.**

**B. Geographic Revenue Assumptions (500-800 words)**

For EACH major region:
```
[Region] Revenue Assumptions

We project [Region] revenue to grow XX% CAGR from 2024-2029E, reaching $XXM, driven by:

1. [Market dynamic with quantification]
2. [Distribution expansion with specifics]
3. [Competitive positioning]
[... 6-8 detailed points total for this region ...]
```

**Repeat for EACH major geographic region.**

**C. Other Key Assumptions (500-700 words)**
- Gross margin evolution (with specific drivers and bridge)
- Operating expense assumptions (R&D, S&M, G&A as % of revenue)
- Working capital assumptions (DSO, DIO, DPO with specific days)
- CapEx as % of sales (with justification)
- Tax rate assumptions

**Scenario Analysis (1,500-2,000 words)** ⭐ CRITICAL

**MUST have specific parameters for each scenario. Structure:**

**Bull Case (500-700 words)**
```
Bull Case: [Title describing key optimistic scenario]

Probability: XX%

Key Assumptions:
- Revenue CAGR (2024-2029E): XX% (vs. XX% base case)
- 2029E Revenue: $X,XXXm (vs. $X,XXXm base)
- 2029E EBITDA Margin: XX% (vs. XX% base)
- Key product growth: XX% CAGR (vs. XX% base)
- Geographic expansion: [specific milestones and timeline]
- Market share: XX% by 2029E (vs. XX% base)

Catalysts Required for Bull Case:
1. [Specific catalyst] - Expected timing: [date/quarter]
2. [Specific catalyst] - Expected timing: [date/quarter]
3. [Specific catalyst] - Expected timing: [date/quarter]

Detailed Rationale:
[200-300 words explaining what needs to happen for bull case to materialize.
Be specific about product launches, market conditions, competitive dynamics, etc.]

Valuation Implications:
- DCF Value: $XX per share (XX% upside from current)
- Trading Comps: XX.Xx EV/EBITDA implies $XX per share
- Bull Case Target: $XX per share
```

**Base Case (300-500 words)**
```
Base Case: [Title describing most likely scenario]

Probability: XX%

Key Assumptions:
[Similar structure to Bull Case with base assumptions]

Rationale:
[Explain why this is most likely scenario]

Valuation:
- DCF Value: $XX per share
- Trading Comps: $XX per share
- Base Case Target: $XX per share (weighted average)
```

**Bear Case (500-700 words)**
```
Bear Case: [Title describing downside scenario]

Probability: XX%

Key Assumptions:
[Similar structure with downside parameters]

Downside Triggers:
1. [Specific risk event] - Likelihood: [%]
2. [Specific risk event] - Likelihood: [%]
3. [Specific risk event] - Likelihood: [%]

Rationale:
[200-300 words on what would cause bear case]

Valuation Implications:
- DCF Value: $XX per share (XX% downside from current)
- Trading Comps: $XX per share
- Bear Case Target: $XX per share
```

**Scenario Comparison (200-300 words)**
- Comprehensive comparison table with key metrics
- Analysis of probability-weighted outcomes
- Risk/reward assessment
- Path dependency discussion

**Growth Drivers (800-1,200 words)**
- 3-5 key growth drivers
- Each quantified with specific opportunity size
- Timeline and milestones
- Supporting data from model

### Pages 31-40: Valuation Analysis

**Valuation Methodology (800-1,200 words)**

**DCF Analysis (300-400 words)**
- Methodology explanation
- Key assumptions:
  - WACC: X.X% (calculation breakdown)
  - Terminal growth: X.X% (rationale)
  - Terminal margin: XX% (justification)
- Sensitivity analysis discussion
- DCF value: $XX per share

**Comparable Companies (300-400 words)**
- Peer selection rationale (why these 5-10 companies)
- Statistical summary (max/75th/median/25th/min)
- Multiple selection (why EV/EBITDA vs. EV/Revenue vs. P/E)
- Premium/discount justification (why target deserves premium/discount)
- Comparable companies value: $XX per share

**Precedent Transactions (200-300 words, if applicable)**
- Transaction relevance
- Control premium analysis
- Precedent transactions value: $XX per share

**Valuation Reconciliation (200-300 words)**
- Weighting rationale (e.g., DCF 50%, Comps 40%, Precedent 10%)
- Weighted average calculation
- Valuation range (low/base/high)
- Final price target: $XX

**Price Target & Recommendation (300-500 words)**
- Final recommendation (BUY/OUTPERFORM/HOLD/UNDERPERFORM/SELL)
- Price target: $XX (XX% upside from current $XX)
- Time horizon: 12 months
- Key catalysts (3-5 with specific timeframes)
- Key risks to price target (3-5 with impact quantification)

### Pages 41-50: Appendices

**Data Sources & References**
- All sources listed with dates
- Organized by category:
  - SEC Filings (with EDGAR links)
  - Earnings Calls (with transcript links)
  - Company Materials
  - Industry Reports
  - News Articles
- **ALL URLs must be clickable hyperlinks**

**Detailed Financial Model Assumptions**
- Comprehensive assumptions detail
- Calculation methodologies
- Data sources for historical figures

**Additional Supporting Tables**
- Extended financial projections
- Detailed comparable companies data
- Sensitivity analyses

---

## Report Assembly Philosophy

**CRITICAL PRINCIPLE 1**: A good equity research report is **text-dense with lots of illustrating images**.

**Target density**: 60-80% page coverage
- Every page should have BOTH text AND visuals
- Charts should be interspersed throughout text, not grouped
- Average 1 chart per page minimum (30-50 pages = 25-35+ charts)
- Tables should break up large text blocks

**CRITICAL PRINCIPLE 2**: Use Claude's DOCX and XLSX skills to programmatically create the report.

**REQUIRED TOOLS** (Claude has built-in skills for these):
- **DOCX skill** - To create and manipulate Word documents
  - Read Task 1 .md file → Convert to Word formatting
  - Insert images from Task 4 chart files
  - Create tables
  - Format text, headers, footers, page numbers
  - Add hyperlinks
- **XLSX skill** - To read data from Excel files
  - Extract tables from Task 2 financial model
  - Read Task 3 valuation tabs
  - Pull historical financials from Task 1
- **Direct file operations** - Work with actual files
  - Read: `[Company]_Research_Document_[Date].md`
  - Read: `[Company]_Financial_Model_[Date].xlsx`
  - Read: `chart_01.png`, `chart_02.png`, etc.
  - Write: `[Company]_Initiation_Report_[Date].docx`

**DO NOT**: Manually copy/paste or describe what should be done
**DO**: Use Claude's DOCX and XLSX skills to open files, extract data, and create the DOCX report

**Content Reuse Strategy**:
- **Task 1 content (40-50% of report)**: Read .md file → Convert to Word format → Add charts
- **Task 2/3 data (30-40% of report)**: Read .xlsx file → Extract tables → Write interpretation
- **Original writing (10-20% of report)**: Investment thesis, projection assumptions, scenario analysis

**This approach**:
- Maximizes efficiency (no rewriting 6-8K words that are already good)
- Maintains quality (Task 1 content is substantive, professional analysis)
- Focuses effort on value-add (quantitative interpretation and investment thesis)
- Uses actual files programmatically (not manual work)

---

## Step-by-Step Report Assembly Workflow

### Step 1: Organize All Inputs and Verify Files

**Verify all input files exist:**

Use Claude's file operations to check:
- `[Company]_Research_Document_[Date].md` (Task 1)
- `[Company]_Historical_Financials_[Date].xlsx` (Task 1)
- `[Company]_Financial_Model_[Date].xlsx` (Task 2 with Task 3 tabs)
- `[Company]_Valuation_Analysis_[Date].md` (Task 3)
- `[Company]_Charts_[Date].zip` (Task 4) - **Extract this first**

**Step 1a: Extract Charts from Zip File**

Before proceeding, extract all chart files from the Task 4 zip:
- Locate `[Company]_Charts_[Date].zip`
- Extract all contents to a working directory (e.g., `task4_charts/`)
- Verify 25-35 PNG files were extracted
- Verify chart_index.txt is present

**Expected folder structure after extraction:**
```
[Company]_Report_Working/
├── [Company]_Research_Document_[Date].md
├── [Company]_Historical_Financials_[Date].xlsx
├── [Company]_Financial_Model_[Date].xlsx (includes Task 3 valuation tabs)
│   ├── [Task 2 tabs: Revenue Model, Income Statement, Scenarios, etc.]
│   └── [Task 3 tabs: DCF, Sensitivity, Comps, Valuation Summary]
├── [Company]_Valuation_Analysis_[Date].md
├── [Company]_Charts_[Date].zip
├── task4_charts/ (extracted from zip)
│   ├── chart_01_stock_price.png
│   ├── chart_02_revenue_growth.png
│   ├── chart_03_revenue_by_product.png ⭐
│   ├── chart_04_revenue_by_geography.png ⭐
│   ├── ... (21-31 more charts)
│   ├── chart_28_dcf_sensitivity.png ⭐
│   ├── chart_32_valuation_football_field.png ⭐
│   └── chart_index.txt
└── sources_and_urls.txt
```

**Open and inspect files using Claude skills:**

1. **Read Task 1 markdown file** - Use Read tool to view content
2. **Open Task 2/3 Excel file** - Use XLSX skill to inspect tabs:
   - Verify required tabs exist: Revenue Model, Income Statement, Scenarios, DCF, Sensitivity Analysis, Comparable Companies
3. **Read Task 3 markdown file** - Use Read tool to view valuation analysis
4. **Check chart files** - Verify all 25-35 PNG files present

**Note**: Task 2's financial model file now contains both the original modeling tabs (from Task 2) AND the valuation tabs (added by Task 3). This single Excel file contains all quantitative data needed for report assembly.

### Step 2: Extract Tables from Excel Using XLSX Skill

**Use Claude's XLSX skill to extract data from Excel files:**

#### Table 1: Page 1 Summary Financials

Use XLSX skill to:
1. Open `[Company]_Financial_Model_[Date].xlsx`
2. Read from `Income Statement` tab
3. Extract key rows: Revenue, Gross Profit, EBITDA, Net Income, EPS, FCF
4. Extract years: 2022A, 2023A, 2024A, 2025E, 2026E, 2027E
5. Create summary table with growth rates and margins

#### Table 2: Full Income Statement (40-50 line items)

Use XLSX skill to:
1. Open `[Company]_Financial_Model_[Date].xlsx`
2. Read entire `Income Statement` tab
3. Extract all line items (40-50 rows)
4. Extract columns for historical (2020A-2024A) + projected years (2025E-2029E)
5. Include all margins and growth rates

#### Table 3: Revenue by Product (20-30 rows)

Use XLSX skill to:
1. Open `[Company]_Financial_Model_[Date].xlsx`
2. Read from `Revenue Model` tab
3. Navigate to product section (typically starts ~row 5)
4. Extract 20-30 rows showing each product category
5. Include columns: Product name, historical years, projected years, % of Total, YoY Growth

#### Table 4: Revenue by Geography (15-20 rows)

Use XLSX skill to:
1. Open `[Company]_Financial_Model_[Date].xlsx`
2. Read from `Revenue Model` tab
3. Navigate to geography section (typically starts ~row 40)
4. Extract 15-20 rows showing each geographic region
5. Include columns: Region, historical years, projected years, % of Total, YoY Growth

#### Table 5: Comparable Companies
**Extract from:** Task 3 valuation tabs in Task 2's financial model (`Comparable Companies` tab)

Use XLSX skill to:
1. Open `[Company]_Financial_Model_[Date].xlsx`
2. Read from `Comparable Companies` tab (added by Task 3)
3. Extract full table with company names as row headers
4. **CRITICAL**: Verify statistical summary rows are present at bottom:
   - Maximum
   - 75th Percentile
   - Median
   - 25th Percentile
   - Minimum
5. If statistical summary is missing, report ERROR

**Expected format:**
```
Company      Ticker  Mkt Cap  EV/Rev  EV/Rev  EV/EBITDA  EV/EBITDA  P/E   Rev     EBITDA
                     ($B)     LTM     NTM     LTM        NTM        NTM   Growth  Margin
[5-10 peers plus target, then statistical summary]
```

#### Additional Tables (7-15 more)
**Extract from Task 2 financial model (with Task 3 tabs):**

Use XLSX skill to extract these tables:

**DCF Assumptions Table** (Task 3 `DCF` tab)
- Open `[Company]_Financial_Model_[Date].xlsx`
- Read from DCF tab
- Extract columns A-C (Assumption, Value, Source)
- Extract first 20 rows

**DCF Sensitivity Matrix** (Task 3 `Sensitivity Analysis` tab)
- Read from Sensitivity Analysis tab
- Extract full sensitivity matrix
- WACC values as row headers
- Terminal growth rates as column headers

**Scenario Comparison Table** (Task 2 `Scenarios` tab)
- Read from Scenarios tab
- Extract full scenario table
- Metrics as row headers (Revenue, EBITDA, Margins, etc.)
- Columns: Bull, Base, Bear

**Other supporting tables to extract:**
- Cash flow statement
- Balance sheet highlights
- Key metrics dashboard
- Margin bridge
- Working capital schedule
- TAM sizing table
- Market share table

**Create all 12-20 tables with proper formatting.**

### Step 3: Write Quantitative Sections

These sections interpret the financial model.

**Write in this order:**

#### A. Financial Analysis (1,200-1,800 words)
- Analyze historical performance from model
- Discuss trends in revenue, margins, cash flow
- Reference specific charts and tables
- Lead with numbers

#### B. Projection Assumptions (2,000-3,000 words) ⭐ CRITICAL
- Follow detailed structure from Report Structure section above
- Must be product-by-product (8-12 points per product)
- Must be region-by-region (6-8 points per region)
- Must include margin, opex, capex, working capital assumptions
- **This section separates amateur from professional analysis**

#### C. Scenario Analysis (1,500-2,000 words) ⭐ CRITICAL
- Follow detailed structure from Report Structure section above
- Bull case: specific parameters, catalysts, probability, valuation
- Base case: most likely scenario with rationale
- Bear case: downside triggers and parameters
- Comparison table and analysis
- **Must have specific quantified parameters for each scenario**

#### D. Growth Drivers (800-1,200 words)
- 3-5 key drivers with quantified opportunities
- Timeline and milestones
- Evidence from model

#### E. Valuation Methodology (800-1,200 words)
- DCF explanation with assumptions
- Comparables rationale
- Precedent transactions (if applicable)
- Reconciliation and weighting
- Price target derivation

### Step 4: Write Synthesis Sections

**Write in this order:**

#### A. Investment Thesis (800-1,200 words)
- 3-5 key pillars
- Each pillar: 200-300 words
- Lead with key statistic
- Quantify financial impact
- Include timeline

#### B. Risk Assessment (600-900 words)
- Pull from Task 1 research document
- Organize into 4 categories
- 8-12 risks total
- Each risk: 50-100 words

#### C. Price Target & Recommendation (300-500 words)
- Final recommendation
- Price target with upside %
- Key catalysts with timeframes
- Key risks to target

#### D. Investment Summary (500-700 words) - WRITE LAST
- Page 1 content
- 3-4 detailed bullets with bold headers
- Complete synthesis of all findings
- **Write this section LAST after full analysis complete**

### Step 5: Integrate Company Content from Task 1

**CRITICAL INSTRUCTION**: Use Task 1 research document almost verbatim. DO NOT rewrite.

**The company research from Task 1 (6-8K words) is already professional, substantive analysis. Objective:**
1. **Reformat for Word** - Convert markdown to DOCX formatting
2. **Insert charts inline** - Add relevant charts from Task 4 throughout the text
3. **Minor style adjustments** - Ensure consistent formatting with rest of report

**Extract these sections from Task 1 research document:**
- Company description (800-1,200 words) → **Use verbatim, insert company overview charts**
- Company history (800-1,200 words) → **Use verbatim, insert timeline chart**
- Management bios (1,000-1,400 words) → **Use verbatim, insert org chart if available**
- Products & services (700-1,000 words) → **Use verbatim, insert product portfolio charts**
- Customers & GTM (500-700 words) → **Use verbatim, insert customer segmentation charts**
- Industry overview (800-1,200 words) → **Use verbatim, insert market size evolution charts**
- Competitive landscape (700-1,000 words) → **Use verbatim, insert competitive positioning charts**
- TAM analysis (500-700 words) → **Use verbatim, insert TAM sizing charts**
- Risk assessment (600-900 words) → **Use verbatim, format as Investment Thesis & Risks section**

**Chart Integration Strategy:**
- Every 200-300 words of text → Insert 1 chart
- Company 101 section (pages 6-17) should have 8-12 charts interspersed
- Place charts immediately after the paragraph that discusses the topic
- **Result**: Dense, visually rich pages (60-80% coverage)

### Step 6: Assemble DOCX Report

**CRITICAL**: Create actual DOCX file, NOT markdown.

**Assembly Order (Most Efficient):**

#### Phase A: Create Structure & Add Page 1
1. Create DOCX document
2. Set up professional styling (fonts, headers, footers)
3. Create Page 1 - Investment Summary (write this LAST after all analysis complete)
4. Add Table of Contents placeholder

#### Phase B: Copy Task 1 Content + Insert Charts
**This is 40-50% of the report - mostly copy/paste + chart insertion**

Use Claude's DOCX skill to:

1. **Initialize new DOCX document**
   - Create new Word document
   - Set professional styling (fonts, margins)

2. **Read Task 1 markdown file**
   - Use Read tool: `[Company]_Research_Document_[Date].md`
   - Identify sections by markdown headers (## Section Title)

3. **Extract and convert each section from Task 1 to Word format:**

**SECTION 1: Investment Thesis & Risks**
- Add heading: 'Investment Thesis & Risks' (level 1)
- Extract 'Risk Assessment' section from Task 1 markdown
- Convert markdown formatting to Word formatting (remove ##, **, etc.)
- Add paragraphs to Word document (split by blank lines)
- Add new 'Investment Thesis' heading (level 2)
- Write new investment thesis content (800-1,200 words based on all analysis)

**SECTION 2: Company 101 (Pages 6-17)**
Copy each section from Task 1 verbatim with formatting conversion:

- **Company Overview**
  - Add heading: 'Company Overview' (level 1)
  - Extract 'Company Overview' section from Task 1
  - Convert to Word paragraphs
  - Insert chart: `task4_charts/chart_05_company_overview.png` (6 inches wide)

- **Company History**
  - Add heading: 'Company History' (level 1)
  - Extract 'Company History' section from Task 1
  - Convert to Word paragraphs
  - Insert chart: `task4_charts/chart_06_company_timeline.png` (6 inches wide)

- **Management Team**
  - Add heading: 'Management Team' (level 1)
  - Extract 'Management Team' section from Task 1
  - Convert to Word paragraphs
  - Insert chart: `task4_charts/chart_07_org_structure.png` (5 inches wide)

- **Products & Services**
  - Add heading: 'Products & Services' (level 1)
  - Extract 'Products & Services' section from Task 1
  - Add first paragraph
  - Insert chart: `task4_charts/chart_08_product_portfolio.png` (6 inches wide)
  - Add remaining paragraphs

- **Customers & Go-to-Market**
  - Add heading: 'Customers & Go-to-Market' (level 1)
  - Extract section from Task 1
  - Convert to Word paragraphs
  - Insert chart: `task4_charts/chart_09_customer_segments.png` (6 inches wide)

- **Industry Overview**
  - Add heading: 'Industry Overview' (level 1)
  - Extract section from Task 1
  - Add first paragraph
  - Insert chart: `task4_charts/chart_10_market_size_evolution.png` (6 inches wide)
  - Add remaining paragraphs
  - Insert chart: `task4_charts/chart_11_industry_trends.png` (6 inches wide)

- **Competitive Landscape**
  - Add heading: 'Competitive Landscape' (level 1)
  - Extract section from Task 1
  - Add first paragraph
  - Insert chart: `task4_charts/chart_16_competitive_positioning.png` (6 inches wide)
  - Add remaining paragraphs
  - Insert chart: `task4_charts/chart_17_market_share.png` (5 inches wide)

- **Market Opportunity**
  - Add heading: 'Market Opportunity' (level 1)
  - Extract 'Market Opportunity' section from Task 1
  - Convert to Word paragraphs
  - Insert chart: `task4_charts/chart_15_TAM_sizing.png` (6 inches wide)

**Result after Phase B**: Pages 6-17 complete (~12 pages, 6-8K words, 8-12 charts embedded)

**Key Point**: Use DOCX skill to READ from Task 1's .md file and INSERT actual image files. No manual copy/paste required.

#### Phase C: Add Financial Analysis with Data from Task 2
**This requires NEW WRITING interpreting quantitative data**

Use Claude's DOCX and XLSX skills to:

**SECTION 3: Financial Analysis (Pages 18-30)**

1. **Add section heading: 'Financial Analysis' (level 1)**

2. **Historical Financial Analysis (1,200-1,800 words) - NEW WRITING**
   - Add heading: 'Historical Performance' (level 2)
   - Use XLSX skill to open `[Company]_Financial_Model_[Date].xlsx`
   - Read `Income Statement` tab to extract historical data
   - Read `Revenue Model` tab to extract revenue trends
   - Calculate key metrics (e.g., Revenue CAGR from 2020-2024)
   - Write analytical paragraphs interpreting the trends (1,200-1,800 words)
   - Lead with specific numbers: "Revenue grew from $XXM in 2020 to $XXM in 2024, representing a XX% CAGR. This growth was driven by..."
   - Insert chart: `task4_charts/chart_02_revenue_growth_trajectory.png` (6 inches wide)

3. **Create Table: Full Income Statement**
   - Add heading: 'Historical Income Statement' (level 3)
   - Use XLSX skill to extract entire Income Statement tab (40-50 rows)
   - Create Word table with all columns (historical years 2020A-2024A + projected 2025E-2029E)
   - Include all line items: Revenue, COGS, Gross Profit, Operating Expenses, EBITDA, Net Income, etc.

4. **Add mandatory charts and tables for Revenue breakdown:**
   - Insert chart: `task4_charts/chart_03_revenue_by_product.png` (6.5 inches wide) ⭐ MANDATORY
   - **Create Table: Revenue by Product (20-30 rows)**
     - Use XLSX skill to extract from Revenue Model tab (product section, typically rows 5-35)
     - Create Word table showing each product category with historical and projected years
     - Include columns: Product name, historical years, projected years, % of Total, YoY Growth

   - Insert chart: `task4_charts/chart_04_revenue_by_geography.png` (6.5 inches wide) ⭐ MANDATORY
   - **Create Table: Revenue by Geography (15-20 rows)**
     - Use XLSX skill to extract from Revenue Model tab (geography section, typically rows 40-60)
     - Create Word table showing each geographic region with historical and projected years

5. **Add additional financial charts:**
   - Insert chart: `task4_charts/chart_10_gross_margin_evolution.png` (6 inches wide)
   - Insert chart: `task4_charts/chart_11_ebitda_margin_progression.png` (6 inches wide)
   - Insert chart: `task4_charts/chart_12_free_cash_flow_trend.png` (6 inches wide)

6. **Projection Assumptions (2,000-3,000 words) ⭐ CRITICAL - NEW WRITING**
   - Add heading: 'Projection Assumptions' (level 2)
   - Use XLSX skill to read Scenarios tab to inform assumptions
   - Use XLSX skill to read Revenue Model tab for specific product/geography projections
   - Add heading: 'Revenue Assumptions by Product' (level 3)
   - Write detailed product-by-product assumptions (8-12 points per major product)
   - Write detailed region-by-region assumptions (6-8 points per major region)
   - Include margin, opex, capex, working capital assumptions
   - **Total: 2,000-3,000 words of specific, quantified assumptions**

7. **Scenario Analysis (1,500-2,000 words) ⭐ CRITICAL - NEW WRITING**
   - Add heading: 'Scenario Analysis' (level 2)
   - Use XLSX skill to extract scenario data from Scenarios tab
   - Extract Bull/Base/Bear parameters for key metrics (2029E Revenue, EBITDA Margin, etc.)
   - Write Bull Case (500-700 words): specific parameters, catalysts, probability, valuation
   - Write Base Case (300-500 words): most likely scenario with rationale
   - Write Bear Case (500-700 words): downside triggers, parameters, probability, valuation
   - Write Scenario Comparison (200-300 words)
   - Insert chart: `task4_charts/chart_14_scenario_comparison.png` (6 inches wide)
   - **Create Table: Scenario Comparison**
     - Use XLSX skill to extract from Scenarios tab
     - Create Word table with Bull/Base/Bear columns and key metrics as rows

8. **Growth Drivers (800-1,200 words) - NEW WRITING**
   - Add heading: 'Key Growth Drivers' (level 2)
   - Write 3-5 key drivers with specific quantified opportunities
   - Include timelines and milestones
   - Reference specific data from financial model

**Result after Phase C**: Pages 18-30 complete (~13 pages, 5-7K words, 7-8 charts, 6-8 tables)

**Key Point**: Use XLSX skill to READ data from Task 2's Excel file, use the data to inform NEW analytical writing, and use DOCX skill to create Word tables from Excel data.

#### Phase D: Add Valuation Analysis from Task 3
**Mix of copying Task 3 analysis + inserting data from Excel**

Use Claude's DOCX and XLSX skills to:

**SECTION 4: Valuation Analysis (Pages 31-40)**

1. **Add section heading: 'Valuation Analysis' (level 1)**

2. **Read Task 3 markdown file**
   - Use Read tool: `[Company]_Valuation_Analysis_[Date].md`
   - Identify sections by markdown headers: DCF Analysis, Comparable Companies, Price Target

3. **DCF Analysis section**
   - Add heading: 'DCF Analysis' (level 2)
   - Extract 'DCF Analysis' section from Task 3 markdown
   - Convert markdown to Word paragraphs
   - Insert chart: `task4_charts/chart_28_dcf_sensitivity_heatmap.png` (6 inches wide) ⭐ MANDATORY

   - **Create Table: DCF Key Assumptions**
     - Add heading: 'DCF Key Assumptions' (level 3)
     - Use XLSX skill to open `[Company]_Financial_Model_[Date].xlsx`
     - Read DCF tab (columns A-C, first 20 rows: Assumption, Value, Source)
     - Create Word table from extracted data

   - **Create Table: DCF Sensitivity Matrix**
     - Use XLSX skill to read Sensitivity Analysis tab
     - Extract full sensitivity matrix (WACC values as rows, terminal growth as columns)
     - Create Word table showing valuation at different parameter combinations

   - Insert chart: `task4_charts/chart_29_dcf_waterfall.png` (6 inches wide)

4. **Comparable Companies section**
   - Add heading: 'Comparable Companies Analysis' (level 2)
   - Extract 'Comparable Companies' section from Task 3 markdown
   - Convert markdown to Word paragraphs

   - **Create Table: Comparable Companies ⭐ CRITICAL**
     - Add heading: 'Comparable Companies' (level 3)
     - Use XLSX skill to read Comparable Companies tab
     - Extract full table including:
       - 5-10 peer companies plus target company
       - Statistical summary rows (Maximum, 75th Percentile, Median, 25th Percentile, Minimum)
     - Create Word table with all columns: Ticker, Market Cap, EV/Revenue (LTM & NTM), EV/EBITDA (LTM & NTM), P/E (NTM), Revenue Growth, EBITDA Margin
     - **Verify statistical summary is included in table**

   - Insert chart: `task4_charts/chart_31_peer_multiples_comparison.png` (6 inches wide)

5. **Valuation Summary**
   - Insert chart: `task4_charts/chart_32_valuation_football_field.png` (6.5 inches wide) ⭐ MANDATORY

   - **Create Table: Valuation Summary**
     - Use XLSX skill to read Valuation Summary tab
     - Extract valuation methods (DCF, Comps, Precedent Transactions if applicable)
     - Create Word table showing: Method, Low Case, Base Case, High Case, Weight, Weighted Value

6. **Price Target & Recommendation**
   - Add heading: 'Price Target and Recommendation' (level 2)
   - Extract 'Price Target' section from Task 3 markdown
   - Convert markdown to Word paragraphs
   - Should include: Final recommendation (BUY/HOLD/SELL), price target with % upside, key catalysts, key risks

**Result after Phase D**: Pages 31-40 complete (~10 pages, 3-4K words, 5-6 charts, 4-5 tables)

**Key Point**: Use Read tool for Task 3's .md file to get written analysis, and use XLSX skill to READ from Task 3's Excel tabs (which were added to Task 2's model file) to create quantitative tables.

#### Phase E: Add Appendices & Finalize

Use Claude's DOCX skill to:

**SECTION 5: Appendices (Pages 41-50)**

1. **Data Sources & References**
   - Add heading: 'Data Sources & References' (level 1)
   - List all sources used throughout the report
   - Organize by category:
     - SEC Filings (10-K, 10-Q, DEF 14A, 8-K with EDGAR links)
     - Earnings Calls (with transcript links)
     - Company Materials (investor presentations, press releases)
     - Industry Reports (Gartner, Forrester, etc.)
     - News Articles
   - **CRITICAL**: All URLs must be clickable hyperlinks (not plain text)
   - Include dates for all sources

2. **Additional Tables**
   - Add heading: 'Additional Tables' (level 1)
   - Add extended financial projections
   - Add detailed assumptions tables
   - Add any supporting tables that didn't fit in main sections

#### Phase F: Write Page 1 Investment Summary
**NOW write Page 1 - after all analysis complete**
- INITIATING COVERAGE header
- Rating box
- 3-4 detailed bullets synthesizing entire report
- Financial summary table
- Stock price chart

#### Phase G: Add Table of Contents & Page Numbers
- Auto-generate TOC
- Add page numbers to all pages

**Key formatting requirements:**
- Professional fonts (Calibri, Arial, or similar)
- Proper headers and footers with page numbers
- Section breaks between major sections
- Embed all 25-35 charts inline throughout text
- Insert all 12-20 tables inline with text
- **All URLs as clickable hyperlinks** (NOT plain text)
- **60-80% page density** - Every page has text AND visuals

**Visual Density Strategy:**
```
Good page layout example:
┌─────────────────────────────┐
│ Section Header              │
│ Text paragraph (200 words)  │
│ [Chart embedded]            │
│ Text paragraph (200 words)  │
│ [Table embedded]            │
│ Text paragraph (200 words)  │
│ [Chart embedded]            │
└─────────────────────────────┘

BAD - Avoid:
- Full page with only one chart
- Multiple pages of pure text
- Charts grouped at end of sections
```

**Result**: 30-50 page report that is text-dense with illustrating images throughout

---

## File Operations Summary

**Throughout the entire assembly process, use Claude's DOCX and XLSX skills with actual file operations:**

**Reading Input Files:**
- ✓ Use Read tool: `[Company]_Research_Document_[Date].md` - Read Task 1 research
- ✓ Use XLSX skill: Open `[Company]_Financial_Model_[Date].xlsx` and read tabs - Extract tables from Task 2/3
- ✓ Use Read tool: `[Company]_Valuation_Analysis_[Date].md` - Read Task 3 analysis
- ✓ Use DOCX skill: Insert images from `task4_charts/chart_XX.png` files

**Writing Output File:**
- ✓ Use DOCX skill: Create new Word document
- ✓ Use DOCX skill: Add paragraphs (text from input .md files)
- ✓ Use DOCX skill: Create tables (data from Excel files read via XLSX skill)
- ✓ Use DOCX skill: Insert images (chart .png files)
- ✓ Use DOCX skill: Save final file as `[Company]_Initiation_Report_[Date].docx`

**Do NOT manually copy/paste. Use Claude's built-in skills to:**
1. Read from .md files (Task 1, Task 3) using Read tool
2. Read from .xlsx files (Task 2 with Task 3 tabs) using XLSX skill
3. Read from .png files (Task 4) as image files
4. Write to .docx file (Task 5 output) using DOCX skill

This approach is efficient, reproducible, and ensures all data flows correctly from source files to final report.

### Step 7: Quality Check

**Run comprehensive verification:**

```
═══════════════════════════════════════════════════════════
REPORT QUALITY CHECKLIST
═══════════════════════════════════════════════════════════

LENGTH REQUIREMENTS:
- [ ] Report is 30-50 pages (count: ____ pages)
- [ ] Word count is 10,000-15,000 (count: ____ words)
- [ ] 25-35 charts embedded (count: ____ charts)
- [ ] 12-20 tables included (count: ____ tables)

PAGE 1 FORMAT:
- [ ] "INITIATING COVERAGE" header present
- [ ] Thesis-focused title (not generic)
- [ ] Rating box complete with all elements
- [ ] Stock price chart (Figure 1) embedded
- [ ] 3-4 detailed bullets with ■ character
- [ ] Each bullet has **bold header** + 3-5 sentences
- [ ] Financial summary table included
- [ ] Years noted as "A" (actual) and "E" (estimate)

SECTION WORD COUNTS:
- [ ] Investment Thesis: 800-1,200 words ✓
- [ ] Risk Assessment: 600-900 words ✓
- [ ] Company Description: 800-1,200 words ✓
- [ ] Management Bios: 1,000-1,400 words (300-400 per exec for 3-4 execs) ✓
- [ ] Products & Services: 700-1,000 words ✓
- [ ] Financial Analysis: 1,200-1,800 words ✓
- [ ] **Projection Assumptions: 2,000-3,000 words ✓** ⭐ CRITICAL
- [ ] **Scenario Analysis: 1,500-2,000 words ✓** ⭐ CRITICAL
- [ ] Growth Drivers: 800-1,200 words ✓
- [ ] Valuation Methodology: 800-1,200 words ✓

MANDATORY CHARTS (4 TOTAL):
- [ ] Revenue by Product (stacked area) embedded ⭐
- [ ] Revenue by Geography (stacked bar) embedded ⭐
- [ ] DCF Sensitivity (heatmap) embedded ⭐
- [ ] Valuation Football Field embedded ⭐

MANDATORY TABLES:
- [ ] Page 1 financial summary table
- [ ] Full income statement (40-50 line items)
- [ ] Revenue by product table (20-30 rows)
- [ ] Revenue by geography table (15-20 rows)
- [ ] Comparable companies table with statistical summary ⭐
- [ ] DCF assumptions table
- [ ] Scenario comparison table
- [ ] Additional 5-13 tables

CITATIONS & HYPERLINKS:
- [ ] All figures have source lines
- [ ] All tables have source lines
- [ ] All URLs are clickable hyperlinks (NOT plain text)
- [ ] Test 5-10 random hyperlinks to verify they work
- [ ] Data Sources & References page included
- [ ] All sources have dates

DATA ACCURACY:
- [ ] All numbers match financial model exactly
- [ ] Revenue figures consistent across all tables/text
- [ ] Price target matches valuation analysis
- [ ] All growth rates calculated correctly
- [ ] All percentages sum to 100% where applicable

CONTENT REUSE (CRITICAL):
- [ ] Task 1 content used almost verbatim (not rewritten)
- [ ] Company 101 sections (pages 6-17) copied from Task 1 with only formatting changes
- [ ] Writing effort focused on quantitative sections (financial analysis, projections, scenarios)

VISUAL DENSITY (CRITICAL):
- [ ] Every page has BOTH text AND visuals (not pure text pages)
- [ ] Charts interspersed throughout (not grouped at end)
- [ ] Average 1+ chart per page (30-50 pages = 25-35+ charts)
- [ ] Charts appear every 200-300 words of text
- [ ] 60-80% page density achieved across entire report

FORMATTING:
- [ ] No markdown syntax visible (no #, ##, **, etc.)
- [ ] Professional fonts throughout
- [ ] Headers and footers present
- [ ] Page numbers present
- [ ] Section breaks appropriate
- [ ] Charts embedded (not just file paths)
- [ ] Tables formatted professionally

WRITING QUALITY:
- [ ] Lead with numbers (not generic statements)
- [ ] Use "vs." not "versus"
- [ ] Quantify everything
- [ ] Professional tone throughout
- [ ] No typos or grammatical errors
- [ ] Specific examples (not vague statements)

═══════════════════════════════════════════════════════════
FINAL VERIFICATION
═══════════════════════════════════════════════════════════

IF ALL ITEMS CHECKED: ✓ READY FOR DELIVERY

IF ANY ITEMS UNCHECKED: ✗ FIX BEFORE DELIVERY

═══════════════════════════════════════════════════════════
```

**IF ANY ITEM FAILS, DO NOT DELIVER. Fix before proceeding.**

---

## Writing Style Guidelines

### Lead with Numbers (CRITICAL)

✓ **CORRECT**: "Revenue increased 150% YoY to $250M in Q4 2024, driven by..."
✗ **INCORRECT**: "The company saw strong revenue growth this quarter..."

✓ **CORRECT**: "EBITDA margin expanded 500bps to 30% vs. 25% in FY2023"
✗ **INCORRECT**: "EBITDA margin expanded versus the prior year"

✓ **CORRECT**: "Market share increased 3 percentage points to 18% vs. 15% in 2023"
✗ **INCORRECT**: "Market share increased compared to last year"

✓ **CORRECT**: "Management expects 40-50% revenue growth in FY2025E"
✗ **INCORRECT**: "Management expects strong revenue growth"

### Professional Writing Standards

- **Front-load**: Most important information first
- **Data-driven**: Lead with numbers and metrics
- **Specific**: Concrete examples, not generic statements
- **Objective**: Present facts, acknowledge risks
- **Confident**: State views clearly with supporting evidence
- **Active voice**: "We estimate revenue will reach $500M"
- **Precise**: Avoid "might", "could", "possibly"

### Number Formatting

**Consistency:**
- Billions: $X.XB (e.g., "$2.5B")
- Millions: $XXXM (e.g., "$250M")
- Always specify: YoY, QoQ, CAGR
- Basis points for small margin changes: "500bps"
- Year format: "2024A" (actual), "2025E" (estimate)

### Use "vs." not "versus"
✓ **CORRECT**: "Gross margin of 65% vs. 60% in prior year"
✗ **INCORRECT**: "Gross margin of 65% versus 60%"

---

## Common Pitfalls to Avoid

**⚠️ MOST COMMON MISTAKE: TAKING SHORTCUTS DUE TO LENGTH**

Many reports fail because they use placeholders like "details would be included here" or "see model for data" instead of actually writing/extracting the content. **DO NOT DO THIS.** Write every section in full. Extract every table. Embed every chart. Use whatever tokens are needed.

1. **Rewriting Task 1 content**: DO NOT rewrite the 6-8K words from Task 1. Use almost verbatim - just reformat and add charts. Focus writing effort on quantitative sections (projections, scenarios, valuation).
2. **Sparse pages**: Every page must have BOTH text AND visuals. Target 60-80% page density. Insert charts every 200-300 words.
3. **Grouping charts at end**: Charts must be interspersed throughout text, not grouped. Place chart immediately after paragraph discussing that topic.
4. **Writing in markdown**: Use DOCX format, NOT markdown
5. **Skipping Page 1 format**: Must follow exact institutional format
6. **Generic bullets**: Page 1 bullets need bold headers + specific data
7. **Short sections**: Must meet minimum word counts
8. **Thin assumptions**: Projection Assumptions MUST be 2,000-3,000 words with product-by-product and region-by-region detail
9. **Vague scenarios**: Must have specific parameters for Bull/Base/Bear
10. **Plain text URLs**: All citations must be clickable hyperlinks
11. **Missing statistical summary**: Comps table must have max/75th/median/25th/min
12. **Charts not embedded**: All 25-35 charts must be IN document, not just referenced
13. **Numbers don't match model**: Verify all figures against source
14. **Skipping verification**: Quality check is NOT optional

---

## Success Criteria

A successful equity research report should:

1. **Meet all length requirements**
   - 30-50 pages (MINIMUM 30)
   - 10,000-15,000 words (MINIMUM 10,000)
   - 25-35 charts embedded
   - 12-20 tables included

2. **Have properly formatted Page 1**
   - "INITIATING COVERAGE" header
   - Rating box, analyst info, chart, bullets, table

3. **Meet all section word count minimums**
   - Especially Projection Assumptions (2,000-3,000) ⭐
   - And Scenario Analysis (1,500-2,000) ⭐

4. **Include all 4 mandatory charts**
   - Revenue by product (stacked area) ⭐
   - Revenue by geography (stacked bar) ⭐
   - DCF sensitivity (heatmap) ⭐
   - Valuation football field ⭐

5. **Have management bios**
   - 300-400 words each for 3-4 key executives

6. **Include comprehensive comps table**
   - With statistical summary (max/75th/median/25th/min)

7. **Have all citations as clickable hyperlinks**
   - Test multiple links to verify they work

8. **Be professionally formatted**
   - 60-80% page density
   - No markdown syntax visible
   - Charts and tables embedded properly

9. **Have numbers matching model exactly**
   - Verify all figures against Excel model

10. **Enable informed investment decision**
    - Client should understand company, valuation, risks
    - Should be indistinguishable from JPM/GS/MS research

---

## Output Files

**Primary Deliverable:**
`[Company]_Initiation_Report_[Date].docx`

**Example**: `Tesla_Initiation_Report_2024-10-27.docx`

**Supporting Deliverable:**
`[Company]_Financial_Model_[Date].xlsx` (from Task 2)

**Both files should be packaged together for final delivery.**

---

## Final Note

This is the culmination of all equity research work from Tasks 1-4. The output should be:
- **Comprehensive**: 30-50 pages covering all aspects
- **Professional**: Indistinguishable from major investment bank research
- **Actionable**: Enables reader to make informed investment decision
- **Publication-ready**: Can be delivered directly to clients

**Standard**: JPMorgan, Goldman Sachs, Morgan Stanley institutional equity research.

**Quality bar**: Client-ready initiation report suitable for publication.

---

## 🔥 FINAL REMINDER: NO SHORTCUTS, NO COMPROMISES

**Use whatever tokens are needed to deliver a complete, professional report.**

This is not a draft. This is not a summary. This is not an outline. This is the **FINAL PUBLICATION-READY REPORT**.

- Write every section in full (10,000-15,000 words minimum)
- Embed every chart (all 25-35 charts throughout)
- Extract and include every table (12-20 tables minimum)
- Copy all Company 101 content from Task 1 verbatim (6-8K words)
- Write detailed projection assumptions (2,000-3,000 words)
- Write comprehensive scenario analysis (1,500-2,000 words)
- Achieve 30-50 pages minimum with 60-80% page density

**If running low on tokens, that's expected and acceptable for this task. Keep going.**

This represents the complete professional work product. Deliver institutional-quality research worthy of a $1M+ investment decision.

### Referencia: references/valuation-methodologies.md

# Valuation Methodologies for Equity Research

This reference document provides comprehensive guidance on the three primary valuation methodologies used in equity research: Discounted Cash Flow (DCF), Trading Comparables, and Precedent Transactions.

## Table of Contents

1. [Discounted Cash Flow (DCF) Analysis](#discounted-cash-flow-dcf-analysis)
2. [Trading Comparables Analysis](#trading-comparables-analysis)
3. [Precedent Transactions Analysis](#precedent-transactions-analysis)
4. [Valuation Reconciliation](#valuation-reconciliation)

---

## Discounted Cash Flow (DCF) Analysis

### Overview

DCF analysis values a company based on the present value of its projected future cash flows. This is considered the most theoretically sound valuation method as it's based on fundamental value creation.

### Step-by-Step DCF Process

#### 1. Historical Financial Analysis
- Collect 3-5 years of historical financials
- Calculate historical FCF = EBIT(1-Tax Rate) + D&A - CapEx - Change in NWC
- Analyze historical growth rates and margins
- Identify trends and cyclicality

#### 2. Build Revenue Projections (5-10 years)
**Approaches:**
- **Top-down**: Start with market size (TAM) → Market share → Revenue
- **Bottom-up**: Units sold × Price per unit
- **Hybrid**: Combine multiple drivers

**Key Considerations:**
- Management guidance and historical growth
- Industry growth rates and market trends
- Competitive dynamics and market share evolution
- Product pipeline and new market opportunities
- Macroeconomic factors

#### 3. Project Operating Expenses
- **COGS**: As % of revenue (analyze historical margins)
- **SG&A**: Often semi-fixed; model as % of revenue with scale effects
- **R&D**: Critical for tech/pharma; model as % of revenue
- **D&A**: Based on CapEx assumptions

**Calculate EBIT** = Revenue - COGS - Operating Expenses

#### 4. Calculate Unlevered Free Cash Flow
```
EBIT
× (1 - Tax Rate)
= NOPAT (Net Operating Profit After Tax)
+ Depreciation & Amortization
- Capital Expenditures
- Increase in Net Working Capital
= Unlevered Free Cash Flow (UFCF)
```

**CapEx Assumptions:**
- Maintenance CapEx: Required to maintain current operations (typically 2-4% of revenue)
- Growth CapEx: Required for expansion
- Consider industry benchmarks and company guidance

**Net Working Capital:**
- NWC = (Accounts Receivable + Inventory) - Accounts Payable
- Model as % of revenue or days (DSO, DIO, DPO)
- An increase in NWC is a use of cash

#### 5. Determine Terminal Value

**Method A: Perpetuity Growth Method**
```
Terminal Value = FCF(final year) × (1 + g) / (WACC - g)
```
- g = perpetual growth rate (typically 2-3%, not exceeding GDP growth)
- Use when company has reached stable, mature growth

**Method B: Exit Multiple Method**
```
Terminal Value = EBITDA(final year) × Exit Multiple
```
- Exit multiple based on current trading comps
- More appropriate for cyclical businesses

#### 6. Calculate Weighted Average Cost of Capital (WACC)

```
WACC = (E/V × Cost of Equity) + (D/V × Cost of Debt × (1 - Tax Rate))
```

**Cost of Equity (using CAPM):**
```
Cost of Equity = Risk-Free Rate + Beta × Equity Risk Premium
```
- Risk-Free Rate: 10-year Treasury yield
- Beta: Regression of stock returns vs. market (or use comparable beta)
- Equity Risk Premium: Historical average ~5-6%

**Cost of Debt:**
```
Cost of Debt = Risk-Free Rate + Credit Spread
```
- Use company's current borrowing rate or implied from bonds
- Adjust for credit rating if no bonds outstanding

**Capital Structure:**
- E/V = Market value of equity / Total value
- D/V = Market value of debt / Total value
- Use target capital structure, not current (if significantly different)

#### 7. Discount Cash Flows to Present Value

```
PV = Σ [FCFt / (1 + WACC)^t] + [Terminal Value / (1 + WACC)^n]
```

#### 8. Calculate Enterprise Value and Equity Value

```
Enterprise Value = PV of Projected FCF + PV of Terminal Value
Less: Net Debt (Total Debt - Cash)
Plus: Non-operating Assets
Less: Minority Interest
Less: Preferred Stock
= Equity Value

Price Per Share = Equity Value / Diluted Shares Outstanding
```

### DCF Sensitivity Analysis

Always perform sensitivity analysis on key variables:

1. **Two-way sensitivity table**: WACC vs. Terminal Growth Rate
2. **Revenue growth scenarios**: Base / Bull / Bear cases
3. **Margin assumptions**: Operating leverage scenarios
4. **Terminal multiple sensitivity**: If using exit multiple method

**Example Sensitivity Table:**
```
           Terminal Growth Rate
WACC      2.0%    2.5%    3.0%
8.0%      $45     $48     $52
9.0%      $40     $43     $46
10.0%     $36     $39     $41
```

### Common DCF Pitfalls to Avoid

1. **Double-counting growth**: Don't project high growth without corresponding investment (CapEx, NWC)
2. **Unrealistic terminal growth**: Should not exceed long-term GDP growth
3. **Ignoring cyclicality**: Normalize earnings for cyclical businesses
4. **Wrong cash flow definition**: Use unlevered FCF, not net income
5. **Inconsistent assumptions**: Match discount rate to cash flows (unlevered FCF → WACC)

---

## Trading Comparables Analysis

### Overview

Trading comps values a company based on how similar companies are valued in the public markets. This reflects current market sentiment and relative valuation.

### Step-by-Step Comps Process

#### 1. Select Comparable Companies

**Selection Criteria:**
- Same industry/sector (primary criterion)
- Similar business model and revenue streams
- Comparable size (market cap, revenue)
- Similar growth profile and margins
- Similar end markets and geographies

**Typical Universe:**
- Start with 8-15 companies
- Remove companies with unique circumstances
- Final set of 5-10 companies

#### 2. Gather Financial Information

**Required Data:**
- Current stock price and shares outstanding
- Latest fiscal year financial statements
- Next-year (NTM) estimates from consensus
- Historical growth rates

**Calculate Market Metrics:**
- Market Cap = Share Price × Shares Outstanding
- Enterprise Value = Market Cap + Debt + Minority Interest + Preferred - Cash
- Net Debt = Total Debt - Cash & Equivalents

#### 3. Calculate Valuation Multiples

**Enterprise Value Multiples:**
- **EV/Revenue**: Good for early-stage/high-growth companies
- **EV/EBITDA**: Most common; good for capital-intensive businesses
- **EV/EBIT**: Useful when D&A varies significantly

**Equity Value Multiples:**
- **P/E (Price/Earnings)**: Most widely used
- **P/B (Price/Book)**: Good for financial institutions
- **P/S (Price/Sales)**: For unprofitable companies

**Calculate for:**
- Last Twelve Months (LTM) - historical
- Next Twelve Months (NTM) - forward-looking (preferred)

#### 4. Analyze and Select Multiples

**Create Comparable Company Table:**

| Company | Market Cap | EV/Revenue | EV/EBITDA | EV/EBIT | P/E (NTM) | Revenue Growth | EBITDA Margin |
|---------|-----------|------------|-----------|---------|-----------|----------------|---------------|
| Comp A  | $10B      | 3.5x       | 12.0x     | 18.0x   | 22.0x     | 15%            | 28%           |
| Comp B  | $8B       | 3.0x       | 10.5x     | 16.0x   | 19.0x     | 12%            | 27%           |
| ...     | ...       | ...        | ...       | ...     | ...       | ...            | ...           |
| Median  | -         | **3.2x**   | **11.0x** | **17.0x** | **20.5x** | 13%            | 27.5%         |

**Adjustments:**
- Remove outliers (typically >2 standard deviations)
- Consider using median instead of mean (less affected by outliers)
- Weight multiples if some comps are more comparable
- Adjust for differences in growth, margins, risk

#### 5. Apply Multiples to Target Company

**Example Calculation:**
```
Target Company NTM EBITDA = $500M
Selected EV/EBITDA Multiple = 11.0x
Implied Enterprise Value = $500M × 11.0x = $5,500M

Less: Net Debt = $1,000M
Equity Value = $4,500M

Shares Outstanding = 100M
Implied Price Per Share = $45.00
```

#### 6. Select Appropriate Multiple

**Choose based on:**
- **EV/Revenue**: High-growth, unprofitable companies (tech, biotech pre-profit)
- **EV/EBITDA**: Most common; capital-intensive industries (manufacturing, telecom)
- **P/E**: Profitable companies with stable cap structure (consumer, retail)
- **Sector-specific**: P/B for banks, EV/Production for oil & gas, EV/Subscriber for media

### Premium/Discount Analysis

Apply premiums or discounts based on:
- **Growth premium**: Higher growth → higher multiple
- **Profitability**: Higher margins → higher multiple
- **Size**: Larger companies typically trade at premium (liquidity)
- **Market position**: Market leaders → premium
- **Geographic**: Developed vs. emerging markets

---

## Precedent Transactions Analysis

### Overview

Precedent transactions values a company based on prices paid for similar companies in M&A transactions. This reflects control premiums and strategic value.

### Step-by-Step Process

#### 1. Identify Relevant Transactions

**Selection Criteria:**
- Same or similar industry
- Similar size (within 0.5x to 2x target's size)
- Similar business characteristics
- Recent transactions (last 3-5 years preferred)
- Announced and closed deals (avoid withdrawn deals)

**Typical Universe:**
- 5-10 transactions minimum
- Focus on recent deals (weight more recent higher)

#### 2. Gather Transaction Details

**Required Information:**
- Transaction date (announcement and close)
- Acquisition price and structure (cash, stock, mixed)
- Target's financials at time of transaction
- Strategic rationale and synergies
- Control premium paid

**Sources:**
- SEC filings (S-4, 8-K, proxy statements)
- Press releases and investor presentations
- M&A databases (CapIQ, FactSet, Bloomberg)

#### 3. Calculate Transaction Multiples

**Same multiples as trading comps, but based on transaction value:**

```
Transaction Value = Equity Purchase Price + Assumed Debt - Cash Acquired

EV/Revenue (LTM) = Transaction Value / Target's LTM Revenue
EV/EBITDA (LTM) = Transaction Value / Target's LTM EBITDA
EV/EBIT (LTM) = Transaction Value / Target's LTM EBIT
```

**Calculate Control Premium:**
```
Control Premium = (Offer Price - Unaffected Price) / Unaffected Price
```
- Unaffected Price = Target's stock price 1-2 days before announcement
- Typical range: 20-40%

#### 4. Analyze Precedent Transactions

**Create Precedent Transactions Table:**

| Date | Target | Acquirer | Deal Value | EV/Revenue | EV/EBITDA | Premium | Rationale |
|------|--------|----------|------------|------------|-----------|---------|-----------|
| Q1'24 | CompX | BuyerA | $5.0B | 4.0x | 14.0x | 35% | Market consolidation |
| Q3'23 | CompY | BuyerB | $3.5B | 3.5x | 12.5x | 28% | Strategic fit |
| Median | - | - | - | **3.8x** | **13.0x** | **31%** | - |

#### 5. Apply to Target Company

**Important Considerations:**
- Precedent multiples typically higher than trading comps (include control premium)
- Adjust for differences in transaction rationale
- Consider market conditions at time of transactions vs. current
- Weight recent transactions more heavily

**Example Calculation:**
```
Target Company LTM EBITDA = $450M
Selected EV/EBITDA Multiple = 13.0x (precedent)
vs Trading Comps Multiple = 11.0x

Implied EV (Precedent) = $450M × 13.0x = $5,850M
Implied EV (Trading) = $450M × 11.0x = $4,950M

Implied Control Premium = $5,850M / $4,950M - 1 = 18%
```

### Adjustments to Transaction Multiples

**Consider adjusting for:**
- **Market conditions**: Bull vs. bear market (M&A activity levels)
- **Deal structure**: Strategic vs. financial buyer
- **Synergies**: Transactions with high synergies command premiums
- **Competitive dynamics**: Single vs. multiple bidders
- **Time value**: Older transactions less relevant

---

## Valuation Reconciliation

### Creating a Valuation Bridge

Present all three methods in a single framework:

**Example Valuation Summary:**

| Method | Enterprise Value | Equity Value | Price/Share | Weight | Implied Value |
|--------|------------------|--------------|-------------|--------|---------------|
| DCF Analysis | $5,200M | $4,200M | $42.00 | 50% | $21.00 |
| Trading Comps | $5,500M | $4,500M | $45.00 | 30% | $13.50 |
| Precedent Trans. | $5,850M | $4,850M | $48.50 | 20% | $9.70 |
| **Weighted Avg** | - | - | **$44.20** | - | **$44.20** |

### Weighting the Methods

**Typical Weighting:**
- **DCF**: 40-60% (fundamental value, but assumes accuracy of projections)
- **Trading Comps**: 25-40% (reflects current market sentiment)
- **Precedent Trans.**: 15-25% (less relevant unless M&A likely)

**Adjust weights based on:**
- **Confidence in forecasts**: Higher confidence → higher DCF weight
- **Market conditions**: Bull/bear market affects comps reliability
- **M&A likelihood**: Higher if company in play or industry consolidating
- **Company maturity**: Mature companies → higher weight on comps; growth → higher DCF weight

### Valuation Range

Always present a valuation range, not a point estimate:

**Approach:**
- **Base Case**: Most likely scenario
- **Bull Case**: Optimistic assumptions (revenue growth, margins)
- **Bear Case**: Conservative assumptions

**Example:**
```
Bear Case: $38 - $40
Base Case: $42 - $46
Bull Case: $48 - $52

Recommendation: BUY with target price of $45 (midpoint of base case)
```

### Sanity Checks

**Cross-check valuation with:**
1. **Historical multiples**: Is current valuation in line with history?
2. **Peer comparison**: Justified premium/discount vs. peers?
3. **Implied growth**: What growth is market pricing in?
4. **Implied returns**: IRR from current price to target price
5. **Market cap analysis**: Does total market cap make sense?

---

## Conclusion

Using all three valuation methods provides a robust framework for determining fair value:

- **DCF** provides intrinsic value based on fundamentals
- **Trading Comps** reflects current market valuation
- **Precedent Transactions** indicates M&A value and control premium

The key is to understand the assumptions driving each method and to present a well-reasoned valuation range that considers multiple scenarios and methodologies.


---

## SKILL: insider-trading

- Fuente: `staskh/trading_skills` → `.claude/skills/insider-trading` (MIT)
- Cuándo usarla: Get insider trading activity (SEC Form 4 filings) for one or more stocks. Use when user asks about insider buying/selling, executive transactions, insider sentiment, or Form 4 activity.
- Código: extraer `code/staskh_trading_skills.tar` y usar `.claude/skills/insider-trading/` (insider_trading.py)

# Insider Trading

Fetch recent insider transactions from Yahoo Finance (SEC Form 4 data).

## Instructions

> **Note:** If `uv` is not installed or `pyproject.toml` is not found, replace `uv run python` with `python` in all commands below.

```bash
uv run python scripts/insider_trading.py SYMBOLS [--days DAYS]
```

## Arguments

- `SYMBOLS` - Single ticker or comma-separated list (e.g., `NVDA` or `NVDA,PLTR,GOOG`)
- `--days` - Trailing days to look back (default: 90)

## Output

Returns JSON with:
- `transactions` - List of insider trades with insider name, role, transaction type, shares, price, value, date, ownership type
- `summary` - Net sentiment (`net_buying`, `net_selling`, `neutral`), buy/sell counts and values

For multiple symbols, results are ranked by net buying value (most buying first).

## Use Cases

- *"Show me insider buys for NVDA in the last 90 days"*
- *"Compare insider activity across NVDA, PLTR, GOOG"*
- *"Which of these stocks has the most insider selling recently?"*

## Dependencies

- `yfinance`


## Timezone

All timestamps and time-based calculations must use the `America/New_York` timezone. All JSON output must include `generated_at` (NY time string) and `data_delay` fields.


---

## SKILL: institutional-flow-tracker

- Fuente: `tradermonty/claude-trading-skills` → `skills/institutional-flow-tracker` (MIT)
- Cuándo usarla: Use this skill to track institutional investor ownership changes and portfolio flows using 13F filings data. Analyzes hedge funds, mutual funds, and other institutional holders to identify stocks with significant smart money accumulation or distribution. Helps discover stocks before major moves by following where sophisticated investors are deploying capital.
- Código: extraer `code/tradermonty_claude-trading-skills.tar` y usar `skills/institutional-flow-tracker/` (requirements.txt, analyze_single_stock.py, data_quality.py, fmp_client.py, track_institution_portfolio.py, track_institutional_flow.py)

# Institutional Flow Tracker

## Overview

This skill tracks institutional investor activity through 13F SEC filings to identify "smart money" flows into and out of stocks. By analyzing quarterly changes in institutional ownership, you can discover stocks that sophisticated investors are accumulating before major price moves, or identify potential risks when institutions are reducing positions.

**Key Insight:** Institutional investors (hedge funds, pension funds, mutual funds) manage trillions of dollars and conduct extensive research. Their collective buying/selling patterns often precede significant price movements by 1-3 quarters.

## Prerequisites

- **FMP API Key:** Set `FMP_API_KEY` environment variable or pass `--api-key` to scripts
- **Python 3.9+:** Required for running analysis scripts
- **Dependencies:** `pip install requests` (scripts handle missing dependencies gracefully)

## When to Use This Skill

Use this skill when:
- Validating investment ideas (checking if smart money agrees with your thesis)
- Discovering new opportunities (finding stocks institutions are accumulating)
- Risk assessment (identifying stocks institutions are exiting)
- Portfolio monitoring (tracking institutional support for your holdings)
- Following specific investors (tracking Warren Buffett, Cathie Wood, etc.)
- Sector rotation analysis (identifying where institutions are rotating capital)

**Do NOT use when:**
- Seeking real-time intraday signals (13F data has 45-day reporting lag)
- Analyzing micro-cap stocks (<$100M market cap with limited institutional interest)
- Looking for short-term trading signals (<3 months horizon)

## Data Sources & Requirements

### Required: FMP API Key

This skill uses Financial Modeling Prep (FMP) API to access 13F filing data:

**Setup:**
```bash
# Set environment variable (preferred)
export FMP_API_KEY=your_key_here

# Or provide when running scripts
python3 scripts/track_institutional_flow.py --api-key YOUR_KEY

FMP transport (rate limiting, single 429 retry, apikey header auth so the key never appears in a URL) is owned by the vendored generated `scripts/fmp_client.py` (Issue #495).
```

**API Tier Requirements:**
- **Free Tier:** 250 requests/day (sufficient for analyzing 20-30 stocks quarterly)
- **Paid Tiers:** Higher limits for extensive screening

**13F Filing Schedule:**
- Filed quarterly within 45 days after quarter end
- Q1 (Jan-Mar): Filed by mid-May
- Q2 (Apr-Jun): Filed by mid-August
- Q3 (Jul-Sep): Filed by mid-November
- Q4 (Oct-Dec): Filed by mid-February

## Analysis Workflow

### Step 1: Identify Stocks with Significant Institutional Changes

Execute the main screening script to find stocks with notable institutional activity:

**Quick scan (top 50 stocks by institutional change):**
```bash
python3 scripts/track_institutional_flow.py \
  --top 50 \
  --min-change-percent 10
```

**Sector-focused scan:**
```bash
python3 scripts/track_institutional_flow.py \
  --sector Technology \
  --min-institutions 20
```

**Custom screening:**
```bash
python3 scripts/track_institutional_flow.py \
  --min-market-cap 2000000000 \
  --min-change-percent 15 \
  --top 100 \
  --output institutional_flow_results.json
```

**Output includes:**
- Stock ticker and company name
- Current institutional ownership % (of shares outstanding)
- Quarter-over-quarter change in shares held
- Number of institutions holding
- Change in number of institutions (new buyers vs sellers)
- Top institutional holders

### Step 2: Deep Dive on Specific Stocks

For detailed analysis of a specific stock's institutional ownership:

```bash
python3 scripts/analyze_single_stock.py AAPL
```

**This generates:**
- Historical institutional ownership trend (8 quarters)
- Top 20 institutional holders with position changes
- Concentration analysis (top 10 holders' % of total institutional ownership)
- New / increased / decreased positions among the largest holders
- Data quality assessment with coverage-based reliability grade

**Key metrics to evaluate:**
- **Ownership %:** Higher institutional ownership (>70%) = more stability but limited upside
- **Ownership Trend:** Rising ownership = bullish, falling = bearish
- **Concentration:** High concentration (top 10 > 50%) = risk if they sell
- **Quality of Holders:** Presence of quality long-term investors (Berkshire, Fidelity) vs momentum funds

### Step 3: Track Specific Institutional Investors

> **Note:** `track_institution_portfolio.py` is **not yet implemented**. FMP API organizes
> institutional holder data by stock (not by institution), making full portfolio reconstruction
> impractical via this API alone.

**Alternative approach — use `analyze_single_stock.py` to check if a specific institution holds a stock:**
```bash
# Analyze a stock and look for a specific institution in the output
python3 institutional-flow-tracker/scripts/analyze_single_stock.py AAPL
# Then search the report for "Berkshire" or "ARK" in the Top 20 holders table
```

**For full institution-level portfolio tracking, use these external resources:**
1. **WhaleWisdom:** https://whalewisdom.com (free tier available, 13F portfolio viewer)
2. **SEC EDGAR:** https://www.sec.gov/cgi-bin/browse-edgar (official 13F filings)
3. **DataRoma:** https://www.dataroma.com (superinvestor portfolio tracker)

### Step 4: Interpretation and Action

Read the references for interpretation guidance:
- `references/13f_filings_guide.md` - Understanding 13F data and limitations
- `references/institutional_investor_types.md` - Different investor types and their strategies
- `references/interpretation_framework.md` - How to interpret institutional flow signals

**Signal Strength Framework:**

**Strong Bullish (Consider buying):**
- Institutional ownership increasing >15% QoQ
- Number of institutions increasing >10%
- Quality long-term investors adding positions
- Low current ownership (<40%) with room to grow
- Accumulation happening across multiple quarters

**Moderate Bullish:**
- Institutional ownership increasing 5-15% QoQ
- Mix of new buyers and sellers, net positive
- Current ownership 40-70%

**Neutral:**
- Minimal change in ownership (<5%)
- Similar number of buyers and sellers
- Stable institutional base

**Moderate Bearish:**
- Institutional ownership decreasing 5-15% QoQ
- More sellers than buyers
- High ownership (>80%) limiting new buyers

**Strong Bearish (Consider selling/avoiding):**
- Institutional ownership decreasing >15% QoQ
- Number of institutions decreasing >10%
- Quality investors exiting positions
- Distribution happening across multiple quarters
- Concentration risk (top holder selling large position)

### Step 5: Portfolio Application

**For new positions:**
1. Run institutional analysis on your stock idea
2. Look for confirmation (institutions also accumulating)
3. If strong bearish signals, reconsider or reduce position size
4. If strong bullish signals, gain confidence in thesis

**For existing holdings:**
1. Quarterly review after 13F filing deadlines
2. Monitor for distribution (early warning system)
3. If institutions are exiting, re-evaluate your thesis
4. Consider trimming if widespread institutional selling

**Screening workflow integration:**
1. Use Value Dividend Screener or other screeners to find candidates
2. Run Institutional Flow Tracker on top candidates
3. Prioritize stocks with institutional accumulation
4. Avoid stocks with institutional distribution

## Output Format

All analysis generates structured markdown reports saved to repository root:

**Filename convention:** `institutional_flow_analysis_<TICKER/THEME>_<DATE>.md`

**Report sections:**
1. Executive Summary (key findings)
2. Institutional Ownership Trend (current vs historical)
3. Top Holders and Changes
4. New Buyers vs Sellers
5. Concentration Analysis
6. Interpretation and Recommendations
7. Data Sources and Timestamp

## Data Reliability Grades

All analysis includes a **coverage-based reliability grade**:

- **Grade A:** A comparable prior quarter exists and the stock has **>= 50** institutional (13F) holders. Dense coverage, safe for ranking.
- **Grade B:** A comparable prior quarter exists and the stock has **>= 10** holders. Usable but thin — reference only.
- **Grade C:** No comparable prior quarter (change not measurable) or **< 10** holders. EXCLUDED from screening results.

The screening script (`track_institutional_flow.py`) automatically excludes Grade C stocks.
The single stock analysis (`analyze_single_stock.py`) displays the grade with appropriate warnings.

**Why coverage, not per-holder reconciliation:** Metrics are sourced from FMP's aggregate 13F
summary (`institutional-ownership/symbol-positions-summary`), which reconciles
quarter-over-quarter deltas across all filing managers **at source**. This replaces the retired
`/api/v3/institutional-holder` feed, which returned asymmetric per-holder lists across quarters
(e.g., 5,415 holders one quarter, 201 the next) and required client-side filtering to avoid
inflated percent changes. With the reconciled summary, the remaining quality signal that matters
in practice is **breadth** (how many managers hold the name) and whether a prior quarter exists
to measure change against — which is what the grade now reflects.

## Limitations and Caveats

**Data Lag:**
- 13F filings have 45-day reporting delay
- Positions may have changed since filing date
- Use as confirming indicator, not leading signal

**Coverage:**
- Only institutions managing >$100M are required to file
- Excludes individual investors and smaller funds
- International institutions may not file 13F

**Reporting Rules:**
- Only long equity positions reported (no shorts, options, bonds)
- Holdings as of quarter-end snapshot
- Some positions may be confidential (delayed reporting)

**Interpretation:**
- Correlation ≠ causation (stocks can fall despite institutional buying)
- Consider overall market environment and fundamentals
- Combine with technical analysis and other skills

## Advanced Use Cases

**Insider + Institutional Combo:**
- Look for stocks where both insiders AND institutions are buying
- Particularly powerful signal when aligned

**Sector Rotation Detection:**
- Track aggregate institutional flows by sector
- Identify early rotation trends before they appear in price

**Contrarian Plays:**
- Find quality stocks institutions are selling (potential value)
- Requires strong fundamental conviction

**Smart Money Validation:**
- Before major position, check if smart money agrees
- Gain confidence or find overlooked risks

## References

The `references/` folder contains detailed guides:

- **13f_filings_guide.md** - Comprehensive guide to 13F SEC filings, what they include, reporting requirements, and data quality considerations
- **institutional_investor_types.md** - Different types of institutional investors (hedge funds, mutual funds, pension funds, etc.), their typical strategies, and how to interpret their moves
- **interpretation_framework.md** - Detailed framework for interpreting institutional ownership changes, signal quality assessment, and integration with other analysis

## Script Parameters

### track_institutional_flow.py

Main screening script for finding stocks with significant institutional changes.

**Required:**
- `--api-key`: FMP API key (or set FMP_API_KEY environment variable)

**Optional:**
- `--top N`: Return top N stocks by institutional change (default: 50)
- `--min-change-percent X`: Minimum % change in institutional ownership (default: 10)
- `--min-market-cap X`: Minimum market cap in dollars (default: 1B)
- `--sector NAME`: Filter by specific sector
- `--min-institutions N`: Minimum number of institutional holders (default: 10)
- `--limit N`: Number of stocks to fetch from screener (default: 100). Lower values save API calls.
- `--output FILE`: Output JSON file path
- `--output-dir DIR`: Output directory for reports (default: reports/)
- `--sort-by FIELD`: Sort by 'ownership_change' or 'institution_count_change'

### analyze_single_stock.py

Deep dive analysis on a specific stock's institutional ownership.

**Required:**
- Ticker symbol (positional argument)
- `--api-key`: FMP API key (or set FMP_API_KEY environment variable)

**Optional:**
- `--quarters N`: Number of quarters to analyze (default: 8, i.e., 2 years)
- `--output FILE`: Output markdown report path
- `--output-dir DIR`: Output directory for reports (default: reports/)
- `--compare-to TICKER`: Compare institutional ownership to another stock (future feature)

### track_institution_portfolio.py

**Status: NOT YET IMPLEMENTED**

This script is a placeholder. It prints alternative resources (WhaleWisdom, SEC EDGAR, DataRoma) and exits with error code 1. FMP API organizes institutional holder data by stock (not by institution), making full portfolio reconstruction impractical.

For institution-specific portfolio tracking, use:
1. WhaleWisdom: https://whalewisdom.com (free tier available)
2. SEC EDGAR: https://www.sec.gov/cgi-bin/browse-edgar
3. DataRoma: https://www.dataroma.com

### Data Quality Module (data_quality.py)

Shared utility module used by both `track_institutional_flow.py` and `analyze_single_stock.py`:

- **coverage_grade():** Assigns A/B/C grade from holder breadth + prior-quarter availability
- **latest filed quarter helpers** (`current_quarter()`, `iter_quarters()`, `quarter_end_date()`): walk back to the most recent quarter with filed 13F data
- **normalize_holder():** Maps a `extract-analytics/holder` row to `{name, shares, change, is_new, is_sold_out}`
- **is_tradable_stock():** Filters out ETFs, funds, and inactive stocks
- **deduplicate_share_classes():** Removes BRK-A/B, GOOG/GOOGL duplicates

## Integration with Other Skills

**Value Dividend Screener + Institutional Flow:**
```
1. Run Value Dividend Screener to find candidates
2. For each candidate, check institutional flow
3. Prioritize stocks with rising institutional ownership
```

**US Stock Analysis + Institutional Flow:**
```
1. Run comprehensive fundamental analysis
2. Validate with institutional ownership trends
3. If institutions are selling, investigate why
```

**Portfolio Manager + Institutional Flow:**
```
1. Fetch current portfolio via Alpaca
2. Run institutional analysis on each holding
3. Flag positions with deteriorating institutional support
4. Consider rebalancing away from distribution
```

**Technical Analyst + Institutional Flow:**
```
1. Identify technical setup (e.g., breakout)
2. Check if institutional buying confirms
3. Higher conviction if both align
```

## Best Practices

1. **Quarterly Reviews:** Set calendar reminders for 13F filing deadlines
2. **Multi-Quarter Trends:** Look for sustained trends (3+ quarters), not one-time changes
3. **Quality Over Quantity:** Berkshire adding > 100 small funds adding
4. **Context Matters:** Rising ownership in a falling stock may be value investors catching a falling knife
5. **Combine Signals:** Never use institutional flow in isolation
6. **Update Your Data:** Re-run analysis each quarter as new 13Fs are filed

## Support & Resources

- FMP API Documentation: https://financialmodelingprep.com/developer/docs
- SEC 13F Filings Database: https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&type=13F
- Institutional Investor Database: https://whalewisdom.com (free tier available)

---

**Note:** This skill is designed for long-term investors (3-12 month horizon). For short-term trading, combine with technical analysis and other momentum indicators.

### Referencia: README.md

# Institutional Flow Tracker

Track institutional investor ownership changes and portfolio flows using 13F filings data to identify "smart money" accumulation and distribution patterns.

## Overview

Institutional Flow Tracker analyzes SEC 13F filings to discover stocks where sophisticated investors (hedge funds, mutual funds, pension funds) are accumulating or distributing positions. By following where institutional money flows, you can:

- **Discover opportunities** before they become mainstream
- **Validate investment ideas** by checking if smart money agrees
- **Get early warnings** when quality investors exit positions
- **Follow superinvestors** like Warren Buffett, Seth Klarman, Bill Ackman

**Key Insight:** Institutional investors manage trillions of dollars and conduct extensive research. Their collective actions often precede major price movements by 1-3 quarters.

## Features

✅ **Stock Screening** - Find stocks with significant institutional ownership changes (>10-15% QoQ)
✅ **Deep Dive Analysis** - Detailed quarterly trends, top holders, position changes for individual stocks
✅ **Institution Tracking** - Follow specific hedge funds/mutual funds portfolio moves
✅ **Signal Quality Framework** - Tier-based weighting system (superinvestors > active funds > index funds)
✅ **Multi-Quarter Trends** - Identify sustained accumulation/distribution (3+ quarters)
✅ **Concentration Analysis** - Assess ownership concentration risk
✅ **FMP API Integration** - Free tier (250 calls/day) sufficient for quarterly reviews

## Prerequisites

### Required: FMP API Key

This skill uses Financial Modeling Prep (FMP) API to access 13F filing data.

**Setup:**
```bash
# Set environment variable (recommended)
export FMP_API_KEY="your_key_here"

# Or provide via command-line when running scripts
python3 scripts/track_institutional_flow.py --api-key YOUR_KEY
```

**Get API Key:**
1. Visit: https://financialmodelingprep.com/developer/docs
2. Sign up for free account (250 requests/day)
3. Copy your API key

**API Usage:**
- Free tier: 250 requests/day (sufficient for analyzing 30-50 stocks quarterly)
- Each stock analysis uses 1-2 API calls
- Quarterly review workflow: ~50-100 API calls total

## Installation

No installation required beyond Python 3 and the `requests` library:

```bash
pip install requests
```

## Usage

### 1. Screen for Stocks with Institutional Changes

Find stocks with significant institutional activity:

**Quick scan (top 50 stocks):**
```bash
python3 institutional-flow-tracker/scripts/track_institutional_flow.py \
  --top 50 \
  --min-change-percent 10
```

**Sector-focused screening:**
```bash
python3 institutional-flow-tracker/scripts/track_institutional_flow.py \
  --sector Technology \
  --min-institutions 20
```

**Custom screening:**
```bash
python3 institutional-flow-tracker/scripts/track_institutional_flow.py \
  --min-market-cap 2000000000 \
  --min-change-percent 15 \
  --top 100 \
  --output institutional_results.json
```

**Output:** Markdown report with top accumulators/distributors, detailed metrics, interpretation guide

### 2. Deep Dive on Specific Stock

Comprehensive analysis of institutional ownership for a single stock:

```bash
python3 institutional-flow-tracker/scripts/analyze_single_stock.py AAPL
```

**Extended history (12 quarters):**
```bash
python3 institutional-flow-tracker/scripts/analyze_single_stock.py MSFT --quarters 12
```

**Output:** Detailed report with quarterly trends, new/increased/decreased/closed positions, concentration analysis

### 3. Track Specific Institutional Investors

Follow portfolio changes of specific hedge funds or investment firms:

```bash
# Track Warren Buffett's Berkshire Hathaway
python3 institutional-flow-tracker/scripts/track_institution_portfolio.py \
  --cik 0001067983 \
  --name "Berkshire Hathaway"

# Track Cathie Wood's ARK Investment Management
python3 institutional-flow-tracker/scripts/track_institution_portfolio.py \
  --cik 0001579982 \
  --name "ARK Investment Management"
```

**Finding CIK (Central Index Key):**
- Search SEC EDGAR: https://www.sec.gov/cgi-bin/browse-edgar
- Or use FMP API institutional search

**Output:** Current portfolio holdings, new positions, exits, largest changes

## Signal Interpretation Framework

### Strong Buy Signal (95th percentile)

**Criteria:**
- Institutional ownership increasing >15% QoQ
- 3+ consecutive quarters of accumulation
- Multiple Tier 1/2 investors buying (clustering score >60)
- Quality long-term investors adding positions

**Action:** BUY with conviction (2-5% portfolio position)

### Moderate Buy Signal (75th percentile)

**Criteria:**
- Institutional ownership increasing 7-15% QoQ
- 2 consecutive quarters of accumulation
- Mix of quality buyers

**Action:** BUY with moderate conviction (1-3% position)

### Neutral Signal

**Criteria:**
- Institutional ownership change <5% QoQ
- No clear trend
- Mixed buyer/seller activity

**Action:** HOLD or decide based on other factors

### Moderate/Strong Sell Signal

**Criteria:**
- Institutional ownership decreasing 7-15% QoQ (moderate) or >15% (strong)
- 2-3+ consecutive quarters of distribution
- Quality investors exiting

**Action:** TRIM/SELL positions, avoid new entries

## Institutional Investor Quality Tiers

**Tier 1 - Superinvestors (Weight: 3.0-3.5x):**
- Warren Buffett (Berkshire Hathaway)
- Seth Klarman (Baupost Group)
- Bill Ackman (Pershing Square)
- David Tepper (Appaloosa Management)
- Patient capital, long-term oriented, concentrated portfolios

**Tier 2 - Quality Active Managers (Weight: 2.0-2.5x):**
- Fidelity Management & Research
- T. Rowe Price Associates
- Dodge & Cox
- Wellington Management
- Research-driven, solid track records

**Tier 3 - Average Institutional (Weight: 1.0-1.5x):**
- Regional mutual funds
- Most pension funds
- Benchmark-aware, committee-driven

**Tier 4 - Passive/Mechanical (Weight: 0.0-0.5x):**
- Index funds (Vanguard, BlackRock, State Street)
- Momentum/quant funds
- No fundamental views, follow index/price action

## Workflow Examples

### Quarterly Portfolio Review

**Objective:** Monitor institutional support for your holdings

1. Run institutional analysis on each holding after 13F filing deadlines
2. Flag positions with deteriorating institutional support
3. Re-evaluate thesis for positions showing Strong Sell signals
4. Consider trimming/exiting if quality investors are distributing

**13F Filing Deadlines:**
- Q1 (Jan-Mar): Mid-May
- Q2 (Apr-Jun): Mid-August
- Q3 (Jul-Sep): Mid-November
- Q4 (Oct-Dec): Mid-February

### New Position Validation

**Objective:** Validate stock ideas with institutional data

1. Run fundamental analysis on stock candidate
2. Check institutional flow signal (accumulation or distribution?)
3. If Strong Buy signal: Gain confidence, initiate position
4. If Strong Sell signal: Reconsider or avoid
5. If Neutral: Decide based on fundamentals and technicals

### Smart Money Replication

**Objective:** Follow superinvestor portfolio moves

1. Track Berkshire Hathaway, Baupost, other Tier 1 investors quarterly
2. Identify new positions or significant increases
3. Research the stock to understand their thesis
4. Initiate positions in highest-conviction ideas

### Sector Rotation Detection

**Objective:** Identify early sector rotation trends

1. Calculate aggregate institutional flow by sector
2. Rank sectors by net institutional inflow/outflow
3. Compare to expected patterns based on economic cycle
4. Overweight sectors with institutional accumulation
5. Underweight/avoid sectors with distribution

## Integration with Other Skills

**Value Dividend Screener + Institutional Flow:**
```
1. Run Value Dividend Screener to find candidates
2. For each candidate, check institutional flow
3. Prioritize stocks with Strong Buy institutional signal
```

**US Stock Analysis + Institutional Flow:**
```
1. Run comprehensive fundamental analysis
2. Validate with institutional ownership trends
3. If institutions selling despite strong fundamentals: investigate discrepancy
```

**Portfolio Manager + Institutional Flow:**
```
1. Fetch current portfolio via Alpaca
2. Run institutional analysis on each holding quarterly
3. Flag positions with deteriorating institutional support
4. Rebalance away from Strong Sell signals
```

**Technical Analyst + Institutional Flow:**
```
1. Identify technical setup (e.g., breakout, basing pattern)
2. Check if institutional buying confirms
3. Higher conviction if both technical + institutional signals align
```

## Data Limitations

**Reporting Lag:**
- 13F filings due 45 days after quarter end
- Positions as of quarter-end snapshot
- Current positions may have changed since filing

**Coverage:**
- Only institutions managing >$100M file 13F
- Excludes individual investors and smaller funds
- Only long equity positions (no shorts, options, bonds)

**Best Practices:**
- Use as confirming indicator, not leading signal
- Look for multi-quarter trends (3+ quarters)
- Weight quality institutions heavily (Tier 1 > Tier 4)
- Combine with fundamental and technical analysis
- Update quarterly, not daily

## Reference Materials

The `references/` folder contains comprehensive guides:

- **13f_filings_guide.md** - Understanding 13F SEC filings, reporting requirements, data quality considerations, common pitfalls
- **institutional_investor_types.md** - Different investor types (hedge funds, mutual funds, etc.), their strategies, quality tiers, weighting framework
- **interpretation_framework.md** - Systematic approach to interpreting signals, decision trees, multi-factor integration

## Script Parameters Reference

### track_institutional_flow.py

**Required:**
- `--api-key` or FMP_API_KEY environment variable

**Optional:**
- `--top N` - Return top N stocks (default: 50)
- `--min-change-percent X` - Minimum % ownership change (default: 10)
- `--min-market-cap X` - Minimum market cap in dollars (default: 1B)
- `--sector NAME` - Filter by sector
- `--min-institutions N` - Minimum institutional holders (default: 10)
- `--sort-by FIELD` - Sort by ownership_change/institution_count_change/dollar_value_change
- `--output FILE` - Output JSON file

### analyze_single_stock.py

**Required:**
- Stock ticker symbol (positional argument)
- `--api-key` or FMP_API_KEY environment variable

**Optional:**
- `--quarters N` - Number of quarters to analyze (default: 8)
- `--output FILE` - Output markdown report path

### track_institution_portfolio.py

**Required:**
- `--cik CIK` - Central Index Key of institution
- `--name NAME` - Institution name for report
- `--api-key` or FMP_API_KEY environment variable

**Optional:**
- `--top N` - Show top N holdings (default: 50)
- `--output FILE` - Output markdown report path

## Notable Institutional Investors to Track

### Tier 1 Superinvestors

| Investor | CIK | Strategy | Track Because |
|----------|-----|----------|---------------|
| Berkshire Hathaway (Warren Buffett) | 0001067983 | Value/Quality | Long-term compounders, patient capital |
| Baupost Group (Seth Klarman) | 0001061768 | Deep Value | Distressed opportunities, contrarian |
| Pershing Square (Bill Ackman) | 0001336528 | Activist/Value | Catalytic events, concentrated bets |
| Appaloosa Management (David Tepper) | 0001079114 | Value | Contrarian, high conviction |
| Third Point (Dan Loeb) | 0001040273 | Event-Driven | Catalyst-driven, activism |

### Tier 2 Quality Active Managers

| Fund Family | CIK | Strategy | Track Because |
|-------------|-----|----------|---------------|
| Fidelity Management | 0000315066 | Growth & Value | Large analyst team, quality research |
| T. Rowe Price | 0001113169 | Growth | Bottom-up research, growth focus |
| Dodge & Cox | 0000922614 | Deep Value | Contrarian, value-oriented |
| ARK Investment (Cathie Wood) | 0001579982 | Disruptive Innovation | High-conviction tech/innovation bets |

## Support & Resources

- FMP API Documentation: https://financialmodelingprep.com/developer/docs
- SEC 13F Filings Database: https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&type=13F
- WhaleWisdom (free tier): https://whalewisdom.com

## License

Educational and research purposes. See repository license for details.

### Referencia: references/13f_filings_guide.md

# 13F Filings Comprehensive Guide

## What is a 13F Filing?

Form 13F is a quarterly report filed with the SEC by institutional investment managers with at least $100 million in assets under management (AUM). The form discloses their equity holdings as of the end of each calendar quarter.

### Legal Requirements

**Who Must File:**
- Investment advisors
- Banks
- Insurance companies
- Pension funds
- Hedge funds
- Other institutions managing >$100M in "13F securities"

**What Must Be Reported:**
- Long positions in US-listed equities
- Convertible bonds
- Exchange-traded options
- Shares held as of quarter-end date

**What is NOT Reported:**
- Short positions
- Non-US securities
- Private equity investments
- Fixed income (except convertibles)
- Cash positions
- Derivatives (except listed options)

**Filing Deadline:**
- Within 45 days after quarter end
- Q1 (ended March 31): Due by May 15
- Q2 (ended June 30): Due by August 14
- Q3 (ended September 30): Due by November 14
- Q4 (ended December 31): Due by February 14

### Key Data Points in 13F Filings

**For Each Holding:**
1. **Issuer Name** - Company name
2. **Ticker Symbol** - Stock ticker
3. **CUSIP** - Unique security identifier
4. **Shares Held** - Number of shares owned
5. **Market Value** - Dollar value of position (shares × price at quarter end)
6. **Investment Discretion** - Sole/Shared/None
7. **Voting Authority** - Sole/Shared/None

**Aggregate Data:**
- Total number of holdings
- Total portfolio value
- Portfolio concentration
- Sector allocation

## Understanding the Data

### Position Changes

**Types of Changes:**
1. **New Position** - Stock not held last quarter, now held
2. **Increased Position** - More shares than last quarter
3. **Decreased Position** - Fewer shares than last quarter
4. **Closed Position** - Stock held last quarter, now zero

**Calculating Changes:**
```
Shares Change = Current Quarter Shares - Previous Quarter Shares
% Change = (Shares Change / Previous Quarter Shares) × 100
Dollar Value Change = (Shares Change) × (Current Stock Price)
```

**Example:**
```
Previous Quarter: 1,000,000 shares of AAPL @ $150 = $150M
Current Quarter:  1,200,000 shares of AAPL @ $180 = $216M

Shares Change: +200,000 shares (+20%)
Dollar Value Change: +$66M (includes price appreciation + new purchases)
```

### Aggregate Institutional Ownership

**Portfolio-Level Metrics:**
- **Total Institutional Ownership %** = (Total Shares Held by All Institutions / Shares Outstanding) × 100
- **Number of Institutional Holders** = Count of unique institutions filing 13F with this stock
- **Ownership Concentration** = % held by top 10 institutions
- **Ownership Trend** = QoQ change in total institutional ownership %

**Typical Ownership Ranges:**
- **<20%** - Low institutional interest (micro/small caps, speculative stocks)
- **20-40%** - Below average (growth stocks, recent IPOs)
- **40-60%** - Average (most mid/large caps)
- **60-80%** - Above average (blue chips, dividend aristocrats)
- **>80%** - Very high (mature, stable companies)

## Data Quality Considerations

### Timing Lags

**Reporting Lag:**
- Position as of: Quarter-end date (e.g., March 31)
- Filing deadline: 45 days later (e.g., May 15)
- Data available: Mid-May onwards
- **Total lag:** 6-7 weeks from position date

**Real-World Impact:**
- Stock may have moved significantly since quarter-end
- Institutions may have already changed positions
- Use 13F data as confirming indicator, not real-time signal

### Confidential Treatment

**Form 13F-NT (Notice of Confidential Treatment):**
- Institutions can request delayed disclosure for certain positions
- Typically granted for 1-2 quarters to prevent front-running
- Common for large accumulations or activist positions

**Red Flags:**
- Sudden appearance of large positions (may have been confidential)
- Large institutions with unusually low reported AUM (hidden positions)

### Aggregation Issues

**Double Counting:**
- Same shares may be reported by multiple entities within same organization
- Example: Vanguard Group + Vanguard Index Funds + Vanguard ETF Trust
- Need to aggregate related entities for accurate institutional ownership

**Custodial vs Beneficial Ownership:**
- Some institutions hold shares as custodians (not beneficial owners)
- Example: State Street as custodian for pension funds
- Look for "voting authority" and "investment discretion" fields

## Common Pitfalls and How to Avoid Them

### Pitfall 1: Ignoring Price Changes

**Problem:**
- Institutional ownership % can decrease even if institutions hold same share count
- Happens when: Stock price falls, institution's AUM falls below reporting threshold

**Solution:**
- Track both share count changes AND ownership % changes
- Focus on share count for more accurate signal

**Example:**
```
Q1: Institution holds 1M shares, stock at $100, ownership = 5%
Q2: Institution holds 1M shares, stock at $50, ownership = 2.5%
Interpretation: No actual selling, just price decline affecting percentage
```

### Pitfall 2: Interpreting Passive Index Funds

**Problem:**
- Index funds must buy/sell based on index composition, not fundamental views
- Large inflows to index funds mechanically increase institutional ownership

**Solution:**
- Separate active managers from passive funds
- Weight active manager changes more heavily
- Track: ARK, Berkshire, Baupost > Vanguard Index Funds

**Active vs Passive Indicators:**
- Active: Concentrated portfolios (20-50 stocks), high conviction bets
- Passive: Diversified portfolios (500+ stocks), matching index weights

### Pitfall 3: Ignoring Institution Quality

**Problem:**
- Not all institutional investors are equal
- 100 small funds buying ≠ Warren Buffett buying

**Solution:**
- Tier institutions by track record and strategy alignment
- Weight Tier 1 (quality long-term investors) more heavily

**Institutional Tiers:**
- **Tier 1** (High conviction): Berkshire, Appaloosa, Baupost, Pershing Square
- **Tier 2** (Quality active): Fidelity, T. Rowe Price, Wellington
- **Tier 3** (Passive/momentum): Vanguard Index, State Street, momentum funds

### Pitfall 4: Overreacting to Single Quarter Changes

**Problem:**
- One quarter of buying/selling may not indicate trend
- Could be portfolio rebalancing, redemptions, or temporary factors

**Solution:**
- Look for multi-quarter trends (3+ quarters)
- Higher conviction when sustained accumulation/distribution
- One quarter = noise, three quarters = signal

**Trend Quality:**
```
Strong Signal (3+ quarters same direction):
Q1: +10% institutional ownership
Q2: +8% institutional ownership
Q3: +12% institutional ownership
Interpretation: Sustained accumulation, high conviction

Noise (inconsistent):
Q1: +10% institutional ownership
Q2: -5% institutional ownership
Q3: +3% institutional ownership
Interpretation: No clear trend, likely portfolio adjustments
```

## Advanced Analysis Techniques

### Flow Analysis

Track net shares added/removed across all institutions:

```
Net Institutional Flow = Sum(All Institutional Share Changes)
Flow Ratio = (Shares Added by Buyers) / (Shares Sold by Sellers)

Flow Ratio > 2.0 = Strong accumulation
Flow Ratio 1.5-2.0 = Moderate accumulation
Flow Ratio 0.8-1.2 = Neutral/Balanced
Flow Ratio 0.5-0.8 = Moderate distribution
Flow Ratio < 0.5 = Strong distribution
```

### Concentration Risk Analysis

**Herfindahl-Hirschman Index (HHI):**
```
HHI = Sum of (Each Institution's Ownership %)²

HHI < 1000 = Diversified ownership (low concentration risk)
HHI 1000-1800 = Moderate concentration
HHI > 1800 = High concentration (risk if top holder sells)
```

**Example:**
```
Top 3 holders: 15%, 12%, 10% of institutional ownership
HHI = 15² + 12² + 10² = 225 + 144 + 100 = 469 (low concentration)

Top 3 holders: 40%, 30%, 20% of institutional ownership
HHI = 40² + 30² + 20² = 1600 + 900 + 400 = 2900 (high concentration)
```

### New Buyers vs Sellers Analysis

**Quarterly Cohort Tracking:**
```
New Buyers = Institutions with zero shares last Q, non-zero this Q
Increasers = Institutions with more shares this Q
Decreasers = Institutions with fewer shares this Q
Exited = Institutions with shares last Q, zero this Q

Bull Signal: New Buyers > Exited AND Increasers > Decreasers
Bear Signal: Exited > New Buyers AND Decreasers > Increasers
```

### Smart Money Clustering

Identify when multiple quality investors accumulate simultaneously:

**Clustering Score:**
```
Score = Sum of (Institution Tier × % Position Change)

Tier 1 institutions: Weight = 3.0
Tier 2 institutions: Weight = 2.0
Tier 3 institutions: Weight = 1.0

Example:
Berkshire (Tier 1) +10% position = 3.0 × 10 = 30 points
Fidelity (Tier 2) +5% position = 2.0 × 5 = 10 points
Index Fund (Tier 3) +2% position = 1.0 × 2 = 2 points
Total Clustering Score = 42

Score > 50 = Strong smart money accumulation
Score 25-50 = Moderate accumulation
Score < 25 = Weak/no clustering
```

## Historical Success Patterns

### Pre-Breakout Accumulation

**Pattern:**
- Stock trading sideways for 2-4 quarters
- Institutional ownership quietly rising (10-20% increase)
- Stock breaks out 1-2 quarters after accumulation visible in 13F

**Example Stocks:**
- NVDA (2019): Institutions accumulated before AI boom
- TSLA (2019-2020): Steady institutional buying before 500% run

### Early Distribution Warning

**Pattern:**
- Stock in uptrend
- Institutional ownership declining for 2+ quarters
- Top-tier institutions exiting
- Stock peaks 1-2 quarters after distribution begins

**Example Stocks:**
- Dot-com stocks (1999-2000): Smart money exited before crash
- Housing stocks (2006-2007): Institutional distribution before crisis

## Integration with Fundamental Analysis

**Bullish Confirmation:**
- Strong fundamentals (revenue growth, margin expansion)
- Rising institutional ownership
- Quality investors adding positions
- **Action:** High conviction buy

**Bearish Warning:**
- Strong fundamentals but declining institutional ownership
- Quality investors exiting despite good numbers
- **Action:** Investigate further, may be hidden risks

**Value Opportunity:**
- Weak short-term fundamentals
- Stable/rising institutional ownership (value investors accumulating)
- **Action:** Contrarian opportunity if fundamentals inflect

**Avoid:**
- Weak fundamentals
- Declining institutional ownership
- Quality investors exiting
- **Action:** Stay away

## Regulatory Changes and Updates

**Current as of 2025:**
- Reporting threshold: $100M AUM
- Filing deadline: 45 days after quarter end
- Amendment rules: Allowed within filing period

**Proposed Changes (Monitor):**
- Potential reduction in filing deadline to 30 days
- Potential requirement to disclose short positions
- Potential reduction in AUM threshold to $50M

**Stay Updated:**
- SEC website: https://www.sec.gov/rules
- Industry news: Follow regulatory announcements

## Tools and Resources

**Official Sources:**
- SEC EDGAR Database: https://www.sec.gov/edgar/searchedgar/companysearch.html
- Form 13F instructions: https://www.sec.gov/pdf/form13f.pdf

**Third-Party Aggregators:**
- WhaleWisdom: https://whalewisdom.com (free tier available)
- DataRoma: https://www.dataroma.com (tracks superinvestors)
- Fintel: https://fintel.io (institutional ownership data)

**API Access:**
- FMP API: Institutional ownership endpoints
- SEC API: Direct access to filings (free, rate-limited)

## Summary: Using 13F Data Effectively

**Best Practices:**
1. ✅ Track multi-quarter trends, not single quarters
2. ✅ Focus on share count changes, not just ownership %
3. ✅ Weight quality institutions more heavily
4. ✅ Combine with fundamental analysis
5. ✅ Use as confirming indicator, not standalone signal
6. ✅ Update quarterly after filing deadlines

**What to Avoid:**
1. ❌ Don't assume 13F = real-time positions
2. ❌ Don't ignore passive fund flows
3. ❌ Don't overweight single institution moves
4. ❌ Don't use for short-term trading
5. ❌ Don't ignore price changes when calculating ownership
6. ❌ Don't forget about confidential treatment requests

**Expected Returns:**
- Academic studies show 13F-based strategies can generate 2-4% annual alpha
- Best results when combined with momentum and value factors
- Effectiveness highest in small/mid caps where information asymmetry is greater

### Referencia: references/institutional_investor_types.md

# Institutional Investor Types and Strategies

## Overview

Not all institutional investors are created equal. Understanding the different types of institutions, their investment strategies, time horizons, and motivations is critical for interpreting 13F filing changes. This guide categorizes institutional investors and explains how to weight their buy/sell signals.

## Major Categories of Institutional Investors

### 1. Hedge Funds

**Characteristics:**
- Active management with concentrated portfolios
- High turnover (often 100%+ annually)
- Performance-driven compensation (2% management + 20% performance fees)
- Flexible investment strategies (long/short, derivatives, leverage)

**Typical Time Horizon:** 3 months to 2 years

**Portfolio Structure:**
- 20-100 core positions
- High conviction bets (top 10 positions = 50-70% of portfolio)
- Willing to take large positions relative to AUM

**Investment Styles:**
- **Value/Deep Value:** Distressed assets, turnarounds, special situations
- **Growth:** High-growth companies, disruptive tech
- **Activist:** Catalyze change through board seats, proxy fights
- **Event-Driven:** M&A arbitrage, restructurings
- **Quantitative:** Algorithm-driven, factor-based
- **Macro:** Top-down, sector rotation, global trends

**Signal Interpretation:**

**Strong Signal (Weight: 3.0x):**
- **Top-tier hedge funds:** Berkshire Hathaway, Appaloosa, Baupost, Pershing Square, Third Point
- **Why:** Deep research, long-term oriented, willing to be contrarian
- **When they buy:** Often early, before institutional herd
- **When they sell:** May be ahead of trouble

**Moderate Signal (Weight: 2.0x):**
- **Mid-tier active managers:** Smaller hedge funds with solid track records
- **Why:** Still research-driven but less patient capital

**Weak Signal (Weight: 1.0x):**
- **Momentum/quant funds:** Tiger Cubs, momentum-driven strategies
- **Why:** Often follow trends rather than lead them
- **Caution:** May be last to buy (top signal) or first to panic sell

**Examples of Notable Hedge Funds:**

| Fund Name | CIK | Strategy | Best Known For | Weighting |
|-----------|-----|----------|----------------|-----------|
| Berkshire Hathaway | 0001067983 | Value/Quality | Warren Buffett, long-term compounders | 3.5x |
| Pershing Square | 0001336528 | Activist/Value | Bill Ackman, catalytic events | 3.0x |
| Baupost Group | 0001061768 | Deep Value | Seth Klarman, distressed opportunities | 3.0x |
| Appaloosa Management | 0001079114 | Value | David Tepper, contrarian bets | 3.0x |
| Third Point | 0001040273 | Event-Driven/Activist | Dan Loeb, catalyst-driven | 2.5x |
| Tiger Global | 0001167483 | Growth/Tech | Chase Coleman, high-growth tech | 2.0x |
| Renaissance Technologies | 0001037389 | Quantitative | Jim Simons, algorithmic trading | 1.5x |

### 2. Mutual Funds

**Characteristics:**
- Active management with diversified portfolios
- Lower turnover than hedge funds (20-50% annually)
- Must stay fully invested (typically 95%+ equity allocation)
- Fee pressure driving shift toward passive strategies

**Typical Time Horizon:** 1-5 years

**Portfolio Structure:**
- 50-200 holdings
- More diversified than hedge funds
- Sector constraints (often cannot exceed index weight by >5%)

**Investment Styles:**
- **Large-Cap Growth:** Fidelity Contrafund, T. Rowe Price Growth Stock
- **Large-Cap Value:** Dodge & Cox Stock Fund, American Funds Washington Mutual
- **Small-Cap Growth:** Baron Small Cap Fund
- **Dividend/Income:** Vanguard Dividend Growth

**Signal Interpretation:**

**Strong Signal (Weight: 2.5x):**
- **Quality active mutual funds:** Fidelity, T. Rowe Price, Dodge & Cox
- **Why:** Rigorous research process, patient capital
- **When they buy:** Methodical accumulation over multiple quarters
- **When they sell:** Often early warning of deteriorating fundamentals

**Moderate Signal (Weight: 1.5x):**
- **Typical mutual funds:** Regional funds, smaller fund families
- **Why:** Still research-driven but less differentiated

**Weak Signal (Weight: 0.5x):**
- **Closet indexers:** Funds that mimic index but charge active fees
- **Why:** Minimal value-add, primarily following index weights

**Examples of Notable Mutual Fund Families:**

| Fund Family | CIK | Strategy | Research Quality | Weighting |
|-------------|-----|----------|------------------|-----------|
| Fidelity Management & Research | 0000315066 | Growth & Value | Excellent, large analyst team | 2.5x |
| T. Rowe Price Associates | 0001113169 | Growth | Excellent, bottom-up research | 2.5x |
| Dodge & Cox | 0000922614 | Deep Value | Excellent, contrarian | 2.5x |
| Wellington Management | 0000105132 | Multi-strategy | Very Good | 2.0x |
| Capital Group (American Funds) | 0001007039 | Multi-manager | Very Good | 2.0x |
| Baron Capital | 0001047469 | Small/Mid Growth | Good | 2.0x |

### 3. Index Funds and ETFs

**Characteristics:**
- Passive management tracking indices
- Extremely low turnover (only when index composition changes)
- Must hold all index constituents
- Forced buyers/sellers based on index rules

**Typical Time Horizon:** Indefinite (hold until removed from index)

**Portfolio Structure:**
- Matches index exactly (S&P 500, Russell 2000, etc.)
- Hundreds to thousands of holdings
- No discretionary overweights/underweights

**Investment Styles:**
- **Broad Market:** SPY (S&P 500), VTI (Total Stock Market)
- **Sector:** XLK (Technology), XLE (Energy)
- **Factor:** QQQ (Nasdaq 100), IWM (Russell 2000)
- **Thematic:** ARK Innovation (actively managed but ETF structure)

**Signal Interpretation:**

**Weak Signal (Weight: 0.3x):**
- **Large index funds:** Vanguard, State Street, BlackRock index products
- **Why:** Mechanical buying/selling based on index rules and fund flows
- **When they buy:** Index inclusion, fund inflows (not fundamental view)
- **When they sell:** Index deletion, fund redemptions

**Zero Signal (Weight: 0.0x):**
- **Pure index trackers:** Changes driven entirely by index methodology
- **Ignore for analysis:** Provides no fundamental insight

**Special Case - ARK ETFs (Weight: 2.0x):**
- Actively managed despite ETF structure
- Cathie Wood's high-conviction disruptive innovation bets
- Treat like active mutual fund, not passive ETF

**Major Index Fund Providers:**

| Provider | CIK | AUM | Passive vs Active | Weighting |
|----------|-----|-----|-------------------|-----------|
| Vanguard Group (Index) | 0000102909 | $7T+ | 90% Passive | 0.3x |
| BlackRock (iShares) | 0001006249 | $3T+ | 80% Passive | 0.3x |
| State Street (SPDR) | 0001067983 | $1T+ | 90% Passive | 0.3x |
| ARK Investment Management | 0001579982 | $20B | 100% Active | 2.0x |

### 4. Pension Funds

**Characteristics:**
- Extremely long-term oriented (liabilities 20-30 years out)
- Conservative mandates with diversification requirements
- Large allocations to fixed income, alternatives
- Equity portion often outsourced to external managers

**Typical Time Horizon:** 10-30 years

**Portfolio Structure:**
- Thousands of holdings (extremely diversified)
- Target allocations by asset class (e.g., 60% stocks, 40% bonds)
- Rebalance mechanically to maintain targets

**Investment Styles:**
- **Public Pensions:** CalPERS, CalSTRS, New York State Common Retirement Fund
- **Corporate Pensions:** IBM Retirement Fund, GE Pension Trust
- **Endowments:** Harvard Management Company, Yale Investments Office

**Signal Interpretation:**

**Weak Signal (Weight: 0.8x):**
- **Most pension funds:** Slow-moving, diversified, often following consultant recommendations
- **Why:** Not differentiated investors, lag behind trends

**Moderate Signal (Weight: 2.0x):**
- **Top university endowments:** Harvard, Yale, Princeton
- **Why:** Sophisticated investment teams, access to best managers
- **David Swensen model:** Yale's approach influenced entire industry

**Examples:**

| Fund Name | CIK | Type | Quality | Weighting |
|-----------|-----|------|---------|-----------|
| CalPERS | 0001133228 | Public Pension | Average | 0.8x |
| Harvard Management Company | 0001082621 | University Endowment | Excellent | 2.0x |
| Yale Investments Office | 0001080232 | University Endowment | Excellent | 2.0x |
| Teacher Retirement System of Texas | 0001023859 | Public Pension | Average | 0.8x |

### 5. Insurance Companies

**Characteristics:**
- Conservative, liability-matching strategies
- Heavy fixed income allocation (regulatory capital requirements)
- Equity investments typically in blue chips, dividends
- Low turnover

**Typical Time Horizon:** 5-15 years

**Portfolio Structure:**
- Hundreds of holdings
- Focus on large-cap, dividend-paying stocks
- Avoid high-volatility growth stocks

**Investment Styles:**
- **Life Insurance:** MetLife, Prudential
- **Property & Casualty:** Berkshire Hathaway (reinsurance), Markel

**Signal Interpretation:**

**Weak Signal (Weight: 1.0x):**
- **Most insurance companies:** Conservative, follow rating agency guidance
- **Why:** Limited risk appetite, prefer safety over returns

**Strong Signal (Weight: 3.0x):**
- **Insurance-affiliated value investors:** Markel (Tom Gayner), Berkshire (special case)
- **Why:** Patient capital, value-oriented, long-term compounders

### 6. Banks and Trust Companies

**Characteristics:**
- Manage money on behalf of clients (wealth management, trusts)
- Report aggregate positions across all client accounts
- May include both discretionary and non-discretionary accounts

**Typical Time Horizon:** Varies by client (1-10 years)

**Portfolio Structure:**
- Thousands of holdings (reflecting diverse client base)
- Often includes model portfolios applied across clients

**Signal Interpretation:**

**Weak Signal (Weight: 0.5x):**
- **Most banks:** Reflect client preferences more than bank's views
- **Why:** Custodial nature, not proprietary investment decisions

**Moderate Signal (Weight: 1.5x):**
- **Private banks with discretionary mandates:** Goldman Sachs Asset Management, JPMorgan Asset Management
- **Why:** Some proprietary research, but still client-driven

## Institutional Investor Quality Tiers

### Tier 1: Superinvestors (Weight: 3.0-3.5x)

**Characteristics:**
- 20+ year track records beating market
- Patient capital, long-term orientation
- Concentrated portfolios indicating high conviction
- Willing to be contrarian

**List:**
1. Warren Buffett (Berkshire Hathaway)
2. Seth Klarman (Baupost Group)
3. David Tepper (Appaloosa Management)
4. Bill Ackman (Pershing Square)
5. Dan Loeb (Third Point)
6. Mohnish Pabrai (Pabrai Investment Funds)
7. Li Lu (Himalaya Capital)
8. Tom Gayner (Markel)

**When to Follow:**
- New positions: Investigate immediately
- Large increases: High conviction, validate thesis
- Exits: Warning sign, re-evaluate your holdings

### Tier 2: Quality Active Managers (Weight: 2.0-2.5x)

**Characteristics:**
- Solid long-term track records
- Research-driven process
- Reasonable turnover (20-60%)
- Institutional-grade due diligence

**List:**
1. Fidelity Management & Research
2. T. Rowe Price Associates
3. Dodge & Cox
4. Wellington Management
5. Capital Group (American Funds)
6. Baron Capital
7. ARK Investment Management (Cathie Wood)
8. Greenhaven Associates

**When to Follow:**
- Multi-quarter trends: Look for 3+ quarters same direction
- Cluster analysis: Multiple Tier 2 managers buying = strong signal
- Exits: Early warning system

### Tier 3: Average Institutional Investors (Weight: 1.0-1.5x)

**Characteristics:**
- Benchmark-aware (avoid large tracking error)
- Committee-driven decisions (slower, less nimble)
- Follow industry/sector trends
- Moderate research quality

**Examples:**
- Regional mutual fund families
- Mid-tier hedge funds
- Most pension funds
- Insurance company investment departments

**When to Follow:**
- Useful for confirming broad trends
- Less useful for individual stock picking
- Aggregate flow analysis (overall institutional sentiment)

### Tier 4: Passive and Mechanical (Weight: 0.0-0.5x)

**Characteristics:**
- No fundamental views
- Index-driven or rules-based
- High correlation to fund flows
- Forced buying/selling

**Examples:**
- Index funds (Vanguard, BlackRock, State Street index products)
- Quantitative funds with high turnover
- Momentum-driven strategies

**When to Follow:**
- Generally ignore for fundamental analysis
- Useful for understanding technical supply/demand
- Can create price dislocations (opportunity)

## Strategy-Specific Interpretation

### Value Investors (Berkshire, Baupost, Dodge & Cox)

**Buying Signal:**
- Often early (stock still falling)
- Multi-year time horizon
- Looking for margin of safety

**How to Interpret:**
- Don't expect immediate price action
- Validate their thesis with fundamental research
- Wait for catalyst or technical confirmation

**Selling Signal:**
- Often late (stock already appreciated)
- Selling into strength
- Taking profits after multi-year holds

### Growth Investors (Fidelity Contrafund, Baron, Tiger Global)

**Buying Signal:**
- Chasing proven growth stories
- Momentum component (buy on strength)
- Paying up for quality

**How to Interpret:**
- Stock may already have moved
- Validate growth trajectory is sustainable
- Watch for slowdown in growth rate

**Selling Signal:**
- Often early at first sign of deceleration
- Growth disappointment
- Momentum reversal

### Activist Investors (Pershing Square, Third Point, Elliot Management)

**Buying Signal:**
- Catalyst-driven (board changes, asset sales, buybacks)
- Concentrated positions (5-10% stakes)
- Public campaigns (13D filings, letters)

**How to Interpret:**
- High potential returns if catalyst realized
- Higher risk (activists don't always win)
- Timeframe: 1-3 years for catalyst to play out

**Selling Signal:**
- Catalyst achieved
- Taking profits after successful campaign
- Activist fight lost

### Momentum/Quantitative Funds (Renaissance, AQR)

**Buying Signal:**
- Trend-following
- Factor-driven (value, momentum, quality)
- Short-term oriented

**How to Interpret:**
- Confirms technical strength
- May reverse quickly
- Don't overweight this signal

**Selling Signal:**
- Momentum breakdown
- Factor signal reversal
- Can accelerate declines

## Institutional Clustering Signals

### Strong Bullish: Quality Investor Clustering

**Pattern:**
- 3+ Tier 1 or Tier 2 investors buying simultaneously
- Sustained accumulation (2+ quarters)
- Increasing position sizes (not just maintenance)

**Example:**
```
Stock XYZ - Q3 2024 Institutional Activity:
- Berkshire: New position, 5% of portfolio
- Dodge & Cox: Increased existing position by 30%
- Baupost: New position, 3% of portfolio
- Fidelity Contrafund: Increased position by 15%

Clustering Score: (3.5×5) + (2.5×30) + (3.0×3) + (2.5×15) = 17.5 + 75 + 9 + 37.5 = 139
Interpretation: Very strong accumulation by quality investors
```

**Action:** High conviction buy if fundamentals support thesis

### Moderate Bullish: Broad Institutional Accumulation

**Pattern:**
- Rising institutional ownership across many Tier 2-3 investors
- Index fund flows also positive
- Gradual, sustained trend

**Interpretation:** Consensus building, mainstream acceptance

**Action:** Consider buying if not overvalued

### Neutral: Mixed Signals

**Pattern:**
- Some quality investors buying, others selling
- Similar number of increasers vs decreasers
- Net change near zero

**Interpretation:** No clear institutional consensus

**Action:** Look to other factors (fundamentals, technicals)

### Moderate Bearish: Quality Investors Exiting

**Pattern:**
- 2-3 Tier 1 or Tier 2 investors reducing/closing positions
- Tier 3 investors still buying (lagging indicators)
- Early stage of trend

**Interpretation:** Smart money getting out, warning sign

**Action:** Re-evaluate thesis, consider trimming

### Strong Bearish: Widespread Distribution

**Pattern:**
- 3+ Tier 1/2 investors exiting
- Sustained distribution (2+ quarters)
- Only Tier 4 (passive) buyers remaining

**Interpretation:** Serious fundamental concerns

**Action:** Sell or avoid, investigate for hidden risks

## Time Horizon Alignment

### Long-Term Investors (Your time horizon: 3+ years)

**Focus on:**
- Tier 1 superinvestors (Berkshire, Baupost)
- Value-oriented mutual funds (Dodge & Cox)
- University endowments

**Ignore:**
- Momentum funds
- Short-term traders
- Index fund flows

### Medium-Term Investors (Your time horizon: 1-3 years)

**Focus on:**
- Quality growth mutual funds (Fidelity, T. Rowe Price)
- Tier 2 hedge funds
- Activist investors

**Monitor:**
- Tier 1 superinvestors (for major themes)
- Aggregate institutional flow

### Short-Term Traders (Your time horizon: <1 year)

**Focus on:**
- Recent quarter changes (not multi-year trends)
- Momentum funds
- Aggregate institutional flow (technical signal)

**Note:** 13F data less useful for short-term trading due to 45-day lag

## Practical Application: Institutional Investor Scorecard

**For Each Stock, Calculate:**

```
Institutional Quality Score =
  (Tier 1 Holders × 3.5) +
  (Tier 2 Holders × 2.5) +
  (Tier 3 Holders × 1.0) +
  (Tier 4 Holders × 0.3)

Institutional Flow Score =
  (Tier 1 Buyers × 3.5) - (Tier 1 Sellers × 3.5) +
  (Tier 2 Buyers × 2.5) - (Tier 2 Sellers × 2.5) +
  (Tier 3 Buyers × 1.0) - (Tier 3 Sellers × 1.0)

Combined Score = Institutional Quality Score + Institutional Flow Score

Score > 50: Strong institutional support
Score 25-50: Moderate institutional support
Score 0-25: Weak institutional support
Score < 0: Institutional distribution underway
```

**Example Calculation:**

```
Stock ABC Analysis:

Tier 1 Holders: 2 (Berkshire, Baupost)
Tier 2 Holders: 5 (Fidelity, T. Rowe Price, Dodge & Cox, Wellington, Baron)
Tier 3 Holders: 20
Tier 4 Holders: 50 (mostly index funds)

Quality Score = (2 × 3.5) + (5 × 2.5) + (20 × 1.0) + (50 × 0.3)
             = 7 + 12.5 + 20 + 15 = 54.5

Recent Changes (Q3 2024):
Tier 1 Buyers: 1 (Baupost increased 20%)
Tier 2 Buyers: 3 (Fidelity +10%, Baron +15%, new buyer +5%)
Tier 1 Sellers: 0
Tier 2 Sellers: 1 (T. Rowe Price -5%)

Flow Score = (1 × 3.5) - 0 + (3 × 2.5) - (1 × 2.5)
          = 3.5 + 7.5 - 2.5 = 8.5

Combined Score = 54.5 + 8.5 = 63

Interpretation: Strong institutional support with ongoing accumulation
Action: High conviction buy if fundamentals align
```

## Summary: Institutional Investor Weighting Guide

**High Weight (3.0-3.5x):**
- Berkshire Hathaway, Baupost, Pershing Square, Third Point
- Value-oriented with long track records
- Contrarian, patient capital

**Moderate Weight (2.0-2.5x):**
- Fidelity, T. Rowe Price, Dodge & Cox, Wellington, ARK
- Quality active managers
- Research-driven

**Low Weight (1.0-1.5x):**
- Average mutual funds, most pension funds
- Committee-driven, benchmark-aware

**Minimal/Zero Weight (0.0-0.5x):**
- Index funds, momentum funds
- Mechanical, no fundamental views

**When in Doubt:**
- Weight quality over quantity
- Multi-quarter trends over single quarter
- Active over passive
- Concentrated portfolios over diversified

### Referencia: references/interpretation_framework.md

# Institutional Flow Interpretation Framework

## Overview

This framework provides a systematic approach to interpreting institutional ownership changes and converting 13F filing data into actionable investment signals. Use this as a decision tree for analyzing stocks discovered through institutional flow tracking.

## Signal Quality Assessment Matrix

### Dimension 1: Change Magnitude

**Strong Change (High Signal Quality):**
- Institutional ownership change: >15% QoQ
- Number of institutions change: >10 net new or exited
- Dollar value change: >$100M net flow
- **Quality:** Unmistakable signal, warrants immediate attention

**Moderate Change (Medium Signal Quality):**
- Institutional ownership change: 5-15% QoQ
- Number of institutions change: 3-10 net change
- Dollar value change: $25M-$100M net flow
- **Quality:** Meaningful signal, validate with other factors

**Weak Change (Low Signal Quality):**
- Institutional ownership change: <5% QoQ
- Number of institutions change: <3 net change
- Dollar value change: <$25M net flow
- **Quality:** Noise, likely portfolio adjustments or rebalancing

### Dimension 2: Consistency (Multi-Quarter Trend)

**Sustained Trend (High Quality):**
- 3+ quarters in same direction
- Accelerating magnitude (Q1: +5%, Q2: +8%, Q3: +12%)
- Consistent across market environments
- **Quality:** High conviction signal

**Emerging Trend (Medium Quality):**
- 2 consecutive quarters in same direction
- Stable magnitude
- **Quality:** Developing signal, monitor next quarter

**Single Quarter (Low Quality):**
- Only 1 quarter of change
- May reverse next quarter
- **Quality:** Inconclusive, wait for confirmation

**Inconsistent (No Signal):**
- Flip-flopping between quarters
- No clear direction
- **Quality:** Noise, ignore

### Dimension 3: Institution Quality Mix

**High Quality Mix (Weight 3.0x):**
- Dominated by Tier 1 superinvestors (Berkshire, Baupost, etc.)
- Multiple quality value investors agreeing
- Long-term oriented capital
- **Interpretation:** Strong validation

**Medium Quality Mix (Weight 2.0x):**
- Mix of Tier 2 active mutual funds
- Some quality participants
- Mostly research-driven
- **Interpretation:** Moderate validation

**Low Quality Mix (Weight 0.5x):**
- Dominated by passive index funds
- Momentum/quant funds
- Following price action
- **Interpretation:** Weak validation, likely late to trend

### Dimension 4: Concentration of Changes

**Clustered Buying/Selling (High Quality):**
- Multiple quality institutions moving same direction simultaneously
- Coordinated timing (not literally, but similar conclusions)
- High clustering score (>50 using framework from institutional_investor_types.md)
- **Interpretation:** Independent research reaching same conclusion = high conviction

**Scattered Activity (Medium Quality):**
- Mix of buyers and sellers
- No clear consensus
- Clustering score 20-50
- **Interpretation:** Divergent views, less clear signal

**Single Institution (Low Quality):**
- Only one significant mover
- Others flat or opposite
- Clustering score <20
- **Interpretation:** Idiosyncratic, institution-specific reason

## Comprehensive Signal Interpretation Framework

### Level 1: Strong Buy Signal (95th percentile)

**Criteria (ALL must be met):**
1. **Magnitude:** Institutional ownership increasing >15% QoQ
2. **Consistency:** 3+ consecutive quarters of accumulation
3. **Quality:** Clustering score >60 (multiple Tier 1/2 investors buying)
4. **Concentration:** Rising institutional concentration (top 10 holders increasing %)
5. **Type:** Quality investors adding, not just index funds
6. **Fundamental Support:** Revenue/earnings growth positive
7. **Price Action:** Stock underperformed or neutral (not already up 50%+)

**Interpretation:**
- Smart money accumulating before broader market recognition
- High probability of significant price appreciation in next 1-4 quarters
- Likely catalysts being anticipated by institutions

**Action:**
- **New position:** BUY with conviction (2-5% portfolio position)
- **Existing position:** ADD to position
- **Risk management:** Normal position sizing, standard stop-loss

**Historical Success Rate:** ~75-80% positive returns over 12 months

**Example Pattern:**
```
Stock XYZ - Sustained Quality Accumulation

Q1 2024:
- Institutional ownership: 45% → 50% (+5%)
- New holders: Baupost Group (Tier 1)
- Clustering score: 35

Q2 2024:
- Institutional ownership: 50% → 58% (+8%)
- Increasers: Berkshire (+20%), Fidelity (+15%), Dodge & Cox (+10%)
- Clustering score: 55

Q3 2024:
- Institutional ownership: 58% → 68% (+10%)
- Increasers: Berkshire (+10% more), Baupost (+25%), T. Rowe Price (new position)
- Clustering score: 72

Stock price during period: $45 → $48 (+6.7%)
Revenue growth: +12% YoY
P/E: 18x (sector average: 22x)

Signal: STRONG BUY
Interpretation: Quality value investors seeing opportunity before market, sustained accumulation
Expected outcome: Stock re-rating to sector average P/E = $48 × (22/18) = $58.67 (+22% upside)
```

### Level 2: Moderate Buy Signal (75th percentile)

**Criteria (Most must be met):**
1. **Magnitude:** Institutional ownership increasing 7-15% QoQ
2. **Consistency:** 2 consecutive quarters of accumulation
3. **Quality:** Clustering score 40-60 (mix of Tier 1/2 investors)
4. **Type:** More quality buyers than sellers
5. **Fundamental Support:** At least stable fundamentals
6. **Price Action:** Not extended (not up >30% in past quarter)

**Interpretation:**
- Institutions building positions
- Positive outlook but not unanimously bullish
- Moderate probability of price appreciation

**Action:**
- **New position:** BUY with moderate conviction (1-3% portfolio position)
- **Existing position:** HOLD or small ADD
- **Risk management:** Tighter stop-loss, monitor quarterly

**Historical Success Rate:** ~60-65% positive returns over 12 months

### Level 3: Neutral/Hold Signal (50th percentile)

**Criteria:**
1. **Magnitude:** Institutional ownership change <5% QoQ
2. **Consistency:** No clear trend
3. **Quality:** Mixed clustering score (20-40)
4. **Type:** Similar number of buyers and sellers

**Interpretation:**
- No clear institutional consensus
- Status quo
- Let other factors drive decision

**Action:**
- **New position:** PASS (wait for clearer signal)
- **Existing position:** HOLD (no change)
- **Risk management:** Standard position sizing

**Historical Success Rate:** ~50% (random walk)

### Level 4: Moderate Sell Signal (25th percentile)

**Criteria (Most must be met):**
1. **Magnitude:** Institutional ownership decreasing 7-15% QoQ
2. **Consistency:** 2 consecutive quarters of distribution
3. **Quality:** Tier 1/2 investors reducing positions
4. **Type:** More quality sellers than buyers
5. **Price Action:** Stock may still be rising (distribution into strength)

**Interpretation:**
- Smart money reducing exposure
- Early warning sign
- Potential deterioration in fundamentals or valuation concerns

**Action:**
- **New position:** AVOID
- **Existing position:** TRIM or SELL (reduce to 50% of normal position size)
- **Risk management:** Tighten stop-loss, prepare to exit

**Historical Success Rate:** ~60-65% underperform market over 12 months

### Level 5: Strong Sell Signal (5th percentile)

**Criteria (ALL must be met):**
1. **Magnitude:** Institutional ownership decreasing >15% QoQ
2. **Consistency:** 3+ consecutive quarters of distribution
3. **Quality:** Clustering score >60 on SELL side (multiple Tier 1/2 investors exiting)
4. **Concentration:** Declining institutional concentration (top holders exiting)
5. **Type:** Quality investors exiting, only passive/momentum funds remaining
6. **Price Action:** May still be positive (smart money exits before crash)

**Interpretation:**
- Widespread institutional exodus
- Serious fundamental concerns (even if not yet visible)
- High probability of significant decline
- Institutional investors know something market doesn't

**Action:**
- **New position:** DO NOT BUY (even if stock looks cheap)
- **Existing position:** SELL immediately (full exit)
- **Short consideration:** Consider short if technical setup supports

**Historical Success Rate:** ~75-80% negative returns over 12 months

**Example Pattern:**
```
Stock ABC - Sustained Quality Distribution

Q1 2024:
- Institutional ownership: 72% → 68% (-4%)
- Exits: Small hedge fund
- Clustering score: -15

Q2 2024:
- Institutional ownership: 68% → 60% (-8%)
- Decreasers: Fidelity (-20%), Wellington (-15%)
- Exits: 2 more funds
- Clustering score: -42

Q3 2024:
- Institutional ownership: 60% → 48% (-12%)
- Decreasers: Berkshire (-30%), Dodge & Cox (-25%), T. Rowe Price (-20%)
- Exits: 5 quality funds
- Clustering score: -85

Stock price during period: $80 → $75 (-6.25%)
Revenue growth: Slowing from +20% to +8% YoY
Management: Guiding lower for next quarter (not yet public in Q2)

Signal: STRONG SELL
Interpretation: Quality investors exiting ahead of visible deterioration
Expected outcome: Stock decline to $50-60 range as problems become apparent (-25% to -40%)
Actual outcome (next 2 quarters): Stock fell to $52 (-35% from Q3 peak)
```

## Contextual Adjustments

### Adjustment 1: Market Cap Considerations

**Large Cap (>$10B):**
- Harder for institutions to accumulate without moving price
- Sustained accumulation = very strong signal
- Distribution easier to hide
- **Adjustment:** Increase signal strength for accumulation (+0.5 levels)

**Mid Cap ($2B-$10B):**
- Sweet spot for institutional accumulation
- Standard signal strength
- **Adjustment:** No adjustment (baseline)

**Small Cap ($300M-$2B):**
- Can be moved easily by single institution
- Need broader participation for strong signal
- **Adjustment:** Require higher clustering score (+10 points)

**Micro Cap (<$300M):**
- Limited institutional interest
- 13F data less relevant
- **Adjustment:** De-weight institutional signals (-0.5 levels)

### Adjustment 2: Current Valuation

**Undervalued (P/E <15, P/B <2, FCF Yield >8%):**
- Institutional accumulation = value investors seeing opportunity
- Higher probability of success
- **Adjustment:** +0.5 signal strength

**Fairly Valued (P/E 15-25, typical metrics):**
- Standard interpretation
- **Adjustment:** No adjustment

**Overvalued (P/E >30, P/B >5, FCF Yield <3%):**
- Institutional accumulation may be late-stage momentum
- Distribution more significant (quality investors taking profits)
- **Adjustment:** -0.5 signal strength for accumulation, +0.5 for distribution

### Adjustment 3: Sector/Industry Dynamics

**Secular Growth Sector (Tech, Healthcare Innovation):**
- Institutional accumulation normal
- Need higher magnitude for strong signal
- **Adjustment:** Require +5% higher ownership change

**Cyclical Sector (Industrials, Materials, Energy):**
- Pay attention to economic cycle
- Early cycle accumulation = strong signal
- Late cycle distribution = strong signal
- **Adjustment:** Context-dependent, weight by macro environment

**Defensive Sector (Utilities, Consumer Staples, REITs):**
- Lower growth, stable ownership
- Large changes more meaningful
- **Adjustment:** Lower thresholds (-3% ownership change)

### Adjustment 4: Recent Price Action

**Stock Down >20% in past quarter:**
- Institutional accumulation = contrarian buying (value opportunity)
- **Interpretation:** Very strong signal if quality investors
- **Adjustment:** +1.0 signal strength

**Stock Flat to +10%:**
- Standard interpretation
- **Adjustment:** No adjustment

**Stock Up >30% in past quarter:**
- Institutional accumulation may be chasing momentum (late)
- Distribution less meaningful (profit-taking)
- **Adjustment:** -0.5 signal strength for accumulation

**Stock Up >100% in past year:**
- Institutional distribution = smart money taking profits (very significant)
- New accumulation suspect (likely late-stage momentum)
- **Adjustment:** +1.0 signal strength for distribution, -1.0 for accumulation

## Multi-Factor Integration

### Combining Institutional Flow with Other Signals

**Institutional Flow + Fundamental Analysis:**

| Institutional Signal | Fundamental Signal | Combined Interpretation | Action |
|---------------------|-------------------|------------------------|---------|
| Strong Buy | Strong Buy | Very High Conviction | BUY LARGE (5%+ position) |
| Strong Buy | Neutral | High Conviction | BUY (3-5% position) |
| Strong Buy | Weak | Contrarian Value | BUY SMALL (1-2%, monitor) |
| Moderate Buy | Strong Buy | High Conviction | BUY (3-5% position) |
| Moderate Buy | Neutral | Moderate Conviction | BUY SMALL (1-3% position) |
| Neutral | Strong Buy | Fundamental-Driven | BUY (2-4% position) |
| Moderate Sell | Strong Buy | Investigate Divergence | HOLD (research further) |
| Strong Sell | Strong Buy | **Major Red Flag** | AVOID (institutions know something) |
| Strong Sell | Weak | Confirmed Decline | SELL or SHORT |

**Institutional Flow + Technical Analysis:**

| Institutional Signal | Technical Signal | Combined Interpretation | Action |
|---------------------|------------------|------------------------|---------|
| Strong Buy | Breakout | Confirmed Uptrend | BUY on breakout |
| Strong Buy | Basing | Accumulation Before Move | BUY in base, add on breakout |
| Strong Buy | Downtrend | Early/Contrarian | WAIT for technical confirmation |
| Moderate Buy | Breakout | Confirming Move | BUY on pullback to breakout level |
| Neutral | Breakout | Technically Driven | TRADE (not invest) |
| Moderate Sell | Breakdown | Confirmed Downtrend | SELL |
| Strong Sell | Breakdown | Accelerating Decline | SELL IMMEDIATELY |

**Institutional Flow + Insider Trading:**

| Institutional Signal | Insider Signal | Combined Interpretation | Action |
|---------------------|----------------|------------------------|---------|
| Strong Buy | Insider Buying | **Maximum Conviction** | BUY LARGE |
| Strong Buy | Neutral | Strong Signal | BUY |
| Strong Buy | Insider Selling | Investigate Discrepancy | BUY SMALL (monitor) |
| Neutral | Insider Buying | Insider Conviction | BUY MODERATE |
| Moderate Sell | Insider Buying | **Conflicting Signals** | HOLD (investigate) |
| Moderate Sell | Insider Selling | Confirming Distribution | SELL |
| Strong Sell | Insider Selling | **Maximum Conviction SELL** | EXIT IMMEDIATELY |

## Sector Rotation Framework

### Using Institutional Flow to Identify Sector Rotation

**Step 1: Calculate Aggregate Sector-Level Institutional Flow**

For each sector (Technology, Healthcare, Financials, etc.):
```
Sector Institutional Flow Score =
  Sum of (Stock Institutional Ownership Change × Market Cap) for all stocks in sector
  / Total Sector Market Cap

Positive score = Net institutional inflow to sector
Negative score = Net institutional outflow from sector
```

**Step 2: Rank Sectors by Flow Score**

```
Top 3 sectors (highest positive flow) = Accumulation sectors
Middle sectors = Neutral
Bottom 3 sectors (most negative flow) = Distribution sectors
```

**Step 3: Interpret by Market Cycle**

**Early Cycle (Post-Recession Recovery):**
- **Expect Accumulation:** Technology, Consumer Discretionary, Financials
- **Expect Distribution:** Utilities, Consumer Staples, Healthcare
- **Signal:** If institutional flow matches expectations = confirmation
- **Signal:** If institutional flow opposes expectations = investigate (possible false recovery or delayed cycle)

**Mid Cycle (Economic Expansion):**
- **Expect Accumulation:** Industrials, Materials, Energy
- **Expect Distribution:** Defensive sectors
- **Signal:** Rotation into cyclicals confirms expansion

**Late Cycle (Peak Growth):**
- **Expect Accumulation:** Energy, Materials (inflation protection)
- **Expect Distribution:** Technology, Consumer Discretionary (profit-taking)
- **Signal:** Rotation to inflation hedges signals late cycle

**Recession:**
- **Expect Accumulation:** Utilities, Consumer Staples, Healthcare
- **Expect Distribution:** Cyclicals, Growth stocks
- **Signal:** Flight to safety

**Step 4: Portfolio Allocation Based on Sector Flow**

```
High Institutional Inflow Sectors:
- Overweight (30-40% of equity allocation)
- Select best stocks within sector using institutional flow

Neutral Sectors:
- Market weight (10-20% of equity allocation)

High Institutional Outflow Sectors:
- Underweight or zero weight (0-10% of equity allocation)
- Sell existing positions showing institutional distribution
```

## Practical Decision Tree

### For New Position Consideration:

```
1. Run institutional flow analysis on stock
   ↓
2. What is the signal level?
   ↓
   ├─ Strong Buy Signal (Level 1)
   │  ├─ Check fundamentals: Strong → BUY LARGE (5%+)
   │  ├─ Check fundamentals: Neutral → BUY (3-5%)
   │  └─ Check fundamentals: Weak → BUY SMALL (1-2%), monitor
   │
   ├─ Moderate Buy Signal (Level 2)
   │  ├─ Check fundamentals: Strong → BUY (3-5%)
   │  ├─ Check fundamentals: Neutral → BUY SMALL (1-3%)
   │  └─ Check fundamentals: Weak → PASS
   │
   ├─ Neutral (Level 3)
   │  └─ Decide based on other factors (fundamental, technical)
   │
   ├─ Moderate Sell Signal (Level 4)
   │  └─ AVOID (do not initiate)
   │
   └─ Strong Sell Signal (Level 5)
      └─ AVOID or SHORT (if appropriate)
```

### For Existing Position Review:

```
1. Run quarterly institutional flow analysis
   ↓
2. What is the signal level?
   ↓
   ├─ Strong Buy Signal (Level 1)
   │  └─ ADD to position (up to maximum 10% portfolio weight)
   │
   ├─ Moderate Buy Signal (Level 2)
   │  └─ HOLD or small ADD
   │
   ├─ Neutral (Level 3)
   │  └─ HOLD (no change)
   │
   ├─ Moderate Sell Signal (Level 4)
   │  ├─ Check fundamentals: Deteriorating → TRIM to 50% or SELL
   │  ├─ Check fundamentals: Stable → TRIM to 75%
   │  └─ Check fundamentals: Strong → HOLD (monitor closely)
   │
   └─ Strong Sell Signal (Level 5)
      └─ SELL immediately (full exit)
```

## Common Mistakes to Avoid

### Mistake 1: Overreacting to Single Quarter

**Problem:** One quarter of institutional buying/selling may not be a trend

**Solution:**
- Require 2+ quarters for moderate signals
- Require 3+ quarters for strong conviction
- View single quarter as hypothesis, not confirmation

### Mistake 2: Ignoring Index Fund Flows

**Problem:** Treating passive inflows like active accumulation

**Solution:**
- Separate active from passive using institutional tiers
- Weight Tier 1/2 heavily, Tier 4 (index funds) minimally
- Focus on WHO is buying, not just THAT institutions are buying

### Mistake 3: Following Too Late

**Problem:** Institutional buying visible in 13F after 45-day lag; stock may have already moved

**Solution:**
- Use 13F as confirming signal, not entry trigger
- Combine with technical analysis for timing
- Be willing to buy after initial move if institutional thesis strong

### Mistake 4: Ignoring Price Action Context

**Problem:** Institutional buying in falling stock (catching falling knife) vs rising stock (momentum)

**Solution:**
- Institutional accumulation + falling price = potential value opportunity (higher conviction)
- Institutional accumulation + rising price = momentum (lower conviction, may be late)
- Adjust signal strength based on recent price action

### Mistake 5: Equal Weighting All Institutions

**Problem:** Treating index fund flows same as Berkshire Hathaway

**Solution:**
- Use institutional tier weighting framework
- Tier 1 (Superinvestors): 3.0-3.5x weight
- Tier 2 (Quality Active): 2.0-2.5x weight
- Tier 3 (Average): 1.0-1.5x weight
- Tier 4 (Passive): 0.0-0.5x weight

## Summary Checklist

Before making investment decision based on institutional flow:

**✅ Verification Checklist:**
- [ ] Signal level determined (Strong/Moderate/Neutral Buy or Sell)
- [ ] Multi-quarter trend confirmed (2+ quarters same direction)
- [ ] Institution quality assessed (Tier 1/2 involvement?)
- [ ] Clustering score calculated (>50 for strong signals)
- [ ] Market cap context considered (adjustment needed?)
- [ ] Valuation context considered (adjustment needed?)
- [ ] Recent price action reviewed (adjustment needed?)
- [ ] Fundamental analysis completed (aligns with institutional thesis?)
- [ ] Technical analysis reviewed (entry timing optimized?)
- [ ] Position sizing determined based on signal strength
- [ ] Risk management plan established (stop-loss, monitoring frequency)

**Final Decision Framework:**
- **5+ yes = High Conviction:** BUY/SELL with conviction
- **3-4 yes = Moderate Conviction:** HOLD or Small BUY/TRIM
- **<3 yes = Low Conviction:** PASS or minimal position

---

This interpretation framework should be used as a systematic guide, not rigid rules. Market conditions, individual stock characteristics, and portfolio constraints should also inform final decisions. Institutional flow is a powerful signal but works best when combined with fundamental and technical analysis.


---

## SKILL: jito-bundles

- Fuente: `agiprolabs/claude-trading-skills` → `skills/jito-bundles` (MIT)
- Cuándo usarla: Jito bundle submission for MEV protection on Solana — bundle building, tip strategies, block engine endpoints, and landing rate optimization
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/jito-bundles/` (build_bundle.py, check_bundle_status.py)

# Jito Bundle Submission for Solana

Jito bundles allow you to submit up to 5 Solana transactions that execute **atomically** — either all land in the same slot or none do. This is the primary mechanism for MEV protection and competitive transaction execution on Solana. Approximately 85%+ of Solana validators run the Jito-modified client, making bundles the standard for reliable, front-run-resistant execution.

> **EXECUTION SKILL — SAFETY WARNING**: Submitting bundles spends real SOL on tips. Always test with `--demo` mode first. Never submit bundles with real funds without explicit confirmation. Default to simulation/dry-run in all scripts and examples.

## When to Use Bundles

| Scenario | Use Bundle? | Why |
|----------|-------------|-----|
| Swap on illiquid token | Yes | Prevents sandwich attacks |
| Multi-step arbitrage | Yes | Atomic execution prevents partial fills |
| Liquidation | Yes | Competitive — tip determines priority |
| Simple SOL transfer | No | Priority fees are cheaper and sufficient |
| Time-insensitive swap | Maybe | Bundles cost tips; priority fees may suffice |
| NFT mint / competitive action | Yes | Guarantees ordering within the slot |

## Core Concepts

### Bundle Anatomy

A Jito bundle is a JSON-RPC request containing 1-5 base58-encoded signed transactions. The transactions execute sequentially and atomically within a single slot.

```
Bundle = [Tx1, Tx2, ..., TxN]  (N <= 5)

- All transactions must be signed
- Transactions execute in order: Tx1 → Tx2 → ... → TxN
- If ANY transaction fails, the ENTIRE bundle is dropped
- The tip instruction goes in the LAST transaction (last instruction)
- Bundle has ~2 slots (~800ms) to land before expiry
```

### Tip Mechanism

Tips are SOL transfers to one of Jito's 8 tip accounts. The tip incentivizes validators to include your bundle.

```python
# Tip is a standard SOL transfer instruction
tip_instruction = transfer(
    from_pubkey=your_wallet,
    to_pubkey=tip_account,      # One of 8 Jito tip accounts
    lamports=tip_amount          # Tip in lamports (1 SOL = 1e9 lamports)
)
# Add as the LAST instruction of the LAST transaction in the bundle
```

Tip accounts are fetched dynamically via `getTipAccounts`. Rotate through them to distribute load.

### Block Engine Endpoints

Jito operates geographically distributed block engines. Choose the one closest to your infrastructure:

| Region | Endpoint |
|--------|----------|
| New York | `https://mainnet.block-engine.jito.wtf` |
| Amsterdam | `https://amsterdam.block-engine.jito.wtf` |
| Frankfurt | `https://frankfurt.block-engine.jito.wtf` |
| Tokyo | `https://tokyo.block-engine.jito.wtf` |

All endpoints accept JSON-RPC over HTTPS on port 443. The `/api/v1/bundles` path handles bundle operations.

## API Methods

### sendBundle

Submit a bundle of up to 5 transactions.

```python
import httpx

BLOCK_ENGINE = "https://mainnet.block-engine.jito.wtf"

payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "sendBundle",
    "params": [
        [tx1_base58, tx2_base58],  # List of base58-encoded signed txs
    ]
}

resp = httpx.post(f"{BLOCK_ENGINE}/api/v1/bundles", json=payload)
data = resp.json()
bundle_id = data["result"]  # UUID string
```

### getBundleStatuses

Check the landing status of submitted bundles (up to 5 bundle IDs per request).

```python
payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getBundleStatuses",
    "params": [[bundle_id]]
}
resp = httpx.post(f"{BLOCK_ENGINE}/api/v1/bundles", json=payload)
statuses = resp.json()["result"]["value"]
# Each status: {bundle_id, status, slot, transactions: [{signature, ...}]}
# status: "Invalid", "Pending", "Failed", "Landed"
```

### getTipAccounts

Fetch the current list of Jito tip accounts.

```python
payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getTipAccounts",
    "params": []
}
resp = httpx.post(f"{BLOCK_ENGINE}/api/v1/bundles", json=payload)
tip_accounts = resp.json()["result"]  # List of 8 base58 pubkeys
```

### getInflightBundleStatuses

Check status of bundles that haven't landed yet (in-flight).

```python
payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getInflightBundleStatuses",
    "params": [[bundle_id]]
}
resp = httpx.post(f"{BLOCK_ENGINE}/api/v1/bundles", json=payload)
# status: "Pending", "Failed", "Landed"
```

## Bundle Construction Pattern

A typical bundle for a protected swap:

```python
from solders.transaction import VersionedTransaction
from solders.message import MessageV0
from solders.instruction import Instruction
from solders.system_program import transfer, TransferParams
from solders.pubkey import Pubkey
import random

def build_protected_swap_bundle(
    swap_ix: Instruction,
    payer: Pubkey,
    tip_lamports: int,
    tip_accounts: list[str],
    recent_blockhash: str,
) -> list[VersionedTransaction]:
    """Build a 1-tx bundle: swap + tip in the same transaction.

    For simple swaps, a single-transaction bundle is sufficient.
    The tip instruction is appended as the last instruction.
    """
    # Pick a random tip account
    tip_account = Pubkey.from_string(random.choice(tip_accounts))

    # Tip instruction
    tip_ix = transfer(TransferParams(
        from_pubkey=payer,
        to_pubkey=tip_account,
        lamports=tip_lamports,
    ))

    # Build transaction with swap + tip
    msg = MessageV0.try_compile(
        payer=payer,
        instructions=[swap_ix, tip_ix],
        address_lookup_table_accounts=[],
        recent_blockhash=recent_blockhash,
    )
    tx = VersionedTransaction(msg, [keypair])
    return [tx]
```

## Tip Sizing Guide

| Scenario | Tip Range (lamports) | Tip Range (SOL) |
|----------|---------------------|-----------------|
| Normal swap (low urgency) | 1,000 - 10,000 | 0.000001 - 0.00001 |
| Normal swap (standard) | 10,000 - 50,000 | 0.00001 - 0.00005 |
| Competitive action (arb, liquidation) | 50,000 - 500,000 | 0.00005 - 0.0005 |
| Highly competitive (NFT mint, MEV) | 500,000 - 5,000,000 | 0.0005 - 0.005 |
| Emergency (must land this slot) | 5,000,000+ | 0.005+ |

Dynamic tip calculation based on recent tip levels:

```python
def calculate_dynamic_tip(
    base_tip: int = 10_000,
    urgency_multiplier: float = 1.0,
    recent_tip_percentile_50: int = 15_000,
) -> int:
    """Calculate tip based on urgency and recent network tips.

    Args:
        base_tip: Minimum tip in lamports.
        urgency_multiplier: 1.0 = normal, 2.0 = urgent, 5.0 = critical.
        recent_tip_percentile_50: Median tip from recent bundles.

    Returns:
        Tip amount in lamports.
    """
    dynamic_tip = max(base_tip, int(recent_tip_percentile_50 * urgency_multiplier))
    # Cap at 0.01 SOL to prevent accidents
    return min(dynamic_tip, 10_000_000)
```

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Bundle dropped (slot expired)` | Bundle didn't land within 2 slots | Retry with fresh blockhash; consider higher tip |
| `Transaction simulation failed` | A tx in the bundle would fail on-chain | Simulate each tx individually to find the failing one |
| `Bundle already processed` | Duplicate bundle ID | Expected on retry; check status instead |
| `Rate limited` | Too many requests to block engine | Back off; rotate between block engine endpoints |
| `Invalid transaction` | Malformed or unsigned transaction | Verify all txs are signed and base58-encoded |
| `Blockhash not found` | Stale blockhash | Use `getLatestBlockhash` with `finalized` commitment |

## Landing Rate Optimization

Strategies to maximize bundle landing probability:

1. **Multi-region submission**: Send the same bundle to multiple block engines simultaneously. The first to reach the current leader wins.

2. **Fresh blockhash**: Use `getLatestBlockhash` with `confirmed` commitment immediately before building. Stale blockhashes are the #1 cause of dropped bundles.

3. **Retry with backoff**: If a bundle doesn't land within 2-3 seconds, rebuild with a fresh blockhash and resubmit. Do NOT resubmit with the same blockhash.

4. **Adequate tipping**: Under-tipped bundles are deprioritized. Monitor the network's tip distribution and tip at or above the 50th percentile for your urgency level.

5. **Minimal bundle size**: Fewer transactions = less simulation time = higher landing rate. Use single-transaction bundles when possible.

```python
async def submit_with_retry(
    bundle_txs: list[str],
    endpoints: list[str],
    max_retries: int = 3,
) -> str | None:
    """Submit bundle to multiple endpoints with retry logic.

    Returns bundle_id if submitted, None if all retries exhausted.
    """
    for attempt in range(max_retries):
        # Submit to all endpoints in parallel
        async with httpx.AsyncClient() as client:
            tasks = [
                client.post(
                    f"{ep}/api/v1/bundles",
                    json={
                        "jsonrpc": "2.0", "id": 1,
                        "method": "sendBundle",
                        "params": [bundle_txs],
                    },
                    timeout=5.0,
                )
                for ep in endpoints
            ]
            # Process first successful response
            for resp in asyncio.as_completed(tasks):
                result = (await resp).json()
                if "result" in result:
                    return result["result"]

        # Wait before retry with fresh blockhash
        await asyncio.sleep(0.5 * (attempt + 1))
    return None
```

## Safety Checklist (Execution)

Before submitting any bundle with real funds:

- [ ] Simulated all transactions individually via `simulateTransaction`
- [ ] Verified tip amount is reasonable (not accidentally SOL instead of lamports)
- [ ] Confirmed blockhash is fresh (< 60 seconds old)
- [ ] Verified all transactions are properly signed
- [ ] Checked wallet balance covers all transaction costs + tip
- [ ] Tested with devnet or --demo mode first
- [ ] Set maximum tip cap to prevent accidental overpayment

## Files

### References
- `references/bundle_api.md` — Complete JSON-RPC API reference with request/response schemas and error codes
- `references/tip_strategies.md` — Tip calculation strategies, dynamic tipping, cost optimization
- `references/best_practices.md` — Bundle construction patterns, landing rate optimization, common pitfalls

### Scripts
- `scripts/build_bundle.py` — Bundle construction with tip instruction; `--demo` mode builds but does not submit
- `scripts/check_bundle_status.py` — Bundle status checking and tip account fetching; `--demo` mode uses mock responses

### Referencia: references/best_practices.md

# Jito Bundles — Best Practices

## Bundle Construction Patterns

### Single-Transaction Bundle (Most Common)

For a simple protected swap, put everything in one transaction:

```
Transaction 1:
  Instruction 1: Compute budget (set compute units)
  Instruction 2: Compute budget (set priority fee — optional alongside tip)
  Instruction 3: Swap instruction (e.g., Jupiter route)
  Instruction 4: Tip transfer (LAST instruction)
```

**Advantages:** Simplest to build, fastest to simulate, highest landing rate.

### Multi-Transaction Bundle

For operations requiring atomicity across multiple transactions:

```
Transaction 1: Setup (create accounts, approve delegations)
Transaction 2: Execute (the core operation)
Transaction 3: Cleanup + Tip (close accounts, collect rent, tip as last ix)
```

**Rules:**
- Tip goes in the LAST instruction of the LAST transaction
- Each transaction must be independently signed
- All transactions share the same recent blockhash
- If ANY transaction fails simulation, the entire bundle is dropped
- Transactions execute in order: Tx1 then Tx2 then Tx3

### Arbitrage Bundle Pattern

```
Transaction 1: Buy on DEX A
Transaction 2: Sell on DEX B + Tip
```

The atomicity guarantees you never get stuck with inventory — if the sell fails, the buy is also reverted.

## Blockhash Management

The blockhash is the single most critical factor for bundle landing. Stale blockhashes are the #1 cause of dropped bundles.

**Best practices:**
1. Fetch `getLatestBlockhash` with `confirmed` commitment immediately before building
2. A blockhash is valid for approximately 60-90 seconds (150 slots)
3. For retries, ALWAYS fetch a new blockhash — never resubmit with the old one
4. Do not cache blockhashes for more than a few seconds

```python
import httpx
import time

class BlockhashManager:
    """Manage blockhash freshness for bundle construction."""

    def __init__(self, rpc_url: str, max_age_seconds: float = 5.0):
        self.rpc_url = rpc_url
        self.max_age = max_age_seconds
        self._blockhash: str | None = None
        self._fetched_at: float = 0.0

    def get_fresh_blockhash(self) -> str:
        """Get a blockhash, refreshing if stale."""
        if (
            self._blockhash is None
            or (time.time() - self._fetched_at) > self.max_age
        ):
            resp = httpx.post(self.rpc_url, json={
                "jsonrpc": "2.0", "id": 1,
                "method": "getLatestBlockhash",
                "params": [{"commitment": "confirmed"}],
            })
            data = resp.json()
            self._blockhash = data["result"]["value"]["blockhash"]
            self._fetched_at = time.time()
        return self._blockhash
```

## Landing Rate Optimization

### Multi-Region Submission

Submit the same bundle to all block engine endpoints simultaneously. The bundle reaching the current leader first wins.

```python
JITO_ENDPOINTS = [
    "https://mainnet.block-engine.jito.wtf/api/v1/bundles",
    "https://amsterdam.block-engine.jito.wtf/api/v1/bundles",
    "https://frankfurt.block-engine.jito.wtf/api/v1/bundles",
    "https://tokyo.block-engine.jito.wtf/api/v1/bundles",
]

async def multi_region_submit(
    bundle_txs: list[str],
    endpoints: list[str] = JITO_ENDPOINTS,
) -> list[dict]:
    """Submit bundle to all endpoints in parallel."""
    import asyncio
    payload = {
        "jsonrpc": "2.0", "id": 1,
        "method": "sendBundle",
        "params": [bundle_txs],
    }
    async with httpx.AsyncClient(timeout=5.0) as client:
        tasks = [client.post(ep, json=payload) for ep in endpoints]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    return [
        r.json() if not isinstance(r, Exception) else {"error": str(r)}
        for r in results
    ]
```

### Retry Strategy

```python
import asyncio

async def submit_with_landing_check(
    build_bundle_fn,  # Callable that builds fresh bundle
    max_attempts: int = 3,
    poll_interval: float = 0.5,
    poll_timeout: float = 3.0,
) -> dict:
    """Submit bundle, poll for landing, retry if needed."""
    for attempt in range(max_attempts):
        # Build fresh bundle (fresh blockhash each time)
        bundle_txs = build_bundle_fn()
        bundle_id = await submit_to_endpoints(bundle_txs)

        if bundle_id is None:
            continue

        # Poll for landing
        landed = await poll_bundle_status(
            bundle_id, poll_interval, poll_timeout
        )
        if landed:
            return {"status": "landed", "bundle_id": bundle_id,
                    "attempt": attempt + 1}

    return {"status": "failed", "attempts": max_attempts}
```

### Compute Budget Optimization

Set compute units accurately to reduce simulation time:

```python
from solders.compute_budget import set_compute_unit_limit

# Profile your transaction's actual compute usage, then add 10-20% buffer
compute_ix = set_compute_unit_limit(200_000)  # Adjust based on profiling
```

Over-allocating compute units doesn't cost more in fees, but accurate limits help validators simulate bundles faster.

## Common Pitfalls

### 1. Tip in Wrong Position

The tip MUST be the last instruction of the last transaction. Placing it elsewhere causes bundle rejection.

```python
# WRONG — tip is not last
instructions = [tip_ix, swap_ix]

# CORRECT — tip is last
instructions = [swap_ix, tip_ix]
```

### 2. Unsigned Transactions

Every transaction in the bundle must be fully signed before base58 encoding. Partially signed transactions cause immediate rejection.

### 3. Inconsistent Blockhash

All transactions in a multi-tx bundle should use the same recent blockhash. Mixing blockhashes from different fetches can cause intermittent failures.

### 4. Transaction Too Large

Solana transactions have a 1232-byte limit. Adding a tip instruction uses ~52 bytes. If your swap instruction is near the limit, the tip may push it over. Solutions:
- Use versioned transactions with address lookup tables
- Split into a multi-transaction bundle

### 5. Simulating the Bundle as Individual Transactions

When debugging, simulate each transaction individually. But remember that in a bundle, Tx2 sees the state changes from Tx1. If Tx2 depends on Tx1's output (e.g., Tx1 creates an account that Tx2 uses), simulating Tx2 alone will fail.

### 6. Not Handling Partial Information

`getBundleStatuses` may return `null` for a bundle ID if:
- The bundle hasn't been processed yet (check inflight status)
- The bundle expired (rebuild and retry)
- The bundle ID is wrong

Always check for `null` entries in the response.

## When NOT to Use Bundles

1. **Simple SOL transfers**: Priority fees are cheaper and sufficient
2. **Low-value swaps** (< 0.1 SOL): MEV risk is negligible; tip costs more than protection saves
3. **Devnet/testnet**: Jito bundles only work on mainnet
4. **When you need finality guarantees**: Bundles land or drop — they don't provide faster finality than normal transactions

## Debugging Bundles

### Step-by-step debugging workflow:

1. **Simulate each transaction individually** via `simulateTransaction` on your RPC
2. **Check for program errors** in simulation logs
3. **Verify all accounts** are correct and have sufficient balances
4. **Check blockhash freshness** — if the blockhash is > 60s old, refresh
5. **Verify tip account** is in the current `getTipAccounts` list
6. **Check base58 encoding** — ensure transactions are properly serialized

### Logging Best Practices

Log these fields for every bundle submission:
- Bundle ID (from sendBundle response)
- Timestamp of submission
- Tip amount (lamports)
- Tip account used
- Blockhash used
- Number of transactions
- Block engine endpoint(s) submitted to
- Landing status (poll after 2-3 seconds)

```python
import logging

logger = logging.getLogger("jito-bundles")

def log_bundle_submission(
    bundle_id: str,
    tip_lamports: int,
    tip_account: str,
    blockhash: str,
    num_txs: int,
    endpoints: list[str],
) -> None:
    logger.info(
        "Bundle submitted | id=%s tip=%d tip_acct=%s blockhash=%s "
        "txs=%d endpoints=%s",
        bundle_id, tip_lamports, tip_account[:8] + "...",
        blockhash[:8] + "...", num_txs, len(endpoints),
    )
```

### Referencia: references/bundle_api.md

# Jito Bundle API Reference

## Overview

The Jito Bundle API uses JSON-RPC 2.0 over HTTPS. All requests go to `/api/v1/bundles` on a block engine endpoint.

**Base URLs:**
- `https://mainnet.block-engine.jito.wtf/api/v1/bundles`
- `https://amsterdam.block-engine.jito.wtf/api/v1/bundles`
- `https://frankfurt.block-engine.jito.wtf/api/v1/bundles`
- `https://tokyo.block-engine.jito.wtf/api/v1/bundles`

**Headers:**
```
Content-Type: application/json
```

Some endpoints may require a UUID auth token (obtained from the Jito dashboard) passed as a query parameter or header. Public endpoints (sendBundle, getBundleStatuses, getTipAccounts) generally do not require auth.

---

## sendBundle

Submit a bundle of up to 5 signed transactions for atomic execution.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "sendBundle",
  "params": [
    ["<base58_tx_1>", "<base58_tx_2>"]
  ]
}
```

**Parameters:**
- `params[0]` (array of strings, required): List of 1-5 base58-encoded signed transactions. Transactions execute in order.

**Response (success):**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

- `result` (string): Bundle UUID for status tracking.

**Response (error):**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "Invalid params: bundle must contain 1-5 transactions"
  }
}
```

**Error codes:**
| Code | Message | Cause |
|------|---------|-------|
| -32600 | Invalid Request | Malformed JSON-RPC |
| -32601 | Method not found | Typo in method name |
| -32602 | Invalid params | Wrong param format, >5 txs, or invalid base58 |
| -32603 | Internal error | Block engine internal failure |
| -32000 | Bundle simulation failed | A transaction in the bundle fails simulation |
| -32001 | Rate limited | Too many requests; back off |

**curl example:**
```bash
curl -X POST "https://mainnet.block-engine.jito.wtf/api/v1/bundles" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "sendBundle",
    "params": [["<base58_tx>"]]
  }'
```

---

## getBundleStatuses

Check landing status of previously submitted bundles.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "getBundleStatuses",
  "params": [
    ["a1b2c3d4-e5f6-7890-abcd-ef1234567890"]
  ]
}
```

**Parameters:**
- `params[0]` (array of strings, required): List of 1-5 bundle UUIDs to check.

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "context": {
      "slot": 280000000
    },
    "value": [
      {
        "bundle_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "transactions": [
          {
            "signature": "5rGz...",
            "slot": 280000000,
            "confirmation_status": "confirmed",
            "err": null
          }
        ],
        "slot": 280000000,
        "confirmation_status": "confirmed",
        "err": {
          "Ok": null
        }
      }
    ]
  }
}
```

**Status values in `confirmation_status`:**
| Status | Meaning |
|--------|---------|
| `processed` | Transaction seen by the cluster |
| `confirmed` | Transaction confirmed by supermajority |
| `finalized` | Transaction finalized (max confirmations) |

**If bundle not found**, the corresponding entry in `value` will be `null`. This means the bundle either expired, was never submitted, or is still in-flight. Use `getInflightBundleStatuses` to check in-flight bundles.

---

## getTipAccounts

Fetch the current list of Jito tip payment accounts.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "getTipAccounts",
  "params": []
}
```

**Parameters:** None.

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": [
    "96gYZGLnJYVFmbjzopPSU6QiEV5fGqZNyN9nmNhvrZU5",
    "HFqU5x63VTqvQss8hp11i4bVqkfRtQ7NmXwkiAMXBiap",
    "Cw8CFyM9FkoMi7K7Crf6HNQqf4uEMzpKw6QNghXLvLkY",
    "ADaUMid9yfUytqMBgopwjb2o2J3mF9Cp4vFsMhBBe6Vy",
    "DfXygSm4jCyNCybVYYK6DwvWqjKee8pbDmJGcLWNDXjh",
    "ADuUkR4vqLUMWXxW9gh6D6L8pMSawimctcNZ5pGwDcEt",
    "DttWaMuVvTiduZRnguLF7jNxTgiMBZ1hyAumKUiL2KRL",
    "3AVi9Tg9Uo68tJfuvoKvqKNWKkC5wPdSSdeBnizKZ6jT"
  ]
}
```

Returns an array of 8 base58-encoded public keys. Select one randomly or rotate through them to distribute load across validators.

---

## getInflightBundleStatuses

Check status of bundles that are still being processed (not yet landed or expired).

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "getInflightBundleStatuses",
  "params": [
    ["a1b2c3d4-e5f6-7890-abcd-ef1234567890"]
  ]
}
```

**Parameters:**
- `params[0]` (array of strings, required): List of 1-5 bundle UUIDs.

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "context": {
      "slot": 280000000
    },
    "value": [
      {
        "bundle_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "status": "Pending",
        "landed_slot": null
      }
    ]
  }
}
```

**Status values:**
| Status | Meaning |
|--------|---------|
| `Pending` | Bundle received, awaiting inclusion |
| `Landed` | Bundle successfully included in a block |
| `Failed` | Bundle failed simulation or expired |
| `Invalid` | Bundle was malformed or contained invalid transactions |

---

## Rate Limits

- Public endpoints: approximately 5-10 requests/second per IP
- Authenticated endpoints: higher limits based on plan
- `sendBundle`: subject to per-IP and per-bundle rate limiting
- `getBundleStatuses` / `getInflightBundleStatuses`: relatively generous limits

**Rate limit response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32001,
    "message": "Rate limited. Please slow down."
  }
}
```

**Mitigation strategies:**
1. Rotate between block engine endpoints (NY, Amsterdam, Frankfurt, Tokyo)
2. Implement exponential backoff on rate limit errors
3. Batch status checks (up to 5 bundle IDs per request)
4. Cache tip accounts (refresh every 60 seconds, not every request)

---

## Request/Response Schema Summary

| Method | Params | Result Type | Notes |
|--------|--------|-------------|-------|
| `sendBundle` | `[[tx1, tx2, ...]]` | `string` (UUID) | Max 5 txs |
| `getBundleStatuses` | `[[id1, id2, ...]]` | `{context, value}` | Max 5 IDs |
| `getTipAccounts` | `[]` | `string[]` | 8 accounts |
| `getInflightBundleStatuses` | `[[id1, id2, ...]]` | `{context, value}` | Max 5 IDs |

### Referencia: references/tip_strategies.md

# Jito Tip Strategies

## Overview

The tip is a SOL transfer added as the last instruction of the last transaction in a bundle. Tips incentivize Jito-enabled validators to include your bundle. The tip amount directly affects landing probability — under-tipped bundles are deprioritized relative to higher-tipping competitors.

## Tip Account Selection

Jito maintains 8 tip accounts. Fetch them via `getTipAccounts` and rotate through them:

```python
import random

def select_tip_account(tip_accounts: list[str]) -> str:
    """Select a random tip account to distribute validator load."""
    return random.choice(tip_accounts)
```

**Cache tip accounts** for 60 seconds. They rarely change, and fetching them on every bundle wastes API calls.

## Static Tip Strategies

### Fixed Tip

Set a constant tip amount. Simple but doesn't adapt to network conditions.

```python
TIP_LAMPORTS = 25_000  # 0.000025 SOL — reasonable for standard swaps
```

**When to use:** Low-urgency transactions where you don't mind occasional drops.

### Tiered by Urgency

Pre-define tip levels by transaction urgency:

```python
TIP_TIERS = {
    "low":      5_000,       # 0.000005 SOL — background tasks
    "normal":   25_000,      # 0.000025 SOL — standard swaps
    "high":     100_000,     # 0.0001 SOL   — time-sensitive trades
    "critical": 500_000,     # 0.0005 SOL   — must land this slot
    "extreme":  5_000_000,   # 0.005 SOL    — competitive MEV/liquidation
}

def get_tip(urgency: str = "normal") -> int:
    return TIP_TIERS.get(urgency, TIP_TIERS["normal"])
```

## Dynamic Tip Strategies

### Percentile-Based Tipping

Query recent tip distribution and tip at a target percentile:

```python
def calculate_percentile_tip(
    recent_tips: list[int],
    target_percentile: float = 0.50,
    minimum: int = 5_000,
) -> int:
    """Tip at a given percentile of recent bundle tips.

    Args:
        recent_tips: List of recent tip amounts in lamports.
        target_percentile: 0.0-1.0, where 0.5 = median.
        minimum: Floor tip amount.

    Returns:
        Tip in lamports.
    """
    if not recent_tips:
        return minimum
    sorted_tips = sorted(recent_tips)
    idx = int(len(sorted_tips) * target_percentile)
    idx = min(idx, len(sorted_tips) - 1)
    return max(sorted_tips[idx], minimum)
```

**Guideline percentiles:**
- 25th percentile: Economy — may drop during congestion
- 50th percentile: Standard — lands most of the time
- 75th percentile: Priority — high landing probability
- 90th+ percentile: Competitive — for time-critical operations

### Congestion-Adjusted Tipping

Scale tips based on network congestion signals:

```python
def congestion_adjusted_tip(
    base_tip: int,
    recent_slot_time_ms: float,
    avg_slot_time_ms: float = 400.0,
    max_multiplier: float = 5.0,
) -> int:
    """Increase tip when slots are slower (congested).

    When slots take longer than average, the network is congested
    and competition for block space increases.
    """
    if recent_slot_time_ms <= avg_slot_time_ms:
        return base_tip

    # Congestion ratio: 1.0 = normal, 2.0 = slots taking 2x longer
    congestion_ratio = recent_slot_time_ms / avg_slot_time_ms
    multiplier = min(congestion_ratio, max_multiplier)
    return int(base_tip * multiplier)
```

### Escalating Retry Tips

Increase tip on each retry attempt:

```python
def escalating_tip(
    base_tip: int,
    attempt: int,
    escalation_factor: float = 1.5,
    max_tip: int = 1_000_000,
) -> int:
    """Increase tip with each failed attempt.

    Args:
        base_tip: Starting tip in lamports.
        attempt: Current attempt number (0-indexed).
        escalation_factor: Multiplier per attempt.
        max_tip: Maximum tip cap to prevent accidents.

    Returns:
        Tip in lamports, capped at max_tip.
    """
    tip = int(base_tip * (escalation_factor ** attempt))
    return min(tip, max_tip)

# attempt 0: 25,000
# attempt 1: 37,500
# attempt 2: 56,250
# attempt 3: 84,375 (capped if > max_tip)
```

## Cost Optimization

### Tip Budgeting

Set a per-trade tip budget and track spending:

```python
class TipBudget:
    """Track tip spending against a budget."""

    def __init__(self, daily_budget_lamports: int = 5_000_000):
        self.daily_budget = daily_budget_lamports
        self.spent_today = 0

    def can_afford(self, tip: int) -> bool:
        return (self.spent_today + tip) <= self.daily_budget

    def record_tip(self, tip: int) -> None:
        self.spent_today += tip

    def remaining(self) -> int:
        return max(0, self.daily_budget - self.spent_today)

    def reset_daily(self) -> None:
        self.spent_today = 0
```

### Bundle vs Priority Fee Decision

Not every transaction needs a bundle. Compare costs:

```python
def should_use_bundle(
    trade_size_lamports: int,
    estimated_mev_risk_bps: float,
    bundle_tip: int,
    priority_fee: int,
) -> bool:
    """Decide whether a bundle is worth the extra tip cost.

    Args:
        trade_size_lamports: Size of the trade in lamports.
        estimated_mev_risk_bps: Estimated MEV loss in basis points.
        bundle_tip: Cost of bundle tip in lamports.
        priority_fee: Cost of priority fee in lamports.

    Returns:
        True if bundle protection saves more than it costs.
    """
    mev_cost = int(trade_size_lamports * estimated_mev_risk_bps / 10_000)
    bundle_extra_cost = bundle_tip - priority_fee
    return mev_cost > bundle_extra_cost
```

**Rule of thumb:** If MEV risk (in lamports) exceeds the bundle tip premium over a priority fee, use a bundle.

### Tip Minimization

For non-competitive transactions (no one else is trying to do the same trade):

1. Start with the minimum viable tip (5,000-10,000 lamports)
2. If dropped, retry with 1.5x the tip
3. Track your personal landing rate at each tip level
4. Find the minimum tip that gives you an acceptable landing rate (>80%)

```python
def find_minimum_viable_tip(
    landing_rates: dict[int, float],
    target_rate: float = 0.80,
) -> int:
    """Find the lowest tip that achieves the target landing rate.

    Args:
        landing_rates: {tip_amount: landing_rate} from historical data.
        target_rate: Minimum acceptable landing rate (0.0-1.0).

    Returns:
        Minimum tip amount meeting the target.
    """
    for tip, rate in sorted(landing_rates.items()):
        if rate >= target_rate:
            return tip
    # If no tip meets the target, return the highest tested
    return max(landing_rates.keys()) if landing_rates else 50_000
```

## Safety Guardrails

Always implement tip caps to prevent accidental overpayment:

```python
MAX_TIP_LAMPORTS = 10_000_000  # 0.01 SOL hard cap

def safe_tip(tip: int) -> int:
    """Apply safety cap to tip amount."""
    if tip > MAX_TIP_LAMPORTS:
        print(f"WARNING: Tip {tip} exceeds cap {MAX_TIP_LAMPORTS}, capping")
    return min(tip, MAX_TIP_LAMPORTS)
```

**Common tip mistakes:**
- Using SOL instead of lamports (1 SOL = 1,000,000,000 lamports)
- Not capping dynamic tips (congestion spike = 100x tip)
- Tipping on every retry with the same blockhash (waste; bundle won't land anyway)
- Over-tipping non-competitive transactions (nobody is competing for your swap)


---

## SKILL: market-news-analyst

- Fuente: `tradermonty/claude-trading-skills` → `examples/weekly-trade-strategy/.claude/skills/market-news-analyst` (MIT)
- Cuándo usarla: This skill should be used when analyzing recent market-moving news events and their impact on equity markets and commodities. Use this skill when the user requests analysis of major financial news from the past 10 days, wants to understand market reactions to monetary policy decisions (FOMC, ECB, BOJ), needs assessment of geopolitical events' impact on commodities, or requires comprehensive review of earnings announcements from mega-cap stocks. The skill automatically collects news using WebSearch/WebFetch tools and produces impact-ranked analysis reports. All analysis thinking and output are conducted in English.

# Market News Analyst

## Overview

This skill enables comprehensive analysis of market-moving news events from the past 10 days, focusing on their impact on US equity markets and commodities. The skill automatically collects news from trusted sources using WebSearch and WebFetch tools, evaluates market impact magnitude, analyzes actual market reactions, and produces structured English reports ranked by market impact significance.

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
