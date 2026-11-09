# 10-wealth-planning-fiscal — parte 2

Skills de terceros agrupadas por tema. Cada sección indica fuente, licencia y dónde está su código.



---

## SKILL: tax-loss-harvesting

- Fuente: `agiprolabs/claude-trading-skills` → `skills/tax-loss-harvesting` (MIT)
- Cuándo usarla: Tax-loss harvesting opportunity identification, scoring, and planning with wash sale compliance and annual carryforward tracking
- Código: extraer `code/agiprolabs_claude-trading-skills.tar` y usar `skills/tax-loss-harvesting/` (harvest_scanner.py)

# Tax-Loss Harvesting

Identify, score, and plan tax-loss harvesting (TLH) opportunities across a crypto portfolio. This skill covers unrealized-loss ranking, net-benefit calculation, wash sale compliance, annual loss carryforward tracking, and year-end "use it or lose it" strategies.

> **Disclaimer:** This skill provides informational analysis only. It is NOT tax advice. Tax rules vary by jurisdiction and change frequently. Consult a qualified tax professional before making any tax-related trading decisions.

## How Tax-Loss Harvesting Works

Tax-loss harvesting is the practice of intentionally realizing investment losses to offset realized capital gains, thereby reducing your current-year tax liability.

### Core Mechanism

1. **Identify** positions with unrealized losses in your portfolio.
2. **Sell** those positions to realize the loss.
3. **Offset** realized gains with the harvested loss, reducing taxable income.
4. **Optionally re-enter** a similar (but not "substantially identical") position to maintain market exposure.

### Short-Term vs Long-Term

| Holding Period | Classification | Typical Tax Rate |
|---------------|---------------|-----------------|
| < 1 year | Short-term capital gain/loss | Ordinary income rate |
| >= 1 year | Long-term capital gain/loss | Preferential rate (0-20%) |

Short-term losses first offset short-term gains; long-term losses first offset long-term gains. Remaining net losses cross over to offset the other category.

### Annual Loss Deduction Limit

If total net losses exceed total gains, the excess is deductible against ordinary income up to **$3,000 per year** ($1,500 if married filing separately). Any remaining loss carries forward indefinitely to future tax years.

## Ranking Unrealized Losses

Not all unrealized losses are equally valuable to harvest. This skill scores each opportunity on four dimensions:

### 1. Loss Magnitude

Larger dollar losses provide more tax savings. The raw loss is the difference between current market value and cost basis.

```
unrealized_loss = current_value - cost_basis  # negative when loss
tax_savings = abs(unrealized_loss) * marginal_tax_rate
```

### 2. Days Until Long-Term Threshold

A position approaching the 1-year holding mark deserves special consideration:
- If close to crossing into long-term territory, harvesting now locks in a **short-term loss** (offsets higher-taxed short-term gains).
- If already long-term, the loss offsets long-term gains (lower tax rate benefit).

```
days_held = (today - acquisition_date).days
days_to_long_term = max(0, 365 - days_held)
```

Positions with fewer days remaining until long-term are **more urgent** to evaluate because once they cross 365 days, a short-term loss becomes a less-valuable long-term loss.

### 3. Wash Sale Risk (Correlation Score)

The IRS wash sale rule prohibits claiming a loss if you buy a "substantially identical" security within 30 days before or after the sale. In crypto, the exact application is evolving, but prudent planning avoids re-entering the same token within the 61-day wash sale window (30 days before + sale day + 30 days after).

**Correlation scoring**: If you hold (or plan to re-enter) a position that is highly correlated with the harvested asset, wash sale risk increases. Score this as:

```
wash_sale_risk = 1.0  # if same token re-entry planned within 30 days
wash_sale_risk = correlation_coefficient  # if correlated substitute held
wash_sale_risk = 0.0  # if no re-entry or uncorrelated substitute
```

Higher wash sale risk reduces the effective score of the opportunity.

