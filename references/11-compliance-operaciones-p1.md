# 11-compliance-operaciones — parte 1

Skills de terceros agrupadas por tema. Cada sección indica fuente, licencia y dónde está su código.



---

## SKILL: account-maintenance

- Fuente: `JoelLewis/finance_skills` → `plugins/client-operations/skills/account-maintenance` (MIT)
- Cuándo usarla: Process account maintenance requests across the account lifecycle. Use when changing a client address or contact info with identity verification, updating beneficiary designations after marriage, divorce, birth, or death, re-registering or re-titling an account to a trust or new entity, selecting tax lot methods or fixing cost basis records, applying legal or compliance holds or Reg T freezes, setting up systematic withdrawals or standing instructions, processing a death notification and estate account setup, handling a QDRO, power of attorney, or guardianship, closing accounts and managing escheatment, or designing data quality review programs.

# Account Maintenance

## Core Concepts

### Contact Information Changes
Address and contact updates are among the most frequent account maintenance requests, but they carry meaningful fraud and elder abuse risk. Firms must balance client convenience with protective controls.

**Address change procedures:**
- **Client-initiated changes** may be submitted through the advisor, client portal, phone, or written request. Regardless of channel, the firm must verify the identity of the requesting party before processing the change. Common verification methods include knowledge-based authentication, callback to the phone number on file, or confirmation sent to the prior address or email.
- **Advisor-initiated changes** on behalf of a client should require documented client authorization. Verbal authorization must be noted with date, time, and the identity of the person providing authorization. Written or electronic authorization is preferred and creates a stronger audit trail.
- **Multi-system propagation** is a persistent operational challenge. When an address changes, the update must flow to all systems that store client contact data: CRM, custodian account master, correspondence system, billing system, and any third-party platforms. Failure to propagate consistently results in mail going to old addresses (privacy risk), incorrect tax form delivery (1099s, K-1s), and compliance exposure. Best practice is to designate a single system of record (typically CRM or custodian) and propagate changes outward via integration, rather than requiring manual updates in each system.
- **Temporary vs permanent changes** should be distinguished in the workflow. A client who is traveling or has a seasonal residence may need mail temporarily redirected without changing the legal address of record. The system should support a temporary address with an expiration date that reverts to the permanent address automatically.

**Third-party address change red flags:**
FINRA Regulatory Notice 07-43 and SEC guidance on senior investor protection highlight address changes as a key indicator of potential financial exploitation. Red flags that should trigger enhanced scrutiny include:
- Address change request from someone other than the account holder (especially if followed by a distribution request)
- Change to a P.O. Box when the prior address was a residential address
- Change to an address associated with a known bad actor or previously flagged account
- Multiple address changes in a short period
- Address change for a senior investor (age 65+) followed within 30 days by a large withdrawal or wire transfer
- Address change to a different state or country for a client with no known connection to that location

When a red flag is detected, the firm should place a temporary hold on the address change, contact the client at the prior contact information to confirm the request, and escalate to compliance or a designated senior investor protection contact if confirmation cannot be obtained.

**Notification requirements:**
Many custodians and regulatory expectations require that a confirmation of the address change be sent to both the old and new addresses. This dual notification provides the client an opportunity to detect an unauthorized change. The confirmation should include the date of the change, the new address, and instructions for contacting the firm if the change was not authorized.

### Beneficiary Management
Beneficiary designations determine the disposition of assets upon the account holder's death. Errors or omissions in beneficiary management are among the most consequential account maintenance failures because they are typically discovered only at death, when correction is impossible.

**Designation structure:**
- **Primary beneficiaries** receive assets first (percentages must total 100%); **contingent beneficiaries** receive assets only if all primaries predecease or disclaim.
- **Per stirpes vs per capita** — the election determines whether a predeceased beneficiary's share passes to their descendants (per stirpes) or redistributes to surviving beneficiaries (per capita). The operational requirement is to record the election explicitly on the custodian's form; an ambiguous or missing election is unresolvable at death.

**Beneficiary updates for life events:**
- **Marriage:** The client may want to add a spouse as primary beneficiary. For ERISA-governed retirement plans, the spouse is the default beneficiary unless the spouse provides written consent to a different designation. For IRAs and non-ERISA accounts, there is no automatic spousal beneficiary right, but advisors should prompt a review.
- **Divorce:** Beneficiary designations naming a former spouse are not automatically revoked by divorce in most states for non-ERISA accounts (the law varies by state and account type). The client must affirmatively update the designation. Failure to update after divorce is one of the most common and costly beneficiary errors. For ERISA plans, a QDRO may assign benefits to a former spouse regardless of the current designation.
- **Birth or adoption:** Clients should add new children as beneficiaries or adjust percentages. Per stirpes designations may automatically include new descendants, but per capita designations do not.
- **Death of a beneficiary:** If a primary beneficiary dies, the firm should notify the account holder and recommend updating the designation; the per stirpes/per capita election on file determines where the predeceased beneficiary's share goes.

**Retirement account beneficiary rules (SECURE Act):**
The SECURE Act of 2019 (and SECURE 2.0 Act of 2022) fundamentally changed inherited retirement account distribution rules:
- **Spouse beneficiaries** may roll the inherited account into their own IRA, treat it as their own, or take distributions over their life expectancy — the most flexible options.
- **Eligible designated beneficiaries** (minor children of the account holder, disabled or chronically ill individuals, individuals not more than 10 years younger than the deceased) may use the life expectancy method.
- **All other designated beneficiaries** (including adult children and non-spouse partners) must distribute the entire inherited account within 10 years of the account holder's death. There is no annual RMD requirement during the 10-year period if the account holder died before their required beginning date; if the account holder died after their required beginning date, annual distributions may be required within the 10-year window.
- **Non-designated beneficiaries** (estates, certain trusts, charities) follow either the 5-year rule or the deceased's remaining life expectancy, depending on whether the account holder died before or after the required beginning date.

These rules make beneficiary designation a critical planning decision. The choice between naming individuals, trusts, or other entities as beneficiaries has significant tax implications that should be coordinated with the tax-efficiency and financial-planning-integration skills.

**TOD/POD designations:**
TOD (brokerage) and POD (bank) designations pass assets to named beneficiaries outside probate and override the will — the operational requirements are to document the designation on the custodian's designated form, retain a copy, and flag the account for estate-planning coordination since a stale TOD silently defeats the client's will.

**Beneficiary review cadence:**
Best practice is to review beneficiary designations at every major life event and at minimum during the annual or biennial client review meeting. The firm should maintain a process to flag accounts with outdated or missing beneficiary designations — for example, accounts with no beneficiary on file, accounts where the designated beneficiary has a flagged death record, or accounts that have not had a beneficiary review in more than 3 years.

### Account Re-Registration and Re-Titling
Re-registration changes the legal ownership or titling of an account. This is operationally more complex than a simple data update because it affects the legal rights to the account assets, may trigger tax consequences, and typically requires custodian processing with supporting documentation.

**Common re-registration events:**
- **Individual to revocable trust:** The most frequent re-registration. Assets move from the individual's name into the trust's name. Because a revocable trust is a grantor trust (the individual retains control), this is generally not a taxable event. The trust uses the grantor's SSN as its TIN. Required documentation typically includes a trust certification, the account holder's written instruction, and (depending on the custodian) a medallion signature guarantee.
- **Name change (marriage or divorce):** The account title changes to reflect the new legal name. Required documentation: legal name change document (marriage certificate, court order), government-issued ID in the new name (or a combination of old ID plus name change document), updated W-9.
- **Joint to individual (death of co-owner):** For JTWROS accounts, the surviving owner becomes the sole owner. Required documentation: death certificate and letter of instruction from the surviving owner. The custodian removes the deceased owner's name from the account. For TIC accounts, the deceased owner's share passes to their estate, requiring a different process.
- **Individual to estate:** Upon death, the individual account may need to be re-titled to the estate while probate is underway. Required documentation: death certificate, letters testamentary or letters of administration, EIN for the estate.
- **Trust to beneficiaries (trust termination):** When a trust terminates per its terms, assets are distributed to trust beneficiaries. Required documentation: trustee certification of termination, distribution instructions, beneficiary identification and account setup.
- **Entity restructuring:** LLC converting to corporation, partnership changes, mergers. Required documentation: entity formation/conversion documents, corporate resolutions, updated operating agreements.

**Tax implications of re-registration:**
- **Cost basis transfer:** When assets are re-registered without a change in beneficial ownership (e.g., individual to revocable trust, name change), the cost basis carries over unchanged. The original acquisition dates and cost lots transfer to the new registration.
- **Step-up in basis:** When assets transfer due to death, the beneficiary generally receives a stepped-up cost basis equal to the fair market value of the assets on the date of death (or alternate valuation date if elected by the estate). This step-up eliminates unrealized capital gains that existed during the decedent's lifetime. Community property assets may receive a full step-up on both halves at the first spouse's death in community property states.
- **Taxable transfers:** Re-registration that constitutes a gift (e.g., transferring assets from parent to child) or a sale (e.g., transferring assets to an unrelated party) may trigger gift tax or capital gains tax. The firm should not provide tax advice but should flag these situations and recommend the client consult a tax advisor.

**Medallion signature guarantee requirements:**
A medallion signature guarantee is a certification by a financial institution that a signature is genuine and that the signer has the authority to execute the transaction. Medallion guarantees are commonly required for: transfers of securities to a different name or entity, requests to change account registration, physical stock certificate transfers, and certain large-value transactions. The three medallion guarantee programs are STAMP (Securities Transfer Agents Medallion Program), SEMP (Stock Exchanges Medallion Program), and MSP (NYSE Medallion Signature Program). Not all financial institutions participate in all programs; the firm must verify that the guarantee is from an institution participating in an accepted program.

**Custodian processing:**
Re-registration timelines vary significantly by custodian and complexity. Simple name changes may process in 1-3 business days. Trust re-registrations typically take 3-7 business days. Estate re-registrations and complex entity changes may take 1-4 weeks, particularly if the custodian's legal department must review trust or entity documents. During processing, the account may be in a restricted state where trading is limited. The firm should set client expectations regarding processing times and any trading restrictions during the re-registration period.

### Cost Basis Management
Accurate cost basis tracking is essential for tax reporting (1099-B), client tax planning, and regulatory compliance. The firm's obligations depend on whether shares are "covered" (acquired after the applicable effective date under the Emergency Economic Stabilization Act of 2008) or "uncovered."

**Tax lot accounting methods:**
- **Specific identification (Spec ID):** The client or advisor selects which specific tax lots to sell. This provides maximum tax control — the ability to choose lots with the highest cost basis (minimizing gains) or lowest basis (harvesting losses). Requires lot-level identification at the time of the trade, either proactively or within the settlement period.
- **First In, First Out (FIFO):** The oldest shares are deemed sold first. This is the IRS default method if no other method is elected. FIFO tends to produce long-term capital gains (favorable tax rates) but may not minimize total tax liability.
- **Last In, First Out (LIFO):** The most recently acquired shares are deemed sold first. This tends to produce short-term capital gains but may result in lower gain amounts if recent purchases were at higher prices.
- **Highest In, First Out (HIFO):** The shares with the highest cost basis are deemed sold first. This minimizes realized gains and is often the preferred method for taxable accounts focused on tax efficiency.
- **Average cost:** Available only for mutual fund shares and shares acquired through dividend reinvestment plans. The average cost of all shares is used as the basis for each share sold. Once elected for a specific fund, average cost applies to all shares of that fund in the account.

**Cost basis transfer rules:**
- **ACATS transfers:** Cost basis transfer mechanics between firms (covered vs uncovered shares, the CBRS 15-day window, IRC Section 6045A) are covered in account-transfers; the maintenance-side obligation is to verify the received basis against client records and resolve discrepancies promptly.
- **Re-registration transfers:** Cost basis carries over in non-taxable re-registrations (e.g., individual to revocable trust). For transfers due to death, the receiving account should reflect the stepped-up basis as of the date of death.
- **Gift transfers:** The recipient generally takes the donor's cost basis (carryover basis) for gains. If the fair market value at the time of gift is less than the donor's basis, special rules apply for determining basis for loss purposes (the basis is the FMV at the date of the gift).

**Corporate action adjustments:**
Corporate actions frequently alter cost basis, and errors in corporate action processing are a leading source of cost basis inaccuracies:
- **Stock splits and reverse splits:** The total cost basis remains the same; per-share basis adjusts proportionally. A 2-for-1 split halves the per-share basis; a 1-for-10 reverse split multiplies per-share basis by 10.
- **Mergers and acquisitions:** If the merger is a tax-free reorganization (stock-for-stock exchange), the cost basis of the old shares carries over to the new shares, allocated proportionally. If the merger involves cash consideration (cash-and-stock deal), the cash portion is taxable and reduces the basis allocated to the new shares.
- **Spin-offs:** The cost basis of the parent company shares is allocated between the parent and the spun-off entity based on the relative fair market values on the distribution date. The IRS typically provides allocation guidance or the companies publish allocation percentages.
- **Return of capital distributions:** Reduce the cost basis of the shares. If return of capital exceeds the cost basis, the excess is treated as capital gain. Accurate tracking of return of capital distributions over time is critical for partnerships, REITs, and MLPs.

**Wash sale tracking:**
The wash sale rule (IRC Section 1091) disallows a loss deduction if substantially identical securities are purchased within 30 days before or after the sale. The disallowed loss is added to the cost basis of the replacement shares. Firms must track wash sales within the same account and, for tax reporting purposes, across all accounts of the same taxpayer at the firm. Cross-account and cross-firm wash sale tracking remains the taxpayer's responsibility, but the firm should provide tools and reporting to assist.

**Covered vs uncovered shares and 1099-B reporting:**
For covered shares, the broker is required to report cost basis to the IRS on Form 1099-B and to apply the client's elected accounting method. For uncovered shares, the broker reports the sale proceeds but is not required to report cost basis (Box 1e is left blank). The client is responsible for reporting basis on their tax return for uncovered shares. The firm should maintain whatever historical basis records it has for uncovered shares and make them available to clients, but the obligation to report accurate basis to the IRS rests with the taxpayer.

### Account Restrictions and Holds
Restrictions limit or prevent transactions on an account. They may be imposed by the firm, a regulator, a court, or by operation of law. Proper restriction management protects the firm from liability and ensures compliance with legal and regulatory requirements.

**Types of restrictions:**
- **Death notification hold:** Upon receipt of a death notification, the firm must immediately restrict the deceased's accounts to prevent unauthorized transactions. No new trades, distributions, or changes should be processed until the firm receives appropriate legal documentation (death certificate, letters testamentary/administration, or beneficiary claim forms). Joint accounts with rights of survivorship are an exception — the surviving owner retains trading authority, but the deceased's name must be removed via re-registration.
- **Divorce/domestic relations hold:** When the firm receives a divorce decree or court order related to a domestic dispute, affected accounts may be restricted pending asset division. The restriction should prevent both parties from making withdrawals or transfers until the division is executed per the court order. QDRO processing for retirement accounts requires special handling (see Life Event Processing below).
- **Legal hold (litigation/subpoena):** A legal hold preserves account records and may restrict transactions when the firm receives a subpoena, litigation hold notice, or regulatory investigation notification. The hold prevents destruction of relevant records and may restrict the account holder's ability to close the account or transfer assets.
- **Compliance hold:** The firm's compliance department may restrict an account pending investigation of suspicious activity (SAR filing), suitability concerns, or other compliance issues. The restriction scope is determined by the nature of the concern — it may be a full freeze or limited to specific transaction types.
- **Reg T freeze:** Under Regulation T, if a client purchases securities and fails to pay for them by the payment date (settlement date), the account may be frozen for 90 days. During the freeze, the client can only purchase securities if the full purchase price is deposited in advance (cash before trade). The restriction is lifted after 90 days or upon application to the firm's credit department.
- **Margin restriction:** When a margin account is in a margin call (maintenance call, Reg T call, or house call) and the client fails to meet the call, the firm may restrict trading to liquidation-only until the call is met.
- **OFAC match:** If an account holder or associated party matches a name on the OFAC Specially Designated Nationals (SDN) list, the account must be blocked (frozen) immediately. All assets in the account are blocked and no transactions may be processed. The firm must file a blocking report with OFAC within 10 business days. The block remains until OFAC provides a specific license to unblock or the match is resolved as a false positive.
- **Garnishment and levy:** When the firm receives a valid garnishment order, tax levy (IRS or state), or attachment order from a court or government agency, the firm must comply by freezing the specified amount and/or remitting funds as directed. Retirement accounts have limited protection under ERISA and state law, requiring careful analysis before responding to a garnishment.

**Restriction application and removal procedures:**
Restrictions should be applied immediately upon receipt of the triggering event (death notification, court order, compliance directive). The restriction should be documented in the account master record and visible to all users who access the account, including advisors, operations staff, and client service representatives. Removal of restrictions requires documented authorization: compliance sign-off for compliance holds, receipt of legal documentation for death and divorce holds, passage of time for Reg T freezes, and OFAC license or false positive determination for OFAC blocks.

### Standing Instructions
Standing instructions are pre-authorized, recurring or default instructions on an account that execute automatically without requiring individual authorization for each occurrence.

**Common standing instruction types:**
- **Systematic withdrawal plan (SWP):** Periodic distributions from the account (monthly, quarterly, annually) in a fixed dollar amount or percentage. Common for retirement income accounts. The plan should specify the source (which holdings to sell or cash to distribute), the distribution method (check, ACH, wire), and tax withholding elections (federal and state).
- **Automatic investment plan (AIP):** Periodic contributions to the account, typically via ACH from a bank account, invested according to a specified allocation (model portfolio, specific funds, or dollar-cost averaging into specified securities).
- **Dividend reinvestment (DRIP):** Elections to reinvest dividends and capital gains distributions rather than receiving cash. DRIP elections may be set at the account level (all holdings) or at the individual security level. Reinvested shares create new tax lots at the reinvestment price.
- **Fee debit instructions:** Authorization for the firm to deduct advisory fees directly from the account. The instruction should specify the fee schedule, billing frequency (monthly, quarterly), and the billing source (which account to debit if the client has multiple accounts). SEC guidance requires that the fee authorization be documented in writing and that the client receive advance notice of fee debits.
- **Cash sweep instructions:** Direction for uninvested cash to be automatically swept into a designated vehicle — money market fund, bank deposit program (FDIC-insured sweep), or interest-bearing cash account. Sweep elections are typically set at account opening but may be changed.
- **Standing wire/ACH instructions:** Pre-authorized instructions for recurring or on-demand transfers to a specific external account (bank account, third-party account). Standing wire instructions reduce fraud risk by limiting wire destinations to pre-verified accounts. Adding a new wire destination should require enhanced verification (callback, written authorization, hold period before first use).

**Instruction modification procedures:**
Modifications to standing instructions should follow the same identity verification procedures as other account changes. Changes to fee debit instructions and distribution methods should be documented in writing. The firm should maintain an audit trail of all instruction changes, including the prior instruction, the new instruction, the date of change, and the identity of the requesting party and the processor.

### Life Event Processing
Life events trigger complex, multi-step account maintenance workflows that cut across multiple accounts and registration types. These events have legal, tax, and operational dimensions that require coordinated processing.

**Death notification and estate processing:**
1. **Receive and verify the death notification.** The firm may learn of a death from a family member, advisor, estate attorney, or obituary monitoring service. The firm should verify the notification by requesting a certified death certificate. A verbal notification is sufficient to trigger an immediate account restriction, but documentation is required before any further processing.
2. **Restrict all accounts.** Upon notification, immediately restrict all accounts in the deceased's name — individual accounts, the deceased's interest in joint accounts, retirement accounts, and any accounts where the deceased was an authorized party. For JTWROS accounts, the surviving owner retains access but the account must be re-registered.
3. **Identify account types and disposition paths.** Each account type follows a different disposition path:
   - *Individual taxable accounts:* Assets pass to the estate (if no TOD) or to TOD beneficiaries (if TOD is on file). Estate distribution requires letters testamentary.
   - *Joint accounts (JTWROS):* Assets pass to the surviving owner automatically. Re-register by removing the deceased's name upon receipt of the death certificate.
   - *Joint accounts (TIC):* The deceased's proportional share passes to their estate. The surviving owner retains their share.
   - *Retirement accounts (IRA, 401k):* Assets pass to the named beneficiary per the beneficiary designation on file. Beneficiary claims require the death certificate and a beneficiary claim form. Inherited IRA accounts must be established for each beneficiary.
   - *Trust accounts:* Disposition depends on the trust terms. The successor trustee takes control upon the death of the original trustee. If the trust terminates, assets are distributed to trust beneficiaries per the trust instrument.
   - *TOD accounts:* Assets transfer directly to named TOD beneficiaries upon receipt of the death certificate and beneficiary claim forms, bypassing probate.
4. **Process beneficiary claims and estate distributions.** For each account, collect the required documentation (death certificate, beneficiary claim form, letters testamentary, trust certification of successor trustee) and process the transfer or distribution. Establish new accounts as needed (inherited IRA for each beneficiary, estate account for the personal representative).
5. **Adjust cost basis.** Apply the step-up in basis to all assets as of the date of death (or alternate valuation date). Update cost basis records in the account master and portfolio management system.
6. **Tax reporting.** The deceased's final 1099 covers activity from January 1 through the date of death. Subsequent activity is reported under the estate's EIN or the beneficiary's SSN, depending on how and when assets are distributed.

**Divorce decree processing:**
- **Non-retirement accounts:** The divorce decree or marital settlement agreement specifies how accounts are divided. The firm processes the division by transferring the specified assets or dollar amounts to the receiving spouse's account. If the receiving spouse does not have an account, one must be opened. The transfer between spouses incident to divorce is not a taxable event (IRC Section 1041); cost basis carries over to the receiving spouse.
- **Retirement accounts — QDRO:** Division of ERISA-governed retirement plan assets requires a Qualified Domestic Relations Order (QDRO). The QDRO must be reviewed and accepted by the plan administrator. For IRAs (which are not ERISA-governed), a transfer incident to divorce is processed per the divorce decree without a QDRO, pursuant to IRC Section 408(d)(6).
- **Account restrictions during divorce:** The firm should restrict affected accounts upon receiving a court order or notification from either party's attorney. Restrictions prevent either party from depleting assets before the division is executed.

**Marriage processing:**
- **Name change:** Process the name change re-registration with supporting documentation (marriage certificate, updated ID).
- **Beneficiary review:** Prompt the client to review and update beneficiary designations on all accounts.
- **Account consolidation:** If both spouses have accounts at the firm, they may wish to establish joint accounts or consolidate household accounts. New joint account opening follows standard onboarding procedures.

**Incapacity:**
- **Power of attorney (POA):** A POA grants an agent authority to act on the account holder's behalf. The firm must review the POA document to confirm it grants authority over financial accounts, verify the agent's identity, and determine whether the POA is durable (survives incapacity) or springs into effect only upon incapacity. Many custodians have specific POA acceptance requirements and may require their own POA form.
- **Guardianship/conservatorship:** A court-appointed guardian or conservator presents court documentation granting authority over the incapacitated person's financial affairs. The firm must verify the court order, confirm its scope and jurisdiction, and establish the guardian/conservator as the authorized party on the account. Transactions by the guardian/conservator may be subject to court oversight and reporting requirements.
- **Senior investor protections:** The FINRA Rule 2165 temporary-hold safe harbor and Rule 4512 trusted contact requirements are covered in account-opening-compliance; operationally, when exploitation is suspected during a maintenance request, place the disbursement hold, notify the trusted contact, and document the basis for the hold.

### Account Closure
Account closure is the final stage of the account lifecycle. Whether voluntary or involuntary, the closure process must ensure complete asset disposition, final billing, and regulatory-compliant record retention.

**Voluntary closure:**
The account holder (or authorized party) requests closure. The firm processes the request by: (1) confirming the client's identity and authorization, (2) determining asset disposition — transfer to another firm via ACAT, liquidation and check/wire, or in-kind transfer to a specific account, (3) processing final fee billing and any outstanding charges, (4) generating final account statements and tax documents, and (5) closing the account in the custodian and internal systems. The firm should document the reason for closure (client-provided or advisor-noted) for business analytics and regulatory purposes.

**Involuntary closure:**
The firm may close an account without the holder's request in certain circumstances: prolonged inactivity (no activity and zero or de minimis balance for a defined period), failure to provide required documentation (CIP/KYC deficiencies), compliance determination (AML concerns, pattern of trading violations, unsuitable activity), or business decision (exiting a client segment, platform consolidation). Involuntary closure requires advance written notice to the account holder (typically 30 days), an opportunity for the client to transfer assets, and compliance review and approval.

**Abandoned property (escheatment):**
State unclaimed property laws require firms to identify and report abandoned accounts — accounts with no client-initiated activity for the state's dormancy period (typically 3-5 years, varying by state and property type). Before escheatment, the firm must conduct due diligence to locate the account holder (mailing, email, phone attempts, database searches). If the owner cannot be located, the assets are remitted to the state of the owner's last known address (or the firm's state of incorporation if no address is on file). Escheatment processing requires careful tracking because each state has different dormancy periods, due diligence requirements, reporting deadlines, and remittance procedures.

**Record retention post-closure:**
Closing an account does not terminate the firm's recordkeeping obligations. SEC Rule 17a-4 (broker-dealers) and Rule 204-2 (investment advisers) require retention of account records for specified periods after the account is closed — generally 6 years for most account records. The firm must maintain access to closed account records for regulatory examinations, client inquiries, and potential litigation. Records should be archived in a searchable, retrievable format.

## Worked Examples


Three worked examples — an individual-to-revocable-trust re-registration (including the close-and-reopen cost basis reset gotcha), a multi-account death notification across five registration types (JTWROS, IRA spousal rollover, trust succession, step-up processing), and a firm-wide data quality review program — are in [references/examples.md](references/examples.md); load it when processing a concrete re-registration, death notification, or data remediation project.

## Common Pitfalls
- Processing an address change without adequate identity verification, enabling unauthorized changes or elder financial exploitation
- Failing to update beneficiary designations after a divorce — the former spouse may inherit retirement account assets if the designation is not changed, regardless of the divorce decree (for non-ERISA accounts in most states)
- Re-registering an account as a close-and-reopen rather than a title change, which can reset cost basis records and create phantom taxable events
- Applying the wrong tax lot accounting method after an ACATS transfer because the receiving firm's default differs from the client's prior election
- Not placing an immediate restriction on all of a deceased client's accounts upon death notification, allowing unauthorized transactions
- Processing a power of attorney without verifying that the document grants authority over financial accounts and that the POA is durable (survives incapacity)
- Failing to distinguish between covered and uncovered shares when processing cost basis transfers, leading to incorrect 1099-B reporting
- Allowing a standing wire instruction to be added or changed without enhanced verification (callback, hold period), creating wire fraud exposure
- Not tracking return-of-capital distributions on partnerships, REITs, and MLPs, leading to overstated cost basis and incorrect gain/loss calculations
- Processing estate distributions before receiving letters testamentary or letters of administration, exposing the firm to liability if the distribution is challenged
- Neglecting escheatment obligations for dormant accounts, resulting in regulatory penalties from state unclaimed property audits
- Treating all joint accounts the same upon a co-owner's death — JTWROS and TIC accounts have fundamentally different disposition rules

## Cross-References
- **account-opening-workflow** (client-operations plugin): Account opening establishes the initial registration, beneficiary designations, and standing instructions that this skill maintains throughout the account lifecycle
- **books-and-records** (compliance plugin): Recordkeeping obligations for account maintenance documentation, including retention of change requests, authorizations, and correspondence per SEC Rules 17a-3/17a-4 and Rule 204-2
- **privacy-data-security** (compliance plugin): Address changes, contact updates, and account data maintenance involve nonpublic personal information protected by Reg S-P; data quality processes must comply with privacy requirements
- **tax-efficiency** (wealth-management plugin): Cost basis management, tax lot accounting method selection, and step-up in basis processing directly affect tax-efficient investing outcomes
- **client-onboarding** (advisory-practice plugin): Onboarding collects the initial data (beneficiaries, suitability, contact information) that account maintenance keeps current throughout the relationship
- **corporate-actions** (client-operations plugin): Corporate actions (splits, mergers, spin-offs, return of capital) alter cost basis and require coordination with the cost basis management processes described in this skill
- **account-transfers** (client-operations plugin): ACATS and non-ACATS transfers interact with cost basis transfer rules and re-registration procedures; transfer processing often triggers account maintenance updates at the receiving firm

### Referencia: references/examples.md

# Account Maintenance — Worked Examples

## Example 1: Processing an account re-registration from individual to revocable trust

**Scenario:** A 62-year-old client with $3.2M across three accounts at the firm (individual taxable brokerage account with $2.1M, traditional IRA with $800K, and Roth IRA with $300K) has recently established a revocable living trust with her estate attorney. The trust names the client as grantor and trustee, with her adult son as successor trustee. The client wants to transfer the taxable brokerage account into the trust. The IRA and Roth IRA cannot be held in a trust (they must remain in the individual's name).

**Step-by-step processing:**

1. **Verify the request and gather documentation.** Confirm the client's identity and the nature of the request. Obtain: (a) a trust certification or the relevant pages of the trust agreement showing the trust name, date of establishment, grantor, trustee(s), successor trustee(s), and the trust's powers regarding investment accounts; (b) a signed letter of instruction from the client directing the re-registration; (c) an updated W-9 in the trust's name (using the client's SSN, since this is a grantor trust). Depending on the custodian, a medallion signature guarantee on the letter of instruction may be required.

2. **Review the trust document.** Operations or the compliance team reviews the trust certification to confirm: the trust is validly established, the client is the current trustee with authority to open and manage investment accounts, the trust is revocable (confirming grantor trust status and SSN usage), and there are no restrictions on the types of investments the trust can hold. Flag any unusual provisions for compliance review.

3. **Prepare the custodian re-registration request.** Complete the custodian's account re-registration or re-titling form. The new registration will read something like: "Jane A. Smith, Trustee of the Jane A. Smith Revocable Living Trust dated January 15, 2026." Submit the form, trust certification, W-9, and letter of instruction to the custodian.

4. **Confirm the tax treatment.** This re-registration is not a taxable event. The assets move from the individual's name to her revocable trust with no change in beneficial ownership. All existing tax lots, cost basis, and acquisition dates carry over unchanged. The account will continue to report under the client's SSN for tax purposes. Document this determination in the account notes.

5. **Update internal systems.** After the custodian confirms the re-registration: update the CRM to reflect the trust account and its relationship to the client record; update the portfolio management system's account registration; verify that the model portfolio assignment and investment restrictions carry over; confirm that the billing account linkage is maintained (fees are typically still billed to the trust account or another account in the household); update beneficiary designations on the IRA and Roth IRA if the client wishes to name the trust as a beneficiary (noting the tax implications — a trust as IRA beneficiary may limit stretch distribution options).

6. **Client communication.** Send the client a confirmation of the completed re-registration with the new account title. Remind the client that the IRA and Roth IRA remain in her individual name and that she should coordinate with her estate attorney to ensure beneficiary designations on those accounts align with the trust's distribution provisions.

**Key risks and controls:** Verify that the SSN (not a separate EIN) is used for the grantor trust — using an EIN would create tax reporting errors. Confirm that cost basis records are preserved through the re-registration; some custodian systems may reset cost basis if the re-registration is processed as a close-and-reopen rather than a title change. Monitor for this and correct any basis discrepancies immediately.

## Example 2: Handling a death notification across multiple accounts with different registration types

**Scenario:** The firm receives a call from the wife of a 71-year-old client who passed away two days ago. The deceased client held five accounts at the firm: (1) an individual taxable brokerage account ($1.4M), (2) a joint taxable brokerage account with his wife as JTWROS ($900K), (3) a traditional IRA ($650K) with his wife as primary beneficiary and two adult children as contingent beneficiaries, (4) a Roth IRA ($200K) with the same beneficiary designation, and (5) a revocable trust account ($500K) where the deceased was sole trustee and his wife is named as successor trustee. The firm also manages the wife's individual IRA ($400K) separately.

**Step-by-step processing:**

1. **Receive and document the notification.** Record the date and time of the notification, the identity of the person providing notification (the wife), and the relationship to the deceased. Express appropriate condolences. Explain that you will need a certified death certificate to proceed with account processing and outline the general timeline. Assign a dedicated operations contact or "estate services coordinator" as the single point of contact for the family.

2. **Immediately restrict the deceased's accounts.** Place a death restriction on all five accounts. For accounts (1), (3), (4), and (5), this means no trading, distributions, or changes until appropriate documentation is received. For account (2) — the JTWROS account — the wife retains access as the surviving owner, but place a notation that the deceased owner must be removed via re-registration. Do not restrict the wife's own IRA (account 6), as it is not an account of the deceased.

3. **Request required documentation.** Provide the wife with a checklist of documents needed for each account:
   - *All accounts:* Certified death certificate (at least 3 copies recommended).
   - *Individual taxable account (1):* If a TOD designation is on file, a beneficiary claim form. If no TOD, letters testamentary (if there is a will) or letters of administration (if intestate), and the estate's EIN.
   - *JTWROS account (2):* Death certificate only — the wife will become sole owner.
   - *Traditional IRA (3) and Roth IRA (4):* Beneficiary claim forms for the wife as primary beneficiary. The wife will need to decide whether to roll the traditional IRA into her own IRA (spousal rollover), treat it as her own, or establish an inherited IRA. For the Roth IRA, a spousal rollover into her own Roth IRA is typically the most advantageous option.
   - *Trust account (5):* Trust certification showing the wife as successor trustee, or the relevant pages of the trust agreement confirming successor trustee status.

4. **Process each account upon receipt of documentation.**
   - *Account 1 (individual taxable):* Assume a TOD designation naming the wife. Upon receipt of the death certificate and signed beneficiary claim form, transfer assets to the wife's account (or a new account in her name). Apply the step-up in basis — revalue all positions to their fair market value as of the date of death. If no TOD, assets pass to the estate: open an estate account titled "Estate of [Deceased], [Personal Representative] as Executor/Administrator," obtain the estate's EIN, and transfer assets to the estate account pending probate and distribution.
   - *Account 2 (JTWROS):* Upon receipt of the death certificate, re-register the account in the wife's name alone. Remove the deceased's name from the account title. The wife's SSN remains on the account. Apply the step-up in basis to the deceased's half of the account (50% of each position is stepped up to date-of-death FMV in non-community-property states; in community property states, both halves may be stepped up).
   - *Account 3 (traditional IRA):* The wife elects spousal rollover, rolling the $650K into her own traditional IRA. This is the most common election because it allows the wife to defer RMDs until she reaches RMD age — 73 (SECURE 2.0; rises to 75 in 2033) — and name her own beneficiaries. Process the rollover as a trustee-to-trustee transfer. Cost basis is not relevant for traditional IRA assets (fully taxable on distribution), but the transfer must be processed as a non-taxable rollover and reported on Form 1099-R with the appropriate distribution code.
   - *Account 4 (Roth IRA):* The wife elects to treat the inherited Roth as her own Roth IRA by rolling it into her existing or a new Roth IRA. This preserves the tax-free growth and eliminates any distribution requirements during her lifetime.
   - *Account 5 (trust account):* Upon receipt of the trust certification confirming the wife as successor trustee, re-title the account to reflect her as trustee: "[Wife's Name], Trustee of the [Trust Name]." Review the trust terms to determine if the trust continues (common with revocable trusts that become irrevocable upon death of the grantor) or terminates and distributes assets to beneficiaries. If the trust becomes irrevocable, it will need its own EIN going forward.

5. **Coordinate tax reporting.** The deceased's final tax year runs from January 1 to the date of death. Activity on accounts (1) through (5) through the date of death is reported under the deceased's SSN. Activity after the date of death is reported under the wife's SSN (for accounts she takes over), the estate's EIN (for estate accounts), or the trust's EIN (if the trust becomes irrevocable). Work with the custodian to ensure correct TIN assignment on all accounts post-death.

6. **Update all internal systems.** Update the CRM to reflect the death, change the household structure, reassign the advisor relationship to the wife as the primary client, update account registrations in the portfolio management system, and adjust the billing configuration (the wife may now be the billable party for all accounts). Schedule a follow-up meeting between the advisor and the wife (after an appropriate interval) to review the consolidated portfolio, update her investment policy, and adjust the financial plan.

**Key risks and controls:** The greatest risk is processing transactions on a deceased person's account before proper documentation is in hand — this can create legal liability and tax reporting errors. The second risk is incorrect cost basis after the step-up: every position must be revalued to the date-of-death FMV, and the custodian's automated step-up process should be verified against an independent price source. Third, ensure that IRA beneficiary elections (spousal rollover vs inherited IRA) are documented in writing, as the choice is irrevocable and has significant long-term tax implications.

## Example 3: Implementing systematic account maintenance review and data quality processes

**Scenario:** A mid-sized RIA with $5B AUM across 4,000 accounts has identified recurring data quality issues: 12% of accounts have no beneficiary designation on file, 8% have addresses that generate returned mail, 15% of trust accounts are missing current trust certifications, and the firm has no systematic process for reviewing accounts that have not been updated in more than 3 years. The firm wants to implement a proactive account maintenance review program to improve data quality, reduce operational risk, and satisfy regulatory expectations for books and records.

**Designing the review program:**

1. **Establish a data quality baseline.** Generate a comprehensive data quality report across all accounts, measuring completeness and accuracy for critical fields:
   - *Beneficiary designations:* Percentage of eligible accounts (retirement accounts, TOD accounts) with primary and contingent beneficiaries on file, percentage with beneficiary review within the past 3 years.
   - *Contact information:* Percentage of accounts with validated mailing addresses (no returned mail), percentage with email on file, percentage with phone number on file and verified.
   - *Trust and entity documentation:* Percentage of trust accounts with trust certification on file and dated within the past 5 years, percentage of entity accounts with current formation documents and beneficial ownership certification.
   - *Suitability profiles:* Percentage of accounts with investment profile updated within the past 3 years, percentage with risk tolerance questionnaire on file.
   - *Standing instructions:* Percentage of accounts with systematic plans that have not been reviewed in more than 2 years.
   - *Cost basis records:* Percentage of holdings with uncovered shares that have no historical cost basis on file.

2. **Prioritize remediation by risk and impact.** Not all data quality issues carry equal risk. Prioritize:
   - *High priority (remediate within 90 days):* Missing beneficiary designations on retirement accounts (disposition risk at death), returned mail with no valid address on file (regulatory and escheatment risk), accounts with compliance or legal holds that have not been reviewed in 6+ months.
   - *Medium priority (remediate within 180 days):* Stale trust certifications (operational risk at trustee change or death), outdated suitability profiles (regulatory risk for ongoing recommendations), missing cost basis on large positions (tax reporting risk).
   - *Lower priority (remediate within 12 months):* Missing email addresses, missing contingent beneficiary designations, standing instructions that have not been reviewed recently.

3. **Design the ongoing review cadence.** Establish a recurring review cycle:
   - *Annual account maintenance review:* Coincide with the annual client review meeting. The advisor reviews and confirms: contact information, beneficiary designations, suitability profile, investment restrictions, standing instructions, and account features. The review is documented in the CRM with a timestamp and the advisor's attestation that all information is current.
   - *Quarterly data quality reports:* Operations generates quarterly metrics showing data completeness rates, trending, and accounts requiring attention. The report is reviewed by the chief compliance officer and the operations manager.
   - *Triggered reviews:* Certain events trigger an immediate account review outside the annual cycle: returned mail, life event notification (marriage, divorce, birth, death), significant market events that may affect suitability, advisor departure (all accounts assigned to a departing advisor receive an expedited review by the successor advisor), and custodian platform migration.

4. **Implement operational workflows for common maintenance items.** For each maintenance category, define a standard operating procedure (SOP) that specifies:
   - *Who* can initiate the request (client, advisor, operations, compliance)
   - *What* documentation or verification is required
   - *How* the request is processed (system workflow, custodian submission)
   - *When* the request must be completed (service-level agreement)
   - *What* quality checks are performed before and after processing
   - *How* the completed action is documented and retained

   For example, the SOP for an address change specifies: the advisor or client initiates the request; identity verification is performed per firm policy (callback to phone on file for verbal requests, or written/electronic authorization); the address is updated in the CRM (system of record); the CRM integration propagates the change to the custodian and correspondence system; a confirmation is sent to both the old and new addresses; senior investor protections are applied if the client is 65+ and the change triggers a red flag; the change is completed within 2 business days; and the change record is retained in the CRM activity log.

5. **Assign accountability and measure progress.** Designate an "account data steward" — a member of the operations team responsible for data quality monitoring and remediation coordination. Publish a monthly data quality dashboard tracking: percentage of accounts with complete and current data across all critical fields, number of open remediation items by priority, average age of open items, and NIGO rates (as a proxy for data quality at the point of custodian submission). Set targets: 95% completeness for high-priority fields within 12 months, 90% for medium-priority fields within 18 months.

**Key risks and controls:** The primary risk in a data quality remediation program is client fatigue — contacting thousands of clients to update information can strain advisor relationships if not managed carefully. Mitigate this by embedding updates in existing client interactions (annual review meetings, service calls) rather than launching a standalone outreach campaign. The second risk is privacy: ensure that all outreach communications about account data comply with Reg S-P and do not disclose nonpublic personal information. Third, maintain an audit trail of all remediation activities for regulatory examination purposes — examiners expect to see a documented, systematic approach to data quality, not ad hoc corrections.


---

## SKILL: account-opening-compliance

- Fuente: `JoelLewis/finance_skills` → `plugins/client-operations/skills/account-opening-compliance` (MIT)
- Cuándo usarla: Embed compliance controls into account opening and verify regulatory readiness. Use when designing CIP/KYC identity verification gates, implementing OFAC and sanctions screening at onboarding, collecting beneficial ownership certification for entity or trust accounts, building risk-based approval tiers that route applications by risk level, defining compliance screening requirements and exception tracking, adding senior investor protections (FINRA Rules 2165/4512) or trusted contact procedures, establishing CDD risk ratings and ongoing monitoring triggers, or preparing account opening procedures for SEC or FINRA examination. For the operational pipeline these controls plug into, see account-opening-workflow.

# Account Opening Compliance

## Core Concepts

### CIP Integration in Account Opening
The Customer Identification Program is the first compliance gate in any account opening workflow. Under USA PATRIOT Act Section 326 and its implementing regulations, a firm must verify the identity of each customer before or at the time of account opening. The account opening process must be designed so that no account becomes active until CIP is satisfied.

**Verification timing.** The regulations permit two approaches: (1) verify identity before the account is opened, which is the most conservative approach and prevents any transactional activity until verification is complete; or (2) verify identity within a reasonable time after the account is opened, provided the firm has procedures to manage the risk of incomplete verification (such as restricting account activity until verification is complete). Most firms implementing digital onboarding choose the first approach — identity verification occurs in real time during the application flow, and the application cannot proceed until verification returns a pass result. The second approach — opening with restricted activity pending verification — is used primarily for paper-based or advisor-assisted workflows where verification cannot occur in real time, and requires the firm to document the risk mitigation procedures (no trading, no disbursements, no margin until verification completes).

**Database verification** is the primary method for digital account opening. The onboarding system sends applicant data (name, date of birth, address, SSN/TIN) to an identity verification vendor (LexisNexis Risk Solutions, Alloy, Equifax, TransUnion) via API. The vendor cross-references the data against credit bureau records, public records, and government databases and returns a pass, fail, or inconclusive result, typically within seconds. Database verification satisfies CIP's non-documentary verification requirement.

**Documentary verification** serves as a fallback when database verification is inconclusive or unavailable. The applicant uploads a photo of a government-issued ID (driver's license, passport, state ID). OCR extracts data fields, and the system may compare the document photo to a selfie for liveness detection. Documentary verification is slower and introduces friction but is necessary for applicants who cannot be verified through database methods — non-US persons, thin-file individuals, and cases where database results are ambiguous.

**Verification failure handling.** The account opening workflow must define clear paths for each verification outcome:
- **Pass** — proceed to the next compliance gate
- **Fail** — halt the application; notify the applicant that the account cannot be opened; document the reason; retain records per CIP recordkeeping requirements
- **Inconclusive** — route to an exception queue for manual review; request additional identifying information or documentary verification; set a time limit for resolution (e.g., 5 business days) after which the application is closed

**Exception processing for inconclusive results** is operationally critical. Common causes of inconclusive results include name mismatches (legal name vs preferred name, hyphenated names, transliteration differences for non-English names), address mismatches (recent moves, PO boxes), and thin credit files (young adults, recent immigrants). The exception processing workflow should collect additional documentation, perform manual database searches, and escalate to compliance when standard exception procedures do not resolve the issue. The firm should track exception rates by cause to identify systemic issues — for example, a high rate of transliteration-related exceptions may indicate a need to improve the verification vendor's handling of non-Latin character sets.

**Non-US persons and foreign accounts.** CIP verification for non-US persons presents additional complexity. Acceptable identification numbers include a passport number and country of issuance, an alien identification card number, or a number and country of issuance of any other unexpired government-issued document evidencing nationality or residence that bears a photograph. Database verification coverage is weaker for non-US persons, making documentary verification (passport upload with liveness check) the primary method. The account opening workflow should detect non-US applicants early and route them to the documentary verification path without requiring a failed database check first.

**Recordkeeping requirements.** CIP regulations require retention of identifying information (name, date of birth, address, identification number), a description of the documents or methods used to verify identity, and the resolution of any discrepancies. These records must be retained for 5 years after the account is closed. The account opening system should automatically generate and store a CIP verification record for each application, including the verification method, vendor response, timestamp, and outcome.

### OFAC and Sanctions Screening
OFAC screening is a mandatory compliance gate that must clear before any account is opened. Unlike CIP, which verifies that the applicant is who they claim to be, OFAC screening determines whether the applicant — or any person associated with the account — is a sanctioned individual or entity with whom the firm is prohibited from doing business.

**Scope of screening.** The firm must screen all individuals associated with the account, not just the primary applicant. This includes:
- Account holders (all owners for joint accounts)
- Beneficial owners (25% equity holders and control persons for entity accounts)
- Authorized signers and persons with trading authority
- Trustees (for trust accounts)
- Custodians under UTMA/UGMA accounts
- Any other person with authority over or beneficial interest in the account

**Lists screened.** At minimum, screening must cover the OFAC SDN (Specially Designated Nationals and Blocked Persons) list. Best practice extends screening to the Sectoral Sanctions Identifications (SSI) list, the Non-SDN Menu-Based Sanctions list, the Foreign Sanctions Evaders (FSE) list, and consolidated non-OFAC lists such as the FinCEN 314(a) list and any firm-specific restricted lists. Automated screening platforms typically screen against all OFAC lists simultaneously.

**Screening frequency.** OFAC screening must occur at account opening and on an ongoing basis thereafter. Ongoing screening is triggered by: (1) OFAC list updates (the SDN list is updated frequently, sometimes multiple times per week), (2) changes to account ownership or authorized parties, and (3) periodic rescreening on a risk-based schedule. At account opening, the screening must occur before the account is activated and before any funds are accepted or transactions are processed.

**Potential match handling.** When the screening system generates a potential match (also called an alert), the workflow must:
1. Halt the account opening process — no account activation until the alert is resolved
2. Route the alert to a trained compliance analyst for manual review
3. Compare all available identifying information (full name, aliases, date of birth, nationality, address, passport number) between the applicant and the list entry
4. Determine whether the match is a true positive (the applicant is the listed person) or a false positive (a different person with similar identifying information)
5. Document the analysis, the data points compared, and the disposition decision
6. For true positives: block the account application, block any associated property, and file a blocked property report with OFAC within 10 business days
7. For false positives: document the basis for the determination, retain the record, and allow the application to proceed

**False positive management** is an ongoing operational challenge. Common names, transliteration variations, and incomplete identifying data on OFAC lists generate high false positive rates. Firms should tune their screening algorithms to balance detection sensitivity against operational burden. Reducing false positives without degrading detection requires maintaining and updating known false positive records, using multiple data points for matching (not just name), and calibrating fuzzy match thresholds. All tuning decisions must be documented and defensible.

**Documentation of screening results.** Regardless of outcome, the account opening record must include a log of every screening run: the lists screened, the individuals screened, the screening timestamp, the algorithm version or configuration, the raw results, and the disposition. For no-match results, the system log is sufficient. For potential matches resolved as false positives, the record must include the analyst's comparison of identifying data points and the rationale for the false-positive determination. For true positives, the record must include the blocking report, the notification to OFAC, and any subsequent correspondence. These records must be retained for the life of the account plus 5 years after closure and must be producible for regulatory examination.

### Beneficial Ownership Certification
The FinCEN CDD Rule (31 CFR 1010.230, effective May 2018) requires covered financial institutions to identify and verify the beneficial owners of legal entity customers at the time of account opening.

**Who must be identified.** For each legal entity customer, the firm must identify:
- Every individual who directly or indirectly owns 25% or more of the equity interests in the entity (the ownership prong)
- At least one individual who has significant responsibility for controlling, managing, or directing the entity — such as a CEO, CFO, COO, managing member, general partner, president, vice president, or treasurer (the control prong)

A single individual may satisfy both prongs (e.g., a sole owner who is also the manager). The maximum number of beneficial owners reported is typically five (four under the ownership prong plus one under the control prong), though an entity with more than four 25% owners must report all of them.

**25% ownership threshold.** Ownership is calculated on a direct and indirect basis. If an individual owns 30% of Entity A, and Entity A owns 100% of Entity B (the account applicant), the individual indirectly owns 30% of Entity B and must be identified as a beneficial owner. Multi-layered ownership structures require the firm to trace ownership through intermediate entities to identify the natural persons who ultimately hold 25% or more.

**Exempt entity types.** Certain entities are exempt from the beneficial ownership requirement because their ownership is already transparent through other regulatory mechanisms:
- Publicly traded companies listed on a US stock exchange (or a foreign exchange meeting equivalent standards)
- SEC-registered investment companies and investment advisers
- Insurance companies regulated by a state
- Banks, credit unions, and other depository institutions regulated by a federal banking agency
- Broker-dealers registered with the SEC
- Entities established by federal or state government
- Pooled investment vehicles operated by a financial institution (but not the underlying investors)

**Certification form management.** The firm collects beneficial ownership information on a certification form (based on FinCEN's standard form or the firm's equivalent). The account opening workflow must present this form when the applicant is a legal entity, collect the required information for each beneficial owner, and verify the identity of each identified beneficial owner using the firm's CIP procedures. The form must be signed (physically or electronically) by the individual opening the account on behalf of the entity, certifying the accuracy of the information. The firm must retain the certification form and verification records for 5 years after the account is closed.

**Ongoing monitoring for ownership changes.** The CDD Rule requires firms to update beneficial ownership information on a risk basis. The account opening process should establish triggers for ownership updates: periodic review (typically annually for high-risk entities, every 3 years for standard risk), event-driven updates (notification of ownership change, corporate restructuring, merger), and customer-initiated updates. The account opening system should flag the next review date and route it to the appropriate review queue.

**Corporate Transparency Act interaction.** The Corporate Transparency Act (CTA) originally required most companies to report beneficial ownership information directly to FinCEN beginning in 2024. As of FinCEN's March 2025 interim final rule, however, all entities formed in the United States (the former "domestic reporting companies") and their beneficial owners are exempt from CTA reporting; only entities formed under foreign law and registered to do business in the US remain reporting companies, and they need not report US-person beneficial owners. The practical consequence for account opening: CTA-reported data is not a substitute for the firm's own beneficial ownership collection, and the CTA does not relieve financial institutions of their CDD Rule obligations. Firms must continue to collect and verify beneficial ownership independently through the certification form process, and should verify the current state of CTA rulemaking, which remains in flux.

### Tax Compliance: FATCA and CRS
Account opening must collect information to satisfy international tax reporting obligations. These requirements apply regardless of the account holder's citizenship and are triggered by indicators of foreign tax residency.

**FATCA (Foreign Account Tax Compliance Act).** US financial institutions must determine whether account holders are US persons (requiring W-9 collection) or non-US persons (requiring W-8BEN or W-8BEN-E collection and FATCA classification). For entity accounts such as trusts, the firm must classify the entity under FATCA (e.g., Active NFFE, Passive NFFE, Financial Institution) and, for Passive NFFEs, identify any controlling persons who are US persons. Failure to collect valid W-8/W-9 forms triggers backup withholding at 24% on reportable payments.

**CRS (Common Reporting Standard).** If any account holder or controlling person is tax-resident in a CRS-participating jurisdiction (most countries outside the US), the firm must collect a self-certification of tax residency, including the foreign taxpayer identification number (TIN). For the family trust scenario with a UK-resident trustee, CRS requires reporting the account to HMRC via the firm's CRS reporting channel. The self-certification must be collected at or before account opening.

**Integration with account opening workflow.** The tax compliance gate should:
- Collect W-9 from all US persons and W-8BEN from all non-US persons at account opening
- Classify entity accounts under FATCA (Active/Passive NFFE, Financial Institution, etc.)
- Collect CRS self-certification forms from any person with foreign tax residency indicators
- Validate TIN format against the issuing country's known format (e.g., UK NI number format: 2 letters + 6 digits + 1 letter)
- Flag accounts with missing or expired tax forms for remediation before activation
- Set renewal triggers for W-8 forms (expire every 3 years unless a change of circumstances occurs)

**Cross-border complexity.** When account holders have tax obligations in multiple jurisdictions (e.g., a US-UK dual national, or a trust with trustees in different countries), the firm may need to report under both FATCA and CRS. The account opening system should identify multi-jurisdictional reporting obligations based on the tax residency declarations collected and route these accounts for compliance review.

### Suitability Assessment at Opening
Account opening is the primary data collection event for investment suitability. The compliance framework requires that the firm gather sufficient information to evaluate the suitability of any subsequent investment recommendation before or at the time of the first recommendation.

**Documenting the investment profile.** The account opening process must collect all elements of the customer's investment profile as defined by FINRA Rule 2111 and Regulation Best Interest: investment objectives, risk tolerance, time horizon, liquidity needs, financial situation (income, net worth, liquid net worth), investment experience, tax status, and any other information the customer discloses. The profile must be documented in a durable, retrievable format — not just captured in a questionnaire that is discarded after scoring.

**Mapping to appropriate products and models.** The suitability data collected at opening drives the mapping of the account to an investment model or strategy. The account opening system should produce a risk score or category from the suitability questionnaire and map that score to a defined range of models or strategies. This mapping must be documented, consistently applied across advisors, and periodically reviewed for reasonableness. Deviations from the mapping (e.g., an advisor selecting a more aggressive model than the client's risk score indicates) should trigger a compliance review.

**Reg BI care obligation for account type recommendation.** Under Regulation Best Interest, the recommendation of an account type itself (e.g., brokerage vs advisory, IRA vs taxable, fee-based vs commission-based) is subject to the Care Obligation. The account opening process for broker-dealers must document that the recommended account type is in the customer's best interest, considering reasonably available alternatives and the customer's investment profile. This means the compliance controls at account opening must capture not just the account type selected but the rationale for selecting it over alternatives.

**Suitability documentation requirements.** The firm must retain documentation of the customer's investment profile, the risk assessment or score, the recommended model or strategy, and the basis for the recommendation. For discretionary accounts, the investment policy statement (IPS) should be established at account opening. For Reg BI accounts, Form CRS must be delivered before or at the time of the recommendation, and the basis for the recommendation must be documented.

**Investment adviser fiduciary considerations at opening.** For RIA accounts, the fiduciary duty of care requires that the adviser understand the client's financial situation and investment objectives before making any recommendation. The account opening suitability questionnaire serves as the foundation for the adviser's duty of care analysis. The adviser must also identify and disclose any material conflicts of interest that may affect the advice provided. The account opening process should include delivery of Form ADV Part 2A and Part 2B (or the brochure supplement), collection of the client's acknowledgment of receipt, and execution of the investment advisory agreement. These disclosure obligations are not just suitability requirements — they are fiduciary obligations that, if not met at account opening, create ongoing compliance risk throughout the advisory relationship.

**Enhanced suitability review triggers.** Certain conditions detected during the account opening process should trigger an enhanced suitability review before the account is activated:
- The client selects an investment objective or risk tolerance inconsistent with their financial situation (e.g., aggressive growth with limited liquid net worth)
- The client requests products or features not typically consistent with their profile (e.g., options trading for a conservative investor)
- The client is a senior investor (age 65 or older)
- The client has limited investment experience and selects a complex strategy
- The client's stated time horizon is inconsistent with the account type (e.g., short-term horizon in a long-term retirement account)
- The client declines to provide certain suitability information — the firm must narrow the range of suitable recommendations accordingly and document the refusal
- The account involves a rollover from an employer plan, triggering Reg BI analysis of whether the rollover recommendation is in the customer's best interest compared to remaining in the plan

### Risk-Based Review Tiers
Not all account applications present the same compliance risk. A risk-based approach assigns each application to a review tier based on risk indicators, ensuring that higher-risk applications receive enhanced scrutiny while standard applications proceed efficiently.

**Standard review** applies to the majority of account openings: individual or joint taxable accounts, IRAs, and other common account types for US persons with clean CIP verification, clear OFAC screening, and a straightforward investment profile. Standard review may be fully automated — the system verifies that all compliance gates have passed and approves the application without manual intervention. An operations supervisor or compliance designee may review a sample of auto-approved accounts on a post-hoc basis.

**Enhanced review triggers.** The following indicators should escalate an application from standard to enhanced review, requiring manual compliance review before account activation:
- **Politically Exposed Persons (PEPs)** — foreign senior political figures, their family members, and close associates, as identified through PEP screening databases
- **High-risk jurisdictions** — applicants with citizenship, residence, or significant ties to countries identified as high risk by FATF, FinCEN advisories, or the firm's own risk assessment
- **Complex ownership structures** — multi-layered entities, nominees, trusts with opaque beneficiary structures, accounts with multiple authorized parties
- **Source of wealth concerns** — stated source of wealth inconsistent with known employment or business, unusually large initial funding amount relative to the applicant's profile, funds originating from high-risk jurisdictions
- **Negative media or adverse information** — screening results revealing adverse news, litigation, regulatory actions, or criminal history
- **Senior investors** — applicants age 65 or older, triggering age-based review under FINRA Rules 2165 and 4512
- **Large initial deposits** — funding amounts exceeding firm-defined thresholds (e.g., $1M or more) warranting source-of-funds review
- **Discretionary authority** — accounts granting trading discretion require supervisory review of the advisory agreement and investment authority

**Risk scoring at account opening.** Many firms assign a numeric risk score to each account at opening based on a weighted assessment of risk factors. Common scoring dimensions include:
- Customer type (individual, entity, trust, foreign national, PEP)
- Geographic risk (customer domicile, citizenship, fund flow jurisdictions)
- Product complexity (standard brokerage, advisory, margin, options, alternatives)
- Funding source (ACH from verified bank, wire from domestic bank, wire from foreign bank, third-party check)
- Relationship characteristics (new client, existing client opening additional account, referral source)
- Account size (accounts above defined thresholds warrant higher scores)

The risk score determines the initial CDD risk rating, which in turn drives the frequency and depth of ongoing monitoring. The scoring model should be documented, validated periodically, and applied consistently. Firms should avoid models that are so coarse that they assign nearly all accounts to the same tier, or so sensitive that they escalate a disproportionate share of routine accounts.

**Escalation to compliance.** When enhanced review is triggered, the application routes to a compliance analyst or compliance officer for manual review. The reviewer evaluates the risk factors, may request additional documentation from the applicant (source of funds statement, additional identification, purpose of account), and makes an approve/deny/escalate decision. If the reviewer cannot resolve the risk, the application escalates to senior compliance or the Chief Compliance Officer. All review decisions, supporting analysis, and documentation must be retained.

**Documentation requirements per tier.** Standard review requires retention of the automated compliance check results (CIP, OFAC, suitability score). Enhanced review requires, in addition: the specific risk factor(s) that triggered escalation, the reviewer's analysis, any additional documentation collected, the approval decision and rationale, and the identity of the approver. The documentation standard increases with risk tier — a PEP account, for example, should have a detailed memo explaining the source of wealth analysis and the basis for approval.

**Account denial procedures.** When compliance determines that an account should not be opened, the denial must be handled carefully. The firm should document the specific reasons for denial, retain the documentation in the compliance file, and communicate the denial to the applicant in a manner that does not reveal OFAC screening results or SAR-related information (to avoid tipping-off violations). The denial letter should state that the firm is unable to open the account at this time without providing the specific compliance reason. If the denial is related to OFAC or AML concerns, the firm should evaluate whether a SAR filing is warranted. Denied applications should be tracked in a centralized log to identify patterns (e.g., repeated attempts by the same individual to open accounts, or a pattern of denials from a particular referral source).

### Senior Investor Protections
Account opening for senior investors (generally age 65 and older, though some firms use age 60) triggers additional compliance obligations designed to protect against financial exploitation and diminished capacity.

**FINRA Rule 4512 — Trusted Contact Person.** Effective February 2018, FINRA Rule 4512 requires firms to make reasonable efforts to obtain the name and contact information of a trusted contact person for each customer's account. The trusted contact is not an authorized party — they cannot transact on the account. The purpose is to provide the firm with a resource to contact if the firm suspects financial exploitation, diminished capacity, or has concerns about the customer's welfare. The account opening process must include a trusted contact designation as a standard field, and the firm must make reasonable efforts to obtain this information for all customers, not just seniors. However, the trusted contact is particularly important for senior investors.

**FINRA Rule 2165 — Financial Exploitation of Specified Adults.** Effective February 2018, this rule provides a safe harbor for firms to place temporary holds on disbursements from the accounts of specified adults (persons age 65 or older, or persons age 18 or older who the firm reasonably believes have a mental or physical impairment that renders them unable to protect their own interests). At account opening, the firm should:
- Document the customer's age and any observable indicators of diminished capacity
- Explain the trusted contact person designation and its purpose
- Record the trusted contact information in the account record
- Flag the account in the firm's system for age-based monitoring and enhanced review

**Age-based triggers for enhanced review at opening.** When the applicant is 65 or older, the account opening process should trigger:
- Mandatory collection of trusted contact person information (with documentation of efforts if the customer declines)
- Enhanced suitability review — is the recommended account type, investment strategy, and product mix appropriate for the customer's age, time horizon, liquidity needs, and cognitive capacity?
- Review for potential financial exploitation indicators — is a third party exerting undue influence over the account opening? Is the customer being pressured into inappropriate products?
- State-specific protections — some states impose additional requirements (such as mandatory reporting of suspected elder financial exploitation) that the account opening process must accommodate

**Diminished capacity indicators** that may be observed during the account opening process:
- Confusion about the purpose of the account or the nature of the investment
- Inability to understand or recall information provided during the application
- Reliance on a third party to answer questions or make decisions
- Significant changes from previously known behavior or decision-making patterns (for existing clients opening new accounts)
- Inconsistent or contradictory responses to suitability questions

When these indicators are present, the firm should pause the account opening, document the observations, consult with a supervisor and potentially the trusted contact person, and determine whether proceeding is in the customer's interest.

**Temporary hold authority.** FINRA Rule 2165 authorizes the firm to place a temporary hold on a disbursement of funds or securities from the account of a specified adult if the firm reasonably believes that financial exploitation has occurred, is occurring, has been attempted, or will be attempted. The hold may last up to 15 business days, extendable to 25 business days if the firm has reported the matter to a state regulator or agency or court of competent jurisdiction. While this authority applies post-opening, the account opening process is the point at which the firm establishes the infrastructure — trusted contact, system flags, monitoring triggers — that enables effective use of hold authority when needed.

**State-level protections.** Many states have adopted their own senior investor protection statutes, often modeled on NASAA's Model Act to Protect Vulnerable Adults from Financial Exploitation. These state laws may impose mandatory reporting obligations (requiring the firm to report suspected exploitation to adult protective services or a state securities regulator), provide additional hold authority beyond FINRA Rule 2165, or create penalties for failure to report. The account opening compliance framework must identify the applicable state law based on the customer's residence and ensure that state-specific obligations are incorporated into the workflow.

### Compliance Automation
Manual compliance processes do not scale. As account volumes grow, firms must automate compliance screening, approval routing, exception tracking, and audit trail generation to maintain both efficiency and control quality.

**Automated screening workflows.** The core compliance checks at account opening — CIP verification, OFAC screening, PEP screening, negative media screening, and beneficial ownership verification for entities — should execute automatically as the application progresses through the workflow. Each screening step fires via API call, the result is captured in the application record, and the workflow engine advances or halts the application based on the result. No manual intervention is required for applications that pass all screens.

**Rules-based approval routing.** The workflow engine should evaluate each application against a configurable rules set to determine the approval path:
- Applications passing all automated screens with no enhanced review triggers route to auto-approval (or to a light-touch operations review)
- Applications with one or more enhanced review triggers route to the appropriate reviewer based on the nature of the trigger (compliance analyst for OFAC alerts, senior compliance for PEPs, operations supervisor for documentation issues)
- Applications with multiple concurrent triggers or the highest-risk indicators route to the CCO or a senior compliance committee

The rules engine must be configurable by compliance (not hardcoded by IT), auditable (all rule changes logged with effective dates and approver), and testable (new rules can be validated against historical applications before deployment).

**Compliance checklist automation.** Each account type has a defined set of compliance requirements. The system should generate an automated checklist at the start of each application based on the account type and features, track completion of each item, and prevent submission until all required items are satisfied. The checklist should be visible to the operations team, the advisor, and compliance. Example checklists by account type:

- **Individual taxable:** CIP verification (pass), OFAC screening (clear), suitability questionnaire (complete), risk score (generated), Form CRS (delivered), privacy notice (delivered), trusted contact (collected or documented refusal), new account form (signed)
- **Entity (LLC/Corp):** All individual checklist items for each authorized party, plus: entity classification (documented), beneficial ownership certification (complete), beneficial owner CIP verification (pass for each), beneficial owner OFAC screening (clear for each), formation documents (collected), corporate resolution or operating agreement (collected), EIN verification (confirmed), compliance review (approved)
- **Trust:** Trustee CIP verification (pass for each), trust classification (revocable vs irrevocable — documented), trust certification or agreement (collected), beneficial ownership determination (documented with rationale), OFAC screening for all associated persons, compliance review if irrevocable or complex structure
- **IRA/Retirement:** Standard individual checklist, plus: IRA adoption agreement (signed), beneficiary designation (complete), IRA disclosure statement (delivered), rollover/transfer documentation (if applicable), Reg BI analysis for rollover recommendation (if applicable)

**Exception tracking.** When an application enters an exception state (inconclusive CIP, OFAC potential match, missing documentation, triggered enhanced review), the system must track the exception from creation through resolution. Exception tracking should include: the exception type, the date raised, the assigned reviewer, the current status, the resolution (approved, denied, pending additional information), the resolution date, and the supporting documentation. Aging exception reports should surface applications that have been in exception status beyond defined thresholds (e.g., 3 business days for CIP exceptions, 1 business day for OFAC alerts).

**Audit trail generation.** Every compliance action during the account opening process must be logged in an immutable audit trail: who performed the action, what the action was, when it occurred, and the result. This includes automated actions (system ran OFAC screening at 14:23:07 — result: no match) and manual actions (compliance analyst J. Smith reviewed OFAC alert #4521 at 15:10:22 — disposition: false positive — rationale: different date of birth and passport number). The audit trail must be retained for the life of the account plus the applicable regulatory retention period (5-6 years after account closure) and must be producible for regulatory examinations.

**Compliance dashboard for the opening pipeline.** A real-time dashboard provides compliance and operations management with visibility into the account opening pipeline: total applications in progress, applications by stage, applications in exception status, aging exceptions, approval rates, auto-approval rates, average time-to-open, and NIGO rates. The dashboard enables compliance to identify bottlenecks, staffing needs, and emerging risk patterns (e.g., a spike in OFAC alerts from a particular region).

**Vendor management for compliance screening.** Most firms rely on third-party vendors for identity verification, OFAC screening, PEP databases, and adverse media feeds. The compliance automation framework must include vendor oversight: initial due diligence on the vendor's data sources and accuracy rates, contractual service-level agreements (SLAs) for response time and uptime, periodic validation testing (running known positives and known negatives through the vendor's system to verify accuracy), and contingency procedures for vendor outages. If the screening vendor is unavailable, the firm must have a fallback process — manual screening against downloadable OFAC lists, for example — to avoid either opening accounts without screening or halting all account openings during the outage.

**Regulatory technology (RegTech) considerations.** The compliance automation landscape is evolving rapidly. Firms evaluating RegTech solutions for account opening compliance should assess: integration capabilities with existing account opening platforms and custodian APIs; configurability of screening rules and thresholds by compliance (not requiring developer intervention); quality of audit trail and reporting outputs; ability to handle multi-entity, multi-jurisdiction screening in a single workflow; and the vendor's regulatory track record (has the vendor's technology been examined by regulators, and what were the findings?). The firm should retain ownership of the compliance decision — automation assists but does not replace compliance judgment on escalated cases.

### Ongoing Monitoring Triggers Set at Opening
The account opening process does not end when the account is activated. The compliance decisions made at opening establish the framework for ongoing monitoring throughout the life of the account.

**CDD risk rating assignment.** Every account receives a CDD risk rating at opening (e.g., low, medium, high, or a numeric score). The risk rating is derived from the risk factors assessed during the opening process: customer type, geographic exposure, product complexity, source of wealth, PEP status, and any enhanced review findings. The risk rating determines the intensity and frequency of ongoing monitoring — high-risk accounts receive more frequent transaction monitoring, periodic reviews, and closer scrutiny of unusual activity.

**Event-driven review triggers.** The account opening process should establish the events that will trigger a compliance review during the life of the account:
- Material changes to account ownership or authorized parties
- Significant changes to the investment profile (objectives, risk tolerance, financial situation)
- Large deposits or withdrawals inconsistent with the established account activity pattern
- Transactions involving high-risk jurisdictions
- Addition of margin, options, or other features that increase risk
- OFAC list updates that produce a new potential match against existing account holders
- Negative media hits on account holders or beneficial owners
- Customer reaching age 65 (triggering senior investor protections)
- Customer complaint or litigation involving the account
- Death of an account holder or beneficial owner
- Regulatory inquiry or subpoena involving the account holder
- Significant change in account balance (increase or decrease) beyond expected thresholds
- Account inactivity for an extended period followed by sudden high-volume activity

**Periodic review scheduling.** Based on the CDD risk rating assigned at opening, the system should schedule the next periodic review: annually for high-risk accounts, every 2-3 years for medium-risk accounts, and every 3-5 years for low-risk accounts. The periodic review confirms that the customer's profile remains current, the risk rating remains appropriate, and no new risk factors have emerged.

**Account activity monitoring thresholds.** The account opening process should establish baseline expectations for account activity based on the customer's profile, account type, and stated purpose. These baselines feed into the firm's transaction monitoring system, which generates alerts when activity deviates significantly from expectations. For example, an account opened for "long-term retirement savings" that begins executing high-frequency trades should generate an alert for compliance review.

**Handoff from opening compliance to ongoing compliance.** The transition from account opening to the ongoing compliance lifecycle must be explicit and documented. When the account opening process is complete, the system should transmit the following to the ongoing monitoring infrastructure: the CDD risk rating, the beneficial ownership record (for entities), the next scheduled periodic review date, any conditions of approval imposed during enhanced review (e.g., "monitor for source-of-funds consistency for the first 6 months"), the trusted contact person record, and the suitability profile. This handoff ensures that the compliance decisions made at opening are not lost and that ongoing monitoring reflects the risk assessment established during the opening process. A gap in the handoff — for example, an account approved with conditions but no system to track compliance with those conditions — is a significant control weakness.

## Worked Examples


Three worked examples — automated compliance screening for a high-volume broker-dealer, beneficial ownership verification for complex entity structures (ownership tracing, trust classification), and a four-tier risk-based review framework (auto-approval through CCO review, with $500K and $2M funding thresholds) — are in [references/examples.md](references/examples.md); load it when designing a concrete screening, beneficial ownership, or review-tier program.

## Common Pitfalls
- Opening an account before CIP verification is complete — the PATRIOT Act requires verification before or at account opening, and "reasonable time after" is narrowly construed by examiners
- Screening only the primary account holder against OFAC and neglecting joint owners, trustees, beneficial owners, and authorized signers — all associated individuals must be screened
- Collecting the FinCEN beneficial ownership certification form but not verifying the identities of the reported beneficial owners — the CDD Rule requires both identification and verification
- Not tracing indirect ownership through intermediate entities — a natural person owning 40% of a parent entity that owns 100% of the applicant entity is a 40% beneficial owner and must be reported
- Applying the same review intensity to every application regardless of risk — this overwhelms compliance resources and paradoxically reduces scrutiny of high-risk accounts
- Treating suitability data collection as a box-checking exercise rather than gathering actionable information that drives investment decisions and compliance review
- Failing to document the rationale for account type recommendations under Reg BI — the account type itself is a recommendation subject to the Care Obligation
- Not obtaining trusted contact information for senior investors or failing to document reasonable efforts when the customer declines
- Relying on manual OFAC screening processes that cannot keep pace with frequent list updates — screening must be automated and triggered by list changes
- Hardcoding compliance rules in the workflow system without providing compliance with the ability to modify rules as regulations and firm policies evolve
- Generating compliance audit trails that record outcomes but not rationale — examiners want to see not just what decision was made but why
- Setting CDD risk ratings at account opening and never updating them — risk ratings must be dynamic, responsive to new information and changing circumstances
- Allowing exception queues to age without escalation — a stale exception is an unresolved compliance risk that grows with time
- Not coordinating account opening compliance across affiliated entities (e.g., a broker-dealer and an investment adviser under common ownership opening accounts for the same client) — this can create duplicative or inconsistent compliance records
- Failing to track the FinCEN 2024 final rule extending BSA/AML requirements to SEC-registered investment advisers — its effective date was postponed from January 1, 2026 to January 1, 2028 (FinCEN final rule, December 2025), and FinCEN intends to revisit the rule's substance before then; advisers should monitor the rulemaking and verify current status rather than assume the 2026 obligations apply
- Overlooking state-level senior investor protection statutes that may impose reporting obligations beyond what FINRA rules require

## Cross-References
- **know-your-customer** (compliance plugin): Defines the CIP, CDD, and ongoing monitoring requirements that this skill implements within the account opening workflow
- **anti-money-laundering** (compliance plugin): OFAC screening, SAR filing, and AML program requirements that intersect with account opening compliance gates
- **investment-suitability** (compliance plugin): Suitability obligations that drive the investment profile data collection at account opening
- **reg-bi** (compliance plugin): Regulation Best Interest's Care and Disclosure Obligations that apply to account type recommendations and initial investment recommendations at opening
- **account-opening-workflow** (client-operations plugin): The operational account opening process into which these compliance controls are embedded; this skill focuses on the compliance layer, that skill on the operational flow
- **client-onboarding** (advisory-practice plugin): The broader client onboarding experience that encompasses account opening compliance as one component of the end-to-end onboarding process
- **privacy-data-security** (compliance plugin): Protection of sensitive personal information (SSN, financial data, identity documents) collected during the account opening compliance process
- **examination-readiness** (compliance plugin): Preparing account opening compliance documentation and procedures for regulatory examination
- **books-and-records** (compliance plugin): Recordkeeping requirements for CIP records, OFAC screening results, beneficial ownership certifications, and suitability documentation generated during account opening
- **sales-practices** (compliance plugin): Ongoing senior investor protections (FINRA Rules 2165/4512 temporary holds and conduct standards) that build on the trusted contact and senior-review infrastructure established at account opening

### Referencia: references/examples.md

# Account Opening Compliance — Worked Examples

## Example 1: Implementing automated compliance screening for a high-volume broker-dealer
**Scenario:** A broker-dealer processing 2,000 new account applications per month wants to automate its compliance screening to reduce manual review from 60% of applications to under 15% while maintaining or improving compliance quality. The firm currently uses a semi-manual process: operations staff run CIP checks via a vendor portal, manually enter names into an OFAC screening tool, and route every entity account and every application with any flag to compliance for manual review. Average time-to-open is 8 business days. The compliance team of 4 analysts spends 70% of its time on routine account opening reviews, leaving insufficient capacity for genuinely high-risk cases.

**Design Approach:**

The firm should implement an automated compliance screening workflow with the following architecture:

**CIP integration.** Replace the vendor portal with a direct API integration to the identity verification vendor. When the applicant submits their personal information, the system sends an API request and receives a pass/fail/inconclusive result in real time. Pass results advance automatically. Fail results halt the application with a notification to the applicant. Inconclusive results route to an exception queue with a 3-business-day resolution window. This eliminates manual CIP entry for the estimated 85% of applications that return a clean pass.

**OFAC and sanctions screening.** Replace the standalone OFAC screening tool with an integrated screening platform that runs automatically against all OFAC lists, the FinCEN 314(a) list, and the firm's internal restricted list. Screening fires for every individual associated with the application — account holders, joint owners, trustees, beneficial owners, and authorized parties. The screening platform should use multi-field matching (name plus date of birth plus nationality) to reduce false positives. Results are written directly to the application record. No-match results advance automatically. Potential matches route to a compliance analyst with the matching data pre-populated for efficient review.

**PEP and negative media screening.** Add automated PEP screening and adverse media screening as parallel checks. These screens run simultaneously with OFAC screening to avoid adding sequential delay. Results are evaluated by the rules engine: PEP matches trigger enhanced review; negative media hits are scored by severity, and only those exceeding a defined threshold trigger manual review. The PEP database should cover both foreign and domestic PEPs, including family members and close associates, and should be updated at least monthly by the vendor.

**Entity account handling.** Entity accounts (LLCs, corporations, partnerships, trusts) cannot be fully auto-approved due to the beneficial ownership certification requirement and the need to review formation documents. However, automation can still reduce manual effort: the system collects beneficial ownership data through a structured workflow, runs CIP verification and OFAC screening on each identified beneficial owner and control person in parallel, and assembles the compliance checklist for the operations or compliance reviewer. The reviewer then focuses on verifying that the ownership structure is accurately captured, that the entity classification is correct, and that no enhanced review triggers are present — rather than performing all screening manually.

**Rules-based routing.** Configure the workflow rules engine to evaluate each application against the enhanced review trigger criteria. Applications that pass all automated screens and have no enhanced review triggers are auto-approved and advance to document completion and custodian submission. Applications with one or more triggers route to the appropriate review queue. The rules engine should be configurable by the compliance team through an administrative interface, with all rule changes logged and effective-dated.

**Expected outcome.** With automated CIP, OFAC, PEP, and negative media screening plus rules-based routing, the firm should achieve auto-approval for 80-85% of standard individual and joint account applications. Enhanced review would be required for approximately 10-15% of applications (entity accounts, OFAC alerts, PEP hits, senior investors, high-risk indicators). Manual compliance review would focus exclusively on genuinely elevated-risk applications, improving both efficiency and compliance quality. Average time-to-open for auto-approved accounts should drop to 1-3 business days. The compliance team's time on routine reviews should decrease from 70% to approximately 20%, freeing capacity for enhanced review, ongoing monitoring, and program improvement.

**Monitoring and continuous improvement.** After deployment, the firm should track key metrics monthly: auto-approval rate by account type, false-positive rate for OFAC and PEP screening, average time-to-open by tier, exception resolution time, and any compliance issues discovered post-opening that the automated screening should have caught. A compliance issue discovered post-opening (for example, an account holder who appears on an updated OFAC list shortly after opening, or a beneficial owner who was not screened due to a data entry error) should trigger a root-cause analysis and a rule or process adjustment. The compliance team should conduct quarterly reviews of a statistically significant sample of auto-approved accounts to validate that the auto-approval criteria remain appropriate.

**Examination defensibility.** The firm should document the design rationale for the automated screening workflow, including: why each screening vendor was selected, how match thresholds were calibrated, what the false-positive and false-negative rates are, how the rules engine was tested, and what post-implementation quality assurance measures are in place. Examiners will want to see that the firm validated the automated process produces results at least as reliable as manual review, and that the firm conducts periodic testing to confirm the system is functioning as designed. The firm should maintain a testing log showing the dates and results of periodic validation tests run against the screening system, including tests with known positive matches to confirm detection capability.

## Example 2: Designing beneficial ownership verification for complex entity structures
**Scenario:** A wealth management firm specializing in high-net-worth and institutional clients frequently opens accounts for complex entity structures: multi-member LLCs, family limited partnerships, tiered holding company structures, and irrevocable trusts with corporate trustees. The firm's current beneficial ownership process collects the FinCEN certification form but does not consistently verify the identities of reported beneficial owners or trace indirect ownership through intermediate entities. A recent internal audit found that 30% of entity accounts had incomplete beneficial ownership records.

**Design Approach:**

**Structured data collection.** Replace the single-form approach with a structured data collection workflow that dynamically adjusts based on entity type. When the applicant selects an entity account type, the system presents an entity classification questionnaire: What type of entity? Is it publicly traded? Is it a regulated financial institution? Is it a government entity? Affirmative answers to the exemption questions bypass beneficial ownership collection (with the exemption documented). Non-exempt entities proceed to the ownership data collection module.

**Ownership tracing for multi-layered structures.** The data collection module must handle indirect ownership. For each entity in the ownership chain, the system asks: Who owns 25% or more of this entity? If the answer is another entity (not a natural person), the system adds that intermediate entity to the chain and repeats the question. The process continues until every 25%+ ownership path terminates at a natural person. The system should present this as a visual ownership diagram that the applicant and the compliance reviewer can inspect. For example, if Client LLC is owned 50% by Holding Co. A and 50% by Holding Co. B, the system must identify the natural persons who own 25%+ of Holding Co. A and Holding Co. B, and if any of those natural persons' indirect ownership of Client LLC reaches 25%, they must be reported.

**Identity verification for beneficial owners.** Each identified beneficial owner must be verified through the firm's CIP procedures. The system should collect the same identifying information required for account holders (name, date of birth, address, SSN or passport number) and run the same database verification. OFAC screening must also be performed on each beneficial owner. The account cannot be opened until all beneficial owners are identified, verified, and screened.

**Control person identification.** Separately from the ownership prong, the system must collect information on at least one control person — an individual with significant managerial responsibility. The system should present common titles (CEO, CFO, managing member, general partner, president) and allow the applicant to identify the control person. The control person must also be verified and screened.

**Ongoing ownership monitoring.** The system should schedule a periodic ownership review based on the entity's risk rating. At each review, the firm contacts the entity's authorized representative to confirm whether ownership has changed. If ownership has changed, the firm collects updated beneficial ownership information, verifies new beneficial owners, and updates the account record. Corporate events (mergers, acquisitions, changes in management) should also trigger ownership review.

**Remediation of existing accounts.** For the 30% of entity accounts with incomplete records, the firm should prioritize remediation by risk rating: high-risk entities first, then medium, then low. The remediation process contacts each entity, collects complete beneficial ownership information, verifies identities, runs OFAC screening, and updates the account record. A remediation tracking report should be maintained for examination purposes, showing the scope of the issue, the remediation plan, progress, and completion.

**Common failure points in entity beneficial ownership.** The most frequent deficiencies found in entity account compliance are: (1) collecting only direct owners and missing indirect owners through intermediate entities; (2) accepting a certification signed by an unauthorized individual (the form must be signed by someone authorized to act on behalf of the entity); (3) failing to update ownership information after a known corporate event such as a merger or change in management; (4) not verifying the identity of beneficial owners with the same rigor applied to account holders; and (5) incorrectly classifying an entity as exempt when it does not meet the specific exemption criteria. The structured workflow described above addresses each of these failure points by building verification, tracing, and classification into the data collection process rather than relying on manual post-hoc review.

**Trust account classification.** Trusts present particular beneficial ownership complexity. Revocable (living) trusts where the grantor retains control are generally treated as individual accounts for CDD purposes — the grantor is the beneficial owner. Irrevocable trusts, however, are legal entities subject to full beneficial ownership requirements. The firm must determine: who are the beneficiaries with 25%+ interests? Who is the trustee with control? For trusts with discretionary distribution provisions (where the trustee has sole discretion over distributions), identifying 25% owners can be challenging because beneficial interests are not fixed. The firm should document its methodology for classifying trust types and identifying beneficial owners, and apply that methodology consistently. When the trust instrument grants the trustee broad discretion, the trustee is typically identified as the control person, and the firm should make reasonable efforts to identify any beneficiaries with ascertainable interests of 25% or more.

## Example 3: Building risk-based review tiers for account opening compliance
**Scenario:** A dually registered broker-dealer and investment adviser opens accounts across a range of client types: retail individuals, high-net-worth families, small businesses, institutional investors, and foreign nationals. The firm currently applies a uniform compliance review to all account applications — every application is reviewed by a compliance analyst before activation, regardless of risk. This creates a bottleneck: the compliance team reviews 800 applications per month, average review time is 45 minutes per application, and the backlog causes a 5-7 business day delay for even the simplest individual accounts. The firm wants to implement a risk-based review framework that maintains compliance quality while reducing time-to-open for low-risk accounts.

**Design Approach:**

**Tier 1 — Auto-Approval (target: 65-70% of applications).** Criteria: US individual or joint taxable account, standard IRA, or Roth IRA; applicant age under 65; clean CIP pass (database verification); OFAC screening no match; no PEP match; no negative media hits above threshold; suitability profile within standard parameters (no enhanced suitability triggers); funding amount below firm-defined threshold (e.g., $500,000); no discretionary authority. Compliance controls: all automated screening must pass; the system generates a compliance checklist and confirms all items are satisfied; the application auto-advances to document completion and custodian submission. Post-hoc quality assurance: a compliance analyst reviews a random 5-10% sample of auto-approved applications weekly to validate the auto-approval rules are working correctly.

**Tier 2 — Operations Review (target: 15-20% of applications).** Criteria: accounts that do not meet auto-approval criteria but do not trigger compliance-level review. Examples include: applicants age 65 or older (trusted contact review), standard entity accounts (LLC, corporation) with straightforward ownership, accounts with minor documentation issues, funding amounts between $500,000 and $2M, accounts requiring feature additions (margin, options level 1-2). Review process: an operations supervisor reviews the application, confirms compliance screenings have passed, verifies documentation completeness, and addresses any minor issues. Target review time: 15-20 minutes. Escalation path: if the operations reviewer identifies a compliance concern, the application escalates to Tier 3.

**Tier 3 — Compliance Review (target: 10-15% of applications).** Criteria: OFAC potential match requiring disposition, PEP match, high-risk jurisdiction connection, complex entity structure (multi-layered ownership, trusts with corporate trustees), source of wealth concerns, negative media above threshold, high-value accounts (above $2M), discretionary authority with complex mandate, foreign national applicants, inconclusive CIP requiring manual resolution. Review process: a compliance analyst performs a full review of the application, risk factors, supporting documentation, and screening results. The analyst may request additional information from the applicant. Target review time: 30-60 minutes. The analyst documents the review findings, risk assessment, and approval/denial decision.

**Tier 4 — Senior Compliance / CCO Review (target: 1-3% of applications).** Criteria: confirmed PEP accounts, applicants from comprehensively sanctioned or highest-risk jurisdictions, accounts with multiple concurrent high-risk indicators, accounts where the compliance analyst recommends escalation, accounts requiring an exception to firm policy. Review process: the senior compliance officer or CCO reviews the application with the compliance analyst's findings and recommendation. The reviewer may consult legal counsel. Approval requires a documented memorandum explaining the risk assessment, mitigating factors, and conditions of approval (e.g., enhanced ongoing monitoring, periodic review schedule, transaction limits).

**Implementation and calibration.** The tier thresholds and criteria should be calibrated using historical data: analyze the last 12 months of account applications, classify each into the proposed tiers, and verify that the risk distribution aligns with expectations. After implementation, monitor the quality metrics: are auto-approved accounts (Tier 1) generating disproportionate compliance issues downstream? Are Tier 3 reviews catching genuine risks, or are they producing a high rate of approvals with no conditions? Adjust tier criteria quarterly based on these findings. All calibration decisions should be documented for examination purposes.

**Expected outcome.** Tier 1 auto-approval eliminates 65-70% of applications from the manual review queue. Tier 2 operations review handles routine but non-automatable applications at one-third the time of the current uniform review. Tier 3 compliance review focuses analyst time on genuinely elevated-risk applications. Tier 4 reserves senior compliance capacity for the highest-risk decisions. Total compliance analyst time on account opening should decrease by approximately 60%, average time-to-open for Tier 1 accounts should drop to 1-2 business days, and compliance quality on high-risk accounts should improve due to increased focus and available capacity.

**Governance and oversight.** The risk-based review framework requires ongoing governance: a quarterly review of tier distribution and outcomes, annual recalibration of tier criteria based on actual risk experience, documentation of all calibration decisions, and reporting to senior management and the board (or compliance committee) on the framework's effectiveness. The firm should maintain a matrix showing, for each tier, the volume of applications, the approval/denial rate, the average review time, and any subsequent compliance issues (regulatory findings, customer complaints, suspicious activity) that emerged after approval. This data enables evidence-based refinement of the tier boundaries and demonstrates to examiners that the firm is actively managing its risk-based approach rather than setting it and forgetting it.

**Regulatory examination considerations.** Examiners reviewing a risk-based framework will focus on three areas: (1) whether the tier criteria are reasonable and capture known risk indicators; (2) whether the firm is actually following the tiered process (are Tier 3 applications truly getting full compliance review, or are they being rubber-stamped?); and (3) whether the quality assurance and calibration processes are functioning. The firm should be prepared to produce sample files from each tier to demonstrate that the review depth matches the tier specification.


---

## SKILL: account-opening-ops

- Fuente: `SYasJ/claude-business-skills` → `plugins/banking/skills/account-opening-ops` (MIT)
- Cuándo usarla: Review an account-opening checklist for identity steps they require, without collecting secrets into the chat. Use when the user mentions account opening, KYC checklist, onboarding a customer bank, new account ops, or asks for a account-opening checklist. Banking and treasury operations skill by Yasir Jilani.

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'account-opening-ops' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Account Opening Operations

Review an account-opening checklist for identity steps they require, without collecting secrets into the chat.

## When to use this skill

Use this skill when the user:

- account opening
- KYC checklist
- onboarding a customer bank
- new account ops

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

This is not a credit decision and not an instruction to move money. Do not request online-banking passwords, one-time codes, or card PINs.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Their required steps
- What is complete
- Exceptions
- The reviewer

## Workflow


### 1. Step 1

Use their checklist. Do not invent a regulator's rule.
### 2. Step 2

Note missing identity steps as gaps.
### 3. Step 3

Do not ask customers to send passwords or full card data by chat.
### 4. Step 4

Exceptions need their compliance owner.
### 5. Step 5

A possible sanctions match follows their screening process. Do not suggest altering a name.
### 6. Step 6

This is operations support, not a license to open the account.

## Output

Deliver a **account-opening checklist**.

- Purpose of this account-opening checklist, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs an account-opening checklist by 30 September 2026. Staff want to skip an identity step because the customer is in a hurry.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Staff want to skip an identity step because the customer is in a hurry.

Their required steps: Payment run 14 Sep; Account opening file 221. Both unassigned as of 14 September 2026
What is complete: Liquidity ladder, last reviewed 14 September 2026. No owner named since
Exceptions: Payment run 14 Sep is open. Account opening file 221 was raised verbally and never logged
The reviewer: Priya Shah. No second reviewer named
```

### Example outcome

**Account-opening checklist**
Northline Studio · 14 September 2026 · Due 30 September 2026

**Decision**
Keeps the step and routes any exception to the compliance owner.

**Checklist**

- [x] **Their required steps** — Payment run 14 Sep; Account opening file 221. Both unassigned as of 14 September 2026  
      Evidenced in the file
- [x] **What is complete** — Liquidity ladder, last reviewed 14 September 2026. No owner named since  
      Evidenced in the file
- [x] **Exceptions** — Payment run 14 Sep is open. Account opening file 221 was raised verbally and never logged  
      Evidenced in the file
- [ ] **The reviewer** — Priya Shah. No second reviewer named  
      Open — nothing in the file closes this

**The gates this list enforces, in order**

1. Use their checklist. Do not invent a regulator's rule
2. Note missing identity steps as gaps
3. Do not ask customers to send passwords or full card data by chat
4. Exceptions need their compliance owner
5. A possible sanctions match follows their screening process. Do not suggest altering a name

**Deliberately not done**
- Invented regulatory rules.
- Name changes to dodge screening.
- Secrets collected in chat.

**Stop rule**
Do not mark this pack complete while a box above is open. An open box is a finding, not a formality — it is the thing this checklist exists to catch.

Next: Priya Shah closes the open items before 30 September 2026.

## Anti-patterns

- Invented regulatory rules
- Name changes to dodge screening
- Secrets collected in chat

## Related skills

- `sanctions-compliance-process`


---

## SKILL: account-opening-workflow

- Fuente: `JoelLewis/finance_skills` → `plugins/client-operations/skills/account-opening-workflow` (MIT)
- Cuándo usarla: Design and operate back-office account opening pipelines from application intake through custodian submission and activation. Use when building account opening automation, reducing NIGO rejection rates from custodians or clearing firms, defining document requirements for trusts, entities, IRAs, or estate accounts, setting up multi-custodian account opening across Schwab, Fidelity, or Pershing, troubleshooting account opening failures or processing delays, or benchmarking cycle times and first-submission acceptance rates. For risk-based approval tiers and compliance screening requirements, see account-opening-compliance.

# Account Opening Workflow

## Core Concepts

### Account Type Determination and Registration
Account type determination is the foundational decision in the account opening workflow. The registration type dictates the document requirements, approval gates, tax treatment, titling rules, and custodian submission path. Operations teams must maintain a comprehensive account type matrix that maps each registration type to its downstream processing requirements.

**Individual and joint registration types:**
- **Individual** — single natural person as owner; titled in the individual's legal name; SSN as TIN; simplest registration and the baseline for all account opening processes
- **Joint Tenants with Right of Survivorship (JTWROS)** — two or more co-owners with equal, undivided interest; on death of one owner, the surviving owner(s) automatically inherit the deceased owner's share without probate; all owners must sign account opening documents; titled as "John Smith and Jane Smith JTWROS"
- **Tenants in Common (TIC)** — two or more co-owners with specified ownership percentages (need not be equal); on death, the deceased owner's share passes to their estate, not to the surviving co-owner(s); ownership percentages must be recorded and may affect tax reporting; titled as "John Smith and Jane Smith TIC"
- **Community Property** — available only in community property states (Arizona, California, Idaho, Louisiana, Nevada, New Mexico, Texas, Washington, Wisconsin); assets acquired during marriage are jointly owned; specific titling and tax implications vary by state; some custodians treat community property accounts differently from other joint account types
- **Community Property with Right of Survivorship** — a hybrid available in some community property states that combines community property tax treatment with automatic survivorship; not all custodians support this registration type

**Trust registration types:**
- **Revocable (living) trust** — grantor retains control and can modify or revoke the trust; typically titled as "John Smith, Trustee of the Smith Family Trust dated 01/15/2020"; grantor's SSN is often used as TIN; account opening requires trust certification or relevant pages of the trust agreement showing trust name, date, trustees, and investment powers
- **Irrevocable trust** — grantor has permanently relinquished control; separate tax entity requiring its own EIN; beneficial ownership certification required under FinCEN CDD Rule; titled in the trust's legal name with trustee designation; requires more extensive documentation including the full trust agreement or comprehensive trust certification
- **Testamentary trust** — created by a will and comes into existence upon the grantor's death; requires letters testamentary, death certificate, and court-certified copy of the will provisions creating the trust; account opening is typically manual due to the complexity and variation in court documentation

**Entity registration types:**
- **LLC (Limited Liability Company)** — requires articles of organization, operating agreement (or certificate of formation in some states), EIN, beneficial ownership certification; titled in the LLC's legal name; operating agreement must authorize the opening of investment accounts and identify authorized signers
- **Corporation (C-Corp and S-Corp)** — requires articles of incorporation, bylaws, corporate resolution authorizing the account and designating authorized signers, EIN, beneficial ownership certification; S-Corp election (IRS Form 2553) may be relevant for tax reporting but does not change account opening requirements
- **Partnership (General Partnership, Limited Partnership, LLP)** — requires partnership agreement, EIN, identification of general partner(s) who have authority to act on behalf of the partnership; limited partners typically do not have signing authority unless specified in the partnership agreement
- **Sole Proprietorship** — may use the individual's SSN or a separate EIN; requires DBA documentation if operating under a trade name; some custodians treat sole proprietorship accounts as individual accounts with a DBA designation

**Retirement account types:**
- **Traditional IRA** — tax-deductible contributions (subject to income limits if the owner participates in an employer plan), tax-deferred growth, required minimum distributions beginning at age 73 (SECURE 2.0; rises to 75 in 2033); requires IRA adoption agreement, beneficiary designation, and IRA disclosure statement
- **Roth IRA** — after-tax contributions, tax-free qualified distributions, no RMDs during the owner's lifetime; same documentation requirements as Traditional IRA plus verification of Roth eligibility (income limits)
- **SEP IRA** — employer-funded; contributions up to 25% of compensation or the annual dollar limit; requires SEP plan document (IRS Form 5305-SEP or prototype plan) and IRA adoption agreement; employer must execute the plan document before the account can be opened
- **SIMPLE IRA** — salary deferral plus employer match or non-elective contribution; requires SIMPLE plan document (IRS Form 5304-SIMPLE or 5305-SIMPLE) and SIMPLE IRA adoption agreement; must be established between January 1 and October 1 of the plan year
- **Inherited IRA** — beneficiary account established upon the death of the original IRA owner; subject to the 10-year distribution rule for most non-spouse beneficiaries under the SECURE Act; requires death certificate, beneficiary verification, and custodian-specific inherited IRA application; titled as "Jane Smith, Beneficiary of John Smith, Deceased"
- **Rollover IRA** — receives funds from an employer-sponsored plan (401(k), 403(b), 457); may be direct rollover (trustee-to-trustee) or indirect rollover (60-day); requires rollover paperwork and often a letter of acceptance from the receiving custodian

**Custodial and estate accounts:**
- **UTMA/UGMA** — custodian (typically a parent or grandparent) manages assets for a minor until the age of majority (18 or 21 depending on state and UTMA vs UGMA); the minor is the beneficial owner and the account is titled in the minor's SSN; titled as "John Smith, Custodian for Jane Smith under the [State] UTMA"
- **Estate** — opened to manage assets of a deceased person during probate; requires letters testamentary (if there is a will) or letters of administration (if intestate), death certificate, and EIN for the estate; titled as "Estate of John Smith, Deceased"; personal representative or executor is the authorized signer

**Account numbering and classification:**
- Account numbers are assigned by the custodian or clearing firm upon successful account creation; the firm's internal systems may maintain a separate internal account identifier that maps to the custodian account number
- Account classification codes are used for regulatory reporting (Form 13F, FOCUS reports, customer protection rule computations); classification must accurately reflect the account type, tax status, and beneficial ownership
- Multi-custodian firms must maintain a cross-reference between internal account identifiers and custodian-specific account numbers
- Account numbering schemes at custodians typically encode the account type, branch, or registration category within the number structure; operations teams should understand each custodian's numbering conventions for troubleshooting and reconciliation

### Document Requirements Matrix
The document requirements matrix is the operational backbone of account opening. It defines exactly which documents are required for each combination of account type, account features, and custodian. A well-maintained matrix prevents NIGO rejections, ensures regulatory compliance, and enables automation.

**Universal documents (required for all account types):**
- New account application form (custodian-specific; each custodian has its own form with different fields and formatting)
- W-9 (Request for Taxpayer Identification Number) for US persons, or W-8BEN (individuals) / W-8BEN-E (entities) for non-US persons
- Advisory agreement (for advisory accounts) or brokerage agreement (for brokerage accounts)
- Form CRS (Client Relationship Summary) — delivery acknowledgment
- Privacy notice (Regulation S-P) — delivery acknowledgment
- Trusted contact person designation (FINRA Rule 4512)

**Type-specific documents:**
- Joint accounts: joint account agreement specifying the ownership type (JTWROS, TIC, community property); signatures of all account holders
- Trust accounts: trust certification (or relevant pages of the trust agreement) showing trust name, date of formation, trustee names and powers, successor trustee provisions, and investment authority; trust EIN (irrevocable trusts); beneficial ownership certification (irrevocable trusts and certain revocable trusts depending on the custodian)
- Entity accounts: formation documents (articles of incorporation/organization, partnership agreement), governing documents (bylaws, operating agreement), authorizing resolution (corporate resolution, LLC member resolution, or partner authorization designating authorized signers and authorizing the account), EIN assignment letter, beneficial ownership certification form (FinCEN)
- IRA accounts: IRA adoption agreement, beneficiary designation form (primary and contingent beneficiaries), IRA disclosure statement, transfer/rollover forms (if funding from another retirement account or employer plan)
- Estate accounts: letters testamentary or letters of administration (court-certified), death certificate, EIN assignment letter for the estate, court order appointing the personal representative or executor
- Custodial accounts (UTMA/UGMA): custodial account agreement, minor's SSN, custodian's identification

**Feature-specific documents:**
- Margin: margin agreement, margin risk disclosure document; some custodians require a separate margin application
- Options: options agreement, OCC Characteristics and Risks of Standardized Options document acknowledgment; options approval level must be specified and may require additional documentation for higher levels
- Check writing and debit card: separate application for cash management features
- Discretionary authority: limited power of attorney or discretionary trading authorization signed by the client; investment advisory agreement with discretionary language

**Custodian-specific variations:**
Each custodian maintains its own form library, field requirements, and validation rules. The operations team must maintain custodian-specific document matrices and update them when custodians revise their requirements. Common variations include: different account application forms, different signature requirements (e.g., one custodian requires a separate signature page while another accepts signatures on the application), different beneficial ownership forms, and different trust certification formats. Failure to track custodian-specific variations is a major source of NIGO rejections.

### Application Processing Workflow
The application processing workflow is the sequence of steps from initial receipt of account opening request through account number assignment and confirmation. A well-designed workflow manages state transitions, enforces required gates, and provides visibility to all stakeholders.

**Workflow stages:**

1. **Receipt and intake** — the account opening request arrives from the advisor (via onboarding platform, CRM, email, or paper). The operations team logs the request, assigns it a tracking number, and records the timestamp. For firms with service-level agreements, the clock starts here.

2. **Initial review and triage** — an operations analyst reviews the request for completeness at a high level: is the account type clear, are the basic client details present, are the required documents attached. Requests are triaged by complexity: standard accounts (individual, joint, IRA) go to the automated or streamlined path; complex accounts (trusts, entities, estates) go to a specialized review queue.

3. **Data entry or import** — client data is entered into the firm's account opening system or imported from the onboarding platform. For API-integrated onboarding, this step is automated. For manual submissions, operations staff key in client information from the application forms. Data entry is a significant source of errors; validation rules should flag inconsistencies in real time.

4. **Document completeness check** — the operations analyst verifies that all required documents are present based on the document requirements matrix. This is a systematic, checklist-driven review: for the given account type plus features plus custodian, are all required documents attached, signed, and complete. Missing or incomplete documents trigger a NIGO hold and a request back to the advisor or client.

5. **Data validation** — automated and manual checks verify data consistency across all documents: name matches between application, W-9, and advisory agreement; SSN/EIN matches across forms; account type coding is consistent; address is complete and formatted correctly; beneficiary designations are complete for retirement accounts. Validation rules should be codified and automated wherever possible.

6. **Supervisory review** — certain account types and configurations require supervisory or compliance review before custodian submission. Triggers include: discretionary accounts, options trading approval, margin requests, accounts for senior investors (age 65+), PEP or EDD-flagged clients, high-net-worth thresholds, accounts with complex ownership structures. The supervisor reviews the application package, suitability documentation, and any compliance flags, then approves, rejects, or requests additional information.

7. **Custodian submission** — the validated and approved application package is submitted to the custodian via API, custodian portal, or manual upload. API submission is the target for standard account types; complex accounts often require portal or manual submission. The operations team records the submission timestamp and method.

8. **Custodian processing and account number assignment** — the custodian reviews the submission, runs its own validation, and either creates the account (returning an account number) or rejects it (NIGO). Processing time varies: API submissions for standard accounts may return an account number within minutes; manual submissions for complex accounts may take days to weeks. The operations team monitors submission status and follows up on aging submissions.

9. **Confirmation and notification** — upon receiving the account number, the operations team updates internal systems (CRM, PMS, billing), notifies the advisor and client, and triggers post-opening activities (funding, model assignment, welcome kit). The confirmation should include the account number, registration details, and any next steps required from the advisor or client.

**Workflow state management:**
Each account opening request should have a defined state at all times: received, in-review, pending-documents, pending-supervisory-review, pending-compliance, submitted-to-custodian, NIGO-hold, approved, activated, or closed/withdrawn. State transitions should be logged with timestamps, responsible party, and any notes. A dashboard showing the distribution of requests across states enables operations management to identify bottlenecks, aging items, and capacity issues.

### NIGO Management
NIGO (Not In Good Order) rejections are the single largest source of delay, cost, and client dissatisfaction in account opening operations. A systematic approach to NIGO management includes prevention, categorization, remediation, tracking, and root cause analysis.

**Common NIGO causes and prevention strategies:**
- **Missing signatures** (typically 20-30% of NIGOs) — prevented by automated signature detection in document review, e-signature platforms that enforce all signature blocks before completion, and pre-submission validation that checks for blank signature fields
- **Data inconsistencies** (15-25%) — name on W-9 does not match account application; address differs between forms; SSN/EIN mismatch. Prevented by single-entry data collection that propagates to all forms, and cross-document validation rules
- **Missing documents** (15-20%) — trust certification not included for trust account; beneficial ownership form missing for entity; beneficiary designation missing for IRA. Prevented by the document requirements matrix with automated checklists that block submission until all required documents are present
- **Incorrect account type coding** (10-15%) — the account type on the application does not match the registration details or the custodian's account type codes. Prevented by mapping tables between the firm's account types and each custodian's type codes, with validation at submission
- **Incomplete beneficiary designations** (5-10%) — missing contingent beneficiaries, percentages that do not sum to 100%, missing beneficiary SSNs for retirement accounts. Prevented by beneficiary form validation rules
- **Expired or invalid identity documents** (5-10%) — government ID has expired, W-8BEN has passed its three-year validity period. Prevented by document expiration tracking and pre-submission date validation
- **Missing beneficial ownership** (5-10%) — entity accounts submitted without the FinCEN beneficial ownership certification. Prevented by requiring the form as a mandatory document for all entity account types

**NIGO categorization:**
NIGOs should be categorized by: (1) custodian — to identify custodian-specific patterns, (2) rejection reason — using a standardized taxonomy of NIGO codes, (3) account type — to identify which account types have the highest rejection rates, (4) originating advisor or office — to identify training needs, (5) severity — distinguishing between minor corrections (e.g., missing initials) and substantive deficiencies (e.g., missing trust agreement). This categorization enables targeted remediation and process improvement.

**Remediation workflows:**
When a NIGO is received: (1) the operations team logs the rejection, categorizes it, and assigns it to an analyst; (2) the analyst determines the specific corrective action required; (3) if the correction can be made by operations (e.g., re-keying a data field), it is corrected and resubmitted; (4) if the correction requires the advisor or client (e.g., a missing signature, an additional document), the analyst contacts the advisor with a clear, specific request describing exactly what is needed; (5) a follow-up schedule is established (e.g., 2-day follow-up, 5-day escalation to the advisor's manager, 10-day escalation to operations management); (6) once the correction is received, the application is revalidated and resubmitted; (7) the NIGO is closed and the resolution is recorded.

**NIGO tracking and reporting:**
- **NIGO rate** — total NIGO rejections divided by total submissions, measured weekly and monthly; segmented by custodian, account type, and advisor/office
- **NIGO aging** — average time from NIGO receipt to resolution; distribution of open NIGOs by age (0-2 days, 3-5 days, 6-10 days, 10+ days)
- **First-submission acceptance rate** — the inverse of the NIGO rate; the percentage of applications accepted on first submission
- **Root cause distribution** — the percentage of NIGOs attributable to each cause category, tracked over time to measure the effectiveness of prevention initiatives
- **NIGO rate benchmarking** — industry benchmarks: best-in-class firms achieve NIGO rates below 5%; average firms operate at 10-20%; firms without automated validation often exceed 25%

### Regulatory Holds and Approval Gates
Regulatory holds and approval gates are control points in the account opening workflow where processing pauses until a specific review or approval is completed. These gates enforce compliance requirements, manage risk, and ensure appropriate oversight of complex or high-risk account openings.

**Supervisory approval requirements:**
- **Discretionary accounts** — accounts where the advisor has discretionary trading authority require supervisory review and approval before activation. The supervisor verifies that the client has granted discretionary authority in writing, that the investment strategy is suitable, and that the advisor is authorized by the firm to exercise discretion. FINRA Rule 3110 requires firms to designate a supervisor for discretionary account activity.
- **Options trading approval** — options approval requires assessment of the client's knowledge, experience, financial situation, and investment objectives. Most custodians use a tiered approval system (e.g., levels 0-4) with increasing levels requiring greater client sophistication and financial capacity. The registered options principal (ROP) or designated supervisor must approve the options level. Higher levels (e.g., uncovered options writing) require enhanced review.
- **Margin accounts** — margin trading requires disclosure delivery, client acknowledgment of margin risks, and supervisory approval. The supervisor reviews suitability of margin for the client's financial situation and investment objectives. Regulation T, FINRA Rules 4210 and 2264 govern margin requirements and disclosures.

**Compliance review triggers:**
- **Politically exposed persons (PEPs)** — clients identified as PEPs through screening trigger enhanced due diligence review before account opening. Compliance reviews source of wealth, source of funds, and the purpose of the account. Senior management approval is typically required.
- **Enhanced due diligence (EDD) clients** — clients from high-risk jurisdictions, with complex ownership structures, or with adverse media hits trigger EDD review. The compliance team conducts a deeper investigation before the account can be opened.
- **Senior investors** — clients age 65 and older trigger age-based review; the senior investor protection requirements (FINRA Rules 2165 and 4512, trusted contact procedures) are covered in account-opening-compliance.
- **High-net-worth thresholds** — firms require elevated review for accounts above defined funding thresholds (illustratively, operations-level review above $500K and compliance review above $2M; account-opening-compliance defines the canonical risk-based review tiers).
- **Concentrated positions** — clients transferring in concentrated stock positions may trigger review to ensure the concentration risk is acknowledged and addressed in the investment strategy.

**Hold management and aging:**
Accounts in regulatory hold must be tracked with: the date the hold was placed, the reason for the hold, the assigned reviewer, and the expected resolution date. Hold aging reports should highlight items approaching or exceeding the firm's service-level targets. Typical targets: supervisory review within 2 business days, compliance review within 5 business days, escalation at 10 business days.

**Escalation procedures:**
When a hold exceeds its target resolution time, the workflow should automatically escalate: first to the assigned reviewer's manager, then to the chief compliance officer or operations director, and finally to senior management. Escalation notifications should include the account details, the hold reason, the elapsed time, and any prior communications.

### Account Opening Automation and STP
Straight-through processing (STP) is the goal of account opening automation: the application flows from submission through account creation without manual intervention. Achieving high STP rates requires investment in technology, data quality, and process standardization.

**STP architecture:**
- **Data collection layer** — onboarding platform or advisor portal collects client data through structured forms with real-time validation. Data is captured once and propagated to all downstream forms and systems.
- **Validation engine** — a rules-based engine that checks every application against the document requirements matrix, custodian-specific validation rules, and regulatory requirements before submission. The engine produces a pass/fail result with specific error messages for any failures.
- **Document assembly** — automated generation of custodian-specific forms, pre-populated with validated client data. Form templates are maintained for each custodian and updated when custodians revise their forms.
- **Custodian integration** — API connections to custodian account opening systems for automated submission and status tracking. The integration handles authentication, data mapping (translating the firm's data model to the custodian's API schema), error handling, and response processing.
- **Exception routing** — applications that fail validation or require manual review are routed to the appropriate operations or compliance queue. STP handles the standard cases; exception-based processing handles the rest.
- **Status tracking and notification** — real-time visibility into the status of every account opening request, with automated notifications to advisors, clients, and operations staff at key milestones.

**OCR and data extraction:**
For firms that still receive paper applications or scanned documents, optical character recognition (OCR) and intelligent document processing (IDP) can extract data from forms and documents. Modern IDP platforms use machine learning to identify document types, extract field values, and flag low-confidence extractions for human review. OCR accuracy varies by document quality; validation against the client's profile data helps catch extraction errors.

**Automated validation rules:**
The validation engine should enforce rules including: all required fields populated and formatted correctly, SSN/EIN passes check-digit validation, name matches across all documents (fuzzy matching to handle minor variations), address is valid and complete (USPS address validation), account type code maps correctly to the custodian's type codes, all required documents are present per the document requirements matrix, all signature fields are completed, beneficiary percentages sum to 100% for retirement accounts, trust certification includes all required elements (trust name, date, trustees, powers), and beneficial ownership certification is complete for entity accounts.

**STP rate measurement:**
- **STP rate** — the percentage of account opening requests that flow from submission to account creation without any manual intervention. Measured overall and segmented by account type, custodian, and advisor.
- **Target STP rates by account type:** Individual taxable accounts: 85-95%; joint accounts: 80-90%; IRA accounts: 75-85%; trust accounts: 30-50%; entity accounts: 20-40%; estate accounts: under 10% (nearly always require manual processing).
- **Exception rate** — the inverse of STP rate; the percentage of applications requiring manual intervention. The goal is to minimize exceptions while maintaining quality and compliance.
- **Time-to-account-number** — elapsed time from submission to custodian account number assignment. For STP-eligible accounts, the target is minutes to hours. For manual accounts, measure against custodian-specific SLA targets.
- **Automation ROI** — compare the cost per account opened before and after automation. Include operations staff time, NIGO remediation cost, advisor time spent on corrections, and technology platform costs. Firms with mature STP typically achieve 60-70% reduction in per-account operations cost for standard account types.

### Multi-Custodian Operations
Firms that custody client assets across multiple custodians (commonly Schwab, Fidelity, Pershing, and others) face additional complexity in account opening. Each custodian has its own forms, validation rules, API specifications, processing timelines, and NIGO patterns.

**Managing custodian-specific requirements:**
- Maintain a separate document requirements matrix for each custodian, updated whenever the custodian revises its forms or requirements
- Map the firm's internal account type codes to each custodian's type codes; discrepancies in type mapping are a frequent source of NIGO rejections
- Maintain custodian-specific form templates for automated document assembly
- Track each custodian's API capabilities and limitations; not all account types are supported via API at all custodians
- Document each custodian's NIGO patterns and common rejection reasons; use this data to build custodian-specific validation rules

**Custodian-specific form requirements (representative examples):**
- Schwab: uses the Schwab Institutional new account application; supports API-based account opening for most standard account types; trust accounts require the Schwab trust certification form
- Fidelity: uses the Fidelity Institutional new account application; API support varies by account type; entity accounts often require manual submission through the Fidelity portal
- Pershing: uses the Pershing new account form (NAF); supports account opening through the NetX360 platform; has specific requirements for options and margin paperwork separate from the main application

**Parallel vs sequential submission:**
When a client is opening accounts at multiple custodians simultaneously (e.g., a trust account at Schwab and an IRA at Fidelity), the operations team must decide whether to submit in parallel or sequentially. Parallel submission is faster but requires the operations team to manage multiple concurrent workflows. Sequential submission is simpler to manage but extends the total processing time. Best practice: submit in parallel when the operations team has capacity and the account types are independent; submit sequentially when the accounts have dependencies (e.g., the IRA rollover depends on the trust account being established first).

**Cross-custodian reconciliation:**
After accounts are opened, the operations team must reconcile the firm's internal records with each custodian's records to ensure: account numbers are correctly mapped, registration details match, account features (margin, options) are correctly reflected, and beneficiary designations are consistent. Discrepancies discovered during reconciliation must be resolved promptly before the account is activated.

### Account Activation and Post-Opening
Account activation is the transition from "account created at custodian" to "account fully operational and ready for trading." Post-opening activities ensure the account is properly funded, configured, and integrated into the firm's systems.

**Funding verification:**
- Verify that the funding method initiated during onboarding is proceeding: ACH transfers should settle within 2-4 business days, wires within 1 business day, ACAT transfers within 4-6 business days
- For accounts funded by ACAT transfer, monitor the transfer status and resolve any rejected or partial transfers promptly
- For IRA rollovers, verify that the rollover is direct (trustee-to-trustee) or that the 60-day deadline for indirect rollovers is tracked
- Flag unfunded accounts at 10, 20, and 30 days; unfunded accounts that remain inactive beyond the custodian's inactivity threshold may be closed by the custodian

**Model portfolio assignment:**
- For discretionary accounts, link the funded account to the appropriate model portfolio in the portfolio management system (PMS) based on the client's risk profile and investment objectives
- Generate the initial rebalancing trades to align the account with the target model; the first trade may require advisor confirmation depending on the firm's policies
- For accounts funded via in-kind transfer (ACAT with existing positions), assess the transferred positions against the target model and develop a transition trading plan that considers tax implications, concentrated positions, and market conditions

**Initial trading enablement:**
- Verify that the account is configured for the correct trading capabilities: cash-only, margin-enabled, options-approved (at the correct level)
- For accounts with options or margin, verify that the custodian has activated these features and that the internal systems reflect the correct permissions
- Place any initial trades and confirm execution

**Welcome kit delivery:**
- Send the client a welcome package confirming the account opening, summarizing account details and features, providing login credentials for client-facing portals, and including any required disclosures not previously delivered
- Welcome communications should be customized by account type and may include educational materials about the client's specific account features

**30-day review:**
- Conduct a post-opening review at 30 days to verify: the account is funded, initial investments are in place and aligned with the investment strategy, all documentation is complete and filed, the client and advisor have no outstanding questions or issues, and the account data is consistent across all systems (CRM, PMS, custodian, billing)
- Any discrepancies or open items identified in the 30-day review must be resolved and documented

**Account maintenance handoff:**
- After the 30-day review, the account transitions from the account opening workflow to the ongoing account maintenance process
- The operations team records the account as fully onboarded and closes the account opening tracking record
- Ongoing activities (rebalancing, billing, performance reporting, regulatory filings) are managed through the account maintenance and servicing workflows

## Worked Examples

Three worked examples (multi-custodian RIA workflow design, NIGO reduction through automated pre-submission validation, and tiered approval workflows for complex account types) are in [references/examples.md](references/examples.md) — load it when designing or benchmarking a concrete account opening process.

## Common Pitfalls
- Treating account opening as a single uniform process rather than designing differentiated workflows by account type complexity — individual accounts and entity accounts have fundamentally different processing requirements
- Maintaining the document requirements matrix in spreadsheets or tribal knowledge rather than encoding it in the account opening system as enforced validation rules
- Not tracking custodian-specific form versions, leading to submissions on outdated forms that are automatically rejected
- Routing all complex accounts through a single approval queue instead of specialized queues with risk-based differentiation
- Allowing custodian submission before all required supervisory and compliance approvals are documented
- Not establishing clear SLAs for each stage of the account opening workflow, making it impossible to identify and address bottlenecks
- Failing to close the feedback loop between NIGO rejections and process improvement — tracking NIGO rates without analyzing root causes and implementing preventive controls
- Not verifying account data consistency across internal systems (CRM, PMS, billing, custodian) after account opening, leading to downstream errors in billing, reporting, and trading
- Treating account activation as automatic upon account number assignment — accounts should not be activated until funding is verified, model assignment is confirmed, and the 30-day review process is initiated
- Assuming that a single set of validation rules works across all custodians — each custodian has unique requirements that must be codified and maintained separately
- Not tracking unfunded accounts, which results in accounts being opened but never funded, wasting operations capacity and potentially violating custodian inactivity policies
- Building account opening automation without investing in exception handling — even the best STP systems will have exceptions, and the exception handling workflow must be as well-designed as the automated path
- Opening entity accounts without verifying that the authorized signer has legal authority to act on behalf of the entity — a corporate resolution or operating agreement authorizing the account must be obtained and reviewed, not just collected
- Failing to distinguish between revocable and irrevocable trusts during intake, leading to incorrect application of beneficial ownership requirements and potential CDD Rule violations
- Not maintaining a log of account opening processing times by stage, which prevents the operations team from identifying systemic delays and measuring the impact of process improvements
- Neglecting to reconcile account features (margin, options levels, check writing) between the firm's internal records and the custodian's records after opening — mismatches can cause trade rejections or unauthorized activity

## Cross-References
- **client-onboarding** (advisory-practice plugin): Covers the front-office, advisor-facing onboarding workflow that feeds into the back-office account opening process described in this skill; client-onboarding handles prospect intake, identity verification, suitability collection, and e-signature, while account-opening-workflow handles the operations processing, custodian submission, and account activation
- **account-maintenance** (client-operations plugin): Accounts transition from the account opening workflow to the account maintenance workflow after the 30-day post-opening review; maintenance covers ongoing updates to registration, beneficiaries, features, and documentation
- **know-your-customer** (compliance plugin): KYC/CIP requirements define the identity verification and due diligence standards that the account opening workflow must satisfy; KYC policies determine which clients require enhanced review during account opening
- **investment-suitability** (compliance plugin): Suitability data collected during onboarding is validated during the account opening supervisory review; the suitability profile must support the account type, features (margin, options), and investment strategy before the account is activated
- **client-disclosures** (compliance plugin): Disclosure delivery requirements (Form CRS, Form ADV, privacy notice, margin and options disclosures) must be satisfied at or before account opening; the account opening workflow must track and confirm disclosure delivery
- **books-and-records** (compliance plugin): Account opening documents, signed agreements, and approval records are books and records subject to retention requirements under SEC Rules 17a-3/17a-4 and Rule 204-2; the account opening workflow must ensure all documents are properly stored and indexed
- **portfolio-management-systems** (advisory-practice plugin): The PMS receives new accounts from the account opening workflow for model portfolio assignment and initial trading; the account opening confirmation triggers the PMS to associate the account with the appropriate model
- **anti-money-laundering** (compliance plugin): OFAC screening and AML checks are mandatory gates in the account opening workflow; accounts flagged by AML screening enter regulatory hold until compliance review is complete
- **account-opening-compliance** (client-operations plugin): Defines the regulatory requirements (CIP/KYC, suitability verification, OFAC screening, beneficial ownership) that the account opening workflow must enforce as processing gates; the compliance skill defines what must be checked, and this skill describes the operational workflow that implements those checks
- **fee-billing** (advisory-practice plugin): New accounts must be configured in the billing system with the correct fee schedule, billing method, and inception date; account opening confirmation triggers billing system setup
- **margin-operations** (trading-operations plugin): Margin account opening requires additional approval gates, documentation, and custodian configuration beyond standard account opening; the margin operations skill covers ongoing margin management after the account is opened and margin is activated

### Referencia: references/examples.md

# Account Opening Workflow — Worked Examples

## Example 1: Designing an account opening workflow for a multi-custodian RIA operations team
**Scenario:** A registered investment adviser with $3B AUM and 80 advisors operates across three custodians: Schwab (60% of assets), Fidelity (30%), and Pershing (10%). The firm opens approximately 400 new accounts per month. The current process is fragmented: each custodian has a separate submission workflow, validation is manual, and the NIGO rate averages 18% across custodians (12% at Schwab, 22% at Fidelity, 28% at Pershing). The operations team of 8 people spends approximately 40% of their time on account opening and NIGO remediation. The firm wants to implement a unified account opening workflow that achieves a first-submission acceptance rate above 90% and reduces operations time spent on account opening to 20%.

**Design Considerations:**
- The unified workflow must abstract custodian-specific differences behind a common interface. The advisor enters client data and selects the account type once; the system handles the translation to custodian-specific forms, validation rules, and submission methods.
- The document requirements matrix must be custodian-aware: for the same account type (e.g., irrevocable trust), the required documents differ across Schwab, Fidelity, and Pershing. The system must present the correct requirements based on the selected custodian.
- API integration is the priority for Schwab (highest volume); Fidelity may support API for some account types; Pershing submission through NetX360 may require semi-automated screen integration or file upload.
- The validation engine must maintain separate rule sets for each custodian. For example, Schwab may require the trust certification in a specific format, while Fidelity accepts a broader range of trust documentation.

**Analysis:**
The recommended architecture has four layers:

Layer 1 — Unified data collection: The advisor or client enters account opening information through a single intake form in the onboarding platform. The form dynamically adjusts required fields based on the account type and selected custodian. Data is entered once and stored in a normalized data model.

Layer 2 — Custodian-specific translation: The system maps the normalized data to each custodian's specific form fields, account type codes, and document requirements. This translation layer is maintained as a configuration — not hard-coded — so that updates to custodian requirements can be made by operations staff without software development. Form templates for each custodian are populated automatically from the translated data.

Layer 3 — Validation and pre-submission review: Before submission, the validation engine runs the custodian-specific rule set against the complete application package. Rules check for: all required fields populated, data consistency across documents, all required documents present and signed, account type code correctly mapped, and any custodian-specific requirements (e.g., Pershing's specific options paperwork format). Applications that pass validation proceed to submission. Applications that fail are returned to the advisor with specific, actionable error messages.

Layer 4 — Submission and tracking: For Schwab, API submission with automated status polling. For Fidelity, API submission where supported, with portal-based submission for unsupported account types. For Pershing, file-based or portal-based submission. All submissions are tracked in a single dashboard regardless of custodian, with status updates, aging alerts, and NIGO management in one view.

Expected outcomes: The custodian-specific validation engine should reduce the overall NIGO rate from 18% to below 8% within 90 days. Automated form population eliminates data inconsistency errors. The unified dashboard gives operations management visibility across all custodians. The 40% time allocation should decrease to approximately 20% as manual validation, form completion, and status checking are automated.

## Example 2: Implementing NIGO reduction through automated pre-submission validation
**Scenario:** A broker-dealer processes 600 new account applications per month through a single clearing firm. The firm's NIGO rate is 32%, resulting in approximately 192 rejections per month. Each NIGO takes an average of 4 business days to resolve, consuming significant operations capacity. Analysis of the past 6 months of NIGO data reveals the following distribution: missing signatures (28%), data inconsistencies between forms (22%), missing required documents (18%), incorrect account type codes (12%), incomplete beneficiary designations (10%), other (10%). The firm wants to reduce the NIGO rate to below 8%.

**Design Considerations:**
- The top three NIGO categories (missing signatures, data inconsistencies, missing documents) account for 68% of all rejections and are all preventable through automated validation.
- Missing signatures can be detected by e-signature platforms that enforce all signature blocks, or by OCR-based signature detection for paper forms.
- Data inconsistencies are best prevented by single-entry data collection where the advisor enters data once and the system populates all forms, eliminating the opportunity for inconsistency.
- Missing documents are prevented by the document requirements matrix enforced as a submission gate — the system will not allow submission until all required documents for the account type and features are present.

**Analysis:**
Phase 1 — Signature enforcement (weeks 1-4): Implement e-signature as the default signing method for all account opening documents. Configure the e-signature platform to require all signature blocks to be completed before the ceremony can be finalized. For the small percentage of accounts that still require paper signatures, implement a signature verification checklist that operations must complete before submission. Expected impact: missing signatures are 28% of all NIGOs, which is 28% of the 32% NIGO rate — approximately 9 percentage points of total submission volume. Eliminating 80-90% of signature-related NIGOs reduces the overall NIGO rate by approximately 7-8 percentage points, from 32% to approximately 24-25%.

Phase 2 — Single-entry data propagation (weeks 3-8): Replace manual multi-form data entry with a single data collection workflow that populates all custodian forms automatically. The advisor enters the client's name, SSN, address, and account details once; the system generates all required forms with consistent data. Implement cross-form validation that flags any remaining inconsistencies before submission. Expected impact: eliminate 80-90% of data inconsistency NIGOs, reducing the NIGO rate by an additional 5-6 percentage points (to approximately 18-19%).

Phase 3 — Document completeness gate (weeks 5-10): Build the document requirements matrix as a system-enforced checklist. For each account type and feature combination, the system lists every required document and blocks submission until all items are checked off. Integrate with the document management system to verify that uploaded documents match the required list. Expected impact: eliminate 80-90% of missing document NIGOs, reducing the NIGO rate by an additional 4-5 percentage points (to approximately 13-14%).

Phase 4 — Account type code mapping and beneficiary validation (weeks 8-12): Implement automated account type code mapping that translates the firm's account type selection to the clearing firm's specific codes, eliminating manual code entry. Build beneficiary validation that verifies percentages sum to 100%, all required fields are populated, and primary and contingent designations are complete. Expected impact: reduce the remaining NIGO causes by an additional 5-6 percentage points (to approximately 8-9%).

Cumulative expected outcome: The four phases should reduce the NIGO rate from 32% to approximately 8-9% within 12 weeks of full implementation. The remaining 8-9% will consist of edge cases, custodian-side processing errors, and account types not yet covered by the automation. Continued monitoring and rule refinement should bring the rate below 8% within 6 months.

## Example 3: Building approval workflows for complex account types
**Scenario:** An independent broker-dealer and RIA with 300 advisors opens approximately 150 complex accounts per month: 60 trust accounts (40 revocable, 20 irrevocable), 50 entity accounts (30 LLCs, 15 corporations, 5 partnerships), 25 estate accounts, and 15 accounts requiring discretionary authority combined with options trading. Currently, all complex accounts go into a single compliance review queue, creating a bottleneck with average approval time of 7 business days. The firm wants to reduce average approval time to 2 business days while maintaining compliance quality.

**Design Considerations:**
- Not all complex accounts require the same level of review. Revocable trusts where the grantor is the sole trustee are relatively straightforward; irrevocable trusts with multiple beneficiaries and trustees require deeper review. The approval workflow should differentiate by risk level, not just account type.
- Entity accounts have specific regulatory requirements (beneficial ownership certification under the CDD Rule) that must be verified before opening. The reviewer must confirm that all 25% owners and at least one control person have been identified and verified.
- Estate accounts involve unique documentation (letters testamentary, death certificates) and require verification that the personal representative has legal authority to act. These are often time-sensitive due to estate settlement deadlines.
- Discretionary accounts with options trading combine two separate approval requirements: supervisory review of discretionary authority and options approval by the registered options principal (ROP). These can be structured as parallel reviews to reduce total approval time.

**Analysis:**
The single-queue model is the root cause of the bottleneck. Replace it with a tiered, parallel approval workflow:

Tier 1 — Automated pre-screening (target: same-day): Before any human review, run automated checks on all complex accounts. Automated checks include: document completeness against the type-specific requirements matrix, beneficial ownership form completeness for entity accounts, trust certification element verification (trust name, date, trustees, powers), CIP/OFAC screening status confirmation, and suitability data completeness. Accounts that pass all automated checks are pre-approved for human review with a green flag; accounts with deficiencies are returned to the advisor immediately with specific correction requests. This prevents reviewers from spending time on incomplete applications.

Tier 2 — Differentiated review queues: Route pre-screened accounts to specialized review queues based on complexity and risk:
- Queue A (revocable trusts, simple LLCs with one or two members): Assign to operations analysts with trust and entity training. Target review time: 1 business day. The review confirms trust certification elements, verifies trustee authority, confirms beneficial ownership (if applicable), and approves for custodian submission.
- Queue B (irrevocable trusts, multi-member entities, partnerships): Assign to senior operations analysts or compliance staff. Target review time: 2 business days. The review includes everything in Queue A plus: full beneficial ownership verification, source-of-funds review for irrevocable trusts, partnership authority verification, and enhanced scrutiny of complex ownership structures.
- Queue C (estate accounts): Assign to a specialist who handles all estate accounts. Target review time: 2 business days. The review verifies letters testamentary or administration, confirms the personal representative's authority, validates the estate EIN, and coordinates with the advisor on any court-imposed restrictions.
- Queue D (discretionary + options): Split into two parallel reviews. The supervisory review of discretionary authority is assigned to the branch manager or designated supervisor. The options approval is assigned to the ROP. Both reviews run concurrently, and the account is approved when both are complete. Target: 2 business days for the slower of the two reviews.

Tier 3 — Escalation for high-risk cases: Within any queue, certain risk indicators trigger escalation to the CCO or senior compliance: PEP involvement, EDD flags, accounts exceeding high-net-worth thresholds, adverse media screening results, or complex multi-layered entity structures. Escalated reviews have a 3-business-day target and require documented senior management approval.

Expected outcomes: The tiered model distributes 150 monthly complex accounts across four specialized queues instead of one general queue. Queue A handles approximately 55 accounts (40 revocable trusts + 15 simple LLCs) with 1-day turnaround. Queue B handles approximately 40 accounts with 2-day turnaround. Queue C handles 25 estate accounts with 2-day turnaround. Queue D handles approximately 15 accounts with 2-day turnaround. Approximately 15 accounts (10%) escalate to Tier 3 with 3-day turnaround. The weighted average approval time drops from 7 business days to approximately 1.8 business days. The automated pre-screening in Tier 1 prevents incomplete applications from entering review queues, further improving reviewer productivity.


---

## SKILL: account-reconciliation-standard

- Fuente: `SYasJ/claude-business-skills` → `plugins/accounting/skills/account-reconciliation-standard` (MIT)
- Cuándo usarla: Set a standard for balance-sheet reconciliations: purpose, frequency, evidence, and aging of open items. Use when the user mentions reconciliation standard, balance sheet reconciliations, rec policy, account ownership, or asks for a reconciliation standard. Accounting skill by Yasir Jilani.

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'account-reconciliation-standard' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Account Reconciliation Standard

Set a standard for balance-sheet reconciliations: purpose, frequency, evidence, and aging of open items.

## When to use this skill

Use this skill when the user:

- reconciliation standard
- balance sheet reconciliations
- rec policy
- account ownership

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

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

- Material balance-sheet accounts
- Current reconcilers
- How old open items get
- Reviewer

## Workflow


### 1. Assign every material account

An account without an owner is unreconciled even if the balance looks quiet.
### 2. Define a proper recon

Source, book balance, itemized difference, and age of each open item.
### 3. Frequency

Cash monthly at minimum, other accounts on a risk basis they agree. Do not demand a daily recon of every accrual without a reason.
### 4. Aging policy

Open items older than their threshold need a disposition plan, not a permanent home.
### 5. Review

Preparer and reviewer are different people for material accounts.
### 6. Storage

Where the evidence lives. Not in a personal inbox only, and not behind a shared password.

## Output

Deliver a **reconciliation standard**.

- Purpose of this reconciliation standard, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a reconciliation standard by 30 September 2026. Several balance-sheet accounts have no named preparer, and cash recs live in one person's inbox.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Several balance-sheet accounts have no named preparer, and cash recs live in one person's inbox.

Material balance-sheet accounts: one file, dated 14 September 2026. No earlier version attached for comparison
Current reconcilers: Undeposited funds and one other, both unconfirmed as of 14 September 2026
How old open items get: Undeposited funds, last reviewed 14 September 2026. No owner named since
Reviewer: Priya Shah. No second reviewer named
```

### Example outcome

**Reconciliation standard**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Assigns owners, defines a proper recon, and moves evidence to a shared location without shared passwords.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Material balance-sheet accounts | one file, dated 14 September 2026. No earlier version attached for comparison | Needs confirmation |
| Current reconcilers | Undeposited funds and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| How old open items get | Undeposited funds, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Reviewer | Priya Shah. No second reviewer named | Needs confirmation |

**How this draft was built**

**1. Assign every material account**  
An account without an owner is unreconciled even if the balance looks quiet.

**2. Define a proper recon**  
Source, book balance, itemized difference, and age of each open item.

**3. Frequency**  
Cash monthly at minimum, other accounts on a risk basis they agree. Do not demand a daily recon of every accrual without a reason.

**4. Aging policy**  
Open items older than their threshold need a disposition plan, not a permanent home.

**5. Review**  
Preparer and reviewer are different people for material accounts.

**Deliberately not done**
- A policy that says 'reconcile everything daily'.
- Open items older than a year with no comment.
- Shared logins to the evidence folder.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A policy that says 'reconcile everything daily'.
- Open items older than a year with no comment.
- Shared logins to the evidence folder.

## Related skills

- `bank-reconciliation`
- `month-end-close`
- `internal-controls-walkthrough`


---

## SKILL: account-transfers

- Fuente: `JoelLewis/finance_skills` → `plugins/client-operations/skills/account-transfers` (MIT)
- Cuándo usarla: Process and manage account transfers between and within financial institutions. Use when handling full or partial ACAT transfers between broker-dealers, troubleshooting ACAT rejection codes or FINRA Rule 11870 timelines, setting up non-ACAT transfers (Fund/SERV, DTC free delivery, physical certificates), processing internal journal entries, handling retirement rollovers or Roth conversions with proper tax reporting, transferring cost basis under IRC Section 6045A, moving decedent assets to beneficiaries with date-of-death step-up, or reconciling residual credits and fractional shares after transfer completion.

# Account Transfers

## Core Concepts

### ACAT Transfer System
The Automated Customer Account Transfer Service (ACATS) is operated by DTCC's National Securities Clearing Corporation (NSCC) and provides a standardized, automated mechanism for transferring customer accounts between broker-dealers and banks. ACATS is the primary system for transferring brokerage accounts in the United States and is governed by FINRA Rule 11870 (Customer Account Transfer Contracts).

**How ACATS works — the transfer lifecycle:**

1. **Transfer Initiation (Day 0)** — The customer signs a Transfer Initiation Form (TIF) authorizing the transfer. The receiving firm submits the transfer request through ACATS, specifying whether the transfer is full or partial and listing the assets to be transferred.
2. **Validation (Days 1-3)** — The delivering firm receives the transfer request and has 3 business days to validate the account information and asset positions. The delivering firm must verify the customer's identity, account number, SSN/TIN, and the assets listed in the request. If the information matches, the delivering firm validates the request. If there are discrepancies, the delivering firm may reject the request with a specific reject code.
3. **Asset Transfer (Days 4-6)** — Once validated, the delivering firm must transfer the account assets within 3 business days (6 business days total from initiation). ACATS coordinates the settlement of securities between the firms through NSCC. Cash balances are transferred via the Federal Reserve wire system or NSCC settlement.
4. **Residual Processing (Days 7+)** — After the primary transfer completes, the delivering firm processes residual items: dividends or interest that were accrued but not yet paid, fractional shares (typically liquidated and sent as a residual credit), reorganization proceeds, and any other items that could not be transferred on the primary settlement date.

**Full ACAT vs partial ACAT:**
- A **full ACAT** transfers the entire account — all positions, cash, and account features. The delivering firm closes the account after transfer completion. Full ACATs are the most common transfer type and benefit from the highest degree of automation.
- A **partial ACAT** transfers only specified positions and/or cash amounts. The account remains open at the delivering firm with the remaining positions. Partial ACATs require the receiving firm to specify exactly which positions and quantities to transfer. Partial ACATs are used when a client wants to consolidate specific holdings, when certain assets are ineligible for ACAT transfer, or when the client is maintaining accounts at both firms.

**ACAT-eligible vs ineligible assets:**
- **Eligible:** Equities (common stock, preferred stock, ADRs), fixed income (corporate bonds, municipal bonds, treasury securities), options (listed options — transferred with assignment of the Options Clearing Corporation position), mutual funds (if the fund is available on the receiving firm's platform), ETFs, unit investment trusts, and cash balances.
- **Ineligible or restricted:** Proprietary products of the delivering firm (proprietary mutual funds, structured notes), limited partnerships and direct participation programs (often require manual transfer), annuities (transferred directly between insurance carriers, not through ACATS), physical certificates held outside DTC, bank deposits (CDs, money market deposit accounts at the bank level), alternative investments (hedge funds, private equity — transferred via assignment or redemption/re-subscription), 529 plan accounts, and certain foreign securities not held at DTC.

When a full ACAT encounters ineligible assets, those assets remain at the delivering firm in a residual account while all eligible assets transfer. The receiving firm and client must then coordinate the manual transfer of ineligible assets or the client must decide whether to liquidate them.

**Transfer Initiation Form (TIF):**
The TIF is the customer's written authorization for the transfer. It must include: customer name, SSN/TIN, delivering firm account number, receiving firm account number, transfer type (full or partial), and for partial transfers, the specific assets and quantities to be transferred. The customer's signature on the TIF is required. Many firms now accept electronic signatures on TIFs. The receiving firm retains the TIF as part of its account records and must produce it upon regulatory request.

**Receiving firm responsibilities:**
- Obtain the signed TIF from the customer
- Submit the ACATS transfer request within one business day of receiving the completed TIF
- Ensure the account is open and properly registered at the receiving firm before submitting the transfer request
- Monitor the transfer status and communicate progress to the customer
- Reconcile received assets against the expected transfer and investigate discrepancies
- Process residual credits as they arrive from the delivering firm

**Delivering firm responsibilities (FINRA Rule 11870):**
- Validate or reject the transfer request within 3 business days — the delivering firm cannot unreasonably delay or refuse a valid transfer request
- Complete the transfer of assets within 3 business days after validation (6 business days total)
- Process and forward residual items (dividends, interest, fractional share proceeds) promptly after the transfer
- Provide cost basis information for transferred securities as required by IRS regulations
- Not charge unreasonable fees for account transfers (FINRA prohibits fees designed to discourage transfers)

### Non-ACAT Transfers
Not all asset movements between firms use the ACATS system. Non-ACAT transfers are used for assets ineligible for ACATS, transfers between non-ACATS-participating institutions, and situations where alternative transfer mechanisms are more appropriate.

**Mutual fund direct transfers (NSCC Fund/SERV):**
Mutual fund shares can be transferred between firms through NSCC's Fund/SERV system without going through ACATS. This is commonly used when the receiving firm has a direct relationship with the fund company. Fund/SERV transfers typically settle in 1-3 business days and preserve the original purchase date, cost basis, and share lot information. The receiving firm submits a transfer request through Fund/SERV, and the fund company re-registers the shares in the receiving firm's name.

**DTC free delivery:**
A DTC free delivery (also called a free receipt/free delivery or DTC transfer) moves securities between DTC participant accounts without a corresponding cash payment. This is used for in-kind transfers where no sale is involved, such as gifting securities, moving positions between related accounts at different firms, or charitable donations of appreciated stock. The delivering firm initiates the delivery through DTC's Deposit/Withdrawal at Custodian (DWAC) system, and the receiving firm must confirm receipt. DTC deliveries typically settle same-day or next-day.

**Physical certificate transfers:**
When securities are held in physical certificate form (increasingly rare but still encountered), the transfer process requires: the certificate to be submitted to the transfer agent with a stock power (signed assignment form) and a medallion signature guarantee. The transfer agent re-registers the shares in the new owner's name and issues a new certificate or deposits the shares into DTC in book-entry form. Medallion Signature Guarantee programs (STAMP, SEMP, MSP) provide the guarantee, and only eligible financial institutions (banks, broker-dealers, credit unions) can provide them. Physical transfers can take 2-4 weeks.

**Alternative investment transfers:**
- **Limited partnerships:** Transferred by assignment — the general partner must approve the transfer. The receiving firm must verify it can hold the partnership interest on its books (many firms restrict which alternative investments they will custody). Transfer may take 4-8 weeks due to GP approval requirements.
- **Hedge funds:** Typically cannot be transferred in-kind. The investor redeems from the fund (subject to redemption terms, lock-up periods, and gate provisions) and re-subscribes at the new firm. Alternatively, some prime brokers can transfer hedge fund positions between accounts.
- **Private placements:** Transferred by assignment or novation, requiring issuer consent. Transfer documentation includes assignment agreements and updated subscription documents.

**International transfers:**
Cross-border transfers involve additional complexity: SWIFT messaging for international wire transfers, correspondent banking relationships, foreign exchange conversion, regulatory considerations (OFAC screening, tax treaty withholding), and potentially different settlement conventions. International security transfers may use Euroclear or Clearstream for European securities, or bilateral arrangements between custodians for other markets.

**Wire transfers for cash:**
Cash-only transfers between firms are typically executed via Fedwire (domestic) or SWIFT (international). Wire transfers settle same-day for domestic transfers initiated before the cutoff time. The receiving firm must verify the wire instructions and authenticate the source. For large wire transfers, firms typically require verbal confirmation and callback verification.

### Partial Transfers
Partial transfers require additional planning because the client is selectively moving specific positions while leaving others in place. This creates considerations around tax lots, cost basis, margin impact, and documentation.

**Selecting specific positions:**
The receiving firm must specify each position to be transferred, including CUSIP, quantity, and for fixed income, par value. The client and advisor should review the full account holdings to determine which positions to transfer and which to leave behind. Common reasons for partial transfers: consolidating duplicate positions held at multiple firms, moving specific asset classes to a specialist manager, transferring appreciated positions for tax-loss harvesting at the new firm, and retaining positions that are ineligible for transfer.

**Tax lot selection implications:**
When transferring a partial position (some but not all shares of a security), the delivering firm must determine which tax lots to transfer. If the account uses specific identification as its tax lot method, the client should specify which lots to move. If the account uses FIFO, the earliest-acquired lots transfer first. The choice of which lots transfer can significantly impact the client's tax situation — transferring high-cost-basis lots leaves the low-basis lots behind (and vice versa). The advisor should evaluate the tax implications before selecting positions for partial transfer.

**Cost basis transfer requirements:**
Under IRS regulations (IRC Section 6045A), the delivering firm must provide cost basis information for transferred securities to the receiving firm. For covered securities (generally acquired after 2011 for equities, 2012 for mutual funds, 2014 for fixed income), the delivering firm must electronically transfer the cost basis to the receiving firm within 15 days of the transfer settlement. The receiving firm must maintain the original cost basis, acquisition date, and holding period for each lot. For uncovered securities (acquired before the applicable dates), cost basis transfer is optional but recommended. Clients should verify cost basis accuracy after the transfer completes, as discrepancies are common and can result in incorrect tax reporting.

**Partial transfer impact on margin accounts:**
Transferring assets out of a margin account reduces the account's equity and may trigger a margin call at the delivering firm. Before initiating a partial transfer from a margin account, the advisor should: calculate the post-transfer equity and margin requirements, ensure the remaining positions maintain sufficient margin collateral, consider whether to pay down the margin debit before or during the transfer, and communicate with the client about the potential margin call. If the transfer would create a margin deficiency, the delivering firm may reject the transfer or require the client to deposit additional funds.

**In-kind vs liquidate-and-transfer:**
- **In-kind transfer** moves the securities as-is, preserving the cost basis and avoiding a taxable event. This is preferred for long-term holdings with significant unrealized gains.
- **Liquidate-and-transfer** involves selling the positions at the delivering firm and transferring the cash proceeds. This creates a taxable event but may be preferable when: the securities are not available on the receiving firm's platform, the client wants to restructure the portfolio anyway, or the positions are small and not worth the complexity of in-kind transfer.

### Internal Journal Entries
Journal entries move assets between accounts within the same firm. Because the assets do not leave the firm, journal entries do not use ACATS and are processed internally through the firm's account management system. Journals are one of the most common operational transactions at brokerage firms.

**Journal types:**
- **Free journal (non-valued):** Moves securities or cash between accounts without a corresponding payment. Used for gifts, estate distributions, trust funding, and household rebalancing. A free journal of securities between accounts with different registrations (e.g., individual to trust) may have tax implications and should be documented accordingly.
- **Valued journal:** Moves securities between accounts with a corresponding cash payment. Used for internal buy/sell transactions between accounts, typically at market value. Valued journals are less common and require additional documentation to ensure fair pricing.

**Common journal scenarios:**
- **Household rebalancing:** Moving securities between family member accounts to optimize asset allocation across the household. For example, concentrating tax-exempt bonds in a taxable account and growth equities in an IRA. Note: journals between accounts with different beneficial owners (e.g., spouse A to spouse B) may constitute gifts for tax purposes.
- **Trust funding:** Transferring assets from an individual account to a trust account. This is a common event when a client establishes a trust and needs to re-title assets. The journal documents the transfer for trust accounting purposes.
- **Gift transfers:** Journaling securities from a donor's account to a recipient's account. The donor's cost basis carries over to the recipient (carryover basis for gifts), and the annual gift tax exclusion applies. The firm should document the fair market value at the date of the gift for tax reporting.
- **Account consolidation:** Merging multiple accounts belonging to the same client into a single account. The firm journals all positions and cash from the closing accounts to the surviving account.
- **Entity restructuring:** Moving assets when a client changes the account registration (e.g., individual to LLC, general partnership to limited partnership).

**Journal approval workflows:**
Most firms require supervisory approval for journal entries, especially when:
- The journal is between accounts with different registrations or beneficial owners
- The journal amount exceeds a specified threshold
- The journal involves retirement accounts (to ensure compliance with distribution and contribution rules)
- The journal is initiated by someone other than the account holder

The approval workflow typically includes: request initiation by the advisor or operations, documentation of the reason for the journal, supervisory review and approval, execution of the journal, and confirmation sent to both account holders.

**Tax implications of journals between different registrations:**
- Individual to revocable trust (same SSN): generally not a taxable event because the grantor and the trust are the same tax entity
- Individual to irrevocable trust: may be a taxable gift; gift tax return (Form 709) may be required; cost basis carries over for gifts below fair market value
- Individual to spouse (community property state): generally not taxable as a transfer between spouses
- Individual to spouse (separate property state): may be a gift; however, interspousal transfers during marriage are generally tax-free under IRC Section 1041
- Any account to an estate account: only occurs upon death; triggers cost basis step-up (or step-down) to fair market value at date of death
- Retirement account to non-retirement account: this is a distribution, not a journal; it triggers taxable income and potentially early withdrawal penalties

### Retirement Account Rollovers
Retirement account rollovers move funds between qualified retirement plans and IRAs. Rollovers are subject to specific IRS rules that differ based on the type of rollover, the source and destination accounts, and the method of transfer. Errors in rollover processing can result in unintended tax consequences, penalties, and plan disqualification.

**Direct rollover (trustee-to-trustee):**
In a direct rollover, the distributing plan or IRA transfers the funds directly to the receiving IRA or plan. The funds are never in the client's possession. Direct rollovers are the preferred method because: there is no mandatory 20% federal tax withholding (which applies to indirect rollovers from employer plans), there is no 60-day deadline to complete the rollover, and the transaction is reported as a non-taxable rollover on Form 1099-R (distribution code G for direct rollovers to eligible retirement plans, or code H for direct rollovers to Roth IRAs). The receiving firm initiates the direct rollover by submitting a rollover request to the distributing institution, accompanied by the client's signed rollover authorization.

**Indirect rollover (60-day rule):**
In an indirect rollover, the distributing plan or IRA pays the funds to the client, who then has 60 calendar days to deposit the funds into an eligible receiving plan or IRA. If the client fails to complete the rollover within 60 days, the distribution is taxable and may be subject to a 10% early withdrawal penalty if the client is under age 59 1/2. For distributions from employer plans, the plan must withhold 20% for federal taxes — meaning the client receives only 80% of the distribution and must contribute the full amount (including the 20% withheld) to the receiving IRA to avoid tax on the shortfall. The IRS may grant a waiver of the 60-day requirement for hardship, error, or circumstances beyond the client's control (Revenue Procedure 2020-46 provides a self-certification procedure).

**Employer plan to IRA rollovers:**
- **401(k), 403(b), 457(b) to Traditional IRA:** Pre-tax contributions and earnings roll over tax-free. After-tax contributions (non-Roth) can be rolled to a Traditional IRA or separated — the after-tax basis rolls to a Roth IRA and the earnings roll to a Traditional IRA (a split rollover under Notice 2014-54).
- **401(k) Roth to Roth IRA:** Designated Roth contributions and earnings from an employer plan can be directly rolled to a Roth IRA. The 5-year holding period for qualified distributions restarts at the Roth IRA.
- **Required documentation:** Distribution request form from the employer plan, rollover election form, receiving firm's IRA application (if a new IRA is being established), and a letter of acceptance from the receiving custodian.

**IRA-to-IRA rollovers (one-per-year rule):**
The IRS imposes a one-per-year rule on indirect (60-day) IRA-to-IRA rollovers: a taxpayer may make only one indirect rollover from an IRA to another IRA (or the same IRA) in any 12-month period. This rule applies in aggregate across all of the taxpayer's IRAs (Traditional, Roth, SEP, SIMPLE). Violating the one-per-year rule results in the second rollover being treated as a taxable distribution plus a 6% excess contribution penalty if deposited into the receiving IRA. Direct (trustee-to-trustee) transfers are not subject to the one-per-year rule, which is why direct transfers are strongly preferred for IRA-to-IRA movements.

**Roth conversions:**
A Roth conversion moves funds from a Traditional IRA (or employer plan) to a Roth IRA. The converted amount is included in the client's taxable income for the year of conversion (except for amounts attributable to non-deductible contributions, which have already been taxed). There is no income limit for Roth conversions. The converted amount is not subject to the 10% early withdrawal penalty. Roth conversions are reported on Form 1099-R (distribution) and Form 5498 (contribution to the Roth IRA). Conversion strategies include: converting in low-income years to minimize the tax impact, partial conversions spread over multiple years to manage bracket creep, and converting before RMDs begin — age 73 (SECURE 2.0; rises to 75 in 2033) — to reduce future RMD obligations.

**Tax reporting:**
- **Form 1099-R:** Issued by the distributing institution for the calendar year of distribution. Reports the gross distribution, taxable amount, federal and state withholding, and distribution code. Key distribution codes: 1 (early distribution), 2 (early distribution — exception applies), 7 (normal distribution), G (direct rollover to qualified plan), H (direct rollover to Roth IRA).
- **Form 5498:** Issued by the receiving institution for the calendar year of the contribution/rollover. Reports rollover contributions, regular contributions, fair market value of the account, and RMD amounts. Form 5498 is due to the IRS by May 31 of the year following the contribution.

### Estate Transfers
Estate transfers move assets from a decedent's account to beneficiaries, estate accounts, or trust accounts established under the decedent's will. Estate transfers are among the most complex operational transactions due to the legal documentation required, tax basis adjustments, and the emotional sensitivity of working with bereaved families.

**Death notification, account freeze, and estate documentation:**
The death notification workflow — immediate account restriction, death certificate verification, letters testamentary or administration, small estate affidavits, and JTWROS survivor handling — is covered in account-maintenance. This skill picks up once documentation is in hand and assets must move: basis step-up, inherited IRA establishment, and beneficiary distributions.

**Cost basis step-up processing:**
Upon death, the cost basis of the decedent's assets is generally stepped up (or stepped down) to the fair market value as of the date of death (IRC Section 1014). The alternate valuation date (6 months after death) may be elected by the estate executor on the federal estate tax return (Form 706), but only if it reduces the gross estate value. The firm must: determine the fair market value of each position as of the date of death, update the cost basis records to reflect the stepped-up basis, and transfer the stepped-up basis to the receiving account (beneficiary, estate, or trust). For community property states, the surviving spouse's half of community property also receives a step-up in basis (full step-up for both halves), which is a significant tax benefit.

**Inherited IRA setup:**
When the decedent held an IRA, the beneficiary designation on file determines the distribution of the IRA assets — the will does not override the IRA beneficiary designation. Processing depends on the beneficiary type:
- **Spouse beneficiary:** May roll the inherited IRA into their own IRA (treating it as their own), transfer to an inherited IRA in their name, or take a lump-sum distribution. Rolling to their own IRA allows continued tax-deferred growth and delays RMDs until the spouse's own required beginning date.
- **Non-spouse individual beneficiary (SECURE Act):** Under the SECURE Act of 2019, most non-spouse beneficiaries must distribute the entire IRA within 10 years of the account owner's death (the 10-year rule). Exceptions (eligible designated beneficiaries): minor children of the account owner (until age of majority), disabled individuals, chronically ill individuals, and individuals not more than 10 years younger than the decedent. The inherited IRA must be titled in the decedent's name for the benefit of the beneficiary (e.g., "John Smith, Deceased, FBO Jane Smith, Beneficiary").
- **Entity or estate beneficiary:** Subject to the 5-year rule (all assets must be distributed within 5 years of death) if the account owner died before the required beginning date, or the remaining life expectancy method if death occurred on or after the required beginning date.

**Multi-beneficiary allocation:**
When an IRA or investment account names multiple beneficiaries, the firm must allocate assets proportionally based on the beneficiary designation percentages. Each beneficiary receives their share in a separately established account. For inherited IRAs, establishing separate inherited IRA accounts for each beneficiary by December 31 of the year following the year of death allows each beneficiary to use their own life expectancy for RMD calculations (if applicable). Failure to separate the accounts by this deadline requires all beneficiaries to use the oldest beneficiary's life expectancy.

**Estate distribution scheduling:**
The executor or administrator determines when and how to distribute estate assets. The firm processes distributions based on the executor's instructions, which may include: in-kind distribution of securities to beneficiaries (preserving the stepped-up basis), liquidation and cash distribution, partial distributions over time (common when estate settlement takes months or years), and specific bequests of particular securities to named beneficiaries. Each distribution must be documented and reconciled against the total estate.

### Transfer Tracking and Reconciliation
Transfer tracking is critical for operational efficiency and client satisfaction. Transfers involve multiple systems, firms, and settlement cycles, creating opportunities for errors, delays, and miscommunication.

**Transfer status monitoring:**
Firms should maintain a centralized transfer tracking system that captures: transfer request date, transfer type (ACAT, non-ACAT, journal, rollover), current status (submitted, validated, in progress, completed, rejected), expected completion date, actual completion date, and any exceptions or holds. ACATS provides real-time status updates through NSCC, which the firm's back office system should capture and display. Operations teams should review outstanding transfers daily and escalate transfers that exceed expected timelines.

**Common ACAT rejection codes and remediation:**
- **Code 01 — Account number not on file:** The account number provided does not match the delivering firm's records. Remediation: verify the account number with the client and resubmit.
- **Code 02 — SSN/TIN mismatch:** The SSN or TIN on the transfer request does not match the delivering firm's records. Remediation: confirm the correct SSN/TIN with the client; may require the client to update records at the delivering firm before resubmission.
- **Code 03 — Account title mismatch:** The account registration on the transfer request does not match the delivering firm's records (e.g., "John A. Smith" vs "John Smith"). Remediation: match the exact registration at the delivering firm or have the client update their registration.
- **Code 04 — Invalid transfer type for this account:** The transfer type requested (full or partial) is not valid for the account. Remediation: verify the account type and correct the transfer request.
- **Code 05 — Duplicate request:** A transfer request for this account is already in progress. Remediation: check for an existing pending transfer and cancel the duplicate.
- **Code 07 — Account in transfer:** The account is already in the process of being transferred. Remediation: wait for the existing transfer to complete before initiating a new request.
- **Code 08 — Account restricted:** The account has a legal restriction (lien, court order, margin liquidation) preventing transfer. Remediation: work with the client and delivering firm to resolve the restriction.

**Escalation procedures:**
When a transfer is delayed beyond expected timelines or encounters repeated rejections, escalation steps include: contacting the delivering firm's transfer department directly, filing a FINRA complaint if the delivering firm is unreasonably delaying (FINRA Rule 11870 prohibits unreasonable delays), involving the client in communicating with the delivering firm, and escalating within the receiving firm's operations management chain. FINRA requires delivering firms to complete validated transfers within 3 business days, and patterns of delay may result in regulatory action.

**Client communication during transfers:**
Proactive client communication reduces anxiety and support inquiries during the transfer process. Best practices include: setting expectations at transfer initiation (explain the timeline, potential for delays, and what to expect), providing status updates at key milestones (validation, asset movement, completion), promptly notifying the client of any rejections or issues requiring their action, confirming completion and providing a summary of transferred assets, and following up after completion to address any discrepancies (missing positions, incorrect cost basis).

**Asset reconciliation post-transfer:**
After a transfer completes, the receiving firm must reconcile the received assets against the expected transfer. Reconciliation checks include: verifying that all expected positions were received in the correct quantities, confirming cash balances match expectations, verifying cost basis information was received and is accurate, checking for positions that may have settled at the delivering firm after the transfer date (late-settling trades), and identifying any corporate action adjustments that occurred during the transfer period (stock splits, dividends, mergers).

**Clean-up processing:**
Post-transfer clean-up addresses residual items that were not part of the primary transfer:
- **Residual credits:** Small cash amounts (typically under $100) sent by the delivering firm after the primary transfer — often from final dividend payments, interest accruals, or fractional share liquidation proceeds. The receiving firm must post these credits to the client's account and notify the client.
- **Fractional shares:** ACATS cannot transfer fractional shares. The delivering firm liquidates fractional shares and sends the cash proceeds as a residual credit. The client should be informed that fractional shares will be liquidated.
- **Accrued income:** Interest or dividends that accrued before the transfer but are paid after the transfer date. The delivering firm is responsible for forwarding these to the receiving firm or directly to the client.
- **Pending transactions:** Trades that were executed before the transfer but settle after the transfer date must be accounted for at the appropriate firm based on trade date vs settlement date conventions.

### Regulatory Requirements
Account transfers are governed by specific FINRA rules, ACATS operating procedures, and IRS regulations for retirement accounts.

**FINRA Rule 11870 — Customer Account Transfer Contracts:**
Rule 11870 establishes the requirements for customer account transfers between FINRA member firms. Key provisions: the receiving firm must submit the transfer request within one business day of receiving the customer's signed TIF; the delivering firm must validate or take exception to the transfer within 3 business days; validated transfers must be completed within 3 business days after validation (6 business days total); the delivering firm must promptly resolve any exceptions and may not unreasonably delay or refuse a valid transfer; and residual credit balances must be forwarded to the receiving firm within 5 business days of the delivering firm's next credit cycle.

**ACATS operating rules:**
ACATS operates under the NSCC Rules and Procedures, which supplement FINRA Rule 11870. ACATS rules define: the electronic format for transfer requests and responses, valid rejection codes and their appropriate use, settlement procedures for transferred assets, timeframes for each stage of the transfer process, and reporting requirements for transfer activity.

**Delivering firm obligations:**
The delivering firm has a regulatory obligation not to impede valid transfer requests. Prohibited practices include: rejecting transfers for pretextual reasons, delaying validation to retain assets, imposing unreasonable transfer fees designed to discourage transfers, and failing to process residual items promptly. FINRA examinations specifically review delivering firm transfer practices, and patterns of delay or obstruction can result in enforcement actions and fines.

**Cost basis reporting requirements:**
Under IRC Section 6045A and associated Treasury Regulations, the delivering firm must transfer cost basis information for covered securities to the receiving firm. The transfer must be electronic (using the CBRS — Cost Basis Reporting System) and must occur within 15 days of the transfer settlement date. The receiving firm must maintain the transferred basis and use it for subsequent tax reporting on Form 1099-B. Failure to transfer cost basis accurately can result in incorrect tax reporting, IRS penalties, and customer complaints.

**ERISA considerations for retirement transfers:**
Transfers involving ERISA-governed retirement plans (401(k), 403(b), pension plans) require compliance with ERISA's fiduciary rules. The plan fiduciary must approve rollover distributions, confirm the receiving institution is an eligible retirement plan, and ensure the participant receives required disclosures (including a Special Tax Notice under IRC Section 402(f)). Plan-to-IRA rollovers must be processed as either direct rollovers or eligible rollover distributions with mandatory 20% withholding.

**Asset validation and due diligence:**
Both the receiving and delivering firms must validate the assets being transferred. The receiving firm must confirm it can hold and service each asset type (some firms restrict certain alternative investments, foreign securities, or thinly traded positions). The delivering firm must verify that the positions are free of liens, pledges, or legal holds before releasing them. For margin accounts, the delivering firm must confirm the transfer will not create an unsecured debit balance. Both firms must maintain an audit trail of the transfer validation process for regulatory examination purposes.

## Worked Examples

Three worked examples — a five-account household ACAT migration (LP interests, proprietary funds, UTMA authorization), a 401(k)-to-IRA split rollover with Roth conversion bracket analysis (Notice 2014-54), and a multi-beneficiary estate transfer (JTWROS, probate, inherited IRAs under the SECURE Act) — are in [references/examples.md](references/examples.md); load it when working through a concrete transfer, rollover, or estate distribution.

## Common Pitfalls
- Submitting ACAT transfer requests with account title mismatches — even minor discrepancies (middle initial, suffix, trust name variation) cause rejections that delay the transfer by days
- Failing to identify ACAT-ineligible assets before initiating a full ACAT, leading to unexpected residual positions at the delivering firm and confused clients
- Not verifying mutual fund availability on the receiving firm's platform before transfer — proprietary funds of the delivering firm cannot be held in-kind and must be liquidated
- Processing an indirect rollover when a direct rollover was intended, triggering mandatory 20% withholding and creating a 60-day compliance deadline
- Violating the one-per-year IRA-to-IRA indirect rollover rule by processing a second indirect rollover within 12 months — this creates a taxable distribution and excess contribution penalty
- Failing to separate inherited IRA accounts for multiple beneficiaries by the December 31 deadline of the year following the year of death, forcing all beneficiaries to use the oldest beneficiary's life expectancy
- Initiating a partial transfer from a margin account without calculating the post-transfer margin impact, resulting in a margin call at the delivering firm
- Not following up on residual credits from the delivering firm — small amounts of dividends, fractional share proceeds, and interest can remain undelivered for months if not tracked
- Accepting a death certificate photocopy rather than a certified copy, causing processing delays when the operations team rejects the documentation
- Confusing a Roth conversion (taxable event) with a Roth contribution (subject to income and contribution limits) — these are different transactions with different rules and reporting
- Failing to transfer cost basis for covered securities within the required 15-day window, resulting in regulatory issues and incorrect tax reporting at the receiving firm
- Processing estate distributions without proper letters testamentary or letters of administration, exposing the firm to liability if the distributions are later challenged

## Cross-References
- **account-opening-workflow** (client-operations plugin): New accounts must be established at the receiving firm before transfers can be initiated; transfer processing depends on proper account setup and registration matching
- **account-maintenance** (client-operations plugin): Account re-registration (name changes, trust re-titling) and beneficiary updates are often prerequisites for successful transfers; maintenance workflows handle post-transfer clean-up tasks
- **settlement-clearing** (trading-operations plugin): ACAT transfers settle through NSCC/DTCC infrastructure; understanding settlement cycles and DTC delivery mechanisms is essential for transfer processing and reconciliation
- **tax-efficiency** (wealth-management plugin): Transfer decisions (in-kind vs liquidate, tax lot selection, Roth conversion timing) have significant tax implications; the tax-efficiency skill informs optimal transfer strategies for taxable accounts
- **books-and-records** (compliance plugin): Transfer documentation (TIFs, rollover forms, death certificates, letters testamentary) must be retained per SEC and FINRA recordkeeping rules; transfer records are commonly requested during regulatory examinations
- **client-onboarding** (advisory-practice plugin): Transfers are a primary funding mechanism during client onboarding; the onboarding workflow initiates and tracks ACAT transfers as part of the new client setup process
- **corporate-actions** (client-operations plugin): Pending corporate actions (dividends, mergers, splits) during the transfer period require coordination between delivering and receiving firms to ensure proper processing and allocation
- **reconciliation** (client-operations plugin): Post-transfer asset reconciliation verifies that all positions, cash balances, and cost basis were transferred accurately; reconciliation processes detect and resolve transfer discrepancies

### Referencia: references/examples.md

# Account Transfers — Worked Examples

## Example 1: Managing a full ACAT transfer for a high-net-worth household moving from a competitor
**Scenario:** A high-net-worth household with $8M across five accounts is moving from a competitor firm to your firm. The accounts are: (1) a joint taxable account with $3M in individual equities and ETFs, (2) the husband's Traditional IRA with $1.5M in mutual funds and bonds, (3) the wife's Roth IRA with $800K in equities and ETFs, (4) a revocable family trust with $2.2M in a diversified portfolio including equities, fixed income, and a limited partnership interest valued at $200K, and (5) a custodial UTMA account for their minor child with $500K in mutual funds. The advisor wants to complete the transfer as efficiently as possible and invest the assets into the firm's model portfolios.

**Design Considerations:**
- Five separate ACAT transfers must be initiated — each account is a distinct ACATS transfer request
- The limited partnership in the trust account is likely ACAT-ineligible and will require separate handling
- The mutual funds in the IRA and UTMA accounts must be verified for availability on the receiving firm's platform — proprietary funds of the competitor may not be transferable in-kind
- The joint taxable account and trust account may have significant unrealized gains, making in-kind transfer critical to avoid unnecessary taxable events
- Cost basis must transfer accurately for all taxable accounts (joint, trust, UTMA); retirement accounts (IRA, Roth IRA) do not have cost basis reporting requirements during the transfer but should be tracked internally
- The UTMA account requires that the custodian (parent) authorize the transfer

**Analysis:** Begin by opening all five accounts at the receiving firm with proper registrations matching the delivering firm exactly (account title mismatches are the most common cause of ACAT rejections). Obtain signed TIFs for all five accounts. For the trust account, ensure the trust certification and EIN documentation are on file. For the UTMA, verify the custodian designation matches.

Submit all five ACAT requests simultaneously. For the trust account, submit a partial ACAT excluding the limited partnership position. Contact the limited partnership's general partner to initiate a separate assignment/transfer process for the LP interest — this will require: a transfer of ownership form from the GP, the receiving firm's confirmation that it can hold the LP interest on its books, and potentially a 30-60 day processing period for GP approval.

For the mutual funds, pre-verify each fund's availability on the receiving firm's platform. If any funds are proprietary to the delivering firm, discuss with the client: (a) liquidate at the delivering firm before the ACAT (taxable event in the IRA/UTMA is not a concern since these are tax-advantaged accounts, but taxable for the joint/trust accounts), or (b) transfer via ACAT and the positions will arrive as "ineligible" and need to be liquidated at the receiving firm, or (c) leave the proprietary fund positions behind and transfer only eligible assets.

Monitor all five transfers daily through ACATS status updates. The expected timeline is: validation within 3 business days, asset delivery within 6 business days total. After the primary transfer settles, reconcile all positions against the delivering firm's final statement. Verify cost basis information was received for the joint, trust, and UTMA accounts. Process any residual credits (fractional shares, pending dividends) as they arrive over the following 2-4 weeks.

Once all assets are received and reconciled, assign each account to the appropriate model portfolio. For the joint and trust accounts with existing equity positions, the advisor should evaluate which positions to retain (to avoid realizing gains) and which to sell for model alignment, factoring in tax-loss harvesting opportunities. Provide the client with a transfer completion summary showing all positions received, cost basis, and any residual items pending.

## Example 2: Processing retirement account rollovers from a 401(k) to an IRA with Roth conversion
**Scenario:** A 55-year-old client has recently left her employer and has a 401(k) with $750K, consisting of $600K in pre-tax contributions and earnings and $150K in after-tax (non-Roth) contributions and earnings. The client wants to roll the funds into an IRA at your firm and convert a portion to a Roth IRA. The client's current-year taxable income is $180K (married filing jointly), placing her in the 24% federal bracket. The client wants to manage the tax impact of the Roth conversion.

**Design Considerations:**
- The 401(k) contains both pre-tax and after-tax funds, which enables a split rollover under IRS Notice 2014-54
- Under Notice 2014-54, the client can direct the pre-tax portion ($600K) to a Traditional IRA and the after-tax contributions (basis) to a Roth IRA, with the earnings on after-tax contributions going to the Traditional IRA
- The after-tax contribution basis of $150K includes both the original contributions and earnings on those contributions — the plan administrator must provide a breakdown. Assume $120K is after-tax basis and $30K is earnings on those contributions
- The $120K after-tax basis can be converted to a Roth IRA with zero tax because it has already been taxed. The $30K in earnings would be taxable if converted to Roth
- A direct rollover avoids the 20% mandatory withholding that applies to indirect rollovers from employer plans
- The client may want to convert additional pre-tax funds to Roth, but must weigh the tax cost

**Analysis:** Step 1: Open a Traditional IRA and a Roth IRA at the receiving firm. Step 2: Request a split direct rollover from the 401(k) plan administrator. The rollover instruction directs: pre-tax contributions and all earnings ($600K pre-tax + $30K earnings on after-tax = $630K) to the Traditional IRA, and after-tax contribution basis ($120K) to the Roth IRA. Under Notice 2014-54, this allocation is permitted because the after-tax basis is directed to the Roth IRA and the pre-tax/earnings portion is directed to the Traditional IRA.

Tax impact of the split rollover: the $120K direct rollover to the Roth IRA from after-tax contributions has zero tax because the basis has already been taxed. The $630K direct rollover to the Traditional IRA is not currently taxable.

Step 3: Evaluate additional Roth conversion. The client is in the 24% bracket at $180K income. The top of the 24% bracket for married filing jointly is $383,900 for the 2024 tax year (the figures used in this example — bracket thresholds are inflation-indexed annually, so verify current-year brackets before executing). The client has approximately $203K of room in the 24% bracket ($383,900 minus $180K). Converting $203K from the Traditional IRA to the Roth IRA would keep the client in the 24% bracket and cost approximately $48,720 in federal tax ($203K multiplied by 24%). Alternatively, the client could convert less to stay well within the bracket or spread conversions over multiple years.

Step 4: Process the Roth conversion. After the direct rollover to the Traditional IRA settles (allow 1-2 weeks for the 401(k) distribution and IRA deposit), initiate a Roth conversion for the agreed-upon amount. The conversion is processed as a distribution from the Traditional IRA and a contribution to the Roth IRA. The firm issues a 1099-R for the conversion in the year it occurs.

Step 5: Tax reporting. The 401(k) plan administrator issues Form 1099-R for the direct rollover distribution (code G). The receiving firm issues Form 5498 for the rollover contribution to the Traditional IRA and the Roth IRA. If a subsequent Roth conversion is done, the receiving firm issues an additional 1099-R for the conversion distribution and an additional 5498 for the Roth conversion contribution.

Step 6: Document the multi-year Roth conversion strategy. If the client plans to convert additional amounts in future years, document the plan: target conversion amount per year, bracket analysis, and the expected timeline to convert the desired total. This becomes part of the client's financial plan and should be reviewed annually as income and tax brackets change.

## Example 3: Handling estate account transfers to multiple beneficiaries with different account types
**Scenario:** A client passed away holding three accounts at your firm: (1) an individual taxable account with $2M in equities and bonds, (2) a Traditional IRA with $500K, and (3) a joint taxable account (JTWROS) with his spouse holding $1M in diversified funds. The will names the spouse as the sole beneficiary of the estate (for the individual taxable account). The IRA beneficiary designation names the spouse (60%) and the two adult children (20% each). The date of death is January 15, and the firm was notified on January 22.

**Design Considerations:**
- The joint JTWROS account passes automatically to the surviving spouse by operation of law — this is not a probate asset and does not go through the estate
- The individual taxable account is a probate asset that passes under the will to the spouse through the estate
- The IRA passes by beneficiary designation, not by will — the 60/20/20 split controls
- All assets in the individual taxable and joint accounts receive a cost basis step-up to fair market value as of the date of death (January 15)
- In a community property state, the spouse's half of the joint account also receives a step-up; in a common law state, only the decedent's half steps up, but for JTWROS the entire account passes to the surviving spouse regardless
- The spouse can roll the 60% IRA share into her own IRA; the adult children must take their shares as inherited IRAs subject to the SECURE Act 10-year rule
- The inherited IRAs must be established as separate accounts by December 31 of the year following the year of death to allow each beneficiary to use their own distribution timeline

**Analysis:**

**Joint account (JTWROS) — immediate processing:** Upon receipt of the certified death certificate, remove the decedent's name from the joint account registration. The account becomes solely the surviving spouse's individual account. No letters testamentary are needed — a death certificate is sufficient. Process the cost basis step-up for the decedent's portion of the holdings (or the full step-up if the couple was in a community property state). This can typically be completed within 1-2 weeks of receiving the death certificate.

**Individual taxable account — estate processing:** Freeze the account upon notification of death. Request the following documentation: certified death certificate, letters testamentary (the spouse must be appointed as executor by the probate court), estate EIN (obtained by the executor from the IRS via Form SS-4), and the firm's beneficiary claim form. Once letters testamentary are received, re-title the account as an estate account ("Estate of [Decedent Name], [Spouse Name], Executor"). Process the cost basis step-up to the January 15 date-of-death values for all positions. The executor may then either: (a) distribute the assets in-kind to the spouse's individual account (preserving the stepped-up basis), (b) liquidate the positions and distribute cash, or (c) maintain the estate account during the probate process and distribute upon estate settlement. Given that the spouse is the sole beneficiary, in-kind distribution to the spouse's account is typically the most tax-efficient approach, preserving the stepped-up basis.

**Traditional IRA — beneficiary distribution:** The IRA beneficiary designation controls. Three separate inherited IRA accounts must be established:

1. **Spouse's inherited IRA (60% = $300K):** The spouse has three options: (a) roll the $300K into her own existing Traditional IRA — this is the most common choice as it allows continued tax-deferred growth, new beneficiary designations, and delays RMDs until the spouse's own required beginning date; (b) transfer to an inherited IRA in the spouse's name — this preserves the ability to take distributions without early withdrawal penalty regardless of age, which is beneficial if the spouse is under 59 1/2 and needs access to funds; or (c) take a lump-sum distribution (fully taxable and rarely advisable). For a spouse who does not need immediate access and is over 59 1/2, spousal rollover is typically preferred.

2. **Child 1 inherited IRA (20% = $100K):** Establish an inherited IRA titled "Decedent Name, Deceased, FBO Child 1 Name, Beneficiary." Under the SECURE Act, Child 1 must distribute the entire inherited IRA by December 31 of the 10th year following the year of death (by December 31 of Year 11 counting from the year after death). There are no annual RMDs required during the 10-year period (assuming the decedent died before the required beginning date); however, the entire balance must be distributed by the end of the 10th year. If the decedent had already reached the required beginning date, annual RMDs are required during the 10-year period based on the beneficiary's life expectancy.

3. **Child 2 inherited IRA (20% = $100K):** Same structure and rules as Child 1.

**Timeline and coordination:** Establish the three inherited IRA accounts as quickly as documentation allows, and no later than December 31 of the year following the year of death to preserve separate account treatment. Process the IRA distributions per the beneficiary designation percentages. Provide each beneficiary with documentation of their inherited IRA, the distribution rules that apply, and the deadline for full distribution. Coordinate with the estate attorney on the probate timeline for the individual taxable account.

**Cost basis documentation:** Prepare a date-of-death valuation report for all three accounts showing: each position, the number of shares or par value, the closing price on January 15 (or the average of the high and low for that date), and the total stepped-up basis. This report becomes part of the estate records and is provided to the executor, the tax preparer, and each beneficiary for their records. The stepped-up basis applies to the individual taxable account and the joint account but does not apply to the IRA (IRA distributions are taxed as ordinary income regardless of basis step-up).


---

## SKILL: accounts-payable-control

- Fuente: `SYasJ/claude-business-skills` → `plugins/accounting/skills/accounts-payable-control` (MIT)
- Cuándo usarla: Tighten payables so the company pays the right vendor, once, with evidence. Use when the user mentions accounts payable, duplicate payment, AP control, vendor payments, or asks for a payables control review. Accounting skill by Yasir Jilani.

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'accounts-payable-control' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Accounts Payable Control

Tighten payables so the company pays the right vendor, once, with evidence.

## When to use this skill

Use this skill when the user:

- accounts payable
- duplicate payment
- AP control
- vendor payments

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

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

- How invoices arrive
- Who can add a vendor
- Approval limits
- Recent duplicate or fraud scares, if any

## Workflow


### 1. Map the path

Invoice, receipt of goods or services, approval, payment. Note where one person can do two of those steps.
### 2. Vendor master

New vendors need evidence the user already requires, plus a second look. Do not ask for or store bank passwords. Do not invent a vendor's bank details.
### 3. Three-way match where it fits

Purchase, receipt, and invoice. Where a match does not fit, say what alternative evidence they use.
### 4. Duplicate test

Same vendor, similar amount, close dates. Recommend a review list, not an automatic accusation.
### 5. Payment run

Who reviews the run before release, and how exceptions are logged.
### 6. Keep evidence

What is retained and for how long, using their retention rule if they have one. Do not invent a legal retention period.

## Output

Deliver a **payables control review**.

- Purpose of this payables control review, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a payables control review by 30 September 2026. Two similar invoices from the same supplier were paid last quarter.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Two similar invoices from the same supplier were paid last quarter.

How invoices arrive: plain, for people who already know the context. No house guide attached
Who can add a vendor: Priya Shah, controller
Approval limits: Undeposited funds. Partly documented: the what is written down, the who is not
Recent duplicate or fraud scares, if any: Sales tax payable. Partly documented: the what is written down, the who is not
```

### Example outcome

**Payables control review**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Separates vendor setup from payment release and proposes a duplicate review list without accusing the supplier.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| How invoices arrive | plain, for people who already know the context. No house guide attached | Needs confirmation |
| Who can add a vendor | Priya Shah, controller | Carried into the draft |
| Approval limits | Undeposited funds. Partly documented: the what is written down, the who is not | Carried into the draft |
| Recent duplicate or fraud scares, if any | Sales tax payable. Partly documented: the what is written down, the who is not | Needs confirmation |

**How this draft was built**

**1. Map the path**  
Invoice, receipt of goods or services, approval, payment. Note where one person can do two of those steps.

**2. Vendor master**  
New vendors need evidence the user already requires, plus a second look. Do not ask for or store bank passwords. Do not invent a vendor's bank details.

**3. Three-way match where it fits**  
Purchase, receipt, and invoice. Where a match does not fit, say what alternative evidence they use.

**4. Duplicate test**  
Same vendor, similar amount, close dates. Recommend a review list, not an automatic accusation.

**5. Payment run**  
Who reviews the run before release, and how exceptions are logged.

**Deliberately not done**
- One person adds vendors and releases payments with no second look.
- Calling every duplicate-looking item fraud.
- Requesting banking passwords.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- One person adds vendors and releases payments with no second look.
- Calling every duplicate-looking item fraud.
- Requesting banking passwords.

## Related skills

- `expense-policy`
- `internal-controls-walkthrough`
- `vendor-contract-playbook`


---

## SKILL: accounts-receivable-control

- Fuente: `SYasJ/claude-business-skills` → `plugins/accounting/skills/accounts-receivable-control` (MIT)
- Cuándo usarla: Review receivables so the aging means something and cash collection is a process, not a hope. Use when the user mentions accounts receivable, AR aging, collections control, unapplied cash, or asks for a receivables control review. Accounting skill by Yasir Jilani.

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'accounts-receivable-control' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Accounts Receivable Control

Review receivables so the aging means something and cash collection is a process, not a hope.

## When to use this skill

Use this skill when the user:

- accounts receivable
- AR aging
- collections control
- unapplied cash

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

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

- Aging by customer
- Billing terms
- Unapplied cash
- Disputes the user knows about

## Workflow


### 1. Tie the aging to the ledger

If the aging and the GL disagree, that is the first finding. Do not analyze a report that does not tie.
### 2. Split the buckets

Current, overdue, disputed, and unapplied. A disputed invoice is not a collections script.
### 3. Credit notes and cash application

Unapplied cash hides both problems and comfort. List it.
### 4. Concentration

A few customers may dominate overdue. Name them only from the user's data.
### 5. Write the action by bucket

Bill, call, resolve dispute, or reserve. Reserving is an accounting judgment for the policy owner, not a collection tactic.
### 6. Do not harass

Draft a factual collections note if asked. No threats, no shame language, no fake legal deadlines.

## Output

Deliver a **receivables control review**.

- Purpose of this receivables control review, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a receivables control review by 30 September 2026. The AR aging shows a large over-90 bucket, and cash sits unapplied in the same report.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

The AR aging shows a large over-90 bucket, and cash sits unapplied in the same report.

Aging by customer: Kite Freight
Billing terms: Operating cash and one other, both unconfirmed as of 14 September 2026
Unapplied cash: Sales tax payable, last reviewed 14 September 2026. No owner named since
Disputes the user knows about: Undeposited funds. Stated in the ask, not documented anywhere else
```

### Example outcome

**Receivables control review**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Reconciles the aging, separates disputes from overdue, and lists unapplied cash before anyone writes a chase note.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Aging by customer | Kite Freight | Needs confirmation |
| Billing terms | Operating cash and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| Unapplied cash | Sales tax payable, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Disputes the user knows about | Undeposited funds. Stated in the ask, not documented anywhere else | Needs confirmation |

**How this draft was built**

**1. Tie the aging to the ledger**  
If the aging and the GL disagree, that is the first finding. Do not analyze a report that does not tie.

**2. Split the buckets**  
Current, overdue, disputed, and unapplied. A disputed invoice is not a collections script.

**3. Credit notes and cash application**  
Unapplied cash hides both problems and comfort. List it.

**4. Concentration**  
A few customers may dominate overdue. Name them only from the user's data.

**5. Write the action by bucket**  
Bill, call, resolve dispute, or reserve. Reserving is an accounting judgment for the policy owner, not a collection tactic.

**Deliberately not done**
- An aging that does not tie to the ledger.
- Treating disputes as lazy customers.
- Threatening language in a collections note.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- An aging that does not tie to the ledger.
- Treating disputes as lazy customers.
- Threatening language in a collections note.

## Related skills

- `working-capital`
- `revenue-recognition-review`
- `bank-reconciliation`


---

## SKILL: advertising-compliance

- Fuente: `JoelLewis/finance_skills` → `plugins/compliance/skills/advertising-compliance` (MIT)
- Cuándo usarla: Ensure investment advertising and marketing materials comply with SEC Marketing Rule and FINRA Rule 2210. Use when the user asks about performance advertising, showing backtested or hypothetical returns, net vs gross performance presentation, client testimonials or endorsements in marketing, social media posts by advisers or reps, third-party ratings in pitchbooks, or advertising recordkeeping. Also trigger when users mention 'can we show this track record', 'pitchbook compliance review', 'marketing rule violations', 'cherry-picking performance periods', 'predecessor performance portability', 'extracted performance', or ask whether a website, one-pager, or presentation needs compliance approval.

# Advertising Compliance — Investment Marketing & Communications

Regulatory status current as of June 2026 — verify effective dates, dollar thresholds, and pending rulemakings against current SEC/FINRA/FinCEN sources before advising.

## Core Concepts

### SEC Marketing Rule (Rule 206(4)-1)
Effective November 4, 2022, the SEC's Marketing Rule replaced both the prior Advertising Rule (old Rule 206(4)-1) and the Cash Solicitation Rule (old Rule 206(4)-3) for investment advisers registered under the Investment Advisers Act of 1940. The rule applies to any "advertisement" — defined broadly as (1) any direct or indirect communication by an adviser that offers or promotes investment advisory services, or (2) any endorsement or testimonial for which the adviser provides compensation.

**Seven general prohibitions.** An advertisement may not:

1. **Include untrue statements of material fact or omit material facts** necessary to make the statement not misleading in light of the circumstances.
2. **Include material statements of fact that the adviser does not have a reasonable basis for believing** it can substantiate upon demand by the SEC.
3. **Include information that would reasonably be likely to cause an untrue or misleading inference** to be drawn about a material fact relating to the adviser.
4. **Discuss potential benefits without providing fair and balanced treatment of associated material risks or limitations.** A one-sided presentation of returns without discussing the corresponding risks violates this prohibition.
5. **Reference specific investment advice in a misleading manner.** This prohibition targets cherry-picking — presenting only favorable past recommendations while omitting unfavorable ones.
6. **Include or exclude performance results, or present performance time periods, in a manner that is not fair and balanced.** This encompasses selective time-period presentation, choosing only the best-performing periods and ignoring others.
7. **Be otherwise materially misleading.**

These prohibitions apply to all advertisements regardless of the audience. There is no "sophisticated investor" exception — even materials shown only to institutional investors must comply.

### Performance Advertising Under the Marketing Rule
Performance presentation is the most technically demanding area of advertising compliance. The Marketing Rule imposes specific requirements depending on the type of performance shown.

**Net performance requirement.** Whenever gross performance is presented, net performance must also be shown with at least equal prominence. Net performance must reflect the deduction of all fees and expenses that a client would pay, including advisory fees, custodial fees, and any other fees the adviser charges. Model fees are permitted only if they reflect the adviser's current fee schedule and the highest fee charged to the relevant audience.

**Time period requirements.** Performance must be shown for standardized time periods of 1-year, 5-year, and 10-year periods (or since inception if the track record is shorter than the prescribed period). These periods must end on the most recent practicable date. An adviser cannot show only a favorable 3-year period while omitting the required 1-, 5-, and 10-year figures. **Private fund carve-out:** the prescribed 1/5/10-year periods do not apply to performance of private funds (Rule 206(4)-1(d)(2) excludes private funds from the time-period requirement) — but private fund performance remains fully subject to the net performance requirement, the seven general prohibitions, and the fair-and-balanced standard.

**Hypothetical performance.** Includes backtested performance, model performance, and targeted or projected returns. The Marketing Rule permits hypothetical performance only if the adviser:

- Adopts and implements written policies and procedures reasonably designed to ensure that the hypothetical performance is relevant to the likely financial situation and investment objectives of the intended audience.
- Provides sufficient information to enable the intended audience to understand the criteria used and assumptions made in calculating the hypothetical performance.
- Provides (or, if the intended audience is an investor in a private fund, provides or offers to provide promptly) sufficient information to enable the intended audience to understand the risks and limitations of using such hypothetical performance in making investment decisions.

Hypothetical performance cannot be used in advertisements directed to a mass audience (such as a public website accessible to all visitors) unless appropriate controls are in place (e.g., requiring the viewer to enter information demonstrating that the content is relevant to their situation before accessing the hypothetical performance).

**Extracted performance.** When showing the performance of a subset of investments from a portfolio (for example, only the equity sleeve of a balanced account), the total portfolio performance must be presented alongside it. The purpose is to prevent advisers from highlighting only the best-performing segment of a portfolio in isolation.

**Related performance (predecessor performance and portability).** An adviser may present performance from a predecessor firm or from an account managed at a prior employer, but only if:

- The person or persons primarily responsible for achieving the prior performance manage accounts at the current adviser.
- The accounts managed at the prior firm are sufficiently similar to the accounts currently managed that the prior performance provides relevant information.
- All accounts managed in a substantially similar manner are included (no cherry-picking of the best-performing accounts).
- The advertisement clearly discloses that the performance was achieved at a different entity and describes any differences in personnel, investment process, or account structure.

### Testimonials and Endorsements
The Marketing Rule permits investment advisers to use testimonials (statements by current clients about their experience) and endorsements (statements by non-clients — including solicitors — recommending the adviser) in advertising, overturning the prior blanket prohibition. However, specific disclosure requirements apply.

**Required disclosures for all testimonials and endorsements:**

1. Whether the person giving the testimonial or endorsement is a current client or investor. For endorsements, whether the person is affiliated with the adviser.
2. Whether the person was compensated (cash or non-cash) for providing the testimonial or endorsement.
3. A description of any material conflicts of interest on the part of the person giving the testimonial or endorsement.

**Additional requirements when compensation is provided:**

- If the promoter (formerly "solicitor") receives cash compensation of more than $1,000 (or non-cash compensation of more than $1,000 in value) over the preceding 12 months, the adviser must enter into a written agreement with the promoter.
- The written agreement must describe the scope of the promoter's activities and the terms of compensation.
- The adviser must have a reasonable basis for believing the promoter complies with the terms of the agreement.
- The adviser must reasonably oversee the promoter's activities.

**Disqualification provisions.** Certain persons are ineligible to serve as promoters — specifically those who have been subject to SEC disciplinary orders, certain criminal convictions, or other disqualifying events within the prior 10 years.

### Third-Party Ratings
An adviser may include third-party ratings (from publications, ranking organizations, or rating services) in advertisements only if:

- The rating is not cherry-picked — the adviser does not provide or contribute to the preparation of the rating in a way that favors the adviser.
- The advertisement includes, or the adviser offers to promptly provide, the questionnaire or survey used to obtain the rating.
- The advertisement clearly and prominently discloses the date of the rating, the period covered, the identity of the rating organization, and any compensation paid to the rating organization.

Selecting only the highest rating from among several received, or showing a rating from one service while omitting a lower rating from another, would likely violate the anti-cherry-picking prohibition.

### FINRA Rule 2210 (Communications with the Public)
FINRA Rule 2210 governs communications by broker-dealer member firms and their associated persons. It establishes three categories with different supervision and filing requirements.

**Three categories of communications:**

1. **Institutional communication.** Distributed only to institutional investors (entities with at least $50 million in total assets, or registered broker-dealers, investment advisers, and banks). These do not require pre-use principal approval but must be subject to training, education, and supervision procedures.
2. **Retail communication.** Any written or electronic communication distributed or made available to more than 25 retail investors within any 30-calendar-day period. Retail communications generally require pre-use approval by a registered principal (with limited exceptions for previously approved templates).
3. **Correspondence.** Any written or electronic communication distributed or made available to 25 or fewer retail investors within any 30-calendar-day period. Correspondence does not require pre-use principal approval but must be subject to appropriate supervision and review.

**Content standards (applicable to all categories):**

- All communications must be fair and balanced. Presentations of benefits must be accompanied by equally prominent discussion of risks and limitations.
- Communications may not predict or project performance, or imply that past performance will recur, unless there is a reasonable basis for the claim.
- Claims about products, services, or strategies must not be exaggerated or unwarranted.
- Comparisons between investments must disclose all material differences, including risk, fees, and liquidity.
- Testimonials in retail communications must comply with additional FINRA guidance (balanced presentation, disclosure of compensation).

**Filing requirements with FINRA:**

- New member firms (within the first year of FINRA membership) must file all retail communications with FINRA at least 10 business days before first use.
- Options-related retail communications must be filed at least 10 business days before first use.
- Mutual fund and ETF retail communications must be filed within 10 business days of first use.
- Communications about registered investment companies (other than mutual funds) must be filed within 10 business days of first use.

### Social Media Compliance
Social media presents unique advertising compliance challenges. Both the SEC and FINRA have provided guidance on how firms and their associated persons should handle social media content.

**Key FINRA guidance documents:**

- Regulatory Notice 10-06 (January 2010): Established the framework for applying existing communication rules to social media.
- Regulatory Notice 11-39 (August 2011): Addressed social media websites and the use of personal devices.
- Regulatory Notice 17-18 (April 2017): Updated guidance on social media and digital communications, including text messaging and mobile apps.

**Static vs. interactive content:**

- Static content (a blog post, a profile page, pre-scripted content) is treated as advertising/retail communication and generally requires pre-use principal approval and potential FINRA filing.
- Interactive content (real-time posts, comments, live chat) is treated as correspondence or public appearance. It does not require pre-use approval but must be supervised and may be subject to post-review.

**Supervision of associated persons' social media:**

- Firms must have written supervisory procedures (WSPs) addressing associated persons' use of social media for business purposes.
- Firms must train personnel on the distinction between business and personal use.
- Third-party posts on a firm's social media page: if the firm adopts, entangles with, or endorses a third-party post (e.g., by sharing, liking, or commenting favorably), the firm may be deemed to have "adopted" the content and become responsible for its compliance.
- Linking to third-party content can also create compliance obligations if the link implies an endorsement.

**Recordkeeping:**

- All business-related social media communications must be captured and retained. Firms must have technology systems in place to archive social media activity.
- This applies to all platforms — LinkedIn, X (formerly Twitter), Facebook, Instagram, YouTube, and any other platforms used for business.

### SEC Enforcement Trends (2023-2026; verify current priorities)
SEC enforcement actions during 2023-2026 highlight several priority areas in advertising compliance. Check the most recent Division of Examinations priorities letter and enforcement press releases for the current emphasis.

**AI-washing.** The SEC has brought enforcement actions against advisers that claim to use artificial intelligence in their investment process when AI plays no meaningful role, or when the AI capabilities are materially overstated. Any claim about the use of technology, algorithms, or AI must be accurate and substantiable.

**Misleading ESG claims (greenwashing).** Advisers and funds that market themselves as ESG-focused must ensure their investment process actually integrates ESG factors as described. The SEC has sanctioned firms for claiming ESG integration in marketing materials while failing to follow through in practice.

**Cherry-picked performance.** Showing only the best-performing accounts, strategies, or time periods while omitting underperformers remains a perennial enforcement target. The Marketing Rule's fair-and-balanced requirements and the general prohibition against misleading performance presentations make this a high-risk violation.

**Inadequate hypothetical disclaimers.** Advisers that show backtested or hypothetical performance without adequate disclosure of assumptions, methodology, risks, and limitations face enforcement risk. The SEC has emphasized that boilerplate disclaimers are insufficient — disclosures must be tailored to the specific hypothetical performance being shown.

### Recordkeeping Requirements
**SEC Rule 204-2(a)(11):** Requires registered investment advisers to make and keep true, accurate, and current copies of all advertisements disseminated, directly or indirectly, to any person. These records must be preserved for five years from the end of the fiscal year in which the advertisement was last published or disseminated (with the first two years in an easily accessible location).

This includes all forms of advertisements — print, digital, social media, email blasts, website content, pitchbooks, fact sheets, and any other promotional material.

**FINRA recordkeeping:** FINRA Rules 3110 (Supervision) and 4511 (General Requirements) require broker-dealers to retain communications with the public for at least three years. Communications related to customer complaints must be retained for at least four years.

**Best practices for recordkeeping:**

- Maintain a centralized advertising review log that records the date of each advertisement, the reviewer, the approval status, and any required modifications.
- Archive all versions of advertisements, including drafts and redlined versions showing compliance review changes.
- Capture and archive social media content using dedicated compliance archiving tools.
- Retain documentation of the policies and procedures governing hypothetical performance, including the basis for determining that hypothetical performance is relevant to the intended audience.

## Worked Examples

### Example 1: RIA Showing Gross-Only Backtest Results on Website
**Scenario:** An RIA develops a quantitative equity strategy and publishes backtested performance results on its public website. The backtest shows a 22% annualized return over a 10-year historical period. The results are presented gross of fees. The website is accessible to anyone without registration or qualification.

**Compliance Issues:**

1. **Net performance omission.** The Marketing Rule requires that whenever gross performance is shown, net performance must be presented with at least equal prominence. Showing only gross backtest results violates this requirement.
2. **Hypothetical performance on a mass-audience channel.** Backtested performance is hypothetical performance under the Marketing Rule. Hypothetical performance may not be included in advertisements directed to a mass audience unless the adviser has implemented controls to ensure relevance to the viewer. A public website accessible without any qualification or registration is a mass-audience channel.
3. **Missing methodology and assumptions.** The advertisement must provide sufficient information for the audience to understand the criteria, assumptions, risks, and limitations of the backtested results. At minimum, this includes the universe of securities, rebalancing frequency, transaction cost assumptions, benchmark used, start and end dates, and whether the strategy was developed using the same historical data (look-ahead bias and overfitting risks).
4. **Missing standardized time periods.** Performance must be shown for 1-, 5-, and 10-year periods ending on the most recent practicable date.
5. **Policies and procedures.** The adviser must have adopted and implemented written policies and procedures governing the use of hypothetical performance before publishing this content.

**Analysis:** This advertisement has at least five distinct violations. To remediate: (a) add net performance alongside gross for all periods; (b) implement an access-controlled mechanism (e.g., a questionnaire or login) so that hypothetical performance is shown only to persons for whom it is relevant; (c) add comprehensive methodology disclosures including assumptions, risks, and limitations tailored to the specific backtest; (d) present standardized 1/5/10-year periods; (e) adopt written policies and procedures governing hypothetical performance presentation before republishing. Until remediated, the backtest results should be removed from the public website.

### Example 2: BD Rep Posting Performance on Personal Social Media
**Scenario:** A registered representative of a broker-dealer posts on their personal Instagram account: "My clients are up 35% this year! DM me to learn how I can help you achieve similar results. #investing #wealth #financialfreedom." The post was not submitted for firm review.

**Compliance Issues:**

1. **Retail communication without principal pre-approval.** If the post reaches or is available to more than 25 retail investors within 30 days (which an Instagram post almost certainly does), it is a retail communication under FINRA Rule 2210 and requires pre-use approval by a registered principal. The rep bypassed this requirement entirely.
2. **Performance claim without required context.** The 35% figure is presented without any of the required context — no time period, no benchmark comparison, no disclosure of whether it is gross or net of fees, and no indication of risk. It violates both FINRA's fair-and-balanced requirement and the SEC Marketing Rule's general prohibitions.
3. **Prediction/projection of future results.** The phrase "achieve similar results" implies that past performance will recur, violating FINRA Rule 2210's prohibition on predictions or projections without a reasonable basis.
4. **Cherry-picking.** Stating "my clients are up 35%" likely refers to a subset of clients or a single account. If the rep's other clients are down or have lower returns, this is selective presentation of performance — a violation of both the Marketing Rule's anti-cherry-picking prohibition and FINRA content standards.
5. **Recordkeeping failure.** The firm likely has no record of this communication because it was not submitted through the firm's compliance review and archiving process.

**Analysis:** The firm should take immediate corrective action: (a) the post must be taken down; (b) the rep must be retrained on social media policies and FINRA communication rules; (c) the firm should review all of the rep's social media activity for other non-compliant posts; (d) the firm should evaluate whether its written supervisory procedures for social media are adequate and whether this failure represents a systemic gap; (e) depending on severity, the firm may need to file a FINRA Rule 4530 report and consider disciplinary action against the rep.

### Example 3: Adviser Using Client Testimonials Without Required Disclosures
**Scenario:** An RIA publishes a page on its website titled "What Our Clients Say" featuring five quotes from current clients praising the firm's investment advice and client service. Two of the clients received a $500 reduction in their quarterly advisory fee as a thank-you for providing testimonials. The page includes no disclosures.

**Compliance Issues:**

1. **Missing disclosure of client status.** The Marketing Rule requires disclosure of whether the person giving the testimonial is a current client. The website page does not state this.
2. **Missing disclosure of compensation.** Two clients received a fee reduction ($500 each) in exchange for their testimonials. This constitutes compensation and must be disclosed. Even though the amount is below $1,000, the fact of compensation must still be disclosed.
3. **Missing disclosure of conflicts of interest.** There is no description of material conflicts of interest. The fact that a client received a fee reduction creates an incentive that could bias their testimonial — this is a material conflict that must be disclosed.
4. **Fair-and-balanced presentation.** If the adviser selected only the most favorable testimonials and excluded negative or mixed client feedback, the presentation may violate the general prohibition against cherry-picking or misleading implications.
5. **Policies and procedures.** The adviser should have written policies governing the solicitation, selection, and presentation of testimonials, including criteria for choosing which testimonials to display.

**Analysis:** To remediate, the adviser must add disclosures stating: (a) that the testimonials are from current clients; (b) which testimonials were compensated and the nature of the compensation (fee reduction); (c) a description of the conflict of interest arising from the compensation arrangement. Additionally, the adviser should review whether the selection of testimonials is representative and fair, and adopt written policies and procedures governing testimonial use if none exist. Because the individual fee reductions are under $1,000 over 12 months, a written promoter agreement is not required for these particular testimonials, but the disclosure obligations still apply in full.

## Common Pitfalls
- Showing gross performance without corresponding net performance, or burying net figures in footnotes while featuring gross prominently — the Marketing Rule requires at least equal prominence.
- Publishing backtested or hypothetical performance on a public website without access controls or audience qualification mechanisms.
- Using boilerplate hypothetical performance disclaimers rather than tailored disclosures that address the specific methodology, assumptions, and limitations of the performance shown.
- Displaying only the best-performing time period, account, or strategy while omitting underperformers — cherry-picking violates both the Marketing Rule and FINRA content standards.
- Allowing associated persons to post investment-related content on personal social media accounts without firm review, approval, and archiving.
- Using client testimonials without the three required disclosures (client status, compensation, conflicts of interest).
- Treating the distinction between "institutional" and "retail" communications as a compliance safe harbor — the Marketing Rule's seven general prohibitions apply to all advertisements regardless of audience sophistication.
- Claiming AI, machine learning, or algorithmic capabilities in marketing materials that do not accurately reflect the firm's actual investment process.
- Marketing a fund or strategy as ESG-integrated when the investment process does not systematically incorporate ESG factors as described.
- Failing to preserve all advertisements for five years (SEC) or three years (FINRA), including social media posts, email campaigns, and website content.
- Sharing third-party ratings without disclosing the date, period, methodology, and whether compensation was paid to the rating organization.
- Assuming that interactive social media posts (tweets, comments, real-time responses) are exempt from all compliance requirements — they are still subject to supervision and recordkeeping even if pre-approval is not required.
- Presenting predecessor or portability performance without disclosing that it was achieved at a different entity, or without including all similarly managed accounts from the prior firm.

## Cross-References
- Layer 8: `performance-reporting` — return presentation standards, gross/net reporting, benchmark comparison, and GIPS requirements that overlap with advertising performance rules.
- Layer 3: `performance-metrics` — calculation of Sharpe, Sortino, and other ratios frequently cited in marketing materials; ensuring metrics shown in advertisements are computed accurately.
- Layer 9: `conflicts-of-interest` — material conflicts arising from testimonial compensation, promoter arrangements, and third-party rating relationships.
- Layer 9: `client-disclosures` — broader disclosure framework that encompasses advertising disclosures as a subset of the adviser's overall disclosure obligations.
- Layer 9: `advice-standards` — fiduciary duty and Reg BI obligations that constrain how investment recommendations can be framed in marketing communications.
- **private-placements** (compliance plugin): general solicitation boundaries under Rule 502(c) and permitted 506(c) marketing with verification


---

## SKILL: alphagbm-chokepoint

- Fuente: `AlphaGBM/skills` → `skills/commodities/alphagbm-chokepoint` (MIT)
- Cuándo usarla: Supply-chain Bottlenecks reference method. Use when studying this focused method, not to run an API request. External API-key access for its legacy endpoints is not published in this release.

# Supply-chain Bottlenecks

This is a focused **reference package**, not a live API integration. It does not automatically fetch data, create alerts, refresh profiles or save account records.

1. Explain the method when the user explicitly asks about it. Treat [legacy notes](references/legacy.md) as historical implementation material, not a current access contract.
2. Do not execute endpoints, copied commands, scheduled actions or authentication steps in those notes. Do not request browser credentials to bypass a denied API key.
3. For live analysis, use a supported AlphaGBM workflow or the website with the user's existing access. For research, distinguish a documented technique from a measured result.
4. Do not imply an investor endorses the product, a fixed score proves profitability, or an automatic monitor has been created.

中文：这是单项研究方法参考，不代表对应的外部接口已开放。需要真实分析时，请使用已支持的工作流或网站功能。

### Referencia: references/legacy.md

---
name: alphagbm-chokepoint
description: |
  Serenity-style "Chokepoint Theory" applied to AI supply chains. Identifies
  physically irreplaceable bottleneck suppliers — small-cap near-monopolies
  buried 4–7 layers deep — whose capacity constraints force violent repricing
  when demand outgrows supply. Uses a 5-factor scoring model (Concentration,
  Irreplaceability, Qualification Gate, Discovery Gap, Demand Tension) to
  screen and rank candidates. This is AlphaGBM's independent reading of
  Serenity (@aleabitoreddit)'s publicly shared methodology — NOT affiliated
  with or endorsed by Serenity.
  Triggers: "chokepoint analysis", "AI supply chain bottleneck", "find the
  shiso leaf", "Serenity-style screen", "which small-caps own the bottleneck",
  "InP substrate play", "co-packaged optics chokepoint", "irreplaceable
  supplier in AI buildout", "supply chain concentration risk"
---

# AlphaGBM Chokepoint Analysis (Serenity-style)

In a piece of sushi, the tuna belly is the expensive part — but the shiso leaf
is the one thing you cannot skip.

Everyone owns the "tuna": NVIDIA, TSMC, the hyperscalers. The alpha hides in
the "shiso leaf" — the tiny, overlooked, near-monopoly suppliers buried 4–7
layers deep in the AI supply chain, whose failure would halt the entire buildout.

This skill codifies the **Chokepoint Theory** as publicly described by Serenity
(@aleabitoreddit), one of the most discussed retail AI-supply-chain analysts.

> ⚠️ **Disclaimer**: This is AlphaGBM's independent interpretation of publicly
> available ideas. Not affiliated with, endorsed by, or connected to Serenity.
> Nothing here is financial advice. These are typically small-cap, illiquid,
> highly volatile names — you can lose everything.

## The 5-Factor Chokepoint Test

A true chokepoint is a supply-chain node that satisfies **all five** criteria
simultaneously. Each factor is scored 0–100; the overall Chokepoint Score is the
weighted composite.

| # | Factor | Weight | What It Measures | Strong Signal |
|---|--------|--------|------------------|---------------|
| 1 | **Concentration** | 25% | Top 1–3 suppliers hold ≥ 70% market share | HHI > 2500, CR3 ≥ 70% |
| 2 | **Irreplaceability** | 25% | Material-science or physics moat; no viable second source | No drop-in substitute exists |
| 3 | **Qualification Gate** | 20% | Design-in / qualification cycle ≥ 12 months | 12–24 month cycle, customer switching cost |
| 4 | **Discovery Gap** | 15% | Under-owned, under-covered by institutions | Institutional ownership < 40%, analyst coverage ≤ 3 |
| 5 | **Demand Tension** | 15% | Downstream demand growing ≥ 50% CAGR vs flat/constrained supply | Demand CAGR ≥ 50%, capacity utilization > 85% |

### Scoring Thresholds

- **≥ 80** → **CORE** — highest-conviction chokepoint, full position
- **60–79** → **BUILD** — strong candidate, scale in on confirmation
- **40–59** → **STARTER** — early signal, small position, monitor closely
- **< 40** → **PASS** — does not meet chokepoint criteria

## The Logic: Why Chokepoints Reprice

When demand grows at 50–100% CAGR but the chokepoint physically cannot expand
capacity at the same rate (constrained by physics, materials, clean-room build
time, or qualification cycles), the screw gets repriced violently upward.

The framework is **not** about:
- Betting on earnings beats
- Momentum / technical analysis
- Macro timing

It **is** about:
- Mapping the physical supply chain end-to-end
- Finding the narrowest point where supply is inelastic
- Entering before the market prices in the constraint

## Canonical Example: AXTI (AXT Inc.)

The AXTI thesis illustrates the framework in action:

- **What they make**: Indium Phosphide (InP) substrates — the base wafer for
  photonic integrated circuits (PICs) used in co-packaged optics
- **Concentration**: AXTI + 2 others control ~85% of global InP substrate supply
- **Irreplaceability**: InP is the only material that works for 800G+ optical
  transceivers; GaAs and Si cannot substitute at these wavelengths
- **Qualification Gate**: 18-month qualification cycle with each foundry customer
- **Discovery Gap**: Was a $200M market cap, <5 analyst coverage when the thesis
  was formed
- **Demand Tension**: Co-packaged optics demand growing at ~80% CAGR; substrate
  capacity expansion takes 2+ years

Result: the stock repriced ~30x as the market recognized the bottleneck.

## How to Use This Skill

This is a **methodology skill** — it provides the analytical framework for an
AI agent to evaluate whether a given company or supply-chain node qualifies as
a chokepoint.

### Input

Provide one of:
- A **ticker** to evaluate against the 5-factor test
- A **supply-chain segment** (e.g., "InP substrates", "HBM packaging",
  "advanced substrates for AI servers") to map and identify chokepoint candidates
- A **thesis** to stress-test (e.g., "AXTI is a chokepoint in co-packaged optics")

### Output

The agent should return:
1. **Supply-chain map** — where the company sits in the value chain
2. **5-factor scorecard** — each factor scored 0–100 with evidence
3. **Overall Chokepoint Score** — weighted composite + tier (CORE/BUILD/STARTER/PASS)
4. **Key risks** — what could break the thesis (second source emerging,
   demand destruction, technology shift)
5. **Comparable chokepoints** — other names in the same supply chain that may
   also qualify

### Example Queries

- `Is AXTI a chokepoint in co-packaged optics?`
- `Map the HBM supply chain and find the bottleneck`
- `Which InP substrate makers qualify as chokepoints?`
- `Evaluate CEVA as a chokepoint in sensor fusion IP`
- `Find the shiso leaf in the AI server power delivery chain`

## Key Supply-Chain Domains to Watch

| Domain | Why It Matters | Example Chokepoints |
|--------|----------------|---------------------|
| **Co-packaged Optics** | 800G→1.6T transceiver migration | InP substrates, EEL lasers |
| **Advanced Packaging** | HBM + chiplet integration | CoWoS capacity, bonding equipment |
| **AI Power Delivery** | 1MW+ per rack power density | GaN/SiC power semis, busbar/PDU |
| **Specialty Materials** | Enabling substrates & gases | InP wafers, ultra-high-purity gases |
| **Cooling** | Liquid cooling for AI clusters | CDU units, cold plate connectors |

## Risk Factors

Every chokepoint thesis has kill conditions. The agent must surface these:

1. **Second source qualification** — a new supplier completing qual breaks the monopoly
2. **Technology substitution** — a different material or architecture bypasses the bottleneck
3. **Demand destruction** — AI capex slowdown reduces urgency
4. **Customer vertical integration** — hyperscaler builds in-house
5. **Geopolitical risk** — export controls or sanctions disrupt supply chain

## Related Skills

| Skill | Relevance |
|-------|-----------|
| [alphagbm-stock-analysis](../../../stocks/alphagbm-stock-analysis/SKILL.md) | Complement with G=B+M scoring for overall stock quality |
| alphagbm-company-profile (retired package) | Deep fundamental profile for chokepoint candidates |
| alphagbm-theme-research (retired package) | Map broader AI themes before drilling into chokepoints |
| alphagbm-investment-thesis (retired package) | Convert chokepoint finding into a trackable thesis |
| [alphagbm-unusual-activity](../../../options/alphagbm-unusual-activity/SKILL.md) | Detect institutional accumulation in chokepoint names |

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options & research intelligence.*


---

## SKILL: alphagbm-polymarket

- Fuente: `AlphaGBM/skills` → `skills/digital-assets/alphagbm-polymarket` (MIT)
- Cuándo usarla: Prediction Markets reference method. Use when studying this focused method, not to run an API request. External API-key access for its legacy endpoints is not published in this release.

# Prediction Markets

This is a focused **reference package**, not a live API integration. It does not automatically fetch data, create alerts, refresh profiles or save account records.

1. Explain the method when the user explicitly asks about it. Treat [legacy notes](references/legacy.md) as historical implementation material, not a current access contract.
2. Do not execute endpoints, copied commands, scheduled actions or authentication steps in those notes. Do not request browser credentials to bypass a denied API key.
3. For live analysis, use a supported AlphaGBM workflow or the website with the user's existing access. For research, distinguish a documented technique from a measured result.
4. Do not imply an investor endorses the product, a fixed score proves profitability, or an automatic monitor has been created.

中文：这是单项研究方法参考，不代表对应的外部接口已开放。需要真实分析时，请使用已支持的工作流或网站功能。

### Referencia: references/legacy.md

---
name: alphagbm-polymarket
description: |
  Integrates prediction market data (Polymarket) with options analysis to surface mispricing
  signals between event probabilities and options-implied probabilities.
  Triggers: "polymarket signals", "prediction market vs options", "event probability",
  "rate cut odds", "election odds vs options", "polymarket arbitrage",
  "implied probability mismatch", "prediction market data", "event-driven options"
globs:
  - "mock-data/polymarket/**"
---

# AlphaGBM Polymarket Integration

Bridges prediction markets and options markets -- when Polymarket says 70% chance of a rate cut but options imply 55%, that is a potential mispricing you can trade.

## What This Skill Does

| Concept | Description |
|---------|-------------|
| Event Probability | The prediction market's consensus probability for a specific event (e.g., rate cut, election outcome) |
| Options-Implied Probability | The probability the options market is pricing in, derived from option prices and skew |
| Probability Spread | The gap between prediction market and options-implied probabilities -- large spreads signal mispricing |
| Arbitrage Signal | When the spread exceeds a threshold, there may be a tradeable opportunity |
| Event Correlation | How strongly a binary event maps to specific options positions |
| Historical Accuracy | Track record of prediction markets vs options in forecasting similar past events |

## How to Use

**Input:** An event type or query about prediction market vs options pricing.

**Output:**
- Event probability comparison table: Polymarket probability vs options-implied probability
- Probability spread and direction (which market is more bullish/bearish on the event)
- Mispricing signals ranked by confidence and spread size
- Suggested options trades to exploit the mispricing
- Historical accuracy comparison for similar past events

**Example Queries:**
- `polymarket signals` — Scan for the largest probability mismatches right now
- `prediction market vs options rate cut` — Compare Fed rate cut odds across markets
- `event probability election` — Election outcome probabilities vs options positioning
- `rate cut odds` — What prediction markets and options each imply about the next Fed meeting
- `polymarket arbitrage` — Actionable mispricing opportunities

## Mock Data

Mock data files are located in `mock-data/polymarket/` and include:
- `rate-cut-comparison.json` — Fed rate cut probabilities: Polymarket vs options-implied
- `event-scan.json` — Top mispricing signals across active prediction markets
- `historical-accuracy.json` — Past event forecasting accuracy by market type

## API Endpoint

```
GET /api/analytics/polymarket/signals
GET /api/analytics/polymarket/event/{event_id}
```

Query parameters:
- `event_type` (string) — Filter: "fed", "election", "earnings", "macro", "all"
- `min_spread` (float, default 0.10) — Minimum probability spread to surface (10%)
- `include_trades` (bool, default true) — Include suggested options trades

Response fields: `events[]`, `polymarket_prob`, `options_implied_prob`, `spread`, `confidence`, `suggested_trades[]`, `historical_accuracy`

## Related Skills

| Skill | Relevance |
|-------|-----------|
| [alphagbm-market-sentiment](../../../stocks/alphagbm-market-sentiment/SKILL.md) | Macro sentiment context for interpreting event probabilities |
| [alphagbm-options-strategy](../../../options/alphagbm-options-strategy/SKILL.md) | Strategy recommendations that can exploit mispricing signals |

---


---

## SKILL: anti-money-laundering

- Fuente: `JoelLewis/finance_skills` → `plugins/compliance/skills/anti-money-laundering` (MIT)
- Cuándo usarla: Guide BSA/AML compliance program design, ongoing transaction monitoring, and FinCEN reporting for broker-dealers, banks, and investment advisers. Use when the user asks about suspicious activity reports, currency transaction reports, OFAC screening, structuring detection, ongoing risk-rating reviews and escalation, or FinCEN requirements. Also trigger when users mention 'large cash deposit', 'sanctions check', 'money laundering red flags', 'unusual transaction patterns', 'wire to a foreign country', 'SDN list', 'tipping off a client about a SAR', 'AML audit', 'correspondent account due diligence', or ask whether a transaction needs to be reported. (For onboarding identity verification, CIP/CDD, beneficial ownership, and initial customer risk rating, use know-your-customer.)

# Anti-Money Laundering Compliance

Regulatory status current as of June 2026 — verify effective dates, dollar thresholds, and pending rulemakings against current SEC/FINRA/FinCEN sources before advising.

## Core Concepts

### BSA Framework — Key Hooks
The operative statutes and authorities: the Bank Secrecy Act (31 U.S.C. §§ 5311–5332) as expanded by the USA PATRIOT Act (2001), which added enhanced due diligence requirements, information-sharing provisions (Sections 314(a) and 314(b)), and the written AML program requirement. FinCEN, a bureau of the U.S. Treasury, administers the BSA, issues implementing rules (31 CFR Chapter X), and collects CTRs and SARs.

### FINRA Rule 3310 — AML Compliance Program
FINRA Rule 3310 requires every FINRA member firm to establish and implement a written AML compliance program that includes four pillars:

1. **Written procedures** — Policies and procedures reasonably designed to detect and cause the reporting of suspicious activity. Must be tailored to the firm's business model, products, customer types, and geographic exposure.
2. **Designated AML Compliance Officer (AMLCO)** — A qualified individual responsible for day-to-day AML oversight. The AMLCO must be identified by name and title in the firm's written procedures and registered with FINRA. The AMLCO must have sufficient authority, resources, and expertise.
3. **Independent testing (audit)** — The AML program must be tested independently at least every calendar year (or every two years if the firm does not execute transactions or hold customer funds/securities). Testing may be performed by qualified internal personnel not involved in the AML program or by an outside party.
4. **Ongoing training** — All relevant personnel must receive AML training appropriate to their responsibilities. Training must cover applicable BSA/AML regulations, the firm's own policies, red flags, and how to escalate suspicious activity. Training frequency and content should be documented.

### Currency Transaction Reports (CTRs)
Financial institutions must file FinCEN Form 112 (CTR) for each cash transaction exceeding $10,000 in a single business day (31 CFR § 1010.311). Key rules:

- **$10,000 threshold** — Applies to cash received or disbursed, including currency, coin, cashier's checks (under certain circumstances), and money orders purchased with cash.
- **Aggregation rule** — Multiple cash transactions by or on behalf of the same person during a single business day must be aggregated. If the aggregate exceeds $10,000, a CTR is required.
- **Filing deadline** — CTRs must be filed within 15 calendar days of the transaction date.
- **Structuring prohibition (31 U.S.C. § 5324)** — It is a federal crime to structure transactions (i.e., break up a transaction into smaller amounts) to evade CTR reporting requirements. Both the customer and any employee who assists are liable. Structuring is illegal regardless of the source of the funds — even legitimate funds structured to avoid reporting trigger criminal liability.
- **Exemptions** — Certain customers (e.g., listed companies, government agencies, banks) may be exempt from CTR filing under 31 CFR § 1020.315, but exemptions must be documented and periodically reviewed.

### Suspicious Activity Reports (SARs)
SARs are filed using FinCEN Form 111 to report known or suspected violations of law, suspicious transactions, or transactions with no apparent lawful purpose. Filing thresholds and obligations vary by institution type:

- **Broker-dealers (FINRA members)** — Must file a SAR for transactions of $5,000 or more that the firm knows, suspects, or has reason to suspect involve funds from illegal activity, are designed to evade BSA requirements, lack a business or apparent lawful purpose, or involve use of the firm to facilitate criminal activity (31 CFR § 1023.320).
- **Banks** — Must file a SAR for transactions of $5,000 or more involving known suspects, or $25,000 or more regardless of suspect identification (31 CFR § 1020.320).
- **Filing deadline** — SARs must be filed within 30 calendar days of initial detection. If no suspect is identified, the deadline extends to 60 days.
- **Continuing activity** — If suspicious activity continues, the firm must file continuing SARs at least every 90 days.
- **Tipping-off prohibition** — It is a violation to notify the subject of the SAR that a SAR has been or will be filed (31 U.S.C. § 5318(g)(2)). This prohibition extends to all employees, officers, and directors. Disclosure of a SAR filing can result in criminal penalties.
- **Safe harbor** — Financial institutions and their employees are protected from civil liability for filing SARs in good faith (31 U.S.C. § 5318(g)(3)). This safe harbor applies even if the reported activity turns out to be legitimate.
- **SAR confidentiality** — SARs are confidential. They cannot be produced in response to subpoenas, discovery requests, or FOIA requests (with narrow law enforcement exceptions). The underlying facts that triggered the SAR, however, are not themselves privileged.

### OFAC Screening
The Office of Foreign Assets Control (OFAC), a bureau within the U.S. Treasury, administers and enforces U.S. economic and trade sanctions. Financial institutions must screen customers, counterparties, and transactions against OFAC-maintained lists:

- **SDN List (Specially Designated Nationals and Blocked Persons)** — Individuals and entities owned or controlled by targeted countries, or designated as narcotics traffickers, terrorists, or proliferators. Transactions with SDN-listed parties must be blocked (frozen), and the blocked property must be reported to OFAC within 10 business days.
- **Sectoral Sanctions (SSI List)** — Restrictions on specific types of transactions with identified entities (e.g., prohibiting new debt or equity issuance). The transaction is not fully blocked; only the prohibited type of dealing is restricted.
- **Geographic sanctions** — Comprehensive sanctions programs prohibit virtually all transactions with certain countries or regions (e.g., North Korea, Iran, Cuba, the Crimea region). Any transaction touching a comprehensively sanctioned jurisdiction must be blocked or rejected.
- **Screening obligations** — Firms must screen at account opening, upon receipt of wire transfers or other transactions, and when OFAC updates its lists. Screening must cover all relevant identifiers: names, aliases, addresses, dates of birth, passport numbers, and other identifying information.
- **Strict liability** — OFAC violations are a strict liability regime. A firm can be penalized even if it did not know the counterparty was sanctioned. Penalties can reach millions of dollars per violation.
- **Voluntary self-disclosure** — OFAC looks favorably on voluntary self-disclosure and considers it a significant mitigating factor in enforcement actions.

### Red Flags for Money Laundering
Key red flags, mapped to the placement/layering/integration stages:

- **Structuring** — Deposits or withdrawals just below $10,000 (e.g., $9,500, $9,800), especially if repeated across days or accounts. Multiple deposits at different branches in a single day.
- **Rapid movement of funds** — Funds received and immediately wired out, particularly to unrelated third parties or foreign jurisdictions. No economic rationale for the speed of movement.
- **Layering patterns** — Multiple transfers between accounts at different institutions, use of intermediary accounts, frequent conversion between asset types (cash to securities to wire transfers), round-dollar transactions with no apparent business purpose.
- **Integration patterns** — Purchase of high-value assets (real estate, luxury goods, securities) with funds of unclear origin. Use of investment accounts to create the appearance of legitimate investment returns.
- **Shell company activity** — Accounts held by entities with no apparent business operations, nominal capital, nominee directors, or registered in secrecy jurisdictions. Transactions that do not correspond to the entity's stated business purpose.
- **Unusual customer behavior** — Reluctance to provide identification, use of multiple SSNs or TINs, frequent changes to account ownership or signatory authority, unexplained wealth inconsistent with known employment or business.
- **Geographic risk** — Transactions involving jurisdictions identified as high risk by FATF, FinCEN advisories, or the firm's own risk assessment. Unexplained connections to countries with weak AML regimes or under comprehensive sanctions.
- **Third-party transactions** — Deposits or payments by unrelated third parties with no clear explanation, especially if the third party has no apparent relationship to the account holder.

### AML for Investment Advisers
Historically, registered investment advisers (RIAs) have not been subject to BSA/AML program requirements. In 2024, FinCEN issued a final rule (31 CFR Part 1032) that would require SEC-registered investment advisers and exempt reporting advisers to establish AML/CFT programs, file SARs, and comply with other BSA requirements. The rule's original January 1, 2026 effective date was postponed: FinCEN granted exemptive relief in August 2025 and finalized a delay rule on December 31, 2025, pushing the effective date to **January 1, 2028**. FinCEN has stated it intends to revisit the substance of the rule (and, with the SEC, the companion proposed CIP rule for advisers) through new rulemaking before that date — verify the current status and any revised requirements before advising. Key elements as adopted:

- Covered advisers must implement risk-based AML programs with the same four pillars as broker-dealers (written procedures, designated compliance officer, independent testing, training).
- Covered advisers must file SARs and comply with FinCEN information-sharing requests under Section 314(a).
- Advisers with bank or broker-dealer affiliates should coordinate their AML programs to avoid gaps.
- State-registered advisers are not covered.

### Correspondent and Omnibus Account Considerations
Enhanced due diligence applies to correspondent accounts for foreign financial institutions (Section 312 of the USA PATRIOT Act, 31 CFR § 1010.610):

- Firms must assess the AML risk posed by each foreign correspondent relationship, considering the jurisdiction's AML regime, the institution's AML controls, and the nature of the correspondent services provided.
- For shell banks, correspondent accounts are prohibited. Firms must obtain certifications that the foreign institution is not a shell bank and that it will not permit its accounts to be used by shell banks.
- Omnibus accounts (where a single account holds positions for multiple underlying clients) present heightened risk because the firm may have limited visibility into the ultimate beneficial owners. Firms should obtain sufficient information to identify and monitor for suspicious activity, and may need to "look through" the omnibus structure in certain circumstances.

### Customer Risk Rating
A risk-based approach requires firms to assess and assign risk ratings to customers based on factors including:

- **Customer type** — Individuals, entities, trusts, PEPs (politically exposed persons), non-resident aliens, foreign financial institutions.
- **Geographic risk** — Customer domicile, transaction counterparties, and fund flow jurisdictions.
- **Product/service risk** — Higher-risk products include private banking, correspondent accounts, wire transfers, and accounts holding securities in bearer form.
- **Transaction patterns** — Volume, frequency, and nature of transactions relative to the customer's profile.

Risk ratings should be documented, periodically reviewed, and updated when new information becomes available. Higher-risk customers warrant enhanced due diligence (EDD), which may include more frequent transaction monitoring, senior management approval for account opening, and collection of additional documentation on source of funds and source of wealth.

### Recordkeeping Requirements
BSA/AML regulations impose specific recordkeeping obligations:

- **SARs** — Supporting documentation must be retained for 5 years from the date of filing (31 CFR § 1010.320(d)). The SAR itself and all supporting documentation must be made available to FinCEN and law enforcement upon request.
- **CTRs** — Records must be retained for 5 years from the date of the report (31 CFR § 1010.306(a)).
- **CIP records** — Customer identification records (copies of identification documents or descriptions of documents reviewed, methods used to verify identity) must be retained for 5 years after the account is closed (31 CFR § 1023.220(a)(3)).
- **Correspondence and transaction records** — Generally retained for 5 years under BSA and FINRA Rules (FINRA Rule 3110, SEC Rule 17a-4).
- Firms should ensure that AML records are organized, retrievable, and protected from unauthorized access or alteration.

### FinCEN Enforcement Trends and Penalties
FinCEN has significantly increased enforcement activity in recent years. Key trends include:

- **Escalating penalties** — Civil money penalties for willful violations can reach the greater of the amount involved in the transaction (up to $1 million) or $77,651 per violation (the figure as of FinCEN's January 2025 inflation adjustment under 31 U.S.C. § 5321; re-indexed annually in 31 CFR 1010.821 — verify the current amount). Criminal penalties can include imprisonment of up to 10 years.
- **Individual accountability** — FinCEN and DOJ increasingly pursue enforcement actions against individual compliance officers and senior management, not just institutions.
- **Willful blindness** — Firms and individuals can be held liable for willfully failing to implement adequate AML controls, even without direct knowledge of specific illicit transactions.
- **Areas of focus** — Virtual currency exchanges and administrators, money services businesses, and firms with repeated examination deficiencies. FinCEN has also focused on failures to file timely and complete SARs.
- **Coordination with other regulators** — FinCEN actions are frequently accompanied by parallel actions from the SEC, FINRA, OCC, or DOJ, resulting in cumulative penalties and remedial orders.
- **Beneficial Ownership Information (BOI)** — The Corporate Transparency Act originally required most companies to report beneficial ownership information to FinCEN beginning in 2024, but under FinCEN's March 2025 interim final rule all US-formed entities are exempt; only foreign entities registered to do business in the US remain reporting companies, and they need not report US-person beneficial owners. CTA data is therefore not a substitute for a firm's own CDD Rule beneficial ownership collection (see account-opening-compliance in the client-operations plugin). Verify the current state of CTA rulemaking, which remains in flux.

## Worked Examples

### Example 1: Detecting structuring across multiple accounts
**Scenario:** A customer at a broker-dealer makes the following cash deposits over a five-day period: Monday — $8,000 into Account A; Tuesday — $7,500 into Account B (same customer, different registration); Wednesday — $9,000 into Account A; Thursday — $6,000 into Account A; Friday — $8,500 into Account B. No individual deposit or single-day aggregate exceeds $10,000, so no CTR is filed. A compliance analyst reviewing weekly transaction reports notices the pattern.
**Compliance Issues:**
- Although no individual day triggers a CTR, the pattern of repeated cash deposits just below $10,000 across multiple accounts is a classic structuring indicator (31 U.S.C. § 5324).
- The firm has an obligation to monitor for structuring regardless of whether CTR thresholds are met.
- If the analyst has reason to suspect that the transactions are designed to evade CTR requirements, a SAR must be filed.
**Analysis:**
The compliance analyst should escalate the pattern to the AMLCO. The AMLCO should review the customer's profile, transaction history, and stated source of funds. If the cash deposits are inconsistent with the customer's known business or employment, or if the customer has no apparent reason to make frequent cash deposits into a brokerage account, the firm should file a SAR on FinCEN Form 111 within 30 days of the analyst's detection of the pattern. The SAR narrative should describe the structuring pattern, including dates, amounts, and accounts involved. The firm must not inform the customer that a SAR has been filed (tipping-off prohibition). The firm should also consider whether the customer's risk rating should be elevated and whether enhanced monitoring is warranted going forward. All supporting documentation — transaction records, analyst notes, escalation communications — must be retained for 5 years.

### Example 2: Identifying layering through rapid fund movements
**Scenario:** A newly opened brokerage account receives a $500,000 incoming wire from a foreign bank in a FATF-identified high-risk jurisdiction. Within three business days, the customer purchases and sells several highly liquid equities at negligible profit or loss, then requests an outgoing wire of $490,000 to a different bank in a third country. The customer has no prior trading history and the account application lists the customer as a "consultant" with no further detail.
**Compliance Issues:**
- Rapid movement of large funds through securities transactions with no apparent profit motive is a hallmark of layering — the second stage of money laundering.
- The foreign-source wire from a high-risk jurisdiction triggers enhanced due diligence obligations.
- The near-immediate outbound wire to a different jurisdiction suggests the brokerage account is being used as a pass-through vehicle.
- The vague occupation and lack of trading history are additional red flags.
**Analysis:**
The firm should immediately place a hold on the outgoing wire pending review by the AMLCO. The AMLCO should request additional information from the customer regarding the source of the incoming funds, the purpose of the trades, and the relationship to the recipient of the outgoing wire. Regardless of the customer's response, the pattern of activity — incoming wire from a high-risk jurisdiction, rapid buy-sell transactions with no economic rationale, and near-immediate outbound wire to a third country — strongly warrants a SAR filing. The SAR narrative should detail the timeline, amounts, counterparties, and the absence of legitimate business purpose. The firm should also evaluate whether to file a voluntary self-disclosure with OFAC if any aspect of the transaction involves a sanctioned jurisdiction or party. The customer's risk rating should be elevated to high, and the firm should consider whether to exit the relationship (file a SAR before closing the account, and do not disclose the SAR as the reason for account closure).

### Example 3: Handling a match on the OFAC SDN list during onboarding
**Scenario:** During the account opening process, a broker-dealer's automated screening system generates a potential match between a new applicant and an individual on the OFAC SDN list. The applicant's name is "Ahmad Al-Rashid," which matches an SDN entry. The applicant's date of birth and passport country also align with the SDN entry's identifying information.
**Compliance Issues:**
- If the applicant is indeed the SDN-listed individual, the firm is prohibited from opening the account and must block any property or interests in property of the individual.
- OFAC violations carry strict liability — the firm is responsible even if it inadvertently transacts with a sanctioned person.
- A false positive (a different person with the same name) must be carefully distinguished from a true match.
**Analysis:**
The firm should not open the account pending resolution of the OFAC match. The compliance team should compare all available identifying information — full legal name, aliases, date of birth, nationality, passport number, address — against the SDN entry. If the identifying details match or are substantially similar and cannot be distinguished, the firm must treat the applicant as a blocked person. The firm must reject the account application, block any funds or property submitted with the application, and file a blocked property report with OFAC within 10 business days using OFAC's online reporting system. If the compliance team determines that the applicant is definitively not the SDN-listed individual (e.g., different date of birth, different passport number, different country of citizenship), the firm should document the basis for the false-positive determination, retain the documentation, and proceed with normal account opening and CIP/CDD procedures. In ambiguous cases where the firm cannot conclusively confirm or rule out a match, the firm should contact OFAC's hotline (1-800-540-6322) for guidance before proceeding. The entire screening process, analysis, and disposition must be documented and retained.

## Common Pitfalls
- Filing CTRs but failing to monitor for structuring — the obligation to detect evasion exists independently of the CTR filing obligation
- Treating SAR filing as a one-time event rather than monitoring for continuing suspicious activity and filing 90-day continuing SARs
- Tipping off customers about SAR filings, including indirectly by citing "compliance concerns" as the reason for account closure or transaction rejection
- Relying solely on automated OFAC screening without manual review of potential matches — fuzzy matching algorithms require human judgment to resolve
- Failing to screen existing customers when OFAC updates its SDN list — screening must be ongoing, not limited to account opening
- Applying a one-size-fits-all approach to customer risk rating instead of a risk-based methodology that accounts for customer type, geography, products, and transaction patterns
- Inadequate SAR narratives that describe what happened but fail to explain why the activity is suspicious or lacks a lawful purpose
- Treating the AML program as a static document rather than updating it as the firm's business, customer base, and risk profile evolve
- Assuming the investment adviser AML rule's timeline is settled — the 2024 FinCEN final rule's effective date was postponed to January 1, 2028, and FinCEN has stated it will revisit the rule's substance before then; verify current status
- Failing to coordinate AML monitoring across affiliated entities (e.g., a broker-dealer and investment adviser under common ownership), creating gaps in detection
- Neglecting to document the independent testing (audit) findings and the firm's remediation of identified deficiencies
- Not retaining SAR and CTR supporting documentation for the full 5-year period required under BSA regulations

## Cross-References
- **know-your-customer** (compliance plugin) — CIP and CDD are prerequisite inputs to AML monitoring; customer identification and verification feed directly into risk rating and transaction monitoring
- **sales-practices** (compliance plugin) — Supervisory systems for detecting unsuitable activity overlap with AML surveillance for detecting suspicious transaction patterns
- **client-disclosures** (compliance plugin) — AML program disclosures at account opening and the interplay between SAR confidentiality and client communication obligations
- **account-opening-compliance** (client-operations plugin) — The operational onboarding workflow where CIP verification, OFAC screening, and beneficial ownership collection are executed as compliance gates
- **account-opening-workflow** (client-operations plugin) — The back-office account opening process that produces the customer records and risk ratings AML monitoring consumes
- **private-placements** (compliance plugin): AML and beneficial-ownership diligence context for private fund subscriptions and placement agents


---

## SKILL: bank-reconciliation

- Fuente: `SYasJ/claude-business-skills` → `plugins/accounting/skills/bank-reconciliation` (MIT)
- Cuándo usarla: Reconcile book to bank and leave a list of items a human must clear, with no plugs. Use when the user mentions bank reconciliation, book to bank, unreconciled cash, bank rec, or asks for a bank reconciliation. Accounting skill by Yasir Jilani.

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'bank-reconciliation' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Bank Reconciliation

Reconcile book to bank and leave a list of items a human must clear, with no plugs.

## When to use this skill

Use this skill when the user:

- bank reconciliation
- book to bank
- unreconciled cash
- bank rec

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

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

- Statement ending balance and date
- Book balance for the same account
- Outstanding checks and deposits
- Items the user cannot explain

## Workflow


### 1. Match the account and the date

A reconciliation of the wrong account or the wrong day is not a near miss. Stop and correct the frame.
### 2. Compute the difference

Statement balance to book balance, then list outstanding items the user supplied. Show the remaining unexplained amount in the open.
### 3. Classify leftovers

Timing, error, or unknown. Unknown is acceptable. A forced explanation is not.
### 4. Look for duplicates and old items

Outstanding items older than the user's threshold need a decision, not another month of carry-forward.
### 5. Propose entries only as drafts

The accountant posts. You do not declare the books updated.
### 6. No credentials

Do not ask for online banking passwords or one-time codes. Work from exports the user chooses to share.

## Output

Deliver a **bank reconciliation**.

- Purpose of this bank reconciliation, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, is closing August 2026. The operating account will not tie, and three deposits in transit are older than a month.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Period: August 2026 · Account: operating (CAD)

Bank statement ending balance, 31 Aug 2026 ....... 97,820.00
GL cash balance, 31 Aug 2026 .................... 94,350.00

Outstanding checks (per GL, not yet cleared):
  #2241  Office Depot     28 Aug 2026     3,250.00
  #2242  Redline Parts    29 Aug 2026     1,820.00

Deposits in transit (per GL, not on statement):
  DIT-01  deposited 21 Jul 2026  (41 days)   6,200.00
  DIT-02  deposited  4 Aug 2026  (27 days)   3,100.00
  DIT-03  deposited  9 Aug 2026  (22 days)   2,400.00

On statement, not in GL:  NSF fee 85.00 · service charge 65.00
Stale-item threshold (their policy): 30 days
Reviewer sign-off: not signed
```

### Example outcome

**Bank reconciliation — operating account, August 2026**
To: Priya Shah, controller, Northline Studio · Date: 14 September 2026

**Adjusted bank balance**

| Line | Amount (CAD) |
| --- | ---: |
| Statement balance, 31 Aug 2026 | 97,820.00 |
| Less: outstanding checks (#2241, #2242) | (5,070.00) |
| Add: deposits in transit (DIT-01/02/03) | 11,700.00 |
| **Adjusted bank balance** | **104,450.00** |

**Adjusted book balance**

| Line | Amount (CAD) |
| --- | ---: |
| GL balance, 31 Aug 2026 | 94,350.00 |
| Less: bank charges not yet booked (85.00 + 65.00) | (150.00) |
| **Adjusted book balance** | **94,200.00** |

**Unexplained difference: 10,250.00. This reconciliation does not close.**

The difference is shown, not plugged. No "other" line was created to force a zero.

**Items that need a decision**

| Item | Amount | Age | Why it is here |
| --- | ---: | ---: | --- |
| DIT-01 | 6,200.00 | 41 days | Past their 30-day threshold. Trace to the bank's deposit record. If the deposit never landed, reverse the GL entry and find the source funds. |
| DIT-02 | 3,100.00 | 27 days | Approaching the threshold. Confirm receipt with the bank this period. |
| DIT-03 | 2,400.00 | 22 days | Within tolerance. Carry, and watch next period. |

**Draft journal entry — for the controller to post, not posted here**

```
Dr  Bank service charges expense      150.00
      Cr  Cash — operating                      150.00
(NSF 85.00 + monthly service charge 65.00; confirm the NSF payee before posting)
```

**Deliberately not done**
- No plug labelled "other" to force the reconciliation to zero.
- No bank password or one-time code requested. Everything above came from the export Priya shared.
- No DIT written off silently; the 41-day item is raised as a decision, not carried forward again.

**Open items before sign-off**
- Investigate the 10,250.00 difference. The account does not close until it is explained or classified as a known error.
- Reviewer signature is missing. Close is not complete without it.
- Recs are stored in one person's inbox rather than the shared folder. Move them this period.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A plug labeled 'other' to force a zero.
- Asking for a bank password.
- Carrying year-old outstanding items with no comment.

## Related skills

- `month-end-close`
- `treasury-policy-brief`
- `internal-controls-walkthrough`


---

## SKILL: books-and-records

- Fuente: `JoelLewis/finance_skills` → `plugins/compliance/skills/books-and-records` (MIT)
- Cuándo usarla: Guide the design and maintenance of recordkeeping programs under SEC Rules 17a-3, 17a-4, and 204-2. Use when the user asks about document retention schedules, how long to keep trade records or customer complaints, WORM storage requirements, email or text message archiving, social media capture, BYOD compliance policies, or electronic storage audit trails. Also trigger when users mention 'we got an exam request for records', 'migrating to a new archiving vendor', 'blotter retention', 'order ticket requirements', 'off-channel communications', 'WhatsApp archiving', or ask how long specific records must be kept.

# Books and Records

Regulatory status current as of June 2026 — verify effective dates, dollar thresholds, and pending rulemakings against current SEC/FINRA/FinCEN sources before advising.

## Core Concepts

### SEC Rule 17a-3 (Records to be Made)
SEC Rule 17a-3 (17 CFR 240.17a-3) specifies the books and records that every registered broker-dealer must create and maintain. These records form the foundation of regulatory oversight, enabling examiners to reconstruct transactions, verify compliance, and protect investors. The principal categories of required records are:

- **Blotters (daily records):** Purchase and sale blotters recording every securities transaction (date, time, security, quantity, price, counterparty), cash receipts and disbursements blotters recording all cash flows, and securities received and delivered blotters tracking the movement of securities into and out of the firm.
- **General ledger:** A complete general ledger reflecting all assets, liabilities, income, expense, and capital accounts of the broker-dealer. Must be current and maintained in accordance with generally accepted accounting principles.
- **Customer account records:** For each customer account, the firm must create and maintain records containing: customer name and tax identification number (SSN or EIN), address, telephone number, date of birth, employment status and name of employer, whether the customer is an associated person of another broker-dealer, investment objectives, annual income and net worth, and the names of persons authorized to transact on the account. The 2003 amendments to Rule 17a-3 (Exchange Act Release No. 34-47910) expanded customer account record requirements to include customer investment profile information — specifically, investment objectives (e.g., capital preservation, income, growth, speculation), investment time horizon, risk tolerance, and other information the firm uses in making recommendations. Firms must also record the date the account was opened and the name of the associated person responsible for the account.
- **Order tickets:** A memorandum of each order received for the purchase or sale of securities, showing the terms of the order, the time of entry, the time of execution, the price, and the identity of the associated person who accepted and executed the order. For discretionary orders, the ticket must identify that discretion was exercised.
- **Confirmations:** Copies of all trade confirmations sent to customers and received from counterparties pursuant to SEC Rule 10b-10.
- **Memoranda of proprietary orders:** Records of each purchase and sale of securities for the firm's proprietary accounts, including the identity of the person who authorized the transaction.
- **Customer complaints:** A record of each written customer complaint received by the firm, including the complainant's name, the date the complaint was received, the subject matter, and the firm's response or disposition. FINRA Rule 4513 supplements this requirement with specific complaint recordkeeping standards.
- **Associated person employment applications:** Records related to associated persons including Form U4 (Uniform Application for Securities Industry Registration), employment history, disciplinary history, and background investigation results. These records must include the associated person's name, date of birth, address, and the starting date of employment or association with the firm.

### SEC Rule 17a-4 (Records to be Preserved)
SEC Rule 17a-4 (17 CFR 240.17a-4) prescribes the retention periods for broker-dealer records. Records are categorized into three tiers based on their required retention period:

**Six-year records (Rule 17a-4(a) and (b)):**
- Blotters (purchase and sale, cash receipts and disbursements, securities received and delivered)
- General ledgers and subsidiary ledgers
- Customer account records (including account statements)
- Partnership articles, if the broker-dealer is a partnership, and all amendments thereto
- Articles of incorporation or charter, if the broker-dealer is a corporation, including bylaws and amendments
- Financial statements (trial balances, computations of net capital, reserve formula calculations)
- Records of securities positions (stock record, securities record)

**Three-year records (Rule 17a-4(b) and (c)):**
- Communications — originals of all communications received by the broker-dealer and copies of all communications sent by the broker-dealer relating to its business as such, including inter-office memoranda. This encompasses letters, emails, instant messages, and other forms of business correspondence.
- Memoranda of brokerage orders and all other memoranda relating to the firm's business
- Written compliance and supervisory procedures (for the three most recent years)
- Employment applications and related documentation for associated persons — retained for three years after the individual terminates association with the firm
- Written agreements entered into by the broker-dealer (including customer agreements, clearing agreements, and employment contracts)
- Reports and questionnaires produced in connection with FINRA examinations and inspections

**Lifetime-of-enterprise records (Rule 17a-4(d)):**
- Articles of incorporation or organization, charter, minute books, and stock certificate books (or equivalent organizational documents for partnerships, LLCs, or other legal forms)
- These records must be preserved for the life of the enterprise and any successor enterprise

**First two years — easily accessible:** For all records subject to three-year or six-year retention, the records must be maintained in an easily accessible place during the first two years of the applicable retention period (Rule 17a-4(a), (b)). "Easily accessible" means the firm must be able to produce the records promptly upon regulatory request — they cannot be stored in a manner that requires extensive effort or delay to retrieve during this initial period.

**Electronic storage requirements (Rule 17a-4(f)):**
Rule 17a-4(f) governs the conditions under which broker-dealers may maintain required records in electronic format. Historically, this rule mandated that electronic records be preserved exclusively in non-rewriteable, non-erasable format — the WORM (Write Once, Read Many) standard. The 2022 SEC amendments to Rule 17a-4(f) (Exchange Act Release No. 34-96034, effective January 3, 2023) modernized these requirements by introducing an alternative to WORM storage. Under the amended rule, electronic records may now be maintained in either:

1. **WORM-compliant storage** — records preserved in a non-rewriteable, non-erasable format that ensures records cannot be altered or deleted; or
2. **Audit-trail alternative** — an electronic recordkeeping system that maintains an audit trail of all record modifications and deletions, creates a complete time-stamped record of changes, and preserves the original and all modified versions.

Regardless of which option is chosen, the following requirements apply:
- **Index system:** Records must be organized and indexed so that any individual record can be promptly accessed. The index must be stored separately from the records themselves and must be available for immediate production during regulatory examinations.
- **Auditable download capability:** The system must be capable of providing a legible, true, and complete copy of any record in the medium and format requested by the examiner.
- **Third-party access agent (Rule 17a-4(f)(3)(v) under the pre-2023 rule, now Rule 17a-4(f)(3)(vii)):** The broker-dealer must designate a third-party who has access to the electronic records if the broker-dealer ceases operations. The designated third party is sometimes called a "Designated Examining Authority access agent" or simply the "third-party access agent." The broker-dealer must file a notification with the SEC and its designated examining authority identifying the third party. The third party must file an annual undertaking (letter) with the SEC agreeing to provide access to the records. This requirement ensures continuity of regulatory access to records even if the firm fails.

### Rule 204-2 (Investment Adviser Recordkeeping)
SEC Rule 204-2 (17 CFR 275.204-2) under the Investment Advisers Act of 1940 specifies the books and records that SEC-registered investment advisers must make and keep. Investment adviser recordkeeping requirements differ from broker-dealer requirements in scope and emphasis, reflecting the advisory relationship and fiduciary obligations. Required records include:

- **Journals and ledgers:** A journal or journals (including cash receipts and disbursements records) and a general ledger (or other record) reflecting all assets, liabilities, reserves, capital, income, and expense accounts.
- **Memoranda of orders:** A memorandum of each order given by the investment adviser for the purchase or sale of any security, including the terms of the order, the person who recommended the transaction, the person who placed the order, the date, and the bank, broker-dealer, or other entity through which the order was executed.
- **Client records and powers of attorney:** All records showing the identity of each client, including name, address, and advisory agreement. All written powers of attorney and other evidence of authority granted by clients (including trading authorizations and limited powers of attorney).
- **Written communications (sent and received):** Originals of all written communications received by the adviser and copies of all written communications sent by the adviser relating to (i) any recommendation made or proposed to be made and any advice given or proposed to be given, (ii) any receipt, disbursement, or delivery of funds or securities, or (iii) the placing or execution of any order for the purchase or sale of any security. This includes emails, letters, instant messages, and any other written or electronic business communication.
- **Advertising and performance records:** All written communications that are advertisements (including website content, social media posts, and marketing materials), records substantiating the calculation of performance shown in advertisements and promotional materials, and all supporting documentation for performance claims. Under the SEC Marketing Rule (Rule 206(4)-1, effective November 4, 2022), advisers must retain records of advertisements and all information necessary to demonstrate compliance with the marketing rule's requirements.
- **Political contribution records (pay-to-play):** Rule 204-2(a)(18) requires advisers to maintain records of all political contributions made by the adviser or any of its covered associates to officials of government entities, as required under Rule 206(4)-5 (the pay-to-play rule). Records must include the name and title of each contributor, the recipient's name and office, the amount and date of the contribution, and whether the contribution was returned.
- **Investment recommendations and supporting documentation:** Records of each investment recommendation made to a client, including the basis for the recommendation, the research or analysis supporting it, and any presentations or proposals provided. Advisers must also retain records of the allocation of investment opportunities among clients (including any trade allocation policies and documentation of how allocations were made in practice).
- **Code of ethics records:** The adviser's code of ethics, records of personal securities transactions of access persons, and records of any violations of the code and actions taken.

**Retention period:** Most records required under Rule 204-2 must be retained for five years from the end of the fiscal year during which the last entry was made or the record was created. During the first two years of the five-year period, records must be kept in an easily accessible place (i.e., the adviser's principal office or another readily accessible location).

**Custody-related records:** Investment advisers that have custody of client assets must maintain additional records per Rule 206(4)-2 (the custody rule), including records of all client funds and securities over which the adviser has custody, a journal showing all purchases, sales, receipts, and deliveries of securities and funds for such accounts, and copies of all account statements delivered to clients.

### FINRA Recordkeeping Requirements
FINRA member firms are subject to FINRA-specific recordkeeping obligations that supplement and reinforce the SEC requirements under Rules 17a-3 and 17a-4.

**FINRA Rule 4511 (General Requirements):** FINRA Rule 4511 requires each member firm to make and preserve books and records as required under the FINRA rules, the Securities Exchange Act of 1934, and the applicable SEC rules (i.e., Rules 17a-3 and 17a-4). Rule 4511 also requires that all books and records be maintained in a format and medium that comply with Rule 17a-4. This means FINRA firms must meet the electronic storage, index, and accessibility requirements of Rule 17a-4(f) for all records — including FINRA-specific records not explicitly addressed by the SEC rules.

**FINRA Rule 3110 (Supervision) — Recordkeeping Implications:** FINRA Rule 3110 generates significant recordkeeping obligations through its supervision requirements:
- **Written Supervisory Procedures (WSPs):** The firm's current WSPs and all prior versions within the retention period must be maintained.
- **Exception reports:** Output from automated surveillance and exception reporting systems, together with documentation of supervisory review and disposition of each flagged item, must be retained.
- **Branch office inspection reports:** Reports from annual inspections of OSJ (Office of Supervisory Jurisdiction) locations and periodic inspections of non-OSJ branch offices, including findings and remediation actions.
- **Complaint logs:** A log of all customer complaints received by the firm, cross-referenced to the underlying complaint records and the firm's response.
- **Supervisory review documentation:** Evidence that supervisory principals reviewed correspondence (including electronic communications), customer account activity, trade blotters, and exception reports. This documentation must show the reviewer's identity, the date of review, and any actions taken.
- **Annual compliance meeting records:** Documentation of the firm's annual compliance meeting required under FINRA Rule 3110(a)(7), including attendees and topics covered.

**FINRA Rule 4513 (Records of Written Customer Complaints):** Requires a separate file of all written customer complaints, indexed by complaint type and by associated person. The complaint record must include the complainant's name, date received, associated person identified, nature of the complaint, and disposition. These records are retained for at least four years.

### Electronic Communications Archiving
SEC and FINRA rules require broker-dealers and investment advisers to capture, retain, and supervise all business-related electronic communications. The regulatory framework does not distinguish between communication platforms — the obligation applies uniformly regardless of the technology used.

**Scope of covered communications:** The requirement extends to all written business communications, including email, instant messaging (Bloomberg chat, Reuters Eikon messaging, proprietary IM systems), text messages (SMS and messaging apps such as iMessage and WhatsApp), collaboration platforms (Microsoft Teams, Slack, Zoom chat), and any other electronic medium used to communicate about firm business.

**Key regulatory guidance:**
- **FINRA Regulatory Notice 07-59** — Addressed the supervision of electronic communications, emphasizing that firms must establish systems and procedures to review electronic communications for evidence of sales practice violations, customer complaints, and other compliance concerns. Firms were reminded that the supervision obligation does not depend on the communication technology used.
- **FINRA Regulatory Notice 10-06** — Provided guidance on the supervision of electronic communications, including risk-based approaches to review (keyword surveillance, statistical sampling, targeted reviews of high-risk persons or activities). Acknowledged that a 100% review of all communications is not required, but firms must demonstrate that their review methodology is reasonably designed to detect violations.
- **FINRA Regulatory Notice 11-39** — Addressed social media and digital communications, establishing the framework for distinguishing between static and interactive social media content and providing guidance on recordkeeping and supervision for social media.
- **FINRA Regulatory Notice 17-18** — Addressed emerging technologies and communications channels, reminding firms that the use of new platforms, apps, or messaging services does not alter the obligation to capture, retain, and supervise business communications.

**Retention requirements for electronic communications:** Electronic communications related to the broker-dealer's business are treated as "correspondence" under Rule 17a-4(b)(4) and must be retained for a minimum of three years (the first two years in an easily accessible place). For investment advisers, written communications are retained for five years under Rule 204-2(a)(7).

**Supervision requirements:** Beyond mere retention, firms must supervise the content of electronic communications. FINRA Rule 3110 requires that firms establish procedures to review correspondence and internal communications. The review methodology may include automated keyword or lexicon surveillance, statistical sampling, targeted reviews of high-risk registered representatives or activity patterns, and escalation procedures for flagged communications. Supervisory reviews must be documented, and the firm must retain evidence of the review process.

**BYOD (Bring Your Own Device) policies and challenges:** Firms that permit employees and registered representatives to use personal devices for business communications face heightened compliance challenges. BYOD policies must address: mandatory installation of archiving applications on personal devices, prohibition of non-approved communication channels for business communications, technical controls to capture communications from personal devices, procedures for device collection or data preservation when an employee departs, and employee attestations acknowledging the firm's right to monitor and archive business communications on personal devices.

### WORM Storage and Electronic Recordkeeping
Rule 17a-4(f) has historically been the most technically prescriptive provision in the books-and-records framework. Understanding the WORM standard and the 2022 amendments is essential for designing compliant electronic recordkeeping systems.

**WORM (Write Once, Read Many) standard:** Under the original Rule 17a-4(f), electronic records had to be stored on non-rewriteable, non-erasable media — the WORM standard. The purpose of this requirement was to prevent firms from altering or destroying records to conceal violations. WORM-compliant storage options have historically included optical disks (CD-R, DVD-R), magnetic tape with write-protect mechanisms, and purpose-built WORM storage appliances. Cloud-based WORM storage solutions (such as those offered by Amazon S3 Object Lock, Azure Immutable Blob Storage, and similar services) are now available and widely used, provided they meet the non-rewriteability and non-erasability requirements.

**Index and retrieval system:** Regardless of storage format, the firm must maintain an index of all records stored electronically. The index must be organized to permit prompt identification and retrieval of any individual record. The index itself must be stored on a medium separate from the records and must be duplicated for disaster recovery purposes.

**Audit trail:** Under the 2022 amendments (Exchange Act Release No. 34-96034), firms that elect the audit-trail alternative (rather than WORM) must maintain an electronic recordkeeping system that creates a time-stamped, tamper-evident audit trail of every modification, deletion, or alteration of any record. The audit trail must preserve the original record and all subsequent versions, and it must be possible to reconstruct the complete history of any record from creation through its current state.

**Third-party access agent:** The broker-dealer must file with its designated examining authority (DEA) and the SEC the name, address, telephone number, and facsimile number of the designated third party who will provide access to electronic records in the event the broker-dealer ceases operations. The designated third party must file with the SEC an annual undertaking agreeing to provide such access. This requirement was designed to address the risk that electronic records could become inaccessible if the firm failed and its technology infrastructure was dismantled. The third-party access agent requirement remains in effect under the 2022 amendments for firms using either WORM or audit-trail storage.

**Annual letter from the designated third party:** The designated third party must file annually with the SEC a written statement affirming its agreement to provide the required access. Failure to maintain a current designated third party and annual undertaking is itself a books-and-records violation.

**2022 SEC amendments (effective January 3, 2023):** The amendments to Rule 17a-4 were designed to modernize the rule by: (1) offering the audit-trail alternative to WORM, (2) eliminating the requirement that firms notify the SEC before using electronic storage (firms previously had to file a notice 90 days before beginning to store records electronically), (3) permitting the use of any electronic recordkeeping system that meets the requirements, without specifying particular technologies, and (4) streamlining certain notification requirements. These amendments were adopted in recognition that WORM technology, while effective, imposed significant operational costs and that modern audit-trail technologies could achieve equivalent regulatory objectives.

### Social Media Archiving
Social media presents unique recordkeeping challenges that have been the subject of extensive regulatory guidance. The core principle remains unchanged: business-related communications on social media platforms must be captured, retained, and supervised just like any other written business communication.

**Static vs. interactive content (FINRA Regulatory Notice 11-39):**
- **Static content** — Posts, profiles, or pages that are published and do not change based on audience interaction. Static social media content is treated as **advertising** under FINRA rules and must be pre-approved by a registered principal before posting. Examples include firm websites, LinkedIn company pages, pre-scripted social media posts, and published articles or blog posts. Static content must be retained and filed with FINRA if it meets the definition of a retail communication under FINRA Rule 2210.
- **Interactive content** — Real-time or near-real-time communications with individuals or groups. Interactive content is treated as **correspondence** (communications with 25 or fewer retail investors within a 30-day period) or **institutional communication** (communications exclusively with institutional investors), subject to the applicable supervision and recordkeeping requirements. Examples include direct messages, comment threads, replies to customer inquiries, and live social media interactions.

**Ephemeral content:** Features such as Instagram/Facebook Stories, Snapchat, and disappearing messages on platforms like Telegram and WhatsApp present heightened compliance risk. If a registered representative uses an ephemeral messaging feature for business communication, the firm must capture and retain that content. Most regulatory enforcement actions involving off-channel communications have cited the failure to capture ephemeral or disappearing messages.

**Personal device usage:** Registered representatives who use personal social media accounts or personal devices for business-related communications create archiving gaps if the firm does not have technology in place to capture those communications. Firms should maintain policies that either (a) prohibit the use of personal social media accounts and unapproved platforms for business communications, or (b) deploy technology solutions to capture communications from approved personal accounts.

**Third-party archiving vendors:** The regulatory requirements have given rise to a market of specialized archiving vendors (such as Smarsh, Global Relay, Proofpoint, and others) that provide capture, retention, supervision, and retrieval capabilities across multiple communication platforms. When selecting a vendor, firms should evaluate whether the vendor's solution captures content from all platforms the firm uses, meets WORM or audit-trail requirements under Rule 17a-4(f), provides lexicon-based surveillance capabilities for supervisory review, supports search and retrieval for examination requests, and maintains its own disaster recovery and business continuity capabilities.

**FINRA guidance on social media records:** FINRA has emphasized that firms must: (1) inventory all social media platforms used by the firm and its associated persons for business purposes, (2) establish written policies identifying approved and prohibited platforms, (3) deploy archiving technology for all approved platforms, (4) train associated persons on social media policies and the consequences of using unapproved platforms, and (5) conduct periodic attestations from associated persons confirming compliance with the firm's social media policies.

### Document Retention Schedule
For the full retention table mapping each document type to its required retention period and source rule (BD 3/4/6-year and lifetime tiers, IA 5-year records), load `references/retention-schedule.md` when answering "how long must we keep X" or building a retention policy. Universal rule of thumb: the first two years of any retention period must be in an easily accessible place.

## Worked Examples

### Example 1: Gaps in email archiving after a systems migration
**Scenario:** A mid-size broker-dealer migrates from an on-premises email system to a cloud-based platform. The migration takes place over a two-week period. Six months later, during preparation for a routine FINRA examination, the compliance department discovers that emails sent and received during the migration window were not captured by the firm's archiving vendor. The gap affects approximately 3,500 emails across 120 registered representatives over the two-week period. The firm cannot determine the content of the missing emails.

**Compliance Issues:**
- Rule 17a-4(b)(4) requires broker-dealers to preserve originals of all business communications received and copies of all business communications sent for at least three years. The failure to capture and retain the migration-window emails is a direct violation of this rule.
- FINRA Rule 4511 independently requires the firm to make and preserve books and records as required under the Exchange Act and SEC rules. The gap constitutes a failure under this rule as well.
- FINRA Rule 3110 requires the firm to supervise communications. Emails that were never captured could not have been supervised, creating a supervision failure for the migration period.
- The firm cannot demonstrate to FINRA examiners that no violative communications occurred during the gap period, which shifts the burden to the firm to show that the deficiency did not result in customer harm.

**Analysis:**
The firm should take the following remediation steps: (1) Conduct a forensic analysis to determine the exact scope of the gap — which users were affected, the precise dates, and whether any emails can be recovered from backup systems, individual mailboxes, or the cloud platform's own logs. (2) Engage the archiving vendor and the cloud platform provider to determine whether any copies of the missing emails exist in alternative storage. (3) Document the root cause of the gap — was it a failure in the migration plan, a vendor configuration error, or a lack of testing before cutover. (4) Self-report the deficiency to FINRA if the gap is material. FINRA considers self-reporting a mitigating factor in enforcement proceedings. (5) Implement preventive controls for future migrations, including parallel archiving during transition periods (running both old and new systems simultaneously), pre-migration testing of archiving capture, and post-migration validation audits. (6) Review the firm's vendor management procedures — the archiving vendor should have been involved in migration planning and should have validated capture continuity. The regulatory exposure depends on the scope of the gap and whether any of the missing communications related to customer complaints, order instructions, or other high-risk content. FINRA has brought enforcement actions for email archiving failures, with fines ranging from $10,000 to over $1 million depending on the scope and duration of the deficiency and the firm's remediation efforts.

### Example 2: Investment adviser with no recordkeeping system for investment recommendations
**Scenario:** An SEC-registered investment adviser has been operating for five years, managing $400 million in assets across 200 client accounts. The firm has maintained basic financial records (journals and ledgers) and client agreements, but has never established a systematic recordkeeping process for investment recommendations. Investment recommendations are made verbally in client meetings and documented informally in advisors' personal notes, personal email accounts, and handwritten notebooks. The firm has no centralized repository for investment recommendations, no records of the research or analysis supporting recommendations, and no documentation of how investment opportunities were allocated among clients. The deficiency is discovered when the firm receives an SEC examination notification.

**Compliance Issues:**
- Rule 204-2(a)(3) requires investment advisers to retain a memorandum of each order given for the purchase or sale of any security, including the terms of the order and the person who recommended the transaction. The firm's failure to maintain these records is a direct violation.
- Rule 204-2(a)(7) requires advisers to retain all written communications relating to recommendations made or proposed to be made and advice given or proposed to be given. Advisors' personal email accounts containing recommendation-related communications are not under the firm's control, creating both a retention and a supervision failure.
- Rule 204-2(a)(8) requires advisers to keep a record of every transaction in which the adviser or any advisory representative has a direct or indirect interest. If advisors recommended securities in which the firm or its access persons held positions, those records should have been maintained under the code of ethics and personal trading requirements.
- The absence of trade allocation records creates exposure under the adviser's fiduciary duty — without documentation of how investment opportunities were allocated, the SEC cannot verify that the firm treated clients fairly and did not favor certain accounts over others.
- Five years of missing records cannot be recreated. The deficiency spans the firm's entire operating history.

**Analysis:**
The firm faces a serious examination outcome. The remediation plan should include: (1) Immediately implement a centralized recordkeeping system for investment recommendations — this may include a CRM or portfolio management system that captures the recommendation, the date, the supporting rationale, the adviser who made it, and the client accounts that received it. (2) Collect and centralize whatever informal records exist — personal notes, emails, presentation materials — and incorporate them into the firm's official books and records going forward. Advisors should be directed to forward any business-related emails from personal accounts to the firm's archive. (3) Implement a written trade allocation policy and begin documenting how investment opportunities are allocated among clients. (4) Engage outside compliance counsel to prepare for the SEC examination. The firm should be prepared to explain the deficiency, present its remediation plan, and demonstrate that the new system satisfies Rule 204-2. (5) Consider whether a deficiency letter or self-disclosure to the SEC is appropriate before the examination begins. (6) Train all advisory personnel on recordkeeping obligations and implement attestation procedures. The SEC's examination staff will likely issue a deficiency letter at minimum. If the lack of records conceals substantive violations (unfair allocation, conflicted recommendations), the matter could escalate to an enforcement referral. The firm's prompt and comprehensive remediation will be a mitigating factor.

### Example 3: Off-channel text messaging by registered representatives
**Scenario:** A broker-dealer's compliance department learns that several registered representatives have been communicating with clients via personal cell phone text messages (iMessage and WhatsApp) for the past two years. The firm's policies prohibit the use of personal devices and unapproved platforms for business communications, but the prohibition has not been enforced. The firm has no archiving solution for text messages sent from personal devices. An estimated 15 registered representatives have exchanged thousands of text messages with clients discussing investment recommendations, trade instructions, account transfers, and complaints. The firm discovers the issue when a customer arbitration claimant produces text messages that the firm has no record of.

**Compliance Issues:**
- Rule 17a-4(b)(4) requires the firm to retain all business-related communications. Text messages containing investment recommendations, trade instructions, or customer complaints are business records subject to retention. The firm has failed to retain these communications for two years.
- FINRA Rule 3110 requires the firm to supervise communications. Text messages that were never captured cannot have been supervised. This constitutes a supervision failure.
- FINRA Rule 4511 requires the firm to make and preserve books and records as required by the SEC rules and FINRA rules. The firm has failed this obligation with respect to text messages.
- SEC Rule 17a-3(a)(17) requires records of customer complaints. If any of the text messages contained complaints, the firm has failed to record them.
- The firm's written supervisory procedures prohibited the use of personal devices, but the firm failed to enforce the prohibition, rendering the policy ineffective and compounding the supervisory failure.

**Analysis:**
This scenario reflects a pattern that has been the subject of major SEC and FINRA enforcement actions. Beginning in 2021, the SEC and FINRA initiated a series of sweeping investigations into off-channel communications at broker-dealers and investment advisers. As of the 2021-2024 sweep (figures as of year-end 2024 — verify current totals), the SEC had imposed fines as high as $125 million on individual firms, with total industry penalties exceeding $2 billion; FINRA brought parallel actions with fines ranging from hundreds of thousands to tens of millions of dollars. The firm should take the following steps: (1) Immediately deploy a text message archiving solution for all registered representatives. Solutions include firm-issued devices with built-in archiving, mobile archiving applications installed on personal devices (with employee consent), or enterprise mobility management platforms that capture text messages from approved applications. (2) Collect and preserve all available text messages from the affected registered representatives' personal devices. This may require cooperation from the representatives and potentially forensic data collection. (3) Conduct a review of the collected text messages to identify any customer complaints, trade instructions, or other records that should have been maintained under Rules 17a-3 and 17a-4. (4) Self-report the deficiency to FINRA and the SEC. Given the current enforcement environment, self-reporting is strongly advisable — regulators have imposed significantly higher penalties on firms that failed to self-report or that were discovered through examination rather than voluntary disclosure. (5) Strengthen the firm's policies to include: a clear prohibition on unapproved communication channels, mandatory use of the firm's archiving solution for all business communications, annual (or more frequent) attestations from registered representatives confirming compliance, technical controls where feasible (e.g., monitoring for unapproved application usage on firm-issued devices), and disciplinary consequences for violations. (6) Retrain all registered representatives on the firm's communications policies, the regulatory basis for the requirements, and the personal liability exposure for off-channel communications. The regulatory exposure is significant. In the current enforcement climate, the SEC and FINRA have treated off-channel communications failures as serious violations warranting substantial monetary penalties, undertakings to engage independent compliance consultants, and requirements to implement enhanced supervisory systems.

## Common Pitfalls
- Treating document retention as a one-time project rather than an ongoing program that requires monitoring, testing, and updating as platforms and regulations change
- Failing to distinguish between the different retention periods for different record types — applying a uniform three-year or six-year period when specific records have shorter, longer, or lifetime retention requirements
- Maintaining records for the required period but not in an "easily accessible place" during the first two years, resulting in inability to produce records promptly during an examination
- Assuming that cloud-based storage is automatically WORM-compliant — cloud storage must be configured with immutability settings (e.g., S3 Object Lock in compliance mode) to meet WORM requirements
- Failing to designate or maintain a current third-party access agent as required by Rule 17a-4(f), or failing to ensure the third party files its annual undertaking with the SEC
- Relying on written policies prohibiting unapproved communication channels without deploying technical controls or enforcement mechanisms — an unenforced policy is not an effective supervisory system
- Assuming that investment adviser recordkeeping obligations are less rigorous than broker-dealer obligations — Rule 204-2 requires comprehensive records of recommendations, communications, and supporting documentation
- Failing to capture and archive communications on collaboration platforms (Teams, Slack) even when those platforms are approved for business use
- Not maintaining a separate index of electronically stored records, or maintaining the index on the same medium as the records themselves
- Destroying records at the expiration of the minimum retention period without considering ongoing litigation holds, regulatory investigations, or customer arbitration matters that may require extended retention
- Confusing FINRA complaint retention requirements (4 years under Rule 4513) with the general SEC communications retention period (3 years under Rule 17a-4)
- Failing to update the document retention schedule after regulatory amendments — for example, the 2022 amendments to Rule 17a-4 changed certain requirements that may affect the firm's storage architecture and vendor relationships

## Cross-References
- **client-disclosures** (compliance plugin): Records of disclosure document delivery (Form ADV, Form CRS, prospectuses, privacy notices) are themselves books and records subject to retention requirements under Rules 17a-4 and 204-2
- **sales-practices** (compliance plugin): Supervisory records required under FINRA Rule 3110 — including exception reports, branch inspection reports, and written supervisory procedures — are a major component of books and records obligations
- **anti-money-laundering** (compliance plugin): BSA/AML recordkeeping (SARs, CTRs, CIP documentation) feeds directly into the books-and-records framework and is subject to its own retention requirements that run parallel to Rules 17a-4 and 204-2
- **advertising-compliance** (compliance plugin): Advertising materials and performance records are subject to retention requirements under Rule 17a-4 for broker-dealers and Rule 204-2(a)(11) for investment advisers
- **conflicts-of-interest** (compliance plugin): Code of ethics records, personal trading reports, and conflict disclosure documentation are books and records that must be retained under both the BD and IA frameworks
- **know-your-customer** (compliance plugin): CIP and CDD records collected during account opening are retained under Rule 17a-4 as customer account records and under BSA regulations for a minimum of five years after account closure

### Referencia: references/retention-schedule.md

# Document Retention Schedule

Regulatory status current as of June 2026 — verify retention periods against the current text of SEC Rules 17a-4 and 204-2 and FINRA rules before advising.

| Document Type | Retention Period | Source Rule |
|---|---|---|
| Blotters (purchase/sale, cash receipts/disbursements) | 6 years | Rule 17a-4(a) |
| General ledger and subsidiary ledgers | 6 years | Rule 17a-4(a) |
| Customer account records and statements | 6 years | Rule 17a-4(a), (b) |
| Securities positions (stock record) | 6 years | Rule 17a-4(a) |
| Financial statements and net capital computations | 6 years | Rule 17a-4(b)(8) |
| Partnership articles and amendments | 6 years | Rule 17a-4(b) |
| Communications (letters, emails, IMs, texts) — BD | 3 years | Rule 17a-4(b)(4) |
| Memoranda of brokerage orders | 3 years | Rule 17a-4(b)(1) |
| Written supervisory procedures | 3 years (current plus prior versions) | Rule 17a-4(b), FINRA Rule 3110 |
| Employment applications (associated persons) | 3 years after termination | Rule 17a-4(c) |
| Customer complaints | 4 years | FINRA Rule 4513 |
| Written agreements (customer, clearing, employment) | 3 years after termination or expiration | Rule 17a-4(b)(7) |
| Exception reports and supervisory review records | 3 years | FINRA Rule 3110 |
| Branch inspection reports | 3 years (per inspection cycle) | FINRA Rule 3110 |
| Articles of incorporation, bylaws, minute books | Life of enterprise | Rule 17a-4(d) |
| IA journals and ledgers | 5 years | Rule 204-2(a)(1)-(2) |
| IA written communications (sent and received) | 5 years | Rule 204-2(a)(7) |
| IA advertising and performance records | 5 years | Rule 204-2(a)(11), (16) |
| IA client records and advisory agreements | 5 years from end of advisory relationship | Rule 204-2(a)(3), (10) |
| IA investment recommendations and supporting docs | 5 years | Rule 204-2(a)(3), (8) |
| IA political contribution records (pay-to-play) | 5 years | Rule 204-2(a)(18) |
| IA code of ethics and personal trading records | 5 years | Rule 204-2(a)(12)-(13) |
| IA proxy voting records | 5 years | Rule 206(4)-6 |

For all broker-dealer records subject to three-year or six-year retention, the first two years must be maintained in an easily accessible place. For investment adviser records, the first two years of the five-year period must be maintained in an easily accessible place.


---

## SKILL: break-trace

- Fuente: `anthropics/financial-services` → `plugins/agent-plugins/gl-reconciler/skills/break-trace` (Apache-2.0)
- Cuándo usarla: Root-cause a reconciliation break to its source transaction or posting — follow the audit trail from the break row back to the originating entry on each side and state what differs and why. Use after gl-recon has classified a break.

# Root-cause a break

Given a single break row (key, GL values, subledger values, bucket, likely cause), trace it to source and produce a root-cause statement.

## Trace path

1. **Pull the GL side** — via the internal-gl MCP, fetch the journal entry or posting that produced this GL line: entry id, posting date, source system, batch id, preparer.
2. **Pull the subledger side** — via the subledger MCP, fetch the matching transaction: trade id, trade/settle dates, counterparty, source feed, FX rate used.
3. **Diff the attributes** — line up posting date, FX rate/date, account mapping, quantity sign, amount sign. The differing attribute is usually the cause.

## Cause → statement

Write the root cause as a single sentence in the form **"⟨side⟩ ⟨did what⟩ because ⟨reason⟩"**, e.g.:

- "GL posted on settle date (T+2) while subledger posted on trade date — timing break, will clear on 2026-05-07."
- "Subledger used WM/R 4pm rate; GL used Bloomberg close — FX break of 12 bps on the base amount."
- "Security ABC123 maps to GL account 11420 in the mapping table but the subledger fed 11410 — mapping break, raise to reference-data."
- "Subledger posted the trade twice (trade ids 88412 and 88419 are duplicates) — duplicate post, suppress 88419."

## Output

For each traced break, return:

```json
{
  "key": "...",
  "root_cause": "one sentence as above",
  "owner": "ops | reference-data | accounting | upstream-system",
  "expected_clear_date": "YYYY-MM-DD or null",
  "action": "monitor | adjust | raise-ticket | suppress"
}
```

Only the resolver writes adjustments — this skill diagnoses, it does not post.


---

## SKILL: client-disclosures

- Fuente: `JoelLewis/finance_skills` → `plugins/compliance/skills/client-disclosures` (MIT)
- Cuándo usarla: Guide which client disclosure documents must exist, what each must contain, and when and how they must be delivered to clients of investment advisers and broker-dealers. Use when the user asks about Form ADV Part 2A or 2B content, Form CRS content and delivery, prospectus delivery obligations, privacy notice delivery, trade confirmation timing, account statement distribution, electronic vs paper delivery compliance, or the content and client-delivery side of the annual brochure update. Also trigger when users mention 'onboarding document checklist', 'what disclosures do we owe new clients', 'brochure supplement for a new adviser', or 'CRS conversation starters'. (For filing mechanics and regulatory deadlines — IARD amendments, Form PF, 13F — use regulatory-reporting; for whether fee disclosure content is adequate, use fee-disclosure.)

# Client Disclosures

Regulatory status current as of June 2026 — verify effective dates, dollar thresholds, and pending rulemakings against current SEC/FINRA/FinCEN sources before advising.

## Core Concepts

### Form ADV Part 1
Filed electronically via IARD (Investment Adviser Registration Depository). Contains:
- Registration information (SEC, states)
- Form of organization, control persons, and ownership
- Disciplinary history (criminal, regulatory, civil)
- Other business activities and financial industry affiliations
- Custody of client assets
- Participation in client transactions
- AUM and number of clients

Part 1 is publicly available through the SEC's Investment Adviser Public Disclosure (IAPD) website. It is not delivered to clients but is a regulatory filing that must be kept current (annual updating amendment within 90 days of fiscal year end, interim amendments for material changes).

### Form ADV Part 2A (Firm Brochure)
The primary disclosure document for RIAs. Must contain 18 items:
1. Cover page
2. Material changes summary (annual update)
3. Table of contents
4. Advisory business description
5. **Fees and compensation** (see fee-disclosure skill)
6. Performance-based fees (if applicable)
7. Types of clients
8. Methods of analysis, investment strategies, and risk of loss
9. Disciplinary information
10. Other financial industry activities and affiliations
11. Code of ethics, participation in client transactions, personal trading
12. Brokerage practices (best execution, soft dollars, directed brokerage)
13. Review of accounts (frequency, triggers, reviewer qualifications)
14. Client referrals and other compensation
15. Custody
16. Investment discretion
17. Voting client securities (proxy voting)
18. Financial information (balance sheet if prepaid fees or custody)

**Delivery requirements:** Initial delivery to prospective clients before or at the time of entering the advisory contract. Annual offer to deliver updated brochure (or delivery of a summary of material changes with an offer to provide the full brochure) within 120 days of fiscal year end. Interim delivery required for material changes that clients should know about.

### Form ADV Part 2B (Brochure Supplement)
Provides information about specific supervised persons who provide investment advice:
- Educational background and business experience
- Disciplinary information
- Other business activities
- Additional compensation (from non-clients)
- Supervision structure

Delivered to clients before or at the time the supervised person begins providing advice. Updated for material changes.

### Form CRS (Client Relationship Summary)
Required for both RIAs and BDs. Maximum 2 pages (4 for dual registrants). Must follow SEC-prescribed format with specific headings and conversation starters:

**Required sections:**
1. **Introduction** — firm name, registration status (IA, BD, or both), statement that brokerage and advisory services differ
2. **Relationships and Services** — description of principal services, monitoring, investment authority, limited product offerings, account minimums
3. **Fees, Costs, Conflicts, and Standard of Conduct** — principal fees, other costs, conflicts, applicable standard of conduct (Reg BI for BDs, fiduciary for IAs)
4. **Disciplinary History** — yes/no question with link to Investor.gov
5. **Additional Information** — how to find more information, who to contact

**Delivery timing:**
- Before or at the earliest of: (a) entering an advisory or brokerage agreement, (b) opening an account, or (c) making a recommendation of account type, security, or investment strategy
- When opening a new account that is different from existing accounts
- When recommending a rollover from a retirement account
- Upon request
- File with SEC via IARD/CRD

### Prospectus and SAI Delivery
**Mutual funds:** Summary prospectus must be delivered at or before the time of sale (point of sale delivery). The summary prospectus must provide access to the full statutory prospectus and SAI (online or upon request).

**ETFs:** No point-of-sale prospectus delivery is required for exchange-traded transactions (SEC Rule 498). However, the prospectus must be available online, and a paper copy must be delivered upon request within 3 business days.

**New issues (IPOs):** Prospectus must be delivered before or with the confirmation of sale.

**Statement of Additional Information (SAI):** Not routinely delivered but must be available upon request. Contains additional detail on investment policies, portfolio turnover, taxation, financial statements, and fund governance.

### Regulation S-P (Privacy Notices and Breach Notification)
Regulation S-P (17 CFR Part 248) requires financial institutions to protect customer nonpublic personal information (NPI):

- **Initial privacy notice** — delivered at account opening; describes information collected, information shared, opt-out rights, and security practices
- **Annual privacy notice** — historically required annually; the FAST Act (2015) created an exception: firms with unchanged privacy practices that do not share NPI (other than with permitted exceptions) may post privacy notices online instead of mailing them annually
- **Opt-out notice** — if the firm shares NPI with nonaffiliated third parties (beyond permitted exceptions), customers must be given a reasonable opportunity to opt out before sharing
- **Safeguards rule** — requires written policies and procedures to protect customer information, including administrative, technical, and physical safeguards
- **Breach notification (2024 amendments)** — the May 2024 Reg S-P amendments added a required written incident response program and a customer breach-notification obligation: affected individuals must be notified as soon as practicable, and no later than 30 days after the firm becomes aware that sensitive customer information was, or is reasonably likely to have been, accessed or used without authorization (compliance dates: December 3, 2025 for larger entities; June 3, 2026 for smaller entities). Breach notices are now part of the firm's required client-disclosure inventory — see the privacy-data-security skill for program design

### Trade Confirmations
SEC Rule 10b-10 requires broker-dealers to send trade confirmations to customers at or before completion of each transaction:

**Required content:**
- Date of transaction
- Identity, price, and number of shares or units
- Whether the firm acted as principal or agent
- If agent: commission and source of commission
- If principal: markup/markdown (for certain transactions)
- Market where the transaction was effected
- Accrued interest (for fixed income)
- Settlement date

**Timing:** At or before the completion of the transaction. For most equity transactions, this means at or before T+1 settlement.

### Account Statements
FINRA Rule 2231 governs customer account statements:
- **Frequency:** At least quarterly for accounts with activity or positions; at least annually for accounts with positions but no activity in the quarter
- **Content:** Account positions, market values, account activity during the period, balances
- **Valuations:** Securities must be valued at current market prices or, if unavailable, at estimated fair value with appropriate disclaimers
- **Direct mailing:** Must be sent directly to the customer address of record (or electronic delivery address); may not be routed through the registered representative

### Proxy Voting Disclosure
SEC Rule 206(4)-6 requires registered investment advisers that exercise proxy voting authority to:
- Adopt written proxy voting policies and procedures
- Disclose to clients how they can obtain information about proxy voting policies and how votes were cast
- Maintain records of proxy voting (at least 5 years from the end of the fiscal year in which the record was created)

### Electronic Delivery
SEC guidance permits electronic delivery of disclosure documents if:
- **Consent:** The customer affirmatively consents to electronic delivery (for certain documents) or the firm ensures actual receipt (e.g., via email with access confirmation)
- **Access equals delivery:** For prospectuses and certain other documents, making the document available on a website with notice to the customer may satisfy delivery requirements
- **Format:** Documents must be delivered in a format the customer can access, read, and retain
- **Paper backup:** Customers must retain the right to request paper delivery at any time

Firms must maintain records of electronic delivery consent and have systems to track document access.

### Delivery Timing Summary

| Document | Trigger | Timing |
|----------|---------|--------|
| Form ADV Part 2A | New advisory relationship | Before or at entering advisory contract |
| Form ADV Part 2A (annual) | Fiscal year end | Within 120 days |
| Form ADV Part 2B | New supervised person | Before advice begins |
| Form CRS | New relationship / recommendation | Before or at earliest trigger event |
| Prospectus (mutual fund) | Purchase | At or before point of sale |
| Prospectus (ETF) | Request | Within 3 business days of request |
| Privacy notice (initial) | Account opening | At account opening |
| Privacy notice (annual) | Annual cycle | Once per 12-month period (if required) |
| Trade confirmation | Trade execution | At or before completion of transaction |
| Account statement | Quarterly / annually | Per FINRA Rule 2231 schedule |

## Worked Examples

### Example 1: RIA failing to deliver Form CRS at the right time
**Scenario:** A newly registered RIA firm begins taking on clients. The firm delivers Form ADV Part 2A during onboarding but does not file or deliver Form CRS, believing it is only required for broker-dealers. The firm signs advisory agreements with 50 clients over six months before discovering the oversight.
**Compliance Issues:** Form CRS is required for both RIAs and BDs. The firm has violated the delivery requirement for all 50 clients and has also failed to file the form with the SEC via IARD. This is a material compliance deficiency that would likely be identified in an SEC examination.
**Analysis:** The firm must immediately: (1) draft a Form CRS compliant with SEC format requirements, (2) file it with the SEC via IARD, (3) deliver it to all existing clients, and (4) implement procedures to ensure delivery at the required trigger points going forward. The firm should consider disclosing the lapse to its CCO and potentially to the SEC if the deficiency is material. The 50 advisory agreements remain valid but the disclosure deficiency exposes the firm to regulatory action.

### Example 2: Relying on annual ADV delivery exception incorrectly
**Scenario:** An RIA updated its fee schedule mid-year, increasing advisory fees by 25 basis points for new clients. The firm also began offering a new service (financial planning) and added two new supervised persons. The firm does not distribute an updated brochure or summary of material changes, planning to address all changes in the next annual ADV delivery.
**Compliance Issues:** Material changes require interim delivery, not just annual updates. A 25 bps fee increase, addition of a new service, and new supervised persons providing advice are all material changes. Waiting until the annual update cycle delays required disclosure.
**Analysis:** The firm must: (1) file an amended Form ADV promptly with the SEC, (2) deliver a summary of material changes or an updated brochure to existing clients who are affected, (3) deliver Part 2B supplements for the new supervised persons to clients they advise, and (4) ensure new clients receive the updated documents before entering into advisory agreements. The annual delivery obligation supplements — but does not replace — the interim delivery requirement for material changes.

### Example 3: BD not providing timely trade confirmations for fixed income
**Scenario:** A broker-dealer's back-office system delays trade confirmations for fixed-income transactions by 5-7 business days after settlement due to a systems processing bottleneck. Equity confirmations are sent on trade date. The delay affects approximately 2,000 fixed-income transactions per quarter.
**Compliance Issues:** SEC Rule 10b-10 requires confirmations at or before completion of the transaction. A 5-7 day delay after settlement is a clear violation. Fixed-income confirmations must include accrued interest calculations, which may explain the processing delay, but the regulatory requirement does not accommodate systems limitations.
**Analysis:** The firm must: (1) remediate the systems bottleneck to ensure timely confirmation delivery, (2) review the scope of the issue (how many clients affected, over what period), (3) assess whether the deficiency must be reported to FINRA under FINRA Rule 4530 (which requires reporting of certain rule violations the firm self-identifies), (4) assess whether the delay caused client harm (e.g., inability to identify errors or unauthorized trades in a timely manner), and (5) implement monitoring to prevent recurrence. Firms should prioritize confirmation delivery systems for all asset classes, not just equities.

## Common Pitfalls
- Delivering Form ADV but forgetting Form CRS (or vice versa)
- Not filing Form CRS with the SEC — it must be both filed and delivered
- Treating annual ADV delivery as a substitute for interim material change delivery
- Failing to deliver Part 2B supplements when a new supervised person begins advising existing clients
- Assuming all electronic delivery is permissible without proper consent or access verification
- Not maintaining records of document delivery (dates, methods, versions delivered)
- Providing privacy notices that satisfy the letter of Reg S-P but do not actually explain the firm's information sharing practices clearly
- Delaying trade confirmations due to systems issues without recognizing the regulatory requirement for timely delivery
- Not updating delivery procedures when regulations change (e.g., Form CRS rollover delivery requirement)
- Sending account statements through the registered representative rather than directly to the customer

## Cross-References
- **fee-disclosure** (compliance plugin): Form ADV Item 5 and Form CRS fee section are key fee disclosure vehicles
- **reg-bi** (compliance plugin): Reg BI Disclosure Obligation drives much of the BD disclosure framework
- **fiduciary-standards** (compliance plugin): Full and fair disclosure is a core fiduciary obligation; Form ADV is the primary vehicle
- **conflicts-of-interest** (compliance plugin): Conflict disclosure is embedded throughout Form ADV, Form CRS, and Reg BI disclosures
- **advertising-compliance** (compliance plugin): Marketing materials must be consistent with disclosure documents
- **private-placements** (compliance plugin): PPM delivery, Rule 502(b) disclosure to non-accredited investors, and placement-compensation disclosure in exempt offerings


---

## SKILL: client-onboarding

- Fuente: `JoelLewis/finance_skills` → `plugins/advisory-practice/skills/client-onboarding` (MIT)
- Cuándo usarla: Design and implement end-to-end client onboarding workflows from prospect intake through funded account, covering KYC verification, document collection, e-signature, and custodian submission. Use when the user asks about building a digital onboarding flow, integrating identity verification or CIP checks, reducing NIGO rejection rates, opening complex account types like trusts or entities, connecting to custodian APIs, designing suitability questionnaires, or comparing advisor-assisted vs self-service models. Also trigger when users mention 'new account opening', 'onboarding bottleneck', 'KYC integration', 'beneficial ownership', 'OFAC screening', 'account funding', or 'onboarding automation'.

# Client Onboarding

## Core Concepts

### Onboarding Workflow Architecture
Client onboarding is an orchestrated, multi-stage process that transforms a prospect into a funded, investable account. The canonical stages are:

1. **Prospect intake** — capture contact information, establish CRM record, assign advisor
2. **Identity verification** — CIP/KYC checks (name, DOB, address, SSN/TIN, government ID)
3. **Suitability data collection** — investment objectives, risk tolerance, time horizon, financial situation
4. **Account type selection** — individual, joint, trust, IRA, entity, or other structure
5. **Document generation** — assemble the required document package based on account type and features
6. **E-signature** — execute new account forms, agreements, and disclosures electronically
7. **Custodian submission** — transmit the completed application to the custodian for account creation
8. **Funding** — ACH, wire, ACAT transfer, or check deposit to fund the new account
9. **Initial investment** — assign the funded account to a model portfolio or execute the initial trade

The two primary flow models are **advisor-assisted** and **self-service (digital-direct)**. In advisor-assisted onboarding, the advisor guides the client through each step, often in a meeting or screen-share, with the onboarding platform pre-populating data from the CRM. In self-service onboarding, the client completes a guided digital workflow independently, with the advisor reviewing and approving the completed application. Most firms support a hybrid model where self-service handles simple account types and advisor-assisted handles complex ones.

The onboarding platform acts as an orchestrator across multiple downstream systems: CRM (client master), KYC/AML vendor (identity verification), custodian (account opening API), document management (storage and retrieval), and portfolio management system (model assignment). The platform must manage state transitions, handle errors at each stage, and provide visibility to both the advisor and compliance.

### Digital Identity Verification
Identity verification during onboarding must satisfy CIP requirements under USA PATRIOT Act Section 326 and, for legal entities, the FinCEN CDD Rule (31 CFR 1010.230). The onboarding workflow collects the following minimum identifying information:

- **Individuals:** Full legal name, date of birth, residential address, Social Security Number (or TIN for non-citizens)
- **Entities:** Legal name, formation date, principal place of business, EIN/TIN, formation documents

**Verification methods integrated into digital onboarding:**

- **Database verification** — real-time API calls to identity verification vendors (LexisNexis Risk Solutions, Equifax, TransUnion, Alloy) that cross-reference provided data against credit bureau, public records, and government databases. This is the most common method for digital onboarding because it requires no document handling and provides a pass/fail result in seconds.
- **Document verification** — the client uploads a photo of a government-issued ID (driver's license, passport), and optionally a selfie for facial comparison. OCR extracts data fields; liveness detection prevents spoofing. Used as a fallback when database verification is inconclusive or as a primary method for non-US persons.
- **Knowledge-based authentication (KBA)** — the client answers challenge questions generated from their credit file (e.g., "Which of the following addresses have you lived at?"). KBA is declining in use due to data breach exposure but remains a supplementary method.
- **Biometric verification** — fingerprint or facial recognition, typically used in mobile onboarding flows.

**OFAC and sanctions screening** is a mandatory gate before account opening. The onboarding platform must screen all individuals associated with the account (account holders, authorized signers, beneficial owners, trustees) against the OFAC SDN list, FinCEN 314(a) lists, and any firm-specific restricted lists. A match or potential match must halt the onboarding flow and route to compliance for manual review.

**Beneficial ownership collection for entity accounts** requires identification of every individual who directly or indirectly owns 25% or more of the equity interests in the legal entity, plus at least one individual with significant managerial control (the control person). The onboarding workflow must dynamically present beneficial ownership forms when the account type is an entity (LLC, corporation, partnership, certain trusts).

**Enhanced due diligence triggers** that the onboarding system should detect and flag: politically exposed persons (PEPs), connections to high-risk jurisdictions (per FinCEN advisories and FATF guidance), complex multi-layered ownership structures, and negative news screening results. When EDD is triggered, the onboarding flow should pause and escalate to the compliance team before proceeding.

### Suitability and Risk Profiling
Onboarding is the primary data collection event for investment suitability. Before any investment recommendation can be made, the firm must gather sufficient information to satisfy FINRA Rule 2111 (suitability) for broker-dealers and Regulation Best Interest for BD recommendations, or the fiduciary duty of care for registered investment advisers.

**Required data elements:**
- Investment objectives (capital preservation, income, growth, aggressive growth, speculation)
- Time horizon (short-term under 3 years, intermediate 3-10 years, long-term over 10 years)
- Risk tolerance (conservative, moderate, aggressive — and the behavioral willingness to endure volatility)
- Liquidity needs (anticipated withdrawals, major expenses, emergency reserves)
- Annual income and net worth (including liquid net worth)
- Investment experience (years of experience, asset classes traded, knowledge level)
- Tax status (marginal tax bracket, tax-sensitive vs tax-exempt accounts)
- Special circumstances (concentrated stock positions, employer restrictions, ESG preferences)

**Risk questionnaire design** follows two approaches:

- **Psychometric questionnaires** measure the client's emotional and behavioral relationship with risk — willingness to accept losses, reaction to market downturns, comfort with uncertainty. These are better at capturing true risk tolerance but can be subjective.
- **Knowledge-based questionnaires** assess the client's understanding of investment concepts and their objective financial capacity to bear risk. These are more defensible from a compliance standpoint but may not capture behavioral tendencies.

Best practice is a combined approach: psychometric questions to assess willingness, financial data to assess capacity, and a mapping algorithm that produces a risk score or category. The risk score then maps to a model portfolio or investment strategy range.

**Regulatory requirements at onboarding:** The suitability profile must be documented before the first investment recommendation. For discretionary accounts, the investment policy statement (IPS) should be established during onboarding. For Reg BI accounts, the Care Obligation requires that any recommendation — including account type — have a reasonable basis given the client's profile.

### Account Type Selection and Configuration
The onboarding workflow must guide account type selection based on the client's needs. Account types and their key characteristics:

**Individual and joint accounts:**
- Individual taxable — single owner, simplest structure
- Joint Tenants with Right of Survivorship (JTWROS) — co-owners; on death, surviving owner inherits automatically
- Tenants in Common (TIC) — co-owners; each owns a specified share that passes to their estate
- Community Property — available in community property states; assets acquired during marriage are jointly owned

**Retirement accounts:**
- Traditional IRA — tax-deductible contributions (subject to income limits), tax-deferred growth, RMDs at age 73
- Roth IRA — after-tax contributions, tax-free growth and qualified withdrawals, no RMDs during owner's lifetime
- SEP IRA — employer-funded; contribution limits up to 25% of compensation or the annual dollar limit
- SIMPLE IRA — employee salary deferral plus employer match or non-elective contribution
- Inherited IRA — beneficiary account; subject to 10-year distribution rule (SECURE Act) for most non-spouse beneficiaries

**Trust accounts:**
- Revocable (living) trust — grantor maintains control; assets avoid probate; grantor's SSN typically used as TIN
- Irrevocable trust — grantor gives up control; separate tax entity with its own EIN; beneficial ownership rules apply
- Testamentary trust — created by will; requires court documentation

**Entity accounts:**
- LLC — requires articles of organization, operating agreement, EIN, beneficial ownership certification
- Corporation (C-Corp, S-Corp) — requires articles of incorporation, bylaws, corporate resolution, EIN
- Partnership (LP, LLP, GP) — requires partnership agreement, EIN, identification of general partner(s)

**Custodial accounts:**
- UTMA/UGMA — custodian manages assets for a minor until the age of majority (18 or 21 depending on state)

**Estate accounts:**
- Require letters testamentary or letters of administration, death certificate, EIN for the estate

**Account features configured during onboarding:**
- Margin eligibility (requires separate margin agreement and additional disclosures)
- Options approval level (levels 0-4 depending on custodian; requires options agreement and risk disclosure)
- Check writing and debit card access
- Tax lot accounting method selection (specific identification, FIFO, average cost)
- Beneficiary designation (primary and contingent for retirement and TOD accounts)
- Dividend and capital gains reinvestment preferences
- Trusted contact person (FINRA Rule 4512)

### Document Collection and Generation
Each account type requires a specific document package. The onboarding system should dynamically assemble the required documents based on the account type and features selected.

**Universal documents (all account types):**
- New account application form (custodian-specific)
- W-9 (US persons) or W-8BEN/W-8BEN-E (non-US persons)
- Advisory agreement or brokerage agreement
- Form CRS (Client Relationship Summary)
- Privacy notice (Reg S-P)
- Trusted contact person designation

**Account-type-specific documents:**
- Joint accounts: joint account agreement specifying ownership type
- Trust accounts: trust certification (or full trust agreement), trustee identification, trust TIN documentation
- Entity accounts: formation documents (articles of incorporation/organization, partnership agreement), corporate resolution or operating agreement authorizing the account, beneficial ownership certification form (FinCEN)
- IRA accounts: IRA adoption agreement, beneficiary designation form, IRA disclosure statement, rollover/transfer forms (if funding from another retirement account)
- Estate accounts: letters testamentary/administration, death certificate, EIN assignment letter
- Custodial accounts (UTMA/UGMA): custodial account agreement, minor's SSN

**Feature-specific documents:**
- Margin: margin agreement, margin risk disclosure
- Options: options agreement, OCC Characteristics and Risks of Standardized Options document

**Document assembly** in modern onboarding platforms involves pre-populating forms with data already collected during earlier onboarding stages (identity, suitability, account type). The system generates a personalized document package with client data filled in, leaving only signature blocks and any fields that require manual completion. This dramatically reduces errors and accelerates the process.

**Document management considerations:**
- Version control: track which version of each form was used (custodians update forms periodically)
- Expiration tracking: certain documents (e.g., trust certifications, corporate resolutions) may need periodic recertification
- Retention: SEC Rule 17a-4 (broker-dealers) and Rule 204-2 (investment advisers) govern document retention periods — typically 5-6 years, with some records retained for the life of the account
- Storage: documents should be stored in a searchable, indexed repository linked to the client and account records

### E-Signature and Consent
Electronic signatures are legally binding for account opening documents under the E-SIGN Act (15 USC 7001) and the Uniform Electronic Transactions Act (UETA), adopted in some form by 49 states and DC.

**E-SIGN Act requirements for valid electronic signatures:**
- The signer must consent to use electronic records and signatures
- The consent must be informed — the signer must be told what types of records will be provided electronically and how to withdraw consent
- The signer must demonstrate the ability to access electronic records in the format used
- The firm must retain the electronic record in a form that accurately reproduces the original

**E-signature platform integration:** Most advisory firms use DocuSign, Adobe Sign, or custodian-embedded signing tools (e.g., Schwab's e-signature within their account opening API). Integration patterns include:

- **Embedded signing** — the e-signature ceremony is embedded within the onboarding platform's user interface, providing a seamless experience
- **Redirect signing** — the client is redirected to the e-signature vendor's portal to complete signing, then returned to the onboarding platform
- **Email-based signing** — the client receives an email with a link to review and sign documents, completing the process asynchronously

**Consent to electronic delivery** is a prerequisite. Before delivering documents electronically, the firm must obtain the client's affirmative consent, inform them of their right to receive paper copies, and verify their ability to access electronic documents. This consent is typically captured as one of the first steps in a digital onboarding flow.

**Wet signature exceptions:** Some custodians and certain form types still require original (wet ink) signatures. Common exceptions include: certain international account forms, some trust documentation, specific alternative investment subscription agreements, and medallion signature guarantees for account transfers. The onboarding system should identify these exceptions and route them to a wet-signature workflow.

**Signature ceremony design for multi-party accounts:**
- Joint accounts: both owners must sign; the system should define a signing order or allow parallel signing
- Trust accounts: all trustees authorized to act on the account must sign
- Entity accounts: authorized signers per the corporate resolution or operating agreement must sign
- The system must track completion status for each signer and send reminders for incomplete ceremonies

**Audit trail requirements:** The e-signature record must include: signer identity (name, email), timestamp of each signature, IP address, authentication method used, document hash (to prove the signed document was not altered post-signature), and a certificate of completion. This audit trail must be retained as part of the account records.

### Custodian Submission and Account Funding
After documents are signed, the completed application package is submitted to the custodian for account creation. Submission methods vary by custodian and account complexity:

**API-based submission (straight-through processing):**
- Major custodians (Charles Schwab, Fidelity, Pershing, TD Ameritrade/Schwab) offer account opening APIs that accept structured data and documents
- The onboarding platform submits client data, account configuration, and signed documents programmatically
- The custodian validates the submission and returns an account number (typically within minutes to hours for standard accounts)
- This is the target state for high-volume firms seeking straight-through processing (STP)

**Semi-automated submission:**
- Some custodians accept submissions through their advisor portal with pre-populated data
- The onboarding platform generates a data file or pre-fills the custodian's web forms
- An operations team member reviews and clicks "submit" — human-in-the-loop

**Manual submission:**
- Complex account types (certain trusts, estates, entities, international accounts) often require manual submission
- Signed documents are uploaded to the custodian's document portal or sent via secure file transfer
- Processing time ranges from days to weeks depending on account complexity

**NIGO (Not In Good Order) handling:**
A NIGO rejection means the custodian has found errors or missing information in the application. Common NIGO causes:
- Missing or illegible signatures
- Inconsistent data between forms (e.g., name on W-9 does not match account application)
- Missing required documents (e.g., trust certification not included)
- Invalid or expired identity documents
- Missing beneficial ownership certification for entity accounts
- Incorrect account type coding
- Missing beneficiary designation for retirement accounts

NIGO remediation workflow: the onboarding system should receive NIGO notifications from the custodian (via API callback, email, or status polling), parse the rejection reason, notify the advisor and/or client, collect the corrected information or documents, and resubmit. Reducing NIGO rates is one of the highest-impact onboarding optimizations.

**Account funding methods:**
- **ACH transfer** — electronic transfer from a linked bank account; typically 2-4 business days; requires bank account verification (micro-deposits, Plaid, or manual voided check)
- **Wire transfer** — same-day or next-day funding for large amounts; requires wire instructions from the custodian
- **ACAT transfer** — Automated Customer Account Transfer system (DTCC) for transferring assets from another brokerage; typically 4-6 business days for full transfers; partial ACAT for specific positions
- **Check deposit** — physical check or mobile check deposit; subject to hold periods
- **In-kind transfer** — transferring existing securities without liquidating; important for tax-sensitive clients
- **Rollover** — direct rollover from employer plan or another IRA; requires rollover paperwork from the distributing institution

**Initial investment:** Once the account is funded, the onboarding system should trigger model portfolio assignment. For discretionary accounts, this means linking the account to the appropriate model in the portfolio management system (PMS) and generating the initial trade orders. For non-discretionary accounts, the advisor submits the first investment recommendation.

### Compliance Checkpoints
Effective onboarding embeds compliance gates at specific stages, preventing the workflow from advancing until requirements are met:

**Gate 1 — Identity verification (before account opening):**
- CIP verification must return a pass result
- OFAC/sanctions screening must clear all associated individuals
- If either fails, the flow halts and routes to compliance
- No account can be opened until identity is verified (USA PATRIOT Act Section 326)

**Gate 2 — Suitability documentation (before investment):**
- Investment profile (objectives, risk tolerance, time horizon, financial situation) must be completed
- Risk questionnaire must be scored and documented
- For Reg BI: the initial recommendation (including account type recommendation) must have a documented reasonable basis
- For fiduciary advisers: the suitability profile must support the proposed investment strategy

**Gate 3 — Beneficial ownership (before entity account opening):**
- FinCEN beneficial ownership certification must be completed for all legal entity accounts
- 25% owners and at least one control person must be identified and verified
- Exempt entity types (publicly traded companies, regulated financial institutions, government entities) must be documented

**Gate 4 — Disclosure delivery (before or at account opening):**
- Form CRS must be delivered before or at the time of opening the account
- Form ADV Part 2A (RIAs) must be delivered before or at the time of entering the advisory agreement
- Privacy notice must be delivered at account opening
- Margin and options disclosures must be delivered if those features are selected

**Gate 5 — Supervisory review (risk-based, before account activation):**
- Certain account types or client profiles trigger mandatory supervisory review before the account becomes active
- Common triggers: discretionary authority requested, margin or options trading, senior investors (age 65+), high-net-worth thresholds, PEPs or EDD clients, concentrated positions, complex entity structures
- The supervisor reviews the application package, suitability documentation, and any compliance flags
- The system must track review status and prevent account activation until supervisory approval is recorded

**Compliance hold and escalation:**
- When any gate fails, the application enters a compliance hold state
- The system notifies the compliance team with the specific failure reason and supporting documentation
- Escalation paths: line supervisor, compliance officer, chief compliance officer, legal counsel
- Resolution options: request additional information from the client, approve with conditions, decline the account
- All compliance decisions must be documented and retained

### Data Flow and System Integration
Onboarding is the primary data collection event that populates downstream systems. The data collected during onboarding flows to:

- **CRM (client master)** — contact information, household relationships, advisor assignment, service tier, communication preferences. The CRM should be the first system updated, often serving as the source of truth for client identity data.
- **Portfolio management system (PMS)** — account number, model portfolio assignment, investment restrictions, tax lot method, rebalancing preferences. The PMS receives the new account once it is created at the custodian and funded.
- **Custodian/account master** — the custodian maintains the official account record, including registration, tax status, beneficiaries, and authorized parties. The onboarding system submits data to the custodian; the custodian returns the account number and confirmation.
- **Compliance systems** — KYC/AML records, suitability documentation, disclosure delivery confirmations, supervisory review records. These records must be retained per regulatory requirements and accessible for examinations.
- **Document repository** — signed account opening documents, identity verification records, formation documents for entities, trust certifications. Must be indexed by client and account for retrieval.
- **Financial planning system** — goals, time horizons, income projections, tax data. If the firm uses a planning tool, onboarding data should feed into the initial plan.

**Integration patterns:**
- **Real-time API calls** — for identity verification, custodian submission, OFAC screening. These require immediate responses and should include timeout handling and fallback procedures.
- **Asynchronous/event-driven** — for downstream notifications (e.g., notifying the PMS that a new account is ready for model assignment). Message queues or webhook patterns are common.
- **Batch processing** — some custodian integrations operate on batch submission cycles (e.g., end-of-day file uploads). The onboarding system must queue submissions and reconcile results.

**Data validation:** The onboarding system should validate data consistency across systems. Common validation checks:
- Name and SSN/TIN match across all forms and systems
- Account type is consistent between the onboarding platform and custodian
- Beneficiary designations match between the onboarding record and custodian record
- Advisor assignment in CRM matches the advisory agreement
- Tax lot method in the PMS matches the client's election

**Pre-population for existing clients:** When an existing client opens an additional account, the onboarding system should pre-populate known data from the CRM and existing account records. Identity verification may be streamlined (re-verification vs full CIP depending on firm policy), and suitability data may only need to be confirmed rather than re-collected.

### Onboarding Metrics and Optimization
Measuring onboarding effectiveness enables continuous improvement:

**Key performance indicators:**
- **Time-to-funded-account** — elapsed time from prospect intake to first funded dollar. Industry benchmarks: 3-5 business days for simple accounts via digital onboarding, 2-4 weeks for complex accounts. Target for best-in-class digital: same day for individual taxable accounts.
- **Application abandonment rate** — percentage of onboarding flows started but not completed. High abandonment at a specific step indicates friction. Industry average: 25-40% for digital-direct flows; significantly lower for advisor-assisted.
- **NIGO rate** — percentage of submissions rejected by the custodian. Target: under 5%. Industry average: 10-20% for firms without automated validation.
- **Straight-through processing (STP) rate** — percentage of applications that pass from submission to account creation without manual intervention. Target: above 80% for standard individual and joint accounts.
- **First-contact resolution rate** — percentage of onboarding issues resolved without requiring the client to take additional action.
- **Client satisfaction score** — post-onboarding survey measuring the client's experience.

**Bottleneck identification:**
- Analyze time spent at each onboarding stage to identify where applications stall
- Common bottlenecks: identity verification failures (especially for non-US persons), missing trust documents, client delays in completing e-signature, custodian processing backlogs, compliance review queues
- Implement dashboards showing pipeline status: how many applications are at each stage, average time per stage, aging applications

**Optimization strategies:**
- **Reduce data entry** — pre-populate from CRM, use OCR for document data extraction, integrate with bank verification services (Plaid, Yodlee) for funding
- **Validate early** — run real-time validation checks as data is entered rather than waiting for custodian submission; catch NIGO-causing errors before documents are signed
- **Parallelize where possible** — run identity verification while the client completes the suitability questionnaire; generate documents while waiting for verification results
- **Design mobile-first** — clients increasingly complete onboarding on mobile devices; forms must be responsive and signature flows must work on small screens
- **A/B test onboarding flows** — test different question orders, form layouts, and communication cadences to reduce abandonment
- **Automate follow-up** — send automated reminders for incomplete applications, unsigned documents, and unfunded accounts

## Worked Examples

Three worked examples are in [references/examples.md](references/examples.md) — load for an end-to-end scenario: (1) designing a digital onboarding flow for individual taxable accounts with Schwab/Salesforce/Orion integration, (2) onboarding an irrevocable trust account for a high-net-worth client alongside individual accounts, (3) reducing a 35% NIGO rate through validation rules and automated document assembly.

## Common Pitfalls
- Opening an account before identity verification is complete — CIP must be satisfied before or at account opening, not after
- Collecting suitability data but not documenting it in a format that satisfies regulatory requirements — the profile must be written, signed or acknowledged, and retained
- Using a one-size-fits-all document package rather than dynamically assembling documents based on account type and features
- Not screening all associated individuals (co-owners, trustees, beneficial owners, authorized signers) against OFAC — screening only the primary account holder is insufficient
- Allowing the onboarding flow to proceed past compliance gates when a checkpoint fails — soft gates that can be bypassed undermine the compliance framework
- Assuming e-signatures are universally accepted — certain custodians and form types still require wet signatures
- Not maintaining a mapping between risk questionnaire scores and model portfolios, leading to inconsistent investment recommendations across advisors
- Failing to validate data consistency before custodian submission, resulting in high NIGO rates
- Treating entity and trust onboarding the same as individual onboarding — these account types require substantially more documentation, verification, and review
- Not linking multiple accounts opened for the same client into a single household, causing fragmented client data across CRM and PMS
- Neglecting the funding step — an opened but unfunded account generates no revenue and may be closed by the custodian after an inactivity period
- Collecting beneficial ownership information but not verifying the identities of the beneficial owners, violating the CDD Rule's verification requirement

## Cross-References
- **know-your-customer** (compliance plugin): KYC/CIP requirements that the onboarding identity verification stage must satisfy; the KYC skill defines the regulatory standards, and this skill describes how to implement them in an onboarding workflow
- **investment-suitability** (compliance plugin): Suitability data collection during onboarding provides the foundation for all subsequent investment recommendations; the suitability skill defines the regulatory obligations, and this skill covers how to gather the required data
- **anti-money-laundering** (compliance plugin): OFAC screening and AML checks are embedded compliance gates in the onboarding flow; the AML skill covers the regulatory framework, and this skill describes the integration points
- **reg-bi** (compliance plugin): Reg BI disclosure and care obligations must be satisfied at or before account opening; Form CRS delivery is a required onboarding step for broker-dealers and RIAs
- **client-disclosures** (compliance plugin): Disclosure documents (Form ADV, Form CRS, privacy notice, prospectus) must be delivered during onboarding at prescribed trigger points
- **crm-client-lifecycle** (advisory-practice plugin): The CRM receives client and household data from the onboarding process; onboarding creates the client master record that CRM manages throughout the relationship
- **portfolio-management-systems** (advisory-practice plugin): The PMS receives new accounts from onboarding for model portfolio assignment and initial investment execution
- **privacy-data-security** (compliance plugin): Onboarding collects sensitive nonpublic personal information (SSN, financial data, identity documents) that must be protected under Reg S-P and firm cybersecurity policies
- **account-opening-workflow** (client-operations plugin): Back-office account opening process that receives onboarding outputs; handles operations processing, custodian submission, and account activation
- **estate-gifting** (wealth-management plugin): background on trust types and beneficiary designations relevant when opening and titling trust accounts

### Referencia: references/examples.md

# Worked Examples — Client Onboarding

## Table of Contents

1. [Designing a Digital Onboarding Flow for Individual Taxable Accounts](#example-1-designing-a-digital-onboarding-flow-for-individual-taxable-accounts) — Schwab/Salesforce/Orion integration, identity verification, pre-submission validation, 3-day time-to-funded target
2. [Onboarding a Trust Account for a High-Net-Worth Client](#example-2-onboarding-a-trust-account-for-a-high-net-worth-client) — irrevocable trust beneficial ownership, multi-account onboarding event, EDD and supervisory review
3. [Reducing a 35% NIGO Rate](#example-3-reducing-a-35-nigo-rate) — NIGO categorization, validation rules engine, automated document assembly, phased remediation

## Example 1: Designing a digital onboarding flow for individual taxable accounts
**Scenario:** A mid-sized RIA with $2B AUM and 50 advisors wants to implement digital onboarding for individual taxable accounts. The firm uses Schwab as its primary custodian, Salesforce as its CRM, and Orion as its portfolio management system. Currently, onboarding is paper-based, takes 7-10 business days, and has a 22% NIGO rate. The firm wants to reduce time-to-funded-account to under 3 business days and NIGO rate below 5%.

**Design Considerations:**
- The onboarding platform must integrate with Schwab's account opening API, Salesforce for client data pre-population, and Orion for model portfolio assignment
- Identity verification should use a database verification vendor (such as Alloy or LexisNexis) as the primary method, with document verification (ID upload) as fallback
- OFAC screening must be integrated as an automated gate that runs immediately after identity data is collected
- The suitability questionnaire should combine psychometric risk tolerance questions with financial data collection, producing a risk score that maps to the firm's model portfolios
- Document generation should be fully automated: the system assembles the Schwab new account form, W-9, advisory agreement, Form CRS, privacy notice, and trusted contact designation, pre-populated with collected data
- E-signature should be embedded in the onboarding flow (not email-based) to minimize drop-off, using DocuSign or Schwab's native e-signature
- Real-time validation must check for common NIGO causes before custodian submission: name consistency, SSN format, complete address, all required signatures present
- After Schwab returns the account number, the system should automatically initiate ACH funding (if the client linked a bank account during onboarding) and notify Orion to assign the account to the model portfolio matching the client's risk score

**Analysis:** The recommended flow is: (1) advisor initiates onboarding from Salesforce, pre-populating known client data; (2) client receives a secure link to complete onboarding digitally; (3) client enters personal information and the system runs real-time identity verification and OFAC screening; (4) client completes the suitability questionnaire and the system generates a risk score; (5) system presents the recommended model portfolio and the advisor confirms; (6) document package is generated and the client signs electronically; (7) system validates the complete package against Schwab's requirements; (8) application is submitted to Schwab via API; (9) Schwab returns the account number; (10) ACH funding is initiated and Orion receives the new account for model assignment. For the 22% NIGO rate, the primary remediation is step 7 — pre-submission validation that catches the errors Schwab would reject. Common causes like name mismatches, missing signatures, and incomplete forms can be caught in real time. The 3-business-day target is achievable for the digital path: identity verification and document signing can occur in a single session (day 1), Schwab API submission processes within hours (day 1-2), and ACH funding settles in 2-3 business days (day 2-3).

## Example 2: Onboarding a trust account for a high-net-worth client
**Scenario:** An advisor at a registered investment adviser is onboarding a new high-net-worth client who wants to invest $5M through a family irrevocable trust. The trust was established 3 years ago, has its own EIN, and names the client and her attorney as co-trustees. The trust has four beneficiaries (the client's adult children). The client also wants a personal taxable account and a Roth IRA.

**Design Considerations:**
- The irrevocable trust is a legal entity requiring full beneficial ownership certification under the FinCEN CDD Rule: identify all individuals owning 25% or more of the trust's beneficial interests and at least one control person
- With four beneficiaries who are the beneficial interest holders, the firm must determine if any owns 25% or more. If the trust splits evenly (25% each), all four meet the threshold and must be identified. The control persons are the co-trustees (the client and her attorney)
- The trust requires its own EIN, a trust certification (or relevant pages of the trust agreement showing formation, trustees, and investment powers), and verification that the trustees have authority to open investment accounts
- Enhanced due diligence considerations: $5M meets most firms' high-net-worth thresholds for supervisory review; irrevocable trust is a complex structure warranting additional scrutiny of the trust's purpose and source of funds
- The personal taxable account and Roth IRA can follow the standard individual onboarding flow; identity verification for the client carries across all three accounts
- Document packages differ substantially: the trust account requires the new account form in the trust's name, W-9 with the trust's EIN, trust certification, beneficial ownership form, and advisory agreement naming the trust as the client; the taxable account requires standard individual forms with the client's SSN; the Roth IRA requires the IRA adoption agreement, beneficiary designation, and IRA disclosure statement
- All three accounts should be linked to a single household in the CRM and PMS for consolidated reporting

**Analysis:** The onboarding workflow should handle this as a single onboarding event with multiple account openings. Start with client identity verification (CIP), which satisfies requirements for the individual accounts and verifies one of the trustees for the trust account. Then collect suitability data for each account (the trust may have different investment objectives than the personal accounts). Next, request the trust documentation: the full trust certification, trust EIN assignment letter, and identification information for the co-trustee (attorney) and all four beneficiaries. Run OFAC screening on all individuals (client, attorney co-trustee, four beneficiaries — six people total). Complete the FinCEN beneficial ownership certification form. Route the trust account application through supervisory review given the complexity and dollar amount. Generate three separate document packages, one per account. The trust account will likely require manual or semi-automated submission to the custodian even if the individual accounts can use API submission, due to the additional documentation. Expect the trust account to take 1-2 weeks from submission to account opening, while the individual accounts can be opened within days. Funding the trust account via wire transfer is common for this dollar amount; the taxable account can be funded via ACAT if the client has an existing brokerage account elsewhere; the Roth IRA may involve a rollover or contribution depending on the source of funds.

## Example 3: Reducing a 35% NIGO rate
**Scenario:** A broker-dealer and RIA with 200 advisors processes 500 new account applications per month through a combination of custodians (Schwab, Fidelity, Pershing). The firm's current NIGO rate is 35%, meaning 175 applications per month are rejected on first submission. Average remediation time for a NIGO rejection is 5 business days, and the operations team spends 60% of its time on NIGO resolution. The firm wants to reduce the NIGO rate to under 10%.

**Design Considerations:**
- First priority is to categorize existing NIGO rejections by cause. Common categories: missing signatures (often 20-30% of NIGOs), data inconsistencies between forms (15-25%), missing or expired documents (15-20%), incorrect account type coding (10-15%), incomplete beneficiary designations (5-10%), missing beneficial ownership for entities (5-10%)
- Each custodian has different form requirements and validation rules; the firm must maintain a rules engine that knows each custodian's specific requirements
- The root cause is often that advisors complete forms manually with no real-time validation, and errors are not caught until the custodian reviews the application days later
- Multi-custodian complexity amplifies the problem: advisors must know which forms and requirements apply to each custodian, and mistakes are more likely when switching between custodians

**Analysis:** A phased approach to reducing the NIGO rate from 35% to under 10%:

Phase 1 — Diagnose (weeks 1-2): Categorize the last 6 months of NIGO rejections by custodian, account type, rejection reason, and originating advisor. Identify the top 5 rejection reasons, which will typically account for 70-80% of all NIGOs. Identify whether certain advisors or offices have disproportionately high NIGO rates (indicating a training issue vs a systemic issue).

Phase 2 — Implement pre-submission validation (weeks 3-8): Build a validation rules engine that checks every application against the applicable custodian's requirements before submission. Critical validations: all required fields populated, signatures present on all required pages, name and SSN/TIN consistent across all forms, account type code matches the application data, beneficiary designation complete for retirement accounts, beneficial ownership form included for entity accounts, required supporting documents attached (trust certification, formation documents). The validation engine should prevent submission until all checks pass and provide clear error messages to the advisor or operations team.

Phase 3 — Automate document assembly (weeks 6-12): Replace manual form completion with automated document generation that pre-populates custodian-specific forms from a single data collection workflow. This eliminates the majority of data inconsistency errors because data is entered once and propagated to all forms. Support all three custodians with custodian-specific form templates and validation rules.

Phase 4 — Train and monitor (ongoing): Provide targeted training to advisors with high NIGO rates. Publish a weekly NIGO dashboard showing rates by custodian, account type, rejection reason, and advisor. Set NIGO rate targets (under 15% at 90 days, under 10% at 180 days) and review progress monthly.

Expected outcome: Pre-submission validation alone typically reduces NIGO rates by 50-60% (from 35% to 14-17%). Adding automated document assembly reduces the remaining errors by another 50% or more (to 7-10%). The combined effect should achieve the sub-10% target within 6 months, freeing the operations team to focus on complex account types rather than routine error remediation.


---

## SKILL: conflict-of-interest

- Fuente: `SYasJ/claude-business-skills` → `plugins/risk/skills/conflict-of-interest` (MIT)
- Cuándo usarla: Structure a conflict-of-interest disclosure so a reviewer can see the interest and the decision it touches. Use when the user mentions conflict of interest, COI disclosure, related party, disclose a conflict, or asks for a conflict disclosure. Risk and compliance skill by Yasir Jilani.

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'conflict-of-interest' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Conflict of Interest Disclosure

Structure a conflict-of-interest disclosure so a reviewer can see the interest and the decision it touches.

## When to use this skill

Use this skill when the user:

- conflict of interest
- COI disclosure
- related party
- disclose a conflict

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

- The interest
- The decision or process it touches
- Who else knows
- The review path

## Workflow


### 1. Describe the interest in plain language

financial, family, or outside role, as the user stated.
### 2. Step 2

Name the decision or vendor it could affect.
### 3. Step 3

Propose recusal or a review, using their policy if they supplied one.
### 4. Step 4

Do not help hide the interest.
### 5. Step 5

Minimize unrelated personal details.
### 6. Step 6

Record the reviewer's decision once they make it. Do not invent an approval.

## Output

Deliver a **conflict disclosure**.

- Purpose of this conflict disclosure, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a conflict disclosure by 30 September 2026. An employee wants the disclosure to omit that their sibling owns the bidding vendor.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

An employee wants the disclosure to omit that their sibling owns the bidding vendor.

The interest: Control 7.2 access review, recorded 14 September 2026. No supporting file attached
The decision or process it touches: An employee wants the disclosure to omit that their sibling owns the bidding vendor
Who else knows: Priya Shah, controller
The review path: Control 7.2 access review, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Conflict disclosure — draft ready to send**

> To: the recipient named in the file
> From: Priya Shah, controller, Northline Studio
> Date: 14 September 2026

---

Hello,

Includes the sibling relationship and recommends recusal from the award.

Everything above comes from the file dated 14 September 2026. Where a figure, a date, or a commitment was not in that file, this note leaves it out rather than filling the gap.

One point is still open, and I would rather flag it than paper over it. I will confirm it before 30 September 2026 and follow up either way.

Priya Shah
controller, Northline Studio

---

**How this draft was checked**

1. **Describe the interest in plain language** — financial, family, or outside role, as the user stated.
2. **Name the decision or vendor it could affect**
3. **Propose recusal or a review, using their policy if they supplied one**
4. **Do not help hide the interest**

**Deliberately not done**
- Hiding an interest.
- Unrelated personal details.
- A fake approval.

Next: Priya Shah sends after confirming the open point. Due 30 September 2026. This is a draft, not a sent message.

## Anti-patterns

- Hiding an interest
- Unrelated personal details
- A fake approval

## Related skills

- `gifts-and-entertainment`
- `procurement-award-note`
