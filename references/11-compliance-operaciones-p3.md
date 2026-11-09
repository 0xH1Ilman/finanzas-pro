# 11-compliance-operaciones — parte 3

Skills de terceros agrupadas por tema. Cada sección indica fuente, licencia y dónde está su código.



---

## SKILL: pre-trade-compliance

- Fuente: `JoelLewis/finance_skills` → `plugins/trading-operations/skills/pre-trade-compliance` (MIT)
- Cuándo usarla: Guide the design and implementation of automated pre-trade compliance systems that validate orders before execution. Use when building a compliance rule engine for an RIA or broker-dealer, configuring hard blocks and soft blocks, maintaining restricted and watch lists including MNPI-driven restrictions, setting concentration limits at security/sector/issuer level, implementing position limits or short selling controls, enforcing wash sale detection or free-riding prevention or pattern day trader identification, applying client-specific ESG screens or legal constraints, designing compliance override workflows with authorization and documentation, backtesting compliance rules, or evaluating compliance check latency impact on execution quality.

# Pre-Trade Compliance

## Core Concepts

### Pre-Trade Compliance Architecture
The pre-trade compliance system intercepts orders after generation by the portfolio management system or order entry interface and before routing to custodians or execution venues. The system evaluates each order against a set of rules and either permits the order to proceed, blocks it entirely (hard block), or flags it for review (soft block).

**Rule engine design — sequential vs. parallel evaluation:**

- **Sequential evaluation:** Rules are evaluated in a defined order, and processing stops at the first failure. This approach is efficient when early rules are likely to catch the majority of violations (e.g., checking whether the account is frozen before evaluating concentration limits). Sequential evaluation reduces latency for orders that fail early but provides incomplete diagnostic information — the trader sees only the first violation, not all violations.
- **Parallel evaluation:** All rules are evaluated simultaneously, and the system returns the complete set of results. This approach provides comprehensive diagnostic output — the trader sees every rule that the order violates in a single pass. Parallel evaluation is preferred for advisory workflows where orders are reviewed before submission and the compliance team benefits from seeing the full picture. The tradeoff is higher computational cost per order, though for typical advisory order volumes this is negligible.
- **Hybrid approach:** Critical rules (account status, restricted list) are evaluated first as a fast-fail gate. If the order passes these, the remaining rules are evaluated in parallel. This balances latency with diagnostic completeness.

**Order interception points:**

- **Pre-routing:** The compliance check occurs before the order is transmitted to the custodian or execution venue. This is the primary interception point and catches violations before any market interaction. The order exists only within the firm's systems at this stage.
- **Pre-execution:** For firms with direct market access or algorithmic execution capabilities, a second compliance check may occur after routing but before the order is released for execution. This catches issues that arise from market conditions between routing and execution (e.g., a rapidly changing position that now breaches a limit).
- **Post-aggregation, pre-routing:** For block trades, compliance checks should be applied both at the individual account level (does this account violate its concentration limit?) and at the aggregate block level (does the total block size exceed the security's average daily volume threshold?).

**Hard blocks vs. soft blocks:**

- **Hard blocks** prevent the order from proceeding under any circumstances without first resolving the underlying condition. The order cannot be overridden — it must be modified, canceled, or the blocking condition must be removed (e.g., removing a security from the restricted list, unfreezing an account). Hard blocks are reserved for regulatory requirements and firm policies where no exception is permissible: restricted list violations, trading in frozen or suspended accounts, exceeding regulatory position limits, and trading in securities subject to a legal hold.
- **Soft blocks** generate a warning that requires acknowledgment and documented justification before the order can proceed. Soft blocks are appropriate for guidelines where professional judgment may justify an exception: internal concentration guidelines (as opposed to regulatory limits), watch list matches, minor deviations from model allocation, and trades that trigger an advisory alert (e.g., approaching but not exceeding a limit). Every soft block override must be logged with the identity of the authorizer, the timestamp, and the stated justification.

**Compliance check latency requirements:**

Pre-trade compliance checks must complete within a timeframe that does not materially impair execution quality. For equity and ETF orders where market prices are moving, compliance latency directly affects execution price risk. Target latency benchmarks: single-order compliance check should complete in under 100 milliseconds for real-time trading workflows; batch compliance checks for model-driven trades (hundreds or thousands of orders) should complete within seconds, not minutes. Rule engines that require real-time database lookups (e.g., checking a restricted list stored in an external system) must use caching strategies to meet latency targets. Caching strategies include: loading restricted lists and concentration thresholds into memory at system startup with incremental refresh on change events, pre-computing portfolio metrics (sector weights, issuer exposures) and updating them incrementally as positions change rather than recalculating from scratch for each compliance check, and maintaining in-memory snapshots of account-level compliance state that are updated after each trade rather than queried from the database on every check.

**Rule priority and ordering:**

Rules should be organized by priority to ensure that the most critical checks are evaluated first and that rule interactions are handled correctly. A typical priority ordering is: (1) account status checks (frozen, suspended, closed), (2) restricted list screening, (3) regulatory position limits, (4) regulatory compliance rules (wash sale, free-riding), (5) client-specific restrictions, (6) firm-level concentration limits, (7) model and guideline compliance. When multiple rules fire on the same order, the most restrictive outcome governs — a hard block from any rule overrides soft blocks from other rules.

### Restricted and Watch Lists
Restricted and watch lists are central compliance tools that control trading in securities where the firm or its personnel have conflicts, information advantages, or regulatory obligations.

**Firm restricted list (MNPI-driven):**

The firm restricted list contains securities in which the firm or its affiliates possess material non-public information (MNPI). For broker-dealers with investment banking affiliates, the restricted list is populated when the firm is engaged in an advisory assignment (M&A, underwriting, restructuring) involving a public company. Trading in restricted list securities is prohibited across all firm accounts — proprietary, advisory, and personal. The restricted list is maintained by the compliance department, typically with input from the legal department and information barriers (Chinese walls) group. Additions and removals are time-sensitive: a security must be added before MNPI is disseminated within the firm and may only be removed after the information becomes public or the engagement terminates.

**Personal trading restricted list:**

Access persons — employees with access to non-public information about client trades, portfolio holdings, or investment recommendations — are subject to personal trading restrictions. The personal trading restricted list may include securities that the firm is actively trading for clients (to prevent front-running), securities under active research coverage, and IPO and limited offering securities (which require pre-clearance under SEC Rule 204A-1). Personal trading restrictions operate independently of the firm restricted list and may be more or less restrictive depending on the employee's role.

**Client-specific restricted securities:**

Individual client accounts may have their own restricted securities lists arising from legal constraints (insider status in a company, divorce decree prohibiting sale of certain holdings), contractual obligations (lock-up agreements), or client preferences (client instructs the firm not to purchase securities of a specific company). These restrictions are maintained at the account level and checked during pre-trade compliance for that specific account.

**Issuer restriction propagation (parent/subsidiary):**

When a security is added to the restricted list, the restriction must propagate to related securities. If the parent company is restricted, all subsidiaries, affiliates, and related entities should also be restricted. This requires maintaining an issuer hierarchy that maps corporate relationships. The propagation should cover: common stock, preferred stock, convertible securities, options, warrants, debt securities, and any other instruments issued by or linked to the restricted issuer. Failure to propagate restrictions across the corporate family is a common compliance gap that regulators specifically test for.

**Watch list vs. restricted list (different actions):**

The watch list contains securities that are under heightened surveillance but not subject to an outright trading prohibition. Watch list securities may be traded, but trades generate alerts for compliance review. The watch list is used when the firm has reason to monitor trading in a security but the information or situation does not rise to the level requiring a full restriction — for example, when the firm is in early-stage discussions about a potential engagement, when rumors are circulating about a company the firm covers, or when an employee has reported a potential conflict. Watch list matches produce soft blocks; restricted list matches produce hard blocks.

**Gray list (additional surveillance tier):**

Some firms maintain a gray list in addition to the restricted and watch lists. The gray list is used for securities where the firm may soon receive MNPI but has not yet — for example, when an investment banking pitch is in progress but no engagement letter has been signed. Gray list securities are not restricted from trading, but all trades are flagged for post-trade review by the compliance surveillance team. The gray list provides an early warning mechanism and helps establish that the firm had surveillance procedures in place before MNPI was received, which can be important in defending against insider trading allegations.

**List maintenance and updates:**

Restricted and watch lists must be updated promptly as circumstances change. Stale lists create two risks: (1) securities that should be restricted are not, exposing the firm to insider trading liability, and (2) securities that should have been removed remain restricted, unnecessarily blocking legitimate trading. Best practices include: real-time or daily list updates, automated feeds from deal management systems (for investment banking-driven restrictions), regular review cycles to confirm that all entries remain valid, and audit trails documenting every addition, removal, and modification with the reason and authorizing person.

### Concentration Limits
Concentration limits prevent excessive exposure to a single security, issuer, sector, or asset class. These limits serve both risk management and regulatory compliance purposes.

**Security-level concentration:**

The most common concentration limit restricts the maximum percentage of a portfolio that may be invested in a single security. Typical thresholds range from 5% to 10% of account value for a single equity position. The compliance system must calculate the post-trade position value (current holding plus the proposed order) as a percentage of the account's total value and compare it against the limit. For buy orders, the check is straightforward: will this purchase cause the position to exceed X% of the portfolio? For sell orders in other securities, the check must consider whether the sale changes the denominator (total portfolio value) such that remaining positions now exceed their concentration limits.

**Sector and industry limits:**

Sector limits restrict aggregate exposure to a single GICS sector (e.g., no more than 25% in Technology) or industry (e.g., no more than 10% in Semiconductors). Implementing sector limits requires mapping every security in the portfolio to its sector and industry classification, which in turn requires a reliable security master database with current classification data. Sector limit checks must aggregate all positions within the sector, including the proposed trade, and compare the total against the limit.

**Asset class limits:**

Asset class limits restrict exposure across broad categories: equities, fixed income, alternatives, cash. These limits typically derive from the investment policy statement (IPS) and are expressed as ranges (e.g., equity 40-70%, fixed income 20-50%, alternatives 0-15%, cash 1-5%). The pre-trade compliance check verifies that the proposed trade does not push any asset class allocation outside its permitted range.

**Issuer limits:**

Issuer limits restrict total exposure to a single issuer across all security types. A client may hold common stock, corporate bonds, and convertible notes from the same issuer — the issuer limit aggregates all of these exposures. This is particularly important for credit risk management: if an issuer defaults, all securities are affected regardless of type.

**Regulatory limits (registered funds):**

The Investment Company Act of 1940 imposes specific diversification requirements on registered investment companies (mutual funds). A diversified fund must meet the 75-5-10 test: at least 75% of the fund's assets must be diversified such that no more than 5% of total assets is invested in any single issuer and no more than 10% of an issuer's outstanding voting securities is held. The remaining 25% of assets is not subject to these limits. These are hard regulatory limits that produce hard blocks.

**Aggregation across accounts and households:**

Some concentration limits apply not just to individual accounts but across related accounts — a household, a family group, or all accounts managed by the same strategy. Household-level concentration limits require the compliance system to aggregate holdings across all accounts in the household before evaluating the limit. This prevents a situation where each individual account is within limits but the household's total exposure to a single security or sector is excessive. Aggregation adds complexity because accounts may be held at different custodians, in different account types (taxable, IRA, trust), and with different investment policies.

### Position and Exposure Limits
Position and exposure limits control the absolute size and risk exposure of positions, complementing the percentage-based concentration limits.

**Maximum position size:**

Absolute limits on the number of shares or notional value of a position in a single security. These limits may be set at the account level, strategy level, or firm level. Firm-level position limits prevent the firm's aggregate holdings in a single security from becoming large enough to trigger regulatory reporting thresholds (e.g., Schedule 13D/13G filing requirements at 5% of outstanding shares) or to create market impact and liquidity concerns.

**Notional exposure limits:**

For derivatives and leveraged instruments, notional exposure limits cap the total economic exposure regardless of the cash outlay. A portfolio with $1 million in assets that holds $5 million in notional futures exposure has 5x leverage. Notional exposure limits are essential for strategies that use derivatives, as a small cash investment can create disproportionate market exposure. The compliance system must calculate notional exposure by multiplying the number of contracts by the contract multiplier and the underlying price.

**Options position limits (exchange-imposed):**

Securities exchanges impose position limits on listed options that cap the number of contracts on the same side of the market (all calls and short puts, or all puts and short calls) that any person or group of persons acting in concert may hold or write. Position limits vary by underlying security based on trading volume and float. The OCC (Options Clearing Corporation) publishes current position limits. Exceeding exchange-imposed position limits results in regulatory action and potential forced liquidation.

**Short selling restrictions:**

Regulation SHO governs short selling in the United States and imposes several pre-trade requirements:
- **Locate requirement:** Before executing a short sale, the broker-dealer must have reasonable grounds to believe that the security can be borrowed and delivered by the settlement date. This locate must be documented before the short sale order is submitted.
- **Hard-to-borrow lists:** Securities for which borrows are difficult to obtain are maintained on hard-to-borrow lists. Short sales in these securities may require pre-borrows (actually borrowing the shares before executing the sale) rather than locates.
- **Threshold securities:** Securities with significant fails to deliver are placed on the threshold security list. Additional close-out requirements apply to short positions in threshold securities.
- **Alternative uptick rule (Rule 201):** When a security's price declines by 10% or more from the prior day's close, short sale price restrictions are triggered for the remainder of the day and the following day. Short sales may only be executed at a price above the current national best bid.

**Leverage limits:**

For margin accounts, Regulation T sets initial margin requirements (generally 50% for equity securities), and FINRA Rule 4210 sets maintenance margin requirements (generally 25% for long positions, 30% for short positions). The pre-trade compliance system must verify that the proposed trade does not cause the account to exceed its margin capacity or fall below maintenance requirements. For portfolio margin accounts, the calculation is more complex and uses a risk-based methodology.

### Regulatory Compliance Rules
Pre-trade compliance systems must enforce specific regulatory rules that govern trading conduct.

**Wash sale detection (30-day window):**

IRC Section 1091 disallows a tax loss deduction if the taxpayer purchases a "substantially identical" security within 30 days before or after the sale at a loss (the 61-day window). The pre-trade compliance system should flag potential wash sales by: (1) checking whether the account sold the same or substantially identical security at a loss within the prior 30 days (repurchase triggers wash sale), and (2) checking whether there is a pending or planned purchase of the same security within 30 days after a proposed loss sale. Substantially identical securities include the same stock, options on the same stock, and in some interpretations, ETFs tracking the same index. Wash sale detection across related accounts (spouse, IRA) adds complexity, as the IRS applies wash sale rules across accounts controlled by the same taxpayer.

**Free-riding prevention (Regulation T):**

In a cash account (non-margin), a customer may not purchase a security and sell it before paying for it in full. If a customer buys a security, the purchase must be paid for by the settlement date (T+1). If the customer sells the security before payment, this constitutes free-riding, and the account is subject to a 90-day freeze (all purchases must be made with settled funds for 90 days). The pre-trade compliance system must track unsettled purchases and prevent sales of unpaid-for securities in cash accounts.

**Pattern day trader detection:**

FINRA Rule 4210 defines a pattern day trader as a customer who executes four or more day trades (buying and selling the same security on the same day) within five business days, provided the number of day trades is more than 6% of the customer's total trading activity in that period. Pattern day traders must maintain at least $25,000 in equity in their margin account. The pre-trade compliance system should count day trades over the rolling five-day window and alert or block when the threshold is approached.

**Mutual fund market timing restrictions:**

Frequent trading in mutual fund shares (rapid purchases and redemptions) can harm long-term shareholders through dilution and increased transaction costs. Most mutual fund prospectuses include market timing policies that restrict round-trip transactions within specified periods (often 30 to 90 days). The pre-trade compliance system should track mutual fund purchase and redemption activity and flag transactions that violate the fund's stated market timing policy. SEC Rule 22c-2 requires funds to have agreements with intermediaries to share shareholder transaction data for market timing surveillance.

**Insider trading prevention (Section 16, Rule 144):**

Section 16 of the Securities Exchange Act requires corporate insiders (officers, directors, and 10% beneficial owners) to report their transactions and disgorge short-swing profits (profits from purchases and sales within a six-month window). Rule 144 restricts the resale of control and restricted securities, imposing holding period requirements and volume limitations. When the firm manages accounts for corporate insiders, the pre-trade compliance system must enforce: (1) pre-clearance requirements before any trade in the insider's company securities, (2) blackout period restrictions (insiders typically cannot trade during the period before earnings announcements), (3) Rule 144 volume limits (sales in any three-month period cannot exceed the greater of 1% of outstanding shares or the average weekly trading volume over the prior four weeks), and (4) Form 4 filing coordination.

**ERISA prohibited transaction rules:**

For accounts subject to the Employee Retirement Income Security Act (ERISA), certain transactions between the plan and "parties in interest" (fiduciaries, service providers, employers, unions) are prohibited. The pre-trade compliance system must maintain a list of parties in interest for each ERISA plan account and block transactions that would constitute prohibited transactions — for example, purchasing securities issued by the plan sponsor or its affiliates, or engaging in lending or leasing arrangements with parties in interest. Exemptions exist under Prohibited Transaction Exemptions (PTEs) issued by the Department of Labor, and the system should be configurable to recognize applicable exemptions.

### Client-Specific Restrictions
Beyond firm-wide and regulatory rules, individual client accounts may carry specific restrictions that the compliance system must enforce.

**Investment policy constraints:**

The investment policy statement (IPS) for each account may specify exclusions based on industry (no tobacco, no firearms, no gambling), geography (no emerging markets, no specific countries), security type (no derivatives, no structured products, no private placements), quality (investment-grade bonds only, no below-BBB), or other criteria. These constraints are mapped to security attributes and enforced as hard or soft blocks depending on the strength of the restriction. IPS constraints should be coded into the compliance system at account onboarding and updated when the IPS is revised.

**Tax-loss harvesting coordination:**

Accounts actively engaged in tax-loss harvesting require compliance coordination to avoid wash sales. When one account sells a security at a loss for tax purposes, the compliance system must prevent repurchase of the same or substantially identical security within the 30-day wash sale window — not only in the same account but across all accounts for the same taxpayer (including spouse's accounts and IRAs). This requires cross-account wash sale monitoring with household-level linkage.

**Legally restricted securities:**

Court orders, divorce decrees, trust provisions, and other legal documents may restrict trading in specific securities or impose conditions on transactions. Examples include: a divorce decree prohibiting the sale of marital property (including securities) during proceedings, a trust provision requiring trustee approval before selling concentrated positions, a court-ordered freeze on assets pending litigation, or restrictions imposed by a regulatory consent order. These restrictions are typically entered manually by compliance and coded as hard blocks.

**ESG/SRI screens:**

Environmental, social, and governance (ESG) screens and socially responsible investing (SRI) criteria exclude securities based on non-financial factors. Common screens include: fossil fuel exclusion (companies deriving more than a specified percentage of revenue from coal, oil, or gas extraction), weapons exclusion (manufacturers of controversial weapons, civilian firearms), tobacco and alcohol exclusion, animal testing exclusion, and human rights screens. ESG screens require mapping securities to ESG data providers (MSCI ESG, Sustainalytics, ISS ESG) and maintaining current classification data. Because ESG classifications can change as companies evolve, the screening data must be refreshed regularly.

**Account-level trading restrictions:**

Certain account-level conditions require trading restrictions: frozen accounts (pending regulatory action, suspicious activity investigation, or customer dispute), accounts with pending paperwork (incomplete account opening documentation, unsigned IPS, missing beneficiary designation), accounts in estate settlement (trading freeze pending legal authority confirmation), and accounts subject to garnishment or levy (where outgoing transactions may be prohibited). These account-level flags produce hard blocks on all or specific types of trading activity.

### Compliance Override Workflow
Soft blocks require a structured override process that balances operational efficiency with compliance rigor.

**Soft block review process:**

When a soft block fires, the order is held in a pending compliance review status. The system presents the compliance officer or authorized reviewer with: the order details, the rule that triggered the block, the current state of the relevant metric (e.g., "this purchase would bring the Technology sector allocation to 27%, exceeding the 25% guideline"), and any relevant context (e.g., the account's IPS permits tactical overweights of up to 5% with advisor approval). The reviewer evaluates whether the trade is justified despite the guideline breach and either approves (overrides) or rejects the order.

**Override authorization levels:**

Not all overrides should be authorized at the same level. A tiered authorization structure matches the severity of the override to the seniority of the authorizer:
- **Level 1 (trader/advisor):** Minor guideline deviations within a defined tolerance (e.g., concentration exceeds guideline by less than 2 percentage points). The trader or advisor can self-authorize with documentation.
- **Level 2 (compliance officer):** Moderate deviations or watch list matches. A compliance officer must review and approve.
- **Level 3 (chief compliance officer or committee):** Significant deviations, repeated overrides of the same rule for the same account, or overrides involving heightened regulatory risk. Requires CCO or compliance committee approval.

**Override documentation requirements:**

Every override must be documented with: (1) the order details, (2) the rule that was triggered, (3) the quantitative details of the violation (how far the metric exceeds the threshold), (4) the identity of the person requesting the override, (5) the identity of the person authorizing the override, (6) the timestamp of the authorization, (7) the stated justification for the override, and (8) any conditions attached to the approval (e.g., "approved provided the overweight is reduced within 30 days"). This documentation must be retained as part of the firm's compliance records and is subject to regulatory examination.

**Escalation procedures:**

When a reviewer is uncertain about whether to approve an override, or when the override involves a particularly sensitive situation (e.g., a trade that raises potential insider trading concerns), the system should provide a clear escalation path. Escalation may route the override to the CCO, the legal department, or a compliance committee. The escalation path and the resolution must be documented.

**Post-override audit:**

Compliance should periodically audit override activity to identify patterns and systemic issues. The audit should examine: the total volume and frequency of overrides, overrides by rule type (which rules are most frequently overridden), overrides by account or advisor (are certain advisors consistently triggering and overriding the same rules), whether conditions attached to approved overrides were fulfilled (e.g., was the overweight actually reduced within 30 days as required), and whether any overrides resulted in adverse outcomes (client harm, regulatory issues).

**Pattern analysis of overrides:**

If the same rule is being overridden frequently, it may indicate that the rule threshold is miscalibrated (too tight, generating excessive false positives), that a particular advisor or strategy systematically operates outside the guideline (requiring either a guideline adjustment or a strategy change), or that the rule is no longer appropriate given current market conditions or regulatory requirements. Override pattern analysis feeds directly into the rule tuning process.

### Rule Configuration and Maintenance
The effectiveness of the pre-trade compliance system depends on ongoing rule management — adding new rules, modifying thresholds, retiring obsolete rules, and ensuring that the rule set reflects current regulatory requirements and firm policies.

**Adding and modifying rules:**

New rules may be required when regulations change, the firm enters a new business line, or compliance identifies a gap in the existing rule set. The rule addition process should include: (1) defining the rule logic (what condition triggers the block, what type of block is produced), (2) setting the threshold or parameter values, (3) determining which accounts or account types the rule applies to, (4) testing the rule against historical order data to assess its impact (how many orders would it have blocked), (5) obtaining approval from the CCO or compliance committee, (6) deploying the rule in a monitoring-only mode before activating blocking (shadow mode), and (7) activating the rule with blocking enabled after the shadow period confirms expected behavior.

**Backtesting rules against historical orders:**

Before activating a new rule or modifying a threshold, the rule should be backtested against a representative sample of historical orders. Backtesting reveals: the expected block rate (percentage of orders that would be blocked), the false positive rate (orders that would be blocked but are actually legitimate), and the false negative rate (orders that should be blocked but are not caught). This data informs threshold calibration and helps the compliance team anticipate the operational impact of the new rule.

**False positive analysis:**

A high false positive rate undermines the compliance system's credibility and creates operational friction. If traders and advisors routinely override soft blocks because the blocks are perceived as invalid, they may develop "alert fatigue" and begin overriding blocks without proper evaluation — including blocks that are valid. The compliance team should track the override rate for each rule and investigate rules with override rates above a defined threshold (e.g., rules overridden more than 50% of the time). Remediation may include adjusting the threshold, refining the rule logic, or reclassifying the rule from a soft block to a monitoring alert.

**Rule tuning:**

Rule tuning is the ongoing process of adjusting thresholds and parameters to optimize the balance between catching genuine violations and minimizing false blocks. Tuning should be data-driven: the compliance team analyzes block rates, override rates, and the outcomes of overridden trades to determine whether thresholds are appropriately calibrated. Tuning decisions should be documented and approved by the CCO.

**Rule version control:**

The compliance rule set should be subject to version control, similar to software code. Each rule change — addition, modification, threshold adjustment, or retirement — should be recorded with the effective date, the person who made the change, the approval, and the reason. Version control enables the compliance team to reconstruct the rule set that was in effect on any historical date, which is essential for regulatory examinations and investigations that require demonstrating what controls were in place at the time of a particular trade.

**Regulatory change management:**

When regulations change, the compliance team must assess the impact on the pre-trade compliance rule set and implement necessary modifications. This requires monitoring regulatory developments (SEC releases, FINRA regulatory notices, exchange rule changes), analyzing the impact on existing rules, modifying or adding rules as needed, backtesting the modified rules, and deploying changes before the regulatory effective date. A regulatory change management calendar should track upcoming effective dates and the status of rule modifications.

## Worked Examples

Three worked examples are in [references/examples.md](references/examples.md) — load for an end-to-end scenario: (1) designing a pre-trade compliance rule engine for a multi-custodian RIA, (2) implementing restricted list management for a broker-dealer with investment banking affiliates, (3) configuring household-level concentration limits around a legacy concentrated position.

## Common Pitfalls
- Implementing only account-level concentration limits without household-level aggregation, allowing excessive household exposure to build across related accounts
- Failing to propagate restricted list entries across the corporate family (parent, subsidiaries, affiliates), leaving gaps that regulators specifically test for
- Setting all compliance violations to hard blocks, creating operational gridlock; the distinction between hard and soft blocks is essential for balancing compliance with trading efficiency
- Not tracking or analyzing override patterns, missing systemic issues such as miscalibrated thresholds or advisors who routinely circumvent guidelines
- Deploying new rules directly into production without backtesting or shadow-mode testing, causing unexpected blocks that disrupt trading operations
- Maintaining stale restricted or watch lists — securities that should have been removed remain, blocking legitimate trades, while securities that should be added are missed
- Ignoring compliance check latency, allowing slow rule evaluation to degrade execution quality for time-sensitive orders
- Applying the same concentration limits to all account sizes without considering that small accounts require different thresholds due to position sizing constraints
- Not coordinating wash sale detection across accounts within a household, undermining tax-loss harvesting programs
- Failing to version-control compliance rules, making it impossible to reconstruct the rule set in effect at the time of a historical trade during regulatory examinations
- Treating pre-trade compliance as a one-time implementation rather than an ongoing process requiring regular backtesting, tuning, and regulatory change management
- Allowing compliance rule overrides without structured documentation, creating examination risk when regulators request override justification records
- Checking concentration limits only on buy orders without considering that sell orders in other positions can change the denominator (total portfolio value) and push remaining positions above their percentage thresholds
- Relying on a single ESG data provider without periodic validation, leading to stale or inconsistent screening results as company classifications change over time
- Not distinguishing between regulatory position limits (which must be hard blocks) and internal risk guidelines (which may be soft blocks), applying inappropriate block types that either create unnecessary rigidity or insufficient control

## Cross-References
- **order-lifecycle** (trading-operations plugin): Pre-trade compliance is a critical stage in the order lifecycle, intercepting orders between generation and routing; the order lifecycle skill provides the broader context for where compliance checks fit in the trade flow
- **post-trade-compliance** (trading-operations plugin): Post-trade compliance monitoring detects violations that were not caught pre-trade, including violations arising from market movements after execution; together, pre-trade and post-trade compliance form a complete compliance surveillance framework
- **order-management-advisor** (advisory-practice plugin): The OMS executes the compliance check workflow, manages hard and soft block statuses, and records override documentation as part of the trade audit trail
- **investment-suitability** (compliance plugin): Suitability and best interest analysis overlaps with pre-trade compliance at the point of evaluating whether a trade is appropriate for the client's risk profile, investment objectives, and financial situation
- **conflicts-of-interest** (compliance plugin): Restricted list management and personal trading restrictions are direct conflict-of-interest controls; the conflicts-of-interest skill covers the broader framework for identifying and mitigating conflicts
- **investment-policy** (wealth-management plugin): IPS constraints — asset class ranges, quality minimums, exclusion lists — are encoded as pre-trade compliance rules; changes to the IPS require corresponding updates to the compliance rule configuration
- **portfolio-management-systems** (advisory-practice plugin): The PMS generates trade proposals that feed into the pre-trade compliance engine; compliance check results flow back to the PMS to inform portfolio managers of blocked or flagged trades
- **books-and-records** (compliance plugin): Override documentation, compliance check results, and rule change records are part of the firm's books and records subject to SEC and FINRA retention requirements
- **settlement-clearing** (trading-operations plugin): Settlement timing affects free-riding detection and cash availability checks; the T+1 settlement cycle determines the window within which pre-trade compliance must validate that funds or securities will be available

### Referencia: references/examples.md

# Pre-Trade Compliance — Worked Examples

### Example 1: Designing a Pre-Trade Compliance Rule Engine for a Multi-Custodian RIA

**Scenario:** A registered investment adviser manages $3 billion across 4,500 accounts custodied at Schwab, Fidelity, and Pershing. The firm uses model-based portfolio management with 12 model portfolios ranging from conservative income to aggressive growth. The compliance team needs to design a pre-trade compliance rule engine that can handle batch compliance checks for model-driven trades (up to 10,000 orders per model change) as well as real-time checks for individual advisor-initiated trades.

**Design Considerations:**

The rule engine architecture uses a hybrid evaluation approach. A fast-fail gate evaluates the three most critical rules first in sequence: (1) account status — is the account frozen, suspended, or closed? (2) restricted list — is the security on the firm restricted list? (3) account trading authority — does the firm have discretionary authority or has the client authorized this specific trade? If any of these fail, the order is immediately hard-blocked without evaluating further rules, saving computational resources. Orders that pass the fast-fail gate proceed to parallel evaluation of all remaining rules.

The rule set is organized into seven categories with defined block types:

Category 1 — Account status rules (hard block): Account must be in active status. Account must not be flagged for pending paperwork, regulatory hold, estate settlement, or AML investigation. These rules check account-level flags in the client master database.

Category 2 — Restricted and watch list rules: Firm restricted list match produces a hard block. Watch list match produces a Level 2 soft block (requires compliance officer approval). Personal trading restricted list match produces a hard block for employee accounts. Client-specific restricted security match produces a hard block for that account.

Category 3 — Concentration limits: Single security exceeding 10% of account value produces a Level 1 soft block (advisor can self-authorize with documentation). Single security exceeding 15% produces a Level 2 soft block. Single sector exceeding 30% produces a Level 1 soft block. Single issuer (aggregated across all security types) exceeding 10% produces a Level 2 soft block. These thresholds apply to the post-trade position — the compliance check must calculate what the portfolio will look like after the proposed trade is executed.

Category 4 — Regulatory limits: Wash sale detection (30-day window, cross-account within household) produces a Level 1 soft block with detailed diagnostic information showing the prior loss sale and the wash sale tax consequence. Free-riding detection in cash accounts produces a hard block. Pattern day trader detection (approaching four day trades in five business days) produces a Level 2 soft block.

Category 5 — Client-specific restrictions: IPS asset class range violation produces a Level 1 soft block. ESG screen violation produces a hard block (if the client has a formal ESG mandate) or Level 1 soft block (if the ESG screen is advisory). Tax-loss harvesting wash sale coordination produces a hard block (the tax benefit is the explicit purpose, so overriding defeats the objective).

Category 6 — Position and exposure limits: Firm-level aggregate position exceeding 3% of a security's outstanding shares produces a Level 3 soft block (CCO approval required, due to 13D/13G reporting implications). Account-level notional exposure exceeding 150% of account value produces a Level 2 soft block.

Category 7 — Model and guideline compliance: Trade deviating from the model allocation by more than 5 percentage points produces a Level 1 soft block. Trade in a security not included in any approved model produces a Level 1 soft block (to catch unauthorized ad hoc trades).

For batch processing of model-driven trades, the engine processes orders in three phases. Phase 1: aggregate all orders by security and calculate the total firm-level position post-trade to check firm-level limits once rather than per-order. Phase 2: evaluate account-level rules for each order in parallel across multiple processing threads. Phase 3: compile results and present the compliance summary showing the total order count, the number passing all checks, the number with soft blocks (by level), and the number with hard blocks.

**Analysis:**

The design prioritizes diagnostic completeness over raw speed for the batch workflow — when processing 10,000 orders from a model change, the compliance team needs to see all violations across all accounts to make informed decisions about overrides and exclusions. For the real-time single-order workflow, the fast-fail gate ensures that obviously non-compliant orders are blocked immediately while the full rule set is evaluated in under 200 milliseconds. The tiered override structure ensures that routine guideline deviations can be handled efficiently by advisors while significant deviations require compliance officer or CCO involvement. All override activity flows into a monthly compliance report that tracks override volume, frequency by rule, and patterns by advisor.

### Example 2: Implementing Restricted List Management for a Broker-Dealer with Investment Banking Affiliates

**Scenario:** A full-service broker-dealer has an investment banking division that engages in M&A advisory, equity underwriting, and debt capital markets. The firm also operates a wealth management division serving 15,000 retail and high-net-worth clients, and a proprietary trading desk. The compliance department must implement a restricted list management system that prevents insider trading violations while minimizing unnecessary trading restrictions.

**Design Considerations:**

The restricted list system has three distinct lists with different scopes and actions:

The firm restricted list is driven by investment banking engagements. When the investment banking division begins work on a transaction involving a public company, the compliance department adds the issuer to the restricted list. The addition includes: the issuer name, all related ticker symbols, CUSIP numbers for all outstanding securities (common stock, preferred stock, convertible bonds, corporate bonds), the date of addition, the reason (type of engagement), and the expected duration. The restriction applies to all firm accounts: proprietary trading, wealth management client accounts, and employee personal accounts. The restriction produces a hard block on all buy and sell orders.

Issuer propagation is critical. When the firm is advising on an acquisition of Company A by Company B, both issuers and all their subsidiaries must be restricted. The compliance system maintains a corporate hierarchy database sourced from a third-party data provider (such as Bloomberg or Refinitiv) that maps parent-subsidiary relationships. When Company A is added to the restricted list, the system automatically identifies and restricts all subsidiaries and affiliates. The compliance team reviews the propagated list to confirm completeness and add any entities not captured by the automated hierarchy (such as recently formed joint ventures or entities with non-obvious corporate relationships).

The watch list contains securities where the firm has reason for heightened surveillance but has not determined that a full restriction is warranted. This includes: companies where the investment banking division is in preliminary discussions (before a formal engagement letter is signed), companies where a research analyst has recently changed a rating or is preparing to publish a significant research report, and companies where the compliance department has received a tip or complaint about potential insider trading. Watch list matches produce soft blocks that route to the compliance surveillance team for review before the trade is permitted to proceed.

The personal trading restricted list adds further restrictions for firm employees. In addition to the firm restricted list (which already applies to personal accounts), employees in the investment banking division are prohibited from trading in any securities of companies within their coverage sector for the duration of their assignment. Research analysts are prohibited from trading in securities they cover. All access persons must pre-clear personal trades through the compliance system, and the pre-clearance check validates against all three lists.

List maintenance follows a defined workflow. Additions to the firm restricted list require: a request from the investment banking division's deal team or the compliance department, approval by the compliance officer or designated deputy, and immediate distribution to all trading desks and the OMS. Removals require: confirmation that the engagement has concluded or the MNPI has become public (e.g., the transaction was announced or the engagement was terminated), approval by the compliance officer, and a documented record of the removal date and reason. The compliance department conducts a weekly review of the restricted list to confirm that all entries remain valid, with quarterly comprehensive audits that reconcile the restricted list against the active engagement list from investment banking.

**Analysis:**

The system must balance insider trading prevention with operational efficiency. Over-restriction — keeping securities on the restricted list longer than necessary or restricting overly broad corporate families — prevents legitimate client trading and creates client dissatisfaction. Under-restriction — failing to add securities promptly or missing related entities — creates regulatory risk. The compliance team tracks metrics including: average time from engagement commencement to restricted list addition (target: same business day), average time from engagement termination to list removal (target: within two business days of public announcement), the number of false-hit blocks per month (orders blocked that are subsequently determined to be legitimate), and the number of watch list escalations that result in full restriction. These metrics are reported to the Chief Compliance Officer monthly and inform process improvements.

### Example 3: Configuring Concentration and Diversification Limits Across a Household of Accounts

**Scenario:** A high-net-worth household has five accounts at the firm: a joint taxable account ($2M), the husband's IRA ($800K), the wife's IRA ($600K), a revocable trust ($1.5M), and a custodial account for a minor child ($100K). Total household assets: $5M. The family's patriarch is a retired executive of a large technology company and holds 40% of the joint taxable account ($800K) in concentrated stock of his former employer. The compliance team must configure concentration limits that address both individual account diversification and household-level exposure, while accommodating the legacy concentrated position.

**Design Considerations:**

The concentration limit configuration operates at two levels: account-level and household-level.

Account-level limits are set per account based on the account's investment policy. The joint taxable account has a special carve-out for the legacy concentrated position: the standard single-security limit of 10% is suspended for the employer stock, but a separate declining limit is established — the position must not exceed 45% of the account currently (providing a 5-percentage-point buffer above the current 40% holding) and must decline to 30% within two years as the family executes a systematic diversification plan. Any purchase of additional employer stock is hard-blocked. All other securities in the joint account are subject to the standard 10% single-security limit and a 30% single-sector limit. The IRAs and trust are subject to standard limits: 10% single security, 30% single sector, and asset class ranges per the IPS (equity 50-70%, fixed income 25-45%, alternatives 0-10%, cash 1-5%). The custodial account, given its smaller size, has a relaxed single-security limit of 15% (because a $100K account holding a minimum position size of $5K would reach 5% concentration with a single position, making a strict 10% limit impractical without limiting the number of holdings to fewer than 20).

Household-level limits aggregate holdings across all five accounts. The household single-security limit is set at 10% of total household assets ($500K). The employer stock position ($800K, or 16% of household assets) currently exceeds this limit. Because this is a legacy position under an active diversification plan, the household limit for this specific security is set at 18% currently with a declining schedule matching the account-level diversification plan. The household single-sector limit is 30%. Given that the employer stock is a technology company and the household already has 16% of assets in this single technology stock, the effective available allocation to other technology securities across all accounts is limited to approximately 14% of household assets (30% sector limit minus 16% in the concentrated position).

The compliance system must perform cross-account aggregation in real-time. When a trade is proposed in any of the five accounts, the system must: (1) look up the household linkage for that account, (2) retrieve current positions in all linked accounts, (3) calculate the post-trade household-level exposure for the relevant security, sector, and asset class, and (4) compare against household-level limits. This cross-account check must also run for wash sale monitoring — if the husband's IRA sells a security at a loss, the system must prevent the joint account, wife's IRA, trust, or custodial account from purchasing the same or substantially identical security within the 30-day wash sale window.

**Analysis:**

The configuration accommodates the reality that high-net-worth households often have legacy concentrated positions that cannot be immediately eliminated. The declining limit schedule creates a compliance-enforced glide path for diversification — the system will automatically begin hard-blocking if the position exceeds the scheduled limit, providing a structural mechanism to ensure the diversification plan stays on track. The household-level aggregation prevents the family from inadvertently building additional concentration by purchasing the same securities across multiple accounts. The cross-account wash sale monitoring protects the tax benefits of tax-loss harvesting across the household. The compliance team reviews the household-level limits quarterly and adjusts the declining schedule for the concentrated position based on market conditions, tax considerations, and the family's progress toward their diversification target.


---

## SKILL: privacy-data-security

- Fuente: `JoelLewis/finance_skills` → `plugins/compliance/skills/privacy-data-security` (MIT)
- Cuándo usarla: Design and operate privacy and data security programs for SEC-registered firms under Reg S-P, Reg S-ID, and SEC cybersecurity expectations. Use when the user asks about privacy notices, the Safeguards Rule, identity theft prevention programs, breach notification obligations, vendor security due diligence, incident response planning, data classification, or state privacy law compliance. Also trigger when users mention 'customer data was exposed', 'do we need to notify clients of a breach', 'cybersecurity exam prep', 'cloud vendor risk assessment', 'encrypting client data', 'BYOD security policy', 'Red Flags Rule', 'NY DFS 500 requirements', or ask how to handle a cybersecurity incident.

# Privacy and Data Security

Regulatory status current as of June 2026 — verify effective dates, dollar thresholds, and pending rulemakings against current SEC/FINRA/FinCEN sources before advising.

## Core Concepts

### Regulation S-P (Privacy of Consumer Financial Information)
Regulation S-P (17 CFR Part 248, Subparts A and B) implements Title V of the Gramm-Leach-Bliley Act (GLBA) for entities registered with the SEC. It applies to SEC-registered investment advisers, broker-dealers, investment companies, and transfer agents. The regulation has three core components:

**Privacy Notice Requirements.** Firms must provide an initial privacy notice to each customer at the time of establishing the customer relationship (17 CFR 248.4). The notice must describe: (a) categories of nonpublic personal information (NPI) collected, (b) categories of NPI disclosed to third parties, (c) categories of affiliates and nonaffiliated third parties to whom NPI is disclosed, (d) the customer's right to opt out of certain disclosures, (e) the firm's policies and practices for protecting confidentiality and security of NPI, and (f) any disclosures required under the Fair Credit Reporting Act. Annual privacy notices must be delivered once during each 12-month period for the duration of the customer relationship (17 CFR 248.5). The FAST Act of 2015 (Pub. L. 114-94, Section 75001) created an exception to the annual notice requirement: firms that (i) share NPI only under the exceptions in 17 CFR 248.14 and 248.15, and (ii) have not changed their privacy policies and practices since the most recent notice, may satisfy the annual requirement by posting the privacy notice continuously on their website in a clear and conspicuous manner rather than mailing it to each customer.

**Opt-Out Requirements.** Before sharing NPI with nonaffiliated third parties, firms must provide customers with a reasonable opportunity to opt out (17 CFR 248.7 and 248.10). The opt-out notice must be clear, conspicuous, and delivered along with or as part of the privacy notice. Exceptions to the opt-out requirement include: (a) disclosures necessary to effect, administer, or enforce a transaction requested by the customer, (b) disclosures to service providers and joint marketing partners under written contractual agreements that restrict the third party's use of NPI, (c) disclosures with customer consent, (d) disclosures to protect against fraud, and (e) disclosures required by law (17 CFR 248.14 and 248.15). Joint marketing agreements must include written contracts specifying that the third party will maintain the confidentiality of NPI and will use it only for the purposes for which it was disclosed.

**Safeguards Rule.** Section 248.30 requires every covered institution to adopt written policies and procedures that address administrative, technical, and physical safeguards for the protection of customer records and information. Administrative safeguards include designating a responsible employee or officer, conducting risk assessments, implementing employee training, and establishing oversight of service providers. Technical safeguards include access controls, encryption, intrusion detection systems, and monitoring of information systems. Physical safeguards include secure storage of records, controlled access to facilities, and proper disposal of documents. The policies must be reasonably designed to: (a) ensure the security and confidentiality of customer records and information, (b) protect against anticipated threats or hazards to the security or integrity of such records, and (c) protect against unauthorized access to or use of such records that could result in substantial harm or inconvenience to the customer.

**Disposal Rule.** Section 248.30(b) requires proper destruction of consumer report information derived from consumer reports. Reasonable measures for disposal include shredding physical documents, erasing or destroying electronic media, and entering into contracts with third-party disposal services that require proper destruction.

### Regulation S-ID (Red Flags Rule)
Regulation S-ID (17 CFR 248.201-202) implements Sections 114 and 315 of the Fair and Accurate Credit Transactions Act (FACTA) for SEC-regulated entities. It requires financial institutions and creditors that hold "covered accounts" to develop and implement a written Identity Theft Prevention Program (ITPP) designed to detect, prevent, and mitigate identity theft.

**Covered Accounts.** Two categories of accounts are covered: (a) accounts primarily for personal, family, or household purposes that involve or are designed to permit multiple payments or transactions (e.g., brokerage accounts, margin accounts, advisory accounts with ongoing services), and (b) any other account for which there is a reasonably foreseeable risk to customers or to the safety and soundness of the financial institution from identity theft, including financial, operational, compliance, reputation, or litigation risks.

**Identity Theft Prevention Program Requirements.** The ITPP must include reasonable policies and procedures to: (1) identify relevant red flags applicable to the firm's covered accounts, drawing from five categories of red flags — alerts, notifications, or warnings from consumer reporting agencies; suspicious documents; suspicious personal identifying information; unusual use of or suspicious activity related to a covered account; and notices from customers, victims of identity theft, law enforcement, or other persons regarding possible identity theft — (2) detect red flags that have been incorporated into the program, (3) respond appropriately to any red flags that are detected to prevent and mitigate identity theft, and (4) ensure the program is updated periodically to reflect changes in risks to customers and to the safety and soundness of the firm.

**Administration.** The ITPP must be approved by the board of directors, a committee of the board, or senior management (17 CFR 248.201(d)). Ongoing administration includes: assigning specific responsibility for the program's implementation, training staff to carry out the program, exercising appropriate and effective oversight of service provider arrangements (ensuring that service providers' activities in connection with covered accounts are conducted in accordance with reasonable policies and procedures to detect, prevent, and mitigate identity theft), and ensuring the program is updated as necessary.

### SEC Cybersecurity Rules and Guidance
The SEC has addressed cybersecurity through a combination of rulemaking, interpretive guidance, and enforcement.

**Public Company Disclosure Rules (2023).** In July 2023, the SEC adopted rules requiring public companies to disclose material cybersecurity incidents on Form 8-K (Item 1.05) within four business days of determining that an incident is material. Companies must also disclose their cybersecurity risk management, strategy, and governance on Form 10-K (Item 1C of Regulation S-K). Required disclosures include: processes for assessing, identifying, and managing cybersecurity risks; whether cybersecurity risks have materially affected or are reasonably likely to materially affect the company's business strategy, results of operations, or financial condition; the board of directors' oversight of cybersecurity risk; and management's role in assessing and managing cybersecurity risks.

**2024 Reg S-P Amendments — Incident Response and Breach Notification.** In May 2024 the SEC adopted amendments to Regulation S-P (Release No. 34-100155) that impose the first general federal breach-response requirements on SEC-registered broker-dealers, investment advisers, investment companies, and transfer agents. Covered institutions must: (a) develop, implement, and maintain a written incident response program reasonably designed to detect, respond to, and recover from unauthorized access to or use of customer information; (b) notify affected individuals whose sensitive customer information was, or is reasonably likely to have been, accessed or used without authorization — as soon as practicable, and no later than 30 days after becoming aware of the incident; and (c) maintain written policies for oversight of service providers, including provisions ensuring the institution receives notice of breaches at service providers. Compliance dates: December 3, 2025 for larger entities and June 3, 2026 for smaller entities — as of June 2026 these requirements are in effect for all covered institutions (verify any transition guidance for newly registered firms).

**Standalone cybersecurity rulemaking status.** The SEC's February/March 2022 proposed cybersecurity risk management rules for advisers and funds (Release No. IA-5956) were formally withdrawn in June 2025 along with thirteen other pending proposals. Beyond the 2024 Reg S-P amendments, the SEC enforces cybersecurity obligations through existing authority: the Reg S-P Safeguards Rule (17 CFR 248.30), the books-and-records rules (SEC Rule 17a-4, IA Act Rule 204-2), and the general antifraud provisions. Verify the current rulemaking agenda before advising on prospective requirements.

**SEC EXAMS (formerly OCIE) Examination Priorities.** Cybersecurity has been a top SEC examination priority since 2014. Key areas examined include: governance and risk assessment (board or senior management oversight, CISO or equivalent role, documented risk assessments), access rights and controls (least privilege, multi-factor authentication, access logging, prompt deprovisioning of terminated employees), data loss prevention (monitoring for unauthorized data transfers, encryption at rest and in transit, endpoint protection), vendor management (due diligence on third-party service providers, contractual security requirements, ongoing monitoring), incident response (written plans, testing and tabletop exercises, escalation procedures), and training (frequency, content, phishing simulation results).

**SEC Enforcement.** The SEC has brought enforcement actions against registered firms for cybersecurity failures under Reg S-P's Safeguards Rule and under the Identity Theft Red Flags Rule. Notable enforcement themes include: failure to implement written policies and procedures for protecting customer information, insufficient access controls (e.g., allowing shared credentials, failing to implement multi-factor authentication), failure to detect and respond to known vulnerabilities, and misleading disclosures about cybersecurity practices following a breach.

### Incident Response Requirements
Regulatory expectations require financial firms to maintain comprehensive incident response capabilities.

**Written Incident Response Plan.** The SEC expects registered firms to maintain a written incident response plan that includes: designation of an incident response team with clear roles and escalation authority; procedures for detecting and classifying incidents by severity; containment procedures to limit the scope and impact of an incident; evidence preservation protocols (forensic imaging, log retention, chain of custody documentation); eradication and recovery procedures; internal escalation and reporting timelines (to senior management, the board, legal counsel, and the compliance department); external notification procedures (to customers, regulators, and law enforcement as required); and a post-incident review process to identify root causes and remediation actions.

**Customer Notification.** Under the 2024 Reg S-P amendments, covered institutions must notify affected individuals within 30 days of becoming aware that sensitive customer information was, or is reasonably likely to have been, accessed or used without authorization (compliance required since December 3, 2025 for larger entities and June 3, 2026 for smaller entities). Notification is not required if the institution determines, after a reasonable investigation, that the sensitive customer information has not been and is not reasonably likely to be used in a manner that would result in substantial harm or inconvenience. State breach notification laws apply on top of the federal requirement in all 50 states, the District of Columbia, and U.S. territories, with varying triggers and content requirements. Most states require notification within 30 to 60 days of discovery; some states, such as Florida (30 days under Fla. Stat. 501.171) and Colorado (30 days under C.R.S. 6-1-716), impose shorter deadlines. Firms operating in multiple states must comply with the notification requirements of each state where affected individuals reside, which often means designing to the most restrictive standard alongside the federal 30-day clock.

**Regulatory Notification.** Beyond customer notification, certain circumstances trigger reporting to regulators: (a) if the breach involves potential financial crime, SAR filing obligations under BSA/AML rules may apply; (b) FINRA expects member firms to notify FINRA of significant cybersecurity incidents; and (c) New York DFS-regulated entities must notify DFS within 72 hours of a cybersecurity event that has a reasonable likelihood of materially harming normal operations (23 NYCRR 500.17).

**Law Enforcement Coordination.** Firms should establish relationships with relevant law enforcement agencies (FBI, Secret Service, state attorneys general) before an incident occurs. In the event of a breach, law enforcement may request a delay in public notification to avoid compromising an investigation; firms should work with counsel to balance this request against state breach notification deadlines.

**SAR Filing.** If a cybersecurity incident involves or is connected to potential financial crime — for example, unauthorized access leading to theft of funds, account takeovers, or identity theft used to facilitate fraudulent transactions — the firm must evaluate whether a Suspicious Activity Report should be filed under its BSA/AML obligations. The SAR should describe the cybersecurity incident, the nature of the suspected criminal activity, and the impact on customer accounts.

### State Privacy Laws
Financial firms face a layered regulatory environment where federal securities privacy rules intersect with state privacy and cybersecurity legislation.

**California (CCPA/CPRA).** The California Consumer Privacy Act (Cal. Civ. Code 1798.100 et seq.), as amended by the California Privacy Rights Act (effective January 1, 2023), grants California residents broad rights over their personal information, including rights to know, delete, correct, and opt out of the sale or sharing of personal information. Financial institutions are partially exempt from the CCPA/CPRA to the extent they are subject to the GLBA and collect, process, sell, or disclose personal information pursuant to GLBA. However, the exemption applies only to information collected, processed, sold, or disclosed subject to GLBA — information outside the GLBA's scope (e.g., employee data, website tracking data, marketing data) may still be subject to CCPA/CPRA. Firms must carefully analyze which data falls within the GLBA exemption and which does not.

**New York (DFS 23 NYCRR 500).** The New York Department of Financial Services cybersecurity regulation applies to all entities operating under or required to operate under a DFS license, registration, or charter, or that are otherwise DFS-regulated. This includes many broker-dealers and investment advisers operating in New York. Key requirements include: designation of a Chief Information Security Officer (CISO); establishment and maintenance of a cybersecurity program based on a risk assessment; written cybersecurity policies covering 14 specified areas (information security, data governance and classification, asset inventory, access controls, business continuity, systems and network security, monitoring, incident response, vendor management, encryption, and others); annual penetration testing and bi-annual vulnerability assessments; multi-factor authentication for accessing internal networks from an external network; encryption of NPI both in transit and at rest; 72-hour notification to DFS of material cybersecurity events (23 NYCRR 500.17); annual written certification of compliance by the board or senior officer (23 NYCRR 500.17(b)); and a requirement that CISOs report in writing at least annually to the board or senior governing body. DFS has actively enforced 23 NYCRR 500 through consent orders and civil penalties.

**Massachusetts (201 CMR 17.00).** Massachusetts Standards for the Protection of Personal Information require every entity that owns, licenses, stores, or maintains personal information of Massachusetts residents to develop, implement, and maintain a comprehensive written information security program (WISP). Required elements include: designation of a responsible employee, risk assessment, employee training, monitoring of the program, discipline for violations, prevention of terminated employees from accessing records, service provider oversight, restrictions on physical access, monitoring of systems for unauthorized access, encryption of transmitted records containing personal information, encryption of all personal information stored on laptops and portable devices, use of reasonably up-to-date firewall and operating system security patches, and use of up-to-date malware protection.

**Multi-State Compliance.** Firms with customers in multiple states must track and comply with each state's privacy and data breach notification laws. Key variations include: the definition of "personal information" triggering notification obligations (some states include broader categories such as biometric data, health information, or online account credentials); notification deadlines (ranging from 30 days to "reasonable" without a specified limit); notification content requirements; requirements to notify the state attorney general or other state agency; and requirements to provide credit monitoring or identity theft protection services. Maintaining a breach notification matrix that maps state-by-state requirements is a best practice for multi-state firms.

### Vendor and Third-Party Risk Management
SEC and FINRA expect registered firms to exercise diligent oversight of service providers with access to customer data, information systems, or critical business functions. The principle that outsourcing does not outsource compliance responsibility is fundamental — the firm remains accountable for the security of customer data regardless of where the data is processed or stored.

**Due Diligence Before Engagement.** Before engaging a vendor with access to customer NPI or critical systems, firms should assess the vendor's information security posture, including: the vendor's written information security policies and procedures, SOC 2 Type II audit reports (or equivalent), business continuity and disaster recovery capabilities, incident response procedures and history, use of subcontractors and sub-processors, data center security (physical and logical), encryption practices, access control mechanisms, employee screening and training, and financial stability.

**Contractual Protections.** Contracts with service providers should include: confidentiality obligations covering all customer NPI and proprietary data; minimum information security standards (referencing recognized frameworks such as NIST CSF, ISO 27001, or SOC 2 criteria); breach notification requirements (specifying the vendor must notify the firm within a defined period, typically 24 to 72 hours, of discovering a security incident affecting the firm's data); the firm's right to audit the vendor's security practices and to receive audit reports; requirements for prompt return or destruction of data upon contract termination; restrictions on the vendor's use of the firm's data for purposes beyond the contracted services; provisions addressing the vendor's use of subcontractors, including the firm's right to approve or be notified of material subcontracting; indemnification for losses arising from the vendor's security failures; and the firm's right to terminate the contract for material security deficiencies.

**Ongoing Monitoring.** Due diligence is not a one-time exercise. Firms should: review updated SOC reports or equivalent assessments annually, conduct periodic security questionnaires or assessments, monitor the vendor for reported security incidents or regulatory actions, review the vendor's business continuity and disaster recovery testing results, and reassess the vendor's risk profile if there are material changes to the services provided, the data accessed, or the vendor's ownership or financial condition.

**Cloud Service Provider Considerations.** The SEC has issued risk alerts specifically addressing cloud security (SEC EXAMS Risk Alert, January 2020). Key expectations include: understanding the shared responsibility model (the cloud provider secures the infrastructure; the firm secures its data and configurations within the cloud); proper configuration of cloud storage to prevent unauthorized public access; strong identity and access management for cloud environments; encryption of data at rest and in transit within cloud services; logging and monitoring of cloud environment activity; and understanding the cloud provider's data residency, backup, and disaster recovery practices.

**Concentration Risk.** Regulators have expressed concern about concentration risk when multiple firms rely on the same critical service providers. Firms should assess whether the failure of a key vendor would create systemic risk, maintain business continuity plans that address vendor failure scenarios, and consider diversification of critical services where practicable.

### Data Governance for Financial Firms
Effective data governance provides the operational framework for meeting privacy and security regulatory requirements.

**Data Classification.** Firms should classify data based on sensitivity and regulatory requirements, and classification must drive the application of access controls, encryption, monitoring, and disposal requirements. For SEC-regulated firms, the categories that matter are "customer information" and "sensitive customer information" as defined in amended Reg S-P (which set the scope of the incident response and notification obligations), consumer report information subject to the Disposal Rule, and material nonpublic information subject to information-barrier controls.

**Access Controls.** The principle of least privilege requires that employees, systems, and service providers receive only the minimum access necessary to perform their functions. Role-based access control (RBAC) assigns permissions based on job function rather than individual identity, facilitating consistent enforcement and efficient provisioning and deprovisioning. Segregation of duties prevents any single individual from having end-to-end control over a process that could facilitate fraud or unauthorized access. Access reviews should be conducted at least annually, and more frequently for privileged accounts.

**Encryption.** Data encryption should be applied both at rest (stored data) and in transit (data moving across networks). At rest, full-disk encryption, database encryption, and file-level encryption are common approaches. In transit, TLS 1.2 or higher should be used for all communications containing NPI. Encryption key management — including key generation, storage, rotation, and destruction — must be addressed in the firm's security policies.

**Data Retention and Destruction.** Financial firms must balance data minimization principles with books-and-records retention requirements. SEC Rule 17a-4 (broker-dealers) and IA Act Rule 204-2 (investment advisers) impose specific retention periods for various categories of records, typically ranging from 3 to 6 years depending on the record type. Data should be retained for the longest applicable retention period and securely destroyed when the retention period expires. Destruction methods must render data unrecoverable: shredding for physical media, cryptographic erasure or physical destruction for electronic media.

**Data Loss Prevention (DLP).** DLP systems monitor and control the movement of sensitive data within and outside the firm. Common DLP controls include: monitoring email and web traffic for NPI patterns (e.g., Social Security numbers, account numbers), blocking unauthorized transfers of sensitive files to external destinations (USB drives, personal email, cloud storage), monitoring print activity for sensitive documents, and generating alerts for anomalous data movement patterns. DLP controls should be calibrated to the firm's data classification scheme.

**Monitoring and Logging.** Firms should maintain comprehensive logs of access to sensitive systems and data, including: user authentication events (successful and failed), access to customer account records, changes to access permissions, data exports and transfers, and system administrator activities. Logs must be retained for a sufficient period to support incident investigation and regulatory examination (SEC examiners frequently request 12 to 24 months of access logs). Automated alerting should be configured for anomalous activity patterns, such as after-hours access, access from unusual locations, or bulk data downloads.

### Employee Training and Awareness
The compliance-specific points: the Reg S-P Safeguards Rule requires employee training as part of the written information security policies; FINRA Regulatory Notice 21-18 emphasizes employee awareness and training for member firms; and New York DFS 23 NYCRR 500.14 specifically mandates regular cybersecurity awareness training for all personnel. Training must occur at least annually and during onboarding before new employees receive access to customer NPI. All training must be documented (date, attendees, topics, materials) and retained for at least 5 years — SEC examiners routinely request training records and phishing simulation click-through rates during cybersecurity examinations, and an annual slide deck without measurable outcomes is increasingly viewed as inadequate.

## Worked Examples

### Example 1: Departing Employee Downloads Client NPI to Personal USB Drive
**Scenario:** An SEC-registered investment adviser discovers during a routine access review that a recently departed portfolio manager downloaded a file containing client NPI — including names, Social Security numbers, dates of birth, and account values for 850 clients — to a personal USB drive on the employee's last day of employment. The firm's IT team identifies the transfer through endpoint monitoring logs. The employee has already left the firm and started at a competing RIA.
**Compliance Issues:**
- The Reg S-P Safeguards Rule (17 CFR 248.30) requires written policies and procedures to protect against unauthorized access to customer records. The firm must evaluate whether its existing controls were adequate to prevent this type of exfiltration and whether its policies were followed.
- If the firm's policies prohibited personal USB device use or required DLP controls blocking the transfer of files containing NPI to removable media, a failure to enforce those policies is itself a Safeguards Rule deficiency.
- If the firm lacked such policies, the absence constitutes a potential Safeguards Rule violation, as the policies must be reasonably designed to protect against unauthorized access.
- The Reg S-P incident response and notification requirements are triggered: Social Security numbers are sensitive customer information, so the firm must execute its incident response program and notify affected individuals within 30 days of becoming aware of the unauthorized access.
- State breach notification laws are also triggered. The firm must determine the states of residence of all 850 affected clients and comply with each applicable state law's notification requirements.
- Several states — including California (Cal. Civ. Code 1798.82), Massachusetts (M.G.L. c. 93H, Section 3), and New York (N.Y. Gen. Bus. Law 899-aa) — require notification to both the affected individuals and the state attorney general. Notification timelines vary but are typically 30 to 60 days from discovery.
- The firm should evaluate whether the departing employee's actions constitute potential financial crime (theft of trade secrets, identity theft facilitation, or misuse of client information for competitive solicitation), which may warrant a SAR filing under BSA/AML obligations.
**Analysis:**
The firm should immediately take the following steps: (1) Preserve all evidence of the data transfer, including endpoint monitoring logs, the employee's access logs, and any records of the files accessed or copied. (2) Engage legal counsel to assess state breach notification obligations and to manage attorney-client privilege over the investigation. (3) Contact the former employee and the competing firm through counsel to demand the return or certified destruction of all client data, supported by a forensic certification that no copies remain. (4) Conduct a forensic analysis of the former employee's workstation and access history to determine whether additional data was compromised. (5) Notify affected clients as required by applicable state laws, providing information about the nature of the data compromised, the steps the firm is taking, and resources for credit monitoring or identity theft protection (several states require the firm to offer credit monitoring at no cost). (6) Report the incident to senior management and the board (or equivalent governing body) for oversight. (7) Evaluate whether existing access controls should be strengthened — for example, implementing or enforcing USB port blocking, DLP controls preventing NPI transfer to removable media, and enhanced monitoring during employee offboarding periods. (8) Document all remediation actions, as SEC examiners will expect to see evidence that the firm identified the root cause and implemented corrective measures.

### Example 2: Third-Party Vendor Ransomware Attack Exposes Customer Data
**Scenario:** A mid-sized broker-dealer uses a third-party portfolio accounting vendor to process and store customer account data for approximately 15,000 accounts. The vendor notifies the firm that it has experienced a ransomware attack in which threat actors exfiltrated data before encrypting systems. The vendor's initial assessment indicates that the exfiltrated data may include customer names, addresses, account numbers, Social Security numbers, and account holdings. The firm's customers reside in 38 states. The vendor's notification arrives 10 days after the vendor discovered the incident.
**Compliance Issues:**
- The firm's Reg S-P Safeguards Rule obligations extend to its oversight of service providers. The firm is required to have written policies and procedures addressing service provider oversight, including contractual protections and ongoing monitoring (17 CFR 248.30).
- The firm must evaluate the adequacy of its vendor management program: Did the contract require the vendor to notify the firm within a specified period (e.g., 24 to 72 hours)? A 10-day delay may indicate a contractual gap or a vendor breach of its contractual obligations. Did the firm conduct due diligence on the vendor's security posture before engagement? Did the firm review the vendor's SOC reports or equivalent assessments? Did the contract include audit rights, subcontractor controls, and indemnification?
- If the firm is DFS-regulated, 23 NYCRR 500.17 requires notification to DFS within 72 hours of determining that a cybersecurity event has occurred that has a reasonable likelihood of materially harming normal operations — this includes incidents at third-party service providers that affect the firm's customer data.
- State breach notification laws are triggered for all 38 states where customers reside. The firm — not the vendor — is typically the entity with the customer relationship and thus bears the notification obligation (though the vendor may have independent notification obligations in some states).
- FINRA expects member firms to notify FINRA of significant cybersecurity incidents. A breach affecting 15,000 customer accounts with Social Security numbers is significant.
- The firm's Reg S-P incident response program obligations apply: the firm must execute its written incident response program and provide customer notification within 30 days of becoming aware that sensitive customer information was, or is reasonably likely to have been, accessed without authorization — the federal clock runs alongside the state deadlines.
**Analysis:**
The firm should activate its incident response plan and take the following actions: (1) Engage external cybersecurity counsel and a forensic investigation firm to assess the scope of the compromise independently of the vendor's assessment. (2) Demand from the vendor: a detailed incident timeline, forensic investigation reports, confirmation of the specific data compromised, the vendor's remediation steps, and evidence that the attack vector has been closed. (3) Begin mapping state-by-state breach notification requirements for all 38 states. Assign the most restrictive deadline (likely 30 days from the firm's discovery) as the target for all notifications to ensure compliance across jurisdictions. (4) Prepare customer notification letters that comply with the content requirements of each applicable state, providing the nature of the compromised data, the firm's response actions, and information about credit monitoring services (the firm should provide credit monitoring at its expense for affected customers). (5) Notify DFS within 72 hours if the firm is subject to 23 NYCRR 500. (6) Notify FINRA of the incident. (7) Evaluate whether the breach resulted in or facilitated any unauthorized transactions, account takeovers, or other potential financial crime, and file SARs as appropriate. (8) Reassess the vendor relationship: review the contract for breach provisions and indemnification rights, consider whether the vendor's security practices are adequate for continued engagement, and document the reassessment. (9) Report the incident and remediation actions to the board or senior management, and update the firm's written information security program to address any gaps revealed by the incident. (10) Retain all documentation of the incident, investigation, notifications, and remediation for examination and audit purposes.

### Example 3: SEC Examination Focused on Cybersecurity
**Scenario:** An SEC-registered investment adviser with $5 billion in AUM receives an examination notification letter from the SEC Division of Examinations. The document request list includes cybersecurity as a focus area, requesting production of the firm's written information security policies, incident response plan, vendor assessments, access control documentation, employee training records, and board or management reporting on cybersecurity.
**Compliance Issues:**
- The examination will test the firm's compliance with the Reg S-P Safeguards Rule, which requires written policies and procedures for administrative, technical, and physical safeguards.
- If the firm is subject to Reg S-ID, examiners may also request the firm's Identity Theft Prevention Program and evidence of its implementation.
- SEC examiners will assess not only the existence of written policies but their actual implementation, testing, and updating — a policy that exists on paper but is not followed is a deficiency.
- Common SEC examination deficiency findings related to cybersecurity include: lack of a comprehensive written information security policy; policies that have not been updated to reflect current threats, technology, or business practices; insufficient access controls (e.g., shared passwords, failure to implement multi-factor authentication, failure to decommission access promptly upon employee departure); lack of a written incident response plan or failure to test the plan through tabletop exercises; insufficient vendor due diligence documentation (no SOC reports, no security questionnaires, no contractual protections); inadequate employee training records (no evidence of training, training not conducted annually, no phishing simulation program); failure to conduct periodic risk assessments; failure to encrypt NPI at rest and in transit; and insufficient board or senior management oversight (no regular reporting on cybersecurity risks, no board-level engagement).
**Analysis:**
To prepare for the examination, the firm should: (1) Assemble all responsive documents before the production deadline, including the written information security policy, risk assessments, incident response plan, vendor management policies and individual vendor assessments (SOC reports, security questionnaires, contracts with security provisions), access control documentation (user access lists, privileged account inventories, access review records, MFA implementation evidence), employee training materials and attendance records for at least the prior two years, phishing simulation results, incident logs (even if no material incidents occurred — examiners want to see the logging process), board or management committee meeting minutes reflecting cybersecurity discussions and reporting, and any third-party penetration testing or vulnerability assessment reports. (2) Conduct a gap analysis against SEC examination expectations before the examination begins. Identify any deficiencies and begin remediation immediately — examiners view active remediation favorably, even if the deficiency exists. (3) Prepare the CISO, CCO, and relevant IT and compliance personnel for examination interviews. Examiners will ask questions about how policies are implemented in practice, how incidents are escalated, how vendors are monitored, and how the firm stays current with evolving threats. (4) Review recent SEC EXAMS risk alerts and deficiency letters related to cybersecurity to anticipate the examination team's areas of focus. (5) Ensure that the firm's written policies are current and accurately reflect the firm's actual practices — a material gap between written policy and actual practice is a significant deficiency. (6) Document the firm's remediation of any prior examination findings, internal audit findings, or self-identified deficiencies.

## Common Pitfalls
- Treating the Reg S-P Safeguards Rule as a documentation exercise rather than an operational requirement — written policies must be implemented, tested, and updated, not merely drafted and filed
- Assuming the FAST Act annual privacy notice exception applies without verifying that the firm shares NPI only under permitted exceptions and has not changed its privacy policies since the last notice
- Failing to conduct a covered account analysis under Reg S-ID — firms sometimes assume that only banks have covered accounts, but brokerage accounts and advisory accounts with ongoing transactions qualify
- Implementing an Identity Theft Prevention Program at the time of initial adoption but never updating it, even as the firm's customer base, products, and threat landscape change
- Treating vendor due diligence as a one-time onboarding exercise rather than an ongoing monitoring obligation — a SOC report from three years ago does not satisfy current diligence expectations
- Including security standards in vendor contracts but never exercising audit rights or reviewing compliance with those standards
- Relying on a vendor's notification of a breach as the sole trigger for the firm's incident response — the firm has an independent obligation to monitor for and detect security incidents
- Failing to map multi-state breach notification obligations before an incident occurs, resulting in delayed or non-compliant notifications under compressed timelines
- Not distinguishing between data subject to the GLBA exemption from CCPA/CPRA and data that falls outside the exemption — employee data, website analytics, and marketing data may not be covered by the GLBA exemption
- Implementing encryption for data in transit but neglecting encryption at rest, or vice versa
- Failing to decommission system access promptly when employees depart — SEC examiners routinely check for active accounts belonging to former employees as an indicator of access control weaknesses
- Treating employee cybersecurity training as a compliance checkbox rather than an effective awareness program — annual slide decks without phishing simulations, role-specific content, or measurable outcomes are increasingly viewed as inadequate
- Maintaining incident response plans that have never been tested through tabletop exercises or simulations — untested plans frequently fail under the pressure of an actual incident
- Assuming that outsourcing data processing or storage to a cloud provider eliminates the firm's regulatory responsibility for data security — the shared responsibility model requires the firm to secure its own configurations, access controls, and data within the cloud environment

## Cross-References
- **client-disclosures** (compliance plugin): The Reg S-P privacy notice is a required client disclosure document; its content, delivery timing, and the FAST Act exception are addressed in the client-disclosures skill
- **books-and-records** (compliance plugin): Data retention and destruction requirements under privacy regulations must be reconciled with books-and-records retention rules under SEC Rule 17a-4 and IA Act Rule 204-2
- **know-your-customer** (compliance plugin): KYC data — including Social Security numbers, dates of birth, addresses, and identification documents — constitutes NPI requiring protection under Reg S-P and is a primary target for identity theft under Reg S-ID
- **anti-money-laundering** (compliance plugin): Cybersecurity incidents involving unauthorized account access, funds theft, or identity theft may trigger SAR filing obligations under BSA/AML requirements
- **examination-readiness** (compliance plugin): Cybersecurity is consistently among the SEC Division of Examinations' top examination priorities; cybersecurity document requests, interview topics, and common deficiency findings are central to examination preparation
- **conflicts-of-interest** (compliance plugin): Information barriers, access controls, and data segregation policies serve dual purposes — preventing misuse of material nonpublic information and protecting customer NPI from unauthorized internal access


---

## SKILL: privacy-impact-assessment

- Fuente: `SYasJ/claude-business-skills` → `plugins/risk/skills/privacy-impact-assessment` (MIT)
- Cuándo usarla: Prepare a privacy impact note for a process that collects personal data, for counsel to complete. Use when the user mentions privacy impact, PIA, DPIA prep, new processing review, or asks for a privacy impact note. Risk and compliance skill by Yasir Jilani.

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'privacy-impact-assessment' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Privacy Impact Assessment

Prepare a privacy impact note for a process that collects personal data, for counsel to complete.

## When to use this skill

Use this skill when the user:

- privacy impact
- PIA
- DPIA prep
- new processing review

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

- The process
- Data elements
- People affected
- Recipients they named

## Workflow


### 1. Step 1

Describe the process and the purpose.
### 2. Step 2

List data elements and who they are about. Cut elements with no purpose.
### 3. Step 3

List recipients the user named. Do not invent vendors.
### 4. Step 4

Note retention if known, otherwise mark it unknown.
### 5. Step 5

Flag high-harm contexts they mentioned, such as children or precise location, for counsel. Do not complete a legal DPIA conclusion.
### 6. Step 6

Recommend a product change where minimization is obvious.

## Output

Deliver a **privacy impact note**.

- Purpose of this privacy impact note, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a privacy impact note by 30 September 2026. A new form collects date of birth to personalize a color theme.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A new form collects date of birth to personalize a color theme.

The process: email to Priya Shah. No written steps after 1 Sep 2026
Data elements: Control 7.2 access review. Partly documented: the what is written down, the who is not
People affected: Issue log item 18, last reviewed 14 September 2026. No owner named since
Recipients they named: Priya Shah plus two others named in the thread. No distribution list attached
```

### Example outcome

**Privacy impact note**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Cuts the date of birth and sends any remaining legal question to counsel.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The process | email to Priya Shah. No written steps after 1 Sep 2026 | Needs confirmation |
| Data elements | Control 7.2 access review. Partly documented: the what is written down, the who is not | Carried into the draft |
| People affected | Issue log item 18, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Recipients they named | Priya Shah plus two others named in the thread. No distribution list attached | Needs confirmation |

**How this draft was built**

**1. Describe the process and the purpose**

**2. List data elements and who they are about. Cut elements with no purpose**

**3. List recipients the user named. Do not invent vendors**

**4. Note retention if known, otherwise mark it unknown**

**5. Flag high-harm contexts they mentioned, such as children or precise location, for counsel. Do not complete a legal DPIA conclusion**

**Deliberately not done**
- A legal conclusion dressed up as a PIA.
- Invented vendors.
- Keeping data with no purpose.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A legal conclusion dressed up as a PIA
- Invented vendors
- Keeping data with no purpose

## Related skills

- `privacy-by-design`
- `privacy-notice-draft`


---

## SKILL: reconciliation

- Fuente: `JoelLewis/finance_skills` → `plugins/client-operations/skills/reconciliation` (MIT)
- Cuándo usarla: Design and operate reconciliation processes across portfolio management, custodian, and clearing systems. Use when building a daily position, cash, or transaction reconciliation process, investigating discrepancies between internal records and custodian records, diagnosing recurring break patterns from corporate actions or pricing differences, setting tolerance thresholds for position, cash, or market value matching, implementing three-way reconciliation, designing break investigation workflows with aging and escalation, normalizing multi-custodian feeds from Schwab, Fidelity, or Pershing, reconciling cost basis or accrued income, or preparing for examinations on books and records accuracy.

# Reconciliation

## Core Concepts

### 1. Reconciliation Types and Hierarchy

Reconciliation is the systematic comparison of records across two or more systems to identify and resolve discrepancies. In securities operations, reconciliation ensures that the firm's internal records (the investment book of record, or IBOR) match the custodian's official records (the official book of record, or OBOR) and, where applicable, the clearing firm's records. The reconciliation hierarchy proceeds from the most fundamental data element (positions) through increasingly derived data elements.

**Position Reconciliation.** The foundational reconciliation. Compares the number of shares or units held for each security in each account between the firm's portfolio management system (PMS) and the custodian. Position reconciliation is typically zero-tolerance: any share count difference, no matter how small, constitutes a break. Fractional share differences (common with dividend reinvestment plans) must also be identified and resolved. Position reconciliation is performed daily, using end-of-day files from the custodian compared against the PMS position ledger.

**Cash Reconciliation.** Compares cash balances between the PMS and the custodian, accounting for settled cash, pending settlements, accrued income, and pending fee debits. Cash reconciliation is more nuanced than position reconciliation because timing differences are inherent — a trade executed on day T settles on T+1, and the PMS and custodian may record the cash impact on different dates. Cash tolerance thresholds are common, typically a small dollar amount (e.g., $0.50 to $5.00) to accommodate rounding differences across systems. Balances outside the tolerance require investigation.

**Transaction Reconciliation.** Compares individual transactions (trades, dividends, interest payments, transfers, fees) recorded in the PMS against the custodian's transaction ledger. Transaction reconciliation operates at the trade level, matching on security, quantity, price, trade date, and settlement date. Unmatched transactions on either side constitute breaks. Transaction reconciliation is typically performed on a T+1 basis — comparing yesterday's activity after the custodian's end-of-day file is received.

**Market Value Reconciliation.** Compares the total market value of each position and each account between systems. Market value breaks often result from pricing differences — the PMS and custodian may source prices from different vendors or apply different pricing hierarchies for thinly traded or illiquid securities. Market value tolerance is typically expressed in basis points (e.g., 5-10 bps of account value) rather than absolute dollars, because a $100 difference on a $50,000 account is more significant than a $100 difference on a $5,000,000 account.

**Accrued Income Reconciliation.** Compares accrued interest on fixed-income holdings and declared-but-unpaid dividends. Accrued income differences frequently arise from day-count convention differences (actual/actual vs. 30/360), ex-date vs. record-date timing, or different treatment of defaulted bonds. This reconciliation is particularly important for fixed-income-heavy portfolios where accrued income is a material component of total value.

**Cost Basis Reconciliation.** Compares the tax lot-level cost basis for each position between the PMS and the custodian. Cost basis discrepancies are among the most difficult to resolve because they may originate from historical corporate actions (splits, mergers, spin-offs, return of capital adjustments) that were processed differently in each system. Since the custodian reports cost basis to the IRS on Form 1099-B, cost basis discrepancies can result in incorrect tax reporting if not resolved. Cost basis reconciliation is typically performed less frequently than position reconciliation — monthly or quarterly — but with zero tolerance for discrepancies.

### 2. Three-Way Reconciliation

For advisory firms that use a portfolio management system separate from both the custodian and any clearing firm, three-way reconciliation is the standard of practice. The three records being compared are:

**Advisor System (PMS / Portfolio Accounting).** The firm's investment book of record (IBOR), maintained in the portfolio management system (Orion, Black Diamond, Tamarac, Addepar, or similar). This is the record the firm uses for performance reporting, billing, rebalancing, and client-facing communications. The advisor system reflects the firm's understanding of what each client owns.

**Custodian Records.** The official book of record (OBOR), maintained by the custodian (Schwab, Fidelity, Pershing, or similar). This is the legally authoritative record of client assets. The custodian is responsible for safekeeping assets, settling transactions, and reporting to the IRS. When the advisor system and custodian disagree, the custodian record is presumed correct unless the firm can demonstrate otherwise.

**Clearing Firm Records.** For firms that clear through a separate entity (introducing broker-dealers that clear through a correspondent clearing firm), the clearing firm maintains its own record of positions and transactions. The clearing firm processes settlements, maintains margin calculations, and generates customer statements. In a fully disclosed arrangement, the clearing firm's records should match the custodian's, but discrepancies can arise from timing, corporate action processing, or data feed errors.

**Authoritative Source by Data Element.** Different systems serve as the authoritative source for different data elements:

| Data Element | Authoritative Source | Reason |
|---|---|---|
| Share/unit count | Custodian | Custodian holds the securities in legal custody |
| Settled cash balance | Custodian | Custodian controls the cash account |
| Trade execution details | Executing broker / custodian | Trade occurred on their platform |
| Cost basis (for tax reporting) | Custodian | Custodian reports 1099-B to IRS |
| Performance returns | Advisor system (PMS) | PMS maintains the calculation methodology |
| Model assignment and drift | Advisor system (PMS) | PMS manages the investment process |
| Fee schedule and billing | Advisor system (PMS) | PMS calculates fees per advisory agreement |
| Corporate action elections | Custodian | Custodian processes the action |

**Reconciliation Frequency.** The standard frequencies are:
- Position reconciliation: daily (end of each business day)
- Cash reconciliation: daily
- Transaction reconciliation: T+1 (one business day after the trade or event)
- Market value reconciliation: daily
- Accrued income reconciliation: daily or weekly, depending on portfolio composition
- Cost basis reconciliation: monthly or quarterly

### 3. Break Identification

A break is any discrepancy identified during reconciliation between two or more records. Break identification is the process of detecting, classifying, and prioritizing breaks for investigation and resolution.

**Tolerance Thresholds.** Not all discrepancies warrant investigation. Tolerance thresholds define the minimum discrepancy that constitutes a reportable break:

| Reconciliation Type | Typical Tolerance | Rationale |
|---|---|---|
| Position (shares/units) | Zero (exact match required) | Any share difference indicates a missing or erroneous transaction |
| Cash balance | $0.50 - $5.00 | Small rounding differences across systems are expected |
| Market value | 5-10 bps of account value | Pricing source differences create small value discrepancies |
| Accrued income | $0.01 - $1.00 | Day-count and rounding conventions vary across systems |
| Cost basis | Zero (exact match required) | Any basis difference affects tax reporting accuracy |
| Transaction matching | Exact match on key fields | Unmatched transactions require investigation |

**Break Categorization.** Breaks are classified by root cause to enable pattern analysis and systemic remediation:

- **Timing differences.** The most common category. Arise when the PMS and custodian record the same event on different dates. Examples: a trade executed late in the day may appear in the PMS on trade date but in the custodian file the following day; a dividend may post in the custodian on the pay date but in the PMS on the record date. Timing breaks typically self-resolve within one to two business days.
- **Pricing differences.** Occur when the PMS and custodian use different pricing sources or apply different pricing hierarchies. Most common for fixed-income securities, international equities (with exchange rate differences), and illiquid or thinly traded securities.
- **Corporate action differences.** Arise when a corporate action (stock split, merger, spin-off, dividend reinvestment) is processed in one system but not the other, or processed with different terms (different exchange ratio, different effective date). Corporate actions are the single largest cause of position breaks that do not self-resolve.
- **Missing transactions.** A transaction appears in one system but not the other. Common causes: a trade placed directly at the custodian without going through the PMS, a manual journal entry in one system, or a data feed failure that dropped a transaction.
- **Duplicate transactions.** The same transaction is recorded twice in one system. Can result from data feed reprocessing, manual entry combined with automated feed, or system errors during corporate action processing.
- **Data quality issues.** Security identifiers do not match across systems (CUSIP changes, ticker symbol changes), account numbers are mapped incorrectly, or data feed parsing errors corrupt field values.

**Break Severity Levels.** Breaks are prioritized based on their operational impact:

- **Critical (must resolve same day).** Position breaks affecting client-facing reporting or imminent billing, cash breaks exceeding a material threshold (e.g., $10,000), and any break that would affect a trade if left unresolved.
- **High (must resolve within two business days).** Position breaks on any actively traded security, market value breaks exceeding the tolerance, and unmatched transactions from the prior day.
- **Medium (must resolve within five business days).** Accrued income differences, cost basis discrepancies identified in periodic reconciliation, and pricing breaks on less liquid securities.
- **Low (resolve within the current monthly cycle).** Minor rounding differences within tolerance, known timing differences expected to self-resolve, and informational discrepancies that do not affect reporting or billing.

### 4. Break Resolution Workflows

Once a break is identified and categorized, it enters a structured resolution workflow. Effective break resolution combines investigative rigor with operational efficiency.

**Investigation Procedures.** The standard investigation sequence for a position break is:

1. Verify the break is not a known timing difference by checking pending transactions and unsettled activity in both systems.
2. Review the transaction history for the affected security in both the PMS and custodian to identify the divergence point — the first date on which the records disagree.
3. Check for unprocessed corporate actions by reviewing the corporate action calendar for the security and confirming that all mandatory actions have been applied in both systems.
4. Check for missing or duplicate trades by comparing the trade blotter in the PMS against the custodian's trade confirmation file for the relevant dates.
5. Verify security identifier mapping — confirm that the CUSIP, ISIN, or ticker symbol in the PMS maps correctly to the custodian's security master.
6. If the cause remains unidentified, submit a custodian inquiry requesting the custodian's transaction history for the security and account over the period in question.

**Common Break Causes and Resolutions.**

| Break Cause | Resolution |
|---|---|
| Unprocessed stock split | Apply the split in the PMS (adjust shares and cost basis) |
| Missed dividend reinvestment | Add the reinvestment transaction in the PMS |
| Trade placed directly at custodian | Enter the trade retroactively in the PMS |
| Data feed failure (dropped transaction) | Re-import the affected date's custodian file |
| Duplicate trade entry | Remove the duplicate from the PMS |
| CUSIP change (corporate action) | Update the security mapping in the PMS |
| Pricing difference | Update the PMS pricing source or override the price |
| Cash posting timing | Confirm the break self-resolves the following day; mark as timing |

**Break Aging and Escalation.** Unresolved breaks must be tracked by age. The aging clock starts on the date the break is first identified. Escalation rules ensure that aging breaks receive management attention:

- 0-2 business days: Operations analyst investigates and resolves.
- 3-5 business days: Escalate to operations supervisor. Supervisor reviews investigation notes and may reassign or provide guidance.
- 6-10 business days: Escalate to operations manager. A written explanation is required for why the break remains open.
- Over 10 business days: Escalate to the chief operations officer or chief compliance officer. Breaks of this age may indicate a systemic issue requiring vendor engagement or system changes.

**Resolution Documentation.** Every resolved break must be documented with: the date the break was identified, the break category, the root cause determination, the corrective action taken, the system in which the correction was made, the date of resolution, and the identity of the person who resolved it. This documentation forms part of the firm's books and records and is subject to regulatory examination.

**Recurring Break Pattern Analysis.** Operations teams should review break data periodically (weekly or monthly) to identify recurring patterns. If the same type of break occurs repeatedly for the same security, account, or data feed, the root cause is likely systemic rather than transactional. Systemic causes require process or system changes, not repeated manual corrections. Examples of systemic patterns: a particular custodian feed consistently drops fractional shares, a specific security type (e.g., foreign ordinaries) always has pricing breaks, or corporate actions for a particular issuer are consistently delayed.

### 5. Reconciliation Automation

Manual reconciliation — comparing records by hand in spreadsheets — is error-prone, time-consuming, and does not scale. Reconciliation automation reduces manual effort, increases accuracy, and enables exception-based processing where human attention is directed only to genuine breaks.

**Automated Matching Engines.** Reconciliation software compares records from two or more sources using configurable matching rules. The matching engine ingests data files from each source, normalizes the data into a common format, applies matching rules to pair records, and flags unmatched or out-of-tolerance items as exceptions.

**Rule-Based Auto-Resolution.** Beyond matching, advanced reconciliation systems can automatically resolve certain categories of breaks without human intervention:
- Timing breaks that match a known pattern (e.g., a transaction appears in the custodian file one day after it appears in the PMS) can be auto-resolved if the offsetting entry appears within a defined window.
- Rounding differences within tolerance can be auto-resolved and logged.
- Known pricing source differences for specific security types can be auto-resolved with the custodian price accepted as authoritative.

Auto-resolution rules must be carefully designed and regularly audited to ensure they are not masking genuine breaks. Each auto-resolved item should be logged for review.

**Exception-Based Processing.** The operational model for a mature reconciliation program is exception-based: the automated system handles the matching and auto-resolution of routine items, and human analysts focus exclusively on the exceptions. This model dramatically reduces the volume of items requiring manual review and allows operations teams to scale without proportional headcount growth.

A well-automated reconciliation program targets the following benchmarks:
- Auto-match rate (positions): 97-99% of position records match without intervention
- Auto-match rate (transactions): 90-95% of transactions match without intervention
- Exception rate: 1-5% of records require human review
- Same-day resolution rate: 80%+ of exceptions resolved on the day they are identified
- Break aging over 5 days: less than 0.5% of total accounts

**Data Normalization Across Sources.** A critical prerequisite for automated matching is data normalization — transforming records from different sources into a common format. Normalization challenges include:
- Security identifiers: the PMS may use CUSIP while the custodian uses ISIN or proprietary identifiers. The reconciliation system must maintain a cross-reference table.
- Account identifiers: the PMS account number may differ from the custodian account number. A mapping table is required.
- Transaction type codes: each system uses its own codes for buys, sells, dividends, etc. A translation table converts source-specific codes to a standard taxonomy.
- Date formats and conventions: different systems may use different date formats (MM/DD/YYYY vs. YYYY-MM-DD) or different date conventions (trade date vs. settlement date).
- Sign conventions: one system may represent sales as negative quantities while another uses positive quantities with a separate direction indicator.

**Reconciliation Scheduling.** The daily reconciliation cycle follows a predictable schedule:
1. Custodian end-of-day files are generated after market close and settlement processing (typically available between midnight and 6:00 AM the following business day).
2. The reconciliation system ingests the custodian files and the PMS end-of-day data.
3. Automated matching runs (typically completed by 7:00-8:00 AM).
4. Exception reports are generated and distributed to operations analysts.
5. Analysts investigate and resolve exceptions during the business day.
6. Resolved exceptions are documented and closed.
7. End-of-day reconciliation status report is produced for management review.

**STP Rate for Reconciliation.** Straight-through processing (STP) rate measures the percentage of reconciliation items that flow through the entire process — from data ingestion through matching to resolution — without manual intervention. A high STP rate indicates a well-automated, well-configured reconciliation operation. Industry benchmarks for mature operations: 95-99% STP rate for position reconciliation, 85-95% STP rate for transaction reconciliation, and 90-97% STP rate for cash reconciliation.

### 6. Corporate Action Reconciliation

Corporate actions are the single most frequent cause of position breaks that require manual resolution. A corporate action is any event initiated by the issuer of a security that affects the security's terms, structure, or ownership — including stock splits, reverse splits, mergers, acquisitions, spin-offs, tender offers, rights offerings, dividends (cash and stock), and return-of-capital distributions.

**Why Corporate Actions Cause Breaks.** Corporate actions are problematic for reconciliation because:
- The custodian and the PMS may process the same action on different dates, especially when the event has multiple milestone dates (announcement, record, ex-date, pay date, effective date).
- Voluntary actions (tender offers, rights offerings) require an election from the account holder. If the election is recorded in one system but not the other, the position diverges.
- Complex actions (mergers with mixed consideration — part cash, part stock; spin-offs with fractional share treatment) require multi-step processing that may be handled differently across systems.
- Some PMS platforms process corporate actions from the custodian data feed automatically, while others require manual entry. If the manual entry is delayed or performed incorrectly, a break results.

**Corporate Action Event Processing Timing.** The reconciliation team must track the lifecycle of each corporate action:
- **Announcement date:** The issuer announces the action. The PMS should record the pending event.
- **Record date:** The date on which shareholders of record are determined. Affects who receives the action's benefits.
- **Ex-date:** The first date on which the security trades without the benefit of the action (e.g., without the dividend or split). The custodian typically adjusts positions as of the ex-date.
- **Pay date / effective date:** The date on which the action takes effect (cash is paid, new shares are delivered, the merger closes).

**Voluntary vs. Mandatory Action Reconciliation.** Mandatory actions (splits, mergers, cash dividends) apply to all holders automatically and should be processed in both systems without account-level intervention. Voluntary actions (tender offers, rights exercises, dividend reinvestment elections) require per-account decisions and are a higher-risk category for breaks because the election must be recorded consistently across systems.

**Dividend and Income Reconciliation.** Cash dividends are the most frequent corporate action. Reconciliation verifies: the correct per-share rate was applied, the share count as of the record date matches, the total dividend amount (rate times shares) matches, and the payment was posted on the correct date. Dividend reinvestment (DRIP) is a common source of fractional-share breaks because the PMS and custodian may calculate the reinvestment slightly differently based on the price used.

**Stock Split and Merger Adjustment Verification.** After a split or merger is processed, the reconciliation team must verify: the new share count equals the old share count times the split ratio (or exchange ratio for mergers), the cost basis per share has been adjusted inversely to the share adjustment, and any fractional shares or cash-in-lieu payments are correctly recorded.

### 7. Multi-Custodian Reconciliation

Many advisory firms custody client assets at two or more custodians (e.g., Schwab and Fidelity, or a primary custodian and a trust company). Multi-custodian operations introduce additional reconciliation complexity.

**Aggregating Positions Across Custodians.** The PMS must maintain a unified view of all positions across all custodians, which requires separate reconciliation against each custodian's records. A position break at one custodian does not affect the reconciliation at another, but the PMS must correctly attribute each position to the correct custodian.

**Held-Away Asset Reconciliation.** Assets that the advisor monitors but does not manage (e.g., employer 401(k) plans, outside brokerage accounts, annuities) present a reconciliation challenge because: the data source is often an aggregation feed (Plaid, Yodlee, ByAllAccounts) rather than a direct custodian feed, data may be delayed by one to three days, position data may lack the granularity needed for precise reconciliation (e.g., no lot-level cost basis), and feed connections can break when the client's credentials change or the institution updates its login process. Held-away assets are typically reconciled at a lower frequency (weekly or monthly) and with wider tolerances than managed assets, because the data quality does not support daily zero-tolerance matching.

**Custodian Data Feed Formats and Timing.** Each custodian delivers data in its own format and on its own schedule:

| Custodian | Typical File Format | Typical Delivery Time | Notes |
|---|---|---|---|
| Schwab | CSV, proprietary layout | 2:00-5:00 AM ET | Schwab Advisor Center feed |
| Fidelity | CSV, proprietary layout | 1:00-4:00 AM ET | Wealthscape data feed |
| Pershing | Fixed-width and CSV | 3:00-6:00 AM ET | NetX360 feed |

**Normalization Challenges Across Custodians.** When reconciling across multiple custodians, the reconciliation system must normalize: security identifiers (one custodian may use CUSIP while another uses a proprietary ID), transaction type codes (each custodian has its own taxonomy for trades, dividends, fees, transfers), account number formats, date and time representations, and corporate action terminology and processing conventions. Maintaining and updating these normalization mappings is an ongoing operational task.

### 8. Regulatory and Fiduciary Requirements

Reconciliation is not merely an operational best practice — it is grounded in specific regulatory requirements and fiduciary obligations.

**SEC Rule 204-2 (Books and Records for Advisers).** Rule 204-2 under the Investment Advisers Act of 1940 requires SEC-registered investment advisers to maintain accurate books and records, including records of all securities transactions, client account positions, and supporting documentation. While the rule does not explicitly mandate a daily reconciliation process, the obligation to maintain accurate records effectively requires regular reconciliation against the custodian's official records. An adviser that reports positions or performance to clients based on unreconciled internal records risks producing inaccurate client communications, which is a violation of the adviser's fiduciary duty and a potential breach of the antifraud provisions of Section 206.

**Fiduciary Duty to Maintain Accurate Records.** Investment advisers owe a fiduciary duty to their clients, which includes the duty to provide accurate information. Reconciliation is the operational mechanism that ensures accuracy. If an adviser's internal records diverge from the custodian's records and the adviser relies on its internal records for billing, performance reporting, or investment decisions, the adviser may be billing incorrectly (overcharging or undercharging), reporting incorrect performance figures (misleading the client), or making investment decisions based on incorrect position data (breaching the duty of care). Regulators have brought enforcement actions against advisers whose failure to reconcile resulted in inaccurate client reporting or billing.

**ERISA Reconciliation Requirements.** For advisers managing ERISA-covered retirement plan assets, the fiduciary standard is heightened. ERISA fiduciaries must maintain accurate records of plan assets and ensure that all transactions are properly recorded. Reconciliation discrepancies that affect plan asset valuation can result in incorrect participant account balances, incorrect benefit calculations, and a breach of ERISA fiduciary duty. DOL audits of retirement plan service providers routinely examine reconciliation processes.

**Client Reporting Accuracy Obligations.** Client reports — whether quarterly statements, performance summaries, or online portal views — must reflect accurate, reconciled data. The SEC's examination priorities have repeatedly cited the accuracy of client reporting as a focus area. Firms that generate client reports from unreconciled data risk distributing misleading information, which can trigger enforcement action under the Investment Advisers Act's antifraud provisions.

**SOC 1 / SOC 2 Implications.** Many advisory firms and their service providers undergo SOC (System and Organization Controls) examinations. SOC 1 reports cover controls relevant to financial reporting, and SOC 2 reports cover security, availability, processing integrity, confidentiality, and privacy. Reconciliation processes are a key control tested in both SOC 1 and SOC 2 examinations. The examiner evaluates whether reconciliation is performed at the required frequency, whether breaks are investigated and resolved within defined timeframes, whether escalation procedures are followed, and whether the reconciliation process is documented and auditable. A reconciliation control failure can result in a qualified SOC opinion, which may cause downstream business consequences (clients and prospects may require an unqualified SOC report).

## Worked Examples

Three worked examples — a daily multi-custodian reconciliation design (ingestion schedule, auto-resolution rules, SOC 2 documentation, KPI targets), a root-cause investigation of a corporate-action break pattern (vendor delivery timing, cash-in-lieu gaps, spin-off basis), and a reconciliation automation build-out with exception-based processing — are in [references/examples.md](references/examples.md); load it when designing or troubleshooting a concrete reconciliation program.

## Common Pitfalls

- **Accepting timing breaks without verification.** It is tempting to classify all breaks as "timing" and assume they will self-resolve. While timing differences are common, labeling a genuine break as a timing difference delays resolution and can allow the break to compound. Every break classified as timing should be verified to have resolved within the expected window (typically one to two business days). If it does not resolve, it should be reclassified and investigated.
- **Reconciling positions but not cash or transactions.** Firms that reconcile only positions miss cash breaks (which can indicate missed dividends, incorrect fee debits, or unauthorized cash movements) and transaction breaks (which can indicate trades placed outside the PMS or duplicate entries). A complete reconciliation program covers all three dimensions.
- **Relying on the PMS as the source of truth.** The custodian, not the PMS, is the legally authoritative record of client assets. When a break is identified, the default assumption should be that the custodian is correct and the PMS needs updating — unless the firm has evidence to the contrary (such as a custodian processing error confirmed by the custodian's own inquiry process).
- **Ignoring cost basis reconciliation.** Because cost basis breaks do not affect current position counts or market values, they can be deprioritized until tax season, when they become urgent. By that point, historical cost basis discrepancies may be months or years old and extremely difficult to resolve. Regular cost basis reconciliation (monthly or quarterly) prevents this problem.
- **Setting auto-resolution tolerances too wide.** Overly generous auto-resolution rules can mask genuine breaks. For example, auto-resolving cash differences up to $100 may hide a pattern of missing dividend payments. Auto-resolution thresholds should be as tight as practical, and auto-resolved items should be sampled periodically for accuracy.
- **Not tracking break trends over time.** A reconciliation operation that resolves each day's breaks individually but never analyzes patterns over time will repeatedly fix the same types of breaks without addressing their systemic cause. Monthly break trend analysis is essential for continuous improvement.
- **Neglecting corporate action processing as a reconciliation input.** Corporate actions are the leading cause of non-timing breaks. Firms that treat corporate action processing and reconciliation as separate functions miss the opportunity to prevent breaks by ensuring timely and accurate corporate action processing upstream of the reconciliation cycle.
- **Underinvesting in data normalization.** Reconciliation automation is only as good as the data normalization layer. If security identifiers, transaction codes, or account mappings are incomplete or incorrect, the matching engine will generate false exceptions that waste analyst time and erode confidence in the system.
- **Failing to document break resolutions for audit purposes.** SOC auditors and SEC examiners expect to see documentation of every break: when it was identified, what caused it, what corrective action was taken, and when it was resolved. Undocumented resolutions are, from the auditor's perspective, the same as unresolved breaks.
- **Treating reconciliation as purely an operations function.** Reconciliation results directly affect compliance (accurate books and records), client reporting (accurate performance and positions), and revenue (accurate billing). The chief compliance officer and firm leadership should receive regular reconciliation reporting and be engaged when break rates deteriorate or systemic issues are identified.

## Cross-References

- **portfolio-management-systems** (advisory-practice plugin) — The PMS is one of the primary systems being reconciled. The PMS skill covers portfolio accounting, custodian data feeds, and the break identification process from the PMS perspective. This skill covers the broader reconciliation program design and operation.
- **settlement-clearing** (trading-operations plugin) — Settlement and clearing processes generate the transactions that are subsequently reconciled. Trade settlement failures and clearing discrepancies are a source of reconciliation breaks.
- **corporate-actions** (client-operations plugin) — Corporate action processing is the leading cause of non-timing reconciliation breaks. The corporate actions skill covers event processing; this skill covers the reconciliation of corporate action outcomes across systems.
- **books-and-records** (compliance plugin) — SEC Rule 204-2 and Rules 17a-3/17a-4 establish the recordkeeping obligations that reconciliation supports. Reconciliation documentation is itself part of the firm's books and records.
- **account-maintenance** (client-operations plugin) — Account-level changes (name changes, address updates, beneficiary changes, account re-registrations) can cause data discrepancies between systems if not synchronized, creating reconciliation breaks.
- **performance-reporting** (wealth-management plugin) — Performance calculations depend on accurate, reconciled position and transaction data. Unresolved reconciliation breaks can produce incorrect performance figures in client reports.
- **operational-risk** (trading-operations plugin) — Reconciliation failures are a category of operational risk. The operational risk skill covers the broader risk management framework; this skill covers the specific reconciliation controls that mitigate data accuracy risk.
- **fee-billing** (advisory-practice plugin) — Advisory fee billing depends on accurate AUM figures, which depend on reconciled position and market value data. Billing on unreconciled data risks overcharging or undercharging clients.

### Referencia: references/examples.md

# Reconciliation — Worked Examples

## Contents

1. [Example 1: Designing a Daily Reconciliation Process for a Multi-Custodian RIA](#example-1-designing-a-daily-reconciliation-process-for-a-multi-custodian-ria) — automated ingestion and matching schedule, exception review, SOC 2 documentation, KPI targets
2. [Example 2: Investigating and Resolving a Pattern of Corporate Action-Related Position Breaks](#example-2-investigating-and-resolving-a-pattern-of-corporate-action-related-position-breaks) — break categorization by event type, vendor timing root cause, corrective measures
3. [Example 3: Building Reconciliation Automation with Exception-Based Processing](#example-3-building-reconciliation-automation-with-exception-based-processing) — requirements, tool selection, normalization mapping, parallel run, steady-state metrics

## Example 1: Designing a Daily Reconciliation Process for a Multi-Custodian RIA

**Scenario:** An RIA manages $1.2 billion in assets across 2,400 accounts at two custodians (Schwab and Fidelity, approximately 60% and 40% of accounts respectively). The firm uses Orion as its portfolio management system. The current reconciliation process is semi-manual: an operations analyst downloads position files from each custodian each morning, loads them into a spreadsheet, and compares them against an Orion position export. The process takes approximately 3.5 hours each day and regularly identifies 30-60 breaks, of which roughly half are timing differences that resolve the next day. The firm wants to design an automated daily reconciliation process that reduces manual effort, provides consistent break tracking, and satisfies the firm's SOC 2 auditors.

**Design Considerations:**
- The firm needs to reconcile positions, cash, and transactions daily against both custodians.
- Schwab files arrive by 4:00 AM ET; Fidelity files arrive by 3:00 AM ET.
- The Orion end-of-day position and transaction data is available by 5:00 AM ET after the nightly batch completes.
- The firm has a two-person operations team that also handles trading and client service, so reconciliation must not consume more than 1 hour of analyst time per day under normal conditions.
- The SOC 2 auditor requires evidence of daily reconciliation, break tracking with aging, and documented resolution for every break.

**Analysis:**

Phase 1 — Automated Data Ingestion and Matching (pre-market, no human involvement):

The firm configures Orion's built-in reconciliation module (or a third-party reconciliation tool such as Advent Geneva, IVP Reconciliation, or a purpose-built solution) to automatically ingest custodian files. The system performs the following steps without manual intervention:
- 3:00-4:00 AM: Retrieve Fidelity and Schwab position, transaction, and cash files via SFTP.
- 5:00-5:30 AM: Retrieve Orion end-of-day position and transaction extracts.
- 5:30-6:00 AM: Normalize custodian data into a common format (map security identifiers via a CUSIP cross-reference, translate transaction type codes, standardize date formats).
- 6:00-6:30 AM: Execute automated matching — compare positions (share count by security by account), cash balances (settled cash plus pending settlements), and transactions (matched on security, account, quantity, trade date).
- 6:30-6:45 AM: Apply auto-resolution rules — mark timing differences that match the known one-day offset pattern for settlement, auto-accept rounding differences within the $1.00 cash tolerance, and auto-accept pricing differences within the 5 bps market value tolerance.
- 6:45-7:00 AM: Generate the daily exception report listing all unmatched and out-of-tolerance items.

Phase 2 — Exception Review (7:00-8:00 AM, one analyst):

The operations analyst reviews the exception report. Under steady-state operations, the expected exception volume after auto-matching and auto-resolution is 5-15 items per day (compared to 30-60 in the current manual process). For each exception, the analyst follows the investigation sequence described in Core Concepts Section 4: check for pending transactions, review the corporate action calendar, verify security identifier mappings, and check for manual trades. Most exceptions should be resolvable within 5-15 minutes each.

Phase 3 — Documentation and Reporting:

Every break and its resolution is documented in the reconciliation system with the fields required for SOC 2 audit: break date, category, severity, root cause, corrective action, resolution date, and analyst identity. The system produces a daily reconciliation summary report showing: total records compared, auto-matched records, auto-resolved records, exceptions requiring manual review, exceptions resolved same-day, and exceptions carried forward (with aging). A weekly summary is produced for management review, and a monthly summary is retained for the SOC 2 auditor.

Phase 4 — Performance Targets and Monitoring:

The firm establishes the following reconciliation KPIs:
- Auto-match rate for positions: target 98% (allowing for 2% corporate action and data feed exceptions).
- Auto-match rate for transactions: target 92%.
- Same-day exception resolution: target 85%.
- Maximum break aging: no break older than 5 business days without escalation to the operations manager.
- Analyst time spent on reconciliation: target under 1 hour per day.

These KPIs are tracked monthly and reported to the chief compliance officer. Deterioration in any metric triggers a root-cause review and process adjustment.

## Example 2: Investigating and Resolving a Pattern of Corporate Action-Related Position Breaks

**Scenario:** Over the past quarter, the operations team at a $600M RIA has observed that corporate action-related position breaks account for 45% of all breaks, up from approximately 20% in the prior year. The increase is not explained by higher corporate action volume in the market. The firm uses Black Diamond as its PMS and custodies assets at Fidelity. The operations manager asks the team to investigate the pattern, identify root causes, and implement corrective measures.

**Design Considerations:**
- The firm processes approximately 80-120 corporate actions per month (dividends, splits, mergers, spin-offs, tender offers).
- The Black Diamond PMS receives corporate action data from the Fidelity data feed and also from a third-party corporate action vendor integrated into the platform.
- The operations team has two analysts who spend approximately 30% of their time on break resolution, up from 15% a year ago due to the corporate action break increase.

**Analysis:**

Step 1 — Data Collection and Break Categorization:

The operations manager extracts break data for the past two quarters from the reconciliation system and categorizes corporate action breaks by sub-type:

| Corporate Action Type | Break Count (Q1) | Break Count (Q2) | Change |
|---|---|---|---|
| Cash dividends | 12 | 15 | +25% |
| Stock splits | 3 | 18 | +500% |
| Mergers / acquisitions | 5 | 22 | +340% |
| Spin-offs | 2 | 8 | +300% |
| Dividend reinvestment (DRIP) | 8 | 14 | +75% |
| Return of capital | 1 | 4 | +300% |
| **Total** | **31** | **81** | **+161%** |

The data reveals that the increase is concentrated in splits, mergers, and spin-offs — action types that require multi-step processing and cost basis adjustment. Cash dividend breaks increased modestly and are largely timing-related.

Step 2 — Root Cause Investigation for Splits and Mergers:

The team examines a sample of 15 split and merger breaks in detail. Findings:
- In 11 of 15 cases, the custodian (Fidelity) processed the action on the effective date, but the Black Diamond PMS did not process it until 1-3 business days later.
- The delay is traced to a change in the third-party corporate action vendor's data delivery schedule. Six months ago, the vendor changed its delivery time from 6:00 PM ET (day before effective date) to 10:00 PM ET (day of effective date). Black Diamond's nightly batch runs at 9:00 PM ET, so actions delivered at 10:00 PM are not processed until the following night — creating a guaranteed one-day lag relative to the custodian.
- In 4 of 15 cases, the action involved a complex merger with mixed consideration (cash plus stock) and fractional share cash-in-lieu. The automated processing applied the exchange ratio correctly but failed to generate the cash-in-lieu transaction for fractional shares, causing both a position break (fractional share difference) and a cash break (missing cash-in-lieu payment).

Step 3 — Root Cause Investigation for Spin-Offs:

The team examines the 8 spin-off breaks. Findings:
- In 6 of 8 cases, the parent company cost basis was not reallocated to the spun-off entity. The PMS created the new position with the correct share count but assigned zero cost basis, while the custodian allocated cost basis using the IRS-prescribed allocation methodology (based on fair market values on the distribution date). This created a cost basis break but not a position break.
- In 2 of 8 cases, the PMS failed to create the new spin-off security position entirely because the new security's CUSIP was not yet in Black Diamond's security master at the time of processing.

Step 4 — Corrective Measures:

The operations manager implements the following changes:

(a) Vendor delivery timing fix: Contact the corporate action data vendor and request a return to the earlier delivery schedule, or configure Black Diamond to run a second mini-batch at 11:00 PM ET specifically for corporate action processing. The second option is implemented because the vendor cannot change its delivery time for a single client.

(b) Fractional share cash-in-lieu rule: Create a post-processing check for all merger and acquisition actions — after the exchange ratio is applied, verify that the resulting position has no fractional shares. If fractional shares exist and the action terms specify cash-in-lieu, generate the cash-in-lieu transaction automatically.

(c) Spin-off cost basis automation: Configure the PMS to automatically apply cost basis reallocation for spin-offs using the custodian's allocation percentages (sourced from the custodian data feed or a reference data provider). Require operations analyst review and approval before the reallocation is posted, to catch errors in the allocation percentages.

(d) New security CUSIP monitoring: Implement a daily check of upcoming corporate actions against the PMS security master. Any action that references a CUSIP not in the security master triggers an alert to the operations team, who can add the security proactively before the effective date.

Step 5 — Monitoring and Target Setting:

The operations manager sets a target of reducing corporate action breaks to no more than 25% of total breaks (from the current 45%) within two quarters. The reconciliation dashboard is updated to include a corporate action break sub-report with the categories above, enabling ongoing monitoring without manual data extraction.

## Example 3: Building Reconciliation Automation with Exception-Based Processing

**Scenario:** A rapidly growing RIA has doubled its account count from 1,500 to 3,000 accounts over the past 18 months without adding operations staff. The reconciliation process, which was adequate at 1,500 accounts, is now overwhelmed. The two operations analysts are spending 4-5 hours per day on reconciliation (split between two custodians), leaving insufficient time for other operations tasks (trading, client service, account maintenance). The firm's reconciliation break rate has risen from 1.5% to 4% of accounts as analysts cut corners to manage the volume. The chief operations officer decides to invest in reconciliation automation to restore quality while supporting continued growth.

**Design Considerations:**
- The firm uses Tamarac as its PMS and custodies at Schwab and Pershing.
- The current process is spreadsheet-based: analysts manually download files, paste into comparison templates, and visually scan for differences.
- The firm's budget supports a mid-range reconciliation solution (not an enterprise platform like Advent Geneva, but more than a spreadsheet).
- The goal is to reduce analyst reconciliation time to under 1 hour per day while improving the break rate to under 1% of accounts.

**Analysis:**

Phase 1 — Requirements Definition and Tool Selection (Weeks 1-3):

The COO defines functional requirements for the reconciliation solution:
- Automated ingestion of Schwab and Pershing data files (position, transaction, cash) via SFTP.
- Automated ingestion of Tamarac end-of-day data via API or file export.
- Configurable matching rules: position matching on CUSIP + account + share count; transaction matching on CUSIP + account + quantity + trade date; cash matching on account + settled balance with tolerance.
- Auto-resolution rules for timing differences, rounding, and known pricing discrepancies.
- Exception dashboard with break categorization, severity, aging, and assignment to analyst.
- Resolution documentation workflow (root cause, corrective action, resolution date).
- Daily, weekly, and monthly reporting for management and SOC auditors.
- Break trend analysis and pattern detection over time.

The firm evaluates three options: (a) Tamarac's built-in reconciliation module, which handles position matching but lacks advanced auto-resolution and reporting; (b) a mid-market reconciliation platform (such as Arcesium, Duco, or a similar SaaS offering) that provides configurable matching, auto-resolution, and reporting; (c) a custom-built solution using the firm's existing technology stack. The firm selects option (b) for its balance of capability and cost.

Phase 2 — Implementation and Configuration (Weeks 3-8):

Data connectivity: Configure SFTP connections to Schwab and Pershing for automated file retrieval. Configure API or file-based data extraction from Tamarac. Test file ingestion for all three sources over a two-week period to identify format issues or delivery timing gaps.

Normalization mapping: Build the cross-reference tables for security identifiers (CUSIP mapping between Tamarac, Schwab, and Pershing), transaction type codes (translating each source's taxonomy into a common set), and account identifiers (PMS account number to custodian account number mapping for all 3,000 accounts).

Matching rule configuration: Define position matching rules (exact match on CUSIP + account number, zero tolerance on share count). Define transaction matching rules (match on CUSIP + account + quantity + trade date, with a one-day tolerance window for settlement timing). Define cash matching rules (match on account, $2.00 tolerance for rounding).

Auto-resolution rule configuration: Configure auto-resolution for: (a) timing breaks where the offsetting transaction appears within one business day; (b) cash rounding differences within $2.00; (c) market value differences within 5 bps attributable to a known pricing source difference; (d) fractional share differences of less than 0.01 shares (common with DRIP).

Phase 3 — Parallel Run and Validation (Weeks 8-10):

Run the automated reconciliation system in parallel with the existing manual process for two full weeks. Compare results: every break identified by the manual process should also be identified by the automated system. Any break caught manually but missed by the automated system indicates a matching rule gap that must be corrected before cutover. Conversely, the automated system may identify breaks that the manual process missed (a positive outcome that validates the investment).

Phase 4 — Cutover and Optimization (Weeks 10-12):

Transition to the automated system as the primary reconciliation process. During the first two weeks post-cutover, analysts review all auto-resolved items to validate that the auto-resolution rules are functioning correctly and not masking genuine breaks. Adjust rules as needed based on this review.

Phase 5 — Steady-State Performance Monitoring:

Post-implementation, the firm tracks the following metrics against targets:

| Metric | Pre-Automation Baseline | Target | Measurement Cadence |
|---|---|---|---|
| Analyst time per day | 4-5 hours | Under 1 hour | Monthly |
| Break rate (% of accounts) | 4.0% | Under 1.0% | Weekly |
| Auto-match rate (positions) | N/A (manual) | 97%+ | Daily |
| Auto-match rate (transactions) | N/A (manual) | 90%+ | Daily |
| Same-day resolution rate | ~60% | 85%+ | Weekly |
| Breaks aged over 5 days | ~8% of breaks | Under 2% | Weekly |

The capacity gained by automation (approximately 3-4 analyst hours per day) is redirected to other operations functions: trading support, client service, and account maintenance. The firm can now support continued account growth without adding operations headcount specifically for reconciliation until account volume reaches approximately 6,000-8,000 accounts, depending on break rates.


---

## SKILL: reference-data

- Fuente: `JoelLewis/finance_skills` → `plugins/data-integration/skills/reference-data` (MIT)
- Cuándo usarla: Design and manage reference data systems — security master, client master, account master, identifier mapping, pricing data sources, golden source designation, and governance. Use when building or evaluating a security master database, mapping identifiers across systems (CUSIP to ISIN, SEDOL to FIGI), designing client master models for onboarding or KYC, defining account master attributes across custodians, designating golden sources and MDM patterns across systems, establishing a pricing vendor hierarchy with fallback order, establishing reference data governance and stewardship, handling identifier changes from corporate actions, or troubleshooting issues traced to missing or changed identifiers. Trigger on: security master, CUSIP, ISIN, SEDOL, FIGI, client master, account master, pricing data, reference data, golden source, MDM, master data, identifier mapping, data governance, vendor hierarchy.

# Reference Data

## Core Concepts

### 1. Security Master

The security master is the authoritative repository of instrument-level reference data, serving as the foundation for portfolio management, trading, performance, reporting, and compliance systems.

**Core fields:** Identifiers (CUSIP, ISIN, SEDOL, FIGI, ticker, internal ID), classification (asset class, sub-class, GICS sector, country, currency), issuer information (name, LEI, ratings), terms and conditions (asset-class-specific contractual attributes), and pricing factors (multiplier, day count, settlement convention).

**Asset-class-specific attributes:** Equity (shares outstanding, market cap, sector, exchange, dividend frequency). Fixed income (coupon, maturity, call schedule, credit rating, seniority, day count). Funds (NAV, expense ratio, share class, distribution frequency, load structure). ETFs (NAV, indicative value, expense ratio, underlying index). Options (underlying, strike, expiration, type, multiplier, exercise style). Alternatives (strategy type, vintage year, commitment, capital call schedule, valuation frequency).

**Security lifecycle events:** IPO/listing (new record creation with all required fields), corporate actions (splits, mergers, spin-offs, name/ticker/exchange changes — the single largest source of security master data quality issues), and delisting/maturity (flag as inactive, retain historical record for performance and audit).

**Golden source designation:** The security master should be the firm's golden source for instrument reference data. All downstream systems retrieve security attributes from it rather than maintaining independent copies.

### 2. Identifier Systems

Financial instruments carry multiple overlapping identifiers. No single scheme is universally sufficient.

- **CUSIP** — 9-character (6 issuer + 2 issue + 1 check digit), US/Canada securities, administered by CUSIP Global Services (FactSet). Changes on fundamental term changes (mergers, reorganizations).
- **ISIN** — 12-character (2 country + 9 national ID + 1 check digit), ISO 6166, globally unique. Required for MiFID II, EMIR reporting. Wraps the national identifier (CUSIP in US, SEDOL in UK).
- **SEDOL** — 7-character, assigned by the London Stock Exchange for LSE and UK/Irish listings. A single security may have different SEDOLs per listing exchange.
- **FIGI** — 12-character, developed by Bloomberg under OMG standard. Open-source and freely available (unlike CUSIP/SEDOL). Distinguishes instrument-level, composite, and exchange-level identifiers.
- **Ticker symbols** — Exchange-assigned, not globally unique, change frequently. Never use as a primary identifier; use only for display or trading convenience.
- **Internal identifiers** — Firm-generated (UUID or sequential integer), immutable across the security's life. Serves as the stable key linking all external identifiers.

**Identifier mapping:** The security master must maintain a cross-reference table linking all identifiers per security. Challenges include one-to-many relationships (one ISIN to multiple SEDOLs), temporal changes from corporate actions (versioned mappings for point-in-time lookups), and vendor discrepancies requiring conflict resolution.

### 3. Client Master

The client master is the authoritative repository of client-level reference data supporting onboarding, account management, KYC/AML compliance, reporting, and relationship management.

**Data model:** Individuals (legal name, DOB, SSN/TIN, address, phone, email, citizenship, employment). Entities (legal name, EIN, formation state/country, entity type, formation date). Trusts (trust name, type, grantor, trustee, beneficiaries, governing law).

**Identity management:** Each client must have a single unique identifier regardless of how many accounts or roles they hold. Deduplication is critical for regulatory reporting, household billing, cross-account compliance (wash sales), and unified servicing.

**Household and relationships:** Household grouping links related clients for billing, reporting, and planning. Relationship types include spouse, parent/child, trustee/beneficiary, authorized signer, trusted contact. Advisor assignment (primary, secondary, service team) is tracked here.

**KYC/AML data:** Verification status, method, risk rating, PEP status, OFAC screening results, beneficial ownership (entities), source of funds/wealth, EDD flags.

**Client preferences:** Communication channel, statement delivery, language, investment preferences (ESG exclusions, sector restrictions), tax lot method preference.

**Golden source:** CRM is typically the golden source for relationship and advisory data; custodian is the golden source for regulatory identity data (legal name, SSN, address of record). The client master integrates both and enforces synchronization.

### 4. Account Master

The account master stores attributes and configuration of every client account, linking accounts to clients and driving trading, billing, reporting, and compliance.

**Attributes:** Registration (individual, joint, trust, IRA, Roth, SEP, 401(k), corporate, estate, UGMA/UTMA), account type (advisory, brokerage, wrap, retirement, education, charitable), tax status (taxable, tax-deferred, tax-exempt), custodian, advisor, model assignment, features (margin, options level, DRIP, cost basis method).

**Account-to-client relationships:** Owner, authorized party (POA, trading authorization), beneficiary, trustee, custodian (for UGMA/UTMA).

**Status management:** Active, restricted (regulatory hold, death notification, legal dispute), closed (retain historical data per books-and-records requirements), dormant (escheatment/unclaimed property exposure).

**Cross-system identification:** Custodian account number, PMS account ID, CRM account ID, and billing account ID may all differ. The account master maintains mappings and provides a canonical internal ID as the cross-system key.

### 5. Pricing Data

Pricing is the most time-sensitive reference data category. Incorrect prices propagate immediately into valuations, performance, billing, and compliance.

**End-of-day pricing:** Official exchange close (4:00 PM ET for US equities), mutual fund NAV (available 6:00-7:00 PM ET), evaluated pricing for infrequently traded fixed income (Bloomberg, ICE, Refinitiv models).

**Pricing hierarchy:** Define a preferred source per security type with automatic fallback. Example: US equities — exchange close, then Bloomberg, then Refinitiv. Corporate bonds — ICE evaluated, then Bloomberg BVAL, then Refinitiv. Alternatives — manager/GP valuation, then third-party appraisal, then internal model.

**Fair value pricing:** Adjust international securities' closing prices for subsequent market, currency, and news developments when foreign exchanges close hours before the US close. Prevents stale-price arbitrage in mutual funds.

**Pricing validation and stale-price detection:** Validation-rule design and execution (variance checks, zero/negative-price detection, stale-price windows, cross-source comparison, threshold calibration) are owned by the **data-quality** skill (data-integration plugin); reference-data owns the source hierarchy those rules validate against.

**Manual overrides:** Restricted to authorized users, documented with reason and source, logged in an audit trail, time-limited pending vendor correction.

### 6. Reference Data Governance

Governance establishes the structures, policies, and processes ensuring reference data is accurate, complete, timely, and consistent.

**Data ownership:** Each domain has a designated owner — security master (investment operations), client master (co-owned by compliance and advisory practice), account master (operations/client services), pricing (portfolio accounting/valuation). Owners are accountable for quality and authorize changes to definitions and sources.

**Data stewardship:** Stewards execute governance daily — monitoring quality dashboards, resolving exceptions, coordinating with vendors, approving overrides, maintaining data dictionaries.

**Data quality metrics:** Measure reference data on the standard quality dimensions (completeness, accuracy, timeliness, consistency). Dimension definitions, validation-rule design, profiling, exception management, and threshold calibration are owned by the **data-quality** skill (data-integration plugin).

**MDM patterns:** Registry (links only, no conflict resolution), consolidation (read-only golden record aggregated from sources), coexistence (bidirectional sync between MDM and sources), transaction/hub (single system of entry for all reference data).

**Change management:** Impact analysis before changes, non-production testing, downstream notification, rollback procedures, post-change validation.

**Audit trail:** Log every change with old value, new value, timestamp, user/process, and reason. Required for regulatory examination, dispute resolution, and root-cause analysis.

### 7. Reference Data Distribution

Mastered reference data must be distributed reliably to all consuming systems.

**Publishing models:** Event-driven/push (message bus or event stream for near-real-time propagation), polling/pull (scheduled queries — simpler but introduces latency), bulk/files (CSV/XML/JSON via SFTP or S3 for EOD snapshots), API/on-demand (point-of-need retrieval — eliminates cache staleness but creates runtime dependency).

**Delta distribution:** Send only changed records since the last distribution. Requires change tracking, sequencing, and full-refresh fallback capability.

**Caching:** Local caching in consuming systems reduces latency but risks staleness. Mitigate with TTL policies, event-driven cache invalidation, and version numbers.

**Point-in-time retrieval:** Support queries for the state of any record as of a specific date. Required for historical performance, regulatory reporting, and audit. Implement via effective-date/expiration-date columns or full history tables.

### 8. Vendor Management

Data vendors are the primary external source for security reference data, pricing, ratings, and identifiers.

**Major vendors:** Bloomberg (broad coverage, FIGI, real-time pricing), Refinitiv/LSEG (global coverage, evaluated pricing), ICE Data Services (fixed income pricing, indices), S&P Global (ratings, CUSIP, fundamentals), Moody's (credit ratings, risk data), FactSet (multi-source aggregation, CUSIP Global Services), MSCI (ESG ratings, factor data, indices).

**Evaluation criteria:** Coverage (asset classes, geographies), quality (accuracy, completeness, error correction), timeliness (availability relative to processing deadlines), format/delivery (API, file, schema stability), licensing terms (redistribution rights, per-user fees), cost (total cost of ownership), support quality.

**Multi-vendor strategy:** Source critical data from at least two vendors — primary, backup, and arbitration rules for disagreements.

**Vendor monitoring:** Track file arrival times, monitor record counts for unexpected drops, compare against independent sources, maintain quarterly vendor scorecards, escalate persistent quality issues.

## Worked Examples

### Example 1: Designing a Security Master for a Multi-Custodian Advisory Firm

**Scenario:** An RIA manages $1.2B across 1,500 accounts at Schwab and Fidelity, trading US/international equities, ETFs, mutual funds, corporate bonds, and municipal bonds. Each custodian feed populates separate security tables — no unified security master exists. Recurring issues: the same mutual fund appears with different names per custodian, corporate bonds lack consistent credit ratings, and a stock split was processed for Schwab but missed for Fidelity because corporate actions were handled independently.

**Design considerations:** The firm defines a security master record with immutable internal UUID, all external identifiers (CUSIP, ISIN, SEDOL, FIGI, ticker, custodian-specific IDs), classification fields (asset class, GICS sector, credit tier), issuer data (name, LEI, country), asset-class-specific terms, pricing fields, and status. A cross-reference table links each internal ID to all external identifiers with effective dates for point-in-time lookups. Bloomberg is the primary vendor for reference data and pricing; ICE is secondary for fixed income; custodian feeds provide reconciliation checks; CUSIP Global Services provides identifier change notifications. All corporate actions are processed through the security master first, then propagated to both custodians — eliminating inconsistent processing. Data quality controls include daily completeness and pricing validation checks, weekly cross-vendor pricing comparison, and monthly classification audits.

**Analysis:** The centralized security master eliminates the root cause — disparate, unreconciled security data. The internal UUID survives corporate actions, identifier changes, and custodian transitions. The most significant ongoing cost is the corporate action workflow, requiring a dedicated data operations analyst as security master steward.

### Example 2: Implementing Pricing Data Management with Validation and Exception Handling

**Scenario:** An asset manager runs nightly valuations for 30 separate accounts and 5 commingled funds holding 2,000 securities (US/international equities, corporate/municipal bonds, MBS). Pricing comes from a single vendor (Refinitiv). Past incidents: a municipal bond valued at zero for three days unnoticed, an international equity stale for a week during a local holiday, a corporate bond evaluated price off by 15% due to vendor error.

**Design considerations:** The firm establishes a tiered pricing hierarchy per asset class with automatic fallback (e.g., corporate bonds: ICE evaluated, then Refinitiv, then Bloomberg BVAL). Automated validation runs before loading: variance check (15% equity, 5% bonds), zero-price check, stale-price check (2 days equities, 5 days bonds, adjusted for local holidays), cross-vendor comparison (flag >2% divergence for fixed income), currency verification, reasonableness bounds. Exceptions are severity-classified (critical/high/medium/low) and appear on a pricing dashboard. Critical exceptions trigger immediate alerts; the pricing analyst investigates, resolves (accept with documentation, substitute from backup vendor, or manual override), and logs all actions. Unresolved exceptions escalate after defined time windows. For international equities, a fair value model adjusts foreign closing prices using US market movement, currency changes, and sector ETF data.

**Analysis:** The framework transforms pricing from passive receipt to active quality control. Multi-vendor hierarchy eliminates single-vendor dependency. Automated validation catches all three prior incident types. A well-run pricing operation targets exception rates below 2% of the universe per day, with same-day resolution for critical and high-severity exceptions.

### Example 3: Building Client Master Data Governance for Regulatory Compliance

**Scenario:** A wealth management firm serving 3,000 households discovers poor client data quality: 12% incomplete addresses, 8% stale employment data (clients known to be retired still listed as employed), 5% of entity clients missing beneficial ownership documentation, and inconsistent household groupings causing billing errors (missing breakpoint discounts). Client data exists in three systems (Salesforce CRM, Schwab custodian, Orion PMS) with no designated golden source and divergent records. The firm must remediate and establish governance before FinCEN's investment adviser AML/CFT program requirements take effect — originally January 1, 2026, delayed by FinCEN to January 1, 2028 (status as of June 2026; verify current).

**Design considerations:** Data owners are assigned by domain: client identity (CCO — regulatory significance), client relationships (Head of Client Services — servicing and billing), client financial profile (CIO — suitability). Golden sources: Schwab for legal identity data (verified through CIP, used for 1099s), Salesforce for relationship/advisory data, Orion as a consumer only (synchronized from the other two, not edited directly). Remediation: incomplete addresses resolved by cross-referencing CRM against custodian and contacting clients for gaps (target 100% in 90 days); stale employment flagged for clients 60+ not updated in two years, with automated triggers when systematic withdrawals begin; missing beneficial ownership collected using FinCEN forms, prioritized by account size (target 100% in 60 days); household groupings identified via shared addresses/phones/names, confirmed by advisors, with overbilling refunds issued. Ongoing governance: daily automated quality checks with exception dashboard, weekly steward review of trends, monthly metrics reporting to operations committee, quarterly governance review with data owners, annual comprehensive data refresh for inactive clients.

**Analysis:** The program addresses both immediate gaps and structural causes. Golden source designation eliminates cross-system ambiguity. The remediation requires significant advisor engagement, best positioned as a client service improvement. FinCEN's effective date (January 1, 2028 after the delay) still warrants early remediation — complete, verified client identity data takes years to build.

## Common Pitfalls

1. **Using ticker symbols as primary identifiers.** Tickers are not globally unique, change frequently, and are recycled. Systems keyed on tickers break during corporate actions.
2. **Maintaining separate security records per custodian.** The same instrument appears as multiple securities, causing duplicated positions and inconsistent corporate action processing.
3. **Treating pricing as passive data receipt.** Loading vendor prices without validation allows zero prices, stale prices, and vendor errors to propagate into valuations and billing.
4. **No designated golden source for client data.** Multiple systems maintaining client data without hierarchy causes drift, conflicts, and no authoritative record.
5. **Ignoring temporal versioning.** Overwriting current state without preserving history prevents point-in-time reporting, historical performance, and audit support.
6. **Underinvesting in corporate action processing.** Corporate actions are the primary source of security master failures — treating them as low-priority clerical work causes persistent reconciliation breaks.
7. **Single-vendor pricing dependency.** No backup source means manual pricing when the vendor is late, missing, or incorrect — which does not scale.
8. **Neglecting data quality metrics.** Without measuring completeness, accuracy, timeliness, and consistency, issues are invisible until they cause downstream failures.
9. **Point-to-point integrations instead of central reference data service.** Each consuming system connecting directly to vendors creates N redundant copies with independent quality issues.
10. **Failing to plan for identifier changes during corporate actions.** Systems that do not handle CUSIP/ISIN/ticker changes gracefully lose position history and break performance chains.

## Cross-References

- **market-data** (data-integration plugin) — Market data covers real-time pricing and trade data; reference data provides the instrument master that market data references.
- **data-quality** (data-integration plugin) — General data quality principles (profiling, validation, monitoring) applied here specifically to financial reference data.
- **integration-patterns** (data-integration plugin) — Integration patterns (event-driven, batch, API) are the mechanisms for distributing reference data.
- **portfolio-management-systems** (advisory-practice plugin) — The PMS is a primary consumer of security master, pricing, and account master data.
- **reconciliation** (client-operations plugin) — Reference data mismatches (identifiers, stale prices) are a leading cause of reconciliation breaks.
- **corporate-actions** (client-operations plugin) — Corporate actions drive security master changes; this skill covers the resulting reference data updates.
- **know-your-customer** (compliance plugin) — KYC requirements define what client data must be collected; the client master stores and governs it.
- **books-and-records** (compliance plugin) — Reference data records are books and records subject to retention and examination requirements.


---

## SKILL: reg-bi

- Fuente: `JoelLewis/finance_skills` → `plugins/compliance/skills/reg-bi` (MIT)
- Cuándo usarla: Analyze the broker-dealer standard of conduct under SEC Regulation Best Interest's four obligations: Disclosure, Care, Conflict of Interest, and Compliance. Owns what triggers a 'recommendation' under Reg BI and the canonical comparison of Reg BI vs FINRA suitability vs IA fiduciary duty. Use when the user asks whether a broker-dealer recommendation satisfies Reg BI, how to evaluate reasonably available alternatives, rollover recommendation compliance, dual-registrant capacity disclosure, share class or account type recommendations, or Reg BI examination preparation. Also trigger when users mention 'best interest standard for brokers', 'is this a Reg BI recommendation', 'care obligation documentation', 'sales contest elimination requirement', or ask how Reg BI differs from suitability or fiduciary duty. (For the IA fiduciary duty itself and DOL rules, use fiduciary-standards.)

# SEC Regulation Best Interest (Reg BI)

Regulatory status current as of June 2026 — verify effective dates, dollar thresholds, and pending rulemakings against current SEC/FINRA/FinCEN sources before advising.

## Core Concepts

### What Constitutes a "Recommendation" Under Reg BI
Reg BI applies whenever a broker-dealer or associated person makes a "recommendation" to a "retail customer" of any securities transaction or investment strategy involving securities, including account type recommendations. The SEC adopted the existing FINRA framework for what constitutes a recommendation but expanded its scope:

- **Explicit recommendations:** "You should buy X" or "I recommend allocating to Y."
- **Account type recommendations:** Recommending a brokerage account vs an advisory account, or a specific account type (margin, options-enabled, fee-based).
- **Implicit hold recommendations:** Agreeing with a customer's decision to continue holding a security when the associated person has a duty to monitor or review the account.
- **Rollover recommendations:** Advising a customer to roll assets from an employer plan (401(k), 403(b), pension) to an IRA. The SEC has specifically identified rollovers as triggering Reg BI (see SEC Staff Bulletin on Account Recommendations, 2022).
- **Investment strategy recommendations:** Recommending a strategy involving securities, such as a particular asset allocation, use of leverage, or concentration approach.

The "facts and circumstances" test considers whether the communication could reasonably be viewed as a suggestion to act. General education, broad asset allocation models without a specific recommendation, and responses to unsolicited orders generally do not trigger Reg BI.

### Disclosure Obligation (17 CFR 240.15l-1(a)(2)(i))
Before or at the time of a recommendation, the broker-dealer must provide the retail customer with full and fair disclosure of all material facts relating to the scope and terms of the relationship, including:

- **Form CRS (Relationship Summary):** A standardized, plain-language document (Form ADV Part 3 / Form CRS) that must be delivered at or before the earliest of: (1) a recommendation, (2) placing an order, or (3) opening an account. Form CRS describes the types of services, fees, conflicts, legal standard of conduct, and disciplinary history.
- **Material facts about the relationship:** The capacity in which the firm is acting (broker-dealer vs investment adviser), the material fees and costs the customer will incur, and the type and scope of services provided.
- **Material facts about conflicts of interest:** All material conflicts associated with the recommendation, including compensation-related conflicts (revenue sharing, 12b-1 fees, proprietary product incentives), conflicts arising from the firm's business model, and conflicts specific to the associated person.

Disclosure alone does not satisfy the obligation. The disclosure must be "full and fair" — it must be specific enough that a retail customer can understand the conflict and how it could affect the recommendation.

### Care Obligation (17 CFR 240.15l-1(a)(2)(ii))
The care obligation requires the broker-dealer and associated person to exercise reasonable diligence, care, and skill when making a recommendation. It operates at three levels:

- **Product-level:** The associated person must understand the potential risks, rewards, and costs of the security or strategy being recommended. This includes reading the prospectus or offering documents, understanding the product's structure and features, and knowing the fee layers.
- **Customer-level:** The recommendation must be in the best interest of the particular retail customer based on that customer's investment profile. The investment profile includes, but is not limited to: age, other investments, financial situation and needs, tax status, investment objectives, investment experience, investment time horizon, liquidity needs, risk tolerance, and any other information the customer discloses.
- **Reasonably available alternatives:** The associated person must have a reasonable basis to believe the recommendation is the best of the reasonably available alternatives. This does not require an evaluation of every possible alternative in the market, but the associated person must consider the alternatives the firm makes available and not recommend a more expensive or riskier product when a less expensive or less risky alternative available through the firm would equally serve the customer's needs.
- **No excessive costs or risks:** The associated person must not place their interest ahead of the customer's. Recommendations must not subject the customer to excessive costs, excessive trading (churning), or excessive risk relative to the customer's profile. A series of recommendations that are each individually suitable but collectively excessive (e.g., frequent switching between fund families) can violate the care obligation.

The SEC has emphasized that the care obligation is not a "best execution" or "lowest cost" standard, but cost is a factor that must be considered. When two products are substantially similar in features and risk, but one is significantly cheaper, recommending the more expensive product requires a documented, reasonable basis for why the costlier option better serves the customer.

### Conflict of Interest Obligation (17 CFR 240.15l-1(a)(2)(iii))
The broker-dealer must establish, maintain, and enforce written policies and procedures reasonably designed to:

- **Identify conflicts of interest:** Map all material conflicts associated with recommendations, including compensation structures, revenue sharing, proprietary products, principal trading, allocation of limited investment opportunities, and any other financial incentive that could influence recommendations.
- **Disclose conflicts or mitigate them:** At a minimum, disclose all material conflicts. For conflicts that create incentives for the associated person to place their interest ahead of the customer's interest, the firm must mitigate the conflict (disclosure alone is not sufficient for these conflicts).
- **Mitigation measures:** Common mitigation approaches include reducing variable compensation tied to specific products, implementing product-neutral compensation grids, leveling commission payouts across similar products, adjusting supervisory review for high-conflict recommendations, and limiting the scope of products an associated person can recommend where conflicts are severe.
- **Eliminate certain conflicts:** Reg BI requires outright elimination of sales contests, sales quotas, bonuses, and non-cash compensation that are based on the sale of specific securities or specific types of securities within a limited period of time. This is the only area where Reg BI mandates elimination rather than mitigation.

### Compliance Obligation (17 CFR 240.15l-1(a)(2)(iv))
The broker-dealer must establish, maintain, and enforce written policies and procedures reasonably designed to achieve compliance with the Disclosure, Care, and Conflict of Interest obligations. This includes:

- Written supervisory procedures addressing each of the three substantive obligations
- Training programs for associated persons on Reg BI requirements
- Supervisory systems to review recommendations for compliance
- Documentation requirements for the basis of recommendations
- Periodic testing and review of the compliance program's effectiveness
- Escalation procedures for identified violations

The Compliance Obligation is a "reasonably designed" standard — it does not require perfection, but the firm must demonstrate a genuine, good-faith effort to build and maintain an effective compliance infrastructure.

### Reg BI vs FINRA Suitability
Reg BI replaced and enhanced the FINRA suitability standard (FINRA Rule 2111) for recommendations to retail customers:

| Dimension | FINRA Suitability | Reg BI |
|-----------|------------------|--------|
| Standard | "Suitable" for the customer | "Best interest" of the customer |
| Scope | Securities transactions and strategies | Adds account type recommendations, explicit rollover coverage |
| Alternatives | No explicit requirement to consider alternatives | Must consider reasonably available alternatives |
| Conflicts | Disclosure-based (general obligation to disclose) | Identify, disclose, mitigate, or eliminate — with mandatory elimination of sales contests |
| Cost consideration | Cost is a factor but not emphasized | Explicit requirement not to recommend costlier products without reasonable basis |
| Compliance | General supervisory obligations | Dedicated compliance obligation with written policies and procedures |
| Applies to | All customers (retail and institutional) | Retail customers only (natural persons using recommendations for personal, family, or household purposes) |

Reg BI is an enhanced standard that goes beyond suitability but is not a fiduciary standard. The SEC explicitly stated that Reg BI does not create a fiduciary duty for broker-dealers.

### Reg BI vs IA Fiduciary Duty
Investment advisers owe a fiduciary duty under the Investment Advisers Act of 1940, as interpreted by the SEC and courts. Reg BI and the IA fiduciary duty are parallel but distinct standards:

| Dimension | Reg BI (Broker-Dealer) | IA Fiduciary Duty |
|-----------|----------------------|-------------------|
| Legal source | Exchange Act Section 15l-1 | Advisers Act Sections 206(1) and 206(2) |
| Standard | Best interest at time of recommendation | Ongoing duty of care and loyalty |
| Duration | Transaction-specific (at time of recommendation) | Continuous throughout the advisory relationship |
| Monitoring | No ongoing monitoring duty (unless agreed to) | Ongoing duty to monitor and update advice |
| Conflicts | Identify, disclose, mitigate, or eliminate | Must either eliminate or provide informed consent (full and fair disclosure + client consent) |
| Compensation | Commission-based compensation permitted | Fee-based; must disclose and manage all compensation conflicts |

The key practical distinction: Reg BI is a point-of-recommendation standard, while the IA fiduciary duty is a relationship-level, ongoing obligation.

### Rollover Recommendations Under Reg BI
The SEC issued Staff Bulletin: Standards of Conduct for Broker-Dealers and Investment Advisers — Account Recommendations for Retail Investors (2022), specifically addressing rollovers. Key points:

- A recommendation to roll assets from an employer-sponsored plan (401(k), 403(b), 457(b), pension) to an IRA is a recommendation of both an account type and a securities transaction, triggering Reg BI.
- The associated person must consider factors including: investment options in the existing plan vs the IRA, fees and expenses in each (plan-level fees, fund expense ratios, advisory or brokerage fees), available services (investment guidance, managed accounts, financial planning), penalty-free withdrawal features (e.g., separation from service after age 55 for 401(k) plans under IRC 72(t)(2)(A)(v)), protection from creditors (ERISA protections in employer plans vs state-law protections for IRAs), required minimum distribution rules, and Net Unrealized Appreciation (NUA) eligibility for employer stock (IRC 402(e)(4) — if the plan holds appreciated employer securities, an in-kind distribution to a taxable account may allow long-term capital gains treatment on the appreciation rather than ordinary income treatment upon later IRA distribution; rolling the stock into an IRA forfeits NUA treatment permanently).
- The firm must document the basis for the rollover recommendation, including the comparison of alternatives (stay in plan, roll to new employer plan, roll to IRA, take a cash distribution).
- "Do nothing" (remaining in the current plan) is a reasonably available alternative that must be considered.

### Dual-Registrant Considerations
Many firms and individuals are registered as both broker-dealers and investment advisers. When interacting with a retail customer, the dual-registrant must:

- **Clearly disclose capacity:** Whether acting in a broker-dealer capacity (Reg BI applies) or investment adviser capacity (fiduciary duty applies). This must be communicated clearly, not buried in fine print.
- **Apply the correct standard:** The standard of conduct depends on the capacity in which the recommendation is made, not the registration status of the firm.
- **Avoid confusion:** The SEC has warned against dual-registrants who "hat-switch" — moving a customer between BD and IA capacity without clear disclosure, potentially to exploit the less demanding standard for a given interaction.
- **Form CRS requirement:** Dual-registrants must provide a single Form CRS that describes both the brokerage and advisory relationships, enabling the customer to compare the two.

### SEC Staff Bulletins on Reg BI
The SEC Division of Examinations and Staff have issued a series of interpretive bulletins providing practical guidance:

- **Staff Bulletin on the Care Obligation (April 2023):** Clarified that cost is an important factor; when two products are comparable but differ in cost, the firm needs a reasonable basis for recommending the more expensive one. Emphasized that a "series of recommendations" must be evaluated holistically — individually suitable recommendations can collectively violate the care obligation.
- **Staff Bulletin on Conflicts of Interest (2022):** Clarified that disclosure alone is not sufficient for material conflicts that incentivize the associated person to put their interest ahead of the customer. Firms must mitigate such conflicts through compensation adjustments, enhanced supervision, or other structural measures.
- **Staff Bulletin on Account Recommendations (2022):** Addressed rollovers, account type recommendations, and the factors to consider when recommending a brokerage vs advisory account. Emphasized that "reasonably available alternatives" includes remaining in the existing arrangement.

### SEC Examination Priorities and Enforcement
SEC Division of Examinations has consistently listed Reg BI as an examination priority since its June 30, 2020 compliance date:

- **Common examination findings:** Inadequate conflict identification, boilerplate disclosures that fail to describe firm-specific conflicts, failure to consider reasonably available alternatives (especially lower-cost share classes), inadequate documentation of the basis for recommendations, insufficient written policies and procedures.
- **Enforcement trends:** Early enforcement actions focused on share class recommendations (recommending higher-cost share classes when lower-cost classes of the same fund were available). More recent actions have addressed failures in conflict mitigation, inadequate Form CRS disclosures, and insufficient rollover documentation.
- **Risk alerts:** The SEC has issued risk alerts highlighting deficiencies in firms' processes for identifying and addressing conflicts, particularly around revenue sharing and proprietary product preferences.

### The "Reasonably Available Alternatives" Requirement in Practice
The care obligation requires considering reasonably available alternatives, but the SEC has clarified this is not a "best in market" standard:

- **Scope:** The firm's own product shelf defines the universe of "reasonably available" alternatives. A firm is not required to evaluate every product in the marketplace, but it must evaluate the alternatives it makes available.
- **Limited product shelf risk:** A firm with a narrow product shelf (e.g., only proprietary products) must still satisfy the care obligation. The SEC has noted that a very limited shelf may make it difficult to demonstrate that recommendations are in the customer's best interest.
- **Documentation:** Firms should document why a recommended product was selected over alternatives, particularly when the recommended product is more expensive or has different risk characteristics. The documentation need not be exhaustive but must be reasonable.
- **Practical approach:** Compare the recommended product against 2-3 reasonably available alternatives on key dimensions: cost, risk, expected return characteristics, liquidity, and suitability for the customer's investment profile.

## Worked Examples

### Example 1: Higher-Cost Share Class Recommendation
**Scenario:** A registered representative at a broker-dealer recommends that a retail customer invest $200,000 in the Class A shares of a large-cap equity mutual fund. Class A shares carry a 5.25% front-end load and a 0.85% annual expense ratio. The same fund offers Class I (institutional) shares with no load and a 0.45% annual expense ratio. The customer qualifies for Class I shares based on the investment amount. The representative receives a higher commission on Class A shares.

**Compliance Issues:**
- **Disclosure Obligation:** The representative must disclose the existence of both share classes, the fee differential, and the compensation conflict (higher commission on Class A).
- **Care Obligation:** The representative must have a reasonable basis for recommending Class A over Class I. Since the customer qualifies for Class I and the funds are identical in investment strategy and performance (before fees), recommending Class A lacks a reasonable basis. The "reasonably available alternatives" analysis clearly favors Class I.
- **Conflict of Interest Obligation:** The higher commission on Class A is a material conflict that must be identified, disclosed, and mitigated. Recommending the higher-cost share class when the lower-cost class is available and the customer qualifies is a conflict that disclosure alone does not cure.

**Analysis:** This recommendation likely violates Reg BI. The SEC's early enforcement actions specifically targeted this pattern. The representative cannot demonstrate that Class A is in the customer's best interest when an identical, lower-cost alternative is available. The firm's compliance program should include automated checks that flag recommendations of higher-cost share classes when a customer qualifies for a lower-cost class of the same fund. The firm's supervisory procedures should require pre-approval or enhanced review for any recommendation where a lower-cost alternative exists.

### Example 2: 401(k) to IRA Rollover Without Documenting Alternatives
**Scenario:** A registered representative recommends that a recently retired customer, age 62, roll $850,000 from her former employer's 401(k) plan into an IRA at the representative's firm. The representative documents the customer's risk tolerance and investment objectives but does not compare the 401(k) plan's investment options, fees, or features against the proposed IRA. The 401(k) plan offers low-cost index funds with expense ratios of 0.02-0.05% and plan administrative fees of $40/year. The proposed IRA would invest in mutual funds with expense ratios of 0.50-0.85%, plus a $95/year custodial fee.

**Compliance Issues:**
- **Care Obligation:** The representative failed to consider reasonably available alternatives. Under the SEC Staff Bulletin on Account Recommendations, the representative must evaluate: (1) staying in the 401(k) plan, (2) rolling to the new employer's plan (if applicable), (3) rolling to the IRA, and (4) taking a distribution. The representative did not document any comparison of fees, investment options, or plan features.
- **Disclosure Obligation:** The representative must disclose the material fee differential and how the firm and representative are compensated on the IRA assets.
- **Specific factors not considered:** The 401(k) plan's ERISA creditor protections (broader than IRA protections), the ability to take penalty-free withdrawals from a 401(k) after separation from service at age 55+ (not available from an IRA until 59 1/2), the plan's institutional-class pricing, and the plan's potential loan provisions.

**Analysis:** This recommendation likely violates Reg BI's care obligation. The cost differential alone is significant: on $850,000, the annual fee difference is approximately $4,000-$7,000 per year. The representative must document a reasonable basis for why the IRA is in the customer's best interest despite the higher costs. Valid reasons might include: substantially broader investment options, access to financial planning services, consolidation benefits, or specific tax planning strategies not available in the plan. But these reasons must be documented and must be reasonable given the customer's specific circumstances. The absence of any alternatives analysis is a clear deficiency.

### Example 3: Dual-Registrant Failing to Clarify Capacity
**Scenario:** A financial professional is registered as both a broker-dealer representative and an investment adviser representative at a dually registered firm. The professional meets with a retail customer and recommends moving $500,000 from a fee-based advisory account (1.0% annual advisory fee) into a commission-based brokerage account, where the professional would receive commissions on mutual fund purchases. The professional does not clearly communicate that this transition involves a change in the applicable standard of conduct from the IA fiduciary duty to Reg BI, and does not explain what protections the customer may lose (ongoing monitoring, ongoing fiduciary duty).

**Compliance Issues:**
- **Disclosure Obligation:** The professional must clearly disclose the capacity in which the recommendation is being made. Moving from an advisory to a brokerage relationship is itself an account type recommendation triggering Reg BI. The customer must understand that in a brokerage relationship, the professional has no ongoing duty to monitor the account.
- **Care Obligation:** The professional must demonstrate that the brokerage account is in the customer's best interest. For a customer with $500,000, the comparison must include: total cost of ownership in each account type (advisory fee vs commissions and fund expense ratios), the services provided in each (ongoing monitoring and fiduciary duty vs transaction-based recommendations), and the customer's trading frequency and need for ongoing advice.
- **Conflict of Interest Obligation:** If the professional earns more in total compensation from the brokerage arrangement than the advisory arrangement, this is a material conflict that must be disclosed and mitigated. Even if total compensation is similar, the change in standard of conduct (from fiduciary to Reg BI) is itself a material fact that must be disclosed.

**Analysis:** This recommendation likely violates both the Disclosure and Care obligations. The SEC has specifically warned against "hat-switching" that obscures the applicable standard of conduct. The customer should receive a clear explanation, ideally in writing, of: (1) the current advisory relationship and fiduciary standard, (2) the proposed brokerage relationship and Reg BI standard, (3) the differences in services, costs, and protections, and (4) why the brokerage relationship is in the customer's best interest. The firm's compliance program should require documented approval for any recommendation to move a customer from an advisory to a brokerage relationship.

## Common Pitfalls
- Treating Reg BI as equivalent to the old suitability standard — Reg BI imposes a meaningfully higher standard, particularly on cost considerations and alternatives analysis
- Relying on disclosure alone to satisfy the conflict of interest obligation — disclosure is necessary but not sufficient for conflicts that incentivize placing the firm's interest ahead of the customer's
- Failing to document the basis for recommendations, particularly rollover recommendations and account type recommendations
- Using boilerplate conflict disclosures that describe generic industry conflicts rather than firm-specific and recommendation-specific conflicts
- Not considering "reasonably available alternatives" — particularly lower-cost share classes or staying in an existing arrangement
- Maintaining sales contests, quotas, or time-limited bonuses tied to specific securities or product types (these must be eliminated, not merely disclosed or mitigated)
- Dual-registrants failing to clearly communicate the capacity in which they are acting and the applicable standard of conduct
- Confusing Reg BI with a fiduciary standard — Reg BI is not a fiduciary duty and does not impose ongoing monitoring obligations unless the firm agrees to provide them
- Applying Reg BI to institutional customers — Reg BI only applies to "retail customers" (natural persons using recommendations for personal, family, or household purposes)
- Inadequate supervisory systems that do not flag high-conflict recommendations for enhanced review
- Treating the compliance obligation as a one-time exercise rather than an ongoing requirement to maintain and enforce policies and procedures

## Cross-References
- **investment-suitability** (compliance plugin): FINRA suitability framework that Reg BI replaced and enhanced for retail customers
- **fiduciary-standards** (compliance plugin): IA fiduciary duty under the Advisers Act — the parallel standard for investment advisers
- **conflicts-of-interest** (compliance plugin): Detailed conflict identification, disclosure, and mitigation frameworks applicable across regulatory regimes
- **fee-disclosure** (compliance plugin): Fee transparency requirements that support the Disclosure Obligation
- **advice-standards** (compliance plugin): Broader standards of conduct for financial professionals across BD and IA channels
- **client-disclosures** (compliance plugin): Form CRS requirements and other client-facing disclosure obligations
- **private-placements** (compliance plugin): exempt offering framework and investor-eligibility rules underlying Care Obligation analysis of private placement recommendations


---

## SKILL: regulatory-change-log

- Fuente: `SYasJ/claude-business-skills` → `plugins/risk/skills/regulatory-change-log` (MIT)
- Cuándo usarla: Log a regulatory change the user has identified, with impact questions and an owner, without giving a legal opinion. Use when the user mentions regulatory change, new rule log, compliance change, regulation tracker, or asks for a regulatory change log. Risk and compliance skill by Yasir Jilani.

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'regulatory-change-log' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Regulatory Change Log

Log a regulatory change the user has identified, with impact questions and an owner, without giving a legal opinion.

## When to use this skill

Use this skill when the user:

- regulatory change
- new rule log
- compliance change
- regulation tracker

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

- The source they provided
- The date they believe applies
- Products or processes affected
- The owner

## Workflow


### 1. Step 1

Record the source they gave. Do not invent a citation.
### 2. Step 2

Summarize the change in their words and mark uncertainties.
### 3. List impact questions for counsel or compliance

does it apply, by when, and to which process.
### 4. Step 4

Assign an owner to get those answers.
### 5. Step 5

Do not tell the business to ignore a rule, and do not declare them compliant.
### 6. Step 6

Review the log on a cadence so a noted change does not sit unread.

## Output

Deliver a **regulatory change log**.

- Purpose of this regulatory change log, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a regulatory change log by 30 September 2026. A blog post says a rule changed, and the team wants to mark the company compliant today.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A blog post says a rule changed, and the team wants to mark the company compliant today.

The source they provided: note from Priya Shah, 14 September 2026. No outside report
The date they believe applies: 30 September 2026
Products or processes affected: email to Priya Shah. No written steps after 1 Sep 2026
The owner: Priya Shah, controller
```

### Example outcome

**Regulatory change log**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Sources the blog as unverified, assigns counsel questions, and makes no compliance claim.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The source they provided | note from Priya Shah, 14 September 2026. No outside report | Needs confirmation |
| The date they believe applies | 30 September 2026 | Carried into the draft |
| Products or processes affected | email to Priya Shah. No written steps after 1 Sep 2026 | Carried into the draft |
| The owner | Priya Shah, controller | Needs confirmation |

**How this draft was built**

**1. Record the source they gave. Do not invent a citation**

**2. Summarize the change in their words and mark uncertainties**

**3. List impact questions for counsel or compliance**  
does it apply, by when, and to which process.

**4. Assign an owner to get those answers**

**5. Do not tell the business to ignore a rule, and do not declare them compliant**

**Deliberately not done**
- An invented citation.
- A compliance declaration.
- An instruction to ignore a rule.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- An invented citation
- A compliance declaration
- An instruction to ignore a rule

## Related skills

- `compliance-calendar`
- `outside-counsel-brief`


---

## SKILL: regulatory-reporting

- Fuente: `JoelLewis/finance_skills` → `plugins/compliance/skills/regulatory-reporting` (MIT)
- Cuándo usarla: Guide regulatory filing mechanics and deadlines for investment advisers, broker-dealers, and large traders — which forms to file, where, and by when. Use when the user asks about Form PF filing thresholds, 13F institutional holdings reports, 13H large trader filings, Form ADV amendment filing timing (including the annual updating amendment filed via IARD), FOCUS report preparation, blue sheet requests, CAT reporting infrastructure, or FINRA short interest and TRACE reporting. Also trigger when users mention 'filing deadline calendar', 'do we need to file Form PF', 'crossed the $100M 13F threshold', 'CAT clock synchronization', 'how to respond to a blue sheet request', or 'FOCUS report errors'. (For what the ADV brochure must contain and when it must be delivered to clients, use client-disclosures.)

# Regulatory Reporting

Regulatory status current as of June 2026 — verify effective dates, dollar thresholds, and pending rulemakings against current SEC/FINRA/FinCEN sources before advising.

## Core Concepts

### Form ADV Amendments
Registered investment advisers must keep Form ADV current through two amendment mechanisms:

**Annual updating amendment** — Must be filed within 90 days of the adviser's fiscal year end (Rule 204-1 under the Investment Advisers Act of 1940). The annual amendment requires the adviser to review and update all items on Form ADV Parts 1, 2A, and 2B. The adviser must also deliver or offer to deliver the updated brochure (Part 2A) to existing clients within 120 days of fiscal year end, along with a summary of material changes.

**Other-than-annual amendments (interim/prompt amendments)** — Certain items on Form ADV must be amended promptly when information becomes inaccurate. "Promptly" is generally interpreted as within 30 days of the event, though some changes require faster action. Items requiring prompt amendment include:
- Changes in the adviser's organizational structure, control persons, or ownership (Part 1, Items 1, 2, 3, 7, 10, 11)
- Changes in disciplinary history (Part 1, Item 11, DRPs)
- Changes in the adviser's financial condition that would require disclosure under Part 2A Item 18
- Changes to the brochure (Part 2A) that are material and that clients or prospective clients should know about — including changes to types of advisory services, fee schedules, methods of analysis, risk factors, material conflicts, disciplinary events, or financial condition

**Items that may wait for the annual amendment** — Statistical information (AUM, number of clients), non-material updates to biographical information, and administrative details that do not affect client decision-making.

**Filing via IARD** — All Form ADV amendments are filed electronically through the Investment Adviser Registration Depository (IARD) system. Filing fees apply. State notice filings are typically triggered automatically upon SEC filing for advisers relying on SEC registration.

**State notice filings** — SEC-registered advisers operating in multiple states must make notice filings with each state in which they have a place of business or meet the de minimis threshold. IARD facilitates most state notice filings alongside the SEC filing.

**Form ADV-W (Withdrawal)** — An adviser withdrawing from SEC registration files Form ADV-W via IARD. Partial withdrawal (from specific states) or full withdrawal from SEC registration. A withdrawal filing becomes effective 60 days after filing unless the SEC institutes proceedings. Firms must maintain books and records for the applicable retention periods after withdrawal.

### Form PF (Private Fund Reporting)
SEC Form PF, required under Section 204(b) of the Advisers Act and Rule 204(b)-1, applies to SEC-registered investment advisers that manage one or more private funds. (The dollar thresholds below are set by rule and are not inflation-indexed; unchanged as of 2026.)

**Filing thresholds and frequency:**
- **Large private fund advisers to hedge funds** — advisers with at least $1.5 billion in hedge fund AUM must file quarterly within 60 days of quarter end. They report on each qualifying hedge fund individually.
- **Large private fund advisers to liquidity funds** — advisers with at least $1 billion in combined money market fund and liquidity fund AUM must file quarterly within 15 days of quarter end.
- **Large private fund advisers to private equity funds** — advisers with at least $2 billion in private equity fund AUM must file annually but report more detailed information on each qualifying PE fund.
- **Smaller private fund advisers** — all other SEC-registered advisers with at least $150 million in private fund AUM file annually within 120 days of fiscal year end. They report aggregate information across all advised private funds.

**Content of Form PF filings:** AUM and NAV for each reported fund; borrowings and leverage (gross and net); investor concentration (largest investors as a percentage of NAV); asset class exposure and geographic breakdown; counterparty credit exposure (top counterparties); trading and clearing practices (exchange-traded vs OTC); liquidity of portfolio positions; side pocket and gate usage; performance data; investment strategy classification; use of high-frequency trading strategies.

**2023 Amendments — Current Reporting (effective 2024):** The SEC adopted amendments to Form PF requiring current reporting of certain triggering events:
- **Large hedge fund advisers** must report within 72 hours of: extraordinary investment losses (20% or more of a reporting fund's NAV over a rolling 10-business-day period), significant margin and default events (failure to meet a margin call that exceeds the reporting fund's NAV by 5% or more), counterparty defaults, material changes in prime broker relationships, changes in unencumbered cash falling below a reporting fund's requirement, and operations events (significant disruption to key operations).
- **All Form PF filers for private equity** must report within 60 days of: GP-led secondary transactions, adviser-led fund restructurings, removal of a fund's GP, election to terminate a fund's investment period, and election to terminate a fund.

Filing is through the Private Fund Reporting Depository (PFRD), an electronic filing system operated by FINRA on the IARD infrastructure — Form PF is not filed on EDGAR. A filing fee applies to each initial and update filing.

### 13F Filings (Institutional Holdings)
SEC Rule 13f-1 under Section 13(f) of the Securities Exchange Act of 1934 requires institutional investment managers exercising investment discretion over $100 million or more in 13(f) securities to file Form 13F quarterly. (The $100 million threshold is statutory, set in 1975 and not inflation-indexed; it remains unchanged as of 2026.)

**Who must file:** Any "institutional investment manager" — a broad category that includes investment advisers, banks, insurance companies, broker-dealers, pension funds, and corporations — that exercises investment discretion over the threshold amount. The threshold is measured as of the last trading day of any month in the calendar year. Once crossed, the manager must file for every quarter of that calendar year and the following calendar year.

**What to report:** Long positions in 13(f) securities as of the last day of the calendar quarter. 13(f) securities include: exchange-listed equities and equity-linked securities (common stock, preferred stock, warrants, convertible securities), shares of closed-end funds, certain exchange-traded options (puts and calls), and shares of ETFs. The official list of 13(f) securities is published quarterly by the SEC.

**Required data elements:** CUSIP number, issuer name, class title (e.g., "COM" for common stock), market value (rounded to the nearest thousand dollars), number of shares or principal amount, investment discretion type (sole, shared, or none), voting authority (sole, shared, or none), and the number of shares for each voting authority type.

**Filing deadline:** Within 45 days of calendar quarter end (filed on SEC EDGAR).

**Confidential treatment requests:** Managers may request confidential treatment under Rule 24b-2 for positions where public disclosure would reveal a trading strategy still being implemented (e.g., ongoing accumulation or disposition). The SEC grants confidential treatment on a case-by-case basis and requires a showing that disclosure would likely cause competitive harm. Historically, the SEC has narrowed the grounds for confidential treatment.

**Common errors and consequences:** Late filings result in public notice and may trigger SEC enforcement. Reporting errors in CUSIPs, share counts, or market values can mislead market participants. Firms must verify 13F data against custodian records and ensure consistent treatment of jointly managed accounts. The SEC has brought enforcement actions for material misstatements on Form 13F.

### 13H Filings (Large Trader Reporting)
SEC Rule 13h-1 under Section 13(h) of the Exchange Act requires "large traders" to identify themselves to the SEC and receive a Large Trader Identification Number (LTID).

**Large trader thresholds:** A person (including a firm) is a "large trader" if their transactions in NMS securities equal or exceed:
- **2 million shares or $20 million in fair market value** during any single calendar day, or
- **20 million shares or $200 million in fair market value** during any calendar month.

(The 13H identifying-activity thresholds are fixed by Rule 13h-1 and are not inflation-indexed; unchanged as of 2026.)

Transactions across all accounts over which the person exercises investment discretion are aggregated. The thresholds apply to both purchases and sales.

**Form 13H filing requirements:**
- **Initial filing** — must be filed promptly after first meeting the threshold. Filed electronically on SEC EDGAR.
- **Annual filing** — within 45 days after the end of each full calendar year following initial filing.
- **Amended filings** — filed promptly upon the occurrence of a material change to previously reported information (e.g., change in organizational structure, new broker-dealer relationships, change in control).
- **Inactive status** — a large trader that has not met the threshold during the previous full calendar year may file for inactive status. Must reactivate if the threshold is subsequently met.

**LTID assignment and use:** Upon filing, the SEC assigns an LTID. The large trader must provide the LTID to each broker-dealer through which it trades. The LTID is attached to the large trader's accounts at each broker-dealer.

**Broker-dealer obligations:** Broker-dealers carrying accounts for large traders must: (a) maintain records of transactions effected through large trader accounts, (b) report large trader transaction data to the SEC upon request (historically via Electronic Blue Sheets, now increasingly through CAT), and (c) monitor for customers who may meet the large trader definition but have not self-identified.

### FOCUS Reports
The Financial and Operational Combined Uniform Single (FOCUS) report is the primary financial reporting form for broker-dealers, required under SEC Rule 17a-5 and filed through FINRA's systems.

**Filing frequency and form versions:**
- **Part II** — filed quarterly by introducing broker-dealers (firms that do not carry customer accounts or clear transactions). Due within 17 business days of quarter end.
- **Part IIA** — filed monthly by carrying/clearing broker-dealers (firms that hold customer funds or securities, clear transactions, or carry customer accounts). Due within 17 business days of month end.
- **Part IIC** — filed by OTC derivatives dealers.

**Content of FOCUS reports:**
- **Statement of financial condition** (balance sheet) — assets, liabilities, ownership equity
- **Net capital computation** (SEC Rule 15c3-1) — the firm's calculation of net capital, showing liquid assets minus liabilities and haircuts. The net capital rule requires broker-dealers to maintain a minimum level of liquid assets to protect customer funds and securities.
- **Aggregate indebtedness computation** — ratio of aggregate indebtedness to net capital (must not exceed 15:1 for firms using the basic method)
- **Customer reserve computation** (SEC Rule 15c3-3) — the computation determining whether the firm must deposit funds into a special reserve bank account for the exclusive benefit of customers
- **Income statement** and revenue detail
- **Operational data** — possession or control of customer fully paid and excess margin securities

**Filing and regulatory oversight:** FOCUS reports are filed with FINRA as the firm's designated examining authority (DEA). FINRA reviews filings for accuracy, timeliness, and compliance with net capital and customer protection rules. FOCUS data is shared with the SEC. Late filing, inaccurate filings, or filings showing net capital deficiencies trigger heightened regulatory scrutiny.

**Consequences of late or deficient filings:** FINRA may impose fines, censure, or suspend a firm for persistent late filings. A FOCUS report showing a net capital deficiency triggers immediate obligations under SEC Rule 17a-11 (discussed in the worked examples below).

### Blue Sheets / EBS (Electronic Blue Sheets)
SEC Rule 17a-25 requires broker-dealers to submit, upon SEC request, standardized electronic trading records for specified securities and time periods.

**When requested:** Blue sheet requests typically arise during SEC investigations into potential insider trading, market manipulation, or other trading violations. The SEC's Division of Enforcement issues blue sheet requests identifying the securities, time period, and type of trading data required.

**Data elements:** Customer identity (name, address, SSN/TIN), account number, transaction date and time, security identifier (CUSIP/symbol), buy/sell/short sale indicator, quantity, price, executing broker, clearing broker, and the capacity in which the firm acted (principal or agent).

**Timeliness:** Broker-dealers must respond within the timeframe specified in the request, typically 10 business days. Firms should have systems capable of extracting and formatting blue sheet data promptly.

**Relationship to CAT:** The Consolidated Audit Trail (CAT) supplies much of the same information for routine regulatory surveillance of NMS equities and listed options. However, as of June 2026 no retirement timeline for the Electronic Blue Sheet system has been announced: data-attribute gaps between EBS and CAT remain, CAT does not cover fixed income, and the SEC continues to issue blue sheet requests in enforcement investigations (including for periods predating CAT). Plan for both systems to coexist, and verify current status before decommissioning any EBS capability.

**Enforcement for non-compliance:** Failure to respond accurately or timely to blue sheet requests can result in SEC enforcement action. The SEC has brought cases against firms for submitting inaccurate blue sheet data, including incorrect customer identification or missing transactions.

### CAT (Consolidated Audit Trail)
SEC Rule 613 mandated the creation of the Consolidated Audit Trail, the most comprehensive order tracking system in U.S. securities markets. The CAT Plan was adopted in 2016, and reporting obligations have been phased in for equities and options.

**Who must report:** All broker-dealers that are members of a national securities exchange or FINRA ("Industry Members") and all national securities exchanges ("Plan Participants") must report to CAT. This includes introducing brokers, clearing firms, market makers, ATSs, and exchange members.

**What is reported:** CAT captures every reportable event in the lifecycle of an order for NMS equities and listed options:
- **Order origination** — receipt of a new order from a customer or another broker-dealer, including order terms (side, quantity, price, time-in-force, order type, special handling instructions)
- **Order routing** — transmission of an order to another broker-dealer, exchange, or ATS
- **Order modification** — changes to order terms (price, quantity, time-in-force)
- **Order cancellation** — cancellation of a pending order
- **Order execution** — full or partial fill, including execution price and quantity
- **Allocation** — post-trade allocation to sub-accounts (for institutional orders)

**Customer and Account Identifying Information (CAIS):** Industry Members must submit CAIS data linking each account to its customer(s). CAIS includes: customer name, address, date of birth (for individuals), SSN/EIN, and account information. CAIS is submitted through a separate reporting channel and must be kept current.

**Clock synchronization requirements:** Accurate timestamps are essential for order lifecycle tracking. SEC Rule 613 and the CAT NMS Plan require:
- **Exchanges and ATSs** — clocks must be synchronized to within 50 milliseconds of the National Institute of Standards and Technology (NIST) atomic clock
- **Broker-dealers (Industry Members)** — clocks must be synchronized to within 1 second of the NIST atomic clock for manual order events, and within 50 milliseconds for electronic order events
- Firms must document their clock synchronization procedures, test compliance regularly, and maintain records of clock drift and synchronization corrections

**Error correction obligations:** CAT reporting firms must monitor their submissions for errors flagged by the CAT system. The CAT system validates submissions and generates error reports. Firms must:
- Repair errors within the timeframes specified by the CAT NMS Plan (generally T+3 for most errors)
- Monitor error rates — the CAT NMS Plan establishes error rate thresholds, and firms with persistently high error rates face regulatory scrutiny
- Maintain records of error identification, root cause analysis, and correction

**Implementation timeline:** Large Industry Members began reporting equities in April 2020 and options in 2022. Small Industry Members followed shortly thereafter. The full lifecycle reporting, including allocations and CAIS data, has been phased in incrementally. Firms should consult the FINRA CAT website and the CAT NMS Plan Processor (FINRA CAT, LLC) for current reporting specifications and implementation deadlines.

**Retirement of OATS:** FINRA's Order Audit Trail System (OATS), which previously served as the primary order tracking system for FINRA member firms, was retired on September 1, 2020, following the implementation of CAT reporting for equities.

### SAR and CTR Filing Mechanics
While the substantive AML compliance framework is covered in the anti-money-laundering skill, the reporting mechanics are a regulatory reporting obligation:

**FinCEN BSA E-Filing System** — SARs (FinCEN Form 111) and CTRs (FinCEN Form 112) are filed electronically through FinCEN's BSA E-Filing System. Firms must register for BSA E-Filing, designate authorized users, and maintain access credentials securely.

**SAR filing deadlines:**
- File within 30 calendar days of the date the suspicious activity is first detected by the firm
- If no suspect is identified at the time of detection, the deadline extends to 60 calendar days, but the firm must make a reasonable effort to identify the suspect before filing
- Continuing SARs for ongoing suspicious activity must be filed at least every 90 days
- SAR amendments may be filed to correct or supplement previously filed SARs

**CTR filing deadlines:**
- File within 15 calendar days of the cash transaction exceeding $10,000 (or aggregated transactions exceeding $10,000 in a single business day)

**SAR confidentiality** — 31 U.S.C. Section 5318(g)(2) prohibits any financial institution, or any officer, director, employee, or agent thereof, from disclosing to the person involved in the transaction (or any other person) that a SAR has been or will be filed. This tipping-off prohibition extends to responses to subpoenas, discovery requests, or other legal process — SARs themselves are not producible, although the underlying facts are not privileged.

**Recordkeeping for filed reports:**
- SARs — supporting documentation (transaction records, analyst notes, investigation files, SAR narrative drafts) must be retained for 5 years from the date of filing (31 CFR Section 1010.320(d))
- CTRs — records must be retained for 5 years from the date of the report (31 CFR Section 1010.306(a))
- All filed SARs and CTRs must be maintained in a format that allows retrieval upon FinCEN or law enforcement request

### FINRA Reporting Obligations
Beyond FOCUS reports and CAT, FINRA member firms have several additional reporting obligations:

**Short interest reporting (FINRA Rule 4560)** — Member firms must report short positions in all equity securities (customer and proprietary) as of settlement on the designated reporting date, which occurs twice monthly (approximately the 15th and last business day of each month). Reports are due to FINRA by 6:00 p.m. ET on the second business day after the reporting settlement date. FINRA publishes aggregate short interest data, and individual firm reports are used for regulatory surveillance.

**TRACE (Trade Reporting and Compliance Engine)** — FINRA-operated system for reporting OTC transactions in eligible fixed-income securities, including corporate bonds, agency debentures, asset-backed securities, and certain other debt instruments. Reporting is required within 15 minutes of execution for most transactions (FINRA Rules 6710-6770). TRACE-eligible securities have expanded over time to include Treasury securities (effective 2020 under FINRA Rule 6730). Late TRACE reports result in regulatory action.

**Trade reporting to FINRA-operated facilities** — For OTC equity transactions, member firms must report trades to the appropriate FINRA facility:
- **ORF (OTC Reporting Facility)** — for OTC equity securities not listed on an exchange
- **TRF (Trade Reporting Facility)** — for NMS stocks (exchange-listed equities traded OTC). Multiple TRFs exist (FINRA/Nasdaq TRF, FINRA/NYSE TRF)
- **ADF (Alternative Display Facility)** — for firms that choose to display quotations through the ADF

Trade reports must be submitted within 10 seconds of execution during market hours.

**Regulatory filings and notifications** — FINRA members must promptly notify FINRA of certain events under FINRA Rule 4530, including: violations of securities laws, written customer complaints, regulatory actions by other agencies, criminal charges against associated persons, and civil litigation related to the firm's investment banking or securities business. Annual statistical reports of customer complaints are also required.

### Regulatory Reporting Calendar
For the consolidated filing calendar (every filing, filer, frequency, deadline, and venue in one table), load `references/filing-calendar.md` when building a compliance calendar or checking a specific deadline.

## Worked Examples

### Example 1: Newly registered IA crossing AUM threshold and triggering Form PF obligations
**Scenario:** An investment advisory firm has been state-registered for three years, managing $120 million in a mix of separate accounts and a single private fund (a hedge fund with $50 million in AUM). In Q2 2025, the firm's total AUM crosses $150 million, and its private fund AUM remains at $50 million. The firm files for SEC registration, which becomes effective in September 2025. The firm has a December 31 fiscal year end.
**Compliance Issues:**
- Crossing $100 million in AUM (for advisers with no state exemption) triggers the obligation to register with the SEC under Section 203A of the Advisers Act, with narrow exceptions for mid-sized advisers subject to examination by their home state.
- SEC registration triggers Form ADV filing via IARD — the firm must file a complete Form ADV (Parts 1, 2A, 2B, and Form CRS if not previously filed) at the time of registration.
- Managing a private fund with at least $150 million in total private fund AUM triggers Form PF filing as a "smaller private fund adviser." Since the firm has under $1.5 billion in hedge fund AUM, it is not a large private fund adviser and files annually.
- The firm's first Form PF is due within 120 days of its first fiscal year end after becoming obligated — meaning by April 30, 2026, for the fiscal year ending December 31, 2025.
- The firm must also transition state notice filings to the SEC IARD system and ensure it withdraws from any state registrations that are no longer required.
**Analysis:**
The firm should establish the following operational timeline: (1) File Form ADV with the SEC via IARD concurrent with the registration application, ensuring all items are completed accurately, including Schedule D for the private fund. (2) File Form CRS with the SEC and deliver to all existing clients. (3) Establish access to the FINRA-operated Private Fund Reporting Depository (PFRD) for Form PF filing. (4) Assign compliance personnel responsible for Form PF preparation and identify data sources — NAV, leverage, asset class exposure, investor concentration, counterparty exposure — that must be compiled from the fund administrator, prime broker, and internal records. (5) Conduct a dry run of the Form PF filing process before the first filing deadline to identify data gaps. (6) Set the compliance calendar: first annual Form PF due by April 30, 2026; first annual ADV updating amendment due by March 31, 2026; Form CRS must be reviewed and updated at least annually. (7) Monitor whether hedge fund AUM approaches $1.5 billion, which would trigger quarterly filing and significantly more detailed reporting. The firm should budget for the operational burden of Form PF — smaller private fund advisers typically spend 20-40 hours on each annual filing, and the data aggregation process requires coordination across multiple service providers.

### Example 2: Broker-dealer FOCUS report reveals net capital deficiency
**Scenario:** A carrying broker-dealer files its monthly FOCUS Part IIA report for January 2026. The net capital computation shows that the firm's net capital has fallen below its minimum required net capital by $1.2 million, driven by unexpected trading losses in a proprietary account and an increase in customer debit balances that raised the firm's required net capital under the alternative method (SEC Rule 15c3-1(a)(1)(ii)). The firm's minimum requirement is $250,000, but its required net capital under the alternative method is $4.5 million, and actual net capital is $3.3 million.
**Compliance Issues:**
- SEC Rule 17a-11 imposes immediate notification obligations when a broker-dealer's net capital falls below its minimum requirement. The firm must notify the SEC, its designated examining authority (FINRA), and its designated self-regulatory organization by telegraph or facsimile (in practice, electronic notice) within 24 hours of the discovery.
- Under Rule 17a-11(b), a broker-dealer whose net capital declines below 120% of its minimum requirement must also provide early warning notice to the SEC and FINRA.
- Under Rule 15c3-1(e), a broker-dealer in net capital deficiency may not conduct securities business (i.e., cannot execute customer transactions, accept new customer accounts, or transfer customer funds or securities) until the deficiency is cured, unless granted a temporary exemption by the SEC.
- The firm must also file a notice under Rule 17a-11(d) if it fails to make a required customer reserve deposit under Rule 15c3-3.
- FINRA will likely impose heightened supervision, require a corrective action plan, and may conduct an accelerated examination.
**Analysis:**
The firm must take the following immediate steps: (1) Notify the SEC (Division of Trading and Markets), FINRA (Member Supervision), and the firm's DSRO within 24 hours of computing the deficiency. The notice must state the amount of the deficiency, the cause, and the firm's plan for remediation. (2) Cease conducting securities business until the deficiency is cured — this means suspending customer transactions, which will require notifying customers and potentially arranging for an emergency carrying agreement with another broker-dealer. (3) Compute the customer reserve formula to determine whether customer funds are at risk and whether an extraordinary reserve deposit is needed. (4) Prepare and file a supplemental FOCUS report showing the deficiency and the corrective action plan. (5) Identify the path to cure: options include capital contribution from the firm's parent or owners, liquidation of proprietary positions, reduction of customer debit balances, or a combination. (6) Once the deficiency is cured, file notice with the SEC and FINRA demonstrating that net capital is restored above the minimum (ideally above 120% to exit early warning). (7) Conduct a root cause analysis and implement controls to prevent recurrence — this may include revised proprietary trading limits, enhanced margin monitoring, or increased capital buffers. A net capital deficiency is one of the most serious regulatory events for a broker-dealer. FINRA enforcement may include fines under Rules 4110 and 4120, and repeated deficiencies can lead to suspension or expulsion.

### Example 3: Blue sheet request reveals systematic CAT reporting errors
**Scenario:** A mid-sized broker-dealer receives a blue sheet request from the SEC's Division of Enforcement seeking transaction data for a particular security over a 90-day period, related to a suspected insider trading investigation. While compiling the blue sheet response, the firm's compliance team discovers that its CAT reporting system has been systematically misidentifying customers for approximately 6 months due to a software mapping error. The error caused roughly 15,000 order events to be submitted to CAT with incorrect Customer Account IDs, linking orders to the wrong customer accounts in CAIS. The blue sheet data, compiled independently from the firm's order management system, is accurate.
**Compliance Issues:**
- The blue sheet response must be accurate and complete within the SEC's stated deadline. Submitting inaccurate blue sheet data is itself a violation of SEC Rule 17a-25 and can result in separate enforcement action.
- The 6-month CAT reporting error constitutes a violation of Rule 613 and the CAT NMS Plan. Systematic errors affecting 15,000 events over 6 months will significantly exceed normal error rate thresholds and will attract regulatory attention from FINRA CAT, LLC (the plan processor) and potentially from the SEC.
- The firm has an obligation to correct CAT errors within the timeframes specified by the CAT NMS Plan. For errors this widespread, the firm must develop a comprehensive remediation plan.
- The overlap between the blue sheet investigation and the CAT error creates additional regulatory exposure — if the incorrect CAT data impeded surveillance of the suspected insider trading, the consequences could be severe.
- Depending on the nature of the customer misidentification, there may also be implications for CAIS data integrity, which is central to linking orders to customers for surveillance purposes.
**Analysis:**
The firm must address three parallel workstreams: (1) **Blue sheet response** — prioritize compiling an accurate and complete response from source systems (not from CAT data). Verify customer identification against account records and the order management system. Submit the blue sheet data within the SEC's specified deadline. If additional time is needed due to the volume or complexity, request an extension from the Division of Enforcement promptly. (2) **CAT error remediation** — conduct a root cause analysis of the software mapping error. Identify all affected order events over the 6-month period. Develop a remediation file to correct the Customer Account IDs for all 15,000+ events. Submit corrected data to FINRA CAT. Notify FINRA's CAT Helpdesk and the firm's designated FINRA examination contact of the systematic error and the remediation plan. Document the root cause, the scope of the impact, the timeline of error detection and correction, and the controls implemented to prevent recurrence. (3) **Regulatory exposure management** — the firm should consider self-reporting the CAT error to FINRA and the SEC proactively, as self-disclosure is a mitigating factor in enforcement proceedings. The firm should assess whether the incorrect customer mapping could have masked any suspicious trading patterns that should have been visible to regulators through CAT surveillance. If so, the firm should include that analysis in its self-disclosure. Legal counsel should be engaged to evaluate the firm's exposure and advise on the self-reporting strategy. The firm should also review its broader technology change management and quality assurance processes for CAT reporting — a 6-month undetected error suggests inadequate reconciliation controls between the firm's order management system and its CAT reporting submissions. Implementing daily reconciliation of CAT-submitted data against source systems is an industry best practice that would have detected this error much sooner.

## Common Pitfalls
- Missing prompt Form ADV amendment deadlines by treating all changes as annual-only updates — material changes to advisory services, fees, disciplinary events, or organizational structure require prompt interim filing
- Failing to monitor private fund AUM against Form PF filing thresholds as assets grow, resulting in missed filing obligations
- Filing 13F reports with incorrect share counts or market values because of failures to reconcile against custodian records or to account for corporate actions (splits, mergers, spin-offs)
- Not updating Form 13H promptly when broker-dealer relationships change or organizational structure is modified
- Treating FOCUS report preparation as a back-office function without CCO review, leading to errors in net capital computation or customer reserve calculation
- Delaying response to SEC blue sheet requests or submitting data extracted from a single system without cross-verification against independent records
- Failing to implement daily CAT data reconciliation between the firm's order management system and CAT submissions, allowing errors to accumulate undetected
- Not maintaining clock synchronization compliance — broker-dealer clocks drifting beyond the 1-second (or 50-millisecond for electronic events) tolerance without detection or correction
- Treating the 72-hour current reporting requirement under the 2023 Form PF amendments as a best-efforts obligation rather than a strict deadline
- Submitting TRACE reports outside the 15-minute window and failing to mark late reports as such, compounding the violation
- Not establishing a regulatory filing calendar with automated reminders, leading to missed deadlines across multiple overlapping filing obligations
- Failing to retain SAR and CTR supporting documentation for the full 5-year period, or commingling SAR files with general compliance records in a way that risks inadvertent disclosure
- Neglecting to file FINRA Rule 4530 event notifications within 30 calendar days, particularly for written customer complaints and associated person disciplinary events

## Cross-References
- **anti-money-laundering** (compliance plugin): SAR and CTR filing mechanics are regulatory reporting obligations; the substantive AML framework (detection, investigation, escalation) feeds into the reporting workflow covered here
- **client-disclosures** (compliance plugin): Form ADV amendments trigger delivery obligations to existing clients — the disclosure skill covers what must be delivered and when, while this skill covers the filing mechanics
- **books-and-records** (compliance plugin): Records retention requirements underpin all regulatory reporting; accurate books and records are the source data for FOCUS reports, 13F filings, Form PF, and CAT submissions
- **know-your-customer** (compliance plugin): CAT CAIS data and blue sheet responses require accurate customer identification information sourced from the firm's KYC and CIP processes
- **fee-disclosure** (compliance plugin): Form ADV amendments reflecting changes to fee schedules are both a filing obligation (covered here) and a fee disclosure requirement (covered in fee-disclosure)

### Referencia: references/filing-calendar.md

# Regulatory Reporting Calendar

Regulatory status current as of June 2026 — verify deadlines and filing venues against current SEC/FINRA/FinCEN sources before advising.

| Filing | Who Must File | Frequency | Deadline | Filed With |
|--------|--------------|-----------|----------|------------|
| Form ADV (annual) | SEC-registered IAs | Annually | 90 days after fiscal year end | SEC via IARD |
| Form ADV (interim) | SEC-registered IAs | As needed | Promptly (within 30 days of material change) | SEC via IARD |
| Form PF (small filer) | IAs with $150M+ private fund AUM | Annually | 120 days after fiscal year end | SEC via PFRD (FINRA-operated) |
| Form PF (large hedge) | IAs with $1.5B+ hedge fund AUM | Quarterly | 60 days after quarter end | SEC via PFRD (FINRA-operated) |
| Form PF (large liquidity) | IAs with $1B+ liquidity fund AUM | Quarterly | 15 days after quarter end | SEC via PFRD (FINRA-operated) |
| Form PF (large PE) | IAs with $2B+ PE fund AUM | Annually | 120 days after fiscal year end | SEC via PFRD (FINRA-operated) |
| Form PF (current report) | Large hedge fund advisers | Event-driven | 72 hours after triggering event | SEC via PFRD (FINRA-operated) |
| Form 13F | Managers with $100M+ in 13(f) securities | Quarterly | 45 days after quarter end | SEC via EDGAR |
| Form 13H (initial) | Large traders | Once | Promptly after threshold is met | SEC via EDGAR |
| Form 13H (annual) | Large traders | Annually | 45 days after calendar year end | SEC via EDGAR |
| FOCUS Part II | Introducing BDs | Quarterly | 17 business days after quarter end | FINRA |
| FOCUS Part IIA | Carrying/clearing BDs | Monthly | 17 business days after month end | FINRA |
| CAT (equities/options) | BD members, exchanges | Daily | 8:00 a.m. ET on T+1 | FINRA CAT |
| CAIS (customer data) | BD members | Ongoing | Per CAT NMS Plan schedule | FINRA CAT |
| Short interest | FINRA members | Semi-monthly | 6:00 p.m. ET, 2nd business day after settlement date | FINRA |
| TRACE (fixed income) | FINRA members | Per transaction | Within 15 minutes of execution | FINRA |
| OTC equity trade reports | FINRA members | Per transaction | Within 10 seconds of execution | FINRA (TRF/ORF/ADF) |
| SARs | BDs, banks, covered IAs (adviser coverage delayed to 2028 — verify) | Event-driven | 30 days after detection (60 if no suspect) | FinCEN via BSA E-Filing |
| CTRs | BDs, banks | Event-driven | 15 days after transaction | FinCEN via BSA E-Filing |
| FINRA Rule 4530 | FINRA members | Event-driven | 30 calendar days of the event | FINRA |


---

## SKILL: regulatory-reporting

- Fuente: `agiprolabs/claude-trading-skills` → `skills/regulatory-reporting` (MIT)
- Cuándo usarla: [STUB] Regulatory report generation including IRS Form 8949, Schedule D, FinCEN FBAR, and state-specific crypto reporting requirements
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/regulatory-reporting/` (form_8949_generator.py)

# Regulatory Reporting

> **STATUS: STUB** — This skill outlines planned capabilities for crypto tax and regulatory reporting. All generated output must be reviewed by a qualified tax professional before filing. Nothing in this skill constitutes tax or legal advice.

## Overview

Track and generate required regulatory reports for cryptocurrency trading activity. Covers U.S. federal forms (IRS Form 8949, Schedule D), FinCEN foreign account reporting (FBAR), state-specific crypto obligations, large-transaction flagging, and deadline tracking.

Crypto tax reporting is complex and evolving. Rules change frequently, cost-basis methods vary by jurisdiction, and DeFi activities (swaps, LP positions, airdrops, staking rewards) have ambiguous treatment under current guidance. This skill provides a structured framework for organizing trade data into the formats regulators expect — but a tax professional must validate every filing.

## Disclaimer

> **WARNING**: This skill is for informational and educational purposes only. It does NOT constitute tax, legal, or financial advice. Cryptocurrency tax law is complex, jurisdiction-specific, and rapidly evolving. You MUST consult a qualified tax professional (CPA, EA, or tax attorney with crypto expertise) before relying on any output from this skill for actual tax filings. Errors in tax reporting can result in penalties, interest, and legal consequences. The authors accept no liability for any use of this material.

## Current Status

This is a **STUB** skill. The code and references provided are starting points that demonstrate data structures and basic calculations. They have NOT been validated against current IRS guidance or any state tax authority requirements.

### What Exists Now

- Basic Form 8949 line-item generation from trade data (see `scripts/form_8949_generator.py`)
- Regulatory requirements overview (see `references/planned_features.md`)
- Demo mode with sample trade data

### What Is Planned

- Complete IRS Form 8949 and Schedule D PDF generation
- FinCEN FBAR generation when foreign exchange accounts exceed $10,000
- State-specific reporting requirement detection and templates
- Reporting threshold tracking and deadline calendar
- Large transaction flagging ($10,000+ cash-equivalent transactions)
- Foreign account reporting requirements (FATCA Form 8938)
- Wash sale detection and adjustment (where applicable)
- Cost-basis method selection (FIFO, LIFO, Specific ID, HIFO)
- DeFi-specific event classification (swaps, LP entry/exit, staking, airdrops)
- Actual IRS-compatible CSV/PDF form data output

## Prerequisites

```bash
# No external dependencies for the demo script
python scripts/form_8949_generator.py --demo
```

For a production implementation, the following would be needed:

```bash
uv pip install pandas reportlab  # PDF generation
```

## Key Concepts

### IRS Form 8949 — Sales and Dispositions of Capital Assets

Form 8949 reports each individual sale or disposition of a capital asset. For crypto, every trade, swap, or spending event is a taxable disposition. Key fields:

| Column | Description |
|--------|-------------|
| (a) | Description of property (e.g., "2.5 BTC") |
| (b) | Date acquired |
| (c) | Date sold or disposed of |
| (d) | Proceeds (sale price in USD) |
| (e) | Cost or other basis |
| (f) | Adjustment code (e.g., W for wash sale) |
| (g) | Adjustment amount |
| (h) | Gain or loss (d minus e, adjusted by g) |

Transactions are split into **Part I** (short-term, held one year or less) and **Part II** (long-term, held more than one year).

### Schedule D — Capital Gains and Losses

Schedule D aggregates the totals from Form 8949:
- Line 1b/8b: Totals from Form 8949 Part I / Part II (basis reported to IRS)
- Line 1c/8c: Totals where basis was NOT reported to IRS
- Line 7/15: Net short-term / long-term capital gain or loss
- Line 16: Combined net gain or loss

### FinCEN FBAR (FinCEN Form 114)

Required when the aggregate value of foreign financial accounts exceeds $10,000 at any point during the calendar year. Crypto held on foreign exchanges (e.g., Binance for non-U.S. entities) may trigger this requirement — though IRS guidance on whether crypto accounts are "foreign financial accounts" remains evolving.

- **Filing deadline**: April 15 (automatic extension to October 15)
- **Penalty for non-filing**: Up to $12,500 per non-willful violation; up to $100,000 or 50% of account balance for willful violations

### Large Transaction Reporting

Businesses receiving $10,000+ in cash (which may include crypto under recent guidance) must file IRS Form 8300 within 15 days. Individual traders generally do not file Form 8300, but exchanges may report large transactions.

## Quick Start

```python
"""Generate Form 8949 line items from trade history."""
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

@dataclass
class Trade:
    asset: str
    quantity: Decimal
    date_acquired: date
    date_sold: date
    proceeds_usd: Decimal
    cost_basis_usd: Decimal

def classify_holding_period(trade: Trade) -> str:
    """Return 'short-term' or 'long-term' based on holding period."""
    holding_days = (trade.date_sold - trade.date_acquired).days
    return "short-term" if holding_days <= 365 else "long-term"

def compute_gain_loss(trade: Trade) -> Decimal:
    """Compute capital gain or loss for a single trade."""
    return trade.proceeds_usd - trade.cost_basis_usd

# Example
trade = Trade(
    asset="SOL",
    quantity=Decimal("10"),
    date_acquired=date(2025, 1, 15),
    date_sold=date(2025, 8, 20),
    proceeds_usd=Decimal("2500.00"),
    cost_basis_usd=Decimal("1800.00"),
)
gain = compute_gain_loss(trade)
period = classify_holding_period(trade)
print(f"{trade.asset}: {period} gain of ${gain}")
# SOL: short-term gain of $700.00
```

## Use Cases

1. **End-of-year tax preparation** — Export trade history from exchanges, generate Form 8949 line items, calculate Schedule D totals, and hand the organized data to your tax professional.

2. **Quarterly estimated tax tracking** — Monitor cumulative realized gains throughout the year to estimate quarterly tax payments (IRS Form 1040-ES).

3. **FBAR threshold monitoring** — Track aggregate balances across foreign exchange accounts to determine whether FBAR filing is required.

4. **Audit preparation** — Maintain organized records of all dispositions with cost-basis documentation in case of an IRS inquiry.

5. **Multi-state filing** — Identify state-specific crypto reporting obligations when trading from states with additional requirements.

## Files

### References
- `references/planned_features.md` — Regulatory requirements overview, Form 8949/Schedule D field descriptions, FBAR thresholds, state requirements summary, and reporting deadlines

### Scripts
- `scripts/form_8949_generator.py` — Basic Form 8949 line-item generator from trade data with `--demo` mode; no external dependencies

## Limitations

- **Not legal or tax advice.** This is a software tool, not a tax professional.
- **U.S.-focused.** International tax obligations are not covered.
- **Evolving rules.** Crypto tax guidance changes frequently; this skill may not reflect the latest IRS notices or rulings.
- **No DeFi classification yet.** Complex DeFi events (LP positions, yield farming, rebasing tokens) are not yet handled.
- **No wash sale certainty.** Whether wash sale rules apply to crypto is unsettled; the skill flags potential wash sales but cannot make definitive determinations.
- **Cost-basis methods limited.** Only FIFO is implemented in the demo; LIFO, HIFO, and Specific ID are planned.

## Reporting Deadlines (U.S. Federal)

| Form | Deadline | Extension |
|------|----------|-----------|
| Form 8949 / Schedule D | April 15 | October 15 (with Form 4868) |
| FinCEN FBAR (Form 114) | April 15 | October 15 (automatic) |
| Form 8300 | 15 days after transaction | None |
| FATCA Form 8938 | With tax return | With tax return extension |
| 1040-ES (quarterly) | Apr 15, Jun 15, Sep 15, Jan 15 | None |

## Contributing

This is a stub skill with significant room for expansion. Contributions welcome in these areas:

- Additional cost-basis methods (LIFO, HIFO, Specific ID)
- DeFi event classification (LP entry/exit, staking, airdrops, bridging)
- State-specific requirement databases
- Wash sale detection algorithms
- PDF form generation (IRS-compatible output)
- International tax jurisdiction support
- Integration with exchange API export formats

All contributions must include appropriate disclaimers and must not provide specific tax advice. See the project CLAUDE.md for contribution guidelines.

## Related Skills

- `portfolio-analytics` — Portfolio performance tracking that feeds into tax reporting
- `trade-journal` — Trade logging that can serve as source data for Form 8949

### Referencia: references/planned_features.md

# Regulatory Reporting — Planned Features & Requirements Overview

> **DISCLAIMER**: This document is for informational purposes only and does not constitute tax or legal advice. Consult a qualified tax professional before making any filing decisions.

## IRS Form 8949 — Sales and Dispositions of Capital Assets

### Purpose

Report each sale, exchange, or disposition of a capital asset. For cryptocurrency, every taxable event (trade, swap, spend, gift) generates a line item on Form 8949.

### Parts

- **Part I**: Short-term transactions (held one year or less). Check Box A, B, or C.
- **Part II**: Long-term transactions (held more than one year). Check Box D, E, or F.

### Box Codes (Basis Reporting)

| Box | Meaning |
|-----|---------|
| A/D | Basis reported to IRS (1099-B received with basis) |
| B/E | Basis NOT reported to IRS (1099-B received, no basis) |
| C/F | No 1099-B received at all |

Most crypto transactions through 2025 fall under Box C/F. Starting in 2026, centralized exchanges must issue 1099-DA forms, shifting many transactions to Box A/D.

### Column Definitions

| Column | Field | Description | Example |
|--------|-------|-------------|---------|
| (a) | Description | Asset name and quantity | "10.5 SOL" |
| (b) | Date Acquired | Purchase or receipt date | "01/15/2025" |
| (c) | Date Sold | Sale or disposition date | "08/20/2025" |
| (d) | Proceeds | Amount received in USD | "$2,500.00" |
| (e) | Cost Basis | Original cost in USD + fees | "$1,800.00" |
| (f) | Adjustment Code | W (wash sale), B (basis incorrect), etc. | "W" |
| (g) | Adjustment Amount | Dollar amount of adjustment | "$200.00" |
| (h) | Gain or Loss | Column (d) minus (e), adjusted by (g) | "$700.00" |

### Taxable Events in Crypto

| Event | Taxable? | Notes |
|-------|----------|-------|
| Crypto-to-fiat sale | Yes | Gain/loss = proceeds minus basis |
| Crypto-to-crypto swap | Yes | Fair market value at time of swap |
| Spending crypto | Yes | Treated as a sale at FMV |
| Receiving as payment | Yes (income) | Ordinary income at FMV when received |
| Mining/staking rewards | Yes (income) | Ordinary income at FMV when received |
| Airdrops | Yes (income) | Ordinary income at FMV when received |
| Gifts received | No (until sold) | Basis carries over from donor |
| Transfers between wallets | No | Same owner, no disposition |
| Buying crypto with fiat | No | Establishes cost basis |

## Schedule D — Capital Gains and Losses

### Key Lines

| Line | Description |
|------|-------------|
| 1b | Short-term totals from Form 8949, Box A |
| 1c | Short-term totals from Form 8949, Box B |
| 2 | Short-term totals from Form 8949, Box C |
| 7 | Net short-term capital gain or (loss) |
| 8b | Long-term totals from Form 8949, Box D |
| 8c | Long-term totals from Form 8949, Box E |
| 9 | Long-term totals from Form 8949, Box F |
| 15 | Net long-term capital gain or (loss) |
| 16 | Combine lines 7 and 15 |
| 21 | Net capital loss deduction (max $3,000/year) |

### Capital Loss Carryforward

If net capital losses exceed $3,000 in a tax year, the excess carries forward to future years indefinitely. Track cumulative carryforward balances across tax years.

## FinCEN FBAR (Form 114)

### Filing Requirement

A U.S. person must file FinCEN Form 114 if they have a financial interest in, or signature authority over, foreign financial accounts with an **aggregate value exceeding $10,000** at any time during the calendar year.

### Key Thresholds

| Threshold | Amount | Notes |
|-----------|--------|-------|
| Filing trigger | $10,000 aggregate | Sum of ALL foreign accounts on any single day |
| Non-willful penalty | Up to $12,500 per violation | Per account, per year |
| Willful penalty | Up to $100,000 or 50% of balance | Whichever is greater |

### Crypto and FBAR

The applicability of FBAR to crypto accounts on foreign exchanges is an evolving area. FinCEN proposed rules in 2020 to include virtual currency, but final rules have not been issued as of this writing. Conservative guidance: if you hold crypto on a foreign exchange, consult a tax professional about FBAR obligations.

### Required Information per Account

- Name and address of the foreign financial institution
- Account number
- Type of account
- Maximum value during the calendar year
- Currency type

### Filing Details

- **Where**: Filed electronically via BSA E-Filing System (not with your tax return)
- **Deadline**: April 15, with automatic extension to October 15
- **No tax due**: FBAR is an information return, not a tax form

## FATCA — Form 8938

### Filing Thresholds

| Filing Status | Living in U.S. | Living Abroad |
|---------------|---------------|---------------|
| Single | $50,000 (year-end) / $75,000 (any time) | $200,000 (year-end) / $300,000 (any time) |
| Married filing jointly | $100,000 (year-end) / $150,000 (any time) | $400,000 (year-end) / $600,000 (any time) |

Form 8938 is filed with your tax return, unlike FBAR. Both may be required for the same accounts.

## State-Specific Requirements

### States with Notable Crypto Provisions (as of 2025)

| State | Requirement | Notes |
|-------|-------------|-------|
| California | Conforms to federal treatment | No special crypto rules; high marginal rates |
| New York | BitLicense for businesses | Individual reporting follows federal |
| Wyoming | No state income tax | Favorable crypto legislation |
| Texas | No state income tax | No additional reporting |
| Florida | No state income tax | No additional reporting |
| Colorado | Accepts crypto for tax payments | Standard capital gains treatment |
| Illinois | Follows federal treatment | Additional state capital gains |

### General State Guidance

- Most states conform to federal capital gains treatment
- Some states tax capital gains as ordinary income (no preferential long-term rate)
- State-level wash sale rules may differ from federal
- Check state Department of Revenue for current guidance

## Reporting Deadlines Calendar

| Date | Form | Description |
|------|------|-------------|
| January 15 | 1040-ES | Q4 estimated tax payment |
| January 31 | 1099 forms | Exchanges issue 1099s to taxpayers |
| April 15 | 1040 + Schedules | Federal tax return (with 8949, Schedule D) |
| April 15 | FBAR (Form 114) | Foreign account reporting |
| April 15 | 1040-ES | Q1 estimated tax payment |
| June 15 | 1040-ES | Q2 estimated tax payment |
| September 15 | 1040-ES | Q3 estimated tax payment |
| October 15 | Extended 1040 | Extended federal return deadline |
| October 15 | Extended FBAR | Automatic FBAR extension deadline |

## Large Transaction Reporting (Form 8300)

Businesses receiving more than $10,000 in cash (which may include digital assets under the Infrastructure Investment and Jobs Act) must file Form 8300 within 15 days. As of 2024, the IRS has indicated that digital assets will be treated as cash for Form 8300 purposes for transactions occurring after January 1, 2024.

### Key Points

- Applies to businesses, not individual traders
- Structuring transactions to avoid the $10,000 threshold is illegal
- Must report the identity of the person from whom cash was received
- Filed with FinCEN, not the IRS

## Planned Implementation Features

### Phase 1 — Core Reporting (Current Focus)
- Form 8949 line-item generation from trade CSV data
- FIFO cost-basis calculation
- Short-term vs. long-term classification
- Schedule D summary totals

### Phase 2 — Enhanced Calculations
- Multiple cost-basis methods (LIFO, HIFO, Specific ID)
- Wash sale detection and flagging
- Like-kind exchange analysis (pre-2018 trades only)
- Capital loss carryforward tracking

### Phase 3 — Additional Forms
- FinCEN FBAR data compilation
- FATCA Form 8938 threshold checking
- Form 8300 large-transaction flagging
- 1040-ES quarterly estimated tax worksheet

### Phase 4 — Output & Integration
- IRS-compatible CSV export
- PDF form generation
- Exchange API import (Coinbase, Kraken, Binance)
- Multi-year reporting with carryforward


---

## SKILL: sales-practices

- Fuente: `JoelLewis/finance_skills` → `plugins/compliance/skills/sales-practices` (MIT)
- Cuándo usarla: Identify and prevent sales practice violations under FINRA and SEC rules governing broker-dealer conduct. Use when the user asks about churning or excessive trading metrics, mutual fund breakpoint discounts, selling away or private securities transactions, outside business activities, unauthorized trading, supervisory procedure design, senior investor protections, trusted contact persons, variable annuity suitability, or options account approval. Also trigger when users mention 'turnover ratio is high', 'rep did trades without authorization', 'breakpoint abuse', 'trusted contact for elderly client', 'selling away from the firm', 'supervision failure', '1035 exchange review', 'marking the close', or ask whether a broker's conduct violates FINRA rules.

# Sales Practices

Regulatory status current as of June 2026 — verify effective dates, dollar thresholds, and pending rulemakings against current SEC/FINRA/FinCEN sources before advising.

## Core Concepts

### FINRA Rule 2010 — Standards of Commercial Honor
FINRA Rule 2010 is the catch-all ethical standard for all member firms and associated persons. It requires adherence to "high standards of commercial honor and just and equitable principles of trade." This rule is intentionally broad and serves as the basis for disciplinary action even when no other specific rule is violated. Conduct that is unethical, dishonest, or in bad faith — even if technically legal — can be sanctioned under Rule 2010. FINRA enforcement frequently pairs Rule 2010 with more specific rule violations as a supplementary charge. Examples of standalone Rule 2010 violations include forgery, misrepresentation of credentials, conversion of client funds, and failure to disclose material information.

### FINRA Rule 2020 — Use of Manipulative, Deceptive, or Other Fraudulent Devices
FINRA Rule 2020 prohibits any member or associated person from effecting any transaction in, or inducing the purchase or sale of, any security by means of any manipulative, deceptive, or other fraudulent device or contrivance. This rule mirrors the antifraud provisions of Section 10(b) of the Securities Exchange Act of 1934 and SEC Rule 10b-5. It covers a broad range of manipulative schemes including pump-and-dump, marking the close, wash trading, matched orders, and any scheme to defraud customers or the market.

### Churning and Excessive Trading
Churning occurs when a broker engages in excessive trading to generate commissions rather than to benefit the customer. Two distinct legal frameworks apply, and they have different elements:

- **Fraud-based churning (Section 10(b)/Rule 10b-5, Section 15(c)):** Requires proof of (1) control — de facto or de jure control over trading decisions (de facto control exists when the customer routinely follows the broker's recommendations without independent judgment); (2) excessive activity inconsistent with the customer's objectives; and (3) scienter — intent to defraud or reckless disregard for the customer's interests.
- **Rule-based excessive trading (FINRA Rule 2111.05(c) quantitative suitability; Reg BI Care Obligation for retail customers):** Since FINRA's 2020 amendments (Regulatory Notice 20-18, effective June 30, 2020), the control element has been removed — a broker who recommends a series of transactions must have a reasonable basis to believe the series is not excessive in light of the customer's investment profile, regardless of whether the broker controls the account. No scienter is required.

Quantitative metrics used under both frameworks:
- **Turnover ratio:** The aggregate cost of purchases divided by the average account equity over the period. A turnover ratio exceeding 6 is generally considered presumptive evidence of excessive trading. Ratios of 4-6 may indicate excessive trading depending on account type and objectives.
- **Cost-to-equity ratio (break-even return):** The total costs (commissions, markups, fees) as a percentage of average account equity on an annualized basis. A cost-to-equity ratio exceeding 20% is generally considered excessive because the account must earn more than 20% annually just to break even after costs.
- **In-and-out trading:** A pattern of purchasing securities and selling them within a short period, generating commissions on both sides without meaningful investment rationale.

### Breakpoint Abuse
Mutual funds offer volume discounts called breakpoints — reduced sales charges for larger purchases. Breakpoint abuse occurs when a broker fails to inform customers of available discounts or structures transactions to avoid breakpoints (e.g., splitting a single purchase into multiple smaller transactions across fund families). Key obligations:

- **Rights of accumulation:** Customers are entitled to count existing holdings in the same fund family toward breakpoint thresholds. Brokers must aggregate qualifying holdings when calculating applicable sales charges.
- **Letters of intent (LOI):** A customer may sign an LOI committing to purchase a specified amount within 13 months, thereby qualifying for a reduced sales charge on each purchase during that period. Brokers must inform customers of this option when a planned purchase schedule would qualify.
- **Household aggregation:** Many fund families allow aggregation of purchases across accounts within the same household for breakpoint purposes. Brokers should inquire about related accounts.

FINRA has brought numerous Letters of Acceptance, Waiver and Consent (AWC) actions against firms and individuals for breakpoint failures. In 2003, FINRA (then NASD) conducted an industrywide sweep that resulted in approximately $43 million in restitution for breakpoint overcharges. Firms must maintain systems to identify breakpoint-eligible transactions and train registered representatives on breakpoint obligations.

### Selling Away — Private Securities Transactions (FINRA Rule 3280)
FINRA Rule 3280 governs private securities transactions — any securities transaction outside the regular course or scope of an associated person's employment with a member firm. An associated person who wishes to participate in a private securities transaction must:

1. **Provide prior written notice** to the employing member firm describing the proposed transaction in detail, the person's proposed role, and whether they have received or may receive selling compensation.
2. **If compensation is involved:** The firm must evaluate the transaction, and if it approves, must record the transaction on its books and supervise the person's participation as if the transaction were executed through the firm. If the firm disapproves, the person must not participate.
3. **If no compensation is involved:** The firm must acknowledge the notice and may impose conditions or restrictions.

Selling away is one of the most common violations leading to FINRA disciplinary action and customer arbitration claims. Associated persons who sell unregistered securities, promissory notes, or interests in private companies without firm approval expose both themselves and investors to significant risk. Common selling away scenarios include private placements, real estate investments, cryptocurrency ventures, and personal loans from customers.

### Outside Business Activities (FINRA Rule 3270)
FINRA Rule 3270 requires associated persons to provide prior written notice to their employing member firm before engaging in any business activity outside the scope of their relationship with the firm. The notice must describe the activity and disclose whether compensation will be received. Upon receiving notice, the firm must:

- Evaluate the proposed activity for potential conflicts of interest, securities law implications, and reputational risk
- Determine whether the activity should be treated as a private securities transaction under Rule 3280
- Impose conditions or restrictions as appropriate, or prohibit the activity entirely
- Supervise the associated person's outside activities on an ongoing basis

The distinction between OBAs (Rule 3270) and private securities transactions (Rule 3280) is critical: if the outside activity involves a securities transaction, Rule 3280 applies and imposes heightened requirements. Firms that fail to evaluate OBA notices or maintain adequate records face supervisory failure charges.

### Supervision Requirements (FINRA Rules 3110 and 3120)
FINRA Rule 3110 (Supervision) requires each member firm to establish, maintain, and enforce a system to supervise the activities of its associated persons that is reasonably designed to achieve compliance with applicable securities laws, regulations, and FINRA rules. Key components:

- **Written Supervisory Procedures (WSPs):** Every firm must maintain written procedures addressing each applicable regulatory requirement, specifying who is responsible, what activities are reviewed, and how reviews are documented.
- **Designation of supervisory personnel:** Each registered person must be assigned to a supervisor. Each office must have a designated principal or supervisory structure.
- **Branch office supervision:** Office of Supervisory Jurisdiction (OSJ) designations, branch office inspections (at least annually for OSJs, at least every three years for non-OSJ branch offices), and surprise inspections where warranted.
- **Review of customer accounts:** Regular review of account activity including trade blotters, exception reports, correspondence, customer complaints, and account statements.
- **Exception reporting:** Automated surveillance systems to flag potentially problematic activity such as excessive trading, concentration, mutual fund switching, and large transactions.

FINRA Rule 3120 (Supervisory Control System) requires each firm to designate one or more principals to establish, maintain, and enforce supervisory control policies and procedures. These principals must test and verify that the firm's supervisory system is functioning effectively. Senior management must receive an annual report on the firm's supervisory controls.

Supervisory failures are among the most frequently cited violations in FINRA enforcement actions. A firm may be held liable for a registered representative's misconduct if the firm failed to reasonably supervise or ignored red flags.

### Marking the Close and Market Manipulation
Marking the close involves placing orders near the end of the trading day with the purpose of artificially influencing the closing price of a security. This practice is prohibited under FINRA Rule 2020, Section 9(a)(2) of the Securities Exchange Act of 1934, and SEC Rule 10b-5. Related prohibited manipulative practices include:

- **Wash trading:** Simultaneously buying and selling the same security to create the appearance of active trading volume
- **Matched orders:** Arranging with another party to enter offsetting buy and sell orders to simulate market activity
- **Pump-and-dump:** Artificially inflating a security's price through false or misleading statements, then selling at the inflated price
- **Spoofing/layering:** Placing orders with the intent to cancel before execution to create a false impression of supply or demand
- **Front-running:** Trading ahead of a customer order to profit from the anticipated price impact

### Unauthorized Trading
Unauthorized trading occurs when a broker executes transactions in a customer's account without obtaining prior authorization. The regulatory framework distinguishes between account types:

- **Non-discretionary accounts:** The broker must obtain the customer's express prior consent before executing each transaction. Any trade placed without such consent is unauthorized, regardless of whether it is profitable.
- **Discretionary accounts:** The broker may exercise discretion over the selection, timing, and amount of securities to trade, but only after the customer has granted written discretionary authority and the firm has accepted it. Even with discretion, the broker must act consistently with the customer's stated investment objectives and constraints.
- **Time-and-price discretion:** A limited form of discretion where the customer authorizes a specific transaction but grants the broker flexibility on timing and execution price. This does not require written discretionary authority if exercised on the same day.

Unauthorized trading violates FINRA Rules 2010 and 2020 and may also constitute fraud under federal securities law. Patterns of unauthorized trading frequently accompany churning allegations.

### Senior Investor Protections (FINRA Rule 2165)
FINRA Rule 2165 provides a safe harbor for member firms to place temporary holds on disbursements of funds or securities from accounts of specified adults — customers aged 65 or older, or customers aged 18 or older who the firm reasonably believes have a mental or physical impairment that renders them unable to protect their own interests. Key provisions:

- **Trusted contact person:** FINRA Rule 4512 requires firms to make reasonable efforts to obtain the name and contact information of a trusted contact person for each customer account. The trusted contact may be notified when the firm suspects financial exploitation, but the trusted contact does not have authority over the account.
- **Temporary hold:** If a firm reasonably believes that financial exploitation has occurred, is occurring, has been attempted, or will be attempted, the firm may place a temporary hold on disbursements — and, since the March 2022 amendments, on securities transactions as well — for up to 15 business days while it investigates. The hold may be extended for an additional 10 business days with firm approval. The 2022 amendments (effective March 17, 2022) also permit a further extension of up to 30 additional business days (55 business days total) if the firm has reported the matter to a state regulator or agency of competent jurisdiction (such as Adult Protective Services) or a court of competent jurisdiction.
- **Notification requirements:** The firm must notify the trusted contact person and all parties authorized to transact on the account of the hold, unless the firm reasonably believes one of those parties is responsible for the suspected exploitation.
- **Record retention:** The firm must retain records of the basis for the hold, internal review, and customer/trusted contact notifications.

These rules do not require firms to place holds but provide a safe harbor from liability when firms act in good faith to protect vulnerable customers.

### Variable Annuity Sales (FINRA Rule 2330)
FINRA Rule 2330 imposes heightened suitability requirements for recommended purchases and exchanges of deferred variable annuities. Before recommending a VA transaction, the broker must make reasonable efforts to obtain and consider:

- The customer's age, annual income, financial situation and needs, investment experience, investment objectives, intended use of the annuity, investment time horizon, existing assets (including other insurance and annuity holdings), liquidity needs, liquid net worth, risk tolerance, and tax status.

Specific requirements for VA recommendations:
- The broker must have a reasonable basis to believe that the customer has been informed of the features of the annuity, including surrender charges, potential tax penalties, various fees and charges, and market risk.
- The customer would benefit from certain features of the annuity (such as tax-deferred growth, annuitization, or a death benefit) that are not available through other products.
- The particular annuity as a whole, the underlying subaccounts, riders, and features are suitable.

**1035 Exchanges:** When a customer exchanges one annuity or insurance contract for another under IRC Section 1035 (a tax-free exchange), the broker must evaluate whether the new contract provides materially better features or benefits. The broker must consider whether the customer will incur surrender charges on the existing contract, lose benefits (such as a death benefit step-up), face a new surrender charge period, or face increased fees. A 1035 exchange that primarily generates a new commission without meaningful customer benefit is a supervisory red flag.

### Options Sales (FINRA Rule 2360)
FINRA Rule 2360 governs the conduct of member firms and associated persons in options transactions. Key requirements:

- **Options account approval:** Before a customer can trade options, the firm must approve the account. Approval must be based on background and financial information including investment objectives, employment status, estimated annual income and net worth, investment experience, and the types of options strategies the customer is approved to use (typically tiered: covered calls, long options, spreads, uncovered writing).
- **Options Disclosure Document (ODD):** The firm must furnish each customer with the current ODD (titled "Characteristics and Risks of Standardized Options") at or before the time the account is approved for options trading. The ODD must be delivered before the customer's first options transaction.
- **Suitability:** Options recommendations must be suitable considering the customer's financial situation, investment objectives, and experience level. Complex strategies (spreads, straddles, uncovered writing) require demonstrated understanding and sufficient financial resources to bear the risk.
- **Supervision and compliance:** The firm must designate a Registered Options Principal (ROP) to review and approve options accounts and transactions. The ROP must review the customer's background information and approve the level of options trading authorized.
- **Position and exercise limits:** FINRA and the options exchanges impose limits on the maximum number of options contracts on the same side of the market that any person or group of persons acting in concert may hold or exercise.
- **Options communications:** All options-related communications (advertisements, sales literature, correspondence) must be supervised and must present a balanced picture of risks and rewards. Projections of future performance and claims of limited risk must be accurate and not misleading.

## Worked Examples

### Example 1: Churning in a Retiree's Account
**Scenario:** A 72-year-old retiree with a stated objective of income and capital preservation opens a brokerage account with $500,000. Over 12 months, her broker executes 147 transactions. The aggregate cost of purchases during the period is $3,200,000. The average account equity over the year is $480,000. Total commissions and fees charged are $112,000.

**Compliance Issues:**
- **Turnover ratio:** $3,200,000 / $480,000 = 6.67. This exceeds the presumptive churning threshold of 6.
- **Cost-to-equity ratio:** $112,000 / $480,000 = 23.3% annualized. This exceeds the 20% threshold generally considered excessive. The account must earn over 23% annually just to break even after costs.
- **In-and-out trading:** With 147 transactions in a $480,000 account over 12 months, the average holding period is extremely short, inconsistent with an income and capital preservation objective.

**Analysis:** This pattern presents strong presumptive evidence of excessive trading under FINRA Rule 2111.05(c) (quantitative suitability — no control element required since the 2020 amendments) and, for a retail customer, under Reg BI's Care Obligation; fraud-based churning charges under Section 10(b)/Rule 10b-5 are also available if control and scienter can be established. The customer's age, conservative objectives, and reliance on the broker for retirement income are aggravating factors. The firm may also face supervisory failure charges under FINRA Rule 3110 if its exception reporting systems did not flag this activity or if flagged exceptions were not investigated. Potential remedies include disgorgement of excess commissions, restitution, fines, suspension, or barring of the broker.

### Example 2: Breakpoint Abuse on Mutual Fund Purchases
**Scenario:** A customer wishes to invest $100,000 in equity mutual funds. The fund family's Class A shares have the following breakpoint schedule: 5.75% sales charge on purchases under $25,000; 5.00% at $25,000; 4.50% at $50,000; 3.50% at $100,000; and 2.50% at $250,000. Rather than placing a single $100,000 purchase to receive the 3.50% sales charge, the broker splits the investment across four different fund families in $25,000 increments. The customer pays an average sales charge of approximately 5.00%.

**Compliance Issues:**
- The customer was not informed of the breakpoint schedule and the discount available at $100,000.
- The customer already held $160,000 in the same fund family in a separate account, which under rights of accumulation would have pushed the combined total to $260,000, qualifying for the 2.50% breakpoint.
- The broker did not inquire about related accounts held at other firms or by household members.
- The broker did not discuss the option of a Letter of Intent for planned future purchases.

**Analysis:** The customer paid approximately $5,000 in sales charges instead of $2,500 (at the 2.50% rate with rights of accumulation) — an overcharge of $2,500. This violates FINRA breakpoint guidance and Rule 2010. The firm's supervisory systems should have flagged the split purchases. FINRA AWC actions in this area typically require restitution of overcharges, a fine, and remediation of supervisory procedures. The broker may face individual sanctions. If the splitting was intentional to generate higher concessions for the broker, it may also implicate Rule 2020.

### Example 3: Selling Away — Unapproved Private Placements
**Scenario:** A registered representative learns about a private real estate development project through a personal contact. Believing it is a strong investment opportunity, the representative recommends the investment to 15 of his brokerage clients, raising $2.3 million. The representative receives a 7% referral fee ($161,000). He does not provide written notice to his employing firm, does not record the transactions on the firm's books, and the investments are not supervised by the firm. Two years later the project fails and investors lose substantially all of their investment.

**Compliance Issues:**
- The representative failed to provide prior written notice to his firm before participating in a private securities transaction, violating FINRA Rule 3280.
- Because selling compensation was involved, the firm would have been required to approve, record, and supervise the transaction. None of these steps occurred.
- The investments were unregistered securities sold without the protections of firm due diligence, compliance review, or customer suitability analysis.
- The representative's receipt of undisclosed referral fees creates a material conflict of interest.

**Analysis:** This is a clear violation of FINRA Rule 3280 (private securities transactions/selling away) and Rule 2010 (standards of commercial honor). The representative faces potential barring from the industry. The firm may also face supervisory liability under Rule 3110 if it had reason to know about the representative's outside activities (e.g., customer complaints, lifestyle indicators, or OBA disclosures that should have prompted further inquiry) and failed to investigate. Customers may pursue arbitration claims against both the representative and the firm. FINRA enforcement actions for selling away frequently result in bars, suspensions, and substantial fines. The firm's failure to detect the activity may indicate deficiencies in its OBA review process and surveillance of associated persons' activities.

## Common Pitfalls
- Treating a high turnover ratio in isolation without considering the customer's investment objectives — active trading in a growth account with a long horizon differs from active trading in a retiree's income account
- Failing to aggregate household accounts and existing fund holdings when calculating breakpoint eligibility
- Assuming that an associated person's outside activity is "not securities-related" without conducting a proper analysis under Rule 3280 — many OBAs have securities components that trigger heightened obligations
- Relying on automated exception reports without meaningful human review — FINRA expects supervisors to investigate flagged exceptions, document findings, and take corrective action
- Confusing time-and-price discretion (which does not require written authorization if exercised the same day) with full discretionary authority (which always requires written authorization)
- Assuming that a profitable unauthorized trade is not a violation — unauthorized trading is a violation regardless of outcome
- Failing to place a temporary hold under Rule 2165 out of concern about interfering with customer rights — the rule provides a safe harbor specifically to encourage protective action
- Recommending VA exchanges (1035 exchanges) without documenting the comparative analysis of surrender charges, fees, and benefits between the old and new contracts
- Approving customers for options strategies beyond their demonstrated knowledge, experience, and financial capacity
- Treating FINRA Rule 2010 as a minor or supplementary charge — it is a powerful independent basis for discipline covering any conduct inconsistent with just and equitable principles of trade
- Failing to update WSPs when regulations change or when the firm's business model evolves, leaving gaps in supervisory coverage

## Cross-References
- **investment-suitability** (compliance plugin): Suitability obligations (FINRA Rule 2111) are closely intertwined with sales practices — churning is a quantitative suitability violation
- **reg-bi** (compliance plugin): Regulation Best Interest imposes a heightened standard on broker-dealer recommendations that overlaps with and strengthens sales practice requirements
- **conflicts-of-interest** (compliance plugin): Selling away, undisclosed compensation, and breakpoint abuse all involve conflicts of interest that must be identified, disclosed, and mitigated
- **know-your-customer** (compliance plugin): KYC obligations under FINRA Rule 2090 provide the customer information foundation for detecting sales practice violations
- **fiduciary-standards** (compliance plugin): For dual-registrants, fiduciary duties may impose obligations beyond FINRA sales practice rules
- **account-opening-compliance** (client-operations plugin): Trusted contact collection (FINRA Rule 4512) and senior investor protection infrastructure are established at onboarding; this skill covers the ongoing-conduct side of Rules 2165/4512


---

## SKILL: sanctions-compliance-process

- Fuente: `SYasJ/claude-business-skills` → `plugins/risk/skills/sanctions-compliance-process` (MIT)
- Cuándo usarla: Describe how a legitimate screening process should handle a possible match, for compliance staff. Not evasion advice. Use when the user mentions sanctions screening, possible match, screening operations, name match review, or asks for a screening operations note. Risk and compliance skill by Yasir Jilani.

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'sanctions-compliance-process' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Sanctions Screening Operations

Describe how a legitimate screening process should handle a possible match, for compliance staff. Not evasion advice.

## When to use this skill

Use this skill when the user:

- sanctions screening
- possible match
- screening operations
- name match review

## When not to use this skill

- Sanctions evasion
- Altering records to defeat screening

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

- The match information they are allowed to share
- Their escalation policy
- The business process paused
- The compliance owner

## Workflow


### 1. Step 1

Treat a possible match as unresolved until their compliance owner clears it.
### 2. Step 2

Do not advise altering a name, address, or ownership record to avoid a match.
### 3. Step 3

List the documents their policy already uses to distinguish a false positive.
### 4. Step 4

Pause the prohibited transaction if their policy says to pause.
### 5. Step 5

Record the decision and the reviewer.
### 6. Step 6

This skill does not determine whether a person is sanctioned and does not help anyone evade screening.

## Output

Deliver a **screening operations note**.

- Purpose of this screening operations note, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a screening operations note by 30 September 2026. Sales wants to tweak a customer name so the screening tool stops flagging it.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Sales wants to tweak a customer name so the screening tool stops flagging it.

The match information they are allowed to share: plain, for people who already know the context. No house guide attached
Their escalation policy: their one-page rule dated 2 Mar 2026. No exception log
The business process paused: email to Priya Shah. No written steps after 1 Sep 2026
The compliance owner: Priya Shah, controller
```

### Example outcome

**Screening operations note**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A refusal of the tweak, a pause recommendation, and a handoff to the compliance owner.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The match information they are allowed to share | plain, for people who already know the context. No house guide attached | Needs confirmation |
| Their escalation policy | their one-page rule dated 2 Mar 2026. No exception log | Carried into the draft |
| The business process paused | email to Priya Shah. No written steps after 1 Sep 2026 | Carried into the draft |
| The compliance owner | Priya Shah, controller | Needs confirmation |

**How this draft was built**

**1. Treat a possible match as unresolved until their compliance owner clears it**

**2. Do not advise altering a name, address, or ownership record to avoid a match**

**3. List the documents their policy already uses to distinguish a false positive**

**4. Pause the prohibited transaction if their policy says to pause**

**5. Record the decision and the reviewer**

**Deliberately not done**
- Advice to alter records to dodge a match.
- A homemade legal clearance.
- Skipping the compliance owner.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Advice to alter records to dodge a match
- A homemade legal clearance
- Skipping the compliance owner

## Related skills

- `third-party-risk`
- `ethics-hotline-triage`


---

## SKILL: settlement-clearing

- Fuente: `JoelLewis/finance_skills` → `plugins/trading-operations/skills/settlement-clearing` (MIT)
- Cuándo usarla: Guide the understanding and management of trade settlement and clearing processes. Use when designing settlement workflows for T+1 compliance, understanding DTC/NSCC/FICC clearing infrastructure, analyzing continuous net settlement (CNS) netting obligations, setting up institutional trade processing (affirmation, confirmation, allocation, matching), investigating settlement fails and designing fail reduction programs, implementing buy-in procedures under Reg SHO Rule 204, assessing corporate action impact on pending settlements, evaluating DVP/RVP mechanics for institutional deliveries, handling when-issued or as-of trades, or managing settlement bank relationships and intraday liquidity. Also covers FX funding gaps for cross-border T+1 settlement.

# Settlement & Clearing

## Core Concepts

### Settlement Cycle
The settlement cycle defines the number of business days between trade date (T) and settlement date (S), during which the buyer must deliver payment and the seller must deliver securities. The settlement cycle has shortened over time to reduce counterparty risk and systemic exposure.

**Current US settlement cycles:**
- **T+1** — US equities (exchange-listed and OTC), corporate bonds, municipal bonds, and unit investment trusts. Effective May 28, 2024, the SEC shortened the standard settlement cycle from T+2 to T+1 under amended Exchange Act Rule 15c6-1(a) (SEC Release No. 34-96930). The move to T+1 reduced the window of counterparty and market risk by approximately 50%, but imposed significant operational demands on market participants to compress post-trade processing into a single business day.
- **T+0 (same-day settlement)** — US government securities (Treasury bills, notes, bonds, and agency securities) settle on trade date or T+1 depending on the instrument and market convention. Options contracts settle T+0 (premium payment) for the premium, with exercise settlement following the underlying's settlement cycle. Money market instruments, including commercial paper and repurchase agreements, typically settle same-day or T+1.
- **T+2** — Remains the standard settlement cycle for many international equity markets (though Europe, the UK, Canada, and others have moved or are moving to T+1). Certain cross-border transactions may still settle on a T+2 or longer basis depending on the foreign market's settlement conventions.

**Settlement date calculation:** Settlement dates are computed using business days, excluding weekends and market holidays. The SIFMA holiday calendar governs US fixed-income markets; exchange calendars govern equity markets. For cross-border trades, settlement date calculation must account for holidays in both the buyer's and seller's jurisdictions — a mismatch can cause unintended settlement delays.

**Same-day settlement:** Certain transactions require same-day settlement, including when-issued trades settling on the issue date, some money market transactions, and trades explicitly agreed to settle same-day. Same-day settlement requires real-time coordination between counterparties and their settlement banks and typically involves Fedwire (for government securities) or DTC's same-day facilities.

**Impact of T+1 on post-trade operations:** The compression from T+2 to T+1 eliminated an entire business day from the post-trade processing window, with cascading effects on every downstream function. Under T+2, firms could execute trades during market hours, process allocations and confirmations on the evening of T, complete affirmation and matching on the morning of T+1, and finalize settlement instructions by the afternoon of T+1 for settlement on T+2. Under T+1, the entire allocation-confirmation-affirmation-matching chain must be completed on trade date, with settlement the next morning. This required investment managers to submit allocations within hours of execution (not the next morning), broker-dealers to generate and send confirmations in near-real-time, custodians to affirm trades by 9:00 PM ET on trade date (the industry's same-day affirmation target), and all parties to resolve exceptions and discrepancies on the same day they arise. Firms that relied on manual, batch-oriented processes found T+1 compliance particularly challenging and experienced elevated fail rates during the transition period.

**Foreign exchange considerations:** For cross-border transactions involving currency conversion, the T+1 settlement cycle creates a timing challenge. The standard FX settlement cycle is T+2 (through CLS Bank for major currency pairs), meaning that the FX leg of a cross-border equity trade cannot settle simultaneously with the equity leg under T+1. This "FX funding gap" requires firms to pre-fund foreign currency positions, use same-day or tom/next FX trades (which carry wider spreads), or maintain standing foreign currency balances at custodians. The FX funding issue was one of the most significant operational challenges identified during the T+1 transition, particularly for non-US investors purchasing US securities.

**Settlement of ETF creation and redemption:** Exchange-traded fund (ETF) shares settle like other equity securities on a T+1 basis for secondary market transactions. However, the ETF primary market — where authorized participants (APs) create or redeem ETF shares by delivering or receiving baskets of underlying securities — involves a more complex settlement process. The AP must deliver the specified basket of underlying securities (which may settle T+1 or T+2 depending on the asset class) in exchange for new ETF shares, or vice versa for redemptions. Mismatches between the settlement cycles of the ETF shares and the underlying basket securities can create settlement timing issues that the AP and the ETF sponsor must manage operationally.

### Central Clearing Infrastructure
The Depository Trust & Clearing Corporation (DTCC) is the holding company for the principal clearing and settlement utilities in the US securities markets. Its subsidiaries provide the infrastructure through which virtually all US securities transactions are cleared and settled.

**DTC (The Depository Trust Company):** DTC is a central securities depository (CSD) and the primary book-entry settlement system for US equities and corporate and municipal debt securities. DTC holds securities in fungible bulk — meaning securities are held in nominee name (Cede & Co., DTC's nominee) and individual ownership is tracked through the records of DTC participants (broker-dealers, banks, and other financial institutions). Book-entry transfers between participants occur by debiting the delivering participant's DTC account and crediting the receiving participant's account, without physical movement of certificates. DTC's participant accounts are the definitive record of securities positions for settlement purposes.

**NSCC (National Securities Clearing Corporation):** NSCC is the central counterparty (CCP) for virtually all US equity and corporate bond trades. NSCC interposes itself between the buyer and seller through a process called novation — the original trade between two counterparties is replaced by two trades: one between the buyer and NSCC, and one between NSCC and the seller. This eliminates bilateral counterparty risk and replaces it with exposure to NSCC as the central counterparty. NSCC guarantees settlement of all novated trades through its clearing fund, which is funded by risk-based margin contributions from all participants. NSCC's guarantee means that if one participant fails to deliver securities or payment, NSCC will complete the settlement using its own resources and pursue the defaulting participant separately.

**FICC (Fixed Income Clearing Corporation):** FICC provides clearing and settlement services for US government securities (through its Government Securities Division, GSD) and mortgage-backed securities (through its Mortgage-Backed Securities Division, MBSD). FICC's GSD clears Treasury and agency transactions and provides netting and central counterparty services similar to NSCC's role in equities. The SEC finalized rules in 2023 requiring central clearing of certain Treasury cash and repo transactions (SEC Release No. 34-99149). The SEC extended the compliance deadlines in February 2025: eligible cash transactions must be centrally cleared by December 31, 2026, and eligible repo transactions by June 30, 2027. As of June 2026, implementation is in progress, and the SEC approved CME Securities Clearing in December 2025 as an additional Treasury clearing agency alongside FICC.

**Central counterparty (CCP) model and novation:** The CCP model is foundational to understanding settlement in US markets. When a trade is submitted to NSCC (or FICC), NSCC validates the trade details, matches the buy and sell sides, and upon successful matching, novates the trade. Post-novation, each participant's settlement obligation is to or from the CCP, not to or from the original counterparty. This has three critical effects: (1) it mutualizes counterparty default risk across all clearing participants; (2) it enables multilateral netting, dramatically reducing the gross volume of securities and cash that must move on settlement date; and (3) it provides regulatory oversight and risk management through clearing fund requirements, margin calls, and loss-allocation rules.

**Clearing fund requirements:** Each NSCC participant must contribute to the NSCC clearing fund based on the participant's risk profile, including the size and volatility of its unsettled positions, historical settlement performance, and credit quality. Clearing fund contributions are adjusted daily through NSCC's risk management system (CCLF — Clearing Fund Cash Liquidity Framework). In periods of market stress or high volatility, NSCC may issue intraday margin calls requiring participants to post additional collateral within hours. Failure to meet a margin call can result in the participant being declared in default, triggering NSCC's loss-allocation waterfall.

**NSCC default waterfall:** The sequencing of resources applied when a clearing member defaults (defaulter's margin and clearing fund deposit, CCP capital, mutualized member contributions, supplemental assessments) follows the standard CCP default waterfall — see the counterparty-risk skill (trading-operations) for the waterfall structure, Cover 1/Cover 2 standards, and recovery tools. The settlement-relevant point: a significant participant default can produce clearing fund losses for all NSCC participants, even those with no direct exposure to the defaulting counterparty.

**Trade submission and validation:** Trades enter the NSCC clearing system through multiple channels. Exchange-executed trades are automatically submitted by the exchange's matching engine. OTC trades between NSCC participants are submitted bilaterally through NSCC's trade capture systems, where both sides must agree on trade terms (security, quantity, price, settlement date, trade date) for the trade to be accepted. Trades submitted by only one side, or where the two sides disagree on terms, are flagged as "uncompared" or "advisory" items that must be resolved before novation occurs. Under T+1, the window for resolving uncompared trades is extremely tight — if a trade is not compared and novated by the end of trade date, it will not settle on T+1.

**Participant types and access:** NSCC participants include full-service clearing members (broker-dealers that clear for themselves and for correspondents), limited-purpose participants, mutual fund/insurance company participants, and other categories defined in NSCC's Rules & Procedures. Each participant type has different clearing fund requirements, settlement obligations, and access to NSCC services. Introducing broker-dealers that do not clear their own trades are not direct NSCC participants — their trades are submitted through and guaranteed by their clearing firm, which bears the clearing fund obligation and settlement risk.

**Clearing firm / introducing broker-dealer relationship:** The clearing agreement between a clearing firm and its introducing broker-dealers is the contractual foundation for settlement services. The clearing firm (also called a carrying firm or correspondent clearing firm) provides trade clearance, settlement, custody, and margin services to the introducing broker-dealer's customers. The clearing firm submits the introducing broker-dealer's trades to NSCC, maintains the customer accounts at DTC, and funds the settlement obligations through its settlement bank. In return, the introducing broker-dealer pays clearing fees (per-trade, per-account, and/or percentage-of-revenue-based fees) and may be required to post collateral or maintain minimum capital levels as defined in the clearing agreement. The clearing agreement typically includes provisions addressing: allocation of settlement fail costs, responsibility for margin deficiencies, handling of customer complaints related to operations, termination rights and conversion procedures, and indemnification for losses arising from the introducing broker-dealer's activities. Under T+1, the clearing firm's ability to process and settle the introducing broker-dealer's trades depends on timely receipt of trade data, allocation instructions, and customer settlement information — operational failures by the introducing broker-dealer directly affect the clearing firm's settlement performance metrics and clearing fund requirements.

### Continuous Net Settlement (CNS)
The Continuous Net Settlement system is NSCC's core settlement mechanism. CNS nets all of a participant's buy and sell obligations in each security into a single net long or net short position per security per day, dramatically reducing the number of individual deliveries required.

**How CNS works:** Each business day, NSCC calculates each participant's net position in every security by aggregating all new trades settling that day with any existing unsettled positions carried forward from prior days. If a participant has a net long position (more shares bought than sold), it is entitled to receive shares from NSCC. If a participant has a net short position (more shares sold than bought), it must deliver shares to NSCC. Settlement occurs through book-entry movements at DTC — NSCC instructs DTC to debit or credit participant accounts to effect the net deliveries.

**Netting efficiency:** CNS achieves netting efficiency of approximately 98% — meaning that only about 2% of the gross value of trades actually requires delivery of securities on settlement date. For example, if a participant buys 50,000 shares and sells 48,000 shares of the same security settling on the same day, the net obligation is to receive only 2,000 shares (rather than executing two separate deliveries totaling 98,000 shares). This netting efficiency is essential to the functioning of the market, as gross settlement of all trades would exceed the operational and liquidity capacity of market participants and the settlement infrastructure.

**Daily settlement obligations:** Each morning, NSCC distributes settlement obligations to participants specifying net quantities to deliver or receive in each security. Participants must fulfill delivery obligations by the applicable DTC cutoff times. Cash settlement (the net payment for all deliveries) is effected through NSCC's settlement banks via the Federal Reserve's payment system.

**Fail tracking through CNS:** When a participant fails to deliver securities on the scheduled settlement date, the obligation is not extinguished — it rolls forward in CNS as a "fail to deliver" (FTD). The failed obligation is carried in the participant's CNS position and remains due until the participant delivers the securities. CNS recalculates the participant's net position each day, and the failed obligation may be netted against new buy-side trades in the same security. This means a participant that buys additional shares of a security in which it has an outstanding fail may see the fail resolved automatically through netting. However, persistent fails are tracked and reported, and regulatory requirements (Rule 204 under Reg SHO) impose close-out obligations on participants with aged fails.

**CNS accounting entries:** From the firm's perspective, CNS positions generate specific accounting entries. A net long CNS position (securities owed to the participant by NSCC) is recorded as a "CNS fail to receive" — an asset on the firm's books representing securities the firm is entitled to receive. A net short CNS position (securities the participant owes to NSCC) is recorded as a "CNS fail to deliver" — a liability representing the firm's outstanding delivery obligation. These positions appear on the firm's FOCUS report and affect the net capital computation, as fail-to-deliver positions may require haircuts or other capital charges depending on their age and the security type.

**Balance order process:** NSCC's balance order process is the daily mechanism through which CNS positions are converted into DTC settlement instructions. Each morning, NSCC generates balance orders directing DTC to move securities between participant accounts and NSCC's account at DTC. The balance order reflects the net delivery or receipt obligation for each participant in each security. Participants receive balance order reports that detail their daily settlement obligations, and operations teams use these reports to manage inventory, prioritize deliveries, and identify potential fails before they occur.

### DVP/RVP Settlement
Delivery Versus Payment (DVP) and Receive Versus Payment (RVP) are settlement methods that ensure the simultaneous exchange of securities and payment, eliminating principal risk — the risk that one side delivers without receiving the corresponding counter-value.

**DVP mechanics:** In a DVP settlement, the delivery of securities and the payment of cash are linked so that one cannot occur without the other. If the seller delivers securities but the buyer's payment fails, the securities are returned to the seller. If the buyer submits payment but the seller fails to deliver securities, the payment is returned. This conditionality is enforced by the settlement infrastructure (DTC for US domestic settlements, Euroclear/Clearstream for international settlements).

**Institutional trade processing (the institutional delivery cycle):** For institutional trades (those involving investment managers, pension funds, insurance companies, and other institutional investors), the post-trade process involves several steps before settlement can occur:

1. **Trade execution** — The broker-dealer executes the trade on behalf of the institutional client.
2. **Allocation** — The investment manager sends allocation instructions to the broker-dealer, specifying how the trade should be split across individual client accounts (sub-accounts, fund accounts, separately managed accounts). Allocations must include account identifiers, quantities, settlement instructions, and any special handling instructions.
3. **Confirmation/Affirmation** — The broker-dealer sends a trade confirmation to the investment manager (or its custodian). The investment manager (or custodian) affirms the trade details — confirming that the trade terms (security, quantity, price, settlement date, settlement instructions) match their records. Under the T+1 regime, same-day affirmation (SDA) became critical — the industry target is to affirm trades by 9:00 PM ET on trade date to ensure timely settlement the following day.
4. **Matching** — DTC's institutional trade processing systems (formerly Omgeo, now DTCC CTM — Central Trade Manager, and DTCC's Institutional Trade Processing service, ITP) facilitate electronic matching between the broker-dealer and the investment manager/custodian. When both sides submit matching instructions, the trade is matched and forwarded for settlement.
5. **Settlement instruction** — Matched trades generate settlement instructions that are delivered to DTC for processing. DTC's settlement system debits the delivering participant's account and credits the receiving participant's account on settlement date.

**Settlement instruction types:** DTC processes several categories of settlement instructions:
- **Deliver Order (DO)** — instruction to deliver securities from one participant to another against payment
- **Deliver Free (DF)** — instruction to deliver securities without payment (used for certain internal transfers, pledges, or free deliveries)
- **Payment Order (PO)** — instruction for cash payment between participants without a corresponding securities movement
- **Pledge/Release** — instructions to pledge securities to a pledgee (for example, to a bank as collateral) or to release pledged securities back to the participant

**Same-day affirmation (SDA) under T+1:** The T+1 transition made same-day affirmation the critical bottleneck in institutional trade processing. SEC Rule 15c6-2 (adopted alongside the T+1 amendments) requires broker-dealers and investment advisers that are parties to institutional trades to establish, maintain, and enforce written policies and procedures reasonably designed to ensure the completion of allocations, confirmations, and affirmations as soon as technologically practicable and no later than the end of trade date. This is not a hard deadline with a specific penalty but a best-efforts obligation backed by written procedures. The DTCC industry target for SDA is affirmation by 9:00 PM ET on trade date, which provides sufficient processing time for settlement the following day. Trades affirmed after this window face elevated fail risk. Per DTCC data, industry SDA rates rose from approximately 73% in early 2024 to roughly 95% by the 9:00 PM ET cutoff following the May 2024 transition, though certain market segments (international investors, complex multi-leg trades, emerging market allocations) have lagged the aggregate rate.

**DTC settlement windows and cutoff times:** DTC operates on a series of processing cycles throughout the settlement day, each with specific cutoff times. The key windows include: the night cycle (processing begins the evening before settlement date for certain pre-matched institutional deliveries), the day cycle (continuous processing during business hours), and recycle processing (attempts to complete deliveries that failed earlier in the day due to insufficient position or pending receipts). Understanding DTC's processing windows is important for settlement operations because a delivery submitted after the final cutoff cannot settle until the next business day — turning a potential same-day resolution into a confirmed fail.

**Net settlement interdiction and risk controls at DTC:** DTC maintains risk controls that can block or delay settlement instructions. DTC's net debit cap limits the maximum net debit position that a participant can accumulate during the settlement day — if a participant's pending receipts (which generate debits) would cause the participant to exceed its net debit cap, DTC will hold the delivery until other credits (from outgoing deliveries or cash deposits) reduce the participant's net debit below the cap. The net debit cap is calculated based on the participant's clearing fund deposits and other collateral. Participants that frequently approach or hit their net debit cap experience settlement delays as deliveries are queued, potentially causing cascade effects to their counterparties. Operations teams must monitor the firm's DTC net debit position throughout the day and coordinate with treasury to manage liquidity within the cap.

**Receiver-authorized delivery (RAD) and reclaim limits:** DTC's RAD system allows receiving participants to set limits on the value of deliveries they will accept from specific counterparties. If a delivery exceeds the receiver's RAD limit, it is held pending the receiver's authorization. RAD limits are a risk management tool that prevents a participant from being overwhelmed by unexpected large deliveries. However, RAD holds can also delay legitimate settlements if the limits are set too conservatively or if the receiving participant's operations team does not review and authorize pending deliveries promptly.

### Settlement Fails
A settlement fail occurs when a party to a trade does not fulfill its settlement obligation — either failing to deliver securities (fail to deliver, FTD) or failing to make payment (fail to receive, FTR) — on the scheduled settlement date.

**Common causes of settlement fails:**
- **Short positions or insufficient inventory** — The seller does not hold sufficient securities in its DTC account to satisfy the delivery obligation. This is the most common cause of fails, particularly in securities with limited float, hard-to-borrow names, or during periods of high demand.
- **Documentation or instruction errors** — Mismatched settlement instructions (wrong DTC participant number, incorrect CUSIP, wrong quantity), late or missing allocation instructions from investment managers, or unaffirmed trades that cannot be matched in time for settlement.
- **Counterparty issues** — The counterparty's custodian rejects the delivery due to insufficient funds, the counterparty has been placed in a restricted status by its clearing firm, or the counterparty is undergoing a corporate event (merger, acquisition, wind-down) that disrupts normal settlement.
- **Corporate actions** — Pending corporate actions (stock splits, reverse splits, mergers, tender offers, spin-offs) can cause fails when the DTC position is frozen or when CUSIP changes create mismatches between trade records and settlement instructions.
- **System errors** — Technology failures in the broker-dealer's back-office systems, errors in STP (straight-through processing) logic, or connectivity issues with DTC or NSCC that prevent timely submission of settlement instructions.
- **Operational timing** — Under T+1, the compressed settlement window leaves minimal time to resolve issues. Trades that fail to affirm by the same-day affirmation deadline, or where allocation instructions arrive late, are at elevated risk of failing.

**Buy-in procedures and Rule 204 close-out requirements:** Regulation SHO Rule 204 imposes mandatory close-out requirements on participants with fails to deliver:
- **T+3 close-out (standard)** — A participant with a fail to deliver position in any equity security must close out the position by purchasing or borrowing securities of like kind and quantity no later than the beginning of regular trading hours on T+3 settlement date (i.e., two days after settlement date). For example, under T+1 settlement, a trade settling on T+1 that fails must be closed out by the opening of T+4 (three settlement days after trade date).
- **T+2 close-out (threshold securities)** — For securities on the threshold list (securities with large and persistent aggregate fails), the close-out must occur by the beginning of regular trading hours on T+2 settlement date (one day after settlement date).
- **Pre-borrow requirement** — Until a fail is closed out, the participant (and any broker-dealer from which it receives trades in the same security) may not accept short sale orders in that security unless the security has been pre-borrowed or the participant has obtained a bona fide arrangement to borrow.
- **Market maker exception** — Market makers engaged in bona fide market-making activity receive an extended close-out period of T+5 (five settlement days after the trade date) for fails resulting from bona fide market-making, but this exception has been narrowed by SEC guidance and is subject to scrutiny.

**Fail tracking and aging:** Clearing firms and broker-dealers track fails by aging category — the number of business days a fail has been outstanding. Standard aging buckets include 1-5 days, 6-10 days, 11-20 days, and over 20 days. Aged fails attract increasing regulatory attention and may trigger escalation procedures, mandatory buy-ins, and reporting obligations.

**Fail charges:** The SEC and NSCC impose charges on fails to incentivize timely settlement. NSCC's fail-to-deliver charges are assessed based on the value and duration of the fail. These charges create an economic incentive for participants to prioritize fail resolution.

**Impact of fails on customers:** Settlement fails have direct consequences for end customers. A customer who has sold securities but whose trade fails to settle does not receive payment on the expected settlement date — the cash is delayed until the fail is resolved. A customer who has purchased securities but whose trade fails does not receive the securities and cannot exercise ownership rights (voting, receiving dividends, pledging as collateral). Broker-dealers have an obligation under FINRA rules and their customer agreements to communicate material settlement delays to affected customers. Persistent or systematic fails affecting customer accounts may constitute a violation of the broker-dealer's duty of best execution and its obligation to process customer orders with reasonable diligence.

**Threshold securities list and Reg SHO Rule 203(b)(3):** The SEC requires self-regulatory organizations (FINRA and the exchanges) to publish daily threshold securities lists — securities in which aggregate fails to deliver at a registered clearing agency have reached specified levels. Specifically, a security is placed on the threshold list if there are aggregate fails to deliver of 10,000 shares or more per security for five consecutive settlement days and the total fails represent at least 0.5% of the issuer's outstanding shares. Once a security appears on the threshold list, participants with outstanding fails in that security face accelerated close-out obligations (13 consecutive settlement days from the trade date for pre-existing fails). The threshold list is a publicly available indicator of settlement stress in specific securities and is monitored by regulators, short sellers, and compliance departments.

### Corporate Actions and Settlement
Corporate actions — events initiated by an issuer that affect its outstanding securities — can significantly disrupt the settlement process. Proper handling of corporate actions in the settlement workflow requires precise coordination between trade capture, position management, and settlement operations.

**Record date, ex-date, and payment date alignment:**
- **Record date** — The date on which the issuer determines the holders of record entitled to a distribution (dividend, interest, rights, etc.). Determined by the issuer's board of directors.
- **Ex-date** — The first date on which a security trades without entitlement to the pending distribution. Under T+1 settlement, the ex-date is typically one business day before the record date (previously two business days under T+2). The exchange sets the ex-date based on the settlement cycle.
- **Payment date** — The date on which the distribution is actually paid to holders of record.

A buyer who purchases shares on or after the ex-date will not receive the pending distribution. A buyer who purchases before the ex-date will settle by the record date and will be the holder of record entitled to the distribution. However, if the buyer's trade fails to settle by the record date, the distribution may be credited to the wrong party, requiring a claims process (a "due bill" or dividend claim) to redirect the payment.

**Dividend and interest adjustments on settlement:** When trades settle after the record date for a distribution, the settlement process must account for accrued interest (for fixed-income securities) or declared-but-unpaid dividends (for equities). DTC's systems automatically process dividend claims — if a security is sold before the ex-date but the trade fails, and the seller is credited with the dividend, DTC will process a claim to redirect the dividend to the buyer who was entitled to it.

**Stock split impact on pending settlements:** When a stock split (forward or reverse) takes effect, all pending settlement obligations must be adjusted to reflect the new share quantity and price. NSCC's CNS system automatically adjusts pending positions — for example, a pending delivery of 1,000 shares at $100 per share will be automatically adjusted to 2,000 shares at $50 per share in a 2-for-1 forward split. However, trades that are in transit (submitted but not yet settled) at the time of the split can create reconciliation issues, particularly when the effective date falls between trade date and settlement date.

**Merger and acquisition close impact:** When an M&A transaction closes, the target company's securities are typically exchanged for the acquirer's securities, cash, or a combination. Pending settlements in the target security must be resolved before or at the close — DTC may freeze the target security's CUSIP and process mandatory exchanges. Trades that fail to settle before the close may require special handling, including the creation of new settlement obligations in the acquirer's securities.

**Mandatory vs. voluntary corporate actions:** Mandatory corporate actions (stock splits, mergers, spin-offs, mandatory redemptions) are applied automatically to all holders by the depository and do not require affirmative action by the holder. Voluntary corporate actions (tender offers, rights offerings, optional dividends) require the holder to submit instructions by a specified deadline, and the settlement operations team must ensure that instructions are transmitted to DTC within the required timeframes.

**Spin-off impact on settlement:** When a company executes a spin-off, shareholders of the parent company receive shares of the new entity on a specified distribution date. Pending settlements in the parent company's stock that span the ex-date of the spin-off require careful handling — the buyer who purchases before the ex-date is entitled to both the parent shares and the spin-off shares. If the trade fails and the seller receives the spin-off distribution, a claims process must redirect the distribution to the entitled buyer. Additionally, the spin-off creates a new CUSIP and a new settlement obligation for the distributed shares, which must be incorporated into the firm's position records and reconciled against DTC's distribution records.

**Bond interest accrual and settlement:** For fixed-income securities, accrued interest is a standard component of the settlement amount. The buyer pays the seller accrued interest from the last coupon payment date to (but not including) the settlement date, and the buyer then receives the full coupon on the next payment date. When a bond trade fails to settle, the accrued interest calculation must be adjusted for each day the fail persists — the buyer's total settlement amount increases by one day's accrued interest for each day of delay. For corporate bonds settling T+1 and government bonds settling T+0 or T+1, fails on interest payment dates or near coupon dates require particular attention to ensure accurate interest allocation between buyer and seller.

**Reorganization deposits and withdrawals:** When a corporate reorganization (merger, acquisition, exchange offer) reaches its effective date, DTC processes the exchange of old securities for new securities (or cash) through its reorganization system. Participants must submit their positions in the old security for exchange by the specified deadline. Pending settlement obligations in the old security that remain unsettled at the reorganization cutoff must be resolved — either by completing settlement before the deadline, by converting the obligation into the reorganization consideration (new securities or cash), or by processing the obligation as a "when-distributed" trade in the new securities.

### Settlement Risk Management
Settlement risk encompasses all risks that can prevent the successful completion of a securities transaction on the intended settlement date. Effective settlement risk management is a core function of back-office operations and a regulatory expectation for clearing firms and broker-dealers.

**Counterparty risk in settlement:** Between trade date and settlement date, each party is exposed to the risk that the other party will default on its settlement obligation. Under T+1, this exposure window is shorter than under T+2, but the compressed timeline also means less time to identify and mitigate problems. Pre-settlement counterparty risk is managed through credit limits, counterparty monitoring, and margin requirements imposed by the clearing house.

**FTD (failure to deliver) monitoring:** Firms must monitor their fail positions daily and maintain systems that flag fails approaching regulatory close-out deadlines. The SEC publishes aggregate FTD data on a semi-monthly basis (with a delay), and firms use this data alongside their own internal fail tracking to identify systemic issues. Persistent high-fail-rate securities may be added to the threshold list under Reg SHO Rule 203(b)(3), triggering enhanced close-out requirements.

**Pre-settlement risk:** The risk that a counterparty will default between trade date and settlement date, leaving the non-defaulting party with market risk (the cost of replacing the trade at current market prices). Pre-settlement risk is proportional to the time between trade and settlement and to the volatility of the security. The move from T+2 to T+1 reduced pre-settlement risk by shortening the exposure window.

**Liquidity management for settlement obligations:** Clearing firms and broker-dealers must manage intraday and overnight liquidity to meet settlement obligations. NSCC's daily cash settlement requires participants to fund net payment obligations through their settlement banks by specified deadlines. Firms must forecast daily settlement funding needs, maintain adequate credit facilities with settlement banks, and monitor real-time cash positions to avoid payment failures. A payment failure at the clearing house level can cascade into a broader settlement disruption.

**Settlement bank relationships:** Participants in NSCC and DTC settle cash obligations through designated settlement banks. The participant's settlement bank receives debit instructions from NSCC and must fund the participant's obligations. Settlement banks impose credit limits on participants, and a reduction in a settlement bank's credit line can constrain a participant's ability to settle trades. Firms should maintain relationships with multiple settlement banks and monitor their settlement bank's financial condition as part of operational risk management.

**Operational risk controls:** Settlement operations require robust controls to prevent and detect errors:
- **Automated reconciliation** — Daily reconciliation of the firm's internal trade records against NSCC and DTC records to identify discrepancies before settlement.
- **Exception-based monitoring** — Systems that flag trades at risk of failing (unaffirmed trades, trades with mismatched settlement instructions, trades in securities undergoing corporate actions) for prioritized attention.
- **Escalation procedures** — Defined escalation paths for fails that are approaching close-out deadlines or that exceed dollar thresholds, with notification to compliance, risk management, and senior operations management.
- **Capacity planning** — Settlement operations must be staffed and resourced to handle peak volume days (index rebalancing, option expiration, quarter-end) and stress events (market dislocations, flash crashes) that generate elevated trade volumes.
- **Segregation and possession/control** — SEC Rule 15c3-3 requires broker-dealers to maintain physical possession or control of all fully paid and excess margin customer securities. Settlement operations must ensure that customer securities are not used to satisfy the firm's proprietary delivery obligations and that securities received on behalf of customers are promptly credited to the customer's account and segregated from the firm's proprietary positions. Violations of possession or control requirements are among the most serious regulatory infractions for a broker-dealer.

**Herstatt risk and cross-border settlement:** Herstatt risk (also called cross-currency settlement risk or principal risk) refers to the risk that one leg of a foreign exchange or cross-border securities transaction settles while the other leg does not, due to time zone differences or counterparty default. The term originates from the 1974 failure of Bankhaus Herstatt, which defaulted after receiving Deutsche marks but before delivering US dollars. In modern settlement, Herstatt risk is mitigated through DVP mechanisms, CLS Bank for FX settlement, and payment-versus-payment (PVP) systems. However, for cross-border securities transactions that do not settle through linked CSD systems, residual Herstatt risk remains and must be managed through pre-funding, collateral arrangements, or counterparty credit limits.

**Systemic risk and settlement interdependencies:** Settlement risk has a systemic dimension because the failure of one major participant can cascade through the settlement system. If a large participant fails to deliver a widely held security, all participants expecting to receive that security may be unable to meet their own downstream delivery obligations, creating a chain of fails. NSCC's central counterparty role and its CNS netting mechanism are designed to contain this risk by isolating the defaulting participant's positions and using clearing fund resources to complete settlement. However, in extreme scenarios — such as a major broker-dealer failure coinciding with high market volatility — the clearing fund may be insufficient, triggering loss allocation to surviving participants. Firms should stress-test their settlement operations against scenarios involving major counterparty defaults and simultaneous market dislocations.

**Regulatory expectations for settlement risk management:** The SEC and FINRA expect broker-dealers and clearing firms to maintain written policies and procedures for settlement risk management. FINRA Rule 3110 requires supervisory systems reasonably designed to ensure compliance with settlement obligations. The SEC's examination priorities regularly include assessment of firms' settlement operations, fail management, and Reg SHO compliance. Firms should be prepared to demonstrate to examiners: documented settlement procedures, fail escalation protocols, evidence of daily settlement monitoring, records of buy-in notices and executions, clearing fund liquidity management procedures, and counterparty risk assessment related to settlement exposure.

### Special Settlement Scenarios
Certain types of trades or market events create non-standard settlement conditions that require specialized handling.

**When-issued trading:** Securities that have been authorized but not yet issued (such as new Treasury securities, IPO shares, or securities involved in a corporate reorganization) trade on a when-issued (WI) basis. When-issued trades settle on the issue date or on a date specified by the market. WI trades carry settlement risk because the security does not yet exist — if the issuance is cancelled or modified, the when-issued trades must be cancelled or adjusted.

**Extended settlement trades:** Parties may agree to a settlement date longer than the standard cycle (for example, T+3 or T+5 for a negotiated block trade). SEC Rule 15c6-1(a) permits extended settlement if the parties expressly agree to a longer settlement cycle at the time of the transaction. Extended settlement trades must be clearly marked in the firm's trade capture and settlement systems.

**Partial deliveries:** When a seller cannot deliver the full quantity of securities owed, a partial delivery may be submitted. DTC and NSCC accept partial deliveries, and the remaining obligation is carried forward as a fail. Partial deliveries require careful tracking to ensure that the remaining obligation is resolved within the applicable close-out deadlines.

**Reclaim and demand transactions:** A reclaim occurs when a participant demands the return of securities that were previously delivered, typically because the original delivery was made in error or was based on incorrect settlement instructions. Demand transactions are instructions to demand payment for securities that have been delivered but for which payment has not been received. Both reclaims and demands are processed through DTC's systems and must be submitted within specified timeframes.

**DK (Don't Know) trades:** A DK trade is one that a participant does not recognize or does not agree to. When a trade is submitted to NSCC and the counterparty "DKs" the trade (disputes the trade terms), the trade is rejected from the clearing process and must be resolved bilaterally between the parties. DK trades are a significant source of settlement fails if not resolved quickly, particularly under T+1 where the resolution window is compressed.

**As-of trades:** An as-of trade is a trade submitted to the clearing system after the original trade date, with the original trade date preserved for settlement and regulatory reporting purposes. As-of trades are used to correct errors, process late-reported trades, or reflect trades that were initially processed outside the clearing system. As-of trades must be clearly flagged in the firm's records and may attract regulatory scrutiny if used excessively, as they can indicate operational deficiencies or potential manipulative activity.

**Reg SHO locate and delivery requirements for short sales:** Short sale transactions present unique settlement challenges because the seller does not own the securities at the time of sale. Regulation SHO Rule 203(b)(1) requires broker-dealers to locate securities available for borrowing before accepting or effecting a short sale order (the "locate requirement"). The locate must be documented and must be based on a reasonable determination that the security can be borrowed for delivery on the settlement date. Even with a valid locate, settlement may fail if the lender recalls the securities, the locate becomes stale, or demand for the security increases between trade date and settlement date. The interplay between the locate requirement, the settlement obligation, and the close-out rules under Rule 204 creates a complex compliance framework that settlement operations teams must navigate daily.

**Stock loan and settlement integration:** The securities lending market is tightly integrated with the settlement process. When a firm borrows securities to cover a short sale or to satisfy a delivery obligation, the borrow itself is a transaction that must settle — the lender delivers securities to the borrower, and the borrower provides cash collateral (typically 102% of the market value of the securities for domestic equities, 105% for international securities). Securities loan transactions settle through DTC's book-entry system, and the cash collateral is managed through the firm's treasury function. Daily mark-to-market adjustments ensure that collateral levels remain appropriate as the market value of the borrowed securities fluctuates. Recalls by the lender (demanding return of the borrowed securities) can trigger settlement fails if the borrower cannot return the securities or find an alternative borrow source in time.

**Ex-clearing and bilateral settlement:** While the vast majority of US securities transactions settle through NSCC and DTC, certain transactions are settled "ex-clearing" — outside the central clearing infrastructure. Ex-clearing transactions are settled bilaterally between the two counterparties, typically through direct DTC deliver orders rather than through NSCC's CNS system. Reasons for ex-clearing settlement include: trades in securities not eligible for NSCC clearing, settlement of previously failed trades where the parties agree to settle bilaterally, settlement of securities lending transactions, and resolution of trade disputes. Ex-clearing transactions lack the risk-mitigating benefits of central clearing (no CCP guarantee, no multilateral netting) and require the firm to manage counterparty risk directly. Firms should track ex-clearing settlement volume and ensure that bilateral settlement procedures include appropriate credit controls and operational safeguards.

**Prime brokerage and settlement:** In prime brokerage arrangements, the prime broker provides settlement services for hedge fund clients who execute trades through multiple executing brokers. When a hedge fund executes a trade with an executing broker, the trade is "given up" to the prime broker for clearing and settlement. The prime broker assumes the settlement obligation — it receives or delivers securities through its DTC account on behalf of the hedge fund. This creates a three-party settlement dynamic: the executing broker delivers to (or receives from) the prime broker, and the prime broker allocates the position to the hedge fund client's account. Give-up agreements define the obligations and limits governing this process, including the types of securities and trade sizes the prime broker will accept. Under T+1, the give-up notification and acceptance process must be completed on trade date, which requires automated give-up messaging between executing brokers and prime brokers.

### Key Regulatory References

**SEC rules governing settlement:**
- **Rule 15c6-1(a)** — Establishes the standard settlement cycle. Amended in 2023 to shorten the cycle from T+2 to T+1, effective May 28, 2024 (SEC Release No. 34-96930).
- **Rule 15c6-2** — Requires broker-dealers and investment advisers to establish written policies and procedures for same-day allocation, confirmation, and affirmation of institutional trades.
- **Regulation SHO Rule 203** — Locate requirement for short sales; threshold securities list; enhanced close-out obligations for threshold securities.
- **Regulation SHO Rule 204** — Mandatory close-out requirements for fails to deliver, including timelines, pre-borrow restrictions, and market maker exceptions.
- **Rule 15c3-3** — Customer protection rule requiring possession or control of customer securities and maintenance of a special reserve bank account for the exclusive benefit of customers.
- **Rule 15c3-1** — Net capital rule; settlement fails may generate haircuts that reduce the firm's net capital.
- **Rule 17a-3 / 17a-4** — Books and records requirements applicable to settlement documentation, fail records, and buy-in notices.

**FINRA rules governing settlement:**
- **Rule 11810** — Buy-in procedures for FINRA member firms, including notice requirements and execution procedures.
- **Rule 11860** — COD (Cash on Delivery) and DVP/RVP settlement procedures for institutional customers.
- **Rule 11870** — Customer account transfer contracts (ACAT); settlement of securities in transit during account transfers.
- **Rule 4210** — Margin requirements; interaction between margin obligations and settlement timing.
- **Rule 3110** — Supervision; requires supervisory systems reasonably designed to ensure compliance with settlement obligations and fail management.

**DTCC/NSCC/DTC rules and procedures:**
- **NSCC Rules & Procedures** — Govern trade submission, novation, CNS settlement, clearing fund requirements, default procedures, and loss allocation.
- **DTC Rules** — Govern participant accounts, book-entry transfers, settlement instruction processing, net debit caps, and reclaim/demand procedures.
- **NSCC Important Notices** — Published regularly to communicate changes to settlement procedures, risk management parameters, and operational deadlines.

### Settlement Timeline Reference (T+1 Equity Trade)

| Time | Event | Responsible Party |
|------|-------|-------------------|
| T (market hours) | Trade execution | Broker-dealer / Exchange |
| T (post-execution) | Trade reported to NSCC for clearing | Executing broker / Exchange |
| T (by 5:00 PM ET) | Investment manager sends allocation instructions | Investment manager |
| T (by 7:00 PM ET) | Broker-dealer sends confirmation to investment manager/custodian | Broker-dealer |
| T (by 9:00 PM ET) | Investment manager/custodian affirms trade (SDA target) | Investment manager / Custodian |
| T (evening) | NSCC novates trade; CNS netting begins | NSCC |
| T (night cycle) | DTC begins processing pre-matched institutional deliveries | DTC |
| T+1 (morning) | NSCC distributes balance orders to participants | NSCC |
| T+1 (morning) | Settlement bank funds participant's net cash obligation | Settlement bank |
| T+1 (business day) | DTC processes deliveries and receipts through day cycle | DTC / Participants |
| T+1 (end of day) | Unsettled trades become fails; carried forward in CNS | NSCC / DTC |
| T+3 (opening) | Rule 204 close-out deadline for standard equity fails | Participant with FTD |
| T+2 (opening) | Rule 204 close-out deadline for threshold securities | Participant with FTD |

## Worked Examples

Three worked examples are in [references/examples.md](references/examples.md) — load for an end-to-end scenario: (1) remediating a clearing firm's T+1 settlement operations (fail-rate and same-day-affirmation improvement), (2) resolving persistent counterparty fails through buy-ins and escalation, (3) designing settlement monitoring and fail escalation procedures.

## Common Pitfalls
- Failing to adjust operational workflows and staffing for T+1's compressed timeline — processes designed for T+2 cannot simply be accelerated; they must be redesigned for same-day completion
- Relying on manual allocation and affirmation processes for institutional trades, which are incompatible with the same-day affirmation requirements of T+1 settlement
- Not monitoring same-day affirmation rates as a leading indicator of settlement fail risk — a low affirmation rate on trade date almost certainly produces fails on settlement date
- Treating settlement fails as a routine operational matter rather than a risk management issue — persistent fails indicate counterparty, inventory, or operational problems that require root cause analysis
- Miscalculating Rule 204 close-out deadlines, particularly after the shift from T+2 to T+1, which changes the calendar math for mandatory buy-in dates
- Failing to account for corporate action processing in the settlement workflow — ex-date, record date, and CUSIP change events require proactive identification and manual intervention for pending settlements
- Not utilizing NSCC's Stock Borrow Program or other automated lending facilities to prevent CNS fails, instead relying solely on bilateral borrowing arrangements
- Ignoring the cash settlement side of the settlement equation — focusing on securities delivery while failing to monitor and manage the firm's daily cash settlement obligations to NSCC
- Failing to maintain current standing settlement instructions (SSIs) for institutional counterparties, leading to repeated instruction mismatches and avoidable fails
- Not establishing formal buy-in procedures and counterparty escalation protocols, resulting in ad hoc responses to fails that lack consistency and documentation
- Underestimating the operational impact of when-issued, extended settlement, and as-of trades, which require specialized handling outside the standard T+1 workflow
- Allowing DK'd trades to age without resolution — under T+1, a DK on trade date that is not resolved by the end of the day will almost certainly result in a settlement fail
- Failing to reconcile the firm's internal trade records against NSCC's balance order and DTC's settlement activity on a daily basis, allowing position discrepancies to accumulate and produce unexpected fails
- Not pre-funding foreign currency positions for cross-border settlements, creating FX funding gaps that delay settlement when the FX trade settles on T+2 but the equity trade settles on T+1
- Overlooking the impact of settlement fails on the firm's net capital computation — aged fails to deliver may require haircuts under SEC Rule 15c3-1, and significant fail positions can erode the firm's net capital cushion
- Treating securities lending and stock borrow transactions as separate from the settlement operations workflow, when in reality borrow recalls, collateral adjustments, and loan settlements are tightly coupled with the firm's delivery obligations
- Not testing settlement operations capacity and disaster recovery procedures for peak volume scenarios (index rebalancing, triple witching, month-end/quarter-end confluence), leading to settlement backlogs and elevated fail rates during predictable high-volume events

## Cross-References
- **order-lifecycle** (trading-operations plugin): The settlement process is the final stage of the order lifecycle — trade capture, allocation, and confirmation flow directly into settlement operations
- **trade-execution** (trading-operations plugin): Execution venue, trade capacity (principal vs. agency), and execution quality data feed into settlement instruction generation and fail analysis
- **counterparty-risk** (trading-operations plugin): Settlement fails are a manifestation of counterparty risk; pre-settlement exposure monitoring and counterparty credit limits directly affect settlement operations
- **operational-risk** (trading-operations plugin): Settlement operations are a primary domain of operational risk — system failures, processing errors, and capacity constraints all produce settlement disruptions
- **margin-operations** (trading-operations plugin): Margin requirements and clearing fund contributions at NSCC are calculated based on unsettled positions; settlement fails increase margin requirements
- **corporate-actions** (client-operations plugin): Corporate action processing intersects with settlement when ex-dates, record dates, or reorganization events affect pending deliveries
- **books-and-records** (compliance plugin): Settlement records — including delivery receipts, fail documentation, buy-in notices, and counterparty communications — are books and records subject to retention under SEC Rules 17a-3 and 17a-4
- **regulatory-reporting** (compliance plugin): FTD data, threshold securities lists, and CAT settlement-related reporting are regulatory reporting obligations that depend on accurate settlement operations data
- **reconciliation** (client-operations plugin): Daily reconciliation of internal trade records against NSCC balance orders and DTC settlement activity is the primary mechanism for detecting and preventing settlement discrepancies
- **liquidity-management** (wealth-management plugin): Intraday and overnight liquidity management directly supports the firm's ability to meet NSCC cash settlement obligations and respond to intraday margin calls
- **account-transfers** (client-operations plugin): ACAT transfers involve the movement of securities positions between clearing firms, requiring coordination of settlement obligations and pending trades during the transfer window
- **stp-automation** (client-operations plugin): Straight-through processing rates for settlement-related workflows (allocation, affirmation, matching, instruction generation) are the primary determinant of settlement efficiency under T+1
- **reference-data** (data-integration plugin): Accurate security master data (CUSIPs, settlement eligibility, corporate action flags) is foundational to settlement instruction generation and fail prevention
- **equities** (wealth-management plugin): Equity market structure concepts — including market microstructure, short selling mechanics, and exchange trading protocols — provide the context for understanding settlement obligations arising from equity trade execution

### Referencia: references/examples.md

# Settlement & Clearing — Worked Examples

### Example 1: Managing settlement operations for a clearing firm handling T+1 settlement
**Scenario:** A mid-sized clearing firm that clears for 45 introducing broker-dealers is evaluating its settlement operations six months after the T+1 transition. The firm is experiencing a settlement fail rate of 4.2% by value (industry average is approximately 2.5%), with the majority of fails concentrated in institutional trades processed through DTC's institutional delivery system. The firm's same-day affirmation rate is 78% (industry target is 90%+). The firm's operations team has identified three primary drivers of fails: (1) late allocation instructions from investment managers, (2) mismatched settlement instructions between broker-dealers and custodians, and (3) insufficient inventory in hard-to-borrow securities.

**Analysis:**
The firm should address each driver systematically:

(1) **Late allocation instructions.** Under T+2, investment managers had until the morning of T+1 to submit allocation instructions, leaving the afternoon and evening for matching and affirmation. Under T+1, allocations must be received on trade date — ideally by 5:00 PM ET on T to allow time for matching and affirmation by the 9:00 PM ET same-day affirmation target. The firm should: (a) Communicate allocation deadlines to all correspondent broker-dealers and their institutional clients, with clear escalation procedures for late allocations. (b) Implement automated allocation messaging through DTCC's CTM platform or FIX protocol connections with investment managers. Manual allocation processes (phone, email, fax) are incompatible with T+1 timelines. (c) Work with investment managers to adopt standing settlement instructions (SSIs) that reduce the data required in each allocation. SSIs pre-define the custodian, DTC participant number, and account identifiers for each investment manager's accounts, eliminating a major source of errors and delays. (d) Monitor allocation timeliness metrics daily and flag investment managers whose late allocations contribute disproportionately to fails.

(2) **Mismatched settlement instructions.** Settlement instruction mismatches — where the broker-dealer's instructions do not match the custodian's expectations for DTC participant number, account number, or quantity — are a persistent source of fails. The firm should: (a) Implement pre-matching validation that compares outgoing settlement instructions against a database of known custodian settlement details before submission to DTC. (b) Subscribe to DTCC's ALERT (Account Level Enrichment and Transformation) system, which maintains a centralized database of standing settlement instructions and automatically enriches trade instructions with the correct settlement details. (c) Establish direct connectivity with the major custodians (State Street, BNY Mellon, JPMorgan, Northern Trust, Citibank) for real-time instruction matching and exception resolution. (d) Analyze the mismatch patterns — if a specific custodian or set of accounts is responsible for a disproportionate share of mismatches, engage the custodian directly to resolve the systemic issue.

(3) **Insufficient inventory in hard-to-borrow securities.** For short sales and certain principal transactions, the firm may not hold sufficient inventory to settle. The firm should: (a) Enhance its securities lending desk's pre-settlement locate process to ensure borrows are confirmed before settlement date. (b) Implement an automated fail-prevention system that identifies pending short deliveries on the morning of settlement date and initiates borrows from the firm's lending counterparties or through DTC's SBP (Stock Borrow Program). NSCC's Stock Borrow Program is an automated lending facility that allows participants to borrow securities from a pool of lendable positions to cover CNS delivery obligations. (c) Monitor Rule 204 close-out obligations and ensure that aged fails are closed out within the required timeframes to avoid pre-borrow restrictions.

The firm should set quantitative targets: reduce fail rate from 4.2% to under 2.5% within 90 days, achieve same-day affirmation rate of 90% within 60 days, and establish real-time monitoring dashboards that track fail rates by correspondent, by security, and by cause category. The firm should also consider the financial impact of its elevated fail rate — each fail generates NSCC fail charges, potential buy-in costs, and increased clearing fund requirements (NSCC's risk model penalizes participants with poor settlement performance by increasing their required clearing fund contributions). Quantifying these costs provides the business case for the operational investments needed to reduce the fail rate.

The clearing firm should also review its clearing agreements with each introducing broker-dealer to ensure that the agreements allocate settlement-related costs (fail charges, buy-in losses, margin call costs) appropriately. Some clearing agreements require the introducing broker-dealer to indemnify the clearing firm for costs arising from its clients' settlement failures, while others leave the clearing firm bearing the risk. Under T+1, the clarity and enforceability of these contractual provisions has become more important as the compressed timeline leaves less room for informal resolution.

### Example 2: Resolving a pattern of persistent settlement fails with a specific counterparty
**Scenario:** A broker-dealer's settlement operations team has identified a pattern of persistent fails with a single counterparty — a mid-tier broker-dealer that clears through a third-party clearing firm. Over the past 60 days, the counterparty has failed to deliver on 23 trades across 14 securities, with aggregate fail value of $18.7 million. The fails span both equity and corporate bond trades. Aging analysis shows that 8 of the 23 fails are over 10 business days old, and 3 are over 20 days old. The counterparty has not responded substantively to repeated fail inquiries. The broker-dealer's inventory is not at risk (these are all fail-to-receive positions — the counterparty owes delivery), but the firm is concerned about the counterparty's financial condition and the operational impact on its clients who are awaiting delivery.

**Analysis:**
The firm should pursue a structured escalation that addresses both the immediate fails and the underlying counterparty risk:

(1) **Immediate fail resolution — mandatory buy-in.** For fails that have exceeded the Rule 204 close-out deadline, the firm has the right (and in some cases the obligation) to execute a buy-in. A buy-in involves purchasing the owed securities in the open market and charging the cost to the failing counterparty. The firm should: (a) Issue formal buy-in notices to the counterparty for all fails that have exceeded Rule 204 deadlines, specifying the security, quantity, and the date by which the counterparty must deliver before the buy-in is executed. FINRA Rule 11810 governs buy-in procedures for FINRA member firms and requires at least two business days' notice before executing a buy-in. (b) Execute the buy-in for any fails where the counterparty does not deliver after receiving proper notice. Document the buy-in execution (price, quantity, date, market conditions) and invoice the counterparty for any price differential and associated costs. (c) For corporate bond fails, consider whether partial delivery is acceptable to the firm's clients, and whether partial buy-ins are operationally feasible given the bond's liquidity.

(2) **Counterparty risk assessment.** The pattern of persistent fails — particularly the 20+ day aged fails and the counterparty's non-responsiveness — raises concerns about the counterparty's operational and financial condition. The firm should: (a) Escalate the matter from operations to the firm's credit risk and counterparty risk teams. Request updated financial information from the counterparty (audited financial statements, net capital computation if the counterparty is a broker-dealer). (b) Check public sources for signs of distress — FINRA BrokerCheck for any recent regulatory actions, FOCUS report data (if available), press reports, or industry intelligence. (c) Review the firm's exposure to the counterparty across all business lines (not just settlement fails — also consider unsettled trades in the pipeline, open repo positions, securities lending exposure, and any credit extensions). (d) Consider reducing or suspending new trade activity with the counterparty until the fail pattern is resolved. The firm's credit risk policy should define thresholds at which counterparty activity is restricted.

(3) **Clearing firm escalation.** Since the counterparty clears through a third-party clearing firm, the clearing firm is the guarantor of the counterparty's settlement obligations under the clearing agreement. The firm should: (a) Notify the counterparty's clearing firm of the persistent fail pattern and the firm's intention to execute buy-ins. The clearing firm may have leverage to compel its correspondent to deliver or may be able to facilitate deliveries from its own inventory. (b) If the clearing firm is unresponsive, escalate to NSCC's participant services — NSCC monitors participant settlement performance and may take action against participants with excessive fail rates.

(4) **Client communication and impact mitigation.** The firm should communicate with affected clients whose deliveries are delayed, explain the fail resolution process, and provide estimated delivery timelines based on the buy-in schedule. If clients need the securities urgently (for example, to meet their own delivery obligations or to exercise corporate action rights), the firm may need to source the securities independently and charge the counterparty for the additional cost.

(5) **Documentation and regulatory preparedness.** Throughout the escalation process, the firm must maintain detailed records of all communications with the counterparty (dates, contact persons, content of discussions), all buy-in notices and executions, the financial impact of each fail (market value changes, accrued interest adjustments, fail charges incurred), and the risk assessment of the counterparty. These records serve multiple purposes: they support any claims against the counterparty for damages, they demonstrate to regulators that the firm actively managed the settlement risk, and they provide evidence for FOCUS report preparation (fails to deliver and fails to receive are reported on the FOCUS report). If the counterparty's pattern of fails is ultimately attributable to financial distress or fraud, the firm's contemporaneous documentation may be requested by FINRA, the SEC, or SIPC in connection with the counterparty's wind-down or liquidation.

### Example 3: Designing settlement monitoring and fail escalation procedures
**Scenario:** A newly formed clearing firm is building its settlement operations infrastructure from scratch and needs to design a comprehensive settlement monitoring and fail escalation framework. The firm expects to clear for 20 introducing broker-dealers with combined daily settlement volume of approximately 15,000 equity trades and 2,000 fixed-income trades. The firm's COO has asked the operations team to design a settlement monitoring system that provides real-time visibility into settlement status, identifies potential fails before settlement date, and implements a structured escalation process for fails that do occur.

**Analysis:**
The settlement monitoring and escalation framework should include the following components:

(1) **Pre-settlement monitoring (T to S-1).** The goal of pre-settlement monitoring is to identify trades at risk of failing before the settlement date, allowing time for corrective action. The system should track: (a) **Affirmation status** — all institutional trades must be affirmed by 9:00 PM ET on trade date. Unaffirmed trades by 5:00 PM ET should be flagged for immediate follow-up with the investment manager and custodian. Trades that remain unaffirmed by the cutoff should be escalated to a senior operations manager. (b) **Inventory availability** — for all net short CNS positions (where the firm owes delivery), the system should compare the delivery obligation against available inventory (DTC position, pending receipts from other settlements, confirmed borrows). Any shortfall should trigger an automated alert to the securities lending desk. (c) **Settlement instruction validation** — all outgoing deliver orders should be pre-validated against the counterparty's known settlement details (DTC participant number, account, sub-account). Mismatched instructions should be flagged for correction before submission. (d) **Corporate action impact** — the system should identify any pending settlements in securities undergoing corporate actions (ex-date processing, CUSIP changes, mergers) and route them to a specialized corporate actions settlement queue for manual review.

(2) **Settlement date monitoring (S).** On the settlement date itself, the system should provide real-time tracking of: (a) **DTC settlement activity** — monitor deliveries and receipts as they process through DTC, comparing actual activity against expected settlements. The system should display settlement completion rates by hour, flagging any participant or security where settlement is lagging. (b) **Cash settlement** — monitor the firm's net cash obligation to NSCC and confirm that the settlement bank has sufficient funds to meet the obligation by the NSCC payment deadline. Cash shortfalls must be escalated immediately to treasury. (c) **Partial deliveries** — track partial deliveries received and delivered, and calculate remaining obligations for each trade. (d) **Fail identification** — at the end of the settlement day, identify all trades that did not settle and classify them by cause (inventory shortfall, unaffirmed trade, instruction mismatch, counterparty fail, corporate action, other).

(3) **Post-settlement fail escalation.** Fails that occur despite pre-settlement monitoring require structured escalation based on age and value:
- **Day 1 (S+1):** Operations staff contacts the counterparty or correspondent to identify the cause and obtain an estimated delivery date. Internal inventory check to determine if the firm can cover the position through its own borrow or locate.
- **Day 2 (S+2):** If unresolved, escalation to a senior operations manager. Formal written notice sent to the counterparty. For short-sale related fails, confirm that the Rule 204 close-out clock has started and calculate the mandatory close-out date.
- **Day 3-5 (S+3 to S+5):** For fails approaching or exceeding Rule 204 close-out deadlines, initiate the buy-in process (issue buy-in notice per FINRA Rule 11810). Notify compliance of the fail and the planned close-out. Update the firm's fail aging report and counterparty risk metrics.
- **Day 6-10 (S+6 to S+10):** Execute buy-ins for any fails that have not been resolved. Escalate persistent counterparty fails to the credit risk team. Notify affected clients if their account positions are impacted.
- **Day 10+ (S+10+):** Invoke counterparty risk review. Consider restricting new business with the failing counterparty. Report aged fails to FINRA if required. Senior management briefing on the fail and its financial and reputational impact.

(4) **Reporting and metrics.** The system should generate daily settlement reports including: total trades settled vs. failed (by count and value), fail rate by correspondent broker-dealer, fail rate by security and asset class, aging distribution of open fails, same-day affirmation rates, average fail duration, and buy-in activity. Weekly and monthly trend reports should be provided to the COO and chief compliance officer. Fail rate thresholds should be established — for example, if the firm's overall fail rate exceeds 3% by value for three consecutive business days, a senior management review is triggered.

(5) **Regulatory compliance integration.** The monitoring system must support regulatory reporting requirements: daily FTD data for potential SEC reporting, threshold securities monitoring for Reg SHO compliance, CAT reporting of settlement-related events (where applicable), and FOCUS report data for the settlement-related line items (fails to deliver and fails to receive). The system should also maintain an audit trail of all escalation actions, counterparty communications, and buy-in executions for examination readiness.

(6) **Technology architecture considerations.** The settlement monitoring system should be designed with the following architectural principles: (a) **Real-time data ingestion** — the system must consume data from multiple sources in near-real-time, including NSCC balance orders, DTC settlement activity feeds, the firm's order management system (OMS), the firm's securities lending system, and the firm's cash management system. Batch processing on an overnight basis is insufficient for T+1 settlement monitoring; the system must process data continuously throughout the business day. (b) **Alerting and notification** — the system should generate automated alerts via multiple channels (email, dashboard, SMS/messaging for critical escalations) based on configurable thresholds. Alert fatigue must be managed by tuning thresholds and prioritizing alerts based on financial impact and regulatory urgency. (c) **Workflow management** — fail resolution requires coordination across multiple teams (operations, securities lending, treasury, compliance, and client service). The system should include a workflow engine that routes fails to the appropriate team, tracks resolution status, and enforces escalation timelines. (d) **Historical data and analytics** — the system should retain historical settlement data for trend analysis, counterparty performance scoring, and regulatory examination support. Fail pattern analysis (by security, counterparty, cause, time of day) can identify systemic issues that are not visible in daily operational reports.

(7) **Staffing and operating model.** The firm should plan for a settlement operations team structured around three functions: (a) a pre-settlement team responsible for monitoring affirmation status, inventory availability, and settlement instruction quality during the afternoon and evening of trade date; (b) a settlement day team responsible for monitoring DTC and NSCC activity, resolving intraday exceptions, and managing the cash settlement process; and (c) a fail resolution team responsible for post-settlement fail management, counterparty communication, buy-in execution, and regulatory reporting. Under T+1, the pre-settlement function extends into the evening hours on trade date, which may require shift scheduling or follow-the-sun arrangements for firms with global operations. The firm should also designate a senior settlement officer who has authority to approve buy-ins, escalate counterparty issues to credit risk, and communicate with NSCC and DTC on participant-level settlement issues.


---

## SKILL: stp-automation

- Fuente: `JoelLewis/finance_skills` → `plugins/client-operations/skills/stp-automation` (MIT)
- Cuándo usarla: Measure and raise straight-through processing (STP) rates in securities operations through zero-touch, exception-based processing. Use when measuring STP rates and analyzing manual touchpoints in an existing process, replacing review-all workflows with exception-based processing, evaluating RPA vs API-based vs hybrid automation for legacy systems, building exception queuing, categorization, and auto-resolution workflows, conducting process mining or root cause analysis on exception volumes, or setting STP rate targets and continuous improvement programs. For approval chains, four-eyes controls, and SLA monitoring, see workflow-automation.

# STP & Automation

## Core Concepts

### 1. STP Fundamentals

Straight-through processing is the end-to-end automated completion of a business process without manual intervention: a transaction enters the system at one end and exits as a completed, booked, and confirmed event at the other with no human touching it along the way. True STP means zero manual intervention for the happy path; a process with a human review or approval at a midpoint is partially automated, not STP.

**STP rate calculation.** The fundamental metric is:

```
STP Rate = Automated Completions / Total Volume * 100
```

An "automated completion" is a transaction or workflow instance that passed through every step without manual intervention. If a trade requires a human to confirm a counterparty identifier before it can settle, that trade is not STP even though every other step was automated. The denominator is total volume, including both automated and exception items.

**Industry benchmarks by process type.** STP rates vary significantly by domain and firm maturity:
- Equity trade processing (listed, domestic): 90-98% for mature firms
- Fixed income trade processing: 70-85% (lower due to less standardized identifiers and settlement conventions)
- Account opening (simple individual/joint accounts): 60-80%
- Account opening (complex entity/trust accounts): 20-40%
- Corporate actions (mandatory events): 80-90%
- Corporate actions (voluntary events): 30-50%
- Reconciliation (position and cash): 85-95% auto-match rates
- Settlement instruction matching: 75-90%

These ranges reflect the spectrum from mid-tier broker-dealers to large custodian banks. A firm's position within the range depends on data quality, system integration maturity, and the complexity of its product mix.

**The business case for STP** compounds across four dimensions: cost reduction (per-transaction labor cost becomes fixed infrastructure cost), speed (seconds instead of queuing and handoff delays — directly reducing settlement risk), error reduction (consistent rules instead of re-keying and judgment variance), and scalability (volume spikes at quarter-end or corporate action clusters do not require proportional staffing).

### 2. STP Architecture

Building STP capability requires five architectural layers that work in concert. A weakness in any layer breaks the chain and forces manual intervention.

**Data standardization.** This is the foundation. STP fails when systems disagree on how to represent the same entity. Standardization encompasses:
- **Identifiers.** Security identifiers (CUSIP, ISIN, SEDOL, ticker), counterparty identifiers (LEI, DTCC participant number, BIC/SWIFT code), account identifiers (custodian account number, internal account ID). Every system in the chain must resolve to the same identifier for the same entity.
- **Formats.** Date formats (ISO 8601), currency codes (ISO 4217), country codes (ISO 3166), quantity representations (whole shares vs. fractional, signed vs. unsigned), price formats (decimal vs. fraction for fixed income).
- **Reference data.** A golden source for security master data, counterparty data, and account data that all systems consume. Discrepancies in reference data are the single largest source of STP breaks.
- **Messaging standards.** FIX protocol for trade messages, SWIFT for settlement instructions, ISO 20022 for payments and corporate actions. Adoption of industry-standard messaging reduces translation errors.

**Validation rules.** At each step in the process, the system applies automated checks to confirm the data is complete, consistent, and within expected parameters:
- **Completeness checks.** All required fields populated (e.g., a settlement instruction must have settlement date, security identifier, quantity, counterparty, settlement location).
- **Format checks.** Values conform to expected formats (dates are valid, amounts are numeric, identifiers match expected patterns).
- **Cross-field checks.** Logical consistency between fields (settlement date is after trade date, quantity and side agree with the net money calculation, currency matches the security's denomination).
- **Range checks.** Values fall within acceptable ranges (price is within a tolerance of the last known price, quantity does not exceed position, settlement date is within the standard settlement cycle).
- **Referential checks.** Referenced entities exist in the system (the security is in the security master, the counterparty is in the counterparty database, the account is active).

**Routing rules.** Automated decision-making that directs a transaction through the correct processing path without human judgment:
- **Product-based routing.** Equities route to equity settlement, fixed income to fixed income settlement, derivatives to derivatives processing.
- **Market-based routing.** Domestic trades route to domestic settlement systems, international trades route to global custody.
- **Counterparty-based routing.** Trades with certain counterparties route to specialized queues or systems (e.g., prime brokerage trades, DVP vs. free delivery).
- **Threshold-based routing.** Transactions above a dollar or quantity threshold route to a senior review queue. Transactions below the threshold process automatically.
- **Regulatory routing.** Transactions subject to specific regulatory requirements (ERISA, OFAC screening, Reg SHO locate) route through the appropriate compliance check.

**Exception handling.** When a transaction fails validation or cannot be routed automatically, the system must identify the exception, categorize it, and route it to the appropriate resolution queue. This is the boundary between STP and manual processing. The goal is to make the exception boundary as narrow as possible, handling as many edge cases automatically as the risk tolerance permits.

**Status tracking.** Automated monitoring of every transaction's progress through the process. Each step in the workflow updates a status record. Status tracking enables real-time dashboards, automated escalation when items age beyond thresholds, and end-of-day completeness reporting.

### 3. Exception-Based Processing

The foundational shift in operations efficiency is moving from a review-all model (every transaction is reviewed by a human) to a review-exceptions model (only transactions that fail automated validation are reviewed by a human).

**Exception categorization.** Effective exception management requires a taxonomy of exception types:
- **Data quality exceptions.** Missing data, invalid formats, unrecognized identifiers. These are preventable with better upstream data management and are the highest-priority targets for STP improvement.
- **Validation failure exceptions.** Transactions that fail cross-field, range, or referential checks. Examples: price tolerance breach, unmatched settlement instructions, quantity exceeding position.
- **Rule violation exceptions.** Transactions that violate business rules or compliance rules. Examples: concentration limit breach, restricted security trade, unapproved counterparty.
- **System error exceptions.** Technical failures — timeout, connectivity loss, message parsing error. These are infrastructure issues, not business logic issues.
- **Timing exceptions.** Transactions that arrive too late for same-day processing, miss a cutoff, or reference a future-dated event that cannot yet be processed.

**Exception queuing and prioritization.** Exceptions are routed to work queues organized by type, severity, and urgency. Prioritization factors include:
- Settlement date proximity (items settling today or tomorrow are highest priority)
- Dollar value (larger transactions carry more financial risk if unresolved)
- Counterparty SLA requirements (some counterparties have contractual resolution timeframes)
- Regulatory deadlines (e.g., T+1 settlement compliance, corporate action election deadlines)
- Aging (items that have been in the queue longer receive escalating priority)

**Exception resolution workflows.** Each exception category has a defined resolution procedure:
1. The resolver opens the exception and reviews the details.
2. The system presents the likely root cause based on the exception category and historical patterns.
3. The resolver takes corrective action (amends data, contacts the counterparty, overrides with documentation, cancels and rebooks).
4. The corrected transaction re-enters the automated flow from the point of failure.
5. The resolution is logged with the action taken, the resolver's identity, and the timestamp.

**Auto-resolution rules.** For well-understood, low-risk exception categories, the system can apply automated resolution without human intervention. Examples:
- If a security identifier is missing but can be derived from other fields (e.g., ticker + exchange uniquely identifies a CUSIP), auto-populate and re-process.
- If a settlement instruction mismatch is within a defined tolerance (e.g., accrued interest difference of less than $1.00), auto-match.
- If a price tolerance breach is caused by a stale reference price, auto-update the reference price from the market data feed and re-validate.

Auto-resolution rules require careful governance. Each rule must be documented with its rationale, risk assessment, approval authority, and periodic review schedule.

**Exception metrics.** Key measurements for exception management:
- **Exception volume.** Total exceptions per period, broken down by category. Trend analysis reveals whether STP is improving or degrading.
- **Exception rate.** Exceptions as a percentage of total volume. The inverse of the STP rate.
- **Aging distribution.** How long exceptions remain unresolved. A healthy queue has most items resolved same-day. Items aging beyond one day require escalation.
- **Resolution time.** Average and median time from exception creation to resolution. Broken down by category to identify which types are slowest to resolve.
- **Repeat exceptions.** Transactions or counterparties that generate the same exception repeatedly. These are the highest-value targets for root cause remediation.
- **Auto-resolution rate.** The percentage of exceptions resolved by auto-resolution rules without human intervention. A sub-STP metric that measures the effectiveness of the auto-resolution layer.

### 4. Process Automation Patterns

Different operational contexts call for different automation approaches. The patterns below are listed from simplest to most sophisticated.

**Rule-based automation.** If-then logic applied to structured data. The most common and most reliable form of automation. Examples: if the trade is a listed equity with a recognized counterparty and standard settlement terms, route directly to settlement. If the account opening application has all required fields populated and KYC verification passes, submit to the custodian. Rule-based automation is deterministic, auditable, and easy to explain to regulators.

**Template-based automation.** Standardized output generation from variable inputs. Examples: generating settlement instructions from trade data using a counterparty-specific template, producing client reports by populating a template with account data, creating regulatory filings by mapping internal data to the required format. Templates reduce errors by eliminating free-form composition.

**Workflow automation.** Multi-step orchestrated processes where the completion of one step triggers the next. A workflow engine manages the sequence, handles branching logic (if step 3 fails, route to exception handling; if step 3 succeeds, proceed to step 4), and tracks status. Workflow automation is the backbone of STP — it connects individual automated steps into an end-to-end chain.

**Robotic process automation (RPA).** Software bots that interact with application user interfaces the same way a human would — clicking buttons, entering data into fields, reading screen values, navigating menus. RPA is the automation pattern of last resort, used when:
- The target system has no API or file-based integration option
- The system is a legacy application that cannot be modified
- The integration is temporary (bridging until a proper API is built)
- The volume does not justify the cost of building a native integration

RPA is brittle — UI changes break the bot — and requires ongoing maintenance. It is a pragmatic solution, not an architectural one.

**API-based automation.** System-to-system communication through defined interfaces. The gold standard for integration because it is structured, versioned, documented, and testable. REST APIs, SOAP web services, and FIX protocol connections all fall in this category. API-based automation enables real-time, synchronous processing (request-response) or asynchronous processing (fire-and-forget with callback or polling).

**Machine learning-assisted automation.** Classification, anomaly detection, and pattern recognition applied to operational data. Examples: classifying incoming corporate action notices by event type, detecting anomalous settlement fails that may indicate a counterparty issue, predicting which exception items are likely to auto-resolve vs. require human attention. ML-assisted automation augments rule-based processing by handling cases where rules are too complex to enumerate or where patterns evolve over time.

### 5. STP by Operations Domain

Each operations domain has distinct STP characteristics, challenges, and success factors.

**Account opening STP.** From application receipt through funded, active account. NIGO taxonomy, pre-submission validation, document requirements matrices, and custodian submission design are covered in account-opening-workflow; apply the measurement and exception-management framework in this skill to the targets defined there (60-80% STP for simple individual/joint accounts, 20-40% for complex entity/trust accounts).

**Trade processing STP.** From trade execution through allocation, confirmation, and booking. Key STP challenges: block trade allocation complexity, counterparty confirmation matching, non-standard settlement terms, late trade reporting, manual enrichment of trade details. Success factors: standardized allocation rules, automated confirmation matching (CTM, ALERT), reference data quality for securities and counterparties, real-time trade validation against compliance rules.

**Settlement STP.** From trade booking through delivery/receipt of securities and funds. Key STP challenges: settlement instruction mismatches, fails due to insufficient securities or funds, cross-border settlement complexity (time zones, local market practices, CSD requirements), partial settlement decisions. Success factors: SSI (standing settlement instruction) databases, automated matching engines, pre-settlement position checks, proactive fail management.

**Corporate actions STP.** From event notification through entitlement calculation and booking. Key STP challenges: unstructured event notifications (narrative-format announcements), complex event types (mergers with elections, rights issues, spin-offs with fractional shares), tight election deadlines, multi-custodian entitlement reconciliation. Success factors: ISO 20022 event messaging, automated scrubbing of event data, rule-based entitlement calculation for mandatory events, automated deadline tracking.

**Reconciliation STP.** Automated matching of internal records against custodian and counterparty records. Auto-match rate benchmarks, matching rule design, break categorization, and tolerance thresholds are covered in reconciliation; that skill owns the auto-match content, and reconciliation also serves as the primary detective control over every other STP domain.

**Reporting STP.** Automated generation and delivery of regulatory reports, client reports, and management reports. Key STP challenges: data aggregation from multiple sources, format requirements that change with regulatory updates, exception handling for missing or inconsistent data, delivery failures (email bounce, portal upload error). Success factors: data warehouse with validated, reconciled data, template-based report generation, automated delivery with confirmation tracking, exception-based review (only review reports that fail validation).

**Billing STP.** Automated fee calculation, debit instruction generation, and revenue booking. Key STP challenges: complex fee schedule structures (tiered, breakpoint, negotiated), mid-period account events requiring proration, held-away asset valuation, custodian debit file format variations. Success factors: centralized fee schedule repository, automated valuation sourcing, rule-based proration, custodian-specific file generation, automated reconciliation of debit confirmations.

### 6. Integration Patterns for Operations

Operations systems do not function in isolation. The integration architecture determines how data flows between systems and directly impacts STP rates.

**Real-time API integration.** Synchronous request-response communication. Best for: trade execution, compliance checks, KYC verification, position queries, price lookups. Characteristics: immediate feedback, tight coupling between systems, requires both systems to be available simultaneously, latency-sensitive.

**Message queue / event-driven processing.** Asynchronous communication through a message broker (e.g., Kafka, RabbitMQ, MQ Series). Best for: trade notifications, status updates, corporate action announcements, settlement confirmations. Characteristics: loose coupling, guaranteed delivery, natural buffering during volume spikes, supports publish-subscribe patterns where multiple consumers process the same event.

**Batch file processing.** Periodic exchange of files (CSV, fixed-width, XML) on a scheduled basis. Best for: end-of-day position files, custodian reconciliation files, billing files, regulatory report files. Characteristics: simple to implement, well-understood by operations teams, introduces latency (data is only as current as the last batch), requires file monitoring and error handling for missing or corrupt files.

**Database-to-database integration.** Direct reading from or writing to another system's database. Best for: tightly integrated systems within the same technology stack. Characteristics: fast and flexible but creates tight coupling, bypasses the application logic layer (risky if business rules are enforced at the application level), complicates upgrades (schema changes break integrations).

**Screen scraping / RPA.** Automated interaction with another system's user interface. Best for: legacy systems without APIs, temporary bridging solutions, low-volume processes where the cost of building a proper integration is not justified. Characteristics: brittle (UI changes break the integration), slow (processes at human speed), difficult to scale, but sometimes the only option.

**Hybrid patterns.** Most real-world operations environments use a combination of patterns. A common architecture: real-time APIs for trade execution and compliance checks, message queues for inter-system event notifications, batch files for end-of-day reconciliation and custodian data feeds, RPA for legacy system interactions that cannot be replaced immediately.

**Error handling.** Every integration must account for failure using standard software resilience patterns — retries with backoff for transient errors, dead-letter routing for messages that exhaust retries, circuit breakers for failing downstream systems, and idempotent message processing so retries cannot create duplicate transactions. The operations-specific requirement is that no failed message may be silently dropped: every failure must surface in an exception queue with an owner.

### 7. Measuring and Improving STP Rates

**STP rate dashboards.** A real-time or near-real-time view of STP performance across all operations domains. The dashboard should display:
- Current-period STP rate by domain (account opening, trade processing, settlement, etc.)
- STP rate trend over time (daily, weekly, monthly)
- Exception volume breakdown by category
- Top exception generators (counterparties, security types, account types that cause the most exceptions)
- Aging distribution of open exceptions

**Process mining.** Analyzing actual process execution data (system logs, timestamps, user actions) to reconstruct how work actually flows through the organization. Process mining reveals:
- Which steps are automated vs. manual in practice (not just in theory)
- Where bottlenecks occur (steps with the longest average processing time)
- Rework loops (items that cycle back to a previous step)
- Deviation from the intended process (workarounds and ad hoc procedures)

**Bottleneck identification.** Using process mining and exception data to pinpoint the specific steps, rules, or data quality issues that cause the most STP breaks. The Pareto principle typically applies: 20% of root causes account for 80% of exceptions. Addressing the top root causes delivers outsized STP improvement.

**Root cause analysis of exceptions.** For each high-volume exception category, a structured investigation:
1. What is the exception? (Precise definition and example)
2. When does it occur? (Which step in the process, what time of day, what market conditions)
3. Why does it occur? (Data quality issue, missing reference data, rule too tight, system limitation)
4. How is it resolved today? (Manual workaround, data correction, override)
5. Can the root cause be eliminated? (Fix the upstream data, adjust the rule, enhance the system)
6. If not eliminated, can auto-resolution handle it? (Automated workaround with appropriate controls)

**Continuous improvement cycles.** STP improvement is iterative, not a one-time project. A standard cycle:
1. **Measure.** Establish current STP rates and exception profiles.
2. **Analyze.** Identify the top 3-5 exception categories by volume.
3. **Prioritize.** Rank by impact (volume times cost-per-exception) and feasibility.
4. **Implement.** Deploy the fix (data quality improvement, rule adjustment, new auto-resolution, system enhancement).
5. **Verify.** Confirm the exception volume decreases as expected.
6. **Repeat.** Move to the next set of exception categories.

**STP rate targets by process.** Setting realistic targets requires understanding current performance and industry benchmarks. A reasonable improvement cadence is 3-5 percentage points per quarter for processes below 80% STP, and 1-2 percentage points per quarter for processes above 80% (marginal gains become harder). Targets above 95% require significant investment in data quality and system integration and should be pursued only where the volume justifies the cost.

### 8. Operational Controls in Automated Environments

Automation does not eliminate the need for controls — it changes the nature of the controls from manual checks to automated monitoring and governance of the automation itself.

**Separation of duties in automated workflows.** The person who configures automation rules should not be the same person who approves them for production. Rule changes should follow a development-testing-approval-deployment cycle analogous to software release management.

**Audit trails.** Every automated action must be logged with sufficient detail to reconstruct what happened, when, why, and based on which rule. The audit trail must capture: the input data, the rule or logic applied, the decision made, the action taken, and the timestamp. This is non-negotiable for regulatory examination readiness.

**Automated monitoring and alerting.** Replace manual supervisory review with automated monitoring:
- **Volume monitoring.** Alert when transaction volumes deviate significantly from expected ranges (may indicate a system issue or market event).
- **STP rate monitoring.** Alert when the STP rate drops below a threshold (may indicate a data quality issue or system change).
- **Aging alerts.** Escalate exception items that exceed resolution time thresholds.
- **Reconciliation break alerts.** Escalate reconciliation breaks that exceed tolerance thresholds.
- **System health monitoring.** Monitor integration connectivity, message queue depths, batch file arrival times.

**Automated reconciliation as a control.** In an STP environment, reconciliation serves as the primary detective control. If the automated processing is producing correct results, reconciliation will confirm it. If something has gone wrong (a rule error, a data feed issue, a system defect), reconciliation will surface the discrepancy. Automated reconciliation — with automated matching, automated break categorization, and aging-based escalation — is the control framework that makes STP trustworthy.

**Change management for automation rules.** Rule changes are the highest-risk activity in an automated environment because a rule error can affect every transaction that passes through it. Change management must include:
- Documented business justification for the change
- Impact analysis (which transactions and volumes are affected)
- Testing in a non-production environment with representative data
- Approval by both operations management and compliance
- Deployment with rollback capability
- Post-deployment monitoring for unintended consequences

**Testing automation changes.** Before any rule change goes live, it must be tested against historical data to confirm that (a) it produces the correct result for the targeted exception category and (b) it does not break STP for previously automated items. Regression testing is essential.

**Regulatory expectations for automated controls.** Regulators (SEC, FINRA, OCC, Federal Reserve) expect firms to demonstrate that their automated processes are subject to governance, monitoring, and testing. Specific expectations include:
- Documented policies and procedures for automation governance
- Periodic validation that automated rules are functioning as intended
- Escalation procedures when automated controls detect anomalies
- Business continuity planning for automation failures (manual fallback procedures)
- Evidence of management oversight of automated processes (dashboard reviews, exception reports, STP rate discussions in operations committees)

## Worked Examples

A worked example — a 12-month STP improvement program for a broker-dealer's equity and fixed income trade processing (data quality remediation, integration upgrade, auto-resolution rules) — is in [references/examples.md](references/examples.md); load it when designing a concrete STP improvement roadmap.

### Account opening and reconciliation examples

For a worked example of exception-based account opening processing (tiered review, pre-submission validation, NIGO reduction), see account-opening-workflow. For worked examples of reconciliation auto-matching and break-reduction programs, see reconciliation.

## Common Pitfalls

- **Automating a bad process.** Automating manual steps without first redesigning the workflow embeds inefficiency permanently. Before automating, ask whether the step is necessary at all.
- **Measuring STP rate without a precise definition.** If "STP completion" is not rigorously defined, the metric becomes meaningless. Every domain needs a clear definition of what counts as automated versus manual.
- **Neglecting data quality as the root cause.** Most STP breaks trace back to data quality issues — missing identifiers, stale reference data, inconsistent formats. Investing in system enhancements without fixing data quality yields disappointing results.
- **Over-engineering auto-resolution rules.** Auto-resolution rules that are too aggressive (matching with loose tolerances, auto-correcting data without sufficient validation) introduce silent errors. Each rule needs a documented risk assessment.
- **Treating RPA as a permanent solution.** RPA is a tactical bridge, not a strategic architecture. Firms that build large RPA estates without a plan to replace bots with API integrations accumulate fragile, high-maintenance automation.
- **Ignoring the human side of automation.** Operations staff may resist STP initiatives if they perceive their roles as threatened. Successful programs reposition staff from manual processing to exception analysis, process improvement, and client service.
- **Deploying rule changes without regression testing.** A new rule that fixes one exception category may break STP for another. Every rule change must be tested against the full range of transaction types.
- **Setting unrealistic STP targets.** Targeting 99% STP for a process that handles complex, variable transactions (e.g., voluntary corporate actions, entity account openings) wastes resources. Set targets that reflect the inherent complexity of the process.
- **Failing to monitor automated processes.** Once a process is automated, there is a temptation to assume it works correctly. Without continuous monitoring, reconciliation, and alerting, errors in automated processes can persist undetected and compound.
- **Skipping the baseline measurement.** Launching improvement initiatives without knowing the current STP rate makes it impossible to demonstrate value or prioritize correctly.

## Cross-References

- **workflow-automation** (client-operations plugin) — Detailed patterns for multi-step workflow orchestration, state machines, and task routing that underpin STP implementations.
- **account-opening-workflow** (client-operations plugin) — End-to-end account opening process design, including the specific STP challenges and custodian integration requirements for new accounts.
- **reconciliation** (client-operations plugin) — Automated matching logic, break categorization, and resolution workflows that serve as both an STP domain and a control over other STP processes.
- **settlement-clearing** (trading-operations plugin) — Settlement instruction matching, fail management, and CSD/DTC integration patterns for trade settlement STP.
- **corporate-actions** (client-operations plugin) — Event processing, entitlement calculation, and election management workflows with their unique STP challenges.
- **operational-risk** (trading-operations plugin) — Risk framework for automated operations, including control design, incident management, and regulatory expectations for operational resilience.
- **portfolio-management-systems** (advisory-practice plugin) — PMS architecture, data feeds, and integration patterns that serve as the hub for many operations STP workflows.

### Referencia: references/examples.md

# STP & Automation — Worked Example

## Example 1: Designing an STP Framework for a Broker-Dealer's Trade Processing Operations

**Scenario.** A mid-size broker-dealer processes approximately 15,000 equity trades and 3,000 fixed income trades per day. Currently, the equity STP rate is 72% and the fixed income STP rate is 45%. The operations team of 28 people spends most of their time on manual exception handling. The COO has set a target of 90% equity STP and 70% fixed income STP within 12 months.

**Design Considerations:**
- The firm uses a legacy order management system (OMS) that generates trades in a proprietary format, a middle-office system that handles allocation and confirmation, and a back-office system that handles settlement and booking.
- The three systems communicate via batch files exchanged every 30 minutes during the trading day and hourly overnight.
- The most common equity exceptions are counterparty SSI mismatches (28% of exceptions), allocation discrepancies (22%), and late trade reporting by the trading desk (18%).
- The most common fixed income exceptions are security identifier mismatches (31%), non-standard settlement terms (24%), and manual enrichment requirements for structured products (19%).

**Analysis:**

Phase 1 — Data quality remediation (months 1-3). The highest-impact STP improvement comes from fixing the data, not changing the processing logic.

For equity counterparty SSI mismatches (28% of equity exceptions): audit the SSI database against the top 50 counterparties by volume. These 50 counterparties likely represent 80%+ of SSI-related breaks. Update stale or incorrect SSIs, establish a process for counterparties to confirm SSI changes proactively, and implement automated SSI validation against the DTCC ALERT database.

For fixed income security identifier mismatches (31% of fixed income exceptions): the root cause is typically that the OMS uses one identifier (e.g., CUSIP) while the counterparty uses another (e.g., ISIN). Implement a security master cross-reference service that maps between identifier types. When an incoming message uses an identifier type not stored in the system, the cross-reference service translates it automatically.

For allocation discrepancies (22% of equity exceptions): standardize allocation instructions. Require the trading desk to submit allocation instructions with the block trade rather than after the fact. Implement validation that allocation quantities sum to the block quantity and that all allocation accounts are valid and active.

Expected STP improvement from Phase 1: equity from 72% to 82%, fixed income from 45% to 58%.

Phase 2 — Integration upgrade (months 3-8). Replace the 30-minute batch file exchange between the OMS and middle-office system with a message queue (e.g., Kafka). This delivers several benefits:

- Trades flow to the middle office within seconds of execution rather than waiting up to 30 minutes for the next batch. This eliminates the late-trade-reporting exception category for all trades reported to the OMS in real time.
- Failed messages are retained in the queue and can be retried automatically, eliminating the manual file-reprocessing procedures.
- The message queue supports event-driven processing: when a trade message arrives, it immediately triggers allocation, enrichment, and confirmation workflows rather than waiting for a batch scheduler.

Implement a real-time API integration with the DTCC for trade confirmation matching, replacing the current end-of-day batch matching. This enables same-day confirmation matching and earlier identification of mismatches.

Expected STP improvement from Phase 2: equity from 82% to 88%, fixed income from 58% to 65%.

Phase 3 — Auto-resolution and rule enhancement (months 8-12). With the major data quality and integration issues addressed, the remaining exceptions are lower-volume, more varied, and require more nuanced resolution. Implement auto-resolution rules for the most common remaining exception types:

- For minor SSI field differences (e.g., abbreviated vs. full counterparty name), implement fuzzy matching with a confidence threshold. Matches above 95% confidence auto-resolve; below 95% route to manual review.
- For fixed income non-standard settlement terms: build a settlement convention library that maps security type, market, and counterparty to the expected settlement terms. Automatically apply the correct convention when the trade does not specify terms explicitly.
- For structured product enrichment: pre-load security master data for actively traded structured products so the system does not need manual enrichment when a trade in a known security arrives.

Implement STP rate dashboards with daily reporting to operations management. Establish a weekly exception review meeting where the top 5 exception categories from the prior week are analyzed and remediation actions assigned.

Expected STP improvement from Phase 3: equity from 88% to 91%, fixed income from 65% to 72%.

**Key success metrics for the 12-month program:**
- Equity STP rate: 72% to 91% (target 90% — achieved)
- Fixed income STP rate: 45% to 72% (target 70% — achieved)
- Daily manual exceptions: reduced from approximately 5,600 to approximately 2,000
- Operations headcount redeployed from exception handling to process improvement and controls: 8 of 28 staff


---

## SKILL: trade-accounting

- Fuente: `agiprolabs/claude-trading-skills` → `skills/trade-accounting` (MIT)
- Cuándo usarla: Double-entry bookkeeping for trading operations with ledger management, P&L statements, balance sheets, and cash flow reporting
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/trade-accounting/` (trading_ledger.py)

# Trade Accounting

Run your trading operation like a business. Every SOL spent, every token acquired, every fee paid, every gain realized — tracked with double-entry bookkeeping so your books always balance. Whether you trade through a personal wallet or an LLC, proper accounting turns chaos into clarity.

**Core principle**: Every transaction touches at least two accounts. Buy a token? Cash goes down, token holdings go up — by the same amount. This double-entry constraint catches errors automatically: if debits do not equal credits, something is wrong.

## Why Traders Need Accounting

Most traders track P&L loosely — "I started with 50 SOL and now I have 62 SOL." That tells you nothing about:

- How much came from realized trades vs unrealized positions
- What you paid in cumulative fees (gas, priority fees, swap fees)
- Whether your staking and LP income covers your operating costs
- Your actual cost basis for each holding (critical for taxes)
- Cash flow timing — are you profitable but illiquid?

Proper accounting answers all of these. It also separates **trading P&L** (mark-to-market, useful for strategy evaluation) from **tax P&L** (realized gains using a specific cost basis method, required for compliance).

---

## Account Types

A trading operation uses four account categories following standard accounting:

| Category | Normal Balance | Examples |
|----------|---------------|----------|
| **Assets** | Debit | Cash (SOL/USDC), token holdings, LP positions, staking deposits, receivables |
| **Liabilities** | Credit | Margin borrowing, accrued taxes payable |
| **Income** | Credit | Realized trading gains, staking rewards, airdrop income, LP fee income |
| **Expenses** | Debit | Trading fees, gas/priority fees, subscription costs, data feeds |
| **Equity** | Credit | Owner capital contributions, retained earnings, withdrawals (contra) |

### Chart of Accounts

See `references/planned_features.md` for a full chart of accounts. A minimal setup:

```
1000  Assets
  1010  Cash – SOL
  1020  Cash – USDC
  1100  Token Holdings (one sub-account per token)
  1200  LP Positions
  1300  Staking Deposits

3000  Income
  3010  Realized Trading Gains
  3020  Staking Rewards
  3030  Airdrop Income
  3040  LP Fee Income

4000  Expenses
  4010  Trading Fees (DEX swap fees)
  4020  Gas & Priority Fees
  4030  Slippage Cost

5000  Equity
  5010  Owner Capital
  5020  Retained Earnings
  5030  Owner Withdrawals (contra-equity)
```

---

## Double-Entry Bookkeeping

Every transaction records equal debits and credits. Debits increase asset and expense accounts; credits increase liability, income, and equity accounts.

### Entry Examples

**Buy 1000 BONK for 0.5 SOL (0.001 SOL gas fee):**

| Account | Debit | Credit |
|---------|-------|--------|
| Token Holdings – BONK | 0.501 SOL | |
| Cash – SOL | | 0.501 SOL |

Or with the fee broken out explicitly:

| Account | Debit | Credit |
|---------|-------|--------|
| Token Holdings – BONK | 0.5 SOL | |
| Gas & Priority Fees | 0.001 SOL | |
| Cash – SOL | | 0.501 SOL |

**Sell 1000 BONK for 0.8 SOL (cost basis was 0.5 SOL, 0.001 SOL gas):**

| Account | Debit | Credit |
|---------|-------|--------|
| Cash – SOL | 0.799 SOL | |
| Gas & Priority Fees | 0.001 SOL | |
| Token Holdings – BONK | | 0.5 SOL |
| Realized Trading Gains | | 0.3 SOL |

**Receive staking rewards of 0.05 SOL:**

| Account | Debit | Credit |
|---------|-------|--------|
| Cash – SOL | 0.05 SOL | |
| Staking Rewards | | 0.05 SOL |

**Receive airdrop of 5000 JUP (valued at 2.1 SOL at receipt):**

| Account | Debit | Credit |
|---------|-------|--------|
| Token Holdings – JUP | 2.1 SOL | |
| Airdrop Income | | 2.1 SOL |

**Collect LP fees of 0.03 SOL:**

| Account | Debit | Credit |
|---------|-------|--------|
| Cash – SOL | 0.03 SOL | |
| LP Fee Income | | 0.03 SOL |

**Partial close — sell half a position:**

If you hold 2000 BONK at cost basis 1.0 SOL and sell 1000 for 0.7 SOL:

| Account | Debit | Credit |
|---------|-------|--------|
| Cash – SOL | 0.699 SOL | |
| Gas & Priority Fees | 0.001 SOL | |
| Token Holdings – BONK | | 0.5 SOL |
| Realized Trading Gains | | 0.2 SOL |

The cost basis of the sold portion (0.5 SOL = half of 1.0 SOL) is removed from the asset account.

---

## Transaction Types

The ledger handles these trading flows:

| Flow | Accounts Touched |
|------|-----------------|
| Fund account | Cash (debit), Owner Capital (credit) |
| Withdraw funds | Owner Withdrawals (debit), Cash (credit) |
| Buy token | Token Holdings (debit), Cash (credit), Gas Expense (debit) |
| Sell token | Cash (debit), Token Holdings (credit), Realized Gains (credit or debit for loss), Gas Expense (debit) |
| Partial close | Same as sell, pro-rated cost basis |
| Swap token for token | Token B (debit), Token A (credit), fees |
| Staking deposit | Staking Deposits (debit), Cash (credit) |
| Staking reward | Cash (debit), Staking Rewards (credit) |
| Airdrop received | Token Holdings (debit), Airdrop Income (credit) |
| LP fee collected | Cash (debit), LP Fee Income (credit) |
| Trading fee | Trading Fees (debit), Cash (credit) |
| Gas/priority fee | Gas & Priority Fees (debit), Cash (credit) |

---

## Reports

### Profit & Loss Statement

Shows income minus expenses for a period:

```
═══════════════════════════════════════════
  P&L Statement: 2026-02-01 to 2026-02-28
═══════════════════════════════════════════
INCOME
  Realized Trading Gains ........  4.200 SOL
  Staking Rewards ...............  0.150 SOL
  Airdrop Income ................  2.100 SOL
  LP Fee Income .................  0.090 SOL
                                  ─────────
  Total Income                     6.540 SOL

EXPENSES
  Trading Fees ..................  0.120 SOL
  Gas & Priority Fees ...........  0.045 SOL
  Slippage Cost .................  0.030 SOL
                                  ─────────
  Total Expenses                   0.195 SOL

═══════════════════════════════════════════
  NET INCOME                       6.345 SOL
═══════════════════════════════════════════
```

### Balance Sheet

Shows the accounting equation: Assets = Liabilities + Equity.

```
═══════════════════════════════════════════
  Balance Sheet: 2026-02-28
═══════════════════════════════════════════
ASSETS
  Cash – SOL ....................  32.450 SOL
  Cash – USDC ...................   0.000 SOL
  Token Holdings ................  12.300 SOL
  LP Positions ..................   5.000 SOL
  Staking Deposits ..............  10.000 SOL
                                  ─────────
  Total Assets                    59.750 SOL

EQUITY
  Owner Capital .................  50.000 SOL
  Retained Earnings .............   3.405 SOL
  Net Income (current period) ...   6.345 SOL
                                  ─────────
  Total Equity                    59.750 SOL

═══════════════════════════════════════════
  Assets - Equity = 0.000 SOL  ✓ Balanced
═══════════════════════════════════════════
```

### Cash Flow Statement

Tracks where cash came from and where it went:

```
═══════════════════════════════════════════
  Cash Flow: 2026-02-01 to 2026-02-28
═══════════════════════════════════════════
OPERATING ACTIVITIES
  Trading proceeds ..............  8.500 SOL
  Token purchases ...............  (4.300) SOL
  Fees paid .....................  (0.195) SOL
  Staking rewards received ......  0.150 SOL
  LP fees received ..............  0.090 SOL
                                  ─────────
  Net Operating Cash Flow        4.245 SOL

INVESTING ACTIVITIES
  LP deposits ...................  (5.000) SOL
  Staking deposits ..............  (2.000) SOL
                                  ─────────
  Net Investing Cash Flow       (7.000) SOL

FINANCING ACTIVITIES
  Capital contributions .........  10.000 SOL
  Withdrawals ...................  (1.000) SOL
                                  ─────────
  Net Financing Cash Flow        9.000 SOL

═══════════════════════════════════════════
  Net Change in Cash              6.245 SOL
  Beginning Cash Balance         26.205 SOL
  Ending Cash Balance            32.450 SOL
═══════════════════════════════════════════
```

---

## Trading P&L vs Tax P&L

These are different numbers and serve different purposes:

| Aspect | Trading P&L | Tax P&L |
|--------|------------|---------|
| **Purpose** | Strategy evaluation | Compliance, filing |
| **Unrealized gains** | Included (mark-to-market) | Excluded (until realized) |
| **Cost basis method** | Average cost (simple) | FIFO, LIFO, or specific ID (jurisdiction-dependent) |
| **Timing** | Real-time | At disposal event |
| **Airdrops** | Valued at receipt | Ordinary income at FMV on receipt |
| **LP IL** | Tracked as unrealized loss | Not a taxable event until withdrawal |

The ledger in `scripts/trading_ledger.py` tracks realized gains using FIFO by default. For trading P&L, you can overlay mark-to-market valuations on open positions.

See `references/planned_features.md` for detailed worked examples of how the same trades produce different P&L under FIFO vs average cost.

---

## Entity Considerations

Traders operating through an LLC or S-Corp should track additional accounts:

- **Management fees** — if the entity charges a management fee
- **Distributions** — payments from entity to owner (not the same as withdrawals from a trading account)
- **Payroll expenses** — S-Corp officer salary
- **Tax provisions** — estimated quarterly tax payments

The accounting principles are identical; the chart of accounts simply expands. The scripts in this skill focus on the trading-level ledger, which is the foundation for entity-level reporting.

---

## Quick Start

```python
from trading_ledger import Ledger, Amount

ledger = Ledger(base_currency="SOL")

# Fund the account
ledger.record_funding(amount=50.0, memo="Initial capital")

# Buy a token
ledger.record_buy(
    token="BONK",
    quantity=100_000,
    cost_sol=0.5,
    fee_sol=0.001,
    memo="Entry on volume spike"
)

# Sell for profit
ledger.record_sell(
    token="BONK",
    quantity=100_000,
    proceeds_sol=0.8,
    fee_sol=0.001,
    memo="Target hit"
)

# Record staking reward
ledger.record_income(
    income_type="staking",
    amount_sol=0.05,
    memo="Epoch 580 rewards"
)

# Generate reports
ledger.print_pnl(start="2026-02-01", end="2026-02-28")
ledger.print_balance_sheet(as_of="2026-02-28")
```

Run the demo script to see a full month of trading activity with all report types:

```bash
python scripts/trading_ledger.py --demo
```

---

## Use Cases

1. **Track real P&L** — Know exactly how much you made after all fees, not just entry/exit prices
2. **Tax preparation** — Hand your accountant a clean ledger with cost basis and realized gains
3. **Fee analysis** — Discover that gas and priority fees are eating 3% of your gross profits
4. **Strategy comparison** — Compare net P&L across strategies, not just win rates
5. **Cash flow planning** — Know if you have enough liquid SOL for the next trade
6. **Audit trail** — Every number traces back to a dated, memo-tagged journal entry

---

## Prerequisites

- Python 3.10+
- No external dependencies (the ledger uses only the standard library)

---

## Files

| File | Description |
|------|-------------|
| `references/planned_features.md` | Chart of accounts, double-entry examples, report formats, trading vs tax P&L |
| `scripts/trading_ledger.py` | Double-entry ledger with P&L, balance sheet, and demo mode |

---

> **Disclaimer**: This skill provides accounting structure and calculations for informational and organizational purposes only. It is not tax advice, legal advice, or financial advice. Consult a qualified tax professional or CPA for guidance on your specific tax obligations. Cryptocurrency tax treatment varies by jurisdiction and changes frequently.

### Referencia: references/planned_features.md

# Trade Accounting — Reference Guide

## Chart of Accounts

A complete chart of accounts for a Solana trading operation:

```
1000  ASSETS
  1010  Cash – SOL
  1020  Cash – USDC
  1030  Cash – USDT
  1100  Token Holdings
    1101  Token Holdings – BONK
    1102  Token Holdings – JUP
    1103  Token Holdings – WIF
    (one sub-account per token held)
  1200  LP Positions
    1201  LP – SOL/USDC (Orca)
    1202  LP – SOL/BONK (Raydium)
  1300  Staking Deposits
    1301  Staked SOL (Marinade)
    1302  Staked SOL (Jito)
  1400  Receivables
    1401  Pending Airdrop Claims

2000  LIABILITIES
  2010  Margin Borrowing
  2020  Accrued Taxes Payable
  2030  Accounts Payable

3000  INCOME
  3010  Realized Trading Gains
  3020  Staking Rewards
  3030  Airdrop Income
  3040  LP Fee Income
  3050  Interest Income
  3060  Referral Income

4000  EXPENSES
  4010  Trading Fees (DEX swap fees)
  4020  Gas & Priority Fees
  4030  Slippage Cost
  4040  Data & Tool Subscriptions
  4050  Infrastructure Costs (RPC nodes)

5000  EQUITY
  5010  Owner Capital (contributions)
  5020  Retained Earnings (prior periods)
  5030  Owner Withdrawals (contra-equity, debit balance)
```

### Sub-Account Convention

Token holdings use dynamic sub-accounts. When you buy a new token for the first time, create account `1100 + next_id`. The ledger script handles this automatically.

---

## Double-Entry Examples

### Example 1: Full Trade Lifecycle

Starting state: 50 SOL in cash, no positions.

**Day 1 — Buy 500,000 BONK for 2.0 SOL + 0.002 SOL gas:**

| # | Account | Debit | Credit |
|---|---------|-------|--------|
| 1 | 1101 Token Holdings – BONK | 2.000 | |
| 2 | 4020 Gas & Priority Fees | 0.002 | |
| 3 | 1010 Cash – SOL | | 2.002 |

Cash: 47.998. BONK holding: 2.000 (cost basis).

**Day 3 — Sell 250,000 BONK for 1.5 SOL + 0.002 SOL gas:**

Cost basis of sold portion: 2.000 * (250,000 / 500,000) = 1.000 SOL.
Realized gain: 1.5 - 1.0 = 0.5 SOL.

| # | Account | Debit | Credit |
|---|---------|-------|--------|
| 1 | 1010 Cash – SOL | 1.498 | |
| 2 | 4020 Gas & Priority Fees | 0.002 | |
| 3 | 1101 Token Holdings – BONK | | 1.000 |
| 4 | 3010 Realized Trading Gains | | 0.500 |

Cash: 49.496. BONK holding: 1.000 (remaining cost basis).

**Day 5 — Sell remaining 250,000 BONK for 0.8 SOL + 0.002 SOL gas:**

Cost basis: 1.000 SOL. Realized loss: 0.8 - 1.0 = -0.2 SOL.

| # | Account | Debit | Credit |
|---|---------|-------|--------|
| 1 | 1010 Cash – SOL | 0.798 | |
| 2 | 4020 Gas & Priority Fees | 0.002 | |
| 3 | 3010 Realized Trading Gains | 0.200 | |
| 4 | 1101 Token Holdings – BONK | | 1.000 |

Note: When there is a loss, Realized Trading Gains is debited (reducing income).

Cash: 50.294. BONK: 0.000. Net gain from BONK: 0.300 SOL. Total fees: 0.006 SOL.

### Example 2: Staking Flow

**Deposit 10 SOL to staking:**

| Account | Debit | Credit |
|---------|-------|--------|
| 1301 Staked SOL | 10.000 | |
| 1010 Cash – SOL | | 10.000 |

**Receive 0.05 SOL staking reward:**

| Account | Debit | Credit |
|---------|-------|--------|
| 1010 Cash – SOL | 0.050 | |
| 3020 Staking Rewards | | 0.050 |

### Example 3: Airdrop

**Receive 5,000 JUP airdrop (market value 2.1 SOL at time of receipt):**

| Account | Debit | Credit |
|---------|-------|--------|
| 1102 Token Holdings – JUP | 2.100 | |
| 3030 Airdrop Income | | 2.100 |

The cost basis for tax purposes is the FMV at time of receipt (2.1 SOL). If you later sell the JUP for 3.0 SOL, you realize a 0.9 SOL gain.

---

## Report Formats

### P&L Statement Structure

```
INCOME
  Realized Trading Gains          sum of 3010
  Staking Rewards                 sum of 3020
  Airdrop Income                  sum of 3030
  LP Fee Income                   sum of 3040
  ────────────────────────────
  Total Income                    sum of all 3xxx

EXPENSES
  Trading Fees                    sum of 4010
  Gas & Priority Fees             sum of 4020
  Slippage Cost                   sum of 4030
  ────────────────────────────
  Total Expenses                  sum of all 4xxx

NET INCOME = Total Income - Total Expenses
```

### Balance Sheet Structure

```
ASSETS
  Cash accounts                   sum of 1010-1030
  Token Holdings                  sum of 1100s
  LP Positions                    sum of 1200s
  Staking Deposits                sum of 1300s
  ────────────────────────────
  Total Assets                    sum of all 1xxx

LIABILITIES
  (sum of all 2xxx)

EQUITY
  Owner Capital                   5010 balance
  Retained Earnings               5020 balance
  Current Period Net Income       calculated
  Less: Withdrawals               5030 balance
  ────────────────────────────
  Total Equity                    sum of all 5xxx

Assets = Liabilities + Equity  (must balance)
```

### Cash Flow Statement Structure

```
OPERATING (trading activity)
  Token sale proceeds
  Token purchase costs
  Fees paid
  Income received (staking, LP fees)

INVESTING (long-term positions)
  LP deposits/withdrawals
  Staking deposits/withdrawals

FINANCING (capital movements)
  Owner contributions
  Owner withdrawals
```

---

## Trading P&L vs Tax P&L

### The Core Difference

**Trading P&L** includes unrealized gains and uses average cost for simplicity. It tells you how your strategy is performing right now.

**Tax P&L** only includes realized gains and uses a specific cost basis method (FIFO, LIFO, or specific identification). It determines what you owe.

### Worked Example: Same Trades, Different P&L

Three buys of BONK:
1. Buy 100,000 BONK at 0.001 SOL each = 0.100 SOL total
2. Buy 100,000 BONK at 0.002 SOL each = 0.200 SOL total
3. Buy 100,000 BONK at 0.003 SOL each = 0.300 SOL total

Total: 300,000 BONK, total cost 0.600 SOL.

Now sell 100,000 BONK at 0.004 SOL each = 0.400 SOL proceeds.

**FIFO (First In, First Out):**
- Cost basis of sold lot: 0.100 SOL (the first buy)
- Realized gain: 0.400 - 0.100 = **0.300 SOL**

**LIFO (Last In, First Out):**
- Cost basis of sold lot: 0.300 SOL (the third buy)
- Realized gain: 0.400 - 0.300 = **0.100 SOL**

**Average Cost:**
- Average cost: 0.600 / 300,000 = 0.000002 SOL each
- Cost basis of sold lot: 100,000 * 0.000002 = 0.200 SOL
- Realized gain: 0.400 - 0.200 = **0.200 SOL**

Same trade, three different gain amounts: 0.300, 0.100, or 0.200 SOL.

### Airdrops: Income at Receipt

Airdrops are taxable as ordinary income at the fair market value on the date received. This creates a cost basis equal to that FMV. Any subsequent gain or loss on sale is a separate capital gain/loss event.

### Wash Sale Considerations

Some jurisdictions apply wash sale rules to crypto. If you sell at a loss and repurchase the same token within 30 days, the loss may be disallowed and added to the cost basis of the new purchase. The ledger does not enforce wash sale rules — consult a tax professional.

---

## Planned Enhancements

Features under consideration for future versions:

- **Multi-currency support** — Track in SOL with USD/EUR conversion at transaction time
- **Wash sale tracking** — Flag potential wash sales with adjustable lookback period
- **Lot-level tracking** — Specific identification for optimal tax lot selection
- **On-chain import** — Parse Solana transactions into journal entries automatically
- **CSV/JSON export** — Export ledger for import into accounting software
- **Mark-to-market overlay** — Add unrealized P&L layer for trading evaluation
- **Entity-level accounts** — Management fees, distributions, payroll for LLC/S-Corp
- **Multi-wallet consolidation** — Merge ledgers across wallets into one view