### 4. Available Gains to Offset

A harvested loss is only immediately useful if there are realized gains to offset. Score opportunities higher when:
- There are matching-type gains (short-term loss vs short-term gain).
- The loss amount does not greatly exceed available gains (diminishing marginal benefit beyond the $3K deduction cap).

```
offset_efficiency = min(1.0, available_matching_gains / abs(unrealized_loss))
```

### Composite Score

```python
def tlh_score(
    unrealized_loss: float,
    days_to_long_term: int,
    wash_sale_risk: float,
    offset_efficiency: float,
    weights: dict | None = None,
) -> float:
    w = weights or {
        "magnitude": 0.35,
        "urgency": 0.25,
        "wash_safety": 0.20,
        "offset_match": 0.20,
    }
    magnitude_score = min(abs(unrealized_loss) / 10_000, 1.0)
    urgency_score = max(0, 1.0 - days_to_long_term / 365)
    wash_safety_score = 1.0 - wash_sale_risk
    return (
        w["magnitude"] * magnitude_score
        + w["urgency"] * urgency_score
        + w["wash_safety"] * wash_safety_score
        + w["offset_match"] * offset_efficiency
    )
```

## Net Benefit Calculation

Harvesting a loss is not free. Transaction costs (swap fees, slippage, gas) reduce the benefit.

```python
def net_benefit(
    unrealized_loss: float,
    marginal_tax_rate: float,
    transaction_cost: float,
    re_entry_cost: float = 0.0,
) -> float:
    """Compute net dollar benefit of harvesting a loss.

    Args:
        unrealized_loss: Negative number representing the loss.
        marginal_tax_rate: Applicable tax rate (0.0 to 1.0).
        transaction_cost: Cost to execute the sell (fees + slippage).
        re_entry_cost: Cost to re-enter a substitute position.

    Returns:
        Net benefit in dollars. Positive means harvesting is worthwhile.
    """
    tax_savings = abs(unrealized_loss) * marginal_tax_rate
    total_costs = transaction_cost + re_entry_cost
    return tax_savings - total_costs
```

**Rule of thumb**: Only harvest when `net_benefit > 0` by a meaningful margin. Very small losses are not worth the transaction costs and operational complexity.

## Year-End "Use It or Lose It"

Near December 31, evaluate whether to accelerate harvesting:

1. **Tally year-to-date realized gains** (both short-term and long-term).
2. **Identify unrealized losses** that can offset those gains.
3. **Prioritize** losses that offset same-type gains (short-term loss vs short-term gain yields the highest tax rate differential).
4. **Check the $3K excess limit**: If net losses already exceed gains by $3K, additional harvesting this year has no immediate tax benefit (though the carryforward still has value).
5. **Consider settlement timing**: Ensure trades settle before year-end.

## Wash Sale Compliance

### The 61-Day Window

The wash sale rule applies to purchases of substantially identical securities within:
- **30 days before** the sale (retroactive wash sale)
- **The day of** the sale
- **30 days after** the sale

If triggered, the disallowed loss is added to the cost basis of the replacement shares, deferring (not eliminating) the tax benefit.

### Compliance Strategies

| Strategy | Description | Trade-off |
|----------|------------|-----------|
| **Wait 31 days** | Sell, wait 31 days, re-buy | Market exposure gap |
| **Substitute asset** | Sell, immediately buy a non-identical but correlated asset | Tracking error |
| **No re-entry** | Sell and stay out | Lost upside |
| **Double-up** | Buy additional shares, wait 31 days, sell original lot | Capital intensive |

### Crypto-Specific Considerations

- The IRS has not explicitly ruled that the wash sale rule applies to cryptocurrency (as of 2025). However, proposed legislation may extend it.
- Prudent practitioners treat crypto as subject to wash sale rules for conservative planning.
- Different tokens (e.g., SOL vs ETH) are generally considered non-identical.
- Wrapped versions of the same token (e.g., SOL vs wSOL) may be considered substantially identical.

## Annual Loss Carryforward Tracking

```python
def compute_carryforward(
    realized_gains_st: float,
    realized_gains_lt: float,
    realized_losses_st: float,
    realized_losses_lt: float,
    prior_carryforward: float = 0.0,
    annual_deduction_limit: float = 3_000.0,
) -> dict:
    """Compute net tax position and carryforward.

    Returns dict with keys:
        net_st, net_lt, total_net,
        deduction_used, carryforward
    """
    net_st = realized_gains_st + realized_losses_st  # losses are negative
    net_lt = realized_gains_lt + realized_losses_lt
    total_net = net_st + net_lt - prior_carryforward

    if total_net >= 0:
        return {
            "net_st": net_st, "net_lt": net_lt,
            "total_net": total_net, "deduction_used": 0.0,
            "carryforward": 0.0,
        }

    excess_loss = abs(total_net)
    deduction_used = min(excess_loss, annual_deduction_limit)
    carryforward = max(0, excess_loss - annual_deduction_limit)
    return {
        "net_st": net_st, "net_lt": net_lt,
        "total_net": total_net,
        "deduction_used": deduction_used,
        "carryforward": carryforward,
    }
```

## Prerequisites

- Python 3.10+
- No external dependencies for core calculations
- Portfolio data: cost basis, acquisition date, current market value per lot
- Tax parameters: marginal tax rate, filing status, prior carryforward

## Capabilities

| Capability | Description |
|-----------|-------------|
| Opportunity scanning | Identify all positions with unrealized losses |
| Multi-factor scoring | Rank by magnitude, urgency, wash safety, offset match |
| Net benefit analysis | Compare tax savings against transaction costs |
| Wash sale tracking | Flag positions within the 61-day window |
| Carryforward calculator | Track annual $3K limit and loss carryforward |
| Year-end planning | Prioritize harvesting before December 31 |
| Harvesting plan output | Generate actionable plan with sell orders and re-entry dates |

## Quick Start

```python
from datetime import date

# Define a portfolio position
position = {
    "symbol": "TOKEN-A",
    "cost_basis": 10_000.0,
    "current_value": 6_500.0,
    "acquisition_date": date(2025, 8, 15),
    "quantity": 500.0,
}

unrealized_loss = position["current_value"] - position["cost_basis"]  # -3500
days_held = (date.today() - position["acquisition_date"]).days
days_to_lt = max(0, 365 - days_held)

# Score the opportunity
score = tlh_score(
    unrealized_loss=unrealized_loss,
    days_to_long_term=days_to_lt,
    wash_sale_risk=0.0,
    offset_efficiency=0.8,
)
print(f"TLH score: {score:.3f}")

# Calculate net benefit
benefit = net_benefit(
    unrealized_loss=unrealized_loss,
    marginal_tax_rate=0.35,
    transaction_cost=15.0,
    re_entry_cost=15.0,
)
print(f"Net benefit: ${benefit:.2f}")
```

## Use Cases

1. **Quarterly portfolio review**: Scan all positions for harvesting opportunities ranked by composite score.
2. **Year-end tax planning**: Identify optimal set of positions to harvest before December 31 given year-to-date gain/loss totals.
3. **Ongoing monitoring**: Flag positions that are approaching the long-term threshold where harvesting a short-term loss becomes urgent.
4. **Carryforward management**: Track multi-year loss carryforward balances and project when they will be fully utilized.
5. **Transaction cost analysis**: Determine minimum loss threshold worth harvesting given current fee environment.

## Files

| File | Description |
|------|-------------|
| `references/planned_features.md` | TLH mechanics, scoring formula, wash sale interaction, carryforward rules, year-end strategies |
| `scripts/harvest_scanner.py` | Demo scanner: score opportunities, generate harvesting plan, compute net benefit |

> **Important:** This skill provides analytical tools for informational purposes only. All tax-related decisions should be reviewed by a qualified tax professional. Tax laws vary by jurisdiction and are subject to change.

### Referencia: references/planned_features.md

# Tax-Loss Harvesting — Planned Features Reference

## TLH Mechanics

Tax-loss harvesting (TLH) converts unrealized portfolio losses into realized losses that offset taxable gains. The core loop:

1. **Scan** — Identify positions where `current_value < cost_basis`.
2. **Score** — Rank each opportunity by a composite metric (see Scoring Formula below).
3. **Filter** — Exclude opportunities where net benefit is negative or wash sale risk is too high.
4. **Plan** — Generate sell orders with quantities, expected proceeds, and re-entry dates.
5. **Execute** — Sell the position (outside this skill's scope — see `jupiter-swap` or `dex-execution`).
6. **Track** — Record the realized loss, update carryforward, set wash sale window alerts.

### Lot-Level Tracking

When a position was acquired across multiple purchases ("lots"), each lot has its own cost basis and acquisition date. TLH should evaluate lots independently because:
- Some lots may have gains while others have losses.
- Lot-level selection (specific identification) lets you harvest only the losing lots.
- FIFO, LIFO, and specific identification methods produce different tax outcomes.

### Realized vs Unrealized

| Term | Definition |
|------|-----------|
| Unrealized loss | Paper loss — position held, not yet sold |
| Realized loss | Loss locked in by selling the position |
| Harvested loss | Realized loss intentionally created for tax purposes |

Only realized losses can offset gains on a tax return.

## Scoring Formula

The composite TLH score ranks opportunities on four equally-weighted-by-default dimensions, each normalized to [0, 1]:

### Magnitude Score

```
magnitude = min(abs(unrealized_loss) / reference_amount, 1.0)
```

`reference_amount` defaults to $10,000 but should scale with portfolio size. A $500 loss in a $10K portfolio is significant; in a $1M portfolio it is noise.

### Urgency Score

```
urgency = max(0, 1.0 - days_to_long_term / 365)
```

A position 10 days from crossing into long-term territory scores 0.97 urgency. One purchased yesterday scores near 0. This reflects the fact that short-term losses offset higher-taxed short-term gains.

### Wash Safety Score

```
wash_safety = 1.0 - wash_sale_risk
```

Where `wash_sale_risk` is:
- `1.0` — Same-token re-entry planned within 30 days.
- `0.5–0.9` — Highly correlated substitute held or planned.
- `0.0` — No re-entry or uncorrelated substitute.

### Offset Match Score

```
offset_match = min(1.0, available_matching_gains / abs(unrealized_loss))
```

A loss of $5,000 with $5,000 in matching gains scores 1.0. A loss of $5,000 with only $1,000 in matching gains scores 0.2. Losses beyond available gains still have value (up to $3K deduction + carryforward), but immediate benefit is lower.

### Composite

```
score = w_mag * magnitude + w_urg * urgency + w_wash * wash_safety + w_off * offset_match
```

Default weights: `{magnitude: 0.35, urgency: 0.25, wash_safety: 0.20, offset_match: 0.20}`.

Adjust weights based on context:
- **Year-end rush**: Increase urgency weight.
- **High wash sale environment**: Increase wash_safety weight.
- **Large realized gains**: Increase offset_match weight.

## Wash Sale Interaction

### The 61-Day Window

A wash sale is triggered when a taxpayer sells a security at a loss and, within **30 days before or after** the sale, acquires a "substantially identical" security.

```
wash_sale_window_start = sale_date - 30 days
wash_sale_window_end   = sale_date + 30 days
```

### Consequences of Triggering a Wash Sale

The loss is **disallowed** for the current tax year. However:
- The disallowed loss is **added to the cost basis** of the replacement shares.
- The holding period of the replacement shares includes the holding period of the original shares.
- The loss is deferred, not permanently lost.

### Planning Around Wash Sales

**Before selling** — Check if you purchased the same token within the prior 30 days. If so, that purchase triggers a retroactive wash sale on the planned harvest.

**After selling** — Set a 31-day calendar reminder before re-entering the position. Any purchase of the same token within 30 days disallows the loss.

**Substitute positions** — If you want continuous market exposure, buy a different but correlated token. For Solana tokens, consider:
- Selling SOL and buying a SOL-correlated token (e.g., JTO, BONK) — generally not "substantially identical."
- Selling one memecoin and buying another in the same sector — generally safe.
- Selling a wrapped token and buying the unwrapped version — potentially risky, may be considered identical.

## Carryforward Rules

### Annual Deduction Limit

Net capital losses exceeding net capital gains may offset up to **$3,000** of ordinary income per year ($1,500 for married filing separately).

### Carryforward Mechanics

Excess losses carry forward **indefinitely** to future tax years. The carryforward retains its character (short-term or long-term) in most cases.

**Year-by-year tracking example:**

| Year | Realized Gains | Realized Losses | Net | Deduction Used | Carryforward |
|------|---------------|----------------|-----|---------------|-------------|
| 2025 | $5,000 | -$15,000 | -$10,000 | $3,000 | $7,000 |
| 2026 | $8,000 | -$2,000 | -$1,000* | $1,000 | $0 |

*Year 2026 net = $8,000 - $2,000 - $7,000 (carryforward) = -$1,000.

### Order of Application

1. Short-term losses offset short-term gains.
2. Long-term losses offset long-term gains.
3. Net short-term loss offsets net long-term gain (and vice versa).
4. Remaining net loss up to $3,000 offsets ordinary income.
5. Excess carries forward.

## Year-End Strategies

### Strategy 1: Gain-Matching Harvest

Identify all realized gains for the year. Harvest losses equal to those gains to zero out the tax liability. Stop harvesting once gains are fully offset plus the $3K ordinary income deduction.

### Strategy 2: Aggressive Harvest

Harvest every available loss regardless of current gains. Benefits:
- Builds a large carryforward for future years.
- Useful if you expect large gains next year.

Drawbacks:
- Transaction costs on many small positions.
- Opportunity cost of being out of positions for 31 days.

### Strategy 3: Threshold Harvest

Set a minimum loss threshold (e.g., $500 or 10% of position value). Only harvest losses exceeding the threshold to balance tax savings against complexity.

### Strategy 4: Continuous Harvest

Monitor positions throughout the year rather than waiting for year-end. Benefits:
- Captures losses that may recover by December.
- Spreads transaction costs over time.
- Avoids year-end liquidity crunches.

### Year-End Checklist

1. Tally all realized gains and losses year-to-date.
2. Apply any prior-year carryforward.
3. Compute remaining taxable gain.
4. Scan portfolio for unrealized losses.
5. Score and rank harvesting opportunities.
6. Filter by net benefit > 0.
7. Check wash sale windows for recent purchases.
8. Execute harvests with enough time for settlement before Dec 31.
9. Set 31-day reminders for re-entry eligibility.
10. Update carryforward tracker for next year.

## Crypto-Specific Notes

- **IRS Notice 2014-21** treats cryptocurrency as property, subject to capital gains rules.
- The wash sale rule (IRC Section 1091) technically applies to "stock or securities." Whether crypto qualifies is debated, but proposed legislation (e.g., Build Back Better Act) aimed to extend it explicitly to digital assets.
- **Conservative approach**: Treat crypto as subject to wash sales.
- **Aggressive approach**: Argue crypto is not a "security" and wash sales do not apply. This carries audit risk.
- **Cost basis methods**: FIFO is the IRS default; specific identification requires contemporaneous records.
- **Staking rewards**: Received tokens have a cost basis equal to fair market value at time of receipt. These can also generate TLH opportunities if value drops.
